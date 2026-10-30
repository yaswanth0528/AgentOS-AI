
import os

from dotenv import load_dotenv
from tavily import TavilyClient

load_dotenv()

api_key = os.getenv("TAVILY_API_KEY")

if not api_key:
    raise RuntimeError("TAVILY_API_KEY is missing from .env")

client = TavilyClient(api_key=api_key)

query = (
    "Virat Kohli total international cricket "
    "centuries latest statistics"
)

try:
    response = client.search(
    query=(
        "Virat Kohli total international centuries "
        "latest October 2026 ODI Test T20 statistics"
    ),
    search_depth="advanced",
    topic="news",
    time_range="month",
    max_results=5,
)

    print("\nWEB SEARCH RESULTS:\n")

    for index, result in enumerate(
        response.get("results", []), start=1
    ):
        print(f"Result {index}")
        print("Title:", result.get("title"))
        print("URL:", result.get("url"))
        print("Content:", result.get("content"))
        print("-" * 50)

except Exception as exc:
    print("Tavily search failed:", exc)
