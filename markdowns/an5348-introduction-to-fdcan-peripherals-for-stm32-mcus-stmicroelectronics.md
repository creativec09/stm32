# Introduction to FDCAN peripherals for STM32 MCUs

# Introduction

The purpose of this document is detailed hereafter:

Give an overview of the controller area network (CAN) with flexible data-rate (CAN-FD) protocol.   
Describe the improvements and benefits of CAN-FD over classical CAN (CAN2.0).   
Present theCAN-FDimplementation in the TM32 microcontrollers and microprocessors isted i the table below.   
Describe the various modes and specific features of the FDCAN peripheral.

STM32 devices in this document.

Table 1. Applicable products   

<table><tr><td>Product classes</td><td>Product series</td></tr><tr><td>Microcontrollers</td><td>STM32C0 series, STM32G0 series, STM32G4 series, STM32H5 series, STM32H7 series, STM32L5 series, STM32N6 series, STM32U5 series.</td></tr><tr><td>Microprocessors</td><td>STM32MP1 series.</td></tr></table>

# 1 General information

This application note gives an overview of the FDCAN peripheral embedded in the STM32 microcontrollers and microprocessors listed in Table 1, that are Arm® Cortex® core-based devices.

# Note:

Arm is a registered trademark of Arm Limited (or its subsidiaries) in the US and/or elsewhere.

# 2 CAN-FD protocol overview

The CAN-FD protocol (CAN with flexible data-rate) is an extension of the classical CAN (CAN 2.0) protocol. CAN-FDsheCAN .0or. I effct port stbu eal-timeontol wit aveyhih-v security. CAN-FD was developed by Bosch and standardized as ISO 11898-1:2015 (suitable for industrial, automotive, and general embedded communications).

# CAN-FD features

Main features of the CAN-FD protocol are listed below:

Compatibility with the CAN protocol: CAN-FD node is able to send/receive CAN messages according to   
ISO 11898-1   
Error-checking improvement, based on checksum field up to CRC 21 bits   
Prioritization of messages   
Guarantee of latency times   
Configuration flexibility   
Multicast reception with time synchronization   
System-wide data consistency up to 64 bytes per message   
Multimaster   
Error detection and signaling   
Distinction between temporary errors and permanent failures of nodes and autonomous switching off of   
defect nodes

# 2.2

# CAN-FD format

Thedata sent package intomessage  hown n he gurebelowAAN-Dmeage an edivi three phases:

a first arbitration phase a data phase 3a second arbitration phase

![](images/3373beced460c0b95dffbc961bdbfe1050f8404a004eadb5ddd999d428fbcf8a.jpg)  
Figure 1. Standard CAN-FD frame

The first arbitration phase is a message that contains:

a start of frame (SOF)   
an ID number and other bits, that indicate the purpose  themessage supplying or requesting data), and   
the speed and format configuration (CAN or CAN-FD)

The data transmission phase consists on:

the data length code (DLC), that indicates how many data bytes the message contains   
the data the user wishes to send   
the check cyclic redundancy sequence (CRC)   
a dominant bit

The second arbitration phase contains:

the receiver of acknowledgment (ACK) transmitted by other nodes on the bus (if at least one has successfully received the message) • the end of frame (EOF) No message is transmited during the IFS: the objective is to separate the current frame with the ne

# Note:

Th IDE in the first arbitration phase.

# Improvements and benefits of CAN-FD over CAN 2.0

The CAN-FD development responds t the needof communication networks that require higher bandwidth. This sreaaoack ol urheb phase.

The data transfer integrity is ensured by:

a CRC used to checksum a payload of up to 16 bytes based on 17 stage polynomial a 21-stage polynomial used to checksum the payload between 16 and 64 bytes

# Frame architecture comparison between CAN-FD and CAN 2.0

Te maiifennrmhitecur  AN-cpar AN.istratheguew

# CAN 2.0: Classical base frame format

![](images/c6150d2f883e71d1464166e9944a724d2b76d244c5a21e8248f7ac9f990895fd.jpg)  
Figure 2. Frame architecture of CAN-FD versus CAN 2.0

# CAN-FD: CAN flexible data rate base frame format

![](images/c833361a0d6f54153dc9a7adae55a03fad6a90163cd3e4d3476c128deee9a76b.jpg)  
DEL = Deliminator RTR = Remote transmission request

After identifier, CAN 2.0 and CAN-FD have a different action:

CAN 2.0 sends an RTR bit to precise the type of frame: data frame (RTR is dominant) or remote frame (RTR is recessive). CAN-FD sends always a dominant RRS (reserved) as it only supports data frames.

T IDE ehe pictg ee a oha ins e (29-bit identifier).

n the CAN-FD frame, three new bits are added in the control field compared to CAN 2.0

Extend data length (EDL) bit: is recessive to signify the frame is CAN-FD, otherwise this bit is dominant (called R0) in CAN 2.0 frame. B rate switching (BRS): indicates whether two bit rates areenabled or example when the data phasis transmitted at a different bit rate to the arbitration phase). • Error state indicator (ESl): indicates if the node is in error-active or error-passive mode.

T bot CAN 2.0 and CAN-FD. The DLC function is the same in CAN-FD and CAN 2.0, but with small changes on CAN-Darnghe payld at legcodtahe ble belowCAN-FDalloete be sent of up to 64 data bytes in a single message while CAN 2.0 payload data is up to 8 bytes.

Table 2. Payload data length codes (bytes)   

<table><tr><td rowspan=1 colspan=1>DLC (Dec)</td><td rowspan=1 colspan=1>0</td><td rowspan=1 colspan=1>1</td><td rowspan=1 colspan=1>2</td><td rowspan=1 colspan=1>3</td><td rowspan=1 colspan=1>4</td><td rowspan=1 colspan=1>5</td><td rowspan=1 colspan=1>6</td><td rowspan=1 colspan=1>7</td><td rowspan=1 colspan=1>8</td><td rowspan=1 colspan=1>9</td><td rowspan=1 colspan=1>10</td><td rowspan=1 colspan=1>11</td><td rowspan=1 colspan=1>12</td><td rowspan=1 colspan=1>13</td><td rowspan=1 colspan=1>14</td><td rowspan=1 colspan=1>15</td></tr><tr><td rowspan=1 colspan=1>CAN 2.0</td><td rowspan=1 colspan=1>0</td><td rowspan=1 colspan=1>1</td><td rowspan=1 colspan=1>2</td><td rowspan=1 colspan=1>3</td><td rowspan=1 colspan=1>4</td><td rowspan=1 colspan=1>5</td><td rowspan=1 colspan=1>6</td><td rowspan=1 colspan=1>7</td><td rowspan=1 colspan=1>8</td><td rowspan=1 colspan=1>8</td><td rowspan=1 colspan=1>8</td><td rowspan=1 colspan=1>8</td><td rowspan=1 colspan=1>8</td><td rowspan=1 colspan=1>8</td><td rowspan=1 colspan=1>8</td><td rowspan=1 colspan=1>8</td></tr><tr><td rowspan=1 colspan=1>CAN-FD</td><td rowspan=1 colspan=1>0</td><td rowspan=1 colspan=1>1</td><td rowspan=1 colspan=1>2</td><td rowspan=1 colspan=1>3</td><td rowspan=1 colspan=1>4</td><td rowspan=1 colspan=1>5</td><td rowspan=1 colspan=1>6</td><td rowspan=1 colspan=1>7</td><td rowspan=1 colspan=1>8</td><td rowspan=1 colspan=1>12</td><td rowspan=1 colspan=1>16</td><td rowspan=1 colspan=1>20</td><td rowspan=1 colspan=1>24</td><td rowspan=1 colspan=1>32</td><td rowspan=1 colspan=1>48</td><td rowspan=1 colspan=1>64</td></tr></table>

