# Claude Code Integration Guide

This guide explains how to configure Claude Code to use the STM32 documentation MCP server.

## Overview

The STM32 MCP Documentation Server integrates with Claude Code through the Model Context Protocol (MCP). This enables Claude Code to:

- Search STM32 documentation using semantic search
- Retrieve peripheral-specific documentation
- Look up HAL/LL function signatures and usage
- Get code examples and initialization sequences
- Troubleshoot common errors
- Access clock configuration guides

## Installation

### Recommended: uvx Installation (One Command)

The simplest way to install is via `uvx`:

```bash
# For private repository - include your GitHub Personal Access Token
claude mcp add stm32-docs -s user -- uvx --from git+https://TOKEN@github.com/creativec09/stm32-agents.git stm32-mcp-docs
```

Replace `TOKEN` with your GitHub PAT (requires `repo` scope).

**What happens on first run:**
1. 16 STM32 agents are auto-installed to `~/.claude/agents/`
2. Vector database (13,815 chunks) is built from 80 bundled docs
3. Marker files prevent re-installation on subsequent runs

First run takes 5-10 minutes. Subsequent starts are instant.

### Alternative: pip Installation

```bash
# Install the package
pip install git+https://TOKEN@github.com/creativec09/stm32-agents.git

# Register with Claude Code
claude mcp add stm32-docs -s user -- python -m mcp_server
```

### Alternative: Development Installation

```bash
# Clone repository
git clone https://github.com/creativec09/stm32-agents.git
cd stm32-agents

# Create virtual environment
python -m venv .venv
source .venv/bin/activate

# Install
pip install -e .

# Register with Claude Code
claude mcp add stm32-docs -s user -- python -m mcp_server
```

### Manual Configuration

If the `claude` CLI is not available, manually edit `~/.claude.json`:

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

## Auto-Installed Agents (16)

On first run, the server automatically installs 16 specialized agents to `~/.claude/agents/`:

| Agent | Domain | Key Topics |
|-------|--------|------------|
| `router` | Triage | Query classification, routing |
| `triage` | Triage | Initial query analysis |
| `firmware` | Core Development | General firmware questions |
| `firmware-core` | Core Development | HAL/LL, timers, DMA, interrupts |
| `debug` | Debugging | HardFault analysis, SWD, trace |
| `bootloader` | Updates | Bootloader development |
| `bootloader-programming` | Updates | IAP, DFU, system bootloader |
| `peripheral-comm` | Communication | UART, SPI, I2C, CAN, USB |
| `peripheral-analog` | Analog | ADC, DAC, OPAMP, comparators |
| `peripheral-graphics` | Display | LTDC, DMA2D, TouchGFX |
| `power` | Power | General power optimization |
| `power-management` | Power | Sleep, Stop, Standby modes |
| `safety` | Certification | Safety-critical development |
| `safety-certification` | Certification | IEC 61508, ISO 26262 |
| `security` | Security | Secure boot, TrustZone, crypto |
| `hardware-design` | PCB/Hardware | EMC, thermal, oscillators |

## Available MCP Tools (15+)

When connected, Claude Code has access to these tools:

| Tool | Purpose | Example Usage |
|------|---------|---------------|
| `search_stm32_docs` | General semantic search | Search for "DMA configuration" |
| `get_peripheral_docs` | Peripheral documentation | Get docs for "UART" |
| `get_code_examples` | Find code examples | Examples for "SPI DMA" |
| `get_register_info` | Register documentation | Info for "GPIOx_MODER" |
| `lookup_hal_function` | HAL function lookup | Lookup "HAL_UART_Transmit" |
| `troubleshoot_error` | Error troubleshooting | Debug "HAL_TIMEOUT" |
| `get_init_sequence` | Initialization code | Init for "I2C" |
| `get_clock_config` | Clock configuration | Clock for "HSE PLL" |
| `compare_peripheral_options` | Compare peripherals | Compare "SPI" vs "I2C" |
| `get_migration_guide` | Migration guidance | Migrate "F4 to H7" |
| `get_interrupt_code` | Interrupt examples | Interrupt for "UART" |
| `get_dma_code` | DMA examples | DMA for "SPI TX" |
| `get_low_power_code` | Low power modes | Enter "Stop mode" |
| `get_callback_code` | HAL callbacks | Callback for "UART TxCplt" |
| `get_init_template` | Init templates | Template for "SPI master" |
| `list_peripherals` | List peripherals | Show all peripherals |

