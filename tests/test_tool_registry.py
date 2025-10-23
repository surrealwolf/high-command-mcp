"""Tests for tool registry functionality."""

import pytest

from highcommand.tool_registry import ToolDefinition, ToolParameter, ToolRegistry


def test_tool_parameter_creation():
    """Test creating tool parameters."""
    param = ToolParameter(
        name="planet_index",
        type="integer",
        description="Index of the planet",
        required=True,
    )
    assert param.name == "planet_index"
    assert param.type == "integer"
    assert param.description == "Index of the planet"
    assert param.required is True


def test_tool_definition_to_input_schema():
    """Test converting tool definition to MCP InputSchema."""
    params = [
        ToolParameter(
            name="planet_index",
            type="integer",
            description="Index of the planet",
            required=True,
        ),
        ToolParameter(
            name="filter",
            type="string",
            description="Filter results",
            required=False,
        ),
    ]

    tool = ToolDefinition(
        name="get_planet_status",
        description="Get planet status",
        handler=lambda: None,
        parameters=params,
    )

    schema = tool.to_input_schema()

    assert schema["type"] == "object"
    assert "planet_index" in schema["properties"]
    assert "filter" in schema["properties"]
    assert schema["properties"]["planet_index"]["type"] == "integer"
    assert schema["properties"]["filter"]["type"] == "string"
    assert "planet_index" in schema["required"]
    assert "filter" not in schema["required"]


def test_tool_definition_validate_arguments_success():
    """Test validating valid arguments."""
    params = [
        ToolParameter(
            name="planet_index",
            type="integer",
            description="Index of the planet",
            required=True,
        )
    ]

    tool = ToolDefinition(
        name="get_planet_status",
        description="Get planet status",
        handler=lambda: None,
        parameters=params,
    )

    # Should not raise
    tool.validate_arguments({"planet_index": 42})


def test_tool_definition_validate_arguments_missing_required():
    """Test validating arguments with missing required parameter."""
    params = [
        ToolParameter(
            name="planet_index",
            type="integer",
            description="Index of the planet",
            required=True,
        )
    ]

    tool = ToolDefinition(
        name="get_planet_status",
        description="Get planet status",
        handler=lambda: None,
        parameters=params,
    )

    with pytest.raises(ValueError, match="Missing required parameter"):
        tool.validate_arguments({})


def test_tool_definition_validate_arguments_wrong_type():
    """Test validating arguments with wrong type."""
    params = [
        ToolParameter(
            name="planet_index",
            type="integer",
            description="Index of the planet",
            required=True,
        )
    ]

    tool = ToolDefinition(
        name="get_planet_status",
        description="Get planet status",
        handler=lambda: None,
        parameters=params,
    )

    with pytest.raises(ValueError, match="must be integer"):
        tool.validate_arguments({"planet_index": "not_an_int"})


def test_tool_registry_register():
    """Test registering tools in registry."""
    registry = ToolRegistry()

    tool = ToolDefinition(
        name="test_tool",
        description="Test tool",
        handler=lambda: None,
        parameters=[],
    )

    registry.register(tool)
    assert registry.get("test_tool") is tool


def test_tool_registry_register_duplicate():
    """Test that registering duplicate tool raises error."""
    registry = ToolRegistry()

    tool = ToolDefinition(
        name="test_tool",
        description="Test tool",
        handler=lambda: None,
        parameters=[],
    )

    registry.register(tool)

    with pytest.raises(ValueError, match="already registered"):
        registry.register(tool)


def test_tool_registry_get_nonexistent():
    """Test getting non-existent tool returns None."""
    registry = ToolRegistry()
    assert registry.get("nonexistent") is None


def test_tool_registry_list_all():
    """Test listing all registered tools."""
    registry = ToolRegistry()

    tool1 = ToolDefinition(
        name="tool1",
        description="Tool 1",
        handler=lambda: None,
        parameters=[],
    )
    tool2 = ToolDefinition(
        name="tool2",
        description="Tool 2",
        handler=lambda: None,
        parameters=[],
    )

    registry.register(tool1)
    registry.register(tool2)

    tools = registry.list_all()
    assert len(tools) == 2
    assert tool1 in tools
    assert tool2 in tools


def test_tool_registry_validate_and_get_success():
    """Test validate_and_get with valid arguments."""
    registry = ToolRegistry()

    params = [
        ToolParameter(
            name="planet_index",
            type="integer",
            description="Index of the planet",
            required=True,
        )
    ]

    tool = ToolDefinition(
        name="test_tool",
        description="Test tool",
        handler=lambda: None,
        parameters=params,
    )

    registry.register(tool)

    # Should not raise
    validated_tool = registry.validate_and_get("test_tool", {"planet_index": 42})
    assert validated_tool is tool


def test_tool_registry_validate_and_get_nonexistent():
    """Test validate_and_get with nonexistent tool."""
    registry = ToolRegistry()

    with pytest.raises(ValueError, match="Unknown tool"):
        registry.validate_and_get("nonexistent", {})


def test_tool_registry_validate_and_get_invalid_arguments():
    """Test validate_and_get with invalid arguments."""
    registry = ToolRegistry()

    params = [
        ToolParameter(
            name="planet_index",
            type="integer",
            description="Index of the planet",
            required=True,
        )
    ]

    tool = ToolDefinition(
        name="test_tool",
        description="Test tool",
        handler=lambda: None,
        parameters=params,
    )

    registry.register(tool)

    with pytest.raises(ValueError):
        registry.validate_and_get("test_tool", {})


def test_tool_registry_clear():
    """Test clearing all tools from registry."""
    registry = ToolRegistry()

    tool = ToolDefinition(
        name="test_tool",
        description="Test tool",
        handler=lambda: None,
        parameters=[],
    )

    registry.register(tool)
    assert len(registry.list_all()) == 1

    registry.clear()
    assert len(registry.list_all()) == 0
