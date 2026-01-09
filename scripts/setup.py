#!/usr/bin/env python3
"""
STM32 MCP Documentation Server - Complete Setup Script

This script provides a unified setup experience that:
1. Configures the MCP server for Claude Code
2. Installs agents to user's Claude configuration
3. Ingests documentation into ChromaDB (if needed)
4. Verifies the installation

Usage:
    stm32-setup              # Run full setup
    stm32-setup --mcp-only   # Only configure MCP server
    stm32-setup --agents     # Only install agents
    stm32-setup --ingest     # Only run ingestion
    stm32-setup --verify     # Only verify installation
    stm32-setup --status     # Show current installation status
    stm32-setup --uninstall  # Remove configurations

Environment:
    STM32_PROJECT_DIR: Override the detected project directory
"""

import sys
import os
import json
import shutil
import argparse
import platform
from pathlib import Path
from typing import Optional, Dict, Any, List, Tuple

# Determine project root
if getattr(sys, 'frozen', False):
    # Running as compiled executable
    SCRIPT_DIR = Path(sys.executable).parent
else:
    SCRIPT_DIR = Path(__file__).parent

PROJECT_ROOT = os.environ.get('STM32_PROJECT_DIR', SCRIPT_DIR.parent)
PROJECT_ROOT = Path(PROJECT_ROOT).resolve()

# Add project root to path for imports
sys.path.insert(0, str(PROJECT_ROOT))


