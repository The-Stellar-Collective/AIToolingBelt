#!/usr/bin/env python3
"""
MCP Server for managing a live word cloud visualization.
Adds words to a cloud and displays them on a local web page.
"""

import os
import sys
import asyncio
import json
import threading
import webbrowser
from pathlib import Path
from http.server import HTTPServer, BaseHTTPRequestHandler
from urllib.parse import parse_qs, urlparse
from datetime import datetime

# Add parent directory to path to import mcp_common
sys.path.insert(0, str(Path(__file__).parent.parent))

from mcp.server import Server
import mcp.types as types
from mcp_common import create_text_response, create_error_response, run_mcp_server, safe_get_arg, MCPToolBuilder


# Global state
WORDS_FILE = Path(__file__).parent / "words.json"
SERVER_PORT = 8765
word_cloud_data = {"words": [], "connections": [], "last_update": None}

sse_clients = []

# Category definitions - logical grouping
CATEGORIES = {
    "mcp": {
        "label": "MCP Server",
        "description": "Installerade MCP-servrar",
        "color": "#ff6b6b",
        "keywords": ["mcp", "server", "large-files", "word-cloud"]
    },
    "verktyg": {
        "label": "Verktyg",
        "description": "Programvaruverktyg och applikationer",
        "color": "#667eea",
        "keywords": ["docker", "git", "vscode", "postman", "jenkins", "terraform", "ansible"]
    },
    "språk": {
        "label": "Programmeringsspråk",
        "description": "Programmeringsspråk",
        "color": "#43e97b",
        "keywords": ["python", "javascript", "typescript", "java", "go", "rust", "c++", "c#"]
    },
    "ramverk": {
        "label": "Ramverk",
        "description": "Ramverk och bibliotek",
        "color": "#fa709a",
        "keywords": ["react", "vue", "angular", "django", "flask", "spring", "express", "fastapi"]
    },
    "teknologi": {
        "label": "Teknologi",
        "description": "Plattformar och teknologier",
        "color": "#f093fb",
        "keywords": ["kubernetes", "aws", "azure", "gcp", "cloud", "serverless", "microservices"]
    },
    "koncept": {
        "label": "Koncept",
        "description": "Koncept och metodik",
        "color": "#4facfe",
        "keywords": ["agile", "scrum", "devops", "ci/cd", "tdd", "ddd", "solid", "rest", "graphql"]
    },
    "databas": {
        "label": "Databas",
        "description": "Databaser och datalagring",
        "color": "#30cfd0",
        "keywords": ["postgresql", "mysql", "mongodb", "redis", "elasticsearch", "cassandra"]
    },
    "roll": {
        "label": "Roll",
        "description": "Roller och titlar",
        "color": "#a8edea",
        "keywords": ["developer", "architect", "devops", "engineer", "manager", "lead", "senior"]
    },
    "metod": {
        "label": "Metod",
        "description": "Metoder och processer",
        "color": "#764ba2",
        "keywords": ["agile", "scrum", "kanban", "waterfall", "lean"]
    }
}

def auto_categorize(word: str, description: str = "") -> str:
    """Automatically categorize a word based on keywords."""
    word_lower = word.lower()
    desc_lower = description.lower()

    # Check if description matches a category directly
    if desc_lower in CATEGORIES:
        return desc_lower

    # Check keywords for each category
    for category, info in CATEGORIES.items():
        if word_lower in info["keywords"]:
            return category
        # Check if any keyword is in the word or description
        for keyword in info["keywords"]:
            if keyword in word_lower or keyword in desc_lower:
                return category

    # Default to koncept if no match
    return "koncept"


def get_claude_config_path():
    """Get Claude Desktop config path based on OS."""
    import platform
    system = platform.system()

    if system == "Darwin":  # macOS
        return Path.home() / "Library" / "Application Support" / "Claude" / "claude_desktop_config.json"
    elif system == "Windows":
        appdata = os.getenv("APPDATA")
        if appdata:
            return Path(appdata) / "Claude" / "claude_desktop_config.json"
    return None


def get_installed_mcp_servers():
    """Get list of installed MCP servers from Claude Desktop config."""
    config_path = get_claude_config_path()

    if not config_path or not config_path.exists():
        return []

    try:
        with open(config_path, 'r') as f:
            config = json.load(f)

        servers = config.get("mcpServers", {})
        return list(servers.keys())
    except Exception as e:
        print(f"Error reading Claude config: {e}")
        return []


