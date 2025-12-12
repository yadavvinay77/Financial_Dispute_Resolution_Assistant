# app/services/vector_store.py

# Standard library imports
import json
import os
from threading import Lock

# Third-party imports
import faiss
import numpy as np

VECTOR_DIR = "vector_store"
INDEX_FILE = os.path.join(VECTOR_DIR, "faiss_index.bin")
META_FILE = os.path.join(VECTOR_DIR, "metadata.json")

class VectorStore:
    def __init__(self, dim=None):
        os.makedirs(VECTOR_DIR, exist_ok=True)
        self.lock = Lock()

        if os.path.exists(INDEX_FILE):
            self.index = faiss.read_index(INDEX_FILE)
            self.dim = self.index.d
        else:
            if dim is None:
                raise ValueError("VectorStore requires dim on first creation.")
            self.dim = dim
            self.index = faiss.IndexFlatL2(dim)

        self.metadata = []
        if os.path.exists(META_FILE):
            with open(META_FILE, "r", encoding="utf-8") as f:
                self.metadata = json.load(f)

    def save(self):
        faiss.write_index(self.index, INDEX_FILE)
        with open(META_FILE, "w", encoding="utf-8") as f:
            json.dump(self.metadata, f, indent=2)

    def add(self, embeddings, chunks, case_id):
        arr = np.array(embeddings).astype("float32")
        self.index.add(arr)

        for c in chunks:
            self.metadata.append({"chunk": c, "case_id": case_id})

        self.save()

    def search(self, query_embedding, k=5):
        if self.index.ntotal == 0:
            return []

        q = np.array([query_embedding]).astype("float32")
        _, idx = self.index.search(q, k)

        return [
            self.metadata[i]
            for i in idx[0]
            if i != -1 and i < len(self.metadata)
        ]
