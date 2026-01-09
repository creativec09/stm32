# STM32 MCP Documentation Server - Infrastructure Guide

This document describes the project infrastructure, configuration options, and setup instructions for the STM32 MCP Documentation Server.

## Table of Contents

1. [Overview](#overview)
2. [Directory Structure](#directory-structure)
3. [Configuration Options](#configuration-options)
4. [Environment Variables](#environment-variables)
5. [Installation](#installation)
6. [Quick Start](#quick-start)
7. [Server Modes](#server-modes)
8. [Troubleshooting](#troubleshooting)

---

## Overview

The STM32 MCP Documentation Server provides semantic search capabilities over STM32 microcontroller documentation through the Model Context Protocol (MCP). It supports:

- **Local Mode**: stdio-based connections for local Claude Code integration
- **Network Mode**: HTTP/SSE connections for Tailscale network access
- **Hybrid Mode**: Both local and network modes simultaneously

The server uses ChromaDB for vector storage and sentence-transformers for embedding generation.

---

## Directory Structure

```
stm32-agents/
├── mcp_server/              # Main MCP server package
│   ├── __init__.py          # Package initialization
│   ├── config.py            # Configuration management (pydantic-settings)
│   ├── server.py            # Main server implementation
│   ├── tools/               # MCP tool implementations
│   │   ├── __init__.py
│   │   ├── search.py        # Search tools
│   │   ├── examples.py      # Code example tools
│   │   └── peripheral.py    # Peripheral-specific tools
│   ├── resources/           # MCP resource handlers
│   │   ├── __init__.py
│   │   └── handlers.py      # Resource URI handlers
│   └── prompts/             # MCP prompt templates
│       ├── __init__.py
│       └── templates.py     # Prompt definitions
│
├── pipeline/                # Document processing pipeline
│   ├── __init__.py
│   ├── chunker.py           # Markdown chunking
│   ├── embedder.py          # Embedding generation
│   ├── ingester.py          # Full ingestion pipeline
│   └── validator.py         # Chunk validation
│
├── storage/                 # Persistence layer
│   ├── __init__.py
│   ├── chroma_store.py      # ChromaDB wrapper
│   └── metadata.py          # Metadata schemas
│
├── scripts/                 # CLI scripts
│   ├── __init__.py
│   ├── start_server.py      # Server launcher
│   ├── ingest_docs.py       # Document ingestion
│   ├── test_retrieval.py    # Search testing
│   └── validate_system.py   # System validation
│
├── data/                    # Data storage
│   ├── raw/                 # Raw input data (if any)
│   ├── chunks/              # Processed chunk JSON files
│   └── chroma_db/           # ChromaDB persistent storage
│
├── markdowns/               # Source documentation (78 markdown files)
│   └── *.md                 # STM32 reference documentation
│
├── tests/                   # Test suite
│   ├── __init__.py
│   ├── conftest.py          # Pytest fixtures
│   ├── test_chunking.py
│   ├── test_search.py
│   ├── test_mcp_tools.py
│   └── test_integration.py
│
├── logs/                    # Log files
│   └── *.log
│
├── docs/                    # Documentation
│   └── INFRASTRUCTURE.md    # This file
│
├── pyproject.toml           # Project configuration
├── requirements.txt         # Production dependencies
├── requirements-dev.txt     # Development dependencies
├── .env.example             # Environment variable template
└── .gitignore               # Git ignore rules
```

---

## Configuration Options

Configuration is managed through `mcp_server/config.py` using pydantic-settings. All options can be set via environment variables with the `STM32_` prefix.

### Server Configuration

| Option | Default | Description |
|--------|---------|-------------|
| `SERVER_MODE` | `hybrid` | Server mode: `local`, `network`, or `hybrid` |
| `HOST` | `0.0.0.0` | Network bind address |
| `PORT` | `8765` | Network port |
| `SERVER_NAME` | `stm32-docs` | MCP server name |
| `SERVER_VERSION` | `1.0.0` | Server version |

### Chunking Configuration

| Option | Default | Description |
|--------|---------|-------------|
| `CHUNK_SIZE` | `1000` | Target chunk size in tokens |
| `CHUNK_OVERLAP` | `150` | Overlap between chunks |
| `MIN_CHUNK_SIZE` | `50` | Minimum valid chunk size |
| `MAX_CHUNK_SIZE` | `2000` | Maximum chunk size |
| `PRESERVE_CODE_BLOCKS` | `true` | Keep code blocks intact |
| `PRESERVE_TABLES` | `true` | Keep tables intact |

### Embedding Configuration

| Option | Default | Description |
|--------|---------|-------------|
| `EMBEDDING_MODEL` | `all-MiniLM-L6-v2` | Sentence transformer model |
| `EMBEDDING_BATCH_SIZE` | `32` | Batch size for embedding |
| `EMBEDDING_DEVICE` | `cpu` | Device: `cpu`, `cuda`, `mps` |
| `NORMALIZE_EMBEDDINGS` | `true` | Normalize vectors |

### ChromaDB Configuration

| Option | Default | Description |
|--------|---------|-------------|
| `COLLECTION_NAME` | `stm32_docs` | ChromaDB collection name |
| `CHROMA_DISTANCE_METRIC` | `cosine` | Distance metric |

### Search Configuration

| Option | Default | Description |
|--------|---------|-------------|
| `DEFAULT_SEARCH_RESULTS` | `5` | Default result count |
| `MAX_SEARCH_RESULTS` | `20` | Maximum result count |
| `MIN_RELEVANCE_SCORE` | `0.3` | Minimum relevance threshold |

### Logging Configuration

| Option | Default | Description |
|--------|---------|-------------|
| `LOG_LEVEL` | `INFO` | Logging level |
| `LOG_TO_FILE` | `true` | Write logs to file |
| `LOG_FILE_MAX_SIZE` | `10485760` | Max log file size (10MB) |
| `LOG_FILE_BACKUP_COUNT` | `5` | Backup file count |

---

## Environment Variables

All environment variables use the `STM32_` prefix. Copy `.env.example` to `.env` and modify as needed:

```bash
cp .env.example .env
```

### Essential Variables

```bash
# Server mode (local/network/hybrid)
STM32_SERVER_MODE=hybrid

# Network settings
STM32_HOST=0.0.0.0
STM32_PORT=8765

# Embedding model
STM32_EMBEDDING_MODEL=all-MiniLM-L6-v2

# Logging
STM32_LOG_LEVEL=INFO
```

### Path Variables (Auto-detected)

These are automatically detected based on project structure but can be overridden:

```bash
# Typically not needed - auto-detected
STM32_PROJECT_ROOT=/path/to/stm32-agents
```

---

## Installation

### Prerequisites

- Python 3.11 or higher
- pip or uv package manager
- 4GB+ RAM (for embedding model)

### Step 1: Clone/Navigate to Project

```bash
cd /mnt/c/Users/creat/Claude/stm32-agents
```

### Step 2: Create Virtual Environment

```bash
# Using venv
python -m venv .venv
source .venv/bin/activate  # Linux/macOS
# or
.venv\Scripts\activate     # Windows

# Using uv (faster)
uv venv
source .venv/bin/activate
```

### Step 3: Install Dependencies

```bash
# Production dependencies
pip install -r requirements.txt

# Development dependencies (includes testing, linting)
pip install -r requirements-dev.txt

# Or install as editable package
pip install -e .
pip install -e ".[dev]"
```

### Step 4: Configure Environment

```bash
cp .env.example .env
# Edit .env with your settings
```

### Step 5: Ingest Documentation

```bash
# Ingest markdown files into ChromaDB
python scripts/ingest_docs.py

# Or with installed command
stm32-ingest
```

### Step 6: Validate Setup

```bash
# Run system validation
python scripts/validate_system.py

# Or with installed command
stm32-validate
```

---

## Quick Start

### Start Server (Local Mode)

```bash
# Using script
python scripts/start_server.py --mode local

# Using installed command
stm32-docs
```

### Start Server (Network Mode)

```bash
# Using script
python scripts/start_server.py --mode network --port 8765

# Using installed command with environment
STM32_SERVER_MODE=network stm32-docs
```

### Start Server (Hybrid Mode)

```bash
# Both local and network
python scripts/start_server.py --mode hybrid --port 8765
```

### Test Search

```bash
# Run search tests
python scripts/test_retrieval.py

# Or with installed command
stm32-test-retrieval
```

---

## Server Modes

### Local Mode (stdio)

- Uses standard input/output for MCP protocol
- Connects to local Claude Code installations
- No network exposure

```bash
STM32_SERVER_MODE=local stm32-docs
```

### Network Mode (HTTP/SSE)

- HTTP server with Server-Sent Events
- Accessible over Tailscale network
- Binds to configured host/port

```bash
STM32_SERVER_MODE=network STM32_PORT=8765 stm32-docs
```

### Hybrid Mode (Both)

- Runs both local and network transports
- Recommended for development
- Default mode

```bash
STM32_SERVER_MODE=hybrid stm32-docs
```

---

## Troubleshooting

### Common Issues

#### Import Errors

Ensure you have installed the package correctly:

```bash
pip install -e .
```

#### ChromaDB Errors

If ChromaDB fails to initialize:

```bash
# Clear and rebuild the database
rm -rf data/chroma_db/
stm32-ingest --clear
```

#### Memory Issues

If embedding model fails to load:

```bash
# Use a smaller model
STM32_EMBEDDING_MODEL=all-MiniLM-L6-v2 stm32-ingest
```

#### Port Already in Use

```bash
# Use a different port
STM32_PORT=8766 stm32-docs
```

### Logs

Check logs for detailed error information:

```bash
# View recent logs
tail -f logs/stm32-docs.log
```

### Validation

Run the validation script to check system health:

```bash
stm32-validate
```

This checks:
- Configuration loading
- Directory structure
- ChromaDB connectivity
- Embedding model availability
- Sample search functionality

---

## Additional Resources

- [MCP Protocol Documentation](https://modelcontextprotocol.io)
- [ChromaDB Documentation](https://docs.trychroma.com)
- [Sentence Transformers](https://www.sbert.net)
- [Pydantic Settings](https://docs.pydantic.dev/latest/concepts/pydantic_settings/)

---

*Last updated: January 2026*
