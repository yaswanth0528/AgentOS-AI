
from app.database.database import SessionLocal
from app.database.models import User
from app.services.memory_service import get_user_memories


with SessionLocal() as db:
    local_user = (
        db.query(User)
        .filter(User.username == "local_user")
        .first()
    )

    if local_user is None:
        raise RuntimeError("Local user not found.")

    local_memories = get_user_memories(
        db=db,
        user_id=local_user.id,
    )

    print("Local user ID:", local_user.id)
    print("Local user memories:", len(local_memories))

    # Choose an ID not assigned to any user.
    unused_user_id = -1

    other_memories = get_user_memories(
        db=db,
        user_id=unused_user_id,
    )

    assert other_memories == [], (
        "Unexpected memories returned for another user."
    )

    print("Basic memory isolation query: PASS")
