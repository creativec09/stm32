# Receiving S/PDIF audio stream with the STM32F4/F7/H7 Series

# Introduction

several ways, by electrical or optical means.

The /PDIFRX perheralbeed TM32 devic designed  eceive  /PDI flo opliant wit IEC-58 I by Dolby or DTS.

that used in STM32 devices.

# 1

# S/PDIF Interface

This document applies to Arm®-based devices.

# Note:

Arm is a registered trademark of Arm Limited (or its subsidiaries) in the US and/or elsewhere.

# 1.1

# S/PDIF backgroun

S/PDIis an audinterfacortranissiondigial audoatover easnablyhort dstans bewe ule uc hetgeilal c interface.

S/PDIF is based on the AES3 interconnect standard. S/PDIF and AES3 are compatible at the protocol level but tll hsalavan channels of uncompressed PCM audio, or compressed 5.1/7.1 surround sound (such as DTS audio codec data). Howevuemindwh,deso orcresudorma otherha-hanel LCM) such as Dolby True HD and DTS master.

S/PDden'peciy any default dat tranmission ratThe device as o extract heclock fromhpu lThsachieved yshasemark code that includes ertwotransitins  each t e tissin ates ypially usedae 4. Hz r ero audo, an 48 Hz o iitalaudo tape AT.Te standards also support simple stereo streams up to a high sample rate (192 kHz).

The format has been standardized in the consumer domain in the form of IEC60958-3 (International Electrotechnical Commission, IEC), and in the professional domain as AES3 and IEC60958-4.

The main purpose of the S/PDF ormat is theability to transfer data between two pieces of digital audio et wiot oro aiwhi wouplysqualysqu alifeyicati otol hicanissiogialattnit receiver, can be implemented using:

electrical transmission, using a coaxial cable and cinch connectors optical transmission, using optical fiber cable and TOSLINK or mini-TOSLINK connectors

As shown in Figure . S/PDIF usage examples, most wellknown consumer equipment is able to exploit S/PDIF transmission:

CD, DVD or BLURAY players   
PC sound cards   
TV sets

In STM32 devics, he S/PDIF can also be used to cone different devices. In such cases there is no ne for electrical adapters.

![](images/140490430b7c104b03f67f69d4ea23604f4fd56ea4d73dfca8ec6ae49c044dfa.jpg)  
Figure 1. S/PDIF usage examples

# S/PDIF format

/P the various components of the bitstream.

T the clock signal from the data signal itself.

![](images/083fabe0d699450954332edeb73269ea84e29cb75a83d72b746fd5bf392ab640.jpg)  
Figure 2. Bi-phase encoding in an S/PDIF stream

E S/PD block is ade u 9 ams. he /PD rm cnsist  o sub-ames.e ub-am concatenation of:

preamble - a synchronization pattern used to identify the start of a 192-frame block or sub-fram   
4-bit auxiliary data (AUX)   
20-bit audio data (24-bit when combined with AUX)   
validity bit - indicates if the data is valid   
user bit - over 192 frames, this forms a user data block   
channel bit - over 192-frames, this forms a channel status block   
parity bit - used to maintain even parity over the sub-frame (except the preamble)

![](images/f2f34b7fecad074b54a74f9ff85cd95922109e86cbc0df487665135ec1771443.jpg)  
Figure 3. S/PDIF block

# 1.2.1

# Synchronization preambles

Tb B", " nd " whi he ps  heye ll ", ""  " ee B s sub-frame of each frame the "W" preamble is used.

![](images/4ad3390b7fdb1b8a0fca03ea69f619c512dd7fd5dfad5959f8151c9c0fd46341.jpg)  
Figure 4. S/PDIF block format

1. Forhistorical reasons preambles "B", "M" and "W" are, for use in professional applecations, referred to as Z", "X" and "Y" respectively.

![](images/a1189015b7349006544fc9c036d4470ce85077a24c4366823db9a57a14091360.jpg)  
Figure 5. Preambles

