from pydantic import BaseModel

from src.models import TriageResult


class PipelineContext(BaseModel):
    symptoms: str

    vitals: dict | None = None

    evidence: list[str] = []

    triage_result: TriageResult | None = None

    logs: list[str] = []