def load_words():
    """Load words from JSON file."""
    global word_cloud_data
    if WORDS_FILE.exists():
        with open(WORDS_FILE, 'r') as f:
            word_cloud_data = json.load(f)
        # Ensure connections list exists (migration)
        if "connections" not in word_cloud_data:
            word_cloud_data["connections"] = []
    else:
        word_cloud_data = {"words": [], "connections": [], "last_update": None}


def save_words():
    """Save words to JSON file."""
    word_cloud_data["last_update"] = datetime.now().isoformat()
    with open(WORDS_FILE, 'w') as f:
        json.dump(word_cloud_data, f, indent=2)


def notify_clients():
    """Notify all SSE clients about data update."""
    for client in sse_clients[:]:
        try:
            client.notify()
        except:
            sse_clients.remove(client)


class WordCloudHTTPHandler(BaseHTTPRequestHandler):
    """HTTP handler for word cloud web interface."""

    def log_message(self, format, *args):
        """Suppress default logging."""
        pass

    def do_GET(self):
        """Handle GET requests."""
        parsed_path = urlparse(self.path)

        if parsed_path.path == '/':
            self.serve_html()
        elif parsed_path.path == '/api/words':
            self.serve_words_json()
        elif parsed_path.path == '/api/events':
            self.serve_sse()
        else:
            self.send_error(404)

    def do_POST(self):
        """Handle POST requests."""
        parsed_path = urlparse(self.path)

        if parsed_path.path == '/api/connect':
            self.handle_connect()
        elif parsed_path.path == '/api/disconnect':
            self.handle_disconnect()
        else:
            self.send_error(404)

    def handle_connect(self):
        """Handle connection creation via API."""
        try:
            content_length = int(self.headers['Content-Length'])
            post_data = self.rfile.read(content_length)
            data = json.loads(post_data.decode('utf-8'))
            
            source = data.get('source')
            target = data.get('target')

            if not source or not target:
                self.send_error(400, "Missing source or target")
                return

            # Verify words exist (case-insensitive)
            words = {w["word"].lower(): w["word"] for w in word_cloud_data["words"]}
            if source.lower() not in words or target.lower() not in words:
                self.send_error(400, "One or both words not found")
                return
            
            # Use original casing
            real_source = words[source.lower()]
            real_target = words[target.lower()]

            # Check existing
            exists = any(c["source"].lower() == source.lower() and c["target"].lower() == target.lower() 
                        for c in word_cloud_data["connections"])
            
            if not exists:
                word_cloud_data["connections"].append({
                    "source": real_source,
                    "target": real_target,
                    "label": "",
                    "added": datetime.now().isoformat()
                })
                save_words()
                notify_clients()

            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            self.wfile.write(json.dumps({"status": "success"}).encode())

        except Exception as e:
            print(f"Error handling connect: {e}")
            self.send_error(500, str(e))

    def handle_disconnect(self):
        """Handle connection removal via API."""
        try:
            content_length = int(self.headers['Content-Length'])
            post_data = self.rfile.read(content_length)
            data = json.loads(post_data.decode('utf-8'))
            
            source = data.get('source')
            target = data.get('target')

            if not source or not target:
                self.send_error(400, "Missing source or target")
                return

            original_count = len(word_cloud_data["connections"])
            word_cloud_data["connections"] = [
                c for c in word_cloud_data["connections"]
                if not (c["source"].lower() == source.lower() and c["target"].lower() == target.lower())
            ]

            if len(word_cloud_data["connections"]) < original_count:
                save_words()
                notify_clients()

            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            self.wfile.write(json.dumps({"status": "success"}).encode())

        except Exception as e:
            print(f"Error handling disconnect: {e}")
            self.send_error(500, str(e))

    def serve_html(self):
        """Serve the main HTML page."""
        html_file = Path(__file__).parent / "index.html"
        if html_file.exists():
            with open(html_file, 'r') as f:
                content = f.read()
            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            self.wfile.write(content.encode())
        else:
            self.send_error(404, "index.html not found")

    def serve_words_json(self):
        """Serve current words as JSON."""
        self.send_response(200)
        self.send_header('Content-type', 'application/json')
        self.send_header('Access-Control-Allow-Origin', '*')
        self.end_headers()
        self.wfile.write(json.dumps(word_cloud_data).encode())

    def serve_sse(self):
        """Serve Server-Sent Events stream."""
        self.send_response(200)
        self.send_header('Content-type', 'text/event-stream')
        self.send_header('Cache-Control', 'no-cache')
        self.send_header('Access-Control-Allow-Origin', '*')
        self.end_headers()

        # Create client notifier
        client = SSEClient(self.wfile)
        sse_clients.append(client)

        # Send initial data
        client.send_data(word_cloud_data)

        # Keep connection alive
        try:
            while True:
                client.wait_for_notification()
                if client.should_send:
                    client.send_data(word_cloud_data)
                    client.should_send = False
        except:
            if client in sse_clients:
                sse_clients.remove(client)


