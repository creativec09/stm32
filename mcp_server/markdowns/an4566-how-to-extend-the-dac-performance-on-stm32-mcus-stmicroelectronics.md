# How to extend the DAC performance on STM32 MCUs

# Introduction

Most of the STM32 microcontrollers embed 12-bit DACs (digital to analog converters), specified to operate at up to 1 Msps (megasamples per second).

Several applications benefit from DACs operating at higher speeds. This document explains how to extend the speed performance of microcontrollers listed in Table 1 using external operational amplifiers (OpAmps).

The STM32 DAC system is described in Section 1 of this document, while an application example focusing on 5 Msps sine wave generation is presented in Section 2.

Table 1. Applicable products   

<table><tr><td rowspan=1 colspan=1>Type</td><td rowspan=1 colspan=1>Product series</td></tr><tr><td rowspan=18 colspan=1>Microcontrollers</td><td rowspan=1 colspan=1>STM32F0 series</td></tr><tr><td rowspan=1 colspan=1>STM32F1 series</td></tr><tr><td rowspan=1 colspan=1>STM32F2 series</td></tr><tr><td rowspan=1 colspan=1>STM32F3 series</td></tr><tr><td rowspan=1 colspan=1>STM32F4 series</td></tr><tr><td rowspan=1 colspan=1>STM32F7 series</td></tr><tr><td rowspan=1 colspan=1>STM32G0 series</td></tr><tr><td rowspan=1 colspan=1>STM32G4 series</td></tr><tr><td rowspan=1 colspan=1>STM32H5 series</td></tr><tr><td rowspan=1 colspan=1>STM32H7 series</td></tr><tr><td rowspan=1 colspan=1>STM32L0 series</td></tr><tr><td rowspan=1 colspan=1>STM32L1 series</td></tr><tr><td rowspan=1 colspan=1>STM32L4 series</td></tr><tr><td rowspan=1 colspan=1>STM32L4+ series</td></tr><tr><td rowspan=1 colspan=1>STM32L5 series</td></tr><tr><td rowspan=1 colspan=1>STM32U0 series</td></tr><tr><td rowspan=1 colspan=1>STM32U3 series</td></tr><tr><td rowspan=1 colspan=1>STM32U5 series</td></tr></table>

# Contents

# The STM32 DAC system . . 5

1.1 DAC equivalent circuit 5   
1.2 DAC speed on the specification 5   
1.3 External OpAmp implementation 6   
1.4 Digital data update rate   
1.4.1 DMA double data mode 8   
1.5 Summary 9

# Example .. 10

2.1 External OpAmp choice 10

2.2 Software implementation 11

2.2.1 Digital sine waveform pattern preparation 11   
2.2.2 Setting the sine waveform frequency . 11   
2.2.3 Offset calibration 12   
2.2.4 Output gain calibration 12

2.3 Hardware implementation 15

# Measurements 16

3.1 Board modification 16   
3.2 Measurement results 16

Conclusion . . 18

Revision history 19

# List of tables

Table 1. Applicable products 1   
Table 2. Maximum sampling time. 8   
Table 3. Example of the offset calibration measurement 12   
Table 4. Example of the calibration measurement . 13   
Table 5. Example of digital sample values 13   
Table 6. Component values 15   
Table 7. Document revision history 19

# List of figures

Figure 1. DAC equivalent circuit 5   
Figure 2. External OpAmp configuration .6   
Figure 3. Circuit implementation 15   
Figure 4. Output signal. 16   
Figure 5. FFT result . 17

# The STM32 DAC system

# 1.1 DAC equivalent circuit

STM32 microcontrollers, based on Arm®(a) cores, use DACs to transform digital data into analog signals. The DAC can be modeled as a digitally controlled voltage source and an output impedance, as shown in Figure 1.

The output impedance of the DAC is constant, independent from the digital input signal.

When the output buffer is OFF, DACINT and DACOUT are connected through the resistor Rb, hence the output impedance of the DAC is Ra + Rb (Rb = Ra), and RDAC = 2 \* Ra (S1 and S2 switches are open).