class Colors:
    """ANSI color codes for terminal output."""
    RESET = '\033[0m'
    BOLD = '\033[1m'
    RED = '\033[91m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    BLUE = '\033[94m'
    CYAN = '\033[96m'

    @classmethod
    def disable(cls):
        """Disable colors for non-TTY output."""
        cls.RESET = cls.BOLD = cls.RED = cls.GREEN = ''
        cls.YELLOW = cls.BLUE = cls.CYAN = ''


def print_header(text: str):
    """Print a formatted header."""
    print(f"\n{Colors.BOLD}{Colors.BLUE}{'='*60}{Colors.RESET}")
    print(f"{Colors.BOLD}{Colors.BLUE}{text.center(60)}{Colors.RESET}")
    print(f"{Colors.BOLD}{Colors.BLUE}{'='*60}{Colors.RESET}\n")


def print_step(step: int, text: str):
    """Print a step indicator."""
    print(f"{Colors.CYAN}[{step}]{Colors.RESET} {text}")


def print_success(text: str):
    """Print success message."""
    print(f"  {Colors.GREEN}[OK]{Colors.RESET} {text}")


def print_warning(text: str):
    """Print warning message."""
    print(f"  {Colors.YELLOW}[WARN]{Colors.RESET} {text}")


def print_error(text: str):
    """Print error message."""
    print(f"  {Colors.RED}[ERROR]{Colors.RESET} {text}")


def print_info(text: str):
    """Print info message."""
    print(f"  {Colors.CYAN}[INFO]{Colors.RESET} {text}")


def get_claude_config_dir() -> Path:
    """Get the Claude Code configuration directory for the current user."""
    if platform.system() == 'Windows':
        # Windows: Check for WSL or native
        if 'microsoft' in platform.uname().release.lower():
            # Running in WSL - use Linux-style path
            home = Path.home()
        else:
            # Native Windows
            home = Path(os.environ.get('USERPROFILE', Path.home()))
    else:
        # Linux/macOS
        home = Path.home()

    return home / '.claude'


def get_project_venv_python() -> Optional[Path]:
    """Find the project's virtual environment Python executable."""
    venv_paths = [
        PROJECT_ROOT / '.venv' / 'bin' / 'python',      # Linux/macOS
        PROJECT_ROOT / '.venv' / 'Scripts' / 'python.exe',  # Windows
        PROJECT_ROOT / 'venv' / 'bin' / 'python',
        PROJECT_ROOT / 'venv' / 'Scripts' / 'python.exe',
    ]

    for path in venv_paths:
        if path.exists():
            return path

    return None


def detect_installation_type() -> Tuple[str, Path]:
    """
    Detect how the package was installed.

    Returns:
        Tuple of (install_type, base_path)
        install_type: 'source', 'pip', or 'editable'
    """
    # Check if we're in a source checkout
    if (PROJECT_ROOT / '.git').exists() or (PROJECT_ROOT / 'pyproject.toml').exists():
        # Check if installed as editable
        try:
            import stm32_mcp_docs
            if hasattr(stm32_mcp_docs, '__path__'):
                return 'editable', PROJECT_ROOT
        except ImportError:
            pass
        return 'source', PROJECT_ROOT

    # Check for pip installation
    try:
        import importlib.metadata
        dist = importlib.metadata.distribution('stm32-mcp-docs')
        return 'pip', Path(dist._path).parent
    except Exception:
        pass

    return 'source', PROJECT_ROOT


def check_markdowns_available() -> Tuple[bool, Optional[Path]]:
    """Check if markdown documentation is available.

    The markdowns are bundled inside the mcp_server package.
    """
    # Check package location first (where markdowns are bundled)
    package_markdowns_dir = PROJECT_ROOT / 'mcp_server' / 'markdowns'
    if package_markdowns_dir.exists() and list(package_markdowns_dir.glob('*.md')):
        return True, package_markdowns_dir

    # Fallback: check old location for backward compatibility
    legacy_markdowns_dir = PROJECT_ROOT / 'markdowns'
    if legacy_markdowns_dir.exists() and list(legacy_markdowns_dir.glob('*.md')):
        return True, legacy_markdowns_dir

    return False, None


def check_chromadb_populated() -> Tuple[bool, int]:
    """Check if ChromaDB has been populated with documents."""
    try:
        from storage.chroma_store import STM32ChromaStore
        from mcp_server.config import settings

        store = STM32ChromaStore(
            persist_dir=settings.CHROMA_DB_PATH,
            collection_name=settings.COLLECTION_NAME,
            embedding_model=settings.EMBEDDING_MODEL
        )
        count = store.count()
        return count > 0, count
    except Exception:
        return False, 0


def generate_mcp_config(python_path: Path, install_type: str) -> Dict[str, Any]:
    """Generate MCP configuration JSON for manual fallback."""
    return {
        "mcpServers": {
            "stm32-docs": {
                "command": str(python_path),
                "args": ["-m", "mcp_server"],
                "env": {
                    "STM32_SERVER_MODE": "local",
                    "STM32_LOG_LEVEL": "INFO"
                },
                "description": "STM32 documentation search and retrieval via semantic search. Note: First startup takes ~90s due to ML model loading."
            }
        }
    }


def check_claude_cli_available() -> bool:
    """Check if the Claude CLI is available."""
    import subprocess
    try:
        result = subprocess.run(
            ["claude", "--version"],
            capture_output=True,
            text=True,
            timeout=10
        )
        return result.returncode == 0
    except (subprocess.TimeoutExpired, FileNotFoundError, OSError):
        return False


def configure_mcp_via_cli(python_path: Path) -> bool:
    """
    Configure MCP server using the Claude CLI.

    Uses: claude mcp add stm32-docs --scope user -- python -m mcp_server

    Returns:
        True if successful, False otherwise
    """
    import subprocess

    try:
        # Build the command
        cmd = [
            "claude", "mcp", "add", "stm32-docs",
            "-s", "user",
            "-e", "STM32_SERVER_MODE=local",
            "-e", "STM32_LOG_LEVEL=INFO",
            "--",
            str(python_path), "-m", "mcp_server"
        ]

        result = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            timeout=30,
            cwd=str(PROJECT_ROOT)
        )

        if result.returncode == 0:
            return True
        else:
            # Server might already exist, try to update it
            if "already exists" in result.stderr.lower():
                print_info("stm32-docs already configured, updating...")
                # Remove and re-add
                subprocess.run(
                    ["claude", "mcp", "remove", "stm32-docs", "-s", "user"],
                    capture_output=True,
                    timeout=10
                )
                result = subprocess.run(cmd, capture_output=True, text=True, timeout=30, cwd=str(PROJECT_ROOT))
                return result.returncode == 0
            return False
    except (subprocess.TimeoutExpired, FileNotFoundError, OSError) as e:
        logger_msg = f"Claude CLI error: {e}" if 'e' in dir() else "Claude CLI not available"
        return False


