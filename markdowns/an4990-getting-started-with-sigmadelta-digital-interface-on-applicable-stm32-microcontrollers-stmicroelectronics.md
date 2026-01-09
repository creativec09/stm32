# Getting started with sigma-delta digital interface on applicable STM32 microcontrollers

# Introduction

The DFSDM (digital filter for sigma-delta modulators) is an innovative embedded peripheral available in a selection of STM32 microcontrollers (see Table 1: Applicable products), and is of particular interest for applications that process external analog signals.

Although the DFSDM is a pure digital peripheral, it is designed to support a wide range of external analog front ends. By keeping the analog front-end part (sigma-delta modulator) outside of the microcontroller, the user has total flexibility to select the analog properties according to the application requirements (analog range, noise, sampling speed).

The raw converted digital data from the sigma-delta modulator is then processed by the DFSDM peripheral (digital filtering). The DFSDM configuration is flexible enough to support a wide range of converted data properties: output data width, output data rate, output frequency range.

From an application point of view, the DFSDM with its external analog front-end behaves like an ADC converter. Additional functions typical of an ADC are also available within the DFSDM such as analog watchdog, extremes detector and offset correction.

# Reference:

[TUTORIAL]

In this document, [TUTORIAL] refers to a DFSDM simulator available in the form of a Microsoft® Exce® workbook, that can be downloaded from www.st.com, using home page search engine with keyword "DFSDM_tutorial".

Table 1. Applicable products   

<table><tr><td rowspan=1 colspan=1>Type</td><td rowspan=1 colspan=1>Applicableperimeter</td><td rowspan=1 colspan=1>Series, lines, references</td></tr><tr><td rowspan=4 colspan=1>Microcontrollers</td><td rowspan=1 colspan=1>Complete Series</td><td rowspan=1 colspan=1>STM32L4 Series, STM32L4+ Series, STM32H7 Series</td></tr><tr><td rowspan=1 colspan=1>Complete Line</td><td rowspan=1 colspan=1>STM32F412 line, STM32F413/423 line</td></tr><tr><td rowspan=1 colspan=1>STM32F76xxx</td><td rowspan=1 colspan=1>STM32F765BG, STM32F765BI, STM32F765IG, STM32F765II,STM32F765NG, STM32F765NI, STM32F765VG,STM32F765VI, STM32F765ZG, STM32F765ZI,STM32F767BG, STM32F767BI, STM32F767IG, STM32F767II,STM32F767NG, STM32F767NI, STM32F767VG,STM32F767VI, STM32F767ZG, STM32F767ZI, STM32F768AI,STM32F769AG, STM32F769AI, STM32F769BG,STM32F769BI, STM32F769IG, STM32F769II, STM32F769NG,STM32F769NI, STM32F769SL</td></tr><tr><td rowspan=1 colspan=1>STM32F77xxx</td><td rowspan=1 colspan=1>STM32F777BI, STM32F777II, STM32F777NI, STM32F777VI,STM32F777ZI, STM32F778AI, STM32F779AI, STM32F779BI,STM32F779II, STM32F779NI</td></tr></table>

# Contents

# Overview of A/D conversion principle using DFSDM .. 6

1.1 Fundamental concept of A/D conversion using DFSDM 6   
1.2 Sigma-delta modulator 6   
1.3 Digital filter 8

# Sigma-delta modulation principle (external analog front-end functioning, simulations) . . g

2.1 Principle of sigma-delta modulation 9

2.2 Advantages of sigma-delta modulation .11

2.2.1 Noise shaping 11   
2.2.2 Linearity of A/D conversion 12   
2.2.3 Scalable ADC resolution 12

# 2.3 Disadvantages of sigma-delta modulation 13

2.3.1 Offset and gain error .13   
2.3.2 Lower data rate 13

2.4 Simulation of sigma-delta modulation 14

2.4.1 Simulation with [TUTORIAL] 14

# Digital filtering - principle and design . . . . 15

3.1 Function description 15   
3.2 Example of Sinc filter function - resolution increase 15   
3.3 Hardware design of Sinc filter 17

# DFSDM peripheral operation . 22

4.1 Block diagram . 22

4.2 DFSDM components 22

4.2.1 Serial transceivers 22   
4.2.2 Parallel transceivers 23   
4.2.3 Digital filter . 23   
4.2.4 Integrator 23   
4.2.5 Output data unit 23   
4.2.6 Analog watchdog 24   
4.2.7 Short circuit detector 24

# 4.2.8 Extremes detector .25

.3 DFSDM simulation 25

4.3.1 Sigma-delta modulator principle 25   
4.3.2 DFSDM filtering simulation (filter and integrator) 26   
4.3.3 Frequency characteristics for Sinc filter 27   
4.3.4 Noise shaping of sigma-delta modulation .28   
4.3.5 High order filters operation 31   
4.3.6 Delta-sigma DAC simulation 33   
4.3.7 High pass filter simulation .34

# 4.4 Additional functions in DFSDM . 35

4.4.1 Digital microphones (MEMS) support 35   
4.4.2 Beamforming support 37   
4.4.3 Audio clock support - independent clock operation 39

4.5 DFSDM power consumption optimization 40

4.5.1 Power optimization in Sleep mode .40

# DFSDM peripheral configuration tutorial . 42

5.1 Configuration introduction 42   
5.2 Clocks configuration 42   
5.3 Transceivers. 43   
5.3.1 Serial transceivers configuration .43   
5.3.2 Parallel transceivers .46   
5.4 Filter 47   
5.4.1 Sinc filter .47   
5.4.2 Integrator 49   
5.5 Analog watchdog 50   
5.6 Short circuit detector 50   
5.7 Pulse skipper 51   
5.8 Configuration using [TUTORIAL] 52

# Conclusion . . 54

Revision history 55

Table 1. Applicable products 1   
Table 2. DFSDM application examples 44   
Table 3. DFSDM analog watchdog parameters 50   
Table 4. Document revision history 55

# List of figures

Figure 1. A/D conversion block diagram using the DFSDM. 6   
Figure 2. PWM modulation example 7   
Figure 3. Sigma-delta modulation example 8   
Figure 4. Sigma-delta modulation principle .9   
Figure 5. Sigma-delta modulator voltages timing diagram. 10   
Figure 6. Spectrum of PWM and sigma-delta modulation 12   
Figure 7. Simulation of sigma-delta modulator 14   
Figure 8. Example of 3rd order filter outputs with one bit per filter length 16   
Figure 9. Example of 3rd order filter outputs with higher density of input pulses. 17   
Figure 10. Basic schematic for simple moving average implementation . 18   
Figure 11. Simplification of Sinc filter design - step 1 18   
Figure 12. Simplification of Sinc filter design - step 2 19   
Figure 13. Simplification of Sinc filter design - step 3 20   
Figure 14. Simplification of Sinc filter design - step 4 20   
Figure 15. Higher order Sinc filter implementation. 21   
Figure 16. Block diagram of DFSDM peripheral 22   
Figure 17. Sigma-delta modulator simulation 26   
Figure 18. Filtering simulation 27   
Figure 19. Filter frequency characteristics . 28   
Figure 20. Sigma-delta and PWM modulated signals (for frequency spectrum   
comparison) 29   
Figure 21. Spectrum of sigma-delta signal and PWM signal . 30   
Figure 22. Spectrum of sigma-delta signal and PWM signal   
with signal amplitude reduced to 10% of full scale 31   
Figure 23. High order filters - multiple averaging principle. 32   
Figure 24. First order delta-sigma DAC principle. 33   
Figure 25. Delta-sigma DAC simulation. 34   
Figure 26. HP filter simulation 35   
Figure 27. MEMS microphone outputs (L and R channel). 36   
Figure 28. MEMS microphone connection to DFSDM (stereo support). 36   
Figure 29. Beamforming principle 37   
Figure 30. Pulse skipping implementation for beamforming 38   
Figure 31. Pulse skipping example (FOSR=8). 39   
Figure 32. Sinc filter frequency characteristic shape . 48   
Figure 33. DFSDM configuration in [TUTORIAL]. 53

# Overview of A/D conversion principle using DFSDM

This document supports Arm®abased devics.

# arm

# 1.1 Fundamental concept of A/D conversion using DFSDM

The basic block diagram of analog-to-digital conversion using DFSDM is provided in Figure 1.

![](images/037bf4e81166bd8eeb64dcff2bae71788937a08a68540b89c2777ef121019449.jpg)  
Figure 1. A/D conversion block diagram using the DFSDM

The external analog signal is processed by an external sigma-delta modulator which converts the analog signal into a digital 1-bit stream (DATA and CLK signals). The 1-bit stream is a fast serial line stream of logical ones and zeros: the DATA signal is sampled by CLK (clock signal). The average value of these logical ones and zeros, computed during a long enough time duration, represents the analog input value. The duration of the averaging period determine the precision of the analog input signal capture.

The averaging of the 1-bit stream is performed by the STM32 microcontroller DFSDM peripheral (DFSDM = digital filter for sigma-delta modulators). The DFSDM acquires and processes the 1-bit data stream (digital filtering, averaging). The DFSDM outputs data samples at a slower data rate than the input 1-bit stream but with a higher resolution. The DFSDM digital filter settings define the output resolution and data rate.

# 1.2 Sigma-delta modulator

The DFSDM peripheral requires an external analog front-end that performs the A/D conversion of the analog source. This external analog to digital conversion is performed in a sigma-delta modulator.

elh data into a serial digital data stream. The analog input is sampled and converted into a 1-bit digital data stream with alternating zeros and ones. The mean value of the digital stream

computed during a given time interval represents the average value of the input analog signal during the same time interval. The sigma-delta modulation principle could be presented as a special PWM modulation where both the period and the duty cycle would be modulated (whereas the period is fixed and only the duty cycle is modulated in a typical PWM modulation). See Figure 2 and Figure 3 for comparison between PWM and sigmadelta modulation.

The digital data stream outputting the sigma-delta modulator is then processed by the STM32 microcontroller DFSDM peripheral. The DFSDM performs a digital filtering using parameters that need to be configured according the application requirements.

# Note:

For analysis, the digital stream is usually "converted" from binary 0 and binary 1 weights into +1 and -1 weights for comparison with input voltages cleared of any DC component. The zero input voltage generates duty cycle 50:50 (first order sigma-delta modulator is used).

![](images/dff8a7771c6f34779a71778c67c96e5c82e3444bf2ad04f55b6902bbcb8f005c.jpg)  
Figure 2. PWM modulation example

![](images/c4ea8c8e0844a2efe12d6eb8ca290ac8fdb94a688a910aa5a83408b5f6407fd7.jpg)  
Figure 3. Sigma-delta modulation example

# 1.3 Digital filter

The DFSDM peripheral (digital filter for sigma-delta modulators) processes the digital part of the A/D conversion. The digital data stream is provided by an external sigma-delta modulator. The basic functionality of the DFSDM is to implement a digital filter. The DFSDM processing consists in averaging a fast rate input serial stream and producing a parallel, lower rate, data output with higher resolution. The DFSDM embedded filter features a set of configurable parameters that allow to tune the output resolution and data rate and meet the application requirements.

The DFSDM features aditional ADC-related functionalities including:

Independent fast watchdog on each channel with programmable speed and resolution to detect input signals exceeding minimal or maximal allowed voltage levels.   
Break signal generation used to instantaneously report events like analog watchdog or short circuit detection to other peripherals (timers).   
Short circuit detector on each channel for very fast detection of signal clamping: when input voltage reaches one of the analog range limits and stays steady in excess of a given time duration (independent from the main conversion).   
Extreme detector to record minimal and maximal input voltage excursion.

# Sigma-delta modulation principle (external analog front-end functioning, simulations)

# 2.1 Principle of sigma-delta modulation

The basic functional block diagram of a sigma-delta modulator is presented on Figure 4.

![](images/f4bd3896b6b8243bad9eb3250f139f16a0995256b25cf2754ef36f9e32427a84.jpg)  
Figure 4. Sigma-delta modulation principle   
e  ] en  ebovg  he  p.

Figure 5 provides an example of the signals available at the different stages of the analog to digital conversion.

![](images/bddc0fe17aa8015240f0042ebf9d2daedc70bb23d828989a2acd8ac548194ca3.jpg)  
Figure 5. Sigma-delta modulator voltages timing diagram

The reerencs []  [5] presnt  he above gure ae use n he oowi paraah.

The below description of sigma-delta modulation uses references present in Figure 4 and Figure 5:

The analog input signal [1] is added to the 1-bit DAC output feedback from the comparator (+Vref or -Vref voltage) and the result [2] goes to the integrator. The integrator cumulates the difference between the analog input signal [1] and the 1-bit DAC output feedback (+Vref or - Vref voltage). The integrator output [3] is then compared with the zero voltage reference by the comparator. The comparator output [4] is latched periodically at the clock frequency by the D-latch to propagate the comparator result to the modulator output in quantized time steps (clock ticks). The D-latch output [5] is the digital 1-bit output from the sigma-delta modulator. The output is fed back to the 1-bit D/A converter which outputs only 2 possible analog voltages (usually implemented as a switch between +Vref and -Vref reference voltages). The data rate of the 1-bit output data stream is defined by the modulator clock frequency.

The output of the sigma-delta modulation is a digital data stream (black curve on Figure 5) that is clocked by the modulator clock. The average value of this output (computed in the digital domain) represents the input analog voltage. This digital average should be computed as the ratio between the number of ones versus the number of zeros observed during a given number of clock periods within the sigma delta output stream.

This digital data stream constitutes the input of the STM32 microcontroller DFSDM peripheral where it can be filtered. DFSDM configurable parameters need to be set according the application requirements.

# 2.2

# Advantages of sigma-delta modulation

# 2.2.1 Noise shaping

The output signal from the sigma-delta modulation must be filtered to remove the high frequency content (the quantization noise) and retain only the useful frequency band. In order to properly design such filter, some understanding of the sigma-delta modulated signal spectrum is required. The sigma-delta modulated signal spectrum is different from the PWM modulation spectrum.

The PwM modulation signal is characterized by a fixed period and a variable duty cycle. Due to the fixed modulation period (or frequency), the PWM spectrum exhibits typical peaks of energy corresponding to the modulation base frequency and its harmonics. The removal of these harmonic peaks is more difficult by analog filtering (RC or LC filter).

The sigma-delta modulation uses both variable duty cycle and variable frequency. As a result, the energy on the sigma-delta spectrum is spread more evenly and is not concentrated on regularly spaced peaks like for the PWM (there is no fixed modulation frequency). Furthermore, there is usually more energy at higher frequencies for sigma-delta modulations than for PWM (due to higher modulation frequencies). The noise content of sigma-delta modulation can be easily removed by analog filtering (RC or LC filter).

A typical spectrum for a PWM and for a sigma-delta modulation are provided on Figure 6 (corresponding respectively to signals presented in Figure 2: PWM modulation example and Figure 3: Sigma-delta modulation example). The PWM modulation produces higher peaks at lower frequencies, therefore the PWM processing requires a filter of higher order in order to properly reject the first peak of energy corresponding to the PWM modulation base frequency. In the sigma-delta modulation spectrum the energy is less present at lower frequencies so the filter design can be simpler. The filtering capabilities must be adapted to the order of the sigma-delta modulator. For example, digital microphones typically have a 4th order sigma-delta modulator, which has a low quantization noise in the useful band, but a very strong out-off band quantization noise. The filter order must be selected in order to suppress this strong out-off band quantization noise without affecting the useful band.

The effect of the sigma-delta modulation to spread the quantization noise more evenly and to higher frequencies is called "noise shaping". One can take advantage of such characteristic to design simpler filters and benefit from less noisy baseband signals.

![](images/072bdde79c3d22bc651ed84f2296853c3ac6c0cb36cb38b43a1cd2bf4339e9da.jpg)  
Figure 6. Spectrum of PWM and sigma-delta modulation

# 2.2.2 Linearity of A/D conversion

The output from the sigma-delta modulator is 1-bit serial data stream. The resolution of this stream is only one bit which is usually not enough for the application. The method to increase the signal resolution consists in averaging the 1-bit stream during a given period of time. The averaged data stream has a wider resolution (typically 16-bit) but a slower sample rate. The averaging (filtering) operation is based on linear mathematical operation in the digital domain hence there is no added non-linear distortion due to filtering.

A/D converters with parallel data output usually use more analog elements than the sigmadelta modulators. For example the SAR ADC type with N-bits resolution uses internally a R-2R resistor network (or C-2C capacitor network) with N resistors (or capacitors). The resistors (capacitors) used in these type of ADCs must have a precise 1:1 or 1:2 resistance (capacitance) ratio. The linearity of the SAR ADC depends on the precision of the resistors (capacitors). In practice the ratios are never perfect and the imprecision is at the origin of non-linearities that impact the transfer curve.

For above mentioned reasons, the linearity of A/D conversion using sigma-delta modulation is usually better than with other type of A/D conversion. The non-linearity in the sigma-delta ADC conversion depends only on the sigma-delta modulator design (see Figure 4: Sigmadelta modulation principle). Furthermore, the non-linearity depends only on the influence of the input voltage on analog element intrinsic characteristics (capacitors/resistors in integrator and switches which capacitance/resistance changing with input voltage) and not on ratios between the different component nominal values. Linearity is more important for audio applications where the non-linearity causes signal distortion (static linearity INL is linked with dynamic linearity THD).

# 2.2.3 Scalable ADC resolution

The final output resolution for sigma-delta conversion is not fixed (as it is for example for a 12-bit SAR ADC). The output from a sigma-delta modulator is 1-bit resolution which can then be increased by following digital filtering (averaging) to the required resolution.

The drawback of this resolution increase is the reduction of the output data rate. This data rate decrease is predictable and must be computed for a given application requirement. For example a digital filter can be configured for a 24-bit output @ 1 kHz output data rate, or for a 16-bit output @ 50 kHz output data rate.

The resolution increase is theoretically unlimited but in practice one needs to take into consideration the noise and the errors caused by the components in the conversion path (sigma-delta modulator design, injected noise .). Another consideration is the stability of the signal during the sampling period that can affect the precision of the measurement, in particular for applications with very low data rate and high resolution.

# 2.3 Disadvantages of sigma-delta modulation

# 2.3.1 Offset and gain error

The average of the 1-bit data stream signal from sigma-delta modulator represents the mean value of the analog input signal. The precision of this digital output average (in the range [0..1]) can be affected by the following sigma-delta modulator components (see Figure 4: Sigma-delta modulation principle):

• resistors and capacitors in the integrator • reference voltage in the 1-bit DAC (+Vref / -Vref) offset of the integrator

These components have tolerances: capacitor/resistor values, offset voltage, difference between +Vref and -Vref absolute voltage.

In the ideal case, a 1-bit digital output having in average the same amount of O's and 1's corresponds exactly to a zero volt input signal. Due to the components tolerances (mentioned above) the input analog voltage corresponding in a same amount of O's and 1's, is not exactly zero volt, and represents the offset error. The offset error can be compensated by software or by hardware (calibration process).

In the ideal case the output 1-bit digital signal with a 50:50 duty cycle (amount of 0's is equal to the amount of 1's) should correspond exactly to the zero input analog voltage. Due to the components tolerances (mentioned above) the input analog voltage corresponding to the 50:50 duty cycle is not exactly zero and represents the offset error. The offset error can be compensated by software or by hardware (calibration process).

The gain coefficient that is the ratio between the output data and the input voltage is also affected by the sigma-delta component tolerances. The difference between the theoretical gain and the actual measured conversion gain represents the gain error. It can be also compensated by calibration (usually in software).

Some characteristics of the sigma-delta components are also dependent on temperature, which affects in turn the offset and gain errors. The influence of the temperature on the integrator resistors and capacitors affects only the gain error. The offset error is less affected by the temperature changes because the errors affecting +Vref and -Vref, due to the symmetric nature of these references, are self compensated.

# 2.3.2 Lower data rate

With sigma-delta modulators, a way to increase the resolution is to increase the averaging of the 1-bit data stream (longer averaging time or higher filter order). This is why the sigma-

delta converters are primarily used for lower data rate applications (usually for audio frequency range and lower frequencies). But in special cases where the excellent linearity is a must, the sigma-delta converters can be used for higher data rate applications.

For quasi static applications (temperature sensors) the data rate is not a constraint and the sigma-delta modulator is often chosen for its scalable resolution capability (high resolution on low data rates).

# 2.4 Simulation of sigma-delta modulation

# 2.4.1 Simulation with [TUTORIAL]

To help understanding the sigma-delta modulation, the sigma-delta model (as shown in Figure 4: Sigma-delta modulation principle) has been implemented in [TUTORIAL]. The timing diagrams are provided for each voltage signal referenced in Figure 4: Sigma-delta modulation principle. The user can change some parameters and input voltages and see the impact at each stage of the sigma-delta modulator. A simulation example available in [TUTORIAL] and based on a sinewave input signal is shown on Figure 7.

![](images/293d33c7f309a8c99dcd75a0880e0861487bbc77a5079ce0004c87f758749f12.jpg)  
Figure 7. Simulation of sigma-delta modulator

# Digital filtering - principle and design

# 3.1 Function description

The digital filter performs the filtering (averaging) of the 1-bit data stream generated from the sigma-delta modulator. The filter output is a data word with higher resolution (usually 12 - 24 bits) but reduced data rate (decimation). The digital filter function consists in removing out-off band frequency components (quantization noise, unwanted signals...) and reducing the data rate according to the useful bandwidth (decimation).

The design of the filter has a strong influence on the A/D conversion characteristics and is the result of a compromise between the required parameters (sharpness of filter, filter tuning, final resolution, ...) and the hardware implementation complexity (which leads to cost issue). The goal is to minimize the filter design complexity while meeting the required A/D characteristics.

# Note:

Signal filtering often requires more complex processing than simply averaging the 1-bit data stream.

Here are some elements to consider when designing a filter:

√ Filter type:

Among various types of filter, the Sinc filter presents interesting characteristics, combining a cheap hardware implementation with acceptable level of performance. The Sinc filter has a frequency response that can be modelized by a sinc(x) function (hence its name). The Sinc filter is the most commonly used type in sigma-delta A/D converter implementations. It is cheap because no multipliers are required, and the filter coefficients are integers. The Sinc filter performs a simple "moving average" calculation over the 1-bit samples.

Filter length (FOSR - filter oversampling ratio):

A longer filter (averaging of more samples) generates higher resolution but decreases the output data rate (decimation). Therefore the filter length is selected as a compromise between required conversion rate and final data resolution.

Filter order (FORD):

The "moving average" calculation can be applied multiple times to already averaged samples. The filter order defines how many time the "moving average" calculation is applied to the same input samples. A higher order filter generates higher resolution (by adding more averaging loops) but increases latency.

# .2 Example of Sinc filter function - resolution increase

This section focuses on showing how multiple "moving average" calculations can increase the Sinc filter resolution.

Here is a detailed presentation of a 3rd order filter (FORD=3) with length FOSR=10 (with moving averaging at each filter stage):

The observation is done on 3 periods of the input stream: 3 x FOSR = 30 samples (see Figure 8 and Figure 9). The input 1-bit data stream is almost always '0' except for '1' pulse per averaging period (FOSR=10) (see the "Input" curves on Figure 8 and on Figure 9). Two input streams are tested: one stream with exactly equidistant pulses (at position 10, 20 and

30 on horizontal axis see Figure 8) and another stream where the second pulse is anticipated by one period to simulate a slightly higher pulse density (position 10, 19 and 29 on horizontal axis, see Figure 9).

The first order filter stage is performing moving average (see the "1st order" curves) and the final result is sampled at each FOSR cycle and constitutes the 1st order filter lt     I a pe al sul  o cass (Figure 8 and Figure ) because of simple moving average in filter stage (only one '1' in each period).

The second order filter stage is performing moving average on samples from first filter order stage (see the "2nd order /10" curves). The final result is sampled at each FOSR cycle and constitutes the  order filter result (at 0t, 0t cycle). There is a visible difference in the final results between the two output streams (Figure 8 and Figure 9): due to higher density of '1s' (with the higher density stream of Figure 9 it produces higher value than with the lower density stream of Figure 8).

The third order filter stage is performing moving average on samples from the second filter order (see the "3rd order /100" curves). The final result is sampled at each FOSR cycle and constitutes the  order filter result (at 30th cycle). There is a visible difference in the final result between the lower density stream (Figure 8) and the higher density stream (Figure 9). Due to moving averaging the third output is smoother and more precise.

Ta      u e  OSRFR FORD x FOSR samples before obtaining the first result because every filter stage must be filled with valid samples from previous filter stage (see Figure 8 and Figure 9). In conclusion, higher order filters offer better resolution for a given stream duration or the same resolution for shorter stream duration. The drawback is a more complex hardware design and a longer initialization time for the filter.

