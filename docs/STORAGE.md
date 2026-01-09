# Storage Layer Documentation

This document describes the storage layer for the STM32 MCP Documentation Server, including the metadata schema, ChromaDB configuration, and usage examples.

## Overview

The storage layer provides a vector database solution for storing and retrieving STM32 documentation chunks with rich metadata. It uses:
- **ChromaDB**: Vector database for semantic search
- **Sentence Transformers**: Embedding generation (all-MiniLM-L6-v2)
- **Pydantic**: Schema validation and serialization

## Architecture

```
┌─────────────────────────────────────────────────────────┐
│                    Storage Layer                        │
├─────────────────────────────────────────────────────────┤
│                                                         │
│  ┌──────────────┐         ┌─────────────────────────┐  │
│  │   Metadata   │         │   STM32ChromaStore      │  │
│  │   Schemas    │◄────────┤   - Add chunks          │  │
│  │              │         │   - Search              │  │
│  │  - DocType   │         │   - Filter by metadata  │  │
│  │  - Peripheral│         │   - Statistics          │  │
│  │  - ContentType         │                         │  │
│  └──────────────┘         └────────┬────────────────┘  │
│                                    │                    │
│                           ┌────────▼────────┐           │
│                           │   ChromaDB      │           │
│                           │   - Embeddings  │           │
│                           │   - Persistence │           │
│                           │   - Vector Search│          │
│                           └─────────────────┘           │
└─────────────────────────────────────────────────────────┘
```

## Metadata Schema

### ChunkMetadataSchema

The `ChunkMetadataSchema` class defines all metadata associated with a documentation chunk.

#### Field Categories

##### 1. Source Identification
- **source_file** (str, required): Original filename
- **doc_type** (DocType, default: GENERAL): Document type classification

##### 2. Content Classification
- **peripheral** (Peripheral, optional): Primary peripheral discussed
- **secondary_peripherals** (list[str]): Additional peripherals mentioned
- **content_type** (ContentType, default: CONCEPTUAL): Type of content

##### 3. Document Hierarchy
- **section_path** (list[str]): Header hierarchy (e.g., ['GPIO', 'Configuration', 'Initialization'])
- **section_title** (str): Current section title

##### 4. Content Flags
- **has_code** (bool): Contains code examples
- **has_table** (bool): Contains tables
- **has_register_map** (bool): Contains register definitions
- **has_diagram_ref** (bool): References diagrams

##### 5. Position Information
- **chunk_index** (int): Index of chunk in document
- **start_line** (int): Starting line number

##### 6. STM32-Specific Information
- **stm32_families** (list[str]): STM32 families mentioned (e.g., ['STM32F4', 'STM32H7'])
- **hal_functions** (list[str]): HAL/LL function names mentioned
- **registers** (list[str]): Register names mentioned

### Enumerations

#### DocType
Document type classifications:
- `REFERENCE_MANUAL`: Reference manuals (RM)
- `APPLICATION_NOTE`: Application notes (AN)
- `USER_MANUAL`: User manuals (UM)
- `PROGRAMMING_MANUAL`: Programming manuals (PM)
- `DATASHEET`: Datasheets
- `HAL_GUIDE`: HAL/LL driver guides
- `ERRATA`: Errata sheets
- `MIGRATION_GUIDE`: Migration guides
- `SAFETY_MANUAL`: Safety certification documentation
- `GENERAL`: General documentation

#### Peripheral
STM32 peripheral classifications (41 total):

**Communication:** GPIO, UART, USART, SPI, I2C, I3C, CAN, FDCAN, USB, ETH, SPDIF

**Analog:** ADC, DAC

**Timers:** TIM, LPTIM, RTC, WWDG, IWDG

**DMA:** DMA, BDMA, MDMA

**System:** RCC, PWR, NVIC, EXTI, FLASH, CRC, TAMP

**Memory:** FMC, SDMMC, OCTOSPI, QUADSPI

**Graphics:** LTDC, DCMI, DMA2D, JPEG

**Audio:** SAI

**Security:** RNG, CRYP, HASH

**Math:** CORDIC

**System:** MPU, GENERAL

