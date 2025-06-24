import streamlit as st
import os
import json
import time
from io import BytesIO
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from reportlab.lib.utils import simpleSplit

# ===== Import functions from your modules =====
from src.extractor import extract_text
from src.metadata import generate_metadata

# ===== Setup folders =====
UPLOAD_DIR = "data/uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)

# ===== Streamlit App Layout =====
st.set_page_config(page_title="Metadata Generator", layout="centered")
st.title("Semantic Metadata Generator")

# ===== PDF Generator Function with Word Wrapping =====
def generate_pdf(metadata):
    buffer = BytesIO()
    c = canvas.Canvas(buffer, pagesize=letter)
    width, height = letter
    text_object = c.beginText(40, height - 50)
    text_object.setFont("Helvetica", 12)

    for key, value in metadata.items():
        if isinstance(value, dict):
            value = json.dumps(value, indent=4)

        wrapped_lines = simpleSplit(f"{key}: {value}", "Helvetica", 12, width - 80)
        for line in wrapped_lines:
            text_object.textLine(line)

        text_object.textLine("")  # Space between fields

    c.drawText(text_object)
    c.showPage()
    c.save()
    buffer.seek(0)
    return buffer

# ===== File Upload Section =====
uploaded_file = st.file_uploader("Upload your document", type=["pdf", "docx", "txt", "jpg", "jpeg", "png"])

if uploaded_file:
    filename = f"{int(time.time())}_{uploaded_file.name}"
    save_path = os.path.join(UPLOAD_DIR, filename)
    with open(save_path, "wb") as f:
        f.write(uploaded_file.read())

    st.success(f"File saved at: `{save_path}`")

    # Extract text
    text = extract_text(save_path)

    # Generate metadata
    with st.spinner("Generating metadata..."):
        metadata = generate_metadata(text)

    # Show metadata in JSON format
    st.subheader("Extracted Metadata (JSON)")
    formatted_json = json.dumps(metadata, indent=4)
    st.code(formatted_json, language="json")

    # Show JSON download button
    st.download_button(
        label="Download Metadata as JSON",
        data=formatted_json,
        file_name="metadata.json",
        mime="application/json"
    )

    # Show PDF download button
    pdf_buffer = generate_pdf(metadata)
    st.download_button(
        label="Download Metadata as PDF",
        data=pdf_buffer,
        file_name="metadata.pdf",
        mime="application/pdf"
    )
 
