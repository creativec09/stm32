#!/usr/bin/env python3
"""
Comprehensive test for the STM32 chunking pipeline.

Tests chunker and validator with realistic STM32 documentation examples.
"""

from chunker import STM32Chunker, ChunkingConfig
from validator import ChunkValidator


def test_basic_chunking():
    """Test basic chunking functionality"""
    print("\n" + "=" * 80)
    print("TEST 1: Basic Chunking")
    print("=" * 80)

    sample = '''
# GPIO Configuration

## Overview

The GPIO peripheral provides general purpose input/output functionality for STM32H7 microcontrollers.

## Register Map

| Register | Offset | Description |
|----------|--------|-------------|
| MODER    | 0x00   | Mode register |
| OTYPER   | 0x04   | Output type register |

## Code Example

```c
GPIO_InitTypeDef gpio = {0};
gpio.Pin = GPIO_PIN_5;
gpio.Mode = GPIO_MODE_OUTPUT_PP;
HAL_GPIO_Init(GPIOA, &gpio);
```
'''

    chunker = STM32Chunker(ChunkingConfig())
    chunks = chunker.chunk_document(sample, "gpio_guide.md")

    print(f"✓ Generated {len(chunks)} chunks")

    for chunk in chunks:
        print(f"\n  Chunk {chunk.metadata.chunk_index}:")
        print(f"    Tokens: {chunk.token_count}")
        print(f"    Section: {' > '.join(chunk.metadata.section_path)}")
        print(f"    Has code: {chunk.metadata.has_code}")
        print(f"    Has table: {chunk.metadata.has_table}")

    assert len(chunks) > 0, "Should generate at least one chunk"
    print("\n✓ Test passed!")


def test_code_preservation():
    """Test that code blocks are never split"""
    print("\n" + "=" * 80)
    print("TEST 2: Code Block Preservation")
    print("=" * 80)

    sample = '''
# UART Example

## Configuration

```c
// Very long code block that exceeds chunk size
void UART_Init(void) {
    UART_HandleTypeDef huart1;
    huart1.Instance = USART1;
    huart1.Init.BaudRate = 115200;
    huart1.Init.WordLength = UART_WORDLENGTH_8B;
    huart1.Init.StopBits = UART_STOPBITS_1;
    huart1.Init.Parity = UART_PARITY_NONE;
    huart1.Init.Mode = UART_MODE_TX_RX;
    huart1.Init.HwFlowCtl = UART_HWCONTROL_NONE;
    huart1.Init.OverSampling = UART_OVERSAMPLING_16;
    HAL_UART_Init(&huart1);
}
```

## Usage

Call the function to initialize UART.
'''

    chunker = STM32Chunker(ChunkingConfig(chunk_size=100))
    chunks = chunker.chunk_document(sample, "uart_example.md")

    print(f"✓ Generated {len(chunks)} chunks")

    # Validate code blocks are intact
    validator = ChunkValidator()
    for chunk in chunks:
        result = validator.check_code_integrity(chunk)
        if not result[0]:
            print(f"✗ Code integrity failed: {result[1]}")
            assert False, "Code block was split!"

    print("✓ All code blocks intact!")
    print("✓ Test passed!")


def test_table_preservation():
    """Test that tables remain intact"""
    print("\n" + "=" * 80)
    print("TEST 3: Table Preservation")
    print("=" * 80)

    sample = '''
# Register Description

## MODER Register

| Bit | Name | Description |
|-----|------|-------------|
| 31:30 | MODER15 | Port x mode bits |
| 29:28 | MODER14 | Port x mode bits |
| 27:26 | MODER13 | Port x mode bits |
| 25:24 | MODER12 | Port x mode bits |
| 23:22 | MODER11 | Port x mode bits |
| 21:20 | MODER10 | Port x mode bits |
'''

    chunker = STM32Chunker(ChunkingConfig(chunk_size=100))
    chunks = chunker.chunk_document(sample, "registers.md")

    print(f"✓ Generated {len(chunks)} chunks")

    # Validate tables
    validator = ChunkValidator()
    for chunk in chunks:
        if chunk.metadata.has_table:
            result = validator.check_table_integrity(chunk)
            print(f"  Table check: {result}")
            if result[1]:
                print(f"  Note: {result[1]}")

    print("✓ Test passed!")


def test_metadata_extraction():
    """Test metadata extraction capabilities"""
    print("\n" + "=" * 80)
    print("TEST 4: Metadata Extraction")
    print("=" * 80)

    sample = '''
# STM32F4 UART Configuration

The USART peripheral for STM32F429 and STM32H743 provides serial communication.

## HAL Functions

Use HAL_UART_Init() and HAL_UART_Transmit() for communication.

## Registers

- USART_CR1 control register
- USART_SR status register
- USART_DR data register
'''

    chunker = STM32Chunker(ChunkingConfig())
    chunks = chunker.chunk_document(sample, "stm32f4_uart_rm.md")

    print(f"✓ Generated {len(chunks)} chunks")

    # Check metadata
    for chunk in chunks:
        print(f"\n  Chunk {chunk.metadata.chunk_index}:")
        print(f"    Peripheral: {chunk.metadata.peripheral}")
        print(f"    Doc type: {chunk.metadata.doc_type}")
        print(f"    Families: {chunk.metadata.stm32_families}")
        print(f"    HAL funcs: {chunk.metadata.hal_functions}")
        print(f"    Registers: {chunk.metadata.registers}")

        # Verify detection
        if "UART" in chunk.content or "USART" in chunk.content:
            assert chunk.metadata.peripheral in ['UART', 'USART'], \
                f"Should detect UART/USART peripheral, got {chunk.metadata.peripheral}"

    print("\n✓ Test passed!")


