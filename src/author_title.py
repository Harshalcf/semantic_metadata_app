import re
from transformers import pipeline

# Load Hugging Face NER pipeline
#ner = pipeline("ner", model="dslim/bert-base-NER", aggregation_strategy="simple")
ner = pipeline("ner", model="dslim/bert-base-NER", tokenizer="dslim/bert-base-NER", aggregation_strategy="simple")

def extract_title(text):
    lines = text.strip().split("\n")
    lines = [line.strip() for line in lines if line.strip()]

    for line in lines:
        if 5 < len(line) < 100 and line[0].isupper():
            return line

    return lines[0] if lines else "Unknown Title"

def extract_author(text):
    lines = text.strip().split('\n')
    for line in lines:
        match = re.search(r"\b(By|Written by|Author:)\s+([A-Z][a-z]+(?:\s+[A-Z][a-z]+)+)", line.strip())
        if match:
            return match.group(2)

    results = ner(text)
    for ent in results:
        if ent.get("entity_group") == "PER":
            return ent.get("word")

    return "Unknown Author"
