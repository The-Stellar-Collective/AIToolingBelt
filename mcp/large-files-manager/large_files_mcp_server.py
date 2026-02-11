#!/usr/bin/env python3
"""
MCP Server for finding and managing large files on disk.
Provides tools to list the largest files and delete them.
"""

import os
import asyncio
from pathlib import Path
from typing import Optional
from mcp.server.models import InitializationOptions
import mcp.types as types
from mcp.server import NotificationOptions, Server
import mcp.server.stdio


server = Server("large-files-manager")


def get_file_size_str(size_bytes: int) -> str:
    """Convert bytes to human-readable format."""
    for unit in ['B', 'KB', 'MB', 'GB', 'TB']:
        if size_bytes < 1024.0:
            return f"{size_bytes:.2f} {unit}"
        size_bytes /= 1024.0
    return f"{size_bytes:.2f} PB"


def find_large_files(
    start_path: str,
    top_n: int = 20,
    min_size_mb: float = 1.0,
    exclude_dirs: Optional[list[str]] = None
) -> list[dict]:
    """
    Find the largest files on disk.

    Args:
        start_path: Root directory to start searching from
        top_n: Number of top files to return
        min_size_mb: Minimum file size in MB to consider
        exclude_dirs: List of directory names to exclude (e.g., ['node_modules', '.git'])

    Returns:
        List of dictionaries with file information
    """
    if exclude_dirs is None:
        exclude_dirs = ['.git', 'node_modules', '__pycache__', '.venv', 'venv',
                       'Library', 'Applications', 'System']

    min_size_bytes = min_size_mb * 1024 * 1024
    files_data = []

    start_path = os.path.expanduser(start_path)

    for root, dirs, files in os.walk(start_path):
        # Remove excluded directories from the search
        dirs[:] = [d for d in dirs if d not in exclude_dirs]

        for filename in files:
            try:
                filepath = os.path.join(root, filename)
                if os.path.islink(filepath):
                    continue

                size = os.path.getsize(filepath)

                if size >= min_size_bytes:
                    files_data.append({
                        'path': filepath,
                        'size': size,
                        'size_str': get_file_size_str(size),
                        'name': filename
                    })
            except (OSError, PermissionError):
                # Skip files we can't access
                continue

    # Sort by size descending and return top N
    files_data.sort(key=lambda x: x['size'], reverse=True)
    return files_data[:top_n]


@server.list_tools()
async def handle_list_tools() -> list[types.Tool]:
    """List available tools."""
    return [
        types.Tool(
            name="list_large_files",
            description="Find and list the largest files on disk. Returns a ranked list of files by size.",
            inputSchema={
                "type": "object",
                "properties": {
                    "start_path": {
                        "type": "string",
                        "description": "Root directory to start searching from (e.g., '~' for home directory, '/' for entire disk)",
                        "default": "~"
                    },
                    "top_n": {
                        "type": "number",
                        "description": "Number of largest files to return",
                        "default": 20
                    },
                    "min_size_mb": {
                        "type": "number",
                        "description": "Minimum file size in megabytes to consider",
                        "default": 1.0
                    },
                    "exclude_dirs": {
                        "type": "array",
                        "items": {"type": "string"},
                        "description": "List of directory names to exclude from search (default: .git, node_modules, __pycache__, .venv, venv, Library, Applications, System)",
                        "default": None
                    }
                },
                "required": []
            },
        ),
        types.Tool(
            name="delete_file",
            description="Delete a specific file from disk. Use with caution!",
            inputSchema={
                "type": "object",
                "properties": {
                    "file_path": {
                        "type": "string",
                        "description": "Full path to the file to delete"
                    },
                    "confirm": {
                        "type": "boolean",
                        "description": "Must be set to true to confirm deletion",
                        "default": False
                    }
                },
                "required": ["file_path", "confirm"]
            },
        ),
        types.Tool(
            name="get_file_info",
            description="Get detailed information about a specific file",
            inputSchema={
                "type": "object",
                "properties": {
                    "file_path": {
                        "type": "string",
                        "description": "Full path to the file"
                    }
                },
                "required": ["file_path"]
            },
        ),
    ]


