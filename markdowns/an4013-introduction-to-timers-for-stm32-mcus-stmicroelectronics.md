# Introduction

The purpose of this document is to:

• Present an overview of the timer peripherals for the STM32 product series listed in Table 1. Describe the various modes and specific timer features, such as clock sources. Explain how to use the available modes and features. Explain how to compute the time base in each configuration. Describe the timer synchronization sequences and the advanced features for motor control applications, in addition to the general-purpose timer modes.

For each mode, the document provides typical configurations and implementation examples.

In the rest of this document (unless otherwise specified), the term STM32xx series is used to refer to the product series listed in Table 1.

Table 1. Applicable products   

<table><tr><td>Type</td><td>Product series</td></tr><tr><td>Microcontrollers</td><td>STM32C0 series, STM32F0 series, STM32F1 series, STM32F2 series, STM32F3 series, STM32F4 series, STM32F7 series, STM32G0 series, STM32G4 series, STM32H5 series, STM32H7 series, STM32N6 series, STM32L0 series, STM32L1 series, STM32L4 series, STM32L5 series, STM32U0 series, STM32U3 series, STM32U5 series, STM32WB series, STM32WB0 series, STM32WL series</td></tr></table>

# Contents

Overview 6

# General-purpose timer modes . . . . 11

2.1 Clock input sources 11   
2.1.1 Internal clock 11   
2.1.2 External clock 11   
2.2 Time base generator 12   
2.3 Timer input capture mode 14   
2.4 Timer in output compare mode 15   
2.5 Timer in PWM mode . 16   
2.6 Timer in one pulse mode 17   
2.7 Timer in asymmetric PWM mode 18   
2.8 Timer in combined PWM mode 20   
2.9 Retriggerable one pulse mode 22   
2.10 PWM analysis mode . 23

# Timer synchronization . 25

3.1 Timer system link 25   
3.2 Master configuration . 25   
3.3 Slave configuration . 27

# Advanced features for motor control .. 28

4.1 Signal generation 28   
4.2 Combined three-phase PWM mode 30   
4.3 Specific features for motor control applications 31   
4.3.1 Complementary signal and deadtime feature .31   
4.3.2 Break input . 32   
4.3.3 Locking mechanism 34   
4.3.4 Specific features for feedback measurement .35

# High-resolution timer applications . 39

Low-power timer 40

6.1 Wake-up timer implementation . .. 40   
6.2 Pulse counter . 41

# Specific applications . . . . 42

7.1 Infrared application . . 42   
7.2 3-phase AC and PMSM control motor 42   
7.3 Six-step mode 42

Revision history . 44

# List of tables

Table 1. Applicable products 1   
Table 2. Simplified overview of timer availability in STM32Fx products 7   
Table 3. Simplified overview of timer availability in STM32Lx products 8   
Table 4. Simplified overview of timer availability in STM32Cx/Gx/Hx/Nx/Ux/Wx products. .9   
Table 5. Timer features overview 10   
Table 6. Advanced timer configurations 29   
Table 7. Behavior of timer outputs versus Break1 and Break2 inputs 33   
Table 8. Locking levels . . 34   
Table 9. Document revision history 44

# List of figures

Figure 1. Asymmetric PWM mode versus center aligned PWM mode 19   
Figure 2. Combined PWM mode 21   
Figure 3. Retriggerable OPM mode . 23   
Figure 4. Timer system link . 25   
Figure 5. Combined three-phase PWM . 30   
Figure 6. Two signals are generated with insertion of a deadtime. 31   
Figure 7. Position at X4 resolution . 35   
Figure 8. Position at X2 resolution . 36   
Figure 9. Output waveform of a typical Hall sensor. 37   
Figure 10. Commutation sequence 38

# 1 Overview

The ST32xx series devices, based on the Arm® cores(), have various built-in timers outlined as follows;

General-purpose timers are used with any application for: output comparison (timing and delay generation), one-pulse mode, input capture (for external signal frequency measurement), sensor interface (encoder, hall sensor). Advanced timers: these timers have the most features. In addition to general purpose functions, they include several features related to motor control and digital power conversion applications: three complementary signals with deadtime insertion and emergency shut-down input.   
C One or two channel timers: used as general-purpose timers with a limited number of channels.   
• One or two channel timers with complementary output: same as the previous timer type with an additional deadtime generator on one channel. In some situations, this feature allows a general purpose timer to be used where an additional advanced timer would be necessary. Basic timers are used either as timebase timers or for triggering the DAC peripheral. These timers do not have any input or output capabilities. Low-power timers are simple general purpose timers and are able to operate in lowpower modes. They are used to generate a wake-up event for example. High-resolution timers are specialized timer peripherals designed to drive power conversion in lighting and power source applications. They can also be used in other fields that require very fine timing resolution. AN4885, AN4539, and AN4449 are practical examples of high-resolution timer use.

Table 2, Table 3 and Table 4 summarize the STM32 family timers.

Table 5 presents a general overview of timer features.

Timers are enhanced with more advanced features in newer devices. Besides minor changes not in scope of this overview, a significant update divides the STM32 family advanced motor control and general purpose timers. In this document STM32F0/F1/F2/F4 series and STM32F37x devices are referred to as the "original series". Some of the features are not available for them and are identified as such.

![](images/5774ceedd403a8c0663f2ad0198e20cde7b1af30471f0408d982b5b02911fa69.jpg)

Table 2. Simplified overview of timer availability in STM32Fx products   

<table><tr><td rowspan=1 colspan=2>Timer type</td><td rowspan=1 colspan=1>202020</td><td rowspan=1 colspan=1>2020(00 Dunx)</td><td rowspan=1 colspan=1>202020</td><td rowspan=1 colspan=1>202020</td><td rowspan=1 colspan=1>2020</td><td rowspan=1 colspan=1>202020</td><td rowspan=1 colspan=1>2020</td><td rowspan=1 colspan=1>2020</td><td rowspan=1 colspan=1>20</td><td rowspan=1 colspan=1>20</td><td rowspan=1 colspan=1>20</td><td rowspan=1 colspan=1>20</td></tr><tr><td rowspan=1 colspan=2>Advanced</td><td rowspan=1 colspan=1>TIM1</td><td rowspan=1 colspan=1>TIM1</td><td rowspan=1 colspan=1>TIM1(1)TIM8(1)</td><td rowspan=1 colspan=1>TIM1(1)TIM8(1)</td><td rowspan=1 colspan=1>TIM1</td><td rowspan=1 colspan=1>TIM1TIM8</td><td rowspan=1 colspan=1>TIM1</td><td rowspan=1 colspan=1>TIM1TIM8(1)TIM20(1)</td><td rowspan=1 colspan=1></td><td rowspan=1 colspan=1>TIM1</td><td rowspan=1 colspan=1>TIM1TIM8(1)</td><td rowspan=1 colspan=1>TIM1TIM8</td></tr><tr><td rowspan=2 colspan=1>Generalpurpose</td><td rowspan=1 colspan=1>32-bit</td><td rowspan=1 colspan=1>TIM2</td><td rowspan=1 colspan=1>TIM2</td><td rowspan=1 colspan=1>-</td><td rowspan=1 colspan=1>-</td><td rowspan=1 colspan=1>-</td><td rowspan=1 colspan=1>TIM2TIM5</td><td rowspan=1 colspan=1>TIM2(1)TIM5</td><td rowspan=1 colspan=1>TIM2</td><td rowspan=1 colspan=1>TIM2TIM5</td><td rowspan=1 colspan=1>TIM2</td><td rowspan=1 colspan=1>TIM2</td><td rowspan=1 colspan=1>TIM2TIM5</td></tr><tr><td rowspan=1 colspan=1>16-bit</td><td rowspan=1 colspan=1>TIM3</td><td rowspan=1 colspan=1>TIM3</td><td rowspan=1 colspan=1>TIM2TIM3TIM4TIM5</td><td rowspan=1 colspan=1>TIM2TIM3TM4(1)TIM5(1)</td><td rowspan=1 colspan=1>TIM2TIM3TIM4TIM5(1)</td><td rowspan=1 colspan=1>TIM3TIM4</td><td rowspan=1 colspan=1>TIM3(1)TIM4(1)</td><td rowspan=1 colspan=1>TIM3(1)TIM4(1)TIM19(1)</td><td rowspan=1 colspan=1>TIM3TIM4TIM19</td><td rowspan=1 colspan=1>TIM3</td><td rowspan=1 colspan=1>TIM3TIM4</td><td rowspan=1 colspan=1>TIM3TIM4</td></tr><tr><td rowspan=1 colspan=2>Basic</td><td rowspan=1 colspan=1></td><td rowspan=1 colspan=1>TIM6TM7(1)</td><td rowspan=1 colspan=1>TIM6TIM7</td><td rowspan=1 colspan=1>TIM6(1)IM7(1)</td><td rowspan=1 colspan=1>TIM6TIM7</td><td rowspan=1 colspan=1>TIM6TIM7</td><td rowspan=1 colspan=1>TIM6(1)</td><td rowspan=1 colspan=1>TIM6IM7(1)</td><td rowspan=1 colspan=1>TIM6TIM7TIM18</td><td rowspan=1 colspan=1>TIM6TIM7</td><td rowspan=1 colspan=1>TIM6TIM(1)</td><td rowspan=1 colspan=1>TIM6TIM7</td></tr><tr><td rowspan=1 colspan=2>1-channel</td><td rowspan=1 colspan=1>TIM14</td><td rowspan=1 colspan=1>TIM14</td><td rowspan=1 colspan=1>TIM10TIM11TIM13TIM14</td><td rowspan=1 colspan=1>-</td><td rowspan=1 colspan=1>TIM13(1)TIM1(1)</td><td rowspan=1 colspan=1>TIM10TIM11TIM13TIM14</td><td rowspan=1 colspan=1>TIM10(1)TIM11</td><td rowspan=1 colspan=1>-</td><td rowspan=1 colspan=1>TIM13TIM14</td><td rowspan=1 colspan=1>-</td><td rowspan=1 colspan=1>-</td><td rowspan=1 colspan=1>TIM10TIM11TIM13TIM14</td></tr><tr><td rowspan=1 colspan=2>2-channel</td><td rowspan=1 colspan=1></td><td rowspan=1 colspan=1>-</td><td rowspan=1 colspan=1>TIM9TIM12</td><td rowspan=1 colspan=1></td><td rowspan=1 colspan=1>TIM12(1)</td><td rowspan=1 colspan=1>TIM9TIM12</td><td rowspan=1 colspan=1>TIM9</td><td rowspan=1 colspan=1>-</td><td rowspan=1 colspan=1>TIM12</td><td rowspan=1 colspan=1>-</td><td rowspan=1 colspan=1></td><td rowspan=1 colspan=1>TIM9TIM12</td></tr><tr><td rowspan=1 colspan=2>2-channel withcomplementaryoutput</td><td rowspan=1 colspan=1>-</td><td rowspan=1 colspan=1>TIM15</td><td rowspan=1 colspan=1>-</td><td rowspan=1 colspan=1>-</td><td rowspan=1 colspan=1>TIM15</td><td rowspan=1 colspan=1>-</td><td rowspan=1 colspan=1>-</td><td rowspan=1 colspan=1>TIM15</td><td rowspan=1 colspan=1>TIM15</td><td rowspan=1 colspan=1>TIM15</td><td rowspan=1 colspan=1>TIM15</td><td rowspan=1 colspan=1>-</td></tr><tr><td rowspan=1 colspan=2>1-channel withcomplementaryoutput</td><td rowspan=1 colspan=1>TIM16TIM17</td><td rowspan=1 colspan=1>TIM16TIM17</td><td rowspan=1 colspan=1></td><td rowspan=1 colspan=1></td><td rowspan=1 colspan=1>TIM16TIM17</td><td rowspan=1 colspan=1>-</td><td rowspan=1 colspan=1></td><td rowspan=1 colspan=1>TIM16TIM17</td><td rowspan=1 colspan=1>TIM16TIM17</td><td rowspan=1 colspan=1>TIM16TIM17</td><td rowspan=1 colspan=1>TIM16TIM17</td><td rowspan=1 colspan=1>-</td></tr><tr><td rowspan=1 colspan=2>Low-power timer</td><td rowspan=1 colspan=1>-</td><td rowspan=1 colspan=1>-</td><td rowspan=1 colspan=1>-</td><td rowspan=1 colspan=1>-</td><td rowspan=1 colspan=1>-</td><td rowspan=1 colspan=1>-</td><td rowspan=1 colspan=1>LPTIM1(1)</td><td rowspan=1 colspan=1>-</td><td rowspan=1 colspan=1>-</td><td rowspan=1 colspan=1>-</td><td rowspan=1 colspan=1>-</td><td rowspan=1 colspan=1>LPTIM1</td></tr><tr><td rowspan=1 colspan=2>High-resolution timer</td><td rowspan=1 colspan=1>-</td><td rowspan=1 colspan=1>-</td><td rowspan=1 colspan=1>-</td><td rowspan=1 colspan=1>-</td><td rowspan=1 colspan=1>-</td><td rowspan=1 colspan=1>-</td><td rowspan=1 colspan=1>-</td><td rowspan=1 colspan=1>-</td><td rowspan=1 colspan=1>-</td><td rowspan=1 colspan=1>HRTIM</td><td rowspan=1 colspan=1>-</td><td rowspan=1 colspan=1>-</td></tr></table>

