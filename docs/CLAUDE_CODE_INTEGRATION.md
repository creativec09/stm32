# Claude Code Integration Guide

This guide explains how to configure Claude Code to use the STM32 documentation MCP server for intelligent STM32 development assistance.

## Overview

The STM32 Multi-Agent Development System integrates with Claude Code through the Model Context Protocol (MCP). This enables Claude Code to:

- Search STM32 documentation using semantic search
- Retrieve peripheral-specific documentation
- Look up HAL/LL function signatures and usage
- Get code examples and initialization sequences
- Troubleshoot common errors
- Access clock configuration guides

## Configuration

### Recommended: Using Claude CLI

The recommended way to configure the MCP server is using the Claude CLI:

```bash
claude mcp add stm32-docs -s user -- python -m mcp_server
```

This registers the server at the user level, making it available across all projects.

### Alternative: Project-Level Configuration (`.mcp.json`)

The repository includes a `.mcp.json` file at the project root that Claude Code automatically detects:

```json
{
  "mcpServers": {
    "stm32-docs": {
      "command": "python",
      "args": ["-m", "mcp_server"],
      "env": {
        "STM32_SERVER_MODE": "local",
        "STM32_LOG_LEVEL": "INFO"
      }
    }
  }
}
```

This provides project-scoped access when working in the stm32-agents directory.

### Network Configuration (Tailscale)

For remote access via Tailscale, use the network configuration template in `.claude/mcp-network.json`:

```json
{
  "mcpServers": {
    "stm32-docs": {
      "type": "sse",
      "url": "http://YOUR_TAILSCALE_IP:8765/sse",
      "description": "STM32 documentation server (network mode)"
    }
  }
}
```

To set up network mode:
1. Start the server with `STM32_SERVER_MODE=network python -m mcp_server`
2. Register on client machines: `claude mcp add stm32-docs -s user --type sse --url "http://YOUR_TAILSCALE_IP:8765/sse"`
3. Replace `YOUR_TAILSCALE_IP` with your actual Tailscale IP address

## Available Slash Commands

### `/stm32` - General Documentation Search

Search STM32 documentation for any topic.

```
/stm32 How to configure UART with DMA
/stm32 GPIO interrupt setup
/stm32 ADC continuous conversion
```

### `/stm32-init` - Peripheral Initialization

Get complete initialization code for a peripheral.

```
/stm32-init UART
/stm32-init SPI DMA mode
/stm32-init ADC continuous conversion with interrupt
/stm32-init TIM PWM output
```

### `/stm32-debug` - Debug Assistance

Get help troubleshooting peripheral issues.

```
/stm32-debug UART not receiving data
/stm32-debug I2C HAL_TIMEOUT error
/stm32-debug SPI wrong data order
```

### `/stm32-hal` - HAL Function Lookup

Look up HAL/LL function documentation.

```
/stm32-hal HAL_UART_Transmit
/stm32-hal HAL_SPI_TransmitReceive_DMA
/stm32-hal HAL_GPIO_Init
```

## Using MCP Tools Directly

When the MCP server is connected, Claude Code has access to these tools:

| Tool | Purpose | Example Usage |
|------|---------|---------------|
| `mcp__stm32-docs__search_stm32_docs` | General semantic search | Search for "DMA configuration" |
| `mcp__stm32-docs__get_peripheral_docs` | Peripheral documentation | Get docs for "UART" |
| `mcp__stm32-docs__get_code_examples` | Find code examples | Examples for "SPI DMA" |
| `mcp__stm32-docs__lookup_hal_function` | HAL function lookup | Lookup "HAL_UART_Transmit" |
| `mcp__stm32-docs__troubleshoot_error` | Error troubleshooting | Debug "HAL_TIMEOUT" |
| `mcp__stm32-docs__get_init_sequence` | Initialization code | Init sequence for "I2C" |
| `mcp__stm32-docs__get_clock_config` | Clock configuration | Clock config for "HSE PLL" |
| `mcp__stm32-docs__list_peripherals` | List available peripherals | List all peripherals |
| `mcp__stm32-docs__get_migration_guide` | Migration guidance | Migrate "F4 to H7" |

