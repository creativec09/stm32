# Guidelines for thermal management on STM32 applications

# Introduction

Thisdocument describes the thermal management guidelines orapplications based on 32 microcontroller

th the specification.

T refers to the ambient temperature, and possibly also to the junction temperature.

product operating-temperature range specification.

# 1 General information

# Note:

This document applies to STM32 Arm®-based devices.   
Arm is a registered trademark of Arm Limited (or its subsidiaries) in the US and/or elsewhere.

# arm

# 2 Thermal systems definitions and basic concepts

This section details basic definitions and concepts related to thermal systems, as applied to silicon-based integrated circuits (ICs).

# Thermal systems definitions

# Heat:

Th mount nergyexchang etween iffeent bodontneousldehfheifnt temperatures.

# Temperature:

Acomparative measurement of how hot or cold a body is.The temperature o a given body increases as it absorbs heat and decreases as it releases heat.

# Temperature gradient:

Refer tthe uneven temperaturedistribution over e body.The temperature gradient magnitde efle the difference in temperature from one location to another inside a body.

# Thermal resistance:

The property of a material to conduct a certain amount of heat under a certain temperature gradient.

# 2.2 Thermal system study

Thermal systems are designed with complex thermal models and advanced simulation software tools.   
These models and tools are used to obtain accurate results.

Trolvethermal system wih an acptableaccuracyand wih limit coputation eormanysili hypotheses can be used (such as considering the thermal resistance to be temperature independent). Using e  h nao equivalent to the electrical resistance.

![](images/b1f69eaa3c8b8f85fe116c4d38753a6d0380d6fc78f925f2c7efea8576336145.jpg)  
Figure 1. Analogy between electrical and thermal system domains

TmodewieyaceptyeelecondstyMos iducrnor roviheal preeh ackag ucbaplideancirnar bodis (like JEDEC EIA/JESD 51-X standards). Designers consider the provided thermal resistance parameters wdalwihe sailat  ee package for a given product.

# 2.3

# Thermal model of a chip carrier

A simplified thermal model for an LQFP-packaged STM32 product is provided in the figure below. All surface temperatures and thermal resistance (as defined by the JEDEC EIA/JESD 51-X standards) are depicted.

![](images/b0ee2b3a3a30628affdf2480b70bc6ecde36c21cdeaadc511d74259ab33a47ab.jpg)  
Figure 2. Thermal model of a chip carrier

The definitions of thermal parameters mentioned in this figure are listed in the table below.

Table 1. Thermal parameters   

<table><tr><td rowspan=1 colspan=1>Symbol</td><td rowspan=1 colspan=2>Description</td><td rowspan=1 colspan=2>Unit</td></tr><tr><td rowspan=1 colspan=1>TJ</td><td rowspan=1 colspan=2>Temperature of the die</td><td rowspan=5 colspan=2>C</td></tr><tr><td rowspan=2 colspan=1>TA</td><td rowspan=2 colspan=2>Temperature of surrounding air</td></tr><tr></tr><tr><td rowspan=1 colspan=1>Tc</td><td rowspan=1 colspan=2>Temperature of the package top</td></tr><tr><td rowspan=1 colspan=1>TB</td><td rowspan=1 colspan=2>Temperature of the board near the device</td></tr><tr><td rowspan=1 colspan=1>θJc</td><td rowspan=1 colspan=2>Thermal resistance between the die and the package</td><td rowspan=3 colspan=2>C/W</td></tr><tr><td rowspan=1 colspan=1>θJB</td><td rowspan=1 colspan=2>Thermal resistance between the die and the PCB on which the IC is mounted</td></tr><tr><td rowspan=1 colspan=1>θJA</td><td rowspan=1 colspan=2>Thermal resistance between the die and the air surrounding the die package</td></tr><tr><td rowspan=1 colspan=1>P_B</td><td rowspan=1 colspan=2>Amount of power dissipated by the device through the board</td><td rowspan=4 colspan=2>W</td></tr><tr><td rowspan=2 colspan=1>PC</td><td rowspan=2 colspan=2>Amount of power dissipated by the device through the package top</td><td rowspan=2 colspan=1></td><td rowspan=1 colspan=1></td></tr><tr><td rowspan=1 colspan=1></td></tr><tr><td rowspan=1 colspan=1>PT</td><td rowspan=1 colspan=2>The total power dissipated by the device (PT = PB + Pc)</td></tr></table>

# 3 STM32 thermal parameters

This section explains the STM32 thermal parameters as specified by their respective datasheets.

# 3.1 Ambient temperature

I W differnt waysmeasur Measurement parmeer   heistancebetween hemeasrement p n t interpretation of the results.

JEDECprovides a standar efition orbient peratur but hat denition  mited to he JEDEC test environment used when determining package thermal characteristics.

MelanJa JEDEefheal tan i-ob atuJA)o illable performance high-power-dissipation devices.

# 3.2

# Junction temperature

The junction temperatureis the widely used term t eer  the temperature  adObviously, he ie unt tl a device.

oT the Inpacti eatureralyonereeoryriny temperaturemeasurement is rovideTh reduction  temperature gradintntoe temperaturei introduces a small uncertainty into subsequent assumptions and computations when the die dimensions are relatively small. This is the case for most STM32 devices.

# 3.3

# Ambient temperature versus junction temperature

Both the ambient and the junction temperatures specify the thermal performance of STM32 devices.

For many  devis, nly heaxiu mbient tperatur  pecifi  heheral peormanc .   
The junction temperature is also sometimes added.

Tubn pratuheal onen u ashanue temperature, as the die of a packaged device is not accessible. This makes the conventional temperature measurement methods unusable for measuring the die temperature.

Measuring the junction temperature requires more advanced measurement techniques. Most STM32 devices embed a junction temperature sensor, which serves as a primitive building block for thermal watchdog implementations. But at the design stage, this embeded temperature sensor cannot help in determining the It isbasedon many parameters including the application power profie,he devichermal resitanc, the surrounding temperature (board temperature and device case temperature). For accurate estimation  the junction teperaturemodelig software tols areused when the al aplicationhas a complex theral del and a complex power profile.

# 3.4 Case temperature

T J standar speciy hat he teperature snormust e plac  e center e package o usi conductive epoxy.

If e packagecas-t-ambint herma resistancmuch highe than he package juncton-t-caseeral reisance oneordermagnitudeat least), nd smost devics issipate powergoes trough he borhe junction temperature can be conflated with case temperature if some uncertainty is acceptable.

# 3.5 Board temperature

The board temperature, as defined by the JEDEC standards, is the PWB temperature easured near he center leof he longest sidef the device The board temperature and the package junction-to-board thermal resistance are very critical parameters when assessing the device thermal performance.

Undsteaddits, msehet genrat yhedeviisipathro hebare dissipated through the board can be 20 times higher than the heat dissipated through the package top. Fce JDE-ivi ar nes %v dissipation passes through the board and only 5% is dissipated through the package top.

# STM32 thermal parameters

Most of the STM32 datasheets give only Theta-JA thermal resistance, but some specify also Theta-JC and Theta-JB, defined in the table below.

Table 2. STM32 thermal resistances   

