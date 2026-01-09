# Low-power timer (LPTIM) applicative use cases on STM32 MCUs and MPUs

# Introduction

STM32 microcontrollers (MCUs) and microprocessors (MPUs) listed in the table below.

This document contains some applicative examples provided with:

the X-CUBE-LPTIMER Expansion Package which includes: asynchronous pulse counter in Stop mode PWM (pulse-width modulation) generation in Stop mode timeout wakeup mode   
the STM32CubeU5 MCU Package firmware for STM32U5 Series which includes: PWM generation in Stop mode with LPBAM (low-power background autonomous mode) input capture in Stop mode with Autonomous mode

T general-purpose timer.

Table 1. Applicable products   

<table><tr><td>Type</td><td>Series and product lines</td></tr><tr><td rowspan="2">Microcontrollers</td><td>STM32F410 and STM32F413/423 product lines</td></tr><tr><td>STM32F7 Series, STM32G0 Series, STM32G4 Series, STM32H7 Series, STM32L0 Series, STM32L4 Series, STM32L4+ Series, STM32L5 Series, STM32U5 Series, STM32WB Series, STM32WL Series</td></tr><tr><td>Microprocessors</td><td>STM32MP1 Series</td></tr></table>

# 1 General information

# Note:

This document applies to STM32 MCUs and MPUs based on the Arm® Cortex®-M processor.   
Arm is a registered trademark of Arm Limited (or its subsidiaries) in the US and/or elsewhere.

# arm

# 2 Overview

La tizihe onsn durg both n-ime nd -iTe ow-poweimr )hels ue the power consumption specifically while the system is in low-power mode.

The T32 LMalows he sstem o peorm simple tasks while he powe consptionis kept t an solute minimum. The LPTIM main features are listed below:

a 1-bit auto-reload register to set the period, a 16-bit compare register to set the duty-cycle for a PWM   
waveform signal output on the timer   
a repetition counter that allows the adjustment of the counter roll-over   
channels that can be functional both as an input or output   
Input-capture mode   
capabilitygeneratA equests reriveheput-capturcountervaluesan erogram par   
the LPTiMER without the intervention of the CPU   
ability to remain fully functional in Stop mode thanks to the Autonomous mode

The LTIM can be used or timing and foroutput generation while the TM32 device is in low-power mode. he L wivu ha Standby and Shutdown modes.

Ta  eicoc e  an  ut  w t src.he  can also wakeup the system from low-powermodes, and realize meout function" wit extremely-low power consumption.

The LPTIM provides the basi functions of the TM32 general-purpose timers with the advantage  avery-low power consumption. Additionally, when configured in Asynchronous counting mode, the LTIM keeps running even when no internal clock source is active.

The LPTIM remains active both in Sleep and Stop modes, and can wake up the STM32 device from these modes Conversely, in Standby or Shutdown mode, the LPTIM is powered down and must be completely reinitialized when the STM32 device exits any of these modes.

The tables below details the main features of the various LPTIM types and the peripheral implementation on STM32 devices.

Table 2. Features on various LPTIM types   

<table><tr><td rowspan=2 colspan=1>Features</td><td rowspan=1 colspan=3>LPTIM</td></tr><tr><td rowspan=1 colspan=1>Type 1</td><td rowspan=1 colspan=1>Type 2</td><td rowspan=1 colspan=1>Type 3</td></tr><tr><td rowspan=1 colspan=1>Auto-reload register</td><td rowspan=1 colspan=1>X</td><td rowspan=1 colspan=1>X</td><td rowspan=1 colspan=1>X</td></tr><tr><td rowspan=1 colspan=1>Compare register</td><td rowspan=1 colspan=1>X</td><td rowspan=1 colspan=1>X</td><td rowspan=1 colspan=1>X</td></tr><tr><td rowspan=1 colspan=1>Repetition counter</td><td rowspan=1 colspan=1></td><td rowspan=1 colspan=1>X</td><td rowspan=1 colspan=1>X</td></tr><tr><td rowspan=1 colspan=1>Input/output channels</td><td rowspan=1 colspan=1></td><td rowspan=1 colspan=1>-</td><td rowspan=1 colspan=1>X</td></tr><tr><td rowspan=1 colspan=1>Input-capture mode</td><td rowspan=1 colspan=1></td><td rowspan=1 colspan=1></td><td rowspan=1 colspan=1>×</td></tr><tr><td rowspan=1 colspan=1>DMA requests</td><td rowspan=1 colspan=1></td><td rowspan=1 colspan=1></td><td rowspan=1 colspan=1>X</td></tr></table>

