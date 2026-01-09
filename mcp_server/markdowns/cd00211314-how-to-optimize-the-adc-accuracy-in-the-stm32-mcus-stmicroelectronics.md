# Introduction

STM32 MCUs embed advanced 12-bit to 16-bit ADCs depending on the device. A selfcalibration feature is provided to enhance ADC accuracy versus environmental condition changes.

In applications involving analog-to-digital conversion, ADC accuracy has an impact on the overall system quality and efficiency. To improve this accuracy, the errors associated with the ADC and the parameters affecting them must be understood.

ADC accuracy does not only depend on ADC performance and features, but also on the overall application design around the ADC.

This application note aim is to help understand ADC errors and explain how to enhance ADC accuracy. It is divided into three main parts:

A simplified description of ADC internal structure to help understand ADC operation and related ADC parameters. Explanations of the different types and sources of ADC errors, related to the ADC design and to external ADC parameters, such as the external hardware design. Recommendations on how to minimize these errors, focusing on hardware and software methods.

# Contents

General information 6

ADC internal principle . . . 6

2.1 SAR ADC internal structure 6

# ADC errors .. 9

3.1 Errors due to the ADC itself 9

3.1.1 Offset error . . 9   
3.1.2 Gain error. 11   
3.1.3 Differential linearity error 12   
3.1.4 Integral linearity error . 13   
3.1.5 Total unadjusted error 14

# 3.2 Errors due to the ADC environment 14

3.2.1 Reference voltage noise 14   
3.2.2 Reference voltage / power supply regulation 15   
3.2.3 Reference voltage decoupling and impedance 15   
3.2.4 External reference voltage parameters 16   
3.2.5 Analog input signal noise 16   
3.2.6 ADC dynamic range bad match for maximum input signal amplitude . . 16   
3.2.7 Effect of the analog signal source resistance 16   
3.2.8 Effect of source capacitance and parasitic capacitance of the PCB . . . 17   
3.2.9 Injection current effect 18   
3.2.10 Temperature influence 18   
3.2.11 I/O pin crosstalk . 18   
3.2.12 EMI-induced noise 19

# How to optimize the ADC accuracy . . 20

4.1 Reduce the effects of the ADC-related ADC errors 20

4.2 Minimize the ADC errors related to the ADC external environment . . . . . 20

4.2.1 Reference voltage / power supply noise minimization . . 20   
4.2.2 Reference voltage / power supply regulation 22   
4.2.3 Analog-input signal noise elimination 22   
4.2.4 Adding white noise or triangular sweep to improve resolution . . .23   
4.2.5 Matching the ADC dynamic range to the maximum signal amplitude . . 24   
4.2.6 SAR ADC sampling time prerequisites 25   
4.2.7 External analog buffer usage 34   
4.2.8 Source frequency condition vs. source and parasitic capacitors . . . . 34   
4.2.9 Temperature-effect compensation 35   
4.2.10 Minimizing injection current 35   
4.2.11 Minimizing I/O pin crosstalk 35   
4.2.12 EMI-induced noise reduction 36   
4.2.13 PCB layout recommendations 37   
4.2.14 Component placement and routing 39

4.3 Software methods to improve precision 39

4.3.1 Averaging samples . 39   
4.3.2 Digital signal filtering 40   
4.3.3 FFT for AC measurement 40   
4.3.4 ADC calibration 41   
4.3.5 Minimizing internal CPU noise 41

4.4 High impedance source measurement . 41

4.4.1 ADC input stage problem . . . .41   
4.4.2 Explanation of the behavior .43   
4.4.3 Minimizing additional errors 44   
4.4.4 Source of described problem - ADC design .48

Conclusion . . 50

Revision history 51

# List of tables

Table 1. Minimum sampling time for STM32H7 series devices (in ns). 29   
Table 2. Examples of ADC SMP selection vs STM32 Series (in ADC clock cycles) 30   
Table 3. Rounded minimum sampling time vs resolution and maximum error (in ADC clock cycles) . 30   
Table 4. Minimum SMP values vs resolution and maximum error (in ADC clock cycles) . . . 31   
Table 5. Additional ADC clock cycles due to SMP vs resolution and maximum error . 31   
Table 6. Minimum ADC conversion time (TSMPL + TSAR) vS resolution and maximum error (in ADC clock cycles) . . 31   
Table 7. Maximum ADC output sampling rate (MSPS) vs resolution and maximum error 32   
Table 8. Document revision history 51

# List of figures

Figure 1. Basic schematic of SAR switched-capacitor ADC (example of 10-bit ADC). .6   
Figure 2. Sample state. .7   
Figure 3. Hold state 7   
Figure 4. Step 1: Compare with VREF/2 8   
Figure 5. Step 2: If MSB = 0, then compare with 1/VREF 8   
Figure 6. Step 2: If MSB = 1, then compare with 3/4VREF 9   
Figure 7. Positive offset error representation. 10   
Figure 8. Negative offset error representation 10   
Figure 9. Positive gain error representation. 11   
Figure 10. Negative gain error representation . 12   
Figure 11. Differential linearity error representation. 12   
Figure 12. Integral linearity error representation 13   
Figure 13. Total unadjusted error. 14   
Figure 14. Input signal amplitude vs. ADC dynamic range (VREF+ = 3.3 V) 16   
Figure 15. Analog signal source resistance effect . 17   
Figure 16. Aa iu    C 17   
Figure 17. Effect of injection current 18   
Figure 18. Crosstalk between I/O pins. 19   
Figure 19. EMI sources 19   
Figure 20. Power supply and reference decoupling for 100- and 144-pin packages. 21   
Figure 21. Power supply decoupling for 36-, 48- and 64-pin packages. 22   
Figure 22. Simple quasi-triangular source using a microcontroller output. 24   
Figure 23. Selecting the reference voltage 25   
Figure 24. Preamplification 25   
Figure 25. SAR ADC sample conversion process. 26   
Figure 26. Simplified external/internal SAR ADC sampling diagram . 27   
Figure 27. Example of SAR ADC input sampling time vs ADC resolution . 28   
Figure 28. Example of SAR ADC input sampling time vs accuracy . . 29   
Figure 29. TSMPL estimation versus ADC frequency and comparison of minimum TSMPL duration   
for slow and fast channels with same RAiN/CAIN .. 33   
Figure 30. TSMPL estimation versus ADC frequency and comparison of minimum TSMPL duration   
for fast channels with RAIN/CAIN = 51 Ω/10 pf and 100 Ω/33 pF 33   
Figure 31. 35   
Figure 32. Crosstalk between I/O pins.. 36   
Figure 33. Shielding technique 36   
Figure 34. Separating the analog and digital layouts . 37   
Figure 35. Separating the analog and digital supplies. 38   
Figure 36. Typical voltage source connection to ADC input 42   
Figure 37. Noise observed on ADC input pin during ADC conversions. 42   
Figure 38. ADC simplified schematic of input stage - sample and hold circuit. 43   
Figure 39. ADC input pin noise spikes from internal charge during sampling process 43   
Figure 40. Effect of sampling time extension . . 44   
Figure 41. Charging the external capacitor with too short time between conversions. 45   
Figure 42. Implementation of sampling switch. . 48   
Figure 43. Parasitic capacitances of sampling switch 49   
Figure 44. Parasitic current example inside ADC structure 49

# 1 General information

This application note applies to STM32 Arm©a)-based microcontrollers.

# 2

# ADC internal principle

# 2.1

# SAR ADC internal structure

The ADC embedded in STM32 microcontrollers uses the SAR (successive approximation register) principle, by which the conversion is performed in several steps. The number of conversion steps is equal to the number of bits in the ADC converter. Each step is driven by the ADC clock. Each ADC clock produces one bit from result to output. The ADC internal design is based on the switched-capacitor technique.

The following figures (Figure 1 to Figure 6) explain the principle of ADC operation. The example given below shows only the first steps of approximation but the process continues until the LSB is reached.

![](images/0442d66b2c623459f87e2264a8b29fb24449fe8a792485e97b30b9b892eea012.jpg)  
Figure 1. Basic schematic of SAR switched-capacitor ADC (example of 10-bit ADC)

Basic ADC schematic with digital output.

![](images/898289c74e2c05d826e6cb636a73991f74e0b181dcde7b98392c33a8381774e8.jpg)  
Figure 2. Sample state   
a  cou time..

![](images/fa1fa75357019357ec794f33f1cbe68cebb1ba4af98fdb50494777782b4c5699.jpg)  
Figure 3. Hold state   
Hold state: the input is disconnecte Capacitors hold the input voltage. Sb switch is open, then S1-S11

![](images/f840fbd7c3a5179bb97d79beabf976a26adbb59327d43efbcf5a83a81eae4f0e.jpg)  
Figure 4. Step 1: Compare with VREF/2

F ppoimaion ied

![](images/4d212e958e80ac169a505ed355a245bc5512acbf80393798432ba5a212a8432f.jpg)  
=

![](images/6641caba5e63ff4f74a743177dcb270264d4b1f01d3c6c4652d712acddbe5ac1.jpg)  
  
ne

# ADC errors

This section lists the main errors that have an effect on A/D conversion accuracy. These types of errors occur in all A/D converters and conversion quality depends on their elimination. These error values are specified in the ADC characteristics section of STM32 microcontroller datasheets.

Different accuracy error types are specified for the STM32 ADC. For easy reference, accuracy errors are expressed as multiples of one1 LSB. The resolution in terms of voltage depends on the reference voltage. The error in terms of voltage is calculated by multiplying the number of LSBs by the voltage corresponding to 1 LSB:

1 LSB = VREF+/2 or VDDA/2 for an N-bit ADC

# 3.1 Errors due to the ADC itself

# 3.1.1 Offset error

The offset error is the deviation between the first actual transition and the first ideal transition. The first transition occurs when the digital ADC output changes from 0 to 1. Ideally, when the analog input ranges between 0.5 LSB and 1.5 LSB, the digital output must be 1. Stillideally, the first transition occurs at 0.5 LSB. The offset error is denoted by Eo. The offset error can easily be calibrated by the application firmware.

# Example

For the STM32 ADC, the smallest detectable incremental change in voltage is expressed in terms of LSBs:

1 LSB = VREF+/4096 (on some packages, VREF+ = VDDA).

If VREF+ = 3.3 V, the input of 402.8 µV (0.5 LSB = 0.5 × 805.6 µV) must ideally lead to the generation of a digital output of 1. In practice, however, the ADC may still provide a reading of 0. If a digital output of 1 is obtained from an analog input of 550 µV, then:

Offset error = Actual transition - Ideal transition Eo = 550 μV - 402.8 µV = 141.2 µV Eo = 141.2 µV / 805.6 µV = 0.17 LSB

When an analog input voltage greater than 0.5 LSB generates the first transition, the offset error is positive (refer to Figure 7 for an example of positive offset error).

![](images/50487f17bf075defda2fcd1727d0b3ae4a1555ae7632c9ab66c1fed5c725ba81.jpg)  
Figure 7. Positive offset error representation

The error offset, Eo, is shown in magenta.

When an analog input voltage of less than 0.5 LSB generates the first transition, the offset error is negative (refer to Figure 8 for an example of negative offset error).

