
from app.tools.registry import ToolRegistry, ToolDefinition


# Create registry
registry = ToolRegistry()


# Create sample tool
def sample_search(query: str):
    return f"Searching for: {query}"


# Register tool
web_tool = ToolDefinition(
    name="web_search",
    description="Search the internet",
    function=sample_search,
)

registry.register(web_tool)


# Test 1: List tools
print("Registered tools:")

for tool in registry.list_tools():
    print(tool.name, "-", tool.description)


# Test 2: Retrieve tool
tool = registry.get_tool("web_search")

print("\nRetrieved tool:", tool.name)


# Test 3: Execute its function
result = tool.function("Artificial Intelligence")

print("Execution result:", result)


# Test 4: Check existence
print(
    "\nTool exists:",
    registry.tool_exists("web_search")
)
