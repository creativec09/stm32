# Agent MCP Integration Documentation

This document describes how STM32 specialized agents integrate with the MCP documentation server to provide accurate, up-to-date responses based on official STM32 documentation.

## Overview

All STM32 agents are configured to query the `stm32-docs` MCP server before responding to user queries. This ensures:

- **Accuracy**: Responses are based on official documentation
- **Currency**: Latest HAL patterns and API usage
- **Completeness**: Includes errata, workarounds, and known issues
- **Consistency**: All agents use the same documentation source

## Architecture

```
User Query
    |
    v
+------------------+
|   Triage Agent   | <-- mcp__stm32-docs__search_stm32_docs (context gathering)
+------------------+
    |
    v (routed with documentation context)
+------------------+
| Specialist Agent | <-- mcp__stm32-docs__<specific_tools>
+------------------+
    |
    v
Documentation-backed Response
```

## How Agents Use MCP Tools

### 1. Triage Agent

The triage agent uses MCP tools to gather context before routing:

```
mcp__stm32-docs__search_stm32_docs(query)        # Understand the domain
mcp__stm32-docs__troubleshoot_error(symptom)    # Categorize issues
```

This helps determine which specialist agent should handle the query and provides initial context.

### 2. Specialist Agents

Each specialist agent uses domain-specific MCP tools:

| Agent | Primary Tools |
|-------|--------------|
| firmware-core | `lookup_hal_function`, `get_init_sequence`, `get_clock_config` |
| peripheral-comm | `get_peripheral_docs`, `get_init_sequence`, `get_code_examples` |
| debug | `troubleshoot_error`, `get_errata`, `get_register_info` |
| bootloader | `search_stm32_docs`, `get_code_examples`, `get_init_sequence` |
| power-management | `get_peripheral_docs`, `get_init_sequence`, `troubleshoot_error` |
| security | `get_peripheral_docs`, `get_code_examples`, `search_stm32_docs` |
| safety | `search_stm32_docs`, `get_code_examples`, `get_init_sequence` |
| hardware-design | `search_stm32_docs`, `get_errata`, `troubleshoot_error` |
| peripheral-analog | `get_peripheral_docs`, `get_init_sequence`, `troubleshoot_error` |
| peripheral-graphics | `get_peripheral_docs`, `get_init_sequence`, `troubleshoot_error` |

## MCP Tool Reference

### search_stm32_docs

General semantic search across all documentation.

```
mcp__stm32-docs__search_stm32_docs("UART DMA configuration")
mcp__stm32-docs__search_stm32_docs("timer interrupt", peripheral="TIM")
```

### get_peripheral_docs

Get comprehensive documentation for a specific peripheral.

```
mcp__stm32-docs__get_peripheral_docs("UART")
mcp__stm32-docs__get_peripheral_docs("ADC")
```

### get_code_examples

Find code examples for specific topics.

```
mcp__stm32-docs__get_code_examples("PWM generation", peripheral="TIM")
mcp__stm32-docs__get_code_examples("DMA circular buffer")
```

### lookup_hal_function

Get HAL/LL function documentation.

```
mcp__stm32-docs__lookup_hal_function("HAL_TIM_PWM_Start")
mcp__stm32-docs__lookup_hal_function("LL_GPIO_SetOutputPin")
```

### troubleshoot_error

Find solutions for common errors.

```
mcp__stm32-docs__troubleshoot_error("UART receiving garbage", peripheral="UART")
mcp__stm32-docs__troubleshoot_error("HardFault after DMA")
```

### get_init_sequence

Get initialization code sequences.

```
mcp__stm32-docs__get_init_sequence("SPI", "DMA master mode")
mcp__stm32-docs__get_init_sequence("ADC", "continuous conversion")
```

### get_clock_config

Get clock configuration guidance.

```
mcp__stm32-docs__get_clock_config("168MHz", "HSE")
mcp__stm32-docs__get_clock_config("480MHz", "HSE 25MHz")
```

### get_migration_guide

Get migration information between STM32 families.

```
mcp__stm32-docs__get_migration_guide("STM32F4", "STM32H7")
```

### get_register_info

Get register-level documentation.

```
mcp__stm32-docs__get_register_info("USART_CR1")
mcp__stm32-docs__get_register_info("RCC_CFGR")
```

### get_errata

Get known errata and workarounds.

```
mcp__stm32-docs__get_errata("STM32H743", "I2C")
mcp__stm32-docs__get_errata("STM32F4")
```

### list_peripherals

List available peripherals for a family.

```
mcp__stm32-docs__list_peripherals("STM32H7")
```

