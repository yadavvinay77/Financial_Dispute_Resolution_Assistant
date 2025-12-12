# app/services/classifier.py

import os
import pickle
from typing import Tuple

MODEL_DIR = "models"
MODEL_PATH = os.path.join(MODEL_DIR, "classifier.pkl")
VECTORIZER_PATH = os.path.join(MODEL_DIR, "vectorizer.pkl")


class ClassifierService:
    def __init__(self):
        self.available = False
        self.model = None
        self.vectorizer = None

        if os.path.exists(MODEL_PATH) and os.path.exists(VECTORIZER_PATH):
            with open(MODEL_PATH, "rb") as f:
                self.model = pickle.load(f)
            with open(VECTORIZER_PATH, "rb") as f:
                self.vectorizer = pickle.load(f)
            self.available = True
        else:
            print("[WARN] Classifier model not found. Running in fallback mode.")

    def predict(self, text: str) -> Tuple[str, float]:
        if not self.available:
            return "unknown", 0.0

        X = self.vectorizer.transform([text])
        probs = self.model.predict_proba(X)[0]
        idx = probs.argmax()
        return self.model.classes_[idx], float(probs[idx])