## MCP Resources

The server also provides resources that can be read:

| Resource URI | Description |
|--------------|-------------|
| `stm32://peripherals/{name}` | Peripheral documentation |
| `stm32://stats` | Server statistics |
| `stm32://sources` | Available documentation sources |

## Tailscale Network Mode Setup

For accessing the MCP server from remote machines via Tailscale:

### 1. Start the Server in Network Mode

```bash
# Set environment variables
export STM32_SERVER_MODE=network
export STM32_HOST=0.0.0.0
export STM32_PORT=8765

# Start the server
python scripts/start_server.py --network
```

### 2. Configure Tailscale

Ensure Tailscale is running on both the server machine and client machine:

```bash
# Check Tailscale status
tailscale status

# Get your Tailscale IP
tailscale ip -4
```

### 3. Update Client Configuration

On the client machine, update `.claude/mcp.json`:

```json
{
  "mcpServers": {
    "stm32-docs": {
      "type": "sse",
      "url": "http://100.x.x.x:8765/sse",
      "description": "STM32 documentation server (network mode)"
    }
  }
}
```

Replace `100.x.x.x` with the actual Tailscale IP of the server machine.

### 4. Verify Connection

```bash
# Test the connection
curl http://100.x.x.x:8765/health
```

## Troubleshooting

### Server Not Starting

1. Check Python environment:
   ```bash
   python --version  # Should be 3.10+
   pip list | grep mcp
   ```

2. Verify dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Check server logs:
   ```bash
   STM32_LOG_LEVEL=DEBUG python mcp_server/server.py
   ```

### Tools Not Appearing in Claude Code

1. Restart Claude Code after adding the MCP server
2. Verify the server is registered: `claude mcp list`
3. Check the module is importable: `python -m mcp_server --help`

### No Search Results

1. Ensure documentation has been indexed:
   ```bash
   python scripts/ingest_docs.py --clear
   ```

2. Verify ChromaDB has data:
   ```bash
   python scripts/verify_mcp.py
   ```

### Network Mode Connection Issues

1. Check Tailscale is connected on both machines
2. Verify firewall allows port 8765
3. Test direct connection:
   ```bash
   curl http://YOUR_TAILSCALE_IP:8765/health
   ```

### Slow Responses

1. First query may be slow due to model loading
2. Subsequent queries should be faster (embeddings cached)
3. Consider reducing `max_results` in queries

## Verification Script

Run the verification script to check your setup:

```bash
python scripts/verify_mcp.py
```

This checks:
- Configuration files exist and are valid
- Server can be imported
- ChromaDB has indexed data
- Slash commands are present

## Environment Variables

| Variable | Default | Description |
|----------|---------|-------------|
| `STM32_SERVER_MODE` | `local` | Server mode: `local` or `network` |
| `STM32_HOST` | `127.0.0.1` | Host to bind (network mode) |
| `STM32_PORT` | `8765` | Port to bind (network mode) |
| `STM32_LOG_LEVEL` | `INFO` | Logging level |
| `CHROMA_DB_PATH` | `./chroma_db` | ChromaDB storage path |

## Best Practices

1. **Always search first**: Use `/stm32` or `search_stm32_docs` before answering STM32 questions
2. **Be specific**: More specific queries yield better results
3. **Use peripheral tools**: For peripheral-specific questions, use `get_peripheral_docs`
4. **Check examples**: Use `get_code_examples` for implementation guidance
5. **Troubleshoot systematically**: Use `troubleshoot_error` for debugging help

## Related Documentation

- [MCP Server Documentation](MCP_SERVER.md)
- [Quick Start Guide](QUICK_START.md)
- [Agent Routing Specification](AGENT_ROUTING_SPECIFICATION.md)
- [Infrastructure Overview](INFRASTRUCTURE.md)