def configure_mcp(force: bool = False) -> bool:
    """
    Configure MCP server for Claude Code.

    This uses the Claude CLI `claude mcp add` command when available,
    with a fallback to manual configuration if the CLI is not available.
    """
    print_step(1, "Configuring MCP server for Claude Code...")

    # Find Python executable
    python_path = get_project_venv_python()
    if not python_path:
        print_warning("Virtual environment not found. Using system Python.")
        python_path = Path(sys.executable)

    # Verify server module exists
    server_module = PROJECT_ROOT / 'mcp_server' / '__main__.py'
    if not server_module.exists():
        print_error(f"Server module not found: {server_module}")
        return False

    # Try Claude CLI first (preferred method)
    if check_claude_cli_available():
        print_info("Using Claude CLI for MCP configuration...")
        if configure_mcp_via_cli(python_path):
            print_success("Configured stm32-docs via 'claude mcp add'")
            print_info(f"Python: {python_path}")
            print_info(f"Module: python -m mcp_server")
            return True
        else:
            print_warning("Claude CLI configuration failed, falling back to manual config")

    # Fallback: Manual configuration
    # Claude Code stores MCP configs in ~/.claude.json (not ~/.claude/mcp.json)
    print_info("Using manual MCP configuration (Claude CLI not available)...")

    home = Path.home()
    mcp_config_path = home / '.claude.json'

    install_type, _ = detect_installation_type()
    new_config = generate_mcp_config(python_path, install_type)

    # No need to create directory - ~/.claude.json is a file in home directory

    # Handle existing configuration
    if mcp_config_path.exists():
        try:
            with open(mcp_config_path, 'r') as f:
                existing_config = json.load(f)
        except json.JSONDecodeError:
            print_warning("Existing ~/.claude.json is invalid, will be replaced")
            existing_config = {"mcpServers": {}}

        if "stm32-docs" in existing_config.get("mcpServers", {}) and not force:
            print_info("stm32-docs already configured in ~/.claude.json")
            # Update it anyway to ensure paths are correct
            existing_config["mcpServers"]["stm32-docs"] = new_config["mcpServers"]["stm32-docs"]
            with open(mcp_config_path, 'w') as f:
                json.dump(existing_config, f, indent=2)
            print_success("Updated existing stm32-docs configuration")
            return True

        # Merge configurations
        existing_config.setdefault("mcpServers", {})
        existing_config["mcpServers"]["stm32-docs"] = new_config["mcpServers"]["stm32-docs"]

        with open(mcp_config_path, 'w') as f:
            json.dump(existing_config, f, indent=2)
        print_success(f"Added stm32-docs to {mcp_config_path}")
    else:
        with open(mcp_config_path, 'w') as f:
            json.dump(new_config, f, indent=2)
        print_success(f"Created {mcp_config_path}")

    # Show configuration
    print_info(f"Python: {python_path}")
    print_info(f"Module: python -m mcp_server")
    print_info(f"Project: {PROJECT_ROOT}")

    return True


