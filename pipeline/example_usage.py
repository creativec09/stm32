#!/usr/bin/env python3
"""
Example usage of the STM32 chunking pipeline.

Demonstrates common use cases and best practices.
"""

from chunker import STM32Chunker, ChunkingConfig, Chunk
from validator import ChunkValidator
from pathlib import Path
import json


def example_1_basic_chunking():
    """Example 1: Basic document chunking"""
    print("\n" + "=" * 80)
    print("EXAMPLE 1: Basic Document Chunking")
    print("=" * 80)

    # Sample STM32 documentation
    sample_doc = '''
# GPIO Peripheral

## Overview

The General Purpose Input/Output (GPIO) peripheral provides configuration
and control of the I/O pins on STM32H7 microcontrollers.

## Configuration Registers

### MODER - Port Mode Register

| Bits | Name | Description |
|------|------|-------------|
| 31:30 | MODER15 | Port x configuration bits for pin 15 |
| 29:28 | MODER14 | Port x configuration bits for pin 14 |

### OTYPER - Output Type Register

Controls the output type (push-pull or open-drain).

## HAL Functions

### Initialization

```c
void GPIO_Example(void) {
    GPIO_InitTypeDef GPIO_InitStruct = {0};

    // Enable clock
    __HAL_RCC_GPIOA_CLK_ENABLE();

    // Configure GPIO pin
    GPIO_InitStruct.Pin = GPIO_PIN_5;
    GPIO_InitStruct.Mode = GPIO_MODE_OUTPUT_PP;
    GPIO_InitStruct.Pull = GPIO_NOPULL;
    GPIO_InitStruct.Speed = GPIO_SPEED_FREQ_LOW;
    HAL_GPIO_Init(GPIOA, &GPIO_InitStruct);
}
```

### Pin Control

Use HAL_GPIO_WritePin() and HAL_GPIO_ReadPin() for pin control.
'''

    # Create chunker with default configuration
    chunker = STM32Chunker()

    # Chunk the document
    chunks = chunker.chunk_document(sample_doc, "stm32h7_gpio.md")

    print(f"\nGenerated {len(chunks)} chunks from the document:\n")

    for i, chunk in enumerate(chunks, 1):
        print(f"Chunk {i} ({chunk.id}):")
        print(f"  Tokens: {chunk.token_count}")
        print(f"  Section: {' > '.join(chunk.metadata.section_path) or '(root)'}")
        print(f"  Peripheral: {chunk.metadata.peripheral}")
        print(f"  Content type: ", end="")

        tags = []
        if chunk.metadata.has_code:
            tags.append("code")
        if chunk.metadata.has_table:
            tags.append("table")
        if chunk.metadata.has_register:
            tags.append("register")
        print(", ".join(tags) if tags else "text")

        print()


def example_2_custom_configuration():
    """Example 2: Custom chunking configuration"""
    print("\n" + "=" * 80)
    print("EXAMPLE 2: Custom Configuration")
    print("=" * 80)

    sample_doc = '''
# DMA Transfer

DMA (Direct Memory Access) enables efficient data transfer on STM32F4 devices.

## Configuration

```c
void DMA_Config(void) {
    DMA_HandleTypeDef hdma;
    hdma.Instance = DMA1_Stream0;
    hdma.Init.Channel = DMA_CHANNEL_0;
    hdma.Init.Direction = DMA_MEMORY_TO_PERIPH;
    HAL_DMA_Init(&hdma);
}
```
'''

    # Custom configuration for code-heavy documentation
    custom_config = ChunkingConfig(
        chunk_size=1200,        # Larger chunks for code
        chunk_overlap=100,      # Less overlap
        min_chunk_size=100,     # Avoid tiny fragments
        max_chunk_size=2500,    # Allow large code blocks
    )

    chunker = STM32Chunker(custom_config)
    chunks = chunker.chunk_document(sample_doc, "dma_example.md")

    print(f"\nConfiguration:")
    print(f"  chunk_size: {custom_config.chunk_size}")
    print(f"  chunk_overlap: {custom_config.chunk_overlap}")
    print(f"  max_chunk_size: {custom_config.max_chunk_size}")
    print(f"\nGenerated {len(chunks)} chunks")


