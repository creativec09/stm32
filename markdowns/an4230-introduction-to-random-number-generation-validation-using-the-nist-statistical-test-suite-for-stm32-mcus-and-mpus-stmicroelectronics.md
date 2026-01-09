# Introduction to random number generation validation using the NiST statistical test suite for STM32 MCUs and MPUs

# Introduction

(RNGs), to verify that their output is indeed random.

Thlton o elitioeeat I 02A 010S00( statistical test suite (STS).

This document is structured as follows:

A general introduction to the STM32 microcontroller random number generator. See Section 1.   
The NIST SP800-22rev1a test suite. See Section 2.   
The steps needed to run NIST SP800-22rev1a test and analysis. See Section 3.   
The NIST SP800-90b test suite. See Section 4.   
The steps needed to run the NIST SP800-90b test and analysis. See Section 3.

Table 1. Applicable products   

<table><tr><td rowspan=2 colspan=2>Type</td><td rowspan=1 colspan=2>Products</td></tr><tr><td rowspan=1 colspan=1>Can be checked with SP800-22rev1a</td><td rowspan=1 colspan=1>Can be checked with SP800-90b</td></tr><tr><td rowspan=2 colspan=1>Microcontrollers</td><td rowspan=1 colspan=1>Series</td><td rowspan=1 colspan=1>STM32F2 series, STM32F4 series, STM32F7 series,STM32L0 series, STM32L4 series, STM32G4 series,STM32WB series.</td><td rowspan=1 colspan=1>STM32WBA series, STM32H5 series, STM32L5 series,STM32U0 series, STM32U5 series, STM32WL series,STM32MP2 series, STM32N6 series, STM32U3 series.</td></tr><tr><td rowspan=1 colspan=1>Lines</td><td rowspan=1 colspan=1>STM32H742, STM32H743/753, STM32H745/755,STM32H747/757 lines, STM32H750 value line,STM32L4R5/S5, STM32L4R7/S7, STM32L4R9/S9 lines,STM32G0x1 lines, STM32MP15x lines.</td><td rowspan=1 colspan=1>STM32H7R3/7S3 line, STM32H7R7/7S7 line,STM32H7A3/7B3 line, STM32H7B0 value line,STM32H723/733, STM32H725/735,STM32H730 value line, STM32L4P5/Q5 line,STM32MP13x lines.</td></tr></table>

# 1 STM32 MCU RNG

# RNG overview

Random number generators (RNGs) used for cryptographic applications typically produce sequences made random O's and 1's bits.

There are two basic classes of random number generators:

Deterministic RNG or pseudo RNG (PRNG)   
AdeterministicRNGconsistsan algorithm that produces a sequence  bitfrom an initial value calla s.To ensureforward upredictability caremust e taken ntainig ses.The valus produc by a PRNGare completely predictable if the seed and generation algorithm are known.Since in many cases the generation algorithm is publicly available, the seed must be kept secret and generated from a TRNG. Non-deterministic RNG or true RNG (TRNG)   
A non-deterministic RNG produces randomness that depends on some unpredictable physical source (the entropy source) outside of any human control.

The RNG hardware peripheral implemented in some STM32 MCUs is a true random number generator.

# 1.2

# STM32 MCU implementation description

Note:

The table below lists the STM32 Arm® Cortex® core-based MCUs that embed the RNG peripheral.   
Arm is a registered trademark of Arm Limited (or its subsidiaries) in the US and/or elsewhere.

arm

Table 2. STM32 lines embedding the RNG hardware peripheral   

<table><tr><td rowspan=1 colspan=1>Series</td><td rowspan=1 colspan=1>STM32 lines</td></tr><tr><td rowspan=1 colspan=1>STM32F2 series</td><td rowspan=1 colspan=1>All lines</td></tr><tr><td rowspan=1 colspan=1>STM32F4 series</td><td rowspan=1 colspan=1>STM32F405/415, STM32F407/417, STM32F410, STM32F412, STM32F413/423,STM32F427/437, STM32F429/439, STM32F469/479</td></tr><tr><td rowspan=1 colspan=1>STM32F7 series</td><td rowspan=1 colspan=1>All lines</td></tr><tr><td rowspan=1 colspan=1>STM32L0 series</td><td rowspan=1 colspan=1>STM32L05x, STM32L06x, STM32L072/073</td></tr><tr><td rowspan=1 colspan=1>STM32L4 series</td><td rowspan=1 colspan=1>All lines</td></tr><tr><td rowspan=1 colspan=1>STM32L4+ series</td><td rowspan=1 colspan=1>All lines</td></tr><tr><td rowspan=1 colspan=1>STM32H5 series</td><td rowspan=1 colspan=1>All lines</td></tr><tr><td rowspan=1 colspan=1>STM32H7 series</td><td rowspan=1 colspan=1>All lines (1)</td></tr><tr><td rowspan=1 colspan=1>STM32L5 series</td><td rowspan=1 colspan=1>All lines</td></tr><tr><td rowspan=1 colspan=1>STM32U0 series</td><td rowspan=1 colspan=1>All lines</td></tr><tr><td rowspan=1 colspan=1>STM32U5 series</td><td rowspan=1 colspan=1>All lines</td></tr><tr><td rowspan=1 colspan=1>STM32G0 series</td><td rowspan=1 colspan=1>STM32G081xB, STM32G041x6, STM32G041x8, STM32G061x6, STM32G061x8,STM32G0C1xC, STM32G0C1xE</td></tr><tr><td rowspan=1 colspan=1>STM32G4 series</td><td rowspan=1 colspan=1>All lines</td></tr><tr><td rowspan=1 colspan=1>STM32MP1 series</td><td rowspan=1 colspan=1>All lines</td></tr><tr><td rowspan=1 colspan=1>STM32WBA series</td><td rowspan=1 colspan=1>STM32WBA52</td></tr><tr><td rowspan=1 colspan=1>STM32WB series</td><td rowspan=1 colspan=1>All lines</td></tr><tr><td rowspan=1 colspan=1>STM32WL series</td><td rowspan=1 colspan=1>All lines</td></tr><tr><td rowspan=1 colspan=1>STM32MP2 series</td><td rowspan=1 colspan=1>All lines</td></tr><tr><td rowspan=1 colspan=1>STM32N6 series</td><td rowspan=1 colspan=1>All lines</td></tr><tr><td rowspan=1 colspan=1>STM32U3 series</td><td rowspan=1 colspan=1>All lines</td></tr></table>

Except the followig partumer, which don' embe RNG peripheralsSTM32H745BG STM32H745XG STM32H7G, STM32H747AG, STM32H747AI, STM32H747BG, STM32H747IG, STM32H747I, STM32H747XG, STM32H757AI, STM32H757II.

The true RNG implemented in the STM32 MCUs is based on an analog circuit. This circuit generates a continuous analog noise that is used in the RNG processing to produce a 32-bit random number. The analog circuit is made of several ring oscillators whose outputs are XORed.

The RNG processing is clocked by a dedicated clock at a constant frequency and, for a subset of nicrocontrollers, the RNG-dedicated clock can be reduced using the divider inside the RNG peripheral.

For more details about the RNG peripherals, refer to the STM32 reference manuals.

1e figures below show a simplified view of a true RNG in STM32 microcontrollers.

![](images/772044d2da362a2d71fbe20b77d7032931d233262b44cada9138d1d1adf79d30.jpg)  
Figure 1. STM32 true RNG block diagram of the products verified with the SP800-22rev1a

![](images/7369e7cfc74304f8981d7d60e979d5792b212b800bc2ffcba2f281db0616ed25.jpg)  
Figure 2. STM32 true RNG block diagram of the products verified with the SP800-90b

# 2 NIST SP800-22rev1a test suite

# 2.1 NIST SP800 22rev1a overview

T I0-aial sui robhealGpraphapl. Acehensiveiptione  presnte nhe ocentiSatisilTe the Validation of Random Number Generators and Pseudo Random Number Generators for Cryptographic Applications.

# NIST SP800-22rev1a test suite description

The NI 2reva tatiical test suists-.1.s a sota package eveloped by NSI that can e downloaded from the NIST web site (search or download the NIST Statistical Test Suite at csrc.nist.gov).

The soure code has been write  S The  staistical tst suit consist   tests that ve randomness of a binary sequence. These tests focus on various types of non-randomness that can exist in a sequence.

These test can be classified as follows:

Frequency tests

Frequency (Monobit) test   
To measure the distribution of O's and 1's in a sequence and to check if the result is similar to theon expected for a truly random sequence.   
Frequency test within a block   
To check whether the frequency of 1's in an Mbit block is approximately M/2, as expected from the theory of randomness.   
Run tests   
To assess if the expected total number of runs of 1's and O's of various lengths is as expected for a random sequence.   
Test of the longest run of 1's in a block   
To examine the long runs of 1's in a sequence. Test of linearity

Test of linearity

Binary matrix rank test   
To assess the distribution of the rank for 32 x 32 binary matrices. Linear complexity test   
To determine the linear complexity of a finite sequence.

est of correlation (by means of Fourier transform)

Discrete Fourier transform (spectral) test   
To assess the spectral frequency of a bit string via the spectral test based on the discrete Fourier transform. It is sensitive to the periodicity in the sequence.

Test of finding some special strings

Non-overlapping template matching test To assess the frequency of Mbit non-periodic patterns. Overlapping template matching test To assess the frequency of Mbit periodic templates.

Entropy tests

Maurer's "Universal Statistical" test   
To assess the compressibility of a binary sequence of L-bit blocks. Serial test   
To assess the distribution of all 2m Mbit blocks.

# Note:

For m = 1, the serial test is equivalent to the frequency test.

Approximate entropy test

To assess the entropy of a bit string, comparing the frequency of all Mbit patterns against all (m+1)-bit patterns.

Random walk tests

Cumulative sums (Cusums) test   
Taess that e sum  partial squenes isot too larger to small it isdicativef tooman O's or 1's.   
Random excursion test   
To assess the distribution of states within a cycle of random walk.   
Ts hat e s partalun ot o armaiativ t O's or 1's.   
Random excursion variant test   
To detect deviations from the expected number of visits to different states of the random walk.

Taalculavahi bl jenerated a sequence less random than the sequence that was tested.

Fo etbu eNIl  eol NI  vaabl  NIST web site: A Statistical Test Suite for Random and Pseudorandom Number Generators for Cryptographic Applications" Special Publication 800-22 Revision 1a.

# 3 NIST SP800-22rev1a test suite running and analyzing

# 3.1

# Firmware description

Te satitial  sui  debe nhe revi ecn,ae ee STM32 microcontroller side and one on the NIST SP800-22rev1a test suite side.

# 3.1.1

# STM32MCU side

The firmware package is provided upon request. For more details, contact the local S sales representative. This program allows random numbers generation, using the STM32 RNG peripheral. It also retrieves these numbers on a workstation for testing with the NIST statistical test suite.

Each firmware program is used to generate 0 4-Kbyte blocks of random numbers.The output file contains 5,120,000 random bits to be tested with the NIST statistical test.

recommended by the NIST statistical test suite, the output file format can be one of the followings:

a sequence of ASCIl O's and 1's if the FILE_ASCII_FORMAT Private define is uncommented in themin. file

• Ainary rnbyheILEBNARYFR Privatefincmen n the

For more etails about the program desription and settings, reer the rade nsidehe fwae package.

# Note:

The USART configuration can be changed via the SendToWorkstation () function in the main. file The output values can be changed by modifying the Private define in the main.  file as follows:

#define NUMBER _OF_RANDOM_BITS_TO_GENERATE 512000

#define BLOCK_NUMBER 10

# 3.1.2

# On the NIST SP800-22rev1a test suite side

Downloaded on a workstation, the NIT statistical test suite package sts-2.1.1verifies the andomness  e output file of the STM32 RNG peripheral.

The generator file to be analyzed must be stored under the data folder (sts-2.1.1 \data).

For more details about how the Ni statistical tests work, refer to section 'How to gt started in the NIST document A Statistical Test Suite for Random and Pseudorandom Number Generators for Cryptographic Applications.

# 3.2

# NISTSP800-22rev1a test suite steps

The figure belowdescribes the tepsneeded tovery the randomness an output number generated by STM32 MCUs using the NIST statistical test suite package sts-2.1.1.

![](images/d23b299e793c61c48e94b644082a28917ce62001df57d2f4c6ac7aef6dbd314a.jpg)  
Figure 3. Block diagram of deviation testing of a binary sequence from randomness based on NIST test suite

# 3.2.1

# Step1: random number generator

Co barhewortatDepenybrhein

via a null-modem female/female RS232 cable via a USB Type-A to Mini-B cable

The STM32 RNG is run via the UART firmware in order to generate a random number as described in Son..at or he woksatin sal ulain apliatin uc and open-source terminal emulator, serial console and network file transfer application).

