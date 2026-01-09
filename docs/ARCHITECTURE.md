# System Architecture

## Overview

The STM32 MCP Documentation Server is a multi-layered system that processes STM32 documentation and provides semantic search capabilities through the Model Context Protocol (MCP). The system is designed for modularity, extensibility, and performance.

## High-Level Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                        Claude Code                              │
│                    (User Interface)                             │
│  - Slash commands (/stm32, /stm32-init, etc.)                  │
│  - Natural language queries                                     │
│  - Specialized agents (firmware, debug, power, etc.)           │
└────────────────────────────┬────────────────────────────────────┘
                             │
                             │ MCP Protocol
                             │ (stdio or HTTP/SSE)
                             │
┌────────────────────────────▼────────────────────────────────────┐
│                    MCP Protocol Layer                           │
│  - Transport: stdio (local) or HTTP/SSE (network)              │
│  - Message format: JSON-RPC 2.0                                │
│  - Capabilities: tools, resources, prompts                     │
└────────────────────────────┬────────────────────────────────────┘
                             │
                             │
┌────────────────────────────▼────────────────────────────────────┐
│                  stm32-docs MCP Server                          │
│                    (mcp_server/server.py)                       │
│  ┌──────────────┬──────────────┬──────────────┬──────────────┐ │
│  │    Tools     │  Resources   │   Prompts    │   Config     │ │
│  │  (15 tools)  │  (13 URIs)   │ (4 prompts)  │  (settings)  │ │
│  │              │              │              │              │ │
│  │ - search     │ - stm32://   │ - firmware   │ - paths      │ │
│  │ - peripheral │   peripheral │ - debug      │ - models     │ │
│  │ - examples   │   /GPIO      │ - init       │ - chunking   │ │
│  │ - hal        │ - stm32://   │ - troublesh  │ - search     │ │
│  │ - debug      │   hal/func   │              │              │ │
│  └──────┬───────┴──────┬───────┴──────────────┴──────────────┘ │
│         │              │                                        │
│         │              │                                        │
│  ┌──────▼──────┐  ┌────▼───────┐                              │
│  │   Tools     │  │ Resources  │                              │
│  │  (tools/)   │  │(resources/)│                              │
│  │             │  │            │                              │
│  │ - search.py │  │- handlers  │                              │
│  │ - examples  │  │  .py       │                              │
│  └──────┬──────┘  └────┬───────┘                              │
│         │              │                                        │
└─────────┼──────────────┼────────────────────────────────────────┘
          │              │
          │              │ Query Interface
          │              │
┌─────────▼──────────────▼────────────────────────────────────────┐
│                   Search Engine Layer                           │
│                 (storage/chroma_store.py)                       │
│  ┌──────────────────────────────────────────────────────────┐  │
│  │  STM32ChromaStore                                        │  │
│  │  - search(query, peripheral, doc_type, require_code)     │  │
│  │  - get_peripheral_docs(peripheral)                       │  │
│  │  - get_code_examples(topic)                              │  │
│  │  - search_function(function_name)                        │  │
│  │  - get_register_info(register_name)                      │  │
│  └──────────────────────┬───────────────────────────────────┘  │
│                         │                                        │
└─────────────────────────┼────────────────────────────────────────┘
                          │
                          │ Vector Search
                          │
┌─────────────────────────▼────────────────────────────────────────┐
│                   ChromaDB Vector Store                          │
│  ┌──────────────────────────────────────────────────────────┐   │
│  │  Collection: stm32_docs                                  │   │
│  │  - Embeddings: 384-dimensional vectors                   │   │
│  │  - Metadata: peripheral, doc_type, source, functions     │   │
│  │  - Full text: Original content                           │   │
│  │  - Indexes: HNSW for fast similarity search             │   │
│  └──────────────────────────────────────────────────────────┘   │
│                                                                   │
│  Storage: data/chroma_db/                                        │
│  Size: ~500MB                                                    │
│  Chunks: ~2,847 (from 80 documents)                             │
└───────────────────────────────────────────────────────────────────┘
                          ▲
                          │
                          │ Ingestion Pipeline
                          │
