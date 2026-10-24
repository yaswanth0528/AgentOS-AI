
from app.database.database import engine
from app.database.models import ChatRequestRecord

# Create only the new request-tracking table.
# Existing chat_sessions and chat_messages are not dropped.
ChatRequestRecord.__table__.create(
    bind=engine,
    checkfirst=True
)

print("Chat request tracking table is ready.")
