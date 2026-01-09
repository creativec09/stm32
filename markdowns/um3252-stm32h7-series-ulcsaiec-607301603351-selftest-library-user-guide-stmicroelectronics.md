# STM32H7 series UL/CSA/IEC 60730-1/60335-1 self-test library user guide

# Introduction

-B Arm® Cortex®-M7 core. Order code X-CUBE-CLASSB-H7.

arcontinuously evolving, and are regularly incorporated into updated versions of the safety standards.

T. clCL standards association (CSA) authorities.

(mostly operating in Europe), and the UL and the CSA (targeting mainly the USA and Canadian markets).

Saraavy a va t microcontrollers, such as the CPU or memories.

T compiler version or combined with the latest firmware drivers. This is generally a common practice.

Table 1. Applicable product   

<table><tr><td>Part number</td><td>Order code</td></tr><tr><td>X-CUBE-CLASSB</td><td>X-CUBE-CLASSB-H7</td></tr></table>

# 1 General information

# 1.1

# Purpose and scope

This document applies to the X-CUBE-CLASSB self-test library set dedicated for STM32H7 series microcontrollers that embed an Arm® Cortex®-M7. This X-CUBE-CLASSB-H7 expansion package provides application independent software to comply with the UL/CSA/IEC 60730-1 safety standard. The UL/CSA/IEC 3saey andartarget heafyutaticelectical controls usnassciaton withhouol equipment and similar electronic applications.

The main purpose of this software library is to facilitate and accelerate:

user software development certification processes or applications which are subject to theassociated requirements and certifications.

The X-CUBE-CLASSB-H7 expansion package runs on the Cortex®-M7 embedded in the STM32H7 series microcontrollers.

arm

# Note:

Arm is a registered trademark of Arm limited (or its subsidiaries) in the US and/or elsewhere.

Thersnhliatndepende aibrar elstbrayvalble X-UBE CLASSB-H7 expansion package (and associated to this manual), STL_Lib_product_x1. a and STL_Lib_product_x2.a file, is V4.0.0.

# 1.2

# Reference documents

[1UM2331: STM32H7 Series safety manual dedicated for applications targeting industrial safety

ieltaL/CSA07360latcati 32ppltio to older versions of this library

# 2 STM32Cube overview

# 2.1 What is STM32Cube?

2Cuielcrongalvproeivianty development effort, time, and cost. STM32Cube covers the whole STM32 portfolio.

STM32Cube includes:

A set of user-friendly software development tools to cover project development from conception to realization, among which are:

STM32CubeMX, a graphical software configuration tool that allows the automatic generation of C   
initialization code using graphical wizards   
STM32CubelDE, an all-in-one development tool with peripheral configuration, code generation, code   
compilation, and debug features   
STM32CubeCLT, an all-in-one command-line development toolset with code compilation, board   
programming, and debug features   
STM32CubeProgrammer (STM32CubeProg), a programming tool available in graphical and   
command-line versions   
STM32CubeMonitor (STM32CubeMonitor, STM32CubeMonPwr, STM32CubeMonRF,   
STM32CubeMonUCPD), powerful monitoring tools to fine-tune the behavior and performance of   
STM32 applications in real time

STM32Cube MCU and MPU Packages, comprehensive embedded-software platforms specific to each microcontroller and microprocessor series (such as STM32CubeH7 for the STM32H7 series), which include:

STM32Cube hardware abstraction layer (HAL), ensuring maximized portability across the STM32   
portfolio   
STM32Cube low-layer APls, ensuring the best performance and footprints with a high degree of user   
control over hardware   
A consistent set of middleware components such as RTOS, USB Host and Device, TCP/IP,   
mbedTLS, FAT file system, audio, and graphicsRTOS, USB, and graphics   
All embedded software utilities with full sets of peripheral and applicative examples

STM32Cube Expansion Packages, which contain embedded software components that complement the functionalities of the STM32Cube MCU and MPU Packages with:

Middleware extensions and applicative layers Examples running on some specific STMicroelectronics development boards

# How does this software complement STM32Cube?

The software expansion package extends STM32Cube by a middleware component t manage specific softwarebased diagnostics.

Th packae roves agen sartig point helpauerbuild anfnaliaplicatispecy solutions. It consists of:

STLhe sef-test library.This provides a binary and some source code to manage the execution  gnric safety tests for the microcontroller. The STL is a standalone unit, which runs independently from any STM32 software. It collects the self-tests for generic components of the microcontroller. User application: This is an STL integration example based on a set of STM32Cube drivers extending the STL by an application speciic test.This part is delivered as full source code to be adapted or extended by calling of additional application specific modules defined by end user. The example can be used for the library testing including artificial failing support of all the provided modules.

# 3 STL overview

TT plicatnneenrae  MTe te petainelvanubsymeani qu ye ClasBelaty aplicableo STM32H7 seris microcontrollers. he STL is n HAL / LLindependent library, dedicate the microcontrollers. The STL is a compilation tool chain-agnostic, so any standard C-compiler can compilet.

The STL is an autonomous software. It executes, on application-demand, selected tests to detect hardware issues, and reports the outcomes to the application.

definitions and the user parameter settings.

# Architecture overview

The STL implements tests required by UL/CSAIEC 60730-1 for the Arm® Cortex®-M7 CPU core, and the volatile and nonvolatile memories embedded in the product.

e of:

User application (indicated in light blue)   
User parameters (indicated in light blue)   
STLheduler ndicate n yellow): detaccessible by teuseapplication  useAPs notgoi through HAL / LL)   
STL internal test modules: called by the STL scheduler (not visible to the user application).

he STL status information returned to the user application at AP/ level (summarized in Table ) is • Function return value collects result of internal defensive programming checks.

Temoduleresult aluetores he est result foration.Thi partiallycoepon nternal ta the module (see Section 7.3: State machines).

![](images/19be91b91e2b9221bb44b8fe0642d0acfd213835727549ed29d97b07d3e8e3b7.jpg)  
Figure 1. STL architecture

STL User

Tlle eveoetal atuTeeveo an hecep user API.

# 2 Supported products

The TLruns on he TM32H seris microcontrollers featuring he same design and integration f the Corte® M7 core and the embedded memories.

Products associated to the STL_Lib_product_x1.a file:

STM32H723xx STM32H725xx STM32H730xx STM32H730xxQ STM32H733xx STM32H735xx STM32H742xx STM32H743xx STM32H750xx STM32H753xx

Products associated to the STL_Lib_product_x2.a file:

• STM32H7A3xx STM32H7A3xxQ STM32H7B0xx STM32H7B0xxQ STM32H7B3xx STM32H7B3xxQ

# Note:

Due to dfferent peripheral memory mappings in the STM32H7 single-core product family used by the STL (see t2fetwelivThesas elche be added in the IDE project settings (see Section 5.5.2: Steps to build an application from scratch).

# 4 STL description

This section describes basiinformation on he functionality and performanceof theTL.The sectinlso summarizes restrictions and mandatory actions to be followed by the end user.

# 4.1

# STL functional description

Some test modules can temporarily mask interrupts.For more details, refer o Section 4..: STL interrupt masking time and to Section 4.3.5: Interrupt management.

# 4.1.1

# Scheduler principle

The scheduler is the API module needed by the user application to execute the STL. The main scheduler:

Must be initialized before being used

Manages:

The initialization and deinitialization of the applied test modules The configuration of the applied test modules The reset of the applied test modules.

Controls the execution of an applied test sequence (API calls)

Manages "artificial failing" used for user debug and integration tests.

Ensures the integrity of critical internal data structures via their specific checksums.

The scheduler controls the execution of the following tests:

CPU tests: o speciinitialization r coniguration procedures f thePU test module aerequir befoe any CPU test execution (see Section 7.2: User APIs and Figure 11).

Flash memory teerateon he content heedicateconfiguration structure definng uset e memory to be tested (see Section 7.: User structures). These structures must be filled by the end user and the content maintained during both configuration and execution of the flash memory test. The test module initialization and configuration procedures are mandatory before any flash memory test execution, see Section 7.2: User APls and Figure 12.

RAM memory estsoperate on the content of thededicated configuration structures defining subsets  the memory to be tested (see Section 7.: User structures). These structures must be filled by the end user and the content maintained during both configuration and execution of the RAM test. RAM test module initialization and configuration procedures are mandatory before RAM test execution, see Section 7.2: User APIs and Figure 13.

euPl he lTL l context, but reentrance is forbidden. In such cases, the STL behavior cannot be guaranteed.

Tplne data structure collecting status information. See details in the following table.

Table 2. STL return information   
Figure 2. Single test control call architecture   

<table><tr><td rowspan=1 colspan=1>STL information</td><td rowspan=1 colspan=1>Value</td><td rowspan=1 colspan=1>Description</td></tr><tr><td rowspan=2 colspan=1>Function return value(1)</td><td rowspan=1 colspan=1>STL_OK</td><td rowspan=1 colspan=1>Scheduler function successfully executed</td></tr><tr><td rowspan=1 colspan=1>STL_KO</td><td rowspan=1 colspan=1>Scheduler defensive programming error (in this case thetest result is not relevant)</td></tr><tr><td rowspan=5 colspan=1>Test module result value(2)</td><td rowspan=1 colspan=1>STL_PASSED</td><td rowspan=1 colspan=1>Test passed</td></tr><tr><td rowspan=1 colspan=1>STL_PARTIAL_PASSED</td><td rowspan=1 colspan=1>Used only for memory testing when the test passed, butthe end of memory configuration has not yet beenreached</td></tr><tr><td rowspan=1 colspan=1>STL_FAILED</td><td rowspan=1 colspan=1>Hardware error detection by test module</td></tr><tr><td rowspan=1 colspan=1>STL_NOT_TESTED</td><td rowspan=1 colspan=1>Test not executed</td></tr><tr><td rowspan=1 colspan=1>STL_ERROR</td><td rowspan=1 colspan=1>Test module defensive programming error</td></tr></table>

1.Refer to STL_Status_t definition in Section 7.1: User structures. 2. See STL_TmSTatus_t in Section 7.1: User structures.

pi palno eile u sequence of API function calls and so handle the order of the test modules execution.

![](images/01ae270c5d07bb1716775364ebb48000d02c5e2229c626f4c183d10c38e6ba1a.jpg)

# Scheduler and interrupts

The scheduler can be interrupted at any time.

# 4.1.2 CPU Arm® core tests

TTcudesU dules t elow gether wi  eneptin oaon the test capability:

TM1L: implements a light pattern test of general-purpose registers TM7: implements the pattern and functional tests of both stack pointers: MSP, and PSP TMCB: implements test of the APSR status register.

# Caution:

Th TLPU tests are partitiein separated es modules. his is otintended oallow partial execuion vs  tle ul uerapplications, o example timing constraints.B default, all availables reassumed to beexeue.

# CPU Arm® core tests and interrupts

The CPU test modules are interruptible at any time. The TM7 one only applies masking interrupt during the ll a anuariyR SecInterrtmentetinoati interrupt management.

# 1.1.3 Flash memory tests

# Principles

he flash test concerns the embedded flash memory of STM32H7 series.

The following structures must be respected to provide correct configuration of the flash memory test.

Block: a contiguous area of 4 bytes (FLASH_BLOCK_SIZE), hard coded by STL. Section: a contiguous area of 1024 bytes (FLASH_SECTION_SIZE), hard coded by the STL. This has no i with hememory physial seco. Thememory is partte in ectins.Te section start first address of the memory, and the following sections are contiguous with each other. The user must ensure proper calculation and placement of the CRC checksum for each section that is to be checked during the memory integrity test.

• By (name user program Figure) a contiguous are code provided by the compiler. It start at the beginning  a section It usuallyends with an incompletesection when thebinary are ize isot a multiple of the section size. Inal ases, the binary must be 32-bit aligned (see RC tool information below).

Subse: a contiguous area of sections defined by the user. The user application can define one subset or seval subsets.A subset has to bedefined within a binary area. Its start address has tobealign wth the beginning of a section. It can only include sections with the corresponding precalculated CRC values. When the ast sectiona subset  the last par o the binary thesection may beincompleTheu aatinas algn e eset with ere ebinay ar sections is tested exclusively, the subset end address has to be aligned with the end of the last-ested section.

The subset is calculated as follows:   
Subset size = K \* FLASH_SECTION_SIZE + L \* FLASH_BLOCK_ SIZE   
where: K is an integer greater than 0.   
0 ≤ L < (FLASH_SECTION_SIZE / FLASH_BLOCK_SIZE) when L > 0 the last section of a binary is incomplete.

The user application defines single or multiple subsets as well as their associated test sequences.

Tpt io configuration structures):

Tests are performed on sections of one or more subsets defined by the user application. Test are peforme either ina row one shot)or partially in a singeatomic step or a number secons defined by the user application. Test results are based on a CRC comparison between the computed CRC value (calculated during test execution) and an expected CRC value (calculated before software binary flashing).

The mandatory steps (for the user application) to perform flash memory tests are

Test initialization   
Configuration of one or more subsets Execution of the test.

Onc all subsets are testedthe userneeds to reset the flash memory test module to perform the test gain. In tecase   STLERROR / STLFAILED estresult, he estmodule s stuck a the failmemoy sbt. In this casedeinitalize,nitialize and reconfigure the flas memory test prior ouning itgain.

# Expected CRC precalculation

