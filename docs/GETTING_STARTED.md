# Getting Started with STM32 MCP Documentation Server

This guide walks you through setting up and using the STM32 documentation server from scratch.

## Overview

The STM32 MCP Documentation Server provides semantic search over 80 STM32 reference documents (application notes, reference manuals, user manuals) using the Model Context Protocol (MCP). It enables Claude Code to answer questions about STM32 development with accurate, source-backed responses.

## Prerequisites

### Required Software

- **Python 3.11 or higher** - Check with `python --version`
- **pip package manager** - Usually included with Python
- **Claude Code CLI** - The official Claude desktop application
- **Git** (optional) - For cloning the repository

### System Requirements

- **RAM**: 4GB minimum, 8GB recommended
- **Disk Space**: ~1GB for embeddings and database
- **OS**: Linux, macOS, or Windows with WSL2
- **Network**: Optional for Tailscale network mode

## Step 1: Installation

### Create Virtual Environment

Navigate to the project directory and create a Python virtual environment:

```bash
cd /mnt/c/Users/creat/Claude/stm32-agents
python -m venv .venv
```

Activate the virtual environment:

```bash
# Linux/Mac
source .venv/bin/activate

# Windows (PowerShell)
.venv\Scripts\Activate.ps1

# Windows (CMD)
.venv\Scripts\activate.bat
```

You should see `(.venv)` in your terminal prompt.

### Install Dependencies

Install the package in editable mode with all dependencies:

```bash
pip install -e .
```

This installs:
- **MCP framework** - Protocol implementation
- **ChromaDB** - Vector database for embeddings
- **Sentence Transformers** - Embedding generation
- **tiktoken** - Token counting for chunking
- **Rich** - Beautiful CLI output
- **FastAPI/Uvicorn** - HTTP server for network mode
- All other required dependencies

### Verify Installation

Check that key modules can be imported:

```bash
python -c "from mcp_server.config import settings; print('Config:', settings.SERVER_NAME)"
python -c "from storage.chroma_store import STM32ChromaStore; print('Storage: OK')"
python -c "from pipeline.chunker import STM32Chunker; print('Pipeline: OK')"
```

All commands should succeed without errors.

## Step 2: Ingest Documentation

The `markdowns/` directory contains 80 STM32 documentation files that need to be processed and indexed.

### Full Ingestion (First Time)

```bash
python scripts/ingest_docs.py --clear -v
```

Options:
- `--clear` - Removes existing database before ingesting
- `-v` or `--verbose` - Shows detailed progress

This process will:
1. Read all 80 markdown files from `markdowns/`
2. Split documents into semantic chunks (~1000 tokens each with 150 token overlap)
3. Extract metadata (peripherals, HAL functions, registers, document types)
4. Generate embeddings using sentence-transformers
5. Store in ChromaDB vector database

### Expected Output

```
STM32 Documentation Ingestion
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

📁 Source: /mnt/c/Users/creat/Claude/stm32-agents/markdowns
🗄️  Target: /mnt/c/Users/creat/Claude/stm32-agents/data/chroma_db
🔧 Config: chunk_size=1000, overlap=150, model=all-MiniLM-L6-v2

Processing files... ━━━━━━━━━━━━━━━━━━━━━━━━━━━ 80/80 100%

✅ Ingestion Complete
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Ingested: 80 files
Chunks Created: 2,847
Failed: 0 files
Time: 3m 24s

Peripheral Distribution:
┌────────────┬────────┐
│ Peripheral │ Chunks │
├────────────┼────────┤
│ GPIO       │ 342    │
│ UART       │ 287    │
│ SPI        │ 234    │
│ I2C        │ 198    │
│ TIM        │ 276    │
│ ADC        │ 213    │
│ DMA        │ 256    │
│ ...        │ ...    │
└────────────┴────────┘
```

### Timing Expectations

- **With CPU**: 1-5 minutes depending on hardware
- **With GPU**: <1 minute if CUDA available
- **Storage**: ~500MB ChromaDB database

## Step 3: Verify Installation

Run the system validation script:

```bash
python scripts/verify_mcp.py
```

Expected output:

```
STM32 MCP System Verification
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

✅ Project Structure: PASS
   - All required directories present
   - Configuration files found

✅ Module Imports: PASS
   - mcp_server.server ✓
   - storage.chroma_store ✓
   - pipeline.chunker ✓

✅ Configuration: PASS
   - Server name: stm32-docs
   - Database: data/chroma_db/
   - Collection: stm32_docs
   - Embedding model: all-MiniLM-L6-v2

✅ Database: PASS
   - Collection exists
   - Chunks indexed: 2,847
   - Peripherals: 15

✅ Search: PASS
   - Query: "GPIO configuration"
   - Results: 5
   - Top relevance: 0.87

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
All checks passed!
```

## Step 4: Test Search

Run the search quality test:

```bash
python scripts/test_retrieval.py
```

