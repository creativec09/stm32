#!/usr/bin/env python3
"""
STM32 MCP Documentation Server - Module Entry Point

This module allows running the MCP server directly via:
    python -m mcp_server

This is equivalent to running:
    python mcp_server/server.py

Or the installed command:
    stm32-docs

Usage:
    # Start with default configuration
    python -m mcp_server

    # Start in local mode (stdio)
    STM32_SERVER_MODE=local python -m mcp_server

    # Start in network mode (HTTP/SSE for Tailscale)
    STM32_SERVER_MODE=network python -m mcp_server

Environment Variables:
    STM32_SERVER_MODE: local, network, or hybrid (default)
    STM32_HOST: Host to bind for network mode (default: 0.0.0.0)
    STM32_PORT: Port for network mode (default: 8765)
    STM32_LOG_LEVEL: Logging level (DEBUG, INFO, WARNING, ERROR)

For more options, use the CLI:
    stm32-docs --help
"""

from mcp_server.server import main

if __name__ == "__main__":
    main()
