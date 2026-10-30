
from app.services.tool_manager import ToolManager
from app.tools.builtins.weather_tool import weather_tool


manager = ToolManager()

# Register the weather tool
manager.register_tool(
    name="weather",
    description="Get current weather information for a city",
    function=weather_tool,
    allowed=True
)

# Execute the tool
result = manager.execute_tool(
    "weather",
    city="Vizianagaram"
)

print("\nWeather Information")
print("-------------------")

for key, value in result.items():
    print(f"{key}: {value}")