Table 3. LPTIM types on STM32 devices   

<table><tr><td>LPTIM type</td><td>STM32 devices(1)</td></tr><tr><td>Type 1</td><td>STM32F410 and STM32F413/423 product lines STM32F7 Series, STM32G0 Series, STM32G4 Series, STM32H7 Series, STM32L0 Series, STM32L4 Series(2) STM32L4R/4Sxx devices</td></tr><tr><td>Type 2</td><td>STM32MP1 Series, STM32WB Series STM32L41/42xx devices, STM32L4P5/4Q5xx devices STM32L5 Series, STM32WL Series</td></tr><tr><td>Type 3</td><td>STM32U5 Series</td></tr></table>

1.All features are not activated on all instances of a given product. 2 Except STM32L41/42xx devices.

The LI presents up 6 external triger ours wih a conigurable polariy.Te external ieru e igi f anceut possible ultgr oieatinvents.e configured to run:

in Continuous mode that is used to generate PWM waveforms in One-shot mode that is used to generate pulse waveforms

Te LM atures cormodehincion ablese M teace witicental qua oseu Input plopu tgl

The LPTIM can output dfferent waveform types even when the STM32 device is in specific low-power modes whereas almost al internal clock sources are turned off. LPTIM_CMP (or LPTIM_CCRx for LPTiM type 3) and LPTIMARR registers, in conjunction with the WAVE bitfield in LPTIM_CFGR and SNGSTRT in LPTIM_CR, are used to control the output waveform.

The output waveform can be a typical PWM signal with its period and duty-cycle controlled by LPTIMARR and LTIM_CMP or LTIMCCR) rgisr respetivly,  he ut waveor can e  sigle pulse with he ast output state defined by the configured waveform.

If the output waveforms are not equal, the SetOnce mode is configured. The polarity of the LPTIM output is controled through the WAVPOL bitield in LPTIM_CFGR for LPTIM type 1, and through CCxP field in LPTIM_CCMRx for LPTIM type 3.

# 3 LPTIM versus general-purpose timer

The main LPTIM advantages compared to any other timer available in the STM32 MCUs are:

The LPTIM can be fully functional in Stop mode thanks to the Autonomous mode and LPDMA.   
The LPTIM generates events to wake up the device from Stop mode.

AalmMctivRuehilozSo:both nn  ho

Depending on the selected clock source, the power consumption can be substantially lowered with LPTIM copare o a general-purpose timer.he table below details heiference between and T perieals during different power modes.

Table 4. TIM versus LPTIM in working modes   

<table><tr><td rowspan=1 colspan=1>Peripheral</td><td rowspan=1 colspan=1>Run</td><td rowspan=1 colspan=1>Low-power run</td><td rowspan=1 colspan=1>Low-power Sleep</td><td rowspan=1 colspan=1>Stop</td></tr><tr><td rowspan=1 colspan=1>TIM</td><td rowspan=1 colspan=1>X</td><td rowspan=1 colspan=1>X</td><td rowspan=1 colspan=1></td><td rowspan=1 colspan=1></td></tr><tr><td rowspan=1 colspan=1>LPTIM</td><td rowspan=1 colspan=1>X</td><td rowspan=1 colspan=1>X</td><td rowspan=1 colspan=1>X</td><td rowspan=1 colspan=1>X</td></tr></table>

# 4 LPTIM clock sources

The LPTIM is a peripheral with two clock domains:

APB (advanced peripheral bus) clock domain: contains the APB interface and the core functions of the peripheral such as the registers and signals connected to the CPU (typically the interrupt request) kernel clock domain:can be clocked by the APB clock source or by other internal clock sources including the LSE, LS, MSIK and HSI sources. It can also be clocked from an external clock source through the input (Input1) of the timer.

The LPTIM main feature is tabiliy o keepning in ow-power modes whealmost all clock sours turned off. The LPTIM also includes a very flexible clocking scheme enabling the features below:

The LPTIM can be clocked from on-chip clock sources such as LSE, LSI, HSI, MSIK or APB clocks (refer to the product reference manual for more details).

