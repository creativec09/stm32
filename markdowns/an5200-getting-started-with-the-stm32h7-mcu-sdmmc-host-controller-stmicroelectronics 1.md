# Getting started with the STM32H7 MCU SDMMC host controller

# Introduction

T r.

tu enhanced SDMMC peripheral.

the SDMMC host interface features that facilitate its configuration.

# 1 SDMMC host interface

# Note:

The STM32H7 series are Arm® based devices.   
Arm is a registered trademark of Arm limited (or its subsidiaries) in the US and/or elsewhere.

# arm

STM32H7 series include below SDMMC features:

Supports SD, SDIO, MMC, and e-MMC memory types.   
Supports data transfer in block(s) mode, SDIO multibyte mode and MMC stream mode.   
Full compliance with MultiMediaCard system specification version 4.51.   
Full compatibility with previous versions of MultiMediaCards (backward compatibility).   
Full compliance with SD memory card specification version 4.1 (SPI mode and UHS-II mode not supported).   
Full compliance with SDIO card specification version 4.0.   
Support data wide bus 1-bit, 4-bit, and 8-bit modes.   
Data transfer up to 208 MHz depending on maximum allowed I/O speed (refer to product datasheet for more details).   
Hal A Auanuulu mode (depending on peripheral version).

The table below presents an overview of the supported speed modes of the SDMMC host interface.

Table 1. SDMMC supported speed modes   

<table><tr><td rowspan=1 colspan=1>SD &amp; SDIO</td><td rowspan=1 colspan=1>Max bus speed[Mbyte/s](1)</td><td rowspan=1 colspan=1>Max clock frequency[MHz](2)</td><td rowspan=1 colspan=1>Signal voltage(V)</td></tr><tr><td rowspan=1 colspan=1>DS (default speed)</td><td rowspan=1 colspan=1>12.5</td><td rowspan=1 colspan=1>25</td><td rowspan=1 colspan=1>3.3</td></tr><tr><td rowspan=1 colspan=1>HS (high speed)</td><td rowspan=1 colspan=1>25</td><td rowspan=1 colspan=1>50</td><td rowspan=1 colspan=1>3.3</td></tr><tr><td rowspan=1 colspan=1>SDR12</td><td rowspan=1 colspan=1>12.5</td><td rowspan=1 colspan=1>25</td><td rowspan=1 colspan=1>1.8</td></tr><tr><td rowspan=1 colspan=1>SDR25</td><td rowspan=1 colspan=1>25</td><td rowspan=1 colspan=1>50</td><td rowspan=1 colspan=1>1.8</td></tr><tr><td rowspan=1 colspan=1>SDR50</td><td rowspan=1 colspan=1>50</td><td rowspan=1 colspan=1>100</td><td rowspan=1 colspan=1>1.8</td></tr><tr><td rowspan=1 colspan=1>DDR50</td><td rowspan=1 colspan=1>50</td><td rowspan=1 colspan=1>50</td><td rowspan=1 colspan=1>1.8</td></tr><tr><td rowspan=1 colspan=1>SDR104</td><td rowspan=1 colspan=1>104</td><td rowspan=1 colspan=1>208</td><td rowspan=1 colspan=1>1.8</td></tr><tr><td rowspan=1 colspan=1></td><td rowspan=1 colspan=1>MMC cards</td><td rowspan=1 colspan=1>MMC cards</td><td rowspan=1 colspan=1></td></tr><tr><td rowspan=1 colspan=1>Legacy compatible</td><td rowspan=1 colspan=1>26</td><td rowspan=1 colspan=1>26</td><td rowspan=1 colspan=1>3/1.8/1.2</td></tr><tr><td rowspan=1 colspan=1>High speed SDR</td><td rowspan=1 colspan=1>52</td><td rowspan=1 colspan=1>52</td><td rowspan=1 colspan=1>3/1.8/1.2</td></tr><tr><td rowspan=1 colspan=1>High speed DDR</td><td rowspan=1 colspan=1>104</td><td rowspan=1 colspan=1>104</td><td rowspan=1 colspan=1>3/1.8/1.2</td></tr><tr><td rowspan=1 colspan=1>High speed HS200</td><td rowspan=1 colspan=1>200</td><td rowspan=1 colspan=1>200</td><td rowspan=1 colspan=1>1.8/1.2</td></tr></table>

1Maximum bus speed in 4-bit mode for SD& SDIO and 8-bit mode for MMC cards. 2. The maximum data transfer depends on the maximum allowed l/O speed.

# 1.1

# STM32H743/753 SDMMC host-interface integration

STM32H7 series devices provide two SDMMC host interfaces: SDMMC1 and SDMMC2. Each interface has its on features.The figure below presents an extract from the TM32H74x/H75x devices architecture showing the SDMMC host interface integration as an example.

![](images/9e8751783b96a90e75612d7758dd06d808aba085cbffa8c20a23ce98860d5e03.jpg)  
Figure 1. SDMMC1 and SDMMC2 internal connections   
1) D3 domain not available on STM32H7R/S devices.

The SDMMC1 is in the D1 domain and the SDMMC2 is in the D2 domain. Each one of them have a master int  epeively  he -bi AXI us at and he3-bit HB us at over  AHB bus, which can access different memories.

The SDMMC1 and SDMMC2 registers are accessible through their slave interface connected respectively to AHB3 and AHB2.

Each SDMMC have his own delay block (DLYB) accessible over AHB3 for SDMMC1 and over AHB2 for SDMMC2. The DLYB can be used to align the sampling clock on the data received (see figure below).

![](images/c31ac9994ce62521efcf4504fead97ec4facec93d0c3165f30d58403078baff9.jpg)  
Figure 2. SDMMC and the delay block (DLYB)

Depending on SDMMC peripheral inked-list feature availability, SDMMC peripherals have no interaction with exteral DMA.When linked ist feature is ot available, the SDMinteracts with he master DMA (MDMA) t implement automatic chaining of transfers.

The MDMA provides a channel for the SDMMC1 and 2 to enable successive data transfer from/to TCM RAMs and any memory region mapped on the three matrixes without any CPU action. The MDMA can also access the SDMC1 and SDMMC2 registers and enable a new data transferusing linked-ist mode without any CPU action.

![](images/bfc9e1fc92ebd1d62dac6da302e817d5b5b76aee2e631ced4f8063266e172a16.jpg)  
Figure 3. Triggers for MDMA and SDMMC1

STM32H7 MCUs feature the VDDMMC supply. This can be connected to VDD or used as an independent power p  ll eain pa t if pply ve pp either VDDMMC or the transceiver power rail.

n cases where the VDDMMC pin is unavailable in certain packages, it is internally connected to VDD.

For detailed information on theavailablefeatures an peripheral countsndiferent packages, refer he applicable datasheet.

SDMMC1 generates control signals for the external voltage switch transceiver to support UHS-I mode.

![](images/2f8efa1d1d815617a4f4d0f59e1b610b1a94883dcd1720c5787f807f7aa89c3a.jpg)  
Figure 4. Voltage switch transceiver

The table below presents the main features for SDMMC1 and SDMMC2.

Table 2. SDMMC1 and SDMMC2 main features   

<table><tr><td rowspan=1 colspan=1>Features</td><td rowspan=1 colspan=1>SDMMC1</td><td rowspan=1 colspan=1>SDMMC2</td></tr><tr><td rowspan=1 colspan=1>SDMMC master interface</td><td rowspan=1 colspan=1>Connected to the 64-bit AXI bus matrixin D1 domain through a 32-bit AHBmaster bus</td><td rowspan=1 colspan=1>Connected to the 32-bit AHB bus matrixin D2 domain through a 32-bit AHBmaster bus</td></tr><tr><td rowspan=1 colspan=1>SDMMC slave interface</td><td rowspan=1 colspan=1>Operating on the AHB3 bus</td><td rowspan=1 colspan=1>Operating on the AHB2 bus</td></tr><tr><td rowspan=1 colspan=1>Memory access</td><td rowspan=1 colspan=1>Domain D1AXI SRAMquad-SPI(1)FMC</td><td rowspan=1 colspan=1>Domain D1AXI SRAMquad-SPI (1)FMCDomain D2SRAM1/SRAM2/SRAM3Domain D3SRAM4Backup SRAM</td></tr><tr><td rowspan=1 colspan=1>SDMMC delay block</td><td rowspan=1 colspan=1>Operating on the AHB3 bus</td><td rowspan=1 colspan=1>Operating on the AHB2 bus</td></tr><tr><td rowspan=1 colspan=1>MDMA</td><td rowspan=1 colspan=1>The MDMA provides a channel forsuccessful end of data transferThe MDMA can configure theSDMMC registers to enable a newdata transfer</td><td rowspan=1 colspan=1>The MDMA can configure theSDMMC registers to enable a newdata transfer</td></tr><tr><td rowspan=1 colspan=1>UHS-I</td><td rowspan=1 colspan=1>Generates control signals to control theexternal voltage switch transceiver</td><td rowspan=1 colspan=1>No control signal generation for externaltransceiver(2)</td></tr></table>

