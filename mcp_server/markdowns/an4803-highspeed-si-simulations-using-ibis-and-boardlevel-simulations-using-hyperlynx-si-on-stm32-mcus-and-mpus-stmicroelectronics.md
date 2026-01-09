# High-speed SI simulations using IBIS and board-level simulations using HyperLynx® SI on STM32 MCUs and MPUs

# Introduction

® perform board-level simulations with the HyperLynx® SI (signal integrity) software, to address S issues.

ca, plnvi conclusions can be extrapolated to any STM32 32-bit Arm® Cortex® MCU or MPU.

equipment, as a signal degradation: overshoot, undershoot, ringing, crosstalk, or timing delay.

very important before designing a prototype.

# 1 General information

This application note information and conclusions can be extrapolated to all the STM32 32-bit Arm® Cortex® MCUs and MPUs.

# Note:

Arm is a registered trademark of Arm Limited (or its subsidiaries) in the US and/or elsewhere.

# 2 Terms and acronyms

This section defines the terms and acronyms used in this document.

Table 1. Acronyms used in this document   

<table><tr><td rowspan=1 colspan=1>Term</td><td rowspan=1 colspan=1>Definition</td></tr><tr><td rowspan=1 colspan=1>DDR</td><td rowspan=1 colspan=1>Double data rate. Define an interface where data are sampled on both clock edges.</td></tr><tr><td rowspan=1 colspan=1>DDR3L</td><td rowspan=1 colspan=1>DDR memory 3rd generation using low voltage.</td></tr><tr><td rowspan=1 colspan=1>EMC</td><td rowspan=1 colspan=1>environment without adversely influencing the surrounding devices, or being influenced by them.</td></tr><tr><td rowspan=1 colspan=1>FR4</td><td rowspan=1 colspan=1>It t uak  ar describes the board itself with no copper covering.</td></tr><tr><td rowspan=1 colspan=1>IBIS</td><td rowspan=1 colspan=1>Iatthe analog behavior of the buffers of a digital device using plain ASCll text formatted data.</td></tr><tr><td rowspan=1 colspan=1>IO</td><td rowspan=1 colspan=1>Input and output words.</td></tr><tr><td rowspan=1 colspan=1>LPDDR2</td><td rowspan=1 colspan=1>Low-power DDR memory 2nd generation.</td></tr><tr><td rowspan=1 colspan=1>LPDDR3</td><td rowspan=1 colspan=1>Low-power DDR memory 3rd generation.</td></tr><tr><td rowspan=1 colspan=1>ODT</td><td rowspan=1 colspan=1>On-die termination.</td></tr><tr><td rowspan=1 colspan=1>PCB</td><td rowspan=1 colspan=1>Printed circuit board.</td></tr><tr><td rowspan=1 colspan=1>QUADSPI</td><td rowspan=1 colspan=1>It is is a specialized communication interface targeting single, dual or quad SPI flash memories.</td></tr><tr><td rowspan=1 colspan=1>SI</td><td rowspan=1 colspan=1>Signal integrity, denotes the correct timing and quality of the signal.</td></tr><tr><td rowspan=1 colspan=1>SDRAM</td><td rowspan=1 colspan=1>Synchronous dynamic random access memory.</td></tr></table>

# 3 SI fundamentals and STM32 signals

# 3.1

# Signal integrity fundamentals

Whorra alantainhiec parcultmust gi design traces that match the impedance of the driver and the receiver devices.

Tacun tanri boarctonohean vay a  ueul once a PCB is loaded with any components.

# 3.1.1 Signal integrity

critical element forany new digital PCB design as the clock speeds have increased by more than hundreds o me e  alaclcsl i setup timing violations and propagation delay times may appear.

# D Transmission lir :

Asioneeuiv eei circuit characteristics are dominated with inductances and capacitances.

# 3.1.3

# Transmission line model

![](images/25cd5272af4be0b0a5c7b5e04da09d4b11f25e6b6f1fb15f838a81e534e70150.jpg)  
Figure 1. Transmission line at high frequency

T gals  tanission  ravel speed that epen he urrondg medim.Te pro delay is the inverse of propagation velocity.

![](images/4a38cc0658aeb45ce4973f209fd1c2dc6c03ebb8b33addcc65093955cdaa17d2.jpg)

![](images/5d53e214277c27fb22d0ca4487b97b47ade0da987a8636a798f48c631dc38e8e.jpg)

