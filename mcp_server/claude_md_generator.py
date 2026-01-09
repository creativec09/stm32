"""
CLAUDE.md Generator for STM32 MCP Server.

Generates and manages STM32 instructions for project CLAUDE.md files.
"""

from pathlib import Path
from typing import Optional


# Template content for CLAUDE.md STM32 section
STM32_CLAUDE_MD_TEMPLATE = '''
## STM32 Development Instructions

This project uses the STM32 MCP documentation server for embedded development assistance.

### IMPORTANT: Always Use MCP Tools for STM32 Questions

When answering ANY question about STM32 development:
1. **ALWAYS** search the documentation first using MCP tools
2. **NEVER** rely solely on training knowledge for STM32-specific details
3. **VERIFY** register names, function signatures, and configurations against docs

### Available MCP Tools (mcp__stm32-docs__*)

| Tool | When to Use | Example |
|------|-------------|---------|
| `search_stm32_docs` | General documentation search | `search_stm32_docs("UART DMA configuration")` |
| `get_peripheral_docs` | Peripheral-specific docs | `get_peripheral_docs("GPIO", topic="interrupt")` |
| `get_code_examples` | Find working code examples | `get_code_examples("SPI DMA", peripheral="SPI")` |
| `get_register_info` | Register and bit field details | `get_register_info("GPIO_MODER")` |
| `lookup_hal_function` | HAL/LL function documentation | `lookup_hal_function("HAL_UART_Transmit_DMA")` |
| `troubleshoot_error` | Debug issues and errors | `troubleshoot_error("I2C timeout", peripheral="I2C")` |
| `get_init_sequence` | Peripheral initialization | `get_init_sequence("ADC", use_case="continuous")` |
| `get_clock_config` | Clock tree configuration | `get_clock_config("168MHz", "HSE")` |
| `compare_peripheral_options` | Compare peripherals/modes | `compare_peripheral_options("SPI", "I2C")` |
| `get_migration_guide` | Migration between families | `get_migration_guide("STM32F4", "STM32H7")` |
| `get_interrupt_code` | Interrupt handling examples | `get_interrupt_code("TIM", interrupt_type="update")` |
| `get_dma_code` | DMA configuration examples | `get_dma_code("UART", direction="RX")` |
| `get_low_power_code` | Low power mode config | `get_low_power_code("Stop")` |
| `get_callback_code` | HAL callback implementations | `get_callback_code("SPI", callback_type="TxCplt")` |
| `get_init_template` | Complete init templates | `get_init_template("TIM", mode="PWM")` |
| `list_peripherals` | List documented peripherals | `list_peripherals()` |

### Available Slash Commands

| Command | Purpose | Example |
|---------|---------|---------|
| `/stm32` | Search STM32 documentation | `/stm32 How to configure UART with DMA` |
| `/stm32-init` | Get initialization code | `/stm32-init SPI master DMA mode` |
| `/stm32-hal` | Look up HAL function | `/stm32-hal HAL_GPIO_Init` |
| `/stm32-debug` | Troubleshoot an issue | `/stm32-debug I2C not responding` |
| `/stm32-setup` | Show setup status | `/stm32-setup --status` |

### Available STM32 Specialist Agents (16)

| Agent | Expertise Area | Use When |
|-------|----------------|----------|
| `router` | Query classification | First point of contact for ambiguous queries |
| `triage` | Initial analysis | Quick assessment of query type |
| `firmware` | General firmware | HAL/LL basics, project structure |
| `firmware-core` | Core peripherals | Timers, DMA, interrupts, GPIO |
| `debug` | Troubleshooting | HardFaults, debugging, trace |
| `bootloader` | Bootloader dev | IAP, DFU, system bootloader |
| `bootloader-programming` | Flash programming | Memory programming protocols |
| `peripheral-comm` | Communication | UART, SPI, I2C, CAN, USB, Ethernet |
| `peripheral-analog` | Analog circuits | ADC, DAC, OPAMP, comparators |
| `peripheral-graphics` | Display/Graphics | LTDC, DMA2D, DCMI, TouchGFX |
| `power` | Power optimization | Current measurement, optimization |
| `power-management` | Low power modes | Sleep, Stop, Standby, wakeup |
| `safety` | Safety critical | Self-tests, watchdogs, diagnostics |
| `safety-certification` | Certification | IEC 61508, ISO 26262, Class B |
| `security` | Security | Secure boot, TrustZone, crypto |
| `hardware-design` | Hardware | PCB, EMC, thermal, crystals |

### Query Best Practices

**Good queries (specific, contextual):**
```
/stm32 How to configure UART2 with DMA RX circular buffer on STM32F407?
/stm32-init ADC continuous conversion with DMA on PA0
/stm32-debug SPI returning wrong data order - MSB/LSB issue
```

**Poor queries (vague, missing context):**
```
/stm32 UART not working
/stm32-init timer
/stm32-debug my code doesn't work
```

### Workflow for STM32 Questions

1. **Identify the domain** - Peripheral, debugging, power, etc.
2. **Search documentation first** - Use appropriate MCP tool
3. **Get code examples** - Use `get_code_examples` or `get_init_sequence`
4. **Verify specifics** - Check register names, function signatures
5. **Provide complete answer** - Include all necessary configuration steps

### Important Notes

- Register names may vary between STM32 families (e.g., F4 vs H7)
- HAL library versions affect function availability
- Always verify clock enable for peripherals (RCC)
- Consider pin alternate function mapping for your specific chip
'''

