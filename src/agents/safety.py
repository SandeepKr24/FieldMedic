from src.models import TriageResult


def apply_safety_rules(
    result: TriageResult,
    vitals: dict | None,
) -> TriageResult:
    """
    Applies deterministic safety rules to the LLM output.
    """

    if vitals is None:
        return result

    oxygen = vitals.get("spo2")

    if oxygen is not None and oxygen < 90:
        result.triage = "Emergency"

        result.care_plan += (
            "\n\nSafety override: "
            "Low oxygen saturation detected."
        )

    return result.model_copy(
        update={
            "triage": "Emergency",
            "care_plan": (
                result.care_plan
                + "\n\nSafety override: Low oxygen saturation detected."
            ),
        }
    )