The fashmemory tst isbased onhe builthardwarRCuni or softwareRC,which  configurable y fThe default configuration is with he hardwareRC.o use the softwareRC, the fagTLWRCmust bl  in e Scn .Stes bul pl .Te CRC compliant with IEEE 802.3.

Phe moy Rahe    e h n CRC patten.Theuser mustensure that valid RC patterns arecalculated and stored inthe field orllthe sections to be tested. This is shown in Figure 3.

O laa Tmeansha stablc peeinalyay al wi ecn  Ina sRhevalhpcipelc and tested exclusively over the section part that overlays the binary area.

# Preconditions:

The user program areas have to start at the beginning of a section   
The boundaries of the user program areas must be 32-bit aligned.   
Depending on total flash memory size and on user program size, last program data and first CRC data may be both stored in the same flash section (without any overlap). In that case, theCRC must be compute on the user program data only, see example 3 in Figure 4. Flash memory test:CRC use cases versus program areas.

# ST CRC tool information

ST provides a CRC precalculation tool. This tool is available as a single feature inside the S2CubeProgrammer (e Section ..CRC tol et-p), which autmatiall fil he binary wih padig bits (0x00 pattern) for a 32-bit alignment.

![](images/a9ea3f4f1a3ea7636ddac9cee6880f2e2e1e3cd5073e089ce498f05dad0519f2.jpg)  
Figure 3. Flash memory test: CRC principle

CRC area

Flash memory

CRC value (32-bit)

Flash memory section (1 Kbyte)

![](images/aa08213629ba01e6e94293376c37a80530b11168e2309788505f438a621f529b.jpg)  
Figure 4. Flash memory test: CRC use cases versus program areas

Use case descriptions illustrated in Figure 4:

Example 1: the user program starts at the ROM_START address, so CRCs are stored from the CRC_START address.   
Example 2: the user program starts at the beginning of a section, but not at ROM_START. The stored CRCs start at the right address of the CRC area.   
Example 3: the user program uses the full program area, so the last program data and the first CRC data are both stored in the same memory section (without any overlap).   
Example : he user program is defined in three separated areas. This requires three separated areas for the CRC data.

CRC start address computation:

Real calculation:   
CRC_START addreSs = (uint32_t \*)(ROM_END - 4 \* (ROM_END + 1 - ROM_START) /   
(FLASH_SECTION_SIZE) + 1); with FLASH_SECTION_SIZE = 1024   
Textual translation:   
CRC_START = ROM_END - (CRC size in bytes) \* (number of the memory sections) + 1

# Flash memory test and interrupts

Flash memory TM is interruptible at any time.

# 4.1.4

# RAM tests

# Principles

The RAM test concerns the embedded SRAM memories of STM32H7 series.   
The following structures must be respected to provide correct configuration of the RAM test. Block: a contiguous area of 16 bytes (RAM_BLOCK_SIZE), hard coded by the STL (no link with the memory physical sectors).   
Section: a contiguous area of 128 bytes (RAM_SECTION_SIZE), hard coded by the STL.   
Subset: a contiguous area, with the size being a multiple of two blocks and with a 32-bit aligned start ares.A subset sis ot necessariy a multple  the section iebecause he last part  a su can be less than one section.

Subset size = N \* RAM_SECTION_SIZE + 2 \* M \* RAM_BLOCK_SIZE, where:

N is an integer ≥ 0 M is an integer 0 ≤ M < 4, when M > 0, the size of the last partial subset not aligned with section size.

The user application defines single or multiple subsets as well as their associated test sequences.

The STL implements a RAM memory test with the following principles (based on actual content of the user configuration structures):

RAM tests are performed on RAM blocks defined by the user application   
RAM tests are performed either in a row (one shot), or partilly in a single atomic step for a number of   
sections defined by the user application   
The test implementation is based on the March C- algorithm   
RAM tests are performed on RAM content (not on DCache content)

The mandatory steps (for the user application) to perform RAM tests are:

Initialization of RAM test   
Configuration of one or more RAM subsets   
Execution of the RAM test

hepmuseAM ulr peoe In th as TLERROR / TLFAILE esult, e ule uc nheaime . In this case, deinitialize, initialize and reconfigure the RAM prior to running the test again.

# RAM test and interrupts

TheRAM TMisnteruptible  y time excpt during he executin themallest dat granularybloc dei  Sectin .Linterrupt masking ime.Thi s when he interrpts nd Cort®ex cnfigurable prirityae teorarlymaske deauleer Secti ..Interup mag detailed information on interrupt management during RAM March-C tests.

# March C- test principle and memory backup principle

The RAM test is based on a March C-algorithm wherememory is overwritten by speci patterns and then rd eorestohenmeocnteack pabl pe u.I a eerus eaceutiAsu uatT A the user is tested). The backup process can be optionally disabled if it is not required. Refer to Section 4.3.8: RAM backup buffer for detailed information on the buffer control and allocation.

![](images/25aac1e84c3b5b9344f8a0d89681e03358cc227147c7f6620b7663605d645ca3.jpg)  
Figure 5. RAM test: usage

# 4.2

# STL performance data

The data is obtained with the following test set-up:

STL library compilation details, described in Application: compilation process.

Projects for performance tests are compiled with IAR Embedded Workbench® for Arm® (EWARM) toolchain v9.30.1

• Compiled software configuration with:

CPU clock set to 400 MHz   
Flash memory latency set to four wait states   
Flash prefetch enabled   
NUCLEO-H743ZI (MB1137 Rev B)

# 1.2.1 STL execution timings

A summary of the STL execution timings when an optimal default STL settings are applied is shown in the following table. The measurements for each AP are detailed in Section 9:TL: execution timing details.

Table 3. STL execution timings, clock at 400 MHz   

<table><tr><td rowspan=1 colspan=1>Testedmodule</td><td rowspan=1 colspan=2>Conditions</td><td rowspan=1 colspan=1>Result inμs</td></tr><tr><td rowspan=1 colspan=1>CPU</td><td rowspan=1 colspan=2>TM1L, TM7, TMCB</td><td rowspan=1 colspan=1>9</td></tr><tr><td rowspan=4 colspan=1>Flashmemory</td><td rowspan=2 colspan=1>Default configuration (STL_SW_CRC not enabled)</td><td rowspan=1 colspan=1>1 Kbyte tested</td><td rowspan=1 colspan=1>10</td></tr><tr><td rowspan=1 colspan=1>34 Kbytes tested</td><td rowspan=1 colspan=1>267</td></tr><tr><td rowspan=2 colspan=1>STL_SW_CRC enabled</td><td rowspan=1 colspan=1>1 Kbyte tested</td><td rowspan=1 colspan=1>25</td></tr><tr><td rowspan=1 colspan=1>34 Kbytes tested</td><td rowspan=1 colspan=1>766</td></tr><tr><td rowspan=2 colspan=1>RAM</td><td rowspan=2 colspan=1>Default configuration (neitherSTL_DISABLE_RAM_BCKUP_BUF, norSTL_ENABLE_IT are enabled</td><td rowspan=1 colspan=1>128 bytes tested</td><td rowspan=1 colspan=1>107</td></tr><tr><td rowspan=1 colspan=1>1015 Kbytes tested</td><td rowspan=1 colspan=1>182525</td></tr></table>

# 4.2.2

# STL code and data size

The STL code and data sizes are detailed in the following table

Table 4. STL code size and data size (in bytes)   

<table><tr><td rowspan=1 colspan=1>Configuration</td><td rowspan=1 colspan=1>Module</td><td rowspan=1 colspan=1>Flash memorycode</td><td rowspan=1 colspan=1>Flash memoryRO-data</td><td rowspan=1 colspan=1>R/Wdata</td></tr><tr><td rowspan=3 colspan=1>STL_SW_CRC not enabled,andSTL_DISABLE_RAM_BCKUP_BUF not enabled</td><td rowspan=1 colspan=1>stl_user_param_template.o</td><td rowspan=1 colspan=1>-</td><td rowspan=1 colspan=1>6</td><td rowspan=1 colspan=1>44</td></tr><tr><td rowspan=1 colspan=1>stl_util.o</td><td rowspan=1 colspan=1>286</td><td rowspan=1 colspan=1></td><td rowspan=1 colspan=1>8</td></tr><tr><td rowspan=1 colspan=1>STL_Lib__product_xl.a orSTL_Lib__product_x2.a</td><td rowspan=1 colspan=1>5058</td><td rowspan=1 colspan=1>1455</td><td rowspan=1 colspan=1>184</td></tr><tr><td rowspan=2 colspan=1>STL_SW_CRC enabled, andSTL_DISABLE_RAM_BCKUP</td><td rowspan=1 colspan=1>stl__user_param_template.o</td><td rowspan=1 colspan=1></td><td rowspan=1 colspan=1>6</td><td rowspan=1 colspan=1>44</td></tr><tr><td rowspan=1 colspan=1>stl_util.o</td><td rowspan=1 colspan=1>150</td><td rowspan=1 colspan=1>-</td><td rowspan=1 colspan=1>4</td></tr><tr><td rowspan=1 colspan=1>_BUF not enabled</td><td rowspan=1 colspan=1>STL_Lib_product_xl.aorSTL_Lib_product_x2.a</td><td rowspan=1 colspan=1>5058</td><td rowspan=1 colspan=1>1455</td><td rowspan=1 colspan=1>184</td></tr></table>

# 4.2.3

# STL stack usage

The minimum stack-available space required by the STL to execute available APls, the number TBD.

# 4.2.4

# STL heap usage

The STL never uses dynamic allocation, therefore the heap size is independent of the STL.

# 4.2.5

# STL interrupt masking time

Th T32 nterrupts, ndCortex® exceptions with conigurable priorit ae askedmultiple times by te STL uring he eecuti PU TM7 an RAM es.s hown  he ollowig table he maxiuterrupt aski time is obtained for a RAM test.

Table 5. STL maximum interrupt masking information   

<table><tr><td>Tested module</td><td>Duration (max) in µs</td><td>Steps</td></tr><tr><td>RAM</td><td>53(1)</td><td>Each execution of STL_SCH_RunRamTM function performs a series of interrupt masking during partial steps of the test at the following time durations: 53 µs for optional DCache disable • 1 µs for backup buffer 1 µs for the first RAM block to be tested 1 µs for each middle RAM block to be tested(2) . 1 µs for the last RAM block to be tested</td></tr><tr><td>TM7</td><td>1</td><td>32 µs for optional DCache enable Masked twice for 1 µs</td></tr></table>

1.1 if DCache is not enabled.

?. NuAM bocultRAM_BLOCKSIZEqvol icRAM content of user structures (size of defined subset(s) versus atomic step - see Section 4.1.4 RAM tests)

# 4.2.6

# Data cache performance impact

This section applies in cases where the DCache is enabled by the user.

Bydesign, heSTL perorms a DCache flush each time he AM tes isnvoked  therelated perforan os kheeqen eacun Tust kencnt user to define the size of RAM to be tested in an atomic way.

# STL user constraints

Teend uer nee  considerinteerence between eapliation an heLTeconquences this are possible false STL error reporting, and/or application software execution issues.

Acoingly ntenlican trtn u ply constraint listed in this section.

# 4.3.1 Privileged-level

The PU TM7 and he RAM TM must beexecuted wit privleged leve, inrder  be able tmodiy certn registers (for example the PRIMASK register) else these TMs return STL_ERROR.

# 4.3.2 RCC resources

During STL eecution, he RCC is conigured to always provide a clock to the RChardware module durig STL initialization and optionally during STL Flash test module execution. This means that:

when the STL returns, it restores the user RCC clock setting (enabled or disabled) for the CRC the user application should be careful when configuring the RCC during TL execution by saving/restoring the STL settings.

# 4.3.3

# CRC resources

The STM32 CRC hardware module is used during STL execution in two different cases:

During execution of STL initialization (function STL_SCH_Init): The use of the CRC hardware module in this phase cannot be modified by the application software, so the STL_SW_CRC flag has no impact during execution of the STL_SCH_Init function.   
During execution of the flash memory test module, the application can choose between hardware and software calculation of the CRC checksums by means of the STL_SW_CRC flag. By default, hardware CRC is used (the STL_SW_CRC flag is disabled).

The use of hardware CRC means that:

• Before caling the STL, the user application must save the complete hardware CRC module configuration. The user configuration has to be restored after the STL execution. During the STL execution, the hardware CRC module is configured and used for STL needs (the user application must save/restore the STL settings when using the module outside of STL execution).

# 4.3.4 Bit Q of APSR

CUCBeecuion ts bt fhe S sicy verflow nd saturation ag)Teusapplicaton mustake this into account when using this bit.

# 4.3.5

# Interrupt manageme

# Escalation mechanism - Arm® Cortex® behavior reminder

Whe he L diables 32 interrupts, an Cortex® excptions with configurable priority, remember ®C®u aruu handler.

# Interrupt and CPU TM7

Bulterpts ore® es wurable priy rily ask iaaulrblockeep ativates the TLABLET comlatin switc (ee Section 5.5. Steps to build aaplication rom scrach). If  STLENABLET fg i activate he corec TLCPU TM7 behaviors ot uante.The end  s ibl agntn enhLplcatin tarht culd aheSTL generate false test error reporting or not to detect hardware failures.

# Interrupt and RAM March C- tests

