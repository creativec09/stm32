# Introduction

STM32 end-users are sometimes confronted with non- or partially-functional systems during product development. The best approach to use for the debug process is not always obvious, particularly for inexperienced users.

To address the above concerns, this application note provides a toolbox describing the most common debug techniques and their application to popular recommended IDEs for STM32 32-bit Arm® Cortex® MCUs. It contains detailed information for getting started as well as hints and tips to make the best use of STM32 Software Development Tools in STM32 ecosystem.

This application note applies to the microcontrollers listed in Table 1.

Table 1. Applicable products   

<table><tr><td>Type</td><td>Sub class</td></tr><tr><td>Microcontrollers</td><td>STM32 High Performance MCUs STM32 Mainstream MCUs STM32 Ultra Low Power MCUs</td></tr></table>

# Contents

# Foreword 8

1.1 General information 8   
1.2 Software versions 8   
1.3 Acronyms 8

# STM32 ecosystem outlines . .9

2.1 Hardware development tools 9

2.1.1 Hardware kits . . 9   
2.1.2 ST-LINK probe 16   
2.1.3 Alternative debugger probes 19

2.2 Software development tools 20

2.2.1 STM32CubeMX 21   
2.2.2 STM32CubeIDE 22   
2.2.3 Partner IDEs .24   
2.2.4 STM32CubeProgrammer . 25   
2.2.5 STM32CubeMonitor . 27

2.3 Embedded software 28

2.4 Information and sharing 29

2.4.1 Documentation . .30   
2.4.2 Wiki platform .31   
2.4.3 Github .31   
2.4.4 ST Community .31   
2.4.5 STM32 Education 32

# Compiling for debug . .. . .. 33

3.1 Optimization 33

3.1.1 IAR™M EWARM . . 34  
3.1.2 Keil® MDK-Arm µVision 35  
3.1.3 STM32CubeIDE .36

3.2 Debugging information 36

3.2.1 IAR™M EWARM . . 37   
3.2.2 Keil®-MDK-Arm μVision 38   
3.2.3 STM32CubeIDE . .39

# Connecting to the board . 40

4.1 SWD/JTAG pinout 40

4.2 Reset and connection mode . 42

4.2.1 Presentation . . 42   
4.2.2 IAR™M EWARM . 43   
4.2.3 Keil©® MDK-Arm µVISION . 44   
4.2.4 STM32CubeIDE . 48   
4.2.5 STM32CubeProgrammer 49

4.3 Low-power case 50

# Breaking and stepping into code . .. . 51

5.1 Debug support for timers, RTC, watchdog, BxCAN and I2C . . . . . . . . . . 51

5.2 Debug performance 51

5.2.1 IAR™M EWARM . . 52   
5.2.2 Kei® MDK-Arm μVISION . 53   
5.2.3 STM32CubeIDE . .54

5.3 Secure platform limitation 55

5.3.1 RDP .55   
5.3.2 PCROP .56

# Exception handling . . . . 57

6.1 Default weak Handlers . 57   
6.2 Custom Handlers 58   
6.3 Trapping div/0 exception 60   
6.3.1 Cortex®-MO/MO+ case 60   
6.3.2 Cortex®-M3/4/7 case .61

# Printf debugging .. 68

7.1 STM32 Virtual COM port driver 68   
7.2 Printf via UART 69   
7.3 Printf via SWO/SWV 71   
7.4 Semihosting 79   
7.4.1 IAR™M EWARM. 80   
7.4.2 Keil® MDK-Arm μVISION. 80   
7.4.3 STM32CubeIDE. .81

# Debug through hardware exploration . . 87

8.1 Easy pinout probing with STMicroelectronics hardware kits 87

8.2 Microcontroller clock output (MCO) 87

8.2.1 Configuration with STM32CubeMX 87   
8.2.2 HAL_RCC_MCOConfig 89   
8.2.3 STM32 Series differences .90

# Dual-Core microcontroller debugging . .. 92

From debug to release . .. .. 93

Troubleshooting • • 94

# Appendix A Managing DBGMCU registers. . .. 95

A.1 By software ... 95   
A.2 By debugger ..... 96   
Appendix B Use Nucleo "cuttable" ST-LINK as stand-alone VCP . . .106   
Appendix C Managing various targets on the same PC . . 109   
Appendix D Cortex®- debug capabilities reminder 116   
D.1 Application notes index . ..116

Revision history 117

# List of tables

Table 1. Applicable products 1   
Table 2. ST-LINK software pack. . 19   
Table 3. STMicroelectronics documentation guide. 30   
Table 4. STM32 Series RDP protection extension . 56   
Table 5. STM32 USART vs. PC terminal WordLength example. 71   
Table 6. Troubleshooting.. 94   
Table 7. STM32 Series vs. debug capabilties 116   
Table 8. STM32 Series vs. debug capabilities 116   
Table 9. Document revision history 117

# List of figures

