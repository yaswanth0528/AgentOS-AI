
from app.services.tool_manager import ToolManager
from app.tools.builtins.web_search_tool import web_search_tool


# Initialize Tool Manager
manager = ToolManager()

# Register the actual web search tool
manager.register_tool(
    name="web_search",
    description="Search the internet using Tavily",
    function=web_search_tool,
    allowed=True
)

# Display registered tools
print("Available tools:")
print(manager.get_available_tools())

# Execute web search through Tool Manager
results = manager.execute_tool(
    "web_search",
    query="Latest developments in artificial intelligence",
    max_results=3
)

# Display results
print("\nSearch results:")

for index, result in enumerate(results, start=1):
    print(f"\nResult {index}")
    print("Title:", result.get("title"))
    print("URL:", result.get("url"))
    print("Content:", result.get("content"))
