# Digital signal processing for STM32 microcontrollers using CMSIS

# Introduction

This application note describes the development of digital filters for analog signals, and the transformations between time and frequency domains. The examples discussed in this document include a low-pass and a high-pass FIR filter, as well as Fourier fast transforms with floating and fixed point at different frequencies.

The associated firmware (X-CUBE-DSPDEMO), applicable to STM32F429xx and STM32F746xx MCUs, can be adapted to any STM32 microcontroller.

Digital Signal Processing (DSP) is the mathematical manipulation and processing of signals. Signals to be processed come in various physical formats that include audio, video or any analog signal that carries information, such as the output signal of a microphone.

Both Cortex®-M4-based STM32F4 Series and Cortex®-M7-based STM32F7 Series provide instructions for signal processing, and support advanced SIMD (Single Instruction Multi Data) and Single cycle MAC (Multiply and Accumulate) instructions.

The use of STM32 MCUs in a real-time DSP application not only reduces cost, but also reduces the overall power consumption.

The following documents are considered as references:

PM0214, "STM32F3 and STM32F4 Series Cortex®-M4 programming manual", available on www.st.com PM0253, "STM32F7 Series Cortex®-M7 programming manual", available on www.st.com   
• CMSIS - Cortex® Microcontroller Software Interface Standard, available on www.arm.com Arm® compiler toolchain Compiler reference, available on http://infocenter.arm.com "Developing Optimized Signal Processing Software on the Cortex®-M4 Processor", technical paper by Shyam Sadasivan, available on www.techonline.com.

# Contents

# Basic DSP notions 5

1.1 Data types 5

1.1.1 Floating point 5   
1.1.2 Fixed point . 6   
1.1.3 Fixed-point vs. floating-point

# Cortex® DSP instructions .. 8

2.1 Saturation instructions 8   
2.2 MAC instructions 8   
2.3 SIMD instructions 8

# Algorithms . . 10

3.1 Filters. 10   
3.2 Transforms. 10

# DSP application development 11

4.1 CMSIS library 11

4.2 DSP demonstration overview 11

4.2.1 FFT demonstration 12   
4.2.2 FFT performance 13   
4.2.3 FIR filter demonstration .15   
4.2.4 FIR filter design specification 17   
4.2.5 FIR performance 20   
4.2.6 FIR example software overview . .20

4.3 Overview of STM32 product lines performance 22

Revision history 24

# List of tables

Table 1. Pros and cons of number formats in DSP applications 7   
Table 2. Saturating instructions 8   
Table 3. SIMD instructions . . 9   
Table 4. FIR filter specifications 17   
Table 5. FFT performance 23   
Table 6. Revision history 24

# List of figures

Figure 1. Single precision number format . 5   
Figure 2. Double precision number format. 5   
Figure 3. 32 bits fixed point number format . .6   
Figure 4. FFT size calculation performance on STM32F429. 13   
Figure 5. FFT size calculation performance on STM32F746. 13   
Figure 6. Running FFT 1024 points with input data in Float-32 on STM32F429I-DISCO 14   
Figure 7. Running FFT 1024 points with input data in Float-32 on STM32F746-DISCO. 15   
Figure 8. Block diagram of the FIR example . 15   
Figure 9. Generated input (sum of two sine waves) 16   
Figure 10. Magnitude spectrum of the input signal 17   
Figure 11. FIR filter verification using MATLAB® FVT tool 19   
Figure 12. FIR filter computation performance for STM32F429. 20   
Figure 13. FIR filter computation performance for STM32F746. 20   
Figure 14. FIR demonstration results on STM32F429I-DISCO 21   
Figure 15. FIR demonstration results on STM32F746-DISCO 21

# Basic DSP notions

# Data types

DSP operations can use either floating-point or fixed-point formats.

# 1.1 Floating point

Floating point is a method to represent real numbers.

The floating point unit in the Cortex®-M4 is only single precision, as it includes an 8-bit exponent field and a 23-bit fraction, for a total of 32 bits (see Figure 1). The floating point unit in the Cortex®-M7 supports both single and double precision, as indicated in Figure 2.

