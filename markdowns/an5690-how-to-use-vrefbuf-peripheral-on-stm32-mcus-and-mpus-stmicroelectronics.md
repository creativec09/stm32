# How to use VREFBUF peripheral on STM32 MCUs and MPUs

# Introduction

o used:

As an internal voltage reference, for peripherals like ADC or DAC

As an external voltage reference, through the VREF+ pin.

variations, supply variations, or product lifetime.

The VREFBUF peripheral has several features like:

Output voltage reference scale selection   
Output voltage reference Tuning/trimming   
Output mode control in order to use an internal or external reference.

within the application environment including the current load on VREF+.

Table 1. Applicable products   

<table><tr><td rowspan=13 colspan=1>TypeMicrocontrollers</td><td rowspan=1 colspan=1>Product series/lines (1)</td></tr><tr><td rowspan=1 colspan=1>STM32G0 series</td></tr><tr><td rowspan=1 colspan=1>STM32G4 series</td></tr><tr><td rowspan=1 colspan=1>STM32H5 series</td></tr><tr><td rowspan=1 colspan=1>STM32H7 series</td></tr><tr><td rowspan=1 colspan=1>STM32L4 series</td></tr><tr><td rowspan=1 colspan=1>STM32L4+ series</td></tr><tr><td rowspan=1 colspan=1>STM32L5 series</td></tr><tr><td rowspan=1 colspan=1>STM32U0 series</td></tr><tr><td rowspan=1 colspan=1>STM32U3 series</td></tr><tr><td rowspan=1 colspan=1>STM32U5 series</td></tr><tr><td rowspan=1 colspan=1>STM32WBx5 line</td></tr><tr><td rowspan=1 colspan=1>STM32WL series</td></tr><tr><td rowspan=1 colspan=1>Microprocessors</td><td rowspan=1 colspan=1>STM32MP1 series</td></tr></table>

1This application note only applies to products with: - Presence of a VREFBUF peripheral - VREF+ pin not internally connected to VDD or VDDA Refer to product datasheet.

# 1 General information

# Note:

This document applies to STM32 Arm®-based microprocessors and microcontrollers. Arm is a registered trademark of Arm Limited (or its subsidiaries) in the US and/or elsewher

# arm

# 2 VREFBUF peripheral principle

The VREFBUF peripheral is a low-drop output regulator powered by the analog supply VDDA. The VREFBUF output is always connected to the VREF+ pin and the associated external capacitors C1 and C2. The VREFBUF output and the VREF+ are always connected internally to the DAC and the ADC reference inputs. There are several output voltage scales available (depending on STM32 series) which can be fine-adjusted by the application with the peripheral bit registers (some scales are calibrated/trimmed during factory test).

# Note:

The VREF+ pin is double-bonded with VDDA on some packages. In these packages the internal voltage reference buffer is not available.

![](images/85fd6f2e8f0cf754d351c7f7f4a7548106339681dc501c2569d88f795969b6cd.jpg)  
Figure 1. STM32 VREBUF peripheral simplified schematic

# 2.1

# Principle and circuitry

Te VRoulaiasn gulatn o wiplili t ouolu the Bandgap voltage and the R1/R2 resistors according to the following formula:

![](images/c8c60ef429b25c55d96f8b278a30af34728352e84aa34c12b9bd1880cea78dcc.jpg)

Teesistorsvariablenorder o provide he followigfeatur:utput scalselecton andtrii.

![](images/cae36540320ecafe3a0b311ed6fba2b3f91956ffecbfa995cc2b8b96c2b34239.jpg)  
Figure 2. VREFBUF peripheral simplified principle

For example: the VREFBUF of the STM32G4 seris supports hreevoltage scales:2.048 V, 2.500 V, and 2.900 V. The outpu voltage elecion is perormed by changing theRresistorvalue.The election ofhe1 valu performed with the VREFBUF register configuration. Considering VREFBUF bandgap voltage equals to 1.25 V, the following table shows the relationship between VREFBUFoutput voltage, Bandgap, and R1/R2 resistors for the STM32G4 series.

Table 2. STM32G4 series VREFBUF output with R1 and R2 resistors example   

<table><tr><td colspan="1" rowspan="1">VREFBUF output voltageon VREF+ pin</td><td colspan="1" rowspan="1">Bandgap</td><td colspan="1" rowspan="1">R1/R2 ratio</td><td colspan="1" rowspan="1">R1(kΩ) / R2(kΩ)</td></tr><tr><td colspan="1" rowspan="1">2.048 V</td><td colspan="1" rowspan="1">1.25 V</td><td colspan="1" rowspan="1">0.6384</td><td colspan="1" rowspan="1">127.68 / 200</td></tr><tr><td colspan="1" rowspan="1">2.500 V</td><td colspan="1" rowspan="1">1.25 V</td><td colspan="1" rowspan="1">1</td><td colspan="1" rowspan="1">200 / 200</td></tr><tr><td colspan="1" rowspan="1">2.900 V</td><td colspan="1" rowspan="1">1.25 V</td><td colspan="1" rowspan="1">1.32</td><td colspan="1" rowspan="1">264 /200</td></tr></table>