Check product datasheet for memory interface availability 2. C signals).

# 1.2

# STM32H7R/S SDMMC host-interface integration

The figure below is an extract from the TM32H7R/S Boot-flash device architecture howing the SDMC hostnterface integration.

![](images/b1fbc3d7271cdb96f8b82af94bb694b3e2e99f1628363d8925daa410b2a06860.jpg)  
Figure 5. SDMMC internal connection in the STM32H7R/S

The SDMMC1 master interace is in the 64-bit AXI bus matrx and SDMC2 is in the 32-it AHB bus matri.   
These interfaces are accessible through their respective slave interfaces connected to AHB5 and AHB2.

For the STM32H7R/S line, an independent VDDMMC supply is not available on the SDMMC l/Os, therefore the supply level is the same as VDD. Therefore, when the UHS-I feature is used, adding a transciever is recommended. Also, the SDMMC has its own IDMA to transfer data in the linked list configuration.

Table 3. SDMMC main features   

<table><tr><td rowspan=1 colspan=1>Feature</td><td rowspan=1 colspan=1>SDMMC1</td><td rowspan=1 colspan=1>SDMMC2</td></tr><tr><td rowspan=1 colspan=1>Master interface</td><td rowspan=1 colspan=1>Connected to the 64-bit AXI bus matrix</td><td rowspan=1 colspan=1>Connected to the 32-bit AHB bus matrix</td></tr><tr><td rowspan=1 colspan=1>Slave interface</td><td rowspan=1 colspan=1>Operates on the AHB5 bus</td><td rowspan=1 colspan=1>Operates on the AHB2 bus</td></tr><tr><td rowspan=1 colspan=1>Memory access</td><td rowspan=1 colspan=1>AXI SRAMFlashXSPIFMC</td><td rowspan=1 colspan=1>AXI SRAMBackup RAMSRAM1, SRAM2FlashXSPIFMC</td></tr><tr><td rowspan=1 colspan=1>SDMMC delay block</td><td rowspan=1 colspan=1>Operates on the AHB5 bus</td><td rowspan=1 colspan=1>Operates on the AHB2 bus</td></tr><tr><td rowspan=1 colspan=1>UHS-I</td><td rowspan=1 colspan=1>Generates control signals to control theexternal voltage switch transceiver</td><td rowspan=1 colspan=1>No control signal generation for externaltransceiver</td></tr></table>

# 1.3

# SDMMC host-interface block diagram

This section presents the SDMMC block diagram. The SDMMC internal input/output signals table and the SDMMC are described in the tables following the figure.

![](images/03b468885c809602578c312d5f4d003dba8178572d1d3accb564a95dcd67d2b3.jpg)  
Figure 6. SDMMC block diagram

Table 4. SDMMC internal input/output signals   

<table><tr><td rowspan=1 colspan=1>Signal name</td><td rowspan=1 colspan=1>Signal type</td><td rowspan=1 colspan=1>Description</td></tr><tr><td rowspan=1 colspan=1>Sdmmc_ker_ck</td><td rowspan=1 colspan=1>Digital input</td><td rowspan=1 colspan=1>SDMMC kernel clock</td></tr><tr><td rowspan=1 colspan=1>Sdmmc_hclk</td><td rowspan=1 colspan=1>Digital input</td><td rowspan=1 colspan=1>AHB clock</td></tr><tr><td rowspan=1 colspan=1>Sdmmc_it</td><td rowspan=1 colspan=1>Digital output</td><td rowspan=1 colspan=1>SDMMC global output</td></tr><tr><td rowspan=1 colspan=1>Sdmmc_dataend_trg</td><td rowspan=1 colspan=1>Digital output</td><td rowspan=1 colspan=1>SDMMC data end trigger</td></tr><tr><td rowspan=1 colspan=1>Sdmmc_rx_ck</td><td rowspan=1 colspan=1>Digital input</td><td rowspan=1 colspan=1>Selected clock for received data andresponses</td></tr><tr><td rowspan=1 colspan=1>Sdmmc_io_in_ck</td><td rowspan=1 colspan=1>Digital input</td><td rowspan=1 colspan=1>Feedback clock Internally connected toSDMMC_CK</td></tr><tr><td rowspan=1 colspan=1>Sdmmc_fb_ck</td><td rowspan=1 colspan=1>Digital input</td><td rowspan=1 colspan=1>Feedback clock from the delay block(DLYB)</td></tr></table>

Table 5. SDMMC pins   

<table><tr><td colspan="1" rowspan="1">Signal name</td><td colspan="1" rowspan="1">Signal type</td><td colspan="1" rowspan="1">Description</td></tr><tr><td colspan="1" rowspan="1">SDMMC_DODIR</td><td colspan="1" rowspan="1">Digital output</td><td colspan="1" rowspan="1">Indicates the direction of SDMMC_D0signal</td></tr><tr><td colspan="1" rowspan="1">SDMMC_D123DIR</td><td colspan="1" rowspan="1">Digital output</td><td colspan="1" rowspan="1">Indicates the direction ofSDMMC_D[1:3] signals</td></tr><tr><td colspan="1" rowspan="1">SDMMC_CDIR</td><td colspan="1" rowspan="1">Digital output</td><td colspan="1" rowspan="1">Indicates the direction of SDMMC_CMDsignal</td></tr><tr><td colspan="1" rowspan="1">SDMMC_CK</td><td colspan="1" rowspan="1">Digital output</td><td colspan="1" rowspan="1">Clock for the SD/SDIO/MMC card</td></tr><tr><td colspan="1" rowspan="1">SDMMC_CKIN</td><td colspan="1" rowspan="1">Digital input</td><td colspan="1" rowspan="1">Feedback clock from the externalvoltage transceiver</td></tr><tr><td colspan="1" rowspan="1">SDMMC_CMD</td><td colspan="1" rowspan="1">Digital input/output</td><td colspan="1" rowspan="1">Command and response line</td></tr><tr><td colspan="1" rowspan="1">SDMMC_D [7:0]</td><td colspan="1" rowspan="1">Digital input/output</td><td colspan="1" rowspan="1">Data transmission lines</td></tr></table>

The SMMC host interace contans two mai inteaces: he adapter interface and heAHB interacThe interfaces are described in the following sections.

# Adapter interface

The Adapater interface uses the smmc_kerckdomain and provides connection between he external cardand the AHB interface. This interface contains:

# Control unit

It groups the power management functions and the clock management with dividers. It generates the control signals for the external voltage switch transceiver.

Command/response path units

They transfer command and responses signals on the SDMmc_cMD line. The command path is clocked by the SDMMc_cK and the response path is clocked by the sdmmc_rx_ck.

# Data receive/transmit path units

They transfer data on the SDMMC_D [7:0] lines. The transmit data is clocked by the SDMMc_CK and the receive data is clocked by the sdmmc_rx_ck.

# CLK MUX unit

It selects the source clock for the response path and the data receive path.

# 1.3.2

# AHB interface

Thisinteraceuss he Mchclk omanontais he AHB slaveinterface nd heAHBmasteint.

# AHB slave interface

Provides access to the SDMC registers and the FO also generates the interrupt requests.The IFO size is 32-bit wide, 16 words deep.

# • AHB master interface

Contains the internal direct memory access (IDMA) to provide high-speed data transfer between the FIFO and the memory.

# IDMA (internal direct memory access)

The SDMMC have its own IDMA, which can be configured over the SDMMC registers. The IDMA provides highspeed data transfer between the FIFO and the memory. It supports the following features:

Burst transfer of 8 beats   
Easy configuration through the SDMMC registers   
Difeent modesperatio:Sglebufertransr Double-buffertransferlinked-istmode deendg on feature availability).

In single-buffer configuration, the IDMA access one base address and starts the data transfer.

Inubluaarn to process the first data buffer while the IDMA is accessing the second memory buffer.

