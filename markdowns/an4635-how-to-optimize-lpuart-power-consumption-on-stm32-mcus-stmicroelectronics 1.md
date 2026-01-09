# Introduction

STM32 microcontrollers listed in Table 1 feature an alternative universal asynchronous receiver transmitter (UART) interface, enabling them to operate with minimum power requirements.

This document explains how to fully exploit the advantages of the low-power UART (LPUART), thus extending product battery life. It shows in practical examples the extremel low-power consumption of the device waiting for a communication.

The code used to perform the measurements described in Section 7.1 and Section 7.2 is supplied in the package X-CUBE-LPUART, and can be downloaded from www.st.com.

Table 1. Applicable products and software   

<table><tr><td rowspan=1 colspan=1>Type</td><td rowspan=1 colspan=1>Series, line or part number</td></tr><tr><td rowspan=5 colspan=1>Microcontrollers</td><td rowspan=1 colspan=1>STM32G0 and STM32G4 series</td></tr><tr><td rowspan=1 colspan=1>STM32L0, STM32L4, STM32L4+, and STM32L5 series</td></tr><tr><td rowspan=1 colspan=1>STM32H7 series</td></tr><tr><td rowspan=1 colspan=1>STM32U0, STM32U3, and STM32U5 series</td></tr><tr><td rowspan=1 colspan=1>STM32WB series</td></tr><tr><td rowspan=1 colspan=1>STM32 Embedded Software</td><td rowspan=1 colspan=1>X-CUBE-LPUART</td></tr></table>

# Contents

Definitions

Reference documents. 8

# Summary of features . . . . 9

3.1 Clock subsystem 9

3.1.1 MSI clock . 9   
3.1.2 HSI clock 9   
3.1.3 Low speed clock sources 9   
3.1.4 CSI clock 10

3.2 Power management 10

3.3 Comparison with USART peripheral 10

# Operation modes . . 12

4.1 Polling mode . . 12   
4.2 IT mode 12   
4.3 DMA mode 12   
4.4 Combined mode examples . 13   
4.4.1Interrupt with polling 13   
4.4.2 Combining DMA with direct access .13

# Other considerations 14

5.1 Execution from SRAM 14   
5.2 GPIO configuration . 14   
5.3 Clock configuration . . 14   
5.3.1 Clock prescalers 15

5.4 Power configuration 15

5.4.1 Use of Stop and Sleep modes 15   
5.4.2 Run time configuration 16   
5.4.3 STM32H7 core domain sections 17   
5.4.4 SMPS . 17

5.5 Cache memory 17

# Reliability and communication quality . . . . .. 18

6.1 Noise and frequency shift . 18   
6.2 Dropped bytes 18

# Power consumption comparison . . . . .. 19

# 7.1 Measurements on the STM32L053 Nucleo board 20

7.1.1 Stop vs. Sleep mode 20   
7.1.2 Short periods of Sleep mode and Low-power run 21   
7.1.3 Interrupt operation overhead 22   
7.1.4 Going to Stop between received bytes 23   
7.1.5 Different oscillator clock speeds 25   
7.1.6 Changing AHB divider ratio 26   
7.1.7 Different peripheral clock settings 28   
7.1.8 ULP bit setting 29   
7.1.9 Higher communication speed 30   
7.1.10 Wake-up from Stop mode on HSI 31   
7.1.11 Voltage regulator settings 33   
7.1.12 GPIO pull-up 34

# 7.2 Measurements on STM32L476 Nucleo board 36

7.2.1 Three approaches at a glance 36   
7.2.2 Simple polling mode on low core frequency 37   
7.2.3 The role of voltage regulator settings 38   
7.2.4 Idle modes compared 39   
7.2.5 Use of MSI PLL-mode for higher speeds 41   
7.2.6 Using two oscillators 42

# 7.3 Measurement on the STM32H743 Nucleo144 board 43

7.4 STM32WB55 Nucleo board testing 43   
7.5 STM32G474 Nucleo board testing 44   
7.6 STM32U575 Nucleo 144 board testing 45   
7.7 STM32U073RC Nucleo 64 board testing 47

# Example project . .. 48

8.1 HW setup 48   
8.2 Configuring the example 48   
8.3 Example operation 49

Conclusion .. 50

10

Revision history 51

# List of tables

Table 1. Applicable products and software. 1   
Table 2. List of acronyms .7   
Table 3. Comparison of features 10   
Table 4. Clock options 15   
Table 5. Configurations - Stop vs. Sleep mode 20   
Table 6. Configurations - Sleep mode vs. LPRUN 22   
Table 7. Configurations - Interrupt operation 23   
Table 8. Configurations - Stop during data reception . 24   
Table 9. Configurations - Core clock speed 25   
Table 10. Configurations - AHB divider 27   
Table 11. Configurations - Clock divider. 28   
Table 12. Configurations - ULP bit effect 30   
Table 13. Configurations - Higher communication speed. 31   
Table 14. Configurations - HSI vS. MSI 32   
Table 15. Configurations - Voltage regulator settings. 33   
Table 16. Configurations - GPIO pull-up.. 34   
Table 17. Configurations - Managing communication 36   
Table 18. Configurations - Polling.. 38   
Table 19. Configurations - Voltage regulator settings. 39   
Table 20. Configurations - Idle modes 40   
Table 21. Configurations - HSI and PLL 41   
Table 22. Configurations - Stop with 56700 Bd speed 42   
Table 23. Configurations - Managing communication 44   
Table 24. Influence of the AHB prescaler. 45   
Table 25. Comparison of different operation modes. 46   
Table 26. Comparison of different operation modes. 47   
Table 27. Document revision history 51

# List of figures

Figure 1. Test loop description. 19   
Figure 2. Stop vs. Sleep mode. . 20   
Figure 3. Sleep mode vs. LPRUN 21   
Figure 4. Interrupt operation overhead 23   
Figure 5. Using the Stop during data reception 24   
Figure 6. Core clock speed comparison 25   
Figure 7. Lowering oscillator speed compared to AHB divider 27   
Figure 8. Three different settings of peripheral clock divider. 28   
Figure 9. ULP bit effect 29   
Figure 10. Operating at 57600 Bd 30   
Figure 11. HSI vs. MSI at 4 MHz . 32   
Figure 12. Comparison between voltage regulator settings. 33   
Figure 13. GPIO internal pull-up 34   
Figure 14. Comparison of three different approaches to manage communication 36   
Figure 15. Polling communication at minimum settings.. 37   
Figure 16. Voltage regulator settings . 39   
Figure 17. Comparison of Idle modes 40   
Figure 18. HSI and PLL current consumption 41   
Figure 19. Using Stop with 57600 Bd speed 42   
Figure 20. Comparison of three different approaches to manage communication 44   
Figure 21. Interrupt operation with three different core clocks. 45   
Figure 22. Power consumption for different operation modes. 46   
Figure 23. Power consumption comparison (FIFO ON/OFF). . .47

# 1 Definitions

Table 2. List of acronyms   

<table><tr><td rowspan=1 colspan=1>Term</td><td rowspan=1 colspan=1>Description</td></tr><tr><td rowspan=1 colspan=1>LSE</td><td rowspan=1 colspan=1>Low-speed external clock</td></tr><tr><td rowspan=1 colspan=1>LSI</td><td rowspan=1 colspan=1>Low-speed internal clock</td></tr><tr><td rowspan=1 colspan=1>HSE</td><td rowspan=1 colspan=1>High-speed external clock</td></tr><tr><td rowspan=1 colspan=1>HSI, HSI16</td><td rowspan=1 colspan=1>High-speed internal clocks</td></tr><tr><td rowspan=1 colspan=1>MSI</td><td rowspan=1 colspan=1>Multispeed internal clock source</td></tr><tr><td rowspan=1 colspan=1>UART</td><td rowspan=1 colspan=1>Universal asynchronous receiver transmitter</td></tr><tr><td rowspan=1 colspan=1>LPUART</td><td rowspan=1 colspan=1>Low-power UART</td></tr><tr><td rowspan=1 colspan=1>MCU</td><td rowspan=1 colspan=1>Microcontroller</td></tr><tr><td rowspan=1 colspan=1>USART</td><td rowspan=1 colspan=1>Universal synchronous and asynchronous receiver transmitter</td></tr><tr><td rowspan=1 colspan=1>BLE</td><td rowspan=1 colspan=1>Bluetooth® Low Energy</td></tr><tr><td rowspan=1 colspan=1>CPU</td><td rowspan=1 colspan=1>Central processing unit (part of the MCU)</td></tr><tr><td rowspan=1 colspan=1>NVIC</td><td rowspan=1 colspan=1>Nested vector interrupt controller</td></tr><tr><td rowspan=1 colspan=1>DMA</td><td rowspan=1 colspan=1>Direct memory access</td></tr><tr><td rowspan=1 colspan=1>TC</td><td rowspan=1 colspan=1>Transmission complete</td></tr><tr><td rowspan=1 colspan=1>RF</td><td rowspan=1 colspan=1>Radio frequency</td></tr><tr><td rowspan=1 colspan=1>RM</td><td rowspan=1 colspan=1>Reference manual</td></tr><tr><td rowspan=1 colspan=1>SWD</td><td rowspan=1 colspan=1>Serial wire debug interface</td></tr><tr><td rowspan=1 colspan=1>BAM</td><td rowspan=1 colspan=1>Batch acquisition mode</td></tr><tr><td rowspan=1 colspan=1>LPBAM</td><td rowspan=1 colspan=1>Low-power background autonomous mode</td></tr></table>

# 2 Reference documents

The following documents (available on www.st.com) must be considered as reference:

C STM32L0xx ultra-low-power features overview (AN4445)   
C STM32L4xx ultra-low-power features overview (AN4621)   
• STM32L5 Series microcontroller ultra-low power features overview (AN5213) Using STM32 cache to optimize performance and power efficiency (AN5212) Optimizing power and performance with STM32L4 and STM32L4+ Series microcontrollers (AN4746) STM32L47xxx, STM32L48xxx, STM32L49xxx and STM32L4Axxx advanced Arm®- based 32-bit MCUs (RM0351) Ultra-low-power STM32LOx2 advanced Arm®-based 32-bit MCUs (RM0376) STM32H7x3 advanced Arm®-based 32-bit MCUs (RM0433) STM32H7A3/B3 advanced Arm®-based 32-bit MCUs (RM0455)   
C STM32H723/733, STM32H725/735 and STM32H730 Value line advanced Arm®- based 32-bit MCUs (RM0468) STM32H7R/7Sxx Arm®-based 32-bit MCUs (RM0477) Multiprotocol wireless 32-bit MCU Arm®-based Cortex®-M4 with FPU, Bluetooth® Low Energy and 802.15.4 radio solution (RM0434) Multiprotocol wireless 32-bit MCU Arm®-based Cortex®-M4 with FPU, Bluetooth® Low Energy or 802.15.4 radio solution (RM0471) STM32L552xx and STM32L562xx advanced Arm®-based 32-bit MCUs (RM0438) STM32G4xx advanced Arm®-based 32-bit MCUs (RM0440) and STM32G0x1 advanced Arm®-based 32-bit MCUs (RM0444)   
− STM32L4+ Series advanced Arm®-based 32-bit MCUs (RM0432)   
• STM32U5 Series Arm®-based 32-bit MCUs (RM0476)   
• STM32U0 series advanced Arm®-based 32-bit MCUs (RM0504)   
C STM32U3 series advanced Arm®-based 32-bit MCUs (RM0487)

