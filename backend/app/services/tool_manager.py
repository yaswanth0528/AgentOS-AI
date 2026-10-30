
from typing import Any, Callable

from app.tools.registry import ToolRegistry, ToolDefinition
from app.tools.permissions import ToolPermissionManager
from app.tools.executor import ToolExecutor


class ToolManager:
    """
    Central manager responsible for registering,
    listing, authorizing, and executing AgentOS tools.
    """

    def __init__(self):
        self.registry = ToolRegistry()
        self.permissions = ToolPermissionManager()

        self.executor = ToolExecutor(
            registry=self.registry,
            permissions=self.permissions
        )

    def register_tool(
        self,
        name: str,
        description: str,
        function: Callable[..., Any],
        allowed: bool = False
    ) -> None:
        """Register a tool and optionally grant permission."""

        tool = ToolDefinition(
            name=name,
            description=description,
            function=function
        )

        self.registry.register(tool)

        if allowed:
            self.permissions.grant_permission(name)

    def execute_tool(self, tool_name: str, **kwargs: Any) -> Any:
        """Execute a registered tool after permission validation."""

        return self.executor.execute(tool_name, **kwargs)

    def get_available_tools(self) -> list[dict[str, str]]:
        """Return the registered tools and their descriptions."""

        return [
            {
                "name": tool.name,
                "description": tool.description
            }
            for tool in self.registry.list_tools()
        ]

    def grant_permission(self, tool_name: str) -> None:
        self.permissions.grant_permission(tool_name)

    def revoke_permission(self, tool_name: str) -> None:
        self.permissions.revoke_permission(tool_name)

    def tool_exists(self, tool_name: str) -> bool:
        return self.registry.tool_exists(tool_name)

    def is_tool_allowed(self, tool_name: str) -> bool:
        return self.permissions.is_allowed(tool_name)