# 3.2.2

# Step 2: NIST statistical tes

T  pkpibehe aal  uta an executable program using visual C++ compiler.

Al   a data to be analyzed and the statistical tests to be applied.

Inln o  il  s nerhe sav the NIsT_Test_Suite_OutputExample folder. As described previously, the random number is defined as 512,000 bits per block.

The various steps are detailed as follows:

1.The first screen that appears is shown below.

![](images/dd65e253e988dcea50113c4dbec96fdb3699ba45c7b6a9c20af499eb299cade0.jpg)  
Figure 4. Main sts-2.1.1 screen

When value  is entered, he program requires to enter he fe name and path of the random number to be tested.

2The second screen is shown below.

![](images/0e098ed8c57db173f6f9a8c6e8c1ae7ed0b8e831951ae5d093b7d204c0baaef3.jpg)  
Figure 5. File input screen

This application note details an example with two files per series, generated with the STM32 RNG, with the following file formats as recommended by NIST:

ascii.bin: sequence of ASCll O's and 1's binary. bin: each byte in the data file contains 8 bits of data

The NIST statistical test suite displays 15 tests that can be run via the screen shown below.

![](images/6698210ac782ddcb51e55d0e008c44a5611d284287539d0deccf4472d7f031bd.jpg)  
Figure 6. Statistical test screen

In this case, 1 has been selected to apply all of the statistical tests.

4The parameter adjustments ca be done in the screen shown below.

