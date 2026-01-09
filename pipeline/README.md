# STM32 Document Chunking Pipeline

Intelligent chunking system for STM32 technical documentation that preserves structure, extracts metadata, and optimizes for RAG retrieval.

## Quick Start

### Installation

```bash
# Create virtual environment (if not already done)
python3 -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate

# Install dependencies
pip install tiktoken
```

### Basic Usage

```python
from pipeline.chunker import STM32Chunker, ChunkingConfig
from pipeline.validator import ChunkValidator

# Load your markdown document
with open('docs/stm32h7_gpio.md', 'r') as f:
    content = f.read()

# Create chunker
chunker = STM32Chunker(ChunkingConfig(
    chunk_size=1000,
    chunk_overlap=150
))

# Chunk the document
chunks = chunker.chunk_document(content, 'stm32h7_gpio.md')

# Validate chunks
validator = ChunkValidator()
report = validator.generate_report(chunks)
validator.print_report(report, verbose=True)

# Process chunks
for chunk in chunks:
    print(f"Chunk {chunk.id}: {chunk.token_count} tokens")
    print(f"  Section: {' > '.join(chunk.metadata.section_path)}")
    print(f"  Peripheral: {chunk.metadata.peripheral}")
    print(f"  Has code: {chunk.metadata.has_code}")
```

## Running Tests

```bash
# Run comprehensive test suite
python pipeline/test_chunking_pipeline.py

# Test individual components
python pipeline/chunker.py
python pipeline/validator.py
```

## Features

### Smart Structure Preservation

- **Headers**: Maintains markdown header hierarchy
- **Code Blocks**: Never splits code mid-block
- **Tables**: Keeps register tables intact
- **Lists**: Preserves list structures

### Token-Aware Chunking

- Uses `tiktoken` (cl100k_base) for accurate token counting
- Target: 800-1200 tokens per chunk
- Overlap: 100-150 tokens for context continuity
- Handles oversized content gracefully

### Rich Metadata Extraction

Each chunk includes:

- **Document Type**: reference_manual, datasheet, app_note, etc.
- **Peripheral**: GPIO, UART, SPI, I2C, DMA, etc. (40+ supported)
- **Section Path**: Hierarchical header trail
- **STM32 Families**: Detected family references (STM32F4, STM32H7, etc.)
- **HAL Functions**: Extracted HAL function names
- **Registers**: Detected register names
- **Content Flags**: has_code, has_table, has_register

### Quality Validation

Validates:
- Token count bounds
- Code block integrity
- Table completeness
- Content quality
- Metadata consistency

## Configuration

### ChunkingConfig Options

```python
config = ChunkingConfig(
    chunk_size=1000,              # Target tokens per chunk
    chunk_overlap=150,            # Overlap for context
    min_chunk_size=50,            # Minimum viable chunk
    max_chunk_size=2000,          # Maximum before forced split
    preserve_code_blocks=True,    # Never split code
    preserve_tables=True          # Keep tables intact
)
```

### Tuning for Different Document Types

**Code-Heavy Documentation:**
```python
config = ChunkingConfig(
    chunk_size=1200,
    max_chunk_size=2500,
    chunk_overlap=100
)
```

**Register Reference Manuals:**
```python
config = ChunkingConfig(
    chunk_size=800,
    chunk_overlap=200,
    preserve_tables=True
)
```

**Quick Retrieval (Smaller Chunks):**
```python
config = ChunkingConfig(
    chunk_size=600,
    chunk_overlap=100,
    min_chunk_size=100
)
```

## Architecture

```
┌─────────────────┐
│  Markdown Doc   │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│  Header Split   │  Split by H1-H6 headers
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│  Protect        │  Extract code blocks & tables
│  Regions        │  (never split these)
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│  Token-Aware    │  Split by tokens with overlap
│  Split          │  Respect protected regions
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│  Metadata       │  Extract peripherals, families,
│  Extraction     │  HAL functions, registers
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│  Validation     │  Check quality & integrity
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│  Chunks Ready   │  Ready for vector store
└─────────────────┘
```

