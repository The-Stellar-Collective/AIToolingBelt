#!/usr/bin/env python3
"""
Automatic MCP installation script.
Detects OS and installs everything needed.

Usage: python3 install.py
"""

import sys
import os
import platform
import subprocess
import json
from pathlib import Path

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

def print_info(text):
    """Print info message."""
    print(f"{Colors.BLUE}ℹ{Colors.RESET} {text}")

def run_command(cmd, shell=False, check=True):
    """Run a command and return result."""
    try:
        result = subprocess.run(
            cmd if isinstance(cmd, list) else cmd,
            shell=shell,
            capture_output=True,
            text=True,
            check=check
        )
        return result.returncode == 0, result.stdout, result.stderr
    except subprocess.CalledProcessError as e:
        return False, e.stdout, e.stderr
    except Exception as e:
        return False, "", str(e)

def detect_os():
    """Detect operating system."""
    system = platform.system()
    if system == "Darwin":
        return "macos"
    elif system == "Windows":
        return "windows"
    elif system == "Linux":
        return "linux"
    else:
        return "unknown"

def check_python():
    """Check Python version."""
    print_header("Checking Python Installation")

    version = sys.version_info
    version_str = f"{version.major}.{version.minor}.{version.micro}"

    if version.major >= 3 and version.minor >= 10:
        print_success(f"Python {version_str} is installed (OK)")
        return True
    else:
        print_error(f"Python {version_str} is too old (need 3.10+)")
        return False

def install_python(os_type):
    """Provide instructions to install Python."""
    print_header("Python Installation Required")

    if os_type == "macos":
        print_info("To install Python on macOS, run:")
        print("  brew install python3")
        print("\nOr download from: https://www.python.org/downloads/macos/")
    elif os_type == "windows":
        print_info("To install Python on Windows:")
        print("  1. Open Microsoft Store")
        print("  2. Search for 'Python 3.11'")
        print("  3. Click 'Install'")
        print("\nOr download from: https://www.python.org/downloads/windows/")
        print("\nOr use winget: winget install Python.Python.3.11")
    else:
        print_info("Please install Python 3.10 or later for your OS")

    return False

def check_pip():
    """Check if pip is installed."""
    print_header("Checking pip Installation")

    # Try different pip commands
    for pip_cmd in ["pip3", "pip", f"{sys.executable} -m pip"]:
        success, stdout, _ = run_command(f"{pip_cmd} --version", shell=True, check=False)
        if success:
            print_success(f"pip is installed: {stdout.strip()}")
            return True, pip_cmd

    print_error("pip not found")
    return False, None

def install_pip():
    """Install pip."""
    print_header("Installing pip")

    print_info("Installing pip...")
    success, stdout, stderr = run_command([sys.executable, "-m", "ensurepip", "--upgrade"])

    if success:
        print_success("pip installed successfully")
        return True
    else:
        print_error(f"Failed to install pip: {stderr}")
        return False

def install_mcp_dependencies(pip_cmd):
    """Install MCP and dependencies."""
    print_header("Installing MCP Dependencies")

    script_dir = Path(__file__).parent
    requirements_file = script_dir / "large-files-manager" / "requirements_large_files.txt"

    if requirements_file.exists():
        print_info(f"Installing from {requirements_file}...")
        success, stdout, stderr = run_command(
            f"{pip_cmd} install -r {requirements_file}",
            shell=True,
            check=False
        )

        if success:
            print_success("MCP dependencies installed successfully")
            return True
        else:
            print_warning(f"Requirements file installation had issues: {stderr}")
            # Try direct installation
            print_info("Trying direct MCP installation...")

    # Direct installation as fallback
    print_info("Installing mcp package...")
    success, stdout, stderr = run_command(
        f"{pip_cmd} install mcp>=1.0.0",
        shell=True,
        check=False
    )

    if success:
        print_success("MCP package installed successfully")
        return True
    else:
        print_error(f"Failed to install MCP: {stderr}")
        return False

def make_executable(file_path):
    """Make file executable (Unix-like systems)."""
    try:
        os.chmod(file_path, 0o755)
        return True
    except Exception as e:
        print_warning(f"Could not make {file_path} executable: {e}")
        return False

def setup_server_files():
    """Setup server files."""
    print_header("Setting Up Server Files")

    script_dir = Path(__file__).parent
    servers = [
        script_dir / "large-files-manager" / "large_files_mcp_server.py",
        script_dir / "word-cloud" / "word_cloud_server.py"
    ]

    all_ok = True
    for server_file in servers:
        if server_file.exists():
            if platform.system() != "Windows":
                if make_executable(server_file):
                    print_success(f"Made executable: {server_file.name}")
                else:
                    all_ok = False
            else:
                print_success(f"Found: {server_file.name}")
        else:
            print_error(f"Server file not found: {server_file}")
            all_ok = False

    return all_ok

def get_claude_config_path(os_type):
    """Get Claude Desktop config path based on OS."""
    if os_type == "macos":
        return Path.home() / "Library" / "Application Support" / "Claude" / "claude_desktop_config.json"
    elif os_type == "windows":
        appdata = os.getenv("APPDATA")
        if appdata:
            return Path(appdata) / "Claude" / "claude_desktop_config.json"
    return None

