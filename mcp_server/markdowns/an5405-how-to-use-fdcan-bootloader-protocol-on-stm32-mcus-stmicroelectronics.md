# How to use FDCAN bootloader protocol on STM32 MCUs

# Introduction

plA supported command.

T pl dinyneplio soo2 v.

F refer to the application note AN2606.

Table 1. Applicable products   

<table><tr><td>Type</td><td>Product series</td></tr><tr><td>Microcontrollers</td><td>STM32G0 series STM32G4 series STM32H5 series STM32H7 series STM32L5 series STM32U3 series</td></tr></table>

# Bootloader code sequence

ol abpb   a® or® are referred to as STM32 in this document.   
Figure 1 presents the global sequence for the STM32 bootloader with FDCAN.

![](images/a2e3d286dac265bfcf599394f188d36d0d935ea252f3afe894a9d484dab4921b.jpg)  
Figure 1. Bootloader for STM32 with FDCAN

Depending onthe DCAN protocol version, the frame sent  theDCAN t tart communication is iffeent \* When protocol version is <= 2.1, any frame can be sent \* When protocol version is > 2.1, only this frame is accepted "ID = 11h, data length = 1 and data = 5Ah"

On he systemmemory boot modes entere and he 2 devic conigure referhe applicatin oe AN2606 for additional details), the bootloader code waits for a frame on the FDCANx_Rx pin.

Arm is a registered trademark of Arm Limited (or its subsidiaries) in the US and/or elsewhere.

# 2 FDCAN settings

In this application, the FDCAN settings are:

Frame format: FD mode with Bit Rate Switching   
Mode: Normal mode   
AutoRetransmission: Enabled   
TransmitPause: Disabled   
Standard identifier (not extended)   
Time quantum = Nominal Prescaler × (1 / fdcan_ker_ck) fdcan_ker_ck = 20 MHz Nominal Prescaler = 0x1   
Synchronization Jump Width = 0x10   
Nominal Time Segment1 = 0x3F   
Nominal Time Segment2 = 0x10   
Data Prescaler = 0x1   
Data Sync Jump Width = 0x4   
Data Time Segment1 = 0xF   
Data Time Segment2 = 0x4   
Standard Filters Number = 1   
Extended Filters Number = 0

Filter settings are:

ID Type = 0   
Filter Index = 0   
Filter Type = 2 (classic filter)   
Filter Config = FDCAN_FILTER_TO_RXFIFO0   
Filter ID1 = 0x111   
Filter ID2 = 0x7FF

u gl u ID sent to bootloader is not filtered and the message ID is taken as a command opcode.

Forprotool versins.e fiecongurationshangerderfie Mesages Is betwe 00 FFh:

Filter Type = FDCAN_FILTER_RANGE;   
Filter Config = FDCAN_FILTER_TO_RXFIFO0; Filter ID1 = 0x00   
Filter ID2 = 0xFF

Transmit settings (from the STM32 to the host) are:

Identifier = 0x111   
Id Type = 0   
Frame Type = FDCAN_DATA_FRAME   
Data Length = FDCAN_DLC_BYTES_64   
ErrorStateIndicator = FDCAN_ESI_ACTIVE   
BitRateSwitch = FDCAN_BRS_ON   
FDFormat = FDCAN_FD_CAN   
TxEventFifoControl = FDCAN_NO_TX_EVENTS   
MessageMarker = 0

# Note:

The CAN bootladr firmware supports only one node at a timeThis means that it does not support CAN Network Management.

2Depending on the FDCAN protocol version, the frame acceptance is different:

When protocol version is ≤ 2.1, filters are not enabled, so any MessagelD and FilterlD1 are accepted.   
When protocol version is > 2.1, MessagelD and FilterlD1 must match exactly.

In the boote, nly he 8LB bitsf the messaged I are taken into accontoanyvalue abov is ignored.

# 3 Bootloader command set

Table 2 lists the supported commands, each of them being described in the corresponding subsection.

Table 2. FDCAN bootloader commands   

