# I3C protocol used in the STM32 bootloader

# Introduction

o supported command.

pl T throughout the document.

F mentioned AN2606.

Table 1. Applicable products   

<table><tr><td>Type</td><td>Product series</td></tr><tr><td rowspan="3">Microcontrollers</td><td>STM32H5</td></tr><tr><td>STM32H7</td></tr><tr><td>STM32U3</td></tr></table>

# Bootloader code sequence

The I3C bootloader code sequence for STM32 microcontrollers, based on Arm®(a) core(s), is shown in Figure 1. Bootloader detection (device side).

Note:

Arm is a registered trademark of Arm Limited (or its subsidiaries) in the US and/or elsewhere.

![](images/866e4029651aba4e5e91e66d99ef69f1a90794c89cbd6a80f449f0004dc84c4d.jpg)  
Figure 1. Bootloader detection (device side)

![](images/0a325dce4df63872e17831f5bc354d78c4bb9b00d77294c653cf56b86fbbb0b5.jpg)  
Figure 2. Bootloader detection (host side)

Once the system memory boot mode is entered and the STM32 device has been configured (for more details refer oAN2606), he I3C IP conigured byhe booadertens on the I3CSDA pin  detec any cotroll activity on the bus. When the BL detects a controller broadcast and HW negotiation is established (dynamic as sied heLC, eBL wa   noatnby x owhat hecontol targetng  commnicatin withe bootlader Whedetected e 3C bootladerfware begi receivihost commands.

# 2 I3C settings

# 2.1

# Target (bootloader) settings

The BL initialization configures I3C as follows:

Mode: Target mode   
Aval timing: 0x4E   
DMA Req RX: Disabled   
DMA Req TX: Disabled   
Status FIFO: Disabled   
DMA Req status: Disabled   
DMA Req control: Disabled   
IBI: Enabled   
Additional data after IBI acknowledged: 1 byte   
IBI configuration: Mandatory Data Byte (MDB)   
MIPI instance ID: OxB (B stands for Bootloader)   
Device characteristics: 0x2   
All IT disabled except RXFNE (Receive FIFO Interrupt)   
The RXFNE interruption is disabled after SYNC byte detection by the bootloader.

# 2.2 Controller (host) settings

The host initialization configures I3C as follows:

Mode: Controller mode Clocks waive form: Ox00262726 (1 Mega)

Note: It is possible to reach 12.5 Mega by modifying this configuration to (0x00550908) but this depends on the HW quality and configuration. Other baudrates are also possible. 1 Mega here is an example.

Bus characteristics: 0x0011004E

DMA Req RX: Disabled

DMA Req TX: Disabled

Status FIFO: Disabled

DMA Req status: Disabled

DMA Req control: Disabled

IBI: Enabled

Additional data after IBI acknowledged: 1 byte

IBI configuration: Mandatory Data Byte (MDB)

Message type: Private message (using dynamic address chosen)

Send method

Data Generate Stop condition after sending a message ACK/NACK: IBI used

All IT disabled

# 3 Bootloader command set

The supported commands are listed in Table 2. I3C bootloader commands and described in this section.

Table 2. I3C bootloader commands   

<table><tr><td rowspan=1 colspan=1>Command</td><td rowspan=1 colspan=1>Command code</td><td rowspan=1 colspan=1>Command description</td></tr><tr><td rowspan=1 colspan=1>Get</td><td rowspan=1 colspan=1>0x00</td><td rowspan=1 colspan=1>Gets the version and the allowed commands supported by the current version of theprotocol</td></tr><tr><td rowspan=1 colspan=1>Get Version</td><td rowspan=1 colspan=1>0x01</td><td rowspan=1 colspan=1>Gets the bootloader version</td></tr><tr><td rowspan=1 colspan=1>Get ID</td><td rowspan=1 colspan=1>0x02</td><td rowspan=1 colspan=1>Gets the chip ID</td></tr><tr><td rowspan=1 colspan=1>Read Memory</td><td rowspan=1 colspan=1>0x11</td><td rowspan=1 colspan=1>Reads up to 2048 bytes of memory starting from an address specified by theapplication</td></tr><tr><td rowspan=1 colspan=1>Go</td><td rowspan=1 colspan=1>0x21</td><td rowspan=1 colspan=1>Jumps to user application code located in the internal flash memory or in SRAM</td></tr><tr><td rowspan=1 colspan=1>Write Memory</td><td rowspan=1 colspan=1>0x31</td><td rowspan=1 colspan=1>Writes up to 2048 bytes to the RAM or flash memory starting from an addressspecified by the application</td></tr><tr><td rowspan=1 colspan=1>Erase</td><td rowspan=1 colspan=1>0x44</td><td rowspan=1 colspan=1>Erases from one to all the flash memory sectors</td></tr><tr><td rowspan=1 colspan=1>Special</td><td rowspan=1 colspan=1>0x50</td><td rowspan=1 colspan=1>Generic command that allows adding new features depending on the productconstraints, without adding a new command for every feature</td></tr><tr><td rowspan=1 colspan=1>Extended Special</td><td rowspan=1 colspan=1>0x51</td><td rowspan=1 colspan=1>Generic command that allows the user to send more data compared to the Specialcommand</td></tr><tr><td rowspan=1 colspan=1>Write Protect</td><td rowspan=1 colspan=1>0x63</td><td rowspan=1 colspan=1>Enables the write protection for some sectors</td></tr><tr><td rowspan=1 colspan=1>Write Unprotect</td><td rowspan=1 colspan=1>0x73</td><td rowspan=1 colspan=1>Disables the write protection for allflash memory sectors</td></tr><tr><td rowspan=1 colspan=1>Readout Protect</td><td rowspan=1 colspan=1>0x82</td><td rowspan=1 colspan=1>Enables the read protection</td></tr><tr><td rowspan=1 colspan=1>Readout Unprotect</td><td rowspan=1 colspan=1>0x92</td><td rowspan=1 colspan=1>Disables the read protection</td></tr></table>

# Note:

Depending on the project some commands can be omitted. The Get command is adapted to give only the commands that are used.

# Communication safety

Each packet is either accepted (ACK answer) or discarded (NACK answer):

ACK message = 0x79 NACK message = 0x1F

# 3.1 Get command

The Get comman allows he host  get the version  the I3C protocol and thesupporte commands. When the bder eceives he Ge coantransmitshe C protoo verson andheupportcoman ce the host.

![](images/6bc072986232d177863b89d0b44d42f16ea20aaf2f6cbdeeffc16e41f503c073.jpg)  
Figure 3. Get command (host side)

Based on the host command, the device answers the following:

![](images/32025322c45445c93d3c23d9c6c502705bbe05b6ef5b37d3cae03f20ec0d3cc4.jpg)  
Figure 4. Get command (device side)

The data is received on the following order:

Byte 1: ACK   
Byte 2: N = 10 = Number of commands   
3. Byte 3: I3C protocol version 0x10 = Version 1.0   
4. Byte 4: Ox00 - Get command   
5. Byte 5: Ox01 - Get version   
6. Byte 6: 0x02 - Get ID   
7. Byte 7: 0x11 - Read Memory command   
8. Byte 8: 0x21 - Go command   
9.Byte 9: 0x31 - Write Memory command   
10. Byte 10: Ox44 - Erase command   
11. Byte 11: Ox50 - Special command   
12. Byte 12: Ox63 - Write Protect command   
13. Byte 13: 0x73 - Write Unprotect command   
14. Byte 14: ACK   
This is an example as the number of commands an

# 3.2 Get version command

The Get version command is used oget the I3C protocol version. When he bootlader receives he comman transmits one byte with protocol version to the host.

![](images/6cad5072a102fc88173409cff3ccb129f2068102951604a52be436533c42440d.jpg)  
Figure 5. Get version command (host side)

The STM32 sends the bytes as follows:

Byte 1: ACK   
Byte 2: Bootloader version (0 < Version < 255) (for example, Ox10 = Version 1.0)   
Byte 3: ACK

![](images/f03f0480beef919ec899d7491a7685e56d9aa3c60bddf646fafb55eb2328e1a8.jpg)  
Figure 6. Get version command (device side)

# 3.3

# Get ID command

The Get ID coans used o get he ersinf the hip ID dentiatin). When he bootlader eceivs he command, it transmits the product ID to the host.

