# STM32 MCP Documentation Server

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.11+](https://img.shields.io/badge/python-3.11+-blue.svg)](https://www.python.org/downloads/)
[![MCP Protocol](https://img.shields.io/badge/MCP-1.0-green.svg)](https://modelcontextprotocol.io/)

An MCP (Model Context Protocol) server that provides semantic search over STM32 microcontroller documentation for use with Claude Code and other AI assistants. Features intelligent document chunking, ChromaDB vector storage, and 16 specialized agents for different embedded development domains.

## Features

- **One-Command Install**: Install via `uvx` from private GitHub repository
- **Auto-Setup**: Agents and vector database auto-install on first run
- **Semantic Search**: Find relevant documentation using natural language queries
- **Peripheral-Specific Search**: Filter results by STM32 peripheral (GPIO, UART, SPI, etc.)
- **Code Examples**: Retrieve working code examples for any topic
- **HAL Function Lookup**: Get documentation for specific STM32 HAL/LL library functions
- **16 Specialized Agents**: Domain-specific agents for firmware, debugging, power, security, and more
- **No Hardcoded Paths**: Fully portable installation

## Quick Start

### One-Command Installation

```bash
# Install the MCP server (auto-installs agents + docs on first run)
claude mcp add stm32-docs --scope user -- uvx --from git+https://TOKEN@github.com/creativec09/stm32-agents.git stm32-mcp-docs
```

Replace `TOKEN` with your GitHub Personal Access Token (requires `repo` scope for private repository).

### What Happens on First Run

1. **16 STM32 agents** are installed to `~/.claude/agents/`
2. **Vector database** (13,815 chunks) is built from 80 bundled STM32 documents
3. **Marker files** prevent re-installation on subsequent runs

First run takes 5-10 minutes. Subsequent starts are instant.

### Start Using

Restart Claude Code, then use slash commands:

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

## Table of Contents

- [Quick Start](#quick-start)
- [Installation](#installation)
- [MCP Tools](#mcp-tools)
- [Specialized Agents](#specialized-agents)
- [Usage](#usage)
- [Configuration](#configuration)
- [Development](#development)
- [Troubleshooting](#troubleshooting)
- [Uninstall](#uninstall)
- [License](#license)

## Installation

### Prerequisites

- Python 3.11 or higher
- [uv](https://docs.astral.sh/uv/) - Install with `curl -LsSf https://astral.sh/uv/install.sh | sh`
- Claude Code CLI
- GitHub Personal Access Token (for private repository)

### Method 1: uvx Installation (Recommended)

```bash
# One command installs everything
claude mcp add stm32-docs --scope user -- uvx --from git+https://TOKEN@github.com/creativec09/stm32-agents.git stm32-mcp-docs
```

### Method 2: pip Installation

```bash
# Install the package
pip install git+https://TOKEN@github.com/creativec09/stm32-agents.git

# Register with Claude Code
claude mcp add stm32-docs --scope user -- python -m mcp_server
```

### Method 3: Development Installation

```bash
# Clone the repository
git clone https://github.com/creativec09/stm32-agents.git
cd stm32-agents

# Create virtual environment
python -m venv .venv
source .venv/bin/activate  # Linux/macOS
# .venv\Scripts\activate   # Windows

# Install in development mode
pip install -e ".[dev]"

# Register with Claude Code
claude mcp add stm32-docs --scope user -- python -m mcp_server
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

## MCP Tools

The server provides 15+ tools for STM32 documentation:

| Tool | Description |
|------|-------------|
| `search_stm32_docs` | Semantic search across all documentation |
| `get_peripheral_docs` | Get documentation for a specific peripheral |
| `get_code_examples` | Find code examples for a topic |
| `get_register_info` | Get detailed register documentation |
| `lookup_hal_function` | Look up HAL/LL function documentation |
| `troubleshoot_error` | Find solutions to errors and issues |
| `get_init_sequence` | Get peripheral initialization code |
| `get_clock_config` | Clock tree configuration examples |
| `compare_peripheral_options` | Compare peripheral features |
| `get_migration_guide` | Migration guides between STM32 families |
| `get_interrupt_code` | Interrupt handling examples |
| `get_dma_code` | DMA configuration examples |
| `get_low_power_code` | Low power mode configuration |
| `get_callback_code` | HAL callback examples |
| `get_init_template` | Complete initialization templates |
| `list_peripherals` | List available peripherals |

### MCP Resources

| Resource URI | Description |
|--------------|-------------|
| `stm32://status` | Server status and statistics |
| `stm32://health` | Health check |
| `stm32://peripherals` | List documented peripherals |
| `stm32://stats` | Database statistics |

## Specialized Agents

16 domain-specific agents are auto-installed to `~/.claude/agents/`:

| Agent | Domain | Key Topics |
|-------|--------|------------|
| `router` | Triage | Query classification, routing |
| `triage` | Triage | Initial query analysis |
| `firmware` | Core Development | General firmware questions |
| `firmware-core` | Core Development | HAL/LL, timers, DMA, interrupts, NVIC, RCC |
| `debug` | Debugging | HardFault analysis, SWD, trace |
| `bootloader` | Updates | Bootloader development |
| `bootloader-programming` | Updates | IAP, DFU, system bootloader |
| `peripheral-comm` | Communication | UART, SPI, I2C, CAN, USB, Ethernet |
| `peripheral-analog` | Analog | ADC, DAC, OPAMP, comparators, sensors |
| `peripheral-graphics` | Display | LTDC, DMA2D, DCMI, TouchGFX |
| `power` | Power | General power optimization |
| `power-management` | Power | Sleep, Stop, Standby, battery |
| `safety` | Certification | Safety-critical development |
| `safety-certification` | Certification | IEC 61508, ISO 26262, Class B |
| `security` | Security | Secure boot, TrustZone, crypto, RNG |
| `hardware-design` | PCB/Hardware | EMC, thermal, oscillators, layout |

See [docs/AGENT_QUICK_REFERENCE.md](docs/AGENT_QUICK_REFERENCE.md) for detailed agent capabilities.

## Usage

### Slash Commands

```
/stm32 <query>           - General STM32 documentation search
/stm32-init <peripheral> - Get initialization code for a peripheral
/stm32-hal <function>    - Look up HAL function documentation
/stm32-debug <issue>     - Troubleshoot an STM32 issue
```

### Natural Language Queries

Agents automatically search documentation:

```
"Show me how to configure GPIO interrupts on STM32H7"
"Why is my I2C peripheral returning HAL_TIMEOUT?"
"How to enter Stop mode and wake up on UART?"
```

### Network Mode (Tailscale)

For accessing from multiple machines:

```bash
# Start server in network mode
STM32_SERVER_MODE=network python -m mcp_server --port 8765

# On client machines
claude mcp add stm32-docs --scope user --type sse --url "http://YOUR_TAILSCALE_IP:8765/sse"
```

## Configuration

Configuration via environment variables:

```bash
STM32_SERVER_MODE=local          # local, network
STM32_HOST=0.0.0.0               # Host to bind (network mode)
STM32_PORT=8765                  # Port (network mode)
STM32_COLLECTION_NAME=stm32_docs # ChromaDB collection name
STM32_EMBEDDING_MODEL=all-MiniLM-L6-v2
STM32_LOG_LEVEL=INFO
```

## Project Structure

```
stm32-agents/
├── mcp_server/              # MCP server implementation
│   ├── server.py            # Main server with tools/resources
│   ├── __main__.py          # Module entry point
│   ├── config.py            # Configuration management
│   ├── markdowns/           # Bundled STM32 documentation (80 files)
│   └── agents/              # Bundled agent definitions (16 agents)
├── pipeline/                # Document processing pipeline
├── storage/                 # Vector storage layer
├── scripts/                 # CLI utilities
├── tests/                   # Test suite
├── docs/                    # Comprehensive documentation
└── .claude/                 # Claude Code configuration
    ├── agents/              # Specialized agent definitions
    └── commands/            # Slash command definitions
```

## Development

### Setup Development Environment

```bash
git clone https://github.com/creativec09/stm32-agents.git
cd stm32-agents
python -m venv .venv
source .venv/bin/activate
pip install -e ".[dev]"
```

### Running Tests

```bash
pytest tests/
pytest tests/ --cov=mcp_server --cov=pipeline --cov=storage
```

### Code Quality

```bash
black .
isort .
ruff check .
mypy mcp_server pipeline storage
```

## System Requirements

| Requirement | Minimum | Recommended |
|-------------|---------|-------------|
| Python | 3.11 | 3.12 |
| RAM | 4GB | 8GB |
| Disk Space | 1GB | 2GB |
| OS | Linux, macOS, Windows (WSL2) | Linux |

### Performance Characteristics

| Metric | Value |
|--------|-------|
| First Run | 5-10 minutes (builds database) |
| Subsequent Starts | <5 seconds |
| Query Response | <100ms (warm) |
| Database Size | ~500MB |
| Total Chunks | 13,815 |
| Documentation Files | 80 |

## Troubleshooting

### "No documentation found"

Database may not have built yet. Wait for auto-ingestion on first run, or:
```bash
python scripts/ingest_docs.py --clear
```

### Slow first request

First request takes 5-10 minutes due to:
1. Loading embedding model
2. Building vector database from 80 documents

Subsequent requests are fast (<100ms).

### Server won't start

```bash
# Check uv is installed
uv --version

# Verify registration
claude mcp list

# Check server status
claude mcp status stm32-docs
```

For more troubleshooting help, see [docs/GETTING_STARTED.md](docs/GETTING_STARTED.md#troubleshooting).

## Uninstall

To completely remove the STM32 MCP server and all its components:

```bash
# Step 1: Remove MCP server configuration
claude mcp remove stm32-docs --scope user

# Step 2: Clean up agents, commands, and database
stm32-uninstall
```

The `stm32-uninstall` command removes:
- 16 STM32 agents from `~/.claude/agents/`
- 4 slash commands from `~/.claude/commands/`
- Marker file `~/.claude/.stm32-agents-installed`
- ChromaDB vector database

### Uninstall Options

```bash
stm32-uninstall --dry-run   # Preview what will be removed
stm32-uninstall --yes       # Skip confirmation prompt
stm32-uninstall --keep-db   # Keep database, only remove agents/commands
```

### Why Manual Cleanup is Required

The MCP protocol does not support uninstall hooks. When you run `claude mcp remove`, only the MCP configuration is removed. Installed agents, commands, and databases are NOT automatically cleaned up.

This is a known limitation documented in:
- [anthropics/claude-code#11240](https://github.com/anthropics/claude-code/issues/11240) - Plugin Lifecycle Hooks
- [anthropics/claude-code#9394](https://github.com/anthropics/claude-code/issues/9394) - postInstall/postUninstall hooks

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Acknowledgments

Built with:
- [MCP (Model Context Protocol)](https://modelcontextprotocol.io/) - AI integration framework by Anthropic
- [ChromaDB](https://www.trychroma.com/) - Vector database
- [Sentence Transformers](https://www.sbert.net/) - Embedding models
- [FastMCP](https://github.com/jlowin/fastmcp) - MCP server framework

## Support

- [Documentation Index](docs/INDEX.md)
- [Getting Started Guide](docs/GETTING_STARTED.md)
- [Claude Code Integration](docs/CLAUDE_CODE_INTEGRATION.md)
- [MCP Server Documentation](docs/MCP_SERVER.md)
