"""
Unit tests for the storage layer.

Tests the metadata schema and ChromaDB store functionality.
"""

import tempfile
from pathlib import Path

import pytest

from storage.metadata import (
    ChunkMetadataSchema,
    ContentType,
    DocType,
    Peripheral,
)
from storage.chroma_store import STM32ChromaStore


class TestMetadataSchema:
    """Test metadata schema serialization and validation."""

    def test_schema_creation(self):
        """Test creating a metadata schema."""
        meta = ChunkMetadataSchema(
            source_file="test.md",
            doc_type=DocType.HAL_GUIDE,
            peripheral=Peripheral.GPIO,
            has_code=True,
            section_path=["GPIO", "Configuration"],
            hal_functions=["HAL_GPIO_Init"],
            registers=["GPIO_MODER"]
        )

        assert meta.source_file == "test.md"
        assert meta.doc_type == DocType.HAL_GUIDE
        assert meta.peripheral == Peripheral.GPIO
        assert meta.has_code is True
        assert len(meta.section_path) == 2
        assert len(meta.hal_functions) == 1

    def test_to_chroma_metadata(self):
        """Test conversion to ChromaDB format."""
        meta = ChunkMetadataSchema(
            source_file="test.md",
            doc_type=DocType.REFERENCE_MANUAL,
            peripheral=Peripheral.UART,
            secondary_peripherals=["DMA", "RCC"],
            has_code=True,
            section_path=["UART", "Configuration"],
            hal_functions=["HAL_UART_Init", "HAL_UART_Transmit"],
            registers=["UART_CR1", "UART_BRR"]
        )

        chroma_meta = meta.to_chroma_metadata()

        assert isinstance(chroma_meta, dict)
        assert chroma_meta["source_file"] == "test.md"
        assert chroma_meta["doc_type"] == "reference_manual"
        assert chroma_meta["peripheral"] == "UART"
        assert chroma_meta["secondary_peripherals"] == "DMA,RCC"
        assert chroma_meta["has_code"] is True
        assert chroma_meta["section_path"] == "UART > Configuration"
        assert "HAL_UART_Init" in chroma_meta["hal_functions"]

    def test_from_chroma_metadata(self):
        """Test reconstruction from ChromaDB format."""
        chroma_meta = {
            "source_file": "test.md",
            "doc_type": "hal_guide",
            "peripheral": "SPI",
            "secondary_peripherals": "DMA,GPIO",
            "content_type": "code_example",
            "section_path": "SPI > Examples",
            "section_title": "SPI Initialization",
            "has_code": True,
            "has_table": False,
            "has_register_map": False,
            "has_diagram_ref": False,
            "chunk_index": 5,
            "start_line": 123,
            "stm32_families": "STM32F4,STM32H7",
            "hal_functions": "HAL_SPI_Init,HAL_SPI_Transmit",
            "registers": "SPI_CR1,SPI_DR"
        }

        meta = ChunkMetadataSchema.from_chroma_metadata(chroma_meta)

        assert meta.source_file == "test.md"
        assert meta.doc_type == DocType.HAL_GUIDE
        assert meta.peripheral == Peripheral.SPI
        assert "DMA" in meta.secondary_peripherals
        assert meta.content_type == ContentType.CODE_EXAMPLE
        assert len(meta.section_path) == 2
        assert meta.has_code is True
        assert len(meta.hal_functions) == 2
        assert "SPI_CR1" in meta.registers

    def test_roundtrip_conversion(self):
        """Test that to/from ChromaDB conversion is lossless."""
        original = ChunkMetadataSchema(
            source_file="roundtrip.md",
            doc_type=DocType.APPLICATION_NOTE,
            peripheral=Peripheral.I2C,
            content_type=ContentType.CONFIGURATION,
            has_code=True,
            has_table=True,
            section_path=["I2C", "Master Mode"],
            stm32_families=["STM32F4", "STM32L4"],
            hal_functions=["HAL_I2C_Master_Transmit"],
            registers=["I2C_CR1", "I2C_CR2"]
        )

        # Convert to ChromaDB and back
        chroma_meta = original.to_chroma_metadata()
        reconstructed = ChunkMetadataSchema.from_chroma_metadata(chroma_meta)

        # Verify key fields match
        assert reconstructed.source_file == original.source_file
        assert reconstructed.doc_type == original.doc_type
        assert reconstructed.peripheral == original.peripheral
        assert reconstructed.content_type == original.content_type
        assert reconstructed.has_code == original.has_code
        assert reconstructed.section_path == original.section_path
        assert set(reconstructed.stm32_families) == set(original.stm32_families)


