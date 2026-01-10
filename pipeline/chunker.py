"""
STM32 Document Chunker

Intelligently chunks STM32 technical documentation while preserving:
- Markdown structure (headers, code blocks, tables)
- Register definitions and bit field tables
- Code examples and HAL function references
- Peripheral-specific context

Designed for optimal RAG retrieval with token-aware splitting and overlap.
"""

from dataclasses import dataclass, field
from typing import Optional
import re
import hashlib
import tiktoken
from pathlib import Path


@dataclass
class ChunkMetadata:
    """Metadata for a documentation chunk"""
    source_file: str
    doc_type: str  # reference_manual, app_note, datasheet, user_guide, etc.
    section_path: list[str]  # ["GPIO", "Configuration", "Mode Register"]
    peripheral: Optional[str]  # GPIO, UART, SPI, etc.
    has_code: bool
    has_table: bool
    has_register: bool
    start_line: int
    chunk_index: int
    stm32_families: list[str] = field(default_factory=list)
    hal_functions: list[str] = field(default_factory=list)
    registers: list[str] = field(default_factory=list)


@dataclass
class Chunk:
    """A chunk of documentation with metadata"""
    id: str
    content: str
    token_count: int
    metadata: ChunkMetadata


@dataclass
class ChunkingConfig:
    """Configuration for the chunking process"""
    chunk_size: int = 1000  # Target tokens per chunk
    chunk_overlap: int = 150  # Overlap tokens for context
    min_chunk_size: int = 50  # Minimum viable chunk
    max_chunk_size: int = 2000  # Maximum before forced split
    preserve_code_blocks: bool = True
    preserve_tables: bool = True