#### ContentType
Content classifications:
- `CONCEPTUAL`: Explanatory content
- `REGISTER_MAP`: Register definitions
- `CODE_EXAMPLE`: Code snippets
- `CONFIGURATION`: Configuration procedures
- `TROUBLESHOOTING`: Debugging/troubleshooting
- `ELECTRICAL_SPEC`: Electrical specifications
- `TIMING_DIAGRAM`: Timing information
- `PIN_DESCRIPTION`: Pin definitions

### Metadata Serialization

The schema provides methods for ChromaDB compatibility:

```python
# Convert to ChromaDB format (flat dict with str, int, float, bool)
chroma_meta = metadata.to_chroma_metadata()

# Reconstruct from ChromaDB
metadata = ChunkMetadataSchema.from_chroma_metadata(chroma_meta)
```

Lists are stored as comma-separated strings in ChromaDB.

## STM32ChromaStore

The main interface for storage operations.

### Initialization

```python
from pathlib import Path
from storage import STM32ChromaStore

store = STM32ChromaStore(
    persist_dir=Path("./data/chroma_db"),
    collection_name="stm32_docs",
    embedding_model="all-MiniLM-L6-v2",
    distance_metric="cosine"
)
```

**Parameters:**
- `persist_dir`: Directory for persistent storage
- `collection_name`: ChromaDB collection name (default: "stm32_docs")
- `embedding_model`: Sentence transformer model (default: "all-MiniLM-L6-v2")
- `distance_metric`: Distance metric (default: "cosine", options: "cosine", "l2", "ip")

### Configuration Details

#### ChromaDB Settings
- **Persistent storage**: Data persists across sessions
- **Telemetry**: Disabled for privacy
- **Distance metric**: Cosine similarity (1 - cosine_distance)

#### Embedding Model
- **Model**: all-MiniLM-L6-v2 (384 dimensions)
- **Loading**: Lazy loaded on first use
- **Performance**: Optimized for semantic similarity

### Core Operations

#### Adding Chunks

```python
from storage import ChunkMetadataSchema, DocType, Peripheral

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

# Add chunks
chunks = [
    ("chunk_001", "GPIO configuration text...", meta.to_chroma_metadata()),
    ("chunk_002", "More GPIO content...", meta.to_chroma_metadata())
]

count = store.add_chunks(chunks)
print(f"Added {count} chunks")
```

#### Basic Search

```python
# Simple search
results = store.search(
    query="How to configure GPIO as output?",
    n_results=5
)

# Results format
for result in results:
    print(f"Score: {result['score']:.3f}")
    print(f"Content: {result['content'][:100]}...")
    print(f"Metadata: {result['metadata']}")
```

#### Filtered Search

```python
# Filter by peripheral
results = store.search(
    query="initialization procedure",
    peripheral=Peripheral.GPIO,
    n_results=5
)

# Filter by document type
results = store.search(
    query="example code",
    doc_type=DocType.HAL_GUIDE,
    n_results=5
)

# Require code examples
results = store.search(
    query="GPIO setup",
    require_code=True,
    n_results=5
)

# Require register information
results = store.search(
    query="GPIO_MODER",
    require_register=True,
    n_results=3
)

# Minimum score threshold
results = store.search(
    query="UART configuration",
    min_score=0.7,  # Only return results with score >= 0.7
    n_results=10
)
```

### Specialized Search Methods

#### Search by Peripheral

Get all documentation for a specific peripheral:

```python
# Get all GPIO documentation
results = store.search_by_peripheral(
    peripheral=Peripheral.GPIO,
    n_results=10
)

# Get GPIO docs matching a query
results = store.search_by_peripheral(
    peripheral=Peripheral.GPIO,
    query="configuration examples",
    n_results=5
)
```

#### Get Code Examples

Find code examples for a topic:

```python
# Get GPIO initialization examples
examples = store.get_code_examples(
    topic="initialization",
    peripheral=Peripheral.GPIO,
    n_results=5
)

# Get general timer examples
examples = store.get_code_examples(
    topic="timer configuration",
    n_results=10
)
```

#### Get Register Information

Find register documentation:

```python
# Search for specific register
results = store.get_register_info(
    register_name="GPIO_MODER",
    n_results=3
)
```

#### Search HAL Functions

Find HAL function documentation:

