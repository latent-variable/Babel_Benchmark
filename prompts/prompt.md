# Babel Benchmark Prompt

**Objective:** Generate multilingual sentences where each word is translated into a different language, using the native script of that language. The goal is to challenge participants (humans or AI) to decipher the original English sentence from the multilingual version.

---

## Prompt for Dataset Generation:
Generate a random, unique, and diverse English sentence of 5-10 words. The sentence should be grammatically correct, coherent, and meaningful. Ensure that the generated sentences include a variety of themes, structures, and vocabulary to enhance diversity. The output must be a complete sentence, and you must ONLY respond with the sentence. Do NOT provide any additional notes, explanations, or comments.

### Example Outputs:
1. The curious cat chased shadows across the garden.
2. A rainbow appeared after the sudden summer rainstorm.
3. She danced gracefully beneath the shimmering northern lights.
4. The robot discovered emotions in a forgotten dusty library.
5. An owl hooted softly as the moon rose over the hill.
6. A lonely fisherman cast his net into the quiet sea.
7. Time travelers often forgot their keys in different centuries.
8. The ancient tree whispered secrets to the wandering traveler.
9. A playful puppy splashed through the puddles of rain.
10. Her laughter echoed through the silent empty corridor.

Ensure creativity and diversity across all generated sentences. Avoid repetition of common phrases and strive for originality. Stick to English and keep the single sentences between 5 to 10 words.


## Sentence Ecoding:
Note: The translations are performed using the Google Translate API, which may introduce slight variations in the output compared to manual translations or other APIs.
```
### Example Outputs:
```json
{
  "original_sentence": "The quick brown fox jumps over the lazy dog.",
  "multilingual_sentence": "Der 迅速な коричневый 狐 skáče über собаку leniwy hund"
}
```
```json
{
  "original_sentence": "She bought some fruits at the market.",
  "multilingual_sentence": "Elle 買った несколько الفواكه auf 市場"
}
```
```json
{
  "original_sentence": "I am going to the store.",
  "multilingual_sentence": "Je 私 gehen إلى متجر"
}
```
---

## Prompt for Model Evaluation:
Given a multilingual sentence where each word is in a different language and native script, translate it back into English. Ensure that the output is a coherent English sentence that matches the original meaning.

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

---

**Use Cases:**

- **Benchmark Testing:** Evaluate the multilingual comprehension of AI models.
- **Human vs. AI Challenge:** Test human participants' ability to decipher multilingual sentences.
- **Dataset Creation:** Generate multilingual datasets for further analysis and training.

