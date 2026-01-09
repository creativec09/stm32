# STM32 MCP Documentation Server - Agent Execution Plan

## Overview

This plan builds a custom MCP server for STM32 documentation retrieval. The system will:
- Process 78 markdown files (~160K lines) into searchable chunks
- Provide semantic search via ChromaDB vector store
- Expose tools and resources via MCP protocol
- Integrate with Claude Code and specialized STM32 agents

## Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                        Claude Code                               │
│                    (User Interface)                              │
├─────────────────────────────────────────────────────────────────┤
│                     MCP Protocol Layer                           │
├─────────────────────────────────────────────────────────────────┤
│                   stm32-docs MCP Server                          │
│  ┌─────────────┬─────────────┬─────────────┬─────────────┐      │
│  │   Tools     │  Resources  │   Prompts   │   Search    │      │
│  │ search_docs │ stm32://... │ debug_help  │   Engine    │      │
│  │ get_examples│             │ config_help │             │      │
│  └─────────────┴─────────────┴─────────────┴─────────────┘      │
├─────────────────────────────────────────────────────────────────┤
│                      ChromaDB Vector Store                       │
│              (Embeddings + Metadata + Full Text)                 │
├─────────────────────────────────────────────────────────────────┤
│                   Document Processing Pipeline                   │
│        (Chunking → Embedding → Indexing → Validation)           │
└─────────────────────────────────────────────────────────────────┘
```

## Directory Structure (Target)

```
/mnt/c/Users/creat/Claude/stm32-agents/
├── mcp-server/
│   ├── __init__.py
│   ├── server.py              # Main MCP server
│   ├── tools/
│   │   ├── __init__.py
│   │   ├── search.py          # Search tools
│   │   ├── examples.py        # Code example tools
│   │   └── peripheral.py      # Peripheral-specific tools
│   ├── resources/
│   │   ├── __init__.py
│   │   └── handlers.py        # Resource URI handlers
│   └── config.py              # Server configuration
├── pipeline/
│   ├── __init__.py
│   ├── chunker.py             # Document chunking logic
│   ├── embedder.py            # Embedding generation
│   ├── ingester.py            # Full ingestion pipeline
│   └── validator.py           # Chunk quality validation
├── storage/
│   ├── __init__.py
│   ├── chroma_store.py        # ChromaDB wrapper
│   └── metadata.py            # Metadata schema
├── scripts/
│   ├── ingest_docs.py         # Run document ingestion
│   ├── test_retrieval.py      # Test search quality
│   └── start_server.py        # Launch MCP server
├── data/
│   ├── raw/                   # Original markdown files (your 78 docs)
│   ├── chunks/                # Processed chunks (JSON)
│   └── chroma_db/             # ChromaDB persistent storage
├── tests/
│   ├── test_chunking.py
│   ├── test_search.py
│   └── test_mcp_tools.py
├── .claude/
│   ├── mcp.json               # MCP server configuration
│   └── agents/                # Updated agent files
├── pyproject.toml
├── requirements.txt
└── README.md
```

---

## Agent Execution Sequence

```
Phase 1: Infrastructure
    └── Agent 1 (Opus): Project Setup
            │
            ▼
Phase 2: Document Processing
    ┌───────┴───────┐
    │               │
Agent 2 (Sonnet)  Agent 3 (Sonnet)
Chunking Logic    Metadata Schema
    │               │
    └───────┬───────┘
            │
            ▼
    Agent 4 (Haiku): Ingestion Script
            │
            ▼
Phase 3: MCP Server
    Agent 5 (Opus): MCP Server Core
            │
    ┌───────┴───────┐
    │               │
Agent 6 (Opus)   Agent 7 (Sonnet)
Search Tools     Resource Handlers
    │               │
    └───────┬───────┘
            │
            ▼
Phase 4: Integration
    Agent 8 (Opus): Claude Code Config
            │
            ▼
    Agent 9 (Opus): Update Existing Agents
            │
            ▼
Phase 5: Validation
    Agent 10 (Opus): Testing & Quality
            │
            ▼
    Agent 11 (Sonnet): Documentation
```

---

## Phase 1: Infrastructure Setup

### Agent 1: Project Setup (Opus)

**Dependencies:** None (runs first)

**Model:** Opus

**Description:** Creates the complete project structure, dependency files, and base configuration.

**Full Prompt:**

```
You are setting up a Python project for an STM32 documentation MCP server. This server will provide semantic search over 78 markdown files containing STM32 reference documentation.

## Your Task

Create the complete project infrastructure:

### 1. Create Directory Structure

Create all directories as specified:
```
/mnt/c/Users/creat/Claude/stm32-agents/
├── mcp-server/
│   ├── tools/
│   └── resources/
├── pipeline/
├── storage/
├── scripts/
├── data/
│   ├── raw/
│   ├── chunks/
│   └── chroma_db/
└── tests/
```

### 2. Create pyproject.toml

```toml
[project]
name = "stm32-mcp-docs"
version = "0.1.0"
description = "MCP server for STM32 documentation retrieval"
requires-python = ">=3.11"
dependencies = [
    "mcp>=1.0.0",
    "chromadb>=0.4.0",
    "sentence-transformers>=2.2.0",
    "pydantic>=2.0.0",
    "python-dotenv>=1.0.0",
    "tiktoken>=0.5.0",
    "rich>=13.0.0",
    "typer>=0.9.0",
]

[project.optional-dependencies]
dev = [
    "pytest>=7.0.0",
    "pytest-asyncio>=0.21.0",
    "ruff>=0.1.0",
]

[project.scripts]
stm32-docs = "scripts.start_server:main"
ingest = "scripts.ingest_docs:main"
```

### 3. Create requirements.txt

Generate from pyproject.toml dependencies with pinned versions.

### 4. Create mcp-server/config.py

```python
from pathlib import Path
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    # Paths
    PROJECT_ROOT: Path = Path(__file__).parent.parent
    DATA_DIR: Path = PROJECT_ROOT / "data"
    RAW_DOCS_DIR: Path = DATA_DIR / "raw"
    CHUNKS_DIR: Path = DATA_DIR / "chunks"
    CHROMA_DB_PATH: Path = DATA_DIR / "chroma_db"

    # Chunking
    CHUNK_SIZE: int = 1000  # tokens
    CHUNK_OVERLAP: int = 150  # tokens
    MIN_CHUNK_SIZE: int = 50  # tokens

    # Embeddings
    EMBEDDING_MODEL: str = "all-MiniLM-L6-v2"

    # ChromaDB
    COLLECTION_NAME: str = "stm32_docs"

    # Search
    DEFAULT_RESULTS: int = 5
    MAX_RESULTS: int = 20

    class Config:
        env_file = ".env"
        env_prefix = "STM32_"

settings = Settings()
```

### 5. Create all __init__.py files

Create empty __init__.py in each Python package directory.

### 6. Create .env.example

```
STM32_EMBEDDING_MODEL=all-MiniLM-L6-v2
STM32_CHUNK_SIZE=1000
STM32_CHUNK_OVERLAP=150
```

### 7. Create .gitignore

Include:
- data/chroma_db/
- data/chunks/
- __pycache__/
- *.pyc
- .env
- .venv/
- *.egg-info/

## Success Criteria

- All directories exist
- pyproject.toml is valid
- All __init__.py files created
- Config loads without errors

## Execution

Use Bash and Write tools to create all files and directories. Verify the structure with ls commands.
```

---

## Phase 2: Document Processing

### Agent 2: Chunking Logic (Sonnet)

**Dependencies:** Agent 1 (project structure must exist)

**Model:** Sonnet

**Description:** Implements the intelligent document chunking system optimized for STM32 markdown documentation.

**Full Prompt:**

```
You are implementing the document chunking pipeline for STM32 documentation. The documents are markdown files containing technical documentation about STM32 microcontrollers.

## Context

The project structure already exists at /mnt/c/Users/creat/Claude/stm32-agents/. You need to create the chunking logic.

## Your Task

Create the following files:

### 1. pipeline/chunker.py

Implement a chunker that:

1. **Respects Markdown Structure**
   - Split on headers (H1, H2, H3)
   - Keep code blocks intact (never split mid-code)
   - Preserve tables as atomic units
   - Maintain list structures

2. **Token-Aware Splitting**
   - Use tiktoken (cl100k_base) for token counting
   - Target chunk size: 800-1200 tokens
   - Overlap: 100-150 tokens for context continuity

3. **STM32-Specific Handling**
   - Detect register definitions (keep together)
   - Identify peripheral sections
   - Extract code examples as tagged content

```python
# Required classes/functions:

@dataclass
class Chunk:
    id: str                      # Unique chunk ID
    content: str                 # Chunk text
    token_count: int             # Token count
    metadata: ChunkMetadata      # Rich metadata

@dataclass
class ChunkMetadata:
    source_file: str             # Original filename
    doc_type: str                # reference_manual, app_note, etc.
    section_path: list[str]      # ["GPIO", "Configuration", "Mode Register"]
    peripheral: str | None       # GPIO, UART, SPI, etc.
    has_code: bool              # Contains code blocks
    has_table: bool             # Contains tables
    has_register: bool          # Contains register definitions
    start_line: int             # Line number in source
    chunk_index: int            # Index within document

class STM32Chunker:
    def __init__(self, config: ChunkingConfig): ...

    def chunk_document(self, content: str, source_file: str) -> list[Chunk]: ...

    def _split_by_headers(self, content: str) -> list[Section]: ...

    def _split_large_section(self, section: Section) -> list[str]: ...

    def _extract_code_blocks(self, text: str) -> list[CodeBlock]: ...

    def _detect_peripheral(self, text: str) -> str | None: ...

    def _detect_doc_type(self, filename: str, content: str) -> str: ...

    def _count_tokens(self, text: str) -> int: ...

    def _generate_chunk_id(self, source: str, index: int, content: str) -> str: ...
```

### 2. pipeline/validator.py

Validate chunk quality:

```python
class ChunkValidator:
    def validate_chunk(self, chunk: Chunk) -> ValidationResult: ...

    def check_token_bounds(self, chunk: Chunk) -> bool: ...

    def check_code_integrity(self, chunk: Chunk) -> bool: ...

    def check_table_integrity(self, chunk: Chunk) -> bool: ...

    def generate_report(self, chunks: list[Chunk]) -> ValidationReport: ...
```

