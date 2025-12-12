# app/ml/train_classifier.py

import os
import pickle
import pandas as pd

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report

# ---------------- CONFIG ----------------

DATA_PATH = "data/fos_complaints.csv"
MODEL_DIR = "models"
MODEL_PATH = os.path.join(MODEL_DIR, "classifier.pkl")
VECTORIZER_PATH = os.path.join(MODEL_DIR, "vectorizer.pkl")

TEXT_COLUMN = "text"   # 🔴 CHANGE if needed
LABEL_COLUMN = "label"        # 🔴 CHANGE if needed

# ---------------- LOAD DATA ----------------

print("📥 Loading dataset...")
df = pd.read_csv(DATA_PATH)

if TEXT_COLUMN not in df.columns or LABEL_COLUMN not in df.columns:
    raise ValueError(
        f"Dataset must contain columns: {TEXT_COLUMN}, {LABEL_COLUMN}"
    )

texts = df[TEXT_COLUMN].astype(str)
labels = df[LABEL_COLUMN].astype(str).str.strip().str.lower()

print(f"✅ Loaded {len(df)} records")

# ---------------- SPLIT ----------------

X_train, X_test, y_train, y_test = train_test_split(
    texts, labels, test_size=0.2, random_state=42, stratify=labels
)

# ---------------- VECTORIZATION ----------------

print("🔠 Vectorizing text...")
vectorizer = TfidfVectorizer(
    max_features=20000,
    ngram_range=(1, 2),
    stop_words="english"
)

X_train_vec = vectorizer.fit_transform(X_train)
X_test_vec = vectorizer.transform(X_test)

# ---------------- TRAIN MODEL ----------------

print("🤖 Training Logistic Regression classifier...")
model = LogisticRegression(
    max_iter=1000,
    class_weight="balanced",
    n_jobs=-1
)

model.fit(X_train_vec, y_train)

# ---------------- EVALUATION ----------------

print("\n📊 Classification Report:")
y_pred = model.predict(X_test_vec)
print(classification_report(y_test, y_pred))

# ---------------- SAVE MODELS ----------------

os.makedirs(MODEL_DIR, exist_ok=True)

with open(MODEL_PATH, "wb") as f:
    pickle.dump(model, f)

with open(VECTORIZER_PATH, "wb") as f:
    pickle.dump(vectorizer, f)

print("\n💾 Models saved:")
print(f" - {MODEL_PATH}")
print(f" - {VECTORIZER_PATH}")
