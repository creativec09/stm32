# STM32 Documentation Chunking Strategy Specification

## Executive Summary

This document defines a comprehensive chunking strategy for STM32 embedded systems documentation, designed to optimize retrieval accuracy for RAG (Retrieval-Augmented Generation) systems while preserving the technical integrity of hardware documentation.

**Document Corpus Overview:**
- 78 markdown files (~160,000 lines total)
- Reference Manual (RM0468): 83,944 lines
- Application Notes (AN): ~50 documents, 200-2,000 lines each
- Programming Manual (PM0253): 7,688 lines
- User Manuals (UM): 1,000-2,000 lines each
- Datasheet: 3,369 lines

---

## 1. Document Classification and Chunking Rules

### 1.1 Reference Manual (RM0468) - Peripheral-Based Chunking

The reference manual is the largest document and requires hierarchical chunking by peripheral chapter.

#### Chunking Strategy: Semantic Peripheral Sections

```
Level 1: Peripheral Chapter (e.g., "GPIO", "TIM1", "USART")
Level 2: Functional Section (e.g., "Registers", "Functional Description", "Interrupts")
Level 3: Individual Register or Feature Block
```

#### Chunk Boundaries for Reference Manual:

| Content Type | Chunk Size (tokens) | Overlap | Boundary Rules |
|--------------|---------------------|---------|----------------|
| Peripheral Overview | 800-1200 | 100 tokens | Split at `## Introduction`, `## Main Features` |
| Functional Description | 1000-1500 | 150 tokens | Split at `### ` subsection headers |
| Register Definitions | 400-800 | 50 tokens | Keep each register as atomic unit |
| Register Bit Tables | Atomic | 0 | Never split tables |
| Register Maps | Atomic | 0 | Keep entire map table intact |
| Block Diagrams | Atomic + context | 100 tokens | Include surrounding explanatory text |

#### Peripheral Chapter Detection Pattern:
```regex
^# \d+\.?\s+([\w\-/]+)\s*\((\w+)\)
```
Examples matched:
- `# 11 General-purpose I/Os (GPIO)`
- `# 54 Serial peripheral interface (SPI)`
- `# 43 Advanced-control timers (TIM1/TIM8)`

#### Register Section Detection:
```regex
^#{2,3}\s+\d+\.\d+\.\d+\s+.*(register|Register).*\((\w+_\w+)\)
```
Examples:
- `### 11.4.1 GPIO port mode register (GPIOx_MODER)`
- `### 8.7.2 RCC source control register (RCC_CR)`

### 1.2 Application Notes (AN) - Topic-Preserving Chunking

Application notes are tutorial-style documents that should preserve conceptual flow.

#### Chunking Strategy: Section-Based with Code Preservation

| Document Size | Strategy | Chunk Target |
|---------------|----------|--------------|
| < 500 lines | Keep intact or split at H2 | 1-3 chunks |
| 500-1000 lines | Split at H2 sections | 3-6 chunks |
| 1000-2000 lines | Split at H2/H3 with overlap | 6-12 chunks |
| > 2000 lines | Hierarchical H2 -> H3 splitting | 10-20 chunks |

#### Code Example Handling:
```
Rule: Code blocks are ATOMIC units
- Never split within code fences or inline code blocks
- Include 2-3 sentences of context before code
- Include any explanatory comments after code
- Minimum code chunk: 200 tokens
- Maximum code chunk: 1500 tokens (split at logical function boundaries)
```

#### Application Note Section Patterns:
```regex
^# \d+\s+.*                    # Main section (e.g., "# 2 Timer synchronization")
^## \d+\.\d+\s+.*              # Subsection (e.g., "## 2.1 Clock input sources")
^### \d+\.\d+\.\d+\s+.*        # Sub-subsection
```

### 1.3 Programming Manual (PM0253) - Instruction-Set Chunking

The programming manual covers Cortex-M7 processor details.

#### Chunking Strategy: Instruction/Feature Groups

