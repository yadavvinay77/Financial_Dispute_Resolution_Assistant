def recommend_steps(predicted_class: str, severity: float):
    """
    Simple rules-based recommender for next steps.
    You can enhance this later or even LLM-generate recommendations.
    """

    severity_level = "low"
    if severity >= 0.66:
        severity_level = "high"
    elif severity >= 0.33:
        severity_level = "medium"

    steps = []

    # ------------- FRAUD CASES -------------
    if predicted_class == "fraud":
        steps.append("Contact the bank's fraud department immediately.")
        steps.append("Freeze or block affected cards or accounts.")
        steps.append("Request the bank's fraud investigation report.")
        if severity_level == "high":
            steps.append("Escalate instantly to FOS for urgent review.")

    # ------------- PAYMENTS CASES ----------
    elif predicted_class == "payments":
        steps.append("Request transaction breakdown from the bank.")
        steps.append("Verify whether direct debits or standing orders changed.")
        if severity_level == "high":
            steps.append("Check for duplicate or unauthorized transactions.")

    # ------------- LOAN CASES --------------
    elif predicted_class == "loan":
        steps.append("Request documentation explaining the interest change.")
        steps.append("Review loan agreement terms regarding notifications.")
        steps.append("Check FCA rules for fair lending and interest adjustments.")
        if severity_level == "high":
            steps.append("Recommend rapid escalation if financial harm documented.")

    # ------------- INSURANCE CASES ---------
    elif predicted_class == "insurance":
        steps.append("Ask for insurance policy details and claim history.")
        steps.append("Check reasons for denial or premium changes.")
        if severity_level == "high":
            steps.append("Request internal insurer review before FOS escalation.")

    # ------------- SERVICE ISSUES ----------
    elif predicted_class == "service":
        steps.append("Request timeline of interactions from the bank.")
        steps.append("Review delays, errors, or poor communication.")
        if severity_level == "high":
            steps.append("Ask for compensation consideration per FCA DISP.")

    # ------------- UNKNOWN ----------------
    else:
        steps.append("Insufficient data — request full complaint details.")
        steps.append("Ask customer to provide evidence such as statements or letters.")

    return steps
