# semantic_metadata_app
Streamlit application for semantic metadata generation from documents

## Semantic Metadata Generator
This Streamlit app automatically generates semantic metadata from documents like PDFs, DOCX files, TXT files, and Images.

It extracts:

Title

Author

Date

Category (using Zero-Shot Classification)

Summary (using Summarization API)

Keywords

OCR support for images via API

Both local system and Streamlit Cloud are supported using .env or Streamlit Secrets.

## Features
Supports PDF, DOCX, TXT, Images (.jpg, .jpeg, .png).

Image text extraction using ocr.space API (Free API key works).

Summarization using Hugging Face API.

Category detection using Zero-Shot Classification API.

Author detection using Named Entity Recognition (NER) API.

Supports JSON and PDF download of extracted metadata.

Clean separation between local and cloud environment variables.