![](images/2521620b7743184441ff23431c782718ee0171d3394dcc2770408ebd0f9be79e.jpg)  
Figure 7. Get ID command (host side)

The STM32 device sends the bytes as follows:

Byte 1: ACK   
Byte 2: Number of bytes to send (Fixed = 0x2)   
Bytes 3-4: PID (product ID) Byte 3 = MSB Byte 4 = LSB   
Byte 5: ACK

![](images/a30a89e38af72ca752dd59bb0cc5ea04a63484fbd4581fbc6bc48137f6b7b73c.jpg)  
Figure 8. Get ID command (device side)

# 3.4

# Read memory command

The Read memory command is used to read data from any valid memory address:RAM, flash memory and in the inormation blocks (ystem memory o option byteareas). Read memory is nly possible when o protection is set and when the address to read is valid.

The bootloader SW then individually checks if:

The ID of the command is correct or not

The protection is disabled or enabled (protection status depends on the product architecture)

IotvalhetACve ACKanthen waivheesdfm nesuACKisines is valid, and its checksum is ok. If not, NACK is sent, and the command is terminated.

After the ACK, the bootloader waits to receive the data size to be written and its checksum.

If the checksum is not OK, size received is null, with a size exceeding 2048 or the readable valid area, NACK is sent and the Read memory command is terminated

