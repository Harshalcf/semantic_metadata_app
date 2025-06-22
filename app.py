import spacy
import importlib.util

def ensure_spacy_model():
    model_name = "en_core_web_sm"
    if importlib.util.find_spec(model_name) is None:
        spacy.cli.download(model_name)

ensure_spacy_model()
import spacy
import importlib.util

def ensure_spacy_model():
    model_name = "en_core_web_sm"
    if importlib.util.find_spec(model_name) is None:
        spacy.cli.download(model_name)

ensure_spacy_model()

import streamlit as st
import os
import json

# ===== Streamlit cache decorators for optimization =====
from transformers import pipeline

@st.cache_resource
def load_summarizer():
    return pipeline("summarization", model="facebook/bart-large-cnn", device=0)

@st.cache_resource
def load_classifier():
    return pipeline("zero-shot-classification", model="facebook/bart-large-mnli", device=0)

# ===== Import functions from your modules =====
from src.extractor import extract_text
from src.metadata import generate_metadata

# ===== Setup folders =====
UPLOAD_DIR = "data/uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)

# ===== Streamlit App Layout =====
st.set_page_config(page_title="Metadata Generator", layout="centered")
st.title("Semantic Metadata Generator")

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
    @st.cache_data
    def get_text(path):
        return extract_text(path)

    with st.spinner("Extracting text..."):
        text = get_text(save_path)

    # Generate metadata
    @st.cache_data
    def get_metadata(t):
        return generate_metadata(t)

    with st.spinner("Generating metadata..."):
        metadata = get_metadata(text)

    # Show metadata in JSON format
    st.subheader("Extracted Metadata (JSON)")
    formatted_json = json.dumps(metadata, indent=4)
    st.code(formatted_json, language="json")  # Pretty format

    # Show download button
    st.download_button(
        label="Download Metadata as JSON",
        data=formatted_json,
        file_name="metadata.json",
        mime="application/json"
    )

    # Clear & Upload another file button
    if st.button("Clear & Upload Another File"):
        st.cache_data.clear()
        st.rerun()
