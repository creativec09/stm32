# Guidelines for oscillator design on STM8AF/AL/S and STM32 MCUs/MPUs

# Introduction

Many designers know oscillators based on Pierce-Gate topology (Pierce oscillators), but not all of them really understand how they operate, and only a few master their design. In practice, limited attention is paid to the oscillator design, until it is found that it does not operate properly (usually when the final product is already in production). A crystal not working as intended results in project delays, if not overall failure.

The oscillator must get the proper amount of attention during the design phase, well before moving to manufacturing, to avoid the nightmare scenario of products failing in application.

This document introduces the Pierce oscillator basics, and provides guidelines for its design. It also shows how to determine the external components, and provides guidelines for correct PCB design and for selecting crystals and external components.

To speed up the application development, the recommended crystals (HSE and LSE) for the products listed in Table 1 are detailed in Section 5: Recommended resonators for STM32 MCUs/MPUs and Section 6: Recommended crystals for STM8AF/AL/S MCUs.

Table 1. Applicable products   

<table><tr><td rowspan=1 colspan=1>Type</td><td rowspan=1 colspan=1>Product categories</td></tr><tr><td rowspan=5 colspan=1>Microcontrollers</td><td rowspan=1 colspan=1>STM8S series, STM8AF series and STM8AL series</td></tr><tr><td rowspan=1 colspan=1>STM32 32-bit Arm® Cortex® MCUs</td></tr><tr><td rowspan=1 colspan=1>STM32 Wireless MCUs</td></tr><tr><td rowspan=1 colspan=1>STM32 Ultra Low Power MCUs</td></tr><tr><td rowspan=1 colspan=1>STM32 High Performance MCUs</td></tr><tr><td rowspan=1 colspan=1>Microprocessors</td><td rowspan=1 colspan=1>STM32 Arm® Cortex® MPUS</td></tr></table>

# Contents

# Quartz crystal properties and model . . . . ..6

# Oscillator theory .8

2.1 Negative resistance 8   
2.2 Transconductance 9   
2.3 Negative-resistance oscillator principles 10

# Pierce oscillator design 11

3.1 Introduction to Pierce oscillators .11   
3.2 Feedback resistor . .11   
3.3 Load capacitance 12   
3.4 Oscillator transconductance 13

# 3.5 Drive level and external resistor calculation 14

3.5.1 Calculating the drive level 14   
3.5.2 Another drive level measurement method 16   
3.5.3 Calculating the external resistor .16

# Startup time 17

3.7 Crystal pullability 17

# 3.8 Safety factor 18

3.8.1 Definition 18   
3.8.2 Measurement methodology 19   
3.8.3 Safety factor for STM32 and STM8 oscillators 19

# 3.9 Oscillation modes 20

3.9.1 What are fundamental and overtone modes? 20   
3.9.2 Third overtone mode: pros and cons 21   
3.9.3 Considerations for crystals interfaced with STM32 products . 22

# Guidelines to select a suitable crystal and external components . . 23

4.1 Low-speed oscillators embedded in STM32 MCUs/MPUs . . . 23   
4.2 How to select an STM32-compatible crystal 26

# Recommended resonators for STM32 MCUs/MPUs • . . . 29

5.1 STM32-compatible high-speed resonators 29   
5.2 STM32-compatible low-speed resonators 29

# Recommended crystals for STM8AF/AL/S MCUs . . 42

6.1 Part numbers of recommended crystal oscillators 42   
6.2 Recommended ceramic resonators 43

# Tips for improving oscillator stability . . .. . 44

7.1 PCB design guidelines 44   
7.2 PCB design examples 46   
7.3 Soldering guidelines 50   
7.4 LSE sensitivity to PC13 activity 50

# Reference documents . . . .. 52

FAQs . . . 53

Conclusion .. .. 54

Revision history .. 55

# List of tables

Table 1. Applicable products 1   
Table 2. Example of equivalent circuit parameters. . .7   
Table 3. Typical feedback resistor values for given frequencies 12   
Table 4. Safety factor (Sf) for STM32 and STM8 oscillators. . 19   
Table 5. LSE oscillators embedded into STM32 MCUs/MPUs. 25   
Table 6. HSE oscillators embedded in STM32 MCUs/MPUs. 29   
Table 7. Recommended crystal / MEMS resonators for the LSE oscillator in STM32 products. . 31   
Table 8. KYOCERA compatible crystals (not exhaustive list). 42   
Table 9. NDK compatible crystals (not exhaustive list). 42   
Table 10. Recommended conditions (for consumer) 43   
Table 11. Recommended conditions (for CAN-BUS) 43   
Table 12. Document revision history 55

# List of figures

Figure 1. Quartz crystal model. 6   
Figure 2. Impedance in the frequency domain.. 6   
Figure 3. l-V curve of a dipole showing a negative trans-resistance area. 9   
Figure 4. Block diagram of a typical oscillation loop based on a crystal resonator 10   
Figure 5. Pierce oscillator circui 11   
Figure 6. Inverter transfer function. . 12   
Figure 7. Current drive measurement with a current probe. 15   
Figure 8. Negative resistance measurement methodology description. 19   
Figure 9. Fundamental and overtone frequencies of an AT-cut quartz crystal 20   
Figure 10. Quartz crystal theoretical model with third overtone. . 21   
Figure 11. Oscillator implementation for third overtone . 21   
Figure 12. Classification of low-speed crystal resonators 23   
Figure 13. Recommended layout for an oscillator circuit. 45   
Figure 14. PCB with separated GND plane and guard ring around the oscillator 46   
Figure 15. GND plane 46   
Figure 16. Signals around the oscillator. 46   
Figure 17. Preliminary design (PCB design guidelines not respected) 47   
Figure 18. Final design (following guidelines) 48   
Figure 19. GND plane 48   
Figure 20. Top layer view. 48   
Figure 21. PCB guidelines not respected 49   
Figure 22. PCB guidelines respected 50

# Quartz crystal properties and model

A quartz crystal is a piezoelectric device converting electric energy into mechanical energy, and vice versa. The transformation occurs at the resonant frequency. The quartz crystal can be modeled as shown in Figure 1.

![](images/2e4cf1a9ece2d31f04bec4ce4ab073ebd85566493fbc2a086c34cf5e9250b487.jpg)  
Figure 1. Quartz crystal model

Co represents the shunt capacitance resulting from the capacitor formed by the   
electrodes   
Lm (motional inductance) represents the vibrating mass of the crystal   
Cm (motional capacitance) represents the elasticity of the crystal   
Rm (motional resistance) represents the circuit losses

The impedance of the crystal (assuming that Rm is negligible) is

![](images/dccd0363526edd17e60f1c9744f5bd152a92bac4b0c0ef2d66c4cc3ed263a177.jpg)

Figure 2 shows the impedance in the frequency domain.

![](images/0a8cffdd67fbd2739ce752443b6bdf0892f094ba0b2f8fa5051d6018c9998f2e.jpg)  
Figure 2. Impedance in the frequency domain

Fs is the series resonant frequency when Z = 0. Its expression can be deduced from equation (1) as follows:

![](images/caa0ec306381e5378ed07450bc74922a7ba2321a74ff5373045570d7186351ae.jpg)

Fa is the antiresonant frequency when Z tends to infinity. Using equation (1), it is expressed as follows:

![](images/3ffa602f49b7cfa7cf0c1435f8ff28d8079db1b017c6056857938114597049de.jpg)

The region delimited by Fs and Fa (shaded area in Figure 2) is the area of parallel resonance. In this region, the crystal operates in parallel resonance and behaves as an inductance that adds an additional 180° phase to the loop. Its frequency Fp (or FL: load frequency) has the following expression:

![](images/6bc843ff35e3accf9ea3bcb87ec3bca61d2ca6397c0ca264f58395323fac1b84.jpg)

According to this equation, the oscillation frequency of the crystal can be tuned by varying the load capacitance CL. This is why, in their datasheets, crystal manufacturers indicate the exact C_ required to make the crystal oscillate at the nominal frequency.

Table 2 gives an example of equivalent crystal circuit component values for an 8 MHz nominal frequency.

Table 2. Example of equivalent circuit parameters   

<table><tr><td rowspan=1 colspan=1>Equivalent component</td><td rowspan=1 colspan=1>Value</td></tr><tr><td rowspan=1 colspan=1>Rm</td><td rowspan=1 colspan=1>8 Ω</td></tr><tr><td rowspan=1 colspan=1>Lm</td><td rowspan=1 colspan=1>14.7 mH</td></tr><tr><td rowspan=1 colspan=1>Cm</td><td rowspan=1 colspan=1>0.027 pF</td></tr><tr><td rowspan=1 colspan=1>Co</td><td rowspan=1 colspan=1>5.57 pF</td></tr></table>

Using equations (2), (3), and (4), it is possible to calculate Fs, Fa, and Fp of this crystal:

Fs = 7988768 Hz Fa = 8008102 Hz

If the load capacitance CL is equal to 10 pF, the crystal oscillates at Fp = 7995695 Hz.   
To have an oscillation frequency of exactly 8 MHz, CL must be 4.02 pF.

# 2 Oscillator theory

Oscillators are among the backbone components of modern digital ICs. They can be classified into different subfamilies, depending upon their topology and operating principles. For each subfamily there is a mathematical model that can be used to study the oscillator behavior, and theoretically determine its performance.

This section deals only with harmonic oscillators (relaxation oscillators are out of the scope of this document), with particular focus (see Section 3) on Pierce oscillators. This is because all the oscillators requiring external passive components (resonator, load capacitors, etc.) covered by this document are of the previously mentioned type and topology.

The harmonic oscillator family can be divided into two main subfamilies:

negative-resistance oscillators positive-feedback oscillators.

These two subfamilies of oscillators are similar for what concerns the output waveform. They deliver an oscillating waveform at the desired frequency. This waveform is typically composed of a fundamental sine wave of the desired frequency, plus a sum of overtone harmonics (at frequencies multiple of the fundamental one), due to the nonlinearity of components of the oscillation loop.

The two subfamilies differ in their operating principles. A specific mathematical model describes and analyzes each of them.

Positive-feedback oscillators are usually modeled using the Barkhausen model, where an oscillator must fulfll the Barkhausen criterion to maintain a stable oscillation at the desired frequency.

The Barkhausen model is not fully adequate to describe negative-resistance oscillators: the most suitable approach is to use the negative-resistance model described in [1].

STM32 microcontrollers and microprocessors (based on Arm®(a) cores) feature low-speed external (LSE) and high-speed external (HSE) oscillators designed according to the negative-resistance principle, hence this section focuses on the presentation of this model.

# 2.1 Negative resistance

Theoretically speaking, a negative resistance is a dipole that absorbs heat and converting it in electrical current, proportional to the applied voltage, but flowing in the opposite direction (the opposite mechanism of an electrical resistance). In the real world, such a dipole does not exist.

# arm

The term negative resistance is a misnomer of negative transresistance, defined as the ratio between a given voltage variation (∆V) and the induced current variation (∆l). Unlike the resistance, always positive, the transresistance (also known as differential resistance) can be either positive or negative. Figure 3 shows the current-voltage curve for a dipole with a negative transresistance region. It is obvious that the V/l ratio is always positive, this is not the case for the ΔV/∆l ratio.

The portion of the I-V curve in purple shows a negative transresistance:

![](images/dc3695f89327ced4e4c6aa3192c635ed9dcae1967c8a32485c070de728bafd79.jpg)

The portions in blue feature a positive transresistance:

![](images/a740fb4e2b14165d55cbe15f33d49f0193f0d66f55a5bc4cc7720005ffd0ff31.jpg)

![](images/dd2a12fede61c849d0685dca57e53107206cd7a6ffffa5a09ccc7c6c159e5d7d.jpg)  
Figure 3. I-V curve of a dipole showing a negative trans-resistance area

# 2.2 Transconductance

Similarly to the conductance, defined as the inverse of the resistance, the transconductance is defined as the inverse of the transresistance. Transconductance can also be defined as the differential conductance, expressed as ∆I / ∆V.

# 2.3 Negative-resistance oscillator principles

An oscillation loop is made of two branches (see Figure):

The active branch, composed by the oscilator itself, provides the energy to make the oscillation start and build up until it reaches a stable phase. When a stable oscillation is reached, this branch provides the energy to compensate for the losses of the passive branch.   
The passive branch is mainly composed by the resonator, the two load capacitors and all the parasitic capacitances.

![](images/916029af2da2131c8428ffa43d522667030d2da6e115a5d8f528fa0444fa5d89.jpg)  
Figure 4. Block diagram of a typical oscillation loop based on a crystal resonator

MSv36188V1

According to the small signals theory, when the active branch (oscillator part) is correctly biased, to maintain a stable oscillation around the oscillator biasing voltage the latter must have its transconductance equal to the passive branch conductance.

However, at startup, the oscillator transconductance must be higher than (multiple of) the conductance of the passive part of the oscillation loop, to maximize the possibility to build up the oscillation from the inherent noise of the loop. An excessive oscillator transconductance compared to the oscillation loop passive branch conductance can saturate the oscillation loop, and cause a startup failure.

To ensure the successful oscillator start, and to maintain stable oscillation, the ratio between the negative resistance of the loop and the crystal maximal equivalent series resistance (ESR) is specified for STM32 and STM8 products. It is recommended to have a ratio higher than 5 for the HSE oscillators, and higher than 3 for the LSE oscillators.

# 3 Pierce oscillator design

This section describes the different parameters, and how to determine their values to be compliant with the Pierce oscillator design.

# 3.1 Introduction to Pierce oscillators

Pierce oscillators are variants of Colpitts oscillators, widely used with crystal resonators. A Pierce oscillator (see Figure 5) requires a reduced set of external components, this results in a lower final design cost. In addition, the Pierce oscillator is known for its stable oscillation frequency when paired with a crystal resonator, in particular a quartz-crystal resonator.

![](images/4d307da1c2e41da8fb233078d331dcab9d6dc13937947961d0ed452b4165c7d7.jpg)  
Figure 5. Pierce oscillator circuitry

• Inv: the internal inverter that works as an amplifier   
• Q: crystal quartz or a ceramic resonator   
• RF: internal feedback resistor   
• RExt: external resistor to limit the inverter output current   
• CL1 and CL2: are the two external load capacitances C: stray capacitance, sum of the device pin (OSC_IN and OSC_OUT) and the PCB (a parasitic) capacitances.

# 3.2 Feedback resistor

In most MCUs/MPUs manufactured by ST, R= is embedded in the oscillator circuitry. Its role is to make the inverter act as an amplifier. The feedback resistor is connected between Vin and Vout to bias the amplifier at Vout = Vin, and force it to operate in the linear region (shaded

area in Figure 6). The noise (for example, the thermal noise of the crystal) is amplified within the range of serial to parallel frequency (Fa, Fp), thus starting the oscillation.

![](images/36545bc2609ee6ca0d4621698569cb4da3debfdbdd8e95d69ceb74907f14213c.jpg)  
Figure 6. Inverter transfer function   
Table 3 provides typical values of Rp.

ai15837b

Table 3. Typical feedback resistor values for given frequencies   

<table><tr><td rowspan=1 colspan=1>Frequency</td><td rowspan=1 colspan=1>Feedback resistor range</td></tr><tr><td rowspan=1 colspan=1>32.768 kHz</td><td rowspan=1 colspan=1>10 to 25 MΩ</td></tr><tr><td rowspan=1 colspan=1>1 MHz</td><td rowspan=1 colspan=1>5 to 10 MΩ</td></tr><tr><td rowspan=1 colspan=1>10 MHz</td><td rowspan=1 colspan=1>1 to 5 MΩ</td></tr><tr><td rowspan=1 colspan=1>20 MHz</td><td rowspan=1 colspan=1>470 kΩ to 5 MΩ</td></tr></table>

# 3.3 Load capacitance

The load capacitance is the terminal capacitance of the circuit connected to the crystal oscillator. This value is determined by the external capacitors CL1 and CL2, and the stray capacitance of the printed circuit board and connections (Cs). The CL value is specified by the crystal manufacturer. For the frequency to be accurate, the oscillator circuit must show the same load capacitance  the ystal  the ne the cystal was adjusted r. requency are used to tune the desired value of CL, to reach the value specified by the crystal manufacturer.

The following equation gives the expression  CL:

![](images/759904491c040b9a177dfbd61d0bc5d7ca8b287ad4c156b7e818b6d003ed819d.jpg)

For example, with CL = 15 pF and C = 5 pF ,

![](images/43b160184ca84d88d8391207dde97f11885416640bff48be80d8b2783580c43a.jpg)

hence CL1 = CL2 = 20 pF.

# 3.4 Oscillator transconductance

Theoretically, to make the oscillation start and reach a stable phase, the oscillator must provide sufficient gain to compensate for the loop losses and to provide the energy for the oscillation buildup. When the oscillation becomes stable, the power provided to the oscillator and the one it dissipates in the loop are equal.

Practically, because of tolerances on passive component values and their dependency upon environmental parameters (such as temperature), the ratio between oscillator gain and oscillation loop critical gain cannot just exceed 1. This would induce a too long oscillator startup time, and even prevent the oscillator from starting up.

This section describes the two approaches that can be used to check if an STM32 oscillator can be paired with a given resonator, to ensure that the oscillation is started and maintained under the specified conditions for both resonator and oscillator. The approach depends on how the oscillator parameters are specified in the device datasheet:

If the oscillation loop maximum critical transconductance parameter (Gm_crit_max) is see the formula below). Note that the maximum critical crystal transconductance can be named either Gm_crit_max or Gm, depending on the STM32 product documentation. If the oscillator transconductance parameter (9m) is specified, make sure that the gain margin ratio (gainmargin) is bigger than 5.

The gain margin ratio is determined by the formula gainmargin = 9m / 9mcrit, where

9m is the oscillator transconductance specified in the STM32 datasheet. The HSE oscillator transconductance is in the range of a dozen of mA/V, while the LSE oscillator transconductance ranges from a few to a few dozens of µA/V, depending upon the product. 9mcrit is defined as the minimal transconductance required to maintain a stable oscillation when it is a part of the oscillation loop for which this parameter is relevant. 9mcrit is computed from oscillation loop passive components parameters.

Assuming CL1 = CL2, and that the crystal sees the same C_ on its pads as the value given by the crystal manufacturer, 9mcrit is expressed as follows:

![](images/79b17406485a1a9e281c5289447bdaaca30ca8f8ee2917bb93e0648fc2780a91.jpg)

where:

• ESR is the equivalent series resistance • Co is the crystal shunt capacitance • CL is the crystal nominal load capacitance. F is the crystal nominal oscillation frequency

For example, to design the oscillation loop for the HSE oscillator embedded in an STM32F1 microcontroller with a transconductance value (9m) of 25 mA/V, we choose a quartz crystal from Fox, with the following characteristics:

Frequency = 8 MHz • C0 = 7 pF • CL = 10 pF • ESR = 80 Ω

![](images/7992ac1d031a7e868684f487f6e50c7f1574e7be63615e8af4055b0354338ca6.jpg)

Calculating the gain margin gives:

![](images/3ab19e1fc43370921a5c789a4d8e6aaa7e0af4eb606a0dd869d8b8e2c820a354.jpg)

The gain margin is sufficient to start the oscillation and the gainmargin > 5 condition is met. The oscillator is expected to reach stable oscillation after the typical delay specified in the datasheet.

If an insufficient gain margin is found (gainmargin < 5), the oscillation can start when designing and testing the final application, but this does not guarantee that the oscillation starts in operating conditions. It is highly recommended that the selected crystal has a gain margin higher than or equal to 5 (try to select a crystal with a lower ESR and/or a lower CL).

In a second example of the case where the maximal critical crystal transconductance is n, te HSE  e in T2G0oe ha Gm = 1.mA/V. for the implemented oscillator must stay below this value. The Fox quartz crystal described above respects this condition.

The conversion between the oscillator transconductance (9m) and the oscillation loop maximal critical transconductance Gm_rit_max) is given by Gm_crit_max = m / 5.

Note:

Before any verification, the crystal chosen must vibrate at a frequency that respects the oscillator frequency range given in the STM32 datasheet.

# 3.5

# Drive level and external resistor calculation

The drive level (DL) and external resistor value (RExt) are closely related, and are addressed in the same section.

# 3.5.1 Calculating the drive level

The drive level is the power dissipated in the crystal. It must be limited, otherwise the quartz crystal can fail because of excessive mechanical vibrations. The maximum drive level is specified by the crystal manufacturer, usually in mW. Exceeding this value can lead to crystal damage, or to a shorter device lifetime.

The ive level i given by he oula: L= E I²:

ER is the equivalent series resistor (specified by the crystal manufacturer):

![](images/f41f12af77f17eea93e035555eae346a8d0773b62e186c92e56f69662d3e474f.jpg)

Iq is the current flowing through the crystal in RMS. This current can be displayed on an oscilloscope as a sine wave. The current value can be read as the peak-to-peak value (Ipp). When using a current probe (as shown in Figure 7), the voltage scale of an oscilloscope may be converted into 1 mA / 1 mV.

![](images/789b0db938fa498828030eca27d000804498b93cdbaadb84ee081d1955d6911f.jpg)  
Figure 7. Current drive measurement with a current probe

So, as described previously, when tuning the current with the potentiometer, the current through the crystal (assuming it is sinusoidal) does not exceed IQmax RMS, given by:

![](images/f905a796ab0c84f40f6eaa5b177259f88e33e1bc03f0bddcdf2e404b188f1dcb.jpg)