he representation of single/double precision floating-point number is, respectively

![](images/649dda259fe9cfd49542022395eb54dc2513a614a9df1e66f3fb34dd75a79ce5.jpg)

where S is the value of the sign bit, M is the value of the mantissa, and E is the value of the exponent.

![](images/ee979ca9d3018ccd95c120c4676a351db9e2ca2c4017d17631ccbadcd29a3718.jpg)  
Figure 1. Single precision number format

![](images/1d9a5ab8d6473b5985fa9aac8fb5a79dd1e8764337868177ba94806bd81cd885.jpg)  
Figure 2. Double precision number format

# 1.1.2 Fixed point

Fixed point representation expresses numbers with an integer part and a fractional part, in a 2-complement format. As an example, a 32-bit fixed point representation, shown in Figure 3, allocates 24 bits for the integer part and 8 bits for the fractional part.

![](images/18454c66554ca974e3dae8618ee585d6ffd12794a15364220e228a0859110145.jpg)  
Figure 3. 32 bits fixed point number format

Available fixed-point data sizes in Cortex®-Mx cores are 8-, 16- and 32-bit.

The most common format used for DSP operations are Q7, Q15 and Q31, with only fractional bits to represent numbers between -1.0 and + 1.0.

The representation of a Q15 number is:

![](images/57e966605e9f9678b85517507d6b50cdb90afff4b59215a4acfb88d81ee97f61.jpg)

i  n

The range of numbers supported in a Q15 number is comprised between -1.0 and 1.0, corresponding to the smallest and largest integers that can be represented, respectively -32768 and 32767.

For example, the number 0.25 will be encoded in Q15 as 0x2000(8192)

When performing operations on fixed-point the equation is as follows:

where a, b and c are all fixed-point numbers, and <operand> refers to addition, subtraction, multiplication, or division. This equation remains true for floating-point numbers as well.

# Note:

Care must be taken when doing operations on fixed-point numbers. For example, if c = a x b with a and b in Q31 format, this will lead to a wrong result since the compiler will treat it as an integer operation, consequently it will generate "muls a, b" and will keep only the least significant 32 bits of the result.

# 1.1.3 Fixed-point vs. floating-point

Table 1 highlights the main advantages and disadvantages of fixed-point vs. floating-point in DSP applications.

Table 1. Pros and cons of number formats in DSP applications   

<table><tr><td rowspan=1 colspan=1>Number format</td><td rowspan=1 colspan=1>Fixed point</td><td rowspan=1 colspan=1>Floating point</td></tr><tr><td rowspan=1 colspan=1>Advantages</td><td rowspan=1 colspan=1>Fast implementation</td><td rowspan=1 colspan=1>Supports a much wider range of values</td></tr><tr><td rowspan=1 colspan=1>Disadvantages</td><td rowspan=1 colspan=1>Limited number rangeCan easily go in overflow</td><td rowspan=1 colspan=1>Needs more memory space</td></tr></table>

# 2 Cortex® DSP instructions

The Cortex®-Mx cores feature several instructions that result in efficient implementation of DSP algorithms.

# 2.1 Saturation instructions

Saturating, addition and subtraction instructions are available for 8-, 16- and 32-bit values, some of these instructions are listed in Table 2.

Table 2. Saturating instructions   

<table><tr><td rowspan=1 colspan=1>Code</td><td rowspan=1 colspan=1>Function</td></tr><tr><td rowspan=1 colspan=1>QADD8</td><td rowspan=1 colspan=1>Saturating four 8-bit integer additions</td></tr><tr><td rowspan=1 colspan=1>QSUB8</td><td rowspan=1 colspan=1>Saturating four 8-bit integer subtraction</td></tr><tr><td rowspan=1 colspan=1>QADD16</td><td rowspan=1 colspan=1>Saturating two 16-bit integer additions</td></tr><tr><td rowspan=1 colspan=1>QSUB16</td><td rowspan=1 colspan=1>Saturating two 16-bit integer subtraction</td></tr><tr><td rowspan=1 colspan=1>QADD</td><td rowspan=1 colspan=1>Saturating 32-bit add</td></tr><tr><td rowspan=1 colspan=1>QSUB</td><td rowspan=1 colspan=1>Saturating 32-bit subtraction</td></tr></table>

