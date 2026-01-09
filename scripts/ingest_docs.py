#!/usr/bin/env python3
"""
Ingest STM32 markdown documentation into ChromaDB.

Usage:
    python scripts/ingest_docs.py [--source-dir PATH] [--clear] [--verbose]
    stm32-ingest [--clear] [--verbose]

Examples:
    stm32-ingest --clear  # Clear and re-ingest all
    stm32-ingest -v       # Verbose output
    python scripts/ingest_docs.py --source-dir /path/to/custom/markdowns
"""

import sys
from pathlib import Path
import argparse
import time
from rich.console import Console
from rich.progress import Progress, SpinnerColumn, TextColumn, BarColumn, TaskProgressColumn, TimeElapsedColumn
from rich.table import Table
from rich.panel import Panel

# Add project root to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from pipeline.chunker import STM32Chunker, ChunkingConfig
from storage.chroma_store import STM32ChromaStore
from storage.metadata import ChunkMetadataSchema, DocType, Peripheral, ContentType
from mcp_server.config import settings

console = Console()


def find_markdown_files(source_dir: Path) -> list[Path]:
    """Find all markdown files in directory."""
    if not source_dir.exists():
        return []

    return sorted(list(source_dir.glob("*.md")))


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
        has_diagram_ref=False,  # Would need to detect this in content
        chunk_index=chunk.metadata.chunk_index,
        start_line=chunk.metadata.start_line,
        stm32_families=chunk.metadata.stm32_families,
        hal_functions=chunk.metadata.hal_functions,
        registers=chunk.metadata.registers,
    )

    return meta_schema.to_chroma_metadata()


def ingest_documents(
    source_dir: Path,
    clear_existing: bool = False,
    verbose: bool = False
) -> dict:
    """Main ingestion function. Returns stats dict."""

    console.print(Panel.fit(
        "[bold blue]STM32 Documentation Ingestion[/bold blue]",
        subtitle=f"Source: {source_dir}"
    ))

    # Find files
    md_files = find_markdown_files(source_dir)
    console.print(f"Found [green]{len(md_files)}[/green] markdown files")

    if not md_files:
        console.print("[red]No markdown files found![/red]")
        return {"error": "No files found"}

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

    # Process files with progress bar
    total_chunks = 0
    failed_files = []
    file_stats = []

    with Progress(
        SpinnerColumn(),
        TextColumn("[progress.description]{task.description}"),
        BarColumn(),
        TaskProgressColumn(),
        TimeElapsedColumn(),
        console=console
    ) as progress:
        task = progress.add_task("Processing files...", total=len(md_files))

        for md_file in md_files:
            try:
                # Read file
                content = md_file.read_text(encoding='utf-8')

                # Chunk
                chunks = chunker.chunk_document(content, md_file.name)

                # Convert and prepare for storage
                chunk_data = []
                for chunk in chunks:
                    # Convert chunk metadata to storage format
                    meta_dict = convert_chunk_metadata(chunk)
                    chunk_data.append((chunk.id, chunk.content, meta_dict))

                # Store
                added = store.add_chunks(chunk_data)
                total_chunks += added

                file_stats.append({
                    "file": md_file.name,
                    "chunks": added,
                    "tokens": sum(c.token_count for c in chunks)
                })

                if verbose:
                    console.print(f"  [dim]{md_file.name}[/dim]: {added} chunks")

            except UnicodeDecodeError as e:
                failed_files.append((md_file.name, f"Encoding error: {str(e)[:50]}"))
                console.print(f"[red]Encoding error in {md_file.name}: {e}[/red]")
            except Exception as e:
                failed_files.append((md_file.name, str(e)[:100]))
                console.print(f"[red]Error processing {md_file.name}: {e}[/red]")

            progress.advance(task)

    # Print summary
    print_summary(store, file_stats, failed_files)

    return {
        "total_files": len(md_files),
        "total_chunks": total_chunks,
        "failed_files": len(failed_files)
    }


def print_summary(store, file_stats, failed_files):
    """Print ingestion summary with rich tables."""

    stats = store.get_stats()

    # Main stats table
    table = Table(title="Ingestion Statistics")
    table.add_column("Metric", style="cyan")
    table.add_column("Value", style="green")

    table.add_row("Files Processed", str(len(file_stats)))
    table.add_row("Files Failed", str(len(failed_files)))
    table.add_row("Total Chunks", str(stats.get('total_chunks', 0)))

    console.print(table)

    # Peripheral distribution
    periph_dist = store.get_peripheral_distribution()
    if periph_dist:
        periph_table = Table(title="Chunks by Peripheral (Top 15)")
        periph_table.add_column("Peripheral")
        periph_table.add_column("Count", justify="right")

        for periph, count in sorted(periph_dist.items(), key=lambda x: x[1], reverse=True)[:15]:
            if periph:
                periph_table.add_row(periph, str(count))

        console.print(periph_table)

    # Doc type distribution
    doc_dist = store.get_doc_type_distribution()
    if doc_dist:
        doc_table = Table(title="Chunks by Document Type")
        doc_table.add_column("Document Type")
        doc_table.add_column("Count", justify="right")

        for doc_type, count in sorted(doc_dist.items(), key=lambda x: x[1], reverse=True):
            doc_table.add_row(doc_type, str(count))

        console.print(doc_table)

    # Top files by chunk count
    if file_stats:
        top_files = sorted(file_stats, key=lambda x: x['chunks'], reverse=True)[:10]
        files_table = Table(title="Top 10 Files by Chunk Count")
        files_table.add_column("File")
        files_table.add_column("Chunks", justify="right")
        files_table.add_column("Tokens", justify="right")

        for f in top_files:
            files_table.add_row(
                f['file'][:50] + "..." if len(f['file']) > 50 else f['file'],
                str(f['chunks']),
                f"{f['tokens']:,}"
            )

        console.print(files_table)

    # Failed files
    if failed_files:
        console.print("\n[yellow]Failed Files:[/yellow]")
        for name, error in failed_files:
            console.print(f"  [red]- {name}[/red]: {error[:100]}")

    console.print(f"\n[bold green]Ingestion Complete![/bold green]")


def main():
    parser = argparse.ArgumentParser(description="Ingest STM32 documentation")
    parser.add_argument(
        "--source-dir", "-s",
        type=Path,
        default=None,
        help="Source directory with markdown files (default: from config)"
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

    source_dir = args.source_dir or settings.RAW_DOCS_DIR

    if not source_dir.exists():
        console.print(f"[red]Source directory not found: {source_dir}[/red]")
        sys.exit(1)

    start_time = time.time()
    result = ingest_documents(
        source_dir=source_dir,
        clear_existing=args.clear,
        verbose=args.verbose
    )
    elapsed = time.time() - start_time

    console.print(f"\n[dim]Completed in {elapsed:.1f} seconds[/dim]")

    if result.get("error"):
        sys.exit(1)


if __name__ == "__main__":
    main()
