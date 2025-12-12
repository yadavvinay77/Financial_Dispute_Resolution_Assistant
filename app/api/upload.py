# app/api/upload.py

from fastapi import APIRouter, UploadFile, File
from app.services.pdf_extractor import extract_text_from_pdf
from app.pipelines.ingest_pipeline import process_document

router = APIRouter()

@router.post("/api/upload")
async def upload_pdf(file: UploadFile = File(...)):
    # Read file ONCE
    file_bytes = await file.read()

    # Extract text + case_id
    case_id, extracted_text = extract_text_from_pdf(file_bytes)

    # Ingest extracted text
    result = await process_document(extracted_text, case_id)

    return {
        "case_id": case_id,
        "summary": result["summary"],
        "extracted_text": extracted_text
    }
