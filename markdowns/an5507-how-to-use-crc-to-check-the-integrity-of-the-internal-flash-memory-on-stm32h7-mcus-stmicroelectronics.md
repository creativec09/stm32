# How to use CRC to check the integrity of the internal flash memory on STM32H7 MCUs

These documents are all available for download on www.st.com.

# Introduction

flash memory to ensure that the content of the flash memory is reliable.

F A the end, details about the time needed to perform a CRC are presented.

# Reference documents

STM32H742, STM32H743/753, and STM32H750 Value line advanced Arm®-based 32-bit MCUs (RM0433) STM32H745/755 and STM32H747/757 advanced Arm®-based 32-bit MCUs (RM0399) STM32H7A3/B3 and STM32H7B0 Value line advanced Arm®-based 32-bit MCUs (RM0455) STM32H723/733, STM32H725/735, and STM32H730 Value line advanced Arm®-based 32-bit MCUs (RM0468) STM32H7Rx/7Sx Arm®-based 32-bit MCUs (RM0477)

# 1 CRC overview

Cyclic redundancy check (CRC) is an error detection technique that checks the integrity of data during transmission or storage.

TheCRCalgorithm computes a checksum oreach specificdata that passes through . For the calculatin uses a polynomial, the initial CRC value, and the data to check.

The CRC-32 Ethernet polynomial is widely used and proved efficient for CRC calculation.

CRC-32 (Ethernet) polynomial: x^32 + x^26 + x^23 + x^22 + x^16 + x^12 + x^11 + x^10 + x^8 + x^7 + x^5 + x^4 + x^2 + x^1 + x^0 which is 0x04C1 1DB7 in normal representation or 0xEDB8 8320 in reverse notation.

The figure below shows the block diagram of the CRC calculation algorithm:

![](images/7a1883c981793b6c305a3c69f10eded3033a690ca0610f330f4f173914e98be5.jpg)  
Figure 1. CRC block diagram

A typical use case of CRC is the check of data integrity during a transfer of programming phase.

# Example:

• The CRC value is computed on sender and receiver sides: The sender calculates its CRC and appends it to the message to send. The receiver, on its side, puts the data through the same process and compares it with the result appended by the sender. If the two calculated CRCs are equal, it means that no issue occurred and the data got sent/stored correctly. Otherwise, in case the CRCs do not match, that indicates data was corrupted during transmission. In suc situations, the receiver can request to transmit again the block of data.

# 2 CRC hardware implementation on STM32H7 series

The STM32 MCUs embed aCRC calculatin unit that allows them toget he CRC value a block f dataAuse cafeRC calculatinni ihevefiation  he flash emoy interiyTeRChel c which was generated at link-time and stored at a given memory location.

If RCalus the same er hi cprison, he aplication maycontiue he eecution  e as m an IAP).

TRCf oec memory contents.Which means that, it could be se t verihe integrity  thermemori.TheRal other eour such as eU r h DMA transe at from he peripheral mmoryhaa need to be checked on the CRC calculation unit data register (CRC_DR) where CRC is calculated.

As an improvement, the STM32H7 series embed a dedicated CRC hardware module inside their flash memory content. It does not need any further peripherals to accomplish this task.

The embedded CRC module in the flash memory interface facilitates the implementation of tests to detect peranent faults that might impact the flash memory including thememory cells and the address decoer y periodically computing the flash memory CRC signature and comparing it against its expected value.

# 3 Flash memory CRC module operating mode

The embedded flash memory interface of the STM32H7 series manages the accesses of any master to their embedded nonvolatile memory (up to 2 Mbytes).

The size of one flash memory word is:

256 bits on STM32H723/733, STM32H725/735, STM32H730, STM32H742, STM32H743/753, STM32H750, STM32H745/755, and STM32H747/757. 128 bits on STM32H7Rx, STM32H7Sx, STM32H7A3, STM32H7B3, and STM32H7B0.