Figure 1. STM32 ecosystem overview. .9   
Figure 2. Development tools overview. 10   
Figure 3. Nucleo-144, Nucleo-64 and Nucleo-32 boards. 10   
Figure 4. STM32 Nucleo-144 structure 11   
Figure 5. Discovery board example . 12   
Figure 6. EVAL board example 13   
Figure 7. 7X-NUCLEO-LPM01A 14   
Figure 8. ST-LINK, ST-LINK/V2, and ST-LINK/V2-ISOL stand-alone probes 16   
Figure 9. STLINK-V3SET. 16   
Figure 10. On-board ST-LINK-V3 on Nucleo 17   
Figure 11. STM32 software development 20   
Figure 12. STM32CubeMX Configure and code generation 21   
Figure 13. STM32CubeIDE 22   
Figure 14. STM32Cube programmer. 26   
Figure 15. STM32Cube monitor. 28   
Figure 16. STM32CubeProjectList screenshot 29   
Figure 17. Get connected to STM32 world 29   
Figure 18. IAR™M EWARM Optimization option 34   
Figure 19. Keil® Vision Code Optimization option 35   
Figure 20. STM32CubelDE optimization level setting 36   
Figure 21. IAR™ EWARM Generate debug Information option. 37   
Figure 22. Keil® Debug Information option 38   
Figure 23. STM32CubelDE debug information option. 39   
Figure 24. SWD pins PA13 and PA14 in Reset state under STM32CubeMX. 40   
Figure 25. SWD pins PA13 and PA14 in Reserved but inactive state   
under STM32CubeMX . 41   
Figure 26. SWD pins PA13 and PA14 in Active State under STM32CubeMX. 41   
Figure 27. Reset Mode in IAR8.10: screenshot. 43   
Figure 28. Connect and Reset option Keil® 44   
Figure 29. Keil hotplug step1. 45   
Figure 30. Keil hotplug step2. 46   
Figure 31. Keil© hotplug step3 .. 47   
Figure 32. Select Generator Options Reset Mode. . 48   
Figure 33. STM32CubeProgrammer Reset mode . 49   
Figure 34. STM32CubeProgrammer Connection mode 49   
Figure 35. IARTM EWARM ST-LINK SWD Speed setting 52   
Figure 36. Keil® sWD Speed Setting.. 53   
Figure 37. Access to Generator Options in STM32CubelDE V2.0.0 . 54   
Figure 38. Asking for Handler code generation . ... 58   
Figure 39. Keil® Access to Show Caller Code in Contextual menu 60   
Figure 40. Cortex®-M3 SCB_CCR Description 61   
Figue 41. Cortex-M3 SCB_CFSR Description 61   
Figure 42. IART™ EWARM exception handling 62   
Figure 43. Kei System Control and Configure. 63   
Figure 44. Keil® Fault Reports. 64   
Figure 45. STM32CubeIDE SCB register access 65   
Figure 46. Fault Analyzer in STM32CubeIDE 66   
Figure 47. Virtual COM port on Windows® PC 68   
Figure 48. USART Pinout configuration with STM32CubeMX. 69   
Figure 49. USART2 setting with STM32CubeMX 70   
Figure 50. SWO Pin configuration with STM32CubeMX 72   
Figure 51. Semihosting/SWO configuration with IAR ™M EWARM 73   
Figure 52. AR™ EWARM SWO CloCk setting 74   
Figure 53. SWO configuration with Keil®. .75   
Figure 54. Access to SWV in Keil® 75   
Figure 55. Enable SWD in STM32CubeIDE 77   
Figure 56. Enable SWV ITM Data Console in STM32CubeIDE. 78   
Figure 57. Enable ITM stimulus Port 0 in STM32CubeIDE .79   
Figure 58. Start Trace button in STM32CubeIDE 79   
Figure 59. Semihosting configuration in IAR ™M EWARM . 80   
Figure 60. Properties for semihosting in STM32CubeIDE- Source Location. 81   
Figure 61. Properties for semihosting in STM32CubeIDE- Librairies 82   
Figure 62. Properties for semihosting in STM32CubeIDE. 82   
Figure 63. Semihosting in STM32CubeIDE - Debug configuration. 84   
Figure 64. Semihosting in STM32CubeIDE - Startup 85   
Figure 65. Semihosting in STM32CubeIDE - Run 86   
Figure 66. MCO pin selection in STM32CubeMX 87   
Figure 67. MCO alternate pin highlight exemple with L073 88   
Figure 68. MCO Multiplexer in STM32CubeMX Clock Configuration Pane . 89   
Figure 69. STM32F4/F7 dual MCO capabilities. 91   
Figure 70. DBMCU Register LL Library Functions. 95   
Figure 71. DBGMCU_CR HAL Library Functions 96   
Figure 72. Access to DBGMCU register with IAR ™M EWARM 97   
Figure 73. EWARM C-SPY® Macro script setting 98   
Figure 74. Accessing DBGMCU register in Keil® MDK-Arm µVision (1/2). 99   
Figure 75. Accessing DBGMCU register in Kei® MDK-Arm Vision (2/2 100   
Figure 76. Keil Initialization script etting 101   
Figure 77. Access to Generator Options in STM32CubeIDE V2.0.0. 102   
Figure 78. Generator Options debug MCU in STM32CubeIDE 103   
Figure 79. Access to DBGMCU settings with STM32CubeIDE V1.3.0 104   
Figure 80. Runtime R/W access to DBGMCU register with SSTM32CubeIDE 105   
Figure 81. ST-LINK cuttable part of Nucleo . . 106   
Figure 82. Using ST-LINK stand-alone part of Nucleo-L476RG as VCP 107   
Figure 83. Virtual COM port on PC side 108   
Figure 84. STM32CubeProgrammer target selection pick list . 109   
Figure 85. Getting target ST-LINK S/N from the console. 110   
Figure 86. IAR™M EWARM Debug Probe Selection pop-up window 110   
Figure 87. IAR™M EWARM Debug Probe Selection with nickname 111   
Figure 88. Probe selection prompt setting on IAR ™ EWARM. 111   
Figure 89. Keil® ST-LINK selection 112   
Figure 90. Error message for multiple ST-LINK detected in STM32CubeIDE 113   
Figure 91. Forcing specific ST-LINK S/N with STM32CubeIDE with OpenOCD option. 114   
Figure 92. Forcing specific ST-LINK S/N with STM32CubelDE with ST-LINK GDB server. 115

1

# Foreword

# 1.1

# General information

This document applies to STM32 32-bit Arm® Cortex® MCUs.

Note:

Arm is a registered trademark of Arm Limited (or its subsidiaries) in the US and/or elsewhere.

# arm

# 1.2 Software versions

The various examples in this application note are illustrated on basisof the following versions of the tools:

• IAR™ EWARM: V8.32.3   
• Keil©® MDK-Arm μVision: V5.26   
• STM32CubeIDE: V1.3.0   
STM32CubeProg: V2.2.1

# 1.3 Acronyms

• AN: Application note   
• CMSIS: Cortex microcontroller software interface standard   
• HAL: Hardware abstraction layer (software library)   
• IDE: Integrated development environment   
• JTAG: Joint Test Action Group   
• MCO: Microcontroller clock output   
• MCU: Microcontroller unit   
• NVIC: Nested vector interrupt controller   
• PM: Programming manual   
• RM: Reference manual   
• SB: Solder bridge   
• SWD: Serial wire debug   
• SWO: Single wire output   
• SWV: Single wire viewer   
• VCP: Virtual COM port

# 2 STM32 ecosystem outlines

STMicroelectronics and its partners are providing a full hardware and software ecosystem to support rapid evaluation, prototyping, and productizing of complete systems using STM32 microcontrollers.

As presented in Figure 1, the ecosystem is composed of all the collaterals required to develop a project with STM32.

![](images/fd2de4b041c87bfbeb0e836dd7430276996756d220ffa96bd60f2dff58233125.jpg)  
Figure 1. STM32 ecosystem overview

This chapter provides a global overview of the main elements composing the ecosystem, outlining debug features and useful pointers, in order to guide the user among available resources.

# 2.1 Hardware development tools

This section introduces the range of available development tools from hardware kits to ST-LINK probes and alternative debugger interfaces.

# 2.1.1 Hardware kits

This section lists the hardware kits provided by STMicroelectronics for STM32-based development:

• Nucleo boards   
• Discovery kits   
• Evaluation boards (EVAL)   
• STM32 Nucleo expansion   
• Third-party boards

![](images/341c45ac1ab5d73ee9bd0a4e67d03216d28fe35533f056902010d20b4b489210.jpg)  
Figure 2. Development tools overview

# STM32 Nucleo

STM32 Nucleo boards are affordable solutions for user willing to try out new ideas and to quickly create prototypes based on STM32 MCU.

![](images/f306e0cf4e166938900743e8b7dce8c072be209a973d69c67125b49ed99f6ef0.jpg)  
Figure 3. Nucleo-144, Nucleo-64 and Nucleo-32 boards

STM32 Nucleo boards feature the same connectors. They can easily be extended with a large number of specialized application hardware add-ons.

# Note:

Nucleo-144 boards include ST Zio connector, which is an extension of ARDUINO® Uno rev3, and ST morpho connector.

Nucleo-68 board and Nucleo-64 boards include ARDUINO® Uno rev3 and ST morpho connectors.

Nucleo-32 boards include ARDUINO® Nano connectors.

All STM32 Nucleo boards integrate an ST-LINK debugger/programmer, so there is no need for a separate probe.

The figure below shows an example of STM32 Nucleo structure

![](images/48e9b67f2c404daf09b6c303714f10fb8f8df10f6084c894599fec0a95f7abc5.jpg)  
Figure 4. STM32 Nucleo-144 structure

A complete description of the embedded ST-LINK features is provided in Section 2.1.2: ST-LINK probe on page 16. Additional information and access to Nucleo boards complete documentation sets are available at www.st.com.

# Discovery kits

STM32 Discovery kits are a cheap and complete solution for the evaluation of the outstanding capabilities of STM32 MCUs. They carry the necessary infrastructure for demonstration of specific device characteristics, the HAL library, and comprehensive software examples allow to fully benefit from the devices features and added values.

![](images/6608e127f15fb87a42198e45710ef54b506b375e6ffdb7aa2143db1e5982d869.jpg)  
Figure 5. Discovery board example

![](images/f3d521022cb2d75bd129fd56d4bd07cda704fded5d2bc68ab800000c7ededfe9.jpg)

Extension connectors give access to most of the device's l/Os and make the connection of add-on hardware possible.

With the integrated debugger/programmer the Discovery kits are ideal for prototyping.

A complete description of the embedded ST-LINK features is provided in Section 2.1.2: ST-LINK probe on page 16. Additional information and access to Discovery kits complete documentation sets are available at www.st.com.

# Evaluation boards

STM32 MCU EVAL boards have been designed as a complete demonstration and development platform for the Arm® Cortex® STM32 MCUs.

![](images/e16cbc646269de838ea9f4b2e1735acc7d095494494b06b407022e0ae71330fd.jpg)  
Figure 6. EVAL board example

They carry external circuitry, such as transceivers, sensors, memory interfaces, displays and many more. The EVAL boards can be considered as a reference design for application development.

EVAL boards have integrated ST-LINK (USB Type-B connector). For complete description of the embedded ST-LINK features refer to Section 2.1.2: ST-LINK probe.

EVAL board has direct access to JTAG/Traces signal through dedicated Arm® JTAG 20-pin connector allowing advanced debug (ETM). For usage of ETM traces refer to Section 2.1.3: Alternative debugger probes on page 19.

The usage of a stand-alone probe may require some jumper and solder bridge adaptation from default. Refer to the specific board user manual.

For further information and access to complete documentation visit www.st.com/stm32evaltools.

# STM32 nucle0 expansion

STM32 Nucleo expansion boards carry all the required components to Evaluate ST devices to be used together with an STM32 MCU.

Build STM32-based applications leveraging functionality and performance of ST's device portfolio.

The expansion boards are equipped with standardized interconnections, such as an ARDUiNO Uno R3 connector, or a Morpho connector for a higher level of connectivity

Each expansion board is supported by STM32-based software modules.

The combination of STM32 Nucleo boards and expansion boards is a unified scalable approach with unlimited possibilities for application development, prototyping or product evaluation.

# X-NUCLEO-LPM01A

This board is an example of STM32 nucleo expansion

![](images/aadc0e0418e4b2df5003745437046de1bea8d0f13c678086849c325a3880de57.jpg)  
Figure 7. 7X-NUCLEO-LPM01A

The X-NUCLEO-LPM01A is a 1.8 V to 3.3 V programmable power supply source with advanced power consumption measurement capability.

It performs consumption averaging (static measurement up to 200 mA) as well as real-time analysis (dynamic measurement up to 50 mA with 100 kHz bandwidth).

The X-NUCLEO-LPM01A operates either in standalone mode (using its LCD, joystick and button to display static measurements), or in controlled mode connected to host PC via

USB (using the STM32CubeMonPwr software tool with its comprehensive graphical user interface).

It can be used to supply and measure the consumption of STM32 Nucleo-32, Nucleo-64, Nucleo-68 or Nucleo-144 boards, using ARDUiNO connectors.

Alternatively, it supplies and measures the consumption of any target connected by wires via the basic connector.

# KEY FEATURES

STM32L496VGT6 microcontroller featuring Arm® Cortex®-M4 core at 80 MHz / 100 DMIPS and three 12-bit ADC at 5 Msps

Programmable voltage source from 1.8 V to 3.3 V

Static current measurement from 1 nA to 200 mA

Dynamic measurements:

100 kHz bandwidth, 3.2 Msps sampling rate   
Current from 100 nA to 50 mA   
Power measurement from 180 nW to 165 mW   
Energy measurement computation by power measurement time integration   
Execution of EEMBC ULPMark ™M tests

Mode standalone:

Monochrome LCD, 2 lines of 16 characters with backlight 4-direction joystick with selection button Enter and Reset push-buttons

Mode controlled:

Connection to a PC through USB FS Micro-B receptacle Command line (Virtual COM port) or STM32CubeMonitor-Power PC tool.

Four status LEDs

Target board connectors:

ARDUINO® Uno and Nano connectors Basic connector (white): 4 wires

Flexible input power-supply options:

USB Micro-B (VBUS) External power connector (7 V to 10 V) ARDUINO Uno and Nano connectors (pin 5 V)

# 2.1.2 ST-LINK probe

The ST-LINK is the JTAG/Serial Wire Debug (SWD) interface used to communicate with any STM32 microcontroller located on an application board.

It is available as:

• Stand-alone in-circuit debugger • Embedded in all STM32 hardware kits (Nucleo boards, Discovery kits, EVAL boards)

ST-LINK/V2 and ST-LINK-V3 are the main used versions.

Figure 8 shows ST-LINK/V2 and ST-LINK/V2- ISOL stand-alone probes on the right.

![](images/a4bf2281bfd34195591d67ee43d15e27704f46653235311ed01658dcec822634.jpg)  
Figure 8. ST-LINK, ST-LINK/V2, and ST-LINK/V2-ISOL stand-alone probes

![](images/d22118dd0b6a68fc7f0aa0d5657bd8cf21fe81b261358dbee61ad01fcf90685f.jpg)  
Figure 9 shows the last STLINK-V3SET version.   
Figure 9. STLINK-V3SET

Figure 10 shows an example of an embedded ST-LINK/V2 as part of a Nucleo board.

![](images/b3f6141e9b658037cd49b594a54d35e38691e5707146a5fda28de33d9bcbdd3d.jpg)  
Figure 10. On-board ST-LINK-V3 on Nucleo

# ST-LINK/V2 basic features

5 V power supplied by a USB connector √ USB 2.0 full-speed-compatible interface

USB standard Type-A to Mini- B cable

JTAG/serial wire debug (SWD) specific features:

1.65 V to 3.6 V application voltage supported on the JTAG/SWD interface and 5 V   
tolerant inputs   
JTAG cable for connection to a standard JTAG 20-pin pitch 2.54 mm connector   
JTAG supported   
SWD and serial wire viewer (SWV) communication supported   
• Device Firmware Upgrade (DFU) feature supported   
• Status LED which blinks during communication with the PC Operating temperature 0 °C to 50 °C 1000 V rms high-isolation voltage (ST-LINK/V2-ISOL only)

Embedded versions usually supports the following additional features:

Virtual COM port interface on USB. (VCP) _ Mass storage interface on USB

The availability of these additional features depends on software version.

# ST-LINK-V3 basic features

Stand-alone probe with modular extensions Self-powered through a USB connector (Micro-B)   
• USB 2.0 high-speed compatible interface   
• Direct firmware update support (DFU)   
• JTAG / serial wire debugging (SWD) specific features: 3 V to 3.6 V application voltage support and 5 V tolerant inputs Flat cables STDC14 to MIPI10 / STDC14 / MIPI20 (connectors with 1.27 mm pitch) JTAG communication support SWD and serial wire viewer (SWV) communication support

Virtual COM port (VCP) specific features:

3 V to 3.6 V application voltage support on the UART interface and 5 V tolerant   
inputs   
VCP frequency up to 15 MHz   
Available on STDC14 debug connector (not available on MIPI10)

Multi-path bridge USB to SPI/UART/I2C/CAN/GPIOs specific features:

3 V to 3.6 V application voltage support and 5 V tolerant inputs Signals available on adapter board only (MB1440)

• Drag-and-drop flash programming of binary files • Two-color LEDs: communication, power

The STLINK-V3SET product does not provide power supply to the target application.

In order to identify the ST-LINK version on a board and the related features associated with it, please refer STMicroelectronics technical note Overview of the ST-LINK embedded in STM32 MCU Nucleo, Discovery Kits and Eval Boards (TN1235).

On-board ST-LINK does not support JTAG port.

Note:

For Nucleo and Discovery, JTAG port signal can be wired through Morpho / ARDUINO® connectors. On EVAL boards, there is a dedicated 20-pin connector.

The use of ST-LINK requires the software packages listed in Table 2.

Table 2. ST-LINK software pack   

<table><tr><td rowspan=1 colspan=1>Part Number</td><td rowspan=1 colspan=1>Description</td></tr><tr><td rowspan=1 colspan=1>STSW-LINK007</td><td rowspan=1 colspan=1>ST-LINK, ST-LINK/V2, ST-LINK/V2-1, STLINK-V3 boards firmware upgrade</td></tr><tr><td rowspan=1 colspan=1>STSW-LINK009</td><td rowspan=1 colspan=1>ST-LINK, ST-LINK/V2, ST-LINK/V2-1 USB driver signed for Windows® 7,Windows® 8, Windows® 10</td></tr><tr><td rowspan=1 colspan=1>STLINK-V3-BRIDGE</td><td rowspan=1 colspan=1>Software API compatible with the bridge interface of STLINK-V3</td></tr></table>

# Note:

STSW-LINK007 is included in STSW-LINK004.

STSW-LINK009 is included in most IDE installation packages (IAR Systems®, Keil®, STM32CubeIDE) and tools.

Tip: It is recommended to use the latest firmware version of the on-board ST-LINK interface. Firmware upgrade can be performed thanks to the STM32CubeProgrammer (refer to Section 2.2.4: STM32CubeProgrammer) or STM32CubeIDE.

# 2.1.3 Alternative debugger probes

J-LINK (Segger), I-Jet™ (IAR Systems®), and U-LINK (Keil®) are the most common alternatives providing features equivalent to the ones provided by ST-LINK.

For most advanced debugging needs, requiring heavy traffic or ETM port tracing, ST recommends using:

U-Link Pro in combination with Keil® MDK-Arm µVISION √ I-Jet ™ Trace in combination with IAR™M EWARM

For a complete catalog of solutions, refer to www.st. com.

# 2.2 Software development tools

The STM32 family of 32-bit Arm® Cortex®-M core-based microcontrollers is supported by a complete range of software tools.

It encompasses traditional integrated development environments - IDEs with C/C++ compilers and debuggers from major third parties that are complemented with tools from ST allowing to configure and initialize the MCU or monitor its behavior in run time.

It offers a complete flow, from configuration up to monitoring as illustrated in Figure 11.

![](images/58897721717fc8855c8a36ee14b67f45335781b91c13975c1b715ee54f5e1123.jpg)  
Figure 11. STM32 software development

# 2.2.1 STM32CubeMX

![](images/2476ad0a88dc0280304c8a254c23cae82b87fc5b3a38a3a9e6ed528ee75b91db.jpg)  
Figure 12. STM32CubeMX Configure and code generation

STM32CubeMX is a graphical tool that allows to easily configure STM32 microcontrollers and to generate the corresponding initialization C code through a step-by-step process.

The first step consists in selecting the STM32 microcontroller that matches the required set of peripherals. MCU can be selected as stand-alone for custom PCB (MCU Selector) or preintegrated into one of STMicroelectronics hardware kit (Board Selector)

In the second step, the user must configure each required embedded software thanks to a pinout-conflict solver, a clock-tree setting helper, a power-consumption calculator, and a utility performing MCU peripheral configuration (GPIO, USART, and others) and middleware stacks (USB, TCP/IP, and others).

Finally, the user launches the generation of the initialization C code based on the selected configuration. This code is ready to be used within several development environments. The user code is kept at the next code generation.

# Key features

Intuitive STM32 microcontroller selection

Rich graphical user interface configuration:

Pinout with automatic conflict resolution   
Clock tree with dynamic validation of configuration   
Peripherals and middleware functional modes and initialization with dynamic   
validation of parameter constraints   
Power consumption calculation for a user-defined application sequence

C code project generation covering STM32 microcontroller initialization compliant with IAR Systems®, Keil® and GCC compilers.

Available as a standalone software running on Windows®, Linux®, and macOS® operating systems, or through Eclipse plug-in

# 2.2.2 STM32CubeIDE

STM32CubeIDE is an all-in-one multi-OS development tool, which is part of the STM32Cube software ecosystem.

![](images/52d1a1a80ae379acf622152ff8d66813e99fac88bd4388934c6276415954454f.jpg)  
Figure 13. STM32CubelDE

STM32CubelDE is an advanced C/C++ development platform with peripheral configuration, code generation, code compilation, and debug features for STM32 microcontrollers. It is based on the Eclipse®/CDT framework and GCC toolchain for the development, and GDB for the debugging. It allows the integration of the hundreds of existing plugins that complete the features of the Eclipse® IDE. STM32CubeIDE integrates all STM32CubeMX functionalities to offer allin-one tool experience and save installation and development time. After the selection of an empty STM32 MCU or MPU, or preconfigured microcontroller from the selection of a board, the project is created, and initialization code generated. At any time during the development, the user can return to the initialization and configuration of the peripherals or middleware and regenerate the initialization code with no impact on the user code. STM32CubelDE includes build and stack analyzers that provide the user with useful information about project status and memory requirements. STM32CubelDE also includes standard and advanced debugging features including views of CPU core registers, memories, and peripheral registers, as well as live variable watch, Serial Wire Viewer interface, or fault analyzer.

# Key features

Integration of STM32CubeMX that provides services for:

STM32 microcontroller selection Pinout, clock, peripheral, and middleware configuration Project creation and generation of the initialization code

Based on Eclipse®/CDT, with support of Eclipse® add-ons, GNU C/C++ for Arm® toolchain and GDB debugger

Additional advanced debug features including:

CPU core, peripheral register, and memory views   
Live variable watch view   
System analysis and real-time tracing (SWV)   
CPU fault analysis tool

Support of ST-LINK (STMicroelectronics) and J-Link (SEGGER) debug probes

Import project from Atolic® TrueSTUDIO® and AC6 System Workbench for STM32 (STM32CubeIDE) ultuWins®Li®ma®6iers

# 2.2.3 Partner IDEs

In this application note, all topics are declined for the three main IDEs:

1. IAR™M EWARM Keil® MDK-Arm µVISION

# IARTM EWARM

The IAR Embedded Workbench® for Arm® (IAR ™ EWARM) is a software development suite delivered with ready-made device configuration files, flash loaders and 4300 example projects included. IAR Systems® and STMicroelectronics closely cooperate in supporting 32-bit Arm® Cortex®-M based microcontrollers.

# Key Features

Key components:

Integrated development environment with project management tools and editor   
Highly optimizing C and C++ compiler for Arm®   
Automatic checking of MISRA C rules (MISRA C:2004)   
Arm® EABI and CMSIS compliance   
Extensive HW target system support   
Optional I-jet ™M and JTAGjet™M-Trace in-circuit debugging probes   
Power debugging to visualize power consumption in correlation with source code   
Run-time libraries including source code   
Relocating Arm® assembler   
Linker and librarian tools   
C-SPY® debugger with Arm® simulator, JTAG support and support for RTOS  
aware bugging on hardware   
RTOS plugins available from IAR Systems® and RTOS vendors   
Over 3100 sample projects for EVAL boards from many different manufacturers   
User and reference guides in PDF format   
Context-sensitive on-line help

Chip-specific support:

4300 example projects included for STMicroelectronics EVAL boards Support for 4 Gbyte applications in Arm® and Thumb® mode Each function can be compiled in Arm® or Thumb® mode VFP Vector Floating Point co-processor code generation

• Intrinsic NEON ™ support o ST-LINK and ST-LINK/V2 support

This product is supplied by a third party not affiliated to ST. For the latest information on the specification, refer to the IAR Systems® web site at http://www.iar.com.

# KeilMDK-Arm μVision

The MDK-Arm-STM32 is a complete software development environment for Cortex®-M microcontroller-based devices. It includes the µVision IDE/Debugger, Arm®C/C++ compiler and essential middleware components. The STM32 peripherals can be configured using STM32CubeMX and the resulting project exported to MDK-Arm.

Free MDK-Arm licenses can be activated for both STM32F0 and STM32L0 Series using the following Product Serial Number (PSN): U1E21-CM9GY-L3G4L.

This product is supplied by a third party not affiliated to ST. For the latest information on the specification refer to the third party's website: http://www2.keil.com/stmicroelectronicsstm32.

# Key Features

• Complete support for Cortex®-M devices   
• Arm® C/C++ compilation toolchain   
• uVision IDE, debugger and simulation environment   
• CMSIS Cortex® Microcontroller Software Interface Standard compliant   
• ST-LINK support   
• Multi-language support: English, Chinese, Japanese, Korean

# 2.2.4 STM32CubeProgrammer

STM32CubeProgrammer (STM32CubeProg) is an all-in-one multi-OS software tool for programming STM32 products.

It provides an easy-to-use and efficient environment for reading, writing and verifying device memory through both the debug interface (JTAG and SWD) and the bootloader interface (UART, USB DFU, I2C, SPI, and CAN). STM32CubeProgrammer offers a wide range of features to program STM32 internal memories (such as Flash, RAM, and OTP) as well as external memories. STM32CubeProgrammer also allows option programming and upload, programming content verification, and programming automation through scripting. STM32CubeProgrammer is delivered in GUI (graphical user interface) and CLI (commandline interface) versions.

# Key Features

Erases, programs, views and verifies the content of the device Flash memory   
o Supports Motorola S19, Intel HEX, ELF, and binary formats Supports debug and bootloader interfaces: ST-LINK debug probe (JTAG/SWD) UART, USB DFU, I2C, SPI, and CAN bootloader interfaces Programs, erases and verifies external memories, with examples of external Flash loaders to help users to develop loaders for specific external memories Automates STM32 programming (erase, verify, programming, configuring option bytes) Allows OTP memory programming Supports the programming and configuring of option bytes   
• Offers a command-line interface for automation through scripting   
• ST-LINK firmware update   
• Enables secure firmware creation using the STM32 Trusted Package Creator tool Supports OTA programming for the STM32WB Series Multi-OS support: Windows, Linux, macOS®

![](images/3b3d2a3c7b944fb19d089ef7ad7040255c92deb4e4a9efdd6166577f71042647.jpg)  
Figure 14. STM32Cube programmer

# 2.2.5 STM32CubeMonitor

The STM32CubeMonitor family of tools helps to fine-tune and diagnose STM32 applications at run-time by reading and visualizing their variables in real-time. In addition to specialized versions (power, RF, USB-PD), the versatile STM32CubeMonitor provides a flow-based graphical editor to build custom dashboards simply, and quickly add widgets such as gauges, bar graphs and plots. With non-intrusive monitoring, STM32CubeMonitor preserves the real-time behavior of applications, and perfectly complements traditional debugging tools to perform application profiling.

With remote monitoring and native support for multi-format displays, STM32CubeMonitor enables users to monitor applications across a network, test multiple devices simultaneously, and perform visualization on various host devices such as PCs, tablets, or mobile phones. Moreover, with the direct support of the Node-RED® open community, STM32CubeMonitor allows an unlimited choice of extensions to address a wide diversity of application types.

# Key Features

• Graphical flow-based editor with no programming needed to build dashboards   
• Connects to any STM32 device via ST-LINK (SWD or JTAG protocols)   
• Reads and writes variables on-the-fly from and to the RAM in real time while the target application is running   
• Parses debugging information from the application executable file   
• Direct acquisition mode or snapshot mode   
• Trigger to focus on application behaviors of interest   
• Enables to log data into a file and replay for exhaustive analysis   
• Delivers customized visualization with configurable display windows (such as curves and boxes) and a large choice of widgets (such as gauges, bar graphs and plots) Multi-probe support to monitor multiple targets simultaneously Remote monitoring with native support of multi-format displays (PCs, tablets, mobile phones) Direct support of the Node-RED® open community Multi-OS support: Windows®, Linux® Ubuntu® and macOS®

![](images/fa2a3ea4e57babe2a4b17c23822e45cd9dc01769fe52faa018ce090a94457100.jpg)  
Figure 15. STM32Cube monitor

# 2.3 Embedded software

The STM32Cube embedded software libraries provides:

The HAL hardware abstraction layer, enabling portability between different STM32   
devices via standardized API calls   
The Low-Layer (LL) APls, a light-weight, optimized, expert oriented set of APIs   
designed for both performance and runtime efficiency   
A collection of Middleware components, like RTOS, USB library, file system, TCP/IP   
stack, Touch sensing library or Graphic Library (depending on the MCU series)   
A complete set of code examples running on STMicroelectronics boards: STM32   
Nucleo, Discovery kits and EVAL boards

Tip: There is a fair chance that a Cube Project example matches the project in design. At project start or if an issue is met, it is worth browsing the complete project list package content available in CubeLibraryFolderProjectsl STM32CubeProjectsList.html (refer to Figure 16).

Figure 16. STM32CubeProjectList screenshot   

<table><tr><td rowspan=1 colspan=1>Level</td><td rowspan=1 colspan=1>Module Name</td><td rowspan=1 colspan=1>Project Name</td><td rowspan=1 colspan=1>Description</td><td rowspan=1 colspan=1>STM32L4R9IM EVAL</td><td rowspan=1 colspan=1>STM32L476G VAL</td></tr><tr><td rowspan=8 colspan=1></td><td rowspan=8 colspan=1>UART</td><td rowspan=1 colspan=1>LPUART_WakeUpFromStop</td><td rowspan=1 colspan=1>onguration   LAR  ak he CU from Sto mode whe  ivestimulus is received.</td><td rowspan=1 colspan=1>X</td><td rowspan=1 colspan=1>-</td></tr><tr><td rowspan=1 colspan=1>UART_HyperTerminal_DMA</td><td rowspan=1 colspan=1>UART transmission (transmit/receive) in DMA mode between a board and anHyperTerminal Capplication</td><td rowspan=1 colspan=1></td><td rowspan=1 colspan=1>X</td></tr><tr><td rowspan=1 colspan=1>UART_LowPower_HyperTerminal_DMA</td><td rowspan=1 colspan=1>LUART transmission transmit/receive) i DMA mode between  board and anHyperTeminal appliatin</td><td rowspan=1 colspan=1>X</td><td rowspan=1 colspan=1></td></tr><tr><td rowspan=1 colspan=1>UART_Printf</td><td rowspan=1 colspan=1>u  ART</td><td rowspan=1 colspan=1>X</td><td rowspan=1 colspan=1>x</td></tr><tr><td rowspan=1 colspan=1>UART_TwoBoards_ComDMA</td><td rowspan=1 colspan=1>UART transmission (transmit/receive) in DMA mode between two boards.</td><td rowspan=1 colspan=1></td><td rowspan=1 colspan=1></td></tr><tr><td rowspan=1 colspan=1>UART_TwoBoards_ComIT</td><td rowspan=1 colspan=1>UART transmission (transmit/receive) in Interrupt mode between two boards.</td><td rowspan=1 colspan=1></td><td rowspan=1 colspan=1></td></tr><tr><td rowspan=1 colspan=1>UART_TwoBoards_ComPolling</td><td rowspan=1 colspan=1>UART ransmissin ransmit/receve iPoln moebetweeoboards.</td><td rowspan=1 colspan=1></td><td rowspan=1 colspan=1></td></tr><tr><td rowspan=1 colspan=1>UART_WakeUpFromStop</td><td rowspan=1 colspan=1>u  A    stimulus is received.</td><td rowspan=1 colspan=1></td><td rowspan=1 colspan=1></td></tr></table>

