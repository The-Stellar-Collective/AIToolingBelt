#!/usr/bin/env python3
"""
GitHub MCP Server - Python implementation
Provides GitHub repository and issue management tools via MCP protocol.
"""

import json
import sys
import os
import logging
from typing import Any
import requests

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    stream=sys.stderr
)
logger = logging.getLogger(__name__)

GITHUB_TOKEN = os.getenv('GITHUB_PERSONAL_ACCESS_TOKEN', '')
GITHUB_API_BASE = 'https://api.github.com'


class GitHubMCPServer:
    def __init__(self):
        self.headers = {
            'Authorization': f'Bearer {GITHUB_TOKEN}',
            'Accept': 'application/vnd.github+json',
            'X-GitHub-Api-Version': '2022-11-28'
        }

    def _make_request(self, method: str, endpoint: str, data: dict = None) -> dict:
        """Make a request to GitHub API"""
        url = f"{GITHUB_API_BASE}/{endpoint.lstrip('/')}"

        try:
            if method.upper() == 'GET':
                response = requests.get(url, headers=self.headers, params=data)
            elif method.upper() == 'POST':
                response = requests.post(url, headers=self.headers, json=data)
            elif method.upper() == 'PATCH':
                response = requests.patch(url, headers=self.headers, json=data)
            else:
                return {'error': f'Unsupported method: {method}'}

            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            logger.error(f"GitHub API error: {e}")
            return {'error': str(e)}

    def list_repos(self, args: dict) -> dict:
        """List repositories for authenticated user"""
        per_page = args.get('per_page', 30)
        sort = args.get('sort', 'updated')

        repos = self._make_request('GET', '/user/repos', {'per_page': per_page, 'sort': sort})

        if isinstance(repos, list):
            return {
                'repositories': [
                    {
                        'name': repo['name'],
                        'full_name': repo['full_name'],
                        'description': repo.get('description', ''),
                        'url': repo['html_url'],
                        'private': repo['private'],
                        'stars': repo['stargazers_count']
                    }
                    for repo in repos
                ]
            }
        return repos

    def get_repo(self, args: dict) -> dict:
        """Get repository details"""
        owner = args.get('owner')
        repo = args.get('repo')

        if not owner or not repo:
            return {'error': 'owner and repo are required'}

        return self._make_request('GET', f'/repos/{owner}/{repo}')

    def list_issues(self, args: dict) -> dict:
        """List issues for a repository"""
        owner = args.get('owner')
        repo = args.get('repo')
        state = args.get('state', 'open')

        if not owner or not repo:
            return {'error': 'owner and repo are required'}

        issues = self._make_request('GET', f'/repos/{owner}/{repo}/issues', {'state': state})

        if isinstance(issues, list):
            return {
                'issues': [
                    {
                        'number': issue['number'],
                        'title': issue['title'],
                        'state': issue['state'],
                        'url': issue['html_url'],
                        'created_at': issue['created_at'],
                        'user': issue['user']['login']
                    }
                    for issue in issues
                ]
            }
        return issues

    def create_issue(self, args: dict) -> dict:
        """Create a new issue"""
        owner = args.get('owner')
        repo = args.get('repo')
        title = args.get('title')
        body = args.get('body', '')

        if not all([owner, repo, title]):
            return {'error': 'owner, repo, and title are required'}

        return self._make_request('POST', f'/repos/{owner}/{repo}/issues', {
            'title': title,
            'body': body
        })

    def get_file_contents(self, args: dict) -> dict:
        """Get contents of a file from a repository"""
        owner = args.get('owner')
        repo = args.get('repo')
        path = args.get('path')
        ref = args.get('ref', 'main')

        if not all([owner, repo, path]):
            return {'error': 'owner, repo, and path are required'}

        return self._make_request('GET', f'/repos/{owner}/{repo}/contents/{path}', {'ref': ref})

    def handle_tool_call(self, tool_name: str, arguments: dict) -> dict:
        """Route tool calls to appropriate handler"""
        handlers = {
            'list_repos': self.list_repos,
            'get_repo': self.get_repo,
            'list_issues': self.list_issues,
            'create_issue': self.create_issue,
            'get_file_contents': self.get_file_contents
        }

        handler = handlers.get(tool_name)
        if not handler:
            return {'error': f'Unknown tool: {tool_name}'}

        return handler(arguments)


def send_message(message: dict):
    """Send a JSON-RPC message to stdout"""
    json_str = json.dumps(message)
    sys.stdout.write(json_str + '\n')
    sys.stdout.flush()
    logger.debug(f"Sent: {json_str}")