def install_agents(force: bool = False) -> bool:
    """
    Install agent definitions to user's Claude configuration.
    """
    print_step(2, "Installing Claude Code agents...")

    source_agents_dir = PROJECT_ROOT / '.claude' / 'agents'
    source_commands_dir = PROJECT_ROOT / '.claude' / 'commands'

    if not source_agents_dir.exists():
        print_error(f"Agents directory not found: {source_agents_dir}")
        return False

    claude_dir = get_claude_config_dir()
    target_agents_dir = claude_dir / 'agents'
    target_commands_dir = claude_dir / 'commands'

    # Create directories
    target_agents_dir.mkdir(parents=True, exist_ok=True)
    target_commands_dir.mkdir(parents=True, exist_ok=True)

    # Copy agents (skip internal files)
    agents_copied = 0
    for agent_file in source_agents_dir.glob('*.md'):
        if agent_file.name.startswith('_') or 'GUIDE' in agent_file.name.upper():
            continue  # Skip template and guide files

        target_path = target_agents_dir / agent_file.name
        if target_path.exists() and not force:
            print_info(f"Agent exists (skipped): {agent_file.name}")
        else:
            shutil.copy2(agent_file, target_path)
            print_success(f"Installed agent: {agent_file.name}")
            agents_copied += 1

    # Copy commands
    commands_copied = 0
    if source_commands_dir.exists():
        for cmd_file in source_commands_dir.glob('*.md'):
            target_path = target_commands_dir / cmd_file.name
            if target_path.exists() and not force:
                print_info(f"Command exists (skipped): {cmd_file.name}")
            else:
                shutil.copy2(cmd_file, target_path)
                print_success(f"Installed command: {cmd_file.name}")
                commands_copied += 1

    print_info(f"Agents installed to: {target_agents_dir}")
    print_info(f"Commands installed to: {target_commands_dir}")

    return True


def run_ingestion(clear: bool = False, verbose: bool = False, force: bool = False) -> bool:
    """
    Run document ingestion to populate ChromaDB.

    Args:
        clear: Clear existing data before ingestion
        verbose: Enable verbose output
        force: Force ingestion even if database already has documents
    """
    print_step(3, "Ingesting STM32 documentation into vector database...")

    has_markdowns, markdowns_path = check_markdowns_available()
    if not has_markdowns:
        print_error("Markdown documentation not found!")
        print_info("The mcp_server/markdowns/ directory with STM32 documentation is required.")
        print_info("This should be included when installing via pip/uvx from the repository.")
        print_info("If missing, reinstall from the git repository:")
        print_info("  uvx --from git+https://github.com/creativec09/stm32-agents.git stm32-mcp-docs")
        return False

    # Check if already populated
    is_populated, doc_count = check_chromadb_populated()
    if is_populated and not clear and not force:
        print_success(f"Pre-built database detected: {doc_count} document chunks")
        print_info("Skipping ingestion (database already populated)")
        print_info("Use --force-ingest to rebuild, or --clear to wipe and rebuild")
        return True

    # Import and run ingestion
    try:
        from scripts.ingest_docs import ingest_documents
        from mcp_server.config import settings

        result = ingest_documents(
            source_dir=markdowns_path,
            clear_existing=clear,
            verbose=verbose
        )

        if result.get("error"):
            print_error(f"Ingestion failed: {result.get('error')}")
            return False

        print_success(f"Ingested {result.get('total_chunks', 0)} chunks from {result.get('total_files', 0)} files")
        return True

    except ImportError as e:
        print_error(f"Failed to import ingestion module: {e}")
        print_info("Try running: pip install -e .")
        return False
    except Exception as e:
        print_error(f"Ingestion failed: {e}")
        return False


