#!/usr/bin/env python3
"""
Start the STM32 documentation MCP server.

This script provides a command-line interface to start the MCP server
with configurable options for mode, host, and port.

Usage:
    # Start in default mode (from config)
    python scripts/start_server.py

    # Start in local mode (stdio)
    python scripts/start_server.py --mode local

    # Start in network mode (HTTP/SSE for Tailscale)
    python scripts/start_server.py --mode network --port 8765

    # Start with custom host binding
    python scripts/start_server.py --mode network --host 0.0.0.0 --port 9000

    # Show current configuration
    python scripts/start_server.py --show-config

Environment Variables:
    STM32_SERVER_MODE: Override default mode (local, network, hybrid)
    STM32_HOST: Override default host
    STM32_PORT: Override default port
    STM32_LOG_LEVEL: Set logging level (DEBUG, INFO, WARNING, ERROR)
"""

import sys
import argparse
import logging
import importlib.util
import types
from pathlib import Path

# Add project root to path
PROJECT_ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(PROJECT_ROOT))


def _setup_mcp_server_module():
    """
    Set up the mcp_server module from the mcp_server directory.

    This function ensures the mcp_server package is properly loaded
    into sys.modules for import resolution.
    """
    # Create mcp_server package if not exists
    if 'mcp_server' not in sys.modules:
        mcp_server = types.ModuleType('mcp_server')
        sys.modules['mcp_server'] = mcp_server
    else:
        mcp_server = sys.modules['mcp_server']

    # Load config module
    if 'mcp_server.config' not in sys.modules:
        config_path = PROJECT_ROOT / 'mcp_server' / 'config.py'
        spec = importlib.util.spec_from_file_location('mcp_server.config', config_path)
        config_mod = importlib.util.module_from_spec(spec)
        sys.modules['mcp_server.config'] = config_mod
        mcp_server.config = config_mod
        spec.loader.exec_module(config_mod)

    return sys.modules['mcp_server.config']


