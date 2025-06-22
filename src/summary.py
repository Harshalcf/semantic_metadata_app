from transformers import pipeline
import torch

# Use GPU if available, else CPU
device = 0 if torch.cuda.is_available() else -1

summarizer = pipeline("summarization", model="facebook/bart-large-cnn", device=device)

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

def generate_summary(text, min_len=40, max_len=150):
    chunks = split_text_into_chunks(text)
    final_summary = ""
    for chunk in chunks:
        summary = summarizer(chunk, max_length=max_len, min_length=min_len, do_sample=False)[0]['summary_text']
        final_summary += summary.strip() + " "
    return final_summary.strip()
