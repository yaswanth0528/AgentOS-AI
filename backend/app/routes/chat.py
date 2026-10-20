
from datetime import datetime
from time import perf_counter

from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel, Field
from sqlalchemy.orm import Session

from app.database.database import get_db
from app.database.models import ChatMessage, ChatSession
from app.services.gemini_service import generate_response

router = APIRouter(prefix="/chat", tags=["Chat"])


class ChatRequest(BaseModel):
    message: str = Field(min_length=1, max_length=10000)
    session_id: int | None = None


class ChatResponse(BaseModel):
    session_id: int
    response: str


class HistoryMessage(BaseModel):
    role: str
    content: str
    created_at: str


# These greetings are answered locally without calling Gemini.
GREETINGS = {
    "hi": "Hello! 👋 How can I help you?",
    "hello": "Hello! 👋 How can I help you?",
    "hey": "Hey! 😊 What can I help you with?",
    "hi jarvis": "Hello! 👋 I'm AgentOS. How can I help?",
    "hello jarvis": "Hello! 👋 I'm AgentOS. How can I help?",
    "good morning": "Good morning! ☀️ How can I help you today?",
    "good afternoon": "Good afternoon! How can I help you?",
    "good evening": "Good evening! How can I help you?",
}


@router.post("", response_model=ChatResponse)
def chat(request: ChatRequest, db: Session = Depends(get_db)):
    user_text = request.message.strip()

    if not user_text:
        raise HTTPException(
            status_code=422,
            detail="Message cannot be empty.",
        )

    try:
        # Find the existing conversation or create a new one.
        if request.session_id is not None:
            chat_session = (
                db.query(ChatSession)
                .filter(ChatSession.id == request.session_id)
                .first()
            )

            if chat_session is None:
                raise HTTPException(
                    status_code=404,
                    detail="Chat session not found.",
                )
        else:
            chat_session = ChatSession(
                title=user_text[:50] or "New Chat"
            )
            db.add(chat_session)
            db.commit()
            db.refresh(chat_session)

        # Always save the user's message.
        db.add(
            ChatMessage(
                session_id=chat_session.id,
                role="user",
                message=user_text,
            )
        )
        db.commit()

        # Handle exact greetings locally to avoid unnecessary API calls.
        normalized_text = user_text.lower().strip(" \t\n.!?,")
        ai_response = GREETINGS.get(normalized_text)

        if ai_response is not None:
            print("AgentOS: Local greeting response; Gemini skipped.")
        else:
            # Keep the full history in MySQL, but send only recent
            # messages to Gemini to limit prompt size.
            recent_messages = (
                db.query(ChatMessage)
                .filter(
                    ChatMessage.session_id == chat_session.id
                )
                .order_by(ChatMessage.id.desc())
                .limit(20)
                .all()
            )
            recent_messages.reverse()

            transcript = "\n".join(
                f'{"User" if item.role == "user" else "AgentOS"}: '
                f"{item.message}"
                for item in recent_messages
            )

            prompt = (
                "You are AgentOS, a helpful AI assistant. Use the "
                "conversation history to answer the latest user message. "
                "Use relevant facts from the history accurately. "
                "Do not claim to remember facts that are not present "
                "in the supplied history.\n\n"
                f"Conversation history:\n{transcript}\n\n"
                "Respond to the latest user message."
            )

            started = perf_counter()
            print("AgentOS: Calling Gemini...")

            try:
                ai_response = generate_response(prompt)
            except Exception as exc:
                print(
                    f"AgentOS Gemini error: "
                    f"{type(exc).__name__}: {exc}"
                )
                raise HTTPException(
                    status_code=502,
                    detail=(
                        "The Gemini service failed. "
                        "Check the backend terminal for details."
                    ),
                ) from exc

            print(
                "AgentOS: Gemini call took "
                f"{perf_counter() - started:.2f} seconds"
            )

            if not ai_response:
                raise HTTPException(
                    status_code=502,
                    detail="Gemini returned an empty response.",
                )

        # Save both local and Gemini responses to conversation history.
        db.add(
            ChatMessage(
                session_id=chat_session.id,
                role="assistant",
                message=ai_response,
            )
        )

        chat_session.updated_at = datetime.utcnow()
        db.commit()

        return ChatResponse(
            session_id=chat_session.id,
            response=ai_response,
        )

    except HTTPException:
        db.rollback()
        raise
    except Exception as exc:
        db.rollback()
        print(
            f"AgentOS chat error: {type(exc).__name__}: {exc}"
        )
        raise HTTPException(
            status_code=500,
            detail=(
                "AgentOS could not process this message. "
                "Check the backend terminal."
            ),
        ) from exc


@router.get(
    "/sessions/{session_id}/messages",
    response_model=list[HistoryMessage],
)
def get_chat_history(
    session_id: int,
    db: Session = Depends(get_db),
):
    chat_session = (
        db.query(ChatSession)
        .filter(ChatSession.id == session_id)
        .first()
    )

    if chat_session is None:
        raise HTTPException(
            status_code=404,
            detail="Chat session not found.",
        )

    messages = (
        db.query(ChatMessage)
        .filter(ChatMessage.session_id == session_id)
        .order_by(ChatMessage.id.asc())
        .all()
    )

    return [
        HistoryMessage(
            role=item.role,
            content=item.message,
            created_at=item.created_at.isoformat(),
        )
        for item in messages
    ]