def main():
    parser = argparse.ArgumentParser(
        description="Start STM32 MCP Documentation Server",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  %(prog)s                    Start with default configuration
  %(prog)s --mode local       Start in local stdio mode
  %(prog)s --mode network     Start HTTP/SSE server for Tailscale
  %(prog)s --show-config      Display current configuration
        """
    )

    parser.add_argument(
        "--mode", "-m",
        choices=["local", "network", "hybrid"],
        default=None,
        help="Server mode: local (stdio), network (HTTP/SSE), or hybrid"
    )

    parser.add_argument(
        "--port", "-p",
        type=int,
        default=None,
        help="Port for network mode (default: 8765)"
    )

    parser.add_argument(
        "--host", "-H",
        type=str,
        default=None,
        help="Host to bind for network mode (default: 0.0.0.0)"
    )

    parser.add_argument(
        "--log-level", "-l",
        choices=["DEBUG", "INFO", "WARNING", "ERROR"],
        default=None,
        help="Logging level"
    )

    parser.add_argument(
        "--show-config",
        action="store_true",
        help="Show current configuration and exit"
    )

    parser.add_argument(
        "--validate",
        action="store_true",
        help="Validate setup (check database, dependencies) and exit"
    )

    args = parser.parse_args()

    # Import config after parsing args (to allow environment setup)
    # Use helper to handle hyphenated directory name
    config_mod = _setup_mcp_server_module()
    settings = config_mod.settings
    ServerMode = config_mod.ServerMode
    LogLevel = config_mod.LogLevel

    # Override settings if provided via command line
    if args.mode:
        settings.SERVER_MODE = ServerMode(args.mode)
    if args.port:
        settings.PORT = args.port
    if args.host:
        settings.HOST = args.host
    if args.log_level:
        settings.LOG_LEVEL = LogLevel(args.log_level)

    # Handle show-config
    if args.show_config:
        import json
        print("STM32 MCP Server Configuration")
        print("=" * 60)
        print(json.dumps(settings.to_dict(), indent=2))
        print("=" * 60)
        print(f"Network URL: {settings.get_network_url()}")
        print(f"Network enabled: {settings.is_network_enabled()}")
        print(f"Local enabled: {settings.is_local_enabled()}")
        print(f"ChromaDB path: {settings.CHROMA_DB_PATH}")
        print(f"Database exists: {settings.CHROMA_DB_PATH.exists()}")
        return 0

    # Handle validation
    if args.validate:
        return validate_setup(settings)

    # Import and run server
    # Load server module using importlib for hyphenated directory
    server_path = PROJECT_ROOT / 'mcp_server' / 'server.py'
    spec = importlib.util.spec_from_file_location('mcp_server.server', server_path)
    server_mod = importlib.util.module_from_spec(spec)
    sys.modules['mcp_server.server'] = server_mod
    spec.loader.exec_module(server_mod)
    server_mod.main()

    return 0


def validate_setup(settings):
    """Validate the server setup before starting."""
    print("Validating STM32 MCP Server setup...")
    print("=" * 60)

    errors = []
    warnings = []

    # Check directories
    print("\n1. Checking directories...")
    settings.ensure_directories()

    if settings.CHROMA_DB_PATH.exists():
        print(f"   [OK] ChromaDB directory exists: {settings.CHROMA_DB_PATH}")
    else:
        print(f"   [WARN] ChromaDB directory created: {settings.CHROMA_DB_PATH}")
        warnings.append("ChromaDB directory was just created (may be empty)")

    # Check for indexed documents
    print("\n2. Checking indexed documents...")
    try:
        from storage.chroma_store import STM32ChromaStore

        store = STM32ChromaStore(
            persist_dir=settings.CHROMA_DB_PATH,
            collection_name=settings.COLLECTION_NAME,
            embedding_model=settings.EMBEDDING_MODEL
        )
        count = store.count()

        if count > 0:
            print(f"   [OK] Found {count} indexed chunks")
            sources = store.list_sources()
            print(f"   [OK] From {len(sources)} source files")
        else:
            print("   [WARN] No documents indexed")
            warnings.append("No documents indexed. Run ingest_docs.py first.")

    except Exception as e:
        print(f"   [ERROR] Failed to connect to ChromaDB: {e}")
        errors.append(f"ChromaDB connection failed: {e}")

    # Check dependencies
    print("\n3. Checking dependencies...")

    try:
        import mcp
        print(f"   [OK] mcp package installed")
    except ImportError:
        print("   [ERROR] mcp package not installed")
        errors.append("mcp package not installed. Run: pip install mcp")

    try:
        import chromadb
        print(f"   [OK] chromadb package installed")
    except ImportError:
        print("   [ERROR] chromadb package not installed")
        errors.append("chromadb package not installed. Run: pip install chromadb")

    try:
        import sentence_transformers
        print(f"   [OK] sentence-transformers package installed")
    except ImportError:
        print("   [ERROR] sentence-transformers package not installed")
        errors.append("sentence-transformers not installed. Run: pip install sentence-transformers")

    # Network mode checks
    if settings.is_network_enabled():
        print("\n4. Checking network mode dependencies...")

        try:
            import uvicorn
            print(f"   [OK] uvicorn package installed")
        except ImportError:
            print("   [ERROR] uvicorn package not installed")
            errors.append("uvicorn not installed (required for network mode). Run: pip install uvicorn")

        try:
            import starlette
            print(f"   [OK] starlette package installed")
        except ImportError:
            print("   [ERROR] starlette package not installed")
            errors.append("starlette not installed (required for network mode). Run: pip install starlette")

    # Summary
    print("\n" + "=" * 60)
    print("Validation Summary")
    print("=" * 60)

    if errors:
        print(f"\n[ERRORS] ({len(errors)}):")
        for err in errors:
            print(f"  - {err}")

    if warnings:
        print(f"\n[WARNINGS] ({len(warnings)}):")
        for warn in warnings:
            print(f"  - {warn}")

    if not errors and not warnings:
        print("\n[SUCCESS] All checks passed!")
        print("Server is ready to start.")

    if errors:
        print("\n[FAILED] Please fix errors before starting the server.")
        return 1

    return 0


if __name__ == "__main__":
    sys.exit(main())
