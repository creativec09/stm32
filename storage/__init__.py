"""
Storage Layer for STM32 MCP Documentation Server

This package provides the persistence layer using ChromaDB
for vector storage and semantic search, with hybrid BM25+vector retrieval.

Modules:
- chroma_store.py: ChromaDB wrapper with STM32-specific methods
- metadata.py: Metadata schemas and enums
- bm25_index.py: BM25 keyword search index
- hybrid_retriever.py: Hybrid search combining BM25 and vector search

Key Classes:
- STM32ChromaStore: Main storage interface with search methods
- HybridRetriever: Combines BM25 + vector search with RRF fusion
- BM25Index: Keyword-based search index with STM32 tokenizer
- ChunkMetadataSchema: Pydantic model for chunk metadata validation
- Peripheral: Enum of STM32 peripherals (GPIO, UART, SPI, etc.)
- DocType: Enum of document types (reference_manual, datasheet, etc.)
- ContentType: Enum of content types (conceptual, code_example, etc.)

Usage:
    from storage import STM32ChromaStore, HybridRetriever, Peripheral, DocType
    from pathlib import Path

    # Initialize store
    store = STM32ChromaStore(
        persist_dir=Path("./data/chroma_db"),
        collection_name="stm32_docs",
        embedding_model="nomic-ai/nomic-embed-text-v1.5"
    )

    # Hybrid search (BM25 + vector with RRF fusion)
    retriever = HybridRetriever(store)
    results = retriever.search("HAL_GPIO_Init configuration", n_results=5)

    # Or pure vector search
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

__version__ = "1.1.0"

from storage.chroma_store import STM32ChromaStore
from storage.metadata import (
    ChunkMetadataSchema,
    ContentType,
    DocType,
    Peripheral,
)
from storage.bm25_index import BM25Index, STM32Tokenizer, create_bm25_index
from storage.hybrid_retriever import (
    HybridRetriever,
    HybridSearchConfig,
    reciprocal_rank_fusion,
    create_hybrid_retriever,
)

__all__ = [
    # Version
    "__version__",
    # Store
    "STM32ChromaStore",
    # Hybrid Retrieval
    "HybridRetriever",
    "HybridSearchConfig",
    "reciprocal_rank_fusion",
    "create_hybrid_retriever",
    # BM25
    "BM25Index",
    "STM32Tokenizer",
    "create_bm25_index",
    # Metadata
    "ChunkMetadataSchema",
    "Peripheral",
    "DocType",
    "ContentType",
]
