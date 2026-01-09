#!/usr/bin/env python3
"""
STM32 MCP Documentation Server - Complete Uninstall Script

This script provides a comprehensive uninstall that removes all STM32 MCP
artifacts when the MCP server is removed via `claude mcp remove stm32-docs --scope user`.

Since Claude Code/MCP protocol doesn't support uninstall hooks, users must run
this script manually after running `claude mcp remove`.

IMPORTANT: There is no MCP uninstall hook mechanism available as of 2025.
This is documented in GitHub issues:
- anthropics/claude-code#11240 (Plugin Lifecycle Hooks)
- anthropics/claude-code#9394 (postInstall/postUninstall hooks)
Both remain unimplemented, so manual cleanup is required.

What this removes:
1. STM32 skills from ~/.claude/commands/ (auto-installed as Claude Code skills)
2. Legacy agents from ~/.claude/agents/ (if present from older versions)
3. Marker files ~/.claude/.stm32-skills-installed and ~/.claude/.stm32-agents-installed
4. ChromaDB database (user's data directory or package data directory)
5. MCP configuration entry from ~/.claude.json (if not using CLI)

Usage:
    stm32-uninstall              # Interactive uninstall
    stm32-uninstall --yes        # Non-interactive (auto-confirm)
    stm32-uninstall --dry-run    # Show what would be removed
    stm32-uninstall --keep-db    # Keep ChromaDB database

Complete Uninstall Steps:
    1. claude mcp remove stm32-docs --scope user  # Remove MCP config
    2. stm32-uninstall                       # Clean up everything else
"""

import sys
import os
import json
import shutil
import argparse
import platform
from pathlib import Path
from typing import List, Tuple, Optional

# Determine project root
if getattr(sys, 'frozen', False):
    SCRIPT_DIR = Path(sys.executable).parent
else:
    SCRIPT_DIR = Path(__file__).parent

PROJECT_ROOT = os.environ.get('STM32_PROJECT_DIR', SCRIPT_DIR.parent)
PROJECT_ROOT = Path(PROJECT_ROOT).resolve()


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
    print(f"\n{Colors.BOLD}{Colors.RED}{'='*60}{Colors.RESET}")
    print(f"{Colors.BOLD}{Colors.RED}{text.center(60)}{Colors.RESET}")
    print(f"{Colors.BOLD}{Colors.RED}{'='*60}{Colors.RESET}\n")


def print_success(text: str):
    """Print success message."""
    print(f"  {Colors.GREEN}[REMOVED]{Colors.RESET} {text}")


def print_skip(text: str):
    """Print skip message."""
    print(f"  {Colors.YELLOW}[SKIP]{Colors.RESET} {text}")


def print_info(text: str):
    """Print info message."""
    print(f"  {Colors.CYAN}[INFO]{Colors.RESET} {text}")


def print_warning(text: str):
    """Print warning message."""
    print(f"  {Colors.YELLOW}[WARN]{Colors.RESET} {text}")


def print_error(text: str):
    """Print error message."""
    print(f"  {Colors.RED}[ERROR]{Colors.RESET} {text}")


def get_claude_config_dir() -> Path:
    """Get the Claude Code configuration directory for the current user."""
    if platform.system() == 'Windows':
        if 'microsoft' in platform.uname().release.lower():
            home = Path.home()
        else:
            home = Path(os.environ.get('USERPROFILE', Path.home()))
    else:
        home = Path.home()

    return home / '.claude'


def get_uvx_cache_dirs() -> List[Path]:
    """Get potential uvx/uv cache directories where ChromaDB might be stored."""
    home = Path.home()
    cache_dirs = []

    # Common uv cache locations
    if platform.system() == 'Darwin':  # macOS
        cache_dirs.extend([
            home / 'Library' / 'Caches' / 'uv',
            home / '.cache' / 'uv',
        ])
    elif platform.system() == 'Windows':
        localappdata = os.environ.get('LOCALAPPDATA', home / 'AppData' / 'Local')
        cache_dirs.extend([
            Path(localappdata) / 'uv' / 'cache',
            home / '.cache' / 'uv',
        ])
    else:  # Linux and others
        xdg_cache = os.environ.get('XDG_CACHE_HOME', home / '.cache')
        cache_dirs.extend([
            Path(xdg_cache) / 'uv',
            home / '.cache' / 'uv',
        ])

    return [d for d in cache_dirs if d.exists()]