By dfault,he 32 interrupts an Cortex® ecptons with configurable priority aremasked during h RAM March C- tests, except if the user application activates the STL_ENABLE_IT compilation switch (see Section 5.5.2: Steps to build an application from scratch).

If the STL_ENABLE_IT flag is activated:

The correct STL RAM test behavior is not guaranteed, as the application may overwrite the STL-tested RAM content during its interrupt treatment. The end user is responsible for managing interferences between the STL and its application software that could lead the STL to generate false RAM test error reporting.

The behavior of the user application software can be compromised. Wrong data may be read or used from RAM locations that are being modified by the STL March C- test.

# Interrupt and general purpose registers

Dupltu vl-ur a C® e  ue y u   ev false error reporting.

# How STL masks the interrupts

To mask the inteupts, the STL sets the RAK register bit .Settg this bit o1 boosts the ur et prrisste  particlarvalu ll eptns wi a weeul piy easke.

# 4.3.6 DMA

The application must manage the DMA to avoid unwanted accesses to the RAM bank during the STL March Ctest. In this case:

DMA writes can disturb the STL test causing false error reporting DMA reads can return wrong data due to STL overwrites to DMA dedicated RAM sections.

# 4.3.7

# Supported memories

The STL memory tests provided (Flash TM and RAM TM) must only be executed on STM32 internal embedded memories. The STL library flow must be executed from the internal embedded memory only.

# 4.3.8

# RAM backup buffer

The backup process is enabled by default during RAM tests to preserve the RAM content. The user must then reve a specific are or the RAM backup bufferat compilation time which must be allocateoutsid RAM uuran.elyAM backu buferhet.eAbackp bu st ear cAn is tested).

The backup process can be optionally disabled either permanently by activating the compilation switch STL_DISABLE_RAM_BCKUP_BUF (see Section 5.5.2: Steps to build an aplication from scratch) or temporarily guarantha plcatn adot onme at estroye eMarTiot be used to speed up testing of those RAM areas where users do not need to preserve the memory content.

# Note:

For a temporary suppression of the RAM backup buffer, the user must follow a set sequence:

Change the TLpRamTmBckUpBu variable value to overwrite it by NULL, while keeping a backup of the original value (default value stored by the STL).

The RAM test must then be restarted To do so the user can use one of the APIs which force the RAM test into either RAM_IDLE or RAM_INIT state (see state diagrams in Section 7.3: State machines) .

Tve ack n er mus phe m ove whi tgheu value of STL_pRamTmBckUpBuf to its original value and reinitialize the RAM test.

# 4.3.9

# Memory mapping

Du theRAM tt odleand Marc metho desig, he sermustensur hat e "ead on"dat e Ssocat e ashmmoyTismust edone proeaptaion eascat k The examples below are for EWARM and STM32CubeIDE.

# EWARM .icf file adaptation example

place in ROM_region { readonly };

# STM32CubelDE.Id file adaptation example

<table><tr><td>.rodata :</td><td></td></tr><tr><td></td><td></td></tr><tr><td></td><td></td></tr><tr><td></td><td></td></tr><tr><td>} &gt;ROM</td><td></td></tr></table>

# Note:

Usually the default configuration locates "read only" data in flash memory.

# 4.3.10 Cortex M7 cache resources

The TM RAM tests the RAM content, but not the DCache content. To ensure this, in cases where the DCache is enabled by the user, the TM RAM:

Disables and cleans the DCache before performing the RAM test   
Invalidates and enables the DCache when the RAM test is complete (when the TM RAM returns)   
Performs the upper two atomic operations under disabled interrupt

The user must not enable the DCache during TM RAM execution, as the DCache must remain disabled during this test execution.

# 4.3.11 Processor mode

TheTLU TM7 must e eecu in redmod order ethe activ ack ponter he ps ac pointer. If the STL is not executed in thread mode, the CPU TM7 returns STL_ERROR.

# 4.4

# End-user integration tests

This section describes themandatoryests to be executed byhe end userduring theverfication phaseThe tests guarantee that the STL is correctly integrated in the application software.

# 4.4.1

# Test 1: correct STL execution

The end user must use the expected function-return value and the expected test-module result value (see Section 7.2: User APls) to check that each planned diagnostic function has been correctly executed. This concerns both the test modules execution and all their configuration actions.

# 4.4.2

# Test 2: correct STL error-message processing

The enduser must check that any eoriormatin produced byhe Lfnction-eturn and test-moduleresult valvcp al n eSUsu t aateindiviualoftariostics(CPU tests,RAM testfashmemor est), r eachftheda functions used.

T pranot sierastivlationcl ilurelevi a testing interface of the implemented APls.

# Note:

In some circumstances, experts performing the safety assessment of final systems embedding the STL might require exhaustive simulation to demonstrate STL capability to capture corruption of STM32 registers or memor inecteitentinalurideugging heTLcdT perorhe est s racticallysle for any end user due to STLoject delivery format. This speciic testing was done for all the provided TMs during theTLcertifiation proes and its passig is recordd atinternal est reports and guaranteed y the valid certificate issued for this ST firmware.

# 5 Package description

This section details the X-CUBE-CLASSB-H7 expansion package content and its correct use.

# 1 General description

X-CUBE-CLASSB-H7 is a software expansion package for STM32H7 series microcontrolle It provides a complete solution that helps end customers to build a safety application:

An application-independent software test library is available:

partly as object code: STL_Lib_product_x1.a and STL_Lib_product_x2.a, the library itself partly as source file: stl_user_param_template.c and stl_util.c with three header files:stl_stm32_hw_config.h,stl_user_api.h,andstl_util.h

A user application example, available as source code

X-CUBE-CLASSB-H7 has been ported on the products listed in Section 3.2: Supported products.

Taepansn packac mplpliationhat develoer ep with the code. It is provided as a zip archive containing both source code and library.

The following integrated development environments are supported:

IAR Embedded Workbench® for Arm® (EWARM) Keil® microcontroller development kit (MDK-ARM) STM32CubeIDE.

# 5.2

# Architecture

The components of the X-CUBE-CLASSB-H7 expansion package are illustrated in Figure 6.

![](images/2ee15d1357335036c0741fdaeb74c2829fb254b97d5da4c24b970d19ed907275.jpg)  
Figure 6. Software architecture overview

# 5.2.1

# STM32Cube HAL

THALdiveayerprovie pegcmutnstanceAPs pliation prorag int to interact with the upper layers (application, libraries, and stacks).

I auilt uponu heidewar ayr, plement thectinalit without dpendenci specific hardware configuration of a given microcontroller.

This structuremproves the library codere-sability and guarantees a easy portabilitytotherdevices.

# 5.2.2

# Board support package (BSP)

T ota paca eeport e prheal 32 boarar fohe isincluded in the board support package (P). Thisis a limited set of APs that provides a programming interface for some specific board components, such as the LED and the user button.

# STL

Aant parTilablwav iblcox age sticst Iisndependet fm he HAL BSP,anMSI eve eTLintgrati exaple some HAL drivers.

# 5.2.4 User application example

Te provienc proj hohowtgrat posleencmouleal al whetnt ula hi alc pe C demonstrates how the library can be extended by specific tests o modules entirely defined by the enduse.

To l y r of partial tests performed periodically during application runtime.

# 5.2.5

# STL integrity

The integrity of the STL content is ensured by hash SHA-256.

# 5.3

# Folder structure

A top-level view of the structure is shown in Figure 7.

![](images/c0a566bb905d39650cad8cae0401a241036b10f64e8bdd922a477dba25527e49.jpg)  
Figure 7. Project file structure

# 5.4

# APIs

# 5.4.1

# Compliance

# Interface compliance

Te library part  the TL ot delivrein source code, has been copid wit IAR EmbeedWorkbench® fo Arm v9.30.. The compilation is done with --aeabi and --guardca11s compilation options to fulillAEABl compliance as described in "AEABI compliance" of the EWARM help section.   
This library can be compiled by any standard version of the EWARM compiler.

# Safety guidelines

Tulfil the afety guidelies copliance as escrie in the IAR Embe Worbench® sfetyguie vie 2.1-1, 2.2-5, 2.4-1a and 5.4-3) and the Keil® safety manual (§4.9.2), the compliance is done with -tr remarks, --require_prototypes and --no_unaligned_access compilation options.

# Library compliance

The library part of the STL (not delivered in source code) is compliant with C standard library ISO C99.   
It has been compiled with the IAR™ option. Language C dialect = Standard C.

# Arm® compiler C toolchain vendor/version independency

The STL user AP refers only to the "uint32t" and "enum" C types:

uint 32_t" C type is a fixed type size of 32 bits according to C standard C99 eu C type size, according to C standard C9, is defined by the implementation. It must be able to represent the values of ll the enumeration members. In the STL interface, the enum type values are unsigned integers, smaller than or equal to (232  ). The user must ensure that the enum type value can hold a 32-bit value.

# 5.4.2 Dependency

The STL library calls the memset standard C library function.

Futhemore, he AR™EWARM toolchain compile is used to compile he TL library. This compiler ayne some circumstances, callthe following standard C library functions: memcpy, memset, and memc1r. This behavior is intrinsic to the IAR™ EWARM toolchain compiler. It is not possible to disable or avoid it.

uk The user can use either the functions provided by the toolchain or the user ones.

# 5.4.3 Details

Detailed technical information about the available APls can be found in Section 7.: User APls, where the functions and parameters are described.

# 5.5

# Application: compilation process

# Steps to build delivered STL example

Install the ST CRC tool (see Section 6.2.2:CRC tool set-up) or other CRC tool that generate an adequate structure necessary for proper execution of the flash test.

Project choice: Select a project example and open it.

Project build: Launch the build which compiles the binary and post build command invokes CRC tool to calculate and allocate the CRC results. In case of error, check the CRC tool path. For details see Section 5.5.2: Steps to build an application from scratch.

Load the compiled binary.

5. Execute.

Boot the board and check the result:

LED toggle regularly: test result is as expected.   
LED toggle irregularly: there is an error.

isuE y error, the LED flashes once every 4 sec.

The FiHand procedure shen called with  paramer keeping the dentiiatin codeftheail module

# Note:

Theein egivehthasdeensiv om il DEF_PROG_OFFSET is added to the module code. User can adapt or extend the et of definitions applied by the STL example there.

# 5.5.2

# Steps to build an application from scratch

To build an application from scratch, follow the steps listed below:

Cr w tn ro w  itableoy rcnd wil heo ackas STM32CubeMX tool to make it automatically.

any automate includeoptions f he TLi the projec is ot supported by he ST32CubeMX too co and paste the content of the ...Middleware\ST\STM32_Safety_STL directory from the delivered STL t puSo modify the project setting manually while following the next steps:

Ad all the STL source fles located at the SRC directory into the projct.   
Assign the INC directory as an additional directory to be included in the project.   
Forc the lnkernclude headequate lirary object e ocate at he L rectory as andital library (refer to Section 3.2: Supported products).

# Note:

This second step is necessary only when no automatic including option is supported by the CubeMX tool e is fully peformed by the tol thenthere s o eed orany manualinterventin  describeove user can leave them out and continue by Step 3

3If needed, add the next optional preprocessor compilation switches at project settings:

Option to enable STL_DISABLE_RAM_BCKUP_BUF, if the RAM backup buffer is not used (in this case the RAM data of the tested subsets are destroyed). If not activated, the RAM backup buffer is used by default. In such cases, the "backupbuffersection" section must be defined in the linker scatter fil. Option to enable STL_SW_CRC: this is where the user application selects the software CRC . If not activated, the hardware CRC calculation is used by default.   
Option to enable STL_ENABLE_IT: this is where the user application enables the STM32 interrupts during the CPU TM7, and RAM test. If not activated, the interrupts are masked during these tests. See Section 4.3.5: Interrupt management and Section 4.1.4: RAM tests.

4Check the configuration of the flash memory density. It ismandatory to set the correct range of the memory for the project at sluser_paramtemplateile. Update the STL_ROM_END_ADDR there especially to ensure coherency with the associated linker scatter fil and the CRC tool script (see step 6.).

evelo heu TL fo control. I i done y plentig he prope quenc AP call epea a periodical cycles, as required by the defined safety task. It i il e apy a correct check of the STL return iforation Refer to Section : TL: User APIs and state machines.

Apply the CRC tool to build the CRC area content necessary for the CRC calculation. Refer to Section 6.2.2: CRC tool set-up. Execute a proper command line of the STM32CubeProgrammer. This can be done automatically within the compilation process by invoking the IDE post build feature action as seen in Figure 8 and Figure 9.

Compile, load, and execute the binary.

Arl a ebhave o hardware failure.

![](images/88d719554a6a981b5cf42572ead99e1bec4c5d21270ad08fc57e4c32fd19621a.jpg)  
Figure 8. IAR™ post-build actions screenshot

![](images/1f1f5ad296448b5fca9f17cf6f7fce277074322469d917da00804ed8fc7f27b9.jpg)  
Figure 9. CRC tool command line

# Hardware and software environment setup

# 6.1

# Hardware setup

The STM32 Nucleo boards provide an affordable and flexible way for users to try out new ideas and build prototypes with any STM32 microcontroller lines. The ARDUINO® connectivity support and ST morpho headers makasy epand thectinalit te Nuclopen develoment plato wi a wiecho alizpansin boarse Nuc bard dso equiy parat probestegrat e ST-LINK/V2-1 debugger/programmer. The STM32 Nucleo boards comes with the STM32 comprehensive software HAL library together with various packaged-software examples.