@server.call_tool()
async def handle_call_tool(
    name: str, arguments: dict | None
) -> list[types.TextContent | types.ImageContent | types.EmbeddedResource]:
    """Handle tool execution requests."""

    if name == "list_large_files":
        args = arguments or {}
        start_path = args.get("start_path", "~")
        top_n = int(args.get("top_n", 20))
        min_size_mb = float(args.get("min_size_mb", 1.0))
        exclude_dirs = args.get("exclude_dirs")

        try:
            files = find_large_files(start_path, top_n, min_size_mb, exclude_dirs)

            if not files:
                return [types.TextContent(
                    type="text",
                    text=f"No files found larger than {min_size_mb} MB in {start_path}"
                )]

            result = f"Top {len(files)} largest files in {start_path}:\n\n"
            result += f"{'Rank':<5} {'Size':<12} {'Path'}\n"
            result += "=" * 80 + "\n"

            for idx, file_info in enumerate(files, 1):
                result += f"{idx:<5} {file_info['size_str']:<12} {file_info['path']}\n"

            total_size = sum(f['size'] for f in files)
            result += "\n" + "=" * 80 + "\n"
            result += f"Total size of listed files: {get_file_size_str(total_size)}\n"

            return [types.TextContent(type="text", text=result)]

        except Exception as e:
            return [types.TextContent(
                type="text",
                text=f"Error searching for files: {str(e)}"
            )]

    elif name == "delete_file":
        args = arguments or {}
        file_path = args.get("file_path")
        confirm = args.get("confirm", False)

        if not file_path:
            return [types.TextContent(
                type="text",
                text="Error: file_path is required"
            )]

        if not confirm:
            return [types.TextContent(
                type="text",
                text="Error: confirm must be set to true to delete the file. This is a safety measure."
            )]

        try:
            file_path = os.path.expanduser(file_path)

            if not os.path.exists(file_path):
                return [types.TextContent(
                    type="text",
                    text=f"Error: File not found: {file_path}"
                )]

            if not os.path.isfile(file_path):
                return [types.TextContent(
                    type="text",
                    text=f"Error: Path is not a file: {file_path}"
                )]

            # Get file info before deletion
            size = os.path.getsize(file_path)
            size_str = get_file_size_str(size)

            # Delete the file
            os.remove(file_path)

            return [types.TextContent(
                type="text",
                text=f"Successfully deleted file:\nPath: {file_path}\nSize: {size_str}"
            )]

        except PermissionError:
            return [types.TextContent(
                type="text",
                text=f"Error: Permission denied to delete {file_path}"
            )]
        except Exception as e:
            return [types.TextContent(
                type="text",
                text=f"Error deleting file: {str(e)}"
            )]

    elif name == "get_file_info":
        args = arguments or {}
        file_path = args.get("file_path")

        if not file_path:
            return [types.TextContent(
                type="text",
                text="Error: file_path is required"
            )]

        try:
            file_path = os.path.expanduser(file_path)

            if not os.path.exists(file_path):
                return [types.TextContent(
                    type="text",
                    text=f"Error: File not found: {file_path}"
                )]

            stat_info = os.stat(file_path)
            size_str = get_file_size_str(stat_info.st_size)

            from datetime import datetime
            modified_time = datetime.fromtimestamp(stat_info.st_mtime)
            created_time = datetime.fromtimestamp(stat_info.st_ctime)

            result = f"File Information:\n"
            result += f"Path: {file_path}\n"
            result += f"Size: {size_str} ({stat_info.st_size:,} bytes)\n"
            result += f"Modified: {modified_time.strftime('%Y-%m-%d %H:%M:%S')}\n"
            result += f"Created: {created_time.strftime('%Y-%m-%d %H:%M:%S')}\n"
            result += f"Permissions: {oct(stat_info.st_mode)[-3:]}\n"

            return [types.TextContent(type="text", text=result)]

        except Exception as e:
            return [types.TextContent(
                type="text",
                text=f"Error getting file info: {str(e)}"
            )]

    else:
        raise ValueError(f"Unknown tool: {name}")


async def main():
    """Main entry point for the MCP server."""
    async with mcp.server.stdio.stdio_server() as (read_stream, write_stream):
        await server.run(
            read_stream,
            write_stream,
            InitializationOptions(
                server_name="large-files-manager",
                server_version="0.1.0",
                capabilities=server.get_capabilities(
                    notification_options=NotificationOptions(),
                    experimental_capabilities={},
                ),
            ),
        )


if __name__ == "__main__":
    asyncio.run(main())
