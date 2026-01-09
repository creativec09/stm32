# How to use PWM shutdown for motor control and digital power conversion on STM32 MCUs

# Introduction

digital power conversion such as lighting, SMPS, and induction heating.

This application note:

provides an overview of the timer break feature.   
details how the timer break input is connected to different break sources.   
enumerates the different break event sources.   
u source, or a combination of both internal and external break signals.   
shohowpnventol onsrh peripherals such as comparators and DAC.

This document applies to the products listed in Table 1.

Table 1. Applicable products   

<table><tr><td>Type</td><td>Product series</td></tr><tr><td></td><td>STM32C0 series</td></tr><tr><td></td><td>STM32F0 series, STM32F1 series, STM32F2 series, STM32F3 series, STM32F4 series, STM32F7 series</td></tr><tr><td></td><td>STM32G0 series, STM32G4 series</td></tr><tr><td>Microcontrollers</td><td>STM32H5 series, STM32H7 series</td></tr><tr><td></td><td>STM32L4 series, STM32L5 series</td></tr><tr><td></td><td>STM32U0 series, STM32U3 series, STM32U5 series</td></tr><tr><td></td><td>STM32WB series, STM32WL series</td></tr></table>

# 1 General information

# Note:

This document applies to Arm®-based devices.   
Arm is a registered trademark of Arm Limited (or its subsidiaries) in the US and/or elsewhere.

# arm

# Reference documents

[1] Application note STM32 cross-series timer overview (AN4013)

# 2 Break function overview

The reak ci s available  ITMTIM20 TIM1 TM16, a TIM17 mer.Theeimer ae generate complementary PWM signals with a dead time insertion for driving power switches in a half-ridge topology.

The purposeof the break function is to protect power switches driven b WM signals generated with these timers. When triggered by a fault, the break circuitry shuts down the WM outputs and forces them to a predefined safe state.

Table 2 summarizes the break inputs availability.

Table 2. Timers and break input availability in STM32 devices   

<table><tr><td rowspan=1 colspan=1></td><td rowspan=1 colspan=1>TIM1</td><td rowspan=1 colspan=1>TIM8</td><td rowspan=1 colspan=1>TIM20</td><td rowspan=1 colspan=1>TIM15</td><td rowspan=1 colspan=1>TIM16</td><td rowspan=1 colspan=1>TIM17</td></tr><tr><td rowspan=2 colspan=1>STM32F0</td><td rowspan=1 colspan=1>BRK</td><td rowspan=2 colspan=1></td><td rowspan=2 colspan=1></td><td rowspan=2 colspan=1></td><td rowspan=2 colspan=1></td><td rowspan=2 colspan=1></td></tr><tr><td rowspan=1 colspan=1>BRK_ACTH</td></tr><tr><td rowspan=2 colspan=1>STM32F1</td><td rowspan=1 colspan=1>BRK</td><td rowspan=2 colspan=1></td><td rowspan=2 colspan=1>-</td><td rowspan=1 colspan=1>BRK</td><td rowspan=1 colspan=1>BRK</td><td rowspan=1 colspan=1>BRK</td></tr><tr><td rowspan=1 colspan=1>BRK_ACTH</td><td rowspan=1 colspan=1>BRK_ACTH</td><td rowspan=1 colspan=1>BRK_ACTH</td><td rowspan=1 colspan=1>BRK_ACTH</td></tr><tr><td rowspan=2 colspan=1>STM32F2 STM32F4</td><td rowspan=1 colspan=1>BRK</td><td rowspan=1 colspan=1>BRK</td><td rowspan=2 colspan=1>-</td><td rowspan=2 colspan=1>-</td><td rowspan=2 colspan=1></td><td rowspan=2 colspan=1></td></tr><tr><td rowspan=1 colspan=1>BRK_ACTH</td><td rowspan=1 colspan=1>BRK_ACTH</td></tr><tr><td rowspan=3 colspan=1>STM32F3</td><td rowspan=1 colspan=1>BRK</td><td rowspan=1 colspan=1>BRK</td><td rowspan=1 colspan=1>BRK</td><td rowspan=1 colspan=1>BRK</td><td rowspan=1 colspan=1>BRK</td><td rowspan=1 colspan=1>BRK</td></tr><tr><td rowspan=1 colspan=1>BRK2</td><td rowspan=1 colspan=1>BRK2</td><td rowspan=1 colspan=1>BRK2</td><td rowspan=1 colspan=1>BRK_ACTH</td><td rowspan=1 colspan=1>BRK_ACTH</td><td rowspan=1 colspan=1>BRK_ACTH</td></tr><tr><td rowspan=1 colspan=1>BRK_ACTH</td><td rowspan=1 colspan=1>BRK_ACTH</td><td rowspan=1 colspan=1>BRK_ACTH</td><td rowspan=1 colspan=1>-</td><td rowspan=1 colspan=1>-</td><td rowspan=1 colspan=1></td></tr><tr><td rowspan=3 colspan=1>STM32F7</td><td rowspan=1 colspan=1>BRK</td><td rowspan=1 colspan=1>BRK</td><td rowspan=3 colspan=1></td><td rowspan=3 colspan=1></td><td rowspan=3 colspan=1></td><td rowspan=3 colspan=1></td></tr><tr><td rowspan=1 colspan=1>BRK2</td><td rowspan=1 colspan=1>BRK2</td></tr><tr><td rowspan=1 colspan=1>BRK_ACTH</td><td rowspan=1 colspan=1>BRK_ACTH</td></tr><tr><td rowspan=3 colspan=1>STM32L4 STM32L5STM32U5SSTM32(1)STM32H5(2)</td><td rowspan=1 colspan=1>BRK</td><td rowspan=1 colspan=1>BRK</td><td rowspan=1 colspan=1></td><td rowspan=1 colspan=1>BRK</td><td rowspan=1 colspan=1>BRK</td><td rowspan=1 colspan=1>BRK</td></tr><tr><td rowspan=1 colspan=1>BRK2</td><td rowspan=1 colspan=1>BRK2</td><td rowspan=2 colspan=1></td><td rowspan=1 colspan=1>System break</td><td rowspan=1 colspan=1>System break</td><td rowspan=1 colspan=1>System break</td></tr><tr><td rowspan=1 colspan=1>System break</td><td rowspan=1 colspan=1>System break</td><td rowspan=1 colspan=1>-</td><td rowspan=1 colspan=1></td><td rowspan=1 colspan=1></td></tr><tr><td rowspan=3 colspan=1>STM32C0S STM32WBSTM32WLSTM32H7Rx/7Sx</td><td rowspan=1 colspan=1>BRK</td><td rowspan=3 colspan=1></td><td rowspan=3 colspan=1></td><td rowspan=3 colspan=1></td><td rowspan=1 colspan=1>BRK</td><td rowspan=1 colspan=1>BRK</td></tr><tr><td rowspan=1 colspan=1>BRK2</td><td rowspan=1 colspan=1>System break</td><td rowspan=1 colspan=1>System break</td></tr><tr><td rowspan=1 colspan=1>System break</td><td rowspan=1 colspan=1></td><td rowspan=1 colspan=1></td></tr><tr><td rowspan=3 colspan=1>STM32G0, STM32U3</td><td rowspan=1 colspan=1>BRK</td><td rowspan=3 colspan=1>-</td><td rowspan=3 colspan=1></td><td rowspan=1 colspan=1>BRK</td><td rowspan=1 colspan=1>BRK</td><td rowspan=1 colspan=1>BRK</td></tr><tr><td rowspan=1 colspan=1>BRK2</td><td rowspan=1 colspan=1>System break</td><td rowspan=1 colspan=1>System break</td><td rowspan=1 colspan=1>System break</td></tr><tr><td rowspan=1 colspan=1>System break</td><td rowspan=1 colspan=1>-</td><td rowspan=1 colspan=1>-</td><td rowspan=1 colspan=1>-</td></tr><tr><td rowspan=3 colspan=1>STM32G4</td><td rowspan=1 colspan=1>BRK</td><td rowspan=1 colspan=1>BRK</td><td rowspan=1 colspan=1>BRK</td><td rowspan=1 colspan=1>BRK</td><td rowspan=1 colspan=1>BRK</td><td rowspan=1 colspan=1>BRK</td></tr><tr><td rowspan=1 colspan=1>BRK2</td><td rowspan=1 colspan=1>BRK2</td><td rowspan=1 colspan=1>BRK2</td><td rowspan=1 colspan=1>System break</td><td rowspan=1 colspan=1>System break</td><td rowspan=1 colspan=1>System break</td></tr><tr><td rowspan=1 colspan=1>System break</td><td rowspan=1 colspan=1>System break</td><td rowspan=1 colspan=1>System break</td><td rowspan=1 colspan=1>-</td><td rowspan=1 colspan=1>-</td><td rowspan=1 colspan=1></td></tr><tr><td rowspan=3 colspan=1>STM32H503STM32U0</td><td rowspan=1 colspan=1>BRK</td><td rowspan=3 colspan=1></td><td rowspan=3 colspan=1></td><td rowspan=3 colspan=1></td><td rowspan=3 colspan=1></td><td rowspan=3 colspan=1></td></tr><tr><td rowspan=1 colspan=1>BRK2</td></tr><tr><td rowspan=1 colspan=1>System break</td></tr><tr><td rowspan=3 colspan=1>STM32L0</td><td rowspan=1 colspan=1>BRK</td><td rowspan=3 colspan=1></td><td rowspan=3 colspan=1></td><td rowspan=3 colspan=1></td><td rowspan=3 colspan=1></td><td rowspan=3 colspan=1></td></tr><tr><td rowspan=1 colspan=1></td></tr><tr><td rowspan=1 colspan=1>-</td></tr></table>

