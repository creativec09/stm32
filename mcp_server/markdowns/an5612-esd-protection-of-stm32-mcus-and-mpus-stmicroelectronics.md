# ESD protection of STM32 MCUs and MPUs

# Introduction

El MCU design challenges in building robust equipment.

must consider since the beginning of the design process.

ST32 MCU an MPU devibe roteon agais EDevent uri viandg nassbl ESD process must prevent them from any ESD stress exceeding that specification.

T   P i EMC appropriate protective solution to each of them.

# 1 General information

# Note:

This document applies to Arm®-based MCUs and MPUs.   
Arm is a registered trademark of Arm Limited (or its subsidiaries) in the US and/or elsewhere.

# arm

Table 1. Glossary of terms   

<table><tr><td rowspan=1 colspan=1>Term</td><td rowspan=1 colspan=1>Developed form</td></tr><tr><td rowspan=1 colspan=1>ANSI</td><td rowspan=1 colspan=1>American national standards institute</td></tr><tr><td rowspan=1 colspan=1>BLE</td><td rowspan=1 colspan=1>Bluetooth® Low Energy</td></tr><tr><td rowspan=1 colspan=1>CDM</td><td rowspan=1 colspan=1>Charged-device model</td></tr><tr><td rowspan=1 colspan=1>CSI</td><td rowspan=1 colspan=1>Camera serial interface</td></tr><tr><td rowspan=1 colspan=1>DSI</td><td rowspan=1 colspan=1>Display serial interface</td></tr><tr><td rowspan=1 colspan=1>D-PHY</td><td rowspan=1 colspan=1>Physical layer option set by MIPI alliance</td></tr><tr><td rowspan=1 colspan=1>ECMF</td><td rowspan=1 colspan=1>EMI/RFI common mode filter</td></tr><tr><td rowspan=1 colspan=1>EMIF</td><td rowspan=1 colspan=1>Electromagnetic interference filter</td></tr><tr><td rowspan=1 colspan=1>ESDA</td><td rowspan=1 colspan=1>ESD association</td></tr><tr><td rowspan=1 colspan=1>ESD</td><td rowspan=1 colspan=1>Electrostatic discharge</td></tr><tr><td rowspan=1 colspan=1>GPIO</td><td rowspan=1 colspan=1>General purpose input/output</td></tr><tr><td rowspan=1 colspan=1>JEDEC</td><td rowspan=1 colspan=1>Joint electron device engineering council</td></tr><tr><td rowspan=1 colspan=1>JTAG</td><td rowspan=1 colspan=1>Joint test action group</td></tr><tr><td rowspan=1 colspan=1>HBM</td><td rowspan=1 colspan=1>Human body model</td></tr><tr><td rowspan=1 colspan=1>IEC</td><td rowspan=1 colspan=1>International electrotechnical commission</td></tr><tr><td rowspan=1 colspan=1>MM</td><td rowspan=1 colspan=1>Machine model</td></tr><tr><td rowspan=1 colspan=1>MIPI</td><td rowspan=1 colspan=1>Mobile industry processor interface</td></tr><tr><td rowspan=1 colspan=1>MOV</td><td rowspan=1 colspan=1>Metal oxide varistor</td></tr><tr><td rowspan=1 colspan=1>NFC</td><td rowspan=1 colspan=1>Near-field communication</td></tr><tr><td rowspan=1 colspan=1>PCB</td><td rowspan=1 colspan=1>Printed circuit board</td></tr><tr><td rowspan=1 colspan=1>SMC</td><td rowspan=1 colspan=1>Surface mounted component</td></tr><tr><td rowspan=1 colspan=1>SMPS</td><td rowspan=1 colspan=1>Switch mode power supply</td></tr><tr><td rowspan=1 colspan=1>SWD</td><td rowspan=1 colspan=1>Serial wire debug</td></tr><tr><td rowspan=1 colspan=1>TVS</td><td rowspan=1 colspan=1>Transient voltage suppressor</td></tr><tr><td rowspan=1 colspan=1>VBR</td><td rowspan=1 colspan=1>Voltage breakdown</td></tr></table>

Table 2. Reference documents   

<table><tr><td>Reference number</td><td>Document title</td></tr><tr><td>[1]</td><td>EMC design guide for STM8, STM32 and Legacy MCUs, AN1709</td></tr><tr><td>[2]</td><td>ESD considerations for touch sensing applications on MCUs, AN3960</td></tr></table>

Table 3. Complementary literature available on www.st.com   

