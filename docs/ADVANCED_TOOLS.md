# Advanced Search Tools

This document describes the advanced search tools available in the STM32 MCP Server for specialized development workflows.

## Overview

The advanced tools are organized into two categories:

1. **Search Tools** (`mcp_server/tools/search.py`) - Specialized search functionality for common STM32 development tasks
2. **Example Tools** (`mcp_server/tools/examples.py`) - Code example retrieval for specific patterns

## Search Tools

### lookup_hal_function

Look up documentation for a specific HAL/LL function.

**Parameters:**
- `function_name` (str, required): The HAL/LL function name

**Supported Patterns:**
- Standard HAL functions: `HAL_UART_Transmit`, `HAL_GPIO_Init`
- LL functions: `LL_GPIO_SetPinMode`, `LL_USART_Enable`
- Clock macros: `__HAL_RCC_GPIOA_CLK_ENABLE`
- DMA variants: `HAL_SPI_TransmitReceive_DMA`

**Examples:**
```
lookup_hal_function("HAL_UART_Transmit")
lookup_hal_function("HAL_SPI_TransmitReceive_DMA")
lookup_hal_function("LL_GPIO_SetPinMode")
lookup_hal_function("__HAL_RCC_GPIOA_CLK_ENABLE")
```

**Return Format:**
```
# HAL Function: HAL_UART_Transmit

## Result 1 (relevance: 0.85)
**Source**: stm32_hal_guide.md
**Peripheral**: UART
**Section**: UART > Functions
**Contains code examples**

[Function documentation content...]

---
```

---

### troubleshoot_error

Search for solutions to STM32 errors and issues.

**Parameters:**
- `error_description` (str, required): Description of the error or symptom
- `peripheral` (str, optional): Peripheral to focus the search

**Supported Error Types:**
- HAL errors: `HAL_TIMEOUT`, `HAL_ERROR`, `HAL_BUSY`
- Faults: `HardFault`, `BusFault`, `UsageFault`
- Communication errors: "UART not receiving", "SPI transfer fails"
- Configuration issues: "clock not working", "interrupt not firing"

**Examples:**
```
troubleshoot_error("UART not receiving data")
troubleshoot_error("HAL_TIMEOUT error", peripheral="I2C")
troubleshoot_error("HardFault after DMA transfer")
troubleshoot_error("SPI communication fails intermittently")
```

**Return Format:**
Includes troubleshooting steps, common causes, and solutions from both main documentation and errata.

---

### get_init_sequence

Get complete initialization sequence for a peripheral.

**Parameters:**
- `peripheral` (str, required): The peripheral to initialize
- `use_case` (str, optional): Specific use case

**Supported Peripherals:**
GPIO, UART, USART, SPI, I2C, ADC, DAC, TIM, DMA, and more.

**Common Use Cases:**
- `"DMA mode"` - DMA-based transfers
- `"interrupt driven"` - Interrupt-based operation
- `"continuous conversion"` - Continuous mode (ADC)
- `"PWM output"` - PWM generation (TIM)
- `"master mode"` / `"slave mode"` - Communication role

**Examples:**
```
get_init_sequence("UART")
get_init_sequence("SPI", use_case="DMA master mode")
get_init_sequence("ADC", use_case="continuous conversion")
get_init_sequence("TIM", use_case="PWM output")
```

**Return Format:**
Returns complete initialization code including clock enable, GPIO configuration, and peripheral setup.

---

### get_clock_config

Get clock configuration documentation.

**Parameters:**
- `target_frequency` (str, optional): Target system clock (e.g., "168MHz", "480MHz")
- `clock_source` (str, optional): Clock source (HSE, HSI, PLL, LSE, LSI)

**Examples:**
```
get_clock_config("168MHz", "HSE")
get_clock_config("480MHz")
get_clock_config(clock_source="PLL")
get_clock_config("84MHz", "HSI")
```

**Return Format:**
Returns clock tree configuration code including PLL settings and prescaler values.

---

### compare_peripheral_options

Compare two peripherals or modes.

**Parameters:**
- `peripheral1` (str, required): First peripheral
- `peripheral2` (str, required): Second peripheral
- `aspect` (str, optional): Comparison aspect (speed, power, features)

