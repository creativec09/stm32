# STM32H7A3/7B3 lines and STM32H7B0 Value line smart power management Expansion Package for STM32Cube

# Introduction

Thalicatioo rovi uielie32HA732H7Baluar pwea Expansion Package r TM32CubeTM32H7A3/7B3 lines andSTM32H7B0 value ineicocontrollrs includ® ®le domain arhitectureoperating independently optimize powerefficncy.

This document is split into two parts:

the power consumption of the system is detailed, along with information on inrush current.

T  ias -CLE-STM32H7A3/7B3 lines and STM32H7B0 Value line devices:

• when using two power domains

• when minimizing power consumption while keeping some activities running when required (autonomous mode).

-UBR isted below.

STM32H7A3Zl_Mode1: temperature acquisition with CPU in CRun mode, CD in DRun mode and SRD in SRDRun mode   
STM32H7A3ZI_Mode: temperature acquisition with CPU in CSleep mode, CD in DRun mode and SRD n SRDRun mode   
ST32H7A3ZIMode3:temperature acquisition with CPU in CStop mode, CD in DStop mode and SRD in SRDRun mode   
STM32H7A3ZI_Mode4: temperature acquisition with CPU in CStop mode, CD in DStop2 mode and SRD in SRDRun   
mode   
ST32H7A3ZI_Mode5: temperature acquisition with CPU in CStop mode, CD in DStop mode, and SRD switching   
between Run and Stop modes   
ST32H7A3ZI_Mode6: temperature acquisition with CPU in CStop mode, CD in DStop2 mode, and SRD switching   
between Run and Stop modes

Thippl T32H7A3/7Bine nd 32BValue nder  2H7A/ ereo32ABn32BVaue evi  1R]

# 1 General information

This document applies to STM32H7A3/7B3 and STM32H7B0 Value line microcontrollers Arm® Cortex®-based devices.

# Note:

Arm is a registered trademark of Arm Limited (or its subsidiaries) in the US and/or elsewhere.

# List of acronyms

Table 1. List of acronyms   

<table><tr><td rowspan=1 colspan=1>Acronym</td><td rowspan=1 colspan=1>Description</td></tr><tr><td rowspan=1 colspan=1>eNVM</td><td rowspan=1 colspan=1>Embedded nonvolatile memories</td></tr><tr><td rowspan=1 colspan=1>LDO</td><td rowspan=1 colspan=1>Low-drop out voltage regulator</td></tr><tr><td rowspan=1 colspan=1>SMPS</td><td rowspan=1 colspan=1>Switch-mode power supply</td></tr><tr><td rowspan=1 colspan=1>HSLV</td><td rowspan=1 colspan=1>High-speed low voltage</td></tr><tr><td rowspan=1 colspan=1>WFI</td><td rowspan=1 colspan=1>Wait for interrupt</td></tr><tr><td rowspan=1 colspan=1>WFE</td><td rowspan=1 colspan=1>Wait for event</td></tr></table>

# Reference documents

Table 2. Reference documents   

<table><tr><td rowspan=1 colspan=1>Reference</td><td rowspan=1 colspan=1>Document title</td></tr><tr><td rowspan=1 colspan=1>[R1]</td><td rowspan=1 colspan=1>STM32H7A3/7B3 and STM32H7B0 Value line advanced Arm®-based 32-bit MCUs:reference manual (RM0455)(1)</td></tr><tr><td rowspan=1 colspan=1>[R2]</td><td rowspan=1 colspan=1>32-bit Arm® Cortex®-M7 280 MHz MCUs, up to 2-Mbyte Flash memory, 1.4-MbyteRAM, 46 com. and analog interfaces, SMPS: datasheet (DS13195)(1)</td></tr><tr><td rowspan=1 colspan=1>[R3]</td><td rowspan=1 colspan=1>32-bit Arm® Cortex®-M7 280 MHz MCUs, up to 2-Mbyte Flash memory, 1.4-MbyteRAM, 46 com. and analog interfaces, SMPS: datasheet (DS13195)(1) Refer tosection 6.3 Operating conditions. For mode 1 and 2 refer to table 35 and table 39,for mode 3, 4, 5 and 6 refer to table 38 and table 40.</td></tr></table>

1. Available at www.st.com.

# 2 System architecture

The advanced eNVM (embedded nonvolatile memories) technology and architecture used in STM32H7A/7Bx devics enable a frequencyf the core o 80 MHz. Themultiple power domains provide a smart solutin to power-consumption challenges.

The system is partitioned as follows:

One CPU subsystem Arm® Cortex®-M7 core, with associated peripheral clocks according to CPU activity.

D Two power domains:

CD domain: a high-bandwidth and high-performance domain with the Cortex®-M7 core and acceleration mechanisms. This domain encompasses high-bandwidth features and smart management thanks to the AXI and AHB bus matrices. It is also an l/O processing domain, that contains most peripherals and requires less bandwidth.

SRD domain: designed to manage the low-power mode feature. It embeds the system configuration block to keep the system state, and the GPiO status. This domain is designed to be autonomous. It embeds a 32-Kbyte RAM and a subset of peripherals to run basic functions. While the CD domain can be shut off to save power.

The figure below shows the system architecture of STM32H7A/7Bx microcontrollers.

![](images/63146f7121015c03e8b4d7bb45464585558e92d2b8b04b561baedb18bb39fac3.jpg)  
Figure 1. STM32H7A/7Bx system architecture