# 2.4 Information and sharing

STMicroelectronics offers a very complete and wide range of solution on the web to get connected to STM32 World.

![](images/7e9f0cce7110bddc0a41e2d468075c77258488feec4ff05dc609d3b9b8fdde4a.jpg)  
Figure 17. Get connected to STM32 world

# 2.4.1 Documentation

Several types of documentation are available on www.st.com. Table 3 provides a reminder of the main technical documents with a short description of their contents.

Table 3. STMicroelectronics documentation guide   

<table><tr><td rowspan=1 colspan=1>Acronym</td><td rowspan=1 colspan=1>Name</td><td rowspan=1 colspan=1>Content</td></tr><tr><td rowspan=1 colspan=1>DB</td><td rowspan=1 colspan=1>Data Brief</td><td rowspan=1 colspan=1>Preliminary Product Specification before complete maturity</td></tr><tr><td rowspan=1 colspan=1>DS</td><td rowspan=1 colspan=1>Data sheet</td><td rowspan=1 colspan=1>Product Specifications, Hardware feature and Electrical Characteristics(Pinout/Alternate function definition table, Memory Map, ElectricalCharacterization etc.)</td></tr><tr><td rowspan=1 colspan=1>RM</td><td rowspan=1 colspan=1>Reference manual</td><td rowspan=1 colspan=1>How to use the targeted microcontroller series, memory andperipherals.(registers details, default/reset value etc.)</td></tr><tr><td rowspan=1 colspan=1>AN</td><td rowspan=1 colspan=1>Application note</td><td rowspan=1 colspan=1>&quot;How to make&quot; guide helping to achieve a specific application with thetargeted MCU.</td></tr><tr><td rowspan=1 colspan=1>UM</td><td rowspan=1 colspan=1>User manual</td><td rowspan=1 colspan=1>&quot;How To Use&quot; guide for a specific software of hardware product (board,software tools etc.)</td></tr><tr><td rowspan=1 colspan=1>TN</td><td rowspan=1 colspan=1>Technical note</td><td rowspan=1 colspan=1>Very brief document addressing single technical aspect. Can be seen as acomplement of AN or UM documents</td></tr><tr><td rowspan=1 colspan=1>ES</td><td rowspan=1 colspan=1>Errata sheet</td><td rowspan=1 colspan=1>Contained known issues and device limitation.</td></tr><tr><td rowspan=1 colspan=1>PM</td><td rowspan=1 colspan=1>Programmer manual</td><td rowspan=1 colspan=1>Target software developer with a full description of the STM32 Cortex®-Mprocessor programming model, instruction set and core peripherals</td></tr><tr><td rowspan=1 colspan=1>RN</td><td rowspan=1 colspan=1>Release note</td><td rowspan=1 colspan=1>It describes new features, known limitations and corrections on a specificsoftware release for an evaluation board, a reference design, a software orprogramming or debugging tool.</td></tr></table>

# 2.4.2 Wiki platform

STMicroelectronics offers the wiki platform to help developers to use its STM32 devices.

This user guide aims at assisting developers to use STM32 MCU devices from STMicroelectronics.

It contains articles to discover STM32 MCUs, as well as examples and helps:

• The Getting started to easily start with an STM32 MCU board in C The Development zone to help developing applications and share projects • The Software tools zone for a first contact with the tools The Training zone to get trained on STM32 MCUs

The home page of wiki is https://wiki.st.com/stm32mcu/index.php/

# Note:

Two wiki spaces are currently proposed: one dedicated to STM32 Microcontroller (MCU products and one for STM32 Microprocessor (MPU) products. The focus of this application note is on the those dedicated to STM32 microcontrollers.

# 2.4.3 Github

STMicroelectronics is now publishing STM32Cube embedded software on GitHub, the popular cloud-based service. The aim is to open up the STM32 integrated software offering to collaborative and community-friendly development and take advantage of faster and more efficient distribution of updates.

Publishing all STM32Cube original code through GitHub lets users of more than 1000 STM32 Arm® Cortex®-M microcontroller variants and heterogeneous Cortex-M/-A microprocessors to easily store, manage, track, and control their code. GitHub features such as Pull requests promote co-development, enabling the community to propose alternate solutions and new features taking advantage of GitHub's change-handling structures. In addition, GitHub Issues - the privileged communication channel between developers - lets users submit problems, share solutions, and contribute to fixes.

The move to GitHub also ensures that the developers can receive all software updates as soon as they are published, more quickly than traditional means of updating MCU packages.

All current STM32Cube MCU packages are already online, as well as hardware abstraction layer (HAL) code and MCU-independent CMSIS drivers. The remaining STM32Cube embedded-software components will be added over the coming months.

All STM32Cube embedded software on GitHub is available free of charge. Please visit https://github.com/STMicroelectronics for more information or to get started.

# 2.4.4 ST Community

STMicroelectronics new community is now live and ready for receiving questions, sharing projects and collaborating among fellow community members. The focus is on collaboration because the primary purpose of this community is to share with peers and help them in a transparent way that showcases the world of STMicroelectronics products, activities and achievements.

The home page of ST Community is https://community.st.com/welcome.

For any problem met, it is interesting to first browse the STM32 Forum for related topics and eventually to post a new one if no relevant thread is found.

# 2.4.5 STM32 Education

STM32 education material is available on-line at www.st.com (search for STM32 Education).

This site provides free educational resources created by STMicroelectronics engineers for bringing an STM32 project to life.

On this site, a user learns at his own pace, watches classes as per his own schedule, anytime, anywhere, on any device, or apply to one of the live learning sessions led by STMicroelectronics experts at a nearby location.

# Content:

• Online Training   
• MOOC   
• Videos   
• Webinar Textbooks   
• ST training courses   
• Partner training courses

# 3 Compiling for debug

This chapter reviews the various options for debug-friendly compiling solutions.

# 3.1 Optimization

Compiler are usually configured by default to optimize performance and/or code size. In most cases, this reduces or even prevents program debugging.

The most common symptoms resulting from code optimization are:

Problem to set or reach a breakpoint. Some lines are not accessibli • Impossibility to evaluate a variable (watch feature). Inconsistency while stepping (what I get, is not what I see).

Therefore, for efficient debugging it is recommended to modify the code optimization option.

# 3.1.1 IAR™ EWARM

# In Project->option->C/C++Compiler->Optimization

![](images/ee83e89733264eae70194962b9a75d8d011318ea2e98d00f08037d784e2cf7ef.jpg)  
Figure 18. IAR™ EWARM Optimization option

# 3.1.2 Keil® MDK-Arm μVision

# In Project Option for Target->C/C++->Optimization

![](images/2140c28d6cfa41c42fe512839cb1348675eeb12b43d2903209b7ea1e57cd98ae.jpg)  
Figure 19. Keil® μVision Code Optimization option

Keil docentaton ggets hat Leve  cane suitable altenativor.

Refer to www.keil.com support page Compiler optimization levels and the debug view for details.

# 3.1.3 STM32CubeIDE

# In project Properties->Settings->Tool Settings->MCU GCC Compiler->Optimization

![](images/45c52696bfc58e3ce89e70d607076b25b267d89d33ce8b513258e1e6d0c1471e.jpg)  
Figure 20. STM32CubelDE optimization level setting

gcc also provides the -Og option:

-Og enables optimizations that do not interfere with debugging. It offers a reasonable level of optimization while maintaining fast compilation and a good debugging experience.

# 3.2 Debugging information

Debugging information is generated by the compiler together with the machine code. It is a representation of the relationship between the executable program and the original source code. This information is encoded into a pre-defined format and stored alongside the machine code.

Debugging information is mandatory to set breakpoint or get the content of a variable.

This chapter presents the location of the Debugging Information related option in IAR ytemsKeiland STCuIDE.

# 3.2.1 IAR ™M EWARM

Generate debug information" option tick box is accessible in

Project -> Options -> C/C++ Compiler -> Output Pane It is set by default.

![](images/79d85676fe09b7bb40851fa67d202bc370a60cc64e5bda48c244c9a556b5d991.jpg)  
Figure 21. IAR™ EWARM Generate debug Information option

# 3.2.2 Keil®-MDK-Arm μVision

Debug Information Tick box is accessible in

Project -> Options -> Output Pane.

It is set by default.

![](images/d3fd79e8a52096f7fc74c264a0832764b93bb40f137f9ae9165e66c673a9b5d7.jpg)  
Figure 22. Keil® Debug Information option

# 3.2.3 STM32CubeIDE

Option to manage Debugging Information are in

Properties-> C/C++ Build -> Settings - Tool Settings -> Debugging.

![](images/c475d435a9dedf5cc40f3077994d8dc8ce38d600c7a19b613513533ad5861076.jpg)  
Figure 23. STM32CubelDE debug information option

Debug Level can be set among four levels:

None: Level 0 produces no debug information at all;   
Minimal (-g1): Level 1 produces minimal information, enough for making backtraces in parts of the program for which no debug is planned. This includes descriptions of functions and external variables, and line number tables, but no information about local variables.   
Default (-g): Produce debugging information in the operating system's native format (stabs, COFF, XCOFF, or DWARF). GDB can work with this debugging information. Maximal (-g3): Level 3 includes extra information, such as all the macro definitions present in the program. Some debuggers support macro expansion when -g3 is used.

The same pane contains the options to add profiling information.

For urthe normation, rer  Sectin3.Option Summary available  http:/c..

# 4 Connecting to the board

The way IDEs get connected to the boards is not always known. In case of trouble, a basic knowledge about this topic can save time in identifying and fixing the issue.

This chapter intends to provide the minimal set of information in order to prevent or quickly fix issues related to connection.

# 4.1 SWD/JTAG pinout

On STMicroelectronics hardware kits, SWD must be made available for connection with ST-LINK.

SWD is always mapped on PA13 (SWDIO) and PA14 (SWCLK). This is the default state after reset.

Nothing specific is required in the application code to make SWD work.

Special attention must be paid to make sure that, voluntarily or accidentally, the SWD pins are not switched to some alternate functions or affected by l/O settings modifications.

Hint: For instance, STM32Cube PWR examples switch all GPIO (including SWD) in an analog state in order to minimize consumption. This disconnects the debugger. A Connect Under Reset using NRST is required to take back the control of the board. (Refer to Section 4.2).

When using STM32CubeMX at configuration stage, PA13 and PA14 can be in one of three states upon selection of Serial Wire in SYS/Debug configuration list:

Reset, shown by the pins colored in gray in Figure 24 Reserved but inactive shown by the pins colored in orange in Figure 25 • Active shown by the pins colored in green in Figure 26

![](images/4e74cc105d894cebfc2a03b2b351a9be2960bbc8165ce7f11766bfd2929935ed.jpg)  
Figure 24. SWD pins PA13 and PA14 in Reset state under STM32CubeMX

![](images/b11045e9df36cdb7afd771c2bbf51a6a6ba4ce69ccdb4bcbc4c8153a3e46b04a.jpg)  
Figure 25. SWD pins PA13 and PA14 in Reserved but inactive state under STM32CubeMX

![](images/9367d8b982893c80b3d0211c8168c601d4639691d326942a6eff7ce2fecdab81.jpg)  
Figure 26. SWD pins PA13 and PA14 in Active State under STM32CubeMX

All three states are functional from SWD connection point of view.

It is anyway recommended to explicitly activate the SWD pins by selecting "Serial Wire" or Trace Asynchronous SW" (together with SWO. Refer to Section 7.3 on page 71). This is the only way by which STM32CubeMX protects the l/O from being selected for another use during the configuration process by highlighting the conflict to the user.

JTAG is not available on Nucleo and Discovery boards.

On EVAL boards, it is available through a dedicated 20-pin connector.

Nevertheless, in STM32CubeMX, SWD remains the default and preferred debug port. For this reason, extra JTAG pins are not reserved. It is then strongly advised to explicitly enable the desired JTAG configuration.

Especially since JTAG is using more pins, users should be aware that it is at the expense of using some IPs.

Refer to the product datasheet for a detailed presentation of the default and alternative function mapping for each pin.

# 4.2 Reset and connection mode

This section reviews the reset and connection mode available while using ST-LINK/V2or STLINK/V3 debug interface.

# 4.2.1 Presentation

Connection mode and reset mode are 2 different but dependent concepts:

Reset mode can be either:

Hardware: drive the NRST pin of the MCU. In all STMicroelectronics hardware kits, the debugger can drive this NRST through ST-LINK/V2 or ST-LINK-V3.

Hint: On Nucleo, check that relevant Solder Bridge SB12 is not OFF.

Software (write to core register) System: Core and all Peripheral SOC IPs are reset Core: Only Arm® Cortex® is reset

Connection mode can be either:

Normal: Debugger takes control through JTAG/SWD port and starts execution after a software reset.

This is working only if JTAG/SWD is available:

GPIO correctly configured and clocked FCLK or HCLK enabled Main Power domain or Low-Power debug active

ConnectUnderReset: Debugger takes control while asserted NRST pin, setting GPIO and clock into there default state.   
This is required in case of a reconnection to a system in Low-Power mode or which has changed SWD pin to alternate functions.   
Hotplug: Debugger connect without reset nor halt. Once connected, the user can chose to perform the required action (typically halt to get where the program stands and read registers or memory for instance).

Reset and Connection mode are differently accessible and exposed depending on tool and IDE.

# 4.2.2 IAR ™ EWARM

Reset and Connection mode are seen as a single reset mode option as shown in Figure 27.

![](images/646bf8a9e6d4994e5cd89184d84a81ed45c2cf235c5fff71aa69085f31870989.jpg)  
Figure 27. Reset Mode in IAR8.10: screenshot

System (default): Normal Connection. Software System Reset prior to jump at main. Core: Normal Connection. Software Core Reset prior to jump at main. • Software: Normal Connection. No Reset prior to jump and stop at main. • Hardware: Normal Connection. Assert NRST MCU pin prior to jump to main. • Connect during reset: Connection while asserted Hardware NRST.

Hotplug connection is accessible with "Attach to running Target" function in project menu.

# 4.2.3 Keil© MDK-Arm μVISION

Can be set through

Project -> Options -> Debug -> Settings -> Debug

![](images/da9390904ec19fff9c15ff0aa1ed1b3434cc0161a68546483487bca991db7a83.jpg)  
Figure 28. Connect and Reset option Keil®

Connect: controls the operations that are executed when the pVision debugger connects to the target device. The drop-down has the following options:

• Normal just stops the CPU at the currently executed instruction after connecting.   
• with Pre-reset applies a hardware reset (HW RESET) before connecting to the device.   
• under Reset holds the hardware reset (HW RESET) signal active while connecting to the device. Use this option when the user program disables the JTAG/SW interface by mistake.

Reset after Connect: performs (if enabled) a reset operation as defined in the Reset dropdown list (see below) after connecting to the target. When disabled, the debugger just stops the CPU at the currently executed instruction after connecting the target.

Reset: controls the reset operations performed by the target device. The available options vary with the selected device.

Autodetect selects the best suitable reset method for the target device. This can be a specialized reset or standard method. If Autodetect finds an unknown device, it uses the SYSRESETREQ method.   
HW RESET performs a hardware reset by asserting the hardware reset (HW RESET) signal.   
SYSRESETREQ performs a software reset by setting the SYSRESETREQ bit. The Cortex®-M core and on-chip peripherals are reset.   
VECTRESET performs a software reset by setting the VECTRESET bit. Only the Cortex®-M core is reset. On-chip peripherals are not reset. For some Cortex®-M devices, VECTRESET is the only way they may be reset. However, VECTRESET is not supported on Cortex®-M0, Cortex®-M0+, Cortex®-M1, and Arm®v8-M cores.

Refer to http://www.keil.com/

# Hotplug

If all of the following options are disabled, no hardware reset is performed at debugger start:

Options for Target -> Debug - Load Application at startup

Options for Target -> Debug -> Settings -> Reset after connect (with Options for Target - > Debug -> Settings -> Connect selected as NORMAL)

Targetiltspdate Target before e

![](images/0fd0503b27fd2c853354b49a495b733611194b465e5dbefc22ab7bcea63468f3.jpg)  
Figure 29. Keil® hotplug step1

![](images/4bc183274bae0b4bc38bb0ef465b1587699e5d4272095d536acc51474ef8bc54.jpg)  
Figure 30. Keil® hotplug step2

![](images/443dd66518a8a8b016a0c72bc08521f553b45b12528812f5fd8301a97660584b.jpg)  
Figure 1. Keil® hotplug step3

With these options disabled, the debugger starts, and the target hardware stops at the current location of the program counter. This allows to analyze the memory and register content.

Because Options For Target - Debug - Load Application at startup is disabled, the debugger does not have any application program and debug information. To load this information into the debugger, use the LOAD debugger command with the option NORESET or INCREMENTAL.

LOAD can be automated using an Initialization Fileunder Options For Target  Debug.

To go further, refer to http:/www.keil.com/.

# 4.2.4 STM32CubeIDE

Reset and connection modes can be changed through

Run -> Debug Configurations -> Debugger

![](images/38112409045902217ee93e2e175844da3341e28b2ee75b7ee9995a5fe9033aae.jpg)  
Figure 32. Select Generator Options Reset Mode

The Mode Setup group allows to set up the Reset Mode along with other debug behaviors.

Reset Mode as Connect under reset: asserts hardware reset and then connects to the target (under reset).   
• Reset Mode as None: performs a hardware reset and then connects to the target.   
• Reset Mode as Software system reset: does not perform any hardware reset but connects to the target and performs a software system reset.

In case of problem to connect to the board with STM32CubeIDE, make sure that NRST from ST-LINK is properly connected to STM32 NRST.

Hotplug mode is not proposed by STM32CubelDE. STM32CubeProgrammer can be used instead.

# 4.2.5 STM32CubeProgrammer

Reset and Connection modes can be selected in the ST-LINK configuration Pane.

![](images/7583ada879fc5b2f7467ef67d8d0983bede46c66afc075f858372df1dbf55891.jpg)  
Figure 33. STM32CubeProgrammer Reset mode

Software system reset: Resets all STM32 components except the Debug via the Cortex-M application interrupt and reset control register (AIRCR). Hardware reset: Resets the STM32 device via the nRST pin. The RESET pin of the JTAG connector (pin 15) must be connected to the device reset pin. C Core reset: Resets only the core Cortex-M via the AlRCR

![](images/bde32217093d569c39bd0a018368cfd4e168b47233ed6e7fb4fc013bd1f2d286.jpg)  
Figure 34. STM32CubeProgrammer Connection mode

With 'Normal' connection mode, the target is reset then halted. The type of reset is selected using the 'Reset Mode' option.   
The 'Connect Under Reset' mode enables connection to the target using a reset vector catch before executing any instructions. This is useful in many cases, for example when the target contains a code that disables the JTAG/SWD pins.   
The 'Hot Plug' mode enables connection to the target without a halt or reset. This is useful for updating the RAM addresses or the IP registers while the application is running.

In Kei® MDK-Arm μVISION, IAR™ EWARM and STM32CubeProgrammer, in case NRST is not connected on the board or PCB a silent falback operates with a System Reset. In case of failure to take control of a board despite the use of Connection UnderReset / Hardware, check the NRST connection on the board.

# 4.3 Low-power case

By default, the debug connection is lost if the application puts the MCU in Sleep, Stop, or Standby mode while the debug features are used. This is due to the fact that the Cortex®-M core is not clocked in any of these modes.

However, the setting of dedicated configuration bits in the DBGMCU_CR register allows software debug even when the low-power modes are used extensively.

Refer to the PWR and DBG sections of the reference manual for details.

Appendix A: Managing DBGMCU registers on page 95 guides the user through the various means to manage DBGMCU depending on IDE and needs.

# Caution:

In order to reduce power consumption, some applications turn all GPlOs to analog input mode, including SWD GPIOs. This is the case for all PWR examples provided in STM32Cube (debug connection is lost after SystemPower_Config () which sets all GPIOs in Analog Input State).

Enabling low-power debug degrades power consumption performance by keeping some clocks enabled and by preventing to optimize GPlO state. Even if this is useful for functional debugging, it has anyhow to be banned as soon as the target is to measure/enhance power consumption.

All DBGMCU registers values are kept while reset. Users must pay attention not to let debug or unwanted states when returning to normal execution (refer to Section 9: Dual-Core microcontroller debugging on page 92).

# 5 Breaking and stepping into code

This chapter provides users with highlights about a few points affecting system behavior at code break.

# 5.1 Debug support for timers, RTC, watchdog, BxCAN and I2C

During a breakpoint, it is necessary to choose how the counter of timers, RTC and watchdog should behave:

They can continue to count inside a breakpoint. This is usually required when a PWM is controlling a motor, for example. • They can stop counting inside a breakpoint. This is required for watchdog purposes.

For the BxCAN, the user can choose to block the update of the receive register during a breakpoint.

For the I2C, the user can choose to block the SMBuS timeout during a breakpoint.

Those options are accessible in DBGMCU freeze registers (DBGMCU_APB1FZR1, DBGMCU_APB1FZR2) which can be written by the debugger under system reset.

If the debugger host does not support these features, it is still possible to write these registers by software.

Refer to Appendix A: Managing DBGMCU registers on page 95 to find suitable ways to handle debug options depending on IDEs and needs.

# 5.2 Debug performance

To save flashing time and improve debugger reactivity when stepping, make sure that the higher SWD frequency possible is used with the probe.

When using IAR ™M EWARM, or Keil® MDK-Arm µVISION speed is set at speed is set at 1.8 MHz by default. On system with a core clock greater than 1 MHz, it is safe to use the highest 4 MHz SWD speed.

# 5.2.1 IAR ™ EWARM

# In Project -> Option -> ST-LINK -> Interface speed

![](images/681c24d4eb0de77bfab3a75bef9e3cd96329a5444c258b1e72bfe8bf5371891a.jpg)  
Figure 35. IAR™ EWARM ST-LINK SWD Speed setting

# 5.2.2 Keil© MDK-Arm μVISION

SWD Speed setting is accessible in

Project -> Options for Target.. -> Debug -> Settings -> Target Com

![](images/6df53b26b6ea59521f5a65ed91511223c3244f2681034aca45c5bd2bcc4de8b4.jpg)  
Figure 36. Kei® SWD Speed Setting

# 5.2.3 STM32CubelDE

# In Run -> Debug Configuration -> Debugger Pane

![](images/22fb0308ba74ef687ed499e9034b1824bd0f3233ac34ec7aa15c99c565d48297.jpg)  
Figure 37. Access to Generator Options in STM32CubelDE V2.0.0

# Note:

SWD communication is always possible on all ST boards whereas JTAG is only present on EVAL boards.

SWD communication is always present on all Cortex®-M devices whereas JTAG is not present on Cortex®-MO(+) devices. Refer to Appendix D on page 116 for a complete overview of debug capabilities for each Cortex®-M type.

# 5.3 Secure platform limitation

The STMicroelectronics platform provides the following code protection means.

RDP: ReadOut Protection

Prevents Flash Memory access through the JTAG for ALL Flash memory.

PcROP: Proprietary Code ReadOut Protection

Prevents read access of configurable Flash memory areas performed by the CPU execution of malicious third-party code (Trojan Horse).

WRP: Prevents accidental or malicious write/erase operations

For further details please refer to the reference manual or section Training L4 on STMicroelectronics website www.st.com.

The next sections provide additional details on the expected behavior of the secure applications.

# 5.3.1 RDP

o Level O: No Protection. This is the factory default mode allowing all accesses. Level 1: Read Protection. Any access to Flash or protection extension region generates a system hard-fault which blocks all code execution until the next power-on reset. A simple reset does reenable code execution; power must be switched off and on so that power-on reset enables code execution. The restriction depends on the STM32 Series as described in Table 4.

Table 4. STM32 Series RDP protection extension   

<table><tr><td rowspan=1 colspan=1>Product</td><td rowspan=1 colspan=1>RDP protection extension</td></tr><tr><td rowspan=1 colspan=1>FO</td><td rowspan=1 colspan=1>+ backup registers</td></tr><tr><td rowspan=1 colspan=1>F2</td><td rowspan=1 colspan=1>+ backup SRAM</td></tr><tr><td rowspan=1 colspan=1>F3</td><td rowspan=1 colspan=1>+ backup registers</td></tr><tr><td rowspan=1 colspan=1>F4</td><td rowspan=1 colspan=1>+ backup SRAM</td></tr><tr><td rowspan=1 colspan=1>LO</td><td rowspan=1 colspan=1>+ EEPROM</td></tr><tr><td rowspan=1 colspan=1>L1</td><td rowspan=1 colspan=1>+ EEPROM</td></tr><tr><td rowspan=1 colspan=1>L4</td><td rowspan=1 colspan=1>+ backup registers+ SRAM2</td></tr><tr><td rowspan=1 colspan=1>L5</td><td rowspan=1 colspan=1>RDP 4 levels+ backup registers + SRAM2</td></tr><tr><td rowspan=1 colspan=1>F7</td><td rowspan=1 colspan=1>+ backup SRAM</td></tr><tr><td rowspan=1 colspan=1>H7</td><td rowspan=1 colspan=1>+ backup SRAM</td></tr></table>

Thus, any attempt to load, or connect to, an application running from Flash crashes.   
It is still possible to load, execute and debug an application in SRAM.

Option Bytes management can be done with ST-LINK utility or with an application running from SRAM.

Going back to RDP Level 0 completely erases the Flash.

Level 2: No Debug. JTAG/SwD connection is killed. There is no way back. In this case, nobody - even STMicroelectronics - can perform any analysis of defective parts. Level 0.5 is an additional protection level associated with TrustZone(only available in STM32L5 Serie). RDP 0.5 is available only when TrustZone is enabled. Debug of secure domain is forbidden, only non-secure domain can be accessed for debug. Regression from level 0.5 to level 0 triggers a Flash mass erase, as well as backup registers and all SRAMs.Regression from RDP Level 1 to RDP Level 0.5 leads to a partial Flash memory erase: only the non-secure part is erased

Note:

Refer to AN5421 and AN5347 for more informations about Trustzone development on STM32L5 Series.

# 5.3.2 PCROP

Proprietary Code ReadOut Protection is the ability to define secure area in Flash where user can locate a proprietary code.

This prevents malicious software or debugger from reading sensitive code.

In case an application with third party code in PCROP area needs to be debugged, the following points must be considered:

Step-into PCROP function is tolerated but ignored (Step-over) Access to protected memory through debugger trigs Flash Interruption (Instrument NMIHandler) and return default pattern for the whole area

For further details refer to section Memory Protection in the reference manual of the device.

# 6 Exception handling

It is usually helpful, or even mandatory in complex project, to properly trap and find root cause of software exception like HardFault and NMl. This chapter intends to make the user aware of a few techniques used to help investigating such issue.

In order to get deeper into the subject, the user can usefully refer to Joseh Yiu's work and book collection The Definitive Guide to Arm-Cortex-M, and to Carmelo Noviello's recent online guide Mastering STM32.

# 6.1 Default weak Handlers

By default Handlers are implemented as _weak functions which perform endless loops:

_vector_table

<table><tr><td>DCD</td><td colspan="3">sfe(CSTACK)</td></tr><tr><td>DCD</td><td>Reset_Handler</td><td></td><td>; Reset Handler</td></tr><tr><td>DCD</td><td>NMI_Handler</td><td></td><td>; NMI Handler</td></tr><tr><td>DCD</td><td>HardFault_Handler</td><td></td><td>; Hard Fault Handler</td></tr><tr><td>DCD</td><td>0</td><td></td><td>; Reserved</td></tr><tr><td>DCD</td><td>0</td><td></td><td>; Reserved</td></tr><tr><td>DCD</td><td>0</td><td></td><td>; Reserved</td></tr><tr><td>DCD</td><td>0</td><td></td><td>; Reserved</td></tr><tr><td>DCD</td><td>0</td><td></td><td>; Reserved</td></tr><tr><td>DCD</td><td>0</td><td></td><td>; Reserved</td></tr><tr><td>DCD</td><td>0</td><td></td><td>; Reserved</td></tr><tr><td>DCD</td><td>SVC_Handler</td><td></td><td>; SVCall Handler</td></tr><tr><td>DCD</td><td>0</td><td></td><td>; Reserved</td></tr><tr><td>DCD</td><td>0</td><td></td><td>; Reserved</td></tr><tr><td>DCD</td><td>PendSv_Handler</td><td></td><td>; PendSV Handler</td></tr><tr><td>DCD</td><td>SysTick_Handler</td><td></td><td>; SysTick Handler</td></tr></table>

Nothing is trigged on debugger side and application looks hanged / stuck.

In that case, code break is needed and the PC must be at the address of the Handler.

Some IDEs provide the faulty calling code through Call stack window. (Keil® MDK-Arm μVision, STM32CubelDE).

If it is not the case, display registers and find the faulty code address in SP + 0x18

In STM32CubelDE all weak default handlers point to the same DefaultHandler which can be confusing.

A more efficient approach is to trap the exception by instrumenting Handlers.

# 6.2 Custom Handlers

One way to generate templates of Handler functions is to use STM32CubeMX.

In Configuration -> NVIC Configuration -> Code Generation, use Generate IRQ handler tick boxes as shown in Figure 38.

Figure 38. Asking for Handler code generation   

<table><tr><td rowspan=1 colspan=1>Enabled interrupt table</td><td rowspan=1 colspan=1></td><td rowspan=1 colspan=1></td></tr><tr><td rowspan=1 colspan=1>Non maskable interr..</td><td rowspan=1 colspan=1></td><td rowspan=1 colspan=1>M</td></tr><tr><td rowspan=1 colspan=1>Hard fault interrupt</td><td rowspan=1 colspan=1></td><td rowspan=1 colspan=1>M</td></tr><tr><td rowspan=1 colspan=1>Memory manageme...</td><td rowspan=1 colspan=1></td><td rowspan=1 colspan=1>M</td></tr><tr><td rowspan=1 colspan=1>Prefetch fault, mem...</td><td rowspan=1 colspan=1></td><td rowspan=1 colspan=1>M</td></tr><tr><td rowspan=1 colspan=1>Undefined instructio...</td><td rowspan=1 colspan=1></td><td rowspan=1 colspan=1>V</td></tr><tr><td rowspan=1 colspan=1>System service call..</td><td rowspan=1 colspan=1></td><td rowspan=1 colspan=1>M</td></tr><tr><td rowspan=1 colspan=1>Debug monitor</td><td rowspan=1 colspan=1></td><td rowspan=1 colspan=1>M</td></tr><tr><td rowspan=1 colspan=1>Pendable request fo...</td><td rowspan=1 colspan=1></td><td rowspan=1 colspan=1></td></tr><tr><td rowspan=1 colspan=1>Time base: System...</td><td rowspan=1 colspan=1></td><td rowspan=1 colspan=1>M</td></tr></table>

When Non maskable interrupt and Hard fault interrupt are selected, the following code is generated:

void NMI_Handler(void)   
{ /\* USER CODE BEGIN NonMaskableInt_IRQn 0 \*/ /\* USER CODE END NonMaskableInt_IRQn 0 \*/ /\* USER CODE BEGIN NonMaskableInt_IRQn 1 \*/ /\* USER CODE END NonMaskableInt_IRQn 1 \*/   
}   
/\*\*   
\* @brief This function handles Hard fault interrupt.   
\*/   
void HardFault_Handler(void)   
{ /\* USER CODE BEGIN HardFault_IRQn 0 \*/ /\* USER CODE END HardFault_IRQn 0 \*/ while (1) { } /\* USER CODE BEGIN HardFault_IRQn 1 \*/ /\* USER CODE END HardFault_IRQn 1 \*/   
}

This simple declaration overriding the default weak function,removes ambiguity and clarifies the call stack.

In order to trap the exception, a hardware or a software breakpoint can be set in the IDE or directly programmed in the source code using Arm® instruction BKPT.

# Caution:

BKPT is not tolerated if no debugger is connected (refer to Chapter 9: Dual-Core microcontroller debugging on page 92). it is advised to set it under #ifdef statement.

In-line insertion of assembly instruction in application C code depends on the IDE.

IAR ™M EWARM and STM32CubeIDE void NMI_Handler(void)   
{   
#ifdef DEBUG   
asm ("BKPT O");   
#endif   
}   
Keil®   
void NMI_Handler(void)   
{   
#ifdef DEBUG _asm { BKPT 0 }   
#endif   
}

For each IDE, it is also possible to use the abstraction function defined in the CMSIS library and provided in STM32Cube software pack.

void NMI_Handler(void)   
{   
#ifdef DEBUG   
BKPT(O);   
#endif   
}   
In all cases, the Halt Debug-Mode is entered; it allows to investigate the issue by inspecting Call Stack and Registers content.

![](images/d649fe8eae0cd12be306ba485cd298c9df6622b6b7939be76870e3cedd7d8d97.jpg)  
Figure 39. Keil® Access to Show Caller Code in Contextual menu

# 6.3 Trapping div/0 exception

Most often, code execution causing a division by zero are difficult to investigate:

Nothing is neither triggered nor trapped.   
Erroneous returned value generates an unexpected and unpredictable behavior that is very difficult to analyze.

This chapter gives several tips in order to properly trap div/0 exceptions.

# 6.3.1 Cortex®-Mo/MO+ case

For targets that do not support hardware division instructions (SDIV/UDIV), integer divisionby-zero errors can be trapped and identified by means of the appropriate C library helper functions:

_aeabi_idivo()

When integer division by zero is detected, a branch to _aeabi_idivo () is made.A breakpoint placed on __aeabi_idiv0() allow to trap the division by zero.

To ease the breakpoint application, override the default function:   
void _aeabi_idivo()   
{ #ifdef DEBUG BKPT(0); #endif   
}

This way, and depending on IDE, the call stack or registers can be examined and the offending line in the source code can be rapidly found.

To go further refer to section 7.7 of Arm® Compiler Software Development Guide.

# 6.3.2 Cortex®-M3/4/7 case

For targets that support hardware division instructions, Trapping of Div0 operation is possible by configuring System Control Block (SCB) registers, accessible through CMSIS library.

For example on Cortex®-M3:

SCB_CCR register description is provided in Figure 40.

Figure 40. Cortex®-M3 SCB_CCR Description   
Figure 41. Cortex-M3 SCB_CFSR Description   

<table><tr><td>31</td><td></td><td>30</td><td>29</td><td>28</td><td>27</td><td>26</td><td>25</td><td>24</td><td>23</td><td>22</td><td>21</td><td></td><td>18</td><td>17</td><td></td><td>16</td></tr><tr><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td>Reserved</td><td></td><td></td><td>20</td><td>19</td><td></td><td></td><td></td><td></td></tr><tr><td></td><td>15</td><td>14</td><td>13</td><td></td><td></td><td>9</td><td></td><td>7</td><td>6</td><td>5</td><td>4</td><td>3</td><td>2</td><td>1</td><td></td><td></td></tr><tr><td></td><td></td><td></td><td></td><td>12</td><td>11</td><td>10</td><td></td><td>8</td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td>0 NON</td></tr><tr><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td>STK</td><td>BFHF</td><td></td><td></td><td>DIV_O_</td><td>UN ALIGN</td><td></td><td>USER SET</td><td>BASE</td><td></td></tr><tr><td></td><td></td><td></td><td>Reserved</td><td></td><td></td><td></td><td>ALIGN</td><td>NMIGN</td><td>Reserved</td><td></td><td>TRP</td><td>TRP</td><td>Res.</td><td>MPEND</td><td>THRD</td><td></td></tr><tr><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td>ENA</td><td></td></tr><tr><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td></tr><tr><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td>Iw</td><td>rw</td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td></tr><tr><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td></tr><tr><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td>rw</td><td>Iw</td><td></td><td>rw</td><td>rw</td><td></td></tr><tr><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td></tr><tr><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td></tr><tr><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td></tr><tr><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td></tr><tr><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td></tr><tr><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td></tr><tr><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td></tr><tr><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td></tr><tr><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td></tr><tr><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td></tr><tr><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td></tr><tr><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td></tr><tr><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td></tr><tr><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td></tr><tr><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td></tr><tr><td></td><td></td><td></td></table>

Refer to STM32F10xxx/20xxx/21xxx/L1xxxx Cortex-M3 programming manual (PM0056).

Setting bit 5 of SCB_CCR register

SCB->CCR |= 0x10; // enable div-by-0 trap

When Div0 occurs it is trapped in HardFault_Handler.

With breakpoint on while instruction into HardFault_Handler, CallStack point to the offended line and SCB->CFSR register explicits the type of fault

SCB_CFSR register description is provided in Figure 41.

31 1615 8 7 0 Usage Fault Status Register Bus Faull Status Mamory Management UFSR BFSR MMFSR 31 30 29 28 27 26 25 24 23 22 21 20 19 18 17 16 DZEBRY Y UGNEL D NOCP INVPC STATE E UNDTER Reserved Reserved rc_w1 rc_w1 rc_w1 rc_w1 rc_w1 rc_w1   
15 14 13 12 11 10 9 8 7 6 5 4 3 2 1 0   
BARD Reserved SETR USTR MPRE E PSRER EBUS S MALAR Reserved MESTK K UEATR Res. DVAOL AIOL rw rw rw rw rw rw rw rw rw rw rw

The following sections describe the management of SCB registers as a function of the selected IDE.

# IARTM EWARM

Detailed R/W access to the values of each SCB registers bits at runtime can be obtained through View -> Register -> System Control Block (from Pick List) as shown in Figure 42

![](images/04155e4bbd73648e3d1818f9a292c5a690cc012540d9c371e883bf5fe8272ba4.jpg)

# Keil® MDK-Arm μVISION

SCB->CCR can be managed at run time through View -> System Viewer -> Core Peripheral -> System Control and Configure.

Refer to Figure 43 for details.

![](images/04da2b268b3166a48c186782d1d165c324c651332161dab20353c440e70d898e.jpg)  
Figure 43. Keil® System Control and Configure

The fault type can be investigated using Peripherals -> Core Peripherals -> Fault Reports as shown in Figure 44.

![](images/fe89d2f890dcba7f4208c2097bf0e66f66b03fac971556c7521cfb13ed4a9ca3.jpg)  
Figure 44. Keil® Fault Reports

# STM32CubeIDE

At runtime, while debug is in break state, the SCB register can be accessed in read mode or in write mode through: Window -> Show View -> SFRs as shown in Figure 45.

![](images/5a1e651381b9c6f5980f8a188016b2c79974fd62287e523417e854e77dce1dcc.jpg)  
Figure 45. STM32CubelDE SCB register access

If you need more informations about the Hardfault,you can first enable faulting or halting when the processor executes an SDIV or UDIV instruction with a divisor of 0:

At runtime, before pressing "resume" button, open "Fault Analyzer" n

Window ->Show View -> Fault Analyzer

If the code performs an SDIV or UDIV instruction with a divisor of 0, code stops with informations in "Fault Analyzer" (see Figure 46).

![](images/fc46c08ff93b3d7d20ee929e10cea52d29784bdd02d54575450fdc44a7391ed4.jpg)  
Figure 46. Fault Analyzer in STM32CubeIDE

Independently from the IDE, for projects including the CMSIS library, the content of the registers in the code can also be printed:

void HardFault_Handler(void)   
{ volatile uint32_t csfr= SCB-> CSFR ; // load into variable printf ( "SCB-> CSFR Ox%O8x \n", SCB-> CSFR) // print while (1) { }   
}

The same content can as well be obtained directly from the memory with any memory browser.

Other faults like UNALIGNED, UNDEFINSTR can be managed in a similar way.

For more details, refer to the relevant programming manual:

• STM32F4 and STM32L4 Series Cortex®-M4 programming manual • (PM0214) • STM32F7 Series Cortex®-M7 processor programming manual (PM0253)

Relevant information is also available on partners websites:

• https://www.iar.com • http://www.keil.com

# 7 Printf debugging

Printf debugging is one of the most straight-forward and used solution in order to start investigating a non-working system.

This chapter is a getting started guide to quickly setup a printf data path through semihosting, USART or SWO, benefiting from facilities offered by STMicroelectronics hardware kits and ecosystem tools.

# 7.1 STM32 Virtual COM port driver

STM32 Virtual COM Port Driver (VCP) is a feature supported by ST-LINK/V2-B embedded in most of recent hardware kits (refer to Section 2.1: Hardware development tools on page 9). It is a RS232 emulation through ST-LINK USB connection.

On the PC side, this requires driver software package (STSW-STM32102) included in ST-LINK driver (STSW-0009).

Once the target is connected, it is seen as a serial port on the PC. An example is presented in Figure 47.

![](images/29f49aaeb6462c3eff3d61a335f41173ddcb3c9b3118bef2d49caeddbe6fbf74.jpg)  
Figure 47. Virtual COM port on Windows® PC

# 7.2 Printf via UART

Direct connection from PC UART to board pinout does not work due to signal level incompatibility.

Take care to use external adapter (such as MAX232, ST3241EB, FTDI USB/UART) or the USART connected to Virtual COM port.

Trick: Appendix B: Use Nucleo "cuttable" ST-LINK as stand-alone VCP on page 106 explains how to use ST-LINK Nucleo stand-alone part as VCP.

The straight-forward way to set a Serial Com port with PC host is to use the USART connected to VCP.

USART connected to VCP depends on the hardware kit:

• Nucleo-32/Nucleo-64: USART2 - PA2/PA3   
• Nucleo-144: USART3 - PA9/PA10   
• Discovery: not standard. Refer to the board schematics EVAL: not standard. Refer to the board schematics. Either the VCP or the RS232 connector can be used

In STM32CubeMX, for Nucleo board, the VCP USART pins (PA2/PA3) are reserved by default, but required to be enabled by selecting "asynchronous" in USART mode selection box as shown in Figure 48.

![](images/0376fe09ef3e6b3fac7e17d36f0496c63696a095709a81cb40c407da56004362.jpg)  
Figure 48. USART Pinout configuration with STM32CubeMX   
Then, set the UART communication settings in Configuration -> USART2 Configuration -> Parameter Settings as shown in Figure 49.

![](images/fcb6539f3487d29bbf0093f08b2b45b8a83ae57fe85852a9be050680b3978c76.jpg)  
Figure 49. USART2 setting with STM32CubeMX

Retargeting printf to UART depends on the toolchain.

For IAR™ EWARM and Keil® MDK-Arm µVISION this is done by overriding the stdio fputc function

#include "stdio.h"

int fputc(int ch, FILE \*f)   
{ HAL_UART_Transmit(&UartHandle, (uint8_t \*)&ch, 1, OxFFFF); return ch;   
}

For GCC based toolset like STM32CubelDE, two cases can be met.

With syscall.c integrated to the project: #include "stdio.h"

int _io_putchar(int ch) {

HAL_UART_Transmit(&UartHandle, (uint8_t \*)&ch, 1, OxFFFF); return ch; } Without syscall.c integrated, a customized _write function has to be defined: int _write(int file, char \*ptr, int len) { int DataIdx; for (DataIdx = 0; DataIdx < len; DataIdx++){ _io_putchar( \*ptr++ );} return len; }

Refer to STM32Cube provided example UART_Printf () available for almost all STM32 Series. An example is available in STM32Cube_FW_F3_V1.7.0|Projectsl STM32F303ZE-Nucleo\Examples\UART\UART_Printf.

# Caution:

USART word length includes parity which is not the case for most of UART terminal. Word length 8 with parity require 7 bits + parity on terminal side to match.

VCP does not support Word length of 7 bits and below (whatever the parity). Table 5 gives examples of compatible configurations:

Table 5. STM32 USART vs. PC terminal WordLength example   

<table><tr><td rowspan=1 colspan=1>STM32 UART</td><td rowspan=1 colspan=1>PC Terminal</td></tr><tr><td rowspan=1 colspan=1>Word Length: 8, Parity: Odd</td><td rowspan=1 colspan=1>Data: 7, Parity: Odd</td></tr><tr><td rowspan=1 colspan=1>Word Length: 8, Parity: None</td><td rowspan=1 colspan=1>Data: 8, Parity: None</td></tr><tr><td rowspan=1 colspan=1>Word Length: 9, Parity: Odd</td><td rowspan=1 colspan=1>Data 8, Parity: Odd</td></tr><tr><td rowspan=1 colspan=1>Word Length: 7, Parity: Odd/None</td><td rowspan=1 colspan=1>Not Working with VCP</td></tr></table>

# 7.3 Printf via SWO/SWV

Serial Wire Output (SwO) is single pin, asynchronous serial communication channel available on Cortex-M3/M4/M7 and supported by the main debugger probes.

It is using the ITM (instrumentation trace macrocell) module of the Cortex Core-Sight.

The asynchronous mode (SwO) requires 1 extra pin and is available on all packages for STM32 based on Cortex-M3, -M4, and -M7.

It is only available if a Serial Wire mode is used. It is not available in JTAG mode.

By default, this pin is NOT assigned. It can be assigned by setting the TRACE_IOEN and TRACE_MODE bits in the Debug MCU configuration register (DBGMCU_CR). This configuration has to be done by the debugger host.

Refer to the related chapter of STMicroelectronics reference manual.

In debug context it can be a good alternative to UART in system where pinout constraints are strong (alternate function preempting UART GPIOs).

It has to be used in combination with a Serial Wire Viewer (SWV) on host side which provides the following features:

• PC (Program Counter) sampling • Event counters that show CPU cycle statistics • Exception and Interrupt execution with timing statistics • Trace data - data reads and writes used for timing analysis • ITM trace information used for simple printf-style debugging

This chapter only addresses the printf-style debugging feature.

In order host debugger can manage flexible pin assignment ensure SwO pin is not used for other purpose.

In STM32CubeMX:

Select "Trace Asynchronous Sw" in SYs -> Debug selection box as shown in Figure 50.

![](images/60353b008c45550c83f1ce2abd96626b0b5356403355de0cc1fb508a25088197.jpg)  
Figure 50. SWO Pin configuration with STM32CubeMX

This secures that the PB3 is not allocated to another use. No specific code is generated.   
Other init steps are performed by the SWV integrated in the IDE or in the ST-LINK utility.

# IARTM EWARM

IAR™M EWARM provides an integrated access to SWO.

Redirection of printf and scanf is possible using Library Configuration options as shown i Figure 51.

![](images/0b12d73b4b9d846cd9876ec8132ba994cfc84c2375fba3dc719ca10603ddaa9b.jpg)  
Figure 51. Semihosting/SWO configuration with IAR™M EWARM

Care must be taken that clock setup is correct by using ST-LINK -> Communication Pane as illustrated in Figure 52.

![](images/f49aaced5b7a057881f9ed4d4c4bcba8402fd161d576e3e8006685065eb96562.jpg)  
Figure 52. IAR™ EWARM SWO Clock setting

Once configured, IAR™M EWARM properly sets TRACE_IOEN and TRACE_MODE and configures the related GPIO.

SWO printf occurrences are visible in Terminal I/O windows.

Port Stimulus 0 is used by printf and scanf. It is not configurable.

# KeilMDK-Arm μVISION:

In MDK-Arm it is required to redirect printf to SWO by some piece of code following same model as for UART (Refer to Section 7.2: Printf via UART on page 69)

#include "stdio.h"   
int fputc(int ch, FILE \*f)   
{ ITM_SendChar(ch); return(ch);   
}   
Keil® must be properly configured for the SWO communication to be properly set. An   
example is given in Figure 53.

# In Projet Option -> Debug -> Probe Settings -> Trace Pane:

1. Tick Trace Enable   
2. Enter correct Core Clock   
3. Enable ITM Stimulus Port 0

![](images/5e1783adbdfbce9efd15712475dbbe28cd979e6851e1c4e76c9035762cc15528.jpg)  
Figure 53. SWO configuration with Keil®

SWV viewer is called "Debug (printf) Viewer" and is accessible while in debug through View -> Serial Windows -> Debug (prinf) Viewer as shown in Figure 54.

![](images/8aa053ad44bdd25a8eb7a480309ccefd2a55db15c9a7d6e870ed4d9b78cab0a9.jpg)  
Figure 54. Access to SWV in Keil®

Tip: Keil® MDK-Arm µVISION allow to select the Stimulus to display. On the other hand it is quite straight forward to make some clone of ITM_SendChar() function using any of the 31 stimulus port. Can be useful in a very verbose system to set a trace

ua error) or there source.