![](images/ef078f36ef26f91d544798056f608f71be9cbea4b20055f1c54d0c669d617bd2.jpg)  
Figure 7. Parameter adjustment screen

In this example, the default settings are kept and value 0 is selected to go to the next step.

5The user needs to provide the number of bitstreams.

![](images/c52f15eefb4e62763ae9c17195da2c89bff4fb5e17f66e0976785faa2147be9d.jpg)  
Figure 8. Bitstream input

The NIT statistical test suite requires to put the numberof bitstreams: 10 is entered for this example, meaning 10 blocks of 512 Kbits are selected (5,12 Mbits).

The user must then specify whether the fil consistsf bits stored in ACl format or hexadecimal strigs stored in a binary format using the following screen.

![](images/834e9cfe4e90399fb76f2f8a273d822f434830f4fca178f7c57912b97d1a6060.jpg)  
Figure 9. Input file format

Value O is selected because the file is in ASCll format.

After entering all necessary inputs, the NIST statistical test suite starts analyzing the input file.

![](images/b58ec9a9b4bc400d75bb9b44078f6a55cab08863d3a1ca0064299b8d4762bed8.jpg)  
Figure 10. Statistical testing in progress

When the testing process is complete, the screen below appears.

![](images/3042d6cd83e0cb50709a084e5ba8ff4bdb0e44219b3d9088772ce609ac21f5cf.jpg)  
Figure 11. Statistical testing complete

The statistical test results can be found in sts-2.1.1\experiments \AlgorithmTesting.

# 3.2.3

# Step 3: test report

Tl  u finalAnaysisReportis generated when the statistical testingis complete and savedunderts..experime nts\AlgorithmTesting.

The repo cntains  aryepmenal esult  et I0-2atisical . The NIST statistical tests also provide a detailed report for each test, saved under

sts-2.1.1\experiments\AlgorithmTesting\<Test suite name>.

The two following examples of complete NIST statistical test suite output reports are available under

NIST_Test_Suite_OutputExample:

example of an Ascii_File_Format, with two folders:

Input_File: contains the random number generator saved with the ascii format. Final_Analysis_Report: contains the complete NIST statistical test suite output report based on this input file, the summary of experimental results and the report of each test.

example of a Binary_File_Format, with two folders:

Input _File: contains the random number generator saved with the binary format. Final_Analysis_Report: contains the complete NIST statistical test suite output report based on this input file, the summary of experimental results and the report of each test.

# 4 NIST SP800-90b test suite

# Cryptographic random bit overview

The cryptographic random bit generators (RBGs), also known as random number generators (RNGs), require a noise source that produces outputs with some level of unpredictability, expressed as min-entropy.

The specificity of the NIST SP800-90b statistical test suite is to probe the quality of random generators for cryptographic applications by its standardized means of estimating the quality of a source of entropy.

A comprehensive description of the suite is presented in the NIST document entitled Recommendation r the Entropy Sources Used for Random Bit Generation.

The NIST SP800-90b statistical test suite can be downloaded from the GitHub web site (https://github.com/ usnistgov/SP800-90B_EntropyAssessment).

# NIST SP800 90b test suite validation steps

The SP800-90B_EntropyAssessment C++ package implements the min-entropy assessment methods included in Special publication 800-90B.

T ure hat  the equiements  he N Spel ublication SP) 800-0 sr ecomendations e it is necessary to validate the entropy source.

The general flow of entropy source validation testing is summarized in the steps below:

Restart tests.

5Entropy estimation for entropy sources using a conditioning component.

Additional noise sources.

The project is composed of two separate sections:

-non-lID tests: provide an estimate for min-entropy, called Horiginal, for any data provided (the STM32   
certifiable TRNG noise source is tested using non-lIID tests)   
--estart testscheck the relations between noise source samples generate after restarting he entropy   
source, and compare the results to the initial entropy estimate HI

# Note:

H=Horauit iay ur whesuhe ntroy t provibas submitter's analysis of the noise source.

# Firmware description used for RNG NIST evaluation

# 5.1

# STM32 MCU side

# 5.1.1

# Data collection descriptior

Random datasets are extracted from STM32-RNG peripheral entropy sources using the interrupt method (see Figure. The USART is used to send the generated raw data to the workstation to be tested with the NIT statistical test suite.

1,024,000 random samples are generated continuously from the RNG peripheral with the conditioning stage deactivated. Then it is shortened to keep exactly 1,000,000 samples. Sampled data are converted to binary in order to respect the format required by NIST SP800-90b tool suite. These binaries are used for the continuous tests.

1024 x 1000 random samples are extracted with restart at every 1000 bits extracted. They are then shortened to get 1000 x1000 samples as recommended by NIST. In restart extraction, 1000 unconditioned samples are collected directly fom the noisesource by dsabling/enabling the RNG oreach restart mong the 1024 restarts required.

This randatat an eextracttherwit coletig cntious b without iablingheGmou with restarting the RNGat evey 1000 bits.The output fle format is a sequenc o hexadecimal digits ASCll forat, whic converteto iary orat without alteration atusia al Python scrptwy random bits are ready to be processed by NIST tests suite in \*.bin dataset format.

An STM32 USART peripheral is configured to establish USB communication between the STM32 board and a workstation.

# 5.1.2 STM32 firmware description

CPU system modules, PLL clocks, and peripherals used within the system are configured in the system initialization (see Figure 12).

RNGinitialization function activates heRNG in the control register with theconditioningstagedeactivated. A health test module is also activated by writing suitable values to the HTCR register. To be aligned with NIST recommended configuration in the reference manual. The RNG interrupt setting is also performed by this function.

Ahardwae e, hema program wairheufilment  block yndo b be them to the workstation. When the number of blocks reaches its maximum value, the system execution is stopped and the 1 megabit random dataset is stored in a log file within the workstation.

When the IE Interrupt Enable) bit is set in the RNG control register, RNG triggers an interrupt each time new 32 random bits are available in the RNG data register (see Figure 13). A callback function is then executed (HAL_RNG_ReadyDataCallback), it extracts the 32 bits raw data and stores them in an STM32 internal memory. When a block of settable size is fulfilled and the maximum of block number is reached, two user flags become true accordingly (NewBlockFlag and EndOfCollect). Flags are supervised by the main function to control data transmission to the workstation.

