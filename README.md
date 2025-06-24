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

## Clone the repo
git clone https://github.com/Harshalcf/semantic_metadata_app.git
cd semantic_metadata_app

## Create a virtual environment
conda create -n meta-gen python=3.10
conda activate meta-gen

## Install requirements
pip install -r requirements.txt

# What We Learned
Using API-based NLP processing significantly reduces load on local and cloud resources, making the app faster and lighter.

Streamlit's secrets.toml and .env need careful setup for smooth cloud deployment.

Large files and complex models can overload local devices — APIs offer a scalable solution.

pytesseract is not cloud-friendly without manual server setup — using online OCR services like ocr.space is a better option for cross-platform deployment.

Modularizing the app into extractor.py, summary.py, category.py, and author_title.py files improves maintainability and scalability.

# Mistakes and Challenges
Initially tried to deploy heavy local models like spacy and transformers directly on the cloud which led to severe performance issues and deployment errors.

Faced multiple dependency conflicts and version mismatches (tokenizers, transformers).

pytesseract was not supported on Streamlit Cloud, which forced a shift to API-based OCR.

Encountered API timeout and rate-limiting issues due to using free API keys without proper optimization.

# Real-World Usage
This app is production-ready for small to medium-scale deployments such as:

Automating metadata generation for research papers, contracts, or corporate documents.

Scanning physical documents using OCR to digitize and extract metadata.

Educational tools that summarize and categorize large reading materials.

Backend services for document management systems that require automatic tagging and metadata enrichment.