## Key Rules

1. **Never split code blocks** - If a code block would cause overflow, it becomes its own chunk
2. **Keep register tables intact** - Bit field tables must stay together
3. **Preserve header hierarchy** - Track the path of headers for context
4. **Detect peripherals** - Parse for GPIO, UART, SPI, I2C, ADC, TIM, DMA, RCC, NVIC, etc.
5. **Handle oversized content** - If content exceeds 2000 tokens and can't be split, flag it

## Test Your Implementation

Create a simple test in the file that chunks a sample markdown:

```python
if __name__ == "__main__":
    sample = '''
    # GPIO Configuration

    ## Overview

    The GPIO peripheral provides...

    ## Register Map

    | Register | Offset | Description |
    |----------|--------|-------------|
    | MODER    | 0x00   | Mode register |

    ## Code Example

    ```c
    HAL_GPIO_Init(GPIOA, &gpio);
    ```
    '''

    chunker = STM32Chunker(ChunkingConfig())
    chunks = chunker.chunk_document(sample, "gpio_guide.md")
    for chunk in chunks:
        print(f"Chunk {chunk.id}: {chunk.token_count} tokens")
        print(f"  Peripheral: {chunk.metadata.peripheral}")
```

## Success Criteria

- Chunker produces valid chunks from markdown
- Code blocks never split
- Token counts within bounds
- Metadata correctly extracted
- Validator catches malformed chunks
```

---

### Agent 3: Metadata Schema (Sonnet)

**Dependencies:** Agent 1 (project structure)

**Model:** Sonnet

**Description:** Defines the metadata schema and storage wrapper for ChromaDB.

**Full Prompt:**

```
You are implementing the storage layer for the STM32 documentation MCP server. This includes the metadata schema and ChromaDB wrapper.

## Context

Project exists at /mnt/c/Users/creat/Claude/stm32-agents/. Chunking logic is being developed separately.

## Your Task

### 1. Create storage/metadata.py

Define comprehensive metadata schemas:

```python
from enum import Enum
from pydantic import BaseModel, Field
from typing import Optional

class DocType(str, Enum):
    REFERENCE_MANUAL = "reference_manual"
    APPLICATION_NOTE = "application_note"
    USER_MANUAL = "user_manual"
    PROGRAMMING_MANUAL = "programming_manual"
    DATASHEET = "datasheet"
    HAL_GUIDE = "hal_guide"
    GENERAL = "general"

class Peripheral(str, Enum):
    GPIO = "GPIO"
    UART = "UART"
    USART = "USART"
    SPI = "SPI"
    I2C = "I2C"
    ADC = "ADC"
    DAC = "DAC"
    TIM = "TIM"
    DMA = "DMA"
    RCC = "RCC"
    NVIC = "NVIC"
    EXTI = "EXTI"
    PWR = "PWR"
    FLASH = "FLASH"
    USB = "USB"
    CAN = "CAN"
    ETH = "ETH"
    SDMMC = "SDMMC"
    LTDC = "LTDC"
    DCMI = "DCMI"
    RNG = "RNG"
    CRYP = "CRYP"
    GENERAL = "GENERAL"

class ContentType(str, Enum):
    CONCEPTUAL = "conceptual"
    REGISTER_MAP = "register_map"
    CODE_EXAMPLE = "code_example"
    CONFIGURATION = "configuration"
    TROUBLESHOOTING = "troubleshooting"
    ELECTRICAL_SPEC = "electrical_spec"

class ChunkMetadataSchema(BaseModel):
    """Schema for chunk metadata stored in ChromaDB."""

    # Source identification
    source_file: str = Field(..., description="Original filename")
    doc_type: DocType = Field(..., description="Document type")

    # Content classification
    peripheral: Optional[Peripheral] = Field(None, description="Primary peripheral")
    secondary_peripherals: list[str] = Field(default_factory=list)
    content_type: ContentType = Field(ContentType.CONCEPTUAL)

    # Hierarchy
    section_path: list[str] = Field(default_factory=list, description="Header hierarchy")
    section_title: str = Field("", description="Current section title")

    # Content flags
    has_code: bool = Field(False)
    has_table: bool = Field(False)
    has_register_map: bool = Field(False)
    has_diagram_ref: bool = Field(False)

    # Position
    chunk_index: int = Field(0)
    start_line: int = Field(0)

    # STM32 specific
    stm32_families: list[str] = Field(default_factory=list, description="e.g., ['STM32F4', 'STM32H7']")
    hal_functions: list[str] = Field(default_factory=list, description="HAL functions mentioned")
    registers: list[str] = Field(default_factory=list, description="Registers mentioned")

    def to_chroma_metadata(self) -> dict:
        """Convert to flat dict for ChromaDB storage."""
        return {
            "source_file": self.source_file,
            "doc_type": self.doc_type.value,
            "peripheral": self.peripheral.value if self.peripheral else "",
            "secondary_peripherals": ",".join(self.secondary_peripherals),
            "content_type": self.content_type.value,
            "section_path": " > ".join(self.section_path),
            "section_title": self.section_title,
            "has_code": self.has_code,
            "has_table": self.has_table,
            "has_register_map": self.has_register_map,
            "chunk_index": self.chunk_index,
            "stm32_families": ",".join(self.stm32_families),
            "hal_functions": ",".join(self.hal_functions[:5]),  # Limit for storage
            "registers": ",".join(self.registers[:10]),
        }

    @classmethod
    def from_chroma_metadata(cls, data: dict) -> "ChunkMetadataSchema":
        """Reconstruct from ChromaDB metadata."""
        return cls(
            source_file=data.get("source_file", ""),
            doc_type=DocType(data.get("doc_type", "general")),
            peripheral=Peripheral(data["peripheral"]) if data.get("peripheral") else None,
            # ... reconstruct other fields
        )
```

### 2. Create storage/chroma_store.py

ChromaDB wrapper with search capabilities:

```python
import chromadb
from chromadb.config import Settings
from sentence_transformers import SentenceTransformer
from pathlib import Path
from typing import Optional
from .metadata import ChunkMetadataSchema, Peripheral, DocType

class STM32ChromaStore:
    """ChromaDB wrapper for STM32 documentation."""

    def __init__(
        self,
        persist_dir: Path,
        collection_name: str = "stm32_docs",
        embedding_model: str = "all-MiniLM-L6-v2"
    ):
        self.persist_dir = persist_dir
        self.collection_name = collection_name

        # Initialize ChromaDB
        self.client = chromadb.PersistentClient(
            path=str(persist_dir),
            settings=Settings(anonymized_telemetry=False)
        )

        # Initialize embedding model
        self.embedder = SentenceTransformer(embedding_model)

        # Get or create collection
        self.collection = self.client.get_or_create_collection(
            name=collection_name,
            metadata={"hnsw:space": "cosine"}
        )

    def add_chunks(
        self,
        chunks: list[tuple[str, str, ChunkMetadataSchema]]  # (id, content, metadata)
    ) -> int:
        """Add chunks to the store. Returns count added."""
        if not chunks:
            return 0

        ids = [c[0] for c in chunks]
        contents = [c[1] for c in chunks]
        metadatas = [c[2].to_chroma_metadata() for c in chunks]

        # Generate embeddings
        embeddings = self.embedder.encode(contents).tolist()

        # Add to collection
        self.collection.add(
            ids=ids,
            embeddings=embeddings,
            documents=contents,
            metadatas=metadatas
        )

        return len(chunks)

    def search(
        self,
        query: str,
        n_results: int = 5,
        peripheral: Optional[Peripheral] = None,
        doc_type: Optional[DocType] = None,
        require_code: bool = False,
        require_register: bool = False
    ) -> list[dict]:
        """Search for relevant chunks."""

        # Build filter
        where = {}
        if peripheral:
            where["peripheral"] = peripheral.value
        if doc_type:
            where["doc_type"] = doc_type.value
        if require_code:
            where["has_code"] = True
        if require_register:
            where["has_register_map"] = True

        # Generate query embedding
        query_embedding = self.embedder.encode(query).tolist()

        # Search
        results = self.collection.query(
            query_embeddings=[query_embedding],
            n_results=n_results,
            where=where if where else None,
            include=["documents", "metadatas", "distances"]
        )

        # Format results
        formatted = []
        for i in range(len(results['ids'][0])):
            formatted.append({
                'id': results['ids'][0][i],
                'content': results['documents'][0][i],
                'metadata': results['metadatas'][0][i],
                'score': 1 - results['distances'][0][i]  # Convert distance to similarity
            })

        return formatted

    def search_by_peripheral(
        self,
        peripheral: Peripheral,
        query: str = "",
        n_results: int = 10
    ) -> list[dict]:
        """Get all documentation for a specific peripheral."""
        return self.search(
            query=query or f"{peripheral.value} configuration usage",
            n_results=n_results,
            peripheral=peripheral
        )

    def get_code_examples(
        self,
        topic: str,
        peripheral: Optional[Peripheral] = None,
        n_results: int = 5
    ) -> list[dict]:
        """Get code examples for a topic."""
        return self.search(
            query=f"{topic} code example",
            n_results=n_results,
            peripheral=peripheral,
            require_code=True
        )

    def get_register_info(
        self,
        register_name: str,
        n_results: int = 3
    ) -> list[dict]:
        """Get register documentation."""
        return self.search(
            query=f"{register_name} register bits configuration",
            n_results=n_results,
            require_register=True
        )

    def get_stats(self) -> dict:
        """Get collection statistics."""
        count = self.collection.count()

        # Get peripheral distribution (sample)
        sample = self.collection.get(limit=1000, include=["metadatas"])
        peripheral_counts = {}
        doc_type_counts = {}

        for meta in sample['metadatas']:
            p = meta.get('peripheral', 'UNKNOWN')
            peripheral_counts[p] = peripheral_counts.get(p, 0) + 1

            d = meta.get('doc_type', 'unknown')
            doc_type_counts[d] = doc_type_counts.get(d, 0) + 1

        return {
            "total_chunks": count,
            "peripheral_distribution": peripheral_counts,
            "doc_type_distribution": doc_type_counts
        }

    def clear(self):
        """Clear all data (use with caution)."""
        self.client.delete_collection(self.collection_name)
        self.collection = self.client.get_or_create_collection(
            name=self.collection_name,
            metadata={"hnsw:space": "cosine"}
        )
```

