# USART protocol used in the STM32 bootloader

# Introduction

This application note describes the USART protocol used in the STM32 microcontroller bootloader, providing details on each supported command.

This document applies to STM32 products embedding any bootloader version, as specified in AN2606 STM32 system memory boot mode, available on www.st.com. These products are listed in Table 1, and are referred to as STM32 throughout the document.

For more information about the USART hardware resources and requirements for your device bootloader, refer to the already mentioned AN2606.

Table 1. Applicable products   

<table><tr><td rowspan=1 colspan=1>Type</td><td rowspan=1 colspan=1>Product series or line</td></tr><tr><td rowspan=20 colspan=1>Microcontrollers</td><td rowspan=1 colspan=1>STM32C0 seriesSTM32F0 seriesSTM32F1 seriesSTM32F2 series</td></tr><tr><td rowspan=1 colspan=1>STM32F3 series</td></tr><tr><td rowspan=1 colspan=1>STM32F4 series</td></tr><tr><td rowspan=1 colspan=1>STM32F7 series</td></tr><tr><td rowspan=1 colspan=1>STM32G0 series</td></tr><tr><td rowspan=1 colspan=1>STM32G4 series</td></tr><tr><td rowspan=1 colspan=1>STM32H5 series</td></tr><tr><td rowspan=1 colspan=1>STM32H7 series</td></tr><tr><td rowspan=1 colspan=1>STM32L0 series</td></tr><tr><td rowspan=1 colspan=1>STM32L1 series</td></tr><tr><td rowspan=1 colspan=1>STM32L4 series</td></tr><tr><td rowspan=1 colspan=1></td></tr><tr><td rowspan=1 colspan=1>STM32U0 series</td></tr><tr><td rowspan=1 colspan=1>STM32U3 series</td></tr><tr><td rowspan=1 colspan=1>STM32U5 series</td></tr><tr><td rowspan=1 colspan=1>STM32WB series</td></tr><tr><td rowspan=1 colspan=1>STM32WBA series</td></tr><tr><td rowspan=1 colspan=1>STM32WB0 series</td></tr><tr><td rowspan=1 colspan=1>STM32WL3x line</td></tr><tr><td rowspan=1 colspan=1>STM32WL5x/Ex lines</td></tr></table>

# Contents

# USART bootloader code sequence ... ..5

# Choosing the USARTx baud rate . . . . .6

2.1 Minimum baud rate . . 6   
2.2 Maximum baud rate 6

# Bootloader command set . . 7

3.1 Get command 9   
3.2 Get Version command 12   
3.3 Get ID command 14   
3.4 Read Memory command 15   
3.5 Go command 18   
3.6 Write Memory command 20   
3.7 Erase Memory command 23   
3.8 Extended Erase Memory command 26   
3.9 Write Protect command 29   
3.10 Write Unprotect command 32   
3.11 Readout Protect command 33   
3.12 Readout Unprotect command 35   
3.13 Get Checksum command 37   
3.14 Special command 41   
3.15 Extended Special command . 43

# Bootloader protocol version evolution . . . . . . 47

Revision history 48

# List of tables

Table 1. Applicable products 1   
Table 2. USART bootloader commands 7   
Table 3. Bootloader protocol versions 47   
Table 4. Document revision history 48

# List of figures

Figure 1. Bootloader for STM32 with USART 5   
Figure 2. Get command: host side. . 9   
Figure 3. Get command: device side . 10   
Figure 4. Get Version command: host side 12   
Figure 5. Get Version command: device side 13   
Figure 6. Get ID command: host side 14   
Figure 7. Get ID command: device side. 15   
Figure 8. Read Memory command: host side 16   
Figure 9. Read Memory command: device side 17   
Figure 10. Go command: host side . 18   
Figure 11. Go command: device side 19   
Figure 12. Write Memory command: host side 21   
Figure 13. Write Memory command: device side. 22   
Figure 14. Erase Memory command: host side . 24   
Figure 15. Erase Memory command: device side 25   
Figure 16. Extended Erase Memory command: host side . 27   
Figure 17. Extended Erase Memory command: device side . 28   
Figure 18. Write Protect command: host side . 30   
Figure 19. Write Protect command: device side 31   
Figure 20. Write Unprotect command: host side 32   
Figure 21. Write Unprotect command: device side 33   
Figure 22. Readout Protect command: host side. 34   
Figure 23. Readout Protect command: device side . 34   
Figure 24. Readout Unprotect command: host side 35   
Figure 25. Readout Unprotect command: device side. 36   
Figure 26. Get Checksum command: host side . . 39   
Figure 27. Get Checksum command: device side . 40   
Figure 28. Special command: host side. 41   
Figure 29. Special command: device side . 42   
Figure 30. Extended Special command: host side. 44   
Figure 31. Extended Special command: device side. 45

1

# USART bootloader code sequence

![](images/209ff771154bb9a5525fb0b19e3a2690695b1d3ded8fb3415d7892c46223505b.jpg)  
Figure 1. Bootloader for STM32 with USART

