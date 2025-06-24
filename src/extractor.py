from PyPDF2 import PdfReader
import docx2txt
from pathlib import Path
from PIL import Image
import requests
import os
import streamlit as st

# Try loading from .env (local) or Streamlit secrets (cloud)
try:
    from dotenv import load_dotenv
    load_dotenv()
except:
    pass

# Universal loader: Cloud secrets first, fallback to local .env
OCR_API_KEY = st.secrets.get("OCR_API_KEY", os.getenv("OCR_API_KEY"))
OCR_API_URL = st.secrets.get("OCR_API_URL", os.getenv("OCR_API_URL"))

def extract_text_from_image(path):
    if not OCR_API_KEY or not OCR_API_URL:
        return "OCR API key or URL not set."

    with open(path, 'rb') as f:
        response = requests.post(
            OCR_API_URL,
            files={'filename': f},
            data={'apikey': OCR_API_KEY, 'language': 'eng'}
        )

    try:
        result = response.json()
        return result['ParsedResults'][0]['ParsedText']
    except Exception as e:
        return f"OCR Error: {str(e)}"

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

    return "Unsupported file format."
