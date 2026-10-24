
import logging
import random
import time
from time import perf_counter

from google import genai
from google.genai import errors, types

from app.config import GEMINI_API_KEY

logger = logging.getLogger(__name__)

MODEL_NAME = "gemini-3.6-flash"

# Limit individual HTTP requests to 15 seconds.
REQUEST_TIMEOUT_MS = 15000

# One initial request + one retry.
MAX_ATTEMPTS = 2

RETRYABLE_CODES = {429, 500, 502, 503, 504}

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
    Generate a Gemini response with limited retries.

    The SDK's own retries are disabled so that this
    function controls application-level retries.
    """

    for attempt in range(1, MAX_ATTEMPTS + 1):
        started = perf_counter()

        try:
            response = client.models.generate_content(
                model=MODEL_NAME,
                contents=message,
            )

            elapsed = perf_counter() - started

            print(
                f"AgentOS: Gemini attempt {attempt} "
                f"completed in {elapsed:.2f} seconds"
            )

            answer = (response.text or "").strip()

            if not answer:
                raise RuntimeError(
                    "Gemini returned an empty response."
                )

            return answer

        except errors.APIError as exc:
            elapsed = perf_counter() - started
            status_code = getattr(exc, "code", None)

            logger.warning(
                "Gemini attempt %s failed: HTTP %s "
                "after %.2f seconds",
                attempt,
                status_code,
                elapsed,
            )

            if status_code not in RETRYABLE_CODES:
                raise

            if attempt >= MAX_ATTEMPTS:
                logger.error(
                    "Gemini failed after %s attempts.",
                    MAX_ATTEMPTS,
                )
                raise

            # Small randomized delay to avoid synchronized retries.
            delay = 1.0 + random.uniform(0, 0.5)

            logger.warning(
                "Retrying Gemini in %.2f seconds...",
                delay,
            )

            time.sleep(delay)

    raise RuntimeError(
        "Gemini failed to generate a response."
    )