## Examples

See comprehensive examples in `test_chunking_pipeline.py`:

1. Basic chunking
2. Code block preservation
3. Table preservation
4. Metadata extraction
5. Validation
6. Overlap handling
7. Peripheral detection

## Documentation

For detailed information, see [docs/CHUNKING.md](../docs/CHUNKING.md):

- Chunking strategy
- Configuration guide
- Peripheral detection
- Document type classification
- Troubleshooting
- Best practices

## API Reference

### STM32Chunker

```python
class STM32Chunker:
    def __init__(self, config: ChunkingConfig = None)
    def chunk_document(self, content: str, source_file: str) -> list[Chunk]
```

### ChunkValidator

```python
class ChunkValidator:
    def __init__(self, min_tokens: int = 50, max_tokens: int = 2000)
    def validate_chunk(self, chunk: Chunk) -> ValidationResult
    def generate_report(self, chunks: list[Chunk]) -> ValidationReport
    def print_report(self, report: ValidationReport, verbose: bool = False)
```

### Data Classes

```python
@dataclass
class Chunk:
    id: str
    content: str
    token_count: int
    metadata: ChunkMetadata

@dataclass
class ChunkMetadata:
    source_file: str
    doc_type: str
    section_path: list[str]
    peripheral: Optional[str]
    has_code: bool
    has_table: bool
    has_register: bool
    start_line: int
    chunk_index: int
    stm32_families: list[str]
    hal_functions: list[str]
    registers: list[str]
```

## Performance

Typical performance on modern hardware:

- **Single document**: <1 second (typical reference manual)
- **100 documents**: ~10-30 seconds
- **Memory**: ~10MB per 1000 chunks
- **Token counting**: Cached by tiktoken (very fast)

For large-scale processing, use parallel processing:

```python
from multiprocessing import Pool

def process_document(file_path):
    with open(file_path) as f:
        content = f.read()
    chunker = STM32Chunker()
    return chunker.chunk_document(content, file_path)

with Pool(8) as pool:
    all_chunks = pool.map(process_document, file_paths)
```

## Supported Peripherals

40+ STM32 peripherals detected:

- **Communication**: UART, USART, LPUART, SPI, I2C, I3C, CAN, FDCAN, USB, ETH
- **Timers**: TIM, LPTIM, RTC, IWDG, WWDG
- **Analog**: ADC, DAC, TSC, VREFBUF
- **Digital I/O**: GPIO, EXTI
- **Memory**: DMA, BDMA, MDMA, FMC, FLASH, SDMMC, MMC, QUADSPI, OCTOSPI
- **Security**: RNG, CRYP, HASH, AES, PKA
- **System**: RCC, PWR, NVIC
- **Multimedia**: LTDC, DCMI, JPEG, SAI, DFSDM
- **Math**: CORDIC, FMAC, CRC
- **Power**: UCPD

## Troubleshooting

### Issue: Chunks too small

Many chunks under 100 tokens.

**Solution:**
- Increase `min_chunk_size`
- Check document structure (too many headers)
- Consider flattening header hierarchy

### Issue: Code blocks split

Validation errors about unmatched fence markers.

**Solution:**
- Ensure `preserve_code_blocks=True`
- Check source markdown for malformed code blocks
- Verify closing ``` exists for all code blocks

### Issue: Poor peripheral detection

Peripheral is None for obvious peripheral content.

**Solution:**
- Include peripheral name in filename
- Ensure peripheral mentioned 3+ times in content
- Check if peripheral is in `PERIPHERALS` list

## Contributing

When adding features:

1. Add tests to `test_chunking_pipeline.py`
2. Update documentation in `docs/CHUNKING.md`
3. Ensure all tests pass
4. Update this README

## License

Part of the STM32 MCP Documentation Server project.

---

**Version**: 1.0
**Last Updated**: 2026-01-08