# 2.2

# Peripheral functional modes and status

The VREFBUF peripheral has several control bit registers available: ENVR, HIZ, VRS, VRR, and TRIM. The following paragraphs describe the behavior change on the peripheral.

# 2.2.1

# ENVR and HIZ bits

ENVR bit: simply enables or disables the VREFBUF peripheral.   
HIZ bit: enables or disables the VREFBUF output high impedance.

The following table describes the VREFBUF peripheral behavior with ENVR/HIZ bits.

Table 3. VREFBUF peripheral behavior with ENVR/HIZ bits   

<table><tr><td rowspan=1 colspan=1>ENVR</td><td rowspan=1 colspan=1>HIZ</td><td rowspan=1 colspan=1>Mode</td><td rowspan=1 colspan=1>Description</td></tr><tr><td rowspan=2 colspan=1>0</td><td rowspan=1 colspan=1>0</td><td rowspan=1 colspan=1>Pull-down</td><td rowspan=1 colspan=1>VREFBUF is disabled, VREF+ pin is pulled down to VsSA.</td></tr><tr><td rowspan=1 colspan=1>1</td><td rowspan=1 colspan=1>External voltage reference</td><td rowspan=1 colspan=1>VREFBUF is disabled, VREF+ is an input floating pin. An external referencevoltage can be connected for analog peripherals usage.</td></tr><tr><td rowspan=2 colspan=1>1</td><td rowspan=1 colspan=1>0</td><td rowspan=1 colspan=1>VREFBUF voltage reference</td><td rowspan=1 colspan=1>VREFBUF is enabled and buffering VREF+ pin with VREFBUF_OUTvoltage.</td></tr><tr><td rowspan=1 colspan=1>1</td><td rowspan=1 colspan=1>VREFBUF hold</td><td rowspan=1 colspan=1>VREFBUF is enabled without output buffer. Voltage on the VREF+ pin isheld with the external capacitor. This is reducing VREFBUF powerconsumption.</td></tr></table>

# 2.2.2 VRS bits

VRS bits: select the VREFBUF_OUT voltage reference scale.

The following table lists the available VREFBUFoutput voltage scales for several TM32 series. The VRS size depends on the STM32 series.

Table 4. Example of VREFBUF output voltage per STM32 series   