Therefore, the current through the crystal (peak-to-peak value readon the oscillosope should not exceed a maximum peak-to-peak (lQmaxPP) equal to:

![](images/b3bc61d1b46e5dcb66fd52923497376f12d328b3bfc8dee5b7d858913cc607c5.jpg)

Hence, the need for an external resistor RExt (refer to Section 3.5.3) when IQ exceeds IQmaxPP. The addition of RExt becomes mandatory, and is added to ESR in the expression of  IQmax\*

# 3.5.2 Another drive level measurement method

The drive level can be computed as DL= I²QRMS \* ESR (IQRMs is the RMS AC current).

This current can be calculated by measuring the voltage swing at the amplifier input with a low-capacitance oscilloscope probe (no more than 1 pF). The amplifier input current is negligible with respect to the current through CL1, so we can assume that the current through the crystal is equal to the current flowing through CL1. Therefore, the RMS voltage at this point is related to the RMS current by lQRMs = 2 π F x VRMS X Ctot, with:

F = crystal frequency Vpp   
VRMS   
Cot = CL1 + (C / 2) + Cprobe where: CL1 is the external load capacitance at the amplifier input Cs is the stray capacitance Cprobe is the probe capacitance

Theore, D ES×t 2

This value must not exceed the drive level specified by the crystal manufacturer.

Note:

Use special care when measuring voltage swing at LSE input, as it is very sensitive to load capacitance. It is recommended to use a 0.1 pF input capacitance probe.

# 3.5.3 Calculating the external resistor

The role f this resistor is to lmit the drive levelof the crystal. With L, it forms a low-pass filter that forces the oscillator to start at the fundamental frequency and not at overtones (prevents the oscillator from vibrating at the odd harmonics of the fundamental frequency). If the power dissipated in the crystal is higher than the value specified by the crystal manufacturer, the external resistor RExt becomes mandatory to avoid overdriving the crystal. If the power dissipated in the selected quartz is lower than the drive level specified by the crystal manufacturer, the insertion of RExt is not recommended, and its value is then 0 Ω.

A  o a Tus h val    eual  the an .

Therefore, RExt = 1 / (2 π F CL2), and so, with an oscillation frequency of 8 MHz and CL2 = 15 pF, we have RExt = 1326 Ω.

The recommended way for optimizing RExt is to first choose CL1 and CL2 as explained before, and to connect a potentiometer in the place of RExt. The potentiometer should be initially set to be approximately equal to the capacitive reactance of CL2. It should then be adjusted as required, until an acceptable output and crystal drive level are obtained.

# Caution:

After calculating RExt, it is recommended to recalculate the gain margin (refer to Section 3.4) to make sure that the addition of RExt has no effect on the oscillation condition. The value of RExt must be added to ESR in the expression of 9mcrit, and 9m  9mcrit must also remain true:

![](images/29cc6ecc66c84d170ca51959063ce498fc23c0e9b4dd4c79ac088a939a78027c.jpg)

Note:

If RExt is too low, there is a considerable increase of the power dissipation by the crystal. If, on the other hand, RExt is too high, there is no oscillation.

# 3.6 Startup time

This is the time required by the oscillation to start and then build up, untilit reaches a stable oscillation phase. The startup time depends, among other factors, on the Q-factor of the resonator used. If the oscillator is paired with a quartz-crystal resonator characterized by its high Q-factor, the startup time is higher when ceramic resonators are used (these are known for their poor Q-factor, compared to quartz-crystal resonators). The startup time also depends upon the external components, CL1 and CL2, and on the crystal frequency. The higher the crystal nominal frequency, the lower the startup time. In addition, startup problems usually arise because the gain margin is not properly dimensioned (as explained previously). This is caused either by CL1 and CL2 being too small or too large, or by the ESR being too high.

As an example, an oscillator paired with a few MHz nominal frequency crystal resonator typically starts up after a delay of a few ms.

The startup time of a 32.768 kHz crystal ranges between 1 and 5 s.

# 3.7 Crystal pullability

Crystal pullabilty, also known as crystal sensitivity, measures the impact of small variations of the load capacitance seen by the crystal on the oscillation frequency shifting. This parameter has more importance when dealing with low-speed oscillators, as they are used to clock time-keeping functions (such as real-time clock).

When the final application is stillin the design stage, the influence of this parameter on the low-speed oscillator accuracy (and consequently on allthe time-keeping functions clocked by this oscillator) is not obvious. This is because the designer fine tunes the load capacitors until the desired oscillation frequency is obtained. When the design reaches production stage it is frozen, and all the passive components including the load capacitors have their values well defined. Any change of the load capacitance induces a shift of the oscillation frequency.

Changes in the capacitive load (CL) seen by the crystal can be thought of as due to inadequate operation environment, and only happening when the final design is not properly operated. In practice, this is not true since changes of the load capacitance are rather frequent and must be taken into account by the designer. The main contributors to the capacitive load (CL) seen by the oscillator are

the capacitance of the load capacitors CL1 and CL2 • the stray capacitance of the PCB paths the parasitic capacitance of the oscillator pins.

Any change on the capacitances listed above directly shifts the oscillation frequency. When the design is in production stage, many of these capacitance values cannot be accurately controlled. Selecting a crystal with low pullability limits the influence of such production uncertainties on the final oscillation frequency accuracy.

Generally speaking, the higher the load capacitance of a crystal, the lower its pullability. As an example, let us consider a crystal with a pullability of 45 PPM/pF. To fine-tune the oscillation frequency, this crystal is loaded by two C0G ceramic capacitors (with a ± 5% tolerance of their nominal value), CL1 and CL2, with the same 7 pF capacitance.

From the crystal point of view, the two load capacitors are mounted in series, which means that their contribution to CL is (CL1 = CL2) / 2. The tolerance on their contribution to CL

remains the same, and is equal to ± 5%. If we consider that all the remaining contributors to the C_ are maintained to their nominal values at design stage (to assess the frequency shift magnitude induced only by load capacitor tolerances), then the load capacitance seen by the crystal (CL) either decreases by 0.175 pF, or increases by the same value. This induces an oscillation shift of:

0.175 pF x 45 PPM / pF = \~7.8 PPM (\~0.7 s/day for a time-keeping function such as RTC)

The above example shows that lower pullability results in lower impact of small load capacitance deviation on the frequency shifting. Crystal pullability is an important factor when defining the final application PPM budget.

![](images/2278e54a1a9889f73dbb028bdc28cd993c7b44b30cf7eb18e35868befacb6ee9.jpg)

where

Cm is the crystal motional capacitance (in pF) • Co is the crystal shunt capacitance (in pF) CL is the crystal nominal load capacitance (in pF)

The following sections give a more detailed description on how to calibrate the oscillation frequency, and how to estimate the final accuracy uncertainty (PPM) budget.

# 3.8 Safety factor

# 3.8.1 Definition

Resonators (such as crystal resonators) undergo aging effects that manifest themselves over time in deviations of resonator parameters from the values defined by the specifications. Among the impacted parameters there is the resonator ESR, whose value depends upon the environment conditions, such as moisture and temperature. The oscillator transconductance depends upon the power supply voltage and upon the temperature.

The safety factor parameter enables to determine the oscillator safe operation under the operating conditions and during the application life. It measures the ability of the oscillator not to fail under operating conditions.

The safety factor is defined as the ratio between the oscillator negative resistance and its ESR:

![](images/237b06a0b8ff401fe206959237fdafef114f291307bdde72a615365f3e034065.jpg)

# 3.8.2 Measurement methodology

To measure the oscillator negative resistance, a resistance is added in series to the resonator, as indicated in Figure 8.

![](images/e4c2d0ccf887940f1a19e83e04b56fbe81af1313edfa552056a8d79c1c8953bd.jpg)  
Figure 8. Negative resistance measurement methodology description

MSv37268V1

T preventing the oscillator from starting up successfully.

In practice, this value is set by conducting a series of experiments in which the value of the series resistance is slightly increased compared to the previous experiment. The sequence stops when the oscillator is unable to start correctly. The oscillator negative resistance is equal to the value of the added series resistance.

# .8.3 Safety factor for STM32 and STM8 oscillators

Table 4 summarizes the safety factor (Sf) for oscillators embedded in STM32 and STM8 devices. For the LSE oscillator, the oscillation is considered safe for Sf ≥ 3, while for the HSE oscillator this is true when Sf ≥ 5.

Table 4. Safety factor (Sf) for STM32 and STM8 oscillators(1)   

<table><tr><td rowspan=2 colspan=1>Safety factor (Sf)</td><td rowspan=1 colspan=2>Assurance level</td></tr><tr><td rowspan=1 colspan=1>HSE</td><td rowspan=1 colspan=1>LSE</td></tr><tr><td rowspan=1 colspan=1>Sf ≥ 5</td><td rowspan=1 colspan=1>Safe</td><td rowspan=1 colspan=1>Very safe</td></tr><tr><td rowspan=1 colspan=1>3≤Sf&lt;5</td><td rowspan=2 colspan=1>Not safe</td><td rowspan=1 colspan=1>Safe</td></tr><tr><td rowspan=1 colspan=1>$Sf&lt;3</td><td rowspan=1 colspan=1>Not safe</td></tr></table>

.Safe and very safe oscilations are shown in green, unsafe oscillation in yellow

# 3.9 Oscillation modes

# 3.9.1 What are fundamental and overtone modes?

Equation (4) gives the oscillation frequency Fp of a crystal, which depends on the series resonant frequency Fs for which the crystal impedance is null. The oscillator is said to operate in fundamental mode when vibrating around Fp.

Fs (and hence Fp) depend upon the parameters of the crystal theoretical model illustrated in Figure 1. These parameters, given by the crystal manufacturer, define the frequency for which the crystal is designed to oscillate around the fundamental frequency.

In real life, an AT-cut quartz crystal impedance reaches a zero value for several frequencies, which correspond to the odd multiples of its fundamental vibration frequency. A crystal can also vibrate around one of those odd multiples, these are the overtone oscillation modes. Figure 9 represents the cancellation of an AT-cut crystal impedance for the fundamental frequency, its following odd multiples (third and fifth overtones are represented), as well as some spurious frequencies.

![](images/03bbf46144ac7ba414b9ee3385f5443ffa8a1aea3ba5e5ae3dbcc6ac248e210a.jpg)  
Figure 9. Fundamental and overtone frequencies of an AT-cut quartz crystal

Note:

AT-cut quartz corresponds to most of the crystals to use with HSE. For LSE, tuning fork crystals can be used, but they do not show the same oscillation mode possibilities (Figure 9 is not valid for them). In this part, we consider an AT-cut quartz crystal when referring to a crystal.

This multiple-time cancellation is because a more accurate quartz crystal theoretical model shows an RLC branch for each one of its overtone modes, as illustrated in Figure 10.

![](images/8a984a6fd9297cc0d6b75d454f4d3528ba5ebf8ab0a8c99f22bf6660c79861b6.jpg)  
Figure 10. Quartz crystal theoretical model with third overtone

For example, it is possible to use the third overtone mode by implementing the oscillator as shown in Figure 11, to suppress the fundamental frequency (theoretically each overtone mode can be selected by suppressing the previous ones).

![](images/3aaaeac9f7f8f80654cb41958e4b3b492fb2bc85680f49b7c21fd3d24e3eb827.jpg)  
Figure 11. Oscillator implementation for third overtone

# 3.9.2 Third overtone mode: pros and cons

Because of the thickness, the crystals designed for a high frequency fundamental mode are very expensive, requiring high-end cutting technologies and a lot of caution for implementation. Practically, it becomes impossible to operate in fundamental mode for a frequency above 50 MHz. This is why most of the high frequency crystals are designed to work in the third overtone mode it is possible to cut the crystal for a frequency three times lower than the one it oscillates at).

The model for a crystal operating in third overtone mode (Figure1) shows a resistance Rm approximately three times higher and a capacitance Cm nine times lower than those associated with the fundamental mode.

For the third overtone mode, these differences mean a higher Q-factor since the quality factor for an RC series circuit is 1 / wRC (less energy loss, more stable performances, better jitter, and lower pullability, see Section 3.7). A lower pullability means a lower frequency shift when the application is deployed in the field, at the expense of lower tunability of the oscillation frequency.

# 3.9.3 Considerations for crystals interfaced with STM32 products

The oscillators integrated in the STM32 products have been validated for use in the fundamental mode, respecting the implementation of Figure 5. If a third overtone crystal is used with this implementation, the theory indicates that it does not start vibrating at the third harmonic frequency, but at the fundamental one.

# Note:

The startup mode of an oscillator can even involuntarily balance between the two modes if its external components have not been chosen according to what indicated in this document.

# Guidelines to select a suitable crystal and external components

# 4.1 Low-speed oscillators embedded in STM32 MCUs/MPUs

The low-speed resonator market provides a wide range of crystal resonators. Selecting the most adequate one for a given design depends on many parameters. The most important parameters to be taken into account (only technical factors are listed) are:

Crystal size or footprint   
• Crystal load capacitance (CL)   
• Oscillation frequency offset (PPM) Startup time

A trade-off between the above parameters must be found, depending on the key design criteria. Figure 12 shows that the resonators available on the market can be divided into two categories, depending upon the above-mentioned factors and trade-offs.

![](images/b4e0a7b819d813d007533832c18eae143348079f440529a2db0f8f4735f6a16a.jpg)  
Figure 12. Classification of low-speed crystal resonators

MSv36189V3

A resonator with a relatively high load-capacitance (such as 12.5 pF) requires more power for the oscillator to drive the oscillation loop at the resonator nominal frequency. Designs targeting low power consumption (for example, RTC application powered by coin-batteries requiring very long autonomy) are consequently more likely to use resonators with relatively small load capacitance. On the other side, big load capacitance resonators have a much smaller pullabilty compared to resonators with small load capacitance. As a result, designs without severe constraints on power consumption tend to use big load capacitance crystals to reduce pullability.

One of the key areas where crystal resonators are massively used is the hand-held and wearable appliance consumer market (such as smartphones, Bluetooth® kits). For this market segment, the crystal size is of critical importance. However, it is widely known that small-footprint crystals come with high crystal ESR. The choice may be harder if the target design has severe constraints in terms of power consumption (the usual scenario). In this case, choose a crystal with a load capacitance as small as possible to optimize power consumption even if this compromises pullabilty. In addition, crystals with high ESR may have a slightly longer startup time. If there are no constraints on crystal size, then it is recommended to choose a crystal with the smallest possible ESR.

In noisy environments (almost always the case for industrial applications), if there are no constraints on power consumption, it is recommended to choose crystals with high load capacitance. These crystals require a high-drive current from the oscillator, but are more robust against noise and external perturbations. Another advantage is that the design pullability is minimized.

Depending on the device used, all the resonator families listed below can be compatible with your design, or only some of them. STM32 devices embed two types of low-speed oscillator (LSE):

Constant gain This type of LSE oscillator features a constant gain, which makes them compatible only with a few crystal groups mentioned above. For example, LSE oscillators embedded in STM32F2 and STM32L1 MCUs target designs with severe power consumption constraints. The selected crystal should consequently have a low load capacitance and a moderate ESR. LSE oscillators embedded in STM32F1 MCUs target crystal resonators with moderate ESR and moderate load capacitance.

Configurable gain

The main advantage of LSE oscillators belonging to this family is the compatibility with a large number of crystals. Almost no constraint comes by the device embedding this kind of oscillator. The large list of compatible resonator crystals allows the designer to focus on design constraints (such as power consumption, footprint) when selecting a compatible resonator. These oscillators are divided into two categories:

Dynamically (on-the-fly) modifiable gain LSE oscillators   
The gain of this type of LSE oscillators can be changed either before starting the oscillator or after enabling it.   
Statically modifiable gain LSE oscillators   
The gain can be changed only when the LSE oscillator is turned off. If the oscillator transconductance has to be increased or decreased, the LSE must be turned off first.

Table 5 gives the list of low-speed oscillators (LSE) embedded in STM32 devices.

# Caution:

When the gain is modified statically or on-the-fly, the calibration of the oscillation frequency must be readjusted to estimate the final accuracy uncertainty (PPM) budget.

# Caution:

In STM32F0 and STM32F3 MCUs, High drive mode (9m = 25 µA/V) must be used only with 12.5 pF crystals, to avoid saturating the oscillation loop and causing a startup failure. When used with a low C_ crystal (for example 6 pF), the oscillation frequency jitters and duty cycle can be distorted.

Table 5. LSE oscillators embedded into STM32 MCUs/MPUs(1)   

<table><tr><td rowspan=1 colspan=1>Series</td><td rowspan=1 colspan=1>Drive level</td><td rowspan=1 colspan=1>gm (min)</td><td rowspan=1 colspan=1>Gm_crit_max</td><td rowspan=1 colspan=1>Unit</td></tr><tr><td rowspan=2 colspan=1>CO</td><td rowspan=1 colspan=1>Medium high</td><td rowspan=1 colspan=1>8.5</td><td rowspan=1 colspan=1>1.7</td><td rowspan=6 colspan=1>μA/V</td></tr><tr><td rowspan=1 colspan=1>High</td><td rowspan=1 colspan=1>13.5</td><td rowspan=1 colspan=1>2.7</td></tr><tr><td rowspan=4 colspan=1>F0,F3</td><td rowspan=1 colspan=1>Low</td><td rowspan=1 colspan=1>5</td><td rowspan=1 colspan=1>1.0</td></tr><tr><td rowspan=1 colspan=1>Medium low</td><td rowspan=1 colspan=1>8</td><td rowspan=1 colspan=1>1.6</td></tr><tr><td rowspan=1 colspan=1>Medium high</td><td rowspan=1 colspan=1>15</td><td rowspan=1 colspan=1>3</td></tr><tr><td rowspan=1 colspan=1>High</td><td rowspan=1 colspan=1>25</td><td rowspan=1 colspan=1>5</td></tr><tr><td rowspan=1 colspan=1>F1,T</td><td rowspan=2 colspan=1>Not available</td><td rowspan=1 colspan=1>5</td><td rowspan=1 colspan=1>1</td><td rowspan=2 colspan=1>μA/V</td></tr><tr><td rowspan=1 colspan=1>F2, F4_g1(2)</td><td rowspan=1 colspan=1>2.8</td><td rowspan=1 colspan=1>0.56</td></tr><tr><td rowspan=2 colspan=1>F4_g2(3)</td><td rowspan=1 colspan=1>Low</td><td rowspan=1 colspan=1>2.8</td><td rowspan=1 colspan=1>0.56</td><td rowspan=2 colspan=1>μA/V</td></tr><tr><td rowspan=1 colspan=1>High</td><td rowspan=1 colspan=1>7.5</td><td rowspan=1 colspan=1>1.5</td></tr><tr><td rowspan=4 colspan=1>F7</td><td rowspan=1 colspan=1>Low</td><td rowspan=1 colspan=1>2.4</td><td rowspan=1 colspan=1>0.48</td><td rowspan=4 colspan=1>μA/V</td></tr><tr><td rowspan=1 colspan=1>Medium low</td><td rowspan=1 colspan=1>3.75</td><td rowspan=1 colspan=1>0.75</td></tr><tr><td rowspan=1 colspan=1>Medium high</td><td rowspan=1 colspan=1>8.5</td><td rowspan=1 colspan=1>1.7</td></tr><tr><td rowspan=1 colspan=1>High</td><td rowspan=1 colspan=1>13.5</td><td rowspan=1 colspan=1>2.7</td></tr><tr><td rowspan=1 colspan=1>L1</td><td rowspan=1 colspan=1>Not available</td><td rowspan=1 colspan=1>3</td><td rowspan=1 colspan=1>0.6</td><td rowspan=1 colspan=1>μA/V</td></tr><tr><td rowspan=4 colspan=1>GO, G4H7L0, L4,L4+,L5MP1,MP2N6UO, U3, U5(4)WB, WBO, WBA(5), WL</td><td rowspan=1 colspan=1>Low</td><td rowspan=1 colspan=1>2.5</td><td rowspan=1 colspan=1>0.5</td><td rowspan=7 colspan=1>μA/V</td></tr><tr><td rowspan=1 colspan=1>Medium low</td><td rowspan=1 colspan=1>3.75</td><td rowspan=1 colspan=1>0.75</td></tr><tr><td rowspan=1 colspan=1>Medium high</td><td rowspan=1 colspan=1>8.5</td><td rowspan=1 colspan=1>1.7</td></tr><tr><td rowspan=1 colspan=1>High</td><td rowspan=1 colspan=1>13.5</td><td rowspan=1 colspan=1>2.7</td></tr><tr><td rowspan=3 colspan=1>H5</td><td rowspan=1 colspan=1>Medium low</td><td rowspan=1 colspan=1>3.75</td><td rowspan=1 colspan=1>0.75</td></tr><tr><td rowspan=1 colspan=1>Medium high</td><td rowspan=1 colspan=1>8.5</td><td rowspan=1 colspan=1>1.7</td></tr><tr><td rowspan=1 colspan=1>High</td><td rowspan=1 colspan=1>13.5</td><td rowspan=1 colspan=1>2.7</td></tr></table>

Color code: Light blue: LSE oscillators with transconductance modifiable on the fly (dynamically) Yelo  lto th non-odblaon - Gray: LSE oscillators with statically-modifiable transconductance 2. STM32F4 series with LSE generation 1 (STM32F401/405/407/415/417/427/429/437/439xx MCUs featuring LSE oscillators with non modifiable transconductance). 3. STM32F4 series with LSE generation 2 (STM32F410/411/412/413/423/446/469/479xx MCUs featuring LSE oscillators with statically modifiable transconductance). 4. STM32U575/585 rev. X devices do not support low drive mode. 5STM32WBA devices do not support low drive mode.

# 4.2 How to select an STM32-compatible crystal

This section describes the procedure recommended to select suitable crystal/external components. The procedure is based on the following steps:

# Step 0: Choose a fundamental mode designed resonator

Choose a fundamental mode designed resonator (as explained in Section 3.9, the STM32 oscillators are validated to work with resonator vibrating in fundamental mode and while using the Pierce oscillator circuitry presented in Figure 5), and make sure that the resonator chosen is designed to work in fundamental mode.

# Step 1: Check the resonator compatibility with the selected STM32