class SSEClient:
    """Represents an SSE client connection."""

    def __init__(self, wfile):
        self.wfile = wfile
        self.should_send = False
        self.event = threading.Event()

    def notify(self):
        """Notify this client of an update."""
        self.should_send = True
        self.event.set()

    def wait_for_notification(self):
        """Wait for notification with timeout."""
        self.event.wait(timeout=30)  # 30 second timeout
        self.event.clear()

    def send_data(self, data):
        """Send data to client."""
        message = f"data: {json.dumps(data)}\n\n"
        self.wfile.write(message.encode())
        self.wfile.flush()

def run_http_server():
    """Run the HTTP server in a separate thread."""
    load_words()
    httpd = HTTPServer(('localhost', SERVER_PORT), WordCloudHTTPHandler)
    print(f"Word Cloud web server running at http://localhost:{SERVER_PORT}/")
    httpd.serve_forever()


# MCP Server setup
server = Server("word-cloud-manager")


@server.list_tools()
async def handle_list_tools() -> list[types.Tool]:
    """List available tools."""
    return [
        MCPToolBuilder.create_tool(
            name="add_word",
            description="Add a word to the word cloud with optional category/description",
            properties={
                "word": {
                    "type": "string",
                    "description": "The word to add to the cloud"
                },
                "description": {
                    "type": "string",
                    "description": "Description or category of the word (e.g., 'tool', 'concept', 'technology')"
                },
                "size": {
                    "type": "number",
                    "description": "Relative size/importance (1-10, default: 5)",
                    "default": 5
                }
            },
            required=["word"]
        ),
        MCPToolBuilder.create_tool(
            name="remove_word",
            description="Remove a word from the word cloud",
            properties={
                "word": {
                    "type": "string",
                    "description": "The word to remove"
                }
            },
            required=["word"]
        ),
        MCPToolBuilder.create_tool(
            name="add_connection",
            description="Create a directed connection (arrow) between two words",
            properties={
                "source": {
                    "type": "string",
                    "description": "The source word (where the arrow starts)"
                },
                "target": {
                    "type": "string",
                    "description": "The target word (where the arrow ends)"
                },
                "label": {
                    "type": "string",
                    "description": "Optional label for the connection (e.g., 'uses', 'is a')"
                }
            },
            required=["source", "target"]
        ),
        MCPToolBuilder.create_tool(
            name="remove_connection",
            description="Remove a connection between two words",
            properties={
                "source": {
                    "type": "string",
                    "description": "The source word"
                },
                "target": {
                    "type": "string",
                    "description": "The target word"
                }
            },
            required=["source", "target"]
        ),
        MCPToolBuilder.create_tool(
            name="clear_cloud",
            description="Clear all words and connections from the cloud",
            properties={
                "confirm": {
                    "type": "boolean",
                    "description": "Must be true to confirm clearing",
                    "default": False
                }
            },
            required=["confirm"]
        ),
        MCPToolBuilder.create_tool(
            name="list_words",
            description="List all words currently in the cloud",
            properties={},
            required=[]
        ),
        MCPToolBuilder.create_tool(
            name="open_browser",
            description="Open the word cloud visualization in your default web browser automatically",
            properties={},
            required=[]
        ),
        MCPToolBuilder.create_tool(
            name="list_categories",
            description="List all available categories and their descriptions",
            properties={},
            required=[]
        ),
        MCPToolBuilder.create_tool(
            name="list_by_category",
            description="List words grouped by their categories in a structured format",
            properties={},
            required=[]
        ),
        MCPToolBuilder.create_tool(
            name="add_mcp_servers",
            description="Automatically add all installed MCP servers from Claude Desktop config to the word cloud",
            properties={
                "size": {
                    "type": "number",
                    "description": "Size for all MCP server words (1-10, default: 7)",
                    "default": 7
                }
            },
            required=[]
        ),
    ]