When the buffer is enabled, the OpAmp is configured as an inverting amplifier with Ay = -1, and the output impedance is almost zero thanks to the feedback loop.

![](images/331c55555046f0e1acc0d12ce1694973c9fe7108643a759a897fc0677d432b3d.jpg)  
Figure 1. DAC equivalent circuit

# 1.2 DAC speed on the specification

When the output buffer is enabled on the DAC output, the speed is specified by the output buf oan.Tibe siat ntpdat p datasheet.

When the output buffer is disabled, the output signal speed simply follows the RC constant, which is determined by the DAC output impedance RDAC (= 2 \* Ra), and the capacitive load on the DACOUT pad.

As an example, the STM32F407 defines the impedance output with buffer off at a maximum value of 15 kΩ. If a 10 pF capacitive load (including the parasitic capacitance of the device on DACOUT pad) is considered, to get ±1 LSB of the final value (from lowest to highest code) we have

![](images/2f3362ce87bd0dbef9f3c83604b3f2778a5d685c97d6b7bd12b0a3b9171070b9.jpg)

Solving for T gives T = CR \* N\* In 2 = 0.693 CR \* N = 1.8 µs. In this configuration the conversion time cannot be smaller than 1.8 µs (equivalent to a frequency of 555 kHz).

This analysis does not include any effect of the switching speed of the DAC itself and its transient. When using high speed, these factors cannot be ignored, they degrade the performance.

1.3

# External OpAmp implementation

As described in Section 1.2, the output DAC conversion time is specified by the embedded output buffer when buffer is enabled. When the buffer is disabled, the output impedance and the DACOUT capacitance (Cp) determine the conversion time.

This  coniguration or which  is ossible  ore he DACOT capacitanc. Bysig the external OpAmp in inverting mode, the DACOuT node voltage is fixed, as shown in Figure 2.

![](images/ecbce17b1dcf01eb159d954549dcc6ab348fc19dbfb743340cebcd911587d8d5.jpg)  
Figure 2. External OpAmp configuration

In this configuration there is a minor limitation due to the RC constant, the main limitation are the external OpAmp speed (gain bandwidth and slew rate) and the DAC digital data update rate. There are, however, some disadvantages. The feedback resistor R1 must be equal to the RDAC on chip of the STM32, otherwise it creates a DAC gain error.

Integrated resistors usually feature a rather wide spread on their absolute value, and significant variations over temperature, hence it is necessary to calibrate the gain error (discussed in detail in Section 2.2.4: Output gain calibration).

It is also possible to use the external OpAmp in voltage follower mode. This enhances the output bandwidth and slew rate, however the RDAc output impedance and the parasitic capacitor on the DACOUT form an RC filter that limits the speed performance.

For the voltage ollower mode, it is not necessary to perform the gain caliation.

# 1.4 Digital data update rate

The STM32 DAC output data need to be written to the DAC holding register (DHR), then the data is moved to the DAC output register (DOR) for the conversion.

Generally, the data are saved in a RAM, and the CPU is in charge of the transferring the data from RAM to DAC.

When using the DMA, the overall performance of the system is increased by freeing up the core: data go from memory to DAC by DMA, without need for any actions by the CPU. This keeps CPU resources free for other operations.

The trigger of the DAC conversion can be done by the software, external triggers, or by the timers. For the high speed conversion cases, it is recommended to use the timer trigger in combination with the data transfer done by the DMA.

The transfer speed from memory to the DAC is limited by several factors, among them:

the clock cycle of the APB or of the AHB (DAC clock) the DMA transfer cycle from memory to the DAC (includes the AHB to APB bridge) • the trigger mechanism itself.

The DAC on STM32F407x microcontrollers is running on the APB1:

• three cycles after the trigger, DHR data is moved to the DOR register • at the same time a DMA request is generated from DAC to DMA DMA transfer takes at least one APB clock cycle.

So a total of four APB clock cycles is needed to update the DOR data. As APB1 maximun clock is 42 MHz (for ST32F407x), 10.5 Msps is the maximum update rate for the DAC output register when timer trigger and the DMA are used for the data update.

