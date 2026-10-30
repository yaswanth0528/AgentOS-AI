
from app.services.memory_extractor import extract_memories


message = (
"I'm studying Information Technology. "
"My career goal is to become a Data Engineer. "
"I prefer Python over Java."
)

memories = extract_memories(message)

print("Extracted memories:")

for memory in memories:
    print("-", memory)