Bank 1 is limited to 128 Kbytes on STM32H7B0 devices. STM32H7A3xG and STM32H7A3xl/7B3xx devices feature two banks of 512 Kbytes and 1 Mbyte each, respectively. 2. OTFDEC1 and OTFDEC2 are available only on STM32H7B0 and STM32H7B3 devices.

# 3 System supply configurations

The VcoRE domain is supplied:

either by the internal linear voltage regulator either by the embedded SMPS step down converter or directly by an external supply voltage (regulator bypass).

T  ep ownconverter analso beascaded with he lnearvoltage egulato. ordevices, whicho support the SMPS feature, only the LDO regulator is available.

p l  g    nd arV domain is split as follows:

CD domain containing the CPU (Cortex®-M7), flash memory, memories interface, graphical, analog, and digital peripherals.   
SRD domain containing the system control, I/O logic and low-power peripherals. The different supply configurations are controlled through the SMPSLEVEL, SMPSEXTHP, SMPSEN, LDOEN and BYPASS bits in PWR control register 3 (PWR_CR3). The choice of the VcoRE domain supply can be done only once, before configuring the system clock source.   
For more details about the supply configuration control, refer to the power supplies section in [R1].

# 4 Voltage regulator (LDO) supply

The LDO ow-drop out voltage egulator) sules both powerdomains D and RD. CD can e  in low-power mindependentlyThevoltage egulator isalways enable afterrese. Forhe ystem supply configurati where the VcoRE is supplied by the LDO, the default output level is set to 1.0 V (VOS3).

For more accurate values on the voltage-scaling output, refer to [R2].

# 5 SMPS step-down converter supply

The embedded SMPS (switch-mode power supply) step down converter has a higher efficiency than the embedded LDO regulator. Using the SMPS, improves the overall system power consumption for ll power modes thas  edial exteal pen ucoran ocpacior. For ooation power efficiencies refer to [R1].

T  hupl pin. The regulated output at startup is 1.2 V.

# Note:

For more accurate values on the voltage-scaling output, refer to [R2].

# 6 SMPS and LDO regulators mode

The figure below gives an overview of all possible use cases of the regulator:

LDO power supply   
direct SMPS power supply   
LDO SMPS power supply   
LDO external SMPS power supply   
external SMPS power supply and bypass   
bypass

In STM32H7A3/7Bx microcontrollers, the software manages the regulator bypass through LDOEN, and BYPASS inhe RR egister.An exteral power supply delivrRhroh  .A sste start MCU starts under LDO. It then switches to the regulator-bypass mode to modify the LDOEN and BYPASS bits with the software.

The figure below illustrates the system supply configuration for STM32H7A7Bx microcontrollers. For more information on external capacitor values refer to [R2].

![](images/d2b8a6d9d474a9b9e40138b343157c0afdaea4826d4a283ec9507b75976636a4.jpg)  
Figure 2. System supply configuration

MSv48170V:

The STM32H7A3/7Bx microcontrollers embed an SMPS step-down converter and an LDO. There are several possible power-supply configurations to provide the digital power supply as follows:

the internal linear voltage regulator the embedded SMPS step down converter or directly an external supply voltage in regulator bypass mode.

The SMPS step-down converter can also be cascaded with the linear voltage regulator.

Note:

I an  eveahouu of the device.

F  ua v apossileaneegulator supply ir rovierougitoueicat packa.

# 7 Power control modes

There are two power control modes available, the operating mode and the low-power mode.

# 7.1

# Operating modes

Ttollowenoeoif sblockw.   
The system operating mode is driven by the CPU subsystem and the system SmartRun autonomous wake-up.   
The CPU subsystem includes multiple domains depending on its peripheral allocation.

The operating modes available on the different system blocks are detailed in Table 3.

Table 3. Subsystem operating mode   

<table><tr><td rowspan=1 colspan=1>CPU subsystem anddomains</td><td rowspan=1 colspan=1>Mode</td><td rowspan=1 colspan=1>Description</td></tr><tr><td rowspan=3 colspan=1>CPU subsystem</td><td rowspan=1 colspan=1>CRun</td><td rowspan=1 colspan=1>CPU and CPU subsystem peripherals allocated via PERxEN bits inthe RCC registers, are clocked.</td></tr><tr><td rowspan=1 colspan=1>CSleep</td><td rowspan=1 colspan=1>The CPU clock is stalled, and the CPU subsystem allocatedperipheral clock operates according to PERxLPEN bits in the RCCregisters.</td></tr><tr><td rowspan=1 colspan=1>CStop</td><td rowspan=1 colspan=1>CPU and CPU subsystem peripheral clocks are stalled. When theCPU subsystem is in CStop mode, the CPU domain is either inDStop or DStop2.</td></tr><tr><td rowspan=3 colspan=1>CPU domain</td><td rowspan=1 colspan=1>DRun</td><td rowspan=1 colspan=1>The domain bus matrix is clocked. The CPU subsystem operates inCRun or CSleep mode.</td></tr><tr><td rowspan=1 colspan=1>DStop</td><td rowspan=2 colspan=1>The domain bus-matrix clock is stalled. The CPU subsystemoperates in CStop mode and the RETDS_CD bit of PWR CPUcontrol register (PWR_CPUCR) selects the DStop or DStop2 mode.The SRD domain peripherals are able to operate in Stop modeotherwise no peripherals in the CPU domain are operational.</td></tr><tr><td rowspan=1 colspan=1>DStop2</td></tr><tr><td rowspan=3 colspan=1>SRD domain</td><td rowspan=1 colspan=1>Run</td><td rowspan=1 colspan=1>The system clock and the SmartRun domain-bus matrix clock arerunning.The CPU subsystem is in CRun or CSleep mode, orA wake-up signal is active (system SmartRun autonomousmode).Run mode is entered after a POR reset and a wake-up from standbymode. The system supply configuration must be programmed inPWR control register 3 PWR_CR3. The system enters Run modeonly when the ACTVOSRDY bit in PWR control status register 1PWR_CSR1 is set to 1.</td></tr><tr><td rowspan=1 colspan=1>Stop</td><td rowspan=1 colspan=1>The system clock and the SmartRun domain-bus matrix clock arestalled.(1)The CPU domain is in DStop or DStop2 modeThe CPU subsystem is in CStopAll wake-up signals are inactiveThe PDDS_SRD bit of PWR CPU control register(PWR_CPÜCR) selects the Stop mode</td></tr><tr><td rowspan=1 colspan=1>Standby</td><td rowspan=1 colspan=1>The system is powered down.The CPU domain and CPU subsystem are powered offThe wake-up pins and RTC can wake up from Standby mode</td></tr></table>

