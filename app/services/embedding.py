# app/services/embedding.py

import requests

EMBED_MODEL = "mxbai-embed-large"
OLLAMA_URL = "http://localhost:11434/api/embeddings"


def embed_text(text: str):
    """
    Embeds text using mxbai-embed-large via Ollama.
    Returns a list[float] or None if it fails.
    """

    payload = {
        "model": EMBED_MODEL,
        "prompt": text
    }

    try:
        res = requests.post(OLLAMA_URL, json=payload)
        data = res.json()

        if "embedding" in data:
            return data["embedding"]

        print("Embedding error (no 'embedding' key):", data)
        return None

    except Exception as e:
        print("Embedding request failed:", e)
        return None
