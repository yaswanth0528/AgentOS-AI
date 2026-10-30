
from app.tools.builtins.web_search_tool import web_search_tool
from app.tools.builtins.weather_tool import weather_tool
from app.tools.builtins.pdf_reader_tool import pdf_reader_tool


def register_builtin_tools(manager):
    """
    Register all built-in AgentOS tools.
    """

    manager.register_tool(
        name="web_search",
        description="Search the internet using Tavily",
        function=web_search_tool,
        allowed=True
    )

    manager.register_tool(
        name="weather",
        description="Get current weather information",
        function=weather_tool,
        allowed=True
    )

    manager.register_tool(
        name="pdf_reader",
        description="Extract text from PDF documents",
        function=pdf_reader_tool,
        allowed=True
    )
