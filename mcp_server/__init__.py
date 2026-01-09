"""
STM32 MCP Documentation Server

A Model Context Protocol (MCP) server that provides semantic search
over STM32 microcontroller documentation.

This package contains:
- server.py: Main MCP server implementation (FastMCP-based)
- config.py: Configuration management (Pydantic settings)
- tools/: MCP tool implementations
- resources/: MCP resource handlers
- prompts/: MCP prompt templates

Usage:
    # Start the server (local mode - stdio)
    python -m mcp_server

    # Start in network mode (for Tailscale)
    STM32_SERVER_MODE=network python -m mcp_server

    # Start via installed command
    stm32-docs

    # Start with options
    stm32-docs --mode network --port 8765

Tools exposed:
    - search_stm32_docs: Semantic search across all documentation
    - get_peripheral_docs: Get peripheral-specific documentation
    - get_code_examples: Find code examples for topics
    - get_register_info: Get register documentation
    - list_peripherals: List available peripherals
    - search_hal_function: Search for HAL/LL function documentation
    - lookup_hal_function: Enhanced HAL function lookup
    - troubleshoot_error: Debug STM32 issues
    - get_init_sequence: Get peripheral initialization code
    - get_clock_config: Get clock configuration examples
    - compare_peripheral_options: Compare peripherals
    - get_migration_guide: Migration between STM32 families
    - get_electrical_specifications: Electrical specs lookup
    - get_timing_specifications: Timing specs lookup
    - get_interrupt_code: Interrupt handling examples
    - get_dma_code: DMA configuration examples
    - get_low_power_code: Low power mode examples
    - get_callback_code: HAL callback examples
    - get_init_template: Peripheral init templates

Resources exposed:
    - stm32://stats: Database statistics
    - stm32://peripherals: List peripherals
    - stm32://peripherals/{name}: Peripheral overview
    - stm32://peripherals/{name}/registers: Register documentation
    - stm32://peripherals/{name}/examples: Code examples
    - stm32://peripherals/{name}/interrupts: Interrupt documentation
    - stm32://peripherals/{name}/dma: DMA configuration
    - stm32://sources: List source files
    - stm32://health: Server health status
    - stm32://hal-functions: List HAL functions
    - stm32://hal-functions/{peripheral}: Peripheral HAL functions
    - stm32://documents/{doc_type}: Documents by type

Prompts exposed:
    - debug_peripheral: Debugging assistance for peripheral issues
    - configure_peripheral: Peripheral configuration guidance
    - explain_hal_function: HAL function explanation
    - migration_guide: Help migrating between STM32 families

Network Mode (Tailscale):
    Set STM32_SERVER_MODE=network or STM32_SERVER_MODE=hybrid
    The server will listen on the configured port for HTTP/SSE connections.
    Default: http://0.0.0.0:8765

Quick Start:
    1. Install: pip install -e .
    2. Ingest docs: stm32-ingest
    3. Run server: stm32-docs
    4. Search: stm32-search "UART DMA configuration"
"""

from mcp_server.config import (
    Settings,
    get_settings,
    settings,
    ServerMode,
    LogLevel,
    EmbeddingModel,
    VALID_PERIPHERALS,
    VALID_DOC_TYPES,
    STM32_FAMILIES,
)

__version__ = "1.0.0"
__author__ = "STM32 Agents Team"
__license__ = "MIT"
__email__ = "stm32-agents@example.com"

__all__ = [
    # Version info
    "__version__",
    "__author__",
    "__license__",
    # Configuration
    "settings",
    "Settings",
    "get_settings",
    "ServerMode",
    "LogLevel",
    "EmbeddingModel",
    # Constants
    "VALID_PERIPHERALS",
    "VALID_DOC_TYPES",
    "STM32_FAMILIES",
]