When the systemoscillator HSI or CSI is use HSIKERON and CSIKERON control the state, therwise the ystem oscillator is off.

# 7.2

# Low-power modes

Several low-power modes are available to save power when the CPU does not execute code. This is, for example, when waiting for an external event. The end user must select the mode that provides the best compromise between low power-consumption, short start-up-time, and available wake-up sources for the application.

The features of the low-power modes for STM32H7A3/7Bx microcontrollers are:

CSleep: CPU clock stopped CStop: CPU subsystem clock stopped DStop: domain bus-matrix clock stopped Stop: system clock stopped Standby: domain/system powered down e are several ways to reduce power consumption on STM32H7A3/7Bx microcontrollers:

Decreasing dynamic power consumption by slowing down the system clocks. This is done even in Run mode and by individually clock-gating peripherals not used.   
Saving power consumption when the CPU is idle, by selecting among the available low-power modes. This is made according to the requirements of the end-user application. This is the best compromise between short startup time, low-power consumption, and available wake-up sources.

The devices have several low-power modes:

System run with CSleep: CPU clock stopped   
Autonomous with CD domain in DStop: CPU and CPU domain bus-matrix clocks stopped   
Autonomous with CD domain in DStop2: CPU and CPU domain bus matrix clocks stopped, and CPU domain in retention mode   
System stop: SRD domain clocks stopped and CD domain in DStop that is CPU and CPU domain bus matrix clocks stopped   
System stop: SRD domain clocks stopped and CD domain in DStop2, that is CPU and CPU domain bus matrix clocks stopped, CPU domain in retention mode   
Standby: system, CD, and SRD domains powered down

CSleep and CStop low-power modes are entered by the MCU when executing the WFI (wait or interrupt) or WFE (wait for event) instructions. These modes are also entered by the MCU when SLEEPONEXIT bit of the Cr®   ugom  ert eriut.Te ents -powe (DStop or DStop2) when the processor, ts subsystem, and the peripherals allocated in the domain enter in low-power mode.

I  ow e at yst nt t mer Standby mode when all ET wakep sources a cleared and whenhe powerdomains are n Sto DStop2 mode.

Table 4. System and domains low-power mode   

<table><tr><td rowspan=1 colspan=1>System power mode</td><td rowspan=1 colspan=1>CD domain power mode</td><td rowspan=1 colspan=1>SRD domain power mode</td></tr><tr><td rowspan=1 colspan=1>Run</td><td rowspan=1 colspan=1>DRun/DStop/DStop2</td><td rowspan=1 colspan=1>DRun</td></tr><tr><td rowspan=1 colspan=1>Stop</td><td rowspan=1 colspan=1>DStop/DStop2</td><td rowspan=1 colspan=1>DStop</td></tr><tr><td rowspan=1 colspan=1>Standby</td><td rowspan=1 colspan=1>Standby</td><td rowspan=1 colspan=1>Standby</td></tr><tr><td rowspan=1 colspan=1>Autonomous</td><td rowspan=1 colspan=1>DStop/DStop2</td><td rowspan=1 colspan=1>SRDRun</td></tr></table>

# 8 DStop2

The DStop2 is a new mode in STM32H7A7Bx microcontrollers, where part of the CPU domain-digital circuitry siches of while thedata etention iskeptThis includes memory and register settings ee figure elow). Stomodeiiantproves lowpowerconsption  s egligiblewakecra.T content of all memories is retained in DStop2.

The main differences between DStop and DStop2 are given below:

In DStop mode, the entire logic is still supplied.   
In DStop2 mode, memories and registers are maintained, while asynchronous logic is switched off. This allows further leakage current reduction. When exiting DStop2, the CPU domain can resume normal execution.

Te te tateaiinStop nStop how hegur belowTe m mode (DStop) or deep-retention mode (DStop2).

![](images/ab04727ab0512e5f5e988faf1f1349bc07efd154fddb54f401eb20d8571ee53c.jpg)  
Figure 3. System supply

The CPU domain enters DStop or DStop2 depending on the configuration of RETDS_CD bit of PWR_CPUCR register.

Beforeentering DStop2,ll the peripherals that belong to the CPU domain and have a kernel clock must be:

either disabled by clearing the enable bit in the peripheral itself   
or reset by setting the corresponding bit in the associated AHB peripheral reset register (RCC_AHBxRSTR) or APB peripheral reset register (RCC_APBxRSTR).