The activation of interrupts can trigger a second callback function (HAL_RNG_ErrorCal1back) to run when the RNG detects seed or clock errors. A counter of errors is consequently incremented, RNG is then restarted, and the current dataset extraction is canceled (see Figure 14.

Note that the HTCR value is characterized for NIST certification to minimize the seed errors without causing any clock errors. In ths expermentation,  seed errors wee detected durig extraction acoring to this HTCR value.

Two extraction modes are performed, with restart at every 1000 bits and continuous without restart: When 1000 x 1024 restart dataset is to be extracted, the following macros definitions are considered.

/\* number of random bits\*/   
#define NUMBER OF RANDOM BITS 1024   
/\* number of 32bits words\*/   
#define NUMBER_OF_RANDOM_32_BITS NUMBER_OF_RANDOM_BITS /32   
/\* number of restarts \*   
#define BLOCK_NUMBER 1000

When continuous 1,024,000 dataset bits are to be extracted, the following macros definitions are considered.

/\* number of random bits\*/   
#define NUMBER OF RANDOM BITS 1024\*1000   
/\* number of 32bits words\*/   
#define NUMBER_OF_RANDOM_32_BITS NUMBER_OF_RANDOM_BITS /32   
/\* number of restarts \*   
#define BLOCK NUMBER 1

# Note:

In ctinuus extracn mod, thee a block is t t1,024,00 and theumber block is set that the RNG is disabled only after the generation of the entire dataset.

The figures below show the different function description modes.

![](images/a8a9ee8005da3adac21ec3c8dad5fc5152590928c0bf1eed2dd76bf51274b7cd.jpg)  
Figure 12. Main function in interrupt mode

![](images/df4bdcb01f7f5481dfcfaa093b685e0897568a1ca1552cff4f2f0e674253f635.jpg)  
Figure 13. ISR callback function when DRDY interrupt flag is set

![](images/02190d9422afd6a9123ce3daa065584c3a776d12309475b27207ea026e055620.jpg)  
Figure 14. ISR callback function when Error-flag

# 5.1.3

# NIST compliant RNG configuration

The table below summarizes the RNG configuration values that are recommended for the entropy source to be compliant with NIST SP 800-90B. Those configurations correspond to an RNG clock of 48 MHz. The certificate column indicates when the configuration values are part of a NIST SP800-90B CMVP certification.

Table 3. RNG register values   

<table><tr><td rowspan=1 colspan=1>Product(1)</td><td rowspan=1 colspan=1>RNG_CR value(2)</td><td rowspan=1 colspan=1>HTCR value</td><td rowspan=1 colspan=1>NSCR value</td><td rowspan=1 colspan=1>Certificate(3)</td></tr><tr><td rowspan=1 colspan=1>STM32L4P/Q</td><td rowspan=1 colspan=1>0x00F00D00</td><td rowspan=1 colspan=1>0xAA74</td><td rowspan=1 colspan=1>default</td><td rowspan=1 colspan=1></td></tr><tr><td rowspan=1 colspan=1>STM32L5</td><td rowspan=1 colspan=1>0x00F00D00</td><td rowspan=1 colspan=1>0xA2B3</td><td rowspan=1 colspan=1>default</td><td rowspan=1 colspan=1></td></tr><tr><td rowspan=1 colspan=1>STM32U0</td><td rowspan=1 colspan=1>Ox00F00D00</td><td rowspan=1 colspan=1>0xAAC7</td><td rowspan=1 colspan=1>default</td><td rowspan=1 colspan=1>-</td></tr><tr><td rowspan=1 colspan=1>STM32U575/585</td><td rowspan=1 colspan=1>0x00F00D00</td><td rowspan=1 colspan=1>0xA2B0</td><td rowspan=1 colspan=1>0x17CBB</td><td rowspan=1 colspan=1>Yes</td></tr><tr><td rowspan=1 colspan=1>STM32U59x/5Ax</td><td rowspan=1 colspan=1>Ox00F10F00</td><td rowspan=1 colspan=1>0x92F3</td><td rowspan=1 colspan=1>0x1609</td><td rowspan=1 colspan=1>Yes</td></tr><tr><td rowspan=1 colspan=1>STM32U535/545</td><td rowspan=1 colspan=1>Ox00F10F00</td><td rowspan=1 colspan=1>0x76B3</td><td rowspan=1 colspan=1>0x24C2</td><td rowspan=1 colspan=1>Yes</td></tr><tr><td rowspan=1 colspan=1>STM32U5Fx/5Gx</td><td rowspan=1 colspan=1>Ox00F10F00</td><td rowspan=1 colspan=1>0xA715</td><td rowspan=1 colspan=1>0x9049</td><td rowspan=1 colspan=1>Yes</td></tr><tr><td rowspan=1 colspan=1>STM32H7Rx/7Sx</td><td rowspan=1 colspan=1>0x08F00E00</td><td rowspan=1 colspan=1>0x6a92</td><td rowspan=1 colspan=1>0x2f83f</td><td rowspan=1 colspan=1>-</td></tr><tr><td rowspan=1 colspan=1>STM32H7A3/7B3</td><td rowspan=1 colspan=1>0x00F00D00</td><td rowspan=1 colspan=1>0x72AC</td><td rowspan=1 colspan=1>default</td><td rowspan=1 colspan=1></td></tr><tr><td rowspan=1 colspan=1>STM32H72x/73x</td><td rowspan=1 colspan=1>Ox00F00D00</td><td rowspan=1 colspan=1>0xAA74</td><td rowspan=1 colspan=1>default</td><td rowspan=1 colspan=1></td></tr><tr><td rowspan=1 colspan=1>STM32WLx</td><td rowspan=1 colspan=1>0x00F00D00</td><td rowspan=1 colspan=1>OxAA74</td><td rowspan=1 colspan=1>default</td><td rowspan=1 colspan=1></td></tr><tr><td rowspan=1 colspan=1>STM32H503</td><td rowspan=1 colspan=1>Ox00FO0D00</td><td rowspan=1 colspan=1>OxAAC7</td><td rowspan=1 colspan=1>default</td><td rowspan=1 colspan=1></td></tr><tr><td rowspan=1 colspan=1>STM32H523/533</td><td rowspan=1 colspan=1>Ox00FO0D00</td><td rowspan=1 colspan=1>0xAAC7</td><td rowspan=1 colspan=1>default</td><td rowspan=1 colspan=1>-</td></tr><tr><td rowspan=1 colspan=1>STM32H563/573/562</td><td rowspan=1 colspan=1>Ox00F00E00</td><td rowspan=1 colspan=1>0x6A91</td><td rowspan=1 colspan=1>0x3AF66</td><td rowspan=1 colspan=1>Yes</td></tr><tr><td rowspan=1 colspan=1>STM32WBA52</td><td rowspan=1 colspan=1>0x08F02F00</td><td rowspan=1 colspan=1>0x6688</td><td rowspan=1 colspan=1>0x0FFF</td><td rowspan=1 colspan=1>Yes</td></tr><tr><td rowspan=1 colspan=1>STM32MP13xA/13xC/13xD/13xF</td><td rowspan=1 colspan=1>0x00F00D00</td><td rowspan=1 colspan=1>0x668A</td><td rowspan=1 colspan=1>0x2B5BB</td><td rowspan=1 colspan=1>Yes</td></tr><tr><td rowspan=1 colspan=1>STM32MP25x</td><td rowspan=1 colspan=1>0x08F00E00</td><td rowspan=1 colspan=1>0x6688</td><td rowspan=1 colspan=1>0x2E649</td><td rowspan=1 colspan=1>-</td></tr><tr><td rowspan=1 colspan=1>STM32U3</td><td rowspan=1 colspan=1>Ox00F00D00</td><td rowspan=1 colspan=1>OxAAC7</td><td rowspan=1 colspan=1>default</td><td rowspan=1 colspan=1>-</td></tr><tr><td rowspan=1 colspan=1>STM32N6</td><td rowspan=1 colspan=1>0x00F00D00</td><td rowspan=1 colspan=1>OxAAC7</td><td rowspan=1 colspan=1>default</td><td rowspan=1 colspan=1>-</td></tr></table>

l deviust  se ee he NIST e sui expt or heTM32LP/TM327A3/7Bn STM32H72x/73x.

2. the NIST SP800-90B test suite.

3. can be found in Table 4.

Table 4. NIST SP800-90B certificates   

<table><tr><td rowspan=1 colspan=1>Product</td><td rowspan=1 colspan=1>SP800-90B entropy source certificate</td><td rowspan=1 colspan=1>NIST public use document</td></tr><tr><td rowspan=1 colspan=1>STM32U575/585</td><td rowspan=1 colspan=1>#E11(1)</td><td rowspan=1 colspan=1>E11 public use(1)</td></tr><tr><td rowspan=1 colspan=1>STM32U5Fx/5Gx</td><td rowspan=1 colspan=1>#E116(1)</td><td rowspan=1 colspan=1>E116 public(1)</td></tr><tr><td rowspan=1 colspan=1>STM32U59x/5Ax</td><td rowspan=1 colspan=1>#E135(1)</td><td rowspan=1 colspan=1>E135 public(1)</td></tr><tr><td rowspan=1 colspan=1>STM32U535x/545x</td><td rowspan=1 colspan=1>#E158</td><td rowspan=1 colspan=1>E158 public(1)</td></tr><tr><td rowspan=1 colspan=1>STM32H56x/573</td><td rowspan=1 colspan=1>#E163(1)</td><td rowspan=1 colspan=1>E163 public(1)</td></tr><tr><td rowspan=1 colspan=1>STM32MP13xA/13xC/13xD/13xF</td><td rowspan=1 colspan=1>#E53(1)</td><td rowspan=1 colspan=1>E53 public use(1)</td></tr><tr><td rowspan=1 colspan=1>STM32WBA5x</td><td rowspan=1 colspan=1>#E186(1)</td><td rowspan=1 colspan=1>E186 public(1)</td></tr></table>

1. change, move, or inactivation of the URL or the referenced material.

# Note:

Entropy results can be shared with customers when required.

# NIST SP800-90B test suite steps

# Step 1: random number generator

Connect the STM32 board to the workstation, via USB Type-A to Micro-B cable.

The STM32 RNG is run via the UART firmware in order to generate a random number as described in STM32 MCU side. Data are storeon he workstation usinga terminal emulation application such as uTTY eand open-source terminal emulator, serial console, and network file transfer application).

