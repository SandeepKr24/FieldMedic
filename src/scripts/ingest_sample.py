from src.agents.rag import ingest_knowledge_document

sample_text = """
Chest pain may indicate a life-threatening emergency.

Patients with severe chest pain should be evaluated immediately.

Shortness of breath accompanying chest pain increases urgency.

Persistent chest pain lasting longer than 15 minutes should not be ignored.

Patients with unstable vital signs require emergency referral.
"""

result = ingest_knowledge_document(
    source="Sample Guideline",
    title="Chest Pain Guideline",
    text=sample_text,
)

print(result)