Details about the STM32 Nucleo boards are available from the http://www.st.com/stm32nucleo web page.

![](images/9669070d22c7d24b15e86263ea42bb616fba7d4710e78957565dbba1b46bcd1c.jpg)  
Figure 10. STM32 Nucleo board example

The following components are needed:

NUCLEO-H743ZI (MB1137 Rev B) development board USB type A to Micro-B USB cable to connect the development board to the PC

# 6.2

# Software setup

T n   eeloe to customize applications.

# 6.2.1

# Development tool-chains and compilers

Select one of the IDEs supported by the STM32Cube software expansion package.   
Read the system requirements and setup information provided by the selected IDE provider.   
C elo cp if it exists.

# 6.2.2 CRC tool set-up

ST provides a CRC tol available as  single feature inside he T32CubeProgrammer, used for fash emory testing. Other CRC tools can be used, provided they fulfil the requirements detailed in Expected CRC precalculation.

Tool installation procedure:

Select STM32CubeProgrammer on the dedicated web page available on www.st.com

Install the package.

Ts wyeo pev  uath.   
If not, the path must be added directly in the project for compilation, in the post-build option.

# 7

# STL: User APIs and state machines

# 7.1

# User structures

The structures are defined in st1_user_api.h. It is forbidden to change the content of this file. Structures detailed hereafter are copies of the stl_user_api. h content:

typedef enum STL_OK = STL_OK_DEF, /\* Scheduler function successfully executed \*/ STL_KO = STL_KO_DEF /\* Scheduler function unsuccessfully executed (defensive programming error, checksum error). In this case the STL_TmStatus_t values are not relevant \*/ STL_Status_t; /\* Type for the status return value of the STL function execution \*/   
typedef enum STL_PASSED = STL_PASSED_DEF, /\* Test passed. For Flash/RAM, test is passed and end of configuration is also reached \*/ STL_PARTIAL_PASSED = STL_PARTIAL_PASSED_DEF, /\* Used only for RAM and Flash testing. Test passed, But end of Flash/RAM configuration not yet reached \*/ STL_FAILED = STL_FAILED_DEF, /\* Hardware error detection by Test Module \*/ STL_NOT_TESTED = STL_NOT_TESTED_DEF, /\* Initial value after a SW init, SW config, SW reset, SW de-init or value when Test Module not executed \*/ STL_ERROR = STL_ERROR_DEF /\* Test Module unsuccessfully executed (defensive programing check failed) \*/ STL_TmStatus_t; /\* Type for the result of a Test Module \*/   
typedef enum STL_CPU_TM1L_IDX = OU, /\* CPU Arm Core Test Module 1L index \*/ STL_CPU_TM_IDX, /\* CPU Arm Core Test Module 7 index \*/ STL_CPU_TMCB_IDX, /\* CPU Arm Core Test Module Class B index \*/ STL_cPU_TM_MAX /\* Number of CPU Arm Core Test Modules \*/ STL_CpuTmxIndex_t; /\* Type for index of cPU Arm Core Test Modules \*/   
typedef struct STL_MemSubset_struct uint32_t StartAddr; /\* start address of Flash or RAM memory subset \*/ uint32_t EndAddr; /\* end address of Flash or RAM memory subset \*/ struct STL_MemSubset_struct \*pNext; /\* pointer to the next Flash or RAM memory subset - to be set to NULL for the last subset \*/ STL_MemSubset_t; /\* Type used to define Flash or RAM subsets to test \*/   
typedef struct STL_MemSubset_t \*pSubset; /\* Pointer to the Flash or RAM subsets to test \*/ uint32_t NumSectionsAtomic; /\* Number of Flash or RAM sections to be tested during an atomic test \*/ STL_MemConfig_t; /\* Type used to fully define Flash or RAM test configuration \*/   
typedef struct   
{ STL_TmStatus_t aCpuTmStatus[STL_CPU_TM_MAX]; /\* Array of forced status value for CPU Test Modules \*/ STL_TmStatus_t FlashTmStatus; /\* Forced status value for Flash Test Module \*/ STL_TmStatus_t RamTmStatus; /\* Forced status value for RAM Test Module \*/ STL_ArtifFailingConfig_t; /\* Type used to force Test Modules status to a specific value for each STL Test Module \*/

# 7.2

# User APIs

TP.I.

# Caution:

For pointers defined by the user application and used as STL API parameters, the user application must set va pma pvabi hee potrTeLd ot cye content, and accesses directly to the memory addresses defined by the application.

T keep the configuration of the memory tests must be maintained. They are stil used by the STL_CH_run_xx called.

For more details about proper API sequence cals see Section 7.3: State machines and Section 8: Test examples.

# 7.2.1

# Common API

The following sections present details on common APls.

# 7.2.1.1

# STL_SCH_Init

ii.   
Declaration: STL_Status_t STL_SCH_Init(void).

Table 6. STL_SCH_Init input information   

<table><tr><td>Allowed states</td><td>Parameters</td></tr><tr><td>CPU TMx: all</td><td></td></tr><tr><td>Flash TM: all</td><td></td></tr><tr><td>RAM TM: all</td><td></td></tr></table>

Table 7. STL_SCH_Init output information   

<table><tr><td rowspan=1 colspan=2>STL_Status_t return value</td><td rowspan=2 colspan=1>Returned state</td></tr><tr><td rowspan=1 colspan=1>Value</td><td rowspan=1 colspan=1>Comments</td></tr><tr><td rowspan=1 colspan=1>STL_OK</td><td rowspan=1 colspan=1>Function successfully executed</td><td rowspan=1 colspan=1>CPU TMx: CPU_TMx_CONFIGUREDFlash TM: FLASH_IDLERAM TM: RAM_IDLE</td></tr><tr><td rowspan=1 colspan=1>STL_KO</td><td rowspan=1 colspan=1>Source of defensive programming error:STL internal data corrupted</td><td rowspan=1 colspan=1>No state change</td></tr></table>

Additional information: there is no specific CPU initialization function for CPU test modules.

Note:

This function uses hardware CRC as explained in Section 4.3.3: CRC resources.

# 7.2.2

# CPU Arm® core testing APIs

# 7.2.2.1

# STL_SCH_RunCpuTMx

Description: runs one of the CPU test modules.

Declaration: STL_Status_t STL_SCH_RunCpuTMx(STL_TmStatus_t \*pSingleTmStatus) where TMx can be one of TM1L, TM7 or TMCB.

Table 8. STL_SCH_RunCpuTMx input information   

<table><tr><td rowspan=2 colspan=1>Allowed states</td><td rowspan=1 colspan=2>Parameters</td></tr><tr><td rowspan=1 colspan=1>Value</td><td rowspan=1 colspan=1>Comments</td></tr><tr><td rowspan=1 colspan=1>CPU_TMx_CONFIGURED</td><td rowspan=1 colspan=1>*pSingleTmStatus</td><td rowspan=1 colspan=1>See Caution</td></tr></table>

Table 9. STL_SCH_RunCpuTMx output information   

<table><tr><td rowspan=1 colspan=2>STL_Status_t return value</td><td rowspan=1 colspan=2>*pSingleTmStatus output</td><td rowspan=2 colspan=1>Returned state</td></tr><tr><td rowspan=1 colspan=1>Value</td><td rowspan=1 colspan=1>Comments</td><td rowspan=1 colspan=1>Value</td><td rowspan=1 colspan=1>Comments</td></tr><tr><td rowspan=1 colspan=1></td><td rowspan=1 colspan=1></td><td rowspan=1 colspan=1>STL_PASSED</td><td rowspan=1 colspan=1></td><td rowspan=3 colspan=1>CPU_TMx_CONFIGURED</td></tr><tr><td rowspan=2 colspan=1>STL_OK</td><td rowspan=2 colspan=1>Function successfully executed</td><td rowspan=1 colspan=1>STL_FAILED</td><td rowspan=1 colspan=1></td></tr><tr><td rowspan=1 colspan=1>STL_ERROR</td><td rowspan=1 colspan=1>Source of defensiveprogramming error:STL internal datacorruptedSoftware is notexecuted withprivileged level for CPUTM7•    Software is notexecuted in threadmode for CPU TM7</td></tr><tr><td rowspan=1 colspan=1>STL_KO</td><td rowspan=1 colspan=1>Possible source of defensiveprogramming error:pSingleTmStatus = NULLSTL internal data corrupted</td><td rowspan=1 colspan=1>Not relevant</td><td rowspan=1 colspan=1>Value must not be used</td><td rowspan=1 colspan=1>No state change</td></tr></table>

# 7.2.3

# Flash memory testing APIs

# 7.2.3.1

# STL_SCH_InitFlash

Description: initializes flash memory test.

Declaration: STL_Status_t STL_SCH_InitFlash(STL_TmStatus_t \*pSingleTmStatus)

Table 10. STL_SCH_InitFlash input information   

<table><tr><td rowspan=2 colspan=1>Allowed states</td><td rowspan=1 colspan=2>Parameters</td></tr><tr><td rowspan=1 colspan=1>Value</td><td rowspan=1 colspan=1>Comments</td></tr><tr><td rowspan=1 colspan=1>FLASH_IDLEFLASH_INITFLASH_CONFIGURED</td><td rowspan=1 colspan=1>*pSingleTmStatus</td><td rowspan=1 colspan=1>Caution</td></tr></table>

Table 11. STL_SCH_InitFlash output information   

<table><tr><td rowspan=1 colspan=2>STL_Status_t return value</td><td rowspan=1 colspan=2>*pSingleTmStatus output</td><td rowspan=2 colspan=1>Returned state</td></tr><tr><td rowspan=1 colspan=1>Value</td><td rowspan=1 colspan=1>Comments</td><td rowspan=1 colspan=1>Value</td><td rowspan=1 colspan=1>Comments</td></tr><tr><td rowspan=1 colspan=1>STL_OK</td><td rowspan=1 colspan=1>Function successfully executed</td><td rowspan=1 colspan=1>STL_NOT_TESTED</td><td rowspan=1 colspan=1></td><td rowspan=1 colspan=1>FLASH_INIT</td></tr><tr><td rowspan=1 colspan=1>STL_KO</td><td rowspan=1 colspan=1>Possible source of defensiveprogramming error:pSingleTmStatus=NULLSTL internal data corrupted</td><td rowspan=1 colspan=1>Not relevant</td><td rowspan=1 colspan=1>Value must not beused</td><td rowspan=1 colspan=1>No state change</td></tr></table>

# 7.2.3.2

# STL_SCH_ConfigureFlash

Description: configures the flash memory test.

Declaration: STL_Status_t STL_SCH_ConfigureFlash(STL_TmStatus_t \*pSingleTmStatus, STL_MemConfig_t \*pFlashConfig)

Table 12. STL_SCH_ConfigureFlash input information   

<table><tr><td rowspan="2">Allowed states</td><td colspan="5">Parameter</td></tr><tr><td>Value</td><td colspan="3">Comments</td><td></td></tr><tr><td rowspan="7">FLASH_INIT</td><td>*pSingleTmStatus</td><td colspan="3">See Caution</td></tr><tr><td rowspan="2"></td><td>Pointer to the flash memory configuration. See Caution. Field</td><td colspan="2">Comments</td></tr><tr><td></td><td colspan="2">Pointer to flash memory subset. See • Caution</td></tr><tr><td rowspan="7">*pFlashConfig</td><td rowspan="7">• *pSubset</td><td colspan="2">A section cannot overlap with the CRC area</td></tr><tr><td>Field</td><td>Comments Start subset address</td></tr><tr><td>StartAddr</td><td>in bytes CRR_START address •</td><td>Cannot be lower than ROM_START and higher than End subset address in bytes</td></tr><tr><td>EndAddr</td><td></td><td>Cannot be lower than ROM_START and higher than CRSTART address Needs to be higher than StartAddr</td></tr><tr><td>*pNext •</td><td></td><td>Pointer to next flash memory subset. See Caution Must be set to NULL for the last subset</td></tr><tr><td>NumSectionsAtomic</td><td>test)</td><td>Number of flash memory sections to be tested during an atomic test Set to 1, as minimum (one section per If the value is higher than the number of sections in all subsets, all flash memory subsets are tested in one pass</td></tr></table>

Table 13. STL_SCH_ConfigureFlash output information   

<table><tr><td rowspan=1 colspan=2>STL_Status_t return value</td><td rowspan=1 colspan=2>*pSingleTmStatus output</td><td rowspan=2 colspan=1>Returned state</td></tr><tr><td rowspan=1 colspan=1>Value</td><td rowspan=1 colspan=1>Comments</td><td rowspan=1 colspan=1>Value</td><td rowspan=1 colspan=1>Comments</td></tr><tr><td rowspan=2 colspan=1></td><td rowspan=2 colspan=1>STL_OK Function successfully executed</td><td rowspan=1 colspan=1>STL_NOT_TESTED</td><td rowspan=1 colspan=1></td><td rowspan=1 colspan=1>FLASH_CONFIGURED</td></tr><tr><td rowspan=1 colspan=1>STL_ERROR</td><td rowspan=1 colspan=1>Possible source ofdefensive programmingerror:State not allowedWrong configurationdetectedSTL internal datacorrupted</td><td rowspan=1 colspan=1>No state change</td></tr><tr><td rowspan=1 colspan=1>STL_KO</td><td rowspan=1 colspan=1>Possible source of defensiveprogramming error:•    pSingleTmStatus = NULL•    pFlashConfig=NULL•    STL internal data corrupted</td><td rowspan=1 colspan=1>Not relevant</td><td rowspan=1 colspan=1>Value must not be used</td><td rowspan=1 colspan=1>No state change</td></tr></table>

Ainal inormaton in the case  retunvalue et  LOorpSigTmau et o LERROR, the flash memory configuration is not applied.

# 7.2.3.3

# STL_SCH_RunFlashTM

Description: runs flash memory test.

Declaration: STL_Status_t STL_SCH_RunFlashTM(STL_TmStatus_t \*pSingleTmStatus)

Table 14. STL_SCH_RunFlashTM input information   

<table><tr><td rowspan=2 colspan=1>Allowed states</td><td rowspan=1 colspan=2>Parameters</td></tr><tr><td rowspan=1 colspan=1>Value</td><td rowspan=1 colspan=1>Comments</td></tr><tr><td rowspan=1 colspan=1>FLASH_CONFIGURED</td><td rowspan=1 colspan=1>*pSingleTmStatus</td><td rowspan=1 colspan=1>See Caution</td></tr></table>

Table 15. STL_SCH_RunFlashTM output information   

<table><tr><td rowspan=1 colspan=2>STL_Status_t return value</td><td rowspan=1 colspan=2>*pSingleTmStatus output</td><td rowspan=2 colspan=1>Returned state</td></tr><tr><td rowspan=1 colspan=1>Value</td><td rowspan=1 colspan=1>Comments</td><td rowspan=1 colspan=1>Value</td><td rowspan=1 colspan=1>Comments</td></tr><tr><td rowspan=1 colspan=1></td><td rowspan=1 colspan=1></td><td rowspan=1 colspan=1>STL_PASSED</td><td rowspan=1 colspan=1></td><td rowspan=1 colspan=1>FLASH_CONFIGURED</td></tr><tr><td rowspan=1 colspan=1></td><td rowspan=3 colspan=1></td><td rowspan=1 colspan=1>STL_PARTIAL_PASSED</td><td rowspan=1 colspan=1></td><td rowspan=1 colspan=1>FLASH_CONFIGURED</td></tr><tr><td rowspan=2 colspan=1></td><td rowspan=1 colspan=1>STL_FAILED</td><td rowspan=1 colspan=1></td><td rowspan=1 colspan=1>FLASH_CONFIGURED</td></tr><tr><td rowspan=1 colspan=1>STL_NOT_TESTED</td><td rowspan=1 colspan=1>All subsets are alreadytested</td><td rowspan=1 colspan=1>FLASH_CONFIGURED</td></tr><tr><td rowspan=1 colspan=1></td><td rowspan=1 colspan=1>STL_OK Function successfully executed</td><td rowspan=1 colspan=1>STL_ERROR</td><td rowspan=1 colspan=1>Possible source ofdefensive programmingerror:•    State not allowed•    Configurationcorrupted•    STL internal datacorrupted</td><td rowspan=1 colspan=1>No state change</td></tr><tr><td rowspan=1 colspan=1>STL_KO</td><td rowspan=1 colspan=1>Possible source of defensiveprogramming error:pSingleTmStatus =NULL•    STL internal data corrupted</td><td rowspan=1 colspan=1>Not relevant</td><td rowspan=1 colspan=1>Value must not be used</td><td rowspan=1 colspan=1>No state change</td></tr></table>

# 7.2.3.4

# STL_SCH_ResetFlash

Description: resets flash memory test. Declaration: STL_Status_t STL_SCH_ResetFlash(STL_TmStatus_t \*pSingleTmStatus)

Table 16. STL_SCH_ResetFlash input information   

<table><tr><td rowspan=2 colspan=1>Allowed states</td><td rowspan=1 colspan=2>Parameters</td></tr><tr><td rowspan=1 colspan=1>Value</td><td rowspan=1 colspan=1>Comments</td></tr><tr><td rowspan=1 colspan=1>FLASH_CONFIGURED</td><td rowspan=1 colspan=1>*pSingleTmStatus</td><td rowspan=1 colspan=1>See Caution</td></tr></table>

Table 17. STL_SCH_ResetFlash output information   

<table><tr><td rowspan=1 colspan=2>STL_Status_t return value</td><td rowspan=1 colspan=2>*pSingleTmStatus output</td><td rowspan=2 colspan=1>Returned state</td></tr><tr><td rowspan=1 colspan=1>Value</td><td rowspan=1 colspan=1>Comments</td><td rowspan=1 colspan=1>Value</td><td rowspan=1 colspan=1>Comments</td></tr><tr><td rowspan=2 colspan=1></td><td rowspan=2 colspan=1>STL_OK Function successfully executed</td><td rowspan=1 colspan=1>STL_NOT_TESTED</td><td rowspan=1 colspan=1>Configuration successfullyaplied</td><td rowspan=1 colspan=1>FLASH_CONFIGURED</td></tr><tr><td rowspan=1 colspan=1>STL_ERROR</td><td rowspan=1 colspan=1>Possible source ofdefensive programmingerror:State not allowedConfigurationcrruptedSTL internal datacorrupted</td><td rowspan=1 colspan=1>No state change</td></tr><tr><td rowspan=1 colspan=1>STL_KO</td><td rowspan=1 colspan=1>Possible source of defensiveprogramming error:pSingleTmStatus =NULLSTL internal data corrupted</td><td rowspan=1 colspan=1>Not relevant</td><td rowspan=1 colspan=1>Value must not be used</td><td rowspan=1 colspan=1>No state change</td></tr></table>

# Additional information

Once al subsets are tested, the user needs to reset the test module to perform the flash memory test again.   
In the case of a return value set to STL_KO or \*pSing1eTmStatus set to STL_ERROR, the flash memory reset is not applied.

# 7.2.3.5

# STL_SCH_DelnitFlash

Description: deinitializes flash memory test.

Declaration: STL_Status_t STL_SCH_DeInitFlash(STL_TmStatus_t \*pSingleTmStatus)

Table 18. STL_SCH_DelnitFlash input information   

<table><tr><td rowspan=2 colspan=1>Allowed states</td><td rowspan=1 colspan=2>Parameters</td></tr><tr><td rowspan=1 colspan=1>Value</td><td rowspan=1 colspan=1>Comments</td></tr><tr><td rowspan=1 colspan=1>FLASH_IDLEFLASH_INITFLASH_CONFIGURED</td><td rowspan=1 colspan=1>*pSingleTmStatus</td><td rowspan=1 colspan=1>See Caution</td></tr></table>

Table 19. STL_SCH_DelnitFlash output information   

<table><tr><td rowspan=1 colspan=2>STL_Status_t return value</td><td rowspan=1 colspan=2>*pSingleTmStatus output</td><td rowspan=2 colspan=1>Returned state</td></tr><tr><td rowspan=1 colspan=1>Value</td><td rowspan=1 colspan=1>Comments</td><td rowspan=1 colspan=1>Value</td><td rowspan=1 colspan=1>Comments</td></tr><tr><td rowspan=1 colspan=1>STL_OK</td><td rowspan=1 colspan=1>Function successfully executed</td><td rowspan=1 colspan=1>STL_NOT_TESTED</td><td rowspan=1 colspan=1></td><td rowspan=1 colspan=1>FLASH_IDLE</td></tr><tr><td rowspan=1 colspan=1>STL_KO</td><td rowspan=1 colspan=1>Possible source of defensiveprogramming error:pSingleTmStatus =NULLSTL internal data corrupted</td><td rowspan=1 colspan=1>Not relevant</td><td rowspan=1 colspan=1>Value must not beused</td><td rowspan=1 colspan=1>No state change</td></tr></table>

# 7.2.4

# RAM testing APIs

# 7.2.4.1

# STL_SCH_InitRam

Description: initializes the RAM test.

Declaration: STL_Status_t STL_SCH_InitRam(STL_TmStatus_t \*pSingleTmStatus).

Table 20. STL_SCH_InitRam input information   

<table><tr><td rowspan=2 colspan=1>Allowed states</td><td rowspan=1 colspan=2>Parameters</td></tr><tr><td rowspan=1 colspan=1>Value</td><td rowspan=1 colspan=1>Comments</td></tr><tr><td rowspan=1 colspan=1>RAM_IDLERAM_INITRAM_CONFIGURED</td><td rowspan=1 colspan=1>*pSingleTmStatus</td><td rowspan=1 colspan=1>See Caution</td></tr></table>

Table 21. STL_SCH_InitRam output information  

<table><tr><td rowspan=1 colspan=2>STL_Status_t return value</td><td rowspan=1 colspan=2>*pSingleTmStatus output</td><td rowspan=2 colspan=1>Returned state</td></tr><tr><td rowspan=1 colspan=1>Value</td><td rowspan=1 colspan=1>Comments</td><td rowspan=1 colspan=1>Value</td><td rowspan=1 colspan=1>Comments</td></tr><tr><td rowspan=1 colspan=1>STL_OK</td><td rowspan=1 colspan=1>Function successfully executed</td><td rowspan=1 colspan=1>STL_NOT_TESTED</td><td rowspan=1 colspan=1></td><td rowspan=1 colspan=1>RAM_INIT</td></tr><tr><td rowspan=1 colspan=1>STL_KO</td><td rowspan=1 colspan=1>Possible source of defensiveprogramming error:pSingleTmStatus = NULLSTL internal data corrupted</td><td rowspan=1 colspan=1>Not relevant</td><td rowspan=1 colspan=1>Value must not beused</td><td rowspan=1 colspan=1>No state change</td></tr></table>

# 7.2.4.2

# STL_Status_t STL_SCH_ConfigureRam

Description: Description: configures the RAM test.

Declaration: STL_Status_t STL_SCH_ConfigureRam(STL_TmStatus_t \*pSingleTmStatus, STL_MemConfig_t \*pRamConfig)

Table 22. STL_SCH_ConfigureRam input information   

<table><tr><td rowspan=3 colspan=1>Allowed states</td><td></td><td></td><td></td></tr><tr><td rowspan=1 colspan=3>Parameter</td></tr><tr><td rowspan=1 colspan=1>Value</td><td rowspan=1 colspan=2>Comments</td></tr><tr><td rowspan=3 colspan=1></td><td rowspan=1 colspan=1>*pSingleTmStatus</td><td rowspan=1 colspan=2>See Caution</td></tr><tr><td rowspan=2 colspan=1></td><td rowspan=1 colspan=2>This pointer contains the RAM configuration. See Caution</td></tr><tr><td rowspan=1 colspan=1>Field</td><td rowspan=1 colspan=1>Comments</td></tr><tr><td rowspan=6 colspan=1>RAM_INIT</td><td rowspan=6 colspan=1>*pRamConfig</td><td rowspan=5 colspan=1>*pSubset</td><td rowspan=1 colspan=1>Pointer to RAM subset. See CautionA subset cannot overlap with the RAMbackup buffer if defined</td></tr><tr><td rowspan=1 colspan=1>Comments</td></tr><tr><td rowspan=1 colspan=1>Start subset address inbytesStart address must be 32-bit alignedRAM subset must beinside RAM areaCannot be lower thanRAM_START and higherthan RAM_END address</td></tr><tr><td rowspan=1 colspan=1>End subset address inbytesHigher than StartAddrCannot be lower thanRAM_START and higherthan RAM_END addressSubset size (EndAddr-StartAddr) needs to bemultiple of 2 *RAM_BLOCK_SIZE, 32bytes</td></tr><tr><td rowspan=1 colspan=1>Pointer to next RAMsubset. See CautionMust be set to NULL forthe last subset</td></tr><tr><td rowspan=1 colspan=1>NumSectionsAtomic</td><td rowspan=1 colspan=1>Number of RAM sections to be tested duringan atomic testSet to 1, as minimum (one section per test)If the value is higher than the number ofsections in all subsets, all RAM subsets aretested in one pass</td></tr></table>

Table 23. STL_SCH_ConfigureRam output information  

<table><tr><td rowspan=1 colspan=2>STL_Status_t return value</td><td rowspan=1 colspan=2>*pSingleTmStatus output</td><td rowspan=2 colspan=1>Returned state</td></tr><tr><td rowspan=1 colspan=1>Value</td><td rowspan=1 colspan=1>Comments</td><td rowspan=1 colspan=1>Value</td><td rowspan=1 colspan=1>Comments</td></tr><tr><td rowspan=2 colspan=1>STL_OK</td><td rowspan=2 colspan=1>Function successfully executed</td><td rowspan=1 colspan=1>STL_NOT_TESTED</td><td rowspan=1 colspan=1></td><td rowspan=1 colspan=1>RAM_CONFIGURED</td></tr><tr><td rowspan=1 colspan=1>STL_ERROR</td><td rowspan=1 colspan=1>Possible source ofdefensiveprogramming error:•    State notallowedWrongconfigurationdetetedSTL internaldata corrupted</td><td rowspan=1 colspan=1>No state change</td></tr><tr><td rowspan=1 colspan=1>STL_KO</td><td rowspan=1 colspan=1>Possible source of defensiveprogramming error:•    pSingleTmStatus = NULLpRamConfig= NULLSTL internal data corrupted</td><td rowspan=1 colspan=1>Not relevant</td><td rowspan=1 colspan=1>Value must not beused</td><td rowspan=1 colspan=1>No state change</td></tr></table>

Aial inormaton:in the caseeturn value t LOorSigmSatet LRRR, the RAM configuration is not applied.

# 7.2.4.3

# STL_SCH_RunRamTM

Description: runs the RAM test.

Declaration: STL_Status_t STL_SCH_RunRamTM(STL_TmStatus_t \*pSingleTmStatus)

Table 24. STL_SCH_RunRamTM input information   

<table><tr><td rowspan=2 colspan=1>Allowed states</td><td rowspan=1 colspan=2>Parameters</td></tr><tr><td rowspan=1 colspan=1>Value</td><td rowspan=1 colspan=1>Comments</td></tr><tr><td rowspan=1 colspan=1>RAM_CONFIGURED</td><td rowspan=1 colspan=1>*pSingleTmStatus</td><td rowspan=1 colspan=1>See Caution</td></tr></table>

Table 25. STL_SCH_RunRamTM output information   

<table><tr><td rowspan=1 colspan=3>STL_Status_t return value</td><td rowspan=1 colspan=2>*pSingleTmStatus output</td><td rowspan=2 colspan=1>Returned state</td></tr><tr><td rowspan=1 colspan=1>Value</td><td rowspan=1 colspan=2>Comments</td><td rowspan=1 colspan=1>Value</td><td rowspan=1 colspan=1>Comments</td></tr><tr><td rowspan=5 colspan=1>STL_OK</td><td rowspan=4 colspan=2></td><td rowspan=1 colspan=1>STL_PASSED</td><td rowspan=1 colspan=1></td><td rowspan=1 colspan=1>RAM_CONFIGURED</td></tr><tr><td rowspan=1 colspan=1>STL_PARTIAL_PASSED</td><td rowspan=1 colspan=1></td><td rowspan=1 colspan=1>RAM_CONFIGURED</td></tr><tr><td rowspan=1 colspan=1></td><td rowspan=1 colspan=1>STL_FAILED</td><td rowspan=1 colspan=1></td><td rowspan=1 colspan=1>RAM_CONFIGURED</td></tr><tr><td rowspan=1 colspan=1>STL_NOT_TESTED</td><td rowspan=1 colspan=1>All subsets arealready tested</td><td rowspan=1 colspan=1>RAM_CONFIGURED</td></tr><tr><td rowspan=1 colspan=2>Function successfully executed</td><td rowspan=1 colspan=1>STL_ERROR</td><td rowspan=1 colspan=1>Possible source ofdefensiveprogramming error:State notallowed•    Configurationcorrupted•    STL internaldata corrupted</td><td rowspan=1 colspan=1>No state change</td></tr><tr><td rowspan=1 colspan=1>STL_KO</td><td rowspan=1 colspan=2>Possible source of defensiveprogramming error:pSingleTmStatus = NULLSTL internal data corrupted</td><td rowspan=1 colspan=1>Not relevant</td><td rowspan=1 colspan=1>Value must not beused</td><td rowspan=1 colspan=1>No state change</td></tr></table>

# 7.2.4.4

# STL_Status_t STL_SCH_ResetRam

Description: resets the RAM test.

Declaration: STL_Status_t STL_SCH_ResetRam(STL_TmStatus_t \*pSingleTmStatus)

Table 26. STL_SCH_ResetRam input information   

<table><tr><td rowspan=2 colspan=1>Allowed states</td><td rowspan=1 colspan=2>Parameters</td></tr><tr><td rowspan=1 colspan=1>Value</td><td rowspan=1 colspan=1>Comments</td></tr><tr><td rowspan=1 colspan=1>RAM_CONFIGURED</td><td rowspan=1 colspan=1>*pSingleTmStatus</td><td rowspan=1 colspan=1>See Caution</td></tr></table>

Table 27. STL_SCH_ResetRam output information   

<table><tr><td rowspan=1 colspan=2>STI_Status_t return value</td><td rowspan=1 colspan=2>*pSingleTmStatus output</td><td rowspan=2 colspan=1>Returned state</td></tr><tr><td rowspan=1 colspan=1>Value</td><td rowspan=1 colspan=1>Comments</td><td rowspan=1 colspan=1>Value</td><td rowspan=1 colspan=1>Comments</td></tr><tr><td rowspan=2 colspan=1>STL_OK</td><td rowspan=2 colspan=1>Function successfully executed</td><td rowspan=1 colspan=1>STL_NOT_TESTED</td><td rowspan=1 colspan=1>Configurationsuccessfully applied</td><td rowspan=1 colspan=1>RAM_CONFIGURED</td></tr><tr><td rowspan=1 colspan=1>STL_ERROR</td><td rowspan=1 colspan=1>Possible source ofdefensiveprogramming error:State notallowedConfigurationcorruptedSTL internaldata corrupted</td><td rowspan=1 colspan=1>No state change</td></tr><tr><td rowspan=1 colspan=1>STL_KO</td><td rowspan=1 colspan=1>Possible source of defensiveprogramming error:•    pSingleTmStatus = NULLSTL internal data corrupted</td><td rowspan=1 colspan=1>Not relevant</td><td rowspan=1 colspan=1>Value must not beused</td><td rowspan=1 colspan=1>No state change</td></tr></table>

# Additional information

Once all subsets are tested, the user needs to reset the test module to perform the RAM test again. In the case of a return value set to STL_KO or \*pSing1eTmStatus set to STL_ERROR, the RAM reset is not applied.

# 7.2.4.5

# STL_SCH_DelnitRam

Description: deinitializes the RAM test.

Declaration: STL_Status_t STL_SCH_DeInitRam(STL_TmStatus_t \*pSingleTmStatus)

Table 28. STL_SCH_DelnitRam input information   

<table><tr><td rowspan=2 colspan=1>Allowed states</td><td rowspan=1 colspan=2>Parameters</td></tr><tr><td rowspan=1 colspan=1>Value</td><td rowspan=1 colspan=1>Comments</td></tr><tr><td rowspan=1 colspan=1>RAM_IDLERAM_INITRAM_CONFIGURED</td><td rowspan=1 colspan=1>*pSingleTmStatus</td><td rowspan=1 colspan=1>See Caution</td></tr></table>

Table 29. STL_SCH_DelnitRam output information   

<table><tr><td rowspan=1 colspan=2>STL_Status_t return value</td><td rowspan=1 colspan=2>*pSingleTmStatus output</td><td rowspan=2 colspan=1>Returned state</td></tr><tr><td rowspan=1 colspan=1>Value</td><td rowspan=1 colspan=1>Comments</td><td rowspan=1 colspan=1>Value</td><td rowspan=1 colspan=1>Comments</td></tr><tr><td rowspan=1 colspan=1>STL_OK</td><td rowspan=1 colspan=1>Function successfully executed</td><td rowspan=1 colspan=1>STL_NOT_TESTED</td><td rowspan=1 colspan=1></td><td rowspan=1 colspan=1>RAM_IDLE</td></tr><tr><td rowspan=1 colspan=1>STL_KO</td><td rowspan=1 colspan=1>Possible source of defensiveprogramming error:pSingleTmStatus =NULLSTL internal data corrupted</td><td rowspan=1 colspan=1>Not relevant</td><td rowspan=1 colspan=1>Value must not beused</td><td rowspan=1 colspan=1>No state change</td></tr></table>

# 7.2.5

# Artificial-failing APIs

# 7.2.5.1

# STL_SCH_StartArtifFailing

Description: sets artificial-failing configuration and starts artificial-failing feature.

Declaration: STL_Status_t STL_SCH_StartArtifFailing(const STL_ArtifFailingConfig_t \*pArtifFailingConfig)

Table 30. STL_SCH_StartArtifFailing input information   

<table><tr><td rowspan=2 colspan=1>Allowed states</td><td rowspan=1 colspan=2>Parameters</td></tr><tr><td rowspan=1 colspan=1>Value</td><td rowspan=1 colspan=1>Comments</td></tr><tr><td rowspan=1 colspan=1>CPU TMx:•    CPU_TMx_CONFIGUREDFlash TM:FLASH_IDLE•    FLASH_INIT•    FLASH_CONFIGUREDRAM TM•    RAM_IDLERAM_INITRAM_CONFIGURED</td><td rowspan=1 colspan=1>*pArtifFailingConfig</td><td rowspan=1 colspan=1>No state change</td></tr></table>

Table 31. STL_SCH_StartArtifFailing output information   

<table><tr><td rowspan=1 colspan=1>STL_Status_treturn value</td><td rowspan=1 colspan=1>Comments</td><td rowspan=1 colspan=1>Output</td><td rowspan=1 colspan=1>Comments</td></tr><tr><td rowspan=1 colspan=1>STL_OK</td><td rowspan=1 colspan=1>Function successfully executed</td><td rowspan=2 colspan=1>No output parameter</td><td rowspan=2 colspan=1>No state change</td></tr><tr><td rowspan=1 colspan=1>STL_KO</td><td rowspan=1 colspan=1>Possible source of defensive programming error:pArtifFailingConfig=NULLconfigured values are not set for each testmodule.     STL internal data corrupted</td></tr></table>

se  LOK, thetestmodule satus(pSingleTmStatus,mLiStatusis forcdto conigurevalue.

# 7.2.5.2

# STL_SCH_StopArtifFailing

Description: stops the artificial-failing feature.

Declaration: STL_Status_t STL_SCH_StopArtifFailing(void)

Table 32. STL_SCH_StopArtifFailing input information   

<table><tr><td rowspan="2">Allowed states</td><td colspan="2">Parameters</td></tr><tr><td>Value</td><td>Comments</td></tr><tr><td>CPU TMx: • CPU_TMx_CONFIGURED</td><td rowspan="7">No input parameter</td><td rowspan="6"></td><td>No state change</td></tr><tr><td>Flash TM:</td></tr><tr><td>FLASH_IDLE •</td></tr><tr><td>FLASH_INIT •</td></tr><tr><td>FLASH_CONFIGURED</td></tr><tr><td>RAM TM</td></tr><tr><td>RAM_IDLE RAM_INIT</td><td></td></tr></table>

Table 33. STL_SCH_StopArtifFailing output information   

<table><tr><td rowspan=1 colspan=1>STI_Status_t return value</td><td rowspan=1 colspan=1>Comments</td><td rowspan=1 colspan=1>Output</td><td rowspan=1 colspan=1>Comments</td></tr><tr><td rowspan=1 colspan=1>STL_OK</td><td rowspan=1 colspan=1>Function successfully executed</td><td rowspan=2 colspan=1>No outputparameter</td><td rowspan=2 colspan=1>No state change</td></tr><tr><td rowspan=1 colspan=1>STL_KO</td><td rowspan=1 colspan=1>Possible source of defensiveprogramming error:STL internal data corrupted</td></tr></table>

# 7.3

# State machines

Each CPU test module has its own state machine diagram linked to the CPU test APls.

# CPU test APIs

![](images/77905a47adfa1b51e8c5a4513cb70e54bc501bfeacaafb3b7953ae85332a8c3b.jpg)  
Figure 11. State machine diagram - CPU test APIs

# Flash memory test APIs

![](images/513381ccc53a04b819e293a2d838fbda5713847a30603833445324ec22ab205d.jpg)  
Figure 12. State machine diagram - flash memory test APls

# RAM test APls

![](images/d9c341ec030cbbe53b533dafee6343847f128f204051c5b065cc2dea3295d081.jpg)  
Figure 13. State machine diagram - RAM test APls   
No)Once alubse are test the user nees reset he AM test module  perorm hees in.

# 7.4

# API usage and sequencing

The user application must:

Maintain the availability and integrityf pointers passed as parameters during the tests. The TLdos not copy the pointer content, and accesses directly the memory addresses defined by the application.

Check the status of function return value (sTLStatus_t), before checking the test result (STL_TmStatus_t or STL_TmListStatus_t). See the example in the delivered applications.

he APls run independently of each other and therefore can be called in any order.

Only APs dedicated to the configuration and initilizationof the memoris tests must be called before any execution of these tests is applied. See Section 7.3: State machines for more details.

The tt fows pli ll he e w eom C-oAl hedules cn le r cinurtidulplcatin ac seqnccluding hecmplete e executedoverl thememory areas beoreheplication ars. This sequence is defined in following order:

All the CPU tests

Complete tests of nonvolatile memory integrity

Fal l vbllall the stack

# Note:

Temporarily suppressing of thememor content backup can be applied o speedup intal testing o uge RAM areas where user does not need to preserve the memory content during this test. For more details see Secion 4.3.8: RAM backup buffer. Functional test is not executed over areas containing program code and data when the code is executed from RAM.

Specific customer tests

Lat t ere e  ehang execu nmorerelaxd wayTememory ust an eduhe et proe n evenbeyamically mod wi prfocu nhos where hemos recently executd safety related code and data re stor.This is especially the case when considering factors like:

Available application process safety time System overall performance Concrete status of the application

# 7.5 User parameters

In addition to parameters set directly inside the APls, there are few parameters to be customized in the stl_user_param_template.c file. They are located in the code, with the following comments:

customisable \*/

Extract from stl_user_param_template.c:

/\* Flash configuration \* #define STL_ROM_START (Ox08000000U) /\* customizable \* #define STL_ROM_END (0x0801FFFFU) / \* customizable \*

# The customization depends upon the STM32 product and the user choice.

/\* TM RAM Backup Buffer configuration \*/   
….   
/\* User shall locate the buffer in RAM \*/   
/\* The RAM backup buffer is placed in "backup_buffer_section" \* /\* "backup_buffer_section" section is defined in scatter file \*

The customizing depends on the user choice.

The remaining user parameters are defined by flags, and can be checked in the following files:

stl_user_param_template.c: use of RAM backup buffer or not   
st1_util. c: use of software or hardware CRC computation   
stlstm32_hw_config.h: if CRC hardware is used, choose the right CRC IP configuration according to   
the STM32 device

Refer to Section 5.5.2: Steps to build an application from scratch for the flag configuration check.

# B Test examples

Figure shows an example  a possible sequence STLAPI calls through th STL sheduler and reurne information provided by STL (refer to Figure 1 and Table 2).

![](images/6db0a09921a6b7a398f0d101912382f56fe9697cedcbe47779b41e5e1efd6d1c.jpg)  
Figure 14. Test flow example

Figure 15 shows a detailed example of flash memory test flow handling:

Use of two flash memory subsets   
Use of functions STL_SCH_RunFlashTM → only the flash memory test module is executed STL_SCH_ResetFlash

Function return value

Flash memory test module result value: pSing1eTmStatus → in this case, it contains the result of the flash memory test

Figure 16 shows a detailed example of RAM test flow handling:

Use of two RAM subsets

Use of functions: STL_SCH_RunRAMTM → only the RAM test module is executed STL_SCH_ResetRam

Function return value

RAM test module result value: pSing1eTmStatus → in this case, it contains the result of the RAM memory test

![](images/138bcb4dd9622d57eb0992dd07fff24c47e330867d4e648f96229d79264f5ece.jpg)  
Figure 15. Flash memory test flow example

![](images/dbeb1a3da3fce774d751c16cafac527110906e86a16d55d289a195281aacb3c0.jpg)  
Figure 16. RAM test flow example

# 9

# STL: execution timing details

Tae abl witheec p

Table 34. Integration tests   

<table><tr><td rowspan=2 colspan=1>Test</td><td rowspan=1 colspan=2>Duration (in µs)</td><td rowspan=2 colspan=1>Tested memory</td></tr><tr><td rowspan=1 colspan=1>Hardware CRC</td><td rowspan=1 colspan=1>Software CRC</td></tr><tr><td rowspan=1 colspan=1>STL_SCH_InitFlash</td><td rowspan=1 colspan=1></td><td rowspan=1 colspan=1>1</td><td rowspan=1 colspan=1></td></tr><tr><td rowspan=1 colspan=1>STL_SCH_ConfigureFlash</td><td rowspan=1 colspan=1>1</td><td rowspan=1 colspan=1>1</td><td rowspan=1 colspan=1></td></tr><tr><td rowspan=1 colspan=1>STL_SCH_RunFlashTM</td><td rowspan=1 colspan=1>267</td><td rowspan=1 colspan=1>766</td><td rowspan=1 colspan=1>34012 bytes tested</td></tr><tr><td rowspan=1 colspan=1>STL_SCH_InitRam</td><td rowspan=1 colspan=1>1</td><td rowspan=1 colspan=1>1</td><td rowspan=1 colspan=1></td></tr><tr><td rowspan=1 colspan=1>STL_SCH_ConfigureRam</td><td rowspan=1 colspan=1>1</td><td rowspan=1 colspan=1>1</td><td rowspan=1 colspan=1></td></tr><tr><td rowspan=1 colspan=1>STL_SCH_RunRamTM</td><td rowspan=1 colspan=1>182525</td><td rowspan=1 colspan=1>182525</td><td rowspan=1 colspan=1>1015771 bytes tested</td></tr><tr><td rowspan=1 colspan=1>STL_SCH_RunCpuTM1L</td><td rowspan=1 colspan=1>5</td><td rowspan=1 colspan=1>5</td><td rowspan=1 colspan=1></td></tr><tr><td rowspan=1 colspan=1>STL_SCH_RunCpuTM7</td><td rowspan=1 colspan=1>3</td><td rowspan=1 colspan=1>3</td><td rowspan=1 colspan=1></td></tr><tr><td rowspan=1 colspan=1>STL_SCH_RunCpuTMCB</td><td rowspan=1 colspan=1>3</td><td rowspan=1 colspan=1>3</td><td rowspan=1 colspan=1></td></tr></table>

# 10 Application-specific tests not included in ST firmware self-test library

Teus must focn l e aigequi tet ovei platin sec part ot incl the ST firmware library:

Test of analog parts (ADC/DAC, multiplexer) Test of digital I/O   
External addressing   
External communication   
Timing and interrupts   
System clock frequency measurement.

# Note:

The clock frequency measurement is not an integrated part of the STL package. The clock testing module is provided as open source within STL integration example to demonstrate the capability of implementing additional user defined testing modules which can be included at the STL flow. For more details refer to Secion 10.5: Extension capabilities STL library.

Aali solutionor hecpnentstrongly ependent naplicationan deviceperpheralcapabilyT lo design.

'ery often this method leads to redundancy at both hardware and software level

Hardware methods can be based on:

Multiplication of inputs and/or outputs   
Reference point measurement   
Loop-back read control at analog or digital outputs such as DAC, PWM, GPIO Configuration protection.

Software methods can be based on:

• Repetition nmultipleacquisitions,multiplhecdecsionscalculations adeat fferent me or performed by different methods Data redundancy (data copies, parity check, error correction/detection codes, checksum, protocol) Plausibility check (valid range, valid combination, expected change, or trend) Periodicity and occurrence checks (flow and occurrence in time controls) Periodic checks of correct configuration (for example, read back the configuration registers).

# .1 Analog signals

Measured values must be checked or consistencyand verified by measurements perormedon other redundant chaes. Free hanels an beuseorreading some eerencevoltages with testiganalog multiplexs used in the application. The internal reference voltage must also be checked.

Some STM32 microcontroller devices feature two (or even three) independent ADC blocks. To ensure the reiaility  the result, perform severl conversions on he samechanel using two different ADC bloks for security reasons. The results can be obtained using either:

Multiple acquisitions from one channel Compare redundant channels followed by an averaging operation. Here are some tips for testing the functionality of analog parts at STM32 microcontroller devices.

# ADC input pin disconnection

The ADC input pin disconnection can be tested by applying additional signal source on the tested pin.

Some STM32 microcontroller devices feature internal pull-down or pull-up resistor activation facilities on theanalog input.They can also feature a ree pin with DAfnctinality r digital GIOoutput.A e of these pins can be used as a known reference input to the ADC.

Some STM32 microcontroler devices feature a routing interface. This interface can be used for internal connection between pins to make:

testing loop-back   
additional signal injection   
duplicate measurement at some other independent channel.

# Note:

Tusermust prevent y citl oltaen nt analog Thi anap when digial an signals are combined and different power levels are applied to analog and digital parts (VDD > VDDA).

Internal reference voltage and temperature sensor (VBAt for some devices)

Ratio between these signals can be verified within the allowed ranges.   
Additional testing can be performed where the VDD voltage is known.

# ADC clock

Measurement of the ADC conversion time (by timers) can be used to test the independent ADC clock functionality.

# DAC output functionality

Free ADC channels can be used to check if the DAC output channel is working correctly. The routing interface can be used when connecting the ADC input channel and the DAC output channel

# Comparator functionality

Comparison between known voltage and DAC output or internal reference voltage can be used for testing comparator output on another comparator input.

Anal gal isconetion can e tested by pull-downr ulactivation n teste  ancopari signal with the DAC voltage as reference on another comparator input.

# Operational amplifier

Functionality can be tested forcing (ormeasuring) a known analog signal to the operational amplifier (OPAMP) evol wi .Teu l PAM measured by ADC (on another channel).

# 10.2 Digital I/Os

Clastaal/Iuy blhe somepliatin oeapla nal al oerau enor c whee/colgicn oSele or  ekypl correct lock sequence to the lock bit in the GPIOx_LCKR register. This action prevents unexpectd changes to g banding feature can be used for atomic manipulation of the SRAM and peripheral registers.

# 10.3 Interrupts

Occrencntmean perdicity events must  heck Diffrent methods can eus; themu a s ncremental countrs whee every iterrupt event icrements a speci counte. Tevalus e conters he crss-check pically witherdependent t bas.Tebvec within the last period depends upon the application requirements.

TxBueco st veioanol for non-safety relevant tasks if possible to simplify an application interrupt scheme.

# 10.4 Communication

Data exchange during communication sessions must be checked while including redundant information in the dt packes. ariy snc signals, Rcheck sus, block rpetitin, rprotool berng can  se oo c Peicy anoccurencein tief thecomunication events together wih protool err sials has o e checked permanently.

The user can find more information and methods in product-dedicated safety manuals.

# Extension capabilities STL library

This framework version features a significantly easierand more flexible mplementation than the previous ns h Llay e Scn.Reencocents) whi allowsrn eas extensn.Evn wi the ew appli rmat,heamewor keeps he same   f-estingmethods t comply with he IEC 60730 standard which are already implemented by previous versions of the library:

Test of registers at CPU TMs 32-bit CRC calculation compatible with STM32 HW CRC unit at Flash TM March C test respecting physical address order of the RAM TM

• Timer triggered by LSI to check system clock frequency of the clock TM defined at STL integration example The main improvements of the new framework version are:

Module oriented   
Supports partial testing   
Based on configuration and parametrizing structures   
No differentiation between startup and runtime test modules   
CRC calculation support based on a format provided by the STM32CubeProgrammer command-line feature   
Pre-compiled and fixed object code format of key generic modules   
No dependency of the generic modules execution on drivers or compilers   
Error handling includes reporting of defensive programing results   
Arial ailueontrol aturve properintegration emodules wit oeern instrumentation code   
Easy extension by additional application specific modules.

A eamplenditia secodulplentativailaleewaackgnte example. A specific test module based on the cross check measurement method of two independent clock elivuratgetherit cktrateapT must eapte yeutakenct secependencinheoigurtion he clock system.

This module uses the same measurement principlealready applied in previous versionsf the library. The harnstly ur a a STLuheTePr stb wi uP integrated in the STL so the same format is applied in its declaration:

STL_Status_t STL_SCH_RunClockTest(STL_TmStatus_t \*pSingleTmStatus)

The pareha i prl pineelcmoulmenu, and the nction itsel provides a STLKO vs STLOK retun status as well as do the regularSTLmodule lasmearement cce set o 8 consecutive LS perids) is ounat theexpecinterval defie b as CLK_LimitLow and CLK LimitHigh), the module measurement status value is changed into STL_PASSED. If is TLAILEs pe egulaPuehis is lso he as whel i module is invoked.

