# MCP Documentation Tools Template

This template provides the standard MCP documentation tools interface for STM32 specialized agents. Copy the relevant sections to new agent files.

## MCP Documentation Server

All STM32 agents have access to the `stm32-docs` MCP server for documentation retrieval.

- **Server Name**: `stm32-docs`
- **Tool Pattern**: `mcp__stm32-docs__<tool_name>`
- **Resource Pattern**: `stm32://<resource_path>`

---

## Complete Tool Reference

### Core Search Tools

| Tool | Parameters | Return Type | Description |
|------|------------|-------------|-------------|
| `search_stm32_docs` | `query` (str), `num_results` (int=5), `peripheral` (str?), `require_code` (bool=False) | Markdown with scores | Semantic search across all docs |
| `get_peripheral_docs` | `peripheral` (str), `topic` (str?), `include_code` (bool=True) | Markdown sections | Comprehensive peripheral docs |
| `get_code_examples` | `topic` (str), `peripheral` (str?), `num_examples` (int=3) | Code with sources | Find code examples |
| `get_register_info` | `register_name` (str) | Register details | Register bit fields and config |
| `list_peripherals` | None | Peripheral list | List peripherals with doc counts |

### HAL/LL Function Tools

| Tool | Parameters | Return Type | Description |
|------|------------|-------------|-------------|
| `search_hal_function` | `function_name` (str) | Function docs | Search HAL/LL documentation |
| `lookup_hal_function` | `function_name` (str) | Detailed docs | Enhanced lookup with context |

### Initialization Tools

| Tool | Parameters | Return Type | Description |
|------|------------|-------------|-------------|
| `get_init_sequence` | `peripheral` (str), `use_case` (str?) | Init code | Complete initialization sequence |
| `get_init_template` | `peripheral` (str), `mode` (str?) | Full template | Comprehensive init template |
| `get_clock_config` | `target_frequency` (str?), `clock_source` (str?) | Clock config | Clock tree configuration |

### Code Example Tools

| Tool | Parameters | Return Type | Description |
|------|------------|-------------|-------------|
| `get_interrupt_code` | `peripheral` (str), `interrupt_type` (str?) | Interrupt code | Interrupt handling examples |
| `get_dma_code` | `peripheral` (str), `direction` (str: TX/RX/both?) | DMA code | DMA configuration examples |
| `get_callback_code` | `peripheral` (str), `callback_type` (str?) | Callback code | HAL callback implementations |
| `get_low_power_code` | `mode` (str: Sleep/Stop/Standby?) | Power code | Low power mode examples |

### Troubleshooting Tools

| Tool | Parameters | Return Type | Description |
|------|------------|-------------|-------------|
| `troubleshoot_error` | `error_description` (str), `peripheral` (str?) | Solutions | Error solutions and fixes |

### Comparison/Migration Tools

| Tool | Parameters | Return Type | Description |
|------|------------|-------------|-------------|
| `compare_peripheral_options` | `peripheral1` (str), `peripheral2` (str), `aspect` (str?) | Comparison | Compare peripherals/modes |
| `get_migration_guide` | `from_family` (str), `to_family` (str), `peripheral` (str?) | Migration info | Family migration guidance |

### Specification Tools

| Tool | Parameters | Return Type | Description |
|------|------------|-------------|-------------|
| `get_electrical_specifications` | `topic` (str) | Electrical specs | Electrical characteristics |
| `get_timing_specifications` | `peripheral` (str), `timing_type` (str?) | Timing specs | Timing requirements |

---

## MCP Resources

Access documentation content directly via URI patterns.

| Resource URI | Description |
|--------------|-------------|
| `stm32://peripherals` | List all documented peripherals |
| `stm32://peripherals/{peripheral}` | Peripheral overview |
| `stm32://peripherals/{peripheral}/overview` | Comprehensive overview |
| `stm32://peripherals/{peripheral}/registers` | Register documentation |
| `stm32://peripherals/{peripheral}/examples` | Code examples |
| `stm32://peripherals/{peripheral}/interrupts` | Interrupt documentation |
| `stm32://peripherals/{peripheral}/dma` | DMA configuration |
| `stm32://hal-functions` | List all HAL functions |
| `stm32://hal-functions/{peripheral}` | HAL functions for peripheral |
| `stm32://sources` | Documentation source files |
| `stm32://documents/{doc_type}` | Documents by type |
| `stm32://stats` | Database statistics |
| `stm32://health` | Server health status |

### Resource Usage

```python
# List peripherals
ReadMcpResourceTool(server="stm32-docs", uri="stm32://peripherals")

# Get peripheral overview
ReadMcpResourceTool(server="stm32-docs", uri="stm32://peripherals/UART")

# Get register docs
ReadMcpResourceTool(server="stm32-docs", uri="stm32://peripherals/SPI/registers")
```

---

## Tool Usage Examples

### Search Examples

```python
# General search
mcp__stm32-docs__search_stm32_docs(
    query="UART DMA configuration",
    num_results=5
)

# Peripheral-filtered search
mcp__stm32-docs__search_stm32_docs(
    query="circular mode",
    peripheral="DMA",
    require_code=True
)

# Get peripheral docs
mcp__stm32-docs__get_peripheral_docs(
    peripheral="SPI",
    topic="DMA mode"
)
```

### HAL Function Examples

```python
# Basic lookup
mcp__stm32-docs__search_hal_function("HAL_GPIO_Init")

# Enhanced lookup
mcp__stm32-docs__lookup_hal_function("HAL_UART_Transmit_DMA")

# Macro lookup
mcp__stm32-docs__lookup_hal_function("__HAL_RCC_GPIOA_CLK_ENABLE")
```

