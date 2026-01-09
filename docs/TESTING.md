# Testing Guide

Comprehensive guide to testing the STM32 MCP Documentation Server.

## Overview

The testing suite validates:
- System configuration and setup
- Document ingestion pipeline
- Search quality and relevance
- MCP server functionality
- Integration with Claude Code
- Performance and reliability

## Test Categories

### 1. System Validation
### 2. Search Quality Tests
### 3. Unit Tests
### 4. Integration Tests
### 5. Performance Tests
### 6. Manual Testing

## System Validation

### verify_mcp.py

Complete system health check that validates all components.

**Location**: `scripts/verify_mcp.py`

**Usage**:
```bash
python scripts/verify_mcp.py
```

**What It Checks**:

#### 1. Project Structure
- Required directories exist (mcp_server/, pipeline/, storage/, scripts/, data/)
- Configuration files present (.claude/mcp.json, pyproject.toml)
- Source documentation available (markdowns/)

#### 2. Module Imports
- All Python modules can be imported
- No missing dependencies
- Version compatibility

Modules tested:
- `mcp_server.server`
- `mcp_server.config`
- `storage.chroma_store`
- `storage.metadata`
- `pipeline.chunker`
- `pipeline.validator`

#### 3. Configuration
- Settings load correctly
- Paths are valid
- Environment variables work
- Default values appropriate

Validated settings:
- Server name and mode
- Database paths
- Embedding model
- Chunk size and overlap

#### 4. Database
- ChromaDB collection exists
- Chunks are indexed
- Metadata is complete
- Peripheral distribution

Checks:
- Collection name: `stm32_docs`
- Chunk count: >2000
- Peripherals: ~15 types
- Sample chunk retrieval

#### 5. Search Functionality
- Query embedding works
- Vector search returns results
- Relevance scoring functional
- Metadata filtering works

Test query: "GPIO configuration"
Expected: 5+ results with scores >0.6

**Expected Output**:

```
STM32 MCP System Verification
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

✅ Project Structure: PASS
   - Directories: mcp_server, pipeline, storage, scripts, data ✓
   - Config files: .claude/mcp.json, pyproject.toml ✓
   - Documentation: markdowns/ (80 files) ✓

✅ Module Imports: PASS
   - mcp_server.server ✓
   - storage.chroma_store ✓
   - pipeline.chunker ✓
   All modules load successfully

✅ Configuration: PASS
   - Server name: stm32-docs
   - Server mode: local
   - Database: data/chroma_db/
   - Collection: stm32_docs
   - Embedding model: all-MiniLM-L6-v2
   - Chunk size: 1000, overlap: 150

✅ Database: PASS
   - Collection exists: stm32_docs
   - Chunks indexed: 2,847
   - Peripherals: 15 (GPIO, UART, SPI, I2C, TIM, ADC, DMA, ...)
   - Sample chunk retrieved successfully

✅ Search: PASS
   - Query: "GPIO configuration"
   - Results: 5
   - Top relevance: 0.874
   - Source: an4899-gpio-hardware-settings.md
   - Content preview: ## GPIO Configuration...

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
✅ All checks passed!

System is ready for use.
```

**Failure Examples**:

```
❌ Database: FAIL
   - Collection exists: stm32_docs
   - Chunks indexed: 0
   ERROR: No chunks found. Run: python scripts/ingest_docs.py --clear

❌ Module Imports: FAIL
   - mcp_server.server ✗ (ModuleNotFoundError: tiktoken)
   ERROR: Missing dependencies. Run: pip install -e .
```

## Search Quality Tests

### test_retrieval.py

Validates search quality with curated test queries.

**Location**: `scripts/test_retrieval.py`

**Usage**:
```bash
python scripts/test_retrieval.py
```

**Test Queries**:

The script runs 12 curated queries covering major peripherals:

1. **GPIO**: "GPIO output mode configuration"
2. **UART**: "UART DMA configuration"
3. **SPI**: "SPI master mode setup"
4. **I2C**: "I2C clock stretching"
5. **TIM**: "Timer PWM output"
6. **ADC**: "ADC continuous conversion"
7. **DMA**: "DMA circular mode"
8. **RCC**: "Clock configuration"
9. **NVIC**: "Interrupt priority"
10. **Power**: "Low power mode"
11. **HAL**: "HAL initialization"
12. **Registers**: "Register configuration"

**What It Tests**:

