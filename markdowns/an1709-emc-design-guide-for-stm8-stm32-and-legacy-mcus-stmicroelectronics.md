# EMC design guide for STM8, STM32 and legacy MCUs

# Introduction

Ce system level.

the optimum level of EMC performance.

# 1 General information

# Note:

This document applies to the Arm®-based devices. Arm is a registered trademark of Arm Limited (or its subsidiaries) in the US and/or elsewhere.

Arm is a registered trademark of Arm Limited (or its subsidiaries) in the US and/or elsewhere.

# arm

# 2 EMC definitions

# 2.1

# EMC

Electromagnetic compatibility (EMC) is the capability of a system to work properly, undisturbed by the electromagnetic phenomena present in tsnormal environment, and not to create lectrical disturbances that would interfere with other equipment.

# 2.2

# EMS

Theelectromagneti susceptibility (EMS) level of adevice is the resistance to electrical disturbances and conucted electrical noise.Electrostatic discharge (ESD)and fast transient burst (FTB) test determine the reliability level of a device operating in an undesirable electromagnetic environment.

# 2.3

# EMI

Theelectromagnetic interference Ml) is the level o conducted or radiated electrical noisesourcedby he equipment. Conducted emission propagates along a cable or any interconnection line. Radiated emission propagates through free space.

# 3 EMC characterization of microcontrollers

# 3.1

# Electromagnetic susceptibility (EMS)

Two different type of tests are performed:

Tests with device power-supplied (functional EMS tests and latch-up): the device behavior is monitored during the stress.   
wot pl ee vealiiy is checked on tester after stress.

# 3.1.1

# Functional EMS test

Fal  olplatB apl gtwoLDh /O ort) he uc e byent MCve a run-away condition (failure) occurs.

# Functional electrostatic discharge test (F_ESD test)

T ts peen  ewitrolleevis.c pstdially w g ornegative electrical discharge.This allows failures investigations inside the hipand furtherapplition recommendations to protect the concerned microcontroller sensitive pins against ESD.

High static voltage has both natural and man made origins. Some specific equipment can reproduce this phenomenon in order to test the device under real conditions. Equipment, test sequence, and standards are descrbed below.The micocontroller FED qualication test uses the standards given Tablesre.

Table 1. ESD standards   

<table><tr><td rowspan=1 colspan=1>European standard</td><td rowspan=1 colspan=1>International standard</td><td rowspan=1 colspan=1>Description</td></tr><tr><td rowspan=1 colspan=1>EN 61000-4-2</td><td rowspan=1 colspan=1>EC 61000-4-2</td><td rowspan=1 colspan=1>Conducted ESD test</td></tr></table>

F_ESD tests uses a signal source and a powempliier o generate ahigh leve feldinto hemicnolr. eiectrostatic discharge is applied (see Figure 1).

![](images/cff8f74e5ab512881752185609b9809e72e988e673f449c18fc71d60fd175a00.jpg)  
Figure 1. ESD test equipment

The equipment used to perform F_ESD test is an NSG 435 generator (TESEQ) compliant with the IEC 61000-4-2 standard. The discharges are directly applied on each pin of the MCU.

![](images/f8fb67eb099d37da707b2719fec65e4dbfd9ebf51a8b71a371b5611712f00b13.jpg)  
Figure 2. Typicai ESD current waveform in contact-mode discharge

![](images/6bd1a6f343029ca34a615ad0084daa4a3e18c3b36b23361955b668448ddab561.jpg)  
Figure 3. Simplified diagram of the ESD generator

# 1. Rch= 50 MΩ, Rd = 330 Ω

# Fast transient burst (FTB)

Mcoplex thannctnal hsmiheevicarquantiittisuan ar   suseu eeeun vabl lasr  t o . The microcontroller FTB test correlates with the standards given in Table 2.

Table 2. FTB standards   

<table><tr><td rowspan=1 colspan=1>European standard</td><td rowspan=1 colspan=1>International standard</td><td rowspan=1 colspan=1>Description</td></tr><tr><td rowspan=1 colspan=1>N61000-4-4</td><td rowspan=1 colspan=1>EC 61000-4-4</td><td rowspan=1 colspan=1>Fast transient burst</td></tr></table>

![](images/24f0b9e457e7e5cee6ebe5dc58fe30b6cb68be4e298e0fbeba95c81d25900d07.jpg)  
Figure 4. FTB waveform diagram

Repetition frequency: 5 kHz.

Bursts repeat for at least 1 minute.

Rising and duration time (±30%) are referred to a 50Ω load

The spike requency s 5 z. The generator produes bursts  spikes that last 5ms every 300 ms (75 ies).   
The fast transients are coupled to the device DUT with capacitors CC (see Figure 5).

![](images/47aa75c64c508b4b0af45930689e2b6dd041883b839db3d6817f1be404aaa64b.jpg)  
Figure 5. Coupling network

Measurements are performed on a ground plane.The generator is connected to ground plane by a short wre. T ply wiresom eo plae  elatooe o plaT FTB voltage level is increased until the device failure.

Sevi ve caselplcationsne etei whc cntoeuitable datasheet.

# ST severity level and behavior class

The IEC 61000-4-2 and IEC 61000-4-4 standards do not refer specifically to semiconductor components such micctrollersullecageiresplither parthe ystem suc c, mains, supplies. The energy level of the FESD and FTB test decreases before reaching the micocontrole, ov e wsia ial aol avi various application environments has been used to develop a correlation chart between ST F_ESD or FTB test voltage and IEC 61000-4-2/61000-4-4 severity levels (see Table 3).

Table 3. ST ESD severity levels   

