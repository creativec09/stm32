# How to use ADC Oversampling techniques to improve signal-to-noise ratio on STM32 MCUs

# Introduction

sampling rate.

application power consumption.

T consumption.

Fa TheoTSW-T32 X-CUBE-ADCOVSPliv io v l STM32F3 series and STM32Lx series products.

is provided. It is integrated in the STM32 products listed in Table 1.

overall lower power consumption compared with the software-based implementation.

the desired resolution improvement. These theoretical formulas are compared to practical use cases.

Table 1. Applicable products   

<table><tr><td>Type</td><td>Series</td></tr><tr><td>Microcontrollers</td><td>STM32U5 series, STM32U0 series, STM32H7 series, STM32H5 series, STM32F7 series, STM32F4 series, STM32F2 series, STM32F0 series, STM32L1 series, STM32F3 series, STM32F1 series, STM32L4+ series, STM32L4 series, STM32L0 series, STM32L5 series, STM32G4 series, STM32G0 series, STM32WB series</td></tr></table>

# 1 General information

# Note:

This document applies to STM32 Arm®-based microcontrollers.   
Arm is a registered trademark of Arm Limited (or its subsidiaries) in the US and/or elsewhere. arm

# 2 Oversampling as a way to improve the quality of signal acquisition

# 2.1

# Quantization of noise and signal-to-noise ratio

AgeDalalticar pplizatneae zatinolunp r allen ee a z signal is called the quantization error.

Tmuerrorelver wheigi alLeas ant the transfer function (left side of Figure 1).

Th LBs lsote ln ha hesea-ialo-oADC and a voltage reerence, VAREF, the quantum , isthe minimum distance between two adjacent ADC codes. Moreover, it is defined as follows:

![](images/6473b3491f6405702040f2d937266421d586b74f6031f6f2bfe781f8760525a5.jpg)

where:

![](images/bcaf344194751feb8366683ef44c092558264e9260b2d6a725e176ff71331688.jpg)

with -q / 2a < t < +q / 2a

The quantization error e(t) as a function of time is shown in the right side of Figure 1.

That y  o l iseh elat aver representation of the quantization error for any AC signal, and that it behaves like wideband noise.

![](images/702123e3e0cf382587cbb49e7ebeb80a3a0c7ac30995192dbbdc641126481c38.jpg)  
Figure 1. Ideal N-bit ADC quantization

The quantization error e(t) is defined as:

![](images/c5b3583e3b2e7f49bffbe188448dc1f31891c70840cfb80001306f15cf54cee9.jpg)

![](images/94e43ee2727f6d2e991cb6ee2cbe56f1f5870b65caa022f4af39d7314e6952d0.jpg)

TR al-onoati he atiofheDCoise heput ia powe.o nel AC, a looo considered.

For a full-scale input sine wave this is expressed as follows:

![](images/0732e669774739f8c7a490cc21ae498da6eebc9d92dcdf198263a4230577b914.jpg)

Using equations (3) and (4), the SNR of an ideal N-bit converter (ADC resolution) is calculated as follws:

![](images/8ddb86230f78588dc87ccc8bad1cbac1d380b97c8196c98949a7a255aab8a058.jpg)

It z Fs/2).

It cn e en hat when heNR c, he ADC efeivub  bi in the euatin ic.

Noalsoha DCt eust ,INL ntal a DNL fentilonear rdesption hee erors cn e ound nhe TM3 CU dataeets. These errors degrade the ideal ADC resolution and determine the real effective number of bits of the ADC (ENOB). Improving the SNR enhances the effective number of bits of the ADC. The following section demonstrates that sampling the input signal rates higher than the Nyquist frequency improves the SNR. The Nyquist frequency is discussed in the next paragraph.

# 2.2

# Nyquist theorem and antialiasing low-pass filter relaxation

TNyqushe aha tuc enalpuhealmuspl F (sampling frequency) that is greater than twice the maximum frequency component of the input signal.

Noncompliance with the Nyquist theorem causes aliasing effects and the analog signal cannot be fully reconstructed from the input samples.

oly I iult deait wi plcT thesample ad reducing he sample ate y decimatinUsinghis method relaxes heantialiasig lowpass filter constraints.

# Processing gain achievable with oversampling

I cn,he unizain oimaey Gausin  rmonily veq bandwidth (see Figure 2).

![](images/1eb53c8491d2ae78fe80df8f7ec3d2f0d2f0233ebea689736a34b2c0db06a325.jpg)  
Figure 2. Quantization noise spectrum

However, undercertain conditions where the sampling clock and the signal are harmonically correlat, the nzatocoelaitra conditions where the quantization noise does not appear as random noise, dithering must be applied (see Section 2.4 Dithering).

In many applications, the useful signal occupies a bandwidth (BW) smaller than Fs/2.

ment beoe he total RMS noiis edu (Fgur); he MS aluehe quantizatin o divided by a ratio that depends on the useful bandwidth (BW) with respect to the sampling rate (Fs).

![](images/2c7a0b8798661de599b1b721fba2b0cbc6f1787c2d6b591f35031218a2c70cf0.jpg)  
Figure 3. Quantization noise gain

We can then eorulate he previous R epressn taking intoaccont this processing gan, by filterg he out-off band noise:

![](images/a04ef8af170572b89ced7317be1459fad6b418b294d9b17b56b4902407aefcf4.jpg)

This expression is valid over a bandwidth, BW, with an oversampling rato given by:

![](images/0050383d108811c97cca691c983b0ea0f64dbbfe68d3bf6b6d5da5726704634f.jpg)

# 2.4

# Dithering

The technique presented above works well for a white quantization noise.

Hoel caeaat lahe lal si work properly.

theory) no code transitions when the signal is smaller than the quantization step.

Owayolheeg he Gaoi toggling.

Dithering also ensures that the quantization noise is always random, independently from the input signal.

![](images/8ce8a1230379b96c63b564547b9ebeb8945e7012618745ccde33f1630b4777b0.jpg)  
Figure 4. Dithering technique

T wanted bandwidth, and is only present outside of that bandwidth.

The embedded DAC can be used for generating the dithering signal. Also, in Section 3.Oversampling using triangular dither, we generate the dithering signal by means o a timer configured in PWM mode, and some additional electronic components.

error can be considered as wideband noise, the dithering technique can be omitted.

# 3 Software oversampling

This section presents two software-oversampling implementation methods. Each has advantages and disadvantages, which are compared.

The embedded software delivered with this application note is available in the STSW-STM32014 (or X-CUBE-ADC_OVSP) package.

# 3.1

# Oversampling using white noise

# 3.1.1

# Oversampled signal SNR with white input noise

Equation 6 in Sectin2.) gives the Robtained whenoversampling he input signal wit a sample raOS times faster than the Nyquist frequency, and low-pass filtering the signal band:

Thi howsa eac ubli he pligeqn u henbandoi ydicae masremen olution by 0.5 biThereore a   NR gaiis equi toaolution bi o heDC. In alal bqubeatneDCplhoul

![](images/12284b4429649c0a9cb7158d9ab52783dfb554b7a029436fe39ba9c3cfc0a2e6.jpg)

Where Fs is the ADC sampling frequency used.

# 3.1.2

# Decimation

Averaging means adding m samples and dividing the result by m. Averaging several data from an ADC masemen uivalen  owpass fhiceuateheal ucatio anoAve therefore often used to smooth and remove spikes from the input signal.

# Note:

Normal averaging does not increase the resolution of the conversion because the sum of m N-bit samples divided by m is an N-bit representation of the sample.

Decimation is an averaging method. When combined with oversampling, decimation improves the ADC resolution.

I    AC eal  v additional effective bits, the sum is shifted to the right by p bits.

sample computed from the OSR input samples.

The oversampling method limits themaximum input frequency bandwidth. In the case of the STM32F1 series, STM32F3 series and STM32Lx series (with maximum sampling rate around 1 Msps), signals having components u to00 kHz can be processed by the ADC. If for example, two additial resolutin bits are requi the maximum input frequency is 500 kHz/16 = 31.25 kHz when the oversampling uses white noise.

# 3.1.3 When is this method efficient?

For the oversampling and decimating method to work properly, the following requirements must be satified:

There should be some noise in the input signal. This noise must approximate the white noise with a uniform power spectral density over the frequency band of interest. The noise amplitude must be sufficient to toggle the input signal randomly from sample to sample by an amount of at least 1 LSB. Otherwise, the input samples would have the same representation, and the sum and average operations would not give any extra resolution. For most applications, the internal ADC thermal noise and the input signal noise are sufficient to use this method. I the thermal noise does not have a high-enough amplitude to toggle the input signal randomly, then a dithering operation must be appled (see part 2.). Regarding this point, two questions can be raised. The firs is How to evaluate the ADC noise and test its Gaussian criteria? and How to generate white noise if needed?.

l sial over heADC codes.Thehistogram method can beused o ver  the iputnoie follows a Gauss distribution. The example in Figure 5 shows two possible situations.

![](images/88e94bf3487a7abdb88f8c1655868f02d3fd015be5ca261b75a12b89183794b0.jpg)  
Figure 5. Histogram analysis

Histogram for a signal with white nois e

![](images/e36e940db3625800b023fcbc7e38b9eb2ac64e4c4a00222148cbb6f50edf244f.jpg)  
Histogram for a signal without white nois e

Inase wheeexteal oisdithermustdeheut sial e heral oi eerat diode or a resistor can be injected into the input signal.

Th iput noe must ot coeate with euseul input al,and e put l hould havqual proability  beig between two adjacent ADCcodes.This means that ths method ds ot work or sstems using a feedback process.

# 3.1.4

# Implementation method on STM32F1, STM32F3, and STM32Lx series devices

This method describes the different steps undertaken to implement and test the oversampling method on the STM32F1 series, STM32F3 series and STM32Lx series devices.

A  w pu w th input signal toggle randomly by/2 LB. For this, the application environment noise must be consiere.

The is te consit  putingheDC theral nois oncludeexteal whitenoi must en i arc t lso the possble noisgenerated bythe iffernt boarconents and theayoutThereo evaluation depends on the application board but the methodology remains the same.

Tehistogrmethoise oriferent iutoltaghisiut voltag mpl a lare times (example 5000). The related distribution can be easily interpreted using a spreadsheet.

For example, for a 1.65 V dc input voltage applied on the STM3210B-EVAL evaluation board, the histogram shown in Figure 6 is detected.

![](images/c265093a614ea47b0cca421a3cb3cd771fff83dcc75e8dc29b52a2c1c0b6aca2.jpg)  
Figure 6. Histogram analysis for DC = 1.65 V

TAC therl onpufom hstog althh t an ehownsot heve of this application note and the details are not offered here).

To carry on this ADC noise test, the user must do the following

Uncomment the line #define Themal_Noise_Measure in the oversampling.h file. Configure the Total_Samples_Number which is the number of ADC conversion operations. It must be smaller than 65535. The DMA channel is configured to store the number of ADC samples in a RAM buffer. At the end of the transfer, an interrupt is generated and the number ofoccurrences of each ADC codeis computed.

To compute the occurrence of the ADC codes, a variable giving the relevant ADC codes is defined.

When the code is run, Relevant_ADC_Samples ADC samples and their coresponding number of occurrences iplayyaeyTeuai at arbau the effective number ofADC samples found is maller than the defined RelevantADC_Samples variable, then displayed or both ADC code and ADC code occuences.Theuser can capture them and build a histogram.

# 3.1.4.1

# Embedded-software flowchart for oversampling using white noise

The STM32F1 series, STM32F3 series and STM32Lx series on-chip ADC conversion frequency is fixed to 1 MHz. TheADC DMA hannel iconfigure ransfer heumber versamplipus from heADC dat eg t A.Tu triggered and the oversampled result is computed.

The general-purpose timerTM2 is used to generate theinput signal sampling frequency. For this, he TIM2 cocu oversampling.h file as #define Input_Signal_Sampling_Period. When the TiM2 update interrupt is triggered, the DMA is reenabled and the converted ADC values can be treated.

Figure 7 summarizes the implemented functionality.

![](images/8af0402903df3f696e806ee55c1935d659f299ef0b5b9be4a6deab057499719f.jpg)  
Figure 7. Oversampling using a white noise flowchart

The oversample datupute nhe MA transercompleterrupt.or yncronizatin easos, pa greater han he  qud beADC nve OSR mple  eatr han he ADCterup time.

I e  eeo tmT  erate he plngeunc. However, eMAmust ure nca continuous mode and theDMA transer completenterruptmust beupdated accordinglyThe oversampled atum is usually computed in the DMA transfer complete interrupt.

# 3.1.4.2

# Oversampling using white noise - result evaluation

To evaluate the oversampling method, the user must uncomment the #define Oversampling_Test line and configure the number of samples with an enhanced resolution.

Whupe ahendisplay he HyperTermialTheHyperTermial coniguratin must eit data pariy u.

To evaluate the new enhanced ADC, a ramp with a 50 Hz frequency and a 1 V amplitude s input to theADC and sampled using the oversampling algorithm every 100 µs.

The embedded software example related to this method is located in the WhiteNoiseMethod folder.

Th oversampling algorithm usig white noise is un with the same ramp (50 Hz frequency and 1 V amplitude). uvlatm ue adding one bit while Figure  is the result of adding two additional bits to the ADCon-chip resolution.

When the ramp is sampled without using any extra software resolution, with a 3.3 V reference supply, 1 V corresponds to the digital value 1250.

When oeadditnal bi is added, V issampled as00 and when two aitional bit re added, V is pled as 5000.