The LPTIM can be clocked from an external clock source through the Input1

Te eiblecloci he   uil ul-cuntr"pliatins. I sa keycion applications such as gas-metes.The table below umarizeshe  clock sources different powerms.

Table 5. LPTIM clock source on different power mode   

<table><tr><td rowspan=1 colspan=1>Mode</td><td rowspan=1 colspan=1>HSI</td><td rowspan=1 colspan=1>LSI</td><td rowspan=1 colspan=1>LSE</td><td rowspan=1 colspan=1>MSIK(1)</td><td rowspan=1 colspan=1>PCLK</td><td rowspan=1 colspan=1>External clock</td></tr><tr><td rowspan=1 colspan=1>Run</td><td rowspan=1 colspan=1>X</td><td rowspan=1 colspan=1>X</td><td rowspan=1 colspan=1>X</td><td rowspan=1 colspan=1>X</td><td rowspan=1 colspan=1>X</td><td rowspan=1 colspan=1>X</td></tr><tr><td rowspan=1 colspan=1>Sleep</td><td rowspan=1 colspan=1>X</td><td rowspan=1 colspan=1>X</td><td rowspan=1 colspan=1>X</td><td rowspan=1 colspan=1>X</td><td rowspan=1 colspan=1>X</td><td rowspan=1 colspan=1>X</td></tr><tr><td rowspan=1 colspan=1>Stop</td><td rowspan=1 colspan=1>-</td><td rowspan=1 colspan=1>X</td><td rowspan=1 colspan=1>X</td><td rowspan=1 colspan=1>-</td><td rowspan=1 colspan=1>X(2)</td><td rowspan=1 colspan=1>X</td></tr></table>

1Only available on STM32U5 devices. Only for STM32U5 devices: PCLK can be activated in Autonomous mode.

# 5 Synchronization block

The STM32 LPTIM can be configured in two modes:

D Asynchronous mode: the LPTIM is not clocked by an internal clock signal.

The LPTIM can operate with any external clock (below 15 MHz), while the STM32 device system clock is stopped.

Synchronous mode: the LPTIM is clocked by an internal clock signal.

The external signal is synchronized with a clock signal dfferent from the one used by the LM periheal.

The synchronization circuit used to synchronize the external signals is connected to the LPTM inputs. This circuit is mainly composed of cascaded D flip-flops that are clocked by the LPTIM core clock signal. This synchronization circuit introduces a delay of at least two LTiM core clock cycles. For this reason, the internal clock signal frequency must be at least two timeshigher than the external clock signal frequency.

In tecaseat bot egeoigur hectvnehteal cloc snal qu a least fourtimeshigher thanheextenal clock signal fequencyThis delay  two countrclocks s l needed after enabling the LPTIM and before the LPTIM starts counting.

# 6 Use cases

# 6.1

# Asynchronous pulse counter in Stop 2 mode

This application example is provided in the X-CUBE-LPTIMER, with a STM32L476RG device.

The pulse counting method for flowmeasurement consists of converting the kinetic energy from rotatin int g  i o rotation, the higher the number of pulses, varying in accordance with the measured flow.

In typical applications, heT32 devi counts henumber pulses, ut it does not want tbe wake up omo vey pul. I u cs,e cur  pulti y eu Asyronous mode anisclocked byhe pulss, whic oot have  rguar pacThe ollwiggureows the input signal and the corresponding counter value.

![](images/975a355e336f36329dda9dca1f2356852b83879ecf033b5c9505caf590579266.jpg)  
Figure 1. Input signal and corresponding counter value

A flow meter can be divided in three parts:

a transducer that converts the physical quantity to measure into electrical signal   
a data treatment logic that counts and stores   
a display that shows the accumulated count

Thplat cunt e uls ig   puouranplhem tial us comunication UART. The used parameters are the pulse counter that s basedon he LM in Asynchroous m and the MCU that s in Stop 2 mode.These parameters have been chosen to show the LTIM features in low-power mode. The UART is clocked by the LSE to guarantee a low power consumption.

The tranision  e pul counted byhe UART is perormein he nterrupt ervi outi SR) e push-button interrupt. The figure below describes the synoptic of the pulse counter.

