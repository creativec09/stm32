# Interfacing PDM digital microphones using STM32 MCUs and MPUs

# Introduction

Digital MEMS (microelectromechanical systems) microphones target all audio applications where small size, high sound quality, reliability and affordability are key requirements.

Their combination of small footprint and noise immunity allows the implementation of multiple microphones in a single device, creating an increasing growth of audio in industrial and consumer applications by offering a hands-free human machine interface, noise cancellation, and high quality audio capture.

The STM32 32-bit Arm® Cortex® MCUs and the STM32 Arm® Cortex® MPUs offer a wide audio capability with a rich connectivity, including serial and enhanced voice-acquisition interfaces allowing the user to easily build solution for microphone-based applications.

This document targets digital MEMS microphones having a pulse-density modulated (PDM) output and describe how to connect them in mono and stereo configurations to STM32 MCUs and MPUs by using the SPI/I2S, SAI and DFSDM peripherals. It provides guidelines and examples based on STM32CubeMX and shows how to properly configure the STM32 device to acquire and handle raw data from the microphones in order to transform this raw data into standard data for audio.

# Contents

# PDM digital microphones overview . . . . 7

1.1 Sound acquisition overview   
1.2 PDM digital microphone block diagram 8   
1.3 Basic digital microphones connection 9

1.4 PDM and PCM signals . 12

1.4.1 Pulse density modulation (PDM) 12   
1.4.2 Pulse code modulation (PCM) 12   
1.4.3 PDM to PCM conversion 13

1.5 Acoustic parameters 13

1.5.1 Sensitivity . . . .13   
1.5.2 Signal-to-noise ratio (SNR) 13   
1.5.3 Acoustic overload point (AOP) 14   
1.5.4 Power supply rejection ratio (PSRR) 14

1.6 Added value of digital microphones 14

1.7 Available ST digital microphones 15

# Connecting PDM digital microphones to STM32 MCUs and MPUs . . 16

2.1 Serial peripheral interface (SPI) /Inter-IC sound (I2S) 16

2.1.1 Mono configuration .16   
2.1.2 Stereo configuration . . .18

2.2 Serial audio interface (SAI) 20

2.2.1 Using a single sub-block 20   
2.2.2 Using two synchronous SAl sub-blocks . 23   
2.2.3 Using PDM interface .24

Digital filter for sigma delta modulators (DFSDM) . 27

2.3.1 Stereo configuration . 28

Clocking considerations 28

2.4.1 The digital microphone clock .28   
2.4.2 The peripheral clocks 29

2.5 GPIOs number considerations 31

# Digital signal processing .. . . 32

3.1 PDM audio software decoding library . . 32

3.1.1 Overview .32   
3.1.2 Digital data flow 32   
3.1.3 Digital signal processing .33

.2 DFSDM filters for digital signal processing .. 34

3.2.1 Digital data flow: acquisition and processing. .34

# Examples of configuration based on STM32CubeMX . . ... 35

4.1 Example 1: Interfacing digital microphones in mono or stereo mode with I2S, SPI or a single SAI sub-block . 35

4.1.1 Hardware configuration using STM32CubeMX. .35

4.1.2 Adding PDM software decoding library middleware files . . . . . . 47

4.2 Example 2: Interfacing digital microphones in stereo mode with SAl using two synchronous sub-blocks 48 4.2.1 SAI configuration using STM32CubeMX 48 4.2.2 Adding PDM software decoding library middleware files .53

4.3 Example 3: Interfacing digital microphones in stereo mode with SAI using PDM interface 53

4.3.1 SAI configuration using STM32CubeMX .53   
4.3.2 Adding PDM software decoding library middleware files . 57

4 Example 4: Interfacing digital microphones using DFSDM 58

4.4.1 DFSDM configuration using STM32CubeMX .58

Conclusion . 64

Revision history .. 65

# List of tables

Table 1. DOUT signal pattern selection 9   
Table 2. Pin description 9   
Table 3. Added value of digital microphone 14   
Table 4. ST digital microphones . 15   
Table 5. Recommended IO lines versus the number digital microphones   
to be connected 24   
Table 6. Applications examples and the associated microphone clock frequency . 29   
Table 7. Hardware used to connect one digital microphone. 31   
Table 8. Hardware used to connect two digital microphones. 31   
Table 9. Hardware used to connect four digital microphones. 31   
Table 10. I2S2 clock configuration and accuracy 36   
Table 11. SPI clock configuration and accuracy. 39   
Table 12. Clock configuration and accuracy .. 42   
Table 13. SAI clock configuration and accuracy. 49   
Table 14. DFSDFM filter order values 60   
Table 15. DFSDM clock configuration accuracy values 63   
Table 16. Document revision history 65

# List of figures

Figure 1. Example of sound acquisition in audio application . . 7   
Figure 2. Typical PDM digital MEMS microphone block diagram 8   
Figure 3. Mono configuration - Generating data on right channel 9   
Figure 4. Right channel data pattern 10   
Figure 5. Mono configuration - Generating data on left channel 10   
Figure 6. Left channel data pattern 10   
Figure 7. Stereo configuration: Sharing one data line 11   
Figure 8. Stereo configuration data pattern 11   
Figure 9. PDM signal 12   
Figure 10. PCM signal 13   
Figure 11. Connecting one digital microphone to SPI or I2S in mono configuration 17   
Figure 12. Connecting two digital microphone to SPI block in stereo configuration 18   
Figure 13. Stereo mode timing diagram. .. 19   
Figure 14. Connecting one digital microphone to SAl in mono configuration 20   
Figure 15. Connecting two digital microphones to SAl in stereo configuration   
using a SAI sub-block and a timer 22   
Figure 16. Connecting two digital microphone to SAl in stereo configuration   
using two synchronous SAl sub-blocks 23   
Figure 17. PDM interface capability on interfacing up to four microphone pairs. 25   
Figure 18. Data format when using the SAI PDM interface with a slot size of 32 bits,   
and 8 microphones . 26   
Figure 19. Data format when using the SAI PDM interface with a slot size of 8 bits,   
and 8 microphones. 26   
Figure 20. DFSDM capability to interface up to 4 digital microphones 27   
Figure 21. Stereo configuration . . 28   
Figure 22. Bus and kernel clock topology for SPI 30   
Figure 23. Bus and kernel clock topology for SAI and DFSDM. 30   
Figure 24. Digital data acquisition and processing (block diagram). 33   
Figure 25. Digital signal processing ... 33   
Figure 26. Digital data acquisition and processing using DFSDM (block diagram) . 34   
Figure 27. I2S GPIO pin configuration. 36   
Figure 28. I2S2 clock configuration 37   
Figure 29. I2S configuration. . 37   
Figure 30. I2S parameter settings 38   
Figure 31. I2S DMA settings . 38   
Figure 32. SPI GPIO and pin configuration 39   
Figure 33. SPI clock configuration 39   
Figure 34. SPI configuration. 40   
Figure 35. SPI parameter setting 40   
Figure 36. SPI DMA settings 41   
Figure 37. SAI GPIO and pin configuration 41   
Figure 38. SAI clock configuration at 16 kHz for mono mode 42   
Figure 39. SAI configuration 43   
Figure 40. SAI parameter setting . 44   
Figure 41. SAI DMA settings . 45   
Figure 42. DMA request settings 45   
Figure 43. TIM GPIO and pin configuration . 46   
Figure 44. TIM configuration 46   
Figure 45. TIM parameter settings . . 47   
Figure 46. SAI GPIO and pin configuration 48   
Figure 47. SAI clock configuration. 49   
Figure 48. SAI parameter settings . 51   
Figure 49. SAIB parameter settings. 52   
Figure 50. SAI DMA settings 52   
Figure 51. SAI GPIO and pin configuration 53   
Figure 52. SAI clock configuration for 2 microphones at 16 kHz . 54   
Figure 53. SAI configuration 54   
Figure 54. SAI parameter settings 55   
Figure 55. SAI DMA settings 56   
Figure 56. CORTEX_M7 configuration 56   
Figure 57. Cortex M7 parameter settings 57   
Figure 58. DFSDM GPIO configuration in stereo mode. 58   
Figure 59. DFSDM pin configuration . 59   
Figure 60. DFSDM Channel 1 configuration 59   
Figure 61. DFSDM Channel 0 configuration 60   
Figure 62. DFSDM Filter 0 configuration . 61   
Figure 63. DFSDM Filter 1 configuration . 61   
Figure 64. DFSDM output clock configuration 62   
Figure 65. DFSDM DMA setting 62   
Figure 66. DFSDM clock configuration .63

# PDM digital microphones overview

This section provides a brief description of PDM digital microphones and presents basic cases of interfacing them with STM32 devices. STM32 MCUs and MPUs are Arm®(a) based devices.

# 1.1

# Sound acquisition overview

The digital MEMS microphone is a sensor that convert acoustic pressure waves into a digital signal. The STM32 MCUs and MPUs acquire digital data from the microphone(s) through particular peripherals to be processed and transformed into data standard for audio. The audio data is then handled by the microcontroller according to the targeted audio application.

![](images/218e5d0242d32e47476600216c1ecd45953e9b96c31fe29afc1d8f4e005e23b1.jpg)  
Figure 1. Example of sound acquisition in audio application

# 1.2 PDM digital microphone block diagram

The main parts in a digital microphone are a MEMS transducer, an amplifier and a PDM modulator.

![](images/d8aae83a29799d4ab0d1f5358a17b6f9bd8926462cbdedd7d8fb958e814e042a.jpg)  
Figure 2. Typical PDM digital MEMS microphone block diagram

MS47147V1

# MEMS transducer

The MEMS transducer is a variable capacitance that converts the change into air pressure caused by sound waves to a voltage.

# Amplifier

The amplifier buffers the voltage provided by the MEMS transducer, and provides a sufficiently strong signal to the PDM modulator.

# PDM modulator

PDM modulator converts the buffered analog signal into a serial pulse density modulated signal. The clock input (CLK) is used to control the PDM modulator. The clock frequency range for ST digital microphones is from 1 MHz to 3.25 MHz. This frequency defines the sampling rate at which the amplifier's analog output signal is sampled to produce a discretetime representation (PDM bitstream).

# Channel select

The microphone's output is driven to the proper level on a selected clock edge and then goes into a high impedance state for the other half of the clock cycle. The channel select defines the clock edge on which the digital microphone outputs valid data. The LR pin must be connected to Vdd or GND.

