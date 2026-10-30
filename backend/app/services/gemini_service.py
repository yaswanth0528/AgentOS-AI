
import time
import logging
import random
import time
from time import perf_counter

from google import genai
from google.genai import errors, types

from app.config import GEMINI_API_KEY


logger = logging.getLogger(__name__)

MODEL_NAME = "gemini-3.6-flash"

# Allow more time for each Gemini request.
REQUEST_TIMEOUT_MS = 45000

# Initial request + two retries.
MAX_ATTEMPTS = 3

RETRYABLE_CODES = {500, 502, 503, 504}


client = genai.Client(
    api_key=GEMINI_API_KEY,
    http_options=types.HttpOptions(
        timeout=REQUEST_TIMEOUT_MS,
        retry_options=types.HttpRetryOptions(
            attempts=1,
        ),
    ),
)


def generate_response(message: str) -> str:
    """
    Generate a Gemini response.

    Features:
    - Configurable request timeout
    - Limited retries for temporary API failures
    - Exponential backoff with jitter
    - Response-time logging
    - No retries for non-retryable API errors
    """

    for attempt in range(1, MAX_ATTEMPTS + 1):
        started = perf_counter()

        try:
            logger.info(
                "Starting Gemini request: attempt %s/%s",
                attempt,
                MAX_ATTEMPTS,
            )

            response = client.models.generate_content(
                model=MODEL_NAME,
                contents=message,
            )

            elapsed = perf_counter() - started

            answer = (response.text or "").strip()

            if not answer:
                raise RuntimeError(
                    "Gemini returned an empty response."
                )

            logger.info(
                "Gemini attempt %s succeeded in %.2f seconds",
                attempt,
                elapsed,
            )

            return answer

        except errors.APIError as exc:
            elapsed = perf_counter() - started
            status_code = getattr(exc, "code", None)

            logger.warning(
                "Gemini attempt %s/%s failed with HTTP %s "
                "after %.2f seconds: %s",
                attempt,
                MAX_ATTEMPTS,
                status_code,
                elapsed,
                exc,
            )

            if status_code not in RETRYABLE_CODES:
                raise

            if attempt == MAX_ATTEMPTS:
                logger.error(
                    "Gemini failed after %s attempts.",
                    MAX_ATTEMPTS,
                )
                raise

            # Exponential backoff with jitter.
            delay = min(
                2 ** (attempt - 1) + random.uniform(0, 0.5),
                8.0,
            )

            logger.info(
                "Retrying Gemini in %.2f seconds",
                delay,
            )

            time.sleep(delay)

    raise RuntimeError("Gemini could not generate a response.")
