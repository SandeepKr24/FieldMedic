from src.agents.rag import search_knowledge
from src.agents.reasoner import generate_triage
from src.logger import logger
from src.agents.safety import apply_safety_rules

def triage_patient(symptoms: str,vitals: dict | None = None,additional_info: str | None = None,):
    try:
        logger.info("Starting triage pipeline.")

        logger.info("Searching knowledge base.")
        evidence = search_knowledge(symptoms)

        logger.info(
            "Retrieved %d evidence chunks.",
            len(evidence),
        )

        logger.info("Generating triage recommendation.")
        result = generate_triage(
            symptoms=symptoms,
            evidence=evidence,
            additional_info=additional_info,
        )

        result = apply_safety_rules(
            result=result,
            vitals=vitals,
        )

        logger.info("Triage pipeline completed.")

        return result

    except Exception:
        logger.exception("Triage pipeline failed.")
        raise