1. Excluding STM32H7Rx/7Sx. 2 Excluding STM32H503.

he v disables the PWM outputs (inactive state).

BRK has ahigher priority than BRK. When both protections are trigered, the predefined safe state relat t the BRK circuitry overrides the inactive state related to the BRK2 input.

Typically, a permanent magnet 3-phase brushless motor drive uses the protections as follows:

The BRK2 input as an overcurrent protection, opening the six switches from the power stage. The BRK input as an overvoltage protection, overriding the overcurrent and closing the three low-side switches to avoid current regeneration to build up the bus voltage and exceed the capacitor-rated voltge.

As an example in STM32F303xB/C/D/E devices, for a dual motor drive, the comparators 1, 2, and 3 can be dedicated oovercurrent monitoring the three phases motor R ipu ).The comparator ,, a 6 an ededicat vercurent monitoring e re hasesmoor R ipu T8), wh e comparator 7 is used for overvoltage monitoring (driving BRK inputs of TIM1 and TIM8).

BRK_ACTH input is connected only to internal signals such as CSS and PVD output. On newer devices like ST32U5or STM32U3, it is markeas timsysbrk (system breakinterconect) orasintenal sourc but his serves the same purpose. For more details, refer to Section 3: Break implementation.

The availability of break inputs and the break sources depends on the selected STM32 family.

This is summarized in Table 3 and in document [1] which details the available timers

Comparator availability may be limited by the package pin count.

Table 3. Comparator peripherals availability per STM32 device   

<table><tr><td rowspan=2 colspan=1></td><td rowspan=1 colspan=2>2</td><td rowspan=1 colspan=10>STM32F3</td><td rowspan=1 colspan=1></td><td rowspan=1 colspan=1></td><td rowspan=1 colspan=2>2</td><td rowspan=2 colspan=1>2</td><td rowspan=2 colspan=1>2</td><td rowspan=2 colspan=1>2</td><td rowspan=2 colspan=1>2</td><td rowspan=1 colspan=1>2</td><td rowspan=1 colspan=2>(ε)03</td><td rowspan=1 colspan=2>2</td><td rowspan=1 colspan=1>2</td><td rowspan=2 colspan=1>(W</td></tr><tr><td rowspan=1 colspan=1>SXX30AX20</td><td rowspan=1 colspan=1>XXX2003XX</td><td rowspan=1 colspan=1>2020</td><td rowspan=1 colspan=1>20</td><td rowspan=1 colspan=1>20</td><td rowspan=1 colspan=1>20</td><td rowspan=1 colspan=2>2SWX3233AGG/EE</td><td rowspan=1 colspan=1>2020</td><td rowspan=1 colspan=2>20208</td><td rowspan=1 colspan=1>SXX3RNX</td><td rowspan=1 colspan=2>()M2⊥(Z0N2)</td><td rowspan=1 colspan=1>2</td><td rowspan=1 colspan=1>20</td><td rowspan=1 colspan=1>()32)</td><td rowspan=1 colspan=1>2020</td><td rowspan=1 colspan=1>20</td><td rowspan=1 colspan=1>2</td><td rowspan=1 colspan=1>SXA3A2</td><td rowspan=1 colspan=1>2</td></tr><tr><td rowspan=1 colspan=1>Filter</td><td rowspan=1 colspan=2></td><td rowspan=1 colspan=1></td><td rowspan=1 colspan=2></td><td rowspan=1 colspan=2></td><td rowspan=1 colspan=1></td><td rowspan=1 colspan=2></td><td rowspan=1 colspan=1></td><td rowspan=1 colspan=1></td><td rowspan=1 colspan=2></td><td rowspan=1 colspan=2>DFSDM</td><td rowspan=1 colspan=1>DFSDM</td><td rowspan=1 colspan=1>MDF(5)</td><td rowspan=1 colspan=4></td><td rowspan=1 colspan=1></td><td rowspan=1 colspan=1></td><td rowspan=1 colspan=1>-</td><td rowspan=1 colspan=1></td><td rowspan=1 colspan=1>DFSDM</td></tr><tr><td rowspan=1 colspan=1>COMP 1</td><td rowspan=1 colspan=2>X</td><td rowspan=1 colspan=1>X</td><td rowspan=1 colspan=2></td><td rowspan=1 colspan=2>X</td><td rowspan=1 colspan=1>X</td><td rowspan=1 colspan=2></td><td rowspan=1 colspan=1></td><td rowspan=1 colspan=1>X</td><td rowspan=1 colspan=2>X</td><td rowspan=1 colspan=2>X</td><td rowspan=1 colspan=1>X</td><td rowspan=1 colspan=1>X</td><td rowspan=1 colspan=4>X</td><td rowspan=1 colspan=1>X</td><td rowspan=1 colspan=1>X</td><td rowspan=1 colspan=1>X</td><td rowspan=1 colspan=1>X</td><td rowspan=1 colspan=1>X</td></tr><tr><td rowspan=1 colspan=1>COMP 2</td><td rowspan=1 colspan=2>X</td><td rowspan=1 colspan=1>X</td><td rowspan=1 colspan=2>X</td><td rowspan=1 colspan=2>X</td><td rowspan=1 colspan=1>X</td><td rowspan=1 colspan=2>X</td><td rowspan=1 colspan=1>X</td><td rowspan=1 colspan=1>X</td><td rowspan=1 colspan=2>X</td><td rowspan=1 colspan=2>X(6)</td><td rowspan=1 colspan=1>X</td><td rowspan=1 colspan=1>X</td><td rowspan=1 colspan=4>X</td><td rowspan=1 colspan=1>X</td><td rowspan=1 colspan=1>X</td><td rowspan=1 colspan=1>X</td><td rowspan=1 colspan=1>-</td><td rowspan=1 colspan=1>X</td></tr><tr><td rowspan=1 colspan=1>COMP 3</td><td rowspan=1 colspan=2>-</td><td rowspan=1 colspan=1>X</td><td rowspan=1 colspan=2></td><td rowspan=1 colspan=2>X</td><td rowspan=1 colspan=1>-</td><td rowspan=1 colspan=2></td><td rowspan=1 colspan=1></td><td rowspan=1 colspan=1></td><td rowspan=1 colspan=2>-</td><td rowspan=1 colspan=2>-</td><td rowspan=1 colspan=1></td><td rowspan=1 colspan=1>-</td><td rowspan=1 colspan=4></td><td rowspan=1 colspan=1>X</td><td rowspan=1 colspan=1>X</td><td rowspan=1 colspan=1>X</td><td rowspan=1 colspan=1>-</td><td rowspan=1 colspan=1>-</td></tr><tr><td rowspan=1 colspan=1>COMP 4</td><td rowspan=1 colspan=2></td><td rowspan=1 colspan=1>X</td><td rowspan=1 colspan=2>X</td><td rowspan=1 colspan=2>X</td><td rowspan=1 colspan=1>X</td><td rowspan=1 colspan=2>X</td><td rowspan=1 colspan=1>X</td><td rowspan=1 colspan=1></td><td rowspan=1 colspan=2>-</td><td rowspan=1 colspan=2>-</td><td rowspan=1 colspan=1></td><td rowspan=1 colspan=1>-</td><td rowspan=1 colspan=4></td><td rowspan=1 colspan=1></td><td rowspan=1 colspan=1>X</td><td rowspan=1 colspan=1>X</td><td rowspan=1 colspan=1></td><td rowspan=1 colspan=1></td></tr><tr><td rowspan=1 colspan=1>COMP 5</td><td rowspan=1 colspan=2></td><td rowspan=1 colspan=1>X</td><td rowspan=1 colspan=2></td><td rowspan=1 colspan=2>X</td><td rowspan=1 colspan=1>-</td><td rowspan=1 colspan=2></td><td rowspan=1 colspan=1></td><td rowspan=1 colspan=1></td><td rowspan=1 colspan=2>-</td><td rowspan=1 colspan=2>-</td><td rowspan=1 colspan=1>-</td><td rowspan=1 colspan=1>-</td><td rowspan=1 colspan=4></td><td rowspan=1 colspan=1></td><td rowspan=1 colspan=1></td><td rowspan=1 colspan=1>X</td><td rowspan=1 colspan=1></td><td rowspan=1 colspan=1></td></tr><tr><td rowspan=1 colspan=1>COMP 6</td><td rowspan=1 colspan=2></td><td rowspan=1 colspan=1>X</td><td rowspan=1 colspan=2>X</td><td rowspan=1 colspan=2>X</td><td rowspan=1 colspan=1>X</td><td rowspan=1 colspan=2>X</td><td rowspan=1 colspan=1>X</td><td rowspan=1 colspan=1></td><td rowspan=1 colspan=2></td><td rowspan=1 colspan=2></td><td rowspan=1 colspan=1></td><td rowspan=1 colspan=1></td><td rowspan=1 colspan=4></td><td rowspan=1 colspan=1></td><td rowspan=1 colspan=1></td><td rowspan=1 colspan=1>X</td><td rowspan=1 colspan=1></td><td rowspan=1 colspan=1></td></tr><tr><td rowspan=1 colspan=1>COMP 7</td><td rowspan=1 colspan=2></td><td rowspan=1 colspan=1>X</td><td rowspan=1 colspan=2></td><td rowspan=1 colspan=2>X</td><td rowspan=1 colspan=1></td><td rowspan=1 colspan=2></td><td rowspan=1 colspan=1></td><td rowspan=1 colspan=1></td><td rowspan=1 colspan=2></td><td rowspan=1 colspan=2></td><td rowspan=1 colspan=1></td><td rowspan=1 colspan=1></td><td rowspan=1 colspan=4></td><td rowspan=1 colspan=1></td><td rowspan=1 colspan=1></td><td rowspan=1 colspan=1>X</td><td rowspan=1 colspan=1></td><td rowspan=1 colspan=1></td></tr></table>