v: propagation velocity, in meters/second   
c: speed of light in a vacuum (3 x 108 m/s)   
εr: dielectric constant   
TD: time delay for a signal to propagate down a transmission line of length x   
The propagation delay can also be determined from the equivalent circuit model of the transmission line:

![](images/990f9bd52aec3a6308ce14c6993dcf3c6f80b208546f3a62175d26d4d07c9229.jpg)

# Where:

TD: is the time delay for a signal to propagate down a transmission line of length x L: is the total series inductance for the length of the line   
C: is the total shunt capacitance for the length of the line.

The propagation delay is about 3.5 ps/mm in air where the dielectric constant is 1.0. In FR-4 PCBs, the propagation delay is about 7 to 7.5 ps/mm and the dielectric constant is 3.9 to 4.5.

T  hee al ha T rise (or fall) times x1/(propagation delay).

Example 1 : For a 2 nanosecond rise time the critical length is 47.6 mm.

# 3.1.4

# Characteristic impedance

The characteristic impedance (Zo) of the transmission line is defined by:

![](images/171ab3e0683e7e5bee54afeab59d1371b6d729740513d78fdd64859cf675ff28.jpg)

# Where:

L: is in henries per unit length C: is in farads per unit length.

At very high frequency or with very lossy lines, the resistive loss become significant.

# 3.2 IBIS model

T elgu o information.

The IB models are used or sinal integrity analysis on system boards.These modes allow system designers ulathereoamenta l ntegrinceissona different devices.

The potential problems that can be analyzed by means of the simulations include among others:

The degree of energy reflected back to the driver from the wave that reaches the receiver due to   
mismatched impedance in the line   
Crosstalk   
Ground and power bounce   
Overshoot or undershoot   
Line termination analysis

# 3.2.1 IC modeling

The figure below shows an example of two ICs modeling:

![](images/7283e63be9b29f2e3382e73be81dce82f2074f3a2c4fcb84131f1a07bb2fac06.jpg)  
Figure 2. Transmission iine with iC modeling

# 3.2.2

# Basic structure of an IBIS file

D Header

File name, date, version, source, notes, copyright, etc.

• Component model data

Default package data (L_pkg, R_pkg, C_pkg)   
Complete pin list (pin name, signal name, buffer name, and optional L_pin, R_pin, C_pin) Differential pin pairs, on-die terminators, buffer selector, etc.

I0 model data

All buffer models for the component must be defined in the file Each flavor of a programmable buffer is separate model

As shown in Figure 3 and Figure 4, the HyperLynx visual IB editor is used to open the TM32F746 and the SDRAM (MT48LC4M32B2B5-6A) and to view their characteristics such as the rising and the fallng waveforms.

![](images/92505b4f97db64c540b7faebcf35956dd8fc7a34fe7834c9bb40aee903d2d69a.jpg)  
Figure 3. IBIS editor

![](images/27d2fffc69fea23bfe29180c278182133861c8a55a3abba093cf5776a725609e.jpg)  
Figure 4. IBIS data

# STM32 MCUs and MPUs IBIS model selection/selector

Ti ct en e Bmol elechevailabl I gal-urut/utu)  STM32 MCUs and MPUs.

# GPIO structure

The GPIO includes below features:

Output driver   
Input buffer   
Pull-up and pull-down   
Electrostatic discharge (ESD) protection Input hysteresis   
Level shifter   
Control logic.

# 4.2

# Model selector

The GPlO pins can be selected following below parameters depending on the application requirements:

Two operating voltage ranges:

V33 (3.3 V): refer to 2.7 V to 3.6 V external voltage range VDDx V18 (1.8 V or Iv): refer to 1.7 ( see Note below) to 2.7 V external voltage range VDDx

Four or less output buffer speed control depending on the required frequency

00 (low speed)   
01 (medium speed)   
10 (fast speed)   
11 (high speed)

Controllable internal pull-up and pull-down resistor (enabled/disabled): PD/PU

Specific IO pins are used to cover special functions: USB and I2C. The same IO is also available as GPIC pin.

Note:

For more details, refer to the specific STM32 device datasheet on the section l/O port characteristics and also to the corresponding STM32 reference manual on the section General purpose l/O (GPIO) for software configuration and selection.

# Example of model selector on STM32F746xx MCU

The example below keeps the same selected IO/Pin as in Section3..2 . The pin is H14 port PG8. This pin belongs to the family "io8p_arsudq_ft" of IO buffer.