The flash memory interface on STM32H7 series embeds a CRC hardware module that permits the check f the intisecnten heasmeory r Dependin he prorae nee,hren e defined as a whole bank, some consecutive sectors, or an area defined by start/end addresses.

The configuration steps recommended for a correct operation of the CRC hardware module are:

1Unlock the flash memory to enable the flash memory control-register access.

Enable the CRC feature by setting the CRC_EN bit in the FLASH_CR1/2 registel

Program the desired data burst size in the CRC_BURST field of the FLASH_CRCCR1/2 register. The CRC hardware module processes flash memory data by chunks of 4, 16, 64 or 256 flash-words. Those chunks values are defined as burst size and are configurable by software.

CRC_InitStruct.BurstSize = FLASH_CRC_BURST_SIZE_4; //every burst has a size of 4 Flash wor ds   
CRC_InitStruct.BurstSize = FLASH_cRC_BURST_SIZE_16; //every burst has a size of 16 Flash w ords   
CRC_InitStruct.BurstSize = FLASH_cCRC_BURST_SIZE_64; //every burst has a size of 64 Flash w ords   
CRC_InitStruct.BurstSize = FLASH_CRC_BURST_SIZE_256; //every burst has a size of 256 Flash words

4Define the flash memory area to compute the CRC. The area processed by the RC module can be defined either between two addresses, on a list of sectors or on a whole bank. The configuration is done by software.

# xample of configuration between two addresses:

Specify the start and end addresses to define the memory area where CRC must be calculated. This is done by programing FLASH_CRCSADD1/2R and FLASH_CRCEADD1/2R registers, respectively.

CRC_InitStruct.TypeCRC = FLASH_CRC_ADDR;   
CRC InitStruct.CRCStartAddr = UserCRCStartAddr;   
CRC_InitStruct.CRCEndAddr = UserCRCEndAddr-1;

# Note:

When addresses are used to define the data to check, the CRC burst size has an impact on the result. Cas 1: The start address and the end address +1 are multiples of the chosen burst size (step 3). In this case, the CRC is calculated exactly from start to end address as shown below.

![](images/dfd47ddfa9019bcdebb6719d6457bcaf7f8e49311b268c7de02f94320b8fe35e.jpg)  
Figure 2. CRC computed in an address-defined area - case 1

Cas : the start address and the end address are not multiples of the chosen burst size. In this case, the CRC is calculated in the area between the last address multiple of the burst size before the chosen start address and the next address multiple of the burst size -1 after the end address as shown below.

![](images/e29037a44b5196f4ff155e8a38aee63f70abe25839cda530004ef9b7cab326b6.jpg)  
Figure 3. Case 2 CRC

When performed at sector level, CRC calculation is done on one or more selected user flash memory sectors.Those sectors are defined by indicating the first sector on which the CRC should be calculated, followed by the total number of sectors to check.

In order to select the targeted sectors, CRC_BY_SECT bit in the FLASH_CRCCR1/2 register should be set and the target sector numbers in the CRC_SECT field of the FLASH_CRCCR1/2 register need to be programmed. In addition, the ADD_SECT bit should be set after each CRC_SECT programming.

CRC InitStruct.TypeCRC FLASH_CRC_SECTORS;   
CRC_InitStruct.Sector = FLASH_SECTOR_0; Specify the initial sector CRC_InitStruct.NbSectors = 1;¯// Number of sectors

# Example of configuration on a whole bank:

Allbank 1 or 2 user sectors are added to the list of sectors on which the CRC should be calculated.

CRC_InitStruct.TypeCRC = FLASH_CRC_BANK; CRC_InitStruct.Bank = FLASH_BANK_1; //Bank1 or 2 could be specified

Start the CRC operation by setting the START_CRC bit in FLASH_CRCCR1/2 register.

Wait until the CRC_BUSY flag in FLASH_SR1/2 register is reset

Retrieve the CRC result in the FLASH_CRCDATAR register.

