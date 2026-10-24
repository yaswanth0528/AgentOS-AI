
import re

from sqlalchemy.orm import Session

from app.database.models import UserMemory


STOP_WORDS = {
    "a", "an", "the", "am", "is", "are",
    "was", "were", "i", "my", "me", "you",
    "your", "what", "which", "who", "where",
    "when", "why", "how", "do", "does",
    "did", "to", "of", "in", "on", "for",
    "and", "or", "that", "this", "with",
    "have", "has", "it", "can", "tell",
    "about", "please"
}


def tokenize(text: str) -> set[str]:
    words = re.findall(r"[a-z0-9]+", text.lower())

    return {
        word
        for word in words
        if word not in STOP_WORDS
    }


def search_relevant_memories(
    db: Session,
    user_id: int,
    query: str,
    limit: int = 5,
) -> list[UserMemory]:
    """
    Find user memories that share meaningful
    keywords with the current question.
    """

    query_tokens = tokenize(query)

    if not query_tokens:
        return []

    memories = (
        db.query(UserMemory)
        .filter(UserMemory.user_id == user_id)
        .order_by(UserMemory.id.desc())
        .limit(500)
        .all()
    )

    scored_memories = []

    for memory in memories:
        memory_tokens = tokenize(memory.memory_text)

        common_tokens = query_tokens & memory_tokens

        if not common_tokens:
            continue

        score = len(common_tokens) / len(query_tokens)

        scored_memories.append((score, memory))

    scored_memories.sort(
        key=lambda item: item[0],
        reverse=True
    )

    return [
        memory
        for score, memory in scored_memories[:limit]
    ]
