# STM32 Document Chunking Pipeline

This document describes the chunking strategy used for processing STM32 technical documentation into semantically meaningful chunks optimized for RAG (Retrieval-Augmented Generation) systems.

## Overview

The chunking pipeline transforms markdown documentation into token-aware chunks that:
- Preserve document structure (headers, code, tables)
- Maintain semantic coherence
- Include rich metadata for filtering
- Optimize for vector similarity search

## Architecture

```
┌─────────────────┐
│  Markdown Doc   │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│  STM32Chunker   │  ← Split by headers, preserve structure
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│  Token Aware    │  ← Apply size limits with overlap
│    Splitting    │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│  Metadata       │  ← Extract peripherals, registers, HAL functions
│  Extraction     │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│ ChunkValidator  │  ← Validate quality before ingestion
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│  Vector Store   │
└─────────────────┘
```

## Chunking Strategy

### 1. Header-Based Splitting

The chunker first splits documents by markdown headers (H1-H6), preserving the hierarchical structure:

```markdown
# GPIO Configuration          ← Creates section with path: ["GPIO Configuration"]
## Overview                   ← Creates section with path: ["GPIO Configuration", "Overview"]
### Mode Register             ← Creates section with path: [..., "Mode Register"]
```

**Benefits:**
- Maintains semantic boundaries
- Preserves context hierarchy
- Enables precise section-based retrieval

### 2. Protected Content Regions

Certain content types are **never split** in the middle:

#### Code Blocks
```c
// This entire block stays together
GPIO_InitTypeDef gpio = {0};
gpio.Pin = GPIO_PIN_5;
gpio.Mode = GPIO_MODE_OUTPUT_PP;
HAL_GPIO_Init(GPIOA, &gpio);
```

#### Tables
| Register | Offset | Description     |
|----------|--------|-----------------|
| MODER    | 0x00   | Mode register   |
| OTYPER   | 0x04   | Output type     |

Tables are kept atomic to preserve register definitions and bit field mappings.

### 3. Token-Aware Splitting

Uses `tiktoken` (cl100k_base encoding) for accurate token counting:

- **Target size**: 800-1200 tokens
- **Min size**: 50 tokens (prevents tiny fragments)
- **Max size**: 2000 tokens (hard limit)

#### Overlap Strategy

Chunks include 100-150 tokens of overlap from the previous chunk to maintain context:

```
Chunk 1: [........................................] (150 overlap) →
Chunk 2:                      (← 150 overlap) [......................................]
```

This ensures queries that match boundary content can retrieve relevant context.

### 4. Oversized Content Handling

When content exceeds max tokens:

1. **Try splitting at paragraph boundaries** while respecting protected regions
2. **If code/table causes overflow**: Make it its own chunk (even if oversized)
3. **Flag oversized chunks**: Validator warns but allows if justified

## Metadata Extraction

Each chunk includes rich metadata for filtering and ranking:

### Document Classification

```python
doc_type: str  # reference_manual, datasheet, app_note, user_guide, etc.
```

**Detection logic:**
1. Check filename patterns (`_rm.md`, `_ds.md`, `AN1234`)
2. Check document content (first 1000 chars)
3. Match against known ST documentation patterns

### Peripheral Detection

```python
peripheral: Optional[str]  # GPIO, UART, SPI, etc.
```

**Supported peripherals:**
- Communication: UART, USART, LPUART, SPI, I2C, I3C, CAN, FDCAN, USB, ETH
- Timers: TIM, LPTIM, RTC, IWDG, WWDG
- Analog: ADC, DAC
- Digital I/O: GPIO, EXTI
- Memory: DMA, BDMA, MDMA, FMC, FLASH, SDMMC
- Security: RNG, CRYP, HASH, AES, PKA
- System: RCC, PWR, NVIC
- Multimedia: LTDC, DCMI, JPEG, SAI, DFSDM

**Detection logic:**
1. **Filename first**: Check for peripheral name in filename (most reliable)
2. **Content analysis**: Count peripheral mentions in text
3. **Threshold**: Require 3+ mentions for confidence

### Section Path

```python
section_path: list[str]  # ["GPIO", "Configuration", "Mode Register"]
```

Tracks the header hierarchy leading to this chunk, enabling:
- "Show me all chunks about GPIO Configuration"
- "Find content under UART > Interrupts"

### STM32 Family Detection

```python
stm32_families: list[str]  # ["STM32F4", "STM32H7"]
```

Extracts family references from content using patterns:
- `STM32[FHLGUWC][0-9]` - Main families (F4, H7, L4, G4, U5, WB, WL, C0)
- `STM32MP[0-9]` - MPU series
- `STM32WB[0-9]` - Wireless
- `STM32WL[0-9]` - LoRa

### HAL Function Extraction

```python
hal_functions: list[str]  # ["HAL_GPIO_Init", "HAL_GPIO_WritePin"]
```

Extracts all HAL function references using pattern: `HAL_[A-Z][A-Za-z0-9_]*\(`

