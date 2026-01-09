# How to wake up an STM32 microcontroller from low-power mode with the USART or the LPUART

# Introduction

TveyiARTneowiv STM32 microcontroller MCU) of the series listed below is in low-power mode, and theAPB clock is disabled.

Table 1. Applicable products   

<table><tr><td>Type</td><td>Products</td></tr><tr><td rowspan="7">Microcontroller</td><td>STM32C0 series</td></tr><tr><td>STM32F0 series, STM32F3 series</td></tr><tr><td>STM32G0 series, STM32G4 series</td></tr><tr><td>STM32H5 series, STM32H7 series</td></tr><tr><td>STM32L0 series, STM32L4 series, STM32L4+ series, STM32L5 series</td></tr><tr><td>STM32N6 series</td></tr><tr><td>STM32U0 series, STM32U3 series, STM32U5 series</td></tr><tr><td>STM32WB series, STM32WB0 series, STM32WBA series</td></tr></table>

# 1 General information

# Note:

This application note applies to the ST32 Series microcontrollers that are Arm® Cortex® core-based devics.   
Arm is a registered trademark of Arm Limited (or its subsidiaries) in the US and/or elsewhere.

# 2 STM32 low-power modes

The table below summarizes the low-power modes, from which the STM32 MCU can be woken up with the USART or the LPUART.

Table 2. STM32 low-power modes   

<table><tr><td rowspan=2 colspan=1>STM32 series</td><td rowspan=1 colspan=2>Mode from which the STM32 can be woken up by</td></tr><tr><td rowspan=1 colspan=1>USART</td><td rowspan=1 colspan=1>LPUART</td></tr><tr><td rowspan=1 colspan=1>STM32C0</td><td rowspan=1 colspan=1>Stop mode</td><td rowspan=2 colspan=1>N/A</td></tr><tr><td rowspan=1 colspan=1>STM32F0, STM32F3</td><td rowspan=1 colspan=1>Stop mode (with the main regulator in Run modeor in low-power mode)</td></tr><tr><td rowspan=1 colspan=1>STM32G0, STM32G4, STM32WBA</td><td rowspan=1 colspan=2>Stop 0 and Stop 1 modes</td></tr><tr><td rowspan=1 colspan=1>STM32H5, STM32H7, STM32N6</td><td rowspan=1 colspan=2>Stop mode</td></tr><tr><td rowspan=1 colspan=1>STM32L0</td><td rowspan=1 colspan=2>Stop mode (with the main regulator in Run mode or in low-power mode, range 1/2/3)</td></tr><tr><td rowspan=1 colspan=1>STM32L4, STM32L4+, STM32L5,STM32U5, STM32WB, STM32U0,SSTM32U3</td><td rowspan=1 colspan=1>Stop 0 and Stop 1 modes</td><td rowspan=1 colspan=1>Stop 0, Stop 1, and Stop 2 modes</td></tr><tr><td rowspan=1 colspan=1>STM32WB0</td><td rowspan=1 colspan=2>DEEPSTOP mode</td></tr></table>

# 3 USART/LPUART wake-up features

# 3.1 Dual-clock domain

The USART or LPUART is able to wake up the MCU from a low-power mode only when the peripheral supports the dual-clock domain. The USART or LPUART can be clocked by a clock independent from the APB clock. This clock can be either the HSI, MSI, or LSE clock depending on the device.

The USART r LUART can then receive data even  clock isdisableand the MCU s in low-powemode.

# 3.2 USART/LPUART wake-up sources

interrupts, refer to the USART and LPUART interrupts section in the product reference manual.

To enable the USART or LPUART to wake up the MCU from low-power mode, the UESM bit must be set in USART/LPUART_CR1 before entering a low-power mode.

# How the USART/PLUART wakes up the STM32

# 4.1

# Wake-up from a low-power mode when the internal oscillator is off

If the TM32 MCU is n  low-powemode, and the interal scilor clock used  USART/LPUART kerelclock is switched off, when a falling edge on the USART/LPUART receive line is detected, the USART or LPUART cco

If the wake-up event is verified, the STM32 MCU wakes up from low-power mode, and the data reception goes on normally.

I akno elclocii C woken up and remains in low-power mode, and the kernel clock request is released.

Table 3. STM32 internal oscillators   

