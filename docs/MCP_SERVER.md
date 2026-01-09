# STM32 Documentation MCP Server

This document describes the Model Context Protocol (MCP) server that provides semantic search over STM32 documentation.

## Overview

The STM32 MCP Server exposes STM32 documentation through the MCP protocol, allowing Claude Code agents and other MCP clients to search and retrieve relevant documentation during development tasks.

### Key Features

- **Semantic Search**: Vector-based search using sentence transformers for natural language queries
- **Peripheral Filtering**: Filter results by specific STM32 peripherals (GPIO, UART, SPI, etc.)
- **Code Examples**: Dedicated tools for finding code examples
- **Register Documentation**: Look up specific register information
- **Auto-Installation**: On first run, auto-installs agents and builds vector database
- **Dual Transport Modes**: Local (stdio) for Claude Code, Network (HTTP/SSE) for Tailscale

## Installation

### Recommended: uvx Installation

```bash
# One command installs everything
claude mcp add stm32-docs -s user -- uvx --from git+https://TOKEN@github.com/creativec09/stm32-agents.git stm32-mcp-docs
```

Replace `TOKEN` with your GitHub Personal Access Token.

### What Auto-Installs on First Run

1. **16 STM32 agents** copied to `~/.claude/agents/`
2. **Vector database** (13,815 chunks) built from 80 bundled markdown docs
3. **Marker files** created to prevent re-installation

First run takes 5-10 minutes. Subsequent starts are instant.

## Architecture

```
                                    +-------------------+
                                    |   Claude Code     |
                                    |   (MCP Client)    |
                                    +--------+----------+
                                             |
                          +------------------+------------------+
                          |                                     |
                   Local Mode (stdio)                   Network Mode (HTTP/SSE)
                          |                                     |
                          v                                     v
              +-----------+-----------+            +------------+-----------+
              |                       |            |                        |
              |   STM32 MCP Server    |            |    STM32 MCP Server    |
              |   (FastMCP + stdio)   |            |   (FastMCP + Starlette)|
              |                       |            |                        |
              +-----------+-----------+            +------------+-----------+
                          |                                     |
                          +------------------+------------------+
                                             |
                                             v
                                  +----------+----------+
                                  |                     |
                                  |   ChromaDB Store    |
                                  |   (Vector Database) |
                                  |                     |
                                  +---------------------+
```

## Server Modes

### Local Mode (stdio)

Default mode for local Claude Code integration. Uses standard input/output for MCP communication.

```bash
# Automatic via uvx
claude mcp add stm32-docs -s user -- uvx --from git+https://TOKEN@github.com/creativec09/stm32-agents.git stm32-mcp-docs

# Or manually
python -m mcp_server
```

**Use case**: Direct integration with Claude Code on the same machine.

### Network Mode (HTTP/SSE)

HTTP server with Server-Sent Events (SSE) for remote access via Tailscale.

```bash
# Start in network mode
STM32_SERVER_MODE=network python -m mcp_server --port 8765
```

**Use case**: Access from remote machines over Tailscale network.

## Tools (15+)

Tools are the primary interface for querying documentation.

### search_stm32_docs

Primary semantic search across all documentation.

**Parameters:**
| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| query | string | required | Natural language query |
| num_results | int | 5 | Number of results (1-20) |
| peripheral | string | "" | Filter by peripheral name |
| require_code | bool | false | Only return code examples |

**Examples:**
```
search_stm32_docs("How to configure UART for 115200 baud")
search_stm32_docs("DMA configuration", peripheral="DMA")
search_stm32_docs("GPIO toggle example", require_code=True)
```

### get_peripheral_docs

Get comprehensive documentation for a specific peripheral.

**Parameters:**
| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| peripheral | string | required | Peripheral name (GPIO, UART, etc.) |
| topic | string | "" | Specific topic within peripheral |
| include_code | bool | true | Include code examples |

**Examples:**
```
get_peripheral_docs("UART")
get_peripheral_docs("GPIO", topic="interrupt")
get_peripheral_docs("DMA", topic="circular mode")
```

### get_code_examples

Find code examples for a specific topic.

**Parameters:**
| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| topic | string | required | Topic to find examples for |
| peripheral | string | "" | Optional peripheral filter |
| num_examples | int | 3 | Number of examples (1-10) |

**Examples:**
```
get_code_examples("UART transmit")
get_code_examples("PWM configuration", peripheral="TIM")
get_code_examples("ADC continuous mode")
```

### get_register_info

Get detailed register documentation.

**Parameters:**
| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| register_name | string | required | Register name |