Not available on all products in the line. Check the datasheet for details T.

Table 3.Simplified overview of timer availability in STM32Lx products   

<table><tr><td rowspan=1 colspan=2>Timer type</td><td rowspan=1 colspan=1>STM32L05X/L06x/L07x/L08x lines</td><td rowspan=1 colspan=1>STM32L0x0Value line</td><td rowspan=1 colspan=1>STM32L0x3/L0x2/L0x1 lines</td><td rowspan=1 colspan=1>STM32L1 series</td><td rowspan=1 colspan=1>STM32L4 series</td><td rowspan=1 colspan=1>STM32L5 series</td></tr><tr><td rowspan=1 colspan=2>Advanced</td><td rowspan=1 colspan=1></td><td rowspan=1 colspan=1></td><td rowspan=1 colspan=1></td><td rowspan=1 colspan=1></td><td rowspan=1 colspan=1>TIM1,TIM8(1)</td><td rowspan=1 colspan=1>TIM1TIM8</td></tr><tr><td rowspan=2 colspan=1>General purpose</td><td rowspan=1 colspan=1>32-bit</td><td rowspan=1 colspan=1></td><td rowspan=1 colspan=1></td><td rowspan=1 colspan=1></td><td rowspan=1 colspan=1>TIM5(1)</td><td rowspan=1 colspan=1>TIM2TIM5(1)</td><td rowspan=1 colspan=1>TIM2TIM5</td></tr><tr><td rowspan=1 colspan=1>16-bit</td><td rowspan=1 colspan=1>TIM2TIM3(1)</td><td rowspan=1 colspan=1>TIM2</td><td rowspan=1 colspan=1>TIM2</td><td rowspan=1 colspan=1>TIM2TIM3TIM4</td><td rowspan=1 colspan=1>TIM3(1)TIM4(1)</td><td rowspan=1 colspan=1>TIM3TIM4</td></tr><tr><td rowspan=1 colspan=2>Basic</td><td rowspan=1 colspan=1>TIM6 TIM7(1)</td><td rowspan=1 colspan=1></td><td rowspan=1 colspan=1></td><td rowspan=1 colspan=1>TIM6TIM7</td><td rowspan=1 colspan=1>TIM6 TIM7(1)</td><td rowspan=1 colspan=1>TIM6TIM7</td></tr><tr><td rowspan=1 colspan=2>1-channel</td><td rowspan=1 colspan=1>-</td><td rowspan=1 colspan=1></td><td rowspan=1 colspan=1>-</td><td rowspan=1 colspan=1>TIM10TIM11</td><td rowspan=1 colspan=1>-</td><td rowspan=1 colspan=1>-</td></tr><tr><td rowspan=1 colspan=2>2-channel</td><td rowspan=1 colspan=1>TIM21TIM22</td><td rowspan=1 colspan=1>TIM21</td><td rowspan=1 colspan=1>TIM21 T2(1)</td><td rowspan=1 colspan=1>TIM9</td><td rowspan=1 colspan=1></td><td rowspan=1 colspan=1>-</td></tr><tr><td rowspan=1 colspan=2>2-channel with complementaryoutput</td><td rowspan=1 colspan=1>-</td><td rowspan=1 colspan=1></td><td rowspan=1 colspan=1></td><td rowspan=1 colspan=1></td><td rowspan=1 colspan=1>TIM15</td><td rowspan=1 colspan=1>TIM15</td></tr><tr><td rowspan=1 colspan=2>1-channel with complementaryoutput</td><td rowspan=1 colspan=1></td><td rowspan=1 colspan=1></td><td rowspan=1 colspan=1></td><td rowspan=1 colspan=1></td><td rowspan=1 colspan=1>TIM16 TIM17(1)</td><td rowspan=1 colspan=1>TIM16TIM17</td></tr><tr><td rowspan=1 colspan=2>Low-power timer</td><td rowspan=1 colspan=1>LPTIM1</td><td rowspan=1 colspan=1>LPTIM1</td><td rowspan=1 colspan=1>LPTIM1</td><td rowspan=1 colspan=1></td><td rowspan=1 colspan=1>LPTIM1LPTIM2</td><td rowspan=1 colspan=1>LPTIM1LPTIM2LPTIM3</td></tr><tr><td rowspan=1 colspan=2>High-resolution timer</td><td rowspan=1 colspan=1>-</td><td rowspan=1 colspan=1>-</td><td rowspan=1 colspan=1>-</td><td rowspan=1 colspan=1>-</td><td rowspan=1 colspan=1>-</td><td rowspan=1 colspan=1>-</td></tr></table>

Not available on all products in the line. Check the datasheet for details.

Table 4. Simplified overview of timer availability in STM32Cx/Gx/Hx/Nx/Ux/Wx products   
20   

<table><tr><td rowspan=1 colspan=2>Timer type</td><td rowspan=1 colspan=1>20</td><td rowspan=1 colspan=1>20</td><td rowspan=1 colspan=1>20</td><td rowspan=1 colspan=1>20</td><td rowspan=1 colspan=1>20</td><td rowspan=1 colspan=1>2022X∀X</td><td rowspan=1 colspan=1>20</td><td rowspan=1 colspan=1>20</td><td rowspan=1 colspan=1>20</td><td rowspan=1 colspan=1>Sas SS</td><td rowspan=1 colspan=1>20</td><td rowspan=1 colspan=1>20</td><td rowspan=1 colspan=1>20</td><td rowspan=1 colspan=1>20</td></tr><tr><td rowspan=1 colspan=2>Advanced</td><td rowspan=1 colspan=1>TIM1</td><td rowspan=1 colspan=1>TIM1</td><td rowspan=1 colspan=1>TIM1TIM8TIM20(1)</td><td rowspan=1 colspan=1>TIM1</td><td rowspan=1 colspan=1>TIM1TIM8</td><td rowspan=1 colspan=1>TIM1TIM8</td><td rowspan=1 colspan=1>TIM1</td><td rowspan=1 colspan=1>TIM1TIM8</td><td rowspan=1 colspan=1>TIM1</td><td rowspan=1 colspan=1>TIM1</td><td rowspan=1 colspan=1>TIM1TIM8</td><td rowspan=1 colspan=1>TIM1</td><td rowspan=1 colspan=1>TIM1(1)</td><td rowspan=1 colspan=1>TIM1(1)</td></tr><tr><td rowspan=2 colspan=1>Generalpurpose</td><td rowspan=1 colspan=1>32-bit</td><td rowspan=1 colspan=1>-</td><td rowspan=1 colspan=1>TIM2</td><td rowspan=1 colspan=1>TIM2TIM5(1)</td><td rowspan=1 colspan=1>TIM2</td><td rowspan=1 colspan=1>TIM2TIM5</td><td rowspan=1 colspan=1>TIM2TIM5TM23(1)TIM24(1)</td><td rowspan=1 colspan=1>TIM2TIM3TIM4TIM5</td><td rowspan=1 colspan=1>TIM2TIM3TIM4TIM5</td><td rowspan=1 colspan=1>TIM2</td><td rowspan=1 colspan=1>TIM2TIM3TIM4</td><td rowspan=1 colspan=1>TIM2TIM3TIM4TIM5</td><td rowspan=1 colspan=1>TIM2</td><td rowspan=1 colspan=1>TIM2(1)</td><td rowspan=1 colspan=1>TIM2(1)</td></tr><tr><td rowspan=1 colspan=1>16-bit</td><td rowspan=1 colspan=1>TIM3</td><td rowspan=1 colspan=1>TIM3</td><td rowspan=1 colspan=1>TIM3TIM4</td><td rowspan=1 colspan=1>TIM3</td><td rowspan=1 colspan=1>TIM3TIM4</td><td rowspan=1 colspan=1>TIM3TIM4</td><td rowspan=1 colspan=1>-</td><td rowspan=1 colspan=1>-</td><td rowspan=1 colspan=1>TIM3</td><td rowspan=1 colspan=1>-</td><td rowspan=1 colspan=1>-</td><td rowspan=1 colspan=1>-</td><td rowspan=1 colspan=1>-</td><td rowspan=1 colspan=1>_(1)</td></tr><tr><td rowspan=1 colspan=2>Basic</td><td rowspan=1 colspan=1>-</td><td rowspan=1 colspan=1>TIM6TIM7</td><td rowspan=1 colspan=1>TIM6TIM7</td><td rowspan=1 colspan=1>TIM6TIM7</td><td rowspan=1 colspan=1>TIM6TIM7</td><td rowspan=1 colspan=1>TIM6TIM7</td><td rowspan=1 colspan=1>TIM6TIM7</td><td rowspan=1 colspan=1>TIM6TIM7TIM18</td><td rowspan=1 colspan=1>TIM6TIM7</td><td rowspan=1 colspan=1>TIM6TIM7</td><td rowspan=1 colspan=1>TIM6TIM7</td><td rowspan=1 colspan=1>-</td><td rowspan=1 colspan=1>-</td><td rowspan=1 colspan=1>-</td></tr><tr><td rowspan=1 colspan=2>1-channel</td><td rowspan=1 colspan=1>TIM14</td><td rowspan=1 colspan=1>TIM14</td><td rowspan=1 colspan=1>-</td><td rowspan=1 colspan=1>-</td><td rowspan=1 colspan=1>TIM13TIM14</td><td rowspan=1 colspan=1>TIM13TIM14</td><td rowspan=1 colspan=1>TIM13TIM14</td><td rowspan=1 colspan=1>TIM10TIM11TIM13TIM14</td><td rowspan=1 colspan=1></td><td rowspan=1 colspan=1></td><td rowspan=1 colspan=1>-</td><td rowspan=1 colspan=1></td><td rowspan=1 colspan=1></td><td rowspan=1 colspan=1>-</td></tr><tr><td rowspan=1 colspan=2>2-channel</td><td rowspan=1 colspan=1></td><td rowspan=1 colspan=1>-</td><td rowspan=1 colspan=1>-</td><td rowspan=1 colspan=1></td><td rowspan=1 colspan=1>TIM12</td><td rowspan=1 colspan=1>TIM12</td><td rowspan=1 colspan=1>TIM9TIM12</td><td rowspan=1 colspan=1>TIM9TIM12</td><td rowspan=1 colspan=1></td><td rowspan=1 colspan=1></td><td rowspan=1 colspan=1></td><td rowspan=1 colspan=1></td><td rowspan=1 colspan=1></td><td rowspan=1 colspan=1></td></tr><tr><td rowspan=1 colspan=2>2-channel withcomplementaryoutput</td><td rowspan=1 colspan=1></td><td rowspan=1 colspan=1>TIM15</td><td rowspan=1 colspan=1>TIM15</td><td rowspan=1 colspan=1></td><td rowspan=1 colspan=1>TIM15</td><td rowspan=1 colspan=1>TIM15</td><td rowspan=1 colspan=1>TIM15</td><td rowspan=1 colspan=1>TIM15</td><td rowspan=1 colspan=1>TIM15</td><td rowspan=1 colspan=1>TIM15</td><td rowspan=1 colspan=1>TIM15</td><td rowspan=1 colspan=1></td><td rowspan=1 colspan=1></td><td rowspan=1 colspan=1>-</td></tr><tr><td rowspan=1 colspan=2>1-channel withcomplementaryoutput</td><td rowspan=1 colspan=1>TIM16TIM17</td><td rowspan=1 colspan=1>TIM16TIM17</td><td rowspan=1 colspan=1>TIM16TIM17</td><td rowspan=1 colspan=1></td><td rowspan=1 colspan=1>TIM 16TIM 17</td><td rowspan=1 colspan=1>TIM16TIM17</td><td rowspan=1 colspan=1>TIM16TIM17</td><td rowspan=1 colspan=1>TIM16TIM17</td><td rowspan=1 colspan=1>TIM16</td><td rowspan=1 colspan=1>TIM16TIM17</td><td rowspan=1 colspan=1>TIM16TIM17</td><td rowspan=1 colspan=1>TIM16TIM17</td><td rowspan=1 colspan=1>TIM16(1) TIMM1(1)</td><td rowspan=1 colspan=1>TIM16 TIM17(1)</td></tr><tr><td rowspan=1 colspan=2>Low-power timer(2)</td><td rowspan=1 colspan=1>-</td><td rowspan=1 colspan=1>LPTIM1(1)LLPTIM2(1)</td><td rowspan=1 colspan=1>LPTIM1LPTIM2</td><td rowspan=1 colspan=1>LPTIM1LPTIM2</td><td rowspan=1 colspan=1>LPTIM1LPTIM2LPTIM3LPTIM4LPTIM5LLPTIM6</td><td rowspan=1 colspan=1>LPTIM1LPTIM2LPTIM3L LPTIM(1)LPTIM()</td><td rowspan=1 colspan=1>LPTIM1LPTIM2LPTIM3LPTIM4LPTIM5</td><td rowspan=1 colspan=1>LPTIM1LPTIM2LPTIM3LPTIM4LPTIM5</td><td rowspan=1 colspan=1>LPTIM1LPTIM2L PTI(1)</td><td rowspan=1 colspan=1>LPTIM1LPTIM2LPTIM3LPTIM4</td><td rowspan=1 colspan=1>LPTIM1LPTIM2LPTIM3LPTIM4</td><td rowspan=1 colspan=1>LPTIM1LPTIM2</td><td rowspan=1 colspan=1></td><td rowspan=1 colspan=1>LPTIM1LPTIM2 LPTIM()</td></tr><tr><td rowspan=1 colspan=2>High-resolutiontimer</td><td rowspan=1 colspan=1></td><td rowspan=1 colspan=1></td><td rowspan=1 colspan=1>HRTIM1(1)</td><td rowspan=1 colspan=1>-</td><td rowspan=1 colspan=1>-</td><td rowspan=1 colspan=1>HRTIM1(1)</td><td rowspan=1 colspan=1>-</td><td rowspan=1 colspan=1>-</td><td rowspan=1 colspan=1></td><td rowspan=1 colspan=1>-</td><td rowspan=1 colspan=1>-</td><td rowspan=1 colspan=1></td><td rowspan=1 colspan=1></td><td rowspan=1 colspan=1></td></tr></table>