1. These devices feature comparators, but no advanced timers with break inputs. 2. 3. STM32G0x0, STM32G031, and STM32G041 have no comparators. 4. Excluding the STM32H7Rx/Sx line. 5. ADF does not feature a break output. 6. STML412/L422 does not have COMP2.

# 3 Break implementation

# 3.1

# TIM1/8/20 break implementation

The source or break BRK chanel is an external source connected to one of the BKIN pins (as per selection done in the AFIO controller), with polarity selection and optional digital filtering.

The surc  break BR2chael is exteal sourccoe  e  he BKIN pis s per eln done in the AFIO controller), with polarity selection and optional digital flteing.

The source for BRK_ACTH (or system break interconnect) is an internal signal coming from:

The comparator output (on STM32Fx)   
The clock security system   
The lockup of Cortex-M family CPUs   
The PVD output   
The SRAM ECC/parity error signal   
The flash ECC error

# BRK

In all series, the input signal on BRK is connected to the BKIN pin.   
In the STM32F3 series, the input signal on BRK is a logical OR between the input signals on the BKIN pin a the secoparator 4 or 7)outu congure andused intenall.  the B altenatencns disabled, the resulting break signal is the comparator (4 or 7) output.   
In the STM32L4 and STM32H7 series (excluding the STM32H7Rx/Sx), the input signal on BRK is a logical OR between the input signals on the BKIN pin, the used comparator (1 or 2) output, and the DFSDM break ouucongur and use intenally.Eachapliation breaksourcehas own polariy congurtion. In the STM32U5 series, the input signal on BRK is a logical OR between the comparators (including MDF) break outputs and external sources.

The polarity feature is available for the BRK input. The filter feature is available as well but nly o STM32F3/F7/L4/U3/U5 devices.

# BRK_ACTH (or system break)

In the STM32F1/F2/F4/F7 series, this input only gathers the system level fault signals.   
In the STM32F0 series, BRK_ACTH is connected to the system level fault signals and the comparators outputs (1 and 2).   
In the STM32F3 series, BRK_ACTH is connected to the system level fault signals and the comparators (1, 2, 3, 5, and 6).   
For any non-Fx series, the system break request is connected to the system level fault signals. W  lfovI BRK_ACTH is enabled using the same bit as BRK (BKE in TIMx_BDTR, x= 1, 8, 20).   
.   
Ex u uano bloc.   
Orakputal orRegehe witte re.   
In ccoparator anexternal sgals, polariy must eserved orhe logical OR o work  nten.

# BRK2

In the STM323 seris, his input signal is a logical OR between the input signal on the BKIN2 pin and the ucomparators outputs (1, 2, 3,4,5, 6, and 7). If the BKIN2 alternate function is disabled (input not used), the resulting break signal is solely related to the comparators. In the STM32F7 series, the input signal on BRK2 is connected to the BKIN2 pin. In the STM32L4 series, the input signal on BRK2 is a logical OR between the input signals on the BKIN2 pin, the used comparator (1 or 2) output and the DFSDM break output if configured. In the STM32U5 series, the input signal on BRK2 is a logical OR between comparators (1 or 2) and MDF1.

In the STM32L4 and STM32L5 series, it is possible to configure the polarity of each break source in addition except the DFSDM break output to the polarity configuration inside the timer peripheral using BKCMP1P, BKCMP2P, BKINP in TIMx_OR2 register and BK2CMP1P, BK2CMP2P, BK2INP in TIMx_OR3 register.

In the STM32U5 and STM32H7 series, it is possible to configure the polarity of each break source in adition except the MDF1 (DFSDM) break output to the polarity configuration inside the timer peripheral using BKCMP1P, BKCMP2P, BKINP in the TIMx_AF1 register and BK2CMP1P, BK2CMP2P, BK2INP in the TIMx_AF2 register.

In the STM32G4 series, it is possible to configure the polarity of COMP1-4 using BKCMPxPbits in TIMx_AF1 register and BK2CMPxP in TIMx_AF2 register. The rest of the internal inputs have individual polarity fixed to active high, though the collective polarity is still configurable (BKP, BK2P).

Onother series, polarity is individually configurable for all theiravailable COMPx and BKIN/BKIN2 inputs

