#!/usr/bin/env python3
"""
Quick search tool for STM32 documentation from the command line.

Usage:
    stm32-search "UART DMA configuration"
    stm32-search "GPIO toggle" --peripheral GPIO
    stm32-search "HAL_SPI_Transmit" --code-only
    stm32-search "clock configuration" --num 10

Examples:
    stm32-search "how to configure UART"
    stm32-search "DMA circular mode" -p DMA -n 3
    stm32-search "interrupt handler" --code-only
    stm32-search "HAL_GPIO_Init" --json
"""

import sys
import argparse
import json
from pathlib import Path

# Add project root to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from mcp_server.config import settings
from storage.chroma_store import STM32ChromaStore
from storage.metadata import Peripheral

# Try to import rich for pretty output
try:
    from rich.console import Console
    from rich.panel import Panel
    from rich.markdown import Markdown
    from rich.syntax import Syntax
    RICH_AVAILABLE = True
    console = Console()
except ImportError:
    RICH_AVAILABLE = False
    console = None


def format_result_plain(result: dict, index: int) -> str:
    """Format a search result as plain text."""
    meta = result['metadata']
    lines = [
        f"\n{'='*60}",
        f"Result {index} (relevance: {result['score']:.3f})",
        f"{'='*60}",
        f"Source: {meta.get('source_file', 'Unknown')}",
    ]

    if meta.get('peripheral'):
        lines.append(f"Peripheral: {meta['peripheral']}")
    if meta.get('section_title'):
        lines.append(f"Section: {meta['section_title']}")
    if meta.get('has_code'):
        lines.append("[Contains code examples]")

    lines.append("")
    lines.append(result['content'])
    lines.append("")

    return "\n".join(lines)


def format_result_rich(result: dict, index: int) -> None:
    """Format a search result using rich formatting."""
    meta = result['metadata']

    # Build header info
    header = f"[bold]Result {index}[/bold] | Score: [green]{result['score']:.3f}[/green]"
    if meta.get('peripheral'):
        header += f" | [cyan]{meta['peripheral']}[/cyan]"
    if meta.get('has_code'):
        header += " | [yellow]Has Code[/yellow]"

    # Source info
    source = f"[dim]Source: {meta.get('source_file', 'Unknown')}"
    if meta.get('section_title'):
        source += f" > {meta['section_title']}"
    source += "[/dim]"

    console.print(Panel(
        Markdown(result['content']),
        title=header,
        subtitle=source,
        border_style="blue"
    ))


def search(
    query: str,
    num_results: int = 5,
    peripheral: str = None,
    code_only: bool = False,
    output_json: bool = False,
    min_score: float = None
) -> int:
    """Execute search and display results."""

    # Initialize store
    try:
        store = STM32ChromaStore(
            persist_dir=settings.CHROMA_DB_PATH,
            collection_name=settings.COLLECTION_NAME,
            embedding_model=settings.EMBEDDING_MODEL
        )
    except Exception as e:
        if RICH_AVAILABLE:
            console.print(f"[red]Error connecting to database: {e}[/red]")
        else:
            print(f"Error connecting to database: {e}", file=sys.stderr)
        return 1

    # Check for indexed data
    if store.count() == 0:
        if RICH_AVAILABLE:
            console.print("[yellow]No documentation indexed. Run 'stm32-ingest' first.[/yellow]")
        else:
            print("No documentation indexed. Run 'stm32-ingest' first.", file=sys.stderr)
        return 1

    # Parse peripheral filter
    periph_filter = None
    if peripheral:
        try:
            periph_filter = Peripheral(peripheral.upper())
        except ValueError:
            if RICH_AVAILABLE:
                console.print(f"[yellow]Unknown peripheral: {peripheral}. Searching all.[/yellow]")
            else:
                print(f"Warning: Unknown peripheral: {peripheral}. Searching all.", file=sys.stderr)

    # Execute search
    min_relevance = min_score if min_score is not None else settings.MIN_RELEVANCE_SCORE

    results = store.search(
        query=query,
        n_results=num_results,
        peripheral=periph_filter,
        require_code=code_only,
        min_score=min_relevance
    )

    if not results:
        if RICH_AVAILABLE:
            console.print(f"[yellow]No results found for: {query}[/yellow]")
        else:
            print(f"No results found for: {query}")
        return 0

    # Output results
    if output_json:
        # JSON output for programmatic use
        output = {
            "query": query,
            "num_results": len(results),
            "results": [
                {
                    "score": r['score'],
                    "content": r['content'],
                    "metadata": r['metadata']
                }
                for r in results
            ]
        }
        print(json.dumps(output, indent=2))
    elif RICH_AVAILABLE:
        # Rich formatted output
        console.print(f"\n[bold]Search Results for:[/bold] [green]{query}[/green]")
        console.print(f"[dim]Found {len(results)} results[/dim]\n")

        for i, result in enumerate(results, 1):
            format_result_rich(result, i)
            print()
    else:
        # Plain text output
        print(f"\nSearch Results for: {query}")
        print(f"Found {len(results)} results")

        for i, result in enumerate(results, 1):
            print(format_result_plain(result, i))

    return 0