Once the system memory boot mode is entered and the STM32 microcontroller (based on A e ui begins to scan the USARTx_RX line pin, waiting to receive the Ox7F data frame: a start bit, 0x7F data bits, even parity bit(b), and a stop bit.

Depending upon the implementation, the baud rate detection is based on the HW (IP supporting auto baud rate), or on the SW. The following paragraphs explain the SW detection mode.

The duration of the data frame is measured using the Systick timer. The count value of the timer is used to calculate the corresponding baud rate factor respect to the current system clock. Then, the code initializes the serial interface accordingly. Using this calculated baud rate, an acknowledge byte (0x79) is returned to the host, who signals that the STM32 is ready to receive commands.

# 2 Choosing the USARTx baud rate

The calculation of the serial baud rate for USARTx, from the length of the first received byte, is used to operate the bootloader within a wide range of baud rates. However, the upper and lower limits must be kept to ensure proper data transfer.

For a correct data transfer from the host to the microcontroller, the maximum deviation between the internal initialized baud rate for USARTx and the real baud rate of the host must be below 2.5%. The deviation (fb, in percent) between the host baud rate and the microcontroller baud rate can be calculated using the formula below:

![](images/540e722c6708c109cb506b4760bcbfddc343eca5f78d9a08449dd3ab1f48acbf.jpg)

This baud rate deviation is a nonlinear function, depending upon the CPU clock and the baud rate of the host. The maximum of the function (fb) increases with the host baud rate. This is due to the smaller baud rate prescaler factors, and the implied higher quantization error.

# 2.1 Minimum baud rate

The lowest tested baud rate (BLow) is 1200. Baud rates below this value cause SysTick timer overflow. In this event, USARTx is not correctly initialized.

# 2.2 Maximum baud rate

BHigh is the highest baud rate for which the deviation does not exceed the limit. All baud rates between BLow and BHigh are below the deviation limit.

The highest tested baud rate (BHigh) is 115200.

# 3 Bootloader command set

The supported commands are listed in Table 2, all of them are described in this section.

Table 2. USART bootloader commands   

<table><tr><td rowspan=1 colspan=1>Command(1)</td><td rowspan=1 colspan=1>Code</td><td rowspan=1 colspan=1>Description</td></tr><tr><td rowspan=1 colspan=1>Get(2)</td><td rowspan=1 colspan=1>0x00</td><td rowspan=1 colspan=1>Gets the version and the alowed commands supported by the current versnothe protocol.</td></tr><tr><td rowspan=1 colspan=1>Get Version(2)</td><td rowspan=1 colspan=1>0x01</td><td rowspan=1 colspan=1>Gets the protocol version.</td></tr><tr><td rowspan=1 colspan=1>Get ID(2)</td><td rowspan=1 colspan=1>0x02</td><td rowspan=1 colspan=1>Gets the chip ID.</td></tr><tr><td rowspan=1 colspan=1>Read Memory(3)</td><td rowspan=1 colspan=1>0x11</td><td rowspan=1 colspan=1>Reads up to 256 bytes of memory starting from an address specified by theapplication.</td></tr><tr><td rowspan=1 colspan=1>Go(3)</td><td rowspan=1 colspan=1>0x21</td><td rowspan=1 colspan=1>Jumps to user application code located in the internal flash memory or in theSRAM.</td></tr><tr><td rowspan=1 colspan=1>Write Memory(3)</td><td rowspan=1 colspan=1>0x31</td><td rowspan=1 colspan=1>Writes up to 256 bytes to the RAM or flash memory starting from an addressspecified by the application.</td></tr><tr><td rowspan=1 colspan=1>Erase(3)(4)</td><td rowspan=1 colspan=1>0x43</td><td rowspan=1 colspan=1>Erases from one to all the flash memory pages.</td></tr><tr><td rowspan=1 colspan=1>Extended Erase(3)(4)(5)</td><td rowspan=1 colspan=1>0x44</td><td rowspan=1 colspan=1>Erases from one to all the flash memory pages using two-byte addressing mode(available only for USART bootloader v3.0 and higher).</td></tr><tr><td rowspan=1 colspan=1>Specia(5)</td><td rowspan=1 colspan=1>0x50</td><td rowspan=1 colspan=1>Generic command that allows to add new features depending on the productconstraints, without adding a new command for every feature.</td></tr><tr><td rowspan=1 colspan=1>Extended Special(5)</td><td rowspan=1 colspan=1>0x51</td><td rowspan=1 colspan=1>Generic command that allows the user to send more data compared to theSpecial command.</td></tr><tr><td rowspan=1 colspan=1>Write Protect(5)</td><td rowspan=1 colspan=1>0x63</td><td rowspan=1 colspan=1>Enables the write protection for some sectors.</td></tr><tr><td rowspan=1 colspan=1>Write Unprotect(5)</td><td rowspan=1 colspan=1>0x73</td><td rowspan=1 colspan=1>Disables the write protection for all flash memory sectors.</td></tr><tr><td rowspan=1 colspan=1>Readout Protect</td><td rowspan=1 colspan=1>0x82</td><td rowspan=1 colspan=1>Enables the read protection.</td></tr><tr><td rowspan=1 colspan=1>Readout Unprotect(2)</td><td rowspan=1 colspan=1>0x92</td><td rowspan=1 colspan=1>Disables the read protection.</td></tr><tr><td rowspan=1 colspan=1>Get Checksum(5)</td><td rowspan=1 colspan=1>0xA1</td><td rowspan=1 colspan=1>Computes a CRC value on a given memory area with a size multiple of 4 bytes.</td></tr></table>

and goes back to command checking. C the device. The protection depends upon the product. 3. Refer to STM32 product datasheets and to AN2606 to know the valid memory areas for these commands. 0x Erase command, but not both. 5. Not supported on STM32WB0 series.

# Protection

The protection used on the bootloader SW depends upon the MCU and its requirements.

Protection active means:

for the STM32H5 series: TrustZone® (TZEN) = 0 and Product state > Provisioning and HiDeProtection Level(HDPL) = 3 • for the other products listed in Table 1: Read protection set

# Communication safety

The communication from the programming tool (PC) to the device is verified by:

1. checksum: received blocks of data bytes are XOR-ed. A byte containing the computed XOR of all previous bytes is added to the end of each communication (checksum byte). By XOR-ing all received bytes (data plus checksum), the result at the end of the packet must be 0x00.

2. for each command, the host sends a byte and its complement (XOR = 0x00)

UART: parity check active (even parity)(a)

Each packet is either accepted (ACK answer), or discarded (NACK answer):

• ACK = 0x79 • NACK = 0x1F

# 3.1 Get command

This command allows the user to get the protocol version and the supported commands. When the bootloader receives the command, it transmits the protocol version and the supported command codes to the host, as shown in Figure 2.

![](images/b1838d48a5462f274a1c703225c7c368704a76faf30da574dd2bebeaf9c6abb7.jpg)  
Figure 2. Get command: host side

![](images/c93095d88c57106013223e4527352eecd8a3b2b05f22c6bc3697a6611d8c5f95.jpg)  
Figure 3. Get command: device side

The STM32 sends the bytes as follows:

Byte 1: ACK   
Byte 2: N = 11 = the number of bytes to follow - 1, except current and ACKs   
Byte 3: Protocol version (0 < version < 255), example: 0x10 = version 1.0   
Byte 4: 0x00 Get command   
Byte 5: 0x01 Get Version command   
Byte 6: 0x02 Get ID command   
Byte 7: 0x11 Read Memory command   
Byte 8: 0x21 Go command   
Byte 9: 0x31 Write Memory command   
Byte 10: 0x43 or 0x44 Erase command or Extended Erase command (exclusive commands)   
Byte 11: 0x63 Write Protect command   
Byte 12: 0x73 Write Unprotect command   
Byte 13: 0x82 Readout Protect command

Byte 14: 0x92 Readout Unprotect command Byte 15: 0xA1 Get Checksum command (only for version V3.3)

Commands depend upon the HW features. Beginning from the USART BL version V4.0, the number of commands is no more fixed, and can change from one product to the other.

As an example, for the STM32H5 series there is no RDP HW feature. The scheme is:

Byte 1: ACK  
Byte 2: N = 10 = the number of bytes to follow - 1, except current and ACKs  
Byte 3: Protocol version 0x40 = v4.0  
Byte 4: 0x00 Get command  
Byte 5: 0x01 Get Version command  
Byte 6: 0x02 Get ID command  
Byte 7: 0x11 Read Memory command  
Byte 8: 0x21 Go command  
Byte 9: 0x31 Write Memory command  
Byte 10: 0x44 Extended Erase command  
Byte 11: 0x50 Special command  
Byte 12: 0x63 Write Protect command  
Byte 13: 0x73 Write command

# 3.2 Get Version command

This command is used to get the protocol version. After receiving the command, the bootloader transmits the version and two bytes (for legacy compatibility, both bytes are 0).

![](images/2b642a18b10ac758751a58bf26f86059339b4c585121147a0d15b234368461b1.jpg)  
Figure 4. Get Version command: host side

![](images/5acacb589af33c459dadaf433cf2b98a0d4d5dc41ab61194219e80e53afe8535.jpg)  
Figure 5. Get Version command: device side

GV = Get Version.

The STM32 sends the bytes as follows:

Byte 1: ACK   
Byte 2: Protocol version (0 < version ≤255), example: 0x10 = version 1.0   
Byte 3: Option byte 1: Ox00 to keep the compatibility with generic bootloader protocol   
By 4:Option byte : Ox00 to keep the compatibility with generic bootloader protool   
Byte 5: ACK

# 3.3 Get ID command

This command is used to get the version of the chip ID (identification). When the bootloader receives the command, it transmits the product ID to the host.

The STM32 device sends the bytes as follows:

Byte 1: ACK   
Byte 2: N = the number of bytes - 1 (N = 1 for STM32), except for current byte and ACKs   
Bytes 3-4: PID(1) byte 3 = 0x04, byte 4 = 0xXX

Byte 5: ACK

PID stands for product ID. Byte 1 and 2 are, respectively, the MSB and the LSB of the ID.

![](images/ac293aa4431a69275af7b478b11040ced251ec177ac157677ee6347062370bdc.jpg)  
Figure 6. Get ID command: host side

![](images/6bc3d7a53769608f22e54c2cdfc673130e44b800e1984397373636489031e10d.jpg)  
Figure 7. Get ID command: device side   
GID = Get ID.

# 3.4 Read Memory command

This command is used to read data from any valid memory address (refer to the product datasheets and to AN2606 for more details) in RAM, flash memory, and in the information block (system memory or option byte areas).

When the bootloader receives the command, it transmits the ACK byte to the application. After the transmission of the ACK byte, the bootloader waits for an address (four bytes, byte 1 is the address MSB and byte 4 is the LSB) and a checksum byte, then it checks the received address. If the address is valid and the checksum is correct, the bootloader transmits an ACK byte, otherwise it transmits an NACK byte, and aborts the command.

When the address is valid and the checksum is correct, the bootloader waits for the number of bytes to be transmitted - 1 (N bytes) and for its complemented byte (checksum). If the checksum is correct, it transmits the needed data (N + 1) bytes) to the application, starting from the received address. If the checksum is not correct, it sends an NACK before aborting the command.

