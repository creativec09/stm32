# STM32 MCP Documentation Server

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.11+](https://img.shields.io/badge/python-3.11+-blue.svg)](https://www.python.org/downloads/)
[![MCP Protocol](https://img.shields.io/badge/MCP-1.0-green.svg)](https://modelcontextprotocol.io/)

An MCP (Model Context Protocol) server that provides semantic search over STM32 microcontroller documentation for use with Claude Code and other AI assistants. Features intelligent document chunking, ChromaDB vector storage, and specialized agents for different embedded development domains.

## Features

- **Semantic Search**: Find relevant documentation using natural language queries with vector similarity
- **Peripheral-Specific Search**: Filter results by STM32 peripheral (GPIO, UART, SPI, TIM, ADC, etc.)
- **Code Examples**: Retrieve working code examples for any topic with context
- **HAL Function Lookup**: Get documentation for specific STM32 HAL/LL library functions
- **Troubleshooting**: Find solutions to common STM32 development issues
- **Network Mode**: Access via Tailscale from multiple machines using SSE transport
- **Specialized Agents**: Domain-specific agents for firmware, debugging, power management, security, and more
- **Smart Chunking**: Structure-aware document chunking that preserves code blocks, tables, and context

## Table of Contents

- [Quick Start](#quick-start)
- [Installation](#installation)
- [Usage](#usage)
- [MCP Tools](#mcp-tools)
- [Specialized Agents](#specialized-agents)
- [Configuration](#configuration)
- [Project Structure](#project-structure)
- [Development](#development)
- [Troubleshooting](#troubleshooting)
- [Contributing](#contributing)
- [License](#license)

## Quick Start

### Prerequisites

- Python 3.11 or higher
- Git
- Claude Code CLI (for Claude Code integration)
- ~500MB disk space for vector database (auto-built on first run)

### Clone-and-Go Setup

The server features **automatic database building** on first run. Just install and start using - the documentation index builds automatically!

```bash
# Clone the repository
git clone https://github.com/creativec09/stm32-agents.git
cd stm32-agents

# Create and activate virtual environment
python -m venv .venv
source .venv/bin/activate  # Linux/macOS
# .venv\Scripts\activate   # Windows PowerShell

# Install the package
pip install -e .

# Run setup - configures MCP and installs agents
stm32-setup
```

The `stm32-setup` command automatically:
- Configures the MCP server in `~/.claude/mcp.json`
- Installs all agents to `~/.claude/agents/`
- Installs slash commands to `~/.claude/commands/`
- Verifies the installation

**Auto-Setup on First Run**: On first use, the MCP server automatically:
- **Installs agents**: Copies 16 STM32 agents to `~/.claude/agents/` for use with Claude Code
- **Ingests documentation**: Indexes the bundled STM32 documentation (takes 5-10 minutes)

Subsequent starts are instant. You'll see progress logs during initial setup.

### Start Using

Restart Claude Code, then use the slash commands:

```
/stm32 How do I configure UART with DMA?
/stm32-init SPI master mode at 10MHz
/stm32-hal HAL_GPIO_Init parameters
/stm32-debug UART not receiving data
```

Or ask naturally - the agents are triggered automatically:
```
"Show me how to configure GPIO interrupts on STM32H7"
"Why is my I2C peripheral returning HAL_TIMEOUT?"
```

## Installation

### Quick Install via uvx (Recommended for Private Repository)

For installation from the private GitHub repository using `uvx`:

#### Prerequisites
- Install uv: `curl -LsSf https://astral.sh/uv/install.sh | sh`
- GitHub Personal Access Token (PAT) with `repo` scope

#### Add to Claude Code
```bash
# Replace TOKEN with your GitHub Personal Access Token
claude mcp add stm32-docs -s user -- uvx --from git+https://TOKEN@github.com/creativec09/stm32-agents.git stm32-mcp-docs
```

This installs and runs the MCP server directly from the private repository without needing to clone it first. On first run, the server automatically installs 16 STM32 agents to `~/.claude/agents/` and indexes the bundled documentation.

#### With Specific Version Tag
```bash
claude mcp add stm32-docs -s user -- uvx --from git+https://TOKEN@github.com/creativec09/stm32-agents.git@v1.0.0 stm32-mcp-docs
```

### Alternative: pip Install

```bash
# Install the package (requires GitHub authentication)
pip install git+https://TOKEN@github.com/creativec09/stm32-agents.git

# Register with Claude Code
claude mcp add stm32-docs -s user -- python -m mcp_server
```

### Development Install

```bash
# Clone the repository
git clone https://github.com/creativec09/stm32-agents.git
cd stm32-agents

# Create and activate virtual environment
python -m venv .venv
source .venv/bin/activate  # Linux/macOS
# .venv\Scripts\activate   # Windows PowerShell

# Install in development mode
pip install -e .

# Register with Claude Code
claude mcp add stm32-docs -s user -- python -m mcp_server

# Or use the setup script (handles everything including doc ingestion)
stm32-setup
```

### Manual MCP Configuration (Alternative)

If the `claude` CLI is not available, you can manually configure the MCP server.

**Option A**: Use the project-level `.mcp.json` (for project-scoped access):
```bash
# The .mcp.json at the project root is automatically detected by Claude Code
# when you open the project directory
```

**Option B**: Add to user config `~/.claude.json`:
```json
{
  "mcpServers": {
    "stm32-docs": {
      "command": "python",
      "args": ["-m", "mcp_server.server"],
      "env": {
        "STM32_SERVER_MODE": "local",
        "STM32_LOG_LEVEL": "INFO"
      }
    }
  }
}
```

For detailed installation instructions including Claude Code integration and network mode setup, see [INSTALL.md](INSTALL.md).

## Usage

### With Claude Code

The MCP server integrates seamlessly with Claude Code. After installation:

1. **Configure MCP** (using Claude CLI - recommended):
   ```bash
   claude mcp add stm32-docs -s user -- python -m mcp_server
   ```

   Or use the project-level `.mcp.json` by opening the project directory in Claude Code.

2. **Use Slash Commands**:
   ```
   /stm32 <query>          - General STM32 documentation search
   /stm32-init <peripheral> - Get initialization code for a peripheral
   /stm32-hal <function>   - Look up HAL function documentation
   /stm32-debug <issue>    - Troubleshoot an STM32 issue
   ```

3. **Natural Language**: Agents automatically search documentation:
   ```
   "Show me how to configure GPIO interrupts on STM32H7"
   "Why is my I2C peripheral returning HAL_TIMEOUT?"
   "How to enter Stop mode and wake up on UART?"
   ```

### Programmatic Usage

```python
from storage.chroma_store import STM32ChromaStore
from storage.metadata import Peripheral

# Initialize store
store = STM32ChromaStore("data/chroma_db/")

# Search all documentation
results = store.search("configure UART DMA", n_results=5)

# Search specific peripheral
results = store.search(
    "PWM output configuration",
    peripheral=Peripheral.TIM,
    n_results=5
)

# Print results
for result in results:
    print(f"Score: {result['score']:.3f}")
    print(f"Source: {result['metadata']['source']}")
    print(f"Content: {result['content'][:200]}...")
```

### Network Mode (Tailscale)

For accessing the server from multiple machines:

```bash
# Start server in network mode
STM32_SERVER_MODE=network python scripts/start_server.py --port 8765

# On client machines, configure .claude/mcp.json:
{
  "mcpServers": {
    "stm32-docs": {
      "type": "sse",
      "url": "http://YOUR_TAILSCALE_IP:8765/sse"
    }
  }
}
```

## MCP Tools

The server exposes the following MCP tools:

| Tool | Description |
|------|-------------|
| `search_stm32_docs` | Semantic search across all documentation |
| `get_peripheral_docs` | Get documentation for a specific peripheral |
| `get_code_examples` | Find code examples for a topic |
| `lookup_hal_function` | Look up HAL/LL function documentation |
| `troubleshoot_error` | Find solutions to errors and issues |
| `get_init_sequence` | Get peripheral initialization code |
| `get_clock_config` | Clock tree configuration examples |
| `get_migration_guide` | Migration guides between STM32 families |
| `compare_peripherals` | Compare peripheral features across families |
| `get_electrical_specs` | Find electrical specifications |
| `get_timing_requirements` | Get timing and signal requirements |
| `get_interrupt_example` | Interrupt configuration examples |
| `get_dma_example` | DMA setup and configuration examples |
| `get_low_power_example` | Low power mode configuration |
| `list_peripherals` | List available peripherals in documentation |

## Specialized Agents

The system includes domain-specific agents that automatically leverage MCP tools:

| Agent | Domain | Key Topics |
|-------|--------|------------|
| **Router** | Triage | Query classification, routing, chip selection |
| **Firmware Core** | Core Development | HAL/LL, timers, DMA, interrupts, NVIC, RCC |
| **Peripheral Comm** | Communication | UART, SPI, I2C, CAN, USB, Ethernet |
| **Peripheral Analog** | Analog | ADC, DAC, OPAMP, comparators, sensors |
| **Peripheral Graphics** | Display | LTDC, DMA2D, DCMI, TouchGFX |
| **Power Management** | Power | Sleep, Stop, Standby, battery optimization |
| **Security** | Security | Secure boot, TrustZone, crypto, RNG |
| **Safety** | Certification | IEC 61508, ISO 26262, Class B self-test |
| **Bootloader** | Updates | IAP, DFU, system bootloader |
| **Debug** | Debugging | HardFault analysis, SWD, trace |
| **Hardware Design** | PCB/Hardware | EMC, thermal, oscillators, layout |

See [docs/AGENT_QUICK_REFERENCE.md](docs/AGENT_QUICK_REFERENCE.md) for detailed agent capabilities.

## Configuration

Configuration via environment variables or `.env` file:

```bash
# Server mode: local, network, or hybrid
STM32_SERVER_MODE=local

# Network settings (for network/hybrid mode)
STM32_HOST=0.0.0.0
STM32_PORT=8765

# Database paths
STM32_CHROMA_DB_PATH=data/chroma_db/
STM32_COLLECTION_NAME=stm32_docs

# Embedding model
STM32_EMBEDDING_MODEL=all-MiniLM-L6-v2

# Document processing
STM32_CHUNK_SIZE=1000
STM32_CHUNK_OVERLAP=150

# Logging
STM32_LOG_LEVEL=INFO
```

See [.env.example](.env.example) for all configuration options.

## Project Structure

```
stm32-agents/
├── mcp_server/              # MCP server implementation
│   ├── server.py            # Main server with tools/resources
│   ├── __main__.py          # Module entry point (python -m mcp_server)
│   ├── config.py            # Configuration management
│   ├── tools/               # Search tool implementations
│   └── resources/           # MCP resource handlers
├── pipeline/                # Document processing pipeline
│   ├── chunker.py           # Markdown chunking with structure preservation
│   └── validator.py         # Chunk validation
├── storage/                 # Vector storage layer
│   ├── chroma_store.py      # ChromaDB wrapper
│   └── metadata.py          # Metadata schemas and enums
├── scripts/                 # CLI utilities
│   ├── setup.py             # Complete setup wizard
│   ├── ingest_docs.py       # Document ingestion
│   ├── start_server.py      # Server launcher
│   ├── verify_mcp.py        # System validation
│   ├── test_retrieval.py    # Search quality testing
│   └── export_chunks.py     # Data export
├── tests/                   # Test suite
├── docs/                    # Comprehensive documentation
├── mcp_server/markdowns/    # Bundled STM32 documentation (80+ files)
├── data/                    # Generated data
│   └── chroma_db/           # ChromaDB vector storage
├── .mcp.json                # Project-level MCP configuration (Claude Code)
├── .claude/                 # Claude Code project settings
│   ├── settings.json        # Project-specific Claude settings
│   ├── agents/              # Specialized agent definitions
│   └── commands/            # Slash command definitions
├── pyproject.toml           # Package configuration
├── requirements.txt         # Dependencies
└── requirements-dev.txt     # Development dependencies
```

## Development

### Setting Up Development Environment

```bash
# Clone and setup
git clone https://github.com/creativec09/stm32-agents.git
cd stm32-agents

# Create virtual environment
python -m venv .venv
source .venv/bin/activate

# Install with development dependencies
pip install -e ".[dev]"

# Install pre-commit hooks
pre-commit install
```

### Running Tests

```bash
# Run all tests
pytest tests/

# Run with coverage
pytest tests/ --cov=mcp_server --cov=pipeline --cov=storage

# Run specific test file
pytest tests/test_chunker.py -v
```

### Code Quality

```bash
# Format code
black .
isort .

# Lint
ruff check .

# Type checking
mypy mcp_server pipeline storage
```

### Validation Scripts

```bash
# Full system validation
python scripts/validate_system.py

# Verify MCP server functionality
python scripts/verify_mcp.py

# Test search quality
python scripts/test_retrieval.py
```

## System Requirements

| Requirement | Minimum | Recommended |
|-------------|---------|-------------|
| Python | 3.11 | 3.12 |
| RAM | 4GB | 8GB |
| Disk Space | 1GB | 2GB |
| OS | Linux, macOS, Windows (WSL2) | Linux |

### Performance Characteristics

- **First Run**: 5-10 minutes (auto-ingests 80+ markdown files and loads ML model)
- **Subsequent Starts**: ~90 seconds (loads ML model from cache)
- **Warm Queries**: <100ms per query
- **Storage**: ~190MB for ChromaDB database (auto-built on first run)

## Troubleshooting

### Common Issues

**"No documentation found"**
```bash
# Re-ingest documentation
python scripts/ingest_docs.py --clear
```

**Import errors**
```bash
# Ensure virtual environment is active and package installed
source .venv/bin/activate
pip install -e .
```

**Slow first request**
The first request after starting takes ~90 seconds due to loading the embedding model. This is normal. Subsequent requests are fast.

**Server won't start**
```bash
# Check configuration
python -c "from mcp_server.config import settings; print(settings)"

# Verify database
python scripts/verify_mcp.py
```

For more troubleshooting help, see [TROUBLESHOOTING.md](TROUBLESHOOTING.md).

## Contributing

We welcome contributions! Please see [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines.

### Quick Contribution Guide

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Make your changes
4. Run tests (`pytest tests/`)
5. Commit your changes (`git commit -m 'Add amazing feature'`)
6. Push to the branch (`git push origin feature/amazing-feature`)
7. Open a Pull Request

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Acknowledgments

Built with:
- [MCP (Model Context Protocol)](https://modelcontextprotocol.io/) - AI integration framework by Anthropic
- [ChromaDB](https://www.trychroma.com/) - Vector database
- [Sentence Transformers](https://www.sbert.net/) - Embedding models
- [FastMCP](https://github.com/jlowin/fastmcp) - MCP server framework

## Support

- Check the [Documentation Index](docs/INDEX.md)
- Review [Getting Started Guide](docs/GETTING_STARTED.md)
- See [Testing Guide](docs/TESTING.md) for validation
- Open an [Issue](https://github.com/creativec09/stm32-agents/issues) for bugs or feature requests