Not available on all products in the line. Check the datasheet for details. Ta yp phecaaheanl .

Table 5. Timer features overview   

<table><tr><td rowspan=2 colspan=1>Timer type</td><td rowspan=2 colspan=1>Counterresolution</td><td rowspan=2 colspan=1>Counter type</td><td rowspan=2 colspan=1>DMA</td><td rowspan=2 colspan=1>Channels</td><td rowspan=2 colspan=1>Complementaryoutput channels</td><td rowspan=1 colspan=2>Synchronization</td></tr><tr><td rowspan=1 colspan=1>Master configuration</td><td rowspan=1 colspan=1>Slave configuration</td></tr><tr><td rowspan=1 colspan=1>Advanced Control</td><td rowspan=1 colspan=1>16 bit</td><td rowspan=1 colspan=1>Up, down and centeraligned</td><td rowspan=1 colspan=1>Yes</td><td rowspan=1 colspan=1>4,6(1)</td><td rowspan=1 colspan=1>3,4(1)</td><td rowspan=1 colspan=1>Yes</td><td rowspan=1 colspan=1>Yes</td></tr><tr><td rowspan=1 colspan=1>General-purpose</td><td rowspan=1 colspan=1>16 bit32 bit(2)</td><td rowspan=1 colspan=1>Up, down and centeraligned</td><td rowspan=1 colspan=1>Yes</td><td rowspan=1 colspan=1>Up to 4</td><td rowspan=1 colspan=1>0</td><td rowspan=1 colspan=1>Yes</td><td rowspan=1 colspan=1>Yes</td></tr><tr><td rowspan=1 colspan=1>Basic</td><td rowspan=1 colspan=1>16 bit</td><td rowspan=1 colspan=1>Up</td><td rowspan=1 colspan=1>Yes</td><td rowspan=1 colspan=1>0</td><td rowspan=1 colspan=1>0</td><td rowspan=1 colspan=1>Yes</td><td rowspan=1 colspan=1>No</td></tr><tr><td rowspan=1 colspan=1>1-channel</td><td rowspan=1 colspan=1>16 bit</td><td rowspan=1 colspan=1>Up</td><td rowspan=1 colspan=1>No</td><td rowspan=1 colspan=1>1</td><td rowspan=1 colspan=1>0</td><td rowspan=1 colspan=1>Yes (OC signal)</td><td rowspan=1 colspan=1>No</td></tr><tr><td rowspan=1 colspan=1>2-channel</td><td rowspan=1 colspan=1>16 bit</td><td rowspan=1 colspan=1>Up(3)</td><td rowspan=1 colspan=1>No</td><td rowspan=1 colspan=1>2</td><td rowspan=1 colspan=1>0</td><td rowspan=1 colspan=1>Yes</td><td rowspan=1 colspan=1>Yes</td></tr><tr><td rowspan=1 colspan=1>1-channel with onecomplementary output</td><td rowspan=1 colspan=1>16 bit</td><td rowspan=1 colspan=1>Up</td><td rowspan=1 colspan=1>Yes</td><td rowspan=1 colspan=1>1</td><td rowspan=1 colspan=1>1</td><td rowspan=1 colspan=1>Yes (OC signal)</td><td rowspan=1 colspan=1>No</td></tr><tr><td rowspan=1 colspan=1>2-channel with onecomplementary output</td><td rowspan=1 colspan=1>16 bit</td><td rowspan=1 colspan=1>Up</td><td rowspan=1 colspan=1>Yes</td><td rowspan=1 colspan=1>2</td><td rowspan=1 colspan=1>1</td><td rowspan=1 colspan=1>Yes</td><td rowspan=1 colspan=1>Yes</td></tr><tr><td rowspan=1 colspan=1>Low-power timer</td><td rowspan=1 colspan=1>16 bit</td><td rowspan=1 colspan=1>Up</td><td rowspan=1 colspan=1>No</td><td rowspan=1 colspan=1>1(4)</td><td rowspan=1 colspan=1>0</td><td rowspan=1 colspan=1>Yes (OC signal)</td><td rowspan=1 colspan=1>No</td></tr><tr><td rowspan=1 colspan=1>High-resolution timer</td><td rowspan=1 colspan=1>16 bit</td><td rowspan=1 colspan=1>Up</td><td rowspan=1 colspan=1>Yes</td><td rowspan=1 colspan=1>Up to 12(4)</td><td rowspan=1 colspan=1>Up to 6</td><td rowspan=1 colspan=1>Yes</td><td rowspan=1 colspan=1>Yes</td></tr></table>

connected to GPIO (not available externally).

equivalent".

# 2 General-purpose timer modes

General-purpose timers can be programmed to work in various different configurations. The following chapter is an introduction to the timer usage.

# 2.1 Clock input sources

The timer always needs a clock source. It can also be synchronized by several clocks simultaneously:

√ Internal clock.

External clock.

External mode1 (TI1 or TI2 pins) External clock mode2 (ETR pin) Internal trigger clock (ITRx).

# 2.1.1 Internal clock

By default, the timer is clocked by the internal clock provided by the RCC. To select this clock source, the TIMx_SMCR->SMS (if present) bits should be reset.

The RCC register then defines the internal clock source for the timer.

# 2.1.2 External clock

The external clock timer is divided in two categories:

External clock connected to TI1 or TI2 pins − External clock connected to ETR pin.

In these cases, the clock is provided by an external signal connected to Tlx pins or ETR pin.   
The maximum external clock frequency should be verified.

In addition to all these clock sources, the timer should be clocked with the APBx clock.

The external clocks are not directly feeding the prescaler, but they are first synchronized with the APBx clock through dedicated logical blocks.

# External clock mode1 (TI1 or TI2 pins)

In this mode, the external clocks are connected to the timer input T11 pin or TI2 pin. To do this:

Configure the timers to use the TIx pin as input:

a) Select the pin to be used by writing CCxS bits in the TIMx_CCMR1 register.   
b) Select the polarity of the input: For the STM32F100/101/102/103/105/107 lines: write CCxP in the TIMx_CCER register to select the rising or the falling edge; For the other series and lines: write CCxP and CCxNP in the TIMx_CCER register to select the rising/falling edge, or both edges(a).   
Enable the corresponding channel by setting the CCEx bit in the TIMx_CCER register.

Select the timer TIx as the trigger input source by writing TS bits in the TIMx_SMCR register.

3.Select the external clock mode1 by writing SMS=111 in the TIMx_ SMCR register.

# External clock mode2 (ETR pin)

The external clock mode2 uses the ETR pin as timer input clock. To use this feature:

1. Select the external clock mode2 by writing ECE = 1 in the TIMx_SMCR register 2. Configure, if needed, the prescaler, the filter, and the polarity by writing ETPS [1:0], ETF [3:0] and ETP in the TIMx_SMCR register.

# Internal trigger clock (ITRx)

This is a particular timer synchronization mode. When using one timer as a prescaler for another timer, the first timer update event or output compare signal is used as a clock for the second one.

# 2.2 Time base generator

The timer can be used as a time base generator. Depending on the clock, prescaler and auto reload, repetition counter (if present) parameters, the 16-bit timer can generate an update event from a nanosecond to a few minutes. The 32-bit timers provide a wider range.