| Content Type | Chunk Strategy | Size |
|--------------|----------------|------|
| Programmer's Model | Section-based | 800-1200 tokens |
| Instruction Groups | Group by category | 600-1000 tokens |
| Individual Instructions | 3-5 related instructions per chunk | 400-800 tokens |
| Core Peripheral Registers | One peripheral per chunk | 800-1200 tokens |
| Exception Handling | Complete section | 1000-1500 tokens |

#### Instruction Pattern Detection:
```regex
^#{2,3}\s+\d+\.\d+\.?\d*\s+(\w+)(\s*,\s*\w+)*\s*$
```
Examples:
- `### 3.4.2 LDR and STR, immediate offset`
- `### 3.5.1 ADD, ADC, SUB, SBC, and RSB`

### 1.4 User Manuals (UM) - Safety/Feature-Based Chunking

User manuals like UM2331 (Safety Manual) have structured requirements.

#### Chunking Strategy: Requirement-Preserving Sections

| Section Type | Chunk Handling |
|--------------|----------------|
| Normative References | Keep intact |
| Safety Architecture | Split at major subsections |
| Safety Mechanisms | One mechanism per chunk |
| Conditions of Use | Keep related conditions together |
| Tables (requirements mapping) | Atomic with header context |

### 1.5 Datasheet (STM32H723ZG) - Specification-Block Chunking

Datasheets contain dense electrical specifications.

#### Chunking Strategy: Specification Category Blocks

| Content Type | Chunk Strategy | Notes |
|--------------|----------------|-------|
| Features List | Atomic | Keep complete feature list |
| Pin Descriptions | Per-function group | Group by peripheral |
| Electrical Specs | Per-parameter category | Keep related specs together |
| Package Info | Atomic | One package per chunk |
| Absolute Max Ratings | Atomic | Safety-critical, never split |
| Timing Diagrams | Atomic + description | Include all related timing params |

---

## 2. Chunk Size Recommendations

### 2.1 Token Count Guidelines

```yaml
Optimal Chunk Sizes:
  default:
    target: 800
    min: 400
    max: 1500
    overlap: 100

  register_definitions:
    target: 600
    min: 300
    max: 1000
    overlap: 50

  code_examples:
    target: 500
    min: 200
    max: 1200
    overlap: 0  # Code is atomic

  tables:
    target: atomic
    min: 100
    max: 2000
    overlap: 0  # Tables are atomic

  conceptual_text:
    target: 1000
    min: 600
    max: 1500
    overlap: 150

  electrical_specs:
    target: 600
    min: 300
    max: 1000
    overlap: 50
```

### 2.2 Overlap Strategy

```yaml
Overlap Rules:
  standard_text:
    overlap_tokens: 100
    overlap_strategy: "sentence_boundary"

  register_sections:
    overlap_tokens: 50
    overlap_strategy: "include_register_name_in_next"

  code_blocks:
    overlap_tokens: 0
    overlap_strategy: "none"  # Atomic

  table_content:
    overlap_tokens: 0
    overlap_strategy: "repeat_header_only"

  cross_referenced_content:
    overlap_tokens: 150
    overlap_strategy: "include_reference_context"
```

### 2.3 Special Content Handling

#### Register Bit-Field Tables
```
RULE: Register tables are ATOMIC units
- Detect pattern: <table> containing bit positions (31:0, 15:0, etc.)
- Never split register bit-field tables
- Include register name and address in chunk
- Include reset value information
- Maximum table chunk: 2000 tokens (acceptable overflow)
```

#### Memory Map Tables
```
RULE: Memory maps stay intact
- Detect pattern: Address ranges (0x0000 0000 format)
- Include complete address range mapping
- Group by memory region if table is very large
```

#### Timing/Waveform Diagrams
```
RULE: Diagrams need context
- Include figure reference and caption
- Include 2-3 paragraphs of surrounding explanation
- Link to related timing parameters
```

---

## 3. Metadata Schema

### 3.1 Core Metadata Fields