<table><tr><td rowspan=1 colspan=1>Severity level</td><td rowspan=1 colspan=1>ESD (IEC 61000-4-2)equipment standard(kV)</td><td rowspan=1 colspan=1>FTB (IEC 61000-4-4)equipment standard(V)</td><td rowspan=1 colspan=1>ESD ST internal EMCtest (kV)</td><td rowspan=1 colspan=1>FTB ST internal EMC test(kV)</td></tr><tr><td rowspan=1 colspan=1>1</td><td rowspan=1 colspan=1>2</td><td rowspan=1 colspan=1>0.5</td><td rowspan=1 colspan=1>≤ 0.5</td><td rowspan=1 colspan=1>≤ 0.5</td></tr><tr><td rowspan=1 colspan=1>2</td><td rowspan=1 colspan=1>4</td><td rowspan=1 colspan=1>1</td><td rowspan=1 colspan=1>≤1</td><td rowspan=1 colspan=1>≤1</td></tr><tr><td rowspan=1 colspan=1>3</td><td rowspan=1 colspan=1>6</td><td rowspan=1 colspan=1>2</td><td rowspan=1 colspan=1>≤ 1.5</td><td rowspan=1 colspan=1>≤ 1.5</td></tr><tr><td rowspan=1 colspan=1>4</td><td rowspan=1 colspan=1>8</td><td rowspan=1 colspan=1>4</td><td rowspan=1 colspan=1>≤2</td><td rowspan=1 colspan=1>≤ 2.5</td></tr><tr><td rowspan=1 colspan=1>5(1)</td><td rowspan=1 colspan=1>&gt;8</td><td rowspan=1 colspan=1>&gt;4</td><td rowspan=1 colspan=1>NA</td><td rowspan=1 colspan=1>&gt; 2.5</td></tr></table>

1. Tv O be passed.

Intin vey ve CUavind res ane ifent avia (see table below) according to EN 50082-2 standard.

Table 4. ST behavior classes   

<table><tr><td rowspan=1 colspan=1>Class A</td><td rowspan=1 colspan=1>Class B</td><td rowspan=1 colspan=1>Class C</td><td rowspan=1 colspan=1>Class D</td></tr><tr><td rowspan=1 colspan=1>No failure detected</td><td rowspan=1 colspan=1>Failure detected but self-recoveryafter disturbance</td><td rowspan=1 colspan=1>Needs an external user action torecover normal functionality</td><td rowspan=1 colspan=1>Normal functionality cannotbe recovered</td></tr></table>

m define good EMS performance.

Class B can be caused by:

• a parasitic reset correctly managed by the firmware (preferable case)

• deprogramming of a peripheral register or memory recovered by the application a blocked status, recovered by a watchdog or other firmware implementation

Class C can be caused by:

deprogramming of a peripheral register or memory not recovered by the application a blocked application status requiring an external user action

The table below shows ST target and acceptance limits.

Table 5. F_ESD/FTB target level and acceptance limit   

<table><tr><td rowspan=1 colspan=1></td><td rowspan=1 colspan=1>Acceptance limit</td><td rowspan=1 colspan=1>Target level</td></tr><tr><td rowspan=1 colspan=1>F_ESD</td><td rowspan=1 colspan=1>0.5kV</td><td rowspan=1 colspan=1>&gt;1kV</td></tr><tr><td rowspan=1 colspan=1>FTB</td><td rowspan=1 colspan=1>0.5kV</td><td rowspan=1 colspan=1>&gt;1.5kV</td></tr></table>

an ar ve evieatiel blopeala system design must be taken to avoid susceptibility issues.

The table below shows how F_ESD/FTB test results are presented in ST datasheets.

Table 6. Example of F_ESD / FTB test results   

<table><tr><td rowspan=1 colspan=1>Symbol</td><td rowspan=1 colspan=1>Ratings</td><td rowspan=1 colspan=1>Conditions</td><td rowspan=1 colspan=1>Severity/Criteria</td></tr><tr><td rowspan=1 colspan=1>VF_ESD</td><td rowspan=1 colspan=1>Voltage limits to be applied on any I/O pin to induce a functional disturbance</td><td rowspan=1 colspan=1>TA=+25°</td><td rowspan=1 colspan=1>2/A, 3/B</td></tr><tr><td rowspan=1 colspan=1>VFTB</td><td rowspan=1 colspan=1>Fast transient voltage burst limits to be applied through 100 pF on VSS and VDDpins to induce a functional disturbance</td><td rowspan=1 colspan=1>TA=+25°</td><td rowspan=1 colspan=1>3/B</td></tr></table>

# 3.1.2

# Latch-up (LU)

# Static latch-up (LU) test

Te lat heeon hic des ahicu nsptionsultno overstre rv

Too abnormal condition that causes the parasitic thyristor structure to become self-sustaining.

magnitude or duration.

# This test conforms to the EIA/JESD 78 IC latch-up standard

T Uet isemoved fromhe deviA temporary U condtion is considered to have been iducefhehigh current condition stops when only the trigger voltage is removed.

Two complementary static tests are required on 10 parts to assess the latch-up performance:

Power supply overvoltage (applied to each power supply pin) simulates a user induced situation where a transient over-voltage is applied on the power supply.

Currnt injecton plie eac ipututu  cgurable /Op) sulate an plication situation where the appliedvoltage to a pin s greater than the maximum rated conditons, such as seve overshoot above VDD or undershoot below ground on an input due to ringing

1e table below shows how LU test result is presented in ST datasheets.

Table 7. Example of the LU test result on STM32L062K8   

<table><tr><td rowspan=1 colspan=1>Symbol</td><td rowspan=1 colspan=1>Parameter</td><td rowspan=1 colspan=1>Conditions</td><td rowspan=1 colspan=1>Class(1)</td></tr><tr><td rowspan=1 colspan=1>LU</td><td rowspan=1 colspan=1>Static latch-up class</td><td rowspan=1 colspan=1>TA=+125°C conforming to JESD78A</td><td rowspan=1 colspan=1>IlI level A</td></tr></table>

C heve   v (international standard).

# Dynamic latch-up (DLU) test

he product is evaluated for its LU susceptibility to ESD discharges when the microcontroller is "runnig.

s the maximum tolerated voltage without latch-up.