# STM32CubeIDE

With STM32CubelDE you also have to redirect printf to SWO by some piece of code.

With syscall.c integrated to the project:

#include "stdio.h" int __io_putchar(int ch) { ITM_SendChar(ch); return(ch); }   
Without syscall, add:   
int _write(int file, char \*ptr, int len)   
{ int DataIdx; for (DataIdx = 0; DataIdx < len; DataIdx++) { _io_putchar(\*ptr++); } return len; }

Enable SWD in Debug configuration ? Debugger pane (see Figure 55).

Core clock must be the same as Cortex clock. You can then start the debug session.

![](images/a0d6e07413bb67fb0838ff5970bd3968b4ed48bc16b9908697f29e1887a72984.jpg)  
Figure 55. Enable SWD in STM32CubelDE

# Enable SWV ITM Data Console in

Window ->Show View -> SWV -> SWV ITM Data Console as shown in the figure below:

![](images/45fd9459b5f1f66f7b4efb60123a1bb441de248600a5c5959612bc0f592f20b1.jpg)  
Figure 56. Enable SWV ITM Data Console in STM32CubelDE   
Enable ITM Stimulus Port 0 after clicking on "Configure trace" as shown in the below figure.

![](images/79d54cd876b9603a9a606ea9c2089c0161471d69c833f318ff8c4d80a95e0239.jpg)  
Figure 57. Enable ITM stimulus Port 0 in STM32CubelDE

