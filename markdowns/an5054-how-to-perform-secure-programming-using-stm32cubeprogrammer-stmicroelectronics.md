# How to perform secure programming using STM32CubeProgrammer

# Introduction

This document specifies the steps and tools required to prepare SFI (secure internal firmware install), SFIx (secure external firmware install), or SSP (secure secret provisioning) images. It then describes how to program these into STM32 MCU devices that support SFI/SFIx on-chip internal memory, external flash memory or, for the SSP install procedure, STM32 MPU devices. It is based on the STM32CubeProgrammer tool set (STM32CubeProg). These tools are compatible with all STM32 devices.

The main objective of the SFI/SFIx processes is the secure installation of OEM and software-partner firmware, which prevents firmware cloning.

The STM32MP1 series supports protection mechanisms allowing protection of critical operations (such as cryptography algorithms) and critical data (such as secret keys) against unexpected access.

This application note also gives an overview of the STM32 SSP solution with its associated tool ecosystem, and explains how to use it to protect OEM secrets during the CM product manufacturing stage.

Refer also to:

AN4992 [1], which provides an overview of the secure firmware install (SFI) solution, and how this provides a practical level of protection of the IP chain - from firmware development up to programming the device on-chip flash memory.

AN5510 [3], which provides an overview of secure secret provisioning (SSP).

# Contents

# General information 11

1.1 Licensing information .11   
1.2 Acronyms and abbreviations .11

# Encrypted firmware (SFI) preparation using the STPC tool . . . . . . . . 12

2.1 System requirements 12   
2.2 SFI generation process 12   
2.3 SFIx generation process 19   
Area E.. .20   
Area K. . .20

2.4 SSP generation process . 23

# STM32 Trusted Package Creator tool in the command-line interface . . . 25

2.5.1 Steps for SFI generation (CLI) . .27   
2.5.2 Steps for SSP generation (CLI) . 30

# 2.6 Using the STM32 Trusted Package Creator tool graphical user interface 31

2.6.1 SFI generation using STPC in GUI mode 31   
SFI GUI tab fields . .33   
2.6.2 SFIx generation using STPC in GUI mode 36   
SFIx GUI tab fields .37   
2.6.3 SSP generation using STPC in GUI mode 39   
SSP GUI tab fields .39   
2.6.4 Settings 41   
2.6.5 Log generation 42

# Encrypted firmware (SFI/SFIx) programming with

# STM32CubeProgrammer 43

3.1 Chip certificate authenticity check and license mechanism 43

3.1.1 Device authentication 43   
3.1.2 License mechanism 43   
License mechanism general scheme .43   
License distribution. .44   
STM32HSM programming by OEM for license distribution .44

3.2 Secure programming using a bootloader interface 45

3.2.1 STM32CubeProgrammer for SFI using a bootloader interface . . . . . .

3.2.2 STM32CubeProgrammer for SSP via a bootloader interface . . . . . . .

3.2.3 STM32CubeProgrammer get certificate via a bootloader interface . . . . 48

3.3 Secure programming using the JTAG/SWD interface 48

3.3.1 SFI/SFIx programming using JTAG/SWD flow .48

3.3.2 STM32CubeProgrammer for secure programming using JTAG/SWD . . 49

3.4 Secure programming using bootloader interface (UART/I2C/SPI/USB) . . 50   
SFI example . .50   
SFIx example . . ..50

# Example of SFI programming scenario . . 51

4.1 Scenario overview 51

4.2 Hardware and software environment 51

4.3 Step-by-step execution 51

4.3.1 Build OEM application 51   
4.3.2 Performing the option byte file generation (GUl mode) 51   
4.3.3 Perform the SFI generation (GUI mode) 52   
4.3.4 Performing STM32HSM programming for license generation   
using STPC (GUI mode) 54   
4.3.5 Performing STM32HSM programming for license generation   
using STPC (CLI mode) . 56   
Example of STM32HSM-V1 provisioning .56   
Example of STM32HSM-V2 provisioning .57   
Example of STM32HSM get information .57   
4.3.6 Programming input conditions 58   
4.3.7 Performing the SFI install using STM32CubeProgrammer 59   
Using JTAG/SWD. .59   
4.3.8 SFI with integrity check (for STM32H73xxx) 60   
Usage example: .60

# Example of SFI programming scenario for STM32WL . . . . . . . ....63

5.1 Scenario overview 63

5.2 Hardware and software environment 63

5.3 Step-by-step execution 63

5.3.1 Build OEM application .63   
5.3.2 Perform the SFI generation (GUI mode) 63   
5.3.3 Programming input conditions 65   
5.3.4 Perform the SFI install using STM32CubeProgrammer .66

# Example of SFI programming scenario for STM32U5 68

6.1 Scenario overview 68   
6.2 Hardware and software environment 68   
6.3 Step-by-step execution . 68   
6.3.1 Build OEM application . . 68   
6.3.2 Perform the SFI generation (GUI mode) 68   
6.3.3 Programming input conditions 70   
6.3.4 Perform the SFI install using STM32CubeProgrammer 70   
Using JTAG/SWD. .70

# Example of SFI programming scenario for

# STM32WBA5x and STM32WBA6x . . . . . . 73

7.1 Scenario overview 73   
7.2 Hardware and software environment 73

7.3 Step-by-step execution 73

7.3.1 Build OEM application 73   
7.3.2 Perform the SFI generation (GUI mode) 73   
7.3.3 Programming input conditions 74   
7.3.4 Perform the SFI install using STM32CubeProgrammer 74   
Using the UART interface. .75

# Example of SFIA programming scenario for STM32WBA5x . . . . . . . . 80

8.1 Scenario overview 80

8.2 Hardware and software environment 80

8.3 Step-by-step execution 80

8.3.1 Build an OEM application .80   
8.3.2 Perform the STM32HSM programming for the SFIA license generation   
(GUI mode) 80   
8.3.3 Perform the SFI generation (GUI mode) 81   
8.3.4 Programming input conditions 81   
8.3.5 Perform the SFI installation using STM32CubeProgrammer . 81

# Example of SFI programming scenario for STM32H5 . . . . ...83

9.1 Scenario overview 83   
9.2 Hardware and software environment 83   
9.3 Step-by-step execution . . 83   
9.3.1 Build OEM application 83   
9.3.2 Perform the SFI generation (GUI mode) 83   
9.3.3 Programming input requirements 84   
9.3.4 Perform the SFI install using STM32CubeProgrammer 85   
Command-line mode . .85   
Graphical user interface mode . . .86

# Example of SFI programming scenario for STM32H7Rx/7Sx . . . . . . . 88

10.1 Scenario overview 88

10.2 Hardware and software environment 88

10.3 Step-by-step execution 88

10.3.1 Build an OEM application 88   
10.3.2 Perform the SFI generation (GUI mode) 88   
10.3.3 Programming input requirements 89   
10.3.4 Perform the SFI install using STM32CubeProgrammer 89   
Command-line mode .90   
Graphical user interface mode . .90

# Example of SFIx programming scenario for STM32H7 . . . . . . 92

11.1 Scenario overview 92

11.2 Hardware and software environment 92

1.3 Step-by-step execution . 92

11.3.1 Build OEM application 92   
11.3.2 Perform the SFIx generation (GUI mode) 92   
11.3.3 Performing STM32HSM programming for license generation using STPC (GUI mode) 94   
11.3.4 Performing STM32HSM programming for license generation using STPC (CLI mode) 95   
11.3.5 Programming input conditions 95   
11.3.6 Perform the SFIx installation using STM32CubeProgrammer 95 Using JTAG/SWD. .95

# Example of SFIx programming scenario for STM32L5/STM32U5 . . . 100

12.1 Scenario overview 100   
12.2 Hardware and software environment 100   
12.3 Step-by-step execution. 100   
12.3.1 Build an OEM application 100   
12.3.2 Perform the SFIx generation (GUI mode) 101   
Use case 1: generation of SFIx without key area for STM32L5. .101

Use case 2: generation of SFIx with key area for STM32L5 .103 Use case 3: generation of SFIx without key area for STM32U5. . . .104 Use case 4: generation of SFIx with key area for STM32U5 . .105   
12.3.3 Performing STM32HSM programming for license generation using STPC (GUI mode) 107   
12.3.4 Performing STM32HSM programming for license generation using STPC (CLI mode) . 107   
12.3.5 Programming input conditions 107   
12.3.6 Perform the SFIx installation using STM32CubeProgrammer . . . . . . . 107

# Example of SFIx programming scenario for STM32H5 . . . . . . .. . . 110

13.1 Scenario overview .110

13.2 Hardware and software environment .110

13.3 Step-by-step execution .110

13.3.1 Build an OEM application 110   
13.3.2 Perform the SFIx generation (GUI mode) 111   
13.3.3 Programming input conditions 112   
13.3.4 Perform the SFIx installation using STM32CubeProgrammer CLI . . . 112

# Example of SSP programming scenario for STM32MP1 . . . . . . . . . . 114

14.1 Scenario overview .114

14.2 Hardware and software environment .114

14.3 Step-by-step execution . .114

14.3.1 Building a secret file 114   
14.3.2 Performing the SSP generation (GUI mode) 115   
14.3.3 Performing STM32HSM programming for license generation   
using STPC (GUI mode) 115   
14.3.4 SSP programming conditions 117   
14.3.5 Perform the SSP installation using STM32CubeProgrammer 117

# Example of SSP-SFI programming scenario for STM32MP2 . . . . . . 119

15.1 Scenario overview .119

15.2 Hardware and software environment .119

15.3 Step-by-step execution .119

15.3.1 Building a secret file .. 119   
15.3.2 Building a backup memory file 120   
15.3.3 Performing the SSP-SFI generation (GUI mode) .121   
15.3.4 Performing STM32HSM programming (GUI mode) 122   
15.3.5 SSP-SFI programming conditions 122   
15.3.6 Perform the SSP installation using STM32CubeProgrammer . . . . . . . 122

3 Reference documents 124

Revision history 125

# List of tables

Table 1. List of abbreviations. 11   
Table 2. SSP preparation inputs. 24   
Table 3. Document references 124   
Table 4. Document revision history 125

# List of figures

Figure 1. SFI preparation mechanism . 12   
Figure 2. SFI image process generation 13   
Figure 3. RAM size and CT address inputs used for SFI. 14   
Figure 4. ' and 'R' area specifics versus a regular SFI area 15   
Figure 5. Error message when firmware files with address overlaps are used 16   
Figure 6. Error message when a SFI area address is not located in flash memory. 17   
Figure 7. SFI format layout 18   
Figure 8. SFI image layout in case of split 19   
Figure 9. RAM size and CT address inputs used for SFIx. 21   
Figure 10. SFIx format layout. . 22   
Figure 11. SFIx image layout in case of split 23   
Figure 12. SSP preparation mechanism 23   
Figure 13. Encryption file scheme 25   
Figure 14. STM32 Trusted Package Creator tool - SFI preparation options 26   
Figure 15. Option bytes file example . 28   
Figure 16. SFI generation example using an ELF file 29   
Figure 17. SSP generation success. 31   
Figure 18. SFI generation Tab 32   
Figure 19. Firmware parsing example 33   
Figure 20. SFI successful generation in GUl mode example 35   
Figure 21. SFIx generation Tab . . 36   
Figure 22. Firmware parsing example 37   
Figure 23. SFIx successful generation in GUl mode example 38   
Figure 24. SSP generation tab. 39   
Figure 25. SSP output information. 40   
Figure 26. Settings icon and settings dialog box 41   
Figure 27. Log example . . . . . 42   
Figure 28. STM32HSM programming GUI in the STPC tool . 45   
Figure 29. SSP installation success. 47   
Figure 30. Example of getcertificate command execution using UART interface 48   
Figure 31. SFI programming by JTAG/SWD flow overview   
(monolithic SFI image example). 49   
Figure 32. Example of getcertificate command using JTAG 50   
Figure 33. STM32Trusted Package Creator SFI OB GUI 52   
Figure 34. STPC GUI during SFI generation . 53   
Figure 35. Example of STM32HSM programming using STPC GUI 55   
Figure 36. Example product ID 56   
Figure 37. STM32HSM information in STM32 Trusted Package Creator CLI mode 57   
Figure 38. STM32Trusted Package Creator SFI 'hash Generator 'check box. . 60   
Figure 39. SFI installation success using SWD connection (1) 61   
Figure 40. SFI installation success using SWD connection () 62   
Figure 41. STPC GUI during the SFI generation (STM32WL). 64   
Figure 42. Example -dsecurity command-line output. 65   
Figure 43. Example -setdefaultob command-line output . 66   
Figure 44. SFI installation via SWD execution command-line output 67   
Figure 45. STPC GUI during the SFI generation (STM32U5) 69   
Figure 46. SFI installation via SWD execution (1) 71   
Figure 47. SFI installation via SWD execution 72   
Figure 48. STPC GUI during the SFI generation (STM32WBA5x) 74   
Figure 49. SFI installation via UART execution using CLI (1) 76   
Figure 50. SFI installation via UART execution using CLI (2) 77   
Figure 51. SFI installation via UART execution using CLI (3) 78   
Figure 52. STM32WBA5x SFI successful programming via UART interface using GUI . 79   
Figure 53. Example of STM32HSM programming (SFIA License) using STPC GU 81   
Figure 54. SFI generation for STM32H5 . 84   
Figure 55. STMicroelectronics global license generation for STM32H5 85   
Figure 56. STM32H5 SFI successful programming via CLI. 86   
Figure 57. STM32H5 SFI successful programming via GUI 87   
Figure 58. SFI generation for STM32H7Rx/7Sx 89   
Figure 59. STM32H7Rx/7Sx SFI successful programming via CLI . 90   
Figure 60. STM32H7Rx/7Sx SFI successful programming via GUI. 91   
Figure 61. Successful SFIx generation 93   
Figure 62. Example of STM32HSM programming using STPC GUI 94   
Figure 63. SFIx installation success using SWD connection (1) 96   
Figure 64. SFIx installation success using SWD connection (2) 97   
Figure 65. SFIx installation success using SWD connection (3) 98   
Figure 66. SFIx installation success using SWD connection (4) 99   
Figure 67. Successful SFIx generation use case 1 102   
Figure 68. Successful SFIx generation use case 2 103   
Figure 69. Successful SFIx generation use case 3 104   
Figure 70. Successful SFIx generation use case 3 for STM32U59xxx, STM32U5Axxx,   
STM32U5Fxxx, and STM32U5Gxxx. 105   
Figure 71. Successful SFIx generation use case 4 106   
Figure 72. Successful SFIx generation use case 4 for STM32U59xxx, STM32U5Axxx,   
STM32U5Fxxx, and STM32U5Gxxx. . .106   
Figure 73. SFIx installation success using SWD connection (1) 108   
Figure 74. SFIx installation success using SWD connection (2) 108   
Figure 75. SFIx installation success using SWD connection (3) 109   
Figure 76. SFIx image generation for STM32H5 . 111   
Figure 77. SFIx installation success for STM32H5 113   
Figure 78. STM32 Trusted Package Creator SSP GUI tab . 115   
Figure 79. Example of STM32HSM-V2 programming using STPC GUI 116   
Figure 80. STM32MP1 SSP installation success. 118   
Figure 81. Secrets Gen Window 120   
Figure 82. SSP Backup memory window. . 121   
Figure 83. SSP-SFI image generation window 121   
Figure 84. SSSP-SFI installation 123

# 1 General information

# 1.1 Licensing information

STM32CubeProgrammer supports STM32 32-bit devices based on Arm®(a) Cortex®-M processors.

# 1.2 Acronyms and abbreviations

Table 1. List of abbreviations   

