from src.agents.orchestrator import triage_patient

result = triage_patient(
    "Patient has severe chest pain and shortness of breath."
)

print(result)