def verify_installation() -> bool:
    """
    Verify the complete installation.
    """
    print_step(4, "Verifying installation...")

    all_ok = True

    # Check Python packages
    print("\n  Checking Python packages...")
    required_packages = ['mcp', 'chromadb', 'sentence_transformers', 'pydantic']
    for pkg in required_packages:
        try:
            __import__(pkg.replace('-', '_'))
            print_success(f"Package: {pkg}")
        except ImportError:
            print_error(f"Package missing: {pkg}")
            all_ok = False

    # Check MCP configuration
    # Claude Code stores MCP configs in ~/.claude.json
    print("\n  Checking MCP configuration...")
    home = Path.home()
    mcp_config = home / '.claude.json'
    if mcp_config.exists():
        try:
            with open(mcp_config) as f:
                config = json.load(f)
            if "stm32-docs" in config.get("mcpServers", {}):
                print_success("MCP: stm32-docs configured")
            else:
                print_warning("MCP: stm32-docs not in configuration")
                all_ok = False
        except Exception as e:
            print_error(f"MCP: Failed to read config: {e}")
            all_ok = False
    else:
        print_error("MCP: Configuration file not found")
        all_ok = False

    # Check agents
    print("\n  Checking agents...")
    agents_dir = claude_dir / 'agents'
    expected_agents = ['router.md', 'firmware-core.md', 'debug.md']
    for agent in expected_agents:
        if (agents_dir / agent).exists():
            print_success(f"Agent: {agent}")
        else:
            print_warning(f"Agent missing: {agent}")

    # Check commands
    print("\n  Checking slash commands...")
    commands_dir = claude_dir / 'commands'
    expected_commands = ['stm32.md', 'stm32-hal.md', 'stm32-init.md', 'stm32-debug.md']
    for cmd in expected_commands:
        if (commands_dir / cmd).exists():
            print_success(f"Command: /{cmd.replace('.md', '')}")
        else:
            print_warning(f"Command missing: {cmd}")

    # Check ChromaDB
    print("\n  Checking vector database...")
    is_populated, doc_count = check_chromadb_populated()
    if is_populated:
        print_success(f"ChromaDB: {doc_count} document chunks indexed")
    else:
        print_warning("ChromaDB: No documents indexed (run stm32-setup --ingest)")
        all_ok = False

    # Check server script
    print("\n  Checking server...")
    server_script = PROJECT_ROOT / 'mcp_server' / 'server.py'
    if server_script.exists():
        print_success(f"Server script: {server_script}")
    else:
        print_error("Server script not found")
        all_ok = False

    return all_ok


def show_status():
    """Show current installation status."""
    print_header("STM32 MCP Server - Installation Status")

    install_type, base_path = detect_installation_type()
    print(f"Installation type: {Colors.CYAN}{install_type}{Colors.RESET}")
    print(f"Project directory: {Colors.CYAN}{PROJECT_ROOT}{Colors.RESET}")

    # Virtual environment
    venv_python = get_project_venv_python()
    if venv_python:
        print(f"Virtual environment: {Colors.GREEN}Found{Colors.RESET} ({venv_python})")
    else:
        print(f"Virtual environment: {Colors.YELLOW}Not found{Colors.RESET}")

    # Documentation
    has_markdowns, markdowns_path = check_markdowns_available()
    if has_markdowns:
        md_count = len(list(markdowns_path.glob('*.md')))
        print(f"Documentation files: {Colors.GREEN}{md_count} markdown files{Colors.RESET}")
    else:
        print(f"Documentation files: {Colors.RED}Not found{Colors.RESET}")

    # ChromaDB
    is_populated, doc_count = check_chromadb_populated()
    if is_populated:
        print(f"Vector database: {Colors.GREEN}{doc_count} chunks indexed{Colors.RESET}")
    else:
        print(f"Vector database: {Colors.YELLOW}Empty (needs ingestion){Colors.RESET}")

    # MCP configuration - Claude Code stores configs in ~/.claude.json
    home = Path.home()
    mcp_config = home / '.claude.json'
    if mcp_config.exists():
        try:
            with open(mcp_config) as f:
                config = json.load(f)
            if "stm32-docs" in config.get("mcpServers", {}):
                print(f"MCP configuration: {Colors.GREEN}Configured{Colors.RESET}")
            else:
                print(f"MCP configuration: {Colors.YELLOW}Missing stm32-docs{Colors.RESET}")
        except Exception:
            print(f"MCP configuration: {Colors.RED}Invalid{Colors.RESET}")
    else:
        print(f"MCP configuration: {Colors.YELLOW}Not found (~/.claude.json){Colors.RESET}")

    # Agents
    agents_dir = claude_dir / 'agents'
    if agents_dir.exists():
        agent_count = len(list(agents_dir.glob('*.md')))
        print(f"Installed agents: {Colors.GREEN}{agent_count} agents{Colors.RESET}")
    else:
        print(f"Installed agents: {Colors.RED}None{Colors.RESET}")

    # Commands
    commands_dir = claude_dir / 'commands'
    if commands_dir.exists():
        stm32_commands = list(commands_dir.glob('stm32*.md'))
        print(f"Slash commands: {Colors.GREEN}{len(stm32_commands)} commands{Colors.RESET}")
    else:
        print(f"Slash commands: {Colors.RED}None{Colors.RESET}")

    print(f"\nClaude config directory: {claude_dir}")


