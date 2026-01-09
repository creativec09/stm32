# STM32H7x3 smart power management Expansion Package for STM32Cube

# Introduction

STM32H7x3 microcontrollers deliver the maximum theoretical performance of the Arm® Cortex®-M7 core, regardless of whether code is executed from the embedded Flash oya moy0 Mar®   H

STM32H7x3 devices embed a flexible power architecture. The system is split into three domains operating independently to optimize power efficiency.

This document is split into two parts:

The first part describes the system supply configuration; how the CPU sub-system is   
configured by allocating peripherals to the CPU. It also describes the various operating   
modes, and how the different system partitions and clock activities are controlled in these   
modes.   
The second part provides an example of temperature acquisition based on I2C   
transmission, using the X-NUCLEO-IKS01A2 expansion board (based on the   
STM32H7743ZI MCU). The purpose of this example is to highlight the smart power   
management of STM32Hx3 devices: using three power domains minimizing power consumption while keeping some activities running when needed (D3 Autonomous mode).

This application note is provided with the X-CUBE-PWRMGT-H7 Expansion Package that contains one project with four different workspaces:

STM32H743ZI_Mode1: temperature acquisition with CPU in CSleep mode, D1 / D2 in DRun mode and D3 in Run mode • STM32H743ZI_Mode2: temperature acquisition with CPU in CStop mode, D1 in DRun mode, D2 in DStandby mode and D3 in Run mode STM32H743ZI_Mode3: temperature acquisition with CPU in CStop mode, D1 and D2 in DStandby mode, and D3 in Run mode STM32H743ZI_Mode4: temperature acquisition with CPU in CStop mode, D1 and D2 in DStandby mode, and D3 switching between Run and Stop modes.

For further information on STM32H7x3 line devices, refer to the following documents available on www.st.com:

STM32H7x3 advanced Arm®-based 32-bit MCUs reference manual (RM0433) • STM32H743xx datasheet (DS12110) and STM32H753xx datasheet (DS12117)

# Contents

System architecture .. 6

# System supply configuration . . 8

2.1 Voltage regulator (LDO) supply 8   
2.2 Voltage regulator bypass 10

# CPU sub-system configuration . 12

3.1 Peripheral allocation . . 12   
3.2 D3 Autonomous mode 13

# Power control modes .. 15

4.1 Operating modes 15   
4.2 Low-power modes 18

# Operating modes comparison between STM32F7 Series and STM32H7x3 line devices . . 19

Peripheral clock distribution . 20

Wakeup from Stop/CStop mode . . . . . . . . 22

# Low-power application . . .. .. . 25

8.1 Low-power application example 25

8.1.1 Mode 1 . .26   
8.1.2 Mode 2 . .27   
8.1.3 Mode 3 . 27   
8.1.4 Mode 4 . .27

# 8.2 Mode 4 - D3 Autonomous mode 28

8.2.1 Memory retention . . .28   
8.2.2 Example description 28   
8.2.3 Overall description of Mode 4 example .32

How to use the application . . 33

8.3.1 Hardware requirements . 33   
8.3.2 Software requirements . .35

8.3.3 Running the example . . 36

3.4 Power consumption measurements 40

Revision history 42

# List of tables

Table 1. Voltage regulator operating mode and voltage scaling. 9   
Table 2. Configure the voltage scaling using STM32Cube_FW_H7. . .9   
Table 3. Configure the system power supply using STM32Cube_FW_H7. 11   
Table 4. Configure the D3 domain state regardless CPU subsystem modes   
using STM32Cube_FW_H7 14   
Table 5. STM32H7x3 line operating modes. 15   
Table 6. System states for D1 / D2 domains states 16   
Table 7. D2 domain states overview. 16   
Table 8. Functions description used for low-power modes in STM32Cube_FW_H7. 18   
Table 9. Shared operating modes - STM32F7 Series and STM32H7x3 line devices. 19   
Table 10. Shared functions - STM32F7 Series and STM32H7x3 line devices. 19   
Table 11. EXTI pending request clear inputs 24   
Table 12. Specifying the clear source of D3 pending event in STM32Cube_FW_H7 24   
Table 13. Mode 1 - operating modes for each domain . 26   
Table 14. Mode 2 - operating modes for each domain. 27   
Table 15. Mode 3 - operating modes for each domain. 27   
Table 16. Mode 4 - operating modes for each domain. 27   
Table 17. Workspaces available in the example 35   
Table 18. MCU power consumption in different modes 40   
Table 19. Document revision history 42

# List of figures

Figure 1. System architecture for STM32H7x3 line devices 7   
Figure 2. VcoRE voltage scaling versus system power modes 10   
Figure 3. System supply configuration. 11   
Figure 4. Example of peripheral allocation. 13   
Figure 5. Power control modes detailed state diagram 17   
Figure 6. Peripheral clock distribution 20   
Figure 7. EXTI block diagram on STM32H7x3 line devices. 23   
Figure 8. D3 pending request clear logic . 24   
Figure 9. Peripherals and memories connections 26   
Figure 10. Timing diagram of SRAM4 to I2C4 transfer with BDMA. 29   
Figure 11. BDMA and DMAMUX2 interconnection 31   
Figure 12. Timing diagram of I2C4 transmission with D3 domain in Autonomous mode. 33   
Figure 13. Hardware requirements and current consumption measurement. 34   
Figure 14. Application workspace selection. 35   
Figure 15. Message after running Mode 1. 36   
Figure 16. Message after running Mode 2. 37   
Figure 17. Message after running Mode 3. 38   
Figure 18. Message after running Mode 4 . . 39   
Figure 19. Domains state impact on power consumption 40

# System architecture

The advanced eNVM technology and architecture used on the STM32H7x3 line devices, enable the higher frequency of the core (up to 480 MHz). The multiple power domains provide a smart solution to the power-consumption challenges.

The system is partitioned as follows:

one CPU sub-system: Arm®(a) Cortex®-M7 core, with associated peripherals clocked according to CPU activity

Three power domains:

D1 domain: high-bandwidth and high-performance domain with the Cortex®-M7 core and acceleration mechanisms. This domain encompasses the high  
bandwidth features and smart management thanks to the AXl bus matrix.   
D2 domain: I/O processing domain, containing most peripherals that are less bandwidth demanding.   
D3 domain: designed to manage the Low-power mode (embeds the system configuration block to keep the system state, the GPlO status). This domain is designed to be autonomous, embedding a 64-Kbyte RAM and a subset of peripherals to run basic functions, while the D1 and D2 domains can be shut-off to save power.

Figure 1 illustrates the system architecture of the STM32H7x3 line devices.

![](images/896f9bb4a33ec7cfaf07f4af76c899a1a9e5095d5506624ee5f5cf0629a58526.jpg)  
Figure 1. System architecture for STM32H7x3 line devices

# System supply configuration

The VcoRE domain supply can be provided by the voltage regulator (LDO) or by an external supply (through VcAp: LDO bypass). VcoRE supplies all the digital circuitries except for the backup domain and the standby circuitry.

The VcoRe domain is split into the following sections:

o D1 domain containing the CPU (Cortex®-M7), Flash memory, memories interface and graphical peripherals D2 domain containing analog and digital peripherals D3 domain containing the system control, I/O logic and low-power peripherals.

The different supply configurations are controlled through the LDOEN and BYPASS bits in PWR control register 3 (PWR_CR3). The choice of the VcoRE domain supply can be done only once, before configuring the system clock source.

For more details about supply configuration control, refer to the power supplies section in the STM32H7x3 advanced Arm®-based 32-bit MCUs reference manual (RM0433).

# 2.1 Voltage regulator (LDO) supply

The voltage regulator (LDO) supplies the three power domains (D1, D2 and D3 - D1 and D2 can be switched off independently). The LDO output can be adjusted according to the application needs through the following power supply levels:

VOS0:\~1.35 V • VOS1:\~1.2 V • VOS2: \~1.1 V • VOS3 / SVOS3: \~1.0 V • SVOS4: \~0.9 V • SVOS5: \~0.7 V

Note:

For more accurate values of voltage scaling output, refer to product datasheet.

According to the frequency, the voltage scaling (vOS) can be reduced to further optimize power consumption. By default, VOS3 is selected after power up. VOS can be changed onthe-fly in the PWR_D3CR register, to fit with the required system performance.

The voltage regulator provides three different operating modes: Main regulator (MR), Low-power (LP) or off. These modes are used depending on the system operating modes (Run, Stop and Standby).

The table belowillustrates thedifferent erating modes and voltage scaling  thevle regulator in Run, Stop and Standby modes.

Table 1. Voltage regulator operating mode and voltage scaling   

<table><tr><td rowspan=1 colspan=1>Mode</td><td rowspan=1 colspan=1>Regulatoroperatingmode</td><td rowspan=1 colspan=1>VOS</td><td rowspan=1 colspan=1>CPU(MHz)</td><td rowspan=1 colspan=1>AXI(MHz)</td><td rowspan=1 colspan=1>AHB(MHz)</td><td rowspan=1 colspan=1>APB(MHz)</td><td rowspan=1 colspan=1>Description</td></tr><tr><td rowspan=4 colspan=1>Run</td><td rowspan=4 colspan=1>MR</td><td rowspan=1 colspan=1>VOSO</td><td rowspan=1 colspan=1>480</td><td rowspan=1 colspan=1>240</td><td rowspan=1 colspan=1>240</td><td rowspan=1 colspan=1>120</td><td rowspan=1 colspan=1>VCORE boost allowing to reach the systemmaximum frequency</td></tr><tr><td rowspan=1 colspan=1>VOS1</td><td rowspan=1 colspan=1>400</td><td rowspan=1 colspan=1>200</td><td rowspan=1 colspan=1>200</td><td rowspan=1 colspan=1>100</td><td rowspan=1 colspan=1>High performance</td></tr><tr><td rowspan=1 colspan=1>VOS2</td><td rowspan=1 colspan=1>300</td><td rowspan=1 colspan=1>150</td><td rowspan=1 colspan=1>150</td><td rowspan=1 colspan=1>75</td><td rowspan=1 colspan=1>Medium performance and consumption</td></tr><tr><td rowspan=1 colspan=1>VOS3</td><td rowspan=1 colspan=1>200</td><td rowspan=1 colspan=1>100</td><td rowspan=1 colspan=1>100</td><td rowspan=1 colspan=1>50</td><td rowspan=1 colspan=1>Optimized performance and low-powerconsumption. By default VOS3 is selected aftersystem reset.</td></tr><tr><td rowspan=3 colspan=1>Stop</td><td rowspan=1 colspan=1>MR or LP</td><td rowspan=1 colspan=1>SVOS3</td><td rowspan=1 colspan=4></td><td rowspan=1 colspan=1>The regulator can be:- in Main mode to allow fast exit from Stop mode- in LP mode to obtain a lower VcoRE supply leveland extend the exit-from-stop latency.</td></tr><tr><td rowspan=2 colspan=1>LP</td><td rowspan=1 colspan=1>SVOS4</td><td rowspan=2 colspan=4>NA</td><td rowspan=2 colspan=1>The Stop mode consumption is further reducedwith a lower voltage level for SVOS4 and SVOS5scaling.In SVOS4/SVOS5, the content of the registers andmemories is not guaranteed.</td></tr><tr><td rowspan=1 colspan=1>SVOS5</td></tr><tr><td rowspan=1 colspan=1>Standby</td><td rowspan=1 colspan=1>Off</td><td rowspan=1 colspan=1>NA</td><td rowspan=1 colspan=4></td><td rowspan=1 colspan=1>Content of the registers and memories is lostexcept for the Standby circuitry and the backupdomain.</td></tr></table>

The functions defined in stm32h7xx_hal_pwr_ex.c file and described in the table below, allow the voltage scaling configuration in STM32Cube_FW_H7.

Table 2. Configure the voltage scaling using STM32Cube_FW_H7   

<table><tr><td rowspan=1 colspan=1>Function</td><td rowspan=1 colspan=1>Ouptut</td><td rowspan=1 colspan=1>Input</td><td rowspan=1 colspan=1>Description</td></tr><tr><td rowspan=1 colspan=1>HAL_PWREx_ControlVoltageScaling</td><td rowspan=2 colspan=1>HAL_ StatusTypeDef</td><td rowspan=1 colspan=1>PWR_REGULATOR_VOLTAGE_SCALEOPWR_REGULATOR_VOLTAGE_SCALE1PWR_REGULATOR_VOLTAGE_SCALE2PWR_REGULATOR_VOLTAGE_SCALE3</td><td rowspan=1 colspan=1>Configure the output voltage ofthe main internal regulator.</td></tr><tr><td rowspan=1 colspan=1>HAL_PWREx_ControlStopModeVoltageScaling</td><td rowspan=1 colspan=1>PWR_REGULATOR_SVOS_SCALE3PWR_REGULATOR_SVOS_SCALE4PWR_REGULATOR_SVOS_SCALE5</td><td rowspan=1 colspan=1>Configure the output voltage ofthe main internal regulator inStop mode.</td></tr></table>

The Stop mode voltage scaling for SvOS4 and SvOS5 sets the voltage regulator in Lowpower (LP) mode automatically to further reduce power consumption.

When preselecting Svos3, the use of the voltage regulator Low-power mode can be selected by LPDS register bit in the PWR_CR1 register.

The figure below illustrates the VcoRE voltage scaling versus system power modes.

![](images/6000611adffdb4e437bc0ee54822d0a8e2a7349e90692e75aad10f738faf8df9.jpg)  
Figure 2. VcoRE voltage scaling versus system power modes

MSv40347V3

# 2.2 Voltage regulator bypass

In STM32H7x3 line devices, the regulator bypass is managed by software through LDOEN and BYPASS bits in the PWR_CR3 register. Vcore is delivered by an external power supply through VCAP pin. At system startup, the MCU starts under LDO then the user can switch to the regulator bypass mode by modifying the LDOEN and BYPASS bits with the software.

The figure below illustrates the system supply configuration for STM32H7x3 line devices (refer to the 'VCAP external capacitor' section of the datasheet for external capacitor values).

![](images/68ecde92aeb5567266b6dae49b452a8246bc5ff8928f7f29126c3a26bf1226e5.jpg)  
Figure 3. System supply configuration

In STM32Cube_FW_H7, the function described in the table below allows the usage of bypass voltage regulator feature.

Table 3. Configure the system power supply using STM32Cube_FW_H7   

<table><tr><td rowspan=1 colspan=1>Function</td><td rowspan=1 colspan=1>Output</td><td rowspan=1 colspan=1>Input</td><td rowspan=1 colspan=1>Description</td></tr><tr><td rowspan=2 colspan=1>HAL_PWREx_ConfigSupply</td><td rowspan=2 colspan=1>HAL_StatusTypeDef</td><td rowspan=1 colspan=1>PWR_LDO_SUPPLY</td><td rowspan=1 colspan=1>The LDO supplies theVcore power domains.</td></tr><tr><td rowspan=1 colspan=1>PWR_EXTERNAL_SOURCE_SUPPLY</td><td rowspan=1 colspan=1>The LDO is bypassed.</td></tr></table>

# CPU sub-system configuration

# 3.1 Peripheral allocation

The peripheral allocation is used by the following peripherals:

the RCC to automatically control the clock gating according to the CPU and domain modes • the PWR to control the supply voltages of D1, D2 and D3 domains

The CPU allocates a peripheral by setting the dedicated PERxEN bit located in the RCC_xxxxENR or RCC_C1_xxxxENR registers.