## Success Criteria

- Metadata schema validates correctly
- ChromaDB operations work (add, search, filter)
- Peripheral filtering returns correct results
- Stats provide useful distribution info

## Test

Include a simple test at the end of chroma_store.py:

```python
if __name__ == "__main__":
    from pathlib import Path
    import tempfile

    with tempfile.TemporaryDirectory() as tmpdir:
        store = STM32ChromaStore(Path(tmpdir))

        # Add test chunk
        meta = ChunkMetadataSchema(
            source_file="test.md",
            doc_type=DocType.HAL_GUIDE,
            peripheral=Peripheral.GPIO,
            has_code=True
        )

        store.add_chunks([
            ("test_001", "Configure GPIO pin as output using HAL_GPIO_Init", meta)
        ])

        # Search
        results = store.search("GPIO configuration")
        print(f"Found {len(results)} results")
        print(results[0] if results else "No results")
```
```

---

### Agent 4: Ingestion Script (Haiku)

**Dependencies:** Agent 2 (chunker) and Agent 3 (storage)

**Model:** Haiku

**Description:** Creates the document ingestion script that processes all markdown files.

**Full Prompt:**

```
You are creating the document ingestion script for the STM32 MCP documentation server.

## Context

- Project at /mnt/c/Users/creat/Claude/stm32-agents/
- Chunking logic exists in pipeline/chunker.py
- Storage exists in storage/chroma_store.py
- Raw markdown files are in the project root (78 files, ~160K lines)

## Your Task

Create scripts/ingest_docs.py:

```python
#!/usr/bin/env python3
"""
Ingest STM32 markdown documentation into ChromaDB.

Usage:
    python scripts/ingest_docs.py [--source-dir PATH] [--clear]
"""

import sys
from pathlib import Path
import argparse
from rich.console import Console
from rich.progress import Progress, SpinnerColumn, TextColumn, BarColumn, TaskProgressColumn
from rich.table import Table

# Add project root to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from pipeline.chunker import STM32Chunker, ChunkingConfig
from storage.chroma_store import STM32ChromaStore
from mcp_server.config import settings

console = Console()

def find_markdown_files(source_dir: Path) -> list[Path]:
    """Find all markdown files in directory."""
    return list(source_dir.glob("**/*.md"))

def ingest_documents(
    source_dir: Path,
    clear_existing: bool = False,
    verbose: bool = False
):
    """Main ingestion function."""

    console.print(f"\n[bold blue]STM32 Documentation Ingestion[/bold blue]")
    console.print(f"Source: {source_dir}")
    console.print(f"Database: {settings.CHROMA_DB_PATH}\n")

    # Find files
    md_files = find_markdown_files(source_dir)
    console.print(f"Found [green]{len(md_files)}[/green] markdown files")

    if not md_files:
        console.print("[red]No markdown files found![/red]")
        return

    # Initialize components
    chunker = STM32Chunker(ChunkingConfig(
        chunk_size=settings.CHUNK_SIZE,
        chunk_overlap=settings.CHUNK_OVERLAP,
        min_chunk_size=settings.MIN_CHUNK_SIZE
    ))

    store = STM32ChromaStore(
        persist_dir=settings.CHROMA_DB_PATH,
        collection_name=settings.COLLECTION_NAME,
        embedding_model=settings.EMBEDDING_MODEL
    )

    if clear_existing:
        console.print("[yellow]Clearing existing data...[/yellow]")
        store.clear()

    # Process files
    total_chunks = 0
    failed_files = []

    with Progress(
        SpinnerColumn(),
        TextColumn("[progress.description]{task.description}"),
        BarColumn(),
        TaskProgressColumn(),
        console=console
    ) as progress:

        task = progress.add_task("Processing files...", total=len(md_files))

        for md_file in md_files:
            try:
                # Read file
                content = md_file.read_text(encoding='utf-8')

                # Chunk
                chunks = chunker.chunk_document(content, md_file.name)

                # Prepare for storage
                chunk_data = [
                    (chunk.id, chunk.content, chunk.metadata)
                    for chunk in chunks
                ]

                # Store
                added = store.add_chunks(chunk_data)
                total_chunks += added

                if verbose:
                    console.print(f"  {md_file.name}: {added} chunks")

            except Exception as e:
                failed_files.append((md_file.name, str(e)))
                console.print(f"[red]Error processing {md_file.name}: {e}[/red]")

            progress.advance(task)

    # Summary
    console.print(f"\n[bold green]Ingestion Complete![/bold green]")

    stats = store.get_stats()

    # Stats table
    table = Table(title="Ingestion Statistics")
    table.add_column("Metric", style="cyan")
    table.add_column("Value", style="green")

    table.add_row("Files Processed", str(len(md_files) - len(failed_files)))
    table.add_row("Files Failed", str(len(failed_files)))
    table.add_row("Total Chunks", str(stats['total_chunks']))

    console.print(table)

    # Peripheral distribution
    if stats.get('peripheral_distribution'):
        periph_table = Table(title="Chunks by Peripheral")
        periph_table.add_column("Peripheral")
        periph_table.add_column("Count")

        for periph, count in sorted(
            stats['peripheral_distribution'].items(),
            key=lambda x: x[1],
            reverse=True
        )[:10]:
            periph_table.add_row(periph, str(count))

        console.print(periph_table)

    if failed_files:
        console.print("\n[yellow]Failed Files:[/yellow]")
        for name, error in failed_files:
            console.print(f"  - {name}: {error}")

def main():
    parser = argparse.ArgumentParser(description="Ingest STM32 documentation")
    parser.add_argument(
        "--source-dir", "-s",
        type=Path,
        default=Path(__file__).parent.parent,  # Project root
        help="Source directory with markdown files"
    )
    parser.add_argument(
        "--clear", "-c",
        action="store_true",
        help="Clear existing data before ingestion"
    )
    parser.add_argument(
        "--verbose", "-v",
        action="store_true",
        help="Verbose output"
    )

    args = parser.parse_args()

    if not args.source_dir.exists():
        console.print(f"[red]Source directory not found: {args.source_dir}[/red]")
        sys.exit(1)

    ingest_documents(
        source_dir=args.source_dir,
        clear_existing=args.clear,
        verbose=args.verbose
    )

if __name__ == "__main__":
    main()
```

## Also Create: scripts/test_retrieval.py

A simple script to test search after ingestion:

```python
#!/usr/bin/env python3
"""Test retrieval quality."""

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent))

from storage.chroma_store import STM32ChromaStore, Peripheral
from mcp_server.config import settings

def main():
    store = STM32ChromaStore(
        persist_dir=settings.CHROMA_DB_PATH,
        collection_name=settings.COLLECTION_NAME
    )

    test_queries = [
        ("UART configuration 115200 baud", None),
        ("GPIO output mode", Peripheral.GPIO),
        ("DMA circular buffer", Peripheral.DMA),
        ("ADC continuous conversion", Peripheral.ADC),
        ("Timer PWM generation", Peripheral.TIM),
    ]

    for query, peripheral in test_queries:
        print(f"\n{'='*60}")
        print(f"Query: {query}")
        if peripheral:
            print(f"Filter: {peripheral.value}")
        print(f"{'='*60}")

        results = store.search(
            query=query,
            n_results=3,
            peripheral=peripheral
        )

        for i, r in enumerate(results, 1):
            print(f"\n[{i}] Score: {r['score']:.3f}")
            print(f"    Source: {r['metadata'].get('source_file', 'unknown')}")
            print(f"    Preview: {r['content'][:150]}...")

if __name__ == "__main__":
    main()
```

## Success Criteria

- Script runs without errors
- Progress bar shows ingestion progress
- Stats table displays after completion
- Test retrieval returns relevant results
```

---

## Phase 3: MCP Server Development

### Agent 5: MCP Server Core (Opus)

**Dependencies:** Agent 3 (storage layer complete)

**Model:** Opus

**Description:** Creates the main MCP server with FastMCP framework.

**Full Prompt:**

```
You are implementing the core MCP server for STM32 documentation retrieval. This server will expose tools and resources that Claude Code agents can use to search and retrieve STM32 documentation.

## Context

- Project at /mnt/c/Users/creat/Claude/stm32-agents/
- Storage layer exists in storage/chroma_store.py
- Configuration in mcp-server/config.py

## Your Task

Create the main MCP server using the FastMCP Python framework.

### 1. Create mcp-server/server.py