<table><tr><td rowspan=1 colspan=1>Abbreviations</td><td rowspan=1 colspan=1>Definition</td></tr><tr><td rowspan=1 colspan=1>AES</td><td rowspan=1 colspan=1>Advanced encryption standard</td></tr><tr><td rowspan=1 colspan=1>CLI</td><td rowspan=1 colspan=1>Command-line interface</td></tr><tr><td rowspan=1 colspan=1>CM</td><td rowspan=1 colspan=1>Contract manufacturer</td></tr><tr><td rowspan=1 colspan=1>GCM</td><td rowspan=1 colspan=1>Galois counter mode (one of the modes of AES)</td></tr><tr><td rowspan=1 colspan=1>GUI</td><td rowspan=1 colspan=1>Graphical user interface</td></tr><tr><td rowspan=1 colspan=1>HSM</td><td rowspan=1 colspan=1>Hardware security module (such as STM32HSM)</td></tr><tr><td rowspan=1 colspan=1>HW</td><td rowspan=1 colspan=1>Hardware</td></tr><tr><td rowspan=1 colspan=1>MAC</td><td rowspan=1 colspan=1>Message authentication code</td></tr><tr><td rowspan=1 colspan=1>MCU</td><td rowspan=1 colspan=1>Microcontroller unit</td></tr><tr><td rowspan=1 colspan=1>OEM</td><td rowspan=1 colspan=1>Original equipment manufacturer</td></tr><tr><td rowspan=1 colspan=1>OTP</td><td rowspan=1 colspan=1>One-time programmable</td></tr><tr><td rowspan=1 colspan=1>PCROP</td><td rowspan=1 colspan=1>Proprietary code read-out protection</td></tr><tr><td rowspan=1 colspan=1>PI</td><td rowspan=1 colspan=1>Position independent</td></tr><tr><td rowspan=1 colspan=1>ROP</td><td rowspan=1 colspan=1>Read-out protection</td></tr><tr><td rowspan=1 colspan=1>RSS</td><td rowspan=1 colspan=1>Root security service (secure)</td></tr><tr><td rowspan=1 colspan=1>RSSe</td><td rowspan=1 colspan=1>Root security service extension</td></tr><tr><td rowspan=1 colspan=1>SFI</td><td rowspan=1 colspan=1>Secure (internal) firmware install</td></tr><tr><td rowspan=1 colspan=1>SFIx</td><td rowspan=1 colspan=1>Secure external firmware install</td></tr><tr><td rowspan=1 colspan=1>SSP</td><td rowspan=1 colspan=1>Secure secret provisioning</td></tr><tr><td rowspan=1 colspan=1>STPC</td><td rowspan=1 colspan=1>STM32 Trusted Package Creator</td></tr><tr><td rowspan=1 colspan=1>STM32</td><td rowspan=1 colspan=1>ST family of 32-bit Arm®-based microcontrollers</td></tr><tr><td rowspan=1 colspan=1>SW</td><td rowspan=1 colspan=1>Software</td></tr><tr><td rowspan=1 colspan=1>XO</td><td rowspan=1 colspan=1>Execute only</td></tr></table>

# Encrypted firmware (SFI) preparation using the STPC tool

The STM32 Trusted Package Creator (STPC) tool allows the generation of SFI image for STM32 devices. It is available in both CLI and GUI modes free of charge from www.st.com.

# 2.1 System requirements

Using the STM32 Trusted Package Creator tool for SFI/SFIx and SSP image nratio u    iteWino buntu Fedora®(), or macOs®(e).

Note:

Refer to [4] or [5] for the supported operating systems and architectures.

# 2.2 SFI generation process

The SFI format is an encryption format for internal firmware created by STMicroelectronics that transforms internal firmware (in ELF, Hex, Bin, or Srec formats) into encrypted and authenticated firmware in a SFI format using the AES-GCM algorithm with a 128-bit key. The SFI preparation process used in the STM32 Trusted Package Creator tool is described in Figure 1.

![](images/29c0e0ea0b1a8b8f13b237d442110faf93443301706a4d2f774bdaf20b630168.jpg)  
Figure 1. SFI preparation mechanism

aWindows is a trademark of the Microsoft group of companies.   
Linux® is a registered trademark of Linus Torvalds.   
c.Ubuntu® is a registered trademark of Canonical Ltd.   
Fedora® is a trademark of Red Hat, Inc.   
ma®s aradark  Apple ncgst nhe U..nd othecunts n .

The SFI generation steps as currently implemented in the tool are described in Figure 2.

![](images/a855de01bdfa9167dcc8f8ee6712f4597573acd544103b87f41f30a5c3f1ad1a.jpg)  
Figure 2. SFI image process generation

Before performing AES-GCM to encrypt an area, we calculate the initialization vector (IV) as:

IV = nonce + area index

The tool partitions the firmware image into several encrypted parts corresponding to different memory areas.

These encrypted parts appended to their corresponding descriptors (the unencrypted descriptive header generated by the tool) are called areas.

These areas can be of different types:

• 'F' for a firmware area (a regular segment in the input firmware) • 'C' for a configuration area (used for option-byte configuration) • 'P' for a pause area   
• 'R' for a resume area.

Areas 'P' and 'R' do not represent a real firmware area, but are created when an SFI image is split into several parts, which is the case when the global size of the SFI image exceeds the allowed RAM size predefined by the user during the SFI image creation.

The STM32 Trusted Package Creator overview below (Figure 3) shows the 'RAM size' input as well as the 'Continuation token address' input, which is used to store states in flash memory during SFI programming.

![](images/f56c0d205c88d2ce636f2dfd969954d22c63f0d0c6d36ac340b893b27c16c007.jpg)  
Figure 3. RAM size and CT address inputs used for SFI

Figure 4 shows the specifics of these new areas compared to a regular SFI area.

Fure . ' and are secifi versus a rgular   

<table><tr><td>Area format</td><td>New Pause Area</td><td>New Resume Area</td></tr><tr><td>Type (F&#x27;, &#x27;M&#x27;, &#x27;C)</td><td>Type &#x27;P&#x27;</td><td>Type &#x27;R&#x27;</td></tr><tr><td>Version</td><td>Version</td><td>Version</td></tr><tr><td>Index</td><td>Index</td><td>Index</td></tr><tr><td>Size</td><td>Size = 0</td><td>Size = 0</td></tr><tr><td>Address</td><td>Address of CT</td><td>Address of CT</td></tr><tr><td>Total Nb of areas</td><td>Total Nb of areas</td><td>Total Nb of areas</td></tr><tr><td>Tag</td><td>Tag</td><td>Tag</td></tr><tr><td>Encrypted Area Content - Firmware -Module - Configuration</td><td></td><td></td></tr></table>

A top-level image header is generated and then authenticated.The tool performs AES-GCM with authentication only (without encryption), using the SFI image header as an AAD, and the nonce as IV.

An authentication tag is generated as output.

# Note:

To prepare an SFI image from multiple firmware files, make sure that there is no overlap between their segments, otherwise an error message appears (Figure 5).

![](images/68459ad8299ea59e9aa0dabd65872e11658f58562e54e09672bdcc83b4b05a0d.jpg)  
Figure 5. Error message when firmware files with address overlaps are used

Also, all SFI areas must be located in flash memory, otherwise the generation fails, and the following error message appears (Figure 6).

![](images/a2d6e593f8dabba5c8314bf97f75d45753c5995031c205d1e03c55b5aff607a6.jpg)  
Figure 6. Error message when a SFI area address is not located in flash memory

The final output from this generation process is a single file, which is the encrypted and authenticated firmware in ".sfi" format. The SFI format layout is described in Figure 7.

![](images/2af77e106710b4fb151d25e2a8a5270493b5b392bb3c79c7f0bfef8e53b8c963.jpg)  
Figure 7. SFI format layout

When the SFI image is split during generation, areas 'P' and 'R' appear in the SFI image layout, as in the following example Figure 8.

![](images/0ad7e03a6ebf0e92ba92e5db397fd3270ebfe6c42b845915f8e59afdb9cd0efc.jpg)  
Figure 8. SFI image layout in case of split

# 2.3 SFIx generation process

In addition to the SFI preparation process mentioned in the previous section, two extra areas are added in the SFI image for the SFlx preparation process:

'E' for an external firmware area _ 'K' for a key area (used for random keys generation)

The 'K' area is optional and it can be stored in the area 'F'.

# Area E

The area 'E' is for external flash memory. It includes the following information at the beginning of an encrypted payload:

OTFD region_number (uint32_t): 0...3: OTFD1 (STM32H7A3/7B3 and STM32H7B0, STM32H723/333 and STM32H725/335, STM32L5, and STM32U5) 4...7: OTFD2 (STM32H7A3/7B3 and STM32H7B0, STM32H723/333, STM32H725/335, and STM32U5)

OTFD region_mode (uint32_t) bit [1:0]:   
00: instruction only AES-CTR) 01: data only (AES-CTR) 10: instruction + data (AES-CTR) 11: instruction only (EnhancedCipher)

OTFD key_address in internal flash memory (uint32_t).

After this first part, area 'E' includes the firmware payload (as for area 'F'). The destination address of area 'E' is in external flash memory (0x9... / 0x7...).

# Area K

The area 'K' triggers the generation of random keys. It contains N couples; each one defines a key area as follows:

• The size of the key area (uint32_t) • The start address of the key area (uint32_t): address in internal flash memory.

Example of an area 'K':

0x00000010, 0x0C020000   
0x00000010, 0x08000060

There are two key areas:

The first key area starts at 0x08010000 with size = 0x80 (8 x 128-bit keys) The second key area starts at 0x08010100 with size 0x20 (256-bit key).

The STM32 Trusted Package Creator overview (Figure 9) shows the RAM size input for SFlx image generation, and also the 'Continuation token address' input, which is used by SFlx to store states in external/internal flash memory during SFlx programming.

The 'Continuation token address' is mandatory due to the image generation that adds areas P and R whatever be the configuration.

![](images/ba3db9159a9b008ef503f66ecf2887b590116b172f07e5e429714bfd7fdc018b.jpg)  
Figure 9. RAM size and CT address inputs used for SFlx

Note:

To prepare an SFlx image from multiple firmware files, make sure that there is no overlap between their segments (Intern and extern), otherwise an error message appears as same as in the SFI use case.

The final output from this generation process is a single file, which is the encrypted and authenticated internal/external firmware in ".sfix" format. The SFIx format layout is described in Figure 10.

![](images/7d06b01e4a3363f905907f51f16f873e3b095afe8a6a8d73ed5b9a9c6e8d4f76.jpg)  
Figure 10. SFIx format layout

When the SFIx image is split during generation, the areas 'P' and 'R' appear in the SFIx image layout, as in the example below Figure 11.

![](images/2e2038a774093987b2535ae292355513bbcb24bb87215f46da6d9b3b312ff2b7.jpg)  
Figure 11. SFIx image layout in case of split.

# 2.4 SSP generation process

SSP is an encryption format that transforms customer secret files into encrypted and authenticated firmware using an AES-GCM algorithm with a 128-bit key. The SSP preparation process used in the STM32 Trusted Package Creator tool is shown in Figure 12.

![](images/4a8eca08eb4ab40c519fa77cfe25c4a9a3f5d4bddae52a3cc81a0389bacfe576.jpg)  
Figure 12. SSP preparation mechanism

An SSP image must be created before SSP processing. The encrypted output file follows a specific layout that guarantees a secure transaction during transport and decryption based on the following inputs:

Secret file: This 148-byte secret file must fit into the OTP area reserved for the customer. There is no tool or template to create this file. RMA password: This password is chosen by the OEM. It is part of the secret file and is placed as the first 4-byte word. To make RMA password creation easier and avoid issues, the STM32 Trusted Package Creator tool add sit directly at the beginning of the 148-byte secret file. o Encryption key: AES encryption key (128 bits). Encryption nonce: AES nonce (128 bits). OEM firmware key: This is the major part of the secure boot sequence. Based on ECDSA verification, the key is used to validate the signature of the loaded binary.

The first layout part (SSP magic, protocol version, ECDSA public key, secret size) is used as additional authenticated data (AAD) to generate the payload tag. This is checked by the ROM code during decryption.

Table 2. SSP preparation inputs   

<table><tr><td rowspan=1 colspan=1>Input</td><td rowspan=1 colspan=1>Size (bytes)</td><td rowspan=1 colspan=1>Content</td></tr><tr><td rowspan=1 colspan=1>SSP magic</td><td rowspan=1 colspan=1>4</td><td rowspan=1 colspan=1>&#x27;SSPP: magic identifier for SSP Payload</td></tr><tr><td rowspan=1 colspan=1>SSP protocol version</td><td rowspan=1 colspan=1>4</td><td rowspan=1 colspan=1>Can be used to indicate how to parse the payload, ifpayload format changes in future</td></tr><tr><td rowspan=1 colspan=1>OEM ECDSA public key</td><td rowspan=1 colspan=1>64</td><td rowspan=1 colspan=1>OEM ECDSA public key</td></tr><tr><td rowspan=1 colspan=1>OEM secret size</td><td rowspan=1 colspan=1>4</td><td rowspan=1 colspan=1>Size of OEM secrets, in bytes</td></tr><tr><td rowspan=1 colspan=1>Payload tag</td><td rowspan=1 colspan=1>16</td><td rowspan=1 colspan=1>Cryptographic signature of all fields above, to ensuretheir integrity.</td></tr><tr><td rowspan=1 colspan=1>Encrypted OEM secrets</td><td rowspan=1 colspan=1>152</td><td rowspan=1 colspan=1>Encrypted OEM secrets. 152 is given by previous field.</td></tr></table>

This encrypted file is automatically generated by the STM32 Trusted Package Creator tool.

![](images/adbe3ce81c31558497cf1f1ab4971d674226e48591d8aaaf2fd10f3b7fa7d9c6.jpg)  
Figure 13. Encryption file scheme

# 2.5 STM32 Trusted Package Creator tool in the command-line interface

This section describes how to use the STM32 Trusted Package Creator tool from the command-line interface to generate SFl/SFIx image. The available commands are listed in Figure 14.

![](images/d1745ff3c62f64770eb76ab0403b0e5145469e3fa25221661df3564c772610cf.jpg)  
Figure 14. STM32 Trusted Package Creator tool - SFI preparation options

# 2.5.1 Steps for SFI generation (CLI)

To generate an SFI/SFIx image in CLI mode, the user must use the "-sfi, --sfi" command followed by the appropriate inputs. Inputs for the "sfi" command are:

-devid, --deviceid

Description: Specifies devicelD. If this option is not used, P and R areas are generated by default for all devices.

Syntax: -devid <device_id> <device_id>: Device ID -fir, --firmware

Description: Adds an input firmware file (supported formats are Bin, Hex, Srec, and ELF).   
This option can be used more than once to add multiple firmware files.

Syntax: -fir <Firmware_file> [<Address>] <Firmware_file>: Firmware file.

[<Address>]: Used only for binary firmware.

-firx, --firmwx

Description: Add an input for an external firmware file. Supported formats are Bin, Hex, Srec, and ELF. This option can be used more than once to add multiple firmware files.

Syntax: -firx <Firmware_file> [<Address>] [<Region_Number>] [<Region_Mode>] [<key_address>] <Firmware_file>: Supported external firmware files are ELF HEX SREC BIN.

[<Aes> Only  he cas Bput f n ys).

<Region_Number> : Only in the case of BIN input file (in any base): [0:3]: OTFD1 (STM32H7A3/7B3, STM32H7B0, or STM32L5), [4:7]: OTFD2 (STM32H7A3/7B3 and STM32H7B0 case).

<Region_Mode>: Only in the case of BIN input file (in any base), only two bits [0:1] where

00: instruction only (AES-CTR)   
01: data only (AES-CTR)   
10: instruction + data (AES-CTR)   
11: instruction only (EnhancedCipher)

<key_address>: Only in the case of BIN input file (in any base), random key values in internal flash memory.

-k, -key

Description: Sets the AES-GCM encryption key.

Syntax: -k <Key_file>< Key _file>: A 16-byte binary file.-n, --nonce

Description: Sets the AES-GCM nonce.

Syntax: -n <Nonce_file> <Nonce _file> A 12-byte binary file.

-V, --ver

Description: sets the image version.

Syntax: -v <lmage_version> <Image_version> : A value between 0 and 255 in any base.

-ob, --obfile

Description: Provides an option bytes configuration file.

The option bytes file field is only mandatory for SFI applications (first install) to allow option bytes programming, otherwise it is optional.

Only csv (comma separated value) file format is supported as input for this field, it is composed from two vectors: register name and register value respectively.

Note:

The number of rows in the CSV file is product dependent (refer to the example available for each product). For instance there are nine rows for all STM32H7 products, with the last row "reserved", except for dual-core devices. It is important to neither change the order of, nor delete, rows.

Example: for STM32H75x devices, nine option byte registers must be configured, and they correspond to a total of nine lines in the csv file (Figure 15).

Syntax: -ob <CSv_file> <CSV_file >: A csv file with nine values.

1 FOPTSR_PRG, Ox1026AAD0   
2 FPRAR_PRG_A,Ox81000200   
3 FPRAR PRG B,Ox81000200   
4 FSCAR_PRG_A,Ox81000200   
5 FSCAR PRG B, Ox81000200   
6 FWPSN PRG A, OxFFFFFFFF   
7 FWPSN_PRG B, OxFFFFFFFF   
8 FBO0T7_PRG,0x24000800   
9 RESERVED,0x10000810

-m, --module -rs, --ramsize

Description: Defines the available ram size (in the case of SFI)

Syntax: -rs <Size> < Size >: RAM available size in bytes

# Note:

The maximum RAM size of each device is mentioned in the descriptor. For example the maximum RAM size of the STM32WL is 20 Kbytes.

-ct, --token

Description: Continuation token address (in the case of SFl)

Syntax: -ct <Address>

< Address > continuation token flash memory address

-0, --outfile

Description: Sets the output SFI file to be created.

Syntax: -0 <out_file>

<out_file > : the SFI file to be generated (must have the ".sfi" extension).

Example of SFI generation command using an ELF file:

STM32TrustedPackageCreator_CLI.exe --sfi -fir firm.axf -k encyption_key.bin -n nonce.bin -ob SFI_OB_U5_4M.csv -v 1 -rs Ox55500 -devid Ox481 -0 out.sfi

The result of the previous command is shown in Figure 16.