To check the compatibility between the selected crystal and the STM32 MCU/MPU, first identify the procedure to follow among the two described in Section 3.4. The decision must be made based on the oscillator specification provided in the datasheet.

If the oscillator transconductance parameter is specified, then apply the second procedure. Ensure that the gain margin ratio is higher than five (x5) to make sure that the crystal is compatible with the selected STM32 part.   
If Gmrta e inste ake ure hat r he latn lo smaller than the specified Gm_crit_max value.

#

To determine the correct capacitance values for CL1 and CL2 load capacitors, apply the formula specified in Section 3.3. The values obtained are approximations of the exact capacitances to be used. In a second phase, to fine-tune the values of the load capacitors, go through a series of experimental iterations, until the right capacitance values are found.

During the experimental phase, use a standard crystal, one whose PPM drift is well known when it is loaded by the crystal nominal load capacitance (CL). This kind of crystal can be provided by the manufacturer upon request. After this crystal has been chosen, calculate its oscillation frequency (Fstandard) when the crystal is loaded by its nominal load capacitance. This frequency is given by the formula:

![](images/c5ad2d2724b80032f960310680c2dea2ebfb67943b8e8c80cf8715990936319e.jpg)

# where:

Fstandard is the standard crystal oscillation frequency when it is loaded by its nominal load capacitance • Fnominal is the oscillation nominal frequency specified in the crystal datasheet Pnarecillat euenc i esanar   az the crystal manufacturer

When Fstandard is computed, go through the following sequence:

Make the first experimental iteration with CL1 and CL2 capacitance values determined by calculation:

I te oition equency is qual  andard an  he capacitances. The user can therefore skip substeps 2 and 3. If the oscillation frequency is slower than Fstandard go to substep 2, otherwise execute substep 3.

2. For this experimental iteration, decrease CL1 and CL2 capacitance values, measure

If the oscillation frequency is slower than Fsandard, execute substep 2, otherwise execute substep 3.   
If the oscillation frequency is almost equal to Fstandard, use the latter CL1 and CL capacitance values.

3.For this experimental iteration, increase CL1 and CL2 capacitance values, measure again the siaion equency a compar

If the oscillation frequency is slower than Fstandard, execute substep 2, otherwie execute substep 3.   
If the oscillation frequency is almost equal to Fstandard, use the latter CL1 and CL2 capacitance values.

# Step 3: Check the safety factor of the oscillation loop

The safety factor must be assessed as described in Section 3.8 to ensure a safe oscillation of the oscillator under operating conditions.

Many crystal manufacturers can check device/crystal pairing compatibility upon request. If the pairing is judged valid, they can provide a report including the recommended CL1 and CL2 values, as well as the oscillator negative resistance measurement. In this case steps 2 and 3 can be skipped.

# Step 4: Calculate the drive level and external resistor

Compute the drive level (DL) (see Section 3.5) and check if it is greater or lower than DLcrystal

If DL < DLcrystal, no need for an external resistor (a suitable crystal has been found). e then recalculate the gain margin taking RExt into account. If gain margin > 5, a suitable crystal has been found. If not, then this crystal does not work, another one must be chosen. Return to Step 1: Check the resonator compatibility with the selected STM32 to run the procedure for the new crystal.

# Step 5 (optional): Calculate the PPM accuracy budget

Use the following formula to estimate the PPM accuracy budget for the application:

![](images/9fad663609b4764d629fb1a8b47c6f35e81a213185e101e772a69316e61a57fe.jpg)

where:

PPMBudget is the estimated accuracy for the oscillation frequency PPMcrystal is the crystal PPM accuracy specifed in the datasheet

Deviation (L) is expressed in F. It measures the deviation of the load capacitance CL) due to tolerances on load capacitor values and the variation of the stray capacitance (Cs) due to PCB manufacturing process deviation.

Pullabilty is expressed in PPM / pF (refer to Section 3.7).

# Note:

The PPM budget calculated above does not take into account the temperature variation, which can make the PPM budget bigger.

# Recommended resonators for STM32 MCUs/MPUs

# 5.1 STM32-compatible high-speed resonators

The high-speed oscillator (HSE) embedded into STM32 products(a) is compatible with almost all the resonators available on the market. The recommended resonators are provided by a wide range of manufacturers, including:

• ABRACON   
• ECS (www.ecsxtal.com)   
• EPSON (http://www5.epsondevice.com)   
• KYOCERA   
• Micro Crystal   
• muRata (www.murata.com)   
• NDK (http://www.ndk.com) RIVER (http://www.river-ele.co.jp)

Several tools are available to select the more recent and high-demand crystals, among them the STM32 Crystal Selection Tool from ECS, and the IC Matching Information provided by NDK.

Compatible resonators come with various frequencies and technologies (ceramic resonators and quartz-crystal resonators working in fundamental mode are all compatible with the HSE oscillator embedded in STM32 MCUs/MPUs). Table 6 summarizes the supported frequency ranges.

Table 6. HSE oscillators embedded in STM32 MCUs/MPUs   

<table><tr><td rowspan=1 colspan=1>Series</td><td rowspan=1 colspan=1>F3</td><td rowspan=1 colspan=1>F1T</td><td rowspan=1 colspan=1>F2</td><td rowspan=1 colspan=1>F4</td><td rowspan=1 colspan=1>F7</td><td rowspan=1 colspan=1>LO</td><td rowspan=1 colspan=1>L1</td><td rowspan=1 colspan=1>COL4, L4+L5H7G0, G4MP1UO</td><td rowspan=1 colspan=1>H5U3U5</td><td rowspan=1 colspan=1>MP2</td><td rowspan=1 colspan=1>N6</td><td rowspan=1 colspan=1>Unit</td></tr><tr><td rowspan=1 colspan=1>Frequencyrange</td><td rowspan=1 colspan=1>4 -32</td><td rowspan=1 colspan=1>4 - 16</td><td rowspan=1 colspan=1>4 - 25</td><td rowspan=1 colspan=1>4 - 26</td><td rowspan=1 colspan=1>4 - 26</td><td rowspan=1 colspan=1>1 - 25</td><td rowspan=1 colspan=1>1 - 24</td><td rowspan=1 colspan=1>4 - 48</td><td rowspan=1 colspan=1>4 - 50</td><td rowspan=1 colspan=1>16 - 48</td><td rowspan=1 colspan=1>16 - 48</td><td rowspan=1 colspan=1>MHz</td></tr><tr><td rowspan=1 colspan=1>9m (min)</td><td rowspan=1 colspan=1>10</td><td rowspan=1 colspan=1>25</td><td rowspan=1 colspan=1>5</td><td rowspan=1 colspan=1>5</td><td rowspan=1 colspan=1>5</td><td rowspan=1 colspan=1>3.5</td><td rowspan=1 colspan=1>3.5</td><td rowspan=1 colspan=1>7.5</td><td rowspan=1 colspan=1>7.5</td><td rowspan=1 colspan=1>12.5</td><td rowspan=1 colspan=1>9.57</td><td rowspan=2 colspan=1>mA/V</td></tr><tr><td rowspan=1 colspan=1>Gm_crit_max</td><td rowspan=1 colspan=1>2</td><td rowspan=1 colspan=1>5</td><td rowspan=1 colspan=1>1</td><td rowspan=1 colspan=1>1</td><td rowspan=1 colspan=1>1</td><td rowspan=1 colspan=1>0.7</td><td rowspan=1 colspan=1>0.7</td><td rowspan=1 colspan=1>1.5</td><td rowspan=1 colspan=1>1.5</td><td rowspan=1 colspan=1>2.5</td><td rowspan=1 colspan=1>1.95</td></tr></table>

# 5.2 STM32-compatible low-speed resonators

Table 7 contains a not exhaustive list (only the compatible resonator part numbers checked by ST are included) of low-speed quartz-crystal 32.768 kHz resonators that are either compatible with the whole STM32 portfolio, or with a subset.

Different footprints are provided to facilitate crystal selection, even if there are geometric constraints for the final application.

Table 7. Recommended crystal / MEMS resonators for the LSE oscillator in STM32 products   
20   

<table><tr><td></td><td rowspan=1 colspan=1>Packagesize</td><td rowspan=1 colspan=1>Manufacturer</td><td rowspan=1 colspan=1>Quartz referencePart number</td><td rowspan=1 colspan=1>ESR(ka)</td><td rowspan=1 colspan=1>CGR) )</td><td rowspan=1 colspan=1>(CF) )</td><td rowspan=1 colspan=1> </td><td rowspan=1 colspan=1>STM32 series compatibility()(3)</td></tr><tr><td rowspan=20 colspan=2>12x10</td><td rowspan=4 colspan=1>RIVER</td><td rowspan=4 colspan=1>TFX-05X</td><td rowspan=4 colspan=1>90</td><td rowspan=4 colspan=1>1.5</td><td rowspan=1 colspan=1>5</td><td rowspan=1 colspan=1>0.6447</td><td rowspan=1 colspan=1>C F0 F, F3 F4g2, L0, L, L4+, L5, G0, G4, F7, H5, H7, N6, WB, WB, WBA, WL, MP1, MP, U0, U3 U5</td></tr><tr><td rowspan=1 colspan=1>7</td><td rowspan=1 colspan=1>1.1026</td><td rowspan=1 colspan=1>C, F0, F3, F4_g2, L0, L4, L4+, L5, G0, G4, F7, H5, H7, N6, WB, WB, WBA, WL, MP1, MP2, U0, U3, U5</td></tr><tr><td rowspan=1 colspan=1>9</td><td rowspan=1 colspan=1>1.6824</td><td rowspan=1 colspan=1>C0, F0, F3, L0, L4, L4+, L5, G0, G4, F7, H5, H7, N6, WB, WB0, WBA, WL, MP1, MP2, U0, U3, U5</td></tr><tr><td rowspan=1 colspan=1>12.5</td><td rowspan=1 colspan=1>2.9910</td><td rowspan=1 colspan=1>F0, F3</td></tr><tr><td rowspan=4 colspan=1>SlI</td><td rowspan=4 colspan=1>SC-12S (2 terminals)</td><td rowspan=4 colspan=1>90</td><td rowspan=4 colspan=1>1.4</td><td rowspan=1 colspan=1>6</td><td rowspan=1 colspan=1>0.8356</td><td rowspan=1 colspan=1>C F0, F1, F3, F4_g2, L0, L4, L4+, L5, G0, G4, F7, H5, H7, N6, WB, WB, WBA, WL, MP1, MP2, U0, U3, U5</td></tr><tr><td rowspan=1 colspan=1>7</td><td rowspan=1 colspan=1>1.0768</td><td rowspan=1 colspan=1>C, F0, F3, F4_g2, L0, L4, L4+, L5, G0, G4, F7, H5, H7, N6, WB, WB, WBA, WL, MP1, MP2, U0, U3, U5</td></tr><tr><td rowspan=1 colspan=1>9</td><td rowspan=1 colspan=1>1.6506</td><td rowspan=1 colspan=1>C F F3, L0, L, L4+ L, G0, G4, F7, H5, H7, N6, WB, WB, WBA, WL, MP1, MP2, U0, U3, U5</td></tr><tr><td rowspan=1 colspan=1>12.5</td><td rowspan=1 colspan=1>2.9484</td><td rowspan=1 colspan=1>F0, F3</td></tr><tr><td rowspan=8 colspan=1>ECS</td><td rowspan=1 colspan=1>ECS-.327-6-1210-TR</td><td rowspan=4 colspan=1>90</td><td rowspan=4 colspan=1>1.1</td><td rowspan=1 colspan=1>6</td><td rowspan=1 colspan=1>0.7692</td><td rowspan=1 colspan=1>C, F0, F1, F3, F4_g2, L0, L4, L4+, L5, G0, G4, F7, H5, H7, N6, WB, WB0, WBA, WL, MP1, MP2, U0, U3, U5</td></tr><tr><td rowspan=1 colspan=1>ECS-.327-7-1210-TR</td><td rowspan=1 colspan=1>7</td><td rowspan=1 colspan=1>1.0012</td><td rowspan=1 colspan=1>C F0 F3, F4g2, L0, L, L4 L5, G0, G4, F7, H5, H7, N6, WB, WB, WBA, WL, MP, MP2, U0, U3, U5</td></tr><tr><td rowspan=1 colspan=1>ECS-.327-9-1210-TR</td><td rowspan=1 colspan=1>9</td><td rowspan=1 colspan=1>1.5567</td><td rowspan=1 colspan=1>C, F0, F3, L0, L4, L4+ L5, G0, G4, F7, H5, H7, N6, WB, WB, WBA, WL, MP1, MP2, U0, U3, U5</td></tr><tr><td rowspan=1 colspan=1>ECS-.327-12.5-1210-TR</td><td rowspan=1 colspan=1>12.5</td><td rowspan=1 colspan=1>2.8225</td><td rowspan=1 colspan=1>FO, F3</td></tr><tr><td rowspan=1 colspan=1>ECS-.327-5-1210B-N-TR</td><td rowspan=4 colspan=1>80</td><td rowspan=4 colspan=1>1.5</td><td rowspan=1 colspan=1>5</td><td rowspan=1 colspan=1>0.5731</td><td rowspan=1 colspan=1>C, F0, F1, F3, F4_g2, L0, L4, L4+, L5, G0, G4, F7, H5, H7, N6, WB, WB0, WBA, WL, MP1, MP2, U0, U3, U5</td></tr><tr><td rowspan=1 colspan=1>ECS-.327-7-1210B-N-TR</td><td rowspan=1 colspan=1>7</td><td rowspan=1 colspan=1>0.9800</td><td rowspan=1 colspan=1>C, F0, F1, F3, F4_g2, L0, L4, L4+, L5, G0, G4, F7, H5, H7, N6, WB, WB0, WBA, WL, MP1, MP2, U0, U3, U5</td></tr><tr><td rowspan=1 colspan=1>ECS-.327-9-1210B-N-TR</td><td rowspan=1 colspan=1>9</td><td rowspan=1 colspan=1>1.4955</td><td rowspan=1 colspan=1>C0, F0, F3, F4_g2, L0, L4, L4+, L5, G0, G4, F7, H5, H7, N6, WB, WB0, WBA, WL, MP1, MP2, U0, U3, U5</td></tr><tr><td rowspan=1 colspan=1>ECS-.327-12.5-1210B-N-TR</td><td rowspan=1 colspan=1>12.5</td><td rowspan=1 colspan=1>2.6587</td><td rowspan=1 colspan=1>C0, F0, F3, L0, L4, L4+, L5, G0, G4, F7, H5, H7, N6, WB, WB0, WBA, WL, MP1, MP2, U0, U3, U5</td></tr><tr><td rowspan=4 colspan=1>ABRACON</td><td rowspan=1 colspan=1>ABS04W-32.768 KHz 4 pF</td><td rowspan=4 colspan=1>80</td><td rowspan=4 colspan=1>1.5</td><td rowspan=1 colspan=1>4</td><td rowspan=1 colspan=1>0.4103</td><td rowspan=1 colspan=1>C, F0,F1, F2, F3, F4, L0, L1, L4, L4+, L5, G0, G4, F7, H5, H7, N6, WB, WB, WBA, WL, MP1, MP2, U0, U3, U5</td></tr><tr><td rowspan=1 colspan=1>ABS04W-32.768 KHz 6 pF</td><td rowspan=1 colspan=1>6</td><td rowspan=1 colspan=1>0.7630</td><td rowspan=1 colspan=1>C, F0, F1, F3, F4_g2, L0, L4, L4+, L5, G0, G4, F7, H5, H7, N6, WB, WB0, WBA, WL, MP1, MP2, U0, U3, U5</td></tr><tr><td rowspan=1 colspan=1>ABS04W-32.768 KHz 9 pF</td><td rowspan=1 colspan=1>9</td><td rowspan=1 colspan=1>1.4955</td><td rowspan=1 colspan=1>CF F, F4g2 L0, L, L4 L5, G0, G4, F7, H5 H7, N6, WB, WB, WBA, WL, MP, MP, UO, U, U5</td></tr><tr><td rowspan=1 colspan=1>ABS04W-32.768 KHz 12.5 pF</td><td rowspan=1 colspan=1>12.5</td><td rowspan=1 colspan=1>2.6587</td><td rowspan=1 colspan=1>F, F3, L0, L, L4+, L5, G,G, F7,H5, H, N6, WB, WB, WBA, WL, MP1, MP, U0, U3, U5</td></tr></table>

00   
Table 7. Recommended crystal / MEMS resonators for the LSE oscillator in STM32 products (continued)   
20   