The host sends bytes to the STM32 as follows:

Bytes 1-2: 0x11 + 0xEE   
Wait for ACK   
Bytes 3 to 6 Start address byte 3: MSB, byte 6: LSB   
Byte 7: Checksum: XOR (byte 3, byte 4, byte 5, byte Wait for ACK   
Byte 8: The number of bytes to be read - 1 (0 < N ≤255); Byte 9: Checksum: XOR byte 8 (complement of byte 8)

![](images/25fc0dcb216b66ffdf784dde81e6905ff5c320cb345ea79198345e54c44a7e66.jpg)  
Figure 8. Read Memory command: host side

# Note:

Some products can return two NACKs instead of one when Read protection (RDP) is active (or Read protection level 1 is active). To know if a given product returns one or two NACKs, refer to the known limitations section relative to that product in AN2606.

![](images/2f21a0d3842dfdea6e49ba4dd1e0d988a003f52649d27546da4d120de7b9c8d0.jpg)  
Figure 9. Read Memory command: device side

# 3.5 Go command

This command is used to execute the downloaded code or any other code by branching to an address specified by the application. When the bootloader receives the command, it transmits the ACK byte to the application. After the transmission of the ACK byte, the bootloader waits for an address (four bytes, byte 1 is the address MSB and byte 4 is LSB) and a checksum byte, then it checks the received address. If the address is valid and the checksum is correct, the bootloader transmits an ACK byte, otherwise it transmits an NACK byte, and aborts the command.

When the address is valid and the checksum is correct, the bootloader firmware:

initializes the registers of the peripherals used by the bootloader to their default reset values   
initializes the main stack pointer of the user application   
jumps to the memory location programmed in the received address + 4 (corresponding to the address of the application reset handler). For example, if the received address is 0x0800 0000, the bootloader jumps to the memory location programmed at address 0x0800 0004.   
In general, the host must send the base address where the application to jump to is programmed.

![](images/276d66a2a38d777d21c8dcd00ab988d040cf3068ae8c704e08e892be0d4a181b.jpg)  
Figure 10. Go command: host side

# Note:

Valid addresses for the Go command are in RAM or flash memory (refer to STM32 product datasheets and to AN2606 for more details about the valid memory addresses for the used device). All other addresses are considered not valid and are NACK-ed by the device.

When an application is loaded into RAM and then a jump is made to it, the program must be configured to run with an offset to avoid overlapping with the first area used by the bootloader firmware (refer to STM32 product datasheets and to AN2606 for more details about the RAM offset for the used device).

The Jump to the application works only if the user application sets the vector table correctly to point to the application address.

Some products can return two NACKs instead of one when Read protection (RDP) is active (or Read protection level 1 is active). To know if a given product returns one or two NACKs, refer to the known limitations section relative to that product in AN2606.

![](images/23f44e3dd94c6054aad48bb2dcd7f4abb0d132e404052b31474377b1477868a3.jpg)  
Figure 11. Go command: device side

The host sends bytes to the STM32 as follows:

Byte 1: 0x21   
Byte 2: 0xDE   
Wait for ACK   
Bytes 3 to 6: Start address (byte 3: MSB, byte 6: LSB)   
Byte 7: Checksum: XOR (byte 3, byte 4, byte 5, byte 6)

# 3.6 Write Memory command

This command is used to write data to any valid memory address (see note below), such as RAM, flash memory, or option byte area.

When the bootloader receives the command, it transmits the ACK byte to the application. After the transmission of the ACK byte, the bootloader waits for an address (four bytes, byte 1 is the address MSB and byte 4 is the LSB) and a checksum byte, it then checks the received address. For the option byte area, the start address must be the base address of the option byte area (see note below) to avoid writing inopportunely in this area.

If the received address is valid and the checksum is correct, the bootloader transmits an ACK byte, otherwise it transmits an NACK byte, and aborts the command. When the address is valid and the checksum is correct, the bootloader

C gets a byte, N, which contains the number of data bytes to be received receives the user data ((N + 1) bytes) and the checksum (XOR of N and of all data bytes   
• programs the user data to memory starting from the received address at the end of the command, if the write operation was successful, the bootloader transmits the ACK byte; otherwise it transmits an NACK byte to the application and aborts the command.

The maximum length of the block to be written for the STM32 is 256 bytes.

If the Write Memory command is issued to the option byte area, all bytes are erased before writing the new values, and at the end of the command the bootloader generates a system reset to take into account the new configuration of the option bytes.

# Note:

When writing to the RAM, do not overlap the first area used by the bootloader firmware.

No error is returned when performing write operations on write-protected sectors. No error is returned when the start address is invalid.

![](images/44eb170bf7198523c4d32144987483aea12cb8b49d9a1e7a9830d144446c6a8b.jpg)  
Figure 12. Write Memory command: host side

WM = Write Memory.   
2N+1 must be a multiple of 4.

# Note:

Some products can return two NACKs instead of one when Read protection (RDP) is active (or Read protection level 1 is active). To know if a given product returns one or two NACKs, refer to the known limitations section relative to that product in AN2606.

![](images/9ca6ea212faaf52fc0ccc256842fc8baba15a24615096d6d19d0f5b4e22f2b62.jpg)  
Figure 13. Write Memory command: device side   
WM = Write Memory. N+1 must be a multiple of 4. 3. System reset is called only for some STM32 BL_ (STM32F0/F2/F4/F7) and some STM32L4 (STM32L412xx/422xx, STM32L43xxx/44xxx, STM32L45xxx/46xxx) products.

The host sends the bytes to the STM32 as follows:   
Byte 1: 0x31   
Byte 2: 0xCE   
Wait for ACK   
Bytes 3 to 6: Start address (byte 3: MSB, byte 6: LSB)   
Byte 7: Checksum: XOR (byte3, byte4, byte5, byte6)   
Wait for ACK   
Byte 8: Number of bytes to be received (0 < N ≤255)   
N +1 data bytes: Max 256 bytes   
Checksum byte: XOR (N, N+1 data byes)

# 3.7 Erase Memory command

This command allows the host to erase flash memory pages. When the bootloader receives the command, it transmits the ACK byte to the host. After the transmission of the ACK byte, the bootloader receives one byte (number of pages to be erased), the flash memory page codes, and a checksum byte. If the checksum is correct, the bootloader erases the memory and sends an ACK byte to the host, otherwise it sends an NACK byte to the host, and the command is aborted.

Erase Memory command specifications:

1. The bootloader receives a byte that contains N, the number of pages to be erased - 1. N = 255 is reserved for global erase requests. For 0 <N ≤254, N + 1 pages are erased.   
2. The bootloader receives (N + 1) bytes, each byte containing a page number.

Note:

No error is returned when performing erase operations on write-protected sectors.

![](images/f46a5cd33bc59a01fc80a69d94b0172fac9291eed2c8edfa7c0f0c4c9c670fff.jpg)  
Figure 14. Erase Memory command: host side

![](images/0d33bf6d7a7ed3ba482648d7a3ea9aee7181b5e1a5a2fcca5d0893170fc4c296.jpg)  
Figure 15. Erase Memory command: device side

# Note:

After sending the command and its checksum, if the host sends OxFF followed by data different from Ox00, the mass erase is not performed, and an ACK is sent by the device.

The host sends bytes to the STM32 as follows:

Byte 1: 0x43

Byte 2: OxBC

Wait for ACK

Bye 3: 0xFF or number of pages to be erased - 1 (0 ≤N ≤maximum number of pages)

Byte 4: Ox00 (in case of global erase) or (N + 1 bytes (page numbers) and then checksum XOR (N, N+1 bytes))

# 3.8 Extended Erase Memory command

This command allows the host to erase flash memory pages using two bytes addressing mode. When the bootloader receives the command, it transmits the ACK byte to the host. After the transmission of the ACK byte, the bootloader receives two bytes (number of pages to be erased), the flash memory page codes (each one coded on two bytes, MSB first) and a checksum byte (XOR of the sent bytes); if the checksum is correct, the bootloader erases the memory and sends an ACK byte to the host. Otherwise, it sends an NACK byte to the host, and the command is aborted.

Extended Erase Memory command specifications:

The bootloader receives one half-word (two bytes) that contains N, the number of pages to be erased:

a)For N = OxFFFY (where Y is from 0 to F) special erase is performed: - OxFFFF for global mass erase - OxFFFE for bank 1 mass erase - 0xFFFD for bank 2 mass erase - Codes from OxFFFC to OxFFF0 are reserved

For other values, where 0 ≤N < maximum number of pages: N + 1 pages are erased.

2The bootloader receives:

a) In the case of a special erase, one byte: checksum of the previous bytes: - Ox00 for OxFFFF - 0x01 for OxFFFE - 0x02 for OxFFFD