DLU test methodology and characterization:Electrostaticdischarges one positive hen ne negative test a  h p a pins of the microcontroller and the component is put in reset mode.

LU/DLU test equipment is same as the one used for the functional EMS (see Figure 1).

# 3.1.3

# Absolute electrical sensitivity

This test is performed to assess the components immunity against destruction caused by ESD. Any device that fails this electrical test program is classified as a failure.

Usiuateeestaiharge  osivhegativ pul parated y al   sampoi atple supply pins of the device (3parts\*(n+1), where n = supply pins).

Two models are usually simulated: human body model (HBM) and the charge device model (CDM). All parts areteten he production tserehestatican ynam parameter coply withheevi datasheet (see Figure 6).

For both models, parts are not powered during the ESD stress. This test conforms to the JESD22-A114A/A115A standard. See Figure 6 and the following test sequences.

![](images/023ef6cadcaec1768953d87e248865ca063cf225b18d9499cdf9afb0fbd1a357.jpg)  
Figure 6. Absolute electrical sensitivity test models

# Human body model test sequence

Th  uunsotaha od 0 paci ar  i n   soi u most requested industry model, for classifying device sensitivity to ESD.

CL is loaded through S1 by the HV pulse generator.   
S1 switches position from generator to R.   
A discharge from CL through R (body resistance) to the microcontroller occurs.   
S2 must be closed 10 to 100 ms after the pulse delivery period to ensure the microcontroller is not left in charge state. S2 must be opened at least 10ms prior to the delivery of the next pulse.

# Charge device model (CDM)

Refe oheaplication otElectrostaticdischargeensitiviymeasurement AN1181)or detaile dest of CDM.

Since 2018 the MCU are characterised for CDM ESD sensitivity following a standard JEDEC ANSI/ESDA/JEDEC JS-002-2014 which is replacing ANSI/ESD STM5.3.1 standard, see Table 9 for comparison of the device classification levels.

# Classification according to ANSI-ESD STM5.3.1

Table 8. CDM ESDS component classification levels   

<table><tr><td rowspan=1 colspan=1>Class</td><td rowspan=1 colspan=1>Voltage range (V)</td></tr><tr><td rowspan=1 colspan=1>C1</td><td rowspan=1 colspan=1>&lt;125</td></tr><tr><td rowspan=1 colspan=1>C2</td><td rowspan=1 colspan=1>125 to &lt; 250</td></tr><tr><td rowspan=1 colspan=1>C3</td><td rowspan=1 colspan=1>250 to &lt; 500</td></tr><tr><td rowspan=1 colspan=1>C4</td><td rowspan=1 colspan=1>500 to &lt; 1000</td></tr><tr><td rowspan=1 colspan=1>C5</td><td rowspan=1 colspan=1>1000 to &lt; 1500</td></tr><tr><td rowspan=1 colspan=1>C6</td><td rowspan=1 colspan=1>1500 to &lt; 2000</td></tr><tr><td rowspan=1 colspan=1>C7</td><td rowspan=1 colspan=1>≥ 2000</td></tr></table>

Table 9. Classification according to ANSI/EDSA/JEDEC JS-002   

<table><tr><td rowspan=1 colspan=1>Classification level</td><td rowspan=1 colspan=1>Classification test condition (V)</td></tr><tr><td rowspan=1 colspan=1>C0a</td><td rowspan=1 colspan=1>&lt;125</td></tr><tr><td rowspan=1 colspan=1>COb</td><td rowspan=1 colspan=1>125 to &lt; 250</td></tr><tr><td rowspan=1 colspan=1>C1</td><td rowspan=1 colspan=1>250 to &lt; 500</td></tr><tr><td rowspan=1 colspan=1>C2a</td><td rowspan=1 colspan=1>500 to &lt; 750</td></tr><tr><td rowspan=1 colspan=1>C2b</td><td rowspan=1 colspan=1>750 to &lt; 1000</td></tr><tr><td rowspan=1 colspan=1>C3</td><td rowspan=1 colspan=1>≥ 1000</td></tr></table>

# 3.2

# Electromagnetic interference (EMI)

# 3.2.1

# EMI radiated test

This test correlates with the IEC 61967-2 standard. It gives a good evaluation of the contribution of the micocontroller toradiatednoisna application evironment. It takes itoaccount he chi as wellas the package, which has a major influence on the noise radiated by the device.

general, the smaller the package belonging to a given package family, the lower the noise generated.

The below lists the package EMI contribution from the highest to the lowest:

• SOP QFP   
• TQFP   
• FBGA CSP

The test is performed in a transverse electromagnetic mode cell (TEMCELL or GTEM) which alows radiated noise measurement in two directions, rotating the test board by 90 °.

Note:

Since December 14, 2015, the upper limit of the emission measurement frequency range has been extended from 1 GHz to 2 GHz with different settings. The reasons and modalities of these changes are described in Section Appendix A , as well as the classification method to use for 100 kHz-1 GHz measurement data.

# Test description

