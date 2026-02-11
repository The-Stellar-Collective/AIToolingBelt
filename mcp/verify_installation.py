#!/usr/bin/env python3
"""
Verify MCP installation and configuration.
Run this script to check if everything is set up correctly.
"""

import sys
import os
from pathlib import Path
import json

# Colors for terminal output
class Colors:
    GREEN = '\033[92m'
    RED = '\033[91m'
    YELLOW = '\033[93m'
    BLUE = '\033[94m'
    RESET = '\033[0m'
    BOLD = '\033[1m'

def print_header(text):
    """Print a header."""
    print(f"\n{Colors.BLUE}{Colors.BOLD}{'='*60}{Colors.RESET}")
    print(f"{Colors.BLUE}{Colors.BOLD}{text}{Colors.RESET}")
    print(f"{Colors.BLUE}{Colors.BOLD}{'='*60}{Colors.RESET}\n")

def print_success(text):
    """Print success message."""
    print(f"{Colors.GREEN}✓{Colors.RESET} {text}")

def print_error(text):
    """Print error message."""
    print(f"{Colors.RED}✗{Colors.RESET} {text}")

def print_warning(text):
    """Print warning message."""
    print(f"{Colors.YELLOW}⚠{Colors.RESET} {text}")

def check_python_version():
    """Check Python version."""
    print_header("Checking Python Version")
    version = sys.version_info
    version_str = f"{version.major}.{version.minor}.{version.micro}"

    if version.major >= 3 and version.minor >= 10:
        print_success(f"Python {version_str} (OK)")
        return True
    else:
        print_error(f"Python {version_str} (Need 3.10 or later)")
        return False

def check_mcp_package():
    """Check if MCP package is installed."""
    print_header("Checking MCP Package")
    try:
        import mcp
        print_success("MCP package is installed")
        if hasattr(mcp, '__version__'):
            print(f"  Version: {mcp.__version__}")
        return True
    except ImportError:
        print_error("MCP package not found")
        print("  Install with: pip3 install mcp")
        return False

def check_mcp_common():
    """Check if mcp_common.py exists and is importable."""
    print_header("Checking mcp_common.py")

    script_dir = Path(__file__).parent
    mcp_common_path = script_dir / "mcp_common.py"

    if not mcp_common_path.exists():
        print_error(f"mcp_common.py not found at {mcp_common_path}")
        return False

    print_success(f"mcp_common.py found at {mcp_common_path}")

    # Try to import
    try:
        sys.path.insert(0, str(script_dir))
        from mcp_common import create_text_response, MCPToolBuilder, run_mcp_server
        print_success("Successfully imported mcp_common utilities")
        return True
    except Exception as e:
        print_error(f"Failed to import mcp_common: {e}")
        return False

def check_server_files():
    """Check if server files exist."""
    print_header("Checking MCP Server Files")

    script_dir = Path(__file__).parent
    servers = {
        "Large Files Manager": script_dir / "large-files-manager" / "large_files_mcp_server.py",
        "Word Cloud Manager": script_dir / "word-cloud" / "word_cloud_server.py"
    }

    all_ok = True
    for name, path in servers.items():
        if path.exists():
            is_executable = os.access(path, os.X_OK)
            if is_executable:
                print_success(f"{name}: {path} (executable)")
            else:
                print_warning(f"{name}: {path} (not executable - run: chmod +x {path})")
        else:
            print_error(f"{name}: {path} (NOT FOUND)")
            all_ok = False

    return all_ok

