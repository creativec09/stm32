# STM32 Ingestion Scripts - Quick Start Guide

## Overview

Three production-ready Python scripts for ingesting and managing STM32 documentation with ChromaDB.

## Quick Commands

```bash
# Install dependencies (one-time)
pip install -r requirements.txt

# Ingest all documentation (clear and rebuild)
python scripts/ingest_docs.py --clear -v

# Test search quality
python scripts/test_retrieval.py

# Export sample chunks for inspection
python scripts/export_chunks.py
```

## Scripts Summary

### 1. ingest_docs.py - Main Ingestion

**Purpose**: Converts raw markdown files into searchable vector embeddings

**Key Features**:
- Processes all 80+ markdown files from `/markdowns/`
- Intelligent chunking (1000 tokens default) with overlap
- Extracts rich metadata (peripherals, functions, registers)
- Generates embeddings with semantic search capability
- Detailed progress tracking and statistics

**Usage**:
```bash
# Full re-ingest with clearing
python scripts/ingest_docs.py --clear -v

# Append new files
python scripts/ingest_docs.py

# Custom source directory
python scripts/ingest_docs.py -s /path/to/docs
```

**Output**:
- Progress bar with file count
- Statistics tables (peripherals, document types, top files)
- Error reporting for failed files
- Execution time

### 2. test_retrieval.py - Quality Testing

**Purpose**: Validates search quality after ingestion

**Key Features**:
- 12 curated test queries covering different peripherals
- Filters for GPIO, UART, DMA, ADC, TIM, I2C, SPI, RCC, NVIC
- Returns top 3 results with relevance scores
- Shows source file, peripheral, content preview

**Usage**:
```bash
python scripts/test_retrieval.py
```

**Output Example**:
```
Query: GPIO output mode push pull
Filter: GPIO

[1] Score: 0.847
    Source: gpio_guide.md
    Peripheral: GPIO
    Preview: The GPIO_MODER register controls the mode...
```

### 3. export_chunks.py - Data Export

**Purpose**: Exports indexed chunks to JSON for inspection

**Key Features**:
- Exports up to 100 chunks as JSON
- Includes full metadata for each chunk
- Useful for debugging and integration testing
- Shows total chunk count and storage size

**Usage**:
```bash
python scripts/export_chunks.py
```

**Output**: `data/sample_chunks.json` with structured chunk data

## Typical Workflow

### First Time Setup

```bash
# 1. Ensure dependencies are installed
pip install -r requirements.txt

# 2. Create required directories
python -c "from mcp_server.config import settings; settings.ensure_directories()"

# 3. Clear existing data and ingest everything
python scripts/ingest_docs.py --clear -v

# 4. Verify ingestion was successful
python scripts/test_retrieval.py

# 5. Check sample data
python scripts/export_chunks.py
ls -lh data/sample_chunks.json
```

### Regular Updates

When new documentation files are added:

```bash
# Option 1: Full rebuild (recommended)
python scripts/ingest_docs.py --clear

# Option 2: Append only (faster, but consistency depends on chunking stability)
python scripts/ingest_docs.py

# Verify
python scripts/test_retrieval.py
```

### Monitoring

```bash
# Check database statistics
python -c "from storage.chroma_store import STM32ChromaStore; from mcp_server.config import settings; s = STM32ChromaStore(settings.CHROMA_DB_PATH); print(f'Total: {s.count()} chunks'); print(s.get_peripheral_distribution())"

# Export current sample
python scripts/export_chunks.py
```

## Configuration

All scripts respect settings from `mcp_server/config.py`:

```python
CHUNK_SIZE = 1000              # Target chunk size (tokens)
CHUNK_OVERLAP = 150            # Overlap between chunks
EMBEDDING_MODEL = "all-MiniLM-L6-v2"
CHROMA_DB_PATH = "data/chroma_db/"
RAW_DOCS_DIR = "markdowns/"
```

Override via environment variables:

```bash
export STM32_CHUNK_SIZE=800
export STM32_EMBEDDING_MODEL=all-mpnet-base-v2
python scripts/ingest_docs.py --clear
```

## Expected Results

**After Full Ingestion** (80 markdown files):
- ~2,500-3,000 chunks created
- ~10-20 minutes on CPU (depends on embedding model)
- 400-600 MB ChromaDB storage
- All peripherals represented in metadata

**Search Quality**:
- Relevance scores: 0.7-0.95 for related queries
- < 0.3 for completely unrelated content
- Top result usually most relevant

## File Structure

```
scripts/
├── ingest_docs.py      # 270 lines - Main ingestion script
├── test_retrieval.py   # 85 lines - Search quality tests
└── export_chunks.py    # 50 lines - Data export utility

docs/
├── INGESTION.md        # Full documentation (this file)
└── QUICK_START.md      # Quick reference (this file)
```

## Troubleshooting

**"No documents indexed"**
```bash
# Check markdown files exist
ls markdowns/*.md | wc -l

# Ingest with verbose to see errors
python scripts/ingest_docs.py --clear -v
```

**"Module not found" errors**
```bash
# Reinstall dependencies
pip install --break-system-packages -r requirements.txt
```

**Slow embedding generation**
```bash
# Use faster model
export STM32_EMBEDDING_MODEL=intfloat/e5-small-v2
python scripts/ingest_docs.py --clear
```

**ChromaDB lock error**
```bash
# Use different collection name
export STM32_COLLECTION_NAME=stm32_docs_v2
python scripts/ingest_docs.py --clear
```

## API Usage

After ingestion, use the store directly in your code:

```python
from storage.chroma_store import STM32ChromaStore
from storage.metadata import Peripheral
from mcp_server.config import settings

store = STM32ChromaStore(settings.CHROMA_DB_PATH)

# Search
results = store.search("GPIO configuration", n_results=5)

# Search with filter
results = store.search(
    "PWM output",
    peripheral=Peripheral.TIM,
    require_code=True
)

# Get code examples
examples = store.get_code_examples("initialization")

# Get register docs
reg_docs = store.get_register_info("GPIO_MODER")

# Statistics
stats = store.get_stats()
dist = store.get_peripheral_distribution()
```

## Performance Tips

1. **Fast ingestion**: Use smaller chunk size and overlap
   ```bash
   export STM32_CHUNK_SIZE=500
   export STM32_CHUNK_OVERLAP=50
   ```

2. **Better search quality**: Use larger embedding model
   ```bash
   export STM32_EMBEDDING_MODEL=all-mpnet-base-v2
   ```

3. **GPU acceleration**: Use CUDA if available
   ```bash
   export STM32_EMBEDDING_DEVICE=cuda
   ```

4. **Incremental ingestion**: Append instead of clearing
   ```bash
   python scripts/ingest_docs.py  # Don't use --clear
   ```

## Next Steps

1. **Start MCP Server**: `python -m mcp_server.server`
2. **Connect with Claude Code**: Configure MCP server connection
3. **Use in chat**: Query documentation through Claude interface
4. **Monitor**: Run periodic `test_retrieval.py` to verify quality

## Support

See `/docs/INGESTION.md` for:
- Detailed API documentation
- Metadata extraction details
- Troubleshooting guide
- Performance benchmarks
- Integration examples
