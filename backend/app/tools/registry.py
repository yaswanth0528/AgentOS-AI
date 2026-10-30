
from dataclasses import dataclass
from typing import Any, Callable


@dataclass
class ToolDefinition:
    """
    Stores information about an individual tool.
    """

    name: str
    description: str
    function: Callable[..., Any]


class ToolRegistry:
    """
    Central registry for managing AgentOS tools.
    """

    def __init__(self):
        self._tools: dict[str, ToolDefinition] = {}

    def register(self, tool: ToolDefinition) -> None:
        """
        Register a new tool.
        """

        if not isinstance(tool, ToolDefinition):
            raise TypeError("Expected a ToolDefinition object.")

        if not tool.name or not tool.name.strip():
            raise ValueError("Tool name cannot be empty.")

        if not callable(tool.function):
            raise ValueError("Tool function must be callable.")

        name = tool.name.strip()

        if name in self._tools:
            raise ValueError(
                f"Tool '{name}' is already registered."
            )

        self._tools[name] = tool

    def get_tool(self, name: str) -> ToolDefinition:
        """
        Retrieve a registered tool by name.
        """

        tool = self._tools.get(name)

        if tool is None:
            raise KeyError(
                f"Tool '{name}' is not registered."
            )

        return tool

    def list_tools(self) -> list[ToolDefinition]:
        """
        Return all registered tools.
        """

        return list(self._tools.values())

    def tool_exists(self, name: str) -> bool:
        """
        Check whether a tool is registered.
        """

        return name in self._tools

    def remove_tool(self, name: str) -> None:
        """
        Remove a registered tool.
        """

        if name not in self._tools:
            raise KeyError(
                f"Tool '{name}' is not registered."
            )

        del self._tools[name]
