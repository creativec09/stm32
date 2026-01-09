# Getting Started with STM32 MCP Documentation Server

This guide walks you through setting up and using the STM32 documentation server.

## Overview

The STM32 MCP Documentation Server provides semantic search over 80 STM32 reference documents using the Model Context Protocol (MCP). It enables Claude Code to answer questions about STM32 development with accurate, source-backed responses.

**Key Features:**
- One-command installation via `uvx`
- Auto-installs 16 specialized STM32 agents
- Auto-builds vector database (13,815 chunks) on first run
- No hardcoded paths - fully portable

## Prerequisites

### Required Software

- **Python 3.11 or higher** - Check with `python --version`
- **Claude Code CLI** - The official Claude desktop application
- **uv** (for uvx installation) - Install with `curl -LsSf https://astral.sh/uv/install.sh | sh`

### System Requirements

- **RAM**: 4GB minimum, 8GB recommended
- **Disk Space**: ~500MB for vector database
- **OS**: Linux, macOS, or Windows with WSL2

## Quick Start - One Command Install

### Step 1: Install the MCP Server

```bash
# For private repository - include your GitHub token
claude mcp add stm32-docs -s user -- uvx --from git+https://TOKEN@github.com/creativec09/stm32-agents.git stm32-mcp-docs
```

Replace `TOKEN` with your GitHub Personal Access Token (requires `repo` scope).

### Step 2: Restart Claude Code

Restart Claude Code to load the new MCP server.

### Step 3: First Run Auto-Setup

On the first query, the server automatically:
1. **Installs 16 agents** to `~/.claude/agents/`
2. **Builds vector database** from 80 bundled STM32 documents (5-10 minutes)
3. **Creates marker files** to prevent re-installation

You'll see progress logs during initial setup. Subsequent starts are instant.

### Step 4: Start Using

Use slash commands:
```
/stm32 How do I configure UART with DMA?
/stm32-init SPI master mode at 10MHz
/stm32-hal HAL_GPIO_Init parameters
/stm32-debug UART not receiving data
```

Or ask naturally:
```
"Show me how to configure GPIO interrupts on STM32H7"
"Why is my I2C peripheral returning HAL_TIMEOUT?"
```

## What Gets Auto-Installed

### Agents (16 total)

Auto-installed to `~/.claude/agents/`:

| Agent | Purpose |
|-------|---------|
| `router`, `triage` | Query routing and classification |
| `firmware`, `firmware-core` | Firmware development |
| `debug` | Debugging and troubleshooting |
| `bootloader`, `bootloader-programming` | Bootloader development |
| `peripheral-comm` | UART, SPI, I2C, CAN, USB |
| `peripheral-analog` | ADC, DAC, OPAMP |
| `peripheral-graphics` | LTDC, DMA2D, TouchGFX |
| `power`, `power-management` | Power optimization |
| `safety`, `safety-certification` | Safety-critical development |
| `security` | Secure boot, TrustZone |
| `hardware-design` | PCB design, EMC |

### Vector Database

- **13,815 chunks** from 80 STM32 documents
- Auto-built on first run using bundled markdown files
- Stored in user's data directory (portable)

## Alternative Installation Methods

### Development Install (Clone Repository)

For contributing or modifying the server:

```bash
# Clone the repository
git clone https://github.com/creativec09/stm32-agents.git
cd stm32-agents

# Create virtual environment
python -m venv .venv
source .venv/bin/activate  # Linux/macOS
# .venv\Scripts\activate   # Windows

# Install in development mode
pip install -e .

# Register with Claude Code
claude mcp add stm32-docs -s user -- python -m mcp_server
```

### pip Install

```bash
# Install from GitHub
pip install git+https://TOKEN@github.com/creativec09/stm32-agents.git

# Register with Claude Code
claude mcp add stm32-docs -s user -- python -m mcp_server
```

### Manual MCP Configuration

If the `claude` CLI is not available, add to `~/.claude.json`:

```json
{
  "mcpServers": {
    "stm32-docs": {
      "command": "uvx",
      "args": ["--from", "git+https://TOKEN@github.com/creativec09/stm32-agents.git", "stm32-mcp-docs"]
    }
  }
}
```

## Available MCP Tools

The server provides 15+ tools for STM32 documentation:

