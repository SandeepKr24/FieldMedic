from src.agents.reasoner import generate_triage

result = generate_triage(
    symptoms="Patient has severe chest pain and shortness of breath.",
    evidence=[
        "Chest pain may indicate a life-threatening emergency.",
        "Patients with severe chest pain should be evaluated immediately.",
        "Shortness of breath accompanying chest pain increases urgency.",
    ],
)

print(result.model_dump_json(indent=2))