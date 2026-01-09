# Level 1 cache on STM32F7 Series and STM32H7 Series

# Introduction

the access to the region can be cached or not.

I shared data.

STM32F7 Series and STM32H7 Series when using the L1-cache.

F user can refer to the following documents available on http:/www.st.com:

STM32F7 Series and STM32H7 Series Cortex®-M7 processor programming manual (PM0253).   
Managing memory protection unit (MPU) in STM32 MCUs (AN4838).

# 1 General information

This document applies to Arm®-based devices.

# arm

# 2 Cache control

The STM32F7 Series and STM32H7 Series devices include up to 16 Kbytes of L1-cache both for the instructions aa ar  av fetching the same data that is repeatedly used, such as a small loop.

Furestemarchiectue illustrate  example estemarchiecture h2 Series.

![](images/103ed1ecbd04be2888a06b53dc098cfcc0dc5131d277903f948f0c3c3cc0cd31.jpg)  
Figure 1. STM32F7 Series system architecture

Since the memory accesses to the subsystem can take multiple cycles (especially on the external memory T aceTeuache usytememory at keorehan  ccec iffe from he pipeli struction treamexecutinThisalows a b perormance boost.A ca lhoy set is called x-way associative. This property is set in the hardware design.

pua m ach modeas pros d consi egar he peorancehat must  weighe acorane wi te application.

I mey iswrbackhe cahe mark ir he wriy peoX AXIM interface to be written to the external memory system.

The L1-caches on all Cortex®M7s aredivided into lines of 32 bytes.Each lineis tagged with an address. The ai ai a hardware compromise to keep from having to tag each line with an address.

Acei is when an adresslls aywheewithin a given   Sotheardwarehs to do we whee a lne s selecte dependingon replacement algorithm) cleaned/invalidated,and reallocatedThe data cache and Instruction cache implement a pseudo-random replacement algorithm.

The L1-cache can be a performance booster when used in conjunction with memory interaces on AXI bus. This must not be confused with memories on the Tghtly Couple Memory TM) interface, which arenot cacheable. Any normal memory area can be cacheable, as described above, but the biggest gains are seen on memories accessed by the AXI bus such as the internal Flash memory internal SRAMs and externalmemoris attached to the FMC or Quad-SPI controllers.

STM32F7 and STM32H7 Cube firmware packages for these operations, reducing the development time.

# 2.1

# Accessing the Cortex®-M7 cache maintenance operations using CMSIS

The CMSIS cache functions defined in core_cm7.h are illustrated in Table 1. CMSIS cache functions.

Table 1. CMSIS cache functions   

<table><tr><td rowspan=1 colspan=1>CMSIS function</td><td rowspan=1 colspan=1>Description</td></tr><tr><td rowspan=1 colspan=1>void SCB_EnablelCache (void)</td><td rowspan=1 colspan=1>Invalidate and then enable the instruction cache</td></tr><tr><td rowspan=1 colspan=1>void SCB_DisablelCache (void)</td><td rowspan=1 colspan=1>Disable the instruction cache and invalidate its contents</td></tr><tr><td rowspan=1 colspan=1>void SCB_InvalidatelCache (void)</td><td rowspan=1 colspan=1>Invalidate the instruction cache</td></tr><tr><td rowspan=1 colspan=1>void SCB_EnableDCache (void)</td><td rowspan=1 colspan=1>Invalidate and then enable the data cache</td></tr><tr><td rowspan=1 colspan=1>void SCB_DisableDCache (void)</td><td rowspan=1 colspan=1>Disable the data cache and then clean and invalidate its contents</td></tr><tr><td rowspan=1 colspan=1>void SCB_InvalidateDCache (void)</td><td rowspan=1 colspan=1>Invalidate the data cache</td></tr><tr><td rowspan=1 colspan=1>void SCB_CleanDCache (void)</td><td rowspan=1 colspan=1>Clean the data cache</td></tr><tr><td rowspan=1 colspan=1>void SCB_CleanInvalidateDCache (void)</td><td rowspan=1 colspan=1>Clean and invalidate the data cache</td></tr></table>

Cacclea teratin wris back ir ce  hemor eatin eimes all flush). Invalidate cache: the operation marks the contents as invalid (basically, a delete operation).

# 3 Cache operation

a  a e o write-through.

Write-back: the cache does not write the cache contents to the memory until a clean operation is done.

