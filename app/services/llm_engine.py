# app/services/llm_engine.py

import json
import requests

OLLAMA_URL = "http://localhost:11434/api/generate"
MODEL_NAME = "llama3.1:8b"

# ---------------- PROMPTS ----------------

def build_stream_prompt(question: str, evidence: list) -> str:
    ev = "\n".join(f"- {e}" for e in evidence) if evidence else "No evidence found."

    return f"""
You are an assistant for the UK Financial Ombudsman Service.

Use ONLY the evidence below.
Answer clearly in plain English.
DO NOT return JSON.
DO NOT mention evidence explicitly.

EVIDENCE:
{ev}

QUESTION:
{question}
"""

def build_json_prompt(question: str, evidence: list) -> str:
    ev = "\n".join(f"- {e}" for e in evidence) if evidence else "No evidence found."

    return f"""
You are an assistant for the UK Financial Ombudsman Service.

Use ONLY the evidence below.

EVIDENCE:
{ev}

QUESTION:
{question}

Return ONLY valid JSON with these fields:
answer (string)
summary (string)
classification (string)
severity (number between 0 and 1)
key_points (list of strings)
"""

# ---------------- STREAMING (TEXT ONLY) ----------------

def stream_llm_answer(question: str, evidence: list):
    payload = {
        "model": MODEL_NAME,
        "prompt": build_stream_prompt(question, evidence),
        "stream": True,
        "options": {"temperature": 0.2}
    }

    resp = requests.post(OLLAMA_URL, json=payload, stream=True)

    for line in resp.iter_lines():
        if not line:
            continue
        try:
            data = json.loads(line.decode("utf-8"))
            token = data.get("response", "")
            if token:
                yield f"data: {token}\n\n"
        except:
            continue

    # ✅ SIGNAL STREAM COMPLETION
    yield "data: [DONE]\n\n"

# ---------------- JSON (STRUCTURED) ----------------

def ask_llm_json(question: str, evidence: list):
    payload = {
        "model": MODEL_NAME,
        "prompt": build_json_prompt(question, evidence),
        "stream": False,
        "format": "json",
        "options": {"temperature": 0.2}
    }

    resp = requests.post(OLLAMA_URL, json=payload)
    try:
        return resp.json()
    except:
        return {
            "answer": "",
            "summary": "",
            "classification": "unknown",
            "severity": 0.0,
            "key_points": []
        }