When using STM32Cube_FW_H7, the peripheral is allocated through the dedicated function defined in stm32h7xx_hal_rcc.h:

_HAL_RCC_XXXX_CLK_ENABLE();

The CPU controls also the peripheral clocks gating when it is in CSleep mode through PERxLPEN bits located into RCC_xxxxLPENR or RCC_C1_xxxxLPENR registers.

When using STM32Cube_FW_H7, the peripheral clocks are controlled in CSleep mode through the dedicated function defined in stm32h7xx_hal_rcc.h:

_HAL_RCC_XXXX_CLK_SLEEP_ENABLE();

The peripheral allocation bits (PERxEN bits) are used by the hardware to provide the kernel and bus interface clocks to the peripherals. However they are also used to link peripherals to the CPU (CPU sub-system). In this way, the hardware is able to safely gate the peripheral clocks and bus matrix clocks according to CPU states. The PWR block also uses this information to control properly the domain states.

Figure 4 gives an example of peripheral allocation.

The CPU enables SDMMC1, SPI5 and SRAM1. Other memories (FLASH, AXISRAM, ITCM, DTCM and SRAM4) are implicitly allocated to the CPU. As a result, there is no enable bit allowing the CPU to allocate these memories.

The CPU needs to enable the memories located in the D2 domain (SRAM1, SRAM2 and SRAM3) before using them. The BackupSRAM has a dedicated enable bit in order to gate the bus interface clock. The CPU needs to enable the BackupSRAM prior to use it.

The group composed of the CPU, bus matrix 1/2/3 and allocated peripherals, makes up a CPU-subsystem.

Note:

FLASH, AXISRAM, ITCM, DTCM, SRAM4, IWGD1, IWGD2, PWR, EXTI and RCC are common resources, implicitly allocated to the CPU.

![](images/3fce1a19d4f46130e10c01084487a140584db422ff47f4669a0be62e5206b29c.jpg)  
Figure 4. Example of peripheral allocation

MSv41941V3

# 3.2 D3 Autonomous mode

The Autonomous mode allows providing the peripheral clocks to peripherals located in the D3 domain, even if the CPU is in CStop mode. When a peripheral is enabled and has its autonomous bit activated (PERxAMEN bit in the RCC_D3AMR register), this peripheral receives its clocks to the D3 domain state, if the CPU is in CStop mode.

When using STM32Cube_FW_H7, the peripheral Autonomous mode is enabled/disabled via the following functions defined in stm32h7xx_hal_rcc.h file:

√ Enable peripheral in Autonomous mode: HAL_RCC_XXXX_CLKAM_ENABLE(); Disable peripheral from Autonomous mode: _HAL_RCC_XXXX_CLKAM_DISABLE();

Setting the RUN_D3 bit in the PWR_CPUCR register, keeps the D3 domain in Run mode while the CPU is in CStop mode and D1 and D2 domains are in DStop or DStandby mode.

When using STM32Cube_FW_H7, the system D3 domain is kept in Run mode regardless the CPU subsystem modes, via the function defined in stm32h7xx_hal_pwr_ex.c and described in the table below.

Table 4. Configure the D3 domain state regardless CPU subsystem modes using STM32Cube_FW_H7   

<table><tr><td rowspan=1 colspan=1>Function</td><td rowspan=1 colspan=1>Output</td><td rowspan=1 colspan=1>Input</td><td rowspan=1 colspan=1>Description</td></tr><tr><td rowspan=2 colspan=1>HAL_PWREx_ConfigD3Domain</td><td rowspan=2 colspan=1>Void</td><td rowspan=1 colspan=1>PWR_D3_DOMAIN_RUN</td><td rowspan=1 colspan=1>D3 domain stays in Run moderegardless of the CPU sub-systemmode.</td></tr><tr><td rowspan=1 colspan=1>PWR_D3_DOMAIN_STOP</td><td rowspan=1 colspan=1>D3 domain follows the CPUsub-system mode.</td></tr></table>

Note:

RCC does not switch off the PLLs as the D3 domain in Run mode.

# Power control modes

# 4.1 Operating modes

The operating modes allow controlling the clock distribution to the different system blocks and powering them. The system operating mode is driven by the CPU subsystem, D2 domain and system D3 autonomous wakeup. The CPU subsystem includes multiple domains depending on its peripheral allocation.

The operating modes available for the different system blocks are detailed in the table below.

Table 5. STM32H7x3 line operating modes   

<table><tr><td colspan="1" rowspan="1">CPUsubsystemand domains</td><td colspan="1" rowspan="1">Mode</td><td colspan="1" rowspan="1">Description</td></tr><tr><td colspan="1" rowspan="3">CPUsubsystem</td><td colspan="1" rowspan="1">CRun</td><td colspan="1" rowspan="1">- CPU and CPU subsystem peripheral(s) allocated via RCC PERxENbits in RCC_C1_xxxxENR or RCC_xxxxENR, are clocked.</td></tr><tr><td colspan="1" rowspan="1">CSleep</td><td colspan="1" rowspan="1">- The CPU clock is stalled and the CPU subsystem allocatedperipheral(s) clock operates according to RCC PERxLPEN bits.</td></tr><tr><td colspan="1" rowspan="1">CStop</td><td colspan="1" rowspan="1"> CPU and CPU subsystem peripheral(s) clocks are stalled.</td></tr><tr><td colspan="1" rowspan="3">D1 domain</td><td colspan="1" rowspan="1">DRun</td><td colspan="1" rowspan="1">- The D1 domain bus matrix is clocked.- The CPU subsystem operates in CRun or CSleep mode.</td></tr><tr><td colspan="1" rowspan="1">DStop</td><td colspan="1" rowspan="1">- The D1 domain bus matrix clock is stalled.- The CPU subsystem operates in CStop mode and the PDDS_D1 bitselects DStop mode.</td></tr><tr><td colspan="1" rowspan="1">DStandby</td><td colspan="1" rowspan="1">- The D1 domain Vcore supply is powered off.- The CPU subsystem operates in CStop mode and the PDDS_D1 bitselects DStandby mode.</td></tr><tr><td colspan="1" rowspan="3">D2 domain</td><td colspan="1" rowspan="1">DRun</td><td colspan="1" rowspan="1"> The D2 domain bus matrix clock is clocked.- The CPU subsystem has an allocated peripheral in the D2 domainand the CPU subsystem operates in CRun or CSleep mode.</td></tr><tr><td colspan="1" rowspan="1">DStop</td><td colspan="1" rowspan="1">- The D2 domain bus matrix clock is stalled. The CPU subsystem has no peripheral allocated in the D2 domainand PDDS_D2 bit selects DStop mode. The CPU subsystem has an allocated peripheral in D2 domain.The CPU subsystem operates in CStop mode and PDDS_D2 bitselects DStop mode.</td></tr><tr><td colspan="1" rowspan="1">DStandby</td><td colspan="1" rowspan="1">- The D2 domain Vcore supply is powered off.- The CPU subsystem has no peripherals allocated in the D2 domainand PDDS_D2 bit selects DStandby mode.The CPU subsystem has an allocated peripheral in the D2 domain.The CPU subsystem operates in CStop mode and PDDS_D2 bitselects DStandby mode.</td></tr><tr><td colspan="1" rowspan="3">System/D3 domain</td><td colspan="1" rowspan="1">Run</td><td colspan="1" rowspan="1">- The system clock and D3 domain bus matrix clock are running.- The CPU subsystem is in CRun or CSleep mode.- A wakeup signal is active (system D3 Autonomous mode).</td></tr><tr><td colspan="1" rowspan="1">Stop</td><td colspan="1" rowspan="1">— The system clock and D3 domain bus matrix clock are stalled.- The CPU subsystem is in CStop mode and all wakeup signals areinactive(1) and at least one PDDS_Dn bit for any domain selectsStop mode.</td></tr><tr><td colspan="1" rowspan="1">Standby</td><td colspan="1" rowspan="1">- The system is powered down.— The CPU subsystem is in CStop mode and all wakeup signals areinactive(1) and all PDDS_Dn bits for all domains select Standbymode</td></tr></table>