# 3 Summary of features

While the LPUART peripheral is practically the same, there are significant differences in its integration on the MCUs addressed by this document. They feature different Arm® Cortex® cores(a), and there are other architectural differences impacting the LPUART efficiency.

# 3.1 Clock subsystem

# 3.1.1 MSI clock

This is an internal oscillator capable of fast, simple, and seamless change in operating frequency of low-power oriented devices. The maximum frequency is different for various MCUs, and so are the MSI ranges. This gearing up of the MSI reduces the choice of low speeds, the slowest possible frequency on STM32U0, STM32WB, STM32L4 and STM32L4+ products is 100 kHz, vs. 65 kHz on STM32L0xx MCUs.

On STM32U3 and STM32U5 series, the MSI is split (MSIS and MSIK). MSIK can be used for LPUART autonomous operation up to Stop2 mode (including wake-up capability), with clock speed different from system MSIS clock.

For speeds closer to 1 MHz, a direct comparison of efficiency is difficult. In the STM32L4, STM32L4+, STM32L5, STM32U0, STM32U3, STM32U5, and STM32WB series the MSI can use the HW auto calibration with LSE in its PLL-mode (option not available on STM32L0 products). This makes the MSI much more precise.

The MSI clock is not implemented on STM32G0, STM32G4, STM32H5, and STM32H7 series, not primarily intended as low-power devices.

# 3.1.2 HSI clock

The STM32L0 series features a simple clock factor-4 divider, associated with the HSI clock source, making the HSI the effective source of either the 16 or the 4 MHz. MCUs of other low-power series do not have a divider directly on the HSl16 clock. As a result, the STM32L0 is much more efficient in certain applications requiring UART speeds higher than 9600 Bd. If (for STM32WB, STM32L4, STM32L4+, STM32L5, STM32U3, and STM32U5 series) 16 MHz is not efficient, the solution is to use a second source for system clock.

STM32G0 and STM32G4 series MCUs feature an even more flexible divider, allowing to set the two dividers in the 1-512 range, using the HPRE bits in the RCC_CFGR register.

STM32H5 and STM32H7 series MCUs have a similar flexible setup, with HSIDIV divider values of 1, 2, 4, and 8, but with a 64 MHz nominal frequency oscillator.

# 3.1.3 Low speed clock sources

LSI clock frequency also differs, but this is not relevant to our case.

# 3.1.4 CSI clock

This is a low-power oscillator integrated on STM32H5 and STM32H7 devices. Its nominal frequency (4 MHz) is sufficient for most of the low-power tasks.

# 3.2 Power management

The main LDO regulator on STM32L4, STM32L4+, STM32G0, STM32G4, STM32U0, STM32U3, and STM32WB() series has only two ranges, instead of the the three available on the STM32LOxx MCUs. Moreover, these two ranges are shifted towards higher frequencies, supported by the more powerful MCU.

This deficiency is compensated by the Low-power run mode.

STM32LOxx MCUs cannot return to the Low-power run mode directly upon waking from Sleep or Stop Low-power mode, this limitation is not present in the series featuring a Low-power mode. Low-power run on STM32L4, STM32L4+, STM32G0, STM32G4, STM32U0, and STM32WB series is not limited by the MSI range 1, but works up to 2 MHz system clock speed. HSl16 can still be used as peripheral clock, even in Low-power run.

STM32H5, STM32H7(b), and STM32U5 MCUs feature four LDO or SMPS power regulator ranges, resulting in an extended performance range.

STM32L5 relies on SMPS regulation, which is only optional in other products.

# 3.3 Comparison with USART peripheral

The LPUART has less features compared to the USART, however it operates using less power, and uses the LSE clock more efficiently.

The main features for the two peripherals are summarized in Table 3.

Table 3. Comparison of features   

<table><tr><td rowspan=1 colspan=1>Configuration</td><td rowspan=1 colspan=1>LPUART</td><td rowspan=1 colspan=1>USART</td></tr><tr><td rowspan=1 colspan=1>LSE clocked 9600 Bd option</td><td rowspan=1 colspan=1>+</td><td rowspan=1 colspan=1>-</td></tr><tr><td rowspan=1 colspan=1>Synchronous mode</td><td rowspan=1 colspan=1>-</td><td rowspan=1 colspan=1>+</td></tr><tr><td rowspan=1 colspan=1>Ir SIR compatibility</td><td rowspan=1 colspan=1></td><td rowspan=1 colspan=1>+</td></tr><tr><td rowspan=1 colspan=1>Smartcard mode</td><td rowspan=1 colspan=1></td><td rowspan=1 colspan=1>+</td></tr><tr><td rowspan=1 colspan=1>Auto baud rate detection</td><td rowspan=1 colspan=1></td><td rowspan=1 colspan=1>+</td></tr><tr><td rowspan=1 colspan=1>Modbus communication</td><td rowspan=1 colspan=1></td><td rowspan=1 colspan=1>+</td></tr><tr><td rowspan=1 colspan=1>LIN mode</td><td rowspan=1 colspan=1>-</td><td rowspan=1 colspan=1>+</td></tr></table>

The USART is also able to operate using the LSE clock, the communication speed is limited to 4000 Bd in case of oversampling by 8, to 2000 Bd when oversampling is by 16.

When using the LPUART, only the 32.768 kHz LSE clock is required for serial communication up to 9600 Bd, with minimal energy consumption and very precise speed setting made possible by the external crystal.

For higher speeds the LPUART energy efficiency advantage drops, but still remains close to 5% (see Section 7.1.9).

This document focuses on communication at 9600 Bd, common to many applications: the efficiency advantage of LPUART is obvious when using wake-up from Stop at the 9600 Bd speed setting.

The LPUART can initiate wake-up from deeper Stop modes, such as Stop2 or Stop1.

# 4 Operation modes

Real-world scenarios cover a wide variety of configurations, using different baud rates, ratios of transmit/receive and delays between messages. All these factors influence the choice of the operation mode.

# 4.1 Polling mode

Polling mode (also known as blocking mode) is the simplest possible operating mode. The CPU is processing a single task, switching to a low-power mode during periods of inactivity. There is almost no processing overhead, making it possible to use very low system clock speeds.

This mode is extremely efficient for very simple scenarios, however it effectively blocks the CPU from executing other tasks, like data processing or concurrent communication.

# 4.2 IT mode

The second option is to rely completely on interrupts, waking the CPU for every transferred h ® e split to atomic operations, never blocking the CPU, and achieving real-time responses.

This mode strains the CPU a little more, adding processing overhead related to stack and context resuming.

# 4.3 DMA mode

In DMA mode the CPU is spared a large portion of processing, setting a DMA channel to move data between the peripheral and the SRAM. The CPU can spend part of the processing time in Sleep mode. The user can disable half-buffer interrupt when not needed for circular buffer management, to let the CPU core rest even longer. In most of the cases the DMA cannot be used in combination with the Stop mode, hence all DMA channels have to be disabled before entering the Stop Low-power mode. Some of the STM32H7 MCUs are an exception to this rule because the power domains are split, and the DMA with LPUART can operate within separate domains. Details are provided in Section 7.3. The STM32U5 introduces an LPBAM, which can operate while the CPU is in Stop mode.

On devices that do not feature LPBAM, the LPUART transfer can be done thanks to the batch acquisition mode (BAM), in which the MCU is in Sleep or in Low-power sleep mode (CPU is clocked off). The consumption is optimized by configuring the flash memory in Power-down mode, switching off its clock, and by clocking only the DMA, the LPUART, and the SRAM.

The DMA has one definitive advantage over the previous two methods: the transfer to memory is handled independently from the CPU load and the interrupt is only triggered once the data is stored in RAM for the firmware to process the following action. With interrupt and polling mode the firmware must read the data from the peripheral register, and with wrong timing some data can be lost in overrun error.

# 4.4 Combined mode examples

Real-world applications usually are a mix of the described modes, and the developers always try to strike the best bargain between conflicting needs. The following examples are not covered in bundled source codes.

# 4.4.1 Interrupt with polling

Some embedded systems are not real-time critical, in this case there is an option to block the CPU for a limited time to process a message frame. Especially in case of transmission, energy normally used to process all TC interrupts is saved. The message is transmitted in blocking mode, possibly with clock speed lowered and power regulator switched to Low-power mode (LPRUN). Only approximately half clock speed is required if the CPU can treat the message in blocking mode. Normal operation is then restored, preferably waiting for incoming reply interrupt in Stop mode.

# 4.4.2 Combining DMA with direct access

The DMA channel is convenient for transmission of data, and is power-efficient during reception.

The downside is that in DMA mode the LPUART cannot take advantage of wake-up from Stop mode. The reason is that after wake-up event the DMA has difficulty picking up on the ongoing communication. This is a serious disadvantage for all applications staying idle for long periods of time.

The DMA can stillbe used for transmission and then reception can proceed with blocking or interrupt approach. In communication systems where incoming messages are coming in quick succession or predictable timing, the DMA based reception is an efficient option.

# 5 Other considerations

For a complete overview of low-power advantages refer to the already mentioned AN4445, AN4621 and AN4746. The following recommendations are specific for our case and example.

# 5.1 Execution from SRAM

If the program can be executed from SRAM, there is an option to turn off the embedded flash memory (by clock gating), further reducing the power consumption. The SRAM is also capable of execution at full CPU speed, without flash memory latency.

# 5.2 GPIO configuration

Some GPlO settings have great influence on power consumption, while others do not.

The pins used for the UART communication lines should be configured to their alternate function mode. It is not recommended to activate pull-ups if lowest possible power consumption is the most important goal, however, in some applications it may be necessary to improve the communication reliability. The speed setting has no consequences regarding the power consumption on the tested baud rates.

Half-duplex mode, when applicable, can lead to further power savings, but this configuration is not addressed in this document.

Other pins, not used by the application, must be configured as analog inputs. The developer must put the debug lines also to analog, once the application is ready for deployment.

On some products, such as the STM32L4 series, the LPUART can be assigned to GPIOG port with alternate (lower) voltage, leading to additional energy savings.

# 5.3 Clock configuration

For LPUART peripheral clock, LSE source is the choice to reach 9600 Bd with wake-up from Stop mode.

HSI/CSI is recommended for higher speeds.

The obvious (and default) choice for system clock is usually the MSl oscillator. On STM32L4, STM32L4+, STM32U0, STM32U3, STM32U5, and STM32WB series the MSI offers even more flexibility and its fluctuations can be corrected using HW auto calibration with the LSE in its PLL-mode.

Prescalers and PLL can be used to derive other speeds, different options are analyzed later in this document. These solutions are not the best ones when power consumption is the first concern. User must refer to the product datasheet for typical power consumptions for different clock configurations.

It makes sense to use a single high speed clock for system and peripherals, as each high speed oscillator contributes to power consumption. On the other hand, it is advantageous to run the low speed clock in parallel to the system clock, and use it for the peripherals able to work at that frequency.

Table 4. Clock options   

