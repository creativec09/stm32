# Storage Layer

Vector database storage layer for the STM32 MCP Documentation Server.

## Overview

This package provides persistent storage and semantic search capabilities for STM32 documentation chunks using ChromaDB as the vector database backend.

## Components

### `metadata.py`
Defines metadata schemas for documentation chunks:
- **ChunkMetadataSchema**: Pydantic model for chunk metadata
- **DocType**: Enumeration of document types (Reference Manual, HAL Guide, etc.)
- **Peripheral**: Enumeration of STM32 peripherals (GPIO, UART, SPI, etc.)
- **ContentType**: Enumeration of content types (Conceptual, Code Example, Register Map, etc.)

### `chroma_store.py`
ChromaDB wrapper providing high-level storage operations:
- **STM32ChromaStore**: Main storage interface
  - Add/delete chunks
  - Semantic search with metadata filtering
  - Peripheral-specific queries
  - Code example retrieval
  - Register documentation lookup
  - HAL function search
  - Statistics and analytics

## Quick Start

```python
from pathlib import Path
from storage import STM32ChromaStore, ChunkMetadataSchema, DocType, Peripheral

# Initialize store
store = STM32ChromaStore(Path("./data/chroma_db"))

# Create metadata
meta = ChunkMetadataSchema(
    source_file="stm32f4_reference.md",
    doc_type=DocType.REFERENCE_MANUAL,
    peripheral=Peripheral.GPIO,
    has_code=True,
    section_path=["GPIO", "Configuration"],
    hal_functions=["HAL_GPIO_Init"],
    registers=["GPIO_MODER", "GPIO_ODR"]
)

# Add chunk
store.add_chunks([
    ("chunk_001", "GPIO configuration text...", meta.to_chroma_metadata())
])

# Search
results = store.search(
    query="How to configure GPIO?",
    peripheral=Peripheral.GPIO,
    require_code=True,
    n_results=5
)

for result in results:
    print(f"Score: {result['score']:.3f}")
    print(f"Content: {result['content'][:100]}...")
```

## Features

### Semantic Search
- Vector embeddings using sentence-transformers
- Cosine similarity ranking
- Configurable result count and score thresholds

### Metadata Filtering
Filter by:
- Peripheral type (GPIO, UART, SPI, etc.)
- Document type (Reference Manual, HAL Guide, etc.)
- Content flags (has_code, has_register_map, has_table)
- STM32 family (F4, H7, L4, etc.)

### Specialized Queries
- **Peripheral Search**: Get all docs for a specific peripheral
- **Code Examples**: Find code snippets for a topic
- **Register Info**: Lookup register documentation
- **HAL Functions**: Search for HAL/LL function usage

### Analytics
- Chunk count and distribution statistics
- Peripheral coverage analysis
- Document type distribution
- Source file tracking

## Architecture

```
STM32ChromaStore
├── ChromaDB (Vector Database)
│   ├── Embeddings (all-MiniLM-L6-v2)
│   ├── Metadata (Flattened)
│   └── Persistence (Disk)
│
├── Search Methods
│   ├── Semantic Search
│   ├── Filtered Search
│   ├── Peripheral Search
│   ├── Code Example Search
│   └── Register Search
│
└── Management
    ├── Add/Delete Chunks
    ├── Statistics
    └── Distribution Analysis
```

## Configuration

### Storage Location
```python
store = STM32ChromaStore(
    persist_dir=Path("./data/chroma_db"),  # Persistent storage directory
    collection_name="stm32_docs",          # Collection name
    embedding_model="all-MiniLM-L6-v2",   # Embedding model
    distance_metric="cosine"               # Distance metric
)
```

### Embedding Model Options
- **all-MiniLM-L6-v2** (default): Fast, 384 dimensions
- **all-mpnet-base-v2**: Better quality, 768 dimensions
- **multi-qa-MiniLM-L6-cos-v1**: Optimized for Q&A

### Distance Metrics
- **cosine** (default): Best for semantic similarity
- **l2**: Euclidean distance
- **ip**: Inner product

## Testing

Run the test suite:
```bash
pytest tests/test_storage.py -v
```

Run the standalone test:
```bash
python storage/chroma_store.py
```

## Performance

### Benchmarks (approximate)
- **Add 1000 chunks**: ~5-10 seconds
- **Search query**: 100-500ms
- **Storage per chunk**: ~2.5KB
- **Memory usage**: ~100MB + embedding model (~100MB)

### Optimization Tips
1. Batch chunk additions for better performance
2. Use appropriate n_results to limit processing
3. Apply filters to reduce search space
4. Consider min_score thresholds for quality

## Requirements

- Python 3.11+
- chromadb >= 0.4.22
- sentence-transformers >= 2.2.2
- pydantic >= 2.5.0

See `requirements.txt` for full dependencies.

## Documentation

See `/docs/STORAGE.md` for comprehensive documentation including:
- Detailed API reference
- Metadata schema documentation
- Search strategies and best practices
- Integration examples
- Troubleshooting guide

## Examples

### Example 1: Multi-Peripheral Search
```python
# Search across multiple peripherals
results = store.search("DMA configuration", n_results=10)

# Group by peripheral
by_peripheral = {}
for result in results:
    periph = result['metadata']['peripheral']
    if periph not in by_peripheral:
        by_peripheral[periph] = []
    by_peripheral[periph].append(result)
```

### Example 2: Code Example Collection
```python
# Collect initialization examples for all communication peripherals
comm_peripherals = [Peripheral.UART, Peripheral.SPI, Peripheral.I2C]

examples = {}
for periph in comm_peripherals:
    examples[periph.value] = store.get_code_examples(
        topic="initialization",
        peripheral=periph,
        n_results=3
    )
```

### Example 3: Documentation Coverage Analysis
```python
# Analyze documentation coverage
stats = store.get_stats()
print(f"Total chunks: {stats['total_chunks']}")

periph_dist = store.get_peripheral_distribution()
print("\nPeripheral coverage:")
for periph, count in sorted(periph_dist.items(), key=lambda x: x[1], reverse=True):
    print(f"  {periph}: {count} chunks")

doc_dist = store.get_doc_type_distribution()
print("\nDocument types:")
for doc_type, count in doc_dist.items():
    print(f"  {doc_type}: {count} chunks")
```

## License

MIT License - See LICENSE file for details.
