# Introduction to SWD multi-drop for STM32 with ST-LINK

# Introduction

Arm® Cortex®-M processor.

and the device to debug. This was the first version implemented in STM32 microcontrollers.

u

![](images/fbfff4a42b4344fae94556b3ce36424d923c2f6c6ae6f293e0a62b481542b5ae.jpg)  
Figure 1. SWD multi-drop connection to multiple targets   
Table 1 lists the ST-LINK tools that support SWD multi-drop.

Table 1. Applicable products   

<table><tr><td rowspan=6 colspan=2>ReferenceDevelopment tools</td><td rowspan=1 colspan=1>Products</td></tr><tr><td rowspan=1 colspan=1>ST-LINK/V2</td></tr><tr><td rowspan=1 colspan=1></td><td rowspan=1 colspan=1>STLINK-V3MINIE</td></tr><tr><td rowspan=1 colspan=1>STLINK-V3MODS</td></tr><tr><td rowspan=1 colspan=1>STLINK-V3PWR</td></tr><tr><td rowspan=1 colspan=1>STLINK-V3SET</td></tr></table>

See Section 1 for examples of compatible target devices.

# 1 Compatible targets

SWD multi-drop is available n the TM32 targets that support SWD protocol v Compatible TM32 target ca beidentifid through their DPDPIDR register (bits [15.2]), which is detailed in their referencemanual.

In an SWD multidrop configuration, the connection sequence uses a 32-it value to select a single target to c Talu fomarg g allTearge ly if the two following conditions are met:

TARGETSEL[27.0] matches DP_TARGETIDR[27..0]. This bitfield is further called targetID in the document. Its value typically includes the STM32 DEV_ID.   
TARGETSEL[31.28] matches DP_DLPIDR[31.28]. This bitfield is further called instancelD in the document. Its value is typically 0 for compatible STM32 targets.

To find the values of DP_TARGETIDR[27..0] and DP_DLPIDR[31..28], use any of the two followig solutions:

Consult the corresponding STM32 reference manual (preferred solution).   
Dynamically read in a point-to-point context from a tool allowing such low-level accesses.

Table 2 gives a non-exhaustive list of TARGETSEL values with corresponding STM32 microcontrollers

Table 2. TARGETSEL values for STM32 MCUs implementing SWD protocol v2   

<table><tr><td rowspan=1 colspan=1>TARGETSEL</td><td rowspan=1 colspan=1>STM32 MCU references</td></tr><tr><td rowspan=1 colspan=1>0x04500041</td><td rowspan=1 colspan=1>STM32H742xx, STM32H743xx, STM32H750xx, STM32H753xx</td></tr><tr><td rowspan=1 colspan=1>0x04510041</td><td rowspan=1 colspan=1>STM32F76xxx, STM32F77xxx</td></tr><tr><td rowspan=1 colspan=1>0x04520041</td><td rowspan=1 colspan=1>STM32F72xxx, STM32F73xxx</td></tr><tr><td rowspan=1 colspan=1>0x04540041</td><td rowspan=1 colspan=1>STM32U375xx, STM32U385xx</td></tr><tr><td rowspan=1 colspan=1>Ox04550041</td><td rowspan=1 colspan=1>STM32U535xx, STM32U545xx</td></tr><tr><td rowspan=1 colspan=1>0x04590041</td><td rowspan=1 colspan=1>STM32U031xx</td></tr><tr><td rowspan=1 colspan=1>0x04740041</td><td rowspan=1 colspan=1>STM32H503xx</td></tr><tr><td rowspan=1 colspan=1>Ox04760041</td><td rowspan=1 colspan=1>STM32U5Fxxx, STM32U5Gxxx</td></tr><tr><td rowspan=1 colspan=1>Ox04780041</td><td rowspan=1 colspan=1>STM32H523xx, STM32H533xx</td></tr><tr><td rowspan=1 colspan=1>Ox04800041</td><td rowspan=1 colspan=1>STM32H7A3xx, STM32H7B0xx, STM32H7B3xx</td></tr><tr><td rowspan=1 colspan=1>0x04810041</td><td rowspan=1 colspan=1>STM32U59xxx, STM32U5Axxx</td></tr><tr><td rowspan=1 colspan=1>Ox04820041</td><td rowspan=1 colspan=1>STM32U575xx, STM32U585xx</td></tr><tr><td rowspan=1 colspan=1>Ox04830041</td><td rowspan=1 colspan=1>STM32H72xxx, STM32H73xxx</td></tr><tr><td rowspan=1 colspan=1>0x04840041</td><td rowspan=1 colspan=1>STM32H562xx, STM32H563xx, STM32H573xx</td></tr><tr><td rowspan=1 colspan=1>0x04850041</td><td rowspan=1 colspan=1>STM32H7Rxxx, STM32H7Sxxx</td></tr><tr><td rowspan=1 colspan=1>0x04860041</td><td rowspan=1 colspan=1>STM32N657xx</td></tr><tr><td rowspan=1 colspan=1>0x04890041</td><td rowspan=1 colspan=1>STM32U073xx, STM32U083xx</td></tr><tr><td rowspan=1 colspan=1>0x04920041</td><td rowspan=1 colspan=1>STM32WBA5xxx</td></tr><tr><td rowspan=1 colspan=1>0x04950041</td><td rowspan=1 colspan=1>STM32WB5MMx</td></tr><tr><td rowspan=1 colspan=1>Ox04960041</td><td rowspan=1 colspan=1>STM32WB35xx</td></tr><tr><td rowspan=1 colspan=1>0x04970041</td><td rowspan=1 colspan=1>STM32WL5xxx</td></tr><tr><td rowspan=1 colspan=1>0x04B00041</td><td rowspan=1 colspan=1>STM32WBA6xXX</td></tr></table>

