# app/pipelines/ingest_pipeline.py

from app.services.chunker import clean_text, chunk_text
from app.services.embedding import embed_text
from app.services.vector_store import VectorStore

async def process_document(text: str, case_id: str):
    cleaned = clean_text(text)
    chunks = chunk_text(cleaned)

    embeddings = []
    valid_chunks = []

    for c in chunks:
        vec = embed_text(c)
        if vec:
            embeddings.append(vec)
            valid_chunks.append(c)

    if not embeddings:
        raise ValueError("No embeddings generated.")

    vector_db = VectorStore(dim=len(embeddings[0]))
    vector_db.add(embeddings, valid_chunks, case_id)

    return {
        "case_id": case_id,
        "summary": cleaned[:500] + "..." if len(cleaned) > 500 else cleaned
    }