```json
{
  "chunk_id": "string (UUID)",
  "document_id": "string (filename without extension)",
  "document_type": "enum: RM|AN|PM|UM|DS",
  "document_number": "string (e.g., 'RM0468', 'AN4776')",
  "document_title": "string",
  "document_version": "string (if available)",

  "chunk_index": "integer",
  "total_chunks": "integer",
  "token_count": "integer",
  "char_count": "integer",

  "hierarchy": {
    "level_1": "string (e.g., 'GPIO')",
    "level_2": "string (e.g., 'Registers')",
    "level_3": "string (e.g., 'GPIOx_MODER')",
    "full_path": "string (e.g., 'GPIO > Registers > GPIOx_MODER')"
  },

  "content_type": "enum: overview|functional|register|table|code|diagram|electrical|safety",
  "has_code": "boolean",
  "has_table": "boolean",
  "has_diagram": "boolean",

  "peripheral_tags": ["string array"],
  "stm32_series": ["string array (e.g., 'H7', 'H723')"],

  "cross_references": {
    "internal_refs": ["string array (section references)"],
    "external_docs": ["string array (e.g., 'AN2606', 'PM0253')"],
    "register_refs": ["string array (e.g., 'RCC_CR', 'FLASH_ACR')"]
  },

  "source_location": {
    "start_line": "integer",
    "end_line": "integer",
    "heading_path": "string"
  }
}
```

### 3.2 Hierarchy Mapping

#### Reference Manual Hierarchy:
```
Document: RM0468
  |-- Memory and bus architecture
  |   |-- System architecture
  |   |-- Memory organization
  |   |-- Boot configuration
  |
  |-- RAM ECC monitoring (RAMECC)
  |   |-- Introduction
  |   |-- Main features
  |   |-- Functional description
  |   |-- Registers
  |       |-- RAMECC_IER
  |       |-- RAMECC_MxCR
  |
  |-- Embedded Flash memory (FLASH)
  |   |-- Introduction
  |   |-- Main features
  |   |-- Functional description
  |   |-- Option bytes
  |   |-- Protection mechanisms
  |   |-- Registers
  |       |-- FLASH_ACR
  |       |-- FLASH_KEYR
  |
  |-- Power control (PWR)
  |-- Reset and clock control (RCC)
  |-- GPIO
  |-- Timers (TIM1/TIM8, TIM2-TIM5, etc.)
  |-- Communication (SPI, I2C, USART, USB, ETH)
  |-- ADC/DAC
  |-- ...
```

#### Application Note Hierarchy:
```
Document: AN4776 (Timer Cookbook)
  |-- Basic operating modes
  |   |-- Timer tear-down
  |   |-- Basic operating modes
  |   |-- Advanced features
  |
  |-- Timer clocking
  |   |-- External clock mode 1
  |   |-- External clock mode 2
  |   |-- Application example
  |
  |-- N-pulse generation
  |-- Break input
  |-- DMA-burst feature
  |-- Timer synchronization
```

### 3.3 Cross-Reference Tracking

```json
{
  "reference_patterns": {
    "section_ref": "Section \\d+(\\.\\d+)*",
    "figure_ref": "Figure \\d+",
    "table_ref": "Table \\d+",
    "register_ref": "[A-Z]+[0-9]*_[A-Z0-9_]+",
    "app_note_ref": "AN\\d{4}",
    "ref_manual_ref": "RM\\d{4}",
    "prog_manual_ref": "PM\\d{4}",
    "user_manual_ref": "UM\\d{4}"
  },

  "extracted_refs_example": {
    "chunk_id": "rm0468_flash_001",
    "internal_refs": ["Section 4.4", "Section 5", "Table 16"],
    "external_docs": ["AN2606", "PM0253"],
    "register_refs": ["FLASH_ACR", "FLASH_CR", "RCC_CFGR"]
  }
}
```

---

## 4. Implementation Approach

### 4.1 Recommended Tools and Libraries