```python
# Search for HAL function
results = store.search_hal_function(
    function_name="HAL_GPIO_Init",
    n_results=5
)
```

### Direct Access Methods

#### Get by ID

```python
# Get specific chunk
chunk = store.get_by_id("chunk_001")

if chunk:
    print(f"Content: {chunk['content']}")
    print(f"Metadata: {chunk['metadata']}")
```

#### Get Multiple by IDs

```python
# Get multiple chunks
chunks = store.get_by_ids(["chunk_001", "chunk_002", "chunk_003"])

for chunk in chunks:
    print(f"ID: {chunk['id']}")
```

### Management Operations

#### Delete by Source

Remove all chunks from a specific source file:

```python
deleted_count = store.delete_by_source("stm32f4_reference.md")
print(f"Deleted {deleted_count} chunks")
```

#### Get Statistics

```python
stats = store.get_stats()
print(f"Total chunks: {stats['total_chunks']}")
print(f"Collection: {stats['collection_name']}")
print(f"Embedding model: {stats['embedding_model']}")
```

#### Get Distributions

```python
# Peripheral distribution
peripheral_dist = store.get_peripheral_distribution()
for peripheral, count in peripheral_dist.items():
    print(f"{peripheral}: {count} chunks")

# Document type distribution
doc_dist = store.get_doc_type_distribution()
for doc_type, count in doc_dist.items():
    print(f"{doc_type}: {count} chunks")
```

#### List Sources

```python
sources = store.list_sources()
print("Available source files:")
for source in sources:
    print(f"  - {source}")
```

#### Count Chunks

```python
total = store.count()
print(f"Total chunks: {total}")
```

#### Clear Collection

**WARNING**: Deletes all data!

```python
store.clear()  # Use with caution!
```

## Search Result Format

All search methods return results in this format:

```python
{
    'id': 'chunk_001',
    'content': 'The GPIO peripheral allows...',
    'metadata': {
        'source_file': 'stm32f4_reference.md',
        'doc_type': 'reference_manual',
        'peripheral': 'GPIO',
        'has_code': True,
        # ... other metadata fields
    },
    'score': 0.87  # Similarity score (0.0-1.0)
}
```

### Score Interpretation

- **0.9-1.0**: Excellent match
- **0.8-0.9**: Good match
- **0.7-0.8**: Moderate match
- **< 0.7**: Weak match

The score is calculated as `1.0 - cosine_distance`, where higher scores indicate better semantic similarity.

## Filter Combinations

You can combine multiple filters:

```python
# Complex query: GPIO code examples from HAL guides
results = store.search(
    query="initialization example",
    peripheral=Peripheral.GPIO,
    doc_type=DocType.HAL_GUIDE,
    require_code=True,
    min_score=0.75,
    n_results=5
)
```

## Performance Considerations

### Embedding Generation
- **First call**: Model loads from disk (~100-200ms)
- **Subsequent calls**: Fast embedding generation
- **Batch processing**: Automatically batches for efficiency

### Search Performance
- **Small collections** (< 10K chunks): Sub-second queries
- **Medium collections** (10K-100K chunks): 1-2 second queries
- **Large collections** (> 100K chunks): Consider indexing tuning

### Storage Requirements
- **Per chunk**: ~1KB metadata + ~1.5KB embedding
- **10,000 chunks**: ~25MB disk space

## Best Practices

### 1. Metadata Quality
- Always set peripheral and doc_type when known
- Use section_path for better context
- Mark has_code and has_register_map accurately

### 2. Search Strategy
- Start with broad queries, then filter
- Use peripheral filters for targeted searches
- Combine min_score with n_results for quality control

### 3. Data Management
- Regularly check distributions for balance
- Clean up outdated sources before re-ingesting
- Use meaningful chunk IDs (e.g., `{source}_{index}`)

### 4. Error Handling
```python
try:
    results = store.search("query")
except Exception as e:
    logger.error(f"Search failed: {e}")
    # Handle error
```

## Example Workflows

### Workflow 1: Ingestion Pipeline