The minimum transfer clock cycle by DMA to the DAC is not the same for all STM32 microcontrollers, because of the different bus configuration.

Table 2 shows the maximum sampling rate for different STM32 products.   
Table 2. Maximum sampling time   

<table><tr><td rowspan=1 colspan=1>Product</td><td rowspan=1 colspan=1>Maximum bus speed</td><td rowspan=1 colspan=1>DAC maximum sampling rate</td></tr><tr><td rowspan=1 colspan=1>STM32F0 series</td><td rowspan=1 colspan=1>48 MHz</td><td rowspan=1 colspan=1>4.8 Msps</td></tr><tr><td rowspan=1 colspan=1>STM32F100xx</td><td rowspan=1 colspan=1>24 MHz</td><td rowspan=1 colspan=1>2.4 Msps</td></tr><tr><td rowspan=1 colspan=1>STM32F101xxSTM32F103xxSTM32F105xxSTM32F107xx</td><td rowspan=1 colspan=1>36 MHz</td><td rowspan=1 colspan=1>4.5 Msps</td></tr><tr><td rowspan=1 colspan=1>STM32F2 series</td><td rowspan=1 colspan=1>30 MHz</td><td rowspan=1 colspan=1>7.5 Msps</td></tr><tr><td rowspan=1 colspan=1>STM32F3 series</td><td rowspan=1 colspan=1>36 MHz</td><td rowspan=1 colspan=1>4.5 Msps</td></tr><tr><td rowspan=1 colspan=1>STM32F40xSTM32F41x</td><td rowspan=1 colspan=1>42 MHz</td><td rowspan=1 colspan=1>10.5 Msps</td></tr><tr><td rowspan=1 colspan=1>STM32F42x</td><td rowspan=1 colspan=1>45 MHz</td><td rowspan=1 colspan=1>11.25 Msps</td></tr><tr><td rowspan=1 colspan=1>STM32F7 series</td><td rowspan=1 colspan=1>54 MHz</td><td rowspan=1 colspan=1>13.5 Msps</td></tr><tr><td rowspan=1 colspan=1>STM32G0 series</td><td rowspan=1 colspan=1>64 MHz</td><td rowspan=1 colspan=1>8.0 Msps</td></tr><tr><td rowspan=1 colspan=1>STM32G4 series</td><td rowspan=1 colspan=1>170 MHz</td><td rowspan=1 colspan=1>28.8 Msps30.9 Msps (DMA double data mode)</td></tr><tr><td rowspan=1 colspan=1>STM32H72xSTM32H73x</td><td rowspan=1 colspan=1>137.5 MHz</td><td rowspan=1 colspan=1>51.1 Msps</td></tr><tr><td rowspan=1 colspan=1>STM32H5 series</td><td rowspan=1 colspan=1>250 MHz</td><td rowspan=1 colspan=1>41.6 Msps</td></tr><tr><td rowspan=1 colspan=1>STM32H74xSTM32H75x</td><td rowspan=1 colspan=1>120 MHz</td><td rowspan=1 colspan=1>40.8 Msps</td></tr><tr><td rowspan=1 colspan=1>STM32H7AxSTM32H7Bx</td><td rowspan=1 colspan=1>140 MHz</td><td rowspan=1 colspan=1>49.2 Msps</td></tr><tr><td rowspan=1 colspan=1>STM32L0 series</td><td rowspan=1 colspan=1>32 MHz</td><td rowspan=1 colspan=1>4.0 Msps</td></tr><tr><td rowspan=1 colspan=1>STM32L1 series</td><td rowspan=1 colspan=1>32 MHz</td><td rowspan=1 colspan=1>3.2 Msps</td></tr><tr><td rowspan=1 colspan=1>STM32L4 series</td><td rowspan=1 colspan=1>80 MHz</td><td rowspan=1 colspan=1>10 Msps</td></tr><tr><td rowspan=1 colspan=1>STM32L4+ series</td><td rowspan=1 colspan=1>120 MHz</td><td rowspan=1 colspan=1>12 Msps</td></tr><tr><td rowspan=1 colspan=1>STM32L5 series</td><td rowspan=1 colspan=1>110 MHz</td><td rowspan=1 colspan=1>11 Msps</td></tr><tr><td rowspan=1 colspan=1>STM32U0 series</td><td rowspan=1 colspan=1>56 MHz</td><td rowspan=1 colspan=1>7 Msps</td></tr><tr><td rowspan=1 colspan=1>STM32U3 series</td><td rowspan=1 colspan=1>96 MHz</td><td rowspan=1 colspan=1>16 Msps</td></tr><tr><td rowspan=1 colspan=1>STM32U5 series</td><td rowspan=1 colspan=1>160 MHz</td><td rowspan=1 colspan=1>16 Msps</td></tr></table>