If ll the conditns above are correct, the BL calculates thenumber f bytes to read and  a "L" is requested to read more or not.

Data size and checksum are received on 3 Bytes (data[0], data[1], data[2])

Bit number - |15|14|13|12|11|10|9|8|7|6|5|4|3|2|1| 0 Content data[0] data[1] Content N =(2x number of bytes) |loopl

Loop = 1 means that there is still data to send to the host.   
o BL waits to receive the new chunk size and its checksum and repeats the above operation.   
Loop = 0 means that this is the last chunk of data to read.

Note:

The maximum length of the block that can be read for the STM32 is 2048 bytes.

To read more than 2048 bytes, it is not necessary to send the command multiple times. Use the "Loop" feature described above instead.

![](images/c17eecddaa40f0787ac4a080e6a23268b93113a42a0ebe9c75b73541f1af3728.jpg)  
Figure 9. Read memory (host side)

The host sends bytes to the STM32 as follows:

Bytes 1-2: 0x11 + 0xEE

Wait for ACK or NACK

Bytes 3-6: Start address (byte 3: MSB, byte 6: LSB)

Byte 7: Checksum: XOR (byte 3, byte 4, byte 5, byte 6)

Wait for ACK or NACK

Bytes 8-9: The number of bytes to be read (2 bytes 8: MSB, byte 9: LSB)

N = (Byte[8] << 8) | Byte[9]) Loop = N & 0x1 number of bytes = (N >> 1)

Byte 10: Checksum: XOR (byte 8, byte 9)

Wait for ACK or NACK

9Byte 11...number of bytes: Data received from the device

10. If loop = 1 go to "6."

Note:

Receiving a NACK terminates the command.

![](images/4462c72ec04761ce4087106950552d6bd7c2ba5324760325ffc2ddc1c98e677f.jpg)  
Figure 10. Read memory (device side)

# 3.5

# Go command

The Go command is used to execute the downloaded code or any other code by branching to an address tWh following valid information:

Opcode of the command is correct or not Protection is disabled or enabled

Vote: - Note that the protection depends on the product (RDP, HDPL..)

Address to jump is valid or not

If the message content is correct, it transmits an ACK message, otherwise it transmits a NACK message.

After sending an ACK message to the application, the bootloader firmware:

• Resets the registers of the peripherals used by the bootloader to their default values