# 1.2.2

# Audio data

Theaudo samples axium lngt  bi/ampl.  teul zheudodatot us e equal to 0. For example, a CD player uses only 16 bits.

# 2.3 Channel status blocl

T hanel status bit acrosshe block togethercompose oration relate theaudiochanneThe ae status is identical for both subframes (except for the channel number). .

![](images/68cbcfad26b8d10970fd17e462c8fe7bbaca675d849e0de321309f8c704a0204.jpg)  
Figure 6. Channel status block composition

1.For both subframes within one frame the channel status information is identical

Tmsoran  hiroanu heheaicat ablcnaboui data format, sampling frequency, number of channels, copyright information and so on.

# 1.2.4

# User data block

Teuerdatblock i p inhesam way s heha stats block n cary y i maxiu z s. It an contxila dat o d use suc  g nae . As the content is not defined in the S/PDIF standard, it might be ignored by some devices.

# 1.2.5

# Hardware specification

Two types of transmission lines are defined by the S/PDIF standard: 75 Ω coaxial or optical fiber lines.

Table 1. S/PDIF characteristics   

<table><tr><td rowspan=1 colspan=1></td><td rowspan=1 colspan=1>S/PDIF coaxial</td><td rowspan=1 colspan=1>S/PDIF optical</td></tr><tr><td rowspan=1 colspan=1>Interconnecting cables</td><td rowspan=1 colspan=2>75 Ω ± 5% ( &lt; 10 m) or 75 Ω ± 35% (I &gt; 10 m)</td></tr><tr><td rowspan=1 colspan=1>Line driver Vout</td><td rowspan=1 colspan=2>0.4 Vpp . . 0.6 Vpp, &lt; 0.05 VDC</td></tr><tr><td rowspan=1 colspan=1>Line receiver Vin</td><td rowspan=1 colspan=2>0.2 Vpp .. 0.6 Vpp</td></tr><tr><td rowspan=1 colspan=1>Rise and fall times</td><td rowspan=1 colspan=2>&lt; 0,4 UI (unit interval)</td></tr><tr><td rowspan=1 colspan=1>Connector</td><td rowspan=1 colspan=1>RCA</td><td rowspan=1 colspan=1>TosLink/mini TosLink</td></tr><tr><td rowspan=1 colspan=1>Max. distance</td><td rowspan=1 colspan=1>15 m</td><td rowspan=1 colspan=1>10 m</td></tr></table>

# 1.3

# SPDIFRX overview

The SPDIFRX peripheral embedded in the STM32 (STM32F4, STM32F7 and STM32H7 Series, see the applicabe device datasheet) is designed to receive an S/PDIF flow compliant with the IEC-60958 and IEC-61937 specifications. This receiver provides ll the necessary features to detect the symbol rate, and decode the ining dat stream received fom one f the PDRX inputs. In addition thePDIRX separates hedata stream from the channel status (C) and the user (U) information.

The received data stream can be stored in the MCU memory using either a dedicated DMA interface AR .  aheh a ) )ao can be stored in the MCU memory either by using a dedicated DMA interface (DMASPDIFRX_CS) or interrupt services.

In most cases, once processed, this data is sent to ne or several audio codecs using, or example, an SAl peripheral. The codec adapts the signal in order to provide a sound through loudspeakers or a headset.

![](images/07496b18efccaf834444fc3b143175dc4a71833da17dfe0dc5ec73cd8fb201c5.jpg)  
Figure 7. Block diagram

The SPDIFRX peripheral also provides two kinds of signals: the symbol clock (spdifrx_ck_symb) and the sampling clock (spdifrx_frame_sync) extracted from the incoming stream. These signals can be used to synchronize the received stream with other devices. It is important to note that these signals might have appreciable jitter due to the resampling of the incoming stream with the S/PDIF internal clock.

# 1.3.1

# SPDIFRX synchronization and decoding