If the analog input voltage (VAiN) is equal to VssA and the ADC generates a nonzero digital output, the offset error is negative. This means that a negative voltage generates the first transition.

![](images/31426a207abcb3803b1635a35202ec26f2d5c2961e89b03f8eb5d058d4ec4106.jpg)  
Figure 8. Negative offset error representation

The error offset, Eo, is shown in magenta.

# 3.1.2 Gain error

The gain error is the deviation between the last actual transition and the last ideal transition.   
It is denoted by EG.

The last actual transition is the transition from OxFFE to OxFFF. Ideally, there must be a transition from OxFFE to OxFFF when the analog input is equal to VREF+ - 0.5 LSB. So, for VREF+= 3.3 V, the last ideal transition must occur at 3.299597 V.

If the ADC provides the OxFFF reading for VAIN < VREF+ - 0.5 LSB, then a negative gain error is obtained.

# Example

The gain error is obtained by the formula below:

EG = Last actual transition - ideal transition

If VREF+ = 3.3 V and VAIN = 3.298435 V generate a transition from 0xFFE to 0xFFF then: EG = 3.298435 V - 3.299597 V EG = -1162 μV EG = (-1162 µV / 805.6 V) LSB = -1.44 LSB

If a full-scale reading (OxFFF) is not obtained for VAiN equal to VREF+, the gain error is positive. This means that a voltage greater than VREF+ causes the last transition. Figure 9 shows a positive gain error while Figure 10 shows a negative gain error.

![](images/fa48d2d95e2ec200ff61255dd975b0fc673d1e96d9753d78afa9938db3e76d24.jpg)  
Figure 9. Positive gain error representation

ai5477b

![](images/3fa3a578b04368a9c5e31bf686e5897c440515398bc565f2f0fcfdeb47b52927.jpg)  
Figure 10. Negative gain error representation

The gain error, Eg, is shown in magenta.

# 3.1.3 Differential linearity error

The differential linearity error (DLE) is the maximum deviation between the actual and ideal steps. Here 'ideal' does not refer to the ideal transfer curve but to the ADC resolution. The DLE is denoted by ED. It is represented in Figure 11.

ED = Actual step width - 1 LSB

Ideally, an analog input voltage change of 1 LSB must cause a change in the digital code. If an analog input voltage greater than 1 LSB is required for a change in digital code, a differential linearity error is observed. The DLE therefore corresponds to the maximum additional voltage that is required to change from one digital code to the next.

The DLE is also known as the differential nonlinearity (DNL) error.

# Example

A given digital output must correspond to an analog input range. Ideally, the step width must be 1 LSB. Let us assume that the digital output is the same over an analog input voltage range of 1.9998 V to 2.0014 V. The step width is:

2.0014 V - 1.9998 V = 1.6 mV.

ED is thus the voltage difference between the higher (2.0014 V) and the lower (1.9998 V) analog voltages minus the voltage corresponding to 1 LSB.

![](images/4d386bbf5a85f868b20ba165e71d100e7cfc528fe356b55c2c7bfe9e79cf5cea.jpg)  
Figure 11. Differential linearity error representation

The differential linearity error, ED, is shown in magenta.

If VREF+ = 3.3 V, an analog input of 1.9998 V (0x9B2) can provide results varying between 0x9B1 and Ox9B3. Similarly, for an input of 2.0014 V (0x9B4), the results may vary between 0x9B3 and 0x9B5.

As a result, the total voltage variation corresponding to the Ox9B3 step is: 0x9B4 - 0x9B2, that is, 2.0014 V - 1.9998 V = 1.6 mV (1660 μV) ED = 1660 μV - 805.6 μV ED = 854.4 μV ED = (854.4 µV/805.6 µV) LSB ED = 1.06 LSB

# 3.1.4 Integral linearity error

The integral linearity error is the maximum deviation between any actual transition and the endpoint correlation line. The ILE is denoted by EL. It is represented in Figure 12.

The endpoint correlation line can be defined as the line on the A/D transfer curve that connects the first actual transition with the last actual transition. E_ is the deviation from this line for each transition. The endpoint correlation line thus corresponds to the actual transfer curve and has no relation to the ideal transfer curve.

The ILE is also known as the integral nonlinearity error (INL). The ILE is the integral of the DLE over the whole range.

![](images/7f5a95c4d0a15cc8552fffe17b983343190e255a0c1267723a259f9b32ddccdf.jpg)  
Figure 12. Integral linearity error representation

The integral linearity error, EL, is shown in magenta.

# Example

If the first transition from 0 to 1 occurs at 550 µV and the last transition (0xFFE to 0xFFF) occurs at 3.298435 V (gain error), then the line on the transfer curve that connects the actual digital codes Ox1 and OxFFF is the endpoint correlation line.

# 3.1.5 Total unadjusted error

The total unadjusted error (TUE) is the maximum deviation between the actual and the ideal transfer curves. This parameter specifies the total errors that may occur, thus causing the maximum deviation between the ideal digital output and the actual digital output. TUE is the maximum deviation recorded between the ideal expected value and the actual value obtained from the ADC for any input voltage.

The TUE is denoted by ET. It is represented in Figure 13.

The TUE is not the sum of Eo, EG. EL, ED. The offset error affects the digital result at lower voltages whereas the gain error affects the digital output for higher voltages.

# Example

If VREF+ = 3.3 V and VAIN = 2 V, the ideal result is Ox9B2. TUE = absolute (actual value - ideal case value) = 0x9B4 - 0x9B2 = 0x2 = 2 LSB

![](images/e8e62555e7459ad997d00969e20096998305ee7f4b7bc3f601bae01a08004b78.jpg)  
Figure 13. Total unadjusted error

The total unadjusted error, ET, is shown in magenta.

# 3.2

# Errors due to the ADC environment

# 3.2.1 Reference voltage noise

As the ADC output is the ratio between the analog signal voltage and the reference voltage, any noise on the analog reference causes a change in the converted digital value. VDDA analog power supply is used on some packages as the reference voltage (VrEF+), so the quality of VDDA power supply has an influence on ADC error.

For example, with an analog reference of 3.3 V (VREF+ = VDDA) and a 1 V signal input, the converted result is:

![](images/768963c934e5b6f143a5c87e81b650a308ac30962c99e5df4a8ea9eb62ae7c90.jpg)

However, with a 40 mV peak-to-peak ripple in the analog reference, the converted value becomes:

(1/3.34) × 4096 = 0x4CA (with VREF+ at its peak). Error = 0x4D9 - 0x4CA = 15 LSB

The SMPS (switch-mode power supply) usually embeds internal fast-switching power transistors. This introduces high-frequency noise in the output. The switching noise is in the range of 15 kHz to 1 MHz.

# 3.2.2 Reference voltage / power supply regulation

Power supply regulation is very important for ADC accuracy since the conversion result is the ratio of the analog input voltage to the VREF+ value.

If the power supply output decreases when connected to VDDA or VREF+ due to the loads on these inputs and to its output impedance, an error is introduced in the conversion result.

Digital code VAIN(2^N) , where N is the resolution of the ADC (in our case N = 12 and VREF+   
digital code range = [0 to (2N-1)]).

If tereferencevoltage changes, thedigital result hanges to.

For example:

If te supplyused is a referenevoltage of 3.3 V and VA = 1 V, the digital outt is:

![](images/81dba990e32e305fb76a53a2eb982f32cd5b5fe499837fe6cf2c4499ec057f2c.jpg)

If te voltage supply provides a voltage equal to 3.292 V (after its utput conein o VREF+), then:

![](images/1d9cf90c0cb2aa38af47e0a2e7ea9bc7283dc7c86c2a5cdca1af802365215970.jpg)

The error introduced by the voltage drop is: Ox4DC - 0x4D9 = 3 LSB.

# 3.2.3 Reference voltage decoupling and impedance

The reference voltage source must have a low output impedance to provide a nominal voltage under various load conditions. Both resistive and inductive parts of the output impedance are important. During the ADC conversion, the reference voltage is connected to the switched capacitor network (see Figure 4. and Figure 5.). The capacitors of this network are charged/discharged from/to a reference voltage in a very short time during successive approximations (one approximation cycle corresponding to one ADC clock period). The reference voltage must provide high current peaks to capacitors. Voltages on capacitors must be stable at the end of each approximation cycle (zero current from the reference voltage). Therefore, the reference voltage must have a very low output impedance including low inductance (to provide high current peaks in a very short time). Parasitic inductance can prevent the charging process from being fully finished at the end of the approximation cycle or oscillations can appear in the LC circuit (parasitic inductance together with capacitor

network). In this case, the result of the approximation cycle is inaccurate. Correct decoupling capacitors on the reference voltage located very close to pins provide a low source impedance.

# 3.2.4 External reference voltage parameters

In case of using an external source for reference voltage (on VREF+ pin), there are important parameters of this external reference source to consider. Three reference voltage specifications must be considered: temperature drift, voltage noise, long-term stability.

# 3.2.5 Analog input signal noise

Small but high-frequency signal variation can result in significant conversion errors during sampling time. This noise is generated by electrical devices, such as motors, engine ignition, and power lines. It affects the source signal (such as sensors) by adding an unwanted signal. As a consequence, the ADC conversion results are not accurate.

# 6.2.6 ADC dynamic range bad match for maximum input signal amplitude

To obtain the maximum ADC conversion precision, it is very important that the ADC dynamic range matches the maximum amplitude of the signal to be converted. Let us assume that the signal to be converted varies between 0 V and 2.5 V and that VREF+ is equal to 3.3 V. The maximum signal value converted by the ADC is 3103 (2.5 V) as shown in Figure 14. In this case, there are 992 unused transitions (4095 - 3103 = 992). This implies a loss in the converted signal accuracy.

See Section 4.2.5: Matching the ADC dynamic range to the maximum signal amplitude on page 24 for details on how to make the ADC dynamic range match the maximum input signal amplitude.

![](images/305babe7ef0e4e3f8f4f6ad563cd327188f2bf774575a0b3084e47d4cfb3def2.jpg)  
Figure 14. Input signal amplitude vS. ADC dynamic range (VREF+ = 3.3 V)

# 3.2.7 Effect of the analog signal source resistance

The impedance of the analog signal source, or series resistance (RAin), between the source and pin, causes a voltage drop across it because of the current flowing into the pin. The charging of the internal sampling capacitor (CADc) is controlled by switches with a resistance RADC.

With the addition of source resistance (with RaDc), the time required to fully charge the hold capacitor increases. Figure 15 shows the analog signal source resistance effect.

The effective charging of CADC is governed by RADC + RAIN, so the charging time constant becomes tc = (RADC+RAiN) \* CADC. If the sampling time is less than the time required to fully charge the CADc through RADC + RAiN (ts < tc), the digital value converted by the ADC is less than the actual value.

![](images/8320cf64e04214eeca5368144c4731227d71be213a5e669bf79ac84a1d8afa02.jpg)  
Figure 15. Analog signal source resistance effect

is the time taken b the C apacior o ully charge: V = VA (with max./2 LSB err) capacitor CADcvolt =RADC +RAIN× CADC

# .2.8 Effect of source capacitance and parasitic capacitance of the PCB