a) In the case of N+1 page erase, the bootloader receives (2 x (N + 1)) bytes, each half-word containing a page number (coded on two bytes, MSB first). Then all previous byte checksums (in one byte).

Note:

No error is returned when performing erase operations on write-protected sectors.   
The maximum number of pages is relative to the product and must be respected.

![](images/5047c269d7a97c1f541fc87cb84dd0e675389ffdb64585ff6aeec5e8f754167b.jpg)  
Figure 16. Extended Erase Memory command: host side   
EER = Extended Erase Memory.

![](images/70eee94879169a99abe8cc238d67ecbf299e761f193aaa11e9c52b45f803beeb.jpg)  
Figure 17. Extended Erase Memory command: device side

The host sends the bytes to the STM32 as follows:

Byte 1: 0x44 Byte 2: 0xBB Wait for ACK

Bytes 3-4: Special erase (0xFFFF, OxFFFE, or OxFFFD) or Number of pages to be erased (N+1 where 0 ≤ N < Maximum number of pages).   
Remaining Checksum of bytes 3-4 in case of special erase (0x00 if OxFFFF or Ox01 if   
bytes: 0xFFFE, or Ox02 if OxFFFD) or (2 x (N + 1)) bytes (page numbers coded on two bytes MSB first) and then the checksum for bytes 3-4 and all the following bytes