InTable, he p  with he electe GOciguratins ishihlghted inierent colors s pe le footnote legend.

Table 2. l/Os in/output buffer for "io8p_arsudq_ft" selector   

<table><tr><td rowspan=2 colspan=1>I0 model name selection (io8p_ar3wsudq_ft)</td><td rowspan=1 colspan=5>I/O parameters</td></tr><tr><td rowspan=1 colspan=3>Voltage range</td><td rowspan=1 colspan=1>Buffer speed</td><td rowspan=1 colspan=1>Pull up/Pull down</td></tr><tr><td rowspan=1 colspan=1>io8p00(1_ar3wsudq_ft_pd(3)_Iv(2) &quot;SPEED00 1P8V, PD=40kOhm&quot;</td><td rowspan=1 colspan=3></td><td rowspan=1 colspan=1></td><td rowspan=1 colspan=1>Pull down 40 K(3)</td></tr><tr><td rowspan=3 colspan=1>io8p00_ar3wsudq_ft_pu_Iv &quot;SPEED00 1P8V, PU=40kOhm&quot;</td><td rowspan=3 colspan=2>1.7 V to 2.7 V(2)</td><td></td><td></td><td></td></tr><tr><td rowspan=2 colspan=2></td><td></td><td></td></tr><tr><td rowspan=1 colspan=1></td><td rowspan=1 colspan=1>Low speed(1)</td><td rowspan=1 colspan=1>Pull up 40 K</td></tr><tr><td rowspan=1 colspan=1>io8p00_ar3wsudq_ft_Iv &quot;SPEED00 1P8V&quot;</td><td rowspan=1 colspan=3></td><td rowspan=1 colspan=1></td><td rowspan=1 colspan=1>Disabled</td></tr><tr><td rowspan=1 colspan=1>io8p01_ar3wsudq_ft_pd_Iv &quot;SPEED01 1P8V, PD=40kOhm&quot;</td><td rowspan=1 colspan=3></td><td rowspan=1 colspan=1></td><td rowspan=1 colspan=1>Pull down 40 K</td></tr><tr><td rowspan=1 colspan=1>io8p01_ar3wsudq_ft_pu_Iv &quot;SPEED01 1P8V, PU=40kOhm&quot;</td><td rowspan=1 colspan=3>1.7 V to 2.7 V</td><td rowspan=1 colspan=1>Medium speed</td><td rowspan=1 colspan=1>Pull up 40 K</td></tr><tr><td rowspan=1 colspan=1>io8p01_ar3wsudq_ft_Iv &quot;SPEED01 1P8V&quot;</td><td rowspan=1 colspan=3></td><td rowspan=1 colspan=1></td><td rowspan=1 colspan=1>Disabled</td></tr><tr><td rowspan=1 colspan=1>io8p10_ar3wsudq_ft_pd_Iv &quot;SPEED10 1P8V, PD=40kOhm&quot;</td><td rowspan=1 colspan=3></td><td rowspan=1 colspan=1></td><td rowspan=1 colspan=1>Pull down 40 K</td></tr><tr><td rowspan=1 colspan=1>io8p10_ar3wsudq_ft_pu_Iv &quot;SPEED10 1P8V, PU=40kOhm&quot;</td><td rowspan=2 colspan=3>1.7 V to 2.7 V</td><td rowspan=2 colspan=1>Fast speed</td><td rowspan=1 colspan=1>Pull up 40 K</td></tr><tr><td rowspan=1 colspan=1>io8p10_ar3wsudq_ft_Iv &quot;SPEED10 1P8V&quot;</td><td rowspan=1 colspan=1>Disabled</td></tr><tr><td rowspan=1 colspan=1>io8p11_ar3wsudq_ft_pd_lv &quot;SPEED11 1P8V, PD=40kOhm&quot;</td><td rowspan=1 colspan=3></td><td rowspan=1 colspan=1></td><td rowspan=1 colspan=1>Pull down 40 K</td></tr><tr><td rowspan=1 colspan=1>io8p11_ar3wsudq_ft_pu_v &quot;SPEED11 1P8V, PU=40kOhm&quot;</td><td rowspan=1 colspan=3>1.7 V to 2.7 V</td><td rowspan=1 colspan=1>High speed</td><td rowspan=1 colspan=1>Pull up 40 K</td></tr><tr><td rowspan=1 colspan=1>io8p11_ar3wsudq_ft_Iv &quot;SPEED11 1P8V&quot;</td><td rowspan=1 colspan=3></td><td rowspan=1 colspan=1></td><td rowspan=1 colspan=1>Disabled</td></tr><tr><td rowspan=1 colspan=1>io8p00_ar3wsudq_ft_pd &quot;SPEED00, PD=40kOhm&quot;</td><td rowspan=1 colspan=3></td><td rowspan=1 colspan=1></td><td rowspan=1 colspan=1>Pull down 40 K</td></tr><tr><td rowspan=1 colspan=1>io8p00_ar3wsudq_ft_pu &quot;SPEED00, PU=40kOhm&quot;</td><td rowspan=1 colspan=3>2.7 V to 3.6 V</td><td rowspan=1 colspan=1>Low speed</td><td rowspan=1 colspan=1>Pull up 40 K</td></tr><tr><td rowspan=1 colspan=1>io8p00_ar3wsudq_ft &quot;SPEED00&quot;</td><td rowspan=1 colspan=3></td><td rowspan=1 colspan=1></td><td rowspan=1 colspan=1>Disabled</td></tr><tr><td rowspan=1 colspan=1>io8p01_ar3wsudq_ft_pd &quot;SPEED01, PD=40kOhm&quot;</td><td rowspan=1 colspan=3></td><td rowspan=1 colspan=1></td><td rowspan=1 colspan=1>Pull down 40 K</td></tr><tr><td rowspan=1 colspan=1>io8p01_ar3wsudq_ft_pu &quot;SPEED01, PU=40kOhm&quot;</td><td rowspan=1 colspan=3>2.7 V to 3.6 V</td><td rowspan=1 colspan=1>Medium speed</td><td rowspan=1 colspan=1>Pull up 40 K</td></tr><tr><td rowspan=1 colspan=1>io8p01_ar3wsudq_ft &quot;SPEED01&quot;</td><td rowspan=1 colspan=3></td><td rowspan=1 colspan=1></td><td rowspan=1 colspan=1>Disabled</td></tr><tr><td rowspan=1 colspan=1>io8p10_ar3wsudq_ft_pd &quot;SPEED10, PD=40kOhm&quot;</td><td rowspan=3 colspan=3>2.7 V to 3.6 V</td><td rowspan=3 colspan=1>Fast speed</td><td rowspan=1 colspan=1>Pull down 40 K</td></tr><tr><td rowspan=1 colspan=1>io8p10_ar3wsudq_ft_pu &quot;SPEED10, PU=40kOhm&quot;</td><td rowspan=1 colspan=1>Pull up 40 K</td></tr><tr><td rowspan=1 colspan=1>io8p10_ar3wsudq_t &quot;SPEED10&quot;</td><td rowspan=1 colspan=1>Disabled</td></tr><tr><td rowspan=1 colspan=1>io8p11_ar3wsudq_ft_pd &quot;SPEED11, PD=40kOhm&quot;</td><td rowspan=1 colspan=3></td><td rowspan=1 colspan=1></td><td rowspan=1 colspan=1>Pull down 40 K</td></tr><tr><td rowspan=1 colspan=1>io8p11_ar3wsudq_ft_pu &quot;SPEED11, PU=40kOhm&quot;</td><td rowspan=1 colspan=3>2.7 V to 3.6 V</td><td rowspan=1 colspan=1>High speed</td><td rowspan=1 colspan=1>Pull up 40 K</td></tr><tr><td rowspan=1 colspan=1>io8p11_ar3wsudq_ft &quot;SPEED11&quot;</td><td rowspan=1 colspan=3></td><td rowspan=1 colspan=1></td><td rowspan=1 colspan=1>Disabled</td></tr></table>

0 01 = medium speed, 10 = fast speed, 11 = high speed. Refer to column "Buffer speed" in this table. 2. nhho "Iv" = 1.7 to 2.7 V, [empty] = 2.7 to 3.6 V. 3. ul u value "pu" = pull down, "pd" = pull down, [empty] = disabled.

# Application example with HyperLynx simulator

# 5.1

# HyperLynx simulation with SDRAM

This design example shows how to perform a simulation with HyperLynx on MCu Discovery board with STM32F746 (32F746GDISCOVERY). The SDRAM data bus are the critical signals on this PCB board to be analyzed.

# 5.1.1 SDRAM signals

The FMC controller nd in partcular heSDRAM memoy controller, hasman als, most them havesil functionalities and work together. The controller I/O signals can be split in four groups as follows:

Address group: consists of row and column address and bank address   
Command group: includes the row address strobe (NRAS), the column address strobe (NCAS), and write   
enable (SDWE)   
Control group: includes chip select bank1 and bank2 (SDNE0/1), clock enable bank1 and bank2   
(SDCKE0/1), and output byte mask for write access (DQM)   
Data group/lane contains x8/x16/x32 signals and the data mask (DQM)

In this Discovery board the memory used is an SDRAM with x16 bus widths and have two data group lanes from Micron (part number: MT48LC4M32B2B5-6A) as shown in the figure below.

![](images/c696e9a187d2ddcd5308a8db21986b53236ef360177415b3c4a5b48d0afd7886.jpg)  
Figure 5. SDRAM schematic

# 5.1.2

# SDRAM simulation

The following sequence describes the steps for design and simulation

Step 1. Schematics design

The schematic shown in Figure 5 is the connected signal between the SDRAM and the STM32F746 (FMC_xx).

# Step 2. PCB design

Use the gerber viewer Gerbv 2.6.1 to see the PCB design. Figure 6 shows the PCB design of the CPU board with STM32F746 and SDRAM chips are placed close to each other, where SDRAM is on the left side.

![](images/c4991961a1c4b868263077db6c4cf2af8c712614ed42c40dc987582c3fc8a9aa.jpg)  
Figure 6. 32F746GDISCOVERY schematic   
tep 3. Translate PCB board file to simulation le

#

Using the HyperLynx simulation tool from Mentor Graphics® to do PCB board simulation. Run HyperLynx and open the MB1191B-V14.paf file, and then translate it to MB1191B- V14.hpy file for simulation as shown in Figure 7.

# Note:

This Discovery board layout was designed with Zuken CADStar, so to do simulation with HyperLynx, use PAF file with the same file name.

# Step 4. Select the signal to simulate. Step 4a. Open the MB1191B-V14.hpy file.

![](images/520e665e4439210f9c019f57d2e62304c6879a8951487931401966ebc78aae85.jpg)  
Figure 7. 32F746GDISCOVERY PCB

Step 4b. Select the signal to simulate (for example SDRAM FMC_D10). Go to Select in upper menu and choose Net by Name for Sl Analysis (see Figure 8).

![](images/b9a7eb711d724f7315a051071c893fc4063cc4e5b642c0d9e2ab5ea31de53e0d.jpg)  
Figure 8. Signal selection

# Step 5. Assign IBIS model for STM32F746 and MT48LC4M32B2B5.

The IBIS model is usually available on the manufacturer's website. The IBIS Model file associated with STM32F746 can be downloaded from the STMicroelectronics web site at www.st.com and for MT48LC4M32B2B5 can be downloaded from Micron website. After downloading the model for each IC and add it to the HyperLynx lib path. Assign the IBIS model for each signal vs IC Figure 7.

![](images/dec01db466f1d0a18eef036d7e68ad7e519c56347326d7d31785b20bdf869fa4.jpg)  
Figure 9. Assign IBIS model

S Export he sele sigal to the eeor sheac an congu he sacup inon.

![](images/f46e604322d468671cb2316fca2c39b5195b1776e28e0dcb2f6e4996df34997f.jpg)  
Figure 10. Free-form schematic

# Step 7. Configure and start the simulation. Set the frequency to 108 MHz and the Duty to 50% (see Figure 11).

![](images/d73fafa2ab36273693c40be16442e7b86eda1c60e4849e4ffafefe23a5f33b2b.jpg)  
Figure 11. Waveform with I/O speed of 0x00

Step 8. Compare and analyze the results by changing IO speed selection for STM32F746 (in red FMC_SDRAM coming out of STM32F7 and in green waveform at SDRAM input).

In the previous steps, the IO speed was set to Ox00. The data signal in red coming out of the STM32F746 is already distorted: square shape with reduced swing and straight slope due to I0 speed limitation. The maximum l/O frequency with this setting is 8 MHz and rise time of 100 ns. This can be explained by output signal transitions under the loading conditions Cref and Rref for IO buffer model at lower speed 0x00.

In order to improve the shape of the waveform at the output of STM32F476, the IO speed must be changed to handle more signal frequency content to 0x10 (I0 maximum frequency of 100 MHz) and 0x11 (IO maximum frequency of 180 MHz) (see Figure 12).

![](images/5c5b8536e0cb72232294c65ebac50c474f92f53b167bab46b104626ae50364af.jpg)  
Figure 12. Waveform with l/O speed of 0x10

![](images/643ef872722689bbf61b077d8afd98df3ba77f3e98abef19b07b41b992e4065b.jpg)  
Figure 13. Waveform with l/O speed of 0x11

Use the right configuration of IOs speed to match frequency content of target signal for a good Sl without any distortion.

# 5.2

# HyperLynx simulation with QUADSPI

# 5.2.1

# QUADSPI signals

![](images/682253d461b0497a4ac27d7126a49e0de3430be5c77beefffd7e68ef8becd1d7.jpg)  
Figure 14. QUADSPI schematic NOR memory interface

![](images/c5e4ea201dc96106a382016ba662288db9591a81811f7038828e7de45c4a9f86.jpg)  
Figure 15. QUADSPI schematic STM32 interface (part 1)

![](images/d0654863629923f884a644dcca5d7c2bde79f8eb93a6e58a7bf41ef0c311febb.jpg)  
Figure 16. QUADSPI schematic STM32 interface (part 2))