```python
"""
STM32 Documentation MCP Server

Provides semantic search over STM32 documentation via MCP protocol.
"""

from pathlib import Path
import sys

# Add project root to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from mcp.server.fastmcp import FastMCP
from storage.chroma_store import STM32ChromaStore, Peripheral, DocType
from mcp_server.config import settings

# Initialize FastMCP server
mcp = FastMCP(
    name="stm32-docs",
    version="1.0.0",
    description="STM32 documentation search and retrieval"
)

# Initialize storage (lazy load)
_store: STM32ChromaStore | None = None

def get_store() -> STM32ChromaStore:
    """Get or initialize the ChromaDB store."""
    global _store
    if _store is None:
        _store = STM32ChromaStore(
            persist_dir=settings.CHROMA_DB_PATH,
            collection_name=settings.COLLECTION_NAME,
            embedding_model=settings.EMBEDDING_MODEL
        )
    return _store


# ============================================================================
# TOOLS
# ============================================================================

@mcp.tool()
def search_stm32_docs(
    query: str,
    num_results: int = 5,
    peripheral: str = "",
    require_code: bool = False
) -> str:
    """
    Search STM32 documentation using semantic search.

    Args:
        query: Natural language query about STM32 development
        num_results: Number of results to return (1-20, default: 5)
        peripheral: Filter by peripheral (GPIO, UART, SPI, I2C, ADC, TIM, DMA, etc.)
        require_code: Only return results with code examples

    Returns:
        Relevant documentation snippets with sources and metadata

    Examples:
        - search_stm32_docs("How to configure UART for 115200 baud")
        - search_stm32_docs("DMA configuration", peripheral="DMA")
        - search_stm32_docs("GPIO toggle example", require_code=True)
    """
    store = get_store()

    # Parse peripheral filter
    periph_filter = None
    if peripheral:
        try:
            periph_filter = Peripheral(peripheral.upper())
        except ValueError:
            pass  # Invalid peripheral, ignore filter

    # Clamp results
    num_results = max(1, min(num_results, 20))

    # Search
    results = store.search(
        query=query,
        n_results=num_results,
        peripheral=periph_filter,
        require_code=require_code
    )

    if not results:
        return f"No documentation found for query: {query}"

    # Format output
    output = []
    for i, r in enumerate(results, 1):
        meta = r['metadata']
        output.append(f"## Result {i} (relevance: {r['score']:.2f})")
        output.append(f"**Source**: {meta.get('source_file', 'Unknown')}")

        if meta.get('peripheral'):
            output.append(f"**Peripheral**: {meta['peripheral']}")
        if meta.get('section_path'):
            output.append(f"**Section**: {meta['section_path']}")

        output.append("")
        output.append(r['content'])
        output.append("")
        output.append("---")
        output.append("")

    return "\n".join(output)


@mcp.tool()
def get_peripheral_docs(
    peripheral: str,
    topic: str = "",
    include_code: bool = True
) -> str:
    """
    Get documentation for a specific STM32 peripheral.

    Args:
        peripheral: The peripheral name (GPIO, UART, SPI, I2C, ADC, TIM, DMA, RCC, NVIC, etc.)
        topic: Optional specific topic within the peripheral (e.g., "interrupt", "configuration")
        include_code: Include code examples in results

    Returns:
        Comprehensive documentation for the peripheral

    Examples:
        - get_peripheral_docs("UART")
        - get_peripheral_docs("GPIO", topic="interrupt")
        - get_peripheral_docs("DMA", topic="circular mode")
    """
    store = get_store()

    try:
        periph = Peripheral(peripheral.upper())
    except ValueError:
        return f"Unknown peripheral: {peripheral}. Valid options: {', '.join(p.value for p in Peripheral)}"

    query = f"{peripheral} {topic}".strip() if topic else f"{peripheral} overview configuration"

    results = store.search_by_peripheral(periph, query, n_results=10)

    if not results:
        return f"No documentation found for peripheral: {peripheral}"

    # Group by section
    output = [f"# {peripheral} Documentation\n"]

    for r in results:
        meta = r['metadata']
        section = meta.get('section_title', 'General')

        output.append(f"## {section}")
        output.append(f"*Source: {meta.get('source_file', 'Unknown')}*\n")
        output.append(r['content'])
        output.append("\n---\n")

    return "\n".join(output)


@mcp.tool()
def get_code_examples(
    topic: str,
    peripheral: str = "",
    num_examples: int = 3
) -> str:
    """
    Get code examples for an STM32 topic.

    Args:
        topic: The topic to find code examples for (e.g., "UART DMA receive", "GPIO toggle")
        peripheral: Optional peripheral filter
        num_examples: Number of examples to return (1-10, default: 3)

    Returns:
        Code examples with context and explanations

    Examples:
        - get_code_examples("UART transmit")
        - get_code_examples("PWM configuration", peripheral="TIM")
        - get_code_examples("ADC continuous mode")
    """
    store = get_store()

    periph_filter = None
    if peripheral:
        try:
            periph_filter = Peripheral(peripheral.upper())
        except ValueError:
            pass

    num_examples = max(1, min(num_examples, 10))

    results = store.get_code_examples(
        topic=topic,
        peripheral=periph_filter,
        n_results=num_examples
    )

    if not results:
        return f"No code examples found for: {topic}"

    output = [f"# Code Examples: {topic}\n"]

    for i, r in enumerate(results, 1):
        meta = r['metadata']
        output.append(f"## Example {i}")
        output.append(f"*Source: {meta.get('source_file', 'Unknown')}*")
        if meta.get('peripheral'):
            output.append(f"*Peripheral: {meta['peripheral']}*")
        output.append("")
        output.append(r['content'])
        output.append("\n---\n")

    return "\n".join(output)


@mcp.tool()
def get_register_info(register_name: str) -> str:
    """
    Get information about a specific STM32 register.

    Args:
        register_name: The register name (e.g., "GPIOx_MODER", "USART_CR1", "RCC_AHB1ENR")

    Returns:
        Register documentation including bit fields and configuration options

    Examples:
        - get_register_info("GPIOx_MODER")
        - get_register_info("TIMx_CR1")
        - get_register_info("RCC_CFGR")
    """
    store = get_store()

    results = store.get_register_info(register_name, n_results=3)

    if not results:
        return f"No register information found for: {register_name}"

    output = [f"# Register: {register_name}\n"]

    for r in results:
        meta = r['metadata']
        output.append(f"*Source: {meta.get('source_file', 'Unknown')}*\n")
        output.append(r['content'])
        output.append("\n---\n")

    return "\n".join(output)


@mcp.tool()
def list_peripherals() -> str:
    """
    List all available peripherals and their documentation coverage.

    Returns:
        List of peripherals with chunk counts
    """
    store = get_store()
    stats = store.get_stats()

    output = ["# Available STM32 Peripherals\n"]

    dist = stats.get('peripheral_distribution', {})
    for periph, count in sorted(dist.items(), key=lambda x: x[1], reverse=True):
        if periph and periph != "GENERAL":
            output.append(f"- **{periph}**: {count} documentation chunks")

    output.append(f"\n**Total chunks**: {stats.get('total_chunks', 0)}")

    return "\n".join(output)


# ============================================================================
# RESOURCES
# ============================================================================

@mcp.resource("stm32://stats")
def get_documentation_stats() -> str:
    """Get statistics about the documentation database."""
    store = get_store()
    stats = store.get_stats()

    import json
    return json.dumps(stats, indent=2)


@mcp.resource("stm32://peripherals/{peripheral}")
def get_peripheral_overview(peripheral: str) -> str:
    """Get overview documentation for a specific peripheral."""
    store = get_store()

    try:
        periph = Peripheral(peripheral.upper())
    except ValueError:
        return f"Unknown peripheral: {peripheral}"

    results = store.search_by_peripheral(periph, "overview introduction", n_results=3)

    if not results:
        return f"No overview found for {peripheral}"

    return "\n\n".join(r['content'] for r in results)


# ============================================================================
# PROMPTS
# ============================================================================

@mcp.prompt()
def debug_peripheral(peripheral: str, error: str) -> str:
    """Generate a debugging assistance prompt."""
    return f"""You are debugging an STM32 {peripheral} issue.

Error/Symptom: {error}

Please search the documentation for:
1. Common {peripheral} configuration issues
2. Known errata or limitations
3. Troubleshooting steps

Use the search_stm32_docs tool with relevant queries to find documentation that helps diagnose this issue."""


@mcp.prompt()
def configure_peripheral(peripheral: str, requirements: str) -> str:
    """Generate a peripheral configuration assistance prompt."""
    return f"""You are helping configure the STM32 {peripheral} peripheral.

Requirements: {requirements}

Steps to follow:
1. Use get_peripheral_docs to understand {peripheral} capabilities
2. Use get_code_examples to find similar configurations
3. Provide complete initialization code with explanations

Search for relevant documentation before providing configuration code."""


# ============================================================================
# MAIN
# ============================================================================

def main():
    """Run the MCP server."""
    mcp.run()

if __name__ == "__main__":
    main()
```

### 2. Create scripts/start_server.py

```python
#!/usr/bin/env python3
"""Start the STM32 documentation MCP server."""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from mcp_server.server import main

if __name__ == "__main__":
    main()
```

### 3. Update mcp-server/__init__.py

```python
from .server import mcp, main

__all__ = ["mcp", "main"]
```

## Success Criteria

- Server starts without errors: `python scripts/start_server.py`
- All 5 tools are exposed and callable
- Resources return valid data
- Prompts generate useful templates

## Testing

Create a simple test file to verify tool functionality:

```python
# tests/test_mcp_tools.py
import pytest
from mcp_server.server import search_stm32_docs, get_peripheral_docs, list_peripherals

def test_search_returns_results():
    result = search_stm32_docs("GPIO configuration")
    assert "Result" in result or "No documentation" in result

def test_list_peripherals():
    result = list_peripherals()
    assert "Available" in result
```
```

---

### Agent 6: Search Tools Enhancement (Opus)

**Dependencies:** Agent 5 (core server)

**Model:** Opus

**Description:** Adds advanced search capabilities and specialized tools.

**Full Prompt:**

```
You are enhancing the MCP server with advanced search tools specifically designed for STM32 development workflows.

## Context

- MCP server exists at mcp-server/server.py
- Basic search tools already implemented
- Need to add specialized tools for common development tasks

## Your Task

Create mcp-server/tools/search.py with advanced search capabilities, then integrate into server.py.

### 1. Create mcp-server/tools/search.py

