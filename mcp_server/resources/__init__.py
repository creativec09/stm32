"""
MCP Resources for STM32 Documentation Server

This package contains resource handlers that expose documentation
as browsable resources via MCP protocol.

Resource URIs:
    stm32://stats
        Documentation database statistics

    stm32://peripherals
        List all documented peripherals

    stm32://peripherals/{name}
        Peripheral overview (alias for /overview)

    stm32://peripherals/{name}/overview
        Comprehensive peripheral overview

    stm32://peripherals/{name}/registers
        Register documentation for peripheral

    stm32://peripherals/{name}/examples
        Code examples for peripheral

    stm32://peripherals/{name}/interrupts
        Interrupt handling documentation

    stm32://peripherals/{name}/dma
        DMA configuration for peripheral

    stm32://sources
        List all documentation source files

    stm32://hal-functions
        List all HAL functions

    stm32://hal-functions/{peripheral}
        List HAL functions for a peripheral

    stm32://documents/{type}
        Get documents by type (reference_manual, application_note, etc.)

Usage:
    from mcp_server.resources.handlers import DocumentationResources

    resources = DocumentationResources(store)
    overview = resources.get_peripheral_overview("UART")
"""

from mcp_server.resources.handlers import DocumentationResources

__all__ = [
    "DocumentationResources",
]
