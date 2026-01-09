# STM32 MCP Server - Quick Start

Quick reference for the STM32 MCP Documentation Server.

## Installation

```bash
# One command installs everything
claude mcp add stm32-docs --scope user -- uvx --from git+https://TOKEN@github.com/creativec09/stm32-agents.git stm32-mcp-docs
```

Replace `TOKEN` with your GitHub Personal Access Token.

## What Auto-Installs

On first run (takes 5-10 minutes):
- **16 agents** -> `~/.claude/agents/`
- **Vector database** (13,815 chunks) from 80 bundled docs
- **Marker files** prevent re-installation

## Slash Commands

```
/stm32 <query>           - Search STM32 documentation
/stm32-init <peripheral> - Get initialization code
/stm32-hal <function>    - HAL function lookup
/stm32-debug <issue>     - Troubleshooting help
```

## Example Queries

### General Documentation
```
/stm32 How to configure UART with DMA?
/stm32 GPIO interrupt setup
/stm32 ADC continuous conversion mode
```

### Initialization Code
```
/stm32-init UART
/stm32-init SPI master DMA mode
/stm32-init TIM PWM output
/stm32-init ADC continuous conversion
```

### HAL Function Lookup
```
/stm32-hal HAL_GPIO_Init
/stm32-hal HAL_UART_Transmit_DMA
/stm32-hal HAL_SPI_TransmitReceive
```

### Debugging
```
/stm32-debug UART not receiving data
/stm32-debug I2C HAL_TIMEOUT
/stm32-debug HardFault after DMA transfer
```

## Natural Language

Just ask questions naturally:
```
"Show me how to configure GPIO interrupts on STM32H7"
"Why is my I2C peripheral returning HAL_TIMEOUT?"
"How to enter Stop mode and wake up on UART?"
```

## MCP Tools (15+)

| Tool | Description |
|------|-------------|
| `search_stm32_docs` | Semantic search |
| `get_peripheral_docs` | Peripheral docs |
| `get_code_examples` | Code examples |
| `get_register_info` | Register docs |
| `lookup_hal_function` | HAL function lookup |
| `troubleshoot_error` | Error troubleshooting |
| `get_init_sequence` | Init code |
| `get_clock_config` | Clock config |
| `compare_peripheral_options` | Compare peripherals |
| `get_migration_guide` | Migration guides |
| `get_interrupt_code` | Interrupt examples |
| `get_dma_code` | DMA examples |
| `get_low_power_code` | Low power modes |
| `get_callback_code` | HAL callbacks |
| `get_init_template` | Init templates |
| `list_peripherals` | List peripherals |

## Agents (16)

| Category | Agents |
|----------|--------|
| Routing | router, triage |
| Firmware | firmware, firmware-core |
| Debugging | debug |
| Bootloader | bootloader, bootloader-programming |
| Peripherals | peripheral-comm, peripheral-analog, peripheral-graphics |
| Power | power, power-management |
| Safety | safety, safety-certification |
| Security | security |
| Hardware | hardware-design |

## Troubleshooting

### No results
Wait for first-run ingestion (5-10 min), or:
```bash
python scripts/ingest_docs.py --clear
```

### Slow first query
First query builds database. Subsequent queries are fast (<100ms).

### Check installation
```bash
claude mcp list
claude mcp status stm32-docs
```

## More Information

- [Getting Started](GETTING_STARTED.md) - Full setup guide
- [Claude Code Integration](CLAUDE_CODE_INTEGRATION.md) - Integration details
- [MCP Server](MCP_SERVER.md) - Server documentation
- [Agent Quick Reference](AGENT_QUICK_REFERENCE.md) - Agent capabilities