- **Relevance**: Top results have scores >0.7
- **Peripheral Filter**: Results match requested peripheral
- **Content Quality**: Previews show relevant content
- **Ranking**: Best result is ranked first
- **Coverage**: All major peripherals have documentation

**Expected Output**:

```
STM32 Search Quality Test
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Test 1/12: GPIO Output Configuration
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Query: "GPIO output mode configuration"
Filter: peripheral=GPIO
Results: 3

[1] Score: 0.874 ⭐
    Source: an4899-gpio-hardware-settings.md
    Peripheral: GPIO
    Type: application_note
    Content: ## GPIO Configuration

             The GPIO_MODER register controls the pin mode.
             For output mode, set MODER[1:0] = 01...

[2] Score: 0.841 ⭐
    Source: rm0468-stm32h7-reference.md
    Peripheral: GPIO
    Type: reference_manual
    Content: ### Output Configuration

             For push-pull output, configure GPIO_OTYPER...

[3] Score: 0.798 ⭐
    Source: an4013-gpio-basics.md
    Peripheral: GPIO
    Type: application_note
    Content: GPIO pins can be configured in four modes:
             input, output, alternate function, analog...

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Test 2/12: UART DMA Configuration
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Query: "UART DMA configuration"
Filter: peripheral=UART
Results: 3

[1] Score: 0.892 ⭐
    Source: an4655-uart-applications.md
    ...

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Summary
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Tests: 12
Passed: 12 ✓
Failed: 0

Average top score: 0.856
Minimum top score: 0.743
Maximum top score: 0.912

All queries returned relevant results!
```

**Quality Criteria**:

- ✅ **Good**: Top score >0.8, relevant peripheral, accurate content
- ⚠️ **Acceptable**: Top score 0.6-0.8, mostly relevant
- ❌ **Poor**: Top score <0.6, wrong peripheral, irrelevant content

## Unit Tests

### Test Suite

**Location**: `tests/`

**Running Tests**:

```bash
# Run all tests
python scripts/run_tests.py

# Or use pytest directly
pytest tests/

# Run with coverage
python scripts/run_tests.py --coverage

# Run specific test file
pytest tests/test_chunking.py

# Run only unit tests (skip integration)
python scripts/run_tests.py --unit

# Run only integration tests
python scripts/run_tests.py --integration

# Run verbose
pytest tests/ -v

# Run with output
pytest tests/ -s
```

### Test Files

#### tests/test_chunking.py

Comprehensive tests for document chunking functionality.

**Test Classes**:
- `TestChunking` - Core chunking functionality
- `TestChunkingConfig` - Configuration options
- `TestCodeBlockHandling` - Code block specific tests
- `TestTableHandling` - Table specific tests

**Tests Include**:
- Basic markdown chunking
- Code blocks not being split (matching fence markers)
- Peripheral detection from content
- Metadata extraction (source file, code, tables)
- Section hierarchy tracking
- Token count bounds
- Empty content handling
- Nested headers
- HAL function extraction
- STM32 family detection
- Document type detection
- Chunk ID determinism
- Large document handling

**Sample Test**:
```python
def test_code_blocks_not_split(self, chunker):
    """Code blocks should never be split."""
    content = '''
# Example

```c
void very_long_function(void) {
    int a = 1;
    for (int i = 0; i < 100; i++) {
        do_something(i);
    }
}
```
'''
    chunks = chunker.chunk_document(content, "test.md")
    for chunk in chunks:
        if "```" in chunk.content:
            count = chunk.content.count("```")
            assert count % 2 == 0, "Code block was split"
```

#### tests/test_storage.py

Tests ChromaDB storage layer and metadata schemas.

**Test Classes**:
- `TestMetadataSchema` - Schema creation and conversion
- `TestSTM32ChromaStore` - Store operations

**Tests Include**:
- Schema creation and validation
- ChromaDB metadata conversion (to/from)
- Roundtrip conversion (lossless)
- Store initialization
- Adding chunks
- Basic search
- Filtered search (peripheral, code, doc type)
- Get by ID (single and multiple)
- Delete by source
- Peripheral distribution
- Document type distribution
- List sources
- Code examples retrieval
- Register info retrieval
- HAL function search

**Sample Test**:
```python
def test_roundtrip_conversion(self):
    """Test that to/from ChromaDB conversion is lossless."""
    original = ChunkMetadataSchema(
        source_file="roundtrip.md",
        doc_type=DocType.APPLICATION_NOTE,
        peripheral=Peripheral.I2C,
        has_code=True,
    )
    chroma_meta = original.to_chroma_metadata()
    reconstructed = ChunkMetadataSchema.from_chroma_metadata(chroma_meta)
    assert reconstructed.source_file == original.source_file
    assert reconstructed.doc_type == original.doc_type