Initializes the user application's main stack pointer

Jumps to the memory location programmed in the received 'address + 4' "Address +4": address of the application's reset handler. For example, if the received address is Ox0800 0000, the bootloader jumps to the memory location programmed at address Ox0800 0004. The host should send the base address where the application to jump to is programmed.

# Note:

The Ju heplatn worknheplatn hevetalec  pin application address.

The valid addresses for the Go command are in RAM or flash memory. All other addresses are considered not valid and are NACK-ed by the device.

Not alladdresses in the RAM are considered as valid, application to jump to must consider an offset to avoid overlapping with the first RAM memory used by the bootloader firmware.

![](images/4526f7a9bbc2295d603803bf668a9ebb9c51b1f33a2fa350cd6706008bb50238.jpg)  
Figure 11. Go command (host side)

The host sends bytes to the STM32 as follows:

Byte 1: 0x21   
Byte 2: OxDE   
Wait for ACK or NACK   
4. Byte 3 to byte 6: start address   
5Byte 7: checksum: XOR (byte 3, byte 4, byte 5, byte 6)   
Wait for ACK or NACK

![](images/3a9af1d6639c8c931976b13384340ee7f901d25a2e6ecbe2d26e3726a4185f36.jpg)  
Figure 12. Go command (device side)

# 3.6

# Write memory command

The Write memory command is used to write data to any valid memory address of RAM, Flash OTP, or Option yrWheeotiseWrieoan rheola valid:

Opcode of the command and its checksum are correct Protection is disabled

IotalACve ACK wavruCi valid, and its checksum is ok. If not, NACK is be sent, and command terminated.

# Note:

For the Option byte area, only the base address of the Option byte area is accepted to avoid writing inopportunely in this area.

After the ACK, the bootloader waits to receive the data size to be written and its checksum

If the checksum is not OK, size received is null, with a size exceeding 2048 or the readable valid area, NACK is sent and the Write memory command is terminated

Ill ecnd bove e corre e Bcalclates eb y  wri nd Lp" is requested to write more or not.

Data size and checksum are received on 3 Bytes (data[0], data[1], data[2])

Bit number- |15|14|13|12|11|10|9|8|7|6|5|4|3|2|1| 0 Content data[0] data[1] Content N = (2x number of bytes) |loop|

Loop = 1 means that there are still data to retrieve from the host o BL waits to receive the new chunk size and its checksum and repeats the above operation _oop = 0 means that this is the last chunk of data to write

After each write operation, ACK is sent to the host.

In summary, the host sends the data to the BL as follows:

Byte 1: 0x31

Byte 2: OxCE

Wait for ACK (if NACK received, command is terminated)

Byte 3 to byte 6: Start address Byte 3: MSB Byte 6: LSB

Byte 7: Checksum: XOR (byte 3, byte 4, byte 5, byte 6)

Wait for ACK (if NACK received, command is terminated)

7Bytes 8-9: The number of bytes to be read (2 bytes 8: MSB, byte 9: LSB) N = (Byte[8] << 8) | Byte[9]) Loop = N & 0x1 number of bytes = (N >> 1)

Byte 10: Checksum byte: XOR (Byte8, byte 9)

Wait for ACK (if NACK received, command is terminated)

. Byte 11 to Byte (N): data to write and its Xor If the Xor is ok, BL writes the data

11. Wait for ACK (if NACK received, command is terminated)

If not last chunk (Loop = 1), go to "7" If last chunk (Loop = 0), command is terminated

Note:

The maximum length of the block that can be written for the STM32 is 2048 bytes. To write more than 2048 bytes, t is not necessary to send the command multiple times. Use the "Loop" feature described above instead. No error is returned when performing write operations on write protected sectors.

![](images/27cddc38d0ba19d37fa038ca3016f14bd6ec6bebc6fcdbf36f56f76c8d164ac6.jpg)  
Figure 13. Write memory command (host side)

![](images/cb46c56bb42fed8be103564318f7538d977a687d1a44204286ae84fb9595d463.jpg)  
Figure 14. Write memory command (device side)