![](images/b04e335ef8f5765bafd2370d3944d52d2f9c11a5f1152f343c194251c616027c.jpg)  
Fuapl fuu i

![](images/1842c0aa3718ef8fb265c031cfc754fdee80678aa6f978467f74fa7955e47d51.jpg)  
FuExmple   fl utus with higher densiy ut puls

# 3.3 Hardware design of Sinc filter

Sinc filters are characterized by a Sinc transfer function which equation in the digital domain is provided below. It can be interpreted as multiple moving average of input 1-bit data. The rest of this section focuses on finding simplifications in order to achieve an efficient and ultimately quite simple hardware implementation.

Equation 1:

![](images/1d456129b2b2a74586e024c94cfbe1eed096e785e29b48759a660549497023d0.jpg)

Where:

x(n) is the input of nth sample y(n) is the output of nth sample

Figure 10 provides the straight forward translation of the above equation into a hardware implementation:

![](images/dc645fb664f502bded776db3e1e023c93033e1cbd206d98efaca93726d350d4b.jpg)  
Figure 10. Basic schematic for simple moving average implementation

The above hardware implementation required (FOSR -1) adders and (FOSR-1) flip-flops.   
Some simplifications can be introduced that are developed hereafter.

The Equation 1: can be simplified by using previous output result y(n-):

Equation 2:

![](images/56332b6560b12a3ea41944e9672d8334b5799813db19da178502919db1ae9159.jpg)

Equation 3:

![](images/e0f94aacc6419c93ffa4e778dd92d008b9cf52f98bf0419703ad71eac950e1c0.jpg)

Figure 11 provides a simplified schematic requiring only 2 adders and FOSR+1 flip-flops.   
The schematic can now be divided into two parts: comb and integrator.

![](images/228a3785535267629a1677a1fc80f239e4a69930ac89a0373e5d478ab9b17886.jpg)  
Figure 1. Simplification of Sinc filter design - step 1

MSv36537V1

A further simplification can be obtained by converting the equation to Z-domain (frequency domain) according these correspondences:

X(z) in the Z-domain corresponds to x(n) in the discrete time domain, where n is an integer number of sample clock periods (sample clock period = 1/Fs; Fs = sampling frequency) X(  (n  (    .

The equation for a 1st order Sinc filter in Z-domain becomes:

![](images/f5b0ff80eb7fffb9953f99d409e058612c32fd4827b30d2fc66506f27c9f6558.jpg)

The corresponding transfer function H(z) is:

![](images/7a0855158310d7a23cef3aab47b90a317496953f2c45bd26f72b7619f05c6e68.jpg)

In Figure 11 we introduced a decomposition of the Sinc filter in two stages: "comb" and "integrator". The transfer function of such filter (called CIC: cascaded integrator-comb filter) is given by:

The comb transfer function in Z-domain:

![](images/71984764b7f93808693381f66162461a0b9d26f8f70bb3adae176fc93fa98a1d.jpg)

The integrator transfer function:

![](images/4e8a674710858cc8253612c8812b723b44faa82ff7294e929eb0803c6779d074.jpg)

The overall transfer function is equivalent to the Sinc filter transfer function:

![](images/64b1810b59f90eb05f4c56fa0fc40140d0d5daeaab58714b7463293263a6dfd3.jpg)

One more filter simplification consists in permuting the comb and the integrator operation as shown in Figure 12:

![](images/abcb1c834a9e34fbc4d9ad6d02382cbba10d0a65ccfecd187869d16d9fc14f70.jpg)

![](images/f5b3883da33f8f8c6b6d837d78ff20ff1979c1a899a379635de440c5cae51ebc.jpg)  
Figure 1. Simplification of Sinc filter design - step 2

Because the filtering limits the output signal bandwidth, it is possible to down-sample the output y(n) by a factor FOSR. This down-sampling is achieved by taking one sample of y(n) every FOSR clock cycles (see Figure 13).

![](images/69c7dccc465c6016e1d7e9d9f5eca4e2e7b74c4cf1c50225e0cf7637c93cface.jpg)  
Figure . Simplification of Sinc filter design - step 3

The down-sampled clock period is defined as:

![](images/f5a759c6330c7b265852aae015e8906eeae041acb5981b428dc09bc4721f5154.jpg)

The equation for the down-sampled comb section can be re-written as follows:

![](images/19e2f452cd80dfc972cd942add12a5d649d1d5462fec4e7e3af59629f9c2fa94.jpg)

This operation corresponds to a down-sampling of p(n) by the factor FOSR, followed by a first order differentiator. The series of flip-flop sampled at high frequency can be replaced by one single flip-flop with down-sampled frequency. The final schematic is shown on Figure 14.

An effect of down sampling is to eliminate the moving average operation (because the output data rate is reduced).

![](images/e46950bb0438f61d24e5c764c5b81431bb045b554a50e2f5507d48609cf4433c.jpg)  
Figure . Simplificationof Sinc filter design ste

The final schematic (Figure 14) is reduced to 2 flip-flops and 2 adders (all with FOSR-bit width).

Higher order Sinc filters are obtained as a serial cascade of first order filter stages where comb and integrator stages can be grouped together (Figure 15).

![](images/9420031e2186532080a3adabe90b7b9c7806e109e5a8fd23ffc8bace148e3f38.jpg)  
Figure 15. Higher order Sinc filter implementation

Cascading FORD first order filters:

![](images/b83eafa944a587e203174a81027706f5ba797cb158288b819e41fbd2e2e39f3a.jpg)

Reordering:

![](images/0e7f139914b8c36022f422702675851bdf4db71e6d26f5ab6348ba8d2c1e57b7.jpg)

Final equation:

![](images/f53104f9f1375dcc6a438620788cf51e206efca1087f5d1a55cc90cab52e09fd.jpg)

The down-sampling is performed at the output of the final integrator stage, allowing to replace each comb stage with a unity delay differentiator at the down-sampled rate (see Figure 15).

Note:

The Sinc filter implementation can be extended to multi-bit width input signal (for example for parallel data input instead of serial data input). In this case the bit-width of flip flops and adders should be extended.

# DFSDM peripheral operation

# 4.1 Block diagram

The block diagram of the DFSDM peripheral with all the internal functional blocks and their internal and external connections is provided on Figure 16. The DFSDM cannot be reduced to only a digital filter but consists in a complete digital peripheral that handles the overall A/D conversion (when associated with an external sigma-delta modulator).

![](images/4d9656d3c5d825c48059c7e4547176f8ca02acf937f49a6d28e24dff0acf866c.jpg)  
Figure 16. Block diagram of DFSDM peripheral

# 4.2 DFSDM components

# 4.2.1 Serial transceivers

The "serial transceivers" block receives serial data from the external sigma-delta modulator. It features SPI and Manchester serial protocol formats with configurable rising/falling sampling clock edge in order to support most of the sigma-delta modulator types. It supports as well the PDM signal format used by digital microphones - see Figure 28: MEMS microphone connection to DFSDM (stereo support).

Up to two digital microphones (configured as stereo microphone) can be connected to one DFSDM_DATINy pin. In this case, each microphone is configured to be sensitive to a different sampling clock edge (the signals from both microphones are present on a single DFSDM_DATIN data line). In order to distribute this composite signal to two different channels, both channels must be configured to take their serial input from the same pins (DFSDM_DATINy, DFSDM_CKINy) where the two microphones are physically connected (see Figure 28: MEMS microphone connection to DFSDM (stereo support)). Each channel is then configured to sample the data on a different sampling edge.

An external clock signal can be connected to DFSDM_CKINy pin (assuming sigma-delta modulator provides this clock signal) or the clock signal can be taken from the internal clock generator (assuming sigma-delta modulator needs external clock signal). The internal clock generator drives the sigma-delta modulator through DFSDM_CKOUT pin. The Manchester format protocol does not require external clock signal because this protocol is single-wire (on DFSDM_DATINy pin) and clock signal is reconstructed from Manchester coded stream. There is a clock signal presence detector that can be used in case of missing clock (external hardware failure) to trigger an interrupt.

The serial transceiver provides also a "Pulse skipper". The Pulse skipper allows to pause the output of the serial transceivers during a given number of sampling clock pulses (given count of 1-bit data samples are discarded). In practice, the "Pulse skipper" is used in beamforming applications in order to delay one channel data with respect to another channel data. Beamforming is a technique that consists in sensing signals (sounds) from a preferred direction by using an array of detectors (microphones). A delay is injected to each microphone signal relative to the previous microphone signal. The delay defines the preferred sensing angle.

# 4.2.2 Parallel transceivers

The parallel transceiver is an internal 16-bit parallel input register which can be accessed through the APB bus by the CPU, the DMA, or directly by the internal ADC. Its function is to allow post processing (filtering) of internal signals. Examples of usage:

• Filtering data captured by internal ADC   
• Filtering data captured by SPI peripheral (through memory buffer) Filtering any 16-bit data stored in memory buffer (DMA transfer to DFSDM parallel transceiver).

# 4.2.3 Digital filter

The digital filter is a key component that processes the input data. The digital filter is configurable to support final application needs (speed, resolution). The following parameters can be configured:

Filter order: Sinc1 ... Sinc5, FastSinc   
Oversampling ratio: FOSR = 1 .. 1024 (for Sinc1 ... Sinc3, FastSinc) FOSR = 1 ... 215 (for Sinc4) FOSR = 1 ... 73 (for Sinc5)

The FOSR ranges provided above take into account the filter order and the filter internal resolution (32-bit width) in order to avoid overflow (case of a 1-bit input signal, for multi-bit parallel input signal the ranges are reduced).

# 4.2.4 Integrator

The optional integrator works as a simple adder. It sums up a given number of samples provided by the filter output. The number of filter output samples that are summed to provide the single integrator output is configurable in the range IOSR = 1 .. 256. The integrator works like a Sinc1 filter (it is performing the average of a given number of samples).

# 4.2.5 Output data unit

The output data unit performs a final correction that consists in shifting the bits to the right and applying an offset correction on the data coming from the integrator.

Shifting bits to the right is used to:

• fit the 32-bit internal output into the final 24-bit register • limit even more the final resolution (to 16-bit for instance in case of audio data)

The offset correction allows to calibrate the external sigma-delta modulator offset error. The user configures the offset register with a signed 24-bit correction, and this register is automatically added to the output result. The offset correction value is usually the result of a calibration routine embedded within the microcontroller software that performs the offset calibration calculation and stores the correction into the offset register.

All operations in the DFSDM peripheral are in signed format (filtering, integration, offset correction, right bit shift).

# 4.2.6 Analog watchdog

The analog watchdog function is the same as in the ADC peripheral. Its purpose is to control that the ADC data excursion stays within given limits by triggering the microcontroller CPU (interrupt) or other peripherals (break signal) when the signal exceeds predefined thresholds.

Not only the DFSDM output data but also the raw data from the sigma-delta modulator (serial transceiver output) can be monitored.

The analog watchdog can monitor serial data directly from the serial transceiver through a dedicated configurable digital filter (FOSR = 1...32, FORD = 1...3). This gives the user the ability to find the best compromise between monitoring speed and monitoring resolution, independently from the main data conversion speed. Some applications require that the reaction time to an input signal exceeding the thresholds, be faster than the main conversion speed. The monitoring of the thresholds for the main conversion itself is usually more precise but slower.

# 4.2.7 Short circuit detector

The short circuit detector is designed for very fast detection of sudden analog input signal saturation, when the signal is over or under the maximum allowed range. In normal situation the analog input signal gain is controlled (current or voltage sensing loop) in order to never reach such saturation levels. In some extreme situations (like a short circuit) the sensed signal measurements can exceed the operating range limits. In this case the reaction time must be as fast as possible (to switch off the supply for instance).

This very fast detection is implemented in the short circuit detector. The detection of signal saturation is based on the analysis of the 1-bit data stream coming from the serial transceiver. A typical sigma-delta modulator outputs a 1-bit signal with frequent transitions between '0' and '1' (to reproduce the analog signal fluctuations). When a saturation of the input signal occurs the output from the sigma-delta modulator gets stuck with either long series of logical '0' (signal under negative threshold) or long series of logical '1' (signal above positive threshold). If this situation exceeds a certain duration the short circuit detector triggers a "short circuit" event. The duration threshold to trigger a detection can be set in the DFSDM short circuit detector threshold setting (SCDT) in the range 1 to 256 input sample counts. For example if SCDT=100 the short circuit detector event is triggered as soon as at least 100 consecutive '0' or '1' are detected in the input 1-bit data stream. The short circuit detector can trigger an interrupt (software intervention) or activate a break signal (fast hardware intervention).

This type of short-circuit detection is much faster than the detection based on analog watchdog involving digital filtering over longer series of 1-bit input samples.

# 4.2.8 Extremes detector

The extremes detector simply analyzes the final output data samples and stores the minimum and maximum values into extremes registers. By reading those extremes registers it is possible to monitor the maximum and minimum level of the converted signal during a period of time. Those levels are useful inputs for software post processing, for example for signal normalization or for automatic gain control. Each time the extremes registers are read, they are re-initialized with their reset values and the extremes detection is restarted.

# 4.3 DFSDM simulation

The sigma-delta modulator and the DFSDM internal blocks behavior are modeled within [TUTORIAL]. The incidence of the input signal and the influence of the DFSDM parameters can be simulated and both the internal and output signals can be observed and analyzed.

The proposed simulations cover:

• Sigma-delta modulator (principle of operation demonstration)   
• Sinc filter + integrator (digital filter functionality demonstration)   
• Frequency characteristics of Sinc filters (LP filters shape demonstration)   
• FFT of PWM and sigma-delta signals (noise shaping demonstration) High order filters operation (demonstration of resolution increase by multiple signal average) Delta-sigma modulator (DAC converter)

# 4.3.1 Sigma-delta modulator principle

This simulation is provided in the first worksheet of [TUTORIAL].

The simulation of the first order sigma-delta principle is based on the schematic provided in Figure 4: Sigma-delta modulation principle where each block has been modeled. The input signal to the modulator corresponds to one period of a sinewave signal. For each observation point (as referenced on Figure 4) corresponds a curve in the chart provided in Figure 17.

The user can modify the input signal shape or modify some parameters of the modulator (integrator gain, Vref level) and visualize the impact on the digital output of the sigma-delta modulator.

This simulation illustrates the principle of the sigma-delta modulator and allows to visualize the internal signal at different stages of the processing.

Here the sigma-delta modulator is modeled as a first order, in order to explain the basic principle. In practice most sigma-delta modulators are using 2nd order with the exception of digital microphones that are typically using 4th order.

![](images/b38104d699e4930c5e38a38810d028077c029a5e7182c2fd9399c37f2334b6a6.jpg)  
Figure 17. Sigma-delta modulator simulation

# 4.3.2

# DFSDM filtering simulation (filter and integrator)

This simulation is provided in the second worksheet of [TUTORIAL]. This part of the DFSDM simulator corresponds to the Sinc filter and the integrator stages (see Section 4.2.3: Digital filter and Section 4.2.4: Integrator for details).

Both the Sinc filter and the integrator models are built within [TUTORIAL] and can be simulated. The user can change the FORD and FOSR parameters for the filter and the IOSR parameter for the integrator. The simulation results are identical to the results obtained with the actual DFSDM block. The user can tune in simulation the filter and the integrator parameters according to his application and observe the impact on the output signal shape without waiting for the actual prototypes.

This simulation requires a digital signal input (1-bit data stream) from the sigma-delta modulator (like in real application). In this particular simulation, the input is provided by the results of the first order sigma-delta modulator simulation also available in [TUTORIAL] (see Section 4.3.1: Sigma-delta modulator principle). By doing so, it is possible to compare the output digital signal (DFSDM filtering simulation curve) with the input analog signal applied to the sigma-delta modulator. The filter parameters should then be adjusted in order to reach the application requirements in term of acceptable error between the analog input signal into sigma-delta modulator versus the output digitized signal from the DFSDM (final output samples).

Figure 18 provides not only the output curve (FORD = 5) but also the internal data results at the output of each filter order. It shows the resolution gain that is obtained by performing more moving average loops.

![](images/1a5d8565735c61e6f40cf2bc5052962e2954c9898b8f97dcfe701adb1f2f7439.jpg)  
Figure 18. Filtering simulation

# 4.3.3 Frequency characteristics for Sinc filter

This simulation is provided in the third worksheet of [TUTORIAL]. It allows to visualize the frequency characteristics of the Sinc filter depending on the filter order.

The frequency characteristics of a filter can be determined by applying an impulse signal at the input of the filter and by computing the FFT transform of the impulse response at the output of the filter. This is how the filter characteristics have been computed in the simulation model. The model calculates the impulse response of the filter and submit the result to a 512-point FFT transform. The results for different filter orders are available in [TUTORIAL] and provided in Figure 19.

The frequency response has a comb shape with periodic attenuation points (notches - also called "zeroes") and a decreasing trend for higher frequencies (low pass filtering). The n  O. Inc  plig n/O  lso e utt at a ey. T frequency components of the input signal corresponding to the notches are completely rejected by the filter. This property can be used in some applications to remove external noise from the input signal at predetermined frequencies. As an example, the long wires that sometime are necessary to connect distant sensors to the microcontroller are prone to collect noise from the power network (50/60Hz) that can be filtered according the above property.

Another property is that the attenuation of the higher frequencies (other than notches which frequency depends only on FOSR) is proportional to the filter order (FORD). So the higher the filter order, the more rejection on higher frequencies. In applications which are sensing quasi static signals (like temperature or pressure sensors) a high order filter (FORD) is recommended as well as a high oversampling ratio (FORD) to suppress noise from AC perturbations. A further filtering of quasi static signals can be done by using the integrator located after the filter. Increasing the integrator oversampling ratio (IOSR) allows to performs additional averaging of the signal. In practice, the user should first set a (high) FORD and then set correctly the FOSR and the IOSR to suppress the noise from mains (/6z. e  o he bloconti [f t] is at frequency: fsampling(FOSR\*IOSR).

![](images/ff99f8b56cf5a800ce3d58aaa96253441ea8c19e9c83c6d090dafae6954d7e9b.jpg)  
Figure 19. Filter frequency characteristics

# 4.3.4 Noise shaping of sigma-delta modulation

This simulation is provided in the fourth and the fifth worksheets of [TUTORIAL]. It compares the spectrum of a PWM modulated signal with the spectrum of a sigma-delta modulated signal and highlights the benefits of the later with respect to noise shaping. The same input signal (one period of a sinus wave, see Figure 20) is either sigma-delta modulated or PWM modulated before undergoing an FFT transform. The frequency spectrum of both the PWM modulated signal and the sigma-delta modulated signal are compared in Figure 21. The Xaxis represents the frequency in multiple of the base signal frequency (signal base frequency and its harmonics), the Y-axis represent the spectrum density. Logically, the amplitude of the spectrum at index 1 (signal base frequency) is very large (\~470). All the other peaks located at indexes > 1 would have to be filtered out in order to reconstruct the original signal.

![](images/ceb8d68cedfdef4fc6431f2941bbb1256e5241d4b2e3eb98ccfce1563c550fa8.jpg)  
Figure 20. Sigma-delta and PWM modulated signals (for frequency spectrum comparison)

![](images/e9e125503113188ab1fe8540bbbb3e88487e0a22ffe1cc0c72e914a3d06190ad.jpg)  
Figure 21. Spectrum of sigma-delta signal and PWM signal   
Figure 21 illustrates the fact that a PWM signal spectrum concentrates its energy on peaks located around multiple of the modulation frequency (modulation frequency = 16 x signal base frequency in this case). This is due to the characteristics of a PWM modulation that has a constant modulation frequency and a variable duty cycle. The amplitude of the peaks decreases with frequency increase.

On the opposite a 1st order sigma-delta modulation spectrum shows an amplitude that is low on the first harmonics, and then increases progressively with the frequency.

As a consequence of the previous observations, the requirements on the low-pass analog filter that is necessary to reconstruct the original signal (sinewave signal at index 1 on Figure 21) are lower for a sigma-delta modulated signal than for a PWM modulated signal. The low-pass filter (analog filter) must be designed with a cut-off frequency slightly higher than the useful analog bandwidth of the original signal to be observed, and must be sharp enough to sufficiently suppress all the higher frequency components resulting from the signal modulation. Because the PWM signal has more unwanted energy concentrated at lower frequency than the sigma-delta modulated signal, the low pass analog filter must be sharper (higher order analog filter).

Another particularity of the sigma-delta modulated signal is that the quantization noise on the lower part of the spectrum is almost constant and independent from the input signal resolution whereas for a PWM modulated signal, a degradation of the quantization noise affects the entire spectrum, and predominately the first harmonic. This higher sensitivity of the PWM modulated signal to a degradation of the quantization noise is put in evidence by decreasing the input signal magnitude from 95% of full scale (Figure 21) down to 10% of full scale (Figure 22).

![](images/e0f1ee7d19d1f05f4329a742be2b1c27d431400100ac8142d221c338d1cb92fd.jpg)  
Figure 22. Spectrum of sigma-delta signal and PwM signal with signal amplitude reduced to 10% of full scale

# 4.3.5 High order filters operation

This simulation is provided in the sixth worksheet of [TUTORIAL]. It shows how it is possible to increase the filter output resolution by the technique of multiple averaging of the same data (principle of the high order filters).

For this simulation the averaging period is 10 samples (FOSR=10). Over the averaging period the input signal consists of a single pulse (one sample at 1 and the nine other samples at 0). Multiple averaging is performed. Two different cases are observed (see Figure 23):

1. Equidistant pulses occurring at 10th, 0th and 30t sample. This situation correspond to a constant density signal.   
2. Non-equidistant pulses occurring at 10th, 19th, 9th sample. This situation correspond to a signal with varying density.

![](images/15468b0ab2ae6c163c87bbcb053fc48b5e40ac9f7481ac7da504606fb73f65a8.jpg)

The results are presented for both input signal cases, and for 1, 2 or 3 averaging (similar to filter orders FORD=1, FORD=2, FORD=3). The final output is sampled at every 10th sample period (end of average period).

In the first case, since the input pulses are at equidistant intervals (every 10th sample), the output (sampled at 10th, 20th, 30th sample) is always 1.00, whatever the filter order.

In the second case, the input pulses e a little bt closer (pulses at 0h,  and h u Ip in the first case. This is because it performs averaging over one period only (10 samples). That means the first order filter is not able to detect changes in pulse density (or a filter with higher FOSR must be designed, with slower data rate).

The double averaging is a bit different. The first valid result is present on the output after the ial sample.The results from this double averagig rresult aftr period 1.00 (result after 3rd period). That means the second order filter is able to detect the increase of pulse density during the  averaging period of the signal and the decrease o the pulse density during the 3d averaging period.

The triple averaging gives even more precision. The first valid result is present on the output o final sample. The results from this triple averaging is.8 (result after 3d period). That means the third order filter gives even more precision on the pulse density.

# 4.3.6 Delta-sigma DAC simulation

This simulation is provided in the seventh worksheet of [TUTORIAL]. The sigma-delta modulation can be used not only for ADC conversion but also for DAC conversion. In this case, all analog blocks of the sigma-delta modulator diagram (see Figure 4: Sigma-delta modulation principle) are replaced by their digital equivalent (Figure 24).

![](images/69be628b717d1974f1558bbde2a2c47cdb779fafa683bdb2b5308c72f67265a3.jpg)  
Figure 24. First order delta-sigma DAC principle

MSv43891V1

Her  arie blockeig

C The "Subtraction" block is a digital operation.   
• The "Integrator" block is also a simple accumulate operation (sum of incoming bits). The "Comparator" block is a digital comparator. It determines the sign of the digital data word coming from the integrator (most significant bit = sign bit). The "Bit fll" block is the equivalent of the 1-bit DAC used in Figure 4: Sigma-delta modulation principle. It is replaced by an ADC which output is ±digital_reference_word according the sign provided by the comparator output. The magnitude of "digital_reference_word" should correspond to the input range of the digital signal into the comparator (equivalent to +Vref, -Vref for sigma-delta converter). The "Low pass filter" block is an analog filter which performs analog filtering of the fast 1-bit digital stream. The fast 1-bit digital stream represents the sigma-delta signal and in this case is built from the parallel N-bit width digital input signal (delta-sigma modulator). The 1-bit digital stream has the same properties as a 1-bit digital stream in the sigma-delta modulator (noise shaping) and can be filtered with a simpler analog filter (with respect to PWM signal).

The simulation of this delta-sigma DAC gets a digitized sinewave signal with amplitude +/-5 as an input (see "Digital input" pink-color signal on Figure 25). In a real application, the fast 1-bit digital stream output (blue signal on Figure 25) should undergo an analog low-pass filtering. For the need of the simulation, the analog low pass filtering is replaced by a digital Sincx filter.

![](images/58e91d18063330a1a8f4dacb04d43bea17fbbcf2e7b9e3b101875525ba9bc29a.jpg)  
Figure 25. Delta-sigma DAC simulation

The final delta-sigma DAC output (see the various order outputs on Figure 25) show a quite well reconstructed "analog" sinewave despite the digital input sinewave quantization uses only 11 discrete levels [-5,., +5]).

Once again the advantage of using a sigma-delta versus a PwM modulation is a simpler low-pass filtering (analog in the case of the DAC) of the output signal. This is for the same reason as the one developed in Section 4.3.4: Noise shaping of sigma-delta modulation.

# 4.3.7 High pass filter simulation

This simulation is provided in the eighth worksheet of [TUTORIAL]. High-pass filters are useful in many applications where the DC component and/or low frequency noise need to be removed from the input signal (audio applications including static pressure changes in microphone output, AC energy measurement, DC offset which vary with temperature, .. ).

The DFSDM does not implement any high pass filtering but it can be easily implemented in software as a post processing over the DFSDM sampled data (as an alternative to the use of an external hardware high-pass filter).

The high-pass filter used in the simulation is modeled by the following equation:

![](images/5d916c77daf1ba51f70f9c64221bce8c9651627b76b0ada738292daf8e555572.jpg)

with

y(n): = "filteredvalue" in the simulation (filter output) cf: = "coeff in the simulation (filter cutoff frequency) y(n-1)= "last_filtered_value" in the simulation (previous filter output) x(n) = "sample" in the simulation (filter input sample) x(n-1) = "last_sample" in the simulation (filter previous input sample)

The complexity of this filter reduces to one multiplication, two additions and one shift operation (/256).

For the simulation a sinewave with a decreasing DC offset is applied to the high-pass filter (light blue curve in Figure 26).

![](images/165c535d97d6a965ecd9f27991aacfb10fb058f968f4f5448f2b56d96701f2fc.jpg)  
Figure 26. HP filter simulation

The high-pass filter output is represented by the dark blue line in Figure 26. After an adaptation period, the high-pass filter suppresses the DC and the low frequency content. The speed of adaptation depends on the "coeff" value (cut-off frequency of the filter).

# 4.4 Additional functions in DFSDM

# 4.4.1 Digital microphones (MEMS) support

Standardization in the domain of audio application has specified a PDM modulation (pulse density modulation) that is a common output format for digital microphones. A PDM signal is equivalent to a sigma-delta modulated signal and is therefore supported by the DFSDM.

Digital microphones are MEMS devices (micro electro mechanical systems) which are manufactured using semiconductor type of technology. The active actuator of such microphones consists in a membrane and a pair of micro electrodes. One of the electrode is fixed, the other one is incorporated within the membrane. As the air pressure (sound) is applied to the membrane, it moves the mobile electrode away from its default position and produces a change of capacity between both electrodes. The induced signal is processed by built-in electronic and output as a PDM modulated signal (pulse density modulation).

The digital microphones require an external clock signal (microphone CLK input signal) and data are sent over a DATA output line as a PDM modulated signal. The clock speed is usually in the range 1 to 3.2 MHz. The clock signal is provided by the DFSDM_CKOUT output signal and defines the microphone output data rate into the DFSDM. A schematic of a typical connection between a stereo digital microphone and the DFSDM is provided on Figure 28.

The DFSDM allows to connect 2 microphones in parallel through one single line (stereo configuration: left and right channel). The data and clock signals are common for both microphones. The clock signal is distributed from DFSDM_CKOUT pin to the left and right microphones. The output data signals from both microphones are multiplexed on the same wire: the left microphone provides data on the rising clock edge and the right microphone provides data on the falling clock edge (see Figure 27). The configuration of microphone for left or right channel is usually done configuring a pin on the microphone (L/R selection pin).

![](images/caff86331e77425f29c671da0fe44b5aba5e74a9d342b9281d0d890942866f4e.jpg)  
Figure 27. MEMS microphone outputs (L and R channel)

![](images/18739561dba7b34e951d2c2bbb5703c0f6eec3dcd406f66994575e4404a09249.jpg)  
Figure 28. MEMS microphone connection to DFSDM (stereo support)

Direct input, falling edge sampling (R data).

Redirected from next channel, rising edge sampling (L data).

The separation of the two microphone signals on the DATA wire is performed by the DFSDM. The input to DFSDM channel x can be redirected in order to take the same input as channel (x+1). Then channel x is configured to sample data on rising edge and channel (x+1) is configured to sample data on falling edge. The clock signal for both channels is the same and internally connected to DFSDM_CKOUT signal. With such configuration, channel x is receiving data from left microphone and channel (x+1) is receiving data from right microphone. Both channels feed their own digital filters which eventually output two separate parallel data flows for left and right microphone channels. See Figure 28 for a complete diagram of a stereo microphone application using the DFSDM.

# 4.4.2 Beamforming support

Beamforming is a technique giving to an array of fixed multi-directional sensors the ability to favor the signals coming from a particular direction (array of microphones in the example below). The preferred direction can be changed by firmware (without changing the position of the sensors).

In the example below, an array of microphones are positioned on a line with equidistant spacing (see Figure 29). An audio source is placed in front of the microphone array at an arbitrary angle, while at the same time unwanted noise and interferences are present all around. If signals from all microphones are simply summed together then only the sounds coming perpendicularly to the array are coherently summed (and therefore amplified). The sounds coming from non-perpendicular directions are not coherently summed.

![](images/26c29bc77ed743844c766b8d0753bccd050fd6934d3b5a83ff1753106a3fe67e.jpg)  
Figure 29. Beamforming principle

MSv43893V1

In order to amplify the signals coming from another direction than perpendicular, one solution would be to mechanically rotate the microphone array, another solution consists in adding a specific delay to each microphone in the array, so that the various propagation delays of the useful signal arriving through each microphone are all compensated at the input of the adder. When the delay lines of all microphone are adjusted, only the sounds coming from the direction of the useful source are in phase and amplified (coherent combination), the sounds coming with a different angle are less amplified (incoherent combination) (see Figure 29).

The above description of beam forming algorithm is a introduction (simplified view). More elaborated algorithm can be implemented, providing even better performances.

Beamforming can be achieved with the DFSDM as follows. The DFSDM is able to sense signals coming from several microphones and process them separately to provide parallel outputs samples. The output samples from the different microphones are stored into separate data buffers in the microcontroller memory (for example 4 memory buffers from 4 microphones). The samples are then summed together by the microcontroller in order to provide the final output. The delay line is realized in 2 steps:

1. Coarse step: a DFSDM output buffer (for a given microphone) can be shifted with respect to another by a given number of samples (one sample corresponds to a delay , 22.05kHz, 16kHz, .. ). A shift of 1 sample corresponds to a propagation distance of the sound in the air of s = v / fdatarate (v is the sound speed in air \~343m/s). Example of coarse step:

fdatarate = 44.1 kHz: s = 343 / 44100 = \~7.8 mm fdatarate = 16 kHz: s = 343 / 16000 = \~21.4 mm

2. Fine step: in order to support short distances between microphones in the array and to be able to fine tune the angle of the preferred sound source, a finer step is required. This is achieved by shifting samples on the 1-bit data stream between the microphone and the DFSDM rather than shifting DFSDM output samples in memory. The input 1-bit samples are sampled at PDM frequency. Here are examples of fine step distances:

fPDM = 3 MHz: s = 343ms-1 / 3000000Hz = \~0.11mm fPDM = 200 kHz: s = 343ms-1 / 200000Hz = \~1.7mm

This range of values is compatible with the fine tuning of the preferred angle for sound reception even for miniature microphone arrays.

The DFSDM fine step circuitry used to fine tune beamforming is not based on delay lines but consists in skipping some samples of the input 1-bit stream. Some of the 1-bit samples coming from the serial transceiver are masked (by clock signal gating) and are not sent to digital filter. The principle based on skipping clock pulses is shown on Figure 30.

![](images/ab6086cf717114471f75ac428492d793c12b05f154ff2d95a11ead7861ed096e.jpg)  
Figure 30. Pulse skipping implementation for beamforming

Figure 31 provides an example that illustrates the pulse skipping mechanism and its similarity with a delay line.

Figure 31. Pulse skipping example (FOSR=8)   

<table><tr><td rowspan=1 colspan=25>Input samples (no sample skipping applied):</td></tr><tr><td rowspan=1 colspan=1>sample#</td><td rowspan=1 colspan=24>3 4 5 6 7 8 910 11 12 13 14 15 16 17 18 19 20 21 22 23 24</td></tr><tr><td rowspan=1 colspan=1>Left</td><td rowspan=1 colspan=8>S1 S2 S3 S4 S5 S6 S7 S8</td><td rowspan=1 colspan=8>S9 S10 S11 S12 S13 S14 S15 S16</td><td rowspan=1 colspan=8>S17 S18 S19 S20 S21 S22 S23 S24</td></tr><tr><td rowspan=1 colspan=1>Right</td><td rowspan=1 colspan=8>S1 S2 S3 S4 S5 S6 S7 S8</td><td rowspan=1 colspan=8>S9 S10 S11 S12 S13 S14 S15 S16</td><td rowspan=1 colspan=8>S17 S18 S19 S20 S21 S22 S23 S24</td></tr><tr><td rowspan=1 colspan=1></td><td rowspan=1 colspan=1></td><td rowspan=1 colspan=1></td><td rowspan=1 colspan=1></td><td rowspan=1 colspan=1></td><td rowspan=1 colspan=1></td><td rowspan=1 colspan=1></td><td rowspan=1 colspan=1></td><td rowspan=1 colspan=1></td><td rowspan=1 colspan=2></td><td rowspan=1 colspan=1></td><td rowspan=1 colspan=1></td><td rowspan=1 colspan=1></td><td rowspan=1 colspan=1></td><td rowspan=1 colspan=1></td><td rowspan=1 colspan=1></td><td rowspan=1 colspan=1></td><td rowspan=1 colspan=1></td><td rowspan=1 colspan=1></td><td rowspan=1 colspan=1></td><td rowspan=1 colspan=1></td><td rowspan=1 colspan=1></td><td rowspan=1 colspan=1></td><td rowspan=1 colspan=1></td></tr><tr><td rowspan=1 colspan=1>Output samples (FOSR=8):</td><td rowspan=1 colspan=1></td><td rowspan=1 colspan=1></td><td rowspan=1 colspan=1></td><td rowspan=1 colspan=1></td><td rowspan=1 colspan=1></td><td rowspan=1 colspan=1></td><td rowspan=1 colspan=1></td><td rowspan=1 colspan=1></td><td rowspan=1 colspan=2></td><td rowspan=1 colspan=1></td><td rowspan=1 colspan=1></td><td rowspan=1 colspan=1></td><td rowspan=1 colspan=1></td><td rowspan=1 colspan=1></td><td rowspan=1 colspan=1></td><td rowspan=1 colspan=1></td><td rowspan=1 colspan=1></td><td rowspan=1 colspan=1></td><td rowspan=1 colspan=1></td><td rowspan=1 colspan=1></td><td rowspan=1 colspan=1></td><td rowspan=1 colspan=1></td><td rowspan=1 colspan=1></td></tr><tr><td rowspan=1 colspan=1>sample#</td><td rowspan=1 colspan=8></td><td rowspan=1 colspan=8></td><td rowspan=1 colspan=8>3</td></tr><tr><td rowspan=1 colspan=1>Left</td><td rowspan=1 colspan=8>S1 S2 S3 S4 S5 S6 S7 S8</td><td rowspan=1 colspan=8>S9 S10 S11 S12 S13 S14 S15 S16</td><td rowspan=1 colspan=8>S17 S18 S19 S20 S21 S22 S23 S24</td></tr><tr><td rowspan=1 colspan=1>Right</td><td rowspan=1 colspan=8>S1 S2 S3 S4 S5 S6 S7 S8</td><td rowspan=1 colspan=8>S9 S10 S11 S12 S13 S14 S15 S16</td><td rowspan=1 colspan=8>S17 S18 S19 S20 S21 S22 S23 S24</td></tr><tr><td rowspan=1 colspan=1></td><td rowspan=1 colspan=8>Right sample built from same input samples numberi on Lehannel delay line nRightchannel</td><td rowspan=1 colspan=8>Right sample built from same input samples numberlike on Left channel =&gt; no delay line on Rightchannel</td><td rowspan=1 colspan=8>Right sample buit from same input samples numberlike on Left channel =&gt; no delay line on Rightchannel</td></tr><tr><td rowspan=1 colspan=1></td><td rowspan=1 colspan=1></td><td rowspan=1 colspan=1></td><td rowspan=1 colspan=1></td><td rowspan=1 colspan=1></td><td rowspan=1 colspan=1></td><td rowspan=1 colspan=1></td><td rowspan=1 colspan=1></td><td rowspan=1 colspan=1></td><td rowspan=1 colspan=1></td><td rowspan=1 colspan=1></td><td rowspan=1 colspan=1></td><td rowspan=1 colspan=1></td><td rowspan=1 colspan=1></td><td rowspan=1 colspan=1></td><td rowspan=1 colspan=1></td><td rowspan=1 colspan=1></td><td rowspan=1 colspan=1></td><td rowspan=1 colspan=1></td><td rowspan=1 colspan=1></td><td rowspan=1 colspan=1></td><td rowspan=1 colspan=1></td><td rowspan=1 colspan=1></td><td rowspan=1 colspan=1></td><td rowspan=1 colspan=1></td></tr><tr><td rowspan=1 colspan=1></td><td rowspan=1 colspan=1></td><td rowspan=1 colspan=1></td><td rowspan=1 colspan=1></td><td rowspan=1 colspan=1></td><td rowspan=1 colspan=1></td><td rowspan=1 colspan=1></td><td rowspan=1 colspan=1></td><td rowspan=1 colspan=1></td><td rowspan=1 colspan=1></td><td rowspan=1 colspan=1></td><td rowspan=1 colspan=1></td><td rowspan=1 colspan=1></td><td rowspan=1 colspan=1></td><td rowspan=1 colspan=1></td><td rowspan=1 colspan=1></td><td rowspan=1 colspan=1></td><td rowspan=1 colspan=1></td><td rowspan=1 colspan=1></td><td rowspan=1 colspan=1></td><td rowspan=1 colspan=1></td><td rowspan=1 colspan=1></td><td rowspan=1 colspan=1></td><td rowspan=1 colspan=1></td><td rowspan=1 colspan=1></td></tr><tr><td rowspan=1 colspan=1></td><td rowspan=1 colspan=1></td><td rowspan=1 colspan=1></td><td rowspan=1 colspan=1></td><td rowspan=1 colspan=1></td><td rowspan=1 colspan=1></td><td rowspan=1 colspan=1></td><td rowspan=1 colspan=1></td><td rowspan=1 colspan=1></td><td rowspan=1 colspan=1></td><td rowspan=1 colspan=1></td><td rowspan=1 colspan=1></td><td rowspan=1 colspan=1></td><td rowspan=1 colspan=1></td><td rowspan=1 colspan=1></td><td rowspan=1 colspan=1></td><td rowspan=1 colspan=1></td><td rowspan=1 colspan=1></td><td rowspan=1 colspan=1></td><td rowspan=1 colspan=1></td><td rowspan=1 colspan=1></td><td rowspan=1 colspan=1></td><td rowspan=1 colspan=1></td><td rowspan=1 colspan=1></td><td rowspan=1 colspan=1></td></tr><tr><td rowspan=1 colspan=1>Input samples (with 3 samples skipped on Left channel):</td><td rowspan=1 colspan=2>ipped on</td><td rowspan=1 colspan=1>eft c</td><td rowspan=1 colspan=2>hannel):</td><td rowspan=1 colspan=1></td><td rowspan=1 colspan=2></td><td rowspan=1 colspan=5></td><td rowspan=1 colspan=3></td><td rowspan=1 colspan=6></td><td rowspan=1 colspan=1></td><td rowspan=1 colspan=1></td></tr><tr><td rowspan=1 colspan=1>sample#</td><td rowspan=1 colspan=8>2  3  4  5</td><td rowspan=1 colspan=16>6 7 8 9 10 11 12 13 14 15 16 17 18 19 20 21 22 23 24</td></tr><tr><td rowspan=1 colspan=1>Left</td><td rowspan=1 colspan=8>S1 S2</td><td rowspan=1 colspan=8>S9- - - S13 S14 S15 S16</td><td rowspan=1 colspan=8>S13 S14 S15 S16 S17 S18 S19 S20 S21 S22 S23 S24</td></tr><tr><td rowspan=1 colspan=1>Right (3 samples delay applied)</td><td rowspan=1 colspan=8>S1 S2 S3 S4 S5 S6 S7 S8</td><td rowspan=1 colspan=8>S9. S10 S11 S12 S13 S14 S15 S16</td><td rowspan=1 colspan=8>S17 S18 S19 S20 S21 S22 S23 S24</td></tr><tr><td rowspan=2 colspan=1>Output samples (FOSR=8):</td><td rowspan=1 colspan=1></td><td rowspan=1 colspan=1></td><td rowspan=1 colspan=1></td><td rowspan=1 colspan=1></td><td rowspan=1 colspan=1></td><td rowspan=1 colspan=1></td><td rowspan=1 colspan=2></td><td rowspan=1 colspan=2></td><td rowspan=1 colspan=1></td><td rowspan=1 colspan=1></td><td rowspan=1 colspan=1></td><td rowspan=1 colspan=1></td><td rowspan=1 colspan=2></td><td rowspan=1 colspan=3></td><td rowspan=1 colspan=1></td><td rowspan=1 colspan=1></td><td rowspan=1 colspan=1></td><td rowspan=1 colspan=1></td><td rowspan=1 colspan=1></td></tr><tr><td rowspan=1 colspan=1></td><td rowspan=1 colspan=1></td><td rowspan=1 colspan=1></td><td rowspan=1 colspan=1></td><td rowspan=1 colspan=1></td><td rowspan=1 colspan=1></td><td rowspan=1 colspan=2></td><td rowspan=1 colspan=2></td><td rowspan=1 colspan=1></td><td rowspan=1 colspan=1></td><td rowspan=1 colspan=1></td><td rowspan=1 colspan=1></td><td rowspan=1 colspan=2></td><td rowspan=1 colspan=3></td><td rowspan=1 colspan=1></td><td rowspan=1 colspan=1></td><td rowspan=1 colspan=1></td><td rowspan=1 colspan=1></td><td rowspan=1 colspan=1></td></tr><tr><td rowspan=1 colspan=1>sample#</td><td rowspan=1 colspan=8>1</td><td rowspan=1 colspan=8>2</td><td rowspan=1 colspan=8>3</td></tr><tr><td rowspan=1 colspan=1>Left</td><td rowspan=1 colspan=8>S1 S2 S3 S4</td><td rowspan=1 colspan=8>S9 S13 S14 S15 S16 S17 S18 S19</td><td rowspan=1 colspan=8>S20 S21 S22 S23 S24 S25 S26 S27</td></tr><tr><td rowspan=1 colspan=1>Right</td><td rowspan=1 colspan=8>S1 S2 S3 S4 S5 S6 S7 S8</td><td rowspan=1 colspan=8>S9. S10 S11.S12 S13 S14 S15 S16</td><td rowspan=1 colspan=8>S17 S18 S19 S20 S21 S22 S23 S24</td></tr><tr><td rowspan=1 colspan=1></td><td rowspan=1 colspan=8>Right sample buit from same input smples umerlike on Left channel =&gt; no delay line on Rightchannel</td><td rowspan=1 colspan=8>Right sample buit from older input samples =&gt; likedelay line on Right channel</td><td rowspan=1 colspan=8>Right sample buit from older input samples =&gt; likedelay line on Right channel</td></tr></table>

The top part of Figure 31 represents the normal operation, without clock skipping applied. Each output sample is built from 8 input samples (FOSR=8). For beam forming several DFSDM filters need to be started simultaneously.

On the bottom part of Figure 31 samples S10, S11, S12 have been skipped on the Left channel. The filter (with configuration: FOSR=8) waits for 3 more samples in order to get 8 complete 1-bit samples for each channel and be able to build one output sample. From the filter output prospective, it seems like the Right channel uses older 1-bit input samples than the Left channel for the same final output sample index. This is the same behavior as if the Right channel would have a 3-samples delay line (the delay line buffers holding the last 3 samples).

The above description of beam forming algorithm is a introduction (simplified view). More elaborated algorithm can be implemented, providing even better performances.

# 1.4.3 Audio clock support  independent clock operation

The DFSDM can clock an external sigma-delta modulator through a clock signal provided on the DFSDM_CKOUT pin. The clock frequency on this pin determines the input sampling frequency from which depends also the output data rate frequency. It is possible to select among the following sources to drive the DFSDM_CKOUT:

DFSDM clock: APB clock System clock (independent from APB clock divider)   
PLL clock (audio PLL used for I2S)

The frequency from the selected clock source is divided by a factor in the range 2-256 (predivider ratio set according CKOUTDIV field in DFSDM_CHyCFGR1 register) in order tc provide the DFSDM_CKOUT frequency.

In order to achieve a fine tuning of the DFSDM_CKOUT frequency, the PLL (providing both a multiplication and a division factor) must be selected as clock source. This is the appropriate selection for audio applications that require an accurate sampling frequency.

The DFSDM peripheral itself (transceivers, filters, additional functions) is using the APB clock or the system clock for digital processing. This "processing" frequency should be 4 times faster than the input sampling frequency (or 6 times if Manchester coding is used).

In order to save power consumption, both the sampling frequency and the processing frequency should be configured with the minimum values required by the application.

# 4.5 DFSDM power consumption optimization

The DFSDM consumption depends on:

Enabled blocks:

Number of enabled channels   
Number of enabled filters   
Number of enabled features (analog watchdog, short circuit detector)

Clock speed:

Transceivers Digital filters (+ additional functions)

In order to optimize the power consumption, only the required blocks should be enabled when needed (transceivers, filters, additional functions) and the minimum clock speed to achieve the required input and output data rate should be used.

# 4.5.1 Power optimization in Sleep mode

The DFSDM may be used in Sleep mode. In this case, the DFSDM is typically used to monitor analog signals (analog watchdog enabled) and to wake up the CPU if an analog threshold is reached.

Examples of such applications are baby monitoring or broken glass detection where the CPU is almost always in sleep mode and the DFSDM is monitoring the sound level through the analog watchdog. If the sound threshold is reached, the CPU is woken up by the DFSDM analog watchdog interrupt, the DFSDM collects the captured data and the CPU performs analysis on the data collected by the DFSDM (to assess if it is realy a baby sound or a broken glass sound). During the sleep mode it is not required that the DFSDM collects the data, only the analog watchdog functionality should be turned ON in order to optimize power consumption.

Here is a example of DFSDM and MCU configuration for low power operation (sound detection):

Clocks:

Disable all peripherals except DFSDM   
Use system clock at minimum frequency for DFSDM operation. (example: 4 MHz, use internal MSl oscillator to reduce even more consumption)   
Reduce AHB and APB clocks to minimum because there is no need to access the peripherals during Sleep mode. Use high AHB and APB predividers (example: AHB predivider = 512, AHB clock = 4 MHz/512 = 7.8 kHz).   
Use system clock (example: 4 MHz) for the DFSDM because the APB clock is too slow for digital filter processing.   
Sampling clock for digital MEMS microphone should be less than DFSDM clock / 4 (example: 1 MHz is appropriate for microphone operation).

DFSDM:

Configure the filter for appropriate output data rate (example: 16 kHz).   
Set the analog watchdog for monitoring output data and set appropriate thresholds for sound detection.   
Disable overrun errors of final data because data are not collected from DFSDM (only analog watchdog is working).

After wakeup (interrupt from analog watchdog):

Set back AHB, APB clocks (predividers) for high speed operation to speed up DFSDM communication and data transfer (example: AHB predivider = 1, AHB clock = 4 MHz).   
Optionally reconfigure DFSDM for higher output data rate for better sound recognition analysis (example: 44.1 kHz).   
Start data collection from DFSDM into memory buffers (example: DMA data transfer).   
Perform sound recognition over each data buffer (example: FFT analysis). If a critical sound is detected, perform the necessary action (invoke alarm). If tr sound was not critical (or no more sound is detected after a while) then go to th Sleep operation again and wait for next wakeup from analog watchdog.

With the above DFSDM scenario ongoing, the increase of the microcontroller power consumption (due to DFSDM activity) is limited to roughly a factor 2 (with respect to the consumption in a strict sleep mode without any DFSDM activity and same system clock frequency).

# DFSDM peripheral configuration tutorial

The DFSDM functionality is similar to an A/D converter that would have an external analog front-end part. The DFSDM offers a lot of flexibility but requires a bit of methodology to navigate through all the settings. The following tutorial helps the user to configure the DFSDM according the application requirements for A/D conversion.

# 5.1 Configuration introduction

The basic application parameters for A/D conversion are:

• Input analog range (sigma-delta modulator property)   
• Minimum output data rate   
• Data rate precision setting   
• Minimum output data resolution   
• Number of collected channels (per ADC)

Additional functionality: Analog watchdog Short circuit detector

MA,irut lg

Application related properties impacting the DFSDM configuration:

• System clock range   
• Supply voltage   
• Consumption limitation Used sigma-delta converter (or digital microphone) properties: clock speed range, input analog range, order of sigma-delta modulator.

In the next sections, the tutorial goes through the configuration of the various DFSDM parts in order to achieve the application requirements.

# 5.2 Clocks configuration

The DFSDM clock selection is guided by the data requirements:

Minimum output data rate • Data rate precision • Minimum output data resolution

The goal is to set the filter parameters and the input sampling clock rate in order to reach the output data rate.

The input sampling clock selection is driven by the sigma-delta modulator (or digital microphone) characteristics:

Please refer to Table 2 below providing examples of clocks configuration for two different applications.

# 5.3 Transceivers

# 5.3.1 Serial transceivers configuration

The serial transceivers convert the data present on the input pins (DFSDM_DATIN and DFSDM_CKIN) and provide them to the filters. The configuration of the transceivers depends on the characteristics of the external device(s) connected to the DFSDM (sigmadelta modulator or digital microphone).

The Table 2 below provides examples of DFSDM configurations for two different applications:

# Application 1:

Application: temperature measurement consisting in measuring voltage and current over a Pt100 sensor and determining the Pt100 sensor resistance/temperature. The temperature measurement is triggered by a timer every 1 second. External device: dual external sigma delta modulator STPMS2 for voltage and current channel measurement.

Physical connection:

The STPMS2 uses only one SPI line (pins: CLK, DAT).   
The STPMS2 CLK pin is driven by DFSDM_CKOUT pin   
The STPMS2 DAT pin is connected to DFSDM_DATIN1 (serial data input on channel 1 pin, the channel 0 input is redirected to channel 1 pin, then signal on DATIN1 is connected to both channel 0 and channel 1).   
DFSDM_CKIN1 pin (serial clock input on channel 1) is not used. Data are sampled using internally redirected clock from CKOUT pin (SPICKSEL [1:0] = 1).

Post processing:

Data from channel 0 (U, voltage) are processed by filter 0.   
Data from channel 1 (I, current) are processed by filter 1.   
The resistance of Pt100 sensor is determined in firmware as R = U/l and is used to extrapolate the Pt100 sensor temperature.

# Application 2:

Application: audio recording at 48 kHz data rate. √ External device: MEMS digital microphone MP34DT01-M.

Physical connection:

MP34DT01-M has one data line (pins: CLK, DOUT).   
The MP34DT01-M CLK pin is driven by DFSDM_CKOUT.   
The MP34DTO1-M DOUT pin is connected to DFSDM_DATINO (serial data input on channel 0).

Post processing:

Data from channel 0 (microphone) are processed by filter 0.   
The output stream at a datarate of 48 kHz is stored in a RAM buffer by the DMA, in continuous mode.

Table 2. DFSDM application examples   
20   
  

<table><tr><td rowspan=1 colspan=2>Parameters</td><td rowspan=1 colspan=2>Application 1: temperature measurement</td><td rowspan=1 colspan=2>Application 2: audio sampling</td></tr><tr><td rowspan=1 colspan=1>Description</td><td rowspan=1 colspan=1>Options</td><td rowspan=1 colspan=1>Setting(1)</td><td rowspan=1 colspan=1>Notes</td><td rowspan=1 colspan=1>Setting(1)</td><td rowspan=1 colspan=1>Notes</td></tr><tr><td rowspan=2 colspan=1>Selection ofthe serialprotocol(SITP[1:0])</td><td rowspan=1 colspan=1>SPI type</td><td rowspan=1 colspan=1>X</td><td rowspan=1 colspan=1>STPMS2 uses SPI communication</td><td rowspan=1 colspan=1>X</td><td rowspan=1 colspan=1>MP34DT01-M uses SPI type protocol.</td></tr><tr><td rowspan=1 colspan=1>Manchestertype</td><td rowspan=1 colspan=1>-</td><td rowspan=1 colspan=1></td><td rowspan=1 colspan=1>-</td><td rowspan=1 colspan=1></td></tr><tr><td rowspan=2 colspan=1>Clockmaster</td><td rowspan=1 colspan=1>DFSDM(2)</td><td rowspan=1 colspan=1>X</td><td rowspan=1 colspan=1>STPMS2 has clock input pin</td><td rowspan=1 colspan=1>X</td><td rowspan=1 colspan=1>MP34DT01-M needs clock input.</td></tr><tr><td rowspan=1 colspan=1>Externaldevice(3)</td><td rowspan=1 colspan=1>-</td><td rowspan=1 colspan=1></td><td rowspan=1 colspan=1>-</td><td rowspan=1 colspan=1></td></tr><tr><td rowspan=2 colspan=1>Activesamplingedge</td><td rowspan=1 colspan=1>Rising edge</td><td rowspan=1 colspan=1>-</td><td rowspan=1 colspan=1>current stream active on rising edge</td><td rowspan=1 colspan=1>X</td><td rowspan=1 colspan=1>MP34DT01-M has pin &quot;L/R&quot; at GND level - risingedge is active.</td></tr><tr><td rowspan=1 colspan=1>Falling edge</td><td rowspan=1 colspan=1>-</td><td rowspan=1 colspan=1>voltage stream active on falling edge</td><td rowspan=1 colspan=1>-</td><td rowspan=1 colspan=1></td></tr><tr><td rowspan=1 colspan=1>Clock source</td><td rowspan=1 colspan=1>APB clockSystem clockPLL clock</td><td rowspan=1 colspan=1>Systemcclock(fHS116)</td><td rowspan=2 colspan=1>fckIN requirement 2 MHz(4)fCKIN configuration:CIN = HS1/COUTDIV + fHSI16 = 16 MHzCKHOUTDIV = 7</td><td rowspan=1 colspan=1>PLL clock</td><td rowspan=2 colspan=1>fCKIN requirement 3.072 MHz(5)fCKIN configuration:fCKI = fHSE * N(Q*(CKOTDIV+1)) withHSE = 16 MHz (crystal - precise clockN =48Q = 2CKOUTDIV = 124</td></tr><tr><td rowspan=1 colspan=1>Input clockfrequency</td><td rowspan=1 colspan=1>fckIn/fckouT</td><td rowspan=1 colspan=1>2 MHz</td><td rowspan=1 colspan=1>3.072 MHz</td></tr><tr><td rowspan=1 colspan=1>Number ofdata streams</td><td rowspan=1 colspan=1>One stream(6)</td><td rowspan=1 colspan=1>-</td><td rowspan=1 colspan=1>Also supported by STPMS2 but requires onemore wire/pin</td><td rowspan=1 colspan=1>X</td><td rowspan=1 colspan=1>Mono microphone is used.</td></tr><tr><td rowspan=1 colspan=1>sent overone serialline</td><td rowspan=1 colspan=1>Two streams(7)</td><td rowspan=1 colspan=1>X</td><td rowspan=1 colspan=1>A common wire for current and voltage signal isused in this example. Only one pin/wire isnecessary.</td><td rowspan=1 colspan=1>-</td><td rowspan=1 colspan=1></td></tr><tr><td rowspan=2 colspan=1>Clockaccuracy</td><td rowspan=1 colspan=1>Low accuracy</td><td rowspan=1 colspan=1>X</td><td rowspan=1 colspan=1>No need of precise clock - temperaturemeasurement is triggered each second by timer.Clock signal based on DFSDM clock (16MHz):CKOUTSRC = 0</td><td rowspan=1 colspan=1>-</td><td rowspan=1 colspan=1></td></tr><tr><td rowspan=1 colspan=1>High accuracy</td><td rowspan=1 colspan=1>-</td><td rowspan=1 colspan=1></td><td rowspan=1 colspan=1>X</td><td rowspan=1 colspan=1>Required precise 48 kHz data rate (audiostandard).</td></tr></table>

Device requires external clock (clock input into device).

Device uses internal clock (clock output by the device).

4STPMS2 clock input range: 1 to 4.915 MHz.

fcKIN = datarate \* FOSR \* IOSR with datarate = 48 kHz, FOSR = 64, continuous mode.

One stream sent (only one sampling edge active).

e  iv coc  .

# 5.3.2 Parallel transceivers

The parallel transceivers offer an alternative consisting in providing 16-bit wide data into the digital filter directly from internal microcontroller data sources.

The parallel transceivers consist in a set of 32-bit (2x16-bit) parallel input registers feeding the digital filter. There is one 32-bit parallel input register (divided into 2x16-bit) for each serial input channel. The DATMPX[1:0] bits in DFSDM_CHyCFGR1 register allow to select the filter input from either the serial input or the 16-bit parallel input. If DATMPX[1:0] = 0 then data are taken from serial transceivers (as 1-bit serial stream) otherwise the data are taken from parallel transceivers (as 16-bit signed data).

Data can be written into parallel registers by the CPU, by the DMA (DATMPX[1:0]=2) or by the ADC (DATMPX[1:0]=1). Depending on the embedded ADC capability, some microcontrollers feature a dedicated fast internal 16-bit bus between ADC and parallel input registers.

Each channel has its own 32-bit parallel register which is divided into two 16-bit registers. It allows to use 32-bit accesses to those registers and write 2 input samples at each write access. The usage of upper and lower 16-bit samples in 32-bit registers depends on the selected "data packing operation mode" defined in field DATPACK[1:0]:

• Standard mode: only lower 16-bit sample is used Interleaved mode: both samples are used for the same channel (like a 2 samples FIFO buffer) Dual mode: the lower 16-bit sample is used as input for a given channel while the upper 16-bit sample is used as input for the next channel.

Writing one 16-bit sample into the parallel input register automatically generates one sampling clock signal for the digital filter which in turn automatically samples the parallel input register as next input to be processed. Therefore the final output data rate depends on the input data rate (CPU or DMA or ADC data transfer speed).

The parallel transceivers allow to perform fast low-pass filtering without CPU intervention. Here are 3 practical examples:

Post-processing of ADC samples

The ADC is used as data source.

The ADC is configured to be used with DFSDM.

The DFSDM configuration is as follows:

Parallel inputs selected from ADC: DATMPX[1:0]=1.   
The ADC is sending its outputs data over 16-bit internal bus directly into parallel registers (only lower 16-bit part is used). The data packing has no meaning in case of ADC data inputs and it is recommended to set DATPACK[1:0]=0.   
The DFSDM processes data according the setting of filter parameters (FOSR, FORD, IOSR) and then produces the final output data samples at a lower data rate. Example: averaging of data from ADC.

Post-processing of data stored in RAM memory buffer (for instance low-pass filtering of data from ADC after software high-pass filtering)

The parallel inputs are selected from the parallel input registers: DATMPX[1:0]=2.

The CPU can write data directly from a buffer to the parallel registers. Alternatively the DMA can be used to load data into the parallel input registers.

The data packing should be optimized according the application:

If data are stored in a buffer in 16-bit format, then DATPACK[1:0]=2 setting can be used to improve performance. In this case 2 consecutive samples can be written in one 32-bit transfer (FIFO buffer).   
If data are stored in a buffer in 16-bit format and each second sample is from another data source (for example odd samples corresponding to audio L channel and even samples corresponding to audio R channel) then DATPACK[1:0]=3 setting can be used to improve performance. In this case one sample pair can be written in one 32-bit transfer (write 2 samples into 2 different channels parallel input registers).

Post-processing of data from another communication peripheral: the analog data are transferred from the peripheral directly into the given parallel input register (DMA) and processed by the DFSDM to produce the final filtered samples. For instance an external ADC may be connected to the microcontroller SPI interface and the DFSDM used for low-pass filtering. In this case the setting of DFSDM is similar to case 2.

# 5.4 Filter

# 5.4.1 Sinc filter

The digital filter performs digital signal processing on data received by serial or parallel transceivers. Data can be in 1-bit format (serial transceivers) or in 16-bit signed integer format (parallel transceivers). Each sample received by the transceiver is automatically sampled by the digital filter for processing. According the digital filter configuration parameters, several input samples may be required until the first output data is available from the filter.

The filter implemented in the DFSDM is a low pass filter of the Sinc type (also known also as comb filter). The basic parameters for this filter are as follows:

FOSR: filter oversampling ratio - defines how many samples are processed together in the moving average. FOSR range is 1..1024.   
FORD: filter order - defines the number of iterations of the moving average. FORD range is 1..5.

The configuration of the filter depends on the application requirements and are discussed in the next 4 sub-sections:

# Low pass filtering characteristics

The filter transfer frequency characteristic is important for the application. The Sinc filter frequency characteristic for FORD = 1, 3 and 5 and for fixed FOSR = 8 is provided in Figure 32: Sinc filter frequency characteristic shape (a more general figure was introduced in Figure 19). The magnitude response curves in Figure 32 indicate the amount of rejection applied to the high frequency components of the signal, outside of the filter passband (from around -20dB rejection for FORD = 1 down to around -100 dB for FORD = 5). The higher the filter order, the better the higher frequencies suppression (low pass filter). There is a side effect of using high filter order that may affect the signal within the useful filter passband. This is illustrated by the "passband zoom" curves of Figure 32. The filter is not flat within the passband but applies a slight attenuation that increases with the frequency and the filter order. Depending on the useful frequency bandwidth of the analog input signal, this may affect the quality of the filtered signal. If necessary, this attenuation can be compensated by application of a software compensation filter on the final output data.

The notch frequencies are those discrete frequencies where the attenuation of the signal is maximum (see Figure 32: Sinc filter frequency characteristic shape). The first notch frequency (and all its harmonics) of the Sinc filter is independent of FORD and depends only sampling cloc and the elecd FOSR: noh = mplig / FOSR. Deceasing FOSR results in larger steps between notch frequencies.

In some applications, one can take advantage of the notch frequencies to better reject sources of noise with energy concentrated at a particular frequency. For instance if an application is sensitive to the 50 Hz mains frequency and its harmonics, it is recommended to tune the filters so that the first notch frequencies equals 50 Hz. With such configuration and filter tuning, it is possible to exploit very low signals in relatively high noise environment.

![](images/e7df6243cb1802c359c7d824eebe8963a0c0f499907971734b9133f79949a673.jpg)  
Figure 32. Sinc filter frequency characteristic shape

# Output data resolution

A consequence of the Sinc filter operation (moving average) is to increase the resolution of the sampled signal (by a factor FOSR). Multiple averaging increases even more the resolution. The total resolution (in LSBs) of the output signal is then:

Resolutionout = Resolutionn\* FOSFORD.

Resolutionin correspond to the input data resolution (2 in case of serial data input or wider in case of parallel data input, for example 4096 for 12-bit parallel input). C Caution must be taken to not increase Resolutionout over the 32-bit range because the filter is performing all internal operations in 32-bit resolution.

# Output data rate

A consequence of the Sinc filter operation (moving average) is to reduce the output data rate with respect to the input sampling rate. The output data rate for a continuous signal conversion depends only on FOSR:

Since Datarateout depends only on FOSR while Resolutionout depends on both FOSR and FORD, it is recommended to first adjust the FOSR to achieve the required output data rate, and then adjust the FORD to achieve the required output resolution.

# Latency time

The latency represents the time that elapses between starting the filter (with valid input samples) and the first valid output sample. The latency has to be considered after starting the filter (first sample) and also after resuming the filter processing (in case input samples are not continuous and a trigger is used to restart conversion). The filter consists in a chain of clocked logic (adders and registers, principle of moving average) that needs to be initialized with valid data from previous input samples. If the input sample flow was stopped and therefore the history of input data was lost, it is necessary to wait that the filter logic is refilled with valid data before the output data becomes meaningful again. The filter latency is given by:

Tlatency = Tsampling \* (FOSR\*FORD) + (FORD+1)]

Note:

T hel tec  c =   FF ut   e implementation and optimization, a few more cycles are required represented by the term (FORD+1) in the formula.

# Simulation

The digital filter simulation available in [TUTORIAL] allows to:

• Define an input signal: either a signed 1-bit data stream or a signed 16-bit data stream   
• Configure the filter parameters (FOSR, FORD and IOSR) Compute the final output signal and verify the influence of the filter parameters. An example of simulation result is provided in Figure 18: Filtering simulation.

# 5.4.2 Integrator

The integrator has one configuration parameter, the IOSR (integrator oversampling ratio). The integrator processing consists in accumulating (sum) IOSR consecutive samples from

the filter output. This operation additionally decreases the output data rate (by a factor IOSR).

The requirements to consider in order to set the IOSR are:

• Required output data rate • Required number of samples from the filter to produce one integrator output sample.

An example of simulation result extracted form [TUTORIAL] is provided in Figure 18: Filtering simulation.

# 5.5 Analog watchdog

The configuration parameters of the analog watchdog embedded inside the DFSDM peripheral are provided in Table 3.

Table 3. DFSDM analog watchdog parameters   

<table><tr><td rowspan=1 colspan=1>Parameter</td><td rowspan=1 colspan=1>Description</td></tr><tr><td rowspan=1 colspan=1>AWLT</td><td rowspan=1 colspan=1>Analog watchdog low threshold. Signed 24-bit format.</td></tr><tr><td rowspan=1 colspan=1>AWHT</td><td rowspan=1 colspan=1>Analog watchdog high threshold. Signed 24-bit format.</td></tr><tr><td rowspan=1 colspan=1>AWFSEL</td><td rowspan=1 colspan=1>Analog watchdog fast mode select.0: analog watchdog watches output final 24-bit data (after the digital filter)1: analog watchdog watches data based on input 1-bit serial data samples(1)</td></tr></table>

In case AWFSEL= the serl input dat  flted by  dedatanalog watog flte hat houl e configured in the same way as the main digital filter: - AWFORD: analog watchdog filter order - AWFOSR = analog watchdog oversampling ratio Due to reduced analog watchdog filter options (AWFOSR = 1...32, AWFORD = 1..3) the signal from this fir as a maximum resolution 16 bits. In this case the resolution of the high (AWHT[:) ad low (AWLT[23:0]) threshold levels is limited to the higher 16 bits (AWHT[23:8], AWLT[23:8]).

Each input channel has its own comparator which compares the analog watchdog data (from analog watchdog filter) with analog watchdog threshold values (AWHT/AWLT). When several channels are selected (AWDCH[] in DFSDM_FLTxCR2 register), several comparison requests may be received simultaneously. In this case, the channel request with the lowest number is managed first and then continuing to higher selected channels. For each channel, the result can be recorded in a separate flag (AWHTF[], AWLTF[] in DFSDM_FLTxAWSR register). One comparison takes 1 DFSDM clock cycle. To be able to perform comparisons from all selected channels the user must properly configure the number of watched channels and analog watchdog filter parameters with respect to the input sampling clock speed and DFSDM frequency.

The DFSDM analog watchdog can generate interrupts and break signals. The interrupts are used to trigger the CPU and require a software intervention. The break signals (BKAWH[3:0]) are used for fast hardware interaction with other peripherals (for example stopping the timers to generate PWM in motor applications).

# 5.6 Short circuit detector

A short circuit detector is available on each channel and can be enabled with the SCDEN bit. The short circuit detector threshold is configured for each channel with SCDT[7:0] (range 0-255).

The short circuit detector features an upcounting counter that counts consecutive O's or 1's on serial data receiver outputs. The counter is restarted each time a logical transition is detected in the data stream (from 1 to 0 or from 0 to 1). If the counter reaches the value stored in SCDT[7:0], then a short-circuit event is invoked.

There are to type of usage for the short circuit detector feature that are presented in the following 2 subsections.

# True short circuit detection

In this case the goal is to detect situations where the DFSDM input signal is in the overflow state (continuously exceeding the external sigma-delta modulator full scale range specification) during a period of time exceeding the allowed duration of overflow state.

According application requirements, the maximum duration of the short circuit state is defined as tshortmax This is converted into a maximum number of consecutive 0's or s that is used to configure SCDT[7:0]:

SCDT[7:0] =

Each time the short circuit detector detects that input signal is stable during SCDT[7:0] bits, an error is reported (the input signal is in saturation over the maximum allowed time).

# Short circuit detection handling

There are 2 ways of handling the short circuit detection events:

Software interrupt generation. The microcontroller application software (interrupt routine) should perform the required actions (feedback) to a given short circuit event (for example stop the PWM generation into motor control applications). Break signal. A break signal, configured through the BKSCD[3:0] field, can be transmitted to other peripherals without any software intervention (example the break signal can be used to control a timer peripheral and stop the PWM generation into motor control applications).

# 5.7 Pulse skipper

The DFSDM can be used in beamforming applications where the location of an input signal source can be selected according its angle of incidence versus an array of sensors. The principle is described in Section 4.4.2: Beamforming support. Beamforming is usually used in conjunction with an array of digital microphones within audio applications.

The configuration of the DFSDM for beamforming requires to calculate the respective delay to be applied to each microphone in the array (see Figure 29: Beamforming principle). The delay of each microphone is calculated according the preferred receiving angle and the input sampling frequency and converted into a number of clock pulses of the serial input signal sampling frequency. Before configuring the delays, the reception of each microphone input bitstream by the respective DFSDM channel must be started synchronously, this is handled by the DFSDM global enable signal (DFSDMEN=1). After the DFSDM conversions are started, the calculated delay for each microphone channel must then be programmed once in each respective PLSSKP[5:0] field for each channel. After configuring the PLSSKP[5:0] fields, the software should read back the PLSSKP[5:0] fields and check that the values have been reset to 0 before asserting that the DFSDM final output data have been processed with the required delays.

After being initially configured, the delays can be updated again without stopping the audio data reception, but only by adding-up to the already programmed delays. The software must remember the successive writes into each PLSSKP[5:0] field for each microphone channel and consider that the effectively applied delay is the cumulated value of all successive writes.

# Example:

Let's assume 3 microphone channels have been synchronously started and their PLSSKP[5:0] fields programmed with respective delay values of 0, 5 and 10 corresponding to a preferred angle φ. If the preferred angle should be changed to -φ, a second write should be performed in PLSSKP[5:0] fields with the respective values 20, 10, 0, resulting in a cumulated total delay for the respective channels of 20, 15, 10 (this is the difference between the delays that determine the preferred angle and not the delay absolute values).

If the DFSDM is stopped (all continuous streams from microphones are stopped) the cumulated delays for all microphones are reset to zero at new DFSDM synchronous start (DFSDMEN=1).

# 5.8 Configuration using [TUTORIAL]

The [TUTORIAL] provides a configurable simulator based on the principles and formulas presented in this application note as well as a model of the DFSDM peripheral.

The interface of the DFSDM simulator is presented in a simple way, like if it would be a standard ADC. The user can configure the characteristics of the input signal and the DFSDM parameters according a specific analog-to-digital conversion application (sampling frequency, mode selection, filter parameters ..). The user can play with the input parameters and converge to the expected final conversion properties (output data rate and resolution) or use the simulator as a verification mean of a predefined configuration. The second approach (more deterministic) involves a preliminary analysis consisting in translating the application requirements into a digital signal processing scenario ported onto the DFSDM architecture, with the help of this application note. The analysis is not always straightforward and the user may sometime consider some trade-offs (like resolution versus data rate).

![](images/f9df24f9a02d8aae0f486f2fb46968b6105d61f9a24cc80dbdfdb2f8ea1055c6.jpg)  
Figure 33. DFSDM configuration in [TUTORIAL]

# 6 Conclusion

The DFSDM peripheral embeds advanced, and sometime complex, features that are useful and beneficial in many applications involving analog-to-digital conversion. This document introduces many different fields of application for the DFSDM, the advantages of using this peripheral and configurations examples as well as guidelines. The [TUTORIAL] allows to quickly experiment the influence of the various DFSDM parameters and validate that the software architecture choices and associated configurations allow to meet application requirements. The understanding of the principles underlying the DFSDM processing and how they can be implemented with appropriate tools and methods (the aim of this document) is a key factor for successful DFSDM-based applications.

# 7 Revision history

Table 4. Document revision history   

<table><tr><td rowspan=1 colspan=1>Date</td><td rowspan=1 colspan=1>Revision</td><td rowspan=1 colspan=1>Changes</td></tr><tr><td rowspan=1 colspan=1>30-Mar-2018</td><td rowspan=1 colspan=1>1</td><td rowspan=1 colspan=1>Initial release.</td></tr></table>

# IMPORTANT NOTICE  PLEASE READ CAREFULLY

acknowledgement.

the design of Purchasers' products.

No license, express or implied, to any intellectual property right is granted by ST herein.

l

I