When converting analog signals, it is necessary to account for the capacitance at the source and the parasitic capacitance seen on the analog input pin (refer to Figure 16). The source resistance and capacitance from an RC network. In addition, the ADC conversion results may not be accurate, except if the external capacitor (Cain + Cp) is fully charged to the level o the input voltage. The greater value of (CAi + Cp), the more limited the source frequency.

T and Cp, respectively.

![](images/245f2ec579a7e6af154e238721ef28f4d52d454f616432225b9f9ffeff08158d.jpg)  
Figure 16. Analog input with RAIN CAN and Cp

# 3.2.9 Injection current effect

A negative injection current on any analog pin (or a closely positioned digital input pin) may introduce leakage current into the ADC input. The worst case is the adjacent analog channel. A negative injection current is introduced when VAiN < Vss, causing the current to flow out from the I/O pin. This is illustrated in Figure 17.

![](images/4a41bcfd89994b45d79959c3cbb3400f8629260168561a52a65f44dacdd7872b.jpg)  
Figure 17. Effect of injection current

ai15484

# 3.2.10 Temperature influence

The temperature has a major influence on ADC accuracy. Mainly it leads to two major errors: offset error drift and gain error drift. Those errors can be compensated in the microcontroller firmware (refer to Section 4.2.9 for the temperature-compensation methods).

# 3.2.11 I/O pin crosstalk

Switching the l/Os may induce some noise in the analog input of the ADC due to capacitive coupling between l/Os. Crosstalk may be introduced by PCB tracks that run close to each other or that cross each other.

Internally switching digital signals and l/Os introduces high-frequency noise. Switching highsink l/Os may induce some voltage dips in the power supply caused by current surges. A digital track that crosses an analog input track on the PCB may affect the analog signal (see Figure 18).

![](images/84d1179c388226372808172fcbd8aad1395b06651f57462e951414aeaf87b677.jpg)  
Figure 18. Crosstalk between I/O pins

Case 1: Digital and analog signal tracks that pass close to each other.

2Case 2: Digital and analog signal tracks that cross each other on a different PCB side.

# 3.2.12 EMI-induced noise

Electromagnetic emissions from neighboring circuits may introduce high-frequency noise in an analog signal because the PCB tracks may act like an antenna (See Figure 19.).

![](images/2294549741595f277db82895a87bf928072c3dbe14e78e3554a4f260becca5f0.jpg)  
Figure 19. EMI sources

# How to optimize the ADC accuracy

# 4.1 Reduce the effects of the ADC-related ADC errors

The TUE is not the sum of all the Eo, EG, EL, ED errors. It is the maximum deviation that can occur between the ideal and actual digital values. It can result from one or more errors occurring simultaneously.

As the ILE is the integral of the DLE, it can be considered as the indicator of the maximum error. Do not add the DLE and ILE together to calculate the maximum error that may occur at any digital step.

The maximum error values specified in the device datasheet are the worst error values measured in a laboratory test environment over the given voltage and temperature range (refer to the device datasheet).

The ILE and DLE are dependent on the ADC design. It is difficult to calibrate them. They can be calibrated by the measured ADC curve stored in the microcontroller memory but this needs calibration of each individual device in the final application.

Offset and gain errors can be easily compensated using the STM32 ADC self-calibration feature or by microcontroller firmware.

# 4.2

# Minimize the ADC errors related to the ADC external environment

# 4.2.1

# Reference voltage / power supply noise minimization

# On the power supply side

Linear regulators have a better output in terms of noise. The mains must be stepped down, rectified, and filtered, then fed to linear regulators. It is highly recommended to connect the filter capacitors to the rectifier output. Refer to the datasheet of the used linear regulator.

When using a switching power supply, it is recommended to have a linear regulator to supply the analog stage.

It is recommended to connect capacitors with good high-frequency characteristics between the power and ground lines. That is, a 0.1 µF and a 1 to 10 µF capacitor must be placed close to the power source.

The capacitors allow the AC signals to pass through them. The small-value capacitors filter high-frequency noise and the high-value capacitors filter low-frequency noise. Ceramic capacitors are generally available in small values (1 pF to 0.1 µF) and with small voltage ratings (16 V to 50 V). It is recommended to place them close to the main supply (VDD and Vss) and analog supply (VDDA and VssA) pins. They filter the noise induced in the PCB tracks. Small capacitors can react fast to current surges and discharge quickly for fastcurrent requirements.

Tantalum capacitors can also be used along with ceramic capacitors. To filter low-frequency noise, high-value capacitors (10 µF to 100 µF), which are generally electrolytic, can be used. It is recommended to put them near the power source.

To filter high-frequency noise, a ferrite inductance in series with the power supply can be used. This solution leads to very low (negligible) DC loss unless the current is high because the series resistance of the wire is very low. At high frequencies, however, the impedance is high.

The inductance must be small enough not to limit high current peak requirements from the supply pins. The inductance together with the decoupling capacitor is an LC circuit, which can start to oscillate if there is a fast voltage drop on the decoupling capacitor, caused by a change of consumption (on VDDA, VDD. VREF+). The oscillations can take more time and influence the ADC measurement (oscillations on VREF+ during conversion). To suppress these oscillations, it is recommended to use small inductances and with ferrte cores, which have losses at high frequencies (resistive character of the impedance).

# On the STM32 microcontroller side

In most STM32 microcontrollers, the VDD and Vss pins are placed close to each other. So are the VREF+ and VssA pins. A capacitor can therefore be connected very close to the microcontroller with very short leads. For multiple VDD and Vss pins, use separate decoupling capacitors.

The VDDA pin must be connected to two external decoupling capacitors (10 nF Ceramic + 1 µF Tantalum or Ceramic). Refer to Figure 20 and Figure 21 for decoupling examples.

For STM32 microcontrollers delivered in 100/144-pin packages, it is possible to improve the accuracy on low-voltage inputs by connecting a separate external ADC reference voltage input on VREF+ (refer to Section 4.2.5). The voltage on VREF+ may range from 2.4 V to VDDA. If a separate, external reference voltage is applied on VREF+, two 10 nF and 1 µF capacitors must be connected on this pin. In all cases, VREF+ must be kept between 2.4 V and VDDA.

![](images/65fb51b8e959cddcc09eb407fdea455222ca7b0c40aea40a7e438666e336e892.jpg)  
Figure 20. Power supply and reference decoupling for 100- and 144-pin packages

![](images/ece03bf010a7fc8db40c41644db750db11d430fb6676720b18f29615a24be6b9.jpg)  
Figure 21. Power supply decoupling for 36-, 48- and 64-pin packages

# 4.2.2 Reference voltage / power supply regulation

The power supply must have good line and load regulation since the ADC uses VREF+ or VDDA as the analog reference and the digital value is the ratio of the analog input signal to this voltage reference. VREF+ must thus remain stable at different loads.

Whenever the load is increased by switching on a part of the circuit, the increase in current must not cause the voltage to decrease. If the voltage remains stable over a wide current range, the power supply has good load regulation.

For example, for the LD1086D2M33 voltage regulator, the line regulation is 0.035% typical when Vin varies from 2.8 V to 16.5 V (when load = 10 mA), and the load regulation is 0.2% when load varies from 0 to 1.5 A (please refer to the LD1086 series datasheet for details).

The lower the line regulation value, the better the regulation. Similarly, the lower the load regulation value, the better the regulation and the stability of the voltage output.

It is also possible to use a reference voltage for VREF+, for instance the TL1431A, which is a voltage reference diode of 2.5 V (refer to TL1431A datasheet for more details).

The reference voltage source design must provide a low output impedance (static and dynamic). The parasitic serial resistance and inductance must be minimized. Correct decoupling capacitors on the reference voltage located very close to pins provide a low reference voltage source impedance.

# 4.2.3 Analog-input signal noise elimination

# Averaging method

Averaging is a simple technique that involves sampling an analog input several times and using software to calculate the average of the results.This technique is helpful to eliminate the effect of noise on the analog input in the case of an analog voltage that does not change often.

The average has to be made on several readings that all correspond to the same analog input voltage. Make sure that the analog input remains at the same voltage during the time period when the conversions are done. Otherwise, digital values corresponding to different analog inputs may be added up, introducing errors.

In the STM32 microcontrollers with the ADC oversampling feature, the ADC hardware oversampling feature can be used for averaging. This feature simply performs the sum of a given number of ADC raw samples into one final sample. This final sample can then be right shifted to reduce the bit width caused by multiple ADC samples accumulation. All these operations (accumulation and right-bit shifting) are performed by hardware. The ADC

hardware oversampling feature can be configured to process up to 1024 input samples (depending on devices).

# Adding an external filter

Adding an external RC filter eliminates the high frequency. An expensive filter is not needed to deal with a signal that has frequency components above the frequency range of interest. In this case, a relatively simple low-pass filter with a cutoff frequency fc just above the frequency range of interest suffices to limit noise and aliasing. A sampling rate consistent with the highest frequency of interest suffices, typically two to five times fc.

# Note:

The R and C that form the external filter must have values that match the conditions described in Section 4.2.4 and Section 4.2.8.

# 4.2.4

# Adding white noise or triangular sweep to improve resolution

This method combines hardware and software techniques to improve precision. From a software point of view, this method uses averaging (oversampling) and from a hardware point of view, it uses signal modification/spreading/dithering.

Averaging can be used in cases where the input signal is noisy (some signal change is necessary to be able to calculate an average) and the requirement is to obtain the mean value of a signal. A problem appears when the input signal is a very stable voltage without noise. In this case, when the input signal is measured, each data sample is the same. This is because the input signal level is somewhere between two ADC word levels (for instance, between 0x14A and 0x14B). Therefore, it is not possible to determine the input voltage level more precisely (for example, if the level is near to Ox14A or near to Ox14B level).

The solution is to add noise or some signal change (with uniform signal distribution, for example, triangular sweep) to the input signal, which pushes its level across 1-bit ADC level (so that the signal level changes below Ox14A and above Ox14B level). This causes the ADC results to vary. Applying software averaging to the different ADC results, produces the mean value of the original input signal. Some STM32 microcontrollers support hardware oversampling, which can be used instead of software oversampling.

As an example, this method can be implemented by using a triangular generator with RC coupling to the input signal (white noise generation is more complicated). Care must be taken not to modify the mean value of the original input signal (so, capacitive coupling must be used).

A very simple implementation of the quasi-triangular source, which is generated directly by the STM32 microcontroller is on Figure 22.

![](images/cdd1d25337f903e03caeb34911be30a44ae84c208f18d1d5ba7c39b3077d0a48.jpg)  
Figure 22. Simple quasi-triangular source using a microcontroller output

ai17803b

# 1.2.5 Matching the ADC dynamic range to the maximum signal amplitude

This method improves accuracy by a proper selection of the reference voltage or by using a preamplifier stage to obtain the maximum possible resolution using the full ADC output range.

# Selecting a reference voltage (method for devices delivered in packages with a dedicated VREF+ pin)

The reference voltage is selected in the expected range of the signal to be measured. If the measured signal has an offset, then the reference voltage must also have a similar offset. If the measured signal has a defined maximum amplitude, then the reference voltage must also have a similar maximum value. By matching this reference voltage to the measurement signal range, we obtain the maximum possible resolution using the full ADC output range.