![](images/62bbc18a1abdc41cee4504531c0972a264348eb6e2d9ce6fd5dc9a802f991d70.jpg)  
Figure 7. IDMA single-buffer and double-buffer channel modes

In kguratiTekcnguratio ro a SDMMC registers. When the IDMA has finished transferring allthe first node data (indicated in IDMABSIZE), ardng MAMOE=a wheneikemL  DMA loadsheke when all data are transferred (according to DATALENGHT).

The linked list content and IDMA behavior are shown in following figure.

![](images/1f0fa2a26d0772cd64977f2bcd4c92c630abfaca7ac42e18bbafac1e35ddc6dc.jpg)  
Figure 8. Linked list content and IDMA behavior

# 1.4

# SDMMC host-interface differences between STM32F7 Series and STM32H7 Series

The new SDMMC interface embedded within the STM32H7 Series enhances the SDMMC host capabilities compared to the previous version of the peripheral embedded in the STM32F7 Series.

The following table contains the main differences between the SDMMC in STM32F7 Series and the SDMMCin STM32H7 Series.

Table 6. SDMMC differences between STM32F7 Series and STM32H7 Series   

<table><tr><td rowspan=1 colspan=1>SDMMC feature(1)</td><td rowspan=1 colspan=1>STM32F7 Series</td><td rowspan=1 colspan=1>STM32H7 Series</td></tr><tr><td rowspan=1 colspan=1>Compatibility version</td><td rowspan=1 colspan=1>SD(2.0) / MMC(4.2) / SDIO(2.0)</td><td rowspan=1 colspan=1>SD(4.1) / MMC(4.51) / SDIO(4.0)</td></tr><tr><td rowspan=1 colspan=1>Data transfer clock frequency</td><td rowspan=1 colspan=1>0-50 MHz (for 3.3 V)</td><td rowspan=1 colspan=1>0-50 MHz (for 3.3 V)0-208 MHz (for 1.8 V)</td></tr><tr><td rowspan=1 colspan=1>Operating buses</td><td rowspan=1 colspan=1>Slave interface: 32-bit APB bus</td><td rowspan=1 colspan=1>Slave interface: 32-bit AHB busMaster interface: 32-bit AHB bus</td></tr><tr><td rowspan=1 colspan=1>DMA transfer</td><td rowspan=1 colspan=1>Request an external DMA (DMA2)Bust of 4 bits</td><td rowspan=1 colspan=1>Supports an internal DMA burst</td></tr><tr><td rowspan=1 colspan=1>Supported speed modes for SD andSDIO cards</td><td rowspan=1 colspan=1>Default speed / high speed (3.3 V)UHS-I not supported</td><td rowspan=1 colspan=1>Default speed / high speed (3.3 V)UHS-I modes: : SDR12 / SDR25 /SDR50 /DDR50 / SDR104</td></tr><tr><td rowspan=1 colspan=1>Supported speed modes for MMC cards</td><td rowspan=1 colspan=1>Legacy compatibleHigh speed SDR</td><td rowspan=1 colspan=1>Legacy compatibleHigh speed SDRHigh speed DDRHigh speed HS200</td></tr><tr><td rowspan=1 colspan=1>Boot operation</td><td rowspan=1 colspan=1>Supports only alternative boot</td><td rowspan=1 colspan=1>Supports normal boot and alternativeboot</td></tr><tr><td rowspan=1 colspan=1>DLYB</td><td rowspan=1 colspan=1>Not available</td><td rowspan=1 colspan=1>Available</td></tr><tr><td rowspan=1 colspan=1>MDMA features</td><td rowspan=1 colspan=1>Not available</td><td rowspan=1 colspan=1>Available</td></tr></table>

1. Maximum frequency depends on the maximum allowed IO speed.

# SDMMC host interface initialization with SD and MMC cards

# 2.1

# Initiate SDMMC host interface configuration using STM32CubeMx

This section presents an example on how to configure the SDMMC using the STM32CubeMx tool. Using the STM32CubeMX tool is a very simple, easy and rapid way to configure the SDMMC peripheral and its GPIOs as it permits the generation of a project with preconfigured SDMMC.

# 2.1.1

# SDMMC host interface GPIO configuration using STM32CubeMX

O heT32CubeMX projec iscreated in the peripheral categoris, eleccoectiviy and then n Cstances available figur belowshows how elect  MCardware configuration wi STM32CubeMX.

![](images/7739f4577f64e793c86e41b0288fb492e2fd531603a6761bed799c04e27c143b.jpg)  
Figure 9. SDMMC pins configuration with STM32CubeMX

The user can chose between SDMMC1 and SDMMC2. The user selects the configuration mode depending on the desired application and below configurations are available:

Type of card: SD/SDIO/MMC card   
Bus width: 1-bit, 4-bit, 8-bit mode   
External transceiver: enable/disable command signals for external transceiver.

# 2.1.2

# SDMMC host interface clock configuration using STM32CubeMx

The first step is to select the source clock for the sdmmc_ker_ck as show in the figure belov

![](images/d52122e5a80501f77bda90695e77b22bd42fcc46ef1aa07a0c9e7a1bbabf682e.jpg)  
Figure 10. sdmmc_ker_ck configuration with STM32CubeMx

In the cloc configuratin panel the user can select he sour clockor themc_kerck1and smc_ker_ck2 either from DIVQ1or DIVR2. A dedicated Mux is available to select SDMMC1 and SDMMC2 kernel clock source from PLL1Q or PLL2R output:

![](images/6f5e4fde3db9caada36a6221837f25d7ba803987ea2cb3bbe52c563c322ad87e.jpg)  
Figure 11. sdmmc_ker_ck source clock selection with STM32CubeMx

# 2.1.3

# SDMMC host interface parameters configuration using STM32CubeMx

Te fs e  o  he paramr ettis,hee we n select e parar

Select the clock edge Enable the Power-save mode (disable the clock when the SDMMC is in idle state and there is no data or command transfer) Enable or disable the hardware flow control refer to SectinSDMC host interfaceand hardware flow control) • Select the divide factor for the SDMMC_CK (SDMMC_CK = sdmmc_ker_ck / [CLKDIV\*2])

![](images/7efc97253fa8c47d7c80598914988f6bb2ea3d285dfee4f95a6e3019fbcf72bc.jpg)  
Figure 12. SDMMC parameters configuration with STM32CubeMx

In the NVIC Settings tab, the user enables the SDMMC global interrupt (see figure below).

![](images/37053553373a95e146714c2ffcc1ee5b8e22fd77f4afc897f1bb7179a56fd2d5.jpg)  
Figure 13. SDMMC global interrupt configuration with STM32CubeMx

File sytemmidleware can be added in the project configuration. For example the FAF can be seleced as shown in the next figure:

![](images/ad3c8246cc8a53e270599418deb9cf955e991384acc9b277793caf107715f430.jpg)  
Figure 14. SDMMC FATFS configuration with STM32CubeMx

Finall, in order configure the MDMA end ofdata transfer triggerfrom the DMMC,he user select the MDMA in the System configuration section.

Onc thedialog box is open, the userclicks on the Ad a chanelbutton and select MCend ofdat. Now theuser can configurethe MDMA for thedata transer (buffertranser length,data aligment, sour nd destination). See the figure below for an example f the dialog boxes that the user finds when doing this configuration.

![](images/5997d6e3197d4ac8c8bbc94070f632840179dae520bdb44ddb4253faf43205f4.jpg)  
Figure 15. MDMA end of data configuration with STM32CubeMx

# 2.2

# Initiate SDMMC host interface configuration

Thi sectin preents examplen how itte heChos interacentil e can pa ata path are ready to initiate the SD card or the MMC card. See a synopsis on the process below:

![](images/dd37b848c8273d22f400a9f891442b5a57763d71c3acfe480c940cbbc6ba82e8.jpg)  
Figure 16. Synoptic diagram of SDMMC initialization

# Clock configuration

The RCC registers should be configured to select the clock for sdmmc_ker_ck and SDMMC_hclk.

The figure below illustrates two source clocks for sdmmc_ker_ck for both sdmmc1 and sdmmc2.

![](images/68e7304079ea89b51da709570ca68f8f7db9f606e078eb4b07e19fe09ddf6f1b.jpg)  
Figure 17. Source clock for sdmmc1/2_ker_ck

With a duty cycle close to 50%, the DIV[P/Q/R]x values shall be even.

