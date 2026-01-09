# Migration guide from STM32F7 Series to STMH74x/75x, STM32H72x/73x and STMH7A3/7Bx devices

# Introduction

for example:

To fulfil extended product requirements, extra demands on memory size, or an increased number of I/Os Meet cost reduction constraints that reauire a switch to smaller components and a shrunk PCB area

T following STM32H7 lines below:

Table 1. Applicable products   

<table><tr><td rowspan=1 colspan=1>Type(1)</td><td rowspan=1 colspan=1>Product lines</td></tr><tr><td rowspan=1 colspan=1>STM32H7A3/7Bx</td><td rowspan=1 colspan=1>STM32H7A3/7B3 and STM32H7B0 Value</td></tr><tr><td rowspan=1 colspan=1>STM32H72x/73x</td><td rowspan=1 colspan=1>STM32H723/733, STM32H725/735, and STM32H730 Value</td></tr><tr><td rowspan=1 colspan=1>STM32H74x/75x</td><td rowspan=1 colspan=1>STM32H742, STM32H743/753, STM32H745/755 and STM32H750(2)</td></tr></table>

1. column.

The dual core aspect of this line's devices is not considered for the purposes of this document.

provided by this application note, the user must be familiar with the STM32 microcontroller family.

For additional information, refer to the following documents available on www.st.com:

STM32F75xxx and STM32F74xxx advanced Arm®-based 32-bit MCUs reference manual (RM0385)   
STM32H745/755 and STM32H747/757 advanced Arm®-based 32-bit MCUs reference manual (RM0399)   
STM32F76xxx and STM32F77xx advanced Arm®-based 32-bit MCUs reference manual (RM0410)   
STM32H742, STM32H743/753 and STM32H750 Value line advanced Arm®-based 32-bit MCUs" reference manual   
(RM0433)   
STM32H7A3/7B3 and STM32H7B0 Value line advanced Arm®-based 32-bit MCUs reference manual (RM0455)   
STM32H723/733, STM32H725/735, and STM32H730 Value line advanced Arm®-based 32-bit MCUs reference manual   
(RM0468)

# 1 General information

# Note:

This document applies to all STM32F7 Series devices and to the STM32H74x/75x, STM32H72x/73x and STM32H7A3/7Bx lines devices. All these products are Arm®-based microcontrollers. Arm is a registered trademark of Arm Limited (or its subsidiaries) in the US and/or elsewhere.

# arm

# 2 STM32H7 devices overview

STM32H7 devices offer extra performance compared to the STM32F7 Series devices without additional complexity. STM32H7 delivers its maximum theoretical performance by taking advantage of an L1-cache regardless of whether the code is executed from the embedded flash memory or the external memory.

ST32H7 devices, as Cortex®-M7 variants, are compatible with the STM32F7 Series devices (for the common packages). This compatibility allows customers to easily migrate from STM32F7 towards STM32H7 devices and to benefit from their significantly higher performance and their advanced peripherals.

ST32H7 devices includea largeretf peripherals with advanced features and optimized power consuptin compared to the STM32F7 devices such as:

Low-power universal asynchronous receiver transmitter (LPUART)   
Single wire protocol master interface (SWPMI)   
FD controller area network (FDCAN)   
Operational amplifiers (OPAMP)   
Comparator (COMP)   
Voltage reference buffer (VREFBUF)   
Switch mode power supply step down converter (SMPS)

This migration guide covers the migration from STM32F7 Series devices towards STM32H7A3/7Bx, STM32H72x 73x, and STM32H74x/75x devices.

The new features present on STM32H7 devices but not already present on STM32F7 Series devices or other STM32H7 devices are not covered in this document. Refer to the STM32H7 devices reference manual and datasheets for more details.

The following table presents the main differences between STM32H7A3/7Bx, STM32H72x/73x, and STM32H74x/75x devices at a glance. The following sections describe the differences in detail.

Table 2. STM32H7 lines differences at a glance   

<table><tr><td rowspan=1 colspan=2>Feature</td><td rowspan=1 colspan=1>STH32H74x/75x</td><td rowspan=1 colspan=1>STH32H7Ax/7Bx</td><td rowspan=1 colspan=1>STH32H72x/73x</td></tr><tr><td rowspan=1 colspan=2>Core</td><td rowspan=1 colspan=1>Arm Cortex-M7, MPU, DP-FPU,L1 16KB-D/16KB-IARM Cortex-M4, MPU, SP-FPU,ART</td><td rowspan=1 colspan=1>Arm Cortex-M7, MPU, DP-FPU, L1 16KB-D/16KB-I</td><td rowspan=1 colspan=1>Arm Cortex-M7, MPU, DP-FPU,L1 32KB-D/32KB-I</td></tr><tr><td rowspan=1 colspan=2>Operating range</td><td rowspan=1 colspan=1>1.62 to 3.6 V andTj-40 to +125° CUp to +140° C with SMPSVOS1 limited to 125°Vcore @VOSO:Tj limited to 105°C,VDD min 1.7 VNo SMPS</td><td rowspan=1 colspan=1>1.62 to 3.6 V and Tj—40 to+130°Vcore @VOS0:Tj limited to 105°VDD min 1.7 V</td><td rowspan=1 colspan=1>1.62 to 3.6 V andTj-40 to +125° CUp to 140° C with SMPSVOS1 up to 140°Vcore @VOSO:Tj limited to 105°VDD min 1.7 V LDOVDD min 2.2 V SMPS</td></tr><tr><td rowspan=1 colspan=2>Cortex-M7 frequency/DDMIPS</td><td rowspan=1 colspan=1>480 MHz / 1027 DMIPS in VOS0400 MHz / 856 DMIPS in VOS1</td><td rowspan=1 colspan=1>280 MHz / 599 DMIPS inVOSO225 MHz / 481 DMIPS inVOS1</td><td rowspan=1 colspan=1>550 MHz / 1177 DMIPS in VOS0400 MHz / 856 DMIPS in VOS1</td></tr><tr><td rowspan=1 colspan=2>AXI and AHB maxfrequency</td><td rowspan=1 colspan=1>240 MHz</td><td rowspan=1 colspan=1>280 MHz</td><td rowspan=1 colspan=1>275 MHz</td></tr><tr><td rowspan=1 colspan=2>APB max frequency</td><td rowspan=1 colspan=1>120 MHz</td><td rowspan=1 colspan=1>140 MHz</td><td rowspan=1 colspan=1>137.5 MHz</td></tr><tr><td rowspan=1 colspan=1>Debug</td><td rowspan=1 colspan=1>SWDIJTAG/ETM</td><td rowspan=1 colspan=1>I//4 Kbytes</td><td rowspan=1 colspan=1>I/I/4 Kbytes</td><td rowspan=1 colspan=1>I //2 Kbytes</td></tr><tr><td rowspan=1 colspan=2>Low-power modes</td><td rowspan=1 colspan=1>Sleep, Stop, Standby, Vbat</td><td rowspan=1 colspan=1>Sleep, Stop, Retention,Standby, Vbat</td><td rowspan=1 colspan=1>Sleep, Stop, Standby, Vbat</td></tr></table>

# STM32H74x/75x devices

The migration from STM32F7 Series devices towards STM32H743/753 devices is covered in detail in the application note Migration of microcontroller applications from STM32F7 Series to STM32H743/753 Line (AN4936).

The maximum theoretical performance of the STM32H74x/75x devices Cortex® -M7 core is 1414 CoreMark / 1027 DMIPS at 480 MHZ fcPU.

When compared to other STM32H7 devices, STM32H74x/75x devices offer the following additional features:

one Cortex®-M4 (STM32H745/755 only)   
one high-resolution timer   
one additional 16b ADC   
MIPI-DSI interface for driving the DSI display (STM32H747/757)   
two additional SAI   
one additional USB (FS)

When compared to STM32H72x/73x devices, STM32H74x/75x devices offer the following additional features:

additional flash and RAM memory one additional passive tamper additional RAM for debug trace

When compared to STM32H7A3/7Bx devices, STM32H74x/75x devices ofer the following additional features:

• two additional low-power timers.

# STM32H72x/73x devices overview

The maximum theoretical performance of the STM32H72/73x devices Cortex® -M7 core is 2778CoreMark / 1177 DMIPS at 550 MHz fcPU.

STM32H72x/73x devices are the fastest STM32H7 Series devices.

When compared to other STM32H7 devices, STM32H72x/73x devices offer the following additional features:

more data and instruction cache   
possibility to increase instruction tightly coupled memory size   
FMAC (filtering) and Cordic (trigonometric) blocks for mathematical acceleration   
low pin-count package (UFQFPN68)   
more 32b timers, FDCAN, UART, USART, I2C   
one low-power 12b ADC in the low-power domain   
increased acceptable temperature at high frequency (400 MHz)

When compared to STM32H74x/75x devices, STM32H72/73x devices offer the following additional features:

two OCTOSPI interfaces, instead of a single QUADSPI   
possibility to store encrypted code or data on external Octo-SPI memories (for STM32H73x devices)   
a parallel synchronous slave interface (PSSI)   
a digital temperature sensor

When compared to STM32H7A3/7Bx devices, STM32H72x/73x devices ofer the following additional features:

Ethernet two low-power timers added.

# 2.3 STM32H7A3/7Bx devices

The maximum theoretical performance of the STM32H7A3/7Bx devices Cortex® -M7 core is 1414 CoreMark / 599 DMIPS at 280-MHZ fcPU.

ST32H7A3/7Bx devices are also the entry point of the wider STM32H7 Series devices, which can be seen as aeplaereneomeih peoey eatu advanced platform.

When compared to other STM32H7 devices, STM32H7A3/7Bx devices offer the following additional features:

further optimized power consumption, significant in the low-power modes   
simplification of the power domains   
increased internal RAM size, very useful for graphics applications   
DFSDM increased to nine filters with dedicated DMA   
graphical oriented memory management unit (GFXXMMU)   
one DAC in low-power domain   
new tampers and active tamper which increases the security level

When compared to STM32H743/753 devices, STM32H7A3/7Bx devices offer the following additional features:

two OCTOSPI interfaces, instead of a single QUADSPI   
possibility to store encrypted code or data on external Octo-SPI memories (for STM32H7B3 devices)   
a parallel synchronous slave interface (PSSI)   
a digital temperature sensor

When compared to STM32H72x/73x devices, STM32H7A3/7Bx devices ofer the following additional features:

increased flash memory size   
jpeg decoder   
DFSDM increased to nine filters with dedicated DMA   
graphical oriented memory management unit (GFXXMMU) additional RAM for debug trace.

# System architecture differences between STM32F7 and STM32H7 Series

STM32F7 Series devices have one single available domain: an embedded AHB bus matrix.

In STM32H72x/73x and STM32H74x/75x devices there are three domains: an AXI bus matrix and two AHB bus matrices. Bus bridges permit the interconnection of the bus masters with the bus slaves:

D1 domain: is the high bandwidth / high performance domain with the Cortex-M7 core and acceleration mechanisms. This domain encompasses the high-bandwidth features and the smart management thanks to the AXI bus matrix.   
D2 domain: is the "I/O processing" domain. It encompasses most peripherals that are less bandwidth demanding.   
D domain: it embeds up to 64-Kbyte RAM and has a subset of peripherals torun the basicfunctions while the domains 1 and 2 can be shut-off to save power (autonomous mode).

For the STM32H7A3/7Bx devices, the D1 and D2 domains are merged in a single domain called CD domain (or CPU domain) and the D3 domain evolved into a domain called SRD domain (or smart-run domain).

CD domain: the CPU domain encompasses the Cortex-M7 core, the AXI bus matrix, an AHB bus matrx and most of the peripherals.

SRD domain: it embeds a 32-Kbyte RAM and some peripherals to run basic functions while the CPU domain is in low-power mode (autonomous mode). For STM32H7A37Bx devices the power consumption in autonomous and Stop modes of this domain has been further optimized.

The differences in power modes are addressed on the Power (PWR) section of this application note.

T b eonhent gultesn e Series, STM32H74x/75x, STM32H72x/73x and STM32H7A3/7Bx devices.

Table 3. Available bus matrix on STM32F7 Series, STM32H74x/75x, STM32H72x/73x and STM32H7A3/7Bx devices   

<table><tr><td rowspan=1 colspan=1>Device</td><td rowspan=1 colspan=1>AHB bus matrix</td><td rowspan=1 colspan=1>AXI bus matrix</td></tr><tr><td rowspan=1 colspan=1>STM32F7 Series</td><td rowspan=1 colspan=1>1</td><td rowspan=1 colspan=1>NA</td></tr><tr><td rowspan=1 colspan=1>STM32H74x/75x and STM32H72x/73x</td><td rowspan=1 colspan=1>2</td><td rowspan=1 colspan=1>1</td></tr><tr><td rowspan=1 colspan=1>STM32H7A3/7Bx</td><td rowspan=1 colspan=1>2</td><td rowspan=1 colspan=1>1</td></tr></table>

![](images/2de50fcf347f74c09d687168ee366b5933575a97b858a615330defa6963634e4.jpg)  
Figure 1. STM32F7 Series devices system architecture

# Note:

I/D cache size:

For STM32F74xxx and STM32F75xxx devices: 4 Kbytes.   
For STM32F72xxx and STM32F73xxx devices: 8 Kbytes.   
For STM32F76xxx and STM32F77xxx devices: 16 Kbytes.

![](images/82701040348e0d1301ea67faa9e6e0ecfeeb9fc6924fb8b17da3504d6d6ffc05.jpg)  
Figure 2. STM32H74x/75x devices system architecture

MSv44011V13

STM32H74x/75x devices supports 16-Kbyte instruction cache and 16-Kbyte data cache.

![](images/44b6c5d3fb2aab426be4917804bb4749436766502de2387409cf8dcc8cfc24af.jpg)  
Figure 3. STM32H72x/73x devices system architecture

Vote: STM32H72x/73x devices supports 32-Kbyte instruction cache and 32-Kbyte data cache.

![](images/03122f86bbc0333e36f7ef4ffe0eca4b559abb28fd0faf006a5df3c7c6137a57.jpg)  
Figure 4. STM32H7A3/7Bx devices system architecture   
STM32H7B0x support a single bank (flash Bank1 only)

Note:

# 4 Hardware migration

# 4.1

# Available packages

The available packages on STM32F7 Series, STM32H74x/75x, STM32H72x/73x and STM32H7A3/7Bx devices are listed in the table below.

STM32H74x/75x, STM32H72x/73x and STM32H7A3/7Bx devices support the switched-mode power supply (SMP) step-down converter available in some speciic packages, which are not compatible with the legacy packages (see table below and refer to Figure 6).

Table 4. Available packages on STM32F7 Series, STM32H74x/75x, STM32H72x/73x and STM32H7A3/7Bx devices   

<table><tr><td rowspan=1 colspan=1>Package</td><td rowspan=1 colspan=4>STM32F7 Series</td><td rowspan=1 colspan=1>STM32H74x/75x</td><td rowspan=1 colspan=2>STM32H72x/73x</td><td rowspan=1 colspan=1>STM32H7A3/7Bx</td><td rowspan=1 colspan=1>Regulator</td></tr><tr><td rowspan=1 colspan=1>LQFP64</td><td></td><td rowspan=1 colspan=3></td><td rowspan=1 colspan=1>NA</td><td rowspan=1 colspan=2>NA</td><td rowspan=4 colspan=1>Available</td><td rowspan=11 colspan=1>LDO(1)</td></tr><tr><td rowspan=1 colspan=1>LQFP100</td><td rowspan=4 colspan=4>Available</td><td rowspan=3 colspan=1>Available</td><td rowspan=3 colspan=2>Available</td></tr><tr><td rowspan=1 colspan=1>TFBGA100</td></tr><tr><td rowspan=1 colspan=1>LQFP144</td></tr><tr><td rowspan=1 colspan=1>UFBGA144</td><td rowspan=1 colspan=1>NA</td><td rowspan=1 colspan=2></td><td rowspan=2 colspan=1>NA</td></tr><tr><td rowspan=1 colspan=1>UFBGA169</td><td rowspan=1 colspan=4>NA</td><td rowspan=4 colspan=1>Available</td><td rowspan=5 colspan=2>NA</td></tr><tr><td rowspan=1 colspan=1>UFBGA176+25</td><td rowspan=4 colspan=4>Available</td><td rowspan=2 colspan=1>Available</td></tr><tr><td rowspan=1 colspan=1>LQFP176</td></tr><tr><td rowspan=1 colspan=1>LQFP208</td><td rowspan=1 colspan=1>NA</td></tr><tr><td rowspan=1 colspan=1>TFBGA216</td><td rowspan=1 colspan=1>NA</td><td rowspan=1 colspan=1>Available</td></tr><tr><td rowspan=1 colspan=1>TFBGA240</td><td rowspan=1 colspan=4></td><td rowspan=1 colspan=1>Available</td><td rowspan=1 colspan=2>NA</td><td rowspan=2 colspan=1>NA</td></tr><tr><td rowspan=1 colspan=1>VFQFPN68 SMPS</td><td rowspan=1 colspan=3></td><td rowspan=3 colspan=1></td><td rowspan=3 colspan=1>NA</td><td rowspan=1 colspan=2></td><td rowspan=9 colspan=1>LDO/SMPS/regulator bypass</td></tr><tr><td rowspan=1 colspan=1>LQFP100 SMPS</td><td></td><td></td><td></td><td rowspan=5 colspan=2>Available</td><td rowspan=6 colspan=1>Available</td></tr><tr><td rowspan=1 colspan=1>TFBGA100 SMPS</td><td rowspan=1 colspan=3></td></tr><tr><td rowspan=1 colspan=1>LQFP144 SMPS</td><td></td><td rowspan=1 colspan=3></td><td rowspan=1 colspan=1>Available</td></tr><tr><td rowspan=1 colspan=1>UFBGA169 SMPS</td><td rowspan=3 colspan=4>NA</td><td rowspan=1 colspan=1>NA</td></tr><tr><td rowspan=1 colspan=1>UFBGA176+25SMPS</td><td rowspan=2 colspan=1>Available</td></tr><tr><td rowspan=1 colspan=1>LQFP176 SMPS</td><td rowspan=1 colspan=2></td><td rowspan=1 colspan=2></td></tr><tr><td rowspan=1 colspan=1>LQFP208 SMPS</td><td rowspan=1 colspan=3></td><td rowspan=2 colspan=1></td><td rowspan=1 colspan=1></td><td rowspan=1 colspan=2>NA</td><td rowspan=1 colspan=1></td><td rowspan=1 colspan=1>NA</td></tr><tr><td rowspan=1 colspan=1>TFBGA225 SMPS</td><td></td><td></td><td></td><td rowspan=1 colspan=1>NA</td><td rowspan=1 colspan=2></td><td rowspan=1 colspan=1>Available</td></tr><tr><td rowspan=1 colspan=1>WLCSPxxx</td><td></td><td rowspan=1 colspan=8>Specific for each device</td></tr></table>

STM32F7 Series and STM32H7A3/7Bx Ines devices can be used in Regulator bypass mode.

# 4.2 Pinout compatibility

STM32F7 Series devices and STM32H74x/75x devices are pin to pin compatible with the STM32H7A3/7Bx devices (with some restrictions for the LQFP64, TFBGA100, LQFP176, UFBGA176 and TFBGA216 packages). In STM32H72x/73x devices, LQFP100 SMPS pin 72 is VCAP whereas it is PE0 for STM32H7A3/7Bx.

In STM32H7A3/7Bx devices, a second VCAP pin is added for the LQFP64 package; in consequence, several GPIOs are no longer compatible with STM32F7 Series devices. See below table and figure for more details.

Table 5. LQFP64 package compatibility between STM32F7 Series and STM32H7A3/7Bx devices   

<table><tr><td rowspan=1 colspan=1>Package</td><td rowspan=1 colspan=1>Pin</td><td rowspan=1 colspan=1>STM32F7 Series</td><td rowspan=1 colspan=1>STM32H7A3/7Bx</td></tr><tr><td rowspan=9 colspan=1>LQFP64</td><td rowspan=1 colspan=1>38</td><td rowspan=1 colspan=1>PC7</td><td rowspan=1 colspan=1>PC7</td></tr><tr><td rowspan=1 colspan=1>39</td><td rowspan=1 colspan=1>PC8</td><td rowspan=1 colspan=1>PC9</td></tr><tr><td rowspan=1 colspan=1>40</td><td rowspan=1 colspan=1>PC9</td><td rowspan=1 colspan=1>PA8</td></tr><tr><td rowspan=1 colspan=1>41</td><td rowspan=1 colspan=1>PA8</td><td rowspan=1 colspan=1>PA9</td></tr><tr><td rowspan=1 colspan=1>42</td><td rowspan=1 colspan=1>PA9</td><td rowspan=1 colspan=1>PA10</td></tr><tr><td rowspan=1 colspan=1>43</td><td rowspan=1 colspan=1>PA10</td><td rowspan=1 colspan=1>PA11</td></tr><tr><td rowspan=1 colspan=1>44</td><td rowspan=1 colspan=1>PA11</td><td rowspan=1 colspan=1>PA12</td></tr><tr><td rowspan=1 colspan=1>45</td><td rowspan=1 colspan=1>PA12</td><td rowspan=1 colspan=1>PA13</td></tr><tr><td rowspan=1 colspan=1>46</td><td rowspan=1 colspan=1>PA13</td><td rowspan=1 colspan=1>VCAP</td></tr></table>

![](images/7081c21b8fb08b646d14dcec245c7e5dae801e1a0f99bf8b8531d395484c4bd1.jpg)  
Figure 5. LQFP64 package compatibility

For the TFBGA100, LQFP176, UFBGA176 and TFBGA216 packages, the BYPASS_REG pin is replaced in the STM32H7 Series with a VSS pin.

For the STM32F7 Series devices, the BYPASS_REG pin connected to VDD permits to select the mode where the internal regulator is switched off and the core supply is externally provided.

For the STM32H Series devices, there is o dedicated pin that defines if the regulator is in bypass mode whc regulator)iareus Iisdone troh software t systemstarup.oth LDOn MPregulator arnfo (see Figure 6).

# Note:

Speal care has to be taken  an STM32F7 Seris device is replaced with an ST32H7 device on a PCB bord where the BYPASS_REG pin is set to VDD (see the table below).

The following table and figure illustrate the BYPASS_REG pin incompatibility in TFBGA100, LQFP176, UFBGA176 and TFBGA216 packages and the system supply configuration on the STM32F7 Series devices and STM32H74x/75x devices.

Table 6. BYPASS_REG pin incompatibility between STM32F7 Series, STM32H74x/75x, STM32H72x/73x and STM32H7A3/7Bx devices   

