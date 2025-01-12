import openai
import os
import json
import requests
import random

THEMES = [
    "Space Exploration", "Ancient History", "Fantasy", "Science Fiction",
    "Nature and Wildlife", "Adventure and Exploration", "Mystery and Crime",
    "Love and Relationships", "Sports and Games", "Cooking and Food",
    "Music and Art", "Weather and Seasons", "Technology and Gadgets",
    "Travel and Culture", "Philosophy and Wisdom", "Animals and Pets",
    "Daily Life", "Dreams and Imagination", "Horror and Suspense", "Comedy and Humor"
]

# Load your OpenAI API key from environment variables or configuration file
# Make sure the environment variable 'OPENAI_API_KEY' is set before running the script
openai.api_key = os.getenv("OPENAI_API_KEY")
NUM_SENTENCES  = int(os.getenv("NUM_SENTENCES",  10))

# Define a prompt to instruct the LLM to generate random sentences
PROMPT = """Generate a random, unique, and diverse English sentence of 5-10 words. The sentence should be grammatically correct, coherent, and meaningful. Ensure that the generated sentences include a variety of themes, structures, and vocabulary to enhance diversity. The output must be a complete sentence, and you must ONLY respond with the sentence. Do NOT provide any additional notes, explanations, or comments.

### Example Outputs:
1. A curious cat chased shadows across the garden.
2. A rainbow appeared after the sudden summer rainstorm.
3. She danced gracefully beneath the shimmering northern lights.
4. Hard robot discovered emotions in a forgotten dusty library.
5. An owl hooted softly as the moon rose over the hill.
6. A lonely fisherman cast his net into the quiet sea.
7. Time travelers often forgot their keys in different centuries.
8. The ancient tree whispered secrets to the wandering traveler.
9. A playful puppy splashed through the puddles of rain.
10. Her laughter echoed through the silent empty corridor.

Ensure creativity and diversity across all generated sentences. Avoid repetition of common phrases and strive for originality. Stick to English and keep the single sentences between 5 to 10 words.
"""
def get_random_theme():
    return random.choice(THEMES)

# Function to generate random sentences using OpenAI API
def generate_openai_sentences():
    sentences = []
    for _ in range(NUM_SENTENCES):
         # Add a random THEME
        random_theme = get_random_theme()
        salt = f"\nGenerate a random sentence with the theme: {random_theme}"
        # Make an API call to OpenAI to generate the sentences
        response = openai.Completion.create(
            engine=os.getenv("MODEL"),  # Specify the LLM engine to use
            prompt=PROMPT+salt,  # Provide the instruction prompt to the LLM
            max_tokens=200,  # Limit the number of tokens in the response
            stop=None,  # No specific stopping condition for the LLM
            temperature=0.7  # Controls randomness; higher value makes output more diverse
        )

        # Extract and clean the generated sentences from the response
        sentence = response.choices[0].text.strip()
        sentences.append({"original_sentence":sentence.strip()})

    return sentences

# Function to generate random sentences using Ollama API
def generate_ollama_sentences():

    url = os.getenv("OLLAMA_HOST", "http://localhost:11434")
    headers = {"Content-Type": "application/json"}

    sentences = []
    for _ in range(NUM_SENTENCES):

        # Add a random THEME
        random_theme = get_random_theme()
        salt = f"\nGenerate a random sentence with the theme: {random_theme}"
        data = {
            "model": os.getenv("MODEL"),
            "prompt": PROMPT+salt,
            "stream": False
        }
        try:
            # Make a POST request to the Ollama server
            response = requests.post(f"{url}/api/generate", headers=headers, json=data)
            if response.status_code != 200:
                print(f"Error: {response.status_code} - {response.text}")
        
            response.raise_for_status()
            result = response.json()
            
            # Extract sentences from the Ollama response
            sentence = result.get("response", "")
            print(sentence)
            sentences.append({"original_sentence": sentence.strip()})
        except requests.exceptions.RequestException as e:
            print(f"Error generating sentences with Ollama: {e}")
        
    return sentences

# Choose the generation method based on availability
if os.getenv("USE_OLLAMA") == "true":
    sentences = generate_ollama_sentences()
else:
    sentences = generate_openai_sentences()

# Save generated sentences to a JSON file
with open("datasets/random_sentences.json", "w", encoding="utf-8") as f:
    json.dump(sentences, f, ensure_ascii=False, indent=4)  # Ensure the JSON is human-readable

# Print a confirmation message once the file is saved
print("Random sentences generated and saved to datasets/random_sentences.json")