class STM32Chunker:
    """
    Intelligent chunker for STM32 technical documentation.

    Handles markdown structure, code blocks, tables, and STM32-specific
    content like register definitions and peripheral sections.
    """

    # STM32 peripherals to detect
    PERIPHERALS = [
        'GPIO', 'UART', 'USART', 'LPUART', 'SPI', 'I2C', 'I3C',
        'ADC', 'DAC', 'TIM', 'LPTIM', 'DMA', 'BDMA', 'MDMA',
        'RCC', 'PWR', 'NVIC', 'EXTI', 'FLASH', 'SDMMC', 'MMC',
        'USB', 'CAN', 'FDCAN', 'ETH', 'LTDC', 'DCMI', 'JPEG',
        'RNG', 'CRYP', 'HASH', 'RTC', 'IWDG', 'WWDG', 'SAI',
        'DFSDM', 'FMC', 'QUADSPI', 'OCTOSPI', 'CRC', 'TSC',
        'AES', 'PKA', 'CORDIC', 'FMAC', 'UCPD', 'VREFBUF'
    ]

    # STM32 family patterns
    FAMILY_PATTERNS = [
        r'STM32[FHLGUWC][0-9]',  # STM32F4, STM32H7, etc.
        r'STM32MP[0-9]',  # STM32MP1
        r'STM32WB[0-9]',  # STM32WB55
        r'STM32WL[0-9]',  # STM32WL55
    ]

    # Document type patterns
    DOC_TYPE_PATTERNS = {
        'reference_manual': [r'reference[\s_-]?manual', r'\bRM\d{4}\b', r'_rm\.md$'],
        'datasheet': [r'datasheet', r'\bDS\d{4,5}\b', r'_ds\.md$'],
        'app_note': [r'application[\s_-]?note', r'\bAN\d{4,5}\b', r'_an\.md$'],
        'user_guide': [r'user[\s_-]?guide', r'user[\s_-]?manual', r'_ug\.md$'],
        'programming_manual': [r'programming[\s_-]?manual', r'\bPM\d{4}\b', r'_pm\.md$'],
        'errata': [r'errata[\s_-]?sheet', r'\bES\d{4}\b', r'_es\.md$'],
        'hal_guide': [r'hal[\s_-]?guide', r'stm32cube', r'hal[\s_-]?description', r'_hal\.md$'],
    }

    def __init__(self, config: ChunkingConfig = None):
        """Initialize the chunker with configuration"""
        self.config = config or ChunkingConfig()
        self.tokenizer = tiktoken.get_encoding("cl100k_base")

    def chunk_document(self, content: str, source_file: str) -> list[Chunk]:
        """
        Main entry point: chunk a markdown document into semantically meaningful pieces.

        Args:
            content: Markdown content to chunk
            source_file: Source filename for metadata

        Returns:
            List of Chunk objects with content and metadata
        """
        # First pass: split by header structure
        sections = self._split_by_headers(content)

        # Second pass: handle oversized sections
        chunks = []
        chunk_index = 0

        for section in sections:
            section_content = section['content'].strip()

            # Skip empty sections
            if not section_content:
                continue

            section_tokens = self._count_tokens(section_content)

            # If section fits in one chunk, use it directly
            if section_tokens <= self.config.max_chunk_size:
                chunk = self._create_chunk(
                    content=section_content,
                    source_file=source_file,
                    section_path=section['path'],
                    start_line=section['start_line'],
                    chunk_index=chunk_index
                )
                chunks.append(chunk)
                chunk_index += 1
            else:
                # Split large section with overlap
                sub_chunks = self._split_large_section(section, self.config.chunk_size)
                for sub_content in sub_chunks:
                    chunk = self._create_chunk(
                        content=sub_content,
                        source_file=source_file,
                        section_path=section['path'],
                        start_line=section['start_line'],
                        chunk_index=chunk_index
                    )
                    chunks.append(chunk)
                    chunk_index += 1

        return chunks

    def _split_by_headers(self, content: str) -> list[dict]:
        """
        Split document by markdown headers while preserving hierarchy.

        Returns list of dicts with:
        - content: section text
        - path: list of header titles leading to this section
        - level: header level (1-6)
        - start_line: line number where section starts
        """
        lines = content.split('\n')
        sections = []
        current_section = []
        header_stack = []  # Track header hierarchy
        start_line = 0

        for i, line in enumerate(lines):
            # Check for markdown header
            header_match = re.match(r'^(#{1,6})\s+(.+)$', line)

            if header_match:
                # Save previous section if it exists
                if current_section:
                    sections.append({
                        'content': '\n'.join(current_section),
                        'path': [h[1] for h in header_stack],
                        'level': header_stack[-1][0] if header_stack else 1,
                        'start_line': start_line
                    })

                # Update header stack
                level = len(header_match.group(1))
                title = header_match.group(2).strip()

                # Pop headers of same or lower level
                while header_stack and header_stack[-1][0] >= level:
                    header_stack.pop()

                # Add new header
                header_stack.append((level, title))

                # Start new section
                current_section = [line]
                start_line = i + 1
            else:
                current_section.append(line)

        # Don't forget the last section
        if current_section:
            sections.append({
                'content': '\n'.join(current_section),
                'path': [h[1] for h in header_stack],
                'level': header_stack[-1][0] if header_stack else 1,
                'start_line': start_line
            })

        return sections

    def _split_large_section(self, section: dict, max_tokens: int) -> list[str]:
        """
        Split a large section into smaller chunks while preserving structure.

        This is the tricky part: we need to split intelligently without
        breaking code blocks, tables, or logical units.
        """
        content = section['content']

        # Extract protected regions (code blocks and tables)
        code_blocks = self._extract_code_blocks(content)
        tables = self._extract_tables(content)

        # Combine and sort protected regions
        protected = []
        for start, end, block_type in code_blocks:
            protected.append((start, end, 'code'))
        for start, end, table_type in tables:
            protected.append((start, end, 'table'))
        protected.sort()

        # Split into paragraphs while respecting protected regions
        chunks = []
        current_chunk = []
        current_tokens = 0

        lines = content.split('\n')
        i = 0

        while i < len(lines):
            # Check if we're at a protected region
            in_protected = False
            protected_content = []

            for start, end, ptype in protected:
                if i >= start and i < end:
                    # Collect entire protected region
                    protected_content = lines[start:end]
                    protected_text = '\n'.join(protected_content)
                    protected_tokens = self._count_tokens(protected_text)

                    # If protected region fits in current chunk, add it
                    if current_tokens + protected_tokens <= max_tokens:
                        current_chunk.extend(protected_content)
                        current_tokens += protected_tokens
                    # If it fits in a new chunk, start new chunk
                    elif protected_tokens <= self.config.max_chunk_size:
                        if current_chunk:
                            chunks.append('\n'.join(current_chunk))
                        current_chunk = protected_content
                        current_tokens = protected_tokens
                    # If it's oversized, make it its own chunk anyway
                    else:
                        if current_chunk:
                            chunks.append('\n'.join(current_chunk))
                        chunks.append(protected_text)
                        current_chunk = []
                        current_tokens = 0

                    i = end
                    in_protected = True
                    break

            if in_protected:
                continue

            # Normal line processing
            line = lines[i]
            line_tokens = self._count_tokens(line)

            # Check if adding this line would overflow
            if current_tokens + line_tokens > max_tokens and current_chunk:
                # Save current chunk with overlap
                chunks.append('\n'.join(current_chunk))

                # Start new chunk with overlap (last few lines)
                overlap_lines = self._get_overlap_lines(current_chunk, self.config.chunk_overlap)
                current_chunk = overlap_lines + [line]
                current_tokens = self._count_tokens('\n'.join(current_chunk))
            else:
                current_chunk.append(line)
                current_tokens += line_tokens

            i += 1

        # Don't forget the last chunk
        if current_chunk:
            chunks.append('\n'.join(current_chunk))

        return chunks

    def _get_overlap_lines(self, lines: list[str], target_tokens: int) -> list[str]:
        """Get the last N lines that fit within target tokens for overlap"""
        overlap = []
        tokens = 0

        for line in reversed(lines):
            line_tokens = self._count_tokens(line)
            if tokens + line_tokens > target_tokens:
                break
            overlap.insert(0, line)
            tokens += line_tokens

        return overlap

    def _extract_code_blocks(self, text: str) -> list[tuple[int, int, str]]:
        """
        Extract code block positions from markdown.

        Returns list of (start_line, end_line, language) tuples.
        """
        lines = text.split('\n')
        code_blocks = []
        in_block = False
        start = 0
        lang = ''

        for i, line in enumerate(lines):
            if line.strip().startswith('```'):
                if not in_block:
                    # Start of code block
                    in_block = True
                    start = i
                    lang = line.strip()[3:].strip()
                else:
                    # End of code block
                    code_blocks.append((start, i + 1, lang))
                    in_block = False

        return code_blocks

    def _extract_tables(self, text: str) -> list[tuple[int, int, str]]:
        """
        Extract markdown table positions.

        Returns list of (start_line, end_line, 'table') tuples.
        """
        lines = text.split('\n')
        tables = []
        in_table = False
        start = 0

        for i, line in enumerate(lines):
            # Detect table by pipe characters
            if '|' in line and line.strip().startswith('|'):
                if not in_table:
                    in_table = True
                    start = i
            else:
                if in_table:
                    # End of table
                    tables.append((start, i, 'table'))
                    in_table = False

        # Don't forget if document ends with a table
        if in_table:
            tables.append((start, len(lines), 'table'))

        return tables

    def _create_chunk(
        self,
        content: str,
        source_file: str,
        section_path: list[str],
        start_line: int,
        chunk_index: int
    ) -> Chunk:
        """Create a Chunk object with full metadata"""
        # Count tokens
        token_count = self._count_tokens(content)

        # Extract metadata
        peripheral = self._detect_peripheral(content, source_file)
        doc_type = self._detect_doc_type(source_file, content)
        stm32_families = self._detect_stm32_families(content)
        hal_functions = self._extract_hal_functions(content)
        registers = self._extract_registers(content)

        # Check for special content types
        has_code = bool(self._extract_code_blocks(content))
        has_table = bool(self._extract_tables(content))
        has_register = bool(registers) or self._has_register_definition(content)

        # Create metadata
        metadata = ChunkMetadata(
            source_file=source_file,
            doc_type=doc_type,
            section_path=section_path,
            peripheral=peripheral,
            has_code=has_code,
            has_table=has_table,
            has_register=has_register,
            start_line=start_line,
            chunk_index=chunk_index,
            stm32_families=stm32_families,
            hal_functions=hal_functions,
            registers=registers
        )

        # Generate unique ID
        chunk_id = self._generate_chunk_id(source_file, chunk_index, content)

        return Chunk(
            id=chunk_id,
            content=content,
            token_count=token_count,
            metadata=metadata
        )

    def _detect_peripheral(self, text: str, filename: str) -> Optional[str]:
        """
        Detect which STM32 peripheral this content is about.

        Checks both filename and content for peripheral keywords.
        """
        text_upper = text.upper()
        filename_upper = filename.upper()

        # Check filename first (more reliable)
        for peripheral in self.PERIPHERALS:
            if peripheral in filename_upper:
                return peripheral

        # Check content (count occurrences)
        peripheral_counts = {}
        for peripheral in self.PERIPHERALS:
            # Use word boundaries to avoid false matches
            pattern = r'\b' + peripheral + r'\b'
            matches = len(re.findall(pattern, text_upper))
            if matches > 0:
                peripheral_counts[peripheral] = matches

        # Return most common peripheral if it appears frequently
        if peripheral_counts:
            max_peripheral = max(peripheral_counts, key=peripheral_counts.get)
            # Require at least 2 mentions to be confident (lowered from 3)
            if peripheral_counts[max_peripheral] >= 2:
                return max_peripheral

        return None

    def _detect_doc_type(self, filename: str, content: str) -> str:
        """
        Detect document type from filename and content.

        Returns: reference_manual, datasheet, app_note, user_guide, etc.
        """
        filename_lower = filename.lower()
        content_lower = content.lower()

        for doc_type, patterns in self.DOC_TYPE_PATTERNS.items():
            for pattern in patterns:
                if re.search(pattern, filename_lower) or re.search(pattern, content_lower[:1000]):
                    return doc_type

        return 'unknown'

    def _detect_stm32_families(self, text: str) -> list[str]:
        """
        Extract STM32 family references from text.

        Returns list like ['STM32F4', 'STM32H7']
        """
        families = set()
        text_upper = text.upper()

        for pattern in self.FAMILY_PATTERNS:
            matches = re.findall(pattern, text_upper)
            families.update(matches)

        return sorted(list(families))

    def _extract_hal_functions(self, text: str) -> list[str]:
        """
        Extract HAL function references from text.

        Looks for HAL_*() patterns.
        """
        # Match HAL function calls
        pattern = r'\bHAL_[A-Z][A-Za-z0-9_]*\('
        matches = re.findall(pattern, text)

        # Remove the trailing parenthesis and deduplicate
        functions = set(m[:-1] for m in matches)

        return sorted(list(functions))

    def _extract_registers(self, text: str) -> list[str]:
        """
        Extract register names from text.

        Looks for common register patterns like MODER, OTYPER, CR1, SR, etc.
        """
        registers = set()

        # Pattern for register names (all caps, optionally with numbers)
        # Common suffixes: R, CR, SR, DR, etc.
        pattern = r'\b[A-Z]{2,}[0-9]?R\b|\b[A-Z]+(?:CR|SR|DR|MR|TR|BR|PR|AR|ER|FR|ISR|ICR|IER|IDR|ODR|BSRR|LCKR|AFRL|AFRH)\b'
        matches = re.findall(pattern, text)

        # Filter out common words that match the pattern
        exclusions = {'OR', 'AND', 'FOR', 'NOT', 'XOR', 'ERROR'}
        for match in matches:
            if match not in exclusions and len(match) <= 10:
                registers.add(match)

        return sorted(list(registers))

    def _has_register_definition(self, text: str) -> bool:
        """
        Check if text contains register bit field definitions.

        Looks for patterns like:
        - Bit 0: ENABLE
        - [31:16] RESERVED
        """
        patterns = [
            r'Bit\s+\d+:',  # Bit 0:
            r'\[\d+:\d+\]',  # [31:16]
            r'Bits?\s+\d+[-:]\d+',  # Bits 7-0
        ]

        for pattern in patterns:
            if re.search(pattern, text, re.IGNORECASE):
                return True

        return False

    def _count_tokens(self, text: str) -> int:
        """Count tokens using tiktoken"""
        return len(self.tokenizer.encode(text))

    def _generate_chunk_id(self, source: str, index: int, content: str) -> str:
        """
        Generate a unique, deterministic ID for a chunk.

        Format: {source_hash}_{index}_{content_hash}
        """
        source_hash = hashlib.md5(source.encode()).hexdigest()[:8]
        content_hash = hashlib.md5(content.encode()).hexdigest()[:8]

        return f"{source_hash}_{index:04d}_{content_hash}"


