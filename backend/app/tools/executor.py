
import logging
from typing import Any

from app.tools.registry import ToolRegistry
from app.tools.permissions import ToolPermissionManager


logger = logging.getLogger(__name__)


class ToolExecutor:
    """
    Executes registered AgentOS tools after permission checks.
    """

    def __init__(
        self,
        registry: ToolRegistry,
        permissions: ToolPermissionManager,
    ):
        self.registry = registry
        self.permissions = permissions

    def execute(
        self,
        tool_name: str,
        **kwargs: Any,
    ) -> Any:
        """
        Retrieve, authorize and execute a tool.
        """

        # Step 1: Check permission
        self.permissions.require_permission(tool_name)

        # Step 2: Retrieve registered tool
        tool = self.registry.get_tool(tool_name)

        # Step 3: Execute tool
        try:
            logger.info("Executing AgentOS tool: %s", tool_name)

            result = tool.function(**kwargs)

            logger.info(
                "Tool '%s' executed successfully.",
                tool_name,
            )

            return result

        except Exception:
            logger.exception(
                "Tool execution failed: %s",
                tool_name,
            )
            raise
