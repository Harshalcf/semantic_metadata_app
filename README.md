# semantic_metadata_app
Streamlit application for semantic metadata generation from documents

📄 Semantic Metadata Generator
This Streamlit app automatically generates semantic metadata from documents like PDFs, DOCX files, TXT files, and Images.

It extracts:

📌 Title

✍️ Author

🗓️ Date

🗂️ Category (using Zero-Shot Classification)

📝 Summary (using Summarization API)

🔑 Keywords

🖼️ OCR support for images via API

Both local system and Streamlit Cloud are supported using .env or Streamlit Secrets.