Into mode alltheC doma clocks are ut dat isretaie The power consption n Stome can be furthe ptimized by choosing to shut ofsome SRAMs with the consequence to lose their content. The PWR block controls the VCORE supply according to the system operating mode (CRun, CSleep, or CStop). The PWR block also controls the power switch (ePODs) to set the CD domain in retention mode (DStop2). The CPU v register content is retained.The selection betwen DStopor DStop  made through theREDSCD bi f WR CPU control register PWRCPUCR. In DStop2 mode, the content of the memory block is maintained. Further tizatin  tai ihingeoyblostizatnpl the memory content. The end user can select which memory is discarded during Stop mode.

This is by means of xxSO bits in PWR control register 1 (PWR_CR1) as follows to keep the content of:

SmartRun domain AHB memory in DStop2 mode, SRDRAMSO bit must be set USB and FDCAN memories in DStop2 mode, HSITFSO bit must be set GFXMMU and GFXMMU memories in DStop2 mode, GFXSO bit must be set. ITCM and ETM memories in DStop2 mode, ITCMSO bit must be set AHB SRAM2 in DStop2 mode, AHBRAM2SO bit must be set AHB SRAM1 in DStop2 mode, AHBRAM1SO bit must be set AXI SRAM3 in DStop2 mode, AXIRAM3SO bit must be set AXI SRAM2 in DStop2 mode, AXIRAM2SO bit must be set AXI SRAM1 in DStop2 mode, AXIRAM1SO bit must be set

Be ntergto mode,he as eoymust e gur in -powermod y etngheL PWR_CR1. This results in a power consumption improved with a slightly longer wake-up time.

# Note:

It is mandatory to set FLPS before entering DStop2 mode.

The core domain cannot be switched to DStop2 when the embedded flash memory is busy: BSY1/2, QW1/2, WBNeus ol mode.

When entering DStop2 domain it generates a reset, the NRST_STOP bits of FLASH_OPTSR_CUR and FLASH_OPTSR_PRG registers are then set.

# 9 SRD autonomous mode

The autonomous mode permits basic operations with an inactive CPU domain in low-power modes, namely in SRD in Run mode.

The autonomous mode  entered when the SLEEPDEEP bit in the Cortex®-M system control register is et. The autonomous mode is exited by enabling an EXTl interrupt or event depending on how the low-power mode is etred. In autonomous mode, the system can wake up from Stop mode by enabling an XTI wake-p, without waking up the CPU subsystem.

Refer to Table 5 for more details for entering and exiting the autonomous mode.

Table 5. Autonomous mode   

<table><tr><td>Autonomous mode</td><td>Description</td></tr><tr><td rowspan="2">Mode entry</td><td>WFI or WFE when: SLEEPDEEP = 1 (refer to Cortex®-M system control register.) CPU NVIC interrupts and events cleared</td></tr><tr><td>On return from ISR when: SLEEPDEEP = 1 and SLEEPONEXIT = 1 (refer to Cortex®-M system control register.)</td></tr><tr><td>Mode exit</td><td>If WFI or return from ISR is used for entry: EXTI interrupt enabled in NVIC If WFE is used for entry and SEVONPEND = 0: EXTI event If WFE is used for entry and SEVONPEND = 1:</td></tr><tr><td>Wake-up latency</td><td>EXTI interrupt even when disabled in NVIC or EXTI event EXTI and RCC wake-up synchronization</td></tr></table>

Perherals locate heSmartRundomain e provied with heclocks thanks heautnous modv h according to the SmartRun domain state. When the CPU is in CStop mode and:

If the SmartRun domain is in DRun mode, peripherals with autonomous mode activated receive their peripheral clocks.

D If the SmartRun domain is in DStop mode, no peripheral clocks are provided.

Autonomous mode does not prevent the SmartRun domain to enter in DStop or DStop2 mode. Autonomous mallows he delivery f he periheal clocks to peripherals locate in heSRD doan,ve f theCPU is in CStop mode. When a peripheral is enabled and has its autonomous bit activated (PERxAMEN bit in the RCCSRDAMR register), this peripheral receives its clocks to the SRD domain state, if the CPU is in CStop mode.

In autonomous mode, thendividual peripheral clocks can remain active by settng the corresponding ERxAMEN bit of the RCC_SRDAMR register:

SRDSRAMAMEN bit, SRDSRAM bus clock is enabled when the SmartRun domain is in Run mode.   
BKPRAMAMEN bit, backup RAM clock enabling is controlled by the SmartRun domain state.   
DFSDM2AMEN bit, DFSDM2 peripheral clocks are enabled when the SmartRun domain is in Run mode.   
Kernel clock is enabled when the SmartRun domain is in Stop mode.   
DTSAMEN bit, digital temperature sensor DTS clocks are enabled when the SmartRun domain is in Run mode.   
RTCAMEN bit, RTC bus clocks are enabled when the SmartRun domain is in Run mode. VREFAMEN bit, VREF clocks are enabled when the SmartRun domain is in Run mode or Stop mode. COMP12AMEN bit, COMP1, and two peripheral clocks are enabled when the SmartRun domain is in Run mode.   
DAC2AMEN bit, DAC2 (containing one converter) peripheral clocks are enabled when the SmartRun domain is in Run mode.   
LPTIM3AMEN, LPTIM3 peripheral clocks are enabled when the SmartRun domain is in Run mode. Kernel clock is enabled when the SmartRun domain is in Stop mode.   
LPTIM2AMEN, LPTIM2 peripheral clocks are enabled when the SmartRun domain is in Run mode. Kernel clock is enabled when the SmartRun domain is in Stop mode.   
1C4AMEN bit, I2C4 peripheral clocks are enabled when the SmartRun domain is in Run mode. Kernel clock is enabled when the SmartRun domain is in Stop mode.   
SPIAMEN bit, SPl6 peripheral clocks are enabled when the SmartRun domain is in Run mode. The kernel clock is enabled when the SmartRun domain is in Stop mode.   
LPUART1AMEN bit, LPUART1 peripheral clocks are enabled when the SmartRun domain is in Run mode. Kernel clock is enabled when the SmartRun domain is in Stop mode.   
GPIOAMEN bit, GPIO peripheral clocks are enabled when the SmartRun domain is in Run.   
BDMA2AMEN bit, BDMA2 and DMAMUX2 peripheral clocks are enabled when the SmartRun domain is in Run.