# Test/Demo code
if __name__ == "__main__":
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

## HAL Functions

- HAL_GPIO_Init()
- HAL_GPIO_WritePin()
- HAL_GPIO_TogglePin()

## STM32F4 Specific Notes

The STM32F4 series implements GPIO differently from STM32H7.
'''

    print("=" * 80)
    print("STM32 Chunker Test")
    print("=" * 80)
    print()

    chunker = STM32Chunker(ChunkingConfig())
    chunks = chunker.chunk_document(sample, "gpio_guide.md")

    print(f"Generated {len(chunks)} chunks:\n")

    for i, chunk in enumerate(chunks, 1):
        print(f"Chunk {i}: {chunk.id}")
        print(f"  Tokens: {chunk.token_count}")
        print(f"  Peripheral: {chunk.metadata.peripheral}")
        print(f"  Doc Type: {chunk.metadata.doc_type}")
        print(f"  Has code: {chunk.metadata.has_code}")
        print(f"  Has table: {chunk.metadata.has_table}")
        print(f"  Has register: {chunk.metadata.has_register}")
        print(f"  Section path: {' > '.join(chunk.metadata.section_path)}")
        print(f"  STM32 families: {chunk.metadata.stm32_families}")
        print(f"  HAL functions: {chunk.metadata.hal_functions}")
        print(f"  Registers: {chunk.metadata.registers}")
        print(f"  Content preview: {chunk.content[:100]}...")
        print()