def main():
    logger.info("Starting GitHub MCP Server (Python)")

    if not GITHUB_TOKEN:
        logger.error("GITHUB_PERSONAL_ACCESS_TOKEN environment variable not set")
        sys.exit(1)

    server = GitHubMCPServer()

    # Send server info
    send_message({
        "jsonrpc": "2.0",
        "id": 0,
        "result": {
            "protocolVersion": "2025-06-18",
            "capabilities": {
                "experimental": {},
                "tools": {"listChanged": False}
            },
            "serverInfo": {
                "name": "github-mcp-python",
                "version": "0.1.0"
            }
        }
    })

    logger.info("Server initialized, waiting for requests...")

    # Process requests from stdin
    for line in sys.stdin:
        line = line.strip()
        if not line:
            continue

        try:
            request = json.loads(line)
            logger.debug(f"Received: {request}")

            method = request.get('method')
            request_id = request.get('id')
            params = request.get('params', {})

            if method == 'initialize':
                send_message({
                    "jsonrpc": "2.0",
                    "id": request_id,
                    "result": {
                        "protocolVersion": "2025-06-18",
                        "capabilities": {
                            "experimental": {},
                            "tools": {"listChanged": False}
                        },
                        "serverInfo": {
                            "name": "github-mcp-python",
                            "version": "0.1.0"
                        }
                    }
                })

            elif method == 'tools/list':
                send_message({
                    "jsonrpc": "2.0",
                    "id": request_id,
                    "result": {
                        "tools": [
                            {
                                "name": "list_repos",
                                "description": "List repositories for the authenticated user",
                                "inputSchema": {
                                    "type": "object",
                                    "properties": {
                                        "per_page": {
                                            "type": "number",
                                            "description": "Number of repositories to return (max 100)",
                                            "default": 30
                                        },
                                        "sort": {
                                            "type": "string",
                                            "description": "Sort by: created, updated, pushed, full_name",
                                            "default": "updated"
                                        }
                                    },
                                    "required": []
                                }
                            },
                            {
                                "name": "get_repo",
                                "description": "Get details about a specific repository",
                                "inputSchema": {
                                    "type": "object",
                                    "properties": {
                                        "owner": {"type": "string", "description": "Repository owner"},
                                        "repo": {"type": "string", "description": "Repository name"}
                                    },
                                    "required": ["owner", "repo"]
                                }
                            },
                            {
                                "name": "list_issues",
                                "description": "List issues for a repository",
                                "inputSchema": {
                                    "type": "object",
                                    "properties": {
                                        "owner": {"type": "string", "description": "Repository owner"},
                                        "repo": {"type": "string", "description": "Repository name"},
                                        "state": {
                                            "type": "string",
                                            "description": "Filter by state: open, closed, all",
                                            "default": "open"
                                        }
                                    },
                                    "required": ["owner", "repo"]
                                }
                            },
                            {
                                "name": "create_issue",
                                "description": "Create a new issue in a repository",
                                "inputSchema": {
                                    "type": "object",
                                    "properties": {
                                        "owner": {"type": "string", "description": "Repository owner"},
                                        "repo": {"type": "string", "description": "Repository name"},
                                        "title": {"type": "string", "description": "Issue title"},
                                        "body": {"type": "string", "description": "Issue body/description"}
                                    },
                                    "required": ["owner", "repo", "title"]
                                }
                            },
                            {
                                "name": "get_file_contents",
                                "description": "Get contents of a file from a repository",
                                "inputSchema": {
                                    "type": "object",
                                    "properties": {
                                        "owner": {"type": "string", "description": "Repository owner"},
                                        "repo": {"type": "string", "description": "Repository name"},
                                        "path": {"type": "string", "description": "File path in repository"},
                                        "ref": {
                                            "type": "string",
                                            "description": "Branch, tag, or commit SHA",
                                            "default": "main"
                                        }
                                    },
                                    "required": ["owner", "repo", "path"]
                                }
                            }
                        ]
                    }
                })

            elif method == 'tools/call':
                tool_name = params.get('name')
                arguments = params.get('arguments', {})

                result = server.handle_tool_call(tool_name, arguments)

                send_message({
                    "jsonrpc": "2.0",
                    "id": request_id,
                    "result": {
                        "content": [
                            {
                                "type": "text",
                                "text": json.dumps(result, indent=2)
                            }
                        ]
                    }
                })

            elif method == 'notifications/initialized':
                # Acknowledge initialization
                pass

            else:
                logger.warning(f"Unknown method: {method}")

        except json.JSONDecodeError as e:
            logger.error(f"Invalid JSON: {e}")
        except Exception as e:
            logger.error(f"Error processing request: {e}", exc_info=True)


if __name__ == '__main__':
    main()