or SDMMCx, the duty cycle shall be 50% when supporting DDR.

The configuration of the AHB3/2 clock domain to select the SDMMC_hclk must be done and should respect the Following relation: SDMMC_hclk > (3x bus width / 32) x SDMMC_CK).

The clock configuration is now completed, sdmmc_ker_ck and SDMMC_hclk are configured but they are not enabled.

# External transceiver selection (if needed)

This configuration is optional, and it is needed when using UHS- modes. The external transceiver must be selected. A GPIO pin should be configured as digital output and the transceiver must be selected.

# SDMMC GPIO configuration

The SMC GIO pins or shall beconfigured or coand, ata, cock and ineeded r the control sials to the external transceiver. Refer to the specific device's datasheet for SDMMC GPIO configuration.

# SDMMC RCC enable

The RCC registers shall be configured to enable the clock for SDMMC1 or SDMMC2, this action enables both sdmmc_ker_ck and sdmmc_hclk for the selected peripheral.

# SDMMC power cycle

I z manual for more information on how to perform a power cycle sequence.

# SDMMC power off

SDMMC disabled and SDMMC signals drive "1"

# SDMMC initial configuration

When using the external transceiver the direction signal polarity must be set as high. For the SDMMC initial configuration, the SDMMC_CK must be in the range of 100 to 400 KHz, the DDR mode and the bus speed must be disabled.

# SDMMC power on

The power on of the SDMMC, must be set. Once it is done, the SDMMC is ready for card initialization.

# 2.3

# SD card initialization

# 2.3.1

# SD power on and initialization

The SD card power on and initialization process is illustrated in the following flow chart:

![](images/fd8d9013a4714254be5c4ebfda5b56be7187bd3c341cbb18c3cd8bd4afbdcfe0.jpg)  
Figure 18. SD card power on and initialization diagram

The user checks the card version and very if the card supports UHS-and  an external voltage switch ave or e serarheolageu nde hecar see  R l optional and it depends on user application.

# Check the card version and voltage

The host sends CMD8, and depending on the result:

If the card returns a response, it means that it is version 2.00 or later If the response is not valid, it means that the voltage range is not compatible If the response is valid, it means that the card voltage range is compatible   
Isou e ha 0 a wiivl   
a version 1.X SD card or not an SD card.

# Does the card supports UHS-I?

To check if the card support UHS- the host sends ACMD1 repetitively and checks the response. If the card support U-I the host needs to check n external tranceiver is spportd then start hevoltageich sequence.

# Voltage switch sequence

The host needs to enable the voltage switch from SDMMC registers for the voltage switch sequence.

Before sending CMD11 check the SDMMC_CK. If it stopped and then busy signal = asserted. If done, enable the external transceiver, otherwise the SD card do not support that feature.   
Wait orevoltswi rtal ti ecn cpletion ehen heck eu l.   
done, the voltage switch succeeded and the SD card speed is set to SDR12, otherwise it failed.   
Clear the voltage switch flag and the status flags.

# Card initialization

Send CMD2 to get all cards unique identification number.   
Send CMD3 to set the related card address (RCA).   
Send CMD9 to get the cards specific data (CSD).

# 2.3.2

# Configure the wide bus operation for SD card

The flowchart below presents the synoptic diagram of the SD card bus wide configuration.

![](images/07ef8366edb7fa427ca74fc731148af93bab61063651cd83d63910c84e970341.jpg)  
Figure 19. SD card bus wide configuration diagram

CMD6 is not supported by SD cards version 1.01.

The detailed steps to configure the wide bus operation are the following:

Send ACMD6 then configure the SDMMC to switch the bus wide for 1-it mode or 4-bit mode (the1-it mode is not supported with UHS-I speeds).   
Se hecoc egesln rMCC >0 MHz  vi    clocege  ll.   
3Enable or disable the hardware flow control.   
Sd CMD, hecard returns he contai 6-ytda  he car suprts hat speed mode t switches to the selected speed mode (if supported).

Table 7. CMD6 data pattern for speed mode selection   

<table><tr><td rowspan=1 colspan=1>Card operating speed after voltage switch sequence(succeed or failed)</td><td rowspan=1 colspan=1>CMD6 argument for the selected speed mode</td></tr><tr><td rowspan=1 colspan=1>DS , SDR12</td><td rowspan=1 colspan=1>0x80FF FF00</td></tr><tr><td rowspan=1 colspan=1>HS,SDR25</td><td rowspan=1 colspan=1>0x80FF FF01</td></tr><tr><td rowspan=1 colspan=1>SDR50</td><td rowspan=1 colspan=1>0x80FF FF02</td></tr><tr><td rowspan=1 colspan=1>SDR104</td><td rowspan=1 colspan=1>0x80FF FF03</td></tr><tr><td rowspan=1 colspan=1>DDR50</td><td rowspan=1 colspan=1>0x80FF FF04</td></tr></table>

DDR mode, Bus speed mode and ClockDiv mode must be configured after sending CMD6 because the SD card switches to the selected speed mode after sending the 64-bytes of data. Changing the clock and bus mode before sending the command may generate a data read error.

Configure the DLYB (if needed) using CMD19 for tuning.

Configure the PWRSAV bit. PWRSAV bit stops the clock when the CPSM and DPSM are in Idle state (no coandor datatranser over he bus). nabling WRAV bit befoecnfiguring he Lcauses aero because the SDMMC_CK is stopped.

# Example of CMD6 switch with SDR104:

errorstate = SDMMC_CmdSwitch(hsd->Instance, SDMMC_SDR104_SWITCH_PATTERN); if(errorstate != HAL_OK) return errorstate; }

# 2.4

# MMC card initialization

# 2.4.1

# MMC power on and initialization

Find below the synoptic diagram of the MMC card initialization:

![](images/4b890ef12ed01efa0cd3ada81a17b1555a4b6bde863a26bd424a175b4b76981d.jpg)  
Figure 20. Synoptic diagram of MMC initialization

# Check the card operating voltage

Put the MMC card into idle state by sending CMDO.   
2Check if the card operating voltage matches by sending CMD1.

# Card initialization

1Send CMD2 to get all cards unique identification number.   
Send CMD3 to set the related card address (RCA).   
3. Send CMD9 to get the card the card specific data (CSD).   
4Send CMD13 to check if card is ready.   
Send CMD8 to get the extended card specific data (EXTCSD).

# 2.4.2

# Configure the wide bus operation for MMC card

The flowchart below presents the synoptic diagram of the MMC card bus wide configuration.

![](images/9abffdc47aabcfa36ab9b6b8cb69175820c767cf8ce3c1a392c04ad613d7ddcc.jpg)  
Figure 21. MMC card bus wide configuration diagram

The detailed steps to configure the wide bus operation are the following:

Send CMD6 to select the speed mode (LC, HS or HS200) and wait until the card is ready using CMD13.

Table 8. CMD6 data pattern for speed mode selection   

<table><tr><td rowspan=1 colspan=1>Card operating speed after voltage switch sequence(succeed or failed)</td><td rowspan=1 colspan=1>CMD6 argument for the selected speed mode</td></tr><tr><td rowspan=1 colspan=1>Legacy compatible</td><td rowspan=1 colspan=1>0x03B9 0000</td></tr><tr><td rowspan=1 colspan=1>HS SDR / HS DDR</td><td rowspan=1 colspan=1>0x03B9 0100</td></tr><tr><td rowspan=1 colspan=1>HS200</td><td rowspan=1 colspan=1>0x03B9 0200</td></tr></table>

Send CMD6 to select the bus wide (1-bit, 4-bit, 8-bit) and wait until the card is ready.

Table 9. CMD6 data pattern for speed mode selection   

<table><tr><td rowspan=1 colspan=1>Bus wide</td><td rowspan=1 colspan=1>CMD6 argument for the selected bus wide</td></tr><tr><td rowspan=1 colspan=1>1-bit data bus</td><td rowspan=1 colspan=1>0x03B7 0000</td></tr><tr><td rowspan=1 colspan=1>4-bit data bus</td><td rowspan=1 colspan=1>0x03B7 0100</td></tr><tr><td rowspan=1 colspan=1>8-bit data bus</td><td rowspan=1 colspan=1>0x03B7 0200</td></tr><tr><td rowspan=1 colspan=1>4-bit data bus (HS DDR)</td><td rowspan=1 colspan=1>0x03B7 0500</td></tr><tr><td rowspan=1 colspan=1>8-bit data bus (HS DDR)</td><td rowspan=1 colspan=1>0x03B7 0800</td></tr></table>