Wrihrougger a writheeory  sonashecntents nhe cachee writenT hea enyu u moreua.  aci he wrie done in the background and has a litte effect unless the same cache se is beingaccessed repeatedy and very quickly. It is always a tradeoff.

# STM32F7 and STM32H7 default settings

y default, the MPU is disabled. In this case, the cache setting is defined as a default address map

Table 2. Memory region shareability and cache policies   

<table><tr><td rowspan=1 colspan=1>Address range</td><td rowspan=1 colspan=1>Memory region</td><td rowspan=1 colspan=1>Memory type</td><td rowspan=1 colspan=1>Shareability</td><td rowspan=1 colspan=1>Cache policy</td></tr><tr><td rowspan=1 colspan=1>0x00000000-0x1FFFFFFF</td><td rowspan=1 colspan=1>Code</td><td rowspan=1 colspan=1>Normal</td><td rowspan=1 colspan=1>Non-shareable</td><td rowspan=1 colspan=1>WT</td></tr><tr><td rowspan=1 colspan=1>0x20000000-0x3FFFFFFF</td><td rowspan=1 colspan=1>SRAM</td><td rowspan=1 colspan=1>Normal</td><td rowspan=1 colspan=1>Non-shareable</td><td rowspan=1 colspan=1>WBWA</td></tr><tr><td rowspan=1 colspan=1>0x40000000-0x5FFFFFFF</td><td rowspan=1 colspan=1>Peripheral</td><td rowspan=1 colspan=1>Device</td><td rowspan=1 colspan=1>Non-shareable</td><td rowspan=1 colspan=1>-</td></tr><tr><td rowspan=1 colspan=1>0x60000000-0Ox7FFFFFFF</td><td rowspan=2 colspan=1>External RAM</td><td rowspan=2 colspan=1>Normal</td><td rowspan=2 colspan=1>Non-shareable</td><td rowspan=1 colspan=1>WBWA</td></tr><tr><td rowspan=1 colspan=1>0x80000000-0x9FFFFFFF</td><td rowspan=1 colspan=1>WT</td></tr><tr><td rowspan=1 colspan=1>0xA0000000-0XxBFFFFFFF</td><td rowspan=2 colspan=1>External Device</td><td rowspan=2 colspan=1>Device</td><td rowspan=1 colspan=1>Shareable</td><td rowspan=2 colspan=1></td></tr><tr><td rowspan=1 colspan=1>0xC0000000-0xDFFFFFFF</td><td rowspan=1 colspan=1>Non-shareable</td></tr><tr><td rowspan=1 colspan=1>OxE0000000-0xE00FFFFF</td><td rowspan=1 colspan=1>Private peripheral bus</td><td rowspan=1 colspan=1>Strongly-ordered</td><td rowspan=1 colspan=1>Non-shareable</td><td rowspan=1 colspan=1></td></tr><tr><td rowspan=1 colspan=1>0xE0100000-0xFFFFFFFF</td><td rowspan=1 colspan=1>Vendor-specific system</td><td rowspan=1 colspan=1>Device</td><td rowspan=1 colspan=1>Non-shareable</td><td rowspan=1 colspan=1></td></tr></table>

# 3.2

# Example for cache maintenance and data coherency

T ur  eampl s  t lirizwitheR® Core®7at cache ey At first the CPU copies 128-byte constant pattern from the Flash memory "aSRCConst_Buffer to the SRAM1 temporary buffer "pBuffer"

Then the CPU configures and enables the DMA to perform a memory-to-memory transfer to copy from the SRAM1 "pBuffer" to the destination buffer "aDST_Buffer" defined in DTCM RAM.

Finally the CPU compares the data read by DMA aDST_Buffer with a constant pattern from the Flash memory (aSRC_Const_Buffer).

Figure 2. Data transfer paths illustrates the data transfer paths.

![](images/37a8ec8cd858c34faa25be34c14de353c8818a0c4717e4c20fc1df1e58e003e5.jpg)  
Figure 2. Data transfer paths

The purpose is to show the impact on data coherency between the CPU and DMA when accessing a cacheable nemory region with the write-back attribute set.

Bel a cacWheacal transfer between SRAM1 and DTCM RAM is done successfully in the described scenario above.

When enabling the data cache beforerunning thedescribed transerscenari, a data mismatch is detected between the data in "aDST_Buffer" (DMA destination buffer in DTCM) and "aSRC_Const_Buffer" (CPU data source buffer in the Flash memory).