<table><tr><td rowspan=1 colspan=1>Package</td><td rowspan=1 colspan=1>Pinlball</td><td rowspan=1 colspan=1>STM32F7Series</td><td rowspan=1 colspan=1>STM32H74xl75x</td><td rowspan=1 colspan=1>STM32H72xl73x</td><td rowspan=1 colspan=1>STM32H7A3/7Bx</td><td rowspan=1 colspan=1>Comment</td></tr><tr><td rowspan=1 colspan=1>TFGA100</td><td rowspan=1 colspan=1>Ball6</td><td rowspan=4 colspan=1>BYPASS_REG</td><td rowspan=1 colspan=1>VSS</td><td rowspan=1 colspan=1>VSS</td><td rowspan=4 colspan=1>VSS</td><td rowspan=4 colspan=1>Impacts only the boardsdesigned with STM32F7Series devices in the regulatorbypass mode(BYPASS_REG set to VDD)</td></tr><tr><td rowspan=1 colspan=1>LQFP176</td><td rowspan=1 colspan=1>Pin48</td><td rowspan=1 colspan=1>VSS</td><td rowspan=1 colspan=1>NA</td></tr><tr><td rowspan=1 colspan=1>UFBGA176+25</td><td rowspan=1 colspan=1>BallL</td><td rowspan=1 colspan=1>VSS</td><td rowspan=1 colspan=1>NA</td></tr><tr><td rowspan=1 colspan=1>TFBGA216</td><td rowspan=1 colspan=1>BallL5</td><td rowspan=1 colspan=1>NA</td><td rowspan=1 colspan=1>NA</td></tr></table>

![](images/aba3b545fb3e0f119fe862baaa49fd46928451598465b42fdc6b94bd475e46f1.jpg)  
1. LDO Supply

![](images/8f58698372711f080298ae13c00edd221e8233d377912a47bb3ecee3b0b2de23.jpg)  
Figure 6. System supply configuration on STM32H74x/75x and STM32H7A3/7Bx devices with SMPS   
2 Direct SMPS Supply

![](images/09ee937567424aad31d540155bed0a362e8b28a76a43fd99618c1989107fd618.jpg)  
SMPS supplies LDO (No External supply)

![](images/56e66a95a8a11b93a9bf51f25db9d2b4a30e4b3b2e44b56e7156bb3988a73e6c.jpg)  
External SMPS supply, supplies LDO

![](images/45fe561201720728a68b205fa239b4b876b249e409f55c44fb852432f3a33cc7.jpg)  
5 External SMPS Supply & Bypass

![](images/ba2b472f79250c1875ab390affbb16c5fdbce1663118671186e7afd5c16c8858.jpg)

![](images/4d98d67d1afc0d7f74276c5b7aaf65e8e8d881d6a03832251f21c9202d829ebd.jpg)  
Figure 7. System supply configuration on STM32H74x/75x and STM32H7A3/7Bx devices without SMPS

# 4.3

# System bootloader

The system bootloader is located in the system memory, programmed by ST during production. The system b yi Mo provided in the following table:

Table 7. STM32F7 Series, STM32H74x/75x, STM32H72x/73x and STM32H7A3/7Bx devices bootloader communication peripherals   

<table><tr><td rowspan=1 colspan=1>System bootloaderperipherals</td><td rowspan=1 colspan=1>STM32F7 Seriesl/0 pin</td><td rowspan=1 colspan=1>STM32H74x/75x I/O pin</td><td rowspan=1 colspan=1>STM32H7A3/7Bx I/O pin</td><td rowspan=1 colspan=1>STM32H72x/73x I/O pin</td></tr><tr><td rowspan=1 colspan=1>DFU</td><td rowspan=1 colspan=4>USB OTG FS (PA11 / PA12) in device mode</td></tr><tr><td rowspan=1 colspan=1>USART1</td><td rowspan=1 colspan=4>PA9 / PA10</td></tr><tr><td rowspan=1 colspan=1>USART 2</td><td rowspan=1 colspan=1>NA</td><td rowspan=1 colspan=3>PA2 /PA3</td></tr><tr><td rowspan=1 colspan=1>USART3</td><td rowspan=1 colspan=1>PB10 /PB11PC10 /PC11</td><td rowspan=1 colspan=2>PB10 / PB11</td><td rowspan=1 colspan=1>PB10 /PB11PD8 / PD9</td></tr><tr><td rowspan=1 colspan=1>I2C1</td><td rowspan=1 colspan=4>PB6 / PB9</td></tr><tr><td rowspan=1 colspan=1>I2C2</td><td rowspan=1 colspan=4>PFO /PF1</td></tr><tr><td rowspan=1 colspan=1>I2C3</td><td rowspan=1 colspan=4>PA8 / PC9</td></tr><tr><td rowspan=1 colspan=1>SPI1</td><td rowspan=1 colspan=4>PA7 / PA6 / PA5 / PA4</td></tr><tr><td rowspan=1 colspan=1>SPI2</td><td rowspan=1 colspan=3>PI3 / PI2 / PI1 / PI0</td><td rowspan=1 colspan=1>NA</td></tr><tr><td rowspan=1 colspan=1>SPI3</td><td rowspan=1 colspan=1>NA</td><td rowspan=1 colspan=3>PC12 / PC11/PC10 / PA15</td></tr><tr><td rowspan=1 colspan=1>SPI4</td><td rowspan=1 colspan=4>PE14 / PE13 / PE12 / PE11</td></tr><tr><td rowspan=1 colspan=1>FDCAN1</td><td rowspan=1 colspan=1>PB5 /PB13 (1)PD0 /PD1(2)</td><td rowspan=1 colspan=1>NA</td><td rowspan=1 colspan=1>PH13 / PH14PD1/PD0</td><td rowspan=1 colspan=1>PH13 /PH14PD1 /PD0</td></tr></table>

1. Available on the STM32F74xxx/75xxx and STM32F76xxx/77xxx devices. 2 Available on the STM32F72xxx/73xxx devices.

# 5 Boot mode compatibility

The STM32F7 Series devices, the STM32H74x/75x, STM32H72x/73x, and the STM32H7A3/7Bx devices boot spaces are based on BOoT0 and boot address option bytes as described in the table below.

For the STM32F7 Series devices, the boot base address supports any address in the range from Ox0000 0000 to 0x3FFF FFFF while in STM32H74x/75x, STM32H72x/73x, and the STM32H7A3/7Bx, the boot base address supports any address in the range from 0x0000 0000 to 0x3FFF 0000.

Table 8. Boot mode compatibility between STM32F7 Series, STM32H74x/75x, STM32H72x/73x, and STM32H7A3/7Bx devices   

<table><tr><td rowspan=1 colspan=2>Boot mode selection</td><td rowspan=2 colspan=1>STM32F7 Series</td><td rowspan=2 colspan=1>STM32H74x/75x, STM32H72x/73x,and STM32H7A3/7Bx</td></tr><tr><td rowspan=1 colspan=1>Boot</td><td rowspan=1 colspan=1>Boot address option bytes</td></tr><tr><td rowspan=1 colspan=1>0</td><td rowspan=1 colspan=1>BOOT_ADDO[15:0]</td><td rowspan=1 colspan=1>Boot address defined by user optionbyte BOOT_ADDO[15:0]ST programmed value: flash on ITCMat 0x0020 0000</td><td rowspan=1 colspan=1>Boot address defined by user optionbyte BOOT_ADDO[15:0]ST programmed value: flash memoryat 0x0800 0000</td></tr><tr><td rowspan=1 colspan=1>1</td><td rowspan=1 colspan=1>BOOT_ADD1[15:0]</td><td rowspan=1 colspan=1>Boot address defined by user optionbyte BOOT_ADD1[15:0]ST programmed value: Systembootloader at 0x0010 0000</td><td rowspan=1 colspan=1>Boot address defined by user optionbyte BOOT_ADD1[15:0]ST programmed value: Systembootloader at 0x1FF0 0000</td></tr></table>

# 6 Peripheral migration

# 6.1

# STM32 product cross-compatibility

The STM32 microcontrollers embed a set of peripherals, which can be classed in three categories:

The first category is for the peripherals that are by definition common to all products. Those peripherals aential eyhavee amstructure gistes,a conol bsThe nee  pero y fiarehange tokeehesamectinalityat heplcation lve ermigratinAllheeaturs behavior remain the same.   
The second category is for the peripherals that are shared by all STM32 products but have only minor i t and does not need any significant new development effort.   
The third category is for peripherals that have been considerably changed from one product toanother (new arhitecture, new features. For this category of peripherals, the migration requires a new development at application level.

This table below shows the STM32 peripheral compatibility between the STM32F7 Series, STM32H74x/75x and STM32H7A3/7Bx devices. The software compatibility mentioned in this table refers only to the register description forow-eveldrivers.The Cube hardware abstraction layer HAL)iscompatible between 32F7 Series devices, STM32H74x/75x and STM32H7A3/7Bx devices.

Table 9. Peripheral summary for STM32F7 Series, STM32H74x/75x, STM32H72x/73x, and STM32H7A3/7Bx devices   

<table><tr><td colspan="2" rowspan="1">Peripheral</td><td colspan="1" rowspan="1">STM32F7Series</td><td colspan="1" rowspan="1">STM32H74x/75x</td><td colspan="1" rowspan="1">STM32H7A3/7Bx</td><td colspan="1" rowspan="1">STM32H72x/73x</td><td colspan="1" rowspan="1">Compatibility/comments</td></tr><tr><td colspan="2" rowspan="1">Power supply</td><td colspan="1" rowspan="1">•   Powersupply for s:171 to3.6 VInternalregulatorD =1.7 to3.6 V</td><td colspan="3" rowspan="1">•    Power supply for l/Os: 1.62 to 3.6 V•    Internal regulator VDDLDO = 1.62 to 3.6 VSMPS step down converterVDDSMPS = 1.62 to 3.6 V</td><td colspan="1" rowspan="1"></td></tr><tr><td colspan="2" rowspan="1">Maximum frequency</td><td colspan="1" rowspan="1">216 MHz</td><td colspan="1" rowspan="1">480 MHz</td><td colspan="1" rowspan="1">280 MHz</td><td colspan="1" rowspan="1">550 MHz</td><td colspan="1" rowspan="1"></td></tr><tr><td colspan="2" rowspan="1">MPU region number</td><td colspan="1" rowspan="1">8</td><td colspan="2" rowspan="1">16</td><td colspan="1" rowspan="1"></td><td colspan="1" rowspan="1"></td></tr><tr><td colspan="2" rowspan="1">Flash memory</td><td colspan="3" rowspan="1">Up to 2 Mbytes single or dual bank</td><td colspan="1" rowspan="1">Up to 1Mbytessingle bank</td><td colspan="1" rowspan="1">With ECC protectionfor STM32H7 Seriesdevices</td></tr><tr><td colspan="1" rowspan="6">SRAM</td><td colspan="1" rowspan="1">System</td><td colspan="1" rowspan="1">512 Kbytes</td><td colspan="1" rowspan="1">~1 Mbyte(992 Kbytes)</td><td colspan="1" rowspan="1">~1.3 Mbytes(1312 Kbytes)</td><td colspan="1" rowspan="1">564 Kbytes</td><td colspan="1" rowspan="1">With ECCprotection forSTM32H72/72/724/75,ECC protection onTCM and cache onlyfor STM32H7A/7B</td></tr><tr><td colspan="1" rowspan="1">ITCM</td><td colspan="1" rowspan="1">16 Kbytes</td><td colspan="2" rowspan="1">64 Kbytes</td><td colspan="1" rowspan="1">64 Kbytes to256 Kbytes</td><td colspan="1" rowspan="1"></td></tr><tr><td colspan="1" rowspan="1">DTCM</td><td colspan="3" rowspan="1">128 Kbytes</td><td colspan="1" rowspan="1"></td><td colspan="1" rowspan="1">-</td></tr><tr><td colspan="1" rowspan="1">Data cache</td><td colspan="3" rowspan="1">16 Kbytes</td><td colspan="1" rowspan="1">32 Kbytes</td><td colspan="1" rowspan="1">-</td></tr><tr><td colspan="1" rowspan="1">Instructioncache</td><td colspan="3" rowspan="1">16 Kbytes</td><td colspan="1" rowspan="1">32 Kbytes</td><td colspan="1" rowspan="1"></td></tr><tr><td colspan="1" rowspan="1">Backup</td><td colspan="4" rowspan="1">4 Kbytes</td><td colspan="1" rowspan="1"></td></tr><tr><td colspan="1" rowspan="2">Commonperipherals</td><td colspan="1" rowspan="1">FMC</td><td colspan="4" rowspan="1">1</td><td colspan="1" rowspan="1"></td></tr><tr><td colspan="1" rowspan="1">QUADSPI</td><td colspan="2" rowspan="1">1</td><td colspan="2" rowspan="1">NA</td><td colspan="1" rowspan="1"></td></tr><tr><td colspan="1" rowspan="2">Commonperipherals</td><td colspan="1" rowspan="1">OCTOSPI</td><td colspan="2" rowspan="1">NA</td><td colspan="2" rowspan="1">2</td><td colspan="1" rowspan="1">All QUADSPI featuresare covered byOCCTOSPI</td></tr><tr><td colspan="1" rowspan="1">Ethernet</td><td colspan="2" rowspan="1">1</td><td colspan="1" rowspan="1">NA</td><td colspan="1" rowspan="1">1</td><td colspan="1" rowspan="1"></td></tr><tr><td colspan="1" rowspan="5">Timers</td><td colspan="1" rowspan="1">Highresolution</td><td colspan="1" rowspan="1">NA</td><td colspan="1" rowspan="1">1</td><td colspan="2" rowspan="1">NA</td><td colspan="1" rowspan="1"></td></tr><tr><td colspan="1" rowspan="1">Generalpuupose</td><td colspan="3" rowspan="1">10</td><td colspan="1" rowspan="1">12</td><td colspan="1" rowspan="1"></td></tr><tr><td colspan="1" rowspan="1">PWM</td><td colspan="2" rowspan="1"></td><td colspan="2" rowspan="1">2</td><td colspan="1" rowspan="1"></td></tr><tr><td colspan="1" rowspan="1">Basic</td><td colspan="2" rowspan="1"></td><td colspan="2" rowspan="1">2</td><td colspan="1" rowspan="1"></td></tr><tr><td colspan="1" rowspan="1">Low-power</td><td colspan="1" rowspan="1">1</td><td colspan="1" rowspan="1">5</td><td colspan="1" rowspan="1">3</td><td colspan="1" rowspan="1">5</td><td colspan="1" rowspan="1"></td></tr><tr><td colspan="1" rowspan="1">RNG</td><td colspan="1" rowspan="1"></td><td colspan="1" rowspan="1"></td><td colspan="1" rowspan="1"></td><td colspan="2" rowspan="1">Yes</td><td colspan="1" rowspan="1"></td></tr><tr><td colspan="1" rowspan="16">Communicationinterfaces</td><td colspan="1" rowspan="1">SPI//2S</td><td colspan="1" rowspan="1">4/3</td><td colspan="1" rowspan="1">6/3</td><td colspan="2" rowspan="1">6/4</td><td colspan="1" rowspan="1">Wakeup fromstop capability forSTM32H7 Series</td></tr><tr><td colspan="1" rowspan="1">12C</td><td colspan="2" rowspan="1">4</td><td colspan="1" rowspan="1"></td><td colspan="1" rowspan="1">5</td><td colspan="1" rowspan="1"></td></tr><tr><td colspan="1" rowspan="1">USART</td><td colspan="2" rowspan="1">4</td><td colspan="2" rowspan="1">5</td><td colspan="1" rowspan="1"></td></tr><tr><td colspan="1" rowspan="1">UART</td><td colspan="2" rowspan="1">4</td><td colspan="2" rowspan="1">5</td><td colspan="1" rowspan="1"></td></tr><tr><td colspan="1" rowspan="1">LPUART</td><td colspan="1" rowspan="1">NA</td><td colspan="1" rowspan="1"></td><td colspan="2" rowspan="1">1</td><td colspan="1" rowspan="1"></td></tr><tr><td colspan="1" rowspan="1">SAI</td><td colspan="1" rowspan="1">2</td><td colspan="1" rowspan="1">4</td><td colspan="2" rowspan="1">2</td><td colspan="1" rowspan="1"></td></tr><tr><td colspan="1" rowspan="1">SPDIFRX</td><td colspan="4" rowspan="1">4 inputs</td><td colspan="1" rowspan="1"></td></tr><tr><td colspan="1" rowspan="1">SWPMI</td><td colspan="1" rowspan="1">NA</td><td colspan="3" rowspan="1">1</td><td colspan="1" rowspan="1"></td></tr><tr><td colspan="1" rowspan="1">MDIO</td><td colspan="4" rowspan="1">1</td><td colspan="1" rowspan="1"></td></tr><tr><td colspan="1" rowspan="1">SDMMC</td><td colspan="4" rowspan="1">2</td><td colspan="1" rowspan="1"></td></tr><tr><td colspan="1" rowspan="1">CAN</td><td colspan="1" rowspan="1">x3 CANs(.0B active)</td><td colspan="2" rowspan="1">x2 CAN FD(FDCAN1 supports TTCAN)</td><td colspan="1" rowspan="1">x3 CAN FD(FDCAN1 supportsCACAN</td><td colspan="1" rowspan="1"></td></tr><tr><td colspan="1" rowspan="1">USB OTGF S</td><td colspan="2" rowspan="1">1</td><td colspan="2" rowspan="1">NA</td><td colspan="1" rowspan="1"></td></tr><tr><td colspan="1" rowspan="1">USB OTGUSHS </td><td colspan="4" rowspan="1">1</td><td colspan="1" rowspan="1">Support FS and HSwith ULPI</td></tr><tr><td colspan="1" rowspan="1">HDMI-CEC</td><td colspan="4" rowspan="1">1</td><td colspan="1" rowspan="1"></td></tr><tr><td colspan="1" rowspan="2">DFSDM umber offiter</td><td colspan="2" rowspan="1">1</td><td colspan="1" rowspan="1">2</td><td colspan="1" rowspan="1">1</td><td colspan="1" rowspan="1"></td></tr><tr><td colspan="2" rowspan="1">4</td><td colspan="1" rowspan="1">8/1</td><td colspan="1" rowspan="1">4</td><td colspan="1" rowspan="1"></td></tr><tr><td colspan="1" rowspan="2">Digital cameraintterface</td><td colspan="1" rowspan="1">DCMI</td><td colspan="2" rowspan="1"></td><td colspan="2" rowspan="1">1</td><td colspan="1" rowspan="1"></td></tr><tr><td colspan="1" rowspan="1">PSSI</td><td colspan="2" rowspan="1">NA</td><td colspan="2" rowspan="1">1</td><td colspan="1" rowspan="1"></td></tr><tr><td colspan="2" rowspan="1">MIPI-DSI host</td><td colspan="2" rowspan="1">1</td><td colspan="2" rowspan="1">NA</td><td colspan="1" rowspan="1">Available only onspecific packages</td></tr><tr><td colspan="1" rowspan="3">Graphics</td><td colspan="1" rowspan="1">LCD-TFT</td><td colspan="4" rowspan="1">1</td><td colspan="1" rowspan="1"></td></tr><tr><td colspan="1" rowspan="1">Chrom-CARTceleratorTM(DMA2D)</td><td colspan="4" rowspan="1">1</td><td colspan="1" rowspan="1">YCbCr to RGB colorspace conversion onSTM32H7 Series</td></tr><tr><td colspan="1" rowspan="1">JOEG</td><td colspan="3" rowspan="1">1</td><td colspan="1" rowspan="1">NA</td><td colspan="1" rowspan="1"></td></tr></table>

<table><tr><td rowspan=1 colspan=2>Peripheral</td><td rowspan=1 colspan=1>STM32F7Series</td><td rowspan=1 colspan=1>STM32H74x/75x</td><td rowspan=1 colspan=4>STM32H7A3/7Bx</td><td rowspan=1 colspan=2>STM32H72x/73x</td><td rowspan=1 colspan=1>Compatibility/comments</td></tr><tr><td rowspan=1 colspan=1>Graphics</td><td rowspan=1 colspan=1>GFXMMU</td><td rowspan=1 colspan=2>NA</td><td rowspan=1 colspan=4>1</td><td rowspan=1 colspan=2>NA</td><td rowspan=1 colspan=1>Graphical orientedmemory managementunit</td></tr><tr><td rowspan=1 colspan=2>GPIOs</td><td rowspan=1 colspan=1>Up to 159</td><td rowspan=1 colspan=5>Up to 168</td><td rowspan=1 colspan=2>Up to 128</td><td rowspan=1 colspan=1></td></tr><tr><td rowspan=5 colspan=1>Analogperipherals</td><td rowspan=1 colspan=1>ADC 12b</td><td rowspan=1 colspan=1>3</td><td rowspan=1 colspan=5>NA</td><td rowspan=1 colspan=2>1</td><td rowspan=2 colspan=1>Available down to1.62 V for STM32H7Series</td></tr><tr><td rowspan=1 colspan=1>ADC 16b</td><td rowspan=1 colspan=1>NA</td><td rowspan=1 colspan=1>3</td><td rowspan=1 colspan=6>2</td></tr><tr><td rowspan=1 colspan=1>12-bit DAC</td><td rowspan=1 colspan=2>2 channels</td><td rowspan=1 colspan=4>3 channels</td><td rowspan=1 colspan=2>2 channels</td><td rowspan=1 colspan=1></td></tr><tr><td rowspan=1 colspan=1>Operationalamplifiers</td><td rowspan=1 colspan=1>NA</td><td rowspan=1 colspan=7>2</td><td rowspan=1 colspan=1></td></tr><tr><td rowspan=1 colspan=1>Ultra-low-powercomparator</td><td rowspan=1 colspan=1>NA</td><td rowspan=1 colspan=7>2</td><td rowspan=1 colspan=1>-</td></tr><tr><td rowspan=8 colspan=2>DMA</td><td rowspan=8 colspan=1>General-purpose DMA:16-streamDMAcontroller withFIFOs andburst support</td><td rowspan=1 colspan=1>4 DMA controllersto unload the CPUx1 high-speedeneral-purosemaster directmmemoryaccesscontroller(MDMA)</td><td rowspan=2 colspan=4>5 DMA controllersto unload the CPUx1 high-peedgeneral-purposemaster directmemoryaccesscontroller(MMDMA)x2 dual-portDMAs withIFO andrequestroutercapabilities</td><td rowspan=7 colspan=2>4 DMA controllersto unload the CPU•   x1 high-speedgeneral-purposemaster directmemoryaccesscontrollerMDMA)x2 dual-portDMAs withFIFO andrequestroutercapabilitiesffor optimalperipheralmanagement</td><td rowspan=8 colspan=1>On STM32H7 Series:No limitation forperipheralrequests thanksto DMAMUXDMA1 andDMA2 canaccess toperipherals inAPB1/APB2busesPeripheralrquestmapping is nolonger managed the DMAcontroller but bythe DMAMUXcontroller</td></tr><tr><td rowspan=6 colspan=1>•   x2 dual-portDMAs withFIFO andrequestroutercapabilitiiesf for optimalperipheralmanagement</td></tr><tr><td rowspan=1 colspan=1></td></tr><tr><td rowspan=1 colspan=1></td></tr><tr><td rowspan=1 colspan=3></td></tr><tr><td rowspan=1 colspan=3>•</td></tr><tr><td rowspan=1 colspan=3></td><td rowspan=1 colspan=1>•</td></tr><tr><td rowspan=1 colspan=1>x1 basicDA withrequestroutercapabilities</td><td rowspan=1 colspan=4>requestroutercapabilities•   x1 basicDMAdedicated tothe DFSDM</td><td rowspan=1 colspan=2>•   x1 basicMA withrequestroutercapabillities</td></tr><tr><td rowspan=1 colspan=2>Cryptographic acceleration</td><td rowspan=1 colspan=8>AES 128, 192, 256, DES/TDESHASH (MD5, SHA-1, SHA-2)HMACTrue random number generator</td><td rowspan=1 colspan=1></td></tr><tr><td rowspan=2 colspan=1>Security</td><td rowspan=1 colspan=1>ROP</td><td rowspan=1 colspan=1>ROP</td><td rowspan=1 colspan=7>ROP, PC-ROP one secure-only areas per flash bank</td><td rowspan=1 colspan=1></td></tr><tr><td rowspan=1 colspan=1>Tamper</td><td rowspan=1 colspan=1>Tamper</td><td rowspan=1 colspan=1>Tamper</td><td rowspan=1 colspan=4>Active tamper</td><td rowspan=1 colspan=2>Tamper</td><td rowspan=1 colspan=1></td></tr></table>

