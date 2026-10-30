
class ToolPermissionManager:
    """
    Manages execution permissions for AgentOS tools.

    Default policy: Deny access unless explicitly allowed.
    """

    def __init__(self):
        self._allowed_tools: set[str] = set()

    def grant_permission(self, tool_name: str) -> None:
        """Allow a tool to execute."""

        if not tool_name or not tool_name.strip():
            raise ValueError("Tool name cannot be empty.")

        self._allowed_tools.add(tool_name.strip())

    def revoke_permission(self, tool_name: str) -> None:
        """Remove permission for a tool."""

        self._allowed_tools.discard(tool_name.strip())

    def is_allowed(self, tool_name: str) -> bool:
        """Check whether a tool has permission."""

        return tool_name.strip() in self._allowed_tools

    def require_permission(self, tool_name: str) -> None:
        """Stop execution if permission is missing."""

        if not self.is_allowed(tool_name):
            raise PermissionError(
                f"Permission denied for tool: {tool_name}"
            )

    def list_allowed_tools(self) -> list[str]:
        """Return all permitted tools."""

        return sorted(self._allowed_tools)
