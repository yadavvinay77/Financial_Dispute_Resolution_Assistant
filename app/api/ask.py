# app/api/ask.py

from fastapi import APIRouter
from pydantic import BaseModel
from typing import Any, Dict

from app.services.llm_engine import ask_llm_json
from app.services.classifier import ClassifierService
from app.pipelines.rag_pipeline import retrieve_evidence
from app.services.recommender import recommend_steps

router = APIRouter()


class AskRequest(BaseModel):
    case_id: str
    question: str


# ---------------- HELPERS ----------------

def infer_llm_classification(text: str) -> str:
    t = text.lower()

    if any(k in t for k in ["loan", "interest", "mortgage", "repayment"]):
        return "Loans"
    if any(k in t for k in ["credit card", "card"]):
        return "Credit Card"
    if any(k in t for k in ["fraud", "scam", "unauthorised"]):
        return "Fraud"
    if "insurance" in t:
        return "Insurance"

    return "Banking Service"


def infer_severity(text: str) -> float:
    t = text.lower()
    score = 0.3  # slightly higher baseline

    if "financial difficulty" in t or "financial difficulties" in t:
        score += 0.3
    if "without notifying" in t or "without telling" in t:
        score += 0.2
    if "complaint" in t or "complained" in t:
        score += 0.1

    return min(score, 1.0)


def normalize_llm_output(raw: Any) -> Dict[str, Any]:
    """
    Ensures LLM output is always a dict with safe defaults.
    """
    # Case 1: already correct dict
    if isinstance(raw, dict):
        # unwrap {"response": {...}}
        if "response" in raw and isinstance(raw["response"], dict):
            return raw["response"]
        return raw

    # Case 2: string response
    if isinstance(raw, str):
        return {
            "answer": raw,
            "summary": raw
        }

    # Fallback
    return {
        "answer": "",
        "summary": ""
    }


# ---------------- MAIN ENDPOINT ----------------

@router.post("/api/ask")
async def ask_question(payload: AskRequest):
    question = payload.question

    # 1️⃣ Retrieve evidence
    evidence = retrieve_evidence(question)

    # 2️⃣ Ask LLM
    raw_llm = ask_llm_json(question, evidence)

    # 🔥 CRITICAL FIX
    llm_result = normalize_llm_output(raw_llm)

    answer = llm_result.get("answer", "")
    summary = llm_result.get("summary", answer)
    key_points = llm_result.get("key_points", [])

    # 3️⃣ Classification
    classification_llm = llm_result.get(
        "classification",
        infer_llm_classification(summary or answer)
    )

    # 4️⃣ Severity
    severity = llm_result.get(
        "severity",
        infer_severity(summary or answer)
    )

    # 5️⃣ ML classifier (safe fallback)
    clf = ClassifierService()
    ml_class, ml_conf = clf.predict(summary or answer)

    # 6️⃣ Recommendations
    recommendations = recommend_steps(classification_llm, severity)

    return {
        "answer": answer,
        "summary": summary,
        "classification_llm": classification_llm,
        "classification_ml": ml_class,
        "ml_confidence": ml_conf,
        "severity": severity,
        "key_points": key_points,
        "evidence": evidence,
        "recommendations": recommendations,
    }
