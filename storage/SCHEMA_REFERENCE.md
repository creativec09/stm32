# Metadata Schema Reference

Quick reference for the STM32 documentation metadata schema.

## ChunkMetadataSchema Fields

### Source Identification
| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `source_file` | `str` | ✅ | Original filename (e.g., "stm32f4_reference.md") |
| `doc_type` | `DocType` | ❌ (default: GENERAL) | Document type classification |

### Content Classification
| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `peripheral` | `Peripheral` | ❌ | Primary peripheral discussed |
| `secondary_peripherals` | `list[str]` | ❌ | Additional peripherals mentioned |
| `content_type` | `ContentType` | ❌ (default: CONCEPTUAL) | Type of content |

### Document Hierarchy
| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `section_path` | `list[str]` | ❌ | Header hierarchy (e.g., ['GPIO', 'Config']) |
| `section_title` | `str` | ❌ | Current section title |

### Content Flags
| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `has_code` | `bool` | ❌ (default: False) | Contains code examples |
| `has_table` | `bool` | ❌ (default: False) | Contains tables |
| `has_register_map` | `bool` | ❌ (default: False) | Contains register definitions |
| `has_diagram_ref` | `bool` | ❌ (default: False) | References diagrams |

### Position Information
| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `chunk_index` | `int` | ❌ (default: 0) | Index of chunk in document |
| `start_line` | `int` | ❌ (default: 0) | Starting line number |

### STM32-Specific
| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `stm32_families` | `list[str]` | ❌ | STM32 families (e.g., ['STM32F4', 'STM32H7']) |
| `hal_functions` | `list[str]` | ❌ | HAL/LL function names mentioned |
| `registers` | `list[str]` | ❌ | Register names mentioned |

## Enumerations

### DocType (10 values)

| Value | Description | Example |
|-------|-------------|---------|
| `REFERENCE_MANUAL` | Reference manuals | RM0090 STM32F4 Reference Manual |
| `APPLICATION_NOTE` | Application notes | AN4013 GPIO application note |
| `USER_MANUAL` | User manuals | Discovery board user manual |
| `PROGRAMMING_MANUAL` | Programming manuals | Cortex-M4 programming manual |
| `DATASHEET` | Datasheets | STM32F407 datasheet |
| `HAL_GUIDE` | HAL/LL driver guides | STM32F4 HAL driver guide |
| `ERRATA` | Errata sheets | STM32F407 errata |
| `MIGRATION_GUIDE` | Migration guides | F4 to H7 migration guide |
| `SAFETY_MANUAL` | Safety certification docs | IEC 61508 safety manual |
| `GENERAL` | General documentation | Any other documentation |

### Peripheral (41 values)

#### Communication (11)
- `GPIO`, `UART`, `USART`, `SPI`, `I2C`, `I3C`
- `CAN`, `FDCAN`, `USB`, `ETH`, `SPDIF`

#### Analog (2)
- `ADC`, `DAC`

#### Timers (5)
- `TIM`, `LPTIM`, `RTC`, `WWDG`, `IWDG`

#### DMA (3)
- `DMA`, `BDMA`, `MDMA`

#### System (7)
- `RCC`, `PWR`, `NVIC`, `EXTI`, `FLASH`, `CRC`, `TAMP`

#### Memory & Storage (4)
- `FMC`, `SDMMC`, `OCTOSPI`, `QUADSPI`

#### Graphics & Display (4)
- `LTDC`, `DCMI`, `DMA2D`, `JPEG`

#### Audio (1)
- `SAI`

#### Security & Crypto (3)
- `RNG`, `CRYP`, `HASH`

#### Math (1)
- `CORDIC`

#### System (2)
- `MPU`, `GENERAL`

### ContentType (8 values)

| Value | Description | Use Case |
|-------|-------------|----------|
| `CONCEPTUAL` | Explanatory content | Feature descriptions, overviews |
| `REGISTER_MAP` | Register definitions | Register bit fields, addresses |
| `CODE_EXAMPLE` | Code snippets | Initialization examples, usage |
| `CONFIGURATION` | Configuration procedures | Step-by-step setup guides |
| `TROUBLESHOOTING` | Debugging/troubleshooting | Common issues, solutions |
| `ELECTRICAL_SPEC` | Electrical specifications | Timing, voltage levels |
| `TIMING_DIAGRAM` | Timing information | Clock cycles, sequences |
| `PIN_DESCRIPTION` | Pin definitions | Pinout, alternate functions |

## Usage Examples

### Minimal Example
```python
meta = ChunkMetadataSchema(
    source_file="stm32f4_reference.md"
)
```

### Basic Example
```python
meta = ChunkMetadataSchema(
    source_file="stm32f4_hal_guide.md",
    doc_type=DocType.HAL_GUIDE,
    peripheral=Peripheral.GPIO,
    has_code=True
)
```

### Complete Example
```python
meta = ChunkMetadataSchema(
    # Source
    source_file="stm32f4_hal_guide.md",
    doc_type=DocType.HAL_GUIDE,
    
    # Classification
    peripheral=Peripheral.GPIO,
    secondary_peripherals=["RCC", "PWR"],
    content_type=ContentType.CODE_EXAMPLE,
    
    # Hierarchy
    section_path=["GPIO", "Initialization", "Example"],
    section_title="GPIO Output Configuration",
    
    # Flags
    has_code=True,
    has_table=False,
    has_register_map=False,
    has_diagram_ref=True,
    
    # Position
    chunk_index=5,
    start_line=123,
    
    # STM32-specific
    stm32_families=["STM32F4", "STM32F7"],
    hal_functions=["HAL_GPIO_Init", "HAL_GPIO_WritePin"],
    registers=["GPIO_MODER", "GPIO_ODR", "GPIO_PUPDR"]
)
```