The received signal on the selected SPDIFRX_IN[x] input, is first re-sampled using the SPDIF_CLK clock (s cock).Thenfitering isaplie ordertcanel spursan  geetecordetects heve transitions.

The resulting sinal goes  the decoder block, which perorms the syncronization and the biphase decding

Oable, he DRX tri  ynoniz  e ele pu ream. I  DFRX is ot ply oniol roaoizatib measurements of the time intervals between consecutive edges.

The synchronization is performed in two steps:

• The COARSE synchronization phase:

In this phase the preambles are used to estimate the symbol length and find the preamble boundary. This zatiaivealvle measured in this phase is short and it is not averaged. As shown in the figure below, the COARSE synchronization searches for the shortest and longest time interval between two transitions. This COARSE synchronization i normally performe once, ut several attempts can e programmed i the signal isnoisy.

• The FINE synchronization phase:

Int haeol lntawi neewioak nzatn to signal quality. This synchronization is performed on every frame, in order to remain locked. The synchronization process is shown in the Figure 8. Sequencer.

![](images/0d4fa49264a804b61041a8f4ac306a36e725475e7a1bda98aa3b2c9cd8338a37.jpg)  
Figure 8. Sequencer

1. The decoding is considered correct when the symbols are properly decoded, and the preamble occurs at the expected position.

Onc the SPDIFRX is synchronized, the data is decoded by measuring the time-interval between consecutive transitions.

Please refer to the SPDIFRX specification for additional details.

# 2 Interfacing a S/PDIF coaxial to SPDIFRX

A shown nTablDI charactristics, the received SPD signal needs to be adapted to levels acc y roleut pelc dapeecelplit adjust the DC value to match the VIL and VIH PAD characteristics.

# Challenges for S/PDIF signal conversion

Teialapusvoirular u akev duty cycle degradation.

Noteha s hembo decodin   S/PDteamis asenhemeasemen  e mnterval bwe tal SPDIFRX is not sensitive to the signal polarity, and only transitions are taken into account.

# 2.2 Electrical signal adapter

S/PDIF devices provide signals between 0.2Vpp and 0.6 Vpp into a 75 Ω load over an unbalanced circuit. The elecrical adaptermustamplify he receivd /PDsignal t a logicevelaccepted by icocontrollers. Thi signal conversion is the purpose of the electrical interface which must be developed.

The minimum gain required for the signal conversion mainly depends on the STM32 application power supply (VDD) assuming that the incoming S/PDIF signal could be 0.2 Vpp worst case.

The required amplification gain in dB is:

![](images/679d3da65d342432703969610347597e2f2efa54c5ea18c37822640fc2f51c79.jpg)

with Vi = 0.2 V

Taplifition liatin poweplyhows epliation ai eui (noticeable) MCU supply voltages (VDD).

Table 2. Amplification gain versus application power supply   

<table><tr><td rowspan=1 colspan=1>VDD</td><td rowspan=1 colspan=1>Amplification gain required</td></tr><tr><td rowspan=1 colspan=1>1.7V</td><td rowspan=1 colspan=1>x8.5 (18.5 dB)</td></tr><tr><td rowspan=1 colspan=1>2.5V</td><td rowspan=1 colspan=1>x12.5 (22 dB)</td></tr><tr><td rowspan=1 colspan=1>3V</td><td rowspan=1 colspan=1>x15 (23.5 dB)</td></tr><tr><td rowspan=1 colspan=1>3.3 V</td><td rowspan=1 colspan=1>x16.5 (24.5 dB)</td></tr><tr><td rowspan=1 colspan=1>3.6 V</td><td rowspan=1 colspan=1>x18 (25 dB)</td></tr></table>

This bandwidth is critical for S/PDIF applications where the S/PDIF sample rate can reach 192 kHz, which corresponds to a symbol rate of 12.288 MHz.

# 2.2.1

# Using simple inverters

Ui is considered as an analog signal.