<table><tr><td>Category</td><td>Document</td></tr><tr><td>EMIF</td><td>HDMI ESD protection and signal conditioning products for STBs, AN5121</td></tr><tr><td colspan="1" rowspan="3">EMIF</td><td colspan="1" rowspan="1">IEC 61000-4-2 standard testing, AN3353</td></tr><tr><td colspan="1" rowspan="1">EMI filters for SD3.0 card high-speed SD card protection and filtering devices, AN4541</td></tr><tr><td colspan="1" rowspan="1">LC filters for mobile phone LCD and camera links, AN3141</td></tr><tr><td colspan="1" rowspan="4">ECMF</td><td colspan="1" rowspan="1">USB Type-C protection and filtering, AN4871</td></tr><tr><td colspan="1" rowspan="1">Antenna desense on handheld equipment, AN4356</td></tr><tr><td colspan="1" rowspan="1">IEC 61000-4-2 standard testing, AN3353</td></tr><tr><td colspan="1" rowspan="1">Common mode filters, AN4511</td></tr><tr><td colspan="1" rowspan="7">Protection</td><td colspan="1" rowspan="1">Increasing the ST25DV-I2C series Dynamic NFC Tags ESD robustness on antenna using anexternal ESD protection, AN5425</td></tr><tr><td colspan="1" rowspan="1">3.3 V RS485 compatible with 1.8 V I/Os and selectable speed 20 Mbps or 250 kbps, AN5245</td></tr><tr><td colspan="1" rowspan="1">Increasing the M24LRXXE-R family ESD robustness on antenna using an external ESD protection,AN4326</td></tr><tr><td colspan="1" rowspan="1">Fundamentals of ESD protection at system level, AN5241</td></tr><tr><td colspan="1" rowspan="1">USB Type-C protection and filtering, AN4871</td></tr><tr><td colspan="1" rowspan="1">HDMI ESD protection and signal conditioning products for STBs, AN5121</td></tr><tr><td colspan="1" rowspan="1">IEC 61000-4-2 standard testing, AN3353</td></tr></table>

# 2 Electrostatic discharge (ESD)

Thi section describes heelectrostatiisharge henmenonconsequences  ICs an standar pea to ESD.

# 2.1 ESD phenomenon

Elerostaticdischarge (ED) is a suden andmomentary fow electricurrent between two electrically charged objects. It is triggered upon contact, an electrical short, or dielectric breakdown.

On an elecical aplianc, temostcoon entry points r ED anteaces such  coecors r interface devices.

The curetndus hi voltagpiks arfl  ensitivelectronevis sc miocntrolles.   
ESD protection methodordevice adapted to theoperating environment iused t prevent them from damage.

Eleostaarging ocivali oonyuultpl failure, such as metallization defect, oxide breakdown, and burn defect.

# Metallization defect

An ecessive current hrough ametal track cause a local ot spot and meltsthe metal.This can creat circuits or/and shorts between metal tracks.

![](images/4ef653cd5d670316ea13de52c60f55d7577fcee4456fef18883ee52472a9509d.jpg)  
Figure 1. Example of metallization defect

# Oxide breakdown defect

Asi hol exces 800 .The damage to the dielectric usually causes permanent leakage that may induce sequential failures.

![](images/c0dcc83a19ae6140e7d02d06edbe03aebeb1a9c9554cdfcfe598b480499fa894.jpg)  
Figure 2. Example of oxide breakdown defect

# Burn defect

Hot metal from the bonding pad, melted due to an ESD, leaks, and burns the silicon, bonding, or the pad.

![](images/be4635991f18c39cddc02b7001f45dcd39cc4767679870986983b87a18d31dd4.jpg)  
Figure 3. Example of burn defect

Theay caue/ eava ilt ar). Damage in the device can be such as:

short or open connection   
shift of impedances   
extra leakage   
overconsumption due to a resistive path to the ground or another internal structure

alp immediate or delayed, for example few power on/off cycles after the EsD stress.

STM32 devices embeprotection  sustai standard factory manipulation and basic protectionexternal ut u pads.mbedeD protectin conses siniiantilicon arAt syste level issuffint t nly he eny point  cosa poie he sur pec evi o mple without impacting the application behavior.

T protected. As the buttons are in direct contact with the user, they are a possible source of ESD.

![](images/b42f923651bc9dc15f81af0a1060f9aaaa731d7ddc2bb9b2bdf41499859d393e.jpg)  
Figure 4. Application variants with protected and unprotected STM32 device

# ESD protection level quantification

International standards pertaining to the ESD protection come from the following bodies:

American national standards institute (ANSI) International electrotechnical commission (IEC) ESD association (ESDA) Joint electron device engineering council (JEDEC)

There are three commonly used models:

Human body model (HBM), representing the manipulation of the product by humans   
Charged-device model (cDM), representing conditions of manufacturing environment such as mechanical device handling   
Machine model (MM), becoming obsolete due to similarity with HBM.

The JEDEstandard pertains  hemanuacturing evioent. I ais  protecting part againstD oroduction machinery (CDM) and human manipulation (HBM).

The IEC00 tanr aims sug that he par utainhe reshat they fc hele equipment in operation.

The great variety  different 3applications can expose the T32 devices o ery different conditions rom the ED stress perspective. Iisnot possible to ompare system ESD robustess from an IC stanpoint in such coitons.Toguideusernargetng  C0 class,hedevicatasheet provides val ba an estimated typical usage and PCB shapes. Relevant details are available in [1].

The STM32 device datasheet provides two types of data:

Absolute maximum rating: based on JEDEC, performed on unpowered devices, functionality validated afterwards.   
Functional susceptibility test: based on IEC 61000-4-2, performed on devices in operation, highlighting the effective operation or self-recovery capabilities of a system.

Check for more details in [1].

# ESD protection requirements in application

The electronic equipment must comply with applicable industry standards in term of robustness with stress ind by Es.Te protecion requiements or military and healthcar aplications a moestricthan consumer applications.

The following table lists the ESD protection levels defined by IEC 61000-4-2 (HBM) and their equivalent test voltages.