Toveaa are pylahe ult packeandnquentl eestr n ydmore  RC field:

If the payload data is up to 16 bytes, CRC is coded in 17 bits.   
If the payload data is higher than 20 bytes, CRC is coded in 21 bits.

n addition, to ensure the CAN-FD frame robustness, the CRC field is supported by stuff bit mechanism.

The table below summarizes the main difference between CAN-FD and CAN 2.0.The main features that provide an improvement on CAN-FD compared to CAN 2.0 are the increase of data payload and the higher speed ensured by the BRS, EDL and ESI bits available in CAN-FD.

Table 3. Main differences between CAN-FD and CAN 2.0   

<table><tr><td rowspan=1 colspan=1>Features</td><td rowspan=1 colspan=1>CAN 2.0</td><td rowspan=1 colspan=1>CAN-FD</td></tr><tr><td rowspan=1 colspan=1>Compatibility</td><td rowspan=1 colspan=1>Does not support CAN-FD</td><td rowspan=1 colspan=1>Supports CAN 2.0 A/B</td></tr><tr><td rowspan=1 colspan=1>Maximum bit rate (Mbit/s)</td><td rowspan=1 colspan=1>Frame bitrate: up to 1</td><td rowspan=1 colspan=1>Arbitration bitrate: up to 1sData bitrate: up to 8</td></tr><tr><td rowspan=1 colspan=1>DLC field (4 bits) code</td><td rowspan=1 colspan=1>Coded in 0 to 8</td><td rowspan=1 colspan=1>Coded in 0 to 64</td></tr><tr><td rowspan=1 colspan=1>Maximum data bytes in one message</td><td rowspan=1 colspan=1>8 bytes of data</td><td rowspan=1 colspan=1>64 bytes of data</td></tr><tr><td rowspan=1 colspan=1>BRS support</td><td rowspan=1 colspan=1>No</td><td rowspan=1 colspan=1>Yes</td></tr><tr><td rowspan=1 colspan=1>EDL support</td><td rowspan=1 colspan=1>No</td><td rowspan=1 colspan=1>Yes</td></tr><tr><td rowspan=1 colspan=1>ASI support</td><td rowspan=1 colspan=1>No</td><td rowspan=1 colspan=1>Yes</td></tr><tr><td rowspan=1 colspan=1>CRC bits check codes</td><td rowspan=1 colspan=1>Bits not included in CRC calculation</td><td rowspan=1 colspan=1>Bits included in CRC calculation</td></tr><tr><td rowspan=1 colspan=1>Remote frame support</td><td rowspan=1 colspan=1>Yes</td><td rowspan=1 colspan=1>No</td></tr></table>

Note:

For more details regarding CAN 2.0 and CAN-FD, refer to Bosch documentation available on their website.

# 4 Implementation of CAN-FD in STM32 devices

The STM32 devices defined in Table 1 embed an FDCAN peripheral that supports the CAN-FD protocol according to ISO 11898-12015. Most STM32 devices support more than one instance of CAN. Refer to the product datasheet for the number of instances available on a specific device.

The range of features and fnctionalities offered by the Flexible Data-rateController Area Network (DCAN feature in STM32 devices is dependent on the specific implementation of the device.

lanpan lA a me ileai the FDCAN superset.

# FDCAN peripheral main features

The features of the FDCAN on STM32 devices are listed below:

Compliant with CAN protocol version 2.0 part A, B and ISO 11898-1: 2015, -4   
Accessible 10-Kbyte RAM memory to allocate up to 2560 words   
Improved acceptance filtering   
Two configurable receive FIFOs   
Up to 64 dedicated receive buffers   
Separate signaling on reception of high priority messages   
Up to 32 dedicated transmit buffers   
Configurable transmit FIFO and transmit queue   
Configurable transmit event FIFO   
Clock calibration unit   
Transceiver delay compensation

The figure below illustrates the FDCAN block diagram.

![](images/769a4d8de8f652decd70fe9e924151a3bd547c108d5d1672c87b40f9acd4463b.jpg)  
Figure 3. FDCAN block diagram

The FDCAN block diagram characteristics are listed below:

All the FDCAN instance numbers share the same memory.   
Each FDCAN instance contains the CAN core.   
The CAN core presents the protocol controller and receive/transmit shift registers.   
The Tx handler controls the message transfer from the CAN message RAM to the CAN core.   
The Rx handler controls the transfer of received messages from the CAN core to the external CAN message RAM.

# 4.2 RAM management

Alltransmitted and received messages are stored in the CAN message RAM. During CAN message RAM messages to transmission.

# 4.2.1 RAM organization

The quantidat bys permege must econiguredetermie hememoryspaceha isequi pe message. The increase of the payload on CAN-FD results in more efficient memory usage and allows more messages to be stored in the allocated memory space.

A dedicated RAM reserved to FDCAN on STM32 devices is used to allocate up to 2560 words of 32 bits. This reserved RAM space makes the CPU more efficient.

As illustrate in the figure below, the CAN message RAM is split into four different sections:

section filtering (11-bit filter, 29-bit filter) section reception (Rx FIFO 0, Rx FIFO 1, Rx Buffer) section transmission (Tx event FIFO, Tx Buffers) section trigger memory (Trigger memory)

![](images/fccfbfbfeb975041d23689d5e558f977d63cc172b7a84bd87e0937e837bb6a68.jpg)  
Figure 4. CAN message RAM mapping

All  A peal n gu beeul etl not be exceed the total CAN message RAM size. This RAM provides increased flexibility and performance by ealinghe psibility eliatu ecns an oepan suffcntmeory r heher

The configured elements of each section are allocated in a dynamic and successive way in the CAN message RAM according  the rder presentein above gure;however in rder avoid hesk exceding theRAM and for reliability reasons, a specific own start and end address is not assigned to each section.

FDCAN peripheral can configure threemechanisms or transmission: Tx bufferandorTx queue and/or Tx FIFO un euwi ar memory ement tartres redefineieguratin urbetween , ae to overlap.

# Note:

The et anheraissnepl e torenet RAM eTh n h, eDLC,h ESI XTD RTRBRS FDF ean tranission/eception b ldorcontol.The mainig bitsf te messageare hand autoatally by hardware and are not saved in the RAM.

T .   
The specific bits fields for transmission are message marker and event FIFO control bit.

l  hav u     u calculated to reserve:

Hearoati twoeserv 3ors) llcate heentie,heDLfel he iol and the specific transmission/reception bits fields

Data (the number of 32-bit words sufficient) to contain the number of bytes per data field he formula below determines the number of 32-bit words allocated for each element

Element size (in words) = Header information (2 words) + Data (data field/4) where data field is the number of data bytes per message.

# Note:

If the data field is in the range of 0 to 8, 2 words are allocated for the data per element.   
The necessary "element" size depending on data field range is detailed in the table below.

Table 4. "Element" size number depending on data field range   

<table><tr><td rowspan=1 colspan=1>Data field (bytes)</td><td rowspan=1 colspan=1>Element size (RAM words)</td></tr><tr><td rowspan=1 colspan=1>0 to 8</td><td rowspan=1 colspan=1>4</td></tr><tr><td rowspan=1 colspan=1>12</td><td rowspan=1 colspan=1>5</td></tr><tr><td rowspan=1 colspan=1>16</td><td rowspan=1 colspan=1>6</td></tr><tr><td rowspan=1 colspan=1>20</td><td rowspan=1 colspan=1>7</td></tr><tr><td rowspan=1 colspan=1>24</td><td rowspan=1 colspan=1>8</td></tr><tr><td rowspan=1 colspan=1>32</td><td rowspan=1 colspan=1>10</td></tr><tr><td rowspan=1 colspan=1>48</td><td rowspan=1 colspan=1>14</td></tr><tr><td rowspan=1 colspan=1>64</td><td rowspan=1 colspan=1>18</td></tr></table>