Thieehoivayufuf

Figure 9. Output responses shows the output response of LVC1GU04 (unbuffered) and LVC1G04 (buffered) vrs  ramignal, ien loomo.Terstn egions uinearrheG, v e orhe LVCG0.Forhe LVCG0 sonstabili he ansi gin can be en, ue h sow sok

![](images/5563a422adc9402c2454663d072466ac4b11420f711abcf7e91b17b8e4a23d27.jpg)  
Figure 9. Output responses

Fourplan o buffuffy anhowufinverr sensitiveo external component values. Hence the propos mplementation  baseon unbuffereinverters.

u beoitted if the amplitude provided by the first stage is sufficient. This depends on the targeted S/PDIF frequencies, the capability of the inverter used and the VDD voltage used for the STM32.

Fepl r   eu  Hz haol = Hz, . MHz), a dual stage is safer.

# Proposed implementation

![](images/a963285d7a1c36e5329668787c871d9f54be9a5f27b0d68f11ecd070147c2c46.jpg)  
Figure 10. Variant A - implemented in STM32F769I Discovery board

# The components can have the following values:

Table 3. Proposed component values   

<table><tr><td rowspan=1 colspan=1>Component</td><td rowspan=1 colspan=1>Value</td><td rowspan=1 colspan=1>Unit</td></tr><tr><td rowspan=1 colspan=1>IC1, IC2</td><td rowspan=1 colspan=1>SN74LVC1GU04</td><td rowspan=1 colspan=1></td></tr><tr><td rowspan=1 colspan=1>R1</td><td rowspan=1 colspan=1>75</td><td rowspan=1 colspan=1>Q</td></tr><tr><td rowspan=1 colspan=1>R2, R4</td><td rowspan=1 colspan=1>220</td><td rowspan=1 colspan=1>Ω</td></tr><tr><td rowspan=1 colspan=1>R3, R5</td><td rowspan=1 colspan=1>100</td><td rowspan=1 colspan=1>kΩ</td></tr><tr><td rowspan=1 colspan=1>C1, C2</td><td rowspan=1 colspan=1>4.7</td><td rowspan=1 colspan=1>$nr$</td></tr><tr><td rowspan=1 colspan=1>C3</td><td rowspan=1 colspan=1>100</td><td rowspan=1 colspan=1>nF</td></tr></table>

Resistor R1 terminates the S/PDIF cable providing the signal.

Cir 1 )blocksheDCaluheiream. Ialusotcital, o  ale 0 too big, the DC setting time at the IC1 input increases.

t to 0Volnd hevut geshih veollg etmeheplThe charges capacitor C1 through R1, R2 and R3. In our example, R1 and R2 can be neglected compared to the c to amplify the AC component of the input signal.

The time constant managing the DC offset settling time can be approximated by the following equation:

![](images/239165611e25673e76c028aae5d4c334921de855e37ac8f71510d86995ccb9c3.jpg)

Wh el valhiattu lh inverter input is approaching the transition level.

![](images/edd465884cb0e59d32037143058eb0ab2e75d4850f353370adbe9f8f281fcc7e.jpg)  
Figure 11. DC setting time

Rr )an Rlsoumi he gi e vree loop gi o) on the SN74LVC1GU04 sample used for this document is quite good at about 36 (that is, 31 dB).

The formula below gives the inverter gain:

![](images/2fcede46398d9819956d2f62dc2a50ea08b656810e7dd21ac3e03e6659ea17ca.jpg)

The current gain is limited to 33 (that is 30.4 dB). The measured value is 32.8.

Itn ell appear at the output under certain conditions.

tle heutut iment epuvoltaentileuut gatgs ah ve.

Controlling the gain avoids spurious oscillations when no signal is connected.

I   po i  LC=M is obtained with an LVC1GU04 and R3 = 100 kΩ.

The strong gain of the LVC1G04 brings about instability on the inverter output.