<table><tr><td rowspan=1 colspan=1>Source</td><td rowspan=1 colspan=1>Advantages</td><td rowspan=1 colspan=1>Limitations</td></tr><tr><td rowspan=1 colspan=1>HSI/HSI16</td><td rowspan=1 colspan=1>Ready to use high speed clock withprecise trimming</td><td rowspan=1 colspan=1>— Worst MHz / W ratio option- Fixed speed on most of STM32 MCUs</td></tr><tr><td rowspan=1 colspan=1>MSI</td><td rowspan=1 colspan=1>- Easy and fast clock throttling- Lowest overall power consumption (onSTM32L0 series when clocked below1 MHz)</td><td rowspan=1 colspan=1>- Only available on low-power MCUs Clock is relatively unstable and imprecise(unless the auto-calibration using LSE inPLL-mode is used)</td></tr><tr><td rowspan=1 colspan=1>HSE</td><td rowspan=1 colspan=1>- Potentially most power efficient at1 MHz and above on STM32L0 series- Efficiency comparable to MSI onSTM32L4 series</td><td rowspan=1 colspan=1> Needs additional external components(1)- Limited options of speed control(prescalers only)</td></tr></table>

HSE is used by the RF block in STM32WB series MCUs, so the components are needed anyway.

# 5.3.1 Clock prescalers

The RCC module offers the possibility to tune down peripheral bus clocks, the AHB and APB frequency (RCC_CFGR register).

Slowing the AHB down brings significant power savings if there is no other clock source with a suitable frequency. The memory interface is also clocked with AHB. While power consumption with prescaler of 8 drops by approximately 50%, the processing capability of the system drops even more, due to delays in fetching instructions from the program memory and in storing the data in the memory. If possible, it is better to slow down the system clock rather than set an AHB prescaler (Section 7.1.6).

Slowing down the APB limits the bandwidth between the LPUART peripheral and the core. This is usually not a problem, as the amount of data transferred is low, especially in case of DMA transfers. In case of CPU driven transfers the core can be stalled waiting for the bus transfer to complete. This causes the overall energy budget for the operation to increase in extreme cases. Also, if the bus transfer is not complete, the core is prevented from going to a low-power mode. In the examples described in this document it is usually safe to set an APB prescaler value of 4, as higher values are likely to cause problems, and do not reduce power consumption (Section 7.1.7).

# 5.4 Power configuration

This section deals with practical implications when configuring power modes for LPUART communication. For complete information read the dedicated sections in the reference manuals.

# 5.4.1 Use of Stop and Sleep modes

It is a paradigm in embedded software that, during the idle time, the CPU must not run and actively check flags, but rather switch to Low-power mode, suspend clock, and only resume operation on external interrupts or events.

In MCUs based on Arm® cores, this is achieved by executing WFE or WFI instruction. All STM32 microcontrollers offer highly configurable selection of Idle modes, described in detail in the reference manuals. The great advantage of LPUART is the ability to take advantage of Stop mode when waiting for message reception (Section 7.1.1).

If the application running on STM32L0xx products does not use VREFINT frequently and spends most of the time in low-power modes, configure Ultra-low-power mode with fast wake-up (ULP and FWU bit in PWR configuration register). Even in applications using internal voltage reference, it is advised to switch it off, and check only the startup time when a measurement is needed (VREFINT startup requires some additional energy). For short periods of Low-power mode (i.e. Sleep mode between bytes) there is no advantage in turning it off and on again, the overall energy budget increases.

# Note:

Ultra-low-power mode without fast wake-up is unable to keep the LPUART Tx register fed, or to keep up with incoming data in blocking and interrupt mode, even with 9600 Bd communication speed.

There is no option to completely switch off the VREFINT on the other series addressed by this document.

In most cases, it is desirable to activate the Sleep mode between processing individual bytes. In case or data reception even Stop mode is available (Section 7.1.4). This practice offers great advantage at higher clock speeds, but at core clock speeds near the bare minimum needed for communication it is not recommended. The overhead related to putting device to Sleep mode and waking it causes a slight increase of power consumption, not balanced by the very short time spent in Low-power mode (Section 7.1.2).

# 5.4.2 Run time configuration

The voltage regulator settings are very important. Use the core voltage scaling as much as possible (see dedicated sections in datasheets and reference manuals). As an example, on STM32L0xx switching from Range 1 to Range 3 is an easy way to lower typical consumed power by more than 25% (Section 7.1.11).

Other low-power series (except STM32L0 and STM32U5) provide only two ranges of the main regulator, however all these series (except STM32U5) feature a Low-power run mode.

As an example, on STM32LOxx MCUs in polling mode, which requires the least CPU processing resources, it is possible to take advantage of the Low-power run mode. This mode essentially bypasses the main voltage regulator, and powers the core with a consumption approximately 25% lower than that achievable with Range 3 of the main power regulator (Section 7.1.2).

On STM32LOxx MCUs waking from Stop or Sleep mode brings the main regulator back on, and because of the current low clock speed (MSl Range 1 at most), the core must immediately dedicate all processing power to data reception. In practical terms the LPRUN is great for transmission phase, but when waiting for data reception it is usually better to take advantage of the Stop mode instead of keeping the CPU in LPRUN. It is however possible to put the main voltage regulator temporarily to Range 3 (it must be in Range 2 when switch to LPRUN is done). Changing configuration of main regulator is quicker than switching the regulator, and less likely to cause dropped bytes in incoming message (wakeup from Stop and power configuration changes must be handled in time shorter than 1 byte duration).

On STM32L4, STM32L4+, STM32L5, and STM32U0 series the LPRUN mode provides additional functionality. It works up to 2 MHz, providing enough processing power for 57600 Bd communication speed in interrupt mode. It is even possible to wake from Stop or Sleep directly to Low-power run, without waking up the main regulator.

The STM32WB regulator power scaling is identical to that of STM32L4 and STM32L5, but, because of the second core, there are more options, exceeding the scope of this document.

The STM32G4 and STM32G0 have two base power scaling ranges, with Range 2 available up to 26 and 16 MHz, respectively.

STM32U5, STM32H5 and STM32H7 MCUs feature four ranges of the internal LDO, there are two on STM32U3 devices. All come with some cache and prefetch. It is advised, for power efficiency, to accept higher latency, and choose the lowest LDO voltage setting for the chosen system clock.

# 5.4.3 STM32H7 core domain sections

Larger devices, based on the Cortex-M7 core, use independent power domains to maintain DMA operation while the CPU is in low power mode. In STM32H74x/H75x/H72x/H73x the LPUART is linked to D3 domain, while on STM32H7Ax/H7Bx it is called SRD, serving the same purpose.

The power domain has its dedicated memory section, to avoid powering the whole memory during the low-power state.

See the specific product reference manual for details and implementation examples.

# 5.4.4 SMPS

Some STM32L4+, STM32L5, STM32U3, STM32U5, and STM32WB products feature an integrated SMPS, a power supply option that increases efficiency, especially if the available VDD branch of the PCB is relatively high voltage (like 3.3 V).

A detailed explanation of the usage of the embedded SMPS is out of the scope of this document.

# 5.5 Cache memory

Several STM32 microcontrollers feature a cache memory. Having the instructions or data available in the cache instead of waiting for fetch from system memory improves execution efficiency and power consumption. Refer to "STM32 power mode examples" (AN4777), available on www.st.com, to learn more about different cache configurations.

# Reliability and communication quality

# 6.1 Noise and frequency shift

Line noise usually causes no issues at the low communication speed typical of low-power applications. In some cases, random noise can be mitigated by adding a weak pull-up, at the expense of additional energy. For example, the internal pull-up (no extra parts) increases power consumption by approximately 30 pA during transmission in the example described in Section 8.

Framing errors occur as result of incorrect base frequency (speed setting) at one of the communication participants. The LSE clock source, which is best suited for low-power applications, is very accurate. The framing errors are likely only if the LPUART peripheral clock is derived from MSI clock. The LPUART cannot auto detect the uncalibrated communication speed of its counterpart, relying only on the precise speed settings with framing reliability.

# 6.2 Dropped bytes

To achieve lower power consumption tune down core frequency and use low-power modes.

This imposes a challenge of waking up and responding to peripheral events. In transmission case this may cause delay between bytes sent, leading to prolonged period of activity, impacting system efficiency, but without data loss.

The problem is data reception. In polling or interrupt driven mode, if the received data in the LPUART data register is not read in time (before a new data is received), an overrun error occurs, and data received during overrun are lost.

To avoid missing data in reception, the following guidelines can be provided:

• ensure a correct clock speed (not below a certain minimum) for the core boost the LPUART interrupts priorities to the highest possible level in the application, to make them basically un-interruptible use the DMA for data transfers

# Power consumption comparison

All the pictures in this section show the detailed measurement of differently configured Low-power Nucleo running the following routine, graphically illustrated in Figure 1:

1. Run mode in waiting loop, showing the regular power consumption   
2. Transmission of a 100-byte message   
3. Idle state 10 ms: Stop or Sleep mode waiting for reply (depending on configuration)   
4. Reception of the same 100 bytes   
5. Compare the message to detect communication errors and go back to 1

![](images/23075d1d4098d9f0db95a5faa92cbe9ea0edc4d93fc06c10bef31350f07436f4.jpg)  
Figure 1. Test loop description

The device starts running full speed in the loop to showcase the regular power consumption on its clock configuration. This is followed by approximately 100 ms of 9600 Bd transmission, then 10 ms of idle state, waiting for the incoming reply. Only few measurements feature the higher communication speed of 57600, where the communication phases 2 and 4 are significantly shorter. Receiving the reply takes another 100 ms.

Both the transmission and reception usually consume less power than the regular run mode, as the device is configured to save power in short periods between single bytes of the message.

The measurements detailed in the following pages are an example of how the X-CUBE-LPUART Expansion Package can be used: it does not cover all the MCU with LPUART and it does not compare all their configurations, but points out interesting features and shows some available solutions.

# Note:

All measurement have been performed at temperatures around 25 C on Nucleo boards. They are in line with datasheet typical values, but this does not ensure that every single MCU reproduces the same values.

# 7.1 Measurements on the STM32L053 Nucleo board

# 7.1.1 Stop vs. Sleep mode

The first comparison deals with the difference between Sleep and Stop modes.

While waiting for the incoming communication, the device tries to minimize the power consumption. The black line in Figure 2 represents debug configuration with device waiting in Sleep mode. Using the LSE clock and LPUART peripheral the Stop mode can be employed up to speed of 9600 Bd (the green line). The purple line shows the absolute minimum current absorbed in Stop mode where the debug lines are configured as analog input and the device uses the ULP + FWU combination.

![](images/718667d95781c24c3c0d49cd649e7aa2332141b90de1aed8873d2db5a205c54a.jpg)  
Figure 2. Stop vs. Sleep mode

Table 5. Configurations - Stop vs. Sleep mode   

<table><tr><td colspan="1" rowspan="1">Curve in Figure 2</td><td colspan="1" rowspan="1">Black</td><td colspan="1" rowspan="1">Green</td><td colspan="1" rowspan="1">Purple</td></tr><tr><td colspan="1" rowspan="1">Idle mode betweentransmissions</td><td colspan="1" rowspan="1">Sleep</td><td colspan="2" rowspan="1">Stop</td></tr><tr><td colspan="1" rowspan="1">Debug interface</td><td colspan="2" rowspan="1">ON</td><td colspan="1" rowspan="1">OFF</td></tr><tr><td colspan="1" rowspan="1">Current averageover phases 2, 3, and 4</td><td colspan="1" rowspan="1">83.3 μA</td><td colspan="1" rowspan="1">80.3 μA</td><td colspan="1" rowspan="1">77.3 μA</td></tr><tr><td colspan="1" rowspan="1">Clock</td><td colspan="3" rowspan="1">500 kHz MSI</td></tr><tr><td colspan="1" rowspan="1">Voltage regulator</td><td colspan="3" rowspan="1">Range 3</td></tr><tr><td colspan="1" rowspan="1">ULP/FWU</td><td colspan="3" rowspan="1">+/+</td></tr><tr><td colspan="1" rowspan="1">AHB/APB ratio</td><td colspan="3" rowspan="1">1/1</td></tr><tr><td colspan="1" rowspan="1">Baud rate</td><td colspan="3" rowspan="1">9600 Bd</td></tr><tr><td colspan="1" rowspan="1">SW used</td><td colspan="3" rowspan="1">Interrupt operation (Com IT) with defines RXSLEEP and TXSLEEP</td></tr></table>

