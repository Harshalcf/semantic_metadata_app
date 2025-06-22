import re
import spacy

nlp = spacy.load("en_core_web_sm")

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

    doc = nlp(text)
    for ent in doc.ents:
        if ent.label_ == "PERSON":
            return ent.text

    return "Unknown Author"