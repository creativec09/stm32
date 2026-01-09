# How to use error correction code (ECC) management for internal memories protection on STM32 MCUs

# Introduction

T pltioni Cnp. T document.

oCCpe al cus32532Hol a specific implementation of the software part of the safety solution.

This document complements the Reference documents, available on www.st.com.

Table 1. Applicable products   

<table><tr><td>Type</td><td>Products</td></tr><tr><td>Microcontroller</td><td>STM32H5 series, STM32H7 series, STM32U3 series, STM32U5 series</td></tr></table>

# 1 General information

This document applies to STM32H5, STM32H7, STM32U3, and STM32U5 series microcontrollers, which are Arm®-based devices.

# Note:

Arm is a registered trademark of Arm Limited (or its subsidiaries) in the US and/or elsewhere.

arm

Table 2. Acronyms and terms   

<table><tr><td rowspan=1 colspan=1>Acronym</td><td rowspan=1 colspan=1>Definition</td></tr><tr><td rowspan=1 colspan=1>ECC</td><td rowspan=1 colspan=1>Error correction code</td></tr><tr><td rowspan=1 colspan=1>CPU</td><td rowspan=1 colspan=1>Central processing unit (part of the MCU)</td></tr><tr><td rowspan=1 colspan=1>CRC</td><td rowspan=1 colspan=1>Cyclic redundancy check</td></tr><tr><td rowspan=1 colspan=1>DED</td><td rowspan=1 colspan=1>Double-error detection</td></tr><tr><td rowspan=1 colspan=1>DTCM</td><td rowspan=1 colspan=1>Data-tightly coupled memory</td></tr><tr><td rowspan=1 colspan=1>FAR</td><td rowspan=1 colspan=1>Falling address register</td></tr><tr><td rowspan=1 colspan=1>ISR</td><td rowspan=1 colspan=1>Interrupt service routine</td></tr><tr><td rowspan=1 colspan=1>ITCM</td><td rowspan=1 colspan=1>Instruction tightly coupled memory</td></tr><tr><td rowspan=1 colspan=1>MCU</td><td rowspan=1 colspan=1>Microcontroller unit</td></tr><tr><td rowspan=1 colspan=1>MDMA</td><td rowspan=1 colspan=1>Master direct-memory access</td></tr><tr><td rowspan=1 colspan=1>POR</td><td rowspan=1 colspan=1>Power-on reset</td></tr><tr><td rowspan=1 colspan=1>RAM</td><td rowspan=1 colspan=1>Random access memory</td></tr><tr><td rowspan=1 colspan=1>SEC</td><td rowspan=1 colspan=1>Single-error correction</td></tr><tr><td rowspan=1 colspan=1>SRAM</td><td rowspan=1 colspan=1>Static RAM</td></tr></table>

# Reference documents