# Example update event period

The update event period is calculated as follows: Update_event = TIM_CLK/(PSC + 1)\*(ARR + 1)\*(RCR + 1))

Where: TIM_CLK = timer clock input PSC = 16-bit prescaler register ARR = 16/32-bit Autoreload register RCR = 16-bit repetition counter

TIM_CLK = 72 MHz   
Prescaler = 1   
Auto reload = 65535   
No repetition counter RCR = 0 Update_event = 72\*(10^6)/(1 + 1)\*(65535 + 1)\*(1)) Update_event = 549.3 Hz

# Example external clock mode2

In this mode, the update event period is calculated as follows: Update_event = ETR_CLK/(ETR_PSC)\*(PSC + 1)\*(ARR + 1)\*(RCR + 1))   
Where ETR_CLK = the external clock frequency connected to ETR pin.   
ETR_CLK = 100 kHz   
Prescaler = 1   
ETPS - external trigger prescaler= 2   
Autoreload = 255   
Repetition counter = 2 Update_event= 100\*(10^3)/(2)\* (1+ 1)\*((255 + 1)\*(2 + 1)) Update_event = 21.7 Hz

# Example external clock mode1

In this mode, the update event period is calculated as follows: Update_event = TIx_CLK/(PSC + 1)\*(ARR + 1)\*(RCR +1))   
Where TIx_CLK = the external clock frequency connected to TI1 pin or TI2 pin.   
Tlx_CLK = 50 kHz   
Prescaler = 1   
Auto reload = 255   
Repetition counter = 2 Update_event = 50 000/(1+ 1)\*(255 + 1)\*(2 + 1)) Update_event = 32.55 Hz

# Example internal trigger clock (ITRx) mode1

In this mode, the update event period is calculated as follows: Update_event = ITRx_CLK/(PSC + 1)\*(ARR + 1)\*(RCR + 1))   
Where ITRx_CLK = the internal trigger frequency mapped to timer trigger input (TRGI)   
ITRx_CLK = 8 kHz   
Prescaler = 1   
Auto reload = 255

Repetition counter = 1 Update_event = 8000/((1+ 1)\*((255 + 1)\*(1 + 1)) Update_event = 7.8 Hz

Depending on the counter mode, the update event is generated each:

• Overflow, if up counting mode is used: the DIR bit is reset in TIMx_CR1 register • Underflow, if down counting mode is used: the DIR bit is set in TIMx_CR1 register • Overflow and underflow, if center aligned mode is used: the CMS bits are different from zero.

The update event is generated also by:

Software, if the UG (update generation) bit is set in TIM_EGR register Update generation through the slave mode controller.

As the buffered registers (ARR, PSC, CCRx) need an update event to be loaded with their preload values, set the URS (update request source) to 1 to avoid the update flag each time these values are loaded. In this case, the update event is only generated if the counter overflow/underflow occurs.

The update event can also be disabled by setting the bit UDIS (update disable) in the CR1 register. In this case, the update event is not generated, and shadow registers (ARR, PSC, CCRx) keep their values. The counter and the prescaler are reinitialized if the UG bit is set, or if a hardware reset is received from the slave mode controller.

An interrupt or/and a DMA request can be generated when the UIE bit or/and UDE bit are set in the DIER register.

Most STM32Cube firmware packages include examples in Examples|TIM\TIM_TimeBase sub folders.

# 2.3 Timer input capture mode

The timer can be used in input capture mode to measure an external signal. Depending on timer clock, prescaler and timer resolution, the maximum measured period is deduced.

To use the timer in this mode:

1. Select the active input by setting the CCxS bits in CCMRx register. These bits should be different from zero, otherwise the CCRx register are in read mode only.   
2. Program the filter by writing the IC1F[3:0] bits in the CCMRx register, and the prescaler by writing the IC1PSC[1:0] if needed   
3. Program the polarity by writing the CCxNP/CCxP bits to select between rising, falling or both edges.

The input capture module is used to capture the value of the counter after a transition is detected by the corresponding input channel. To get the external signal period, two consecutive captures are needed. The period is calculated by subtracting these two values:

Period= Capture(1) /(TIMx_CLK \*(PSC+1)\*(ICxPSC)polarity_index(2)

The capture difference between two consecutive captures CCRx_tn and CCRx_tr • If CCRx_tn < CCRx_tn+1: capture = CCRx_tn+1 - CCRx_tn • If CCRx_tn > CCRx_tn+1: capture = (ARR_max - CCRx_tn) + CCRx_tn+1.

The polarity index isf theriingoralng edge s used, and 2 f both eges aresed.

# Particular case

To facilitate the input capture measurement, the timer counter is reset after each rising edge detected on the timer input channel by:

Selecting TlxFPx as the input trigger by setting the TS bits in the SMCR register Selecting the reset mode as the slave mode by configuring the SMS bits in the SMCR register.

Using this configuration, when an edge is detected, the counter is reset and the period of the external signal is automatically given by the value on the CCRx register. This method is used only with channel 1 or channel 2.

In this case, the input capture prescaler (ICPSC) is not considered in the period computation.

The period is computed as follows:

Period = CCRx (TIMx_CLK \*(PSC+1)\* polarity_index(1))

he polarity index is fsing or falling edge isused, and 2 if both eges areused.

Many STM32Cube firmware packages include examples in Examples|TIM\TIM_InputCapture sub folder.

# 2.4 Timer in output compare mode

To control an output waveform, or to indicate when a period of time has elapsed, the timer is used in one of the following output compare modes. The main difference between these modes is the output signal waveform.

Output compare timing: The comparison between the output compare register CCRx and the counter CNT has no effect on the outputs. This mode is used to generate a timing base   
Output compare active: Set the channel output to active level on match. The OCxRef signal is forced high when the counter (CNT) matches the capture/compare register (CCRx)   
Output compare inactive: Set channel to inactive level on match. The OCxRef signal is forced low when the counter (CNT) matches the capture/compare register (CCRx); Output compare toggle: OCxRef toggles when the counter (CNT) matches the capture/compare register (CCRx)   
Output compare forced active/inactive: OCREF is forced high (active mode) or low (inactive mode) independently from counter value.

To configure the timer in one of these modes:

Select the clock source.

Write the desired data in the ARR and CCRx registers

Configure the output mode:

Select the output compare mode: timing / active / inactive / toggle.   
b) In case of active, inactive and toggle modes, select the polarity by writing CCxP in CCER register.   
Disable the preload feature for CCx by writing OCxPE in CCMRx register.   
Enable the capture / compare output by writig CCx in CCERx register.

Enable the counter by setting the CEN bit in the TIMx_CR1 register.

5Set the CCxIE / CCxDE bit if an interrupt / DMA request is to be generated.

# Timer output compare timing / delay computation

CCx update rate = CK_CNT / TIMx_ARRx

CCx delay = CCRx / CK_CNT

If internal clock: CK_CNT= CK_PSC / (PSC + 1; • If external clock mode2: CK_CNT = CK_PSC / (ETPS)\*(PSC + 1)) If external clock mode1: CK_CNT = CK_PSC / (PSC + 1):

if ETRF used as clock source: CK_PSC = ETR_CLK / ETPS if TIxFPx used as clock source: CK_PSC = TIx_CLK / ICPS if TI1F_ED (filtered edge detection) used as clock source: CK_PSC = TI1_ED_CLK if ITRx (another timer) used as clock source: CK_PSC = ITRx_CLK.

For more details on using the timer in this mode, refer to the examples provided in the STM32Cube package libraries in ExamplesITIMITIM_OCToggle, \TIMxOCActive, and ITIM_OCInactive subfolders.

# 2.5 Timer in PWM mode

The timer is able to generate PWM in edge-aligned mode or in center-aligned mode with a frequency determined by the value of the TIMx_ARR register, and a duty cycle determined by the value of the TIMx_CCRx register.

# PWM mode 1

• In up-counting, channelx is active as long as CNT< CCRx, otherwise it is inactive • In down-counting, channelx is inactive as long as CNT> CCRx, otherwise it is active.

# PWM mode 2

• In up-counting, channelx is inactive as long as CNT < CCRx, otherwise it is active • In down-counting, channelx is active as long as CNT > CCRx, otherwise it is inactive.

Note:

Active when OCREF = 1, inactive when OCREF = 0.

To configure the timer in this mode:

Configure the output pin:

aSelect the output mode by writing CCS bits in CCMRx register.   
Select the polarity by writing the CCxP bit in CCER register.

2Select the PWM mode (PWM1 or PWM2) by writing OCxM bits in CCMRx register.

3Program the period and the duty cycle respectively in ARR and CCRx registers.

Set the preload bit in CCMRx register and the ARPE bit in the CR1 register.

5 Select the counting mode:

a) PWM edge-aligned mode: the counter must be configured up-counting or down-counting   
b) PWM center aligned mode: the counter mode must be center aligned counting mode (CMS bits different from '00').

6Enable the capture compare.

7. Enable the counter.

For more details on using the timer in this mode, refer to the STM32CubeF3, STM32CubeH7, STM32CubeN6, STM32CubeL5, STM32CubeU5, STM32CubeU3, and STM32CubeG4 firmware package examples in the Examples|TIM\TIM_PWMOutput subfolders.

# Timer in one pulse mode

One pulse mode (OPM) is a particular case of the input capture mode and the output compare mode. It allows the counter to be started in response to a stimulus and to generate a pulse with a programmable length after a programmable delay.

To configure the timer in this mode:

Configure the input pin and mode:

a) Select the TlxFPx trigger to be used by writing CCxS bits in CCMRx register.   
b) Select the polarity of the input pin by writing CCxP and CCxNP bits in CCER register.   
C Configure the TlxFPx trigger for the slave mode trigger by writing TS bits in SMCR register.   
d) Select the trigger mode for the slave mode by writing SMS = 110 in SMCR register.

Configure the output pin and mode:

a) Select the output polarity by writing CCyP bit in CCER register.   
b) Select the output compare mode by writing OCyM bits in CCMRy register (PWM1 or PWM2 mode).   
C Set the delay value by writing in CCRy register.   
d) Set the auto reload value to have the desired pulse: pulse = TIMy_ARR - TIMy_CCRy.

3. Select the one pulse mode by setting the OPM bit in CR1 register, if only one pulse is to be generated. Otherwise, this bit should be reset: Delay = CCRy/(TIMx_CLK/(PSC + 1)) Pulse-Length= (ARR+1-CCRy)/(TIMx_CLK/(PSC+1)).

For more details on using the timer in this mode, refer to the examples provided in the STM32Cube package in the Examples\TIM\TIM_OnePulse sub folder.

# Timer in asymmetric PWM mode

This feature is not available in the original series. See Section 1: Overview for more details.

The asymmetric mode allows center-aligned PWM signals to be generated with a programmable phase shift.

For a dedicated channel, the phase shift and the pulse length are programmed using the two TIMx_CCRx registers (TIMx_CCR1 and TIMx_CCR2 or TIMx_CCR3 and TIMx_CCR4), the value of the TIMx_ARR register determines the frequency. So, the asymmetric PWM mode can be selected independently on two channels by programming the OCxM bits in TIMx_CCMRx register:

OCxM = 1110 to use the asymmetric PWM1, in this mode the output reference has the same behavior as in PWM1 mode. When the counter is counting up the output reference is identical to OC1/3REF, when the counter is down counting, the output reference is identical to OC2/4REF   
OCxM = 1111 to use the asymmetric PWM2, in this mode the output reference has the same behavior as in PWM2 mode. When the counter is counting up the output reference is identical to OC1/3REF, when the counter is down counting, the output reference is identical to OC2/4REF.