wakeup signals are enabled but no wakeup event is pending.

The operating modes for D1 and D2 domains are independent. However the system operating mode depends on D3 domain operating mode. The table below details the system state according to D1 and D2 domains states.

Table 6. System states for D1 / D2 domains states   

<table><tr><td rowspan=1 colspan=1>D1 domainpower mode</td><td rowspan=1 colspan=1>D2 domainpower mode</td><td rowspan=1 colspan=1>System/D3 domainpower mode</td></tr><tr><td rowspan=1 colspan=1>DRun</td><td rowspan=1 colspan=1>DRun/DStop/DStandby</td><td rowspan=2 colspan=1>Run</td></tr><tr><td rowspan=1 colspan=1>DStop/DStandby</td><td rowspan=1 colspan=1>DStop/DStandby</td></tr><tr><td rowspan=1 colspan=1>DStop/DStandby</td><td rowspan=1 colspan=1>DStop/DStandby</td><td rowspan=1 colspan=1>Stop</td></tr><tr><td rowspan=1 colspan=1>DStandby</td><td rowspan=1 colspan=1>DStandby</td><td rowspan=1 colspan=1>Standby</td></tr></table>

The D1, D2 and system/D3 domains are supplied from a single regulator at a common VcoRE level. The VcoRE supply level follows the system operating mode (Run, Stop, and Standby). The D1 domain and/or D2 domain supply can be powered down individually when these domains are in DStandby mode.

When the system is in RUN mode, the D2 domain is by default in DStop mode unless the CPU allocates at least one peripheral belonging to this domain.

.The table below describes the D2 domain states according to CPU peripheral allocation and D1 domain states.

Table 7. D2 domain states overview   

<table><tr><td colspan="1" rowspan="1">Peripheral allocationin D2 domain</td><td colspan="1" rowspan="1">CPU</td><td colspan="1" rowspan="1">D1 domain</td><td colspan="1" rowspan="1">D2 domain</td></tr><tr><td colspan="1" rowspan="2">None</td><td colspan="1" rowspan="1">CRun or CSleep</td><td colspan="1" rowspan="1">DRun</td><td colspan="1" rowspan="2">DStop / DStandby</td></tr><tr><td colspan="1" rowspan="1">CStop</td><td colspan="1" rowspan="1">DStop / DStandby</td></tr><tr><td colspan="1" rowspan="2">Peripherals allocated</td><td colspan="1" rowspan="1">CRun or CSleep</td><td colspan="1" rowspan="1">DRun</td><td colspan="1" rowspan="1">DRun</td></tr><tr><td colspan="1" rowspan="1">CStop</td><td colspan="1" rowspan="1">DStop / DStandby</td><td colspan="1" rowspan="1">DStop / DStandby</td></tr></table>

The state diagram below illustrates the different power control modes available for STM32H7x3 devices.

![](images/729b6597874364b4720a70e77d2d07f42365be5c8bc150f3b2c500fa459e1a4b.jpg)  
Figure 5. Power control modes detailed state diagram

# 4.2 Low-power modes

Several low-power modes are available to save power when the CPU does not execute code (when waiting for an external event). The user must select the mode providing the best compromise between low power-consumption, short startup-time and available wakeup sources for the application.

STM32H7x3 ne devis feature e ollowing low-powermodes:

CSleep (CPU clock stopped)   
• CStop (CPU sub-system clock stopped)   
• DStop (domain bus matrix clock stopped)   
• Stop (system clock stopped)   
• DStandby (domain powered down) Standby (system powered down) When using STM32Cube_FW_H7, several functions are defined for low-power modes.   
These functions are described in the table below.

Table 8. Functions description used for low-power modes in STM32Cube_FW_H7   

<table><tr><td rowspan=1 colspan=1>Low-powermode</td><td rowspan=1 colspan=1>Function</td><td rowspan=1 colspan=1>Input</td><td rowspan=1 colspan=1>Description</td></tr><tr><td rowspan=2 colspan=1>CSleep</td><td rowspan=2 colspan=1>HAL_PWR_EnterSLEEPMode</td><td rowspan=1 colspan=1>PWR_MAINREGULATOR_ONPWR_LOWPOWERREGULATOR_ON</td><td rowspan=1 colspan=1>The regulator parameter is notused for STM32H7x3 line devicesand is kept as parameter just tomaintain compatibility with thelower-power families (STM32L).</td></tr><tr><td rowspan=1 colspan=1>PWR_SLEEPENTRY_WFIPWR_SLEEPENTRY_WFE</td><td rowspan=1 colspan=1>Specifies if Sleep mode is enteredwith WFI or WFE instruction.</td></tr><tr><td rowspan=3 colspan=1>CStop /DStop</td><td rowspan=3 colspan=1>HAL_PWREx_EnterSTOPMode</td><td rowspan=1 colspan=1>PWR_MAINREGULATOR_ONPWR_LOWPOWERREGULATOR_ON</td><td rowspan=1 colspan=1>Specifies the regulator state inStop mode.</td></tr><tr><td rowspan=1 colspan=1>PWR_STOPENTRY_WFIPWR_STOPENTRY_WFE</td><td rowspan=1 colspan=1>Specifies if Stop mode is enteredwith WFI or WFE instruction.</td></tr><tr><td rowspan=1 colspan=1>PWR_D1_DOMAINPWR_D2_DOMAINPWR_D3_DOMAIN</td><td rowspan=1 colspan=1>Specifies the domain to enter Stopmode.</td></tr><tr><td rowspan=2 colspan=1>Stop</td><td rowspan=2 colspan=1>HAL_PWR_EnterSTOPMode</td><td rowspan=1 colspan=1>PWR_MAINREGULATOR_ONPWR_LOWPOWERREGULATOR_ON</td><td rowspan=1 colspan=1>Specifies the regulator state inStop mode.</td></tr><tr><td rowspan=1 colspan=1>PWR_STOPENTRY_WFIPWR_STOPENTRY_WFE</td><td rowspan=1 colspan=1>Specifies if Stop mode is enteredwith WFI or WFE instruction.</td></tr><tr><td rowspan=1 colspan=1>DStandby</td><td rowspan=1 colspan=1>HAL_PWREx_EnterSTANDBYMode</td><td rowspan=1 colspan=1>PWR_D1_DOMAINPWR_D2_DOMAINPWR_D3_DOMAIN</td><td rowspan=1 colspan=1>Specifies the domain to enterStandby mode.</td></tr><tr><td rowspan=1 colspan=1>Standby</td><td rowspan=1 colspan=1>HAL_PWR_EnterSTANDBYMode</td><td rowspan=1 colspan=1>Void</td><td rowspan=1 colspan=1>System enters Standby mode.</td></tr></table>

# Operating modes comparison between STM32F7 Series and STM32H7x3 line devices

What is new in STM32H7x3 line devices regarding STM32F7 Series MCUs, is the flexibility of managing power supply on three domains. For example you can switch off a whole domain and keep the two others running.

The table below illustrates shared operating modes between STM32F7 Series and STM32H7x3 devices.

Table 9. Shared operating modes - STM32F7 Series and STM32H7x3 line devices   

