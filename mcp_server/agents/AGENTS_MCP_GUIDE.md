# STM32 Agents - MCP Integration Guide

## Overview

All STM32 specialized agents have access to the `stm32-docs` MCP server for documentation retrieval. This guide provides comprehensive documentation for all MCP tools, resources, and best practices.

## MCP Server Details

- **Server Name**: `stm32-docs`
- **Tool Access Pattern**: `mcp__stm32-docs__<tool_name>`
- **Resource Access Pattern**: `stm32://<resource_path>`
- **Purpose**: Query STM32 documentation, code examples, errata, and troubleshooting databases

---

## Available MCP Tools

### Core Search Tools

| Tool | Purpose | Parameters | Return Type |
|------|---------|------------|-------------|
| `search_stm32_docs` | Semantic search across all documentation | `query` (str), `num_results` (int, default=5), `peripheral` (str, optional), `require_code` (bool, default=False) | Formatted markdown with relevance scores |
| `get_peripheral_docs` | Get comprehensive peripheral documentation | `peripheral` (str), `topic` (str, optional), `include_code` (bool, default=True) | Markdown documentation sections |
| `get_code_examples` | Find code examples | `topic` (str), `peripheral` (str, optional), `num_examples` (int, default=3) | Code examples with source citations |
| `get_register_info` | Get register-level documentation | `register_name` (str) | Register bit fields and configuration |
| `list_peripherals` | List available peripherals with doc counts | None | Peripheral list with chunk counts |

### HAL/LL Function Tools

| Tool | Purpose | Parameters | Return Type |
|------|---------|------------|-------------|
| `search_hal_function` | Search for HAL/LL function documentation | `function_name` (str) | Function docs with parameters and examples |
| `lookup_hal_function` | Enhanced HAL/LL lookup with peripheral context | `function_name` (str) | Detailed function documentation |

### Initialization and Configuration Tools

| Tool | Purpose | Parameters | Return Type |
|------|---------|------------|-------------|
| `get_init_sequence` | Get complete initialization sequence | `peripheral` (str), `use_case` (str, optional) | Init code with clock, GPIO, peripheral setup |
| `get_clock_config` | Get clock configuration guidance | `target_frequency` (str, optional), `clock_source` (str, optional) | Clock tree configuration code |
| `get_init_template` | Get complete peripheral init template | `peripheral` (str), `mode` (str, optional) | Full initialization template |

### Code Example Tools

| Tool | Purpose | Parameters | Return Type |
|------|---------|------------|-------------|
| `get_interrupt_code` | Get interrupt handling examples | `peripheral` (str), `interrupt_type` (str, optional) | Interrupt config and callback code |
| `get_dma_code` | Get DMA configuration examples | `peripheral` (str), `direction` (str: TX/RX/both) | DMA setup code |
| `get_low_power_code` | Get low power mode examples | `mode` (str: Sleep/Stop/Standby, optional) | Power mode entry/exit code |
| `get_callback_code` | Get HAL callback examples | `peripheral` (str), `callback_type` (str, optional) | Callback implementation examples |

### Troubleshooting Tools

| Tool | Purpose | Parameters | Return Type |
|------|---------|------------|-------------|
| `troubleshoot_error` | Find solutions for common errors | `error_description` (str), `peripheral` (str, optional) | Troubleshooting steps and solutions |

### Comparison and Migration Tools

| Tool | Purpose | Parameters | Return Type |
|------|---------|------------|-------------|
| `compare_peripheral_options` | Compare peripheral configurations | `peripheral1` (str), `peripheral2` (str), `aspect` (str, optional) | Comparison documentation |
| `get_migration_guide` | Migration information between families | `from_family` (str), `to_family` (str), `peripheral` (str, optional) | Migration considerations and code changes |

### Specification Tools

| Tool | Purpose | Parameters | Return Type |
|------|---------|------------|-------------|
| `get_electrical_specifications` | Get electrical specs | `topic` (str) | Electrical characteristics |
| `get_timing_specifications` | Get timing specs and diagrams | `peripheral` (str), `timing_type` (str, optional) | Timing requirements |

---

## MCP Resources

Resources provide direct access to documentation content via URI patterns.

### Available Resources