Table 4. Sensitivity classification for the HBM (IEC 61000-4-2)   

<table><tr><td rowspan=5 colspan=1>Test typeContact discharge</td><td rowspan=1 colspan=1>Level</td><td rowspan=1 colspan=1>Test voltage</td></tr><tr><td rowspan=1 colspan=1>1</td><td rowspan=1 colspan=1>2 kV</td></tr><tr><td rowspan=1 colspan=1>2</td><td rowspan=1 colspan=1>4 kv</td></tr><tr><td rowspan=1 colspan=1>3</td><td rowspan=1 colspan=1>6 kV</td></tr><tr><td rowspan=1 colspan=1>4</td><td rowspan=1 colspan=1>8 kV</td></tr><tr><td rowspan=4 colspan=1>Air discharge</td><td rowspan=1 colspan=1>1</td><td rowspan=1 colspan=1>2 kV</td></tr><tr><td rowspan=1 colspan=1>2</td><td rowspan=1 colspan=1>4 kV</td></tr><tr><td rowspan=1 colspan=1>3</td><td rowspan=1 colspan=1>8 kV</td></tr><tr><td rowspan=1 colspan=1>4</td><td rowspan=1 colspan=1>15 kV</td></tr></table>

The air discharge model is generally used when the contact cannot be characterized.

Table 5. ST classification of ESD consequences   

<table><tr><td rowspan=1 colspan=1>Class A</td><td rowspan=1 colspan=1>Class B</td><td rowspan=1 colspan=1>Class C</td><td rowspan=1 colspan=1>Class D</td></tr><tr><td rowspan=1 colspan=1>No failure detected</td><td rowspan=1 colspan=1>Failure detected but self-recovery after disturbance</td><td rowspan=1 colspan=1>Need an external user actionto recover normal functionality</td><td rowspan=1 colspan=1>Normal functionality cannotbe recovered</td></tr></table>

ES nso Teree uin make havehterestshosurh d  eey protect them.

# 2.4

# Choosing an optimum ESD protection method

MCU and MPU s expo  D o he exteal wor requ proten.Tenclue puts nd uuts for interfaces such as:

USB, HDMI, USART, Ethernet audio line, microphone, speaker joystick, touch sensor, mouse RF antenna, power plug

This section describes possible ESD protection methods, then focuses on the TVS devices.

# 2.4.1 ESD protection methods

# Using clamping diodes

Clamping diodes are most commonly used as IC ESD protection devices. Microcontrollers, digital signal controllers, and processors usually integrate ESD clamping diodes.

ICs without the embedded ESD protection can be protected with external clamping diodes, as shown in the following figure. For a standard GPIO, diodes clamping to VDD and Vss shunt the ESD stress to VDD (positive plarityr ND (negative polarity.  dide clamping oV  5 tolerant /O prevents he from used as such.

Pla a capacir or example  F) between VDD and GND and as close as possible to the diodes, aso the ESD current.

![](images/70e892f9be26a7f8520f77c1cd7516234060db9934e4474735d76e4c34996c9d.jpg)  
Figure 5. Clamping diodes as ESD protection devices

# Using a varistor

Theritanvrsorvarwit heolagcheigheheolaghewerhei. T property makes them behave s clamps when exposed to E.Furthermore, varistors are low-capaci n sviTw poa voltaloi o drawback is that by their construction, these metal-oxide varistors (MOV) degrade when exposed to ESDs.

![](images/32c21ebd84d949231e6082bb77181d485e29bdeaa96184807b437dbbaa03627b.jpg)  
Figure 6. Varistor as ESD protection device

# Using a capacitor

ESD is most commonly caused by humans, upon touching the electronic equipment The IEC 61000-4-2 standard (HBM) categorizes the electronicequipment resistance to a 330 pF capacitor discharge, without damage. The vle   uivalen  bo paaetac ee in capacitor voltage prior to the discharge. It spans up to 8 kV.

Elecrical terminals can be protected with a capacitor (usuall 100 For more) that absorbs the charge thehuman body tansfer  hequipment upon he  It als down hevoltage with the rat tw capacitns. Forhe protection tbctve the protecion capacitor must have  ry ow ps inductance, which is the property of high-frequency capacitors.

Tl  p lh o in e altvolse in parallel with the decoupling capacitor then suppresses peaks due to parasitic inductance.

Themethod isot sitableo protecting dat ports  tdegrade data atrprevents dat intefac r operating.

![](images/86b4773011af5d84ebe95c14fa3f0d32e9f1dcd4d27ce4ea28f56a6ad8d9c04d.jpg)  
Figure 7. Capacitor as ESD protection device

# Using a resistor in series

R  mi  .al  nel o I/O al poerigemials.Standard resistors reot designed tosustainhihvoltagRepetitive exposure tESDs mal pohi hen an  h oivfpe naliyelan  io nvus here op

![](images/10408dced9fe7d0627a838ee28a712a04f8f25080d1a94c26062ca15c382b703.jpg)  
Figure 8. Resistor in series as ESD protection device

# Using a transient voltage suppressor

Transient voltage suppressor TVS) such as Transi is high-impedance until thevoltage across reaches a voltc  hr There are unidirectional (see Figure 10) and bidirectional (see Figure 11) TVS devices.