<table><tr><td rowspan=2 colspan=1>STM32 series</td><td rowspan=1 colspan=3>Internal clock supported</td><td rowspan=2 colspan=1>LPBAM supported(1)</td></tr><tr><td rowspan=1 colspan=1>MSI</td><td rowspan=1 colspan=1>HSI</td><td rowspan=1 colspan=1>CSI</td></tr><tr><td rowspan=1 colspan=1>STM32C0, STM32F0, STM32F3, STM32G0,STM32G4, STM32L4, STM32L4+, STM32L5,STM32WBA</td><td rowspan=1 colspan=1>No</td><td rowspan=2 colspan=1></td><td rowspan=2 colspan=1>No</td><td rowspan=4 colspan=1>No</td></tr><tr><td rowspan=1 colspan=1>STM32WB0</td><td rowspan=1 colspan=1></td></tr><tr><td rowspan=1 colspan=1>STM32H5, STM32H7</td><td rowspan=2 colspan=1>Yes</td><td rowspan=3 colspan=1>Yes</td><td rowspan=1 colspan=1>Yes</td><td rowspan=1 colspan=1></td></tr><tr><td rowspan=1 colspan=1>STM32L0, STM32N6, STM32WB, STM32U0,ST32U3</td><td rowspan=1 colspan=1>No</td></tr><tr><td rowspan=1 colspan=1>STM32U5</td><td rowspan=1 colspan=1></td><td rowspan=1 colspan=1></td><td rowspan=1 colspan=1>Yes</td></tr></table>

1. LPBAM means low-power background autonomous mode.

The figures below show an example of a wake-up event programmed to an "address match detection" (see Section 5.2 for details on twuusART and twuLPUART).

![](images/72162274bc32b09549df68c5d0282a84e8591629211ae3a3feb0723a057bb1eb.jpg)  
Figure 1. Wake-up event verified (wake-up event = address match)

The address does not match.

![](images/257bcba90f146f1a90f09a9a18bec0c5dbad2a2e6bc3dd5713d90bc552106a64.jpg)  
Figure 2. Wake-up event not verified (wake-up event = address match)

# 4.2

# Wake-up from a low-power mode in SmartRun domain (SRD)

The STM32 MCUs that support the LPBAM, which allows the devices to be functional and autonomous in Stop 0 Stop 1, and Stop 2 modes (with no software running).

The USART/LPUART is also functional in Stop mode thanks to the autonomous mode. The APB clock is requested by the peripheral each time the USART/LPUART status needs to be updated. Once the USART or LPUART receives the APB clock, it generates either an interrupt or a DMA request, depending on the peripheral configuration.

in Stop mode, but the kernel and APB clocks are stil available for the USART/LPUART. All the autnomous a   colle t blay transferred to/from the SRAM thanks to the DMA, while the STM32 MCU remains in Stop mode.

The LPDMA transfer complete interrupt wakes up the MCU.

![](images/5e81e2df1b3f45a49fff25c1561d51c598fa94759d9ed48f0fab6a27d8d815af.jpg)  
Figure 3. Wake-up interrupt from SmartRun domain   
Software configures DMA to send three data blocks and To enable the LPUART.

# 5 USART/LPUART baudrate for a correct wake-up

The maximum USART or LPUART baudrate to correctly wake up the STM32 MCU from a low-power mode depends on the USART/LPUART kernel clock status (switched on or off).

# USART/LPUART kernel clock switched on in low-power mode

In ashecnstraintnheaxi bauat ake he m  lo-powemo. It is the same as in Run mode.

# 5.1.1

# Internal oscillator clock used as USART/LPUART clock source

Fo 2LLwayeeaio co low-power mode:

# Note:

Set the HSIKERON/MSIKERON bit in RCC_CR.   
Set the UCESM bit in USART/LPUART_CR3.   
This bit allows the USART/LPUART torequest the clock al the time, and not only on START bit fllng edge.   
For consumption reasons, some products offer peripheral clock gating during Sleep and Stop modes. Consequently, for the USART and LPUART, the clock gating must be removed prior to entering in lowpower mode. For more details, refer to the RCC section in the device reference manual,.   
For STM32FO/F3 devices, the internal oscillator clock is always switched off during Stop mode. It is switched on only when a falling edge is detected on the USART/LPUART receive line.

# 5.1.2

# LSE used as LPUART clock source

When the LSE clock is used as LPUART clock source, the maximum baudrate is 9600 bauds.

The LS clockai withed   low-powrmode, ut,  TM32L/L devis,is ot propagatee LUAR  LAR deso st  ke cock.   at  ba rlow eUCEM    UARTRh  UAR   oc time, not only on the START bit falling edge.

For the other STM32 devices, the LSE clock remains switched on in low-power mode, and is propagated to the LPUART. There is no constraint to receive data at 9600 bauds.

