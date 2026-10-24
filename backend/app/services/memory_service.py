
from datetime import datetime

from sqlalchemy.orm import Session

from app.database.models import User, UserMemory


MAX_MEMORY_LENGTH = 1000


def save_memory(
    db: Session,
    user_id: int,
    memory_text: str,
) -> UserMemory:
    """Save a user-approved long-term memory."""

    memory_text = memory_text.strip()

    if not memory_text:
        raise ValueError("Memory cannot be empty.")

    if len(memory_text) > MAX_MEMORY_LENGTH:
        raise ValueError("Memory is too long.")

    user = db.get(User, user_id)

    if user is None:
        raise ValueError("User does not exist.")

    existing = (
        db.query(UserMemory)
        .filter(
            UserMemory.user_id == user_id,
            UserMemory.memory_text == memory_text,
        )
        .first()
    )

    if existing is not None:
        return existing

    memory = UserMemory(
        user_id=user_id,
        memory_text=memory_text,
    )

    db.add(memory)
    db.commit()
    db.refresh(memory)

    return memory


def get_user_memories(
    db: Session,
    user_id: int,
    limit: int = 20,
) -> list[UserMemory]:
    """Retrieve memories belonging to one user."""

    limit = max(1, min(limit, 100))

    return (
        db.query(UserMemory)
        .filter(UserMemory.user_id == user_id)
        .order_by(UserMemory.id.desc())
        .limit(limit)
        .all()
    )


def delete_memory(
    db: Session,
    user_id: int,
    memory_id: int,
) -> bool:
    """Delete a memory belonging to the specified user."""

    memory = (
        db.query(UserMemory)
        .filter(
            UserMemory.id == memory_id,
            UserMemory.user_id == user_id,
        )
        .first()
    )

    if memory is None:
        return False

    db.delete(memory)
    db.commit()

    return True


def update_memory(
    db: Session,
    user_id: int,
    memory_id: int,
    new_memory_text: str,
) -> UserMemory | None:
    """Update an existing memory owned by the user."""

    new_memory_text = new_memory_text.strip()

    if not new_memory_text:
        raise ValueError("Memory cannot be empty.")

    if len(new_memory_text) > MAX_MEMORY_LENGTH:
        raise ValueError("Memory is too long.")

    memory = (
        db.query(UserMemory)
        .filter(
            UserMemory.id == memory_id,
            UserMemory.user_id == user_id,
        )
        .first()
    )

    if memory is None:
        return None

    duplicate = (
        db.query(UserMemory)
        .filter(
            UserMemory.user_id == user_id,
            UserMemory.memory_text == new_memory_text,
            UserMemory.id != memory_id,
        )
        .first()
    )

    if duplicate is not None:
        raise ValueError("This memory already exists.")

    memory.memory_text = new_memory_text
    memory.updated_at = datetime.utcnow()

    db.commit()
    db.refresh(memory)

    return memory