def configure_claude_desktop(os_type):
    """Configure Claude Desktop."""
    print_header("Configuring Claude Desktop")

    config_path = get_claude_config_path(os_type)

    if not config_path:
        print_error(f"Could not determine Claude Desktop config path for {os_type}")
        return False

    print_info(f"Config file: {config_path}")

    # Create directory if it doesn't exist
    config_path.parent.mkdir(parents=True, exist_ok=True)

    # Get absolute paths to servers
    script_dir = Path(__file__).parent.absolute()
    large_files_server = script_dir / "large-files-manager" / "large_files_mcp_server.py"
    word_cloud_server = script_dir / "word-cloud" / "word_cloud_server.py"

    # Determine Python command
    if os_type == "windows":
        python_cmd = "python"
    else:
        python_cmd = "python3"

    # Read existing config or create new
    if config_path.exists():
        try:
            with open(config_path, 'r') as f:
                config = json.load(f)
            print_info("Found existing config, updating...")
        except:
            print_warning("Existing config is invalid, creating new one...")
            config = {}
    else:
        print_info("Creating new config file...")
        config = {}

    # Ensure mcpServers section exists
    if "mcpServers" not in config:
        config["mcpServers"] = {}

    # Add our servers
    config["mcpServers"]["large-files-manager"] = {
        "command": python_cmd,
        "args": [str(large_files_server)]
    }

    config["mcpServers"]["word-cloud"] = {
        "command": python_cmd,
        "args": [str(word_cloud_server)]
    }

    # Write config
    try:
        with open(config_path, 'w') as f:
            json.dump(config, f, indent=2)
        print_success("Claude Desktop configured successfully")
        print_info(f"Configured servers: large-files-manager, word-cloud")
        return True
    except Exception as e:
        print_error(f"Failed to write config: {e}")
        return False

def run_verification():
    """Run verification script."""
    print_header("Running Verification")

    verify_script = Path(__file__).parent / "verify_installation.py"

    if not verify_script.exists():
        print_warning("Verification script not found")
        return False

    print_info("Running verification script...")
    success, stdout, stderr = run_command([sys.executable, str(verify_script)])

    if success:
        print(stdout)
        return True
    else:
        print_error("Verification failed")
        print(stderr)
        return False

def main():
    """Main installation function."""
    print(f"{Colors.BOLD}{Colors.BLUE}")
    print("""
    ███╗   ███╗ ██████╗██████╗     ██╗███╗   ██╗███████╗████████╗ █████╗ ██╗     ██╗
    ████╗ ████║██╔════╝██╔══██╗    ██║████╗  ██║██╔════╝╚══██╔══╝██╔══██╗██║     ██║
    ██╔████╔██║██║     ██████╔╝    ██║██╔██╗ ██║███████╗   ██║   ███████║██║     ██║
    ██║╚██╔╝██║██║     ██╔═══╝     ██║██║╚██╗██║╚════██║   ██║   ██╔══██║██║     ██║
    ██║ ╚═╝ ██║╚██████╗██║         ██║██║ ╚████║███████║   ██║   ██║  ██║███████╗███████╗
    ╚═╝     ╚═╝ ╚═════╝╚═╝         ╚═╝╚═╝  ╚═══╝╚══════╝   ╚═╝   ╚═╝  ╚═╝╚══════╝╚══════╝
    """)
    print(f"{Colors.RESET}")
    print(f"{Colors.BOLD}MCP Automatic Installation{Colors.RESET}\n")

    # Detect OS
    os_type = detect_os()
    print_info(f"Detected OS: {os_type}")

    if os_type == "unknown":
        print_error("Unsupported operating system")
        return False

    # Check Python
    if not check_python():
        install_python(os_type)
        print_error("\nPlease install Python and run this script again")
        return False

    # Check pip
    pip_exists, pip_cmd = check_pip()
    if not pip_exists:
        if not install_pip():
            print_error("\nFailed to install pip. Please install it manually.")
            return False
        # Recheck
        pip_exists, pip_cmd = check_pip()
        if not pip_exists:
            print_error("\nPip still not available after installation")
            return False

    # Install MCP dependencies
    if not install_mcp_dependencies(pip_cmd):
        print_error("\nFailed to install MCP dependencies")
        return False

    # Setup server files
    if not setup_server_files():
        print_warning("\nSome server files had issues, but continuing...")

    # Configure Claude Desktop
    if not configure_claude_desktop(os_type):
        print_error("\nFailed to configure Claude Desktop")
        return False

    # Run verification
    print("\n")
    run_verification()

    # Final instructions
    print_header("Installation Complete!")

    print(f"{Colors.GREEN}{Colors.BOLD}✓ MCP installation successful!{Colors.RESET}\n")

    print(f"{Colors.BOLD}Next steps:{Colors.RESET}")
    print("1. Restart Claude Desktop")
    print("   macOS: Quit and reopen Claude Desktop")
    print("   Windows: Close and reopen Claude Desktop")
    print()
    print("2. Test the servers in Claude:")
    print("   • Large Files: 'Hitta de 10 största filerna i min hemkatalog'")
    print("   • Word Cloud: 'Lägg till ordet Test med beskrivning demo'")
    print()
    print("3. Open Word Cloud in browser:")
    print("   http://localhost:8765/")
    print()
    print(f"{Colors.BOLD}Documentation:{Colors.RESET}")
    print("  • SETUP.md - Setup guide")
    print("  • INIT.md - Create your own MCP servers")
    print("  • README.md - Overview")

    return True

if __name__ == "__main__":
    try:
        success = main()
        sys.exit(0 if success else 1)
    except KeyboardInterrupt:
        print(f"\n\n{Colors.YELLOW}Installation cancelled by user{Colors.RESET}")
        sys.exit(1)
    except Exception as e:
        print(f"\n\n{Colors.RED}Unexpected error: {e}{Colors.RESET}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