<table><tr><td rowspan=25 colspan=2>Packagessize20 1.×10M</td><td rowspan=1 colspan=1>Packagessize</td><td rowspan=1 colspan=1>Manufacturer</td><td rowspan=1 colspan=5>Quartz referenceart number</td><td rowspan=1 colspan=1>ESR(ka</td><td rowspan=1 colspan=1>(OF </td></tr><tr><td rowspan=5 colspan=1>Micro Crystal</td><td rowspan=5 colspan=2>CM9V-T1A / CM9V-T1A 0.3</td><td rowspan=5 colspan=1></td><td rowspan=5 colspan=1>1.4</td><td rowspan=1 colspan=1>4</td><td rowspan=1 colspan=1>0.4449</td><td rowspan=1 colspan=1>F F F F,LL L L+L G0G,FH H7 N6WB, WB WBA WL MP MP U0UU</td><td></td></tr><tr><td rowspan=1 colspan=1>6</td><td rowspan=1 colspan=1>0.8356</td><td rowspan=1 colspan=1>C0, F0, F1, F3, F4_g2, L0, L4, L4+,L5, G0, G4, F7, H5, H7, N6, WB, WB0, WBA, WL, MP1, MP2, U0, U3, U5</td><td></td></tr><tr><td rowspan=1 colspan=1>7</td><td rowspan=1 colspan=1>1.0768</td><td rowspan=1 colspan=1>C F0, F3, F4_g2, L0, L4, L4+,L5, G0, G4, F7, H5, H7, N6, WB, WB, WBA, WL, MP1, MP2, U0, U3, U5</td><td rowspan=1 colspan=1></td></tr><tr><td rowspan=1 colspan=1>9</td><td rowspan=1 colspan=1>1.6506</td><td rowspan=1 colspan=1>F3, L, L, L4+,L,GG, F, H5, H7, N6, WB, WB, WBA, WL, MP, MP, U0U3U5</td><td rowspan=1 colspan=1></td></tr><tr><td rowspan=1 colspan=1>12.5</td><td rowspan=1 colspan=1>2.9484</td><td rowspan=1 colspan=1>FO, F3</td><td rowspan=1 colspan=1></td></tr><tr><td rowspan=4 colspan=1>ECS</td><td rowspan=1 colspan=2>ECS-.327-6-16-TR3</td><td rowspan=4 colspan=1>90</td><td rowspan=4 colspan=1>1.3</td><td rowspan=1 colspan=1>6</td><td rowspan=1 colspan=1>0.8132</td><td rowspan=1 colspan=1>CF0F1, F3, F4g2, L0 L, L4+L5, G0, G4,F7, H5,H7, N6, WB, WB, WBA,WL, MP1, MP2, U0, U3, U5</td><td rowspan=1 colspan=1></td></tr><tr><td rowspan=1 colspan=2>ECS-.327-7-16-C-TR</td><td rowspan=1 colspan=1>7</td><td rowspan=1 colspan=1>1.0513</td><td rowspan=1 colspan=1>CF0F1, F3, F4g2, L0, L, L4+L5, G0, G4, F7, H5, H7, N6, WB, WB, WBA, WL, MP1, MP2, U0,U3, U5</td><td rowspan=1 colspan=1></td></tr><tr><td rowspan=1 colspan=2>ECS-.327-9-16-TR</td><td rowspan=1 colspan=1>9</td><td rowspan=1 colspan=1>1.6190</td><td rowspan=1 colspan=1>C F0 F3, L0, L4, L4+,L5, G0, G4, F7, H5, H7, N6, WB, WB, WBA, WL, MP1, MP, U0, U3, U5</td><td rowspan=1 colspan=1></td></tr><tr><td rowspan=1 colspan=2>ECS-.327-12.5-16-TR</td><td rowspan=1 colspan=1></td><td rowspan=1 colspan=1>12.5</td><td rowspan=1 colspan=1>2.9062</td><td rowspan=1 colspan=1>FO, F3</td><td rowspan=1 colspan=1></td></tr><tr><td rowspan=7 colspan=1>NDK</td><td rowspan=2 colspan=2>NX1610SA 32.768 kHzEXS00A-MU00658</td><td rowspan=3 colspan=1></td><td rowspan=3 colspan=1>1.3</td><td rowspan=2 colspan=1>6</td><td rowspan=2 colspan=1>0.8132</td><td rowspan=2 colspan=1>CF0F1, F3, F4g2, L0 L, L4+L5, G0, G4,F7, H5,H7, N6, WB, WB, WBA,WL, MP1, MP2, U0, U3, U5</td><td rowspan=2 colspan=1></td></tr><tr></tr><tr><td rowspan=1 colspan=2>NX1610SA 32.768 kHz EXS00A-U01367</td><td rowspan=1 colspan=1>12.5</td><td rowspan=1 colspan=1>2.9062</td><td rowspan=1 colspan=1>FO, F3</td><td rowspan=1 colspan=1></td></tr><tr><td rowspan=1 colspan=2>NX1610SE 32.768 kHz EXS00A-MU01501</td><td rowspan=4 colspan=1>60(4)</td><td rowspan=4 colspan=1>1.55</td><td rowspan=1 colspan=1>6</td><td rowspan=1 colspan=1>0.5799</td><td rowspan=1 colspan=1>C F, F1,F2 F3, F4, L, L1, L, L4+, L5, G0 G4,F7H5, H7, N6, WB, WB, WBA, WL, MP1, MP2, U0, U3, U5</td><td></td></tr><tr><td rowspan=1 colspan=2>NX1610SE 32.768 kHz EXS00A-U01500</td><td rowspan=1 colspan=1>7</td><td rowspan=1 colspan=1>0.7437</td><td rowspan=1 colspan=1>C, F0, F1, F3, F4_g2, L0, L4, L4+ L5, G0,G, F7, H5, H7, N6, WB, WB, WBA, WL, MP1, MP2, U0, U3 U5</td><td></td></tr><tr><td rowspan=1 colspan=2>NX1610SE 32.768 kHz EXS00A- MU01499</td><td rowspan=1 colspan=1>9</td><td rowspan=1 colspan=1>1.1323</td><td rowspan=1 colspan=1>C, F0, F3 F4g2, L0, L4, L4+, L5, G0, G4, F7, H5, H7, N6, WB, WB, WBA, WL, MP, MP2, U0, U3,U5</td><td></td></tr><tr><td rowspan=1 colspan=2>NX1610SE 32.768 kHz EXS00A-MU01498</td><td rowspan=1 colspan=1>12.5</td><td rowspan=1 colspan=1>2.0083</td><td rowspan=1 colspan=1>C F, F3 L0, L, L4+ L5, G0, G4, F7, H5, H7, N6, WB, WB, WBA, WL, MP1, MP2, U0, U, U5</td><td></td></tr><tr><td rowspan=2 colspan=1>SII</td><td rowspan=2 colspan=2>SC-16S</td><td rowspan=8 colspan=2>90  1.2</td><td rowspan=1 colspan=1>6</td><td rowspan=1 colspan=1>0.7910</td><td rowspan=1 colspan=1>F, F3 F4 L0 L, L+L G0GF7, H5H7, N6 WB,WB, WBAWL, MP, MP U0,U U</td><td></td></tr><tr><td rowspan=1 colspan=1>12.5</td><td rowspan=1 colspan=1>2.8642</td><td rowspan=1 colspan=1>FO, F3</td><td></td></tr><tr><td rowspan=2 colspan=1>EPSON</td><td rowspan=1 colspan=2>FC1610AN 32.768000 kHz 9</td><td rowspan=1 colspan=1>9</td><td rowspan=1 colspan=1>1.5877</td><td rowspan=1 colspan=1>F F3, L, L, L+LG, G,F,H5, H7, N6WB, WB, WBA WL MP, MP,U0U U</td><td></td></tr><tr><td rowspan=1 colspan=2>FC1610AN 32.768000 KHz 12.5</td><td rowspan=1 colspan=1>12.5</td><td rowspan=1 colspan=1>2.8642</td><td rowspan=1 colspan=1>FO, F3</td><td></td></tr><tr><td rowspan=4 colspan=1>CITIZEN</td><td rowspan=4 colspan=2>CM1610H</td><td rowspan=1 colspan=1>6</td><td rowspan=1 colspan=1>0.7910</td><td rowspan=1 colspan=1>C F0F1, F3, F4_g2, L0, L4, L4+L5, G0, G4, F7, H5,H7, N6, WB, WB, WBA, WL, MP1, MP2, U0, U3, U5</td><td></td></tr><tr><td rowspan=1 colspan=1>7</td><td rowspan=1 colspan=1>1.0261</td><td rowspan=1 colspan=1>C F0 F3, F4g2, L0, L4, L4+,L5, G0, G4, F7, H5, H7, N6, WB, WB, WBA, WL, MP1, MP2, U0, U3, U5</td><td></td></tr><tr><td rowspan=1 colspan=1>9</td><td rowspan=1 colspan=1>1.5877</td><td rowspan=1 colspan=1>F F3, L, L, L+LG, G,F,H5, H7, N6WB, WB, WBA WL MP, MP,U0U U</td><td></td></tr><tr><td rowspan=1 colspan=1>12.5</td><td rowspan=1 colspan=1>2.8642</td><td rowspan=1 colspan=1>FO, F3</td><td></td></tr></table>

Table 7. Recommended crystal / MEMS resonators for the LSE oscillator in STM32 products (continued)   

<table><tr><td rowspan=1 colspan=1>Packagessize</td><td rowspan=1 colspan=1>Manufacturer</td><td rowspan=1 colspan=1>Quartz referencePart number</td><td rowspan=1 colspan=1>ESR(Ka</td><td rowspan=1 colspan=1>(GF )</td><td rowspan=1 colspan=1>(OF) )</td><td rowspan=1 colspan=1>h </td><td rowspan=1 colspan=1>STM32 series compatibility()(3)</td></tr><tr><td rowspan=11 colspan=1>18×10</td><td rowspan=3 colspan=1>ABRACON</td><td rowspan=1 colspan=1>ABS05-32.768 kHz 9 pF</td><td rowspan=2 colspan=1>90</td><td rowspan=2 colspan=1>1.3</td><td rowspan=1 colspan=1>9</td><td rowspan=1 colspan=1>1.6190</td><td rowspan=1 colspan=1>C0, F0, F3, F4_g2, L0, L4, L4+,L5, G0, G4, F7, H5, H7, N6, WB, WB0, WBA, WL, MP1, MP2, U0, U3, U5</td></tr><tr><td rowspan=1 colspan=1>ABS05-32.768 kHz</td><td rowspan=1 colspan=1>12.5</td><td rowspan=1 colspan=1>2.9062</td><td rowspan=1 colspan=1>F0, F3</td></tr><tr><td rowspan=1 colspan=1>ABS05W-32.768 kHz-D</td><td rowspan=1 colspan=1>70</td><td rowspan=1 colspan=1>2</td><td rowspan=1 colspan=1>4</td><td rowspan=1 colspan=1>0.4272</td><td rowspan=1 colspan=1>FFFF LL LL+LGFH H N WBWBW WL P MPUUU</td></tr><tr><td rowspan=8 colspan=1>RIVER</td><td rowspan=4 colspan=1>TFX-04</td><td rowspan=4 colspan=1>90</td><td rowspan=4 colspan=1>1.3</td><td rowspan=1 colspan=1>5</td><td rowspan=1 colspan=1>0.6056</td><td rowspan=1 colspan=1>F FF, L L L+LGGFH H7, N6WB, WB WBA WL P MPUUU</td></tr><tr><td rowspan=1 colspan=1>7</td><td rowspan=1 colspan=1>1.0513</td><td rowspan=1 colspan=1>C, F0, F3, F4_g2, L0, L4, L4+,L5, G0, G4, F7, H5, H7, N6, WB, WB, WBA, WL, MP1, MP2, U0, U3, U5</td></tr><tr><td rowspan=1 colspan=1>9</td><td rowspan=1 colspan=1>1.6190</td><td rowspan=1 colspan=1>CF0, F3, L0, L4, L4+L5, G0, G4, F7, H5, H7, N6, WB, WB, WBA, WL, MP1, MP2, U0, U3 U5</td></tr><tr><td rowspan=1 colspan=1>12.5</td><td rowspan=1 colspan=1>2.9062</td><td rowspan=1 colspan=1>FO, F3</td></tr><tr><td rowspan=4 colspan=1>TFX-04C</td><td rowspan=4 colspan=1>60</td><td rowspan=4 colspan=1>1.5</td><td rowspan=1 colspan=1>5</td><td rowspan=1 colspan=1>0.4298</td><td rowspan=1 colspan=1>C F0 F1, F2,F3, F4, L0, L1, L4, L4+,L5, G0, G4, F7, H5, H7, N6, WB, WB, WBA, WL, MP1, MP2, U0, U3, U5</td></tr><tr><td rowspan=1 colspan=1>7</td><td rowspan=1 colspan=1>0.7350</td><td rowspan=1 colspan=1>C0, F0, F1, F3, F4_g2, L0, L4, L4+,L5, G0, G4, F7, H5, H7, N6, WB, WB0, WBA, WL, MP1, MP2, U0, U3, U5</td></tr><tr><td rowspan=1 colspan=1>9</td><td rowspan=1 colspan=1>1.1216</td><td rowspan=1 colspan=1>C, F0, F3, F4_g2, L0, L4, L4+,L5, G0, G4, F7, H5, H7, N6, WB, WB, WBA, WL, MP1, MP2, U0, U3, U5</td></tr><tr><td rowspan=1 colspan=1>12.5</td><td rowspan=1 colspan=1>1.9940</td><td rowspan=1 colspan=1>C0, F0, F3, L0, L4, L4+,L5, G0, G4, F7, H5, H7, N6, WB, WB0, WBA, WL, MP1, MP2, U0, U3, U5</td></tr></table>

Table 7. Recommended crystal / MEMS resonators for the LSE oscillator in STM32 products (continued)   
  
20   

<table><tr><td colspan="3" rowspan="20">PackageManufacturersizeABRACON2.0 x 1.2mm{ECS</td><td colspan="1" rowspan="1">Packagesize</td><td colspan="2" rowspan="1">Manufacturer</td><td colspan="2" rowspan="1">Quartz referencePart number</td><td colspan="1" rowspan="1">ESR(ka)</td><td colspan="1" rowspan="1">(OF )</td></tr><tr><td colspan="1" rowspan="7">ABRACON</td><td colspan="1" rowspan="1">ABS06-127-32.768kHz</td><td colspan="1" rowspan="1"></td><td colspan="1" rowspan="1"></td><td colspan="1" rowspan="1">12.5</td><td colspan="1" rowspan="1">2.3844</td><td colspan="1" rowspan="1"> F3, L, L, L4+,L,G,G, F, H5, H7, N6, WB, WB, WBA, WL MP, MP, U0 U3U5</td><td></td></tr><tr><td colspan="1" rowspan="1">ABS06-32.768kHz-4P</td><td colspan="1" rowspan="1"></td><td colspan="1" rowspan="1"></td><td colspan="1" rowspan="1">4</td><td colspan="1" rowspan="1">0.2441</td><td colspan="1" rowspan="1">C, F0, F1, F2, F3, F4, L0, L1, L4, L4+,L5, G0, G4, F7, H5, H7, N6, WB, WB, WBA, WL, MP1, MP2, U0, U3, U5</td><td></td></tr><tr><td colspan="1" rowspan="1">ABS06-32.768kHz-6</td><td colspan="1" rowspan="2">90</td><td colspan="1" rowspan="2"></td><td colspan="1" rowspan="1">6</td><td colspan="1" rowspan="1">0.5493</td><td colspan="1" rowspan="1">C, F0, F1, F2, F3, F4, L0, L1, L4, L4+,L5, G0, G4, F7, H5, H7, N6, WB, WB, WBA, WL, MP1, MP2, U0, U3, U5</td><td></td></tr><tr><td colspan="1" rowspan="1">ABS06-32.768kHz-7</td><td colspan="1" rowspan="1">7</td><td colspan="1" rowspan="1">0.7477</td><td colspan="1" rowspan="1">C0, F0, F1, F3, F4_g2, L0, L4, L4+,L5, G0, G4, F7, H5, H7, N6, WB, WB0, WBA, WL, MP1, MP2, U0, U3, U5</td><td></td></tr><tr><td colspan="1" rowspan="1">ABS06-32.768kHz-9</td><td colspan="1" rowspan="2"></td><td colspan="1" rowspan="2"></td><td colspan="1" rowspan="1">9</td><td colspan="1" rowspan="1">1.2361</td><td colspan="1" rowspan="1">C0, F0, F3, F4_g2, L0, L4, L4+,L5, G0, G4, F7, H5, H7, N6, WB, WBO, WBA, WL, MP1, MP2, U0, U3, U5</td><td></td></tr><tr><td colspan="1" rowspan="1">ABS06-32.768kHz</td><td colspan="1" rowspan="1">12.5</td><td colspan="1" rowspan="1">2.3844</td><td colspan="1" rowspan="1"> F3, L, L, L4+,L,G0,G, F, H5, H7, N6, WB, WB, WBA, WL, MP, MP, U0 U3U5</td><td></td></tr><tr><td colspan="1" rowspan="1">ABS06-107-32.768kHz-T</td><td colspan="1" rowspan="1">80</td><td colspan="1" rowspan="1">1.5</td><td colspan="1" rowspan="1">4</td><td colspan="1" rowspan="1">0.4103</td><td colspan="1" rowspan="1">C, F0 F1, F2, F3, F4, L0, L1, L4, L4+,L5, G0, G4, F7, H5, H7, N6, WB, WB, WBA, WL, MP1, MP2, U0, U3, U5</td><td></td></tr><tr><td colspan="1" rowspan="1">ECS-.327-6-12-TR</td><td colspan="1" rowspan="1"></td><td colspan="1" rowspan="1"></td><td colspan="1" rowspan="1">6</td><td colspan="1" rowspan="1">0.8312</td><td colspan="1" rowspan="1">CF0F1, F3, F4g2, L0 L, L+L, G0, G4 F7, H5,H7, N6, WB,WB, WBA, WL, MP1, MP2, U0,U, U5</td><td></td></tr><tr><td colspan="1" rowspan="1">ECS-.327-7-12-TR</td><td colspan="1" rowspan="2">90</td><td colspan="1" rowspan="2">1.3</td><td colspan="1" rowspan="1">7</td><td colspan="1" rowspan="1">1.0513</td><td colspan="1" rowspan="1">CF0, F3, F4_g2, L0, L4, L4+,L5, G0, G4, F7, H5, H7, N6, WB, WB0, WBA, WL, MP1, MP2, U0, U3, U5</td><td></td></tr><tr><td colspan="1" rowspan="1">ECS-.327-9-12-TR</td><td colspan="1" rowspan="1"></td><td colspan="1" rowspan="1">9</td><td colspan="1" rowspan="1">1.6190</td><td colspan="1" rowspan="1">F3, L, L, L4+,L,GG, F, H5, H7, N6, WB, WB, WBA, WL, MP, MP, U0U3U5</td><td></td></tr><tr><td colspan="1" rowspan="1">ECS-.327-12.5-12-TR</td><td colspan="1" rowspan="1"></td><td colspan="1" rowspan="1"></td><td colspan="1" rowspan="1">12.5</td><td colspan="1" rowspan="1">2.9062</td><td colspan="1" rowspan="1">FO, F3</td><td></td></tr><tr><td colspan="1" rowspan="1">ECS-.327-CDX-1082</td><td colspan="1" rowspan="1">80</td><td colspan="1" rowspan="1">1.5</td><td colspan="1" rowspan="1">4</td><td colspan="1" rowspan="1">0.4103</td><td colspan="1" rowspan="1">C, F0, F1, F2, F3, F4, L0, L1, L4, L4+,L5, G0, G4, F7, H5, H7, N6, WB, WB, WBA, WL, MP1, MP2, U0, U3, U5</td><td></td></tr><tr><td colspan="1" rowspan="1">ECS-.327-6-12RR-TR</td><td colspan="1" rowspan="2"></td><td colspan="1" rowspan="1"></td><td colspan="1" rowspan="1">6</td><td colspan="1" rowspan="1">0.7372</td><td colspan="1" rowspan="1">F1, F3 F4 L0 L, L+L, G0 GF7, H5H7, N6, WB,WB, WBA, WL, MP1, MP, U0,U U</td><td></td></tr><tr><td colspan="1" rowspan="1">ECS-.327-7-12RR-TR</td><td colspan="1" rowspan="2"></td><td colspan="1" rowspan="2">1.7</td><td colspan="1" rowspan="1">7</td><td colspan="1" rowspan="1">0.8983</td><td colspan="1" rowspan="1">C0, F0, F1, F3, F4_g2, L0, L4, L4+,L5, G0, G4, F7, H5, H7, N6, WB, WB0, WBA, WL, MP1, MP2, U0, U3, U5</td><td colspan="1" rowspan="3"></td></tr><tr><td colspan="1" rowspan="1">ECS-.327-9-12RR-TR</td><td colspan="1" rowspan="1">9</td><td colspan="1" rowspan="1">1.3589</td><td colspan="1" rowspan="1">C0, F0, F3, F4_g2, L0, L4, L4+,L5, G0, G4, F7, H5, H7, N6, WB, WB0, WBA, WL, MP1, MP2, U0, U3, U5</td></tr><tr><td colspan="1" rowspan="1">ECS-.327-12.5-12R-TR</td><td colspan="1" rowspan="1">70</td><td colspan="1" rowspan="1"></td><td colspan="1" rowspan="1">12.5</td><td colspan="1" rowspan="1">2.3933</td><td colspan="1" rowspan="1">C0, F0, F3, L0, L4, L4+,L5, G0, G4, F7, H5, H7, N6, WB, WB0, WBA, WL, MP1, MP2, U0, U3, U5</td></tr><tr><td colspan="1" rowspan="1">ECS-.327-6-12R-TR</td><td colspan="1" rowspan="3"></td><td colspan="1" rowspan="3">1.3</td><td colspan="1" rowspan="1">6</td><td colspan="1" rowspan="1">0.4517</td><td colspan="1" rowspan="1">C, F0, F1, F2, F3, F4, L0, L1, L4, L4+,L5, G0, G4, F7, H5, H7, N6, WB, WB, WBA, WL, MP1, MP2, U0, U3, U5</td><td colspan="1" rowspan="1"></td></tr><tr><td colspan="1" rowspan="1">ECS-.327-9-12R-TR</td><td colspan="1" rowspan="1">9</td><td colspan="1" rowspan="1">0.8994</td><td colspan="1" rowspan="1">FF1, F3 F4g2 L0 L, L+L5, G0,GF7, H5H7, N6, WB,WB, WBA, WL, MP1, MP, U0,U3 U</td><td colspan="1" rowspan="1"></td></tr><tr><td colspan="1" rowspan="1">ECS-.327-12.5-12R-TR</td><td colspan="1" rowspan="1">12.5</td><td colspan="1" rowspan="1">1.6145</td><td colspan="1" rowspan="1"> F3, L, L, L4+,L,G,G, F, H5, H7, N6, WB, WB, WBA, WL, MP, MP, U0 U3U5</td><td colspan="1" rowspan="1"></td></tr><tr><td colspan="2" rowspan="29">PackageLsize2.0 x 1.2mm{</td><td colspan="1" rowspan="2">Packagesize</td><td colspan="1" rowspan="2">Manufacturer</td><td colspan="4" rowspan="2">Quartz referencePart number</td><td colspan="1" rowspan="2">ESRmax(kΩ)</td><td colspan="1" rowspan="2">(C )</td></tr><tr><td colspan="1" rowspan="1"></td></tr><tr><td colspan="1" rowspan="15">Micro Crystal</td><td colspan="1" rowspan="5">CM8V-T1A 0.3</td><td colspan="1" rowspan="5">90</td><td colspan="1" rowspan="5"></td><td colspan="1" rowspan="1">4</td><td colspan="1" rowspan="1">0.4126</td><td colspan="1" rowspan="1">C, F0, F1, F2, F3, F4, L0, L1, L4, L4+,L5, G0, G4, F7, H5, H7, N6, WB, WB, WBA, WL, MP1, MP2, U0, U3, U5</td><td colspan="1"></td></tr><tr><td colspan="1" rowspan="1">6</td><td colspan="1" rowspan="1">0.7910</td><td colspan="1" rowspan="1">C F0, F1, F3, F4_g2, L0, L4, L4+,L5, G0, G4, F7, H5, H7, N6, WB, WBO, WBA, WL, MP1, MP2, U0, U3, U5</td><td colspan="1"></td></tr><tr><td colspan="1" rowspan="1">7</td><td colspan="1" rowspan="1">1.0261</td><td colspan="1" rowspan="1">C, F0, F3, F4_g2, L0, L4, L4+,L5, G0, G4, F7, H5, H7, N6, WB, WB0, WBA, WL, MP1, MP2, U0, U3, U5</td><td colspan="1"></td></tr><tr><td colspan="1" rowspan="1">9</td><td colspan="1" rowspan="1">1.5877</td><td colspan="1" rowspan="1">CF F3, L0, L, L4+L5, G0, G4, F7,H5, H7, N6, WB, WB, WBA, WL, MP1, MP, U0, U3 U5</td><td colspan="1"></td></tr><tr><td colspan="1" rowspan="1">12.5</td><td colspan="1" rowspan="1">2.8642</td><td colspan="1" rowspan="1">F0, F3</td><td colspan="1"></td></tr><tr><td colspan="1" rowspan="5">CC8V-T1A</td><td colspan="1" rowspan="5">80</td><td colspan="1" rowspan="5">1.2</td><td colspan="1" rowspan="1">4</td><td colspan="1" rowspan="1">0.3667</td><td colspan="1" rowspan="1">CF F1, F2,F3, F4, L0, L, L, L4+,L5, G0, G4, F7,H5, H7, N6, WB, WB, WBA, WL, MP1, MP2, U0, U3, U5</td><td colspan="1" rowspan="1"></td></tr><tr><td colspan="1" rowspan="1">6</td><td colspan="1" rowspan="1">0.7031</td><td colspan="1" rowspan="1">C0, F0, F1, F3, F4_g2, L0, L4, L4+,L5, G0, G4, F7, H5, H7, N6, WB, WB0, WBA, WL, MP1, MP2, U0, U3, U5</td><td colspan="1" rowspan="1"></td></tr><tr><td colspan="1" rowspan="1">7</td><td colspan="1" rowspan="1">0.9120</td><td colspan="1" rowspan="1">C0, F0, F1, F3, F4_g2, L0, L4, L4+,L5, G0, G4, F7, H5, H7, N6, WB, WB0, WBA, WL, MP1, MP2, U0, U3, U5</td><td colspan="1" rowspan="1"></td></tr><tr><td colspan="1" rowspan="1">9</td><td colspan="1" rowspan="1">1.4113</td><td colspan="1" rowspan="1">C0, F0, F3, F4_g2, L0, L4, L4+,L5, G0, G4, F7, H5, H7, N6, WB, WB0, WBA, WL, MP1, MP2, U0, U3, U5</td><td colspan="1" rowspan="1"></td></tr><tr><td colspan="1" rowspan="1">12.5</td><td colspan="1" rowspan="1">2.5460</td><td colspan="1" rowspan="1">CF0, F3, L0, L4, L4+L5, G0, G4, F7, H5, H7, N6, WB, WB, WBA, WL, MP1, MP2, U0, U3, U5</td><td colspan="1"></td></tr><tr><td colspan="1" rowspan="5">CM8V-T1A</td><td colspan="1" rowspan="5">70</td><td colspan="1" rowspan="5"></td><td colspan="1" rowspan="1">4</td><td colspan="1" rowspan="1">0.3209</td><td colspan="1" rowspan="1">CF, F, F2, F, F4, L0, L, L, L4+,L5, G0, G4 F, H5, H7, N6, WB, WB, WBA, WL, MP, MP2, U0,U3, U</td><td colspan="1"></td></tr><tr><td colspan="1" rowspan="1">6</td><td colspan="1" rowspan="1">0.6152</td><td colspan="1" rowspan="1">CF0, F, F3, F4g2, L0, L, L4+,L5, G0, G4, F7, H5,H7, N6, WB, WB, WBA, WL, MP1, MP, U0, U3, U5</td><td colspan="1"></td></tr><tr><td colspan="1" rowspan="1">7</td><td colspan="1" rowspan="1">0.7980</td><td colspan="1" rowspan="1">C F0, F1, F3, F4_g2, L0, L4, L4+,L5, G0, G4, F7, H5, H7, N6, WB, WBO, WBA, WL, MP1, MP2, U0, U3, U5</td><td colspan="1"></td></tr><tr><td colspan="1" rowspan="1">9</td><td colspan="1" rowspan="1">1.2349</td><td colspan="1" rowspan="1">C, F0, F3, F4_g2, L0, L4, L4+,L5, G0, G4, F7, H5, H7, N6, WB, WB, WBA, WL, MP1, MP2, U0, U3, U5</td><td colspan="1"></td></tr><tr><td colspan="1" rowspan="1">12.5</td><td colspan="1" rowspan="1">2.2277</td><td colspan="1" rowspan="1">CF0, F3, L0, L4, L4+L5, G0, G4, F7, H5, H7, N6, WB, WB, WBA, WL, MP1, MP2, U0, U3, U5</td><td colspan="1"></td></tr><tr><td colspan="1" rowspan="4">EPSON</td><td colspan="1" rowspan="1">FC-12M 32.768000kHz 12.5</td><td colspan="1" rowspan="1">90</td><td colspan="1" rowspan="1">1.3</td><td colspan="1" rowspan="1">12.5</td><td colspan="1" rowspan="1">2.9062</td><td colspan="1" rowspan="1">FO, F3</td><td colspan="1"></td></tr><tr><td colspan="1" rowspan="1">FC-12D 32.768000kHz 7</td><td colspan="1" rowspan="1"></td><td colspan="1" rowspan="1"></td><td colspan="1" rowspan="1">7</td><td colspan="1" rowspan="1">0.7737</td><td colspan="1" rowspan="1">CF0, F1, F3, F4_g2, L0, L4, L4+,L5, G0, G4, F7, H5, H7, N6, WB, WB, WBA, WL, MP1, MP2, U0, U3, U5</td><td colspan="1"></td></tr><tr><td colspan="1" rowspan="1">FC-12D 32.768000kHz 9</td><td colspan="1" rowspan="2">75</td><td colspan="1" rowspan="2">0.8</td><td colspan="1" rowspan="1">9</td><td colspan="1" rowspan="1">1.2213</td><td colspan="1" rowspan="1">C0, F0, F3, F4_g2, L0, L4, L4+,L5, G0, G4, F7, H5, H7, N6, WB, WB0, WBA, WL, MP1, MP2, U0, U3, U5</td><td colspan="1" rowspan="1"></td></tr><tr><td colspan="1" rowspan="1">FC-12D 32.768000kHz 12.5</td><td colspan="1" rowspan="1">12.5</td><td colspan="1" rowspan="1">2.2495</td><td colspan="1" rowspan="1">C0, F0, F3, L0, L4, L4+,L5, G0, G4, F7, H5, H7, N6, WB, WB0, WBA, WL, MP1, MP2, U0, U3, U5</td><td colspan="1" rowspan="1"></td></tr><tr><td colspan="1" rowspan="8">RIVER</td><td colspan="1" rowspan="4">TFX-03</td><td colspan="1" rowspan="4">90</td><td colspan="1" rowspan="4">1.3</td><td colspan="1" rowspan="1">5</td><td colspan="1" rowspan="1">0.6447</td><td colspan="1" rowspan="1">C0, F0, F1, F3, F4_g2, L0, L4, L4+,L5, G0, G4, F7, H5, H7, N6, WB, WB0, WBA, WL, MP1, MP2, U0, U3, U5</td><td colspan="1" rowspan="1"></td></tr><tr><td colspan="1" rowspan="1">7</td><td colspan="1" rowspan="1">1.0513</td><td colspan="1" rowspan="1">C0, F0, F3, F4_g2, L0, L4, L4+,L5, G0, G4, F7, H5, H7, N6, WB, WB0, WBA, WL, MP1, MP2, U0, U3, U5</td><td colspan="1" rowspan="1"></td></tr><tr><td colspan="1" rowspan="1">9</td><td colspan="1" rowspan="1">1.6190</td><td colspan="1" rowspan="1">C F0, F3, L0, L4, L4+L5, G0, G4, F7, H5, H7, N6, WB, WB, WBA, WL, MP1, MP2, UO, U3, U5</td><td colspan="1" rowspan="1"></td></tr><tr><td colspan="1" rowspan="1">12.5</td><td colspan="1" rowspan="1">2.9062</td><td colspan="1" rowspan="1">F0, F3</td><td colspan="1" rowspan="1"></td></tr><tr><td colspan="1" rowspan="4">TFX-03C</td><td colspan="1" rowspan="4">60</td><td colspan="1" rowspan="4">1.8</td><td colspan="1" rowspan="1">5</td><td colspan="1" rowspan="1">0.4704</td><td colspan="1" rowspan="1">CFF, F2F3, F, L0,L L, L4+L5, G, G, F7,H5, H7, N6 WB,WB, WBA, WL, MP, MP, U0, U U</td><td colspan="1" rowspan="1"></td></tr><tr><td colspan="1" rowspan="1">7</td><td colspan="1" rowspan="1">0.7878</td><td colspan="1" rowspan="1">C0, F0, F1, F3, F4_g2, L0, L4, L4+,L5, G0, G4, F7, H5, H7, N6, WB, WB0, WBA, WL, MP1, MP2, U0, U3, U5</td><td colspan="1" rowspan="1"></td></tr><tr><td colspan="1" rowspan="1">9</td><td colspan="1" rowspan="1">1.1866</td><td colspan="1" rowspan="1">C0, F0, F3, F4_g2, L0, L4, L4+,L5, G0, G4, F7, H5, H7, N6, WB, WB0, WBA, WL, MP1, MP2, U0, U3, U5</td><td colspan="1" rowspan="1"></td></tr><tr><td colspan="1" rowspan="1">12.5</td><td colspan="1" rowspan="1">2.0804</td><td colspan="1" rowspan="1">CO, F0, F3, L0, L4, L4+,L5, G0, G4, F7, H5, H7, N6, WB, WBO, WBA, WL, MP1, MP2, U0, U3, U5</td><td colspan="1" rowspan="1"></td></tr></table>

0

Table 7. Recommended crystal / MEMS resonators for the LSE oscillator in STM32 products (continued)   
  
20   

<table><tr><td colspan="1" rowspan="1"></td><td colspan="1" rowspan="1">Packagessize</td><td colspan="1" rowspan="1">Manufacturer</td><td colspan="1" rowspan="1">Quartz referencePart number</td><td colspan="1" rowspan="1">ESRmax(kΩ)</td><td colspan="1" rowspan="1">(CF) )</td><td colspan="1" rowspan="1"> OF) )</td><td colspan="1" rowspan="1">Sm </td><td colspan="1" rowspan="1">STM32 series compatibility()(3)</td></tr><tr><td colspan="2" rowspan="17">20 xx1,2</td><td colspan="1" rowspan="7">NDK</td><td colspan="1" rowspan="1">NX2012SA 32.768 kHz EXS00A-MU00527</td><td colspan="1" rowspan="1"></td><td colspan="1" rowspan="1"></td><td colspan="1" rowspan="1">6</td><td colspan="1" rowspan="1">0.7228</td><td colspan="1" rowspan="1">C0, F0, F1, F3, F4_g2, L0, L4, L4+, L5, G0, G4, F7, H5, H7, N6, WB, WB0, WBA, WL, MP1, MP2, U0, U3, U5</td></tr><tr><td colspan="1" rowspan="1">NX2012SA 32.768 kHz EXS00A-MU00524</td><td colspan="1" rowspan="1">80</td><td colspan="1" rowspan="1">1.3</td><td colspan="1" rowspan="1">7</td><td colspan="1" rowspan="1">0.9344</td><td colspan="1" rowspan="1">C0, F0, F1, F3, F4_g2, L0, L4, L4+, L5, G0, G4, F7, H5, H7, N6, WB, WB0, WBA, WL, MP1, MP2, U0, U3, U5</td></tr><tr><td colspan="1" rowspan="1">NX2012SA 32.768 kHz EXS00A-0528</td><td colspan="1" rowspan="1"></td><td colspan="1" rowspan="1"></td><td colspan="1" rowspan="1">12.5</td><td colspan="1" rowspan="1">2.5833</td><td colspan="1" rowspan="1">C F0, F3, L0, L4, L4+, L5, G0, G4, F7, H5, H7, N6, WB, WB0, WBA, WL, MP1, MP2, U0, U3, U5</td></tr><tr><td colspan="1" rowspan="1">NX2012SE 32.768 kHz EXS00A-MU01260</td><td colspan="1" rowspan="4">50(4)</td><td colspan="1" rowspan="4">1.7</td><td colspan="1" rowspan="1">6</td><td colspan="1" rowspan="1">0.5026</td><td colspan="1" rowspan="1">C0, F0, F1, F3, F4_g2, L0, L4, L4+, L5, G0, G4, F7, H5, H7, N6, WB, WB0, WBA, WL, MP1, MP2, U0, U3, U5</td></tr><tr><td colspan="1" rowspan="1">NX2012SE 32.768 kHz EXS00A-MU01259</td><td colspan="1" rowspan="1">7</td><td colspan="1" rowspan="1">0.6416</td><td colspan="1" rowspan="1">C, F0, F1, F3, F4_g2, L0, L4, L4+, L5, G0, G4, F7, H5, H7, N6, WB, WB0, WBA, WL, MP1, MP2, U0, U3, U5</td></tr><tr><td colspan="1" rowspan="1">NX2012SE 32.768 kHz EXS00A-MU01611</td><td colspan="1" rowspan="1">9</td><td colspan="1" rowspan="1">0.9706</td><td colspan="1" rowspan="1">C, F0, F1, F3, F4_g2, L0, L4, L4+, L5, G0, G4, F7, H5, H7, N6, WB, WB0, WBA, WL, MP1, MP2, U0, U3, U5</td></tr><tr><td colspan="1" rowspan="1">NX2012SE 32.768 kHz EXS00A-MU01612</td><td colspan="1" rowspan="1">12.5</td><td colspan="1" rowspan="1">1.7095</td><td colspan="1" rowspan="1">C, F0, F3, L0, L4, L4+,L5, G0, G4, F7, H5, H7, N6, WB, WB0, WBA, WL, MP1, MP2, U0, U3, U5</td></tr><tr><td colspan="1" rowspan="6">SlI</td><td colspan="1" rowspan="4">SC-20T</td><td colspan="1" rowspan="4">75</td><td colspan="1" rowspan="4">1</td><td colspan="1" rowspan="1">6</td><td colspan="1" rowspan="1">0.6231</td><td colspan="1" rowspan="1">C, F0, F1, F3, F4_g2, L0, L4, L4+,L5, G0, G4, F7, H5, H7, N6, WB, WB0, WBA, WL, MP1, MP2, U0, U3, U5</td></tr><tr><td colspan="1" rowspan="1">7</td><td colspan="1" rowspan="1">0.8138</td><td colspan="1" rowspan="1">C0, F0, F1, F3, F4_g2, L0, L4, L4+,L5, G0, G4, F7, H5, H7, N6, WB, WB0, WBA, WL, MP1, MP2, U0, U3, U5</td></tr><tr><td colspan="1" rowspan="1">9</td><td colspan="1" rowspan="1">1.2717</td><td colspan="1" rowspan="1">C0, F0, F3, F4_g2, L0, L4, L4+,L5, G0, G4, F7, H5, H7, N6, WB, WB0, WBA, WL, MP1, MP2, U0, U3, U5</td></tr><tr><td colspan="1" rowspan="1">12.5</td><td colspan="1" rowspan="1">2.3177</td><td colspan="1" rowspan="1">C, F0, F3, L0, L4, L4+,L5, G0, G4, F7, H5, H7, N6, WB, WB0, WBA, WL, MP1, MP2, U0, U3, U5</td></tr><tr><td colspan="1" rowspan="2">SC-20S</td><td colspan="1" rowspan="2">70</td><td colspan="1" rowspan="2">1.3</td><td colspan="1" rowspan="1">6</td><td colspan="1" rowspan="1">0.6325</td><td colspan="1" rowspan="1">C, F0, F1, F3, F4_g2, L0, L4, L4+,L5, G0, G4, F7, H5, H7, N6, WB, WB0, WBA, WL, MP1, MP2, U0, U3, U5</td></tr><tr><td colspan="1" rowspan="1">12.5</td><td colspan="1" rowspan="1">2.2604</td><td colspan="1" rowspan="1">CO, F0, F3, L0, L4, L4+,L5, G0, G4, F7, H5, H7, N6, WB, WBO, WBA, WL, MP1, MP2, U0, U3, U5</td></tr><tr><td colspan="1" rowspan="4">CITIZEN</td><td colspan="1" rowspan="4">CM2012H</td><td colspan="1" rowspan="4">70</td><td colspan="1" rowspan="4">1.3</td><td colspan="1" rowspan="1">6</td><td colspan="1" rowspan="1">0.6325</td><td colspan="1" rowspan="1">C, F0, F1, F3, F4_g2, L0, L4, L4+,L5, G0, G4, F7, H5, H7, N6, WB, WB0, WBA, WL, MP1, MP2, U0, U3, U5</td></tr><tr><td colspan="1" rowspan="1">7</td><td colspan="1" rowspan="1">0.8176</td><td colspan="1" rowspan="1">C0, F0, F1, F3, F4_g2, L0, L4, L4+,L5, G0, G4, F7, H5, H7, N6, WB, WB0, WBA, WL, MP1, MP2, U0, U3, U5</td></tr><tr><td colspan="1" rowspan="1">9</td><td colspan="1" rowspan="1">1.2592</td><td colspan="1" rowspan="1">C0, F0, F3, F4_g2, L0, L4, L4+,L5, G0, G4, F7, H5, H7, N6, WB, WB0, WBA, WL, MP1, MP2, U0, U3, U5</td></tr><tr><td colspan="1" rowspan="1">12.5</td><td colspan="1" rowspan="1">2.2604</td><td colspan="1" rowspan="1">C0, F0, F3, L0, L4, L4+,L5, G0, G4, F7, H5, H7, N6, WB, WB0, WBA, WL, MP1, MP2, U0, U3, U5</td></tr><tr><td colspan="2" rowspan="25">1 Packagessize3.2×152</td><td colspan="1" rowspan="1">Packagessize</td><td colspan="1" rowspan="1">Manufacturer</td><td colspan="4" rowspan="1">Quartz referencePart number</td><td colspan="1" rowspan="1">ESR(ka) )</td></tr><tr><td colspan="1" rowspan="11">ABRACON</td><td colspan="1" rowspan="1">ABS07L-32.768kHz 7pF</td><td colspan="1" rowspan="3">80</td><td colspan="1" rowspan="3">1.4</td><td colspan="1" rowspan="1">7</td><td colspan="1" rowspan="1">0.9751</td><td colspan="1" rowspan="1">C0, F0, F1, F3, F4_g2, L0, L4, L4+,L5, G0, G4, F7, H5, H7, N6, WB, WB0, WBA, WL, MP1, MP2, U0, U3, U5</td></tr><tr><td colspan="1" rowspan="1">ABS07L-32.768kHz 9pF</td><td colspan="1" rowspan="1">9</td><td colspan="1" rowspan="1">1.6472</td><td colspan="1" rowspan="1">CF0, F3, L0, L4, L4+,L5, G0, G4, F7, H5, H7, N6, WB, WB, WBA, WL, MP1, MP2, U0, U3, U5</td></tr><tr><td colspan="1" rowspan="1">ABS07L-32.768kHz</td><td colspan="1" rowspan="1">12.5</td><td colspan="1" rowspan="1">2.6208</td><td colspan="1" rowspan="1">C0, F0, F3, L0, L4, L4+,L5, G0, G4, F7, H5, H7, N6, WB, WB0, WBA, WL, MP1, MP2, U0, U3, U5</td></tr><tr><td colspan="1" rowspan="1">ABS07-32.768kHz 6pF</td><td colspan="1" rowspan="5">70</td><td colspan="1" rowspan="5">1.1</td><td colspan="1" rowspan="1">6</td><td colspan="1" rowspan="1">0.5815</td><td colspan="1" rowspan="1">CF0, F1, F3, F4_g2, L0, L4, L4+,L5, G0, G4, F7, H5, H7, N6, WB, WB, WBA, WL, MP1, MP2, U0, U3, U5</td></tr><tr><td colspan="1" rowspan="1">ABS07-32.768kHz 7pF</td><td colspan="1" rowspan="1">7</td><td colspan="1" rowspan="1">0.7596</td><td colspan="1" rowspan="1">C,F0, F1, F3, F4_g2, L0, L4, L4+,L5, G0, G4, F7, H5, H7, N6, WB, WB, WBA, WL, MP1, MP2, U0, U3, U5</td></tr><tr><td colspan="1" rowspan="1">ABS07-32.768kHz 9pF</td><td colspan="1" rowspan="1">9</td><td colspan="1" rowspan="1">1.1869</td><td colspan="1" rowspan="1">C, F0, F3, F4_g2, L0, L4, L4+,L5, G0, G4, F7, H5, H7, N6, WB, WB, WBA, WL, MP1, MP2, U0, U3, U5</td></tr><tr><td colspan="1" rowspan="1">ABS07 32.768kHz</td><td colspan="1" rowspan="1">12.5</td><td colspan="1" rowspan="1">2.1631</td><td colspan="1" rowspan="1">C F0, F3, L0, L4, L4+,L5, G0, G4, F7, H5, H7, N6, WB, WB, WBA, WL, MP1, MP2, U0, U3, U5</td></tr><tr><td colspan="1" rowspan="1">ABS07-166-32.768kHz-T</td><td colspan="1" rowspan="1">7</td><td colspan="1" rowspan="1">0.7596</td><td colspan="1" rowspan="1">C0, F0, F1, F3, F4_g2, L0, L4, L4+,L5, G0, G4, F7, H5, H7, N6, WB, WB0, WBA, WL, MP1, MP2, U0, U3, U5</td></tr><tr><td colspan="1" rowspan="1">ABS07-120-32.768kHz-T</td><td colspan="1" rowspan="1">60</td><td colspan="1" rowspan="1">1.2</td><td colspan="1" rowspan="1">6</td><td colspan="1" rowspan="1">0.5273</td><td colspan="1" rowspan="1">C,F0, F1, F2, F3, F4, L0, L1, L4, L4+,L5, G0, G4, F7, H5, H7, N6, WB, WB, WBA, WL, MP1, MP2, U0, U3, U5</td></tr><tr><td colspan="1" rowspan="1">ABS07W-32.768kHz-D</td><td colspan="1" rowspan="1">55</td><td colspan="1" rowspan="1">1.15</td><td colspan="1" rowspan="1">3</td><td colspan="1" rowspan="1">0.1606</td><td colspan="1" rowspan="1">C, F0, F1, F2, F3, F4, L0, L1, L4, L4+,L5, G0, G4, F7, H5, H7, N6, WB, WB, WBA, WL, MP1, MP2, U0, U3, U5</td></tr><tr><td colspan="1" rowspan="1">ABS07-LR-32.768 kHz-6</td><td colspan="1" rowspan="1">50</td><td colspan="1" rowspan="1">1.3</td><td colspan="1" rowspan="1">6</td><td colspan="1" rowspan="1">0.4517</td><td colspan="1" rowspan="1">C, F0, F1, F2, F3, F4, L0, L1, L4, L4+,L5, G0, G4, F7, H5, H7, N6, WB, WB, WBA, WL, MP1, MP2, U0, U3, U5</td></tr><tr><td colspan="1" rowspan="13">CITIZEN</td><td colspan="1" rowspan="4">CM315D</td><td colspan="1" rowspan="4"></td><td colspan="1" rowspan="4">0,95</td><td colspan="1" rowspan="1">6</td><td colspan="1" rowspan="1">0.5733</td><td colspan="1" rowspan="1">C, F0, F1, F3 F4_g2, L0, L4, L4+,L5, G0, G4, F7, H5, H7, N6, WB, WB0, WBA, WL, MP1, MP2, U0, U3, U5</td></tr><tr><td colspan="1" rowspan="1">7</td><td colspan="1" rowspan="1">0.7501</td><td colspan="1" rowspan="1">C0, F0, F1, F3, F4_g2, L0, L4, L4+,L5, G0, G4, F7, H5, H7, N6, WB, WBO, WBA, WL, MP1, MP2, U0, U3, U5</td></tr><tr><td colspan="1" rowspan="1">9</td><td colspan="1" rowspan="1">1.1751</td><td colspan="1" rowspan="1">C, F0, F3, F4_g2, L0, L4, L4+,L5, G0, G4, F7, H5, H7, N6, WB, WB, WBA, WL, MP1, MP2, U0, U3, U5</td></tr><tr><td colspan="1" rowspan="1">12.5</td><td colspan="1" rowspan="1">2.1471</td><td colspan="1" rowspan="1">C0, F0, F3, L0, L4, L4+,L5, G0, G4, F7, H5, H7, N6, WB, WB0, WBA, WL, MP1, MP2, U0, U3, U5</td></tr><tr><td colspan="1" rowspan="5">CM315E</td><td colspan="1" rowspan="5">70</td><td colspan="1" rowspan="5">0,75</td><td colspan="1" rowspan="1">4</td><td colspan="1" rowspan="1">0.2678</td><td colspan="1" rowspan="1">C F0 F1, F2,F3, F4, L0, L1, L4, L4+,L5, G0, G4, F7, H5, H7, N6, WB, WB, WBA, WL, MP1, MP2, U0, U3, U5</td></tr><tr><td colspan="1" rowspan="1">6</td><td colspan="1" rowspan="1">0.5407</td><td colspan="1" rowspan="1">C F0 F1, F2,F3, F4, L0, L1, L4, L4+,L5, G0, G4, F7, H5, H7, N6, WB, WB, WBA, WL, MP1, MP2, U0, U3, U5</td></tr><tr><td colspan="1" rowspan="1">8</td><td colspan="1" rowspan="1">0.9087</td><td colspan="1" rowspan="1">C0, F0, F1, F3, F4_g2, L0, L4, L4+,L5, G0, G4, F7, H5, H7, N6, WB, WB0, WBA, WL, MP1, MP2, U0, U3, U5</td></tr><tr><td colspan="1" rowspan="1">9</td><td colspan="1" rowspan="1">1.1283</td><td colspan="1" rowspan="1">C, F0, F3, F4_g2, L0, L4, L4+,L5, G0, G4, F7, H5, H7, N6, WB, WB, WBA, WL, MP1, MP2, U0, U3, U5</td></tr><tr><td colspan="1" rowspan="1">12.5</td><td colspan="1" rowspan="1">2.0838</td><td colspan="1" rowspan="1">C0, F0, F3, L0, L4, L4+,L5, G0, G4, F7, H5, H7, N6, WB, WB0, WBA, WL, MP1, MP2, U0, U3, U5</td></tr><tr><td colspan="1" rowspan="4">CM315DL</td><td colspan="1" rowspan="4">50</td><td colspan="1" rowspan="4">1,3</td><td colspan="1" rowspan="1">6</td><td colspan="1" rowspan="1">0.4517</td><td colspan="1" rowspan="1">CF0 F1, F2,F3, F4, L0, L, L4, L4+,L5, G0, G4, F7, H5, H7, N6, WB, WB, WBA, WL, MP1, MP2, U0, U3, U5</td></tr><tr><td colspan="1" rowspan="1">7</td><td colspan="1" rowspan="1">0.5840</td><td colspan="1" rowspan="1">C0, F0, F1, F3, F4_g2, L0, L4, L4+,L5, G0, G4, F7, H5, H7, N6, WB, WB0, WBA, WL, MP1, MP2, U0, U3, U5</td></tr><tr><td colspan="1" rowspan="1">9</td><td colspan="1" rowspan="1">0.8994</td><td colspan="1" rowspan="1">C0, F0, F1, F3, F4_g2, L0, L4, L4+,L5, G0, G4, F7, H5, H7, N6, WB, WB0, WBA, WL, MP1, MP2, U0, U3, U5</td></tr><tr><td colspan="1" rowspan="1">12.5</td><td colspan="1" rowspan="1">1.6145</td><td colspan="1" rowspan="1">C0, F0, F3, L0, L4, L4+,L5, G0, G4, F7, H5, H7, N6, WB, WB0, WBA, WL, MP1, MP2, U0, U3, U5</td></tr></table>