| Resource URI | Description | Parameters |
|--------------|-------------|------------|
| `stm32://peripherals` | List all documented peripherals | None |
| `stm32://peripherals/{peripheral}` | Overview for specific peripheral | `peripheral`: GPIO, UART, SPI, etc. |
| `stm32://peripherals/{peripheral}/overview` | Comprehensive peripheral overview | `peripheral` |
| `stm32://peripherals/{peripheral}/registers` | Register documentation | `peripheral` |
| `stm32://peripherals/{peripheral}/examples` | Code examples | `peripheral` |
| `stm32://peripherals/{peripheral}/interrupts` | Interrupt documentation | `peripheral` |
| `stm32://peripherals/{peripheral}/dma` | DMA configuration | `peripheral` |
| `stm32://hal-functions` | List all HAL functions | None |
| `stm32://hal-functions/{peripheral}` | HAL functions for peripheral | `peripheral` |
| `stm32://sources` | List documentation source files | None |
| `stm32://documents/{doc_type}` | Documents by type | `doc_type`: reference_manual, application_note, etc. |
| `stm32://stats` | Documentation database statistics | None |
| `stm32://health` | Server health status | None |

### Resource Usage Examples

```python
# List available peripherals
ReadMcpResourceTool(server="stm32-docs", uri="stm32://peripherals")

# Get UART overview
ReadMcpResourceTool(server="stm32-docs", uri="stm32://peripherals/UART")

# Get SPI register documentation
ReadMcpResourceTool(server="stm32-docs", uri="stm32://peripherals/SPI/registers")

# List HAL functions for TIM peripheral
ReadMcpResourceTool(server="stm32-docs", uri="stm32://hal-functions/TIM")
```

---

## Tool Usage Examples

### Basic Search

```python
# General documentation search
mcp__stm32-docs__search_stm32_docs(
    query="How to configure UART for 115200 baud",
    num_results=5
)

# Peripheral-filtered search
mcp__stm32-docs__search_stm32_docs(
    query="DMA circular mode configuration",
    peripheral="DMA",
    num_results=8
)

# Code-only search
mcp__stm32-docs__search_stm32_docs(
    query="GPIO toggle LED",
    require_code=True
)
```

### Peripheral Documentation

```python
# Get comprehensive UART documentation
mcp__stm32-docs__get_peripheral_docs(
    peripheral="UART"
)

# Get specific topic within peripheral
mcp__stm32-docs__get_peripheral_docs(
    peripheral="SPI",
    topic="DMA mode"
)

# Get ADC with interrupt focus
mcp__stm32-docs__get_peripheral_docs(
    peripheral="ADC",
    topic="interrupt"
)
```

### HAL Function Lookup

```python
# Basic HAL function search
mcp__stm32-docs__search_hal_function(
    function_name="HAL_GPIO_Init"
)

# Enhanced lookup with context
mcp__stm32-docs__lookup_hal_function(
    function_name="HAL_UART_Transmit_DMA"
)

# LL function lookup
mcp__stm32-docs__lookup_hal_function(
    function_name="LL_TIM_SetCounter"
)

# Macro lookup
mcp__stm32-docs__lookup_hal_function(
    function_name="__HAL_RCC_GPIOA_CLK_ENABLE"
)
```

### Initialization Sequences

```python
# Basic peripheral init
mcp__stm32-docs__get_init_sequence(
    peripheral="UART"
)

# Specific use case
mcp__stm32-docs__get_init_sequence(
    peripheral="SPI",
    use_case="DMA master mode"
)

# Init template with mode
mcp__stm32-docs__get_init_template(
    peripheral="TIM",
    mode="PWM"
)
```

### Code Examples

```python
# Get interrupt examples
mcp__stm32-docs__get_interrupt_code(
    peripheral="UART",
    interrupt_type="RXNE"
)

# Get DMA examples
mcp__stm32-docs__get_dma_code(
    peripheral="SPI",
    direction="TX"
)

# Get callback examples
mcp__stm32-docs__get_callback_code(
    peripheral="I2C",
    callback_type="Error"
)

# Get low power examples
mcp__stm32-docs__get_low_power_code(
    mode="Stop"
)
```

### Troubleshooting

```python
# Error troubleshooting
mcp__stm32-docs__troubleshoot_error(
    error_description="UART receiving garbage data"
)

# Peripheral-specific troubleshooting
mcp__stm32-docs__troubleshoot_error(
    error_description="HAL_TIMEOUT error",
    peripheral="I2C"
)
```

### Comparison and Migration