# Figure 16. SFI generation example using an ELF file

C:\CubeProg\STM32CubeProgrammer_2.14.0_Signed\bin   
λSTM32TrustedPackageCreator_cLI.exe -sfi -fir firm.axf -k encyption_key.bin -n nonce.bin   
-ob SFI_OB_U5_4M.cSv -v 1 -rs 0x55500 -devid 0x481 -0 out.sfi STM32 Trusted Package Creator v2.14.0   
SFI generation SucCESS DT48249V3

# 2.5.2 Steps for SSP generation (CLI)

To generate an SSP image in CLI mode, the user must use the "-ssp, --ssp" command followed by the appropriate inputs.

Inputs for the "ssp" command are:

-ru, --rma_unlock   
Description: RMA unlock password   
Syntax: -ru <RMA_Unlock>   
<RMA_Unlock> : Hexadecimal value Ox0000 to Ox7FFF   
-rr, --rma_relock   
Description: RMA relock password   
Syntax: -rr <relock_value>   
<relock_value> : Hexadecimal value Ox0000 to Ox7FFF   
-b, --blob   
Description: Binary to encrypt   
Syntax: -b <Blob>   
<Blob> : Secrets file of size 148 bytes   
-pk, --pubk   
Description: OEM public key file   
Syntax: -pk <PubK.pem>   
<PubK> : pem file of size 178 bytes   
-k, -key   
Description: AES-GCM encryption key   
Syntax: -k <Key_File>   
<Key_File> : Bin file, its size must be 16 bytes   
-n, --nonce   
Description: AES-GCM nonce   
Syntax: -n <Nonce_File>   
<Nonce_File>  Bin file, its size must be 16 bytes   
-o, --out   
Description: Generates an SSP file   
Syntax: -out <Output_File.ssp>   
<Output_File> : SSP file to be created with (extension .ssp)   
If all input felds are valdated, an  fle s generated in the directory pathaleady

mentioned in the "-o" option.

# Example SSP generation command:

STM32TrustedPackageCreator_CLI -ssp -ru Ox312 -rr OxECA

-b "C:\sSP\secrets\secrets.bin"

-pk "C:\SSP\OEMPublicKey.pem" -k "C: \SSP\key.bin"

-n "C:\ssP\nonce.bin" - "C:\out.ssp"

Once the operation is done, a green message is displayed to indicate that the generation was finished successfully. Otherwise, an error occurred.

![](images/7db61007dfc43fdb6067b80c3cc3762b80785edfc07ca3c41574362bf0121675.jpg)  
Figure 17. SSP generation success

# 2.6 Using the STM32 Trusted Package Creator tool graphical user interface

The STPC is also available in graphical mode. This section describes its use.

# 2.6.1 SFI generation using STPC in GUI mode

Figure 18 shows the graphical user interface tab corresponding to SFI generation.

![](images/8cfcc2482d9c74a2622b8b65dce3e5cf25d1ef924737ea3ebfaa9a2b142b3fac.jpg)  
Figure 18. SFI generation Tab

To generate an SFI image successfully from the supported input firmware formats, the user must fill in the interface fields with valid values.

# SFI GUI tab fields

Firmware files:

The user needs to add the input firmware files with the "Add" button.

If the file is valid, it is appended to the "input firmware files" list, otherwise an error message box appears to notify the user that either the file could not be opened, or the file is not valid.

Clicking on "input firmware file" causes related information to appear in the "Firmware information" section (Figure 19).

![](images/91cb93b67d669e564c36bc4aaf4fe10a8c9291bf9555a6a27d21ffc2fb98c008.jpg)  
Figure 19. Firmware parsing example

Encryption key and nonce file:   
The encryption key and nonce file are selected by entering their paths (absolute or relative), or by selecting them with the "Open" button. Notice that sizes must be respected (16 bytes for the key and 12 bytes for the nonce).   
Option bytes file:   
The option bytes file is selected the same way as the encryption key and nonce. Onl csv files are supported.

Note:

STM32CubeProgrammer v2.8.0 and later provide one option byte file example for each product.

It is located in the directory: STM32CubeProgrammerlvx.x.x\bin\SFI_OB_CSV_FILES

The option bytes are described in the product reference manual.

In the case of customization of a provided example file, care must be taken not to change the number of rows, or their order.

Image version:   
Choose the image version value of the SFI under generation within this interval: [0..255].   
Output file:   
Sets the folder path in which the SFI image is to be created. This is done by enterin the folder path (absolute or relative) or by using the "Select folder" button.

# Note:

By using the "Select folder" button, the name "out.sfi" is automatically suggested. This car be kept or changed.

'Generate SFI' button:   
Once all fields are filled in properly, the "Generate SFl" button becomes enabled. The user can generate the SFI file by a single click on it.   
If everything goes well, a message box indicating successful generation appears (Figure 20) and information about the generated SFI file is displayed in the SFI information section.

![](images/be151ad28de2e965679831f4f43bc42d75ec41437a59efd02173bfb89053e948.jpg)  
Figure 20. SFI successful generation in GUI mode example

# 2.6.2 SFIx generation using STPC in GUI mode

Figure 21 shows the graphical user interface tab corresponding to SFIx generation.

![](images/9e5e72605612ee2c14ba7a2ac6772ef37fc8d630110c9a90715ccf4118a9c01b.jpg)  
Figure 21. SFIx generation Tab

To generate an SFlx image successfully from the supported input firmware formats, the user must fill in the interface fields with valid values.

# SFIx GUI tab fields

Firmware files: The user needs to add the input firmware files with the "Add" button. If the file is valid, it is appended to the "input firmware files "list, otherwise an error message box appears to notify the user that either the file could not be opened, or the file is not valid. Clicking on "input firmware file" causes information related information to appear in the "Firmware information" section (Figure 22).

![](images/955b356402c2bfd40d54f17cafc5a3fa8ed7d626b73005deba4118b287f427c3.jpg)  
Figure 22. Firmware parsing example

As is the case for the SFI use case, once all fields are filled in properly, the "Generate SFlx" button becomes enabled. The user can generate the SFlx file by a single click on it. If everything goes well, a message box indicating successful generation appears (Figure 23) and information about the generated SFlx file is displayed in the SFIx information section.

![](images/a5ef47da2e150b467cd8b723a4b43c1afde152db52b0c43379488f2ab651352e.jpg)  
Figure 23. SFIx successful generation in GUI mode example

# 2.6.3 SSP generation using STPC in GUI mode

Figure 24 shows the SSP generation graphical user interface tab.

![](images/7c9bad4eff90816e1e84e0b17700fd361486d017c9f6a390c7277bb4947d719e.jpg)  
Figure 24. SSP generation tab

To generate an SSP image successfully from the supported firmware input formats, the user must fill in the interface fields with valid values.

# SSP GUI tab fields

RMA Lock: Unlock password, hexadecimal value from Ox0000 to Ox7FFF

RMA Relock: Relock password, hexadecimal value from Ox0000 to Ox7FFF

Secrets file: Binary file of size 148 bytes to be encrypted. Can be selected by entering the file path (absolute or relative), or by selection with the Open button.

Encryption key and nonce files: The encryption key and nonce file can be selected by entering their paths (absolute or relative), or by selection with the Open button. Notice that sizes must be respected (16 bytes for the key and 12 bytes for the nonce).

OEM public key file: 178-byte .pem file.

Output SSP file: Select the output directory by entering the SSP file name to be created with a .ssp extension.

When allfields are properly filled in, the user can start the generation by clicking on the Generate SsP button (the button becomes active).

![](images/36c4b8f4afbe9711085188d1c7e8d4631b2dbecc8182fd55efdb5fd33fdc811e.jpg)  
Figure 25. SSP output information

When the generation is complete, SSP information is available in the SSP overview section.

− File name: SSP output file name.   
• Type: SSP format. Size: indicates the generated file size including all data fields.

# 2.6.4 Settings

The STPC allows generation to be performed respecting some user-defined settings. The settings dialog is displayed by clicking the settings icon (see Figure 26) in the tool bar or in the menu bar by choosing: Options -> settings.

![](images/7cb6fb199d3acddd378e98175b4f0dfc2221b96564eebc6abfd419b3eb64de35.jpg)  
Figure 26. Settings icon and settings dialog box

Settings can be performed on:

Padding byte:   
When parsing Hex and Srec files, padding can be added to fill gaps between close segments to merge them and reduce the number of segments. The user might choose to perform padding either with OxFF (the default value) or Ox00.   
Settings file:   
When checked, a "settings.ini" file is generated in the executable folder. It saves the application state: window size and field contents.   
Log file:   
When checked, a log file is generated in the selected path.

# 2.6.5 Log generation

A log can be visualized by clicking the "Iog" icon in the tool bar or menu bar: Options-> log.

Figure 27 shows a log example:

![](images/f87889d54930453b858741c761dd081381f1ae1d3a182ead01ad51f0065f9ca3.jpg)  
Figure 27. Log example

# Encrypted firmware (SFI/SFIx) programming with STM32CubeProgrammer

STM32CubeProgrammer is a tool for programming STM32 devices through UART, USB, SPI, CAN, I2C, JTAG, and SWD interfaces. So far, programming via JTAG/SWD is only supported with an ST-LINK probe.

The STM32CubeProgrammer tool currently also supports secure programming of SFI images using UART, USB, SPI, JTAG/SWD interfaces, and SFIx using only JTAG/SWD interfaces. The tool is currently available only in CLI mode, it is available free of charge from www.st.com.

# 3.1 Chip certificate authenticity check and license mechanism

The SFI solution was implemented to provide a practical level of IP protection chain from the firmware development up to flashing the device, and to attain this objective, security assets are used, specifically device authentication and license mechanisms.

# 3.1.1 Device authentication

The device authentication is guaranteed by the device's own key.

In fact, a certificate is related to the device's public key and is used to authenticate this public key in an asymmetric transfer: the certificate is the public key signed by a Certificate Authority (CA) private key. (This CA is considered as fully trusted).

This asset is used to counteract usurpation by any attackers who could substitute the public key with their own key.

# 3.1.2 License mechanism

One important secure flashing feature is the ability of the firmware provider to control the number of chips that can be programmed. This is where the concept of licenses comes in to play. The license is an encrypted version of the firmware key, unique to each device and session. It is computed by a derivation function from the device's own key and a random number chosen from each session (the nonce).

Using this license mechanism, the OEM is able to control the number of devices to be programmed, since each license is specific to a unique chip, identified by its public key.

# License mechanism general scheme

When a firmware provider wants to distribute new firmware, they generate a firmware key, and use it to encrypt the firmware.

When a customer wants to download the firmware to a chip, they send a chip identifier to the provider server, STM32HSM, or any provider license generator tool,

which returns a license for the identified chip. The license contains the encrypted firmware key, and only this chip can decrypt it.

# License distribution

There are many possible ways for the firmware provider to generate and distribute licenses.

ST solution is based on STM32HSM: a standalone chip in a smartcard form factor that could be programmed during the SFI preparation then used on the device production line. This solution is securing end to end transport of the firmware. Only the STM32 is capable to authenticate and decrypt the firmware. In addition, an ST solution based on STM32HSM is protecting device production against cloning.

Other solutions could be considered and STMicroelectronics, through its partnership program, is offering programming services. Find yours from the following link: Global Services from Partners - STMicroelectronics.

# STM32HSM programming by OEM for license distribution

Before an OEM delivers an STM32HSM to a programming house for deployment as a license generation tool for programming of relevant STM32 devices, some customization of the STM32HSM must be done first.

The STM32HSM needs to be programmed with all the data needed for the license scheme deployment. In the production line, a dedicated APl is available for STM32HSM personalization and provisioning.

This data is as follows:

The counter: the counter is set to a maximum value that corresponds to the maximum number of licenses that can be delivered by the STM32HSM. It aims to prevent overprogramming.   
It is decremented with each license delivered by the STM32HSM.   
No more licenses are delivered by the STM32HSM once the counter is equal to zero. The maximum counter value must not exceed a maximum predefined value, which depends on the STM32HSM used.   
The firmware key: the key size is 32 bytes. It is composed of two fields: the   
initialization vector field (IV) and the key field, which are used for AES128-GCM firmware encryption.   
Both fields are 16 bytes long, but the last 4 bytes of the IV must be zero (only 96 bits of IV are used in the AES128-GCM algorithm).   
Both fields must remain secret; that is why there are encrypted before being sent to the chip.   
The key and IV remains the same for all licenses for a given piece of firmware. However, they must be different for different firmware or different versions of the same firmware. As a consequence, the STM32HSM must be changed.   
The firmware identifier: allows the correct STM32HSM to be identified for a given firmware.   
The personalization data: this is specific to each MCU and delivered inside the TPC directory. More info about personalization data in Section 4.3.5: Performing   
STM32HSM programming for license generation using STPC (CLI mode).

The STM32HSM must be in "OPERATIONAL STATE" (locked) when shipped by the OEM to guarantee the OEM's data confidentiality and privacy.

STMicroelectronics provides the tools needed to support SFI/SFIx via STM32HSM. In fact, STM32HSM programming is supported by the STM32 Trusted Package Creator tool. Figure 28 shows the GUI for STM32HSM programming in the STPC tool.

![](images/f4278e463c642e9a7f0e64e469fdd9ec9aef22b3bbdc1677453f617e140a4bbb.jpg)  
Figure 28. STM32HSM programming GUI in the STPC tool

During SFI install, STM32CubeProgrammer communicates with the device to get the chip certificate, upload it into the STM32HSM to request the license. Once the license is generated by the STM32HSM, it gives it back to the STM32 device.

# 3.2 Secure programming using a bootloader interface

# 1 STM32CubeProgrammer for SFI using a bootloader interface

For SFI programming, the STM32CubeProgrammer is used in CLI mode (the only mode so far available) by launching the following command:

-sfi, --sfi

Syntax: -sfi protocol=<Ptype> <file_path> <licenseFile_path>

[<protocol=Ptype>] : Protocol type to be used: static/live Only a static protocol is supported so far

Default value static

<lpah   fil   p

[hsm=0|1] : Set a user option for STM32HSM use value in {0 (do not use STM32HSM), 1 (use STM32HSM)} Default value : hsm = 0

<lic_path|slot=slotID>: Path to the SFI license file (f hsm = 0) or reader slot ID if STM32HSM is used (hsm = 1)