Note:

The values reported in Table 2 have been measured on the bench, when the bus is not used by any other system. In real applications some margin is needed.

# 1.4.1 DMA double data mode

Some DACs on STM32 MCUs support DMA double data mode. When the DMA controller is used in Normal mode, only 8- or 12-bit data are transfered by a DMA request. As the

STM32 MCUs can be accessed with 32-bit data bus, DMA double data mode transfers two 12-bit sets data at once, thus requiring lower bus occupation compared to the normal mode.

# 1.5 Summary

By using an external high speed OpAmp, it is possible to extend the speed performance of the DACs by more than 1 Msps. See Section 2 for an example showing how to use this technique on STM32 products.

# 2 Example

The example of the DAC used at high speed is based on STM32F407. It shows how to generate a 200 kHz sine wave by the DAC operating at 5 Msps.

# 2.1 External OpAmp choice

As indicated before, the external OpAmp defines the DAC total performance.

To choose the OpAmp, the following parameters must be considered.

• slew rate   
• gain bandwidth (GBW)   
• open loop gain   
• supply voltage range   
• output voltage swing performance • input common mode voltage range minimum stable gain.

For the lowest to highest code transient on 5 Msps case with VREF voltage 3.3 V, the OpAmp must have a slew rate higher than 3.3 \* 5 \* 106 = 16.5 V/μs.

If STM32 DAC operates at 3.3 V, it is possible to use the OpAmp 3.3 V supply. It is also possible to consider another analog supply rail, this is the option used in the example.

It is recommended to have at least two times of sampling speed of the gain bandwidth, so, for 5 Msps, GBW must be wider than 10 MHz.

To keep good DAC linearity, the open loop gain must be higher than 60 dB.

If the output voltage must be near the supply voltage, the output voltage swing of the OpAmp must preferably be rail to rail. Otherwise, if the voltage swing is near to the supply or ground rail, the signal is saturated and this results in distortion.

Even the OpAmp negative input is fixed at the reference voltage level, it is necessary to verify that the input common voltage range covers the reference voltage level with a margin.

The used OpAmp gain is about -1, so the OpAmp must be stable at this gain.

By considering the above criteria, LMH6645/6646/6647 from Texas Instruments fit the requirements:

• slew rate: 22 V/µs   
• gain band width: 55 MHz open loop gain: 87 dB   
• supply voltage range: 2.5 to 12 V   
• input common mode voltage 0.3 V beyond rails   
• output voltage swing 20 mV from rails stable from gain +1.

# 2.2 Software implementation

For this example the STM32F407 is powered with a 3.3 V supply.

# 2.2.1 Digital sine waveform pattern preparation

As described in AN3126 "Audio and waveform generation using the DAC in STM32 products", available on www.st.com, a sine wave pattern must be prepared according to the following formula

![](images/071d8f8751707f6778d5bc8f230d8965c8ef77c97e395d67aa0a8cb256d00268.jpg)

Dgtal input nvert tutoltages rversintwen nV+

The analog output voltage on each DAC channel pin is determined as:

![](images/ce93b6e3059ca24de6a3a9f285b20b4935aca70af4fca07aa951ba55d7a8f003.jpg)

So the analog sine waveform can be determined by the following equation

![](images/e6f99d1739b36dcc35a5e44f39ff54e999f99bd8ab46297f49eef94e5f1cc62f.jpg)