<table><tr><td rowspan=1 colspan=1>Command</td><td rowspan=1 colspan=1>Commandcode</td><td rowspan=1 colspan=1>Subsection</td><td rowspan=1 colspan=1>Description</td></tr><tr><td rowspan=1 colspan=1>Get(1)</td><td rowspan=1 colspan=1>0x00</td><td rowspan=1 colspan=1>Section 3.1</td><td rowspan=1 colspan=1>Gets the version and allowed commands supported by the currentversion of the protocol.</td></tr><tr><td rowspan=1 colspan=1>Get Version(1)</td><td rowspan=1 colspan=1>0x01</td><td rowspan=1 colspan=1>Section 3.2</td><td rowspan=1 colspan=1>Gets the protocol version and the readout protection status of the flashmemory.</td></tr><tr><td rowspan=1 colspan=1>Get ID(1)</td><td rowspan=1 colspan=1>0x02</td><td rowspan=1 colspan=1>Section 3.3</td><td rowspan=1 colspan=1>Gets the chip ID.</td></tr><tr><td rowspan=1 colspan=1>Read Memory(2)</td><td rowspan=1 colspan=1>0x11</td><td rowspan=1 colspan=1>Section 3.4</td><td rowspan=1 colspan=1>Reads up to 256 bytes of memory starting from an address specified bythe application.</td></tr><tr><td rowspan=1 colspan=1>Go(2)</td><td rowspan=1 colspan=1>0x21</td><td rowspan=1 colspan=1>Section 3.5</td><td rowspan=1 colspan=1>Jumps to user application code located in the internal flash memory orSRAM.</td></tr><tr><td rowspan=1 colspan=1>Write Memory(2)</td><td rowspan=1 colspan=1>0x31</td><td rowspan=1 colspan=1>Section 3.6</td><td rowspan=1 colspan=1>Writes up to 256 bytes of RAM or flash memory starting from anaddress specified by the application.</td></tr><tr><td rowspan=1 colspan=1>Erase Memory(2)</td><td rowspan=1 colspan=1>0x44</td><td rowspan=1 colspan=1>Section 3.7</td><td rowspan=1 colspan=1>Erases from one to all the flash memory sectors.</td></tr><tr><td rowspan=1 colspan=1>Special</td><td rowspan=1 colspan=1>0x50</td><td rowspan=1 colspan=1>Section 3.12</td><td rowspan=1 colspan=1>Generic command that allows the addition of new features dependingon the product constraints without adding a new command for everyfeature needed.</td></tr><tr><td rowspan=1 colspan=1>ExtendedSpecial</td><td rowspan=1 colspan=1>0x51</td><td rowspan=1 colspan=1>Section 3.13</td><td rowspan=1 colspan=1>Generic command that allows the user to send more data compared tothe Special command.</td></tr><tr><td rowspan=1 colspan=1>Write Protect</td><td rowspan=1 colspan=1>0x63</td><td rowspan=1 colspan=1>Section 3.8</td><td rowspan=1 colspan=1>Enables the write protection of some sectors.</td></tr><tr><td rowspan=1 colspan=1>Write Unprotect</td><td rowspan=1 colspan=1>0x73</td><td rowspan=1 colspan=1>Section 3.9</td><td rowspan=1 colspan=1>Disables the write protection of all flash memory sectors.</td></tr><tr><td rowspan=1 colspan=1>ReadoutProtec()</td><td rowspan=1 colspan=1>0x82</td><td rowspan=1 colspan=1>Section 3.10</td><td rowspan=1 colspan=1>Enables readout protection.</td></tr><tr><td rowspan=1 colspan=1>ReadoutUnprotect(1)</td><td rowspan=1 colspan=1>0x92</td><td rowspan=1 colspan=1>Section 3.11</td><td rowspan=1 colspan=1>Disables readout protection.</td></tr></table>

1. Ced and have no effect on the device. Protection depends on product series. Protection is active means