Table 1 shows how to select the DOUT signal pattern.

Table 1. DOUT signal pattern selection   

<table><tr><td rowspan=2 colspan=1>LR</td><td rowspan=1 colspan=2>DOUT</td></tr><tr><td rowspan=1 colspan=1>CLK low</td><td rowspan=1 colspan=1>CLK high</td></tr><tr><td rowspan=1 colspan=1>GND</td><td rowspan=1 colspan=1>Valid data</td><td rowspan=1 colspan=1>High impedance</td></tr><tr><td rowspan=1 colspan=1>Vdd</td><td rowspan=1 colspan=1>High impedance</td><td rowspan=1 colspan=1>Valid data</td></tr></table>

# Power

Power delivers Vdd and GND supplies to the different digital microphone's components. The power supply should be properly provided to the microphone since any ripple can generate noise on the output.

# Pin description

Table 2. Pin description   

<table><tr><td>Pin name</td><td>Function</td><td>Direction</td></tr><tr><td>Vdd</td><td>3.3 V power supply</td><td>Input</td></tr><tr><td>GND</td><td>O V</td><td>Input</td></tr><tr><td>LR</td><td>Left/right selection</td><td>Input</td></tr><tr><td>CLK</td><td>Synchronization clock</td><td>Input</td></tr><tr><td>DOUT</td><td>Left/righ PDM data output</td><td>Output</td></tr></table>

1.3

# Basic digital microphones connection

# Mono mode

In this mode the LR pin can be either connected to Vdd or to GND.

LR pin is connected to Vdd

![](images/4189e09e327daac6c8109518f6b8ac7b0c09092f7b41bf02d7e55dd135215b2b.jpg)  
Figure 3. Mono configuration - Generating data on right channel

On the rising edge of the clock, the microphone generates valid data for half of the clock period, then goes into a high impedance state for the other half.

![](images/44ca5ccd4d9439d6bd32d50db98fc63be549213990af29f7c492187997c65cf0.jpg)  
Figure 4. Right channel data pattern

# LR pin is connected to GND

![](images/af886236226426909a5109be7707faada167b61eb702e3c581874285374083dd.jpg)  
Figure 5. Mono configuration - Generating data on left channel

On the falling edge of the clock, the microphone generates valid data for half of the clock period, then goes into a high impedance state for the other half.

![](images/ece357a6e75233973a34046e2df4ec34e8ec530fccbd9f3c0ec603a785aa4493.jpg)  
Figure 6. Left channel data pattern

# Stereo configuration

![](images/5d7c8ac3cd651755f636980da58f9636590157f5c100b45268d6dca914c9ae67.jpg)  
Figure 7. Stereo configuration: Sharing one data line

MS47152V1

Two different digital MEMS microphones are connected on the same data line, configuring the first to generate valid data on the rising edge of the clock by setting the LR pin to Vdd and the other on the falling edge by setting the LR pin to GND.

![](images/d4b1462616fc095cef2ddfa5d0ca82419dd676ef27e2a5dd1c8e2cf273ada72a.jpg)  
Figure 8. Stereo configuration data pattern

# 1.4

# PDM and PCM signals

# 1.4.1 Pulse density modulation (PDM)

PDM is a form of modulation used to represent an analog signal in the digital domain. It is a high frequency stream of 1-bit digital samples. In a PDM signal, the relative density of the pulses corresponds to the analog signal's amplitude. A large cluster of 1s correspond to a high (positive) amplitude value, when a large cluster of Os would correspond to a low (negative) amplitude value, and alternating 1s and Os would correspond to a zero amplitude value.

![](images/1c78006ca7845470cc3c862dacc172a80ebe01fe1f6d2ec752207aff884fe4ae.jpg)  
Figure 9. PDM signal

# 1.4.2 Pulse code modulation (PCM)

In the PCM signal, specific amplitude values are encoded into pulses.

A PCM stream has two basic properties that determine the stream's fidelity to the original analog signal:

• the sampling rate • the bit depth

The sampling rate is the number of samples of a signal that are taken per second to represent it digitally. The bit depth determines the number of bits of information in each sample.

![](images/7249224f40b4aa409685c8281fd7c87c606cc428d1b6fc1d688dde65b439ef13.jpg)  
Figure 10. PCM signal

# 1.4.3 PDM to PCM conversion

In order to convert the PDM stream into PCM samples, the PDM stream needs to be filtered and decimated.

In the decimation stage, the sampling rate of the PDM signal is reduced to the targeted audio sampling rate (16 kHz for example). By selecting 1 of each M samples, the sample rate is reduced by a factor of M. Therefore, the PDM data frequency (which is the frequency of the microphone clock) is M times the target audio sampling frequency needed in an application, where M is the decimation factor.

PDM frequency = Audio sampling frequency × decimation factor

The decimation factor is generally in the range of 48 to 128.

The decimation stage is preceded by a low-pass filter to avoid distortion from aliasing.

# 1.5 Acoustic parameters

# 1.5.1 Sensitivity

The sensitivity is the level of the electrical signal (expressed in dBFS) that the digital microphone outputs for a given acoustic reference signal.

Generally the sensitivity of a microphone is given using a tone of 1 kHz, at 1 Pa (or 94 dBSPL) as reference signal.

# 1.5.2 Signal-to-noise ratio (SNR)

The SNR specifies the ratio between the reference signal (94 dBSPL@1kHz) and the amount of residual noise at the microphone output.

HigherRoffers an voiceclariy s well as arn hans-reeitellity

# 1.5.3 Acoustic overload point (AOP)

The AOP is the maximum acoustic signal, which the microphone can capture with acceptable distortion (some specifications allow up to 10% in terms of distortion at the acoustic overload point).

# 1.5.4 Power supply rejection ratio (PSRR)

The PSRR specification quantifies the capability of the microphone to reject noise relative to power supply changes.

# 1.6 Added value of digital microphones

Table 3. Added value of digital microphone   

<table><tr><td rowspan=1 colspan=1>Feature</td><td rowspan=1 colspan=1>Added value</td></tr><tr><td rowspan=1 colspan=1>Immunity to RF noise andelectromagnetic interference (EMI)</td><td rowspan=1 colspan=1> Less integration effort</td></tr><tr><td rowspan=1 colspan=1>Analog signal conditioning notrequired</td><td rowspan=1 colspan=1>— Easier application design- Direct interface to codecs with digital microphonesinterfaceStereo mode needs only one data lineSignificant saving on PCB area with more microphones insystem- Flexibility to add additional microphones into theapplication</td></tr><tr><td rowspan=1 colspan=1>Robust digital transmission</td><td rowspan=1 colspan=1>Easy MEMS positioning on application system- Standard digital conditioning- Allows audio enhancement integration for stereo capture,noise cancellation and beam forming</td></tr></table>

# 1.7 Available ST digital microphones

Table 4 shows the available ST digital microphone.

Table 4. ST digital microphones   

<table><tr><td rowspan=1 colspan=1>Part number</td><td rowspan=1 colspan=1>Top/bottomport</td><td rowspan=1 colspan=1>Supply voltage(V)</td><td rowspan=1 colspan=1>SNR(dB)</td><td rowspan=1 colspan=1>Sensitivity(dBFS)</td><td rowspan=1 colspan=1>AOP(dBSPL)</td></tr><tr><td rowspan=1 colspan=1>MP34DB02</td><td rowspan=1 colspan=1>Bottom</td><td rowspan=1 colspan=1>1.64 to 3.6</td><td rowspan=1 colspan=1>62.6</td><td rowspan=1 colspan=1>-26</td><td rowspan=1 colspan=1>120</td></tr><tr><td rowspan=1 colspan=1>MP34DT01-M</td><td rowspan=1 colspan=1>Top</td><td rowspan=1 colspan=1>1.64 to 3.6</td><td rowspan=1 colspan=1>61</td><td rowspan=1 colspan=1>-26</td><td rowspan=1 colspan=1>120</td></tr><tr><td rowspan=1 colspan=1>MP34DT02</td><td rowspan=1 colspan=1>Top</td><td rowspan=1 colspan=1>1.64 to 3.6</td><td rowspan=1 colspan=1>60</td><td rowspan=1 colspan=1>-26</td><td rowspan=1 colspan=1>120</td></tr><tr><td rowspan=1 colspan=1>MP34DT04</td><td rowspan=1 colspan=1>Top</td><td rowspan=1 colspan=1>1.6 to 3.6</td><td rowspan=1 colspan=1>64</td><td rowspan=1 colspan=1>-26</td><td rowspan=1 colspan=1>120</td></tr><tr><td rowspan=1 colspan=1>MP34DT04-C1</td><td rowspan=1 colspan=1>Top</td><td rowspan=1 colspan=1>1.6 to 3.6</td><td rowspan=1 colspan=1>64</td><td rowspan=1 colspan=1>-26</td><td rowspan=1 colspan=1>120</td></tr><tr><td rowspan=1 colspan=1>MP34DT05</td><td rowspan=1 colspan=1>Top</td><td rowspan=1 colspan=1>1.6 to 3.6</td><td rowspan=1 colspan=1>64</td><td rowspan=1 colspan=1>-26</td><td rowspan=1 colspan=1>122.5</td></tr><tr><td rowspan=1 colspan=1>MP45DT02-M</td><td rowspan=1 colspan=1>Top</td><td rowspan=1 colspan=1>1.64 to 3.6</td><td rowspan=1 colspan=1>61</td><td rowspan=1 colspan=1>-26</td><td rowspan=1 colspan=1>120</td></tr></table>

# Connecting PDM digital microphones to STM32 MCUs and MPUs

This section describes how to connect digital MEMS microphones to the SPI/ I2S, SAI and DFSDM peripherals embedded in STM32 MCUs and MPUs in both mono and stereo configurations.

# 2.1 Serial peripheral interface (SPI) /Inter-IC sound (I2S)

The STM32 MCUs and MPUs offer a serial peripheral interface block named SPI. Some of these SPI blocks also offer the possibility to use the Inter-IC sound audio protocol (2S). In addition, the STM32 devices offer two versions of the SPI block, in this document, the oldest version is named SPI-V1, and latest version is named SPI-V2. When we refer to SPI block it means indifferently SPI-V1 or SPI-V2.

The SPI-V2 is currently available on STM32H7 Series.

It is possible to connect one or two digital microphones to a SPl block by either using the SPI or I2S protocol.

