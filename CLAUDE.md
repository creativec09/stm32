# STM32 MCP Documentation Server - Claude Code Project

This file provides instructions for Claude Code when working with this project.

## Project Overview

The STM32 MCP Documentation Server is an MCP (Model Context Protocol) server that provides semantic search over 80+ STM32 microcontroller documentation files. It includes 16 specialized agents and auto-installs everything on first run.

**Repository**: https://github.com/creativec09/stm32 (private)

## Installation

### One-Command Install (Recommended)

This installation method auto-installs `uv` if needed, making it work out-of-the-box on Ubuntu 24 WSL and other Linux systems:

```bash
# Install MCP server with auto-setup (auto-installs uv if needed, agents + docs auto-install on first run)
claude mcp add-json stm32-docs --scope user '{"command":"bash","args":["-c","export PATH=\"$HOME/.local/bin:$PATH\" && (command -v uvx >/dev/null 2>&1 || curl -LsSf https://astral.sh/uv/install.sh | sh -s -- -q) && uvx --from git+https://github.com/creativec09/stm32.git stm32-mcp-docs"]}'
```

**Note**: For private repository access, include a GitHub Personal Access Token in the URL:
```bash
claude mcp add-json stm32-docs --scope user '{"command":"bash","args":["-c","export PATH=\"$HOME/.local/bin:$PATH\" && (command -v uvx >/dev/null 2>&1 || curl -LsSf https://astral.sh/uv/install.sh | sh -s -- -q) && uvx --from git+https://TOKEN@github.com/creativec09/stm32.git stm32-mcp-docs"]}'
```

### If you already have `uv` installed

```bash
claude mcp add stm32-docs --scope user -- uvx --from git+https://github.com/creativec09/stm32.git stm32-mcp-docs
```

### What Auto-Installs on First Run

1. **16 STM32 Specialist Agents** are copied to `~/.claude/agents/`
2. **Vector Database** (13,815 chunks) is built from 80 bundled markdown docs
3. **Marker files** prevent re-installation on subsequent runs

First run takes 5-10 minutes (embedding generation). Subsequent starts are instant.

## Available MCP Tools (15+)

When this MCP server is connected, Claude Code has access to these tools:

| Tool | Description |
|------|-------------|
| `search_stm32_docs` | Semantic search across all STM32 documentation |
| `get_peripheral_docs` | Get documentation for a specific peripheral (GPIO, UART, etc.) |
| `get_code_examples` | Find code examples for any topic |
| `get_register_info` | Detailed register documentation with bit fields |
| `lookup_hal_function` | HAL/LL function documentation and parameters |
| `troubleshoot_error` | Find solutions to STM32 errors and issues |
| `get_init_sequence` | Complete peripheral initialization code |
| `get_clock_config` | Clock tree configuration examples |
| `compare_peripheral_options` | Compare peripherals or modes |
| `get_migration_guide` | Migration guides between STM32 families |
| `get_interrupt_code` | Interrupt handling examples |
| `get_dma_code` | DMA configuration examples |
| `get_low_power_code` | Low power mode configuration |
| `get_callback_code` | HAL callback implementation examples |
| `get_init_template` | Complete initialization templates |
| `list_peripherals` | List all documented peripherals |

### MCP Resources

| Resource URI | Description |
|--------------|-------------|
| `stm32://status` | Server status and statistics |
| `stm32://health` | Health check |
| `stm32://peripherals` | List documented peripherals |
| `stm32://stats` | Database statistics |

## Available Agents (16)

Agents are auto-installed to `~/.claude/agents/` on first MCP server run:

| Agent | Purpose |
|-------|---------|
| `router` | Query classification and routing |
| `triage` | Initial query analysis |
| `firmware` | General firmware development |
| `firmware-core` | Core HAL/LL, timers, DMA, interrupts |
| `debug` | Debugging and troubleshooting |
| `bootloader` | Bootloader development |
| `bootloader-programming` | Bootloader programming protocols |
| `peripheral-comm` | UART, SPI, I2C, CAN, USB |
| `peripheral-analog` | ADC, DAC, OPAMP, comparators |
| `peripheral-graphics` | LTDC, DMA2D, DCMI, TouchGFX |
| `power` | Power optimization |
| `power-management` | Sleep, Stop, Standby modes |
| `safety` | Safety-critical development |
| `safety-certification` | IEC 61508, ISO 26262 certification |
| `security` | Secure boot, TrustZone, crypto |
| `hardware-design` | PCB design, EMC, thermal |

## Slash Commands

```
/stm32 <query>           - General STM32 documentation search
/stm32-init <peripheral> - Get initialization code for a peripheral
/stm32-hal <function>    - Look up HAL function documentation
/stm32-debug <issue>     - Troubleshoot an STM32 issue
```

## Development Instructions

### Local Development Setup

```bash
# Clone repository
git clone https://github.com/creativec09/stm32.git
cd stm32-agents

# Create virtual environment
python -m venv .venv
source .venv/bin/activate  # Linux/macOS
# .venv\Scripts\activate   # Windows

# Install in development mode
pip install -e ".[dev]"

# Run tests
pytest tests/

# Run the server locally
python -m mcp_server
```

### Project Structure

```
stm32-agents/
├── mcp_server/              # MCP server implementation
│   ├── server.py            # Main server with tools
│   ├── __main__.py          # Entry point
│   ├── config.py            # Configuration
│   ├── markdowns/           # Bundled STM32 documentation (80 files)
│   └── agents/              # Bundled agent definitions (16 agents)
├── pipeline/                # Document processing
├── storage/                 # ChromaDB storage layer
├── scripts/                 # CLI utilities
├── tests/                   # Test suite
├── docs/                    # Documentation
└── .claude/                 # Claude Code configuration
    ├── agents/              # Agent definitions
    └── commands/            # Slash commands
```

### Key Files

- `mcp_server/server.py` - Main MCP server implementation
- `mcp_server/config.py` - Configuration management
- `storage/chroma_store.py` - ChromaDB vector store wrapper
- `pipeline/chunker.py` - Document chunking logic

### Environment Variables

```bash
STM32_SERVER_MODE=local          # local, network, or hybrid
STM32_CHROMA_DB_PATH=data/chroma_db/
STM32_COLLECTION_NAME=stm32_docs
STM32_EMBEDDING_MODEL=all-MiniLM-L6-v2
STM32_LOG_LEVEL=INFO
```

### Testing

```bash
# Run all tests
pytest tests/

# Run with coverage
pytest tests/ --cov=mcp_server --cov=pipeline --cov=storage

# Verify MCP server
python scripts/verify_mcp.py

# Test search quality
python scripts/test_retrieval.py
```

### Re-ingesting Documentation

If you need to rebuild the vector database:

```bash
python scripts/ingest_docs.py --clear -v
```

## Best Practices for Claude Code

1. **Use MCP tools first** - Always search documentation before answering STM32 questions
2. **Be specific** - Use peripheral-specific tools when appropriate
3. **Check examples** - Use `get_code_examples` for implementation guidance
4. **Troubleshoot systematically** - Use `troubleshoot_error` for debugging help
5. **Verify with HAL docs** - Use `lookup_hal_function` to confirm function usage

## Documentation

- [README.md](README.md) - Project overview
- [docs/GETTING_STARTED.md](docs/GETTING_STARTED.md) - Setup guide
- [docs/MCP_SERVER.md](docs/MCP_SERVER.md) - Server documentation
- [docs/AGENT_QUICK_REFERENCE.md](docs/AGENT_QUICK_REFERENCE.md) - Agent capabilities
- [docs/INDEX.md](docs/INDEX.md) - Full documentation index