Figure 1 shows the break feature implementation for TIM1 and TIM8 in STM32F0/F1/F2/F4/F7 series devices.   
Figure 2 shows the break feature implementation for TIM1, TIM8, and TIM20 in STM32F3 series devices.   
Figure 3 shows the break feature implementation for TIM1 and TIM8 in STM32L4 series devices.   
Figure 4 shows the break feature implementation for TIM1 and TIM8 in STM32U5 series devices.

![](images/a45dd0d0d6a265758aa97a27f02c49abf3e59f1a0d5c614291bc63ec1c7d9475.jpg)  
Figure 1. Break feature implementation in advanced timers for STM32F0/F1/F2/F4/F7 series devices

![](images/3fba0d6ad4e2b10daed2250fa1d2e9e26cd72207d1ecc740de16372606e5e202.jpg)  
Figure 2. Break feature implementation in advanced timers for STM32F3 series devices

![](images/ae728679e7c52893e0233a62c51118ad2278d8d387e89f6aa5743800e103cb30.jpg)  
Figure 3. Break feature implementation in advanced timers for STM32L4 series devices

![](images/ffb6aeb966314b01a56302466526ac87af776a4fa6ccb03226bb1ea263047f4a.jpg)  
Figure 4. Break feature implementation in advanced timers for STM32U5 series devices

# Bidirectional break inputs

Forexaple he32L  325 ers, e ime timer 8ar eaturig bional breakut outpus combining the comparator output (to be configured in open drain) and the Timer BKIN input, as represented in Figure 5.

This feature allows information about the global break available for external MCUs with a single-pin.

![](images/1e9cf8df4f89bdf69601fbfcc7e51c339e568e8e9a715c0af03280823eb152ad.jpg)  
Figure 5. Output redirection

# 3.2

# TIM15/16/17 break implementation

The source for break BRK chanel is an external source connected to one of the BKIN pins as per selection done in the AFIO controller), with polarity selection and optional digital filtering.

The source for BRK_ACTH is an internal signal coming from:

The clock security system   
The lockup of Cortex-M family CPUs   
The PVD output   
The SRAM ECC/parity error signal   
The flash ECC error

Inputs from available comparators are ORed with BRK_ACTH signals (on STM32Fx series) or with the external BRK input with polarity selection option.

# BRK

In all series: the input signal on BRK is connected to the BKIN pin.   
In the STM32L4 series: the input signal on BRK is a logical OR between the input signals on the BKIN pin, the used comparator (1 or 2) output and the DFSDM break output if configured.   
In STM32U5 series: the input signal on BRK is a logical OR between the BKIN pin, the used comparator (1 or 2) output, and the MDF1 break output.

The polarity selection feature is available for the BRK source.

InSLs sible gurhe polar brea urt excpt FSDM brekoutput  he polarity coniguration inside he imer periheral usig BKCMPP, BKCMPP, BKINP  e TIMx_OR2 register.

I u oar brkr.e MDF1 break output to the polarity configuration inside the timer peripheral. This is done using BKCMP1P, BKCMP2P, BKINP in the TIMx_AF1 register.

Note: On TIM15-17, the filter feature is only available for STM32Gx, STM32Hx, and STM32U5 devices.

# BRK_ACTH (or system break)

In STM32F1/L4 series, this input only gathers the system level fault signals (CSS, PVD output, SRAM parity error, and the Hardfault).   
In STM32F3 series, BRK_ACTH is connected to the system level fault signals and the comparators (1 and 2) for the STM32F37xxx devices and the comparators outputs (3, 5, and 7) for the rest of the STM32F3 series.   
In other series, system break interconnected sources are CSS, flash, and SRAM ECC errors, PVD and core lockup detection.

Whu fv BRK_ACTH is enabled using the same bit BRK (BKE in TIMx_BDTR, x= 15, 16, 17).

When using BRK_ACTH as break input, the polarity must be configured high. Otherwise, there is no PWM generation independently of the break signal coming from the internal source.

Figure 6 shows the break feature implementation for TIM15, TIM16, and TIM17 in STM32F1 series devices.   
Figure 7 shows the break feature implementation for TIM15, TIM16, and TIM17 in STM32F3 series devices.   
Figure 8 shows the break feature implementation for TIM15, TIM16, and TIM17 in STM32L4 series devices.   
Figure 9 shows the break feature implementation for TIM15, TIM16, and TIM17 in STM32U5 series devices.

![](images/87465509f608f134708111d58127e64114b8a52a549df0cea5488c9af0df2f30.jpg)  
Figure 6. Break feature implementation for TIM15, TIM16, and TIM17 for STM32F1 series devices

![](images/b4ba1a6e5e90fbea79689f4cbb4095b039375066482d61c86328c8d06302532e.jpg)  
Figure 7. Break feature implementation for TIM15, TIM16, and TIM17 for STM32F3 series devices

![](images/258c6d8080960cff08e68d2e61dfc97fbedb0d19856332acebed91137cf3a622.jpg)  
Figure 8. Break feature implementation for TIM15, TIM16, and TIM17 for STM32L4 and STM32H7 series devices

If only an internal break source is used, the polarity must be configured to high in the software. If tee e evel break nput urs, eesultiinput gnal sOR betwee ll e put ls. If bot internal break source and BKIN are used, the resultig break signal is anOR between the sigal p and the internal break signal.

If the alternate function AF of the BKIN or BKIN2 pin is ot activated, the BRK or the BRK2 is conneed to aRR po tmutput isablTus it must cngure he break polarity hi.nly in he must configure the break polarity to low.

![](images/920ed7508767e79bad6ed28559918efb97c97a7083c6491a6f50f5cf3adc20b8.jpg)  
Figure 9. Break feature implementation for TIM15, TIM16, and TIM17 in STM32U5 series devices

STM32G0, STM32H7, STM32WB, and STM32WL are similar to STM32U5, except for MDF.

# 4 Break sources summary

Taivbleurtalleall 15, 16, and 17) break inputs.

Table 4. Break input sources   

<table><tr><td rowspan=1 colspan=1></td><td rowspan=1 colspan=1>BRK</td><td rowspan=1 colspan=1>BRK_ACTH(or system break)</td><td rowspan=1 colspan=1>BRK2</td></tr><tr><td rowspan=1 colspan=1>External connection to pin</td><td rowspan=1 colspan=1>BKIN</td><td rowspan=1 colspan=1>No corresponding I/O</td><td rowspan=1 colspan=1>BKIN2</td></tr><tr><td rowspan=1 colspan=1>Internal connection to pin</td><td rowspan=1 colspan=1>In STM32F3:Comparators 4 and 7for TIM1/8/20NA for TIM15/16/17In STM32G4: Allcomparators, some withpolarity control on TIM1/8/20In STM32L4 andSTM32H7(1):Comparators 1 and 2DFSDM break outputIn STM32U5:Comparators 1 and 2MDF1 break output</td><td rowspan=1 colspan=1>Available signals from:Clock failure eventgenerated by CSSPVD outputRAM parity error signalCortex-M LOCKUPoutput (Hardfault)Comparator outputs(on STM32Fx series)Flash double ECC error</td><td rowspan=1 colspan=1>In STM32F3:Comparators 1, 2, 3, 4,5, 6, and 7In STM32G4: Allcomparators, some withpolarity control on TIM1/8/20In STM32L4 andSTM32H7(1):Comparators 1 and 2DFSDM break outputIn STM32U5:•    Comparators 1 and 2MDF1 break output</td></tr><tr><td rowspan=1 colspan=1>Polarity feature in case ofinternal connection</td><td rowspan=1 colspan=1>Configurable for most inputs:active high or active low</td><td rowspan=1 colspan=1>Always active high</td><td rowspan=1 colspan=1>Configurable for some inputs:active high or active low</td></tr><tr><td rowspan=1 colspan=1>Polarity feature in case ofexternal break event</td><td rowspan=1 colspan=1>Available</td><td rowspan=1 colspan=1>NA</td><td rowspan=1 colspan=1>Available</td></tr><tr><td rowspan=1 colspan=1>Filter feature</td><td rowspan=1 colspan=1>Not available in STM32F0,STM32F1, STM32F2, andSTM32F4. Only available inSTM32F3 advanced timers.</td><td rowspan=1 colspan=1>NA</td><td rowspan=1 colspan=1>Not available in STM32F0,STM32F1, STM32F2, andSTM32F4</td></tr><tr><td rowspan=1 colspan=1>Available in</td><td rowspan=1 colspan=1>TIM1/8/20/15/16/17</td><td rowspan=1 colspan=1>TIM1/8/20/15/16/17</td><td rowspan=1 colspan=1>TIM1/8/20 in STM32F3,TIM1/8 in other series</td></tr><tr><td rowspan=1 colspan=1>Resulting break signal in caseof parallel external or/andinternal break sources</td><td rowspan=1 colspan=3>It is an OR between the external break signals and the internal ones.</td></tr></table>

