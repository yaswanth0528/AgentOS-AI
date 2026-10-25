from app.services.gemini_service import generate_response

try:
    response = generate_response(
        "Hello! Reply with one short sentence."
    )
    print("Gemini response:", response)

except Exception as error:
    print("Error type:", type(error).__name__)
    print("Error details:", str(error))