This runs 12 curated test queries covering different peripherals and shows relevance scores. Look for:
- **Top results have scores > 0.7** - Good semantic match
- **Results match the query topic** - Correct peripheral/concept
- **Content previews are relevant** - Actual STM32 documentation

Sample output:

```
STM32 Search Quality Test
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Query: "GPIO output mode configuration"
Filter: GPIO
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

[1] Score: 0.874
    Source: an4899-gpio-hardware-settings.md
    Peripheral: GPIO
    Content: ## GPIO Configuration

             The GPIO_MODER register controls the pin mode...

[2] Score: 0.841
    Source: rm0468-stm32h7-reference.md
    Peripheral: GPIO
    Content: ### Output Configuration

             For push-pull output mode, configure...

[3] Score: 0.798
    Source: an4013-gpio-basics.md
    Peripheral: GPIO
    Content: GPIO pins can be configured in four modes...

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

## Step 5: Configure Claude Code

The MCP server is already configured in `.claude/mcp.json`. Verify the configuration:

```bash
cat .claude/mcp.json
```

You should see:

```json
{
  "mcpServers": {
    "stm32-docs": {
      "command": "python",
      "args": [
        "/mnt/c/Users/creat/Claude/stm32-agents/mcp_server/server.py"
      ],
      "env": {
        "STM32_SERVER_MODE": "local",
        "STM32_LOG_LEVEL": "INFO"
      },
      "description": "STM32 documentation search and retrieval via semantic search"
    }
  }
}
```

Claude Code will automatically:
1. Start the MCP server when needed
2. Communicate via stdio (standard input/output)
3. Make MCP tools available to agents and commands

## Step 6: Use with Claude Code

### Slash Commands

The system provides four slash commands:

#### `/stm32` - General Documentation Search

```bash
/stm32 How do I configure UART with DMA?
/stm32 What are the GPIO alternate functions?
/stm32 SPI clock polarity settings
```

#### `/stm32-init` - Initialization Code

```bash
/stm32-init UART 115200 baud
/stm32-init SPI master mode
/stm32-init GPIO output push-pull
```

#### `/stm32-hal` - HAL Function Lookup

```bash
/stm32-hal HAL_GPIO_Init
/stm32-hal HAL_UART_Transmit_DMA
/stm32-hal HAL_TIM_PWM_Start
```

#### `/stm32-debug` - Troubleshooting

```bash
/stm32-debug UART not receiving data
/stm32-debug I2C returns HAL_TIMEOUT
/stm32-debug SPI clock not working
```

### Natural Language Queries

You can also ask questions naturally. The specialized agents will automatically use MCP tools:

```
User: "Show me how to configure GPIO interrupts"

Claude Code (using firmware agent):
- Calls search_stm32_docs("GPIO interrupt configuration")
- Retrieves relevant documentation
- Provides answer with code examples
```

Example queries:
- "How do I set up UART with DMA for continuous reception?"
- "What's the difference between SPI mode 0 and mode 3?"
- "Why is my ADC returning incorrect values?"
- "Show me an example of I2C master transmit"

### Specialized Agents

The system includes domain-specific agents that automatically search documentation:

| Agent | Purpose | Example Usage |
|-------|---------|---------------|
| **firmware** | Core development | "Configure system clock to 480MHz" |
| **debug** | Troubleshooting | "Why is UART2 not transmitting?" |
| **power** | Power optimization | "How to enter Stop mode?" |
| **peripheral-comm** | Serial protocols | "I2C multi-master configuration" |
| **peripheral-analog** | ADC/DAC | "ADC oversampling setup" |
| **security** | Cryptography | "Enable secure boot" |

See [Agent Quick Reference](AGENT_QUICK_REFERENCE.md) for all agents.

## Step 7: Test MCP Tools Directly

You can also test MCP tools programmatically:

```python
from storage.chroma_store import STM32ChromaStore
from storage.metadata import Peripheral, DocType

# Initialize store
store = STM32ChromaStore("data/chroma_db/")

# Basic search
results = store.search("GPIO configuration", n_results=5)
for i, result in enumerate(results, 1):
    print(f"[{i}] {result.metadata['source_file']}")
    print(f"    Score: {result.relevance_score:.3f}")
    print(f"    {result.content[:100]}...")

# Search with peripheral filter
results = store.search(
    "PWM output",
    peripheral=Peripheral.TIM,
    n_results=3
)

# Get code examples
examples = store.get_code_examples("initialization", n_results=5)

# Get HAL function documentation
hal_docs = store.search_function("HAL_GPIO_Init")

# Get peripheral documentation
gpio_docs = store.get_peripheral_docs(Peripheral.GPIO, n_results=10)
```

## Network Mode (Optional)

For accessing the documentation server from multiple machines via Tailscale:

### Start Server in Network Mode

```bash
STM32_SERVER_MODE=network python scripts/start_server.py --port 8765
```

The server will:
1. Start HTTP server on port 8765
2. Expose Server-Sent Events (SSE) endpoint
3. Listen on all interfaces (0.0.0.0)

### Configure Client Machines

On other machines with Claude Code, update `.claude/mcp.json`:

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

Replace `100.x.x.x` with your machine's Tailscale IP address.

### Test Network Connection

```bash
# From client machine
curl http://100.x.x.x:8765/health