| Tool | Description |
|------|-------------|
| `search_stm32_docs` | Semantic search across all documentation |
| `get_peripheral_docs` | Peripheral-specific documentation |
| `get_code_examples` | Find code examples |
| `get_register_info` | Register bit field documentation |
| `lookup_hal_function` | HAL/LL function lookup |
| `troubleshoot_error` | Error troubleshooting |
| `get_init_sequence` | Initialization code |
| `get_clock_config` | Clock configuration |
| `compare_peripheral_options` | Compare peripherals |
| `get_migration_guide` | Migration between STM32 families |
| `get_interrupt_code` | Interrupt handling |
| `get_dma_code` | DMA configuration |
| `get_low_power_code` | Low power modes |
| `get_callback_code` | HAL callbacks |
| `get_init_template` | Complete init templates |
| `list_peripherals` | List documented peripherals |

### MCP Resources

| Resource URI | Description |
|--------------|-------------|
| `stm32://status` | Server status and statistics |
| `stm32://health` | Health check |
| `stm32://peripherals` | List of peripherals |
| `stm32://stats` | Database statistics |

## Slash Commands

### `/stm32` - General Documentation Search

```
/stm32 How to configure UART with DMA
/stm32 GPIO interrupt setup
/stm32 ADC continuous conversion
```

### `/stm32-init` - Peripheral Initialization

```
/stm32-init UART
/stm32-init SPI DMA mode
/stm32-init TIM PWM output
```

### `/stm32-debug` - Debug Assistance

```
/stm32-debug UART not receiving data
/stm32-debug I2C HAL_TIMEOUT error
/stm32-debug SPI wrong data order
```

### `/stm32-hal` - HAL Function Lookup

```
/stm32-hal HAL_UART_Transmit
/stm32-hal HAL_SPI_TransmitReceive_DMA
/stm32-hal HAL_GPIO_Init
```

## Network Mode (Tailscale)

For accessing the server from multiple machines:

### Start Server in Network Mode

```bash
STM32_SERVER_MODE=network python -m mcp_server --port 8765
```

### Configure Client Machines

On client machines, add to Claude Code configuration:

```json
{
  "mcpServers": {
    "stm32-docs": {
      "type": "sse",
      "url": "http://YOUR_TAILSCALE_IP:8765/sse"
    }
  }
}
```

Replace `YOUR_TAILSCALE_IP` with your machine's Tailscale IP address.

## Troubleshooting

### "No documentation found" or 0 chunks

The database may not have been built yet. Wait for auto-ingestion to complete on first run (5-10 minutes), or manually trigger:

```bash
python scripts/ingest_docs.py --clear -v
```

### Server Won't Start

1. Check uv is installed: `uv --version`
2. Verify MCP registration: `claude mcp list`
3. Check logs for errors

### Slow First Request

The first request takes 5-10 minutes as the server:
1. Loads the embedding model
2. Ingests 80 documentation files
3. Builds the vector database

Subsequent requests are fast (<100ms).

### Import Errors

Ensure dependencies are installed:

```bash
# If using uvx, dependencies are automatic
# If using pip install:
pip install -e .
```

### Tools Not Appearing in Claude Code

1. Restart Claude Code after adding the MCP server
2. Verify registration: `claude mcp list`
3. Check server status: `claude mcp status stm32-docs`

## Performance Characteristics

| Metric | Value |
|--------|-------|
| First Run | 5-10 minutes (builds database) |
| Subsequent Starts | <5 seconds |
| Query Response | <100ms (warm) |
| Database Size | ~500MB |
| Total Chunks | 13,815 |
| Documentation Files | 80 |

## Next Steps

1. **Read Agent Guide** - [AGENT_QUICK_REFERENCE.md](AGENT_QUICK_REFERENCE.md) for agent capabilities
2. **Explore Tools** - [ADVANCED_TOOLS.md](ADVANCED_TOOLS.md) for all search tools
3. **Server Details** - [MCP_SERVER.md](MCP_SERVER.md) for server documentation
4. **Full Index** - [INDEX.md](INDEX.md) for complete documentation

## Support

- Check the [Documentation Index](INDEX.md)
- Review [MCP Server Documentation](MCP_SERVER.md)
- See [Claude Code Integration](CLAUDE_CODE_INTEGRATION.md) for advanced setup
