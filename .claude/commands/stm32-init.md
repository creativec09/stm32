---
name: stm32-init
description: Get initialization code for an STM32 peripheral
---

# STM32 Peripheral Initialization

Get complete initialization sequence for a peripheral.

## Usage

```
/stm32-init <peripheral> [use-case]
```

## Examples

```
/stm32-init UART
/stm32-init SPI DMA mode
/stm32-init ADC continuous conversion with interrupt
/stm32-init TIM PWM output
/stm32-init I2C master mode
```

## What This Does

Uses `get_init_sequence` tool with the peripheral and optional use case.

Returns complete HAL initialization code with:
- Required includes
- Handle declarations
- Init function implementation
- IRQ handlers if applicable
- DMA configuration if requested