def find_chromadb_locations() -> List[Path]:
    """Find all potential ChromaDB database locations."""
    locations = []

    # Primary location: package data directory
    package_data = PROJECT_ROOT / 'data' / 'chroma_db'
    if package_data.exists():
        locations.append(package_data)

    # Secondary: Check if settings module is available for runtime config
    try:
        sys.path.insert(0, str(PROJECT_ROOT))
        from mcp_server.config import settings
        if settings.CHROMA_DB_PATH.exists():
            locations.append(settings.CHROMA_DB_PATH)
    except ImportError:
        pass

    # Check uvx cache for any stm32-mcp data directories
    for cache_dir in get_uvx_cache_dirs():
        # Search for stm32-related data directories in uvx cache
        for pattern in ['**/stm32*/**/chroma_db', '**/data/chroma_db']:
            for match in cache_dir.glob(pattern):
                if match.is_dir() and match not in locations:
                    locations.append(match)

    return locations


# List of STM32 agent files (legacy - from older versions in ~/.claude/agents/)
STM32_LEGACY_AGENTS = [
    'router.md',
    'triage.md',
    'firmware.md',
    'firmware-core.md',
    'debug.md',
    'bootloader.md',
    'bootloader-programming.md',
    'peripheral-comm.md',
    'peripheral-analog.md',
    'peripheral-graphics.md',
    'power.md',
    'power-management.md',
    'safety.md',
    'safety-certification.md',
    'security.md',
    'hardware-design.md',
]

# List of STM32 skills/commands installed to ~/.claude/commands/
# These are auto-generated from agent files with stm32- prefix
STM32_SKILLS = [
    # Auto-installed skills (converted from agents)
    'stm32-bootloader-programming.md',
    'stm32-bootloader.md',
    'stm32-debug.md',
    'stm32-firmware-core.md',
    'stm32-firmware.md',
    'stm32-hardware-design.md',
    'stm32-peripheral-analog.md',
    'stm32-peripheral-comm.md',
    'stm32-peripheral-graphics.md',
    'stm32-power-management.md',
    'stm32-power.md',
    'stm32-safety-certification.md',
    'stm32-safety.md',
    'stm32-security.md',
    # Core skills (may have been manually created or from older versions)
    'stm32.md',
    'stm32-hal.md',
    'stm32-init.md',
]


def collect_items_to_remove(keep_db: bool = False) -> Tuple[List[Path], List[Path], int]:
    """
    Collect all items that will be removed.

    Returns:
        Tuple of (files_to_remove, dirs_to_remove, total_size_bytes)
    """
    files = []
    dirs = []
    total_size = 0

    claude_dir = get_claude_config_dir()

    # Skills/Commands (primary installation location)
    commands_dir = claude_dir / 'commands'
    for skill in STM32_SKILLS:
        skill_path = commands_dir / skill
        if skill_path.exists():
            files.append(skill_path)
            total_size += skill_path.stat().st_size

    # Legacy agents (from older versions, now deprecated)
    agents_dir = claude_dir / 'agents'
    for agent in STM32_LEGACY_AGENTS:
        agent_path = agents_dir / agent
        if agent_path.exists():
            files.append(agent_path)
            total_size += agent_path.stat().st_size

    # Marker files (both old and new names)
    marker_files = [
        claude_dir / '.stm32-skills-installed',    # New marker (skills)
        claude_dir / '.stm32-agents-installed',    # Legacy marker (agents)
    ]
    for marker in marker_files:
        if marker.exists():
            files.append(marker)
            total_size += marker.stat().st_size

    # ChromaDB database
    if not keep_db:
        for db_path in find_chromadb_locations():
            if db_path.exists():
                dirs.append(db_path)
                # Calculate directory size
                for f in db_path.rglob('*'):
                    if f.is_file():
                        total_size += f.stat().st_size

    return files, dirs, total_size