![](images/76e40da235a3becfa00ccfc5279364f54d3707254893b22a99127a839b3fc707.jpg)  
Figure 12. Inverter output   
Figure. Single inverter stage at  MHz and Figure. Single inverter stage at 6 MHz show the resulting output signal of a single inverter stage at 13 MHz and 6 MHz.

![](images/a80058132a91aed3bb4e3f5eac0c23beb780cb8f4ce60384024c34bd4137d7cd.jpg)  
Figure 13. Single inverter stage at 13 MHz

1The yellow waveform is the input signal and the green waveform is th output signal.

![](images/d6fe880ee850471b9aa959ac8f630994ce4c24cd6f023469b3c3bb7c71e932b3.jpg)  
Figure 14. Single inverter stage at 6 MHz

1.The yellow waveform is the input signal and the green waveform is th output signal.

# Power supply sensitivity

Iu p IC1 and IC2.

reasons:

the propagation delay of the inverter is sensitive to ripple in the supply voltage the open loop gain is sensitive to ripple in the supply voltage

A variant of the adapter proposed in Figure0.VariantA  implemented in TM32769 Discovery board keeps t e e weak.

![](images/b7c5e72b7eda3ed303c83c2241b01c733ca2b8871be70f15b25f55a80463e360.jpg)  
Figure 15. Variant B - simplified version

![](images/a18270df9c8ebb16d7b0a489dd40fe44fbf64410113fa6b7561bfe3a7f81e071.jpg)  
Figure Output f he second stage shows the signal obtainedat the second stage output, or an dio bitstream at 192 kHz.   
Figure 16. Output of the second stage

1. The yellow waveform is the output signal.

# 2.2.2

# High-speed differential line transceiver

Ti option uses a high-speeddfferential linedriver and receiver such as an S65LDM1The deviceis a l rates of 400 Mbit/s.

![](images/4d22428ffdea5bd2f284675f79e2eb714c581130c974c55b3a372b989d3bd6b2.jpg)  
Figure 17. Schematic for transceiver receiver mode

Fur Receiveriut  uut waveors hows he sgal aiat he econ stage utut, audio bitstream at 192kHz.

![](images/e425f45becd32882305ffec745cc391ba6a503e47cd855f56331db774097861c.jpg)  
Figure 18. Receiver input and output waveforms

# 2.2.3

# Fast comparator

This option uses a fast comparator such as the LT1713.   
In t plementaton, he DCcomponent  heiut sigal is extractd ymeansR4 and3,and coe to the minus input as the threshold signal.

![](images/91c3ea81cc7ad54efe237a7693c46936a7b375f10f838a7f4a00619b0d529653.jpg)  
Figure 19. Schematic for fast comparator mode

![](images/50f5cfff297e17003b32302385062ee887908d2f8d3fbfec24e03f9bbf7ff797.jpg)  
Figure 20. Comparator input and output waveforms

1. The yellow waveform is the input signal and the green waveform is the output signal. Insehystere plement,  ample, y  postivac loopisoteend  l influence the distance between the signal edges. To achieve suficient output-signal quality, a clean and properly decoupled supply is recommended.

# 2.3

# Optical connection

l l was created by the Toshiba Corporation, which named the system TOSLINK.

Thotical ferinTOSLINK cablescan e pleente indierent matrils.Whilplastioptical fi s between devices is more than approximately7 to10meters, the use  coaxial cable  recommended instead. Also, the fiber core of a TOSLINK cable may be permanently damaged if tightly bent.

Ondvantageptical fer vercaxial cables muny rou loopsandR ntereren. The link, the more jitter is added.

# 2.3.1 Proposed implementation

T eablh/PDX, esuo etl al i signal. Converters are available on the market that can do the required conversion. For example:

Cliff Electronics - FC684205R Toshiba - TORX177L Everlight - PLR135/T

Thee products provide data rates up15 MHz and typical application rise times of 0 ns. All these products require an external supply.