# 3.9 Write Protect command

This command is used to enable the write protection for some or all flash memory sectors. When the bootloader receives the command, it transmits the ACK byte to the host. After the transmission of the ACK byte, the bootloader waits for the number of bytes to be received (sectors to be protected), and then receives the flash memory sector codes from the application.

At the end of the command, the bootloader transmits the ACK byte, and generates a system reset to take into account the new configuration of the option byte.

# Note:

Refer to STM32 product datasheets and to AN2606 for more details about the sector size for the used device.

The Write Protect command sequence is as follows:

the bootloader receives one byte that contains N, the number of sectors to be write-protected - 1 (0 ≤ N ≤ 255) the bootloader receives (N + 1) bytes, each byte contains a sector code

# Note:

The total number of sectors and the sector number to be protected are not checked, this means that no error is returned when a command is passed with a wrong number of sectors to be protected or a wrong sector number.

If a second Write Protect command is executed, the flash memory sectors protected by the first command become unprotected, and only the sectors passed within the second Write Protect command become protected.

![](images/9030d8beded45d3cb5111926a40b2e6e61936bfcabe1bc0b969236260e63b902.jpg)  
Figure 18. Write Protect command: host side

![](images/03c745d41f027f116e57aa17ee8d1503c6d814861a5d1bc22f9df8c8639eba36.jpg)  
Figure 19. Write Protect command: device side   
WP = Write Protect. 2System reset is called only for some STM32 BL (STM32F0/F2/F4/F7) and some STM32L4 (STM32L412xx/422xx, STM32L43xxx/44xxx, STM32L45xxx/46xxx) products.

# 3.10 Write Unprotect command

This command is used to disable the write protection of all the flash memory sectors. When the bootloader receives the command, it transmits the ACK byte to the host. After the transmission of the ACK byte, the bootloader disables the write protection of all the flash memory sectors. After the unprotection operation, the bootloader transmits the ACK byte.

At the end of the Write Unprotect command, the bootloader transmits the ACK byte, and generates a system reset to take into account the new configuration of the option byte.

![](images/e6cb523c1246837544f7e6b2e5d81343bd30ffe25cfce2143b9299abf14f3493.jpg)  
Figure 20. Write Unprotect command: host side

![](images/161c76531c5e7e46a14f27f401e9ab5ff0b0b61406c208c24e6172bb87d22425.jpg)  
Figure 21. Write Unprotect command: device side

WPUN = Write Unprotect.

2. System reset is called only for some STM32 BL_ (STM32F0/F2/F4/F7) and some STM32L4 (STM32L412xx/422xx, STM32L43xxx/44xxx, STM32L45xxx/46xxx) products.

# 3.11 Readout Protect command

This command is used to enable the flash memory read protection. When the bootloader receives the command, it transmits the ACK byte to the host. After the transmission of the ACK byte, the bootloader enables the read protection for the flash memory.

At the end of the Readout Protect command, the bootloader transmits the ACK byte and generates a system reset to take into account the new configuration of the option byte.

![](images/b26a1f8c9e153ddbdebae61ce602f154f8d77c5aec1633e89335671261355891.jpg)  
Figure 22. Readout Protect command: host side

ai14649

RDP_PRM = Readout Protect.

![](images/f961db37190bd9b2cb264f25bb83ccdceea2709c0d40730c4aab9360c82f190e.jpg)  
Figure 23. Readout Protect command: device side

1RDP_PRM = Readout Protect. 2System reset is called only for some STM32 BL (STM32F0/F2/F4/F7) and some STM32L4 (STM32L412xx/422xx, STM32L43xxx/44xxx, STM32L45xxx/46xxx) products.

# 3.12 Readout Unprotect command

This command is used to disable the flash memory read protection. When the bootloader receives the command, it transmits the ACK byte to the host. After the transmission of the ACK byte, the bootloader erases all the flash memory sectors and disables the read protection for the whole memory. If the erase operation is successful, the bootloader deactivates the RDP.