# 5.1.3 LSE used as USART clock source

When the LSE clock is used as USART clock source, the maximum baudrate is:

4096 bauds in case of oversampling by eight

• 2048 bauds in case of oversampling by 16

# USART/LPUART internal oscillator clock off in low-power mode

Il up an STM32 MCU from a low-power mode depends on the following criteria:

the wake-up time parameter (twuusART or twuLPUART)

For STM32F0/F3/L0 devices, twuuSART (or twuLPUART) equals twusTOP (as specified in the datasheet). For the other STM32 devices, twuusART (or twuLPUART) is specified in the datasheet.

the USART receiver tolerance, which depends on the following parameters:

9-, 10-, or 11-bit character length, configured through the M bits in USART_CR1   
oversampling by eight or 16, configured through the OVER8 bit in USART_CR1   
BRR[3:0] = or ≠ 0 in USART_BRR   
one or three sample bits used to sample data, depending on ONEBIT in USART_CR3   
The tables below summarize the USART receiver tolerance according to the values of the above parameters.

Table 4. USART receiver tolerance when BRR[3:0] = 0x0   

<table><tr><td rowspan=2 colspan=1>M bits</td><td rowspan=1 colspan=2>USART receiver tolerance (%)when OVER8 = 0</td><td rowspan=1 colspan=2>USART receiver tolerance (%)when OVER8 = 1</td></tr><tr><td rowspan=1 colspan=1>ONEBIT = 0</td><td rowspan=1 colspan=1>ONEBIT = 1</td><td rowspan=1 colspan=1>ONEBIT = 0</td><td rowspan=1 colspan=1>ONEBIT = 1</td></tr><tr><td rowspan=1 colspan=1>00</td><td rowspan=1 colspan=1>3.75</td><td rowspan=1 colspan=1>4.375</td><td rowspan=1 colspan=1>2.5</td><td rowspan=1 colspan=1>3.75</td></tr><tr><td rowspan=1 colspan=1>01</td><td rowspan=1 colspan=1>3.41</td><td rowspan=1 colspan=1>3.97</td><td rowspan=1 colspan=1>2.27</td><td rowspan=1 colspan=1>3.41</td></tr><tr><td rowspan=1 colspan=1>10</td><td rowspan=1 colspan=1>4.16</td><td rowspan=1 colspan=1>4.86</td><td rowspan=1 colspan=1>2.77</td><td rowspan=1 colspan=1>4.16</td></tr></table>

Table 5. USART receiver tolerance when BRR[3:0] ≠ 0x0   

<table><tr><td rowspan=2 colspan=1>M bits</td><td rowspan=1 colspan=2>USART receiver tolerance (%)when OVER8 = 0</td><td rowspan=1 colspan=2>USART receiver tolerance (%)when OVER8 = 1</td></tr><tr><td rowspan=1 colspan=1>ONEBIT = 0</td><td rowspan=1 colspan=1>ONEBIT = 1</td><td rowspan=1 colspan=1>ONEBIT = 0</td><td rowspan=1 colspan=1>ONEBIT = 1</td></tr><tr><td rowspan=1 colspan=1>00</td><td rowspan=1 colspan=1>3.33</td><td rowspan=1 colspan=1>3.88</td><td rowspan=1 colspan=1>2</td><td rowspan=1 colspan=1>3</td></tr><tr><td rowspan=1 colspan=1>01</td><td rowspan=1 colspan=1>3.03</td><td rowspan=1 colspan=1>3.53</td><td rowspan=1 colspan=1>1.82</td><td rowspan=1 colspan=1>2.73</td></tr><tr><td rowspan=1 colspan=1>10</td><td rowspan=1 colspan=1>3.7</td><td rowspan=1 colspan=1>4.31</td><td rowspan=1 colspan=1>2.22</td><td rowspan=1 colspan=1>3.33</td></tr></table>

the LPUART receiver tolerance, which depends on the following parameters:

number of Stop bits configured through STOP[1:0] bitfield in LPUART_CR2   
value of LPUART_BRR   
The table below summarizes the LPUART receiver tolerance according to the values of the above parameters.

Table 6. LPUART receiver tolerance   

