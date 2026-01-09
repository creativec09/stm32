# MCP Resources Documentation

This document describes the available MCP resources for direct documentation access in the STM32 Documentation Server. Resources provide browsable, structured access to documentation content without requiring search queries.

## Table of Contents

- [Overview](#overview)
- [Resources vs Tools](#resources-vs-tools)
- [Available Resources](#available-resources)
  - [Statistics and Health](#statistics-and-health)
  - [Peripherals](#peripherals)
  - [HAL Functions](#hal-functions)
  - [Documents](#documents)
  - [Sources](#sources)
- [Usage Examples](#usage-examples)
- [Resource URI Patterns](#resource-uri-patterns)

## Overview

Resources in MCP provide a REST-like interface for accessing documentation content. They are accessed via URI patterns and return formatted documentation content directly. Unlike tools, resources don't require search queries - they provide direct access to categorized and structured content.

### Key Benefits

1. **Direct Access**: Get specific documentation without formulating search queries
2. **Browsability**: Navigate documentation structure through URI hierarchy
3. **Performance**: Faster access for known content categories
4. **Structured Output**: Pre-formatted, organized documentation content

## Resources vs Tools

| Aspect | Resources | Tools |
|--------|-----------|-------|
| **Access Method** | URI-based (stm32://...) | Function calls |
| **Query Required** | No | Yes (usually) |
| **Use Case** | Browse known content | Search for answers |
| **Output** | Structured categories | Search results |
| **Performance** | Fast, direct | Depends on search |

**When to use Resources:**
- You know exactly what peripheral/topic you need
- Browsing available content
- Getting comprehensive overviews
- Checking documentation coverage

**When to use Tools:**
- Looking for answers to specific questions
- Don't know where information is located
- Need semantic search capabilities
- Want ranked, relevant results

## Available Resources

### Statistics and Health

#### `stm32://stats`

Get comprehensive statistics about the documentation database.

**Returns:**
```json
{
  "total_chunks": 15234,
  "peripheral_distribution": {
    "GPIO": 456,
    "UART": 389,
    "SPI": 312,
    ...
  },
  "document_type_distribution": {
    "reference_manual": 8934,
    "application_note": 3456,
    "hal_guide": 2844
  },
  "collection_name": "stm32_docs",
  "embedding_model": "all-MiniLM-L6-v2"
}
```

**Use Cases:**
- Check database status
- Verify documentation coverage
- Identify gaps in documentation
- Monitor system health

#### `stm32://health`

Get server health status.

**Returns:**
```json
{
  "status": "healthy",
  "server": "stm32-docs",
  "version": "1.0.0",
  "mode": "local",
  "chunks_indexed": 15234,
  "embedding_model": "all-MiniLM-L6-v2"
}
```

**Use Cases:**
- Monitor server status
- Verify server configuration
- Check indexed content count

### Peripherals

#### `stm32://peripherals`

List all available peripherals with documentation coverage.

**Returns:**
```markdown
# Available STM32 Peripherals

The following peripherals have documentation available:

- **GPIO**: 456 documentation chunks
- **UART**: 389 documentation chunks
- **SPI**: 312 documentation chunks
- **I2C**: 287 documentation chunks
...

*Plus 234 general documentation chunks*

**Total documentation chunks**: 15234
```

**Use Cases:**
- Discover available peripherals
- Check documentation coverage
- Plan development work

#### `stm32://peripherals/{peripheral}`

Get peripheral overview (alias for `/overview`).

**Parameters:**
- `peripheral`: Peripheral name (e.g., "GPIO", "UART", "SPI")

**Returns:** Comprehensive overview of the peripheral with introduction, features, and capabilities.

**Example:**
```
stm32://peripherals/UART
```

#### `stm32://peripherals/{peripheral}/overview`

Get comprehensive peripheral overview documentation.

**Parameters:**
- `peripheral`: Peripheral name

**Returns:**
```markdown
# UART Overview

[Detailed overview content including:]
- Introduction and purpose
- Key features and capabilities
- Common use cases
- Block diagrams and architecture
- Related peripherals
```

**Use Cases:**
- Understanding peripheral capabilities
- Learning peripheral architecture
- Planning implementation

#### `stm32://peripherals/{peripheral}/registers`

Get register documentation for a peripheral.

**Parameters:**
- `peripheral`: Peripheral name

**Returns:**
```markdown
# UART Registers

[Register documentation including:]
- Register maps and offsets
- Bit field descriptions
- Reset values
- Access permissions
- Configuration examples
```

**Use Cases:**
- Low-level peripheral programming
- Register-level debugging
- Understanding hardware configuration
- Writing bare-metal code

#### `stm32://peripherals/{peripheral}/examples`

Get code examples for a peripheral.

**Parameters:**
- `peripheral`: Peripheral name

**Returns:**
```markdown
# UART Code Examples

## Example 1
*Source: um1234_hal_guide.md*

[Code example with context]
```c
// UART initialization example
HAL_UART_Init(&huart1);
...
```

---

## Example 2
...
```

**Use Cases:**
- Learning by example
- Copy-paste starting points
- Understanding API usage
- Seeing working configurations

#### `stm32://peripherals/{peripheral}/interrupts`

Get interrupt documentation for a peripheral.

**Parameters:**
- `peripheral`: Peripheral name

**Returns:**
```markdown
# UART Interrupts

[Interrupt documentation including:]
- Interrupt sources
- IRQ handler examples
- NVIC configuration
- Callback functions
- Priority settings
```

**Use Cases:**
- Implementing interrupt handlers
- Understanding interrupt sources
- Configuring NVIC
- Debugging interrupt issues

#### `stm32://peripherals/{peripheral}/dma`

Get DMA configuration for a peripheral.

**Parameters:**
- `peripheral`: Peripheral name

**Returns:**
```markdown
# UART DMA Configuration

[DMA documentation including:]
- DMA channel/stream assignments
- Request mappings
- Configuration examples
- Circular mode setup
- Double buffering
```

**Use Cases:**
- Setting up DMA transfers
- Optimizing data throughput
- Reducing CPU load
- Implementing efficient I/O

### HAL Functions

#### `stm32://hal-functions`

List all HAL functions found in documentation.

**Returns:**
```markdown
# HAL Functions

- `HAL_ADC_Init()`
- `HAL_ADC_Start()`
- `HAL_ADC_Start_DMA()`
- `HAL_GPIO_Init()`
- `HAL_GPIO_ReadPin()`
- `HAL_GPIO_WritePin()`
- `HAL_UART_Init()`
- `HAL_UART_Transmit()`
- `HAL_UART_Transmit_DMA()`
...
```

**Use Cases:**
- Discovering available HAL functions
- Finding function names
- Exploring HAL API coverage

#### `stm32://hal-functions/{peripheral}`

List HAL functions for a specific peripheral.

**Parameters:**
- `peripheral`: Peripheral name

**Returns:**
```markdown
# HAL Functions for UART

- `HAL_UART_Init()`
- `HAL_UART_DeInit()`
- `HAL_UART_Transmit()`
- `HAL_UART_Receive()`
- `HAL_UART_Transmit_IT()`
- `HAL_UART_Receive_IT()`
- `HAL_UART_Transmit_DMA()`
- `HAL_UART_Receive_DMA()`
...
```

**Use Cases:**
- Finding peripheral-specific HAL functions
- Comparing different operation modes (polling, IT, DMA)
- API discovery

### Documents

#### `stm32://documents/{doc_type}`

Get documents of a specific type.

**Parameters:**
- `doc_type`: Document type (see valid types below)

**Valid Document Types:**
- `reference_manual` - Comprehensive hardware reference
- `application_note` - Specific application guides
- `user_manual` - User guides and tutorials
- `programming_manual` - Programming guides
- `datasheet` - Electrical specifications
- `hal_guide` - HAL library documentation
- `errata` - Known issues and workarounds
- `migration_guide` - Migration between MCU families
- `safety_manual` - Safety-critical documentation
- `general` - General documentation

**Returns:**
```markdown
# Reference Manual Documents

Found 5 documents of this type:

- rm0090_stm32f4_reference.md
- rm0385_stm32f7_reference.md
- rm0433_stm32h7_reference.md
- rm0440_stm32g4_reference.md
- rm0453_stm32u5_reference.md
```

**Use Cases:**
- Finding documentation by type
- Exploring available manuals
- Locating specific document categories
- Understanding documentation structure

### Sources

#### `stm32://sources`

List all documentation source files with categorization.

**Returns:**
```markdown
# Documentation Sources

## Reference Manuals
- rm0090_stm32f4_reference.md
- rm0385_stm32f7_reference.md
- rm0433_stm32h7_reference.md

## Application Notes
- an3126_audio_streaming.md
- an4061_pcb_design.md
- an4989_stm32_bootloader.md

## User Manuals
- um1234_hal_drivers.md
- um1850_usb_library.md

## Programming Manuals
- pm0214_cortex_m4_programming.md

**Total sources**: 47
```

**Use Cases:**
- Browsing available documentation
- Verifying ingestion status
- Finding specific source files
- Documentation inventory

## Usage Examples

### Example 1: Getting Started with GPIO

```python
# 1. First, check if GPIO documentation is available
peripherals = mcp.read_resource("stm32://peripherals")
# Verify GPIO is listed

# 2. Get GPIO overview
overview = mcp.read_resource("stm32://peripherals/GPIO/overview")
# Read about GPIO capabilities

# 3. Get code examples
examples = mcp.read_resource("stm32://peripherals/GPIO/examples")
# Find initialization examples

# 4. Get register details for low-level access
registers = mcp.read_resource("stm32://peripherals/GPIO/registers")
# Understand GPIO registers
```

### Example 2: Exploring UART with DMA

```python
# 1. Get UART overview
overview = mcp.read_resource("stm32://peripherals/UART/overview")

# 2. Check DMA configuration
dma_config = mcp.read_resource("stm32://peripherals/UART/dma")

# 3. Find relevant HAL functions
hal_functions = mcp.read_resource("stm32://hal-functions/UART")

# 4. Get code examples
examples = mcp.read_resource("stm32://peripherals/UART/examples")
```

### Example 3: Finding Application Notes

```python
# 1. List all application notes
app_notes = mcp.read_resource("stm32://documents/application_note")

# 2. Get statistics to see coverage
stats = mcp.read_resource("stm32://stats")

# 3. Browse all sources
sources = mcp.read_resource("stm32://sources")
```

### Example 4: System Health Check

```python
# Check server health
health = mcp.read_resource("stm32://health")

# Get detailed statistics
stats = mcp.read_resource("stm32://stats")

# Verify specific peripheral coverage
uart_docs = mcp.read_resource("stm32://peripherals/UART")
```

## Resource URI Patterns

### URI Structure

Resources follow a hierarchical URI pattern:

```
stm32://<category>/<identifier>/<subcategory>
```

### Pattern Examples

| Pattern | Example | Description |
|---------|---------|-------------|
| `stm32://<info>` | `stm32://stats` | Top-level information |
| `stm32://<category>` | `stm32://peripherals` | Category listing |
| `stm32://<category>/<item>` | `stm32://peripherals/GPIO` | Item overview |
| `stm32://<category>/<item>/<aspect>` | `stm32://peripherals/GPIO/registers` | Specific aspect |

### Hierarchical Navigation

Resources are designed for hierarchical browsing:

```
stm32://peripherals                     # List all peripherals
  └─ stm32://peripherals/UART           # UART overview
       ├─ stm32://peripherals/UART/overview   # Detailed overview
       ├─ stm32://peripherals/UART/registers  # Register docs
       ├─ stm32://peripherals/UART/examples   # Code examples
       ├─ stm32://peripherals/UART/interrupts # Interrupt docs
       └─ stm32://peripherals/UART/dma        # DMA configuration
```

## Best Practices

### 1. Start Broad, Then Narrow

```python
# Good: Progressive discovery
peripherals = read("stm32://peripherals")           # List available
overview = read("stm32://peripherals/UART")         # Get overview
examples = read("stm32://peripherals/UART/examples") # Get examples

# Less efficient: Direct deep access without context
examples = read("stm32://peripherals/UART/examples")
```

### 2. Use Resources for Known Content

```python
# Good: Use resources when you know what you want
uart_regs = read("stm32://peripherals/UART/registers")

# Better: Use tools for unknown queries
results = search_stm32_docs("How do I configure UART baud rate?")
```

### 3. Combine Resources and Tools

```python
# 1. Use resource to get overview
overview = read("stm32://peripherals/SPI/overview")

# 2. Use tool to find specific answer
config = search_stm32_docs("SPI master mode configuration for 8-bit data")

# 3. Use resource to get examples
examples = read("stm32://peripherals/SPI/examples")
```

### 4. Check Coverage First

```python
# Before diving deep, verify documentation exists
stats = read("stm32://stats")
# Check if your peripheral has good coverage

peripherals = read("stm32://peripherals")
# Verify your peripheral is documented
```

## Error Handling

Resources return error messages as plain text when issues occur:

### Unknown Peripheral

```
Unknown peripheral: XYZ
```

**Resolution:** Check available peripherals with `stm32://peripherals`

### No Documentation Found

```
No documentation for PERIPHERAL_NAME
```

**Resolution:** The peripheral may not be documented yet, or use a different peripheral name

### Invalid Document Type

```
Unknown document type: invalid_type. Valid: reference_manual, application_note, ...
```

**Resolution:** Use one of the valid document types listed

## Performance Considerations

### Resource Access Speed

Resources are generally fast because they:
1. Don't require embedding generation for queries
2. Use pre-filtered database queries
3. Return cached/structured content

### When Resources Are Slower

- First access (lazy loading of resources handler)
- Very large result sets (e.g., all HAL functions)
- Complex peripheral documentation (many chunks)

### Optimization Tips

1. **Cache frequent accesses** - Resource content doesn't change during runtime
2. **Use specific resources** - `/registers` is faster than broad `/overview`
3. **Parallel requests** - Resources can be accessed concurrently

## Integration with Other Features

### Resources + Tools

```python
# Get overview via resource
overview = read("stm32://peripherals/ADC/overview")

# Search for specific implementation
impl = search_stm32_docs("ADC continuous conversion with DMA")

# Get code examples via resource
examples = read("stm32://peripherals/ADC/examples")
```

### Resources + Prompts

```python
# Use resource to gather context
uart_info = read("stm32://peripherals/UART/overview")
uart_examples = read("stm32://peripherals/UART/examples")

# Use prompt to generate configuration
config_prompt = configure_peripheral("UART", "115200 baud, 8N1, DMA receive")
```

## Summary

Resources provide structured, URI-based access to STM32 documentation:

- **Fast** - Direct access without search overhead
- **Organized** - Hierarchical categorization
- **Complete** - Comprehensive peripheral coverage
- **Browsable** - Easy navigation and discovery

Use resources when you know what you're looking for, and tools when you need to search for answers.

## See Also

- [TOOLS.md](TOOLS.md) - MCP Tools documentation
- [PROMPTS.md](PROMPTS.md) - MCP Prompts documentation
- [API.md](API.md) - Complete API reference