If the erase operation is unsuccessful, the bootloader transmits an NACK and the read protection remains active.

At the end of the Readout Unprotect command, the bootloader transmits an ACK and generates a system reset to take into account the new configuration of the option byte.

# Note:

For most STM32 products, this operation induces a mass erase of the flash memory, so the host must wait sufficient time after the second ACK before restarting the connection. To know how much time this operation takes, refer to the mass erase time (when specified) in the product datasheet.

![](images/3233f1904a8f7ed88feae3bcd319efe53724d710ac349da3b975f3009858ee0c.jpg)  
Figure 24. Readout Unprotect command: host side

![](images/593ee7338818c9069d80e029d2010b5e431bf5c3fb5d8481ac9e28a99599e8c9.jpg)  
Figure 25. Readout Unprotect command: device side   
RDU_PRM = Readout Unprotect. 2Not applicable to STM32WB0 series. 3. System reset is called only for some STM32 BL_ (STM32F0/F2/F4/F7) and some STM32L4 (STM32L412xx/422xx, STM32L43xxx/44xxx, STM32L45xxx/46xxx) products.

# 3.13 Get Checksum command

This command is used to compute a CRC value on a given memory area.

The memory area size must be a multiple of 32 bits (4 bytes

When the bootloader receives the command, it transmits the ACK byte to the application.

After the transmission of the ACK byte, the bootloader waits for an address (four bytes, byte 1 is the MSB and byte 4 is the LSB) with a checksum byte, then it checks the received address.

If the address is valid and the checksum is correct, the bootloader transmits an ACK byte, otherwise it transmits an NACK byte, and aborts the command.

When the address is valid and the checksum is correct, the bootloader waits for the size of the memory area that is expressed in 32-bit words (4 bytes) number and their complement byte (checksum).

If the checksum is not correct, the bootloader sends an NACK before aborting the command.

If the checksum is correct, the bootloader checks that the area size is different than 0 and that it does not exceed the size of the memory.

If the memory size is correct, the bootloader sends an ACK byte to the application.

When the memory size is valid and the checksum is correct, the bootloader waits for the CRC polynomial value and its complement byte (checksum).

If the checksum is correct, the bootloader transmits an ACK byte, otherwise it transmits an NACK byte, and aborts the command. If a product does not support polynomial value change, the value is ignored, but the device still sends ACK.

When the checksum is valid, the bootloader waits for the CRC initialization value and its complement byte (checksum).

If the checksum is correct, the bootloader transmits an ACK byte, otherwise it transmits an NACK byte, and aborts the command. If a product does not support CRCR initialization value change, the value is ignored but the device still sends ACK.

If the checksum is correct, the bootloader computes the CRC of the given memory, then sends an ACK to the application, followed by the CRC value and its complement byte (checksum).

The host sends the bytes to the STM32 as follows:   
Byte 1: 0xA1 + 0x5E   
Wait for ACK   
Bytes 3 to 6: Start address (byte 3: MSB, byte 6: LSB)   
Byte 7: Checksum: XOR (byte 3, byte 4, byte 5, byte 6)   
Wait for ACK   
Bytes 8 to 11 Memory area size (number of 32-bit words) (byte 8: MSB, byte 11: LSB)   
Byte 12: Checksum: XOR (byte 8, byte 9, byte 10, byte 11)   
Wait for ACK   
Byte 13 to 16: CRC polynomial (byte 13: MSB, byte 16: LSB)   
Wait for ACK   
Byte 17: Checksum: XOR (byte 13, byte 14, byte 15, byte 16)   
Wait for ACK   
Bytes 18 to 21 CRC initialization value (byte 18: MSB, byte 21: LSB)   
Wait for ACK   
Byte 22: Checksum: XOR (byte 18, byte 19, byte 20, byte 21)   
Wait for ACK

![](images/84e2f0fb1b85e2069be9accd68a4792991f0d4605ea923c4b64e2831c2446ddf.jpg)  
Figure 26. Get Checksum command: host side

![](images/8a0bdf17381926b47531766406da543a39caaf75e4b7a3d1f0db5184b4d2d0d8.jpg)  
Figure 27. Get Checksum command: device side

# 3.14 Special command

New bootloader commands are needed to support new STM32 features and to fulfill customers needs. To avoid specific commands for a single project, the Special command has been created, to be as generic as possible.

![](images/668aaa552f60a3b7dd10cd616cde88cca7cc6fbcfa3585f68fe74cecd8d543af.jpg)  
Figure 28. Special command: host side

![](images/c4b053daff5d6552cb4508d587a75bcb03d9953b863a33b598dddb9568e41b05.jpg)  
Figure 29. Special command: device side

The internal processing depends upon the project.

When the bootloader receives the Special command, it transmits the ACK byte to the host. Once the ACK is transmitted, the bootloader waits for a subcommand opcode (two bytes, MSB first) and a checksum byte. If the subcommand is supported by the STM32 bootloader and its checksum is correct, the bootloader transmits an ACK byte, otherwise it transmits an NACK byte, and aborts the command.

To keep the command generic, the data packet received by the bootloader can have different sizes, depending upon the subcommand needs.

Therefore, the packet is split in two parts:

Size of the data (two bytes, MSB first)   
N bytes of data If N = 0, no data are transmitted N must be inferior to 128.

If all conditions are satisfied (N ≤ 128 and the checksum is correct), the bootloader transmits an ACK, otherwise, it transmits an NACK byte, and aborts the command.

Once the subcommand is executed using the received data, the bootloader sends a response consisting in two consecutive packets:

Data packet Size of the data (two bytes, MSB first) N bytes of data If N = 0, no data are transmitted

√ Status packet

Size of the status data (two bytes, MSB first) N bytes of data If N = 0, no status data are transmitted

Finally, an ACK byte closes the special command interaction between the bootloader and the host.

# 3.15 Extended Special command

This command is slightly different from the Special command. It allows the user to send more data with the addition of a new buffer of 1024 bytes, and as a response it returns only the commands status.

![](images/66114664513fc6d694673b16cdccd796426124ba83f29876ab475a622d4ee182.jpg)  
Figure 30. Extended Special command: host side

![](images/ad44894e8c47d3d00c883287a899cfe7473808f83dd48ec7775947e1311caf75.jpg)  
Figure 31. Extended Special command: device side   
The internal processing depends on the project needs.

When the bootloader receives this command, it transmits the ACK byte to the host. Once the ACK is transmitted, the bootloader waits for a subcommand opcode (two bytes, MSB first) and a checksum byte. If the subcommand is supported by the STM32 bootloader and

its checksum is correct, the bootloader transmits an ACK byte, otherwise it transmits an NACK byte, and aborts the command.

The two packets can be received depending upon the subcommand needs:

• Packet1: Data 1 packet, where the number of bytes is limited to 128 bytes Packet2: Data2 packet, where the number of bytes is limited to 1024 bytes

If all conditions are satisfied (Packet1: N ≤ 128 and checksum is correct, and Packet2: N ≤ 128 and checksum is correct), the bootloader transmits an ACK. otherwise, it transmits an NACK byte, and aborts the command.

Once the subcommand is executed using received data, the bootloader sends a response consisting in one packet:

Size of the data (two bytes, MSB first) N bytes of data (If N = 0, no data are transmitted)

Finally, an ACK byte closes the command interaction between the bootloader and the host.

# Bootloader protocol version evolution

Table 3 lists the bootloader versions.

Table 3. Bootloader protocol versions(1)   

<table><tr><td rowspan=1 colspan=1>Version</td><td rowspan=1 colspan=1>Description</td></tr><tr><td rowspan=1 colspan=1>V2.0</td><td rowspan=1 colspan=1>Initial bootloader version.</td></tr><tr><td rowspan=1 colspan=1>V2.1</td><td rowspan=1 colspan=1>- Update Go command to initialize the main stack pointer- Update Go command to return NACK when jump address is in the option bytearea or system memory area- Update Get ID command to return the device ID on two bytes- Update the bootloader version to V2.1</td></tr><tr><td rowspan=1 colspan=1>V2.2</td><td rowspan=1 colspan=1>- Update Read Memory, Write Memory and Go commands to deny access, with anNACK response, to the first bytes of RAM used by the bootloader- Update Readout Unprotect command to initialize the whole RAM content to 0x0before RDP disable operation</td></tr><tr><td rowspan=1 colspan=1>V3.0</td><td rowspan=1 colspan=1>Extended Erase command added to support number of pages larger than 256 andseparate bank mass eraseErase command has not been modified in this version but, due to addition of theExtended Erase command, it is no longer supported (Erase and Extended Erasecommands are exclusive)</td></tr><tr><td rowspan=1 colspan=1>V3.1</td><td rowspan=1 colspan=1>Limitation fix of:When a Read Memory command or Write Memory command is issued with anunsupported memory address and a correct address checksum (i.e. address0x6000 0000), the command is aborted by the bootloader device, but the NACK(0x1F) is not sent to the host. As a result, the next two bytes (that is, the number ofbytes to be read/written and its checksum) are considered as a new command andits checksum (2).— No changes in specification, the product implementation has been corrected</td></tr><tr><td rowspan=1 colspan=1>V3.3</td><td rowspan=1 colspan=1>- Added support for Get Checksum command- Updated Get Command command to return the opcode of the Get Checksumcommand</td></tr><tr><td rowspan=1 colspan=1>V4.0</td><td rowspan=1 colspan=1>— Number of commands can vary from device to device with the same protocol. Toknow supported commands, use Get command</td></tr></table>

Not applicable on STM32WB0 series. Dedicated bootloaders have been implemented. f      -)o e /it   eual   al co x00, x01 x, 01, 0x21, 0x31, 0x43, 0x44, 0x63, 0x73, 0x82, or 0x92), the limitation is not perceived from the host as the command is NACK-ed anyway (as an unsupported new command).

