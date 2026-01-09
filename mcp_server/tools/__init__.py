"""
MCP Tools for STM32 Documentation Server

This package contains all tool implementations exposed via MCP protocol.

Tools:
- search.py: Advanced documentation search tools
    - search_hal_function: HAL/LL function documentation lookup
    - search_error_solution: Error troubleshooting search
    - search_initialization_sequence: Peripheral initialization code
    - search_clock_configuration: Clock tree configuration
    - compare_peripherals: Compare two peripherals
    - search_migration_info: Migration guide between families
    - search_electrical_specs: Electrical specifications
    - search_timing_info: Timing specifications

- examples.py: Code example tools
    - get_interrupt_example: Interrupt handling examples
    - get_dma_example: DMA configuration examples
    - get_low_power_example: Low power mode examples
    - get_callback_example: HAL callback examples
    - get_peripheral_init_template: Complete init templates

Usage:
    from mcp_server.tools import search, examples

    # Use search tools
    result = search.search_hal_function(store, "HAL_UART_Transmit")

    # Use example tools
    result = examples.get_interrupt_example(store, "UART")
"""

# Use relative imports for package structure compatibility
from . import search, examples

# Export search functions
from .search import (
    search_hal_function,
    search_error_solution,
    search_initialization_sequence,
    search_clock_configuration,
    compare_peripherals,
    search_migration_info,
    search_electrical_specs,
    search_timing_info,
)

# Export example functions
from .examples import (
    get_interrupt_example,
    get_dma_example,
    get_low_power_example,
    get_callback_example,
    get_peripheral_init_template,
)

__all__ = [
    # Modules
    "search",
    "examples",
    # Search functions
    "search_hal_function",
    "search_error_solution",
    "search_initialization_sequence",
    "search_clock_configuration",
    "compare_peripherals",
    "search_migration_info",
    "search_electrical_specs",
    "search_timing_info",
    # Example functions
    "get_interrupt_example",
    "get_dma_example",
    "get_low_power_example",
    "get_callback_example",
    "get_peripheral_init_template",
]
