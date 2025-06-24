import re
import requests
from src.load_secrets import load_secret

NER_API_URL = load_secret("NER_API_URL")
NER_API_KEY = load_secret("NER_API_KEY")

headers = {"Authorization": f"Bearer {NER_API_KEY}"}

def call_ner_api(text):
    payload = {"inputs": text}
    response = requests.post(NER_API_URL, headers=headers, json=payload)
    return response.json()

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

    results = call_ner_api(text)

    try:
        for ent in results[0]['entities']:
            if ent.get("entity_group", ent.get("entity")) == "PER":
                return ent.get("word")
    except:
        pass

    return "Unknown Author"
