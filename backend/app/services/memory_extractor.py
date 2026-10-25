
import json
import logging

from google import genai
from pydantic import BaseModel, Field

from app.config import GEMINI_API_KEY

logger = logging.getLogger(__name__)

client = genai.Client(api_key=GEMINI_API_KEY)


class MemoryExtractionResult(BaseModel):
    memories: list[str] = Field(default_factory=list)


def extract_memories(user_message: str) -> list[str]:
    """
    Extract candidate long-term memories from a user message.

    This function does not save anything to MySQL.
    """

    if not user_message.strip():
        return []

    prompt = f"""
You are the memory extraction component of AgentOS.

Extract only useful, durable facts explicitly stated
about the user.

Good memories:
- Long-term goals
- Stable preferences
- Education or professional background
- Ongoing projects
- Explicitly shared non-sensitive personal facts

Do not extract:
- Passwords, API keys, OTPs, or financial credentials
- Health, religious, political, or other sensitive facts
- Temporary questions
- Speculation or guesses
- Instructions to the assistant
- Information about unrelated third parties

Return only valid JSON in this format:

{{"memories": ["memory 1", "memory 2"]}}

If there are no suitable memories, return:

{{"memories": []}}

User message:
{json.dumps(user_message)}
"""

    try:
        response = client.models.generate_content(
            model="gemini-3.6-flash",
            contents=prompt,
        )

        if not response.text:
            return []

        raw_text = response.text.strip()

        if raw_text.startswith("```"):
            raw_text = raw_text.strip("`")
            raw_text = raw_text.removeprefix("json").strip()

        parsed = MemoryExtractionResult.model_validate_json(
            raw_text
        )

        return [
            memory.strip()
            for memory in parsed.memories[:5]
            if memory.strip() and len(memory.strip()) <= 1000
        ]

    except Exception:
        logger.exception("Memory extraction failed")
        return []