def example_3_validation():
    """Example 3: Validating chunk quality"""
    print("\n" + "=" * 80)
    print("EXAMPLE 3: Chunk Validation")
    print("=" * 80)

    sample_doc = '''
# UART Communication

Complete guide to UART on STM32L4 series.

## Initialization

```c
UART_HandleTypeDef huart1;
huart1.Instance = USART1;
HAL_UART_Init(&huart1);
```

## Transmission

```c
uint8_t data[] = "Hello";
HAL_UART_Transmit(&huart1, data, 5, 1000);
```
'''

    chunker = STM32Chunker()
    chunks = chunker.chunk_document(sample_doc, "uart_guide.md")

    # Validate chunks
    validator = ChunkValidator(min_tokens=50, max_tokens=2000)
    report = validator.generate_report(chunks)

    print(f"\nValidation Results:")
    print(f"  Total chunks: {report.total_chunks}")
    print(f"  Valid: {report.valid_chunks}")
    print(f"  Invalid: {report.invalid_chunks}")
    print(f"  Warnings: {report.warnings_count}")

    if report.issues:
        print("\nIssues detected:")
        for issue in report.issues:
            print(f"\n  Chunk {issue['chunk_index']} ({issue['chunk_id']}):")
            if issue['errors']:
                for error in issue['errors']:
                    print(f"    ❌ {error}")
            if issue['warnings']:
                for warning in issue['warnings']:
                    print(f"    ⚠️  {warning}")


def example_4_metadata_filtering():
    """Example 4: Filtering chunks by metadata"""
    print("\n" + "=" * 80)
    print("EXAMPLE 4: Metadata-Based Filtering")
    print("=" * 80)

    sample_doc = '''
# Multi-Peripheral Guide

## GPIO Section

GPIO for STM32F4 and STM32H7.

```c
HAL_GPIO_WritePin(GPIOA, GPIO_PIN_5, GPIO_PIN_SET);
```

## SPI Section

SPI communication for STM32F4.

```c
HAL_SPI_Transmit(&hspi1, data, 10, 100);
```

## ADC Section

ADC conversion for STM32H7.

| Register | Function |
|----------|----------|
| ADC_CR1  | Control  |
'''

    chunker = STM32Chunker()
    chunks = chunker.chunk_document(sample_doc, "multi_peripheral.md")

    print(f"\nGenerated {len(chunks)} total chunks\n")

    # Filter by peripheral
    gpio_chunks = [c for c in chunks if c.metadata.peripheral == 'GPIO']
    print(f"GPIO chunks: {len(gpio_chunks)}")
    for chunk in gpio_chunks:
        print(f"  - {' > '.join(chunk.metadata.section_path)}")

    # Filter by content type
    code_chunks = [c for c in chunks if c.metadata.has_code]
    print(f"\nChunks with code: {len(code_chunks)}")

    table_chunks = [c for c in chunks if c.metadata.has_table]
    print(f"Chunks with tables: {len(table_chunks)}")

    # Filter by STM32 family
    f4_chunks = [c for c in chunks if 'STM32F4' in c.metadata.stm32_families]
    print(f"STM32F4 specific: {len(f4_chunks)}")

    h7_chunks = [c for c in chunks if 'STM32H7' in c.metadata.stm32_families]
    print(f"STM32H7 specific: {len(h7_chunks)}")