The table can be saved in the memory and transferred by DMA. The transfer is triggered by the same timer that triggers the DAC.

# 2.2.2 Setting the sine waveform frequency

To set the frequency of the sine wave signal,it is necessary to set the frequency of the timer trigger output. The frequency of the produced sine wave is

![](images/89b82b96d1c5688d9fc96e80a0108fca75397ac18e00f44bafd991ebed0498d2.jpg)

If TIMx_TRGO is 5 MHz (ns = 25), then the frequency of the DAC sine wave is 200 kHz.

To have the exact frequency on the output, the system clock must be adjusted, so that the timer can generate exactly 5 MHz.

In STM32F407, some timers can run with a clock frequency twice the one of the APB1 clock, so the resolution is two times better than APB1 clock. However, the DAC captures the trigger signal by APB1 clock, so the DAC timing cannot be better than APB1 clock.

For example, if the timer is programmed with 25 clock cycles (corresponding to 12.5 cycles of the APB1 clock), the DAC trigger occurs 12 times, then 13 times, alternately. So one APB1 clock results in jitter on every sampling period.

Here is the example of the clock setting:

• System clock source = PLL (HSE)   
• SYSCLK (Hz) = 160000000   
• HCLK (Hz) = 160000000   
• AHB prescaler = 1   
• APB1 prescaler = 4   
• APB2 prescaler = 2   
• HSE frequency (Hz) = 8000000   
• PLL_M = 8   
• PLL_N = 320   
• PLL_P = 2   
• PLL_Q = 7

TIM6 has been used for the trigger.

With this configuration, 80 MHz is the timer clock, so, to get 5 MHz trigger, the prescaler has been set to 1 (PSC = 0) and the counter to 16 (CNT = 15).

# 2.2.3 Offset calibration

The use of an external OpAmp introduces additional offsets, among them the one of the OpAmp itself, and the one coming from the external VREF resistor ladder.

To do the calibration, it is necessary to connect the output of the OpAmp to one of the available ADC channels of the STM32 microcontroller.

The procedure to calibrate the offset is the following one (see Table 3):

1. Set up the DAC DOR as 2047.   
2. Measure the OpAmp output by the ADC.   
3. Set up the DAC DOR of the ADC result of last measurement (in this case 2065).   
4. Verify the result with the ADC (in this case, 2048, still 1 LSB offset).

Table 3. Example of the offset calibration measurement   

<table><tr><td rowspan=1 colspan=1>DAC DOR</td><td rowspan=1 colspan=1>ADC result value</td></tr><tr><td rowspan=1 colspan=1>2047</td><td rowspan=1 colspan=1>2065</td></tr><tr><td rowspan=1 colspan=1>2065</td><td rowspan=1 colspan=1>2048</td></tr></table>

# 2.2.4 Output gain calibration

As indicated before, the output gain is defined by the ratio of the DAC output impedance and the feedback resistance of the external OpAmp.

The output gain calibration must be performed during the initialization of chip, and every time the temperature changes significantly (say more than 10 C). Temperature changes can be detected by the on-chip temperature sensor.

To do the calibration, connect the output of the OpAmp to one of the available STM32 ADC channels.

To calibrate the gain (see Table 4) go through the following steps:

1. Set up DAC DOR as 1023   
2. Measure the OpAmp output by the ADC   
3. Set up DAC DOR as 3071   
4. Measure the OpAmp output by the ADC.

Table 4. Example of the calibration measurement   

<table><tr><td rowspan=1 colspan=1>DAC DOR</td><td rowspan=1 colspan=1>ADC result value</td></tr><tr><td rowspan=1 colspan=1>1023</td><td rowspan=1 colspan=1>3135</td></tr><tr><td rowspan=1 colspan=1>3071</td><td rowspan=1 colspan=1>983</td></tr></table>

So the amplifier has a gain of 1.0508, obtained as (3135 - 983) / 2048.

This result can be used in the equation shown in Section 2.2.1. It is recommended to have some margin (say 100 mV) for each of the supply rail and ground rails. The digital code swing must be less than 200 mV from the supply, and also use the gain calibration factor

