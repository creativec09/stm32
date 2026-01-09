---
name: stm32-debug
description: Debug an STM32 peripheral issue
---

# STM32 Debugging Assistant

Get help debugging STM32 peripheral issues.

## Usage

```
/stm32-debug <peripheral> <issue description>
```

## Examples

```
/stm32-debug UART not receiving data
/stm32-debug I2C HAL_TIMEOUT error
/stm32-debug SPI wrong data order
/stm32-debug ADC values stuck at 0
/stm32-debug DMA transfer not completing
```

## What This Does

1. Uses `troubleshoot_error` to find known issues and solutions
2. Uses `get_peripheral_docs` to verify configuration
3. Suggests common fixes based on documentation