**Use cases:**
- "Find examples using HAL_UART_Transmit"
- "Show initialization code with HAL_ADC_Init"

### Register Detection

```python
registers: list[str]  # ["MODER", "OTYPER", "CR1", "SR"]
has_register: bool
```

Extracts register names and detects register definitions:

**Register patterns:**
- Common suffixes: `CR`, `SR`, `DR`, `MR`, `TR`, `BR`, `PR`, `AR`, `ER`
- Specific registers: `ISR`, `ICR`, `IER`, `IDR`, `ODR`, `BSRR`, `LCKR`
- Numbered variants: `CR1`, `CR2`, `ARR`, `PSC`

**Bit field detection:**
- "Bit 0: ENABLE"
- "[31:16] RESERVED"
- "Bits 7-0: MODE"

### Content Type Flags

```python
has_code: bool      # Contains code blocks
has_table: bool     # Contains markdown tables
has_register: bool  # Contains register definitions
```

Enables filtering:
- "Find code examples for UART"
- "Show register tables for GPIO"

## Configuration Options

### ChunkingConfig

```python
@dataclass
class ChunkingConfig:
    chunk_size: int = 1000              # Target tokens per chunk
    chunk_overlap: int = 150            # Overlap tokens for context
    min_chunk_size: int = 50            # Minimum viable chunk
    max_chunk_size: int = 2000          # Maximum before forced split
    preserve_code_blocks: bool = True   # Never split code mid-block
    preserve_tables: bool = True        # Keep tables intact
```

### Tuning Guidelines

#### For Code-Heavy Docs
```python
config = ChunkingConfig(
    chunk_size=1200,      # Allow more room for code
    max_chunk_size=2500,  # Accommodate large examples
)
```

#### For Register Reference Manuals
```python
config = ChunkingConfig(
    chunk_size=800,       # Smaller chunks for dense content
    chunk_overlap=200,    # More overlap for register context
)
```

#### For Quick Retrieval
```python
config = ChunkingConfig(
    chunk_size=600,       # Smaller chunks
    chunk_overlap=100,    # Less overlap
    min_chunk_size=100,   # Avoid tiny fragments
)
```

## Validation

The `ChunkValidator` ensures quality before ingestion:

### Validation Checks

1. **Token Bounds**
   - Error if < min_tokens or > max_tokens (without justification)
   - Warning if < 100 tokens or oversized with code/tables

2. **Code Integrity**
   - Count fence markers (must be even)
   - Check for truncated blocks
   - Verify metadata flags match content

3. **Table Integrity**
   - Verify header separator row exists
   - Check column consistency
   - Detect truncated tables

4. **Content Quality**
   - Not just whitespace
   - Minimum 20 letters of actual text
   - Reasonable char-to-token ratio (2-8)
   - Check for repeated lines (chunking errors)

5. **Metadata Completeness**
   - Required fields present
   - Flags match actual content

### Validation Report

```python
report = validator.generate_report(chunks)
# ValidationReport(
#     total_chunks=150,
#     valid_chunks=148,
#     invalid_chunks=2,
#     warnings_count=12,
#     issues=[...]
# )
```

## Usage Examples

### Basic Chunking

```python
from pipeline.chunker import STM32Chunker, ChunkingConfig

# Load markdown content
with open('docs/stm32h7_gpio.md', 'r') as f:
    content = f.read()

# Create chunker with default config
chunker = STM32Chunker()

# Chunk the document
chunks = chunker.chunk_document(content, 'stm32h7_gpio.md')

print(f"Generated {len(chunks)} chunks")
for chunk in chunks:
    print(f"  {chunk.id}: {chunk.token_count} tokens")
    print(f"    Section: {' > '.join(chunk.metadata.section_path)}")
```

### Custom Configuration

```python
# Configure for code-heavy documentation
config = ChunkingConfig(
    chunk_size=1200,
    chunk_overlap=150,
    max_chunk_size=2500,
    preserve_code_blocks=True,
    preserve_tables=True
)

chunker = STM32Chunker(config)
chunks = chunker.chunk_document(content, source_file)
```

### Validation

```python
from pipeline.validator import ChunkValidator

# Validate chunks
validator = ChunkValidator(min_tokens=50, max_tokens=2000)
report = validator.generate_report(chunks)

# Print report
validator.print_report(report, verbose=True)

# Check for errors
if report.invalid_chunks > 0:
    print(f"⚠️  {report.invalid_chunks} invalid chunks!")
    for issue in report.issues:
        if issue['errors']:
            print(f"  Chunk {issue['chunk_id']}: {issue['errors']}")
```

### Filtering by Metadata

```python
# Find GPIO-related chunks
gpio_chunks = [c for c in chunks if c.metadata.peripheral == 'GPIO']

# Find chunks with code examples
code_chunks = [c for c in chunks if c.metadata.has_code]

# Find register reference chunks
register_chunks = [c for c in chunks if c.metadata.has_register]

# Find STM32H7-specific content
h7_chunks = [c for c in chunks if 'STM32H7' in c.metadata.stm32_families]

# Find HAL_UART_Transmit examples
uart_tx_chunks = [
    c for c in chunks
    if 'HAL_UART_Transmit' in c.metadata.hal_functions
]
```