# 5.2.2

# Step 2: NIST statistical tests

The Makefile s used to compile he program s describe inhe readme mentione in NIST S0-ob tes suite side.

For non-lID tests, the user must follow the steps detailed below:

1Use the Makefile to compile the program: make non_iid

Run the program with

./ea_non_iid [-i|-c] [-a|-t] [-v] [-1 <index>,<samples> ] <file_name> [bits_per_symbol]

# where

-i indicates that data is unconditioned and returns an initial entropy estimate (default).   
-c indicates that data is conditioned.   
-a estimates the entropy for all data in the binary file (default).   
-t truncates the created bit-string representation of data to the first 1 Mbit.   
-l reads (at most) data samples after indexing into the file by \* bytes.   
-v verbosity flag for more output (optional, can be used multiple times)bits_per_symbol: numb er of bits per symbol. Each symbol is expected to fit within a single byte.

# Example:

/ea_non_iid ../bin/15.bin 1 -i -t -v

For restart tests, the user must follow the steps detailed below:

1Use the Makefile to compile the program: make restart.

Run the program with.

ea_restart [-i|-n] [-v] <file_name> [bits_per_symbol] <H_I>

# Where

[bits_per_symbol]: Must be between 1-8, inclusive.   
<H_I>: Initial entropy estimate.   
[-|-n]: '-i' for IID data, '-n' for non-IID data. Non-IID is the default.   
-v Optional verbosity flag for more output.

<file_name>: Must be relative path to a binary file contains the data that consists of 1000 r estarts, each with 1000 samples. The data is converted to rows and columns.

# Example:

./ea_restart It_res_1000x1000.bin 1 0.7695 -n -v

# .2.3

# Step 3: test report

The NiT statistical tests provide an analytical routine to facilitate the interpretation of the results:

For the non IID tests, the result for each IID test is provided and, at the end, the final min entropy. For the restart tests, we determine the Hr and Hc , the entropy estimates of the row and the column datasets, respectively. the final result of the restart tests is min (H_r, H_c, H_I).

# 6 Conclusion

Thi application notdescribeshemain guidelines an sepseriherandomness umbers generat y the STM32 microcontrollers RNG peripheral, using either NiST statistical test suite SP800-22rev1a, April 2010or SP800-90B, January 2018.

# Appendix A NIST SP800-22rev1a statistical test suite

The results are represented as a table with p rows and q columns, where:

p, the number of rows, corresponds to the number of statistical tests applied q, the number of columns (q = 13) is distributed as follows:

columns 1-10 correspond to the frequency of 10 Pvalues column 11 is the Pvalue that arises via the application of a chi-square test11 column 12 is the proportion of binary sequences that passed column 13 is the corresponding statistical test

The example below shows the first and last part of the test results. For more details, refer to the finalAnalysisReport file under sts-2.1.1\experiments\AlgorithmTesting.

Part 1   

<table><tr><td>RESULTS FOR THE UNIFORMITY OF P-VALUES AND THE PROPORTION OF PASSING</td></tr><tr><td>SEQUENCES</td></tr><tr><td>generator is &lt;data/ascii.bin&gt;</td></tr><tr><td>C1 C2 C3 C4 C5 C6 C7 C8 C9 C10 P-VALUE PROPORTION STATISTICAL TEST</td></tr><tr><td></td></tr><tr><td>0 1 2 1 1 1 1 0 1 0.911413 10/10 Frequency 2</td></tr><tr><td>1 1 0 1 3 0 2 1 1 0 0.534146 10/10 BlockFrequency</td></tr><tr><td>0 1 3 3 0 1 0 2 0 0 0.122325 10/10 CumulativeSums</td></tr><tr><td>3 1 0 1 1 1 0 1 0.739918 10/10 CumulativeSums</td></tr><tr><td>2 0 2 2 1 1 0 1 0 1 0.739918 10/10 Runs</td></tr><tr><td>0 1 1 0 3 1 1 1 0 2 0.534146 9/10 LongestRun</td></tr><tr><td>1 2 1 0 2 1 1 0 0 2 0.739918 10/10 Rank</td></tr><tr><td>3 0 1 2 1 1 0 1 0 1 0.534146 9/10 FFT</td></tr><tr><td>1 1 1 0 0 2 1 2 0 2 0.739918 10/10 NonOverlapping Template</td></tr><tr><td>1 1 0 0 1 1 1 3 0 2 0.534146 10/10 NonOverlapping Template</td></tr><tr><td>0 2 1 0 4 0 2 0 0 1 0.066882 10/10 NonOverlapping Template</td></tr><tr><td>0 0 0 1 1 3 0 2 1 2 0.350485 10/10 NonOverlappingTemplate</td></tr><tr><td></td></tr><tr><td>0 1 2 2 1 1 1 2 0 0 0.739918 10/10 NonOverlapping Template</td></tr><tr><td>2 2 1 0 2 0 1 1 1 0 0.739918 10/10 NonOverlapping Template</td></tr><tr><td>1 0 2 2 1 1 1 0 1 1 0.911413 10/10 NonOverlappingTemplate 0 0 1 1 0 0 2 3 1 2 0.350485 10/10 NonOverlapping Template</td></tr></table>