<table><tr><td rowspan=2 colspan=1>M and Stop bits</td><td rowspan=1 colspan=2>LPUART receiver tolerance (%)when OVER8 = 0</td><td rowspan=1 colspan=2>LPUART receiver tolerance (%)when OVER8 = 1</td></tr><tr><td rowspan=1 colspan=1>ONEBIT = 0</td><td rowspan=1 colspan=1>ONEBIT = 1</td><td rowspan=1 colspan=1>ONEBIT = 0</td><td rowspan=1 colspan=1>ONEBIT = 1</td></tr><tr><td rowspan=1 colspan=1>8 bits (M = 00), 1 Stop bit</td><td rowspan=1 colspan=1>1.82</td><td rowspan=1 colspan=1>2.56</td><td rowspan=1 colspan=1>3.9</td><td rowspan=1 colspan=1>4.42</td></tr><tr><td rowspan=1 colspan=1>9 bits (M = 01), 1 Stop bit</td><td rowspan=1 colspan=1>1.69</td><td rowspan=1 colspan=1>2.33</td><td rowspan=1 colspan=1>2.53</td><td rowspan=1 colspan=1>4.14</td></tr><tr><td rowspan=1 colspan=1>7 bits (M = 10), 1 Stop bit</td><td rowspan=1 colspan=1>2.08</td><td rowspan=1 colspan=1>2.86</td><td rowspan=1 colspan=1>4.35</td><td rowspan=1 colspan=1>4.42</td></tr><tr><td rowspan=1 colspan=1>8 bits (M = 00), 2 Stop bits</td><td rowspan=1 colspan=1>2.08</td><td rowspan=1 colspan=1>2.86</td><td rowspan=1 colspan=1>4.35</td><td rowspan=1 colspan=1>4.42</td></tr><tr><td rowspan=1 colspan=1>9 bits (M = 01), 2 Stop bits</td><td rowspan=1 colspan=1>1.82</td><td rowspan=1 colspan=1>2.56</td><td rowspan=1 colspan=1>3.9</td><td rowspan=1 colspan=1>4.42</td></tr><tr><td rowspan=1 colspan=1>7 bits (M = 10), 2 Stop bits</td><td rowspan=1 colspan=1>2.34</td><td rowspan=1 colspan=1>3.23</td><td rowspan=1 colspan=1>4.92</td><td rowspan=1 colspan=1>4.42</td></tr></table>

The USART/LPUART asyncronous receiver workscorrectly only f the total clock system deviation s less tha the USART/LPUART receiver tolerance. The following parameters contribute to the total deviation:

DTRAdevation uthetanitteror alsoncludes heevitinhetranitter localcilato   
DQUANT: error due to the baudrate quantization of the receiver   
DREC: deviation of the receiver local oscillator   
DTCL: deviation due to the transmission line (generally due to the transceivers, which introduce an   
asymmetry between the low-to-high and high-to-low transition timings)

The rule is then given by this formula

DTRA + DQUANT + DRAC + DTCL + DWU < USART or LPUART receiver toleranCe where DWU is the error due to samplig point deviation when the wakeup from a low-power mode is used. The maximum baudrate to wake up the MCU from a low-power mode can be computed as follows:

case 1: USART/LPUART receiver with 9-bit data length and M = 01

![](images/b32f3e9dc1fc2c84b2290a3272b1fe78d992d2a8d5844fe89e42ff04de8815fe.jpg)

where Tbit min is the minimum bit duration

![](images/a1080d0a8dadf87744b0f240c02b505c18e140a436413466373e48a00cc063df.jpg)

• case 2: USART/LPUART receiver with 8-bit data length and M = 00

![](images/008a13aa34ceec118e05dc7b86a276005d4ec87588842346651f19565e99f783.jpg)

case 3: USART/LPUART receiver with 7-bit data length and M = 10

![](images/0e2ad7781afacf427114e3615eea027c2b16cb392ec36259945b5fd79230e3c3.jpg)

# STM32L4 example

Conditions: USART receiver with OVER8 = 0, M = 10, ONEBIT = 1, and BRR[3:0] = 0x0.   
In this case, the USART receiver tolerance is 4.86 % (refer to Table 4).   
In the ideal case where DTRA = DQUANT = DREC = DTCL = 0%, DWU max = 4.86%. In reality, the HSI inaccuracy must be taken into account.   
For an HSI inaccuracy of 1 %:

twuuSART = 8.5 µs (for Stop 1 or Stop 2 modes) DWUmax = 4.86 - 1 % = 3.86 % Tbit min = 8.5 / (9 x 3.86 %) = 24.4 µs

The maximum baudrate to correctly wake up the STM32 MCU from a low-power mode is then: 1 / 24.4 µs = \~ 40 kbauds.

# 6 Conclusion

This application note explains how the USART or the LPUART wakes up an STM32 MCU from a low-power mode. It also provides guidelines to approximately determine the associated USART/LPUART maximum baudrate.