Click on "Start Trace" button

![](images/1d177accff008b4c537ae65d4a17287ac2e0eed5eb249ba8e0042a8757600129.jpg)  
Figure 58. Start Trace button in STM32CubelDE

Press "Resume" button, and your printf message is printed in SWV ITM Data Console.

# 7.4 Semihosting

Semihosting is a mechanism that enables code running on an Arm® target to communicate and use the Input/Output facilities on a host computer that is running a debugger.

Examples of these facilities include keyboard input, screen output, and disk l/O. For example, this mechanism can be used to enable functions in the C library, such as printf () and scanf () . It can also allow to use the screen and keyboard of the host instead of having a screen and keyboard on the target system.

This is useful because development hardware often does not have allthe input and output facilities of the final system. Semihosting enables the host computer to provide these facilities.

However, the user has to be aware of the following drawbacks:

Semihosting only works during a debug session. Otherwise, the program gets stuck in the first printf () routine reached.   
Since semihosting uses breakpoint instruction and host dependent code, it has significant and unpredictable impact on performance.

Semihosting depends on the library provided by the IDE. The next sections present how to set semihosting using the three main IDEs covered in this application note.

# 7.4.1 IAR™ EWARM

IAR ™m EWARM provides a highly integrated semihosting feature, enabled by default.

Figure 59 shows how to check if t is the case for the project in Options -> General options -> Library Configuration Pane.

![](images/20342446ef851a21867da49ed39e7f0e77b9e1f1163b94e0c699ae96f4fb588f.jpg)  
Figure 59. Semihosting configuration in IAR™ EWARM

In such a case, simply use printf () / scanf () functions in the code.   
Input and output of the program are displayed in the Terminal l/O window.

# 7.4.2 Kei® MDK-Arm μVISION

Keil® has no semihosting capability.

# 7.4.3 STM32CubeIDE

# Set linker parameters

First the linker must ignore the default syscalls.c file and has to use the newlib-nano librairies, which contains printf() function.

# in Project -> Properties -> C/C++ General -> Paths and Symbol

Click on the Source Location tab. Click on the arrow near to "[Project name]/Core", and select "Filter(empty)".

Then click on "Edit filter" button and add "syscall.c" to the Exclusion patterns list.

![](images/fcc8ba46250ae4c92f6c2da2e52dd063a6b444909ac18d93272f6f675a74fdf2.jpg)  
Figure 60. Properties for semihosting in STM32CubelDE- Source Location

To use semihosting the librdimon must be enabled. Librdimon implements the semihosting versions of syscalls from newlib.

On the left-side pane, go into C/C++ Build -> Settings and select the Tool Settings tab.

Then, select MCU GCC Linker -> Libraries. In the libraries pane, click the "Add" button and enter rdimon.

![](images/bf63d672ba1fee2b28f2a6b551e5f6b40bd12dc564410c26ce2e479374166bc8.jpg)  
Figure 61. Properties for semihosting in STM32CubelDE- Librairies

Next, select McU GCC Linker -> Miscellaneous while stillin the Tool Settings tab.

