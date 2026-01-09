"""
MCP Prompts for STM32 Documentation Server

This package contains prompt templates that guide LLM behavior
when working with STM32 documentation.

Prompts:
- debug_peripheral: Debugging assistance for peripheral issues
- configure_peripheral: Peripheral configuration guidance
- code_review: STM32 code review assistance
- migration_help: Help migrating between STM32 families

Usage:
    from mcp_server.prompts.templates import debug_peripheral, configure_peripheral
"""

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from mcp_server.prompts.templates import (
        configure_peripheral,
        debug_peripheral,
    )

__all__ = [
    "debug_peripheral",
    "configure_peripheral",
]