For he T32H5 series Trust zone TZEN) = 0and Product state > Provisining, and HiDeProtectin Level (HDPL = 3

For the other products listed in Table 1. Applicable products: read protection set.

3 prcaahee lt 26 bou ale command.

# Communication safety

Each packet is either accepted (ACK answer) or discarded (NACK answer):

ACK message = 0x79 NACK message = 0x1F

# 3.1 Get command

The Get command allows the host to get the version of the protocol and the supported commands. When the bd eceivshe Ge mananithe rotool versin n heortcancode host.

![](images/e1155dff439f5f19dc514ced5516eec6df148fc0d108514972f9baa768c3e079.jpg)  
Figure 2. Get command (host side)

Based on the host command, the device answers as shown in Figure 3.

![](images/261d71bd38f69e72f6a2a51f3bca00f46fcc0c02a081d79da30d443302288869.jpg)  
Figure 3. Get command (device side)

All data sent from the device on this command are sent using DataLength = 0000h (one byte).

The data are received as per the following order:

1. Number of commands (11)   
2. FDCAN protocol version (0x11)   
3. Get command opcode (0x00)   
4. Get Version command opcode (0x01)   
5. Get ID command opcode (0x02)   
6. Read Memory command opcode (0x11)   
7 Go command opcode (0x21)   
8. Write Memory command opcode (0x31)   
9. Erase Memory command opcode (0x44)   
10. Write Protect command opcode (0x63)   
11. Write Unprotect command opcode (0x73)   
Readout Protect command opcode (0x82)   
13. Readout Unprotect command opcode (0x92)

Some bootloader commands depend on the availability of hardware features on the STM32 product.

From the FDCAN BL version V2.0, the number of commands is not fixed anymore. It can change from one product to another.

Forinstance, ieT3 r eRDhardwa eatue sot available.Tegetcand is  s

1. Number of commands (10)   
2. FDCAN protocol version (0x20)   
3. Get command opcode (0x00)   
4. Get Version command opcode (0x01)   
5. Get ID command opcode (0x02)   
6. Read Memory command opcode (0x11)   
7. Go command opcode (0x21)   
8. Write Memory command opcode (0x31)   
9. Erase Memory command opcode (0x44)   
10. Special command opcode(0x50)   
11. Write Protect command opcode (0x63)   
12. Write Unprotect command opcode (0x73)

# 3.2

# Get Version command

The Get Version command is used to get the protocol version. When the bootloader receives the command it tranmits henormation he host a describein igure version and todumy byteshaving hevale 000).

![](images/0f3c3ec514a6a80dc5c65630d8cf2887c12a5c3d2dba3fc8b56c80e21ad2844b.jpg)  
Figure 4. Get Version command (host side)

The host receives first the protocol version (one byte), and then two dummy bytes equal each to 00h.

![](images/77569d1e088eafe24d8ee9870b4a97576716906aa7a6cb50bf85e6d761596f9d.jpg)  
Figure 5. Get Version command (device side)

# 3.3 Get ID command

The Get ID command is used to get the version of the STM32 product ID (identification). When the bootloader receives the command, it transmits the product ID to the host.

![](images/d41e73d410804b75e0fa70ba1bac0ce276a49e5efca8554df010a8297f967c23.jpg)  
Figure 6. Get ID command (host side)

Teost reeivs he 32 product I two bytes) sent by he devicea hownn igur.he B y is sent first.

![](images/c366195885edfeb11f12a375ba96f5fbeb9409f23542c975db083208dc479bdf.jpg)  
Figure 7. Get ID command (device side)

# 3.4

# Read Memory command

The Read Memory command is used to read data from any valid memory address: RAM, flash memory, and information block (system memory or option byte areas).

Running he Read Memory commands nly possible when theread protecion s ot et and theadress t red from is valid. For this reason, the bootloader software performs the following checks in sequence:

Is the ID of the command correct or not?   
Is the protection disabled or not?   
Is the address to read from valid or not?   
If all checks pass, the Read Memory command proceeds with reading the data, otherwise NACK is sent to the host.   
The bootloader sends the data as 64-byte messages. The host takes only the number of data needed.

Note:

![](images/1b4ef00a4ea58e048568afbe928b05def11a8072ea23b1e836df38b755b273b6.jpg)  
Figure 8. Read Memory command (host side)

Together with the message ID for the Read Memory command (1h), the address, and number of bytes are sent to the device. The message content is as follows:

ID = 0x11, DLC = 0x05   
data[0] = OxXX (MSB of the address)   
data[1] = 0xYY   
data[2] = 0xZZ   
data[3] = OxTT (LSB of the address)   
6data[4] = N (number of bytes to be read minus one; 0 < N ≤ 255)

![](images/c741f6e305c13ca0a6c7a048984399bd26f04f5506fcf3b4c61cd713e072a859.jpg)  
Figure 9. Read Memory command (device side)

Ta n eos tp  ye u f as number of data requested.

# 3.5

# Go command

The Go command is used to execute downloaded code or any other code by branching to an address specified bteppliatiWhehebootreceve he Gocan  trhemesecontal information and passes the following checks:

Is the ID of the command correct? Is the protection disabled? Is the address to jump to valid?