**Examples:**
```
get_register_info("GPIOx_MODER")
get_register_info("TIMx_CR1")
get_register_info("RCC_CFGR")
```

### lookup_hal_function

Enhanced HAL/LL function documentation lookup.

**Parameters:**
| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| function_name | string | required | HAL/LL function name |

**Examples:**
```
lookup_hal_function("HAL_GPIO_Init")
lookup_hal_function("HAL_UART_Transmit_DMA")
lookup_hal_function("LL_TIM_SetCounter")
lookup_hal_function("__HAL_RCC_GPIOA_CLK_ENABLE")
```

### troubleshoot_error

Search for solutions to STM32 errors and issues.

**Parameters:**
| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| error_description | string | required | Error message or symptom |
| peripheral | string | "" | Optional peripheral focus |

**Examples:**
```
troubleshoot_error("UART not receiving data")
troubleshoot_error("HAL_TIMEOUT error", peripheral="I2C")
troubleshoot_error("HardFault after DMA transfer")
```

### get_init_sequence

Get complete initialization sequence for a peripheral.

**Parameters:**
| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| peripheral | string | required | Peripheral to initialize |
| use_case | string | "" | Specific use case |

**Examples:**
```
get_init_sequence("UART")
get_init_sequence("SPI", use_case="DMA master mode")
get_init_sequence("ADC", use_case="continuous conversion")
get_init_sequence("TIM", use_case="PWM output")
```

### get_clock_config

Get clock configuration documentation.

**Parameters:**
| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| target_frequency | string | "" | Target system clock frequency |
| clock_source | string | "" | Clock source (HSE, HSI, PLL, etc.) |

**Examples:**
```
get_clock_config("168MHz", "HSE")
get_clock_config("480MHz")
get_clock_config(clock_source="PLL")
```

### compare_peripheral_options

Compare two peripherals or modes.

**Parameters:**
| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| peripheral1 | string | required | First peripheral |
| peripheral2 | string | required | Second peripheral |
| aspect | string | "" | Aspect to compare |

**Examples:**
```
compare_peripheral_options("UART", "USART")
compare_peripheral_options("SPI", "I2C", aspect="speed")
compare_peripheral_options("DMA", "BDMA")
```

### get_migration_guide

Get migration information between STM32 families.

**Parameters:**
| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| from_family | string | required | Source STM32 family |
| to_family | string | required | Target STM32 family |
| peripheral | string | "" | Peripheral focus |

**Examples:**
```
get_migration_guide("STM32F4", "STM32H7")
get_migration_guide("STM32F7", "STM32H7", peripheral="DMA")
```

### get_interrupt_code

Get interrupt handling examples for a peripheral.

**Parameters:**
| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| peripheral | string | required | Peripheral |
| interrupt_type | string | "" | Specific interrupt type |

**Examples:**
```
get_interrupt_code("UART")
get_interrupt_code("TIM", interrupt_type="update")
get_interrupt_code("EXTI", interrupt_type="rising edge")
```

### get_dma_code

Get DMA configuration examples for a peripheral.

**Parameters:**
| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| peripheral | string | required | Peripheral |
| direction | string | "" | Transfer direction (TX, RX, both) |

**Examples:**
```
get_dma_code("UART")
get_dma_code("SPI", direction="TX")
get_dma_code("ADC", direction="RX")
```

### get_low_power_code

Get low power mode examples.

**Parameters:**
| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| mode | string | "" | Low power mode (Sleep, Stop, Standby) |

**Examples:**
```
get_low_power_code()
get_low_power_code("Sleep")
get_low_power_code("Stop")
```

### get_callback_code

Get HAL callback function examples.

**Parameters:**
| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| peripheral | string | required | Peripheral |
| callback_type | string | "" | Callback type (TxCplt, RxCplt, Error) |

**Examples:**
```
get_callback_code("UART")
get_callback_code("SPI", callback_type="TxRxCplt")
get_callback_code("I2C", callback_type="Error")
```

### get_init_template

Get a complete peripheral initialization template.

**Parameters:**
| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| peripheral | string | required | Peripheral |
| mode | string | "" | Specific mode or configuration |

**Examples:**
```
get_init_template("SPI")
get_init_template("SPI", mode="master")
get_init_template("TIM", mode="PWM")
```

### list_peripherals

List all available peripherals with documentation coverage.

**Parameters:** None

**Returns:** List of peripherals with chunk counts.

## Resources

Resources provide direct access to documentation via URI schemes.

### stm32://status

Get server status and database statistics.