00   
Table 7. Recommended crystal / MEMS resonators for the LSE oscillator in STM32 products (continued)   
20   
20   

<table><tr><td></td><td colspan="1" rowspan="1">Packagessize</td><td colspan="1" rowspan="1">Manufacturer</td><td colspan="1" rowspan="1">Quartz referencePart number</td><td colspan="1" rowspan="1">ESRmax(kΩ)</td><td colspan="1" rowspan="1">(OF )</td><td colspan="1" rowspan="1">(oF )</td><td colspan="1" rowspan="1"> </td><td colspan="1" rowspan="1">STM32 series compatibility(2)(3)</td></tr><tr><td colspan="2" rowspan="24">3.2×1</td><td colspan="1" rowspan="12">Micro Crystal</td><td colspan="1" rowspan="4">CC7V-T1ACM7V-T1A (low profile)</td><td colspan="1" rowspan="4">70</td><td colspan="1" rowspan="4">1,2</td><td colspan="1" rowspan="1">6</td><td colspan="1" rowspan="1">0.6152</td><td colspan="1" rowspan="1">CF, F, F3 F4g, L0, L, L4+L5, G, G, F7,H5, H, N6, WB, WB, WBA, WL, MP1, MP, U0, U3, U5</td></tr><tr><td colspan="1" rowspan="1">7</td><td colspan="1" rowspan="1">0.7980</td><td colspan="1" rowspan="1">C0, F0, F1, F3, F4_g2, L0, L4, L4+,L5, G0, G4, F7, H5, H7, N6, WB, WB0, WBA, WL, MP1, MP2, U0, U3, U5</td></tr><tr><td colspan="1" rowspan="1">9</td><td colspan="1" rowspan="1">1.2349</td><td colspan="1" rowspan="1">C, F0, F3, F4_g2, L0, L4, L4+, L5, G0, G4, F7, H5, H7, N6, WB, WB0, WBA, WL, MP1, MP2, U0, U3, U5</td></tr><tr><td colspan="1" rowspan="1">12.5</td><td colspan="1" rowspan="1">2.2277</td><td colspan="1" rowspan="1">C, F0, F3, L0, L4, L4+,L5, G0, G4, F7, H5, H7, N6, WB, WB0, WBA, WL, MP1, MP2, U0, U3, U5</td></tr><tr><td colspan="1" rowspan="4">CM7V-T1A 0.3</td><td colspan="1" rowspan="4">60</td><td colspan="1" rowspan="4">1,4</td><td colspan="1" rowspan="1">6</td><td colspan="1" rowspan="1">0.5571</td><td colspan="1" rowspan="1">C0, F0, F1, F2, F3, F4, L0, L1, L4, L5, G0, G4, F7, H5, H7, N6, WB, WB0, WBA, WL, MP1, MP2, U0, U3, U5</td></tr><tr><td colspan="1" rowspan="1">7</td><td colspan="1" rowspan="1">0.7178</td><td colspan="1" rowspan="1">C0, F0, F1, F3, F4_g2, L0, L4, L5, G0, G4, F7, H5, H7, N6, WB, WB0, WBA, WL, MP1, MP2, U0, U3, U5</td></tr><tr><td colspan="1" rowspan="1">9</td><td colspan="1" rowspan="1">1.1004</td><td colspan="1" rowspan="1">CO, F0, F3, F4_g2, L0, L4, L5, G0, G4, F7, H5, H7, N6, WB, WB0, WBA, WL, MP1, MP2, U0, U3, U5</td></tr><tr><td colspan="1" rowspan="1">12.5</td><td colspan="1" rowspan="1">1.9656</td><td colspan="1" rowspan="1">CF0, F3, L0, L4, L5, G0, G4, F7, H5, H7, N6, WB, WB0, WBA, WL, MP1, MP2, U0, U3, U5</td></tr><tr><td colspan="1" rowspan="4">CM7V-T1A</td><td colspan="1" rowspan="4">50</td><td colspan="1" rowspan="4">1,3</td><td colspan="1" rowspan="1">6</td><td colspan="1" rowspan="1">0.4517</td><td colspan="1" rowspan="1">C, F0, F1, F2, F3, F4, L0, L1,L4, L5, G0, G4, F7, H5, H7, N6, WB, WB0, WBA, WL, MP1, MP2, U0, U3, U5</td></tr><tr><td colspan="1" rowspan="1">7</td><td colspan="1" rowspan="1">0.5840</td><td colspan="1" rowspan="1">C0, F0, F1, F3, F4_g2, L0, L4, L4+,L5, G0, G4, F7, H5, H7, N6, WB, WB0, WBA, WL, MP1, MP2, U0, U3, U5</td></tr><tr><td colspan="1" rowspan="1">9</td><td colspan="1" rowspan="1">0.8994</td><td colspan="1" rowspan="1">C0, F0, F1, F3, F4_g2, L0, L4, L4+,L5, G0, G4, F7, H5, H7, N6, WB, WB0, WBA, WL, MP1, MP2, U0, U3, U5</td></tr><tr><td colspan="1" rowspan="1">12.5</td><td colspan="1" rowspan="1">1.6145</td><td colspan="1" rowspan="1">CO, F0, F3, L0, L4, L4+,L5, G0, G4, F7, H5, H7, N6, WB, WBO, WBA, WL, MP1, MP2, U0, U3, U5</td></tr><tr><td colspan="1" rowspan="8">EPSON</td><td colspan="1" rowspan="1">FC-135 32.768000 kHz 7</td><td colspan="1" rowspan="3">70</td><td colspan="1" rowspan="3">1.0</td><td colspan="1" rowspan="1">7</td><td colspan="1" rowspan="1">0.7596</td><td colspan="1" rowspan="1">CF0, F1, F3, F4_g2, L0, L4, L4+,L5, G0, G4, F7, H5, H7, N6, WB, WB, WBA, WL, MP1, MP2, U0, U3, U5</td></tr><tr><td colspan="1" rowspan="1">FC-135 32.768000 kHz 9</td><td colspan="1" rowspan="1">9</td><td colspan="1" rowspan="1">1.1869</td><td colspan="1" rowspan="1">C0, F0, F3, F4_g2, L0, L4, L4+,L5, G0, G4, F7, H5, H7, N6, WB, WB0, WBA, WL, MP1, MP2, U0, U3, U5</td></tr><tr><td colspan="1" rowspan="1">FC-135 32.768000 kHz 12.5</td><td colspan="1" rowspan="2">70</td><td colspan="1" rowspan="1">12.5</td><td colspan="1" rowspan="1">2.1631</td><td colspan="1" rowspan="1">C0, F0, F3, L0, L4, L4+,L5, G0, G4, F7, H5, H7, N6, WB, WBO, WBA, WL, MP1, MP2, U0, U3, U5</td></tr><tr><td colspan="1" rowspan="1">FC-13A 32.768000 kHz 9</td><td colspan="1" rowspan="2"></td><td colspan="1" rowspan="2">0.9</td><td colspan="1" rowspan="1">9</td><td colspan="1" rowspan="1">1.1633</td><td colspan="1" rowspan="1">C0, F0, F3, F4_g2, L0, L4, L4+,L5, G0, G4, F7, H5, H7, N6, WB, WB0, WBA, WL, MP1, MP2, U0, U3, U5</td></tr><tr><td colspan="1" rowspan="1">FC-13A 32.768000 kHz 12.5</td><td colspan="1" rowspan="1">12.5</td><td colspan="1" rowspan="1">2.1312</td><td colspan="1" rowspan="1">C, F0, F3, L0, L4, L4+,L5, G0, G4, F7, H5, H7, N6, WB, WB0, WBA, WL, MP1, MP2, U0, U3, U5</td></tr><tr><td colspan="1" rowspan="1">FC-135R 32.768000 kHz 7</td><td colspan="1" rowspan="3">50</td><td colspan="1" rowspan="3">1.1</td><td colspan="1" rowspan="1">7</td><td colspan="1" rowspan="1">0.5562</td><td colspan="1" rowspan="1">C, F0, F1, F3, F4_g2, L0, L1, L4, L4+ L5, G0, G4, F7, H5, H7, N6, WB, WB, WBA, WL, MP1, MP2, U0, U3, U5</td></tr><tr><td colspan="1" rowspan="1">FC-135R 32.768000 kHz 9</td><td colspan="1" rowspan="1">9</td><td colspan="1" rowspan="1">0.8648</td><td colspan="1" rowspan="1">C0, F0, F1, F3, F4_g2, L0, L4, L4+,L5, G0, G4, F7, H5, H7, N6, WB, WB0, WBA, WL, MP1, MP2, U0, U3, U5</td></tr><tr><td colspan="1" rowspan="1">FC-135R 32.768000 kHz 12.5</td><td colspan="1" rowspan="1">12.5</td><td colspan="1" rowspan="1">1.5681</td><td colspan="1" rowspan="1">CF0, F3, L0, L4, L4+,L5, G0, G4, F7, H5, H7, N6, WB, WB, WBA, WL, MP1, MP2, U0, U3, U5</td></tr><tr><td colspan="1" rowspan="4">SlI</td><td colspan="1" rowspan="2">SC-32S</td><td colspan="1" rowspan="2">70</td><td colspan="1" rowspan="2">1.0</td><td colspan="1" rowspan="1">6</td><td colspan="1" rowspan="1">0,5815</td><td colspan="1" rowspan="1">CF0, F1, F3, F4_g2, L0, L4, L4+,L5, G0, G4, F7, H5, H7, N6, WB, WB, WBA, WL, MP1, MP2, U0, U3, U5</td></tr><tr><td colspan="1" rowspan="1">1.0</td><td colspan="1" rowspan="1">12.5</td><td colspan="1" rowspan="1">2.1631</td><td colspan="1" rowspan="1">C0, F0, F3, L0, L4, L4+,L5, G0, G4, F7, H5, H7, N6, WB, WB0, WBA, WL, MP1, MP2, U0, U3, U5</td></tr><tr><td colspan="1" rowspan="2">SC-32P</td><td colspan="1" rowspan="2">50</td><td colspan="1" rowspan="1"></td><td colspan="1" rowspan="1">6</td><td colspan="1" rowspan="1">0,4154</td><td colspan="1" rowspan="1">C, F0, F1, F2, F3, F4, L0, L1, L4, L4+,L5, G0, G4, F7, H5, H7, N6, WB, WB0, WBA, WL, MP1, MP2, U0, U3, U5</td></tr><tr><td colspan="1" rowspan="1">12.5</td><td colspan="1" rowspan="1">1.5451</td><td colspan="1" rowspan="1">C0, F0, F3, L0, L4, L4+,L5, G0, G4, F7, H5, H7, N6, WB, WB0, WBA, WL, MP1, MP2, U0, U3, U5</td></tr><tr><td colspan="2" rowspan="26">4 Packagesiiz2  3.2 x 1.5mm{300</td><td colspan="1" rowspan="1">Packagesiiz</td><td colspan="1" rowspan="1">Manufacturer</td><td colspan="4" rowspan="1">Quartz referencePart number</td><td colspan="1" rowspan="1">ESR(ka)</td></tr><tr><td colspan="1" rowspan="20">ECS</td><td colspan="1" rowspan="1">ECS-.327-6-34QS-TR</td><td colspan="1" rowspan="4"></td><td colspan="1" rowspan="4">1,1</td><td colspan="1" rowspan="1">6</td><td colspan="1" rowspan="1">0.5983</td><td colspan="1" rowspan="1">CF0, F, F3, F4_g2, L0, L, L4+,L5, G0, G4,F7, H5, H7, N6, WB, WB, WBA, WL, MP, MP, UO, U3, U5</td></tr><tr><td colspan="1" rowspan="1">ECS-.327-7-34QS-TR</td><td colspan="1" rowspan="1">7</td><td colspan="1" rowspan="1">0.7787</td><td colspan="1" rowspan="1">C0, F0, F1, F3, F4_g2, L0, L4, L4+,L5, G0, G4, F7, H5, H7, N6, WB, WB, WBA, WL, MP1, MP2, U0, U3, U5</td></tr><tr><td colspan="1" rowspan="1">ECS-.327-9-34QS-TR</td><td colspan="1" rowspan="1">9</td><td colspan="1" rowspan="1">1.2108</td><td colspan="1" rowspan="1">C F0, F3, F4_g2, L0, L4, L4+,L5, G0, G4, F7, H5, H7, N6, WB, WB0, WBA, WL, MP1, MP2, U0, U3, U5</td></tr><tr><td colspan="1" rowspan="1">ECS-.327-12.5-34QS-TR</td><td colspan="1" rowspan="1"></td><td colspan="1" rowspan="1">12.5</td><td colspan="1" rowspan="1">2.1953</td><td colspan="1" rowspan="1">C0, F0, F3, L0, L4, L4+,L5, G0, G4, F7, H5, H7, N6, WB, WB0, WBA, WL, MP1, MP2, U0, U3, U5</td></tr><tr><td colspan="1" rowspan="1">ECS-.327-6-34G-TR</td><td colspan="1" rowspan="2"></td><td colspan="1" rowspan="2">0,75</td><td colspan="1" rowspan="1">6</td><td colspan="1" rowspan="1">0.5407</td><td colspan="1" rowspan="1">CF0, F1, F2 F3, F4, L0, L, L4, L4+,L5,G0, G, F7,H5, H7, N6, WB, WB, WBA, WL, MP1, MP2, U0, U, U5</td></tr><tr><td colspan="1" rowspan="1">ECS-.327-12.5-34G-TR</td><td colspan="1" rowspan="1">70</td><td colspan="1" rowspan="1">12.5</td><td colspan="1" rowspan="1">2.0838</td><td colspan="1" rowspan="1">C0, F0, F3, L0, L4, L4+,L5, G0, G4, F7, H5, H7, N6, WB, WB0, WBA, WL, MP1, MP2, U0, U3, U5</td></tr><tr><td colspan="1" rowspan="1">ECS-.327-6-34S-TR</td><td colspan="1" rowspan="1"></td><td colspan="1" rowspan="6">1,05</td><td colspan="1" rowspan="1">6</td><td colspan="1" rowspan="1">0.5899</td><td colspan="1" rowspan="1">C F0, F1, F3, F4_g2, L0, L4, L4+,L5, G0, G4, F7, H5, H7, N6, WB, WB, WBA, WL, MP1, MP2, U0, U3, U5</td></tr><tr><td colspan="1" rowspan="1">ECS-.327-12.5-34S-TR</td><td colspan="1" rowspan="1">12.5</td><td colspan="1" rowspan="1">2.1792</td><td colspan="1" rowspan="1">C0, F0, F3, L0, L4, L4+,L5, G0, G4, F7, H5, H7, N6, WB, WB0, WBA, WL, MP1, MP2, U0, U3, U5</td></tr><tr><td colspan="1" rowspan="1">ECX-.327-CDX-1293</td><td colspan="1" rowspan="1">12.5</td><td colspan="1" rowspan="1">2.1792</td><td colspan="1" rowspan="1">CF F3, L, L, L4+,L5,G0, G4, F7, H5, H7, N6, WB, WB, WBA, WL, MP1, MP, U0, U3,U5</td></tr><tr><td colspan="1" rowspan="1">ECS-.327-7-34B-TR</td><td colspan="1" rowspan="1">7</td><td colspan="1" rowspan="1">0.7691</td><td colspan="1" rowspan="1">C0, F0, F1, F3, F4_g2, L0, L4, L4+,L5, G0, G4, F7, H5, H7, N6, WB, WB0, WBA, WL, MP1, MP2, U0, U3, U5</td></tr><tr><td colspan="1" rowspan="1">ECS-.327-9-34B-TR</td><td colspan="1" rowspan="1">9</td><td colspan="1" rowspan="1">1.1988</td><td colspan="1" rowspan="1">C F0 F3, F4g2, L0, L, L4+,L5, G0, G4,F7, H5, H7, N6, WB, WB, WBA, WL, MP1, MP2, U0, U3, U5</td></tr><tr><td colspan="1" rowspan="1">ECS-.327-12.5-34B-TR</td><td colspan="1" rowspan="1">12.5</td><td colspan="1" rowspan="1">2.1792</td><td colspan="1" rowspan="1">C F0, F3, L0, L4, L4+,L5, G0, G4, F7, H5, H7, N6, WB, WB, WBA, WL, MP1, MP2, U0, U3, U5</td></tr><tr><td colspan="1" rowspan="1">ECS-.327-CDX-1128</td><td colspan="1" rowspan="1">60</td><td colspan="1" rowspan="1">2</td><td colspan="1" rowspan="1">6</td><td colspan="1" rowspan="1">0.6511</td><td colspan="1" rowspan="1">FF1, F3, F4g2, L0 L, L+L5, G0, GF7, H5,H7, N6, WB,WB, WBA, WL, MP1, MP, U0,U3 U5</td></tr><tr><td colspan="1" rowspan="1">ECS-.327-6-34R-TR</td><td colspan="1" rowspan="4">50</td><td colspan="1" rowspan="4">1,3</td><td colspan="1" rowspan="1">6</td><td colspan="1" rowspan="1">0.4517</td><td colspan="1" rowspan="1">CF0, F1, F2 F3, F4, L0, L1, L4, L4+,L5, G0, G4, F7, H5, H7, N6, WB, WB, WBA, WL, MP1, MP2, U0,U3, U5</td></tr><tr><td colspan="1" rowspan="1">ECS-.327-7-34R-TR</td><td colspan="1" rowspan="1">7</td><td colspan="1" rowspan="1">0.5840</td><td colspan="1" rowspan="1">C0, F0, F1, F3, F4_g2, L0, L4, L4+,L5, G0, G4, F7, H5, H7, N6, WB, WB0, WBA, WL, MP1, MP2, U0, U3, U5</td></tr><tr><td colspan="1" rowspan="1">ECS-.327-9-34R-TR</td><td colspan="1" rowspan="1">9</td><td colspan="1" rowspan="1">0.8994</td><td colspan="1" rowspan="1">C0, F0, F1, F3, F4_g2, L0, L4, L4+,L5, G0, G4, F7, H5, H7, N6, WB, WB0, WBA, WL, MP1, MP2, U0, U3, U5</td></tr><tr><td colspan="1" rowspan="1">ECS-.327-12.5-34R-TR</td><td colspan="1" rowspan="1">1,3</td><td colspan="1" rowspan="1">12.5</td><td colspan="1" rowspan="1">1.6145</td><td colspan="1" rowspan="1"> F3, L, L, L4+,L,G0,G, F, H5, H7, N6, WB, WB, WBA, WL, MP, MP, U0 U3U5</td></tr><tr><td colspan="1" rowspan="1">ECS-.327-6-34RR-TR</td><td colspan="1" rowspan="3">40</td><td colspan="1" rowspan="1"></td><td colspan="1" rowspan="1">6</td><td colspan="1" rowspan="1">0.3614</td><td colspan="1" rowspan="1">C, F0, F1, F2, F3, F4, L0, L1, L4, L4+,L5, G0, G4, F7, H5, H7, N6, WB, WB, WBA, WL, MP1, MP2, U0, U3, U5</td></tr><tr><td colspan="1" rowspan="1">ECS-.327-9-34RR-TR</td><td colspan="1" rowspan="1">9</td><td colspan="1" rowspan="1">0.7195</td><td colspan="1" rowspan="1">C0, F0, F1, F3, F4_g2, L0, L4, L4+,L5, G0, G4, F7, H5, H7, N6, WB, WB0, WBA, WL, MP1, MP2, U0, U3, U5</td></tr><tr><td colspan="1" rowspan="1">ECS-.327-12.5-34RR-TR</td><td colspan="1" rowspan="1">12.5</td><td colspan="1" rowspan="1">1.2916</td><td colspan="1" rowspan="1">C0, F0, F3, F4_g2, L0, L4, L4+,L5, G0, G4, F7, H5, H7, N6, WB, WB0, WBA, WL, MP1, MP2, U0, U3, U5</td></tr><tr><td colspan="1" rowspan="5">NDK</td><td colspan="1" rowspan="1">NX3215SA 32.768 kHz EXS00A-MU0525</td><td colspan="1" rowspan="3">70</td><td colspan="1" rowspan="3">1.0</td><td colspan="1" rowspan="1">6</td><td colspan="1" rowspan="1">0.5815</td><td colspan="1" rowspan="1">C, F0, F1, F2, F3, F4, L0, L1, L4, L4+, L5, G0, G4, F7, H5, H7, N6, WB, WB, WBA, WL, MP1, MP2, U0, U3, U5</td></tr><tr><td colspan="1" rowspan="1">NX3215SA 32.768 kHz EXS00A-MU0523</td><td colspan="1" rowspan="1">7</td><td colspan="1" rowspan="1">0.7596</td><td colspan="1" rowspan="1">CF0F1, F3, F42, L0 L, L+ L5, G0 G4,F7, H5, H7, N6 WB, WB, WBA, WL, MP1, MP2, U0, U3, U5</td></tr><tr><td colspan="1" rowspan="1">NX3215SA 32.768 kHz EXS00A-MU00526</td><td colspan="1" rowspan="1">12.5</td><td colspan="1" rowspan="1">2.1631</td><td colspan="1" rowspan="1">C F F3, L, L4, L4, L5, G0, G4, F7, H5, H7, N6, WB, WB, WBA, WL, MP1, MP2, U0, U3, U5</td></tr><tr><td colspan="1" rowspan="1">NX3215SE 32.768 KHzEXS00A-MU00990</td><td colspan="1" rowspan="2">40</td><td colspan="1" rowspan="2">1.3</td><td colspan="1" rowspan="1">6</td><td colspan="1" rowspan="1">0.3323</td><td colspan="1" rowspan="1">C F0, F1, F2, F3, F4, L0, L1, L4, L4+, L5, G0, G4, F7, H5, H7, N6, WB, WB, WBA, WL, MP1, MP2, U0, U3, U5</td></tr><tr><td colspan="1" rowspan="1">NX3215SE 32.768 KHzEXS00A-MU00989</td><td colspan="1" rowspan="1">12.5</td><td colspan="1" rowspan="1">1.2361</td><td colspan="1" rowspan="1">C, F0, F3, F4_g2, L0, L4, L4+, L5, G0, G4, F7, H5, H7, N6, WB, WB, WBA, WL, MP1, MP2, U0, U3, U5</td></tr></table>

Table 7. Recommended crystal / MEMS resonators for the LSE oscillator in STM32 products (continued)   
20   
  

<table><tr><td rowspan=2 colspan=1>Packagessize</td><td rowspan=2 colspan=1>Manufacturer</td><td rowspan=2 colspan=1>Quartz referencePart number</td><td rowspan=2 colspan=1>FSR(kΩ)</td><td rowspan=2 colspan=1>(O )</td><td rowspan=2 colspan=1>(OF )</td><td rowspan=2 colspan=1> </td><td rowspan=2 colspan=1>STM32 series compatibility(2)(3)</td></tr><tr></tr><tr><td rowspan=8 colspan=1>4.1 x 1.5mm^{2}</td><td rowspan=4 colspan=1>Micro Crystal</td><td rowspan=4 colspan=1>CC5V-T1A</td><td rowspan=5 colspan=1>70</td><td rowspan=4 colspan=1>1.2</td><td rowspan=1 colspan=1>6</td><td rowspan=1 colspan=1>0.6152</td><td rowspan=1 colspan=1>CF, F, F3 F4g, L0, L, L4+,L5, G0, G, F7, H5, H7, N6, WB, WB, WBA, WL, MP1, MP, U0, U3, U5</td></tr><tr><td rowspan=1 colspan=1>7</td><td rowspan=1 colspan=1>0.7980</td><td rowspan=1 colspan=1>CF0, F1, F3, F4_g2, L0, L4, L4+,L5, G0, G4, F7, H5, H7, N6, WB, WB, WBA, WL, MP1, MP2, U0, U3, U5</td></tr><tr><td rowspan=1 colspan=1>9</td><td rowspan=1 colspan=1>1.2349</td><td rowspan=1 colspan=1>F, F3 F4g, L0, L, L4+L5, G0, G4, F7,H5, H7, N6, WB, WB, WBA, WL, MP1, MP, U0, U3, U5</td></tr><tr><td rowspan=1 colspan=1>12.5</td><td rowspan=1 colspan=1>2.2277</td><td rowspan=1 colspan=1>C F0, F3, L0, L, L4+,L5, G0, G4, F7, H5 H7, N6, WB, WB, WBA, WL, MP1, MP2, U0, U3, U5</td></tr><tr><td rowspan=4 colspan=1>ECS</td><td rowspan=1 colspan=1>ECS-.327-6-49-TR</td><td rowspan=4 colspan=1></td><td rowspan=4 colspan=1>1.1</td><td rowspan=1 colspan=1>6</td><td rowspan=1 colspan=1>0.5983</td><td rowspan=1 colspan=1>C F0,F1, F3, F4g2, L0, L, L4+,L5, G0 G4,F7, H5, H7, N6 WB, WB, WBA, WL, MP1, MP2, U0, U3, U5</td></tr><tr><td rowspan=1 colspan=1>ECS-.327-7-49-TR</td><td rowspan=1 colspan=1>7</td><td rowspan=1 colspan=1>0.7787</td><td rowspan=1 colspan=1>CF0, F1, F3, F4g2, L0, L, L4+,L5, G0, G4, F7, H5,H7, N6, WB, WB, WBA, WL, MP1, MP, U0, U3, U5</td></tr><tr><td rowspan=1 colspan=1>ECS-.327-9-49-TR</td><td rowspan=1 colspan=1>9</td><td rowspan=1 colspan=1>1.2108</td><td rowspan=1 colspan=1>C0, F0, F3, F4_g2, L0, L4, L4+,L5, G0, G4, F7, H5, H7, N6, WB, WB0, WBA, WL, MP1, MP2, U0, U3, U5</td></tr><tr><td rowspan=1 colspan=1>ECS-.327-12.5-49-TR</td><td rowspan=1 colspan=1>12.5</td><td rowspan=1 colspan=1>2.1953</td><td rowspan=1 colspan=1>CF F3, L0, L, L4+L5, G0, G4, F7,H5, H7, N6, WB, WB, WBA, WL, MP1, MP, U0, U3 U5</td></tr><tr><td rowspan=2 colspan=1>6.9 x 1.4mm{</td><td rowspan=2 colspan=1>ABRACON</td><td rowspan=1 colspan=1>ABS13 -32.768kHz-7pF</td><td rowspan=2 colspan=1>65</td><td rowspan=2 colspan=1>-</td><td rowspan=1 colspan=1>7</td><td rowspan=1 colspan=1>0.5400</td><td rowspan=1 colspan=1>CF0, F1, F2, F3, F4, L0, L, L, L4+,L5 G0, G4,F7, H5, H7, N6, WB, WB, WBA, WL, MP1, MP2, U0, U3,U</td></tr><tr><td rowspan=1 colspan=1>ABS13 -32.768kHz</td><td rowspan=1 colspan=1>12.5</td><td rowspan=1 colspan=1>1.7221</td><td rowspan=1 colspan=1>FF3, L0, L, L4+L5, G0, G, F, H5 H7, N6, WB, WB, WBA, WL, MP1, MP2, U0,U U</td></tr><tr><td rowspan=16 colspan=1>7.0x1</td><td rowspan=5 colspan=1>SII</td><td rowspan=2 colspan=1>SSP-T7-F</td><td rowspan=5 colspan=1></td><td rowspan=5 colspan=1>0.9</td><td rowspan=1 colspan=1>7</td><td rowspan=1 colspan=1>0.6878</td><td rowspan=1 colspan=1>CF0, F, F3, F4_g2, L0, L, L4+,L5, G0, G4, F7, H5, H7, N6, WB, WB, WBA, WL, MP, MP, U0, U3, U5</td></tr><tr><td rowspan=1 colspan=1>12.5</td><td rowspan=1 colspan=1>1.9790</td><td rowspan=1 colspan=1>C0, F0, F3, L0, L4, L4+,L5, G0, G4, F7, H5, H7, N6, WB, WBO, WBA, WL, MP1, MP2, U0, U3, U5</td></tr><tr><td rowspan=3 colspan=1>SSP-T7-FL</td><td rowspan=1 colspan=1>3.7</td><td rowspan=1 colspan=1>0.2332</td><td rowspan=1 colspan=1>CFF, F2F3, F, L0,L, L, L4+L5, G0, G, F7, H5, H7, N6 WB, WB, WBA, WL, MP, MP, U0, U U</td></tr><tr><td rowspan=1 colspan=1>4.4</td><td rowspan=1 colspan=1>0.3095</td><td rowspan=1 colspan=1>C, F0, F1, F2, F3, F4, L0, L1, L4, L4+,L5, G0, G4, F7, H5, H7, N6, WB, WB, WBA, WL, MP1, MP, U0, U3, U5</td></tr><tr><td rowspan=1 colspan=1>6</td><td rowspan=1 colspan=1>0.5247</td><td rowspan=1 colspan=1>C, F0, F1, F2, F3, F4, L0, L1, L4, L4+,L5, G0, G4, F7, H5, H7, N6, WB, WB, WBA, WL, MP1, MP2, U0, U3, U5</td></tr><tr><td rowspan=3 colspan=1>EPSON</td><td rowspan=1 colspan=1>MC-164 32.768000kHz 7</td><td rowspan=1 colspan=1></td><td rowspan=1 colspan=1>7</td><td rowspan=1 colspan=1>0.6705</td><td rowspan=1 colspan=1>CFF1, F F4g, L0, L, L+L, G0 G4,F7, H5, H7, N6 WB, WB, WBA,WL, MP1, MP2, U0, U, U</td></tr><tr><td rowspan=1 colspan=1>MC-164 32.768000kHz 9</td><td rowspan=1 colspan=1>9</td><td rowspan=1 colspan=1>1.0585</td><td rowspan=1 colspan=1>C0, F0, F3, F4_g2, L0, L4, L4+,L5, G0, G4, F7, H5, H7, N6, WB, WB0, WBA, WL, MP1, MP2, U0, U3, U5</td></tr><tr><td rowspan=1 colspan=1>MC-164 32.768000kHz 12.5</td><td rowspan=1 colspan=1>12.5</td><td rowspan=1 colspan=1>1.9496</td><td rowspan=1 colspan=1>CF0, F3, L0, L4, L4+,L5, G0, G4, F7, H5, H7, N6, WB, WB, WBA, WL, MP1, MP2, U0, U3, U5</td></tr><tr><td rowspan=4 colspan=1>ECS</td><td rowspan=1 colspan=1>ECS-.327-6-38-TR</td><td rowspan=1 colspan=1>6</td><td rowspan=1 colspan=1>0.5096</td><td rowspan=1 colspan=1>C, F0, F1, F2, F3, F4, L0, L1, L4, L4+,L5, G0, G4, F7, H5, H7, N6, WB, WB, WBA, WL, MP1, MP2, U0, U3, U5</td></tr><tr><td rowspan=1 colspan=1>ECS-.327-7-38-TR</td><td rowspan=1 colspan=1>7</td><td rowspan=1 colspan=1>0.6705</td><td rowspan=1 colspan=1>CF0 F1, F3, F4_g2, L0, L, L4+,L5, G0, G, F7, H5, H7, N6, WB, WB, WBA, WL, MP1, MP2, U0, U3, U5</td></tr><tr><td rowspan=1 colspan=1>ECS-.327-9-38-TR</td><td rowspan=1 colspan=1>9</td><td rowspan=1 colspan=1>1.0585</td><td rowspan=1 colspan=1>C, F0, F3, F4_g2, L0, L4, L4+,L5, G0, G4, F7, H5, H7, N6, WB, WB, WBA, WL, MP1, MP2, U0, U3, U5</td></tr><tr><td rowspan=1 colspan=1>ECS-.327-12.5-38-TR</td><td rowspan=1 colspan=1>12.5</td><td rowspan=1 colspan=1>1.9496</td><td rowspan=1 colspan=1>C0, F0, F3, L0, L4, L4+,L5, G0, G4, F7, H5, H7, N6, WB, WB0, WBA, WL, MP1, MP2, U0, U3, U5</td></tr><tr><td rowspan=4 colspan=1>CITIZEN</td><td rowspan=4 colspan=1>CM130</td><td rowspan=1 colspan=1>6</td><td rowspan=1 colspan=1>0.5096</td><td rowspan=1 colspan=1>FFF F3 F, L,LL L+L G0G, F, H5, H7, N6, WB, WB, WBA, WL, MP, MP, U,U U</td></tr><tr><td rowspan=1 colspan=1>7</td><td rowspan=1 colspan=1>0.6705</td><td rowspan=1 colspan=1>CF0, F1, F3 F4_g2, L0, L4, L4+,L5, G0, G4, F7, H5, H7, N6, WB, WB0, WBA, WL, MP1, MP2, U0, U3, U5</td></tr><tr><td rowspan=1 colspan=1>9</td><td rowspan=1 colspan=1>1.0585</td><td rowspan=1 colspan=1>C0, F0, F3, F4_g2, L0, L4, L4+,L5, G0, G4, F7, H5, H7, N6, WB, WB0, WBA, WL, MP1, MP2, U0, U3, U5</td></tr><tr><td rowspan=1 colspan=1>12.5</td><td rowspan=1 colspan=1>1.9496</td><td rowspan=1 colspan=1>CF, F3, L0, L, L4+L5, G0, G, F7,H5, H7, N6, WB, WB, WBA, WL, MP1, MP, U0, U3, U5</td></tr></table>

Table 7. Recommended crystal / MEMS resonators for the LSE oscillator in STM32 products (continued)   

<table><tr><td rowspan=1 colspan=1>Packagesize</td><td rowspan=1 colspan=1>Manufacturer</td><td rowspan=1 colspan=1>Quartz referencePart number</td><td rowspan=1 colspan=1>ESRKa </td><td rowspan=1 colspan=1>CGR )</td><td rowspan=1 colspan=1>G )</td><td rowspan=1 colspan=1>ua </td><td rowspan=1 colspan=1>STM32 series compatibility()(3)</td></tr><tr><td rowspan=4 colspan=1>8.0x38</td><td rowspan=2 colspan=1>ECS</td><td rowspan=1 colspan=1>ECS-.327-6-17X-TR</td><td rowspan=4 colspan=1>50</td><td rowspan=4 colspan=1>1.35</td><td rowspan=1 colspan=1>6</td><td rowspan=1 colspan=1>0.4580</td><td rowspan=1 colspan=1>FLLHW PP</td></tr><tr><td rowspan=1 colspan=1>ECS-.327-12.5-17X-TR</td><td rowspan=1 colspan=1>12.5</td><td rowspan=1 colspan=1>1.6263</td><td rowspan=1 colspan=1></td></tr><tr><td rowspan=2 colspan=1>ABRACON</td><td rowspan=1 colspan=1>ABS25-32.768kHz-6-T</td><td rowspan=1 colspan=1>6</td><td rowspan=1 colspan=1>0.4580</td><td rowspan=1 colspan=1>FLLPU</td></tr><tr><td rowspan=1 colspan=1>ABS25-32.768kHz-T</td><td rowspan=1 colspan=1>12.5</td><td rowspan=1 colspan=1>1.6263</td><td rowspan=1 colspan=1>F L L L+LGFH HNWB WB WB WL P MPUUU</td></tr></table>