Configure the SDMMC registers to select:

The clock edge: rising or falling.   
Power save: enable or disable.   
Bis width: 1-bit, 4-bit or 8-bit.   
Hardware flow control: enable or disable.   
CLK div.   
Bus speed: enable or disable.   
DDR mode: enable or disable.

Now the card is ready for data transfer operations.

# How to read / write with SDMMC host interface in single / multiple block(s) mode

Teo .

![](images/c2551f36c00813904d19ef5539c8a164a0afb30402fcad0b72a507e5c1f16826.jpg)  
Figure 22. Data transfer initialization

![](images/1b230f3f0fa142622f012629f4097cb3d06e19ffdbf19e0fc1136708233047d6.jpg)  
Figure 23. Read/write block(s) commands

The following commands are used for read/write multiple/single block

CMD17: read single block.   
CMD18: read multiple blocks.   
CMD23: write single block.   
CMD24: write multiple blocks.

# 3.1

# Interrupt mod

The read/write flow in Interrupt mode is illustrated below.

![](images/2a0937f6f291ff339c369069b4aeca0510003521915c2c01c4cbdb8348582bef.jpg)  
Figure 24. Read/write data in Interrupt mode

# Reading in Interrupt mode

Send the block size to the card using CFinMD16 then configure the SDMMC registers for data transfer:

Set the data timeout.   
Set the data length.   
Set the data block size.   
Configure the data transfer direction (from SD/MMC card to host).   
Configure the data transfer mode block(s).   
Enable the DPSM.

Send the Read-command block(s) then enable the interrupts listed in the following table:

Table 10. Interrupts to enable to read in Interrupt mode   

<table><tr><td rowspan=1 colspan=1>SDMMC interrupts enabled</td><td rowspan=1 colspan=1>Description</td></tr><tr><td rowspan=1 colspan=1>DCRCFAIL</td><td rowspan=1 colspan=1>Data CRC check failed</td></tr><tr><td rowspan=1 colspan=1>DTIMEOUT</td><td rowspan=1 colspan=1>Data timeout</td></tr><tr><td rowspan=1 colspan=1>RXOVERR</td><td rowspan=1 colspan=1>Received FIFO overrun</td></tr><tr><td rowspan=1 colspan=1>DATAEND</td><td rowspan=1 colspan=1>Successful end of data transfer</td></tr><tr><td rowspan=1 colspan=1>RXFIFOHF</td><td rowspan=1 colspan=1>Received FIFO half full</td></tr></table>

# Writing in Interrupt mode

1Enable the interrupts listed in the following table:

Table 11. Interrupts to enable to write in Interrupt mode   

<table><tr><td rowspan=1 colspan=1>SDMMC interrupts enabled</td><td rowspan=1 colspan=1>Description</td></tr><tr><td rowspan=1 colspan=1>DCRCFAIL</td><td rowspan=1 colspan=1>Data CRC check failed</td></tr><tr><td rowspan=1 colspan=1>DTIMEOUT</td><td rowspan=1 colspan=1>Data timeout</td></tr><tr><td rowspan=1 colspan=1>TXUNDERR</td><td rowspan=1 colspan=1>Transfer FIFO underrun</td></tr><tr><td rowspan=1 colspan=1>DATAEND</td><td rowspan=1 colspan=1>Successful end of data transfer</td></tr><tr><td rowspan=1 colspan=1>RXFIFOHF</td><td rowspan=1 colspan=1>Transfer FIFO half empty</td></tr></table>

2Send block size to the card using CMD16 then send the Write-command block(s).

Configure the SDMMC registers for data transfer:

Set the data timeout.   
Set the data length.   
Set the data block size.   
Configure the data transfer direction (from host to SD/MMC card).   
Configure the data transfer mode block(s).   
Enable the DPSM.

# SDMMC IRQ handler

T Rr a Fve FOaphal fuctons manages heatredwrierors.Alst n hedattransecanCMf successful read or write.

# 3.2

# DMA Single-buffer mode

The read/write flow in DMA Single-buffer mode is illustrated below.

![](images/2f29a7ea318d7340ff6b72225826a92ece163bbc7d8802d5ea5ae858ef117ba9.jpg)  
Figure 25. Read/write data in DMA Single-buffer mode

# Reading in DMA Single-buffer mode

Configure the SDMMC registers for data transfer:

Set the data timeout.   
Set the data length.   
Set the data block size.   
Configure the data transfer direction (from SD/MMC card to host).   
Configure the data transfer mode block(s).   
Disable the DPSM.

Send the block size to the card using CMD16 then enable the interrupts listed in the following table:

Table 12. Interrupts to enable to read in DMA Single-buffer mode   

<table><tr><td rowspan=1 colspan=1>SDMMC interrupts enabled</td><td rowspan=1 colspan=1>Description</td></tr><tr><td rowspan=1 colspan=1>DCRCFAIL</td><td rowspan=1 colspan=1>Data CRC check failed</td></tr><tr><td rowspan=1 colspan=1>DTIMEOUT</td><td rowspan=1 colspan=1>Data timeout</td></tr><tr><td rowspan=1 colspan=1>RXOVERR</td><td rowspan=1 colspan=1>Received FIFO overrun</td></tr><tr><td rowspan=1 colspan=1>DATAEND</td><td rowspan=1 colspan=1>Successful en dof data transfer</td></tr></table>

Enable CMDTRANS.The CPSM treats the command as a data transfer command, stops the interrupt period and signals data enable to the DPSM.

Configure he DMMC registers  et he buffer base address or he IDMA and enable he IDMA as Sigle buffer mode.

Send the read command block(s).

# Writing in DMA Single-buffer mode

Send block size to the card using CMD16 then configure the SDMMC registers for data transfer:

Set the data timeout.   
Set the data length.   
Set the data block size.   
Configure the data transfer direction (from host to SD/MMC card).   
Configure the data transfer mode block(s).   
Disable the DPSM.

Enable the interrupts listed in the following table:

Table 13. Interrupts to enable to write in DMA Single-buffer mode   

<table><tr><td rowspan=1 colspan=1>SDMMC interrupts enabled</td><td rowspan=1 colspan=1>Description</td></tr><tr><td rowspan=1 colspan=1>DCRCFAIL</td><td rowspan=1 colspan=1>Data CRC check failed</td></tr><tr><td rowspan=1 colspan=1>DTIMEOUT</td><td rowspan=1 colspan=1>Data timeout</td></tr><tr><td rowspan=1 colspan=1>TXUNDERR</td><td rowspan=1 colspan=1>Transfer FIFO underrun</td></tr><tr><td rowspan=1 colspan=1>DATAEND</td><td rowspan=1 colspan=1>Successful end of data transfer</td></tr></table>

# 3Enable CMDTRANS.

onfigure he SDMMC egisters  et he buffer base address or he IDMA an enable he IDMA as Singlebuffer mode.   
Send the write command block(s).

# SDMMC IRQ handler

The IRQhandercalls he albackctns andmanages he dataread/wri errors. Ilo sendshe data transfer command CMD12 after successful read or write.

# 3.3

# DMA Double-buffer mode

The read/write flow in DMA Double-buffer mode is illustrated below.

![](images/3d0f8f409a96b971b69be6901bd1ab2b8a19ac2f0e16894c1a431dddfb2654ba.jpg)  
Figure 26. Read/write data in DMA Double-buffer mode

# Reading DMA Double-buffer mode

Configure the SDMMC register for data transfer:

Set the data timeout.   
Set the data length.   
Set the data block size.   
Configure the data transfer direction (from SD/MMC card to host).   
Configure the data transfer mode block(s).   
Disable the DPSM.

Send block size to the card using CMD16.

3Enable CMDTRANS.

Configure the SDMMC register to enable the IDMA as Double-buffer mode.

5Enable the interrupts listed in the following table:

Table 14. Interrupts to enable to read in DMA Double-buffer mode   

