"""
STM32 Chunk Validator

Validates chunk quality to ensure:
- Token counts are within bounds
- Code blocks are intact
- Tables are complete
- Content has sufficient information density
- Metadata is properly populated
"""

from dataclasses import dataclass
from typing import Optional
import re


@dataclass
class ValidationResult:
    """Result of validating a single chunk"""
    is_valid: bool
    warnings: list[str]
    errors: list[str]


@dataclass
class ValidationReport:
    """Aggregate report for all chunks"""
    total_chunks: int
    valid_chunks: int
    invalid_chunks: int
    warnings_count: int
    issues: list[dict]  # List of {chunk_id, errors, warnings}


class ChunkValidator:
    """
    Validates chunk quality for the STM32 documentation pipeline.

    Ensures chunks meet quality standards before ingestion into vector store.
    """

    def __init__(self, min_tokens: int = 50, max_tokens: int = 2000):
        """
        Initialize validator with token bounds.

        Args:
            min_tokens: Minimum tokens for a valid chunk
            max_tokens: Maximum tokens before considering oversized
        """
        self.min_tokens = min_tokens
        self.max_tokens = max_tokens

    def validate_chunk(self, chunk) -> ValidationResult:
        """
        Validate a single chunk.

        Checks:
        - Token count bounds
        - Code block integrity
        - Table integrity
        - Content quality
        - Metadata completeness

        Args:
            chunk: Chunk object to validate

        Returns:
            ValidationResult with errors and warnings
        """
        errors = []
        warnings = []

        # Check token bounds
        is_valid, msg = self.check_token_bounds(chunk)
        if not is_valid:
            errors.append(msg)
        elif msg:
            warnings.append(msg)

        # Check code integrity
        is_valid, msg = self.check_code_integrity(chunk)
        if not is_valid:
            errors.append(msg)
        elif msg:
            warnings.append(msg)

        # Check table integrity
        is_valid, msg = self.check_table_integrity(chunk)
        if not is_valid:
            errors.append(msg)
        elif msg:
            warnings.append(msg)

        # Check content quality
        is_valid, msg = self.check_content_quality(chunk)
        if not is_valid:
            errors.append(msg)
        elif msg:
            warnings.append(msg)

        # Check metadata completeness
        is_valid, msg = self.check_metadata_completeness(chunk)
        if not is_valid:
            errors.append(msg)
        elif msg:
            warnings.append(msg)

        return ValidationResult(
            is_valid=len(errors) == 0,
            warnings=warnings,
            errors=errors
        )

    def check_token_bounds(self, chunk) -> tuple[bool, Optional[str]]:
        """
        Check if token count is within acceptable bounds.

        Returns:
            (is_valid, message) tuple
            - is_valid: False if hard error, True if ok or warning
            - message: Error/warning message, or None if perfect
        """
        tokens = chunk.token_count

        if tokens < self.min_tokens:
            return False, f"Chunk too small: {tokens} tokens (min: {self.min_tokens})"

        if tokens > self.max_tokens:
            # Oversized is a warning if it contains code/tables, error otherwise
            if chunk.metadata.has_code or chunk.metadata.has_table:
                return True, f"Chunk oversized but contains protected content: {tokens} tokens (max: {self.max_tokens})"
            else:
                return False, f"Chunk too large: {tokens} tokens (max: {self.max_tokens})"

        # Check if chunk is suspiciously small
        if tokens < 100:
            return True, f"Chunk is small: {tokens} tokens - ensure it contains useful information"

        return True, None

    def check_code_integrity(self, chunk) -> tuple[bool, Optional[str]]:
        """
        Check if code blocks are properly formed.

        Validates:
        - Matching opening/closing fence markers
        - No truncated code blocks
        """
        content = chunk.content

        # Count code fence markers
        fence_markers = re.findall(r'^```', content, re.MULTILINE)
        fence_count = len(fence_markers)

        if fence_count % 2 != 0:
            return False, f"Unmatched code fence markers: {fence_count} found (should be even)"

        # If metadata says has_code, verify we can find code blocks
        if chunk.metadata.has_code and fence_count == 0:
            return True, "Metadata indicates code but no code blocks found"

        # Check for truncated code (opening fence near end without closing)
        lines = content.split('\n')
        if len(lines) > 2:
            # Check last few lines
            last_lines = '\n'.join(lines[-3:])
            if '```' in last_lines and fence_count % 2 != 0:
                return False, "Code block appears truncated at end of chunk"

        return True, None

    def check_table_integrity(self, chunk) -> tuple[bool, Optional[str]]:
        """
        Check if markdown tables are complete.

        Validates:
        - Table has header separator row
        - Consistent column counts
        - No truncated tables
        """
        content = chunk.content
        lines = content.split('\n')

        # Find table lines (contain |)
        table_lines = [i for i, line in enumerate(lines) if '|' in line.strip()]

        if not table_lines:
            # No tables found
            if chunk.metadata.has_table:
                return True, "Metadata indicates table but no table rows found"
            return True, None

        # Check for table separator (|---|---|)
        has_separator = False
        for i in table_lines:
            if re.match(r'^\s*\|[\s\-:|]+\|\s*$', lines[i]):
                has_separator = True
                break

        if not has_separator:
            return False, "Table missing header separator row"

        # Check if table is at start or end (might be truncated)
        if table_lines[0] == 0:
            return True, "Table starts at beginning of chunk - may be truncated"

        if table_lines[-1] == len(lines) - 1:
            # Check if it's a complete table by verifying separator exists
            if has_separator:
                return True, None
            else:
                return False, "Table at end of chunk appears incomplete"

        # Check column consistency
        column_counts = []
        for i in table_lines[:5]:  # Check first few rows
            cols = len([c for c in lines[i].split('|') if c.strip()])
            column_counts.append(cols)

        if len(set(column_counts)) > 1:
            return True, f"Inconsistent column counts in table: {column_counts}"

        return True, None

    def check_content_quality(self, chunk) -> tuple[bool, Optional[str]]:
        """
        Check general content quality.

        Validates:
        - Not just whitespace
        - Has actual text (not just symbols)
        - Reasonable character-to-token ratio
        """
        content = chunk.content.strip()

        if not content:
            return False, "Chunk is empty or whitespace only"

        # Check for minimum actual text content
        text_chars = len(re.findall(r'[a-zA-Z]', content))
        if text_chars < 20:
            return False, f"Insufficient text content: only {text_chars} letters"

        # Check character-to-token ratio (should be roughly 3-5 chars per token)
        char_count = len(content)
        if chunk.token_count > 0:
            ratio = char_count / chunk.token_count
            if ratio < 2:
                return True, f"Low char-to-token ratio ({ratio:.1f}) - may indicate encoding issues"
            if ratio > 8:
                return True, f"High char-to-token ratio ({ratio:.1f}) - may indicate excessive whitespace"

        # Check for repeated content (possible chunking error)
        lines = content.split('\n')
        if len(lines) > 10:
            unique_lines = set(lines)
            if len(unique_lines) < len(lines) * 0.5:
                return True, "High line repetition - possible chunking error"

        return True, None

    def check_metadata_completeness(self, chunk) -> tuple[bool, Optional[str]]:
        """
        Check if metadata is properly populated.

        Validates:
        - Required fields are present
        - Metadata flags match content
        """
        metadata = chunk.metadata

        # Check required fields
        if not metadata.source_file:
            return False, "Missing source_file in metadata"

        if not metadata.doc_type or metadata.doc_type == 'unknown':
            return True, "Document type could not be determined"

        if not metadata.section_path:
            return True, "No section path - chunk may lack context"

        # Validate metadata flags against content
        content = chunk.content

        # Check has_code flag
        has_code_fence = '```' in content
        if metadata.has_code and not has_code_fence:
            return True, "has_code=True but no code fences found"
        if not metadata.has_code and has_code_fence:
            return True, "has_code=False but code fences found"

        # Check has_table flag
        has_table_markers = '|' in content and re.search(r'\|[\s\-:|]+\|', content)
        if metadata.has_table and not has_table_markers:
            return True, "has_table=True but no table markers found"
        if not metadata.has_table and has_table_markers:
            return True, "has_table=False but table markers found"

        return True, None

    def generate_report(self, chunks: list) -> ValidationReport:
        """
        Generate validation report for a list of chunks.

        Args:
            chunks: List of Chunk objects to validate

        Returns:
            ValidationReport with summary statistics and issues
        """
        total_chunks = len(chunks)
        valid_chunks = 0
        invalid_chunks = 0
        warnings_count = 0
        issues = []

        for chunk in chunks:
            result = self.validate_chunk(chunk)

            if result.is_valid:
                valid_chunks += 1
            else:
                invalid_chunks += 1

            warnings_count += len(result.warnings)

            # Record issues
            if result.errors or result.warnings:
                issues.append({
                    'chunk_id': chunk.id,
                    'chunk_index': chunk.metadata.chunk_index,
                    'source_file': chunk.metadata.source_file,
                    'errors': result.errors,
                    'warnings': result.warnings
                })

        return ValidationReport(
            total_chunks=total_chunks,
            valid_chunks=valid_chunks,
            invalid_chunks=invalid_chunks,
            warnings_count=warnings_count,
            issues=issues
        )

    def print_report(self, report: ValidationReport, verbose: bool = False):
        """
        Print validation report in human-readable format.

        Args:
            report: ValidationReport to print
            verbose: If True, show all warnings; if False, only errors
        """
        print("\n" + "=" * 80)
        print("CHUNK VALIDATION REPORT")
        print("=" * 80)
        print(f"Total chunks: {report.total_chunks}")
        print(f"Valid chunks: {report.valid_chunks}")
        print(f"Invalid chunks: {report.invalid_chunks}")
        print(f"Warnings: {report.warnings_count}")
        print()

        if report.invalid_chunks > 0:
            print("ERRORS:")
            print("-" * 80)
            for issue in report.issues:
                if issue['errors']:
                    print(f"\nChunk: {issue['chunk_id']}")
                    print(f"  Source: {issue['source_file']}")
                    print(f"  Index: {issue['chunk_index']}")
                    for error in issue['errors']:
                        print(f"  ❌ {error}")
            print()

        if verbose and report.warnings_count > 0:
            print("WARNINGS:")
            print("-" * 80)
            for issue in report.issues:
                if issue['warnings']:
                    print(f"\nChunk: {issue['chunk_id']}")
                    print(f"  Source: {issue['source_file']}")
                    print(f"  Index: {issue['chunk_index']}")
                    for warning in issue['warnings']:
                        print(f"  ⚠️  {warning}")
            print()

        print("=" * 80)