# 1.2 Short periods of Sleep mode and Low-power run

In some cases the WFE can be used to put the core to suspended mode while waiting for a flag or event, but this can increase the power consumption. When the core clock speed is just enough to perform the requested operation, adding WFE instruction can increase the power consumption. Consider using the Low-power run regulator mode instead. The Lowpower run effect is terminated with each wake-up from either Stop or Sleep mode, but until that wake-up t saves a lot ofy.

In Figure 3 the red line represents the configuration where the execution in Low-power run mode is terminated by the code that goes to Sleep mode after each byte transmission. The green line is a code that runs with voltage regulator set to Range 3, making no attempts to use Sleep mode during transmission. The black line is the power consumption of a code that stays in LPRUN until it goes to Stop mode after finishing the transmission. Allthree codes use the regulator Range 3 along with Sleep mode after each byte during reception phase. In case of such a short time in Stop mode it is more efficient to leave the code in LPRUN all the time.

![](images/f9a2766bbdfc56ae19b114511921bfa7ed423f14f6ab1096b9b61b017d494045.jpg)  
Figure 3. Sleep mode vs. LPRUN

Table 6. Configurations - Sleep mode vs. LPRUN   

<table><tr><td rowspan=1 colspan=1>Curve in Figure 3</td><td rowspan=1 colspan=1>Black</td><td rowspan=1 colspan=1>Green</td><td rowspan=1 colspan=1>Red</td></tr><tr><td rowspan=1 colspan=1>Idle mode betweentransmissions</td><td rowspan=1 colspan=3>Stop</td></tr><tr><td rowspan=1 colspan=1>Debug interface</td><td rowspan=1 colspan=3>OFF</td></tr><tr><td rowspan=1 colspan=1>Current averageover phases 2, 3, and 4</td><td rowspan=1 colspan=1>34.9 μA</td><td rowspan=1 colspan=1>40.0 μA</td><td rowspan=1 colspan=1>42.0 μA</td></tr><tr><td rowspan=1 colspan=1>Clock</td><td rowspan=1 colspan=3>130 kHz MSI</td></tr><tr><td rowspan=1 colspan=1>Voltage regulator</td><td rowspan=1 colspan=1>LPRUN, then Range 3</td><td rowspan=1 colspan=2>Range 3</td></tr><tr><td rowspan=1 colspan=1>AHB/APB ratio</td><td rowspan=1 colspan=3>1/1</td></tr><tr><td rowspan=1 colspan=1>ULP/FWU</td><td rowspan=1 colspan=3>+/+</td></tr><tr><td rowspan=1 colspan=1>Baud rate</td><td rowspan=1 colspan=3>9600 Bd</td></tr><tr><td rowspan=1 colspan=1>SW used</td><td rowspan=1 colspan=2>Blocking operation (Com polling)with define RXSLEEP</td><td rowspan=1 colspan=1>Also TXSLEEP defined</td></tr></table>

# 7.1.3 Interrupt operation overhead

The interupt mechanism on the Arm® Cortex® core is very efficient, but still represents an additional effort. This fact is best illustrated by comparison on the very minimum core clock suitable for interrupt driven operation of our example code, 250 kHz.

As shown in Figure 4, the IT code (black line) actually spends almost no time in Sleep mode (waiting for interrupt) and the power consumption is comparatively high. Blocking operation represented by the red line saves some energy in waiting for event (Tx buffer empty or Rx buffer full).

This comparison cannot be absolutely fair, as a different code is executed, nevertheless it holds significance of code optimization too.

![](images/add86adec459c20a19c98adc5e0dd527e9f3a8f52d3d7f8a13536bddd5133920.jpg)  
Figure 4. Interrupt operation overhead

Table 7. Configurations - Interrupt operation   

<table><tr><td rowspan=1 colspan=1>Curve in Figure 4</td><td rowspan=1 colspan=1>Black</td><td rowspan=1 colspan=1>Red</td></tr><tr><td rowspan=1 colspan=1>Idle mode betweentransmissions</td><td rowspan=1 colspan=2>Stop</td></tr><tr><td rowspan=1 colspan=1>Debug interface</td><td rowspan=1 colspan=2>OFF</td></tr><tr><td rowspan=1 colspan=1>Current averageover phases 2, 3, and 4</td><td rowspan=1 colspan=1>66.6 μA</td><td rowspan=1 colspan=1>44.3 μA</td></tr><tr><td rowspan=1 colspan=1>Clock</td><td rowspan=1 colspan=2>250 kHz MSI</td></tr><tr><td rowspan=1 colspan=1>Voltage regulator</td><td rowspan=1 colspan=2>Range 3</td></tr><tr><td rowspan=1 colspan=1>AHB/APB ratio</td><td rowspan=1 colspan=2>1/1</td></tr><tr><td rowspan=1 colspan=1>ULP/FWU</td><td rowspan=1 colspan=2>+/+</td></tr><tr><td rowspan=1 colspan=1>Baud rate</td><td rowspan=1 colspan=2>9600 Bd</td></tr><tr><td rowspan=1 colspan=1>SW used</td><td rowspan=1 colspan=1>Interrupt operation (Com IT)with defines RXSLEEPand TXSLEEP</td><td rowspan=1 colspan=1>Blocking operation (Com polling)with defines RXSLEEPand TXSLEEP</td></tr></table>

# 7.1.4 Going to Stop between received bytes

The LPUARTs ability to wake from Stop on external event leads to possibility to enter the Stop mode even during pause between bytes in reception phase.

The best results comes with operational speeds slightly below the limit of voltage regulator Range 3, specifically 4 MHz MSI clock. In this way the interrupt overhead time is very short and the MCU spends most of the time in Stop mode.

Lower speeds actually lead to slightly higher power consumption during reception. The difference is not big, just around 10%. Yet still using polling and very slow clock setting the power consumption can be even lower than this, at the expenses of the flexibility of serving any other tasks.

![](images/cbc216cd5881b01b236a67cf83e16915726feee170c4da117048dc241403830e.jpg)  
Figure 5. Using the Stop during data reception

Table 8. Configurations - Stop during data reception   

<table><tr><td rowspan=1 colspan=1>Curve in Figure 5</td><td rowspan=1 colspan=1>Black</td><td rowspan=1 colspan=1>Red</td></tr><tr><td rowspan=1 colspan=1>Idle mode betweentransmissions</td><td rowspan=1 colspan=2>Stop</td></tr><tr><td rowspan=1 colspan=1>Debug interface</td><td rowspan=1 colspan=2>OFF</td></tr><tr><td rowspan=1 colspan=1>Current average</td><td rowspan=1 colspan=1>55.5 μA (Rx only)</td><td rowspan=1 colspan=1>61.8 μA (Rx only)</td></tr><tr><td rowspan=1 colspan=1>Clock</td><td rowspan=1 colspan=1>4 MHz MSI</td><td rowspan=1 colspan=1>500 kHz MSI</td></tr><tr><td rowspan=1 colspan=1>Voltage regulator</td><td rowspan=1 colspan=2>Range 3</td></tr><tr><td rowspan=1 colspan=1>AHB/APB ratio</td><td rowspan=1 colspan=2>1/1</td></tr><tr><td rowspan=1 colspan=1>ULP/FWU</td><td rowspan=1 colspan=2>+/+</td></tr><tr><td rowspan=1 colspan=1>Baud rate</td><td rowspan=1 colspan=2>9600 Bd</td></tr><tr><td rowspan=1 colspan=1>SW used</td><td rowspan=1 colspan=2>Interrupt operation (Com IT) with defines RXSTOP and TXSLEEP</td></tr></table>

# 7.1.5 Different oscillator clock speeds

Using the MSl clock the application computing power and power consumption can be easily tuned to imminent needs of the system. It is of course possible to change the clock settings on the fly, during execution.

Figure 6 shows the test execution at 2 MHz (black line), 500 kHz (red line) and 130 kHz (green line). The difference is large, but using the Sleep mode between both transmitted and received bytes the duty cycle makes it less prominent, at higher speeds the core spends more time in Low-power state.

There is,of course, o observable difference during the Stop mode.

![](images/100d566700e484e407c4b3781c45a5761234d24a08f336bf9fdc57473deaf772.jpg)  
Figure 6. Core clock speed comparison

Table 9. Configurations - Core clock speed   

<table><tr><td colspan="1" rowspan="1">Curve in Figure 6</td><td colspan="1" rowspan="1">Black</td><td colspan="1" rowspan="1">Green</td><td colspan="1" rowspan="1">Red</td></tr><tr><td colspan="1" rowspan="1">Idle mode betweentransmissions</td><td colspan="3" rowspan="1">Stop</td></tr><tr><td colspan="1" rowspan="1">Debug interface</td><td colspan="3" rowspan="1">OFF</td></tr><tr><td colspan="1" rowspan="1">Current averageover phases 2, 3, and 4</td><td colspan="1" rowspan="1">136.6 μA</td><td colspan="1" rowspan="1">42 μA</td><td colspan="1" rowspan="1">57.1 μA</td></tr><tr><td colspan="1" rowspan="1">Clock</td><td colspan="1" rowspan="1">2 MHz MSI</td><td colspan="1" rowspan="1">130 kHz MSI</td><td colspan="1" rowspan="1">500 kHz MSI</td></tr><tr><td colspan="1" rowspan="1">Voltage regulator</td><td colspan="3" rowspan="1">Range 3</td></tr><tr><td colspan="1" rowspan="1">AHB/APB ratio</td><td colspan="3" rowspan="1">1/1</td></tr><tr><td colspan="1" rowspan="1">ULP/FWU</td><td colspan="3" rowspan="1">+1+</td></tr><tr><td colspan="1" rowspan="1">Baud rate</td><td colspan="3" rowspan="1">9600 Bd</td></tr><tr><td colspan="1" rowspan="1">SW used</td><td colspan="3" rowspan="1">Blocking operation (Com polling) with RXSLEEP and TXSLEEP defined</td></tr></table>

# 7.1.6 Changing AHB divider ratio

Changing the AHB divider ratio leads to decreased power consumption since most of the circuitry runs at lower frequency.

This is demonstrated in Figure 7, where the black line is the current absorption of the example running at 1 MHz MSI clock, and the red line is the same code running with AHB divider set to 4. If the clock can be directly configured to lower frequency, it is always better to choose this option. The green line represents the same example, only the MSl oscillator is set directly to 250 kHz. Proven by the difference between Sleep mode and run phase the actual processing power is the same, but the solution without AHB divider is more efficient.

Use of the AHB divider only makes sense with external clock or if there is necessity to use the HSI.

![](images/239e63d0f2faaa8c87c8314ff6a6b5e87b2ca7ad3d27fd5c73e1faee4a2fd00b.jpg)  
Figure 7. Lowering oscillator speed compared to AHB divider

Table 10. Configurations - AHB divider   

