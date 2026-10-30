import logging

from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel, Field
from sqlalchemy.orm import Session

from app.database.database import get_db
from app.database.models import User
from app.services.memory_conflict import detect_memory_conflict
from app.services.memory_extractor import extract_memories
from app.services.memory_service import (
    delete_memory,
    get_user_memories,
    save_memory,
    update_memory,
)

logger = logging.getLogger(__name__)
router = APIRouter(prefix="/memory", tags=["Memory"])
LOCAL_USERNAME = "local_user"


class ExtractRequest(BaseModel):
    message: str = Field(min_length=1, max_length=10000)


class SaveMemoryRequest(BaseModel):
    memory_text: str = Field(min_length=1, max_length=1000)


class UpdateMemoryRequest(BaseModel):
    memory_text: str = Field(min_length=1, max_length=1000)


class ConflictCheckRequest(BaseModel):
    new_information: str = Field(min_length=1, max_length=1000)


def get_local_user(db: Session) -> User:
    user = db.query(User).filter(User.username == LOCAL_USERNAME).first()
    if user is None:
        raise HTTPException(status_code=404, detail="Local development user not found.")
    return user


@router.post("/extract")
def suggest_memories(request: ExtractRequest):
    return {"suggested_memories": extract_memories(request.message)}


@router.post("/save")
def save_user_memory(request: SaveMemoryRequest, db: Session = Depends(get_db)):
    user = get_local_user(db)
    try:
        memory = save_memory(db=db, user_id=user.id, memory_text=request.memory_text)
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc
    return {
        "message": "Memory saved successfully.",
        "memory_id": memory.id,
        "memory_text": memory.memory_text,
    }


@router.get("")
def list_memories(db: Session = Depends(get_db)):
    user = get_local_user(db)
    memories = get_user_memories(db=db, user_id=user.id, limit=100)
    return [
        {
            "id": memory.id,
            "memory_text": memory.memory_text,
            "created_at": memory.created_at.isoformat(),
        }
        for memory in memories
    ]


@router.delete("/{memory_id}")
def remove_memory(memory_id: int, db: Session = Depends(get_db)):
    user = get_local_user(db)
    deleted = delete_memory(db=db, user_id=user.id, memory_id=memory_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Memory not found.")
    return {"message": "Memory deleted successfully."}


@router.put("/{memory_id}")
def update_user_memory(
    memory_id: int,
    request: UpdateMemoryRequest,
    db: Session = Depends(get_db),
):
    user = get_local_user(db)
    try:
        memory = update_memory(
            db=db,
            user_id=user.id,
            memory_id=memory_id,
            new_memory_text=request.memory_text,
        )
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc
    if memory is None:
        raise HTTPException(status_code=404, detail="Memory not found.")
    return {
        "message": "Memory updated successfully.",
        "memory_id": memory.id,
        "memory_text": memory.memory_text,
    }


@router.post("/check-conflict")
def check_memory_conflict(
    request: ConflictCheckRequest,
    db: Session = Depends(get_db),
):
    user = get_local_user(db)
    memories = get_user_memories(db=db, user_id=user.id, limit=100)

    # Copy values while ORM objects are attached to the active session.
    memory_snapshot = [
        {"id": memory.id, "memory_text": memory.memory_text}
        for memory in memories
    ]

    # Release the database read transaction before calling Gemini.
    db.rollback()

    try:
        decision = detect_memory_conflict(
            new_information=request.new_information,
            existing_memories=memory_snapshot,
        )
    except Exception:
        logger.exception("Memory conflict analysis failed")
        raise HTTPException(
            status_code=502,
            detail="Memory conflict analysis failed. Check backend logs.",
        )

    return decision.model_dump()