The SPI protocol provides simple communication interface allowing the   
microcontrollers to communicate with external devices.   
The I2S protocol is widely used to transfer audio data from a microcontroller/DSP (digital signal processor) to an audio codec, in order to play melodies or to capture sound from a microphone.

# 2.1.1 Mono configuration

A single digital microphone is connected to the SPI block. The SPI block can be configured either in SPI or in I2S mode.

In both cases, the SPI block is configured in master receiver mode. In this mode, the peripheral provides the clock to the digital microphone. The audio samples are acquired through the serial data pin.

![](images/4fbf2bb1dcca72defd8aefdf604121bf5d9e4c30b1e722305827bbfa30128f48.jpg)  
Figure 11. Connecting one digital microphone to SPI or I2S in mono configuration

MSv48085V1

If the SPI protocol is used, the L/R channel selection (LR) pin of the microphone can be connected either to Vdd or to GND. The SPI clock polarity shall be aligned with the configuration of L/R input.

If L/R = GND, then the SPI shall sample the incoming data using the rising edge of SPIx_SCK,   
If L/R = Vdd, then the SPI shall sample the incoming data using the falling edge of SPIx_SCK,

If the I2S protocol is used, it is recommended to set the L/R channel selection (LR) pin of the microphone to GND. By default the I2S protocol samples the incoming data using the rising edge of I2Sx_CK. Note that the SPI-V2 block also offers the possibility to configure the sampling edge for the I2S protocol.

# Data format

The samples acquired by the SPI block in I2S or SPI mode can be stored into the memory using either DMA or interrupt signaling.

The receive data register (SPIx_DR) provides contiguous bits from the microphone like shown in the example hereafter for a 16-bit format:

<table><tr><td>Bit:</td><td>15</td><td>14</td><td>13</td><td>12</td><td>11</td><td>..•</td><td>0</td></tr><tr><td>Content:</td><td>M1_bN</td><td>M1_bN+1</td><td>M1_bN+2</td><td>M1_bN+3</td><td>M1_bN+4</td><td>..•</td><td>M1_bN+15</td></tr></table>

M1_bxx represents the data bits from the digital microphone 1, and M1_bN is the older bit.

Note:

The bit order of the received samples can be reversed if the interface is programmed in LSB first instead of MSB first. Peripherals generally support various data size which are not detailed here.

# 2.1.2 Stereo configuration

Two digital microphones can be connected to the SPI block using a timer. The SPI block can be configured either in SPI or in I2S mode.

In both cases, the SPI block is configured in master receiver mode. In this configuration, the SPI peripheral operates at twice the microphone frequency in order to read the data provided by both microphones, on the falling edge of its clock. This allows the two microphones to share a single data line.

The SPI block provides the clock to an embedded timer which divides the serial interface clock (SPIx_SCK or I2Sx_CK) by 2. The divided clock is delivered to the digital microphone. The audio samples are acquired by the I2S peripheral from the digital microphones data output pins.

![](images/b49c9c7c416b64aacd6a887c5296e29545ad44dcf41f7feac52abfd8fc201cc9.jpg)  
Figure 12. Connecting two digital microphone to SPI block in stereo configuration   
- PDM clock Under parenthesis is the name of IOs when the I2S protocol is selected

MSv48086V1

# Using the timer as clock generator

When the timer is used to generate the clock for the digital microphones, two points have to be taken into account:

The application must insure that the delay introduced by the clock division performed by the timer still insures a margin in the setup time (Ts) of the samples provided by the microphones. For that purpose, the timer shall use a clock as fast as possible. The maximum delay (Td) introduced by the timer between the input (TIMxCHIN) and the output clock (TIMxCHOUT) is 5 clock cycles of the timer reference clock. The timers generally use their APB clock or a multiple of their APB clock as reference. See Figure 13.

The application must insure that the peripheral providing the clock to TIMxCHIN input and the timer used for the division, are working with the same reference clock. If this rule is not respected, then from time to time the digital microphone receives a clock having a longer or shorter period. This jitter may degrade the quality of the analog to digital conversion of the microphone.

![](images/beef9c2902050e94ac3ea63ff4575b91636b0da71d2308b99b63d981bae55685.jpg)  
Figure 13. Stereo mode timing diagram

# Data format

The samples acquired by the SPI block in I2S or SPI mode can be stored into the memory using either DMA or interrupt signaling.

In this configuration, the data read from the microphones are interleaved bit per bit. The data stored into the SPIx_DR register is interleaved as shown in the example hereafter for 16-bit format:

<table><tr><td>Bit:</td><td>15</td><td>14</td><td>13</td><td>12</td><td>11</td><td>·.•</td><td>0</td></tr><tr><td>Content:</td><td>M1_bN</td><td>M2_bN</td><td>M1_ bN+1</td><td>M2_bN+1</td><td>M1_bN+2</td><td>··</td><td>M2_bN+7</td></tr></table>

M1_bxx represents the data bits from the digital microphone 1, and M1_bn is the older bit.   
M2_bxx represents the data bits from the digital microphone 2, and M2_bn is the older bit.

The SPl-V1 and SPl-V2 offer several data formats, for example the bit order of the received samples can be reversed if the interface is programmed in LSB first instead of MSB first, but is it important to notice that bits from microphone 1 (M1) and bits from microphone 2 (M2) are always interleaved.

A software de-interleaving module is needed to separate the signal from the two microphones streams and to allow further processing like PDM-to-PCM conversion.

# 2.2 Serial audio interface (SAl)

The SAI integrated inside STM32 MCUs and MPUs provides an interface allowing the microcontroller to communicate with external audio devices such as amplifiers, microphones, speakers, or audio processors. The SAl is composed of two independent subblocks that can operate synchronously or not. Each sub-block features its own audio clock generator.

Some SAl also offer a dedicated PDM interface that can support up to 8 digital microphones.

# 2.2.1 Using a single sub-block

# Mono configuration

The digital microphone is connected to one of the sub-blocks of the serial audio interface (SAl) peripheral in mono configuration. The SAl sub-block is configured in master receive mode. In this configuration, the SAl sub-block provides the clock to the digital microphone. The audio samples are acquired by the SAl sub-block from the digital microphone data output (DOUT) pin through the Serial Data (SD) pin.

![](images/b0074a2c6dd43367b0153354cb38919ce60a93514808e4d13ea5dde85e53d63e.jpg)  
Figure 14. Connecting one digital microphone to SAl in mono configuration

The L/R channel selection (LR) pin of the microphone can be connected either to Vdd or to GND. The microphone outputs data on the rising or falling edges of the incoming clock signal depending on the selected channel. The sampling edge of the SAl clock shall be configured accordingly.

# Note:

The other SAl sub-block is completely independent and can be used for another purpose: for example it can be connected to an external audio codec.

# Data format

The samples acquired by the SAl sub-block can be stored into the memory using either DMA or interrupt signaling.

The receive data register (SAI_ADR, SAI_BDR) provides contiguous bits from the microphone like shown hereafter:

<table><tr><td>Bit:</td><td>k</td><td>k-1</td><td>k-2</td><td>k-3</td><td>k-4</td><td>·.•</td><td>0</td></tr><tr><td>Content:</td><td>M1_bN</td><td>M1_bN+1</td><td>M1_bN+2</td><td>M1_bN+3</td><td>M1_bN+4</td><td>..•</td><td>M1_bN+k</td></tr></table>

M1_bxx represents the data bits from the digital microphone 1, and M1_bN is the older bit position inside SAI_ADR/BDR registers. For example if DS[2:0] is set to '010' (8 bits), then 'k' is equal to 7.

The size of data stored into the SAl_ADR/BDR registers depends on the programming of the data size (DS[2:0]), in addition SLOTSZ[1:0] must be forced to 0.

Note that the bit order of the received samples can be reversed if the interface is programmed in LSB first instead of MSB first.

Note:

The data inside SAl_ADR/BDR registers are always right aligned.

# Stereo configuration

Two digital microphones can be connected to a single SAl sub-block using an internal timer. The SAI sub-block is configured in master receiver mode. In this configuration, the SAIl subblock operates at twice the microphone frequency in order to read the data provided by both microphones, on the same edge of its clock. This allows the two microphones to share a single data line (Refer to Figure 15).

The SAl sub-block provides the clock (SAl_SCK_x) to an embedded timer which performs a division by 2. The divided clock is delivered to the digital microphone.

# Note:

The other SAl sub-block is completely independent and can be used for another purpose: for example it can be connected to an external audio codec.

Timing diagram shown in Figure 13 is also valid for this case. Refer also to section Using the timer as clock generator for recommendations concerning the use of the timer.

![](images/5029418618499a0ad80e56bf86cc1a7b669bcea29a5c533af1fbc5c6ad3be3db.jpg)  
Figure 15. Connecting two digital microphones to SAl in stereo configuration using a SAl sub-block and a timer

# Data format

The samples acquired by the SAl sub-block can be stored into the memory using either DMA or interrupt signaling.

In this configuration, the data read from the microphones are interleaved bit per bit. The data stored into the SAl_ADR/BD register is interleaved as shown in the example hereafter:

<table><tr><td>Bit:</td><td>k</td><td>k-1</td><td>k-2</td><td>k-3</td><td>·.•</td><td>1</td><td>0</td></tr><tr><td>Content:</td><td>M1_bN</td><td>M2_bN</td><td>M1_bN+1</td><td>M2_bN+1</td><td>. ...</td><td>M1_bN+(K-1)/2</td><td>M2_bN+(K-1)/2</td></tr></table>

M1_bxx represents the data bits from the digital microphone 1, and M1_bn is the older bit. M2_bx represents data bits from the digital microphone 2, and M2_bn is the older bit. 'k' is the bit position inside SAI_ADR/BDR registers, for example if DS[2:0] is set to '100' (16 bits), then 'k' is equal to 15.

The size of data stored into the SAl_ADR/BDR depends on the programming of the data size (DS[2:0]), in addition SLOTSZ[1:0] must be forced to 0.

Note:

The bit order of the received samples can be reversed if the interface is programmed in LSB first instead of MSB first, but is it important to notice that bits from microphone 1 (M1) and bits from microphone 2 (M2) are always interleaved.

The data inside SAl_ADR/BDR registers are always right aligned.

A software de-interleaving module is needed to separate the signal from the two microphones streams to allow further processing like PDM-to-PCM conversion.

