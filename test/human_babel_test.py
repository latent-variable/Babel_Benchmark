import os
import csv
import json
import random
from datetime import datetime
from bert_score import score

def load_dataset():
    with open("./datasets/babel_encodings.json", "r", encoding="utf-8") as f:
        return json.load(f)

def calculate_bert_score(original_sentence, user_response):
    P, R, F1 = score([user_response], [original_sentence], lang="en", rescale_with_baseline=True, model_type="microsoft/deberta-xlarge-mnli")
    return max(F1.mean().item() * 100, 0.0)

def present_sentence_to_human(sentence_data):
    multilingual_sentence = sentence_data["multilingual_sentence"]
    original_sentence = sentence_data["original_sentence"]

    print(f"\nMultilingual Sentence: {multilingual_sentence}")
    user_response = input("Your Translation: ").strip()

    bert_score = calculate_bert_score(original_sentence, user_response)
    
    print(f"Your Response: {user_response}")
    print(f"\nOriginal Sentence: {original_sentence}")
    print(f"BERTScore: {bert_score:.2f}")

    return bert_score

def save_human_score(model_name, final_score):
    final_score_file = "results/final_scores.csv"

    with open(final_score_file, "a", newline="", encoding="utf-8") as csvfile:
        fieldnames = ["datetime", "model_name", "final_score"]
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

        if csvfile.tell() == 0:
            writer.writeheader()

        writer.writerow({
            "datetime": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "model_name": model_name,
            "final_score": round(final_score, 2)
        })

def main():
    dataset = load_dataset()
    random.shuffle(dataset)

    username = input("Enter your username (or leave blank for 'Human'): ").strip()
    if not username:
        username = "Human"
    model_name = username

    total_score = 0
    rounds_played = 0

    for sentence_data in dataset:
        bert_score = present_sentence_to_human(sentence_data)
        total_score += bert_score
        rounds_played += 1

        continue_playing = input("\nDo you want to play another round? (y/n): ").strip().lower()
        if continue_playing != "y":
            break

    final_score = total_score / rounds_played if rounds_played > 0 else 0
    print(f"\nFinal Score: {final_score:.2f}")

    save_human_score( model_name, final_score)
    print("\nYour score has been saved. Thank you for playing!")

if __name__ == "__main__":
    main()
