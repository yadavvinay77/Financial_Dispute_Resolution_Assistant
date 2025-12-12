# scripts/generate_dataset.py

import pandas as pd
import random
from pathlib import Path

OUTPUT_PATH = Path("data/fos_complaints.csv")
OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)

fraud_samples = [
    "My card was used for an unauthorized transaction at a store I’ve never visited.",
    "Money was withdrawn from my account without my approval.",
    "There are multiple fraudulent online purchases I did not make.",
    "My debit card was cloned and used for ATM withdrawals.",
    "The bank refused to refund a fraud transaction made overseas.",
]

payment_samples = [
    "A payment I made did not reach the merchant but was deducted from my account.",
    "The bank processed the same payment twice and won't reverse it.",
    "An international transfer is missing and customer service is unresponsive.",
    "Direct debit was taken early and caused my account to go overdrawn.",
    "Merchant charged me even though the service was cancelled.",
]

loan_samples = [
    "My loan was approved but funds were never released.",
    "Interest rate on my loan increased without prior notification.",
    "The bank miscalculated my loan EMI and overcharged me.",
    "I was sold a loan product without clear explanation of terms.",
    "My loan closure request is pending despite repeated follow-ups.",
]

insurance_samples = [
    "My insurance claim was rejected without proper justification.",
    "Premiums increased significantly without informing me.",
    "They refused to cover a medical expense listed in my policy.",
    "My home insurance claim is delayed for months.",
    "The insurer cancelled my policy without notifying me.",
]

service_samples = [
    "My bank account was closed without explanation.",
    "Customer support did not resolve my issue despite multiple calls.",
    "Mobile banking app keeps failing during transactions.",
    "I was given incorrect advice which caused financial loss.",
    "The branch refused to assist with updating my KYC details.",
]

categories = {
    "fraud": fraud_samples,
    "payments": payment_samples,
    "loan": loan_samples,
    "insurance": insurance_samples,
    "service": service_samples,
}

# Generate 200 synthetic variants for each category
rows = []

for label, base_samples in categories.items():
    for _ in range(200):
        sentence = random.choice(base_samples)

        # Add random noise, variation, and extension
        variation = random.choice([
            "",
            " This caused financial stress.",
            " The issue is still unresolved.",
            " I contacted support but received no help.",
            " I want this reviewed immediately.",
            " I have evidence supporting my claim.",
        ])

        row = sentence + variation
        rows.append((row, label))

df = pd.DataFrame(rows, columns=["text", "label"])

df.to_csv(OUTPUT_PATH, index=False)

print(f"Dataset generated: {OUTPUT_PATH} ({len(df)} rows)")
