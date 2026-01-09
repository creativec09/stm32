"""
Document Processing Pipeline for STM32 MCP Documentation Server

This package handles the transformation of raw markdown documentation
into searchable chunks stored in the vector database.

Pipeline stages:
1. Document Loading - Read markdown files from disk
2. Chunking - Split documents into semantic chunks
3. Metadata Extraction - Extract peripheral, doc type, etc.
4. Validation - Ensure chunk quality
5. Embedding - Generate vector embeddings (via ChromaDB)
6. Storage - Persist to ChromaDB

Modules:
- chunker.py: Intelligent markdown chunking with STM32-aware parsing
- validator.py: Chunk quality validation and reporting

Key Classes:
- STM32Chunker: Main chunking class with configurable parameters
- ChunkingConfig: Configuration for chunk sizes and behavior
- Chunk: Data class representing a document chunk
- ChunkMetadata: Metadata associated with each chunk
- ChunkValidator: Validates chunk quality
- ValidationReport: Report from validation

Usage:
    from pipeline.chunker import STM32Chunker, ChunkingConfig
    from pipeline.validator import ChunkValidator

    # Create chunker with config
    config = ChunkingConfig(chunk_size=1000, chunk_overlap=150)
    chunker = STM32Chunker(config)

    # Chunk a document
    chunks = chunker.chunk_document(content, "doc.md")

    # Validate chunks
    validator = ChunkValidator()
    report = validator.generate_report(chunks)
"""

__version__ = "1.0.0"

# Lazy imports to avoid circular dependencies and slow startup
from pipeline.chunker import (
    STM32Chunker,
    ChunkingConfig,
    Chunk,
    ChunkMetadata,
)
from pipeline.validator import ChunkValidator, ValidationReport

__all__ = [
    # Version
    "__version__",
    # Chunker
    "STM32Chunker",
    "ChunkingConfig",
    "Chunk",
    "ChunkMetadata",
    # Validator
    "ChunkValidator",
    "ValidationReport",
]