A epl fcint eAAM illrate u belowheas an application where the FDCAN peripheral is configured:

to send 32 messages with dedicated Tx buffer (each message contains 8 bytes in the data field) to have 128 11-bit filters for acceptance of the messages to receive 64 messages where each message contains 64 bytes in data field in dedicated Rx buffers to receive 64 messages where each message contains 64 bytes in data field in Rx FIFO 0

![](images/e1364618db68ad6c5f40540a58887aa2a7021ea4b2772ea990a3b40a91f2ad7d.jpg)  
Figure 5. RAM mapping example for and efficient use of the CAN message RAM

In this example, the allocation in the RAM is done in the following order:

Allocate 128 words in the section ID-11bits.   
2Reserve 1152 words for the reception of the elements in the section Rx FIFO 0.   
3Reserve 1152 words for the reception of the elements in the section Rx buffer.   
Reserve 128 words for the elements sent in Tx buffer.

Thank heaiaon  oakiyllatn use wholory the RAM is used efficiently: allthe 2560 words are allocated in this application.

After the configuration, the allocated address range is initialized to zero.

# 4.2.2 Multiple FDCAN instances

Most STM32 devices support more than one FDCAN instance to meet all the application requirements (rfer to the product datasheet for the number of instances).

Inah the RAM on the various instances (each instance size is chosen by indicating its start offset address).

An example of a CAN message RAM using multiple DCAN instances isillustrated in the figure below. This phaeviAeAMehes the double of the second instance.

![](images/034ec5b14ece5d3a75b37eb09468855b51c086a3e9ec0e9977ee62d6d146b936.jpg)  
Figure 6. Example of CAN message RAM with multiple FDCAN instances

# 4.3

# RAM sections

# 4.3.1

# RAM filtering sections

T a xtn eUpt for 11-bit standard IDs and up to 64 filter elements can be configured for 29-bit extended IDs.

The arres  1-bt file ecion ogur vi he LSSA[13:0] bit he DCANSIDFCegi the 29-bit filter section is configured via the FLESA[13:0] in the FDCAN_XIDFC register.

The gure below shows a secton f he CANmessage RAM with he number fr elements and the tar addresses.

![](images/5e131c53d7e8f526a1273a62146df5466b23ff2f100aa7423cf80a6c8ea79230.jpg)  
Figure 7. CAM message RAM filters section

These filters can be assigned to the Rx FIFO 0/1 or to the dedicated Rx buffers. When the FDCAN performs elmnt.Accptance fitering stops at the rstmatching element and thefollowing filer elements e not Teuna performance of the filtering process.

The usehooes enablerdisable each filelement,an can configureeac element acptac rejection filtering. Each filter element can be configured as:

Range filter: the filter matches for all messages with an identifier in the range defined by two IDs. Filter for dedicated IDs: the filter can be configured to match for one or two specific identifiers. Clat as fltat grouent maskng eiventie D coigured is used as message ID filter, the second ID is used as filter mask. Each zero bit at the iter mask masks out the corresponding bit position of the configured ID filter.

# Note:

l  ela ny whenhee nhee fn all mask bits equal 0, all message IDs match.

# 4.3.1.1

# High-priority message:

The FDCAN can notify the user when a high priority message is received. This notifications can be used to monitor the status of incoming high-priority messages and to enable fast access to these elements.

TA tei-prre wit elpesm oiee settings related to high-priority messages:

Set priority and store in FIFO 0/1 if filter matches: if this message filter matches, the FDCAN informs about the high-priority message arrival and stores the element in Rx FIFO 0/1. Set priorityif filter matches: if thismessage filermatches, the FDCAN notis about the high-ity message arrival but does not store the element.

The following flow chart explains the global mechanism of an acceptance filter.

![](images/b350b451ce5e49e08100102e1e3f3742b45c3fbc5c5b8e1b81cd6586b7372f8f.jpg)  
Figure 8. Global flow chart of acceptance filter

# Example to illustrate the acceptance filtering

user wants to configure the FDCAN:

to reject all the messages with identifier in the range [0x16 to 0x20] to accept all the messages with identifier equal to 0x15 or 0x120 and to store them in FIFO 1 to accept the message with identifier equal to Ox130 and store it in the Rx buffer index 4

to accept the messages with identifier that corresponds to:

bits [10..6] = 0b111 00 bits [5..4] = don't care bits [3..0] = 0b00000

In this case, the filter must be configured as classic bit mask filter because the accepted identifer correspond to Ob11100xx0000 (where x can be any value in 0 or 1). The accepted identifiers are:

0b111 0000 0000 (0x700)   
0b111 0001 0000 (0x710)   
0b111 0010 0000 (0x720)   
0b111 0011 0000 (0x730)

The base filter ID can be any value in Ox700, Ox710,0x720,0x730. The mask filter ID equals 0b111 1100 1111 (0x7CF).

Taet above example. Each standard filter element contains:

SFT bits (standard filter type)   
SFEC bits (standard filter element configuration). SFID1 bits (standard filter ID1)   
SFID2 bits (standard filter ID2)

Table 5. Standard filter element configuration   

<table><tr><td rowspan=1 colspan=1>Filter</td><td rowspan=1 colspan=1>Standard filter typeSFT [31:30]</td><td rowspan=1 colspan=1>Standard filter elementconfigurationSFEC [29:27]</td><td rowspan=1 colspan=1>Standard filter ID 1SFID1 [26:16]</td><td rowspan=1 colspan=1>Standard filter ID 2SFID2 [15:0]</td></tr><tr><td rowspan=1 colspan=1>First</td><td rowspan=1 colspan=1>00 - Range filter</td><td rowspan=1 colspan=1>011 - Reject</td><td rowspan=1 colspan=1>0x16</td><td rowspan=1 colspan=1>0x20</td></tr><tr><td rowspan=1 colspan=1>Second</td><td rowspan=1 colspan=1>01 - Dual ID</td><td rowspan=1 colspan=1>010 - Store in FIFO 1</td><td rowspan=1 colspan=1>0x15</td><td rowspan=1 colspan=1>0x120</td></tr><tr><td rowspan=1 colspan=1>Third</td><td rowspan=1 colspan=1>xx - Don&#x27;t care</td><td rowspan=1 colspan=1>111 - Store in Rx buffer</td><td rowspan=1 colspan=1>0x130</td><td rowspan=1 colspan=1>0x04 (buffer index)</td></tr><tr><td rowspan=1 colspan=1>Fourth</td><td rowspan=1 colspan=1>10 - Classic bit mask filter</td><td rowspan=1 colspan=1>001 - Store in FIFO 0</td><td rowspan=1 colspan=1>0x700</td><td rowspan=1 colspan=1>0x7CF</td></tr></table>

The first filter is configured to reject the messages with ID in the range [0x16...0x20].

The second filter is configured to store in Rx FIFO 1, the messages with ID equal to dual ID Ox15 or Ox120.   
The third filter is configured to store in Rx buffer index 4, the message with ID equal to Ox130 .

# Note:

I  s conure s Stoe ntox bufr"henhe cnguration   s or.Theacptan stops at the first match. So the order of the filters is important.

T product datasheet for more details).

The numerous filter possibilities of the FDCAN allow a complex message filtering in hardware, which makes software filtering redundant and saves CPU resources.

# 4.3.2 Reception section

# 4.3.2.1

# Rx FIFO 0 and Rx FIFO1

Two Rx FIFO can be configured in the CAN message RAM. Each Rx FIFO section can store up to 64 elements.   
Each element is stored in one Rx FIFO element.

The size f a Rx FIFO element can be coniguredvia the DCANRXESC register or each Rx FIFOindivally. The R FFO element ize defies howmany dat field byte receiv eement can e stord.The iz Rx FIFO element is defined by the formula specified in Section 4.2.1: RAM organization.

H   fmatching frame, Rx timestamp).