As defined in Section 3.4: Oscillator transconductance.   
. 4Low_ESR: -40 to +85 C.

Note: STM32U575/585 rev. X devices do not support crystal/MEMS resonators with CL ≤ 6 pF.

# Recommended crystals for STM8AF/AL/S MCUs

6.1 Part numbers of recommended crystal oscillators

Table 8. KYOCERA compatible crystals (not exhaustive list)   

<table><tr><td rowspan=1 colspan=1>Part number</td><td rowspan=1 colspan=1>Frequency</td><td rowspan=1 colspan=1>ESR max</td><td rowspan=1 colspan=1>CL</td><td rowspan=1 colspan=1>Drive level (DL)</td></tr><tr><td rowspan=1 colspan=1>CX3225GA8000D0PTVCC</td><td rowspan=2 colspan=1>8 MHz</td><td rowspan=2 colspan=1>500 Ω</td><td rowspan=7 colspan=1>8 pF</td><td rowspan=3 colspan=1>200 μW max</td></tr><tr><td rowspan=1 colspan=1>CX3225SA8000D0PTVCC</td></tr><tr><td rowspan=1 colspan=1>CX2016SA16000D0GSSCC</td><td rowspan=5 colspan=1>16 MHz</td><td rowspan=1 colspan=1>200 Ω</td></tr><tr><td rowspan=1 colspan=1>CX2016GR16000D0GTVCC</td><td rowspan=1 colspan=1>300 Ω</td><td rowspan=1 colspan=1>300 μW max</td></tr><tr><td rowspan=1 colspan=1>CX3225CA16000D0PSVCCCX3225GA16000D0PTVCC</td><td rowspan=1 colspan=1>100 Ω</td><td rowspan=1 colspan=1>200 μW max</td></tr><tr><td rowspan=1 colspan=1>CX3225SB16000D0GSSCC</td><td rowspan=1 colspan=1>80 Ω</td><td rowspan=1 colspan=1>100 μW max</td></tr><tr><td rowspan=1 colspan=1>CX3225SA16000D0PTVCC</td><td rowspan=1 colspan=1>60 Ω</td><td rowspan=1 colspan=1>200 μW max</td></tr></table>