The SmartRun domain can be kept in DRun mode while the CPU is in CStop mode and the CPU domain is in DSt or DStop2 mode.This is done by etting RUNSRD bit in PWRCPUCR register. I is worth to note that the CPU can control:

if the CPU domain is allowed entering DStop or DStop2 modes   
or the SmartRun domain is allowed entering in DStop when conditions are met, through bits RETDS_CD   
and PDDS_SRD of PWR control register (PWR_CPUCR)

Thehighped owoltatalowsheuut buftzation t owvoltge wi ustable When activated, HSLV mode enables a perorance close to 3.3 V at 1.8 V at the same frequency. To maxiize the performance, the l/O high-speed feature, HSLV, must be activated at low-device supply voltage.

For STM32H7A7Bx microcontrollers, HSLV must be activated when VD is lower than 2.7 V. HSLV must not be enabled when VDD is higher than 2.7 V, as this can damage the STM32 device.

Inorder o enable the HSLV mode, a speciic bytes option must be enable, and specfic bits in the SYSCFG register must be set. These are listed below:

Option bytes   
VDDIO_HSLV and VDDMMC_HSLV option bytes enable the configuration of pads below 2.7 V. This is respectively for VDDio and VDDMmc power rails if set to one.

• SYSCFG register

The speed of some l/Os can be increased at low voltage. This can be done by programming the corresponding HSLVx bits in the SYSCGF_CCCSR interfaces. This feature must be used only when the I/O power supply is below 2.7 V. The software writes the HSLVx bits to optimize the I/O speed when the product voltage is low.

HSLV3 indicates the high speed at low voltage for VDDMMc l/Os. It is active only when VDDMMC_HSLV user option bit is set. It mainly controls the speed of SDIO on VDDMMC power rail. HSLV2, HSLV1, and HSLV0 indicate the high speed at low voltage for VDD I/Os. They are active only when VDDIO_HSLV user option bit is set. They respectively control the speed of FMC, OCTOSPI, and SDMMC. When testing a bus at 1.8 V (SDMMC data bus), special care must be taken before activating HSLV mode. All /Os in the bus must support this mode. Otherwise, there is an unbalance in the timings.

# 11 Low-power application

This section provides information on smart power management of STM32H7A3/7B3 microcontrollers through an application example. It provides as well an example of SRD autonomous mode beneficial to power consumption.

# Low-power application example

This example is based on I2C transmission using the ST shield (X-NUCLEO-IKS01A2). The purpose of this example is to highlight the smart power management of STM32H7A3/7Bx microcontrollers when using two power domains.

The demo code is based on six modes:

Mo this mode is equivalent to legacy products that keepal domains active to transfer data.This is performed from the ST shield through I2C1 with the CPU in Run mode.   
Mothismode isequivalent to legacy products that keepal domains active to transfer dataThis is performed from the ST shield through I2C1 with the CPU in Sleep mode.   
Mode 3: in this mode, the power efficiency enhances keeping SRD in Run mode and CD in DStop. The datatransfe witched Cinsteadf Thishighlights therhitecture flexiblity move be peripheral instances. Namely, from CD to SRD without changing external connections.   
Mode 4: as mode 3 while the CD domain is in DStop2 for more power-energy saving. This mode shows the SRD autonomous Run mode.   
Mode 5: as mode 3 while the SRD domain switches between Run mode and Stop mode during transfer. This mode optimizes power consumption.   
Mode 6: as mode 4 while the SRD domain switches between Run mode and Stop mode during transfer. This mode optimizes power consumption   
The demo code uses the Nucleo board NUCLEO-H7A3ZI-Q and the X-NUCLEO-IKS01A2/A3 expansion board to get temperature values from the HTS221 sensor via the I2C bus.   
The figure below shows the connections between peripherals and memories.

![](images/66d558753969d8ca0822b9c87e557c4b9cf8e17c529dc4c85ca8c06e380d8f23.jpg)  
Figure 4. Peripherals and memories connections

# Mode 1

1. Temperature acquisition from shield to SRAM1 through I2C1 in the CD domain.   
2. Saving data from SRAM1 to BKPSRAM.

Table 6. Mode 1: operating mode and domains   

<table><tr><td>CD domain</td><td>SRD domain</td></tr><tr><td>DRun(CRUN)</td><td>SRDRun</td></tr></table>

# Mode 2

1. Temperature acquisition from shield to SRAM1 through I2C1 in the CD domain. The CPU is in Sleep mode.   
2. Saving data from SRAM1 to BKPSRAM after waking up the Cortex®-M7 core.

Table 7. Mode 2: operating mode and domains   

<table><tr><td>CD domain</td><td>SRD domain</td></tr><tr><td>DRun(CSleep)</td><td>SRDRun</td></tr></table>

# Mode 3

Temperature acquisition from shield to SRDSRAM through I2C4 in the SRD domain in autonomous mode.   
The CD domain is in DStop mode.