In STM32 microcontrollers delivered in packages with a dedicated VREF+ pin, the ADC reference voltage is connected to the external VREF+ and VREF- pins that must be tied to ground. This makes it possible to match the reference voltage and the measured signal range.

For example, if the measured signal varies between 0 V and 2.5 V, it is recommended to choose a VREF+ of 2.5 V, possibly using a reference voltage like TL1431A (see TL1431A datasheet for more details). Figure 23 illustrates these conditions.

Note:

The voltage n VREF+ may range between 2.4V and DDA

![](images/69434873ead558e7bc73334f6d0678c3f065825ef8af7d6aa183a7deae6a4e81.jpg)  
Figure 23. Selecting the reference voltage

# Using a preamplifier

If the measured signal is too small (in comparison with the ADC range), then an external preamplifier can be useful. This method can be implemented whatever the STM32 package, and more specifically in packages that do not have a VREF+ input.

For example, if the measured signal varies between 0 V to 1 V and VDDA is set to 3 V, the signal can be amplified so that its peak-to-peak amplitude is similar to the VDDA value. The gain is then equal to 3 (see Figure 24 for an example).

This amplifier can adapt the input signal range to the ADC range. It can also insert offsets between the input signal and the ADC input. When designing the preamplifier, care must be taken not to generate additional errors (such as additional offset, amplifier gain stability or linearity, frequency response).

![](images/f12189b4404ca27eb9b3b5e47aee8c1b53550956474caf7cc4406f88b90ac277.jpg)  
Figure 24. Preamplification

# 4.2.6 SAR ADC sampling time prerequisites

# SAR ADC sample conversion process

The SAR ADC sample conversion process consists in two successive operations: sampling and bit conversion. When these operations are completed, the sample conversion result is available in the ADC data register (ADC_DR). When the ADC conversion has started, the new converted data is available after a sample conversion time of Tconv. When continuous acquisition is performed, a new data is available every Tconv and it can be converted into the ADC sampling rate. The number of samples obtained in one second can be computed using the following formula:

ADC m e nen

![](images/d4f5fb5270a1d629c0ae754c316cd79472980c03e946d87b5dbf7bf8d5b3b4c9.jpg)  
Figure 25. SAR ADC sample conversion process

The following paragraph describes the two successive operations required for sample conversion:

Sampling This operation samples the analog input signal by charging the internal ADC sampling capacitor (CADC). The duration of this operation is TsMPL. It depends on the SMP parameter that is configured in the ADC configuration register to select the sampling time duration.

Bit conversion

This operation converts the analog value stored in the CADc sampling capacitor to a digital value.

The duration of this operation is TsAR. It depends on the RES parameter that is configured in the ADC configuration register to select the ADC bit resolution.

ADC sample conversion time (Tconv) = Sampling time (TPL) + Bit conversion time (TAR)

![](images/ad1c3f8f211171319803fd93045460f328707d07ea1afa8647520012aa705b6e.jpg)

Both TsMPL and TsAR durations are relative to multiple of ADC clock cycles:

TsMPL duration:   
This duration depends on the SMP parameter (ADC sampling duration). As an example, SMP values for STM32L5 series can be 2.5, 6.5, 12.5, 24.5, 47.5, 92.5, 247.5 or 640.5 ADC clock cycles.   
TsAR duration:   
This duration depends on the RES parameter (ADC bit resolution). As an example, RES values for STM32L5 series can be 6.5, 8.5, 10.5 and 12.5 ADC clock cycles for 6, 8, 10 and 12-bit resolution.

The ADC sampling rate or sample conversion time (Tconv) can be calculated using the following formula:

![](images/6243ed5bcb75f0e5f0bd1de764a6d7cfbe260107be0b00ff71e963fdc3849b0a.jpg)

ADC sample rate = 1/ TcoNv = 3.336 samples per second or 3.33 MSPS

where   
FADC_CLK = 50 MHz   
TsMPL = 2.5 clock cycles   
TSAR = 12.5 (ADC 12-bit resolution):

# SAR ADC sampling TsMPL and TsAR constraints

TsMPL and TsAR durations must be selected according to the application scope and environment. TsAR is easier to choose since it depends only on the selected ADC bit resolution (6, 8, 10 or 12 bits). TsMPL is more complex and depends on various parameters:

TsmpL minimum duration depends on the external electrical components of the input path (Section 3.2.7: Effect of the analog signal source resistance and Section 3.2.8: Effect of source capacitance and parasitic capacitance of the PCB):

RaiN: analog source output impedance   
CPCB or CAIN: PCB parasitic capacitor or analog input decoupling/filtering   
capacitor

TsMPL depends on the internal STM32 SAR circuitry (RPAR, CPAR and CADC): SAR ADC channel type: fast, slow, direct (refer to the device datasheet) Internal circuitry parameters vary according to the package dimensions, manufacturing process, temperature, and supply voltage levels.

TsmPL also varies according to application constraints and functionalities:

Maximum conversion error: ±1 LSB or higher ADC resolution (expressed in bits) Number of ADCs running in parallel

![](images/3e8538f705281e675c049e0b0ce0f778d817eea19bf02615c48f50679a1d07ae.jpg)  
Figure 26. Simplified external/internal SAR ADC sampling diagram

Based on the above constraints, the minimum TsMPL required to achieve the maximum output sampling rate can then be estimated.

The device datasheet provides a few TsmPL values to obtain a maximum accuracy of ± 1/2 LSB for each channel type, different RAin values, a given CAIN/CPCB capacitor, and in the worst conditions of package dimensions, temperature, manufacturing process and supply voltages.

Figure 27 and Figure 28 show the impact of the desired accuracy (from ± 0.5 to ± 3 LSB) and ADC resolution (expressed in LSB) on the input signal to reach the voltage accuracy. When the resolution is low and the error accuracy is high, the required signal sampling time is short, whereas when the resolution is high and the error accuracy is low, the required signal sampling time is long.

Figure 27 shows that the sampling duration increases with the ADC resolution. It also shows the voltage variation on the STM32 ADC analog input pin. The first ADC conversion starts at 0 ns. For negative timings, the curve shows the input voltage state before the first ADC conversion.

![](images/665a6f6ca0d61f965f229ef856873d50c4f30b0a9920b15386b9ac41e9ce7cad.jpg)  
Figure 27. Example of SAR ADC input sampling time vs ADC resolution

The above results are obtained in the following conditions: VREF+=2V AN1 CAIN/CpcB = 2 nF Typical conditions of voltage, temperature, process, package, and number of ADCs running.

Figure 28 shows that the sampling duration has to be increased to achieve a higher accuracy: a 23.8 ns sampling duration is required to obtain a 12-bit resolution and ± 3 LSB, whereas a 40.4 ns duration is needed for 12 bits and ± 0.5 LSB.

![](images/87046b82613d8366893fbd461724fa8e8c73db31e140801b324480a82fa987ef.jpg)  
Figure 28. Example of SAR ADC input sampling time vs accuracy   
The above results are obtained in the following conditions: RA=1 CAIN/CPCB = 2 nF 12-bit ADC resolution Typical conditions of voltage, temperature, process, package, and number of ADCs running.

Table 1 gives examples of sampling time for STM32H7 series with RAIN = 1 kΩ, CAiN/CPCB = 2 nF, VREF+ = 2 V and FADC = 20 MHz.

Table 1. Minimum sampling time for STM32H7 series devices (in ns)   

<table><tr><td rowspan=1 colspan=1>Acquisitionaccuracy</td><td rowspan=1 colspan=1>8 bits</td><td rowspan=1 colspan=1>10 bits</td><td rowspan=1 colspan=1>12 bits</td><td rowspan=1 colspan=1>14 bits</td><td rowspan=1 colspan=1>16 bits</td></tr><tr><td rowspan=1 colspan=1>± 0.5 LSB</td><td rowspan=1 colspan=1>17.1</td><td rowspan=1 colspan=1>27.1</td><td rowspan=1 colspan=1>40.4</td><td rowspan=1 colspan=1>53.8</td><td rowspan=1 colspan=1>67.1</td></tr><tr><td rowspan=1 colspan=1>± 1 LSB</td><td rowspan=1 colspan=1>7.9</td><td rowspan=1 colspan=1>20.4</td><td rowspan=1 colspan=1>33.8</td><td rowspan=1 colspan=1>47.1</td><td rowspan=1 colspan=1>60.4</td></tr><tr><td rowspan=1 colspan=1>± 2 LSB</td><td rowspan=1 colspan=1>0.0</td><td rowspan=1 colspan=1>17.1</td><td rowspan=1 colspan=1>27.1</td><td rowspan=1 colspan=1>40.4</td><td rowspan=1 colspan=1>53.8</td></tr><tr><td rowspan=1 colspan=1>± 3 LSB</td><td rowspan=1 colspan=1>0.0</td><td rowspan=1 colspan=1>10.4</td><td rowspan=1 colspan=1>23.8</td><td rowspan=1 colspan=1>37.1</td><td rowspan=1 colspan=1>50.4</td></tr></table>

When the ADC resolution is 8 bits and the acquisition accuracy is greater than ± 1 LSB, TsMPL can be minimized to a few picoseconds due to LSB amplitude, whereas with an ADC resolution is 16 bits and an acquisition accuracy equal to ± 0.5 LSB, TsMPL maximum value is 67.1 ns.

# SAR ADC conversion duration and sampling rate dependency versus SMP

The ADC SMP parameter enables programming the duration of the ADC sampling operation to a given number of ADC clock cycles. SMP can be selected among a list of values that depends on each STM32 series (see Figure 29 and Table 2). To match the requirements of wide frequency-range applications, SMP values approximately follow a logarithm law.

Table 2. Examples of ADC SMP selection vs STM32 Series (in ADC clock cycles)   