# Part 2

<table><tr><td></td><td>0 1 1 1 1 0 0 0 1 0</td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td>2 0 1 0 1 2 1 0 2 1 0.739918</td><td colspan="2"></td><td>10/10 OverlappingTemplate</td></tr><tr><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td>1 0 2 1 0 2 2 1 1 0 0.739918</td><td colspan="2">10/10</td><td>Universal</td></tr><tr><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td>1 1 0 0 2 0 2 3 1 0 0.350485</td><td colspan="2">10/10</td><td>ApproximateEntropy</td></tr><tr><td></td><td></td><td>1 1 0 0 2 0 0 0 0 1</td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td colspan="2">5/5</td><td>RandomExcursions RandomExcursions</td></tr><tr><td></td><td></td><td></td><td></td><td>0 1 1 1 0 0 0 0 1 1</td><td></td><td></td><td></td><td></td><td></td><td></td><td colspan="2">5/5 5/5</td><td>RandomExcursions</td></tr><tr><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td>0 0 0 0 0 1 1 0 2 1</td><td></td><td></td><td></td><td colspan="2">5/5</td><td>RandomExcursions</td></tr><tr><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td>1 0 0 0 3 0 0 0 1 0</td><td></td><td></td><td></td><td colspan="2">5/5</td><td>RandomExcursions</td></tr><tr><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td>0 0 0 1 1 0 0 1 1 1</td><td></td><td></td><td></td><td colspan="2">5/5</td><td>RandomExcursions</td></tr><tr><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td>1 0 1 1 0 2 0 0 0 0</td><td></td><td></td><td></td><td colspan="2">5/5</td><td>RandomExcursions</td></tr><tr><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td>1 0 0 0 1 1 1 0 1 0</td><td></td><td colspan="2">5/5</td><td>RandomExcursions</td></tr><tr><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td>2 1 0 1 1 0 0 0 0 0</td><td></td><td colspan="2">5/5</td><td>RandomExcursionsVariant</td></tr><tr><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td>2 1 0 0 1 1 0 0 0 0</td><td></td><td colspan="2">5/5</td><td>RandomExcursionsVariant</td></tr><tr><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td>1 1 0 2 1 0 0 0 0 0</td><td></td><td colspan="2">5/5</td><td>RandomExcursionsVariant</td></tr><tr><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td>1 2 0 1 1 0 0 0 0 0</td><td></td><td colspan="2">5/5</td><td>RandomExcursionsVariant</td></tr><tr><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td>1 1 1 1 0 0 0 1 0 0</td><td></td><td colspan="2">5/5</td><td>RandomExcursionsVariant</td></tr><tr><td>1 1 0 1 1 0 0 0 0 1</td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td colspan="2">5/5</td><td>RandomExcursionsVariant</td></tr><tr><td>0 1 0 2 1 0 0 0 0 1</td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td colspan="2">5/5</td><td>RandomExcursionsVariant</td></tr><tr><td>0 0 0 1 0 1 0 3 0 0</td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td colspan="2">5/5</td><td>RandomExcursionsVariant</td></tr><tr><td>0 0 0 0 0 0 2 1 1 1</td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td colspan="2">5/5</td><td>RandomExcursionsVariant</td></tr><tr><td>0 0 1 0 0 0 1 1 1 1</td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td colspan="2">5/5</td><td>RandomExcursionsVariant</td></tr><tr><td>0 0 0 1 0 0 2 0 2 0</td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td colspan="2">5/5</td><td>RandomExcursionsVariant</td></tr><tr><td>0 1 0 0 1 1 1 1 0 0</td><td></td><td></td><td>1 0 0 2 0 1 1 0 0 0</td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td colspan="2">5/5</td><td>RandomExcursionsVariant</td></tr><tr><td></td><td></td><td></td><td>1 0 0 0 2 1 0 0 0 1</td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td colspan="2">5/5 5/5</td><td>RandomExcursionsVariant</td></tr><tr><td></td><td></td><td></td><td>0 0 0 1 1 0 1 1 1 0</td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td colspan="2">5/5</td><td>RandomExcursionsVariant RandomExcursionsVariant</td></tr><tr><td>0 0 0 0 2 0 2 0 0 1</td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td>•</td><td colspan="2">5/5</td><td>RandomExcursionsVariant</td></tr><tr><td>0 0 1 0 1 2 1 0 0 0</td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td colspan="2">5/5</td><td></td></tr><tr><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td colspan="2">5/5</td><td>RandomExcursionsVariant RandomExcursionsVariant</td></tr><tr><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td>0 0 1 0 0 2 2 0 0 0</td><td></td><td></td><td>1 1 0 0 0 2 3 0 2 1 0.350485 10/10 Serial</td></table>

T al n a sample size of 10 binary sequences.

Temim pasa  e and excrsin arnt)  isiaty mple sequences.

Frelistruc  abilblAPLE rapvieedu of the documentation.

# Appendix B NIST SP800-90b statistical test suite

# This is an example of the execution of the non-lID tests

\$ ./ea_non_iid ../bin/15.bin 1 -i -t -v Opening file: '../bin/15.bin'   
Number¯of Binary Symbols: 1024000   
Symbol alphabet consists of 2 unique symbols   
Running non-IID tests...   
Running Most Common Value Estimate..   
MCV Estimate: mode = 530185, p-hat = 0.51775878906249995, p_u = 0.51903071907139675   
Most Common Value Estimate (bit string) = O.946108 / 1 bit(s)   
Running Entropic Statistic Estimates (bit strings only)...   
Collision Estimate: X-bar = 2.4954732991667945, sigma-hat = 0.49998011778222412, p = 0.557171 51750062044   
Collision Test Estimate (bit string) = O.843807 / 1 bit(s)   
Markov Estimate: P_0 = 0.4822412109375, P_1 = 0.51775878906249995, P_0,0 = 0.4861830567784631 3, P_0,1 = 0.51381694322153693, P_1,0 = 0.47857068759018079, P_1,1 =¯0.52142931240981927, p_m ax =¯6.2798397734367098e-37   
Markov Test Estimate (bit string) = 0.939536 / 1 bit(s)   
Compression Estimate: X-bar = 5.2113069751685934, sigma-hat = 1.0187463366852749, p = 0.03543 1813237513987   
Compression Test Estimate (bit string) = 0.803135 / 1 bit(s)   
Running Tuple Estimates... t-Tuple Estimate: t = 16, p-hat_max = 0.53187518804173173, p_u = 0 .53314533218239224   
LRS Estimate: u = 17, v = 38, P_{max,W} = 0.50423097749594759, p_u = 0.50550366496585808 T-Tuple Test Estimate (bit string) = O.907399 / 1 bit(s)   
LRS Test Estimate (bit string) = 0.984207 / 1 bit(s)   
Running Predictor Estimates...   
MultiMCw Prediction Estimate: N = 1023937, Pglobal' = 0.51634782805743162 (C = 527405) Plocal = 0.42674646958653317 (r = 21)   
Multi Most Common in Window (MultiMCw) Prediction Test Estimate (bit string) = 0.953585 / 1 b it(s)   
Lag Prediction Estimate: N = 1023999, Pglobal' = 0.50526439621655594 (C = 516087) Plocal = 0. 40830971576974662 (r = 20)   
Lag Prediction Test Estimate (bit string) = 0.984890 / 1 bit(s)   
MultiMMC Prediction Estimate: N = 1023998, Pglobal' = 0.51899462537798435 (C = 530147) Plocal = 0.42674521449187308 (r = 21)   
Multi Markov Model with Counting (MultiMC) Prediction Test Estimate (bit string) = 0.946208 / 1 bit(s)   
Lz78Y Prediction Estimate: N = 1023983, Pglobal' = 0.51899440603936897 (C = 530139) Plocal = 0.42674552311446512 (r = 21)   
Lz78Y Prediction Test Estimate (bit string) = 0.946209 / 1 bit(s)   
H_original: 1.000000   
H_bitstring: 0.803135   
min(H_original, 1 X H_bitstring): 0.803135