@server.call_tool()
async def handle_call_tool(
    name: str, arguments: dict | None
) -> list[types.TextContent | types.ImageContent | types.EmbeddedResource]:
    """Handle tool execution requests."""

    if name == "add_word":
        word = safe_get_arg(arguments, "word")
        description = safe_get_arg(arguments, "description", "")
        size = safe_get_arg(arguments, "size", 5)

        if not word:
            return create_error_response("word is required")

        # Auto-categorize the word
        category = auto_categorize(word, description)
        category_label = CATEGORIES[category]["label"]

        # Check if word already exists
        existing = next((w for w in word_cloud_data["words"] if w["word"].lower() == word.lower()), None)

        if existing:
            existing["description"] = description
            existing["category"] = category
            existing["size"] = max(1, min(10, int(size)))
            existing["updated"] = datetime.now().isoformat()
            action = "Updated"
        else:
            word_cloud_data["words"].append({
                "word": word,
                "description": description,
                "category": category,
                "size": max(1, min(10, int(size))),
                "added": datetime.now().isoformat()
            })
            action = "Added"

        save_words()
        notify_clients()

        return create_text_response(
            f"{action} word: '{word}' (size: {size})\n"
            f"Category: {category_label}\n"
            f"Description: {description}\n"
            f"Total words: {len(word_cloud_data['words'])}\n"
            f"View at: http://localhost:{SERVER_PORT}/"
        )

    elif name == "remove_word":
        word = safe_get_arg(arguments, "word")

        if not word:
            return create_error_response("word is required")

        # Remove word
        original_count = len(word_cloud_data["words"])
        word_cloud_data["words"] = [
            w for w in word_cloud_data["words"]
            if w["word"].lower() != word.lower()
        ]

        if len(word_cloud_data["words"]) < original_count:
            # Also remove associated connections
            original_conn_count = len(word_cloud_data["connections"])
            word_cloud_data["connections"] = [
                c for c in word_cloud_data["connections"]
                if c["source"].lower() != word.lower() and c["target"].lower() != word.lower()
            ]
            conn_removed = original_conn_count - len(word_cloud_data["connections"])

            save_words()
            notify_clients()
            msg = f"Removed word: '{word}'\nRemaining words: {len(word_cloud_data['words'])}"
            if conn_removed > 0:
                msg += f"\nRemoved {conn_removed} associated connection(s)."
            return create_text_response(msg)
        else:
            return create_error_response(f"Word '{word}' not found in cloud")

    elif name == "add_connection":
        source = safe_get_arg(arguments, "source")
        target = safe_get_arg(arguments, "target")
        label = safe_get_arg(arguments, "label", "")

        if not source or not target:
            return create_error_response("Source and target words are required")

        # Verify both words exist
        words = [w["word"].lower() for w in word_cloud_data["words"]]
        if source.lower() not in words:
            return create_error_response(f"Source word '{source}' not found. Add it first.")
        if target.lower() not in words:
            return create_error_response(f"Target word '{target}' not found. Add it first.")

        # Check for existing connection
        existing = next((c for c in word_cloud_data["connections"] 
                        if c["source"].lower() == source.lower() and c["target"].lower() == target.lower()), None)
        
        if existing:
            existing["label"] = label
            action = "Updated"
        else:
            word_cloud_data["connections"].append({
                "source": source,
                "target": target,
                "label": label,
                "added": datetime.now().isoformat()
            })
            action = "Added"

        save_words()
        notify_clients()
        return create_text_response(f"{action} connection: {source} -> {target} ({label})")

    elif name == "remove_connection":
        source = safe_get_arg(arguments, "source")
        target = safe_get_arg(arguments, "target")

        if not source or not target:
            return create_error_response("Source and target words are required")

        original_count = len(word_cloud_data["connections"])
        word_cloud_data["connections"] = [
            c for c in word_cloud_data["connections"]
            if not (c["source"].lower() == source.lower() and c["target"].lower() == target.lower())
        ]

        if len(word_cloud_data["connections"]) < original_count:
            save_words()
            notify_clients()
            return create_text_response(f"Removed connection: {source} -> {target}")
        else:
            return create_error_response("Connection not found")

    elif name == "clear_cloud":
        confirm = safe_get_arg(arguments, "confirm", False)

        if not confirm:
            return create_error_response("confirm must be true to clear all words")

        count = len(word_cloud_data["words"])
        conn_count = len(word_cloud_data["connections"])
        word_cloud_data["words"] = []
        word_cloud_data["connections"] = []
        save_words()
        notify_clients()

        return create_text_response(f"Cleared {count} words and {conn_count} connections from the cloud")

    elif name == "list_words":
        if not word_cloud_data["words"]:
            return create_text_response("No words in the cloud yet.")

        result = f"Word Cloud ({len(word_cloud_data['words'])} words):\n\n"
        for w in sorted(word_cloud_data["words"], key=lambda x: x.get("size", 5), reverse=True):
            result += f"• {w['word']} (size: {w.get('size', 5)})"
            if w.get('description'):
                result += f" - {w['description']}"
            result += "\n"

        if word_cloud_data["connections"]:
            result += f"\nConnections ({len(word_cloud_data['connections'])}):\n"
            for c in word_cloud_data["connections"]:
                label = f" [{c['label']}]" if c.get("label") else ""
                result += f"• {c['source']} -> {c['target']}{label}\n"

        result += f"\nView at: http://localhost:{SERVER_PORT}/"
        return create_text_response(result)

    elif name == "open_browser":
        url = f"http://localhost:{SERVER_PORT}/"
        try:
            webbrowser.open(url)
            return create_text_response(
                f"✓ Opened word cloud in your default browser!\n\n"
                f"URL: {url}\n\n"
                f"The word cloud will update automatically when you add new words.\n"
                f"Current words: {len(word_cloud_data['words'])}"
            )
        except Exception as e:
            return create_error_response(
                f"Failed to open browser: {str(e)}\n"
                f"Please open manually: {url}"
            )

    elif name == "list_categories":
        result = "Tillgängliga kategorier:\n\n"
        for cat_key, cat_info in CATEGORIES.items():
            result += f"• {cat_info['label']} ({cat_key})\n"
            result += f"  {cat_info['description']}\n"
            result += f"  Exempel: {', '.join(cat_info['keywords'][:5])}\n\n"

        result += f"\nAnvändning: Lägg till ett ord med 'description' som kategori-namn,\n"
        result += f"eller låt systemet automatiskt kategorisera baserat på nyckelord."

        return create_text_response(result)

    elif name == "list_by_category":
        if not word_cloud_data["words"]:
            return create_text_response("Inga ord i molnet än.")

        # Group words by category
        grouped = {}
        for word_data in word_cloud_data["words"]:
            category = word_data.get("category", "koncept")
            if category not in grouped:
                grouped[category] = []
            grouped[category].append(word_data)

        # Build result
        result = f"Ord grupperade efter kategori ({len(word_cloud_data['words'])} totalt):\n\n"

        for cat_key in CATEGORIES.keys():
            if cat_key in grouped:
                cat_info = CATEGORIES[cat_key]
                words = grouped[cat_key]
                result += f"📁 {cat_info['label']} ({len(words)} ord)\n"
                result += "─" * 50 + "\n"

                # Sort by size
                for word_data in sorted(words, key=lambda x: x.get("size", 5), reverse=True):
                    result += f"  • {word_data['word']}"
                    if word_data.get("description"):
                        result += f" - {word_data['description']}"
                    result += f" (size: {word_data.get('size', 5)})\n"
                result += "\n"

        result += f"View at: http://localhost:{SERVER_PORT}/"
        return create_text_response(result)

    elif name == "add_mcp_servers":
        size = safe_get_arg(arguments, "size", 7)
        size = max(1, min(10, int(size)))

        # Get installed MCP servers
        servers = get_installed_mcp_servers()

        if not servers:
            return create_error_response(
                "Kunde inte hitta några MCP-servrar i Claude Desktop config.\n"
                "Kontrollera att Claude Desktop är konfigurerat korrekt."
            )

        # Add each server to the word cloud
        added = []
        updated = []

        for server_name in servers:
            # Check if word already exists
            existing = next((w for w in word_cloud_data["words"] if w["word"].lower() == server_name.lower()), None)

            if existing:
                existing["category"] = "mcp"
                existing["description"] = "MCP Server"
                existing["size"] = size
                existing["updated"] = datetime.now().isoformat()
                updated.append(server_name)
            else:
                word_cloud_data["words"].append({
                    "word": server_name,
                    "description": "MCP Server",
                    "category": "mcp",
                    "size": size,
                    "added": datetime.now().isoformat()
                })
                added.append(server_name)

        save_words()
        notify_clients()

        result = f"✓ Lade till MCP-servrar i ordmolnet!\n\n"
        if added:
            result += f"Nya servrar ({len(added)}):\n"
            for name in added:
                result += f"  • {name}\n"
        if updated:
            result += f"\nUppdaterade servrar ({len(updated)}):\n"
            for name in updated:
                result += f"  • {name}\n"

        result += f"\nTotalt ord i molnet: {len(word_cloud_data['words'])}\n"
        result += f"View at: http://localhost:{SERVER_PORT}/"

        return create_text_response(result)

    else:
        raise ValueError(f"Unknown tool: {name}")


async def main():
    """Main entry point for the MCP server."""
    # Start HTTP server in background thread
    http_thread = threading.Thread(target=run_http_server, daemon=True)
    http_thread.start()

    # Run MCP server
    await run_mcp_server(server, "word-cloud-manager", "0.1.0")


if __name__ == "__main__":
    asyncio.run(main())