<table><tr><td rowspan=2 colspan=1>Sharedoperatingmodes</td><td rowspan=2 colspan=1>STM32F7Seriesdevices</td><td rowspan=1 colspan=4>STM32H7x3 line devices</td></tr><tr><td rowspan=1 colspan=1>CPU state</td><td rowspan=1 colspan=1>D1 domain</td><td rowspan=1 colspan=1>D2 domain</td><td rowspan=1 colspan=1>D3 domain</td></tr><tr><td rowspan=1 colspan=1>Run</td><td rowspan=1 colspan=1>Run</td><td rowspan=1 colspan=1>CRun</td><td rowspan=1 colspan=1>DRun</td><td rowspan=1 colspan=1>DRun</td><td rowspan=1 colspan=1>Run</td></tr><tr><td rowspan=1 colspan=1>Sleep</td><td rowspan=1 colspan=1>Sleep</td><td rowspan=1 colspan=1>CSleep</td><td rowspan=1 colspan=1>DRun</td><td rowspan=1 colspan=1>DRun</td><td rowspan=1 colspan=1>Run</td></tr><tr><td rowspan=1 colspan=1>Stop</td><td rowspan=1 colspan=1>Stop</td><td rowspan=1 colspan=1>CStop</td><td rowspan=1 colspan=1>DStop</td><td rowspan=1 colspan=1>DStop</td><td rowspan=1 colspan=1>Stop</td></tr><tr><td rowspan=1 colspan=1>Standby</td><td rowspan=1 colspan=1>Standby</td><td rowspan=1 colspan=1>CStop</td><td rowspan=1 colspan=1>DStandby</td><td rowspan=1 colspan=1>DStandby</td><td rowspan=1 colspan=1>Standby</td></tr></table>

To use low-power modes, STM32F7 Series and STM32H7x3 line devices share also the same functions defined in STM32Cube_FW_F7 and STM32Cube_FW_H7. These functions are described in the table below.

Table 10. Shared functions - STM32F7 Series and STM32H7x3 line devices   

<table><tr><td rowspan=1 colspan=1>Sharedlow-powermode</td><td rowspan=1 colspan=1>Function</td><td rowspan=1 colspan=1>Output</td><td rowspan=1 colspan=1>Input</td><td rowspan=1 colspan=1>Description</td></tr><tr><td rowspan=1 colspan=1>Sleep</td><td rowspan=1 colspan=1>HAL_PWR_EnterSLEEPMode</td><td rowspan=3 colspan=1>Void</td><td rowspan=1 colspan=1>Regulator(1)SLEEPEntry</td><td rowspan=1 colspan=1>Cortex®-M7 entersSleep mode.</td></tr><tr><td rowspan=1 colspan=1>Stop</td><td rowspan=1 colspan=1>HAL_PWR_EnterSTOPMode</td><td rowspan=1 colspan=1>RegulatorSTOPEntry</td><td rowspan=1 colspan=1>System enters Stopmode.</td></tr><tr><td rowspan=1 colspan=1>Standby</td><td rowspan=1 colspan=1>HAL_PWR_EnterSTANDBYMode</td><td rowspan=1 colspan=1>Void</td><td rowspan=1 colspan=1>System entersStandby mode.</td></tr></table>

This parameter is not used for STM32H7x3 devices nor for STM32F7 Series. I is kept as a parameter just to maintain compatibility with the lower-power MCUs.

# Peripheral clock distribution

The peripheral clocks are provided by the RCC to the peripherals. Two kinds of clock are available:

• bus interface clocks • kernel clocks.

On STM32H7x3 line devices, the peripherals generally receive one or several bus and kernel clocks.

The figure below describes the peripheral clock distribution on STM32H7x3 line devices.

![](images/6d593b663540a0bad1d50f28c19030890a4af146711aedba6ac17a6fc2b4606e.jpg)  
Figure 6. Peripheral clock distribution

MSv44231V2

A kernel clock allows the peripheral to use a different clock frequency for the peripheral function (compared to the peripheral bus clock).

Peipherals wi  kerel cock ecassifid n seveal gus:

PK1: Peripherals with a kernel clock following the same clock gating as the peripheral bus clock.   
Examples: FMC, QUADSPI, DFSDM1, I2Cx, LPTIMx, SPI4/5/6, SWPMI, USARTx, UARTx, LPUART1, SDMMC1/2, SAIx, ADCx, DSI, FDCAN, HDMI-CEC, LTDC, RNG, SPDIFRX, USBxLPI, USBxOTG.   
PK2: Peripherals with a kernel clock request signal (select clock source HSI or CSI). Examples: I2Cx, SPI4/5/6, USARTx, UARTx, LPUART1.   
These PK2 peripherals are able to run when the CPU subsystem allocating the peripheral is in CStop or the domain is in DStop or the whole system is in Stop.For example, if the system is expecting messages via l2C4, the whole system can be put in Stop mode. When the I2C4 peripheral detects a START bit, it generates a kernel clock

request which enables the HSI or CSI. This kernel clock is provided only to the requester (I2C4) and decodes then the incoming message.

PK3: peripherals with kernel clock source LSE or LSI.   
Examples: HDMI-CEC, LPTIM1/2/3/4/5, RNG, RTC/AWU, USARTx, UARTx, LPUART1.   
These PK3 peripherals are able to run when the CPU subsystem allocating the peripheral is in CStop, when the domain is in DStop or when the system is in Stop. PK4: peripherals with external slave clock as kernel clock.   
Examples: MDIOS, I2Cx, SPIx.

The peripherals having a kernel clock request, operates in Stop mode if the two following conditions are filled:

the system uses SvOS3 level.   
the PERxAMEN bit, when available on the peripheral (ones located in D3 domain), is set to request the kernel clock.

When using STM32Cube_FW_H7, the kernel clock of the peripheral is selected using the following function defined in stm32h7xx_hal_rcc_ex.h file:

# Wakeup from Stop/CStop mode

The extended interrupt and event controller module (EXTl) allows the system and/or the CPU to wake up from respectively the Stop mode or the CStop mode.

What is new in STM32H7x3 devices is that these events are coming from peripherals.   
These events are handled by the EXTl as configurable or as direct events.

There are three types of peripheral output signals connected to the EXTI input events:

Wakeup signals: generated by the peripheral without any bus- interface clock (when the only clock running is the kernel one). These signals are referred to as xxx_wkup and are not available for some peripherals.

# Note:

the use of a kernel clock for I2C and SPI peripherals is supported only in Slave mode, so the wakeup signals available in these peripherals are supported only in Slave mode.

Interrupt signals: generated only if the peripheral bus-interface clock is running. These interrupt signals are generally connected directly to NVIC of CPU and referred t as xxx_it.

Signals: pulses generated by the peripheral. Once a peripheral generates a signal, no action (flag clearing) is required at peripheral level.

Each EXTI input event has different wakeup capability or possible target:

CPU wakeup (CPU): the input event is enabled to wake up the CPU.

CPU and D3 domain wakeup for Autonomous Run mode (ANY): the input event is enabled to wake up the CPU or the D3 domain only for Autonomous Run mode phase.

For more details about the EXTl, refer to the reference manual RM0433: dedicated section for ExTI main features and specific table for wakeup inputs.

The figure below illustrates the EXTI bloc diagram on the STM32H7x3 line devices.

![](images/576e9fbc97a7df465641b73bfe7acb7b13e2b9c1afc8f6f6a4444f9e704c2b8a.jpg)  
Figure 7. EXTI block diagram on STM32H7x3 line devices

MSv41947V1

# EXTI pending requests clear for D3 Run mode inputs

As described above, the EXTI event inputs are able to wake up the D3 domain for Autonomous Run mode which has a pending request logic.

This pending request can be cleared by four input sources, allowing D3 domain to resume the Stop mode.

D dmamux2_evt6 • dmamux2_evt7 • Iptim4_out

The figure and table below describe the D3 pending request clear logic and the EXTI pending requests clear inputs.

![](images/2bebfc3209dd85def0be4aa6311353e1ab27fb50146f3b32f1a0457602371f16.jpg)  
Figure 8. D3 pending request clear logic

Table 11. EXTI pending request clear inputs   