# Test/Demo code
if __name__ == "__main__":
    from chunker import STM32Chunker, ChunkingConfig, Chunk, ChunkMetadata

    # Create some test chunks
    print("Testing Chunk Validator")
    print("=" * 80)
    print()

    # Valid chunk
    valid_chunk = Chunk(
        id="test_001",
        content="""
# GPIO Configuration

The GPIO peripheral provides general purpose I/O functionality.

```c
HAL_GPIO_Init(GPIOA, &gpio_init);
```
""",
        token_count=150,
        metadata=ChunkMetadata(
            source_file="gpio.md",
            doc_type="reference_manual",
            section_path=["GPIO", "Configuration"],
            peripheral="GPIO",
            has_code=True,
            has_table=False,
            has_register=False,
            start_line=0,
            chunk_index=0,
            hal_functions=["HAL_GPIO_Init"],
            registers=[],
            stm32_families=[]
        )
    )

    # Invalid chunk (too small)
    invalid_chunk_small = Chunk(
        id="test_002",
        content="GPIO",
        token_count=1,
        metadata=ChunkMetadata(
            source_file="gpio.md",
            doc_type="reference_manual",
            section_path=["GPIO"],
            peripheral="GPIO",
            has_code=False,
            has_table=False,
            has_register=False,
            start_line=10,
            chunk_index=1
        )
    )

    # Invalid chunk (broken code block)
    invalid_chunk_code = Chunk(
        id="test_003",
        content="""
# Code Example

```c
HAL_GPIO_Init(GPIOA, &gpio_init);
""",
        token_count=100,
        metadata=ChunkMetadata(
            source_file="gpio.md",
            doc_type="reference_manual",
            section_path=["GPIO", "Example"],
            peripheral="GPIO",
            has_code=True,
            has_table=False,
            has_register=False,
            start_line=20,
            chunk_index=2
        )
    )

    # Test validator
    validator = ChunkValidator(min_tokens=50, max_tokens=2000)

    chunks = [valid_chunk, invalid_chunk_small, invalid_chunk_code]

    print("Validating individual chunks:")
    print("-" * 80)
    for chunk in chunks:
        result = validator.validate_chunk(chunk)
        print(f"\nChunk {chunk.id}:")
        print(f"  Valid: {result.is_valid}")
        if result.errors:
            print(f"  Errors: {result.errors}")
        if result.warnings:
            print(f"  Warnings: {result.warnings}")

    print("\n" + "=" * 80)
    print("Generating aggregate report:")
    report = validator.generate_report(chunks)
    validator.print_report(report, verbose=True)