Aerhe configuration f the element iz i the1DS[2:] feld in theDCANRXESC gister, he u elements and the start address of Rx FIFO 1 must be configured respectively via the F1S[6:0] and F1SA[13:0] fields in the FDCAN_RXF1C register.

The figure below shows the Rx FIFO section on the CAN message RAM with the number of elements that can supported and the start address for each section.

![](images/4292aef0455d34e495c68c24cd7b41bb5c800f34baff0864a092fe8069b0b7aa.jpg)  
Figure 9. Rx FIFO section in CAN message RAM

or O tha pe ohea hea.

: the Rx FIFO is full, the newly arriving element can be handled according to two different modes:

• Bloking mode: this is the default operation mode of the Rx FFO,o further elements are written to the Rx FIFO until at least one element has been read out. Overwrite mode: The new element accepted in the Rx FIFO overwrites the oldest element in the Rx FIFO and the put and get index of the FIFO are incremented by one.

To read an element from an Rx FIFO, the CPU has to perform the following steps:

Read the register FDCAN_RXF1S to know the status of the Rx FIFO.

2. Calculate the address of the oldest element in the RAM as with the following formula: Oldest element address = CAN_message_RAM_base_address + FDCAN_RXF1C.F1SA (start address) + FDCAN_RXF1S.F1GI (get Index) x Rx FIFO_element_size.

3Read the element from the calculated address.

After hePU has read an element r  equence  elements rom heRx FIFOit mus acknowleg hera. After acknowledgement, the FDCAN can reuse the corresponding Rx FIFO buffer for a new element. To t wd  mO FDCAN_RXF1A register. As a consequence, the FDCAN updates the FIFO fll level and the get index.

The following chart presents a simplified operation of Rx FIFO.

![](images/157e2c80cad4699e09f825eb1345cf39d484b610a3ed674c0d0e2a5501a31703.jpg)  
Figure 10. Simplified operation of Rx FIFO

# Note:

The registers of Rx FIFO 0 and Rx FIFO 1 have identical registers with meaningful names by changing the number of FIFO each time.

# 4.3.2.2

# Dedicated Rx buffer section

The FDCAN supports up to 64 dedicated Rx buffers. Each dedicated Rx buffer can store one element.

The iz dedicatedRx bufer an becongured via theDCANRXECegister.heRxbufer ize ee hmanyda fd bytimn n torei deicat bufdf y the formula described in Section 4.2.1: RAM organization.

After the configuration of the element size via the RBDS[2:0] field in the FDCANRXESC register, the start address must be configured via the RBSA[13:0] field in the FDCAN_RXBC register.

The figure below shows the Rx buffer section on the CAN message RAM with the maximum number of dedicated 2x buffer elements that can be supported and the start address.

![](images/9c8ebfb957d7247424668de90a92de6950513a209d508a004c06fc6419e8d86f.jpg)  
Figure 11. Rx buffer section on CAN message RAM

Whena element isstore n  dedicatedRx buffer,he DCAN sets thenterupt fagthe DRX bit e FDCAN_IR register and the corresponding bit in the new data flag FDCAN_NDAT1 or FDCAN_NDAT2 registers. Wh DCANA1/,heR u c oie FDCAN_NDAT1/2, in order to unlock the respective Rx buffer.

To read an element from a dedicated Rx buffer, the CPU must perform the following steps:   
1. Check the bits in FDCAN_NDAT1/2 to know if a new element arrived in a dedicated Rx buffer.   
2. Calculate the address of the element in the CAN message RAM, as determined by the formula below: Reference Rx buffer address = CAN_message_RAM_base_address + FDCAN_RXBC.RBSA (start address) + dedicated Rx buffer index x Rx_Buffer_element_size.

3Read the message from the calculated address.

The filter element can reference Rx buffers index (0 to 63) as destination for a received element. I the can  wr ut. e, the FDCAN does not write to unreferenced Rx buffer locations.

# Example for the relative configuration of Rx buffer number to the Rx buffer index

Iuu s

# Note:

The user must choose the best configuration to avoid wasting the RAM.   
The figure below presents a flowchart to simplify the operation of Rx buffer.

![](images/ab1e9973a6f72c7e4333e2555069ddd285efb1cd0a1256e4b4a774ac969efb65.jpg)  
Figure 12. Simplified operation of Rx buffer

# 4.3.2.3

# Differences between dedicated Rx buffer and Rx FIFO

preente in he previous section, he DCAN has two mechanis:ither a dedicat Rx buf r Rx FIFO 0/1 can be configured to store a received element.

he differences between a dedicated Rx buffer and an Rx FIFO are described in the table below.

Table 6. Differences between dedicated Rx buffer and Rx FIFO   

<table><tr><td rowspan=1 colspan=1>Feature</td><td rowspan=1 colspan=1>Dedicated Rx buffer</td><td rowspan=1 colspan=1>Rx FIFO</td></tr><tr><td rowspan=1 colspan=1>Sections to configure</td><td rowspan=1 colspan=1>64 dedicated Rx buffers can be configured .</td><td rowspan=1 colspan=1>Two Rx FIFO can be configured.</td></tr><tr><td rowspan=1 colspan=1>Elements per section</td><td rowspan=1 colspan=1>Configured to contain only one element perbbuffer</td><td rowspan=1 colspan=1>May contain one or more elements (up to 64elements) per section</td></tr><tr><td rowspan=1 colspan=1>Position in the RAM</td><td rowspan=1 colspan=1>The user chooses the buffer index.</td><td rowspan=1 colspan=1>The position in the RAM is automatically anddynamically managed (using the incrementing ofget/put index).</td></tr><tr><td rowspan=2 colspan=1>Discards newly arrivingelement configuration</td><td rowspan=1 colspan=1>Discards the newly arriving element when bufferis locked.</td><td rowspan=2 colspan=1>Discards the newly arriving element when RxFIFO is full (blocking mode by default).Note: Overwrite mode option to receive the newelement and overwrite the oldest element.</td></tr><tr><td rowspan=1 colspan=1>Note: The user must reset the corresponding bitin FDCAN_NDAT1/2.</td></tr></table>

# 4.3.3 Transmission section

# 4.3.3.1 Tx event FIFO section

By using a Tx event FIFO, the CPU gets the following information about the sent elements:

in which order the elements were transmitted the local time when the frame was transmitted for each element

The DCAN provides a Tx event FFO.The use of this Tx event FFO is optional. After the DCAN succsfully transmitted an element on the CAN bus, it can store the message ID and the timestamp in a Tx event FIFO en em aucuraoratbouite event FIFO can be configured vi the DCANTXEFC register Tx event FFO configuration). The FIFO can store a maximum of up to 32 elements.

The following figure shows an example of a CAN message RAM where the Tx event FFO elements are stored and the EFSA[13:0] field contains the start address.

![](images/08d63fddb44ea917f361a168d65f6ef4012a5968615e1f6d6f1b96f2530adb44.jpg)  
Figure 13. Tx event FIFO section in the CAN message RAM

The address of a Tx event FIFO element in the CAN message RAM, is determined by the formula below:

Tx event FIFO element address = CAN_message_RAM_base_address + FDCAN_TXEFC.EFSA (start address) + FDCAN_TXEFS.EFGI (get index) x Tx_event_FIFO_element_size

Toi   n FO aei u the Tx event FIFO element.

E ovn OnC t) i .

W event is discarded. To avoid a Tx event FIFO overflow, the Tx event FIFO watermark can be used.

Ater the CPU read an element or a sequence  elements from theTx event FFO, the CPU must acknowledge A FDCAN_TXEFA register.

# 4.3.3.2 Tx buffer section

For a module to transmit an element, the element is formed within the defined memory space and the h the mechanism to be used: a dedicated Tx buffer and/or Tx queue or Tx FIFO.

