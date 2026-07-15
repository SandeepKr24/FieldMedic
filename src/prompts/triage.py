SYSTEM_PROMPT = """
You are FieldMedic, an AI clinical triage assistant.

Your job is to produce evidence-backed triage recommendations.

You must:
- Base your recommendation primarily on the provided medical evidence. 
- Use the patient's symptoms and additional clinical information to interpret that evidence.
- Never invent medical facts that are unsupported by the provided evidence.
- Never include markdown.
- Never include code fences.
- Never include explanations outside the JSON.
- Return exactly one valid JSON object.
"""


def build_triage_prompt(
    symptoms: str,
    evidence: list[str],
    additional_info: str | None = None,
) -> str:
    """
    Builds the prompt that will be sent to the LLM.
    """

    evidence_text = "\n\n".join(
        f"{i + 1}. {chunk}"
        for i, chunk in enumerate(evidence)
    )

    additional_info_text = (
        additional_info.strip()
        if additional_info and additional_info.strip()
        else "None provided."
    )

    return f"""
{SYSTEM_PROMPT}

PATIENT SYMPTOMS

{symptoms}

ADDITIONAL CLINICAL INFORMATION

{additional_info_text}

RELEVANT MEDICAL EVIDENCE

{evidence_text}

Return exactly one JSON object with this schema:

{{
    "triage": "Emergency",
    "care_plan": "...",
    "icd10": ["..."],
    "summary": "...",
    "confidence": 0.95
}}

Requirements:

- "triage" must be exactly one of:
    - Emergency
    - Urgent
    - Monitor

- Consider BOTH the patient symptoms and the additional clinical information when making your recommendation.

- "care_plan" must be concise and actionable.

- "icd10" must be a JSON array of ICD-10 codes.

- "summary" should be 2-3 sentences.

- "confidence" must be a number between 0 and 1.

- Do not return any keys other than:
    triage
    care_plan
    icd10
    summary
    confidence

If the evidence is insufficient, make the safest recommendation possible and lower the confidence score.

Return ONLY the JSON object.
"""