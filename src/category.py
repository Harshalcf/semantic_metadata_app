import os
import requests
from dotenv import load_dotenv
from collections import Counter

# Load environment variables
load_dotenv()

API_URL = os.getenv("CLASSIFY_API_URL")
API_KEY = os.getenv("CLASSIFY_API_KEY")

headers = {"Authorization": f"Bearer {API_KEY}"}

def query_zero_shot(text, labels):
    payload = {
        "inputs": text,
        "parameters": {
            "candidate_labels": labels
        }
    }
    response = requests.post(API_URL, headers=headers, json=payload)
    return response.json()

def detect_category_from_chunks(text, candidate_labels=None, max_chunk_size=1000):
    if candidate_labels is None:
        candidate_labels = ["Finance", "Health", "Education", "Politics", "Technology", "History", "Philosophy", "Biography", "Science", "Fiction"]

    chunks = [text[i:i+max_chunk_size] for i in range(0, len(text), max_chunk_size)]
    scores = Counter()

    for chunk in chunks:
        result = query_zero_shot(chunk, candidate_labels)

        # Safely get highest label and score
        if "labels" in result and "scores" in result:
            scores[result['labels'][0]] += result['scores'][0]

    best_category = scores.most_common(1)[0][0] if scores else "Unknown"
    return best_category, dict(scores)