<table><tr><td rowspan=2 colspan=1>STM32 series</td><td rowspan=2 colspan=1>VRSsize (bits)</td><td rowspan=1 colspan=6>Available VREFBUF output voltage scale (1) (2)</td></tr><tr><td rowspan=1 colspan=1>1.5 V</td><td rowspan=1 colspan=1>1.8 V</td><td rowspan=1 colspan=1>2 V</td><td rowspan=1 colspan=1>2.5 V</td><td rowspan=1 colspan=1>2.9 V</td><td rowspan=1 colspan=1></td></tr><tr><td rowspan=1 colspan=1>STM32G0</td><td rowspan=1 colspan=1>1</td><td rowspan=1 colspan=1></td><td rowspan=1 colspan=1></td><td rowspan=1 colspan=1>O</td><td rowspan=1 colspan=1>0</td><td rowspan=1 colspan=1></td><td rowspan=1 colspan=1></td></tr><tr><td rowspan=1 colspan=1>STM32G4</td><td rowspan=1 colspan=1>2</td><td rowspan=1 colspan=1></td><td rowspan=1 colspan=1></td><td rowspan=1 colspan=1>0</td><td rowspan=1 colspan=1>O</td><td rowspan=1 colspan=1>O</td><td rowspan=1 colspan=1></td></tr><tr><td rowspan=1 colspan=1>STM32H5</td><td rowspan=1 colspan=1>3</td><td rowspan=1 colspan=1></td><td rowspan=1 colspan=1>0</td><td rowspan=1 colspan=1>0</td><td rowspan=1 colspan=1>O</td><td rowspan=1 colspan=1></td><td rowspan=1 colspan=1></td></tr><tr><td rowspan=1 colspan=1>STM32H7</td><td rowspan=1 colspan=1>3</td><td rowspan=1 colspan=1>O</td><td rowspan=1 colspan=1>0</td><td rowspan=1 colspan=1>0</td><td rowspan=1 colspan=1>0</td><td rowspan=1 colspan=1></td><td rowspan=1 colspan=1></td></tr><tr><td rowspan=1 colspan=1>STM32L4</td><td rowspan=1 colspan=1>1</td><td rowspan=1 colspan=1></td><td rowspan=1 colspan=1></td><td rowspan=1 colspan=1>0</td><td rowspan=1 colspan=1>0</td><td rowspan=1 colspan=1></td><td rowspan=1 colspan=1></td></tr><tr><td rowspan=1 colspan=1>STM32L4+</td><td rowspan=1 colspan=1>1</td><td rowspan=1 colspan=1></td><td rowspan=1 colspan=1></td><td rowspan=1 colspan=1>O</td><td rowspan=1 colspan=1>O</td><td rowspan=1 colspan=1></td><td rowspan=1 colspan=1></td></tr><tr><td rowspan=1 colspan=1>STM32L5</td><td rowspan=1 colspan=1>1</td><td rowspan=1 colspan=1></td><td rowspan=1 colspan=1></td><td rowspan=1 colspan=1>0</td><td rowspan=1 colspan=1>O</td><td rowspan=1 colspan=1></td><td rowspan=1 colspan=1></td></tr><tr><td rowspan=1 colspan=1>STM32U0</td><td rowspan=1 colspan=1>1</td><td rowspan=1 colspan=1></td><td rowspan=1 colspan=1></td><td rowspan=1 colspan=1>0</td><td rowspan=1 colspan=1>O</td><td rowspan=1 colspan=1></td><td rowspan=1 colspan=1></td></tr><tr><td rowspan=1 colspan=1>STM32U5</td><td rowspan=1 colspan=1>3</td><td rowspan=1 colspan=1>O</td><td rowspan=1 colspan=1>0</td><td rowspan=1 colspan=1>0</td><td rowspan=1 colspan=1>0</td><td rowspan=1 colspan=1></td><td rowspan=1 colspan=1></td></tr><tr><td rowspan=1 colspan=1>STM32WB</td><td rowspan=1 colspan=1>1</td><td rowspan=1 colspan=1></td><td rowspan=1 colspan=1></td><td rowspan=1 colspan=1>O</td><td rowspan=1 colspan=1>0</td><td rowspan=1 colspan=1></td><td rowspan=1 colspan=1></td></tr><tr><td rowspan=1 colspan=1>STM32WLE/5</td><td rowspan=1 colspan=1>1</td><td rowspan=1 colspan=1></td><td rowspan=1 colspan=1></td><td rowspan=1 colspan=1>0</td><td rowspan=1 colspan=1>0</td><td rowspan=1 colspan=1></td><td rowspan=1 colspan=1></td></tr><tr><td rowspan=1 colspan=1>STM32MP1</td><td rowspan=1 colspan=1>3</td><td rowspan=1 colspan=1>0</td><td rowspan=1 colspan=1>0</td><td rowspan=1 colspan=1>O</td><td rowspan=1 colspan=1>0</td><td rowspan=1 colspan=1></td><td rowspan=1 colspan=1></td></tr></table>

O = available VREFBUF output voltage.

# Refer to the product datasheet for VREFBUF output voltage scale accuracy.

Table 5. STM32G4 series VREFBUF output voltage with VRS value   

<table><tr><td rowspan=1 colspan=1>STM32 series</td><td rowspan=1 colspan=1>VRS[1:0]</td><td rowspan=1 colspan=1>VREFBUF output voltageon VREF+ pin</td></tr><tr><td rowspan=3 colspan=1>STM32G4</td><td rowspan=1 colspan=1>00</td><td rowspan=1 colspan=1>2.048 V</td></tr><tr><td rowspan=1 colspan=1>01</td><td rowspan=1 colspan=1>2.500 V</td></tr><tr><td rowspan=1 colspan=1>10</td><td rowspan=1 colspan=1>2.900 V</td></tr></table>

# 2.2.3 VRR

VRR bit (voltage reference ready) is set when the VREFBUF output voltage accuracy is within 1% of the selected voltage range. When the HIZ bit is set, the VRR is stuck at 1 and therefore it is up to the application to ensure that the VREFBUF_OUT voltage remains in the selected scale voltage limits.

# 2.2.4 TRIM

• TRIM bits control the VREFBUF adjustable trimming code.

# 3 VREFBUF constraints in application

The following sections describe the application constraints when VREFBUF is used.

# 3.1 VREFBUF trimming circuitry

STM32 peripherals like the ADC or the OPAMP may embed a self-calibration circuitry but some others like internal oscillators or VREFBUF require a measured trimming performed during the factory process.

A par uvoltaeorheVREBU asis ustb asn  regi wr value. The VREFBUF output voltage is trimmed at factory with different conditions depending on the STM32 series. The product datasheet provides the trimming temperature and voltage range details.