1. Excluding the STM32H7Rx/Sx line.

# 5 Examples

Tal hos e W outut status orTx (where x =8, 0 ,in respse t intealxtl break events.

In the following waveforms:

The PWM signal is the reference waveform (internal signal, before BRK protection).   
The COMP_OUT signal represents the BRK input signal, in our case it is the comparator output.   
The BIN signal is the input signal on BKIN.   
The PWM_BRK signal is the resulting PWM signal on the timer output after break detection.

# Table 5. Scenarios of PWM output status in response to internal/external break events

or legend: green = PWM signal, blue = COMP_OUT signal, yellow = BKIN signal, purple = PWM_BRK signa

<table><tr><td rowspan=1 colspan=1>Configuration</td><td rowspan=1 colspan=1>Programmedpolarity</td><td rowspan=2 colspan=12>ResultThe PWM generation is stopped when the comparator output is at the high level, as shown in thefollowing screenshot:</td></tr><tr><td rowspan=6 colspan=1>Comparator 1 outputis connectedinternally to TIM1BRK_ACTH andTIM1 BKIN alternatefunction is disabled.</td><td rowspan=6 colspan=1>High</td></tr><tr><td rowspan=5 colspan=1></td><td rowspan=1 colspan=1></td><td rowspan=1 colspan=1></td><td rowspan=1 colspan=1></td><td rowspan=1 colspan=1></td><td rowspan=1 colspan=1></td><td rowspan=1 colspan=1></td><td rowspan=1 colspan=1></td><td rowspan=1 colspan=1></td><td rowspan=1 colspan=1></td><td rowspan=1 colspan=1></td><td rowspan=5 colspan=1>20</td></tr><tr><td rowspan=2 colspan=1>u</td><td rowspan=2 colspan=1>u</td><td rowspan=2 colspan=1></td><td rowspan=1 colspan=1></td><td rowspan=1 colspan=1></td><td rowspan=1 colspan=1></td><td rowspan=1 colspan=1></td><td rowspan=1 colspan=1></td><td rowspan=1 colspan=1></td><td rowspan=1 colspan=1></td></tr><tr><td rowspan=1 colspan=1></td><td rowspan=1 colspan=1></td><td rowspan=1 colspan=1></td><td rowspan=1 colspan=1></td><td rowspan=1 colspan=1></td><td rowspan=1 colspan=1></td><td rowspan=1 colspan=1>COMP_OUT</td></tr><tr><td rowspan=1 colspan=1></td><td rowspan=1 colspan=1></td><td rowspan=1 colspan=1></td><td rowspan=1 colspan=1></td><td rowspan=1 colspan=1></td><td rowspan=1 colspan=1></td><td rowspan=1 colspan=1></td><td rowspan=1 colspan=1></td><td rowspan=1 colspan=1></td><td rowspan=1 colspan=1>PWM_BRK</td></tr><tr><td rowspan=1 colspan=1></td><td rowspan=1 colspan=1></td><td rowspan=1 colspan=1></td><td rowspan=1 colspan=1></td><td rowspan=1 colspan=1></td><td rowspan=1 colspan=1></td><td rowspan=1 colspan=1></td><td rowspan=1 colspan=1></td><td rowspan=1 colspan=1></td><td rowspan=1 colspan=1></td></tr><tr><td></td><td></td><td rowspan=1 colspan=11>The break input signal is an OR between the signal on BKIN and the comparator output. Thefollowing screenshot shows an example (polarity = High):</td><td rowspan=1 colspan=1></td></tr><tr><td></td><td></td><td></td><td rowspan=1 colspan=1></td><td rowspan=1 colspan=1></td><td rowspan=1 colspan=1></td><td rowspan=1 colspan=1></td><td rowspan=1 colspan=1></td><td rowspan=1 colspan=1></td><td rowspan=1 colspan=1></td><td rowspan=1 colspan=1></td><td rowspan=1 colspan=1></td><td rowspan=1 colspan=1></td><td rowspan=5 colspan=1>0</td></tr><tr><td></td><td></td><td></td><td rowspan=1 colspan=2></td><td rowspan=1 colspan=2></td><td rowspan=1 colspan=1></td><td rowspan=1 colspan=1></td><td rowspan=1 colspan=1></td><td rowspan=1 colspan=2></td><td rowspan=1 colspan=1>PWMBKIN</td></tr><tr><td></td><td></td><td></td><td rowspan=1 colspan=1></td><td rowspan=1 colspan=1></td><td rowspan=1 colspan=1></td><td rowspan=1 colspan=1></td><td rowspan=1 colspan=1></td><td rowspan=1 colspan=1></td><td rowspan=1 colspan=1></td><td rowspan=1 colspan=1></td><td rowspan=1 colspan=1></td><td rowspan=1 colspan=1>COMP_OUT</td></tr><tr><td></td><td></td><td></td><td rowspan=2 colspan=2></td><td rowspan=2 colspan=1></td><td rowspan=2 colspan=1></td><td rowspan=2 colspan=1></td><td rowspan=2 colspan=1></td><td rowspan=1 colspan=1></td><td rowspan=1 colspan=1></td><td rowspan=1 colspan=1></td><td rowspan=1 colspan=1>PWM BRK</td></tr><tr><td></td><td></td><td></td><td rowspan=1 colspan=1></td><td rowspan=1 colspan=1></td><td rowspan=1 colspan=1></td><td rowspan=1 colspan=1></td><td rowspan=1 colspan=1></td></tr></table>

<table><tr><td rowspan=1 colspan=1>Configuration</td><td rowspan=6 colspan=1>ProgrammedpolarityLow</td><td rowspan=6 colspan=12>ResultThe PWM signal is stopped during the break signal low level, as shown in the following screenshot:VMCOMP_OUTPWM_BRK20</td></tr><tr><td rowspan=5 colspan=1>Comparator 4 outputis connectedinternally to TIM1BRK and the filter isnot configured.</td></tr><tr><td rowspan=1 colspan=1></td><td rowspan=1 colspan=1></td><td rowspan=1 colspan=1></td><td rowspan=1 colspan=1></td><td rowspan=1 colspan=1></td><td rowspan=1 colspan=1></td><td rowspan=1 colspan=1></td><td rowspan=1 colspan=1></td><td rowspan=1 colspan=1></td><td rowspan=1 colspan=1></td><td rowspan=4 colspan=1>20</td></tr><tr><td rowspan=2 colspan=1></td><td rowspan=2 colspan=1>U</td><td rowspan=2 colspan=1></td><td rowspan=1 colspan=1></td><td rowspan=1 colspan=1></td><td rowspan=1 colspan=1></td><td rowspan=1 colspan=1>T</td><td rowspan=1 colspan=1></td><td rowspan=1 colspan=1>T</td><td rowspan=1 colspan=1>VM</td></tr><tr><td rowspan=1 colspan=1></td><td rowspan=1 colspan=1></td><td rowspan=1 colspan=1></td><td rowspan=1 colspan=1></td><td rowspan=1 colspan=1></td><td rowspan=1 colspan=1></td><td rowspan=1 colspan=1>COMP_OUT</td></tr><tr><td rowspan=1 colspan=1></td><td rowspan=1 colspan=1>U</td><td rowspan=1 colspan=1></td><td rowspan=1 colspan=1></td><td rowspan=1 colspan=1></td><td rowspan=1 colspan=1></td><td rowspan=1 colspan=1></td><td rowspan=1 colspan=1></td><td rowspan=1 colspan=1></td><td rowspan=1 colspan=1>PWM_BRK</td></tr><tr><td></td><td></td><td></td><td></td><td></td><td rowspan=1 colspan=1></td><td rowspan=1 colspan=1></td><td rowspan=1 colspan=1></td><td rowspan=1 colspan=1></td><td rowspan=1 colspan=1></td><td rowspan=1 colspan=1></td><td rowspan=1 colspan=1></td><td rowspan=1 colspan=1></td><td></td></tr><tr><td></td><td></td><td></td><td rowspan=1 colspan=1></td><td rowspan=1 colspan=1></td><td rowspan=1 colspan=1></td><td rowspan=1 colspan=1></td><td rowspan=1 colspan=1></td><td rowspan=1 colspan=1></td><td rowspan=1 colspan=1></td><td rowspan=1 colspan=1></td><td rowspan=1 colspan=1></td><td rowspan=1 colspan=1></td><td></td></tr><tr><td></td><td></td><td></td><td rowspan=2 colspan=1></td><td rowspan=2 colspan=1></td><td rowspan=1 colspan=1></td><td rowspan=1 colspan=1></td><td rowspan=1 colspan=1></td><td rowspan=1 colspan=1></td><td rowspan=1 colspan=1></td><td rowspan=1 colspan=1></td><td rowspan=1 colspan=1></td><td rowspan=1 colspan=1>PWM_BRK</td><td></td></tr><tr><td></td><td></td><td></td><td rowspan=1 colspan=1></td><td rowspan=1 colspan=1></td><td rowspan=1 colspan=1></td><td rowspan=1 colspan=1></td><td rowspan=1 colspan=1></td><td rowspan=1 colspan=1></td><td rowspan=1 colspan=1></td><td rowspan=1 colspan=1></td><td></td></tr><tr><td></td><td></td><td></td><td rowspan=1 colspan=1></td><td rowspan=1 colspan=1></td><td rowspan=1 colspan=1></td><td rowspan=1 colspan=1></td><td rowspan=1 colspan=1></td><td rowspan=1 colspan=1></td><td rowspan=1 colspan=1></td><td rowspan=1 colspan=1></td><td rowspan=1 colspan=1></td><td rowspan=1 colspan=1></td><td></td></tr></table>

# 3 Using the break function with other MCU resources

This section focuses on the STM32G4 and STM32F3 series, but some parts may also apply to other STM32 series. In some cases, analogous resources may be used, such as system level fault instead of BRK_ACTH.

# Break function used for overcurrent protection

The STM32F3 and STM32G4 series microcontroller embeds a set of peripherals designed to resolve common morcontrol sues whil educing eumberrequirexteral components.Th ectindescribe how u the pepherals plement vercurrent potectiongurhows hevercurrent rotection that can be implemented using the internal resources of the MCU.

![](images/a806568bad282aecf78735b42ab05dd402fe5dd669459c39b207e8e7a18bc9fa.jpg)  
Figure 10. Overcurrent protection network implementation block diagram

The principle of this overcurrent protection mechanism can be summarized as follows:

T ha urn emo fow wnsver p shunt resistor (Rshunt) producing a voltage drop (V+). This voltage drop is compared with a threshold (V-) defining the maximum admissible current. If the threshold is exceeded, a break signal stops the PWM generation putting the system in a safe state.

Al e ru comparators and advanced timer break function (BRK2). In the basic implementation, the only external cnt quhehun isorhat must pendinurrent em shunt resistor power rating.

The two dotted line boxes in Figure 10 show the components required to measure current:

The R1/R2 resistive network to add an offset necessary to measure AC currents.

• An operational amplifier with a built-in gain setting network.

Theaplicatonetor an eplement extenally  e ca whehe bui gat are not adequate.

# 6.2

# Break function used for overvoltage protection

Figure shows the overvoltage protection network that can be implemented usig the internal resources many STM32 MCUs.

![](images/74c4b57be4d24089ff42376bbb3bf4f92bd30bc8dc4fcc5e305253b2b60c7d06.jpg)  
Figure 11. Overvoltage protection network block diagram

In this case, the principle is similar to the one described in Section 6.1 :

A resistive voltage divider provides a signal proportional to the bus voltage. This reading is compared to an overvoltage threshold to generate a fault signal. See also: Appendix A.1: How to use the DAC to define thresholds. • If the threshold is exceeded, a break signal stops the PWM generation putting the system in a safe state.

l on the PWM signals in case of an overcurrent.

In te apleenatn, eetealcent quevoltvihi mus  iz volrn maximum admissible voltage level.

Thedotted ie box i gurehos hecponent equiorhe us voltagmeasement. In te llo signal is fed directly to the analog-to-digital converter.

# Using an external emergency signal together with the internal comparator

Commonly in MC applications, gate driver ICs, such as ST's L639x family or intelligent powermodules (IPMs)- such as's LL (small ow-ossintelligentmoldoduleamil haveintegrate comparators that ca protect the inverter (ST's smart shutdown function) while sending an error signal to the microcontroller.

T  how plhcthow functional safety offered by the "break function".

f IMsso olvie u case is summarized in the following table.

Table 6. Comparator output connected internally to break inputs   

<table><tr><td rowspan=1 colspan=1>Description</td><td rowspan=1 colspan=1>Register</td><td rowspan=1 colspan=1>Bit</td><td rowspan=1 colspan=1>Configuration(1)</td></tr><tr><td rowspan=1 colspan=1>TIM1/8/20 BRK_ACTH/BRK/BRK2 polarity</td><td rowspan=1 colspan=1>TIMx_BDTR</td><td rowspan=1 colspan=1>BKP or BK2P</td><td rowspan=1 colspan=1>1 (active high)</td></tr><tr><td rowspan=1 colspan=1>Comparator output polarity</td><td rowspan=1 colspan=1>COMPx_CSR</td><td rowspan=1 colspan=1>COMPxPOL</td><td rowspan=1 colspan=1>0 (not inverted), comparators inputconnected as shown in previous sections</td></tr><tr><td rowspan=1 colspan=1>TIM1/8/20 BKIN and BKIN2 AF</td><td rowspan=1 colspan=1>GPIOxAFRL orTPXAFRH</td><td rowspan=1 colspan=1></td><td rowspan=1 colspan=1>AF is not enabled on BKIN1/2 related pins</td></tr><tr><td rowspan=1 colspan=1>TIM1/8/20 BRK and BRK2enable</td><td rowspan=1 colspan=1>TIMX_BDTR</td><td rowspan=1 colspan=1>BKE or BK2E</td><td rowspan=1 colspan=1>1</td></tr><tr><td rowspan=1 colspan=1>COMPx out selection</td><td rowspan=1 colspan=1>COMPx_CSR</td><td rowspan=1 colspan=1>COMPxOUTSEL</td><td rowspan=1 colspan=1>0001: TIM1 BRK or TIM1 BRK_ACTH(2)0010: TIM1 BRK20011: TIM8 BRK or TIM8 BRK_ACTH(3)0100: TIM8 BRK20101: TIM1 BRK2 + TIM8 BRK21100: TIM20 BRK or TIM20 BRK_ACTH(4)1101: TIM20 BRK21110: TIM1 BRK2 + TIM8 BRK2 + TIM20BBRK2</td></tr></table>

Some newer STM32 series, such as STM32U5 abandned the use f BRKACTH identier using name system level internal fault instead. The functionality remains analogous. 2. TIM1 BRK in case of COMP4 and COMP7, or TIM1 BRK_ACTH in case of COMPx, x = 1, 2, 3, 5, and 6. 3. TIM8 BRK in case of COMP4 and COMP7, or TIM8 BRK_ACTH in case of COMPx, x = 1, 2, 3, 5, and 6. 4. TIM20 BRK in case of COMP4 and COMP7, or TIM20 BRK_ACTH in case of COMPx, x= 1, 2, 3, 5, and 6.

O t ul eweeedinextealcarator g pss ogu write are summarized in the following tables.

Table 7. Comparator output connected externally to break inputs, with low break polarity   

<table><tr><td rowspan=1 colspan=1>Description</td><td rowspan=1 colspan=1>Register</td><td rowspan=1 colspan=1>Bit</td><td rowspan=1 colspan=1>Configuration</td></tr><tr><td rowspan=1 colspan=1>TIM1/8/20 BRK polarity</td><td rowspan=1 colspan=1>TIMx_BDTR</td><td rowspan=1 colspan=1>BKP</td><td rowspan=1 colspan=1>0 (active low), it means that the externalsignal goes low during the fault</td></tr><tr><td rowspan=1 colspan=1>Comparator output polarity</td><td rowspan=1 colspan=1>COMPx_CSR</td><td rowspan=1 colspan=1>COMPxPOL</td><td rowspan=1 colspan=1>0 (not inverted), comparators inputconnected as shown in previous sections</td></tr><tr><td rowspan=1 colspan=1>TIM1/8/20 BKIN AF</td><td rowspan=1 colspan=1>GPIOxAFRL orTGPIXAFRH</td><td rowspan=1 colspan=1></td><td rowspan=1 colspan=1>AF enabled on BKIN pin selected amongavailable</td></tr><tr><td rowspan=1 colspan=1>TIM1/8/20 BRK enable</td><td rowspan=1 colspan=1>TIMX_BDTR</td><td rowspan=1 colspan=1>BKE</td><td rowspan=1 colspan=1>1</td></tr><tr><td rowspan=1 colspan=1>COMPx out selection</td><td rowspan=1 colspan=1>COMPx_CSR</td><td rowspan=1 colspan=1>COMPxOUTSEL</td><td rowspan=1 colspan=1>0001: TIM1 BRK0011: TIM8 BRK1100: TIM20 BRK</td></tr></table>

Table 8. Comparator output connected externally to break inputs, with high break polarity   

<table><tr><td colspan="1" rowspan="1">Description</td><td colspan="1" rowspan="1">Register</td><td colspan="1" rowspan="1">Bit</td><td colspan="1" rowspan="1">Configuration</td></tr><tr><td colspan="1" rowspan="1">TIM1/8/20 BRK/BRK2 polarity</td><td colspan="1" rowspan="1">TIMx_BDTR</td><td colspan="1" rowspan="1">BKP or BK2P</td><td colspan="1" rowspan="1">1 (active high), it means that the externalsignal goes high during the fault</td></tr><tr><td colspan="1" rowspan="1">Comparator output polarity</td><td colspan="1" rowspan="1">COMPx_CSR</td><td colspan="1" rowspan="1">COMPxPOL</td><td colspan="1" rowspan="1">0 (not inverted), comparators inputconnected as shown in previous sections</td></tr><tr><td colspan="1" rowspan="1">TIM1/8/20 BKIN/BKIN2 AF</td><td colspan="1" rowspan="1">GPIOxAFRL orGPIOXAFRH</td><td colspan="1" rowspan="1"></td><td colspan="1" rowspan="1">AF enabled on BKIN/BKIN2 pin selectedamong available</td></tr><tr><td colspan="1" rowspan="1">TIM1/8/20 BRK/BRK2 enable</td><td colspan="1" rowspan="1">TIMX_BDTR</td><td colspan="1" rowspan="1">BKEor BK2E</td><td colspan="1" rowspan="1">1</td></tr><tr><td colspan="1" rowspan="1">COMPx out selection</td><td colspan="1" rowspan="1">COMPx_CSR</td><td colspan="1" rowspan="1">COMPxOUTSEL</td><td colspan="1" rowspan="1">0001: TIM1 BRK0010: TIM1 BRK20011: TIM8 BRK0100: TIM8 BRK20101: TIM1 BRK2 + TIM8 BRK21100: TIM20 BRK1101: TIM20 BRK21110: TIM1 BRK2 + TIM8 BRK2 + TIM20BRK2</td></tr></table>

Tblla u or open-drain mode, for signaling to other devices or for debugging purposes.

![](images/fcc14dbed3390cf058ed434866d70b74fc2319d4c0c4ef597609de12ba343c92.jpg)  
Figure 12. Combining external and internal protection concept

# 6.4

# Filtering the break input

Pbleble events (switching noise for instance).

Thdigital filer eatur savailableon BRKand BRK. It is ot availablen BRKACTH.That means ha he digital filter is:

available when the break source is external and comes from the external inputs BKIN/BKIN2.   
available when the break source is internal and connected to BRK or BRK2.   
not available when the break source is internal and connected to BRK_ACTH.

# 6.5

# Locking the selected configuration

Elelmoi bile tn a caused in case of failure.

To increase robustness against software runaways, many STM32 microcontrollers come with a chain of peripherals featuring the lock feature, begining from the mode of the GPO pins used or sensing through coparators, perational amplifiers (OPAMP), and advanced timers, down to the GPIO pins used or driving, as shown in Figure 13.

In particular, BRK and BRK2 configurations can be locked using the LOCK bits in the TIMx_BDTR register. At least LOCK level 1 is recommended to freeze DTG/BKE/BKP/AOE/BKF/BK2F/BK2E/BK2P bits in the TIMx_BDTR register and OISx/OISxN bits in the TIMx_CR2 register until the next reset.

![](images/4790026dd5ad3e3f101942cab506d3e5725da4d4ea3d282c9c4958b591584aba.jpg)  
Figure 13. Comparator chain configuration locking

Table 9 summarizes the recommended settings for comparators.   
Table 9. Register locking mechanism   

<table><tr><td rowspan=1 colspan=1>Peripheral</td><td rowspan=1 colspan=1>Feature</td><td rowspan=1 colspan=1>Register</td><td rowspan=1 colspan=1>Comment</td></tr><tr><td rowspan=1 colspan=1>GPIO port x, pin y</td><td rowspan=1 colspan=1>Inverting input, pinmode selection</td><td rowspan=1 colspan=1>GPIOx_MODER register, MODERy bit tobe configured in analog mode</td><td rowspan=1 colspan=1></td></tr><tr><td rowspan=1 colspan=1>GPIO port x, pin y</td><td rowspan=1 colspan=1>Inverting input, pinconfigurationlocking</td><td rowspan=1 colspan=1>GPIOx_LCKR register, specific writesequence coded with LCKy bit</td><td rowspan=1 colspan=1>MODERy bit (in GPIOx_MODERregister) now frozen until next reset</td></tr><tr><td rowspan=1 colspan=1>GPIO port w, pin z</td><td rowspan=1 colspan=1>Non inverting input,pin mode selection</td><td rowspan=1 colspan=1>GPIOw_MODER register, MODERz bitto be configured in analog mode</td><td rowspan=1 colspan=1>Not needed if an internal reference isselected</td></tr><tr><td rowspan=1 colspan=1>GPIO port w, pin z</td><td rowspan=1 colspan=1>Non inverting input,pin configurationlocking</td><td rowspan=1 colspan=1>GPIOw_LCKR register, specific writesequence coded with LCKz bit</td><td rowspan=1 colspan=1>MODERz bit (in the GPIOw_MODERregister) now frozen until next reset</td></tr><tr><td rowspan=1 colspan=1>TIMER 1/8/20</td><td rowspan=1 colspan=1>BKIN/BKIN2configurationlocking</td><td rowspan=1 colspan=1>TIMx_BDTR register, LOCK bits</td><td rowspan=1 colspan=1>LOCK level 1 (at least) recommended:DTG bits in TIMx_BDTR register, OISx,and OISxN bits in TIMx_CR2 registerand BKE/BKP/AOE bits in TIMx_BDTRregister frozen until next reset</td></tr></table>

# Appendix A

# A.1

# How to use the DAC to define thresholds

on  o input voltage (V) to define the threshold levels for overcurrent protection and overvoltage protection.

An external reference (GPIO) A fixed internal reference (Vref, ½/4 Vref, 1½ Vref, 1½4 Vref) A programmable internal reference (DAC)

![](images/9bd270048ac54bea9c95559042ec116c3b312abc67afcea9bebb1ac9067980aa.jpg)  
Figure 14. Inverting input selection

# Practical example: overcurrent protection using the offset network

T she a guwhee nsie heot  o pen In formula to compute the overcurrent threshold is the following:

![](images/149341eb45f03cd3b6cba9838c7c0dc379f40874fd2b757ef496dafea616208a.jpg)

sl l eh si reference for V- can lead to a threshold value Ith, which is not exactly coincident with the requiredone. Ae al heovercuet reholOhewi seceary hexteal erenchevaribll reference. The latter is recommended, because it does not require any external components.

Many STM32 microcontrollers include two -bit DAC channels that can be used for this purpose. For tree-overcurrent by setting the same DAC channel for all three inverter inputs.

T v of protection, one for each motor.

# Revision history

Table 10. Document revision history   

<table><tr><td colspan="1" rowspan="1">Date</td><td colspan="1" rowspan="1">Revision</td><td colspan="1" rowspan="2">ChangesInitial release.</td></tr><tr><td colspan="1" rowspan="1">25-Nov-2013</td><td colspan="1" rowspan="1">1</td></tr><tr><td colspan="1" rowspan="1">05-Mar-2015</td><td colspan="1" rowspan="1">2</td><td colspan="1" rowspan="1">Updated cover page with STM32F3 series and adding RM references.Updated the whole document adding TIM20 and replacing STM32F30x/31 x bySTM32F3 series.Updated Section 1: Break function overview adding Table 3: Peripherals availability perSTM32 devices.Updated Figure 1: Break feature implementation for TIM1, TIM8, and TIM20.Updated Figure 11: Comparator chain configuration locking.Updated Table 9: Register locking mechanism.</td></tr><tr><td colspan="1" rowspan="1">30-Jun-2015</td><td colspan="1" rowspan="1">3</td><td colspan="1" rowspan="1">Updated Section 2.2: TIM15/16/17 break implementation removing the filter feature inBRK and BRK_ACTH paragraphs.Updated Figure 5: Break feature implementation for TIM15, TIM16, and TIM17 forSTM32F1 series devices replacing filter/polarity by polarity.Updated Table 4: Break input sources adding "NA for TIM15/16/17" for 2 lines in BRKcolumn.</td></tr><tr><td colspan="1" rowspan="1">03-May-2016</td><td colspan="1" rowspan="1">4</td><td colspan="1" rowspan="1">Updated cover page title and introduction with the application note applying to STM32devices.Added Table 1: Applicable products.Updated Section 1: Break function overview.Added Table 2: Timers and break input availability in STM32 devices.Updated Table 3: Peripherals availability per STM32 devices.Updated Section 2: Break implementation.Updated Figure 1, Figure 2, Figure 3, Figure 5, Figure 6, and Figure 7.Updated Table 4: Break input sources.Updated Table 5: Scenarios of PWM output status in response to internal/external breakevents.Updated Section 5: Using the break function with other MCU resources adding a note.Updated Section: BRK_ATCH.Added Section: Bidirectional break inputs.Added Figure 4: Output redirection.</td></tr><tr><td colspan="1" rowspan="1">09-Mar-2022</td><td colspan="1" rowspan="1">5</td><td colspan="1" rowspan="1">Updated all document with STM32U series in:Section 1: General informationSection 4: Break implementationSection 5: Break sources summarySection 7: Using the break function with other MCU resourcesAdded:Figure 4: Break feature implementation in advanced timers for STM32U5 series devicesFigure 9: Break feature implementation for TIM15, TIM16, and TIM17 in STM32U5series devices</td></tr><tr><td colspan="1" rowspan="1">05-Jan-2023</td><td colspan="1" rowspan="1">6</td><td colspan="1" rowspan="1">Updated the whole document to add STM32 series information in:Section Table 1: Applicable productsSection Table 3: Timers and break input availability in STM32 devicesSection Table 4: Comparator peripherals availability per STM32 deviceSection 4.1: TIM1/8/20 break implementationSection 4.2: TIM15/16/17 break implementationSection 5: Break sources summary</td></tr><tr><td colspan="1" rowspan="1">06-Mar-2024</td><td colspan="1" rowspan="1">7</td><td colspan="1" rowspan="1">Added STM32U0 series.Updated:Document titleTable 2. Timers and break input availability in STM32 devicesTable 3. Comparator peripherals availability per STM32 device</td></tr><tr><td>Date</td><td>Revision</td><td>Changes</td></tr><tr><td>20-Feb-2025</td><td>8</td><td>Added STM32U3 series. Updated: Section Introduction Section 2: Break function overview Section 3.1: TIM1/8/20 break implementation</td></tr></table>

# Contents

General information   
2 Break function overview 3   
3 Break implementation 5   
3.1 TIM1/8/20 break implementation. . 5   
3.2 TIM15/16/17 break implementation. .9   
4 Break sources summary .12   
5 Examples. ..13   
6 Using the break function with other MCU resources . .15   
6.1 Break function used for overcurrent protection .15   
6.2 Break function used for overvoltage protection .16   
6.3 Using an external emergency signal together with the internal comparator. .16   
6.4 Filtering the break input .18   
6.5 Locking the selected configuration .19   
A.1 How to use the DAC to define thresholds .20   
Revision history . 21   
List of tables .. .24   
List of figures. .25

# List of tables

Table 1. Applicable products   
Table 2. Timers and break input availability in STM32 devices 3   
Table 3. Comparator peripherals availability per STM32 device 4   
Table 4. Break input sources 12   
Table 5. Scenarios of PWM output status in response to internal/external break events. 13   
Table 6. Comparator output connected internally to break inputs 17   
Table 7. Comparator output connected externally to break inputs, with low break polarity 17   
Table 8. Comparator output connected externally to break inputs, with high break polarity. 17   
Table 9. Register locking mechanism 19   
Table 10. Document revision history . 21

# List of figures

Figure 1. Break feature implementation in advanced timers for STM32F0/F1/F2/F4/F7 series devices. 6   
Figure 2. Break feature implementation in advanced timers for STM32F3 series devices . 7   
Figure 3. Break feature implementation in advanced timers for STM32L4 series devices . 8   
Figure 4. Break feature implementation in advanced timers for STM32U5 series devices. 8   
Figure 5. Output redirection . 9   
Figure 6. Break feature implementation for TIM15, TIM16, and TIM17 for STM32F1 series devices 10   
Figure 7. Break feature implementation for TIM15, TIM16, and TIM17 for STM32F3 series devices 10   
Figure 8. Break feature implementation for TIM15, TIM16, and TIM17 for STM32L4 and STM32H7 series devices 11   
Figure 9. Break feature implementation for TIM15, TIM16, and TIM17 in STM32U5 series devices 11   
Figure 10. Overcurrent protection network implementation block diagram 15   
Figure 11. Overvoltage protection network block diagram 16   
Figure 12. Combining external and internal protection concept. 18   
Figure 13. Comparator chain configuration locking 19   
Figure 14. Inverting input selection. 20

# IMPORTANT NOTICE  READ CAREFULLY

pt old ursant  dits   leole.

purchasers' products.

No license, express or implied, to any intellectual property right is granted by ST herein.

are the property of their respective owners.

I

© 2025 STMicroelectronics - All rights reserved