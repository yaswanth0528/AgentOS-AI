
from app.database.database import SessionLocal
from app.database.models import User

from app.services.memory_search import search_relevant_memories


with SessionLocal() as db:
    user = (
        db.query(User)
        .filter(User.username == "local_user")
        .first()
    )

    if user is None:
        raise RuntimeError("Local user not found.")

    questions = [
        "What is my career goal?",
        "What is my friend's name?",
        "Which degree am I studying?",
    ]

    for question in questions:
        print(f"\nQuestion: {question}")

        memories = search_relevant_memories(
            db=db,
            user_id=user.id,
            query=question,
        )

        if not memories:
            print("No matching memories found.")

        for memory in memories:
            print("-", memory.memory_text)