def example_5_export_chunks():
    """Example 5: Exporting chunks to JSON"""
    print("\n" + "=" * 80)
    print("EXAMPLE 5: Exporting Chunks to JSON")
    print("=" * 80)

    sample_doc = '''
# I2C Master Mode

I2C configuration for STM32 microcontrollers.

```c
void I2C_Master_Init(void) {
    I2C_HandleTypeDef hi2c1;
    hi2c1.Instance = I2C1;
    hi2c1.Init.ClockSpeed = 100000;
    HAL_I2C_Init(&hi2c1);
}
```
'''

    chunker = STM32Chunker()
    chunks = chunker.chunk_document(sample_doc, "i2c_master.md")

    # Convert chunks to JSON-serializable format
    chunks_json = []
    for chunk in chunks:
        chunks_json.append({
            'id': chunk.id,
            'content': chunk.content,
            'token_count': chunk.token_count,
            'metadata': {
                'source_file': chunk.metadata.source_file,
                'doc_type': chunk.metadata.doc_type,
                'section_path': chunk.metadata.section_path,
                'peripheral': chunk.metadata.peripheral,
                'has_code': chunk.metadata.has_code,
                'has_table': chunk.metadata.has_table,
                'has_register': chunk.metadata.has_register,
                'chunk_index': chunk.metadata.chunk_index,
                'stm32_families': chunk.metadata.stm32_families,
                'hal_functions': chunk.metadata.hal_functions,
                'registers': chunk.metadata.registers,
            }
        })

    # Pretty print JSON
    print("\nChunks as JSON:")
    print(json.dumps(chunks_json, indent=2)[:500] + "...\n")

    print(f"✓ {len(chunks)} chunks ready for export")


def example_6_batch_processing():
    """Example 6: Processing multiple documents"""
    print("\n" + "=" * 80)
    print("EXAMPLE 6: Batch Processing Multiple Documents")
    print("=" * 80)

    # Simulate multiple documents
    documents = {
        'stm32f4_gpio.md': '# GPIO\n\nGPIO for STM32F4...',
        'stm32h7_uart.md': '# UART\n\nUART for STM32H7...',
        'stm32l4_adc.md': '# ADC\n\nADC for STM32L4...',
    }

    chunker = STM32Chunker()
    validator = ChunkValidator()

    all_chunks = []
    stats = {
        'total_docs': 0,
        'total_chunks': 0,
        'valid_chunks': 0,
        'invalid_chunks': 0,
    }

    print("\nProcessing documents...")

    for filename, content in documents.items():
        # Chunk document
        chunks = chunker.chunk_document(content, filename)

        # Validate
        report = validator.generate_report(chunks)

        # Update statistics
        stats['total_docs'] += 1
        stats['total_chunks'] += report.total_chunks
        stats['valid_chunks'] += report.valid_chunks
        stats['invalid_chunks'] += report.invalid_chunks

        all_chunks.extend(chunks)

        print(f"  ✓ {filename}: {len(chunks)} chunks")

    print(f"\nBatch Statistics:")
    print(f"  Documents processed: {stats['total_docs']}")
    print(f"  Total chunks: {stats['total_chunks']}")
    print(f"  Valid chunks: {stats['valid_chunks']}")
    print(f"  Invalid chunks: {stats['invalid_chunks']}")

    # Analyze by peripheral
    peripherals = {}
    for chunk in all_chunks:
        if chunk.metadata.peripheral:
            peripherals[chunk.metadata.peripheral] = \
                peripherals.get(chunk.metadata.peripheral, 0) + 1

    print(f"\nChunks by peripheral:")
    for peripheral, count in sorted(peripherals.items()):
        print(f"  {peripheral}: {count}")


def main():
    """Run all examples"""
    print("\n" + "=" * 80)
    print("STM32 CHUNKING PIPELINE - USAGE EXAMPLES")
    print("=" * 80)

    try:
        example_1_basic_chunking()
        example_2_custom_configuration()
        example_3_validation()
        example_4_metadata_filtering()
        example_5_export_chunks()
        example_6_batch_processing()

        print("\n" + "=" * 80)
        print("ALL EXAMPLES COMPLETED SUCCESSFULLY")
        print("=" * 80 + "\n")

    except Exception as e:
        print(f"\n❌ Error: {e}\n")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()