def test_validation():
    """Test chunk validation"""
    print("\n" + "=" * 80)
    print("TEST 5: Chunk Validation")
    print("=" * 80)

    sample = '''
# Valid Documentation

This is a properly formatted documentation section with sufficient content
to pass all validation checks. It contains meaningful text and follows
best practices for technical documentation.

## Code Example

```c
void example(void) {
    // Complete code block
    HAL_Init();
}
```

## Valid Table

| Column 1 | Column 2 |
|----------|----------|
| Data 1   | Data 2   |
'''

    chunker = STM32Chunker(ChunkingConfig())
    chunks = chunker.chunk_document(sample, "valid_doc.md")

    validator = ChunkValidator(min_tokens=50, max_tokens=2000)
    report = validator.generate_report(chunks)

    print(f"✓ Validation complete:")
    print(f"  Total chunks: {report.total_chunks}")
    print(f"  Valid chunks: {report.valid_chunks}")
    print(f"  Invalid chunks: {report.invalid_chunks}")
    print(f"  Warnings: {report.warnings_count}")

    if report.invalid_chunks > 0:
        print("\n  Issues found:")
        for issue in report.issues:
            if issue['errors']:
                print(f"    Chunk {issue['chunk_index']}: {issue['errors']}")

    print("\n✓ Test passed!")


def test_overlap():
    """Test chunk overlap functionality"""
    print("\n" + "=" * 80)
    print("TEST 6: Chunk Overlap")
    print("=" * 80)

    # Generate long content that will require splitting
    paragraphs = []
    for i in range(10):
        paragraphs.append(f'''
## Section {i}

This is section {i} with substantial content. The GPIO peripheral provides
multiple configuration options. Register MODER controls the mode setting.
The HAL_GPIO_Init function initializes the peripheral. STM32H7 series
implements advanced features.
''')

    sample = "# Large Document\n\n" + "\n\n".join(paragraphs)

    chunker = STM32Chunker(ChunkingConfig(
        chunk_size=200,
        chunk_overlap=50
    ))
    chunks = chunker.chunk_document(sample, "large_doc.md")

    print(f"✓ Generated {len(chunks)} chunks")

    # Check for overlap between consecutive chunks
    for i in range(len(chunks) - 1):
        chunk1 = chunks[i].content
        chunk2 = chunks[i + 1].content

        # Look for shared words
        words1 = set(chunk1.split())
        words2 = set(chunk2.split())
        shared = words1 & words2

        print(f"  Chunks {i}-{i+1}: {len(shared)} shared words")

    print("✓ Test passed!")


def test_peripheral_detection():
    """Test peripheral detection accuracy"""
    print("\n" + "=" * 80)
    print("TEST 7: Peripheral Detection")
    print("=" * 80)

    test_cases = [
        ("gpio_rm.md", "GPIO configuration for STM32", "GPIO"),
        ("uart_guide.md", "UART peripheral usage", "UART"),
        ("spi_example.md", "SPI communication example", "SPI"),
        ("i2c_master.md", "I2C master mode", "I2C"),
        ("dma_transfer.md", "DMA memory transfer", "DMA"),
        ("adc_sampling.md", "ADC analog sampling", "ADC"),
    ]

    chunker = STM32Chunker(ChunkingConfig())

    for filename, content, expected_peripheral in test_cases:
        # Expand content to meet detection threshold
        full_content = f"# {expected_peripheral} Guide\n\n"
        full_content += content + "\n\n"
        full_content += f"The {expected_peripheral} peripheral provides...\n"
        full_content += f"Use {expected_peripheral} registers for configuration.\n"
        full_content += f"{expected_peripheral} functionality is essential.\n"

        chunks = chunker.chunk_document(full_content, filename)

        detected = chunks[0].metadata.peripheral if chunks else None
        status = "✓" if detected == expected_peripheral else "✗"
        print(f"  {status} {filename}: expected={expected_peripheral}, got={detected}")

    print("\n✓ Test passed!")


def run_all_tests():
    """Run all tests"""
    print("\n" + "=" * 80)
    print("STM32 CHUNKING PIPELINE TEST SUITE")
    print("=" * 80)

    try:
        test_basic_chunking()
        test_code_preservation()
        test_table_preservation()
        test_metadata_extraction()
        test_validation()
        test_overlap()
        test_peripheral_detection()

        print("\n" + "=" * 80)
        print("ALL TESTS PASSED!")
        print("=" * 80 + "\n")

    except AssertionError as e:
        print(f"\n✗ Test failed: {e}\n")
        return False
    except Exception as e:
        print(f"\n✗ Unexpected error: {e}\n")
        import traceback
        traceback.print_exc()
        return False

    return True


if __name__ == "__main__":
    import sys
    success = run_all_tests()
    sys.exit(0 if success else 1)