This means that the environment contains enough noise for this method to work.

# 50H/1V-1 additional bit

![](images/28b183d6822f89673d0489ac39b72189ad494e88a2f13755a0cc6222672d3b28.jpg)  
Figure 8. Ramp samples with 1 additional bit   
Figure 9. Ramp samples with 2 additional bits

![](images/a5d0ef94ca0decb16d374d520eff931d3c385f7903295af8361c28b7275048b7.jpg)  
50 H/1 V - 2 additional bits

# 3.2

# Oversampling using triangular dither

Aihae lee uzatn e e  ex the relative position of the input signal between q0 and q1.

Wgula ntiz A t the higher quantization steps.

Teaulhugu with a period of OSR times the ADC sampling period and an amplitude of n + 0.5 LSB where n = 0,1,2,3.

Telpet works. In thi example, heADCon-chip reolutons 3 and 3 extr bit aeaded by be softae.The hav pli  0. 0 = ple, the input signal is sampled 2.23 times (16 times).

![](images/4c407212fa2efaf873c9cad8d7929187e486147fa11de0205619650a1078841c.jpg)  
Figure 10. How to perform oversampling by adding a triangular signal

I equal to:

![](images/d094d59ac990a4c36ae690809ca955d84f127d70625d4715aed20fc31fdf2d96.jpg)

Thereoeac doublin  the mpling equecproves he SNR by 6 dB and as b  ADC eolun. In general, to add p-bit extra resolution, the oversampling frequency must be equal to:

![](images/40792d77987c31f28e0681c044c7ade9e774e0ec75c18afa00b74775d35aa9af.jpg)

# 3.2.1

# When does this method work?

In order to make this method work, the input signal must not vary by more than ± 0.5 LSB during the oversampling period and must not correlate with the triangular dither signal.

# 3.2.2

# Implementation method on STM32F1, STM32F3, and STM32Lx Series device

In order to implement the second solution, the following is needed:

Aeatial mplir  perr e su heu al and heringular wavefor. or amp inverter/summing stage is required. An STMicroelectronics LMV321 can be used.

A triangular waveform with a period of OSR times the ADC conversion rate. The user can either use a signal generatororoeof then-chiptimers and anCnetwork to generate thistringular sigal. Ide, the on-chip timer generates a PWM signal with a duty cycle varying from 0 to 100%. This PWM output can b fltered with anRCfiergenerat trigular ial varyifrom 0 toVDD.Inorder o genera amplitude of 0.5 LSB, then the output is first passed through a capacitor (to cut the DC component) and then divided by the prescaler R2/R3 (see Figure 1. Hardware requirements of oversampling by adding a triangular signal). This prescaler is equal to the ADC number of words.

The input signal must not be changed after the op-amp. For this reason, R1 should be equal to R3. Tesm  e pu al and eguath vrorh pu Vo is te positive eny the-mpAter heoverampld data ecoput hisoff  sutac t give the input signal estimation with an extra resolution.

![](images/560b5832a69b06d6a7a3d109a509bbc4402871978dbb01fe368a490a4b5e0c81.jpg)  
Figure 11. Hardware requirements of oversampling by adding a triangular signal

# 3.2.2.1

# Embedded-software flowchart for oversampling using triangular dither

The STM32F1 series, STM32F3 series and STM32Lx series on-chip ADC conversion frequency is fixed at 1 MHz. The ADC DMA channel is configured otransfer he number oversample inputs from heADC dat register to A MA triggered and the oversampled result is computed.

Thegeneral-urpoe timrT is use o generate heinput signal samplng equecy. For this, he TIM2 c the oversampling.h file by #define Input_Signal_Sampling_Period.

The triangular dither is generated using the timer TIM3 configured in PWM mode by updating the Capture Compare Register CCR1. The timer TIM3 period must be equal to the ADC conversion rate and CCR1 must be updated OSR times where OSR is the oversampling factor. To do this, the possible CCR1 values are first cud n soreinto RAM bufr, henhe MAranser usedate he CR1gisterie need for interrupts.

Notethat the ADC conversion rate limits the oversampling factor. For example, in the case where the ADC is a  MHz, he   iseti  6 Hz.T hav  pr   sheuelg the timer TIM3 must be equal to 55. The maximum number of additional bits is then 4.

When a TIM2 update nterrupt is triggered, he ADC andTIM3 DMA are reenabled and he converted ADCvalues can be treated to compute the new sample with the extra resolution bits. Figure 12 summarizes the implementation.

![](images/5b5e9f76c99236fe984ad79176b940dfa9ee7612469a8ddb804e8c561e59bbeb.jpg)  
Figure 12. Oversampling using triangular dither flowchart

For his method to work, the ipu sgnal must ot vary b more than ±.LB during theoversampling p. This means that for STM32F1 series, STM32F3 series or STM32Lx series devices operating from a 3.3 V VREF+ the maximum allowed variations of the input signal during the oversampling period is \~0.4 mV.

O eohe e atrngular waveor wit a plitde f . LB means a 0.m plitde when t the STM32F1 series, STM32F3 series or STM32Lx series from a 3.3 V VREF+. The application environment must therefore not be very noisy. Any disturbance of the triangular waveform has an impact on the computed oversampled data.

According themplementation, hetriangular waveform is enerateby means  theSTM32 timeran RC fhauuau with a 3.3 V amplitude. The division is done with the ratio R3/R2.

The embedded software related to this method is located in the TriangularDitherMethod directory.

# Comparison of software oversampling methods

Temeth basveaplngveragi whio oviehadital for each doubling o the oversampling rate.The maximum input fequency is drastically decreased with the additional number of additional bits.

FhoI input signal to make the signal toggle between two adjacent ADC codes. In general, he ADC thermal noiseis u htaltl whoua solution more cost effective.

The onmetho basen diherigheput alusggularwaveform an coputingeative pnbetwen quanti roviemoreublieveapling tev iye emakmed orua msto with the triangular signal and must not have avarition greater than 0. LSBduring the oversampling pe. However, external hardware is needed to add the input signal and the triangular waveform.

Tablesarizhe ai iffen bete he tmethos. Iisot possble  y hateme is hanehcmethodvanta  iaTe mus elec heha meets their application requirements (sampling frequency, number of effective bits, and so on).

Table 2. Oversampling using white noise versus oversampling using triangular dither   