<table><tr><td rowspan=1 colspan=1>Curve in Figure 7</td><td rowspan=1 colspan=1>Black</td><td rowspan=1 colspan=1>Green</td><td rowspan=1 colspan=1>Red</td></tr><tr><td rowspan=1 colspan=1>Idle mode betweentransmissions</td><td rowspan=1 colspan=3>Stop</td></tr><tr><td rowspan=1 colspan=1>Debug interface</td><td rowspan=1 colspan=3>OFF</td></tr><tr><td rowspan=1 colspan=1>Current averageover phases 2, 3, and 4</td><td rowspan=1 colspan=1>75.9 μA</td><td rowspan=1 colspan=1>44.3 μA</td><td rowspan=1 colspan=1>63.9 μA</td></tr><tr><td rowspan=1 colspan=1>Clock</td><td rowspan=1 colspan=1>1 MHz MSI</td><td rowspan=1 colspan=1>250 kHz MSI</td><td rowspan=1 colspan=1>1 MHz MSI</td></tr><tr><td rowspan=1 colspan=1>Voltage regulator</td><td rowspan=1 colspan=3>Range 3</td></tr><tr><td rowspan=1 colspan=1>AHB/APB ratio</td><td rowspan=1 colspan=2>1/1</td><td rowspan=1 colspan=1>4/1</td></tr><tr><td rowspan=1 colspan=1>ULP/FWU</td><td rowspan=1 colspan=3>+1+</td></tr><tr><td rowspan=1 colspan=1>Baud rate</td><td rowspan=1 colspan=3>9600 Bd</td></tr><tr><td rowspan=1 colspan=1>SW used</td><td rowspan=1 colspan=3>Blocking operation (Com polling) with RXSLEEP and TXSLEEP defined</td></tr></table>

# 7.1.7 Different peripheral clock settings

DMA based communication was measured on three different APB clock divider settings, as shown in Figure 8, where the black line represents current consumption with no divider, the red and green lines with divider set to 4 and to 8, respectively.

![](images/9f98ed17e200d77ad104e0d9dce488a306a4bd696737511e1f564f5ee03563c2.jpg)  
Figure 8. Three different settings of peripheral clock divider

Table 11. Configurations - Clock divider   

<table><tr><td colspan="1" rowspan="1">Curve in Figure 8</td><td colspan="1" rowspan="1">Black</td><td colspan="1" rowspan="1">Red</td><td colspan="1" rowspan="1">Green</td></tr><tr><td colspan="1" rowspan="1">Idle mode betweentransmissions</td><td colspan="3" rowspan="1">Stop</td></tr><tr><td colspan="1" rowspan="1">Debug interface</td><td colspan="3" rowspan="1">OFF</td></tr><tr><td colspan="1" rowspan="1">Current averageover phases 2, 3, and 4</td><td colspan="1" rowspan="1">31.5 μA</td><td colspan="1" rowspan="1">30.5 μA</td><td colspan="1" rowspan="1">30.1 μA</td></tr><tr><td colspan="1" rowspan="1">Clock</td><td colspan="3" rowspan="1">250 kHz MSI</td></tr><tr><td colspan="1" rowspan="1">Voltage regulator</td><td colspan="3" rowspan="1">Range 3</td></tr><tr><td colspan="1" rowspan="1">AHB/APB ratio</td><td colspan="1" rowspan="1">1/1</td><td colspan="1" rowspan="1">1/4</td><td colspan="1" rowspan="1">1/8</td></tr><tr><td colspan="1" rowspan="1">ULP/FWU</td><td colspan="3" rowspan="1">+/+</td></tr><tr><td colspan="1" rowspan="1">Baud rate</td><td colspan="3" rowspan="1">9600 Bd</td></tr><tr><td colspan="1" rowspan="1">SW used</td><td colspan="3" rowspan="1">DMA operation (Com DMA) with half buffer interrupt disabled</td></tr></table>

The power trace of the DMA operated example is different from the interrupt or blocking mode code execution. There is a peak in half of the transmission, caused by the half message interrupt. Then for half of the reply data reception the core stays in Sleep mode, it is only active during the second half. Different arrangement is of course possible.

# 7.1.8 ULP bit setting

The role of the ULP bit is to disconnect the internal voltage reference during Stop mode. The power analysis screen-shot in Figure 9 illustrates that this setting (black line) achieves lower power consumption in the Stop mode, but produces significant peaks when waking up (compared to green trace without ULP).

The microcontroller waiting for incoming data in the ULP mode consumes approximately 0,8 µA compared to almost 3 µA without ULP mode, but if it wakes from idle mode too frequently, the effect is negated by the voltage reference startup peaks.

![](images/6b2fe3309038b1ec95aa87e37f005c5ea1072b4a1cb8c493dcbb76e7dcea10f5.jpg)  
Figure 9. ULP bit effect

Table 12. Configurations - ULP bit effect   

<table><tr><td rowspan=1 colspan=1>Curve in Figure 9</td><td rowspan=1 colspan=1>Black</td><td rowspan=1 colspan=1>Green</td></tr><tr><td rowspan=1 colspan=1>Idle mode betweentransmissions</td><td rowspan=1 colspan=2>Stop</td></tr><tr><td rowspan=1 colspan=1>Debug interface</td><td rowspan=1 colspan=2>OFF</td></tr><tr><td rowspan=1 colspan=1>Current averageover phases 2, 3, and 4</td><td rowspan=1 colspan=1>74.5 μA</td><td rowspan=1 colspan=1>72.6 μA</td></tr><tr><td rowspan=1 colspan=1>Clock</td><td rowspan=1 colspan=2>500 kHz MSI</td></tr><tr><td rowspan=1 colspan=1>Voltage regulator</td><td rowspan=1 colspan=2>Range 3</td></tr><tr><td rowspan=1 colspan=1>AHB/APB ratio</td><td rowspan=1 colspan=2>1/1</td></tr><tr><td rowspan=1 colspan=1>ULP/FWU</td><td rowspan=1 colspan=1>+/+</td><td rowspan=1 colspan=1>-/-</td></tr><tr><td rowspan=1 colspan=1>Baud rate</td><td rowspan=1 colspan=2>9600 Bd</td></tr><tr><td rowspan=1 colspan=1>SW used</td><td rowspan=1 colspan=2>Interrupt operation (Com IT) with defines RXSTOP and TXSLEEP</td></tr></table>

# 7.1.9 Higher communication speed

While no advanced power saving features of the LPUART can be used on higher communication speeds (as compared with regular USART peripheral), still the LPUART simpler circuitry will result in lower power consumption (red line) compared to a full featured USART (black line), see Figure 10.

![](images/9be7ca1c386488b24a8d5e0f971a202ad0d46943715e128375a2018d07b36911.jpg)  
Figure 10. Operating at 57600 Bd

Table 13. Configurations - Higher communication speed   

<table><tr><td rowspan=1 colspan=1>Curve in Figure 10</td><td rowspan=1 colspan=1>Black</td><td rowspan=1 colspan=1>Red</td></tr><tr><td rowspan=1 colspan=1>Idle mode betweentransmissions</td><td rowspan=1 colspan=2>Stop</td></tr><tr><td rowspan=1 colspan=1>Debug interface</td><td rowspan=1 colspan=2>ON</td></tr><tr><td rowspan=1 colspan=1>Current averageover phases 2, 3, and 4</td><td rowspan=1 colspan=1>434.5 μA</td><td rowspan=1 colspan=1>415.2 μA</td></tr><tr><td rowspan=1 colspan=1>Clock</td><td rowspan=1 colspan=2>4 MHz MSI</td></tr><tr><td rowspan=1 colspan=1>Voltage regulator</td><td rowspan=1 colspan=2>Range 1</td></tr><tr><td rowspan=1 colspan=1>AHB/APB ratio</td><td rowspan=1 colspan=2>1/1</td></tr><tr><td rowspan=1 colspan=1>ULP/FWU</td><td rowspan=1 colspan=2>+/+</td></tr><tr><td rowspan=1 colspan=1>Baud rate</td><td rowspan=1 colspan=2>57600 Bd</td></tr><tr><td rowspan=1 colspan=1>SW used</td><td rowspan=1 colspan=1>Interrupt operation (Com IT)modified with USART on SYSCLK</td><td rowspan=1 colspan=1>Interrupt operation (Com IT)modified with LPUART on SYSCLK</td></tr></table>

Note:

The timing is slightly different for the 2 cases. This is a common problem when MSl is used to clock the LPUART peripheral. MSI clock is generally less precise than LSE or even HSI.

# 7.1.10 Wake-up from Stop mode on HSI

Another possible option at higher communication speeds is to exploit the feature of wake-up from Stop mode with peripheral clocked from the HSI clock (see Figure 11).

The HSI oscillator in Stop mode draws approximately the same current as the MSI in Sleep mode at 2 MHz. It is however more precise, and provides the core with more processing power in Run mode.

![](images/bfc1728302633e82869a29b9db4a1dd9e298332dadd8c4c144d827643b221a64.jpg)  
Figure 11. HSI vs. MSI at 4 MHz

Note that the timing with MSl is slightly off in the transmission phase. This is a common problem when MSI is used to clock the LPUART peripheral.

Table 14. Configurations - HSI vs. MSI   

<table><tr><td colspan="1" rowspan="1">Curve in Figure 11</td><td colspan="1" rowspan="1">Black</td><td colspan="1" rowspan="1">Red</td></tr><tr><td colspan="1" rowspan="1">Idle mode betweentransmissions</td><td colspan="1" rowspan="1">Stop</td><td colspan="1" rowspan="1">Sleep</td></tr><tr><td colspan="1" rowspan="1">Debug interface</td><td colspan="2" rowspan="1">OFF</td></tr><tr><td colspan="1" rowspan="1">Current averageover phases 2, 3, and 4</td><td colspan="1" rowspan="1">369.1 μA</td><td colspan="1" rowspan="1">329.7 μA</td></tr><tr><td colspan="1" rowspan="1">Clock</td><td colspan="1" rowspan="1">4 MHz HSI</td><td colspan="1" rowspan="1">4 MHz MSI</td></tr><tr><td colspan="1" rowspan="1">Voltage regulator</td><td colspan="2" rowspan="1">Range 3</td></tr><tr><td colspan="1" rowspan="1">AHB/APB ratio</td><td colspan="2" rowspan="1">1/1</td></tr><tr><td colspan="1" rowspan="1">ULP/FWU</td><td colspan="2" rowspan="1">+/+</td></tr><tr><td colspan="1" rowspan="1">Baud rate</td><td colspan="2" rowspan="1">57600 Bd</td></tr><tr><td colspan="1" rowspan="1">SW used</td><td colspan="2" rowspan="1">Interrupt operation (Com IT)</td></tr></table>

# 7.1.11 Voltage regulator settings

Setting lower core voltage level is an easy and straightforward way to save energy.

In Figure 12 it is demonstrated that even with HSl clock the run mode can be significantly more current-hungry just by changing the voltage.

Note that the setting has little or no influence on idle mode.

![](images/5fb330afec4e1d43e4fdd70f7d30847d118f73426dbe5c10dc5a1f2b65daeb75.jpg)  
Figure 12. Comparison between voltage regulator settings

Table 15. Configurations - Voltage regulator settings   