[1] Reference manual STM32H503 Arm®-based 32-bit MCUs (RM0492)   
[2] Reference manual STM32H563/H573 and STM32H562 Arm®-based 32-bit MCUs (RM0481)   
[3] Reference manual STM32H7A3/7B3 and STM32H7B0 value line advanced Arm®-based 32-bit MCUs (RM0455)   
[4] Reference manual STM32H745/755 and STM32H747/757 advanced Arm®-based 32-bit MCUs (RM0399)   
[5] Reference manual STM32H723/733, STM32H725/735, and STM32H730 value line advanced Arm®-based 32-bit MCUs ((0468)   
[6] Reference manual STM32U5 series Arm®-based 32-bit MCUs (RM0456)   
[7] User manual STM32H7 dual-core safety manual (UM2840)   
[8] Reference manual STM32U3 series advanced Arm®-based 32-bit MCUs (RM0487)

# 2 ECC overview

The mathematician Richard Hamming invented the first ECC. The original Hamming code uses 7 bits to store ni RAM and flash memories are protected using a SEC-DED algorithm based on Hamming principles, but improved two-bit error in the stored word of data.

Ia a reset, for example a battery-powered data logger.

In flash memory, the data decays over time, especially at high temperatures. Storage temperatures have an impac on flash memory data, but cyclig(programming) temperaturehas neven strongermpact.The flash memory can sustain only a certain amount of rewrites to each memory word, this leads to the need of for a given product is published in the product datasheet.

data loss.

Table 3. Number of extra check bits used for SEC-DED   

<table><tr><td rowspan=1 colspan=1>Data word width</td><td rowspan=1 colspan=1>Number of redundancy bits</td></tr><tr><td rowspan=1 colspan=1>16</td><td rowspan=1 colspan=1>6</td></tr><tr><td rowspan=1 colspan=1>32</td><td rowspan=1 colspan=1>7</td></tr><tr><td rowspan=1 colspan=1>64</td><td rowspan=1 colspan=1>8</td></tr><tr><td rowspan=1 colspan=1>128</td><td rowspan=1 colspan=1>9</td></tr><tr><td rowspan=1 colspan=1>256</td><td rowspan=1 colspan=1>10</td></tr></table>

# 2.1 ECC implications

ECC is a key element in embedded systems that aim to comply with requirements of safety standards such as IEC60730 Class C or IEC 61508 SIL2 and higher.

AsioarwaCmameeargeynrcpliancuudl considerable softwareoverhedTheuCCmemory ncrease heoveral ignostic overage abov90% is easy to do and increases the system's readiness to comply with high safety standards.Another advantage using ECC  the potential mprovement  securiy s ECCusagemay lead  detection hardwaretampeing.

# 2.2 RAM ECC

The RAM ECC unctionality f the STM32 evices has a peripheral-ik interface with registers or ettins an with interrupts that permit a quick reaction to detected fault. Al STM32H72x/H73x/H74x, and STM32H75x SRAM and instruction/data cache memories are protected with ECC. The data width is 64-bit for AXI-SRAM and for ITCM-RAM. Allother volatile memories are accessed by 32-bit bus width (word size). On STM32H7Ax/H7Bx, only the tightly coupledmemories and instruction/data cache memories are protected with ECC. The other SRAMs ae not protected with ECC.

The ECC Monitoring is local per RAM region and each region is controlled by the RAMECC_MxCR. The RAMECC_IER allows a global ECC monitoring of ll the RAM sectors when activated whatever the configuration of RAMECC_MxCR

Other series featuring the RAM ECC protection are STM32H5 and STM32U5. Based on Cortex®-M33, these series have simpler memory architecture. They have ECC implemented on SRAM regions intended for data, which are backuSRAM SRAM2, and SRAM3. In case SRAM3, the use ECCis imitd o the rst 25B SRAM3 memory range. Last 64 KB block is then made unavailable for the user, serving for ECC redundancy storage.

Table 4. SRAM ECC coverage in selected STM32 devices   

<table><tr><td rowspan=1 colspan=1></td><td rowspan=1 colspan=1>H72x/H73x</td><td rowspan=1 colspan=1>H74x/H75x</td><td rowspan=1 colspan=1>H7Ax/H7Bx</td><td rowspan=1 colspan=1>H5</td><td rowspan=1 colspan=1>U5</td><td rowspan=1 colspan=1>H7Rx/H7Sx</td></tr><tr><td rowspan=1 colspan=1>AXI</td><td rowspan=1 colspan=1>64b</td><td rowspan=1 colspan=1>64b</td><td rowspan=1 colspan=1>X</td><td rowspan=1 colspan=1>-</td><td rowspan=1 colspan=1></td><td rowspan=1 colspan=1>64b (1)</td></tr><tr><td rowspan=1 colspan=1>ITCM</td><td rowspan=1 colspan=1>64b</td><td rowspan=1 colspan=1>64b</td><td rowspan=1 colspan=1>64b</td><td rowspan=1 colspan=1>-</td><td rowspan=1 colspan=1>-</td><td rowspan=1 colspan=1>64b</td></tr><tr><td rowspan=1 colspan=1>DTCM</td><td rowspan=1 colspan=1>32b</td><td rowspan=1 colspan=1>32b</td><td rowspan=1 colspan=1>32b</td><td rowspan=1 colspan=1>-</td><td rowspan=1 colspan=1>-</td><td rowspan=1 colspan=1>32b</td></tr><tr><td rowspan=1 colspan=1>SRAM1</td><td rowspan=1 colspan=1>32b</td><td rowspan=1 colspan=1>32b</td><td rowspan=1 colspan=1>X</td><td rowspan=1 colspan=1>X</td><td rowspan=1 colspan=1>X</td><td rowspan=1 colspan=1>32b</td></tr><tr><td rowspan=1 colspan=1>SRAM2</td><td rowspan=1 colspan=1>32b</td><td rowspan=1 colspan=1>32b</td><td rowspan=1 colspan=1>X</td><td rowspan=1 colspan=1>32b</td><td rowspan=1 colspan=1>32b</td><td rowspan=1 colspan=1>×</td></tr><tr><td rowspan=1 colspan=1>SRAM3</td><td rowspan=1 colspan=1>-</td><td rowspan=1 colspan=1>32b</td><td rowspan=1 colspan=1>-</td><td rowspan=1 colspan=1>32b(2)</td><td rowspan=1 colspan=1>32b(3)</td><td rowspan=1 colspan=1>32b</td></tr><tr><td rowspan=1 colspan=1>SRAM4</td><td rowspan=1 colspan=1>32b</td><td rowspan=1 colspan=1>32b</td><td rowspan=1 colspan=1>-</td><td rowspan=1 colspan=1>-</td><td rowspan=1 colspan=1>X</td><td rowspan=1 colspan=1>×</td></tr><tr><td rowspan=1 colspan=1>Backup RAM</td><td rowspan=1 colspan=1>32b</td><td rowspan=1 colspan=1>32b</td><td rowspan=1 colspan=1>X</td><td rowspan=1 colspan=1>32b</td><td rowspan=1 colspan=1>32b</td><td rowspan=1 colspan=1>32b</td></tr></table>

1AXI bus is 64b, but the same memory can also be accessed by AHB. 2Only the first 256 KB of SRAM3; the last block of memory is used to manage the ECC. Not the whole SRAM3, refer to document [6].

On most of the STM32H7 series microcontrollers, the RAM ECC cannot be turned off (except STM32H7Rx/ HSx). The ECC is powere and clockealong with the RAM and  is anintegral part of the RAM interfac. For example, backup SRAM can be disabled. This also disables the RAM ECC controller associated with it.

Te uor allworivolye i oy-wribs plecs, eC ot wrihevaleatel maybe the very next byter hal wor it waits or the next wriaccess.This s especally porn n aplications dealng with the backu RAM. Frexample when modifying array characters, s has vy posiveefcndevi powerconsptin. However wrieration t coplete ncs e e memory contents is retained without the last incomplete word write).

