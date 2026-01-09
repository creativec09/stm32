---
name: stm32-hal
description: Look up STM32 HAL function documentation
---

# STM32 HAL Function Lookup

Get documentation for HAL/LL library functions.

## Usage

```
/stm32-hal <function_name>
```

## Examples

```
/stm32-hal HAL_UART_Transmit
/stm32-hal HAL_SPI_TransmitReceive_DMA
/stm32-hal HAL_GPIO_Init
/stm32-hal HAL_TIM_PWM_Start
/stm32-hal LL_GPIO_SetPinMode
```

## What This Does

Uses `lookup_hal_function` tool to find:
- Function signature and parameters
- Return values and error codes
- Usage examples
- Related functions