The SSAT (Signed SATurate) instruction is used to scale and saturate a signed value to any bit position, with optional shift before saturating.

# 2.2 MAC instructions

Multiply ACcumulate (MAC) instructions are widely used in DSP algorithms, as in the case of the Finite Impulse Response (FIR) and Infinite Impulse Response (IIR).

Executing multiplication and accumulation in single cycle instruction is a key requirement for achieving high performance.

The following example explains how the SMMLA (Signed Most significant word MuLtiply Accumulate) instruction works.

SMMLA RO, R4, R5, R6 ; Multiplies R4 and R5, extracts top 32 bits, adds ; R6, truncates and writes to RO

# 2.3 SIMD instructions

In addition to MAC instructions that execute a multiplication and an accumulation in a single cycle, there are the SIMD (Single Instruction Multiple Data) instructions, performing multiple identical operations in a single cycle instruction.

Table 3 lists some SIMD instructions.   
Table 3. SIMD instructions   

<table><tr><td rowspan=1 colspan=1>Code</td><td rowspan=1 colspan=1>Function</td></tr><tr><td rowspan=1 colspan=1>_qadd16</td><td rowspan=1 colspan=1>Performs two 16-bit integer arithmetic additions in parallel, saturating the results to the16-bit signed integer range -215 ≤ x ≤ 215 - 1.</td></tr><tr><td rowspan=1 colspan=1>_uhadd16</td><td rowspan=1 colspan=1>Performs two unsigned 16-bit integer additions, halving the results.</td></tr><tr><td rowspan=1 colspan=1>_shadd18</td><td rowspan=1 colspan=1>Performs four signed 8-bit integer additions, halving the results.</td></tr><tr><td rowspan=1 colspan=1>_smlsd</td><td rowspan=1 colspan=1>Performs two 16-bit signed multiplications, takes the difference of the products,subtracting the high half-word product from the low half-word product, and adds thedifference to a 32-bit accumulate operand.</td></tr></table>

The following example explains how the __shadd8 instruction works.