Tme akey aatwp o w each regular one. The dummy write address must be within the same memory (backup SRAM in this case).

![](images/25629e077bcb846f2016d1a1342dd04bb41a1bfe220b2bfabf47c4bff18db517.jpg)  
Figure 1. Unaligned access handling in preserved SRAM

![](images/aed93d54cd915f5ec0a478d33107a3ae3d2c5525828c82fb569b24138bfdac2f.jpg)  
Figure 2. RAM ECC controller interfaced with memory unit

RAM ECC controllers are assigned to each internal SRAM block. Within the STM32H7 architecture, the crollers eusually divi mog he ree yste mains:  n Diostifoml ial SRAM units/controllers are gathered into a global control block. This global control block has a set of coniguration registers and  global interrupt signal with the possibility f eventmasking.The TM32H7Rx/H7Sx line are exceptions. They do not share the power domain segmented SRAM. Instead, almost al the SRAM can be accessed on the AXI bus. Parts of SRAM can be relocated between the TCM and AXI mapping. This is the 327 e where the CC can be deactivatedhisalows he area used r redundancy purposes  e available as the SRAM4.

The STM32U5 series and STM32H5 series microcontrollers have the ECC configurable for each SRAM block lC o vaiC bltRAMie bleutatathe by a fielded application.

![](images/4eba5d947faa3a1ab3bb22e3e1f4dff808802794a922f295446c72581b6f6018.jpg)  
Figure 3. ECC RAM simplified block diagram

The particular RAM ECC controller assigned to a specific SRAM block checks the data integrity at each read accss to that SRAM block.Some read access types arenot obvious, as certain write includean mplict red phas.An examplenotbvious read access is anincompleteRAM wri peforme as aread/modify/wri two cycles. This can be either write of data smaller than RAM word, or an unaligned write.

# 1.3 Flash memory ECC