<table><tr><td colspan="1" rowspan="1">Curve in Figure 12</td><td colspan="1" rowspan="1">Red</td><td colspan="1" rowspan="1">Green</td><td colspan="1" rowspan="1">Black</td></tr><tr><td colspan="1" rowspan="1">Idle mode betweentransmissions</td><td colspan="3" rowspan="1">Sleep</td></tr><tr><td colspan="1" rowspan="1">Debug interface</td><td colspan="3" rowspan="1">OFF</td></tr><tr><td colspan="1" rowspan="1">Current averageover phases 2, 3, and 4</td><td colspan="1" rowspan="1">296.9 μA</td><td colspan="1" rowspan="1">300.8 μA</td><td colspan="1" rowspan="1">301.1 μA</td></tr><tr><td colspan="1" rowspan="1">Clock</td><td colspan="3" rowspan="1">4 MHz HSI</td></tr><tr><td colspan="1" rowspan="1">Voltage regulator</td><td colspan="1" rowspan="1">Range 3</td><td colspan="1" rowspan="1">Range 2</td><td colspan="1" rowspan="1">Range 1</td></tr><tr><td colspan="1" rowspan="1">AHB/APB ratio</td><td colspan="3" rowspan="1">1/1</td></tr><tr><td colspan="1" rowspan="1">Baud rate</td><td colspan="3" rowspan="1">9600 Bd</td></tr><tr><td colspan="1" rowspan="1">SW used</td><td colspan="3" rowspan="1">DMA operation (Com DMA)</td></tr></table>

# 7.1.12 GPIO pull-up

Figure 13 demonstrates the energetic costs of enabling the GPlO pull-up, in this case on the transmission line. Black line refers to internal GPlO pull-up enabled, red line to no pull-up.

It is clearly visible that no other phases are affected by extra power consumption.

![](images/3361c4b7ff53da57fb26b7f7fb8b752b17bbb8d6a11c4ad0dac2544a29cbaff7.jpg)  
Figure 13. GPIO internal pull-up

Table 1. Configurations - GPIO pull-up   

<table><tr><td colspan="1" rowspan="1">Curve in Figure 13</td><td colspan="1" rowspan="1">Black</td><td colspan="1" rowspan="1">Red</td></tr><tr><td colspan="1" rowspan="1">Idle mode betweentransmissions</td><td colspan="2" rowspan="1">Stop</td></tr><tr><td colspan="1" rowspan="1">Debug interface</td><td colspan="2" rowspan="1">OFF</td></tr><tr><td colspan="1" rowspan="1">Current averageover phases 2, 3, and 4</td><td colspan="1" rowspan="1">87.8 μA</td><td colspan="1" rowspan="1">66.6 μA</td></tr><tr><td colspan="1" rowspan="1">Clock</td><td colspan="2" rowspan="1">250 kHz MSI</td></tr><tr><td colspan="1" rowspan="1">Voltage regulator</td><td colspan="2" rowspan="1">Range 3</td></tr><tr><td colspan="1" rowspan="1">AHB/APB ratio</td><td colspan="2" rowspan="1">1/1</td></tr><tr><td colspan="1" rowspan="1">ULP/FWU</td><td colspan="2" rowspan="1">+/+</td></tr><tr><td colspan="1" rowspan="1">Baud rate</td><td colspan="2" rowspan="1">9600 Bd</td></tr><tr><td colspan="1" rowspan="1">SW used</td><td colspan="1" rowspan="1">Interrupt operation (Com IT) modifiedwith Tx line internal PULL UP</td><td colspan="1" rowspan="1">Interrupt operation (Com IT)</td></tr></table>

# 7.2

# Measurements on STM32L476 Nucleo board

# 7.2.1

# Three approaches at a glance

In this section the advantages and disadvantages of the three basic approaches (DMA, Polling and Interrupt) to govern the communication will be compared.

Looking at Figure 14, the DMA one wins this comparison, but, if the pause before reply had been longer, it would have lost by a wide margin. Polling would then appear as the most efficient, but it assumes that a single task be processed. Interrupt seems to solve this problem, but at 200 kHz system clock it has no margin to do so (judging by the negligible time spent in Sleep between bytes).

While DMA and Polling driven communications are still operational at 100 kHz minimal MSI setting, Interrupt operation is not.

![](images/3a14f2811b60129c5b8e1a731d57c28be8e41a60bc6ec6c21bfa83ea74400893.jpg)

Figure 14. Comparison of three different approaches to manage communication   
Table 17. Configurations - Managing communication   

<table><tr><td colspan="1" rowspan="1">Curve in Figure 14</td><td colspan="1" rowspan="1">Black</td><td colspan="1" rowspan="1">Red</td><td colspan="1" rowspan="1">Green</td></tr><tr><td colspan="1" rowspan="1">Idle mode</td><td colspan="2" rowspan="1">Stop2</td><td colspan="1" rowspan="1">Sleep</td></tr><tr><td colspan="1" rowspan="1">Debug interface</td><td colspan="3" rowspan="1">OFF</td></tr><tr><td colspan="1" rowspan="1">Current averageover phases 2, 3, and 4</td><td colspan="1" rowspan="1">64.1 μA</td><td colspan="1" rowspan="1">51.6 μA</td><td colspan="1" rowspan="1">49.4 μA</td></tr><tr><td colspan="1" rowspan="1">Clock</td><td colspan="3" rowspan="1">200 MHz MSI</td></tr><tr><td>Voltage regulator</td><td colspan="3">Low-power run</td></tr><tr><td>AHB/APB ratio</td><td colspan="3">1/1</td></tr><tr><td>Baud rate</td><td colspan="3">9600 Bd</td></tr><tr><td>SW used</td><td>Interrupt driven (Com IT) with Sleep between bytes</td><td>POLL operation with TXSLEEP and RXSLEEP defines</td><td>DMA stream (Com DMA) with half buffer interruptions</td></tr></table>

# 7.2.2 Simple polling mode on low core frequency

After reset the MCU initializes with MSI oscillator running at 4 MHz, a compromise between low-power consumption and acceptable communication speed. A lower frequency is needed to establish a communication link using LPUART. Note that at this pace an interrupt from different peripheral can disrupt the ongoing communication.

Figure 15 shows the consumption profile using different low speeds of the MSl oscillator.

![](images/ebc529153ab67e8aa462761eac98bb015bacc105a4ba89710a2dc3d3744e56d2.jpg)  
Figure 15. Polling communication at minimum settings

Table 18. Configurations - Polling   

<table><tr><td rowspan=1 colspan=1>Curve in Figure 15</td><td rowspan=1 colspan=1>Black</td><td rowspan=1 colspan=1>Red</td><td rowspan=1 colspan=1>Green</td></tr><tr><td rowspan=1 colspan=1>Idle mode</td><td rowspan=1 colspan=3>Stop2</td></tr><tr><td rowspan=1 colspan=1>Debug interface</td><td rowspan=1 colspan=3>OFF</td></tr><tr><td rowspan=1 colspan=1>Current averageover phases 2, 3, and 4</td><td rowspan=1 colspan=1>81.2 μA</td><td rowspan=1 colspan=1>49.7 μA</td><td rowspan=1 colspan=1>44.9 μA</td></tr><tr><td rowspan=1 colspan=1>Clock</td><td rowspan=1 colspan=1>800 kHz MSI</td><td rowspan=1 colspan=1>200 kHz MSI</td><td rowspan=1 colspan=1>100 kHz MSI</td></tr><tr><td rowspan=1 colspan=1>Voltage regulator</td><td rowspan=1 colspan=3>Low-power run</td></tr><tr><td rowspan=1 colspan=1>AHB/APB ratio</td><td rowspan=1 colspan=3>1/1</td></tr><tr><td rowspan=1 colspan=1>Baud rate</td><td rowspan=1 colspan=3>9600 Bd</td></tr><tr><td rowspan=1 colspan=1>SW used</td><td rowspan=1 colspan=3>POLL operation with TXSLEEP and RXSLEEP</td></tr></table>

# 7.2.3 The role of voltage regulator settings

An important step towards lower power consumption is the use of regulator settings appropriate to the actual core frequency. Speed of 2 MHz (MSI Range 5) is the top setting supported by the Low-power run mode. Remaining connected to the main regulator (in Figure 16 this is emphasized by using it even during Sleep) a lot of energy is wasted.

![](images/e4635ead10a6d5c06fa6babfa08313c71923499b664a114c327a407f16d588bd.jpg)  
Figure 16. Voltage regulator settings

Table 19. Configurations - Voltage regulator settings   

<table><tr><td rowspan=1 colspan=1>Curve in Figure 16</td><td rowspan=1 colspan=1>Black</td><td rowspan=1 colspan=1>Red</td><td rowspan=1 colspan=1>Green</td></tr><tr><td rowspan=1 colspan=1>Idle mode</td><td rowspan=1 colspan=3>Sleep</td></tr><tr><td rowspan=1 colspan=1>Debug interface</td><td rowspan=1 colspan=3>OFF</td></tr><tr><td rowspan=1 colspan=1>Current averageover phases 2, 3, and 4</td><td rowspan=1 colspan=1>244.4 μA</td><td rowspan=1 colspan=1>215.5 μA</td><td rowspan=1 colspan=1>139.1 μA</td></tr><tr><td rowspan=1 colspan=1>Clock</td><td rowspan=1 colspan=3>2 MHz MSI</td></tr><tr><td rowspan=1 colspan=1>Voltage regulator</td><td rowspan=1 colspan=1>Range 1</td><td rowspan=1 colspan=1>Range 2</td><td rowspan=1 colspan=1>Low-power run</td></tr><tr><td rowspan=1 colspan=1>AHB/APB ratio</td><td rowspan=1 colspan=3>1/1</td></tr><tr><td rowspan=1 colspan=1>Baud rate</td><td rowspan=1 colspan=3>9600 Bd</td></tr><tr><td rowspan=1 colspan=1>SW used</td><td rowspan=1 colspan=3>DMA operation (Com DMA) with half buffer interrupt disabled</td></tr></table>

# 7.2.4 Idle modes compared

Microcontrollers of the L4 series feature three basic Idle modes, namely Sleep, Stop1 and Stop2.

Note, in Figure 17, how Stop 2 minimizes the power consumption drastically, and how waking up produces a notable peak. This causes the Stop1 to outperform Stop2 in measured case of approximately 10 ms of ldle. Main reason of this peak is the fact that the Stop2 mode cannot be entered directly from the Low-power mode. Main regulator must be ON when entering and leaving the Stop2.

![](images/b41acf1623db750fc8a73ecc2079458d21e83714662bf81a63393b40e0d21239.jpg)  
Figure 17. Comparison of Idle modes

Table 20. Configurations - Idle modes   

<table><tr><td rowspan=1 colspan=1>Curve in Figure 17</td><td rowspan=1 colspan=1>Black</td><td rowspan=1 colspan=1>Red</td><td rowspan=1 colspan=1>Green</td></tr><tr><td rowspan=1 colspan=1>Idle mode</td><td rowspan=1 colspan=1>Stop2</td><td rowspan=1 colspan=1>Sleep</td><td rowspan=1 colspan=1>Stop1</td></tr><tr><td rowspan=1 colspan=1>Debug interface</td><td rowspan=1 colspan=3>OFF</td></tr><tr><td rowspan=1 colspan=1>Current averageover phases 2, 3, and 4</td><td rowspan=1 colspan=1>73.2 μA</td><td rowspan=1 colspan=1>75.6 μA</td><td rowspan=1 colspan=1>72.8 μA</td></tr><tr><td rowspan=1 colspan=1>Clock</td><td rowspan=1 colspan=3>400 kHz MSI</td></tr><tr><td rowspan=1 colspan=1>Voltage regulator</td><td rowspan=1 colspan=3>Low-power run</td></tr><tr><td rowspan=1 colspan=1>AHB/APB ratio</td><td rowspan=1 colspan=3>1/1</td></tr><tr><td rowspan=1 colspan=1>Baud rate</td><td rowspan=1 colspan=3>9600 Bd</td></tr><tr><td rowspan=1 colspan=1>SW used</td><td rowspan=1 colspan=3>IT operation (Com IT) with Rx Stop</td></tr></table>