unsigned int add_and_halve(unsigned int vall, unsigned int val2)   
{ unsigned int res; res = shadd8(val1,val2); /\* res[7:0] = (val1[7:0] + val2[7:0]) >> 1 res[15:8] = (val1[15:8] + val2[15:8]) >> 1 res[23:16] = (val1[23:16] + val2[23:16]) >> 1 res[31:24] = (val1[31:24] + val2[31:24]) >> 1 \* return res;

The shadd8 intrinsic returns:

The halved addition of the first bytes from each operand, in the first byte of the return   
value   
The halved addition of the second bytes from each operand, in the second byte of the   
return value   
The halved addition of the third bytes from each operand, in the third byte of the return   
value   
The halved addition of the fourth bytes from each operand, in the fourth byte of the   
return value

# 3 Algorithms

# 3.1 Filters

The most common digital filters are:

FIR (Finite Impulse Response): used, among others, in motor control and audio   
equalization   
IIR (Infinite Impulse Response): used in smoothing data

The IIR filter can be used to implement filters such as Butterworth, Chebyshev, and Bessel.

# 3.2 Transforms

A transform is a function that converts data from a domain into another.

The FFT (Fast Fourier Transform) is a typical example: it is an efficient algorithm used to convert a discrete time-domain signal into an equivalent frequency-domain signal based on the Discrete Fourier Transform (DFT).

# DSP application development

# 4.1 CMSIS library

The Arm® Cortex® Microcontroller Software Interface Standard (CMSIS) is a vendor-independent hardware abstraction layer for all Cortex® processor based devices.

CMSIS has been developed by Arm® in conjunction with silicon, tools and middleware partners.

The idea behind CMSiS is to provide a consistent and simple software interface to the processor for interface peripherals, real-time operating systems, and middleware, simplifying software re -use, reducing the learning curve for new microcontroller developments and reducing the time to market for new devices.

CMSIS library comes with ST firmware under \DriversICMSISI.

The CMSIS-DSP library includes:

• Basic mathematical functions with vector operations   
• Fast mathematical functions, like sine and cosine   
• Complex mathematical functions like calculating magnitude   
• Filtering functions like FIR or IIR   
• Matrix computing functions   
• Transform functions like FFT   
• Controller functions like PID controller   
• Statistical functions like calculating minimum or maximum   
• Support functions like converting from one format to another Interpolation functions

Most algorithms uses floating-point and fixed-point in various formats. For example, in FIR case, the available Arm® functions are:

arm_fir_init_f32  
• arm_fir_f32  
• arm_fir_init_q31  
• arm_fir_q31  
• arm_fir_fast_q31  
• arm_fir_init_q15  
• arm_fir_q15  
• arm_fir_fast_q15  
• arm_fir_init_q7  
− arm_fir_q7

# 4.2 DSP demonstration overview

The goal of this demonstration is to show a full integration with STM32F429 using ADC, DAC, DMA and timers, and also calling CMSIS routines, all with the use of graphics, taking advantage of the 2.4" QVGA TFT LCD included in the discovery board.

This demonstration also shows how easy it is to migrate an application from an STM32F4 microcontroller to one of the STM32F7 Series.

A graphical user interface is designed using STemWin, to simplify access to different features of the demonstration.

# 4.2.1 FFT demonstration

The main features of this FFT example are

For the STM32F429

Generate data signal and transfer it through DMA1 Stream6 Channel7 to DAC   
output Channel2   
Acquire data signal with ADC Channel0 and transfer it for elaboration through   
DMA2 Stream0 ChannelO   
Vary the frequency of the input signal using Timer 2   
Initialize FFT processing with various data: Float-32, Q15 and Q31   
Perform FFT processing and calculate the magnitude values   
Draw input and output data on LCD screen

For the STM32F746

Generate data signal and transfer it through DMA1 Stream5 Channel7 to DAC   
output Channel1   
Acquire data signal with ADC Channel4 and transfer it for elaboration through   
DMA2 Stream0 Channel0   
Vary the frequency of the input signal using Timer 2   
Initialize FFT processing with various data: Float-32, Q15 and Q31   
Perform FFT processing and calculate the magnitude values   
Draw input and output data on LCD screen

The code below shows how to initialize the CFFT function to compute a 1024, 256 or 64 points FFT and transform the input signals (aFFT_Input_ f32) from the time domain to the frequency domain, then calculate the magnitude at each bin, and finally calculate and return the maximum magnitude value.

/\* Initialize the CFFT/cIFFT module, intFlag = 0, doBitReverse = 1 \*/   
arm_cfft_radix4_init_f32(aFFT F32_struct, FFT _Length, FFT _INVERSE_FLAG, FFT Normal_UTPUT FLAG); /\*Processing function for the floating-point Radix-4 cFFT/cIFFT./   
arm_cfft_radix4_f32(&FFT_32_struct,aFFT_Input_f32);   
/\*Process the data through the Complex Magiture Module for calculating the magnitude at each bn / arm_cmplx_mag_f32(aFFT_nput_f32,aFFT_Output_f32,FFT_Length);   
/\* Calculates maxValue and returns corresponding value \*/   
arm_max_f32(aFFT_Output_f32,FFT_Length, &maxValue, &maxIndex);

FFT_Length depends on the user choice, it can be 1024, 256 or 64. The user can find FFT initialization and processing for other formats in the fft_processing.c source file.

# 4.2.2 FFT performance

Figure 4 shows the absolute execution time and the number of cycles taken to perform an FFT on STM32F429 device running at 180 MHz, while Figure 5 refers to the same parameters measured on an STM32F746 device running at 216 MHz, in both cases using MDK-Arm ™M (5.14.0.0) toolchain supporting C Compiler V5.05 with Level 3 (-O3) for time optimization.

![](images/700e30fa3350166c27469c2651142ebe4b4295198242e6d9eb5ad860ffd55fe3.jpg)  
Figure 4. FFT size calculation performance on STM32F429

![](images/1cef5da631f2d8abdca7dc75e1cab38030735505b80b182560e742f24f2b5c04.jpg)  
Figure 5. FFT size calculation performance on STM32F746

# Results on STM32F429I-DISCO

To run one of the FFT examples select FFT, then connect PA5 to PA0.

Signal shape and spectrum are displayed on the LCD.

By varying the slider position the user can see the new input signal shape and the FFT spectrum of the input signal updated in real time, as illustrated in Figure 6.

![](images/707b3b6958f25499b137a9a605c164ef7f5921656462914a08ea85e16b9991d4.jpg)

# Results on STM32F746-DISCO

In this case it is possible to take advantage of the existing connection between PA4 and DCMI_HSYNC. No other connections are needed since PA4 is configured as an output for DAC1 and an input for ADC1.

Signal shape and spectrum are displayed on the LCD

By varying the slider position the user can see the new input signal shape and the FFT spectrum of the input signal updated in real time, as illustrated in Figure 7.

![](images/5ebaac81ce5f28c5ffb795c2856d8f1e187ab9059fa4e6f752d6352473a36497.jpg)  
Figure 7. Running FFT 1024 points with input data in Float-32 on STM32F746-DISCO

# 4.2.3 FIR filter demonstration

The goal of this demonstration is to remove the spurious signal (a sine wave at 15 kHz) from the desired signal (a sine wave at 1 kHz), applying a low-pass FIR filter in different format.

When choosing the Q15 format, it is possible to isolate the spurious signal applying a high-pass FIR filter.

The block diagram of the FIR example is shown in Figure 8.

![](images/34292e96764d5448786fb833c84746f6b62b0f3ac49e5b5253ae91cb3c91674e.jpg)  
Figure 8. Block diagram of the FIR example

The code below shows the initialization and the processing function for the floating-point FIR filter.

/\* Call FIR init function to initialize the instance structure, \*/ arm_fir_init_f32(6FIRF32_Struct,NUM_TAP8,float32t\*)&aFIR32Coeffs[0],sfirStateP32[0],blockSize); for(counter_PIR_f32_p=0; counter_FIR_f32_ <numBlocks; counter_PIR_f32_p\*) II