For STM32H72x/3x/4x/5x lines, the flash memory word (smallest programmable amount of memory) is 256 bits, while n STM32H7Ax/Bx lines,STM325 seris, and STM32U5 series,t is8 bitsTable5show he wor ize for STM32 devices with ECC in non-volatile memory. This is also the portion of memory protected b the10ECC (9 ECC bit or less orother MCUs) bits required t achieve SEC and DED funcionality on the flash memory W higher stress to the memory hardware. The STM32H5 series, STM32U5 series, and STM32H7Ax/Bx line also featu adde obustnes n he smal 0.by are wheeeve 6 bit  proteed with ECC redundancy. There is no OTP memory area on STM32H72x/3x/4x/5x lines.

Table 5. Flash memory ECC coverage in STM32 devices   

<table><tr><td rowspan=1 colspan=1>.</td><td rowspan=1 colspan=1>H72xlH73x</td><td rowspan=1 colspan=1>OtherH74x/H75x</td><td rowspan=1 colspan=1>H7AxlH7Bx</td><td rowspan=1 colspan=1>GO</td><td rowspan=1 colspan=1>G4/L4/L5/WB/WL/U3</td><td rowspan=1 colspan=1>H503</td><td rowspan=1 colspan=1>H563/573</td><td rowspan=1 colspan=1>L0/L1(1)</td><td rowspan=1 colspan=1>U5</td><td rowspan=1 colspan=1>U0</td></tr><tr><td rowspan=1 colspan=1>Bank1</td><td rowspan=1 colspan=1>256b</td><td rowspan=1 colspan=1>256b</td><td rowspan=1 colspan=1>128b</td><td rowspan=1 colspan=1>64b</td><td rowspan=1 colspan=1>64b(2)</td><td rowspan=1 colspan=1>128b</td><td rowspan=1 colspan=1>128b</td><td rowspan=1 colspan=1>16b</td><td rowspan=1 colspan=1>128b</td><td rowspan=1 colspan=1>64b</td></tr><tr><td rowspan=1 colspan=1>Bank2</td><td rowspan=1 colspan=1>-</td><td rowspan=1 colspan=1>256b</td><td rowspan=1 colspan=1>128b</td><td rowspan=1 colspan=1>64b(3)</td><td rowspan=1 colspan=1>64b(4)</td><td rowspan=1 colspan=1>-</td><td rowspan=1 colspan=1>128b</td><td rowspan=1 colspan=1>16b(4)</td><td rowspan=1 colspan=1>128b</td><td rowspan=1 colspan=1>-</td></tr><tr><td rowspan=1 colspan=1>Specialregion</td><td rowspan=1 colspan=1></td><td rowspan=1 colspan=1>-</td><td rowspan=1 colspan=1>16b</td><td rowspan=1 colspan=1>-</td><td rowspan=1 colspan=1>-</td><td rowspan=1 colspan=1></td><td rowspan=1 colspan=1>16b(5)</td><td rowspan=1 colspan=1>-</td><td rowspan=1 colspan=1>-</td><td rowspan=1 colspan=1>-</td></tr></table>

1ECC in STM32L0 has no user interface, so it is not described in detail in this table. 2. If DBANK = 0, the access width is 128 bits, but ECC remains 2 × 8 bytes. 3. Only G0Bx/GOCx. 4. Only on dual bank devices. Area of 16 bits words is configurable.

Talo flash memory status registers.

The disadvantage o an integratedECC solution is that programming single bitsin the flash memory words not pe witut ior prora itot  em  lenato EEPROM emulation or a monotonic counter, another algorithm must be selected for such applications on ECC enabled memories.

The flash memory controller f STM32H7 series implements also a hardware CRC integrity protection. The CRC is a complementary mechanism, not an ECC replacement. If the automated background CRC check is activated, the read access to the flash memory also implicitly checks the ECC in the whole range.

# 2.4 Cache memory ECC

oaothav e the addressed memory by preserving a copy frequentlyaccessed contents (eithercode f data)or contents whic are likely to be needed soon (current address+for example). Physically it is n SRAM with diffent addressing.

Ony STM32H7 series have cache with ECC protection. By default, the Cortex®-M7 L1 cache is also protected by EC by using the same SEC DED code.The word widh  56-it as the entire lne of cache is coverd. The C prn an bly e aecacCecdemus flush the cache. Then the ECC settings can be modified and the cache re-enabled with new setting.

