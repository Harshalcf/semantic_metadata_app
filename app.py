import streamlit as st
import os
import json
from io import BytesIO
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas

# ===== Import functions from your modules =====
from src.extractor import extract_text
from src.metadata import generate_metadata

# ===== Setup folders =====
UPLOAD_DIR = "data/uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)

# ===== Streamlit App Layout =====
st.set_page_config(page_title="Metadata Generator", layout="centered")
st.title("Semantic Metadata Generator")

# ===== PDF Generation Function =====
def generate_pdf(metadata):
    buffer = BytesIO()
    c = canvas.Canvas(buffer, pagesize=letter)
    width, height = letter
    text_object = c.beginText(40, height - 50)

    text_object.setFont("Helvetica", 12)

    for key, value in metadata.items():
        text_object.textLine(f"{key}: {value}")
        text_object.textLine("")  # Add space between entries

    c.drawText(text_object)
    c.showPage()
    c.save()
    buffer.seek(0)
    return buffer

# ===== File Upload Section =====
uploaded_file = st.file_uploader("Upload your document", type=["pdf", "docx", "txt", "jpg", "jpeg", "png"])

if uploaded_file:
    # Save file permanently
    import time
    filename = f"{int(time.time())}_{uploaded_file.name}"
    save_path = os.path.join(UPLOAD_DIR, filename)
    with open(save_path, "wb") as f:
        f.write(uploaded_file.read())

    st.success(f"File saved at: `{save_path}`")

    # Extract text
    def get_text(path):
        return extract_text(path)

    with st.spinner("Extracting text..."):
        text = get_text(save_path)

    # Generate metadata
    def get_metadata(t):
        return generate_metadata(t)

    with st.spinner("Generating metadata..."):
        metadata = get_metadata(text)

    # Show metadata in JSON format
    st.subheader("Extracted Metadata (JSON)")
    formatted_json = json.dumps(metadata, indent=4)
    st.code(formatted_json, language="json")  # Pretty format

    # Show download button for JSON
    st.download_button(
        label="Download Metadata as JSON",
        data=formatted_json,
        file_name="metadata.json",
        mime="application/json"
    )

    # Show download button for PDF
    pdf_file = generate_pdf(metadata)
    st.download_button(
        label="Download Metadata as PDF",
        data=pdf_file,
        file_name="metadata.pdf",
        mime="application/pdf"
    )

    # Clear & Upload another file button
    if st.button("Clear & Upload Another File"):
        st.rerun()
