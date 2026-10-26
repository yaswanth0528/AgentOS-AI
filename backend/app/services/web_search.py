
import os
import logging

from dotenv import load_dotenv
from tavily import TavilyClient

load_dotenv()

logger = logging.getLogger(__name__)

TAVILY_API_KEY = os.getenv("TAVILY_API_KEY")

if not TAVILY_API_KEY:
    raise RuntimeError(
        "TAVILY_API_KEY is missing from the .env file."
    )

client = TavilyClient(api_key=TAVILY_API_KEY)


def search_web(query: str, max_results: int = 5) -> list[dict]:
    """
    Search the web using Tavily.

    Returns a list of sources containing:
    - title
    - url
    - content
    - published_date (when available)
    """

    logger.info("AgentOS Web Search: %s", query)

    response = client.search(
        query=query,
        search_depth="basic",
        topic="general",
        max_results=max_results,
    )

    sources = []

    for result in response.get("results", []):
        sources.append(
            {
                "title": result.get("title", ""),
                "url": result.get("url", ""),
                "content": result.get("content", ""),
                "published_date": result.get(
                    "published_date"
                ),
            }
        )

    logger.info(
        "AgentOS Web Search returned %s sources",
        len(sources),
    )

    return sources