**Common Comparisons:**
- `UART` vs `USART` - Feature differences
- `SPI` vs `I2C` - Speed and use cases
- `DMA` vs `BDMA` vs `MDMA` - DMA controller variants
- `ADC` vs `DAC` - Analog peripheral differences

**Examples:**
```
compare_peripheral_options("UART", "USART")
compare_peripheral_options("SPI", "I2C", aspect="speed")
compare_peripheral_options("DMA", "BDMA")
```

---

### get_migration_guide

Get migration information between STM32 families.

**Parameters:**
- `from_family` (str, required): Source family (e.g., "STM32F4")
- `to_family` (str, required): Target family (e.g., "STM32H7")
- `peripheral` (str, optional): Specific peripheral focus

**Supported Families:**
STM32F0, STM32F1, STM32F2, STM32F3, STM32F4, STM32F7, STM32G0, STM32G4, STM32H5, STM32H7, STM32L0, STM32L1, STM32L4, STM32L5, STM32U5, STM32WB, STM32WL

**Examples:**
```
get_migration_guide("STM32F4", "STM32H7")
get_migration_guide("STM32F7", "STM32H7", peripheral="DMA")
get_migration_guide("STM32F1", "STM32G4", peripheral="ADC")
```

**Return Format:**
Returns migration considerations, register differences, API changes, and code modifications needed.

---

### get_electrical_specifications

Search for electrical specifications.

**Parameters:**
- `topic` (str, required): The specification topic

**Common Topics:**
- "GPIO drive strength"
- "ADC input impedance"
- "power consumption sleep mode"
- "operating voltage range"
- "operating temperature"
- "timing specifications"

**Examples:**
```
get_electrical_specifications("GPIO drive strength")
get_electrical_specifications("ADC input impedance")
get_electrical_specifications("power consumption sleep mode")
```

---

### get_timing_specifications

Search for timing specifications.

**Parameters:**
- `peripheral` (str, required): Peripheral to search
- `timing_type` (str, optional): Specific timing type

**Timing Types:**
- `"setup hold"` - Setup and hold times
- `"clock frequency"` - Supported clock rates
- `"baud rate"` - Communication speeds
- `"latency"` - Response times

**Examples:**
```
get_timing_specifications("SPI", "clock frequency")
get_timing_specifications("I2C", "setup hold")
get_timing_specifications("UART", "baud rate")
```

---

## Code Example Tools

### get_interrupt_code

Get interrupt handling examples.

**Parameters:**
- `peripheral` (str, required): Peripheral name
- `interrupt_type` (str, optional): Specific interrupt type

**Interrupt Types:**
- `"RXNE"` / `"RX"` - Receive interrupts
- `"TC"` / `"TX"` - Transmit complete
- `"update"` - Timer update
- `"capture"` / `"CC"` - Capture/compare
- `"error"` - Error interrupts
- `"DMA"` - DMA completion

**Examples:**
```
get_interrupt_code("UART")
get_interrupt_code("TIM", interrupt_type="update")
get_interrupt_code("EXTI", interrupt_type="rising edge")
```

---

### get_dma_code

Get DMA configuration examples.

**Parameters:**
- `peripheral` (str, required): Peripheral name
- `direction` (str, optional): Transfer direction (TX, RX, both)

**Examples:**
```
get_dma_code("UART")
get_dma_code("SPI", direction="TX")
get_dma_code("ADC", direction="RX")
get_dma_code("I2C", direction="both")
```

---

### get_low_power_code

Get low power mode examples.

**Parameters:**
- `mode` (str, optional): Low power mode

**Supported Modes:**
- `"Sleep"` - CPU stopped, peripherals running
- `"Stop"` - Most clocks stopped
- `"Standby"` - Lowest power, RAM lost
- `"Shutdown"` - Ultra-low power (if supported)

**Examples:**
```
get_low_power_code()
get_low_power_code("Sleep")
get_low_power_code("Stop")
get_low_power_code("Standby")
```

---

### get_callback_code

Get HAL callback function examples.

**Parameters:**
- `peripheral` (str, required): Peripheral name
- `callback_type` (str, optional): Callback type

**Callback Types:**
- `"TxCplt"` - Transmit complete
- `"RxCplt"` - Receive complete
- `"TxRxCplt"` - Full-duplex complete
- `"Error"` - Error callback
- `"HalfCplt"` - Half transfer
- `"Abort"` - Abort callback