# 5.2.2

# QUADSPI simulation

The following sequence describes the steps or design and simulation  clock signal or QuADSP inteace:

# Step 1.

Schematic design.

The schematic shown in Figure 14 and Figure 15 is the connected signal between the serial NOR flash memory and the STM32F746 (QSPI_xx).

# Step 2.

Open the PCB board file to simulation QUADSPI.   
Run HyperLynx and open the MB1191B-V14.hpy file for simulation.

Step 3. Select the signal to simulate.

Select the clock signal to simulate (for example QSPI_CLK/ PB2). Go to Select in upper menu and choose Net by Name for Sl Analysis (see Figure 8).

![](images/70a59d7647205bd5a3f70113560734b66487c6e25938930e0a75226e5a76b608.jpg)  
Figure 17. Signal selection   
Step 4. Assign IBIS model for STM32F746 and N25Q128A13EF840E.

The IBIS model is usually available on the manufacturer's website. The IBIS model file associated with STM32F746 can be downloaded from the STMicroelectronics web site at www.st.com and for N25Q128A13EF840E can be downloaded from Micron web site.

After downloading the model for each IC and add it to the HyperLynx lib path. Assign the IBIS model for each signal vs IC Figure 8. Signal selection.

S .Export the sele sigal to the eeorm sheac an congue the sac up inorn.