```yaml
Primary Chunking Framework:
  - LangChain TextSplitters (customized)
  - LlamaIndex NodeParser (alternative)

Markdown Parsing:
  - markdown-it (for structure extraction)
  - BeautifulSoup4 (for HTML table handling)
  - regex (for pattern matching)

Token Counting:
  - tiktoken (cl100k_base for OpenAI compatibility)
  - transformers AutoTokenizer (for other models)

Table Processing:
  - pandas (for table manipulation)
  - tabulate (for table reconstruction)

Metadata Extraction:
  - pydantic (for schema validation)
  - jsonschema (for validation)
```

### 4.2 Processing Pipeline

```
┌─────────────────────────────────────────────────────────────────┐
│                    STM32 Document Chunking Pipeline              │
└─────────────────────────────────────────────────────────────────┘
                                │
                                ▼
┌─────────────────────────────────────────────────────────────────┐
│ STAGE 1: Document Classification                                 │
│ ─────────────────────────────────────────────────────────────── │
│ • Identify document type (RM/AN/PM/UM/DS) from filename         │
│ • Extract document number and version                            │
│ • Parse table of contents structure                              │
│ • Build initial hierarchy map                                    │
└─────────────────────────────────────────────────────────────────┘
                                │
                                ▼
┌─────────────────────────────────────────────────────────────────┐
│ STAGE 2: Structure Extraction                                    │
│ ─────────────────────────────────────────────────────────────── │
│ • Parse markdown headers (H1-H6)                                 │
│ • Identify section boundaries                                    │
│ • Detect special content blocks:                                 │
│   - Tables (HTML <table> tags)                                   │
│   - Code blocks (``` fences)                                     │
│   - Images/diagrams (![])                                        │
│   - Register definitions (specific patterns)                     │
└─────────────────────────────────────────────────────────────────┘
                                │
                                ▼
┌─────────────────────────────────────────────────────────────────┐
│ STAGE 3: Atomic Unit Identification                              │
│ ─────────────────────────────────────────────────────────────── │
│ • Mark tables as atomic (never split)                            │
│ • Mark code blocks as atomic                                     │
│ • Mark register bit-field tables as atomic                       │
│ • Mark diagrams with context as atomic                           │
│ • Calculate token counts for atomic units                        │
└─────────────────────────────────────────────────────────────────┘
                                │
                                ▼
┌─────────────────────────────────────────────────────────────────┐
│ STAGE 4: Semantic Chunking                                       │
│ ─────────────────────────────────────────────────────────────── │
│ • Apply document-type-specific chunking rules                    │
│ • Respect atomic unit boundaries                                 │
│ • Apply overlap strategy                                         │
│ • Ensure chunks meet size constraints                            │
│ • Handle edge cases (oversized atomic units)                     │
└─────────────────────────────────────────────────────────────────┘
                                │
                                ▼
┌─────────────────────────────────────────────────────────────────┐
│ STAGE 5: Metadata Enrichment                                     │
│ ─────────────────────────────────────────────────────────────── │
│ • Attach hierarchy metadata                                      │
│ • Extract cross-references                                       │
│ • Tag peripherals and STM32 series                               │
│ • Calculate content type classifications                         │
│ • Generate chunk IDs                                             │
└─────────────────────────────────────────────────────────────────┘
                                │
                                ▼
┌─────────────────────────────────────────────────────────────────┐
│ STAGE 6: Quality Validation                                      │
│ ─────────────────────────────────────────────────────────────── │
│ • Verify chunk size constraints                                  │
│ • Check table integrity (no split tables)                        │
│ • Validate metadata completeness                                 │
│ • Check cross-reference validity                                 │
│ • Generate quality report                                        │
└─────────────────────────────────────────────────────────────────┘
                                │
                                ▼
