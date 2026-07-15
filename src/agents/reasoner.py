import json
from unittest import result

from src.agents.llm import generate
from src.models import TriageResult
from src.prompts.triage import build_triage_prompt


def generate_triage(
    symptoms: str,
    evidence: list[str],
    additional_info: str | None = None,
) -> TriageResult:
    """
    Generates a triage recommendation using the LLM.
    """

    prompt = build_triage_prompt(
        symptoms,
        evidence,
        additional_info,
    )

    response = generate(prompt)

    result = parse_llm_response(response)

    result.evidence = evidence

    return result


def parse_llm_response(response: str) -> TriageResult:
    """
    Parses and validates the LLM response.
    """

    response = response.strip()

    if response.startswith("```"):
        response = response.replace("```json", "")
        response = response.replace("```", "")
        response = response.strip()

    try:
        data = json.loads(response)
    except json.JSONDecodeError as e:
        raise ValueError(
            f"Gemini returned invalid JSON: {e}"
        ) from e

    try:
        return TriageResult(**data)
    except Exception as e:
        raise ValueError(
            f"Gemini returned an invalid response schema: {e}"
        ) from e