class TestSTM32ChromaStore:
    """Test ChromaDB store operations."""

    @pytest.fixture
    def temp_store(self):
        """Create a temporary store for testing."""
        with tempfile.TemporaryDirectory() as tmpdir:
            store = STM32ChromaStore(Path(tmpdir))
            yield store

    def test_store_initialization(self, temp_store):
        """Test store initialization."""
        assert temp_store.count() == 0
        stats = temp_store.get_stats()
        assert stats["total_chunks"] == 0
        assert stats["collection_name"] == "stm32_docs"

    def test_add_chunks(self, temp_store):
        """Test adding chunks to the store."""
        meta = ChunkMetadataSchema(
            source_file="test.md",
            doc_type=DocType.HAL_GUIDE,
            peripheral=Peripheral.GPIO,
            has_code=True
        )

        chunks = [
            ("test_001", "GPIO configuration example", meta.to_chroma_metadata()),
            ("test_002", "Another GPIO example", meta.to_chroma_metadata())
        ]

        count = temp_store.add_chunks(chunks)
        assert count == 2
        assert temp_store.count() == 2

    def test_search(self, temp_store):
        """Test basic search functionality."""
        # Add test data
        meta = ChunkMetadataSchema(
            source_file="gpio_guide.md",
            doc_type=DocType.HAL_GUIDE,
            peripheral=Peripheral.GPIO,
            has_code=True,
            hal_functions=["HAL_GPIO_Init"]
        )

        chunks = [
            (
                "gpio_001",
                "Configure GPIO pin as output using HAL_GPIO_Init",
                meta.to_chroma_metadata()
            )
        ]
        temp_store.add_chunks(chunks)

        # Search
        results = temp_store.search("GPIO configuration")
        assert len(results) > 0
        assert results[0]["id"] == "gpio_001"
        assert "score" in results[0]

    def test_search_with_filters(self, temp_store):
        """Test search with metadata filters."""
        # Add GPIO chunk
        gpio_meta = ChunkMetadataSchema(
            source_file="gpio.md",
            peripheral=Peripheral.GPIO,
            has_code=True
        )
        temp_store.add_chunks([
            ("gpio_001", "GPIO initialization code", gpio_meta.to_chroma_metadata())
        ])

        # Add UART chunk
        uart_meta = ChunkMetadataSchema(
            source_file="uart.md",
            peripheral=Peripheral.UART,
            has_code=False
        )
        temp_store.add_chunks([
            ("uart_001", "UART configuration guide", uart_meta.to_chroma_metadata())
        ])

        # Filter by peripheral
        gpio_results = temp_store.search("configuration", peripheral=Peripheral.GPIO)
        assert len(gpio_results) == 1
        assert gpio_results[0]["metadata"]["peripheral"] == "GPIO"

        # Filter by code requirement
        code_results = temp_store.search("initialization", require_code=True)
        assert all(r["metadata"]["has_code"] for r in code_results)

    def test_get_by_id(self, temp_store):
        """Test retrieving chunks by ID."""
        meta = ChunkMetadataSchema(source_file="test.md")
        temp_store.add_chunks([
            ("test_123", "Test content", meta.to_chroma_metadata())
        ])

        chunk = temp_store.get_by_id("test_123")
        assert chunk is not None
        assert chunk["id"] == "test_123"
        assert chunk["content"] == "Test content"

        # Test non-existent ID
        missing = temp_store.get_by_id("does_not_exist")
        assert missing is None

    def test_get_by_ids(self, temp_store):
        """Test retrieving multiple chunks by IDs."""
        meta = ChunkMetadataSchema(source_file="test.md")
        temp_store.add_chunks([
            ("test_001", "Content 1", meta.to_chroma_metadata()),
            ("test_002", "Content 2", meta.to_chroma_metadata()),
            ("test_003", "Content 3", meta.to_chroma_metadata())
        ])

        chunks = temp_store.get_by_ids(["test_001", "test_003"])
        assert len(chunks) == 2
        ids = [c["id"] for c in chunks]
        assert "test_001" in ids
        assert "test_003" in ids

    def test_delete_by_source(self, temp_store):
        """Test deleting chunks by source file."""
        meta1 = ChunkMetadataSchema(source_file="doc1.md")
        meta2 = ChunkMetadataSchema(source_file="doc2.md")

        temp_store.add_chunks([
            ("doc1_001", "Content from doc1", meta1.to_chroma_metadata()),
            ("doc1_002", "More content from doc1", meta1.to_chroma_metadata()),
            ("doc2_001", "Content from doc2", meta2.to_chroma_metadata())
        ])

        assert temp_store.count() == 3

        # Delete doc1
        deleted = temp_store.delete_by_source("doc1.md")
        assert deleted == 2
        assert temp_store.count() == 1

    def test_peripheral_distribution(self, temp_store):
        """Test peripheral distribution statistics."""
        gpio_meta = ChunkMetadataSchema(peripheral=Peripheral.GPIO, source_file="test.md")
        uart_meta = ChunkMetadataSchema(peripheral=Peripheral.UART, source_file="test.md")

        temp_store.add_chunks([
            ("gpio_001", "GPIO content", gpio_meta.to_chroma_metadata()),
            ("gpio_002", "More GPIO", gpio_meta.to_chroma_metadata()),
            ("uart_001", "UART content", uart_meta.to_chroma_metadata())
        ])

        dist = temp_store.get_peripheral_distribution()
        assert dist.get("GPIO") == 2
        assert dist.get("UART") == 1

    def test_doc_type_distribution(self, temp_store):
        """Test document type distribution statistics."""
        hal_meta = ChunkMetadataSchema(
            doc_type=DocType.HAL_GUIDE,
            source_file="test.md"
        )
        ref_meta = ChunkMetadataSchema(
            doc_type=DocType.REFERENCE_MANUAL,
            source_file="test.md"
        )

        temp_store.add_chunks([
            ("hal_001", "HAL content", hal_meta.to_chroma_metadata()),
            ("ref_001", "Reference content", ref_meta.to_chroma_metadata()),
            ("ref_002", "More reference", ref_meta.to_chroma_metadata())
        ])

        dist = temp_store.get_doc_type_distribution()
        assert dist.get("hal_guide") == 1
        assert dist.get("reference_manual") == 2

    def test_list_sources(self, temp_store):
        """Test listing source files."""
        meta1 = ChunkMetadataSchema(source_file="doc1.md")
        meta2 = ChunkMetadataSchema(source_file="doc2.md")
        meta3 = ChunkMetadataSchema(source_file="doc3.md")

        temp_store.add_chunks([
            ("doc1_001", "Content", meta1.to_chroma_metadata()),
            ("doc2_001", "Content", meta2.to_chroma_metadata()),
            ("doc3_001", "Content", meta3.to_chroma_metadata())
        ])

        sources = temp_store.list_sources()
        assert len(sources) == 3
        assert "doc1.md" in sources
        assert "doc2.md" in sources
        assert "doc3.md" in sources

    def test_get_code_examples(self, temp_store):
        """Test getting code examples."""
        code_meta = ChunkMetadataSchema(
            source_file="examples.md",
            peripheral=Peripheral.GPIO,
            has_code=True
        )
        text_meta = ChunkMetadataSchema(
            source_file="guide.md",
            peripheral=Peripheral.GPIO,
            has_code=False
        )

        temp_store.add_chunks([
            ("code_001", "GPIO initialization code example", code_meta.to_chroma_metadata()),
            ("text_001", "GPIO overview text", text_meta.to_chroma_metadata())
        ])

        examples = temp_store.get_code_examples(
            topic="initialization",
            peripheral=Peripheral.GPIO
        )

        assert len(examples) > 0
        # All results should have has_code=True
        assert all(r["metadata"]["has_code"] for r in examples)

    def test_get_register_info(self, temp_store):
        """Test getting register information."""
        reg_meta = ChunkMetadataSchema(
            source_file="reference.md",
            has_register_map=True,
            registers=["GPIO_MODER"]
        )
        text_meta = ChunkMetadataSchema(
            source_file="guide.md",
            has_register_map=False
        )

        temp_store.add_chunks([
            ("reg_001", "GPIO_MODER register description", reg_meta.to_chroma_metadata()),
            ("text_001", "General GPIO information", text_meta.to_chroma_metadata())
        ])

        results = temp_store.get_register_info("GPIO_MODER")

        assert len(results) > 0
        # All results should have has_register_map=True
        assert all(r["metadata"]["has_register_map"] for r in results)

    def test_search_hal_function(self, temp_store):
        """Test searching for HAL functions."""
        hal_meta = ChunkMetadataSchema(
            source_file="hal_guide.md",
            doc_type=DocType.HAL_GUIDE,
            hal_functions=["HAL_GPIO_Init"]
        )

        temp_store.add_chunks([
            ("hal_001", "HAL_GPIO_Init function usage", hal_meta.to_chroma_metadata())
        ])

        results = temp_store.search_hal_function("HAL_GPIO_Init")

        assert len(results) > 0
        assert results[0]["metadata"]["doc_type"] == "hal_guide"


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
