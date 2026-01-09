---
name: stm32
description: Search and retrieve STM32 documentation
---

# STM32 Documentation Command

Use this command to search STM32 documentation.

## Usage

```
/stm32 <query>
```

## Examples

```
/stm32 How to configure UART with DMA
/stm32 GPIO interrupt setup
/stm32 ADC continuous conversion
/stm32 HAL_SPI_TransmitReceive parameters
```

## What This Does

When invoked, this command uses the stm32-docs MCP server tools:

1. For general queries: Use `search_stm32_docs` tool
2. For peripheral-specific: Use `get_peripheral_docs` tool
3. For code examples: Use `get_code_examples` tool
4. For HAL functions: Use `lookup_hal_function` tool
5. For errors: Use `troubleshoot_error` tool

Always search the documentation before providing answers about STM32 development.

## Available Tools

| Tool | Purpose |
|------|---------|
| `search_stm32_docs` | General semantic search |
| `get_peripheral_docs` | Peripheral documentation |
| `get_code_examples` | Find code examples |
| `lookup_hal_function` | HAL function lookup |
| `troubleshoot_error` | Error troubleshooting |
| `get_init_sequence` | Initialization code |
| `get_clock_config` | Clock configuration |
| `list_peripherals` | List available peripherals |