# Marker to identify STM32 section in CLAUDE.md
STM32_SECTION_MARKER = "## STM32 Development Instructions"
STM32_END_MARKER = "<!-- END STM32 SECTION -->"


def get_stm32_claude_content() -> str:
    """
    Get the STM32 content for CLAUDE.md.

    Returns:
        The template content with end marker
    """
    return f"{STM32_CLAUDE_MD_TEMPLATE}\n{STM32_END_MARKER}\n"


def has_stm32_section(claude_md_path: Path) -> bool:
    """
    Check if CLAUDE.md already has STM32 section.

    Args:
        claude_md_path: Path to CLAUDE.md file

    Returns:
        True if STM32 section exists
    """
    if not claude_md_path.exists():
        return False

    content = claude_md_path.read_text(encoding="utf-8")
    return STM32_SECTION_MARKER in content


def update_claude_md(
    project_dir: Path,
    force: bool = False
) -> tuple[bool, str]:
    """
    Update or create CLAUDE.md with STM32 instructions.

    Args:
        project_dir: Project directory containing CLAUDE.md
        force: Force update even if section exists

    Returns:
        Tuple of (success, message)
    """
    claude_md_path = project_dir / "CLAUDE.md"
    stm32_content = get_stm32_claude_content()

    if claude_md_path.exists():
        existing_content = claude_md_path.read_text(encoding="utf-8")

        if has_stm32_section(claude_md_path):
            if not force:
                return True, "STM32 section already exists in CLAUDE.md"

            # Remove existing section and replace
            start_idx = existing_content.find(STM32_SECTION_MARKER)
            end_idx = existing_content.find(STM32_END_MARKER)

            if end_idx != -1:
                end_idx += len(STM32_END_MARKER)
                # Also remove trailing newlines
                while end_idx < len(existing_content) and existing_content[end_idx] == '\n':
                    end_idx += 1

                new_content = (
                    existing_content[:start_idx].rstrip() +
                    "\n\n" +
                    stm32_content +
                    existing_content[end_idx:]
                )
            else:
                # No end marker, just replace from start
                new_content = existing_content[:start_idx].rstrip() + "\n\n" + stm32_content

            claude_md_path.write_text(new_content, encoding="utf-8")
            return True, "Updated STM32 section in CLAUDE.md"
        else:
            # Append STM32 section
            new_content = existing_content.rstrip() + "\n\n" + stm32_content
            claude_md_path.write_text(new_content, encoding="utf-8")
            return True, "Added STM32 section to CLAUDE.md"
    else:
        # Create new CLAUDE.md
        header = f"# {project_dir.name} - Claude Code Project\n\n"
        claude_md_path.write_text(header + stm32_content, encoding="utf-8")
        return True, "Created CLAUDE.md with STM32 instructions"


def get_status_report(
    db_chunk_count: int,
    db_source: str,
    db_version: str
) -> str:
    """
    Generate a status report for /stm32-setup.

    Args:
        db_chunk_count: Number of chunks in database
        db_source: Source of database (downloaded, ingested, etc.)
        db_version: Version string

    Returns:
        Formatted status report
    """
    agents = [
        ("router", "Query classification and routing"),
        ("triage", "Initial query analysis"),
        ("firmware", "General firmware development"),
        ("firmware-core", "Core HAL/LL, timers, DMA, interrupts"),
        ("debug", "Debugging and troubleshooting"),
        ("bootloader", "Bootloader development"),
        ("bootloader-programming", "Bootloader programming protocols"),
        ("peripheral-comm", "UART, SPI, I2C, CAN, USB"),
        ("peripheral-analog", "ADC, DAC, OPAMP, comparators"),
        ("peripheral-graphics", "LTDC, DMA2D, DCMI, TouchGFX"),
        ("power", "Power optimization"),
        ("power-management", "Sleep, Stop, Standby modes"),
        ("safety", "Safety-critical development"),
        ("safety-certification", "IEC 61508, ISO 26262"),
        ("security", "Secure boot, TrustZone, crypto"),
        ("hardware-design", "PCB design, EMC, thermal"),
    ]

    commands = [
        ("/stm32 <query>", "Search STM32 documentation"),
        ("/stm32-init <peripheral>", "Get initialization code"),
        ("/stm32-hal <function>", "Look up HAL function"),
        ("/stm32-debug <issue>", "Troubleshoot an issue"),
        ("/stm32-setup", "Show setup status"),
    ]

    report = []
    report.append("=" * 60)
    report.append("STM32 MCP Server - Setup Status")
    report.append("=" * 60)
    report.append("")

    # Database status
    report.append("Database Status:")
    if db_chunk_count > 0:
        report.append(f"  Status: Ready")
        report.append(f"  Chunks: {db_chunk_count:,} document chunks indexed")
        report.append(f"  Source: {db_source}")
        report.append(f"  Version: {db_version}")
    else:
        report.append("  Status: Empty or not initialized")
        report.append("  Action: Run /stm32-setup to download database")

    report.append("")

    # Agents
    report.append(f"Available Agents ({len(agents)}):")
    for name, desc in agents:
        report.append(f"  - {name}: {desc}")

    report.append("")

    # Commands
    report.append("Available Commands:")
    for cmd, desc in commands:
        report.append(f"  - {cmd}: {desc}")

    report.append("")
    report.append("=" * 60)

    if db_chunk_count > 0:
        report.append("")
        report.append("Quick Start:")
        report.append("  Try: /stm32 How do I configure UART with DMA?")
        report.append("  Or:  /stm32-init SPI master mode")

    return "\n".join(report)