Iniorul isthemedian codeEachtriming register ep changes thetrime parameter wi  given resolution . For example, the VREFBUF typical trimming step is ± 0.05% equivalent to 1.25 mV when VREFBUF output is 2.5 V V trimming step.

The VREFBUF trimming operation needs the following steps to be completed:

1Set median code value in the TRIM register and measure the VREFBUF output.   
Calculatehe ffence betweeheeasvoltageand he argetvoltagalculat he steps to apply. aTrim code to apply = median code - round nearest (∆V / typical trim step voltage)   
plyeus eaiVREBuoltf ttriimming.

The following table provides trimming operation steps examples.

Table 6. Trimming operation example for STM32G4 2.5 V VREFBUF output voltage   

<table><tr><td rowspan=2 colspan=1>Example</td><td rowspan=1 colspan=3>Trimming step 1</td><td rowspan=1 colspan=3>Trimming step 2</td><td rowspan=1 colspan=3>Trimming step 3</td><td rowspan=1 colspan=2>Trimming results</td></tr><tr><td rowspan=1 colspan=1>Initialtrimmingcode</td><td rowspan=1 colspan=1>InitialVoltage(mV)</td><td rowspan=1 colspan=2>ΔV vs 2.5 V(mV)</td><td rowspan=1 colspan=1>Trimmingstepcorrection</td><td rowspan=1 colspan=2>Adjusted trimmingcode</td><td rowspan=1 colspan=1>TrimmedVoltage(mV)</td><td rowspan=1 colspan=2>VoltageAccuracy(mV)</td><td rowspan=1 colspan=1>TrimmingcodeAccuracy</td></tr><tr><td rowspan=1 colspan=1>#1</td><td rowspan=1 colspan=1>32</td><td rowspan=1 colspan=1>2503.83</td><td rowspan=1 colspan=2>3.83</td><td rowspan=1 colspan=1>-3</td><td rowspan=1 colspan=2>29</td><td rowspan=1 colspan=1>2500.08</td><td rowspan=1 colspan=2>0.08</td><td rowspan=1 colspan=1>0.06</td></tr><tr><td rowspan=1 colspan=1>#2</td><td rowspan=1 colspan=1>32</td><td rowspan=1 colspan=1>2498.28</td><td rowspan=1 colspan=2>-1.72</td><td rowspan=1 colspan=1>1</td><td rowspan=1 colspan=2>33</td><td rowspan=1 colspan=1>2499.53</td><td rowspan=1 colspan=2>-0.47</td><td rowspan=1 colspan=1>-0.38</td></tr><tr><td rowspan=1 colspan=1>#3</td><td rowspan=1 colspan=1>32</td><td rowspan=1 colspan=1>2503.88</td><td rowspan=1 colspan=2>3.88</td><td rowspan=1 colspan=1>-3</td><td rowspan=1 colspan=2>29</td><td rowspan=1 colspan=1>2500.13</td><td rowspan=1 colspan=2>0.13</td><td rowspan=1 colspan=1>0.10</td></tr><tr><td rowspan=1 colspan=1>#4</td><td rowspan=1 colspan=1>32</td><td rowspan=1 colspan=1>2497.53</td><td rowspan=1 colspan=2>-2.47</td><td rowspan=1 colspan=1>2</td><td rowspan=1 colspan=2>34</td><td rowspan=1 colspan=1>2500.03</td><td rowspan=1 colspan=2>0.03</td><td rowspan=1 colspan=1>0.03</td></tr><tr><td rowspan=1 colspan=1>#5</td><td rowspan=1 colspan=1>32</td><td rowspan=1 colspan=1>2491.42</td><td rowspan=1 colspan=2>-8.58</td><td rowspan=1 colspan=1>7</td><td rowspan=1 colspan=2>39</td><td rowspan=1 colspan=1>2500.17</td><td rowspan=1 colspan=2>0.17</td><td rowspan=1 colspan=1>0.14</td></tr><tr><td rowspan=1 colspan=1>#6</td><td rowspan=1 colspan=1>32</td><td rowspan=1 colspan=1>2498.85</td><td rowspan=1 colspan=2>-1.15</td><td rowspan=1 colspan=1>1</td><td rowspan=1 colspan=2>33</td><td rowspan=1 colspan=1>2500.10</td><td rowspan=1 colspan=2>0.10</td><td rowspan=1 colspan=1>0.08</td></tr></table>

# 3.2

# VREFBUF trimming with an external voltage and ADC

The VREFBUF output can be trimmed with the ADC peripheral and an external accurate voltage source. When the VREFBUF is used as ADC reference, here is a proportionallinear factor between the ADC iput voltae and the ADC digital output:

![](images/3cf769ab71c12b8feaee9df64e1fcb421d46619a8459e6df4909d9793a1146a6.jpg)

