"""
Storage Layer for STM32 MCP Documentation Server

This package provides the persistence layer using ChromaDB
for vector storage and semantic search.

Modules:
- chroma_store.py: ChromaDB wrapper with STM32-specific methods
- metadata.py: Metadata schemas and enums

Key Classes:
- STM32ChromaStore: Main storage interface with search methods
- ChunkMetadataSchema: Pydantic model for chunk metadata validation
- Peripheral: Enum of STM32 peripherals (GPIO, UART, SPI, etc.)
- DocType: Enum of document types (reference_manual, datasheet, etc.)
- ContentType: Enum of content types (conceptual, code_example, etc.)

Usage:
    from storage import STM32ChromaStore, Peripheral, DocType
    from pathlib import Path

    # Initialize store
    store = STM32ChromaStore(
        persist_dir=Path("./data/chroma_db"),
        collection_name="stm32_docs",
        embedding_model="all-MiniLM-L6-v2"
    )

    # Search documentation
    results = store.search("UART configuration", n_results=5)

    # Search with filters
    results = store.search(
        "DMA transfer",
        peripheral=Peripheral.DMA,
        require_code=True
    )

    # Get statistics
    stats = store.get_stats()
    print(f"Total chunks: {stats['total_chunks']}")
"""

__version__ = "1.0.0"

from storage.chroma_store import STM32ChromaStore
from storage.metadata import (
    ChunkMetadataSchema,
    ContentType,
    DocType,
    Peripheral,
)

__all__ = [
    # Version
    "__version__",
    # Store
    "STM32ChromaStore",
    # Metadata
    "ChunkMetadataSchema",
    "Peripheral",
    "DocType",
    "ContentType",
]