```python
# Compare peripherals
mcp__stm32-docs__compare_peripheral_options(
    peripheral1="SPI",
    peripheral2="I2C",
    aspect="speed"
)

# Migration guide
mcp__stm32-docs__get_migration_guide(
    from_family="STM32F4",
    to_family="STM32H7",
    peripheral="DMA"
)
```

### Specifications

```python
# Electrical specs
mcp__stm32-docs__get_electrical_specifications(
    topic="GPIO drive strength"
)

# Timing specs
mcp__stm32-docs__get_timing_specifications(
    peripheral="SPI",
    timing_type="clock frequency"
)
```

---

## Workflows by Use Case

### Configuration Questions

```
1. mcp__stm32-docs__get_peripheral_docs("UART")
2. mcp__stm32-docs__get_init_sequence("UART", "DMA receive")
3. mcp__stm32-docs__get_code_examples("UART DMA", peripheral="UART")
```

### Code Implementation

```
1. mcp__stm32-docs__lookup_hal_function("HAL_UART_Transmit_DMA")
2. mcp__stm32-docs__get_callback_code("UART", "TxCplt")
3. mcp__stm32-docs__get_dma_code("UART", "TX")
```

### Debugging Issues

```
1. mcp__stm32-docs__troubleshoot_error("UART receiving garbage")
2. mcp__stm32-docs__search_stm32_docs("UART baud rate mismatch")
3. mcp__stm32-docs__get_register_info("USART_BRR")
```

### Migration Projects

```
1. mcp__stm32-docs__get_migration_guide("STM32F4", "STM32H7")
2. mcp__stm32-docs__compare_peripheral_options("DMA F4", "DMA H7")
3. mcp__stm32-docs__get_init_sequence("DMA", "new family patterns")
```

---

## Fallback Instructions

When MCP tools are unavailable or return no results, use these fallback strategies:

### 1. MCP Server Not Connected

If you see "MCP server not available" or connection errors:

```markdown
**Note**: The STM32 documentation server is currently unavailable.
I'll provide guidance based on general STM32 knowledge.

For verified documentation, please consult:
- ST Reference Manuals (RMxxxx)
- ST Application Notes (ANxxxx)
- STM32Cube HAL User Manual (UM1785)
- STM32 online documentation at st.com
```

### 2. No Results Found

If a search returns no results:

1. **Broaden the query**: Remove specific filters or use more general terms
2. **Try alternative tool**: Use `search_stm32_docs` instead of specific tools
3. **Check peripheral name**: Ensure correct spelling (UART vs USART, TIM vs TIMER)
4. **Provide general guidance** with disclaimer:

```markdown
**Note**: No specific documentation found in the database.
Based on general STM32 knowledge:
[Your guidance here]

Please verify with official ST documentation.
```

### 3. Partial Results

If results are incomplete:

1. **Combine multiple searches**: Use different query terms
2. **Cross-reference**: Use both search and resource tools
3. **Fill gaps**: Add general knowledge with clear attribution

### 4. Error Handling Pattern

```python
# Try primary tool
result = mcp__stm32-docs__get_peripheral_docs("UART")

# If empty or error, try fallback
if not result or "No documentation" in result:
    result = mcp__stm32-docs__search_stm32_docs("UART configuration overview")

# If still empty, use resources
if not result or "No documentation" in result:
    result = ReadMcpResourceTool(server="stm32-docs", uri="stm32://peripherals/UART")

# Final fallback: provide general guidance with disclaimer
```

---

## Best Practices

### 1. Always Search Before Answering

Documentation is more reliable than general knowledge for STM32-specific details:
- Register addresses and bit definitions
- HAL/LL function signatures
- Known errata and workarounds
- Timing requirements

### 2. Cite Your Sources

Always reference which documentation informed the answer:

```markdown
## Documentation Reference
Based on:
- [Reference Manual RM0433]: Timer configuration
- [AN4776]: Timer cookbook
- [Code examples]: PWM generation
```

### 3. Combine Knowledge Sources

Use documentation + expertise for best answers:
- Documentation provides accuracy
- Expertise provides context and best practices
- Together they provide complete solutions

### 4. Use Appropriate Tools

| Need | Primary Tool | Fallback Tool |
|------|-------------|---------------|
| General info | `search_stm32_docs` | `get_peripheral_docs` |
| Function usage | `lookup_hal_function` | `search_hal_function` |
| Code examples | `get_code_examples` | `search_stm32_docs` with `require_code=True` |
| Initialization | `get_init_sequence` | `get_init_template` |
| Troubleshooting | `troubleshoot_error` | `search_stm32_docs` |
| Register details | `get_register_info` | Resource: `stm32://peripherals/{p}/registers` |