```python
"""
Advanced search tools for STM32 documentation.
"""

from typing import Optional
from storage.chroma_store import STM32ChromaStore, Peripheral, DocType

def search_hal_function(
    store: STM32ChromaStore,
    function_name: str
) -> str:
    """
    Search for documentation about a specific HAL function.

    Args:
        function_name: HAL function name (e.g., "HAL_UART_Transmit", "HAL_GPIO_Init")
    """
    results = store.search(
        query=f"{function_name} function usage parameters return",
        n_results=5,
        require_code=True
    )

    if not results:
        return f"No documentation found for HAL function: {function_name}"

    output = [f"# HAL Function: {function_name}\n"]

    for r in results:
        if function_name.lower() in r['content'].lower():
            output.append(r['content'])
            output.append("\n---\n")

    return "\n".join(output) if len(output) > 1 else f"Function {function_name} not found in indexed documentation."


def search_error_solution(
    store: STM32ChromaStore,
    error_description: str,
    peripheral: Optional[str] = None
) -> str:
    """
    Search for solutions to common STM32 errors.
    """
    periph_filter = None
    if peripheral:
        try:
            periph_filter = Peripheral(peripheral.upper())
        except ValueError:
            pass

    # Search for troubleshooting content
    results = store.search(
        query=f"{error_description} error solution fix troubleshooting",
        n_results=8,
        peripheral=periph_filter
    )

    if not results:
        return "No troubleshooting information found."

    output = ["# Troubleshooting Results\n"]

    for r in results:
        content_lower = r['content'].lower()
        # Prioritize content with error/troubleshooting keywords
        if any(kw in content_lower for kw in ['error', 'issue', 'problem', 'fix', 'solution', 'troubleshoot']):
            output.append(f"## Possible Solution (relevance: {r['score']:.2f})")
            output.append(f"*Source: {r['metadata'].get('source_file', 'Unknown')}*\n")
            output.append(r['content'])
            output.append("\n---\n")

    return "\n".join(output) if len(output) > 1 else "No specific troubleshooting content found."


def search_initialization_sequence(
    store: STM32ChromaStore,
    peripheral: str,
    use_case: str = ""
) -> str:
    """
    Search for complete initialization sequences for a peripheral.
    """
    try:
        periph = Peripheral(peripheral.upper())
    except ValueError:
        return f"Unknown peripheral: {peripheral}"

    query = f"{peripheral} initialization sequence {use_case} HAL_Init configure".strip()

    results = store.search(
        query=query,
        n_results=8,
        peripheral=periph,
        require_code=True
    )

    if not results:
        return f"No initialization examples found for {peripheral}"

    output = [f"# {peripheral} Initialization\n"]

    if use_case:
        output.append(f"*Use case: {use_case}*\n")

    for r in results:
        output.append(f"## From: {r['metadata'].get('source_file', 'Unknown')}")
        output.append(f"*Relevance: {r['score']:.2f}*\n")
        output.append(r['content'])
        output.append("\n---\n")

    return "\n".join(output)


def search_clock_configuration(
    store: STM32ChromaStore,
    target_frequency: str = "",
    clock_source: str = ""
) -> str:
    """
    Search for clock configuration examples.
    """
    query_parts = ["clock configuration RCC"]
    if target_frequency:
        query_parts.append(target_frequency)
    if clock_source:
        query_parts.append(clock_source)

    results = store.search(
        query=" ".join(query_parts),
        n_results=5,
        peripheral=Peripheral.RCC
    )

    if not results:
        return "No clock configuration documentation found."

    output = ["# Clock Configuration\n"]

    for r in results:
        output.append(r['content'])
        output.append("\n---\n")

    return "\n".join(output)


def compare_peripherals(
    store: STM32ChromaStore,
    peripheral1: str,
    peripheral2: str,
    aspect: str = ""
) -> str:
    """
    Get documentation for comparing two peripherals.
    """
    output = [f"# Comparison: {peripheral1} vs {peripheral2}\n"]

    if aspect:
        output.append(f"*Focus: {aspect}*\n")

    for periph in [peripheral1, peripheral2]:
        try:
            p = Peripheral(periph.upper())
        except ValueError:
            output.append(f"\n## {periph}: Unknown peripheral\n")
            continue

        query = f"{periph} {aspect}".strip() if aspect else f"{periph} overview features"
        results = store.search(query=query, n_results=3, peripheral=p)

        output.append(f"\n## {periph}\n")
        for r in results:
            output.append(r['content'][:500] + "...")
            output.append("")

    return "\n".join(output)
```

### 2. Update mcp-server/server.py

Add these new tools to the server:

```python
# Add to imports
from mcp_server.tools.search import (
    search_hal_function,
    search_error_solution,
    search_initialization_sequence,
    search_clock_configuration,
    compare_peripherals
)

# Add new tool definitions

@mcp.tool()
def lookup_hal_function(function_name: str) -> str:
    """
    Look up documentation for a specific HAL function.

    Args:
        function_name: The HAL function name (e.g., HAL_UART_Transmit, HAL_GPIO_Init)

    Returns:
        Function documentation, parameters, and usage examples

    Examples:
        - lookup_hal_function("HAL_UART_Transmit")
        - lookup_hal_function("HAL_SPI_TransmitReceive_DMA")
    """
    return search_hal_function(get_store(), function_name)


@mcp.tool()
def troubleshoot_error(
    error_description: str,
    peripheral: str = ""
) -> str:
    """
    Search for solutions to STM32 errors and issues.

    Args:
        error_description: Description of the error or issue
        peripheral: Optional peripheral to focus the search

    Returns:
        Troubleshooting steps and solutions

    Examples:
        - troubleshoot_error("UART not receiving data")
        - troubleshoot_error("HAL_TIMEOUT error", peripheral="I2C")
        - troubleshoot_error("DMA transfer not completing")
    """
    return search_error_solution(get_store(), error_description, peripheral)


@mcp.tool()
def get_init_sequence(
    peripheral: str,
    use_case: str = ""
) -> str:
    """
    Get complete initialization sequence for a peripheral.

    Args:
        peripheral: The peripheral to initialize (GPIO, UART, SPI, etc.)
        use_case: Specific use case (e.g., "DMA mode", "interrupt driven")

    Returns:
        Complete initialization code with explanations

    Examples:
        - get_init_sequence("UART")
        - get_init_sequence("SPI", use_case="DMA master mode")
        - get_init_sequence("ADC", use_case="continuous conversion")
    """
    return search_initialization_sequence(get_store(), peripheral, use_case)


@mcp.tool()
def get_clock_config(
    target_frequency: str = "",
    clock_source: str = ""
) -> str:
    """
    Get clock configuration documentation.

    Args:
        target_frequency: Target system clock frequency (e.g., "168MHz", "84MHz")
        clock_source: Clock source (HSE, HSI, PLL)

    Returns:
        Clock configuration code and explanations

    Examples:
        - get_clock_config("168MHz", "HSE")
        - get_clock_config("84MHz")
        - get_clock_config(clock_source="PLL")
    """
    return search_clock_configuration(get_store(), target_frequency, clock_source)
```

## Success Criteria

- All new tools callable from MCP
- HAL function lookup returns relevant results
- Troubleshooting finds solution-oriented content
- Init sequence returns complete code examples
```

---

### Agent 7: Resource Handlers (Sonnet)

**Dependencies:** Agent 5 (core server)

**Model:** Sonnet

**Description:** Implements MCP resource handlers for direct document access.

**Full Prompt:**

```
You are implementing MCP resource handlers for direct documentation access.

## Context

- MCP server at mcp-server/server.py
- Need to expose documentation as browsable resources
- Resources allow direct access without search

## Your Task

Create mcp-server/resources/handlers.py:

```python
"""
MCP Resource handlers for STM32 documentation.

Resources provide direct access to documentation content.
"""

from pathlib import Path
from typing import Optional
import json

from storage.chroma_store import STM32ChromaStore, Peripheral
from mcp_server.config import settings


class DocumentationResources:
    """Handler for documentation resources."""

    def __init__(self, store: STM32ChromaStore):
        self.store = store

    def get_peripheral_overview(self, peripheral: str) -> str:
        """Get overview for a peripheral."""
        try:
            periph = Peripheral(peripheral.upper())
        except ValueError:
            return f"Unknown peripheral: {peripheral}"

        results = self.store.search_by_peripheral(
            periph,
            "overview introduction features",
            n_results=5
        )

        if not results:
            return f"No documentation for {peripheral}"

        content = [f"# {peripheral} Overview\n"]
        for r in results:
            content.append(r['content'])
            content.append("\n---\n")

        return "\n".join(content)

    def get_peripheral_registers(self, peripheral: str) -> str:
        """Get register documentation for a peripheral."""
        try:
            periph = Peripheral(peripheral.upper())
        except ValueError:
            return f"Unknown peripheral: {peripheral}"

        results = self.store.search(
            query=f"{peripheral} register map offset bits",
            n_results=10,
            peripheral=periph,
            require_register=True
        )

        if not results:
            return f"No register documentation for {peripheral}"

        content = [f"# {peripheral} Registers\n"]
        for r in results:
            content.append(r['content'])
            content.append("\n---\n")

        return "\n".join(content)

    def get_peripheral_examples(self, peripheral: str) -> str:
        """Get code examples for a peripheral."""
        try:
            periph = Peripheral(peripheral.upper())
        except ValueError:
            return f"Unknown peripheral: {peripheral}"

        results = self.store.get_code_examples(
            topic=f"{peripheral} example",
            peripheral=periph,
            n_results=10
        )

        if not results:
            return f"No code examples for {peripheral}"

        content = [f"# {peripheral} Code Examples\n"]
        for i, r in enumerate(results, 1):
            content.append(f"## Example {i}")
            content.append(f"*Source: {r['metadata'].get('source_file', 'Unknown')}*\n")
            content.append(r['content'])
            content.append("\n---\n")

        return "\n".join(content)

    def get_stats(self) -> str:
        """Get documentation statistics."""
        stats = self.store.get_stats()
        return json.dumps(stats, indent=2)

    def list_sources(self) -> str:
        """List all documentation sources."""
        # Get unique source files
        sample = self.store.collection.get(limit=10000, include=["metadatas"])
        sources = set()
        for meta in sample['metadatas']:
            if 'source_file' in meta:
                sources.add(meta['source_file'])

        output = ["# Documentation Sources\n"]
        for source in sorted(sources):
            output.append(f"- {source}")

        output.append(f"\n**Total sources**: {len(sources)}")
        return "\n".join(output)
```

### Update mcp-server/server.py with new resources:

```python
# Add to server.py

from mcp_server.resources.handlers import DocumentationResources

# Initialize resource handler
_resources: DocumentationResources | None = None

def get_resources() -> DocumentationResources:
    global _resources
    if _resources is None:
        _resources = DocumentationResources(get_store())
    return _resources


# Add more resources

@mcp.resource("stm32://peripherals")
def list_all_peripherals() -> str:
    """List all documented peripherals."""
    return list_peripherals()


@mcp.resource("stm32://peripherals/{peripheral}/overview")
def peripheral_overview(peripheral: str) -> str:
    """Get peripheral overview documentation."""
    return get_resources().get_peripheral_overview(peripheral)


@mcp.resource("stm32://peripherals/{peripheral}/registers")
def peripheral_registers(peripheral: str) -> str:
    """Get peripheral register documentation."""
    return get_resources().get_peripheral_registers(peripheral)


@mcp.resource("stm32://peripherals/{peripheral}/examples")
def peripheral_examples(peripheral: str) -> str:
    """Get peripheral code examples."""
    return get_resources().get_peripheral_examples(peripheral)


@mcp.resource("stm32://sources")
def list_doc_sources() -> str:
    """List all documentation source files."""
    return get_resources().list_sources()
```