2. Saving data from SRDSRAM to BKPSRAM after waking up the Cortex®-M7 core.

Table 8. Mode 3: operating mode and domains   

<table><tr><td>CD domain</td><td>SRD domain</td></tr><tr><td>DStop(CStop)</td><td>SRDRun</td></tr></table>

# Mode 4

. Temperature acquisition from shield to SRDSRAM through I2C4 in the SRD domain in autonomous mode. The CD domain in DStop2 (retention) mode.

2. Saving data from SRDSRAM to BKPSRAM after waking up the Cortex®-M7 core.

Table 9. Mode 4: operating mode and domains   

<table><tr><td>CD domain</td><td>SRD domain</td></tr><tr><td>DStop2(CStop)</td><td>SRDRun</td></tr></table>

# Mode 5

Temperature acquisition from shield to SRDSRAM through I2C4 in SRD domain. In autonomous mode (SRDRun) with the CD domain in DStop mode.

2. System state in Stop mode (CD domain in DStop mode and SRD domain in SRDStop mode). Toggling of five times between state 1 and state 2.

3. Saving data from SRDSRAM to BKPSRAM after waking up the Cortex®-M7 core.

Table 10. Mode 5: operating mode and domains   

<table><tr><td>CD domain</td><td>SRD domain</td></tr><tr><td>DStop(CStop)</td><td>SRDRun/SRDStop</td></tr></table>

# Mode 6

1. Temperature acquisition from shield to SRDSRAM through I2C4 in SRD domain. In autonomous mode (SRDRun) with the CD domain in DStop2 mode (retention).   
2. System state in Stop mode (CD domain in DStop2 mode and SRD domains in SRDStop mode). Toggling of five times between state 1 and state 2.   
3. Saving data from SRDSRAM to BKPSRAM after waking up the Cortex®-M7 core.

Table 11. Mode 6: operating mode and domains   

<table><tr><td>CD domain</td><td>SRD domain</td></tr><tr><td>DStop2(CStop)</td><td>SRDRun/SRDStop</td></tr></table>

# 11.2

# Mode 6 - SRD autonomous mode

This section details the SRD autonomous mode with mode 6 example in Section 1.1 , and its power consumption benefits.

# 11.2.1 Memory retention

The SRD domain features a 32 kbytes of SRAM (SRDSRAM) to retain data while the CD is in DStop2 mode. This feature can be used in several use-cases:

To retain the application code in order to recover properly from DStop2 mode.   
To retain the data from or to a sensor when the CPU enters CStop. CD domain is in DStop2 between two consecutive operations.

In Figure 5, both SRDSRAM, and BKPSRAM are used, respectively to save the transmitted data from the temperature snsor when he system  inautonomous mode.The nal datas saveater waking up theCPU from CStop mode.

# 11.2.2 Example description

Figure 5 shows the proposed implementation of SRDSRAM to I2C4 using BDMA2. The timing diagram describes the different steps. The LTIM3 gives intervals each second The SRD domain wakes up from Stop mode and the SRD domain executes the following tasks in autonomous mode:

1. Transfer data from SRDSRAM to I2C 4 using BDMA2.   
2. When the 2C4 interface indicates that the last 2 bytes have been transferred from C4 to SRDSRAM, the SRD domain switches to Stop mode.

A henhe ast 0yBMAe Ah7 e  wak CPU from CStop mode. When theCPU is inCRun mode, it prepares data located into the SRDSRAM or process and transfer to the backup SRAM.

![](images/dc46fbdf86d3b0af8a9e6e602dbab8d26913e7e7d4e76820e4c6f6df4d5e59bc.jpg)  
Figure 5. SRDSRAM timing diagram to 12C 4 transfer with BDMA2

# Note:

To toggle the SRD domain between Stop mode and Run mode, the wake-up event (ptim3_out each second) must trigger Run mode. The SRD domain can clear this event with the dmamux2_evt7 signal and switch back the SRD domain to Stop mode.

# RCC programming

In this example, the CPU subsystem also includes the peripherals of the SRD domain that are used or data transfer. Namely, LPTIM3, BDMA2, DMAMUX2, SRDSRAM, I2C4, backup SRAM.

These peripherals must be programmed in autonomous mode to operate even when the CPU is in CStop mode. When STM32CubeFW_H7is used, the followingfunctions defined in thestm32h7xx_halrcc.h file permit the programming of peripherals in autonomous mode:

HAL_RCC_LPTIM3_CLKAM_ENABLE ();   
HAL_RCC_BDMA_CLKAM_ENABLE ();   
HAL RCC SRDSRAM CLKAM ENABLE HAL_RCC_I2C4_CLKAM_ENABLE ();   
HAL RCC BKPRAM CLKAM ENABLE ();

# PWR programming

In this mode, the PWR block must be programmed:

to prevent the system SRD domain enters in Standby mode, when the data transfer completes to allow CD domain to enter DStop2 mode to define the working voltage according to the system modes (SvOS3).

# EXTI programming

The Iptim3_out signal is used to wake up the SRD domain from Stop mode:

When LPTIM3 time intervals have elapsed at each second, the Iptim3_out signal is connected to the EXTI input event, line number 51.   
When selecting BDMA2_ch7 as pendclear source of SRD domain, the SRD domain switches back to Stop mode.   
When using STM32Cube_FW_H7 function:   
HAL_EXTI_SRD_EventInputConfig(EXTI_LINE51,ENABLE,BDMA_CH7_CLEAR); definedinstm3 2h7xx_ha1. it selects Iptim3_out signal as wake-up source and dmamux2_evt7 as pendclear source:

