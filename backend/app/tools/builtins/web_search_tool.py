
from typing import Any

from app.services.web_search import search_web


def web_search_tool(
    query: str,
    max_results: int = 5
) -> list[dict[str, Any]]:
    """
    Search the internet using the existing Tavily service.
    """

    if not query or not query.strip():
        raise ValueError("Search query cannot be empty.")

    if not 1 <= max_results <= 10:
        raise ValueError("max_results must be between 1 and 10.")

    return search_web(
        query=query.strip(),
        max_results=max_results
    )