Up to 32 elements ae supported by he DCAN. Each element stores the identifier, the DLC, the conrol bit , XTD,RTR, BRS, DF), he atfel he femea nd e vent IFO ol one message.

T h  eo  FOa  que er n  qu  h application: a combination of them is not supported by the FDCAN.

u0 FDCAN_TXBC register.

![](images/b937b901e5c709f61bad377214cbd3761f9e90ec2e97784f843e852db2112df6.jpg)  
Figure 14. Tx buffer section in CAN message RAM

# Note:

As idicat in the previus ection,heallatin theRAM ismadena dnian scesive way the user does not configure a dedicated Tx buffer mechanism. The Tx buffer section contains only the configured Tx queue or Tx FIFO and it is stored in the start section address.

# Dedicated Tx buffers

The numberof dedicated Tx buffers are configured via the NTDB[5:0] field in the DCAN_TXBC register. Each deicat T bufrisgurd wiha pecientifer tsorenlyement Te issni requested by an add request via the FDCAN_TXBAR register. The requested messages arbitrate externally with messages on the CAN bus, and are sent out according to the lowest identifier (highest priority).

Thememory requments or hedeicat Tx bufr epend on he Tx bufrement iz. The T uff element size defines the number of data bytes belonging to a Tx buffer.

The address of a dedicated Tx buffer in the CAN message RAM is calculated using the formula below:

Dedicated Tx buffer address = CAN_message_RAM_base_address + FDCAN_TXBC[TBSA] (start address) + Tx_buffer_index x Tx_buffer_element_size

The folowig flow har is usedto simpliy theoperation  a tranmisson with the Tx buffermechanim.

![](images/38c3cf59689a89c947560bd3687f2d4d2afd03f95f98dc3c451783c76749615a.jpg)  
Figure 15. Transmission with Tx buffer mechanism

u is transmitted first.

# Tx FIFO

The Tx FIFO operation is configured by writing 0 to the TFQM bit in FDCANTXBC. The elements stored in the Tx FIFO are transmitted starting with the element referenced by the get index via the TFG1[4:0] field in ANF.sn   lt

The TFFOableheaision nt her hemet havbewitte   FIFO. T FIFO is sent out first.

The FDCAN calculates the Tx FIFO buffer free level via the TFFL[5:0] field in FDCAN_TXFQS as a diffence between get nd put index (get nd e index twomechanism ncrements ac tansaction tdicatehe next ua elements.

Newri ent must  ien heT FOtar wit e ufnc byhe u indicated via the TFAQPI[4:0] field in FDCAN_TXFQS.

The address of the next free Tx FIFO buffer in the CAN message RAM is calculated with the below formula:

Vext free Tx FIFO buffer address = CAN_message_RAM_base_address + FDCAN_TXBC.TBSA (star address) + FDCAN_TXFQS.TFQPI (put Index) x Tx_FIFO_element_size

he following flow chart shows a simplified operation of the transmission with Tx FIFO mechanism.

![](images/7d23fe590c38b18c481354507a915b7413483baa7e727f0d542727701e7a5fad.jpg)  
Figure 16. Transmission with Tx FIFO mechanism

# Tx queue

Tx queue operation is configured by writing 1 to theTFQM bit in DCAN_TXBC. The elements stored in he Tx queue are transmitted starting with the Tx queue buffer with the lowest Identifier (highest priority).

In contrast to dedicated Tx buffrs, the position on the RAM is automatically and dynamically managed so the message identifier is not fixed to a predefined Tx buffer index.

Newmeags haveeritene u bufec yhe unde.n qu y bit set to 1 in FDCAN_TXFQS. No further element must be written to the Tx queue until at least one of the requested elements is sent out or a pending transmission request is cancelled.

The memory reqirments or theTx queue bufrdepend o the numbe data bytes belonging  Tx queue element.

Tvaabl  buAM n alculat e formula:

Next free Tx queue buffer address = CAN_message_RAM_base_address + FDCAN_TXBC.TBSA (start address) + FDCAN_TXFQS.TFQPI (put index) x Tx_Buffer_element_size

The following flow chart shows a simplified operation of the transmission with Tx queue mechanism.

![](images/eed96f8a25ac00166d84df36bcd0d6e72544e4c7a92a952372dce2e2a340ceac.jpg)  
Figure 17. Transmission with Tx queue mechanism

# Differences between dedicated Tx buffer, Tx FIFO and Tx queue

The diffrencs between a dedicated Tx buffer a Tx FIFO and a Tx queue aredescribd in he tablebelow.

Table 7. Differences between dedicated Tx buffer, Tx FIFO and Tx queue   

<table><tr><td rowspan=1 colspan=1>Feature</td><td rowspan=1 colspan=1>Dedicated Tx buffer</td><td rowspan=1 colspan=1>Tx FIFO</td><td rowspan=1 colspan=1>Tx queue</td></tr><tr><td rowspan=1 colspan=1>Sections that can beconfigured</td><td rowspan=1 colspan=1>32 dedicated Tx buffers can beconfigured.</td><td rowspan=1 colspan=1>One Tx FIFO can configured.</td><td rowspan=1 colspan=1>One Tx queue can configured.</td></tr><tr><td rowspan=1 colspan=1>Elements per section</td><td rowspan=1 colspan=1>Tx buffer is configured to containonly one element per buffer.</td><td rowspan=1 colspan=1>May contain one or moreelements per section (up to 32)</td><td rowspan=1 colspan=1>May contain one or moreelements per section (up to 32)</td></tr><tr><td rowspan=1 colspan=1>Element to be sentfirst</td><td rowspan=1 colspan=1>Element with the lowest ID issent first.</td><td rowspan=1 colspan=1>Elements transmitted in the FIFOorder</td><td rowspan=1 colspan=1>Element with the lowest ID issent first.</td></tr><tr><td rowspan=1 colspan=1>Behaviour if multipleelements with thesame ID are present</td><td rowspan=1 colspan=1>The first transmission request issent first.</td><td rowspan=1 colspan=1>No prioritization with identifier</td><td rowspan=1 colspan=1>FIFO order</td></tr><tr><td rowspan=1 colspan=1>Position in the RAM</td><td rowspan=1 colspan=1>User chooses the buffer index.</td><td rowspan=1 colspan=2>Automatically and dynamically managed (using the incrementing ofget and put index)</td></tr><tr><td rowspan=1 colspan=1>Pending elementsmanagement</td><td rowspan=1 colspan=1>Elements become pending afterbeing added to the RAM or afterthe tx buffer request is enabled.</td><td rowspan=1 colspan=2>Elements become pending after being added to the RAM (therequest is automatically enabled).</td></tr></table>

# Flexible transmission configuration

A eficint CAN supports i cgurations allow more fxibiltnrnsissons an takeebe advantage o each mechanism benefits.The supported mixed configurations are dedicated Tx buffer +Tx FIFO and dedicated Tx buffer + Tx queue.

# Mixed configuration: dedicated Tx buffers and Tx FIFO

The Tx buffer section of the CAN message RAM can be configured with a mixed configuration, where the Tx buffers section in the CAN message RAM is subdivided into a set of dedicated Tx buffers and a Tx FIFO.

The numberof dedicated Tx buffer is configured via NDTB[5:0] in FDCAN_TXBC. The number f Tx buffers assigned to the Tx FIFO is configured via TFQS[5:0] in FDCAN_TXBC.

Tan u euie transmitted next.

A use case using a mixed dedicated Tx buffer and a Tx FIFO is illustrated in the figure below.

![](images/f70dca25dc8d87eeb6acfd609a53d39ab8498982296ee5b0985ad2ae7d32f3aa.jpg)  
Figure 18. Mixed configuration with dedicated Tx buffers and Tx FIFO

Inhi example, theelment etrni n thefollowig order ssig that aldedicate Tx buffs requests are enabled):