In rway herntraheolouls.Fopl  achareqsi stack boundary area check or implementing watchdog testing and servicing is no longer included at this new fotaloatn boueyizeyetho aeo ecaqu household standard. They may be useful to improve the user application robustness.

# 11 Compliance with IEC, UL, and CSA standards

The pivotal IEC standards are IEC 60730-1 and IEC 60335-1, harmonized with UL/CSA 60730-1 and UL/CSA 60335-1 starting from the 4th edition. Previous UL/CSA editions use references to the UL1998 standard in addition.

Taruolr a an obsolete certification can still comply and stay valid for newer editions of the standard.

The relevant detailed conditions required are defined in:

Annexes Q and R of the IEC 60335-1 norm Annex H of the IEC 60730-1 norm.

Three classes are defined by the IEC 60730-1:2010 H.2.22 they are:

Class A: control functions that are not intended to be relied upon for the safety of the application. Clntol ns ha n revntnsaentrollu of the control function does not directly lead to a hazardous situation.   
Clas C:control functions that are intended to prevent special hazards such as explosionor which failure could directly cause a hazard in the appliance.

For a programmable electronic component applying a safety protection function, the IEC 60335-1 standard tituol ul  ecbl.

Table R.1 summarizes general conditions comparable with requirements given for Class B level Table R.2 summarizes specific conditions comparable with requirements given for Class C level.

Rhi iluenulrey-eoy u at this level.

The osucharwar protecion qure Clasevecontng hat whateveraul at safey-l uz lys the implementation of specific hardware redundancy at system level, like dual channel structures.

more information on more stringent test methods, refer to the industrial documentation [1].

IEC73defies he aplicable rhitecures accptableorheesigClascnrol u