┌─────────────────────────────────────────────────────────────────┐
│ STAGE 7: Output Generation                                       │
│ ─────────────────────────────────────────────────────────────── │
│ • Generate JSON/JSONL output with chunks + metadata              │
│ • Create chunk index for fast lookup                             │
│ • Generate cross-reference graph                                 │
│ • Output statistics and quality metrics                          │
└─────────────────────────────────────────────────────────────────┘
```

### 4.3 Core Chunking Algorithm

```python
# Pseudocode for main chunking logic

class STM32DocumentChunker:
    def __init__(self, config: ChunkingConfig):
        self.config = config
        self.tokenizer = tiktoken.get_encoding("cl100k_base")

    def chunk_document(self, doc: Document) -> List[Chunk]:
        # 1. Classify document
        doc_type = self.classify_document(doc.filename)

        # 2. Extract structure
        structure = self.extract_structure(doc.content)

        # 3. Identify atomic units
        atomic_units = self.identify_atomic_units(structure)

        # 4. Apply chunking strategy based on document type
        if doc_type == "RM":
            chunks = self.chunk_reference_manual(structure, atomic_units)
        elif doc_type == "AN":
            chunks = self.chunk_application_note(structure, atomic_units)
        elif doc_type == "PM":
            chunks = self.chunk_programming_manual(structure, atomic_units)
        elif doc_type == "UM":
            chunks = self.chunk_user_manual(structure, atomic_units)
        elif doc_type == "DS":
            chunks = self.chunk_datasheet(structure, atomic_units)

        # 5. Enrich metadata
        chunks = self.enrich_metadata(chunks, doc, structure)

        # 6. Validate
        self.validate_chunks(chunks)

        return chunks

    def identify_atomic_units(self, structure: DocumentStructure) -> List[AtomicUnit]:
        """Identify content that should never be split."""
        atomic_units = []

        # Tables are atomic
        for table in structure.tables:
            atomic_units.append(AtomicUnit(
                type="table",
                content=table.content,
                tokens=self.count_tokens(table.content),
                start_line=table.start_line,
                end_line=table.end_line
            ))

        # Code blocks are atomic
        for code in structure.code_blocks:
            atomic_units.append(AtomicUnit(
                type="code",
                content=code.content,
                tokens=self.count_tokens(code.content),
                start_line=code.start_line,
                end_line=code.end_line
            ))

        # Register definitions with bit tables
        for register in structure.register_definitions:
            if register.has_bit_table:
                atomic_units.append(AtomicUnit(
                    type="register",
                    content=register.full_content,
                    tokens=self.count_tokens(register.full_content),
                    register_name=register.name
                ))

        return atomic_units

    def chunk_reference_manual(self, structure, atomic_units) -> List[Chunk]:
        """Chunk reference manual by peripheral chapters."""
        chunks = []

        for peripheral in structure.peripheral_chapters:
            # Chunk introduction/overview
            if peripheral.overview:
                chunks.extend(self.chunk_text_section(
                    peripheral.overview,
                    target_tokens=1000,
                    overlap=100
                ))

            # Chunk functional description
            for section in peripheral.functional_sections:
                chunks.extend(self.chunk_text_section(
                    section,
                    target_tokens=1200,
                    overlap=150
                ))

            # Chunk registers (respecting atomic units)
            for register in peripheral.registers:
                if register in atomic_units:
                    chunks.append(self.create_atomic_chunk(register))
                else:
                    chunks.extend(self.chunk_register_section(register))

        return chunks
```

### 4.4 Quality Validation Methods

```yaml
Validation Rules:

  chunk_size_validation:
    - rule: "min_tokens >= 200"
      severity: "warning"
      action: "merge_with_adjacent"

    - rule: "max_tokens <= 2000"
      severity: "error"
      action: "flag_for_review"
      exception: "atomic_units"

  table_integrity:
    - rule: "no_split_tables"
      check: "table_start_tag has matching end_tag in same chunk"
      severity: "critical"

    - rule: "table_header_preserved"
      check: "first row of table present if table is chunked"
      severity: "critical"

  code_integrity:
    - rule: "no_split_code_blocks"
      check: "code fence start has matching end in same chunk"
      severity: "critical"

    - rule: "code_has_context"
      check: "code block has >= 50 tokens of surrounding text"
      severity: "warning"

  metadata_completeness:
    - rule: "required_fields_present"
      fields: ["chunk_id", "document_id", "hierarchy", "content_type"]
      severity: "error"

    - rule: "valid_cross_references"
      check: "all internal refs resolve to existing chunks"
      severity: "warning"

  semantic_coherence:
    - rule: "chunk_starts_at_boundary"
      check: "chunk starts at sentence or header boundary"
      severity: "info"

    - rule: "register_name_in_chunk"
      check: "if register chunk, register name appears in content"
      severity: "warning"