The user can find FIR initialization and processing for other formats in the fir_processing.c source file.

Input data to the FIR filter is the sum of the 1 kHz and 15 kHz sine waves (see Figure 9), generated by MATLAB® in floating point format using the following spt:

%Samples per second   
Fs=48000;   
T=1/Fs;   
% Number of samples in the signal   
Lenght=320;   
t=(0:Lenght-1)\*T;   
% Generate the input signal   
Input_signal=sin (2\*pi\*1000\*t) + 0.5\*sin(2\*pi\*15000\*t);

![](images/406ac837223e2fa6dad24322c349780c89a41a779dc1e18bae5e5a9c959e2bc3.jpg)  
Figure 9. Generated input (sum of two sine waves)

The magnitude spectrum of the input signal (Figure 10) shows that there are two frequencies, 1 kHz and 15 kHz.

![](images/f2050edf6dbe4aa5f66983b4d20e497029c7691f7fae94f8ff7dc056698d5c5f.jpg)  
Figure 10. Magnitude spectrum of the input signal

As the noise is positioned around 15 kHz, the cutoff point must be set at a lower frequency, namely at 6 kHz.

# 4.2.4 FIR filter design specification

The main features are listed in Table 4.

Table 4. FIR filter specifications   

<table><tr><td rowspan=1 colspan=1>Feature / Parameter</td><td rowspan=1 colspan=1>Value</td></tr><tr><td rowspan=1 colspan=1>Type</td><td rowspan=1 colspan=1>Low-pass</td></tr><tr><td rowspan=1 colspan=1>Order</td><td rowspan=1 colspan=1>28</td></tr><tr><td rowspan=1 colspan=1>Sampling frequency</td><td rowspan=1 colspan=1>48 kHz</td></tr><tr><td rowspan=1 colspan=1>Cut-off frequency</td><td rowspan=1 colspan=1>6 kHz</td></tr></table>

The low-pass filter is designed with MATLAB®, using the commands shown below