Single channel with functional test. A single CPU executes the software control functions as required. A funcional tes is perormeas the oftwarstarts. It guarntees that ll critial fatures work pry. Single channel with periodic self-test. A single CPU executes the software control functions. Embedded peridic tests check the various critical functions of he system without pacting the perormance the planned control tasks.   
Dual channel (homogeneous or diverse) with comparison. The software is designed to execute control fuctions (identically or differently on two independent PUs. Bot CPUs compare internal signals or fult detection when executing any safety-critical task.

# Note:

This structure is recognized to comply with Class C level also. A common principle is that whatever method complies with Class C automatically complies with Class B.

Anverve hemetho pli y TLand theencs esanarsten hetableo T nttol  plts.T par nderhe nds esibili as theestinmostaplicatispecand canbev eive p eneo in ST firmware self-test library for more information on how to handle these application-specific tests.

Table 35. IEC 60335-1 components covered by the X-CUBE-CLASSB library by methods recognized by IEC-60730-1   

<table><tr><td rowspan=1 colspan=2>Component of Table R.1 (IEC60335-1: Annex R)</td><td rowspan=1 colspan=1>Class B</td><td rowspan=1 colspan=1>References toIEC 60730-1:Annex H</td><td rowspan=1 colspan=1>Fault/error</td><td rowspan=1 colspan=1>Safety method appliedat X-CUBE-CLASSB</td><td rowspan=1 colspan=1>Note</td></tr><tr><td rowspan=5 colspan=1>1. CPU</td><td rowspan=1 colspan=1>1.1 CPU registers</td><td rowspan=1 colspan=1>X</td><td rowspan=1 colspan=1>H.2.16.5H.2.16.6H.2.19.6</td><td rowspan=1 colspan=1>Stuck at</td><td rowspan=1 colspan=1>Periodic run of the STLTM1L, TM7, and TMCBCPU test modules</td><td rowspan=1 colspan=1>Functional pattern test of theCPU registers,(general-purposeR0-R12, special-purpose mainand process stack pointers R13,program status APSR andCONTROL registers(</td></tr><tr><td rowspan=1 colspan=1>1.2 Instructiondecoding andexecuion</td><td rowspan=1 colspan=4>N/A</td><td rowspan=1 colspan=1>Not required for Class B</td></tr><tr><td rowspan=1 colspan=1>1.3 Programcounter</td><td rowspan=1 colspan=1>X</td><td rowspan=1 colspan=1>H.2.18.10.2H.2.18.10.4</td><td rowspan=1 colspan=1>Stuck at</td><td rowspan=1 colspan=1>N/AEnd-user responsibility</td><td rowspan=1 colspan=1>Logical and time slot programsequence monitoring,implementation of watchdogs</td></tr><tr><td rowspan=1 colspan=1>1.4 Addressing</td><td rowspan=1 colspan=4>N/A</td><td rowspan=1 colspan=1>Not required for Class B</td></tr><tr><td rowspan=1 colspan=1>1.5 Data pathinstructiondecoding</td><td rowspan=1 colspan=4>N/A</td><td rowspan=1 colspan=1>Not required for Class B</td></tr><tr><td rowspan=1 colspan=2> Interrupt handling and execution</td><td rowspan=1 colspan=1>X</td><td rowspan=1 colspan=1>H.2.18.10.4H2.18.18</td><td rowspan=1 colspan=1>No interruptor toofequentinterrupts</td><td rowspan=1 colspan=1>Handshake of results isapplied at the interruptassociated with a clockcross-checkmeasurement module</td><td rowspan=1 colspan=1>End-user responsibility for theother interrupts implemented ataplication</td></tr><tr><td rowspan=1 colspan=2>3. Clock</td><td rowspan=1 colspan=1>X</td><td rowspan=1 colspan=1>H.2.18.10.1H.2.18.10.4</td><td rowspan=1 colspan=1>Wrongfequency</td><td rowspan=1 colspan=1>Periodic run of clockcross-check module.Added at open sourceformat as a user specifictest module within thefirmware integrationexample</td><td rowspan=1 colspan=1>Clock cross-check measurementdone between two independentclock sources (system clock andLSI)</td></tr><tr><td rowspan=3 colspan=1>4. Memory</td><td rowspan=1 colspan=1>4.1 Invariablememory</td><td rowspan=1 colspan=1>X</td><td rowspan=1 colspan=1>H.2.19.3.1H.2.19.3.2H.2.19.8.2</td><td rowspan=1 colspan=1>All single bitfaults</td><td rowspan=1 colspan=1>Periodic execution of theSTL FlashTM test module</td><td rowspan=1 colspan=1>ECC enable under end-userresponsibility(2)</td></tr><tr><td rowspan=1 colspan=1>4.2. Variablememory</td><td rowspan=1 colspan=1>X</td><td rowspan=1 colspan=1>H.2.19.6H..19.8.2</td><td rowspan=1 colspan=1>DC fault</td><td rowspan=1 colspan=1>Periodic execution of theSTL RamTM test module</td><td rowspan=1 colspan=1>ECC or parity enable under end-user responsibility()</td></tr><tr><td rowspan=1 colspan=1>4.3 Addressingreleant for)varible andinvariablememory</td><td rowspan=1 colspan=1>X</td><td rowspan=1 colspan=1>H.2.19.8.2</td><td rowspan=1 colspan=1>Stuck at</td><td rowspan=1 colspan=1></td><td rowspan=3 colspan=1>Tested indirectly by execution ofthe applied memory testmodulesECC enable under end-userresponsibility(2)</td></tr><tr><td rowspan=2 colspan=1>5. Internaldata path</td><td rowspan=1 colspan=1>5.1 Data</td><td rowspan=1 colspan=1>X</td><td rowspan=1 colspan=1>H.2.19.8.2</td><td rowspan=1 colspan=1>Stuck at</td><td rowspan=1 colspan=1></td></tr><tr><td rowspan=1 colspan=1>5.2 Addressing</td><td rowspan=1 colspan=1>X</td><td rowspan=1 colspan=1>H.2.19.8.2</td><td rowspan=1 colspan=1>Wrongaddress</td><td rowspan=1 colspan=1></td></tr><tr><td rowspan=1 colspan=2>6. External communication</td><td rowspan=1 colspan=1>X</td><td rowspan=1 colspan=1></td><td rowspan=1 colspan=1>-</td><td rowspan=1 colspan=1>N/AEnd-user responsibility</td><td rowspan=1 colspan=1></td></tr><tr><td rowspan=1 colspan=2>7. I/O periphery</td><td rowspan=1 colspan=1>X</td><td rowspan=1 colspan=1></td><td rowspan=1 colspan=1></td><td rowspan=1 colspan=1>N/AEnd-user responsibility</td><td rowspan=1 colspan=1></td></tr><tr><td rowspan=1 colspan=2>Monitoring devices andcomparators</td><td rowspan=1 colspan=4>N/A</td><td rowspan=1 colspan=1>Not required for Class B</td></tr><tr><td rowspan=1 colspan=2>. Custom chips</td><td rowspan=1 colspan=1>X</td><td rowspan=1 colspan=1></td><td rowspan=1 colspan=1></td><td rowspan=1 colspan=1>N/A</td><td rowspan=1 colspan=1></td></tr></table>

CPU registers L14 and L15 are tested indirectly via defensive programming methods.

# Revision history

Table 36. Document revision history   

<table><tr><td>Date</td><td>Version</td><td>Changes</td></tr><tr><td>10-Jan-2024</td><td>1</td><td>Initial release.</td></tr></table>

# Glossary

ADC analog to digital converter   
AEABl Arm® embedded application binary interface   
API application programing interface   
APSR CPU status register   
BSP board support package

# Class B

middle level of regulations targeting safety for home appliances (UL/CSA/IEC 60730-1/60335-1)

cMsis common microcontroller software interface standard

CPU central processing unit   
CRC cyclic redundancy check   
DAC digital to analog conveter   
DCache data cache   
FPU floating-point unit   
GPIO general purpose input output   
HAL hardware abstraction level   
ICache instruction cache   
IDE integrated development environment   
LL low layer   
MCU microcontroller unit   
MPU memory protection unit   
MSP main stack pointer   
OPAMP operational amplifier   
PSP process stack pointer   
PWM pulse width modulation

RAM random access memory SDK software development kit STL self-test library TM test module

# Contents

# 1 General information

1.1 Purpose and scope. 2   
1.2 Reference documents.

# STM32Cube overview. 3

2.1 What is STM32Cube?. 3   
2.2 How does this software complement STM32Cube?. 3

# STL overview. 4

3.1 Architecture overview   
3.2 Supported products. 5

# STL description. 6

# 4.1 STL functional description 6

4.1.1 Scheduler principle. 6   
4.1.2 CPU Arm® core tests   
4.1.3 Flash memory tests. 8   
4.1.4 RAM tests . 10

# .2 STL performance data 12

4.2.1 STL execution timings. . 12   
4.2.2 STL code and data size 13   
4.2.3 STL stack usage . 13   
4.2.4 STL heap usage . 13   
4.2.5 STL interrupt masking time 13   
4.2.6 Data cache performance impact . 14

# .3 STL user constraints. 14

4.3.1 Privileged-level 14   
4.3.2 RCC resources . 14   
4.3.3 CRC resources . 14   
4.3.4 Bit Q of APSR . 15   
4.3.5 Interrupt management. 15   
4.3.6 DMA 15   
4.3.7 Supported memories. 15   
4.3.8 RAM backup buffer . 16   
4.3.9 Memory mapping 16   
4.3.10 Cortex M7 cache resources 16   
4.3.11 Processor mode 16

1.4 End-user integration tests 16

4.4.1 Test 1: correct STL execution 17   
4.4.2 Test 2: correct STL error-message processing 17

# Package description 18

5.1 General description. 18

# 5.2 Architecture 18

5.2.1 STM32Cube HAL 18   
5.2.2 Board support package (BSP). 19   
5.2.3 STL 19   
5.2.4 User application example 19   
5.2.5 STL integrity 19

5.3 Folder structure 20

# 5.4 APIs 20

5.4.1 Compliance. 20   
5.4.2 Dependency 21   
5.4.3 Details. 21

# 5.5 Application: compilation process 21

5.5.1 Steps to build delivered STL example . . 21   
5.5.2 Steps to build an application from scratch. 22

# Hardware and software environment setup. 24

6.1 Hardware setup. 24

6.2 Software setup. 24

6.2.1 Development tool-chains and compilers 24   
6.2.2 CRC tool set-up 25

# STL: User APIs and state machines 26

7.1 User structures 26

# 7.2 User APIs. 26

7.2.1 Common API. 27   
7.2.2 CPU Arm® core testing APIs. 27   
7.2.3 Flash memory testing APIs 28   
7.2.4 RAM testing APIs. 32   
7.2.5 Artificial-failing APIs 36

7.3 State machines 37

7.4 API usage and sequencing 40   
7.5 User parameters 41

# Test examples 42

STL: execution timing details 46

# 10 Application-specific tests not included in ST firmware self-test library . .. .47

10.1 Analog signals . .47   
10.2 Digital I/Os . .48   
10.3 Interrupts 48   
10.4 Communication 49   
10.5 Extension capabilities STL library 49

# 11 Compliance with IEC, UL, and CSA standards 50

Revision history .52   
Glossary .53   
List of tables .57   
List of figures. .58

# List of tables

Table 1. Applicable product . 1   
Table 2. STL return information 7   
Table 3. STL execution timings, clock at 400 MHz 13   
Table 4. STL code size and data size (in bytes) 13   
Table 5. STL maximum interrupt masking information . 14   
Table 6. STL_SCH_Init input information. 27   
Table 7. STL_SCH_Init output information. 27   
Table 8. STL_SCH_RunCpuTMx input information 27   
Table 9. STL_SCH_RunCpuTMx output information 28   
Table 10. STL_SCH_InitFlash input information . 28   
Table 11. STL_SCH_InitFlash output information . 28   
Table 12. STL_SCH_ConfigureFlash input information 29   
Table 13. STL_SCH_ConfigureFlash output information 30   
Table 14. STL_SCH_RunFlashTM input information . . 30   
Table 15. STL_SCH_RunFlashTM output information. 31   
Table 16. STL_SCH_ResetFlash input information . 31   
Table 17. STL_SCH_ResetFlash output information 31   
Table 18. STL_SCH_DelnitFlash input information . 32   
Table 19. STL_SCH_DelnitFlash output information 32   
Table 20. STL_SCH_InitRam input information 32   
Table 21. STL_SCH_InitRam output information 32   
Table 22. STL_sCH_ConfigureRam input information. 33   
Table 23. STL_sCH_ConfigureRam output information. 34   
Table 24. STL_SCH_RunRamTM input information 34   
Table 25. STL_SCH_RunRamTM output information 35   
Table 26. STL_sCH_ResetRam input information 35   
Table 27. STL_SCH_ResetRam output information 35   
Table 28. STL_SCH_DelnitRam input information 36   
Table 29. STL_SCH_DelnitRam output information 36   
Table 30. STL_SCH_StartArtifFailing input information. 36   
Table 31. STL_SCH_StartArtifFailing output information 37   
Table 32. STL_SCH_StopArtifFailing input information 37   
Table 33. STL_SCH_StopArtifFailing output information 37   
Table 34. Integration tests. 46   
Table 35. IEC 60335-1 components covered by the X-CUBE-CLASSB library by methods recognized by IEC-60730-1. 51   
Table 36. Document revision history . 52

# List of figures

Figure 1. STL architecture . 4   
Figure 2. Single test control call architecture 7   
Figure 3. Flash memory test: CRC principle . 9   
Figure 4. Flash memory test: CRC use cases versus program areas. 10   
Figure 5. RAM test: usage . 12   
Figure 6. Software architecture overview . 18   
Figure 7. Project file structure 20   
Figure 8. IAR™ post-build actions screenshot. 23   
Figure 9. CRC tool command line . 23   
Figure 10. STM32 Nucleo board example 24   
Figure 11. State machine diagram - CPU test APls. 38   
Figure 12. State machine diagram - flash memory test APls 39   
Figure 13. State machine diagram - RAM test APIs 40   
Figure 14. Test flow example . 42   
Figure 15. Flash memory test flow example. 44   
Figure 16. RAM test flow example 45

# IMPORTANT NOTICE  READ CAREFULLY

ST products and/or to this document any time without notice.

T

conditions

purchasers' products.

granted by ST herein.

are the property of their respective owners.