### Initialization Examples

```python
# Basic init
mcp__stm32-docs__get_init_sequence("UART")

# With use case
mcp__stm32-docs__get_init_sequence("SPI", "DMA master mode")

# Full template
mcp__stm32-docs__get_init_template("TIM", "PWM")

# Clock config
mcp__stm32-docs__get_clock_config("168MHz", "HSE")
```

### Code Example Tools

```python
# Interrupt code
mcp__stm32-docs__get_interrupt_code("UART", "RXNE")

# DMA code
mcp__stm32-docs__get_dma_code("SPI", "TX")

# Callback code
mcp__stm32-docs__get_callback_code("I2C", "Error")

# Low power code
mcp__stm32-docs__get_low_power_code("Stop")
```

### Troubleshooting Examples

```python
# General error
mcp__stm32-docs__troubleshoot_error("UART receiving garbage")

# Peripheral-specific
mcp__stm32-docs__troubleshoot_error("HAL_TIMEOUT", peripheral="I2C")
```

### Migration/Comparison Examples

```python
# Compare peripherals
mcp__stm32-docs__compare_peripheral_options("SPI", "I2C", "speed")

# Migration guide
mcp__stm32-docs__get_migration_guide("STM32F4", "STM32H7", "DMA")
```

---

## Tool Selection Guidelines

| Query Type | Primary Tool | Fallback Tool |
|------------|--------------|---------------|
| "How to configure X" | `get_init_sequence` | `get_peripheral_docs` |
| "X not working" | `troubleshoot_error` | `search_stm32_docs` |
| "What does HAL_X do" | `lookup_hal_function` | `search_hal_function` |
| "Example of X" | `get_code_examples` | `search_stm32_docs` (require_code=True) |
| "Register X meaning" | `get_register_info` | Resource: `stm32://peripherals/{p}/registers` |
| "Migrate from X to Y" | `get_migration_guide` | `compare_peripheral_options` |
| "Interrupt handling" | `get_interrupt_code` | `get_callback_code` |
| "DMA setup" | `get_dma_code` | `get_init_sequence` (use_case="DMA") |
| "Low power mode" | `get_low_power_code` | `search_stm32_docs` |
| "Electrical specs" | `get_electrical_specifications` | `search_stm32_docs` |

---

## Standard Workflow

1. **Understand Query** - Analyze what the user is asking
2. **Search Documentation** - Use appropriate MCP tool(s)
3. **Synthesize Answer** - Combine documentation with expertise
4. **Cite Sources** - Reference the documents used
5. **Provide Code** - Include working examples with explanations

---

## Fallback Instructions

### When MCP Server is Unavailable

```markdown
**Note**: The STM32 documentation server is currently unavailable.
I'll provide guidance based on general STM32 knowledge.

For verified documentation, please consult:
- ST Reference Manuals (RMxxxx)
- ST Application Notes (ANxxxx)
- STM32Cube HAL User Manual (UM1785)
- STM32 online documentation at st.com
```

### When No Results Found

1. **Broaden query**: Remove filters, use general terms
2. **Try alternative tool**: `search_stm32_docs` as fallback
3. **Check peripheral name**: UART vs USART, TIM vs TIMER
4. **Provide guidance with disclaimer**:

```markdown
**Note**: No specific documentation found.
Based on general STM32 knowledge:
[Your guidance]

Please verify with official ST documentation.
```

### Error Handling Pattern

```python
# Primary tool
result = mcp__stm32-docs__get_peripheral_docs("UART")

# Fallback if empty
if not result or "No documentation" in result:
    result = mcp__stm32-docs__search_stm32_docs("UART configuration")

# Resource fallback
if not result or "No documentation" in result:
    result = ReadMcpResourceTool(server="stm32-docs", uri="stm32://peripherals/UART")

# Final: general guidance with disclaimer
```

---

## Response Pattern Template

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
[Best practices and adaptations]

## Known Issues
[From troubleshooting/errata]

## Testing Recommendations
[Verification steps]

## References
[Specific documents cited]
```

---

## Example Workflows

### Configuration Question

```
User: "How do I configure UART for DMA receive?"

Workflow:
1. mcp__stm32-docs__get_init_sequence("UART", "DMA receive")
2. mcp__stm32-docs__get_dma_code("UART", "RX")
3. mcp__stm32-docs__get_callback_code("UART", "RxCplt")
4. Synthesize: Combine with best practices
5. Respond: Init code, DMA config, callback handling
```

### Debugging Question

```
User: "UART receiving garbage characters"

Workflow:
1. mcp__stm32-docs__troubleshoot_error("UART garbage characters")
2. mcp__stm32-docs__search_stm32_docs("UART baud rate mismatch")
3. mcp__stm32-docs__get_register_info("USART_BRR")
4. Analyze: Identify causes from docs
5. Respond: Systematic checklist with solutions
```

### HAL Function Question

```
User: "What parameters does HAL_ADC_Start_DMA take?"

Workflow:
1. mcp__stm32-docs__lookup_hal_function("HAL_ADC_Start_DMA")
2. mcp__stm32-docs__get_code_examples("ADC DMA")
3. Respond: Signature, parameters, return values, example
```

---

## Integration Notes

- Tools return structured markdown content
- Multiple tools can be called in sequence
- Always prefer documentation over general knowledge
- Use resources for direct content access
- Cite sources in every technical response
