import json
import csv
import requests
from datetime import datetime
import os
from bert_score import score
import warnings

# Suppress warnings
warnings.filterwarnings("ignore")

# Load environment variables
OLLAMA_URL = os.getenv("OLLAMA_HOST", "http://localhost:11434")
OLLAMA_MODEL = os.getenv("OLLAMA_MODEL", "llama3.2")

PROMPT = """Given a multilingual sentence where each word is in a different language and native script, translate it back into English. Ensure that the output is a coherent English sentence that matches the original meaning.

### Example 1:
Der 迅速な коричневый 狐 skáče över собаку leniwy hund

### Expected Output:
The quick brown fox jumps over the lazy dog.

### Example 2:
El gato 快速的 черный chat прыгать su perro 

### Expected Output:
The fast black cat jumps over his dog.

### Example 3:
La maison 快速的 дом house находится près de леса

### Expected Output:
The house is near the forest.

### Important Instructions:
(Note: You must only respond with the predicted expected sentence and nothing else! Do not include any notes, explanations, or additional text.)
(Note: Your response will be directly compared for accuracy with the original sentence, so it is crucial that your response is only the translation!)
### Input:
"""

# Function to call the Ollama API for predictions
def get_ollama_prediction(multilingual_sentence):
    headers = {"Content-Type": "application/json"}
    
    data = {
        "model": OLLAMA_MODEL,
        "prompt": PROMPT + multilingual_sentence,
        "stream": False
    }

    try:
        response = requests.post(f"{OLLAMA_URL}/api/generate", headers=headers, json=data)
        if response.status_code != 200:
            print(f"Error: {response.status_code} - {response.text}")
        
        response.raise_for_status()
        result = response.json()

        # Extract sentences from the Ollama response and remove anything after the first period
        response_text = result.get("response", "")
        if "." in response_text:
            cleaned_response = response_text[:response_text.index(".") + 1]
        else:
            cleaned_response = response_text
        return cleaned_response.strip()
    except requests.exceptions.RequestException as e:
        print(f"Error calling Ollama: {e}")
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

    # Call the Ollama model to get the prediction
    predicted_sentence = get_ollama_prediction(multilingual_sentence).split()

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
        "model_name": OLLAMA_MODEL
    })

# Calculate the final model score
final_bert_score = total_bert_score / len(translations)
print(f'Final BERTscores: {final_bert_score}' )

# Write results to a CSV file
with open("results/results.csv", "w", newline="", encoding="utf-8") as csvfile:
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
        "model_name": OLLAMA_MODEL,
        "final_bert_score": round(final_bert_score, 2)
    })

print("Results have been saved to results.csv")
print("Final scores have been appended to final_scores.csv")