The firmware running is based on a simple application, toggling two LEDs through the I/O ports. The main directives of IEC61967 standard related to test hardware are the following (see Figure 8

100 x 100 mm square board.   
At least 2-layer board (ideally 4-layer)   
5 mm conductive edges on both sides connected to ground for contact with TEMCELL

The figure below shows a typical example of an MCU EMC test board schematics.

![](images/293b2c3ce92d609b1c5be02cb8ff5d13e16a897d53f4109013fc755b61847b07.jpg)  
Figure 7. Example of test board schematics for STM32

![](images/eb9d5caefb903b2165c28aebaa351949e5e52f223856018baaa1a9f4b5858502.jpg)  
Figure 8. Test printed circuit board specification according IEC 61967-2 standard   
Additional signal layers may be added as necessary

# Spectrum analyzer settings

The IEC61967-1 standard describes the spectrum analyzer hardware and software settings. In spite of these directives, the resolution bandwidth must be chosen according to the measured signal type narrowbandor broadband.

The table below defines the resolution bandwidth (RBW) versus the emission measurement frequency range

Table 10. Spectrum analyzer resolution bandwidth versus frequency range (broadband EMI)   

<table><tr><td rowspan=1 colspan=1>Frequency range (MHz)</td><td rowspan=1 colspan=1>Resolution bandwidth (RBW)</td><td rowspan=1 colspan=1>Detector</td></tr><tr><td rowspan=1 colspan=1>0.1 -1</td><td rowspan=1 colspan=1>10 kHz</td><td rowspan=5 colspan=1>Peak</td></tr><tr><td rowspan=1 colspan=1>1-10</td><td rowspan=1 colspan=1>10 kHz</td></tr><tr><td rowspan=1 colspan=1>10 - 100</td><td rowspan=1 colspan=1>10 kHz</td><td rowspan=1 colspan=1></td></tr><tr><td rowspan=1 colspan=1>100 - 1000</td><td rowspan=1 colspan=1>100 kHz</td><td rowspan=1 colspan=1></td></tr><tr><td rowspan=1 colspan=1>1000 - 2000</td><td rowspan=1 colspan=1>1 MHz</td></tr></table>

# 3.2.2

# EMI level classification

The EMI classifications are based on IEC61967-2 international standard-Annex D-3 (see Figure 9).

Tazatoneegraebeanar oviethecasatiM t etl gal Fhe attrp atthav eele tal asat u sectr analyzer as we asronancu by egeoey  he tboar a setuphe tet bench.

When the overstepping of a particular limit is not significant, and the corresponding peak valuesof he intererence aproiately in hemidle between two patterns, thenhalf-evels might be use as well.

![](images/ec96e11b41806cbf88b7a8d9275c3115a23e3cf0716ee2ffdb9755eed094ec77.jpg)  
Figure 9. IEC61967-2 classification chart

![](images/0c5c8d10158db4c0f2a49e71a9ab81715f22fb1ef386ce7f3c2f77f79fc8e55f.jpg)  
Figure 10. ST internal EMI level classification

# Note:

Compliance with level 2 and level 2.5 regardless of peaks above 1 GHz.

Compliance with level 1 and level 1.5 regardless of peaks above 500 MHz.

Based on ST experience, the potential risk associated to each EMI level has been defined:

Above level 4: high risk due to EMI level   
In the range of levels 3—4: may require cost for EMl compliance   
In the range of levels 23: moderate EMI risk   
In the range of levels 12: minimal EMI risk   
Below level 1: very low EMI risk

The table below shows how EMl test results are presented in the datasheets.

Table 11. Example of EMI results on STM32   

<table><tr><td rowspan=1 colspan=1>Symbol</td><td rowspan=1 colspan=1>Parameter</td><td rowspan=1 colspan=1>Conditions</td><td rowspan=1 colspan=1>Monitoredfrequency band</td><td rowspan=1 colspan=1>Value</td><td rowspan=1 colspan=1>Unit</td></tr><tr><td rowspan=5 colspan=1>SEMI</td><td rowspan=4 colspan=1>Peak</td><td rowspan=5 colspan=1>VDD = 3.6 V, TA =25 °C, LQFP64 packagecompliant with IEC 61967-2</td><td rowspan=1 colspan=1>0.1 MHz to30 MHz</td><td rowspan=1 colspan=1>7</td><td rowspan=4 colspan=1>dBμV</td></tr><tr><td rowspan=1 colspan=1>30 MHz to130 MHz</td><td rowspan=1 colspan=1>-1</td></tr><tr><td rowspan=1 colspan=1>130 MHz to1Gz</td><td rowspan=1 colspan=1>8</td></tr><tr><td rowspan=1 colspan=1>1 GHz to 2 GHz</td><td rowspan=1 colspan=1>7</td></tr><tr><td rowspan=1 colspan=1>Level</td><td rowspan=1 colspan=1>0.1 MHz to2 GHz</td><td rowspan=1 colspan=1>2.5</td><td rowspan=1 colspan=1></td></tr></table>

# MCU design strategy and EMC specific feature

During the initial specification phase of a new product, EMC dedicated features are implemented after an ienficationMcstraint IheMCUtargaplcations ha ps heconstraintsRee specific product datasheet to know which of these features described in the figure below are embedded.

![](images/9b6d251222bb1bee9eaca05967ab5e2999f0ab070d2dd8daf61666fad772f994.jpg)  
Figure 11. Overview of specific features embedded in microcontrollers

# 4.1 Susceptibility

# 4.1.1

# Brownout reset (BOR)

The purpose of the BOR is to ensure that themicrocontrolleralways work in s safe operating are (see u. In erMS te prec f he OR makes he CU morbus esues ha outside disturbance affects the power supply, the application can recover safely.

WhVeloi workeavictrolle logan is not enough power to decode/execute the instructions and/or read the memory. When VD is below the BOR olatal hh vib.

T al lve wi whenstWh, the hardware set a bit. This bit is used to recover an application.

T  olV Thmen hate he pwe s we s he pown epn hetrole  e Figure 12).

reset. This is the case when the MCU starts running and sinks current on the supply (hysteresis).

The BOR circuitry generates a reset when VDD is below:

VIT+ when VDD is rising   
VIT- when VDD is falling   
Th BOR ncon s istrateFiguTevoltae rehold cacgured ytin bye low, medium, or high.   
The MCU can only be in two modes f the minimum VDD value (guaranteed for the oscillator frequency) is above VIT-:   
under full software control   
in static safe reset   
In theecondtions, a secure operation is lways ensured for he applicatin without the need oreteal hardware reset.

During a brownout reset, the NRST pin is held low, thus permitting the MCU to reset other devices.

# Note:

The BOR allows the device to be used without any external reset circuitry.

The BOR is an optional function that can be selected by option byte. Refer to product specification.

![](images/7dee9c4286af74535053d1416e689b23dc2137550aa0ee6cf9f7eed67b5bc627.jpg)  
Figure 12. Brownout reset versus reset

# 4.1.2

# Programmable voltage detector (PVD)

Ti feature ike he BOR provs MS peorance. I sures that heiccontrollerbehave safely whe the power supply is disturbed by external noise.

The PVD has also different levels (around 200mV above BOR levels), it enables an early warning befoe the re caused by the BOR. Whe PVD threshold is crossed, an interrupt is generated, requesting fr example to the correct level for the device (refer to the product datasheet).

# Example

If f is between 8 MHZ and 16 MHZ the minimum working level is 3.5 V. The Voltage detector function (PVD) is based on an analog comparison between a VT and ViT+ reference value and the VDD main supply. The parasitic detection (hysteresis).

Trbl ltl (PVDO). This bit is read only.

corresponding product datasheet).

