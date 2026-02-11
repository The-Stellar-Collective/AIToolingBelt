"""
Common utilities and helpers for MCP servers.
Provides reusable components for building MCP servers.
"""

import asyncio
from typing import Callable, Any
from mcp.server.models import InitializationOptions
from mcp.server import NotificationOptions, Server
import mcp.server.stdio
import mcp.types as types


def create_text_response(text: str) -> list[types.TextContent]:
    """Create a standard text response for MCP tools."""
    return [types.TextContent(type="text", text=text)]


def create_error_response(error_msg: str) -> list[types.TextContent]:
    """Create a standard error response for MCP tools."""
    return create_text_response(f"Error: {error_msg}")


async def run_mcp_server(
    server: Server,
    server_name: str,
    server_version: str = "0.1.0"
) -> None:
    """
    Run an MCP server with standard configuration.

    Args:
        server: The MCP Server instance
        server_name: Name of the server
        server_version: Version string
    """
    async with mcp.server.stdio.stdio_server() as (read_stream, write_stream):
        await server.run(
            read_stream,
            write_stream,
            InitializationOptions(
                server_name=server_name,
                server_version=server_version,
                capabilities=server.get_capabilities(
                    notification_options=NotificationOptions(),
                    experimental_capabilities={},
                ),
            ),
        )


def safe_get_arg(arguments: dict | None, key: str, default: Any = None) -> Any:
    """Safely get an argument from the arguments dict."""
    if arguments is None:
        return default
    return arguments.get(key, default)


class MCPToolBuilder:
    """Helper class for building MCP tool definitions."""

    @staticmethod
    def create_tool(
        name: str,
        description: str,
        properties: dict,
        required: list[str] | None = None
    ) -> types.Tool:
        """
        Create a tool definition with standard schema.

        Args:
            name: Tool name
            description: Tool description
            properties: JSON schema properties
            required: List of required property names
        """
        return types.Tool(
            name=name,
            description=description,
            inputSchema={
                "type": "object",
                "properties": properties,
                "required": required or []
            }
        )