![](images/537ea79c1acc18f777985d26f91ce5f335290aa093c8511a59e494a56352847f.jpg)  
Figure 18. Free-form schematic QSPI_CLK

Step 6. Configure and start the simulation. Set the frequency to 108 MHz and the Duty to 50% (see figure below)

![](images/c1d2b2950fa7dd4e339831b32cde728fd6a17fd7e0aa802be5439a9dcfa4dd34.jpg)  
Figure 19. Waveform with R44 = 0Ω

Step 7.Compare and analyze the results by changing R4 serial resitor.

In the previous steps, the series source termination resistor was 0Ω, the green waveform (at input of QSPI memory) is showing an overshooting and undershooting due to mismatching of the characteristic impedance.This type o termination requires that the sum of the buffer impedance and thevalue he resistor be equal to the characteristic impedance of the line.

Double click on the R44 and change its value to 33Ω, see figure Figure 20.

![](images/c5e0b8ace78444efae2513dab65152fd2f8af77fbe68eb3c9725064c85cb5b7c.jpg)  
Figure 20. Waveform with R44 = 33Ω

An improvement of shape of clock output from STM32 can be observed. Else, the Terminator Wizard can be run to analyze the selected net and suggest the optimum termination values for R44.

![](images/4a7fa6ac9e9d1ce8cc78d842cfc8af12a0e11fc15bed4dde236fdf3f259ba402.jpg)  
Figure 21. Terminator Wizard menu