The STM32 32-bit microcontrollers implementing SWD protocol v2 are based on the Arm® Cortex®M processor Arm is a registered trademark of Arm Limited (or its subsidiaries) in the US and/or elsewhere.

# 2 Compatible tools

# 2.1 ST-LINK boards and firmware

SWmultiopvailable witheollowi-snalo rob rovie hers recent enough (see Table 3):

ST-LINK/V2, including the ST-LINK/V2-ISOL variant   
STLINK-V3SET   
STLINK-V3MINIE   
STLINK-V3MODS   
STLINK-V3PWR

SWD multi-drop can also be used with STM32 boards providing a DEBUG_OUT connector from their embedded ST-LINKV2-1, STLINK-V2EC, STLINK-V3E, r STLINK-V3EC (see Table for the minimu fimware versions).

Table 3. Minimum ST-LINK firmware version for SWD multi-drop   

<table><tr><td rowspan=1 colspan=1>ST-LINK</td><td rowspan=1 colspan=1>Minimum firmware version</td></tr><tr><td rowspan=1 colspan=1>Standalone ST-LINK/V2</td><td rowspan=1 colspan=1>V2J45S7</td></tr><tr><td rowspan=1 colspan=1>Standalone ST-LINK/V2-ISOL</td><td rowspan=1 colspan=1>V2J45S7</td></tr><tr><td rowspan=1 colspan=1>Standalone STLINK-V3SET</td><td rowspan=1 colspan=1>V3J15M6B5S1</td></tr><tr><td rowspan=1 colspan=1>Standalone STLINK-V3MINIE</td><td rowspan=1 colspan=1>V3J15M6</td></tr><tr><td rowspan=1 colspan=1>Standalone STLINK-V3MODS</td><td rowspan=1 colspan=1>V3J15M6B5S1</td></tr><tr><td rowspan=1 colspan=1>Standalone STLINK-V3PWR</td><td rowspan=1 colspan=1>V4J5B1P5</td></tr><tr><td rowspan=1 colspan=1>Board with embedded ST-LINK/V2-1</td><td rowspan=1 colspan=1>V2J45M30</td></tr><tr><td rowspan=1 colspan=1>Board with embedded STLINK-V2EC</td><td rowspan=1 colspan=1>V2J45M30</td></tr><tr><td rowspan=1 colspan=1>Board with embedded STLINK-V3E</td><td rowspan=1 colspan=1>V3J15M6</td></tr><tr><td rowspan=1 colspan=1>Board with embedded STLINK-V3EC</td><td rowspan=1 colspan=1>V3J15M6</td></tr></table>

The ST-LINK firmware can be updated either from some toolchains, or with the STSW-LINKo07 software tool available from the www.st. com website.

# 2.2

# Host toolchains

The Keil® MDK-ARM third-party toolchain and STMicroelectronics' STM32CubeProgrammer (STM32CubeProg) support SWD multi-drop through T-LINK. Table 4 gives the minimum versions for SWD multi-drop support through ST-LINK.

Table 4. Toolchains minimum versions for SWD multi-drop support with ST-LINI   