┌─────────────────────────┴────────────────────────────────────────┐
│              Document Processing Pipeline                        │
│                    (pipeline/chunker.py)                         │
│  ┌──────────────────────────────────────────────────────────┐   │
│  │  1. Document Loading                                     │   │
│  │     - Read markdown files from markdowns/               │   │
│  │     - Parse frontmatter and content                      │   │
│  │                                                           │   │
│  │  2. Chunking (STM32Chunker)                             │   │
│  │     - Preserve markdown structure (headers, code)        │   │
│  │     - Token-aware splitting (~1000 tokens)              │   │
│  │     - Overlap management (150 tokens)                    │   │
│  │     - Section context preservation                       │   │
│  │                                                           │   │
│  │  3. Metadata Extraction                                  │   │
│  │     - Peripheral detection (GPIO, UART, SPI, etc.)      │   │
│  │     - HAL function identification                        │   │
│  │     - Register name extraction                           │   │
│  │     - Document type classification                       │   │
│  │     - Code block detection                               │   │
│  │                                                           │   │
│  │  4. Validation (pipeline/validator.py)                  │   │
│  │     - Size limits (min 50, max 3000 tokens)            │   │
│  │     - Content quality checks                             │   │
│  │     - Metadata completeness                              │   │
│  │                                                           │   │
│  │  5. Embedding Generation                                 │   │
│  │     - Model: all-MiniLM-L6-v2                           │   │
│  │     - Batch processing for efficiency                    │   │
│  │     - 384-dimensional vectors                            │   │
│  │                                                           │   │
│  │  6. Indexing                                             │   │
│  │     - Store in ChromaDB                                  │   │
│  │     - Build similarity indexes                           │   │
│  └──────────────────────────────────────────────────────────┘   │
└───────────────────────────────────────────────────────────────────┘
                          ▲
                          │
                          │ Source Documents
                          │