Note:

Contact provider regarding recommended crystals for new designs.

Table 9. NDK compatible crystals (not exhaustive list)   

<table><tr><td rowspan=1 colspan=1>Part number</td><td rowspan=1 colspan=1>Frequency</td><td rowspan=1 colspan=1>ESR max</td><td rowspan=1 colspan=1>CL</td><td rowspan=1 colspan=1>Drive level (DL)</td></tr><tr><td rowspan=1 colspan=1>NX3225GD 8MHzEXS00A-CG04874</td><td rowspan=1 colspan=1>8 MHz</td><td rowspan=1 colspan=1>500 Ω</td><td rowspan=3 colspan=1>8 pF</td><td rowspan=8 colspan=1>200 μW max</td></tr><tr><td rowspan=1 colspan=1>NX3225GA 16MHzEXS00A-CG04815</td><td rowspan=2 colspan=1>16 MHz</td><td rowspan=1 colspan=1>80 Ω</td></tr><tr><td rowspan=1 colspan=1>NX2016SA 16MHzEXS00A-CS07826</td><td rowspan=1 colspan=1>200 Ω</td></tr><tr><td rowspan=1 colspan=1>NX3225GA 24MHzEXS00A-CG04818</td><td rowspan=2 colspan=1>24 MHz</td><td rowspan=1 colspan=1>50 Ω</td><td rowspan=1 colspan=1>8 pF</td></tr><tr><td rowspan=1 colspan=1>NX2016SA 24MHzEXS00A-CS10820</td><td rowspan=1 colspan=1>80 Ω</td><td rowspan=1 colspan=1>6 pF</td></tr><tr><td rowspan=1 colspan=1>NX3225GA 25MHzEXS00A-CG06750</td><td rowspan=2 colspan=1>25 MHz</td><td rowspan=1 colspan=1>50 Ω</td><td rowspan=1 colspan=1>8 pF</td></tr><tr><td rowspan=1 colspan=1>NX2016SA 25MHzEXS00A-CS11321</td><td rowspan=1 colspan=1>80 Ω</td><td rowspan=1 colspan=1>6 pF</td></tr><tr><td rowspan=1 colspan=1>NX2016SA32MHzEXS00A-CS10925</td><td rowspan=1 colspan=1>32 MHz</td><td rowspan=1 colspan=1>80 Ω</td><td rowspan=1 colspan=1>6 pF</td></tr><tr><td rowspan=1 colspan=1>NX1612SA 40MHzEXS00A-CS13836</td><td rowspan=1 colspan=1>40 MHz</td><td rowspan=2 colspan=1>80 Ω</td><td rowspan=1 colspan=1>6 pF</td><td rowspan=2 colspan=1>100 μW max</td></tr><tr><td rowspan=1 colspan=1>NX1612SA 48MHzEXS00A-CS13734</td><td rowspan=1 colspan=1>48 MHz</td><td rowspan=1 colspan=1>7 pF</td></tr></table>