priority than the oldest pending Tx FIFO: Tx buffer 7)   
2. t priority than the oldest pending Tx FIFO: Tx buffer 7)   
3. Tx bufr7 ecause  s theoldest pending Tx FFO with dentir =4 and has higher priority betwe all dedicated Tx buffers)   
4. Tu  ued  Oi =haseh dedicated Tx buffers)   
eh   n empty)   
6. = e  el empty)   
e empty)   
Tx buffer 5 (because t is the only pending dedicated Tx buffer

# Mixed configuration: dedicated Tx buffers and Tx queue

The Tx buffer section of the CAN message RAM can be configured with a mixed configuration where the Tx buffers ection n he CAN mesage RAM i ubdivied ito a set dedicatedTx buffers nd a Tx qe.

The numberof dedicated Tx buffers is configured via NDTB[5:0] in FDCANTXBC and the number of Tx queue buffers is configured via TFQS[5:0] in FDCAN_TXBC.

T Tnu i asne qu.   
The buffer with the lowest identifier gets the highest priority and is transmitted next.

use case using a mixed dedicated Tx buffer and a Tx queue is illustrated in the figure below

![](images/94a3e908557fdaa2766ee857ab39e09190a7a3f80cdff11fecdd9e67e09d6841.jpg)

In thi example, themesages ae tranite n the ollowigorder assig hat all dedicatd Tx buffers request are enabled):

Tx buffer 3 (identifier = 1: it is the highest priority between all other Tx buffers) Tx buffer 8 (identifier = 2: it is the highest priority between all other Tx buffers) 3. Tx buffer 0 (identifier = 3: it is the highest priority between all other Tx buffers) 4. Tx buffer 7 (identifier = 4: it is the highest priority between all other Tx buffers) 5. Tx buffer 4 (identifier = 8: it is the highest priority between all other Tx buffers) 6. Tx buffer 2 (identifier = 12: it is the highest priority between all other Tx buffers) 7Tx buffer 1 (identifier = 15: it is the highest priority between all other Tx buffers) Tx buffer 5 (because it is the only pending Tx buffer)

Note:

The mixed configuration with Tx FIFO and Tx queue is not supported.

# Differences between mixed configuration of dedicated buffer + Tx FIFO and mixed configuration of Tx buffer + Tx queue

The main differences between the mixd configurations Tx buffer + Tx queue and Tx buffer + Tx FIFO ae presented in the table below.

Figure 19. Mixed configuration with dedicated Tx buffers and Tx queue   
Table 8. Differences between mixed Tx buffer + Tx FIFO and mixed Tx buffer + Tx queue configurations   

<table><tr><td rowspan=1 colspan=1>Feature</td><td rowspan=1 colspan=1>Mixed configuration: Tx buffer + Tx queue</td><td rowspan=1 colspan=1>Mixed configuration: Tx buffer + Tx FIFO</td></tr><tr><td rowspan=1 colspan=1>Description</td><td rowspan=1 colspan=1>A combination of dedicated Tx buffers and Txqueue</td><td rowspan=1 colspan=1>A combination of dedicated Tx buffers and TxFIFO</td></tr><tr><td rowspan=1 colspan=1>Element to be sent first</td><td rowspan=1 colspan=1>Element with the lowest ID between all dedicatedTx buffers and Tx queue</td><td rowspan=1 colspan=1>Element with the lowest ID between all dedicatedTx buffers and oldest element in Tx</td></tr><tr><td rowspan=1 colspan=1>Management ofmultiple elements withsame ID</td><td rowspan=1 colspan=1>First request is sent first.</td><td rowspan=1 colspan=1>Order request FIFO</td></tr></table>

# Note:

In Tx FIFO + Tx queue, elements become pending just after the "add to the RAM" action.

# 4.3.4 Test modes

Within theoperation mode  a FDCAN, several test modes are available besides the normal operation.There test modes must be used for production tests or self-test only and for the calibration unit.

The TEST bit in FDCAN_CCCR must be set to 1 to enable a write access to the FDCAN test register and the configuration of test modes and functions.

The FDCAN works in one of the following modes:

Restricted-operation mode Bus-monitoring mode External loop-back mode Internal loop-back mode

# .3.4.1 Restricted-operation mode

In restricted-operation mode, the FDCAN is able:

to receive data frames to receive remote frames to give acknowledge to valid frames

This mode does not support:

data frames sending   
remote frames sending   
active error frames or overload frames sending

The FDCAN is set in the restricted-operation mode via the ASM bit in FDCAN_CCCR.

T o wheeo oCA nessage RAM on time or when the clock calibration is active.

I received a valid frame.

The following fgure illustrates theconnection of FDCANTX and FDCANRX pins in restricted-operation mode.

![](images/c4b87fbef6890d8b021c82927d05888162e0dceff6ffc397f5c16f893b606462.jpg)  
Figure 20. Pin control in restricted-operation mode

# Note:

FDCAN_TX pin isrecessive as longas FDCAN is in restricte-operation mode.A dominant bt is transmitt to acknowledge the reception of a valid frame.

# 4.3.4.2

# Bus-monitoring mode

the FDCAN in bus-monitoring mode via the MON bit in FDCAN_CCCR.

In bus-monitoring mode, the FDCAN is able:

to receive valid data frames to receive valid remote frames

This mode does not support:

transmission start acknowledge to valid frames (difference versus the restricted-operation mode)

In the bus-monitoring mode, the FDCAN only sends recessive bits on the bus. The figure below shows the connection of FDCAN_TX and FDCAN_RX pins in bus-monitoring mode.

![](images/eaef7e216d19cacac0ee3cfb5fd72c036900ee9ed436e96d69c86a3c2fdeffc3.jpg)  
Figure 21. Pin control in bus-monitoring mode

# 4.3.4.3

# External loop-back mode

Tmode ovie arware el-.euseraeAteal lop-back ode y 1 to the LBCK bit in FDCAN_TEST and by writing 0 to the MON bit in FDCANCCCR. The FDCAN treats its own transmittedmessages as received messages and stores them if they pass the acceptance filtering in Rx FIFO.

Ie enent fom eexteal atin,hCAoole ors t saple in theacknowlee slot).The performs an internal feedback fromt ransmitoutput  t receive" input.

The following figure shows the connection of FDCAN_TX and FDCAN_RX pins in external loop-back mode.

![](images/b8d495441cdd213e3df3688d67f4adcde8a5980fd9d03ddbc661d7d487bf111d.jpg)  
Figure 22. Pin control in external loop-back mode

# 4.3.4.4

# Internal loop-back mode

Thismode  providedorhardware elf-stThe user can et eCAN in ntenal loop-back mode y writing 1 to the LBCK bit in FDCAN_TEST and by writing 1 to the MON bit in FDCAN_CCCR.

The FDCAN can be tested without afecting a running CAN system connected to the FDCAN_TX and FDCAN_RX pins. FDCAN_RX pin is disconnected from the FDCAN and FDCAN_TX pin is held recessive.

The figure below shows the connection of FDCAN_TX and FDCAN_RX pin in internal loop-back mode.

![](images/d0d3334fef59d3c3ed726817dfeb1feddabe19289148981b2e2d04fe6d27f0b8.jpg)  
Figure 23. Pin control in internal loop-back mode

# 4.3.5

# Transceiver delay compensation

At the ample poi all trnsitte hec whetherhe previusynitt bi ismpl corret Thi manieec obl neteoemheite ieye oeyeyi G t  e reason why the transceiver delay compensation mechanism (TDC) was introduced.

![](images/df33e45e2d784f5aae3e986434aad577d4f1ddee3cc54b09ab78d901b2fc5f55.jpg)  
Figure 24. Bit timing

Inpeat o ey wheekngr ympe-poi I stored until the next sample point is reached.

An   generated or each b anmitt nhe dat pharansceiverasymmery andinging nhe us bit stream.

