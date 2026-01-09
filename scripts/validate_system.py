#!/usr/bin/env python3
"""
Validate the complete STM32 MCP Documentation System.

This script performs end-to-end validation of all system components:
- Project structure
- Module imports
- Configuration
- Database connectivity
- Search functionality

Usage:
    python scripts/validate_system.py [--verbose]
"""

import sys
from pathlib import Path
from typing import Tuple, Any

# Add project root to path
sys.path.insert(0, str(Path(__file__).parent.parent))

PROJECT_ROOT = Path(__file__).parent.parent

# Try to import rich for pretty output
try:
    from rich.console import Console
    from rich.table import Table
    from rich.panel import Panel
    RICH_AVAILABLE = True
except ImportError:
    RICH_AVAILABLE = False

if RICH_AVAILABLE:
    console = Console()
else:
    # Fallback console for when rich is not available
    class FallbackConsole:
        def print(self, *args, **kwargs):
            # Strip rich markup for plain text output
            text = str(args[0]) if args else ""
            # Remove common rich markup
            import re
            text = re.sub(r'\[.*?\]', '', text)
            print(text)

    console = FallbackConsole()


def check_structure() -> Tuple[bool, str]:
    """Check project structure."""
    required = [
        "mcp_server/server.py",
        "mcp_server/config.py",
        "mcp_server/tools/search.py",
        "mcp_server/resources/handlers.py",
        "pipeline/chunker.py",
        "pipeline/validator.py",
        "storage/chroma_store.py",
        "storage/metadata.py",
        "scripts/ingest_docs.py",
        ".mcp.json",  # Project-scoped MCP config at project root
    ]

    missing = [f for f in required if not (PROJECT_ROOT / f).exists()]
    if missing:
        return False, f"Missing: {', '.join(missing[:3])}{'...' if len(missing) > 3 else ''}"
    return True, "All files present"


def check_imports() -> Tuple[bool, str]:
    """Check if all modules import correctly."""
    try:
        from mcp_server.server import mcp
        from mcp_server.config import settings
        from pipeline.chunker import STM32Chunker
        from storage.chroma_store import STM32ChromaStore
        from storage.metadata import ChunkMetadataSchema
        return True, "All imports successful"
    except ImportError as e:
        return False, str(e)[:60]


def check_config() -> Tuple[bool, str]:
    """Check configuration."""
    try:
        from mcp_server.config import settings
        return True, f"Mode: {settings.SERVER_MODE.value}, Port: {settings.PORT}"
    except Exception as e:
        return False, str(e)[:60]


def check_database() -> Tuple[bool, str]:
    """Check if documentation is indexed."""
    try:
        from storage.chroma_store import STM32ChromaStore
        from mcp_server.config import settings

        if not settings.CHROMA_DB_PATH.exists():
            return False, "Database directory does not exist"

        store = STM32ChromaStore(settings.CHROMA_DB_PATH)
        count = store.count()
        if count > 0:
            return True, f"{count} chunks indexed"
        else:
            return False, "No data - run ingest_docs.py"
    except Exception as e:
        return False, str(e)[:60]


def check_search() -> Tuple[bool, str]:
    """Check if search works."""
    try:
        from storage.chroma_store import STM32ChromaStore
        from mcp_server.config import settings

        if not settings.CHROMA_DB_PATH.exists():
            return False, "Database not initialized"

        store = STM32ChromaStore(settings.CHROMA_DB_PATH)
        if store.count() == 0:
            return False, "No data to search"

        results = store.search("GPIO configuration", n_results=1)
        if results:
            return True, f"Search works (score: {results[0]['score']:.2f})"
        return False, "Search returned no results"
    except Exception as e:
        return False, str(e)[:60]


def check_chunker() -> Tuple[bool, str]:
    """Check if chunker works."""
    try:
        from pipeline.chunker import STM32Chunker, ChunkingConfig

        chunker = STM32Chunker(ChunkingConfig())
        sample = "# Test\n\nSample content for testing."
        chunks = chunker.chunk_document(sample, "test.md")

        if chunks:
            return True, f"Chunker works ({len(chunks)} chunks created)"
        return False, "Chunker returned no chunks"
    except Exception as e:
        return False, str(e)[:60]


def check_validator() -> Tuple[bool, str]:
    """Check if validator works."""
    try:
        from pipeline.chunker import STM32Chunker, ChunkingConfig
        from pipeline.validator import ChunkValidator

        chunker = STM32Chunker(ChunkingConfig())
        validator = ChunkValidator()

        sample = "# Test\n\nSample content for testing the validator."
        chunks = chunker.chunk_document(sample, "test.md")
        report = validator.generate_report(chunks)

        return True, f"Validator works (valid: {report.valid_chunks}/{report.total_chunks})"
    except Exception as e:
        return False, str(e)[:60]