# 6.2

# Memory organization

# 6.2.1

# RAM size

The following table illustrates the difference of RAM size between STM32F7 Series, STM32H74x/75x, STM32H72x/73x and STM32H7A3/7Bx devices.

Table 10. Comparison of RAM size between STM32F7 Series, STM32H74x/75x, STM32H72x/73x and STM32H7A3/7Bx devices   

<table><tr><td rowspan=1 colspan=1>Memory</td><td rowspan=1 colspan=1>STM32F7 Series</td><td rowspan=1 colspan=1>STM32H74x/75x</td><td rowspan=1 colspan=1>STM32H7A3/7Bx</td><td rowspan=1 colspan=1>STM32H72x/73x</td><td rowspan=10 colspan=1>UnitsKbyte</td></tr><tr><td rowspan=1 colspan=1>ITCM-RAM</td><td rowspan=1 colspan=1>16</td><td rowspan=1 colspan=2>64</td><td rowspan=1 colspan=1>64(1)</td></tr><tr><td rowspan=1 colspan=1>DTCM-RAM</td><td rowspan=1 colspan=1>128(2)</td><td rowspan=1 colspan=3>128</td></tr><tr><td rowspan=1 colspan=1>AXI-SRAM</td><td rowspan=1 colspan=1>-</td><td rowspan=1 colspan=1>512</td><td rowspan=1 colspan=1>1024(split in 3 SRAMs)</td><td rowspan=1 colspan=1>128(1)</td></tr><tr><td rowspan=1 colspan=1>SRAM1</td><td rowspan=1 colspan=1>368</td><td rowspan=1 colspan=1>128</td><td rowspan=1 colspan=1>64</td><td rowspan=1 colspan=1>16</td></tr><tr><td rowspan=1 colspan=1>SRAM2</td><td rowspan=1 colspan=1>16</td><td rowspan=1 colspan=1>128</td><td rowspan=1 colspan=1>64</td><td rowspan=1 colspan=1>16</td></tr><tr><td rowspan=1 colspan=1>SRAM3</td><td rowspan=1 colspan=1>NA</td><td rowspan=1 colspan=1>32</td><td rowspan=1 colspan=1>NA</td><td rowspan=1 colspan=1>NA</td></tr><tr><td rowspan=1 colspan=1>SRAM4</td><td rowspan=1 colspan=1>NA</td><td rowspan=1 colspan=1>64</td><td rowspan=1 colspan=1>32</td><td rowspan=1 colspan=1>16</td></tr><tr><td rowspan=1 colspan=1>Backup SRAM</td><td rowspan=1 colspan=4>4</td></tr><tr><td rowspan=1 colspan=1>Total</td><td rowspan=1 colspan=1>532</td><td rowspan=1 colspan=1>1060</td><td rowspan=1 colspan=1>1380</td><td rowspan=1 colspan=1>564</td></tr></table>

Can be increased with ITCM / AXI hared memory. 264k bytes for STM32F74xxx/75xxx devices.

# 6.2.2

# Memory map and peripherals register boundary addresses

The table and figure below ilustrate the memory addresses between STM32F7 Series, STM32H74x/75x, STM32H72x/73x and STM32H7A3/7Bx devices.

Table 11. Memory organization and compatibility between STM32F7 Series, STM32H74x/75x, STM32H72x/73x and STM32H7A3/7Bx devices   

<table><tr><td rowspan=1 colspan=2>Memory</td><td rowspan=1 colspan=1>STM32F7</td><td rowspan=1 colspan=1>STM32H74/75</td><td rowspan=1 colspan=1>STM32H7A/7B</td><td rowspan=1 colspan=1>STM32H72/73</td><td rowspan=1 colspan=1>Comments</td></tr><tr><td rowspan=1 colspan=2>ITCM-RAM</td><td rowspan=1 colspan=1>0x0000 0000 -0x0000 3FFF</td><td rowspan=1 colspan=2>0x0000 0000 - 0x0000 FFFF</td><td rowspan=1 colspan=1>0x0000 0000 -0x0000 FFFF0x0000 0000 -0x0001 FFFF0x0000 0000 -0x0002 FFFF0x0000 0000 -0x0003 FFFF</td><td rowspan=1 colspan=1>STM32H72/73 sizedepends on sharedmemory assignment</td></tr><tr><td rowspan=1 colspan=2>DTCM-RAM</td><td rowspan=1 colspan=1></td><td rowspan=1 colspan=3>0x2000 0000 - 0x2001 FFFF</td><td rowspan=1 colspan=1>Some STM32F7devices feature only64 Kbytes</td></tr><tr><td rowspan=7 colspan=1>FLASH</td><td rowspan=3 colspan=1>Bank1</td><td rowspan=6 colspan=1>Flash bank 10x0800 0000 -0x080F FFFFFlash bank 20x0810 0000 -0x081F FFFF</td><td rowspan=1 colspan=3>0x0800 0000 - 0x080F FFFF</td><td rowspan=1 colspan=1>STM2H74/75xxlSTM32H7B3/H7A3xlSTM32H72/73xxG</td></tr><tr><td rowspan=1 colspan=3>0x0800 0000 - 0x0807 FFFF</td><td rowspan=1 colspan=1>STM2H74/75xxGSTM32H7B3/H7A3xGSTM32H72/73xxE</td></tr><tr><td rowspan=1 colspan=3>0x0800 0000 - 0x0801 FFFF</td><td rowspan=1 colspan=1>Value line</td></tr><tr><td rowspan=3 colspan=1>Bank2</td><td rowspan=1 colspan=2>0x0810 0000 - 0x081F FFFF</td><td rowspan=1 colspan=1>NA</td><td rowspan=1 colspan=1>STM2H74/75xxlSTM32H7B3/H7A3xl</td></tr><tr><td rowspan=1 colspan=2>0x0810 0000 - 0x0817 FFFF</td><td rowspan=1 colspan=1>NA</td><td rowspan=1 colspan=1>STM2H74/75xxGSTM32H7B3/H73xG</td></tr><tr><td rowspan=1 colspan=3>NA</td><td rowspan=1 colspan=1>Value line</td></tr><tr><td rowspan=1 colspan=1>Flash -ITCM</td><td rowspan=1 colspan=1>0x0020 0000 0x003FF FFFF</td><td rowspan=1 colspan=3>NA</td><td rowspan=1 colspan=1>NA</td></tr><tr><td rowspan=2 colspan=1>Systemmemory</td><td rowspan=1 colspan=1>Bank1</td><td rowspan=1 colspan=1>0x1FF0 0000 -0x1FF0 EDBF</td><td rowspan=1 colspan=1>0x1FF0 0000 -0x1FF1 FFFF</td><td rowspan=1 colspan=1>0x1FF0 0000 -0x1FF0 FFFF</td><td rowspan=1 colspan=1>0x1FF0 0000 -0x1FF0 FFFF</td><td rowspan=1 colspan=1>NA</td></tr><tr><td rowspan=1 colspan=1>Bank2</td><td rowspan=1 colspan=1>NA</td><td rowspan=1 colspan=1>0x1FF4 0000 -0x1FF5 FFFF</td><td rowspan=1 colspan=1>0x1FF1 0000 -0x1FF1 FFFF</td><td rowspan=1 colspan=2>NA</td></tr></table>

![](images/d52a547948cade6bfb11e5cc84760c9b718fb42f8b684b62be3ece1ab47737cc.jpg)  
Figure 8. RAM memory organization of STM32F7 Series, STM32H743/753 and STM32H7A3/7Bx devices

# Note:

# DTCM-RAM size:

128 Kbytes STM32F76xxx, STM32F77xxx and STM32H743/753 and STM32H7A3/7B0/7B3 devices   
64 Kbytes for the STM32F75xxx and STM32F74xxx devices

# 6.2.3

# Peripheral register boundary addresses

The peripheral address mapping has been changed for most of peripherals in the STM32H74x/75x, STM32H72x/73x and STM32H7A3/7Bx devices versus the STM32F7 Series devices.

Formore details about registers boundary addresses differences refer to Memory map and register boundary addresses section of RM0368, RM0385, RM0410, RM0433 and RM0455 reference manuals.

Section 6.2.2 Memory map and peripherals register boundary addresses shows the detail of all the peripherals address mapping differences between STM32F7 Series, STM32H74x/75x, STM32H72x/73x and STM32H7A3/7Bx devices.

Table 12. Examples of peripheral address mapping differences between STM32F7 Series,STM32H74x/75x, STM32H72x/73x and STM32H7A3/7Bx devices   

<table><tr><td rowspan=2 colspan=2>Peripheral</td><td rowspan=1 colspan=3>STM32F7Seriesdevices</td><td rowspan=1 colspan=1>STM32H74/75devices</td><td rowspan=1 colspan=1>STM32H72/73devices</td><td rowspan=1 colspan=1>STM32H7A/7Bdevices</td><td rowspan=1 colspan=1>STM32F7Seriesevices</td><td rowspan=1 colspan=2>STM32H74/75devices</td><td rowspan=1 colspan=1>STM32H72/73devices</td><td rowspan=1 colspan=1>STM32H7A/7B devices</td></tr><tr><td rowspan=1 colspan=3></td><td rowspan=1 colspan=3>Bus</td><td rowspan=1 colspan=5>Base address</td></tr><tr><td rowspan=1 colspan=2>QUADSPIcontrol</td><td rowspan=1 colspan=4>AHB3</td><td rowspan=1 colspan=2>NA</td><td rowspan=1 colspan=1>OxA000 1000- 0xA000 1F</td><td rowspan=1 colspan=2>0x5200 5000 -0x5200 5FFF</td><td rowspan=1 colspan=2>NA</td></tr><tr><td rowspan=1 colspan=2>GPIOA</td><td rowspan=2 colspan=3>AHB1</td><td rowspan=2 colspan=3>AHB4 (D3 or SRD)</td><td rowspan=1 colspan=1>Ox4002 0000 -0x4002 03FF</td><td rowspan=1 colspan=4>0x5802 0000 - 0x5802 03FF</td></tr><tr><td rowspan=1 colspan=2>RCC</td><td rowspan=1 colspan=1>Ox40023800 -0x40023BF</td><td rowspan=1 colspan=4>0x58024400 - 0x580247FF</td></tr><tr><td rowspan=1 colspan=2>DFSDM2</td><td rowspan=1 colspan=5>NA</td><td rowspan=1 colspan=1>AHB4(RD)</td><td rowspan=1 colspan=4>NA</td><td rowspan=1 colspan=1>0x5800 6C000x580073F</td></tr><tr><td rowspan=1 colspan=2>DTS</td><td rowspan=1 colspan=4>NA</td><td rowspan=1 colspan=2>AHB4 (D3 or SRD)</td><td rowspan=1 colspan=3>NA</td><td rowspan=1 colspan=2>0x5800 6800 - 0x5800 6BFF</td></tr><tr><td rowspan=1 colspan=2>RTC2 andBackup reg</td><td rowspan=1 colspan=3>AHB1</td><td rowspan=1 colspan=2>AHB4 (D3)</td><td rowspan=1 colspan=1>NA</td><td rowspan=1 colspan=1>0x4000 2800 -0x400002BF</td><td rowspan=1 colspan=3>0x5800 4000 - 0x5800 43FF</td><td rowspan=1 colspan=1>NA</td></tr><tr><td rowspan=1 colspan=2>Tamp andBackup reg</td><td rowspan=1 colspan=5>NA</td><td rowspan=3 colspan=1>AHB4(SRD)</td><td rowspan=1 colspan=4>NA</td><td rowspan=1 colspan=1>0x5800 4400 -0x5800 47FF</td></tr><tr><td rowspan=1 colspan=2>RTC3</td><td rowspan=2 colspan=4></td><td rowspan=2 colspan=1>NA</td><td rowspan=3 colspan=3></td><td rowspan=3 colspan=1>NA</td><td rowspan=1 colspan=1>0x5800 4000 -0x5800 43FF</td></tr><tr><td rowspan=1 colspan=2>DAC2</td><td rowspan=1 colspan=1>0x5800 3400 -0x5800 37FF</td></tr><tr><td rowspan=1 colspan=2>GFXMMU</td><td rowspan=1 colspan=4></td><td rowspan=1 colspan=1></td><td rowspan=1 colspan=1>AHB3</td><td rowspan=1 colspan=1>0x5200 C0000x5200 EFF</td></tr><tr><td rowspan=3 colspan=2>OTFDEC2</td><td rowspan=3 colspan=1></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td></tr><tr><td rowspan=2 colspan=2></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td></tr><tr><td rowspan=1 colspan=3></td><td rowspan=1 colspan=2></td><td rowspan=7 colspan=3>NA</td><td rowspan=1 colspan=1></td><td rowspan=1 colspan=2>0x5200 BC00 - 0x5200 BFFF</td></tr><tr><td rowspan=1 colspan=2>OTFDEC1</td><td></td><td></td><td rowspan=2 colspan=3>NA</td><td rowspan=2 colspan=2></td><td rowspan=1 colspan=2>0x5200 B800 - 0x5200 BBFF</td></tr><tr><td rowspan=1 colspan=2>OTCOSPI I/Omanager</td><td></td><td></td><td rowspan=1 colspan=2>0x5200B400 - 0x5200B7FF</td></tr><tr><td rowspan=1 colspan=2>Delay blockOCTOSPI2</td><td rowspan=4 colspan=4></td><td rowspan=1 colspan=2>AHB3</td><td rowspan=1 colspan=2>0x5200 B000 - Ox5200 B3FF</td></tr><tr><td rowspan=1 colspan=2>OCTOSPI2</td><td rowspan=3 colspan=2></td><td rowspan=1 colspan=2>0x5200 A000 - 0x5200 AFFF</td></tr><tr><td rowspan=1 colspan=2>Delay blockOCTOSPI1</td><td rowspan=1 colspan=2>0x5200 6000 - 0x5200 63FF</td></tr><tr><td rowspan=1 colspan=2>OCTOSPI1</td><td rowspan=1 colspan=2>0x5200 5000 - 0x5200 5FFF</td></tr><tr><td rowspan=1 colspan=2>QUADSPI</td><td rowspan=1 colspan=4>AHB3</td><td rowspan=1 colspan=2>NA</td><td rowspan=1 colspan=1>OxA000 1000-0xA000 1F</td><td rowspan=1 colspan=2>0x5200 5000 -0x52005FFF</td><td rowspan=1 colspan=2>NA</td></tr></table>

<table><tr><td rowspan=2 colspan=1>Peripheral</td><td rowspan=1 colspan=1>STM32F7 Seriesdevices</td><td rowspan=1 colspan=1>STM32H74/75devices</td><td rowspan=1 colspan=1>STM32H72/73devices</td><td rowspan=1 colspan=1>STM32H7A/7Bdevices</td><td rowspan=1 colspan=1>STM32F7Seriesdevices</td><td rowspan=1 colspan=1>STM32H74/75devices</td><td rowspan=1 colspan=1>STM32H72/73devices</td><td rowspan=1 colspan=1>STM32H7A/7B devices</td></tr><tr><td rowspan=1 colspan=1></td><td rowspan=1 colspan=3>Bus</td><td rowspan=1 colspan=4>Base address</td></tr><tr><td rowspan=1 colspan=1>BDMA1</td><td rowspan=1 colspan=3>NA</td><td rowspan=1 colspan=1>AHB2</td><td rowspan=1 colspan=3>NA</td><td rowspan=1 colspan=1>0x48022C000x48022FFF</td></tr><tr><td rowspan=1 colspan=1>HSEM</td><td rowspan=1 colspan=1>NA</td><td rowspan=1 colspan=3>AHB4</td><td rowspan=1 colspan=1>NA</td><td rowspan=1 colspan=2>0x58026400 - 0x580267FF</td><td rowspan=1 colspan=1>0x48020800 -0x4802 0BFF</td></tr><tr><td rowspan=1 colspan=1>PSSI</td><td rowspan=1 colspan=2>NA</td><td rowspan=1 colspan=2>AHB2</td><td rowspan=1 colspan=2>NA</td><td rowspan=1 colspan=2>0x48020400 - 0x4802 07FF</td></tr><tr><td rowspan=1 colspan=1>CRC</td><td rowspan=1 colspan=1>AHB1</td><td rowspan=1 colspan=2>AHB4 (D3)</td><td rowspan=1 colspan=1>AHB1</td><td rowspan=1 colspan=1>0x4002 3000 -0x4002 33FF</td><td rowspan=1 colspan=2>0x5802 4C00 - 0x5802 4FFF</td><td rowspan=1 colspan=1>0x4002 30000x4002 33FF</td></tr><tr><td rowspan=1 colspan=1>DFSDM1</td><td rowspan=1 colspan=4>APB2</td><td rowspan=1 colspan=1>0x4001 7400 -0x4001 77F</td><td rowspan=1 colspan=2>0x4001 7000 - 0x4001 73FF</td><td rowspan=1 colspan=1>0x4001 7800 -0x4001 7F</td></tr><tr><td rowspan=1 colspan=1>USART10</td><td rowspan=2 colspan=2>NA</td><td rowspan=2 colspan=2>APB2</td><td rowspan=2 colspan=2>NA</td><td rowspan=1 colspan=2>0x4001 1C00 - 0x4001 1FFF</td></tr><tr><td rowspan=1 colspan=1>UART9</td><td rowspan=1 colspan=2>0x4001 1800 - 0x4001 1BFF</td></tr></table>

# 6.3 Flash memory

Table 13 presents the differences of the flash memory interface between STM32F7 Series, STM32H74x/75x, STM32H72x/73x and STM32H7A3/7Bx and devices.

The STM32H7 Series devices instantiate a different flash memory module both in terms of architecture and interace. For more information on programming, erasing and protectionf STM327 Series devices refer  the corresponding product's reference manual.

Table 13. Flash memory differences between STM32F7 Series, STM32H74x/75x, STM32H72x/73x and STM32H7A3/7Bx devices   

<table><tr><td colspan="1" rowspan="1">Flash</td><td colspan="1" rowspan="1">STM32F7 Series</td><td colspan="1" rowspan="1">STM32H74x/75x</td><td colspan="1" rowspan="1">STM32H72x/73x</td><td colspan="1" rowspan="1">STM32H7A3/7Bx</td></tr><tr><td colspan="1" rowspan="1">Mapping</td><td colspan="1" rowspan="1">AHB</td><td colspan="1" rowspan="1"></td><td colspan="1" rowspan="1">AXI</td><td colspan="1" rowspan="1"></td></tr><tr><td colspan="1" rowspan="2">Flash address</td><td colspan="1" rowspan="1">•    STM32F76xxx/STM32F77xxxFlash - AXI0x0800 0000 -0x081FFFSTM32F746xx/STM32F756xxFlash - AXI0x0800 0000 - 0x080FFF</td><td colspan="1" rowspan="1">Flash bank 10x0800 0000 -0x080F FFFFFlash bank 20x0810 0000 -0x081F FFF</td><td colspan="1" rowspan="1">Flash bank10x08000000 0x080FFF</td><td colspan="1" rowspan="1">•    Flash bank 10x0800 0000 -0x080F FFFF•    Flash bank 20x0810 0000 -0x081F FFF</td></tr><tr><td colspan="1" rowspan="1">STM32F76xxx/STM32F77xxxFlash  ITCM0x0020 0000 - 0x003FFFFFSTM32F746xx/STM32F756xxFlash - ITCM0x0020 0000 - 0x002FFF</td><td colspan="3" rowspan="1">NA</td></tr><tr><td colspan="1" rowspan="1">Main / programmemory</td><td colspan="1" rowspan="1">•    STM32F76xxx/STM32F77xxxUp to 2 Mbytes(single/dual bank)Single bank: up to256-Kbyte sector sizeDual bank: up to 128-Kbyte sector size</td><td colspan="1" rowspan="1">Up to 2 Mbytes (dualbank)128-Kbyte size sector</td><td colspan="1" rowspan="1">Up to 1 Mbyte(single bank)128-Kbyte sizesector</td><td colspan="1" rowspan="1">Up to 2 Mbytes (dualbank)8-Kbyte size sector</td></tr><tr><td colspan="1" rowspan="2">Main / programmemory</td><td colspan="1" rowspan="1">•    STM32F746xx/STM327F56xxUp to 1 Mbyte (singlebbank)Up to 256-Kbytesector size</td><td colspan="1" rowspan="1"></td><td colspan="1" rowspan="1"></td><td colspan="1" rowspan="1"></td></tr><tr><td colspan="1" rowspan="1">Programming granularity: 64 bitsFlash line width: 256 bits or 128bits</td><td colspan="2" rowspan="1">Programming granularity: 256 bitsFlash line width: 256 bits</td><td colspan="1" rowspan="1">Programminggranularity: 128 bitsFlash line width: 128bbits</td></tr><tr><td colspan="1" rowspan="1">Wait state</td><td colspan="1" rowspan="1">Up to 9 (depending on the supplyvoltage and frequency)</td><td colspan="2" rowspan="1">Up to 4 (depending on the core voltage andfrequency)</td><td colspan="1" rowspan="1">Up to 6 (depending onthe core voltage andfrequency)</td></tr><tr><td colspan="1" rowspan="1">Option bytes</td><td colspan="1" rowspan="1">32 bytes</td><td colspan="2" rowspan="1">2 Kbytes</td><td colspan="1" rowspan="1"></td></tr><tr><td colspan="1" rowspan="1">OTP</td><td colspan="1" rowspan="1">1024 bytes</td><td colspan="2" rowspan="1">NA</td><td colspan="1" rowspan="1">1024 bytes</td></tr><tr><td colspan="1" rowspan="1">Features</td><td colspan="1" rowspan="1">STM32F76xxx/STM32F77xxx•    Read while write (RWW)Supports dual boot modeSector, mass erase andbank mass erase (only inDual-bank mode)</td><td colspan="3" rowspan="1">•    Error code correction (ECC)Double-word, word, half-word and byte read / write operationsSector erase, bank erase and mass eraseDual-bank organization supporting simultaneous operations:two read/program/erase operations can be executed in parallelon the two banksBank swapping: the address mapping of the user flash memoryof each bank can be swapped.</td></tr><tr><td colspan="1" rowspan="3">Protectionmechanisms</td><td colspan="1" rowspan="1"></td><td colspan="3" rowspan="1">Readout protection (RDP)</td></tr><tr><td colspan="1" rowspan="2">NA</td><td colspan="3" rowspan="1">1 PCROP protection area per bank (execute-only memory)1 secure area in user flash memory per bank</td></tr><tr><td colspan="2" rowspan="1">Sector write protection128-Kbyte sectors</td><td colspan="1" rowspan="1">Sector write protection32-Kbyte sectors</td></tr></table>

# 6.4

# Nested vectored interrupt controllers (NVIC)

The table below presents the interrupt vector differences between STM32F7 Series, STM32H74x/75x, STM32H72x/73x and STM32H7A3/7Bx devices.

