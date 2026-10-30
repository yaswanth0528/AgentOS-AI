
from datetime import datetime

from sqlalchemy import (
    DateTime,
    ForeignKey,
    Integer,
    String,
    Text,
)
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database.database import Base


<<<<<<< HEAD
# --------------------------------------------------
# User Model
# --------------------------------------------------
=======
# ==========================================
# USER MODEL
# ==========================================
>>>>>>> origin/main

class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
<<<<<<< HEAD
        index=True
=======
        autoincrement=True
>>>>>>> origin/main
    )

    username: Mapped[str] = mapped_column(
        String(100),
        unique=True,
<<<<<<< HEAD
        nullable=False,
        index=True
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=datetime.utcnow
    )

    chat_sessions = relationship(
        "ChatSession",
        back_populates="user",
        cascade="all, delete-orphan"
    )

    memories = relationship(
        "UserMemory",
        back_populates="user",
        cascade="all, delete-orphan"
    )

# --------------------------------------------------
# User Memory Model
# --------------------------------------------------

class UserMemory(Base):
    __tablename__ = "user_memories"

    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
        index=True
    )

    user_id: Mapped[int] = mapped_column(
        ForeignKey("users.id"),
        nullable=False,
        index=True
    )

    memory_text: Mapped[str] = mapped_column(
        Text,
=======
>>>>>>> origin/main
        nullable=False
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=datetime.utcnow
    )

<<<<<<< HEAD
    updated_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=datetime.utcnow,
        onupdate=datetime.utcnow
    )

    user = relationship(
        "User",
        back_populates="memories"
    )

# --------------------------------------------------
# Chat Session Model
# --------------------------------------------------
=======
    sessions = relationship(
        "ChatSession",
        back_populates="user"
    )

    memories = relationship(
        "UserMemory",
        back_populates="user",
        cascade="all, delete-orphan"
    )


# ==========================================
# CHAT SESSION MODEL
# ==========================================
>>>>>>> origin/main

class ChatSession(Base):
    __tablename__ = "chat_sessions"

    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
        index=True
    )

<<<<<<< HEAD
    user_id: Mapped[int] = mapped_column(
        ForeignKey("users.id"),
        nullable=False,
        index=True
=======
    user_id: Mapped[int | None] = mapped_column(
        ForeignKey("users.id"),
        nullable=True
>>>>>>> origin/main
    )

    title: Mapped[str] = mapped_column(
        String(255),
        default="New Chat"
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=datetime.utcnow
    )

    updated_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=datetime.utcnow,
        onupdate=datetime.utcnow
    )

    user = relationship(
        "User",
<<<<<<< HEAD
        back_populates="chat_sessions"
=======
        back_populates="sessions"
>>>>>>> origin/main
    )

    messages = relationship(
        "ChatMessage",
        back_populates="session",
        cascade="all, delete-orphan"
    )


<<<<<<< HEAD
# --------------------------------------------------
# Chat Message Model
# --------------------------------------------------
=======
# ==========================================
# CHAT MESSAGE MODEL
# ==========================================
>>>>>>> origin/main

class ChatMessage(Base):
    __tablename__ = "chat_messages"

    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
        index=True
    )

    session_id: Mapped[int] = mapped_column(
        ForeignKey("chat_sessions.id"),
        nullable=False
    )

    role: Mapped[str] = mapped_column(
        String(20),
        nullable=False
    )

    message: Mapped[str] = mapped_column(
        Text,
        nullable=False
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=datetime.utcnow
    )

    session = relationship(
        "ChatSession",
        back_populates="messages"
    )


<<<<<<< HEAD
# --------------------------------------------------
# Chat Request Record Model
# --------------------------------------------------
=======
# ==========================================
# REQUEST RELIABILITY MODEL (PHASE 1)
# ==========================================
>>>>>>> origin/main

class ChatRequestRecord(Base):
    __tablename__ = "chat_request_records"

    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
        index=True
    )

    request_id: Mapped[str] = mapped_column(
        String(36),
        unique=True,
        nullable=False,
        index=True
    )

    session_id: Mapped[int] = mapped_column(
        ForeignKey("chat_sessions.id"),
        nullable=False
    )

    user_message_id: Mapped[int] = mapped_column(
        ForeignKey("chat_messages.id"),
        nullable=False
    )

    status: Mapped[str] = mapped_column(
        String(20),
        nullable=False,
        default="processing"
    )

<<<<<<< HEAD
    attempt_count: Mapped[int] = mapped_column(
        Integer,
        nullable=False,
        default=1
    )

    processing_started_at: Mapped[datetime | None] = mapped_column(
        DateTime,
        nullable=True
    )

=======
>>>>>>> origin/main
    response: Mapped[str | None] = mapped_column(
        Text,
        nullable=True
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=datetime.utcnow
    )

    updated_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=datetime.utcnow,
        onupdate=datetime.utcnow
    )

<<<<<<< HEAD
    session = relationship("ChatSession")

    user_message = relationship("ChatMessage")
=======
    attempt_count: Mapped[int] = mapped_column(
        Integer,
        nullable=False,
        default=1
    )

    processing_started_at: Mapped[datetime | None] = mapped_column(
        DateTime,
        nullable=True
    )


# ==========================================
# LONG-TERM MEMORY MODEL (PHASE 2)
# ==========================================

class UserMemory(Base):
    __tablename__ = "user_memories"

    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
        autoincrement=True
    )

    user_id: Mapped[int] = mapped_column(
        ForeignKey("users.id"),
        nullable=False,
        index=True
    )

    memory_text: Mapped[str] = mapped_column(
        Text,
        nullable=False
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=datetime.utcnow
    )

    updated_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=datetime.utcnow,
        onupdate=datetime.utcnow
    )

    user = relationship(
        "User",
        back_populates="memories"
    )
>>>>>>> origin/main