threshold (PVDO bit toggles).

I ybeoe heBR ethecrolr. e gur.Thetpt nhe inform the application that the VDD warning state is over.

If the voltage rise time try is less than 256 or 4096 CPU cycles (depending on the reset delay of the microcontroller), no PVD interrupt is generated when VIT+(PVD) is reached.

If try is greater than 256 or 4096 cycles then:

If the PVD interrupt is enabled before the VIT+(PVD) threshold is reached, then two PVD interrupts are received, the first when the PVDE bit is set, and the second when the threshold is reached. If te VDtrupt abl aftr eVIT(PVD)reold is ae hen nly  VDter .

![](images/cf4aa08cea4c4f49a001c9d8354fcbce090306cb9496b9a2ff6f7ed43f1e9c82.jpg)  
Figure 13. Using the PVD to monitor VDD

# 1.1.3 I/O features and properties

Integrated circuit datasheets provide the user with conservative limits and conditions to prevent damage. of exposure to illegal voltages and conditions can be reduced.

Iti o   su tha whevvoltagple eviry iantlu epoo vtatiatuxtalaciol other devices.

Inoeu damage to the microcontroller device.

# Electrostatic discharge and latch-up

CMtatally sivoltaaey h iekhihiu current and sometimes shorts.

Tatot eecritegratcn bartructures, rsilicon-controll rectifiers (SR), may overheat an rapidly destroy the device.Tee unintentional structures are composed of Pand  regions, which work as emitters, bases, and collectorso SCR structure. The SCR may be turned on when voltages below Vss or above VDD, are applied. It may be tu e o Tuso e pwTeo uar at i standards and recommendations (see Section 3.1.2 Latch-up (LU)).

# Protective interface

Microcontroller input/output circuitry has been designed to take ESD and latch-up problems into account. Howel t wheol lol isgraolT case, low-pass filters, and clamp diodes are usually sufficient in preventing stress conditions.

Toto bill oo go performance. This induces undesired timing delays, and impacts the global system speed.

![](images/5f752f94ed38eeb4898d0a3f6ca7d4b9e6a98c3a78086b6a450ae352fe848b9c.jpg)  
Figure 14. Digital input/output - push-pull

# Internal circuitry: digital I/O pin

Fuow eaeatimiotroller leranu buplent t dioe-ison eraioee he n -well o VDD) Mehie -ae eu ufp  eVSS.Tha  -usra to V and N-diffusion of he drai connected o the pi. In parallel to these diodes,dedicate circy is implemented to protect the logic from ESD events. These are MOS, diodes, and input series resistor.

Themostporant haracterishesextevicsthathemus o isturormal peratige. apl whi  ur u -tsvo pt ma circuitry.

S O psn  prorame  work alo s en-ra outputs. hsis peormehrou siply w in thecorespondig egistr the O port.This depenon heU ushe gatef te -chael e w. Iha opl   aVD al p condition injects current through the diode, risking permanent damages to the device.

# Internal circuitry: analog input pin

multiplexer for the selection of the input channel of the ADC (analog to digital converter).

The presence of the multiplexer P-channel and N-channel can affect the behavior of the pin when exposed to illvotseo oll   oo ta w uplg valc not limited) may destroy the device.

![](images/9209dd0057f4da8fa26593861170d68d6ac1455cae2e91fde8ee158e78ec8f4c.jpg)  
Figure 15. Digital input/output - push-pull output - analog multiplexer input

# 4.2

# Emission

# 4.2.1

# Internal PLL

Some microcontrollers have an embedded programmable PLL clock generator that allows the usagef standard MHz to25 MHz crystals.This allows a large range internal fequencis (up to a few hundred MHz) t e iByhsmeans,hemiontrolle anerat wit heapemedequenc ystal whileil providin a high frequency internal clock ormaximum system perormance.Thehigh-clock equency ource iscontained inside the chip and does not go through the PCB (printed circuit board) tracks and external components. This reduces the potential noise emission of the application.

The use of the PLL network also filters the CPU clock against external sporadic disturbances (glitches).

# 4.2.2 Clock sources

# Low-powered oscillator

Tla is limited. The main clock of some microcontrollers is generated by four different source types coming from the multciatorblock (M).Thisallows the desier  elec easihe bes trade-oin terms cs, perormance, and noise emission. The clock sources are listed below from the most to the least noisy:

an external source crystal or ceramic resonator oscillators an internal high frequency RC oscillator

Eacillatortizogiv ang tptn. Ielctaler eatarwa coguatinsownueateee characteristics section for more details in each case.

# External clock source

I ccec l  wi \~%uy ci OSC32_OUTpins while the OSC_OUT respect to the OSC32_OUTpin is tied:

to ground left unconnected or used as standard GPIO

See product reference manual for recommended configuration.

# Crystal/ceramic oscillators

Thifmilat cataclchetrollTe o tu iz adjusted according to the selected oscillator.

Thee osilators ar ot stopped during eRET phase avoid the delay needed or he ilator aru.

# Internal RC oscillator