<table><tr><td colspan="1" rowspan="1">Implementation conditions</td><td colspan="1" rowspan="1">Oversampling using white noise</td><td colspan="1" rowspan="1">Oversampling using triangular dither</td></tr><tr><td colspan="1" rowspan="1">Oversampling factor to add p bits to theADC on-chip resolution</td><td colspan="1" rowspan="1">4p</td><td colspan="1" rowspan="1">2.2P</td></tr><tr><td colspan="1" rowspan="1">Maximum input signal frequency</td><td colspan="1" rowspan="1">fADC max /(2.4P)</td><td colspan="1" rowspan="1">fADCmax/(2.2.(2P))</td></tr><tr><td colspan="1" rowspan="1">Dither signal</td><td colspan="1" rowspan="1">White noise with an amplitude of at least11 LSB</td><td colspan="1" rowspan="1">Triangular signal with an amplitude ofn+0.5LSB</td></tr><tr><td colspan="1" rowspan="1">External hardware</td><td colspan="1" rowspan="1">External white noise source needed ifthe input signal noise is not sufficient.</td><td colspan="1" rowspan="1">Triangular waveform generator: an on-chip timer can be used. In this case, anRC network is used to filter the PWMfrequency.An op-amp is needed to add thetriangular waveform and the input signal.</td></tr></table>

# 3.4

# Hints for software oversampling

# 3.4.1

# What is the maximum number of bits that can be added to the on-chip ADC resolution?

Itcan be easiy shown hat increasing the n-chi ADC resolution decreases the maximum fequency compnent of the input signal.

For example, when using the STM32F1 series, STM32F3 series or STM32Lx series ADC at 1 MHz and two additional bits are required by the application, then the maximum input frequency is divided by:

16 when using the white noise method (62.5 kHz)   
4 when using the triangular dither method (125 kHz).

For e omeths,he tation he pu gal oedurigan verampling per  OR t e ADCconversion rate. I the case the ADCis unning at 1 MHz, he ipu signal estimation s done over OSR µs. The signal must not vary by more than /2LSB for the white noise method and, by ±.5LSB for the trangular waveform method.

When using the white noise method, the maximum number of bits that can be added to the ADC resolution depends only on the input signal.

When using the triangular dither method, the maximum number of bits that can be added to the ADC dsot enypu alnchefegur al on the ADC and APB frequencies. The timer period should be equal to the ADC rate:

2x(2P) ≤ timer period P ≤ log2 (timer period / 2)

In our example, running the ADC with a rate of 1 µs causes the STM32F1 series to operate at 56 MHz, which ma  pmus ual Teht 4.

# 3.4.2

# Taking advantage of the STM32 DAC implementation

Some STM32F1 series, STM32F3 series and STM32Lx series devices come with a DAC (digital-to-analog converter) that can be used in the oversampling method to avoid the use of external components.

The DAC can be used in the two oversampling methods as follows:

In the first method, the DAC can be used to generate a white-noise waveform with programmable amplitude that can be injected into the input signal if noise is not suficient.The waveform is generated thanks to the implemented pseudorandom algorithm. For more details, refer to the STM32F1 series, STM32F3 series and STM32Lx series reference manuals.   
In the second method, the DAC can be used to generate the triangular waveform. This removes the need for any additional external RC circuitry to filter the timer PWM frequency.

Note:

This is not implemented in the software described in this application note.

# 3.4.3 Taking advantage of the STM32F1 series, STM32F3 series and STM32L4 series dual ADC mode implementation

In some STM32F1 series, STM32F3 series and STM32L4 series devices, the dual ADC mode is an interesting feature that alows twoADCs toconvert at the same time.Using the dual ADCfast intereave mode, thesame channel is converted alternately by ADC2 and ADC1. The time separating two successive samples is 7 ADC slv a ADC clock cycles that is every 0.5 µs when running the ADC at 14 MHz.

Note:

This hint is not implemented in the software given within the application note.

# 3.4.4

# Taking advantage of the hardware ADC oversampling implementation

O  devics, eDCplements he oversamplingfeatur hardwarehis featur re Section 4 Hardware oversampling, and a comparison between hardware and software oversampling in Section 5 Hardware versus software oversampling comparison.

# 4 Hardware oversampling

vpll Temabenefit hat heuser an et omhearwarovemplig eas R ialonoi with less CPU interaction, resulting in overll lower power consumption compared with the software-based implementation.

# Hardware oversampling feature overview

# Note:

This sctin concens he r noratin coul sghtlffrher products.Thede documentation should be consulted.

The hardware oversampling engineaccumulates the results f ADC conversions. The accumulatedoutput data can beright-shifd andronded) to provide elected bit-depth in elation to OR.Theoutput valu  o updated every sampling period but once N samples are accumulated, therefore, the output data rate is decimated by a factor of OSR.

The result is the average of accumulated samples as follows:

![](images/d8e5abffa406353af04c6e931ce31fbbce950968b3c82f351f58648acfa7ebc8.jpg)

Where both N and M can be adjusted:

N is the oversampling ratio. It is set with the OVFS[2:0] bits in the ADCCFGR2 register. I can be a actor between 2x and 256x.   
Mis the divisioncoefficin (right bit shif. It is et with the OVSS[3:0] bit in theADCCFGR2 egise. It can allow to right shift the sum up to 8 bits.

In the case of STM32L4 series, the oversampling engine begins summing N samples. The sum is then right value according to the bits removed by the shifting.

The final result is saved in the ADCDR data register and because of the 16-bit truncation, it cannot be represented on more than 16 bits.

# How to operate the bit-depth obtained with oversampling

When N samples of X bits are accumulated, the result can be coded on up to X + (In(N) / In(2)) bits.

Foealpl as  dla e will be on 20 bits since In(256) / In(2) = 8 and 12 + 8 = 20.

Next, the right shifting, which is up to 8 bits has to be taken into account.

all, the bit-depth is given by X + (n(N) / In(2) - M but is limited to 16 bits because of the truncatio

# Note:

The number of bits X for a sample depends on the product used and can be found in its datasheet.

TheAcculate naveragestagean ehought sa ki igi fler oftecalleacculatendump.Thefrequencyresonse  uch fle sequivalent ta fsorderCascaded-ntegrator-comb C Hogenauer filter. The frequency response in case of sampling frequency 1 MHz and OSR = 10 can be seen in Figure 13. Frequency response of accumulate-and-dump filter.

![](images/545097b9613b3ccf546658682a45b0d7491f22a21e6e62c8de4398c2d95d8f8a.jpg)  
Figure 13. Frequency response of accumulate-and-dump filter

A o powpas eyi atnepliqe pry I stivligheanoiultgsaloo

# 5 Hardware versus software oversampling comparison

The ADC oversampling method can be implemented by hardware or by developing a dedicated software routine.

The advantage of hardware implementation is that the total energy budget needed for processing the ADC auirmples isuincparisonhesotwareplementation wheel thedat processnges to be done by the core. However, the hardware oversampling unit is not available on every product.

Two test projects emulating he common data acquisition tasks have been developed and executed on the same system to evaluate the energy difference and to demonstrate how much energy can be saved by using the hardware oversampling.

# Software implementation

The project demonstrating the software oversampling implementation method consists of the following steps, which are repeated every 100 ms:

1. Configuring the system/data acquisition.   
2. Capturing  4 samples by ADC and storig them i the memory b usig DMA while the coreis nSleep   
low-power mode.   
3. Processing the data acquired by the CPU to get an oversampled value.   
4. Putting the system in Stop mode for the rest of the 100 ms interval.

# Hardware implementation

T pro howgheawaplnatiarrutheeaskecpt hat a po don by heADC overampling engi.Hence, teCPU can be activ uring he acqusition an oversapl

1. Configuring the system/data acquisition.   
2. Capturing of 64 samples and processing them by the ADC oversampling engine while the core is in Sleep low-power mode.   
3. Putting the system in Stop mode for the rest of the 100 ms interval.

# 5.3 Results

Tergy consuption r he data aquisition a processing ask,and he average curen consmptin o the whole 100 ms period for both demonstration projects are detailed in Table 3.

Table 3. Comparison of SW and HW implementation of ADC oversampling technique   

<table><tr><td rowspan=1 colspan=1>Implementation</td><td rowspan=1 colspan=1>Data acquisition andprocessing time</td><td rowspan=1 colspan=2>Acquisition task charge</td><td rowspan=1 colspan=1>Average current(during 100 ms)</td></tr><tr><td rowspan=1 colspan=1>Hardware</td><td rowspan=1 colspan=1>6.06 ms</td><td rowspan=1 colspan=1>896 pAh</td><td rowspan=1 colspan=1>3.23 μC</td><td rowspan=1 colspan=1>37 μA</td></tr><tr><td rowspan=1 colspan=1>Software</td><td rowspan=1 colspan=1>6.80 ms</td><td rowspan=1 colspan=1>1099 pAh</td><td rowspan=1 colspan=1>3.96 μC</td><td rowspan=1 colspan=1>44 μA</td></tr></table>

The hardware oversampling implementation can save about 20% of the energy consumed to complete the acquisition and data processing task with lower coding effort and CPU time.

# ENOB (effective number of bits) measurement

Tploe

Table 4. Formulas for ENOB improvement   

<table><tr><td rowspan=1 colspan=1>Method</td><td rowspan=1 colspan=1>Formula(X is the ADC resolution OSR is the oversampling ratio)</td></tr><tr><td rowspan=1 colspan=1>Hardware oversampling</td><td rowspan=1 colspan=1>Resolution = X + (In (OSR) / In(2)) - MM is the division coefficient of the hardware oversampling engine</td></tr><tr><td rowspan=1 colspan=1>Software oversampling with white noise</td><td rowspan=1 colspan=1>Resolution = X + p with OSR = 4p</td></tr><tr><td rowspan=1 colspan=1>Software oversampling with dithering</td><td rowspan=1 colspan=1>Resolution = X + p with OSR = 2*2p</td></tr></table>

I eei  fe . r an erealol akict potental osortin ruipeectis. Ioi gdati dynamic performance.

It g pace  haoluC its implementation and configuration.

Th O eyv Ienx ulat ik o parameters is use:SA (signal-tonoise and distortion ratio) and THD+ (total harmonicdistortion + noise).

The formulas are as follows:

![](images/6373b06121dce70aaee16868355d4cba936a34386ea6e36fc4442a7517d30e7b.jpg)

Full_scale_amp is the maximum amplitude that can be measured by the ADC.

Input_amp is the amplitude of the signal applied to the ADC.

Thuls esul  o euation .The iffencs that noie n ditortins e take t y ac RSNAeakiloser raliae otheinput signal used orENOBmeasurement s also taken intoaccounthanks tothe ratiFull-scalemp. I this has to be considered when computing a ratio featuring the level of this signal.

# Note:

If the bandwith of the measurement s DC to Fs/2 (the Nyquist bandwidth, Fs is the samplng fequency), THD + N is equal to SINAD. That is what we consider for the two formulas above.

"he following steps can be followed to measure the ENOB of an ADC:

With a high precision signal generator, inject a sinusoid on one of the tested ADC channels with a frequency respecting the maximums given in Table 2. Oversampling using white noise versus oversampling using triangular dither for software oversampling, or fADCmax/(2\*N) for hardware oversampling with N being the oversampling ratio of the oversampling engine. The sinusoid amplitude should be 90% of the ADC full-scale to avoid saturation. • Configure the ADC to acquire some samples of the signal. The best is to get a rounded number of the signal period. 4096 is a good example but might need to be adjusted in function of the frequency of the input signal. Make the successive binary codes operated by the ADC available for measurement (parallel/serial transmission, file recording...). Analyze the ADC measured signal with a frequency analyzer capable to do SINAD or THD+N measurement. With the SINAD or THD+N measurement features, get the value for one of these two parameters. Measuring both parameters enable doing a comparison of the ENOB values obtained. Apply the formula to determine the ENOB of the ADC (see Eq. (12) or Eq. (13)).

l a  lalyev been followed with the following equipment and tools.

The input snusoid has been generated with the analogoutputf the Audio Precision AP2722 Audio Analyzer. vl uavbea ee at AP2722 is 0-centered, so a conversion stage is needed to set its amplitude between 0 and 3.0 V (VDD=VDDA=3.3 V on STMicroelectronics EVAL and Nucleo boards).

# Note:

This conversion stage behaves like an HP filter and influences the signal measured by the ADC (lower signal resolution for lower frequencies). This can give a good representation of a real-life use case.

The STM32L476G-EVAL board has been used to process the ADC measurement and transmitting/recording it. The ADC sampling is done on the pin PA4 linked to the STM32L4 ADC1 Channel 9 and to ground through a .capacior  filr high frequency noisThis pi isavailableon the coneorN7 fhe VALbr.

The application running on the STM32L476G-EVAL board saves 4096 ADC samples in RAM thanks to the DMA peripheral.

The oversampling unit is used to analyze its effect and configured as presented in table 6.

e pT this timer is adjusted according to the oversampling configuration wanted.

When he 096 samples are saved, hey are transferrehrough theTM32UART interface o be ecover in file on a PC thanks to a Python script.

The resulting file is formatted so that it can be processed with MATLAB®.

T lhoe he hv e pl be able to keep a constant ADC clock frequency (80 MHz) and sampling time (12.5 cycles).

MATLAB® enables computing the SINAD or THD+N of the ADC signal. It has a native sinad function that i used t analyze the ADC signal saved into the file created previously. Then, applying eq.X gives us the ENOB measured.

hazvplvpln posls be wig coefficient to target the best resolution offered.

T b have beeareo eratvalu   l hi vely bha processed to achieve the 16-bite target.

Table 5. Theoretical ENOB values for hardware oversampling unit versus configuration   
olnthavehraveplgutut t.   

<table><tr><td rowspan=2 colspan=1>OSRIM</td><td rowspan=1 colspan=9>Hardware oversampling unit coefficient (M)(1)</td></tr><tr><td rowspan=1 colspan=1>0</td><td rowspan=1 colspan=1>1</td><td rowspan=1 colspan=1>2</td><td rowspan=1 colspan=1>3</td><td rowspan=1 colspan=1>4</td><td rowspan=1 colspan=1>5</td><td rowspan=1 colspan=1>6</td><td rowspan=1 colspan=1>7</td><td rowspan=1 colspan=1>8</td></tr><tr><td rowspan=1 colspan=1>2</td><td rowspan=1 colspan=1>13</td><td rowspan=1 colspan=1>12</td><td rowspan=1 colspan=1>11</td><td rowspan=1 colspan=1>10</td><td rowspan=1 colspan=1>9</td><td rowspan=1 colspan=1>8</td><td rowspan=1 colspan=1>7</td><td rowspan=1 colspan=1>6</td><td rowspan=1 colspan=1>5</td></tr><tr><td rowspan=1 colspan=1>4</td><td rowspan=1 colspan=1>14</td><td rowspan=1 colspan=1>13</td><td rowspan=1 colspan=1>12</td><td rowspan=1 colspan=1>11</td><td rowspan=1 colspan=1>10</td><td rowspan=1 colspan=1>9</td><td rowspan=1 colspan=1>8</td><td rowspan=1 colspan=1>7</td><td rowspan=1 colspan=1>6</td></tr><tr><td rowspan=1 colspan=1>8</td><td rowspan=1 colspan=1>15</td><td rowspan=1 colspan=1>14</td><td rowspan=1 colspan=1>13</td><td rowspan=1 colspan=1>12</td><td rowspan=1 colspan=1>11</td><td rowspan=1 colspan=1>10</td><td rowspan=1 colspan=1>9</td><td rowspan=1 colspan=1>8</td><td rowspan=1 colspan=1>7</td></tr><tr><td rowspan=1 colspan=1>16</td><td rowspan=1 colspan=1>16</td><td rowspan=1 colspan=1>15</td><td rowspan=1 colspan=1>14</td><td rowspan=1 colspan=1>13</td><td rowspan=1 colspan=1>12</td><td rowspan=1 colspan=1>11</td><td rowspan=1 colspan=1>10</td><td rowspan=1 colspan=1>9</td><td rowspan=1 colspan=1>8</td></tr><tr><td rowspan=1 colspan=1>32</td><td rowspan=1 colspan=1>17</td><td rowspan=1 colspan=1>16</td><td rowspan=1 colspan=1>15</td><td rowspan=1 colspan=1>14</td><td rowspan=1 colspan=1>13</td><td rowspan=1 colspan=1>12</td><td rowspan=1 colspan=1>11</td><td rowspan=1 colspan=1>10</td><td rowspan=1 colspan=1>9</td></tr><tr><td rowspan=1 colspan=1>64</td><td rowspan=1 colspan=1>18</td><td rowspan=1 colspan=1>17</td><td rowspan=1 colspan=1>16</td><td rowspan=1 colspan=1>15</td><td rowspan=1 colspan=1>14</td><td rowspan=1 colspan=1>13</td><td rowspan=1 colspan=1>12</td><td rowspan=1 colspan=1>11</td><td rowspan=1 colspan=1>10</td></tr><tr><td rowspan=1 colspan=1>128</td><td rowspan=1 colspan=1>19</td><td rowspan=1 colspan=1>18</td><td rowspan=1 colspan=1>17</td><td rowspan=1 colspan=1>16</td><td rowspan=1 colspan=1>15</td><td rowspan=1 colspan=1>14</td><td rowspan=1 colspan=1>13</td><td rowspan=1 colspan=1>12</td><td rowspan=1 colspan=1>11</td></tr><tr><td rowspan=1 colspan=1>256</td><td rowspan=1 colspan=1>20</td><td rowspan=1 colspan=1>19</td><td rowspan=1 colspan=1>18</td><td rowspan=1 colspan=1>17</td><td rowspan=1 colspan=1>16</td><td rowspan=1 colspan=1>15</td><td rowspan=1 colspan=1>14</td><td rowspan=1 colspan=1>13</td><td rowspan=1 colspan=1>12</td></tr></table>

Table 6. Practical ENOB measurement with the hardware oversampling unit versus configuration   
Bolnvevu i a.   

<table><tr><td rowspan=2 colspan=1>OSR</td><td rowspan=1 colspan=9>Hardware oversampling unit coefficient (M)(1)</td></tr><tr><td rowspan=1 colspan=1>0</td><td rowspan=1 colspan=1>1</td><td rowspan=1 colspan=1>2</td><td rowspan=1 colspan=1>3</td><td rowspan=1 colspan=1>4</td><td rowspan=1 colspan=1>5</td><td rowspan=1 colspan=1>6</td><td rowspan=1 colspan=1>7</td><td rowspan=1 colspan=1>8</td></tr><tr><td rowspan=1 colspan=1>2</td><td rowspan=1 colspan=1>13</td><td rowspan=1 colspan=1>12</td><td rowspan=1 colspan=1>11</td><td rowspan=1 colspan=1>10</td><td rowspan=1 colspan=1>9</td><td rowspan=1 colspan=1>8</td><td rowspan=1 colspan=1>7</td><td rowspan=1 colspan=1>6</td><td rowspan=1 colspan=1>5</td></tr><tr><td rowspan=1 colspan=1>4</td><td rowspan=1 colspan=1>14</td><td rowspan=1 colspan=1>13</td><td rowspan=1 colspan=1>12</td><td rowspan=1 colspan=1>11</td><td rowspan=1 colspan=1>10</td><td rowspan=1 colspan=1>9</td><td rowspan=1 colspan=1>8</td><td rowspan=1 colspan=1>7</td><td rowspan=1 colspan=1>6</td></tr><tr><td rowspan=1 colspan=1>8</td><td rowspan=1 colspan=1>15</td><td rowspan=1 colspan=1>14</td><td rowspan=1 colspan=1>13</td><td rowspan=1 colspan=1>12</td><td rowspan=1 colspan=1>11</td><td rowspan=1 colspan=1>10</td><td rowspan=1 colspan=1>9</td><td rowspan=1 colspan=1>8</td><td rowspan=1 colspan=1>7</td></tr><tr><td rowspan=1 colspan=1>16</td><td rowspan=1 colspan=1>16</td><td rowspan=1 colspan=1>15</td><td rowspan=1 colspan=1>14</td><td rowspan=1 colspan=1>13</td><td rowspan=1 colspan=1>12</td><td rowspan=1 colspan=1>11</td><td rowspan=1 colspan=1>10</td><td rowspan=1 colspan=1>9</td><td rowspan=1 colspan=1>8</td></tr><tr><td rowspan=1 colspan=1>32</td><td rowspan=1 colspan=1>•</td><td rowspan=1 colspan=1>16</td><td rowspan=1 colspan=1>15</td><td rowspan=1 colspan=1>14</td><td rowspan=1 colspan=1>13</td><td rowspan=1 colspan=1>12</td><td rowspan=1 colspan=1>11</td><td rowspan=1 colspan=1>10</td><td rowspan=1 colspan=1>9</td></tr><tr><td rowspan=1 colspan=1>64</td><td rowspan=1 colspan=1>-</td><td rowspan=1 colspan=1>•</td><td rowspan=1 colspan=1>16</td><td rowspan=1 colspan=1>15</td><td rowspan=1 colspan=1>14</td><td rowspan=1 colspan=1>13</td><td rowspan=1 colspan=1>12</td><td rowspan=1 colspan=1>11</td><td rowspan=1 colspan=1>10</td></tr><tr><td rowspan=1 colspan=1>128</td><td rowspan=1 colspan=1></td><td rowspan=1 colspan=1></td><td rowspan=1 colspan=1>•</td><td rowspan=1 colspan=1>16</td><td rowspan=1 colspan=1>15</td><td rowspan=1 colspan=1>14</td><td rowspan=1 colspan=1>13</td><td rowspan=1 colspan=1>12</td><td rowspan=1 colspan=1>11</td></tr><tr><td rowspan=1 colspan=1>256</td><td rowspan=1 colspan=1>•</td><td rowspan=1 colspan=1>•</td><td rowspan=1 colspan=1>•</td><td rowspan=1 colspan=1>-</td><td rowspan=1 colspan=1>16</td><td rowspan=1 colspan=1>15</td><td rowspan=1 colspan=1>14</td><td rowspan=1 colspan=1>13</td><td rowspan=1 colspan=1>12</td></tr></table>

Table 7. Practical ENOB measurement with the hardware oversampling unit versus configuration   

<table><tr><td rowspan=2 colspan=1>OSR</td><td rowspan=1 colspan=2>Software oversampling with white noise</td><td rowspan=1 colspan=2>Software oversampling with dithering</td></tr><tr><td rowspan=1 colspan=1>Theoretical resolution</td><td rowspan=1 colspan=1>Practical ENOB</td><td rowspan=1 colspan=1>Theoretical resolution</td><td rowspan=1 colspan=1>Practical ENOB</td></tr><tr><td rowspan=1 colspan=1>2</td><td rowspan=1 colspan=1>•</td><td rowspan=1 colspan=1></td><td rowspan=1 colspan=1>12</td><td rowspan=1 colspan=1></td></tr><tr><td rowspan=1 colspan=1>4</td><td rowspan=1 colspan=1>13</td><td rowspan=1 colspan=1></td><td rowspan=1 colspan=1>13</td><td rowspan=1 colspan=1></td></tr><tr><td rowspan=1 colspan=1>8</td><td rowspan=1 colspan=1>:</td><td rowspan=1 colspan=1></td><td rowspan=1 colspan=1>14</td><td rowspan=1 colspan=1></td></tr><tr><td rowspan=1 colspan=1>16</td><td rowspan=1 colspan=1>14</td><td rowspan=1 colspan=1></td><td rowspan=1 colspan=1>15</td><td rowspan=1 colspan=1></td></tr><tr><td rowspan=1 colspan=1>32</td><td rowspan=1 colspan=1>:</td><td rowspan=1 colspan=1></td><td rowspan=1 colspan=1>16</td><td rowspan=1 colspan=1></td></tr><tr><td rowspan=1 colspan=1>64</td><td rowspan=1 colspan=1>15</td><td rowspan=1 colspan=1></td><td rowspan=1 colspan=1>17</td><td rowspan=1 colspan=1></td></tr><tr><td rowspan=1 colspan=1>128</td><td rowspan=1 colspan=1>:</td><td rowspan=1 colspan=1></td><td rowspan=1 colspan=1>18</td><td rowspan=1 colspan=1></td></tr><tr><td rowspan=1 colspan=1>256</td><td rowspan=1 colspan=1>16</td><td rowspan=1 colspan=1></td><td rowspan=1 colspan=1>19</td><td rowspan=1 colspan=1></td></tr></table>

Asmentioned before, the signal test input is a 3.0Vpp sinusoid and the sampling rate is .5 kHz. Thus, t e yri heol avbees500 Hz 1 Hz 1 Hz,  Hz, .z.

Table 8. Effect of oversampling on ENOB   

<table><tr><td rowspan=2 colspan=1>OVS ration</td><td rowspan=2 colspan=1>OVS right shift</td><td rowspan=2 colspan=1>OVS left shift</td><td rowspan=1 colspan=5>ENOB</td></tr><tr><td rowspan=1 colspan=1>500 Hz</td><td rowspan=1 colspan=1>1 kHz</td><td rowspan=1 colspan=1>1.5 kHz</td><td rowspan=1 colspan=1>2 kHz</td><td rowspan=1 colspan=1>2.5 kHz</td></tr><tr><td rowspan=1 colspan=1>None</td><td rowspan=1 colspan=1>None</td><td rowspan=1 colspan=1>None</td><td rowspan=1 colspan=1>10.4126</td><td rowspan=1 colspan=1>10.3622</td><td rowspan=1 colspan=1>10.3543</td><td rowspan=1 colspan=1>10.2774</td><td rowspan=1 colspan=1>10.3084</td></tr><tr><td rowspan=1 colspan=1>2</td><td rowspan=1 colspan=1>None</td><td rowspan=1 colspan=1>3</td><td rowspan=1 colspan=1>10.6245</td><td rowspan=1 colspan=1>10.6302</td><td rowspan=1 colspan=1>10.9172</td><td rowspan=1 colspan=1>10.8618</td><td rowspan=1 colspan=1>10.9524</td></tr><tr><td rowspan=1 colspan=1>4</td><td rowspan=1 colspan=1>None</td><td rowspan=1 colspan=1>2</td><td rowspan=1 colspan=1>10.9567</td><td rowspan=1 colspan=1>11.2234</td><td rowspan=1 colspan=1>11.2249</td><td rowspan=1 colspan=1>11.3322</td><td rowspan=1 colspan=1>11.3531</td></tr><tr><td rowspan=1 colspan=1>8</td><td rowspan=1 colspan=1>None</td><td rowspan=1 colspan=1>1</td><td rowspan=1 colspan=1>11.1692</td><td rowspan=1 colspan=1>11.3454</td><td rowspan=1 colspan=1>11.4646</td><td rowspan=1 colspan=1>11.5817</td><td rowspan=1 colspan=1>11.7653</td></tr><tr><td rowspan=1 colspan=1>16</td><td rowspan=1 colspan=1>None</td><td rowspan=1 colspan=1>None</td><td rowspan=1 colspan=1>11.2158</td><td rowspan=1 colspan=1>11.4962</td><td rowspan=1 colspan=1>11.6551</td><td rowspan=1 colspan=1>11.8414</td><td rowspan=1 colspan=1>11.9138</td></tr><tr><td rowspan=1 colspan=1>32</td><td rowspan=1 colspan=1>1</td><td rowspan=1 colspan=1>None</td><td rowspan=1 colspan=1>11.2718</td><td rowspan=1 colspan=1>11.6126</td><td rowspan=1 colspan=1>11.8103</td><td rowspan=1 colspan=1>12.0408</td><td rowspan=1 colspan=1>12.2725</td></tr><tr><td rowspan=1 colspan=1>64</td><td rowspan=1 colspan=1>2</td><td rowspan=1 colspan=1>None</td><td rowspan=1 colspan=1>11.3109</td><td rowspan=1 colspan=1>11.6220</td><td rowspan=1 colspan=1>11.8968</td><td rowspan=1 colspan=1>12.1124</td><td rowspan=1 colspan=1>12.3626</td></tr><tr><td rowspan=1 colspan=1>128</td><td rowspan=1 colspan=1>3</td><td rowspan=1 colspan=1>None</td><td rowspan=1 colspan=1>11.3259</td><td rowspan=1 colspan=1>11.6568</td><td rowspan=1 colspan=1>11.9050</td><td rowspan=1 colspan=1>12.1579</td><td rowspan=1 colspan=1>12.6038</td></tr><tr><td rowspan=1 colspan=1>256</td><td rowspan=1 colspan=1>4</td><td rowspan=1 colspan=1>None</td><td rowspan=1 colspan=1>11.3582</td><td rowspan=1 colspan=1>11.7032</td><td rowspan=1 colspan=1>11.9301</td><td rowspan=1 colspan=1>12.2419</td><td rowspan=1 colspan=1>12.8259</td></tr></table>

# Note:

Forreference, ater theconversion stage and at the ADC pin level, the following THD+N valus weremese: -8.5 dB at 500 Hz (this is equivalent o 13.55 ENOB according to eq.Y), -93 dB at 1 kHz (15.29 ENOB), -96 dB at 1.5 kHz (15.79 ENOB), -97 dB at 2 kHz (15.96 ENOB) and -98 dB at 2.5 kHz (16.12 ENOB). At the audio precision analyzer output, which is before the conversion stage, -105 dB were measured (17.28 ENOB).

In the STM32L476 datasheet, it is given that the typical ENOB of the ADC is 10.5 (the ADC is configured as single-ended).

Thus,Table 8hows that  is possible oget over his typical value and even over he real ADC resolutin. However, the theoretical 16-bit target stays far from the results and corresponds more to an idea of the performance of the oversampling configuration.

The result also highlights that a higheroversampling rato gives a better ENOB despite lmiting the ampling frequency and so the input signal frequency.

# 7 Conclusion

This application note has explained the basics of the oversampling technique used to improve the SNR performances (and thus the effective resolution) of ADCs integrated in most of the STM32 microcontrollers.

The cornerstones of the oversampling technique are:

The RMS quantization noise of an ADC is q / (12), over the Nyquist bandwidth (q is the ADC quantum:   
LSB value   
If the wanted bandwidth is smaller than the Nyquist bandwidth, the quantization noise is reduced in   
proportion by using a filter to remove the out of band noise   
Dithering can be used if the quantization noise does not behave like a wideband noise

The hardware implementation of the ADC oversampling technique reduces the time and energy needed by the CPU for the data processing tasks. It results in lowering the overall power consumption.

Wpllly the technique via software as it has been presented in this document.

T c veramplingn he effective ADC esolution NOB) has also beenanalyz. With overamplt is possible to get the effective resolution over the real one.

# Revision history

Table 9. Document revision history   

<table><tr><td>Date</td><td>Version</td><td>Changes</td></tr><tr><td>25-Sep-2023</td><td>1</td><td>Initial version.</td></tr></table>

# Contents

# 1 General information

# Oversampling as a way to improve the quality of signal acquisition 3

2.1 Quantization of noise and signal-to-noise ratio 3   
2.2 Nyquist theorem and antialiasing low-pass filter relaxation   
2.3 Processing gain achievable with oversampling .   
2.4 Dithering. 5

# Software oversampling

3.1 Oversampling using white noise

3.1.1 Oversampled signal SNR with white input noise   
3.1.2 Decimation   
3.1.3 When is this method efficient?.   
3.1.4 Implementation method on STM32F1, STM32F3, and STM32Lx series devices. . . . . . 8

# 3.2 Oversampling using triangular dither 12

3.2.1 When does this method work? 12   
3.2.2 Implementation method on STM32F1, STM32F3, and STM32Lx Series devices . . . . 12

3 Comparison of software oversampling methods 14

# 3.4 Hints for software oversampling 15

3.4.1 What is the maximum number of bits that can be added to the on-chip ADC resolution? . 15 3.4.2 Taking advantage of the STM32 DAC implementation 15 3.4.3 Taking advantage of the STM32F1 series, STM32F3 series and STM32L4 series dual ADC mode implementation 15

# 3.4.4 Taking advantage of the hardware ADC oversampling implementation . 16

# Hardware oversampling. .17

4.1 Hardware oversampling feature overview. 17

# Hardware versus software oversampling comparison 19

5.1 Software implementation 19   
5.2 Hardware implementation 19   
5.3 Results 19

# ENOB (effective number of bits) measurement 20

# 7 Conclusion .24

Revision history .25

List of tables 27

# List of figures. 28

# List of tables

Table 1. Applicable products 1   
Table 2. Oversampling using white noise versus oversampling using triangular dither . 14   
Table 3. Comparison of SW and HW implementation of ADC oversampling technique. 19   
Table 4. Formulas for ENOB improvement. 20   
Table 5. Theoretical ENOB values for hardware oversampling unit versus configuration 21   
Table 6. Practical ENOB measurement with the hardware oversampling unit versus configuration 22   
Table 7. Practical ENOB measurement with the hardware oversampling unit versus configuration 22   
Table 8. Effect of oversampling on ENOB 22   
Table 9. Document revision history . 25

# List of figures

Figure 1. Ideal N-bit ADC quantization 3   
Figure 2. Quantization noise spectrum 4   
Figure 3. Quantization noise gain. 5   
Figure 4. Dithering technique. 5   
Figure 5. Histogram analysis 8   
Figure 6. Histogram analysis for DC = 1.65 V . 9   
Figure 7. Oversampling using a white noise flowchart 10   
Figure 8. Ramp samples with 1 additional bit . 11   
Figure 9. Ramp samples with 2 additional bits 11   
Figure 10. How to perform oversampling by adding a triangular signal 12   
Figure 11. Hardware requirements of oversampling by adding a triangular signal. 13   
Figure 12. Oversampling using triangular dither flowchart 14   
Figure 13. Frequency response of accumulate-and-dump filter. 18

# IMPORTANT NOTICE  READ CAREFULLY

pt old ursant  dits   leole.

purchasers' products.

No license, express or implied, to any intellectual property right is granted by ST herein.

are the property of their respective owners.

I

© 2023 STMicroelectronics - All rights reserved