<table><tr><td rowspan=1 colspan=1>ADC SMP code</td><td rowspan=1 colspan=1>STM32G0</td><td rowspan=1 colspan=1>STM32F1</td><td rowspan=1 colspan=1>STM32L4</td><td rowspan=1 colspan=1>STM32H7</td><td rowspan=1 colspan=1>STM32H5</td></tr><tr><td rowspan=1 colspan=1>0</td><td rowspan=1 colspan=1>1.5</td><td rowspan=1 colspan=1>1.5</td><td rowspan=1 colspan=1>2.5</td><td rowspan=1 colspan=1>1.5</td><td rowspan=1 colspan=1>2.5</td></tr><tr><td rowspan=1 colspan=1>1</td><td rowspan=1 colspan=1>3.5</td><td rowspan=1 colspan=1>7.5</td><td rowspan=1 colspan=1>6.5</td><td rowspan=1 colspan=1>2.5</td><td rowspan=1 colspan=1>6.5</td></tr><tr><td rowspan=1 colspan=1>2</td><td rowspan=1 colspan=1>7.5</td><td rowspan=1 colspan=1>13.5</td><td rowspan=1 colspan=1>12.5</td><td rowspan=1 colspan=1>8.5</td><td rowspan=1 colspan=1>12.5</td></tr><tr><td rowspan=1 colspan=1>3</td><td rowspan=1 colspan=1>12.5</td><td rowspan=1 colspan=1>28.5</td><td rowspan=1 colspan=1>24.5</td><td rowspan=1 colspan=1>16.5</td><td rowspan=1 colspan=1>24.5</td></tr><tr><td rowspan=1 colspan=1>4</td><td rowspan=1 colspan=1>19.5</td><td rowspan=1 colspan=1>41.5</td><td rowspan=1 colspan=1>47.5</td><td rowspan=1 colspan=1>32.5</td><td rowspan=1 colspan=1>47.5</td></tr><tr><td rowspan=1 colspan=1>5</td><td rowspan=1 colspan=1>39.5</td><td rowspan=1 colspan=1>55.5</td><td rowspan=1 colspan=1>92.5</td><td rowspan=1 colspan=1>64.5</td><td rowspan=1 colspan=1>92.5</td></tr><tr><td rowspan=1 colspan=1>6</td><td rowspan=1 colspan=1>79.5</td><td rowspan=1 colspan=1>71.5</td><td rowspan=1 colspan=1>247.5</td><td rowspan=1 colspan=1>387.5</td><td rowspan=1 colspan=1>247.5</td></tr><tr><td rowspan=1 colspan=1>7</td><td rowspan=1 colspan=1>160.5</td><td rowspan=1 colspan=1>239.5</td><td rowspan=1 colspan=1>640.5</td><td rowspan=1 colspan=1>810.5</td><td rowspan=1 colspan=1>640.5</td></tr></table>

The distribution of ADC SMP values is a constraint to optimize the ADC sampling time. In the following example, which is based on the STM32H7 series, some application conditions are optimized.

Table 3 to Table 7 show examples of results for STM32H7 series obtained with RAiN = 1 kΩ, CAiN/CpCB = 2 nF, VREF+ = 2 V and FADC = 20 MHz.

Table 3 shows the real minimum sampling time expressed in ADC clock cycles (sampling duration / ADC clock period) corresponding to Table 1.

Table 3. Rounded minimum sampling time vs resolution and maximum error (in ADC clock cycles)   

<table><tr><td rowspan=1 colspan=1>Acquisitionaccuracy</td><td rowspan=1 colspan=1>8 bits</td><td rowspan=1 colspan=1>10 bits</td><td rowspan=1 colspan=1>12 bits</td><td rowspan=1 colspan=1>14 bits</td><td rowspan=1 colspan=1>16 bits</td></tr><tr><td rowspan=1 colspan=1>± 0.5 LSB</td><td rowspan=1 colspan=1>4</td><td rowspan=1 colspan=1>6</td><td rowspan=1 colspan=1>9</td><td rowspan=1 colspan=1>11</td><td rowspan=1 colspan=1>14</td></tr><tr><td rowspan=1 colspan=1>± 1 LSB</td><td rowspan=1 colspan=1>2</td><td rowspan=1 colspan=1>5</td><td rowspan=1 colspan=1>7</td><td rowspan=1 colspan=1>10</td><td rowspan=1 colspan=1>13</td></tr><tr><td rowspan=1 colspan=1>± 2 LSB</td><td rowspan=1 colspan=1>1</td><td rowspan=1 colspan=1>4</td><td rowspan=1 colspan=1>6</td><td rowspan=1 colspan=1>9</td><td rowspan=1 colspan=1>11</td></tr><tr><td rowspan=1 colspan=1>± 3 LSB</td><td rowspan=1 colspan=1>1</td><td rowspan=1 colspan=1>3</td><td rowspan=1 colspan=1>5</td><td rowspan=1 colspan=1>8</td><td rowspan=1 colspan=1>11</td></tr></table>

For STM32H7 series, TsMPL can be programmed to the following values, through the SMP parameter: 1.5, 2.5, 8.5, 16.5, 32.5, 64.5, 387.5 or 810.5 ADC clock cycles. Table 4 shows the minimum SMP value required to reach various input sampling accuracies:

Table 4. Minimum SMP values vs resolution and maximum error (in ADC clock cycles)   

<table><tr><td rowspan=1 colspan=1>Acquisitionaccuracy</td><td rowspan=1 colspan=1>8 bits</td><td rowspan=1 colspan=1>10 bits</td><td rowspan=1 colspan=1>12 bits</td><td rowspan=1 colspan=1>14 bits</td><td rowspan=1 colspan=1>16 bits</td></tr><tr><td rowspan=1 colspan=1>± 0.5 LSB</td><td rowspan=1 colspan=1>8.5</td><td rowspan=1 colspan=1>8.5</td><td rowspan=1 colspan=1>16.5</td><td rowspan=1 colspan=1>16.5</td><td rowspan=1 colspan=1>16.5</td></tr><tr><td rowspan=1 colspan=1>± 1 LSB</td><td rowspan=1 colspan=1>2.5</td><td rowspan=1 colspan=1>8.5</td><td rowspan=1 colspan=1>8.5</td><td rowspan=1 colspan=1>16.5</td><td rowspan=1 colspan=1>16.5</td></tr><tr><td rowspan=1 colspan=1>± 2 LSB</td><td rowspan=1 colspan=1>1.5</td><td rowspan=1 colspan=1>8.5</td><td rowspan=1 colspan=1>8.5</td><td rowspan=1 colspan=1>16.5</td><td rowspan=1 colspan=1>16.5</td></tr><tr><td rowspan=1 colspan=1>± 3 LSB</td><td rowspan=1 colspan=1>1.5</td><td rowspan=1 colspan=1>8.5</td><td rowspan=1 colspan=1>8.5</td><td rowspan=1 colspan=1>8.5</td><td rowspan=1 colspan=1>16.5</td></tr></table>

Table 5 gives additional clock cycles between the real minimum sampling time and the corresponding minimum SMP value.

Table 5. Additional ADC clock cycles due to SMP vs resolution and maximum error   

<table><tr><td rowspan=1 colspan=1>Acquisitionaccuracy</td><td rowspan=1 colspan=1>8 bits</td><td rowspan=1 colspan=1>10 bits</td><td rowspan=1 colspan=1>12 bits</td><td rowspan=1 colspan=1>14 bits</td><td rowspan=1 colspan=1>16 bits</td></tr><tr><td rowspan=1 colspan=1>± 0.5 LSB</td><td rowspan=1 colspan=1>4.5</td><td rowspan=1 colspan=1>2.5</td><td rowspan=1 colspan=1>7.5</td><td rowspan=1 colspan=1>5.5</td><td rowspan=1 colspan=1>2.5</td></tr><tr><td rowspan=1 colspan=1>± 1 LSB</td><td rowspan=1 colspan=1>0.5</td><td rowspan=1 colspan=1>3.5</td><td rowspan=1 colspan=1>1.5</td><td rowspan=1 colspan=1>6.5</td><td rowspan=1 colspan=1>3.5</td></tr><tr><td rowspan=1 colspan=1>± 2 LSB</td><td rowspan=1 colspan=1>1.5</td><td rowspan=1 colspan=1>4.5</td><td rowspan=1 colspan=1>2.5</td><td rowspan=1 colspan=1>7.5</td><td rowspan=1 colspan=1>5.5</td></tr><tr><td rowspan=1 colspan=1>± 3 LSB</td><td rowspan=1 colspan=1>1.5</td><td rowspan=1 colspan=1>5.5</td><td rowspan=1 colspan=1>3.5</td><td rowspan=1 colspan=1>0.5</td><td rowspan=1 colspan=1>5.5</td></tr></table>

In normal application conditions, an optimized sampling time is achieved for an 8-bit ADC resolution and an accuracy greater than ± 1 LSB, while nonoptimized sampling times are obtained for a 12-bit ADC resolution and accuracy lower than ± 1 LSB, and 14-bit and 16-bit resolution with an accuracy lower than ± 3 LSB.

Table 6 shows the total conversion times including TsAR duration and the computed ADC output sampling rate (TsMPL). For STM32H7 series, TsAR can be programmed to the following values: 4.5, 5.5, 6.5, 7.5 or 8.5 ADC clock cycles for ADC resolutions of 8-, 10-, 12-, 14-, and 16 bit resolutions.

Table 6. Minimum ADC conversion time (TsMPL + TsAR) vs resolution and maximum error (in ADC clock cycles)   

<table><tr><td rowspan=1 colspan=1>Acquisitionaccuracy</td><td rowspan=1 colspan=1>8 bits</td><td rowspan=1 colspan=1>10 bits</td><td rowspan=1 colspan=1>12 bits</td><td rowspan=1 colspan=1>14 bits</td><td rowspan=1 colspan=1>16 bits</td></tr><tr><td rowspan=1 colspan=1>± 0.5 LSB</td><td rowspan=1 colspan=1>13</td><td rowspan=1 colspan=1>14</td><td rowspan=1 colspan=1>23</td><td rowspan=1 colspan=1>24</td><td rowspan=1 colspan=1>25</td></tr><tr><td rowspan=1 colspan=1>± 1 LSB</td><td rowspan=1 colspan=1>7</td><td rowspan=1 colspan=1>14</td><td rowspan=1 colspan=1>15</td><td rowspan=1 colspan=1>24</td><td rowspan=1 colspan=1>25</td></tr><tr><td rowspan=1 colspan=1>± 2 LSB</td><td rowspan=1 colspan=1>6</td><td rowspan=1 colspan=1>14</td><td rowspan=1 colspan=1>15</td><td rowspan=1 colspan=1>24</td><td rowspan=1 colspan=1>25</td></tr><tr><td rowspan=1 colspan=1>± 3 LSB</td><td rowspan=1 colspan=1>6</td><td rowspan=1 colspan=1>14</td><td rowspan=1 colspan=1>15</td><td rowspan=1 colspan=1>16</td><td rowspan=1 colspan=1>25</td></tr></table>

The maximum ADC output sampling rate for these application conditions can then be computed.

Table 7. Maximum ADC output sampling rate (MSPS) vs resolution and maximum error   

<table><tr><td rowspan=1 colspan=1>Acquisitionaccuracy</td><td rowspan=1 colspan=1>8 bits</td><td rowspan=1 colspan=1>10 bits</td><td rowspan=1 colspan=1>12 bits</td><td rowspan=1 colspan=1>14 bits</td><td rowspan=1 colspan=1>16 bits</td></tr><tr><td rowspan=1 colspan=1>± 0.5 LSB</td><td rowspan=1 colspan=1>1.5</td><td rowspan=1 colspan=1>1.4</td><td rowspan=1 colspan=1>0.9</td><td rowspan=1 colspan=1>0.8</td><td rowspan=1 colspan=1>0.8</td></tr><tr><td rowspan=1 colspan=1>± 1 LSB</td><td rowspan=1 colspan=1>2.9</td><td rowspan=1 colspan=1>1.4</td><td rowspan=1 colspan=1>1.3</td><td rowspan=1 colspan=1>0.8</td><td rowspan=1 colspan=1>0.8</td></tr><tr><td rowspan=1 colspan=1>± 2 LSB</td><td rowspan=1 colspan=1>3.3</td><td rowspan=1 colspan=1>1.4</td><td rowspan=1 colspan=1>1.3</td><td rowspan=1 colspan=1>0.8</td><td rowspan=1 colspan=1>0.8</td></tr><tr><td rowspan=1 colspan=1>± 3 LSB</td><td rowspan=1 colspan=1>3.3</td><td rowspan=1 colspan=1>1.4</td><td rowspan=1 colspan=1>1.3</td><td rowspan=1 colspan=1>1.3</td><td rowspan=1 colspan=1>0.8</td></tr></table>