Figure 21. Schematic used for optical connection shows a sample circuit of a TOSLINK device.

![](images/7425fce70e5a45a510ee8492fafe93d64a6a25f2c690606ef92460f7831684f6.jpg)  
Figure 21. Schematic used for optical connection

O  thre convertrabove, nly he LR provides  -Volt utputhe her wodevics provie Volt outputs. When connecting to STM32 devices, care must taken to choose a 5 V tolerant pin.

# 3 Conclusion

Thi documet hows several ways plement aelectrical interace or /PD igals, base on theu inverters, or on the use of more application-specific components such as comparators.

For inverter-based implementations, the choice of an unbuffered version is recommended, as they are less tiveeal ufveno work ohaapol

Wl and attention must be paid to the routing of the signals to the microcontroller.

# 4 List of references

For further details, refer to following documents:

IEC 60958-3: Digital audio interface Part 3: Consumer applications.   
IEC 60958-4: Digital audio interface Part 4: Professional applications.

# Revision history

Table 4. Document revision history   

<table><tr><td rowspan=1 colspan=1>Date</td><td rowspan=1 colspan=1>Revision</td><td rowspan=1 colspan=1>Changes</td></tr><tr><td rowspan=1 colspan=1>05-Jun-2018</td><td rowspan=1 colspan=1>1</td><td rowspan=1 colspan=1>Initial release.</td></tr><tr><td rowspan=1 colspan=1>26-Jun-2018</td><td rowspan=1 colspan=1>2</td><td rowspan=1 colspan=1>Changed confidentiality classification</td></tr></table>

# Contents

# S/PDIF Interface

1.1 S/PDIF background. 2   
1.2 S/PDIF format 3   
1.2.1 Synchronization preambles. 4   
1.2.2 Audio data. 5   
1.2.3 Channel status block. 5   
1.2.4 User data block. . 6   
1.2.5 Hardware specification

1.3 SPDIFRX overview

1.3.1 SPDIFRX synchronization and decoding.

# Interfacing a S/PDIF coaxial to SPDIFRX 10

2.1 Challenges for S/PDIF signal conversion. 10

# 2.2 Electrical signal adapter 10

2.2.1 Using simple inverters. 11   
2.2.2 High-speed differential line transceiver 16   
2.2.3 Fast comparator 18

2.3 Optical connection. 18

2.3.1 Proposed implementation 19

Conclusion 20

4 List of references . .21

Revision history 22

# List of tables

Table 1. S/PDIF characteristics 7   
Table 2. Amplification gain versus application power supply. 10   
Table 3. Proposed component values 12   
Table 4. Document revision history . 22

# List of figures

Figure 1. S/PDIF usage examples 3   
Figure 2. Bi-phase encoding in an S/PDIF stream. 3   
Figure 3. S/PDIF block 4   
Figure 4. S/PDIF block format 4   
Figure 5. Preambles . 5   
Figure 6. Channel status block composition . 6   
Figure 7. Block diagram 7   
Figure 8. Sequencer . 9   
Figure 9. Output responses 11   
Figure 10. Variant A - implemented in STM32F769I Discovery board 12   
Figure 11. DC setting time. 13   
Figure 12. Inverter output 14   
Figure 13. Single inverter stage at 13 MHz 15   
Figure 14. Single inverter stage at 6 MHz 15   
Figure 15. Variant B - simplified version 16   
Figure 16. Output of the second stage 16   
Figure 17. Schematic for transceiver receiver mode 17   
Figure 18. Receiver input and output waveforms 17   
Figure 19. Schematic for fast comparator mode 18   
Figure 20. Comparator input and output waveforms 18   
Figure 21. Schematic used for optical connection. 19

# IMPORTANT NOTICE - PLEASE READ CAREFULLY

ol uant  l.

Purchasers' products.

No license, express or implied, to any intellectual property right is granted by ST herein.

I

© 2018 STMicroelectronics - All rights reserved