# 3.7

# Erase memory command

The Erase memory command allows the host to erase flash memory pages. When the bootloader receives the Erase memory command and the protection is disabled, it transmits the ACK message to the host.

After the transmission of the ACK message, the bootloader checks the first 2 bytes data received on a MSB forat and constructs the ageNumber" Depending on thevaluef the ageNumber", the requir erase operation is executed:

PageNumber = OxFFFF: Mass erase is requested   
PageNumber = OxFFFE: Bank1 erase is requested (if supported)   
PageNumber = OxFFFD: Bank2 erase is requested (if supported)   
PageNumber: if diferent from the above values, it represents the number of pages to erase

If the PageNumber represents Mass or Bank erase, and once pages erase is complete, it sends an ACK mesage.Otherie, the bootader starts the memory page) erase s defind by the host, and after pges erase it sends an ACK message.

As every PageNumber is represented on 2 bytes (MSB first), the Bytes number is (BytesNumber = 2x PageNumber)

When erasing different pages, the bootloader receives (BytesNumber + Xor byte)

PageNumber (each on 2 bytes) Xor byte for all Pages

# Note:

ACK message sent after the erase operation indicates that the required command is finished, but it does not guarantee that the erase operation has succeeded.

No error is returned when performing erase operations on write protected sectors.

![](images/f825c9ca1610c3edbdb7d8d448dc9a391f52a963c6fd3a5786bbb6a08539dcfb.jpg)  
Figure 15. Erase memory command (host side)

The host sends bytes to the STM32 as follows:

# Mass/Bank Erase

Byte 1: 0x44   
Byte 2: OxBB   
3. Wait for ACK or NACK   
4. Bytes 3-4: Special erase (0xFFFx)   
5. Bytes 5: Checksum of Bytes 3-4   
Wait for ACK or NACK   
Pages Erase   
Byte 1: 0x44   
Byte 2: OxBB   
Wait for ACK or NACK

Bytes 3-4: PageNumber (Represents the number of pages to erase)

Byte 3: MSB Byte 4: LSB

Bytes 5: Checksum of Bytes 3-4

Wait for ACK or NACK

7Bytes 6 to N - 1 (N = 2x PageNumber + 1) 2x PageNumber; as every page number is represented on 2 bytes (MSB first) +1"; Checksum for all byte 6 to (N - 1)

Wait for ACK or NACK

Example of I3C frame:

erase page 3

Ox44 OxBB Wait ACK Ox00 Ox01 OxFE Wait ACK Ox00 Ox03 OxFC Wait ACK

erase page 1 and page 2:

Ox44 OxBB Wait ACK Ox00 Ox02 OxFD Wait ACK Ox00 Ox01 Ox00 Ox02 OxFC Wait ACK

![](images/f7691dd299ab2237e08b5bac74f8d9e77681d32602fca775ce178bde510ee84e.jpg)  
Figure 16. Erase memory command (device side)

# 3.8

# Write protect command

TWr pocan ablehe r poen  m meory cWh e bivWonCes else it transmits NACK.

AhesCheaic application. At the end of the Write protect command, the bootloader transmits the ACK message.

# Note:

The toalnube  cors and he ecorumber eprote eot heck thseans hat o retuned when a command is passed with a wrong number f sectors t be protectedor a wrong secor numbe.

![](images/c03cc351a3b4bd0b2c1de53afd09fddca0b49314954e90fe9ccee4c6a4059c80.jpg)  
Figure 17. Write protect memory command (host side)   
Figure 18. Write protect memory command (device side)

Every sector number is sent on 2 bytes.

![](images/fdb059fd8583bdb6e1ac6374d1f23b2afcb5e24a2206602b3107439401814366.jpg)

# 3.9

# Write unprotect command

ThWrieprotec cansisable he wri protectonl heash meory ecorWh e beiv heWrproan aniACesgeheoshe prote isale e tranmt NACAterhetrnissin thACKmesge h ootderisables r protection of all the flash memory sectors.

