"""
Auto-ingestion module for STM32 MCP server.

This module provides reusable ingestion functionality that can be called
both from the CLI scripts and from the MCP server lifespan during startup.
"""

import logging
from pathlib import Path
from typing import Callable, Optional

from pipeline.chunker import STM32Chunker, ChunkingConfig
from storage.chroma_store import STM32ChromaStore
from storage.metadata import ChunkMetadataSchema, DocType, Peripheral, ContentType

logger = logging.getLogger(__name__)


def convert_chunk_metadata(chunk) -> dict:
    """Convert pipeline Chunk metadata to storage format."""
    # Map chunker doc_type strings to storage enum
    doc_type_mapping = {
        'reference_manual': DocType.REFERENCE_MANUAL,
        'datasheet': DocType.DATASHEET,
        'app_note': DocType.APPLICATION_NOTE,
        'user_guide': DocType.USER_MANUAL,
        'programming_manual': DocType.PROGRAMMING_MANUAL,
        'errata': DocType.ERRATA,
        'hal_guide': DocType.HAL_GUIDE,
        'unknown': DocType.GENERAL,
    }

    doc_type = doc_type_mapping.get(chunk.metadata.doc_type, DocType.GENERAL)

    # Map peripheral string to enum
    peripheral = None
    if chunk.metadata.peripheral:
        try:
            peripheral = Peripheral[chunk.metadata.peripheral.upper()]
        except KeyError:
            peripheral = None

    # Determine content type based on chunk characteristics
    if chunk.metadata.has_register:
        content_type = ContentType.REGISTER_MAP
    elif chunk.metadata.has_code:
        content_type = ContentType.CODE_EXAMPLE
    else:
        content_type = ContentType.CONCEPTUAL

    # Create metadata schema
    meta_schema = ChunkMetadataSchema(
        source_file=chunk.metadata.source_file,
        doc_type=doc_type,
        peripheral=peripheral,
        content_type=content_type,
        section_path=chunk.metadata.section_path,
        section_title=chunk.metadata.section_path[-1] if chunk.metadata.section_path else "",
        has_code=chunk.metadata.has_code,
        has_table=chunk.metadata.has_table,
        has_register_map=chunk.metadata.has_register,
        has_diagram_ref=False,
        chunk_index=chunk.metadata.chunk_index,
        start_line=chunk.metadata.start_line,
        stm32_families=chunk.metadata.stm32_families,
        hal_functions=chunk.metadata.hal_functions,
        registers=chunk.metadata.registers,
    )

    return meta_schema.to_chroma_metadata()


def find_markdown_files(source_dir: Path) -> list[Path]:
    """Find all markdown files in directory."""
    if not source_dir.exists():
        return []
    return sorted(list(source_dir.glob("*.md")))


def run_ingestion(
    source_dir: Path,
    store: STM32ChromaStore,
    chunk_size: int = 1000,
    chunk_overlap: int = 150,
    min_chunk_size: int = 50,
    clear_existing: bool = False,
    progress_callback: Optional[Callable[[str, int, int], None]] = None
) -> dict:
    """
    Run the ingestion process.

    Args:
        source_dir: Directory containing markdown files
        store: ChromaDB store instance
        chunk_size: Target chunk size in tokens
        chunk_overlap: Overlap between chunks in tokens
        min_chunk_size: Minimum chunk size in tokens
        clear_existing: Whether to clear existing data before ingestion
        progress_callback: Optional callback(message, current, total) for progress updates

    Returns:
        Dictionary with ingestion statistics
    """
    # Find markdown files
    md_files = find_markdown_files(source_dir)

    if not md_files:
        logger.warning(f"No markdown files found in {source_dir}")
        return {
            "success": False,
            "error": "No markdown files found",
            "total_files": 0,
            "total_chunks": 0
        }

    logger.info(f"Found {len(md_files)} markdown files to process")

    if progress_callback:
        progress_callback(f"Found {len(md_files)} markdown files", 0, len(md_files))

    # Initialize chunker
    chunker = STM32Chunker(ChunkingConfig(
        chunk_size=chunk_size,
        chunk_overlap=chunk_overlap,
        min_chunk_size=min_chunk_size
    ))

    # Clear if requested
    if clear_existing:
        logger.info("Clearing existing data...")
        store.clear()

    # Process files
    total_chunks = 0
    failed_files = []

    for i, md_file in enumerate(md_files):
        try:
            # Read file
            content = md_file.read_text(encoding='utf-8')

            # Chunk
            chunks = chunker.chunk_document(content, md_file.name)

            # Convert and prepare for storage
            chunk_data = []
            for chunk in chunks:
                meta_dict = convert_chunk_metadata(chunk)
                chunk_data.append((chunk.id, chunk.content, meta_dict))

            # Store
            added = store.add_chunks(chunk_data)
            total_chunks += added

            if progress_callback:
                progress_callback(
                    f"Processed {md_file.name}: {added} chunks",
                    i + 1,
                    len(md_files)
                )

            logger.debug(f"Processed {md_file.name}: {added} chunks")

        except UnicodeDecodeError as e:
            failed_files.append((md_file.name, f"Encoding error: {str(e)[:50]}"))
            logger.error(f"Encoding error in {md_file.name}: {e}")
        except Exception as e:
            failed_files.append((md_file.name, str(e)[:100]))
            logger.error(f"Error processing {md_file.name}: {e}")

    result = {
        "success": True,
        "total_files": len(md_files),
        "total_chunks": total_chunks,
        "failed_files": len(failed_files),
        "failed_file_names": [f[0] for f in failed_files]
    }

    logger.info(
        f"Ingestion complete: {len(md_files)} files, "
        f"{total_chunks} chunks, {len(failed_files)} failures"
    )

    return result


async def run_ingestion_async(
    source_dir: Path,
    store: STM32ChromaStore,
    chunk_size: int = 1000,
    chunk_overlap: int = 150,
    min_chunk_size: int = 50,
    clear_existing: bool = False,
    progress_callback: Optional[Callable[[str, int, int], None]] = None
) -> dict:
    """
    Async wrapper for ingestion process.

    This allows the ingestion to be called from async contexts like the
    MCP server lifespan without blocking.

    Note: The actual ingestion is CPU-bound, so this just wraps the sync
    function. For true async, we'd need to use ProcessPoolExecutor.
    """
    import asyncio

    # Run in thread pool to avoid blocking
    loop = asyncio.get_event_loop()
    return await loop.run_in_executor(
        None,
        lambda: run_ingestion(
            source_dir=source_dir,
            store=store,
            chunk_size=chunk_size,
            chunk_overlap=chunk_overlap,
            min_chunk_size=min_chunk_size,
            clear_existing=clear_existing,
            progress_callback=progress_callback
        )
    )