T e  gl  Iheilao  ar P They are lt unconnected o tied t ground,see product documentation ormore details.Process vartions a ri some iffns rom ots ots (0 0%) Semiontrollers eer  product setn e a process compensation.This feature iscalled trimmable internal RC". A procedure during the test alag RC accuracy to 1%. The user can also perform this procedure.

![](images/d822907b7b7056ea01ce6d5aa4c8dac4ca0ec5dcb83a0b41e75090144fe4ddee.jpg)  
Figure 16. STM32 clock sources - hardware configuration

Ttiliylote etween emission, accuracy, and cost criteria.

# Internal voltage regulators (for MCUs with low-power core)

An internal voltage regulator isused to power some microcontrollers cores starting from the external power supply.

The voltage regulator reduces EMI due to the MCU core with two effects:

lower CPU supply voltage   
isolate CPU supply from external MCU supplies   
For moreinformation on how touse the osillator, reer to theapplication noteOscillator design guie or STM8S, STM8A and STM32 microcontrollers (AN2867).

# 4.2.3

# Output l/O current limitation and edge timing control

u rolehihetollv oscillations when they are switched. The MCU design makes a trade-off between noise and speed.

# 5 EMC guidelines for MCU based applications

The following guidelines result from the experience gained in a wide variety of applications.

# 5.1 Hardware

T  ary th ear theThe ctions  prevent nois probles thus concen the  layout and h de the power supply.

Inl alle,ei Rutilsivo memory circuit.

# 5.1.1 Optimized PCB layout

Nosbasiaeceiv antnihroghtrack d cpent which,cexci c s neas. Each loop and track includes parasitic inductance and capacitance. This radiate and absorb energy once submitted to a variation of current, voltage, or electromagnetic flux.

An MCU chip itself presents high imunity to and low generation f EMI since ts dimensions are mall versus the wave lengths  M sgnals (typicay  versu 0'  orM sinals in the GHz range).There, a single chip solution with small loops and short wires reduces noise problems.

Ta    ucsTeo w pplilatoan ut ie wi elttn must be especially small since it operates at high frequency (see Figure 17).

suggests that in most cases inductance is the first parameter to minimize.

![](images/117b50b165cd41f21eced0a091e1894d270ae39bff1f9d15ab60928a8a8ec981.jpg)  
Figure 17. PCB board-oscillator layout examples

The reduction of inductance isobtained by making the lengths and surfacesof the track smalle. This is performed placing the track loops closer on the same PCB layer or on top of one another (Figure 7). The resulting loop area is small and the electromagnetic fields reduce one another.

T /cm2Typical examplesf ow inductivity wiresa coaxial, twisted pairablesrultiple ayer CBs wit or the paralleling of several small capacitances mounted in the current flow.

I aC ha the los between  MC an envionent mus also beminmiz To achive his,ay socket betwe e MCU package and the PCB must be removed oreither, a ceramic MCU package must be replaced with a plastic one using a surface mounting instead of dual in line packages.

# Note:

Board vias are inductances. Try to avoid them. If required, use multivias.

![](images/f09dbd0403a15aa218365bd076a028f96448af02888aff1a66e9a41fdcbb2b29.jpg)  
Figure 18. Reduction of PCB tracks loop surfaces

# Note:

This test is done with a double sided PCB. Insulator thickness is1.5 mm: copper thickness is 0.13 mm. The overall board size is 65 x 200 mm.

# 5.1.2 Power supply filtering

T uy sus a al vute can be separated using star wiring with one node designated as common for the circuit (Figure 19).

Thedecoupligapacitance must e placed vey close  the  suply pis ominimize he resultant o. Itl  i ntvol s te oeioeelerwi eleolyap (ypically 0 F to0 F) since the delectric use i such capacitors provides a highvolumi capactae. Hoeheacors eaviuanc hiheucypicboveMHzwhic plastic capacitors keep a capacitive behavior at higher frequency.

A crami capacance or instanc, 0.1 F to 1 F must be usd as hihrequency supply decoupln or critical chips operating at high frequency.

![](images/478b392ed9d30cb64a300c7c60fe7c79a0fa87daf91f533e6f450741896fc151.jpg)  
Figure 19. Power-supply layout examples

# 5.1.3 Ground connections

It icede cc al pitgether e hort posbe pauce voltagedifference between theVSS pins abovethe absolutemaximum ratings stated in the device datasheet, due to the current induced by external disturbance and toreduce the impedance of ground return path.

The best practic is tconect he nes  thegroud plane hrough heis placeas close s posle to the device S pis.The ground plane must be solid without slots orholes, which may cause an incrase o the ground plane impedance. The split of analog and digital ground is not recommended While it may vaaaoMC performance.

# 5.1.4 I/O configuration

gu / pis otuse heaplcation  cgure utut push-pul low stathiscearuse configure as an analog input connected to ground to reduce power current consumption.

# 5.1.5

# Shielding

Sdisoeatho Itv yvsvo incdeplinpactancvlo peanoidanc owsan)volag.

I e cage around the control board may strongly increase the immunity.

b Inn, hran  heol on he shilshould ereuc  muc  pos increase its efficiency.

Incritial cases,heplantation a ground plane below he MC, and he removal  socket between he device and the PCB can reduce the MCU noise sensitivity. Indeed, both actions lead to a reduction of the apparent surface of loops between the MCU, its supply, its I/O and the PCB.

# 5.1.6 I/O bonding coupling

In se appliatin cases, when he ESD strike occurs on a pn PA3 then, he adacent pins PA2 and PA4 can be affected by a voltage spike transferred to the current.

![](images/813249479e109643ff4f3235e07f2921dfa0f0aa792d5e25b99bd90c2c430a19.jpg)  
Figure 20. UFQFPN48 package example: top view

D    i a capacitive/inductive coupling between adjacent pins.

pins due to the coupling.

Iho uati ctaee u ceal may be altered.

Il strongly recommend improving the ESD protection on the identified entry point pn PA.This reduces the ESD coupled energy and ensures the good application operation.