![](images/950d29fa6a2dc21b02328b7413e7fd6fa9b43cf24c8c8f7f102cc7c264f89c9c.jpg)  
Figure 19. Write unprotect memory command (host side)

![](images/04256d28825348806f62b1cd2908881be0bf3eb3abb8d2166b890d33f948a186.jpg)  
Figure 20. Write unprotect memory command (device side)

# 3.10

# Read protect command

The Read protect command is used to enable the fash memory read protection. When the bootloader receives theRed prot omandansmits heACKesageheos RDPisisabled s transmits NACK. Ater the transmission  the ACK message, the bootladernables he read protecion or the flash memory.

Note

Note:

RDP feature isn't present on allthe STM32 devices. In this case, the Read protect command is omitted

![](images/3254c30d38d5b47efe582d222daf03a32ae5ea5ae16cb2965408fc126b0725bc.jpg)  
Figure 21. Read protect memory command (host side)

![](images/553cf9e0ac9e2950c5b89648d65c106ddff8b5f411abcc21fcb1025726ec90dd.jpg)  
Figure 22. Read protect memory command (device side)

# 3.11

# Read unprotect command

The Readprotec commanuse iablehefashmemory read protecon When he bootlader reives the Readunprotect command, it transmits the ACK message to the host. After the transmissionof the ACK message, the bootloader deactivates the RDP.

![](images/de419cc74e4c947f22a23a8d20c86fe1444452e9e80319319b51432a4e860b8e.jpg)  
Figure 23. Read unprotect memory command (host side)

![](images/3b86165fd6f328ba42632cef22d8f04760e05be863233ab8be34c5cb9c5faf89.jpg)  
Figure 24. Read unprotect memory command (device side)

# 3.12 Special command

New bootloader commands are needed to support new STM32 features and to fulfil customer needs. To avoid specfic commands for a single project, the Special command has been created to be as generic as possible.

![](images/4a7b2b719763f00e22bc3cadea6aaa22fdc97bbba8221e3e961cdaa3b37c0778.jpg)  
Figure 25. Special command (host side)

![](images/8eebb37afecd2637152867595a0646c49d06433dbe2f753479f0f96802e5a9cb.jpg)  
Figure 26. Special command (device side)

When the bootloader receives the Special command, it transmits the ACK byte to the host. Once the ACK is trit the bootrwai r sub-cacoewobyts)an  checksuy Ie sub-commans supported byhe T32 bootloader nd t checksuis correct, he bootloadertransi ACK byte, otherwise it transmits a NACK byte and aborts the command.

To keep hecangeneric,he dat packt receied bthe booladran have ifferent ze depenig the sub-command needs. Therefore, the packet is split in two parts:

Size of the data (2 bytes, MSB first)   
N bytes of data If N = 0, no data is transmitted N must be lower than 128

Ilcta ati  8 chesiorr he erin ACK.Oh transmits a NACK byte and aborts the command. Once the sub-command is executed using the received data, the bootloader sends a response consisting of two consecutive packets:

Data packet

Size of the data (2 bytes, MSB first) N bytes of data If N = 0, no data is transmitted

Status packet

Size of the status data (2 bytes, MSB first) N bytes of data If N = 0, no status data is transmitted

An ACK byte closes the Special command interaction between bootloader and the host

# 3.13 Extended Special command

This command is slightlydifferent from the Special command. It allows the user to send more data with the addition of a new buffer of 1024 bytes and, as a response, it only returns the status of the command.

![](images/c1277d8b73e08b2d770821b36113d14af4a99d17a1f4e9fbb8737770a5ff1326.jpg)  
Figure 27. Extended Special command (host side)

![](images/088538295c2f31750e519c02cafb075b09e68354c4e1397762d8ad4388686631.jpg)  
Figure 28. Extended Special command (device side)

When the bootloader receives theExtended Special command, t transmits the ACK byte to the host. Once the ACtransitehe botloaer waior a subcmacoewobyes, B st) and achecksum ye. I  ub-r byhe booanhecksorheoot an ACK byte, otherwise it transmits a NACK byte and aborts the command.

