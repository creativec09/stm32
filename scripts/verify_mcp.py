#!/usr/bin/env python3
"""Verify MCP server is working correctly."""

import subprocess
import json
import sys
from pathlib import Path
from rich.console import Console
from rich.table import Table

console = Console()
PROJECT_ROOT = Path(__file__).parent.parent

def check_config_files():
    """Check MCP configuration files exist and are valid."""
    checks = []

    # Check mcp.json
    mcp_json = PROJECT_ROOT / ".claude" / "mcp.json"
    if mcp_json.exists():
        try:
            config = json.loads(mcp_json.read_text())
            if "mcpServers" in config and "stm32-docs" in config["mcpServers"]:
                checks.append(("mcp.json", True, "Valid configuration"))
            else:
                checks.append(("mcp.json", False, "Missing stm32-docs server"))
        except json.JSONDecodeError as e:
            checks.append(("mcp.json", False, f"Invalid JSON: {e}"))
    else:
        checks.append(("mcp.json", False, "File not found"))

    # Check commands
    commands_dir = PROJECT_ROOT / ".claude" / "commands"
    if commands_dir.exists():
        for cmd in ["stm32.md", "stm32-init.md", "stm32-debug.md", "stm32-hal.md"]:
            cmd_path = commands_dir / cmd
            if cmd_path.exists():
                checks.append((f"commands/{cmd}", True, "Found"))
            else:
                checks.append((f"commands/{cmd}", False, "Missing"))

    return checks

def check_server_imports():
    """Check if server can be imported."""
    try:
        # Ensure project root is in path
        if str(PROJECT_ROOT) not in sys.path:
            sys.path.insert(0, str(PROJECT_ROOT))

        # Check if mcp_server directory exists
        server_path = PROJECT_ROOT / "mcp_server" / "server.py"
        if not server_path.exists():
            return False, f"Server file not found: {server_path}"

        # Try to import
        from mcp_server.server import mcp, search_stm32_docs
        return True, "Server imports correctly"
    except ImportError as e:
        # Check if it's a missing dependency vs module not found
        error_str = str(e)
        if "mcp_server" in error_str:
            return False, "Module path issue - check PYTHONPATH"
        return False, f"Missing dependency: {e}"

def check_storage():
    """Check if ChromaDB has data."""
    try:
        # Ensure project root is in path
        if str(PROJECT_ROOT) not in sys.path:
            sys.path.insert(0, str(PROJECT_ROOT))

        # Check for chromadb dependency
        try:
            import chromadb
        except ImportError:
            return False, "chromadb not installed - run: pip install chromadb"

        from storage.chroma_store import STM32ChromaStore
        from mcp_server.config import settings

        store = STM32ChromaStore(
            persist_dir=settings.CHROMA_DB_PATH,
            collection_name=settings.COLLECTION_NAME
        )
        count = store.count()
        if count > 0:
            return True, f"{count} chunks indexed"
        else:
            return False, "No data indexed - run ingest_docs.py first"
    except ImportError as e:
        return False, f"Missing module: {e}"
    except Exception as e:
        return False, f"Storage error: {e}"

def main():
    console.print("\n[bold blue]STM32 MCP Server Verification[/bold blue]\n")

    table = Table()
    table.add_column("Check", style="cyan")
    table.add_column("Status")
    table.add_column("Details")

    # Config files
    for name, passed, msg in check_config_files():
        status = "[green]PASS[/green]" if passed else "[red]FAIL[/red]"
        table.add_row(name, status, msg)

    # Server imports
    passed, msg = check_server_imports()
    status = "[green]PASS[/green]" if passed else "[red]FAIL[/red]"
    table.add_row("Server imports", status, msg)

    # Storage
    passed, msg = check_storage()
    status = "[green]PASS[/green]" if passed else "[yellow]WARN[/yellow]"
    table.add_row("Storage/Data", status, msg)

    console.print(table)

    console.print("\n[dim]Run 'python scripts/ingest_docs.py --clear' to index documentation[/dim]")

if __name__ == "__main__":
    main()