The following figure summarizes the asymmetric behavior versus the center aligned PWM mode:

![](images/3d253f36c6d82784ae93e6e1cda29c69e4e7942824b7af765a6f8eb28c3b9295.jpg)  
Figure 1. Asymmetric PWM mode versus center aligned PWM mode

To configure the timer in this mode:

Configure the output pin:

a) Select the output mode by writing CCS bits in CCMRx register. Select the polarity by writing the CCxP bit in CCER register. 2. Select the Asymmetric PWM mode (Asymmetric PWM1 or Asymmetric PWM2) by writing OCxM bits in CCMRx register. 3. Program the period, the pulse length and the phase shift respectively in ARR, CCRx, and CCRy registers. 4. Select the counting mode: the Asymmetric PWM mode is working only with center aligned mode: the counter mode must be center aligned counting mode (CMS bits different from '00'). 5. Enable the capture compare. 6. Enable the counter.

The example called TIM_Asymetric is available for selected boards supported in the STM32Cube packages for STM32F3 series and STM32H7 series.

# 2.8 Timer in combined PWM mode

This feature is not available in the original series. See Section 1: Overview for more details.

The combined mode allows edge or center aligned PWM signals to be generated with programmable delay and phase shift between respective pulses. To generate a combined signal, the TIMx_CCRx and TIMx_CCRy must be used to program the delay and the phase shift. The frequency is determined by the value of the TIMx_ARR register.

The resulting signal (combined signal) is made of an OR or AND logical combination of two reference PWMs. So, the combined PWM mode can be selected independently on two channels by programming the OCxM bits in TIMx_CCMRx register:

OCxM = 1100 to use the Combined PWM1, in this case the combined output reference has the same behavior as in PWM mode 1. The combined output reference is the logical OR between OC1/3REF and OC2/4REF   
OCxM = 1101 to use the Combined PWM2,in this case the combined output reference has the same behavior as in PWM mode 2. The combined output reference is the logical AND between OC1/2REF and OC2/4REF.

The following figures resume the combined mode:

![](images/d96e4961090270237d8547249c0f9c5986ca7e46de458c1632cd8d5bf4b655d1.jpg)  
Figure 2. Combined PWM mode

To configure the timer in this mode:

Configure the output pin:

aSelect the output mode by writing CCS bits in CCMRx register;   
Select the polarity by writing the CCxP bit in CCER register.

2. Select the Combined PWM mode (Combined PWM1 or Combined PWM2) by writing OCxM bits in CCMRx register.

3. Program the period, the delay and the phase shift respectively in ARR, CCRx and CCRy registers.

Select the counting mode:

a) Edge-aligned mode: the counter must be configured up-counting or down-counting.   
b) Center aligned mode: the counter mode must be center aligned counting mode (CMS bits different from '00').

5. Enable the capture compare.

6Enable the counter.

# 2.9 Retriggerable one pulse mode

This feature is not available in the original series. See Section 1: Overview for more details.

The retriggerable one pulse mode is a one pulse mode with these additional characteristics:

• The pulse starts as soon as the trigger occurs (no programmable delay);   
• The pulse is extended if a new trigger occurs before the previous one is completed.

If the counter is configured in up-counting mode, the corresponding CCRx must be set to 0. In this case, the pulse length is determined by ARR register. If the timer is configured in down-counting mode, the ARR must be set to 0 in this case the pulse length is determined by CCRx register. As for the OPM mode, there are two retriggerable one pulse modes. Retriggerable OPM mode 1 and retriggerable OPM mode 2:

Retriggerable OPM mode 1 is selected by setting the OCxM bits to 1000:

In up-counting mode, channel is inactive until a trigger event is detected (on TRGl signal), the comparison is performed like in PWM mode 1, then the channel becomes inactive again at the next update;   
In down-counting mode, channel is active until a trigger event is detected (on TRGI signal), the comparison is performed like in PWM mode 1, then the channel becomes active again at the next update.

Retriggerable OPM mode 2 is selected by setting the OCXM bits to 1001:

In up-counting mode, the channel is active until a trigger event is detected (on TRGI signal). The comparison is performed like in PWM mode 2, then the channel becomes inactive again at the next update;   
In down-counting mode, the channel is inactive until a trigger event is detected (on TRGI signal). The comparison is performed like in PWM mode 1, then the channel becomes inactive again at the next update.

![](images/79c4231886a91887a0865e789eff3fe812e56dbe7565ba34596a84fcf57b53c8.jpg)  
Figure 3 presents an example of the retriggerable OPM mode.   
Figure 3. Retriggerable OPM mode

To configure the timer in this mode:

Configure the input pin and mode:

a) Select the TlxFPx trigger to be used by writing CCxS bits in CCMRx register.   
b) Select the polarity of the input pin by writing CCxP and CCxNP bits in CCER register. Configure the TlxFPx trigger for the slave mode trigger by writing TS bits in SMCR register.   
d) Select the Combined Reset + trigger mode for the slave mode by writing SMS = 1000 in SMCR register.

Configure the output pin and mode:

a)Select the output polarity by writing CCyP bit in CCER register.   
b) Select the output compare mode by writing OCyM bits in CCMRy register (Retriggerable OPM mode 1 or retriggerable OPM mode 2). Set the pulse length value by writing in CCRy register if the counter is downcounting or by writing in the ARR if the counter is up-counting.

For more details on using the timer in this mode, refer to the examples provided in the STM32F30x standard peripheral libraries, in the /Project/STM32F30x_StdPeriph_Examples/ TIM/Retriggerable OPM folder.

# 2.10 PWM analysis mode

This example is only provided in more recent product lines packages, but it can be implemented with any STM32. The purpose of PWM input configuration is to analyze incoming PWM signal frequency and duty cycle.

The timer clock is limiting the measurable input frequency and measurement accuracy.

To configure the timer in this mode:

The external signal is connected to an input pin.

Timer channel is configured to the pin.

To measure the frequency and the duty cycle, use the CC2 interrupt request.

