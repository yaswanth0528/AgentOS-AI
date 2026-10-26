
from app.services.web_search import search_web

print("Testing AgentOS Web Search Service...\n")

query = (
    "Virat Kohli total international centuries "
    "latest October 2026"
)

try:
    sources = search_web(query, max_results=5)

    if not sources:
        print("No search results returned.")
    else:
        print(f"Found {len(sources)} sources.\n")

        for index, source in enumerate(sources, start=1):
            print(f"Source {index}")
            print("Title:", source["title"])
            print("URL:", source["url"])
            print("Published:", source["published_date"])
            print("Content:", source["content"][:300])
            print("-" * 60)

except Exception as exc:
    print("Web Search Service Error:", exc)