# Revision history

Table 7. Document revision history   

<table><tr><td rowspan=2 colspan=1>Date</td><td rowspan=2 colspan=1>Version</td><td></td></tr><tr><td rowspan=1 colspan=1>Changes</td></tr><tr><td rowspan=1 colspan=1>8-Mar-2017</td><td rowspan=1 colspan=1>1</td><td rowspan=1 colspan=1>Initial release.</td></tr><tr><td rowspan=1 colspan=1>17-Dec-2019</td><td rowspan=1 colspan=1>2</td><td rowspan=1 colspan=1>Updated microcontroller list in:Title of the documentTable 1: Applicable productsSection 5.2: USART/LPUART HSI kernel clock is OFF in low-power modeAdded Section 1: General information (Arm logo added)Updated:Table 2: Low-power modes versus STM32xx SeriesSection 5.1.1: HSI clock used as USART/LPUART clock source•    Section 5.1.2: LSE clock used as LPUART clock source</td></tr><tr><td rowspan=1 colspan=1>8-Dec-2022</td><td rowspan=1 colspan=1>3</td><td rowspan=1 colspan=1>STM32U5 Series inserted in this documentUpdatedDocument titleTable 1. Applicable productsSection 2 STM32 low-power modesSection 3.2 USART/LPUART wake-up sourcesSection 4 How the USART/PLUART wakes up the STM32 with new Section 4.2Section 5.1.1 Internal oscillator clock used as USART/LPUART clock source</td></tr><tr><td rowspan=1 colspan=1>14-Dec-2022</td><td rowspan=1 colspan=1>4</td><td rowspan=1 colspan=1>Updated:Table 1. Applicable products to include the STM32C0 SeriesTable 2. STM32 low-power modesTable 3. STM32 internal oscillators</td></tr><tr><td rowspan=1 colspan=1>16-Jan-2023</td><td rowspan=1 colspan=1>5</td><td rowspan=1 colspan=1>Updated:Table 1. Applicable products to include the STM32WBA seriesTable 2. STM32 low-power modesTable 3. STM32 internal oscillators</td></tr><tr><td rowspan=1 colspan=1>05-Sep-2024</td><td rowspan=1 colspan=1>6</td><td rowspan=1 colspan=1>Added support for STM32H5 series, STM32H7 series, STM32N6 series, and STM32WB0series.</td></tr><tr><td rowspan=1 colspan=1>14-Feb-2025</td><td rowspan=1 colspan=1>7</td><td rowspan=1 colspan=1>Added STM32U0 series and STM32U3 series.Updated:Section 2: STM32 low-power modes.Section 4.1: Wake-up from a low-power mode when the internal oscillator is off</td></tr></table>

# Contents

# 1 General information

2 STM32 low-power modes 5

# 3 USART/LPUART wake-up features

3.1 Dual-clock domain.   
3.2 USART/LPUART wake-up sources.

# How the USART/PLUART wakes up the STM32 5

4.1 Wake-up from a low-power mode when the internal oscillator is off . 5   
4.2 Wake-up from a low-power mode in SmartRun domain (SRD). 6

# USART/LPUART baudrate for a correct wake-up. . 8

5.1 USART/LPUART kernel clock switched on in low-power mode 8

5.1.1 Internal oscillator clock used as USART/LPUART clock source 8   
5.1.2 LSE used as LPUART clock source 8   
5.1.3 LSE used as USART clock source 8

5.2 USART/LPUART internal oscillator clock off in low-power mode 8

# 5 Conclusion 11

Revision history 12

# .ist of tables 14

List of figures. . 15

# List of tables

Table 1. Applicable products   
Table 2. STM32 low-power modes 3   
Table 3. STM32 internal oscillators . 5   
Table 4. USART receiver tolerance when BRR[3:0] = 0x0 9   
Table 5. USART receiver tolerance when BRR[3:0] ≠ 0x0 9   
Table 6. LPUART receiver tolerance . 9   
Table 7. Document revision history . 12

# List of figures

Figure 1. Wake-up event verified (wake-up event = address match) 5 Figure 2. Wake-up event not verified (wake-up event = address match). 6 Figure 3. Wake-up interrupt from SmartRun domain

# IMPORTANT NOTICE  READ CAREFULLY

pt old ursant  dits   leole.

purchasers' products.

No license, express or implied, to any intellectual property right is granted by ST herein.

are the property of their respective owners.

I

© 2025 STMicroelectronics - All rights reserved