# This is an example of the execution of the restart tests.

\$ ./ea_restart It_res_1000x1000.bin 1 0.7695 -n -v   
Opening file: '/home/Desktop/It_restart_1000x1000_bins/It_res_1000x1000.bin'   
Loaded 1000000 samples made up of 2 distinct 1-bit-wide symbols.   
H_I: 0.769500   
ALPHA: 5.0251553006530614e-06, X_cutoff: 654   
X_max: 592   
Restart Sanity Check Passed...   
Running non-IID tests...   
Running Most Common Value Estimate...   
Literal MCV Estimate: mode = 524815, p-hat = 0.524815000000003, p_u = 0.52610132816195332 Most Common Value Estimate (Rows) = 0.926587 / 1 bit(s)   
Literal MCV Estimate: mode = 524815, p-hat = 0.5248150000000003, p_u = 0.52610132816195332 Most Common Value Estimate (Cols) = 0.926587 / 1 bit(s)   
Running Entropic Statistic Estimates (bit strings only)...   
Literal Collision Estimate: X-bar = 2.4939272870560187, sigma-hat = 0.49996374423442524, p 0.56366499259647185   
Collision Test Estimate (Rows) = 0.827090 / 1 bit(s)   
Literal Collision Estimate: X-bar = 2.4988330426351748, sigma-hat = 0.499926291763369, p 0.54001782688956723   
Collision Test Estimate (Cols) = 0.888921 / 1 bit(s)   
Literal Markov Estiate: P_0 = 0.5248150000000003, P_1 = 0.4751849999999997, P_0,0 = 0.5286 091289311472, P_0,1 = 0.4713908710688528, P_1,0 = 0.52062569446782725, P_1,1 = 0.479374305532 17275, p_max = 3.6149969304059282e-36   
Markov Test Estimate (Rows) = 0.919808 / 1 bit(s)   
Literal Markov Estimate: P_0 = 0.52481500000000003, P_1 = 0.47518499999999997, P_0,0 = 0.5249 0687194535213, P_0,1 = 0.47509312805464787, P_1,0 = 0.5247146368564598, P_1,1 = 0.47528536314 35402, p_max = 1.4806522327909964e-36   
Markov Test Estimate (Cols) = 0.929869 / 1 bit(s)   
Literal Compression Estimate: X-bar = 5.2053159685055412, sigma-hat = 1.0214276541597365, p 0.040397638399976898   
Compression Test Estimate (Rows) = 0.771598 / 1 bit(s)   
Literal Compression Estimate: X-bar = 5.2093623833151179, sigma-hat = 1.0198576801023285, p 0.037170466884093645   
Compression Test Estimate (Cols) = 0.791617 / 1 bit(s)   
Running Tuple Estimates...   
Literal t-Tuple Estimate: t = 16, p-hat_max = 0.54171776156680396, p_u = 0.54300118613085924 Literal LRS Estimate: u = 17, v = 38, p-hat = 0.50185202103932736, p_u = 0.50313992749997694 Literal t-Tuple Estimate: t = 16, p-hat_max = 0.53421514909068124, p_u = 0.535500045383837 Literal LRS Estimate: u = 17, v = 36, p-hat = 0.50196715258596614, p_u = 0.50325505791399572 T-Tuple Test Estimate (Rows) = 0.880973 / 1 bit(s)   
T-Tuple Test Estimate (Cols) = 0.901041 / 1 bit(s)   
LRS Test Estimate (Rows) = 0.990968 / 1 bit(s)   
LRS Test Estimate (Cols) = 0.990638 / 1 bit(s)   
Running Predictor Estimates...   
Literal MultiMCw Prediction Estimate: N = 999937, Pglobal' = 0.52385156519694509 (C = 522532) Plocal can't affect result (r = 21)   
Multi Most Common in Window (MultiMCW) Prediction Test Estimate (Rows) = 0.932770 / 1 bit(s) Literal MultiMCw Prediction Estimate: N = 999937, Pglobal' = 0.52391856160939276 (C = 522599) Plocal can't affect result (r = 22)   
Multi Most Common in Window (MultiMCw) Prediction Test Estimate (Cols) = 0.932586 / 1 bit(s) Literal Lag Prediction Estimate: N = 999999, Pglobal' = 0.50560437226186183 (C = 504316) Ploc al can't affect result (r = 20)   
Lag Prediction Test Estimate (Rows) = 0.983919 / 1 bit(s)   
Literal Lag Prediction Estimate: N = 999999, Pglobal' = 0.50229941431576741 (C = 501011) Ploc al can't affect result (r = 19)   
Lag Prediction Test Estimate (Cols) = 0.993381 / 1 bit(s)   
Literal MultiMMC Prediction Estimate: N = 99998, Pglobal' = 0.52608038171682492 (C = 524793) Plocal can't affect result (r = 21)   
Multi Markov Model with Counting (MultiMMC) Prediction Test Estimate (Rows) = 0.926645 / 1 bi t(s)   
Literal MultiMMC Prediction Estimate: N = 9998, Pglobal' = 0.5260743824720614 (C = 524787) Plocal can't affect result (r = 22)   
Multi Markov Model with Counting (MultiMMC) Prediction Test Estimate (Cols) = 0.926661 / 1 bi t(s)   
Literal LZ78Y Prediction Estimate: N = 99983, Pglobal' = 0.52609326184739169 (C = 524798) Pl ocal can't affect result (r = 21)   
LZ78Y Prediction Test Estimate (Rows) = 0.926610 / 1 bit(s)   
Literal LZ78Y Prediction Estimate: N = 99983, Pglobal' = 0.52608626262396685 (C = 524791) Pl ocal can't affect result (r = 22)   
Lz78Y Prediction Test Estimate (Cols) = 0.926629 / 1 bit(s)   
H_r: 0.771598   
H_c: 0.791617   
H_I: 0.769500   
Validation Test Passed...   
min(H_r, H_c, H_I): 0.769500

# Revision history

Table 5. Document revision history   

