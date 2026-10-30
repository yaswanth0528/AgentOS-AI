
from app.services.tool_manager import ToolManager


def sample_search(query: str):
    return {
        "status": "success",
        "result": f"Searching for: {query}"
    }


# 1. Initialize Tool Manager
manager = ToolManager()

# 2. Register a tool and grant permission
manager.register_tool(
    name="web_search",
    description="Search the internet",
    function=sample_search,
    allowed=True
)

# 3. List registered tools
print("Available tools:")
print(manager.get_available_tools())

# 4. Check whether the tool exists
print("Tool exists:", manager.tool_exists("web_search"))

# 5. Check permission
print("Permission:", manager.is_tool_allowed("web_search"))

# 6. Execute the tool
result = manager.execute_tool(
    "web_search",
    query="Latest AI developments"
)

print("Execution result:", result)

# 7. Revoke permission
manager.revoke_permission("web_search")

print("Permission after revoking:",
      manager.is_tool_allowed("web_search"))

# 8. Verify that execution is blocked
try:
    manager.execute_tool(
        "web_search",
        query="Latest AI developments"
    )
except PermissionError as error:
    print("Security check:", error)
