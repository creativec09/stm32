# STM32 Documentation Ingestion Guide

## Overview

The ingestion system processes raw STM32 markdown documentation files from `/markdowns/` into ChromaDB, creating searchable vectors with rich metadata. This enables the MCP server to provide semantic search over the entire STM32 documentation corpus.

## Components

### 1. `scripts/ingest_docs.py` - Main Ingestion Script

The primary tool for ingesting STM32 documentation into ChromaDB.

**Usage:**
```bash
python scripts/ingest_docs.py [OPTIONS]
```

**Options:**
- `--source-dir PATH, -s PATH`: Specify custom source directory (default: from config)
- `--clear, -c`: Clear all existing data before ingestion
- `--verbose, -v`: Show detailed progress for each file

**Examples:**

```bash
# Clear and re-ingest all documentation
python scripts/ingest_docs.py --clear

# Verbose output to see per-file progress
python scripts/ingest_docs.py -v

# Use custom source directory
python scripts/ingest_docs.py --source-dir ./custom_docs

# Combination: clear and verbose
python scripts/ingest_docs.py -c -v
```

**Process Flow:**

1. **Discover Files**: Scans source directory for all `.md` files
2. **Chunking**: Uses STM32Chunker to intelligently split documents:
   - Splits by markdown headers while preserving hierarchy
   - Protects code blocks and tables from being split
   - Maintains token count within configured limits (default: 1000 tokens)
   - Adds overlap between chunks for context (default: 150 tokens)
3. **Metadata Extraction**: For each chunk, extracts:
   - STM32 peripherals mentioned (GPIO, UART, etc.)
   - Document type (reference manual, datasheet, etc.)
   - Section hierarchy
   - HAL function references
   - Register names
   - Content characteristics (has code, has tables, has register maps)
4. **Embedding Generation**: Generates semantic embeddings using the configured model
5. **Storage**: Persists chunks and metadata to ChromaDB

**Output:**

The script displays:
- Progress bar with file count
- Summary statistics table:
  - Files processed
  - Files failed
  - Total chunks created
- Peripheral distribution (top 15)
- Document type distribution
- Top 10 files by chunk count
- List of failed files with error messages
- Total execution time

**Example Output:**

```
╭─────────────────────────────────────────────────────────────────────╮
│                STM32 Documentation Ingestion                        │
│              Source: /path/to/markdowns                            │
╰─────────────────────────────────────────────────────────────────────╯
Found 80 markdown files

████████████████████████████████████████████████████████ 100%
Processing files... 80/80 ✓ [00:05]

┌─ Ingestion Statistics ──────────────────────────────┐
│ Metric               │ Value                         │
├──────────────────────┼───────────────────────────────┤
│ Files Processed      │ 80                            │
│ Files Failed         │ 0                             │
│ Total Chunks         │ 2,847                         │
└──────────────────────┴───────────────────────────────┘

┌─ Chunks by Peripheral (Top 15) ─────────────────────┐
│ Peripheral │ Count                                   │
│ GPIO       │ 340                                     │
│ UART       │ 295                                     │
│ Timer      │ 280                                     │
...
└────────────┴─────────────────────────────────────────┘

Ingestion Complete!
Completed in 5.2 seconds
```

### 2. `scripts/test_retrieval.py` - Test Search Quality

Validates that ingestion was successful and searches work correctly.

**Usage:**
```bash
python scripts/test_retrieval.py
```

**What It Tests:**

Runs 12 test queries covering different peripherals and topics:
- UART baud rate setup
- GPIO output configuration
- DMA circular buffer
- ADC continuous conversion
- Timer PWM generation
- I2C communication
- SPI with DMA
- Clock configuration
- Interrupt handling
- HAL function lookup
- Bootloader documentation
- Power management

**Output:**

For each test query, displays:
- Query text and filters
- Up to 3 matching results with:
  - Relevance score (0.0-1.0)
  - Source file
  - Primary peripheral
  - Content preview (first 200 characters)

**Example Result:**

```
============================================================
Query: GPIO output mode push pull
Filter: GPIO
============================================================

[1] Score: 0.847
    Source: gpio_configuration_guide.md
    Peripheral: GPIO
    Preview: The GPIO_MODER register controls the mode of each GPIO pin...

[2] Score: 0.812
    Source: hal_peripheral_guide.md
    Peripheral: GPIO
    Preview: GPIO_MODE_OUTPUT_PP mode configures the pin as a push-pull...

[3] Score: 0.791
    Source: stm32h7_reference.md
    Peripheral: GPIO
    Preview: Output driver configuration uses GPIO_OTYPER register...
```

### 3. `scripts/export_chunks.py` - Export Sample Data

Exports a sample of indexed chunks to JSON for inspection and debugging.

**Usage:**
```bash
python scripts/export_chunks.py
```