**Examples:**
```
get_callback_code("UART")
get_callback_code("SPI", callback_type="TxRxCplt")
get_callback_code("I2C", callback_type="Error")
```

---

### get_init_template

Get complete peripheral initialization template.

**Parameters:**
- `peripheral` (str, required): Peripheral name
- `mode` (str, optional): Operating mode

**Common Modes:**
- `"master"` / `"slave"` - Communication role
- `"PWM"` - PWM output mode
- `"DMA"` - DMA mode
- `"blocking"` / `"polling"` - Blocking mode
- `"interrupt"` - Interrupt mode
- `"encoder"` - Encoder mode (TIM)

**Examples:**
```
get_init_template("SPI")
get_init_template("SPI", mode="master")
get_init_template("TIM", mode="PWM")
get_init_template("UART", mode="DMA")
```

---

## Best Practices

### 1. Start Broad, Then Narrow

Begin with general searches and refine based on results:

```
# Start with general peripheral docs
get_peripheral_docs("UART")

# Then get specific init sequence
get_init_sequence("UART", use_case="DMA mode")

# Finally, look up specific functions
lookup_hal_function("HAL_UART_Receive_DMA")
```

### 2. Use Troubleshooting for Issues

When debugging, use the troubleshoot_error tool:

```
# Describe the symptom
troubleshoot_error("UART receive buffer overflow", peripheral="UART")

# Check for errata
troubleshoot_error("I2C BUSY flag stuck", peripheral="I2C")
```

### 3. Combine Tools for Migration

When migrating between families:

```
# Get migration overview
get_migration_guide("STM32F4", "STM32H7")

# Check specific peripheral differences
get_migration_guide("STM32F4", "STM32H7", peripheral="DMA")

# Compare peripheral implementations
compare_peripheral_options("DMA", "BDMA")
```

### 4. Use Code Examples for Implementation

For implementation guidance:

```
# Get initialization template
get_init_template("SPI", mode="DMA master")

# Get interrupt handling
get_interrupt_code("SPI", interrupt_type="TxRx")

# Get callback implementation
get_callback_code("SPI", callback_type="TxRxCplt")
```

---

## Tool Summary Table

| Tool | Purpose | Key Parameters |
|------|---------|----------------|
| `lookup_hal_function` | HAL/LL function docs | `function_name` |
| `troubleshoot_error` | Error solutions | `error_description`, `peripheral` |
| `get_init_sequence` | Init sequences | `peripheral`, `use_case` |
| `get_clock_config` | Clock configuration | `target_frequency`, `clock_source` |
| `compare_peripheral_options` | Compare peripherals | `peripheral1`, `peripheral2`, `aspect` |
| `get_migration_guide` | Migration info | `from_family`, `to_family`, `peripheral` |
| `get_electrical_specifications` | Electrical specs | `topic` |
| `get_timing_specifications` | Timing specs | `peripheral`, `timing_type` |
| `get_interrupt_code` | Interrupt examples | `peripheral`, `interrupt_type` |
| `get_dma_code` | DMA examples | `peripheral`, `direction` |
| `get_low_power_code` | Low power examples | `mode` |
| `get_callback_code` | Callback examples | `peripheral`, `callback_type` |
| `get_init_template` | Init templates | `peripheral`, `mode` |

---

## Architecture

### Module Structure

```
mcp_server/
  tools/
    __init__.py      # Package exports
    search.py        # Advanced search functions
    examples.py      # Code example functions
  server.py          # MCP tool wrappers
```

### Data Flow

1. MCP client calls tool (e.g., `lookup_hal_function`)
2. Server wrapper in `server.py` receives call
3. Wrapper calls implementation in `tools/search.py` or `tools/examples.py`
4. Implementation queries `STM32ChromaStore` with appropriate filters
5. Results are formatted and returned to client

### Search Strategy

Each tool uses a multi-stage search strategy:

1. **Primary search** with specific filters (doc_type, peripheral, require_code)
2. **Secondary search** with relaxed filters if primary yields few results
3. **Fallback search** with minimal filters as last resort
4. **Deduplication** to remove similar results
5. **Ranking** by relevance score