% Define filter cut-off frequency (6 kHz)   
Cutoff_Freq = 6000;   
% Nyquist frequency   
Nyq_Freq = Fs / 2;   
cutoff_norm = Cutoff_Freq / Nyq_Freq;   
% FIR filter order   
order = 28;   
% Create low-pass FIR filter   
FIR_Coeff = firl(order, cutoff_norm);   
% Filter the Input signal with the FIR filter   
Filterd_signal = filt§r(FIR_Coeff, 1, Input_signal);

Note:

FIR filter order is equal to the number of coefficients -1.

In order to verify the designed filter, it's possible to use the Filter Visualization Tool in MATLAB® using the following command:

% Using Filter Visualization Tool fvtool(FIR_Coeff, 'Fs', Fs)

The Filter Visualization Tool (FVT) is a practical tool allowing the user to verify the details and the parameters of the built filter.

In Figure 11 are reported (left to right, top to bottom):

• magnitude response   
• filter gain (in dB) vs. frequency (in Hz)   
• impulse response   
• step response

![](images/3696c180909d189ed40665d2bfff7eb37be2c13902e9b2ba5cf81be30cc43d18.jpg)  
Figure 11. FIR filter verification using MATLAB® FVT tool

# 4.2.5 FIR performance

Figure 12 shows the absolute execution time and the number of cycles taken to run the previously designed FIR filter on STM32F429I device running at 180 MHz, while Figure 13 refers to the STM32F746 device running at 216 MHz, in both cases using MDK-Arm ™M (5.14.0.0) toolchain supporting C Compiler V5.05 with Level 3 (-O3) for time optimization.

![](images/89cd4d45abf7a47cd76f188158826905c4666a4c4cd81ee1582f8c6d86d948b3.jpg)  
Figure 12. FIR filter computation performance for STM32F429

![](images/d1d2da6f82ca713649409fc9988e425492e052548b86ae2916644bc656d6ad84.jpg)  
Figure 13. FIR filter computation performance for STM32F746

# 4.2.6 FIR example software overview

The main features of this FIR example are

Generate the input data signal and stock in the RAM   
• Initialize FFT processing with various data: F32, Q15 and Q31   
• Apply the low-pass FIR filter for Float-32, Q15 and Q31   
• Apply the high-pass FIR filter for Q15 Draw input and output data on LCD screen

# Results on STM32F429I-DISCO

This example considers two scenarios:

1.a FIR low-pass filter that includes Float-32, Q31 and Q15 data format   
2a FIR high-pass filter that includes only Q15 data format.

The oscilloscope screen captures for three different configurations are reported in Figure 14. Left to right are shown

a low-pass FIR filter when the input data is floating point 2. a low-pass FIR filter with Q15 input data 3a high-pass FIR filter with Q15 input data

![](images/3f84d554021705b1e515ffac97f5a9a7f0742be67cff41fa84c6b5922e013092.jpg)  
Figure 14. FIR demonstration results on STM32F429I-DISCO

# Results on STM32F746-DISCO

The same example has been run on the STM32F746, the waveforms are visible in Figure 15. Left to right are shown:

1a low-pass FIR filter when the input data is floating point.   
2. a low-pass FIR filter with Q15 input data.   
3. a high-pass FIR filter with Q15 input data.

![](images/b5beb55e4eac62533b653bf4fd5a5767956bb09dc3dcb5426747544b0f2c468b.jpg)  
Figure 15. FIR demonstration results on STM32F746-DISCO

# 4.3 Overview of STM32 product lines performance

One of the purposes of this application note is to provide benchmarking results for different STM32 Series. In the case in discussion, the DSP algorithm to use are:

• complex FFT using 64 and 1024 points (radix-4) use of fixed point format (Q15 and Q31)

The comparison is based on execution time (i.e. the time required for the FFT processing). The input vector is generated with MATLAB®, using the commands below:

>Fs=48000;   
T=1/FS;   
> L=1024;   
> t=(0:L-1)\*T;   
> x=sin (2\*pi\*1000\*t) + 0.5\*sin(2\*pi\*15000\*t);   
> x = x(:) ;