f themessage content is correct, the Go command transmits an ACK message.Otherwise, it transmits a NACK nessage.

After sending an ACK message to the application, the bootloader firmware:

Resets the registers of the peripherals used by the bootloader to their default values Initializes the main stack pointer of the user application Jumps to the memory location programmed in the received "address + 4", which is the address of the application reset handler. For example, if the received address is Ox0800 0000, the bootloader jumps to the memory location programmed at address Ox0800 0004. The host must send the base address where the application to jump to is programmed.   
1. The jump o the aplcatin works n  thesrapliation ts hevecortable correctl  poin h application address.   
2. The valid addresses for the Go command are in RAM or flash memory. All other addresses are considered not valid and are NACK-ed by the device.   
3. Not al addresses in the RAM are considered valid. The application to jump must consider an offset to avoid overlapping with the first RAM memory used by the bootloader firmware.

# Note:

![](images/29e2034b00ac7abeb617dc84c68651da3a2d9ca197ed03c6c4bed737c85c34e1.jpg)  
Figure 10. Go command (host side)

The message content sent to the device, including the Go command ID (21h), is as follows:

1ID = 0x21, DLC = 0x04   
data[0] = OxXX (MSB of the address)   
data[1] = 0xYY   
data[2] = 0xZZ   
data[3] = OxTT (LSB of the address)

![](images/b9552424439ea8022dc12c85ff87c040977f5b6b057c63acdc595fbcbf24baa8.jpg)  
Figure 11. Go command (device side)

# 3.6

# Write Memory commanc

The Write Memory command is used to write data to any valid memory address of the RAM, flash memory, or opton byte area. When the bootloader receives the Write Memory command, it starts only if the message contains valid information and passes the following checks:

Is the ID of the command correct? Is the protection disabled? Is the address to write to valid?

If the message content iscorrect, he Write Memory command transmits an ACK message nd continues hejob.   
Otherwise, it transmits a NACK message and exits the command.

Fen ruse inopportunely in this area.

When the address is valid, the bootloader:

Receives the user data (N bytes). This means that the device receives N/64 messages, each message being composed of 64 data bytes.   
Programs the user data into the memory starting from the received address   
Transmits the ACK message at theend of the command if the writeoperation was successful. Otherwise, i transmits a NACK message to the application and aborts the command.

# Note:

The maximum length of the block to be written for the STM32 is 256 bytes.

2No error is returned when performing write operations on write protected sectors.

![](images/0a041d0b797a05d0d2e48d062908521cc2c976b0ba7b8ec93c04265e83bb2f3f.jpg)  
Figure 12. Write Memory command (host side)

Teher with he message ID or he Wrie Memory command (h), he address, nd number  bytes  snt to the device. The message content is as follows:

ID = 0x31, DLC = 0x05   
data[0] = OxXX (MSB of the address)   
3. data[1] = 0xYY   
4. data[2] = 0xZZ   
data[3] = OxTT (LSB of the address)   
data[4] = N (number of bytes to be written minus one; 0 < N ≤ 255) The host sends N / 64 messages.

![](images/e15fdacf37af15a81462366f9fb71db44025f8b3462df81218b099bd41e92294.jpg)  
Figure 13. Write Memory command (device side)

# 3.7

# Erase Memory command

The Erase Memory command allows the host to erase flash memory pages. When the bootloader receives the Erase Memory command and the protection is disabled, it transmits the ACK message to the host.

Aerheranissin theACKmesge hebootrheckshest two bytedateceiv nn MSB forat an construct vale alageNumber, which controls heexecutionherase Memory coman as follows:

PageNumber = OxFFFF: mass erase is requested PageNumber = OxFFFE: Bank1 erase is requested (if supported) PageNumber = OxFFFD: Bank2 erase is requested (if supported) Otherwise, PageNumber represents the number of pages to erase

If te PageNumbervalueindicates mass or bank erasing, an ACK message s sent upon completion.Otherwise the botloader starts erasing the memory pages as defined by the host, and then sends an ACK message wher all the requested pages are erased.

# Erase Memory command specifications

The bootloader receives one message that contains N, the number of pages to be erased. The bootloader receives N bytes, every two bytes containing the page number to be erased

# Note:

The ACK message sent after the erase operation only indicates that the command is finished. It des not guarantee that the erase operation has succeeded. 2No error is returned when performing erase operations on write-protected sectors.