The steps listed above, excepting step 1, are already implemented on the function "HAL_FLASHEx_ComputeCRC" in the extended FLASH HAL module driver "stm32h7x_hal_flash_ex.c".

T a ogurtin abovhoul ureendngeeRclculan .

# Note:

• The CRC operation is concurrent with option-byte change operations. If a CRC operation is requested while an option-byte change is ongoing, the option-byte change operation must be completed before serving the CRC operation, and vice versa. Running a CRC on PCROP-protected or secure-protected user flash memory area may alter the expected CRC value. Only one CRC check operation on bank 1 or 2 can be launched at the time. Thus, to avoid corruption, do not configure the CRC calculation on one bank, while calculating the CRC on the other bank.

# Software simulation of the hardware CRC block calculation

The "SW_crc32Calcul" function below is developed to simulate the behavior of the CRC hardware module embedded in the flash memory interface of the STM32H7 series.

# CRC-32 polynomial should be defined: as follows:

/\* CRC-32 polynomial \*   
#define POLY Ox4c11db7   
/\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*   
\* Title: SW_crc32_Calcul \* Input parameters: \* \* - buf: Pointer to first data byte \* \* len: Number of data bytes stored, for which CRC should be calculated \* \* - BurstSize: varies depending on the requested burst size "4, 16, 64 or 256 Flash words" \*

Output: Calculated CRC result