<table><tr><td rowspan=1 colspan=4>Source</td><td rowspan=1 colspan=4>Destination</td></tr><tr><td rowspan=1 colspan=1>Domain</td><td rowspan=1 colspan=1>Bus</td><td rowspan=1 colspan=1>Peripheral</td><td rowspan=1 colspan=1>Signal</td><td rowspan=1 colspan=1>Signal</td><td rowspan=1 colspan=1>Peripheral</td><td rowspan=1 colspan=1>Bus</td><td rowspan=1 colspan=1>Domain</td></tr><tr><td rowspan=4 colspan=1>D3</td><td rowspan=2 colspan=1>AHB4</td><td rowspan=2 colspan=1>DMAMUX2</td><td rowspan=1 colspan=1>dmamux2__evt6</td><td rowspan=1 colspan=1>PRCO</td><td rowspan=4 colspan=1>EXTI</td><td rowspan=4 colspan=1>APB4</td><td rowspan=4 colspan=1>D3</td></tr><tr><td rowspan=1 colspan=1>dmamux2_evt7</td><td rowspan=1 colspan=1>PRC1</td></tr><tr><td rowspan=2 colspan=1>APB4</td><td rowspan=1 colspan=1>LPTIM4</td><td rowspan=1 colspan=1>Iptim4_out</td><td rowspan=1 colspan=1>PRC2</td></tr><tr><td rowspan=1 colspan=1>LPTIM5</td><td rowspan=1 colspan=1>Iptim5_out</td><td rowspan=1 colspan=1>PRC3</td></tr></table>

In STM32Cube_FW_H7, the function described in the table below allows the configuration of the EXTI input line for D3 domain, in order to specify the clear source of D3 pending event.

Table 12. Specifying the clear source of D3 pending event in STM32Cube_FW_H7   

<table><tr><td rowspan=1 colspan=1>Function</td><td rowspan=1 colspan=1>Output</td><td rowspan=1 colspan=1>Input</td><td rowspan=1 colspan=1>Description</td></tr><tr><td rowspan=3 colspan=1>HAL_EXTI_D3_EventInputConfig</td><td rowspan=3 colspan=1>Void</td><td rowspan=1 colspan=1>EXTI_Line</td><td rowspan=1 colspan=1>Specifies the EXTI line that iswaking up D3 domain.</td></tr><tr><td rowspan=1 colspan=1>EXTI_LineCmd: Enable/disable</td><td rowspan=1 colspan=1>Enable or disable the EXTI line.</td></tr><tr><td rowspan=1 colspan=1>EXTI_ClearSrc:BDMA_CH6_CLEARBDMA_CH7_CLEAR- LPTIM4_OUT_CLEAR- LPTIM5_OUT_CLEAR</td><td rowspan=1 colspan=1>This parameter specifies the clearsource of D3 pending event to allowD3 resume Stop mode.</td></tr></table>

# Low-power application

# 3.1 Low-power application example

This example is based on I2C transmission using ST shield (X-NUCLEO-IKS01A2). The purpose is to highlight the smart power management of STM32H7x3 devices using three power domains.

The demo code is based on four modes:

Mode 1: this mode is equivalent to legacy products which keep all domains active to transfer data from ST shield through I2C1 (with CPU in Sleep mode).   
Mode 2: in this mode, the power efficiency is enhanced keeping D1 in DRun, D3 in Run and D2 in DStandby. The data transfer is switched to I2C4 instead of I2C1. This highlights the architecture flexibility, moving from one peripheral instances in D2 to another in D3, without changing external connections.   
Mode 3: same as Mode 2 but the D1 domain is in DStandby for more power- energy saving. This mode shows the D3 Autonomous Run mode.   
Mode 4: same as Mode 3 but the D3 domain switches between two modes (Run and Stop) all along the transfer, in order to optimize power-consumption.

The demo code uses the Nucleo board NUCLEO-H743ZI and the X-NUCLEO-IKS01A2 expansion board to get temperature values from HTS221 sensor via I2C bus.

The figure below shows the connections between peripherals and memories.

![](images/c7845005f50ddf7b77920e64c8141433676e8643c21cf9f7f709d1f048780364.jpg)  
Figure 9. Peripherals and memories connections

MSv46602V1

# 8.1.1 Mode 1

This mode is equivalent to Sleep mode in STM32F7 Series devices.

Temperature acquisition from shield to SRAM1 through I2C1 in the D2 domain Saving data from SRAM4 to BackupSRAM after waking up Cortex®-M7

Table 13. Mode 1 - operating modes for each domain   

<table><tr><td rowspan=1 colspan=1>D1 domain</td><td rowspan=1 colspan=1>D2 domain</td><td rowspan=1 colspan=1>D3 domain</td></tr><tr><td rowspan=1 colspan=1>DRun (CSleep)</td><td rowspan=1 colspan=1>DRun</td><td rowspan=1 colspan=1>Run</td></tr></table>

# 8.1.2 Mode 2

Temperature acquisition from shield to SRAM4 through I2C4 in the D3 domain Saving data from SRAM4 to BackupSRAM after waking up Cortex®-M7

Table 14. Mode 2 - operating modes for each domain   

<table><tr><td rowspan=1 colspan=1>D1 domain</td><td rowspan=1 colspan=1>D2 domain</td><td rowspan=1 colspan=1>D3 domain</td></tr><tr><td rowspan=1 colspan=1>DRun (CSleep)</td><td rowspan=1 colspan=1>DStandby</td><td rowspan=1 colspan=1>Run</td></tr></table>

# 8.1.3 Mode 3

Temperature acquisition from shield to SRAM4 through I2C4 in the D3 domain Saving data from SRAM4 to BackupSRAM after waking up Cortex®-M7

Table 15. Mode 3 - operating modes for each domain   

<table><tr><td rowspan=1 colspan=1>D1 domain</td><td rowspan=1 colspan=1>D2 domain</td><td rowspan=1 colspan=1>D3 domain</td></tr><tr><td rowspan=1 colspan=1>DStandby</td><td rowspan=1 colspan=1>DStandby</td><td rowspan=1 colspan=1>Run</td></tr></table>

# 8.1.4 Mode 4

Temperature acquisition from shield to SRAM4 through I2C4 in the D3 domain C Saving data from SRAM4 to BackupSRAM after waking up Cortex®-M7

Table 16. Mode 4 - operating modes for each domain   

<table><tr><td rowspan=1 colspan=1>D1 domain</td><td rowspan=1 colspan=1>D2 domain</td><td rowspan=1 colspan=1>D3 domain</td></tr><tr><td rowspan=1 colspan=1>DStandby</td><td rowspan=1 colspan=1>DStandby</td><td rowspan=1 colspan=1>Run / Stop</td></tr></table>

# 8.2 Mode 4 - D3 Autonomous mode

This section details the D3 Autonomous mode (Mode 4) and its benefits on power consumption.

# 8.2.1 Memory retention

The D3 domain features 64 Kbytes of SRAM (SRAM4), available to retain data while the D1 and D2 domains are in DStandby mode.

This feature can be used in several use-cases:

C To retain the application code in order to recover properly from DStandby mode To retain the data from / to a sensor when the CPU enters CStop (with D1 or D2 domain in DStandby) between two consecutive operations.

SRAM4 remains available as long as the system is not in Standby mode. But if the system is in Standby mode, it is still possible to retain data in BackupSRAM. Its size is optimized to 4 Kbytes to reduce the associated leakage.

In the given example, both the SRAM4 and BKUP_SRAM are used, respectively for saving the transmitted data from temperature sensor when D3 is in Autonomous mode, and saving the final data after waking up the CPU from CStop mode.

# 8.2.2 Example description

Figure 10 shows the proposed implementation. At regular time interval given by LPTIM2 (each 1 s), the D3 domain wakes up from Stop mode. The D3 domain executes the following tasks in Autonomous mode:

1. transfer the data from SRAM4 to I2C4 using BDMA   
2. when the I2C4 interface indicates that the last 2 bytes has been transferred from I2C4 to SRAM4, the D3 domain is switched to Stop mode.