AirectionalThas ymetrialvoltage-current haractrispresentinghesamreakdownvol the negative and positive ideofthe voltage axis. It is well suited or protecting analog unbiased nes.

Anidiectional TVShas asymmerical voltage-current characteris similar o aZener diodes tclamps bear positive voltages.

![](images/d5fcc9ee7e0d6bbc4252ed31405257b7f4f6b39b9c3c73fd477f7998eda39954.jpg)  
Figure 9. TVS as ESD protection device

# 2.4.2

# ESD protection with TVS

The rest of the document focuses on the ESD protection with TVS and in particular with ST TVS devices.

TVS devisoffr ery st sponse me  harvoltage-current haraeriscandrobustnes i ESDs. Ainalhtrctuochallow urallo he short circuit. This is generally better than an open circuit leaving the equipment unprotected.

nl    IC) io suc as 3.3 V. Bidirectional TVS devices typically protect electronic equipment supplied from positive and negative voltages, such as 3.3 V and -3.3 V.

![](images/bc0f0f7cf39aa0c4a4867ccd3c09b5367b0f9400d7e6e9fcd60b5f3d7331d9d8.jpg)  
Figure 10. Unidirectional TVS voltage-current characteristic

![](images/5f8af2b2e86d8da2f414a00cabe26425fe9bfccf9deb4f95f18ccdd46a2b3210.jpg)  
Figure 11. Bidirectional TVS voltage-current characteristic

# 2.5

# Optimizing the application for ESD protection

Teduc electrial fel can istur othr part  e sstem  coupling henea.Kee TVS device as close as possible to the expected point of electrostatic discharge.

The voltage of the TVS-protected point during an ESD is a sum of:

VBR - the TVS device breakdown voltage VR - voltage across a parasitic serial resistance Rd: VR = Rd X IESD. VL - voltage across a parasitic inductance L: VL = L x di/dt.

T unloading the ESD protection embedded in the STM32.

As every single track has an inherent inductance, the system can be schematized as follows:

![](images/d1e7f13b135c530d1abdeb934fc24b15738a0101bdd3aa2fe57d55166f527619.jpg)  
Figure 12. Schematic diagram of a TVS protected system

T n f he TVS pa  L1 + L2 + L3 whi heewar he po IC isL1 + L4.For ESD con eeal n L1.

Te olg gurehows e pricia  yasurs ach hat gal With tmizay TVSevic patnhe CBsalngacks In hs wayiz L2 nd L3 p inan.Aso, s closer  theESD soure than  he IC to prote, thusmaxiizn he L4/La.

![](images/3a04010d180872bfa680d9dc45ed590b85a26d082cfe6717c0d52950ef1f65ce.jpg)  
Figure 13. Optimizing PCB layout

# 3 ESD solutions in application

This section pertains to ESD protection solutions in various applications such as human interface, wired communication, or multimedia.

![](images/bfab251c4b4084dc21bc74a3883fe937d6bf8f03e39585126ecb14a9b71f6f2e.jpg)  
Figure 14. Protection and filters around an MCU

# 3.1

# Human interface

os E aecaused b humans.Te lwing sections pertain   protectin solutins or jystic, p button, and touch sensing.

# Note:

The STM32 peripherals involved are: ADC and GPIOs.

# 3.1.1

# Joystick

oelu Wh pl its maxmuoperatng voltage3.6 V, the asoluemaxumvoltae  he joysic sensng /ss we ove the VBR  he protection component ee 6.V). This headroo allows he   a protectin mponent w parasitic capacitance.

![](images/2bcca497bded43d8516383a113d165ca9c97db160e27a65b7352c58df21f6f0d.jpg)  
Figure 15. Joystick port ESD protection

Refer to Transil TVS) array for ESD protection (ESDA6V1-5SC6) page on www.st.com for more information on this ESD protection device.

# 3.1.2

# Press button

For signal always at VDD, use a low leakage protection component. This protection component respects the maximum voltage and frequency for a press button application, leaving a good margin on VBR.

![](images/ea2b7cc6a4dc45882ffc164210216e39f6825e079adb2ada57ac300614aed5c1.jpg)  
Figure 16. Press button port ESD protection (two buttons)

Refer to DUAL TRANSIL ARRAY FOR ESD PROTECTION (ESDAL) (for two-button application) and Single-line ocapacitaneransil or D protecion DALC61-1U orne-button application) page nwwwt.com for more information on these ESD protection devices.

# 3.1.3

# Touch sensing

For touch sensing application, refer o [2].

# Analog and power

The following sections pertain to ESD protection solutions for analog signal monitoring, audio playback, and recording and power.

# Analog signal monitoring

Analg igals and es such as he batyvoltage can bemonrd by nAC.Te batteymoitrge, often comig from a mezzanine board, is sensitive o ESD and the input f he STM32 ADC must be protected.

![](images/eaaa801ec1b6ea83558ebe704996468257d565f7fdb525ff9d508ee421109404.jpg)  
Figure 17. Analog signal monitoring port ESD protection

Refer to Single-line low capacitance Transil for bidirectional ESD protection (ESDALC6V1-1BU2) page on www.st.com for more information on this ESD protection device.

The STM32 peripherals involved are: ADC, OPAMP, COMP, and DAC.

