"""
Example usage of the STM32 storage layer.

This script demonstrates how to use the storage layer for typical operations.
"""

from pathlib import Path
import tempfile

from storage.chroma_store import STM32ChromaStore
from storage.metadata import (
    ChunkMetadataSchema,
    DocType,
    Peripheral,
    ContentType,
)


def example_basic_usage():
    """Basic usage example."""
    print("=" * 70)
    print("Example 1: Basic Usage")
    print("=" * 70)

    with tempfile.TemporaryDirectory() as tmpdir:
        # Initialize store
        store = STM32ChromaStore(Path(tmpdir))
        print("\n1. Store initialized")

        # Create some example chunks
        chunks = [
            (
                "gpio_001",
                "GPIO Configuration: Use HAL_GPIO_Init to configure GPIO pins. "
                "The GPIO_MODER register controls the pin mode (input, output, etc.).",
                ChunkMetadataSchema(
                    source_file="stm32f4_reference.md",
                    doc_type=DocType.REFERENCE_MANUAL,
                    peripheral=Peripheral.GPIO,
                    has_code=False,
                    has_register_map=True,
                    section_path=["GPIO", "Configuration"],
                    registers=["GPIO_MODER"],
                    hal_functions=["HAL_GPIO_Init"]
                ).to_chroma_metadata()
            ),
            (
                "gpio_002",
                """GPIO Code Example:
```c
GPIO_InitTypeDef GPIO_InitStruct;
GPIO_InitStruct.Pin = GPIO_PIN_5;
GPIO_InitStruct.Mode = GPIO_MODE_OUTPUT_PP;
GPIO_InitStruct.Pull = GPIO_NOPULL;
GPIO_InitStruct.Speed = GPIO_SPEED_FREQ_LOW;
HAL_GPIO_Init(GPIOA, &GPIO_InitStruct);
```""",
                ChunkMetadataSchema(
                    source_file="stm32f4_hal_guide.md",
                    doc_type=DocType.HAL_GUIDE,
                    peripheral=Peripheral.GPIO,
                    content_type=ContentType.CODE_EXAMPLE,
                    has_code=True,
                    section_path=["GPIO", "Examples", "Output Configuration"],
                    hal_functions=["HAL_GPIO_Init"],
                    stm32_families=["STM32F4"]
                ).to_chroma_metadata()
            ),
            (
                "uart_001",
                "UART Configuration: Configure UART using HAL_UART_Init. "
                "Set baud rate, word length, stop bits, and parity in UART_InitTypeDef.",
                ChunkMetadataSchema(
                    source_file="stm32f4_hal_guide.md",
                    doc_type=DocType.HAL_GUIDE,
                    peripheral=Peripheral.UART,
                    has_code=False,
                    section_path=["UART", "Configuration"],
                    hal_functions=["HAL_UART_Init"],
                    stm32_families=["STM32F4"]
                ).to_chroma_metadata()
            )
        ]

        # Add chunks
        count = store.add_chunks(chunks)
        print(f"2. Added {count} chunks")

        # Basic search
        print("\n3. Searching for 'GPIO configuration'...")
        results = store.search("GPIO configuration", n_results=2)
        for i, result in enumerate(results, 1):
            print(f"\n   Result {i} (score: {result['score']:.3f}):")
            print(f"   {result['content'][:80]}...")

        # Filtered search
        print("\n4. Searching for code examples...")
        code_results = store.search("GPIO", require_code=True, n_results=2)
        print(f"   Found {len(code_results)} code examples")


