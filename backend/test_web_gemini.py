
from app.services.web_search import search_web
from app.services.gemini_service import generate_web_response


def main():
    question = (
        "How many international centuries has "
        "Virat Kohli scored as of October 2026?"
    )

    print("\nStep 1: Searching the web with Tavily...\n")

    try:
        sources = search_web(
            query=question,
            max_results=5,
        )

        print(f"Found {len(sources)} web sources.")

        if not sources:
            print("No sources found. Stopping test.")
            return

    except Exception as exc:
        print("Tavily search failed:", exc)
        return

    print("\nStep 2: Generating a grounded answer with Gemini...\n")

    try:
        answer = generate_web_response(
            message=question,
            sources=sources,
        )

        print("\nAGENTOS ANSWER:\n")
        print(answer)

    except Exception as exc:
        print("Gemini generation failed:", exc)
        return


if __name__ == "__main__":
    main()