![](images/282c7db33b8bfb58e8006423379f953678eafbc89b1bddf4cf2621ea79692deb.jpg)

By using the above equation, Table 5 can be generated.

Table 5. Example of digital sample values   

<table><tr><td colspan="1" rowspan="1">Sample</td><td colspan="1" rowspan="1">Digital sample value YSineDigital (x)</td></tr><tr><td colspan="1" rowspan="1">0</td><td colspan="1" rowspan="1">2066</td></tr><tr><td colspan="1" rowspan="1">1</td><td colspan="1" rowspan="1">2521</td></tr><tr><td colspan="1" rowspan="1">2</td><td colspan="1" rowspan="1">2948</td></tr><tr><td colspan="1" rowspan="1">3</td><td colspan="1" rowspan="1">3319</td></tr><tr><td colspan="1" rowspan="1">4</td><td colspan="1" rowspan="1">3612</td></tr><tr><td colspan="1" rowspan="1">5</td><td colspan="1" rowspan="1">3807</td></tr><tr><td colspan="1" rowspan="1">6</td><td colspan="1" rowspan="1">3893</td></tr><tr><td colspan="1" rowspan="1">7</td><td colspan="1" rowspan="1">3864</td></tr><tr><td colspan="1" rowspan="1">8</td><td colspan="1" rowspan="1">3723</td></tr><tr><td colspan="1" rowspan="1">9</td><td colspan="1" rowspan="1">3477</td></tr><tr><td colspan="1" rowspan="1">10</td><td colspan="1" rowspan="1">3142</td></tr><tr><td colspan="1" rowspan="1">11</td><td colspan="1" rowspan="1">2740</td></tr><tr><td colspan="1" rowspan="1">12</td><td colspan="1" rowspan="1">2295</td></tr><tr><td colspan="1" rowspan="1">13</td><td colspan="1" rowspan="1">1837</td></tr><tr><td colspan="1" rowspan="1">14</td><td colspan="1" rowspan="1">1392</td></tr><tr><td colspan="1" rowspan="1">15</td><td colspan="1" rowspan="1">990</td></tr><tr><td colspan="1" rowspan="1">16</td><td colspan="1" rowspan="1">655</td></tr><tr><td colspan="1" rowspan="1">17</td><td colspan="1" rowspan="1">409</td></tr><tr><td colspan="1" rowspan="1">18</td><td colspan="1" rowspan="1">268</td></tr><tr><td colspan="1" rowspan="1">19</td><td colspan="1" rowspan="1">239</td></tr><tr><td colspan="1" rowspan="1">20</td><td colspan="1" rowspan="1">325</td></tr><tr><td colspan="1" rowspan="1">21</td><td colspan="1" rowspan="1">520</td></tr><tr><td colspan="1" rowspan="1">22</td><td colspan="1" rowspan="1">813</td></tr><tr><td colspan="1" rowspan="1">23</td><td colspan="1" rowspan="1">1184</td></tr><tr><td colspan="1" rowspan="1">24</td><td colspan="1" rowspan="1">1611</td></tr></table>

Note:

The output signal is inverted if compared to the digital code, because of the inverting amplifier stage of the external OpAmp.

# 2.3 Hardware implementation

As described in Section 2.1, an external component has been chosen.

The actual circuit is shown in Figure 3, the component values are listed in Table 6.

R1, chosen as typical output DAC impedance, is 12.5 kΩ (for other devices, consult the electrical specification in the datasheet). C1 is added to avoid overshoot on the output signal.

![](images/2cc6a8c62b3321e1a7f7badd25f96bb55a0768bc42c48a5a32a74df3a032ed2c.jpg)  
Figure 3. Circuit implementation

Table 6. Component values   