The transceiver delay compensation is enabled by writing 1 to the TDC bit in FDCAN_DBTP. The measurement sar ih achi Aa beheeihea ha  e ll FDF bit to bit es). Themeasrement sops when this ege s seen at e eceve nput p DANRX  e transmitter. The resolution of this measurement is 1 mtq (minimum time quantum).

The following figure presents the measurement of loop delay.

![](images/b3069a3e3221e576ae8ccd25b5a99ccb82e9e54e8d73a18fcad81847f72d77bf.jpg)  
Figure 25. Loop delay measurement

# Note:

During the arbitration phase, the delay compensation is always disabled.

The SSP position is defined as the sum of the measured delays from the FDCAN_TX pin to the FDCAN_RX pin, olus the transmitter delay compensation offset as configured via the TDCO[6:0] field in FDCAN_TDCR.

# Note:

The transmitter delay compensation offset is used to adjust the position of the SP inside the received bit.

T valasn guebelow,at how tni t quenctoKan reivd eqencR, together with a sequence of SPs from SSPA to SSPK.The received bit BR is checked at PB by comparin it eelay  Te pi eimeehe ar ei specific time is the sum of the measured transceiver delay and the configured SSP offset.

![](images/b23cc382cf59f218b8ccfadee09a4e7274627d2148d6fcd51946aa6838d750e1.jpg)  
Figure 26. SSP position in transmit delay-compensation

As determined in Bosch documentation, the following boundary conditions have to be considered for the transmitter delay compensation implemented in the FDCAN:

The sum of the measured delay from FDCAN_Tx to FDCAN_Rx and the configured transmiter delay compensation offset mus t be less than six bit times in the data phase.   
The sum of the measured delay from FDCAN_Tx to FDCAN_Rx and the configured transmiter delay compensation offset mus t be less or equal 127 mtq.   
If the sum exceeds 127 mtq, the maximum value (127 mtq) is used for transmitter delay compensation The data phase ends at the sample point of the CRC delimiter that stops checking received bits at the SSPs.

# Note:

T

# 4.3.6

# Clock calibration on FDCAN

The CAN suport he clock caliatinn (CCU)faturhis featue allows a usr calibrate DCAN receiver (device) by a FDCAN transmitter (host). For example, when the FDCAN device communicates with the newest bitrate of the host.

useful when the FDCAN receiver does not have a precise quartz (can cause an error on time).

# 4.3.6.1 CCU description

T cloc cltun liz the FDCANCCUCCFGriste, hat can ite nly whbo CCE and INIT bits are set to 1 in FDCAN_CCCR.

The CCU is only possible when the FDCAN operates in CAN 2.0 mode.

The clock calibration is bypassed when BCC = 1 in FDCAN_CCU_CCFG. The following figure shows the bypass operation.

![](images/513e8adbd35f380fb82f14c334826398bfd059c328314c0a3ca54d2f7072fdc0.jpg)  
Figure 27. Bypass operation of the CCU

# 4.3.6.2

# CCU operating conditions

The CCU operates only when the FDCAN bitrate is between 125 Kbit/s and 1 Mbit/s.

# 4.3.6.3 CCU functional description

Thecaliration fdcantqck (tme quantaclock)via CANmessages s perorme by adapting a clock ivie that generates the CAN protocol time quantum, tq, from the fdcan_ker_ck clock.

# Calibration of the state machine

The calibration of the functional state machine is illustrated below

![](images/3866cb3a8561cc8176705ba4c8ffe8a82405cab8c1fba1e4377748c4db83f076.jpg)  
Figure 28. Functional state machine calibration

TO: Hardware reset T3: Evaluate messages T6: Configuration change enabled T1: Check for minimum T4: Quartz message received T7: Watchdog event: no quartz message received T2: Message received T5: Evaluate quartz message T8: Watchdog event: no quartz message received or configuration change enabled

# Basic calibration

The minimum distance between two consecutive falling edges from recessive to dominant is measured. This maseasses wo A  mes cnt cock pes.Teclock divie sdatac t measurement finds a smaller distance between edges by the CDIV[3:0] field in FDCAN_CCU_CCFG. A basic calibration is achieved when the CAN protocol controller detects a valid CAN message.

# Precision calibration

Tlan aaheasug gensAmc an sT    an u in FDCAN_CCU_cCFG. Precision calibration is based on the new clock divider value, calculated from the measurement of the longer bit sequence.

Caliation ramesa detecte b heCAN acctance iltergfileelement nd nRx buf ut e configured in the FDCAN to identify and store the calibration messages.

If he can_erck caliration done y oftwae evaluating he aliai statu from CALS[1:0] feln FDCAN_CCU_CSTAT), the FDCAN must be set in restricted-operation mode until the calibration is in Precision_Calibrated state (no frame and no error or overload flag transmission, no error counting).

# Note:

Ar ceptiona calationmessge,heRx bufernew dat ag must ereset oenablesnali e next calibration message.

Thdatealanese must  as biayqunsuha devi can enter the Basic_Calibrated state, and that the host node messages are acknowledged.

l alialcontrolle clock.Precision calibration must be repeated in predefinedmaximumintervals supervised by the calibration watchdog.

# Calibration watchdog

Tlwach o oalaie messages.

When in Basic_Calibrated state, the calibration watchdog is restarted with each received message.

# Note:

In case nomessage is receiveduntil the calibration watchdog countd down to zero, the FM calibration tays in Not_Calibrated state. The counter is reloaded and basic calibration restarts.

Whnalalatral watchdog monitors the quartz message received.

# Note:

In case o message from a quartz-controlled node is received by the FDCAN until the calibration watchdog counted down to zero, the FSM calibration transits back to "Basic_Calibrated" state.

# 4.3.6.4

# Calibration example

This example presents a use case to calibrate an FDCAN device (receiver) by an FDCAN host (transmitter). The following flow chart illustrates the steps through the FDCAN device before calibrating.

![](images/dc0f2a54651eb8b84e3020ff63b4a620672d5aaa512c42ffd45c1b46cab9838e.jpg)  
Figure 29. Steps to calibrate a FDCAN device

After the calibration passed successfull, the FDCAN device becomes ready for reception and transmission messages with the new FDCAN host bitrate.

# FDCAN implementation improvements over BxCAN

The below table helpsusers t simpliy he CAN 2.0 protool upgrade  the CAN-D proocol in STM32 devices.   
This table also specifies the improvements on the FDCAN.

The FDCAN offers many advantages over the traditional BxCAN (basic extended CAN), including faster data nv reduced. There is an increase on the number of messages in transmission and reception that requires an improvement of the RAM memory.

Table 9. FDCAN improvements over BxCAN   