# 5 Revision history

Table 4. Document revision history   

<table><tr><td colspan="1" rowspan="1">Date</td><td colspan="1" rowspan="1">Revision</td><td colspan="1" rowspan="1">Changes</td></tr><tr><td colspan="1" rowspan="1">09-Mar-2010</td><td colspan="1" rowspan="1">1</td><td colspan="1" rowspan="1">Initial release.</td></tr><tr><td colspan="1" rowspan="1">20-Apr-2010</td><td colspan="1" rowspan="1">2</td><td colspan="1" rowspan="1">Table 2: USART bootloader commands: added Extended Erasecommand; removed footnote 2 concerning read protection from theReadout Protect command.Communication safety: amended Note 1.Section 3.1: Get command: updated byte 10.Updated Figure 10: Go command: host side for missing ACK state.Section 3.7: Write Memory command: added Note 1 and Note 2.Figure 12, and Figure 13: added notes regarding N+1.Added Section 3.8: Extended Erase Memory command.Table 3: Bootloader protocol versions: added v3.0.</td></tr><tr><td colspan="1" rowspan="1">12-Feb-2013</td><td colspan="1" rowspan="1">3</td><td colspan="1" rowspan="1">Added Note:, Note and Note:.Changed all occurrences of "ROP" by "RDP" including in figures: Figure Figure 1 Figure 13 Figure 15 Figure 17 Figure 9 Figure,Figure 23., Figure 25..Added Table 1: Applicable products.</td></tr><tr><td colspan="1" rowspan="1">26-Mar-2013</td><td colspan="1" rowspan="1">4</td><td colspan="1" rowspan="1">Added Version 3.1 in Table 3: Bootloader protocol versions.Updated "byte 4" value in Section 3.3: Get ID command.Replaced "address" by "ID" in this Note 1.Replaced "End of EER" by "End of Go" in Figure 10: Go command: hostside.Updated first sentence in Section 3.7: Write Memory command.Removed "&amp; address=Ox1FFF F800" and replaced the two tests "Flashmemory address?" and "RAM address?" by a single test in Figure 13:Write Memory command: device side.Precised missing "Y" values in the third test of Figure 17: Extended EraseMemory command: device side.Added Note: above Figure 24: Readout Unprotect command: host side.</td></tr><tr><td colspan="1" rowspan="1">22-May-2013</td><td colspan="1" rowspan="1">5</td><td colspan="1" rowspan="1">Replaced "STM32L151xx, STM32L152xx and STM32L162xx" bySTM32L1 series" in Table 1: Applicable products.</td></tr><tr><td colspan="1" rowspan="1">20-Jun-2014</td><td colspan="1" rowspan="1">6</td><td colspan="1" rowspan="1">Updated Table 1: Applicable products.Removed footnote 4 and added footnote 3.in Table 2: USART bootloadercommands.Removed section 3.1 Device-dependent bootloader parameters.Updated Figure 10: Go command: host side and Figure 11: Go command:device side.Updated Section 3.6: Write Memory command.</td></tr><tr><td colspan="1" rowspan="1">21-Oct-2016</td><td colspan="1" rowspan="1">7</td><td colspan="1" rowspan="1">Introduced STM32L4 and STM32F7 series, hence updated Introductionand Table 1: Applicable products.</td></tr><tr><td colspan="1" rowspan="1">14-Feb-2019</td><td colspan="1" rowspan="1">8</td><td colspan="1" rowspan="1">Added STM32H7 series, hence updated Table 1: Applicable products.Updated Section 1: USART bootloader code sequence.Updated Figure 4: Get Version command: host side.Minor text edits across the whole document.</td></tr><tr><td colspan="1" rowspan="1">21-Feb-2019</td><td colspan="1" rowspan="1">9</td><td colspan="1" rowspan="1">Added STM32WB series, hence updated Table 1: Applicable products.</td></tr><tr><td colspan="1" rowspan="1">09-Apr-2019</td><td colspan="1" rowspan="1">10</td><td colspan="1" rowspan="1">Added STM32G0 and STM32G4 series, hence updated Table 1:Applicable products.</td></tr><tr><td colspan="1" rowspan="1">23-Sep-2019</td><td colspan="1" rowspan="1">11</td><td colspan="1" rowspan="1">Added STM32L5 series, hence updated Table 1: Applicable products.</td></tr><tr><td colspan="1" rowspan="1">04-Dec-2019</td><td colspan="1" rowspan="1">12</td><td colspan="1" rowspan="1">Added STM32WL series, hence updated Table 1: Applicable products.</td></tr><tr><td colspan="1" rowspan="1">30-Oct-2020</td><td colspan="1" rowspan="1">13</td><td colspan="1" rowspan="1">Updated Section 3.1: Get command.Added Section 3.13: Get Checksum command.Updated Table 2: USART bootloader commands and Table 3: Bootloaderprotocol versions.Minor text edits across the whole document.</td></tr><tr><td colspan="1" rowspan="1">08-Jun-2021</td><td colspan="1" rowspan="1">14</td><td colspan="1" rowspan="1">Updated Section 1: USART bootloader code sequence and Section 3.13:Get Checksum command.Updated Table 2: USART bootloader commands.Updated Figure 13: Write Memory command: device side, Figure 19:Write Protect command: device side, Figure 21: Write Unprotectcommand: device side, Figure 23: Readout Protect command: device sideand Figure 25: Readout Unprotect command: device side, and addedfootnotes to them.Updated Figure 26: Get Checksum command: host side.Added Section 3.14: Special command and Section 3.15: ExtendedSpecial command.</td></tr><tr><td colspan="1" rowspan="1">08-Feb-2022</td><td colspan="1" rowspan="1">15</td><td colspan="1" rowspan="1">Added STM32U5 series, hence updated Table 1: Applicable products.</td></tr><tr><td colspan="1" rowspan="1">06-Feb-2023</td><td colspan="1" rowspan="1">16</td><td colspan="1" rowspan="1">Added STM32C0 and STM32H5 series.Updated Table 1: Applicable products, Table 2: USART bootloadercommands, and Table 3: Bootloader protocol versions.Updated Section 3: Bootloader command set, Section 3.1: Get commandand Section 3.2: Get Version command.Updated Figure 2: Get command: host side, Figure 3: Get command:device side, Figure 4: Get Version command: host side, Figure 5: GetVersion command: device side, Figure 9: Read Memory command: deviceside, Figure 11: Go command: device side, Figure 12: Write Memorycommand: host side, Figure 13: Write Memory command: device side,Figure 15: Erase Memory command: device side, Figure 17: ExtendedErase Memory command: device side, Figure 19: Write Protectcommand: device side, Figure 21: Write Unprotect command: device side,and Figure 27: Get Checksum command: device side.Minor text edits across the whole document.</td></tr><tr><td colspan="1" rowspan="1">05-Mar-2024</td><td colspan="1" rowspan="1">17</td><td colspan="1" rowspan="1">Added STM32U0 and STM32WBA series.Updated Protection.Minor text edits across the whole document.</td></tr><tr><td colspan="1" rowspan="1">24-May-2024</td><td colspan="1" rowspan="1">18</td><td colspan="1" rowspan="1">Added STM32WB0 series.Updated Table 1: Applicable products and Table 2: USART bootloadercommands.Updated Figure 14: Erase Memory command: host side, Figure 15: EraseMemory command: device side, Figure 24: Readout Unprotect command:host side, and Figure 25: Readout Unprotect command: device side.Added footnotes to Table 3: Bootloader protocol versions and toSection 3: Bootloader command set.</td></tr><tr><td colspan="1" rowspan="1">04-Feb-2025</td><td colspan="1" rowspan="1">19</td><td colspan="1" rowspan="1">Added STM32U3 series.Updated Table 1: Applicable products.</td></tr><tr><td colspan="1" rowspan="1">03-Jul-2025</td><td colspan="1" rowspan="1">20</td><td colspan="1" rowspan="1">Added STM32WL3x line.Updated Table 1: Applicable products.Added note in Section 1: USART bootloader code sequence.Updated Figure 30: Extended Special command: host side and Figure 31:Extended Special command: device side.</td></tr></table>

# IMPORTANT NOTICE  READ CAREFULLY

acknowledgment.

the design of purchasers' products.

No license, express or implied, to any intellectual property right is granted by ST herein.

or service names are the property of their respective owners.

I