def format_size(size_bytes: int) -> str:
    """Format byte size to human-readable string."""
    for unit in ['B', 'KB', 'MB', 'GB']:
        if size_bytes < 1024:
            return f"{size_bytes:.1f} {unit}"
        size_bytes /= 1024
    return f"{size_bytes:.1f} TB"


def remove_mcp_config_entry() -> bool:
    """
    Remove stm32-docs entry from ~/.claude.json if present.

    Note: If user used `claude mcp add`, they should also run `claude mcp remove`.
    This function handles manual JSON configurations.

    Claude Code stores MCP configurations in ~/.claude.json (not ~/.claude/mcp.json).
    The mcpServers key contains all MCP server configurations.
    """
    home = Path.home()
    mcp_config = home / '.claude.json'

    if not mcp_config.exists():
        return False

    try:
        with open(mcp_config) as f:
            config = json.load(f)

        if 'stm32-docs' not in config.get('mcpServers', {}):
            return False

        del config['mcpServers']['stm32-docs']

        with open(mcp_config, 'w') as f:
            json.dump(config, f, indent=2)

        return True
    except (json.JSONDecodeError, KeyError, IOError):
        return False


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


def check_mcp_still_registered() -> bool:
    """Check if stm32-docs is still registered in MCP config."""
    import subprocess
    try:
        result = subprocess.run(
            ["claude", "mcp", "list"],
            capture_output=True,
            text=True,
            timeout=10
        )
        return 'stm32-docs' in result.stdout
    except (subprocess.TimeoutExpired, FileNotFoundError, OSError):
        return False