## Performance Considerations

### Typical Performance

- **Speed**: ~50-100 documents per second (typical reference manual)
- **Memory**: ~10MB per 1000 chunks
- **Token counting**: Cached by tiktoken, very fast

### Optimization Tips

1. **Batch processing**: Process multiple documents in parallel
2. **Streaming**: For very large documents, consider streaming line-by-line
3. **Caching**: Cache peripheral detection results for similar sections
4. **Precompile regexes**: Reuse compiled patterns across documents

### Scalability

The chunker is designed for:
- **Single document**: <1 second for typical reference manual
- **100 documents**: ~10-30 seconds
- **1000+ documents**: Use parallel processing (multiprocessing pool)

## Integration with Vector Store

Chunks are designed for ChromaDB ingestion:

```python
from storage.vector_store import VectorStore

# Initialize vector store
vector_store = VectorStore()

# Add chunks
for chunk in chunks:
    vector_store.add_document(
        id=chunk.id,
        content=chunk.content,
        metadata={
            'source_file': chunk.metadata.source_file,
            'doc_type': chunk.metadata.doc_type,
            'peripheral': chunk.metadata.peripheral,
            'section_path': ' > '.join(chunk.metadata.section_path),
            'has_code': chunk.metadata.has_code,
            'has_table': chunk.metadata.has_table,
            'stm32_families': ','.join(chunk.metadata.stm32_families),
            'hal_functions': ','.join(chunk.metadata.hal_functions),
            'registers': ','.join(chunk.metadata.registers),
        }
    )
```

## Best Practices

### 1. Validate After Chunking

Always run validation before ingestion:

```python
chunks = chunker.chunk_document(content, source)
report = validator.generate_report(chunks)

if report.invalid_chunks > 0:
    print("⚠️  Fix invalid chunks before ingestion")
    # Handle errors...
```

### 2. Monitor Chunk Size Distribution

Check that most chunks are within target range:

```python
sizes = [c.token_count for c in chunks]
print(f"Min: {min(sizes)}, Max: {max(sizes)}, Avg: {sum(sizes)/len(sizes):.0f}")

# Visualize distribution
import collections
buckets = collections.Counter(s // 200 * 200 for s in sizes)
for bucket, count in sorted(buckets.items()):
    print(f"{bucket:4d}-{bucket+200:4d}: {'█' * count}")
```

### 3. Preserve Context

Use adequate overlap for technical documentation:

```python
# Good overlap for register docs (context-heavy)
config = ChunkingConfig(chunk_overlap=200)

# Less overlap for independent sections
config = ChunkingConfig(chunk_overlap=100)
```

### 4. Test with Real Documentation

Use actual STM32 documents for testing:

```python
# Test with reference manual (complex, large)
chunks = chunker.chunk_document(ref_manual_content, 'rm0433.md')

# Test with app note (code-heavy)
chunks = chunker.chunk_document(app_note_content, 'an4891.md')

# Test with datasheet (tables-heavy)
chunks = chunker.chunk_document(datasheet_content, 'ds12345.md')
```

## Troubleshooting

### Issue: Chunks Too Small

**Symptom**: Many chunks under 100 tokens

**Solutions:**
- Increase `min_chunk_size`
- Check if document has excessive headers (flatten structure)
- Reduce header-based splitting levels

### Issue: Chunks Too Large

**Symptom**: Many chunks over max_tokens

**Solutions:**
- Decrease `chunk_size` target
- Check for very large code blocks or tables (may need manual splitting)
- Adjust `max_chunk_size` if oversized content is justified

### Issue: Code Blocks Split

**Symptom**: Validation errors about unmatched fence markers

**Solutions:**
- Ensure `preserve_code_blocks=True`
- Check for malformed markdown (missing closing ```)
- Manually fix source documents if needed

### Issue: Poor Peripheral Detection

**Symptom**: `peripheral` is None for obvious peripheral content

**Solutions:**
- Check peripheral name in filename
- Verify peripheral appears 3+ times in content
- Add peripheral to `PERIPHERALS` list if missing
- Lower detection threshold for short documents

## Future Enhancements

Potential improvements for v2:

1. **Semantic Splitting**: Use embeddings to detect topic shifts
2. **Cross-Reference Handling**: Link related chunks (e.g., "See Section 5.2")
3. **Image Extraction**: Handle diagrams and figures
4. **Multi-Language**: Support non-English documentation
5. **Adaptive Sizing**: Adjust chunk size based on content density
6. **Version Tracking**: Track changes across document versions

## References

- [tiktoken Documentation](https://github.com/openai/tiktoken)
- [ChromaDB Guide](https://docs.trychroma.com/)
- [STM32 Documentation Catalog](https://www.st.com/content/st_com/en/support/resources/resource-selector.html)

---

**Last Updated**: 2026-01-08
**Version**: 1.0
**Maintainer**: STM32 Agents Team