In the timer callback function (HAL_TIM_IC_CaptureCallback(), the frequency and the duty cycle of the external signal are computed:

Frequency = TIMx counter clock / TIMx_CCR2 in Hz, DutyCycle = (TIMx_CCR1\*100)/(TIMx_CCR2) in %.

The minimum frequency value to measure is (clock / counter clock / CCR MAX).

For more details on using the timer in this mode, refer to the STM32CubeG0, STM32CubeG4, STM32CubeU5, STM32CubeU3, STM32CubeL5, STM32CubeWB, STM32CubeWB0, STM32CubeWL, STM32CubeC0, and STM32CubeN6 firmware package examples in the Examples|TIM\TIM_PWMInput subfolders.

# 3

# Timer synchronization

# 3.1 Timer system link

STM32xx series timers are linked together internally for timer synchronization or chaining. Each timer has several internal input and output triggers. These signals allow timer interconnection. Figure 4 illustrates the time interconnection.

![](images/b7a79c8546bcf679ee32be77a3314875c885ee28ae64e5b874d6f8b8f1af4d05.jpg)  
Figure 4. Timer system link

MS30121V2

# 3.2 Master configuration

When a timer is selected as a master timer, the corresponding trigger output signal is used by the slave internal trigger (when configured). The trigger output can be selected from the following list:

Reset: the UG bit from the TIMx_EGR register is used as a trigger output (TRGO); Enable: the counter enable signal is used as a trigger output (TRGO) to start several timers at the same time, or to control a window in which a slave timer is enabled; Update: the update event is selected as trigger output (TRGO). For example, a master timer can be used as a prescaler for a slave timer; Compare pulse: the trigger output sends a positive pulse when the CC1IF flag is to be set (even if it was already high) as soon as a capture or a compare match occurs; • OC1Ref: OC1REF signal is used as trigger output (TRGO); • Oc2Ref: OC2REF signal is used as trigger output (TRGO); • OC3Ref: OC3REF signal is used as trigger output (TRGO); • OC4Ref: OC4REF signal is used as trigger output (TRGO).

To configure a timer in master mode:

1. Configure the timer.   
2. Select the trigger output to be used, by writing the MMS (Master mode selection) bits in TIMx_CR2 register.   
3. Enable the MSM (Master/Slave mode) bit in the SMCR register to allow a perfect synchronization between the current timer and its slaves (through TRGO).

On selected devices such as STM32G4 series, for example, the advanced-control timer can generate two trigger outputs: TRGO as described above and TRGO2 (used for TIM and ADC synchronization) which can be selected from the following list:

Reset - the UG bit from the EGR register is used as trigger output (TRGO2). Enable - the Counter Enable signal CNT_EN is used as trigger output (TRGO2). It is useful to start several timers simultaneously or to control a window in which a slave timer is enabled. The Counter Enable signal is generated by a logical AND between CEN control bit and the trigger input when configured in gated mode. Update - the update event is selected as trigger output (TRGO2). For instance a master timer can then be used as a prescaler for a slave timer. Compare Pulse - the trigger output sends a positive pulse when the CC1IF flag is set high (even if it was already set high), as soon as a capture or a compare match occurs.   
• Compare - OC1REF signal is used as trigger output (TRGO2)   
• Compare - OC2REF signal is used as trigger output (TRGO2)   
• Compare - OC3REF signal is used as trigger output (TRGO2)   
• Compare - OC4REF signal is used as trigger output (TRGO2)   
• Compare - OC5REF signal is used as trigger output (TRGO2)   
• Compare - OC6REF signal is used as trigger output (TRGO2)   
• Compare Pulse - OC4REF rising or falling edges generate pulses on TRGO2   
• Compare Pulse - OC6REF rising or falling edges generate pulses on TRGO2   
• Compare Pulse - OC4REF rising or OC6REF rising edges generate pulses on TRGO2   
• Compare Pulse - OC4REF rising or OC6REF falling edges generate pulses on TRGO2   
• Compare Pulse - OC5REF rising or OC6REF rising edges generate pulses on TRGO2   
• Compare Pulse - OC5REF rising or OC6REF falling edges generate pulses on TRGO2.

# 3.3 Slave configuration

The slave timer is connected to the master timer through the input trigger. Each ITRx is connected internally to another timer, and this connection is specific for each STM32Fx/Gx/Hx/Lx/Wx series product as stated on the first page.

The slave mode can be:

Reset mode: rising edge of the selected trigger input (TRGl) reinitializes the counter and generates an update of the registers   
Gated mode: the counter clock is enabled when TRGl is high. The counter stops (but is not reset) as soon as the trigger becomes low. Both counter start and stop are controlled.   
Trigger mode: the counter starts at a rising edge of the trigger TRGl (but it is not reset). Only the counter start is controlled   
External clock mode 1: rising edges of the selected trigger TRGl clock the counter Combined reset + trigger mode: rising edge of the selected TRGl reinitializes the counter, generates an update of the registers, and starts the counter. This feature is not available in the original series. See Section 1: Overview for more details.

To configure a timer in slave mode:

1. Select the slave mode to be used by writing SMS (slave mode selection) bits in SMCR register.   
2. Select the internal trigger to be used by writing TS (trigger selection) bits in SMCR register.

For more details on using the timer in this mode, refer to the examples provided in the STM32Cube package:

# Examples:

√ ITIMITIM_CascadeSynchro • ITIM_ExtTriggerSynchrolTIM_Synchronization ITIM_ParallelSynchro folders.

# Advanced features for motor control

# 1.1

# Signal generation

The STM32Fx/Gx/Hx/Lx/Ux/Wx series timer can output two complementary signals and manage the on/ off state switching of the outputs.

The complementary signals OCx and OCxN are activated by a combination of several control bits: the CCxE and CCxNE and the MOE, OISx, OISxN, OSSI, and OSSR bits.

The main output enable (MOE) bit is reset once a break input becomes active. It is set by software or automatically based on the automatic output enable (AOE) bit. When the MOE bit is reset, the OCx and OCxN outputs are disabled or forced to idle state (OISx OISxN), depending on whether the OSSl bit is set or not.

# Note:

The MOE bit is valid only on the channels that are configured as output.

The off-state selection for run mode (OSSR) bit is used when MOE=1 to determine the pin output when the channel output is not enabled. When this bit is set, OCx and OCxN outputs are set to their inactive level as soon as their complementary bits CCxE=1 or CCxNE=1. The output is still controlled by the timer.

The off-state selection for idle mode (OSSl) bit is used when MOE=0 due to a break event or by a software write, on channels configured as outputs. When this bit is set, OCx and OCxN outputs are first forced with their inactive level, then forced to their idle level after the deadtime. The timer maintains its control over the output.

Table 6: Advanced timer configurations explains the possible configurations of the advanced timer.

Table 6. Advanced timer configurations   

<table><tr><td rowspan=1 colspan=5>Control bits</td><td rowspan=1 colspan=2>Output state</td><td rowspan=2 colspan=1>Typical use</td></tr><tr><td rowspan=1 colspan=1>MOE</td><td rowspan=1 colspan=1>OSSI</td><td rowspan=1 colspan=1>OSSR</td><td rowspan=1 colspan=1>OCxE</td><td rowspan=1 colspan=1>OCxNE</td><td rowspan=1 colspan=1>OCx outputstate</td><td rowspan=1 colspan=1>OCxN outputstate</td></tr><tr><td rowspan=8 colspan=1>1</td><td rowspan=1 colspan=1>X</td><td rowspan=1 colspan=1>0</td><td rowspan=1 colspan=1>0</td><td rowspan=1 colspan=1>0</td><td rowspan=1 colspan=1>Output disable</td><td rowspan=1 colspan=1>Output disable</td><td rowspan=3 colspan=1>General purpose</td></tr><tr><td rowspan=1 colspan=1>X</td><td rowspan=1 colspan=1>0</td><td rowspan=1 colspan=1>0</td><td rowspan=1 colspan=1>1</td><td rowspan=1 colspan=1>Output disable</td><td rowspan=1 colspan=1>OCxREF+ polarity</td></tr><tr><td rowspan=1 colspan=1>X</td><td rowspan=1 colspan=1>0</td><td rowspan=1 colspan=1>1</td><td rowspan=1 colspan=1>0</td><td rowspan=1 colspan=1>OCxREF+ polarity</td><td rowspan=1 colspan=1>Output disable</td></tr><tr><td rowspan=1 colspan=1>X</td><td rowspan=1 colspan=1>0</td><td rowspan=1 colspan=1>1</td><td rowspan=1 colspan=1>1</td><td rowspan=1 colspan=1>OCxREF+ polarity+ Deadtime</td><td rowspan=1 colspan=1>(not OCxREF)+ polarity+ Deadtime</td><td rowspan=1 colspan=1>Motor control(sinewave)</td></tr><tr><td rowspan=1 colspan=1>X</td><td rowspan=1 colspan=1>1</td><td rowspan=1 colspan=1>0</td><td rowspan=1 colspan=1>0</td><td rowspan=1 colspan=1>Output disabled</td><td rowspan=1 colspan=1>Output disabled</td><td rowspan=3 colspan=1>Motor control(6-steps)</td></tr><tr><td rowspan=1 colspan=1>X</td><td rowspan=1 colspan=1>1</td><td rowspan=1 colspan=1>0</td><td rowspan=1 colspan=1>1</td><td rowspan=1 colspan=1>Off-state</td><td rowspan=1 colspan=1>OCxREF+ polarity</td></tr><tr><td rowspan=1 colspan=1>X</td><td rowspan=1 colspan=1>1</td><td rowspan=1 colspan=1>1</td><td rowspan=1 colspan=1>0</td><td rowspan=1 colspan=1>OCxREF +polarity</td><td rowspan=1 colspan=1>Off-state</td></tr><tr><td rowspan=1 colspan=1>X</td><td rowspan=1 colspan=1>1</td><td rowspan=1 colspan=1>1</td><td rowspan=1 colspan=1>1</td><td rowspan=1 colspan=1>OCxREF+ polarity+ deadtime</td><td rowspan=1 colspan=1>(not OCxREF)+ polarity+ deadtime</td><td rowspan=1 colspan=1>Motor control(sinewave)</td></tr><tr><td rowspan=1 colspan=1>MOE</td><td rowspan=1 colspan=1>OSSI</td><td rowspan=1 colspan=1>OSSR</td><td rowspan=1 colspan=1>OCxE</td><td rowspan=1 colspan=1>OCxNE</td><td rowspan=1 colspan=1>OCx outputstate</td><td rowspan=1 colspan=1>OCxN outputstate</td><td rowspan=1 colspan=1>Comments</td></tr><tr><td rowspan=8 colspan=1>0</td><td rowspan=1 colspan=1>0</td><td rowspan=1 colspan=1>X</td><td rowspan=1 colspan=1>0</td><td rowspan=1 colspan=1>0</td><td rowspan=4 colspan=2>Output disable</td><td rowspan=4 colspan=1>Outputsdisconnectedfrom I/0 ports</td></tr><tr><td rowspan=1 colspan=1>0</td><td rowspan=1 colspan=1>X</td><td rowspan=1 colspan=1>0</td><td rowspan=1 colspan=1>1</td></tr><tr><td rowspan=1 colspan=1>0</td><td rowspan=1 colspan=1>X</td><td rowspan=1 colspan=1>1</td><td rowspan=1 colspan=1>0</td></tr><tr><td rowspan=1 colspan=1>0</td><td rowspan=1 colspan=1>X</td><td rowspan=1 colspan=1>1</td><td rowspan=1 colspan=1>1</td></tr><tr><td rowspan=1 colspan=1>1</td><td rowspan=1 colspan=1>X</td><td rowspan=1 colspan=1>0</td><td rowspan=1 colspan=1>0</td><td rowspan=4 colspan=2>Off-state(outputs are first forced with theirinactive level then forced to theiridle level after the deadtime.)</td><td rowspan=4 colspan=1>All PWMs OFF(low Z for safestop)</td></tr><tr><td rowspan=1 colspan=1>1</td><td rowspan=1 colspan=1>X</td><td rowspan=1 colspan=1>0</td><td rowspan=1 colspan=1>1</td></tr><tr><td rowspan=1 colspan=1>1</td><td rowspan=1 colspan=1>X</td><td rowspan=1 colspan=1>1</td><td rowspan=1 colspan=1>0</td></tr><tr><td rowspan=1 colspan=1>1</td><td rowspan=1 colspan=1>X</td><td rowspan=1 colspan=1>1</td><td rowspan=1 colspan=1>1</td></tr></table>

Note: 1 Deadtime insertion is enabled by setting both CCxE and CCxNE bits, and the MOE bit.

2 When only OCxN is enabled (CCxE=0, CCxNE=1), it is not complemented and becomes active as soon as OCxREF is high. For example, if CCxNP=0 then OCxN=OCxRef. On the other hand, when both OCx and OCxN are enabled (CCxE=CCxNE=1) OCx becomes active when OCxREF is high, whereas OCxN is complemented and becomes active when OCxREF is low.

# 4.2 Combined three-phase PWM mode

This feature is not available in the original series. See Section 1: Overview for more details.

The combined three-phase mode allows the generation of one to three center-aligned PWM signals with a single programmable signal ANDed in the middle of the pulses. The configuration is helpful for shunt resistor current sensing applications. Refer to UM1052 for further reading on this topic.

Using the 3-bits GC5C[3:1] in the TIMx_CCR5, each channel of the TIM can be a combination between the original signal and the OC5Ref signal:

• If GC5C1 is set, OC1 output is controlled by TIMx_CCR1 and TIMx_CCR5 • If GC5C2 is set, OC1 output is controlled by TIMx_CCR2 and TIMx_CCR5 • If GC5C3 is set, OC1 output is controlled by TIMx_CCR3 and TIMx_CCR5.

The Figure 5 below illustrates an example of this mode:

![](images/93e829159173bc3d92354b5df8974e7a43f74d7b15bef3a4a0df9e7007b4af1b.jpg)  
Figure 5. Combined three-phase PWM

To configure the timer in this mode:

Configure the output pin:

a)Select the output mode by writing CCS bits in TIMx_CCMRx register. Select the polarity by writing the CCxP bit in TIMx_CCER register. 2. Configure the used channel (1, 2 or/and 3) in PWM mode: Configure the frequency, the duty cycle and the polarity. Select the PWM 1 or 2. 3. Configure the Channel 5 in PWM mode with the desired parameter (duty cycle). 4. Select the Combined PWM mode by programming the GC5Cx bits. 5. Select the Center aligned mode as counting mode. 6. Enable the capture compare. 7. Enable the counter.

For more details on using the timer in this mode, refer to the examples provided in the STM32CubeF3, STM32CubeG4 and STM32CubeH7 firmware packages in the Examples|TIMITIM_Combined sub folder.

# 4.3

# Specific features for motor control applications

# Complementary signal and deadtime feature

The STM32xx series advanced timers can generate up to three complementary outputs with the insertion of deadtime.

To use the complementary signal for one channel, set the two output compare enable bits of this channel and its complementary (OCxE and OCxNE) channel. If the deadtime bits are not zero, the two signals are generated with the insertion of a deadtime as illustrated in Figure 6:

![](images/9355b2c7ae4f9f2efec73b981bff6db9ced39b7c17eb2257a6bdfc7e47af496f.jpg)

MS30125V3

Note:

The deadtime parameter is computed using the DTG[7:0] bits and the deadtime clock (Tdtg).

The deadtime clock is computed as follows:

Tdtg = TDTS, if DTG[7] = 0   
Tdtg = 2 x TDTS, if DTG[6] = 0   
Tdtg = 8 x TDTS, if DTG[5] = 0   
Tdtg = 16 x TDTS, if DTG[7:5] = 111

Where: TDTS = TCK_INT, if CKD[1:0] = 00 TDTS = 2 x TCK_INT, if CKD[1:0] = 01 TDTS = 4 x TCK_INT, if CKD[1:0] = 10

Note: TCK_INT is the internal clock timer.

The deadtime delay is computed using the following formula: deadtime = DTG[7:0]x Tdtg, if DTG[7] = 0 deadtime = (64+DTG[5:0]) x Tdtg, if DTG[6] = 0 deadtime = (32+DTG[4:0]) x Tdtg, if DTG[5] = 0 deadtime = (32+DTG[4:0]) x Tdtg, if DTG[7:5] = 111

For more details on using the timer in this mode refer to the examples provided in the STM32Cube package examples in the following directories:

Examples|TIMITIM_ComplementarySignals • Examples\TIM\TIM_Combined Examples|TIM\TIM_DeadtimeInsertion

Note:

At the time of writing this application note, the complementary signals example is available for STM32F0, STM32F1, STM32F2, STM32F3, STM32F4, STM32F7, STM32G4, and STM32H7 series microcontrollers. The combined example is available for STM32F3, STM32G4, and STM32H7 series microcontrollers. The dead time insertion example is available for STM32N6 series microcontrollers.

# 4.3.2 Break input