# 3.2.2

# Audio playback and recording

Consumer aplications often provide an audio receptacle to plug aheaphone or an external amplifier and a microphone or another audio source The 32 device can e connected o an audio codec device that drives the audio sinal externally.At the same tme the application can monitor theacousti evironment roh analog or MEMS microphones to detect or cancel noise. As these signal lines face the environment through connectors, speakers, or microphones, they must be ESD-protected.

![](images/9b23161f27ed76330b644dfde053c5821e03dab78ef75beb9e0754120f5de277.jpg)  
Figure 18. ESD protection of audio application with jack connectors

![](images/c59e105cd67c6f8a82b6774dc978a2d7b535e9af079fa9cf552549dc53b31e67.jpg)  
Figure 19. ESD protection of audio amplifier application with speakers

Refer to QUAD BIDIRECTIONAL TRANSIL SUPPRESSOR FOR ESD PROTECTION (ESDA6V1-4BC6) page on www.st.com for information on the appropriate protection device for this application.

![](images/afc4454163a3acc26d2ee42bc029d3c54dfbc5250a7405e41b594285cb98b6e0.jpg)  
Figure 20. ESD protection of audio application with ECM

Refer to Single-line low capacitance Transil for ESD protection (ESDALC6V1-1U2) page on www.st.com for information on the appropriate protection device for this application.

![](images/4ab2de6e1265b9068bb08f40a7ddde21a69e718fb8175d6079b68391cf77ffcd.jpg)  
Figure 21. ESD protection of audio application with digital microphone

Refer to QUAD TRANSIL ARRAY FOR ESD PROTECTION (ESDALC6V1W) page on www.st.com for more information on this ESD protection device.

# Note:

The STM32 peripherals involved are: ADC, OPAMP, COMP, DAC, DFSDM, SPDIF, SAI, and I2S.

# 3.2.3

# Power

The SMC30J Transil seris protects sensitive equipment against surges below 3000 W (10/1000 µs) and against ESD according to IEC 61000-4-2, and MIL STD 883, method 3015. It is compatible with high-end equipment and switch mode power supply (SMPS). These applications require an ESD protection component with low leakage cure ha eliblnd ln-astiihjucpeatu3 package packag wi SMC footprint compliant with the IPC 7531 standard.

![](images/d331eac93e69b6739635274e464175381bbfdbc500fec7271b6d79bb51087060.jpg)  
Figure 22. Power supply line ESD protection

Refer to High-power transient voltage supressor (TVS) (ESDA7P120-1U1M) page on www.st.com for more information on this ESD protection device.

The STM32 peripherals involved are: BOR, PVD, and PVM.

# 3.3

# Wired communication

Thefollowig sectins pertain ED protection solutions orCAN, Ethern, ril interfac protocols, RS-32 and RS-485.

# 3.3.1 CAN

![](images/894bef632abdab9bfa92520c9ba3bd79b680d4318e361d0e28481ad84e1f765e.jpg)  
Figure 23. CAN port ESD protection

Refer to Automotive dual-line TVS in SOT323-3L for CAN bus (12 V system) (ESDCAN03-2BWY) page on www.st.com for more information on this ESD protection device.

# Note:

The STM32 peripherals involved are: CAN and FDCAN.

# 3.3.2

# Ethernet

![](images/0cd6429c73822c8e91131e912fe0e36de231e7a281565cc0d52b40d5f432f374.jpg)  
Figure 24. Ethernet port ESD protection

Refer to Very low capacitance ESD protection (USBLC6-4SC6) and 4-line ESD protection for high-speed lines (HS53-4M5) pages on www.st.com or more information on thes ESD protection devices.Consider the latter for gigabit Ethernet ports.

Note:

The STM32 peripheral involved is the Ethernet MAC.

# 3.3.3

# RS-232 and RS-485

The l port an eED-protec rogh he s  trniver wi beded ESD prtectin, w an extra ESD-protecting device.

![](images/e589a94f113f7401f33ccf0e78915525440588191d12228c4695536f3a751ff8.jpg)  
Figure 25. RS-232 transceiver with embedded ESD protection

Refer to 15kV ESD protected 3 to 5.5V, 400kps, RS-232 transceiver with auto power-down (ST3241EB) page on www.st.com for details.

![](images/fdecd3092579e55aadec8c150c3785467d022e70f9e6e6ac06d6e43c8484e782.jpg)  
Figure 26. STM32 embedded RS-232 transceiver with external ESD protection

Refer to TRANSIL ARRAY FOR ESD PROTECTION (ESDAxxP6) page on www.st.com for more information on this ESD protection device.

# 3.3.4 Other serial interfaces

![](images/2d01f7760875091843751e0762b950782f64b570f2277fe2ece6fbef8b5043b4.jpg)  
Figure 27. I2C-bus port ESD protection

Refer to Very low capacitance ESD protection (USBLC6-4SC6) page on www.st.com for more information on this ESD protection device.

# Note:

Other STM32 peripherals such as FMP I2C, I2C, SPI, QUADSPI, OCTOSPI, UART, USART, and LPUART can be protected based on this example.

# 3.4 Multimedia

The followig sections pertain o ESD protecion solutions or MIPI D-PHY, parallel displa interface, HDMI,USB 2.0 Full or High speed, and USB Type-C.