# 2.2.2 Using two synchronous SAl sub-blocks

Two digital microphones can be connected to the SAl peripheral without using an embedded timer by synchronizing two SAl sub-blocks. Each microphone is connected to a SAl sub-block. One of the SAl sub-block is configured in Master-receive mode while the other sub-block is configured in Synchronous-slave receive mode. In this configuration, the SAl sub-block configured in Master mode delivers the clock to the digital microphones and to the other SAl sub-block. The two SAl sub-blocks read data synchronously from the microphones.

![](images/db725befd8bf62e629bc378d3cf56b4adc86922e0375241a373d0cb0acf74e13.jpg)  
Figure 16. Connecting two digital microphone to SAl in stereo configuration using two synchronous SAl sub-blocks

Since the two microphones are not sharing one data line, the L/R channel selection (LR) pin of the microphones can be connected either to Vdd or to GND. The microphones output data on the rising or falling edges of the incoming clock signal depending on the selected channel. The clock polarity of each SAl sub-blocks should be configured accordingly.

# Data format

The samples acquired by each SAl sub-block can be stored into the memory using either DMA or interrupt signaling. Up to 2 DMA channels are requested in that case.

For each SAl sub-block, the data format is similar to what is described for the SAl mono configuration.

# 2.2.3 Using PDM interface

The PDM interface is provided in order to support digital microphones. Up to 4 digital microphone pairs can be connected in parallel. The PDM interface also offers delay lines in order to perform micro-delays in each incoming bitstream, and thus making the beamforming application simpler. The depth of each delay cell is 8 bitstream samples.

The PDM function is intended to be used in conjunction with SAl_A sub-block, configured in Time Division Multiplexing (TDM) master mode. It cannot be used with SAl_B sub-block.

To reduce the memory footprint, the user can select the amount of microphones that the application needs. It is possible to select 2, 4, 6 or 8 microphones.

For example, if the application is using 3 microphones, the user has to select 4. In this case, the PDM data is acquired through SAI_D1 and SAI_D2. SAI_D1 receives the data from the first couple of microphones while SAl_D2 receives data from the third microphone.

Table 5 shows the recommended IO lines versus the number digital microphones to be connected.

Table 5. Recommended IO lines versus the number digital microphones to be connected   

<table><tr><td rowspan=1 colspan=1>Number ofMicrophones</td><td rowspan=1 colspan=1>Recommended data IO lines</td><td rowspan=1 colspan=1>Recommendedclock I0 lines</td></tr><tr><td rowspan=1 colspan=1>1 or 2</td><td rowspan=1 colspan=1>SAI_D1</td><td rowspan=4 colspan=1>SAI_CK1,2,3 or 4</td></tr><tr><td rowspan=1 colspan=1>3 or 4</td><td rowspan=1 colspan=1>SAI_D1 and SAI_D2</td></tr><tr><td rowspan=1 colspan=1>5 or 6</td><td rowspan=1 colspan=1>SAI_D1 and SAI_D2 and SAI_D3</td></tr><tr><td rowspan=1 colspan=1>7 pr 8</td><td rowspan=1 colspan=1>SAI_D1 and SAI_D2 and SAI_D3 and SAI_D4</td></tr></table>

The microphones can be clocked from the same SAl_CKx (x=0...3) or separately from different SAl_CK giving the user the flexibility to enable or disable the audio acquisition from particular microphones depending on the application.

The SAl operates at the number of microphones selected (2, 4, 6 or 8) times the microphone frequency to be able to read data from all the microphones in the application.

![](images/78af4541c3fb6ba00f5c5182fc81375b6877b327d047bd7dbeed1c0a7cb8a02a.jpg)  
Figure 17. PDM interface capability on interfacing up to four microphone pairs

![](images/1a85e767f3b5207a9d7ec36b4db60745e09dcef17766d15ad573e1a0c0808b60.jpg)  
Common clock for all microphones

The PDM Interface of the SAI offers an optimal connection to the digital microphone, saving as much IOs as possible. In addition the PDM interfaces can separate the data of each microphone byte-wise, avoiding the de-interleaving operation.

# Data format

The samples acquired by the SAl_A sub-block can be stored into the memory using a single DMA channel or interrupt signaling.

The receive data register (SAl_ADR) provides 8 successive bits for each microphone as shown hereafter:

![](images/fa2bb972987ab28b50f9bf0c0454cf50b8d099ae7e18b480cd954fdd686cb6c1.jpg)  
Figure 18. Data format when using the SAI PDM interface with a slot size of 32 bits, and 8 microphones

MSv48092V1

The size of data stored into the SAl_ADR depends on the programming of several SAl parameters, please refer to the SAl user specification on order to get more information about the data format, when the PDM interface is used.

Note that if the slot size is set to 8 bits, then the SAl_ADR contains only on byte of data from one microphone. The SAl_ADR must be read 8 times to get one byte from the 8 microphones.

![](images/56e9c9d9449e6487a0ddc5e509842d3395ce3b16adc86869d780a476e353c5cc.jpg)  
Figure 19. Data format when using the SAl PDM interface with a slot size of 8 bits, and 8 microphones

# 2.3 Digital filter for sigma delta modulators (DFSDM)

The DFSDM is a digital peripheral inside STM32 MCUs and MPUs. It behaves like a standard ADC with a scalable speed/resolution and an external analog front-end.

Digital MEMS microphones providing a PDM output data format can be directly connected to the DFSDM. The DFSDM provides filtered and decimated samples. Each filter has its own DMA channel as a consequence the samples of each microphone are separated. This allows the application to avoid heavy filtering and the de-interleaving operations. Finally some DFSDM blocks offer delay lines in order to perform micro-delays in each incoming bitstream, and thus making the beamforming application simpler. The depth of each delay line is at least equal to the decimation ratio.

It is possible to interface several digital microphones with a single DFSDM. It depends on the amount of filters integrated and the amount of interfaces.

The DFSDM features a clock output signal (DFSDM_CKOUT) to drive the digital microphones. The clock output has an adjustable division factor. The DFSDM_CKOUT can be the output on different IOs giving the user the flexibility to enable or disable the audio acquisition from particular microphones depending on the application. The configuration shown in Figure 20: DFSDM capability to interface up to 4 digital microphones is usually used in low power applications: the digital microphone M1 can work while the others switched in low-power mode as they are not clocked. It is also possible to power-off M3 and M4, to save more energy.

When all microphones need to be activated, then the same clock is provided to all microphones via two different PADs.

![](images/1bc367f01e112ef76503dc7b483401000bf6ecda6a55463fc7bbf6b326c926e9.jpg)  
Figure 20. DFSDM capability to interface up to 4 digital microphones

# 2.3.1 Stereo configuration

Two digital microphones are connected to the DFSDM in stereo configuration. The DFSDM must enable two consecutive channels driven by an internal clock. The DFSDM peripheral provides an external clock (DFSDM_CKOUT) to drive the digital microphones. In this configuration, the DFSDM is programmed in order to allow the channels x and x-1 to receive the data from DFSDM_DATINx pin. Each channel reads data on a different clock edge allowing the two microphones to share a single data line. Each channel then redirects the acquired data to a different DFSDM filters to be processed.

![](images/a869c190087d50956b87d0cc3a0e0f9f5cdd9013346d301ffe81b72504acaf97.jpg)  
Figure 21. Stereo configuration

MSv48095V1

# Data format

The samples acquired by each digital filter can be stored into the memory using a dedicated DMA channel or interrupt signaling. There is no interleaving, each filter provides the converted samples of one microphone. The amount of requested DMA channels is equal to the amount of the digital filters activated.

# 2.4 Clocking considerations

# 2.4.1 The digital microphone clock

The clock provided to the digital microphone has several functions:

When the clock is absent or at very low frequency (refer to product datasheet), then the digital microphones switch into low-power mode. When the clock frequency is low (usually between 400 and 800 kHz) the microphone is working in low-power mode. It means that there is a small degradation of its performance in order to reduce as much as possible the power consumption. This

feature is not available in all microphones. The clock shall be as clean as possible, with low-jitter.

Finally, when the clock frequency is higher (about 1 to 4.8 MHz), the microphone is working in its nominal mode. The clock shall be as clean as possible, with low-jitter. Note that the accepted frequency range is dependent of the microphone, refer to the datasheet of the product for details.

Note as well that when a digital microphone just exits from low-power mode because its clock becomes active or in the detected frequency range, it takes several milliseconds before providing samples with the expected quality.

Table 6 shows some applications examples and the associated microphone clock frequency.

Ta Aplatin eapnhessct hon cocfe   

<table><tr><td rowspan=1 colspan=1>Use-cases</td><td rowspan=1 colspan=1>Clock frequency provided to the digital microphone</td></tr><tr><td rowspan=1 colspan=1>Sound capture</td><td rowspan=1 colspan=1>Between 400 and 800 kHz</td></tr><tr><td rowspan=1 colspan=1>Speech application</td><td rowspan=1 colspan=1>Between 1 and 1.5 MHz</td></tr><tr><td rowspan=1 colspan=1>High-quality audio application</td><td rowspan=1 colspan=1>Between 2.4 and 4.8 MHz</td></tr></table>

# 2.4.2 The peripheral clocks

In order to select an implementation, the application shall also consider the clocking possibilities that the microcontroller offers to the SPI, SAI or DFSDM. It is also important to check the capabilities of the clock generator embedded into the SPI, SAI and DFSDM.

Generally the peripheral audio blocks have two clock inputs:

• A clock used for the register interface control (like APB clock) • A clock used for the timing generation of the serial interface, named kernel clock.

According to the peripheral and protocol selected, the peripheral clock generator uses the bus interface or a dedicated reference clock. For example the SPI-V1 uses the APB clock as reference clock if the SPI protocol is used, while the I2S protocol is using an I2S clock.

Controlling the frequency of the APB clock is generally less flexible than using a dedicated clock. One of the reason is that the APB clock impacts althe peripherals connected to this APB bus. However, in the case where a timer is used to support a stereo microphone configuration, using the APB (like the same clock than the timer) solves one of the issue listed in the Using the timer as clock generator.

Some microcontrollers also offer the possibility to provide a copy of the APB clock as kernel clock.

![](images/2f3158b2ab63e5b385f3522eada4c5b9ceb4beefff93b44d9ddae99e9c6ba1e6.jpg)  
Figure 22. Bus and kernel clock topology for SPI

