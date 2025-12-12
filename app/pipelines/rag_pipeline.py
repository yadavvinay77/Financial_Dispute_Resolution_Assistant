# app/pipelines/rag_pipeline.py

from app.services.embedding import embed_text
from app.services.vector_store import VectorStore

def retrieve_evidence(question: str, top_k: int = 5):
    """
    Retrieves top-k relevant chunks from GLOBAL FAISS vector store.
    """

    # Load existing FAISS index
    vector_db = VectorStore()

    # Embed question
    q_embed = embed_text(question)
    if not q_embed:
        return []

    # ✅ FIX: use k instead of top_k
    results = vector_db.search(q_embed, k=top_k)

    # Return chunk text only
    return [r["chunk"] for r in results]