## Success Criteria

- Resources accessible via stm32:// URIs
- Peripheral resources return relevant content
- Stats and sources resources work
```

---

## Phase 4: Integration

### Agent 8: Claude Code Configuration (Opus)

**Dependencies:** Agents 5-7 (MCP server complete)

**Model:** Opus

**Description:** Configures Claude Code to use the MCP server.

**Full Prompt:**

```
You are configuring Claude Code to use the STM32 documentation MCP server.

## Context

- MCP server at /mnt/c/Users/creat/Claude/stm32-agents/mcp-server/server.py
- Server provides tools: search_stm32_docs, get_peripheral_docs, get_code_examples, etc.
- Server provides resources: stm32://peripherals/{name}, stm32://stats, etc.

## Your Task

### 1. Create .claude/mcp.json

This configures Claude Code to connect to the MCP server:

```json
{
  "mcpServers": {
    "stm32-docs": {
      "command": "python",
      "args": [
        "/mnt/c/Users/creat/Claude/stm32-agents/mcp-server/server.py"
      ],
      "env": {
        "STM32_CHROMA_DB_PATH": "/mnt/c/Users/creat/Claude/stm32-agents/data/chroma_db",
        "STM32_COLLECTION_NAME": "stm32_docs",
        "STM32_EMBEDDING_MODEL": "all-MiniLM-L6-v2"
      },
      "description": "STM32 documentation search and retrieval"
    }
  }
}
```

### 2. Create .claude/commands/stm32.md

Slash command for easy access:

```markdown
---
name: stm32
description: Search and retrieve STM32 documentation
---

# STM32 Documentation Command

Use this command to search STM32 documentation.

## Usage

```
/stm32 <query>
```

## Examples

```
/stm32 How to configure UART with DMA
/stm32 GPIO interrupt setup
/stm32 ADC continuous conversion
```

## Implementation

When invoked, use the stm32-docs MCP server tools:

1. For general queries: `mcp__stm32-docs__search_stm32_docs`
2. For peripheral-specific: `mcp__stm32-docs__get_peripheral_docs`
3. For code examples: `mcp__stm32-docs__get_code_examples`

Always search the documentation before providing answers about STM32 development.
```

### 3. Create .claude/commands/stm32-init.md

Command to initialize a peripheral:

```markdown
---
name: stm32-init
description: Get initialization code for an STM32 peripheral
---

# STM32 Peripheral Initialization

Get complete initialization sequence for a peripheral.

## Usage

```
/stm32-init <peripheral> [use-case]
```

## Examples

```
/stm32-init UART
/stm32-init SPI DMA mode
/stm32-init ADC continuous conversion with interrupt
```

## Implementation

Use `mcp__stm32-docs__get_init_sequence` tool with the peripheral and use case.
```

### 4. Update .claude/settings.json

```json
{
  "project_name": "STM32 Multi-Agent Development System",
  "description": "AI-powered development assistance for STM32 microcontrollers",

  "mcp": {
    "servers": ["stm32-docs"]
  },

  "agents": {
    "default": "triage",
    "context_source": "mcp:stm32-docs"
  },

  "documentation": {
    "auto_search": true,
    "max_results": 5,
    "include_code_examples": true
  }
}
```

### 5. Create a startup verification script

scripts/verify_mcp.py:

```python
#!/usr/bin/env python3
"""Verify MCP server is working correctly."""

import subprocess
import json
import sys

def test_mcp_connection():
    """Test that the MCP server responds."""
    print("Testing MCP server connection...")

    # This would normally use MCP client SDK
    # For now, just verify the server can start
    try:
        result = subprocess.run(
            ["python", "-c",
             "from mcp_server.server import mcp; print('Server initialized')"],
            capture_output=True,
            text=True,
            timeout=30,
            cwd="/mnt/c/Users/creat/Claude/stm32-agents"
        )

        if result.returncode == 0:
            print("✓ MCP server initializes correctly")
            return True
        else:
            print(f"✗ Server initialization failed: {result.stderr}")
            return False

    except Exception as e:
        print(f"✗ Error: {e}")
        return False

def verify_config():
    """Verify MCP configuration files."""
    import pathlib

    config_path = pathlib.Path("/mnt/c/Users/creat/Claude/stm32-agents/.claude/mcp.json")

    if not config_path.exists():
        print("✗ mcp.json not found")
        return False

    try:
        config = json.loads(config_path.read_text())
        if "mcpServers" in config and "stm32-docs" in config["mcpServers"]:
            print("✓ MCP configuration valid")
            return True
        else:
            print("✗ Invalid MCP configuration")
            return False
    except json.JSONDecodeError as e:
        print(f"✗ Invalid JSON: {e}")
        return False

if __name__ == "__main__":
    results = [
        verify_config(),
        test_mcp_connection()
    ]

    if all(results):
        print("\n✓ All checks passed!")
        sys.exit(0)
    else:
        print("\n✗ Some checks failed")
        sys.exit(1)
```

## Success Criteria

- mcp.json is valid and Claude Code recognizes the server
- Slash commands work
- MCP tools are accessible as mcp__stm32-docs__*
- Verification script passes
```

---

### Agent 9: Update Existing Agents (Opus)

**Dependencies:** Agent 8 (Claude Code configured)

**Model:** Opus

**Description:** Updates existing STM32 agent files to use MCP tools for documentation retrieval.

**Full Prompt:**

```
You are updating the existing STM32 specialized agents to use the new MCP documentation server.

## Context

- MCP server provides tools: search_stm32_docs, get_peripheral_docs, get_code_examples, lookup_hal_function, troubleshoot_error, get_init_sequence
- Existing agents are in .claude/agents/
- Agents need to be updated to query documentation before responding

## Your Task

Update each agent file to include MCP tool usage instructions.

### 1. Update .claude/agents/triage.md

Add to the agent prompt:

```markdown
## Documentation Retrieval

Before routing queries, gather relevant documentation:

1. Use `mcp__stm32-docs__search_stm32_docs` to find relevant content
2. Include retrieved context when routing to specialist agents
3. For ambiguous queries, search first to determine the best agent

Example workflow:
```
User: "My UART isn't working"

1. Search: mcp__stm32-docs__search_stm32_docs("UART troubleshooting common issues")
2. Analyze results to determine if this is:
   - Configuration issue → peripheral-comm agent
   - HAL function issue → firmware-core agent
   - Interrupt issue → interrupt handler agent
3. Route with context
```
```

### 2. Update .claude/agents/firmware-core.md

Add documentation integration section:

```markdown
## Using Documentation

Always search documentation before providing code:

### For HAL Questions
```
mcp__stm32-docs__lookup_hal_function("HAL_UART_Transmit")
```

### For Configuration
```
mcp__stm32-docs__get_init_sequence("UART", "DMA mode")
```

### For Troubleshooting
```
mcp__stm32-docs__troubleshoot_error("HAL_TIMEOUT", peripheral="UART")
```

### For Code Examples
```
mcp__stm32-docs__get_code_examples("UART interrupt receive")
```

## Response Pattern

1. **Search first**: Query documentation for the user's topic
2. **Cite sources**: Mention which documents informed your answer
3. **Provide code**: Include examples from documentation when available
4. **Explain adaptations**: If modifying example code, explain why
```

### 3. Update .claude/agents/peripheral-comm.md

```markdown
## Documentation Integration

For all peripheral configuration queries:

1. **Get Overview**
   ```
   mcp__stm32-docs__get_peripheral_docs("UART")
   ```

2. **Get Initialization Code**
   ```
   mcp__stm32-docs__get_init_sequence("UART", "interrupt driven")
   ```

3. **Get Register Details**
   ```
   mcp__stm32-docs__get_register_info("USART_CR1")
   ```

4. **Get Examples**
   ```
   mcp__stm32-docs__get_code_examples("UART DMA", peripheral="UART")
   ```

## Required Workflow

ALWAYS search documentation before answering:

1. User asks about UART configuration
2. Search: `search_stm32_docs("UART configuration baud rate")`
3. Get init: `get_init_sequence("UART")`
4. Synthesize answer from documentation + your expertise
5. Cite the source documents used
```

### 4. Update .claude/agents/debug.md

```markdown
## Debugging with Documentation

When debugging issues:

1. **Search for Known Issues**
   ```
   mcp__stm32-docs__troubleshoot_error("HardFault after DMA", peripheral="DMA")
   ```

2. **Check Common Mistakes**
   ```
   mcp__stm32-docs__search_stm32_docs("common DMA mistakes pitfalls")
   ```

3. **Verify Configuration**
   ```
   mcp__stm32-docs__get_init_sequence("DMA")
   ```
   Compare user's code against documented initialization sequence.

4. **Check Register Settings**
   ```
   mcp__stm32-docs__get_register_info("DMA_SxCR")
   ```

## Debug Workflow

1. Understand the symptom from user
2. Search documentation for similar issues
3. Identify likely causes from documentation
4. Guide user through diagnostic steps
5. Reference specific documentation for fixes
```

### 5. Create a template for other agents

.claude/agents/_mcp_template.md:

```markdown
## MCP Documentation Tools

This agent has access to the STM32 documentation server via MCP tools.

### Available Tools

| Tool | Purpose | Example |
|------|---------|---------|
| `search_stm32_docs` | General search | `search_stm32_docs("GPIO interrupt", peripheral="GPIO")` |
| `get_peripheral_docs` | Peripheral documentation | `get_peripheral_docs("UART")` |
| `get_code_examples` | Code examples | `get_code_examples("PWM", peripheral="TIM")` |
| `lookup_hal_function` | HAL function docs | `lookup_hal_function("HAL_TIM_PWM_Start")` |
| `troubleshoot_error` | Error solutions | `troubleshoot_error("timer not firing")` |
| `get_init_sequence` | Init code | `get_init_sequence("SPI", "DMA master")` |
| `get_clock_config` | Clock setup | `get_clock_config("168MHz", "HSE")` |

### Usage Pattern

1. **Understand query** - What is the user asking?
2. **Search docs** - Use appropriate MCP tool to find relevant documentation
3. **Synthesize answer** - Combine documentation with your expertise
4. **Cite sources** - Reference the documents used
5. **Provide code** - Include working examples with explanations

### Always Search First

Before answering any STM32 question, search the documentation. This ensures:
- Accurate register/function information
- Up-to-date HAL patterns
- Known errata and workarounds
- Tested code examples
```

