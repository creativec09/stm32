# Installation Guide

This guide provides detailed installation instructions for the STM32 MCP Documentation Server.

## Table of Contents

- [Prerequisites](#prerequisites)
- [Private Distribution via uvx (Recommended)](#private-distribution-via-uvx-recommended)
- [Quick Install (Clone-and-Go)](#quick-install-clone-and-go)
- [What Gets Installed](#what-gets-installed)
- [Alternative Installation Methods](#alternative-installation-methods)
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

## Private Distribution via uvx (Recommended)

The fastest way to use this MCP server from a private repository is via `uvx`. This method:
- Automatically installs dependencies
- No need to clone the repository
- Works with version tags for reproducible installations
- Caches the package for fast subsequent launches

### Prerequisites

1. **Install uv** (a fast Python package installer and runner):
   ```bash
   curl -LsSf https://astral.sh/uv/install.sh | sh
   ```

2. **GitHub Personal Access Token (PAT)** with `repo` scope:
   - Go to GitHub Settings > Developer settings > Personal access tokens
   - Generate a new token with `repo` scope
   - Save the token securely

### Add to Claude Code

```bash
# Replace TOKEN with your GitHub Personal Access Token
claude mcp add stm32-docs -s user -- uvx --from git+https://TOKEN@github.com/creativec09/stm32-agents.git stm32-mcp-docs
```

### Using a Specific Version Tag

For production use, pin to a specific version:

```bash
# Install from a tagged release (recommended for stability)
claude mcp add stm32-docs -s user -- uvx --from git+https://TOKEN@github.com/creativec09/stm32-agents.git@v1.0.0 stm32-mcp-docs
```

Available tags:
- `v1.0.0` - Initial stable release

### Environment Variables

If you need to pass environment variables to the MCP server, add them to your Claude config manually:

Edit `~/.claude.json`:
```json
{
  "mcpServers": {
    "stm32-docs": {
      "command": "uvx",
      "args": ["--from", "git+https://TOKEN@github.com/creativec09/stm32-agents.git", "stm32-mcp-docs"],
      "env": {
        "STM32_SERVER_MODE": "local",
        "STM32_LOG_LEVEL": "INFO"
      }
    }
  }
}
```

### Verify Installation

After adding to Claude Code:

```bash
# List configured MCP servers
claude mcp list

# Restart Claude Code, then test with:
/stm32 How do I configure UART with DMA?
```

### Updating

To update to a newer version:

```bash
# Remove old configuration
claude mcp remove stm32-docs -s user

# Add with new version
claude mcp add stm32-docs -s user -- uvx --from git+https://TOKEN@github.com/creativec09/stm32-agents.git@v1.1.0 stm32-mcp-docs
```

---

## Quick Install (Clone-and-Go)

The MCP server features **automatic database building** on first run. Just install and start using - the documentation index builds automatically from the included markdown files!

### Clone-and-Go Setup

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

# Register with Claude Code (recommended method)
claude mcp add stm32-docs -s user -- python -m mcp_server

# (Optional) Run complete setup for agents and slash commands
stm32-setup
```

The `stm32-setup` command automatically:
- Uses `claude mcp add` when available (with manual fallback)
- Installs all agents to `~/.claude/agents/`
- Installs slash commands to `~/.claude/commands/`
- Verifies the installation

**Auto-Ingestion**: On first use, the MCP server automatically detects an empty database and ingests the bundled STM32 documentation. This takes 5-10 minutes and you will see progress logs like:

```
Database empty, starting auto-ingestion...
Found 80 markdown files in mcp_server/markdowns/
[10/80] Processed an4013-introduction-to-timers...
[20/80] Processed an4435-guidelines-for-obtaining...
...
Ingestion complete!
Ready - 13,815 chunks indexed
```

### Development Install (with Re-ingestion)

For development or to force rebuild the vector database:

```bash
# 1. Clone the repository
git clone https://github.com/creativec09/stm32-agents.git
cd stm32-agents

# 2. Create and activate virtual environment
python -m venv .venv
source .venv/bin/activate  # Linux/macOS
# .venv\Scripts\activate   # Windows PowerShell

# 3. Install the package
pip install -e .

# 4. (Optional) Force re-ingestion to rebuild database
stm32-setup --ingest --clear

# Or delete the database to trigger auto-ingestion on next start
rm -rf data/chroma_db/
```

### Verify It Works

```bash
# List configured MCP servers
claude mcp list

# Check installation status
stm32-setup --status

# Or restart Claude Code and try:
/stm32 How do I configure UART with DMA?
```

---

## What Gets Installed

| Component | Location | Installed By |
|-----------|----------|--------------|
| Python package | Site-packages or editable | `pip install` |
| MCP server config | User config (via `claude mcp add`) | `claude mcp add` or `stm32-setup` |
| Project MCP config | `.mcp.json` (project root) | Already in repository |
| Agent definitions | `~/.claude/agents/*.md` | `stm32-setup` |
| Slash commands | `~/.claude/commands/*.md` | `stm32-setup` |
| Vector database | `data/chroma_db/` | Auto-built on first run or `stm32-setup --ingest` |
| CLI commands | `stm32-*` | `pip install` |

### CLI Commands Available After Install

| Command | Description |
|---------|-------------|
| `stm32-setup` | Complete setup wizard |
| `stm32-setup --status` | Show installation status |
| `stm32-setup --verify` | Verify installation |
| `stm32-server` | Start the MCP server |
| `stm32-ingest` | Ingest documentation (auto-runs on first start if needed) |
| `stm32-search` | Search from command line |
| `stm32-validate` | Full system validation |

---

## Alternative Installation Methods

### Option A: Selective Setup

Run only specific setup steps:

```bash
# Only configure MCP server
stm32-setup --mcp-only

# Only install agents
stm32-setup --agents

# Only ingest documentation
stm32-setup --ingest

# Re-ingest (clear and rebuild)
stm32-setup --ingest --clear
```

### Option B: Re-build Database from Source

The pre-built database is included via Git LFS. To rebuild from scratch:

```bash
# Clone and install
git clone https://github.com/creativec09/stm32-agents.git
cd stm32-agents
python -m venv .venv && source .venv/bin/activate
pip install -e .

# Force re-ingestion (rebuilds database from markdown files)
stm32-setup --ingest --clear

# Or use the ingest script directly
python scripts/ingest_docs.py --clear
```

### Option C: Install from GitHub (Without Clone)

```bash
# Create project directory
mkdir stm32-docs-server && cd stm32-docs-server

# Create virtual environment
python -m venv .venv
source .venv/bin/activate

# Install from GitHub
pip install git+https://github.com/creativec09/stm32-agents.git

# Clone to get documentation files
git clone https://github.com/creativec09/stm32-agents.git source

# Set project directory for setup
export STM32_PROJECT_DIR=$(pwd)/source

# Run setup
stm32-setup
```

### Option D: Development Installation

For contributors and customization:

```bash
git clone https://github.com/creativec09/stm32-agents.git
cd stm32-agents
python -m venv .venv
source .venv/bin/activate

# Install with development dependencies
pip install -e ".[dev]"

# Install pre-commit hooks
pre-commit install

# Run setup
stm32-setup
```

---

## Post-Installation Setup

### Automatic Setup (Default)

The `stm32-setup` command handles everything. Just run it after `pip install`.

### Manual Configuration (If Needed)

If you prefer manual control, here's what `stm32-setup` does:

#### 1. MCP Configuration

**Recommended: Use Claude CLI**
```bash
claude mcp add stm32-docs -s user -- python -m mcp_server
```

**Alternative: Project-level config**
The repository includes a `.mcp.json` file at the project root that Claude Code automatically detects when you open the project directory:
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

**Fallback: Manual user config**
If the Claude CLI is not available, add to `~/.claude.json`:
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

#### 2. Agent Installation

```bash
mkdir -p ~/.claude/agents ~/.claude/commands
cp .claude/agents/*.md ~/.claude/agents/
cp .claude/commands/*.md ~/.claude/commands/
```

#### 3. Document Ingestion

```bash
python scripts/ingest_docs.py --clear
```

---

## Claude Code Integration

### Local Mode (Default)

Local mode uses stdio transport - Claude Code launches the server directly.

After running `claude mcp add stm32-docs -s user -- python -m mcp_server`, restart Claude Code and test:

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

On each client machine, add to `~/.claude/mcp.json`:

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

### Detailed Validation

```bash
# Full system validation
stm32-validate

# Verify MCP specifically
stm32-verify

# Test search quality
stm32-test-retrieval
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

### From Git

```bash
cd stm32-agents
git pull origin main
source .venv/bin/activate
pip install -e . --upgrade

# Re-run setup to update agents and re-ingest if needed
stm32-setup --force
```

### From pip

```bash
pip install --upgrade git+https://github.com/creativec09/stm32-agents.git
stm32-setup --force
```

### Update Database Only

```bash
# Re-ingest documentation
stm32-setup --ingest --clear

# Or download latest pre-built
python scripts/download_db.py --force
```

---

## Uninstallation

### Using Claude CLI (Recommended)

```bash
# Remove the MCP server configuration
claude mcp remove stm32-docs -s user

# Then uninstall the Python package
pip uninstall stm32-mcp-docs
```

### Using the Uninstall Command

```bash
# Remove MCP config, agents, and commands from ~/.claude
stm32-setup --uninstall

# Then uninstall the Python package
pip uninstall stm32-mcp-docs
```

### Manual Removal

```bash
# Remove from MCP configuration using Claude CLI
claude mcp remove stm32-docs -s user

# Or manually edit ~/.claude.json and remove "stm32-docs" entry

# Remove agents
rm ~/.claude/agents/{router,firmware,power,debug,safety,bootloader,security}*.md
rm ~/.claude/agents/{peripheral,hardware,triage}*.md

# Remove commands
rm ~/.claude/commands/stm32*.md

# Uninstall package
pip uninstall stm32-mcp-docs

# Remove project directory
rm -rf /path/to/stm32-agents
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

### "stm32-setup: command not found"

The package isn't installed or not in PATH:

```bash
# Ensure virtual environment is active
source .venv/bin/activate

# Reinstall
pip install -e .
```

### "No markdown files found"

The documentation files are missing or not bundled correctly:

```bash
# Check if markdowns are bundled in the package
ls mcp_server/markdowns/

# If missing, reinstall from the git repository to get bundled docs:
uvx --from git+https://github.com/creativec09/stm32-agents.git stm32-mcp-docs
# Or clone and install in editable mode:
git clone https://github.com/creativec09/stm32-agents.git
cd stm32-agents && pip install -e .
```

### MCP Server Not Connecting

1. Check configuration:
   ```bash
   stm32-setup --status
   ```

2. Verify paths in `~/.claude/mcp.json` are correct

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
