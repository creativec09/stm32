# STM32 Documentation MCP Server

This document describes the Model Context Protocol (MCP) server that provides semantic search over STM32 documentation.

## Overview

The STM32 MCP Server exposes STM32 documentation through the MCP protocol, allowing Claude Code agents and other MCP clients to search and retrieve relevant documentation during development tasks.

### Key Features

- **Semantic Search**: Vector-based search using sentence transformers for natural language queries
- **Peripheral Filtering**: Filter results by specific STM32 peripherals (GPIO, UART, SPI, etc.)
- **Code Examples**: Dedicated tools for finding code examples
- **Register Documentation**: Look up specific register information
- **Dual Transport Modes**: Local (stdio) for Claude Code, Network (HTTP/SSE) for Tailscale

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
# Start in local mode
python -m mcp_server.server

# Or explicitly
STM32_SERVER_MODE=local python -m mcp_server.server
```

**Use case**: Direct integration with Claude Code on the same machine.

### Network Mode (HTTP/SSE)

HTTP server with Server-Sent Events (SSE) for remote access via Tailscale.

```bash
# Start in network mode
STM32_SERVER_MODE=network python -m mcp_server.server

# Or with script
python scripts/start_server.py --mode network --port 8765
```

**Use case**: Access from remote machines over Tailscale network.

### Hybrid Mode

Default configuration. Intended for systems that need both modes. Currently defaults to local mode when run directly.

```bash
# In hybrid mode, defaults to local
STM32_SERVER_MODE=hybrid python -m mcp_server.server
```

## Tools

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

### list_peripherals

List all available peripherals with documentation coverage.

**Parameters:** None

**Returns:** List of peripherals with chunk counts.

### search_hal_function

Search for HAL/LL function documentation.

**Parameters:**
| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| function_name | string | required | HAL/LL function name |

**Examples:**
```
search_hal_function("HAL_GPIO_Init")
search_hal_function("HAL_UART_Transmit_DMA")
search_hal_function("LL_TIM_SetCounter")
```

## Resources

Resources provide direct access to documentation via URI schemes.

### stm32://stats

Get database statistics including chunk counts and distributions.

**Returns:** JSON with:
- total_chunks: Total indexed chunks
- collection_name: ChromaDB collection name
- peripheral_distribution: Chunks per peripheral
- doc_type_distribution: Chunks per document type

### stm32://peripherals

List all documented peripherals with coverage information.

### stm32://peripherals/{peripheral}

Get overview documentation for a specific peripheral.

**Example:** `stm32://peripherals/GPIO`

### stm32://sources

List all documentation source files.

### stm32://health

Get server health status.

**Returns:** JSON with:
- status: "healthy" or "unhealthy"
- server: Server name
- version: Server version
- chunks_indexed: Number of indexed chunks

## Prompts

Prompts provide guided assistance templates for common tasks.

### debug_peripheral

Generate a debugging assistance prompt.

**Parameters:**
- peripheral: The peripheral being debugged
- error: Error message or symptom description

### configure_peripheral

Generate a configuration assistance prompt.

**Parameters:**
- peripheral: The peripheral to configure
- requirements: Configuration requirements

### explain_hal_function

Generate an explanation prompt for HAL functions.

**Parameters:**
- function_name: The HAL function to explain

### migration_guide

Generate a migration assistance prompt.

**Parameters:**
- from_family: Source STM32 family (e.g., "STM32F4")
- to_family: Target STM32 family (e.g., "STM32H7")
- peripheral: Peripheral focus for migration

## Configuration

Configuration is managed via environment variables or `.env` file.

### Key Settings

| Variable | Default | Description |
|----------|---------|-------------|
| STM32_SERVER_MODE | hybrid | Server mode: local, network, hybrid |
| STM32_HOST | 0.0.0.0 | Host to bind (network mode) |
| STM32_PORT | 8765 | Port (network mode) |
| STM32_COLLECTION_NAME | stm32_docs | ChromaDB collection name |
| STM32_EMBEDDING_MODEL | all-MiniLM-L6-v2 | Sentence transformer model |
| STM32_LOG_LEVEL | INFO | Logging level |
| STM32_MAX_SEARCH_RESULTS | 20 | Maximum search results |
| STM32_MIN_RELEVANCE_SCORE | 0.3 | Minimum relevance score |