┌─────────────────────────┴────────────────────────────────────────┐
│                   Source Documentation                           │
│                      (markdowns/)                                │
│  ┌──────────────────────────────────────────────────────────┐   │
│  │  80 STM32 Documentation Files                           │   │
│  │  - Application Notes (AN*)                               │   │
│  │  - Reference Manuals (RM*)                              │   │
│  │  - User Manuals (UM*)                                   │   │
│  │  - Programming Manuals (PM*)                            │   │
│  │  - Datasheets                                            │   │
│  │                                                           │   │
│  │  Total: ~160,000 lines                                   │   │
│  │  Format: Markdown with embedded code blocks             │   │
│  └──────────────────────────────────────────────────────────┘   │
└───────────────────────────────────────────────────────────────────┘
```

## Component Details

### 1. Claude Code Layer

**Location**: External (Claude desktop application)

**Responsibilities**:
- User interface for queries
- Command routing (slash commands)
- Agent orchestration
- MCP client implementation

**Interfaces**:
- Slash commands: `/stm32`, `/stm32-init`, `/stm32-hal`, `/stm32-debug`
- Natural language queries
- Specialized agents with MCP tool integration

### 2. MCP Protocol Layer

**Transports**:

#### Local Mode (stdio)
- **Use Case**: Single machine, default mode
- **Transport**: Standard input/output
- **Process**: Spawned as subprocess by Claude Code
- **Configuration**: `~/.claude.json` (user scope) or `.mcp.json` (project scope) with `command` and `args`

```json
{
  "mcpServers": {
    "stm32-docs": {
      "command": "python",
      "args": ["mcp_server/server.py"]
    }
  }
}
```

#### Network Mode (HTTP/SSE)
- **Use Case**: Multi-machine access via Tailscale
- **Transport**: HTTP with Server-Sent Events
- **Server**: Uvicorn/Starlette
- **Configuration**: `~/.claude.json` (user scope) or `.mcp.json` (project scope) with `type: "sse"` and `url`

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

**Protocol**: JSON-RPC 2.0 over MCP

### 3. MCP Server

**Location**: `mcp_server/server.py`

**Framework**: FastMCP (built on `mcp` Python package)

**Capabilities**:

#### Tools (15 total)
MCP tools are callable functions exposed to clients:

1. **search_stm32_docs** - General semantic search
2. **get_peripheral_docs** - Peripheral-specific documentation
3. **get_code_examples** - Code example retrieval
4. **lookup_hal_function** - HAL function documentation
5. **troubleshoot_error** - Error troubleshooting
6. **get_init_sequence** - Initialization code templates
7. **get_clock_config** - Clock configuration examples
8. **get_migration_guide** - Migration guides between families
9. **compare_peripherals** - Compare peripheral features
10. **get_electrical_specs** - Electrical specifications
11. **get_timing_requirements** - Timing information
12. **get_interrupt_example** - Interrupt examples
13. **get_dma_example** - DMA examples
14. **get_low_power_example** - Low-power examples
15. **list_peripherals** - List available peripherals

See [ADVANCED_TOOLS.md](ADVANCED_TOOLS.md) for details.

#### Resources (13 URIs)
MCP resources are data endpoints that clients can read:

- `stm32://peripheral/{peripheral_name}` - Peripheral documentation
- `stm32://hal/{function_name}` - HAL function details
- `stm32://register/{register_name}` - Register information
- `stm32://example/{topic}` - Code examples
- `stm32://init/{peripheral}` - Initialization templates
- `stm32://clock/{family}` - Clock configuration
- `stm32://migration/{from_to}` - Migration guides
- `stm32://specs/{peripheral}` - Electrical specs
- `stm32://troubleshoot/{error}` - Error solutions
- `stm32://compare/{peripherals}` - Peripheral comparison
- `stm32://interrupt/{peripheral}` - Interrupt setup
- `stm32://dma/{peripheral}` - DMA configuration
- `stm32://lowpower/{mode}` - Low-power mode guides

See [RESOURCES.md](RESOURCES.md) for details.

#### Prompts (4 total)
Predefined prompts for common tasks:

1. **firmware_development** - Core firmware assistance
2. **debugging_help** - Troubleshooting guidance
3. **peripheral_init** - Peripheral initialization
4. **error_analysis** - Error analysis

**Configuration**:
- Module: `mcp_server/config.py`
- Settings class with environment variable support
- Pydantic validation

### 4. Search Engine Layer

**Location**: `storage/chroma_store.py`

**Class**: `STM32ChromaStore`

**Core Methods**:

```python
class STM32ChromaStore:
    def search(
        query: str,
        peripheral: Optional[Peripheral] = None,
        doc_type: Optional[DocType] = None,
        require_code: bool = False,
        n_results: int = 5
    ) -> List[SearchResult]

    def get_peripheral_docs(
        peripheral: Peripheral,
        n_results: int = 10
    ) -> List[SearchResult]

    def get_code_examples(
        topic: str,
        peripheral: Optional[Peripheral] = None,
        n_results: int = 5
    ) -> List[SearchResult]

    def search_function(
        function_name: str,
        n_results: int = 5
    ) -> List[SearchResult]

    def get_register_info(
        register_name: str,
        n_results: int = 5
    ) -> List[SearchResult]
```

**Features**:
- Metadata filtering (peripheral, doc_type, code presence)
- Relevance scoring
- Result deduplication
- Peripheral distribution statistics
- Batch operations

See [STORAGE.md](STORAGE.md) for details.

### 5. ChromaDB Vector Store

**Technology**: ChromaDB (embedded SQLite + HNSW index)

**Collection Schema**:

