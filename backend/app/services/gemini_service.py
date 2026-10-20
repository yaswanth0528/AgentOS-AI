
import time
import logging

from google import genai
from google.genai import types
from google.genai import errors

from app.config import GEMINI_API_KEY

logger = logging.getLogger(__name__)

# HTTP timeout: 45 seconds per request attempt
client = genai.Client(
    api_key=GEMINI_API_KEY,
    http_options=types.HttpOptions(timeout=45000),
)

MODEL_NAME = "gemini-3.6-flash"
MAX_ATTEMPTS = 3
RETRY_DELAYS = [1, 2]


def generate_response(message: str) -> str:
    """
    Generate a response using Gemini.
    Retry temporary API errors up to two times.
    """

    for attempt in range(MAX_ATTEMPTS):
        try:
            response = client.models.generate_content(
                model=MODEL_NAME,
                contents=message,
            )

            answer = (response.text or "").strip()

            if not answer:
                raise RuntimeError(
                    "Gemini returned an empty response."
                )

            return answer

        except errors.APIError as exc:
            status_code = getattr(exc, "code", None)

            # Retry only temporary errors.
            if status_code not in (429, 500, 502, 503, 504):
                logger.exception(
                    "Gemini API returned a non-retryable error."
                )
                raise

            if attempt == MAX_ATTEMPTS - 1:
                logger.exception(
                    "Gemini failed after all retry attempts."
                )
                raise

            delay = RETRY_DELAYS[attempt]

            logger.warning(
                "Gemini returned HTTP %s. "
                "Retrying in %s second(s), attempt %s/%s.",
                status_code,
                delay,
                attempt + 2,
                MAX_ATTEMPTS,
            )

            time.sleep(delay)

    raise RuntimeError("Gemini could not generate a response.")