<table><tr><td rowspan=1 colspan=1>SDMMC interrupts enabled</td><td rowspan=1 colspan=1>Description</td></tr><tr><td rowspan=1 colspan=1>DCRCFAIL</td><td rowspan=1 colspan=1>Data CRC check failed</td></tr><tr><td rowspan=1 colspan=1>DTIMEOUT</td><td rowspan=1 colspan=1>Data timeout</td></tr><tr><td rowspan=1 colspan=1>RXOVERR</td><td rowspan=1 colspan=1>Received FIFO overrun</td></tr><tr><td rowspan=1 colspan=1>DATAEND</td><td rowspan=1 colspan=1>Successful end of data transfer</td></tr><tr><td rowspan=1 colspan=1>IDMATE</td><td rowspan=1 colspan=1>IDMA transfer error</td></tr><tr><td rowspan=1 colspan=1>IDMABTC</td><td rowspan=1 colspan=1>IDMA buffer transfer complete</td></tr></table>

# Send the read command block(s).

# Writing in DMA Double-buffer mode

Send block size to the card using CMD16.

Configure the SDMMC registers for data transfer:

Set the data timeout.   
Set the data length.   
Set the data block size.   
Configure the data transfer direction (from host to SD/MMC card).   
Configure the data transfer mode block(s).   
Disable the DPSM.

3Enable CMDTRANS.

4Configure the SDMMC registers to enable the IDMA as Double-buffer mode.

5Enable the interrupts listed in the following table:

Table 15. Interrupts to enable to write in DMA Double-buffer mode   

<table><tr><td rowspan=1 colspan=1>SDMMC interrupts enabled</td><td rowspan=1 colspan=1>Description</td></tr><tr><td rowspan=1 colspan=1>DCRCFAIL</td><td rowspan=1 colspan=1>Data CRC check failed</td></tr><tr><td rowspan=1 colspan=1>DTIMEOUT</td><td rowspan=1 colspan=1>Data timeout</td></tr><tr><td rowspan=1 colspan=1>TXUNDERR</td><td rowspan=1 colspan=1>Transfer FIFO underrun</td></tr><tr><td rowspan=1 colspan=1>DATAEND</td><td rowspan=1 colspan=1>Successful end of data transfer</td></tr><tr><td rowspan=1 colspan=1>IDMATE</td><td rowspan=1 colspan=1>IDMA transfer error</td></tr><tr><td rowspan=1 colspan=1>IDMABTC</td><td rowspan=1 colspan=1>IDMA buffer transfer complete</td></tr></table>

Send the write command block(s).

# SDMMC IRQ handler

Th IRQande l hecallbaccins admaaes he at rd/wrierrors. I also sends he data transfer command CMD12 after successful read or write.

TultaAublulM IDMA Double-buffer mode. The full application example is available in STM32Cube_FW_H7_V1.2.0

![](images/863c58c2511fdf96c93b5336fc97b0908ccc235a6870c4b502f9d5be22f6513a.jpg)  
Figure 27. IDMA Double-buffer mode example

# 3.4

# IDMA Linked List mode

I locut SDMMCar sllo terconiguratinshatadaptvaryig dat izes antyesas wel aseducing heU ladRee Section 1.3.2: AHB interface for more details.

The read/write in IDMA Linked List mode is simplified in the steps below:

1SDMMC initialization   
2. Linked list node creation   
3. Set the IDMABASER and IDMABSIZE registers for write/read address range operation   
4. Initialize the DCTRL register   
5. Configure the SD DPSM   
6. Initiate read/write Multi Block command   
7Enable SDMMC interrupts

Table 16. Interrupts to enable to write in IDMA Linked list mode   

<table><tr><td colspan="1" rowspan="1">SDMMCinterrupts enabled</td><td colspan="1" rowspan="1">Description</td></tr><tr><td colspan="1" rowspan="1">DCRCFAIL</td><td colspan="1" rowspan="1">CRC error inthe received data during a read or write operation</td></tr><tr><td colspan="1" rowspan="1">DTIMEOUT</td><td colspan="1" rowspan="1">Timeout error duringdata transfer</td></tr><tr><td colspan="1" rowspan="1">TXUNDERR</td><td colspan="1" rowspan="1">Buffer underrun duringdata transmission</td></tr><tr><td colspan="1" rowspan="1">RXOVERR</td><td colspan="1" rowspan="1">Buffer overrun duringdata reception</td></tr><tr><td colspan="1" rowspan="1">DATAEND</td><td colspan="1" rowspan="1">End of data transfer</td></tr><tr><td colspan="1" rowspan="1">IDMABTC</td><td colspan="1" rowspan="1">Completion of abuffer transfer in IDMA mode</td></tr></table>

# How to read/write with SDMMC host interface using file system FATFS

Data can be transferred from SD card using file system FATFS in Polling, Interrupt and DMA modes. The following example (available in STM32CubeFW_H7) describes how to create, write and then read a text document in DMA Single-buffer mode with SDMMC on STM32H743I-EVAL board.

# Imported project files for file system management with SDMMC

Inapn erojec   ne the configuration.

![](images/b4ca7c59bc9a77aee45d69bc593439bb4e5dc5538b18989ffb62fca27f7054fb.jpg)  
Figure 28. Middleware files tree

The middleware files contain the FATFS files diskio.c, ff.c and ff_gen_drv.c; and the driver file sd_diskio_dma.c .

The user can chose the data transfer mode (Interrupt, DMA, and Polling) by modifying or changing the diskma.. Itnts eis r izatin,ad wricallmB .

![](images/e2c0745138a40fcbd2026403a30f69d0a15a7fe96cc6b8dbfc7fc08fec305998.jpg)  
Figure 29. BSP files tree

The user needs to select the BSP files depending on the board (as an example here the STM32H743l-EVAL brheSfcntai ncee anage he I ps.User can alointegrate BS files.

# 4.2

# File system exampl

The following chart illustrates the description of a file system example.

![](images/53b5f1d069985131aaada0ef0b7386ebab9948eb90402d6dec65e28a671be079.jpg)  
Figure 30. File system example

# SDMMC host interface and hardware flow control

Teara onol al av Oden Xmoenver RXmo. The SDMMC_hclk must respect the following relation:

SDMMC_hclk > (3x bus width / 32) x SDMMC_CK).

Whe enablig hearware fow control,Cclk can e slihty euc, is actn dsot c data error but it reducse the SDMMC data speed transfer.

As an example of transferring data in DMA mode with CPU clock frequency = SDMMC_hclk = 37.5 MHz, when enabling the hardware flow control the clock frequency can reach SDMMC_hclk = 20 MHz but the data speed transfer is reduced by 33%.

# Note:

Hardware flow control shall only be used when the SDMMC_Dn data is cycle-aligned with the SDMMC_CK. Whenever the sdmmc b_ck from the DLYB delay block is used (such as in the case of SDR104 mode with a d o dlaycyc,harware o cntrol can not sRer he evic'ataheet information.

# 6 How to enable the DLYB

# DLYB enabling use case presentation

TDLsteplg clocheeaWheneg e read error may be prevented by enabling the DLYB.

# DLYB enabling use case configuration

The DLYB can be configured with two different methods; each method has its own advantages compared to the other.

Without tuning command: the advantage is that it take less time to be configured.

With tuning command: the advantage is that there are less chances to face a data transfer error.

# DLYB configuration without tuning command

TuDLYB i ele LY a coc t coc hea delay block. See an example below:

/\*select the DLYB feedback clock as input clock\*/ MODIFY_REG(hsd->Instance->CLKCR, SDMMC_CLKCR_SELCLKRX, SDMMC_CLKCR_SELCLKRX_1); /\*Enable the DLYB\*/ DelayBlock_Enable(DLYB_SDMMC1);

The following diagram shows the steps to enable the delay block function:

![](images/fa258f243e00e2310e608f0bf3dd6a5625d6e70c2c7f61ed8578320f897c47c9.jpg)  
Figure 31. Delay block configuration

# 6.2.2

# DLYB configuration with tuning command

See below an example on how to configure DLYB with tuning command:

uint32_t sel=0; 7\*select the DLYB feedback clock as input clock\*/ MODIFY_REG(hsd->Instance->CLKCR, SDMMC_CLKCR_SELCLKRX, SDMMC_CLKCR_SELCLKRX_1   
\*SDMMC_CLKCR_SELCLKRX_1\*/); 7\*Enable DLYB with sel = 0 and start tuning proceedure.repeat with updating the value   
of sel until sel = 13 or tuning succeeded \*/ while (sel!=13) { DelayBlock_Enable(DLYB_SDMMC1,sel); errorstate = tuning(hsd); if(errorstate == HAL_OK) { return errorstate; sel++; /\* in case tuning didnt succeed with each selected phase (sel = 13) disable dlyb and   
select the SDMMC_CKIN \*/ DelayBlock_Disable(DLYB_SDMMC1); MODIFY_REG(hsd->Instance->CLKCR, SDMMC_CLKCR_SELCLKRX, SDMMC_CLKCR_SELCLKRX_0/   
\*SDMMC_CLKCR_SELCLKRX_0\*/);

The following diagram shows the steps to enable DLYB with tuning command:

![](images/7f3638bd515a7a86a934f6cdb5ae1a55ac8e8526c554ca81e7f6ff170e32286e.jpg)  
Figure 32. DLYB configuration with tuning command

The process starts with SEL = 0, then follow the next steps:

1Select the sdmmc_fb_ck as input clock.

Sr  u period, select the output clock phase value SEL.

3Start the tuning process: send CMD19, for tuning it returns 64 bytes of data.

Check data CRC error:

If no data CRC error occurred, DLYB was enabled successfully   
If a data CRC error occurred, reconfigure the DLYB with another clock phase value until the tuning process succeed oruntil tuning was tested with all clock phases selection value [0.12] then disable the DLYB and keep the old configuration of input clock.

# SDMMC host interface and MDMA

# Transfer data from SD card to DTCM memory with SDMMC and MDMA

The following exampledescribes how  configure he MDMA otransfer thedata received successfully  he SDMMC to DTCM memory using end of data transfer trigger.

![](images/1ee48529d5a5ebe6d1d852f04f54674f64bd3a9e573a325faf53d76f9ae785a7.jpg)  
Figure 33. MDMA and SDMMC end of data trigger example

# 7.2

# Configure the MDMA to enable data transfer with the SDMMC

The following example describes how to configure the MDMA to configure the SDMC registers to enable data transfer in DMA Single-buffer mode without any CPU action and using the Linked-list mode.

![](images/999c0baba2e869b58f414a21eb1b7c15b8dbc621e59f08889fa5879f4e447d00.jpg)  
Figure 34. MDMA and SDMMC Linked-list mode example

# How to enable Normal-boot mode from an MMC card

The following example describes how to execute Normal-boot mode from a multimedia card.

![](images/93b550e94e8fc8c1e82462f2b8622ca4461f4113bcf59937333fa6c8bbd3f33d.jpg)  
Figure 35. MMC card Normal-boot mode example

# 8.1

# Write data in the boot partition of the MMC card

Afrntaliznghe Cr as he boot partitin y sdi with  earguet ho the table below to write boot code to it. CMD6 is used to configure the MMC EXTCSD.

Table 17. Partitions selected to write into and their CMD6 arguments   

<table><tr><td rowspan=1 colspan=1>Partition selected to write into boot code</td><td rowspan=1 colspan=1>Argument for CMD6</td></tr><tr><td rowspan=1 colspan=1>User partition</td><td rowspan=1 colspan=1>0x03B3 0000</td></tr><tr><td rowspan=1 colspan=1>Boot partition 1</td><td rowspan=1 colspan=1>0x03B3 0100</td></tr><tr><td rowspan=1 colspan=1>Boot partition 2</td><td rowspan=1 colspan=1>0x03B3 0200</td></tr></table>

For this example's purposes we chose boot partition 1.

So in order to write data in the boot partition of the MMC card:

Access the boot partition and wait until the card is ready.

Erase the boot partition and write data to it and wait until the card is ready.

# 8.2

# Configure the MMC card boot bus

Enable boot acknowledgment and configure the MMC card to boot from the desired boot partition (boot partition 1) and wait until MMC card is ready.

CMD 6 boot acknowledgment argument selection : 0x03B3 4000

Table 18. Partitions selected for boot and their CMD6 arguments   

<table><tr><td rowspan=1 colspan=1>Partition selection for boot</td><td rowspan=1 colspan=1>Argument for CMD6</td></tr><tr><td rowspan=1 colspan=1>User partition</td><td rowspan=1 colspan=1>0x03B3 0800</td></tr><tr><td rowspan=1 colspan=1>Boot partition 1</td><td rowspan=1 colspan=1>0x03B3 1000</td></tr><tr><td rowspan=1 colspan=1>Boot partition 2</td><td rowspan=1 colspan=1>0x03B3 3000</td></tr></table>

Configure the bus width for boot mode:

Table 19. MMC boot bus widths and their CMD6 arguments   

<table><tr><td rowspan=1 colspan=1>Bus width selected for boot</td><td rowspan=1 colspan=1>Argument for CMD6</td></tr><tr><td rowspan=1 colspan=1>1-bit</td><td rowspan=1 colspan=1>0x03B1 0000</td></tr><tr><td rowspan=1 colspan=1>4-bit</td><td rowspan=1 colspan=1>0x03B1 0100</td></tr><tr><td rowspan=1 colspan=1>8-bit</td><td rowspan=1 colspan=1>0x03B1 0200</td></tr></table>

Configure the speed mode for boot.

Table 20. MMC speed modes selected for boot and their CMD6 arguments   

<table><tr><td rowspan=1 colspan=1>Bus width selected for boot(1)</td><td rowspan=1 colspan=1>Argument for CMD6</td></tr><tr><td rowspan=1 colspan=1>Legacy compatible</td><td rowspan=1 colspan=1>0x03B1 0000</td></tr><tr><td rowspan=1 colspan=1>HS SDR</td><td rowspan=1 colspan=1>0x03B1 0800</td></tr><tr><td rowspan=1 colspan=1>HS DDR</td><td rowspan=1 colspan=1>0x03B1 1000</td></tr></table>

HS200 is not supported for boot mode

4Preserve or reset bus configuration after boot.

Table 21. Bus configuration after boot and their CMD6 arguments   

<table><tr><td rowspan=1 colspan=1>Bus configuration after boot</td><td rowspan=1 colspan=1>Argument for CMD6</td></tr><tr><td rowspan=1 colspan=1>Preserve</td><td rowspan=1 colspan=1>0x03B1 0000</td></tr><tr><td rowspan=1 colspan=1>Reset</td><td rowspan=1 colspan=1>0x03B1 0400</td></tr></table>

After all those steps, the MMC card is configured and ready for boot mode.

# 8.3

# Configure the SDMMC to start Normal-boot mode

The ollowing procedure is an example f SDMC configuration or Normal-boot mode usig the Singleuffer DMA mode.

![](images/f4608c3e59e7d86abe74019d00f37a64ce27aee6868cb116927965fc5462c824.jpg)  
Figure 36. SDMMC configuration for Normal-boot mode

Send CMD0 with argument = OxFOFOFOF0 to reset the MMC card to pre-idle state.

Wait 74 SDMMC_CK cycles.

3Reset the DTCTRL register.

Configure the DPSM:

Enable BOOTACKEN.   
Set the acknowledgement timeout and the data timeout (SDMMC_ACKTIMER and SDMMC_DTIMER).   
Set the data block size and the data length.   
Set the transfer direction (from MMC card to SDMMC).   
Set the transfer mode as block mode.   
Disable the DPSM.

Enable the following interrupts:

Table 22. Interrupts to enable to configure SDMMC to start Normal-boot mode   

<table><tr><td rowspan=1 colspan=1>SDMMC interrupts enabled</td><td rowspan=1 colspan=1>Description</td></tr><tr><td rowspan=1 colspan=1>ACKTIMEOUT</td><td rowspan=1 colspan=1>Boot acknowledgement timeout</td></tr><tr><td rowspan=1 colspan=1>ACKFAIL</td><td rowspan=1 colspan=1>Boot acknowledgement check fail</td></tr><tr><td rowspan=1 colspan=1>DCRCFAIL</td><td rowspan=1 colspan=1>Data CRC check failed</td></tr><tr><td rowspan=1 colspan=1>CMDSENT</td><td rowspan=1 colspan=1>Command sent</td></tr><tr><td rowspan=1 colspan=1>RXOVERR</td><td rowspan=1 colspan=1>Received FIFO overrun</td></tr><tr><td rowspan=1 colspan=1>DATAEND</td><td rowspan=1 colspan=1>Successful end of data transfer</td></tr></table>

Enable the IDMA for Single-buffer transfer mode then configure the CPSM:

Select the Normal-boot mode.   
Enable boot mode (BOOTEN = 1).   
Enable the CPSM.

# SDMMC IRQ handler

The IRQ handler manages the errors. It disables the BOOTEN bit after the data end flag is set. I   ce

# 8.3.1

# Compare the written and the received data

Aer receiving dat wih Noral-boot modepareboth fhe writenand he eceivdat tcnfi ha they match.

# 9 Conclusion

The enhanced SDMMC host interface integrated in STM32 devices (example STM32H7 series), ofers multiple diffnt featurealloiguser eect e best coniguratin raplication.Tehost in supports multiple different memory devices with a very high-speed data transfer. This application note demonstrates the STM32H7 Series SDMMC host interface performances and its flexibility. The userf this interaceallows to extende storagememory and thanks toecosystem allow o lower development costs and fasten the time to market.

# Revision history

Table 23. Document revision history   

<table><tr><td rowspan=1 colspan=1>Date</td><td rowspan=1 colspan=1>Version</td><td rowspan=1 colspan=1>Changes</td></tr><tr><td rowspan=1 colspan=1>26-Nov-2018</td><td rowspan=1 colspan=1>1</td><td rowspan=1 colspan=1>Initial release.</td></tr><tr><td rowspan=1 colspan=1>05-Mar-2024</td><td rowspan=1 colspan=1>2</td><td rowspan=1 colspan=1>Updates:Section IntroductionSection 1: SDMMC host interfaceSection 1.1: STM32H743/753 SDMMC host-interface integrationSection 1.3.2: AHB interfaceSection 1.4: SDMMC host-interface differences between STM32F7Series and STM32H7 SeriesSection 2.1.1: SDMMC host interface GPIO configuration usingSTM32CubeMXSection 2.1.3: SDMMC host interface parameters configuration usingSTM32CubeMx</td></tr><tr><td rowspan=1 colspan=1>25-Jun-2025</td><td rowspan=1 colspan=1>3</td><td rowspan=1 colspan=1>UpdatedSection IntroductionTable 1. SDMMC supported speed modesSection 1.1: STM32H743/753 SDMMC host-interface integrationincluding:Figure 1. SDMMC1 and SDMMC2 internal connectionsTable 2. SDMMC1 and SDMMC2 main featuresAddedSection 1.2: STM32H7R/S SDMMC host-interface integrationSection 3.4: IDMA Linked List mode</td></tr></table>

# Contents

# 1 SDMMC host interface

1.1 STM32H743/753 SDMMC host-interface integration 3   
1.2 STM32H7R/S SDMMC host-interface integration. 6   
1.3 SDMMC host-interface block diagram. 8   
1.3.1 Adapter interface. 9   
1.3.2 AHB interface 9

1.4 SDMMC host-interface differences between STM32F7 Series and STM32H7 Series . ... 12

# SDMMC host interface initialization with SD and MMC cards. 13

2.1 Initiate SDMMC host interface configuration using STM32CubeMx . 13

2.1.1 SDMMC host interface GPIO configuration using STM32CubeMX . 13   
2.1.2 SDMMC host interface clock configuration using STM32CubeMx 14   
2.1.3 SDMMC host interface parameters configuration using STM32CubeMx . 15

2.2 Initiate SDMMC host interface configuration 18

# 2.3 SD card initialization 20

2.3.1 SD power on and initialization. 20   
2.3.2 Configure the wide bus operation for SD card. 21

# .4 MMC card initialization 22

2.4.1 MMC power on and initialization 22   
2.4.2 Configure the wide bus operation for MMC card 23

# How to read / write with SDMMC host interface in single / multiple block(s) mode . .25

3.1 Interrupt mode 26   
3.2 DMA Single-buffer mode 28   
3.3 DMA Double-buffer mode. 30   
3.4 IDMA Linked List mode .33

# How to read/write with SDMMC host interface using file system FATFS. .35

4.1 Imported project files for file system management with SDMMC 35   
4.2 File system example . 36

# SDMMC host interface and hardware flow control 37

# How to enable the DLYB 38

6.1 DLYB enabling use case presentation 38   
6.2 DLYB enabling use case configuration. 38   
6.2.1 DLYB configuration without tuning command 38   
6.2.2 DLYB configuration with tuning command. 40

# 7 SDMMC host interface and MDMA. 42

7.1 Transfer data from SD card to DTCM memory with SDMMC and MDMA . 42   
7.2 Configure the MDMA to enable data transfer with the SDMMC 42

# How to enable Normal-boot mode from an MMC card. 43

8.1 Write data in the boot partition of the MMC card. 43   
8.2 Configure the MMC card boot bus 44   
8.3 Configure the SDMMC to start Normal-boot mode 45   
8.3.1 Compare the written and the received data. 46

# Conclusion. .47

Revision history 48

# List of tables

Table 1. SDMMC supported speed modes. 2   
Table 2. SDMMC1 and SDMMC2 main features. 5   
Table 3. SDMMC main features 7   
Table 4. SDMMC internal input/output signals 8   
Table 5. SDMMC pins. 8   
Table 6. SDMMC differences between STM32F7 Series and STM32H7 Series 12   
Table 7. CMD6 data pattern for speed mode selection 22   
Table 8. CMD6 data pattern for speed mode selection 24   
Table 9. CMD6 data pattern for speed mode selection 24   
Table 10. Interrupts to enable to read in Interrupt mode 26   
Table 11. Interrupts to enable to write in Interrupt mode 27   
Table 12. Interrupts to enable to read in DMA Single-buffer mode 29   
Table 13. Interrupts to enable to write in DMA Single-buffer mode 29   
Table 14. Interrupts to enable to read in DMA Double-buffer mode 31   
Table 15. Interrupts to enable to write in DMA Double-buffer mode. 32   
Table 16. Interrupts to enable to write in IDMA Linked list mode . 33   
Table 17. Partitions selected to write into and their CMD6 arguments 43   
Table 18. Partitions selected for boot and their CMD6 arguments . 44   
Table 19. MMC boot bus widths and their CMD6 arguments 44   
Table 20. MMC speed modes selected for boot and their CMD6 arguments. 44   
Table 21. Bus configuration after boot and their CMD6 arguments 44   
Table 22. Interrupts to enable to configure SDMMC to start Normal-boot mode 46   
Table 23. Document revision history . 48

# List of figures

Figure 1. SDMMC1 and SDMMC2 internal connections. 3   
Figure 2. SDMMC and the delay block (DLYB). 3   
Figure 3. Triggers for MDMA and SDMMC1. 4   
Figure 4. Voltage switch transceiver 4   
Figure 5. SDMMC internal connection in the STM32H7R/S 6   
Figure 6. SDMMC block diagram 8   
Figure 7. IDMA single-buffer and double-buffer channel modes 10   
Figure 8. Linked list content and IDMA behavior. 11   
Figure 9. SDMMC pins configuration with STM32CubeMX. 13   
Figure 10. sdmmc_ker_ck configuration with STM32CubeMx. 14   
Figure 11. sdmmc_ker_ck source clock selection with STM32CubeMx 14   
Figure 12. SDMMC parameters configuration with STM32CubeMx. 15   
Figure 13. SDMMC global interrupt configuration with STM32CubeMx 16   
Figure 14. SDMMC FATFS configuration with STM32CubeMx 17   
Figure 15. MDMA end of data configuration with STM32CubeMx 18   
Figure 16. Synoptic diagram of SDMMC initialization 18   
Figure 17. Source clock for sdmmc1/2_ker_ck. 19   
Figure 18. SD card power on and initialization diagram 20   
Figure 19. SD card bus wide configuration diagram 21   
Figure 20. Synoptic diagram of MMC initialization. 22   
Figure 21. MMC card bus wide configuration diagram. 23   
Figure 22. Data transfer initialization. 25   
Figure 23. Read/write block(s) commands. 25   
Figure 24. Read/write data in Interrupt mode 26   
Figure 25. Read/write data in DMA Single-buffer mode 28   
Figure 26. Read/write data in DMA Double-buffer mode 30   
Figure 27. IDMA Double-buffer mode example. 33   
Figure 28. Middleware files tree 35   
Figure 29. BSP files tree. 35   
Figure 30. File system example 36   
Figure 31. Delay block configuration 39   
Figure 32. DLYB configuration with tuning command 40   
Figure 33. MDMA and SDMMC end of data trigger example 42   
Figure 34. MDMA and SDMMC Linked-list mode example. 42   
Figure 35. MMC card Normal-boot mode example 43   
Figure 36. SDMMC configuration for Normal-boot mode 45

# IMPORTANT NOTICE  READ CAREFULLY

pt old ursant  dits   leole.

purchasers' products.

No license, express or implied, to any intellectual property right is granted by ST herein.

are the property of their respective owners.

I

© 2025 STMicroelectronics - All rights reserved