## Success Criteria

- All agents updated with MCP tool instructions
- Agents know how to use each tool
- Workflow includes documentation search as first step
- Template available for future agents
```

---

## Phase 5: Validation

### Agent 10: Testing & Quality (Opus)

**Dependencies:** All previous agents (full system complete)

**Model:** Opus

**Description:** Creates comprehensive tests and validates the entire system.

**Full Prompt:**

```
You are creating comprehensive tests for the STM32 MCP documentation system.

## Context

- Complete system at /mnt/c/Users/creat/Claude/stm32-agents/
- MCP server with tools and resources
- ChromaDB storage with embedded documents
- Integration with Claude Code

## Your Task

### 1. Create tests/test_chunking.py

```python
"""Test document chunking quality."""

import pytest
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).parent.parent))

from pipeline.chunker import STM32Chunker, ChunkingConfig

@pytest.fixture
def chunker():
    return STM32Chunker(ChunkingConfig())

class TestChunking:

    def test_basic_markdown_chunking(self, chunker):
        """Test basic markdown is chunked correctly."""
        content = """
# GPIO Configuration

The GPIO peripheral allows...

## Pin Modes

GPIO pins can be configured...

```c
HAL_GPIO_Init(GPIOA, &gpio);
```
"""
        chunks = chunker.chunk_document(content, "test.md")
        assert len(chunks) >= 1
        assert all(c.token_count > 0 for c in chunks)

    def test_code_blocks_not_split(self, chunker):
        """Code blocks should never be split."""
        content = """
# Example

```c
void very_long_function(void) {
    // Many lines of code
    int a = 1;
    int b = 2;
    int c = 3;
    // ... more code
    for (int i = 0; i < 100; i++) {
        do_something(i);
    }
}
```
"""
        chunks = chunker.chunk_document(content, "test.md")

        for chunk in chunks:
            if "```" in chunk.content:
                # Count code block markers
                opens = chunk.content.count("```c") + chunk.content.count("```")
                closes = chunk.content.count("```") - opens
                # Should have equal opens and closes (or be complete)
                assert chunk.content.count("```") % 2 == 0

    def test_peripheral_detection(self, chunker):
        """Peripheral should be detected from content."""
        content = """
# UART Configuration

Configure the USART peripheral for serial communication.
Set baud rate using USART_BRR register.
"""
        chunks = chunker.chunk_document(content, "uart_guide.md")

        assert len(chunks) >= 1
        assert chunks[0].metadata.peripheral in ["UART", "USART"]

    def test_metadata_extraction(self, chunker):
        """Metadata should be correctly extracted."""
        content = """
# STM32F4 Timer Configuration

## PWM Mode

```c
HAL_TIM_PWM_Start(&htim1, TIM_CHANNEL_1);
```
"""
        chunks = chunker.chunk_document(content, "timer_guide.md")

        assert chunks[0].metadata.source_file == "timer_guide.md"
        assert chunks[0].metadata.has_code == True
        assert "STM32F4" in chunks[0].metadata.stm32_families or len(chunks[0].metadata.stm32_families) == 0
```

### 2. Create tests/test_search.py

```python
"""Test search functionality."""

import pytest
from pathlib import Path
import sys
import tempfile

sys.path.insert(0, str(Path(__file__).parent.parent))

from storage.chroma_store import STM32ChromaStore, Peripheral, DocType
from storage.metadata import ChunkMetadataSchema

@pytest.fixture
def temp_store():
    """Create a temporary store with test data."""
    with tempfile.TemporaryDirectory() as tmpdir:
        store = STM32ChromaStore(Path(tmpdir))

        # Add test chunks
        test_chunks = [
            (
                "gpio_001",
                "Configure GPIO pins for output using HAL_GPIO_Init with GPIO_MODE_OUTPUT_PP",
                ChunkMetadataSchema(
                    source_file="gpio_guide.md",
                    doc_type=DocType.HAL_GUIDE,
                    peripheral=Peripheral.GPIO,
                    has_code=True
                )
            ),
            (
                "uart_001",
                "UART configuration for 115200 baud rate. Use HAL_UART_Init to initialize.",
                ChunkMetadataSchema(
                    source_file="uart_guide.md",
                    doc_type=DocType.HAL_GUIDE,
                    peripheral=Peripheral.UART,
                    has_code=True
                )
            ),
            (
                "dma_001",
                "DMA circular mode configuration for continuous data transfer",
                ChunkMetadataSchema(
                    source_file="dma_guide.md",
                    doc_type=DocType.REFERENCE_MANUAL,
                    peripheral=Peripheral.DMA,
                    has_code=False
                )
            ),
        ]

        store.add_chunks(test_chunks)
        yield store

class TestSearch:

    def test_basic_search(self, temp_store):
        """Basic search returns results."""
        results = temp_store.search("GPIO configuration")
        assert len(results) > 0

    def test_peripheral_filter(self, temp_store):
        """Peripheral filter limits results."""
        results = temp_store.search(
            "configuration",
            peripheral=Peripheral.UART
        )

        for r in results:
            assert r['metadata']['peripheral'] == "UART"

    def test_relevance_ordering(self, temp_store):
        """Results should be ordered by relevance."""
        results = temp_store.search("GPIO output mode", n_results=10)

        if len(results) > 1:
            scores = [r['score'] for r in results]
            assert scores == sorted(scores, reverse=True)

    def test_code_filter(self, temp_store):
        """Code filter returns only chunks with code."""
        results = temp_store.search(
            "configuration",
            require_code=True
        )

        for r in results:
            assert r['metadata']['has_code'] == True

    def test_empty_query(self, temp_store):
        """Empty query should still work."""
        results = temp_store.search("")
        # Should return something or empty list, not error
        assert isinstance(results, list)
```

### 3. Create tests/test_mcp_tools.py

```python
"""Test MCP server tools."""

import pytest
from pathlib import Path
import sys
import tempfile

sys.path.insert(0, str(Path(__file__).parent.parent))

# Mock the store for testing
from unittest.mock import patch, MagicMock

class TestMCPTools:

    @patch('mcp_server.server.get_store')
    def test_search_stm32_docs(self, mock_get_store):
        """Test search tool returns formatted results."""
        mock_store = MagicMock()
        mock_store.search.return_value = [
            {
                'id': 'test_001',
                'content': 'Test content about GPIO',
                'metadata': {'source_file': 'test.md', 'peripheral': 'GPIO'},
                'score': 0.95
            }
        ]
        mock_get_store.return_value = mock_store

        from mcp_server.server import search_stm32_docs

        result = search_stm32_docs("GPIO configuration")

        assert "Result 1" in result
        assert "GPIO" in result
        assert "test.md" in result

    @patch('mcp_server.server.get_store')
    def test_search_no_results(self, mock_get_store):
        """Test search with no results."""
        mock_store = MagicMock()
        mock_store.search.return_value = []
        mock_get_store.return_value = mock_store

        from mcp_server.server import search_stm32_docs

        result = search_stm32_docs("nonexistent topic xyz")

        assert "No documentation found" in result

    @patch('mcp_server.server.get_store')
    def test_list_peripherals(self, mock_get_store):
        """Test peripheral listing."""
        mock_store = MagicMock()
        mock_store.get_stats.return_value = {
            'total_chunks': 100,
            'peripheral_distribution': {
                'GPIO': 30,
                'UART': 25,
                'SPI': 20
            }
        }
        mock_get_store.return_value = mock_store

        from mcp_server.server import list_peripherals

        result = list_peripherals()

        assert "GPIO" in result
        assert "UART" in result
        assert "100" in result
```

### 4. Create tests/test_integration.py

```python
"""Integration tests for the complete system."""

import pytest
from pathlib import Path
import sys
import subprocess
import json

sys.path.insert(0, str(Path(__file__).parent.parent))

PROJECT_ROOT = Path(__file__).parent.parent

class TestIntegration:

    def test_project_structure(self):
        """Verify project structure is complete."""
        required_dirs = [
            "mcp-server",
            "pipeline",
            "storage",
            "scripts",
            "data",
            ".claude"
        ]

        for dir_name in required_dirs:
            assert (PROJECT_ROOT / dir_name).exists(), f"Missing directory: {dir_name}"

    def test_mcp_config_valid(self):
        """Verify MCP configuration is valid JSON."""
        config_path = PROJECT_ROOT / ".claude" / "mcp.json"

        if config_path.exists():
            config = json.loads(config_path.read_text())
            assert "mcpServers" in config
            assert "stm32-docs" in config["mcpServers"]

    def test_server_imports(self):
        """Verify server can be imported."""
        try:
            from mcp_server.server import mcp, search_stm32_docs
            assert mcp is not None
        except ImportError as e:
            pytest.fail(f"Import failed: {e}")

    def test_storage_imports(self):
        """Verify storage can be imported."""
        try:
            from storage.chroma_store import STM32ChromaStore
            from storage.metadata import ChunkMetadataSchema
        except ImportError as e:
            pytest.fail(f"Import failed: {e}")

    def test_pipeline_imports(self):
        """Verify pipeline can be imported."""
        try:
            from pipeline.chunker import STM32Chunker
        except ImportError as e:
            pytest.fail(f"Import failed: {e}")
```

### 5. Create scripts/run_tests.py

```python
#!/usr/bin/env python3
"""Run all tests with coverage report."""

import subprocess
import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).parent.parent

def main():
    """Run pytest with coverage."""
    result = subprocess.run(
        [
            sys.executable, "-m", "pytest",
            str(PROJECT_ROOT / "tests"),
            "-v",
            "--tb=short",
            "-x",  # Stop on first failure
        ],
        cwd=PROJECT_ROOT
    )

    return result.returncode