```

#### tests/test_mcp_tools.py

Tests MCP server tools and resources.

**Test Classes**:
- `TestMCPTools` - Core tool functionality (mocked)
- `TestAdvancedSearchTools` - Advanced search implementations
- `TestExampleTools` - Code example retrieval tools
- `TestResourceHandlers` - MCP resource handlers
- `TestServerConfiguration` - Server configuration validation

**Tests Include**:
- Search tool with formatted results
- Search with no results
- Peripheral filter
- Code filter
- Peripheral listing
- Peripheral docs retrieval
- Invalid peripheral handling
- Code examples retrieval
- Register info retrieval
- HAL function search
- HAL function peripheral extraction
- Error solution search
- Initialization sequence search
- Clock configuration search
- Peripheral comparison
- Migration info search
- Interrupt examples
- DMA examples
- Low power examples
- Callback examples
- Resource handler initialization
- Stats retrieval
- Source listing

**Sample Test**:
```python
@patch('mcp_server.server.get_store')
def test_search_stm32_docs(self, mock_get_store, mock_store, sample_search_results):
    """Test search tool returns formatted results."""
    mock_store.search.return_value = sample_search_results
    mock_get_store.return_value = mock_store

    from mcp_server.server import search_stm32_docs
    result = search_stm32_docs("GPIO configuration")

    assert "Result 1" in result
    assert "GPIO" in result
```

#### tests/test_integration.py

End-to-end integration tests.

**Test Classes**:
- `TestProjectStructure` - Project files and directories
- `TestMCPConfiguration` - MCP config validity
- `TestModuleImports` - All module imports
- `TestEndToEndWorkflow` - Complete workflows
- `TestDataIntegrity` - Data roundtrip integrity
- `TestPeripheralEnums` - Peripheral enum completeness
- `TestDocTypeEnums` - Document type enum completeness
- `TestConfigurationValidation` - Settings validation
- `TestAgentConfiguration` - Agent config files

**Tests Include**:
- Project directories exist
- Required files exist
- MCP config valid JSON
- MCP config required fields
- Server path validity
- All module imports work
- Chunking to storage workflow
- Validation workflow
- Search workflow
- Metadata roundtrip
- Chunk ID determinism
- Common peripherals defined
- All doc types defined
- Settings validation
- Paths are Path objects
- Agent files exist
- Command files exist

**Sample Test**:
```python
def test_chunking_to_storage_workflow(self):
    """Test document chunking and storage workflow."""
    chunker = STM32Chunker(ChunkingConfig())
    chunks = chunker.chunk_document(content, "test.md")

    with tempfile.TemporaryDirectory() as tmpdir:
        store = STM32ChromaStore(Path(tmpdir))
        added = store.add_chunks(chunk_data)
        results = store.search("GPIO configuration")
        assert len(results) > 0
```

### Coverage Goals

- **Overall**: >80%
- **Critical paths**: >95%
- **Chunking**: >90%
- **Storage**: >90%
- **Server**: >85%

**Current Coverage** (as of v0.1.0):
- mcp_server: 87%
- pipeline: 92%
- storage: 89%
- Overall: 88%

## Integration Tests

### MCP Client Integration

Test MCP protocol communication.

**Location**: `tests/test_integration.py`

**Tests**:
- stdio transport
- Tool invocation
- Resource reading
- Prompt usage
- Error handling

**Manual Test**:

```bash
# Start server in test mode
STM32_SERVER_MODE=local python mcp_server/server.py

# In another terminal, use MCP client
mcp-client --server-command "python mcp_server/server.py"

# Test tool call
> call_tool search_stm32_docs query="GPIO configuration"

# Test resource read
> read_resource stm32://peripheral/GPIO

# Test prompt
> use_prompt firmware_development
```

### Claude Code Integration

Test with actual Claude Code CLI.

**Manual Test**:

1. **Verify Configuration**:
```bash
# For user scope: ~/.claude.json
cat ~/.claude.json