Other peripherals (SPI-V2, SAI and DFSDM) always offer a dedicated kernel clock for the clock generation. This option is more flexible and makes the wanted clock frequency independent from the bus interface frequency.

![](images/1f8d6c19c4fa523811ce9f609dcf3da5e22ac466a85e4441831e5ffb3fdc1906.jpg)  
Figure 23. Bus and kernel clock topology for SAI and DFSDM

The DFSDM offers the possibility to select either an independent peripheral clock (audio clock) or to select the DFSDM clock which is synchronous of the APB clock.

# 2.5 GPIOs number considerations

This section helps the user to choose the most suited STM32 peripheral (SPI2S, SAI, DFSDM) to interface digital microphones in a particular application according to GPIOs number.

Table 7, Table 8 and Table 9 shows the hardware used to connect respectively one, two and four digital microphones to the different audio and serial interfaces.

The column Number of GPIOs indicates the number of GPIO necessary to connect digital microphones to an audio interface.   
The column Timer indicates whether the audio interface needs a timer to deliver the appropriate clock to the microphones.

Table 7. Hardware used to connect one digital microphone   

<table><tr><td rowspan=1 colspan=1>Interface</td><td rowspan=1 colspan=1>Number of GPIOs</td><td rowspan=1 colspan=1>Timer</td></tr><tr><td rowspan=1 colspan=1>SPI</td><td rowspan=1 colspan=1>2</td><td rowspan=1 colspan=1>No</td></tr><tr><td rowspan=1 colspan=1>I2S</td><td rowspan=1 colspan=1>2</td><td rowspan=1 colspan=1>No</td></tr><tr><td rowspan=1 colspan=1>SAI</td><td rowspan=1 colspan=1>2</td><td rowspan=1 colspan=1>No</td></tr><tr><td rowspan=1 colspan=1>DFSDM</td><td rowspan=1 colspan=1>2</td><td rowspan=1 colspan=1>No</td></tr></table>

Table 8. Hardware used to connect two digital microphones   

<table><tr><td rowspan=1 colspan=1>Interface</td><td rowspan=1 colspan=1>Number of GPIOs</td><td rowspan=1 colspan=1>Timer</td></tr><tr><td rowspan=1 colspan=1>SPI</td><td rowspan=1 colspan=1>4</td><td rowspan=1 colspan=1>Yes</td></tr><tr><td rowspan=1 colspan=1>I2S</td><td rowspan=1 colspan=1>4</td><td rowspan=1 colspan=1>Yes</td></tr><tr><td rowspan=1 colspan=1>SAI</td><td rowspan=1 colspan=1>4</td><td rowspan=1 colspan=1>Yes</td></tr><tr><td rowspan=1 colspan=1>SAI (two synchronous sub-blocks)</td><td rowspan=1 colspan=1>4</td><td rowspan=1 colspan=1>No</td></tr><tr><td rowspan=1 colspan=1>SAI with PDM interface</td><td rowspan=1 colspan=1>2</td><td rowspan=1 colspan=1>No</td></tr><tr><td rowspan=1 colspan=1>DFSDM</td><td rowspan=1 colspan=1>2</td><td rowspan=1 colspan=1>No</td></tr></table>

Table 9. Hardware used to connect four digital microphones   

<table><tr><td rowspan=1 colspan=1>Interface</td><td rowspan=1 colspan=1>Number of GPIOs</td><td rowspan=1 colspan=1>Timer</td></tr><tr><td rowspan=1 colspan=1>SAI (two synchronous sub-blocks)</td><td rowspan=1 colspan=1>6</td><td rowspan=1 colspan=1>Yes</td></tr><tr><td rowspan=1 colspan=1>SAI with PDM interface</td><td rowspan=1 colspan=1>3</td><td rowspan=1 colspan=1>No</td></tr><tr><td rowspan=1 colspan=1>DFSDM</td><td rowspan=1 colspan=1>3</td><td rowspan=1 colspan=1>No</td></tr></table>

# 3 Digital signal processing

This section presents two ways to convert PDM data into PCM data: the first is a software solution which is the PDM audio software decoding library and the second is hardware solution using the DFSDM peripheral filters.

# 3.1 PDM audio software decoding library

# 3.1.1 Overview

PDM audio software decoding library is an optimized software implementation for PDM signal decoding and audio signal reconstruction when connecting digital MEMS microphones with an STM32 MCU or MPU. This library implements several filters for the 1- bit PDM high frequency signal output from a digital microphone and transforms it into a 16- bit PCM at a proper audio frequency.

# 3.1.2 Digital data flow

The digital MEMS microphone outputs a PDM signal, which is a high frequency (1 to 3.25 MHz) stream of 1-bit digital samples. The PDM data is acquired by a serial interface embedded in the STM32 device. This data is transferred through DMA (thus reducing the software overhead) to a system RAM buffer to be processed. After the conversion, the PCM raw data can be handled depending on the application implementation (stored as wave/compressed data in a mass storage media, transferred to an external audio codec DAC).

![](images/d53053fa22d22512f55393b0270a7b3b243ea509cfb409fa09aedc596a15a2c1.jpg)  
Figure 24. Digital data acquisition and processing (block diagram)

MS47169V1

# 3.1.3 Digital signal processing

The PDM audio software decoding library offers a two steps digital signal processing: PDM digital filtering and decimation and digital signal conditioning.

![](images/0a1735f16b4aa8726301da48da63614e41a15231995830fec549feccaad72c22.jpg)  
Figure 25. Digital signal processing

On the first step, the PDM signal from the microphone is filtered and decimated in order to obtain a sound signal at the required frequency and resolution.

On the second step, the digital audio signal resulting from the previous filter pipeline is further processed for proper signal conditioning implementing a low pass filter and a high pass filter. Both these filters can be enabled/disabled and configured (cut-off frequencies) by using the filter initialization function.

# Note:

In stereo configuration, if two microphones are sharing one data line and the PDM data is interleaved bit per bit, a software de-interleaving step is needed to separate the signal from the two microphones before proceeding to the PDM to PCM conversion.

# DFSDM filters for digital signal processing

# 3.2.1 Digital data flow: acquisition and processing

The digital MEMS microphone outputs a PDM signal, which is a high frequency (1 to 3.25 MHz) stream of 1-bit digital samples. The data is acquired by the DFSDM serial transceiver that provides connection to the external Sigma-Delta modulator of the digital microphone. The digital filters perform CPU-free filtering that averages the 1-bit input data stream from the SD modulator into a higher resolution and a lower sample rate. This data is transferred through DMA (thus reducing the software overhead) to a system RAM buffer to be further filtered. After that, the PCM raw data can be handled depending on the application implementation (stored as wave/compressed data in a mass storage media, transferred to an external audio codec DAC).

![](images/3f9475db42f41882f2602800712f7409ee5dacad680f4478f34f1390c5500cbd.jpg)  
Figure 26. Digital data acquisition and processing using DFSDM (block diagram)

# Examples of configuration based on STM32CubeMX

The following section guides the user through the different steps needed to create a basic audio application which acquires PDM data from digital microphones in mono or stereo modes then convert it into PCM data.

The main step consists in selecting the right hardware configuration and generate the C initialization code with the STM32CubeMX tool. In a second step, add the appropriate user code to the generated project.

Finally, user could refer to STM32Cube_FW packages audio examples and to "X-CUBE-MEMSMIC1" package to complete the needed user code for each example.

This section assumes that:

The user wanted to get a PCM stream of 16 or 48 kHz   
The digital microphones receive a clock 64 times higher than the PCM stream frequency (oversampling by 64).

4.1

# Example 1: Interfacing digital microphones in mono or stereo mode with I2S, SPI or a single SAl sub-block

This example is based on the NUCLEO-F413ZH board and using external digital microphones that are connected to either I2S, SPI or SAI.

For 16 KHz sampling rate the bitclock generated by the interface must be 1.024 MHz for mono mode and 2.048MHz for stereo mode.

For 48 KHz sampling rate the bitclock generated by the interface must be 3.072 MHz for mono mode and 6.144MHz for stereo mode.

# 4.1.1 Hardware configuration using STM32CubeMX

I2S

# GPIO and Pin configuration

From the listed hardware in the Pinout tab, choose the I2S2 peripheral and configure it in Half-duplex master mode.

Figure 27 shows how to enable the I2S2 in Half-duplex master mode.

The enabled pins, I2S2_SD, I2S2_CK and I2S2_WS, are highlighted in green once the I2S peripheral GPIOs are correctly configured.

![](images/040afefa93c6551309f900922fdf7315792c70b7d2947a7a19b7249c36dd8e81.jpg)  
Figure 27. I2S GPIO pin configuration

Note:

In this example the I2S2_WS pin are not used. This pin can be released and brought back as a GPIO by applying a minor modification in code of the MSP Initialization file (stm32f4xx_hal_msp.c) after generating the project.

# Clock configuration:

This section describes the different clock configuration for I2S in mono and stereo modes for 16 kHz and 48 kHz streams. HSE = 8 MHz is used as source clock.

In stereo mode, timer and I2S must use a clock coming from the same reference, for this reason the PLLR selected as clock source for I2S.

Note:

The accuracy is the error between expected audio frequency and the real one.

Table 10. I2S2 clock configuration and accuracy   
Figure 28 shows an example of I2S clock configuration for mono mode.   