When the ADC resolution is 8 bits and the acquisition accuracy is above ± 2 LSB, the maximum ADC sampling rate output 3.3 MSPS, is achieved with RAIN = 1 kΩ, CAIN/CpCB = 2 nF, FADC = 20 MHz, and typical conditions of voltage, temperature, process, package, and number of ADCs running.

When the ADC resolution is 16 bits, the ADC sampling rate is reduced to 0.8 MSPS with an acquisition accuracy lower than ± 3 LSB.

# Method for estimating the SAR ADC sampling rate (TMPL)

A mathematical model is not accurate enough given the number of parameters and their nonlinear characteristics. Only a complex design simulation can provide a very good estimate of the minimum TsMPL duration in various conditions. Such SAR ADC sampling estimation tool is available on demand. TsmpL simulation results are simply postprocessed and rendered based on ADC clock frequency to achieve the desired ADC output data rate. The simulation tool performs the following functions:

Estimation of TsMPL versus ADC frequency (see Figure 29).   
Vilizang r /Aalu c i al (see Figure 30)

The tool helps selecting the correct SMP value to optimize the sampling duration for any ADC frequency range. It directly shows the output data rate that is achievable with the selected ADC resolution.

![](images/a17f870761e73f542352c373df85a9ce6ebbf011ee2ce792a87fd64564f2e74c.jpg)  
Figure 29. TsMPL estimation versus ADC frequency and comparison of minimum TsmPL duration for slow and fast channes with same RAinAI

The above results are obtained in the worst conditions of temperature, supply voltages, and process.

![](images/bdb6c7f6a7a5391ac90fda8b6e47fd4c994f5e049ca845489958f404fa49e537.jpg)  
Figure 30. TsMPL estimation versus ADC frequency and comparison of minimum TsmPL duration for fast channels with RAIN/CAIN = 51 Ω/10 pf and 100 Ω/33 pF   
The above results are obtained in the worst conditions of temperature, supply voltage, and process.

# 4.2.7 External analog buffer usage

The use of a follower amplifier (buffer) in front of an ADC analog input reduces the resistance of the source effect because of the high input impedance of the amplifier and its very low output impedance. It isolates RAi from RADC.

However, the amplifier introduces an offset error that must be taken into account as an additional error. The used amplifier must provide a small offset error.

The amplifier speed (bandwidth and slew rate) parameter is important for designing fast signal data acquisition applications.

The amplifier in follower mode offers a very low output impedance. The ADC can then use short sampling times. However, the required sampling time must be designed also regarding the amplifier speed. The amplifier has a low output impedance due to its feedback (driving the output to be on the same voltage as the input). This feedback response has a limited speed, which is defined by the used amplifier speed. The discharged sampling capacitor is connected to the amplifier output if the ADC starts the sampling operation. The amplifier (through its feedback) starts compensating this unbalance by increasing the output driving and charging the sampling capacitor. The speed of this output driving depends on the amplifier speed (propagation of the input change to the output change). The chosen ADC sampling time must be designed to be several times longer than this amplifier propagation delay.

# 4.2.8 Source frequency condition vs. source and parasitic capacitors

The external capacitance of Cain does not allow the analog input voltage to be exactly the same as VAin if the capacitor is not fully charged by the analog source (see Figure 16.).

If the analog input signal changes, then the analog signal frequency (FAin) must be such that the time period of this analog signal is at least: 10 × RAIN × (AIN + Cp).

TAIN = analog signal time period = 1/FAIN.

We have: TAin≥ 10× RAiN (AiN +C)

Theore FAIN  I AIN 1

For example:

For RAIN = 25 kΩ CAIN = 7 pF, Cp = 3 pF, this gives:

![](images/b069cf702621a98ce327cab66eba8715d098600816128f787277ccc4c371570c.jpg)

.

So, for the above defined source characteristics (capacitance and resistance), the frequency of the source must not exceed 400 kHz, otherwise the ADC conversion result is not accurate.

![](images/560aff19576836b504a5dbf5fc35795190bdb489565b95aa94ba6d69e7f38d24.jpg)  
Figure . Recomended values for RAI and CA V. source freqency FAIN

# 4.2.9 Temperature-effect compensation

One method is be to fully characterize the offset and gain drift and provide a lookup table in memory to correct measurement according to temperature change. This calibration involves additional costs and takes time.

The second method consists in recalibrating the ADC when the temperature change reaches a given value, by using the internal temperature sensor and the ADC watchdog.

# 4.2.10 Minimizing injection current

Check the application to verify whether any digital or analog input voltage can be less than Vss or VssA. If it is the case, a negative injection current flows from the pins. The effect on the accuracy is greater if a digital input is close to the analog input being converted.

Negative current injection on any of the standard (nonrobust) analog input pins must be avoided, as this significantly reduces the accuracy of the conversion performed on another analog input.

It is recommended to connect a Schottky diode between VssA and the I/O pin that can give birth to the negative injection current.

The ADC accuracy is not affected by positive injection currents within the limits specified for INJ(PIN) and ∑lNJ(PIN) (refer to the corresponding STM32 datasheet, I/O port characteristics ssection).

# 4.2.11 Minimizing I/O pin crosstalk

The noise produced by crosstalk can be reduced by shielding the analog signal by placing ground tracks across it. Figure 32 shows the recommended grounding between signals.

![](images/bc868b5737bdd01c0af6e7877d704530135dbcb3ce7fb6b2cc0db66ed1dda030.jpg)  
Figure 32. Crosstalk between l/O pins

# 4.2.12 EMI-induced noise reduction

EMI noise can be reduced by using proper shielding and layout techniques. The possible sources of emission must be physically separated from the receptors. They can be separated electrically by proper grounding and shielding.

# Shielding technique

Placing ground tracks alongside sensitive analog signals provides shielding on the PCB. The other side of the two-layer PCB must also have a ground plane. This prevents interference and I/O crosstalk affecting the signal (see Figure 33).

Signals coming from distant locations (such as sensors) must be connected to the PCB using a shielded cable. Care must be taken to minimize the length of the paths of these types of signals on the PCB.

The shield must not be used to carry the ground reference from the sensor or analog source to the microcontroller. A separate wire must be used as the ground. The shield must be grounded at only one place near the receiver such as the analog ground of the microcontroller. Grounding the shield at both ends (source and receiver) might lead to the creation  ground loops, with theresult o current fowig through theshild In thiscase, the shield acts like an antenna and the purpose of the shielding is lost.

The shielding concept also applies to grounding the chassis of the application if it is metallic. And it also helps remove EMI and EMC interference. In this case, the mains earth ground is used to shield the chassis. Similarly, DC ground can be used for shielding in case of the earth ground not being available.

![](images/942db4dae2acf781b75320318dff31fca6fc34d7533297e8358bbaee6df85b3e.jpg)  
Figure 33. Shielding technique

# 4.2.13 PCB layout recommendations

# Separating the analog and digital layouts

It is recommended to separate the analog and digital circuitry on the PCB (see Figure 34). This also avoids tracks crossing each other. The tracks carrying digital signals may introduce high-frequency noise in analog signals because of coupling.

The digital signals produce high-frequency noise because of fast switching.

Coupling of a capacitive nature is formed due to the metal connections (tracks) separated by the dielectric provided by the PCB base (glass, ceramic or plastic).

It is recommended to use different planes for analog and digital grounds. If there is a lot of analog circuitries, then an analog ground plane is recommended. The analog ground must be placed below the analog circuitry.

![](images/fa2a4e63f2551353acd123c31568ef1f07a0fa4d1396dd6900bfaafc65f9053e.jpg)  
Figure 34. Separating the analog and digital layouts

# Separating the analog- and digital-circuit power supplies

It is desirable to have separate analog and digital power supplies in cases where there are a lot of analog and digital circuits external to the microcontroller (see Figure 35). Depending on the STM32 package, different analog and digital power supply and ground pins are available. The VDDA/VREF+ and VDD pins can be powered from separate power supplies.

When using a switching-type power supply for the digital circuitry, it is recommended to use a separate linear supply for the analog circuit. Additionally, if a lot of noise is expected on the DC power supply due to l/O switching, etc., it is recommended to use a separate supply for the analog circuit.

![](images/10678484cb42ef8603d8b13243040452605ee890d403818ddcf690518789d7f5.jpg)  
Figure 35. Separating the analog and digital supplies

ai15493b

It is also recommended to connect the analog and digital grounds in a star network. This means that the analog and digital grounds must be connected at only one point. This prevents the introduction of noise in the analog power supply circuit due to digital signal switching. This also prevents current surges from affecting the analog circuit.

# Using separate PCB layers for the supply and ground

Two-layer PCBs

For two-layer PCBs, it is recommended to provide a maximum ground plane area. The power supply (VDD, VDDA) must run through thick tracks. The two layers can have their ground shorted together via multiple connections in the overlap region if the two layers feature the same ground signals. The unused PCB area can be used as the ground plane.

The other convention is to connect the unused PCB area on one layer to the positive supply (VDD) and the unused area on the other layer, to the ground. The advantage is a reduced inductance for power and ground signals. The maximum ground area provided for ground on the PCB results in a good shielding effect and reduces the electromagnetic induction susceptibility of the circuit.

Multilayer PCBs

Wherever possible, try to use multilayer PCBs and use separate layers on the PCB for power and ground. The VDD and Vss pins of the various devices can be directly connected to the power planes, thus reducing the length of track needed to connect the supply and ground. Long tracks have a high-inductive effect. The analog ground can be connected at one point to this ground plane. If so, it must be close to the power supply.

A full ground plane provides good shielding and reduces the electromagnetic induction susceptibility of the circuit.

Single-layer PCBs

Single-layer PCBs are used to save cost. They can be used only in simple applications when the number of connections is very limited. It is recommended to fillthe unused area with ground. Jumpers can be used to connect different parts of the PCB.

# 4.2.14 Component placement and routing

Place the components and route the signal traces on the PCB so as to shield analog inputs.

Components like resistors and capacitors must be connected with very short leads. Surface-mounted device (SMD) resistors and capacitors can be used. SMD capacitors can be placed close to the microcontroller for decoupling purposes.

Use wide tracks for power, otherwise, the series resistance of the tracks causes a voltage drop. Indeed, narrow power tracks have a nonnegligible finite resistance, so high load currents through them cause a voltage drop across them.

Quartz crystals must be surrounded by ground tracks/plane. The other side of the two-layer PCB below the crystal must preferably be covered by the ground plane. Most crystals have a metallic body that must be grounded. Additionally, place the crystal close to the microcontroller. A surface-mounted crystal can be used.

# 4.3 Software methods to improve precision

Averaging samples:

Averaging decreases speed but can improve accuracy

Digital filtering (50/60 Hz suppression from DC value)