```

### 4.5 Expected Output Statistics

```yaml
Expected Chunk Distribution:

Reference Manual (RM0468):
  total_chunks: ~2500-3500
  avg_tokens_per_chunk: 700
  distribution:
    register_chunks: ~40%
    functional_description: ~35%
    overview_chapters: ~15%
    tables_and_maps: ~10%

Application Notes (50 docs):
  total_chunks: ~400-600
  avg_tokens_per_chunk: 850
  distribution:
    tutorial_content: ~50%
    code_examples: ~25%
    tables_and_figures: ~15%
    overview: ~10%

Programming Manual (PM0253):
  total_chunks: ~200-300
  avg_tokens_per_chunk: 750
  distribution:
    instruction_descriptions: ~60%
    core_peripherals: ~25%
    programmer_model: ~15%

User Manuals (2 docs):
  total_chunks: ~80-120
  avg_tokens_per_chunk: 800

Datasheet:
  total_chunks: ~100-150
  avg_tokens_per_chunk: 650
  distribution:
    electrical_specs: ~50%
    pinouts: ~20%
    features_overview: ~15%
    package_info: ~15%

TOTAL ESTIMATED CHUNKS: 3300-4700
```

---

## 5. Special Handling Cases

### 5.1 Handling Oversized Atomic Units

```yaml
Problem: Some tables exceed 2000 tokens
Solution:
  1. Log warning for review
  2. If table has natural row groupings:
     - Split at row group boundaries
     - Repeat header row in each chunk
  3. If table cannot be split:
     - Accept oversized chunk (up to 3000 tokens)
     - Add metadata flag: "oversized_atomic": true
```

### 5.2 Cross-Document References

```yaml
Strategy: Build reference graph during chunking

Reference Resolution:
  - Extract all AN/RM/PM/UM references
  - Build document dependency graph
  - Store in chunk metadata for retrieval-time linking

Example:
  chunk_id: "rm0468_flash_012"
  external_refs:
    - doc: "AN2606"
      context: "bootloader configuration"
    - doc: "PM0253"
      context: "Cortex-M7 exception handling"
```

### 5.3 Register Cross-References

```yaml
Strategy: Track register references across chunks

Register Reference Index:
  - Extract all register names (pattern: [A-Z]+_[A-Z0-9_]+)
  - Build register -> chunk mapping
  - Store in separate index for fast lookup

Example:
  register_index:
    FLASH_ACR:
      definition_chunk: "rm0468_flash_reg_001"
      referenced_in: ["rm0468_flash_003", "rm0468_rcc_015"]
    RCC_CR:
      definition_chunk: "rm0468_rcc_reg_001"
      referenced_in: ["rm0468_flash_012", "rm0468_pwr_008"]
