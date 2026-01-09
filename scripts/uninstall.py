#!/usr/bin/env python3
"""
STM32 MCP Documentation Server - Database Cleanup Script

This script removes the ChromaDB database and related artifacts when uninstalling
the STM32 MCP server.

NOTE: Agent and command cleanup is now handled by the Claude Code plugin system.
When users run `/plugin uninstall stm32-agents`, Claude Code automatically removes:
- Agents from the agents/ directory
- Commands from the commands/ directory
- MCP server configuration

This script only handles:
1. ChromaDB database (user's data directory or package data directory)
2. MCP configuration entry from ~/.claude.json (manual fallback)
3. Legacy marker files (from older versions)

Usage:
    stm32-uninstall              # Interactive uninstall
    stm32-uninstall --yes        # Non-interactive (auto-confirm)
    stm32-uninstall --dry-run    # Show what would be removed

Complete Uninstall Steps:
    1. /plugin uninstall stm32-agents    # Remove plugin (agents, commands, MCP config)
    2. stm32-uninstall                   # Clean up database
"""

import sys
import os
import json
import shutil
import argparse
import platform
from pathlib import Path
from typing import List, Tuple

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


def collect_items_to_remove() -> Tuple[List[Path], List[Path], int]:
    """
    Collect all items that will be removed.

    Returns:
        Tuple of (files_to_remove, dirs_to_remove, total_size_bytes)
    """
    files = []
    dirs = []
    total_size = 0

    claude_dir = get_claude_config_dir()

    # Legacy marker files (from older versions before plugin system)
    marker_files = [
        claude_dir / '.stm32-skills-installed',    # Old skills marker
        claude_dir / '.stm32-agents-installed',    # Legacy agents marker
    ]
    for marker in marker_files:
        if marker.exists():
            files.append(marker)
            total_size += marker.stat().st_size

    # ChromaDB database
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

    Note: This is a fallback for manual cleanup. The plugin system should
    handle MCP configuration automatically.
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


def uninstall(dry_run: bool = False, yes: bool = False) -> bool:
    """
    Perform the database cleanup.

    Args:
        dry_run: Only show what would be removed
        yes: Skip confirmation prompt

    Returns:
        True if cleanup completed successfully
    """
    print_header("STM32 MCP Server - Database Cleanup")

    print_info("This script removes the ChromaDB database and related artifacts.")
    print_info("Agent/command cleanup is handled by: /plugin uninstall stm32-agents")
    print()

    # Collect items to remove
    files, dirs, total_size = collect_items_to_remove()

    if not files and not dirs:
        print_info("Nothing to remove. Database appears to be already cleaned up.")
        return True

    # Show what will be removed
    print(f"\n{Colors.BOLD}The following items will be removed:{Colors.RESET}\n")

    if files:
        print(f"  {Colors.CYAN}Marker Files ({len(files)}):{Colors.RESET}")
        for f in files:
            print(f"    - {f}")

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
        response = input("Proceed with cleanup? [y/N]: ").strip().lower()
        if response != 'y':
            print_info("Cleanup cancelled.")
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

    # Also try to remove MCP config entry (fallback)
    if remove_mcp_config_entry():
        print_success("~/.claude.json entry for stm32-docs (manual fallback)")
        removed_count += 1

    # Summary
    print()
    if error_count == 0:
        print(f"{Colors.GREEN}{'='*60}{Colors.RESET}")
        print(f"{Colors.GREEN}{'Cleanup Complete!'.center(60)}{Colors.RESET}")
        print(f"{Colors.GREEN}{'='*60}{Colors.RESET}")
        print(f"\n  Removed {removed_count} items ({format_size(total_size)} freed)")
    else:
        print(f"{Colors.YELLOW}{'='*60}{Colors.RESET}")
        print(f"{Colors.YELLOW}{'Cleanup Completed with Errors'.center(60)}{Colors.RESET}")
        print(f"{Colors.YELLOW}{'='*60}{Colors.RESET}")
        print(f"\n  Removed: {removed_count}, Errors: {error_count}")

    # Additional cleanup instructions
    print(f"\n{Colors.BOLD}Complete uninstall steps:{Colors.RESET}")
    print("  1. /plugin uninstall stm32-agents  # Remove plugin from Claude Code")
    print("  2. pip uninstall stm32-mcp-docs    # Remove Python package (optional)")
    print("  3. uv cache clean                  # Clear uv cache (optional)")

    return error_count == 0


def main():
    """Main entry point."""
    parser = argparse.ArgumentParser(
        description="STM32 MCP Documentation Server - Database Cleanup",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Complete Uninstall Steps:
  1. /plugin uninstall stm32-agents   # Remove plugin (agents, commands, MCP)
  2. stm32-uninstall                  # Clean up database
  3. pip uninstall stm32-mcp-docs     # Remove Python package (optional)

This script only removes the ChromaDB database and legacy marker files.
The Claude Code plugin system handles agent and command cleanup.

Examples:
  stm32-uninstall                # Interactive cleanup
  stm32-uninstall --yes          # Non-interactive (auto-confirm)
  stm32-uninstall --dry-run      # Show what would be removed
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
        yes=args.yes
    )

    return 0 if success else 1


if __name__ == "__main__":
    sys.exit(main())
