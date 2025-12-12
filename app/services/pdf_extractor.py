# app/services/pdf_extractor.py

import pdfplumber
import uuid
from pathlib import Path

UPLOAD_DIR = Path("data/uploads")
UPLOAD_DIR.mkdir(parents=True, exist_ok=True)

def extract_text_from_pdf(file_bytes):
    case_id = uuid.uuid4().hex[:8]
    pdf_path = UPLOAD_DIR / f"{case_id}.pdf"

    with open(pdf_path, "wb") as f:
        f.write(file_bytes)

    text = ""
    with pdfplumber.open(pdf_path) as pdf:
        for p in pdf.pages:
            page_text = p.extract_text() or ""
            text += page_text + "\n"

    return case_id, text.strip()