def check_claude_config():
    """Check Claude Desktop configuration."""
    print_header("Checking Claude Desktop Configuration")

    # Determine config path based on OS
    if sys.platform == "darwin":  # macOS
        config_path = Path.home() / "Library" / "Application Support" / "Claude" / "claude_desktop_config.json"
    elif sys.platform == "win32":  # Windows
        config_path = Path(os.getenv("APPDATA")) / "Claude" / "claude_desktop_config.json"
    else:
        print_warning(f"Unknown platform: {sys.platform}")
        return False

    if not config_path.exists():
        print_error(f"Config file not found: {config_path}")
        print("  Create it with the configuration from SETUP.md")
        return False

    print_success(f"Config file found: {config_path}")

    # Try to parse JSON
    try:
        with open(config_path, 'r') as f:
            config = json.load(f)

        print_success("Config file is valid JSON")

        # Check for MCP servers
        if "mcpServers" in config:
            servers = config["mcpServers"]
            print(f"  Found {len(servers)} MCP server(s) configured:")
            for server_name in servers:
                print(f"    - {server_name}")

            # Check for our servers
            our_servers = ["large-files-manager", "word-cloud"]
            for server in our_servers:
                if server in servers:
                    print_success(f"  {server} is configured")
                else:
                    print_warning(f"  {server} is NOT configured")
        else:
            print_warning("No mcpServers section found in config")
            return False

        return True

    except json.JSONDecodeError as e:
        print_error(f"Config file has invalid JSON: {e}")
        return False
    except Exception as e:
        print_error(f"Error reading config: {e}")
        return False

def check_requirements():
    """Check if all requirements are installed."""
    print_header("Checking Additional Requirements")

    required_packages = [
        "pydantic",
        "httpx",
        "starlette",
        "uvicorn"
    ]

    all_ok = True
    for package in required_packages:
        try:
            __import__(package)
            print_success(f"{package} is installed")
        except ImportError:
            print_warning(f"{package} is not installed (will be installed with MCP)")
            all_ok = False

    return all_ok

def print_summary(results):
    """Print summary of checks."""
    print_header("Summary")

    all_passed = all(results.values())

    for check, passed in results.items():
        if passed:
            print_success(check)
        else:
            print_error(check)

    print()
    if all_passed:
        print(f"{Colors.GREEN}{Colors.BOLD}🎉 All checks passed! Your MCP setup is ready.{Colors.RESET}")
        print(f"\n{Colors.BOLD}Next steps:{Colors.RESET}")
        print("1. Restart Claude Desktop")
        print("2. Test large-files-manager: 'Hitta de 10 största filerna i min hemkatalog'")
        print("3. Test word-cloud: 'Lägg till ordet Test'")
        print("4. Open word cloud: http://localhost:8765/")
    else:
        print(f"{Colors.RED}{Colors.BOLD}❌ Some checks failed. Please fix the issues above.{Colors.RESET}")
        print(f"\n{Colors.BOLD}Help:{Colors.RESET}")
        print("- See SETUP.md for installation instructions")
        print("- See PYTHON_INSTALL.md for Python setup")
        print("- Run: pip3 install -r large-files-manager/requirements_large_files.txt")

def main():
    """Main verification function."""
    print(f"{Colors.BOLD}{Colors.BLUE}")
    print("""
    ███╗   ███╗ ██████╗██████╗     ██╗   ██╗███████╗██████╗ ██╗███████╗██╗   ██╗
    ████╗ ████║██╔════╝██╔══██╗    ██║   ██║██╔════╝██╔══██╗██║██╔════╝╚██╗ ██╔╝
    ██╔████╔██║██║     ██████╔╝    ██║   ██║█████╗  ██████╔╝██║█████╗   ╚████╔╝
    ██║╚██╔╝██║██║     ██╔═══╝     ╚██╗ ██╔╝██╔══╝  ██╔══██╗██║██╔══╝    ╚██╔╝
    ██║ ╚═╝ ██║╚██████╗██║          ╚████╔╝ ███████╗██║  ██║██║██║        ██║
    ╚═╝     ╚═╝ ╚═════╝╚═╝           ╚═══╝  ╚══════╝╚═╝  ╚═╝╚═╝╚═╝        ╚═╝
    """)
    print(f"{Colors.RESET}")
    print(f"{Colors.BOLD}MCP Installation Verification Tool{Colors.RESET}\n")

    results = {
        "Python Version": check_python_version(),
        "MCP Package": check_mcp_package(),
        "mcp_common.py": check_mcp_common(),
        "Server Files": check_server_files(),
        "Claude Config": check_claude_config(),
        "Requirements": check_requirements()
    }

    print_summary(results)

if __name__ == "__main__":
    main()