def main():
    parser = argparse.ArgumentParser(
        description="Search STM32 documentation from the command line",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  %(prog)s "UART configuration"
  %(prog)s "GPIO interrupt" -p GPIO
  %(prog)s "DMA example" --code-only -n 3
  %(prog)s "HAL_SPI_Init" --json
        """
    )

    parser.add_argument(
        "query",
        help="Search query (natural language or technical term)"
    )

    parser.add_argument(
        "-n", "--num",
        type=int,
        default=5,
        help="Number of results to return (default: 5)"
    )

    parser.add_argument(
        "-p", "--peripheral",
        type=str,
        default=None,
        help="Filter by peripheral (GPIO, UART, SPI, I2C, ADC, TIM, DMA, etc.)"
    )

    parser.add_argument(
        "-c", "--code-only",
        action="store_true",
        help="Only return results with code examples"
    )

    parser.add_argument(
        "--json",
        action="store_true",
        help="Output results as JSON"
    )

    parser.add_argument(
        "--min-score",
        type=float,
        default=None,
        help="Minimum relevance score (0.0-1.0, default: from config)"
    )

    parser.add_argument(
        "--stats",
        action="store_true",
        help="Show database statistics instead of searching"
    )

    args = parser.parse_args()

    if args.stats:
        # Show stats instead of searching
        try:
            store = STM32ChromaStore(
                persist_dir=settings.CHROMA_DB_PATH,
                collection_name=settings.COLLECTION_NAME,
                embedding_model=settings.EMBEDDING_MODEL
            )
            stats = store.get_stats()
            periph_dist = store.get_peripheral_distribution()

            if args.json:
                print(json.dumps({
                    "stats": stats,
                    "peripheral_distribution": periph_dist
                }, indent=2))
            elif RICH_AVAILABLE:
                console.print(Panel.fit("[bold]STM32 Documentation Database[/bold]"))
                console.print(f"Total chunks: [green]{stats.get('total_chunks', 0)}[/green]")
                console.print(f"Sources: [green]{len(stats.get('sources', []))}[/green]")
                console.print("\n[bold]Chunks by Peripheral:[/bold]")
                for periph, count in sorted(periph_dist.items(), key=lambda x: x[1], reverse=True):
                    if periph:
                        console.print(f"  {periph}: {count}")
            else:
                print(f"Total chunks: {stats.get('total_chunks', 0)}")
                print(f"Sources: {len(stats.get('sources', []))}")
                print("\nChunks by Peripheral:")
                for periph, count in sorted(periph_dist.items(), key=lambda x: x[1], reverse=True):
                    if periph:
                        print(f"  {periph}: {count}")
            return 0
        except Exception as e:
            print(f"Error: {e}", file=sys.stderr)
            return 1

    return search(
        query=args.query,
        num_results=args.num,
        peripheral=args.peripheral,
        code_only=args.code_only,
        output_json=args.json,
        min_score=args.min_score
    )


if __name__ == "__main__":
    sys.exit(main())
