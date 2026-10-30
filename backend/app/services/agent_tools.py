
import logging
import re

from app.services.tool_manager import ToolManager
from app.tools.builtins import register_builtin_tools

logger = logging.getLogger(__name__)


# Create one shared Tool Manager.
tool_manager = ToolManager()

# Register built-in tools once when this module is imported.
register_builtin_tools(tool_manager)


def select_tool(message: str) -> str | None:
    """
    Select a built-in tool using rule-based detection.
    """

    text = message.casefold()

    weather_keywords = (
        "weather",
        "temperature",
        "forecast",
        "rain",
        "humidity",
    )

    pdf_keywords = (
        "read pdf",
        "read this pdf",
        "summarize pdf",
        "summarize this pdf",
        "extract text from pdf",
    )

    web_keywords = (
        "latest",
        "current",
        "today",
        "recent",
        "news",
        "search the web",
        "search online",
        "look up",
        "who won",
        "latest score",
        "statistics",
        "record",
    )

    if any(keyword in text for keyword in weather_keywords):
        return "weather"

    if any(keyword in text for keyword in pdf_keywords):
        return "pdf_reader"

    if any(keyword in text for keyword in web_keywords):
        return "web_search"

    return None


def extract_weather_city(message: str) -> str:
    """
    Extract the city from a weather question.

    Examples:
    - What is the weather in Vizianagaram right now?
      -> Vizianagaram
    - Temperature in Hyderabad today?
      -> Hyderabad
    - Weather at Visakhapatnam currently?
      -> Visakhapatnam
    """

    text = message.strip().rstrip("?.!, ")

    # Remove common opening phrases.
    text = re.sub(
        r"^(what(?:'s| is)?\s+)?(the\s+)?",
        "",
        text,
        flags=re.IGNORECASE,
    )

    # Remove common time-related phrases at the end.
    text = re.sub(
        r"\s+(right now|currently|at present|today|now|tonight)$",
        "",
        text,
        flags=re.IGNORECASE,
    )

    # Extract the location after a supported separator.
    match = re.search(
        r"\b(?:in|at|for)\s+(.+)$",
        text,
        flags=re.IGNORECASE,
    )

    if not match:
        raise ValueError(
            "Please specify a city for the weather request. "
            "Example: What is the weather in Vizianagaram?"
        )

    city = match.group(1).strip(" ?.!, ")

    if not city:
        raise ValueError("Please specify a valid city.")

    logger.info("Weather city extracted: %s", city)

    return city


def execute_selected_tool(
    tool_name: str,
    message: str,
) -> dict:
    """
    Execute the selected tool through Tool Manager.
    """

    if tool_name == "weather":

        city = extract_weather_city(message)

        result = tool_manager.execute_tool(
            "weather",
            city=city,
        )

        return {
            "tool": "weather",
            "result": result,
        }

    if tool_name == "web_search":

        result = tool_manager.execute_tool(
            "web_search",
            query=message,
            max_results=5,
        )

        return {
            "tool": "web_search",
            "result": result,
        }

    if tool_name == "pdf_reader":

        raise ValueError(
            "PDF reading requires a PDF file path. "
            "PDF upload support will be added separately."
        )

    raise ValueError(f"Unsupported tool: {tool_name}")
