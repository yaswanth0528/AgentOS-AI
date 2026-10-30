
import requests
from typing import Any


GEOCODING_URL = "https://geocoding-api.open-meteo.com/v1/search"
WEATHER_URL = "https://api.open-meteo.com/v1/forecast"


def weather_tool(city: str) -> dict[str, Any]:
    """
    Get current weather information for a city using Open-Meteo.
    """

    if not city or not city.strip():
        raise ValueError("City name cannot be empty.")

    city = city.strip()

    try:
        # Step 1: Find the city's latitude and longitude
        location_response = requests.get(
            GEOCODING_URL,
            params={
                "name": city,
                "count": 1,
                "language": "en",
                "format": "json"
            },
            timeout=10
        )
        location_response.raise_for_status()

        locations = location_response.json().get("results", [])

        if not locations:
            raise ValueError(f"City not found: {city}")

        location = locations[0]

        latitude = location["latitude"]
        longitude = location["longitude"]

        # Step 2: Get current weather
        weather_response = requests.get(
            WEATHER_URL,
            params={
                "latitude": latitude,
                "longitude": longitude,
                "current": (
                    "temperature_2m,"
                    "relative_humidity_2m,"
                    "apparent_temperature,"
                    "is_day,"
                    "precipitation,"
                    "weather_code,"
                    "wind_speed_10m"
                ),
                "timezone": "auto"
            },
            timeout=10
        )
        weather_response.raise_for_status()

        current = weather_response.json()["current"]

        return {
            "status": "success",
            "city": location["name"],
            "country": location.get("country"),
            "temperature_c": current["temperature_2m"],
            "feels_like_c": current["apparent_temperature"],
            "humidity_percent": current["relative_humidity_2m"],
            "wind_speed_kmh": current["wind_speed_10m"],
            "precipitation_mm": current["precipitation"],
            "weather_code": current["weather_code"],
            "is_day": current["is_day"],
            "timezone": weather_response.json().get("timezone")
        }

    except requests.RequestException as error:
        raise RuntimeError(
            f"Weather service request failed: {error}"
        ) from error
