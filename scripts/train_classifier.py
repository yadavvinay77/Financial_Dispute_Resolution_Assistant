# scripts/train_classifier.py

import pandas as pd
import pickle
from pathlib import Path

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import (
    classification_report,
    confusion_matrix,
    accuracy_score
)
import matplotlib.pyplot as plt
import seaborn as sns

DATA_PATH = Path("data/fos_complaints.csv")
MODEL_DIR = Path("app/models")
MODEL_DIR.mkdir(parents=True, exist_ok=True)

print("Loading dataset...")
df = pd.read_csv(DATA_PATH)

X = df["text"]
y = df["label"]

print("Vectorizing text...")
vectorizer = TfidfVectorizer(stop_words="english", max_features=5000)
X_vec = vectorizer.fit_transform(X)

X_train, X_test, y_train, y_test = train_test_split(
    X_vec, y, test_size=0.2, random_state=42
)

print("Training classifier...")
clf = LogisticRegression(max_iter=1000)
clf.fit(X_train, y_train)

print("Evaluating model...")
y_pred = clf.predict(X_test)
acc = accuracy_score(y_test, y_pred)

print("\nClassification Report:\n")
print(classification_report(y_test, y_pred))

print("\nConfusion Matrix:")
cm = confusion_matrix(y_test, y_pred)
print(cm)

# Plot confusion matrix
plt.figure(figsize=(8,6))
sns.heatmap(cm, annot=True, cmap="Blues",
            xticklabels=clf.classes_,
            yticklabels=clf.classes_)
plt.title("Confusion Matrix")
plt.xlabel("Predicted")
plt.ylabel("Actual")
plt.tight_layout()
plt.savefig("confusion_matrix.png")
print("\nSaved: confusion_matrix.png")

# Save model
pickle.dump(vectorizer, open(MODEL_DIR / "tfidf_vectorizer.pkl", "wb"))
pickle.dump(clf, open(MODEL_DIR / "lr_classifier.pkl", "wb"))

print("\nSaved:")
print(" - tfidf_vectorizer.pkl")
print(" - lr_classifier.pkl")
print("\nTraining completed successfully!")
