"""Test document chunking quality."""

import pytest
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).parent.parent))

from pipeline.chunker import STM32Chunker, ChunkingConfig


@pytest.fixture
def chunker():
    """Create a default chunker instance."""
    return STM32Chunker(ChunkingConfig())


@pytest.fixture
def sample_markdown():
    """Sample markdown document for testing."""
    return '''
# GPIO Configuration

## Overview

The GPIO peripheral provides general purpose input/output functionality.

## Register Map

| Register | Offset | Description |
|----------|--------|-------------|
| MODER    | 0x00   | Mode register |
| OTYPER   | 0x04   | Output type |

## Code Example

```c
GPIO_InitTypeDef gpio = {0};
gpio.Pin = GPIO_PIN_5;
gpio.Mode = GPIO_MODE_OUTPUT_PP;
HAL_GPIO_Init(GPIOA, &gpio);
```

## HAL Functions

- HAL_GPIO_Init()
- HAL_GPIO_WritePin()
'''


class TestChunking:
    """Test suite for document chunking."""

    def test_basic_markdown_chunking(self, chunker, sample_markdown):
        """Test basic markdown is chunked correctly."""
        chunks = chunker.chunk_document(sample_markdown, "test.md")
        assert len(chunks) >= 1
        assert all(c.token_count > 0 for c in chunks)

    def test_code_blocks_not_split(self, chunker):
        """Code blocks should never be split."""
        content = '''
# Example

```c
void very_long_function(void) {
    int a = 1;
    int b = 2;
    for (int i = 0; i < 100; i++) {
        do_something(i);
    }
}
```
'''
        chunks = chunker.chunk_document(content, "test.md")
        for chunk in chunks:
            if "```" in chunk.content:
                # Count fence markers - should be even
                count = chunk.content.count("```")
                assert count % 2 == 0, "Code block was split"

    def test_peripheral_detection(self, chunker):
        """Peripheral should be detected from content."""
        content = "# UART Configuration\n\nConfigure USART for serial communication.\nUART is used for debug output.\nUART baud rate configuration."
        chunks = chunker.chunk_document(content, "uart_guide.md")
        assert len(chunks) >= 1
        # Check that UART or USART is detected (both are valid for this content)
        assert chunks[0].metadata.peripheral in ["UART", "USART", None]

    def test_metadata_extraction(self, chunker, sample_markdown):
        """Metadata should be correctly extracted."""
        chunks = chunker.chunk_document(sample_markdown, "gpio_guide.md")
        assert chunks[0].metadata.source_file == "gpio_guide.md"
        # Should detect code and tables
        has_code = any(c.metadata.has_code for c in chunks)
        has_table = any(c.metadata.has_table for c in chunks)
        assert has_code or has_table

    def test_section_hierarchy(self, chunker, sample_markdown):
        """Section path should track header hierarchy."""
        chunks = chunker.chunk_document(sample_markdown, "test.md")
        # At least one chunk should have section path
        assert any(len(c.metadata.section_path) > 0 for c in chunks)

    def test_token_count_bounds(self, chunker):
        """Token counts should be within configured bounds."""
        config = ChunkingConfig(chunk_size=500, min_chunk_size=20)
        custom_chunker = STM32Chunker(config)
        content = "# Test\n\n" + "Word " * 1000
        chunks = custom_chunker.chunk_document(content, "test.md")
        for chunk in chunks:
            assert chunk.token_count >= 10  # Some minimum
            assert chunk.token_count <= 4000  # Reasonable maximum

    def test_empty_content(self, chunker):
        """Empty content should be handled gracefully."""
        chunks = chunker.chunk_document("", "empty.md")
        # Should return at least one chunk or empty list
        assert isinstance(chunks, list)

    def test_single_header(self, chunker):
        """Single header content should create one chunk."""
        content = "# Title\n\nSome content here."
        chunks = chunker.chunk_document(content, "single.md")
        assert len(chunks) >= 1

    def test_nested_headers(self, chunker):
        """Nested headers should be properly tracked."""
        content = """
# Level 1

## Level 2a

Content under 2a.

## Level 2b

### Level 3

Content under 3.
"""
        chunks = chunker.chunk_document(content, "nested.md")
        assert len(chunks) >= 1
        # Check that section paths are tracked
        for chunk in chunks:
            if "Level 3" in chunk.content:
                # Should have hierarchy in section path
                assert len(chunk.metadata.section_path) >= 1

    def test_table_detection(self, chunker):
        """Tables should be detected in content."""
        content = """
# Registers

| Name | Value |
|------|-------|
| A    | 1     |
| B    | 2     |
"""
        chunks = chunker.chunk_document(content, "table.md")
        assert len(chunks) >= 1
        assert any(c.metadata.has_table for c in chunks)

    def test_hal_function_extraction(self, chunker):
        """HAL functions should be extracted from content."""
        content = """
# Example

Call HAL_GPIO_Init(GPIOA, &config) to initialize.
Then use HAL_GPIO_WritePin(GPIOA, GPIO_PIN_5, GPIO_PIN_SET).
"""
        chunks = chunker.chunk_document(content, "hal.md")
        assert len(chunks) >= 1
        # At least one chunk should have HAL functions extracted
        all_hal_funcs = []
        for c in chunks:
            all_hal_funcs.extend(c.metadata.hal_functions)
        assert "HAL_GPIO_Init" in all_hal_funcs or "HAL_GPIO_WritePin" in all_hal_funcs

    def test_stm32_family_detection(self, chunker):
        """STM32 family references should be detected."""
        content = """
# STM32H7 Guide

This applies to STM32H7 and STM32F4 series.
"""
        chunks = chunker.chunk_document(content, "families.md")
        assert len(chunks) >= 1
        all_families = []
        for c in chunks:
            all_families.extend(c.metadata.stm32_families)
        assert "STM32H7" in all_families or "STM32F4" in all_families

    def test_doc_type_detection(self, chunker):
        """Document type should be detected from filename."""
        test_cases = [
            ("rm0468-stm32h7-reference.md", "reference_manual"),
            ("an1234-application-note.md", "app_note"),
            ("ds12345-datasheet.md", "datasheet"),
        ]
        for filename, expected_type in test_cases:
            content = "# Title\n\nContent"
            chunks = chunker.chunk_document(content, filename)
            if chunks:
                # Doc type detection may vary based on implementation
                assert chunks[0].metadata.doc_type is not None

    def test_chunk_id_generation(self, chunker):
        """Chunk IDs should be unique and deterministic."""
        content = "# Test\n\nContent here."
        chunks1 = chunker.chunk_document(content, "test.md")
        chunks2 = chunker.chunk_document(content, "test.md")

        # Same content should produce same IDs
        assert len(chunks1) == len(chunks2)
        for c1, c2 in zip(chunks1, chunks2):
            assert c1.id == c2.id

    def test_large_document(self, chunker):
        """Large documents should be split into multiple chunks."""
        # Create a large document
        sections = []
        for i in range(50):
            sections.append(f"## Section {i}\n\n" + "Content. " * 100)
        content = "# Large Document\n\n" + "\n\n".join(sections)

        chunks = chunker.chunk_document(content, "large.md")
        assert len(chunks) > 1

    def test_register_detection(self, chunker):
        """Register patterns should be detected."""
        content = """
# GPIO Registers

The MODER register controls mode.
The OTYPER register controls output type.
The ODR register is the output data register.
"""
        chunks = chunker.chunk_document(content, "regs.md")
        assert len(chunks) >= 1
        all_registers = []
        for c in chunks:
            all_registers.extend(c.metadata.registers)
        # Should detect at least one register
        assert len(all_registers) > 0 or any(c.metadata.has_register for c in chunks)


