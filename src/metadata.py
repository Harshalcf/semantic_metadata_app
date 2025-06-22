from src.extractor import extract_text
from src.author_title import extract_title, extract_author
from src.date import extract_date
from src.summary import generate_summary
from src.category import detect_category_from_chunks
from src.keywords import extract_keywords

def generate_metadata(text):
    metadata = {
        "title": extract_title(text),
        "author": extract_author(text),
        "date": extract_date(text),
        "summary": generate_summary(text),
        "category": None,
        "category_scores": {},
        "keywords": extract_keywords(text)
    }
    metadata["category"], metadata["category_scores"] = detect_category_from_chunks(text)
    return metadata