## MCP Resources

| Resource URI | Description |
|--------------|-------------|
| `stm32://status` | Server status and database statistics |
| `stm32://health` | Health check |
| `stm32://peripherals` | List documented peripherals |
| `stm32://peripherals/{name}` | Peripheral overview |
| `stm32://stats` | Database statistics |
| `stm32://sources` | Documentation source files |

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
/stm32-init ADC continuous conversion with interrupt
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

## How Agents Work with MCP Tools

Agents are specialized personas that automatically use MCP tools to answer questions:

1. **User asks question** - "How do I configure UART with DMA?"
2. **Agent selected** - `peripheral-comm` agent activated
3. **MCP tools called** - Agent calls `search_stm32_docs`, `get_dma_code`
4. **Documentation retrieved** - Relevant chunks from vector database
5. **Answer generated** - Agent synthesizes response with code examples

Example flow:
```
User: "Show me how to configure GPIO interrupts"

Agent (firmware-core):
  -> Calls: search_stm32_docs("GPIO interrupt configuration")
  -> Calls: get_code_examples("GPIO interrupt", peripheral="GPIO")
  -> Returns: Documentation + code examples
```

## Network Mode (Tailscale)

For accessing from multiple machines via Tailscale:

### Start Server in Network Mode

```bash
export STM32_SERVER_MODE=network
export STM32_HOST=0.0.0.0
export STM32_PORT=8765
python -m mcp_server
```

### Configure Client Machines

On client machines, register with SSE transport:

```bash
claude mcp add stm32-docs -s user --type sse --url "http://YOUR_TAILSCALE_IP:8765/sse"
```

Or manually add to `~/.claude.json`:

```json
{
  "mcpServers": {
    "stm32-docs": {
      "type": "sse",
      "url": "http://100.x.x.x:8765/sse"
    }
  }
}
```

Replace `100.x.x.x` with your Tailscale IP.

### Verify Connection

```bash
curl http://YOUR_TAILSCALE_IP:8765/health
```

## Troubleshooting

### Server Not Starting

1. Check uv is installed: `uv --version`
2. Verify registration: `claude mcp list`
3. Check server status: `claude mcp status stm32-docs`

### Tools Not Appearing in Claude Code

1. Restart Claude Code after adding the MCP server
2. Verify registration: `claude mcp list`
3. Test manually: `uvx --from git+https://TOKEN@github.com/creativec09/stm32-agents.git stm32-mcp-docs --help`

### No Search Results

The database builds on first run. Wait 5-10 minutes for auto-ingestion, or manually trigger:

```bash
python scripts/ingest_docs.py --clear
```

### Slow First Query

First query triggers:
1. Embedding model loading
2. Database connection
3. (If not done) Documentation ingestion

Subsequent queries are fast (<100ms).

### Network Mode Connection Issues

1. Check Tailscale is connected: `tailscale status`
2. Verify firewall allows port 8765
3. Test direct connection: `curl http://YOUR_TAILSCALE_IP:8765/health`

## Environment Variables

| Variable | Default | Description |
|----------|---------|-------------|
| `STM32_SERVER_MODE` | `local` | Server mode: `local` or `network` |
| `STM32_HOST` | `127.0.0.1` | Host to bind (network mode) |
| `STM32_PORT` | `8765` | Port to bind (network mode) |
| `STM32_LOG_LEVEL` | `INFO` | Logging level |
| `STM32_CHROMA_DB_PATH` | (auto) | ChromaDB storage path |

## Best Practices

1. **Use MCP tools first** - Always search documentation before answering STM32 questions
2. **Be specific** - More specific queries yield better results
3. **Use peripheral filters** - Filter by peripheral for targeted results
4. **Check examples** - Use `get_code_examples` for implementation guidance
5. **Troubleshoot systematically** - Use `troubleshoot_error` for debugging help

## Verification

Check your installation:

```bash
# List registered MCP servers
claude mcp list

# Check server status
claude mcp status stm32-docs

# Test the server directly (if development install)
python scripts/verify_mcp.py
```

## Related Documentation

- [Getting Started](GETTING_STARTED.md) - Setup guide
- [MCP Server](MCP_SERVER.md) - Server documentation
- [Agent Quick Reference](AGENT_QUICK_REFERENCE.md) - Agent capabilities
- [Advanced Tools](ADVANCED_TOOLS.md) - Tool reference