After transferring the first or last 10 bytes, BDMA_channel7 (BDMA_ch7) sends an interrupt to wake up the CPU from CStop mode. When the CPU is in CRun mode, it prepares data located into SRAM4 to be processed and transferred to the BackupSRAM.

![](images/50f079457d876ebd91a704dfd4559df4ae87a394c1132e92ddb4fbbd60cf9b5e.jpg)  
Figure 10. Timing diagram of SRAM4 to I2C4 transfer with BDMA

Note:

To toggle the D3 domain between Stop and Run modes, the Run mode must be triggered by wakeup event (Ilptim2_out each 1 s) so that the D3 domain can clear this event with dmamux2_evt7 signal and switch back the D3 domain to Stop mode.

# RCC programming

In this example, the CPU sub-system also includes the peripherals of the D3 domain that are used for data transfer: LPTIM2, BDMA, DMAMUX2, SRAM4, I2C4, BackupSRAM.

These peripherals must be programmed in Autonomous mode, in order to operate even when the CPU is in CStop mode.

When using STM32Cube_FW_H7, the following functions defined in stm32h7xx_hal_rcc.h file are used to program peripherals in Autonomous mode:

• _HAL_RCC_LPTIM2_CLKAM_ENABLE();   
• _HAL_RCC_BDMA_CLKAM_ENABLE();   
• _HAL_RCC_D3SRAM1_CLKAM_ENABLE();   
• HAL_RCC_I2C4_CLKAM_ENABLE();   
• _HAL_RCC_BKPRAM_CLKAM_ENABLE();

# PWR programming

In this mode, the PWR block must be programmed in order to:

• prevent system D3 domain to enter Standby mode when the data transfer is complete • allow D1 and D2 domains to enter DStandby mode • define the working voltage according to system modes (SvOS3).

# EXTI programming

The Iptim2_out signal is used to wake up the D3 domain from Stop mode when LPTIM2 time interval has elapsed (each 1 s). The Iptim2_out signal is connected to the EXTI input event line number 49.

Selecting BDMA_ch7 as pendclear source of the D3 domain, allow to switch back the D3 domain to Stop mode.

When using STM32Cube_FW_H7, the following function defined in stm32h7xx_hal.c is used to select Iptim2_out signal as wakeup source and dmamux2_evt7 as pendclear source:

HAL_EXTI_D3_EventInputConfig(EXTI_LINE49,ENABLE,BDMA_CH7_CLEAR);

# BDMA and DMAMUX programming

Four BDMA channels are required to execute data transfers between SRAM4 and I2C4:

BDMA_channel0 (BDMA_ch0) is used to transfer data from SRAM4 to I2C4_CR2 register, in order to configure the I2C4 interface to request write transfer to HTS221 sensor.

BDMA_chO uses Req_Gen0 to generate BDMA requests. The generation of BDMA requests is triggered by the rising edge of Iptim2_out signal. This signal is generated by LPTIM2 each 1 s.

BDMA_channel1 (BDMA_ch1) is used to transfer data from SRAM4 to I2C4_TXDR register, in order to send a specified address to HTS221 sensor.

BDMA_ch1 request is generated when I2C4 TX-FIFO is not full (enable TXDMAEN bit in I2C4_CR1 register).

The DMAMUx SYNC1 block is programmed to generate a pulse on its dmamux2_evt1 output when the BDMA request is complete.

BDMA_channel2 (BDMA_ch2) is used to transfer data from SRAM4 to I2C4_CR2 register, in order to configure I2C4 interface to request read transfer from HTS221 sensor.

BDMA_ch2 uses Req_Gen2 to generate BDMA requests. The generation of BDMA requests is triggered by the falling edge of dmamux2_evt1.

BDMA_channel7 (BDMA_ch7) is used to transfer the received data from I2C4_RXDR register (data sent from HTS221 sensor) to SRAM4. BDMA_ch7 transmission is enabled by setting RXDMAEN bit.

BDMA_ch7 is configured to generate interrupts to wake up the CPU from CStop mode each time after half-transfer complete (10 bytes of data) or after full transfer complete (20 bytes of data).

The DMAMUX2 SYNC7 block is programmed to generate a pulse on its dmamux2_evt7 output when the BDMA request is complete. The dmamux2_evt7 signal is used by the EXTI to switch back the D3 domain to Stop mode.

The figure below shows the active signal paths via DMAMUX2.

![](images/eb256dd2ab0dfa291da586c4d5fd815ce8044455ee762b9f2bbd1449901e5b2e.jpg)  
Figure 11. BDMA and DMAMUX2 interconnection

dmamux_req_inx: DMAMux DMA request line inputs (from peripherals or from dmamux_req_genx)   
dmamux_req_outx: DMAMUX requests outputs (to DMA controllers)   
dmamux_evtx: DMAMUX events outputs   
dmamux_trgx: DMAMUX DMA request triggers inputs (to request generator sub-block)

MSv46606V1

# LPTIM2 programming

LPTIM2 is programmed to still operate when the D3 domain enters Stop mode since it uses ck_Isi clock.

LPTIM2 is programmed to wake up the D3 domain from Stop mode each 1 s and to start BDMA_ch0 transfer through Req_Gen0.

# I2C programming

I2C4 is configured to use ck_hsi as kernel clock and programmed to generate BDMA request when TX-FIFO/RX-FIFO is Empty/Full.

A dedicated function called I2C4_ENABLE_DMA_REQUEST ( ) is defined in common.h file to enable BDMA requests generation by the I2C4.

# 8.2.3 Overall description of Mode 4 example

Figure 12 illustrates the timing diagram of I2C4 transmission with D3 domain in Autonomous mode. Detailed steps are the following ones:

The Iptim2_out signal wakes up the D3 domain from Stop mode each 1 s.   
When the D3 domain wakes up from Stop mode, the rising edge of Iptim2_out signal triggers BDMA_ch0 to begin data transfer (TRNSF1).   
As soon as I2C4 TX-FIFO is empty, BDMA_ch1 begins data transfer from SRAM4 to I2C4_TXDR register (TRNSF2).   
The end of this transfer triggers BDMA_ch2 transfer (through dmamux2_ch1_evt) from SRAM4 to I2C_CR2 register (TRNSF3).   
As soon as I2C4 RX-FIFO is full, BDMA_ch7 transfers 2 bytes of data from   
I2C4_RXDR register to SRAM4 (TRNSF4).   
The end of this transfer triggers a dmamux2_evt7 signal which is used to clear the D3_PendClear bit.   
The whole system returns to Stop mode.   
After 5 s and when the expected amount of data has been transmitted (NDT bits of BDMA_CNDTR0 set to 10 indicating half-transfer is complete), the BDMA_ch7 generates an interrupt to wake up the CPU from CStop mode.   
The CPU processes the data located in SRAM4 to be transferred, and copies them to BackupSRAM (CPU_TRSF). The data stored in BackupSRAM are retained while the system is in Stop mode.   
The CPU returns to CStop mode and the whole system return to Stop mode.

LPTIM2 continues to wake up the D3 domain after each 1 s, and BDMA channels continue to do all transfers as mentioned above.

When the expected amount of data has been transmitted (NDT bits of BDMA_CNDTR0 set to 20 indicating transfer is complete), the BDMA_ch7 generates an interrupt to wake up the CPU from CStop mode. The CPU processes the data located in SRAM4 to be transferred, and copies them to BackupSRAM. (CPU_TRSF).

![](images/9a2eda348a473048c01b0d24fb1c29de5754c82eec63c4fda7c9cdee8e0f424a.jpg)  
Figure 12. Timing diagram of I2C4 transmission with D3 domain in Autonomous mode

# 8.3 How to use the application

# 8.3.1 Hardware requirements

To setup the application, the user needs:

the STM32H743ZI-Nucleo board the X-NUCLEO-IKS01A2 expansion board to measure temperature values from HTS221 sensor via I²C bus The X-NUCLEO-IKS01A2 expansion board must be plugged on the matching pins of the STM32 Nucleo board connector. • to connect the board to a computer through ST-Link with a mini USB for programming and debugging • a multimeter to measure the current consumption

![](images/9781f79149a84625cf35edbfcfbe3d60d5b3a8da8888864e0967520b7dcc80c1.jpg)  
Figure 13. Hardware requirements and current consumption measurement   
Picture is not contractual.

# 8.3.2 Software requirements

This example is provided with four workspaces described in the table below.

Table 17. Workspaces available in the example   
Figure 14. Application workspace selection   

<table><tr><td rowspan=2 colspan=1>Workspace</td><td rowspan=1 colspan=4>Conditions of temperature acquisition</td></tr><tr><td rowspan=1 colspan=1>CPU</td><td rowspan=1 colspan=1>D1 domain</td><td rowspan=1 colspan=1>D2 domain</td><td rowspan=1 colspan=1>D3 domain</td></tr><tr><td rowspan=1 colspan=1>STM32H743ZI__Mode1</td><td rowspan=1 colspan=1>CSleep</td><td rowspan=1 colspan=1>DRun</td><td rowspan=1 colspan=1>DRun</td><td rowspan=1 colspan=1>DRun</td></tr><tr><td rowspan=1 colspan=1>STM32H743ZI_Mode2</td><td rowspan=1 colspan=1>CStop</td><td rowspan=1 colspan=1>DRun</td><td rowspan=1 colspan=1>DStandby</td><td rowspan=1 colspan=1>DRun</td></tr><tr><td rowspan=1 colspan=1>STM32H743ZI_Mode3</td><td rowspan=1 colspan=1>CStop</td><td rowspan=1 colspan=1>DStandby</td><td rowspan=1 colspan=1>DStandby</td><td rowspan=1 colspan=1>Run</td></tr><tr><td rowspan=1 colspan=1>STM32H743ZI_Mode4</td><td rowspan=1 colspan=1>CStop</td><td rowspan=1 colspan=1>DStandby</td><td rowspan=1 colspan=1>DStandby</td><td rowspan=1 colspan=1>Run / Stop</td></tr></table>

The user needs to choose the dedicated workspace to execute the selected mode.

File Edit View Project Flash Debug Peripherals Tools SVCS Window Help H PL T Pe   
L STM32H743ZI_Mode1 \*   
Project STM32H743ZI Mode1 STM32H743ZI_Mode2   
Project: Project STM32H743ZI_Mode3 STM32H743ZI Mode4 STM32H743ZI_Mode + Doc Drivers/CMSIS Drivers/STM32H7x_HAL_Driver +· Example/User + Example/MDK-ARM + Drivers/BSP/STM32H7xx_Nucleo_144 + Example/User/BSP CMSIS

# 8.3.3 Running the example

The figures below show the different messages displayed on the terminal after running each mode.

![](images/e316a4c574c7abb82dbed8171d54bb7d55270e88a846c106403a4fb4f10e9f02.jpg)  
Figure 15. Message after running Mode 1

![](images/b1578eea462745c0c02bb7e19bf843e1bc1cee8d358cf015e086e989de506054.jpg)  
Figure 16. Message after running Mode 2

![](images/543812cb32fc0521b75c9f8f0c506a55f96425ca8d1e7c984e05dcaab69ef5c1.jpg)  
Figure 17. Message after running Mode 3

![](images/4729c010b3fa93580631363eaedda8e01f152b6fb65104e6507958a7299b675c.jpg)  
Figure 18. Message after running Mode 4

# 8.4 Power consumption measurements

The measurements below have been done with the following settings:

voltage = 3.3 V system clock HCLK = 64 MHz

The table below describes the measured current consumption in all modes.

Table 18. MCU power consumption in different modes   

<table><tr><td rowspan=1 colspan=1>Mode</td><td rowspan=1 colspan=1>CPU state</td><td rowspan=1 colspan=1>D1 domain</td><td rowspan=1 colspan=1>D2 domain</td><td rowspan=1 colspan=1>D3 domain</td><td rowspan=1 colspan=1>Average MCUcurrentconsumption(mA)</td></tr><tr><td rowspan=1 colspan=1>Mode1</td><td rowspan=1 colspan=1>CSleep</td><td rowspan=1 colspan=1>DRun</td><td rowspan=1 colspan=1>DRun</td><td rowspan=1 colspan=1>Run</td><td rowspan=1 colspan=1>18.7</td></tr><tr><td rowspan=1 colspan=1>Mode2</td><td rowspan=1 colspan=1>CSleep</td><td rowspan=1 colspan=1>DRun</td><td rowspan=1 colspan=1>DStandby</td><td rowspan=1 colspan=1>Run</td><td rowspan=1 colspan=1>14.8</td></tr><tr><td rowspan=1 colspan=1>Mode3</td><td rowspan=1 colspan=1>CStop</td><td rowspan=1 colspan=1>DStandby</td><td rowspan=1 colspan=1>DStandby</td><td rowspan=1 colspan=1>Run</td><td rowspan=1 colspan=1>7.8</td></tr><tr><td rowspan=1 colspan=1>Mode4</td><td rowspan=1 colspan=1>CStop</td><td rowspan=1 colspan=1>DStandby</td><td rowspan=1 colspan=1>DStandby</td><td rowspan=1 colspan=1>Run/Stop</td><td rowspan=1 colspan=1>5.2</td></tr></table>

# Synthesis

The figure below summarizes the STM32H7x3 devices state domains effects on current consumption optimization.

![](images/d15e1571bab37179308fc623da3c14638acdc3ea65381dc00a7916dc9a649426.jpg)  
Figure 19. Domains state impact on power consumption

This figure illustrates the benefits of STM32H7x3 devices smart architecture that manages power supply per domain. Up to 72 % (Mode4) of power consumption is saved compared with an application running only with basic low-power optimization (using Sleep mode only: Mode1).

The new feature, allowing one sub-domain to be disabled while the two other domains remain in Run, enhances the power consumption in our example by 21 % (Mode2).

Activating the batch acquisition mode (D3 domain in Autonomous mode) decreases Mode2 power values down to 7,8 mA and save up to 47 % of power consumption.

Enhancing D3 Autonomous mode by allowing D3 to enter Stop mode when there is no communication ongoing (mode4), saves more power consumption compared to mode3 (up to 33 %).

More power efficient implementations are also available. As an example, the system clock frequency ca be reduced by using the low-power internal oscillator (CSl at 4 MHz) as wakeup clock from Stop mode. This implementation is possible when using D3 Autonomous mode (in Mode 4: switching from Run to Stop), since CSl can be selected as wakeup clock from system Stop mode (STOPWUCK bit in RCC_CFGR register).

# 9 Revision history

Table 19. Document revision history   

<table><tr><td rowspan=1 colspan=1>Date</td><td rowspan=1 colspan=1>Revision</td><td rowspan=1 colspan=1>Changes</td></tr><tr><td rowspan=1 colspan=1>9-Jun-2017</td><td rowspan=1 colspan=1>1</td><td rowspan=1 colspan=1>Initial release.</td></tr><tr><td rowspan=1 colspan=1>15-May-2019</td><td rowspan=1 colspan=1>2</td><td rowspan=1 colspan=1>Updated:Section 1: System architectureSection 2.1: Voltage regulator (LDO) supplySection 2.2: Voltage regulator bypassFigure 5: Power control modes detailed state diagram</td></tr></table>

# IMPORTANT NOTICE  PLEASE READ CAREFULLY

acknowledgement.

the design of Purchasers' products.

No license, express or implied, to any intellectual property right is granted by ST herein.

product or service names are the property of their respective owners.

I