# STM32 Agent Quick Reference

## Agent Routing Summary

This document provides a quick reference for routing queries to the appropriate STM32 specialist agent.

---

## Agent Selection Table

| Agent | Primary Domain | Key Triggers | Example Query |
|-------|----------------|--------------|---------------|
| **Router** | Query classification, STM32 selection | "which STM32", "compare", "getting started" | "Which STM32 for battery sensor?" |
| **Firmware** | Core MCU programming | timer, clock, DMA, interrupt, HAL, RTOS | "Timer interrupt not firing" |
| **Peripheral-Comm** | Serial protocols | UART, SPI, I2C, CAN, USB, Ethernet | "UART receiving garbage" |
| **Peripheral-Analog** | Analog/Audio | ADC, DAC, SAI, audio, sensor, DSP | "ADC readings are noisy" |
| **Peripheral-Graphics** | Display/Camera | LTDC, DMA2D, DCMI, TouchGFX, LVGL | "Display tearing issue" |
| **Hardware** | PCB/Circuit design | PCB, EMC, thermal, crystal, decoupling | "Decoupling for STM32H7" |
| **Security** | Secure boot/Crypto | encryption, TrustZone, RNG, tamper, RDP | "Implement secure boot" |
| **Safety** | Functional safety | SIL, ASIL, IEC 60730, self-test, STL | "Class B certification" |
| **Power** | Low-power modes | sleep, stop, standby, battery, wakeup | "Enter Stop 2 mode" |
| **Bootloader** | Firmware updates | IAP, DFU, boot mode, option bytes | "Custom bootloader jump" |
| **Debug** | Fault analysis | HardFault, SWD, trace, crash, GDB | "HardFault diagnosis" |

---

## Routing Decision Flowchart

```
                        User Query
                            |
                            v
                   +------------------+
                   | Extract Keywords |
                   +------------------+
                            |
            +---------------+---------------+
            |               |               |
            v               v               v
      +-----------+   +-----------+   +-----------+
      | Hardware? |   | Software? |   | Debug?    |
      | PCB, EMC, |   | Code,     |   | Fault,    |
      | thermal   |   | config    |   | crash     |
      +-----------+   +-----------+   +-----------+
            |               |               |
            v               |               v
       Hardware             |            Debug
         Agent              |            Agent
                            |
            +-------+-------+-------+
            |       |       |       |
            v       v       v       v
         Comm?   Analog? Graphics? Core?
            |       |       |       |
            v       v       v       v
         Periph   Periph  Periph  Firmware
         Comm     Analog  Graph    Agent
```

---

## Keyword Priority Rules

When multiple domains match, use these priority rules:

### 1. Debug Takes Priority for Crashes
Any query with "HardFault", "crash", "exception", "freeze" goes to **Debug Agent** first.

### 2. Safety Override for Certification
Queries mentioning "SIL", "ASIL", "IEC 60730", "Class B" go to **Safety Agent**.

### 3. Security Override for Protection
Queries about "secure boot", "encryption", "TrustZone" go to **Security Agent**.

### 4. End-Goal Rule
Route to the agent handling the final objective:
- "DMA for UART" -> **Peripheral-Comm** (UART is the goal)
- "Timer for ADC" -> **Peripheral-Analog** (ADC is the goal)

### 5. Specificity Rule
More specific domain wins over general domain:
- "SPI configuration" -> **Peripheral-Comm** (not Firmware)
- "DAC waveform" -> **Peripheral-Analog** (not Firmware)

---

## Common Collaboration Patterns

| Query Type | Primary Agent | Collaborator(s) |
|------------|---------------|-----------------|
| DMA + Peripheral | Peripheral-* | Firmware |
| Secure bootloader | Security | Bootloader |
| Low-power UART wakeup | Power | Peripheral-Comm |
| SPI display | Peripheral-Graphics | Peripheral-Comm |
| Safety watchdog | Safety | Firmware |
| Timer-triggered ADC | Peripheral-Analog | Firmware |
| Ethernet + RTOS | Peripheral-Comm | Firmware |
| Camera + USB | Peripheral-Graphics | Peripheral-Comm |

---

## Ambiguous Query Resolution

### When to Ask for Clarification

1. **Generic terms**: "problem", "not working", "issue" without context
2. **Multiple valid domains**: Query could reasonably go to 2+ agents
3. **Missing context**: No STM32 model or peripheral specified
4. **Confidence < 50%**: Keyword matching score below threshold

### Clarification Templates

**Domain Clarification:**
```
To help you better, could you clarify:
- Are you asking about [hardware design] or [software configuration]?
- What is your main goal with this feature?
```

**Context Gathering:**
```
I can help with that. To give you the best answer:
- Which STM32 series/part number are you using?
- What have you tried so far?
- What symptoms or errors are you seeing?
```

---

## Agent File Location

All agent definition files are located in:
```
.claude/agents/
├── router.md           # Query routing and classification
├── firmware.md         # Core MCU programming
├── peripheral-comm.md  # Communication protocols
├── peripheral-analog.md # Analog and audio
├── peripheral-graphics.md # Display and camera
├── hardware.md         # PCB and circuit design
├── security.md         # Security and encryption
├── safety.md           # Functional safety
├── power.md            # Power management
├── bootloader.md       # Firmware updates
└── debug.md            # Debugging and faults
```

---

## Confidence Scoring Quick Reference

| Score | Confidence | Action |
|-------|------------|--------|
| >= 100 | High | Route directly |
| 75-99 | Medium-High | Route, may suggest collaboration |
| 50-74 | Medium | Route with collaboration flag |
| 25-49 | Low | Request clarification |
| < 25 | Very Low | Router handles or asks for details |

---

## Quick Keyword Lookup

### Route to Firmware
`clock`, `PLL`, `timer`, `TIM`, `PWM`, `interrupt`, `NVIC`, `DMA`, `HAL`, `LL`, `FreeRTOS`, `GPIO`, `EXTI`, `cache`, `MPU`, `watchdog`

### Route to Peripheral-Comm
`UART`, `USART`, `SPI`, `I2C`, `CAN`, `FDCAN`, `USB`, `Ethernet`, `baud`, `MOSI`, `SCL`, `CDC`, `HID`

### Route to Peripheral-Analog
`ADC`, `DAC`, `analog`, `SAI`, `I2S`, `audio`, `sensor`, `DFSDM`, `FFT`, `filter`, `DSP`, `CMSIS-DSP`

### Route to Peripheral-Graphics
`LTDC`, `LCD`, `display`, `DMA2D`, `DCMI`, `camera`, `TouchGFX`, `LVGL`, `framebuffer`

### Route to Hardware
`PCB`, `schematic`, `EMC`, `ESD`, `thermal`, `crystal`, `decoupling`, `impedance`, `layout`

### Route to Security
`secure boot`, `encryption`, `AES`, `TrustZone`, `RNG`, `tamper`, `RDP`, `CRYP`, `PKA`

### Route to Safety
`SIL`, `ASIL`, `IEC 60730`, `self-test`, `STL`, `Class B`, `diagnostic coverage`, `FMEA`

### Route to Power
`sleep`, `stop`, `standby`, `low power`, `battery`, `wakeup`, `voltage scaling`, `VOS`

### Route to Bootloader
`bootloader`, `IAP`, `DFU`, `flash programming`, `option bytes`, `dual bank`, `VTOR`

### Route to Debug
`HardFault`, `crash`, `SWD`, `JTAG`, `breakpoint`, `trace`, `ITM`, `GDB`, `fault`