For eampl, sing .800 V isapli at heinput f the ADC, producing a diitaloutput  961 LSB, e VREFBUF voltage is calculated as follows:

![](images/ca4fc583e98d2b250093b2d7f2e8552e6a00de54dc6c5bf35d662dbf1ab01984.jpg)

There is no trimming correction to apply because the VREFBUF output is only 3.3 mV away from 2.5 V.

It ntplyolual zeDCoweADC a should be considered as well. The offset error can be canceled and the VREFBUF estimation improved by peoing equsiton  u vlg.Teollowig abl prent eccrac oanc method using various input voltage configurations.

Table 5 STM32 ADC digital output code /VREFBUF estimation

Table 7. STM32 ADC digital output code /VREFBUF estimation   

<table><tr><td rowspan=1 colspan=1>Method</td><td rowspan=1 colspan=1>Input voltage(V)</td><td rowspan=1 colspan=1>ADC condition</td><td rowspan=1 colspan=1>ADCdigital output(LSB)</td><td rowspan=1 colspan=1>VREFBUFvoltageestimation(V)</td><td rowspan=1 colspan=1>Estimation error(mV)(real VREFBUF =2.051 V</td></tr><tr><td rowspan=2 colspan=1>Single point</td><td rowspan=1 colspan=1>0.1</td><td rowspan=3 colspan=1>Theorical</td><td rowspan=1 colspan=1>200</td><td rowspan=1 colspan=1>2.048</td><td rowspan=1 colspan=1>3</td></tr><tr><td rowspan=1 colspan=1>1.8</td><td rowspan=1 colspan=1>3595</td><td rowspan=1 colspan=1>2.0508</td><td rowspan=1 colspan=1>0.15</td></tr><tr><td rowspan=1 colspan=1>Two points</td><td rowspan=1 colspan=1>1.8 - 0.1 = 1.7</td><td rowspan=1 colspan=1>3595-200 = 3395</td><td rowspan=1 colspan=1>2.051</td><td rowspan=1 colspan=1>0.016</td></tr><tr><td rowspan=2 colspan=1>single point</td><td rowspan=1 colspan=1>0.1</td><td rowspan=3 colspan=1>ADC offset error=2 LSBADC gain error 2.5 LSB</td><td rowspan=1 colspan=1>202</td><td rowspan=1 colspan=1>2.0277</td><td rowspan=1 colspan=1>23.3</td></tr><tr><td rowspan=1 colspan=1>1.8</td><td rowspan=1 colspan=1>3599</td><td rowspan=1 colspan=1>2.0486</td><td rowspan=1 colspan=1>2.43</td></tr><tr><td rowspan=1 colspan=1>Two points</td><td rowspan=1 colspan=1>1.8 - 0.1 = 1.7</td><td rowspan=1 colspan=1>3599-202 = 3397</td><td rowspan=1 colspan=1>2.04981</td><td rowspan=1 colspan=1>1.2</td></tr></table>

Iner t emosacratan f VREBUFolage TMADC igial utu, us  input voltage points to minimize the ADC offet error and achieve more accurate VREFBUF voltage calculation results.

# 3.3

# VREFBUF trimming with the internal VREFINT voltage and the ADC

Another interesting method mprove he VREFBUF trimin is t use he VREFINT caliration (VREFINT_CAL) C phDur  s Fl  o given reference (VREF+ = 3.0 V ± 10m V for STM32G4 series) and a given temperature (30° ± 5°C for STM32G4 series).

One can calculate the VREFBUF voltage value directly from the following procedure:

Retrieve the VREFINT conversion value result at VREFINT_CAL address:

a.The conversion value is Ox067B or 1659 in decimal bThe equivalent voltage is 1659 × (3 V/212 ) = 1.2151 V with factory conditions (3 V and 30°C)

Configure the 2-bit ADC peripheral and acquire the VREFINT voltage while VREFBUF is the ADC reference.

Retrieve the VREFINT average conversion value:

a.The average conversion value is 1989.2 (10 acquisition samples) 0x067B or 1659 in decimal bCalculating VREFBUF voltage from the equation: 1989.2 × (VREFBUF/212 ) = 1.2151 V C. VREFBUF = (1.2151/1989.2) × 212 = 2.5020 V

With ths mplewa peratin, heVREFBUF voltage can be sply retrivd usig heADC perheala the VREFINT calibrated input.

# Minimum VDDA supply voltage

TVREBU phe cuias  owrovoltaeulatoeroally  pro ut, eVREB plyvoltus  ih illio nominal value. When the supply voltage drops under the minimum supply margin, the VREFBUF operates in degraded mode and the VREFBUF output voltage follows the VDDA supply drop. The minimum voltage margin The following table presents the degraded mode parameter for STM32G4 series when VREFBUF output is 2.5 V and according to VDDA supply variations and output current load.

Table 8. VREFBUF degraded mode example   

<table><tr><td rowspan=1 colspan=1>VREFBUF supply</td><td rowspan=1 colspan=1>VREFBUF OUTPUT (VRS = 1)</td><td rowspan=1 colspan=1>Operation mode</td></tr><tr><td rowspan=1 colspan=1>1.65 V ≤ VDDA ≤ 2.8 V</td><td rowspan=1 colspan=1>min(VDDA - 250 mV, 2.5 V)</td><td rowspan=1 colspan=1>Degraded</td></tr><tr><td rowspan=1 colspan=1>VDDA ≥ 2.8 V</td><td rowspan=1 colspan=1>2.5 V</td><td rowspan=1 colspan=1>Normal</td></tr></table>

# 3.5

# VREFBUF output decreases when VRS changes

RBU dea wiVRrant  pwi eolatta e accurate output voltage:

Dsable REFBUF wit HIZ = har tage n VREF+ith he VREFBUVA pulldown.   
Configure the VRS register value.   
Enable the VREFBUF with HIZ = 1 and monitor the VRR bit status until the output reaches the requested level.

# 4 VREFBUF application examples

The following section describes analog oriented applications using the VREFBUF reference peripheral with analog-to-digital converter (ADC), digital-to-analog converter (DAC) or a resistor voltage divider.

# 4.1

# VREFBUF used as ADC reference for analog signal acquisition

Converting an analog signal to digital values with the ADC requires an accurate analog reference voltge to liWlvol eatiplitefiantealnte

The quantization ste formula i VREF/2 where  is the number of bit of the ADC. For example, an ADC with 1.8 V reference voltage and 16-bit resolution: quantization step = 1.8 V/216 = 27.466 μV.

The following figure shows this behavior for a 3-bit ADC, VREF = 1.8 V and a quantization step = 225 mV. Wher tepuvultenizatiheigi vlwhen voltage decreases over a multiple of the quantization step, the digital value is decreased.

![](images/7258314284a633ea896b31c0e08c3848f1d430c945c52db95c3035eb332e7ff5.jpg)  
Figure 3. ADC 3-bit quantization step example

Forhi pliation case,he ADC eerenc VREF+ pi) is ntenally coeo he VREFBUF utut external connection between pins is required. Only external capacitors are required on VREF+ pin.