\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\* \* \* \* \* \* \*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*   
uint32_t SW_crc32_Calcul(const uint32_t \*buf, size_t len, uint32_t BurstSize)   
{ int k; /\* Define the initial CRC value \*/ uint32_t crc = 0; /\* Define the length of data on which CRC has to be computed depending on CRC burst size if ( len > BurstSize) { if ( (len % BurstSize) != 0) len = BurstSize \* ( ( len / BurstSize) + 1 ); } else len = BurstSize; /\* Calculate CRC value \*/ while (len--) { crc ^= \*buf++; for (k = 0; k< 32; k++) crc = crc & 0x80000000 ? (crc << 1) ^ POLY : crc << 1; crc ^= 0x55555555; /\* Return CRC value \*/ return crc;   
Simple example:   
#define N 10   
int main(void)   
{ /\* compute CRC for N words starting at address Ox08000000 \*/ uint32_t u32CrcValue = SW_crc32_Calcul((const uint32_t \*)Ox08000000, N\*4\*8, 4); while(1);

# System performance impact when using CRC

Using theRC hardware module costs the application some U clock pulses. The number of pulses depends on the load of the flash memory interface. Any operation on the flash memory increases the load, and then increases the time for a CRC calculation.

In the case whee nly eRCcaclati beexece he fash meory    put n heRC vey clock pule. In this case, the time needed to complete the calculation can e estimated.The numb clock pulses needed to calculate one flash memory word depends on the flash memory word size:

8 clock pulses for STM32H723/733, STM32H725/735, STM32H730, STM32H742, STM32H743/753, STM32H750, STM32H745/755, and STM32H747/757 devices

4 clock pulses for STM32H7Rx, STM32H7Sx, STM32H7A3, STM32H7B3, and STM32H7B0 devices

In aditin,minium e-lock pulss ostevey tme that heRChardwae block loads aew burs data.

The fwig tables desribe the calculation time needed t calculate he CRCalueor  flash memoy depending on the configured burst size on the STM32H7 series.

Table 1. CRC calculation time on STM32H742, STM32H7X3, STM32H7x5, STM32H7x7, STM32H730, and STM32H750   

<table><tr><td rowspan=1 colspan=1>Burst size</td><td rowspan=1 colspan=1>CPU clock pulses for 1 burst</td><td rowspan=1 colspan=1>CPU clock pulses for X burst</td></tr><tr><td rowspan=1 colspan=1>4 Flash word</td><td rowspan=1 colspan=1>4 x 8 =32</td><td rowspan=1 colspan=1>(32 + 1)×X</td></tr><tr><td rowspan=1 colspan=1>16 Flash words</td><td rowspan=1 colspan=1>16 x 8 = 128</td><td rowspan=1 colspan=1>(128 + 1) × X</td></tr><tr><td rowspan=1 colspan=1>64 Flash words</td><td rowspan=1 colspan=1>64 x8 =512</td><td rowspan=1 colspan=1>(512 + 1)× X</td></tr><tr><td rowspan=1 colspan=1>256 Flash words</td><td rowspan=1 colspan=1>256 x 8 = 2048</td><td rowspan=1 colspan=1>(2048 + 1)× X</td></tr></table>

1. X = number of bursts in the memory area in which the CRC is computed

Table 2. CRC calculation time on STM32H7Rx, STM32H7Sx, STM32H7A3, STM32H7B3, and STM32H7B0   

<table><tr><td rowspan=1 colspan=1>Burst size</td><td rowspan=1 colspan=1>CPU clock pulses for 1 burst</td><td rowspan=1 colspan=1>CPU clock pulses for X burst</td></tr><tr><td rowspan=1 colspan=1>4 Flash word</td><td rowspan=1 colspan=1>4 x 4 = 16</td><td rowspan=1 colspan=1>(16+1)×X</td></tr><tr><td rowspan=1 colspan=1>16 Flash words</td><td rowspan=1 colspan=1>16 x 4 = 64</td><td rowspan=1 colspan=1>(64 + 1) × X</td></tr><tr><td rowspan=1 colspan=1>64 Flash words</td><td rowspan=1 colspan=1>64 x 4 = 256</td><td rowspan=1 colspan=1>(256 + 1)× X</td></tr><tr><td rowspan=1 colspan=1>256 Flash words</td><td rowspan=1 colspan=1>256 x 4 = 1024</td><td rowspan=1 colspan=1>(1024 + 1)× X</td></tr></table>

1. X = number of bursts in the memory area in which the CRC is computed

oblolculann the Flash memory area integrity using the dedicated CRC hardware block is highly recommended.

# 6 Conclusion

CRC is a simple but an effective way  detect data corruption during transr/programmig r ashmemory failure. This application note described the CRC feature and how the CRC hardware module embedded in STM32H7 Series devices flash memory interface works.

# Revision history

Table 3. Document revision history   

<table><tr><td>Date</td><td>Version</td><td>Changes</td></tr><tr><td>29-Mar-2022</td><td>1</td><td>Initial release.</td></tr><tr><td rowspan="6">07-Mar-2024</td><td rowspan="5">2</td><td>Updated:</td></tr><tr><td>Document title</td></tr><tr><td>Section Introduction</td></tr><tr><td>Section 3: Flash memory CRC module operating mode</td></tr><tr><td>Section 4: Software simulation of the hardware CRC block calculation</td></tr><tr><td></td><td>Section 5: System performance impact when using CRC</td></tr></table>

# Contents

CRC overview CRC hardware implementation on STM32H7 series.   
3 Flash memory CRC module operating mode   
4 Software simulation of the hardware CRC block calculation   
5 System performance impact when using CRC 8   
6 Conclusion 9   
Revision history 10   
List of tables 12   
List of figures. 13

# List of tables

Table 1. CRC calculation time on STM32H742, STM32H7X3, STM32H7x5, STM32H7x7, STM32H730, and STM32H750. . 8   
Table 2. CRC calculation time on STM32H7Rx, STM32H7Sx, STM32H7A3, STM32H7B3, and STM32H7B0. 8   
Table 3. Document revision history . 10

# List of figures

Figure 1. CRC block diagram. 2   
Figure 2. CRC computed in an address-defined area - case 1 5   
Figure 3. Case 2 CRC. 5

# IMPORTANT NOTICE  READ CAREFULLY

pt old ursant  dits   leole.

purchasers' products.

No license, express or implied, to any intellectual property right is granted by ST herein.

are the property of their respective owners.

I

© 2024 STMicroelectronics - All rights reserved