# BDMA2 and DMAMUX2 programming

To execute the data transfers between BKPSRAM and 12C4 they must be four BDMA channels.

BDMA_channel0 (BDMA_ch0) transfers data from BKPSRAM to the I2C4_CR2 register, to configure the 12C4 interface to request write transfer to HTS221sensor.

BDMA_ch0 uses Req_Gen0 to generate BDMA requests. The rising edge of the Iptim3_out signal. tiggers the generation of BDMA requests. LPTIM3 generates the signal each second.

BDMA_channel1 (BDMA_ch1) transfers data from BKPSRAM to I2C4_TXDR register to send a specified address to the HTS221 sensor. BDMA_ch1 request is generated when I2C4 TX-FIFO enables TXDMAEN bit in I2C4_CR1 register. The DMAMUX SYNC1 block is programmed to generate a pulse on its dmamux2_evt1 output when the BDMA request is complete.

BDMA_channel2 (BDMA_ch2) transfers data from BKPSRAM to I2C4_CR2 register, to configure the I2C interface. This allows to request read transfer from the HTS221 sensor.

BDMA_ch2 uses Req_Gen2 to generate BDMA requests. The falling edge of dmamux2_evt1 triggers the generation of BDMA requests.

BDMA_channel7 (BDMA_ch7) transfers the received data from I2C4_RXDR register. Data from the HTS221 sensor to BKPSRAM. BDMA_ch7 transmission is enabled by setting RXDMAEN bit. BDMA_ch7 iscnfigured to generate interrupts to wake up the U from CStop mode.The interrupts are generated timeaaltransercopletes.Teransecopletest bye atrull tran 20 bytes of data.

The DMAMUx2 SYNC7 block is programmed to generate a pulse on its dmamux2_evt7 output when the BDMA2 reqest is complete. The dmamux2evt signal is used by the EXTI to switch back the SRD domain to Stop mode.

The figure below shows the active signal paths via DMAMUX2.

![](images/1cb0a0b6eb33e97889cea58087824528d356ee98cbeb169895187767fd6712b7.jpg)  
Figure 6. BDMA2 and DMAMUX2 interconnection

dmamux2_req_inx: DMAMUX DMA request line inputs (from peripherals or from dmamux_req_genx) dmamux2_req_outx: DMAMUX requests outputs (to DMA controllers) dmamux2_evtx: DMAMUX events outputs dmamux2_trgx: DMAMUX DMA request triggers inputs (to request generator sub-block)

# LPTIM3 programming

LPTIM3 operates when the SRD domain enters Stop mode and uses ck_Isi clock. LPTIM3 wakes up the SRD domain from Stop mode each second and to start BDMA2_ch0 transfer through Req_Gen0.

# I2C programming

|2C4 is configured to use k_hsi as the kernel clock to generate BDMA2 request when TX-FIFO/RX-FIFO is empt or fulAdedicated function calledI24ENABLEDMAREQUESTisdefined inthe common. file to enable BDMA2 requests generation by the 12C4.

# 11.2.3

# Mode 6 example - general description

The steps below details Figure 5:

Step 1. The Iptim3_out signal wakes up the SRD domain from Stop mode each one second.

tep 2. When the SRD domain wakes up from Stop mode, the rising edge of Iptim3_out signal triggers BDMA2_ch0 to begin data transfer (TRNSF1).

As soon as I2C4 TX-FIFO is empty, BDMA_ch1 begins the data transfer from BKPSRAM to I2C4_TXDR register (TRNSF2).

The end of this transfer triggers BDMA2_ch2 transfer (through dmamux2_ch1_evt) from BKPSRAM to I2C_CR2 register (TRNSF3).

5. As soon as I2C4 RX-FIFO is full, BDMA2_ch7 transfers 2 bytes of data from I2C4_RXDR register to BKPSRAM (TRNSF4).

i. The end of this transfer triggers a dmamux2_evt7 signal which is used to clear the SRD_PendClear bit.

Step 7. The whole system returns to Stop mode.

After five seconds and when the expected amount of data has been transmitted (NDT bits of BDMA_CNDTR0 set to 10 indicating half-transfer is complete), the BDMA_ch7 generates an interrupt to wake up the CPU from CStop mode.

S 9.The CPU processes the data located in BKPSRAM for transfer, copy it to BackupSRAM (CPUTRSF). The data stored in BackupSRAM is retained while the system is in Stop mode.

Step 10. The CPU returns to CStop mode and the whole system return to Stop mode. LPTIM3 continues to wake up the SRD domain after each one second, and BDMA2 channels continue to do all transfers as mentioned above. When the expected amount of data has been transmitted (NDT bits of BDMA_CNDTR0 set to 20 indicating that the transfer is complete), the BDMA2_ch7 generates an interrupt to wake up the CPU from CStop mode. The CPU processes the data located in SRDSRAM for transfer and copies it to BackupSRAM. (CPU_TRSF).

# 11.3 How to use the application

The hardware requirements and set-up of the application are listed below.

NUCLEO-H7A3ZI-Q board   
X-NUCLEO-IKS01A2 expansion board to measure temperature values from HTS221 sensor via I2C bus   
The X-NUCLEO-IKS01A2 expansion board must be plugged on the matching pins of the STM32   
Nucleo boards connector: Cec hebard  cmpur hroug -LINK wi minUSBorprogramig andeu   
A PowerShield to measure the current consumption

# 11.3.1

# Application example

Follow these steps to perform correctly the example.

