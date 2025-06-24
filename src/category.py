import requests
from collections import Counter
from src.load_secrets import load_secret

API_URL = load_secret("CLASSIFY_API_URL")
API_KEY = load_secret("CLASSIFY_API_KEY")

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

        if isinstance(result, dict) and "labels" in result and "scores" in result:
            scores[result['labels'][0]] += result['scores'][0]

    best_category = scores.most_common(1)[0][0] if scores else "Unknown"
    return best_category, dict(scores)