Click the Add... button and enter -specs=rdimon.specs into the dialog box.

This add the linker fags inorder to include the librdimon lrary

![](images/5a405c48720969e7c766c4f49fc3155cfe05e3e34cec7c40eddad7ec1580023a.jpg)  
Figure 62. Properties for semihosting in STM32CubelDE

# Add printf Code

Above int main(void) (USER CODE 0 section), add:

extern void initialize_monitor_handles(void);

Theconfigure the semihosting system cll In int main(void) before the while(1) lo (USER CODE 1 section) add:

Initialise_monitor_handles();   
Then inside the while(1) loop, add: Printf("Hello World!\n");   
HAL_Delay(1000);   
Click Project -> Build Project to compile and link everything.

# Debug configuration

In Run -> Debug configuration -> Debugger tab, change the debugger probe to ST-LINK (Open OCD).

In Generator options, choose "Software system reset"as reset Mode.

![](images/72b1179b8810da23e96907ac8b7e2d17b2ba8e92905f926f3433de4f3f79b098.jpg)  
Figure 63. Semihosting in STM32CubelDE  Debug configuration

In the Startup tab enter the command: monitor arm semihosting enable.

![](images/63a19e229a7f34216240d4789e2dd5e6f94654caf6b63af95e777c54f374d7dc.jpg)  
Figure 64. Semihosting in STM32CubelDE  Startup

Click on Debug button.

# Run

In the debugging perspective, click Run -> Resume, and you should see "Hello, World!" being printed at the bottom of the console once per second.

![](images/9ec6f7010f890f76ab463286bd9456144ad04152c9c504793ad7814a4a66ba25.jpg)  
Figure 65. Semihosting in STM32CubeIDE - Run

# Debug through hardware exploration

As a complement to software instrumentation, a user facing a non-working system may take great advantage to monitor STM32 pin states (GPIO or clock among others) with external tools such as oscilloscopes or logic analyzers.

This chapter presents the possibilities offered by STMicroelectronics hardware kits and integrates a complete tutorial to setup the microcontroller clock output (MCO)

# Easy pinout probing with STMicroelectronics hardware kits

All STMicroelectronics hardware kits presented in Section 2.1.1 on page 9 offers easy pinout access thanks to their Morpho or ARDUINO® connectors.

The coverage of the pinout by the connectors depends on the board itself as well as on the MCU type. In most cases, a large number of GPiOs are covered.

In order to use this coverage at best, the user is advised to study the board schematics that show the connections between the MCU pins and the connectors. In association with the schematics, the board user manual presents the jumper and solder bridge configurations that modify the routing of pins to connectors.

# 8.2 Microcontroller clock output (MCO)

This feature allows to output one or more internal clock to one or more pins in order to enable measurement through an external tool, typically an oscilloscope.

It can be useful in debug context in order to check that clock settings is as per expectation and help to investigate potential error in clock tree initialization code.

# 8.2.1 Configuration with STM32CubeMX

In STM32CubeMX, MCO stands for master clock output. It is enabled by ticking the Master Clock Output option in the RCC section as shown in Figure 66.

OPAMP2 PA12 RCC PA11 High Speed Clock (HSE)Disable PA10 LOow Speed Clock (LSE) Disable PA9 √ Master Clock Output PA8 RCC_MCO Audio Clock Input (I2S_CKIN) PC9 + RTC PC8 + x SPI2 PC7

This allocates a pin labeled RCC_MCO.

This is typically pin PA8 for all STM32 families.

For Nucleo kits, the PA8 pin is accessible on the D7 pin of the ARDUINO® connector.

For other board pin configuration, please refer to the board schematics.

Depending on board or and chip families, other pins can be used if needed and available.

The Ctrl + click on RCC_MCO pin command sequence under STM32CubeMX highlights in blue the alternate pin. An example is shown in Figure 67.

![](images/2e290a38abd3a6637d5cfbf02bb2e32dd783c094e962311b1c65a5be8be8461f.jpg)  
STM32CubeMX Clock Configuration pane selects the signal to route to pin and the divider as presented in Figure 68.

![](images/c66ee5e79532447b7b131e7ea6b26dd571028f97c360424ae017be808d50f6c5.jpg)  
Figure 68. MCO Multiplexer in STM32CubeMX Clock Configuration Pane

The divider allows to output a signal frequency compatible with output capabilities.

# 8.2.2 HAL_RCC_MCOConfig

Independantly of the fact that STM32CubeMX is used or not, MCO configuration is done using the hal_rcc or LL function:

stm32XXxx_hal_rcc.c/ stm32XXxx_hal_rcc.h

void HAL_RCC_MCOConfig( uint32_t RCC_MCOx, uint32_t RCC_MCOSource, uint32_t RCC_MCODiv)

Examples based on LL drivers are available in STM32Cube libraries (refer to STM32CubeProjectList.html) which configure the GPIO and the related registers depending on source and divider.

They also configure the selected GPIO accordingly:

/\* Configure the MCol pin in alternate function mode \*/ GPIO_InitStruct.Pin = MCO1_PIN; GPIO_InitStruct.Mode = GPIO_MODE_AF_PP; GPIO_InitStruct.Speed = GPIO_SPEED_HIGH; GPIO_InitStruct.Pull = GPIO_NOPULL; GPIO_InitStruct.Alternate = GPIO_AFO_MCO; HAL_GPIO_Init(MCO1_GPIO_PORT, &GPIO_InitStruct);

C t      .

OSPEED setting and maximum output frequency value are described in the datasheet of the related MCU in chapter I/O port characteristics.

Max Frequency values are given for a typical load of 50 pF or 10 pF.

If the measure is performed with an oscilloscope, the load of the probe circuitry must be taken into account.

If the frequency of the signal under observation exceeds the GPIO capability (e.g. 216 MHz Sysclock on F7 while GPIO maximum frequency is 100 MHz), use a divider to produce a suitable signal.

The default value RCCHALunction s the highest (which  od).

In case of a STM32CubeMX generated project, be aware that default value applied in generated MX_GPIO_init () function (executed after MCO config) is the lowest.

In case the output clock is higher than 1 MHz, it is recommended to change this.

A too low OSPEED setting can be suspected in case no signal or very noisy/flatten signal (small amplitude).

A too high setting can be suspected if a signal with a long and high amplitude dumping oscillation is observed (overshoot / undershoot).

# 8.2.3 STM32 Series differences

STM32L4 Series also provides an LSCO (Low Speed Clock Output) on PA2 in order to output LSE or LSI, same as MCO, but with benefit to be still available during stop and standby mode.

Refer to section 6.2.15 Clock-out capability of STMicroelectronics reference manual STM32L4x5 and STM32L4x6 advanced Arm®-based 32-bit MCUs (RM035) for details.

HAL Function to call is:

void HAL_RCCEx_EnableLSCO(uint32_t LSCOSource'

in stm3214xx_hal_rcc_ex.c/.h

# Note:

LSCO is conflicting with UART2 TX (PA2). On Nucleo-64 board, the use of the LSCO board use and the use of the ST-LINK VCP are mutually exclusive.

SB63 must be set in order to get the LSCO signal available on Morpho and ARDUINO® connectors.

Refer to the board user manual for details.

STM32F4 and STM32F7 Series devices provide two different MCO outputs given choice of four clocks each as shown in Figure 69. Refer also to Appendix D: Cortex®-M debug capabilities reminder on page 116.

![](images/c1a5f754984d826b7779e5eae669b9a31213dbb1ca98eac96d7ab92604db5bbb.jpg)  
Figure 69. STM32F4/F7 dual MCO capabilities

# Dual-Core microcontroller debugging

STM32H7x5/x7 Series are dual core microcontrollers using heterogeneous core architecture: An Arm Cortex-M7 core and an Arm Cortex-M4 core.

Debug process is different for these dual core microcontrollers as we need a simultaneous debug of both cores using a single hardware debug probe.

# Note:

Refer to AN5286 and AN5361, both available on st.com which explain how to proceed to debug dual core with IAR™ EWARM (AN5286), MDK-Arm (AN5286) and STM32CubeIDE (AN5361).

Dual debug is supported using   
- STM32CubeIDE, IAR ™M EWARM starting from version 8.30, or MDK-Arm version v5.25 and later   
— ST-Link server starting from version v1.1.1-3

# 10 From debug to release

It is important to have in mind that most of technics presented in this AN and suitable for debugging have to be properly cleaned to prevent problem while releasing the application.

The following action list can be used as a checklist helping to avoid the most common problems:

Remove software BKPT instructions or take care to let them inside #ifdef DEBUG statements. Ensure printf ( ) uses available data path on final product. Semihosting and SwO cause hardfault otherwise. Reestablish Code Optimization level. • Implement proper Fault Handlers. Reset DBGMCU registers to default.

# 11 Troubleshooting

Table 6 summarizes solutions to overcome some of the most frequent issues faced during debug setting and operation.

Table 6. Troubleshooting   

<table><tr><td rowspan=1 colspan=1>Problem</td><td rowspan=1 colspan=1>Solution</td></tr><tr><td rowspan=1 colspan=1>Connection with target lost during debug of low-powersystem</td><td rowspan=1 colspan=1>Ensure debug in low-power in DBGMCU register isenabled.Ensure SWD pin not set in analog state.Refer to Section 4.1: SWD/JTAG pinout and toSection 4.3: Low-power case.</td></tr><tr><td rowspan=1 colspan=1>Fail to get printf via SWO</td><td rowspan=1 colspan=1>Refer to Section 7.3: Printf via SWO/SWV.</td></tr><tr><td rowspan=1 colspan=1>An unexpected power consumption is measured for alow-power application.</td><td rowspan=1 colspan=1>Check that low-power debug in DBGMCU register isOFF. Beware that this register is reset only with a POR(power-on reset).Refer to Section 4.3.</td></tr><tr><td rowspan=1 colspan=1>Fail to connect to a board with Normal/System Reset</td><td rowspan=1 colspan=1>Try ConnectUnderReset / Hardware Reset connectionmode. This resets SWD connection in case it has beendisabled by application.Refer to Section 4.2.</td></tr><tr><td rowspan=1 colspan=1>Fail to connect on board usingConnectUnderReset/Hardware using ST-LINK</td><td rowspan=1 colspan=1>Ensure NRST of ST-LINK is properly connected to MCUNRST (e.g. check SB12 for Nucleo).</td></tr><tr><td rowspan=1 colspan=1>Fail to see clock signal on MCO output</td><td rowspan=1 colspan=1>Ensure that the clock configured to MCO is in thesupported range of the GPIO and that the OSPEEDsetting is correct.Refer to Section 8.2.</td></tr><tr><td rowspan=1 colspan=1>Impossible to evaluate a value or a variable, orimpossible to set a breakpoint at a specific line in code</td><td rowspan=1 colspan=1>Compiler optimization is probably enabled. Remove it.Refer to Chapter 3: Compiling for debug.</td></tr></table>

# Appendix A Managing DBGMCU registers

This appendix provides a tutorial for the different ways to Read/Write the DBGMCU registers with various tools and IDEs.

# A.1

# By software

HAL and LL provide functions to set/reset DBGMCU registers.

Refer to STM32Cube\Repository|STM32Cube_FW_[MCU] _[Version]Drivers|STM32[MCU]xx_HAL_Driverl STM32[MCU]xx_User_Manual.chm

Figure 70 and Figure 71 show the positions of the DBGMCU registers iwithin the LL and HAL libraries.

+ 12S SYSTEM + SYSTEM Private Constants Definitio + SYSTEM Exported Constants m SYSTEM Exported Functions + SYSCFG STA DBGMCU m Functions LL_DBGMCU_ABP1_GRP1_FreezePeriph Get Inte LL_DBGMCU_ABP1_GRP1_UnFreezePeriph Refer LL_DBGMCU_ABP2_GRP1_FreezePeriph ( LL_DBGMCU_ABP2_GRP1_UnFreezePeriph LL_DBGMCU_DisableDBGSleepMode Returi LL_DBGMCU_DisableDBGStandbyMode LL_DBGMCU_DisableDBGStopMode LL_DBGMCU_EnableDBGSleepMode Definitio LL_DBGMCU_EnableDBGStandbyMode LL_DBGMCU_EnableDBGStopMode LL_DBGMCU_GetDevicelD STA LL_DBGMCU_GetRevisionID + FLASH Get Wak TI

m Modules Returi m STM32LOxx_HAL_Driver m HAL HAL Private Definitio + HAL Exported Constants m HAL Exported Macros Defines STA m HAL Exported Functions + Initialization and de-initialization functions Get Star m Peripheral Coounction Refere HAL_DBGMCU_DBG_DisableLowPowerConfig C HAL_DBGMCU_DBG_EnableLowPowerConfig Returi HAL_DBGMCU_DisableDBGSleepMode HAL_DBGMCU_DisableDBGStandbyMode HAL_DBGMCU_DisableDBGStopMode Definitio HAL_DBGMCU_EnableDBGSleepMode HAL_DBGMCU_EnableDBGStandbyMode HAL_DBGMCU_EnableDBGStopMode STAT HAL_Delay HAL_GetDEVID Indicate HAL_GetHalVersion

For MO Cortex based families (L0/F0) DBGMCU module need to be clocked by setting bit 22 of register RCC_APB2ENR (refer to the corresponding reference manual) prior to be written.

RCC->APB2ENR |= RCC_APB2ENR_DBGMCUEN;

Some HAL macros are also available to Enable/Disable this clock.

_HAL_RCC_DBGMCU_CLK_ENABLE();   
HAL_DBGMCU_EnableDBGStopMode();   
HAL_DBGMCU_EnableDBGStandbyMode();   
HAL_DBGMCU_EnableDBGSleepMode(); _HAL_RCC_DBGMCU_CLK_DISABLE();

# A.2 By debugger

In order to avoid debugging specific lines in the source code, there are several possibilities to set DBGMCU registers through debugger interfaces or scripts.

# IAR T™M EWARM

Read/Write of DBGMCU registers is possible through the register window as shown in Figure 72:

Register x DBG MCU   
IDCODE = Ox20036410   
CR = Ox00000100 DBG_SLEEP = DBG_STOP =0 DBG_STANDBY =0 TRACE_IOEN =0 TRACE_HODE =0x0 DBG_IUDG_STOP = 1 DBG_VVDG_STOP =0 DBG_TIH1_STOP =0 DBG_TIM2_STOP =0 DBG_TIH3_STOP =0 DBG_TIM4_STOP =0 DBG_CAN1_STOP =0 DBG_I2C1_SMBUS_TIMEOUT = 0 DBG_I2C2_SHBUS_TIHEOUT = 0 DBG_TIH8_STOP =0 DBG_TIH5_STOP =0 DBG_TIH6_STOP =0 DBG_TIM7_STOP =0 DBG_CAN2_STOP =0

In case a more permanent setup is required EWARM C-SPY® debugger macros enable to define execUserSetup ( ) , which is executed at debugger start prior to program execution.

Figure 73 shows the Project Option Debugger -> Setup Pane.

![](images/dc29a3a83e3faaf3e68c6f42d62fcb32bfe697db27fd4bdc940580ea9b0b40e3.jpg)  
Figure 73. EWARM C-SPY® Mac script setting

A basic sample code of execUserSetup () function used to enable low-power debug on LO is provided below:

execUserSetup() {/\* Write a message to the debug log \*/ _message "L0 DBGMCU Setup IAR Macro \n";

_writeMemory32 (0x00400000, Ox40021034, "Memory"); // Enable clock DBG writeMemory32 (0x00000007, Ox40015804, "Memory"); // Enable low-power Debug in DBG_CR writeMemory32 (Ox00000001, Ox40015808, "Memory"); // DBG_APBl_FZ Timer2 Stop Enable

# }

For further information about feature offer by C-SPY® macros please refer to C-SPY® Debugging Guide available in IAR Help Menu and on www.iar.com.

IAR™ EWARM enables Low-Power debug by default if connected with I-jet™ or cmis-dap compliant probes.

# KeilMDK-Arm μVision

At runtime, access to the DBGMCU register is possible through View -> System Viewer -> DBG.

![](images/fe9e34952211363326ada4fd6f1bc90a80404cae6406bae41766e69217548eb3.jpg)  
Figure 74. Accessing DBGMCU register in Keil©® MDK-Arm μVision (1/2)

![](images/c3628a1cf87402a42f09ddb43ca63c8381d70eabc7af215c40f46dffd6d5534e.jpg)  
Figure 75. Accessing DBGMCU register in Keil® MDK-Arm μVision (2/2))

Each bit inthe register can be set or reset independently.

For a permanent debug configuration, use Keil® MDK-Arm µVision initialization file capability.

Debugger script files are plain text files that contain debugger commands. These files are not created by the tools. The user must create them to suit his specific needs. Typically, they are used to configure the debugger or to setup or initialize something prior to running the program.

Figure 76 shows initialization script setting in Project option ->Debug Pane.

![](images/a188d7701a202683fb6d4d46fe29346230c44085c34c4ccbd5f1e3e1e9e6a0e8.jpg)  
Figure 7Ke® ntialization script et

# Sample code for Init file setting DBGMCU registers on MO based MCU (Clock enabling)

FUNC void DBGMCUSetup (void) { // DBGMCU configuration _WDWORD(0x40021034, 0x00400000); // Enable clock DBG _WDWORD(0x40015804, Ox00000007); // DBG_CR _WDWORD(0x40015808, Ox00000001); // DBG_APB1_FZ

}DBGMCUSetup();

For further information regarding Keil® MDK-Arm μVision initialization script, refer to http://www.keil.com.

# STM32CubeIDE

By default, STM32CubelDEenable Low-Power debug. This default setting can be changed through Run->Debug Configurations->Debugger Pane.

Setting up with OpenOCD server

By clicking on the Show generator options as presented in the figure below.

![](images/9eeddee099ca08df66bf77905c8239a458d6b1f8246df4817117ff74779ef87b.jpg)  
Figure 77. Access to Generator Options in STM32CubelDE V2.0.0   
DBGMCU options are available under Reset Mode in the Mode Setup group as shown in Figure 78.

![](images/3f3f70b3d86282c2700d5f6f0905b4f0db3a7001b6065d407892b6aee4369dd4.jpg)  
Figure 78. Generator Options debug MCU in STM32CubelDE

![](images/c920a79e9e87a8518fa8d8b5ed89b0955d859d372520d0d7d46722138a5b82df.jpg)  
Figure 79. Access to DBGMCU settings with STM32CubelDE V1.3.0

If needed, the DBGMCU value can be changed at run time through the l/O Registers window as shown in Figure 80.

![](images/be2ba9698afc2fc08bcc31445b2e3fe87bb41284423f0f03a4a4cf32534964bd.jpg)  
Figure 80. Runtime R/W access to DBGMCU register with SSTM32CubeIDE   
All DBGMCU registers values are kept while reset. Pay attention to not let a debug or unwanted state when returning to normal execution. (refer to Chapter 9: Dual-Core microcontroller debugging on page 92).

Note:

# Appendix B Use Nucleo "cuttable" ST-LINK as standalone VCP

As stated in Section 7.2: Printf via UART on page 69, it is required to have an adapter between MCU and PC to setup a proper serial connection.

Design constraints may prevent to use the default UART connected to VCP, or may require another serial connection with the PC.

In such a case, it is simpler and cheaper to use another Nucleo board instead of getting the appropriate RS232 level shifter.

The "Cuttable PCB" capabilities of the Nucleo-64 and Nucleo-144 boards represent their capacity to disconnect on-board ST-LINK from STM32 application part.

The simple way to disconnect the ST-LINK part from the MCU application part is to power off the MCU by removing jumper J5. This is indicated by the fact that LED LD3 is off when a USB cable is connected. This configuration is presented in As show in Figure 81.

![](images/a013e328c83a97f8efce6ecc7770b0296cd0bf43bb361a86863e2042dcbba413.jpg)  
Figure 81. ST-LINK cuttable part of Nucleo

In this case the ST-LINK part can be used as a stand-alone module.

1As debugger interface to program and debug an external application as documented in the user manual

STM32 Nucleo-144 board: section 6.3.4 of Using ST-LINK/V2-1 to program and debug an external STM32 application (UM1974)   
STM32 Nucleo-64 board: Using ST-LINK/V2-1 to program and debug an external STM32 application (UM1724)

As an alternative and/or additional Virtual COM port

Any available UART of the STM32 application can be connected to the CN3 connector of the ST-LINK part.

Figure 82 illustrates a project using NUCLEO-F302R8 is using ST-LINK part of a NUCLEO-L476RG for connection of UART1 to the host.

UART1 RX PC5 is routed via Morpho Connector CN10 Pin 6 to CN3 TX of NUCLEO-L476RG ST-LINK.

UART1 TX PC4 is routed via Morpho Connector CN10 Pin 34 to CN3 RX of NUCLEO-L476RG ST-LINK.

![](images/1d1a97d7da1e2fb806c09733b513ca38c7801e05a7778983516ccc005bf53eec.jpg)  
Figure 82. Using ST-LINK stand-alone part of Nucleo-L476RG as VCP

With this setup, on the PC side, two Virtual COM ports are available with potentially two different serial channels:

1Nucleo-F302R8 UART2 (native default VCP) to COM4   
2.Nucleo-F302R8 UART1 (VCP through Nucleo-L476RG) to COM8

![](images/6e7a885464a6496fdb1edfecea8c4767d2292551ac0c2ef82910677c16cb3f57.jpg)  
Figure 83. Virtual COM port on PC side

# Note:

This usage implies to have several targets connected to a single host PC.

In order to properly identify the target and the VCP, refer to Appendix C: Managing various targets on the same PC.

# Appendix C Managing various targets on the same PC

This appendix provides hints to identify and control the connection to a specific target among several ones using ST-LINK probe.

Each ST-LINK connection is identified by a serial number.

In order to correlate a serial number with a board, it is advised to use STM32CubeProgrammer.

At the top of the screen, the serial number pick list contains all connected ST-LINK probes. By selecting one, access to the target is generated, making blinking of the related ST-LINK LED switch from red to green.

![](images/b5db75ec883be3c4b28d2124b3e4d32f19b33d44be2c541c99682ae42a1c4c67.jpg)  
Figure 84. STM32CubeProgrammer target selection pick list

Once the target is identified, it is possible to copy the S/N from the console in the clip-board as shown in Figure 85.

![](images/019b176c856be3df6cb45c4328c0d6d7f62b6154e10e88f20456153fcb8e35e2.jpg)  
Figure 85. Getting target ST-LINK S/N from the console

The next sections detail the selection of a specific target with each of the main IDEs considered in this application note.

# IARTM EWARM

The first time a debug session is launched while several targets are connected, a Debug Probe Selection window pops up.

A list of connected targets is displayed, identified by the last four bytes of the ST-LINK S/N as illustrated in Figure 86.

![](images/4d1be1fe94bc17f465b04dd6706af11cef3477e71ef81425add3e296e4dd9332.jpg)  
Figure 86. IAR™ EWARM Debug Probe Selection pop-up window

It is recommended to use the Edit Nickname feature to ease board identification in anticipation of further connection as shown in Figure 87.

![](images/19b808aef48e672d1e3ac3ed4e3c2078f831d5dd587177f78845ff4d5f621d65.jpg)  
Figure 87. IAR ™ EWARM Debug Probe Selection with nickname

Important: The pop-up window is displayed only at first time. The selection made is then applied by default to further connections. Changing this initial selection requires that the "Debug Probe Selection" display is forced by setting the "Always prompt for probe selection" option in Option -> ST-LINK -> Setup as shown in Figure 88.

![](images/74d0ecc4a534853d17df214ad6bc70e796027a201197bfc07c50f0ebdab2738d.jpg)  
Figure 88. Probe selection prompt setting on IAR ™ EWARM

# Keil MDK-Arm μVision

The list of connected targets is visible in ST-LINK debug pane (Options -> Debug -> ST-LINK -> Settings -> Debug Pane) as presented in Figure 89.

![](images/2aabdcc3d329484a9d16d55afda0e43903f5bdea5173f053047ab0d492631b6a.jpg)  
Figure 89. Keil® ST-LINK selection

In the Debug Adapter section, the pick list allows to select among all connected targets.

At selection it can be observed a brief activity of the ST-LINK LED of the related board and the Serial Number is displayed.

The selection is stored for the next connections.

# STM32CubeIDE

If you try to launch a debug session with two ST-LINK connected, a pop-up message appear as shown in the figure below:

![](images/29f5064d967fd9bdeefc56b48059de80353e5a8584cb87ac47f3a69f47bfd605.jpg)  
Figure 90. Error message for multiple ST-LINK detected in STM32CubelDE

Setting up with OpenOCD

rIt is possible to force the connection to a specific target using the ST-LINK S/N.

In Run -> Debug Configurations -> Debugger Pane, add the following OpenOCD option: -c hla_serial [ST-LINK S/N]

Figure belowillustrates the setting an OpenOoton or orcing  c.

![](images/8f7c50dc95c66ac82463949eb6709909605f82c197be457983f208c46ef6f8f2.jpg)  
Figure 91. Forcing specific ST-LINK S/N with STM32CubelDE with OpenOCD option   
Setting up with ST-LINK GDB server

![](images/bc9f96770b500e550ebc5919dd3d387f955b4746404fada1e6205f6e30eeaa2e.jpg)  
Figure 92. Forcing specific ST-LINK S/N with STM32CubelDE with ST-LINK GDB server

# Appendix D Cortex®M debug capabilities reminder

STM32 families debug capabilities depend on their Cortex®-M type.

Table 7. STM32 Series vs. debug capabilties   

<table><tr><td rowspan=1 colspan=1>STM32Series</td><td rowspan=1 colspan=1>Cortex type</td><td rowspan=1 colspan=1>SWD</td><td rowspan=1 colspan=1>JTAG</td><td rowspan=1 colspan=1>ETM</td><td rowspan=1 colspan=1>SWO</td><td rowspan=1 colspan=1>Hardwarebreakpoints</td><td rowspan=1 colspan=1>CoreReset</td><td rowspan=1 colspan=1>MCO(1)</td></tr><tr><td rowspan=1 colspan=1>LO/FO</td><td rowspan=1 colspan=1>M0/0+</td><td rowspan=1 colspan=1>Yes</td><td rowspan=1 colspan=1>No</td><td rowspan=1 colspan=1>No</td><td rowspan=1 colspan=1>No</td><td rowspan=1 colspan=1>4</td><td rowspan=1 colspan=1>No</td><td rowspan=1 colspan=1>1</td></tr><tr><td rowspan=1 colspan=1>F1/L1/F2</td><td rowspan=1 colspan=1>M3</td><td rowspan=1 colspan=1>Yes</td><td rowspan=1 colspan=1>Yes</td><td rowspan=1 colspan=1>Yes(2)</td><td rowspan=1 colspan=1>Yes</td><td rowspan=1 colspan=1>6</td><td rowspan=1 colspan=1>Yes</td><td rowspan=1 colspan=1>1</td></tr><tr><td rowspan=1 colspan=1>F3/F4/L4</td><td rowspan=1 colspan=1>M4</td><td rowspan=1 colspan=1>Yes</td><td rowspan=1 colspan=1>Yes</td><td rowspan=1 colspan=1>Yes(2)</td><td rowspan=1 colspan=1>Yes</td><td rowspan=1 colspan=1>6</td><td rowspan=1 colspan=1>Yes</td><td rowspan=1 colspan=1>2({</td></tr><tr><td rowspan=1 colspan=1>F7/H7</td><td rowspan=1 colspan=1>M7</td><td rowspan=1 colspan=1>Yes</td><td rowspan=1 colspan=1>Yes</td><td rowspan=1 colspan=1>Yes(2)</td><td rowspan=1 colspan=1>Yes</td><td rowspan=1 colspan=1>8</td><td rowspan=1 colspan=1>Yes</td><td rowspan=1 colspan=1>2(2)</td></tr></table>

Microcontroller Clock Output (refer to Section 8.2: Microcontroller clock output (MCO) on page 87) Depends on package size. Check availability in the Pin Allocation Table in the related datasheet.

Fo etiela or® ®

# D.1 Application notes index

Table 8. STM32 Series vs. debug capabilities   
Note: Microcontroller Clock Output (refer to Section 8.2: Microcontroller clock output (MCO).   

<table><tr><td rowspan=1 colspan=1>AN references</td><td rowspan=1 colspan=1>Subject</td></tr><tr><td rowspan=1 colspan=1>AN5361</td><td rowspan=1 colspan=1>Dual core microcontrollers debugging</td></tr><tr><td rowspan=1 colspan=1>AN5286</td><td rowspan=1 colspan=1>Dual core microcontrollers debugging</td></tr><tr><td rowspan=1 colspan=1>AN5421</td><td rowspan=1 colspan=1>Trustzone</td></tr><tr><td rowspan=1 colspan=1>AN5347</td><td rowspan=1 colspan=1>Trustzone</td></tr></table>

# Revision history

Table 9. Document revision history   

<table><tr><td rowspan=1 colspan=1>Date</td><td rowspan=1 colspan=1>Revision</td><td rowspan=1 colspan=1>Changes</td></tr><tr><td rowspan=1 colspan=1>16-Jun-2017</td><td rowspan=1 colspan=1>1</td><td rowspan=1 colspan=1>Initial release.</td></tr><tr><td rowspan=1 colspan=1>29-Jun-2017</td><td rowspan=1 colspan=1>2</td><td rowspan=1 colspan=1>Added Table 1: Applicable products.</td></tr><tr><td rowspan=1 colspan=1>26-Jan-2021</td><td rowspan=1 colspan=1>3</td><td rowspan=1 colspan=1>Updated:Section 1.2: Software versionsSection 2.1.1: Hardware kitsFigure 5: Discovery board exampleAdded:Section 1.1: General informationSection 2.4.2: Wiki platformSection 2.4.3: GithubFigure 2: Development tools overviewFigure 4: STM32 Nucleo-144 structureFigure 15: STM32Cube monitorFigure 14: STM32Cube programmer</td></tr></table>

# IMPORTANT NOTICE  PLEASE READ CAREFULLY

acknowledgement.

the design of Purchasers' products.

No license, express or implied, to any intellectual property right is granted by ST herein.

I