import os 
import csv
import json
import requests
from datetime import datetime
import warnings
from bert_score import score
from time import sleep


# Suppress warnings
warnings.filterwarnings("ignore")


# Load environment variables
OLLAMA_HOST = os.getenv("OLLAMA_HOST", "http://localhost:11434")
MODEL = os.getenv("MODEL", "llama3.2")
OPENROUTER_API_KEY = os.getenv('OPENROUTER_API_KEY')
USE_OLLAMA = os.getenv("USE_OLLAMA", "True").lower() in ("true", "1", "yes")


PROMPT = """Given a multilingual sentence where each word is in a different language and native script, translate it back into English. You are allowed to provide reasoning or explanations to arrive at your answer, but the final output must be formatted as a JSON object with the key 'answer'.

Example Input:

Der 迅速な коричневый 狐 skáče över собаку leniwy hund

Reasoning:

'Der' is a German word meaning 'The'.

'迅速な' is a Japanese word meaning 'quick'.

'коричневый' is a Russian word meaning 'brown'.
...

Final Output:

{"answer": "The quick brown fox jumps over the lazy dog."}

Example Input:

El gato 快速的 черный chat прыгать su perro

Reasoning:

'El gato' is Spanish for 'The cat'.

'快速的' is Chinese for 'fast'.

'черный' is Russian for 'black'.
...

Final Output:

{"answer": "The fast black cat jumps over his dog."}

Important Instructions:

You are allowed provide reasoning and explanations to support your translation process but its is not required.

No two words in the sentence are from the same language.

The final output must be a valid JSON object with the key 'answer'.
Note: FAILURE TO COMPLY WITH THE EXPECTED ANSWERFORMAT WILL RESULT IN A SCORE OF 0% FOR THIS TASK.

Input:"""

def parse_answer(response_text):
    try:
        # Find the part of the response that looks like a JSON object
        start_index = response_text.find('{')
        end_index = response_text.rfind('}') + 1
        
        # Extract and parse the JSON
        json_str = response_text[start_index:end_index]
        parsed_json = json.loads(json_str)
        
        # Return the answer value
        return parsed_json.get("answer", "").strip()
    except (json.JSONDecodeError, AttributeError) as e:
        print(f"Error parsing answer: {e}")
        return ""

# Function to call the Ollama API for predictions
def get_ollama_prediction(prompt):
    headers = {"Content-Type": "application/json"}
    
    data = {
        "model": MODEL,
        "prompt":  prompt,
        "stream": False
    }

    try:
        response = requests.post(f"{OLLAMA_HOST}/api/generate", headers=headers, json=data)
        if response.status_code != 200:
            print(f"Error: {response.status_code} - {response.text}")
        
        response.raise_for_status()
        result = response.json()

        # Extract sentences from the Ollama response and remove anything after the first period
        response_text = result.get("response", "")

        answer = parse_answer(response_text)
        if answer == "":
            print('Trying again!')
            answer = get_ollama_prediction(prompt)

        return answer
    except requests.exceptions.RequestException as e:
        print(f"Error calling Ollama: {e}")
        return ""
    

# Function to call the OpenRouter API for predictions
def get_openrouter_prediction(prompt):
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {OPENROUTER_API_KEY}"
    }

    data = {
        "model": MODEL,
        "messages": [
            {"role": "user", "content": prompt}
        ]
    }
    try:
        response = requests.post("https://openrouter.ai/api/v1/chat/completions", headers=headers, json=data)
        if response.status_code != 200:
            print(f"Error: {response.status_code} - {response.text}")
        
        response.raise_for_status()
        result = response.json()

        if "choices" not in result:
            print('API issues... trying again', str(result)[:100])
            sleep(10)
            return get_openrouter_prediction(prompt)
        
        # Extract sentences from the OpenRouter response
        response_text = result["choices"][0]["message"]["content"]
        answer = parse_answer(response_text)
        if answer == "":
            print('Invalid format... Trying again!')
            answer = get_openrouter_prediction(prompt)
        return answer
    except requests.exceptions.RequestException as e:
        print(f"Error calling OpenRouter: {e}")
        return ""

# Load the dataset
with open("./datasets/babel_encodings.json", "r", encoding="utf-8") as f:
    translations = json.load(f)

# Prepare the results list and initialize accuracy sum
results = []
total_bert_score = 0

# Iterate through each item in the dataset
for i, item in enumerate(translations):
    original_sentence = item["original_sentence"].split()
    multilingual_sentence = item["multilingual_sentence"]

    full_prompt = PROMPT + multilingual_sentence 

    # Call the Ollama model to get the prediction
    if USE_OLLAMA:
        predicted_sentence = get_ollama_prediction(full_prompt).split()
    else:
        predicted_sentence = get_openrouter_prediction(full_prompt).split()

    # Calculate BERTScore
    P, R, F1 = score([" ".join(predicted_sentence)], [" ".join(original_sentence)], lang="en", rescale_with_baseline=True, model_type="microsoft/deberta-xlarge-mnli" )
    bert_f1 = max(F1.mean().item() * 100, 0.0)
    total_bert_score += bert_f1

    print(f'\n{i+1}/{len(translations)}: Orig: {" ".join(original_sentence)}')
    print(f'{i+1}/{len(translations)}: Pred: {" ".join(predicted_sentence)} - BERTScore: {bert_f1:.2f}')

    # Append results to the list
    results.append({
        "original_sentence": " ".join(original_sentence),
        "multilingual_sentence": multilingual_sentence,
        "predicted_sentence": " ".join(predicted_sentence),
        "bert_score": round(bert_f1, 2),
        "model_name": MODEL
    })

# Calculate the final model score
final_bert_score = total_bert_score / len(translations)
print(f'Final BERTscores: {final_bert_score}' )

# Write results to a CSV file
model_name_file = MODEL.replace('/','_')
with open(f"results/{model_name_file}_results.csv", "w", newline="", encoding="utf-8") as csvfile:
    fieldnames = ["original_sentence", "multilingual_sentence", "predicted_sentence", "bert_score", "model_name"]
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

    writer.writeheader()
    for result in results:
        writer.writerow(result)

# Append the final score to a separate CSV file
final_score_file = "results/final_scores.csv"
with open(final_score_file, "a", newline="", encoding="utf-8") as csvfile:
    fieldnames = ["datetime", "model_name", "final_bert_score"]
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

    # Write header if the file is empty
    if csvfile.tell() == 0:
        writer.writeheader()

    # Append the final score
    writer.writerow({
        "datetime": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "model_name": model_name_file,
        "final_bert_score": round(final_bert_score, 2)
    })

print("Results have been saved to results.csv")
print("Final scores have been appended to final_scores.csv")