```

---

## 6. Implementation Checklist

### Phase 1: Setup
- [ ] Set up Python environment with required libraries
- [ ] Create configuration files for chunk sizes per document type
- [ ] Implement document classifier
- [ ] Implement markdown structure parser

### Phase 2: Core Chunking
- [ ] Implement atomic unit detection (tables, code, registers)
- [ ] Implement reference manual chunker
- [ ] Implement application note chunker
- [ ] Implement programming manual chunker
- [ ] Implement user manual chunker
- [ ] Implement datasheet chunker

### Phase 3: Metadata
- [ ] Implement hierarchy extraction
- [ ] Implement cross-reference extraction
- [ ] Implement peripheral tagging
- [ ] Implement metadata schema validation

### Phase 4: Quality
- [ ] Implement chunk size validation
- [ ] Implement table integrity checks
- [ ] Implement code block integrity checks
- [ ] Generate quality reports

### Phase 5: Output
- [ ] Generate JSON/JSONL output
- [ ] Create chunk index
- [ ] Build cross-reference graph
- [ ] Generate statistics report

---

## 7. Revision History

| Version | Date | Author | Changes |
|---------|------|--------|---------|
| 1.0 | 2024-01-08 | Claude | Initial specification |

---

## Appendix A: Sample Chunks

### A.1 Register Chunk Example (Atomic)

```json
{
  "chunk_id": "rm0468_ramecc_reg_001",
  "document_id": "rm0468",
  "document_type": "RM",
  "hierarchy": {
    "level_1": "RAM ECC monitoring (RAMECC)",
    "level_2": "RAMECC registers",
    "level_3": "RAMECC_IER",
    "full_path": "RAM ECC monitoring > Registers > RAMECC_IER"
  },
  "content_type": "register",
  "has_table": true,
  "content": "### 3.4.1 RAMECC interrupt enable register (RAMECC_IER)\n\nAddress offset: 0x00\nReset value: 0x0000 0000\n\n[BIT TABLE HERE]\n\nBit 3 GECCDEBWIE: Global ECC double error on byte write (BW) interrupt enable...",
  "token_count": 450,
  "cross_references": {
    "register_refs": ["RAMECC_MxCR", "RAMECC_MxSR"]
  }
}
```

### A.2 Code Example Chunk (Atomic)

```json
{
  "chunk_id": "an4776_timer_code_001",
  "document_id": "an4776",
  "document_type": "AN",
  "hierarchy": {
    "level_1": "Basic operating modes",
    "level_2": "Timer time-base configuration",
    "full_path": "Basic operating modes > Timer time-base configuration"
  },
  "content_type": "code",
  "has_code": true,
  "content": "### 1.3.1 Timer time-base configuration\n\nThe following code snippet demonstrates a hardware-precision delay loop using TIM6:\n\n```c\n#define ANY_DELAY_REQUIRED 0x0FFF\n/* Clear the update event flag */\nTIM6->SR = 0;\n/* Set the required delay */\nTIM6->ARR = ANY_DELAY_REQUIRED;\n/* Start the timer counter */\nTIM6->CR1 |= TIM_CR1_CEN;\n/* Loop until the update event flag is set */\nwhile (!(TIM6->SR & TIM_SR_UIF));\n```\n\nThis demonstrates the basic timer configuration for delay generation.",
  "token_count": 380,
  "peripheral_tags": ["TIM6", "Timer"],
  "cross_references": {
    "register_refs": ["TIM6_SR", "TIM6_ARR", "TIM6_CR1"]
  }
}
```

### A.3 Conceptual Section Chunk

```json
{
  "chunk_id": "rm0468_flash_func_003",
  "document_id": "rm0468",
  "document_type": "RM",
  "hierarchy": {
    "level_1": "Embedded Flash memory (FLASH)",
    "level_2": "FLASH functional description",
    "level_3": "FLASH read operations",
    "full_path": "Embedded Flash memory > Functional description > Read operations"
  },
  "content_type": "functional",
  "has_table": true,
  "content": "### 4.3.8 FLASH read operations\n\nThe embedded Flash memory supports the execution of one read command while two are waiting in the read command queue. Multiple read access types are also supported...\n\n[TABLE 16: Wait states vs clock frequency]\n\nWhen changing the AXI bus frequency, the application software must follow the below sequence...",
  "token_count": 920,
  "peripheral_tags": ["FLASH"],
  "cross_references": {
    "internal_refs": ["Section 4.3.3"],
    "register_refs": ["FLASH_ACR", "RCC_CFGR"]
  }
}
```