def uninstall():
    """Remove STM32 MCP configurations.

    Note: For complete uninstall including ChromaDB database,
    use the dedicated `stm32-uninstall` command instead.
    """
    print_header("STM32 MCP Server - Uninstall")

    claude_dir = get_claude_config_dir()

    # Remove from MCP config - Claude Code stores configs in ~/.claude.json
    home = Path.home()
    mcp_config = home / '.claude.json'
    if mcp_config.exists():
        try:
            with open(mcp_config) as f:
                config = json.load(f)
            if "stm32-docs" in config.get("mcpServers", {}):
                del config["mcpServers"]["stm32-docs"]
                with open(mcp_config, 'w') as f:
                    json.dump(config, f, indent=2)
                print_success("Removed stm32-docs from MCP configuration")
            else:
                print_info("stm32-docs not in MCP configuration")
        except Exception as e:
            print_error(f"Failed to update MCP config: {e}")

    # Remove agents
    agents_dir = claude_dir / 'agents'
    stm32_agents = [
        'router.md', 'triage.md', 'firmware.md', 'firmware-core.md',
        'debug.md', 'bootloader.md', 'bootloader-programming.md',
        'peripheral-comm.md', 'peripheral-analog.md', 'peripheral-graphics.md',
        'power.md', 'power-management.md', 'safety.md', 'safety-certification.md',
        'security.md', 'hardware-design.md'
    ]
    for agent in stm32_agents:
        agent_path = agents_dir / agent
        if agent_path.exists():
            agent_path.unlink()
            print_success(f"Removed agent: {agent}")

    # Remove commands
    commands_dir = claude_dir / 'commands'
    stm32_commands = ['stm32.md', 'stm32-hal.md', 'stm32-init.md', 'stm32-debug.md']
    for cmd in stm32_commands:
        cmd_path = commands_dir / cmd
        if cmd_path.exists():
            cmd_path.unlink()
            print_success(f"Removed command: {cmd}")

    # Remove marker file
    marker = claude_dir / '.stm32-agents-installed'
    if marker.exists():
        marker.unlink()
        print_success("Removed installation marker file")

    # Try to remove ChromaDB database
    chroma_db_path = PROJECT_ROOT / 'data' / 'chroma_db'
    if chroma_db_path.exists():
        try:
            shutil.rmtree(chroma_db_path)
            print_success("Removed ChromaDB database")
        except Exception as e:
            print_warning(f"Could not remove ChromaDB database: {e}")

    print_info("\nNote: This does not remove:")
    print_info("  - The installed Python package (use: pip uninstall stm32-mcp-docs)")
    print_info("  - The project directory")
    print_info("")
    print_info("For complete uninstall including uvx cache cleanup:")
    print_info("  1. claude mcp remove stm32-docs --scope user")
    print_info("  2. stm32-uninstall")