The CPU cache is only involved in AXIM bus accesses, the ITCM, and DTCM address range does not require cace. The tightly coupled memories are almostexclusively dedicated to the usef the Cortex®M7 cor. The Corte®M7 prosor aautaically recover fomanydetecte EC fault in struction cache. Onebi aaifromh rogrammemory Ihecasdat cacetwobi errdetection mayresul in ose ongoing modifications while reloading old data.

# Note:

The write through practice is not recommended as a countermeasure to this rare event.

The ART accelerator cache that supports the Cortex®M4 core on dual-core STM32H7 seris microcontrollers is not protected by ECC.

C ulUe e he ae ven to-it at cacCC ero s orhe IEBR an DEBRcoe egiss.R the document [7] and the Arm® Cortex® technical documentation (TRM) for more details.

It memory (by flash or SRAM). Otherwise, llegal opcode may remain in cache, leading to hard fault.

# 2.5 ECC testing

It  l CC vAMhizA ol  e  i produce.

# Note:

On specific STM32 series, a dedicated software-based procedure to test ECC efficiency is available. The test prcedure allows the application software to inject ECC errors in memory. Refer to the Reference Manual to check if the option is available and related details.

Foron-volatimemory heoniversal oluton. Onhe32  eicateadress re ECCeror which is very convenient or testing.See hedesciption in theeerencemanual r moredtails. memory that requires reinitialization to avoid triggering ECC error by reading from it.

# Note:

If testin selat ncinal sfety coplian eeds,  is eende to er o he Safety anal of the applicable STM32 MCU series, available on www.st.com.

# 3 ECC use in applications

Inorder  correctuse he ECC capabilits, basiouties todeal withdetec errs diately mut e ilemente heae. Iende monior erpc aienan priconazawaredatiecallyorant eidustpl.

# Dealing with ECC errors in RAM

laoeoo en statae gilery ksi hence the device keeps a low-power consumption.

Arayalpha partce ma cause hat b nheRAMhange or alueCCmeani o u propehe erors mayacmulateverencaudt amageven  ysemiure.

The events a andom bynature nd occurence  error n some adress des ot provideanyindiatin where or when the next error may occur.

# 3.1.1 Initialization

When ECC is beigused in theRAMa memoris that are to beaccessed by the code must benitializ.A reaenalige wriitalizeor s liely tigerheCerorethe initial setting of both the stored value and the redundant bits.

Any pattern is fine for the memory initialization. Find below a proposed list of steps to follow:

S r wh RAM inlizaton r ORr ter wakeup o Stany moe rr ma   
Step 2. Clear the RAM ECC status register flags after RAM initialization.   
Step 3. Activate the ECC error latching. Even if optional, this action is important for subsequent correction o errors and for reliability errors.   
Step 4. Enable the interrupts for error correction and detection. It is possible to selectively enable interrupts only for some memory regions by using register flags for particular RAM ECC controller units.

Step 5. Enable the global RAM ECC interrupts.

# 3.1.2

# ECC ISR

The interrupt ervieroutie provies ortniy medately reac  an event  ECCerrrThe ISR implemented in CubeHAL generated in projects using STM32CubeMX tool is however just a start. The HAL ISR res llacictot pr e Ah ec ohocu implemented..

Theiglrorally yCcoleut n eat I I (in the case of another bit within the same word is damaged).

I  errappanyway he squn actnen  what exacty was mage  the wlc u between the SRAM and the CPU, the cache contents must be flushed.

In case of the damaged address falng into a stack area, to avoidfurther damage caused byexecuting in n RAM eapabls), heevelopeehictikGal recommended, but risk analysis conclusion may differ case by case.

![](images/2dc071181ccdf3f00b5f00b5d89f6d676a02cf28c12375bc2155279b7726af94.jpg)  
Figure 4. RAM ECC interrupt actions example   
NOTE: The abbreviations are register flags in the RAMECC monitor x status register (RAMECC_MxSR)

Logging the error for subsequent analysis can be an optional part of the post-failure operation.

# 3.1.3

# Interpreting FAR (failing address register)

