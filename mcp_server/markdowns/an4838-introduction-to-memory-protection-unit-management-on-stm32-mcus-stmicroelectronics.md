# Introduction to memory protection unit management on STM32 MCUs

# Introduction

This application note describes how to manage the memory protection unit (MPU) in the STM32 products.

P PC no change in the memory system behavior.

M33/M55 design that supports the MPU.

For more details about the MPU, refer to the following documents available on www.st.com

Programming manual STM32F7 series and STM32H7 series Cortex®-M7 processor (PM0253)   
Programming manual STM32F10xxx/20xxx/21xxx/L1xxxx Cortex®-M3 (PM0056)   
Programming manual STM32 Cortex®-MO+ MCUs programming manual (PM0223)   
Programming manual STM32 Cortex®-M4 MCUs and MPUs (PM0214)   
Programming manual STM32 Cortex®-M33 MCUs (PM0264)   
Programming manual STM32 Cortex®-M55 MCUs (PM0273)

Table 1. Applicable products   

<table><tr><td>Type</td><td>Product series</td></tr><tr><td></td><td>STM32C0 series STM32F1 series, STM32F2 series, STM32F3 series, STM32F4 series, STM32F7 series</td></tr><tr><td></td><td>STM32G0 series, STM32G4 series</td></tr><tr><td></td><td>STM32H5 series, STM32H7 series</td></tr><tr><td>Microcontrollers</td><td>STM32L0 series, STM32L1 series, STM32L4 series, STM32L4+ series, STM32L5 series</td></tr><tr><td></td><td>STM32U0 series, STM32U3 series, STM32U5 series</td></tr><tr><td></td><td></td></tr><tr><td></td><td>STM32WB series, STM32WB0 series STM32N6 series</td></tr></table>

# 1 General information

# Note:

This application note applies to STM32 microcontrollers Arm®-based devices. Arm is a registered trademark of Arm Limited (or its subsidiaries) in the US and/or elsewher

# arm

# 2 Overview

The MPU can be used to make an embedded system more robust and more secure by:

prohibiting the user applications from corrupting data used bycritical tasks (such as the operating system kernel defining the SRAM memory region as a non-executable (execute never XN) to prevent code injection attacks • changing the memory access attributes

The MPU can be used to protect up to 16 memory regions. In Armv6 and Armv7 architecture (Cortex-M0+, M3, oregions protected can vary between core and devices in the 3, refer toTable6 or more details. The subregions are always of equal size, and can be enabled or disabled by a subregion number. Because the m gion zivecace  eng  yte h egon  y 256-byte size.

T Iallfu 0-15 memory regions take priority over the default region.

The regions can overlap, and can be nested The region 15 has the highest priority and the region 0has the lowest one and this governs how overlapping the regions behave. The priorities are fixed, and cannot be changed.

In Armv8 architecture (Cortex-M33 and M55) the regions are defined using a base and a limit address offig febility anspliciy hedeveloperewayrganihemAditnallyorte-33 nd Mo include subregions as the region size is now more flexible.

The figure below shows an example with i regions.This example hows the rgion overlapping the eins aThegn o cpleey wihihe giSce pririy   dior v falling in the overlap between 0 and 4 is not writeable.

![](images/5afa33cc2a3444a3fee3db99b76c35cf736da050ee87ed4c366f6fd02665f728.jpg)  
Figure 1. Example of overlapping regions

# Caution:

In Armv8 architecture, regions are now not allowed to overlap. As the MPU region definition is much more flexible, overlapping MPU regions is not necessary.

The MPU is unified, meaning that there are not separate regions for the data and the instructions.

The MPU can be us also o defieothemeoy ttributes such as the cacheability, which can eexpor t olT tt® st to level ace: iecacea ut cach.o   ny  ve of cache (L1-cache) is supported.

T  ol whether the region is cacheable or not.

# 2.1 Memory model

In T32 products, the processor has a fixed default memory map that provides up to 4 Gbytesf addressable memory.

Figure 2. Cortex-M0+/M3/M4/M7 processor memory map   

<table><tr><td colspan="2">Vendor-specific memory</td><td rowspan="2">0xFFFF FFFF OxE010 0000 0xE00F FFFF 0xE000 0000 0xDFFF FFFF</td></tr><tr><td>Private peripheral bus</td><td>511 Mbytes 1.0 Mbyte</td></tr><tr><td>External device</td><td>1.0 Gbyte</td><td rowspan="3">OxA000 0000 0x9FFF FFFF</td></tr><tr><td>External RAM</td><td>1.0 Gbyte 0x6000 0000</td></tr><tr><td>Peripheral</td><td>0x5FFF FFFF 0.5 Gbyte 0x4000 0000</td></tr><tr><td>SRAM</td><td>0.5 Gbyte</td><td>0x3FFF FFFF 0x2000 0000</td></tr><tr><td>Code</td><td>0.5 Gbyte</td><td>0x1FFF FFFF 0x0000 0000</td></tr></table>

![](images/b3ad409ceb5aeac322e5ceb2bb7e94a06f8b00ea6478c4996c3e37570263a581.jpg)  
Figure 3. Cortex-M33 processor memory map

Table 2. Default memory map for the Cortex-M55 processor   

<table><tr><td rowspan=1 colspan=1>Address range (inclusive)</td><td rowspan=1 colspan=1>Region</td><td rowspan=1 colspan=1>Interface</td></tr><tr><td rowspan=1 colspan=1>0x00000000-0x1FFFFFFF</td><td rowspan=1 colspan=1>Code</td><td rowspan=1 colspan=1>All accesses are performed on the instruction tightly coupled memory (TCM)or manager-AXI (M-AXI) interface.</td></tr><tr><td rowspan=1 colspan=1>0x20000000-0x3FFFFFFF</td><td rowspan=1 colspan=1>SRAM</td><td rowspan=1 colspan=1>All accesses are performed on the data tightly coupled memory (DTCM) orM-AXI interface.</td></tr><tr><td rowspan=1 colspan=1>0x40000000-0x5FFFFFFF</td><td rowspan=1 colspan=1>Peripheral</td><td rowspan=1 colspan=1>Data accesses are performed on peripheral AHB (P-AHB) or M-AXIinterface.Instruction accesses are performed on M-AXI.</td></tr><tr><td rowspan=1 colspan=1>0x60000000-0x9FFFFFFF</td><td rowspan=1 colspan=1>External RAM</td><td rowspan=1 colspan=1>All accesses are performed on the M-AXI interface</td></tr><tr><td rowspan=1 colspan=1>0xA0000000-0OxDFFFFFFF</td><td rowspan=1 colspan=1>External device</td><td rowspan=1 colspan=1>All accesses are performed on the M-AXI interface.</td></tr><tr><td rowspan=1 colspan=1>0xE0000000-0xE00FFFFF</td><td rowspan=1 colspan=1>Private peripheralbus (PB)</td><td rowspan=1 colspan=1>Instruction fetches are not supported.Reserved for system control and debug.Data accesses are either performed internally or on external privateperipheral bus (EPPB).</td></tr><tr><td rowspan=1 colspan=1>0xE0100000-0xFFFFFFFF</td><td rowspan=1 colspan=1>Vendor_SYS</td><td rowspan=1 colspan=1>Instruction fetches are not supported.OxE0100000-0xEFFFFFFF is reserved. Vendor resources start at0xF0000000.Data accesses are performed on P-AHB interface.</td></tr></table>

# 3 Cortex-M0+/M3/M4/M7 memory types, registers and attributes

The memory map and the programmig the MPU split the memory map int regions.Each region has a dfi meory ymeor ttueeory yuteie heeavi region.

# Memory types

There are three common memory types:

Normal memory: allows the load and store of bytes, half-words, and words to be arranged by the CPU in an efficient manner (the compiler is not aware of memory region types). For the normal memory region, the load/store is not necessarily performed by the CPU in the order listed in the program.   
Devimemoy: wihindevie egin,he ads an store e donestrict rThs that the registers are set in the proper order.   
Strongly ordered memory: everything is always done in the programmatically listed order, where the CPU whe /stostutiexeutin eiv u a) beeeting he exs in the program stream. This can cause a performance hit.

# 3.2 MPU register description

The MPU registers are located at OxE000 ED90. There are five basic MPU registers and a number of alias registers for region. The following are used to set up regions in the MPU:

MPU_TYPE: read-only register used to detect the MPU presence.   
MPU_CTRL: control register.   
MPU_RNR: region number, used to determine which region operations are applied to.   
MPU_RBAR: region base address.   
MPU_RASR: region attributes and size.   
MPU_RBAR_An: alias n of MPU_RBAR, where n is 1 to 3.   
MPU_RASR_An: alias n of MPU_RASR, where n is 1 to 3.

# Note:

The Cortex-MO+ does not implement the MPU_RBAR_An and MPU_RASR_An registers.

For more details about the MPU registers, refer to the programming manuals listed in Introduction.

# 3.3 Memory attributes

The region attributes and size register (MPURASR) are where allthe memory attributes are set. The able shows a brief description of the region attributes and size in the MPU_RASR register.

Table 3. Region attributes and size in MPU_RASR register   

<table><tr><td rowspan=1 colspan=1>Bits</td><td rowspan=1 colspan=1>Name</td><td rowspan=1 colspan=1>Description</td></tr><tr><td rowspan=1 colspan=1>28</td><td rowspan=1 colspan=1>XN</td><td rowspan=1 colspan=1>Execute never</td></tr><tr><td rowspan=1 colspan=1>26:24</td><td rowspan=1 colspan=1>AP</td><td rowspan=1 colspan=1>Data access permission field (RO, RW, or No access)</td></tr><tr><td rowspan=1 colspan=1>21:19</td><td rowspan=1 colspan=1>TEX</td><td rowspan=1 colspan=1>Type extension field</td></tr><tr><td rowspan=1 colspan=1>18</td><td rowspan=1 colspan=1>S</td><td rowspan=1 colspan=1>Shareable</td></tr><tr><td rowspan=1 colspan=1>17</td><td rowspan=1 colspan=1>C</td><td rowspan=1 colspan=1>Cacheable</td></tr><tr><td rowspan=1 colspan=1>16</td><td rowspan=1 colspan=1>B</td><td rowspan=1 colspan=1>Bufferable</td></tr><tr><td rowspan=1 colspan=1>15:8</td><td rowspan=1 colspan=1>SRD</td><td rowspan=1 colspan=1>Subregion disabled. For each subregion 1 = disabled, 0 = enabled.</td></tr><tr><td rowspan=1 colspan=1>5:1</td><td rowspan=1 colspan=1>SIZE</td><td rowspan=1 colspan=1>Specifies the size of the MPU protection region.</td></tr></table>

Parameters of the previous table are detailed below:

The Xcnrols he deeecuti. Inreecunstctiwihi egn tem read access for the privileged level, and XN must be 0. Otherwise, a MemManage fault is generated.

The data access permission (AP) field defines the AP of memory region. The table below illustrates the access permissions:

Table 4. Access permissions of regions   

<table><tr><td rowspan=1 colspan=1>AP[2:0]</td><td rowspan=1 colspan=1>Privilegedpermissions</td><td rowspan=1 colspan=1>Unprivilegedpermissions</td><td rowspan=1 colspan=1>Description</td></tr><tr><td rowspan=1 colspan=1>000</td><td rowspan=1 colspan=1>No access</td><td rowspan=1 colspan=1>No access</td><td rowspan=1 colspan=1>All accesses generate a permission fault</td></tr><tr><td rowspan=1 colspan=1>001</td><td rowspan=1 colspan=1>RW</td><td rowspan=1 colspan=1>No access</td><td rowspan=1 colspan=1>Access from a privileged software only</td></tr><tr><td rowspan=1 colspan=1>010</td><td rowspan=1 colspan=1>RW</td><td rowspan=1 colspan=1>RO</td><td rowspan=1 colspan=1>Written by an unprivileged software generates apermission fault</td></tr><tr><td rowspan=1 colspan=1>011</td><td rowspan=1 colspan=1>RW</td><td rowspan=1 colspan=1>RW</td><td rowspan=1 colspan=1>Full access</td></tr><tr><td rowspan=1 colspan=1>100</td><td rowspan=1 colspan=1>Unpredictable</td><td rowspan=1 colspan=1>Unpredictable</td><td rowspan=1 colspan=1>Reserved</td></tr><tr><td rowspan=1 colspan=1>101</td><td rowspan=1 colspan=1>RO</td><td rowspan=1 colspan=1>No access</td><td rowspan=1 colspan=1>Read by a privileged software only</td></tr><tr><td rowspan=1 colspan=1>110</td><td rowspan=1 colspan=1>RO</td><td rowspan=1 colspan=1>RO</td><td rowspan=1 colspan=1>Read only, by privileged or unprivileged software</td></tr><tr><td rowspan=1 colspan=1>111</td><td rowspan=1 colspan=1>RO</td><td rowspan=1 colspan=1>RO</td><td rowspan=1 colspan=1>Read only, by privileged or unprivileged software</td></tr></table>

The S field is for a shareable memory region: the memory system provides data synchronization between bus masters in a system with multiple bus masters, for example, a processor with a DMA controller. A strongly-orderedmemory is always shareable. If multiple bus masters can access a non-shareable memory region, the software must ensure the data coherency between the bus masters. The STM32F7 series and STM32H7 series do not support hardware coherency. The S field is equivalent to non-cacheable memory.

The TEX, C and B bits are used to define cache properties for the region, and to some extent, its shareability. They are encoded as per the following table.

Table 5. Cache properties and shareability   

<table><tr><td rowspan=1 colspan=1>TEX</td><td rowspan=1 colspan=1>C</td><td rowspan=1 colspan=1>B</td><td rowspan=1 colspan=1>Memory type</td><td rowspan=1 colspan=1>Description</td><td rowspan=1 colspan=1>Shareable</td></tr><tr><td rowspan=1 colspan=1>000</td><td rowspan=1 colspan=1>0</td><td rowspan=1 colspan=1>0</td><td rowspan=1 colspan=1>Strongly ordered</td><td rowspan=1 colspan=1>Strongly ordered</td><td rowspan=1 colspan=1>Yes</td></tr><tr><td rowspan=1 colspan=1>000</td><td rowspan=1 colspan=1>0</td><td rowspan=1 colspan=1>1</td><td rowspan=1 colspan=1>Device</td><td rowspan=1 colspan=1>Shared device</td><td rowspan=1 colspan=1>Yes</td></tr><tr><td rowspan=1 colspan=1>000</td><td rowspan=1 colspan=1>1</td><td rowspan=1 colspan=1>0</td><td rowspan=1 colspan=1>Normal</td><td rowspan=1 colspan=1>Write through, no write allocate</td><td rowspan=1 colspan=1>S bit</td></tr><tr><td rowspan=1 colspan=1>000</td><td rowspan=1 colspan=1>1</td><td rowspan=1 colspan=1>1</td><td rowspan=1 colspan=1>Normal</td><td rowspan=1 colspan=1>Write-back, no write allocate</td><td rowspan=1 colspan=1>S bit</td></tr><tr><td rowspan=1 colspan=1>001</td><td rowspan=1 colspan=1>0</td><td rowspan=1 colspan=1>0</td><td rowspan=1 colspan=1>Normal</td><td rowspan=1 colspan=1>Non-cacheable</td><td rowspan=1 colspan=1>S bit</td></tr><tr><td rowspan=1 colspan=1>001</td><td rowspan=1 colspan=1>0</td><td rowspan=1 colspan=1>1</td><td rowspan=1 colspan=1>Reserved</td><td rowspan=1 colspan=1>Reserved</td><td rowspan=1 colspan=1>Reserved</td></tr><tr><td rowspan=1 colspan=1>001</td><td rowspan=1 colspan=1>1</td><td rowspan=1 colspan=1>0</td><td rowspan=1 colspan=1>Undefined</td><td rowspan=1 colspan=1>Undefined</td><td rowspan=1 colspan=1>Undefined</td></tr><tr><td rowspan=1 colspan=1>001</td><td rowspan=1 colspan=1>1</td><td rowspan=1 colspan=1>1</td><td rowspan=1 colspan=1>Normal</td><td rowspan=1 colspan=1>Write-back, write and read allocate</td><td rowspan=1 colspan=1>S bit</td></tr><tr><td rowspan=1 colspan=1>010</td><td rowspan=1 colspan=1>0</td><td rowspan=1 colspan=1>0</td><td rowspan=1 colspan=1>Device</td><td rowspan=1 colspan=1>Non-shareable device</td><td rowspan=1 colspan=1>No</td></tr><tr><td rowspan=1 colspan=1>010</td><td rowspan=1 colspan=1>0</td><td rowspan=1 colspan=1>1</td><td rowspan=1 colspan=1>Reserved</td><td rowspan=1 colspan=1>Reserved</td><td rowspan=1 colspan=1>Reserved</td></tr></table>

The subregion disable bits (SRD) flag whether a particular subregion is enabled ordisabled. Disabling a subregion means that another region overlapping the disabled range matches instead. Ino other eabled region overlaps the disabled subregion, the MPU issues a fault.

For the products that implement a cache (only for STM32F7 series and STM32H7 series that implement L1- cache) the additional memory attributes include:

Cacheable/non-cacheable: means that the dedicated region can be cached or not.   
Write through with no write allocate: on hits, it writes to the cache and the main memory. On misses it updates the block in the main memory not bringing that block to the cache.   
Wal memory is not update. On misses, i updates the block in the main memory not bringing that block to the cache.   
W memory is not updated. On misses it updates the block in the main memory and brings the block to the cache.

# Note:

For Cortex-M7, TCMs memories always behave as non-cacheable, non-shared normal memories, rrespective of the memory type attributes defined in the MPU for a memory region containing addresses held in the TCM.

Oheis, the access perisions associated with an MPU region in theTCM adres space aretreate in te same way as addresses outside the TCM address space.

# 3.4

# Cortex-M7 constraint speculative prefetch

The Cortex-M7 implements the speculative prefetch feature, which allows speculative accesses to normal memory locations (or example: MC, QuadSPI devices). When a speculative prefetch happens, it may ipct meviaiup uole. Iy the traff generated by another masters such as LCD-TFT or DMA2D with higher bandwidth consumption when a speculative prefetch happens. In order to protect normal memories from a speculative prefetch, it is recommended to change memory atributes rom normal to a strongly ordered or to devicememory hanks to the MPU. For more details about configuring memory attributes, refer to Section 6: MPU settng example with STM32Cube HAL on Armv6 and Armv7 architectures.

# 4 Cortex-M33/M55 memory types, registers and attributes

Cortex-M33 and Cortex-M55 are respectively based on the Armv8-M and Armv8.1-M architectures (Cortex®-M55 processor supports Arm Protected Memory System Architecture (PMSA). In both cases, the MPU is a component that is primarily used for memory region protection.

Ah trhePUtn i heMPUevhiuea programmers' model to the MPU in previous versions of the M-profile Arm® architecture.

Ii T® registers or the secure state, and a mirror et or the non-secure state. When acessing he MP adress between OxE000 ED90 and OxE000 EDC4, the type of MPU registers accessed is determined by the current state of the processor.

Non-secure code can access non-secure MPU registers and secure code can access secure MPU registers.   
Secure code can access non-secure MPU registers at their aliased address.

Secure access sees secure MPU regisers, on-secureaccess sees non-secure MPU registers. Secure sotae can also access non-secure MPU registers using the alias address.

# Note:

See Arm®-M Architecture reference manual for more information about the memory model.

# 4.1

# Memory types and attributes

In Armv8-M and Armv8.1-M architectures, memory types are divided into:

normal memory device memory

# Note:

The strongly ordered (SO) device memory type in Armv6-M and Armv7-M is now a subset of the device memory type.

Aoral meory ytene s P ginsh use geneal tucin memory. Normal memory llows the processor to perform some memory access optimizations, such as access reordering ormerging. Normal memory also allowsmemory to be cacheand is suitable oholding executable code. Normal memory must not be used to access peripheral MMiO registers. The device memory type is intended for that use.A normal memory definition remains mostly unchanged fom the Armv7-M architecture.

A normal memory has the following attributes:

cacheability: memories cacheable or non-cacheable shareability: normal memory shareable or non-shareable execute never: memories marked as executable or execute never (XN)

A device memory must be used for memory regions that cover peripheral control registers. Some of the zl register.

A device memory has the following attributes:

• G or nG: gathering or non-gathering. (multiple accesses to a device can be merged into a single transaction except for operations with memory ordering semantics, for example, memory barrier instructions, load acquire/store release). R or nR: reordering E or nE: early write acknowledge (similar to bufferable)

Only four combinations of these attributes are valid:

device-nGnRnE: equivalent to Armv7-M strongly ordered memory type   
device-nGnRE: equivalent to Armv7-M device memory   
device-nGRE: new to Armv8-M   
device-GRE: new to Armv8-M

# 4.1.1

# Cortex®-M55 access privilege level for device and normal memory

The AMBA® 5 AXI, AMBA® 5 AHB, and AMBA® 4 APB protocols have signals that can report the privilege level an access request to the system.

The Cortex-M55 processor supports these signals across the manager AXI (M-AXI), the peripheral AHB (P-AHB), l  l  v for normal memory on P-AHB. However, accesses to normal memory on M-AXI can be buffered and cached, alling memory read and write requess, as wel as nstruction fetches from both privilege and upriviled sotare, to be merged. For these transactions initiated by loads and stores, the AXI signals ARPROT[0] and AWPROT[0] arealwayidicating a privileged access.Access permission toa region memory canalw e restricted to software running in privileged mode by using the MPU.

The istrucion tightl couplememory TCM) and data tightly couplememory (DTCM) inteaces provie the following signals: ITCMPRIV, DOTCMPRIV, D1TCMPRIV, D2TCMPRIV, and D3TCMPRIV. These signalS indicate the privilege of all memory accesses except the ones initiated by loads and stores.

# 4.2 Attribute indirection

The attribute indirection mechanism allows multiple MPU regions to share a set of memory attributes.

The MPU can be configured to support 0, 4, 8, , r16memory regios (ecurity extension is included i e Cortex-M55 processor. Memory protection can be duplicated between secure and nonsecure MPU (MPUS and MP_NS).)

The numberof regions in the secure and nonsecure MPU can be configured independently, and each can be programmed to protect memory for the associated security state.

The following figure shows that MPU regions , , and 3 are al assigned to SRAM. Therefore, they can share cache-related memory attributes.

![](images/4f5cf0828a59fa3830afa5ee348c4f4c026c38f4e7d9ed3b60301b104c2df605.jpg)  
Figure 4. Attribute indirection example

A  e g   n  havehe s eisn, hailtyt.   
This is required as each region can be used differently in the application.

# 4.3 MPU registers

The Cortex-M33/M55 MPU registers are different from previous Cortex® cores, offering more flexibility and copatibility with Arm® TrustZone® Consequently, the programming approach used in previous products annot leBasm to easily define start and end of their protected regions.

Table 6. MPU register summary   
MPU_TYPE[15:8] depends on the number of MPU regions configured. This value can be 0, 4, 8, 12, or 16.   

<table><tr><td rowspan=1 colspan=1>AdressName</td><td rowspan=1 colspan=1>Type</td><td rowspan=1 colspan=1>Reset value</td><td rowspan=1 colspan=1>Description</td></tr><tr><td rowspan=1 colspan=1>OxE000ED90</td><td rowspan=1 colspan=1>MPU_TYPE(1)</td><td rowspan=1 colspan=1>RO</td><td rowspan=1 colspan=1>0x0000xx00</td></tr><tr><td rowspan=1 colspan=1>OxE000ED94</td><td rowspan=1 colspan=1>MPU_CTRL</td><td rowspan=1 colspan=1>RW</td><td rowspan=1 colspan=1>Ox00000000MPU Type Register</td></tr><tr><td rowspan=1 colspan=1>OxE000ED98</td><td rowspan=1 colspan=1>MPU_RNR</td><td rowspan=1 colspan=1>RW</td><td rowspan=1 colspan=1>0x000000xXMPU Control Register</td></tr><tr><td rowspan=1 colspan=1>OxE000ED9C</td><td rowspan=1 colspan=1>MPU_RBAR</td><td rowspan=1 colspan=1>RW</td><td rowspan=1 colspan=1>UnknownMPU Region Number Register</td></tr><tr><td rowspan=1 colspan=1>OxE000EDAO</td><td rowspan=1 colspan=1>MPU_RLAR</td><td rowspan=1 colspan=1>RW</td><td rowspan=1 colspan=1>Unknown, bit [0] resets to 0MPU Region Base Address Register</td></tr><tr><td rowspan=1 colspan=1>0xE000EDA4</td><td rowspan=1 colspan=1>MPU_RBAR_A1</td><td rowspan=1 colspan=1>RW</td><td rowspan=1 colspan=1>UnknownMPU Region Limit Address Register</td></tr><tr><td rowspan=1 colspan=1>0xE000EDA8</td><td rowspan=1 colspan=1>MPU_RLAR_A1</td><td rowspan=1 colspan=1>RW</td><td rowspan=1 colspan=1>UnknownMPU Region Base Address Register Alias 1</td></tr><tr><td rowspan=1 colspan=1>0xE000EDAC</td><td rowspan=1 colspan=1>MPU_RBAR_A2</td><td rowspan=1 colspan=1>RW</td><td rowspan=1 colspan=1>UnknownMPU Region Limit Address Register Alias 1</td></tr><tr><td rowspan=1 colspan=1>OxE000EDBO</td><td rowspan=1 colspan=1>MPU_RLAR_A2</td><td rowspan=1 colspan=1>RW</td><td rowspan=1 colspan=1>UnknownMPU Region Base Address Register Alias 2</td></tr><tr><td rowspan=1 colspan=1>OxE000EDB4</td><td rowspan=1 colspan=1>MPU_RBAR_A3</td><td rowspan=1 colspan=1>RW</td><td rowspan=1 colspan=1>UnknownMPU Region Limit Address Register Alias 2</td></tr><tr><td rowspan=1 colspan=1>OxE000EDB8</td><td rowspan=1 colspan=1>MPU_RLAR_A3</td><td rowspan=1 colspan=1>RW</td><td rowspan=1 colspan=1>UnknownAddress Register Alias 3</td></tr><tr><td rowspan=1 colspan=1>OxE000EDCO</td><td rowspan=1 colspan=1>MPU_MAIRO</td><td rowspan=1 colspan=1>RW</td><td rowspan=1 colspan=1>Unknown.MPU Memory Attribute Indirection Register 0</td></tr><tr><td rowspan=1 colspan=1>0xE000EDC4</td><td rowspan=1 colspan=1>MPU_MAIR1</td><td rowspan=1 colspan=1>RW</td><td rowspan=1 colspan=1>UnknownMPU Memory Attribute Indirection Register 1</td></tr></table>

# MPU features comparison between Cortex® cores

There are few MPU differences between Cortex-M0+, Cortex-M3/M4, Cortex-M7, Cortex-M33 and -.emu ahe  bl illustrates these differences.

Table 7. Comparison of MPU features between Cortex cores   

<table><tr><td rowspan=1 colspan=1>Features</td><td rowspan=1 colspan=1>Cortex-M0+</td><td rowspan=1 colspan=1>Cortex-M3/M4</td><td rowspan=1 colspan=1>Cortex-M7</td><td rowspan=1 colspan=1>Cortex-M33</td><td rowspan=1 colspan=1>Cortex-M55</td></tr><tr><td rowspan=1 colspan=1>Number of regions</td><td rowspan=1 colspan=1>8</td><td rowspan=1 colspan=1>8</td><td rowspan=1 colspan=1>8/16 (1)(2)</td><td rowspan=1 colspan=1>8 MPU_S /8MPUNS()</td><td rowspan=1 colspan=1>16 MPU_S / 16MPU_NS</td></tr><tr><td rowspan=1 colspan=1>Region address</td><td rowspan=1 colspan=1>Yes</td><td rowspan=1 colspan=1>Yes</td><td rowspan=1 colspan=1>Yes</td><td rowspan=1 colspan=1>Yes</td><td rowspan=1 colspan=1>Yes</td></tr><tr><td rowspan=1 colspan=1>Region size</td><td rowspan=1 colspan=1>256 bytes to 4bytes</td><td rowspan=1 colspan=1>32 bytes to 4 bytes</td><td rowspan=1 colspan=1>32 bytes to 4bytes</td><td rowspan=1 colspan=1>32 bytes to 4 Gbytes</td><td rowspan=1 colspan=1>32 bytes to 4 Gbytes</td></tr><tr><td rowspan=1 colspan=1>Region memoryattributes</td><td rowspan=1 colspan=1>S, C, B, XN(4)</td><td rowspan=1 colspan=1>TEX, S, C, B, XN</td><td rowspan=1 colspan=1>TEX, S, C, B, XN</td><td rowspan=1 colspan=1>S,C, E (5),G (6), R (7),XN</td><td rowspan=1 colspan=1>S,C, E(5) ,G (6), R (7),XN, PXN(8)</td></tr><tr><td rowspan=1 colspan=1>Region accesspermissson (AP)</td><td rowspan=1 colspan=1>Yes</td><td rowspan=1 colspan=1>Yes</td><td rowspan=1 colspan=1>Yes</td><td rowspan=1 colspan=1>Yes (privileged ornot)</td><td rowspan=1 colspan=1>Yes (privileged or not)</td></tr><tr><td rowspan=1 colspan=1>Subregion disable</td><td rowspan=1 colspan=1>8 bits</td><td rowspan=1 colspan=1>8 bits</td><td rowspan=1 colspan=1>8 bits</td><td rowspan=1 colspan=1>NA</td><td rowspan=1 colspan=1>NA</td></tr><tr><td rowspan=1 colspan=1>MPU bypass forNMI/HardFault</td><td rowspan=1 colspan=1>Yes</td><td rowspan=1 colspan=1>Yes</td><td rowspan=1 colspan=1>Yes</td><td rowspan=1 colspan=1>Yes</td><td rowspan=1 colspan=1>Yes</td></tr><tr><td rowspan=1 colspan=1>Alias of MPUregisters</td><td rowspan=1 colspan=1>No</td><td rowspan=1 colspan=1>Yes</td><td rowspan=1 colspan=1>Yes</td><td rowspan=1 colspan=1>Yes</td><td rowspan=1 colspan=1>Yes</td></tr><tr><td rowspan=1 colspan=1>Fault exception</td><td rowspan=1 colspan=1>HardFault only</td><td rowspan=1 colspan=1>HardFault/MemManage</td><td rowspan=1 colspan=1>HardFault/MemManage</td><td rowspan=1 colspan=1>HardFault/MemManage</td><td rowspan=1 colspan=1>HardFault/MemManage</td></tr></table>

1 For STM32H7 series devices. 2. For STM32F7 series devices. 3. For STM32H5/STM32U3: 12 MPU_S / 8 MPU_NS . 4. - la l 5. Early write acknowledge (similar to bufferable) 6. Gathering 7. Reordering Privileged eXecute Never attribute in Armv8.1-M architecture.

# 6 MPU setting example with STM32Cube HAL on Armv6 and Armv7 architectures

Th table belowdescribes anexample setnguphe MPU with the followigmemory regions: Internal SRAM, flah memory and peripherals.The default memory map is used or privileged accesses as a background region, the MPU is not enabled for the HardFault handler and NMI.

Internal SRAM: 8 Kbytes of internal SRAM is configured as Region0.

Ml l and code execution enabled.

Flash memory: the whole Flash memory is configured as Region.

le wil and code execution enabled.

Peripheral region: is configured as Region2.

Memory attributes: cached and shared device, full access permission and execute never.

Table 8. Example of setting up the MPU   

<table><tr><td rowspan=1 colspan=1>Configuration</td><td rowspan=1 colspan=1>Memory type</td><td rowspan=1 colspan=1>Base address</td><td rowspan=1 colspan=1>Region number</td><td rowspan=1 colspan=1>Memory size</td><td rowspan=1 colspan=1>Memory attributes</td></tr><tr><td rowspan=1 colspan=1>Internal SRAM</td><td rowspan=1 colspan=1>Normal memory</td><td rowspan=1 colspan=1>0x2000 0000</td><td rowspan=1 colspan=1>Region0</td><td rowspan=1 colspan=1>8 Kbytes</td><td rowspan=1 colspan=1>Shareable, write through, no write allocateC = 1, B = 0, TEX = 0, S = 1SRD = 0, XN = 0, AP = full access</td></tr><tr><td rowspan=1 colspan=1>Flash memory</td><td rowspan=1 colspan=1>Normal memory</td><td rowspan=1 colspan=1>0x0800 0000</td><td rowspan=1 colspan=1>Region1</td><td rowspan=1 colspan=1>1 Mbyte</td><td rowspan=1 colspan=1>Non-shareable write through, no write allocateC = 1, B = 0, TEX = 0, S = 1SRD = 0, XN = 0, AP = full access</td></tr><tr><td rowspan=1 colspan=1>FMC</td><td rowspan=1 colspan=1>Device memory</td><td rowspan=1 colspan=1>0x4000 0000</td><td rowspan=1 colspan=1>Region2</td><td rowspan=1 colspan=1>512 Mbytes</td><td rowspan=1 colspan=1>Shareable, write through, no write allocateC = 1, B = 0, TEX = 0, S = 1SRD = 0, XN = 1, AP = full access</td></tr></table>

# Setting the MPU with STM32Cube HAL

void MPU_RegionConfig(void) MPU_Region_InitTypeDef MPU_InitStruct;   
/\* Disable¯MPU \*/ HAL_MPU_Disable();   
/\* Configure RAM region as Region N°O, 8kB of size and R/W region \*/ MPU_InitStruct.Enable = MPU_REGION_ENABLE;   
MPU_InitStruct.BaseAddress = Ox20000000;   
MPU_InitStruct.Size = MPU_REGION_SIZE_8KB;   
MPU_InitStruct.AccessPermission = MPU_REGION_FULL_ACCESS;   
MPU_InitStruct.IsBufferable = MPU_ACCESS_NOT_BUFFERABLE;   
MPU_InitStruct.IsCacheable = MPU_ACCESS_CACHEABLE;   
MPU_InitStruct.IsShareable = MPU_ACCESS_SHAREABLE;   
MPU_InitStruct.Number = MPU_REGION_NUMBERO;   
MPU_InitStruct.TypeExtField¯= MPU_TEX_LEVELO;   
MPU_InitStruct.SubRegionDisable = Ox00;   
MPU_InitStruct.DisableExec = MPU_INSTRUCTION_ACCESS_ENABLE;   
HAL_MPU_ConfigRegion(&MPU_InitStruct);   
/\* Configure FLASH region¯as REGION N°1, 1MB of size and R/W region \*/ MPU_InitStruct.BaseAddress = Ox08000000;   
MPU_InitStruct.Size = MPU_REGION_SIZE_1MB;   
MPU_InitStruct.Number = MPU_REGION_NUMBER1;   
HAL_MPU_ConfigRegion(&MPU_InitStruct);   
/\* Configure FMC region as REGION N°2, 0.5GB of size, R/W region \*/ MPU_InitStruct.BaseAddress = Ox40000000;   
MPU_InitStruct.Size = MPU_REGION_SIZE_512MB;   
MPU_InitStruct.IsShareable = MPU_ACCESS_SHAREABLE;   
MPU_InitStruct.Number = MPU_REGION_NUMBER2; MPU InitStruct.DisableExec = MPU INSTRUCTION ACCESS DISABLE; HAL_MPU_ConfigRegion(&MPU_InitStruct);   
/\* Enable MPU \*/   
HAL_MPU_Enable(MPU_PRIVILEGED_DEFAULT);

# MPU setting example with STM32Cube HAL on Armv8-M architecture

T abe be ee apleeAru witeol regions: internal SRAM, internal flash memory and peripherals.

# Internal SRAM

Region number 0 with a size of 256 KB Memory attributes: normal, non-cacheable, full access permission, code execution enabled

# Internal flash memory

Region number 1 with a size of 2 MB   
Memory attributes:normal, write through and no write allocate, ful access permission, code execution   
enabled

# Peripherals

Region number 2 with a size of 512 MB Memory attributes: device nGnRE, full access permission, code execution disabled

Table 9. Example of setting up the MPU with Armv8-M   

<table><tr><td rowspan=1 colspan=1>Configuration</td><td rowspan=1 colspan=1>Memorytype</td><td rowspan=1 colspan=1>Baseaddress</td><td rowspan=1 colspan=1>Regionnumber</td><td rowspan=1 colspan=1>Memory size</td><td rowspan=1 colspan=1>Memory attributes</td></tr><tr><td rowspan=1 colspan=1>Internal SRAM</td><td rowspan=1 colspan=1>Normalmemory</td><td rowspan=1 colspan=1>0x2000 0000</td><td rowspan=1 colspan=1>Region0</td><td rowspan=1 colspan=1>256 Kbytes</td><td rowspan=1 colspan=1>Memory attribute = normal, non-cacheable.XN = 0AP = full accessS = 0</td></tr><tr><td rowspan=1 colspan=1>Flash memory</td><td rowspan=1 colspan=1>Normalmemory</td><td rowspan=1 colspan=1>0x0800 0000</td><td rowspan=1 colspan=1>Region1</td><td rowspan=1 colspan=1>2 Mbyte</td><td rowspan=1 colspan=1>Memory attribute = normal, write through and nowrite allocate.XN = 0AP = full accessS = 0</td></tr><tr><td rowspan=1 colspan=1>Peripherals</td><td rowspan=1 colspan=1>Device</td><td rowspan=1 colspan=1>0x4000 0000</td><td rowspan=1 colspan=1>Region2</td><td rowspan=1 colspan=1>512 Mbytes</td><td rowspan=1 colspan=1>Memory attribute = device nGnREXN = 1AP = full accessS = 0</td></tr></table>

# Setting the MPU with STM32Cube HAL

void MPU_Config(void)   
MPU_Region_InitTypeDef MPU_InitStruct;   
MPU_Attributes_InitTypeDef¯MPU_AttributesInit;   
/\* Disable MPU \*/   
HAL_MPU_Disable();   
/\* Configure RAM region as Region Number O, 256KB of size \*/ MPU_AttributesInit.Number = MPU_ATTRIBUTES_NUMBERO;   
MPU_AttributesInit.Attributes =¯INNER_OUTER(MPU_NOT_CACHEABLE); HAL_MPU_ConfigMemoryAttributes(&MPU_AttributesInit);   
MPU_InitStruct.Enable = MPU_REGION_ENABLE;   
MPU_InitStruct.BaseAddress = Ox20000000; MPU_InitStruct.LimitAddress = Ox2003FFFF;   
MPU_InitStruct.AccessPermission = MPU_REGION_ALL_RW;   
MPU_InitStruct.AttributesIndex = MPU_ATTRIBUTES_NUMBERO;   
MPU_InitStruct.IsShareable = MPU_ACCESS_NOT_SHAREABLE;   
MPU_InitStruct.Number = MPU_REGIÖN_NUMBERO;   
MPU_InitStruct.DisableExec = MPU_INSTRUCTION_ACCESS_ENABLE;   
HAL_MPU_ConfigRegion(&MPU_InitStruct);   
/\* Configure FLASH region as REGION Number 1, 2M of size \*/ MPU_AttributesInit.Number = MPU_ATTRIBUTES_NUMBER1;   
MPU_AttributesInit.Attributes =¯INNER_OUTER(MPU_WRITE_THROUGH|MPU_R_ALLOCATE);   
HAL_MPU_ConfigMemoryAttributes(&MPU_AttributesInit);   
MPU_InitStruct.Enable = MPU_REGION_ENABLE;   
MPU_InitStruct.BaseAddress = Ox08000000;   
MPU_InitStruct.LimitAddress = Ox081FFFFF;   
MPU_InitStruct.AccessPermission = MPU_REGION_ALL_RW;   
MPU_InitStruct.AttributesIndex = MPU_ATTRIBUTES_NUMBER1;   
MPU_InitStruct.IsShareable = MPU_ACCESS_NOT_SHAREABLE;   
MPU_InitStruct.Number = MPU_REGION_NUMBER1;   
MPU_InitStruct.DisableExec = MPU_INSTRUCTION_ACCESS_ENABLE;   
HAL_MPU_ConfigRegion(&MPU_InitStruct);   
/\* Configure Peripheral region as REGIoN Number 2, 512MB of size, Execute Never region \*/ MPU_AttributesInit.Number = MPU_ATTRIBUTES_NUMBER2;   
MPU_AttributesInit.Attributes = MPU_DEVICE_nGnRE;   
HAL_MPU_ConfigMemoryAttributes(&MPU_AttributesInit);   
MPU_InitStruct.BaseAddress = Ox40000000;   
MPU_InitStruct.LimitAddress = Ox5FFFFFFF;   
MPU_InitStruct.AccessPermission = MPU_REGION_ALL_RW;   
MPU_InitStruct.AttributesIndex = MPU_ATTRIBUTES_NUMBER2;   
MPU_InitStruct.IsShareable = MPU_ACCESS_NOT_SHAREABLE;   
MPU_InitStruct.Number = MPU_REGION_NUMBER2;   
MPU_InitStruct.DisableExec = MPU_INSTRUCTION_ACCESS_DISABLE;   
/\* Enable MPU \*/ HAL_MPU_Enable(MPU_PRIVILEGED_DEFAULT);   
1

# 8 Conclusion

Using the MPU in the STM32 microcontroers makes them robust, reliable and in some cases more secure by preventinghepliatin skfoacesioutinetacka atemoyse yhehesks.

Ti a tePU i 2ubALowuPTM3 MCUs.

For more details about the MPU register, refer to the Cortex® core programming manuals.

# Revision history

Table 10. Document revision history   

<table><tr><td rowspan=1 colspan=1>Date</td><td rowspan=1 colspan=1>Revision</td><td rowspan=1 colspan=1>Changes</td></tr><tr><td rowspan=1 colspan=1>24-Mar-2016</td><td rowspan=1 colspan=1>1</td><td rowspan=1 colspan=1>Initial release.</td></tr><tr><td rowspan=1 colspan=1>04-May-2018</td><td rowspan=1 colspan=1>2</td><td rowspan=1 colspan=1>Added STM32H7 series in the whole document.Updated Figure 1. Example of overlapping regions..Added Section 1 General informationAdded Section 3.4 Cortex-M7 constraint speculative prefetch.</td></tr><tr><td rowspan=1 colspan=1>17-Jul-2019</td><td rowspan=1 colspan=1>3</td><td rowspan=1 colspan=1>Updated Introduction adding STM32G0 series, STM32G4 series,STM32L4+ series, STM32L5 series and STM32WB series.</td></tr><tr><td rowspan=1 colspan=1>10-Feb-2020</td><td rowspan=1 colspan=1>4</td><td rowspan=1 colspan=1>Added:PM0214 in Section IntroductionSection 4 Memory types, registers and attributes of the CM33Section 5 Comparison of MPU features between Cortex-M0+,Cortex-M3/M4, Cortex-M7, and Cortex-M33Updated:title of the documentSection IntroductionSection 2 OverviewSection 2.1 Memory model</td></tr><tr><td rowspan=1 colspan=1>20-Sep-2021</td><td rowspan=1 colspan=1>5</td><td rowspan=1 colspan=1>Updated the Applicable products table.</td></tr><tr><td rowspan=1 colspan=1>07-Feb-2023</td><td rowspan=1 colspan=1>6</td><td rowspan=1 colspan=1>Added the STM32C0 series and STM32H5 series in Table 1.Applicable products.Updated the Section 6: MPU setting example with STM32Cube HAL onArmv6 and Armv7 architectures.Updated the whole document with minor changes.Updated the document title.</td></tr><tr><td rowspan=1 colspan=1>04-Mar-2024</td><td rowspan=1 colspan=1>7</td><td rowspan=1 colspan=1>Added the STM32U0 series in Table 1. Applicable products.</td></tr><tr><td rowspan=1 colspan=1>04-Apr-2024</td><td rowspan=1 colspan=1>8</td><td rowspan=1 colspan=1>Added:STM32WB0 series in Table 1. Applicable productsSection 3.2: MPU register description</td></tr><tr><td rowspan=1 colspan=1>15-Jan-2025</td><td rowspan=1 colspan=1>9</td><td rowspan=1 colspan=1>Added STM32N6 series.Updated:Section 2.1: Memory modelSection 4.2: Attribute indirectionSection 4.3: MPU registersAdded Section 4.1.1: Cortex®-M55 access privilege level for deviceand normal memory.</td></tr><tr><td rowspan=1 colspan=1>25-Feb-2025</td><td rowspan=1 colspan=1>10</td><td rowspan=1 colspan=1>Added STM32U3 series.Updated:Section IntroductionSection 2: OverviewSection 4.3: MPU registersSection 4: Cortex-M33/M55 memory types, registers andattributesSection 5: MPU features comparison between Cortex® coresAdded Section 7: MPU setting example with STM32Cube HAL onArmv8-M architecture.</td></tr></table>

# Contents

1 General information 2 Overview 2.1 Memory model.

# 3 Cortex-M0+/M3/M4/M7 memory types, registers and attributes.

3.1 Memory types   
3.2 MPU register description   
3.3 Memory attributes   
3.4 Cortex-M7 constraint speculative prefetch. 9

# 1 Cortex-M33/M55 memory types, registers and attributes. 10

4.1 Memory types and attributes 10   
4.1.1 Cortex®-M55 access privilege level for device and normal memory 10   
4.2 Attribute indirection 11   
4.3 MPU registers 12

# MPU features comparison between Cortex® cores. 13

# MPU setting example with STM32Cube HAL on Armv6 and Armv7 architectures . ..14

MPU setting example with STM32Cube HAL on Armv8-M architecture . .16

# Conclusion 18

# Revision history 19

# .ist of tables 21

# List of figures. .22

# List of tables

Table 1. Applicable products.   
Table 2. Default memory map for the Cortex-M55 processor 6   
Table 3. Region attributes and size in MPU_RASR register 7   
Table 4. Access permissions of regions. 8   
Table 5. Cache properties and shareability 8   
Table 6. MPU register summary . 12   
Table 7. Comparison of MPU features between Cortex cores. 13   
Table 8. Example of setting up the MPU 14   
Table 9. Example of setting up the MPU with Armv8-M. 16   
Table 10. Document revision history . 19

# List of figures

Figure 1. Example of overlapping regions 3   
Figure 2. Cortex-M0+/M3/M4/M7 processor memory map 4   
Figure 3. Cortex-M33 processor memory map 5   
Figure 4. Attribute indirection example 11

# IMPORTANT NOTICE  READ CAREFULLY

pt old ursant  dits   leole.

purchasers' products.

No license, express or implied, to any intellectual property right is granted by ST herein.

are the property of their respective owners.

I

© 2025 STMicroelectronics - All rights reserved