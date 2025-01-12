import random
import json
import asyncio
from googletrans import Translator

# Initialize the translator
translator = Translator()

# Sample languages to use (ISO 639-1 language codes)
LANGUAGES = [
    'en',  # English
    'de',  # German
    'ja',  # Japanese
    'ru',  # Russian
    'zh-cn',  # Chinese (Simplified)
    'sk',  # Slovak
    'sv',  # Swedish
    'uk',  # Ukrainian
    'pl',  # Polish
    'no',  # Norwegian
    'ar',  # Arabic
    'fr',  # French
    'es',  # Spanish
    'it',  # Italian
    'hi',  # Hindi
    'ko',  # Korean
    'pt',  # Portuguese
    'nl',  # Dutch
    'fi',  # Finnish
    'tr',  # Turkish
    'cs',  # Czech
    'el',  # Greek
    'he',  # Hebrew
    'id',  # Indonesian
    'ms',  # Malay
    'ro',  # Romanian
    'vi',  # Vietnamese
    'da',  # Danish
    'th',  # Thai
]

# Function to translate each word into a different language
async def translate_to_multilingual(sentence):
    languages = list(LANGUAGES)
    words = sentence.split()
    translated_words = []

    for i, word in enumerate(words):
        lang = random.choice(languages)
        try:
            # Await the async translate function
            translated_word = await translator.translate(word, dest=lang)
            translated_words.append(translated_word.text)
        except Exception as e:
            print(f"Translation error: {e}")
            translated_words.append(word)

        languages.remove(lang)  # Ensure no two consecutive words use the same language

    return " ".join(translated_words)

# Async helper function to load sentences and call the translator
async def process_sentences():
    # Load random sentences from JSON file
    with open("datasets/random_sentences.json", "r", encoding="utf-8") as f:
        sentences = json.load(f)

    translations = []
    # Translate sentences
    for sentence in sentences:
        original_sentence = sentence['original_sentence']
        translated = await translate_to_multilingual(original_sentence)
        print(translated)
        translations.append({"original_sentence": original_sentence, "multilingual_sentence": translated})

    # Save translations to a new JSON file
    with open("datasets/babel_encodings.json", "w", encoding="utf-8") as f:
        json.dump(translations, f, ensure_ascii=False, indent=4)


# Run the async process
asyncio.run(process_sentences())

print("Encoding generated and saved to datasets/babel_encodings.json")