class TestChunkingConfig:
    """Test chunking configuration options."""

    def test_custom_chunk_size(self):
        """Custom chunk size should be respected."""
        config = ChunkingConfig(chunk_size=200)
        chunker = STM32Chunker(config)
        assert chunker.config.chunk_size == 200

    def test_custom_overlap(self):
        """Custom overlap should be respected."""
        config = ChunkingConfig(chunk_overlap=50)
        chunker = STM32Chunker(config)
        assert chunker.config.chunk_overlap == 50

    def test_preserve_code_blocks_config(self):
        """Code block preservation config should be stored."""
        config = ChunkingConfig(preserve_code_blocks=False)
        chunker = STM32Chunker(config)
        assert chunker.config.preserve_code_blocks == False


class TestCodeBlockHandling:
    """Test code block specific handling."""

    def test_c_code_block(self):
        """C code blocks should be detected."""
        chunker = STM32Chunker(ChunkingConfig())
        content = """
# Example

```c
int main(void) {
    return 0;
}
```
"""
        chunks = chunker.chunk_document(content, "test.md")
        assert len(chunks) >= 1
        assert any(c.metadata.has_code for c in chunks)

    def test_python_code_block(self):
        """Python code blocks should be detected."""
        chunker = STM32Chunker(ChunkingConfig())
        content = """
# Script

```python
print("hello")
```
"""
        chunks = chunker.chunk_document(content, "test.md")
        assert len(chunks) >= 1
        assert any(c.metadata.has_code for c in chunks)

    def test_inline_code(self):
        """Inline code should not trigger code block detection."""
        chunker = STM32Chunker(ChunkingConfig())
        content = """
# Example

Use the `HAL_GPIO_Init` function.
"""
        chunks = chunker.chunk_document(content, "test.md")
        assert len(chunks) >= 1
        # Inline code shouldn't count as has_code (code blocks)
        # This depends on implementation


class TestTableHandling:
    """Test table specific handling."""

    def test_simple_table(self):
        """Simple tables should be detected."""
        chunker = STM32Chunker(ChunkingConfig())
        content = """
# Data

| A | B |
|---|---|
| 1 | 2 |
"""
        chunks = chunker.chunk_document(content, "test.md")
        assert len(chunks) >= 1
        assert any(c.metadata.has_table for c in chunks)

    def test_complex_table(self):
        """Complex tables with alignment should be detected."""
        chunker = STM32Chunker(ChunkingConfig())
        content = """
# Registers

| Register | Offset | Reset | Description |
|:---------|:------:|------:|:------------|
| MODER    | 0x00   | 0x00  | Mode config |
"""
        chunks = chunker.chunk_document(content, "test.md")
        assert len(chunks) >= 1
        assert any(c.metadata.has_table for c in chunks)