A proper sampling frequency is set (the trigger from timer is useful in this case). Software postprocessing is performed on sampled data (for instance, comb filter for 50 Hz noise and its harmonics suppression).

Fast Fourier Transform (FFT) for AC measurements This method allows showing harmonic parts in a measured signal. It is slower due to the use of more computation power.

ADC calibration: offset, gain, bit weight calibration   
ADC calibration decreases internal ADC errors. However, the internal ADC structure must be known.

Minimizing the internal noise generated by the CPU The application has to be designed.

to use minimum disturbance from the microcontroller during ADC conversion. to minimize digital signal changes during sampling and conversion (digital silence).

# 4.3.1 Averaging samples

The principle of this method is to increase ADC precision but decrease ADC conversion speed (oversampling). If the measured analog signal produces unstable ADC values, then the mean value of the given input signal can be obtained by averaging a set of values. Variation can be caused by signal noise or noise generated by the microcontroller itself (high speed digital signals capacitively coupled to the analog input signal).

Averaging is performed by choosing an appropriate number of samples to be averaged. This number depends on the required precision, minimum conversion speed and the level of other ADC errors (if another error has a greater influence on ADC precision, then increasing the number of averaging values has no effect on total measurement precision).

In some STM32 microcontrollers, averaging can be performed by using the hardware oversampling feature: the ADC performs built-in hardware averaging according to configurable parameters (number of samples to average and final right bit shift of result).

The advantage of averaging is to improve ADC precision without any hardware changes. The drawback is that the conversion speed is lower as well as the frequency response (it is equivalent to decreasing effective sampling frequency).

# 4.3.2 Digital signal filtering

This method uses digital signal processing techniques.

In principle, averaging is also a simple digital filter with a specific frequency response. However, if the noise frequency spectrum is known, a digital filter can be designed which minimizes noise influence and maximizes ADC frequency response. For example, if the noise in the measured signal is coming from the 50 Hz power lines, then an appropriate digital filter suppresses only the 50 Hz frequency and delivers data signal without this noise.

The disadvantage of this method is that it requires appropriate microcontroller processing power and resources: CPU speed and data/program memory usage.

# 4.3.3 FFT for AC measurement

In some specific cases, the application needs to know the amplitude of an AC signal with a given frequency. In this case, the effective value of an AC signal can also be obtained by using a relatively slow sampling speed (in comparison to the measured signal frequency). For example, when measuring an AC mains signal (which is near-to-sinusoidal and has relatively low harmonics content), it is sufficient to choose a sampling frequency 32 times greater than the mains frequency (50 Hz). In this case harmonics of up to, the 15th order can be obtained. The amplitude of 15th harmonics in the main signal is very small (the next order harmonics can be neglected). The calculated effective value of the mains signal is obtained with high precision because the effective values of harmonics are added to the total AC harmonic value as:

![](images/1c32166f000703c76e2216286bbddf1010656cc543b7be2627bbea29cf147592.jpg)

So, if the 15th harmonics amplitude is only 1% (0.01) from the 1st harmonics (50 Hz), then its contribution to the total effective value is only 0.01% (because the square addition in the above equation gives: 0.012 = 0.0001).

The principle of this method is therefore to sample the AC signal with a known frequency and then perform postprocessing on the FFT for each measured period. Because the number of sampling points per measured signal period is small (32 points for example) then the performance needed for FFT processing is not so high (only 32-point FFT for example).

This method is well adapted for AC measurement of signals with lower distortion. The drawback is that it requires precise signal sampling:

The frequency of the measured signal must be known and the ADC sampling   
frequency must be set exactly as a 2" multiplier of the measured frequency.   
The input signal frequency is measured by another method.   
The ADC sampling frequency is tuned by programming the prescaler and MCU master clock selection (if sampling is performed with an inaccurate clock an interpolation can be used to obtain samples at the required points).

# 4.3.4 ADC calibration

This method requires knowledge of the internal ADC structure and of how the ADC converter is implemented inside the microcontroller. This is necessary to design a physical/mathematical model of the ADC implementation.

A proper physical model (which is usually a schematic diagram) is used as a basis for describing it mathematically. From the mathematical model, each element in the model can be obtained by a set of equations (for example, resistor/capacitor values, which represent bit weights). To solve these equations, it is necessary to perform a set of practical measurements and obtain a set of solvable equations.

From the measured values and mathematical computation of the model, all the known values of model elements (resistors, voltages, capacitors, ..) can be put into the schematic diagram.

As a result, instead of the ADC schematic with the designed values, an ADC schematic with the real values for a given microcontroller can be obtained.

Computed model parameters are stored in the microcontroller memory after calibration and used in postprocessing to correct ADC values.

# 4.3.5 Minimizing internal CPU noise

When the CPU operates, it generates a lot of internal and external signal changes, which are transferred into the ADC peripheral through capacitive coupling. This disturbance influences ADC precision (unpredictable noise due to different microcontroller operations).

To minimize influences of the CPU (and of other peripherals) on ADC, it is necessary to minimize digital signal changes during sampling and conversion time (digital silence). This is done using one of the following methods (applied during sampling and conversion time):

• Minimizing I/O pin changes • Minimizing internal CPU changes (CPU stop, wait mode) • Stopping clock for unnecessary peripherals (timers, communications...)

# 4.4 High impedance source measurement

This section describes the ADC measurement behavior of STM32 ADC when a signal source with high internal impedance is used. It explains how to design an application to reach the requested precision and provides workarounds.

# 4.4.1 ADC input stage problem

The ADC embedded in STM32 devices is a switched-capacitor ADC. Switched capacitors work also as sampling capacitors (see Section 2.1 for a detailed explanation).

When a signal comes from a voltage source with high internal impedance (for instance, 150 kΩ), an additional error can be seen in measurement results. Error signals have also been observed on the ADC input pin, as shown in Figure 38 (if the voltage source has zero voltage: Uin = 0 V, Rin = 150 kΩ, Cext = 0 pF):

![](images/a68c590d38e463bf68de31d5bba04a56384ebbe1dda0e9d514e42fc6f11c8118.jpg)  
Figure 36. Typical voltage source connection to ADC input

![](images/4f5e5efeb171a0b614ceff2fc24a1b7389220ed45c8f379eb80e78107fc2d3a9.jpg)  
Figure 37. Noise observed on ADC input pin during ADC conversions

ADC input signal during conversion: an ADC noise is injected to the input.

ai17904b

# 4.4.2 Explanation of the behavior

The explanation of this additional pin noise and additional measurement error (in case a signal source with high internal impedance is used) comes from the internal ADC structure: its input sampling circuit.

Figure 38 shows a simplified schematic of the input stage (sample and hold circuit).

![](images/0e5a58e551443fee0885883405b31179c8567fd48e6fc845beba0f24ac37a7b2.jpg)  
Figure 38. ADC simplified schematic of input stage - sample and hold circuit

The spikes (noise) present on ADC input pin during conversions are related to the sampling switch (S1). If the switch is closed, some charge (coming from the sample and hold capacitor Csh or caused by another effect) is transferred to the input pin. Then this charge starts discharging through the source impedance (Rin). The discharge process ends at the end of the sampling time (ts) when the switch S is opened. The remaining undischarged voltage remains on the capacitor Csh and ADC measures this voltage. If the sampling time (ts) is too short, the remaining voltage does not drop under 0.5 LSB and ADC measurement shows an additional error. Figure 39 illustrates this process.

![](images/6d0cee162896fee675f769f28e519a2dbcabcf8d4d478ac511a9fff97bda78c6.jpg)  
Figure 39. ADC input pin noise spikes from internal charge during sampling process

ai17906b

Note that a nonzero external capacitance Cext (parasitic pin capacitance) also exists, so during conversion time the pin capacitance is discharged through source impedanceRn

# 4.4.3 Minimizing additional errors

# Workaround for high impedance sources

To solve the additional error problem, the sampling time (Ts) can be increased by configuring ADC settings in MCU firmware, so that the Csh charge is discharged through the source impedance Rin. The time constant (Rin x Csh) is the reference for choosing the sampling time. To calculate the sampling time cycles, use this formula (for a maximum error of 1/2 LSB, see also Section 4.2.6):

![](images/3adc94f48d389cfa71695a54ff26ad4218c81a9a3cbf510bf1a39f4a62c68b5a.jpg)

The ADC clock (fADc) is another important factor, since slowing down the ADC clock increases the sampling time.

![](images/afa3511f0262af9e737f7be4024a6cc2b6ba9e8cfcf7f4b9189d2cb277c2ffd6.jpg)  
Figure 40. Effect of sampling time extension

ai17907b

If the maximum register value of the sampling time (Ts) setting is reached and the problem is stil present, more complex solution is needed, which is applicable also for measurements of source with extra high internal impedance (see Section : Workaround for extra high impedance sources).

Note that for this application, it is important to consider not only the internal sampling capacitance but also any external parasitic capacitance (in parallel to Cext), such as pin capacitance or PCB path capacitance.

Do not add any external capacitor (Cext) to the input pin when applying this above workaround. Its capacity increases the timing constant (Rin x Csh I| Cext) and the problem remains.

# Workaround for extra high impedance sources

This workaround combines both hardware and software changes.

# Hardware change

The hardware change consists in adding a large external capacitor (Cext) to the input pin. The capacity size connected to the input pin must reach the value that causes the discharging of the internal sampling capacity Csh to the external capacitor Cext without increasing the voltage on Cext to more than 0.5 LSB.

Example

If the internal capacitor (Csh = 16 pF) is charged to full scale (Umax, which corresponds to 4095 LSB), then the external capacitor Cext must be charged at maximum 0.5 LSB voltage level (Uisb) after discharging Csh to it. The capacity of Cext is then:

![](images/99da2442eb8f9b061f7870eae2f48db78ad45aaf257ff00f11c684a7ba1a0ccb.jpg)

The closest larger standard value chosen here is: Cext = 150 nF.

If the internal sampling capacitor Csh is not charged to full voltage range (4095 level) before sampling, the Cext value can be computed by replacing "4095" in the formula above. Calculating with 4095 level gives precise measurement results also in the case of ADC input channels switching (Csh was charged from different ADC input in the previous measurement).

A side effect of this hardware workaround is the cyclical charging of Cext which must be taken into account. Each ADC conversion transfers the charge from Csh to Cext. One transfer charges the Cext below 0.5 LSB, as described above, but more transfers can charge Cext to larger values if it is not discharged between two conversions. Figure 41 shows an example of this scenario where the ADC measurement is performed faster.

![](images/49ca94e98dada8675e0270eec47d597e4b34039636a3b9a8f7d97a6769f2ae6b.jpg)  
Figure 41. Charging the external capacitor with too short time between conversions

# Software change

The side effects mentioned above can be solved by software. The objective is to create a delay to let Cext discharge through Rin (not measure so often) giving enough "discharge time" between ADC conversions. The "discharge time" (tc) is equal to the transferred charge >> Csh.

![](images/6272cdf8fd77110ea5800b5e5f32571e66b9a171805cc4a8a9c2739e7956fe49.jpg)

tc t Qdisch arging UIsb Rin e RinCext dt 0

where:

UIsb ... 0.5 LSB voltage Ievel Umax ... 4095 LSB voltage level (worst case) Qcharging = Qdischarging

![](images/6ead214ec104f9c3f9066bae2c044570d6f3b6c3bdb09e9c17c31caea1e727f8.jpg)

Simplification of the above formula gives the final formula for the required waiting time between conversions:

![](images/314bb8e341ed5d932734a284f9b2aec631fcbe6ad91c445aa437cfd8d5195c1d.jpg)

This final formula shows the dependency between the external capacitor Cext and the required waiting time between two conversions if the precision Uisb is needed.

From the same formula, the argument in the logarithm must be positive. Therefore, there is a tionor theinimal valu  e

![](images/aa656aa48f1f5da9f516c0284adfb26254963881cdf68640bdbcead0e5556cfd.jpg)

![](images/7454d99fa3fb0534d31246dd855a9df91679fc538f870b4b5a9f80a156001272.jpg)

![](images/403945ce27385518c2589caab92e9c7b1c169df8c239f98f1f1d92194bc0338f.jpg)

Choosing a larger Cext decreases more the time between conversions (tc).

An extra large Cext (ext>h Umax enables sampling more often. Ulsb   
However, increasing Cext limits the frequency bandwidth of the measurement signal   
(increasing the "external" timing constant Rin . Cext).

The formulas below show how to choose the optimal Cext value: signal bandwidth in correlation with sample time. Signal bandwidth is characterized by an "external" timing constant, so the optimal solution is to charge Cext during tc:

![](images/b28dcb606f69decca1972d656b83eb10f574511f876d98a7ab5caf80a4141a31.jpg)

![](images/aef01f7f869ba6a1d87dbe57112465c8fdf969138d10952e2c118aee4b1153c8.jpg)

![](images/a2cf95f1a80b717972890652dd2647ec9304f2018a315c0ab8e7fc03b0cf65f5.jpg)

![](images/c396e9fbb2d7ff7778e53bb91b9a32ec21e1b471523c4e8c631918d37a5673e0.jpg)

and the corresponding waiting time between conversions:

![](images/dc36fba441f9f9c611c547b9e5250b476791fc37fd0b71b25277dec18147621e.jpg)

Practically the firmware must not program the ADC in continuous mode but only in single mode and must ensure that there is a time gap between conversions with duration equal to tc. This adding of waiting time is the software change, which must be applied together with the hardware change (adding an external capacitor Cext).

Without implementation of tc waiting time in software (for instance, running a conversion just after the first one) the external capacitor Cext is cyclically charged from the Csh capacitor. After a lot of cycles, the voltage on Cext reaches a quite high error value (as previously shown in Figure 41).

A practical example of implementation for STM32L1 ADC is shown below:

Csh = 16 pF ....ADC property Rin = 150 kΩ ... signal source property

Umax = 4095 LSB .... ADC property UIsb = 0.5 LSB .. required precision

![](images/72e65df8080a972da8adc424126a8c5939a50341482c35237d4060513c3c72b1.jpg)

C = −(Rn · ext) · In[ 1. Can Uma ma] 16pF 4095 ≈ 29879μs =30ms

# 4.4.4 Source of described problem - ADC design

The following sections list some possible causes for the charging of the internal sampling capacitor Csh. This is not an exhaustive list; only the main possible sources of the ADC design are mentioned.

# Parasitic switch capacitance effect

The sampling switch inside ADC sampling circuit (see Figure 38) is not ideal. In reality the sample and hold switch (S1) is designed as 2 transistors (PMOS and NMOS, see Figure 42):

![](images/8dc0817247d3bc706391e806784fc61661b8a08461ce79e64511a1aed1b3f84d.jpg)  
Figure 42. Implementation of sampling switch

ai17909b

The switch is controlled by the gate voltages of transistors (inverted signal on PMOS traistor.This des   sadard bidctioal sith orail l nge  iu voltages). Both transistors have parasitic capacitances between gate and source.

If those capacitances are charged (close to the switch), then their charge can be transferred to the sampling capacitor (see Figure 43).

![](images/1ec7695ba8c2ee08f57082abdd8b97a0101cc6a1aed6253d7a699309b35bb8e4.jpg)  
Figure 43. Parasitic capacitances of sampling switch

ai17910b

This charging and discharging currents (PMOS and NMOS asymmetric capacitances) can charan smlin apc

# Internal charging of the sampling capacitor

It is possible that after the conversion process (successive approximation process in SAR type of ADC) the sample and hold capacitor Csh is charged to some voltage. The reason can be:

Some leakage current to Csh (parasitic current inside ADC structure, see Figure 44). Residual charge transfer from the switches when the ADC structure is switched back to the default state before the next conversion.   
Other reasons (related to internal ADC parasitic structures).

![](images/f87414cc150ecdb991d98924ae7e86c417424d88b8a13ddc82e6166ef31a7b67.jpg)  
Figure 44. Parasitic current example inside ADC structure

# 5 Conclusion

This application note describes the main ADC errors and then methods and application design rules to minimize STM32 microcontroller ADC errors and obtain the best ADC accuracy.

The choice of method depends on the application requirements and is always a compromise between speed, precision, enough computation power and design topology. The published methods lead to a precision improvement and are optimized for the design of an ADC converter using the SAR (successive approximation register) principle.

# 6 Revision history

Table 8. Document revision history   

<table><tr><td rowspan=1 colspan=1>Date</td><td rowspan=1 colspan=1>Revision</td><td rowspan=1 colspan=1>Changes</td></tr><tr><td rowspan=1 colspan=1>14-Nov-2008</td><td rowspan=1 colspan=1>1</td><td rowspan=1 colspan=1>Initial release.</td></tr><tr><td rowspan=1 colspan=1>16-Sep-2013</td><td rowspan=1 colspan=1>2</td><td rowspan=1 colspan=1>Extended to STM32Fx Series and STM32L1 Series devices.Added Section 2.1: SAR ADC internal structure.Added Section 4.4: High impedance source measurement.Added Section 4.3: Software methods to improve precision.Text improvements and additions.Changed the Disclaimer on the final page.</td></tr><tr><td rowspan=1 colspan=1>15-Feb-2017</td><td rowspan=1 colspan=1>3</td><td rowspan=1 colspan=1>Document scope extended to all STM32 microcontrollers.Updated Figure 5: Step 2: If MSB = 0, then compare with 1/4VREF andFigure 6: Step 2: If MSB = 1, then compare with 3/4VREF.Updated Section 4.3: Software methods to improve precisionintroduction.Added STM32L0/L4 ADC hardware oversampling in Section 4.2.3:Analog-input signal noise elimination, Section 4.2.4: Adding whitenoise or triangular sweep to improve resolution and Section 4.3.1:Averaging samples.Harmonized hexadecimal notation to &#x27;0x&#x27;.Harmonized least significant bit term to &#x27;LSB&#x27;.Updated figures look-and-feel and ground symbol. Color legendadded when required.</td></tr><tr><td rowspan=1 colspan=1>07-Nov-2019</td><td rowspan=1 colspan=1>4</td><td rowspan=1 colspan=1>Modified Introduction.Added the Arm logo and trademark notice in Section 1: Generalinformation.Added Section 3.2.3: Reference voltage decoupling and impedance.Updated Section 4.2.1: Reference voltage / Power supply noiseminimization, Section 4.2.2: Reference voltage / Power-supplyregulation, Section 4.2.3: Analog-input signal noise elimination,Section 4.2.4: Adding white noise or triangular sweep to improveresolution (references to STM32 devices changed), Section 4.2.5:Matching the ADC dynamic range to the maximum signal amplitude,Section 4.2.6: Analog source resistance calculation.Added Section 4.2.7: External analog buffer usageUpdated Section 4.2.8: Source frequency condition vs. source andparasitic capacitors, Section 4.3.1: Averaging samples (references toSTM32 devices changed).</td></tr><tr><td rowspan=1 colspan=1>25-Aug-2020</td><td rowspan=1 colspan=1>5</td><td rowspan=1 colspan=1>Renamed Section 4.2.6 into SAR ADC sampling time prerequisitesand section deeply reworked</td></tr><tr><td rowspan=1 colspan=1>16-Dec-2020</td><td rowspan=1 colspan=1>6</td><td rowspan=1 colspan=1>Updated Table 2: ADC SMP selection vs STM32 Series (in ADC clockcycles).Updated Section 3.1.3: Differential linearity error and Section 3.1.5:Total unadjusted error.</td></tr></table>

Table 8. Document revision history   

<table><tr><td rowspan=1 colspan=1>Date</td><td rowspan=1 colspan=1>Revision</td><td rowspan=1 colspan=1>Changes</td></tr><tr><td rowspan=1 colspan=1>31-May-2021</td><td rowspan=1 colspan=1>7</td><td rowspan=1 colspan=1>Updated conversion results corresponding to 1.9998 V and 2.0014 Vanalog input voltage in Section 3.1.3: Differential linearity error.Replaced 4095 by 4096 LSB in the equations used to calculate theconverted value in Section 3.2.1: Reference voltage noise.Updated equations used to calculate the digital code and the digitaloutput in Section 3.2.2: Reference voltage / power supply regulation.Section 3.2.6: ADC dynamic range bad match for maximum inputsignal amplitude: changed maximum value converted by the ADC to3103 and updated Figure 14: Input signal amplitude vs. ADC dynamicrange (VREF+ = 3.3 V).Updated Figure 23: Selecting the reference voltage and Figure 24:Preamplification.Changed 4096 to 4095 LSB in Section : Workaround for extra highimpedance sources</td></tr><tr><td rowspan=1 colspan=1>10-Jan-2022</td><td rowspan=1 colspan=1>8</td><td rowspan=1 colspan=1>Formula used to calculate LSB made generic in Section 3: ADCerrors.</td></tr><tr><td rowspan=1 colspan=1>22-Aug-2023</td><td rowspan=1 colspan=1>9</td><td rowspan=1 colspan=1>Removed the figure:SMP clock cycles vs STM32 Series.Updated the following elements:Section : IntroductionSection 4.2.8: Source frequency condition vs. source and parasiticcapacitorsTable 2: ADC SMP selection vs STM32 Series (in ADC clock cycles).Table 4.4.3: Minimizing additional errorsTable 8: Negative offset error representation.Table 4.2.2: Reference voltage / power supply regulationTable 4.2.5: Matching the ADC dynamic range to the maximum signalamplitudeUpdated the whole document with minor changes.</td></tr><tr><td rowspan=1 colspan=1>25-Oct-2024</td><td rowspan=1 colspan=1>10</td><td rowspan=1 colspan=1>Updated:Figure 8: Negative offset error representation- Note for Figure 5: Step 2: If MSB = 0, then compare with 14VREFand Figure 6: Step 2: If MSB = 1, then compare with 34VREFFigure 20: Power supply and reference decoupling for 100- and144-pin packagesFigure 21: Power supply decoupling for 36-, 48- and 64-pinpackages</td></tr></table>

# IMPORTANT NOTICE  PLEASE READ CAREFULLY

acknowledgment.

the design of Purchasers' products.

No license, express or implied, to any intellectual property right is granted by ST herein.

product or service names are the property of their respective owners.

I