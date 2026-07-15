from google import genai

from src.logger import logger
from src.config import (
    GEMINI_API_KEY,
    GEMINI_MODEL,
)

client = genai.Client(
    api_key=GEMINI_API_KEY,
)

model = GEMINI_MODEL

logger.info(
    "Sending prompt to Gemini."
)


def generate(prompt: str) -> str:
    """
    Sends the prompt to Gemini and returns the generated text.
    """

    try:
        response = client.models.generate_content(
            model=model,
            contents=prompt,
        )

        return response.text

    except Exception as e:
        logger.exception(
            "Gemini request failed."
        )

        raise RuntimeError(
            "The AI model is temporarily unavailable due to high demand. Please try again in a few moments."
        ) from e