def example_peripheral_queries():
    """Example of peripheral-specific queries."""
    print("\n" + "=" * 70)
    print("Example 2: Peripheral-Specific Queries")
    print("=" * 70)

    with tempfile.TemporaryDirectory() as tmpdir:
        store = STM32ChromaStore(Path(tmpdir))

        # Add documentation for multiple peripherals
        peripherals = [
            (Peripheral.GPIO, "GPIO initialization and configuration"),
            (Peripheral.UART, "UART communication setup"),
            (Peripheral.SPI, "SPI master/slave configuration"),
            (Peripheral.I2C, "I2C bus communication"),
        ]

        chunks = []
        for i, (periph, desc) in enumerate(peripherals):
            chunks.append((
                f"{periph.value.lower()}_{i:03d}",
                f"{periph.value}: {desc}",
                ChunkMetadataSchema(
                    source_file=f"{periph.value.lower()}_guide.md",
                    peripheral=periph,
                    has_code=i % 2 == 0  # Every other chunk has code
                ).to_chroma_metadata()
            ))

        store.add_chunks(chunks)
        print(f"\n1. Added {len(chunks)} chunks for various peripherals")

        # Get all GPIO documentation
        print("\n2. Getting all GPIO documentation...")
        gpio_docs = store.search_by_peripheral(Peripheral.GPIO)
        print(f"   Found {len(gpio_docs)} GPIO chunks")

        # Get peripheral distribution
        print("\n3. Peripheral distribution:")
        dist = store.get_peripheral_distribution()
        for periph, count in sorted(dist.items()):
            print(f"   {periph}: {count} chunks")


def example_code_and_register_search():
    """Example of searching for code and register information."""
    print("\n" + "=" * 70)
    print("Example 3: Code Examples and Register Information")
    print("=" * 70)

    with tempfile.TemporaryDirectory() as tmpdir:
        store = STM32ChromaStore(Path(tmpdir))

        # Add mixed content
        chunks = [
            (
                "code_001",
                "GPIO initialization code with HAL_GPIO_Init function",
                ChunkMetadataSchema(
                    source_file="examples.md",
                    peripheral=Peripheral.GPIO,
                    has_code=True,
                    hal_functions=["HAL_GPIO_Init"]
                ).to_chroma_metadata()
            ),
            (
                "reg_001",
                "GPIO_MODER register controls pin mode. Bits [1:0] for pin 0, [3:2] for pin 1.",
                ChunkMetadataSchema(
                    source_file="reference.md",
                    peripheral=Peripheral.GPIO,
                    has_register_map=True,
                    registers=["GPIO_MODER"]
                ).to_chroma_metadata()
            ),
            (
                "text_001",
                "General GPIO overview and features",
                ChunkMetadataSchema(
                    source_file="overview.md",
                    peripheral=Peripheral.GPIO,
                    has_code=False,
                    has_register_map=False
                ).to_chroma_metadata()
            )
        ]

        store.add_chunks(chunks)
        print(f"\n1. Added {len(chunks)} chunks (code, register, text)")

        # Get code examples
        print("\n2. Finding code examples...")
        examples = store.get_code_examples("GPIO initialization")
        print(f"   Found {len(examples)} code examples")

        # Get register info
        print("\n3. Finding register information...")
        reg_info = store.get_register_info("GPIO_MODER")
        print(f"   Found {len(reg_info)} register docs")

        # Search HAL function
        print("\n4. Searching for HAL function...")
        hal_docs = store.search_hal_function("HAL_GPIO_Init")
        print(f"   Found {len(hal_docs)} HAL function docs")