T D[  poit  oran   ye ysils eiee following formula:

Address = Memory start address + FADD x word size in byte

For example, AXI SRAM monitor FADD=0x2004 means Ox2400 0000 + 0x2004 x 8 = 0x2401 0020 (64-bit words) But in SRAM1 monitor the FADD=0x2004 value interprets as 0x3000 0000 + 0x2004 x 4 = 0x3000 8010 (32-bit words).

A seial case is DTCM and other memoris, whic are interleaved To be specic, it works as ollows with STM32H7 series:

D0TCM starts at 0x20000000   
D1TCM starts at 0x20000004

In DOTCM, the address = DOTCM start address + FADD x 8 and in D1TCM address = D1TCM start address + FADD x 8. Each 64 bit of the DTCM consists of 32 bit from D0TCM followed by 32 bit f D1TCM formig common address space, but with separate ECC reporting.

# Preventive actions for ECC in RAM

The RAM ECC events are random, hence some damage can be prevented by performing a periodic check on the u RAM are. The CC check s activated by reading from each word the checkup perd is approate, m wor ewhihi  p hours to several days, it depends on the operating conditions, and the role of the microcontroller.

A preventivCcheckup does ot need  ecpleted ina sige round. I is a bacground task that ay e ur or a DMA transfer is not possible as the SRAM is divided into non continuous address ranges.

In te case of the STM32 sr, the MDMA is particularly suited for this task, as it can access the ITCM/ DTCM. When using the Cortex®-M7 CPU for memory check-by-read, the cache is involved (i cache is enabled). Accessing the SRAM through the Cortex®M7 cache (so ITCM and DTCM are excluded from this rule), each read from memory filhe cache lneof 56 bits.The loop that activates the CC check on each memory word r e t wordea  nd te cace e adg cnts wit eaig worh lowers the CPU load, but the bus remains heavily loaded.

Regular GPDMA is adequate for sweeping the memory of the STM32H5 and STM32U5 series.

# 3.2

# Dealing with ECC errors in flash memory

Tyical ailures o he ashmemorya l due oemory l wear nd l ue harge eakagome factors that might contributetofailurearnterference rom adjacent l orvoltagestabilityur nli osdicaha a subsequent failure in the same page. Flash memory errors should be non-existent on a new device, with l on temperature conditions and the amount of erase cycles.

# 3.2.1 Flash memory ECC ISR

Fo thea  het aotrrc n memory global interrupt vector. The ISR checks the flash memory status register FLASH_SR1 for ECC flags T as eu e ate   ual Gvhat r vector is shared with normal flash memory operations (such as end of programming), the ISR should then pass control to HAL to deal with the other flags. On the STM32H5 series and the STM32U5 series, the ECCC is signaled using regular flash interrupt vector, while the ECCD issues an NMI.

# 3.2.2 Flash memory code

Tolaoey is possible to have a second copy of the same code and swap to this second copy when an ECC error is pl failneealyweaanouc might improve the device life expectancy.

# 3.2.3 EEPROM emulation

cycling. Advanced EEPROM emulation implementations include mechanisms that deals with failing memory cells a are able to exclude them from the cycling. The application note EPROM emulation techniques and softae for STM32 microcontrollers(AN4894) deals with the problematic of EEPROM emulation including the ECC implications.

# 3.2.4

# Preventive action for ECC in flash memory

The CRC hardware modulef the STM32H7 eri s a useful tool tomonitor the embeded flash memoryhealth. CRC can check either the whole bank or a specific address range autonomously; ECC isimplicitly checked on read as well. The program must then implement a reaction to a detected problem.

For prdus whout hiRC eatu, DMA, exampe,may euse  heck n arey used pornse. If te secue boot is n plaesuh peridical checkups installapliations and loadercode can e implemented here.

# 4 Conclusion

Wit ahihe vngratiohemiceletroni  ystmemory elmo proneie hence ECC memory integrity protection becomes more important. The main difference between the RAM ECC caular ealhat AMCCot al prRAM interface.

This application note is a description of the ECC in RAM, flash memory and cache memory.   
It provides also procedures to deal with ECC errors in RAM and flash memory.

# Revision history

Table 6. Document revision history   

<table><tr><td rowspan=1 colspan=1>Date</td><td rowspan=1 colspan=1>Version</td><td rowspan=1 colspan=1>Changes</td></tr><tr><td rowspan=1 colspan=1>27-May-2019</td><td rowspan=1 colspan=1>1</td><td rowspan=1 colspan=1>Initial release.</td></tr><tr><td rowspan=1 colspan=1>6-Jan-2020</td><td rowspan=1 colspan=1>2</td><td rowspan=1 colspan=1>Updated:Section IntroductionSection 2.2 RAM ECCSection 2.3 Flash memory ECC</td></tr><tr><td rowspan=1 colspan=1>31-Mar-2022</td><td rowspan=1 colspan=1>3</td><td rowspan=1 colspan=1>Updated:Section IntroductionSection 2 ECC overviewSection 2.2 RAM ECCSection 2.3 Flash memory ECCAdded Section 3.1.3 Interpreting FAR (failing address register)</td></tr><tr><td rowspan=1 colspan=1>21-Feb-2023</td><td rowspan=1 colspan=1>4</td><td rowspan=1 colspan=1>Updated document to cover STM32H5, STM32H7, and STM32U5 seriesmicrocontrollers.Section IntroductionSection General InformationSection 2 ECC overviewSection 2.1 ECC implicationsSection 2.2 RAM ECCSection 2.3 Flash memory ECCSection 2.4 Cache memory ECCSection 3.1.2 ECC ISRSection 3.2.1 Flash memory ECC ISRAdded:Section 2.5 ECC testing</td></tr><tr><td rowspan=1 colspan=1>10-Jul-2023</td><td rowspan=1 colspan=1>5</td><td rowspan=1 colspan=1>Updated:Section 2: ECC overviewSection 2.2: RAM ECCSection 3.1.3: Interpreting FAR (failing address register)</td></tr><tr><td rowspan=1 colspan=1>7-Feb-2024</td><td rowspan=1 colspan=1>6</td><td rowspan=1 colspan=1>Updated:H7Rx/H7Sx added to Table 4. SRAM ECC coverage in selected STM32devicesH7Rx/H7Sx description added to Section 2.2: RAM ECCU0 added to Table 5. Flash memory ECC coverage in STM32 devices</td></tr><tr><td rowspan=1 colspan=1>11-Jun-2025</td><td rowspan=1 colspan=1>7</td><td rowspan=1 colspan=1>Updated:Product information to include the STM32U3 seriesSection IntroductionSection 2.2: RAM ECCSection 2.3: Flash memory ECC</td></tr></table>

# Contents

#

# 1 General information

# 2 ECC overview

2.1 ECC implications. 3   
2.2 RAM ECC. 3   
2.3 Flash memory ECC. 6   
2.4 Cache memory ECC. 6   
2.5 ECC testing

# ECC use in applications 8

# 3.1 Dealing with ECC errors in RAM. 8

3.1.1 Initialization . 8   
3.1.2 ECC ISR. 8   
3.1.3 Interpreting FAR (failing address register) . 9   
3.1.4 Preventive actions for ECC in RAM. 9

# 3.2 Dealing with ECC errors in flash memory 11

3.2.1 Flash memory ECC ISR. 11   
3.2.2 Flash memory code. 11   
3.2.3 EEPROM emulation 11   
3.2.4 Preventive action for ECC in flash memory . 11

# Conclusion 12

# Revision history 13

# .ist of tables .15

# List of figures. 16

# List of tables

Table 1. Applicable products   
Table 2. Acronyms and terms 2   
Table 3. Number of extra check bits used for SEC-DED 3   
Table 4. SRAM ECC coverage in selected STM32 devices 4   
Table 5. Flash memory ECC coverage in STM32 devices 6   
Table 6. Document revision history . 13

# List of figures

Figure 1. Unaligned access handling in preserved SRAM 4   
Figure 2. RAM ECC controller interfaced with memory unit 5   
Figure 3. ECC RAM simplified block diagram. 5   
Figure 4. RAM ECC interrupt actions example 9

# IMPORTANT NOTICE  READ CAREFULLY

pt old ursant  dits   leole.

purchasers' products.

No license, express or implied, to any intellectual property right is granted by ST herein.

are the property of their respective owners.

I

© 2025 STMicroelectronics - All rights reserved