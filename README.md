# 📘 Financial Dispute Resolution Assistant - GenAI  
### Financial Dispute Resolution Assistant (GenAI + Machine Learning)

An end-to-end, production-style **Generative AI + Machine Learning system** designed to assist financial dispute resolution caseworkers (e.g., Financial Ombudsman Service) by automating document understanding, evidence extraction, classification, severity scoring, and next-step recommendations.

---

## 🚀 Project Overview

**FDR-GenAI** is a web-based decision-support platform that:

- Ingests unstructured financial complaint documents (PDF or raw text)
- Extracts and chunks complaint content
- Retrieves evidence using a **RAG (Retrieval-Augmented Generation)** pipeline
- Answers questions using a **Large Language Model (LLM)**
- Classifies complaints using a **supervised ML model**
- Assigns **severity scores**
- Recommends **procedural next steps**
- Streams responses in real time with a modern UI

The system is designed with **regulated environments** in mind: explainable, conservative, and human-in-the-loop.

---

## 🎯 Problem Statement

Financial dispute resolution organisations receive **thousands of complaints weekly**. Caseworkers must manually:

- Read lengthy unstructured documents
- Extract key evidence
- Classify dispute types
- Assess severity
- Decide appropriate next actions

This process is slow, inconsistent, and difficult to scale.

👉 **FDR-GenAI reduces resolution time while maintaining transparency and fairness.**

---

## 🧠 Key Features

### 📄 Complaint Ingestion
- Upload PDF or paste complaint text
- Automatic text extraction
- Case ID generation

### 🔍 Evidence Retrieval (RAG)
- Text chunking + embeddings
- FAISS vector search
- Evidence-grounded answers only
- Exact evidence highlighted in UI

### 🤖 GenAI Question Answering
- LLM-powered responses (Ollama / Llama)
- Streaming “live typing” UX
- Evidence-aware prompts (no hallucinations)

### 🏷️ Complaint Classification
- Semantic classification (LLM + heuristics)
- Supervised ML classifier (TF-IDF + Logistic Regression)
- Confidence scoring
- Graceful fallback when models are unavailable

### ⚠️ Severity Scoring
- Rule-based, explainable severity logic
- Conservative defaults suitable for regulation

### 📌 Recommended Next Steps
- Hybrid rule-based + GenAI suggestions
- Escalation based on severity
- Designed for decision support, not automation

### 🖥️ Professional UI
- Single-page caseworker layout
- Streaming answers
- Auto-scroll
- Clear separation of outputs

---

## 🏗️ System Architecture

Browser UI (HTML / CSS / JS)
│
▼
FastAPI Backend
├── Upload & Ingestion
├── RAG Pipeline (FAISS)
├── LLM Engine (Ollama)
├── ML Classifier
├── Severity & Recommendation Engine
│
▼
Explainable, evidence-backed outputs


---

## 🧪 Machine Learning Pipeline

### Training
- Dataset: labelled financial complaints (`text`, `label`)
- Vectorisation: TF-IDF (unigrams + bigrams)
- Model: Logistic Regression (class-balanced)
- Evaluation: train/test split + classification report

### Inference
- Models loaded at runtime
- Outputs:
  - Predicted class
  - Confidence score
- Automatic fallback if artefacts are missing

---

## 📂 Project Structure

Financial_Dispute_Resolution_Assistant/
├── app/
│ ├── api/ # FastAPI routes
│ ├── ml/ # ML training scripts
│ ├── pipelines/ # RAG pipeline
│ ├── services/ # LLM, classifier, recommender
│ ├── main.py # Application entry point
├── templates/ # HTML UI
├── static/ # CSS & JavaScript
├── models/ # Trained ML models
├── data/ # Dataset (optional / ignored)
├── requirements.txt
├── README.md


---

## ▶️ How to Run Locally

### 1️⃣ Create virtual environment
```bash
python -m venv venv
venv\Scripts\activate

### 2️⃣ Install dependencies
```bash
pip install -r requirements.txt

### 3️⃣ (Optional) Train ML classifier
```bash 
python app/ml/train_classifier.py

### 4️⃣ Start the application
```bash
uvicorn app.main:app --reload --port 8000

### 5️⃣ Open in browser
```bash
http://127.0.0.1:8000

### 🧪 Example Output
```bash
Question:
Why did this dispute happen?

Answer:
The bank increased the customer’s loan interest rate without prior notification, which caused financial difficulty.

🏷 Classification
LLM: Loans

ML: loans (confidence ~0.85)

⚠️ Severity
Medium (60%)

🔍 Evidence Used
Exact supporting complaint text shown in UI.

## 📌 Recommended Steps
Request justification for interest change

Review loan agreement notification clauses

Assess FCA fair-lending compliance

## ☁️ Azure / Production Mapping (Conceptual)
Local Component	Azure Equivalent
FastAPI	Azure Functions / App Service
FAISS	Azure AI Search
Ollama	Azure OpenAI
CSV Dataset	Azure Blob Storage
Training Script	Azure ML Pipeline
Logs	Application Insights

## 🧠 Design Principles
Explainability over automation

Evidence-first reasoning

Conservative defaults

Graceful degradation

Human-in-the-loop decisions

## 🎤 Interview Talking Point
“I built an end-to-end GenAI system with supervised ML retraining, RAG-based evidence retrieval, streaming UX, and explainable severity scoring — designed for regulated environments.”

## 📌 Future Enhancements
UI-based model retraining

LLM vs ML disagreement alerts

Model drift monitoring

CI/CD with GitHub Actions

Full Azure deployment

## 👤 Author
Vinaykumar Yadav
Data Scientist | Machine Learning Engineer
MSc Artificial Intelligence (Distinction)
University of East London