### Example .env

```env
STM32_SERVER_MODE=network
STM32_HOST=0.0.0.0
STM32_PORT=8765
STM32_LOG_LEVEL=INFO
STM32_EMBEDDING_MODEL=all-MiniLM-L6-v2
```

## Starting the Server

### Using Python Module

```bash
# Local mode (default)
python -m mcp_server.server

# Network mode
STM32_SERVER_MODE=network python -m mcp_server.server
```

### Using Start Script

```bash
# Show help
python scripts/start_server.py --help

# Show configuration
python scripts/start_server.py --show-config

# Validate setup
python scripts/start_server.py --validate

# Start in local mode
python scripts/start_server.py --mode local

# Start in network mode
python scripts/start_server.py --mode network --port 8765

# Start with custom settings
python scripts/start_server.py --mode network --host 0.0.0.0 --port 9000 --log-level DEBUG
```

## Tailscale Integration

For remote access via Tailscale:

1. **Configure Network Mode**:
   ```bash
   export STM32_SERVER_MODE=network
   export STM32_HOST=0.0.0.0
   export STM32_PORT=8765
   ```

2. **Start the Server**:
   ```bash
   python scripts/start_server.py --mode network
   ```

3. **Access via Tailscale**:
   The server will be accessible at `http://<tailscale-hostname>:8765`

4. **Optional: Set Tailscale Hostname**:
   ```bash
   export STM32_TAILSCALE_HOSTNAME=stm32-docs-server
   ```

### Network Endpoints

| Endpoint | Description |
|----------|-------------|
| `/` | Server information |
| `/health` | Health check |
| `/sse` | SSE connection for MCP |
| `/messages` | MCP message endpoint |

## Claude Code Integration

### Local Mode Configuration

Add to your Claude Code MCP configuration:

```json
{
  "mcpServers": {
    "stm32-docs": {
      "command": "python",
      "args": ["-m", "mcp_server.server"],
      "cwd": "/path/to/stm32-agents"
    }
  }
}
```

### Network Mode Configuration

For remote servers:

```json
{
  "mcpServers": {
    "stm32-docs": {
      "transport": "sse",
      "url": "http://your-tailscale-host:8765/sse"
    }
  }
}
```

## Troubleshooting

### Server Won't Start

1. **Check dependencies**:
   ```bash
   python scripts/start_server.py --validate
   ```

2. **Check ChromaDB path**:
   ```bash
   python scripts/start_server.py --show-config
   ```

3. **Check for indexed documents**:
   ```bash
   python scripts/test_retrieval.py
   ```

### No Search Results

1. **Verify documents are indexed**:
   ```bash
   python scripts/test_retrieval.py
   ```

2. **Re-ingest documents**:
   ```bash
   python scripts/ingest_docs.py --clear
   ```

### Network Mode Connection Issues

1. **Check server is listening**:
   ```bash
   curl http://localhost:8765/health
   ```

2. **Check Tailscale connectivity**:
   ```bash
   tailscale ping <hostname>
   ```

3. **Verify firewall allows port**:
   ```bash
   sudo ufw allow 8765
   ```

## Performance Considerations

- **Embedding Model**: The default `all-MiniLM-L6-v2` is fast but less accurate than larger models
- **Lazy Loading**: Embedding model loads on first query to reduce startup time
- **Result Caching**: Consider implementing caching for frequently used queries
- **Index Size**: Monitor ChromaDB size if indexing large documentation sets

## Security Notes

- Network mode exposes the server to network access
- Consider using Tailscale's built-in security features
- Set `STM32_API_KEY` for optional API key authentication
- Limit `STM32_ALLOWED_TAILSCALE_IPS` for IP-based access control

## API Reference

### Python API

```python
from mcp_server.server import get_store, mcp

# Access the ChromaDB store directly
store = get_store()
results = store.search("GPIO configuration")

# Access the FastMCP server
print(mcp.name)  # "stm32-docs"
```

### HTTP Endpoints (Network Mode)

```bash
# Health check
curl http://localhost:8765/health

# Server info
curl http://localhost:8765/

# SSE connection (for MCP clients)
curl http://localhost:8765/sse
```