# VREFBUF used as DAC reference for signal generation application

The DAC perheral useo generate analog ignals fromdigtal values.Ashe ADC principle a quantat saplitu oltage (VREF/ = 1.8 V/ = 7.03 mor 8-it AC) is u cnvert a igal valu al henaomTe uantzationplitcufomheAeerencvo and the DAC bit resolution.

![](images/9d373ad0983d68d2c13ef52232c648692e0addae3761f46ea433a324672269f1.jpg)  
Figure 4. DAC 8-bit quantization step example

Forhi pliton case,he DAC eeec VREF+ pi) istenally o he VREFBUFutut external connection between pins is required.

# VREFBUF used as voltage reference with a voltage divider

T whl hn mA).Other eferencevoltage values could bebtain usiga voltagebrigedivier connected the REF+ pin.

The following schematic shows how to build a 1 V reference voltage from VREFBUF/VREF+ pin. A simple voltage dividercircuity with two resistors isused to obtain the desired 1Vreference voltage

![](images/6ad4da35fc2484b1379ef75a3a32dfc4ce77c47c31aeaa8119e7f74d7e5ef0f5.jpg)

![](images/63a0ecc63a6428320e2d1973153de6e895baaf78188e857029013934b7455213.jpg)  
Figure 5. 1 V reference voltage from VREFBUF divided

T rsor riividerdng he REFBUFutu and heum VREFBUF loa pably houl e respeted. With this example, the static current load is 0.415 mA = 2.5 V / (3600 + 2400). In STM32G4 sris is correct.

# VREFBUF used as voltage reference with thermal sensor

AVRagelativheal  uplt motherboards, rheating/coolng systes.This temperature sensor circuit could simply consist a volage divider between a resistor and a negative-temperature-coefficient thermistor (NTC). When the temperature is increasing, the NTC thermistor impedance is decreasing.

![](images/83d1191a6e2627dffeffb5d3b1041699e2ba19a4df9e66cb1433513559b5c606.jpg)  
Figure 6. Example of a generic NTC thermistor impedance versus temperature

![](images/3143291046deab44a4d4c180ba08097ea4f4f41c96eccd25e7ef13e4af0cc4c9.jpg)  
Figure 7. NTC thermistor voltage divider with VREFBUF peripheral