![](images/9a67d457fe7171d04b2814dbf9655a5b36a3c42708affe0851e2cca807fe47c4.jpg)  
Figure 2. Pulse-counter architecture example

The hardware environment used for this example development is the NUCLEO-L476RG.

To establish the serial communication, the STM32 Nucleo-64 board already embeds the ST-LINK debug and probea atu iARacARaplea t il  portepts ualy requires a Mini-B USB cable for data transmission.

A COM port monitor software application on the PC can be used: to display the messages coming from the device via the serial link to be able to send data via the serial link to the device

![](images/34534f2bf87953ec418f0bbaa35cccf22aa1a18e8c3f8410cc70e413f1112b6d.jpg)  
Figure 3. STMicroelectronics Virtual COM port device manager

In Asynchronous mode, the external pulses injected on the LPTIM external Input1 are also used to clock the supported in Asynchronous mode).

![](images/d0c0a7b130befcbf27d3caf12d30ed1f83b9b934642c4fc41d2a1b19fdee3d1a.jpg)  
Figure 4. Asynchronous pulse-counter increment

To apply this configuration:

Set the control bit CKSEL in the LPTIM_CFGR register. Use CKPOL bits to configure the active edges. The following figure shows the block diagram for the asynchronous pulse counter.

![](images/cb8e485a88582d76d0aa8d78a32f26562d03ae81b4a9f6a54f7133e0569401e9.jpg)  
Figure 5. Pulse-counter block diagram

# Firmware description

System clock:

System clock: HSI LPTIM1 source clock: external signal UART2 source clock: LSE

• LPTIM1:

Source clock: external source (LPTIM1_input1)   
Prescaler = 1   
Clock polarity: rising edge   
Trigger source: software

• UART2:

Source clock: LSE   
Baudrate = 1200   
Stop bits = 1   
Parity: none   
Mode: Tx   
Hardware flow control: none

# 6.2

# PWM generation in Stop 2 mode

This PMW generation is done in a different way depending on the software used:

• Legacy mechanism (example available in X-CUBE-LPTIMER • LPBAM mechanism (example available in STM32CubeU5 firmware)

![](images/9b2868597e8a041eb7b62965df269ff4f210488d8225b9f100c14b8e842fa757.jpg)  
Figure 6. PWM generation in Stop mode with legacy mechanism

![](images/2c5c9f8e55c56ba0e0e7a73b0d9263cb946c7a5fe1c64e5db373fbf0cae330db.jpg)  
Figure 7. PWM generation in Stop mode with LPBAM mechanism

emai vanebil ork tmo whe sl several different waveforms.

Thanks to the PWM in Stop 2 mode, a signal can be generated:

with a frequency determined by the value of LPTIM_ARR with a duty cycle determined by the value of LPTIM_CMP (or LPTIM_CCRx)

Ther are two ways to update the values of LPTIM_ARR and LPTIM_CMP (or LPTIM_CCRx) that are controlled by the PRELOAD bit in LPTIM_CFGR:

PRELOAD = 0: LPTIM_ARR and LPTIM_CMP (or LPTIM_CCRx) are updated immediately after the write access.   
Tory: the waveform at the LPTIM output is directly impacted by the selected PRELOAD mode.   
PRELOAD = 1: LPTIM_ARR and LPTIM_CMP (or LPTIM_CCRx) are updated at the end of the running period of the timer.

Tewris he gisermust eone beoeast cock  per the update is postponed to the next period.

The LPTIM output depends on the continuous comparison between the LPTIM counter and the LPTIM_CMP (or LPTIM_CCRx) values. Writing directly to the channel register in the middle of a PWM period may generate spurious waveforms.The synchronization of the LTIM clock source with the APB clock domain creates some latency after the write access in LPTIM_CMP (or LPTIM_CCRx).

Any writeacces during this latency perid must beavoided becauset leads opreictable results. Thi latency is he delay betwee a write in neof the registers (LPTIMARRor LPTIMCMP/CCRx), and thesetti of the corresponding flag (ARROK or CMPOK).

The ncratn time he LIco coc with heBcock s par heeayTe eayc 2 × APB_CLK + 3 × LPTIM_CLK, with LPTIM_CLK being the kernel clock of the LPTIM.

The user must then ad 2 × APBCLK to set the ARROK flag to 1, knowing that this writeaccess must beade after the LPTIM enabling.

The change in LPTIM_ARR or LPTIM_CMP (or LPTIM_CCRx) is applied only when their flag is set to inform the application that the APB bus operation has been successfully completed. When ARROK or CMPOK is set, aiterrpt enerate e evic without ayneer polng heckhe pletionhe operation.

Example:

system clock = 180 MHz and LPTIM_CLK = LSI = 32 kHz system cycle = 5.55 ns and LPTIM_CLK cycle = 31.25 µs

The delay is then given by 2 × APB_CLK + 3 × LPTIM_CLK + 2 × APB_CLK = 2 × 5.55 ns + 3 × 31.25 µs + 2 × 5.55 ns = 93.77 µs = 16 896 system cycles

If thee ARROK and CMPOK flags do not exist, the application wastes 16 896 cycles to test the update  the register status.

The figure below summarizes the preload mechanism for the LPTIM_ARR register.

![](images/139ea128fb446d0cb79c7660e23613c613c7cee0a81269d70f1b89d0086332e9.jpg)  
Figure 8. Counter timing diagram with and without update immediately

# 6.2.1 Tasks with legacy mechanism

In aple e  ele becau valabl  omT eT heo source clock is the LSI. The PWM output waveform is configured through:

the WAVE bit reset to 0   
the CNTSTRT bit set to 1   
the WAVEPOL bit that controls the output polarity

The LPTIM1 is started after the detection of an active edge on the LPTIM_ETR pin.

Bee the device enters the low-powermode, he LT1 must be configured by loading the period and pulse values to the LPTIM_ARR and LPTIM_CMP (or LPTIM_CCR1) registers, and then by enabling the LPTIM1. To start the LPTIM1, a pulse must be applied on the LPTIM_ETR even if the device is in Stop mode.

The architecture of this example is described in the following figure.

![](images/d5e4b4b0b33a0be7573307a10edb5bc4c029419f73bc6f896d711aab7d6c5758.jpg)  
Figure 9. Architecture example of PWM generator in Stop 2 mode with legacy mechanism

# Firmware description

System clock: system clock: MSI LPTIM1 source clock: LSI • LPTIM1: source clock: internal source (LSI) prescaler = 1 trigger source: LPTIM_ETR pin trigger polarity: rising edge output polarity: high

# Tasks with LPBAM mechanism

The LPTIM1 is started after a software trigger. This example is based on a STM32U585 devic The following actions are needed before the device enters the low-power mode:

Configure the LPTIM1 by loading the period and pulse values to the LPTIM_ARR and LPTIM_CRR1 registers.   
Set the DMA information (such as instance and queue type).   
Configure the LPTIM1 to start in Continuous mode.   
Build the LPTIM1 start full DMA linked-list queue:

Configure the LPTIM1 enable node:

o Set the LPTIM1 instance and channel.   
o Set the node descriptor.   
o Set the LPTIM1 configuration.   
o Fill the node configuration.   
o Build the stop node.   
o Insert the node to the LPTIM1 queue.   
o Update register and node indexes. Configure the LPTIM1 wakeup interrupt node.   
Configure the LPTIM1 configuration node. Set PWM parameter to be changed.   
Set PWM configuration X.

The application calls ADV_LPBAM_LPTIM_PWM_SetFull () to update period, pulse and repetition values.A linked-ist queue is created and placed in the SRAM that is executed by a DMA channel in Stop 2 mode. This qu ontai oguraon ode  ueac time dat ven i rat su transfer in DMA mode:

• Build the LPTIM1 PWM full DMA linked-list queue:

Set the LPTIM1 instance and channel.   
Set the node descriptor.   
Set the LPTIM1 configuration.   
Configure the LPTIM1 period node.   
Configure the LPTIM1 pulse node.   
Configure the LPTIM1 repetition node.   
Configure the LPTIM1 clear flag node. Set the Circular mode.   
Configure the DMA linked list.   
Start the LPTIM1 PWM generation.   
Enter the whole system to Stop 2 mode.

The architecture of this example is described in the figure below.

![](images/a535d193f3c389db9e630ae36d8aa2fdd0bfc7a5eb91c4d838fd92f9d2171606.jpg)  
Figure 10. Architecture example of PWM generation in Stop 2 mode with LPBAM mechanism

# Firmware description

System clock:

system clock: MSI LPTIM1 source clock: LSE

# LPTIM1:

instance: LPTIM1_Channel1 source clock: LSE   
prescaler = 1   
trigger source: software trigger

• LPDMA

instance: LPDMA1_Channel0   
source clock: MSI   
linked-list mode: Circular mode   
transfer-event mode: TC event generated at the end of the last linked-list item   
with the LPBAM task: sequence of DMA transactions conditioned by the LPTIM1 request/trigger

# 6.3

# Timeout wakeup mode

The L can egure  peally wakep he viom Sleep tomode eaple y e u mwakvn ration rmaluncon like a watchogs ong s the periictrier keecong, edevice y uow uheeeeaknt.

c can enerat extenally aninjecte he I Inpu henever he  is red gure (CKSEL appropriately configured).

This LPTIM feature is controlle through the TIMOUT bit in the LPTIMCFGR register that alows therier signal to reset the LPTIM counter by the detection of an active edge when the timer is already started.

The timeout duration depends on the LPTIM frequency count and LPTIM_CMP (or LPTIM_CCRx) value, as follows:

Timeout = (CMP + 1) / LPTIM clock

# Note:

CMP is replaced by CCRx for LPTIM type 3.

I raeacivehanee st chieviSleSdeken ea. The timeout timing is presented in the diagram below.

![](images/0c9db6d95903b06fb6fbe9a16b1c0cf9aa245e0fc0ec0223f8e1faf007a73dfb.jpg)  
Figure 11. Timing of timeout wakeup from Stop 2 mode

The trigger signal can be selected from several sources by the TRIGSEL bits, such as GPIO, RTC alarm, RTC_TAMP and COMP_OUT. The TRIGSEL bits are used only when TRIGEN[1:0] is different from 00.

In teaple, heT  lbea  is valable  heod.e  as bee h src clock to run this LPTIM.The Tmeout mode is configurethrough the TIMOT bit in the LTIM1CFGR register. The LPTIM1 is started after detection of the first active edge on the LPTIM_ETR.

Before entering the low-power mode, the period and the pulse must be loaded to the LPTIM1_ARR and LPTIM_CMP (or LPTIM_CCRx) registers to set the timeout duration, then the LPTIM1 must be enabled.

The architecture of this example is described in the figure below.

![](images/0ab9044701266f7d80272354e011620f080dc1f131b4bd7cea8b3892d58568d7.jpg)  
Figure 12. Architecture example of timeout wakeup mode

# Firmware description

System clock:

System clock: HSI LPTIM1 source clock: LSE

• LPTIM1:

Source clock: internal source (LSE) Prescaler = 1 Trigger source: LPTIM_ETR pin Trigger polarity: rising edge Counter source: internal source (LSE)

# 6.4

# Autonomous input capture

In this example provided in the STM32CubeU5, the LPTIM instance used is LPTIM1 and the low-power mode is Stop mode. The LPTIM1 is configured in Input-capture mode: the external signal is connected to LPTIM1 Channel1 used as input pin.

# LPTIM1 configuration

Enable Autonomous mode: Enable or disable the peripheral bus clock when the SRD domain is in DRUN. After reset,the peripheral clock is disabled when CPUs are in CSTOP.   
Initialize the LPTIM according to the passed parameters.   
Suspend SysTick.   
Tominimize the power consumption, after starting Inpu-capture mode, he device enters Stop 2 mode and DMA transfers data from the LPTIM_CCR1 register to SRDDmaCapturedVa1ue buffer . When the transfer is completed, the DMA generates an interruption to wake up the device.   
Enter in Stop mode.   
Check that the system is resumed from Stop 2 mode, clear the OP flag, and check this last operation has been correctly done.   
Compute the expected SysTick value.   
Suspend SysTick.   
Get the input-capture value.

The architecture of this example is described in the figure below.

![](images/0714e45516a3b9883c7e5051c842db4736687c3ebab7093b577c17ee2599f418.jpg)  
Figure 13. Architecture example of input capture in Stop 2 mode (with Autonomous mode)

# Firmware description

System clock:

system clock: MSI LPTIM1 source clock: LSE

• LPTIM1:

instance: LPTIM1_Channel1 source clock: LSE   
prescaler = 1   
trigger source: software trigger

# LPDMA

instance: LPDMA1_Channel0   
source clock: MSI   
transfer direction: peripheral to memory   
transfer-event mode: TC event generated at the end of each block

# Revision history

Table 6. Document revision history   

<table><tr><td rowspan=1 colspan=1>Date</td><td rowspan=1 colspan=1>Version</td><td rowspan=1 colspan=1>Changes</td></tr><tr><td rowspan=1 colspan=1>18-Aug-2016</td><td rowspan=1 colspan=1>1</td><td rowspan=1 colspan=1>Initial release.</td></tr><tr><td rowspan=1 colspan=1>07-Nov-2016</td><td rowspan=1 colspan=1>2</td><td rowspan=1 colspan=1>Updated cover page.</td></tr><tr><td rowspan=1 colspan=1>13-Dec-2016</td><td rowspan=1 colspan=1>3</td><td rowspan=1 colspan=1>Extended scope to the document to add STM32F413/423 line devices.</td></tr><tr><td rowspan=1 colspan=1>19-Feb-2019</td><td rowspan=1 colspan=1>4</td><td rowspan=1 colspan=1>Updated:Extended scope to the document to add STM32L4+ Series, STM32H7 Series,STM32G0 Series and STM32WB Series devices.All tables in the document.Cover page.Added:Section 1 General information</td></tr><tr><td rowspan=1 colspan=1>17-Dec-2019</td><td rowspan=1 colspan=1>5</td><td rowspan=1 colspan=1>Extended the document scope to STM32L5 Series devices.Added mention of the repetition counter in Overview.</td></tr><tr><td rowspan=1 colspan=1>11-Aug-2020</td><td rowspan=1 colspan=1>6</td><td rowspan=1 colspan=1>Updated LPTIM availability for STM32H7 Series microcontrollers in Table 3.</td></tr><tr><td rowspan=1 colspan=1>27-Sep-2021</td><td rowspan=1 colspan=1>7</td><td rowspan=1 colspan=1>Added: Section 6.4 Autonomous input capture.Updated:Introduction with new STM32G4 Series, STM32MP1 Series, STM32U5 Series andSTM32WL SeriesSection 2 OverviewSection 5 Synchronization blockSection 4 LPTIM clock sourcesSection 6.2 PWM generation in Stop 2 mode</td></tr></table>

# Contents

General information   
Overview .   
LPTIM versus general-purpose timer..   
LPTIM clock sources .6   
5 Synchronization block . 7   
6 Use cases .8   
6.1 Asynchronous pulse counter in Stop 2 mode .8   
6.2 PWM generation in Stop 2 mode 10   
6.2.1 Tasks with legacy mechanism. 12   
6.2.2 Tasks with LPBAM mechanism . .13   
6.3 Timeout wakeup mode . .15   
6.4 Autonomous input capture . .16   
Revision history .18   
List of tables .20   
List of figures. . .21

# List of tables

Table 1. Applicable products 1   
Table 2. Features on various LPTIM types. 3   
Table 3. LPTIM types on STM32 devices. 4   
Table 4. TIM versus LPTIM in working modes 5   
Table 5. LPTIM clock source on different power mode. 6   
Table 6. Document revision history . 18

# List of figures

Figure 1. Input signal and corresponding counter value . 8   
Figure 2. Pulse-counter architecture example. 8   
Figure 3. STMicroelectronics Virtual COM port device manager 9   
Figure 4. Asynchronous pulse-counter increment 9   
Figure 5. Pulse-counter block diagram 9   
Figure 6. PWM generation in Stop mode with legacy mechanism 10   
Figure 7. PWM generation in Stop mode with LPBAM mechanism 10   
Figure 8. Counter timing diagram with and without update immediately 12   
Figure 9. Architecture example of PWM generator in Stop 2 mode with legacy mechanism 12   
Figure 10. Architecture example of PWM generation in Stop 2 mode with LPBAM mechanism 14   
Figure 11. Timing of timeout wakeup from Stop 2 mode 15   
Figure 12. Architecture example of timeout wakeup mode . 16   
Figure 13. Architecture example of input capture in Stop 2 mode (with Autonomous mode) 17

# IMPORTANT NOTICE  PLEASE READ CAREFULLY

ol uant  l.

Purchasers' products.

No license, express or implied, to any intellectual property right is granted by ST herein.

Te ames are the property of their respective owners.