When "Apply values" is selected, the serial resistor R44 takes the value in this schematic, which is 40.6Ω. See the shape of the wave with simulation in Figure 22.

![](images/9c906401e403e89e12d8459ddc6d60717b84d04b34bea1f47b038250586d52d1.jpg)  
Figure 22. Waveform with R44 = 40.6Ω

The Termination Wizard analyzes the selected net, presents a list of trace statistics and makes suggestions for the optimum value of R. It takes into account the capacitive loading of the receiver ICs, total line length, and driver impedance.

# 5.3

# HyperLynx simulation with DDR3L

# 5.3.1 DDR3L signals

This example shows how to perform a simulation on STM32MP15 Series and DDR3L with DDRx batch simulation of Hyperlynx. The DDR SDRAM has:

dedicated signals   
differential pair for clock   
address/command, controls   
reference voltage   
calibration resistor   
data lines in which four bytes are each composed with:   
eight data   
a data mask   
differential pair for data strobe

![](images/b9c4913b55cac5024a226e45acce6750a0cb77ff143692b8767dd789bb89de6e.jpg)  
Figure 23. DDR3L schematic STM32MP15 interface

![](images/9046bba1245a085c43a78927d584f43c649c016025a63c1c3b1a1bad69c6982b.jpg)  
Figure 24. DDR3L schematic memory interface