if __name__ == "__main__":
    sys.exit(main())
```

### 6. Create scripts/validate_system.py

End-to-end validation:

```python
#!/usr/bin/env python3
"""Validate the complete system is working."""

import sys
from pathlib import Path
from rich.console import Console
from rich.table import Table

sys.path.insert(0, str(Path(__file__).parent.parent))

console = Console()

def check_structure():
    """Check project structure."""
    required = [
        "mcp-server/server.py",
        "pipeline/chunker.py",
        "storage/chroma_store.py",
        ".claude/mcp.json"
    ]

    root = Path(__file__).parent.parent
    missing = [f for f in required if not (root / f).exists()]

    return len(missing) == 0, missing

def check_database():
    """Check if documentation is indexed."""
    from storage.chroma_store import STM32ChromaStore
    from mcp_server.config import settings

    try:
        store = STM32ChromaStore(settings.CHROMA_DB_PATH)
        count = store.collection.count()
        return count > 0, f"{count} chunks indexed"
    except Exception as e:
        return False, str(e)

def check_search():
    """Check if search works."""
    from storage.chroma_store import STM32ChromaStore
    from mcp_server.config import settings

    try:
        store = STM32ChromaStore(settings.CHROMA_DB_PATH)
        results = store.search("GPIO configuration", n_results=1)
        return len(results) > 0, f"Search returned {len(results)} results"
    except Exception as e:
        return False, str(e)

def check_mcp_server():
    """Check if MCP server initializes."""
    try:
        from mcp_server.server import mcp
        return True, "Server initialized"
    except Exception as e:
        return False, str(e)

def main():
    console.print("\n[bold blue]STM32 MCP Documentation System Validation[/bold blue]\n")

    checks = [
        ("Project Structure", check_structure),
        ("Database Indexed", check_database),
        ("Search Working", check_search),
        ("MCP Server", check_mcp_server),
    ]

    table = Table()
    table.add_column("Check", style="cyan")
    table.add_column("Status", style="bold")
    table.add_column("Details")

    all_passed = True

    for name, check_fn in checks:
        try:
            passed, details = check_fn()
            status = "[green]PASS[/green]" if passed else "[red]FAIL[/red]"
            if not passed:
                all_passed = False
        except Exception as e:
            status = "[red]ERROR[/red]"
            details = str(e)
            all_passed = False

        table.add_row(name, status, str(details))

    console.print(table)

    if all_passed:
        console.print("\n[bold green]All checks passed![/bold green]")
        return 0
    else:
        console.print("\n[bold red]Some checks failed.[/bold red]")
        return 1

if __name__ == "__main__":
    sys.exit(main())
```

## Success Criteria

- All unit tests pass
- Integration tests verify system completeness
- Validation script confirms working system
- Test coverage > 70%
```

---

### Agent 11: Documentation (Sonnet)

**Dependencies:** Agent 10 (testing complete)

**Model:** Sonnet

**Description:** Creates comprehensive documentation for the system.

**Full Prompt:**

```
You are creating comprehensive documentation for the STM32 MCP documentation system.

## Your Task

Create the following documentation files:

### 1. README.md (project root)

```markdown
# STM32 MCP Documentation Server

An MCP (Model Context Protocol) server that provides semantic search over STM32 microcontroller documentation for use with Claude Code and other AI assistants.

## Features

- **Semantic Search**: Find relevant documentation using natural language queries
- **Peripheral-Specific Search**: Filter results by STM32 peripheral (GPIO, UART, SPI, etc.)
- **Code Examples**: Retrieve working code examples for any topic
- **HAL Function Lookup**: Get documentation for specific HAL library functions
- **Troubleshooting**: Find solutions to common STM32 development issues

## Quick Start

### Prerequisites

- Python 3.11+
- Claude Code CLI

### Installation

```bash
# Clone the repository
cd /path/to/stm32-agents

# Install dependencies
pip install -e .

# Ingest documentation
python scripts/ingest_docs.py --source-dir . --clear

# Verify installation
python scripts/validate_system.py
```

### Usage with Claude Code

The MCP server is automatically configured in `.claude/mcp.json`. Once documentation is ingested, you can:

```bash
# Use slash commands
/stm32 How do I configure UART with DMA?
/stm32-init SPI master mode

# Or ask naturally - agents will search documentation automatically
```

## MCP Tools

| Tool | Description |
|------|-------------|
| `search_stm32_docs` | Semantic search across all documentation |
| `get_peripheral_docs` | Get documentation for a specific peripheral |
| `get_code_examples` | Find code examples for a topic |
| `lookup_hal_function` | Look up HAL function documentation |
| `troubleshoot_error` | Find solutions to errors |
| `get_init_sequence` | Get peripheral initialization code |
| `list_peripherals` | List all documented peripherals |

## Project Structure

```
stm32-agents/
├── mcp-server/          # MCP server implementation
├── pipeline/            # Document processing
├── storage/             # ChromaDB wrapper
├── scripts/             # Utility scripts
├── data/                # Documentation and database
├── tests/               # Test suite
└── .claude/             # Claude Code configuration
```

## Adding Documentation

1. Place markdown files in the project root or `data/raw/`
2. Run ingestion: `python scripts/ingest_docs.py --clear`
3. Verify: `python scripts/test_retrieval.py`

## Development

```bash
# Run tests
python scripts/run_tests.py

# Validate system
python scripts/validate_system.py
```

## License

MIT
```

### 2. docs/USAGE.md

```markdown
# Usage Guide

## Searching Documentation

### General Search

```
mcp__stm32-docs__search_stm32_docs(
    query="UART DMA configuration",
    num_results=5,
    peripheral="UART"
)
```

### Peripheral Documentation

```
mcp__stm32-docs__get_peripheral_docs(
    peripheral="GPIO",
    topic="interrupt"
)
```

### Code Examples

```
mcp__stm32-docs__get_code_examples(
    topic="PWM generation",
    peripheral="TIM"
)
```

## Common Workflows

### 1. Configuring a New Peripheral

1. Get overview: `get_peripheral_docs("UART")`
2. Get init sequence: `get_init_sequence("UART", "interrupt mode")`
3. Get examples: `get_code_examples("UART receive")`

### 2. Debugging an Issue

1. Search for error: `troubleshoot_error("HAL_TIMEOUT")`
2. Check configuration: `get_init_sequence("I2C")`
3. Look up function: `lookup_hal_function("HAL_I2C_Master_Transmit")`

### 3. Understanding a HAL Function

1. Look up function: `lookup_hal_function("HAL_SPI_TransmitReceive_DMA")`
2. Get examples: `get_code_examples("SPI DMA")`
```

### 3. docs/ARCHITECTURE.md

```markdown
# Architecture

## System Overview

```
┌─────────────────────────────────────────────┐
│              Claude Code                     │
├─────────────────────────────────────────────┤
│           MCP Protocol Layer                 │
├─────────────────────────────────────────────┤
│         stm32-docs MCP Server               │
│  ┌─────────┬──────────┬───────────┐         │
│  │  Tools  │ Resources│  Prompts  │         │
│  └─────────┴──────────┴───────────┘         │
├─────────────────────────────────────────────┤
│           ChromaDB Vector Store             │
├─────────────────────────────────────────────┤
│       Document Processing Pipeline          │
└─────────────────────────────────────────────┘
```

## Components

### MCP Server (`mcp-server/`)

- FastMCP-based server
- Exposes tools, resources, and prompts
- Lazy-loaded ChromaDB connection

### Document Pipeline (`pipeline/`)

- Markdown chunking with code block preservation
- Token-aware splitting
- Metadata extraction (peripheral, doc type, etc.)

### Storage (`storage/`)

- ChromaDB wrapper with filtering
- Sentence-transformer embeddings
- Persistent local storage

## Data Flow

1. **Ingestion**: Markdown → Chunks → Embeddings → ChromaDB
2. **Query**: User Query → Embedding → Vector Search → Results
3. **Response**: Results → Formatting → MCP Response → Claude

## Extending

### Adding New Tools

```python
@mcp.tool()
def my_new_tool(param: str) -> str:
    """Tool description."""
    store = get_store()
    # Implementation
    return result
```

### Adding New Resources

```python
@mcp.resource("stm32://my-resource/{id}")
def my_resource(id: str) -> str:
    """Resource description."""
    return content
```
```

## Success Criteria

- README provides quick start
- Usage guide covers common workflows
- Architecture explains system design
- All documentation is accurate and complete
```

---

## Execution Order Summary

| Order | Agent | Model | Depends On | Deliverables |
|-------|-------|-------|------------|--------------|
| 1 | Project Setup | Opus | None | Directory structure, pyproject.toml, config |
| 2 | Chunking Logic | Sonnet | Agent 1 | pipeline/chunker.py, validator |
| 3 | Metadata Schema | Sonnet | Agent 1 | storage/metadata.py, chroma_store.py |
| 4 | Ingestion Script | Haiku | Agents 2, 3 | scripts/ingest_docs.py |
| 5 | MCP Server Core | Opus | Agent 3 | mcp-server/server.py |
| 6 | Search Tools | Opus | Agent 5 | mcp-server/tools/search.py |
| 7 | Resource Handlers | Sonnet | Agent 5 | mcp-server/resources/handlers.py |
| 8 | Claude Code Config | Opus | Agents 5-7 | .claude/mcp.json, commands |
| 9 | Update Agents | Opus | Agent 8 | Updated .claude/agents/*.md |
| 10 | Testing | Opus | All | tests/*, validation scripts |
| 11 | Documentation | Sonnet | Agent 10 | README.md, docs/* |

## Parallel Execution Opportunities

These agents can run in parallel:
- **Agents 2 & 3**: Chunking and Storage (both depend only on Agent 1)
- **Agents 6 & 7**: Search Tools and Resources (both depend on Agent 5)

## Estimated Total Chunks

For 78 markdown files (~160K lines):
- Estimated chunks: 3,000 - 5,000
- Estimated storage: 50-100 MB
- Ingestion time: 5-15 minutes

## After Execution

1. Run ingestion: `python scripts/ingest_docs.py --clear`
2. Validate: `python scripts/validate_system.py`
3. Test: `python scripts/run_tests.py`
4. Use: `/stm32 your question here`