def uninstall(dry_run: bool = False, yes: bool = False, keep_db: bool = False) -> bool:
    """
    Perform the complete uninstall.

    Args:
        dry_run: Only show what would be removed
        yes: Skip confirmation prompt
        keep_db: Keep ChromaDB database

    Returns:
        True if uninstall completed successfully
    """
    print_header("STM32 MCP Server - Complete Uninstall")

    # Check if MCP server is still registered
    if check_claude_cli_available() and check_mcp_still_registered():
        print_warning("stm32-docs is still registered as an MCP server!")
        print_info("Run this command first to remove the MCP configuration:")
        print(f"\n    {Colors.CYAN}claude mcp remove stm32-docs --scope user{Colors.RESET}\n")
        if not yes:
            response = input("Continue anyway? [y/N]: ").strip().lower()
            if response != 'y':
                print_info("Uninstall cancelled. Run the command above first.")
                return False

    # Collect items to remove
    files, dirs, total_size = collect_items_to_remove(keep_db)

    if not files and not dirs:
        print_info("Nothing to remove. STM32 MCP server appears to be already uninstalled.")
        return True

    # Show what will be removed
    print(f"\n{Colors.BOLD}The following items will be removed:{Colors.RESET}\n")

    claude_dir = get_claude_config_dir()

    # Group by category
    skills = [f for f in files if 'commands' in str(f)]
    legacy_agents = [f for f in files if 'agents' in str(f) and not f.name.startswith('.')]
    markers = [f for f in files if f.name.startswith('.stm32-')]

    if skills:
        print(f"  {Colors.CYAN}Skills/Commands ({len(skills)} files):{Colors.RESET}")
        for f in skills:
            print(f"    - {f.relative_to(claude_dir.parent)}")

    if legacy_agents:
        print(f"\n  {Colors.CYAN}Legacy Agents ({len(legacy_agents)} files):{Colors.RESET}")
        for f in legacy_agents:
            print(f"    - {f.relative_to(claude_dir.parent)}")

    if markers:
        print(f"\n  {Colors.CYAN}Marker Files:{Colors.RESET}")
        for f in markers:
            print(f"    - {f.relative_to(claude_dir.parent)}")

    if dirs:
        print(f"\n  {Colors.CYAN}Databases ({len(dirs)} directories):{Colors.RESET}")
        for d in dirs:
            print(f"    - {d}")

    print(f"\n  {Colors.YELLOW}Total size: {format_size(total_size)}{Colors.RESET}")

    if dry_run:
        print(f"\n{Colors.YELLOW}Dry run mode - no files were removed.{Colors.RESET}")
        return True

    # Confirm
    if not yes:
        print()
        response = input("Proceed with uninstall? [y/N]: ").strip().lower()
        if response != 'y':
            print_info("Uninstall cancelled.")
            return False

    # Perform removal
    print(f"\n{Colors.BOLD}Removing files...{Colors.RESET}\n")

    removed_count = 0
    error_count = 0

    # Remove files
    for f in files:
        try:
            f.unlink()
            print_success(f.name)
            removed_count += 1
        except OSError as e:
            print_error(f"Failed to remove {f.name}: {e}")
            error_count += 1

    # Remove directories
    for d in dirs:
        try:
            shutil.rmtree(d)
            print_success(f"{d.name}/ (database)")
            removed_count += 1
        except OSError as e:
            print_error(f"Failed to remove {d}: {e}")
            error_count += 1

    # Also try to remove MCP config entry (in case user didn't use CLI)
    if remove_mcp_config_entry():
        print_success("~/.claude.json entry for stm32-docs")
        removed_count += 1

    # Summary
    print()
    if error_count == 0:
        print(f"{Colors.GREEN}{'='*60}{Colors.RESET}")
        print(f"{Colors.GREEN}{'Uninstall Complete!'.center(60)}{Colors.RESET}")
        print(f"{Colors.GREEN}{'='*60}{Colors.RESET}")
        print(f"\n  Removed {removed_count} items ({format_size(total_size)} freed)")
    else:
        print(f"{Colors.YELLOW}{'='*60}{Colors.RESET}")
        print(f"{Colors.YELLOW}{'Uninstall Completed with Errors'.center(60)}{Colors.RESET}")
        print(f"{Colors.YELLOW}{'='*60}{Colors.RESET}")
        print(f"\n  Removed: {removed_count}, Errors: {error_count}")

    # Additional cleanup instructions
    print(f"\n{Colors.BOLD}Additional cleanup (optional):{Colors.RESET}")
    print("  - Remove Python package: pip uninstall stm32-mcp-docs")
    print("  - Clear uv cache: uv cache clean")

    return error_count == 0


def main():
    """Main entry point."""
    parser = argparse.ArgumentParser(
        description="STM32 MCP Documentation Server - Complete Uninstall",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Complete Uninstall Steps:
  1. claude mcp remove stm32-docs --scope user  # Remove MCP configuration
  2. stm32-uninstall                       # Clean up agents, commands, and database

Examples:
  stm32-uninstall                # Interactive uninstall
  stm32-uninstall --yes          # Non-interactive (auto-confirm)
  stm32-uninstall --dry-run      # Show what would be removed
  stm32-uninstall --keep-db      # Keep ChromaDB database

Why manual cleanup is required:
  The MCP protocol does not support uninstall hooks. When you run
  `claude mcp remove`, only the MCP server configuration is removed.
  Installed agents, commands, and databases are NOT cleaned up.

  This is a known limitation documented in GitHub issues:
  - anthropics/claude-code#11240 (Plugin Lifecycle Hooks)
  - anthropics/claude-code#9394 (postInstall/postUninstall hooks)
        """
    )

    parser.add_argument(
        '--dry-run',
        action='store_true',
        help='Show what would be removed without actually removing'
    )
    parser.add_argument(
        '--yes', '-y',
        action='store_true',
        help='Skip confirmation prompt'
    )
    parser.add_argument(
        '--keep-db',
        action='store_true',
        help='Keep ChromaDB database (only remove agents and commands)'
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

    success = uninstall(
        dry_run=args.dry_run,
        yes=args.yes,
        keep_db=args.keep_db
    )

    return 0 if success else 1


if __name__ == "__main__":
    sys.exit(main())