Icoects heempeaturevoltage sigal  an TM32 -t ADCiput, he olloig able ere e digitalized temperature characteristic values (ADC VREF is VREFBUF = 2.5 V).

Table 9. Temperature/STM32 12-bit ADC code summary   

<table><tr><td rowspan=1 colspan=1>T</td><td rowspan=1 colspan=1>NTC1(Ω)</td><td rowspan=1 colspan=1>R1(Ω)</td><td rowspan=1 colspan=1>Temperature voltage (mV)</td><td rowspan=1 colspan=1>STM3212-bit ADC code</td></tr><tr><td rowspan=1 colspan=1>-40</td><td rowspan=1 colspan=1>114943.3</td><td rowspan=1 colspan=1>5000</td><td rowspan=1 colspan=1>2395.784</td><td rowspan=1 colspan=1>3925</td></tr><tr><td rowspan=1 colspan=1>-25</td><td rowspan=1 colspan=1>58524.1</td><td rowspan=1 colspan=1>5000</td><td rowspan=1 colspan=1>2303.224</td><td rowspan=1 colspan=1>3773</td></tr><tr><td rowspan=1 colspan=1>-10</td><td rowspan=1 colspan=1>29797.9</td><td rowspan=1 colspan=1>5000</td><td rowspan=1 colspan=1>2140.783</td><td rowspan=1 colspan=1>3507</td></tr><tr><td rowspan=1 colspan=1>5</td><td rowspan=1 colspan=1>15171.8</td><td rowspan=1 colspan=1>5000</td><td rowspan=1 colspan=1>1880.323</td><td rowspan=1 colspan=1>3080</td></tr><tr><td rowspan=1 colspan=1>20</td><td rowspan=1 colspan=1>7724.8</td><td rowspan=1 colspan=1>5000</td><td rowspan=1 colspan=1>1517.666</td><td rowspan=1 colspan=1>2486</td></tr><tr><td rowspan=1 colspan=1>35</td><td rowspan=1 colspan=1>3933.1</td><td rowspan=1 colspan=1>5000</td><td rowspan=1 colspan=1>1100.71</td><td rowspan=1 colspan=1>1803</td></tr><tr><td rowspan=1 colspan=1>50</td><td rowspan=1 colspan=1>2002.6</td><td rowspan=1 colspan=1>5000</td><td rowspan=1 colspan=1>714.9487</td><td rowspan=1 colspan=1>1171</td></tr><tr><td rowspan=1 colspan=1>65</td><td rowspan=1 colspan=1>1019.6</td><td rowspan=1 colspan=1>5000</td><td rowspan=1 colspan=1>423.4501</td><td rowspan=1 colspan=1>693</td></tr><tr><td rowspan=1 colspan=1>80</td><td rowspan=1 colspan=1>519.2</td><td rowspan=1 colspan=1>5000</td><td rowspan=1 colspan=1>235.179</td><td rowspan=1 colspan=1>385</td></tr><tr><td rowspan=1 colspan=1>95</td><td rowspan=1 colspan=1>264.3</td><td rowspan=1 colspan=1>5000</td><td rowspan=1 colspan=1>125.5153</td><td rowspan=1 colspan=1>205</td></tr><tr><td rowspan=1 colspan=1>110</td><td rowspan=1 colspan=1>134.6</td><td rowspan=1 colspan=1>5000</td><td rowspan=1 colspan=1>65.53578</td><td rowspan=1 colspan=1>107</td></tr><tr><td rowspan=1 colspan=1>125</td><td rowspan=1 colspan=1>68.5</td><td rowspan=1 colspan=1>5000</td><td rowspan=1 colspan=1>33.78712</td><td rowspan=1 colspan=1>55</td></tr></table>

can estimate the actual temperature value from the ADC code with the help  a polynomial calculation.

= C+C1AC+ ×A+

![](images/1dcb9df1a64a85d087c0e3e19436e9952a8944d80d7b77578345518c51bc3dbc.jpg)  
Figure 8. Table results and estimation curve from ADC code with a polynomial interpolation

The previous interpolation curve is obtained with the following coefficients:

Table 10. Polynomial coefficients of the interpolation function   

<table><tr><td rowspan=1 colspan=1>CO</td><td rowspan=1 colspan=1>C1</td><td rowspan=1 colspan=1>C2</td><td rowspan=1 colspan=1>C3</td><td rowspan=1 colspan=1>C4</td><td rowspan=1 colspan=1>C5</td></tr><tr><td rowspan=1 colspan=1>3277.1</td><td rowspan=1 colspan=1>-32.104</td><td rowspan=1 colspan=1>-0.3492</td><td rowspan=1 colspan=1>0.0024</td><td rowspan=1 colspan=1>4e-5</td><td rowspan=1 colspan=1>-2e-7</td></tr></table>

Wiheceficntcetancn wi ec ecal