**Output:**

Exports up to 100 chunks to `data/sample_chunks.json` with:
- Chunk ID
- Content (truncated to 500 characters)
- Full content length
- Complete metadata

Useful for:
- Verifying chunk quality
- Inspecting metadata extraction
- Debugging search issues
- Integration testing

**Example JSON:**

```json
[
  {
    "id": "a1b2c3d4_0000_e5f6g7h8",
    "content": "# GPIO Configuration\n\nThe GPIO peripheral provides general-purpose...",
    "content_length": 1250,
    "metadata": {
      "source_file": "gpio_guide.md",
      "doc_type": "reference_manual",
      "peripheral": "GPIO",
      "has_code": true,
      "has_table": false,
      "has_register_map": true,
      "stm32_families": ["STM32F4", "STM32H7"],
      "hal_functions": ["HAL_GPIO_Init", "HAL_GPIO_WritePin"],
      "registers": ["GPIO_MODER", "GPIO_ODR"]
    }
  },
  ...
]
```

## Configuration

The ingestion process uses settings from `mcp_server/config.py`:

**Chunking Settings:**
- `CHUNK_SIZE`: Target chunk size in tokens (default: 1000)
- `CHUNK_OVERLAP`: Overlap between chunks (default: 150)
- `MIN_CHUNK_SIZE`: Minimum viable chunk (default: 50)
- `MAX_CHUNK_SIZE`: Maximum before forced split (default: 2000)
- `PRESERVE_CODE_BLOCKS`: Never split code blocks (default: True)
- `PRESERVE_TABLES`: Never split tables (default: True)

**Embedding Settings:**
- `EMBEDDING_MODEL`: Model for semantic vectors (default: "all-MiniLM-L6-v2")
- `EMBEDDING_BATCH_SIZE`: Batch size for embedding (default: 32)

**Storage Settings:**
- `CHROMA_DB_PATH`: ChromaDB storage directory (default: `data/chroma_db/`)
- `COLLECTION_NAME`: ChromaDB collection name (default: "stm32_docs")
- `RAW_DOCS_DIR`: Raw markdown directory (default: `markdowns/`)

**Override via Environment:**

```bash
export STM32_CHUNK_SIZE=800
export STM32_EMBEDDING_MODEL=all-mpnet-base-v2
python scripts/ingest_docs.py --clear
```

## Workflow

### Initial Setup

```bash
# 1. Install dependencies
pip install -r requirements.txt

# 2. Prepare directories
python -c "from mcp_server.config import settings; settings.ensure_directories()"

# 3. Ingest all documentation (with clearing old data)
python scripts/ingest_docs.py --clear -v

# 4. Test retrieval quality
python scripts/test_retrieval.py

# 5. Export sample for inspection
python scripts/export_chunks.py
```

### Incremental Updates

When new documentation files are added:

```bash
# Option 1: Full re-ingestion (recommended for consistency)
python scripts/ingest_docs.py --clear

# Option 2: Append new chunks (preserves existing data)
python scripts/ingest_docs.py
```

### Maintenance

```bash
# Check current state
python scripts/export_chunks.py

# Re-test after updates
python scripts/test_retrieval.py

# Monitor indexing
python -c "from storage.chroma_store import STM32ChromaStore; from mcp_server.config import settings; store = STM32ChromaStore(settings.CHROMA_DB_PATH); stats = store.get_stats(); print(f'Total chunks: {stats[\"total_chunks\"]}')"
```

## Metadata Extraction

The ingestion system automatically extracts rich metadata from content:

### Peripheral Detection

Identifies STM32 peripherals based on:
- Filename (highest confidence)
- Content keywords with frequency analysis (requires 3+ mentions)

Examples: `GPIO`, `UART`, `SPI`, `I2C`, `ADC`, `DMA`, `RCC`, etc.

### Document Type Classification

Classifies documents by examining:
- Filename patterns (e.g., `_rm.md` for reference manual)
- Content patterns (first 1000 characters)

Examples:
- `reference_manual`: "Reference Manual", "RM" prefix
- `datasheet`: "Datasheet", "DS" prefix
- `application_note`: "Application Note", "AN" prefix
- `user_manual`: "User Guide", "User Manual"
- `programming_manual`: "Programming Manual", "PM" prefix

### Content Characteristics

Automatically detected:
- **has_code**: Contains code blocks (triple backticks)
- **has_table**: Contains markdown tables (pipe characters)
- **has_register**: Contains register definitions or bit field tables
- **hal_functions**: Extracts HAL function names (e.g., `HAL_GPIO_Init`)
- **registers**: Extracts register names (e.g., `GPIO_MODER`)
- **stm32_families**: Identifies STM32 families mentioned (e.g., `STM32F4`, `STM32H7`)