def example_statistics_and_management():
    """Example of statistics and collection management."""
    print("\n" + "=" * 70)
    print("Example 4: Statistics and Management")
    print("=" * 70)

    with tempfile.TemporaryDirectory() as tmpdir:
        store = STM32ChromaStore(Path(tmpdir))

        # Add some test data
        doc_types = [DocType.HAL_GUIDE, DocType.REFERENCE_MANUAL, DocType.APPLICATION_NOTE]
        peripherals = [Peripheral.GPIO, Peripheral.UART, Peripheral.SPI]

        chunks = []
        idx = 0
        for doc_type in doc_types:
            for peripheral in peripherals:
                chunks.append((
                    f"chunk_{idx:03d}",
                    f"Content about {peripheral.value} from {doc_type.value}",
                    ChunkMetadataSchema(
                        source_file=f"{doc_type.value}_{peripheral.value}.md",
                        doc_type=doc_type,
                        peripheral=peripheral
                    ).to_chroma_metadata()
                ))
                idx += 1

        store.add_chunks(chunks)

        # Get statistics
        print("\n1. Collection statistics:")
        stats = store.get_stats()
        print(f"   Total chunks: {stats['total_chunks']}")
        print(f"   Collection: {stats['collection_name']}")
        print(f"   Model: {stats['embedding_model']}")

        # Peripheral distribution
        print("\n2. Peripheral distribution:")
        periph_dist = store.get_peripheral_distribution()
        for periph, count in sorted(periph_dist.items()):
            print(f"   {periph}: {count} chunks")

        # Document type distribution
        print("\n3. Document type distribution:")
        doc_dist = store.get_doc_type_distribution()
        for doc_type, count in sorted(doc_dist.items()):
            print(f"   {doc_type}: {count} chunks")

        # List sources
        print("\n4. Source files:")
        sources = store.list_sources()
        print(f"   Found {len(sources)} source files")
        for source in sorted(sources)[:5]:  # Show first 5
            print(f"   - {source}")

        # Delete by source
        test_source = sources[0]
        print(f"\n5. Deleting chunks from '{test_source}'...")
        deleted = store.delete_by_source(test_source)
        print(f"   Deleted {deleted} chunks")
        print(f"   Remaining: {store.count()} chunks")


def example_advanced_filtering():
    """Example of advanced filtering combinations."""
    print("\n" + "=" * 70)
    print("Example 5: Advanced Filtering")
    print("=" * 70)

    with tempfile.TemporaryDirectory() as tmpdir:
        store = STM32ChromaStore(Path(tmpdir))

        # Add diverse content
        chunks = [
            (
                "f4_gpio_code",
                "STM32F4 GPIO initialization code example",
                ChunkMetadataSchema(
                    source_file="f4_examples.md",
                    doc_type=DocType.HAL_GUIDE,
                    peripheral=Peripheral.GPIO,
                    has_code=True,
                    stm32_families=["STM32F4"]
                ).to_chroma_metadata()
            ),
            (
                "h7_gpio_code",
                "STM32H7 GPIO initialization code example",
                ChunkMetadataSchema(
                    source_file="h7_examples.md",
                    doc_type=DocType.HAL_GUIDE,
                    peripheral=Peripheral.GPIO,
                    has_code=True,
                    stm32_families=["STM32H7"]
                ).to_chroma_metadata()
            ),
            (
                "gpio_ref",
                "GPIO reference documentation without code",
                ChunkMetadataSchema(
                    source_file="reference.md",
                    doc_type=DocType.REFERENCE_MANUAL,
                    peripheral=Peripheral.GPIO,
                    has_code=False
                ).to_chroma_metadata()
            )
        ]

        store.add_chunks(chunks)

        # Complex query 1: GPIO + HAL Guide + Code
        print("\n1. Search: GPIO + HAL Guide + Code")
        results = store.search(
            query="GPIO initialization",
            peripheral=Peripheral.GPIO,
            doc_type=DocType.HAL_GUIDE,
            require_code=True
        )
        print(f"   Found {len(results)} results")

        # Complex query 2: High quality matches only
        print("\n2. Search: High-quality matches (score >= 0.8)")
        results = store.search(
            query="GPIO setup",
            min_score=0.8,
            n_results=10
        )
        print(f"   Found {len(results)} results with score >= 0.8")


def main():
    """Run all examples."""
    print("\nSTM32 Storage Layer - Usage Examples")
    print("=" * 70)

    try:
        example_basic_usage()
        example_peripheral_queries()
        example_code_and_register_search()
        example_statistics_and_management()
        example_advanced_filtering()

        print("\n" + "=" * 70)
        print("All examples completed successfully!")
        print("=" * 70)

    except Exception as e:
        print(f"\nError running examples: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()
