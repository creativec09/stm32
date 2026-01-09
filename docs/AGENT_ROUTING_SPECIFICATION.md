# STM32 Agent Routing and Invocation Specification

## Document Overview

This specification defines the complete routing logic for the STM32 multi-agent system. It provides explicit rules for query classification, agent selection, collaboration protocols, and result synthesis.

---

## Table of Contents

1. [Routing Architecture Overview](#1-routing-architecture-overview)
2. [Agent Definitions and Triggers](#2-agent-definitions-and-triggers)
3. [Global Routing Decision Tree](#3-global-routing-decision-tree)
4. [Collaboration Protocols](#4-collaboration-protocols)
5. [Confidence Scoring System](#5-confidence-scoring-system)
6. [Edge Cases and Ambiguity Resolution](#6-edge-cases-and-ambiguity-resolution)

---

## 1. Routing Architecture Overview

### 1.1 System Flow

```
User Query
    |
    v
+-------------------+
| Router/Triage     |
| Agent             |
+-------------------+
    |
    +-- Classify query intent
    +-- Extract domain signals
    +-- Calculate confidence scores
    +-- Select primary agent(s)
    |
    v
+-------------------+     +-------------------+
| Primary Agent     |<--->| Secondary Agent   |
| (Specialist)      |     | (Collaborator)    |
+-------------------+     +-------------------+
    |
    v
+-------------------+
| Response          |
| Synthesis         |
+-------------------+
    |
    v
Final Response
```

### 1.2 Routing Principles

1. **Single Primary Agent**: Every query has exactly one primary agent owner
2. **Explicit Collaboration**: Secondary agents are invoked explicitly, not implicitly
3. **Confidence-Based Routing**: Queries below threshold trigger clarification
4. **Domain Boundaries**: Clear separation prevents overlap conflicts

---

## 2. Agent Definitions and Triggers

---

### 2.1 Router/Triage Agent

#### Agent Description (for agent file)
```yaml
description: |
  Primary entry point for all STM32 queries. Classifies user intent, extracts
  domain-specific signals, and routes to appropriate specialist agents. Handles
  meta-queries about the agent system itself, general STM32 family questions,
  and ambiguous queries requiring clarification.

  <examples>
  - "Which STM32 should I use for my project?" -> Router handles directly
  - "How do I configure the ADC?" -> Routes to Peripheral-Analog Agent
  - "I'm having issues with my board" -> Clarifies then routes appropriately
  </examples>

  <capabilities>
  - Query classification and intent extraction
  - Multi-domain query decomposition
  - Agent coordination and result synthesis
  - Clarification dialog management
  </capabilities>
```

#### Trigger Keywords and Phrases

**Positive Triggers (Handle Directly):**
- "which STM32", "what STM32", "recommend STM32", "STM32 selection"
- "compare STM32", "difference between STM32"
- "getting started", "new to STM32", "beginner"
- "overview", "introduction to STM32"
- "help me choose", "which series", "which family"

**Routing Triggers (Pass to Specialists):**
- Domain-specific keywords (see individual agents below)
- Technical implementation questions
- Debugging and troubleshooting with clear domain

**Meta Triggers (System Questions):**
- "how does this agent work", "what can you help with"
- "list capabilities", "what agents are available"

#### Example Queries - Handle Directly

1. "Which STM32 microcontroller should I use for a battery-powered sensor node?"
2. "What's the difference between STM32F4 and STM32H7 series?"
3. "I'm new to STM32 development. Where should I start?"
4. "Can you give me an overview of the STM32 ecosystem?"
5. "I need an MCU with USB, CAN, and at least 512KB flash. What do you recommend?"

#### Example Queries - Route to Specialists

1. "How do I configure Timer 2 in PWM mode?" -> Firmware Agent
2. "My SPI communication is dropping bytes" -> Peripheral-Comm Agent
3. "The ADC readings are noisy" -> Peripheral-Analog Agent
4. "How do I enter Stop mode?" -> Power Agent

#### Edge Cases

1. "STM32 problems" -> Clarify: "What specific issue are you experiencing?"
2. "Not working" -> Clarify: "Please describe what you're trying to do and what's happening"
3. "Best practices" -> Clarify: "Best practices for which aspect? (firmware, hardware, security, etc.)"

---

### 2.2 Firmware Agent

#### Agent Description (for agent file)
```yaml
description: |
  Core firmware development specialist for STM32 microcontrollers. Expert in
  HAL/LL drivers, clock configuration, timer programming, interrupt handling,
  DMA setup, memory management, and RTOS integration. Primary agent for general
  MCU programming questions not specific to communication peripherals, analog,
  or graphics.

  <examples>
  - "How do I configure the system clock to 480MHz on H7?"
  - "Timer interrupt not firing - help debug"
  - "Best way to structure my FreeRTOS tasks"
  - "DMA transfer complete callback not working"
  </examples>

  <triggers>
  clock, PLL, timer, TIM1-TIM17, interrupt, NVIC, DMA, MDMA, HAL, LL driver,
  FreeRTOS, CMSIS-RTOS, task, semaphore, mutex, queue, GPIO, EXTI, flash
  programming, MPU configuration, cache, TCM, linker script, startup code,
  SystemInit, main loop, state machine, watchdog, IWDG, WWDG
  </triggers>

  <excludes>
  USART, SPI, I2C, CAN, USB (-> Peripheral-Comm)
  ADC, DAC, audio, analog (-> Peripheral-Analog)
  LTDC, DMA2D, camera (-> Peripheral-Graphics)
  secure boot, encryption (-> Security)
  low-power modes, battery (-> Power)
  bootloader, IAP (-> Bootloader)
  </excludes>
```

#### Trigger Keywords and Phrases

**Primary Triggers:**
- Clock: "clock", "PLL", "HSE", "HSI", "LSE", "LSI", "SYSCLK", "HCLK", "PCLK", "clock tree", "frequency", "MHz"
- Timers: "timer", "TIM", "PWM", "input capture", "output compare", "encoder mode", "one-pulse"
- Interrupts: "interrupt", "NVIC", "IRQ", "ISR", "priority", "preemption", "vector table"
- DMA: "DMA", "MDMA", "BDMA", "DMA stream", "DMA channel", "circular mode", "double buffer"
- HAL/LL: "HAL_", "LL_", "STM32Cube", "CubeMX", "driver", "middleware"
- RTOS: "FreeRTOS", "CMSIS-RTOS", "task", "thread", "semaphore", "mutex", "queue", "scheduler"
- Memory: "flash", "SRAM", "TCM", "DTCM", "ITCM", "cache", "MPU", "linker", "scatter file"
- Watchdog: "watchdog", "IWDG", "WWDG", "reset", "timeout"
- GPIO: "GPIO", "pin", "port", "EXTI", "external interrupt"

**Negative Triggers (Route Elsewhere):**
- "USART", "UART", "SPI", "I2C", "CAN", "USB", "Ethernet" -> Peripheral-Comm
- "ADC", "DAC", "analog", "sensor", "audio", "microphone" -> Peripheral-Analog
- "LCD", "display", "LTDC", "DMA2D", "camera", "DCMI" -> Peripheral-Graphics
- "secure boot", "encryption", "CRYP", "HASH", "RNG", "TrustZone" -> Security
- "low power", "sleep", "stop", "standby", "battery", "consumption" -> Power
- "bootloader", "DFU", "IAP", "firmware update" -> Bootloader
- "HardFault", "debug", "SWD", "breakpoint", "trace" -> Debug

#### Example Queries - Primary Domain

1. "How do I configure the STM32H7 to run at 480MHz with external crystal?"
2. "Timer 2 interrupt is not firing. I've enabled NVIC and started the timer."
3. "What's the best DMA configuration for memory-to-memory transfers on H7?"
4. "How should I structure FreeRTOS tasks for a sensor polling application?"
5. "My application crashes when I enable the data cache. How do I fix cache coherency?"
6. "How do I use the MPU to protect critical memory regions?"
7. "What's the difference between HAL and LL drivers? When should I use each?"

#### Edge Cases and Ambiguous Queries

1. "DMA with UART" -> **Collaboration**: Firmware (DMA) + Peripheral-Comm (UART)
2. "Timer-triggered ADC" -> **Collaboration**: Firmware (Timer) + Peripheral-Analog (ADC)
3. "PWM for motor control" -> **Primary**: Firmware (timer focus, not motor drive circuits)
4. "GPIO configuration for SPI" -> **Route to**: Peripheral-Comm (SPI is primary intent)

#### Collaboration Scenarios

| Query Pattern | Primary Agent | Collaborator | Reason |
|---------------|---------------|--------------|--------|
| DMA + UART/SPI/I2C | Peripheral-Comm | Firmware | Peripheral is primary focus |
| Timer + ADC trigger | Peripheral-Analog | Firmware | ADC is end goal |
| FreeRTOS + USB stack | Peripheral-Comm | Firmware | USB is primary feature |
| Cache + ETH DMA | Peripheral-Comm | Firmware | Network is primary feature |
| RTOS + power modes | Power | Firmware | Power optimization is goal |

---

### 2.3 Peripheral-Comm Agent

#### Agent Description (for agent file)
```yaml
description: |
  Serial communication and connectivity specialist for STM32. Expert in USART/UART,
  SPI, I2C, CAN/FDCAN, USB device/host/OTG, Ethernet, and emerging protocols like
  I3C. Handles protocol configuration, timing, DMA integration for comm peripherals,
  and debugging communication issues.

  <examples>
  - "UART receiving garbage characters at 115200 baud"
  - "How to configure SPI in DMA mode with hardware NSS"
  - "CAN bus not acknowledging messages"
  - "USB CDC device not enumerating on Windows"
  </examples>

  <triggers>
  USART, UART, LPUART, SPI, QSPI, OSPI, I2C, FMPI2C, I3C, CAN, FDCAN, USB,
  OTG, CDC, HID, MSC, Ethernet, RMII, MII, PHY, baud rate, parity, stop bits,
  MOSI, MISO, SCK, NSS, SDA, SCL, TX, RX, protocol, communication, serial,
  bus, acknowledge, arbitration, frame, packet
  </triggers>
```

#### Trigger Keywords and Phrases

**USART/UART Triggers:**
- "USART", "UART", "LPUART", "serial", "RS-232", "RS-485"
- "baud", "baud rate", "parity", "stop bit", "overrun", "framing error"
- "TX", "RX", "transmit", "receive", "DMA UART"
- "printf redirect", "console", "terminal"

**SPI Triggers:**
- "SPI", "QSPI", "OSPI", "OctoSPI", "HexaSPI"
- "MOSI", "MISO", "SCK", "NSS", "chip select", "slave select"
- "SPI mode", "CPOL", "CPHA", "full duplex", "half duplex"
- "SPI flash", "W25Q", "external flash"

**I2C Triggers:**
- "I2C", "I3C", "FMPI2C", "SMBus", "PMBus"
- "SDA", "SCL", "pull-up", "address", "7-bit", "10-bit"
- "I2C stuck", "bus busy", "NACK", "acknowledge"
- "I2C sensor", "EEPROM", "RTC chip"

**CAN Triggers:**
- "CAN", "FDCAN", "CAN FD", "CAN bus", "CAN 2.0"
- "CAN ID", "filter", "FIFO", "mailbox", "arbitration"
- "CAN transceiver", "TJA1050", "bus off", "error passive"
- "J1939", "CANopen", "UDS"

**USB Triggers:**
- "USB", "OTG", "device", "host", "hub"
- "CDC", "HID", "MSC", "audio class", "DFU class"
- "enumeration", "descriptor", "endpoint", "VID", "PID"
- "USB cable", "VBUS", "D+", "D-"

**Ethernet Triggers:**
- "Ethernet", "ETH", "RMII", "MII", "PHY"
- "LwIP", "TCP/IP", "socket", "DHCP", "MAC address"
- "LAN8742", "DP83848", "KSZ8081"

**Negative Triggers:**
- Pure DMA questions without comm context -> Firmware
- Low-level timer for baud generation -> Firmware (but may collaborate)
- SDMMC/SD card -> Peripheral-Analog (storage/data acquisition context)

#### Example Queries - Primary Domain

1. "My UART is receiving garbage at 115200 baud. Clock is 64MHz."
2. "How do I configure SPI3 in DMA circular mode with hardware NSS management?"
3. "I2C bus stays busy and never releases. How do I recover?"
4. "FDCAN messages are being sent but not received on the other node."
5. "USB CDC device works on Linux but not on Windows 10."
6. "What's the correct PHY configuration for Ethernet on STM32H7?"
7. "How do I implement a custom USB HID device with multiple reports?"

#### Edge Cases and Ambiguous Queries

1. "DMA not working with SPI" -> **Primary**: Peripheral-Comm (SPI is focus)
2. "Timer for UART bit-banging" -> **Primary**: Peripheral-Comm (UART is goal)
3. "USB power consumption" -> **Collaboration**: Power (primary) + Peripheral-Comm
4. "Secure USB boot" -> **Collaboration**: Bootloader (primary) + Security + Peripheral-Comm

#### Collaboration Rules

| Query Pattern | Primary | Collaborator(s) | Division of Work |
|---------------|---------|-----------------|------------------|
| DMA + SPI/UART/I2C | Peripheral-Comm | Firmware | Comm configures peripheral, Firmware advises DMA setup |
| USB + Bootloader | Bootloader | Peripheral-Comm | Bootloader leads, Comm advises USB specifics |
| CAN + Security | Security | Peripheral-Comm | Security leads for SecOC, Comm advises CAN config |
| Ethernet + RTOS | Peripheral-Comm | Firmware | Comm leads for LwIP, Firmware advises RTOS integration |

---

### 2.4 Peripheral-Analog Agent

#### Agent Description (for agent file)
```yaml
description: |
  Analog peripherals and signal processing specialist for STM32. Expert in ADC
  configuration, DAC operation, audio interfaces (SAI, I2S, SPDIF), analog
  sensors, signal conditioning, DSP algorithms, and data acquisition systems.
  Handles noise reduction, sampling strategies, and analog accuracy optimization.

  <examples>
  - "ADC readings are noisy and unstable"
  - "How to configure SAI for I2S audio codec"
  - "DAC output has stepping artifacts"
  - "Implementing digital filter for sensor data"
  </examples>

  <triggers>
  ADC, DAC, analog, VREF, sample, conversion, resolution, oversampling,
  SAI, I2S, SPDIF, audio, codec, PCM, PDM, microphone, speaker,
  sensor, temperature, pressure, accelerometer, gyroscope,
  DSP, filter, FFT, Goertzel, CMSIS-DSP, signal processing,
  noise, SNR, ENOB, INL, DNL, calibration, DFSDM, sigma-delta
  </triggers>
```

#### Trigger Keywords and Phrases

**ADC Triggers:**
- "ADC", "analog to digital", "analog input", "conversion"
- "sample rate", "sampling", "resolution", "12-bit", "16-bit"
- "oversampling", "averaging", "noise", "SNR", "ENOB"
- "VREF", "reference voltage", "calibration", "offset"
- "injected", "regular", "scan mode", "continuous mode"
- "ADC accuracy", "ADC error", "ADC noise"

**DAC Triggers:**
- "DAC", "digital to analog", "analog output"
- "waveform", "sine wave", "triangle", "sawtooth"
- "DAC DMA", "DAC timer trigger", "buffer mode"
- "audio output", "speaker drive"

**Audio Triggers:**
- "SAI", "I2S", "SPDIF", "audio", "sound"
- "codec", "WM8994", "CS4344", "PCM1774"
- "PDM", "microphone", "DFSDM", "digital microphone"
- "sample rate", "44.1kHz", "48kHz", "96kHz"
- "audio streaming", "audio buffer", "underrun"

**Sensor Triggers:**
- "sensor", "temperature sensor", "internal temp"
- "accelerometer", "gyroscope", "IMU", "magnetometer"
- "pressure sensor", "humidity", "gas sensor"
- "sensor fusion", "Kalman filter", "complementary filter"

**DSP Triggers:**
- "DSP", "digital signal processing", "CMSIS-DSP"
- "FFT", "DFT", "Goertzel", "spectrum"
- "filter", "FIR", "IIR", "low pass", "high pass", "band pass"
- "convolution", "correlation", "moving average"
- "CORDIC", "trigonometric", "math functions"

**Negative Triggers:**
- "SPI sensor" -> Peripheral-Comm (communication is primary)
- "I2C accelerometer setup" -> Peripheral-Comm first, then collaborate
- "ADC for security RNG" -> Security (purpose is security)

#### Example Queries - Primary Domain

1. "My ADC readings on STM32H7 are jumping around by 50-100 LSB. How do I reduce noise?"
2. "How do I configure the SAI peripheral for I2S communication with a WM8994 codec?"
3. "I want to generate a 1kHz sine wave using the DAC with DMA."
4. "How do I use DFSDM to interface with a PDM microphone?"
5. "What's the best oversampling configuration to get 16-bit effective resolution from 12-bit ADC?"
6. "How do I implement a real-time FFT on STM32H7 using CMSIS-DSP?"
7. "The internal temperature sensor reading doesn't match my external thermometer."

#### Edge Cases and Ambiguous Queries

1. "Timer-triggered ADC" -> **Primary**: Peripheral-Analog (ADC is goal), **Collaborate**: Firmware
2. "DMA with ADC" -> **Primary**: Peripheral-Analog (ADC focus)
3. "Audio over USB" -> **Collaboration**: Peripheral-Comm (USB) + Peripheral-Analog (audio)
4. "Sensor data logging to SD" -> **Primary**: Peripheral-Analog, **Collaborate**: Peripheral-Comm (SDMMC)

---

### 2.5 Peripheral-Graphics Agent

#### Agent Description (for agent file)
```yaml
description: |
  Display and graphics specialist for STM32. Expert in LTDC display controller,
  DMA2D/ChromArt acceleration, camera interface (DCMI), touchscreen integration,
  GUI frameworks (TouchGFX, STemWin, LVGL), and framebuffer management. Handles
  display timing, color formats, layer composition, and graphics performance.

  <examples>
  - "LTDC display shows garbage or tearing"
  - "How to use DMA2D for fast rectangle fills"
  - "Camera preview is garbled or has wrong colors"
  - "TouchGFX framebuffer configuration"
  </examples>

  <triggers>
  LTDC, LCD, display, TFT, screen, pixel, framebuffer, layer,
  DMA2D, ChromArt, blend, fill, copy, pixel format, RGB565, ARGB8888,
  DCMI, camera, OV5640, OV2640, image capture, JPEG,
  TouchGFX, STemWin, LVGL, GUI, graphics, animation, widget,
  touchscreen, touch controller, FT5336, GT911
  </triggers>
```

#### Trigger Keywords and Phrases

**LTDC/Display Triggers:**
- "LTDC", "LCD", "TFT", "display", "screen", "monitor"
- "framebuffer", "layer", "foreground", "background"
- "pixel clock", "PCLK", "HSYNC", "VSYNC", "DE"
- "tearing", "flickering", "display timing"
- "RGB565", "RGB888", "ARGB8888", "color format"
- "resolution", "480x272", "800x480", "1024x600"

**DMA2D/Graphics Acceleration Triggers:**
- "DMA2D", "ChromArt", "Chrom-ART"
- "fill", "copy", "blend", "alpha blending"
- "graphics acceleration", "hardware rendering"
- "pixel conversion", "color conversion"

**Camera Triggers:**
- "DCMI", "camera", "image sensor"
- "OV5640", "OV2640", "OV7670", "camera module"
- "capture", "snapshot", "video", "preview"
- "JPEG", "image compression", "camera DMA"

**GUI Framework Triggers:**
- "TouchGFX", "STemWin", "LVGL", "emWin", "uGFX"
- "GUI", "graphical interface", "user interface"
- "widget", "button", "slider", "gauge", "chart"
- "animation", "transition", "screen change"
- "font", "text rendering", "anti-aliasing"

**Touch Triggers:**
- "touchscreen", "touch panel", "touch controller"
- "FT5336", "GT911", "FT6206", "touch I2C"
- "touch coordinates", "multi-touch", "gesture"

**Negative Triggers:**
- "LCD SPI interface" -> Peripheral-Comm (SPI is mechanism)
- "Display power consumption" -> Power (energy is focus)

#### Example Queries - Primary Domain

1. "My LTDC display shows random pixels and sometimes tears. Timing seems off."
2. "How do I use DMA2D to efficiently fill rectangles with transparency?"
3. "Camera preview from OV5640 shows wrong colors - looks like RGB/BGR swap."
4. "What's the best framebuffer configuration for TouchGFX on STM32H7?"
5. "How do I configure double buffering to eliminate tearing?"
6. "LVGL animations are choppy. How do I improve graphics performance?"
7. "How do I capture a JPEG image from the camera using hardware compression?"

#### Edge Cases and Ambiguous Queries

1. "SPI display" -> **Collaboration**: Peripheral-Comm (SPI) + Peripheral-Graphics (display logic)
2. "Display DMA" -> **Primary**: Peripheral-Graphics (display is goal)
3. "Camera + USB streaming" -> **Collaboration**: Peripheral-Graphics + Peripheral-Comm
4. "GUI with RTOS" -> **Collaboration**: Peripheral-Graphics + Firmware

---

### 2.6 Hardware Agent

#### Agent Description (for agent file)
```yaml
description: |
  Hardware design and PCB specialist for STM32 systems. Expert in schematic design,
  PCB layout, power supply design, EMC compliance, thermal management, signal
  integrity, and component selection. Handles circuit design questions, reference
  design interpretation, and manufacturing considerations.

  <examples>
  - "What decoupling capacitors do I need for STM32H7?"
  - "My board fails EMC testing at 100MHz harmonics"
  - "STM32 overheating under heavy load"
  - "High-speed signal routing for SDRAM"
  </examples>

  <triggers>
  PCB, schematic, layout, routing, trace, via, ground plane, power plane,
  decoupling, bypass capacitor, ferrite bead, EMC, EMI, ESD, immunity,
  thermal, heat sink, temperature rise, thermal via, power dissipation,
  signal integrity, impedance, crosstalk, reflection, termination,
  crystal, oscillator, HSE, LSE, load capacitor, ESR,
  power supply, LDO, SMPS, voltage regulator, VBAT, VDD, VDDA,
  connector, pinout, footprint, package, BGA, LQFP, QFN
  </triggers>
```

#### Trigger Keywords and Phrases

**PCB/Schematic Triggers:**
- "PCB", "printed circuit board", "schematic", "circuit"
- "layout", "routing", "trace", "track", "via"
- "ground plane", "power plane", "layer stack"
- "footprint", "pad", "solder", "reflow"

**Decoupling/Power Distribution Triggers:**
- "decoupling", "bypass capacitor", "bulk capacitor"
- "ferrite bead", "power filtering", "noise filtering"
- "power plane", "PDN", "power distribution"
- "VDD", "VDDA", "VDDIO", "VBAT", "VCAP"

**EMC/ESD Triggers:**
- "EMC", "EMI", "electromagnetic", "compatibility"
- "ESD", "electrostatic", "TVS", "protection"
- "radiated emissions", "conducted emissions"
- "immunity", "susceptibility", "CE marking", "FCC"
- "harmonics", "spectral", "noise floor"

**Thermal Triggers:**
- "thermal", "temperature", "overheating", "hot"
- "heat sink", "thermal pad", "thermal via"
- "power dissipation", "thermal resistance", "junction temperature"
- "cooling", "airflow", "thermal management"

**Signal Integrity Triggers:**
- "signal integrity", "SI", "impedance", "controlled impedance"
- "crosstalk", "reflection", "ringing", "overshoot"
- "termination", "series resistor", "matched impedance"
- "high-speed", "DDR", "SDRAM routing", "differential pair"

**Crystal/Oscillator Triggers:**
- "crystal", "oscillator", "HSE", "LSE"
- "load capacitor", "CL", "ESR", "ppm", "accuracy"
- "startup time", "oscillation", "crystal not starting"

**Component Selection Triggers:**
- "component selection", "BOM", "part number"
- "package", "BGA", "LQFP", "QFN", "WLCSP"
- "connector", "header", "debug connector"

**Negative Triggers:**
- "How to configure HSE in code" -> Firmware (software configuration)
- "Clock tree setup" -> Firmware (software)
- "Secure element selection" -> Security

#### Example Queries - Primary Domain

1. "What decoupling capacitor values and placement do I need for STM32H723?"
2. "My board is failing EMC at 480MHz - probably USB. How do I fix it?"
3. "The STM32H7 reaches 95C under full load. How do I improve thermal performance?"
4. "How should I route the high-speed SDRAM signals for good signal integrity?"
5. "My 8MHz crystal isn't starting reliably. What load capacitors should I use?"
6. "What's the recommended power supply sequencing for STM32H7 with SMPS?"
7. "How do I protect the USB lines from ESD?"

#### Edge Cases and Ambiguous Queries

1. "Crystal not starting" -> **Primary**: Hardware (likely capacitor/layout issue)
2. "HSE not stable" -> **Clarify**: Hardware issue or software configuration?
3. "Power consumption too high" -> **Route to**: Power Agent (unless explicitly PCB issue)
4. "Flash not working" -> **Clarify**: External flash PCB issue or software issue?

---

### 2.7 Security Agent

#### Agent Description (for agent file)
```yaml
description: |
  Security specialist for STM32 embedded systems. Expert in secure boot, hardware
  cryptography (AES, SHA, RSA), random number generation, TrustZone, secure
  firmware updates, key management, tamper detection, and security certifications.
  Handles threat modeling, security architecture, and hardening recommendations.

  <examples>
  - "How to implement secure boot on STM32H7?"
  - "AES encryption is too slow for my application"
  - "Implementing secure firmware update with signature verification"
  - "How to protect encryption keys from extraction?"
  </examples>

  <triggers>
  security, secure boot, trusted boot, chain of trust, root of trust,
  encryption, decryption, AES, DES, RSA, ECC, ECDSA, SHA, HASH, HMAC,
  CRYP, PKA, RNG, random number, entropy, TRNG,
  TrustZone, SAU, secure/non-secure, isolation, TEE,
  key, certificate, signature, authentication, provisioning,
  tamper, anti-tamper, intrusion detection, RDP, PCROP, WRP,
  secure storage, key storage, OTP, secure element
  </triggers>
```

#### Trigger Keywords and Phrases

**Secure Boot Triggers:**
- "secure boot", "trusted boot", "verified boot"
- "chain of trust", "root of trust", "boot authentication"
- "boot signature", "boot verification", "secure bootloader"
- "RDP", "read protection", "option bytes security"

**Cryptography Triggers:**
- "encryption", "decryption", "cipher", "cryptography"
- "AES", "AES-128", "AES-256", "AES-GCM", "AES-CCM"
- "SHA", "SHA-256", "HASH", "HMAC", "message digest"
- "RSA", "ECC", "ECDSA", "PKA", "public key", "private key"
- "CRYP", "crypto accelerator", "hardware crypto"

**Random Number Triggers:**
- "RNG", "random number", "TRNG", "entropy"
- "random seed", "cryptographic random"

**TrustZone Triggers:**
- "TrustZone", "TZ", "secure world", "non-secure world"
- "SAU", "IDAU", "secure attribution"
- "secure gateway", "NSC", "non-secure callable"
- "isolation", "partition", "TEE"

**Key Management Triggers:**
- "key", "key storage", "key provisioning", "key injection"
- "certificate", "X.509", "PKI", "CA"
- "OTP", "one-time programmable", "fuses"
- "secure element", "HSM", "TPM"

**Tamper/Protection Triggers:**
- "tamper", "anti-tamper", "intrusion detection"
- "TAMP", "backup domain", "RTC tamper"
- "PCROP", "WRP", "write protection", "readout protection"
- "secure storage", "protected region"

**Negative Triggers:**
- "USB security" -> Depends: USB auth = Peripheral-Comm + Security
- "Bootloader without security" -> Bootloader Agent

#### Example Queries - Primary Domain

1. "How do I implement secure boot with signature verification on STM32H7?"
2. "AES-256 encryption is taking 2ms per block. Can I speed it up?"
3. "How do I use the hardware RNG for cryptographic key generation?"
4. "What's the correct way to configure TrustZone for secure/non-secure partitioning?"
5. "How do I securely store encryption keys so they can't be extracted?"
6. "My application needs FIPS 140-2 compliance. What STM32 features help?"
7. "How do I implement secure firmware update with rollback protection?"

#### Edge Cases and Ambiguous Queries

1. "Secure USB DFU" -> **Collaboration**: Bootloader + Security
2. "Protected bootloader" -> **Primary**: Security (unless just IAP mechanics)
3. "RNG for simulation" -> **Primary**: Security (even if non-crypto use)
4. "Memory protection" -> **Clarify**: MPU (Firmware) or security protection (Security)?

---

### 2.8 Safety Agent

#### Agent Description (for agent file)
```yaml
description: |
  Functional safety specialist for STM32 applications. Expert in IEC 61508, ISO
  26262, IEC 60730 certifications, self-test libraries (STL/ClassB), safety
  architectures, diagnostic coverage, FMEA/FMEDA, and safety documentation.
  Handles safety requirement analysis, test coverage, and certification guidance.

  <examples>
  - "How to achieve SIL-2 with STM32?"
  - "Implementing Class B self-tests for IEC 60730"
  - "CPU register test failing intermittently"
  - "What diagnostic coverage do I need for ISO 26262 ASIL-B?"
  </examples>

  <triggers>
  safety, functional safety, SIL, ASIL, IEC 61508, ISO 26262, IEC 60730,
  Class B, self-test, STL, diagnostic, fault detection, fault coverage,
  FMEA, FMEDA, failure mode, failure rate, FIT, SFF,
  watchdog, program flow, stack monitoring, clock monitoring,
  CPU test, register test, RAM test, flash test, CRC check,
  safe state, fail-safe, fault tolerant, redundancy
  </triggers>
```

#### Trigger Keywords and Phrases

**Certification Triggers:**
- "IEC 61508", "SIL", "SIL-1", "SIL-2", "SIL-3"
- "ISO 26262", "ASIL", "ASIL-A", "ASIL-B", "ASIL-C", "ASIL-D"
- "IEC 60730", "Class A", "Class B", "Class C"
- "UL", "CSA", "certification", "compliance"
- "functional safety", "safety integrity"

**Self-Test Triggers:**
- "self-test", "STL", "X-CUBE-STL", "X-CUBE-CLASSB"
- "CPU test", "register test", "ALU test"
- "RAM test", "March C", "March X", "memory test"
- "flash test", "CRC check", "integrity check"
- "clock test", "frequency monitoring"
- "program flow", "control flow", "stack test"

**Analysis Triggers:**
- "FMEA", "FMEDA", "failure mode", "failure analysis"
- "diagnostic coverage", "DC", "fault coverage"
- "failure rate", "FIT", "MTBF", "SFF"
- "safe failure fraction", "hardware fault tolerance"

**Architecture Triggers:**
- "safe state", "fail-safe", "fail-operational"
- "redundancy", "dual-core lockstep", "diverse redundancy"
- "watchdog", "safety watchdog", "window watchdog"
- "independent monitoring", "external watchdog"

**Negative Triggers:**
- "Watchdog for crash recovery" -> Firmware (not safety-focused)
- "CRC for data integrity" -> Firmware (unless safety context)
- "Security certification" -> Security Agent

#### Example Queries - Primary Domain

1. "How do I implement IEC 60730 Class B self-tests on STM32H7?"
2. "What diagnostic coverage does the STL RAM test provide?"
3. "My CPU register test is failing randomly. How do I debug it?"
4. "What architecture do I need for ISO 26262 ASIL-B compliance?"
5. "How do I integrate X-CUBE-STL into my existing application?"
6. "What's the difference between online and offline self-tests?"
7. "How do I calculate the diagnostic coverage for my safety function?"

#### Edge Cases and Ambiguous Queries

1. "Watchdog for safety" -> **Primary**: Safety (safety context)
2. "Memory ECC" -> **Clarify**: Safety (fault detection) or Firmware (reliability)?
3. "Dual-core for safety" -> **Primary**: Safety + Firmware collaboration
4. "Safe bootloader" -> **Collaboration**: Safety + Bootloader

---

### 2.9 Power Agent

#### Agent Description (for agent file)
```yaml
description: |
  Power management and optimization specialist for STM32. Expert in low-power
  modes (Sleep, Stop, Standby, Shutdown), wake-up sources, power consumption
  measurement, battery-powered design, dynamic voltage/frequency scaling, and
  power-aware firmware design. Handles energy optimization and battery life.

  <examples>
  - "How to enter Stop 2 mode and wake on RTC alarm?"
  - "Current consumption in Stop mode is too high"
  - "Battery life estimation for sensor node"
  - "Optimizing power while maintaining responsiveness"
  </examples>

  <triggers>
  power, low power, low-power, sleep, stop, standby, shutdown, VBAT,
  wake-up, wakeup, WFI, WFE, SLEEPDEEP, PWR, power mode,
  current consumption, power consumption, microamps, milliamps,
  battery, battery life, energy, energy harvesting,
  SMPS, LDO, voltage scaling, VOS, dynamic voltage,
  clock gating, peripheral disable, power domain, backup domain
  </triggers>
```

#### Trigger Keywords and Phrases

**Low-Power Mode Triggers:**
- "low power", "low-power", "sleep", "deep sleep"
- "stop", "stop mode", "Stop 0", "Stop 1", "Stop 2"
- "standby", "standby mode", "shutdown", "VBAT mode"
- "WFI", "WFE", "SLEEPDEEP", "SLEEPONEXIT"
- "power mode", "PWR", "power controller"

**Wake-up Triggers:**
- "wake-up", "wakeup", "wake up", "wake source"
- "WKUP pin", "RTC wakeup", "RTC alarm"
- "EXTI wakeup", "UART wakeup", "I2C wakeup"
- "wakeup latency", "wakeup time"

**Consumption Triggers:**
- "current consumption", "power consumption"
- "microamps", "uA", "milliamps", "mA"
- "idle current", "run current", "sleep current"
- "power measurement", "current measurement"
- "power analyzer", "current probe"

**Battery Triggers:**
- "battery", "battery life", "battery powered"
- "coin cell", "CR2032", "LiPo", "Li-ion"
- "energy", "energy budget", "energy harvesting"
- "duty cycle", "active time", "sleep time"

**Power Supply Triggers:**
- "SMPS", "LDO", "internal regulator"
- "voltage scaling", "VOS", "VOS0", "VOS1", "VOS2", "VOS3"
- "dynamic voltage", "DVFS", "frequency scaling"
- "power domain", "D1", "D2", "D3", "SRD"
- "backup domain", "VBAT", "backup SRAM"

**Negative Triggers:**
- "Power supply schematic" -> Hardware Agent
- "USB power delivery" -> Peripheral-Comm Agent
- "Power safety" -> Safety Agent

#### Example Queries - Primary Domain

1. "How do I enter Stop 2 mode on STM32H7 and wake up from RTC alarm?"
2. "My Stop mode current is 50uA instead of the expected 6uA. What's wrong?"
3. "How do I estimate battery life for a sensor that wakes every 10 seconds?"
4. "What's the optimal voltage scaling setting for 240MHz operation?"
5. "How do I keep SRAM3 powered in Standby mode?"
6. "My application takes 5ms to wake from Stop mode. How do I reduce this?"
7. "How do I implement UART wakeup from low-power mode?"

#### Edge Cases and Ambiguous Queries

1. "UART wakeup" -> **Primary**: Power (wakeup focus), **Collaborate**: Peripheral-Comm
2. "RTC for low power" -> **Primary**: Power (power is goal)
3. "GPIO in low power" -> **Primary**: Power (power context)
4. "Power supply design" -> **Route to**: Hardware Agent

---

### 2.10 Bootloader Agent

#### Agent Description (for agent file)
```yaml
description: |
  Bootloader and firmware update specialist for STM32. Expert in system bootloader,
  custom bootloaders, in-application programming (IAP), DFU protocol, boot modes,
  flash programming, option bytes, and firmware update mechanisms. Handles boot
  configuration, update protocols, and recovery strategies.

  <examples>
  - "How to use system bootloader for UART programming?"
  - "Implementing custom bootloader with firmware update"
  - "DFU mode not working on Windows"
  - "Dual-bank boot with fallback"
  </examples>

  <triggers>
  bootloader, system bootloader, boot mode, BOOT0, BOOT1, boot pin,
  IAP, in-application programming, firmware update, OTA, FOTA,
  DFU, device firmware update, STM32CubeProgrammer,
  flash programming, flash write, flash erase, flash unlock,
  option bytes, OB, read protection, write protection,
  dual bank, bank swap, BFB2, A/B update, fallback,
  jump to application, vector table, reset handler
  </triggers>
```

#### Trigger Keywords and Phrases

**System Bootloader Triggers:**
- "system bootloader", "built-in bootloader", "ROM bootloader"
- "boot mode", "BOOT0", "BOOT1", "boot pin", "boot configuration"
- "STM32CubeProgrammer", "STM32 Programmer", "ST-LINK"
- "USART bootloader", "I2C bootloader", "SPI bootloader", "USB DFU bootloader"

**Custom Bootloader Triggers:**
- "custom bootloader", "application bootloader", "secondary bootloader"
- "bootloader design", "bootloader implementation"
- "jump to application", "start application"
- "vector table relocation", "VTOR", "SCB->VTOR"
- "reset handler", "main application"

**Firmware Update Triggers:**
- "IAP", "in-application programming", "self-programming"
- "firmware update", "firmware upgrade", "OTA", "FOTA"
- "DFU", "device firmware update", "DFU class"
- "update protocol", "update mechanism"

**Flash Programming Triggers:**
- "flash programming", "flash write", "flash erase"
- "flash unlock", "FLASH_CR", "flash operations"
- "flash sector", "flash page", "flash bank"
- "embedded flash", "internal flash"

**Option Bytes Triggers:**
- "option bytes", "OB", "option byte programming"
- "read protection", "RDP", "level 0", "level 1", "level 2"
- "write protection", "WRP", "sector protection"
- "boot address", "BOOT_ADD0", "BOOT_ADD1"

**Dual Bank/Recovery Triggers:**
- "dual bank", "bank swap", "BFB2", "bank boot"
- "A/B update", "ping-pong", "fallback", "rollback"
- "recovery", "fail-safe boot", "golden image"
- "version management", "firmware version"

**Negative Triggers:**
- "Secure boot" -> Security Agent (security focus)
- "Boot time optimization" -> Firmware Agent (unless bootloader-specific)
- "Flash for data storage" -> Firmware Agent

#### Example Queries - Primary Domain

1. "How do I use the system bootloader to program via UART?"
2. "I'm implementing a custom bootloader. How do I jump to the main application?"
3. "DFU mode works on Linux but not Windows. How do I fix driver issues?"
4. "How do I implement dual-bank firmware update with automatic fallback?"
5. "What's the correct sequence to erase and program flash in IAP?"
6. "How do I change option bytes from within my application?"
7. "My bootloader works but the application doesn't start. Vector table issue?"

#### Edge Cases and Ambiguous Queries

1. "Secure bootloader" -> **Collaboration**: Bootloader + Security
2. "USB DFU" -> **Primary**: Bootloader (DFU is boot protocol)
3. "Flash CRC check" -> **Clarify**: Boot validation (Bootloader) or runtime check (Firmware)?
4. "Bootloader power consumption" -> **Collaboration**: Bootloader + Power

---

### 2.11 Debug Agent

#### Agent Description (for agent file)
```yaml
description: |
  Debugging and fault analysis specialist for STM32. Expert in HardFault diagnosis,
  SWD/JTAG debugging, trace capabilities (ETM, ITM, SWO), breakpoints, watchpoints,
  debugging tools, and crash analysis. Handles runtime errors, core dumps, and
  performance profiling.

  <examples>
  - "HardFault at address 0x08001234 - how to diagnose?"
  - "SWD connection drops randomly during debug"
  - "Setting up ITM printf for debugging"
  - "Application crashes after running for 10 minutes"
  </examples>

  <triggers>
  debug, debugging, debugger, SWD, JTAG, ST-LINK, J-Link, CMSIS-DAP,
  HardFault, BusFault, MemManage, UsageFault, fault handler,
  breakpoint, watchpoint, halt, step, trace,
  ETM, ITM, SWO, trace buffer, instruction trace,
  crash, exception, stack overflow, stack corruption,
  core dump, register dump, fault analysis, post-mortem,
  STM32CubeIDE, Ozone, IAR, Keil, GDB
  </triggers>
```

#### Trigger Keywords and Phrases

**Fault Triggers:**
- "HardFault", "BusFault", "MemManage", "UsageFault", "SecureFault"
- "fault", "exception", "crash", "freeze", "hang"
- "fault handler", "fault analysis", "fault address"
- "CFSR", "HFSR", "MMFAR", "BFAR", "fault registers"

**Debug Interface Triggers:**
- "SWD", "JTAG", "debug interface", "debug port"
- "ST-LINK", "J-Link", "CMSIS-DAP", "Black Magic Probe"
- "debug connection", "debug session", "connect under reset"
- "SWDIO", "SWCLK", "SWO", "TDI", "TDO", "TCK", "TMS"

**Breakpoint/Watchpoint Triggers:**
- "breakpoint", "hardware breakpoint", "software breakpoint"
- "watchpoint", "data breakpoint", "access breakpoint"
- "halt", "stop", "pause", "step", "single step"
- "step into", "step over", "step out", "run to cursor"

**Trace Triggers:**
- "trace", "ETM", "ITM", "MTB", "DWT"
- "SWO", "trace output", "ITM printf"
- "instruction trace", "data trace", "PC sampling"
- "trace buffer", "trace viewer", "trace analysis"

**Crash Analysis Triggers:**
- "crash", "crash analysis", "post-mortem", "core dump"
- "register dump", "stack dump", "memory dump"
- "stack overflow", "stack corruption", "heap corruption"
- "memory leak", "buffer overflow", "null pointer"

**Tool Triggers:**
- "STM32CubeIDE", "debugging in IDE"
- "GDB", "OpenOCD", "GDB server"
- "Ozone", "IAR debugger", "Keil debugger"
- "debug configuration", "launch configuration"

**Negative Triggers:**
- "Debug build vs release" -> Firmware (build configuration)
- "Debug UART output" -> Peripheral-Comm (UART focus)
- "Bootloader debugging" -> Bootloader (primary domain)

#### Example Queries - Primary Domain

1. "I'm getting HardFault at 0x08004572. How do I find the cause?"
2. "My ST-LINK connection fails randomly during debugging. What's wrong?"
3. "How do I set up ITM/SWO printf debugging on STM32H7?"
4. "Application runs for 10 minutes then crashes. How do I capture the fault?"
5. "What do the fault status registers tell me about this crash?"
6. "How do I debug a hang where the watchdog doesn't trigger?"
7. "Setting up ETM trace to see instruction history before crash?"

#### Edge Cases and Ambiguous Queries

1. "UART debug output" -> **Clarify**: ITM/SWO debug (Debug) or UART comms (Peripheral-Comm)?
2. "Performance profiling" -> **Primary**: Debug (profiling tools)
3. "Memory corruption" -> **Primary**: Debug (crash analysis)
4. "Debugging bootloader" -> **Collaboration**: Debug + Bootloader

---

## 3. Global Routing Decision Tree

### 3.1 Primary Classification Algorithm

```
FUNCTION ClassifyQuery(query):
    // Step 1: Extract keywords and signals
    keywords = ExtractKeywords(query)
    intent = AnalyzeIntent(query)

    // Step 2: Calculate agent scores
    scores = {}
    FOR EACH agent IN agents:
        score = 0

        // Positive keyword matches
        FOR EACH keyword IN agent.triggers:
            IF keyword IN query (case-insensitive):
                score += GetKeywordWeight(keyword)

        // Negative keyword matches (exclusions)
        FOR EACH keyword IN agent.excludes:
            IF keyword IN query:
                score -= 50  // Strong penalty

        // Pattern matching
        FOR EACH pattern IN agent.patterns:
            IF pattern.matches(query):
                score += pattern.weight

        scores[agent] = score

    // Step 3: Apply priority rules
    scores = ApplyPriorityRules(scores, keywords)

    // Step 4: Determine routing
    primary = GetHighestScore(scores)

    IF primary.score < CONFIDENCE_THRESHOLD:
        RETURN RequestClarification(query)

    collaborators = GetCollaborators(query, primary)

    RETURN RouteDecision(primary, collaborators)
```

### 3.2 Keyword Weight Table

| Weight | Keyword Type | Examples |
|--------|--------------|----------|
| 100 | Exclusive domain term | "LTDC", "TrustZone", "IEC 60730" |
| 75 | Strong domain indicator | "ADC noise", "bootloader jump", "HardFault" |
| 50 | Common domain term | "timer", "UART", "flash" |
| 25 | Weak indicator | "configure", "setup", "problem" |
| -50 | Negative indicator | Term in wrong domain |

### 3.3 Priority Rules

When multiple agents have similar scores, apply these priority rules:

1. **Specificity Rule**: More specific agent wins
   - "SPI DMA" -> Peripheral-Comm (SPI is more specific than DMA)
   - "Timer ADC trigger" -> Peripheral-Analog (ADC is end goal)

2. **End-Goal Rule**: Agent handling the end goal wins
   - "DMA for UART" -> Peripheral-Comm (UART is the goal)
   - "Flash for bootloader" -> Bootloader (boot is the goal)

3. **Debug Priority**: Debug agent handles all crashes/faults
   - Any query with "HardFault", "crash", "exception" -> Debug first
   - Unless clearly domain-specific debug (e.g., "ADC giving wrong values")

4. **Safety Override**: Safety takes priority for certification queries
   - "Watchdog for SIL-2" -> Safety (not Firmware)
   - "RAM test for Class B" -> Safety (not Firmware)

5. **Security Override**: Security takes priority for protection queries
   - "Protected bootloader" -> Security (unless just implementation)
   - "Encrypted firmware update" -> Security (not Bootloader)

### 3.4 Confidence Thresholds

| Score Range | Action |
|-------------|--------|
| >= 100 | Route to primary agent with high confidence |
| 75-99 | Route to primary agent, may suggest clarification |
| 50-74 | Route with collaboration, request might be ambiguous |
| 25-49 | Request clarification before routing |
| < 25 | Router handles directly or asks for more details |

---

## 4. Collaboration Protocols

### 4.1 Collaboration Triggers

A query requires collaboration when:
1. Keywords from multiple domains appear with similar weights
2. The query explicitly mentions multiple subsystems
3. The primary agent cannot fully answer without domain expertise
4. Standard integration patterns are involved (e.g., DMA + Peripheral)

### 4.2 Collaboration Patterns

#### Pattern A: Primary with Advisory
Primary agent handles query, requests specific info from collaborator.

```
User: "How do I configure DMA for SPI transfers?"

Router: Route to Peripheral-Comm (primary: SPI)
        Flag collaboration with Firmware (advisory: DMA specifics)

Peripheral-Comm Agent:
  1. Explains SPI DMA mode configuration
  2. Requests Firmware Agent: "DMA stream assignment for SPI3 on H7?"
  3. Integrates response into complete answer
```

#### Pattern B: Sequential Handoff
One agent handles their portion, then hands off.

```
User: "Implement secure OTA firmware update"

Router: Route to Security (primary: secure aspects)
        Then Bootloader (implementation)
        Then Peripheral-Comm (transport)

Sequence:
  1. Security: Defines signature verification, key management
  2. Bootloader: Implements update mechanism with security requirements
  3. Peripheral-Comm: Advises on transport (USB DFU, UART, etc.)
```

#### Pattern C: Parallel Consultation
Multiple agents contribute simultaneously.

```
User: "Debug audio dropout issue with SAI"

Router: Route to all three in parallel:
  - Debug Agent: Crash/fault analysis
  - Peripheral-Analog: SAI/DMA configuration
  - Firmware: DMA interrupt priorities, RTOS timing

Synthesis: Combine insights into unified diagnosis
```

### 4.3 Inter-Agent Communication Format

When one agent needs input from another:

```json
{
  "request_type": "domain_expertise",
  "from_agent": "peripheral-comm",
  "to_agent": "firmware",
  "context": "User configuring SPI DMA on STM32H7",
  "question": "What is the optimal DMA configuration for bidirectional SPI at 50MHz?",
  "required_info": [
    "DMA stream recommendation",
    "FIFO threshold settings",
    "Memory burst configuration"
  ]
}
```

### 4.4 Common Collaboration Pairs

| Domain Pair | Typical Scenario | Primary |
|-------------|------------------|---------|
| Firmware + Peripheral-Comm | DMA for communication | Peripheral-Comm |
| Firmware + Peripheral-Analog | Timer-triggered ADC | Peripheral-Analog |
| Firmware + Power | RTOS low-power | Power |
| Security + Bootloader | Secure boot | Security |
| Safety + Firmware | Self-test integration | Safety |
| Debug + Any | Fault in specific domain | Debug first |
| Hardware + Power | Power supply design | Hardware |
| Peripheral-Graphics + Peripheral-Comm | SPI display | Peripheral-Graphics |

---

## 5. Confidence Scoring System

### 5.1 Score Calculation

```
TotalScore = Σ(PositiveMatches) - Σ(NegativeMatches) + ContextBonus

Where:
  PositiveMatches = keyword_weight × match_quality
  NegativeMatches = exclusion_weight × match_quality
  ContextBonus = conversation_history_relevance × 10
```

### 5.2 Match Quality Factors

| Factor | Multiplier | Description |
|--------|------------|-------------|
| Exact match | 1.0 | Keyword appears exactly |
| Phrase match | 1.2 | Multi-word phrase matches |
| Partial match | 0.5 | Substring or related term |
| Negated | -0.5 | "not", "without", "except" nearby |
| Question focus | 1.5 | Keyword is subject of question |

### 5.3 Confidence Levels

```
Level 1: CERTAIN (score >= 100)
  - Single clear domain match
  - No competing domains
  - Action: Route immediately

Level 2: CONFIDENT (score 75-99)
  - Strong domain match
  - Minor competing signals
  - Action: Route with optional clarification

Level 3: LIKELY (score 50-74)
  - Moderate domain match
  - Multiple domains possible
  - Action: Route with collaboration flag

Level 4: UNCERTAIN (score 25-49)
  - Weak domain signals
  - Ambiguous query
  - Action: Request clarification

Level 5: UNKNOWN (score < 25)
  - No clear domain match
  - Generic or unclear query
  - Action: Router handles or asks for details
```

---

## 6. Edge Cases and Ambiguity Resolution

### 6.1 Common Ambiguous Queries

#### Query: "Timer not working"
**Ambiguity**: Could be any timer issue
**Resolution**:
```
IF context mentions PWM/motor -> Firmware
IF context mentions ADC triggering -> Peripheral-Analog
IF context mentions communication timeout -> Peripheral-Comm
IF context mentions power/wakeup -> Power
ELSE -> Firmware (default for timers) + ask for clarification
```

#### Query: "Flash problems"
**Ambiguity**: Internal flash, external flash, or QSPI flash
**Resolution**:
```
IF mentions "external", "QSPI", "W25Q" -> Peripheral-Comm
IF mentions "bootloader", "IAP", "programming" -> Bootloader
IF mentions "corruption", "ECC", "retention" -> Safety or Firmware
ELSE -> Ask: "Are you referring to internal flash or external flash memory?"
```

#### Query: "Communication error"
**Ambiguity**: Which protocol?
**Resolution**:
```
IF protocol specified -> Peripheral-Comm with that protocol
IF hardware symptoms (EMI, signal) -> Hardware
IF timing symptoms (overrun, underrun) -> Peripheral-Comm + Firmware
ELSE -> Ask: "Which communication protocol are you using?"
```

### 6.2 Multi-Domain Query Decomposition

For complex queries spanning multiple domains:

```
Query: "My battery-powered sensor node needs to wake up every second,
        read I2C temperature sensor, and send data over LoRa SPI,
        while meeting IEC 60730 Class B requirements"

Decomposition:
1. Power: Low-power mode, 1-second RTC wakeup, power budget
2. Peripheral-Comm: I2C sensor interface, SPI LoRa module
3. Peripheral-Analog: Temperature sensor data processing (if analog)
4. Safety: IEC 60730 Class B self-tests, diagnostic coverage

Routing:
  Primary: Power (battery optimization is primary concern)
  Collaborators: Peripheral-Comm, Safety
  Sequence: Power -> Peripheral-Comm -> Safety
```

### 6.3 Clarification Templates

When routing confidence is low, use structured clarification:

```
Template 1 - Domain Clarification:
"To help you better, could you clarify:
 - Are you asking about [Domain A interpretation] or [Domain B interpretation]?
 - What is your main goal with this [feature/peripheral]?"

Template 2 - Context Gathering:
"I can help with that. To give you the best answer:
 - Which STM32 series/part number are you using?
 - What have you tried so far?
 - What symptoms or errors are you seeing?"

Template 3 - Scope Clarification:
"This could involve several aspects:
 - Hardware/PCB design
 - Firmware/software configuration
 - Debugging/troubleshooting
 Which aspect would you like to focus on?"
```

### 6.4 Fallback Rules

When no clear routing exists:

1. **Hardware mention without software context** -> Hardware Agent
2. **Software mention without hardware context** -> Firmware Agent
3. **Error/problem without domain context** -> Debug Agent
4. **"How to" without specific topic** -> Router asks for clarification
5. **General STM32 question** -> Router handles directly

---

## Appendix A: Quick Reference Routing Table

| Primary Keywords | Agent | Confidence |
|------------------|-------|------------|
| ADC, DAC, analog, sensor, audio, SAI, I2S, DFSDM | Peripheral-Analog | High |
| UART, SPI, I2C, CAN, USB, Ethernet | Peripheral-Comm | High |
| LTDC, DMA2D, display, camera, DCMI, GUI | Peripheral-Graphics | High |
| timer, clock, PLL, DMA, interrupt, NVIC, HAL, FreeRTOS | Firmware | High |
| PCB, schematic, EMC, ESD, thermal, crystal | Hardware | High |
| secure boot, encryption, AES, TrustZone, key | Security | High |
| SIL, ASIL, IEC 60730, self-test, Class B | Safety | High |
| low power, sleep, stop, standby, battery | Power | High |
| bootloader, IAP, DFU, firmware update | Bootloader | High |
| HardFault, crash, SWD, debug, trace | Debug | High |

---

## Appendix B: Agent File Template

```yaml
# .claude/agents/<agent-name>.md

---
name: <Agent Display Name>
description: |
  <Comprehensive description optimized for automatic selection>

  <examples>
  - "Example query 1"
  - "Example query 2"
  </examples>

  <triggers>
  keyword1, keyword2, keyword3, phrase with spaces
  </triggers>

  <excludes>
  keyword that should not route here -> correct agent
  </excludes>

  <collaborates_with>
  - agent-name: "When collaboration is needed"
  </collaborates_with>
---

# Agent Instructions

## Your Role
<Detailed agent role and responsibilities>

## Core Expertise
<List of specific expertise areas>

## Knowledge Sources
<Documentation and references agent should use>

## Response Guidelines
<How to structure responses>

## Collaboration Protocol
<When and how to request help from other agents>
```

---

*Document Version: 1.0*
*Last Updated: 2025*
*Maintainer: STM32 Agent System*