# 3.4.1 MIPI D-PHY (DSI and CSI)

![](images/782110bfdb4c44fbc6392602058b21873494246cb7bea234a651543f0cefdef1.jpg)  
Figure 28. MIPI port ESD protection

Refer to Common mode filter with ESD protection in QFN-10L (ECMF04-4HSWM10) and Very low capacitance ESD protection (USBLC6-4) pages on www.st.com for more information on these ESD protection devices.

# 3.4.2 Parallel display interface

![](images/a2e57b5edcd2c4b1cb60d9b3987c999c825c819be5af7e315157b74e0219dafc.jpg)  
Figure 29. Parallel display port ESD protection

Refer to 8-ine L-C EMI filter and ESD protectin or isplay intefaces (EMIF08-LCD04M16) page n wwwt.com for more information on this ESD protection device.

# 3.4.3 HDMI

![](images/754abee75cb1bde586344c566428f7bd76149781252f9299859fb8e078d58322.jpg)  
Figure 30. HDMI port ESD protection

Refer to Common mode filter with ESD protection in QFN-10L (ECMF04-4HSWM10) and 5-line low capacitance Transil arrays for ESD protection (ESDALC6V1-5M6) pages on www.st.com for more information on these ESD protection devices.

# Note:

On STM32 devices, the I/Os to protect against ESD are those of the HDMI CEC port.

# 3.4.4

# USB

![](images/393938c0f3660d8c508ca18ce5be8f1969ff3d2674ef102058181b262ad6e8a6.jpg)  
Figure 31. USB 2.0 full-speed port ESD protection

Refer to ESD Protection for USB 2.0 High Speed (USBLC6-2) page on www.st.com for more information on this ESD protection device.

![](images/7bc1b82a7456ea956465edffd3cabd0ce24c674fdb9749620b4321b8c7b21c7d.jpg)  
Figure 32. USB 2.0 full-speed OTG port ESD protection

Rer toVery low capacitance ESD protection (USBLC6-4) page on wst.com for more information on ths ESD protection device.

![](images/e567b449e5d0c18290c7b953a69bd7aea9dc385024efe35abe79c4a711c9eb8e.jpg)  
Figure 33. USB 2.0 high-speed port ESD protection

Refer to Common-mode filter and ESD protection for USB 2.0 and MIPI/MDDI interfaces (ECMF02-2AMX6) page on www.st.com for more information on this ESD protection device.

![](images/39ffd5b8fb6be9c3359c34b20a8225fee8f28053e7b375265016158c6ad7eaeb.jpg)  
Figure 34. USB Type-C® port ESD protection

Refer to USB Type-C Port Protection for Sink application (TCPP01-M12) page on www.st.com for more information on this ESD protection device.

# Note:

On STM32 devices, the I/Os subject to be ESD-protected are those of the USB, USB OTG_FS, USB OTG_HS, and UCPD ports.

# 3.5

# Storage

The following sections pertain to ESD protecting SD card and smartcard.

# 3.5.1 SD card 2.0

![](images/a47f17b6a6388422b21b218f7bf05f529caaf1221cca8f7c69f355a89fb8a47c.jpg)  
Figure 35. SD card 2.0 port ESD protection