# 7.2.5 Use of MSI PLL-mode for higher speeds

Higher communication speeds require an LPUART clock source different from LSE.

System clock driven by MSI up to 48 MHz can be used, configured in PLL-mode, in which it is auto-calibrated using the LSE. An obvious but not efficient solution is to use the HSI clock with dividers (such as the AHB).

HSE external source is another option. The measurement shown in Figure 18 compares the HSI configurations using the MSI PLL-mode to get lower clock frequency and lower consumption.

![](images/7cc74d4b06688ed6102d1440a69c2ce498d613ba9dec7d8aafa362f6871bfc7b.jpg)  
Figure 18. HSI and PLL current consumption

Table 21. Configurations - HSI and PLL   

<table><tr><td colspan="1" rowspan="1">Curve in Figure 18</td><td colspan="1" rowspan="1">Black</td><td colspan="1" rowspan="1">Green</td><td colspan="1" rowspan="1">Red</td></tr><tr><td colspan="1" rowspan="1">Idle mode</td><td colspan="3" rowspan="1">Sleep</td></tr><tr><td colspan="1" rowspan="1">Debug interface</td><td colspan="3" rowspan="1">OFF</td></tr><tr><td colspan="1" rowspan="1">Current averageover phases 2, 3, and 4</td><td colspan="1" rowspan="1">1.05 mA</td><td colspan="1" rowspan="1">0.536 mA</td><td colspan="1" rowspan="1">0.250 mA</td></tr><tr><td colspan="1" rowspan="1">Clock</td><td colspan="2" rowspan="1">HSI16</td><td colspan="1" rowspan="1">MSI auto-callibrated using LSE;Sysclk 2 MHz</td></tr><tr><td colspan="1" rowspan="1">Voltage regulator</td><td colspan="2" rowspan="1">Range2</td><td colspan="1" rowspan="1">Low-power run</td></tr><tr><td colspan="1" rowspan="1">AHB/APB ratio</td><td colspan="1" rowspan="1">1/1</td><td colspan="1" rowspan="1">8/1</td><td colspan="1" rowspan="1">1/1</td></tr><tr><td colspan="1" rowspan="1">Baud rate</td><td colspan="3" rowspan="1">57600 Bd</td></tr><tr><td colspan="1" rowspan="1">SW used</td><td colspan="3" rowspan="1">DMA operation (Com DMA) with half buffer interrupt disabled</td></tr></table>

# 7.2.6 Using two oscillators

To use Stop modes at higher communication speed, the LPUART peripheral must be clocked from the HSI16 source. It is not necessary to reuse the same 16 MHz clock for the Sysclk, especially if this speed is considered too high. At 57600 Bd it is possible to use the 2 MHz frequency from MSI, saving a considerable amount of energy.

![](images/8bef5b11ec16fd1d49f23b6add2238efe61dcbc7db959dbc738a4276d47ab460.jpg)  
Figure 19. Using Stop with 57600 Bd speed

Table 22. Configurations - Stop with 56700 Bd speed   

<table><tr><td colspan="1" rowspan="1">Curve in Figure 19</td><td colspan="1" rowspan="1">Black</td><td colspan="1" rowspan="1">Green</td></tr><tr><td colspan="1" rowspan="1">Idle mode</td><td colspan="2" rowspan="1">Stop2</td></tr><tr><td colspan="1" rowspan="1">Debug interface</td><td colspan="2" rowspan="1">OFF</td></tr><tr><td colspan="1" rowspan="1">Current averageover phases 2, 3, and 4</td><td colspan="1" rowspan="1">480 μA</td><td colspan="1" rowspan="1">321 μA</td></tr><tr><td colspan="1" rowspan="1">System clock</td><td colspan="1" rowspan="1">HSI16</td><td colspan="1" rowspan="1">MSI auto-callibrated using LSE;Sysclk 2 MHz</td></tr><tr><td colspan="1" rowspan="1">Voltage regulator</td><td colspan="1" rowspan="1">Range2</td><td colspan="1" rowspan="1">Low-power run</td></tr><tr><td colspan="1" rowspan="1">AHB/APB ratio</td><td colspan="1" rowspan="1">8/1</td><td colspan="1" rowspan="1">1/1</td></tr><tr><td colspan="1" rowspan="1">Baud rate</td><td colspan="2" rowspan="1">57600 Bd</td></tr><tr><td colspan="1" rowspan="1">SW used</td><td colspan="1" rowspan="1">IT operation (Com IT) with Rx Stop</td><td colspan="1" rowspan="1">IT operation (Com IT)</td></tr></table>

Note:

For Stop2 mode the LPRUN must be exited.

# 7.3 Measurement on the STM32H743 Nucleo144 board

The reference manual describes how to use the D3 domain to minimize power consumption when communicating using the LPUART. This is the only case interesting in the context of this application note.

This MCU has non-negligible static power consumption in Stop mode, for the details see the tables in the datasheet.

Since there is only one configuration presented in example, there is no measurement comparison.

# 7.4 STM32WB55 Nucleo board testing

This product has several similarities with STM32L476, but it is very different in purpose and application, thanks to its RF part, which is practically unusable with low power regulator. For STM32WBxx devices the embedded SMPS is more useful.

The example covers settings different from the other products. The STM32WB55 based project also shows how the DMA and DMAMUX must be configured (this setup is very different vs. the STM32L476).

It is also important to keep in mind the device embeds two CPU cores. In the example project the second core (Cortex® M0+, responsible for the RF stack) is shut down, but in real applications this is probably not be the case.

![](images/1ce4970fdd592409fbc96b788bffe073b7543b087c1bd5affdd8f88d4f742ada.jpg)  
Figure 20. Comparison of three different approaches to manage communication

Table 23. Configurations - Managing communication   

<table><tr><td rowspan=1 colspan=1>Curve in Figure 20</td><td rowspan=1 colspan=1>Black</td><td rowspan=1 colspan=1>Red</td><td rowspan=1 colspan=1>Green</td></tr><tr><td rowspan=1 colspan=1>Idle mode between transmissions</td><td rowspan=1 colspan=1>Sleep</td><td rowspan=1 colspan=1>Stopo</td><td rowspan=1 colspan=1>Stop2</td></tr><tr><td rowspan=1 colspan=1>Debug interface</td><td rowspan=1 colspan=3>OFF</td></tr><tr><td rowspan=1 colspan=1>Current averageover phases 2, 3, and 4</td><td rowspan=1 colspan=1>96 μA</td><td rowspan=1 colspan=1>52 μA</td><td rowspan=1 colspan=1>50 μA</td></tr><tr><td rowspan=1 colspan=1>Clock</td><td rowspan=1 colspan=3>800 kHz MSI</td></tr><tr><td rowspan=1 colspan=1>Voltage regulator</td><td rowspan=1 colspan=3>Range2(1)</td></tr><tr><td rowspan=1 colspan=1>AHB/APB ratio</td><td rowspan=1 colspan=3>1/1</td></tr><tr><td rowspan=1 colspan=1>Baud rate</td><td rowspan=1 colspan=3>9600 Bd</td></tr><tr><td rowspan=1 colspan=1>SW used</td><td rowspan=1 colspan=1>DMA</td><td rowspan=1 colspan=1>Polling</td><td rowspan=1 colspan=1>Interrupt</td></tr></table>

Other STM32WB devices usually do not feature selectable voltage regulator ranges.

# 7.5 STM32G474 Nucleo board testing

This device is not low-power oriented, even if it embeds the LPUART peripheral. It features a low-power regulator, but it does not have the MSl clock and the best way to make use of the Low-power run without HSE external clock is to use the AHB clock prescaler on the HSI.

![](images/13eccdab3146d8b7d1d96fc6d600b34f2520865540ab3846d701c1d72ca352e5.jpg)  
Figure 21. Interrupt operation with three different core clocks

Table 24. Influence of the AHB prescaler   

<table><tr><td rowspan=1 colspan=1>Curve in Figure 21</td><td rowspan=1 colspan=1>Red</td><td rowspan=1 colspan=1>Black</td><td rowspan=1 colspan=1>Green</td></tr><tr><td rowspan=1 colspan=1>Idle mode between transmissions</td><td rowspan=1 colspan=3>Stop1</td></tr><tr><td rowspan=1 colspan=1>SWD interface</td><td rowspan=1 colspan=3>OFF</td></tr><tr><td rowspan=1 colspan=1>Current averageover phases 2, 3, and 4</td><td rowspan=1 colspan=1>914 μA</td><td rowspan=1 colspan=1>858 μA</td><td rowspan=1 colspan=1>838 μA</td></tr><tr><td rowspan=1 colspan=1>Clock</td><td rowspan=1 colspan=3>16 MHz HSI</td></tr><tr><td rowspan=1 colspan=1>Voltage regulator</td><td rowspan=1 colspan=3>Low-power</td></tr><tr><td rowspan=1 colspan=1>AHB/APB ratio</td><td rowspan=1 colspan=1>1/4</td><td rowspan=1 colspan=1>1/8</td><td rowspan=1 colspan=1>1/16</td></tr><tr><td rowspan=1 colspan=1>Baud rate</td><td rowspan=1 colspan=3>9600 Bd</td></tr><tr><td rowspan=1 colspan=1>SW used</td><td rowspan=1 colspan=3>Interrupt</td></tr></table>

There is no prescaler divider by 32 available. On the divide by 64 setting the example code is barely able to receive the data without overrun. A more optimized code could be able to keep up with this data rate, but some margin is needed for reliability and robustness.

# 7.6 STM32U575 Nucleo 144 board testing

There is no significant difference in configuration and capabilities of the polling or interrupt driven mode. The DMA operation can take advantage of the LPBAM mode. In autonomous mode the LPDMA and LPUART can work even with CPU in Stop mode, thanks to a hardware subsystem embedded in the STM32 microcontroller.

The autonomous mode is rich in features and settings. The additional effort to set and optimize it is paid off by the performance enhancement.

CubeMX includes a tool that helps setting up the code servicing the LPBAM library and hardware. An LPTIM is used to trigger the LPDMA when the CPU is in Stop mode.

![](images/7d615c5ad67adc26432e7636eb6dd31f3876a328dd22eb0473931599da6d27eb.jpg)  
Figure 22. Power consumption for different operation modes

In Figure 22 the system communicates using different DMA set-ups at 9600 Bd to facilitate the comparison with other measurements. The black line demonstrates the benefit of using the LPDMA in Stop mode (without any further changes), while the green line demonstrates complete optimization using the LPBAM library. The autonomous operation in Stop mode is not limited by LSE, hence the advantage is significant even at higher communication speeds.

Table 25. Comparison of different operation modes   

