
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


def search_web(
    query: str,
    max_results: int = 5,
    search_depth: str = "advanced",
    time_range: str | None = None
) -> list[dict]:
    """
    Search the web using Tavily and return structured sources.

    Advanced search improves retrieval depth.
    time_range can be: day, week, month, year.
    """

    if not query or not query.strip():
        raise ValueError("Search query cannot be empty.")

    max_results = max(1, min(max_results, 10))

    logger.info("Web search started: %s", query)

    try:
        search_params = {
            "query": query.strip(),
            "search_depth": search_depth,
            "topic": "general",
            "max_results": max_results,
            "include_raw_content": "text",
            "include_answer": False
        }

        if time_range:
            search_params["time_range"] = time_range

        response = client.search(**search_params)

        sources = []

        for result in response.get("results", []):
            sources.append({
                "title": result.get("title"),
                "url": result.get("url"),
                "content": result.get("content"),
                "raw_content": result.get("raw_content"),
                "published_date": result.get("published_date"),
                "score": result.get("score")
            })

        logger.info(
            "Web search completed. Retrieved %d sources.",
            len(sources)
        )

        if not sources:
            logger.warning("No search results found for: %s", query)

        return sources

    except Exception:
        logger.exception("Tavily search failed for query: %s", query)
        raise RuntimeError("Web search is temporarily unavailable.")
