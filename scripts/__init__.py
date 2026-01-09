"""
Scripts for STM32 MCP Documentation Server

Command-line scripts for server management and maintenance.

Available Scripts:
- start_server.py: Launch the MCP server (local or network mode)
- ingest_docs.py: Ingest markdown documentation into ChromaDB
- search.py: Quick search from command line
- test_retrieval.py: Test search quality with sample queries
- validate_system.py: Validate complete system setup
- run_tests.py: Run the test suite
- export_chunks.py: Export chunks to JSON for inspection
- verify_mcp.py: Verify MCP configuration

Installed Commands (after pip install):
    stm32-docs          Start the MCP server
    stm32-ingest        Ingest documentation into database
    stm32-search        Quick search from command line
    stm32-validate      Validate system setup

Usage:
    # Via installed commands (recommended)
    stm32-docs                          # Start server
    stm32-ingest --clear                # Clear and re-ingest
    stm32-search "UART DMA"             # Quick search
    stm32-validate                      # Check system

    # Via Python scripts directly
    python scripts/start_server.py --mode network --port 8765
    python scripts/ingest_docs.py --source-dir ./markdowns
    python scripts/search.py "GPIO toggle" --peripheral GPIO
"""

__version__ = "1.0.0"

__all__: list[str] = []