# 5.3.2

# DDR3L simulation

When your layout is finished follow these steps:

![](images/a170dafa720785c14e73f8b7524c8ab5e5cbee0a94d26c84d5706fabf7da1b28.jpg)  
Step 1. Export your PCB into Hyperlynx file through Altium.   
Figure 25. Altium export menu   
Step 2. With Hyperlynx, open .hyp file created.

![](images/47776398c02b79302d914648aff62ff80d22586a768683a626af6511a59d9a94.jpg)  
Figure 26. STM32MP15XXAA PCB

Step 3. Fill the stack up, the power supplies. Do not forget to set as signal the layers used to route data and address/command tracks, as plane the ground layer and the layer which has the VDD_DDR power plane.

# Step 4. Assign IBIS model by reference designator.

![](images/41675ab12d31e76d6acc1823bab50d5755e1de024d0b911d059dfcf94e3267aa.jpg)  
Figure 27. DDRx batch simulation   
Ste 5. Continue the set up of your simulation, assign the conroller, the DRAM and the nets.

Step 6. Select the models of driver impedance and ODT for data, data mask, and differential pair for data strobe

![](images/003328b52ba234e8f5b6020776bab42197ca272187e36f95717cbf5cbd0ebbda.jpg)  
Figure 28. DDRx batch simulation: ODT for data lines

# Rule of data naming for output driver impedance in the column 'ODT Disable':

MSD_D3RP3_xx for DDR3 single-ended signal, xx is the value of driver impedance MSD_D3RP3L_ xx for DDR3L single-ended signal, xx is the value of driver impedance MSD_D3RPL2_ xx for LPDDR2 single-ended signal, xx is the value of driver impedance MSD_D3RF3_xx for DDR3 differential signal, xx is the value of driver impedance MSD_D3RF3L_ xx for DDR3L differential signal, xx is the value of driver impedance MSD_D3RFL2_ xx for LPDDR2 differential signal, xx is the value of driver impedance

# Rule of data naming for ODT receiver in the column 'ODT Enable':

MSD_D3RP3_oDTyy for DDR3 single-ended signal, yy is the value of ODT receiver MSD_D3RP3L_oDTyy for DDR3L single-ended signal, yy is the value of oDT receiver MSD_D3RPL2_oDTyy for LPDDR2 single-ended signal, yy is the value of ODT receiver MSD_D3RF3_DTyy for DDR3 differential signal, yy is the value of ODT receiver MSD_D3RF3L_oDTyy for DDR3L differential signal, yy is the value of ODT receiver MSD_D3RFL2_oDTyy for LPDDR2 differential signal, yy is the value of ODT receiver

For LPDDR3, use LPDDR2 models.

Step 7. For the controller, select the models of driver impedance for address/command, controls, and differential pair for clock.

Even if clock is a differential signal, for simulation it is set as a single-ended signal. For the DRAM, select the input with the right data rate.

Step 7a. For the DRAM, select the input with the right data rate.

![](images/38170eda41e3c93939a541b547069db1f9c5bef90775c6e779d3e2e4f12e6462.jpg)

# Rule of address/command, control, and clock naming for driver impedance in the column 'Model':

MSD_D3RP3_xx for DDR3 single-ended signal, xx is the value of driver impedance MSD_D3RP3L_ xx for DDR3L single-ended signal, xx is the value of driver impedance MSD_D3RPL2_ xx for LPDDR2 single-ended signal, xx is the value of driver impedance

For LPDDR3, use LPDDR2 models.

Full explanation of model selector can be found in the STM32MP15 IBIS file.

Step 8. Continue the setup until no issue is detected than click "run Batch Simulation". If the simulation is failed, find the best settings in accordance with your design.

![](images/fc06eeab75ef85a6d4295654f7c2694f5b4d51fb9c0565a758bfc0f14c9731e6.jpg)  
Figure 30. DDRx batch simulation: simulate