Taupltla  blp atuposhoraint heal ecu voltage architecture with a trimming feature.

# Revision history

Table 11. Document revision history   

<table><tr><td rowspan=1 colspan=1>Date</td><td rowspan=1 colspan=1>Version</td><td rowspan=1 colspan=1>Changes</td></tr><tr><td rowspan=1 colspan=1>24-Sep-2021</td><td rowspan=1 colspan=1>1</td><td rowspan=1 colspan=1>Initial release.</td></tr><tr><td rowspan=1 colspan=1>09-Dec-2021</td><td rowspan=1 colspan=1>2</td><td rowspan=1 colspan=1>Updated Table 1. Applicable products.Updated Table 4. Example of VREFBUF output voltage per STM32 series.</td></tr><tr><td rowspan=1 colspan=1>13-Jul-2023</td><td rowspan=1 colspan=1>3</td><td rowspan=1 colspan=1>Updated document title.Updated Table 1. Applicable products.Updated Figure 1. STM32 VREBUF peripheral simplified schematic.Updated Table 3. VREFBUF peripheral behavior with ENVR/HIZ bits.Updated Table 4. Example of VREFBUF output voltage per STM32 series.</td></tr><tr><td rowspan=1 colspan=1>15-Nov-2024</td><td rowspan=1 colspan=1>4</td><td rowspan=1 colspan=1>Updated Table 1. Applicable products.Updated Table 4. Example of VREFBUF output voltage per STM32 series.</td></tr><tr><td rowspan=1 colspan=1>17-Feb-2025</td><td rowspan=1 colspan=1>5</td><td rowspan=1 colspan=1>Updated Table 4. Example of VREFBUF output voltage per STM32 series byreplacing &quot;STM32WL&quot; by &quot;STM32WLE/5&quot;.</td></tr><tr><td rowspan=1 colspan=1>12-May-2025</td><td rowspan=1 colspan=1>6</td><td rowspan=1 colspan=1>Updated Table 1. Applicable products by adding &quot;STM32U3 series&quot;.</td></tr></table>

# Contents

# 1 General information

# 2 VREFBUF peripheral principle

2.1 Principle and circuitry 3

# 2.2 Peripheral functional modes and status 4

2.2.1 ENVR and HIZ bits 4   
2.2.2 VRS bits 4   
2.2.3 VRR 5   
2.2.4 TRIM. 5

# VREFBUF constraints in application 6

3.1 VREFBUF trimming circuitry .6   
3.2 VREFBUF trimming with an external voltage and ADC 7   
3.3 VREFBUF trimming with the internal VREFINT voltage and the ADC 8   
3.4 Minimum VDDA supply voltage . 8   
3.5 VREFBUF output decreases when VRS changes 8

# VREFBUF application examples. 9

4.1 VREFBUF used as ADC reference for analog signal acquisition .9   
4.2 VREFBUF used as DAC reference for signal generation application . .9   
4.3 VREFBUF used as voltage reference with a voltage divider 10   
4.4 VREFBUF used as voltage reference with thermal sensor 11

# Revision history 14

# List of tables 16

_ist of figures. 17

# List of tables

Table 1. Applicable products   
Table 2. STM32G4 series VREFBUF output with R1 and R2 resistors example 3   
Table 3. VREFBUF peripheral behavior with ENVR/HIZ bits. 4   
Table 4. Example of VREFBUF output voltage per STM32 series. 4   
Table 5. STM32G4 series VREFBUF output voltage with VRS value. 5   
Table 6. Trimming operation example for STM32G4 2.5 V VREFBUF output voltage. 6   
Table 7. STM32 ADC digital output code /VREFBUF estimation . 7   
Table 8. VREFBUF degraded mode example. 8   
Table 9. Temperature/STM32 12-bit ADC code summary 12   
Table 10. Polynomial coefficients of the interpolation function 12   
Table 11. Document revision history. 14

# List of figures

Figure 1. STM32 VREBUF peripheral simplified schematic 3   
Figure 2. VREFBUF peripheral simplified principle 3   
Figure 3. ADC 3-bit quantization step example. 9   
Figure 4. DAC 8-bit quantization step example 10   
Figure 5. 1 V reference voltage from VREFBUF divided 10   
Figure 6. Example of a generic NTC thermistor impedance versus temperature 11   
Figure 7. NTC thermistor voltage divider with VREFBUF peripheral 11   
Figure 8. Table results and estimation curve from ADC code with a polynomial interpolation 12

# IMPORTANT NOTICE  READ CAREFULLY

pt old ursant  dits   leole.

purchasers' products.

No license, express or implied, to any intellectual property right is granted by ST herein.

are the property of their respective owners.

I

© 2025 STMicroelectronics - All rights reserved