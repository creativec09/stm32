---
name: stm32-setup
description: Set up STM32 MCP documentation server in your project
---

# STM32 MCP Setup Command

Interactive setup for the STM32 documentation server.

## Usage

```
/stm32-setup                 Full setup with CLAUDE.md update
/stm32-setup --status        Show current installation status
/stm32-setup --update-claude Only update project CLAUDE.md
/stm32-setup --force-db      Force re-download of database
```

## What This Command Does

When you run `/stm32-setup`, the assistant will:

### 1. Check Database Status
- Verify if the STM32 documentation database is installed
- Report the number of indexed document chunks
- Show the database source (downloaded, ingested, or bundled)

### 2. Download Database (if needed)
- Automatically downloads pre-built vector database from GitHub releases
- Shows download progress
- Falls back to local ingestion if download fails

### 3. Update Project CLAUDE.md
- Adds comprehensive STM32 instructions to your project's CLAUDE.md
- Lists all 16 available STM32 agents and their purposes
- Documents all MCP tools (mcp__stm32-docs__*) with usage examples
- Provides best practices for STM32 queries

### 4. Show Installation Summary
- Database status and chunk count
- Installed agents list
- Available slash commands
- Quick start examples

## MCP Tools Used

This command relies on the following MCP tools:

| Tool | Purpose |
|------|---------|
| `mcp__stm32-docs__list_peripherals` | Verify database is working |
| Read resource `stm32://status` | Get server status |
| Read resource `stm32://health` | Check server health |

## Example Output

```
STM32 MCP Setup
===============

Database Status:
  - Status: Ready
  - Chunks: 13,815 document chunks
  - Source: Downloaded from GitHub release v0.1.0

Available Agents (16):
  - router: Query routing and classification
  - firmware: Core firmware development
  - debug: Debugging and troubleshooting
  ... (13 more)

Available Commands:
  - /stm32 <query>
  - /stm32-init <peripheral>
  - /stm32-hal <function>
  - /stm32-debug <issue>
  - /stm32-setup

CLAUDE.md Updated:
  Added STM32 instructions to ./CLAUDE.md

Quick Start:
  Try: /stm32 How do I configure UART with DMA?
```

## Instructions for the Assistant

When the user runs `/stm32-setup`, follow these steps:

1. **Check MCP Server Status**
   - Read the `stm32://status` resource to get database state
   - If status is "setup_required", inform the user

2. **Verify Database**
   - Call `mcp__stm32-docs__list_peripherals()` to verify the database works
   - Report the number of peripherals documented

3. **Update CLAUDE.md**
   - Check if a CLAUDE.md exists in the current project directory
   - If it exists, append STM32 instructions (avoiding duplicates)
   - If it doesn't exist, create it with STM32 instructions
   - Use the content from the STM32 CLAUDE.md template

4. **Show Summary**
   - Report all installed components
   - Provide quick start examples
   - Suggest first queries to try

## CLAUDE.md Template Content

When updating the user's project CLAUDE.md, add the following content:

```markdown
## STM32 Development Instructions

This project uses the STM32 MCP documentation server for embedded development assistance.

### IMPORTANT: Always Use MCP Tools for STM32 Questions

When answering ANY question about STM32 development:
1. ALWAYS search the documentation first using MCP tools
2. NEVER rely solely on training knowledge for STM32-specific details
3. Verify register names, function signatures, and configurations

### Available MCP Tools

| Tool | When to Use |
|------|-------------|
| `mcp__stm32-docs__search_stm32_docs` | General documentation search |
| `mcp__stm32-docs__get_peripheral_docs` | Peripheral-specific documentation |
| `mcp__stm32-docs__get_code_examples` | Find working code examples |
| `mcp__stm32-docs__get_register_info` | Register and bit field details |
| `mcp__stm32-docs__lookup_hal_function` | HAL/LL function documentation |
| `mcp__stm32-docs__troubleshoot_error` | Debug issues and errors |
| `mcp__stm32-docs__get_init_sequence` | Peripheral initialization code |
| `mcp__stm32-docs__get_clock_config` | Clock configuration examples |
| `mcp__stm32-docs__compare_peripheral_options` | Compare peripherals/modes |
| `mcp__stm32-docs__get_migration_guide` | Migration between STM32 families |
| `mcp__stm32-docs__get_interrupt_code` | Interrupt handling examples |
| `mcp__stm32-docs__get_dma_code` | DMA configuration examples |
| `mcp__stm32-docs__get_low_power_code` | Low power mode examples |
| `mcp__stm32-docs__get_callback_code` | HAL callback implementations |
| `mcp__stm32-docs__get_init_template` | Complete init templates |
| `mcp__stm32-docs__list_peripherals` | List documented peripherals |

### Available Slash Commands

- `/stm32 <query>` - Search STM32 documentation
- `/stm32-init <peripheral>` - Get initialization code
- `/stm32-hal <function>` - Look up HAL function
- `/stm32-debug <issue>` - Troubleshoot an issue
- `/stm32-setup` - Run setup and show status

### Available STM32 Agents

| Agent | Purpose |
|-------|---------|
| router | Query classification and routing |
| triage | Initial query analysis |
| firmware | General firmware development |
| firmware-core | Core HAL/LL, timers, DMA, interrupts |
| debug | Debugging and troubleshooting |
| bootloader | Bootloader development |
| bootloader-programming | Bootloader protocols |
| peripheral-comm | UART, SPI, I2C, CAN, USB |
| peripheral-analog | ADC, DAC, OPAMP, comparators |
| peripheral-graphics | LTDC, DMA2D, DCMI, TouchGFX |
| power | Power optimization |
| power-management | Sleep, Stop, Standby modes |
| safety | Safety-critical development |
| safety-certification | IEC 61508, ISO 26262 |
| security | Secure boot, TrustZone, crypto |
| hardware-design | PCB design, EMC, thermal |

### Best Practices

1. **Be specific in queries**
   - Good: "How to configure UART2 with DMA RX on STM32F4?"
   - Bad: "UART not working"

2. **Include context**
   - Mention STM32 family when relevant (F4, H7, G4, etc.)
   - Specify HAL vs LL preference
   - Include error messages exactly

3. **Use appropriate tools**
   - For code: `get_code_examples` or `get_init_sequence`
   - For errors: `troubleshoot_error`
   - For functions: `lookup_hal_function`

4. **Verify before using**
   - Always confirm register names match your specific chip
   - Check HAL library version compatibility
```