### 5. Provide Complete Examples

Include all required initialization from documentation, not just the main function.

---

## Agent-Specific Tool Priorities

### Triage Agent
- `search_stm32_docs` - Understand query domain
- `troubleshoot_error` - Categorize issues
- `list_peripherals` - Identify relevant peripherals

### Firmware-Core Agent
- `lookup_hal_function` - HAL documentation
- `get_init_sequence` - Configuration patterns
- `get_clock_config` - Clock tree setup
- `get_callback_code` - HAL callbacks

### Peripheral-Comm Agent
- `get_peripheral_docs` - Protocol capabilities
- `get_init_sequence` - Communication setup
- `get_dma_code` - DMA configurations
- `troubleshoot_error` - Protocol issues

### Debug Agent
- `troubleshoot_error` - Error diagnosis
- `get_register_info` - Register analysis
- `search_stm32_docs` - Fault investigation

### Bootloader Agent
- `search_stm32_docs` - Boot procedures
- `get_init_sequence` - Flash programming
- `get_code_examples` - IAP implementations

### Power-Management Agent
- `get_peripheral_docs` - Power controller
- `get_low_power_code` - Low-power modes
- `get_electrical_specifications` - Power consumption
- `troubleshoot_error` - Current issues

### Security Agent
- `search_stm32_docs` - Security features
- `get_peripheral_docs` - Crypto peripherals
- `get_code_examples` - Security implementations

### Safety-Certification Agent
- `search_stm32_docs` - Safety standards
- `get_code_examples` - Self-test implementations

### Hardware-Design Agent
- `search_stm32_docs` - Hardware guidelines
- `get_electrical_specifications` - Electrical specs
- `get_timing_specifications` - Timing requirements
- `troubleshoot_error` - Design problems

### Peripheral-Analog Agent
- `get_peripheral_docs` - ADC/DAC specs
- `get_init_sequence` - Analog configuration
- `get_electrical_specifications` - Accuracy specs
- `troubleshoot_error` - Accuracy issues

### Peripheral-Graphics Agent
- `get_peripheral_docs` - LTDC/DMA2D
- `get_init_sequence` - Display setup
- `get_timing_specifications` - Display timing
- `troubleshoot_error` - Display issues

---

## Response Pattern Template

All agents should follow this pattern when using MCP documentation:

```markdown
## Analysis
[Understanding of the query]

## Documentation Reference
Based on MCP documentation search:
- Source 1: Key finding
- Source 2: Relevant configuration

## Solution

### Configuration/Code
[From documentation with explanations]

### Implementation Notes
[Adaptations and best practices]

## Known Issues
[From errata or troubleshooting database]

## Testing Recommendations
[Verification steps]

## References
[Specific documents cited]
```

---

## MCP Tool Quick Reference Card

### Search Tools
```
search_stm32_docs(query, num_results?, peripheral?, require_code?)
get_peripheral_docs(peripheral, topic?, include_code?)
get_code_examples(topic, peripheral?, num_examples?)
get_register_info(register_name)
list_peripherals()
```

### HAL Tools
```
search_hal_function(function_name)
lookup_hal_function(function_name)
```

### Init Tools
```
get_init_sequence(peripheral, use_case?)
get_init_template(peripheral, mode?)
get_clock_config(target_frequency?, clock_source?)
```

### Example Tools
```
get_interrupt_code(peripheral, interrupt_type?)
get_dma_code(peripheral, direction?)
get_callback_code(peripheral, callback_type?)
get_low_power_code(mode?)
```

### Debug Tools
```
troubleshoot_error(error_description, peripheral?)
```

### Compare/Migrate Tools
```
compare_peripheral_options(peripheral1, peripheral2, aspect?)
get_migration_guide(from_family, to_family, peripheral?)
```

### Spec Tools
```
get_electrical_specifications(topic)
get_timing_specifications(peripheral, timing_type?)
```

---

## Adding MCP Support to New Agents

When creating new agents, include the MCP integration section:

1. List primary MCP tools for the domain
2. Define documentation workflow for common queries
3. Create topic-specific query tables
4. Include example workflows with actual tool calls
5. Define response pattern with documentation citations
6. Add fallback instructions for when tools are unavailable

Reference the `_mcp_template.md` file for the standard template structure.