![](images/e3d20014f9a7af4ee8b5b7ee248dfa1017ad8f63262510e6903404ba9696d0dd.jpg)  
Figure 14. Erase Memory command (host side)

The PageNumber value sent from the host is MSB first:

PageNumber = (data[0] << 8) | (data[1])   
Page numbers sent for erasing are sent on a 64-byte frame format,  which only PageNumber is read by   
the bootloader (the padding bytes in the 64-byte frame are not read)

![](images/0438f88713c56974dfee6293d1e6088c5d7c4e55bea0cfde390b8a4a67d8d357.jpg)  
Figure 15. Erase Memory command (device side)

# 3.8

# Write Protect command

T Wrro n  able wr on  m eo Wh boooader receives the WriProtect command it transmit ACK message o the host  the protectnis disabled. Otherwise, it transmits a NACK message.

A nissi AC y e ooer waicivhe ash mey crco application.

At the end of the Write Protect command, the bootloader transmits the ACK message.

# Note:

I a second Write Protect command is executed, the flash memory sectors protected by the first command become unprotected, and only the sectors passed within the second Write Protect command become protected. The total number of sectors and the sector numbers to be protected are not checked. This means that no error is returned when a command is passed with a wrong number of sectors to be protected, or a wrong sector number.

![](images/951af20e6ec038e20853959ad1941c06e667d7e6613218f53a0b9cdaf1df117a.jpg)  
Figure 16. Write Protect command (host side)

T cor cods none yenbe ecors n hecde  n together with can ID of the Write Protect command.

![](images/c1dbf301ee3ae6defd3ab46dc74c7d64f46457ddb35760f4024b1f7434b40f34.jpg)  
Figure 17. Write Protect command (device side)

# Write Unprotect command

TheWrinprotect omand issed diablehe wri protection l he fash memory scors.Whe the boceivheWriprocand transit ACKmesgeheoshe rote diableOtherwise ittransit  NACKmessageAfer the ransmissionf theACK message, theboot disables the write protection of all the flash memory sectors.

![](images/5c114e10af62ac2ab6a4c41f8d728c1ff02102658ba52edf9afc4d9191f9dcb1.jpg)  
Figure 18. Write Unprotect command (host side)

![](images/8bed35680cc652ef9639a4c8d718829eaf60a3626f436428bce4b68276891645.jpg)  
Figure 19. Write Unprotect command (device side)

# 3.10

# Readout Protect command

The Readout Protect command is used to enable the flash memory readout protection. When the bootloader vheou roan an CesgehosRDiablhe transmits a NACK message. After the transmission of the ACK message, the bootloader enables the readout protection of the flash memory.

![](images/5e3fd05ce155ef760ddd56beeca48aa4eba46b6245494239ffd4e3d90d118126.jpg)  
Figure 20. Readout Protect command (host side)

![](images/ad8e534c1f00c7b28a57d99e25026445501b773992e2f430dd3027d1fbb3a5fe.jpg)  
Figure 21. Readout Protect command (device side)

# 3.11

# Readout Unprotect command

The Readout Unprotect command is used to disable the fash memory readout protection. When the bootloader iveadou nproan anmitCeagehesanissio ACK message, the bootloader deactivates the RDP.

![](images/ed9a25b60bf7262f393f645ccfa0effa2cd1ad7ff36743516950993568399f66.jpg)  
Figure 22. Readout Unprotect command (host side)

![](images/0c83b5632b06f3fe7c8616d59341a4fe55708ba5df3705692ebb53b4eb7445ef.jpg)  
Figure 23. Readout Unprotect command (device side)

# 3.12 Special command

Many new bootloader commands are needed to support new features and fulfillusers requirements for new aplications. o avoid having new speciicommans or every project, he gene Specl comand is at to cover new command requests.

![](images/373a04da66be5c7223e4aedb30e92a4f894ddc4cb07ec056f5a79fe96a0a5145.jpg)  
Figure 24. Special command (host side)

![](images/7c0b59ded53a999b1bd8c04698cbbb90b3affb821bbede29a51c28dd0b13f372.jpg)  
Figure 25. Special command (device side)

When the bootloader receives the Special command, it transmits the ACK byte to the host.Once theACK is traitted, the bootoader waitor a subcomanocode two bytes,  first) and a checksum byte. I e suan ppor y he2 bootlrn hcksu corhe bootn ACK byte, otherwise it transmits a NACK byte and aborts the command.

