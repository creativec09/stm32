#!/usr/bin/env python3
"""Export chunks to JSON for inspection."""

import sys
import json
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent))

from rich.console import Console
from storage.chroma_store import STM32ChromaStore
from mcp_server.config import settings

console = Console()


def main():
    store = STM32ChromaStore(
        persist_dir=settings.CHROMA_DB_PATH,
        collection_name=settings.COLLECTION_NAME
    )

    # Check if data exists
    count = store.count()
    if count == 0:
        console.print("[red]No documents indexed! Run ingest_docs.py first.[/red]")
        return

    # Get sample chunks
    limit = min(100, count)
    sample = store.collection.get(limit=limit, include=["documents", "metadatas"])

    output = []
    for i in range(len(sample['ids'])):
        content = sample['documents'][i]
        output.append({
            'id': sample['ids'][i],
            'content': content[:500] + "..." if len(content) > 500 else content,
            'content_length': len(content),
            'metadata': sample['metadatas'][i]
        })

    output_path = settings.DATA_DIR / "sample_chunks.json"
    with open(output_path, 'w') as f:
        json.dump(output, f, indent=2)

    console.print(f"[green]Exported {len(output)} chunks to {output_path}[/green]")
    console.print(f"[dim]Total chunks in store: {count}[/dim]")


if __name__ == "__main__":
    main()