### compare_peripheral_options

Compare peripheral configurations or options.

```
mcp__stm32-docs__compare_peripheral_options("ADC modes")
```

## Best Practices for Documentation Search

### 1. Search Before Responding

All agents should search documentation before providing technical answers:

```
# Good workflow
1. Receive user question
2. Search relevant documentation
3. Synthesize answer from docs + expertise
4. Cite sources in response

# Not recommended
1. Receive user question
2. Answer from general knowledge only
```

### 2. Use Appropriate Tools

Select the right tool for the query type:

| Query Type | Tool |
|------------|------|
| "How to configure X" | `get_init_sequence` |
| "X not working" | `troubleshoot_error` |
| "What does HAL_X do" | `lookup_hal_function` |
| "Show example of X" | `get_code_examples` |
| "Register X meaning" | `get_register_info` |
| "Known issues with X" | `get_errata` |

### 3. Chain Multiple Tools

For complex queries, use multiple tools:

```
1. get_peripheral_docs("UART")           # Overview
2. get_init_sequence("UART", "DMA")     # Configuration
3. get_code_examples("UART DMA")        # Examples
4. get_errata("<family>", "UART")       # Known issues
```

### 4. Include Context in Searches

Provide specific context for better results:

```
# Good - specific
mcp__stm32-docs__troubleshoot_error("I2C bus busy stuck", peripheral="I2C")

# Less specific
mcp__stm32-docs__search_stm32_docs("I2C problem")
```

### 5. Cite Documentation Sources

Always reference documentation in responses:

```markdown
## Documentation Reference
Based on:
- [RM0433]: UART DMA configuration (Section 12.4)
- [AN4031]: DMA best practices
- [Code examples]: UART_DMA_Receive
```

## Example Workflows

### Configuration Question

```
User: "How do I configure UART2 for DMA receive?"

Agent workflow:
1. mcp__stm32-docs__get_peripheral_docs("UART")
2. mcp__stm32-docs__get_init_sequence("UART", "DMA receive")
3. mcp__stm32-docs__get_code_examples("UART DMA receive")
4. mcp__stm32-docs__lookup_hal_function("HAL_UART_Receive_DMA")

Response includes:
- Peripheral overview from docs
- Proper initialization sequence
- Working code example
- HAL function usage
```

### Debugging Question

```
User: "UART receiving corrupted data"

Agent workflow:
1. mcp__stm32-docs__troubleshoot_error("UART corrupted data", peripheral="UART")
2. mcp__stm32-docs__search_stm32_docs("UART baud rate calculation")
3. mcp__stm32-docs__get_errata("<family>", "UART")

Response includes:
- Common causes from troubleshooting database
- Configuration verification steps
- Known errata if applicable
```

### HAL Function Question

```
User: "What parameters does HAL_ADC_Start_DMA take?"

Agent workflow:
1. mcp__stm32-docs__lookup_hal_function("HAL_ADC_Start_DMA")
2. mcp__stm32-docs__get_code_examples("ADC DMA")

Response includes:
- Function signature
- Parameter descriptions
- Return values
- Usage example
```

## Adding MCP Support to New Agents

When creating a new specialist agent:

1. **Include MCP integration section** in the agent definition
2. **List primary tools** for the domain
3. **Define documentation workflow** for common query types
4. **Create topic-specific query table** for quick reference
5. **Include example workflows** demonstrating tool usage
6. **Define response pattern** that includes documentation citations

Reference the template file:
- `/mnt/c/Users/creat/Claude/stm32-agents/.claude/agents/_mcp_template.md`

Reference the guide file:
- `/mnt/c/Users/creat/Claude/stm32-agents/.claude/agents/AGENTS_MCP_GUIDE.md`

## Troubleshooting MCP Integration

### Tool Not Returning Results

- Verify tool name spelling: `mcp__stm32-docs__<tool_name>`
- Check parameter names and values
- Try broader search terms

### Incomplete Documentation

- Use multiple tools to gather comprehensive information
- Combine peripheral docs + init sequence + code examples
- Search for related application notes

### Performance Considerations

- Cache results conceptually within a session
- Use specific queries rather than broad searches
- Chain tools efficiently (parallel when possible)

## Related Documentation

- [MCP_SERVER.md](MCP_SERVER.md) - MCP server implementation details
- [AGENT_QUICK_REFERENCE.md](AGENT_QUICK_REFERENCE.md) - Agent overview
- [AGENT_ROUTING_SPECIFICATION.md](AGENT_ROUTING_SPECIFICATION.md) - Query routing