<table><tr><td rowspan=1 colspan=1>Thermal metric</td><td rowspan=1 colspan=1>Symbol</td><td rowspan=1 colspan=1>Value</td><td rowspan=1 colspan=1>Main purpose</td></tr><tr><td rowspan=1 colspan=1>Theta-JA</td><td rowspan=1 colspan=1>θJA</td><td rowspan=1 colspan=1>Tj-TAPt</td><td rowspan=1 colspan=1>Used to rank package performance in the JEDECenvironment</td></tr><tr><td rowspan=1 colspan=1>Theta-JC</td><td rowspan=1 colspan=1>θJc</td><td rowspan=1 colspan=1>Tj-TcPC</td><td rowspan=1 colspan=1>Used to rank package performanceUsed in simulations with a 2R model (2R = tworesistances</td></tr><tr><td rowspan=1 colspan=1>Theta-JB</td><td rowspan=1 colspan=1>θJB</td><td rowspan=1 colspan=1>Tj-TBPB</td><td rowspan=1 colspan=1>Used to rank package performanceUsed in simulations with 2R model</td></tr></table>

Th prrdetenderheollog pectnshat oet conditions:

Theta-JA: The JEDEC51-2 document Integrated circuits thermal test method environmental conditions - natural convection (still air) describes the thermal test method to define Theta-JA.   
Theta-JB: The JEDEC51 document Integrated circuit thermal test method environmental conditions - junction-to-board describes the thermal test method to define Theta-JB.   
Theta-JC: The MIL-STD-883E document Test method standard microcircuits describes the thermal test method to define Theta-JC.

These thermal resistances must be carefully defined in semiconductor packages and devices context.

Tmosn ooela ai oe two following "points":

The junction Ambient or board temperature

Theo etneu paral heral pathe yteaowig som e heat  "kwayAll heat leaving the junction eventually arrives at or passes through the other point.

It part that flows through the air gap under the package.

l oc the heat flows out through the top and the bottom of the device.

# Power dissipation and cooling methods

This section provides recommendations for efficient thermal analysis on STM32 applications, focusing on the following points:

poe disipation an  varition wit factors nameVTA (proes, voltage, unctin)tmperature, ad   
activity)   
how to minimize the power consumption   
how to optimize the thermal dissipation

# 1 Power dissipation

There are two types of current consumed by the device:

Thstatcurrent: ao call leakge curret,depends ne pros,volt anjuncion epue but does not depend on the activity   
The dynamic current: depends on the process, voltage, and activity but does not depend on the junction temperature (at least in first approximation).

Tak significantly change).

Therefore, the total current can be written as follows:

Ta ulatpl :he device and the (average) current consumed.

T jcnratucabovbintpeatualculat uc power and the junction-to-room thermal resistance.

The junction temperature must be kept lower than the maximum target given by the following equation:

# Important:

In this simplifed formula used only ordidactc purpose, Theta _room is a complex coefficient that is not a device characteristic but a system one (device + other components + boards + casing).

Te owg tho kehecn patubelobn patudtaiex sections:

Limiting Pdiss Limiting Theta_room (cooling system, host board and casing design)

# 4.2

# Minimizing power consumption (Pdiss)

e ptne ctuepl olS v multe eT to optimize the power efficiency (see the corresponding datasheets for more details).

T powcnpton prosovar wi eliatiSepliatins moshe m working on u r mite capacity nly when an event occurs.Someothers demand a regular world.

For these various power profiles, the user programmer enables the low-power modes by software.

The most common available modes are listed below:

Pa ptnuternt  rei a use.   
Cloc gatings:educes ynamic powerdissipation byshutting down clocks to a circuit or portion clock tree.   
Dynamic voltage scaling: power management technique where the voltage is increased or decreased, depending upon circumstances.   
Dynamic frequency scaling (also known as throttling when applied to a CPU): frequency automatically adjusted on-the-fly depending on the actual needs, to conserve power and reduce the amount of heat generated.

All these modes are available, for example, on STM32H7 and STM32MP1 series devices (see the reference manuals for more details).

# Power dissipation variation with junction temperature

I junction temperature.

eak ly significantly change).

The power dissipation variation with junction temperature has the following main consequences:

A cooling solution must be implemented to limit the junction temperature below 25  (maximum junction temperature).   
Iol so f,ee ealaty destructive.

When performing ystem-level thermal simulations in thedesign phase, fundamental toinput junction temperature dependent power dissipation.

# 4.4 Risk of thermal runaway

The junction-to-room temperature thermal resistance, Theta__room, characterizes the cooling system of a design.

This thermal resistance gives the capability to dissipate power in the design while limiting the juncion temperature.

he following equation gives the heat dissipation capability (HDC):

![](images/5c75d454d08c95ba9ed2a7ecd5e223efe7d36e5ce084080200c564396a45a79e.jpg)

![](images/9e68b0ab73fd7c91058617551579880f0580bd7f828a05f8fd34491fa6609fff.jpg)  
Figure 3. HDC (heat dissipation capability)

Note: Better: design has more ability to dissipate heat Worse: design has less ability to dissipate heat

# Case 1

T ie re ee ).

![](images/5426a20b0b5f0f23cff71114bc5dca78fc1830998c9811d2fc6d441df3be0854.jpg)  
Figure 4. HDC and junction-temperature-dependent dissipated power (case 1)

Tole oheaa poiexistTx junction temperature < 125 °C.

# Case 2

The figure below shows the efect of an increased room temperature (without changing any other factors).

![](images/cfa52b40affd7eb8eb5c5f79ee62ab7dfcda756a3f2551a4c6e4fcc0c9dd27a6.jpg)  
jigure 5. HDC and junction-temperature-dependent dissipated power (case 2

# Case 3

Thefgur belowshowshe efec anceasd junction-o-oomhermal eistan withou angig y other factors).

![](images/233387f04a0d8b142b70d2b880facaff3261c016dfd82bd34d9e24d67b94e5b6.jpg)  
Figure 6. HDC and junction-temperature-dependent dissipated power (case 3)

Tural po e a condition of thermal runaway.

# Case 4

The figure below shows the efect  decrease n power dissipation (without changing any otherfactors).

![](images/d15226c81265fcfc2fb3d0087c67e5937f860002bda2b6697483f0c1cf9e0b50.jpg)  
Figure 7. HDC and junction-temperature-dependent dissipated power (case 4)

# 5 Cooling

# 5.1

# Power dissipation paths

The power dissipated by the die is extracted along the two following main paths

top side: power dissipated from the top side, by a heat sink through an optional TM, thermal interface   
material)   
bot side: power dissipated from the bottom side by the C, by botom metal plate through an otinal   
TIM)

![](images/a76aaeba6a8de06ddcd63dbc48ca3a28e28feba98b2f5ad3875e0f8058079805.jpg)  
Figure 8. Power dissipation paths

# 5.2

# Main cooling methods

The heat sik and the CB dissipate he power the surrounding environment b the convcion and ratin methods.

# 5.2.1

# Natural convection

T matural cvtis s wheno  us ihe casiTh colgmethos ca natural convection and radiation that always work in parallel.

# 5.2.2 Forced convection

The term 'forced convection' is used when a fan is used in the casing.

# 5.2.3

# Natural and forced convection comparison

The table below details the main comparison factors between the natural and forced convection.

Table 3. Natural and forced convection comparison   

<table><tr><td rowspan=1 colspan=1>Comparison factors</td><td rowspan=1 colspan=1>Natural convection</td><td rowspan=1 colspan=1>Forced convection</td></tr><tr><td rowspan=1 colspan=1>Cooling efficiency</td><td rowspan=1 colspan=1>Low</td><td rowspan=1 colspan=1>Medium to high(depending on air speed)</td></tr><tr><td rowspan=1 colspan=1>Cost</td><td rowspan=1 colspan=1>Low (no fan)</td><td rowspan=1 colspan=1>Higher (cost of the fan)</td></tr><tr><td rowspan=1 colspan=1>Reliability</td><td rowspan=1 colspan=1>Higher(no moving parts)</td><td rowspan=1 colspan=1>Lower(mechanical part moving)</td></tr><tr><td rowspan=1 colspan=1>Acoustic noise</td><td rowspan=1 colspan=1>None</td><td rowspan=1 colspan=1>Small to medium(depending on air speed)</td></tr><tr><td rowspan=1 colspan=1>Possibility to control cooling efficiency based on needs</td><td rowspan=1 colspan=1>None</td><td rowspan=1 colspan=1>Yes, by varying fan voltage</td></tr></table>

# 5.3

# Bottom cooling - host PCB design

l  n the recommended stack-up and to optimize the PCB layout beneath the package.