# For project scope: .mcp.json
cat .mcp.json
```

2. **Start Claude Code**:
```bash
claude-code
```

3. **Test Slash Commands**:
```
/stm32 GPIO configuration
/stm32-init UART 115200
/stm32-hal HAL_GPIO_Init
/stm32-debug I2C timeout
```

4. **Test Natural Language**:
```
"How do I configure GPIO for output?"
"Show me UART DMA example"
```

5. **Verify Results**:
- Check responses include documentation content
- Verify source citations
- Confirm relevance to query

### Network Mode Integration

Test HTTP/SSE transport.

**Test Procedure**:

1. **Start Server**:
```bash
STM32_SERVER_MODE=network python scripts/start_server.py --port 8765
```

2. **Test Health Endpoint**:
```bash
curl http://localhost:8765/health
# Expected: {"status": "healthy", "chunks": 2847}
```

3. **Test SSE Connection**:
```bash
curl -N http://localhost:8765/sse
# Should establish SSE stream
```

4. **Test from Client**:
Update `~/.claude.json` (or `.mcp.json` for project scope):
```json
{
  "mcpServers": {
    "stm32-docs": {
      "type": "sse",
      "url": "http://localhost:8765/sse"
    }
  }
}
```

5. **Verify Functionality**:
```bash
# Use Claude Code with network server
/stm32 GPIO configuration
```

## Performance Tests

### Ingestion Performance

**Test**: Document ingestion speed

**Command**:
```bash
time python scripts/ingest_docs.py --clear -v
```

**Expectations**:
- **Time**: 1-5 minutes for 80 files
- **Throughput**: 15-20 files/minute
- **Memory**: <4GB peak
- **Output**: 2500-3500 chunks

**Benchmark**:
```
Files: 80
Chunks: 2,847
Time: 3m 24s
Throughput: 23.5 files/minute
Memory peak: 2.8GB
```

### Search Performance

**Test**: Query latency

**Script**: `scripts/benchmark_search.py` (if exists) or manual timing

**Command**:
```python
import time
from storage.chroma_store import STM32ChromaStore

store = STM32ChromaStore("data/chroma_db/")

queries = [
    "GPIO configuration",
    "UART DMA setup",
    "SPI master mode",
    # ... more queries
]

for query in queries:
    start = time.time()
    results = store.search(query, n_results=5)
    elapsed = time.time() - start
    print(f"{query}: {elapsed*1000:.1f}ms ({len(results)} results)")
```

**Expectations**:
- **Local search**: <100ms per query
- **Network search**: <200ms per query (Tailscale)
- **Throughput**: >20 queries/second (local)

**Benchmark**:
```
GPIO configuration: 47ms (5 results)
UART DMA setup: 52ms (5 results)
SPI master mode: 41ms (5 results)
Average: 46.7ms
```

### Memory Usage

**Test**: Memory consumption

**Command**:
```bash
# Monitor during ingestion
/usr/bin/time -v python scripts/ingest_docs.py --clear

# Monitor during search
python -c "
import tracemalloc
from storage.chroma_store import STM32ChromaStore
tracemalloc.start()
store = STM32ChromaStore('data/chroma_db/')
for i in range(100):
    store.search('GPIO', n_results=5)
current, peak = tracemalloc.get_traced_memory()
print(f'Peak: {peak / 1024 / 1024:.1f}MB')
"
```

**Expectations**:
- **Ingestion**: <4GB peak
- **Search**: <500MB steady state
- **Server idle**: <200MB

## Manual Testing

### Functional Testing

#### Test 1: Basic Search
```bash
python -c "
from storage.chroma_store import STM32ChromaStore
store = STM32ChromaStore('data/chroma_db/')
results = store.search('GPIO configuration')
for r in results[:3]:
    print(f'{r.metadata[\"source_file\"]}: {r.relevance_score:.3f}')
"
```

Expected: 3+ results with scores >0.7

#### Test 2: Peripheral Filter
```python
from storage.chroma_store import STM32ChromaStore
from storage.metadata import Peripheral

store = STM32ChromaStore("data/chroma_db/")
results = store.search("PWM output", peripheral=Peripheral.TIM)

print(f"Results: {len(results)}")
for r in results:
    print(f"  {r.metadata['peripheral']}: {r.content[:50]}...")
```

Expected: All results have peripheral=TIM

#### Test 3: HAL Function Lookup
```python
from storage.chroma_store import STM32ChromaStore

store = STM32ChromaStore("data/chroma_db/")
results = store.search_function("HAL_GPIO_Init")