The break input is an emergency input in the motor control application. The break function protects power switches driven by PWM signals generated with the advanced timers. The break input is usually connected to fault outputs of power stages and 3-phase inverters. When activated, the break circuitry shuts down the TIM outputs and forces them to a predefined safe state.

The break event is generated by:

• The BRK input that has a programmable polarity and an enable bit BKE   
• The CSS (clock security system)   
• Software, by setting the BG bit in the EGR register

When a break event occurs:

• The MOE bit (main output enable) is cleared • The break status flag is set and an interrupt request can be generated • Each output channel is driven with the level programmed in the OlSx bit.

Note:

More information about break inputs is also provided in the application note 4277.

# Revised break inputs

Break inputs Break1 and Break2 are not available on the original series.

The break can be generated by any of the two BRK inputs that have:

• a programmable polarity (BKPx bit in the TIMx_BDTR Register)   
• a programmable enable bit (BKEx in the TIMx_BDTR Register) a programmable filter (BKxF[3:0] bits in the TIMx_BDTR Register) to avoid spurious events.

Table 7 presents the two break inputs priorities.

Table 7. Behavior of timer outputs versus Break1 and Break2 inputs   

<table><tr><td rowspan=1 colspan=1>Break input 1</td><td rowspan=1 colspan=1>Break input 2</td><td rowspan=1 colspan=1>OCxN output</td><td rowspan=1 colspan=1>OCx output</td></tr><tr><td rowspan=1 colspan=1>Active</td><td rowspan=1 colspan=1>Inactive</td><td rowspan=1 colspan=1>ON after deadtimeinsertion</td><td rowspan=1 colspan=1>OFF</td></tr><tr><td rowspan=1 colspan=1>Inactive</td><td rowspan=1 colspan=1>Active</td><td rowspan=1 colspan=1>OFF</td><td rowspan=1 colspan=1>OFF</td></tr><tr><td rowspan=1 colspan=1>Active</td><td rowspan=1 colspan=1>-</td><td rowspan=1 colspan=1>ON after deadtimeinsertion</td><td rowspan=1 colspan=1>OFF</td></tr></table>

# 4.3.3 Locking mechanism

The advanced timer registers and bits can be protected or locked in order to safeguard the application using the locking mechanism by programming the LOCK bits in the BDTR register. There are three locking levels illustrated in Table 8.

Table 8. Locking levels   

<table><tr><td rowspan=1 colspan=2>Level 1</td><td rowspan=1 colspan=3>LOCK Level 2(1)</td><td rowspan=1 colspan=2>LOCK Level 3(2)</td></tr><tr><td rowspan=1 colspan=1>Register</td><td rowspan=1 colspan=1>Bits</td><td rowspan=1 colspan=2>Register</td><td rowspan=1 colspan=1>Bits</td><td rowspan=1 colspan=1>Register</td><td rowspan=1 colspan=1>Bits</td></tr><tr><td rowspan=2 colspan=1>CR2</td><td rowspan=1 colspan=1>OISx</td><td rowspan=2 colspan=2>CR2</td><td rowspan=1 colspan=1>OISx</td><td rowspan=2 colspan=1>CR2</td><td rowspan=1 colspan=1>OISx</td></tr><tr><td rowspan=1 colspan=1>OISxN</td><td rowspan=1 colspan=1>OISxN</td><td rowspan=1 colspan=1>OISxN</td></tr><tr><td rowspan=8 colspan=1>BDTR</td><td rowspan=1 colspan=1>DTG[7:0]</td><td rowspan=1 colspan=2></td><td rowspan=1 colspan=1>DTG[7:0]</td><td rowspan=6 colspan=1>BDTR</td><td rowspan=1 colspan=1>DTG[7:0]</td></tr><tr><td rowspan=1 colspan=1>BKE</td><td rowspan=3 colspan=2>BDTR</td><td rowspan=1 colspan=1>BKE</td><td rowspan=1 colspan=1>BKE</td></tr><tr><td rowspan=1 colspan=1>BKP</td><td rowspan=1 colspan=1>BKP</td><td rowspan=1 colspan=1>BKP</td></tr><tr><td rowspan=1 colspan=1>AOE</td><td rowspan=1 colspan=1></td><td rowspan=1 colspan=1>AOE</td><td rowspan=1 colspan=1>AOE</td></tr><tr><td rowspan=1 colspan=1>BK2E(3)</td><td rowspan=1 colspan=2></td><td rowspan=1 colspan=1>OSSR</td><td rowspan=1 colspan=1>OSSR</td></tr><tr><td rowspan=1 colspan=1>BK2P(3)</td><td rowspan=1 colspan=2></td><td rowspan=1 colspan=1>OSSI</td><td rowspan=1 colspan=1>OSSI</td></tr><tr><td rowspan=1 colspan=1>BKF[3:0](3)</td><td rowspan=2 colspan=2>CCER</td><td rowspan=1 colspan=1>CCxP</td><td rowspan=2 colspan=1>CCER</td><td rowspan=1 colspan=1>CCxP</td></tr><tr><td rowspan=1 colspan=1>BK2F[3:0](3)</td><td rowspan=1 colspan=1>CCxNP</td><td rowspan=1 colspan=1>CCxNP</td></tr><tr><td rowspan=1 colspan=1></td><td rowspan=1 colspan=1>-</td><td rowspan=1 colspan=2>b</td><td rowspan=1 colspan=1>-</td><td rowspan=2 colspan=1>CCMRx</td><td rowspan=1 colspan=1>OCxM</td></tr><tr><td rowspan=1 colspan=1>-</td><td rowspan=1 colspan=1>-</td><td rowspan=1 colspan=2>-</td><td rowspan=1 colspan=1>-</td><td rowspan=1 colspan=1>OCxPE</td></tr></table>

1LOCK Level 2 = LOCK Level 1 + CC polarity bits (CCxP/CCxNP bits in TIMx_CCER). 2 LOCK Level 3 = LOCK Level 2 + CC control bits (OCxM and OCxPE. 3.Bits present in STM32L4/F7/L5/U3/U5/G0/G4/WB/WB0/H7/N6 series and STM32F30x/F3x8 lines.

Note:

The LOCK bits can only be written once after the reset. Once the BDTR register has been written, its content is frozen until the next reset.

# 4.3.4 Specific features for feedback measurement

# Encoder modes

The incremental quadrature encoder is a type of sensor used in motor-control applications to measure the angular position and the rotation direction.

In general, the incremental quadrature encoder generates three signals: phase A, phase B and index.

The direction of the motor depends on whether Phase A leads Phase B, or Phase B leads Phase A. A third channel, index pulse, occurs once per revolution and is used as a reference to measure an absolute position.

The Phase A and B output signals are connected to the encoder interface to compute the frequency and then determine the velocity and the position. Velocity and position information can be measured at X2 or X4 resolution. Figure 7: Position at X4 resolution and Figure 8: Position at X2 resolution explain the encoder interface function.

The timer's counter is incremented or decremented for each transition on both inputs TI1 and TI2.

![](images/783b9ff33a8f845f70c0ad65d55825e790e350aac780fc0e081cb337e69a1528.jpg)

The timer's counter is incremented or decremented for each transition on the selected input TI1 or TI2.

![](images/014bf73fb3d63e689db5616a517555e7c4bec5bd99555c248cb02aa3eeaa350f.jpg)  
Figure 8. Position at X2 resolution

Note:

In case of X2 resolution, the counter can also be incremented on the Tl1 edge.

In STM32 timer encoder interface mode, the encoder mode3 corresponds to the X4 resolution. In this mode, the counter counts up/down on both TI1 and TI2 edges.

The X2 resolution is selected when encoder mode 1 or mode 2 is selected, that is, the counter counts up/down on TI2 edge depending on the TI1 level, or the counter counts up/down on TI1 edge depending on TI2 level.

# How to use the encoder interface

An external incremental quadrature encoder can be connected directly to the MCU without external interface logic. The third encoder output (index) which indicates the mechanical zero position, may be connected to an external interrupt input and triggers a counter reset.

The output signal of the incremental encoder is filtered by the STM32 timer input filter block to reject all noise sources that typically occur in motor systems. This filter is described in Section 2.3: Timer input capture mode on page 14.

# TIM configuration in encoder mode

Select and configure the timer input:

Input selection:

TI1 connected to TI1FP1 CC1S='01' in TIMx_CCMR1 register;   
TI2 connected to TI2FP2 CC2S='01' in TIMx_CCMR1 register.

Input polarity: CC1P='0' and CC1NP='0'(CCER register, TI1FP1 noninverted, TI1FP1=TI1); CC2P='0' and CC2NP='0'(CCER register, TI1FP2 noninverted, TI1FP2= TI2).

2. Select the encoder mode:

• Encoder mode1 (resolution X2 on TI2): SMS='001' in theTIMx_SMCR register;   
• Encoder mode2 (resolution X2 on TI1): SMS='010' in the TIMx_SMCR register;   
• Encoder mode3 (resolution X4 on TI1 and TI2): SMS='011' in the TIMx_ SMCR register.   
3. Enable the timer counter: • Set the counter enable bit, CEN='1' in TIMx_CR1 register.

# Hall sensor

The Hall sensor is a type of sensor based on the Hall effect: when a conductor is placed in a magnetic field, a voltage is generated perpendicular to both the current and the magnetic field.

There are four types of Hall sensor IC devices that provide a digital output: unipolar switches, bipolar switches, omnipolar switches, and latches. The main difference between them is the output waveforms (pulse duration).

The digital hall sensor provides a digital output in relation to the magnetic field that it is exposed. When the magnetic field increases and is greater than the BRp (magnetic field release point value), the output is set to ON. When the magnetic field decreases and is lower than the Bop (magnetic field operate point value) the output is set to OFF.

Figure 9 presents the output waveform of a typical Hall sensor.

![](images/41d6edeb52e577d0a4440572b1acd954eb1b8084261a5a94d02b79f36bb94e18.jpg)  
Figure 9. Output waveform of a typical Hall sensor

Generally, the Hall sensor is used in the three-phase motor control. Figure 10 presents the commutation sequence.

![](images/117032ebf2ab94246dad60e9870d72d4ed18412af9574bb9230037b0762a4013.jpg)  
Figure 10. Commutation sequence

# How to use the Hall sensor interface

The STM32 timers can interface with the Hall effect sensors via the standard inputs (CH1, CH2, and CH3). Setting TI1S bit in the TIMx_CR2 register enables to connect the input filter of channel 1 to the output of an XOR gate. This combines the three input pins TIMx_CH1, TIMx_CH2 and TIMx_CH3.

The slave mode controller is configured in reset mode; the slave input is TI1F_ED. Thus, each time one of the three inputs toggles, the counter restarts counting from 0. This creates a time base triggered by any change on the Hall inputs.

Channel 1 is configured as an input capture mode and the capture signal is TRC. The captured value, which corresponds to the time, elapsed between two changes on the inputs, gives information on the motor speed.

# TIM configuration in Hall sensor interface mode

1. Configure three timer inputs ORed to the T11 input channel by writing the TI1S bit in TIMx_CR2 register to '1'.   
2. Program the time base: write the TIMx_ARR to the max value (the counter must be cleared by the T11 change. Set the prescaler to a period longer than the time between two changes on the sensors.   
3. Program channel 1 in capture mode (TRC selected): write the CC1S bits in the TIMx_CCMR1 register to '01'. The user can also program the digital filter if needed.

# 5 High-resolution timer applications

The high-resolution timer was designed specifically to control power conversion systems in the lighting systems switch mode power supply. Even though it really excels in this role, it can of course be used in other applications with high-resolution timer requirements.

The HRTIM features up to 10 outputs that can be configured in various coupled and autonomous modes using five timing units tied to a common master for synchronization purposes. The synchronization with other timers is also facilitated. The HRTIM is strongly tied to ADCs and fault inputs for feedback purposes.

For more information about the high-resolution timer, read the reference manual of the particular MCU line.

Application related information can be found in the following documents:

• "High brightness LED dimming using the STM32F334 discovery kit" (AN4885) • "Buck-boost converter using the STM32F334 discovery kit" (AN4449) "HRTIM cookbook" (AN4539)

Numerous examples are available in the STM32Cube packages of families featuring the high-resolution timer (STM32F3, STM32G4, STM32H7).

# 6 Low-power timer

The main difference and advantage of the LPTIM compared to any other timer peripheral in the STM32 microcontroller family is the ability to continue working even in Stop mode and trigger events that wake the MCU up from the Stop mode. For a list of Stop modes supported by each LPTIM instance, refer to the product datasheet. Depending on the selected clock source, the runtime power consumption can be substantially lower compared to a general purpose timer. While it can perform a similar job to the general purpose timer, the focus is put on the task for which it is designed for.

# 6.1 Wake-up timer implementation

The LPTIM can be configured to periodically wake up the MCU from stop mode, for example to refresh a display or to read a sensor. For this purpose it needs to be configured to use a clock source that remains functional in stop mode. It can be an LSE, an LSI oscillator, or an external clock source. An external clock source is fed to the LPTIM Input1 that has configured to use it (CKSEL is appropriately configured).

To configure the timer in this mode:

1. Configure a clock source.   
2. Code the interrupt handler, callback function and enable the LPTIM interrupt.   
3. Set up the LPTIM peripheral: a) Clock source selection; b) Set timing range using prescaler; Set trigger event (software or external signal).   
4. Enable and start the timer.   
5. Go to stop mode.