```python
from pathlib import Path
from storage import STM32ChromaStore, ChunkMetadataSchema

# Initialize store
store = STM32ChromaStore(Path("./data/chroma_db"))

# Process documents
for doc_path in Path("./docs").glob("*.md"):
    # Parse document (from pipeline)
    chunks = parse_document(doc_path)

    # Add to store
    store_chunks = []
    for i, chunk in enumerate(chunks):
        meta = ChunkMetadataSchema(
            source_file=doc_path.name,
            chunk_index=i,
            # ... other metadata
        )
        chunk_id = f"{doc_path.stem}_{i:04d}"
        store_chunks.append((chunk_id, chunk.content, meta.to_chroma_metadata()))

    count = store.add_chunks(store_chunks)
    print(f"Added {count} chunks from {doc_path.name}")
```

### Workflow 2: MCP Query Handler

```python
async def handle_query(query: str, peripheral: Optional[str] = None):
    # Parse peripheral
    periph = Peripheral(peripheral) if peripheral else None

    # Search
    results = store.search(
        query=query,
        peripheral=periph,
        n_results=5,
        min_score=0.7
    )

    # Format response
    if results:
        return format_results(results)
    else:
        return "No relevant documentation found."
```

### Workflow 3: Code Example Retrieval

```python
def get_peripheral_examples(peripheral_name: str, topic: str):
    peripheral = Peripheral(peripheral_name)

    # Get code examples
    examples = store.get_code_examples(
        topic=topic,
        peripheral=peripheral,
        n_results=3
    )

    # Extract code blocks from results
    code_blocks = []
    for result in examples:
        # Parse markdown code blocks from content
        blocks = extract_code_blocks(result['content'])
        code_blocks.extend(blocks)

    return code_blocks
```

## Integration with Pipeline

The storage layer integrates with the chunking pipeline:

```python
from pipeline import DocumentChunker
from storage import STM32ChromaStore

# Initialize
chunker = DocumentChunker()
store = STM32ChromaStore(Path("./data/chroma_db"))

# Process document
chunks = chunker.chunk_document("stm32f4_reference.md")

# Store chunks
for chunk in chunks:
    store.add_chunks([(
        chunk.id,
        chunk.content,
        chunk.metadata.to_chroma_metadata()
    )])
```

## Troubleshooting

### Issue: Slow first query
**Solution**: The embedding model loads on first use. This is normal.

### Issue: Low relevance scores
**Solution**:
- Check if documents are properly chunked
- Verify metadata is set correctly
- Consider adjusting min_score threshold

### Issue: ChromaDB errors
**Solution**:
- Check persist_dir permissions
- Ensure sufficient disk space
- Verify ChromaDB version compatibility

### Issue: Memory usage high
**Solution**:
- ChromaDB keeps some data in memory
- Use batch processing for large ingestion
- Consider collection size limits

## API Reference Summary

### STM32ChromaStore Methods

| Method | Purpose | Returns |
|--------|---------|---------|
| `add_chunks()` | Add chunks to store | int (count added) |
| `search()` | Semantic search with filters | list[dict] |
| `search_by_peripheral()` | Get peripheral docs | list[dict] |
| `get_code_examples()` | Find code examples | list[dict] |
| `get_register_info()` | Get register docs | list[dict] |
| `search_hal_function()` | Find HAL function docs | list[dict] |
| `get_by_id()` | Get specific chunk | Optional[dict] |
| `get_by_ids()` | Get multiple chunks | list[dict] |
| `delete_by_source()` | Delete source file chunks | int (count deleted) |
| `get_stats()` | Collection statistics | dict |
| `get_peripheral_distribution()` | Chunks per peripheral | dict[str, int] |
| `get_doc_type_distribution()` | Chunks per doc type | dict[str, int] |
| `list_sources()` | List source files | list[str] |
| `count()` | Total chunk count | int |
| `clear()` | Delete all data | None |

## Future Enhancements

Potential improvements for the storage layer:

1. **Hybrid Search**: Combine semantic and keyword search
2. **Reranking**: Secondary ranking stage for better precision
3. **Caching**: Cache frequent queries
4. **Batch Operations**: Optimize bulk operations
5. **Compression**: Reduce storage footprint
6. **Sharding**: Support very large collections
7. **Incremental Updates**: Efficient document updates
8. **Query Analytics**: Track search patterns

---

For implementation examples, see `/storage/chroma_store.py`.
For schema definitions, see `/storage/metadata.py`.
