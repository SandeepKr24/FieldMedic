from pydantic import BaseModel, Field
from typing import Any

class KnowledgeIngestRequest(BaseModel):
    source: str
    title: str | None = None
    text: str
    

class TriageRequest(BaseModel):
    symptoms: str
    vitals: dict[str, Any] | None = None
    additional_info: str | None = None


class TriageResult(BaseModel):
    triage: str = Field(
        description="Emergency, Urgent, or Monitor"
    )

    care_plan: str

    icd10: list[str]

    summary: str

    confidence: float

    evidence: list[str] = Field(
        default_factory=list,
        description="Knowledge chunks used to generate the response.",
    )