1. Connect the NUCLEO-H7A3ZI-Q board to a computer trough ST-LINK with a mini-USB r programming and debugging.   
2. X-CUBE-PWRMGT-H7.   
3. Compile the project with the selected mode, and download it to the MCU.

![](images/839435f45bfc813406599e64e8db19234a8b7d884dbd98d706a5ea02b56c4949.jpg)  
Figure 7. How to select the different modes

4Plug in the shield X-NUCLEO-IKS01A2/A3 to the matching pins of the STM32H7A3ZI-Q board.

![](images/ff95761c2d6eac00c8010bf3fd2a769bf78d5f8367cd038286b01d7691c21ba5.jpg)  
Figure 8. X-NUCLEO-IKS01A2/A3 connection

5. Remove the jumper 4 (JP4) and connec instea an ampee meter  measure he current consmption. It is also possible to use the PowerShield X-NUCLEO-LPM01A (see Figure 9).

If the PowerShield is used:

a. Remove the IDD jumper JP4 in the NUCLEO-H7A3ZI-Q board.   
b. Connect the PowerShield on the X-NUCLEO-IKS01A2/A3.   
C. Reset the PowerShield X-NUCLEO-LPM01A.

For more details, follow the instructions on how to use the Cube monitor. See STM32CubeMonitor-Power software tool for power and ultra-low-power measurements (Um2202). It is also possible to use only the LCD screen on the board.

![](images/3d3bbceb310cd5caf4e44f19529b9e5c927221409a0a0163b43b184aca86ef16.jpg)  
Figure 9. PowerShield connection   
Figure 10 illustrates the PowerShield connection as follows:

S1 and S2 must be in ST position Jumper position:

o JP4 = on   
o JP1: for measurements, the jumper must be always in the normal position   
o JP9 = on   
o JP10 = off   
JP3: the jumper must be inserted in the USBposition   
S3 in flash memory position

![](images/15faa3ee0a425e24802f450bd74df59e979277530792e8b77800422d719a8cd2.jpg)  
Figure 10. PowerShield top view

To setup Tera Term, see Figure 11:

6. Open the terminal to see the output messages (Tera Term for example) with the setup

a. Open the terminal and select the serial protocol.   
b. Select Setup then Serial port. i. The last step is to set up the communication port configuration. This is illustrated with the green frame.   
C. Follow the steps as illustrated with the red frames for the correct functioning of the terminal.

Note: Note:

7. Press the reset button of the NUCLEO-H7A3ZI-Q board, the program starts the execution. Select and recompile the project for the other modes. Connect the PowerShield X-NUCLEO-LPM01A to a computer through the mini-USB cable to power it up.

![](images/4fcda29648c110a753aa989ca1392febeed751ec27c98232abef7d543691c351.jpg)  
Figure 11. Tera Term setup

# 11.3.2

# Results comparison

To compare the obtained results, refer to [R3]. When the system is in Stop mode, al the peripherals bus ineac clocks reHowever, perpheralstheSmartRudoainhavin kere clock requst active by programming their PERxAMEN bit (RCC_SRDAMEN).

In proviexamplehe case r eTu aditnally  he power consupti mde, the LTIM3 power consuption must be considered. Refer to LTIM3 kernel in table eripheral current consumption in Run mode from [R3].

# Revision history

Table 12. Document revision history   

<table><tr><td>Date</td><td>Version</td><td>Changes</td></tr><tr><td>27-May-2022</td><td>1</td><td>Initial release.</td></tr></table>

# Contents

# 1 General information 2

2 System architecture 3

3 System supply configurations 4

Voltage regulator (LDO) supply 5

SMPS step-down converter supply. 6

SMPS and LDO regulators mode

# Power control modes 10

7.1 Operating modes.. 10   
7.2 Low-power modes. 11

# DStop2 12

SRD autonomous mode. 14

HSLV 16

# Low-power application. 17

11.1 Low-power application example 17

1.2 Mode 6 - SRD autonomous mode. 19

11.2.1 Memory retention 19   
11.2.2 Example description 19   
11.2.3 Mode 6 example - general description. 22

# 11.3 How to use the application. 22

11.3.1 Application example 23   
11.3.2 Results comparison. 27

# Revision history 28

# List of tables 30

_ist of figures. . .31

# List of tables

Table 1. List of acronyms 2   
Table 2. Reference documents 2   
Table 3. Subsystem operating mode 10   
Table 4. System and domains low-power mode 11   
Table 5. Autonomous mode. 14   
Table 6. Mode 1: operating mode and domains 18   
Table 7. Mode 2: operating mode and domains 18   
Table 8. Mode 3: operating mode and domains 18   
Table 9. Mode 4: operating mode and domains 18   
Table 10. Mode 5: operating mode and domains 18   
Table 11. Mode 6: operating mode and domains 19   
Table 12. Document revision history . 28

# List of figures

Figure 1. STM32H7A/7Bx system architecture 3   
Figure 2. System supply configuration. 8   
Figure 3. System supply 12   
Figure 4. Peripherals and memories connections 17   
Figure 5. SRDSRAM timing diagram to I2C 4 transfer with BDMA2 20   
Figure 6. BDMA2 and DMAMUX2 interconnection 21   
Figure 7. How to select the different modes 23   
Figure 8. X-NUCLEO-IKS01A2/A3 connection 24   
Figure 9. PowerShield connection 25   
Figure 10. PowerShield top view 26   
Figure 11. Tera Term setup 27

# IMPORTANT NOTICE  READ CAREFULLY

pt old ursant  dits   leole.

purchasers' products.

No license, express or implied, to any intellectual property right is granted by ST herein.

re the property of their respective owners.