## Troubleshooting

### Issue: "No documents indexed"

**Cause**: Markdown files not found in source directory

**Solution**:
```bash
# Verify files exist
ls /path/to/markdowns/*.md | wc -l

# Check configuration
python -c "from mcp_server.config import settings; print(settings.RAW_DOCS_DIR)"

# Explicit path
python scripts/ingest_docs.py --source-dir /absolute/path/to/markdowns
```

### Issue: "Encoding error" on specific files

**Cause**: File is not UTF-8 encoded

**Solution**:
```bash
# Check file encoding
file -i problem_file.md

# Convert to UTF-8
iconv -f ISO-8859-1 -t UTF-8 problem_file.md > problem_file_fixed.md
```

### Issue: Slow embedding generation

**Cause**: Large dataset or CPU-bound embedding model

**Solutions**:
```bash
# Use faster model
export STM32_EMBEDDING_MODEL=all-MiniLM-L6-v2
# or
export STM32_EMBEDDING_MODEL=intfloat/e5-small-v2

# Increase batch size
export STM32_EMBEDDING_BATCH_SIZE=64

# Use CUDA if available
export STM32_EMBEDDING_DEVICE=cuda
```

### Issue: Low search quality / irrelevant results

**Causes and Solutions**:

1. **Poor chunk quality** - chunks too large or too small:
   ```bash
   export STM32_CHUNK_SIZE=800
   export STM32_CHUNK_OVERLAP=200
   python scripts/ingest_docs.py --clear
   ```

2. **Weak embedding model** - switch to better quality:
   ```bash
   export STM32_EMBEDDING_MODEL=all-mpnet-base-v2
   python scripts/ingest_docs.py --clear
   ```

3. **Insufficient metadata** - check extraction:
   ```bash
   python scripts/export_chunks.py
   # Review data/sample_chunks.json for metadata completeness
   ```

### Issue: "ChromaDB lock" errors

**Cause**: Another process is accessing the database

**Solution**:
```bash
# Wait for other processes to finish, or
# Use a different collection name
export STM32_COLLECTION_NAME=stm32_docs_v2
python scripts/ingest_docs.py --clear
```

### Issue: Out of memory during embedding

**Cause**: Batch size too large for available RAM

**Solution**:
```bash
# Reduce batch size
export STM32_EMBEDDING_BATCH_SIZE=8
python scripts/ingest_docs.py
```

## Performance Benchmarks

On typical hardware (CPU-based embeddings):

- **Ingestion speed**: ~50-100 chunks/second
- **Full dataset** (80 files, ~3000 chunks): 30-60 seconds
- **Embedding generation**: 2-3 chunks/second per thread
- **Storage size**: ~500MB for 3000 chunks with embeddings

With GPU acceleration (CUDA):
- **5-10x faster** embedding generation
- **Full dataset**: 5-10 seconds

## API Integration

After ingestion, the stored data can be accessed via the MCP server:

```python
from storage.chroma_store import STM32ChromaStore
from storage.metadata import Peripheral

store = STM32ChromaStore(...)

# Simple search
results = store.search("GPIO configuration")

# Search with filters
results = store.search(
    "PWM output",
    peripheral=Peripheral.TIM,
    require_code=True
)

# Get code examples
examples = store.get_code_examples("initialization")

# Get register documentation
reg_docs = store.get_register_info("GPIO_MODER")

# Statistics
dist = store.get_peripheral_distribution()
sources = store.list_sources()
```

## File Structure

```
stm32-agents/
├── scripts/
│   ├── ingest_docs.py       # Main ingestion script
│   ├── test_retrieval.py    # Quality testing
│   └── export_chunks.py     # Export sample data
├── data/
│   ├── chroma_db/           # ChromaDB storage
│   └── sample_chunks.json   # Exported sample
├── markdowns/               # Raw markdown files (80+ files)
├── pipeline/
│   └── chunker.py           # Chunking logic
├── storage/
│   ├── chroma_store.py      # ChromaDB wrapper
│   └── metadata.py          # Metadata schemas
└── mcp_server/
    └── config.py            # Configuration
```

## Next Steps

After successful ingestion:

1. **Start the MCP Server**:
   ```bash
   python -m mcp_server.server
   ```

2. **Test with Claude Code**:
   ```bash
   # Configure Claude Code to use the MCP server
   # See ARCHITECTURE.md for integration details
   ```

3. **Monitor Performance**:
   ```bash
   python scripts/export_chunks.py
   python scripts/test_retrieval.py
   ```

## References

- [ChromaDB Documentation](https://docs.trychroma.com/)
- [Sentence Transformers](https://www.sbert.net/)
- [MCP Protocol](https://modelcontextprotocol.io/)
- [STM32 Documentation](https://www.st.com/en/microcontrollers/)