# Should return:
{"status": "healthy", "chunks": 2847}
```

## Troubleshooting

### "No module named 'tiktoken'"

Dependencies not installed. Activate virtual environment and reinstall:

```bash
source .venv/bin/activate
pip install -e .
```

### "No documentation found" or 0 chunks

Database is empty. Run ingestion:

```bash
python scripts/ingest_docs.py --clear -v
```

### Import Errors

Ensure you're in the project root and virtual environment is activated:

```bash
cd /mnt/c/Users/creat/Claude/stm32-agents
source .venv/bin/activate
python scripts/verify_mcp.py
```

### Search Returns Irrelevant Results

1. Check embedding model quality:
```bash
# Use better model (slower but more accurate)
export STM32_EMBEDDING_MODEL=all-mpnet-base-v2
python scripts/ingest_docs.py --clear
```

2. Try more specific queries with peripheral filters
3. Verify database has sufficient chunks (should be 2500+)

### Server Won't Start

Check configuration:

```bash
python -c "from mcp_server.config import settings; print(settings)"
```

Verify database exists:

```bash
ls -lh data/chroma_db/
python -c "from storage.chroma_store import STM32ChromaStore; s = STM32ChromaStore('data/chroma_db/'); print(f'Chunks: {s.count()}')"
```

### Slow Embedding Generation

Use a smaller or faster model:

```bash
export STM32_EMBEDDING_MODEL=intfloat/e5-small-v2
python scripts/ingest_docs.py --clear
```

Or use GPU if available:

```bash
export STM32_EMBEDDING_DEVICE=cuda
python scripts/ingest_docs.py --clear
```

### ChromaDB Lock Error

Another process is using the database. Stop all servers and retry:

```bash
# Kill any running servers
pkill -f "mcp_server/server.py"

# Or use a different collection
export STM32_COLLECTION_NAME=stm32_docs_v2
python scripts/ingest_docs.py --clear
```

## Next Steps

Now that your system is set up:

1. **Read the Architecture** - [ARCHITECTURE.md](ARCHITECTURE.md) for system overview
2. **Explore MCP Server** - [MCP_SERVER.md](MCP_SERVER.md) for server details
3. **Learn Advanced Tools** - [ADVANCED_TOOLS.md](ADVANCED_TOOLS.md) for all search tools
4. **Configure Agents** - [AGENT_MCP_INTEGRATION.md](AGENT_MCP_INTEGRATION.md) for agent setup
5. **Run Tests** - [TESTING.md](TESTING.md) for test suite

## Common Workflows

### Daily Development

```bash
# Start Claude Code - it automatically starts MCP server
# Use slash commands or natural language queries
/stm32 your query here
```

### Update Documentation

```bash
# Add new markdown files to markdowns/
# Re-ingest
python scripts/ingest_docs.py --clear

# Verify
python scripts/test_retrieval.py
```

### Monitor System

```bash
# Check database statistics
python -c "from storage.chroma_store import STM32ChromaStore; s = STM32ChromaStore('data/chroma_db/'); print(f'Chunks: {s.count()}'); print(s.get_peripheral_distribution())"

# Export sample data
python scripts/export_chunks.py
cat data/sample_chunks.json
```

### Development Mode

```bash
# Install dev dependencies
pip install -e ".[dev]"

# Run tests
pytest tests/

# Run validation
python scripts/verify_mcp.py
```

## Support

- **Documentation Index**: [INDEX.md](INDEX.md)
- **Quick Reference**: [QUICK_START.md](QUICK_START.md)
- **Testing Guide**: [TESTING.md](TESTING.md)
- **Configuration**: [INFRASTRUCTURE.md](INFRASTRUCTURE.md)

## Configuration Reference

Key environment variables:

```bash
# Server
STM32_SERVER_MODE=local          # local, network, or hybrid
STM32_SERVER_NAME=stm32-docs
STM32_HOST=0.0.0.0
STM32_PORT=8765

# Database
STM32_CHROMA_DB_PATH=data/chroma_db/
STM32_COLLECTION_NAME=stm32_docs
STM32_EMBEDDING_MODEL=all-MiniLM-L6-v2

# Processing
STM32_CHUNK_SIZE=1000
STM32_CHUNK_OVERLAP=150
STM32_RAW_DOCS_DIR=markdowns/

# Search
STM32_DEFAULT_SEARCH_RESULTS=5
STM32_MAX_SEARCH_RESULTS=10

# Logging
STM32_LOG_LEVEL=INFO
STM32_LOG_FILE=logs/server.log
```

See [.env.example](.env.example) for all options.