# 5.1.7 High-speed signal tracks

Another source EMC weaknesses with microcontrol-base applications may be due tohigh speed digital I/O and communication interfaces such as, xSPI, I²C, external memories interfaces, USB, or PWM from GPIO.

When designing the PCB with high-speed signals, the following EMC consideration list must be considered:

Coupling/crosstalk:

When a signal couple and interfere with another one and leads to an intrusive spike (can be sampled as data) and timing shift.

Signal reflection:

The high-speed signals are susceptible to impedance mismatching which may alter the shape of the signal.

Clock jitter:

An external interference,or noise can introduce a deviation of the clock edge, this leads to a narrower timing tolerance or communication failure.

Potential antennas:

Routing close to the edge of the PCB or a gap in plane can act as an antenna.

Certification fails:

Even if there is o functional issue, he product may fil the required certification and the PCB must be redesigned.

To avoid these issues, planning with EMC performances in mind must be done from the earliest stages of development.

• Stack-up:

One major consideration to improve EMI is to use four (or more) layers PCB with the external layers (top and bottom) being for signals and the internal for GND and power planes. The solid planes help with controlling the signal impedance on the top and bottom and together (GND and PWR planes) create stack-up capacitance that improves the performance at higher frequencies.   
If there is a particularly noisy signal, t can be routed between two solid PWR/GND planes to reduce its emission but that require eight or more layer stack-up.   
Avoid gaps in the solid planes, these gaps can behave as antennas.

Routing tips and recommendations:

If a high-speed signal needs to go through a vias (not recommended for high-speed signals as they are seen as impedance mismatch), then the return path loop requires to keep at minimum loop area. Never route over plane gap and in case that it is unavoidable use stitching caps. Avoid routing in parallel for long distance to noisy signals to avoid coupling issues. For very long tracks (>30 cm) and very high-speed signals (>50 MHz) a termination resistance can be added to reduce the signal reflection (resistance range between 30 Ω \~ 50 Ω).

# 5.2

# Handling precautions for ESD protection

To determine the susceptibility of microcontroller devices to ESD damage, refer to the application note Electrostatic discharge sensitivity measurement (AN1181).

# 5.3 Firmware

This section is detailed in the application note Software techniques for improving microcontrollers EMC performance (AN1015) available on www.st.com..

# 5.4 EMC organizations resources

Table 12. EMC reference sources   

<table><tr><td rowspan=1 colspan=1>Name</td><td rowspan=1 colspan=1>Web link</td></tr><tr><td rowspan=1 colspan=1>FCC: Federal communication commission</td><td rowspan=1 colspan=1>www.fcc.gov</td></tr><tr><td rowspan=1 colspan=1>EIA: Electronic industries alliance</td><td rowspan=1 colspan=1>www.eoa.org</td></tr><tr><td rowspan=1 colspan=1>SAE: Society of automotive engineers</td><td rowspan=1 colspan=1>www.sae.org</td></tr><tr><td rowspan=1 colspan=1>IEC: The international electrotechnical commission</td><td rowspan=1 colspan=1>www.iec.ch</td></tr><tr><td rowspan=1 colspan=1>IEC: The international electrotechnical commission</td><td rowspan=1 colspan=1>www.cenelec.eu</td></tr><tr><td rowspan=1 colspan=1>JEDEC: Joint electron device engineering council</td><td rowspan=1 colspan=1>www.jedec.org</td></tr></table>

# 6 Conclusion

For any microcontroller application, EMC requirements must be considered at the very beginning of the development project Standards, features and parameters given in microcontroller datasheets help the system desigerdeterminehemostsuitablecomponent given applicatinHardwareanfiware precauion must be taken to optimize EMC and system stability.

# Appendix A EMI classification before December 14 2015

The section gives information that complements Section 3.2.1

Since December 14 2015, the upper limit of the emission measurement frequency range has been extended from1 GHz to2 GHz, thus increasing the resolution bandwidth (RBW). This change is due t the evolution o microcontrollers, which embed higher frequency internal clocks, sometimes above 200 MHz, with higher PLL multiplication factors. This leads to higher frequency broadband harmonics emissions.

ual  el assat patt datnuthe e settings.

For data related to measurements performed before December 14 2015 in the 100 kHz- 1 GHz frequency range, refer to Figure 21 and Table 13.

![](images/93f34a11a4ce58393c82da2cd23d682e492e899fb6e303c5c44c6be21a50bcb9.jpg)  
Figure 21. ST internal EMI level classification before December 14 2015

According to ST experience, the potential risk associated with each EMI level have been defined:

Level higher than 4: high risk due to EMI level.   
Level 4: may require cost for EMI compliance.   
Level 3: moderate EMI risk.   
Level 2: minimal EMI risk.   
Level 1: very low EMI risk

Table 13. Spectrum analyzer resolution bandwidth versus frequency range (narrowband EMl)   

<table><tr><td rowspan=1 colspan=1>Frequency range (MHz)</td><td rowspan=1 colspan=1>Resolution bandwidth</td><td rowspan=1 colspan=1>Detector</td></tr><tr><td rowspan=1 colspan=1>0.1 -1</td><td rowspan=1 colspan=1>1 kHz</td><td rowspan=4 colspan=1>Peak</td></tr><tr><td rowspan=1 colspan=1>1-10</td><td rowspan=1 colspan=1>1 kHz</td></tr><tr><td rowspan=1 colspan=1>10 - 100</td><td rowspan=1 colspan=1>1 kHz</td></tr><tr><td rowspan=1 colspan=1>100 - 1000</td><td rowspan=1 colspan=1>9 kHz</td></tr></table>

# Contents

# 1 General information

# 2 EMC definitions. 3

2.1 EMC 3   
2.2 EMS 3   
2.3 EMI 3

# EMC characterization of microcontrollers

# 3.1 Electromagnetic susceptibility (EMS) 4

3.1.1 Functional EMS test . 4   
3.1.2 Latch-up (LU) 8   
3.1.3 Absolute electrical sensitivity. 8