# 6.2 Recommended ceramic resonators

Table 10 and Table 11 give the references of recommended CERALOCK® ceramic resonators for the STM8A microcontrollers provided and certified by muRata.

Table 10. Recommended conditions (for consumer)   

<table><tr><td rowspan=1 colspan=1>Part number</td><td rowspan=1 colspan=1>Frequency</td><td rowspan=1 colspan=1>CL</td></tr><tr><td rowspan=1 colspan=1>CSTCR4M00G55-R0</td><td rowspan=1 colspan=1>4 MHz</td><td rowspan=1 colspan=1>CL1 = CL2 = 39 pF</td></tr><tr><td rowspan=1 colspan=1>CSTNE8M00G550000R0</td><td rowspan=1 colspan=1>8 MHz</td><td rowspan=1 colspan=1>CL1 = CL2 = 33 pF</td></tr><tr><td rowspan=1 colspan=1>CSTNE16M0V530000R0</td><td rowspan=1 colspan=1>16 MHz</td><td rowspan=1 colspan=1>CL1 = CL2 = 15 pF</td></tr></table>

Table 11. Recommended conditions (for CAN-BUS)   

<table><tr><td rowspan=1 colspan=1>Part number</td><td rowspan=1 colspan=1>Frequency</td><td rowspan=1 colspan=1>CL</td></tr><tr><td rowspan=1 colspan=1>CSTCR4M00G55B-R0</td><td rowspan=1 colspan=1>4 MHz</td><td rowspan=1 colspan=1>CL1 = CL2 = 39 pF</td></tr><tr><td rowspan=1 colspan=1>CSTNE8M00G55A000R0</td><td rowspan=1 colspan=1>8 MHz</td><td rowspan=1 colspan=1>CL1 = CL2= 33 pF</td></tr><tr><td rowspan=1 colspan=1>CSTNE16M0V53C000RO</td><td rowspan=1 colspan=1>16 MHz</td><td rowspan=1 colspan=1>CL1 = CL2 = 15 pF</td></tr></table>

# Tips for improving oscillator stability

# 7.1 PCB design guidelines

Keeping the signal-to-noise ratio (SNR) below acceptable limits for a perfect operation of the oscillator means more severe constraints on the oscillator PCB design to reduce its sensitivity to noise.

Therefore, great care must be taken when designing the PCB to reduce as much as possible the SNR. A non exhaustive list of precautions to take when designing the oscillator PCB is provided below:

Avoid high values of stray capacitance and inductances, as they can lead to   
uncontrollable oscillation (the oscillator can resonate at overtones or harmonic frequencies). Reducing the stray capacitance also decreases startup time and improves oscillation frequency stability.   
To reduce high frequency noise propagation across the board, the MCu/MPU must have a stable power supply source, to ensure noiseless crystal oscillations. This means that well-sized decoupling capacitor must be used for powering the device.   
Mount the crystal as close as possible to the MCU/MPU, to keep tracks short, and to reduce inductive and capacitive effects. A guard ring around these connections, connected to the ground, is essential to avoid capturing unwanted noise, which can affect oscillation stability.   
Long tracks/paths behave as antennas for a given frequency spectrum, generating oscillation issues when passing EMI certification tests. Refer to Figure 14 and Figure 16.   
Any path conveying high-frequency signals must be routed away from the oscillator paths and components. Refer to Figure 14.   
The oscillator PCB must be underlined with a dedicated underneath ground plane, distinct from the application PCB ground plane. The oscillator ground plane should be connected to the nearest McuU/MPU ground. It prevents interferences between the oscillator components and other application components (for example, crosstalk between paths). If a crystal in a metallic package is used, do not connect it to the oscillator ground. Refer to Figure 13, Figure 14, and Figure 15.   
Leakage current can increase startup time and even prevent the oscillator start. If the device operates in a severe environment (high moisture/humidity ratio), an external coating is recommended.

![](images/f64045e9e733e1cc42bceb6eadbfc49cdaecae26eef33fa1e8cfe8d9943bb5af.jpg)  
Figure 13. Recommended layout for an oscillator circuit

# Warning:

It is highly recommended to apply conformal coatings to the PCB area shown in Figure 13, especially for the LSE quartz, CL1, CL2, and paths to the OSC_IN and OSC_OUT pads as a protection against moisture, dust, humidity, and temperature extremes that may lead to startup problems.

# 7.2 PCB design examples

Example 1

![](images/f33c977674eca67cfd9e04676d8be563f3c132031bffb378ed6cf749675c651b.jpg)  
Figure 14. PCB with separated GND plane and guard ring around the oscillator

![](images/eaa83e3f83cb1413ead0bc0aa74e75b6d65004fa52f31fdc7125fd417b2c2ef0.jpg)  
Figure 15. GND plane

![](images/e5122be158faf60f4e875a5083988f2bf05147f5ffce168f5d74caaff0b3bdfb.jpg)  
Figure 16. Signals around the oscillator

# Example 2

Figure 17 is an example of a PCB that does not respect the guidelines provided in Section 7.1, for the following reasons:

• no ground planes around the oscillator component • too long paths   
• no symmetry between oscillator capacitances • high crosstalk / coupling between paths   
• too many test points.

![](images/ec9c39f334c411086ec9481cb348f4c642b13cd521d6a54aa43bf8d6739a981d.jpg)

The PCB design has been improved according to the guidelines (see Figure 18):

• guard ring connected to the GND plane around the oscillator   
• symmetry between oscillator capacitances   
• less test points no coupling between paths.

![](images/b6ea92886401fe035a625886f1204ee9866776fcd2b76ec204cac4b1638c8d11.jpg)  
Figure 18. Final design (following guidelines)

![](images/baea3a5569086e1968213e4edf510b4284c519f672739383ebe951facf38fc10.jpg)  
Figure 19. GND plane

![](images/2a9b6d9c8bdcfc5ffa89864d16c2679f5f5778907306f18d1ad6e242246aaf17.jpg)  
Figure 20. Top layer view

# Example 3

Figure 21 is another example of PCB that does not respect the guidelines provided in Section 7.1 (EMC tests likely to fail):

• no guard ring around oscillator components long paths.

![](images/c2b7eacf6d16e2a23802e07ed47f7255746d23316e2eda049e251dc6a21dc1a4.jpg)  
Figure 21. PCB guidelines not respected

The layout has been improved to respect the guidelines (see Figure 22), EMC tests are likely to be passed:

• ground planes around the oscillator component • short paths that link the STM32 to the oscillator symmetry between oscillator capacitances.

![](images/7b862ca4b3004cc609171eebabf0e19f44d99fce6fbf0b67d2d7c324abf3eb70.jpg)  
Figure 22. PCB guidelines respected

# 7.3 Soldering guidelines

In general, soldering is a sensitive process, especially for low-frequency crystals. To reduce the impact of such process on the crystal parameters user should consider that

Exposing crystals to temperatures above their maximum ratings can damage the crystal and affect their ESR value. Refer to the crystal datasheet for the right reflow temperature curve (if not provided, ask the manufacturer).   
PCB cleaning is recommended to obtain the maximum performance by removing flux residuals from the board after assembly (even when using "no-clean" products in ultra-low power applications).

# 7.4 LSE sensitivity to PC13 activity

The OSC32_IN is sensitive to PC 13 activity, When PC13 is active (toggling) the LSE clock may shift, depending upon the LSE drive configuration. For example, using PC_13 as RTC_OUT calibration for 512 Hz or 1 Hz can disturb the LSE oscillation loop, hence shift the calibration frequency.

On products having the possibility to remap RTC_OUT on another pin (for example PB2), it is recommended to use this remapping to avoid LSE disturbances.

# 8 Reference documents

[] E. Vittoz High-Performance Crystal Oscillator Circuits: Theory and Application IEEE Journal of solid State Circuits, Vol 23, No 3, June 1988 pp 774 - 783.

# FAQs

# Question

How can I know if my crystal is compatible with a given STM32 part?

# Answer

Refer to Section 4: Guidelines to select a suitable crystal and external components.

# Question

Can I use a 32.768 kHz crystal compatible with STM32 parts but not mentioned in Table 7?

# Answer

Yes, you can. Table 7 is not exhaustive, it is given as a reference for some selected crystal manufacturers, footprint size, and crystal load capacitance.

# Question

In my application, 32.768 kHz frequency very-low drift and high accuracy are mandatory to obtain an accurate clock without calibration. Which crystal load capacitance (CL) should I choose?

# Answer

First, you must be sure that your crystal is compatible with the selected STM32 LSE. Then, it is highly recommended to use a crystal with low pullability, that is with C_ ≥ 6 pF:

• 7 pF is a good compromise between low drift and moderate power consumption • 9 and 12.5 pF can be used in noisy environments, but impact the power consumption.

# 10 Conclusion

The most important parameter is the gain margin of the oscilator, which determines if the oscillator starts up or not. This parameter must be calculated at the beginning of the design phase, to choose a crystal suitable for the application. The second parameter is the value of the external load capacitors, to select in accordance with the CL specification of the crystal (provided by the manufacturer). This determines the frequency accuracy. The third parameter is the value of the external resistor used to limit the drive level. In the 32 kHz oscillator part, however, it is not recommended to use an external resistor.

Because of the number of variables involved, in the experimentation phase it is recommended to select components that have exactly the same properties as those that will be used in production, and operate with the same oscillator layout and in the same environment, to avoid unexpected behavior.

Recently, MEMS oscillators have emerged on the market. They are a good alternative to resonators-based oscillators, thanks to their reduced power consumption, small size (they do not require additional passive components such as external load capacitors), and cost. This kind of oscillator is compatible with all STM32 MCUs/MPUs, except for the STM32F1 and STM32L1 series. When a MEMS oscillator is paired with an STM32 embedded oscillator, configure the latter in bypass mode.

# 11 Revision history

Table 12. Document revision history   

<table><tr><td colspan="1" rowspan="1">Date</td><td colspan="1" rowspan="1">Revision</td><td colspan="1" rowspan="1">Changes</td></tr><tr><td colspan="1" rowspan="1">20-Jan-2009</td><td colspan="1" rowspan="1">1</td><td colspan="1" rowspan="1">Initial release.</td></tr><tr><td colspan="1" rowspan="1">10-Nov-2009</td><td colspan="1" rowspan="1">2</td><td colspan="1" rowspan="1">DL formula corrected in Section 3.5.2: Another drive level measurementmethod.Package column added to all tables in Section 6: Some recommendedcrystals for STM32 microcontrollers.Recommended part numbers updated in Section 5.1: STM32-compatiblehigh-speed resonators.</td></tr><tr><td colspan="1" rowspan="1">27-Apr-2010</td><td colspan="1" rowspan="1">3</td><td colspan="1" rowspan="1">Added Section 7: Some recommended crystals for STM8A/Smicrocontrollers.</td></tr><tr><td colspan="1" rowspan="1">25-Nov-2010</td><td colspan="1" rowspan="1">4</td><td colspan="1" rowspan="1">Updated Section 5.1: STM32-compatible high-speed resonators:removed Table 7: Recommendable condition (for consumer) andTable 8: Recommendable condition (for CAN bus); added Table 8:Recommendable conditions (for consumer); updated Murata resonatorlink.Updated Section 5.1: STM32-compatible high-speed resonators:removed Table 13: EPSON TOYOCOM, Table 14: JFVNY®, andTable 15: KDS; Added Table 6: Recommendable crystals.Added Warning: after Figure 13.</td></tr><tr><td colspan="1" rowspan="1">30-Mar-2011</td><td colspan="1" rowspan="1">5</td><td colspan="1" rowspan="1">Section 5.1: STM32-compatible high-speed resonators: updated"STM32" with "STM8".Table 16: Recommendable conditions (for consumer): replaced ceramicresonator part number "CSTSE16M0G55A-RO" by"CSTCE16M0V53-RO".</td></tr><tr><td colspan="1" rowspan="1">17-Jul-2012</td><td colspan="1" rowspan="1">6</td><td colspan="1" rowspan="1">Whole document restricted to STM32 devices.</td></tr><tr><td colspan="1" rowspan="1">19-Sep-2014</td><td colspan="1" rowspan="1">7</td><td colspan="1" rowspan="1">Changed STM32F1 into STM32 throughout the document.Added STM8AL series in Table 1: Applicable products.Replace STM8 by STM32 in Section : and updated hyperlink.Added Section 7: Tips for improving oscillator stability.Remove section Some PCB hints.</td></tr><tr><td colspan="1" rowspan="1">19-Dec-2014</td><td colspan="1" rowspan="1">8</td><td colspan="1" rowspan="1">Updated Section 2: Oscillator theory.Updated Section 3: Pierce oscillator design. Renamed section "Gainmargin of the oscillator" into Section 3.4: Oscillator transconductanceand content updated. Updated Section 3.6: Startup time. UpdatedSection 3.7: Crystal pullability.Updated Section 4: Guidelines to select a suitable crystal and externalcomponents.Updated Section 5: Recommended resonators for STM32 MCUs/MPUs.Added Section 8: Reference documents.Updated Section 10: Conclusion.</td></tr><tr><td colspan="1" rowspan="1">19-Feb-2015</td><td colspan="1" rowspan="1">9</td><td colspan="1" rowspan="1">Updated Section 2.3: Negative-resistance oscillator principles to specifythe ratio between negative resistance and crystal ESR for STM8 andSTM32 microcontrollers.Added Section 3.8: Safety factor.Added Check the Safety Factor of the oscillation loop step in Section 4.2:How to select an STM32-compatible crystal. Note moved from step 2 to3 and updated.Renamed Table 7: Recommended crystal / MEMS resonators for theLSE oscillator in STM32 products.</td></tr><tr><td colspan="1" rowspan="1">17-Aug-2015</td><td colspan="1" rowspan="1">10</td><td colspan="1" rowspan="1">Updated Figure 12: Classification of low-speed crystal resonators.Added caution notes in Section 4.1: Low-speed oscillators embedded inSTM32 MCUs/MPUs.Added STM32F7, STM32F446xx, STM32F469/479xx and STM32L4microcontrollers in Table 5: LSE oscillators embedded into STM32MCUs/MPUs.Added STM32F411xx, STM32F446xx, STM32F469/479xx andSTM32L4xx microcontrollers in Table 6: HSE oscillators embedded inSTM32 MCUs/MPUs.Updated Table 7: Recommended crystal / MEMS resonators for the LSEoscillator in STM32 products.Added Section 9: FAQs.</td></tr><tr><td colspan="1" rowspan="1">31-May-2017</td><td colspan="1" rowspan="1">11</td><td colspan="1" rowspan="1">Updated document title, Introduction, Section 9: FAQs, Section 10:Conclusion, title of Section 6: Recommended crystals for STM8AF/AL/SMCUs, and revision of text across the whole document.Updated Table 5: LSE oscillators embedded into STM32 MCUs/MPUs,Table 6: HSE oscillators embedded in STM32 MCUs/MPUs and Table 7:Recommended crystal / MEMS resonators for the LSE oscillator inSTM32 products.Updated caption of Table 8: KYOCERA compatible crystals (notexhaustive list), and added Table 9: NDK compatible crystals (notexhaustive list).Updated Figure 12: Classification of low-speed crystal resonators.</td></tr><tr><td colspan="1" rowspan="1">21-Jan-2020</td><td colspan="1" rowspan="1">12</td><td colspan="1" rowspan="1">Updated document title, Section 2: Oscillator theory, Section 5.1:STM32-compatible high-speed resonators and Section 5.2: STM32-compatible low-speed resonators.Updated Table 1: Applicable products, Table 5: LSE oscillatorsembedded into STM32 MCUs/MPUs, Table 6: HSE oscillatorsembedded in STM32 MCUs/MPUs, Table 7: Recommended crystal /MEMS resonators for the LSE oscillator in STM32 products, Table 8:KYOCERA compatible crystals (not exhaustive list), Table 9: NDKcompatible crystals (not exhaustive list), Table 10: Recommendedconditions (for consumer) and Table 11: Recommended conditions (forCAN-BUS).Minor text edits across the whole document.</td></tr><tr><td colspan="1" rowspan="1">04-Dec-2020</td><td colspan="1" rowspan="1">13</td><td colspan="1" rowspan="1">Updated Table 7: Recommended crystal / MEMS resonators for the LSEoscillator in STM32 products and its footnotes 2 and 3.Updated footnotes of Table 5: LSE oscillators embedded into STM32MCUs/MPUs.Added Section 7.4: LSE sensitivity to PC13 activity.Minor text edits across the whole document.</td></tr><tr><td colspan="1" rowspan="1">27-Jul-2021</td><td colspan="1" rowspan="1">14</td><td colspan="1" rowspan="1">Updated Section 2.2: Transconductance, Section 3.4: Oscillatortransconductance, Section 4.2: How to select an STM32-compatiblecrystal and Section 5.1: STM32-compatible high-speed resonatorsAdded Section 3.9: Oscillation modes and its subsections.Updated Table 7: Recommended crystal / MEMS resonators for the LSEoscillator in STM32 products.Minor text edits across the whole document.</td></tr><tr><td colspan="1" rowspan="1">05-Oct-2021</td><td colspan="1" rowspan="1">15</td><td colspan="1" rowspan="1">Added notes in Section 3.5.2: Another drive level measurement method,Section 5.2: STM32-compatible low-speed resonators and Section 6.1:Part numbers of recommended crystal oscillators.Added footnote 4 to Table 5: LSE oscillators embedded into STM32MCUs/MPUs.Updated Table 6: HSE oscillators embedded in STM32 MCUs/MPUs,Table 7: Recommended crystal / MEMS resonators for the LSE oscillatorin STM32 products and Table 9: NDK compatible crystals (notexhaustive list).Minor text edits across the whole document.</td></tr><tr><td colspan="1" rowspan="1">22-Aug-2022</td><td colspan="1" rowspan="1">16</td><td colspan="1" rowspan="1">Updated Table 1: Applicable products, Table 5: LSE oscillatorsembedded into STM32 MCUs/MPUs, Table 7: Recommended crystal /MEMS resonators for the LSE oscillator in STM32 products, and Table 9:NDK compatible crystals (not exhaustive list).Updated Section 6.1: Part numbers of recommended crystal oscillators.Minor text edits across the whole document.</td></tr><tr><td colspan="1" rowspan="1">19-Jan-2023</td><td colspan="1" rowspan="1">17</td><td colspan="1" rowspan="1">Updated Table 5: LSE oscillators embedded into STM32 MCUs/MPUs,Table 6: HSE oscillators embedded in STM32 MCUs/MPUs, and Table 7:Recommended crystal / MEMS resonators for the LSE oscillator inSTM32 products.Minor text edits across the whole document.</td></tr><tr><td colspan="1" rowspan="1">25-Jan-2023</td><td colspan="1" rowspan="1">18</td><td colspan="1" rowspan="1">Updated Table 5: LSE oscillators embedded into STM32 MCUs/MPUs,Table 6: HSE oscillators embedded in STM32 MCUs/MPUs, and Table 7:Recommended crystal / MEMS resonators for the LSE oscillator inSTM32 products.Minor text edits across the whole document.</td></tr><tr><td colspan="1" rowspan="1">03-Apr-2023</td><td colspan="1" rowspan="1">19</td><td colspan="1" rowspan="1">Updated Table 5: LSE oscillators embedded into STM32 MCUs/MPUsand Table 7: Recommended crystal / MEMS resonators for the LSEoscillator in STM32 products.Updated Note: in Section 5.2: STM32-compatible low-speed resonators.</td></tr><tr><td colspan="1" rowspan="1">21-Mar-2024</td><td colspan="1" rowspan="1">20</td><td colspan="1" rowspan="1">Updated document title.Updated Table 5: LSE oscillators embedded into STM32 MCUs/MPUs,Table 6: HSE oscillators embedded in STM32 MCUs/MPUs, and Table 7:Recommended crystal / MEMS resonators for the LSE oscillator inSTM32 products.Updated footnote a.Updated Section 7.1: PCB design guidelines.Minor text edits across the whole document.</td></tr><tr><td colspan="1" rowspan="1">14-May-2024</td><td colspan="1" rowspan="1">21</td><td colspan="1" rowspan="1">Updated Section 5.1: STM32-compatible high-speed resonators andfootnote a.Updated Table 5: LSE oscillators embedded into STM32 MCUs/MPUsand Table 7: Recommended crystal / MEMS resonators for the LSEoscillator in STM32 products.Updated Figure 10: Quartz crystal theoretical model with third overtone.Minor text edits across the whole document.</td></tr><tr><td colspan="1" rowspan="1">12-Nov-2024</td><td colspan="1" rowspan="1">22</td><td colspan="1" rowspan="1">Updated Section 3.5.3: Calculating the external resistor.Updated Table 5: LSE oscillators embedded into STM32 MCUs/MPUs,Table 6: HSE oscillators embedded in STM32 MCUs/MPUs, and Table 7:Recommended crystal / MEMS resonators for the LSE oscillator inSTM32 products.</td></tr><tr><td colspan="1" rowspan="1">28-Jan-2025</td><td colspan="1" rowspan="1">23</td><td colspan="1" rowspan="1">Introduced STM32U3 series, hence updated Table 5: LSE oscillatorsembedded into STM32 MCUs/MPUs, Table 6: HSE oscillatorsembedded in STM32 MCUs/MPUs, and Table 7: Recommended crystal /MEMS resonators for the LSE oscillator in STM32 products.</td></tr></table>

# IMPORTANT NOTICE  READ CAREFULLY

acknowledgment.

the design of purchasers' products.

No license, express or implied, to any intellectual property right is granted by ST herein.

or service names are the property of their respective owners.

I