def check_mcp_json() -> Tuple[bool, str]:
    """Check MCP configuration file.

    Checks both project-scoped (.mcp.json at project root) and
    user-scoped (~/.claude.json) configurations.
    """
    try:
        import json
        from pathlib import Path

        # Check project-scoped .mcp.json first
        project_mcp = PROJECT_ROOT / ".mcp.json"
        user_mcp = Path.home() / ".claude.json"

        config_found = False
        stm32_configured = False

        if project_mcp.exists():
            config = json.loads(project_mcp.read_text())
            if "mcpServers" in config and "stm32-docs" in config["mcpServers"]:
                return True, "MCP config valid (.mcp.json)"
            config_found = True

        if user_mcp.exists():
            config = json.loads(user_mcp.read_text())
            if "mcpServers" in config and "stm32-docs" in config.get("mcpServers", {}):
                return True, "MCP config valid (~/.claude.json)"
            config_found = True

        if not config_found:
            return False, "No MCP config found (.mcp.json or ~/.claude.json)"

        return False, "stm32-docs not configured in any MCP config"
    except json.JSONDecodeError as e:
        return False, f"Invalid JSON: {str(e)[:40]}"
    except Exception as e:
        return False, str(e)[:60]


def check_markdown_docs() -> Tuple[bool, str]:
    """Check if markdown documentation exists."""
    try:
        from mcp_server.config import settings

        docs_dir = settings.RAW_DOCS_DIR
        if not docs_dir.exists():
            return False, f"Docs dir missing: {docs_dir.name}"

        md_files = list(docs_dir.glob("*.md"))
        if not md_files:
            return False, "No markdown files found"

        return True, f"{len(md_files)} markdown files found"
    except Exception as e:
        return False, str(e)[:60]


def main():
    """Run all validation checks."""
    if RICH_AVAILABLE:
        console.print(Panel.fit(
            "[bold blue]STM32 MCP System Validation[/bold blue]",
            subtitle=f"Project: {PROJECT_ROOT.name}"
        ))
    else:
        print("=" * 60)
        print("STM32 MCP System Validation")
        print(f"Project: {PROJECT_ROOT.name}")
        print("=" * 60)

    checks = [
        ("Project Structure", check_structure),
        ("Module Imports", check_imports),
        ("Configuration", check_config),
        ("MCP JSON Config", check_mcp_json),
        ("Markdown Docs", check_markdown_docs),
        ("Chunker", check_chunker),
        ("Validator", check_validator),
        ("Database", check_database),
        ("Search", check_search),
    ]

    if RICH_AVAILABLE:
        table = Table()
        table.add_column("Check", style="cyan")
        table.add_column("Status")
        table.add_column("Details")
    else:
        print("\n{:<20} {:<10} {}".format("Check", "Status", "Details"))
        print("-" * 60)

    all_passed = True
    critical_failed = False

    for name, check_fn in checks:
        try:
            passed, details = check_fn()
            if RICH_AVAILABLE:
                status = "[green]PASS[/green]" if passed else "[red]FAIL[/red]"
            else:
                status = "PASS" if passed else "FAIL"
            if not passed:
                all_passed = False
                # Mark as critical if it's an import or structure failure
                if name in ["Project Structure", "Module Imports"]:
                    critical_failed = True
        except Exception as e:
            if RICH_AVAILABLE:
                status = "[red]ERROR[/red]"
            else:
                status = "ERROR"
            details = str(e)[:60]
            all_passed = False

        if RICH_AVAILABLE:
            table.add_row(name, status, str(details)[:60])
        else:
            print("{:<20} {:<10} {}".format(name, status, str(details)[:60]))

    if RICH_AVAILABLE:
        console.print(table)
    print()

    # Summary
    if all_passed:
        if RICH_AVAILABLE:
            console.print("\n[bold green]All checks passed![/bold green]")
        else:
            print("\nAll checks passed!")
        return 0
    elif critical_failed:
        if RICH_AVAILABLE:
            console.print("\n[bold red]Critical checks failed. Please fix before proceeding.[/bold red]")
        else:
            print("\nCritical checks failed. Please fix before proceeding.")
        return 2
    else:
        if RICH_AVAILABLE:
            console.print("\n[yellow]Some checks failed. See details above.[/yellow]")
            console.print("[dim]Hint: Run 'python scripts/ingest_docs.py' to index documentation.[/dim]")
        else:
            print("\nSome checks failed. See details above.")
            print("Hint: Run 'python scripts/ingest_docs.py' to index documentation.")
        return 1


if __name__ == "__main__":
    sys.exit(main())