Asnificant power proportion drawn rom e package to ambient atroug thehost board b the path detaile in the next sections (sorted by decreasing order  importance.The design rule mplementatin for ground and power connections is necessary for cooling and power distribution.

It own requirements.

# Host PCB ground and power layout

Teground (ND) plane must have a low resistance (thermal and electrical) or ll CB areas.This proves qual e y with multiple vias maintain the resistance at a low level.

Plac manyheral viass possiblenegrouan powr planes us belowe packagesush ther  nough contiuus coper between hejacen s or powristribution and thermal dsiatin. A compromise must be found.

The possible thermal vias are listed below:

ground vias: connecting GND to the unified GND plane (these are the most efficient thermal vias) power vias: connecting power to the power plane

The thermal vis conduct heat fom he evice  the internal ND and power planes.These planes spred he heat inside the PCB that acts as a planar heat sink.

# 5.3.2

# Additional GND areas on outer layers

Onthe outer ayers, some GND areas can be added whereverunctional tracks are absent Connect these areas to GND by a network of vias wherever possible.

ares eh g sat alogeoargulo hows additional GND areas and vias to the GND plane.

![](images/c1c9e71a38b7a16206570e6085db2048beaa62d8777e27b63d963892a1b325db.jpg)  
Figure 9. Principle of additional GND areas and vias to the GND plane

# 6 Thermal analysis examples

This section shows examples of thermal analysis performed on a discovery kit (STM32H747XI MCU), an evaluation board (STM32MP157), and an internal validation board (STM32MP135 MPU).

These analyses provide some answers to the following questions (at maximum ambient temperature 85)

How much does the power dissipation admit the leakage?   
Is Tj < 125 °C?   
Is there a risk of thermal runaway?

# Discovery kit with STM32H747XI MCU

This thermal analysis has been done on a Discovery kit with an STM32H747XI device (STM32H7471-DISCO), without casing (see the figure below).

This picture is not contractual.

![](images/fa1200d66ab3122371e81e5ff26958cf08aabd88443be660d81110e8d572aeb8.jpg)  
Figure 10. STM32H747I-DISCO

The test case is the following:

Run mode (400 MHz) data processing running from the flash memory   
Cache ON   
All peripherals enabled The temperature sensor connected to the ADC3 VINP [18] input channel, is used for TJ measurement.   
The TJ measurements are read via the USART2 using the DMA transfer, without CPU interruption.

# 6.1.1

# STM32H7 power dissipation

As tate  Sect, he issipat power ar wi.Te power onsption n hi xampl smes for different Tj values (see the table and the figure below).

Table 4. STM32H747XI power dissipation versus Tj   

<table><tr><td rowspan=2 colspan=1>T(</td><td rowspan=1 colspan=2>STM32H747I-DISCO (supplied with 5 V)</td><td rowspan=2 colspan=1>STM32H747XI power dissipation (mW)</td></tr><tr><td rowspan=1 colspan=1>Current consumption (A)</td><td rowspan=1 colspan=1>Power consumption (mW)</td></tr><tr><td rowspan=1 colspan=1>46.9</td><td rowspan=1 colspan=1>0.395</td><td rowspan=1 colspan=1>1975</td><td rowspan=1 colspan=1>737</td></tr><tr><td rowspan=1 colspan=1>51.8</td><td rowspan=1 colspan=1>0.405</td><td rowspan=1 colspan=1>2025</td><td rowspan=1 colspan=1>769</td></tr><tr><td rowspan=1 colspan=1>55.8</td><td rowspan=1 colspan=1>0.412</td><td rowspan=1 colspan=1>2060</td><td rowspan=1 colspan=1>788</td></tr><tr><td rowspan=1 colspan=1>61.5</td><td rowspan=1 colspan=1>0.423</td><td rowspan=1 colspan=1>2115</td><td rowspan=1 colspan=1>824</td></tr><tr><td rowspan=1 colspan=1>65.7</td><td rowspan=1 colspan=1>0.430</td><td rowspan=1 colspan=1>2150</td><td rowspan=1 colspan=1>852</td></tr><tr><td rowspan=1 colspan=1>71</td><td rowspan=1 colspan=1>0.442</td><td rowspan=1 colspan=1>2210</td><td rowspan=1 colspan=1>888</td></tr><tr><td rowspan=1 colspan=1>77.3</td><td rowspan=1 colspan=1>0.452</td><td rowspan=1 colspan=1>2260</td><td rowspan=1 colspan=1>920</td></tr><tr><td rowspan=1 colspan=1>81.9</td><td rowspan=1 colspan=1>0.465</td><td rowspan=1 colspan=1>2325</td><td rowspan=1 colspan=1>965</td></tr><tr><td rowspan=1 colspan=1>87.5</td><td rowspan=1 colspan=1>0.480</td><td rowspan=1 colspan=1>2400</td><td rowspan=1 colspan=1>1010</td></tr><tr><td rowspan=1 colspan=1>92</td><td rowspan=1 colspan=1>0.490</td><td rowspan=1 colspan=1>2450</td><td rowspan=1 colspan=1>1056</td></tr><tr><td rowspan=1 colspan=1>96.8</td><td rowspan=1 colspan=1>0.509</td><td rowspan=1 colspan=1>2545</td><td rowspan=1 colspan=1>1104</td></tr><tr><td rowspan=1 colspan=1>102.5</td><td rowspan=1 colspan=1>0.534</td><td rowspan=1 colspan=1>2670</td><td rowspan=1 colspan=1>1179</td></tr><tr><td rowspan=1 colspan=1>106.3</td><td rowspan=1 colspan=1>0.550</td><td rowspan=1 colspan=1>2750</td><td rowspan=1 colspan=1>1229</td></tr><tr><td rowspan=1 colspan=1>111.3</td><td rowspan=1 colspan=1>0.571</td><td rowspan=1 colspan=1>2855</td><td rowspan=1 colspan=1>1298</td></tr><tr><td rowspan=1 colspan=1>116.9</td><td rowspan=1 colspan=1>0.600</td><td rowspan=1 colspan=1>3000</td><td rowspan=1 colspan=1>1387</td></tr><tr><td rowspan=1 colspan=1>123</td><td rowspan=1 colspan=1>0.635</td><td rowspan=1 colspan=1>3175</td><td rowspan=1 colspan=1>1499</td></tr><tr><td rowspan=1 colspan=1>125</td><td rowspan=1 colspan=1>0.650</td><td rowspan=1 colspan=1>3250</td><td rowspan=1 colspan=1>1559</td></tr></table>

![](images/e69824d3898582d617d755b8cd8c1a869e7c57f20543ebde2c6b9c89094b9837.jpg)  
Figure 11. Junction-temperature-dependent dissipated power for STM32H7

# 6.1.2

# STM32H7 thermal measurements at TA = 25 °C

The figures and table below detail the thermal measurements performed at TA = 25 C.

![](images/57305d60a7a0931d4e627b61094755e5a0ce28a8b9964c24afdaf41ec14e3e42.jpg)  
Figure 12. STM32H747XI thermal measurements at TA = 25 °C

Table 5. STM32H7 thermal measurements at TA = 25°C   

<table><tr><td rowspan=2 colspan=1>T(</td><td rowspan=1 colspan=3>Thermal camera module measurement ()</td><td rowspan=2 colspan=1>STM32H7 power consumption(mW)</td><td rowspan=2 colspan=1>Total power consumption (mW)</td></tr><tr><td rowspan=1 colspan=1>Avg</td><td rowspan=1 colspan=1>Min</td><td rowspan=1 colspan=1>Max</td></tr><tr><td rowspan=1 colspan=1>46.9</td><td rowspan=1 colspan=1>45.5</td><td rowspan=1 colspan=1>39.7</td><td rowspan=1 colspan=1>50.6</td><td rowspan=1 colspan=1>737</td><td rowspan=1 colspan=1>1975</td></tr></table>

![](images/200b6b9c8cdb95b8879fa4e7df640c88fe4a2945f6f9a54f795f1f6f8faa3284.jpg)  
Figure 13. HDC at 25 °C and junction-temperature-dependent dissipated power for STM32H7

Once the design HDC is defined (by measurement at 25 C), and assuming that this HDC is constant at 25 an 8 , the operating point of the design at 8 is given by translating the DC at 8 See the figuen table below.

![](images/35ed93314ad744eda956d3b286cba31830441efb535e8351b8547e7cae4b0c4f.jpg)  
Figure 14. HDC at 85 °C and junction-temperature-dependent dissipated power for STM32H7

Table 6. Measurement interpolation at TA = 85 °C for STM32H7   

<table><tr><td rowspan=1 colspan=1>Parameter</td><td rowspan=1 colspan=1>Value</td></tr><tr><td rowspan=1 colspan=1>TJ</td><td rowspan=1 colspan=1>119</td></tr><tr><td rowspan=1 colspan=1>Ptot</td><td rowspan=1 colspan=1>3050 mW</td></tr></table>

In conclusion, the STM32H7 device is safe, with no thermal runaway, and Tj remaining < 125 C.

# 6.2

# Evaluation board with STM32MP157 MPU

This thermal analysis has been done on an evaluation board with an STM32MP157 device, without casing (see the figure below).

This picture is not contractual.

![](images/9e26d64afd9e92eb38f2bdf74d3dace9d204119b71635d249d58f1123b74840a.jpg)  
Figure 15. STM32MP157x-EV1

While running commands, the script monitors the following:

The CPU load with mpstat   
The board temperature via / sys / class / hwmon / hwmon0 / templ_input   
The memory used via the free command

# 6.2.1

# STM32MP157 power dissipation

As tate  Sect he issipat powerars wi.Te powerconsupion n i exampl sme for different Ty values (see the table and the figure below).

Table 7. STM32MP157 power dissipation versus TJ   

<table><tr><td rowspan=2 colspan=1>T(</td><td rowspan=1 colspan=2>STM32MP157x-EV1 board (supplied with 5 V)</td><td rowspan=2 colspan=1>STM32MP157 power dissipation (mW)</td></tr><tr><td rowspan=1 colspan=1>Current consumption (A)</td><td rowspan=1 colspan=1>Power consumption (mW)</td></tr><tr><td rowspan=1 colspan=1>39</td><td rowspan=1 colspan=1>0.4</td><td rowspan=1 colspan=1>2000</td><td rowspan=1 colspan=1>970.2</td></tr><tr><td rowspan=1 colspan=1>46</td><td rowspan=1 colspan=1>0.4</td><td rowspan=1 colspan=1>2000</td><td rowspan=1 colspan=1>973.8</td></tr><tr><td rowspan=1 colspan=1>65</td><td rowspan=1 colspan=1>0.405</td><td rowspan=1 colspan=1>2025</td><td rowspan=1 colspan=1>1006.4</td></tr><tr><td rowspan=1 colspan=1>81</td><td rowspan=1 colspan=1>0.41</td><td rowspan=1 colspan=1>2050</td><td rowspan=1 colspan=1>1053.1</td></tr><tr><td rowspan=1 colspan=1>95</td><td rowspan=1 colspan=1>0.42</td><td rowspan=1 colspan=1>2100</td><td rowspan=1 colspan=1>1104.7</td></tr><tr><td rowspan=1 colspan=1>106</td><td rowspan=1 colspan=1>0.432</td><td rowspan=1 colspan=1>2160</td><td rowspan=1 colspan=1>1195.5</td></tr><tr><td rowspan=1 colspan=1>116</td><td rowspan=1 colspan=1>0.445</td><td rowspan=1 colspan=1>2225</td><td rowspan=1 colspan=1>1280.6</td></tr><tr><td rowspan=1 colspan=1>125</td><td rowspan=1 colspan=1>0.456</td><td rowspan=1 colspan=1>2280</td><td rowspan=1 colspan=1>1366.6</td></tr></table>

![](images/f2f25cb1f1003eab4ed1d7c1624bfad14f3244f94d0efcf8ad9ff22e02adef3f.jpg)  
Figure 16. Junction-temperature-dependent dissipated power for STM32MP157

# 6.2.2

# STM32MP157 thermal measurements at TA = 25 °C

The figures and table below detail the thermal measurements performed at TA = 25 C.

![](images/7a92aefd1c10ada8c63cd67f70de23bee3389cf1db66fc9b181366fd44a19528.jpg)  
Figure 17. STM32MP157 thermal measurements at TA = 25 °C   
Table 8. STM32MP157 thermal measurements at TA = 25 °C

<table><tr><td rowspan=2 colspan=1>T(</td><td rowspan=1 colspan=3>Thermal camera measurement ()</td><td rowspan=2 colspan=1>STM32MP157 power consumption (mW)</td><td rowspan=2 colspan=1>Total power consumption (mW)</td></tr><tr><td rowspan=1 colspan=1>Avg</td><td rowspan=1 colspan=1>Min</td><td rowspan=1 colspan=1>Max</td></tr><tr><td rowspan=1 colspan=1>46</td><td rowspan=1 colspan=1>46.2</td><td rowspan=1 colspan=1>40.52</td><td rowspan=1 colspan=1>51.4</td><td rowspan=1 colspan=1>974</td><td rowspan=1 colspan=1>2000</td></tr></table>

![](images/cbf400f7efa2de21b92ba9fe06d98ea5cee521fb4892e9dd40f954a1365600fc.jpg)  
Figure 18. HDC at 25 °C and junction-temperature-dependent dissipated power for STM32MP157

Once the HDC of the design is defined (by measurement at 25 C), and assuming that this HDC is constant at and 85 , the operating point of the design at 85 is given by translating the DC at 85  as shown the figure and table below.

![](images/35529155707ccc4075758d340fb97f12923eec03baabf63c3e3e466aa5e48ded.jpg)  
Figure 19. HDC at 85 °C and junction-temperature-dependent dissipated power for STM32MP157

Table 9. Measurement interpolation at TA = 85 °C for STM32MP157   

<table><tr><td rowspan=1 colspan=1>Parameter</td><td rowspan=1 colspan=1>Value</td></tr><tr><td rowspan=1 colspan=1>TJ</td><td rowspan=1 colspan=1>110</td></tr><tr><td rowspan=1 colspan=1>Ptot</td><td rowspan=1 colspan=1>2200 mW</td></tr></table>

In conclusion, the STM32MP157 device is safe, with no thermal runaway, and Tj remaining < 125 C.

# 6.3

# Internal validation board with STM32MP135 MPU

Thi thermal analysis has been done on an internal validation board with an TM32MP35 device without casing This analysis is based on the use cases detailed in the table below. They correspond to CPU frequenciso 900 MHz and 1 GHz:

Table 10. Use cases for STM32MP135 MPU   

<table><tr><td rowspan=1 colspan=1>Name</td><td rowspan=1 colspan=1>Description</td><td rowspan=1 colspan=1>CPU load</td><td rowspan=1 colspan=1>DDR load</td></tr><tr><td rowspan=1 colspan=1>cpuburn</td><td rowspan=1 colspan=1></td><td rowspan=1 colspan=1></td><td rowspan=1 colspan=1>R = 3 Mbyte/s, W = 0Mbyte/s, R&amp;W = 4 Mbyte/s</td></tr><tr><td rowspan=1 colspan=1>dd</td><td rowspan=1 colspan=1>Idle (weston launcher,netdata) + dual eth + USBhard drive + dd on hard drive(ETH cables unplugged)</td><td rowspan=1 colspan=1>100%</td><td rowspan=1 colspan=1>R = 129 Mbyte/s,W = 40 Mbyte/s,R&amp;W = 169 Mbyte/s</td></tr></table>

# 6.3.1

# STM32MP135 power dissipation

# 6.3.1.1

# Use case about cpuburn

A atSec eissipa powearwiTe powonspionn i eampl me for different Tj values (see the following tables and figure).

Table 11. STM32MP135 power dissipation versus Tj at 900 MHz (cpuburn)   

<table><tr><td rowspan=1 colspan=1>T(</td><td rowspan=1 colspan=1>STM32MP135 power dissipation (mW) at 900 MHz</td></tr><tr><td rowspan=1 colspan=1>20.00</td><td rowspan=1 colspan=1>711.44</td></tr><tr><td rowspan=1 colspan=1>31.00</td><td rowspan=1 colspan=1>721.04</td></tr><tr><td rowspan=1 colspan=1>43.00</td><td rowspan=1 colspan=1>740.00</td></tr><tr><td rowspan=1 colspan=1>47.00</td><td rowspan=1 colspan=1>748.83</td></tr><tr><td rowspan=1 colspan=1>52.00</td><td rowspan=1 colspan=1>757.93</td></tr><tr><td rowspan=1 colspan=1>56.00</td><td rowspan=1 colspan=1>763.62</td></tr><tr><td rowspan=1 colspan=1>66.00</td><td rowspan=1 colspan=1>791.42</td></tr><tr><td rowspan=1 colspan=1>71.00</td><td rowspan=1 colspan=1>804.79</td></tr><tr><td rowspan=1 colspan=1>78.00</td><td rowspan=1 colspan=1>823.36</td></tr><tr><td rowspan=1 colspan=1>86.00</td><td rowspan=1 colspan=1>857.92</td></tr><tr><td rowspan=1 colspan=1>91.00</td><td rowspan=1 colspan=1>881.62</td></tr><tr><td rowspan=1 colspan=1>96.00</td><td rowspan=1 colspan=1>903.01</td></tr><tr><td rowspan=1 colspan=1>98.00</td><td rowspan=1 colspan=1>914.23</td></tr><tr><td rowspan=1 colspan=1>101.00</td><td rowspan=1 colspan=1>926.44</td></tr><tr><td rowspan=1 colspan=1>106.00</td><td rowspan=1 colspan=1>951.83</td></tr><tr><td rowspan=1 colspan=1>111.00</td><td rowspan=1 colspan=1>973.00</td></tr><tr><td rowspan=1 colspan=1>116.00</td><td rowspan=1 colspan=1>994.98</td></tr><tr><td rowspan=1 colspan=1>119.00</td><td rowspan=1 colspan=1>1014.19</td></tr><tr><td rowspan=1 colspan=1>129.00</td><td rowspan=1 colspan=1>1110.12</td></tr><tr><td rowspan=1 colspan=1>139.00</td><td rowspan=1 colspan=1>1238.89</td></tr></table>

Table 12. STM32MP135 power dissipation versus TJ at 1 GHz (cpuburn)   

<table><tr><td rowspan=1 colspan=1>TJ(</td><td rowspan=1 colspan=1>STM32MP135 power dissipation (mW) at 1 GHz</td></tr><tr><td rowspan=1 colspan=1>21.60</td><td rowspan=1 colspan=1>795.45</td></tr><tr><td rowspan=1 colspan=1>32.00</td><td rowspan=1 colspan=1>800.12</td></tr><tr><td rowspan=1 colspan=1>37.00</td><td rowspan=1 colspan=1>806.26</td></tr><tr><td rowspan=1 colspan=1>44.00</td><td rowspan=1 colspan=1>825.79</td></tr><tr><td rowspan=1 colspan=1>49.00</td><td rowspan=1 colspan=1>833.00</td></tr><tr><td rowspan=1 colspan=1>56.00</td><td rowspan=1 colspan=1>841.39</td></tr><tr><td rowspan=1 colspan=1>61.00</td><td rowspan=1 colspan=1>861.53</td></tr><tr><td rowspan=1 colspan=1>68.00</td><td rowspan=1 colspan=1>890.82</td></tr><tr><td rowspan=1 colspan=1>76.00</td><td rowspan=1 colspan=1>912.60</td></tr><tr><td rowspan=1 colspan=1>83.00</td><td rowspan=1 colspan=1>936.60</td></tr><tr><td rowspan=1 colspan=1>89.00</td><td rowspan=1 colspan=1>967.97</td></tr><tr><td rowspan=1 colspan=1>100.00</td><td rowspan=1 colspan=1>1014.80</td></tr><tr><td rowspan=1 colspan=1>110.00</td><td rowspan=1 colspan=1>1061.20</td></tr></table>

Table 13. STM32MP135 thermal measurements at TA = 25 °C (cpuburn)   

<table><tr><td rowspan=1 colspan=1>Parameter</td><td rowspan=1 colspan=1>900 MHz</td><td rowspan=1 colspan=1>1 GHz</td><td rowspan=1 colspan=1>Unit</td></tr><tr><td rowspan=1 colspan=1>TJ</td><td rowspan=1 colspan=1>47</td><td rowspan=1 colspan=1>49</td><td rowspan=1 colspan=1>[C]</td></tr><tr><td rowspan=1 colspan=1>VCORE</td><td rowspan=1 colspan=1>1.32</td><td rowspan=1 colspan=1>1.332</td><td rowspan=1 colspan=1>M</td></tr><tr><td rowspan=1 colspan=1>ICORE</td><td rowspan=1 colspan=1>180</td><td rowspan=1 colspan=1>195</td><td rowspan=1 colspan=1>[mA]</td></tr><tr><td rowspan=1 colspan=1>PCORE</td><td rowspan=1 colspan=1>237</td><td rowspan=1 colspan=1>260</td><td rowspan=1 colspan=1>[mW]</td></tr><tr><td rowspan=1 colspan=1>VDD</td><td rowspan=1 colspan=1>3.33</td><td rowspan=1 colspan=1>3.321</td><td rowspan=1 colspan=1>M</td></tr><tr><td rowspan=1 colspan=1>IDD</td><td rowspan=1 colspan=1>13</td><td rowspan=1 colspan=1>19</td><td rowspan=1 colspan=1>[mA]</td></tr><tr><td rowspan=1 colspan=1>PDD</td><td rowspan=1 colspan=1>43</td><td rowspan=1 colspan=1>63</td><td rowspan=1 colspan=1>[mW]</td></tr><tr><td rowspan=1 colspan=1>VCPu</td><td rowspan=1 colspan=1>1.415</td><td rowspan=1 colspan=1>1.414</td><td rowspan=1 colspan=1>[V]</td></tr><tr><td rowspan=1 colspan=1>ICPU</td><td rowspan=1 colspan=1>306</td><td rowspan=1 colspan=1>331</td><td rowspan=1 colspan=1>[mA]</td></tr><tr><td rowspan=1 colspan=1>PCPU</td><td rowspan=1 colspan=1>432</td><td rowspan=1 colspan=1>468</td><td rowspan=1 colspan=1>[mW]</td></tr><tr><td rowspan=1 colspan=1>VDDR2</td><td rowspan=1 colspan=1>1.2</td><td rowspan=1 colspan=1>1.206</td><td rowspan=1 colspan=1>M</td></tr><tr><td rowspan=1 colspan=1>IDDR2</td><td rowspan=1 colspan=1>30</td><td rowspan=1 colspan=1>35.5</td><td rowspan=1 colspan=1>[mA]</td></tr><tr><td rowspan=1 colspan=1>PDDR2</td><td rowspan=1 colspan=1>36</td><td rowspan=1 colspan=1>43</td><td rowspan=1 colspan=1>[mW]</td></tr><tr><td rowspan=1 colspan=1>STM32MP135 power</td><td rowspan=1 colspan=1>748</td><td rowspan=1 colspan=1>834</td><td rowspan=2 colspan=1>[mW]</td></tr><tr><td rowspan=1 colspan=1>dissipation</td><td rowspan=1 colspan=2>+11%</td></tr></table>

![](images/4b2164ee06cba0008cdc3cd43086d56d648014657fbd6aef3e0f523c239502e1.jpg)  
Figure 20. Junction temperature-dependent dissipated power for STM32MP135 (cpuburn)

# 6.3.1.2

# Use case about dd

As stated in Section 3, the dissipated power varies with the Tj. The power consumption in this example is measured for different Tj values (see the following tables and figure).

Table 14. STM32MP135 power dissipation versus Tj at 900 MHz (dd)   

<table><tr><td rowspan=1 colspan=1>TJ ()</td><td rowspan=1 colspan=1>STM32MP135 power dissipation (mW) at 900 MHz</td></tr><tr><td rowspan=1 colspan=1>20</td><td rowspan=1 colspan=1>586.44</td></tr><tr><td rowspan=1 colspan=1>31</td><td rowspan=1 colspan=1>596.04</td></tr><tr><td rowspan=1 colspan=1>43</td><td rowspan=1 colspan=1>615.00</td></tr><tr><td rowspan=1 colspan=1>47</td><td rowspan=1 colspan=1>623.83</td></tr><tr><td rowspan=1 colspan=1>52</td><td rowspan=1 colspan=1>632.93</td></tr><tr><td rowspan=1 colspan=1>56</td><td rowspan=1 colspan=1>638.62</td></tr><tr><td rowspan=1 colspan=1>66</td><td rowspan=1 colspan=1>666.42</td></tr><tr><td rowspan=1 colspan=1>71</td><td rowspan=1 colspan=1>679.79</td></tr><tr><td rowspan=1 colspan=1>78</td><td rowspan=1 colspan=1>698.36</td></tr><tr><td rowspan=1 colspan=1>86</td><td rowspan=1 colspan=1>732.92</td></tr><tr><td rowspan=1 colspan=1>91</td><td rowspan=1 colspan=1>756.62</td></tr><tr><td rowspan=1 colspan=1>96</td><td rowspan=1 colspan=1>778.01</td></tr><tr><td rowspan=1 colspan=1>98</td><td rowspan=1 colspan=1>789.23</td></tr><tr><td rowspan=1 colspan=1>101</td><td rowspan=1 colspan=1>801.44</td></tr><tr><td rowspan=1 colspan=1>106</td><td rowspan=1 colspan=1>826.83</td></tr><tr><td rowspan=1 colspan=1>111</td><td rowspan=1 colspan=1>848.00</td></tr><tr><td rowspan=1 colspan=1>116</td><td rowspan=1 colspan=1>869.98</td></tr><tr><td rowspan=1 colspan=1>119</td><td rowspan=1 colspan=1>889.9</td></tr><tr><td rowspan=1 colspan=1>129</td><td rowspan=1 colspan=1>985.12</td></tr></table>

Table 15. STM32MP135 power dissipation versus Tj at 1 GHz (dd)   

<table><tr><td rowspan=1 colspan=1>TJ(</td><td rowspan=1 colspan=1>STM32MP135 power dissipation (mW) at 1 GHz</td></tr><tr><td rowspan=1 colspan=1>21.6</td><td rowspan=1 colspan=1>670.45</td></tr><tr><td rowspan=1 colspan=1>32</td><td rowspan=1 colspan=1>675.12</td></tr><tr><td rowspan=1 colspan=1>37</td><td rowspan=1 colspan=1>681.26</td></tr><tr><td rowspan=1 colspan=1>46</td><td rowspan=1 colspan=1>700</td></tr><tr><td rowspan=1 colspan=1>49</td><td rowspan=1 colspan=1>708.00</td></tr><tr><td rowspan=1 colspan=1>56</td><td rowspan=1 colspan=1>716.39</td></tr><tr><td rowspan=1 colspan=1>61</td><td rowspan=1 colspan=1>736.53</td></tr><tr><td rowspan=1 colspan=1>68</td><td rowspan=1 colspan=1>765.82</td></tr><tr><td rowspan=1 colspan=1>76</td><td rowspan=1 colspan=1>787.60</td></tr><tr><td rowspan=1 colspan=1>83</td><td rowspan=1 colspan=1>811.60</td></tr><tr><td rowspan=1 colspan=1>89</td><td rowspan=1 colspan=1>842.97</td></tr><tr><td rowspan=1 colspan=1>100</td><td rowspan=1 colspan=1>889.80</td></tr><tr><td rowspan=1 colspan=1>110</td><td rowspan=1 colspan=1>936.20</td></tr></table>

Table 16. STM32MP135 thermal measurements at TA = 25 °C (dd)   

<table><tr><td rowspan=1 colspan=1>Parameter</td><td rowspan=1 colspan=1>900 MHz</td><td rowspan=1 colspan=1>1 GHz</td><td rowspan=1 colspan=1>Unit</td></tr><tr><td rowspan=1 colspan=1>TJ</td><td rowspan=1 colspan=1>43</td><td rowspan=1 colspan=1>46</td><td rowspan=1 colspan=1>[C]</td></tr><tr><td rowspan=1 colspan=1>VCORE</td><td rowspan=1 colspan=1>1.32</td><td rowspan=1 colspan=1>1.32</td><td rowspan=1 colspan=1>[M]</td></tr><tr><td rowspan=1 colspan=1>ICORE</td><td rowspan=1 colspan=1>177</td><td rowspan=1 colspan=1>198</td><td rowspan=1 colspan=1>[mA]</td></tr><tr><td rowspan=1 colspan=1>PCORE</td><td rowspan=1 colspan=1>233</td><td rowspan=1 colspan=1>261</td><td rowspan=1 colspan=1>[mW]</td></tr><tr><td rowspan=1 colspan=1>VDD</td><td rowspan=1 colspan=1>3.33</td><td rowspan=1 colspan=1>3.33</td><td rowspan=1 colspan=1>[V]</td></tr><tr><td rowspan=1 colspan=1>IDD</td><td rowspan=1 colspan=1>13</td><td rowspan=1 colspan=1>19</td><td rowspan=1 colspan=1>[mA]</td></tr><tr><td rowspan=1 colspan=1>PDD</td><td rowspan=1 colspan=1>43</td><td rowspan=1 colspan=1>63</td><td rowspan=1 colspan=1>[mW]</td></tr><tr><td rowspan=1 colspan=1>VcPu</td><td rowspan=1 colspan=1>1.415</td><td rowspan=1 colspan=1>1.398</td><td rowspan=1 colspan=1>[V]</td></tr><tr><td rowspan=1 colspan=1>ICPU</td><td rowspan=1 colspan=1>173</td><td rowspan=1 colspan=1>199</td><td rowspan=1 colspan=1>[mA]</td></tr><tr><td rowspan=1 colspan=1>PCPU</td><td rowspan=1 colspan=1>244</td><td rowspan=1 colspan=1>278</td><td rowspan=1 colspan=1>[mW]</td></tr><tr><td rowspan=1 colspan=1>VDDR2</td><td rowspan=1 colspan=1>1.268</td><td rowspan=1 colspan=1>1.268</td><td rowspan=1 colspan=1>[V]</td></tr><tr><td rowspan=1 colspan=1>IDDR2</td><td rowspan=1 colspan=1>75</td><td rowspan=1 colspan=1>77</td><td rowspan=1 colspan=1>[mA]</td></tr><tr><td rowspan=1 colspan=1>PDdR2</td><td rowspan=1 colspan=1>95</td><td rowspan=1 colspan=1>97</td><td rowspan=1 colspan=1>[mW]</td></tr><tr><td rowspan=2 colspan=1>STM32MP135</td><td rowspan=1 colspan=1>615</td><td rowspan=1 colspan=1>700</td><td rowspan=2 colspan=1>[mW]</td></tr><tr><td rowspan=1 colspan=2>+13%</td></tr></table>

![](images/c8d37426b9059dbbc4b76636e3b9ab16854ca2943acdba848ba985f30e93638a.jpg)  
Figure 21. Junction temperature-dependent dissipated power for STM32MP135 (dd)

# 6.3.2

# HDC at 25 °C and junction temperature

Once the design HDC is defined (by measurement at 25 C), and assuming that this HDC is constant at 25 and 85 , the operating point of the design at 85  is given by translating the HDC at 85 Cas shown in he figure below.

![](images/44ff26f8995252110cd5ceb6e78dbba3bb21a122dcac985ae3b6968e640fbc35.jpg)  
Figure 22. MPU power dissipation   
Maximum ambient temperature (STM32MP135 MPU)

# 6.3.3

The maximum ambient temperature for the cpuburn and dd use cases are given in the figures below.

![](images/1168ca32e56250504cf1be1040154bef888a6066bee5d1521664d28ae92505c9.jpg)  
Figure 23. Maximum ambient temperature(Cpuburn)

![](images/5fb16b5de73e36a0a79e5433aa62f788befc7f662648c38913954ff5bd9abdfb.jpg)  
Figure 24. Maximum ambient temperature (dd)

# 6.3.4

# Conclusion

The measurement details given in the previous sections give:

An 11% and 13% increase of the power consumption between 900 MHz and 1 GHz. These are respectively for the cpuburn and dd use cases.   
A 2 and 3 °C increase of Tj between 900 MHz and 1 GHz (for cpuburn and dd use case respectively) No risk of thermal runaway

# Table 17 summarizes the maximum ambient temperature for various configurations.

Table 17. Maximum ambient temperature (STM32MP135 MPU)   

<table><tr><td rowspan=3 colspan=1>Frequency</td><td rowspan=1 colspan=4>Maximum ambient temperature ()</td></tr><tr><td rowspan=1 colspan=2>Tj = 105 </td><td rowspan=1 colspan=2>Tj = 125 </td></tr><tr><td rowspan=1 colspan=1>cpuburn</td><td rowspan=1 colspan=1>dd</td><td rowspan=1 colspan=1>cpuburn</td><td rowspan=1 colspan=1>dd</td></tr><tr><td rowspan=1 colspan=1>900 MHz</td><td rowspan=1 colspan=1>77.5</td><td rowspan=1 colspan=1>81</td><td rowspan=1 colspan=1>93.5</td><td rowspan=1 colspan=1>97.5</td></tr><tr><td rowspan=1 colspan=1>1 GHz</td><td rowspan=1 colspan=1>74</td><td rowspan=1 colspan=1>78</td><td rowspan=1 colspan=1>91</td><td rowspan=1 colspan=1>94</td></tr></table>

# 6.4

# Internal validation board with STM32MP257 MPU

This thermal analysis has been done on an internal validation board with an ST32MP257 device without casing. The test case is the following:

Glmark2-es2-drm Video decoder Endecoder Memtester1 Memtester2

# 6.4.1

# STM32MP257 power dissipation

a essa pv  Iu  p ope different TJ values.

![](images/7b62861e68a913ee23439b599c5a5d61b2bb9bbf4b0bc519de45cf4758c3ca4b.jpg)  
Figure 25. Junction temperature-dependent dissipated power for STM32MP257

# 6.4.2

# STM32MP257 thermal measurements at TA = 25 °C

he figures and table below detail the thermal measurements performed at TA = 25

![](images/10402ff31d875dc08554971df12298f6eac8b69e3e43b67f0abacfff04309ca2.jpg)  
Figure 26. STM32MP257 thermal measurements at TA = 25 °C

Table 18. STM32MP257 thermal measurements at TA = 25 °C   

<table><tr><td rowspan=2 colspan=1>(</td><td rowspan=1 colspan=3>Thermal camera module measurement ()</td><td rowspan=2 colspan=1>STM32MP257 power consumption (mW)</td></tr><tr><td rowspan=1 colspan=1>Avg</td><td rowspan=1 colspan=1>Min</td><td rowspan=1 colspan=1>Max</td></tr><tr><td rowspan=1 colspan=1>47.5 (1)</td><td rowspan=1 colspan=1>40.24</td><td rowspan=1 colspan=1>31.5</td><td rowspan=1 colspan=1>48.7</td><td rowspan=1 colspan=1>2164.77</td></tr></table>

1. Thermocouple measurement

Once the HDC of the design is defined (by measurement at 25 C), and assuming that this HDC is constant at and 85, the operating point of the design at 85 is given by translating the HDC at 85 Cas shown Figure 27 and Table 19.

![](images/34d504146fc83e786acb6c5eb400c0bba55b4ed3a1e6cd88b25bf16ba2f86ce6.jpg)  
Figure 27. HDC at 85 °C and junction temperature-dependent dissipated power for STM32MP257

Table 19. Measurement interpolation at TA = 85 °C for STM32MP257   

<table><tr><td rowspan=1 colspan=1>Parameter</td><td rowspan=1 colspan=1>Value</td></tr><tr><td rowspan=1 colspan=1>TJ</td><td rowspan=1 colspan=1>115</td></tr><tr><td rowspan=1 colspan=1>Ptot</td><td rowspan=1 colspan=1>2886.5 mW</td></tr></table>

In conclusion, the STM32MP257 device is safe, with no thermal runaway, and Tj remaining < 125 C.

# Discovery kit with STM32N657XOH3 MCU

This thermal analysis was done on a Discovery kit with an STM32N657XOH3 device without casing. The test case is the following:

Internal VDD_core voshigh-trusted.bin configuration CPU frequency = 800 MHz NPU frequency = 1000 MHz NPU RAM frequency = 900 MHz

STM32N6 max load application firmware:

Use DCMI and VENC in YUV2 (camera board MB1723C with OV5640 sensor)   
Use NPU inference   
Stream video on LTDC using GPUD2 accelerator

# 6.5.1

# STM32N657 power dissipation

As tate  Sect he issipat powerars wi.Te powerconsupion n i exampl sme for different Tj values (as Figure 28 below demonstrates).

![](images/3b3a5980f282ca658a9191e6fc39509a723ca7f5309403daf96d852b1b5272e8.jpg)  
igure 28. Junction-temperature-dependent dissipated power for STM32N65

# 6.5.2

# STM32N657 thermal measurements at TA = 25 °C

The figures and table below detail the thermal measurements performed at TA = 25 °C.

![](images/9559f9308b0108c2abbbb5951d46542f996699e7dafebfb0b492fa07b1321883.jpg)  
Figure 29. STM32N657 thermal measurements at TA = 25 °C

Table 20. STM32H7 thermal measurements at TA = 25 °C   

<table><tr><td rowspan=1 colspan=1>T()</td><td rowspan=1 colspan=1>Thermal camera module measurement (°)Max</td><td rowspan=1 colspan=1>STM32N657 power consumption (mW)</td></tr><tr><td rowspan=1 colspan=1>47(1)</td><td rowspan=1 colspan=1>48.7</td><td rowspan=1 colspan=1>1318</td></tr></table>

# 1. Thermocouple measurement

Once the heat dissipation capability (HDC) of the design has been defined (by measurement at 25 C), and aing hat hiHDC is onstant at andmaxium ambient tmperature he erating point  the at Tj = 125 °C is given by translating the HDC, as shown in the figure and table below.

![](images/eab1c997cda10970785ad5d39a635361a5866ea27080372a5bfe21ba39a9e083.jpg)  
Figure 30. HDC at max ambient temperature and junction temperature-dependent dissipated power for STM32N657

Table 21. Measurement interpolation at maximum ambient temperature for STM32N657   

<table><tr><td rowspan=1 colspan=1>Parameter</td><td rowspan=1 colspan=1>Value</td></tr><tr><td rowspan=1 colspan=1>TJ</td><td rowspan=1 colspan=1>125°</td></tr><tr><td rowspan=1 colspan=1>Ptot</td><td rowspan=1 colspan=1>2082 mW</td></tr><tr><td rowspan=1 colspan=1>Max ambient temperature</td><td rowspan=1 colspan=1>91</td></tr></table>

In conclusion, the STM32N657 device is safe, with no thermal runaway, and for Tj = 125 C, the maximum ambient temperature = 91 °C.

# Revision history

Table 22. Document revision history   

<table><tr><td rowspan=1 colspan=1>Date</td><td rowspan=1 colspan=1>Version</td><td rowspan=1 colspan=1>Changes</td></tr><tr><td rowspan=1 colspan=1>24-May-2018</td><td rowspan=1 colspan=1>1</td><td rowspan=1 colspan=1>Initial release.</td></tr><tr><td rowspan=1 colspan=1>4-Mar-2019</td><td rowspan=1 colspan=1>2</td><td rowspan=1 colspan=1>Updated:Title of the documentSection 2.3 Thermal model of a chip carrierSection 3.3 Ambient temperature versus junction temperatureSection 3.5 Board temperatureSection 4 Power dissipation and cooling methodsAdded:Section 3.6 STM32 thermal parameters•    Section 6 Thermal analysis example</td></tr><tr><td rowspan=1 colspan=1>19-Apr-2019</td><td rowspan=1 colspan=1>3</td><td rowspan=1 colspan=1>Updated Section 3.6 STM32 thermal parameters.Added Section 6.2 Discovery kit with STM32H747XI MCU.</td></tr><tr><td rowspan=1 colspan=1>28-Feb-2023</td><td rowspan=1 colspan=1>4</td><td rowspan=1 colspan=1>Updated:Section orders between Section 6.1 and Section 6.2Section 6.2 Evaluation board with STM32MP157 MPUFigure 3. HDC (heat dissipation capability)Added Section 6.3 Internal validation board with STM32MP135 MPU</td></tr><tr><td rowspan=1 colspan=1>11-Oct-2023</td><td rowspan=1 colspan=1>5</td><td rowspan=1 colspan=1>Updated:•    Document title•    Figure 20. Junction temperature-dependent dissipated power forSTM32MP135 (cpuburn)</td></tr><tr><td rowspan=1 colspan=1>28-Jun-2024</td><td rowspan=1 colspan=1>6</td><td rowspan=1 colspan=1>Added Section 6.4: Internal validation board with STM32MP257 MPU</td></tr><tr><td rowspan=1 colspan=1>21-Nov-2024</td><td rowspan=1 colspan=1>7</td><td rowspan=1 colspan=1>Added Section 6.5: Discovery kit with STM32N657XOH3 MCU</td></tr></table>

# Contents

# 1 General information

# 2 Thermal systems definitions and basic concepts.

2.1 Thermal systems definitions 3   
2.2 Thermal system study.   
2.3 Thermal model of a chip carrier.

# STM32 thermal parameters 5

3.1 Ambient temperature .5   
3.2 Junction temperature 5   
3.3 Ambient temperature versus junction temperature . 5   
3.4 Case temperature 5   
3.5 Board temperature 5   
3.6 STM32 thermal parameters . 6

# Power dissipation and cooling methods.

4.1 Power dissipation   
4.2 Minimizing power consumption (Pdiss)   
4.3 Power dissipation variation with junction temperature 8   
4.4 Risk of thermal runaway. 8

# Cooling. 11

5.1 Power dissipation paths. 11   
5.2 Main cooling methods. 11   
5.2.1 Natural convection 11   
5.2.2 Forced convection. 11   
5.2.3 Natural and forced convection comparison . 12

# 5.3 Bottom cooling - host PCB design 12

5.3.1 Host PCB ground and power layout 12   
5.3.2 Additional GND areas on outer layers. 13

# Thermal analysis examples 14

# 6.1 Discovery kit with STM32H747XI MCU 14

6.1.1 STM32H7 power dissipation 15   
6.1.2 STM32H7 thermal measurements at TA = 25 °C. 16

1.2 Evaluation board with STM32MP157 MPU 18

6.2.1 STM32MP157 power dissipation. 19

6.2.2 STM32MP157 thermal measurements at TA = 25 °C 20

5.3 Internal validation board with STM32MP135 MPU 22

6.3.1 STM32MP135 power dissipation. 22   
6.3.2 HDC at 25 C and junction temperature 26   
6.3.3 Maximum ambient temperature (STM32MP135 MPU) 26   
6.3.4 Conclusion 27

# 5.4 Internal validation board with STM32MP257 MPU 29

6.4.1 STM32MP257 power dissipation. 29   
6.4.2 STM32MP257 thermal measurements at TA = 25 C 29

5 Discovery kit with STM32N657XOH3 MCU . 30

6.5.1 STM32N657 power dissipation 31

6.5.2 STM32N657 thermal measurements at TA = 25 °C. 32

# Revision history 34

# List of tables

Table 1. Thermal parameters . 4   
Table 2. STM32 thermal resistances. 6   
Table 3. Natural and forced convection comparison 12   
Table 4. STM32H747XI power dissipation versus Tj 15   
Table 5. STM32H7 thermal measurements at TA = 25°C. 16   
Table 6. Measurement interpolation at TA = 85 C for STM32H7. 17   
Table 7. STM32MP157 power dissipation versus TJ 19   
Table 8. STM32MP157 thermal measurements at TA = 25 C 20   
Table 9. Measurement interpolation at TA = 85 °C for STM32MP157. 21   
Table 10. Use cases for STM32MP135 MPU. 22   
Table 11. STM32MP135 power dissipation versus Tj at 900 MHz (cpuburn) 22   
Table 12. STM32MP135 power dissipation versus Tj at 1 GHz (cpuburn) 23   
Table 13. STM32MP135 thermal measurements at TA = 25 °C (cpuburn) 23   
Table 14. STM32MP135 power dissipation versus TJ at 900 MHz (dd) 24   
Table 15. STM32MP135 power dissipation versus TJ at 1 GHz (dd) 25   
Table 16. STM32MP135 thermal measurements at TA = 25 C (dd) 25   
Table 17. Maximum ambient temperature (STM32MP135 MPU) 28   
Table 18. STM32MP257 thermal measurements at TA = 25 C 30   
Table 19. Measurement interpolation at TA = 85 °C for STM32MP257. 30   
Table 20. STM32H7 thermal measurements at TA = 25 C 33   
Table 21. Measurement interpolation at maximum ambient temperature for STM32N657 33   
Table 22. Document revision history . 34

# List of figures

Figure 1. Analogy between electrical and thermal system domains 3   
Figure 2. Thermal model of a chip carrier. 4   
Figure 3. HDC (heat dissipation capability) 8   
Figure 4. HDC and junction-temperature-dependent dissipated power (case 1) 9   
Figure 5. HDC and junction-temperature-dependent dissipated power (case 2) 9   
Figure 6. HDC and junction-temperature-dependent dissipated power (case 3) 10   
Figure 7. HDC and junction-temperature-dependent dissipated power (case 4) 10   
Figure 8. Power dissipation paths . . 11   
Figure 9. Principle of additional GND areas and vias to the GND plane . 13   
Figure 10. STM32H747I-DISCO. 14   
Figure 11. Junction-temperature-dependent dissipated power for STM32H7 15   
Figure 12. STM32H747XI thermal measurements at TA = 25 C. 16   
Figure 13. HDC at 25 C and junction-temperature-dependent dissipated power for STM32H7 16   
Figure 14. HDC at 85 C and junction-temperature-dependent dissipated power for STM32H7 17   
Figure 15. STM32MP157x-EV1 18   
Figure 16. Junction-temperature-dependent dissipated power for STM32MP157 19   
Figure 17. STM32MP157 thermal measurements at TA = 25 C 20   
Figure 18. HDC at 25 °C and junction-temperature-dependent dissipated power for STM32MP157. 20   
Figure 19. HDC at 85 C and junction-temperature-dependent dissipated power for STM32MP157. 21   
Figure 20. Junction temperature-dependent dissipated power for STM32MP135 (cpuburn) 24   
Figure 21. Junction temperature-dependent dissipated power for STM32MP135 (dd) 26   
Figure 22. MPU power dissipation 26   
Figure 23. Maximum ambient temperature(Cpuburn) 27   
Figure 24. Maximum ambient temperature (dd) 27   
Figure 25. Junction temperature-dependent dissipated power for STM32MP257 29   
Figure 26. STM32MP257 thermal measurements at TA = 25 C. 29   
Figure 27. HDC at 85 °C and junction temperature-dependent dissipated power for STM32MP257. 30   
Figure 28. Junction-temperature-dependent dissipated power for STM32N657 31   
Figure 29. STM32N657 thermal measurements at TA = 25 C 32   
Figure 30. HDC at max ambient temperature and junction temperature-dependent dissipated power for STM32N657 . . . . 33

# IMPORTANT NOTICE  READ CAREFULLY

pt old ursant  dits   leole.

purchasers' products.

No license, express or implied, to any intellectual property right is granted by ST herein.

are the property of their respective owners.

I

© 2024 STMicroelectronics - All rights reserved