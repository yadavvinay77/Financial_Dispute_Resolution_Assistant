# app/api/ingest_text.py

from fastapi import APIRouter
import uuid

from app.services.chunker import clean_text, chunk_text
from app.services.embedding import embed_text
from app.services.vector_store import VectorStore

router = APIRouter()

@router.post("/api/ingest_text")
async def ingest_text(payload: dict):
    raw_text = payload.get("text", "").strip()

    if not raw_text:
        return {"error": "No text provided."}

    case_id = str(uuid.uuid4())[:8]

    cleaned = clean_text(raw_text)
    chunks = chunk_text(cleaned)

    embeddings = []
    valid_chunks = []
    for c in chunks:
        vec = embed_text(c)
        if vec:
            embeddings.append(vec)
            valid_chunks.append(c)

    # FIX: Automatically detect embedding dimension
    vector_db = VectorStore(dim=len(embeddings[0]))
    vector_db.add(embeddings, valid_chunks, case_id)

    summary = cleaned[:500] + "..." if len(cleaned) > 500 else cleaned

    return {
        "case_id": case_id,
        "summary": summary,
        "extracted_text": cleaned
    }