<table><tr><td rowspan=1 colspan=1>Curve in Figure 22</td><td rowspan=1 colspan=1>Red</td><td rowspan=1 colspan=1>Black</td><td rowspan=1 colspan=1>Green</td></tr><tr><td rowspan=1 colspan=1>Power mode during transmissions</td><td rowspan=1 colspan=1>Sleep</td><td rowspan=1 colspan=1>Stop2</td><td rowspan=1 colspan=1>Stop2 + LPBAM + SMPS</td></tr><tr><td rowspan=1 colspan=1>SWD interface</td><td rowspan=1 colspan=3>OFF</td></tr><tr><td rowspan=1 colspan=1>Current average over phases 2, 3, and 4</td><td rowspan=1 colspan=1>660 μA</td><td rowspan=1 colspan=1>110 μA</td><td rowspan=1 colspan=1>&lt; 10 μA(1)</td></tr><tr><td rowspan=1 colspan=1>System clock</td><td rowspan=1 colspan=3>4 MHz MSIS</td></tr><tr><td rowspan=1 colspan=1>Kernel clock</td><td rowspan=1 colspan=2>100 kHz MSIK</td><td rowspan=1 colspan=1>4 MHz MSIK</td></tr><tr><td rowspan=1 colspan=1>Voltage regulator</td><td rowspan=1 colspan=3>Range 2</td></tr><tr><td rowspan=1 colspan=1>Baud rate</td><td rowspan=1 colspan=3>9600 Bd</td></tr></table>

When using the same set-up of other cases, the SMPS makes the measurement less precise. With a different set-up power consumption as low as 7.2 µA has been measured.

# 7.7 STM32U073RC Nucleo 64 board testing

STM32U0 MCUs can run a code written for STM32L0 devices with few changes, but with lower dynamic power consumption.

The STM32U0 products features a new version of the LPUART interface, with two FIFOs (transmit and receive) with 8-byte capacity. The FIFOs are easily configured using CubeMX SW, fully supported by the Cube HAL.

Using this buffer, the CPU does not need to wake up for each byte, so it can spend more time in low power modes. This is clearly visible in Figure 23, where the red and black curves refer to, respectively, FIFO enabled and FIFO disabled.

![](images/91cbc487f88720819d176686baaac67bfff14daa1e6f5967d5d37f62c1f1a49b.jpg)  
Figure 23. Power consumption comparison (FIFO ON/OFF)

In this measurement the system communicates at 9600 Bd using 800 kHz MSI clock, to facilitate the comparison.

Table 26. Comparison of different operation modes   

<table><tr><td rowspan=1 colspan=1>Curve in Figure 23</td><td rowspan=1 colspan=1>Red</td><td rowspan=1 colspan=1>Black</td></tr><tr><td rowspan=1 colspan=1>Power mode during transmission</td><td rowspan=1 colspan=2>Sleep</td></tr><tr><td rowspan=1 colspan=1>FIFO</td><td rowspan=1 colspan=1>ON</td><td rowspan=1 colspan=1>OFF</td></tr><tr><td rowspan=1 colspan=1>Current average over phases 2, 3, and 4</td><td rowspan=1 colspan=1>60 μA</td><td rowspan=1 colspan=1>66 μA</td></tr><tr><td rowspan=1 colspan=1>System clock</td><td rowspan=1 colspan=2>800 kHz MSI</td></tr><tr><td rowspan=1 colspan=1>Voltage regulator</td><td rowspan=1 colspan=2>Low power (LPR)</td></tr><tr><td rowspan=1 colspan=1>Baud rate</td><td rowspan=1 colspan=2>9600 Bd</td></tr></table>

# 8 Example project

An example code X-CUBE-LPUART is supplied with this document, demonstrating the usage of the different configurations (most of them are switchable using the defines section in the main.c source file).

Two boards are needed to replicate the measurements, namely a primary board and a repeater, loaded with DMA FW built with BOARD2 option.

Measurements of consumption are carried out on the primary board, not on the repeater.

The example has been developed and tested with Nucleo boards.

# 8.1 HW setup

Just cross connect Tx pins with Rx pins on the opposite board using two wires. JP6 pins of Nucleo-64 or JP5 pins of Nucleo-144 can be used to monitor the power consumption. It is possible to combine different Nucleo boards, keeping in mind that the Rx and Tx pins have different positions.

Most boards require no physical modification, only for STM32H7 Nucleo144 solder bridges SB2 and SB125 have been removed before measurement.

# 8.2 Configuring the example

Various features and working modes of the example FW can be configures using following preprocessor defines:

• DEBUG_OFF: disables the SWD debug capability on port A and error checking   
• BOARD2: configures the SW as the repeater board (only present in DMA version)   
• UI: enables user interface (it is impossible to take correct power consumption readings with buttons and LEDs enabled)   
• BD_SPEED: sets the communication baud speed   
• ST: configures Stop mode when waiting for reception (where applicable)   
• STOP2: configures Stop2 Low-power mode when waiting for reception (where applicable)   
• LPRUN: configures the Low-power run mode (where applicable)   
• PWR_CR_VOS_CONF: configures the main power regulator (lowest available is the default)   
• TXSLEEP: Sleep mode configured between transmitted bytes   
• RXSLEEP: Sleep mode configured between received bytes   
• RXSTOP: Stop mode configured between received bytes (available in interrupt mode) HSI: sets the system clock to HSI mode. MSI is default where available   
• RCC_MSIRANGE_SET: if HSI is disabled, sets the MSI speed range.

# 8.3 Example operation

It is recommended to first load and execute firmware in board 1 (the measured one), then prepare the repeater. The measurement cycle can be then started, by pressing the user button on the board 1.

The boards start exchanging messages in an endless loop. In case of communication error and debugging enabled, the loop is halted. With Ul option the board flashes the LED to indicate activity. This has significant influence on the current consumption, and, for all power measurements, disables the UI (LED blinking) on board 1.

# Conclusion

There is no single optimal way of configuring the LP UART with respect to lowest possible power consumption.

Depending on the application and the operational constraints, a lot of parameters have to be taken into account, the general guidelines can be summarized as follows:

use lower frequencies; • use lower voltages; keep the MCU as much as possible in low-power modes.

Optimized software is also crucial part of the whole low-power solution. It is advisable to go through the same test with firmware compiled at different optimization levels.

# 10 Revision history

Table 27. Document revision history   

<table><tr><td rowspan=1 colspan=1>Date</td><td rowspan=1 colspan=1>Revision</td><td rowspan=1 colspan=1>Changes</td></tr><tr><td rowspan=1 colspan=1>22-Apr-2015</td><td rowspan=1 colspan=1>1</td><td rowspan=1 colspan=1>Initial release.</td></tr><tr><td rowspan=1 colspan=1>26-May-2015</td><td rowspan=1 colspan=1>2</td><td rowspan=1 colspan=1>Updated Introduction with addition of software X-CUBE-LPUART.Updated Section 8: Example project.</td></tr><tr><td rowspan=1 colspan=1>12-Oct-2015</td><td rowspan=1 colspan=1>3</td><td rowspan=1 colspan=1>Introduced STM32L4 series.Updated Introduction, Section 3.1: Clock subsystem, Section 3.3:Comparison with USART peripheral, Section 5.2: GPIO configuration,Section 5.4.1: Use of Stop and Sleep modes, Section 5.4.2: Run timeconfiguration, Section 6.2: Dropped bytes, Section 8: Example projectand its subsections.Updated tables 2 to 16.Updated Figure 8: Three different settings of peripheral clock divider andFigure 12: Comparison between voltage regulator settings.Added Section 2.1: Comparison between L0 and L4 series and itssubsections, Section 5.1: Execution from SRAM, Section 7.2:Measurements on STM32L476 Nucleo board and its subsections.</td></tr><tr><td rowspan=1 colspan=1>04-Jun-2019</td><td rowspan=1 colspan=1>4</td><td rowspan=1 colspan=1>Introduced STM32G0, STM32G4, STM32H7 and STM32WB series.Updated document title, Introduction, Section 3: Summary of featuresand its subsections, Section 4.3: DMA mode, Section 5.3: Clockconfiguration, Section 5.3.1: Clock prescalers, Section 5.4.1: Use ofStop and Sleep modes, Section 5.4.2: Run time configuration, Section 8:Example project and Section 9: Conclusion.Updated Table 2: List of acronyms and Table 4: Clock options.Added Table 1: Applicable products and software, Section 5.4.3:STM32H7 core domain sections, Section 7.3: Measurement on theSTM32H743 Nucleo144 board, Section 7.4: STM32WB55 Nucleo boardtesting and Section 7.5: STM32G474 Nucleo board testing.Minor text edits across the whole document.</td></tr><tr><td rowspan=1 colspan=1>28-Nov-2019</td><td rowspan=1 colspan=1>5</td><td rowspan=1 colspan=1>Introduced STM32L4+ and STM32L5 series.Updated Introduction, Section 4.3: DMA mode and Section 7: Powerconsumption comparison.Updated Table 1: Applicable products and software and Table 4: Clockoptions.Added Section 5.4.4: SMPS and Section 5.5: Cache memory.Minor text edits across the whole document.</td></tr><tr><td rowspan=1 colspan=1>29-Mar-2022</td><td rowspan=1 colspan=1>6</td><td rowspan=1 colspan=1>Updated Introduction, Section 3.1.1: MSI clock, Section 3.1.2: HSI clock,Section 3.2: Power management, Section 3.3: Comparison with USARTperipheral, Section 4.3: DMA mode, Section 5.1: Execution from SRAM,Section 5.3: Clock configuration, Section 5.4.2: Run time configuration,and Section 5.4.4: SMPS.Updated Table 1: Applicable products and software, Table 2: List ofacronyms and added footnote to Table 23: Configurations - Managingcommunication.Added Section 7.6: STM32U575 Nucleo 144 board testing.</td></tr></table>

Table 27. Document revision history   

<table><tr><td rowspan=1 colspan=1>Date</td><td rowspan=1 colspan=1>Revision</td><td rowspan=1 colspan=1>Changes</td></tr><tr><td rowspan=1 colspan=1>17-Nov-2022</td><td rowspan=1 colspan=1>7</td><td rowspan=1 colspan=1>Updated Introduction, Section 3.1.1: MSI clock, Section 3.1.2: HSI clock,Section 3.1.4: CSI clock, Section 3.2: Power management, Section 4.3:DMA mode, Section 5.2: GPIO configuration, and Section 5.4.3:STM32H7 core domain sections.Updated Table 1: Applicable products and software and Table 21:Configurations - HSI and PLL.Added Section 2: Reference documents.Minor text edits across the whole document.</td></tr><tr><td rowspan=1 colspan=1>19-Mar-2024</td><td rowspan=1 colspan=1>8</td><td rowspan=1 colspan=1>Updated document title, Section 2: Reference documents, Section 3.1.1:MSI clock, Section 3.2: Power management, Section 5.3: Clockconfiguration, and Section 5.4.2: Run time configuration.Document scope extended to STM32U0 series, hence updated Table 1:Applicable products and software.Added Section 7.7: STM32U073RC Nucleo 64 board testing.Minor text edits across the whole document.</td></tr><tr><td rowspan=1 colspan=1>20-Oct-2024</td><td rowspan=1 colspan=1>9</td><td rowspan=1 colspan=1>Document scope extended to STM32U3 series, hence updated Table 1:Applicable products and software.Updated Section 2: Reference documents, Section 3.1.1: MSI clock,Section 3.1.2: HSI clock, Section 3.2: Power management, Section 5.3:Clock configuration, Section 5.4.2: Run time configuration, andSection 5.4.4: SMPS.</td></tr></table>

# IMPORTANT NOTICE  READ CAREFULLY

acknowledgment.

the design of purchasers' products.

No license, express or implied, to any intellectual property right is granted by ST herein.

or service names are the property of their respective owners.

I