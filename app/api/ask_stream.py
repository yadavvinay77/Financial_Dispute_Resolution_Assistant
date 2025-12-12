from fastapi import APIRouter
from fastapi.responses import StreamingResponse

from app.pipelines.rag_pipeline import retrieve_evidence
from app.services.llm_engine import stream_llm_answer

router = APIRouter()


@router.get("/api/ask_stream")
async def ask_stream(case_id: str, question: str):
    evidence_chunks = retrieve_evidence(question, top_k=5)

    return StreamingResponse(
        stream_llm_answer(question, evidence_chunks),
        media_type="text/event-stream",
        headers={
            "Cache-Control": "no-cache",
            "Connection": "keep-alive",
        }
    )