## Serialization

### To ChromaDB
```python
# Convert to flat dict for storage
chroma_meta = meta.to_chroma_metadata()

# Result (all values are str, int, float, or bool):
{
    "source_file": "stm32f4_hal_guide.md",
    "doc_type": "hal_guide",
    "peripheral": "GPIO",
    "secondary_peripherals": "RCC,PWR",  # Comma-separated
    "content_type": "code_example",
    "section_path": "GPIO > Initialization > Example",  # > separated
    "section_title": "GPIO Output Configuration",
    "has_code": True,
    "has_table": False,
    "has_register_map": False,
    "has_diagram_ref": True,
    "chunk_index": 5,
    "start_line": 123,
    "stm32_families": "STM32F4,STM32F7",  # Comma-separated
    "hal_functions": "HAL_GPIO_Init,HAL_GPIO_WritePin",  # Limited to 10
    "registers": "GPIO_MODER,GPIO_ODR,GPIO_PUPDR"  # Limited to 15
}
```

### From ChromaDB
```python
# Reconstruct from flat dict
meta = ChunkMetadataSchema.from_chroma_metadata(chroma_meta)
```

## Field Constraints

### Storage Limits
- **hal_functions**: Limited to 10 functions (most relevant)
- **registers**: Limited to 15 registers (most relevant)
- Lists truncated during serialization if exceeded

### ChromaDB Constraints
- Metadata keys: Must be strings
- Metadata values: Must be str, int, float, or bool
- No nested structures allowed

### Validation
- **source_file**: Required, must be non-empty
- **Enums**: Must be valid enum values
- **Lists**: Default to empty list if not provided

## Query Patterns

### By Peripheral
```python
# All GPIO documentation
results = store.search_by_peripheral(Peripheral.GPIO)

# GPIO with specific query
results = store.search("initialization", peripheral=Peripheral.GPIO)
```

### By Document Type
```python
# All HAL guides
results = store.search("configuration", doc_type=DocType.HAL_GUIDE)
```

### By Content Type
```python
# Code examples only
results = store.search("GPIO setup", require_code=True)

# Register documentation only
results = store.search("GPIO_MODER", require_register=True)
```

### Combined Filters
```python
# GPIO code examples from HAL guides
results = store.search(
    query="initialization",
    peripheral=Peripheral.GPIO,
    doc_type=DocType.HAL_GUIDE,
    require_code=True
)
```

## Best Practices

### 1. Always Set Core Fields
```python
# Minimum recommended
meta = ChunkMetadataSchema(
    source_file="...",      # Required
    doc_type=DocType...,    # Recommended
    peripheral=Peripheral...  # Recommended if applicable
)
```

### 2. Use Flags Accurately
```python
# Set flags based on actual content
has_code=True            # Only if contains actual code blocks
has_register_map=True    # Only if contains register definitions
has_table=True           # Only if contains structured tables
```

### 3. Maintain Section Hierarchy
```python
# Good: Clear hierarchy
section_path=["GPIO", "Configuration", "Output Mode"]

# Avoid: Flat or unclear
section_path=["GPIO Config"]
```

### 4. Track Related Information
```python
# Include related peripherals
peripheral=Peripheral.GPIO,
secondary_peripherals=["RCC", "PWR"]  # GPIO needs clock from RCC

# Track all HAL functions mentioned
hal_functions=["HAL_GPIO_Init", "HAL_GPIO_WritePin", "HAL_RCC_GPIOx_CLK_ENABLE"]
```

### 5. Use Appropriate Content Types
```python
# Register definition
content_type=ContentType.REGISTER_MAP

# Example code
content_type=ContentType.CODE_EXAMPLE

# Explanation
content_type=ContentType.CONCEPTUAL
```

## Common Patterns

### Pattern 1: Reference Manual Register
```python
ChunkMetadataSchema(
    source_file="rm0090_stm32f4.md",
    doc_type=DocType.REFERENCE_MANUAL,
    peripheral=Peripheral.GPIO,
    content_type=ContentType.REGISTER_MAP,
    has_register_map=True,
    section_path=["GPIO", "Registers", "GPIO_MODER"],
    registers=["GPIO_MODER"]
)
```

### Pattern 2: HAL Guide Code Example
```python
ChunkMetadataSchema(
    source_file="stm32f4_hal_gpio.md",
    doc_type=DocType.HAL_GUIDE,
    peripheral=Peripheral.GPIO,
    content_type=ContentType.CODE_EXAMPLE,
    has_code=True,
    section_path=["GPIO", "Examples", "Output Configuration"],
    hal_functions=["HAL_GPIO_Init"],
    stm32_families=["STM32F4"]
)
```

### Pattern 3: Application Note Configuration
```python
ChunkMetadataSchema(
    source_file="an4013_gpio.md",
    doc_type=DocType.APPLICATION_NOTE,
    peripheral=Peripheral.GPIO,
    content_type=ContentType.CONFIGURATION,
    has_code=True,
    has_diagram_ref=True,
    section_path=["GPIO", "Configuration Examples"],
    hal_functions=["HAL_GPIO_Init", "HAL_GPIO_WritePin"]
)
```

---

For detailed documentation, see `/docs/STORAGE.md`.
For implementation, see `/storage/metadata.py`.