**Returns:** JSON with:
- server_name: Server name
- version: Server version
- total_chunks: Total indexed chunks
- agents_installed: Whether agents are installed
- database_ready: Whether database is ready

### stm32://health

Get server health status.

**Returns:** JSON with:
- status: "healthy" or "unhealthy"
- chunks_indexed: Number of indexed chunks
- agents: Number of installed agents

### stm32://stats

Get database statistics including chunk counts and distributions.

**Returns:** JSON with:
- total_chunks: Total indexed chunks
- peripheral_distribution: Chunks per peripheral
- doc_type_distribution: Chunks per document type

### stm32://peripherals

List all documented peripherals with coverage information.

### stm32://peripherals/{peripheral}

Get overview documentation for a specific peripheral.

**Example:** `stm32://peripherals/GPIO`

### stm32://sources

List all documentation source files.

## Configuration

Configuration via environment variables or `.env` file:

### Key Settings

| Variable | Default | Description |
|----------|---------|-------------|
| STM32_SERVER_MODE | local | Server mode: local, network |
| STM32_HOST | 0.0.0.0 | Host to bind (network mode) |
| STM32_PORT | 8765 | Port (network mode) |
| STM32_COLLECTION_NAME | stm32_docs | ChromaDB collection name |
| STM32_EMBEDDING_MODEL | all-MiniLM-L6-v2 | Sentence transformer model |
| STM32_LOG_LEVEL | INFO | Logging level |
| STM32_MAX_SEARCH_RESULTS | 20 | Maximum search results |

### Example .env

```env
STM32_SERVER_MODE=network
STM32_HOST=0.0.0.0
STM32_PORT=8765
STM32_LOG_LEVEL=INFO
STM32_EMBEDDING_MODEL=all-MiniLM-L6-v2
```

## Auto-Installed Agents

On first run, 16 specialized agents are installed to `~/.claude/agents/`:

| Agent | Domain |
|-------|--------|
| router | Query routing |
| triage | Initial query analysis |
| firmware | General firmware |
| firmware-core | HAL/LL, timers, DMA |
| debug | Debugging |
| bootloader | Bootloader development |
| bootloader-programming | IAP, DFU protocols |
| peripheral-comm | UART, SPI, I2C, CAN, USB |
| peripheral-analog | ADC, DAC, OPAMP |
| peripheral-graphics | LTDC, DMA2D, TouchGFX |
| power | Power optimization |
| power-management | Sleep, Stop, Standby |
| safety | Safety-critical development |
| safety-certification | IEC 61508, ISO 26262 |
| security | Secure boot, TrustZone |
| hardware-design | PCB, EMC, thermal |

## Tailscale Integration

For remote access via Tailscale:

1. **Start in Network Mode**:
   ```bash
   export STM32_SERVER_MODE=network
   export STM32_HOST=0.0.0.0
   export STM32_PORT=8765
   python -m mcp_server
   ```

2. **Configure Client**:
   ```bash
   claude mcp add stm32-docs -s user --type sse --url "http://YOUR_TAILSCALE_IP:8765/sse"
   ```

### Network Endpoints

| Endpoint | Description |
|----------|-------------|
| `/` | Server information |
| `/health` | Health check |
| `/sse` | SSE connection for MCP |
| `/messages` | MCP message endpoint |

## Troubleshooting

### Server Won't Start

1. Check uv is installed: `uv --version`
2. Verify registration: `claude mcp list`
3. Check server status: `claude mcp status stm32-docs`

### No Search Results

Database builds on first run. Wait 5-10 minutes for auto-ingestion, or:
```bash
python scripts/ingest_docs.py --clear
```

### Slow First Query

First query triggers embedding model loading and database connection. Subsequent queries are fast (<100ms).

### Network Mode Connection Issues

1. Check server is listening: `curl http://localhost:8765/health`
2. Check Tailscale connectivity: `tailscale ping <hostname>`
3. Verify firewall allows port: `sudo ufw allow 8765`

## Performance Characteristics

| Metric | Value |
|--------|-------|
| First Run | 5-10 minutes |
| Subsequent Starts | <5 seconds |
| Query Response | <100ms (warm) |
| Database Size | ~500MB |
| Total Chunks | 13,815 |
| Documentation Files | 80 |

## Related Documentation

- [Getting Started](GETTING_STARTED.md) - Setup guide
- [Claude Code Integration](CLAUDE_CODE_INTEGRATION.md) - Integration guide
- [Advanced Tools](ADVANCED_TOOLS.md) - Detailed tool reference
- [Resources](RESOURCES.md) - Resource URI reference