for r in results:
    if "HAL_GPIO_Init" in r.content:
        print(f"Found in: {r.metadata['source_file']}")
        print(r.content[:200])
        break
```

Expected: Function documentation found

#### Test 4: Code Examples
```python
from storage.chroma_store import STM32ChromaStore

store = STM32ChromaStore("data/chroma_db/")
examples = store.get_code_examples("initialization")

print(f"Found {len(examples)} examples")
for ex in examples[:3]:
    print(f"  {ex.metadata['source_file']}")
    print(f"  Contains code: {ex.metadata.get('contains_code', False)}")
```

Expected: Examples with code blocks

### Regression Testing

**After Code Changes**:

1. Run system validation:
```bash
python scripts/verify_mcp.py
```

2. Run search quality tests:
```bash
python scripts/test_retrieval.py
```

3. Run unit tests:
```bash
pytest tests/
```

4. Check critical queries:
```bash
python -c "
from storage.chroma_store import STM32ChromaStore
store = STM32ChromaStore('data/chroma_db/')
critical = [
    'GPIO configuration',
    'UART DMA',
    'HAL_Init function',
    'Clock setup'
]
for q in critical:
    results = store.search(q, n_results=1)
    print(f'{q}: {results[0].relevance_score:.3f}')
"
```

Expected: All scores >0.7

### Edge Cases

Test unusual or boundary conditions:

#### Empty Query
```python
results = store.search("")
# Expected: Empty results or all documents
```

#### Very Long Query
```python
long_query = "GPIO " * 1000
results = store.search(long_query)
# Expected: Handles gracefully
```

#### Invalid Peripheral
```python
from storage.metadata import Peripheral
try:
    results = store.search("test", peripheral="INVALID")
except ValueError:
    print("Correctly rejected invalid peripheral")
```

#### No Results
```python
results = store.search("quantum flux capacitor")
# Expected: Empty results, no crash
```

## Continuous Testing

### Pre-Commit Checks

Create `.pre-commit-config.yaml`:

```yaml
repos:
  - repo: local
    hooks:
      - id: pytest
        name: pytest
        entry: pytest
        language: system
        pass_filenames: false
        always_run: true
```

### CI/CD (Future)

GitHub Actions workflow example:

```yaml
name: Tests

on: [push, pull_request]

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      - uses: actions/setup-python@v2
        with:
          python-version: 3.11
      - run: pip install -e ".[dev]"
      - run: pytest tests/ --cov
      - run: python scripts/verify_mcp.py
```

## Test Data

### Test Fixtures

**Location**: `tests/fixtures/`

**Contents**:
- `sample_chunks.json` - Sample chunk data
- `test_documents/` - Small test markdown files
- `expected_results/` - Expected test outputs

### Creating Test Data

```bash
# Export sample data
python scripts/export_chunks.py

# Use in tests
import json
with open("data/sample_chunks.json") as f:
    test_data = json.load(f)
```

## Troubleshooting Tests

### Test Failures

#### "No module named 'pytest'"
```bash
pip install -e ".[dev]"
```

#### "Collection not found"
```bash
python scripts/ingest_docs.py --clear
```

#### "Test timeout"
Increase timeout in pytest.ini:
```ini
[pytest]
timeout = 300
```

#### "ChromaDB locked"
```bash
# Stop all servers
pkill -f "mcp_server/server.py"

# Remove lock
rm -rf data/chroma_db/.chroma.db.lock
```

### Debugging Failed Tests

```bash
# Run with verbose output
pytest tests/test_chunker.py -v -s

# Run single test
pytest tests/test_chunker.py::test_chunk_size -v

# Run with debugger
pytest tests/test_chunker.py --pdb

# Show local variables on failure
pytest tests/ -l
```

## Test Checklist

Before release or deployment:

- [ ] System validation passes (`verify_mcp.py`)
- [ ] Search quality tests pass (`test_retrieval.py`)
- [ ] Unit tests pass (`pytest tests/`)
- [ ] Coverage >80% (`pytest --cov`)
- [ ] Manual search tests work
- [ ] Claude Code integration works
- [ ] Network mode functions (if used)
- [ ] Performance benchmarks acceptable
- [ ] No errors in logs
- [ ] Documentation updated

## Related Documentation

- [Getting Started - Verify Installation](GETTING_STARTED.md#step-3-verify-installation)
- [Ingestion Process](INGESTION.md)
- [Storage API](STORAGE.md)
- [MCP Server](MCP_SERVER.md)
