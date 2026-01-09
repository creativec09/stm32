---
name: stm32-setup
description: Set up STM32 MCP documentation server - installs dependencies and configures your project
---

# STM32 MCP Setup Command

Interactive setup for the STM32 documentation server. Handles dependency installation and project configuration.

## Usage

```
/stm32-setup                 Full setup (install deps, check MCP, update CLAUDE.md)
/stm32-setup --status        Show current installation status
/stm32-setup --update-claude Only update project CLAUDE.md
/stm32-setup --force-db      Force re-download of database
```

## Instructions for the Assistant

When the user runs `/stm32-setup`, follow these steps IN ORDER:

### Step 1: Check and Install uvx/uv

**CRITICAL: Do this FIRST before anything else.**

1. Check if uvx is available:
   ```bash
   command -v uvx
   ```

2. If uvx is NOT found, install uv:
   ```bash
   curl -LsSf https://astral.sh/uv/install.sh | sh
   ```

3. After installation, update PATH for current session:
   ```bash
   export PATH="$HOME/.local/bin:$PATH"
   ```

4. Verify installation worked:
   ```bash
   ~/.local/bin/uvx --version
   ```

5. If uv installation fails, try pip fallback:
   ```bash
   pip install uv
   ```

6. If all uv methods fail, install the package directly via pip:
   ```bash
   pip install git+https://github.com/creativec09/stm32.git
   ```
   Then tell the user: "Installed via pip. The MCP server will use `python -m mcp_server` instead of uvx."

7. **After installing uvx**, tell the user:
   ```
   ✓ uvx installed successfully!

   ACTION REQUIRED: Please restart Claude Code to connect the MCP server.

   After restarting, run /stm32-setup again to complete configuration.
   ```
   Then STOP - don't continue to other steps until they restart.

### Step 2: Check MCP Server Connection

Only proceed here if uvx was already installed (not just installed in Step 1).

1. Try to read the `stm32://status` resource
2. If connection fails with error, diagnose:
   - "spawn uvx ENOENT" → uvx not in PATH, go back to Step 1
   - "ECONNREFUSED" → MCP server not starting, check logs
   - Other errors → report to user

3. If status shows "setup_required" or database is empty:
   - The database will auto-download on first query
   - Or user can wait for it to initialize

### Step 3: Verify Database

1. Call `mcp__stm32-docs__list_peripherals()` to verify the database works
2. If it returns results, report:
   - Number of peripherals documented
   - Number of chunks indexed
3. If it fails, the database may still be downloading - tell user to wait or try again

### Step 4: Update Project CLAUDE.md

1. Check if a CLAUDE.md exists in the current project directory
2. If it exists, check for existing STM32 section (look for "## STM32 Development Instructions")
3. If no STM32 section exists, append the template content below
4. If it doesn't exist, create it with STM32 instructions

### Step 5: Show Summary

Report to the user:
```
STM32 MCP Setup Complete
========================

Dependencies:
  ✓ uvx installed at ~/.local/bin/uvx

MCP Server:
  ✓ Connected to stm32-docs

Database:
  ✓ 13,815 document chunks indexed
  ✓ 80 source documentation files

Agents Installed: 16
  router, triage, firmware, firmware-core, debug, bootloader,
  bootloader-programming, peripheral-comm, peripheral-analog,
  peripheral-graphics, power, power-management, safety,
  safety-certification, security, hardware-design

Commands Available:
  /stm32 <query>        - Search documentation
  /stm32-init <periph>  - Get initialization code
  /stm32-hal <func>     - Look up HAL function
  /stm32-debug <issue>  - Troubleshoot problems
  /stm32-setup          - This setup command

Quick Start:
  Try: /stm32 How do I configure UART with DMA on STM32F4?
```

## Troubleshooting Decision Tree

If something fails, follow this logic:

```
MCP Connection Failed?
├── "spawn uvx ENOENT" or "uvx not found"
│   └── Install uvx (Step 1) → Tell user to restart Claude Code
├── "ECONNREFUSED"
│   └── Check if Python/pip issues → Try pip install fallback
├── "Authentication" or "404" errors
│   └── Check GitHub access → Repo is public, should work
└── Database empty or missing
    └── Will auto-download on first query, or run /stm32-setup --force-db
```

## MCP Tools Used

| Tool | Purpose |
|------|---------|
| `mcp__stm32-docs__list_peripherals` | Verify database is working |
| Read resource `stm32://status` | Get server status |
| Read resource `stm32://health` | Check server health |

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
