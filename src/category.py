from transformers import pipeline
from collections import Counter

classifier = pipeline("zero-shot-classification", model="facebook/bart-large-mnli", tokenizer="facebook/bart-large-mnli")


def detect_category_from_chunks(text, candidate_labels=None, max_chunk_size=1000):
    if candidate_labels is None:
        candidate_labels = ["Finance", "Health", "Education", "Politics", "Technology", "History", "Philosophy", "Biography", "Science", "Fiction"]

    chunks = [text[i:i+max_chunk_size] for i in range(0, len(text), max_chunk_size)]
    scores = Counter()

    for chunk in chunks:
        result = classifier(chunk, candidate_labels)
        scores[result['labels'][0]] += result['scores'][0]

    best_category = scores.most_common(1)[0][0]
    return best_category, dict(scores)
