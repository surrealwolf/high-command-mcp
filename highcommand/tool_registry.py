"""Tool registry and management for High-Command MCP Server."""

from dataclasses import dataclass
from typing import Any, Callable, Optional

import structlog

logger = structlog.get_logger(__name__)


@dataclass
class ToolParameter:
    """Definition of a tool parameter."""

    name: str
    type: str
    description: str
    required: bool = True


@dataclass
class ToolDefinition:
    """Definition of an MCP tool."""

    name: str
    description: str
    handler: Callable[..., Any]
    parameters: list[ToolParameter]

    def to_input_schema(self) -> dict[str, Any]:
        """Convert to MCP InputSchema format."""
        properties = {}
        required_params = []

        for param in self.parameters:
            properties[param.name] = {
                "type": param.type,
                "description": param.description,
            }
            if param.required:
                required_params.append(param.name)

        return {
            "type": "object",
            "properties": properties,
            "required": required_params,
        }

    def validate_arguments(self, arguments: dict) -> None:
        """Validate tool arguments against parameter definitions.

        Args:
            arguments: Arguments passed to the tool

        Raises:
            ValueError: If required parameters are missing or types are invalid
        """
        for param in self.parameters:
            if param.required and param.name not in arguments:
                raise ValueError(f"Missing required parameter: {param.name}")

            if param.name in arguments:
                arg_value = arguments[param.name]
                # Type validation (basic - can be enhanced)
                if param.type == "integer":
                    if not isinstance(arg_value, int):
                        raise ValueError(
                            f"Parameter '{param.name}' must be integer, got {type(arg_value).__name__}"
                        )
                elif param.type == "string":
                    if not isinstance(arg_value, str):
                        raise ValueError(
                            f"Parameter '{param.name}' must be string, got {type(arg_value).__name__}"
                        )
                elif param.type == "boolean":
                    if not isinstance(arg_value, bool):
                        raise ValueError(
                            f"Parameter '{param.name}' must be boolean, got {type(arg_value).__name__}"
                        )


class ToolRegistry:
    """Registry of available tools."""

    def __init__(self):
        """Initialize empty tool registry."""
        self._tools: dict[str, ToolDefinition] = {}

    def register(self, tool: ToolDefinition) -> None:
        """Register a tool.

        Args:
            tool: Tool definition to register

        Raises:
            ValueError: If tool with same name already registered
        """
        if tool.name in self._tools:
            raise ValueError(f"Tool '{tool.name}' already registered")

        self._tools[tool.name] = tool
        logger.info("Tool registered", tool_name=tool.name)

    def get(self, name: str) -> Optional[ToolDefinition]:
        """Get tool by name.

        Args:
            name: Tool name

        Returns:
            Tool definition or None if not found
        """
        return self._tools.get(name)

    def list_all(self) -> list[ToolDefinition]:
        """List all registered tools.

        Returns:
            List of tool definitions
        """
        return list(self._tools.values())

    def validate_and_get(self, name: str, arguments: dict) -> ToolDefinition:
        """Get tool and validate arguments.

        Args:
            name: Tool name
            arguments: Arguments to validate

        Returns:
            Validated tool definition

        Raises:
            ValueError: If tool not found or arguments invalid
        """
        tool = self.get(name)
        if not tool:
            raise ValueError(f"Unknown tool: {name}")

        tool.validate_arguments(arguments)
        return tool

    def clear(self) -> None:
        """Clear all registered tools."""
        self._tools.clear()