# 3.2 Electromagnetic interference (EMI). 10

3.2.1 EMI radiated test. 10   
3.2.2 EMI level classification 13

# MCU design strategy and EMC specific feature. .16

# 4.1 Susceptibility 16

4.1.1 Brownout reset (BOR). 16   
4.1.2 Programmable voltage detector (PVD) 17   
4.1.3 I/O features and properties 18

# 4.2 Emission. 21

4.2.1 Internal PLL 21   
4.2.2 Clock sources 21   
4.2.3 Output I/O current limitation and edge timing control. 23

# EMC guidelines for MCU based applications .24

# 5.1 Hardware 24

5.1.1 Optimized PCB layout. 24   
5.1.2 Power supply filtering .25   
5.1.3 Ground connections 26   
5.1.4 I/O configuration . 26   
5.1.5 Shielding.. 26   
5.1.6 I/O bonding coupling. 27   
5.1.7 High-speed signal tracks. 27   
5.2 Handling precautions for ESD protection . 28   
5.3 Firmware 28   
5.4 EMC organizations resources 29

# Conclusion .30

Appendix A EMI classification before December 14 2015. .31   
List of tables .34   
List of figures. .. .35   
Revision history .36

# List of tables

Table 1. ESD standards 4 Table 2. FTB standards. 5 Table 3. ST ESD severity levels .   
Table 4. ST behavior classes.   
Table 5. F_ESD/FTB target level and acceptance limit   
Table 6. Example of F_ESD / FTB test results   
Table 7. Example of the LU test result on STM32L062K8 8 Table 8. CDM ESDS component classification levels 9 Table 9. Classification according to ANSI/EDSA/JEDEC JS-002. 10 Table 10. Spectrum analyzer resolution bandwidth versus frequency range (broadband EMI) 12 Table 11. Example of EMI results on STM32 15 Table 12. EMC reference sources 29 Table 13. Spectrum analyzer resolution bandwidth versus frequency range (narrowband EMI). 31 Table 14. Document revision history . 36

# List of figures

Figure 1. ESD test equipment 4   
Figure 2. Typical ESD current waveform in contact-mode discharge 5   
Figure 3. Simplified diagram of the ESD generator 5   
Figure 4. FTB waveform diagram 6   
Figure 5. Coupling network 6   
Figure 6. Absolute electrical sensitivity test models 9   
Figure 7. Example of test board schematics for STM32. 11   
Figure 8. Test printed circuit board specification according IEC 61967-2 standard. 12   
Figure 9. IEC61967-2 classification chart. 14   
Figure 10. ST internal EMI level classification 14   
Figure 11. Overview of specific features embedded in microcontrollers 16   
Figure 12. Brownout reset versus reset. 17   
Figure 13. Using the PVD to monitor VDD 18   
Figure 14. Digital input/output - push-pull 19   
Figure 15. Digital input/output - push-pull output - analog multiplexer input 21   
Figure 16. STM32 clock sources - hardware configuration . 22   
Figure 17. PCB board-oscillator layout examples 24   
Figure 18. Reduction of PCB tracks loop surfaces 25   
Figure 19. Power-supply layout examples 26   
Figure 20. UFQFPN48 package example: top view. 27   
Figure 21. ST internal EMI level classification before December 14 2015. 31

# Revision history

Table 14. Document revision history   

<table><tr><td rowspan=1 colspan=1>Date</td><td rowspan=1 colspan=1>Version</td><td rowspan=1 colspan=1>Changes</td></tr><tr><td rowspan=1 colspan=1>Sep-2023</td><td rowspan=1 colspan=1>1</td><td rowspan=1 colspan=1>Initial release.</td></tr><tr><td rowspan=1 colspan=1>03-Feb-2016</td><td rowspan=1 colspan=1>2</td><td rowspan=1 colspan=1>Changed IEC 1000 standard into IEC 61000.Changed NSG 435 provider in Section 3.1.1: Functional EMS test. UpdatedTable 3: ST ESD severity levels.Changed static latch-up example to STM32L062K8 inModified Table 7.Removed Table Example of DLU test result on ST72F521 from Section 3.1.2:Latch-up (LU).Section 3.1.3: Absolute electrical sensitivity:Added the fact that parts are not powered during the ESD stress.Removed machine model.Added Section : Charge device model (CDM).Updated Section 3.2: Electromagnetic interference(EMI).Section 4.1: Susceptibility:Replaced low-voltage detector (LVD) by brownout reset (BOR).Replaced RESET by NRST.Removed Figure Maximum operating frequency vs supply voltage.Replaced Auxiliary voltage detector (AVD) by Programmable voltagedetector (PVD).Removed Section Multiple VDD and VSSUpdated Section 4.2.1: Internal PLL.Updated Section : Internal RC oscillator and SectionInternal voltage regulators (for MCUs with low-power core).Added trays in Section 5.2: Handling precautions for ESD protection.Added Appendix A: EMI classification before December 14 2015.</td></tr><tr><td rowspan=1 colspan=1>23-Apr-2018</td><td rowspan=1 colspan=1>3</td><td rowspan=1 colspan=1>Updated Charge device model (CDM), replace title of Section 3.2.2: Globallow-power approach by Section 4.2.2: Clock sources, External Clock source,Internal RC oscillatorAdded Table 8: CDM ESDS component classification levels, Table 9: CDMESDS device classification levels,Section 5.1.3: Ground connections</td></tr><tr><td rowspan=1 colspan=1>1-Jul-2022</td><td rowspan=1 colspan=1>4</td><td rowspan=1 colspan=1>Added:Section 5.1.6Section 5.1.4Section 5.1.7Updated Section 3.2.2</td></tr></table>

# IMPORTANT NOTICE  READ CAREFULLY

pt old ursant  dits   leole.

purchasers' products.

No license, express or implied, to any intellectual property right is granted by ST herein.

re the property of their respective owners.