Table 5 summarizes the results, achieved using MDK-Arm ™ (5.14.0.0) toolchain supporting C Compiler V5.05 with Level 3 (-O3) for time optimization.

Table 5. FFT performance   

<table><tr><td rowspan=1 colspan=1>MCU</td><td rowspan=1 colspan=1>Systemfrequency</td><td rowspan=1 colspan=1>Cortexcore</td><td rowspan=1 colspan=1>Fixed pointformat</td><td rowspan=1 colspan=1>No. ofpoints</td><td rowspan=1 colspan=1>Cycles</td><td rowspan=1 colspan=1>Duration (μs)</td></tr><tr><td rowspan=4 colspan=1>STM32F091</td><td rowspan=4 colspan=1>48 MHz</td><td rowspan=4 colspan=1>MO</td><td rowspan=2 colspan=1>Q31</td><td rowspan=1 colspan=1>1024</td><td rowspan=1 colspan=1>783106</td><td rowspan=1 colspan=1>16314</td></tr><tr><td rowspan=1 colspan=1>64</td><td rowspan=1 colspan=1>26576</td><td rowspan=1 colspan=1>553</td></tr><tr><td rowspan=2 colspan=1>Q15</td><td rowspan=1 colspan=1>1024</td><td rowspan=1 colspan=1>938278</td><td rowspan=1 colspan=1>19547</td></tr><tr><td rowspan=1 colspan=1>64</td><td rowspan=1 colspan=1>37522</td><td rowspan=1 colspan=1>781</td></tr><tr><td rowspan=4 colspan=1>STM32F103</td><td rowspan=4 colspan=1>72 MHz</td><td rowspan=4 colspan=1>M3</td><td rowspan=2 colspan=1>Q31</td><td rowspan=1 colspan=1>1024</td><td rowspan=1 colspan=1>214098</td><td rowspan=1 colspan=1>2973</td></tr><tr><td rowspan=1 colspan=1>64</td><td rowspan=1 colspan=1>7983</td><td rowspan=1 colspan=1>110</td></tr><tr><td rowspan=2 colspan=1>Q15</td><td rowspan=1 colspan=1>1024</td><td rowspan=1 colspan=1>248936</td><td rowspan=1 colspan=1>3457</td></tr><tr><td rowspan=1 colspan=1>64</td><td rowspan=1 colspan=1>9696</td><td rowspan=1 colspan=1>134</td></tr><tr><td rowspan=4 colspan=1>STM32F217</td><td rowspan=4 colspan=1>120 MHz</td><td rowspan=4 colspan=1>M3</td><td rowspan=2 colspan=1>Q31</td><td rowspan=1 colspan=1>1024</td><td rowspan=1 colspan=1>193189</td><td rowspan=1 colspan=1>1609</td></tr><tr><td rowspan=1 colspan=1>64</td><td rowspan=1 colspan=1>6992</td><td rowspan=1 colspan=1>58</td></tr><tr><td rowspan=2 colspan=1>Q15</td><td rowspan=1 colspan=1>1024</td><td rowspan=1 colspan=1>200608</td><td rowspan=1 colspan=1>1671</td></tr><tr><td rowspan=1 colspan=1>64</td><td rowspan=1 colspan=1>7828</td><td rowspan=1 colspan=1>65</td></tr><tr><td rowspan=4 colspan=1>STM32F303</td><td rowspan=4 colspan=1>72 MHz</td><td rowspan=4 colspan=1>M4</td><td rowspan=2 colspan=1>Q31</td><td rowspan=1 colspan=1>1024</td><td rowspan=1 colspan=1>178005</td><td rowspan=1 colspan=1>2472</td></tr><tr><td rowspan=1 colspan=1>64</td><td rowspan=1 colspan=1>7129</td><td rowspan=1 colspan=1>99</td></tr><tr><td rowspan=2 colspan=1>Q15</td><td rowspan=1 colspan=1>1024</td><td rowspan=1 colspan=1>101316</td><td rowspan=1 colspan=1>1407</td></tr><tr><td rowspan=1 colspan=1>64</td><td rowspan=1 colspan=1>4304</td><td rowspan=1 colspan=1>59</td></tr><tr><td rowspan=4 colspan=1>STM32F429</td><td rowspan=4 colspan=1>180 MHz</td><td rowspan=4 colspan=1>M4</td><td rowspan=2 colspan=1>Q31</td><td rowspan=1 colspan=1>1024</td><td rowspan=1 colspan=1>153307</td><td rowspan=1 colspan=1>855</td></tr><tr><td rowspan=1 colspan=1>64</td><td rowspan=1 colspan=1>6025</td><td rowspan=1 colspan=1>33</td></tr><tr><td rowspan=2 colspan=1>Q15</td><td rowspan=1 colspan=1>1024</td><td rowspan=1 colspan=1>82299</td><td rowspan=1 colspan=1>457</td></tr><tr><td rowspan=1 colspan=1>64</td><td rowspan=1 colspan=1>3655</td><td rowspan=1 colspan=1>20</td></tr><tr><td rowspan=4 colspan=1>STM32F746</td><td rowspan=4 colspan=1>216 MHz</td><td rowspan=4 colspan=1>M7</td><td rowspan=2 colspan=1>Q31</td><td rowspan=1 colspan=1>1024</td><td rowspan=1 colspan=1>93725</td><td rowspan=1 colspan=1>468</td></tr><tr><td rowspan=1 colspan=1>64</td><td rowspan=1 colspan=1>4537</td><td rowspan=1 colspan=1>22</td></tr><tr><td rowspan=2 colspan=1>Q15</td><td rowspan=1 colspan=1>1024</td><td rowspan=1 colspan=1>56989</td><td rowspan=1 colspan=1>284</td></tr><tr><td rowspan=1 colspan=1>64</td><td rowspan=1 colspan=1>2994</td><td rowspan=1 colspan=1>14</td></tr><tr><td rowspan=2 colspan=1>STM32L073</td><td rowspan=2 colspan=1>32 MHz</td><td rowspan=2 colspan=1>M0+</td><td rowspan=1 colspan=1>Q31</td><td rowspan=1 colspan=1>64</td><td rowspan=1 colspan=1>33493</td><td rowspan=1 colspan=1>1046</td></tr><tr><td rowspan=1 colspan=1>Q15</td><td rowspan=1 colspan=1>64</td><td rowspan=1 colspan=1>44506</td><td rowspan=1 colspan=1>1390</td></tr><tr><td rowspan=4 colspan=1>STM32L476</td><td rowspan=4 colspan=1>80 MHz</td><td rowspan=4 colspan=1>M4</td><td rowspan=2 colspan=1>Q31</td><td rowspan=1 colspan=1>1024</td><td rowspan=1 colspan=1>144214</td><td rowspan=1 colspan=1>1802</td></tr><tr><td rowspan=1 colspan=1>64</td><td rowspan=1 colspan=1>6007</td><td rowspan=1 colspan=1>75</td></tr><tr><td rowspan=2 colspan=1>Q15</td><td rowspan=1 colspan=1>1024</td><td rowspan=1 colspan=1>77371</td><td rowspan=1 colspan=1>967</td></tr><tr><td rowspan=1 colspan=1>64</td><td rowspan=1 colspan=1>3509</td><td rowspan=1 colspan=1>43</td></tr></table>

# 5 Revision history

Table 6. Revision history   

<table><tr><td rowspan=1 colspan=1>Date</td><td rowspan=1 colspan=1>Revision</td><td rowspan=1 colspan=1>Description of changes</td></tr><tr><td rowspan=1 colspan=1>23-Mar-2016</td><td rowspan=1 colspan=1>1</td><td rowspan=1 colspan=1>Initial release</td></tr><tr><td rowspan=1 colspan=1>23-Feb-2018</td><td rowspan=1 colspan=1>2</td><td rowspan=1 colspan=1>Updated Table 5: FFT performance.Minor text edits across the whole document.</td></tr></table>

# IMPORTANT NOTICE  PLEASE READ CAREFULLY

acknowledgement.

the design of Purchasers' products.

No license, express or implied, to any intellectual property right is granted by ST herein.

I