To keep the Special command generic, the data packet received by the bootloader can have different sizes depending on the subcommand needs.

Therefore, the packet is split in two parts:

Size of the data (2 bytes, MSB first)   
N bytes of data If N = 0, no data is transmitted N must be less than 128

I all condtins are satisfid (N ≤ 8 and checksumOK), the bootloaer transmits n ACK byt.Otherwi transmits a NACK byte and aborts the command.

Oebaneecusingheecei at he boot en spshat consi consecutive packets:

• Data packet Size of the data (2 bytes, MSB first) N bytes of data 0 If N = 0, no data is transmitted   
• Status packet Size of the status data (2 bytes, MSB first) N bytes of data 0 If N = 0, no status data is transmitted

Finally, an ACK byte closes the Special command interaction between the bootloader and the host.

# 3.13

# Extended Special command

The Extende pecalcoand isderiv romhepeci cand, wit  slghtly ifferent behavior. Iow theuse moea withenw bu yu anu as a response.

![](images/0e460e2e9f76a2584ea1075cf9fc35d329e0aa3fdca018733a0be4a77f723583.jpg)  
Figure 26. Extended Special command (host side)

![](images/5fedf17c78264a707405eee1c448aa7810192b08ae12043493cab5b149ffb4eb.jpg)  
Figure 27. Extended Special command (device side)

When the bootloader receives the Extended Special command, t transmits the ACK byte to the host. Once the ACK isransited, hebootloader waiora subcmadce wo byes, MB st) and achecksum e. I hec an ACK byte. Otherwise, it transmits a NACK byte and aborts the command.

Two packets can then be received depending on the subcommand needs:

Packet1 Data1 packet, where the number of bytes is limited to 128 bytes   
Packet2 Data2 packet, where the number of bytes is limited to 1024 bytes

If all conditions are satisfied for packe1 first (N ≤ 128 and checksum OK) and then for packet2 (N ≤ 1024 and checksum OK), the bootloader transmits an ACK byte. Otherwise, it transmits a NACK byte and aborts the command.

Oc he sbcan eecsingheeceiv dat hebootae en espos hat cnsist packet:

Size of the data (2 bytes, MSB first) N bytes of data If N = 0, no data is transmitted

Finally, an ACK byte closes the Extended Special command interaction between the bootloader and the host.

# 1 Bootloader protocol version evolution

# Table 3 lists the bootloader versions.

Table 3. Bootloader protocol versions   

<table><tr><td rowspan=1 colspan=1>Date</td><td rowspan=1 colspan=1>Revision</td><td rowspan=1 colspan=1>Changes</td></tr><tr><td rowspan=1 colspan=1>16-Aug-2018</td><td rowspan=1 colspan=1>V1.0</td><td rowspan=1 colspan=1>Initial version</td></tr><tr><td rowspan=1 colspan=1>27-Feb-2021</td><td rowspan=1 colspan=1>V1.1</td><td rowspan=1 colspan=1>Added support for extended special commands</td></tr><tr><td rowspan=1 colspan=1>24-Feb-2023</td><td rowspan=1 colspan=1>V2.0</td><td rowspan=1 colspan=1>The number of commands can vary from device to device with thesame protocol version v2.0. To know the supported commands, usethe Get command.</td></tr><tr><td rowspan=1 colspan=1>15-Mar-2024</td><td rowspan=1 colspan=1>V2.1</td><td rowspan=1 colspan=1>Add check on the received command opcode to not exceed one bytemax value. Otherwise, a NACK is sent to the host.</td></tr><tr><td rowspan=1 colspan=1>15-Feb-2024</td><td rowspan=1 colspan=1>V2.2</td><td rowspan=1 colspan=1>Limit detection frame to &quot;ID = 111h, data length =1 and data=5Ah&quot;Enable global filters rejection</td></tr></table>

# Revision history

Table 4. Document revision history   