Refer to 6-line EMI filter and ESD protection for T-Flash and micro SD card™interfaces (EMIF06-MSD02N16 page on www.st.com for more information on this EsD protection device.

# Note:

On STM32 devices, the I/Os to protect against ESD are those of the SDMMC peripheral.

# 3.5.2

# SD card 3.0

![](images/96b80dfc6ec4bc02c25eccbea912352fe4c8d64299e00245d70c28335d858f2c.jpg)  
Figure 36. SD card 3.0 port ESD protection

Refe toVery low capacitanc ESD protection (USBLC6-4) page on w.st.com formore information on ths ESD protection device.

Note:

On STM32 devices, the I/Os to protect against ESD are those of the SDMMC peripheral.

# 3.5.3 Smartcard (ISO-7816)

![](images/35dfe4bce37a6d880d1539d11a52ceeed1140ded73f3f8ff3bcf863fa4ac4d7d.jpg)  
Figure 37. Smartcard interface ESD protection

Refer to 3-line EMI filter and ESD protection for SIM card interfaces (EMIF03-SIM02M8) and Single-line unidirectional ESD protection for high speed interface (ESDAULC6-1U2) pages on www.st.com for more information on these ESD protection devices.

Note:

On STM32 devices, the I/Os to protect against ESD are those of the USART peripheral.

# 3.6

# Debug and programming

This sections pertain to ESD protecting SWD and JTAG interfaces.

# 3.6.1

# SWD

![](images/ca2723eef5a73e3134e005fdb83948d4c6115d1a243a8b9a189ea455f915edce.jpg)  
Figure 38. SWD interface ESD protection

Refer to 600 W, 3.3 V TVS in SMB (SMLVT3V3) and QUAD TRANSIL ARRAY FOR ESD PROTECTION (ESDALC6V1W) pages on www.st.com for more information on this ESD protection device.

# 3.6.2 JTAG

![](images/ddde8c08afd7e9c2e225e6d33a6a78baaf8bee9b718516c71e31afc0d5d44e9e.jpg)  
Figure 39. JTAG interface ESD protection

Refer to 600 W, 3.3 V TVS in SMB (SMLVT3V3) and 5-ine low capacitance Transi™arrays for ESD protection (ESDALC6V1-5M6) pages on www.st.com for more information on this ESD protection device.

# 3.7

# Summary

The following table summarizes the ESD protection components presented in the previous sections.

<table><tr><td colspan="1" rowspan="1">Application</td><td colspan="1" rowspan="1">ESD protection device</td></tr><tr><td colspan="2" rowspan="1">Human interface</td></tr><tr><td colspan="1" rowspan="1">Joystick or Keypad</td><td colspan="1" rowspan="1">ESDA6V1-5SC6</td></tr><tr><td colspan="1" rowspan="1">Press button (one button)</td><td colspan="1" rowspan="1">ESDALC6V1-1U2</td></tr><tr><td colspan="1" rowspan="1">Press button (two buttons)</td><td colspan="1" rowspan="1">ESDAL</td></tr><tr><td colspan="2" rowspan="1">Analog and power</td></tr><tr><td colspan="1" rowspan="1">Analog signal monitoring (positive-only)</td><td colspan="1" rowspan="1">ESDALC6V1-1U2</td></tr><tr><td colspan="1" rowspan="1">Analog signal monitoring (bi-directional)</td><td colspan="1" rowspan="1">ESDALC6V1-1BU2</td></tr><tr><td colspan="1" rowspan="1">Audio application with two jack connectors or speakers</td><td colspan="1" rowspan="1">ESDA6V1-4BC6</td></tr><tr><td colspan="1" rowspan="1">Audio application with ECM</td><td colspan="1" rowspan="1">ESDALC6V1-1U2</td></tr><tr><td colspan="1" rowspan="1">Audio application with digital microphone</td><td colspan="1" rowspan="1">ESDALC6V1W5</td></tr><tr><td colspan="1" rowspan="1">Power line</td><td colspan="1" rowspan="1">ESDA7P120-1U1M</td></tr><tr><td colspan="2" rowspan="1">Wired communication</td></tr><tr><td colspan="1" rowspan="1">CAN port</td><td colspan="1" rowspan="1">ESDCANxx-2BWY</td></tr><tr><td colspan="1" rowspan="1">Ethernet port</td><td colspan="1" rowspan="1">USBLC6-4HSP053-4M5</td></tr><tr><td colspan="1" rowspan="1">RS-232 / RS-485 port</td><td colspan="1" rowspan="1">ESDAxxxP6</td></tr><tr><td colspan="1" rowspan="1">Other serial interfaces</td><td colspan="1" rowspan="1">USBLC6-4</td></tr><tr><td colspan="2" rowspan="1">Multimedia</td></tr><tr><td colspan="1" rowspan="1">MIPI D-PHY (DSI / CSI)</td><td colspan="1" rowspan="1">ECMF04-4HSWM10USBLC6-4</td></tr><tr><td colspan="1" rowspan="1">Parallel display interface</td><td colspan="1" rowspan="1">EMIF08-LCD04M16</td></tr><tr><td colspan="1" rowspan="1">HDMI</td><td colspan="1" rowspan="1">ECMF04-4HSWM10 (data lines, with common mode choke)HSP053-4M5 (data lines, protection only)ESDALC6V1-5M6 (CEC lines)</td></tr><tr><td colspan="1" rowspan="1">USB 2.0 FS</td><td colspan="1" rowspan="1">USBLC6-2</td></tr><tr><td colspan="1" rowspan="1">USB 2.0 FS OTG</td><td colspan="1" rowspan="1">USBLC6-4</td></tr><tr><td colspan="1" rowspan="1">USB 2.0 HS</td><td colspan="1" rowspan="1">ECMF02-2AMX6</td></tr><tr><td colspan="1" rowspan="1"></td><td colspan="1" rowspan="1">Storage</td></tr><tr><td colspan="1" rowspan="1">SD card 2.0</td><td colspan="1" rowspan="1">EMIF06-MSD02N16</td></tr><tr><td colspan="1" rowspan="1">SD card 3.0</td><td colspan="1" rowspan="1">USBLC6-4</td></tr><tr><td colspan="1" rowspan="1">Smartcard (ISO-7816)</td><td colspan="1" rowspan="1">EMIF03-SIM02M8 (with filter)ESDALC6V1W5 (without filter)ESDAULC6-1U2</td></tr><tr><td colspan="1" rowspan="1"></td><td colspan="1" rowspan="1">Debug interfaces</td></tr><tr><td colspan="1" rowspan="1">SWD</td><td colspan="1" rowspan="1">SMLVT3V3ESDALC6V1W5</td></tr><tr><td colspan="1" rowspan="1">JTAG</td><td colspan="1" rowspan="1">SMLVT3V3ESDALC6V1-5M6</td></tr><tr><td colspan="1" rowspan="1"></td><td colspan="1" rowspan="1">RF interfaces</td></tr><tr><td colspan="1" rowspan="1">NFC tag</td><td colspan="1" rowspan="1">DSILC6-4xx</td></tr><tr><td colspan="1" rowspan="1">NFC reader</td><td colspan="1" rowspan="1">ESDAXLC18-1BF4</td></tr><tr><td colspan="1" rowspan="1">Bluetooth, Sub-GHz (SigFox, LoRa, 169-433 MHz)</td><td colspan="1" rowspan="1">ESDARF02-1BU2CK</td></tr></table>

Note:

The list is not exhaustive. For more information on ST ESD protection components, refer to and/or contact your local ST sales office.

# 4 Conclusion

Tht prlel w he ahe dh0nr selection of adequate ESD protection components to protect effectively the STM32 device.

Man parameters come into account or protecting a system against ED, such as PCB housing, board shielding and coating, and PCB routing and technology. However, TVS is the most effective and easy-to-implement protection device for the majority of applications.

# Revision history

Table 6. Document revision history   

<table><tr><td>Date</td><td>Version</td><td>Changes</td></tr><tr><td>02-Jun-2022</td><td>1</td><td>Initial release.</td></tr></table>

# Contents

#

# 1 General information

# 2 Electrostatic discharge (ESD) 4

2.1 ESD phenomenon. 4   
2.2 ESD protection level quantification 6   
2.3 ESD protection requirements in application. 6

# 2.4 Choosing an optimum ESD protection method

2.4.1 ESD protection methods   
2.4.2 ESD protection with TVS. 10

2.5 Optimizing the application for ESD protection . 11

# ESD solutions in application 12

# 3.1 Human interface 12

3.1.1 Joystick. 12   
3.1.2 Press button . 13   
3.1.3 Touch sensing. 13

# 3.2 Analog and power 13

3.2.1 Analog signal monitoring. 13   
3.2.2 Audio playback and recording. 14   
3.2.3 Power 16

# 3.3 Wired communication . 16

3.3.1 CAN 17   
3.3.2 Ethernet 17   
3.3.3 RS-232 and RS-485 18   
3.3.4 Other serial interfaces. 19

# i.4 Multimedia 19

3.4.1 MIPI D-PHY (DSI and CSI) . 20   
3.4.2 Parallel display interface . 21   
3.4.3 HDMI 21   
3.4.4 USB 22

# 3.5 Storage. 23

3.5.1 SD card 2.0. 24   
3.5.2 SD card 3.0. 24   
3.5.3 Smartcard (ISO-7816). . 25

# 3.6 Debug and programming 25

3.6.1 SWD 25   
3.6.2 JTAG. 26   
3.7 Summary .26   
4 Conclusion. .28   
Revision history .29   
List of tables .32   
List of figures. .33

# List of tables

Table 1. Glossary of terms. 2 Table 2. Reference documents 2 Table 3. Complementary literature available on www.st.com 2 Table 4. Sensitivity classification for the HBM (IEC 61000-4-2).   
Table 5. ST classification of ESD consequences   
Table 6. Document revision history . 29

# List of figures

Figure 1. Example of metallization defect. 4   
Figure 2. Example of oxide breakdown defect 5   
Figure 3. Example of burn defect 5   
Figure 4. Application variants with protected and unprotected STM32 device 6   
Figure 5. Clamping diodes as ESD protection devices. 8   
Figure 6. Varistor as ESD protection device. 8   
Figure 7. Capacitor as ESD protection device 9   
Figure 8. Resistor in series as ESD protection device 9   
Figure 9. TVS as ESD protection device 9   
Figure 10. Unidirectional TVS voltage-current characteristic. 10   
Figure 11. Bidirectional TVS voltage-current characteristic. 10   
Figure 12. Schematic diagram of a TVS protected system. 11   
Figure 13. Optimizing PCB layout. . 11   
Figure 14. Protection and filters around an MCU 12   
Figure 15. Joystick port ESD protection. 12   
Figure 16. Press button port ESD protection (two buttons). 13   
Figure 17. Analog signal monitoring port ESD protection . 14   
Figure 18. ESD protection of audio application with jack connectors 14   
Figure 19. ESD protection of audio amplifier application with speakers 15   
Figure 20. ESD protection of audio application with ECM 15   
Figure 21. ESD protection of audio application with digital microphone 16   
Figure 22. Power supply line ESD protection. 16   
Figure 23. CAN port ESD protection. 17   
Figure 24. Ethernet port ESD protection 17   
Figure 25. RS-232 transceiver with embedded ESD protection. 18   
Figure 26. STM32 embedded RS-232 transceiver with external ESD protection 18   
Figure 27. 12C-bus port ESD protection . 19   
Figure 28. MIPI port ESD protection 20   
Figure 29. Parallel display port ESD protection. . 21   
Figure 30. HDMI port ESD protection 21   
Figure 31. USB 2.0 full-speed port ESD protection. 22   
Figure 32. USB 2.0 full-speed OTG port ESD protection 22   
Figure 33. USB 2.0 high-speed port ESD protection 23   
Figure 34. USB Type-C® port ESD protection 23   
Figure 35. SD card 2.0 port ESD protection. 24   
Figure 36. SD card 3.0 port ESD protection . 24   
Figure 37. Smartcard interface ESD protection. 25   
Figure 38. SWD interface ESD protection 25   
Figure 39. JTAG interface ESD protection 26

# IMPORTANT NOTICE  READ CAREFULLY

pt old ursant  dits   leole.

purchasers' products.

No license, express or implied, to any intellectual property right is granted by ST herein.

re the property of their respective owners.