<table><tr><td>Date</td><td>Version</td><td>Changes</td></tr><tr><td>13-May-2013</td><td>Initial release. 1</td><td></td></tr><tr><td rowspan="7">22-Jun-2016</td><td rowspan="7"></td><td>Updated: Introduction.</td></tr><tr><td>Section 1: STM32 microcontrollers random number generator.</td></tr><tr><td>Figure 1: Block diagram.</td></tr><tr><td>Section 3.1: Firmware description.</td></tr><tr><td></td></tr><tr><td>Section 3.2.1: First step: random number generator.</td></tr><tr><td>Section 3.2.2: Second step: NIST statistical test. Section 4: Conclusion.</td></tr><tr><td>1-Oct-2019</td><td></td><td>Added Figure 2: STM32 lines embedding the RNG hardware peripheral. Updated:</td></tr><tr><td></td><td></td><td>Introduction and Table 1: Applicable products Table 2: STM32 lines embedding the RNG hardware peripheral Figure 1: STM32 true RNG block diagram</td></tr><tr><td></td><td>3 Added:</td><td>Section 6: Conclusion Appendix A: NIST SP800-22b statistical test suite</td></tr><tr><td></td><td></td><td>Section 4: NIST SP800-90b test suite Section 5: NIST SP800-90b test suite running and analyzing</td></tr><tr><td>10-Oct-2019</td><td></td><td>Appendix B: NIST SP800-90b statistical test suite</td></tr><tr><td></td><td>4 Updated:</td><td>Updated Table 2: STM32 lines embedding the RNG hardware peripheral.</td></tr><tr><td>8-Jan-2020</td><td>5</td><td>Table 1: Applicable products</td></tr><tr><td></td><td></td><td>Table 2: STM32 lines embedding the RNG hardware peripheral Section 5.1.1: STM32 MCU side</td></tr><tr><td>18-Aug-2020</td><td>6</td><td>Updated with new products STM32H72x/73x: Table 1: Applicable products Table 2: STM32 lines embedding the RNG hardware peripheral</td></tr><tr><td>25-Aug-2021</td><td>6 Updated:</td><td>Migration to DITA</td></tr><tr><td>1-Jul-2022</td><td>7</td><td>Table 1: Applicable products NIST SP800-22rev1a test suite NIST SP800-90b test suite</td></tr><tr><td>09-Mar-2023</td><td></td><td>Firmware description used for RNG NIST evaluation Updated the following elements to add STM32H5 and STM32WBA series: Table 1. Applicable products.</td></tr><tr><td></td><td>8</td><td>Table 2. STM32 lines embedding the RNG hardware peripheral. Section 5.1.3: NIST compliant RNG configuration. Updated the document title. Applied minor changes to the whole document.</td></tr><tr><td></td><td>Updated:</td><td></td></tr><tr><td></td><td>Figure 2. STM32 true RNG block diagram of the products verified with the SP800-90b. Table 3. RNG register values.</td><td>Table 2. STM32 lines embedding the RNG hardware peripheral.</td></tr><tr><td>10-Jan-2024</td><td>9</td><td>Document title. Table 1. Applicable products.</td></tr><tr><td colspan="1" rowspan="1">Date</td><td colspan="1" rowspan="1">Version</td><td colspan="1" rowspan="2">ChangesAdded STM32U0 series and STM32H7R3/7S3 and STM32H7R7/7S7 lines inTable 1. Applicable productsUpdated:Table 3. RNG register valuesTable 4. NIST SP800-90B certificates</td></tr><tr><td colspan="1" rowspan="1">14-Mar-2024</td><td colspan="1" rowspan="1">10</td></tr><tr><td colspan="1" rowspan="1">21-Oct-2024</td><td colspan="1" rowspan="1">11</td><td colspan="1" rowspan="1">Added STM32MP2 series in Table 1. Applicable productsUpdated:•    Table 2. STM32 lines embedding the RNG hardware peripheralTable 3. RNG register valuesTable 4. NIST SP800-90B certificates</td></tr><tr><td colspan="1" rowspan="1">07-Feb-2025</td><td colspan="1" rowspan="1">12</td><td colspan="1" rowspan="1">Added STM32N6 series and STM32U3 series in Table 1. Applicable productsUpdated:Table 2. STM32 lines embedding the RNG hardware peripheralTable 3. RNG register valuesTable 4. NIST SP800-90B certificates</td></tr></table>

# Contents

# 1 STM32 MCU RNG •

1.1 RNG overview 2   
1.2 STM32 MCU implementation description.

# NIST SP800-22rev1a test suite 4

2.1 NIST SP800 22rev1a overview   
2.2 NIST SP800-22rev1a test suite description.

# NIST SP800-22rev1a test suite running and analyzing 6

3.1 Firmware description 6

3.1.1 STM32MCU side. 6   
3.1.2 On the NIST SP800-22rev1a test suite side 6

# 3.2 NISTSP800-22rev1a test suite steps

3.2.1 Step1: random number generator   
3.2.2 Step 2: NIST statistical test .   
3.2.3 Step 3: test report. 12

# NIST SP800-90b test suite. 13

4.1 Cryptographic random bit overview. . 13   
4.2 NIST SP800 90b test suite validation steps. 13

# Firmware description used for RNG NIST evaluation 14

# 5.1 STM32 MCU side 14

5.1.1 Data collection description 14   
5.1.2 STM32 firmware description 14   
5.1.3 NIST compliant RNG configuration 17

5.2 NIST SP800-90B test suite steps 18

5.2.1 Step 1: random number generator 18   
5.2.2 Step 2: NIST statistical tests 18   
5.2.3 Step 3: test report. 18

# 3 Conclusion .19

# Appendix A NIST SP800-22rev1a statistical test suite . 20

Appendix B NIST SP800-90b statistical test suite 22

Revision history 24

# _ist of tables .27

List of figures. .28

# List of tables

Table 1. Applicable products   
Table 2. STM32 lines embedding the RNG hardware peripheral 2   
Table 3. RNG register values. 17   
Table 4. NIST SP800-90B certificates 17   
Table 5. Document revision history 24

# List of figures

Figure 1. STM32 true RNG block diagram of the products verified with the SP800-22rev1a 3   
Figure 2. STM32 true RNG block diagram of the products verified with the SP800-90b 3   
Figure 3. Block diagram of deviation testing of a binary sequence from randomness based on NIST test suite 7   
Figure 4. Main sts-2.1.1 screen 8   
Figure 5. File input screen 8   
Figure 6. Statistical test screen. 9   
Figure 7. Parameter adjustment screen. 9   
Figure 8. Bitstream input . 10   
Figure 9. Input file format. 10   
Figure 10. Statistical testing in progress 11   
Figure 11. Statistical testing complete. 11   
Figure 12. Main function in interrupt mode. 15   
Figure 13. ISR callback function when DRDY interrupt flag is set 16   
Figure 14. ISR callback function when Error-flag 16

# IMPORTANT NOTICE  READ CAREFULLY

pt old ursant  dits   leole.

purchasers' products.

No license, express or implied, to any intellectual property right is granted by ST herein.

are the property of their respective owners.

I

© 2025 STMicroelectronics - All rights reserved