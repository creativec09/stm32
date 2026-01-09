# Installation Guide

This guide provides detailed installation instructions for the STM32 MCP Documentation Server.

## Table of Contents

- [Prerequisites](#prerequisites)
- [Plugin Installation (Recommended)](#plugin-installation-recommended)
- [Alternative Installation Methods](#alternative-installation-methods)
- [What Gets Installed](#what-gets-installed)
- [Post-Installation Setup](#post-installation-setup)
- [Claude Code Integration](#claude-code-integration)
- [Network Mode (Tailscale)](#network-mode-tailscale)
- [Verification](#verification)
- [Upgrading](#upgrading)
- [Uninstallation](#uninstallation)
- [Troubleshooting Installation](#troubleshooting-installation)

---

## Prerequisites

### Required

- **Python 3.11+**: Check with `python --version` or `python3 --version`
- **pip**: Python package installer (usually included with Python)
- **Git**: For cloning the repository
- **Claude Code CLI**: For using the MCP server with Claude

### Recommended

- **4GB+ RAM**: 8GB recommended for faster embedding generation
- **SSD Storage**: ~500MB free space for auto-built database and model cache

### Platform-Specific Notes

#### Linux
```bash
# Ubuntu/Debian
sudo apt update
sudo apt install python3.11 python3.11-venv python3-pip git

# Fedora
sudo dnf install python3.11 python3-pip git
```

#### macOS
```bash
# Using Homebrew
brew install python@3.11 git
```

#### Windows
- Install Python 3.11+ from [python.org](https://www.python.org/downloads/)
- **Recommended**: Use WSL2 for best compatibility
  ```powershell
  wsl --install
  ```

---

## Plugin Installation (Recommended)

The easiest way to install is using Claude Code's plugin system. This method:
- Automatically configures the MCP server
- Installs all 16 specialized agents
- Sets up 4 slash commands
- No manual configuration required

### Install the Plugin

In Claude Code, run:

```
/plugin install github:creativec09/stm32
```

### What Gets Installed

| Component | Description |
|-----------|-------------|
| MCP Server | Auto-configured via `mcp-config.json` |
| 16 Agents | Specialized STM32 development agents |
| 4 Commands | `/stm32`, `/stm32-hal`, `/stm32-init`, `/stm32-debug` |

### First Run

On first use, the MCP server automatically:
- Ingests the bundled STM32 documentation (takes 5-10 minutes)
- Builds the ChromaDB vector database

You will see progress logs like:

```
Database empty, starting auto-ingestion...
Found 80 markdown files in mcp_server/markdowns/
[10/80] Processed an4013-introduction-to-timers...
[20/80] Processed an4435-guidelines-for-obtaining...
...
Ingestion complete!
Ready - 13,815 chunks indexed
```

### Verify Installation

After installation, restart Claude Code and test:

```
/stm32 How do I configure UART with DMA?
```

---

## Alternative Installation Methods

### Option A: Manual MCP Installation via uvx

If you prefer not to use the plugin system:

```bash
# Install uv first
curl -LsSf https://astral.sh/uv/install.sh | sh

# Add MCP server to Claude Code
claude mcp add stm32-docs --scope user -- uvx --from git+https://github.com/creativec09/stm32.git stm32-mcp-docs
```

Note: For private repositories, use a GitHub Personal Access Token:
```bash
claude mcp add stm32-docs --scope user -- uvx --from git+https://TOKEN@github.com/creativec09/stm32.git stm32-mcp-docs
```

### Option B: pip Installation

```bash
# Install the package
pip install git+https://github.com/creativec09/stm32.git

# Register with Claude Code
claude mcp add stm32-docs --scope user -- python -m mcp_server
```

### Option C: Development Installation

For contributors and customization:

```bash
# Clone the repository
git clone https://github.com/creativec09/stm32.git
cd stm32-agents

# Create virtual environment
python -m venv .venv
source .venv/bin/activate  # Linux/macOS
# .venv\Scripts\activate   # Windows PowerShell

# Install with development dependencies
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
      "args": ["--from", "git+https://github.com/creativec09/stm32.git", "stm32-mcp-docs"],
      "env": {
        "STM32_SERVER_MODE": "local",
        "STM32_LOG_LEVEL": "INFO"
      }
    }
  }
}
```

---

## What Gets Installed

| Component | Location | Installed By |
|-----------|----------|--------------|
| Plugin manifest | `.claude-plugin/plugin.json` | Plugin system |
| Agent definitions | `agents/*.md` | Plugin system |
| Slash commands | `commands/*.md` | Plugin system |
| MCP configuration | `mcp-config.json` | Plugin system |
| Vector database | `data/chroma_db/` | Auto-built on first run |
| CLI commands | `stm32-*` | pip install |

### CLI Commands Available After Install

| Command | Description |
|---------|-------------|
| `stm32-setup` | Complete setup wizard |
| `stm32-setup --status` | Show installation status |
| `stm32-server` | Start the MCP server |
| `stm32-ingest` | Ingest documentation (auto-runs on first start) |
| `stm32-search` | Search from command line |
| `stm32-uninstall` | Clean up database |

---

## Post-Installation Setup

### Automatic Setup (Default)

The plugin system handles everything automatically. Just install and use.

### Manual Agent Installation (Alternative Methods Only)

If you installed via uvx or pip without the plugin:

```bash
# Copy agents and commands manually (if needed)
mkdir -p ~/.claude/agents ~/.claude/commands
cp agents/*.md ~/.claude/agents/
cp commands/*.md ~/.claude/commands/
```

### Document Ingestion

Ingestion happens automatically on first run. To force re-ingestion:

```bash
python scripts/ingest_docs.py --clear
```

---

## Claude Code Integration

### Local Mode (Default)

Local mode uses stdio transport - Claude Code launches the server directly.

After installation, restart Claude Code and test:

```
/stm32 How do I configure UART?
/stm32-hal HAL_GPIO_Init
/stm32-init SPI master mode
/stm32-debug UART not receiving
```

### Using the Agents

Specialized agents are automatically triggered based on keywords:

| Agent | Triggered By | Purpose |
|-------|--------------|---------|
| Firmware Core | HAL, LL, timer, DMA, interrupt | Core firmware development |
| Peripheral Comm | UART, SPI, I2C, CAN, USB | Communication protocols |
| Peripheral Analog | ADC, DAC, OPAMP | Analog peripherals |
| Power Management | sleep, stop, standby, low power | Power optimization |
| Debug | HardFault, debugging, trace | Troubleshooting |
| Security | TrustZone, crypto, secure boot | Security features |
| Safety | IEC 61508, Class B, self-test | Safety certification |

---

## Network Mode (Tailscale)

Access the server from multiple machines using SSE transport over Tailscale.

### Server Setup

```bash
# Install Tailscale
# See: https://tailscale.com/download

# Start server in network mode
stm32-server --mode network --port 8765

# Or via environment variable
STM32_SERVER_MODE=network stm32-server
```

### Client Configuration

On each client machine, add to `~/.claude.json`:

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

### Test Connection

```bash
curl http://YOUR_TAILSCALE_IP:8765/health
```

---

## Verification

### Quick Check

```bash
# Show installation status
stm32-setup --status

# Verify all components
stm32-setup --verify
```

### Manual Testing

```bash
# Test imports
python -c "from mcp_server.server import mcp; print('MCP server OK')"

# Test database
python -c "
from storage.chroma_store import STM32ChromaStore
store = STM32ChromaStore('data/chroma_db/')
print(f'Documents indexed: {store.count()}')
"

# Test search
python -c "
from storage.chroma_store import STM32ChromaStore
store = STM32ChromaStore('data/chroma_db/')
results = store.search('UART DMA', n_results=3)
for r in results:
    print(f'{r[\"score\"]:.3f}: {r[\"content\"][:80]}...')
"
```

---

## Upgrading

### Plugin Upgrade

```bash
# Uninstall and reinstall the plugin
/plugin uninstall stm32-agents
/plugin install github:creativec09/stm32
```

### Manual Upgrade (Alternative Methods)

```bash
cd stm32-agents
git pull origin main
source .venv/bin/activate
pip install -e . --upgrade

# Re-ingest if needed
stm32-setup --ingest --clear
```

### Update Database Only

```bash
# Re-ingest documentation
python scripts/ingest_docs.py --clear
```

---

## Uninstallation

### Using Plugin System (Recommended)

If you installed via plugin:

```bash
# Remove the plugin (removes agents, commands, MCP config)
/plugin uninstall stm32-agents

# Clean up database (optional)
stm32-uninstall
```

### Manual Uninstall

If you installed via uvx or pip:

```bash
# Remove MCP configuration
claude mcp remove stm32-docs --scope user

# Clean up database
stm32-uninstall

# Uninstall Python package
pip uninstall stm32-mcp-docs
```

### Clean Data Only

```bash
# Remove vector database (keeps installation)
rm -rf data/chroma_db/

# Remove logs
rm -rf logs/*.log
```

---

## Troubleshooting Installation

### Plugin Installation Fails

```bash
# Check Claude Code CLI is available
claude --version

# Check network connectivity
curl https://github.com/creativec09/stm32
```

### "No markdown files found"

The documentation files are missing or not bundled correctly:

```bash
# Check if markdowns are bundled in the package
ls mcp_server/markdowns/

# If missing, reinstall from the git repository
/plugin uninstall stm32-agents
/plugin install github:creativec09/stm32
```

### MCP Server Not Connecting

1. Check configuration:
   ```bash
   claude mcp list
   ```

2. Verify paths in `~/.claude.json` are correct

3. Test server directly:
   ```bash
   stm32-server --validate
   ```

4. Check logs:
   ```bash
   cat logs/mcp_server.log
   ```

### Slow First Request

The first request takes ~90 seconds due to ML model loading. This is normal. Subsequent requests are fast (<100ms).

### Import Errors

```bash
# Verify installation
pip list | grep stm32

# Reinstall
pip install -e . --force-reinstall
```

---

## Environment Variables Reference

| Variable | Description | Default |
|----------|-------------|---------|
| `STM32_SERVER_MODE` | Server mode: `local`, `network`, `hybrid` | `local` |
| `STM32_HOST` | Network bind address | `0.0.0.0` |
| `STM32_PORT` | Network port | `8765` |
| `STM32_CHROMA_DB_PATH` | ChromaDB storage path | `data/chroma_db/` |
| `STM32_COLLECTION_NAME` | ChromaDB collection name | `stm32_docs` |
| `STM32_EMBEDDING_MODEL` | Sentence transformer model | `all-MiniLM-L6-v2` |
| `STM32_CHUNK_SIZE` | Target chunk size (tokens) | `1000` |
| `STM32_CHUNK_OVERLAP` | Chunk overlap (tokens) | `150` |
| `STM32_LOG_LEVEL` | Logging level | `INFO` |
| `STM32_PROJECT_DIR` | Override project directory | Auto-detected |

See [.env.example](.env.example) for the complete list.

---

## Next Steps

After installation:

1. **Try the slash commands**: `/stm32`, `/stm32-hal`, `/stm32-init`, `/stm32-debug`
2. **Explore Agents**: Check [docs/AGENT_QUICK_REFERENCE.md](docs/AGENT_QUICK_REFERENCE.md)
3. **Review Architecture**: See [ARCHITECTURE.md](ARCHITECTURE.md)
4. **Run Tests**: Execute `pytest tests/` to verify everything works

## Getting Help

- **Troubleshooting**: See [TROUBLESHOOTING.md](TROUBLESHOOTING.md)
- **Documentation**: Check the [docs/](docs/) directory
- **Issues**: Open a GitHub issue for bugs or questions