<table><tr><td rowspan=1 colspan=1>Company</td><td rowspan=1 colspan=1>Toolchain</td><td rowspan=1 colspan=1>Minimum version</td><td rowspan=1 colspan=1>Website</td></tr><tr><td rowspan=1 colspan=1>Arm® Keil©(1)</td><td rowspan=1 colspan=1>MDK-ARM</td><td rowspan=1 colspan=1>5.40</td><td rowspan=1 colspan=1>www.keil.com(2)</td></tr><tr><td rowspan=1 colspan=1>STMicroelectronics</td><td rowspan=1 colspan=1>STM32CubeProgrammer (STM32CubeProg)</td><td rowspan=1 colspan=1>2.21.0</td><td rowspan=1 colspan=1>www.st.com</td></tr></table>

Keil is a registered trademark of Arm Limited (or its subsidiaries) in the US and/or elsewhere.

2. R any change, move, or inactivation of the URL or the referenced material.

# 3 General constraints of SWD multi-drop

# 3.1

# Electrical constraints

# Power supply and ground

Whe cemulte are tehemulro coguratin trmst workt voltage level and share the same GND reference.

Whult ar-uu u i pop the T_VCC signal on the STDC14 connector (pin 3). As a safety precaution, connect only one T_VCC signal to the-v vov.

# SWDIO pin

Conflicts might occur on the SwDiO pin depending on the usage context.

S-LINKeraten-ramodewhicminmizs helectrial mpac  poool erors.Howevers muavot heultvheeh point mode instead ofusing the WD multi-drop mode.Proper implementation f the WD multdrop proocol prevents such conflicts.

# 3.2 Constraints on usage

In ivversin  ais  prool hat able a glectnfowbetwee ahost n t. The SWD protocol v2 implements a method to select a single target among multiple ones simultaneously connected to the same SWD lines. The consequences are listed below.

# Single-target debug session

As  tmuioo tpemultiplesultaneous deug sessions nfferent target hat hare he s When r a new session, the user must select the target to connect to from all the targets present on the lines.

# No point-to-point mode with multiple devices

Teuermusotpt  oinpotmodestesat roviemulteviha same SWD lines. Although these devices implement the SWD protocol v2, they stll respond to the protocol v1 entry sequence. As a result, such a connection attempt causes a conflict on the SwDiO line.

It in hl iv  s reach this state. Additionally, it is unpredictable which device gains control of the line.

# Connection order with ST-LINK in shared mode

When using ST-LINK in shared mode, he first application that opens a connection with a target defines the connection mode. All subsequent applications attempting to connect must use the same mode and select the same target; otherwise, their connections fail.

# No automatic target detection

It isnot possible to autoaticallydetect at the protocol level whic targets are conected n WDmultro mTveoe thitatio,hetonplemen ecton lothatrat knoe TARGETSEL values to identify the values that receive a response.

# 3.3

# Constraints on targe

T prevtcnflc  pecalleusre eciny sglart mu with the host at any time. This requirement imposes the constraints listed below.

# No target implementing the SWD protocol v1

It is not possible to insert a target implementing the WD protocol von the WD lines.This target does not cerprehWmultrounhatelnotergCquentmiepy drive the SWDlO line and cause a conflict.

# No simultaneous targets with the same TARGETSEL

It isnot possble tnsmultiple arget hat caot beniqueyelecte by the WD multiros nc.hireuires aldevics n he es havestincRGvalues.crrent , eulorov  rg can be parallelized in SWD.

# Revision history

Table 5. Document revision history   

<table><tr><td>Date</td><td>Revision</td><td>Changes</td></tr><tr><td>06-Nov-2025</td><td>1</td><td>Initial release.</td></tr></table>

# Contents

# 1 Compatible targets

2 Compatible tools 3

2.1 ST-LINK boards and firmware .   
2.2 Host toolchains

# General constraints of SWD multi-drop 4

3.1 Electrical constraints.   
3.2 Constraints on usage   
3.3 Constraints on target

# Revision history 6

# List of tables 8

_ist of figures. 9

# List of tables

Table 1. Applicable products   
Table 2. TARGETSEL values for STM32 MCUs implementing SWD protocol v2. 2   
Table 3. Minimum ST-LINK firmware version for SWD multi-drop 3   
Table 4. Toolchains minimum versions for SWD multi-drop support with ST-LINK. 3   
Table 5. Document revision history . 6

# List of figures

Figure 1. SWD multi-drop connection to multiple targets

# IMPORTANT NOTICE  READ CAREFULLY

products and/or to this document at any time without notice.

ST, the provisions of such contractual arrangement shall prevail.

T conditions of sale in place at the time of order acknowledgment.

T the purchasers' products.

No license, express or implied, to any intellectual property right is granted by ST herein.

segment, the purchasers shall contact ST for more information.

are the property of their respective owners.