When using the L-cache there is always angoing problem, smetimes called cache coherency. Thismatt cros up when multiple masters , DMAs share he memory. I the CPU writes something to an ar that has a write-back cache attibute example SRAM1), the write result is not seen on the SRAM as the access is buffd thenhe DMA reads e sammemory are peform  dattrans evalus readoo match the intended data.

Solution 1: to perform a cache maintenance operation after writing data to a cacheable memory region, by forcing a D-cache clean operation by software through CMSIS function SCB_CleanDCache() (all the dirty lines are write-back to SRAM1).   
Solution :in order to ensure the cache coherency the user must modify the MPU attribute of the SRAM1 from write-back (default) to write-through policy.   
Solution 3: tomodify the MPU attribute of the SRAM1 by using a shared attribute.This prevents by default the SRAM1 from being cached in D-cache.   
Soln  peor  amitaneratinrg wrroh polhe wriT can be enabled by setting force write-through in the D-Cache bit in the CACR control register.

The data coherency between the core and the DMA is ensured by:

1. Either making the SRAM1 buffers not cacheable   
2. Or making the SRAM1 buffers cache enabled with write-back policy, with the coherency ensured by software   
(clean or invalidate D-Cache)   
3. Or modifying the SRAM1 region in the MPU attribute to a shared region.   
4. Or making the SRAM1 buffer cache enabled with write-through policy.

Another case is when the DMA is writing to the SRAM1 and the CPU is going to read data from the SRAM1. To esure thedata coherency between the cache and the SRAM,he software must perform a cacheinvalidate before reading the updated data from the SRAM1.

For more details about he cachemaintenance operations theuser can reero cachemaintenance operations section in STM32F7 Series and STM32H7 Series Cortex®-M7 processor programming manual (PM0253).

# 4 Mistakes to avoid and tips

Atr reset, he usermust nvalidateeach cache before nablin  herwise nUNPREDICTIBLE beav can occur.   
Whbacacsemus cenncacsayiya to the external memory.   
Benabling he at cach theuser ust ivalidat he entiatcachtheextenalmemoryh have changed since the cache was disabled.   
Blasal a memory might have changed since the cache was disabled.   
If the software is usig cacheable memory regions for the DMA source/or destination buffers. The software must triger a cache clean before starting a DMA operation to ensure that ll the data aecommitted the subsystem memory. After the DMA transfer complete, when reading the data from the peripheral, the software must perform a cache invalidate before reading the DMA updated memory region.   
Always better to use non-cacheable regions for DMA buffers. The software can use the MPU to set up a non-cacheable memory block to use as a shared memory between the CPU and DMA.   
Do not enable cache for the memory that is being used extensively for a DMA operation.   
When using the ART accelerator, the CPU can read an instruction in just 1 clock from the internal Flash memory (like O-wait state). So I-cache cannot be used for the internal Flash memory.   
When using NOR Flash, the write-back causes problems because the erase and write commands are not sent to this external Flash memory.   
I cone devic s a normal memory a D-cace read  useful. However,  he external devic ASIC and/or a FIFO, the user must disable the D-cache for reading.

# Revision history

Table 3. Document revision history   

<table><tr><td>Date</td><td>Revision</td><td>Changes</td></tr><tr><td>23-Mar-2016</td><td>1</td><td>Initial release.</td></tr><tr><td rowspan="4">06-Mar-2018</td><td rowspan="4">2</td><td>Added STM32H7 Series in the whole document.</td></tr><tr><td>Updated Figure 1. STM32F7 Series system architecture.</td></tr><tr><td>Updated Figure 2. Data transfer paths.</td></tr><tr><td>Added Section 1 General information.</td></tr></table>

# Contents

1 General information   
2 Cache control 2.1 Accessing the Cortex®-M7 cache maintenance operations using CMSIS   
3 Cache operation . 3.1 STM32F7 and STM32H7 default settings . 5 3.2 Example for cache maintenance and data coherency. 5   
4 Mistakes to avoid and tips 8   
Revision history 9   
Contents .10   
List of tables 11   
List of figures. 12

# List of tables

Table 1. CMSIS cache functions. 4   
Table 2. Memory region shareability and cache policies 5   
Table 3. Document revision history . 9

# List of figures

Figure 1. STM32F7 Series system architecture 3   
Figure 2. Data transfer paths . 6

# IMPORTANT NOTICE  PLEASE READ CAREFULLY

pu ol urant ts ndns   pa el.

Purchasers' products.

No license, express or implied, to any intellectual property right is granted by ST herein.

.

I

© 2018 STMicroelectronics - All rights reserved