<table><tr><td rowspan=1 colspan=2></td><td rowspan=1 colspan=1>Features</td><td rowspan=1 colspan=1>Supported by BxCAN</td><td rowspan=1 colspan=1>Supported by FDCAN</td></tr><tr><td rowspan=3 colspan=2>Compatibility</td><td rowspan=1 colspan=1>Compatibility with BxCAN</td><td rowspan=1 colspan=1>Yes</td><td rowspan=1 colspan=1>Yes</td></tr><tr><td rowspan=1 colspan=1>Compatibility with CAN-FD</td><td rowspan=1 colspan=1>No</td><td rowspan=1 colspan=1>No</td></tr><tr><td rowspan=1 colspan=1>Remote frame</td><td rowspan=1 colspan=1>No</td><td rowspan=1 colspan=1>Supported to become compatiblewith BxCAN</td></tr><tr><td rowspan=2 colspan=2>Frame</td><td rowspan=1 colspan=1>Arbitration bitrate/data rate (in Mbit/s)</td><td rowspan=1 colspan=1>Up to 1 (only bitrate per frame)</td><td rowspan=1 colspan=1>Up to 1/Up to 8</td></tr><tr><td rowspan=1 colspan=1>Data length per frame (in bytes)</td><td rowspan=1 colspan=1>0 to 8</td><td rowspan=1 colspan=1>0 to 64</td></tr><tr><td rowspan=2 colspan=2>RAM</td><td rowspan=1 colspan=1>RAM</td><td rowspan=1 colspan=1>512 bytes</td><td rowspan=1 colspan=1>10 Kbytes</td></tr><tr><td rowspan=1 colspan=1>Accessible RAM</td><td rowspan=1 colspan=1>No</td><td rowspan=1 colspan=1>Yes</td></tr><tr><td rowspan=2 colspan=2>Transmission</td><td rowspan=1 colspan=1>Dedicated Tx buffer/Tx queue/TxFIFO</td><td rowspan=1 colspan=1>No/Yes/YesMaximum three elements can beused as queue or FIFO.</td><td rowspan=1 colspan=1>Yes/Yes/YesMaximum 32 elements: userchooses the transmit mechanism.</td></tr><tr><td rowspan=1 colspan=1>Transmit pause</td><td rowspan=1 colspan=1>No</td><td rowspan=1 colspan=1>Yes</td></tr><tr><td rowspan=1 colspan=2></td><td rowspan=1 colspan=1>Dedicated Rx buffer/Rx FIFO</td><td rowspan=1 colspan=1>No/2Up to three elements in each RxFIFOUp to six elements maximum</td><td rowspan=1 colspan=1>64/2Up to 64 elements in each RxFIFOUp to 192 elements maximum</td></tr><tr><td rowspan=2 colspan=2>Reception</td><td rowspan=1 colspan=1></td><td rowspan=1 colspan=1>Overwrite mode option</td><td rowspan=1 colspan=1>Overwrite the last elementreceived in FIFO</td></tr><tr><td rowspan=1 colspan=1>Improvements acceptance filters</td><td rowspan=1 colspan=1>Classical CAL (Can 2.0)acceptance filters</td><td rowspan=1 colspan=1>Some features are added as:Discards matching filter.Accepts non matchingfilters.</td></tr><tr><td rowspan=3 colspan=2>Other</td><td rowspan=1 colspan=1>Restricted test mode</td><td rowspan=1 colspan=1>No</td><td rowspan=1 colspan=1>Yes</td></tr><tr><td rowspan=1 colspan=1>Transceiver delay compensation</td><td rowspan=1 colspan=1>No</td><td rowspan=1 colspan=1>Yes</td></tr><tr><td rowspan=1 colspan=1>Clock calibration unit</td><td rowspan=1 colspan=1>No</td><td rowspan=1 colspan=1>Yes</td></tr></table>

BxCAN developers can easily migrate to FDCAN given its BxCAN compatibility and as the FDCAN can be implemented without posing a revision f the entie system design.he DAN contains ll xCAN featue an improved matter and meets the requirements for the new applications.

# Revision history

Table 10. Document revision history   

<table><tr><td rowspan=1 colspan=1>Date</td><td rowspan=1 colspan=1>Version</td><td rowspan=1 colspan=1>Changes</td></tr><tr><td rowspan=1 colspan=1>4-Oct-2019</td><td rowspan=1 colspan=1>1</td><td rowspan=1 colspan=1>Initial release.</td></tr><tr><td rowspan=1 colspan=1>21-Feb-2023</td><td rowspan=1 colspan=1>2</td><td rowspan=1 colspan=1>Updated the title of the document.Updated the Table 1. Applicable products.Updated the Section 4: Implementation of CAN-FD in STM32 devices.</td></tr><tr><td rowspan=1 colspan=1>06-Mar-2024</td><td rowspan=1 colspan=1>3</td><td rowspan=1 colspan=1>Updated:Figure 1. Standard CAN-FD frameSection 3.1: Frame architecture comparison between CAN-FD andAN 2.0</td></tr><tr><td rowspan=1 colspan=1>03-Sep-2024</td><td rowspan=1 colspan=1>4</td><td rowspan=1 colspan=1>Document title updated.</td></tr><tr><td rowspan=1 colspan=1>29-Oct-2024</td><td rowspan=1 colspan=1>5</td><td rowspan=1 colspan=1>Updated Table 1. Applicable products.</td></tr></table>

# Contents

# 1 General information

2 CAN-FD protocol overview.

2.1 CAN-FD features.   
2.2 CAN-FD format

# Improvements and benefits of CAN-FD over CAN 2.0.

3.1 Frame architecture comparison between CAN-FD and CAN 2.0 b

# Implementation of CAN-FD in STM32 devices

4.1 FDCAN peripheral main features

1.2 RAM management 8

4.2.1 RAM organization 8   
4.2.2 Multiple FDCAN instances 11

# 1.3 RAM sections. 12

4.3.1 RAM filtering sections . 12   
4.3.2 Reception section 14   
4.3.3 Transmission section 17   
4.3.4 Test modes 23   
4.3.5 Transceiver delay compensation. 26   
4.3.6 Clock calibration on FDCAN 28

# FDCAN implementation improvements over BxCAN. 32

Revision history 33

# List of tables .35

# List of figures. .36

# List of tables

Table 1. Applicable products 1   
Table 2. Payload data length codes (bytes) 6   
Table 3. Main differences between CAN-FD and CAN 2.0 6   
Table 4. "Element" size number depending on data field range. 9   
Table 5. Standard filter element configuration 14   
Table 6. Differences between dedicated Rx buffer and Rx FIFO. 17   
Table 7. Differences between dedicated Tx buffer, Tx FIFO and Tx queue. 21   
Table 8. Differences between mixed Tx buffer + Tx FIFO and mixed Tx buffer + Tx queue configurations 23   
Table 9. FDCAN improvements over BxCAN . 32   
Table 10. Document revision history . 33

# List of figures

Figure 1. Standard CAN-FD frame 3   
Figure 2. Frame architecture of CAN-FD versus CAN 2.0 5   
Figure 3. FDCAN block diagram. 7   
Figure 4. CAN message RAM mapping . 8   
Figure 5. RAM mapping example for and efficient use of the CAN message RAM. 10   
Figure 6. Example of CAN message RAM with multiple FDCAN instances. 11   
Figure 7. CAM message RAM filters section 12   
Figure 8. Global flow chart of acceptance filter . 13   
Figure 9. Rx FIFO section in CAN message RAM . 15   
Figure 10. Simplified operation of Rx FIFO 15   
Figure 11. Rx buffer section on CAN message RAM. 16   
Figure 12. Simplified operation of Rx buffer 17   
Figure 13. Tx event FIFO section in the CAN message RAM 18   
Figure 14. Tx buffer section in CAN message RAM 19   
Figure 15. Transmission with Tx buffer mechanism. 19   
Figure 16. Transmission with Tx FIFO mechanism 20   
Figure 17. Transmission with Tx queue mechanism 21   
Figure 18. Mixed configuration with dedicated Tx buffers and Tx FIFO 22   
Figure 19. Mixed configuration with dedicated Tx buffers and Tx queue. 23   
Figure 20. Pin control in restricted-operation mode 24   
Figure 21. Pin control in bus-monitoring mode 25   
Figure 22. Pin control in external loop-back mode 25   
Figure 23. Pin control in internal loop-back mode 26   
Figure 24. Bit timing. 26   
Figure 25. Loop delay measurement. 27   
Figure 26. SSP position in transmit delay-compensation 27   
Figure 27. Bypass operation of the CCU 28   
Figure 28. Functional state machine calibration 29   
Figure 29. Steps to calibrate a FDCAN device 30

# IMPORTANT NOTICE  READ CAREFULLY

pt old ursant  dits   leole.

purchasers' products.

No license, express or implied, to any intellectual property right is granted by ST herein.

are the property of their respective owners.

I

© 2024 STMicroelectronics - All rights reserved