<table><tr><td rowspan=1 colspan=1>Type</td><td rowspan=1 colspan=1>Component</td><td rowspan=1 colspan=1>Value</td></tr><tr><td rowspan=3 colspan=1>Resistor</td><td rowspan=1 colspan=1>R1</td><td rowspan=1 colspan=1>12 kΩ</td></tr><tr><td rowspan=1 colspan=1>R2</td><td rowspan=1 colspan=1>10 kΩ</td></tr><tr><td rowspan=1 colspan=1>R3</td><td rowspan=1 colspan=1>10 kΩ</td></tr><tr><td rowspan=3 colspan=1>Capacitor</td><td rowspan=1 colspan=1>C1</td><td rowspan=1 colspan=1>5 pF</td></tr><tr><td rowspan=1 colspan=1>C2</td><td rowspan=1 colspan=1>100 nF</td></tr><tr><td rowspan=1 colspan=1>C3</td><td rowspan=1 colspan=1>100 nF</td></tr></table>

# 3 Measurements

The measurements have been done on a STM32F4DISCOVERY board with the configuration shown in Figure 3.

# 3.1 Board modification

STM32F407 DAC1 output is assigned to PA4, which, in turn, is connected to the on-board audio codec through a 100 kΩ resistor to GND. To remove this effect, the R48 (0 Ω) resistor has been removed from the board.

# 3.2 Measurement results

The output signal is shown in Figure 4, while Figure 5 is the corresponding FFT analysis.

![](images/f2bc6ee0f878b4d95d4333994fe87e34f740336111b34208cbd0835fdf9f8b77.jpg)

Output swing is not equal to 3.1 Vp, as sampling time is not aligned with the peak of the sine wave signal.

![](images/8289ab0af421fb733e158e74f364aecc93fc9ff4ffbc4d9ea9eed378aeeed7f2.jpg)  
Figure 5. FFT result

The second and third harmonics are around the noise level.

# 4 Conclusion

The DAC used by STM32F4 microcontrollers has been characterized up to 1 Msps. By using a high speed external OpAmp, it can operate up to 5 Msps.

Additional remarks:

by using high speed sampling rate, it is possible to reduce the anti-aliasing filter order • by using the on chip ADC, it is possible to calibrate the output swing and the offset.

# 5 Revision history

Table 7. Document revision history   

<table><tr><td rowspan=1 colspan=1>Date</td><td rowspan=1 colspan=1>Revision</td><td rowspan=1 colspan=1>Changes</td></tr><tr><td rowspan=1 colspan=1>03-Nov-2014</td><td rowspan=1 colspan=1>1</td><td rowspan=1 colspan=1>Initial release.</td></tr><tr><td rowspan=1 colspan=1>02-Aug-2015</td><td rowspan=1 colspan=1>2</td><td rowspan=1 colspan=1>Added STM32L4 series in Table 1: Applicable products and in Table 2:Maximum sampling time.</td></tr><tr><td rowspan=1 colspan=1>19-Sep-2019</td><td rowspan=1 colspan=1>3</td><td rowspan=1 colspan=1>Document scope extended to STM32L4+, STM32L5, STM32H7,STM32G0 and STM32G4 series, hence updated Table 1: Applicableproducts and Table 2: Maximum sampling time.Updated Section 1.1: DAC equivalent circuit, Section 1.3: ExternalOpAmp implementation and Section 2.2.4: Output gain calibration.Added Section 1.4.1: DMA double data mode.Updated Figure 1: DAC equivalent circuit.Minor text edits across the whole document.</td></tr><tr><td rowspan=1 colspan=1>03-Oct-2022</td><td rowspan=1 colspan=1>4</td><td rowspan=1 colspan=1>Document scope extended to STM32U5 series.Updated Table 1: Applicable products and Table 2: Maximum samplingtime.Minor text edits across the whole document.</td></tr><tr><td rowspan=1 colspan=1>09-Jan-2025</td><td rowspan=1 colspan=1>5</td><td rowspan=1 colspan=1>Document scope extended to STM32H5, STM32U0, and STM32U3series, hence updated Table 1: Applicable products and Table 2:Maximum sampling time.Minor text edits across the whole document.</td></tr></table>

# IMPORTANT NOTICE  READ CAREFULLY

acknowledgment.

the design of purchasers' products.

No license, express or implied, to any intellectual property right is granted by ST herein.

product or service names are the property of their respective owners.

I