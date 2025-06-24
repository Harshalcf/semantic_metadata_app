from PyPDF2 import PdfReader
import docx2txt
from PIL import Image
from pathlib import Path
import requests

def extract_text_from_image(path):
    api_key = 'K82535128888957'  # Free OCR.Space
    ocr_url = 'https://api.ocr.space/parse/image'

    with open(path, 'rb') as f:
        response = requests.post(
            ocr_url,
            files={'filename': f},
            data={'apikey': api_key, 'language': 'eng'}
        )

    result = response.json()

    try:
        return result['ParsedResults'][0]['ParsedText']
    except:
        return "Could not extract text from image."

def extract_text(path):
    file_ext = Path(path).suffix.lower()

    if file_ext == '.pdf':
        reader = PdfReader(path)
        return "\n".join([page.extract_text() for page in reader.pages if page.extract_text()])

    elif file_ext == '.docx':
        return docx2txt.process(path)

    elif file_ext == '.txt':
        with open(path, 'r', encoding='utf-8') as f:
            return f.read()

    elif file_ext in ['.jpg', '.jpeg', '.png']:
        return extract_text_from_image(path)

    return ""
