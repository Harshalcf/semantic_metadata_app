import os
import requests
import streamlit as st

# Load environment variables
try:
    from dotenv import load_dotenv
    load_dotenv()
except:
    pass

# Universal loader: Cloud first, then local
API_URL = st.secrets.get("SUMMARY_API_URL", os.getenv("SUMMARY_API_URL"))
API_KEY = st.secrets.get("SUMMARY_API_KEY", os.getenv("SUMMARY_API_KEY"))

headers = {"Authorization": f"Bearer {API_KEY}"}

def split_text_into_chunks(text, max_chunk_size=3000):
    text = text.replace('\n', ' ').strip()
    chunks = []
    while len(text) > max_chunk_size:
        split_index = text.rfind('.', 0, max_chunk_size)
        if split_index == -1:
            split_index = max_chunk_size
        chunks.append(text[:split_index + 1].strip())
        text = text[split_index + 1:].strip()
    if text:
        chunks.append(text)
    return chunks

def call_summarizer_api(text, min_len=40, max_len=150):
    payload = {
        "inputs": text,
        "parameters": {
            "min_length": min_len,
            "max_length": max_len,
            "do_sample": False
        }
    }
    response = requests.post(API_URL, headers=headers, json=payload)
    return response.json()

def generate_summary(text, min_len=40, max_len=150):
    chunks = split_text_into_chunks(text)
    final_summary = ""

    for chunk in chunks:
        response = call_summarizer_api(chunk, min_len, max_len)
        try:
            summary = response[0]['summary_text']
            final_summary += summary.strip() + " "
        except:
            final_summary += "[Summary Failed] "

    return final_summary.strip()