For more details on using the timer in this mode, refer to examples provided in the STM32Cube package in the Examples|LPTIMLPTIM_Timeout sub folder.

# 6.2 Pulse counter

In some applications, the microcontroller needs to record some external events, but it is not desirable to wake it up from Stop mode each time. In this case, the LPTiM is configured as a pulse counter. Use the timer period/compare setting to set the number of events required to wake the microcontroller.

To configure the timer in this mode:

1Configure a clock source.   
Code the interrupt handler calback function and enable the LPTIM interrupt.

3.Set up the LPTIM timer peripheral:

a) Clock source and counter source selection. Only input1 can be used as a clock source;   
b) Typical configuration selection is immediate update mode and software trigger source.

4. Enable and start the timer.

Go to Stop mode.

For more details on using the timer in this mode, refer to the examples provided in the STM32Cube package in the Examples|LPTIMILPTIM_PulseCounter sub folder.

# Specific applications

# 7.1 Infrared application

The STM32 general-purpose timers can be used to emulate several infrared protocols. An example of this application type is given in the application note Implementation of transmitters and receivers for infrared remote control protocols with STM32Cube (AN4834)

This application note describes a software solution for implementing an RC5/SIRC receiver and transmitter using a pair of the STM32 general-purpose timers, usually TIM16 and TIM17.

This solution uses a specialized feature called IRTIM for implementation of the transmitter part. IRTIM is available on STM32C0, STM32F0, STM32F3, STM32U3, STM32U5, STM32L5, STM32G0, STM32G4, STM32WB, STM32WB0, and STM32L4 devices.

Some microcontrollers, such as the STM32G0, feature an innovated IRTIM internally connected to USART for easier modulation.

# 3-phase AC and PMSM control motor

The STM32 advanced and general-purpose timers together with ADC and DAC are used to control two types of 3-phase motor: AC induction motor and PMSM, with different current sensing methodologies:

• Isolated current sensing (also referred to as sensor-less solution);   
• Three shunt resistors;   
• Single shunt resistor (ST patented solution).

The STM32 timers are used also in the feedback loop to interface with the different sensors used in the different rotor position feedback:

S Tachogenerator;   
• Quadrature encoder;   
• Hall sensors: 60° and 120° placement.

For more details, refer to STM32 ecosystem for motor control available at www.st.com.

# 7.3 Six-step mode

The six-step mode is a specific mode of STM32 advanced timers. When complementary outputs are used on a channel, preload bits are available on the OCxM, CCxE, and CCxNE bits. The preload bits are transferred to the shadow bits at the COM (commutation event).

The user can program in advance the configuration for the next step and change the configuration of all the channels at the same time. COM can be generated by software by setting the COM bit in the TIMx_EGR register or by hardware (on TRGI rising edge).

An application example of the use of this mode is the control of the brush-less 3-phase DC motor (3-phase BLDC motor).

# Configuring the timer to generate a six-step signal to control a brush-less 3- phase DC motor (3-phase BLDC motor)

• Time base configuration: prescaler, period, clock source;   
• Channels 1, 2, 3 and 4 configured in PWM mode;   
• Set the capture compare preload control bit CCPC;   
• Enable the commutation interrupt source; Use the system tick to generate time base; For each commutation event, the TIM configuration is updated for the next commutation event.

For more details on using the timer in this mode, refer to the examples provided in the STM32Cube package in the Examples\TIM\TIM_6Steps folder.

# Note:

For some devices, this example is not available.

# 8 Revision history

Table 9. Document revision history   

<table><tr><td colspan="1" rowspan="1">Date</td><td colspan="1" rowspan="1">Revision</td><td colspan="1" rowspan="1">Changes</td></tr><tr><td colspan="1" rowspan="1">21-Feb-2012</td><td colspan="1" rowspan="1">1</td><td colspan="1" rowspan="1">Initial release.</td></tr><tr><td colspan="1" rowspan="1">22-Oct-2012</td><td colspan="1" rowspan="1">2</td><td colspan="1" rowspan="1">Added support for STM32F30x, STM32F31x, STM32F37x,STM32F38x.</td></tr><tr><td colspan="1" rowspan="1">12-Feb-2014</td><td colspan="1" rowspan="1">3</td><td colspan="1" rowspan="1">Added support for STM32F0 series, STM32F358xC.Replaced "basic timers" by "general-purpose" timers in the wholedocument.Updated Section 2.1.2: External clock.UpdatedSection 2.4: Timer in output compare mode.Updated Section 2.5: Timer in PWM mode.Updated Section 7.3: Six-step mode.</td></tr><tr><td colspan="1" rowspan="1">28-Jan-2015</td><td colspan="1" rowspan="1">4</td><td colspan="1" rowspan="1">Extended the applicability to STM32F303xDxE. Updated:Table 1: Applicable products- Table 2: Simplified overview of timer availability in STM32Fxproducts- The document title and introductionAdded references to timer examples available in STM32CubeF3firmware package where applicable.</td></tr><tr><td colspan="1" rowspan="1">15-Apr-2016</td><td colspan="1" rowspan="1">5</td><td colspan="1" rowspan="1">Extended coverage to STM32F7 series, STM32L0 series andSTM32L4 series.Added:Section 5: High-resolution timer applications.Section 6: Low-power timer.Updated:Table 2.: Simplified overview of timer availability in STM32Fxproducts.Table 5: Timer features overview.Section 2.4: Timer in output compare mode.</td></tr><tr><td colspan="1" rowspan="1">28-Jul-2016</td><td colspan="1" rowspan="1">6</td><td colspan="1" rowspan="1">Updated Section 2.2: Time base generator: corrected values on theformulas for "update event" on the examples for update event periodand external clock mode2.</td></tr><tr><td colspan="1" rowspan="1">08-Apr-2019</td><td colspan="1" rowspan="1">7</td><td colspan="1" rowspan="1">Added the STM32WB series, STM32H7series, STM32G0 series,STM32G4 series in Table 1: Applicable products.Updated:Section 1: Overview content.Table 2: Simplified overview of timer availability in STM32Fxproducts footer information.Table 4: Timer features overview content and foot noteSection 2.1.1: Internal clockSection 2.6: Timer in one pulse mode Pulse-Length definition.Section 2.7: Timer in asymmetric PWM mode, Section 2.8: Timerin combined PWM mode and Section 2.9: Retriggerable one pulsemode with the unsupported series.Section 3.2: Master configuration with STM32G4 series reference.Section 3.3: Slave configuration removed specified references toSTM32L4/F7 series and STM32F30x/F3x8 lines in and updatedwith the unsupported series.Section 4.2: Combined three-phase PWM mode updated the titleand added unsupported series.- Note updated in Section 4.3.1: Complementary signal anddeadtime feature.Section 4.3.2: Break input Revised break inputs section forsupported series.Section 7.1: Infrared application included additional supportedseries (added STM32WB)</td></tr><tr><td colspan="1" rowspan="1">24-Sep-2019</td><td colspan="1" rowspan="1">8</td><td colspan="1" rowspan="1">Added STM32L5 series in Table 1: Applicable productsUpdated Section 1: Overview (added AN4539 and updated Table 3:Simplified overview of timer availability in STM32Lx products).Added references to STM32CubeG4 and STM32CubeH7 inSection 2.5: Timer in PWM modeUpdated Section 2.7: Timer in asymmetric PWM mode (firmwareexample)Removed note 4 in Table 5: Timer features overviewAdded references to STM32CubeG4 and STM32CubeH7 firmwarepackages in Section 4.2: Combined three-phase PWM modeAdded STM32F2 and STM32G4 Section 4.3.1: Complementarysignal and deadtime featureAdded references to STM32L5/G0/G4/WB/H7 in Table 8: LockinglevelsUpdated Section 5: High-resolution timer applicationsUpdated Section 7.1: Infrared applicationModified Table 5: Timer features overview (removed one note andadded STM32WB/L5 in note 1).</td></tr><tr><td colspan="1" rowspan="1">01-Jun-2021</td><td colspan="1" rowspan="1">9</td><td colspan="1" rowspan="1">Added:- STM32U5 series and STM32WL series to the document's scopeTable 4: Simplified overview of timer availability inSTM32Cx/Gx/Hx/Nx/Ux/Wx productsUpdated:Table 1: Applicable productsTable 3: Simplified overview of timer availability in STM32Lxproducts- Notes 2 and 3 on Table 5: Timer features overviewSection 6: Low-power timerFigure 7: Position at X4 resolution and Figure 8: Position at X2resolution</td></tr><tr><td colspan="1" rowspan="1">12-Jan-2023</td><td colspan="1" rowspan="1">10</td><td colspan="1" rowspan="1">Updated:Table 1: Applicable productsTable 5: Timer features overviewAdded:Section 2.10: PWM analysis mode</td></tr><tr><td colspan="1" rowspan="1">13-Mar-2024</td><td colspan="1" rowspan="1">11</td><td colspan="1" rowspan="1">-Updated the document title.- Added STM32U0 series, SM32WB0 series, andSTM32H7Rx/7Rx lines.</td></tr><tr><td colspan="1" rowspan="1">15-Nov-2024</td><td colspan="1" rowspan="1">12</td><td colspan="1" rowspan="1">Added STM32N6 series.-Updated Table 4: Simplified overview of timer availability inSTM32Cx/Gx/Hx/Nx/Ux/Wx products</td></tr><tr><td colspan="1" rowspan="1">13-Feb-2025</td><td colspan="1" rowspan="1">13</td><td colspan="1" rowspan="1">Introduced STM32U3 series throughout the document.</td></tr></table>

# IMPORTANT NOTICE  PLEASE READ CAREFULLY

acknowledgement.

the design of Purchasers' products.

No license, express or implied, to any intellectual property right is granted by ST herein.

product or service names are the property of their respective owners.

I