[During th SFI process, the generated license can be used multiple times with the same MCU, without the need of an STM32HSM card.

Example using the UART bootloader interface:

To use an STM32HSM, the command is:

STM32_Programmer.exe -C port=COM1 br=115200 -sfi "C:\SFI\data.sfi" hsm=1 slot=1

To use a license file, the command is:

STM32_Programmer.exe -C port=COM1 br=115200 -sfi "C:\SFI\data.sfi" --sfi hsm=0 "C:\SFI\license.bin"

This command allows secure installation of firmware "data.sfi"into a dedicated flash memory address.

# .2.2 STM32CubeProgrammer for SSP via a bootloader interface

In this part, the STM32CubeProgrammer tool is used in CLI mode (the only mode available so far for secure programming) to program the SsP image already created with STM32 Trusted Package Creator. STM32CubeProgrammer supports communication with STMicroelectronics STM32HSMs (hardware secure modules based on smartcard) to generate a license for the connected STM32 MPU device during SSP install.

The SSP flow can be performed using both USB or UART interfaces (not the ST-LINK interface).

STM32CubeProgrammer exports a simple SSP command with some options to perform the SSP programming flow.

-ssp, --ssp

Description: Programs an SSP file

Syntax: -ssp <ssp_file_path> <ssp-fw-path> <hsm=0|1> <license_path|slot=slotID>

- <ssp_file_path>: SSP file path to be programmed, bin, or ssp extensions - <hsm=0|1>: Set user option for STM32HSM use (do not use STM32HSM / use STM32HSM) Default value: hsm=0

- <license_path|slot=slotID>: Path to the license file (if hsm=0), Reader slot ID if STM32HSM is used (if hsm=1)

Example using USB DFU bootloader interface:

STM32_Programmer_CLl.exe -c port=usb1 -ssp "out.ssp" "tf-a-ssp-stm32mp157fdk2-trusted.stm32" hsm=1 slot=1

Note:

All SSP traces are shown on the output console.

![](images/f6dc7e6c753f1facd6711552b3e83c66b03e3cc25fcce2f294ed9c217ecaace5.jpg)  
Figure 29. SSP installation success

If there is any faulty input, the SSP process is aborted, and an error message is displayed to indicate the root cause of the issue.

# 3.2.3 STM32CubeProgrammer get certificate via a bootloader interface

To get the chip certificate, STM32CubeProgrammer is used in CLI mode by launching the following command:

-gc, --getcertificate

Syntax: -gc <file_path>

Example using the UART bootloader interface:

STM32_Programmer.exe -c port=COM1 -gc "C:\Demo_certificate.bin"

This command allows the chip certificate to be read and uploaded into the specified file: "C:\Demo_certificate.bin"

The execution results are shown in Figure 30.

# Figure 30. Example of getcertificate command execution using UART interface

Requesting Chip Certificate from connected device. ..   
Serial Port CoM1 is successfully opened.   
Activating device: OK   
Port configuration: parity.= none. baudrate = 115200, data-bi t = 8, stop-bit = 1.000000, flow-control= off   
Chip ID: 0x450   
BootLoader version: 3.1 Certificate File C:\Demo_certificate.bin File already exist. It wili be overwritten.   
Get Certificate done successfully :Writing data to file C:\Demo_certificate.bin   
writing chip certificate to file C:\Demo_certificate.bin finished successfully

# 3.3 Secure programming using the JTAG/SWD interface

# 3.3.1 SFI/SFIx programming using JTAG/SWD flow

It is also possible to program the SFI/SFIx image using the JTAG interface. Here the readout protection mechanism (RDP level 1) cannot be used during SFI/SFIx as user flash memory is not accessible after firmware chunks are written to RAM through the JTAG interface.

The whole process happens in RDP level O. In the case of SFIx programming the code is protected by the OTFDEC encryption.

SFI via debug interface is currently supported for STM32H753XI, STM32H7A3/7B3 and STM32H7B0, STM32H723/333 and STM32H725/335, and STM32L5 devices.

SFIx via debug interface is currently supported for STM32H7A3/7B3 and STM32H7B0, STM32H723/733, STM32L5, and STM32U5 devices.

For these devices, there is around 1 Mbyte of RAM available, with 512 Kbytes in main SRAM. This means that the maximum image size supported is 1 Mbyte, and the maximum area size is 512 Kbytes.

To remedy this, the SFl/SFIx image is split into several parts, so that each part fits into the allowed RAM size.

An SFI/SFIx is then performed. Once allits SFI/SFIx parts are successfully instaled, the global SFI/SFIx image install is successful.

Other limitations are that security must be left activated in the configuration area if there is a PCROP area. In the case of STM32L5 and STM32U5 devices, STM32CubeProgrammer sets the RDP Level on 0.5.

The SFI flow for programming through JTAG is described in Figure 31.

![](images/2723b97ac4520315addd84b6581ced7720af689cdce8f28c0d4ebd7676852687.jpg)  
Figure 31. SFI programming by JTAG/SWD flow overview (monolithic SFI image example)

# 3.3.2 STM32CubeProgrammer for secure programming using JTAG/SWD

The only modification in the STM32CubeProgrammer secure command syntax is the connection type that must be set to "jtag" or "swd", otherwise all secure programming syntax for supported commands is identical.

Note:

Using a debug connection "HOTPLUG" mode must be used with the connect command.

The result of this example is shown in Figure 32.

![](images/35c3aa616861c6bb94bd6db2eddb65cf3529fb8046c9f9c54b5c777346d59f2c.jpg)  
Figure 32. Example of getcertificate command using JTAG

# 3.4 Secure programming using bootloader interface (UART/I2C/SPI/USB)

It is also possible to program the SFl/SFIx image using the bootloader interface (UART/I2C/SPI/USB). FDCAN is not supported by STLINK-V3.

The whole process happens in RDP level 0.5. In the case of SFIx programming the code is protected by the OTFDEC encryption.

SFI via the bootloader interface (UART/I2C/SPI/USB) is currently supported for STM32L5 devices. It needs to load an external loader using the -elbl command in the SRAM.

For STM32L5 devices, 1 Mbyte of SRAM is available, with 512 Kbytes in the main SRAM. This means that the maximum image size supported is 1 Mbyte, and the maximum area size is 512 Kbytes.

To remedy this, the SFI/SFIx image is split into several parts, so that each part fits into the allowed SRAM size.

An SFI/SFIx is then performed. Once allits SFI/SFIx parts are successfully installed, the global SFI/SFIx image install is successful.

# SFI example

STM32_Programmer_CLI.exe -c port=usbl -sfi out.sfix hsm=0 license.bin -rsse RSSe\L5\enc_signed_RSSe_sfi_bl.bin

# SFIx example

STM32_Programmer_CLI.exe -C port=usb1 -elbl MX25LM51245G_STM32L552E-EVAL-SFIX-BL.stldr -sfi out.sfix hsm=0 license.bin -rsse RSSe\L5\enc_signed_RSSe_sfi_bl.bin

# Example of SFI programming scenario

# 4.1 Scenario overview

The actual user application to be installed on the STM32H753XI (or STM32L5) device makes "print f" packets appear in serial terminals. The application was encrypted using the STPC.

The OEM provides tools to the CM to get the appropriate license for the concerned SFI application.

# 4.2 Hardware and software environment

For successful I programming, some hardware nd software prerequisites apply:

STM32H743I-EVAL board   
C STM32H753XI with bootloader and RSS programmed   
• RS-232 cable for SFI programming via UART   
• Micro-B USB for debug connection   
o PC running on either Windows®, Linux® Ubuntu® or Fedora®, or macOS® STM32 Trusted Package Creator v0.2.0 (or greater) package available from www.st.com STM32CubeProgrammer v0.4.0 (or greater) package available from www.st.com

Note:

Refer to [4] or [5] for the supported operating systems and architectures.

# 4.3

# Step-by-step execution

# 4.3.1

# Build OEM application

OEM application developers can use any IDE to build their own firmware.

# Performing the option byte file generation (GUl mode)

The STM32 Trusted Package Creator tool GUI presents an SFI OB tab to generate an option bytes Csv file with a custom option byte value.

To generate an SFI CSV option bytes file, the user must:

1. Select the concerned product.   
2. Fill the option bytes fields with desired values.   
3. Select the generation path.   
4. Click on the Generate OB button.

![](images/2b299a0677e1864e43cd539e0d36e0dd3211fa50f1d680cf51292ef9d9f7a5e5.jpg)  
Figure 33. STM32Trusted Package Creator SFI OB GUI

# 4.3.3 Perform the SFI generation (GUI mode)

To be encrypted with the STM32 Trusted Package Creator tool, OEM firmware is provided in AXF format in addition to a CSV file to set the option bytes configuration. A 128-bit AES encryption key and a 96-bit nonce are also provided to the tool. They are available in the "SFl_ImagePreparation" directory.

An simage is then generated (out.

# Note:

STM32CubeProgrammer v2.8.0 and later provide one option byte file example for each product.

It is located in the directory: STM32CubeProgrammerlvx.x.x\bin\SFI_OB_CSV_FILES

The option bytes are described in the product reference manual.

In the case of customization of a provided example file, care must be taken not to change the number of rows, or their order.

# Note:

If you want to reopen the Device using the Debug Authentication mechanism, a DA ObKey file must be included in the SFl image, otherwise the device becomes inaccessible.

Figure 34 shows the STPC GUI during the SFI generation.

![](images/d624879dc66417abb784c28569ceec0b77b9e9c3346e884356d63a6d107d71fc.jpg)  
Figure 34. STPC GUI during SFI generation

# 4.3.4 Performing STM32HSM programming for license generation using STPC (GUI mode)

The OEM must provide a license generation tool to the programming house to be used for license generation during the SFI install process.

In this example, STM32HSMs are used as license generation tools in the field. See Section 3.1.2: License mechanism for STM32HSM use and programming.

Figure 35 shows an example for STM32HSM programming by OEM to be used for SFI install.

The maximum number of licenses delivered by the STM32HSM in this example is 1000.

This example uses STM32HSM-V2, and is also valid for STM32HSM-V1 when the 'version' field is set accordingly. The STM32HSM version can be identified before performing the programming operation by clicking the Refresh button to make the version number appear in the 'version' field.

The STM32 Trusted Package Creator tool provides all personalization package files ready to be used on SFI/SFIx and SSP flows. To get al the supported packages, go to the PersoPackages directory residing in the tool's install path.

Each file name starts with a number, which is the product ID of the device. Select the correct one.

To obtain the appropriate personalization data, you first need to obtain the product ID:

Use the STM32CubeProgrammer tool to launch a Get Certificate command to   
generate a certificate file containing some chip security information, bearing in mind that this command is only recognized only for devices that support the security feature: STM32_Programmer_CLI -c port=swd -gc "certificate.bin"   
A file named "certificate.bin" is created in the same path of the   
STM32CubeProgrammer executable file.   
Open the certificate file with a text editor tool, then read the eight characters from the header, which represents the product ID.   
For example:   
When using the STM32H7 device, you find: 45002001.   
When using the STM32L4 device, you find: 46201002.

Once you have the product ID, you can differentiate the personalization package to be used on the STM32HSM provisioning step respecting the following naming convention:

ProdcutID_FlowType_LicenseVersion_SecurityVersion.enc.bin

For example: 47201003_SFI._01000000_00000000.enc.bin

Based on this name we can retrieve the associated information:

• Product ID = 47201003 for STM32L5 devices (0x472 as device ID).   
• Type = SFI   
• License version = 01 (Large endian) Security version = 0

![](images/ed260f35ebf18ac882241a0d1927cf5ae59c1fe35ec45638d7741461d140a3d5.jpg)  
Figure 35. Example of STM32HSM programming using STPC GUI

# Note:

When using STM32HSM-V1, the "Personalization data file" field is ignored when programming starts. It is only used with STM32HSM-V2.

When the card is successfully programmed, a popup window message "HSM successfully programmed" appears, and the STM32HSM is locked. Otherwise, an error message is displayed.

# 4.3.5 Performing STM32HSM programming for license generation using STPC (CLI mode)

STM32 Trusted Package Creator provides CLI commands to program STM32HSM cards. To configure the STM32HSM before programming, the user must provide the mandatory inputs by using the specific options.

# Example of STM32HSM-V1 provisioning

STM32TrustedPackageCreator_CLI -hsm -i 1 -k "C:\TrustedFiles\key.bin" -n "C:\TrustedFiles\nonce.bin" -id HSMvl_SLOT_1-mc2000

• -i: select the slot ID • -k: set the encryption key file path • -n: set the nonce file path • -id: set the firmware identifier • -mc: set the maximum number of licenses.

STM32HSM-V2 allows users to personalize their own HSM to achieve, for example, compatibility with the desired STM32 device. This solution covers the limitations of STM32HSM-V1 (static behavior), so it is possible to support new devices that are not available on STM32HSM-V1.

To perform this operation the user first needs to know the product ID of the device. This information is provided in the STM32 device certificate, which can be obtained with the following command:

STM32_Programmer.exe -C port=COM1 -gc "C:\SFI\Certificate.bin"

After getting the binary file of the device certificate, it is necessary to open this file using a HEX editor application. Once these steps are done the user can read the product ID.

Figure 36. Example product ID   

<table><tr><td>00000000</td><td>00</td><td>01</td><td></td><td>02 03</td><td></td><td>04 05</td><td></td><td>06 07</td><td></td><td>08 09</td><td></td><td>Oa Ob</td><td></td><td>Oc Od Oe Of</td><td></td><td></td><td></td><td></td></tr><tr><td>00000000</td><td>34</td><td>39</td><td>37</td><td>′30</td><td></td><td>3130</td><td></td><td>3035</td><td></td><td>07d7</td><td></td><td>60 ′65</td><td></td><td>98</td><td>2a</td><td>fe36</td><td></td><td>49701005.*e&quot;*b6</td></tr><tr><td>00000010</td><td></td><td>29 ca</td><td></td><td>59 ′f3</td><td></td><td>d529</td><td></td><td>9b99</td><td></td><td>f7a3</td><td></td><td>4e</td><td>c0</td><td>bb</td><td>15</td><td></td><td>5fd1</td><td>)ÉY)-£Nà&gt;N</td></tr><tr><td>00000020</td><td></td><td>1d82</td><td></td><td>f4 ′8a</td><td></td><td>9a ′13</td><td></td><td>2dd3</td><td></td><td>c92a</td><td></td><td>9a ′02</td><td></td><td>c09b</td><td></td><td>db</td><td>′10</td><td>.,ós.-ÓÉ*.À&gt;.</td></tr><tr><td>00000030</td><td>fc2d</td><td></td><td></td><td>28d9</td><td></td><td>c9 77</td><td></td><td>bc4c</td><td></td><td>ba38</td><td></td><td>5b15</td><td></td><td>e5b0</td><td></td><td>8dbd</td><td></td><td>ü-(ùÉwL°8[.°</td></tr><tr><td>00000040</td><td>do</td><td>′4d</td><td></td><td>c3 4a</td><td></td><td>e9 d1</td><td></td><td>24 ′6b</td><td></td><td>a8 fc</td><td></td><td>3f51</td><td></td><td>af42</td><td></td><td>41</td><td>dd</td><td>DMÄJé$k&quot;ü?Q BA</td></tr><tr><td>00000050</td><td>be</td><td>b3</td><td></td><td>e4 bb</td><td></td><td>77</td><td>48</td><td>14 ′fa</td><td></td><td>4b ′d6</td><td>3b</td><td>′bb</td><td></td><td>67</td><td>′44</td><td>e5</td><td>al</td><td>x&#x27;ä&gt;wH.úKÖ;&gt;gDài</td></tr><tr><td>00000060</td><td>63ca</td><td></td><td></td><td>766b</td><td></td><td>dba3</td><td></td><td>80cf</td><td></td><td>e061</td><td></td><td>f301</td><td></td><td>07</td><td>′05</td><td>dd</td><td>′6c</td><td>cvkû€àaó...íι</td></tr><tr><td>00000070</td><td></td><td></td><td>74 f6 29 23</td><td></td><td></td><td></td><td></td><td>17 8f bd e7</td><td></td><td>c5cb</td><td></td><td>3a5c</td><td></td><td>Oe</td><td>5b′</td><td>58a3</td><td></td><td>tö)#. Kç:\.[XE</td></tr><tr><td>00000080</td><td></td><td></td><td>8cdc 8d 13</td><td></td><td></td><td></td><td></td><td>971eab52</td><td></td><td></td><td>:</td><td></td><td></td><td></td><td></td><td></td><td></td><td>..&lt;R.</td></tr><tr><td>00000090</td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td>:</td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td></tr></table>

The product ID of the STM32WL used is: 49701005

In the second step, the users provision their own STM32HSM-V2 by programming it using STPC. The personalization data file .bin can be found under "..\bin\PersoPackages".

# Example of STM32HSM-V2 provisioning

A new option [-pd] must be inserted to include the personalization data:

STM32TrustedPackageCreator_CLI -hsm -i 1 -k "C:\TrustedFiles\key.bin" -n "C:\TrustedFiles\nonce.bin" -id HSMv2_SLOT_2 -mc 2000 -pd "C:\TrustedFiles\enc_ST_Perso_L5.bin"

-pd: Set the personalization data file path.

To obtain the appropriate personalization data file and for further information, refer to Section 4.3.5: Performing STM32HSM programming for license generation using STPC (CLI mode).

# Note:

A green message display indicates that the programming operation succeeded, otherwise a red error message is displayed.

If the STM32HSM is already programmed and there is a new attempt to reprogram it, an error message being displayed to indicate that the operation failed, and the STM32HSM is locked.

STM32HSM-V1 supports a list of a limited number of STM32 devices such as STM32L4, STM32H7, STM32L5, and STM32WL.

# Example of STM32HSM get information

If the STM32HSM is already programmed or is virgin yet and whatever the version, a get information command can be used to show state details of the current STM32HSM by using the command below:

STM32TrustedPackageCreator_CLI -hsm -i 1 -info

![](images/cd56023e1af41693c2919a2f601dbdbd1433296480486b6dbe92524223ae4bf8.jpg)  
Figure 37. STM32HSM information in STM32 Trusted Package Creator CLI mode

# 4.3.6 Programming input conditions

Before performing an SFI install make sure that:

Flash memory is erased.

No PCROPed zone is active, otherwise destroy it.

• h muso ury  cry  mus  rent otn ).

When using a UART interface, the user security bit in option bytes must be enabled before launching the SFI command. For this, the following STM32CubeProgrammer command is launched:

Launch the following command (UART bootloader used => Boot0 pin set to VDD): -C port=COM9 -ob SECURITY=1

When using a UART interface the Boot0 pin must be set to VSS:

After enabling security (boot0 pin set to VDD), a power off/power on is needed when switching the Boot0 pin from VDD to VSS: power off, switch pin then power on.

When performing an SFI install using the UART bootloader then, no debug interface must be connected to any USB host. If a debug interface is still connected, disconnect it then perform a power off/power on before launching the SFI install to avoid any debug intrusion problem.

Boot0 pin set to VDD When using a debug interface.

A valid license generated for the currently used chip must be at your disposal, or a license generation tool to generate the license during SFI install (STM32HSM).

For STM32L5 products, TZEN must be set at 0 (TZEN=0).

# 1.3.7 Performing the SFI install using STM32CubeProgrammer

In this section, the STM32CubeProgrammer tool is used in CLI mode (the only mode so-far available for secure programming) to program the SFI image "out.sfi" already created in the previous section.

STM32CubeProgrammer supports communication with STMicroelectronics STM32HSMs (Hardware secure modules based on smartcard) to generate a license for the connected STM32 device during SFI install.

# Using JTAG/SWD

After making sure that all the input conditions are respected, open a cmd terminal and go to <STM32CubeProgrammer_package_path>/bin, then launch the following STM32CubeProgrammer command:

STM32_Programmer_CLI.exe -c port=swd mode=HOTPLUG -sfi protocol=static "<local_path>/out.sfi" hsm=1 slot=<slot_id>

# Note:

In the case of an STM32L5 device the SFI install uses the RSSe and its binary file is located in the STM32CubeProgrammer bin/RSSe folder.

The STM32CubeProgrammer command is as follows:

STM32_Programmer_CLI.exe -c port=Swd mode=HOTPLUG -sfi protocol=static "<local_path>/out.sfi" hsm=1 slot=<slot_id> -rsse <RsSe_path>

# 4.3.8 SFI with integrity check (for STM32H73xxx)

For the STM32H73xxx, an integrity check mechanism is implemented. STM32 Trusted Package Creator calculates the input firmware hash and integrates it into the SFI firmware. The STM32H73xxx MCU is able to use this hash input to check the firmware integrity.

Enabling this mechanism is mandatory for STM32H73xxx, and it can be done through GUI and CLI.

For the GUl part, hash is enabled by checking Generate hash.

![](images/21031a08120f2ab494e4d84ed945f098cd988f6f887af8ec858b15a2b5337566.jpg)  
Figure 38. STM32Trusted Package Creator SFI 'hash Generator 'check box

For the CLI part SFI command line must integrate the -hash option.

# Usage example:

STM32TrustedPackageCreator_CLI.exe -sfi -fir OEM_Dev.bin Ox08000000 -k aeskey.bin -n nonce.bin -ob ob.csv -v 0 -- ramsize OxlE000 --token Ox080FF000 -hash 1 -o outCLI.sfi

Figure 39 shows the SFI install via SWD execution and the STM32HSM as license generation tool in the field.

![](images/ddfc483478095ab50763bd1d7fba26a4d5ea3e1e59d456356c2b0447650586de.jpg)  
Figure 39. SFI installation success using SWD connection (1)

![](images/c572b5bb8e3cef330e777fb89a5ca297bf914d10e0dcd672fc4386acff5ad2a0.jpg)  
Figure 40. SFI installation success using SWD connection (2)

# Example of SFI programming scenario for STM32WL

# 5.1 Scenario overview

The user application is developed by the OEM and encrypted by STPC. The OEM provides the following elements to the programming house:

• The encrypted firmware of STM32WL • STM32HSM-V1 or provisioned STM32HSM-V2 • STM32CubeProgrammer

With these inputs, the untrusted manufacturer is able to securely program the encrypted firmware.

# 5.2 Hardware and software environment

For successful SFI programming, the following hardware and software prerequisites apply:

STM32WL5x board with bootloader and RSS programmed RS-232 cable for SFI programming via UART • Micro-B USB for debug connection PC running on either Windows®, Linux® Ubuntu® or Fedora®, or macOS® STM32 Trusted Package Creator v1.7.0 (or greater) package available from www.st.com STM32CubeProgrammer v2.16.0 (or greater) package available from www.st.com STM32HSM-V1 or STM32HSM-V2

Note:

Refer to [4] or [5] for the supported operating systems and architectures.

# 5.3

# Step-by-step execution

# 5.3.1

# Build OEM application

OEM application developers can use any IDE to build their own firmware.

# 5.3.2 Perform the SFI generation (GUI mode)

The first step to install the secure firmware on STM32 devices is the encryption of the user OEM firmware (already provided in AXF format) using the STM32 Trusted Package Creator tool.

This is done by adding the following files in the STPC tool:

• OEM firmware   
• A .csv file containing option bytes configuration   
• A 128-bit AES encryption key   
• A 96-bit nonce

#

STM32CubeProgrammer v2.8.0 and later provide one option byte file example for each product.

It is located in the directory: STM32CubeProgrammerlvx.x.x\bin\SFI_OB_CSV_FILES

The option bytes are described in the product reference manual.

In the case of customization of a provided example file, care must be taken not to change the number of rows, or their order.

A programmed STM32HSM card must be inserted in the PC, and an "out.sfi" image is then generated.

![](images/5105c733bfab562236755ba8d0ddd053d99036f57c0b76724f31763bf18fd767.jpg)  
Figure 41. STPC GUI during the SFI generation (STM32WL)

# Note:

# To perform STM32HSM programming for license generation using STPC (GUI mode and CLI mode) refer to the following sections:

Section 4.3.4: Performing STM32HSM programming for license generation using STPC (GUI mode)

Section 4.3.5: Performing STM32HSM programming for license generation using STPC (CLI mode)

# 5.3.3 Programming input conditions

Before performing an SFI install on STM32WL devices make sure that:

• Flash memory is erased   
• No PCROPed zone is active, otherwise remove it   
• The chip supports security (a security bit must be present in the option bytes)   
• The security must be disabled, if activated The option bytes of the device are set to default values. This step is done by the two commands given below.

-desurity: This option allows the user to disable security. After executing this command, a power OFF / power ON must be done.

# Example:

STM32_Programmer_CLI.exe -c port=swd mode=hotplug -dsecurity

Figure 42 hows the resulting output on the command line.

![](images/f6e16e5101a31d0e99b6b057193b5d8ed7a0822c76fda0b06c472318692805f7.jpg)  
Figure 42. Example -dsecurity command-line output

-setdefaultob: This command allows the user to configure option bytes to their default values. After executing this command, a power OFF/power ON must be done.

# Example:

;TM32_Programmer_CLI.exe -c port=swd mode=hotplug -setdefaulto

Figure 43 shows the resulting output on the command line.

![](images/3b0c107b1141789f7322367035a296c2f77eff6bbbb7a1c10c8368ff7e999715.jpg)  
Figure 43. Example -setdefaultob command-line output

# 5.3.4 Perform the SFI install using STM32CubeProgrammer

In this section, the STM32CubeProgrammer tool is used in CLI mode (the only mode so-far available for secure programming) to program the SFI image "out.sfi" already created in the previous section.

STM32CubeProgrammer supports communication with STMicroelectronics STM32HSMs (Hardware secure modules based on smartcard) to generate a license for the connected STM32 device during SFI install.

Using JTAG/SWD

After making sure that all the input conditions are respected, open a cmd terminal and go to <STM32CubeProgrammer_package_path>/bin, then launch the following STM32CubeProgrammer command:

STM32_Programmer_CLI.exe -C port=Swd mode=HOTPLUG -sfi "<local_path>/out.sfi" hsm=1 slot=<slot_id> -rsse "< RSSe_path >"

# Note:

The RSSe and its binary file are located in the STM32CubeProgrammer bin/RSSe/WL folder.

Figure 44 shows the SFI install via SWD execution.

![](images/2fcac344a6062dd02e351313f4552cc9ade2f2d7dd82379165500b01e8b11fed.jpg)  
Figure 44. SFI installation via SWD execution command-line output

# Example of SFI programming scenario for STM32U5

# 6.1 Scenario overview

The actual user application to be installed on the STM32U5 device makes "print f" packets appear in serial terminals. The application was encrypted using the STPC.

The OEM provides tools to the CM to get the appropriate license for the concerned SFI application.

# 6.2 Hardware and software environment

For successful I programming, some hardware nd software prerequisites apply:

STM32U5 board with bootloader and RSS programmed   
RS-232 cable for SFI programming via UART   
Micro-B USB for debug connection   
PC running on either Windows®, Linux® Ubuntu® or Fedora®, or macOS®   
STM32 Trusted Package Creator v1.2.0 (or greater) package available from   
www.st.com   
STM32CubeProgrammer v2.8.0 (or greater) package available from www.st.com   
STM32HSM-V2

Note:

Refer to [4] or [5] for the supported operating systems and architectures.

# 6.3

# Step-by-step execution

# 6.3.1

# Build OEM application

OEM application developers can use any IDE to build their own firmware.

# .3.2 Perform the SFI generation (GUI mode)

The first step to install the secure firmware on STM32 devices is the encryption of the user OEM firmware (already provided in AXF format) using the STM32 Trusted Package Creator tool. This step is done by adding the following files in the STPC tool:

• An OEM firmware   
• A .csv file containing option bytes configuration   
• A 128-bit AES encryption key   
• A 96-bit nonce

#

STM32CubeProgrammer v2.8.0 and later provide one option byte file example for each product.

It is located in the directory: STM32CubeProgrammerlvx.x.x\bin\SFI_OB_CSV_FILES

The option bytes are described in the product reference manual.

In the case of customization of a provided example file, care must be taken not to change the number of rows, or their order.

In addition, a programmed STM32HSM card must be inserted in the PC. An "out.sff" image is then generated.

Figure 45 shows the STPC GUI during SFI generation.

![](images/0b0e31c506d4476ff1af54da4e6c69849f0b07ca8803321589a78ddc80eaab7b.jpg)  
Figure 45. STPC GUI during the SFI generation (STM32U5)

# Note:

To perform STM32HSM programming for license generation using STPC (GUI and CLI modes), refer to Section 4.3.4: Performing STM32HSM programming for license generation using STPC (GUI mode) and Section 4.3.5: Performing STM32HSM programming for license generation using STPC (CLI mode).

# 6.3.3 Programming input conditions

Before performing an SFI install on STM32U5 devices, make sure that:

• The flash memory is erased.   
• No WRP zone is active, otherwise destroy it.   
• The chip supports security (a security bit must be present in the option bytes).   
• If the security is activated, disable it.

# j.3.4 Perform the SFI install using STM32CubeProgrammer

In this section, the STM32CubeProgrammer tool is used in CLI mode (the only mode so far available for secure programming) to program the SFl image "out.sf" already created in the previous section.

STM32CubeProgrammer supports communication with STMicroelectronics STM32HSMs (hardware secure modules based on smartcards) to generate a license for the connected STM32 device during the SFI install process.

# Using JTAG/SWD

First make sure that all the input conditions are respected, then open a cmd terminal, go to <STM32CubeProgrammer_package_path>/bin and launch the following STM32CubeProgrammer command:

STM32_Programmer_CLI.exe -C port=Swd mode=HOTPLUG -sfi "<local_path>/out.sfi" hsm=1 slot=<slot_id> -rsse "< RSSe_path >"

# Note:

The RSSe and the corresponding binary file are located in the STM32CubeProgrammer bin/RSSe/U5 folder.

Figure 46 and Figure 47 show the STM32CubeProgrammer command used for the SFI install process via SWD execution.

![](images/387476d37dc6e0e0556abac298dd34493dffd806134b5271d9ea9e6f52154a7b.jpg)  
Figure 46. SFI installation via SWD execution (1)

![](images/bb08ffd1ffc91197375bcb5421fd7321a853883f9339b1a73ea22e46114c58aa.jpg)  
Figure 47. SFI installation via SWD execution (2)

# Example of SFI programming scenario for STM32WBA5x and STM32WBA6x

# 7.1 Scenario overview

The actual user application to be installed on the STM32WBA5x/6x device. The application was encrypted using the STPC. The OEM provides tools to the CM to get the appropriate license for the concerned SFI application

# 7.2 Hardware and software environment

For successful SFI programming, some hardware and software prerequisites apply:

STM32WBA5x/6x board with bootloader and RSS programmed • RS-232 cable for SFI programming via UART Micro-B USB for debug connection PC running on either Windows®, Linux® Ubuntu® or Fedora®, or macOS® STM32 Trusted Package Creator v1.7.0 (or greater) package available from www.st.com STM32CubeProgrammer package available from www.st.com For STM32WBA5x, v2.16.0 (or greater) For STM32WBA6x, v2.19.0 (or greater) STM32HSM-V2

Note:

Refer to [4] or [5] for the supported operating systems and architectures.

# 7.3

# Step-by-step execution

# 7.3.1

# Build OEM application

OEM application developers can use any IDE to build their own firmware.

# Perform the SFI generation (GUI mode)

The first step to install the secure firmware on STM32 devices is the encryption of the user OEM firmware (already provided in AXF format) using the STM32 Trusted Package Creator tool. This step is done by adding the following files in the STPC tool:

• An OEM firmware   
• A .csv file containing option bytes configuration   
• A128-bit AES encryption key   
• A 96-bit nonce

# Note:

STM32CubeProgrammer v2.8.0 and later provide one option byte file example for each   
product. It is located in the directory:   
STM32CubeProgrammerlvx.x.x\bin\SFI_OB_CSV_FILES

The option bytes are described in the product reference manual. In the case of customization of a provided example file, care must be taken not to change the number of rows, or their order.

In addition, a programmed STM32HSM card must be inserted in the PC. An output-WBA5.sfi" or "output-WBA6.sfi" image is then generated.

Figure 48 shows the STPC GUI during SFI generation.

![](images/ef68c0e71140872a3b7ab1d7e4cd63d951ee8b082e3256a196fcaa9275b6cfd4.jpg)  
Figure 48. STPC GUI during the SFI generation (STM32WBA5x)

Note:

To perform STM32HSM programming for license generation using STPC (GUI and CLI modes), refer to Section 11.3.3: Performing STM32HSM programming for license generation using STPC (GUI mode) and Section 4.3.5: Performing STM32HSM programming for license generation using STPC (CLI mode).

# 7.3.3 Programming input conditions

Before performing an SFI install on STM32WBA5x/6x devices, make sure that:

• The flash memory is erased.   
• No WRP zone is active, otherwise destroy it.   
• The chip supports security (a security bit must be present in the option bytes).   
• If the security is activated, disable it.

# 7.3.4 Perform the SFI install using STM32CubeProgrammer

In this section, the STM32CubeProgrammer tool is used in CLI mode to program the SFI image "output-WBA5.sfi" or "output-WBA6.sfi" already created in the previous section.

STM32CubeProgrammer supports communication with STMicroelectronics STM32HSMs (hardware secure modules based on smartcards) to generate a license for the connected STM32 device during the SFI install process.

# Using the UART interface

First make sure that allthe input conditions are respected, then open a cmd terminal, go to /bin and launch the following STM32CubeProgrammer command:

STM32_Programmer_CLI.exe -c port=COM204 -sfi protocol=static "/output-WBAx.sfi" hsm=1 slot=1 -rsse "< RSSe_path >"

# Note:

The RSSe and the corresponding binary file are located in the STM32CubeProgrammer bin/RSSe/WBA folder.

Figure 49 shows the STM32CubeProgrammer command used for the SFI install process via UART execution.

![](images/d364cd8a8a23d7991f8c120ef8a7457552b70987b106579150e523f605eee073.jpg)  
Figure 49. SFI installation via UART execution using CLI (1)

MC.70704

![](images/3428bf2e74b6f363676bb7615e906a55e7994d1bad0315be91e6495f2e4b40b3.jpg)  
Figure 50. SFI installation vi UART execution using CLI (2)

![](images/afeffd6f50a4fa85e6bfce3d0dde7365387a9a837337ae00f42b5afe25d6ac33.jpg)  
Figure 51. SFI installation via UART execution using CLI (3)

# Graphical user interface mode (STM32wBA5x example)

Open the STM32CubeProgrammer and connect the board through the UART interface with the right COM port. Press on the "Security" panel and select the SFI/SFIx from the tab options with the following inputs:

License source selection: "Using License from HSM" •SFI/SFIx path: output-WBA5.sfi •RSSe: /RSSe/WBA/enc_signed_RSSe_sfi_WBA5_1M.bin

Click on the "Start SFI/SFIx" button to launch the SFI installation.

![](images/ad5d0b96a419d7c6d4b25887b78aa4dfdfddbf81cf7e8d52b9799c9b40657b8b.jpg)  
Figure 52. STM32WBA5x SFI successful programming via UART interface using GUI

# Example of SFIA programming scenario for STM32WBA5x

# 8.1 Scenario overview

SFIA is an SFI operation without a mass erase. It means that the user should perform an SFI install when all the flash memory is empty, or when the data written in the user flash memory is outside of the SFI firmware to install. (For more details refer to [1]).

In this example, the SFI is installed when the flash memory is already empty. The actual user application to be installed on the STM32WBA5x device. The application is encrypted using the STPC. The OEM provides the tools to the CM to get the appropriate license for the concerned SFIA application.

# 8.2 Hardware and software environment

For a successful SFIA programming, the following hardware and software prerequisites are needed:

An STM32WBA5x board with boot loader and RSS programmed An RS-232 cable for SFIA programming via UART A Micro-B USB for debug connection C A PC running on either Windows®, Linux® Ubuntu® or Fedora®, or macOS® STM32 Trusted Package Creator v2.17.0 (or greater) package available from www.st.com STM32CubeProgrammer v2.17.0 (or greater) package available from www.st.com STM32HSM-V2 (To generate the SFIA license)

Note:

Refer to [4] or [5] for the supported operating systems and architectures.

# 8.3

# Step-by-step execution

# 8.3.1

# Build an OEM application

OEM application developers can use any IDE to build their own firmware.

# 8.3.2 Perform the STM32HSM programming for the SFIA license generation (GUI mode)

The STM32 Trusted Package Creator tool provides all the personalization package files ready to be used on the SFI/SFIA/SFIx and SSP flows. To get all the supported SFIA packages, go to the PersoPackages/SFIA directory in the install path of the tool. Each file name starts with a number, which is the product ID of the device. Select the correct one.

In this case, select: STM32WBA5_49202013_SFIA_01000000_00000000.enc.bin to program the STM32HSM card.

![](images/dc3a48010b380d1c4d405be32e04fb6cede8d9c95954ba142d9a98460b8c11f2.jpg)  
Figure 53. Example of STM32HSM programming (SFIA License) using STPC GU

# 8.3.3 Perform the SFI generation (GUI mode)

The first step to install the secure firmware on STM32 devices is the encryption of the user OEM firmware. The firmware is already provided in AXF format. The installation is done using the STM32 Trusted Package Creator tool.

The steps described in Section 7.3.2: Perform the SFI generation (GUI mode) can be followed.

# 8.3.4 Programming input conditions

Before performing an SFI install on STM32WBA5x devices, the user must ensure that:

• The flash memory is erased.   
• No WRP zone is active, otherwise it should be destroyed.   
• The chip supports security (a security bit must be present in the option bytes). The security is disabled.

# 8.3.5 Perform the SFI installation using STM32CubeProgrammer

In this section, the STM32CubeProgrammer tool is used in CLI mode to program the SFI image "output-WBA5.sf" that was created in the previous section.

The STM32CubeProgrammer supports communication with STMicroelectronics STM32HSMs (hardware secure modules based on smartcards) to generate a license for the connected STM32 device during the SFI install process.

# Example of SFI programming scenario for STM32H5

# 9.1 Scenario overview

The user application is developed by the OEM and encrypted by STPC. The OEM provides the following elements to the programming house:

• The encrypted STM32H5 firmware • A global license binary • STM32CubeProgrammer

The untrusted manufacturer is then required to securely program the encrypted firmware using these inputs.

# 9.2 Hardware and software environment

For successful SFI programming, the following hardware and software prerequisites apply:

STM32H5-based board with bootloader and RSS programmed SFI programming via UART (use RS-232 cable or ST-LINK VCOM) o PC running on either Windows®, Linux® Ubuntu® or Fedora®, or macOS® aSTM32 Trusted Package Creator v2.14.0 (or greater) package available from www.st.com STM32CubeProgrammer v2.14.0 (or greater) package available from www.st.com

Note:

Refer to [4] or [5] for the supported operating systems and architectures.

# 9.3

# Step-by-step execution

# 9.3.1

# Build OEM application

OEM application developers can use any IDE to build their own firmware.

# Perform the SFI generation (GUI mode)

The first step to install the secure firmware on STM32H5 devices is the encryption of the user OEM firmware using the STM32 Trusted Package Creator tool.

This step is done by including the following files in the STPC tool:

• An OEM firmware   
• A .csv file containing option bytes configuration   
• A 128-bit AES encryption key   
• A 96-bit nonce   
• OBKey files for device configuration (optional) An SSFI file to integrate the STMicroelectronics SFI image (optional, only for STM32H573xx)

#

It is recommended to use the "SFI Option Bytes" feature from the "H5" panel of the STM32 Trusted Package Creator tool to obtain the option bytes file (.csv file).

Note:

If you want to reopen the device using the Debug Authentication mechanism, a DA ObKey file must be included in the SFI image, otherwise the device becomes inaccessible.

![](images/793439ba1ff3914c867d5366326d13de3ea437b2b730e0808505306973223c3b.jpg)  
Figure 54. SFI generation for STM32H5

# 9.3.3 Programming input requirements

Before performing an SFI install on STM32H5 devices, make sure that:

Flash memory erased   
• Chip supporting cryptography for a Secure Manager usage   
• Product state open: OxED   
• Boot on bootloader: UART interface   
• RSSe binary STMicroelectronics global license file (no need for an STM32HSM card in this use case)

Note:

The RSSe binary file is in the STM32CubeProgrammer bin/RSSe/H5 folder.

Note:

To embed an SSFI image into the SFI image, it is recommended to follow a specific secure sequence and choose an adequate start address of the nonsecure application that depends on the SSFI configuration. See the details in STM32CubeH5 MCU Package available from www.st.com.

To generate an STMicroelectronics global license binary, use the "H5" panel of the STM32 Trusted Package Creator GUI and select the "License Gen" option. Then, include the same key and nonce previously used to generate the SFl image (see the figure below).

![](images/f648fa194df8a73e06bcf9fad6848888f32967ae56b28a26cac2672e4a7e9cbf.jpg)  
Figure 55. STMicroelectronics global license generation for STM32H5

# ).3.4 Perform the SFI install using STM32CubeProgrammer

In this section, the STM32CubeProgrammer tool is used in CLI mode to program the SFI image "out.sfi" already created in the previous section.

STM32CubeProgrammer communicates with the device through the UART interface after it is confirmed that all the input conditions are respected.

Note that the same operation is possible using ST-LINK (SWD/JTAG) or any bootloader interface.

# Command-line mode

Open a cmd terminal, go to /bin in the install path, and then launch the following command:

STM32_Programmer_CLI.exe -C port=COM8 -sfi "out.sfi" hsm=O "ST_Global_License_Vo.bin" -rsse "\RSSe\H5\enc_signed_RSSe_SFI_STM32H5_v2.0.0.0'

Figure 56 shows the SFI execution traces.

![](images/315445b0118d8b1aa97bf190aa94d5b449e551caf4eaf8243779c0f47d864e8a.jpg)  
Figure 56. STM32H5 SFI successful programming via CLI

DT73501V1

# Graphical user interface mode

Open the STM32CubeProgrammer and connect the board through the UART interface with the right COM port. Press on the "Security" panel and select the SFI/SFIx from the tab options with the following inputs:

• License source selection: "Using License from file" • SFI/SFIx path: out.sfi • RSSe: \RSSelH5\ enc_signed_RSSe_SFI_STM32H5_v2.0.0.0.bir

Click on the "Start SFI/SFIx" button to launch the SFI installation.

![](images/c5b1c11448b4155793e258e5a1ffeaf587c3dbed67eb48a5bd1c880bf197d7b6.jpg)  
Figure 57. STM32H5 SFI successful programming via GUI

# Example of SFI programming scenario for STM32H7Rx/7Sx

# 10.1 Scenario overview

There are three steps during this scenario:

• Generate STM32H7Rx/7Sx encrypted firmware using the STPC • STM32HSM card provisioning via STPC • Use STM32CubeProgramer to perform the SFI process.

# 10.2 Hardware and software environment

For successful SFI programming, some hardware and software prerequisites apply:

An STM32H7Rx/7Sx-based board and system flash security package (SFSP) v1.1.0 ol   
greater   
USB Type-C® cable for SWD connection   
A PC running on either Windows®, Linux® Ubuntu® or Fedora®, or macOS®   
An STM32 Trusted Package Creator v2.16.0 (or later) package available from   
www.st.com   
An STM32CubeProgrammer v2.16.0 (or later) package available from www.st.com   
An STM32HSM-V2 smartcard

Note:

Refer to [4] or [5] for the supported operating systems and architectures.

# 10.3

# Step-by-step execution

10.3.1

# Build an OEM application

OEM application developers can use any IDE to build their own firmware.

# Perform the SFI generation (GUI mode)

The first step to install the secure firmware on STM32H7Rx/7Sx devices is the encryption of the user OEM firmware using the STM32 Trusted Package Creator tool.

This step is done by including the following files in the STPC tool:

S An OEM firmware   
• A .csv file containing option bytes configuration   
• A 128-bit AES encryption key   
• A 96-bit nonce   
• Random key area file (optional)   
√ OBKey files for device configuration (optional)

Note:

It is recommended to use the "SFI Option Bytes" feature of the STM32 Trusted Package Creator tool to obtain the option bytes file (.csv file).

#

If you want to reopen the device using the Debug Authentication mechanism, a DA ObKey file must be included in the SFI image, otherwise the device becomes inaccessible.

![](images/5e102430b682bf035011cca090c0c3fd07d6d9e7dae60bf03ba0e4d438daede0.jpg)  
Figure 58. SFI generation for STM32H7Rx/7Sx

# 10.3.3 Programming input requirements

Before performing an SFI install on STM32H7Rx/7Sx devices, make sure that:

• Product state is open: 0x39   
• A ready generated SFI image using the STPC tool   
• RSSe binary   
• STMicroelectronics global license file (no need for an STM32HSM card in this use case)

Note:

Using a non STM32H7Rx/7Sx sfi image might result in errors or issues during the installation process.

Note:

The RSSe binary file is in the STM32CubeProgrammer bin/RSSe/H7RS folder.

# 0.3.4 Perform the SFI install using STM32CubeProgrammer

In this section, the STM32CubeProgrammer tool is used in CLI mode to program the SFl image "out.sfi" already created in the previous section.

STM32CubeProgrammer communicates with the device through the SWD interface after it is confirmed that all the input conditions are respected.

Note that the same operation is possible using ST-LINK (SWD/JTAG) or any bootloader interface.

# Command-line mode

Open a cmd terminal, go to /bin in the install path, and then launch the following command:

STM32_Programmer_CLI.exe -c port=swd mode=hotplug -sfi "out.sfi" hsm=0 "ST_Global_License_VO.bin" -rsse "\RSSe\H7RS\ enc_signed_RSSe_sfi.bin"

Figure 5 shows the SFI execution traces.

C:\Windows\System32\cmd.exe × Memory Programming   
Opening and parsing file: enc_signed_RSSe_sfi.bin   
File : enc_signed_RSSe_sfi.bin   
Size : 33.67 KB   
Address : 0x20000200   
Erasing memory corresponding to segment 0:   
Download in Progress:   
File download complete   
Time elapsed during download operation: 00:00:00.069   
License Install   
Installing Areas...   
Succeed to write Areas   
Attempt to reconnect to check on SFI success...   
ST-LINK SN : 003300184741500820383733   
ST-LINK FW : V3J13M4   
Board :STM32H7S78-DK   
Voltage : 3.30V   
...retrying...   
ST-LINK SN : 003300184741500820383733   
ST-LINK FW : V3J13M4   
Board :STM32H7S78-DK   
Voltage : 3.30V   
...retrying...   
STT-LINK N : 003300184741500820383733   
ST-LINK FW : V3J13M4   
Board : STM32H7S78-DK   
Voltage : 3.30V   
..retrying...   
ST-LINK SN : 003300184741500820383733   
ST-LINK FW : V3J13M4   
Board : STM32H7S78-DK   
Voltage : 3.30V   
...retrying...   
ST-LINK SN: 003300184741500820383733   
ST-LINK FW : V3J13M4   
Board : STM32H7S78-DK   
Voltage : 3.30V   
...retrying...   
ST-LINK SN : 003300184741500820383733   
ST-LINK FW : V3J13M4   
Board : STM32H7S78-DK   
Voltage : 3.30V   
Error: failed to reconnect after reset !   
SseiiccrDesotH..nstaperatiuc   
Time elapsed during SFI install operation: 00:00:07.059

# Graphical user interface mode

Open the STM32CubeProgrammer and connect the board through the SWD. Go to the security panel and select the SFl/SFIx from the tab options with the following inputs:

License source selection: "Using License from file" • SFI/SFIx path: out.sfi RSSe: \IRSSelH7RSI enc_signed_RSSe_sfi.bin

Click on the "Start SFI/SFIx" button to launch the SFI installation.

![](images/e974bfd9ab19e8871bfa82e6f730974f43f59780b24a0d6460313d309fa4893d.jpg)  
Figure 60. STM32H7Rx/7Sx SFI successful programming via GUI

#

# Example of SFIx programming scenario for STM32H7

# 11.1 Scenario overview

There are three steps during this scenario:

Generate an SFIx image using the STPC.   
• Provisioning STM32HSM card via STPC.   
• Use the STM32CubeProgrammer to perform the SFIx process.

Once this scenario is successfully installed on the STM32H7B3I-EVAL, follow the steps below:

C Write internal firmware data in the internal flash memory starting at the address 0x08000000. Write external frmware data in the external flash memory starting at the adress 0x90000000.   
• Verify that the option bytes were correctly programmed (depends on area C).

# 11.2 Hardware and software environment

For successful SFIx programming, some hardware and software prerequisites apply:

STM32H7B3I-EVAL board containing external flash memory.   
Micro-B USB for debug connection.   
PC running on either Windows®, Linux® Ubuntu® or Fedora®, or macOS® STM32 Trusted Package Creator v1.2.0 (or greater) package available from www.st.com   
STM32CubeProgrammer v2.3.0 (or greater) package available from www.st.com STM32HSM-V1.1 card

Note:

Refer to [4] or [5] for the supported operating systems and architectures.

# 11.3

# Step-by-step execution

# 11.3.1 Build OEM application

OEM application developers can use any IDE to build their own firmware.

In this use case, there are different user codes. Each one is specific to a flash memory type (internal/external).

# 11.3.2 Perform the SFIx generation (GUI mode)

To be encrypted with the STM32 Trusted Package Creator tool, OEM firmware is provided in Bin/Hex/AXF format in addition to a CSV file to set the option bytes configuration. A 128-bit AES encryption key and a 96-bit nonce are also provided to the tool.

# Note:

STM32CubeProgrammer v2.8.0 and later provide one option byte file example for each product.

It is located in the directory: STM32CubeProgrammerlvx.x.x\bin|SFI_OB_CSV_FILES

The option bytes are described in the product reference manual.

In the case of customization of a provided example file, care must be taken not to change the number of rows, or their order.

An "sfix" image is then generated (out.sfix).

![](images/125aa432624958cf98cbad30e58507be669f93a36ce4bbaa5b0bc04af4c6341c.jpg)  
Figure 61. Successful SFlx generation

# |1.3.3 Performing STM32HSM programming for license generation using STPC (GUI mode)

The OEM must provide a license generation tool to the programming house to be used for license generation during the SFI install process.

In this example, STM32HSMs are used as license generation tools in the field. See Section 3.1.2: License mechanism for STM32HSM use and programming.

Figure 62 shows an example for STM32HSM programming by OEM to be used for SFIx install.

The maximum number of licenses delivered by the STM32HSM in this example is 1000.

This example uses STM32HSM-V1. The STM32HSM version can be identified before performing the programming operation by clicking the "Refresh" button to make the version number appear in the version field.

![](images/15f0666143672209e79e2c2dae83003a7cb583f2f4f582024141eb7ff7b6515a.jpg)  
Figure 62. Example of STM32HSM programming using STPC GUI

# Note:

When using STM32HSM-V1, the "Personalization data file" field is ignored when programming starts. It is only used with STM32HSM-V2.

When the card is successfully programmed, a popup window message "HSM successfully programmed" appears, and the STM32HSM is locked. Otherwise, an error message is displayed.

# 1.3.4 Performing STM32HSM programming for license generation using STPC (CLI mode)

Refer to Section 4.3.5: Performing STM32HSM programming for license generation using STPC (CLI mode).

# 11.3.5 Programming input conditions

Before performing an SFIx install, make sure that:

• Use the JTAG/SWD interface.   
• No PCROPed zone is active, otherwise disable it.   
• The chip must support security (a security bit must be present in the option bytes).   
• The SFIx image must be encrypted by the same key/nonce used in the STM32HSM provisioning.

# 1.3.6 Perform the SFIx installation using STM32CubeProgrammer

In this section, the STM32CubeProgrammer tool is used in CLI mode (the only mode so-far available for secure programming) to program the SFlx image "out.sfix" already created in the previous section.

STM32CubeProgrammer supports communication with STMicroelectronics STM32HSMs (hardware secure modules based on smartcard) to generate a license for the connected STM32 device during SFIx install.

After making sure that all the input conditions are respected, open a cmd terminal and go to <STM32CubeProgrammer_package_path>/bin, then launch the following STM32CubeProgrammer command:

# Using JTAG/SWD

STM32_Programmer_CLI.exe -c port=swd mode=HOTPLUG -sfi protocol=static "<local_path>/out.sfix" hsm=1 slot=<slot_id> -el <ExternalLoader_Path>

Figure 63: SFlx installation success using SWD connection (1) through Figure 66: SFIx installation success using SWD connection (4) shows the SFlx install via SWD execution and the STM32HSM as license generation tool in the field.

![](images/c44d2bb1e3b6bbb88570d9c845c1fe35b4cdf1bd69b42792903028ce3aafab49.jpg)  
Figure 63. SFIx installation success using SWD connection (1)

![](images/6284ca7d5cf26072a010e3e24ffd411d919b21b40d08f584b731893b494631de.jpg)  
Figure 64. SFIx installation success using SWD connection (2)

# Figure 65. SFIx installation success using SWD connection (3)

Activating security.   
Warning: Option Byte: SECURITY, value: 0x1, was not modified. Warning: Option Bytes are unchanged, Data won't be downloaded Activating security Success   
Setting write mode to SFI   
Warning: Option Byte: SECURITY, value: 0x1, was not modified. Warning: Option Byte: ST_RAM_SIZE, value: 0x3, was not modified. Warning: Option Bytes are unchanged, Data won't be downloaded Succeed to set write mode for SFI

Starting SFI part 1

Writing license to address 0x24030800 Writing Img header to address 0x24031000 Writing areas and areas wrapper. RSS process started...

RSS command execution OK   
RSS complete Value = 0x0   
Reconnecting..   
ST-LINK SN 004000193037510B35333131 ST-LINK FW : V3J1M1   
Voltage : 3.28V   
SWD freq 24000 KHz   
Connect mode: Hot Plug   
Reset mode : Core reset   
Device ID : 0x480   
Reconnected !

Requesting security state.. Warning: Could not verify security state after last chunk programming

Starting SFI part 2

Writing license to address 0x24030800 Writing Img header to address 0x24031000 Writing areas and areas wrapper. RSS process started...

RSS command execution OK   
RSS complete Value = 0x0   
Reconnecting..   
ST-LINK SN 004000193037510B35333131 ST-LINK FW : V3J1M1   
Voltage : 3.28V   
SWD freq 24000 KHz   
Connect mode: Hot Plug   
Reset mode : Core reset   
Device ID : 0x480   
Reconnected!

Requesting security state... Warning: Could not verify security state after last chunk programming

Downloading area [3] data for external flash memory at address 0x9000000.. Data download complete

Starting SFI part 3

Writing license to address 0x24030800 Writing Img header to address 0x24031000 Writing areas and areas wrapper...   
all areas processed   
RSS process started...   
RSS command execution OK   
Warning: Could not verify security state after last chunk programming   
SFI Process Finished!   
SFI file C: \Users

Time elapsed during SFI install operation: 00:00:44.321

# Example of SFlx programming scenario for STM32L5/STM32U5

# 12.1 Scenario overview

There are three steps during this scenario:

1. Generate an SFIx image using the STPC   
2. STM32HSM card provisioning via STPC   
3. Use STM32CubePrg to perform the SFIx process.

Successful installation of this scenario on the STM32L5 provides the following results:

The internal flash memory is readable from base addresses Ox08000000 and   
0x08040000. It contains the internal firmware.   
The external flash memory is programmed so as to be readable with the external flash memory loader. You can then read the external flash memory encrypted by the OTFDEC keys. The pattern of values must be present in the binary files of external firmware.   
If the application works correctly, the onboard LED blinks.

# 12.2 Hardware and software environment

For successful SFIx programming, some hardware and software prerequisites apply:

• An STM32L5/STM32U5-based evaluation board containing external flash memory   
• A Micro-B USB for debug connection   
C A PC running on either Windows®, Linux® Ubuntu® or Fedora®, or macOS® An STM32 Trusted Package Creator v2.11.0 (or greater) package is available from www.st.com An STM32CubeProgrammer v2.11.0 (or greater) package is available from www.st.com An STM32HSM-V1.1 card

Note:

Refer to [4] or [5] for the supported operating systems and architectures.

# 12.3 Step-by-step execution

# 12.3.1 Build an OEM application

OEM application developers can use any IDE to build their own firmware. Note that in this use case there are different user codes, each being specific for a flash memory type (internal/external).

# 12.3.2 Perform the SFIx generation (GUI mode)

To be encrypted with the STM32 Trusted Package Creator tool, OEM firmware is provided in Bin/Hex/AXF format in addition to a CSV file to set the option bytes configuration. A 128-bit AES encryption key and a 96-bit nonce are also provided to the tool.

Note:

STM32CubeProgrammer v2.11.0 and later provide one option byte file example for each product.

It is located in the directory: STM32CubeProgrammerlvx.x.x\bin|SFI_OB_CSV_FILES

The option bytes are described in the product reference manual.

In the case of customization of a provided example file, care must be taken not to change the number of rows, or their order.

An"si" image is then generated (out.i).

# Use case 1: generation of SFlx without key area for STM32L5

Internal firmware files:

1. Add a nonsecure binary with a start address equal to 0x08040000.   
2. Add an internal binary file at Ox0C000000 (application to be executed after downloading SFlx to verify full process success by blinking an LED).   
3. Add an OTFDEC key binary at Ox0C020000 (to be used as the key in OTFD ENC-DEC).

External firmware files: add an external binary at Ox90000000 with these parameters:

Region number = 0 • Region mode = 0x2 Key address = Ox0C020000 (same as the OTFDEC key binary).

Encryption key: use the same key as STM32HSM.

Nonce file: use the same nonce as STM32HSM.

Option bytes file: use .csv contains the option-byte configuration.

RAM size: Ox19000 to split the input areas avoiding memory overflow.

![](images/52765423b4e8a7557e6fab38200b1aae2ad7f3c9b88708d35ed754fcbe36a18c.jpg)  
Figure 67. Successful SFlx generation use case 1

# Use case 2: generation of SFIx with key area for STM32L5

This is essentially the same process as test case1. The main difference is:

Add a ".kcsv" file (to be used in OTFD ENC-DEC during SFlx downloading) in the key area field, instead of using an OTFDEC key binary file.   
The key address for external firmware files is the first address of the area 'K' key file, which is 0x0C020000.

![](images/f52dc7d8b4a04efba10170a5278d2295d9b27b79115b849b0855cba1d028e5b4.jpg)  
Figure 68. Successful SFlx generation use case 2

After the generation of the SFlx image in this use case the output file contains 12 internal segments (F area), and 166 external segments (E area).

# Use case 3: generation of SFIx without key area for STM32U5

Find below an example for STM32U585xx.

Internal firmware files:

1. Add a nonsecure binary with a start address equal to 0x08100000.   
2. Add an internal binary file at Ox0C000000 (application to be executed after downloading SFlx to verify full process success by blinking an LED).   
3. Add an OTFDEC key binary at 0x0800A000 (to be used as the key in OTFD ENC-DEC).

External firmware files: add an external binary (at 0x70000000 for STM32U585xx) with these parameters:

Region number = 4 • Region mode = 1 Key address = Ox0800A000 (same as the OTFDEC key binary).

Encryption key: use the same key as STM32HSM.

Nonce file: use the same nonce as STM32HSM.

Option bytes file: use .csv contains the option-byte configuration.

RAM size: Ox55500 to split the input areas avoiding memory overflow.

![](images/1e777d3f02552d25985278c9d6889fdd96285d099db80be59f8426c1a936a9ac.jpg)  
Figure 69. Successful SFlx generation use case 3

Find below an example for STM32U59xxx, STM32U5Axxx, STM32U5Fxxx, and STM32U5Gxxx.

# Internal firmware files:

1. Add a nonsecure binary with a start address equal to 0x08100000. 2. Add an internal binary file at Ox0C000000. It is an application to be executed after downloading SFlx to verify the full process success through a blinking LED. 3. Add an OTFDEC key binary at Ox0800A000. It is used as the key in OTFD ENCDEC.

External firmware files:

Add an external binary at Ox90000000 with these parameters:

• Region number = 3   
• Region mode = 1   
• Key address = Ox0800A000. It is the same as the OTFDEC key binary. Encryption key: use the same key as STM32HSM.   
Nonce file: use the same nonce as STM32HSM.   
Option bytes file: use the .csv file that contains an option-byte configuration.   
√ RAM size: it is Ox55500 to split the input areas to avoid a memory overflow.

![](images/b6c2ed68d704407b59b60358597b0623714f533c3ec560e6589a2470fef9c052.jpg)  
Figure 70. Successful SFIx generation use case 3 for STM32U59xxx, STM32U5Axxx, STM32U5Fxxx, and STM32U5Gxxx

# Use case 4: generation of SFlx with key area for STM32U5

This is essentially the same process as test case1. The main difference is:

Add a ".kcsv" file (to be used in OTFD ENC-DEC during SFIx downloading) in the key area field, instead of using an OTFDEC key binary file.   
The key address for external firmware files is the first address of the area 'K' key file, which is 0x0800A000.

![](images/831789244c9fb8f4d25a862c71cc7da1ff5a980841228595f2f8431d3b2bc6e7.jpg)  
Figure 71. Successful SFlx generation use case 4

![](images/b9476c33d325e6c055b3b81b39331d3c976b310a1057393573abc60af92e8650.jpg)  
Figure 72. Successful SFIx generation use case 4 for STM32U59xxx, STM32U5Axxx, STM32U5Fxxx, and STM32U5Gxxx

# 12.3.3 Performing STM32HSM programming for license generation using STPC (GUI mode)

Refer to Section 11.3.3: Performing STM32HSM programming for license generation using STPC (GUI mode).

# 2.3.4 Performing STM32HSM programming for license generation using STPC (CLI mode)

Refer to Section 11.3.4: Performing STM32HSM programming for license generation using STPC (CLI mode).

# 12.3.5 Programming input conditions

Before performing an SFIx install, make sure that:

• A JTAG/SWD interface is used • The chip supports security (a security bit must be present in the option bytes)

The SFlx image is encrypted by the same key/nonce as is used in the STM32HSM provisioning.

The option bytes are:

DBank=1   
− nSWBOOT0=1   
nBOOT0=1 RDP=AA

# 2.3.6 Perform the SFlx installation using STM32CubeProgrammer

In this section, the STM32CubeProgrammer tool is used in CLI mode (the only mode so-far available for secure programming) to program the SFIx image "out.sfix" already created in the previous section.

STM32CubeProgrammer supports communication with STMicroelectronics STM32HSMs (Hardware secure modules based on smartcard) to generate a license for the connected STM32 device during SFIx install.

Using JTAG/SWD

After making sure that all the input conditions are respected, open a cmd terminal and go to <STM32CubeProgrammer_package_path>/bin, then launch the following STM32CubeProgrammer command:

STM32_Programmer_CLI.exe -c port=Swd mode=HOTPLUG -sfi protocol=static "<local_path>/out.sfix" hsm=1 slot=<slot_id> -rsse <RSSe_Path> -el <ExternalLoader_Path>

# Note:

The RSSe binary file is located in the STM32CubeProgrammer install path in the bin/RSSe folder.

Figure 73: SFlx installation success using SWD connection (1) through Figure 75: SFlx installation success using SWD connection (3) show the SFIx install via SWD execution and the STM32HSM as license generation tool in the field.

![](images/f72654969bc2e288a6213475d1c82df0f3b84db8adba9dcdb14e97be69f50d86.jpg)  
Figure 73. SFIx installation success using SWD connection (1)

![](images/c7d8f34a82fc394fff084b14a5cf03f321573e870b33bfd032058dcde5f99e9e.jpg)  
Figure 74. SFIx installation success using SWD connection (2)

![](images/cd28ce2550981493d8c2d5d37e96b63ee903149fdb8e770fc016d1d2f43b4c70.jpg)  
Figure 75. SFIx installation success using SWD connection (3)

# 13

# Example of SFIx programming scenario for STM32H5

# 13.1 Scenario overview

There are three steps during this scenario:

1. Generate an SFIx image using the STPC   
2. STM32HSM card provisioning via STPC   
3. Use STM32CubePrg to perform the SFIx process.

# 13.2 Hardware and software environment

For successful FIx programming, mehardware and sotare prerequisies ply:

An STM32H5-based board with an external flash memory and system flash security   
package (SFSP) v2.4.0 or greater   
SFI programming via SWD   
A PC running on either Windows®, Linux® Ubuntu® or Fedora®, or macOS®   
An STM32 Trusted Package Creator v2.14.0 (or greater) package is available from   
www.st.com   
An STM32CubeProgrammer v2.14.0 (or greater) package is available from   
www.st.com   
An STM32HSM-V2 smartcard

Note:

Refer to [4] or [5] for the supported operating systems and architectures.

# 13.3

# Step-by-step execution

# 13.3.1 Build an OEM application

OEM application developers can use any IDE to build their own firmware.

# 13.3.2 Perform the SFIx generation (GUI mode)

The first step to install the secure firmware on STM32H5 devices is the encryption of the user OEM firmware using the STM32 Trusted Package Creator tool. This step is done by including the following files:

• An OEM firmware at 0x08100000   
• A .csv file containing option bytes configuration   
• A 128-bit AES encryption key   
• A 96-bit nonce   
• A binary file for an external firmware file   
• OBKey files for device configuration   
• An SSFI file to integrate the STMicroelectronics SFI image   
• An OTFDEC key binary at Ox081FFFF0 (to be used as the key in OTFD ENC/DEC)

External firmware files. Add an external binary at Ox90000000 with the following parameters:

Region number = 0   
Region mode = 0x2   
Key address = Ox081FFFF0 (same as the OTFDEC key binary)

An MCSV file to insert the modules list: ./module.bin, ./LicenseV0.bin, Ox8172000

![](images/ffc3d8678683e3c440ad531a3f01527937281dacdbf3f66b8f727be69d89da82.jpg)  
Figure 76. SFIx image generation for STM32H5

# 13.3.3 Programming input conditions

Before performing an SFIx install on STM32H5 devices, make sure that:

There is an accessible external memory loader file such as MX25LM51245G_STM32H573I-DK-RevB-SFIx.stldr The chip supports security and boots on system memory   
• The product state is open: OxED   
• An RSSe binary is available   
• The STM32HSM-V2 is provisioned for the STM32H5 product

Note:

The RSSe binary file is in the STM32CubeProgrammer bin/RSSe/H5 folder.

Note:

To embed an SSFI image into the SFI image, it is recommended to follow a specific secure sequence and choose an adequate start address of the nonsecure application that depends on the SSFI configuration. See the details in STM32CubeH5 MCU Package available from www.st.com.

# 13.3.4 Perform the SFIx installation using STM32CubeProgrammer CLI

In this section, the STM32CubeProgrammer tool is used in CLI mode to program the SFlx image "out.sfix" already created in the previous section.

STM32CubeProgrammer communicates with the device through the SWD interface after it is confirmed that all the input conditions are respected.

Open a cmd terminal, go to /bin in the install path, and then launch the following command:

Using JTAG/SWD

After making sure that all the input conditions are respected, open a cmd terminal and go to <STM32CubeProgrammer_package_path>/bin, then launch the following STM32CubeProgrammer command:

STM32_Programmer_CLI.exe -C port=swd mode=hotplug ap=1   
-sfi "out.sfix" hsm=1 slot=1 -rsse   
"\RSSe\H5\enc_signed_RSSe_SFI_STM32H5_v2.0.0.0.bin"   
-el "\ExternalLoader\MX25LM51245G_STM32H573I-DK-RevB-  
SFIx.stldr"   
-mcsv ".\modules.mcsv"

![](images/4bc7d8283770d9c4ba9b8e731ab9cbc497acfacd3d4f1568467ffce55beb07f2.jpg)  
Figure 77. SFIx installation success for STM32H5

# Example of SSP programming scenario for STM32MP1

# 14.1 Scenario overview

On each SSP install step, STM32 ecosystem tools are used to manage the secure programming and SSP flow.

Three main steps are done using SSP tools:

• Encrypted secret file generation with STM32 Trusted Package Creator • STM32HSM provisioning with STM32 Trusted Package Creator • SSP procedure with STM32CubeProgrammer.

# 14.2 Hardware and software environment

The following prerequisites are needed for successful SSP programming:

an STM32MP157F-DK2 board a Micro-B USB for DFU connection • a PC running on either Windows®, Linux® Ubuntu® or Fedora®, or macOS® STM32 Trusted Package Creator v1.2.0 (or greater) package available from www.st.com STM32CubeProgrammer v2.5.0 (or greater) package available from www.st.com an STM32HSM-V2 card

Note:

Refer to [4] or [5] for the supported operating systems and architectures.

# 14.3 Step-by-step execution

# 14.3.1 Building a secret file

A secret file must be created before SSP processing. This secret file must fit into the OTP area reserved for the customer. OTP memory is organized as 32-bit words.

On an STM32MP1 microprocessor:

One OTP word is reserved for RMA password (unlock/relock): OTP 56. 37 free words are reserved for customer use. The secret size can be up to 148 bytes: OTP 59 to 95.

There is no tool or template to create this file. A 148-byte binary file must be used as the reference to construct the secret file.

# 14.3.2 Performing the SSP generation (GUI mode)

For encryption with the STM32 Trusted Package Creator tool, the secret file is provided in BIN format in addition to the RMA password values.

An OEM public key, a 128-bit AES encryption key and a 96-bit nonce are also provided to the tool.

An "ssp" image is then generated (out.ssp).

![](images/b775bbb797fa17d9be63d29f91055a0195e48172fad7991e6e9bf44669be44c6.jpg)  
Figure 78. STM32 Trusted Package Creator SSP GUI tab

# |4.3.3 Performing STM32HSM programming for license generation using STPC (GUI mode)

The OEM must provide a license generation tool to the programming house, to be used for license generation during the SSP install process. In this example, STM32HSMs are used as license generation tools in the field.

See Section 3.1.2: License mechanism for STM32HSM use and programming details.

This example uses STM32HSM-V2. The STM32HSM version can be identified before performing the programming operation by clicking the Refresh button to make the version number appear in the version field.

Note: STM32HSM-V2 must be used for STM32 MPU devices.

![](images/d01b2fbf5fbcddca1642a1aec5fb9371165c5eb908952c4cffbfe03d34db3131.jpg)  
Figure 79. Example of STM32HSM-V2 programming using STPC GUI

The STM32 Trusted Package Creator tool provides all personalization package files, ready to be used on SSP flow. To obtain all the supported packages, go to the "PersoPackages" directory residing in the tool's install path. Each file name starts with a number, which is the product ID of the device. The correct one must be selected.

# 14.3.4 SSP programming conditions

Before performing an SSP flow make sure that:

• only DFU or UART interfaces are used   
• the chip supports security the SSP image is encrypted by the same key/nonce as used in the STM32HSM provisioning step. There is an adequate Trusted Firmware-A file, which is previously signed and ready for SSP use via USB or UART interface.

# 14.3.5 Perform the SSP installation using STM32CubeProgrammer

In this step, the STM32CubeProgrammer tool is used in CLI mode (the only mode available so far for secure programming) to program the SsP image already created with STM32 Trusted Package Creator. STM32CubeProgrammer supports communication with STMicroelectronics STM32HSMs (hardware secure modules based on a smartcard) to generate a license for the connected STM32 MPU device during SSP install.

Example using USB DFU bootloader interface:

STM32_Programmer_CLI.exe -c port=usbl -ssp "out.ssp" "tf-assp-stm32mp157f-dk2-trusted.stm32" hsm=1 slot=1

All SSP traces are shown on the output console (Figure 80).

![](images/d7f3fd103137701e5758885892d1a0738136810bb00560d67d2ce88b2ddebddc.jpg)  
Figure 80. STM32MP1 SSP installation success

# Example of SSP-SFI programming scenario for STM32MP2

# 15.1 Scenario overview

On each SSP-SFI installation step, the STM32 ecosystem tools are used to manage the secure programming and the SSP flow.

Five main steps are done using SSP tools:

• Secrets generation with STM32 Trusted Package Creator • Backup memory generation with STM32 Trusted Package Creator (optional) • SSP-SFI file generation with STM32 Trusted Package Creator • STM32HSM provisioning with STM32 Trusted Package Creator SSP-SFI procedure with STM32CubeProgrammer.

# 15.2 Hardware and software environment

The following prerequisites are needed for a successful SSP-SFI programming:

An STM32MP2 board A USB-C cable for DFU connection • A PC running on either Windows®, Linux® or macOS® The STM32 Trusted Package Creator v2.17.0 (or greater) package available from www.st.com STM32CubeProgrammer v2.17.0 (or greater) package available from www.st.com • An STM32HSM-V2 card

Note:

Refer to [4] or [5] for the supported operating systems and architectures.

# 15.3 Step-by-step execution

# 15.3.1 Building a secret file

A secret file must be created before the SSP processing. This secret file must fit into the OTP area reserved for the customer. OTP memory is organized as 32-bit words.

The STM32Trusted Package Creator offers a graphical interface to edit and customize the secrets binary.

From the SSP panel, select the "Secrets Gen" tab and start the editing.

![](images/a313a2b93c6c8d478cf05fdcfc39e4a6b9256ba10a18c2406999918e999703eb.jpg)  
Figure 81. Secrets Gen Window

# 15.3.2 Building a backup memory file

It is optional to integrate a backup file into an SSP-SFI image by specifying the backup input file.

The STM32Trusted Package Creator offers a graphical interface to edit and customize the secrets of the backup memory file.

From the SSP panel, select the "Backup Gen" tab and start the editing.

If all necessary elements are present,pressing the "Generate Backup" button initiates the preparation of the image. The resulting image is saved into a binary file, which is specified in the "Output Backup binary file" field.

![](images/4db757c5b891e2ea58e9e7f8556c2b62f05a55f0cca2161fd79d8d2ed7473f51.jpg)  
Figure 82. SSP Backup memory window

# |5.3.3 Performing the SSP-SFI generation (GUI mode)

The STM32Trusted Package Creator tool GUI presents an SSP-SFI tab located in the SSP panel to generate an SSP image in SFI format. The user must fill in the input fields with valid values.

![](images/ce893007ed73f61d0b85827ec366458617c73d06d47ea52fddae7d2f50209ab7.jpg)  
Figure 83. SSP-SFI image generation window

# 15.3.4 Performing STM32HSM programming (GUI mode)

Refer to Section 14.3.3: Performing STM32HSM programming for license generation using STPC (GUI mode).

# 15.3.5 SSP-SFI programming conditions

Before performing an SSP flow make sure that:

Only DFU or UART interfaces are used. • The chip supports security to deploy the SSP flow. The SSP image is encrypted by the same key/nonce that is used in the STM32HSM provisioning step. C A trusted RSSe SSP binary provided by STMicroelectronics is used.

# 15.3.6 Perform the SSP installation using STM32CubeProgrammer

In this step, the STM32CubeProgrammer tool is used in CLI mode (in a similar way the GUI mode with the Security window can be used) to program the SSP-SFI image already created with STM32 Trusted Package Creator.

The STM32CubeProgrammer supports the communication with STMicroelectronics STM32HSMs (hardware secure modules based on a smartcard) to generate a license for the connected STM32MP2 device during the SSP installation.

Example using USB DFU bootloader interface:

STM32_Programmer_CLI.exe -c port=usbl1 -ssp "image.ssp" "EncBootExt_STM32_RSSE_SSP.bin" hsm=1 slot=1

The file EncBootExt_STM32_RSSE_SSP.bin is located in the STM32CubeProgrammer install path under the /bin/RSSe/MP25 folder.

All the SSP traces are shown on the output console.

![](images/55fcb6b8be0559b2c853d470e2a822d01437efbac308f1683db67412ec966051.jpg)  
Figure 84. SSSP-SFI installation

# 16 Reference documents

Table 3. Document references   

<table><tr><td rowspan=1 colspan=1>Reference</td><td rowspan=1 colspan=1>Document title</td></tr><tr><td rowspan=1 colspan=1>[1]</td><td rowspan=1 colspan=1>Application note Introduction to secure firmware install (SFI) for STM32 MCUs(AN4992), STMicroelectronics.</td></tr><tr><td rowspan=1 colspan=1>[2]</td><td rowspan=1 colspan=1>User manual Hardware secure module (HSM) for STM32CubeProgrammer securefirmware install (SFI) (UM2428), STMicroelectronics.</td></tr><tr><td rowspan=1 colspan=1>[3]</td><td rowspan=1 colspan=1>Application note Overview of the secure secret provisioning (SSP) on STM32MP1series (AN5510), STMicroelectronics.</td></tr><tr><td rowspan=1 colspan=1>[4]</td><td rowspan=1 colspan=1>Release note STM32CubeProgrammer release vx.y.z (RN0109),STMicroelectronics.</td></tr><tr><td rowspan=1 colspan=1>[5]</td><td rowspan=1 colspan=1>User manual STM32 Trusted Package Creator tool software description (UM2238),STMicroelectronics.</td></tr></table>

# 17 Revision history

Table 4. Document revision history   

<table><tr><td colspan="1" rowspan="1">Date</td><td colspan="1" rowspan="1">Revision</td><td colspan="1" rowspan="1">Changes</td></tr><tr><td colspan="1" rowspan="1">03-Aug-2018</td><td colspan="1" rowspan="1">1</td><td colspan="1" rowspan="1">Initial release.</td></tr><tr><td colspan="1" rowspan="1">18-Apr-2019</td><td colspan="1" rowspan="1">2</td><td colspan="1" rowspan="1">Updated publication scope from 'ST restricted' to 'Public'.</td></tr><tr><td colspan="1" rowspan="1">16-Oct-2019</td><td colspan="1" rowspan="1">3</td><td colspan="1" rowspan="1">Updated:- Section 4.1.2: License mechanism-Section 5.3.4: Performing HSM programming for licensegeneration using STPC (GUI mode)Figure 44: HSM programming GUI in the STPC tool (titlecaption)Figure 54: Example of HSM programming using STPCGUI</td></tr><tr><td colspan="1" rowspan="1">03-Feb-2020</td><td colspan="1" rowspan="1">4</td><td colspan="1" rowspan="1">Replaced occurrences of STM32L451CE withSTM32L462CE in Section 4.2.1: Secure firmwareinstallation using a bootloader interface flow.Updated document to cover secure programming withSFIx.</td></tr><tr><td colspan="1" rowspan="1">26-Feb-2020</td><td colspan="1" rowspan="1">5</td><td colspan="1" rowspan="1">Updated:-Section 4.3.1: SFI/SFIx programming using JTAG/SWDflowSection 5.3.4: Performing HSM programming for licensegeneration using STPC (GUI mode)Section 5.3.5: Performing HSM programming for licensegeneration using STPC (CLI mode)Figure 72: SFIx installation success using SWDconnection (1)- Figure 75: SFIx installation success using SWDconnection (4)</td></tr><tr><td colspan="1" rowspan="1">27-Jul-2020</td><td colspan="1" rowspan="1">6</td><td colspan="1" rowspan="1">Updated:Introduction-Section 3.1: System requirementsAdded:-Section 3.5: SSP generation process- Section 3.6.3: Steps for SSP generation (CLI)- Section 3.7.4: SSP generation using STPC in GUI mode-Section 4.2.5: STM32CubeProgrammer for SSP via abootloader interface-Section 12: Example of SSP programming scenario forSTM32MP1</td></tr><tr><td colspan="1" rowspan="1">19-Nov-2020</td><td colspan="1" rowspan="1">7</td><td colspan="1" rowspan="1">Updated:- Introduction on cover page- License mechanism general scheme- HSM programming by OEM for license distributionSection 5.3.5: Performing HSM programming for licensegeneration using STPC (CLI mode)Added:Section 4.4: Secure programming using bootloaderinterface (UART/I2C/SPI/USB)Section 6: Example of SFI programming scenario forSTM32WL</td></tr><tr><td colspan="1" rowspan="1">29-Jun-2021</td><td colspan="1" rowspan="1">8</td><td colspan="1" rowspan="1">Updated:- In the whole document, replaced STM32H7A/B bySTM32H7A3/7B3 and STM32H7B0, STM32H72/3 bySTM32H723/333 and STM32H725/335, STM32H7Bboard by STM32H7B3I-EVALReplaced BL by bootloader.Section 3.2: SFI generation process: removedreferences to RSSSection 4.1.2: License mechanism: removed FigureHSM programming toolchainSection 4.2: Secure programming using a bootloaderinterfaceSection 4.2.2: Secure module installation using abootloader interface flowSection 4.2.3: STM32CubeProgrammer for SFI using abootloader interfaceSection 4.3.1: SFI/SFIx programming using JTAG/SWDflow and Section 4.3.2: SMI programming throughJTAG/SWD flowSection 4.4: Secure programming using bootloaderinterface (UART/I2C/SPI/USB)Example of SFI programming scenarioSection 5.2: Hardware and software environment andExample of SFI programming scenario for STM32WLSection 6.2: Hardware and software environment:removed bootloader and RSS versionsSection 5.3.5: Performing HSM programming for licensegeneration using STPC (CLI mode): removed STM32L4from the list of devices that support SFI via debuginterface.Added:Support for STM32U5 Series.Section 7: Example of SFI programming scenario forSTM32U5</td></tr><tr><td colspan="1" rowspan="1">02-Aug-2021</td><td colspan="1" rowspan="1">9</td><td colspan="1" rowspan="1">Added note about CSV file in Section 3.6.1: Steps for SFIgeneration (CLl) and Figure 27: Option bytes file example.Corrected binary file names in Section 4.4: Secure pro-gramming using bootloader interface (UART/I²C/SPI/USB).Added Section 3.6.1: Steps for SFI generation (CLI).Added note about option byte file example in:Section 3.7.1: SFI generation using STPC in GUI modeSection 5.3.3: Perform the SFI generation (GUI mode)Section 6.3.2: Perform the SFI generation (GUI mode)Section 7.3.2: Perform the SFI generation (GUI mode)Section 9.3.2: Perform the SFIx generation (GUI mode)Section 10.3.2: Perform the SFIx generation (GUI mode)Section 11.3: Step-by-step executionUpdated:Corrected board name in Section 4.2: Secureprogramming using a bootloader interfaceCorrected board name in Section 7.2: Hardware andsoftware environment</td></tr><tr><td colspan="1" rowspan="1">04-Mar-2022</td><td colspan="1" rowspan="1">10</td><td colspan="1" rowspan="1">Updated Section 3.3: SFlx generation process.Added:- Section 5.3.2: Performing the option bytes file generation(GUI mode)Section 5.3.8: SFI with Integrity check (for STM32H73)</td></tr><tr><td colspan="1" rowspan="1">29-Jun-2022</td><td colspan="1" rowspan="1">11</td><td colspan="1" rowspan="1">Updated:Section 3.3: SFlx generation processSection 4.2.3: STM32CubeProgrammer for SFI using abootloader interfaceSection 10.1: Scenario overviewSection 10.2: Hardware and software environmentSection 10.3.2: Perform the SFIx generation (GUImode): STM32CubeProgrammer version, use cases 1and 2 scope STM32L5, and added subsections for usecases 3 and 4 for STM32U5, listed below.Figure 67: STPC GUI during SMI generationFigure 88: STM32 Trusted Package Creator SSP GUItabSection 12.3.4: SSP programming conditionsAdded:- Use case 3: generation of SFIx without key area forSTM32U5Use case 4: generation of SFIx with key area forSTM32U5</td></tr><tr><td colspan="1" rowspan="1">25-Nov-2022</td><td colspan="1" rowspan="1">12</td><td colspan="1" rowspan="1">Updated Section 3.2: SFI generation process.Removed "multi install" from document.</td></tr><tr><td>24-Feb-2023</td><td>13</td><td>Updated: Section 3.6: STM32 Trusted Package Creator tool in the command line interface Section 3.6.1: Steps for SFI generation (CLI) Global document update, and compatibility with the</td></tr><tr><td></td><td></td><td>STM32H5 series and extended STM32U5 series. Updated: - Figure 28: SFI generation example using an ELF file and the related command line example Figure 60: STPC GUI showing the STPC GUI during the SFI generation</td></tr><tr><td>04-Aug-2023</td><td>14</td><td>Figure 63: SFI installation via SWD execution command- line output Figure 86: Successful SFlx generation use case 1 Figure 87: Successful SFlx generation use case 2 Figure 92: SFIx installation success using SWD connection (1) Figure 93: SFIx installation success using SWD connection (2) Figure 94: SFIx installation success using SWD connection (3) Removed: Figure 83. SFIx installation success using SWD connection (4)</td></tr><tr><td>22-Mar-2024 15</td><td>Added: - Example of SFI programming scenario for STM32WBA5 - Example of SFI programming scenario for STM32H7RS</td><td>Figure 84. SFIx installation success using SWD connection (5) Added: Chapter 9: Example of SFI programming scenario for STM32H5 Chapter 14: Example of SFIx programming scenario for STM32H5 Figure 89: Successful SFlx generation use case 3 for STM32U59xxx, STM32U5Axxx, STM32U5Fxxx, and STM32U5Gxxx Figure 91: Successful SFlx generation use case 4 for STM32U59xxx, STM32U5Axxx, STM32U5Fxxx, and STM32U5Gxxx Minor text edits across the document.</td></tr><tr><td colspan="1" rowspan="1">24-Jun-2024</td><td colspan="1" rowspan="1">16</td><td colspan="1" rowspan="1">Added:- Section 8: Example of SFIA programming scenario forSTM32WBA5- Section 15: Example of SSP-SFI programming scenariofor STM32MP2</td></tr><tr><td colspan="1" rowspan="1">20-Nov-2024</td><td colspan="1" rowspan="1">17</td><td colspan="1" rowspan="1">Updated:— Section 1: General information- Section 1.2: Acronyms and abbreviations— Section 2.1: System requirements- Section 2.5: STM32 Trusted Package Creator tool in thecommand-line interfaceSection 3.2: Secure programming using a bootloaderinterfaceSection 3.1.2: License mechanismRemoved different references to SMI.</td></tr><tr><td colspan="1" rowspan="1">10-Mar-2025</td><td colspan="1" rowspan="1">18</td><td colspan="1" rowspan="1">Updated:Chapter 7: Example of SFI programming scenario forSTM32WBA5x and STM32WBA6x extended toSTM32WBA6x The Firmware key item in Section 3.1.2: LicensemechanismReferences of Figure 50: SFI installation via UARTexecution using CLI (2) and Figure 51: SFI installationvia UART execution using CLI (3)Chapter 10: Example of SFI programming scenario forSTM32H7Rx/7Sx with STM32H7Rx/7Sx to refer to themicrocontrollers in the STM32H7R3/7S3 andSTM32H7R7/7S7 lines- The entire document with STM32HSM for the hardwaresecurity module- The entire document with ST-LINK as the generic termdescribing the probe interface The AN4992 title in Chapter 16: Reference documents.</td></tr></table>

# IMPORTANT NOTICE  READ CAREFULLY

acknowledgment.

the design of purchasers' products.

No license, express or implied, to any intellectual property right is granted by ST herein.

or service names are the property of their respective owners.

I