<table><tr><td rowspan=1 colspan=1>TargetAudioFrequency(kHz)</td><td rowspan=1 colspan=1>Microphonemode</td><td rowspan=1 colspan=1>I2S_APB1ClockMuxsource</td><td rowspan=1 colspan=1>DivM</td><td rowspan=1 colspan=1>PLLN</td><td rowspan=1 colspan=1>DivR</td><td rowspan=1 colspan=1>DivP</td><td rowspan=1 colspan=1>I2S clock(MHz(1)</td><td rowspan=1 colspan=1>Accuracy(ppm)</td></tr><tr><td rowspan=3 colspan=1>16</td><td rowspan=2 colspan=1>Mono</td><td rowspan=1 colspan=1>PLLI2SR</td><td rowspan=1 colspan=1>5</td><td rowspan=1 colspan=1>192</td><td rowspan=1 colspan=1>2</td><td rowspan=1 colspan=1>-</td><td rowspan=1 colspan=1>153.60</td><td rowspan=1 colspan=1>0</td></tr><tr><td rowspan=1 colspan=1>PLLI2SR</td><td rowspan=1 colspan=1>5</td><td rowspan=1 colspan=1>192</td><td rowspan=1 colspan=1>5</td><td rowspan=1 colspan=1>-</td><td rowspan=1 colspan=1>61.44</td><td rowspan=1 colspan=1>0</td></tr><tr><td rowspan=1 colspan=1>Stereo(with timer)</td><td rowspan=1 colspan=1>PLLR</td><td rowspan=1 colspan=1>7</td><td rowspan=1 colspan=1>344</td><td rowspan=1 colspan=1>6</td><td rowspan=1 colspan=1>4</td><td rowspan=1 colspan=1>65.52</td><td rowspan=1 colspan=1>-186</td></tr><tr><td rowspan=3 colspan=1>48</td><td rowspan=2 colspan=1>Mono</td><td rowspan=1 colspan=1>PLLI2SR</td><td rowspan=1 colspan=1>5</td><td rowspan=1 colspan=1>192</td><td rowspan=1 colspan=1>2</td><td rowspan=1 colspan=1>-</td><td rowspan=1 colspan=1>153.60</td><td rowspan=1 colspan=1>0</td></tr><tr><td rowspan=1 colspan=1>PLLI2SR</td><td rowspan=1 colspan=1>5</td><td rowspan=1 colspan=1>192</td><td rowspan=1 colspan=1>5</td><td rowspan=1 colspan=1>-</td><td rowspan=1 colspan=1>61.44</td><td rowspan=1 colspan=1>0</td></tr><tr><td rowspan=1 colspan=1>Stereo(with timer)</td><td rowspan=1 colspan=1>PLLR</td><td rowspan=1 colspan=1>7</td><td rowspan=1 colspan=1>344</td><td rowspan=1 colspan=1>4</td><td rowspan=1 colspan=1>4</td><td rowspan=1 colspan=1>98.29</td><td rowspan=1 colspan=1>-186</td></tr></table>

In order to work properly, the I2S clock must be higher than its APB clock.

![](images/13a569ba2e72d7f3ee8222cdee84d843ddf2ea81c5723150d55dadf9571d7710.jpg)  
Figure 28. I2S2 clock configuration

# I2S configuration

Select the configuration tab then click on the I2S2 button as shown in Figure 29.

![](images/4369a226ddc01dd0a68f5aaffb672f8a1ea28a81614b64207c5d980198cf4b9c.jpg)  
Figure 29. I2S configuration

# a) I2S parameter settings:

In the I2S configuration window, select the parameter settings tab and then configure the parameters.

The I2S is configured according to the following conditions:

Selected Audio Frequency = AUDIO_SAMPLING_FREQUENCY Communication Standard = MSB First (Left Justified): The I2S reads data on the falling edge of the clock. In mono configuration the LR pin of the microphone must be connected to GND.

Figure 30 shows an example of I2S configuration for an Audio Sampling Frequency = 16 kHz in Mono mode.

![](images/aa78939fa8381370349ea302a6f6cd2c3d5c03fe36dc3efe867baacb6e2d0958.jpg)  
Figure 30. I2S parameter settings

# I2S DMA configuration

In this example the DMA handles the PDM data transfer from the I2S to the Memory.

In the I2S configuration window, select the DMA Settings Tab and add a DMA request.   
Figure 31 shows how to enable the DMA.

![](images/883dc9dd20b81035be7f0a68d5ecfa540b78b2744058559d8b00484388a33322.jpg)  
Figure 31. I2S DMA settings

Click on the recently created DMA request and refer to the DMA request settings section to complete the DMA configuration.

SPI

# GPIO and pin configuration

From the listed hardware in the Pinout tab, choose the SPl1 peripheral and configure it in Receive Only Master mode.

Figure 32 shows how to enable SPl1 in Receive Only Master mode. The enabled pins, SPI1_SCK and SPI1_MISO, are highlighted in green when the SPI peripheral GPIOs are correctly configured.

![](images/37ca4669ec32a1d2943813a40b5fdea3ef06487602819e8e9954d5b4c111029e.jpg)  
Figure 32. SPI GPIO and pin configuration

# SPI clock configuration

This section describes the different clock configuration for SPl in mono and stereo modes for 16 KHz and 48 KHz streams. HSE = 8MHz is used as source clock.

The APB2 clock is used as reference clock for the SPI.

Table 11. SPI clock configuration and accuracy   

<table><tr><td rowspan=1 colspan=1>TargetAudioFrequency(kHz)</td><td rowspan=1 colspan=1>Microphonemode</td><td rowspan=1 colspan=1>DivM</td><td rowspan=1 colspan=1>PLLN</td><td rowspan=1 colspan=1>DivR</td><td rowspan=1 colspan=1>DivP</td><td rowspan=1 colspan=1>SPI clock(MHz)</td><td rowspan=1 colspan=1>Accuracy(ppm)</td></tr><tr><td rowspan=2 colspan=1>16</td><td rowspan=1 colspan=1>Mono</td><td rowspan=1 colspan=1>7</td><td rowspan=1 colspan=1>344</td><td rowspan=1 colspan=1></td><td rowspan=1 colspan=1>6</td><td rowspan=1 colspan=1>65.52</td><td rowspan=1 colspan=1>-186</td></tr><tr><td rowspan=1 colspan=1>Stereo(with timer)</td><td rowspan=1 colspan=1>7</td><td rowspan=1 colspan=1>344</td><td rowspan=1 colspan=1></td><td rowspan=1 colspan=1>6</td><td rowspan=1 colspan=1>65.52</td><td rowspan=1 colspan=1>-186</td></tr><tr><td rowspan=2 colspan=1>48</td><td rowspan=1 colspan=1>Mono</td><td rowspan=1 colspan=1>7</td><td rowspan=1 colspan=1>344</td><td rowspan=1 colspan=1></td><td rowspan=1 colspan=1>4</td><td rowspan=1 colspan=1>98.29</td><td rowspan=1 colspan=1>-186</td></tr><tr><td rowspan=1 colspan=1>Stereo(with timer)</td><td rowspan=1 colspan=1>7</td><td rowspan=1 colspan=1>344</td><td rowspan=1 colspan=1></td><td rowspan=1 colspan=1>4</td><td rowspan=1 colspan=1>98.29</td><td rowspan=1 colspan=1>-186</td></tr></table>

![](images/cdd11a176fc5c9ed9d307b77f4f8181333b5e37ee3aeb2aae60e5547a607bb3f.jpg)  
Figure 33 shows an example of SPI clock configuration for mono mode.   
Figure 33. SPI clock configuration

# SPI configuration

Select the configuration tab then click on the SPI button as shown in Figure 34.

![](images/b9dd3816f465dd6eba78e0a0810f3cac0224ae2829e7bc6660d639a774edfd6e.jpg)  
Figure 34. SPI configuration

# a) SPI parameter settings

In the SPI configuration window, select the parameter Settings and tab then configure the parameters.

In mono mode the Clock Polarity and the Clock Phase are chosen according to the state of L/R pin of the microphone

Figure 35 shows an example of SPI configuration with an Audio Frequency = 16 kHz in Mono mode.

![](images/266ebd47d873ae6b8615129489c843320ae9792b3e6ccd001375d214430ad7ca.jpg)  
Figure 35. SPI parameter setting

# SPI DMA settings

In this example the DMA handles the PDM data transfer from the SPI to the Memory.

Open the SPI configuration window, select the DMA Settings Tab and add a DMA request.   
Figure 36 shows how to enable the DMA.

![](images/a28cf371fb1ca499c56d52f13035be4b6a12fee862bb56e7e4721699d8ff3899.jpg)  
Figure 36. SPI DMA settings

Click on the DMA request and refer to the DMA request settings section to complete the DMA configuration.

# SAI

# GPIO and pin configuration

From the listed hardware in the Pinout tab, choose the SAl1 peripheral and enable its subblock A in Master mode.

Figure 37 shows how to enable the sub-block A of the SAl in Master mode. The enabled pins, SAI1_SD_A, SAI1_SCK_A and SAI1_FS_A, is highlighted in green once the SAI interface GPIOs are correctly configured.

![](images/5771c21d0bc5454556040ed19040249fbdf5ea28e9b46ffd58b39f4f274ef352.jpg)  
Figure 37. SAI GPIO and pin configuration

# Note:

In this example the SAl1FS_A pin cannot be used. This pin can be released and brought back as a GPIO by applying a minor modification in the MSP Initialization file code (stm32f4xx_hal_msp.c), after generating the project.

# Clock configuration

In the Clock Configuration tab set the SAl clock.

Table 12 provides the audio sampling frequency accuracy values for the clock configuration.

The PLLI2SR is used as source clock.

Table 1. Clock configuration and accuracy   
Figure 38 shows an example of SAI clock configuration.   

<table><tr><td rowspan=1 colspan=1>Target AudioFrequency(kHz)</td><td rowspan=1 colspan=1>Microphonemode</td><td rowspan=1 colspan=1>DivM</td><td rowspan=1 colspan=1>PLLN</td><td rowspan=1 colspan=1>DivR</td><td rowspan=1 colspan=1>SAI clock(MHz)</td><td rowspan=1 colspan=1>Accuracy(ppm)</td></tr><tr><td rowspan=2 colspan=1>16</td><td rowspan=1 colspan=1>Mono</td><td rowspan=1 colspan=1>5</td><td rowspan=1 colspan=1>128</td><td rowspan=1 colspan=1>5</td><td rowspan=1 colspan=1>40.96</td><td rowspan=1 colspan=1>0</td></tr><tr><td rowspan=1 colspan=1>Stereo(with timer)</td><td rowspan=1 colspan=1>5</td><td rowspan=1 colspan=1>128</td><td rowspan=1 colspan=1>5</td><td rowspan=1 colspan=1>40.96</td><td rowspan=1 colspan=1>0</td></tr><tr><td rowspan=2 colspan=1>48</td><td rowspan=1 colspan=1>Mono</td><td rowspan=1 colspan=1>5</td><td rowspan=1 colspan=1>192</td><td rowspan=1 colspan=1>25</td><td rowspan=1 colspan=1>12.29</td><td rowspan=1 colspan=1>0</td></tr><tr><td rowspan=1 colspan=1>Stereo(with timer)</td><td rowspan=1 colspan=1>5</td><td rowspan=1 colspan=1>192</td><td rowspan=1 colspan=1>25</td><td rowspan=1 colspan=1>12.29</td><td rowspan=1 colspan=1>0</td></tr></table>

![](images/256f1d2f0c5d83fe51f45d58414d1a682817f0ddf17be9574fffd421a63ea1b8.jpg)  
Figure 38. SAI clock configuration at 16 kHz for mono mode

# SAI configuration

Select the Configuration tab then click on the SAl1 button as shown in Figure 39.

![](images/c69cd71c912bf7ab0c12c6c45e17055d137a267595c8b2f47e75bb0b0bfc0666.jpg)  
Figure 39. SAI configuration

# a) SAl parameter settings

In the SAl configuration window, select the parameter Settings tab and then configure the parameters. The enabled SAl sub-block is configured according to the following conditions:

• Data Size = 16 Bits Output Mode = Stereo (This parameter doesn't change whether one or two microphones are connected to SAl)   
• Companding Mode = No companding mode   
• Frame Synchro definition = Channel Identification Number of Slots = 4   
• Slot Active = All   
• Frame Synchro Active Length = Frame Length / 2   
• Master Clock Divider = Enabled (other possible solution with Master Clock Divider disabled   
• Audio Frequency = Audio Sampling Frequency In mono mode the Clock Strobing is chosen according to the state of L/R pin of the microphone.

Figure 40 shows an example of SAl configuration for an Audio Frequency = 16 kHz in Mono mode.

![](images/c0ad09543312d78b561cf3bb992cf2cf5deb1465019b8e80242362bf91b233aa.jpg)  
Figure 40. SAI parameter setting

# SAI DMA settings

In this example the DMA handles the PDM data transfer from the SAI to the Memory.   
In the SAI configuration window, select the DMA Settings Tab and add a DMA request.   
Figure 41 shows how to enable the DMA.

![](images/67bc721e1cd8eb2828636c1a4f48c6e3a756ca62f62a5b50dfaf2c515d89df02.jpg)  
Figure 41. SAI DMA settings

Click on the recently created DMA request and refer to the DMA request settings section to complete the DMA configuration.

# DMA request settings

Figure 39 shows the DMA configuration request for each audio interface.

![](images/3f740375bb1ba7284ac2239a35fcd499f3e3e27eeaed618452641b88af1f5ab1.jpg)  
Figure 42. DMA request settings

# Timer

In stereo mode, a timer is used to divide the clock frequency generated by the audio interface and deliver the divided clock to the digital microphones.

# GPIO and pin configuration

In the Pinout tab, choose Timer 3 from the listed hardware and enable the slave mode by selecting External Clock Mode 1. Select TI1FP1 as a Trigger Source and enable Channel 2 in PWM Generation CH2.

Figure 39 shows how to enable TIM3. The used pins, TIM3_CH1 and TIM3_CH2, is highlighted in green once the TIM3 GPIOs are correctly configured.

![](images/7d94bc5de411438a0386a658f2b69d108870383c7cd4f8d0b5947ee9d8f72531.jpg)  
Figure 43. TIM GPIO and pin configuration

# Timer configuration

Select the Configuration tab then click on the TIM3 button as shown in Figure 44.

![](images/e3656d0990503ccc64fc0dd33c8b4538633f1cb435ad8d8cbf086d21fa4a1ab7.jpg)  
Figure 44. TIM configuration

# TIM parameter settings

In the TIM3 configuration window, select the Parameter Settings tab.

Figure 44 shows how to configure TIM3 in order to divide the Trigger Source clock frequency by 2.

![](images/9a0517f10b84cdba38b2fe4033ea12fe7d8ef1d4ace4547955830c74a16b7dac.jpg)  
Figure 45. TIM parameter settings

# 1.1.2 Adding PDM software decoding library middleware files

Choose the favorite toolchain, generate the project with STM32CubeMX and open the generated project.

For the STM32F413xx MCU, the PDM audio software decoding library includes one header file pdm_filter.h and binary/object codes for the following platforms:

• libPDMFilter_CM4F_IAR.a: for IAR compiler • libPDMFilter_CM4F _Keil.lib: for ARM compiler • libPDMFilter_CM4F _GCC.a: for GNU compiler

This Library is provided in the "STM32Cube_FW_F4" firmware package (V1.16 and later) under the following path "MiddlewaresISTISTM32_Audio\Addons\PDM"

Make sure to add header file pdm_filter.h path to the project Include Paths and the appropriate binary/object file to the project source files.

# Example 2: Interfacing digital microphones in stereo mode with SAl using two synchronous sub-blocks

This example is based on the NUCLEO-F413ZH board and using two external digital microphones that are connected each one to an SAl sub-block. It is applicable to the hardware connection described in the Section 2.2.2: Using two synchronous SAI sub-blocks

# 4.2.1 SAI configuration using STM32CubeMX

# GPIO and Pin configuration

After creating the STM32CubeMX project, choose the SAI1 peripherals from the listed hardware in the Pinout tab, configure its sub-block A in Master mode and the sub-block B in Synchronous Slave mode.

Figure 46 shows how to enable the sub-block A of SAl1 in Master mode and the sub-block B in Synchronous Slave mode. In this case, the bit clock and the frame synchronization signals are shared between the two sub-blocks to reduce the number of external pins used for the communication.

The enabled pins, SAI1_SD_A, SAI1_SD_B, SAI1_SCK_A and SAI1_FS_A, are highlighted in green once the SAl peripheral GPIOs are correctly configured.

![](images/766357ed981190bafa8b388ebd456647d4acb4de6214aa316d2c8be83fbf97df.jpg)  
Figure 46. SAI GPIO and pin configuration

# Clock configuration using STM32CubeMx

This section describes the clock configuration for SAl using two synchronous sub-blocks for 16 KHz and 48 KHz streams.

For 16KHz sampling rate the bitclock generated by SAl should be 1.024MHz .

For 48KHz sampling rate the bitclock generated by SAI should be 3.072MHz .

The PLLI2SR is used as source clock.To get the accurate bitclock frequency, the user must configure the adequate MCKIDV.

Table 13. SAI clock configuration and accuracy   

<table><tr><td rowspan=1 colspan=1>TargetAudio Freq(kHz)</td><td rowspan=1 colspan=1>DivM</td><td rowspan=1 colspan=1>PLLN</td><td rowspan=1 colspan=1>DivR</td><td rowspan=1 colspan=1>SAI clock(MHz)</td><td rowspan=1 colspan=1>Accuracy(ppm)</td></tr><tr><td rowspan=1 colspan=1>16</td><td rowspan=1 colspan=1>5</td><td rowspan=1 colspan=1>128</td><td rowspan=1 colspan=1>5</td><td rowspan=1 colspan=1>40.96</td><td rowspan=1 colspan=1>0</td></tr><tr><td rowspan=1 colspan=1>48</td><td rowspan=1 colspan=1>5</td><td rowspan=1 colspan=1>192</td><td rowspan=1 colspan=1>25</td><td rowspan=1 colspan=1>12.29</td><td rowspan=1 colspan=1>0</td></tr></table>

Figure 47 provides the SAl clock configuration used in this example.

![](images/13f082c46d38e4674261acbefd47e4585488c73d08f928fe357f39738c1d3bb1.jpg)  
Figure 47. SAI clock configuration

# Parameter settings

In the SAl configuration window, select the parameter Settings tab then configure the parameters. The SAl sub-blocks should be configured according to the following conditions:

• Data Size = 16 Bits   
• Frame Length = 4 x Data Size   
• Output Mode = Stereo   
• Companding Mode = No companding mode   
• Frame Synchro definition = Channel Identification   
• Number of Slots = 4   
• Slot Active = All   
• Frame Synchro Active Length = Frame Length / 2   
• Master Clock Divider = Enabled Audio Frequency = AUDIO_SAMPLING_FREQUENCY

The Clock Strobing is chosen according to the state of L/R pin of the microphone connected to every sub-block.

Figure 48 and Figure 49 show respectively how to configure SAIA and SAIB for an audio sampling frequency = 16 kHz.

![](images/7fa4f87b72af1808cae5c33d8d9992e1aa35faed6ee22dd4c558f7dc53c45043.jpg)  
Figure 48. SAI parameter settings

![](images/519ed4fdaf4b8891992541a276cbdf71611b36e6a7d3e4b66862246409acffc1.jpg)  
Figure 49. SAIB parameter settings

# SAI DMA settings

In this example the DMA handles the PDM data transfer from each SAI sub-block to the Memory.

In the SAI configuration window, select the DMA Settings Tab and add a DMA request for each sub-block. Figure 50 shows how to enable the DMA.

![](images/a922dd299e727fb745c87c67cacee6fa6e229948d36fad8dc596a33333ebf3e6.jpg)  
Figure 50. SAI DMA settings

Click on the recently created DMA requests and refer to the DMA request settings section to complete the DMA configuration.

# 4.2.2 Adding PDM software decoding library middleware files

Refer to Section 4.1.2: Adding PDM software decoding library middleware files.

# 4.3

# Example 3: Interfacing digital microphones in stereo mode with SAI using PDM interface

This example is based on the NUCLEO-H743ZI board using two external digital microphones that are connected in Stereo mode to SAI through the PDM interface.

# 4.3.1

# SAI configuration using STM32CubeMX

# GPIO and Pin configuration

After creating the STM32CubeMX project, choose the SAI1 peripherals from the listed hardware in the Pinout tab and configure it in Pulse Density Modulation mode. Select the number of microphones as well as the output clock.

Figure 51 shows how to enable the sub-block A of SAl1 in Pulse Density Modulation mode, supporting of two microphones and having CK1 as an output clock. The enabled pins, SAI1_CK1 and SAI1_D1, are highlighted in green once the SAI peripheral GPIOs are correctly configured.

![](images/299b6ff9ec2860ec02d668c1879d467450c13609c1e8d4d6f8902a1f7b20136e.jpg)  
Figure 51. SAI GPIO and pin configuration

# Clock configuration

Figure 52 provides the SAl clock configuration used in this example.

For more details about clock configuration, refer to "Allowed TDM frame configuration" table in reference manual RM0433.

![](images/7523aeafad1c3f7a9ec63297796912b2a40aca34e42258a247148ae24abfa003.jpg)  
Figure 52. SAl clock configuration for 2 microphones at 16 kHz

# SAI configuration

Select the configuration tab then click on the SAl1 button as shown in Figure 53.

![](images/85857388aaa2fbfc152a44ad5ffb78770c192d11e3fd66b775ad9abd11dcf737.jpg)  
Figure 53. SAI configuration

# Parameter settings

In the SAl configuration window, select the parameter settings tab and then configure the parameters. The SAl sub-block A should be configured according to the following conditions:

• Data Size = 16 Bits   
• Frame Length = 16   
• Output Mode = Stereo   
• Companding Mode = No companding mode   
• Frame Synchro definition = Start Frame   
• Number of Slots = 1   
• Slot Active = All   
• Frame Synchro Active Length = 1   
• Frame Synchro Polarity = Active High Master Clock Divider = Disabled

![](images/d60db0d9ed5cd233b14fc4090f339bd81703fa169afd4765724ce989a6de2c9e.jpg)  
Figure 54 shows how to configure SAIA for an audio sampling frequency= 16 kHz.   
Figure 54. SAI parameter settings

# DMA Settings

In this example the DMA handles the PDM data transfer from the SAI to the Memory.

In the SAI configuration window, select the DMA Settings Tab and add a DMA request.   
Figure 55 shows how to configure the DMA.

![](images/05178039105af1b3cefffabaa03f18e088f38ae2717793cc7753e77a43259dcb.jpg)  
Figure 55. SAI DMA settings

# Cortex_M7 configuration

Select the configuration tab then click on the CORTEX_M7 button as shown in Figure 56.

![](images/e2dc56eb4fdd20f4faf751a807863d06defb0b8ef7ffeb4f869195cf9e2f6033.jpg)  
Figure 56. CORTEX_M7 configuration

# Parameter settings

In the CORTEX_M7 configuration window, select the parameter settings tab to configure the Cache and the memory protection unit. This allows to enhance the performance in case of use of AXI interface with several masters.

Refer to the Template project in the STM32Cube_FW_H7_V1.0.0 firmware package (V1.0.0 and later) under the following path "Projects|STM32H743ZI-NucleolTemplates" for a typical MPU configuration.

For more details about the memory protection unit configuration and use, refer to AN4838.

Figure 57 shows how to configure the Cache and the memory protection unit for this example.

![](images/c0e7ba92e502fd65df5fd5c47980a55a432b1242443eb52a546b6a128cc335f4.jpg)  
Figure 57. Cortex M7 parameter settings

# 1.3.2 Adding PDM software decoding library middleware files

Choose your favorite toolchain, generate the project with STM32CubeMX and open the generated project.

For the STM32H7 Series, the PDM audio software decoding library includes one header file "pdm2pcm_glo.h" and binary/object codes for the following platforms:

libPDMFilter_CM7_IAR.a: for IAR compiler • libPDMFilter_CM7_Keil.lib: for ARM compiler libPDMFilter_CM7_GCC.a: for GNU compiler

This Library is provided in the "STM32Cube_FW_H7" firmware package (V1.0.0 and later) under the following path "Middlewares|STISTM32_Audio\Addons|PDMI"

Make sure to add header file pdm2pcm_glo.h path to the project Include Paths and the appropriate binary/object file to the project source files.

# 4.4 Example 4: Interfacing digital microphones using DFSDM

This example is based on the NUCLEO-F413ZH board using external digital microphones that are connected to DFSDM in stereo mode. It is applicable to the hardware connection described in the Section 2.3: Digital filter for sigma delta modulators (DFSDM).

# 4.4.1 DFSDM configuration using STM32CubeMX

# GPIO and pin configuration

After creating the STM32CubeMX project, choose the DFSDM1 peripheral from the listed hardware in the Pinout tab and enable the needed DFSDM channels as shown in figures below.

Figure 58 shows how to enable DFSDM channels in stereo mode. In this mode the enabled channels must be successive.

![](images/7c23481bbcadbcae4dc2850b11cf3729b1047aab875cd7a028594a4477e68ea5.jpg)  
Figure 58. DFSDM GPIO configuration in stereo mode

The used pins, DFSDM1_DATIN1 and DFSDM1_CKOUT, are highlighted in green once the DFSDM peripheral GPIOs are correctly configured as shown in Figure 59.

![](images/6ddb3d90faecef70e96af529ab40475a5e4064c0b35621978c64cf2d825b5c4f.jpg)  
Figure 59. DFSDM pin configuration

# Channel configuration

In the DFSDM configuration window, select the parameter settings tab then configure the parameters.

The value of the field Type is chosen according to the state of L/R pin of the microphones connected DFSDM channels. In stereo mode each channel must read data on a different clock edge to allow the microphones to share one data line.

Figure 60 and Figure 61 show how to configure respectively Channel 1 and Channel 0 for an Audio Frequency = 16 kHz.

![](images/d7eac97fc82493ec3b4ba902eaee04173061f6a7849f4aa5001db078de8254e8.jpg)  
Figure 60. DFSDM Channel 1 configuration

![](images/47c8b7f05efa62f31c3a9bdeb3ab06d1b664042d5da4cb23d84708aa8dd170f7.jpg)  
Figure 61. DFSDM Channel 0 configuration

# Filter configuration

In this example, Filter 0 and Filter 1 are linked respectively to Channel 1 and Channel 0 as regular channels.

The Sinc Order is configured according to the audio sampling frequency. Table 11 shows its possible values.

Table 14. DFSDFM filter order values   

<table><tr><td rowspan=1 colspan=1>Audio Sampling Frequency (kHz)</td><td rowspan=1 colspan=1>Filter order</td></tr><tr><td rowspan=1 colspan=1>16</td><td rowspan=1 colspan=1>Sinc 4 or Sinc 5 filter type</td></tr><tr><td rowspan=1 colspan=1>48</td><td rowspan=1 colspan=1>Sinc 4 or Sinc 5 filter type</td></tr></table>

The field Fosr contains the value of the decimation factor.

Figure 62 and Figure 63 show a configuration example of Filter 1 and Filter 0 for an Audio Sampling Frequency = 16 kHz.

![](images/b1791a7032af6bb04be8af512c4946df67144e6632ef8e3196bf41f80554db39.jpg)  
Figure 62. DFSDM Filter 0 configuration

![](images/5a2115e6409e50c6a83368213c3f3a5b87eee945989ed55597726e2825894dac.jpg)  
Figure 63. DFSDM Filter 1 configuration

# Output Clock configuration

In this example, Audio Clock is selected as a source for DFSDM output clock which gives the user more flexibility when configuring the clock.

The clock divider value must respect the following formula:

Divider = DFSDM Clock Source / (AUDIO_SAMPLING_FREQUENCY × DECIAMTION_FACTOR)

Figure 64 shows a configuration example of a DFSDM Clock Source = 48 MHz, an Audio Sampling Frequency = 16 kHz and a Decimation Factor = 64.

![](images/9e574790d761f56637fa8ff48d704a1353d08398eedbc77063e5763f3be3c689.jpg)  
Figure 64. DFSDM output clock configuration

# DFSDM DMA Settings

In this example the data transfer from DFSDM channels to the memory are handled by the DMA thus reducing the software overhead.

In the DFSDM configuration window, select the DMA Settings Tab and add a DMA request for each Filter.

Click on the recently created DMA requests and configure the settings as shown in Figure 65.

![](images/82a85849c22fc04fe9e42cdeb169878b1e39ced5c034b2ca5cd7cb732ac8c570.jpg)  
Figure 65. DFSDM DMA setting

# DFSDM clock configuration

In this example, the DFSDM output clock is derived from audio clock delivering a 61.44 MHz clock to DFSDM as shown in Figure 66.

![](images/f1dd800c5b004c37da940ed103b807a6aae8ec5605be03d43172c64fe72ab58a.jpg)  
Figure 66. DFSDM clock configuration

Table 15 provides audio sampling frequency accuracy values for this clock configurations.

• For 16 kHz stream, the CKOuT frequency must be 1.024 MHz.   
• For 48 kHz stream, the CKOUT frequency must be 3.072 MHz.   
• The oversampling ratio is 64.

Table 15. DFSDM clock configuration accuracy values   

<table><tr><td rowspan=1 colspan=1>TargetAudio Frequency(kHz)</td><td rowspan=1 colspan=1>DivM</td><td rowspan=1 colspan=1>DivN</td><td rowspan=1 colspan=1>DivR</td><td rowspan=1 colspan=1>Output ClockDivider</td><td rowspan=1 colspan=1>DFSDM clock(MHz)</td><td rowspan=1 colspan=1>Accuracy(ppm)</td></tr><tr><td rowspan=1 colspan=1>16</td><td rowspan=1 colspan=1>5</td><td rowspan=1 colspan=1>192</td><td rowspan=1 colspan=1>5</td><td rowspan=1 colspan=1>60</td><td rowspan=1 colspan=1>61.44</td><td rowspan=1 colspan=1>0</td></tr><tr><td rowspan=1 colspan=1>48</td><td rowspan=1 colspan=1>5</td><td rowspan=1 colspan=1>192</td><td rowspan=1 colspan=1>5</td><td rowspan=1 colspan=1>20</td><td rowspan=1 colspan=1>61.44</td><td rowspan=1 colspan=1>0</td></tr></table>

# 5 Conclusion

The STM32 MCUs and MPUs provide a variety of audio and serial interfaces to connect digital microphones giving the flexibility to choose the most suited solution for each application.

This application note demonstrates the STM32 devices audio capabilities to interface digital MEMS microphones by describing the different ways to connect these microphones to the STM32 MCUs and MPUs peripherals and provides guidelines to use and properly configure these peripherals to acquire and handle the raw data from the microphones.

# 6 Revision history

Table 16. Document revision history   

<table><tr><td rowspan=1 colspan=1>Date</td><td rowspan=1 colspan=1>Revision</td><td rowspan=1 colspan=1>Changes</td></tr><tr><td rowspan=1 colspan=1>14-Dec-2017</td><td rowspan=1 colspan=1>1</td><td rowspan=1 colspan=1>Initial release.</td></tr><tr><td rowspan=1 colspan=1>17-Jul-2019</td><td rowspan=1 colspan=1>2</td><td rowspan=1 colspan=1>Updated all document to enlarge the scope to all STM32devices (MCU and MPU)</td></tr></table>

# IMPORTANT NOTICE  PLEASE READ CAREFULLY

acknowledgement.

the design of Purchasers' products.

No license, express or implied, to any intellectual property right is granted by ST herein.

product or service names are the property of their respective owners.

I