# 6 References

HyperLynx® LineSim User Guide Software Version 9.1, Mentor Graphics, March 2014 HyperLynx® BoardSim User Guide Software Version 9.2, Mentor Graphics, December 2014 High-Speed Digital System Design, Hall, Stephen, Hall Garrtt, and McCall, James, John Wiley and Sons, Inc., 2000

# Revision history

Table 3. Document revision history   

<table><tr><td>Date</td><td>Version</td><td>Changes</td></tr><tr><td>1-Avr-2016</td><td>1</td><td>Initial release.</td></tr><tr><td>4-Sep-2019</td><td>2</td><td>Updated all the document to include MPUs on its scope.</td></tr><tr><td rowspan="6">10-Aug-2022</td><td rowspan="5">3</td><td>Updated:</td></tr><tr><td>Section Introduction •</td></tr><tr><td>Figure 15 •</td></tr><tr><td>Added:</td></tr><tr><td>Section 5.3.1 •</td></tr><tr><td></td><td>Section 5.3.2 •</td></tr></table>

# Contents

# 1 General information

2 Terms and acronyms

# 3 SI fundamentals and STM32 signals.

# 3.1 Signal integrity fundamentals. 4

3.1.1 Signal integrity 4   
3.1.2 Transmission line 4   
3.1.3 Transmission line model 4   
3.1.4 Characteristic impedance 5

# 3.2 IBIS model 5

3.2.1 IC modeling. 6   
3.2.2 Basic structure of an IBIS file 6

# STM32 MCUs and MPUs IBIS model selection/selector 8

4.1 GPIO structure. 8   
4.2 Model selector. 8   
4.3 Example of model selector on STM32F746xx MCU. 8

# Application example with HyperLynx simulator. 10

# 5.1 HyperLynx simulation with SDRAM 10

5.1.1 SDRAM signals. . 10   
5.1.2 SDRAM simulation 11

5.2 HyperLynx simulation with QUADSPI. 16

5.2.1 QUADSPI signals 16   
5.2.2 QUADSPI simulation. 17

HyperLynx simulation with DDR3L 21

5.3.1 DDR3L signals 21   
5.3.2 DDR3L simulation . 23

# 6 References 29

# Revision history .30

# List of tables .32

List of figures. .33

# List of tables

Table 1. Acronyms used in this document 3   
Table 2. I/Os in/output buffer for "io8p_arsudq_ft" selector 9   
Table 3. Document revision history . . 30

# List of figures

Figure 1. Transmission line at high frequency. 4   
Figure 2. Transmission line with IC modeling 6   
Figure 3. IBIS editor 7   
Figure 4. IBIS data . 7   
Figure 5. SDRAM schematic 10   
Figure 6. 32F746GDISCOVERY schematic . 11   
Figure 7. 32F746GDISCOVERY PCB 12   
Fiure 8. Signal selection 12   
Figure 9. Assign IBIS model. 13   
Figure 10. Free-form schematic 13   
Figure 11. Waveform with l/O speed of 0x00 14   
Figure 12. Waveform with I/O speed of 0x10 15   
Figure 13. Waveform with l/O speed of 0x11 16   
Figure 14. QUADSPI schematic NOR memory interface 16   
Figure 15. QUADSPI schematic STM32 interface (part 1) 17   
Figure 16. QUADSPI schematic STM32 interface (part 2)). 17   
Figure 17. Signal selection 18   
Figure 18. Free-form schematic QSPI_CLK 18   
Figure 19. Waveform with R44 = 0Ω. 19   
Figure 20. Waveform with R44 = 33Ω 20   
Figure 21. Terminator Wizard menu 20   
Figure 22. Waveform with R44 = 40.6Ω. 21   
Figure 23. DDR3L schematic STM32MP15 interface 22   
Figure 24. DDR3L schematic memory interface   
Figure 25. Altium export menu. 24   
Figure 26. STM32MP15XXAA PCB 24   
Figure 27. DDRx batch simulation 25   
Figure 28. DDRx batch simulation: ODT for data lines 27   
Figure 29. DDRx batch simulation: non ODT signal   
Figure 30. DDRx batch simulation: simulate. 28

# IMPORTANT NOTICE  READ CAREFULLY

pt old ursant  dits   leole.

purchasers' products.

No license, express or implied, to any intellectual property right is granted by ST herein.

re the property of their respective owners.