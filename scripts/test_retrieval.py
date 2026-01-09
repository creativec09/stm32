#!/usr/bin/env python3
"""Test retrieval quality with sample queries."""

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent))

from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from storage.chroma_store import STM32ChromaStore
from storage.metadata import Peripheral
from mcp_server.config import settings

console = Console()

TEST_QUERIES = [
    # (query, peripheral_filter, description)
    ("UART configuration 115200 baud", None, "UART baud rate setup"),
    ("GPIO output mode push pull", Peripheral.GPIO, "GPIO output config"),
    ("DMA circular buffer configuration", Peripheral.DMA, "DMA circular mode"),
    ("ADC continuous conversion mode", Peripheral.ADC, "ADC continuous"),
    ("Timer PWM generation", Peripheral.TIM, "Timer PWM"),
    ("I2C master transmit receive", Peripheral.I2C, "I2C communication"),
    ("SPI DMA transfer", Peripheral.SPI, "SPI with DMA"),
    ("RCC clock configuration PLL", Peripheral.RCC, "Clock setup"),
    ("NVIC interrupt priority", Peripheral.NVIC, "Interrupt config"),
    ("HAL_UART_Transmit function", None, "HAL function lookup"),
    ("bootloader USART protocol", None, "Bootloader docs"),
    ("low power sleep mode", None, "Power management"),
]


def main():
    console.print(Panel.fit(
        "[bold blue]STM32 Documentation Retrieval Test[/bold blue]"
    ))

    store = STM32ChromaStore(
        persist_dir=settings.CHROMA_DB_PATH,
        collection_name=settings.COLLECTION_NAME
    )

    # Check if data exists
    count = store.count()
    if count == 0:
        console.print("[red]No documents indexed! Run ingest_docs.py first.[/red]")
        return

    console.print(f"Testing against [green]{count}[/green] indexed chunks\n")

    for query, peripheral, description in TEST_QUERIES:
        console.print(f"\n{'='*60}")
        console.print(f"[bold cyan]Query:[/bold cyan] {query}")
        if peripheral:
            console.print(f"[dim]Filter: {peripheral.value}[/dim]")
        console.print(f"{'='*60}")

        results = store.search(
            query=query,
            n_results=3,
            peripheral=peripheral
        )

        if not results:
            console.print("[yellow]No results found[/yellow]")
            continue

        for i, r in enumerate(results, 1):
            console.print(f"\n[green][{i}][/green] Score: {r['score']:.3f}")
            console.print(f"    Source: [dim]{r['metadata'].get('source_file', 'unknown')}[/dim]")
            if r['metadata'].get('peripheral'):
                console.print(f"    Peripheral: {r['metadata']['peripheral']}")

            # Show preview
            content = r['content'][:200].replace('\n', ' ')
            console.print(f"    Preview: {content}...")

    console.print("\n" + "="*60)
    console.print("[bold green]Retrieval test complete![/bold green]")


if __name__ == "__main__":
    main()