The two packets then can be received depending on the subcommand needs:

Packet1: Data1 packet, where number of bytes is limited to 128 bytes.

Packet2: Data2 packet, where number of bytes is limited to 1024 bytes.

If all conditions are satisfied (Packet1: N ≤ 128 and checksum is correct, Packet2: N ≤ 1024 and checksum is correct), the bootloader transmits an ACK, otherwise it transmits a NACK byte and aborts the command.

Onc the u-coan  execteusing he receivd data, the bootoader sends a esponsconsisting packet:

Size of the data (2 bytes, MSB first) N bytes of data If N = 0, no data are transmitted

An ACK byte closes the Extended Special command interaction between bootloader and the host.

# Revision history

Table 3. Document revision history   

<table><tr><td rowspan=1 colspan=1>Date</td><td rowspan=1 colspan=1>Version</td><td rowspan=1 colspan=1>Changes</td></tr><tr><td rowspan=1 colspan=1>22-Feb-2023</td><td rowspan=1 colspan=1>1</td><td rowspan=1 colspan=1>Initial release.</td></tr><tr><td rowspan=1 colspan=1>26-Feb-2024</td><td rowspan=1 colspan=1>2</td><td rowspan=1 colspan=1>Updated Product series in Section Introduction to add STM32H7.</td></tr><tr><td rowspan=1 colspan=1>06-Feb-2025</td><td rowspan=1 colspan=1>3</td><td rowspan=1 colspan=1>Updated Product series in Section Introduction to add STM32U3.</td></tr></table>

# Contents

# 1 Bootloader code sequence

# 2 I3C settings 4

2.1 Target (bootloader) settings   
2.2 Controller (host) settings

# Bootloader command set

3.1 Get command 5   
3.2 Get version command.   
3.3 Get ID command . .8   
3.4 Read memory command 10   
3.5 Go command. .14   
3.6 Write memory command .15   
3.7 Erase memory command . .19   
3.8 Write protect command 23   
3.9 Write unprotect command .24   
3.10 Read protect command . . .25   
3.11 Read unprotect command .27   
3.12 Special command 27   
3.13 Extended Special command 30

# Revision history 34

# List of figures

#

Figure 1. Bootloader detection (device side) 2   
Figure 2. Bootloader detection (host side) 3   
Figure 3. Get command (host side) 6   
Figure 4. Get command (device side) 7   
Figure 5. Get version command (host side) 8   
Figure 6. Get version command (device side) 8   
Figure 7. Get ID command (host side) 9   
Figure 8. Get ID command (device side) . 10   
Figure 9. Read memory (host side) 11   
Figure 10. Read memory (device side) 13   
Figure 11. Go command (host side) 14   
Figure 12. Go command (device side). 15   
Figure 13. Write memory command (host side) 17   
Figure 14. Write memory command (device side). 18   
Figure 15. Erase memory command (host side). 20   
Figure 16. Erase memory command (device side) 22   
Figure 17. Write protect memory command (host side) 23   
Figure 18. Write protect memory command (device side) 23   
Figure 19. Write unprotect memory command (host side) 25   
Figure 20. Write unprotect memory command (device side). 25   
Figure 21. Read protect memory command (host side) . 26   
Figure 22. Read protect memory command (device side) 26   
Figure 23. Read unprotect memory command (host side) 27   
Figure 24. Read unprotect memory command (device side). 27   
Figure 25. Special command (host side) 28   
Figure 26. Special command (device side) 29   
Figure 27. Extended Special command (host side) 31   
Figure 28. Extended Special command (device side) 32

# List of tables

Table 1. Applicable products Table 2. I3C bootloader commands 5 Table 3. Document revision history . 34

# IMPORTANT NOTICE  READ CAREFULLY

pt old ursant  dits   leole.

purchasers' products.

No license, express or implied, to any intellectual property right is granted by ST herein.

are the property of their respective owners.

I

© 2025 STMicroelectronics - All rights reserved