Table 14. Interrupt vector differences between STM32F7 Series, STM32H74x/75x, STM32H72x/73x and STM32H7A3/7Bx devices   

<table><tr><td rowspan=1 colspan=1>Position</td><td rowspan=1 colspan=1>STM32F7 Series</td><td rowspan=1 colspan=1>STM32H74x/75x</td><td rowspan=1 colspan=1>STM32H72x/73x</td><td rowspan=1 colspan=1>STM32H7A3/7Bx</td></tr><tr><td rowspan=1 colspan=1>2</td><td rowspan=1 colspan=1>NA</td><td rowspan=1 colspan=3>RTC_TAMP_STAMP_CSS_LSE</td></tr><tr><td rowspan=1 colspan=1>18</td><td rowspan=1 colspan=1>ADC</td><td rowspan=1 colspan=3>ADC1_2</td></tr><tr><td rowspan=1 colspan=1>19</td><td rowspan=1 colspan=1>CAN1_TX</td><td rowspan=1 colspan=3>FDCAN1_ITO</td></tr><tr><td rowspan=1 colspan=1>20</td><td rowspan=1 colspan=1>CAN1_RXO</td><td rowspan=1 colspan=3>FDCAN2_ITO</td></tr><tr><td rowspan=1 colspan=1>21</td><td rowspan=1 colspan=1>CAN1_RX1</td><td rowspan=1 colspan=3>FDCAN1_IT1</td></tr><tr><td rowspan=1 colspan=1>22</td><td rowspan=1 colspan=1>CAN1_SCE</td><td rowspan=1 colspan=3>FDCAN2_IT1</td></tr><tr><td rowspan=1 colspan=1>24</td><td rowspan=1 colspan=1>TIM1_BRK_TIM9</td><td rowspan=1 colspan=3>TIM1_BRK</td></tr><tr><td rowspan=1 colspan=1>25</td><td rowspan=1 colspan=1>TIM1_UP_TIM10</td><td rowspan=1 colspan=3>TIM1_UP</td></tr><tr><td rowspan=1 colspan=1>26</td><td rowspan=1 colspan=1>TIM1_TRG_COM_TIM11</td><td rowspan=1 colspan=3>TIM1_TRG_COM</td></tr><tr><td rowspan=1 colspan=1>42</td><td rowspan=1 colspan=1>OTG_FS WKUP</td><td rowspan=1 colspan=1>OTG_FS WKUP</td><td rowspan=1 colspan=1>Reserved</td><td rowspan=1 colspan=1>DFSDM2</td></tr><tr><td rowspan=1 colspan=1>61</td><td rowspan=1 colspan=1>ETH</td><td rowspan=1 colspan=2>ETH</td><td rowspan=1 colspan=1>Reserved</td></tr><tr><td rowspan=1 colspan=1>62</td><td rowspan=1 colspan=1>ETH_WKUP</td><td rowspan=1 colspan=1>ETH_WKUP</td><td rowspan=1 colspan=1>ETH_WKUP</td><td rowspan=1 colspan=1>Reserved</td></tr></table>

<table><tr><td rowspan=1 colspan=1>Position</td><td rowspan=1 colspan=8>STM32F7 Series</td><td rowspan=1 colspan=1>STM32H74x/75x</td></tr><tr><td rowspan=1 colspan=1>63</td><td rowspan=1 colspan=8>CAN2_TX</td><td rowspan=1 colspan=1>FDCAN_CAL</td></tr><tr><td rowspan=1 colspan=1>64</td><td rowspan=1 colspan=8>CAN2_TX</td><td rowspan=1 colspan=1>Reserved</td></tr><tr><td rowspan=1 colspan=1>65</td><td rowspan=1 colspan=8>CAN2_RX1</td><td rowspan=1 colspan=1>Reserved</td></tr><tr><td rowspan=1 colspan=1>66</td><td rowspan=1 colspan=8>CAN2_SCE</td><td rowspan=1 colspan=1>Reserved</td></tr><tr><td rowspan=1 colspan=1>67</td><td rowspan=1 colspan=8>OTG_FS</td><td rowspan=1 colspan=1>Reserved</td></tr><tr><td rowspan=1 colspan=1>81</td><td rowspan=1 colspan=8>-</td><td rowspan=1 colspan=1>FPU</td></tr><tr><td rowspan=1 colspan=1>92</td><td rowspan=1 colspan=8>QUADSPI</td><td rowspan=1 colspan=1>QUADSPI</td></tr><tr><td rowspan=1 colspan=1>97</td><td rowspan=1 colspan=8>Reserved</td><td rowspan=1 colspan=1>SPDIFRX</td></tr><tr><td rowspan=1 colspan=1>98</td><td rowspan=1 colspan=8>DSIHOST</td><td rowspan=1 colspan=1>OTG_FS_EP1_OUT</td></tr><tr><td rowspan=1 colspan=1>99</td><td rowspan=1 colspan=8>DFSDM1_FLT1</td><td rowspan=1 colspan=1>OTG_FS_EP1_IN</td></tr><tr><td rowspan=1 colspan=1>100</td><td rowspan=1 colspan=8>DFSDM1_FLT2</td><td rowspan=1 colspan=1>OTG_FS_WKUP</td></tr><tr><td rowspan=1 colspan=1>101</td><td rowspan=1 colspan=8>DFSDM1_FLT3</td><td rowspan=1 colspan=1>OTG_FS</td></tr><tr><td rowspan=1 colspan=1>102</td><td rowspan=1 colspan=8>DFSDM1_FLT4</td><td rowspan=1 colspan=1></td></tr><tr><td rowspan=1 colspan=1>103</td><td rowspan=1 colspan=8>SDMMC2</td><td rowspan=1 colspan=1>HRTIM1_MST</td></tr><tr><td rowspan=1 colspan=1>104</td><td rowspan=1 colspan=8>CAN3_TX</td><td rowspan=1 colspan=1>HRTIM1_TIMA</td></tr><tr><td rowspan=1 colspan=1>105</td><td rowspan=1 colspan=8>CAN3_RXO</td><td rowspan=1 colspan=1>HRTIM_TIMB</td></tr><tr><td rowspan=1 colspan=1>106</td><td rowspan=1 colspan=8>CAN3_RX1</td><td rowspan=1 colspan=1>HRTIM1_TIMC</td></tr><tr><td rowspan=1 colspan=1>107</td><td rowspan=1 colspan=8>CAN3_SCE</td><td rowspan=1 colspan=1>HRTIM1_TIMD</td></tr><tr><td rowspan=1 colspan=1>108</td><td rowspan=1 colspan=8>JPEG</td><td rowspan=1 colspan=1>HRTIM_TIME</td></tr><tr><td rowspan=1 colspan=1>109</td><td rowspan=1 colspan=8>MDIOS</td><td rowspan=1 colspan=1>HRTIM1_FLT</td></tr><tr><td rowspan=1 colspan=1>110</td><td rowspan=1 colspan=8></td><td rowspan=1 colspan=1>DFSDM1_FLTO (filter 0)</td></tr><tr><td rowspan=1 colspan=1>111</td><td rowspan=2 colspan=8>NA</td><td rowspan=1 colspan=1>DFSDM1_FLT1 (filter 1)</td></tr><tr><td rowspan=1 colspan=1>112</td><td rowspan=1 colspan=1>DFSDM1_FLT2 (filter 2)</td></tr><tr><td rowspan=1 colspan=1>113</td><td rowspan=1 colspan=8></td><td rowspan=1 colspan=1>DFSDM1_FLT3 (filter 3)</td></tr><tr><td rowspan=1 colspan=1>114</td><td rowspan=1 colspan=8>NA</td><td rowspan=1 colspan=1>SAI3</td></tr><tr><td rowspan=1 colspan=1>115</td><td rowspan=1 colspan=8></td><td rowspan=1 colspan=1>SWPMI1</td></tr><tr><td rowspan=2 colspan=1>116</td><td rowspan=2 colspan=2></td><td rowspan=1 colspan=1></td><td rowspan=2 colspan=3></td><td rowspan=1 colspan=2></td><td rowspan=2 colspan=1></td></tr><tr><td rowspan=1 colspan=2></td><td></td><td></td></tr><tr><td rowspan=3 colspan=1>117</td><td rowspan=3 colspan=2></td><td rowspan=1 colspan=1></td><td rowspan=3 colspan=2></td><td></td><td></td><td></td><td></td></tr><tr><td></td><td rowspan=2 colspan=2></td><td></td><td></td><td></td></tr><tr><td></td><td rowspan=1 colspan=3></td><td rowspan=1 colspan=1>TIM16</td></tr><tr><td rowspan=1 colspan=1>118</td><td rowspan=1 colspan=3></td><td rowspan=2 colspan=5>NA</td><td rowspan=1 colspan=1>TIM17</td></tr><tr><td rowspan=1 colspan=1>119</td><td></td><td></td><td></td><td rowspan=1 colspan=1>MDIO_WKUP</td></tr><tr><td rowspan=1 colspan=1>120</td><td rowspan=2 colspan=8></td><td rowspan=1 colspan=1>MDIO</td></tr><tr><td rowspan=2 colspan=1>121</td><td rowspan=2 colspan=5></td><td rowspan=2 colspan=3></td><td rowspan=2 colspan=1>JPEG</td></tr><tr><td rowspan=1 colspan=3></td></tr><tr><td rowspan=1 colspan=1>122</td><td rowspan=1 colspan=8></td><td rowspan=1 colspan=1>MDMA</td></tr><tr><td rowspan=1 colspan=1>123</td><td rowspan=1 colspan=8>NA</td><td rowspan=1 colspan=1>DSI/DSI_WKUP</td></tr><tr><td rowspan=1 colspan=1>124</td><td rowspan=2 colspan=8>NA</td><td rowspan=1 colspan=1>SDMMC2</td></tr><tr><td rowspan=1 colspan=1>125</td><td rowspan=1 colspan=1>HSEMO</td></tr><tr><td rowspan=1 colspan=1>127</td><td rowspan=1 colspan=8>NA</td><td rowspan=1 colspan=1>ADC3</td></tr><tr><td rowspan=1 colspan=1>128</td><td rowspan=1 colspan=8></td><td rowspan=1 colspan=1>DMAMUX2_OVR</td></tr><tr><td rowspan=1 colspan=1>129</td><td rowspan=2 colspan=8>NA</td><td rowspan=1 colspan=1>BDMA_CH1</td></tr><tr><td rowspan=1 colspan=1>130</td><td rowspan=1 colspan=1>BDMA_CH2</td></tr><tr><td rowspan=1 colspan=1>131</td><td rowspan=1 colspan=8></td><td rowspan=1 colspan=1>BDMA_CH3</td></tr></table>

<table><tr><td rowspan=1 colspan=1>Position</td><td rowspan=1 colspan=1>STM32F7 Series</td><td rowspan=1 colspan=1>STM32H74x/75x</td><td rowspan=1 colspan=1>STM32H72x/73x</td><td rowspan=1 colspan=1>STM32H7A3/7Bx</td></tr><tr><td rowspan=1 colspan=1>132</td><td rowspan=1 colspan=1></td><td rowspan=1 colspan=3>BDMA_CH4</td></tr><tr><td rowspan=1 colspan=1>133</td><td rowspan=1 colspan=1></td><td rowspan=1 colspan=3>BDMA_CH5</td></tr><tr><td rowspan=1 colspan=1>134</td><td rowspan=1 colspan=1></td><td rowspan=1 colspan=3>BDMA_CH6</td></tr><tr><td rowspan=1 colspan=1>135</td><td rowspan=1 colspan=1>NA</td><td rowspan=1 colspan=3>BDMA_CH7</td></tr><tr><td rowspan=1 colspan=1>136</td><td rowspan=1 colspan=1></td><td rowspan=1 colspan=3>BDMA_CH8</td></tr><tr><td rowspan=1 colspan=1>137</td><td rowspan=1 colspan=1></td><td rowspan=1 colspan=3>COMP</td></tr><tr><td rowspan=1 colspan=1>138</td><td rowspan=1 colspan=1></td><td rowspan=1 colspan=3>LPTIM2</td></tr><tr><td rowspan=1 colspan=1>139</td><td rowspan=1 colspan=1></td><td rowspan=1 colspan=3>LPTIM3</td></tr><tr><td rowspan=1 colspan=1>140</td><td rowspan=2 colspan=1>NA</td><td rowspan=1 colspan=2>LPTIM4</td><td rowspan=1 colspan=1>UART9</td></tr><tr><td rowspan=1 colspan=1>141</td><td rowspan=1 colspan=2>LPTIM5</td><td rowspan=1 colspan=1>USART10</td></tr><tr><td rowspan=1 colspan=1>142</td><td rowspan=1 colspan=1>NA</td><td rowspan=1 colspan=3>LPUART1</td></tr><tr><td rowspan=1 colspan=1>143</td><td rowspan=1 colspan=1>NA</td><td rowspan=1 colspan=1>WWDG1_RST</td><td rowspan=1 colspan=2>Reserved</td></tr><tr><td rowspan=1 colspan=1>144</td><td rowspan=2 colspan=1>NA</td><td rowspan=1 colspan=3>CRS</td></tr><tr><td rowspan=1 colspan=1>145</td><td rowspan=1 colspan=3>ECC</td></tr><tr><td rowspan=1 colspan=1>146</td><td rowspan=1 colspan=1></td><td rowspan=1 colspan=2>SAI4</td><td rowspan=1 colspan=1>Reserved</td></tr><tr><td rowspan=1 colspan=1>147</td><td rowspan=1 colspan=1>NA</td><td rowspan=1 colspan=1>Reserved</td><td rowspan=1 colspan=2>TEMP_IT</td></tr><tr><td rowspan=1 colspan=1>148</td><td rowspan=1 colspan=1></td><td rowspan=1 colspan=1>Reserved</td><td rowspan=1 colspan=2>Reserved</td></tr><tr><td rowspan=1 colspan=1>149</td><td rowspan=1 colspan=1>NA</td><td rowspan=1 colspan=3>WKUP</td></tr><tr><td rowspan=1 colspan=1>150</td><td rowspan=1 colspan=2></td><td rowspan=1 colspan=2>OCTOSPI2</td></tr><tr><td rowspan=1 colspan=1>151</td><td rowspan=1 colspan=2></td><td rowspan=1 colspan=2>OTFDEC1</td></tr><tr><td rowspan=1 colspan=1>152</td><td rowspan=1 colspan=2></td><td rowspan=1 colspan=2>OTFDEC2</td></tr><tr><td rowspan=1 colspan=1>153</td><td rowspan=1 colspan=2></td><td rowspan=1 colspan=1>FMAC</td><td rowspan=1 colspan=1>GFXMUX</td></tr><tr><td rowspan=1 colspan=1>154</td><td rowspan=1 colspan=2></td><td rowspan=1 colspan=1>CORDIC</td><td rowspan=1 colspan=1>BDMA1</td></tr><tr><td rowspan=1 colspan=1>155</td><td rowspan=1 colspan=2></td><td rowspan=1 colspan=1>UART9</td><td rowspan=1 colspan=1></td></tr><tr><td rowspan=1 colspan=1>156</td><td rowspan=1 colspan=2>NA</td><td rowspan=1 colspan=1>USART10</td><td rowspan=1 colspan=1></td></tr><tr><td rowspan=1 colspan=1>157</td><td rowspan=1 colspan=2></td><td rowspan=1 colspan=1>I2C5_EV</td><td></td></tr><tr><td rowspan=1 colspan=1>158</td><td rowspan=1 colspan=2></td><td rowspan=1 colspan=1>I2C5_ER</td><td rowspan=1 colspan=1></td></tr><tr><td rowspan=1 colspan=1>159</td><td rowspan=1 colspan=2></td><td rowspan=1 colspan=1>FDCAN3_ITO</td><td rowspan=1 colspan=1></td></tr><tr><td rowspan=1 colspan=1>160</td><td rowspan=1 colspan=2></td><td rowspan=1 colspan=1>FDCAN3_IT1</td><td rowspan=1 colspan=1></td></tr><tr><td rowspan=1 colspan=1>161</td><td rowspan=1 colspan=2></td><td rowspan=1 colspan=1>TIM23</td><td rowspan=1 colspan=1></td></tr><tr><td rowspan=1 colspan=1>162</td><td rowspan=1 colspan=2></td><td rowspan=1 colspan=1>TIM24</td><td></td></tr></table>

# 6.5

# Extended interrupt and event controller (EXTI)

# 6.5.1

# EXTI main features in STM32H74x/75x, STM32H72x/73x and STM32H7A3/7Bx devices

The extended interrupt and event controller (EXTl) manages wakeup through configurable and direct event ako the D3/SRD domain DMAMUX2. It also generates events to the CPU event input.

The asynchronous event inputs are classified in two groups:

• Configurable events (active edge selection, dedicated pending flag, triggerable by software

Dve trpt wakur he pealge peal with the following features:

Fixed rising edge active trigger   
No interrupt pending status register bit in the EXTI (the interrupt pending status is provided by the   
peripheral generating the event)   
Individual interrupt and event generation mask   
No SW trigger possibility   
Direct system SRD domain wakeup events, that have a SRD pending mask and status register and   
may have a SRD interrupt signal

The table below describes the difference of EXTI event input types between STM32F7 Series, STM32H74x/75x, STM32H72x/73x and STM32H7A3/7Bx devices.

Table 15. EXTI event input types differences between STM32F7 Series, STM32H74x/75x, STM32H72x/73x and STM32H7A3/7Bx devices   

<table><tr><td rowspan=1 colspan=1>Main features</td><td rowspan=1 colspan=1>STM32F7 Series</td><td rowspan=1 colspan=1>STM32H74x/75x, STM32H72x/73x and STM32H7A3/7Bx</td></tr><tr><td rowspan=1 colspan=1>Configurable events</td><td rowspan=1 colspan=1>Available</td><td rowspan=1 colspan=1>Available</td></tr><tr><td rowspan=1 colspan=1>Direct events</td><td rowspan=1 colspan=1></td><td rowspan=1 colspan=1>Available</td></tr></table>

# 6.5.2

# EXTI block diagram in STM32H74x/75x, STM32H72x/73x and STM32H7A3/7Bx devices

blo l aamaskig block.Te registr block contais all hgisers.Te even iut gerb provides an event input edge triggering logic.

![](images/4ab4e7813fe97d43b5d71f18a15ff67133390f91693c7104068ac3a812fc0d28.jpg)  
Figure 9. EXTI block diagram on STM32H74x/75x, STM32H72x/73x and STM32H7A3/7Bx devices

# Note:

For more details about EXTI functional description and registers description, refer to RM0455. The table below presents the EXTI line differences between STM32F7 Series, STM32H74x/75x, STM32H72x/73x and STM32H7A3/7Bx devices.

Table 16. EXTI line differences between STM32F7 Series, STM32H74x/75x, STM32H72x/73x and STM32H7A3/7Bx devices   

<table><tr><td rowspan=2 colspan=1>EXTI line</td><td rowspan=2 colspan=1>STM32F7 Series</td><td rowspan=1 colspan=1>STM32H74x/75x</td><td rowspan=1 colspan=1>STM32H72x/73x</td><td rowspan=1 colspan=1>STM32H7A3/7Bx</td><td rowspan=2 colspan=1>Event input type</td></tr><tr><td rowspan=1 colspan=1>Source</td><td rowspan=1 colspan=1>Source</td><td rowspan=1 colspan=1>Source</td></tr><tr><td rowspan=1 colspan=1>0 - 15</td><td rowspan=1 colspan=1>EXTI[15:0]</td><td rowspan=1 colspan=3>EXTI[15:0]</td><td rowspan=1 colspan=1>Configurable</td></tr><tr><td rowspan=1 colspan=1>16</td><td rowspan=1 colspan=1>PVD output</td><td rowspan=1 colspan=3>PVD and AVD</td><td rowspan=1 colspan=1>Configurable</td></tr><tr><td rowspan=1 colspan=1>17</td><td rowspan=1 colspan=1>RTC alarm event</td><td rowspan=1 colspan=3>RTC alarms</td><td rowspan=1 colspan=1>Configurable</td></tr></table>

<table><tr><td rowspan=2 colspan=1>EXTI line</td><td rowspan=2 colspan=5>STM32F7 Series</td><td rowspan=1 colspan=1>STM32H74x/75x</td><td rowspan=1 colspan=1>STM32H72x/73x</td><td rowspan=1 colspan=1>STM32H7A3/7Bx</td><td rowspan=2 colspan=1>Event input type</td></tr><tr><td rowspan=1 colspan=1>Source</td><td rowspan=1 colspan=1>Source</td><td rowspan=1 colspan=1>Source</td></tr><tr><td rowspan=1 colspan=1>18</td><td rowspan=1 colspan=5>USB OTG FS wakeup event</td><td rowspan=1 colspan=3>RTC tamper, RTC timestamp, RCC LSECSS</td><td rowspan=1 colspan=1>Configurable</td></tr><tr><td rowspan=1 colspan=1>19</td><td rowspan=1 colspan=5>Ethernet wakeup event</td><td rowspan=1 colspan=3>RTC wakeup timer</td><td rowspan=1 colspan=1>Configurable</td></tr><tr><td rowspan=1 colspan=1>20</td><td rowspan=1 colspan=5>USB OTG HS (configured inFS wakeup event</td><td rowspan=1 colspan=3>COMP1</td><td rowspan=1 colspan=1>Configurable</td></tr><tr><td rowspan=1 colspan=1>21</td><td rowspan=1 colspan=5>RTC tamper and time stampevets</td><td rowspan=1 colspan=3>COMP2</td><td rowspan=1 colspan=1>Configurable</td></tr><tr><td rowspan=1 colspan=1>22</td><td rowspan=1 colspan=5>RTC wakeup event</td><td rowspan=1 colspan=3>I2C1 wakeup</td><td rowspan=1 colspan=1>Direct</td></tr><tr><td rowspan=1 colspan=1>23</td><td rowspan=1 colspan=5>LPTIM1 asynchronous event</td><td rowspan=1 colspan=3>I2C2 wakeup</td><td rowspan=1 colspan=1>Direct</td></tr><tr><td rowspan=1 colspan=1>24</td><td rowspan=1 colspan=5>MDIO slave asynchronousinterrupt</td><td rowspan=1 colspan=3>I2C3 wakeup</td><td rowspan=1 colspan=1>Direct</td></tr><tr><td rowspan=1 colspan=1>25</td><td rowspan=3 colspan=5></td><td rowspan=1 colspan=3>I2C4 wakeup</td><td rowspan=1 colspan=1>Direct</td></tr><tr><td rowspan=1 colspan=1>26</td><td rowspan=1 colspan=1></td><td rowspan=1 colspan=3>USART1 wakeup</td><td rowspan=1 colspan=1>Direct</td></tr><tr><td rowspan=1 colspan=1>27</td><td rowspan=1 colspan=3></td><td rowspan=1 colspan=2></td><td rowspan=1 colspan=3>USART2 wakeup</td><td rowspan=1 colspan=1>Direct</td></tr><tr><td rowspan=2 colspan=1>28</td><td rowspan=2 colspan=3></td><td rowspan=1 colspan=1></td><td rowspan=2 colspan=1></td><td rowspan=2 colspan=3>USART3 wakeup</td><td rowspan=2 colspan=1>Direct</td></tr><tr><td rowspan=1 colspan=2></td></tr><tr><td rowspan=1 colspan=1>29</td><td rowspan=1 colspan=5>NA</td><td rowspan=1 colspan=3>USART6 wakeup</td><td rowspan=1 colspan=1>Direct</td></tr><tr><td rowspan=1 colspan=1>30</td><td rowspan=1 colspan=5></td><td rowspan=1 colspan=3>UART4 wakeup</td><td rowspan=1 colspan=1>Direct</td></tr><tr><td rowspan=2 colspan=1>31</td><td rowspan=2 colspan=3></td><td rowspan=1 colspan=1></td><td rowspan=2 colspan=1></td><td rowspan=2 colspan=3>UART5 wakeup</td><td rowspan=2 colspan=1>Direct</td></tr><tr><td rowspan=1 colspan=2></td></tr><tr><td rowspan=1 colspan=1>32</td><td rowspan=1 colspan=4></td><td rowspan=1 colspan=1></td><td rowspan=1 colspan=3>UART7 wakeup</td><td rowspan=1 colspan=1>Direct</td></tr><tr><td rowspan=1 colspan=1>33</td><td rowspan=1 colspan=5></td><td rowspan=1 colspan=3>UART8 wakeup</td><td rowspan=1 colspan=1>Direct</td></tr><tr><td rowspan=1 colspan=1>34</td><td rowspan=2 colspan=5>NA</td><td rowspan=1 colspan=3>LPUART1 RX wakeup</td><td rowspan=1 colspan=1>Direct</td></tr><tr><td rowspan=1 colspan=1>35</td><td rowspan=1 colspan=3>LPUART1 TX wakeup</td><td rowspan=1 colspan=1>Direct</td></tr><tr><td rowspan=1 colspan=1>36</td><td rowspan=1 colspan=5></td><td rowspan=1 colspan=3>SPI1 wakeup</td><td rowspan=1 colspan=1>Direct</td></tr><tr><td rowspan=2 colspan=1>37</td><td rowspan=2 colspan=3></td><td rowspan=1 colspan=1></td><td rowspan=2 colspan=1></td><td rowspan=2 colspan=3>SPI2 wakeup</td><td rowspan=2 colspan=1>Direct</td></tr><tr><td rowspan=1 colspan=2></td></tr><tr><td rowspan=2 colspan=1>38</td><td rowspan=2 colspan=3></td><td rowspan=1 colspan=1></td><td rowspan=2 colspan=1></td><td rowspan=2 colspan=3>SPI3 wakeup</td><td rowspan=2 colspan=1>Direct</td></tr><tr><td rowspan=1 colspan=2></td></tr><tr><td rowspan=1 colspan=1>39</td><td rowspan=2 colspan=5>NA</td><td rowspan=1 colspan=3>SPI4 wakeup</td><td rowspan=1 colspan=1>Direct</td></tr><tr><td rowspan=1 colspan=1>40</td><td rowspan=1 colspan=3>SPI5 wakeup</td><td rowspan=1 colspan=1>Direct</td></tr><tr><td rowspan=2 colspan=1>41</td><td rowspan=2 colspan=3></td><td rowspan=1 colspan=2></td><td rowspan=2 colspan=1></td><td rowspan=2 colspan=3>SPI6 wakeup</td></tr><tr><td rowspan=1 colspan=2></td><td></td></tr><tr><td rowspan=1 colspan=1>42</td><td rowspan=1 colspan=4></td><td rowspan=1 colspan=1></td><td rowspan=1 colspan=3>MDIO wakeup</td><td rowspan=1 colspan=1>Direct</td></tr><tr><td rowspan=1 colspan=1>43</td><td rowspan=1 colspan=5></td><td rowspan=1 colspan=3>USB1 wakeup</td><td rowspan=1 colspan=1>Direct</td></tr><tr><td rowspan=1 colspan=1>44</td><td rowspan=1 colspan=5>NA</td><td rowspan=1 colspan=2>USB2 wakeup</td><td rowspan=1 colspan=1>Reserved</td><td rowspan=1 colspan=1>Direct</td></tr><tr><td rowspan=1 colspan=1>47</td><td rowspan=1 colspan=5></td><td rowspan=1 colspan=3>LPTIM1 wakeup</td><td rowspan=1 colspan=1>Direct</td></tr><tr><td rowspan=2 colspan=1>48</td><td rowspan=2 colspan=3></td><td rowspan=1 colspan=1></td><td rowspan=2 colspan=1></td><td rowspan=2 colspan=3>LPTIM2 wakeup</td><td rowspan=2 colspan=1>Direct</td></tr><tr><td rowspan=1 colspan=2></td></tr><tr><td rowspan=1 colspan=1>49</td><td rowspan=1 colspan=5>NA</td><td rowspan=1 colspan=3>LPTIM2 output</td><td rowspan=1 colspan=1>Configurable</td></tr><tr><td rowspan=1 colspan=1>50</td><td rowspan=1 colspan=5></td><td rowspan=1 colspan=3>LPTIM3 wakeup</td><td rowspan=1 colspan=1>Direct</td></tr><tr><td rowspan=1 colspan=1>51</td><td rowspan=1 colspan=5></td><td rowspan=1 colspan=3>LPTIM3 output</td><td rowspan=1 colspan=1>Configurable</td></tr><tr><td rowspan=1 colspan=1>52</td><td rowspan=2 colspan=5>NA</td><td rowspan=1 colspan=2>LPTIM4 wakeup</td><td rowspan=1 colspan=1>UART9 wakeup</td><td rowspan=1 colspan=1>Direct</td></tr><tr><td rowspan=1 colspan=1>53</td><td rowspan=1 colspan=2>LPTIM5 wakeup</td><td rowspan=1 colspan=1>USART10 wakeup</td><td rowspan=1 colspan=1>Direct</td></tr><tr><td rowspan=1 colspan=1>54</td><td rowspan=1 colspan=5></td><td rowspan=1 colspan=3>SWPMI wakeup</td><td rowspan=1 colspan=1>Direct</td></tr><tr><td rowspan=1 colspan=1>55</td><td rowspan=2 colspan=5>NA</td><td rowspan=1 colspan=3>WKUP1</td><td rowspan=1 colspan=1>Direct</td></tr><tr><td rowspan=1 colspan=1>56</td><td rowspan=1 colspan=3>WKUP2</td><td rowspan=1 colspan=1>Direct</td></tr><tr><td rowspan=1 colspan=1>57</td><td rowspan=1 colspan=5></td><td rowspan=1 colspan=1>WKUP3</td><td rowspan=1 colspan=1>Reserved</td><td rowspan=1 colspan=1>WKUP3</td><td rowspan=1 colspan=1>Direct</td></tr></table>

<table><tr><td rowspan=2 colspan=1>EXTI line</td><td rowspan=2 colspan=1>STM32F7 Series</td><td rowspan=1 colspan=1>STM32H74x/75x</td><td rowspan=1 colspan=1>STM32H72x/73x</td><td rowspan=1 colspan=1>STM32H7A3/7Bx</td><td rowspan=1 colspan=1></td><td rowspan=2 colspan=1>Event input type</td></tr><tr><td rowspan=1 colspan=1>Source</td><td rowspan=1 colspan=1>Source</td><td rowspan=1 colspan=1>Source</td><td></td></tr><tr><td rowspan=1 colspan=1>58</td><td rowspan=1 colspan=1></td><td rowspan=1 colspan=1></td><td rowspan=1 colspan=1>WKUP4</td><td rowspan=1 colspan=1></td><td rowspan=1 colspan=2>Direct</td></tr><tr><td rowspan=1 colspan=1>59</td><td rowspan=1 colspan=1></td><td rowspan=1 colspan=1>WKUP5</td><td rowspan=1 colspan=1>Reserved</td><td rowspan=1 colspan=1>WKUP5</td><td rowspan=1 colspan=2>Direct</td></tr><tr><td rowspan=1 colspan=1>60</td><td rowspan=1 colspan=1></td><td rowspan=1 colspan=3>WKUP6</td><td rowspan=1 colspan=2>Direct</td></tr><tr><td rowspan=1 colspan=1>61</td><td rowspan=1 colspan=1>NA</td><td rowspan=1 colspan=3>RCC interrupt</td><td rowspan=1 colspan=2>Direct</td></tr><tr><td rowspan=1 colspan=1>62</td><td rowspan=1 colspan=1></td><td rowspan=1 colspan=3>I2C4 Event interrupt</td><td rowspan=1 colspan=2>Direct</td></tr><tr><td rowspan=1 colspan=1>63</td><td rowspan=1 colspan=1></td><td rowspan=1 colspan=3>I2C4 Error interrupt</td><td rowspan=1 colspan=2>Direct</td></tr><tr><td rowspan=1 colspan=1>64</td><td rowspan=1 colspan=1></td><td rowspan=1 colspan=3>LPUART1 global Interrupt</td><td rowspan=1 colspan=2>Direct</td></tr><tr><td rowspan=1 colspan=1>65</td><td rowspan=1 colspan=1></td><td rowspan=1 colspan=3>SPI6 interrupt</td><td rowspan=1 colspan=2>Direct</td></tr><tr><td rowspan=1 colspan=1>66</td><td rowspan=1 colspan=1></td><td rowspan=1 colspan=2>BDMA CHO interrupt</td><td rowspan=1 colspan=1>BDMA2 CHO interrupt</td><td rowspan=1 colspan=2>Direct</td></tr><tr><td rowspan=1 colspan=1>67</td><td rowspan=1 colspan=1></td><td rowspan=1 colspan=2>BDMA CH1 interrupt</td><td rowspan=1 colspan=1>BDMA2 CH1 interrupt</td><td rowspan=1 colspan=2>Direct</td></tr><tr><td rowspan=1 colspan=1>68</td><td rowspan=1 colspan=1></td><td rowspan=1 colspan=2>BDMA CH2 interrupt</td><td rowspan=1 colspan=1>BDMA2 CH2 interrupt</td><td rowspan=1 colspan=2>Direct</td></tr><tr><td rowspan=1 colspan=1>69</td><td rowspan=1 colspan=1>NA</td><td rowspan=1 colspan=2>BDMA CH3 interrupt</td><td rowspan=1 colspan=1>BDMA2 CH3 interrupt</td><td rowspan=1 colspan=2>Direct</td></tr><tr><td rowspan=1 colspan=1>70</td><td rowspan=1 colspan=1></td><td rowspan=1 colspan=2>BDMA CH4 interrupt</td><td rowspan=1 colspan=1>BDMA2 CH4 interrupt</td><td rowspan=1 colspan=2>Direct</td></tr><tr><td rowspan=1 colspan=1>71</td><td rowspan=1 colspan=1></td><td rowspan=1 colspan=2>BDMA CH5 interrupt</td><td rowspan=1 colspan=1>BDMA2 CH5 interrupt</td><td rowspan=1 colspan=2>Direct</td></tr><tr><td rowspan=1 colspan=1>72</td><td rowspan=1 colspan=1></td><td rowspan=1 colspan=2>BDMA CH6 interrupt</td><td rowspan=1 colspan=1>BDMA2 CH6 interrupt</td><td rowspan=1 colspan=2>Direct</td></tr><tr><td rowspan=1 colspan=1>73</td><td rowspan=1 colspan=1></td><td rowspan=1 colspan=2>BDMA CH7 interrupt</td><td rowspan=1 colspan=1>BDMA2 CH7 interrupt</td><td rowspan=1 colspan=2>Direct</td></tr><tr><td rowspan=1 colspan=1>74</td><td rowspan=1 colspan=1>NA</td><td rowspan=1 colspan=3>DMAMUX2 interrupt</td><td rowspan=1 colspan=2>Direct</td></tr><tr><td rowspan=1 colspan=1>75</td><td rowspan=1 colspan=1></td><td rowspan=1 colspan=2>ADC3 interrupt</td><td rowspan=1 colspan=1>Reserved</td><td rowspan=1 colspan=2>Direct</td></tr><tr><td rowspan=1 colspan=1>76</td><td rowspan=1 colspan=1>NA</td><td rowspan=1 colspan=2>SAI4 interrupt</td><td rowspan=1 colspan=1>Reserved</td><td rowspan=1 colspan=2>Direct</td></tr><tr><td rowspan=1 colspan=1>77</td><td rowspan=1 colspan=1></td><td rowspan=1 colspan=1>NA</td><td rowspan=1 colspan=1>HSEMO</td><td rowspan=1 colspan=1>NA</td><td rowspan=1 colspan=2>-</td></tr><tr><td rowspan=1 colspan=1>85</td><td rowspan=1 colspan=1>NA</td><td rowspan=1 colspan=3>HDMICEC wakeup</td><td rowspan=1 colspan=2>Configurable</td></tr><tr><td rowspan=1 colspan=1>86</td><td rowspan=1 colspan=1>NA</td><td rowspan=1 colspan=1>ETHERNET wakeup</td><td rowspan=1 colspan=1>ETH_ASYNC_IT</td><td rowspan=1 colspan=1>Reserved</td><td rowspan=1 colspan=2>Configurable</td></tr><tr><td rowspan=1 colspan=1>87</td><td rowspan=1 colspan=1>NA</td><td rowspan=1 colspan=3>HSECSS interrupt</td><td rowspan=1 colspan=2>Direct</td></tr><tr><td rowspan=1 colspan=1>88</td><td rowspan=1 colspan=1>NA</td><td rowspan=1 colspan=1>Reserved</td><td rowspan=1 colspan=2>TEMP wakeup</td><td rowspan=1 colspan=2>Direct</td></tr><tr><td rowspan=1 colspan=1>89</td><td rowspan=1 colspan=2></td><td rowspan=1 colspan=1>UART9 wakeup</td><td rowspan=1 colspan=1>NA</td><td rowspan=1 colspan=2></td></tr><tr><td rowspan=1 colspan=1>90</td><td rowspan=2 colspan=2>NA</td><td rowspan=1 colspan=1>USART10 wakeup</td><td rowspan=1 colspan=1>NA</td><td rowspan=1 colspan=2>-</td></tr><tr><td rowspan=1 colspan=1>91</td><td rowspan=1 colspan=1>I2C5 wakeup</td><td rowspan=1 colspan=1>NA</td><td rowspan=1 colspan=2>-</td></tr></table>

For more details about EXTI events input mapping, refer to EXTI event input mapping section of RM0433, RM0468 and RM0455 reference manuals.

# 6.6

# Reset and clock control (RCC)

# 6.6.1

#

# Clock manageme

The table below presents the source clock differences between STM32F7 Series, STM32H74x/75x, STM32H72x/73x and STM32H7A3/7Bx devices.

Table 17. Different source clock in STM32F7 Series, STM32H74x/75x, STM32H72x/73x and STM32H7A3/7Bx devices   

<table><tr><td rowspan=1 colspan=2>Source clock</td><td rowspan=1 colspan=1>STM32F7 Series</td><td rowspan=1 colspan=1>STM32H74x/75x, STM32H72x/73x and STM32H7A3/7Bx</td></tr><tr><td rowspan=4 colspan=1>Internal oscillators</td><td rowspan=1 colspan=1>HSI</td><td rowspan=1 colspan=1>16 MHz</td><td rowspan=1 colspan=1>8/16/32/64 MHz</td></tr><tr><td rowspan=1 colspan=1>HSI48</td><td rowspan=1 colspan=1>NA</td><td rowspan=1 colspan=1>48 MHz</td></tr><tr><td rowspan=1 colspan=1>CSI</td><td rowspan=1 colspan=1>NA</td><td rowspan=1 colspan=1>4 MHz</td></tr><tr><td rowspan=1 colspan=1>LSI</td><td rowspan=1 colspan=1>32 kHz</td><td rowspan=1 colspan=1>32 kHz</td></tr><tr><td rowspan=2 colspan=1>External oscillators</td><td rowspan=1 colspan=1>HSE</td><td rowspan=1 colspan=1>4-26 MHz</td><td rowspan=1 colspan=1>4-50 MHz</td></tr><tr><td rowspan=1 colspan=1>LSE</td><td rowspan=1 colspan=1></td><td rowspan=1 colspan=1>32.768 kHz</td></tr><tr><td rowspan=1 colspan=2>PLLs(1)</td><td rowspan=1 colspan=1>x3without fractional mode</td><td rowspan=1 colspan=1>x3with fractional mode(13-bit fractional multiplication factor)</td></tr></table>

Special care to be taken for the PLL configuration:

STM32H72x/73x and STM32H74x/75x: the PLL VCO max frequency is 836 MHz STM32H7A3/7Bx: the PLL VCO max frequency is 560 MHz

# 6.6.2 Peripheral clock distribution

T pheal clocksecloc poi y e e prealsT kindclock vl:

The bus interface clock The kernel clocks

On STM32H74x/75x, STM32H72x/73x and STM32H7A3/7Bx devices, the peripherals generally receive:

One or several bus clocks.   
One or several kernel clocks.

Figure 10 describes the peripheral clock distribution on STM32H74x/75x, STM32H72x/73x and STM32H7A3/7Bx devices.

Figure 10. Peripheral clock distribution on STM32H74x/75x, STM32H72x/73x and STM32H7A3/7Bx devices

![](images/87bbd2d1d5237f2c35dbde729d0a60969d7c1983a670bebfea80c2d73a97173f.jpg)

The following table describes an example of peripheral clock distribution for STM32F7 Series, STM32H74x/75x, STM32H72x/73x and STM32H7A3/7Bx devices.

F   v RM0455, RM0468 and RM0433 reference manuals.

Table 18. Peripheral clock distribution example   

<table><tr><td rowspan=1 colspan=1>Peripheral</td><td rowspan=1 colspan=1>STM32F7 Series</td><td rowspan=1 colspan=1>STM32H74x/75x, STM32H72x/73x and STM32H7A3/7Bx</td></tr><tr><td rowspan=1 colspan=1>SPI1</td><td rowspan=1 colspan=1>APB2_Clock</td><td rowspan=1 colspan=1>Bus clockAPB2_ClockKernel clockP1_q_ck/PII2_p_ck/PII3_p_ck/l2S_CKIN/Per_ck</td></tr><tr><td rowspan=1 colspan=1>USART1</td><td rowspan=1 colspan=1>•    Bus clockAPB2_ClockKernel clockLSEHSISYSCLKPCLK2</td><td rowspan=1 colspan=1>Bus clockAPB2_ClockKernel clockPII2_q_ck/pll3_q_ck/hsi_ker_ck/csi_ker_ck/lse_ck</td></tr></table>

# 6.7

# Operating conditions

The table below illustrates the maximum operating frequency of STM32F7 Series, STM32H74x/75x, STM32H72x/73x and STM32H7A3/7Bx devices.

Table 19. General operating conditions for STM32F7 Series, STM32H74x/75x, STM32H72x/73x and STM32H7A3/7Bx devices   

<table><tr><td rowspan=2 colspan=1>Scale</td><td rowspan=2 colspan=1>STM32F7Series devicesmaximumfrequency</td><td rowspan=1 colspan=2>STM32H74x/75x devicesmaximum frequency</td><td rowspan=1 colspan=2>STM32H72x/73xdevices maximumfrequency</td><td rowspan=1 colspan=2>STM32H7A3/7Bx devicesmaximum frequency</td><td rowspan=2 colspan=1>Unit</td></tr><tr><td rowspan=1 colspan=1>Max CPU</td><td rowspan=1 colspan=1>Max D1/D2/D3</td><td rowspan=1 colspan=1>Max CPU</td><td rowspan=1 colspan=1>MaxD1/D2/D3</td><td rowspan=1 colspan=1>Max CPU</td><td rowspan=1 colspan=1>Max CD/SRD</td></tr><tr><td rowspan=1 colspan=1>Scale 0</td><td rowspan=1 colspan=1>NA</td><td rowspan=1 colspan=1>480</td><td rowspan=1 colspan=1>240</td><td rowspan=1 colspan=1>550</td><td rowspan=1 colspan=1>275</td><td rowspan=1 colspan=1>280</td><td rowspan=1 colspan=1>280</td><td rowspan=4 colspan=1>MHz</td></tr><tr><td rowspan=1 colspan=1>Scale 1</td><td rowspan=1 colspan=1>216</td><td rowspan=1 colspan=1>400</td><td rowspan=1 colspan=1>200</td><td rowspan=1 colspan=1>400</td><td rowspan=1 colspan=1>200</td><td rowspan=1 colspan=1>225</td><td rowspan=1 colspan=1>225</td></tr><tr><td rowspan=1 colspan=1>Scale 2</td><td rowspan=1 colspan=1>180</td><td rowspan=1 colspan=1>300</td><td rowspan=1 colspan=1>160</td><td rowspan=1 colspan=1>300</td><td rowspan=1 colspan=1>150</td><td rowspan=1 colspan=1>160</td><td rowspan=1 colspan=1>160</td></tr><tr><td rowspan=1 colspan=1>Scale 3</td><td rowspan=1 colspan=1>144</td><td rowspan=1 colspan=1>200</td><td rowspan=1 colspan=1>88</td><td rowspan=1 colspan=1>170</td><td rowspan=1 colspan=1>85</td><td rowspan=1 colspan=1>88</td><td rowspan=1 colspan=1>88</td></tr></table>

# 7 Power (PWR)

The table below presents the PWR controller differences between STM32F7 Series, STM32H74x/75x, STM32H72x/73x and STM32H7A3/7Bx devices. Both dynamic and static power-consumption had been optimized for the STM32H7A3/7Bx devices.

Table 20. PWR differences between STM32F7 Series, STM32H74x/75x, STM32H72x/73x and STM32H7A3/7Bx devices   

<table><tr><td colspan="1" rowspan="1"></td><td colspan="1" rowspan="1">PWR</td><td colspan="1" rowspan="1">STM32F7 Series</td><td colspan="1" rowspan="1">STM32H72x/73x andSTM32H74x/75x</td><td colspan="2" rowspan="1">STM32H7A3/7Bx</td></tr><tr><td colspan="1" rowspan="10">20</td><td colspan="1" rowspan="5">Autonomous mode(basic operation with inactiveCPU domain(s) in low-powermode</td><td colspan="1" rowspan="5">NA</td><td colspan="1" rowspan="1">D3 in Run mode</td><td colspan="2" rowspan="1">SRD in Run mode</td></tr><tr><td colspan="1" rowspan="1">D1/D2 in DStop</td><td colspan="2" rowspan="1">CD in DStop</td></tr><tr><td colspan="1" rowspan="1">NA</td><td colspan="2" rowspan="1">CD in DStop with RAMSh ut-off 1)</td></tr><tr><td colspan="1" rowspan="1">D1/D2 in DStandby</td><td colspan="2" rowspan="1">NA</td></tr><tr><td colspan="1" rowspan="1">NA</td><td colspan="2" rowspan="1">CD in DStop2(retention mode)with/without RAM Shuf-ooff()</td></tr><tr><td colspan="3" rowspan="5">Stop</td><td colspan="1" rowspan="2">Stop</td><td colspan="1" rowspan="1">D3 in DStop</td><td colspan="1" rowspan="1">SRD in DStop</td></tr><tr><td colspan="1" rowspan="1">D1/D2 in DStop</td><td colspan="2" rowspan="1">CD in DStop</td></tr><tr><td colspan="1" rowspan="3">NA</td><td colspan="1" rowspan="1">NA</td><td colspan="2" rowspan="1">CD in DStop with RAMSh ut-off(1)</td></tr><tr><td colspan="1" rowspan="1">D1/D2 in DStandby</td><td colspan="2" rowspan="1">NA</td></tr><tr><td colspan="1" rowspan="1">NA</td><td colspan="2" rowspan="1">CD in DStop2(retention mode)with/without RAM Shuf-off(1)</td></tr><tr><td colspan="1" rowspan="9">Pons Jaies</td><td colspan="1" rowspan="1">External power supply for I/Os</td><td colspan="1" rowspan="1">VDD = 1.7 to 3.6 V</td><td colspan="3" rowspan="1">VDD = 1.62 to 3.6 V</td></tr><tr><td colspan="1" rowspan="1">Internal regulator (LDO)supplying VCORE</td><td colspan="1" rowspan="1">VDD = 1.7 to 3.6 V</td><td colspan="3" rowspan="1">VDDLDO = 1.62 to 3.6 V</td></tr><tr><td colspan="1" rowspan="1">Step-down converter (SMPS)supplying VCORE</td><td colspan="1" rowspan="1">NA</td><td colspan="3" rowspan="1">VDDSMPS = 1.62 to 3.6 V</td></tr><tr><td colspan="1" rowspan="2">External analog power supply</td><td colspan="1" rowspan="1">VDDA = 1.7 to 3.6 VVREF-</td><td colspan="3" rowspan="1">VDDA = 1.8 to 3.6 VVREF-</td></tr><tr><td colspan="1" rowspan="1">VREF+: a separate referencevoltage, available on VREF+pin for ADC and DAC</td><td colspan="3" rowspan="1">VREF+: a separate reference voltage, available onVREF+ pin for ADC and DACWhen enabled by ENVR bit in the VREFBUF controlstatus and status register + is provided fromthe internal voltage reference buffer</td></tr><tr><td colspan="1" rowspan="1">USB power supply</td><td colspan="1" rowspan="1">VDD33USB = 3.0 to 3.6 V</td><td colspan="3" rowspan="1">VDD33USB = 3.0 to 3.6 VVDD50USB = 4.0 to 5.5 V</td></tr><tr><td colspan="1" rowspan="1">Backup domain</td><td colspan="1" rowspan="1">VBAT = 1.65 to 3.6 V</td><td colspan="3" rowspan="1">VBAT = 1.2 to 3.6 V</td></tr><tr><td colspan="3" rowspan="1">Independent power supply</td><td colspan="1" rowspan="1">VDDSDMMC = 1.7 to 3.6 VVDDDSI = 1.7 to 3.6 V</td><td colspan="1" rowspan="1">NANA</td><td colspan="1" rowspan="1">VDDMMC = 1.62 to 3.6 VNA</td></tr><tr><td colspan="3" rowspan="1">VCORE supplies</td><td colspan="1" rowspan="1">1.08 V ≤ VCAP_1 andVCAP_2 ≤ 1.40 V</td><td colspan="1" rowspan="1">0.7 V ≤ VCAP ≤ 1.35 V</td><td colspan="1" rowspan="1">1.0 V ≤ VCAP ≤ 1.3V</td></tr><tr><td colspan="3" rowspan="1">PWR</td><td colspan="1" rowspan="1">STM32F7 Series</td><td colspan="1" rowspan="1">STM32H72x/73x andSTM32H74x/75x</td><td colspan="1" rowspan="1">STM32H7A3/7Bx</td></tr><tr><td colspan="1" rowspan="4">Podne Jies</td><td colspan="1" rowspan="4">Reg bypass:must besupplied fromxxternalregulator onVCAP pins</td><td colspan="1" rowspan="1">VOSO</td><td colspan="1" rowspan="1">NA</td><td colspan="1" rowspan="1">1.35 V</td><td colspan="1" rowspan="1">1.3 V</td></tr><tr><td colspan="1" rowspan="1">VOS1</td><td colspan="1" rowspan="1">1.32 V</td><td colspan="2" rowspan="1">1.2 V</td></tr><tr><td colspan="1" rowspan="1">VOS2</td><td colspan="1" rowspan="1">1.26 V</td><td colspan="2" rowspan="1">1.1 V</td></tr><tr><td colspan="1" rowspan="1">VOS3</td><td colspan="1" rowspan="1">1.14 V</td><td colspan="2" rowspan="1">1.00 V</td></tr><tr><td colspan="3" rowspan="1">Peripheral supply regulation</td><td colspan="1" rowspan="1">DSI voltage regulator</td><td colspan="2" rowspan="1">USB regulator</td></tr><tr><td colspan="3" rowspan="2">Power supply supervision</td><td colspan="3" rowspan="1">POR/PDR monitorBOR monitorPVD monitor</td></tr><tr><td colspan="1" rowspan="1">NA</td><td colspan="2" rowspan="1">AVD monitor(3)VBAT thresholds(4)Temperature thresholds(5)</td></tr></table>

1. lost (refer to RM0455).

For moredetails about VREFBUF eeVoltage reference buffer (VREFBUF) sctio  RM0433, RM0468 andRM0455 reference manuals.

V L: the PWR_CR1 register. The ÁVD is enabled by setting the AVDEN bit in the PWR_CR1 register.

1. atolthhoAo)iAerhanA monitoring (available only in VBAT mode) can be enabled/disabled via MONEN bit in the PWR_CR2 register.

5. TeaoaablOWRR indicates whether the device temperature is higher or lower than the threshold.

# System configuration controller (SYSCFG)

The table below illustrates the SYSCFG main differences between STM32F7 Series, STM32H74x/75x, STM32H72x/73x and STM32H7A3/7Bx devices.

Table 21. SYSCFG main features differences between STM32F7 Series, STM32H74x/75x, STM32H72x/73x and STM32H7A3/7Bx devices   

<table><tr><td rowspan=1 colspan=1>.</td><td rowspan=1 colspan=1>STM32F7 Series</td><td rowspan=1 colspan=1>STM32H74x/75x</td><td rowspan=1 colspan=1>STM32H72x/73x</td><td rowspan=1 colspan=1>STM32H7A3/7Bx</td></tr><tr><td rowspan=6 colspan=1>0</td><td rowspan=1 colspan=1>Remap the memoryareasManage Class Bfeature</td><td rowspan=1 colspan=3>NA</td></tr><tr><td rowspan=1 colspan=3>Select the Ethernet PHY interface</td><td rowspan=1 colspan=1>NA</td></tr><tr><td rowspan=1 colspan=4>Manage the external interrupt line connection to the GPIOsManage I/O compensation cell featureI2C Fast mode + configuration</td></tr><tr><td rowspan=1 colspan=1>NA</td><td rowspan=1 colspan=3>Analog switch configuration management</td></tr><tr><td rowspan=1 colspan=1>NA</td><td rowspan=1 colspan=2>Get readout protection and flash memory bank swapinformationsManagement of boot sequences and boot addressesGet BOR reset levelGet flash memory secured and protected sector statusGet flash memory write protections statusGet DTCM secured section statusGet independent watchdog behavior (hardware or software /freezeReset generation in Stop and Standby modeGet secure mode enabling/disabling</td><td rowspan=1 colspan=1>Not part of the systemcontrollerFeatures are part of the flashmemory registers</td></tr><tr><td rowspan=1 colspan=2>NA</td><td rowspan=1 colspan=1>Management of timer break input lockControl CPU frequency boost</td><td rowspan=1 colspan=1>NA</td></tr></table>

Note:

For more details, refer to the SYSCFG register description section of RM0433, RM0468 and RM0455 reference manuals.

# 9 Secure digital input/output and MultiMediaCard interface (SDMMC)

The following table presents the differences between the SDMMC interface of STM32F7 Series, STM32H74x75x, STM32H72x/73x and STM32H7A3/7Bx devices.

Table 22. SDMMC differences between STM32F7 Series, STM32H74x/75x, STM32H72x/73x and STM32H7A3/7Bx devices   
Depending of the maximum allowed IO speed. for more details refer to datasheets.   

<table><tr><td rowspan=1 colspan=1>SDMMC</td><td rowspan=1 colspan=1>STM32F7 Series</td><td rowspan=1 colspan=1>STM32H72x/73x andSTM32H74x/75x</td><td rowspan=1 colspan=1>STM32H7A3/7Bx</td></tr><tr><td rowspan=6 colspan=1>Fenues</td><td rowspan=1 colspan=1>Full compliance withMultiMediaCard systemspecification version 4.2.Card support for three differentdatabus modes: 1-bit (default), 4-bit and 8-bit</td><td rowspan=1 colspan=2>Full compliance with MultiMediaCard system specification version 4.51.Card support for three different databus modes: 1-bit (default), 4-bitand 8-bit</td></tr><tr><td rowspan=1 colspan=1>Full compliance with SD memorycard specifications version 2.0</td><td rowspan=1 colspan=2>Full compliance with SD memory card specifications version 4.1.</td></tr><tr><td rowspan=1 colspan=1>Full compliance with SD I/O cardspecification version 2.0.Card support for two differentdatabus modes: 1-bit (default) and4-bit</td><td rowspan=1 colspan=2>Full compliance with SDIO card specification version 4.0.Card support for two different databus modes: 1-bit (default) and 4-bit.</td></tr><tr><td rowspan=1 colspan=1>Data transfer up to 200 Mbyte/sfor the 8-bit mode.</td><td rowspan=1 colspan=2>Data transfer up to 208 Mbyte/s for the 8-bit mode.</td></tr><tr><td rowspan=1 colspan=1>NA</td><td rowspan=1 colspan=2>SDMMC IDMA: is used to provide high speed transfer between theSDMMC FIFO and the memory.The AHB master optimizes the bandwidth of the system bus.The SDMMC internal DMA (IDMA) provides one channel to be usedeither for transmit or receive.</td></tr><tr><td rowspan=1 colspan=1>Independent power supply forSDMC2</td><td rowspan=1 colspan=1>NA</td><td rowspan=1 colspan=1>Independent power supply forSDMC2</td></tr></table>

# 10 Universal (synchronous) asynchronous receiver-transmitter (U(S)ART)

The STM32H74x/75x, STM32H72x/73x and STM32H7A3/7Bx devices implement several new features on the U(S)ART compared to the STM32F7 Series devices. The following table shows the U(S)ART differences.

Table 23. U(S)ART differences between STM32F7 Series, STM32H74x/75x, STM32H72x/73x and STM32H7A3/7Bx devices   

<table><tr><td rowspan=1 colspan=1>U(S)ART</td><td rowspan=1 colspan=1>STM32F7 Series</td><td rowspan=1 colspan=1>STM32H74x/75x3</td><td rowspan=1 colspan=1>STM32H72x/73x and STM32H7A3/7Bx</td></tr><tr><td rowspan=1 colspan=1>Instances</td><td rowspan=1 colspan=1>X4 USARTX4 UART</td><td rowspan=1 colspan=1>x4 USARTX4 UARTx1 LPUART</td><td rowspan=1 colspan=1>x5 USARTx5 UARTx1 LPUART</td></tr><tr><td rowspan=1 colspan=1>Clock</td><td rowspan=1 colspan=3>Dual clock domain with dedicated kernel clock for peripherals independent from PCLK</td></tr><tr><td rowspan=1 colspan=1>Wakeup</td><td rowspan=1 colspan=1></td><td rowspan=1 colspan=2>Wakeup from low-power mode</td></tr><tr><td rowspan=1 colspan=1>Features</td><td rowspan=1 colspan=1>NA</td><td rowspan=1 colspan=2>SPI slave transmission, underrun flagTwo internal FIFOs for transmit and receive dataEach FIFO can be enabled/disabled by software and come with a status flag.</td></tr></table>

# 11 Serial peripheral interface (SPI)

The STM32H74x/75x, STM32H72x/73x and STM32H7A3/7Bx devices implement some enhanced SPI compared to the STM32F7 Series devices. See the table below for the SPI differences.

Table 24. SPI differences between STM32F7 Series, STM32H74x/75x, STM32H72x/73x and STM32H7A3/7Bx devices   

<table><tr><td>SPI</td><td>STM32F7 Series</td><td>STM32H74x/75x, STM32H72x/73x and STM32H7A3/7Bx</td></tr><tr><td>Instances</td><td>X4</td><td>x6</td></tr><tr><td>Clock</td><td>Single clock domain</td><td>Dual clock domain with dedicated kernel and serial interface clock independent from PCLK with transmission and reception capability at low-power stop</td></tr><tr><td>Wakeup</td><td>NA</td><td>Wakeup from low-power mode Full-duplex synchronous transfers on three lines (with two separated data lines)</td></tr><tr><td>Features</td><td colspan="2">Half-duplex synchronous transfer on two lines (with single bidirectional data line) Simplex synchronous transfers on two lines (with unidirectional data line) 8 master mode baud rate prescalers up to fPCLK/2 Slave mode frequency up to fPCLK/2 NSS management by hardware or software for both master and slave Master and slave capability, multi-master multi-slave support Programmable clock polarity and phase Programmable data order with MSB-first or LSB-first shifting Dedicated transmission, reception and error flags with interrupt capability SPI Motorola and TI formats support Hardware CRC feature for reliable communication (at the end of transaction): Configurable size and polynomial Autommatic CRC upend in Tx mode Automatic CRC check in Rx mode Configurable RxFIFO threshold, data packeting support Configurable data size (4-32 bit) Protection of configuration and setting Adjustable minimum delays between data and between SS and data flow at master Configurable SS signal polarity and timing, MISO x MOSI swap capability Programmable number of data within a transaction to control SS and CRC Two 16x or 8x 8-bit embedded Rx and TxFIFOs with Two 32-bit embedded Rx and Tx DMA capability FIFOs with DMA capability Programmable number of data in transaction CRC pattern size 8 or 16 bit Configurable behavior at slave underrun condition (support of cascaded circular buffers) RxFIFO threshold 8 or 16 bit Master automatic suspend at receive mode Master start/suspend control Alternate function control of associated GPIOs Selected status and error flags with wake up capability CRC pattern size configurable from 4 to 32 bit Configurable CRC polynomial length RxFIFO threshold from 1 to 16 data</td></tr></table>

# 12 Integrated interchip sound interface (I2S)

The table below presents the I2S differences between the STM32F7 Series, STM32H74x/75x, STM32H72x/73x and STM32H7A3/7Bx devices.

Table 25. I2S differences between STM32F7 Series, STM32H74x/75x, STM32H72x/73x and STM32H7A3/7Bx devices   

<table><tr><td rowspan=1 colspan=1>I2S</td><td rowspan=1 colspan=1>STM32F7 Series</td><td rowspan=1 colspan=1>STM32H74x/75x3</td><td rowspan=1 colspan=1>STM32H72x/73x andSTM32H7A3/7Bx</td></tr><tr><td rowspan=15 colspan=1>FenS</td><td rowspan=1 colspan=1>x3</td><td rowspan=1 colspan=1>x3</td><td rowspan=1 colspan=1>X4</td></tr><tr><td rowspan=1 colspan=1>Full duplex only when theextension module is implemented</td><td rowspan=1 colspan=2>Full duplex native</td></tr><tr><td rowspan=1 colspan=1>Minimum allowed value = 4</td><td rowspan=1 colspan=2>More flexible clock generator (division by 1,2 are possible)</td></tr><tr><td rowspan=1 colspan=1>Sampling edge is notprogrammable</td><td rowspan=1 colspan=2>Programmable sampling edge for the bit clock</td></tr><tr><td rowspan=1 colspan=1>Frame sync polarity cannot beselected</td><td rowspan=1 colspan=2>Programmable frame sync polarity</td></tr><tr><td rowspan=1 colspan=1>Receive buffer accessible in half-word</td><td rowspan=1 colspan=2>Receive buffer accessible in half-word and words</td></tr><tr><td rowspan=1 colspan=1>Data are right aligned into thereceive buffer</td><td rowspan=1 colspan=2>Various data arrangement available into the receive buffer</td></tr><tr><td rowspan=1 colspan=1>Error flags signaling for underrun,overrun and frame error</td><td rowspan=1 colspan=2>Error flags signaling for underrun, overrun and frame error</td></tr><tr><td rowspan=3 colspan=1>NA</td><td rowspan=1 colspan=2>Improved reliability: automatic resynchronization to the frame sync incase of frame error</td></tr><tr><td rowspan=1 colspan=2>Improved reliability: re-alignement f left and right samples in caseounderrun or overrun situation</td></tr><tr><td rowspan=1 colspan=2>MSb/LSb possible in the serial data interface</td></tr><tr><td rowspan=1 colspan=1>16 or 32 bits channel length inmaster</td><td rowspan=1 colspan=2>16 or 32 bits channel length in master</td></tr><tr><td rowspan=1 colspan=1>16 or 32 bits channel length inslave</td><td rowspan=1 colspan=2>Any channel length in slave</td></tr><tr><td rowspan=1 colspan=1>NA</td><td rowspan=1 colspan=2>Embedded RX and TX FIFOs</td></tr><tr><td rowspan=1 colspan=1>DMA capabilities (16-bit wide)</td><td rowspan=1 colspan=2>DMA capabilities (16-bit and 32-bit wide)</td></tr></table>

# 13 Flexible memory controller (FMC)

The table below presents the FMC differences between STM32F7 Series, STM32H74x/75x, STM32H72x/73x and STM32H7A3/7Bx devices.

Table 26. FMC differences between STM32F7 Series devices, STM32H74x/75x, STM32H72x/73x and STM32H7A3/7Bx devices   
Figure 11. FMC bank address mapping on STM32H7A3/7Bx and STM32H72x/73x devices   

<table><tr><td rowspan=1 colspan=1>FMC</td><td rowspan=1 colspan=1>STM32F7 Series</td><td rowspan=1 colspan=1>STM32H74x/75x, STM32H72x/73x and STM32H7A3/7Bx</td></tr><tr><td rowspan=1 colspan=1>Mapping</td><td rowspan=1 colspan=1>AHB</td><td rowspan=1 colspan=1>AXI</td></tr><tr><td rowspan=1 colspan=1>Clock</td><td rowspan=1 colspan=1>Single clock domain</td><td rowspan=1 colspan=1>Dual clock domain with dedicated kernel clock for peripherals independent fromAXI clock</td></tr><tr><td rowspan=1 colspan=1>Bankremap</td><td rowspan=1 colspan=1>SYSCFG_MEMRMPregisterFMC bank mapping canbe configured by softwarethrough the SWP_FMC[1:0]bits.</td><td rowspan=1 colspan=1>FMC_BCR1 registerFMC bank mapping can be configured by software through the BMAP[1:0] bits.See Figure 11 and Figure 12.</td></tr><tr><td rowspan=1 colspan=1>Features</td><td rowspan=1 colspan=1>NA</td><td rowspan=1 colspan=1>FMCEN bit: FMC controller Enable bit added in the FMC_BCR1 register.To modify some parameters while FMC is enabled follow the below sequence:First disable the FMC controller to prevent any further accesses to anymemory controller during register modification.2.   Update all required configurations.3.   Enable the FMC controller again.When the SDRAM controller is used, if the SDCLK clock ratio or refresh rate hasto be modified after initialization phase, the following procedure must be followed.1.   Put the SDRAM device in Self-refresh mode.2.   Disable the FMC controller by resetting the FMCEN bit in the FMC_BCR1register.3.   Update the required parameters.4.   Enable the FMC controller once all parameters are updated.5.   Then, send the clock configuration enable command to exit Self-fresh mode.</td></tr></table>

0xDFFF FFFF 0xDFFF FFFF SDRAM bank2 SDRAM bank2 256 Mbytes 256 Mbytes   
0xD000 0000 0xD000 0000   
0xCFFF FFFF SDRAM bank1 0xCFFF FFFF NOR/PSRAM bank 256 Mbytes 256 Mbytes   
OxC000 0000 0xC000 0000   
0x9FFF FFFF Bank4 0x9FFF FFFF Bank4 Reserved Reserved   
0x9000 0000 0x9000 0000   
0x8FFF FFFF NAND bank 0x8FFF FFFF NAND bank 256 Mbytes 256 Mbytes   
0x8000 0000 0x8000 0000   
0x7FFF FFFF Bank2 0x7FFF FFFF Bank2 Reserved Reserved   
0x7000 0000 0x7000 0000   
0x6FFF FFFF NOR/PSRAM bank 0x6FFF FFFF SDRAM bank1   
0x6000 0000 256 Mbytes 0x6000 0000 256 Mbytes NOR/PSRAM and Default mapping SDRAM banks swapped Default mapping Swap Reserved

![](images/f615d769a36a08a4132760600c4def612c24799d87158ff31fb82701d7996ca1.jpg)  
Figure 12. FMC bank address mapping on STM32H74x/75x devices

# 14 Analog-to-digital converters (ADC)

The following table presents the differences between the ADC peripheral of the STM32F7 Series, STM32H74xl 75x, STM32H72x/73x and STM32H7A3/7Bx devices.

Table 27. ADC differences between STM32F7 Series,STM32H74x/75x, STM32H72x/73x and STM32H7A3/7Bx devices   

<table><tr><td rowspan=1 colspan=1>ADC</td><td rowspan=1 colspan=1>STM32F7Series</td><td rowspan=1 colspan=1>STM32H74x/75x</td><td rowspan=1 colspan=1>STM32H72x/73x</td><td rowspan=1 colspan=1>STM32H7A3/7Bx</td></tr><tr><td rowspan=1 colspan=1>Instances</td><td rowspan=1 colspan=1>x3</td><td rowspan=1 colspan=1>x3</td><td rowspan=1 colspan=1></td><td rowspan=1 colspan=1>x2</td></tr><tr><td rowspan=1 colspan=1>Clock</td><td rowspan=1 colspan=1>Single clockdomain</td><td rowspan=1 colspan=3>Dual clock domain with dedicated kernel clock for peripherals independent from CLK or HCLK</td></tr><tr><td rowspan=1 colspan=1>Number ofchannels</td><td rowspan=1 colspan=1>Up to 24channels</td><td rowspan=1 colspan=3>Up to 20 channels</td></tr><tr><td rowspan=1 colspan=1>Resolution</td><td rowspan=1 colspan=1>12, 10, 8 or6-bit</td><td rowspan=1 colspan=1>16, 14, 12, 10 or 8-bit</td><td rowspan=1 colspan=1>114, 12, 10 or 8-bit forADC1 and ADC212, 10, 8 or 6-bit for ADC3</td><td rowspan=1 colspan=1>16, 14, 12, 10 or 8-bit</td></tr><tr><td rowspan=1 colspan=1>Conversionmodes</td><td rowspan=1 colspan=4>SingleContinuousScanDiscontinuous•    Dual and triple mode</td></tr><tr><td rowspan=1 colspan=1>DMA</td><td rowspan=1 colspan=4>Yes</td></tr><tr><td rowspan=2 colspan=1>Newfeatures</td><td rowspan=1 colspan=1>NA</td><td rowspan=1 colspan=3>Input voltage reference from VREF+ pin or internal VREFBUF referenceADC conversion time is independent from the AHB bus clock frequencySelf-calibration (both offset and the linearity)Low-power featuresThree analog watchdogs per ADCInternal dedicated channels: the internal DAC1 channel 1 and channel 2 are connected to ADC2Oversampler:32-bit data registerOversampling ratio adjustable from 2 to 1024Programmable data right and left shiftData can be routed to DFSDM for post processing</td></tr><tr><td rowspan=1 colspan=1>NA</td><td rowspan=1 colspan=1>All the internal references(VBAT, VREFINT,VSENSE) are connectedo ADC3</td><td rowspan=1 colspan=1>Internal references VBAT,VREFINT are connected toADC3 and ADC2VSENSE is connected toADC3</td><td rowspan=1 colspan=1>All the internal references (VBAT,VREFINT, VSENSE) are connectedto ADC2The internal DAC2 channel 1 isconnected to ADC2One additional DAC forSTM32H7A3/7B0/7B3 devices</td></tr></table>

Tho bl ent cteaeguhae a between STM32F7 Series, STM32H74x/75x, STM32H72x/73x and STM32H7A3/7Bx devices.

Table 28. External trigger for regular channel differences between STM32F7 Series, STM32H74x/75x, STM32H72x/73x and STM32H7A3/7Bx devices   

<table><tr><td rowspan=2 colspan=1>Type</td><td rowspan=2 colspan=1>EXTSEL[3:0]STM32F7Series devices</td><td rowspan=2 colspan=1>EXTSEL[4:0]STM32H7 Series</td><td rowspan=1 colspan=5>ADC</td></tr><tr><td rowspan=1 colspan=3>STM32F7Series</td><td rowspan=1 colspan=1>STM32H74x/75x</td><td rowspan=1 colspan=1>STM32H7A3/7Bx</td></tr><tr><td rowspan=24 colspan=2>00000001001000110100010101100111100020        10011010101111001101NA1111NA</td><td rowspan=1 colspan=1>0000</td><td rowspan=1 colspan=3>00000</td><td rowspan=1 colspan=2>TIM1_CC1 event</td></tr><tr><td rowspan=1 colspan=1>0001</td><td rowspan=1 colspan=1>00001</td><td rowspan=1 colspan=5>TIM1_CC2 event</td></tr><tr><td rowspan=1 colspan=1>0010</td><td rowspan=1 colspan=1>00010</td><td rowspan=1 colspan=5>TIM1_CC3 event</td></tr><tr><td rowspan=1 colspan=1>0011</td><td rowspan=1 colspan=1>00011</td><td rowspan=1 colspan=5>TIM2_CC2 event</td></tr><tr><td rowspan=1 colspan=1>0100</td><td rowspan=1 colspan=1>00100</td><td rowspan=1 colspan=3>TIM5_TRGOevent</td><td rowspan=1 colspan=2>TIM3_TRGO event</td></tr><tr><td rowspan=1 colspan=1>0101</td><td rowspan=1 colspan=1>00101</td><td rowspan=1 colspan=5>TIM4_CC4 event</td></tr><tr><td rowspan=1 colspan=1>0110</td><td rowspan=1 colspan=1>00110</td><td rowspan=1 colspan=3>TIM3_CC4</td><td rowspan=1 colspan=2>EXTI line 11</td></tr><tr><td rowspan=1 colspan=1>0111</td><td rowspan=1 colspan=1>00111</td><td rowspan=1 colspan=5>TIM8_TRGO event</td></tr><tr><td rowspan=1 colspan=1>1000</td><td rowspan=1 colspan=1>01000</td><td rowspan=1 colspan=5>TIM8_TRGO(2) event</td></tr><tr><td rowspan=1 colspan=1>1001</td><td rowspan=1 colspan=1>01001</td><td rowspan=1 colspan=5>TIM1_TRGO event</td></tr><tr><td rowspan=1 colspan=1>1010</td><td rowspan=1 colspan=1>01010</td><td rowspan=1 colspan=5>TIM1_TRGO(2) event</td></tr><tr><td rowspan=1 colspan=1>1011</td><td rowspan=1 colspan=1>01011</td><td rowspan=1 colspan=5>TIM2_TRGO event</td></tr><tr><td rowspan=1 colspan=1>1100</td><td rowspan=1 colspan=1>01100</td><td rowspan=1 colspan=5>TIM4_TRGO event</td></tr><tr><td rowspan=1 colspan=1>1101</td><td rowspan=1 colspan=1>01101</td><td rowspan=1 colspan=5>TIM6_TRGO event</td></tr><tr><td rowspan=1 colspan=1>NA</td><td rowspan=1 colspan=1>01110</td><td rowspan=1 colspan=3>EXTI line11</td><td rowspan=1 colspan=2>TIM15_TRGO event</td></tr><tr><td rowspan=1 colspan=1>1111</td><td rowspan=1 colspan=1>01111</td><td rowspan=2 colspan=3></td><td rowspan=1 colspan=2>TIM3_CC4 event</td></tr><tr><td rowspan=1 colspan=1>10000</td><td rowspan=1 colspan=2></td><td rowspan=1 colspan=1>HRTIM1_ADCTRG1 event</td><td rowspan=1 colspan=1>Reserved</td></tr><tr><td rowspan=2 colspan=1>10001</td><td rowspan=2 colspan=2></td><td rowspan=1 colspan=2></td><td rowspan=2 colspan=1></td><td rowspan=2 colspan=1>HRTIM1_ADCTRG3 event</td><td rowspan=2 colspan=1>Reserved</td></tr><tr><td rowspan=1 colspan=2></td></tr><tr><td rowspan=1 colspan=1>10010</td><td rowspan=5 colspan=3>NA</td><td rowspan=1 colspan=2></td><td rowspan=1 colspan=2>LPTIM1_OUT event</td></tr><tr><td rowspan=1 colspan=1>10011</td><td rowspan=1 colspan=2>LPTIM2_OUT event</td></tr><tr><td rowspan=1 colspan=1>10100</td><td rowspan=1 colspan=2>LPTIM3_OUT event</td></tr><tr><td rowspan=1 colspan=1>10101</td><td rowspan=2 colspan=1>NA</td><td rowspan=2 colspan=1>NA</td></tr><tr><td rowspan=1 colspan=1>10110</td><td rowspan=1 colspan=1>TIM24_TRGOvent</td></tr></table>

Table 29. External trigger for injected channel differences between STM32F7 Series, STM32H74x/75x, STM32H72x/73x and STM32H7A3/7Bx devices   

<table><tr><td rowspan=2 colspan=1>Type</td><td rowspan=2 colspan=1>JEXTSEL[3:0]STM32F7Series</td><td rowspan=2 colspan=1>JEXTSEL[4:0]STM32H7 Series</td><td rowspan=1 colspan=1>ADC</td></tr><tr><td rowspan=1 colspan=1>STM32H7A3/7Bx</td></tr><tr><td rowspan=23 colspan=1>20</td><td rowspan=1 colspan=1>0000</td><td rowspan=1 colspan=1>00000</td><td rowspan=1 colspan=1>TIM1_TRGO event</td></tr><tr><td rowspan=1 colspan=1>0001</td><td rowspan=1 colspan=1>00001</td><td rowspan=1 colspan=1>TIM1_CC4 event</td></tr><tr><td rowspan=1 colspan=1>0010</td><td rowspan=1 colspan=1>00010</td><td rowspan=1 colspan=1>TIM2_TRGO event</td></tr><tr><td rowspan=1 colspan=1>0011</td><td rowspan=1 colspan=1>00011</td><td rowspan=1 colspan=1>TIM2_CC1 event</td></tr><tr><td rowspan=1 colspan=1>0100</td><td rowspan=1 colspan=1>00100</td><td rowspan=1 colspan=1>TIM3_CC4 event</td></tr><tr><td rowspan=1 colspan=1>0101</td><td rowspan=1 colspan=1>00101</td><td rowspan=1 colspan=1>TIM4_TRGO event</td></tr><tr><td rowspan=1 colspan=1>NA</td><td rowspan=1 colspan=1>00110</td><td rowspan=1 colspan=1>EXTI line 15</td></tr><tr><td rowspan=1 colspan=1>0111</td><td rowspan=1 colspan=1>00111</td><td rowspan=1 colspan=1>TIM8_ CC4 event</td></tr><tr><td rowspan=1 colspan=1>1000</td><td rowspan=1 colspan=1>01000</td><td rowspan=1 colspan=1>TIM1_TRGO(2) event</td></tr><tr><td rowspan=1 colspan=1>1001</td><td rowspan=1 colspan=1>01001</td><td rowspan=1 colspan=1>TIM8_TRGO event</td></tr><tr><td rowspan=1 colspan=1>1010</td><td rowspan=1 colspan=1>01010</td><td rowspan=1 colspan=1>TIM8_TRGO(2) event</td></tr><tr><td rowspan=1 colspan=1>1011</td><td rowspan=1 colspan=1>01011</td><td rowspan=1 colspan=1>TIM3_CC3 event</td></tr><tr><td rowspan=1 colspan=1>1100</td><td rowspan=1 colspan=1>01100</td><td rowspan=1 colspan=1>TIM3_TRGO event</td></tr><tr><td rowspan=1 colspan=1>1101</td><td rowspan=1 colspan=1>01101</td><td rowspan=1 colspan=1>TIM3_CC1 event</td></tr><tr><td rowspan=1 colspan=1>1110</td><td rowspan=1 colspan=1>01110</td><td rowspan=1 colspan=1>TIM6_TRGO event</td></tr><tr><td rowspan=8 colspan=1>NA</td><td rowspan=1 colspan=1>01111</td><td rowspan=1 colspan=1>TIM15_TRGO event</td></tr><tr><td rowspan=1 colspan=1>10000</td><td rowspan=1 colspan=1>Reserved</td></tr><tr><td rowspan=1 colspan=1>10001</td><td rowspan=1 colspan=1>Reserved</td></tr><tr><td rowspan=1 colspan=1>10010</td><td rowspan=1 colspan=1>LPTIM1_OUT event</td></tr><tr><td rowspan=1 colspan=1>10011</td><td rowspan=1 colspan=1>LPTIM2_OUT event</td></tr><tr><td rowspan=1 colspan=1>10100</td><td rowspan=1 colspan=1>LPTIM3_OUT event</td></tr><tr><td rowspan=1 colspan=1>10101</td><td rowspan=2 colspan=1>NA</td></tr><tr><td rowspan=1 colspan=1>10110</td><td rowspan=1 colspan=1>TIM24_TRGOevent</td></tr></table>

# 15 Digital-to-analog converter (DAC)

The STM32H74x/75x, STM32H72x/73x and STM32H7A3/7Bx devices implement some enhanced DAC compared to the STM32F7 Series devices. Refer to the table below for the main DAC diferences between them.

Table 30. DAC differences between STM32F7 Series, STM32H74x/75x, STM32H72x/73x and STM32H7A3/7Bx devices   

<table><tr><td rowspan=1 colspan=1>DAC</td><td rowspan=1 colspan=1>STM32F7 Series</td><td rowspan=1 colspan=1>STM32H74x/75x</td><td rowspan=1 colspan=1>STM32H72x/73x</td><td rowspan=1 colspan=1>STM32H7A3/7Bx</td></tr><tr><td rowspan=1 colspan=1>Instance</td><td rowspan=1 colspan=1>1xOne dual channel</td><td rowspan=1 colspan=2>1xOne dual channel</td><td rowspan=1 colspan=1>2xOne dual channelOne single channel</td></tr><tr><td rowspan=1 colspan=1>Clock</td><td rowspan=1 colspan=1>Single clock domain</td><td rowspan=1 colspan=3>Single clock domain (APB)LSI is used for sample and hold mode</td></tr><tr><td rowspan=2 colspan=1>Features</td><td rowspan=1 colspan=1>Input voltage reference, VREF+</td><td rowspan=1 colspan=3>Input voltage reference from VREF+ pin or internal VREFBUF reference</td></tr><tr><td rowspan=1 colspan=1>NA</td><td rowspan=1 colspan=3>Buffer offset calibrationDAC output connection to on chip peripheralsSample and hold mode for low power operation in Stop mode</td></tr></table>

Table 31. DAC1 trigger selection differences between STM32F7 Series, STM32H74x/75x, STM32H72x/73x and STM32H7A3/7Bx devices   

<table><tr><td rowspan=18 colspan=1>Type20</td><td rowspan=2 colspan=1>TSEL[2:0]STM32F7Series</td><td rowspan=2 colspan=1>TSEL[3:0]STM32H7 Series</td><td rowspan=1 colspan=4>DAC1</td></tr><tr><td rowspan=1 colspan=1>STM32F7Series</td><td rowspan=1 colspan=1>STM32H74x/75x</td><td rowspan=1 colspan=1>STM32H72x/73X</td><td rowspan=1 colspan=1>STM32H7A3/7Bx</td></tr><tr><td rowspan=1 colspan=1>000</td><td rowspan=1 colspan=1>0000</td><td rowspan=1 colspan=1>TIM6_TRGO</td><td rowspan=1 colspan=3>SWTRIG</td></tr><tr><td rowspan=1 colspan=1>001</td><td rowspan=1 colspan=1>0001</td><td rowspan=1 colspan=1>TIM8_TRGO</td><td rowspan=1 colspan=3>TIM1_TRGO</td></tr><tr><td rowspan=1 colspan=1>010</td><td rowspan=1 colspan=1>0010</td><td rowspan=1 colspan=1>TIM7_TRGO</td><td rowspan=1 colspan=2>TIM2_TRGO</td><td rowspan=1 colspan=1></td></tr><tr><td rowspan=1 colspan=1>011</td><td rowspan=1 colspan=1>0011</td><td rowspan=1 colspan=1>TIM5_TRGO</td><td rowspan=1 colspan=3>TIM4_TRGO</td></tr><tr><td rowspan=1 colspan=1>100</td><td rowspan=1 colspan=1>0100</td><td rowspan=1 colspan=1>TIM2_TRGO</td><td rowspan=1 colspan=2>TIM5_TRGO</td><td rowspan=1 colspan=1>TIM3_TRGO event</td></tr><tr><td rowspan=1 colspan=1>101</td><td rowspan=1 colspan=1>0101</td><td rowspan=1 colspan=1>TIM4_TRGO</td><td rowspan=1 colspan=2>TIM6_TRGO</td><td rowspan=1 colspan=1></td></tr><tr><td rowspan=1 colspan=1>110</td><td rowspan=1 colspan=1>0110</td><td rowspan=1 colspan=1>EXTI9</td><td rowspan=1 colspan=2>TIM7_TRGO</td><td rowspan=1 colspan=1>EXTI line 11</td></tr><tr><td rowspan=1 colspan=1>111</td><td rowspan=1 colspan=1>0111</td><td rowspan=1 colspan=1>SWTRIG</td><td rowspan=1 colspan=3>TIM8_TRGO</td></tr><tr><td rowspan=8 colspan=1>NA</td><td rowspan=1 colspan=1>1000</td><td rowspan=1 colspan=1></td><td rowspan=1 colspan=3>TIM15_TRGO</td></tr><tr><td rowspan=1 colspan=1>1001</td><td rowspan=1 colspan=1></td><td rowspan=1 colspan=1>HRTIM1_DACTRG1</td><td rowspan=1 colspan=2>Reserved</td></tr><tr><td rowspan=1 colspan=1>1010</td><td rowspan=2 colspan=1></td><td rowspan=1 colspan=1>HRTIM1_DACTRG2</td><td rowspan=1 colspan=2>Reserved</td></tr><tr><td rowspan=1 colspan=1>1011</td><td rowspan=5 colspan=1>NA</td><td rowspan=1 colspan=3>LPTIM1_OUT</td></tr><tr><td rowspan=1 colspan=1>1100</td><td rowspan=1 colspan=3>LPTIM2_OUT</td></tr><tr><td rowspan=1 colspan=1>1101</td><td rowspan=1 colspan=3>EXTI9</td></tr><tr><td rowspan=1 colspan=1>1110</td><td rowspan=1 colspan=1>Reserved</td><td rowspan=1 colspan=1>TIM23_TRGOevent</td><td rowspan=1 colspan=1>LPTIM2_OUT</td></tr><tr><td rowspan=1 colspan=1>1111</td><td rowspan=1 colspan=1>Reserved</td><td rowspan=1 colspan=1>TIM24_TRGOeent</td><td rowspan=1 colspan=1>Reserved</td></tr></table>

Table 32. DAC2 trigger selection new for STM32H7A3/7Bx devices   

<table><tr><td rowspan=2 colspan=1>Type</td><td rowspan=2 colspan=1>TSEL[3:0]</td><td rowspan=1 colspan=1>DAC2</td></tr><tr><td rowspan=1 colspan=1>STM32H7A3/7B0/7B3 devices</td></tr><tr><td rowspan=16 colspan=1>20</td><td rowspan=1 colspan=1>0000</td><td rowspan=1 colspan=1>SWTRIG</td></tr><tr><td rowspan=1 colspan=1>0001</td><td rowspan=1 colspan=1>TIM1_TRGO</td></tr><tr><td rowspan=1 colspan=1>0010</td><td rowspan=1 colspan=1>TIM2_TRGO</td></tr><tr><td rowspan=1 colspan=1>0011</td><td rowspan=1 colspan=1>TIM4_TRGO</td></tr><tr><td rowspan=1 colspan=1>0100</td><td rowspan=1 colspan=1>TIM5_TRGO</td></tr><tr><td rowspan=1 colspan=1>0101</td><td rowspan=1 colspan=1>TIM6_TRGO</td></tr><tr><td rowspan=1 colspan=1>0110</td><td rowspan=1 colspan=1>TIM7_TRGO</td></tr><tr><td rowspan=1 colspan=1>0111</td><td rowspan=1 colspan=1>TIM8_TRGO</td></tr><tr><td rowspan=1 colspan=1>1000</td><td rowspan=1 colspan=1>TIM15_TRGO</td></tr><tr><td rowspan=1 colspan=1>1001</td><td rowspan=1 colspan=1>Reserved</td></tr><tr><td rowspan=1 colspan=1>1010</td><td rowspan=1 colspan=1>Reserved</td></tr><tr><td rowspan=1 colspan=1>1011</td><td rowspan=1 colspan=1>LPTIM1_OUT</td></tr><tr><td rowspan=1 colspan=1>1100</td><td rowspan=1 colspan=1>LPTIM2_OUT</td></tr><tr><td rowspan=1 colspan=1>1101</td><td rowspan=1 colspan=1>EXTI9</td></tr><tr><td rowspan=1 colspan=1>1110</td><td rowspan=1 colspan=1>LPTIM3_OUT</td></tr><tr><td rowspan=1 colspan=1>1111</td><td rowspan=1 colspan=1>Reserved</td></tr></table>

# 16 USB on-the-go (USB OTG)

The STM32H72x/73x and STM32H7A3/7Bx devices embed one USB OTG HS/FS instance while the STM32H74x/75x devices and STM32F7 Series devices embed one USB OTG HS/FS instance and one USB OTG FS instance.

The table below summarizes the difference of USB OTG between STM32F7 Series, STM32H74x/75x, STM32H72x/73x and STM32H7A3/7Bx devices.

Table 33. USB OTG differences between STM32F7 Series, STM32H74x/75x, STM32H72x/73x and STM32H7A3/7Bx devices   

<table><tr><td rowspan=1 colspan=1>USB OTG</td><td rowspan=1 colspan=2>STM32F7 Series</td><td rowspan=1 colspan=1>STM32H74x/75x</td><td rowspan=1 colspan=1>STM32H72x/73xandSTM32H7A3/7Bx</td></tr><tr><td rowspan=1 colspan=1>Instance</td><td rowspan=1 colspan=1>FS</td><td rowspan=1 colspan=1>HS</td><td rowspan=1 colspan=1>x2 HS(1)</td><td rowspan=1 colspan=1>HS</td></tr><tr><td rowspan=1 colspan=1>Device bidirectional endpoints (includingEP0)</td><td rowspan=1 colspan=1>6</td><td rowspan=1 colspan=1>9</td><td rowspan=1 colspan=2>9</td></tr><tr><td rowspan=1 colspan=1>Host mode channels</td><td rowspan=1 colspan=1>12</td><td rowspan=1 colspan=1>16</td><td rowspan=1 colspan=2>16</td></tr><tr><td rowspan=1 colspan=1>Size of dedicated SRAM</td><td rowspan=1 colspan=1>1.2 Kbytes</td><td rowspan=1 colspan=1>4 Kbytes</td><td rowspan=1 colspan=2>4 Kbytes</td></tr><tr><td rowspan=1 colspan=1>USB 2.0 link power management (LPM)support</td><td rowspan=1 colspan=4>Yes</td></tr><tr><td rowspan=1 colspan=1>OTG revision supported</td><td rowspan=1 colspan=2>1.3, 2.0</td><td rowspan=1 colspan=2>2.0</td></tr><tr><td rowspan=1 colspan=1>Attach detection protocol (ADP) support</td><td rowspan=1 colspan=4>Not supported</td></tr><tr><td rowspan=1 colspan=1>Battery Charging Detection (BCD)support</td><td rowspan=1 colspan=2>No</td><td rowspan=1 colspan=2>Yes</td></tr><tr><td rowspan=1 colspan=1>ULPI available to primary IOs via,muxing</td><td rowspan=1 colspan=1></td><td rowspan=1 colspan=1>x1</td><td rowspan=1 colspan=1>x1</td><td rowspan=1 colspan=1>X1</td></tr><tr><td rowspan=1 colspan=1>Integrated PHY</td><td rowspan=1 colspan=1>x1 FS</td><td rowspan=1 colspan=1>x1 FS</td><td rowspan=1 colspan=1>x1 FS</td><td rowspan=1 colspan=1>x1 FS</td></tr><tr><td rowspan=1 colspan=1>DMA availability</td><td rowspan=1 colspan=4>Yes</td></tr></table>

OTGSn OTGHS2 ay   HSnlye bLP which willallow a High Speed operation using an external HS transceiver.

# 17 Ethernet (ETH)

The STM32H74x/75x and STM32H72x/73x devices implement several new features on the Ethernet compared to the STM32F7 Series devices.

There is no Ethernet embedded in STM32H7A3/7Bx devices.

Table 34. Ethernet differences between STM32F7 and STM32H7 devices   

<table><tr><td rowspan=1 colspan=1>Ethernet</td><td rowspan=1 colspan=1>STM32F7 Series</td><td rowspan=1 colspan=1>STM32H74x/75x and STM32H72x/73xlines</td></tr><tr><td rowspan=1 colspan=1>Operation modes and PHY support</td><td rowspan=1 colspan=2>10/100 Mbps data rateFull-duplex and half-duplex operationsMIl and RMIl interface to external PHY</td></tr><tr><td rowspan=1 colspan=1>Processing control</td><td rowspan=1 colspan=1>NA</td><td rowspan=1 colspan=1>Multi-layer filtering (Layer 3 and 4, VLANand MAC filtering)Double VLAN support (C-VLAN+ S- VLAN)</td></tr><tr><td rowspan=1 colspan=1>Offload processing</td><td rowspan=1 colspan=1>NA</td><td rowspan=1 colspan=1>Automatic ARP responseTCP segmentation</td></tr><tr><td rowspan=2 colspan=1>Low-power mode</td><td rowspan=1 colspan=2>Remote wakeup packet AMD Magic Packet detections</td></tr><tr><td rowspan=1 colspan=1>NA</td><td rowspan=1 colspan=1>Energy efficient Ethernet (EEE)</td></tr></table>

# 18 Digital filter for sigma delta modulators (DFSDM)

The STM32H7A3/7Bx devices implement several new features on DFSDM compared to STM32H74x/75x, STM32H72x/73x and STM32F7 Series devices with a DFSDM.

For STM32H7A3/7Bx devices, an additional single filter DFSDM has been included in the APB4 that can run in autonomous mode. The following table shows the DFSDM differences between STM32F7 Series, STM32H74x/ 75x, STM32H72x/73x and STM32H7A3/7Bx devices.

Table 35. DFSDM differences between STM32F7 Series, STM32H74x/75x, STM32H72x/73x and STM32H7A3/7Bx devices   

<table><tr><td rowspan=1 colspan=1>DFSDM</td><td rowspan=1 colspan=1>STM32F7 Series</td><td rowspan=1 colspan=1>STM32H74x/75x and STM32H72x/73x</td><td rowspan=1 colspan=2>STM32H7A3/7Bx</td></tr><tr><td rowspan=1 colspan=1>Instance</td><td rowspan=1 colspan=1>DFSDM1</td><td rowspan=1 colspan=1>DFSDM1</td><td rowspan=1 colspan=1>DFSDM1</td><td rowspan=1 colspan=1>DFSDM2</td></tr><tr><td rowspan=1 colspan=1>Number of channels</td><td rowspan=1 colspan=2>8</td><td rowspan=1 colspan=1>8</td><td rowspan=1 colspan=1>2</td></tr><tr><td rowspan=1 colspan=1>Number of filters</td><td rowspan=1 colspan=2>4</td><td rowspan=1 colspan=1>8</td><td rowspan=1 colspan=1>1</td></tr><tr><td rowspan=1 colspan=1>Input from ADC</td><td rowspan=1 colspan=1>NA</td><td rowspan=1 colspan=1>Yes</td><td rowspan=1 colspan=1>Yes</td><td rowspan=1 colspan=1>NA</td></tr><tr><td rowspan=1 colspan=1>Supported trigger sources</td><td rowspan=1 colspan=1>12</td><td rowspan=1 colspan=2>16</td><td rowspan=1 colspan=1>7</td></tr></table>

The table below presents the DFSDM internal signals differences between STM32F7 Series, STM32H74x/75x, STM32H72x/73x and STM32H7A3/7Bx devices.

# Table 36. DFSDM internal signal differences between STM32F7 Series, STM32H74x/75x, STM32H72x/73x and STM32H7A3/7Bx devices

<table><tr><td rowspan=1 colspan=1>Name</td><td rowspan=1 colspan=1>STM32F7 Series</td><td rowspan=1 colspan=1>STM32H74x/75x andSTM32H72x/73x</td><td rowspan=1 colspan=2>STM32H7A3/7Bx</td></tr><tr><td rowspan=1 colspan=1>Instance</td><td rowspan=1 colspan=1>DFSDM1</td><td rowspan=1 colspan=1>DFSDM1</td><td rowspan=1 colspan=1>DFSDM1</td><td rowspan=1 colspan=1>DFSDM2</td></tr><tr><td rowspan=1 colspan=1>Internal/ externaltrigger signal</td><td rowspan=1 colspan=4>Refer to the following tables for DFSDM triggers signals connections</td></tr><tr><td rowspan=1 colspan=1>break signaloutput</td><td rowspan=1 colspan=4>Refer to the following tables for DFSDM break signal connections</td></tr><tr><td rowspan=1 colspan=1>DMA requestsignal</td><td rowspan=1 colspan=2>x4 DMA request from DFSDM_FLTx (x =0..3)</td><td rowspan=1 colspan=1>x8 DMA request fromDFSDM_FLTx(x =0..7)</td><td rowspan=1 colspan=1>x1 DMA request</td></tr><tr><td rowspan=1 colspan=1>Interrupt requestsignal</td><td rowspan=1 colspan=2>x4 interrupt request from each DFSDM_FLTx(x=0.3)</td><td rowspan=1 colspan=1>x8 interrupt request from eachDFSDM_FLTx (x=0..7)</td><td rowspan=1 colspan=1>x1 interrupt request</td></tr><tr><td rowspan=1 colspan=1>ADC input data</td><td rowspan=1 colspan=1>NA</td><td rowspan=1 colspan=2>dfsdm_dat_adc[15:0]</td><td rowspan=1 colspan=1>NA</td></tr></table>

This table describes the DFSDM triggers connection differences between STM32F7 Series, STM32H74x/75x, STM32H72x/73x and STM32H7A3/7Bx devices.

Table 37. DFSDM trigger connection differences between STM32F7 Series, STM32H74x/75x, STM32H72x/73x and STM32H7A3/7Bx devices   

<table><tr><td rowspan=1 colspan=1>Trigger name</td><td rowspan=1 colspan=1>STM32F7 Series</td><td rowspan=1 colspan=1>STM32H74x/75x</td><td rowspan=1 colspan=1>STM32H72x/73x</td><td rowspan=1 colspan=2>STM32H7A3/7Bx</td></tr><tr><td rowspan=1 colspan=1>Instance</td><td rowspan=1 colspan=1>DFSDM1</td><td rowspan=1 colspan=1>DFSDM1</td><td rowspan=1 colspan=1>DFSDM1</td><td rowspan=1 colspan=1>DFSDM1</td><td rowspan=1 colspan=1>DFSDM2</td></tr><tr><td rowspan=1 colspan=1>DFSDM_JTRG[0]</td><td rowspan=1 colspan=4>TIM1_TRGO</td><td rowspan=11 colspan=1>Reserved</td></tr><tr><td rowspan=1 colspan=1>DFSDM_JTRG[1]</td><td rowspan=1 colspan=4>TIM1_TRGO2</td></tr><tr><td rowspan=1 colspan=1>DFSDM_JTRG[2]</td><td rowspan=1 colspan=4>TIM8_TRGO</td></tr><tr><td rowspan=1 colspan=1>DFSDM_JTRG[3]</td><td rowspan=1 colspan=4>TIM8_TRGO2</td></tr><tr><td rowspan=1 colspan=1>DFSDM_JTRG[4]</td><td rowspan=1 colspan=4>TIM3_TRGO</td></tr><tr><td rowspan=1 colspan=1>DFSDM_JTRG[5]</td><td rowspan=1 colspan=4>TIM4_TRGO</td></tr><tr><td rowspan=1 colspan=1>DFSDM_JTRG[6]</td><td rowspan=1 colspan=1>TIM10_OC1</td><td rowspan=1 colspan=3>TIM16_OC1</td></tr><tr><td rowspan=1 colspan=1>DFSDM_JTRG[7]</td><td rowspan=1 colspan=4>TIM6_TRGO</td></tr><tr><td rowspan=1 colspan=1>DFSDM_JTRG[8]</td><td rowspan=1 colspan=4>TIM7_TRGO</td></tr><tr><td rowspan=1 colspan=1>DFSDM_JTRG[9]</td><td rowspan=1 colspan=1>Reserved</td><td rowspan=1 colspan=1>HRTIM1_ADCTRG1</td><td rowspan=1 colspan=2>Reserved</td></tr><tr><td rowspan=1 colspan=1>DFSDM_JTRG[10]</td><td rowspan=1 colspan=1>Reserved</td><td rowspan=1 colspan=1>HRTIM1_ADCTRG3</td><td rowspan=1 colspan=2>Reserved</td></tr><tr><td rowspan=1 colspan=1>DFSDM_JTRG[11]</td><td rowspan=1 colspan=2>Reserved</td><td rowspan=1 colspan=1>TIM23_TRGO</td><td rowspan=1 colspan=2>Reserved</td></tr><tr><td rowspan=1 colspan=1>DFSDM_JTRG[12]</td><td rowspan=1 colspan=2>Reserved</td><td rowspan=1 colspan=1>TIM24_TRGO</td><td rowspan=1 colspan=2>Reserved</td></tr><tr><td rowspan=1 colspan=1>DFSDM_JTRG[13:23]</td><td rowspan=1 colspan=5>Reserved</td></tr><tr><td rowspan=1 colspan=1>DFSDM_JTRG[24]</td><td rowspan=1 colspan=5>EXTI11</td></tr><tr><td rowspan=1 colspan=1>DFSDM_JTRG[25]</td><td rowspan=1 colspan=5>EXTI15</td></tr><tr><td rowspan=1 colspan=1>DFSDM_JTRG[26]</td><td rowspan=1 colspan=5>LPTIMER1</td></tr><tr><td rowspan=1 colspan=1>DFSDM_JTRG[27]</td><td rowspan=1 colspan=1>Reserved</td><td rowspan=1 colspan=4>LPTIMER2</td></tr><tr><td rowspan=1 colspan=1>DFSDM_JTRG[28]</td><td rowspan=1 colspan=1>Reserved</td><td rowspan=1 colspan=4>LPTIMER3</td></tr><tr><td rowspan=1 colspan=1>DFSDM_JTRG[29]</td><td rowspan=1 colspan=3>Reserved</td><td rowspan=1 colspan=2>COMP1_OUT</td></tr><tr><td rowspan=1 colspan=1>DFSDM_JTRG[30]</td><td rowspan=1 colspan=3>Reserved</td><td rowspan=1 colspan=2>COMP2_OUT</td></tr><tr><td rowspan=1 colspan=1>DFSDM_JTRG[31]</td><td rowspan=1 colspan=5>Reserved</td></tr></table>

This table presents the DFSDM break connections differences between STM32F7 Series devices, STM32H74x/ 75x, STM32H72x/73x and STM32H7A3/7Bx devices.

Table 38. DFSDM break connection differences between STM32F7 Series, STM32H74x/75x, STM32H72x/73x and STM32H7A3/7Bx devices   

<table><tr><td rowspan=1 colspan=1>Break name</td><td rowspan=1 colspan=1>STM32F7 Series</td><td rowspan=1 colspan=1>STM32H74x/75x</td><td rowspan=1 colspan=1>STM32H72x/73x</td><td rowspan=1 colspan=2>STM32H7A3/7Bx</td></tr><tr><td rowspan=1 colspan=1>Instance</td><td rowspan=1 colspan=1>DFSDM1</td><td rowspan=1 colspan=1>DFSDM1</td><td rowspan=1 colspan=1>DFSDM1</td><td rowspan=1 colspan=1>DFSDM1</td><td rowspan=1 colspan=1>DFSDM2</td></tr><tr><td rowspan=1 colspan=1>DFSDM_BREAK[0]</td><td rowspan=1 colspan=1>TIM1 break</td><td rowspan=1 colspan=1>TIM15 break</td><td rowspan=1 colspan=2>TIM1/TIM15 break</td><td rowspan=1 colspan=1>LPTIM3 ETR</td></tr><tr><td rowspan=1 colspan=1>DFSDM_BREAK[1]</td><td rowspan=1 colspan=1>TIM1 break2</td><td rowspan=1 colspan=1>TIM16 break2</td><td rowspan=1 colspan=2>TIM1_break2 /TIM16 break</td><td rowspan=1 colspan=1></td></tr><tr><td rowspan=1 colspan=1>DFSDM_BREAK[2]</td><td rowspan=1 colspan=1>TIM8 break</td><td rowspan=1 colspan=1>TIM1/TIM17/TIM8 break</td><td rowspan=1 colspan=2>TIM17/TIM8 break</td><td rowspan=1 colspan=1></td></tr><tr><td rowspan=1 colspan=1>DFSDM_BREAK[3]</td><td rowspan=1 colspan=1>TIM8 break2</td><td rowspan=1 colspan=1>TIM1/TIM8 break2</td><td rowspan=1 colspan=2>TIM8 break2</td><td rowspan=1 colspan=1></td></tr></table>

# Revision history

Table 39. Document revision history   

<table><tr><td colspan="1" rowspan="1"></td><td colspan="1" rowspan="1"></td><td colspan="1" rowspan="2">Changes</td></tr><tr><td colspan="1" rowspan="1">Date</td><td colspan="1" rowspan="1">Version</td></tr><tr><td colspan="1" rowspan="1">27-Feb-2019</td><td colspan="1" rowspan="1">1</td><td colspan="1" rowspan="1">Initial release.</td></tr><tr><td colspan="1" rowspan="1">15-Mar-2019</td><td colspan="1" rowspan="1">2</td><td colspan="1" rowspan="1">Updated:Section 2.3 STM32H7A3/7Bx devicesSection 3 System architecture differences between STM32F7 and STM32H7SeriesSection 6.1Section 7 Power (PWR)Section 6.2.2Table 27. ADC differences between STM32F7 Series,STM32H74x/75x,STM32H72x/73x and STM32H7A3/7Bx devices</td></tr><tr><td colspan="1" rowspan="1">31-Jan-2020</td><td colspan="1" rowspan="1">3</td><td colspan="1" rowspan="1">Changed document classification to public.</td></tr><tr><td colspan="1" rowspan="1">25-May-2020</td><td colspan="1" rowspan="1">4</td><td colspan="1" rowspan="1">Updated:Added support for the STM32H7B0 Value line devicesSection 2.3 STM32H7A3/7Bx devicesSection 3Figure 4. STM32H7A3/7Bx devices system architectureFigure 6. System supply configuration on STM32H74x/75x andSTM32H7A3/7Bx devices with SMPSSection 6.1Section 6.2.2Table 13. Flash memory differences between STM32F7 Series, STM32H74x/75x, STM32H72x/73x and STM32H7A3/7Bx devicesTable 17. Different source clock in STM32F7 Series, STM32H74x/75x,STM32H72x/73x and STM32H7A3/7Bx devicesTable 19. General operating conditions for STM32F7 Series, STM32H74x/75x,STM32H72x/73x and STM32H7A3/7Bx devicesAdded:Section 1 General informationFigure 7. System supply configuration on STM32H74x/75x andSTM32H7A3/7Bx devices without SMPS</td></tr><tr><td colspan="1" rowspan="1">12-Oct-2020</td><td colspan="1" rowspan="1">5</td><td colspan="1" rowspan="1">Updated Table 7. STM32F7 Series, STM32H74x/75x, STM32H72x/73x andSTM32H7A3/7Bx devices bootloader communication peripherals</td></tr><tr><td colspan="1" rowspan="1">17-Aug-2022</td><td colspan="1" rowspan="1">6</td><td colspan="1" rowspan="1">Changed Flash into flash in the whole document.Updated:Document title and scope to add STM32H723/733, STM32H725/735,STM32H730 Value, STM32H742, STM32H745/755, and STM32H750 linesCover page to align with new scope and to add Table 1, which indicates all thespecific product lines covered in this document and the generic names that areused from this version on to refer to the identified three groups of STM32H7lines.All chapters in the document are impacted by the new document's scope andupdated in consequence.</td></tr><tr><td>Date</td><td>Version</td><td>Changes</td></tr><tr><td rowspan="3"></td><td rowspan="3"></td><td>Modified: Figure 4. STM32H7A3/7Bx devices system architecture STM32H7A3/B3 I/O pin corresponding to FDCAN1 in Table 7. STM32F7 Series,</td></tr><tr><td colspan="1">STM32H74x/75x, STM32H72x/73x and STM32H7A3/7Bx devices bootloader communication peripherals Table 11. Memory organization and compatibility between STM32F7 Series, STM32H74x/75x, STM32H72x/73x and STM32H7A3/7Bx devices</td></tr><tr><td colspan="1">Table 12. Examples of peripheral address mapping differences between STM32F7 Series,STM32H74x/75x, STM32H72x/73x and STM32H7A3/7Bx devices Added:</td></tr></table>

# Contents

#

# 1 General information

# 2 STM32H7 devices overview

2.1 STM32H74x/75x devices   
2.2 STM32H72x/73x devices overview.   
2.3 STM32H7A3/7Bx devices

# 3 System architecture differences between STM32F7 and STM32H7 Series .. 6

# 4 Hardware migration. 11

4.1 Available packages. 11   
4.2 Pinout compatibility 12   
4.3 System bootloader 16

# Boot mode compatibility 17

# Peripheral migration 18

6.1 STM32 product cross-compatibility . 18

# 6.2 Memory organization 21

6.2.1 RAM size 21   
6.2.2 Memory map and peripherals register boundary addresses 22   
6.2.3 Peripheral register boundary addresses 24

# 3 Flash memory 25

6.4 Nested vectored interrupt controllers (NVIC). 26

.5 Extended interrupt and event controller (EXTI) . 28

6.5.1 EXTI main features in STM32H74x/75x, STM32H72x/73x and STM32H7A3/7Bx devices 28   
6.5.2 EXTI block diagram in STM32H74x/75x, STM32H72x/73x and STM32H7A3/7Bx devices 29

# 3.6 Reset and clock control (RCC) 32

6.6.1 Clock management . 32   
6.6.2 Peripheral clock distribution 32

# Operating conditions. 34

# Power (PWR) 35

System configuration controller (SYSCFG). 37

Secure digital input/output and MultiMediaCard interface (SDMMC). . .38

Universal (synchronous) asynchronous receiver-transmitter (U(S)ART) .39

Serial peripheral interface (SPI) 40

2 Integrated interchip sound interface (I2S) .41

3 Flexible memory controller (FMC). 42

14 Analog-to-digital converters (ADC). 44

15 Digital-to-analog converter (DAC) . 47

16 USB on-the-go (USB OTG) 49

17 Ethernet (ETH). .50

18 Digital filter for sigma delta modulators (DFSDM). 51

Revision history 53

List of tables 57

List of figures. .59

# List of tables

Table 1. Applicable products 1   
Table 2. STM32H7 lines differences at a glance 3   
Table 3. Available bus matrix on STM32F7 Series, STM32H74x/75x, STM32H72x/73x and STM32H7A3/7Bx devices .6   
Table 4. Available packages on STM32F7 Series, STM32H74x/75x, STM32H72x/73x and STM32H7A3/7Bx devices . 11   
Table 5. LQFP64 package compatibility between STM32F7 Series and STM32H7A3/7Bx devices 12   
Table 6. BYPASS_REG pin incompatibility between STM32F7 Series, STM32H74x/75x, STM32H72x/73x and STM32H7A3/7Bx devices 13   
Table 7. STM32F7 Series, STM32H74x/75x, STM32H72x/73x and STM32H7A3/7Bx devices bootloader communication peripherals. 16   
Table 8. Boot mode compatibility between STM32F7 Series, STM32H74x/75x, STM32H72x/73x, and STM32H7A3/7Bx devices.. 17   
Table 9. Peripheral summary for STM32F7 Series, STM32H74x/75x, STM32H72x73x, and STM32H7A3/7Bx devices. . . 18   
Table 10. Comparison of RAM size between STM32F7 Series, STM32H74x/75x, STM32H72x/73x and STM32H7A3/7Bx devices. . ..21   
Table 11. Memory organization and compatibility between STM32F7 Series, STM32H74x/75x, STM32H72x/73x and STM32H7A3/7Bx devices . . .22   
Table 12. Examples of peripheral address mapping differences between STM32F7 Series,STM32H74x/75x, STM32H72x/73x and STM32H7A3/7Bx devices . . .24   
Table 13. Flash memory differences between STM32F7 Series, STM32H74x/75x, STM32H72x/73x and STM32H7A3/7Bx devices. . 25   
Table 14. Interrupt vector differences between STM32F7 Series, STM32H74x/75x, STM32H72x/73x and STM32H7A3/7Bx devices. 26   
Table 15. EXTI event input types differences between STM32F7 Series, STM32H74x/75x, STM32H72x/73x and STM32H7A3/7Bx devices . 29   
Table 16. EXTI line differences between STM32F7 Series, STM32H74x/75x, STM32H72x/73x and STM32H7A3/7Bx devices 29   
Table 17. Different source clock in STM32F7 Series, STM32H74x/75x, STM32H72x/73x and STM32H7A3/7Bx devices. . . 32   
Table 18. Peripheral clock distribution example . 33   
Table 19. General operating conditions for STM32F7 Series, STM32H74x/75x, STM32H72x/73x and STM32H7A3/7Bx devices. 34   
Table 20. PWR differences between STM32F7 Series, STM32H74x/75x, STM32H72x/73x and STM32H7A3/7Bx devices . 35   
Table 21. SYSCFG main features differences between STM32F7 Series, STM32H74x/75x, STM32H72x/73x and STM32H7A3/7Bx devices 37   
Table 22. SDMMC differences between STM32F7 Series, STM32H74x/75x, STM32H72x/73x and STM32H7A3/7Bx devices .38   
Table 23. U(S)ART differences between STM32F7 Series, STM32H74x/75x, STM32H72x/73x and STM32H7A3/7Bx devices 39   
Table 24. SPI differences between STM32F7 Series, STM32H74x/75x, STM32H72x/73x and STM32H7A3/7Bx devices . . 40   
Table 25. I2S differences between STM32F7 Series, STM32H74x/75x, STM32H72x/73x and STM32H7A3/7Bx devices. . . 41   
Table 26. FMC differences between STM32F7 Series devices, STM32H74x/75x, STM32H72x/73x and STM32H7A3/7Bx devices.. ...42   
Table 27. ADC diferences between STM32F7 Series,STM32H74x/75x, STM32H72x/73x and STM32H7A3/7Bx devices . . 44   
Table 28. External trigger for regular channel dfferences between STM32F7 Series, STM32H74x/75x, STM32H72x/73x and STM32H7A3/7Bx devices 45   
Table 29. External triger for injectedchannel differences between STM32F7 Series, STM32H74x/75x, STM32H72x73x and STM32H7A3/7Bx devices . . . .46   
Table 30. DAC diffrences between STM32F7 Series, STM32H74x/75x, STM32H72x/73x and STM32H7A3/7Bx devices. . 47   
Table 31. DAC1 trigger selection differences between STM32F7 Series, STM32H74x/75x, STM32H72x/73x and STM32H7A3/7Bx devices . . 47   
Table 32. DAC2 trigger selection new for STM32H7A3/7Bx devices 48   
Table 33. USB OTG differences between STM32F7 Series, STM32H74x/75x, STM32H72x/73x and STM32H7A3/7Bx devices .49   
Table 34. Ethernet differences between STM32F7 and STM32H7 devices .50   
Table 35 DESDM differences between STM32F7 Series STM32H74x/75x STM32H72x/73x and STM32H7A3/7Bx devices51   
Table 36. DFSDM internal signal differences between STM32F7 Series, STM32H74x/75x, STM32H72x/73x and STM32H7A3/7Bx devices . ...51   
Table 37. DFSDM trigger connection differences between STM32F7 Series, STM32H74x/75x, STM32H72x/73x and STM32H7A3/7Bx devices . 52   
Table 38. DFSDM break connection differences between STM32F7 Series, STM32H74x/75x, STM32H72x/73x and STM32H7A3/7Bx devices 52   
Table 39. Document revision history . 53

# List of figures

Figure 1. STM32F7 Series devices system architecture. 7   
Figure 2. STM32H74x/75x devices system architecture. 8   
Figure 3. STM32H72x/73x devices system architecture. 9   
Figure 4. STM32H7A3/7Bx devices system architecture 10   
Figure 5. LQFP64 package compatibility . 12   
Figure 6. System supply configuration on STM32H74x/75x and STM32H7A3/7Bx devices with SMPS 14   
Figure 7. System supply configuration on STM32H74x/75x and STM32H7A3/7Bx devices without SMPS 15   
Figure 8. RAM memory organization of STM32F7 Series, STM32H743/753 and STM32H7A3/7Bx devices 23   
Figure 9. EXTI block diagram on STM32H74x/75x, STM32H72x/73x and STM32H7A3/7Bx devices 29   
Figure 10. Peripheral clock distribution on STM32H74x/75x, STM32H72x/73x and STM32H7A3/7Bx devices 32   
Figure 11. FMC bank address mapping on STM32H7A3/7Bx and STM32H72x/73x devices 42   
Figure 12. FMC bank address mapping on STM32H74x/75x devices 43

# IMPORTANT NOTICE  READ CAREFULLY

pt old ursant  dits   leole.

purchasers' products.

No license, express or implied, to any intellectual property right is granted by ST herein.

re the property of their respective owners.