```python
{
    "id": str,                    # Unique chunk identifier
    "embeddings": List[float],    # 384-dim vector
    "metadatas": {
        "source_file": str,       # Original markdown file
        "peripheral": str,        # Primary peripheral (if any)
        "peripherals": str,       # JSON array of all peripherals
        "doc_type": str,          # application_note, reference_manual, etc.
        "section": str,           # Document section/header
        "hal_functions": str,     # JSON array of HAL functions
        "registers": str,         # JSON array of register names
        "contains_code": bool,    # Has code blocks
        "chunk_index": int,       # Position in document
        "total_chunks": int,      # Total chunks from document
        "timestamp": str          # ISO format
    },
    "documents": str              # Full text content
}
```

**Indexing**: HNSW (Hierarchical Navigable Small World) for fast approximate nearest neighbor search

**Storage**:
- Path: `data/chroma_db/`
- Format: SQLite + Parquet
- Size: ~500MB for 80 documents

See [STORAGE.md](STORAGE.md) for schema details.

### 6. Document Processing Pipeline

**Location**: `pipeline/chunker.py`

**Main Class**: `STM32Chunker`

#### Chunking Strategy

1. **Structural Preservation**
   - Respect markdown headers (##, ###, ####)
   - Keep code blocks intact
   - Preserve lists and tables
   - Maintain section context

2. **Token-Aware Splitting**
   - Target: 1000 tokens per chunk
   - Overlap: 150 tokens between chunks
   - Tokenizer: tiktoken (cl100k_base)
   - Min size: 50 tokens
   - Max size: 3000 tokens

3. **Metadata Extraction**
   - **Peripheral Detection**: Pattern matching for GPIO, UART, SPI, etc.
   - **HAL Functions**: Regex for `HAL_*` functions
   - **Registers**: Pattern for register names (e.g., `GPIO_MODER`)
   - **Document Type**: From filename patterns
   - **Code Presence**: Detect code blocks

4. **Validation**
   - Size constraints
   - Content quality (non-empty, meaningful)
   - Metadata completeness

See [CHUNKING.md](CHUNKING.md) for algorithm details.

### 7. Source Documentation

**Location**: `markdowns/`

**Content**:
- 80 STM32 documentation files
- Converted from PDF to markdown
- ~160,000 lines total
- Application notes, reference manuals, user manuals

**Document Types**:
- **Application Notes (AN*)**: Specific use cases and examples
- **Reference Manuals (RM*)**: Complete peripheral documentation
- **User Manuals (UM*)**: Development board guides
- **Programming Manuals (PM*)**: Processor core details
- **Datasheets**: Electrical specifications

## Data Flow

### Ingestion Flow

```
1. Load Markdown Files
   ├─ Read from markdowns/
   └─ Parse frontmatter and content

2. Chunk Documents
   ├─ Split by structure (headers, code blocks)
   ├─ Target 1000 tokens per chunk
   ├─ Apply 150 token overlap
   └─ Preserve section context

3. Extract Metadata
   ├─ Detect peripherals (GPIO, UART, etc.)
   ├─ Find HAL functions (HAL_*)
   ├─ Identify registers (*_MODER, etc.)
   ├─ Classify document type
   └─ Detect code blocks

4. Validate Chunks
   ├─ Check size (50-3000 tokens)
   ├─ Verify content quality
   └─ Ensure metadata completeness

5. Generate Embeddings
   ├─ Model: all-MiniLM-L6-v2
   ├─ Batch size: 32
   ├─ Output: 384-dim vectors
   └─ Normalize vectors

6. Index in ChromaDB
   ├─ Store embeddings
   ├─ Store metadata
   ├─ Store full text
   └─ Build HNSW index

7. Statistics
   ├─ Count chunks per peripheral
   ├─ Count chunks per document type
   └─ Report ingestion metrics
```

### Query Flow

```
1. User Query
   ├─ Via slash command (/stm32)
   ├─ Via natural language
   └─ Via specialized agent

2. MCP Tool Call
   ├─ Parse parameters (query, peripheral, etc.)
   ├─ Route to appropriate tool
   └─ Apply filters

3. Embedding
   ├─ Generate query embedding
   ├─ Same model as ingestion
   └─ 384-dim vector

4. Vector Search
   ├─ Similarity search in ChromaDB
   ├─ Apply metadata filters
   ├─ Compute relevance scores
   └─ Return top N results

5. Post-Processing
   ├─ Deduplicate results
   ├─ Format for display
   └─ Add context (source, peripheral)

6. Response
   ├─ Return to MCP client
   └─ Display in Claude Code
```

## Transport Modes

### Local Mode (stdio)

**Architecture**:
```
Claude Code
    │
    ├─ spawns ──> MCP Server Process
    │                 │
    │                 ├─ stdin  (receives requests)
    │                 └─ stdout (sends responses)
    │
    ├─ reads stdout
    └─ writes stdin
```

**Characteristics**:
- Single process per client
- Low latency (~10ms)
- No network overhead
- Automatic process lifecycle
- Default mode

**Use Cases**:
- Local development
- Single-machine usage
- Maximum performance

### Network Mode (HTTP/SSE)

**Architecture**:
```
Claude Code Client 1                Claude Code Client 2
    │                                       │
    │ HTTP POST (tool call)                 │
    ├───────────────────┐                   │
    │                   │                   │
    │              ┌────▼───────────────────▼────┐
    │              │   MCP Server (Uvicorn)      │
    │              │   http://0.0.0.0:8765       │
    │              │                             │
    │              │   Endpoints:                │
    │              │   - /sse (SSE transport)    │
    │              │   - /health (status)        │
    │              └─────────────────────────────┘
    │                           │
    └─ SSE stream ─────────────┘
       (server responses)
```

**Characteristics**:
- Shared server process
- Higher latency (~50-100ms over Tailscale)
- Multiple concurrent clients
- Persistent connection via SSE
- Manual server start

**Use Cases**:
- Multi-machine access
- Tailscale network
- Shared documentation server
- Team usage

## Configuration Management

**Module**: `mcp_server/config.py`

**Implementation**: Pydantic Settings

```python
class Settings(BaseSettings):
    # Server
    SERVER_MODE: ServerMode = ServerMode.LOCAL
    SERVER_NAME: str = "stm32-docs"
    HOST: str = "0.0.0.0"
    PORT: int = 8765

    # Database
    CHROMA_DB_PATH: Path = Path("data/chroma_db")
    COLLECTION_NAME: str = "stm32_docs"
    EMBEDDING_MODEL: str = "all-MiniLM-L6-v2"

    # Processing
    CHUNK_SIZE: int = 1000
    CHUNK_OVERLAP: int = 150
    RAW_DOCS_DIR: Path = Path("markdowns")

    # Search
    DEFAULT_SEARCH_RESULTS: int = 5
    MAX_SEARCH_RESULTS: int = 10

    # Logging
    LOG_LEVEL: LogLevel = LogLevel.INFO
    LOG_FORMAT: str = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"

    class Config:
        env_prefix = "STM32_"
        env_file = ".env"
```

**Environment Variables**:
All settings can be overridden with `STM32_*` prefixed environment variables.

## Specialized Agents

**Location**: `.claude/agents/`

Specialized agents automatically use MCP tools for domain-specific tasks:

| Agent | Domain | Primary Tools |
|-------|--------|---------------|
| **firmware** | Core development | search_stm32_docs, get_init_sequence |
| **debug** | Troubleshooting | troubleshoot_error, search_stm32_docs |
| **power** | Power management | search_stm32_docs, get_low_power_example |
| **peripheral-comm** | UART/SPI/I2C | get_peripheral_docs, get_code_examples |
| **peripheral-analog** | ADC/DAC | get_peripheral_docs, lookup_hal_function |
| **security** | Cryptography | search_stm32_docs, get_code_examples |
| **bootloader** | Boot systems | search_stm32_docs, get_init_sequence |

See [AGENT_MCP_INTEGRATION.md](AGENT_MCP_INTEGRATION.md) for details.

## Performance Characteristics

### Ingestion
- **Time**: 1-5 minutes for 80 files (CPU)
- **Throughput**: ~15-20 files/minute
- **Memory**: ~2GB peak during embedding generation
- **Output**: ~3000 chunks

### Search
- **Latency**: <100ms per query (local)
- **Latency**: <200ms per query (network over Tailscale)
- **Throughput**: ~20 queries/second (local), ~10 queries/second (network)
- **Accuracy**: 0.7-0.95 relevance scores for related content

### Storage
- **Size**: ~500MB for 80 documents
- **Growth**: ~6MB per document
- **Index**: HNSW (logarithmic query time)

## Scalability

### Current Scale
- Documents: 80
- Chunks: ~3,000
- Peripherals: 15
- Embedding dimension: 384

### Theoretical Limits
- ChromaDB: Up to millions of vectors
- Embedding generation: Limited by CPU/GPU
- Network mode: Limited by network bandwidth and server resources

### Scaling Strategies
1. **More Documents**: Linear growth in storage and ingestion time
2. **Larger Chunks**: Reduce chunk count, but may decrease search precision
3. **Better Embeddings**: Use larger models (768 or 1024 dim) for improved accuracy
4. **GPU Acceleration**: 10-50x faster embedding generation
5. **Distributed Search**: Shard by peripheral or document type

## Security Considerations

### Local Mode
- No network exposure
- File system access limited to project directory
- Process isolation via subprocess

### Network Mode
- **Exposure**: Server listens on all interfaces (0.0.0.0)
- **Recommendation**: Use only on trusted networks (Tailscale)
- **No Authentication**: Currently no authentication mechanism
- **Transport**: HTTP (not HTTPS) - acceptable on Tailscale VPN

### Future Enhancements
- API key authentication
- HTTPS support
- Rate limiting
- Request logging

## Error Handling

### Ingestion Errors
- **File not found**: Log error, continue with other files
- **Parsing errors**: Log error, skip file
- **Embedding errors**: Retry with exponential backoff
- **Database errors**: Fail fast, report to user

### Search Errors
- **Empty results**: Return empty list, log warning
- **Invalid filters**: Fall back to unfiltered search
- **Embedding errors**: Return error to client
- **Database connection**: Retry with backoff

### Network Errors
- **Connection timeout**: Return error, client retries
- **SSE disconnect**: Client reconnects automatically
- **Server crash**: Client detects and reports

## Monitoring

### Available Metrics
- Chunk count: `store.count()`
- Peripheral distribution: `store.get_peripheral_distribution()`
- Document statistics: `store.get_stats()`
- Search performance: Log query time

### Health Checks
- `/health` endpoint (network mode)
- Database connectivity check
- Embedding model load status

### Logging
- Level: INFO (configurable)
- Output: stdout and optional log file
- Format: Timestamp, level, message

## Future Architecture Enhancements

### Planned Improvements
1. **Caching**: Redis cache for frequent queries
2. **Reranking**: Cross-encoder reranker for improved precision
3. **Hybrid Search**: Combine vector search with keyword search
4. **Multi-Model**: Support multiple embedding models
5. **Incremental Updates**: Update specific documents without full rebuild
6. **Query Analytics**: Track query patterns and relevance feedback
7. **Distributed Deployment**: Load balancing and horizontal scaling

### Integration Opportunities
1. **IDE Plugins**: VSCode, CLion integration
2. **Web Interface**: Browser-based documentation explorer
3. **API Gateway**: RESTful API for broader access
4. **Continuous Ingestion**: Auto-update from documentation sources
5. **Community Contributions**: User-contributed documentation

## Related Documentation

- [MCP Server Details](MCP_SERVER.md)
- [Storage Layer](STORAGE.md)
- [Document Processing](CHUNKING.md)
- [Advanced Tools](ADVANCED_TOOLS.md)
- [Resources](RESOURCES.md)
- [Infrastructure](INFRASTRUCTURE.md)