def main():
    """Main entry point for setup script."""
    parser = argparse.ArgumentParser(
        description="STM32 MCP Documentation Server Setup",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  stm32-setup                    Run complete setup (skips ingestion if DB exists)
  stm32-setup --status           Show installation status
  stm32-setup --mcp-only         Only configure MCP server
  stm32-setup --agents           Only install agents
  stm32-setup --ingest           Only run documentation ingestion (skips if exists)
  stm32-setup --force-ingest     Force re-ingestion even if DB exists
  stm32-setup --ingest --clear   Clear and re-ingest all documentation
  stm32-setup --verify           Verify installation
  stm32-setup --uninstall        Remove configurations
        """
    )

    parser.add_argument(
        '--mcp-only',
        action='store_true',
        help='Only configure MCP server'
    )
    parser.add_argument(
        '--agents',
        action='store_true',
        help='Only install agents and commands'
    )
    parser.add_argument(
        '--ingest',
        action='store_true',
        help='Only run documentation ingestion'
    )
    parser.add_argument(
        '--verify',
        action='store_true',
        help='Only verify installation'
    )
    parser.add_argument(
        '--status',
        action='store_true',
        help='Show current installation status'
    )
    parser.add_argument(
        '--uninstall',
        action='store_true',
        help='Remove STM32 MCP configurations'
    )
    parser.add_argument(
        '--force',
        action='store_true',
        help='Force overwrite existing configurations'
    )
    parser.add_argument(
        '--clear',
        action='store_true',
        help='Clear existing ChromaDB data before ingestion'
    )
    parser.add_argument(
        '--force-ingest',
        action='store_true',
        help='Force ingestion even if pre-built database exists'
    )
    parser.add_argument(
        '--verbose', '-v',
        action='store_true',
        help='Verbose output'
    )
    parser.add_argument(
        '--no-color',
        action='store_true',
        help='Disable colored output'
    )

    args = parser.parse_args()

    # Disable colors if requested or not a TTY
    if args.no_color or not sys.stdout.isatty():
        Colors.disable()

    # Handle specific commands
    if args.status:
        show_status()
        return 0

    if args.uninstall:
        uninstall()
        return 0

    if args.verify:
        success = verify_installation()
        return 0 if success else 1

    # Determine what to run
    run_mcp = args.mcp_only or not (args.agents or args.ingest)
    run_agents = args.agents or not (args.mcp_only or args.ingest)
    run_ingest = args.ingest or not (args.mcp_only or args.agents)

    print_header("STM32 MCP Documentation Server Setup")

    success = True

    # Run selected setup steps
    if run_mcp:
        if not configure_mcp(args.force):
            success = False

    if run_agents:
        if not install_agents(args.force):
            success = False

    if run_ingest:
        force_ingest = getattr(args, 'force_ingest', False)
        if not run_ingestion(args.clear, args.verbose, force_ingest):
            success = False

    # Always verify at the end of full setup
    if not (args.mcp_only or args.agents or args.ingest):
        print("\n")
        verify_installation()

    # Print summary
    print("\n")
    if success:
        print(f"{Colors.GREEN}{'='*60}{Colors.RESET}")
        print(f"{Colors.GREEN}{'Setup Complete!'.center(60)}{Colors.RESET}")
        print(f"{Colors.GREEN}{'='*60}{Colors.RESET}")
        print(f"\n{Colors.BOLD}Next steps:{Colors.RESET}")
        print("  1. Restart Claude Code to load the new MCP server")
        print("  2. Try a command: /stm32 How do I configure UART?")
        print("  3. Or ask naturally: 'Search STM32 docs for DMA setup'")
    else:
        print(f"{Colors.RED}{'='*60}{Colors.RESET}")
        print(f"{Colors.RED}{'Setup completed with warnings'.center(60)}{Colors.RESET}")
        print(f"{Colors.RED}{'='*60}{Colors.RESET}")
        print("\nSome components may need manual attention.")
        print("Run 'stm32-setup --status' to see current state.")

    return 0 if success else 1


if __name__ == "__main__":
    sys.exit(main())
