
from app.tools.registry import ToolRegistry, ToolDefinition
from app.tools.permissions import ToolPermissionManager
from app.tools.executor import ToolExecutor


# Create registry
registry = ToolRegistry()


# Create sample function
def web_search(query: str):
    return {
        "status": "success",
        "result": f"Searching for {query}"
    }


# Register tool
registry.register(
    ToolDefinition(
        name="web_search",
        description="Search the internet",
        function=web_search,
    )
)


# Create permission manager
permissions = ToolPermissionManager()


# Grant permission
permissions.grant_permission("web_search")


# Create executor
executor = ToolExecutor(
    registry=registry,
    permissions=permissions,
)


# Execute tool
result = executor.execute(
    "web_search",
    query="Latest AI developments",
)

print("Execution result:", result)


# Test permission denial
permissions.revoke_permission("web_search")

try:
    executor.execute(
        "web_search",
        query="Artificial Intelligence",
    )
except PermissionError as error:
    print("Permission test:", error)
