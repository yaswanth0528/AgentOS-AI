
from app.services.tool_manager import ToolManager
from app.tools.builtins import register_builtin_tools


manager = ToolManager()

register_builtin_tools(manager)

print("Registered AgentOS Built-in Tools:")
print("----------------------------------")

for tool in manager.get_available_tools():
    print(f"{tool['name']}: {tool['description']}")

print("\nPermission Status:")

for tool in manager.get_available_tools():
    name = tool["name"]
    print(f"{name}: {manager.is_tool_allowed(name)}")