<table><tr><td rowspan=1 colspan=1>Date</td><td rowspan=1 colspan=1>Revision</td><td rowspan=1 colspan=1>Changes</td></tr><tr><td rowspan=1 colspan=1>14-Nov-2019</td><td rowspan=1 colspan=1>1</td><td rowspan=1 colspan=1>Initial release.</td></tr><tr><td rowspan=1 colspan=1>28-Jun-2021</td><td rowspan=1 colspan=1>2</td><td rowspan=1 colspan=1>Extended the range of applicable products to the STM32G0 Series andSTM32G4 Series.Added Section 3.12 Special command and Section 3.13 Extended Specialcommand.</td></tr><tr><td rowspan=1 colspan=1>09-Feb-2022</td><td rowspan=1 colspan=1>3</td><td rowspan=1 colspan=1>Extended the range of applicable products to the STM32U5 series.</td></tr><tr><td rowspan=1 colspan=1>14-Feb-2023</td><td rowspan=1 colspan=1>4</td><td rowspan=1 colspan=1>Extended the range of applicable products to the STM32H5 series (updatedTable 1. Applicable products and Section 1: Bootloader code sequence)Replaced &quot;bootloader version&quot; with &quot;protocol version&quot; throughout thedocumentUpdated note 1 to Table 2. FDCAN bootloader commandsUpdated information below Figure 3. Get command (device side)Replaced &quot;readout protection&quot; or RDP with &quot;protection&quot; in Section 3.4: ReadMemory command to Section 3.9: Write Unprotect commandAdded Section 4: Bootloader protocol version evolution</td></tr><tr><td rowspan=1 colspan=1>02-Nov-2023</td><td rowspan=1 colspan=1>5</td><td rowspan=1 colspan=1>Updated:Document title.Table 2. FDCAN bootloader commands.Erase Memory command specifications</td></tr><tr><td rowspan=1 colspan=1>07-Mar-2024</td><td rowspan=1 colspan=1>6</td><td rowspan=1 colspan=1>Updated: Table 3. Bootloader protocol versions</td></tr><tr><td rowspan=1 colspan=1>22-May-2025</td><td rowspan=1 colspan=1>7</td><td rowspan=1 colspan=1>Updated Table 1. Applicable products.Updated Figure 1. Bootloader for STM32 with FDCAN.Updated Section 2: FDCAN settings.Updated Figure 8. Read Memory command (host side) and Figure 9. ReadMemory command (device side).</td></tr></table>

# Contents

# 1 Bootloader code sequence

2 FDCAN settings 3

# Bootloader command set 5

3.1 Get command 6   
3.2 Get Version command 9   
3.3 Get ID command. 10   
3.4 Read Memory command 11   
3.5 Go command . 13   
3.6 Write Memory command 14   
3.7 Erase Memory command . .16   
3.8 Write Protect command . .19   
3.9 Write Unprotect command . .20   
3.10 Readout Protect command .21   
3.11 Readout Unprotect command 22   
3.12 Special command 24   
3.13 Extended Special command 27

# Bootloader protocol version evolution 30

Revision history .31

# .ist of tables .33

_ist of figures.. 34

# List of tables

Table 1. Applicable products Table 2. FDCAN bootloader commands 5 Table 3. Bootloader protocol versions. 30 Table 4. Document revision history . 31

# List of figures

Figure 1. Bootloader for STM32 with FDCAN. 2   
Figure 2. Get command (host side). 6   
Figure 3. Get command (device side) 7   
Figure 4. Get Version command (host side) 9   
Figure 5. Get Version command (device side) 9   
Figure 6. Get ID command (host side). 10   
Figure 7. Get ID command (device side) 10   
Figure 8. Read Memory command (host side) 11   
Figure 9. Read Memory command (device side). 12   
Figure 10. Go command (host side) 13   
Figure 11. Go command (device side). 14   
Figure 12. Write Memory command (host side) 15   
Figure 13. Write Memory command (device side) . 16   
Figure 14. Erase Memory command (host side). 17   
Figure 15. Erase Memory command (device side) 18   
Figure 16. Write Protect command (host side) 19   
Figure 17. Write Protect command (device side). 20   
Figure 18. Write Unprotect command (host side) 20   
Figure 19. Write Unprotect command (device side). 21   
Figure 20. Readout Protect command (host side). 21   
Figure 21. Readout Protect command (device side) 22   
Figure 22. Readout Unprotect command (host side). 22   
Figure 23. Readout Unprotect command (device side) 23   
Figure 24. Special command (host side) 24   
Figure 25. Special command (device side) 25   
Figure 26. Extended Special command (host side). 27   
Figure 27. Extended Special command (device side) 28

# IMPORTANT NOTICE  READ CAREFULLY

pt old ursant  dits   leole.

purchasers' products.

No license, express or implied, to any intellectual property right is granted by ST herein.

are the property of their respective owners.

I

© 2025 STMicroelectronics - All rights reserved