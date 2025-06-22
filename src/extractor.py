from PyPDF2 import PdfReader
import docx2txt
import pytesseract
import cv2
from pathlib import Path

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
        img = cv2.imread(path)
        return pytesseract.image_to_string(img)

    return ""