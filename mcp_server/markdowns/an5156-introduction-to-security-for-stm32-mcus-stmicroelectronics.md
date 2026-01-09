# Introduction to security for STM32 MCUs

# Introduction

This application note presents the basics of security in STM32 microcontrollers.

rivate data in the device, and guarantee of a service execution.

a t encryption.

I attackers exploit the different vulnerabilities in an embedded system.

Table 1. Applicable products   

<table><tr><td>Type</td><td>Product series</td></tr><tr><td>Microcontrollers</td><td>STM32C0, STM32F0, STM32F1, STM32F2, STM32F3, STM32F4, STM32F7, STM32G0, STM32G4, STM32H5, STM32H7, STM32L0, STM32L1, STM32L4, STM32L4+, STM32L5, STM32N6, STM32U5, STM32U3, STM32UO, STM32WB, STM32WBA, STM32WB0, STM32WL.</td></tr></table>

# 1 General information

# Note:

This document applies to STM32 Arm® Cortex®-core based microcontrollers.   
Arm is a registered trademark of Arm limited (or its subsidiaries) in the US and/or elsewhere.

The table below presents a nonexhaustive listof the acronyms used in this document and ther definitions.

Table 2. Glossary   

<table><tr><td colspan="2" rowspan="2">Term                                                     Definition</td></tr><tr><td colspan="1" rowspan="1">Term</td></tr><tr><td colspan="1" rowspan="1">AES</td><td colspan="1" rowspan="1">Advanced encryption standard</td></tr><tr><td colspan="1" rowspan="1">CCM</td><td colspan="1" rowspan="1">Core-coupled memory (SRAM)</td></tr><tr><td colspan="1" rowspan="1">CPU</td><td colspan="1" rowspan="1">Central processing unit-core of the microcontroller</td></tr><tr><td colspan="1" rowspan="1">CSS</td><td colspan="1" rowspan="1">Clock security system</td></tr><tr><td colspan="1" rowspan="1">Dos</td><td colspan="1" rowspan="1">Denial of service (attack)</td></tr><tr><td colspan="1" rowspan="1">DRNG</td><td colspan="1" rowspan="1">Deterministic random number generator: generates pseudo-random number from input value</td></tr><tr><td colspan="1" rowspan="1">DPA</td><td colspan="1" rowspan="1">Differential power analysis</td></tr><tr><td colspan="1" rowspan="1">ECC</td><td colspan="1" rowspan="1">Error code correction</td></tr><tr><td colspan="1" rowspan="1">FIA</td><td colspan="1" rowspan="1">Fault injection attack</td></tr><tr><td colspan="1" rowspan="1">FIB</td><td colspan="1" rowspan="1">Focused ion beam</td></tr><tr><td colspan="1" rowspan="1">GTZC</td><td colspan="1" rowspan="1">Global TrustZone® controller</td></tr><tr><td colspan="1" rowspan="1">HDP</td><td colspan="1" rowspan="1">Secure hide protection</td></tr><tr><td colspan="1" rowspan="1">HUK</td><td colspan="1" rowspan="1">Hardware unique key</td></tr><tr><td colspan="1" rowspan="1">IAP</td><td colspan="1" rowspan="1">In-application programming</td></tr><tr><td colspan="1" rowspan="1">IAT</td><td colspan="1" rowspan="1">Initial attestation token</td></tr><tr><td colspan="1" rowspan="1">loT</td><td colspan="1" rowspan="1">Internet of things</td></tr><tr><td colspan="1" rowspan="1">IV</td><td colspan="1" rowspan="1">Initialization vector (cryptographic algorithms</td></tr><tr><td colspan="1" rowspan="1">IWDG</td><td colspan="1" rowspan="1">Independent watchdog</td></tr><tr><td colspan="1" rowspan="1">MAC</td><td colspan="1" rowspan="1">Message authentication code</td></tr><tr><td colspan="1" rowspan="1">MCU</td><td colspan="1" rowspan="1">Microcontroller unit (ST32 Arm® Cortex® based devies</td></tr><tr><td colspan="1" rowspan="1">MPCBB</td><td colspan="1" rowspan="1">Memory protection block-based controller</td></tr><tr><td colspan="1" rowspan="1">MPCWM</td><td colspan="1" rowspan="1">Memory protection watermark-based controller</td></tr><tr><td colspan="1" rowspan="1">MPU</td><td colspan="1" rowspan="1">Memory protection unit</td></tr><tr><td colspan="1" rowspan="1">NSC</td><td colspan="1" rowspan="1">Nonsecure callable</td></tr><tr><td colspan="1" rowspan="1">NVM</td><td colspan="1" rowspan="1">Nonvolatile memory</td></tr><tr><td colspan="1" rowspan="1">OTFDEC</td><td colspan="1" rowspan="1">On-the-fly decryption</td></tr><tr><td colspan="1" rowspan="1">OTP</td><td colspan="1" rowspan="1">One-time programmable</td></tr><tr><td colspan="1" rowspan="1">PCROP</td><td colspan="1" rowspan="1">Proprietary code readout protection</td></tr><tr><td colspan="1" rowspan="1">PKA</td><td colspan="1" rowspan="1">Public key algorithm (also named aka asymmetric algorithm)</td></tr><tr><td colspan="1" rowspan="1">PSA</td><td colspan="1" rowspan="1">Platform security architecture</td></tr><tr><td colspan="1" rowspan="1">PVD</td><td colspan="1" rowspan="1">Programmable voltage detector</td></tr><tr><td colspan="1" rowspan="1"></td><td></td></tr><tr><td colspan="1" rowspan="1">Term</td><td colspan="1" rowspan="1">Definition</td></tr><tr><td colspan="1" rowspan="1">PWR</td><td colspan="1" rowspan="1">Power control</td></tr><tr><td colspan="1" rowspan="1">ROM</td><td colspan="1" rowspan="1">Read only memory—system flash memory in STM32</td></tr><tr><td colspan="1" rowspan="1">RoT</td><td colspan="1" rowspan="1">Root of trust</td></tr><tr><td colspan="1" rowspan="1">RDP</td><td colspan="1" rowspan="1">Read protection</td></tr><tr><td colspan="1" rowspan="1">RIF</td><td colspan="1" rowspan="1">Resource isolation framework</td></tr><tr><td colspan="1" rowspan="1">RSS</td><td colspan="1" rowspan="1">Root secure services</td></tr><tr><td colspan="1" rowspan="1">RTC</td><td colspan="1" rowspan="1">Real-time clock</td></tr><tr><td colspan="1" rowspan="1">SAU</td><td colspan="1" rowspan="1">Security attribution unit</td></tr><tr><td colspan="1" rowspan="1">SB</td><td colspan="1" rowspan="1">Secure boot</td></tr><tr><td colspan="1" rowspan="1">SCA</td><td colspan="1" rowspan="1">Side channel attack</td></tr><tr><td colspan="1" rowspan="1">SDRAM</td><td colspan="1" rowspan="1">Synchronous dynamic random access memory</td></tr><tr><td colspan="1" rowspan="1">SECDED</td><td colspan="1" rowspan="1">ECC mode of operation: single error correct, double error detect</td></tr><tr><td colspan="1" rowspan="1">SFI</td><td colspan="1" rowspan="1">Secure firmware installation</td></tr><tr><td colspan="1" rowspan="1">SFU</td><td colspan="1" rowspan="1">Secure firmware update</td></tr><tr><td colspan="1" rowspan="1">SPA</td><td colspan="1" rowspan="1">Simple power analysis</td></tr><tr><td colspan="1" rowspan="1">SPE</td><td colspan="1" rowspan="1">Secure processing environment</td></tr><tr><td colspan="1" rowspan="1">SRAM</td><td colspan="1" rowspan="1">Static random access memory (volatile)</td></tr><tr><td colspan="1" rowspan="1">SST</td><td colspan="1" rowspan="1">Secure storage</td></tr><tr><td colspan="1" rowspan="1">STSAFE</td><td colspan="1" rowspan="1">Secure element product from STMicroelectronics portfolio</td></tr><tr><td colspan="1" rowspan="1">SWD</td><td colspan="1" rowspan="1">Serial-wire debug</td></tr><tr><td colspan="1" rowspan="1">TF-M</td><td colspan="1" rowspan="1">Trusted firmware-M</td></tr><tr><td colspan="1" rowspan="1">WRP</td><td colspan="1" rowspan="1">Write protection</td></tr></table>

# Documentation references

Tll memory protections implementation.

A programming manual is also available for each Arm® Cortex® version and can be used for an MPU (memory protection unit) description:

STM32 Cortex®-M33 MCUs programming manual (PM0264)   
STM32F7 series and STM32H7 series Cortex®-M7 processor programming manual (PM0253)   
STM32 Cortex®-M4 MCUs and MPUs programming manual (PM0214)   
STM32F10xxx/20xxx/21xxx/L1xxx Cortex®-M3 programming manual (PM0056)   
Cortex®-MO+ programming manual for STM32L0, STM32G0, STM32WL, STM32WB, and STM32WB0   
series (PM0223)

Refr o thefollowing et fuermanuals and application notes availableonwwst.com) ordetiled description of security features:

<table><tr><td rowspan=1 colspan=1>Ref.</td><td rowspan=1 colspan=1>Docnumber</td><td rowspan=1 colspan=1>Title</td><td rowspan=1 colspan=1>Comment</td></tr><tr><td rowspan=1 colspan=1>[1]</td><td rowspan=1 colspan=1>AN4246</td><td rowspan=1 colspan=1>Proprietary code readout protection onSTM32L1 series MCUs</td><td rowspan=4 colspan=1>Explains how to set up and work with PCROP firmware for thespecified MCUs, provided with the X-CUBE-PCROP expansionpackage.</td></tr><tr><td rowspan=1 colspan=1>[2]</td><td rowspan=1 colspan=1>AN4701</td><td rowspan=1 colspan=1>Proprietary code readout protection onSTM32F4 series MCUs</td></tr><tr><td rowspan=1 colspan=1>[3]</td><td rowspan=1 colspan=1>AN4758</td><td rowspan=1 colspan=1>Proprietary code readout protection onSTM32L4, STM32L4+, STM32G4,and STM32WB series MCUs</td></tr><tr><td rowspan=1 colspan=1>[4]</td><td rowspan=1 colspan=1>AN4968</td><td rowspan=1 colspan=1>Proprietary code readout protection onSTM32F72/F73xx MCUs</td></tr><tr><td rowspan=1 colspan=1>[5]</td><td rowspan=1 colspan=1>AN4838</td><td rowspan=1 colspan=1>Managing memory protection unit(MPU) in STM32 MCUs</td><td rowspan=1 colspan=1>Describes how to manage the MPU in the STM32 products.</td></tr><tr><td rowspan=1 colspan=1>[6]</td><td rowspan=1 colspan=1>AN5185</td><td rowspan=1 colspan=1>STMicroelectronics firmware upgradeservices for STM32WB series</td><td rowspan=1 colspan=1></td></tr><tr><td rowspan=1 colspan=1>[7]</td><td rowspan=1 colspan=1>AN5447</td><td rowspan=1 colspan=1>Overview of secure boot and securefirmware update solution on Arm®TrustZone® STM32 MCUs</td><td rowspan=1 colspan=1></td></tr><tr><td rowspan=1 colspan=1>[8]</td><td rowspan=1 colspan=1>UM1924</td><td rowspan=1 colspan=1>Legacy STM32 crypto library</td><td rowspan=1 colspan=1>Describes the API of the STM32 crypto library; provided with theX-CUBE-CRYPTOLIB expansion package.</td></tr><tr><td rowspan=1 colspan=1>[9]</td><td rowspan=1 colspan=1>UM2262</td><td rowspan=1 colspan=1>Getting started with the X-CUBE-SBSFU STM32Cube expansionpackage</td><td rowspan=1 colspan=1>Presents the SB (secure boot) and SFU (secure firmware update)STMicroelectronics solutions; provided with the X-CUBE-SBSFUexpansion package.</td></tr><tr><td rowspan=1 colspan=1>[10]</td><td rowspan=1 colspan=1>AN4730</td><td rowspan=1 colspan=1>Using the firewall embedded inSTM32L0/L4/L4+ series MCUs</td><td rowspan=1 colspan=1>Describes how to access securely sensitive parts of code anddata</td></tr></table>

The  wiki also offers vastresources n securitytopics, icuding detaile step-by-steguidesontt:/ wiki.st.com/stm32mcu/wiki/Category:Security

# 2 Overview

# 2.1

# Security purpos

# Why protection is needed

Seurit inmicocontrollersmean protectigbedeware dat, and he yte unctinaliy.Thene for data protection is greatest in the case of cryptographic keys or personal data.

T l sotware, it makes sense to attest that the code is authentic, and not replaced by malicious firmware.

Denial-of-service attack (DoS attack) is another major threat when considering protection systems (such as ll robust and reliable.

Thereqment  curity must ot erestiat ve s moe cplexiy estT, systems built around microcontrollers become potential targetsormore and more skil attackers who epect e.votey  pakettmp

In arviven rCvi forhackers becausehe motely ccsible.Teoectivityffr anglettack throh o entire network (see the figure below).

![](images/5756157c7658a1f9aa710a002f9369049532ea2bf49222afb14017605020a8e3.jpg)  
Figure 1. Corrupted connected device threat

# What must be protected

Both the attacks and the protection mechanisms often do not make difference. However t isstll usful to summarize the assets and risks.

The table below presents a non-exhaustive list of assets targeted by attackers.

Table 3. Assets to be protected   

<table><tr><td rowspan=1 colspan=1>Target</td><td rowspan=1 colspan=1>Assets</td><td rowspan=1 colspan=1>Risks</td></tr><tr><td rowspan=1 colspan=1>Data</td><td rowspan=1 colspan=1>Sensor data (such as healthcare data or log of positions)User data (such as ID, PIN, password or accounts)Transactions logsCryptographic keys</td><td rowspan=1 colspan=1>Unauthorized sale of personal dataUsurpationSpyingBlackmail</td></tr><tr><td rowspan=1 colspan=1>Control of device (bootloader,malicious application)</td><td rowspan=1 colspan=1>Device correct functionalityDevice/user identity</td><td rowspan=1 colspan=1>Denial of serviceAttacks on service providersFraudulent access to service (cloud)</td></tr><tr><td rowspan=1 colspan=1>User code</td><td rowspan=1 colspan=1>Device hardware architecture/designSoftware patent/architectureTechnology patents</td><td rowspan=1 colspan=1>Device counterfeitSoftware counterfeitSoftware modificationAccess to secure areas</td></tr></table>

# Vulnerability, threat, and attack

nvl inattacknvvmatt tyes reSectcyoh ones to the most advanced ones.

The following specific wording is used around security:

asset: what needs to be protected threat: what the device/user need to be protected against vulnerability: weakness or gap in a protection mechanism

Inzplbl

# 3 Attack types

Thi t coeyhaveo oto very sophisticated and expensive ones.The last part presents typical examples  attacks targeting an loT system.

Attacks on microcontroller are classified in one of the following types:

software attack: exploits software vulnerabilities (such as bug or protocol weaknesses). hardware non-invasive attack: focuses on MCU interfaces and environment information. hardware invasive attack: destructive attack with direct access to silicon

# 3.1

# Introduction to attack types

A key rule in security is that a successful attack is always possible.

Fi, theosolutprotecnagaisepecattckWhateverhe ecuriyeasuake makes it necessary to consider how the device firmware is updated to increase its security (see Section 5.3.2: Secure firmware update (SFU)).

itsdesign architecture details. These techniques are briely presented in Section 3. Hardware attacks.

Fr  ats psiblThe revenue depends on the stolen asset valan on he epeatabily  the ttackThe cost depends on time, the acquisition of the necessary skils by the attacker, and on money (equipment) sent to succeed.

# Attack types

While there emoredetaild groups and categorisattack, the basicategories ae heollowiges

Software attacks are carred by exploiting bugs, protocol weaknesses, or untrusted pieces of code among oters.Attacks on communication chanels interception or usurpation are partf this category.Soare attacks represent the vast majority of cases. Their cost may be very low. They can be widely spread and repeated with hugedamage. Iis not necessary to have a physical acces tothe devic.Theattack can be executed remotely.

Hardware attacks need physical access to the device.The mostobvious one exploits the debug port, is not protected. However, in general, hardware attacks are sophisticated and can be very expensive. They ar carred out with specific materials and require electronics engineering skills. A distinction is made between noninvasive attacks (carrid out at board or hip level without devicedestruction), and invasive ats (arrut t devision level wi package etuctin). In most cass,su an attck profitable if it reveals information that leads to a new and widely applicable remote attack.

The table below gives an overview of the cost and techniques used for each type of attack.

Table 4. Attacks types and costs   

<table><tr><td rowspan=1 colspan=1>Attackstypes</td><td rowspan=1 colspan=1>Non-invasive</td><td rowspan=2 colspan=2>Non-invasive                       Semi-invasive                           Invasivewogeduu       Square</td></tr><tr><td rowspan=1 colspan=1></td><td></td></tr><tr><td rowspan=1 colspan=1>Scope</td><td rowspan=1 colspan=1>Remote or local</td><td rowspan=1 colspan=1>Local board and device level</td><td rowspan=1 colspan=1>Local device level</td></tr><tr><td rowspan=1 colspan=1>Techniques</td><td rowspan=1 colspan=1>Software bugsProtocol weaknessesTrojan horseEavesdropping</td><td rowspan=1 colspan=1>Debug portPower glitchesFault injectionSide-channels analysis</td><td rowspan=1 colspan=1>ProbingLaserFIBReverse engineering</td></tr><tr><td rowspan=1 colspan=1>Cost/expertise</td><td rowspan=1 colspan=1>From very low to high,depending on the securityfailure targeted</td><td rowspan=1 colspan=1>Quite low cost. Need only moderatelysophisticated equipment and knowledge toimplement.</td><td rowspan=1 colspan=1>Very expensive. Need dedicatedequipment and very specific skills.</td></tr><tr><td rowspan=1 colspan=1>Objectives</td><td rowspan=1 colspan=1>Access to confidential assets(code and data).UsurpationDenial of service</td><td rowspan=1 colspan=1>Access to secret data or device internalbehavior (algorithm).</td><td rowspan=1 colspan=1>Reverse engineering of the device(silicon intellectual property)Access to hidden hardware andsoftware secrets (flash memoryaccess)</td></tr></table>

# 3.2

# Software attacks

Soae attacks ae carriout  the system by executing a pi cdname a malware, y he CPU. Tema akesontrol hedeviore yeohe ysteu I RAM, and flash memory content or peripheral registers), or to modify its functionality.

This type of attack represents most of device threats for the following reasons:

The attack cost is low since it does not need specific equipment but a personal computer. Ma hackers an put theeforttgetheargheeperi  tricksthat  ssul at likely to happen  a security breach exists. Furthermore, in case of success, the attack protocol may spread very quickly through the web

Themala an eneceintheevian ready rent nsierhreat)imaapl or a very small and easy to hide.

Here are examples of what a malware can do:

Modify device configuration (such as option bytes or memory attributes).   
Disable protections.   
Read memory and dump its content for firmware and data cloning.   
Trace or log device data.   
Access to cryptographic items.   
Open communication channel/interface.   
Modify or block the device functionality.

Unetslaei world, software attacks must be considered.

# Malware injection

Te ps Ta tareut ay ey all  yTeeu eamus nje nev meory (RAM  fash memory. Onceinjec the hallenges ohav execut by he , whic means that the PC (program counter) must branch to it.

Methods of injecting malware can be categorized as follows:

basics device access/"open doors":

Debug port: JTAG or SWD interface   
Bootloader: if accessible, can be used to read/write memory content through any available interface. Execution from external memory

These malware injections are easy to counter with simple hardware mechanisms that are described in Section 4: Device protections .

Application download:

Firmware update procedure: a malware can be transferred instead of a new FW. OS with capability to download new applications

This category countermeasure is based on authentication between the device and the server or directly with code authentication. Authentication relies on cryptography algorithms.

Weaknesses of communication ports and bugs exploitation:

Execution of data. Sometimes it is possible to sneak the malware in as data, and to exploit incorrect boundary check to execute it.   
Stack-based buffer overflows, heap-based buffer overflows, jump-to-libc attacks, and data-nly attacks

This third category is by definition difficult to circumvent. Most embedded system applications are coded using low-level languages such as C/C++. These languages are considered unsafe because they can lead to memory management errors leveraged by attackers (such as stack, heap, or buffers overflow). The general idea is to reduce as much as possible what is called the attack surface, by minimizing the untrusteornveri par  fwarOnesolution consist olating the eecution and he ercs of the different processes. For example, the TF-M includes such a mechanism.

Use of untrusted libraries with device back door: This last categorys an intentionalmalware introduction that facilitatesdevicecorruption.Today, lo firmware developments rely on software shared on the web and complex ones can hide Trojan horses. As in prev ateoyhe wa ceeu harueaattc yola much as possible the process execution and protecting the critical code and data.

# Brute forcing

Tyc reetbasas evay qu uetication acesig rvi heco  ample unmachite exploited with an automatic process in order to try successive passwords exhaustively.

Interesting countermeasures are listed below:

Lm he  wi on pe w ese backup domain).   
Increase the delay between consecutive login attempts.   
Add a challenge-response mechanism to break automatic trials.

# 3 Hardware attacks

Hardware attacks require a physical access to the device or, often, to several devices in paralle

The two following types of attacks differ in cost, time, and necessary expertise:

Non-invasive attacks have only external access to the device (board-level attack) and are moderately expensive (thousands to tens of thousands US dollars in equipment).   
Invivttacks have ircaccessdeviilion tr e-packig).Tey cart wih adv equipment often found in specialized laboratories. They are very expensive (more than 100k dollars, and oin the rangemilons)and target very valuable data (Keys or IDs)or even the protection technoloy itself.

General-purpose microcontrollers are ot the best candidates to counter the most advanced physical attacks. If a highest protection level is required, consider pairing a secure element with the general-purpose molSctictollet atcrar specific hardware.

Refer to ST secure microcontrollers web page.

# 3.3.1 Non-invasive attacks

-y. Only accessible interfaces and device environment areused. These attacks requiremoderately sophisticated equipment and engineering skills (such as signal processing).

# Debug port access

T poeon vel onse. Inde asing debug porran harou JTAGrWD poollow acssing the fll internal reourcesfthe device:PU registersbeded fash memoryRAM and perheal registers.

Countermeasure:

Debug port deactivation or fuse through Readout protection (RDP) Life-cycle management using product state (where this technology succeeded the RDP)

# Serial port access

Acces to communication ports (such as 2Cor SPl) may hide a weakness that can be exploited. Communication por can be spd o use as a device enty point. Depending nhow the associatd protocol areplemented (such as memory address access range, targeted peripherals or read/write operations), an attacker can potentially gain access to the device resources.

Countermeasures:

Software:

Associated protocol operations must be limited by the firmware level, so that no sensitive resources can be read or written.   
Isolate communication stack from sensitive data.   
Length of data transfer must be checked to avoid buffer overflows.   
Communication can be encrypted with a shared key between the device and the target.

# Hardware:

Physical communication port can be buried in multi-layer boards to make it more difficult to access.   
Unused interface port must be deactivated.

# Fault injection: clock and power disturbance/glitch attacks

Fault injection consists in using the device outside the parameters defined in the datasheet to generate malfunctions in the system. A successful atack can modifythe program behaviorin different ways such as corptng programtaecouptinmemorycontent oppig proces eecution (stuckat fault sk instruction, modifying conditional jump or providing unauthorized access.

fult may be non-ntentional, countemeasures are the sameas thene used r safety: redundancy, detection and monitoring.

# Countermeasures:

Software:

Check function return values.   
Use strict comparisons when branching.   
Make sure that no code was skipped in critical parts by incrementing a dedicated variable in each branch with prime number and check for the expected value.   
Use non-trivial values as true and false (avoid comparing to 0 or -1, try complex values with high mutual Hamming distance).

# Hardware:

Use Clock security system (CSS) if available.   
Use internal clock sources.   
Use internal voltage regulators.   
Use memory error detection (ECC and parity).

# Side-channel attacks (SCA)

When a firmware is executed, an attacker can observe the device running characteristics (such as power consumption, electromagnetic radiations, temperature or activity tme). This observation can bring enough inomationrveece assetuatalundogorithsplementationSehanel attacks ae poweul agaist yptographicdevics iorder reveal he keys used byhe ystem.A iple a  al consumption.

Countermeasures:

Software:

Limit key usage: use session random keys when possible.   
Use protected cryptographic libraries with behavioral randomization (such as delays or fake instructions).

# Hardware:

Shields against monitoring can be found in secure elements (STSAFE), but there is usually no efficient hardware countermeasure embedded in general-purpose microcontrollers (except for the SAES in STM32H5, STM32N6, STM32H7S, STM32WBA, STM32U3 and STM32U5 devices, the hardware protection in limited in general-purpose microcontrollers.The protection level is reflected by the certification level achieved by the device. See Section 5.6: Product certifications for more details).

# 3.3.2

# Silicon invasive attack

The cost o such attacks is veryhigh; all means areconsidere to extract iforation of thedevice hat is estrure sTetcereaantl uanteviel Car tli il and knowledge, as well as time.

a psatnowvganivacn ieprobing or modification attacks.

v molledicatcurusegais neaense part of the STM32 family and are out of scope of this document. Refer to ST secure hardware platforms (www.st.com/en/secure-mcus.html).

# Reverse engineering

al task with modern devices featuring millions of gates.

evieyalz metal layers have been stripped off by etching the device.

# Reading the data

Wieahar to read the whole device memory.

# Micro probing and internal fault injection

l with it while the device is running.

# Device modification

Morsohisticated tools can e used to perorm attacks. F (ocse n beam) workstations,orexaple, simpliy themanual probing  deep metal and polysilicon lnes.They also can beused tomodiy he device structure by cutting existing or creating new interconnection lines and even new transistors.

# 3.4

# loT system attack examples

Th ection presnts typical examples o attacks on an o system.Fortunately, most  theseattacks an e ablcraasuplathic countermeasures). The countermeasures are detailed in the next sections.

An loT system is built around a STM32 microcontroller with connectivity systems (such as Ethernet, Wi-Fi® Bluoth® Low Energy r ,LoRa® and sensors and/or actuators see the figure below).The microcontrolle hanes heaplicationdata acquisition an communications wit a cou rviThemicrocontroller ls be responsible for the system maintenance through firmware update and integrity check.

![](images/2aa479e2d5a47d88c875534c187104150e893f636c9526e04484a01d24a01158.jpg)  
Figure 2. loT system

# 3.5

# List of attack targets

The following sections list the possible attack targets.

# Initial provisioning

wyWheekcrtfihas nl vamus ulen programmed inside the device, the data protection mechanism must be enabled and only authorized process must have access to it.

Risks: firmware corruption or usurpation

Countermeasures:

trusted manufacturer environment   
use of secure data provisioning services (SFI)   
data protection mechanisms   
secure application isolation   
use of OTP memory

# Boot modification

T bomod and/or he boot addressto preempt theuse aplication an to take contol f the U throh the be USB DFU, C P, e e por r eRAM.Teot the address are controlled by device configuration and/or input pin and must be protected.

Risks: full access of the microcontroller content

Countermeasures:

unique boot entry bootloader and debug disabled (see Section 6.2: Readout protection (RDP))

# Secure boot (SB) or Trusted Firmware-M (TF-M)

R root of trust of a device, this part of user firmware must be immutable and impossible to bypass.

As attcoiteuo-rustplatn ysieviaion  y I uuln beginning of this chapter).

Risks: device spoofing or application modification

Countermeasures:

unique boot entry point to avoid verification bypass   
"immutable code" to avoid SB code modification   
secure storage of firmware signature and/or tag value   
environment event detection (such as power supply glitch, temperature or clock speed)

# Firmware update

Teul ne snea t etusepnuvitHowve uaice enter the device with its own firmware or a corrupted version of the existing firmware.

T u u atte chapter).

Risk: device firmware corruption

Countermeasure: SFU application with authentication and integrity checks. Confidentiality can also be added by encrypting the firmware in addition to signature.

# Communication interfaces

Sel inteacs (such  SP, I2C USARTa sed ether y he botder  b pliatis exae data and/or commands with the device. The interception of a communication allows an attacker to use the interface as a device entry point. The firmware protocol can also be prone for bugs (like overflow).

Risk: Access to device content

Countermeasures:

Make physical bus hard to reach on board.   
Isolate software communication stacks to prevent them from accessing critical data and operations.   
Use cryptography for data exchange.   
Disable I/F ports when not needed.   
Check inputs carefully.

# Debug port

T  h SAnga This is the first breach tried by an attacker with physical access to the device.

D Risk: full access to the device

Countermeasure: Disable device debug capabilities see Section 6.Readout protection (RDP)).

# External peripheral access

An loT device controls sensors and actuators depending on theglobal application. An attacker can diver he system by modifying data coming from sensors or by shunting output data going to actuators.

Risk: incorrect system behavior. Countermeasure: anti-tamper to detect system intrusion at board level

# Sensitive firmware and data

S par e a esel protectio:examplehcyptographiagorithm thiry library. In additon, selected data may needehanced protection f they are considereas valuableassets (cryptographic keys).

The internal memory content must be protected against external accesses (such as communication interfaces) aint e Teett wale for process and data isolation.

Risks: sensitive firmware copy or data theft

Countermeasures:

execute-only access right (XO)   
firewall   
memory protection unit   
secure area   
encryption of external memory

# SRAM

The SRAM is the device running memory.I embeds runtime buffers and variables (such as stackor heap) and can embed fimware and keys While i the non-volatilmemory, the secrets may be stored as encrypted when l  hSRAM, they need o e preent in plainview be us In the sameme heSRAMusuall ol communication buffrs.For these two reasons, an atacker may be tempted to focus his effort on the SRAM. At lreeypetack caneraisagaist thismemory:code malwarinjectnmemoy cortin through buffer overflow and retrieval of secrets through temporary stored variables.

Risks: buffer overflow, data theft or device control

Countermeasures:

firewall   
memory protection unit   
Secure area

# Random number generation

apsnaphlizat generation. Weak random generator may make any secure protocol vulnerable.

a break intcomunication confientialityAhardwar attack attempts odisable theentropy sou weaken the statistic randomness of the output.

Arobs rando generatordepends on both the quality the entropy source analog) and the subsequent processing in digital.

Risk: reduced security of cryptographic protocols

Countermeasure:

Use true hardware entropy generator.   
Use tests on the RNG output, and verify statistic properties of produced random numbers.   
Take full advantage of the error detection and heath check mechanisms available on the device RNG.

# Communication stack

Connectivity protocols (such as Bluetooth, Ethernet, Wi-Fi or LoRa) have complex communication firmware stacks.These stacks, often available i open source, must not always be considered s trustd. A pontial weakness can be massively exploited.

Risk: device access (content, control) through network

Countermeasures:

communication process isolation server authentication secure firmware update to patch bugs

# Communication eavesdrop

Data exchanges between a device and an oservice can be eavesdropeitherdirectly by a copatible device orough heetwork.Anhacker may seek orretrieving dat gttg devi IDs osin vi.

Cryptography can be adopted by a communication protocols. Several encryption steps are often consider to protect the communication between all the different layers (device, gateway, applications).

Risk: observation and spoofing of network traffic

Countermeasure: use of cryptographic version of the communication stack (like TLS for Ethernet)

# 4 Device protections

Security protections described in this section are controlled by hardware mechanisms. They are set either by configuring the device through option bytes, or dynamically by hardware component settings:

• Memory protection: main security feature, used to protect code and data from internal (software) and external attacks Software isolation: inter-processes protection to avoid internal attacks Interface protection: used to protect device entry points like serial or debug ports System monitoring: detects device external tampering attempts or abnormal behaviors

# 4.1 Configuration protection

Aputolatl lBeul yry c  y  se are rules to determine the default value in case of OB corruption.

# Note:

M common examples are OxB4 or OxC3 for TRUE or FALSE.

Detals about rules tomodiy theoption bytes are detailed ineach referencemanual. The configuratinis generally frozen by raising the RDP level. Additional rules apply case-by-case.

In   etn BL n v R ust hegans ulaea   ak from damaged microcontroller.

Hit umbe  corruptptin byshoweveresuleorsn prorming. heOemodn controlled environment, the threat of unintentional device locked-up is very low.

# 4.2

# TrustZone® for Armv8-M architecture

Miontrollers base on Armv rArmv7 arhitecture Cortex-M0, M3, M4, and M7) rely mostly n sote iplementations orware  esurceolatinThemehanisdescribe aternedocen rut oapablolatiecuwaierainstfomnstallplicatis nonsecure firmware.

Th Armv8-M architecture brings a new security paradigm Ar microcontrollers. Itimplements theTrusto tenology atmirocontroller sstem level allowing the development truste mwar hrough arobust isolation at runtime.

The TrustZone® technology relieson a processor (Cortex-M23, Cortex-M55 or Cortex-M33) separation for ecure a nonsecuremains nd a bu rastructureAMBA®) propagating curetributehroghout hehole system (peripherals and memories).

TTusto derbus  fexilcrno nt  sec dmanand ievers  aighfoard with ew ce penalts.There is o need or Secuemonitrs TrustZone® for application processors Cortex-A.

Secure modes are orthogonal to the existing modes, Thread and Handler. Thus, there can be a Thread or Handler mode in each secure mode (see the figure below).

![](images/946bd7ddd39e4f2482d700217e0d04b8e19259e501ff6cb721f1cc40d4514766.jpg)  
Figure 3. Armv8-M TrustZone® execution modes

Onypil fwar rchitecturenign ArmTrustZone®, theonsecuredomai executes h pltn and the OS tasks, while the secure domain executes the secure application and the system root-of-trust mechanisms.

# 4.3 Dual-core architecture

In dual-core products, one core can act as secure while the other is nonsecure. Some products, memory and peripherals, ensuring that robust runtime isolation implementation is possible.

Adedicated security controller is added to the dual-core STM32WL devices to facilitate the isolation.

Intusigattriutonunits,he secure Vmemorydedicate osecurable s defie ihe as meory intea uratin. e perheral cshDM musconve he ecurcontext e user manual Getting started with STM32CubeWL for STM32WL series (UM2643) for details about this hybrid architecture).

![](images/ee0e8df7e1f6912c76087f8f8088d2077e0b2ffab95795ef4e93e07e7cd8408e.jpg)  
Figure 4. Simplified diagram of dual-core system architecture

# 4.4

# Memory protections

Storage containing sensitive code and data must not be accessible from any unexpected interface (debuging port) or an unauthorized process (internal threat).

Dedineasset  oec deavmehani anetabli prt tur eauha teal inteal po heemoyy (flash, SRAM, or external memory).

hide protection, PCROP, WRP, RDP, RIF, IDAU) can be found in Section 6: STM32 security features.

Embedded flash memory, embedded SRAM, and external memories are designed for dfferent purposes. Their respective protections mechanisms reflect these differences.

The figure below provides a simple view of memories access architecture in a microcontroller.

![](images/a3a0994ba9e3713180ea25bb62accaeb3896c4f4793ddd26950eabfa4a4e247d.jpg)  
Figure 5. Memory types

The table below summarizes the particularities of each type of memories and typical protection features.

Table 5. Memory types and associated protection   

<table><tr><td colspan="1" rowspan="1">Memory</td><td colspan="1" rowspan="1">Types</td><td colspan="1" rowspan="1">Description</td><td colspan="1" rowspan="1">Protections</td></tr><tr><td colspan="1" rowspan="1">System flashmemory</td><td colspan="1" rowspan="1">. Internal. NVM.ROM</td><td colspan="1" rowspan="1">ROM part of the flash memory. Embeds devicebootloader and other ST services.</td><td colspan="1" rowspan="1">Cannot be updated (erase/written).A part may also be unreadable.</td></tr><tr><td colspan="1" rowspan="1">User flash memory</td><td colspan="1" rowspan="1">. Internal. NVM</td><td colspan="1" rowspan="1">Flash memory for user application</td><td colspan="1" rowspan="1">Internal protections:RDPWRPTrustZone</td></tr><tr><td colspan="1" rowspan="1">SRAM</td><td colspan="1" rowspan="1">. Internal. Volatile</td><td colspan="1" rowspan="1">Working memory for Stack, heap or buffers.Can be used to execute the firmwaredownloaded from internal or external non-volatile memories.</td><td colspan="1" rowspan="1">•    PCROP (not for SRAM)OTP (not in SRAM)FirewallSecure hide protection (not for SRAM)MPU</td></tr><tr><td colspan="1" rowspan="1">NAND, NOR, Octo-or Quad-SPI flashmemory</td><td colspan="1" rowspan="1">. External. NVM</td><td colspan="1" rowspan="1">Additional memory for applications or datastorage</td><td colspan="1" rowspan="1">Cryptography (MCE, OTFDEC)Write protection (on Flash device)TrustZone</td></tr><tr><td colspan="1" rowspan="1">SDRAM</td><td colspan="1" rowspan="1">. External. Volatile</td><td colspan="1" rowspan="1">Additional RAM for application execution</td><td colspan="1" rowspan="1">Cryptography (MCE)</td></tr></table>

# 4.4.1

# System flash memory

In STM32 MCUs, the system memory is a read-nly part (ROM) of the embedd flash memory. It is dedicated to tco services (RS) in this area. This part cannot be modified to guarantee its authenticity and integrity. The bbl   S r are not accessible or execute only and cannot be read by the user.

The protection attribute on the system flash memory cannot be modified.

# 4.4.2 User flash memory

Th is heaisermeyuoendnonolata I parhebea memory, and can be protected by a set of memory protection features available on all STM32 MCUs.

# External attacks

T mo  o gaete attanieteaa iol from outside.

Associated protection: RDP to disable debug access

# Internal attacks

Aninternal read or writaccess  thememory can come fro amalware njecteeithern the deviRAMo ia . Associated protections: PCROP, MPU, firewall, secure hide protection, or TrustZone

# Protecting unused memory

Wri  u  ul meo v m a (SWI) op-codes, illegal op-codes, or NOPs.

Associated protections: MPU or WRP

# Error code correction (ECC)

Te fashmemoy etimes atu EC that alws erordeetion an ceton up  -bi er dn ator corectin Moe consider s  sfety eature also works s  cpleentar pro against fault injection.

# 4.4.3 Embedded SRAM

Tbede RAM is hedevice workgemory I is used o ack,hepgloal bursandvriabl a ntmehe SRAM can be acces as bytes, half-words 6 bit), rfullwords 32 bit), at maxium sem clock frequency without wait state.

# Code execution

T  n memory, and executed from the SRAM. Another reason to execute code from the SRAM is when using encrypted al iihnsiA execution. Appropriate memory protections must then be enabled on the SRAM address range containing the c.Wheno code must be executed i the SRAM, is advised o prevent any malware execution by etting the appropriate attribute (execute never) with the MPU.

Associated protections: MPU or firewall

# SRAM cleaning

TheSRAM can contai sensitive ata o temorary values allowig some secrets etriving. typical exapl anhic o o cerxA. I highly recommended to clean explicitly the working buffers and variables immediately after the processing functions manipulating sensitive data.

# Note:

In cs f reset, the TM32 MCUs allow the autoati erase f the SRAM (reer  the reference manual. For some devices, part of the SRAM is protected against external access or untrusted boot (SRAM boot) when the RDP is set.

# Write protection

The write protection can be used to isolate part of the area from being corrupted by another process or ypenteowckveowattoahaheru n r e the SRAM regions, which are used primarily for code execution (this protection is not practical for data). The SRAM write protection is available for SRAM2 region on some STM32 MCUs only (refer to Section 6.1: Overview of security features and to the reference manual).

Associated protections: MPU, TrustZone, or SRAM write protection (available on some STM32 devices only)

# Parity check and ECC

T Al   yent aieu Class B or SIL norms. ECC is more sophisticated, with SECDED functionality, but only available for SRAM on certain MCU devices. Integrity protections based on redundancy often cannot be disabled.

# 4.4.4 External flash memories

The external flash memories are connected to the microcontroller through dedicated interfaces (NAND, NOR, Octo-SPl, or Quad-SPl). As the embeded flash memory, the external ones contain code and data, but the es bleentialinn oio)tiati . T in broht yryptography algorithsThe conten must bt leassie avoexecutionauhentia firmware. Encryption is required only if the content is confidential.

The embedded code can be either executed in-place or loaded into the SRAM before execution. Execution in-tewmust deryp when oade inAM. edeypcod par ot pro from readout (RDP2), then the confidentiality of the code is violated. It is also recommended to combine encryption with integrity protection.

Associated protection: OTFDEC, MCE

# 4.4.5

# STM32 memory protections

Several  eatures aavailable coverhevari cascnsieTheye ltehe tableeo with their respective scope, and described in Section 6: STM32 security features.

Table 6. Scope of STM32 embedded memory protection features   

<table><tr><td rowspan=1 colspan=1>Feature</td><td rowspan=1 colspan=1>External attackprotection</td><td rowspan=1 colspan=1>Internal attackprotection</td><td rowspan=1 colspan=1>Flash memory</td><td rowspan=1 colspan=1>SRAM</td></tr><tr><td rowspan=1 colspan=1>RDP</td><td rowspan=1 colspan=1>Yes</td><td rowspan=1 colspan=1>No</td><td rowspan=1 colspan=1>Yes</td><td rowspan=1 colspan=1>Yes</td></tr><tr><td rowspan=1 colspan=1>Firewall</td><td rowspan=1 colspan=1>No</td><td rowspan=1 colspan=1>Yes</td><td rowspan=1 colspan=1>Yes</td><td rowspan=1 colspan=1>Yes</td></tr><tr><td rowspan=1 colspan=1>MPU</td><td rowspan=1 colspan=1>No</td><td rowspan=1 colspan=1>Yes</td><td rowspan=1 colspan=1>Yes</td><td rowspan=1 colspan=1>Yes</td></tr><tr><td rowspan=1 colspan=1>PCROP(1)</td><td rowspan=1 colspan=1>Yes</td><td rowspan=1 colspan=1>Yes (read/write)</td><td rowspan=1 colspan=1>Yes</td><td rowspan=1 colspan=1>No</td></tr><tr><td rowspan=1 colspan=1>WRP(2)</td><td rowspan=1 colspan=1>Yes</td><td rowspan=1 colspan=1>Yes</td><td rowspan=1 colspan=1>Yes</td><td rowspan=1 colspan=1>No</td></tr><tr><td rowspan=1 colspan=1>HDP</td><td rowspan=1 colspan=1>Yes</td><td rowspan=1 colspan=1>Yes</td><td rowspan=1 colspan=1>Yes</td><td rowspan=1 colspan=1>Yes (for execution)(3)</td></tr><tr><td rowspan=1 colspan=1>TrustZone®, RIF</td><td rowspan=1 colspan=1>Yes</td><td rowspan=1 colspan=1>Yes</td><td rowspan=1 colspan=1>Yes</td><td rowspan=1 colspan=1>Yes</td></tr></table>

Support of this feature in Armv6-M products is limited as constant data cannot be stored in NVM. 2. Write protection can be unset when RDP level ≠ 2.

# 4.5 Software isolation

The otalatnteeani oeingin  ae te protection). These processes can be executed sequentially or concurrently (or example tasks ofoperating system).he software solation in theSRAM ensures that respective stack and working dat each process c   oontn memory and nonvolatile data as well.

Goals of the software isolation:

Prevent a process to spy the execution of another sensitive process.   
Protect a process execution against a stack corruption due to memory leaks or overflow (incorrect memory management implementation).

This memory protection can be achieved through diferent mechanisms listed in the table below, and detailed in Section 6: STM32 security features .

Table 7. Software isolation mechanism   

<table><tr><td rowspan=1 colspan=1>Protection</td><td rowspan=1 colspan=1>Type</td><td rowspan=1 colspan=1>Isolation</td></tr><tr><td rowspan=1 colspan=1>MPU</td><td rowspan=1 colspan=1>Dynamic</td><td rowspan=1 colspan=1>By privilege attribute</td></tr><tr><td rowspan=1 colspan=1>Firewall</td><td rowspan=1 colspan=1>Static</td><td rowspan=1 colspan=1>By bus address hardware control</td></tr><tr><td rowspan=1 colspan=1>Secure hide protection</td><td rowspan=1 colspan=1>Static</td><td rowspan=1 colspan=1>Process preemption at reset</td></tr><tr><td rowspan=1 colspan=1>Dual core</td><td rowspan=1 colspan=1>Static</td><td rowspan=1 colspan=1>By core ID2)</td></tr><tr><td rowspan=1 colspan=1>TrustZone®/Security attribute</td><td rowspan=1 colspan=1>Static and dynamic</td><td rowspan=1 colspan=1> a </td></tr></table>

et on  no ke heuss u MA. Reading the CPUID indicates which CPU is currently executing code. An example can be found in the HAL_GetCurrentCPUID function.

# 4.6

# Debug port and other interface protection

The debug ports provide acess the internal esourcs (corememoris,an registers) and must edisabled i  etJAG W cur nimuable war re  Sectn5.3.Secu boot   preerably y permnty disabling the functionality (JTAG fuse in RDP2).

O l inteac can e eotvilbl teevicntnt cne r I2C SPI,USART,  USB-DFU.  heteacuri hen, heplatn protocol must limit its access capabilities (such as operation mode or address access range).

Associated STM32 features:

read protection (RDP)/product state   
disable of unused ports   
bootloader access forbidden (configured by RDP in STM32 devices)

# .7 Boot protection

teevoeeienpnap or to access unsecured bootloader applications that give access to the device memory.

mtalllogatio aro pliatin RA locatae ot protconrelsgle a trusted code that can be the user application, or a secure service area if available (RSS).

Associated STM32 features:

read protection (RDP)/product state   
unique boot entry   
secure hide protection (HDP)   
TrustZone

# 8 System monitoring

The monitoring of the device power supply and environment can be set to avoid malfunction and to take corresponding countermeasures. Some mechanisms, like tamper detection, are dedicated to security. Other manis  raru  yan u n riy  weoaple ee powtl ontl y.

Tardetectionus etyte/boar ve intrusins.eenicnserproduc c irregular voltage, temperature, or other parameters.

Clcuriyysteuspoe agaisexteal cilatlur. ailetec allows the firmware to react to the clock failure event.

ply ol vealy-oltBer value, the normal behavior cannot be guaranteed and it may be the sign of a fault injection attack.

Device temperature can be measured with an internal sensor. The information is feedbacked to the device through an internal ADC channel. A monitoring application can take appropriate actions according to the temperature range. Increased temperature may be part of a fault injection attack scheme.

Associated STM32 features:

tamper protection (with RTC component)   
clock security system   
power supply supervision   
temperature sensor

# 5 Secure applications

Inrercrat  secure ystem, hharware atures must eused n secue warearhiue implementation. An industry standard solution is the PSA, proposed by Arm for the loT ecosystem. The ou  o    s use Secure firmware installation (SFI) to securely provision blank devices in manufacturing.

This section defines the root and chain of trust concept before presenting the following typical secure applications implementing the features listed below:

Secure boot Secure firmware update Secure storage Cryptographic services

Thee applications have a close link with cryptography. All cryptographic schemes are based on the three concepts of secret key, public key, and hashing. Basics of cryptography are explained in Appendix A. Cryptography - Main concepts.

# Note:

The document [9] provides an implementation example of SB and SFU (www.st.com/en/product/ x-cube-sbsfu).   
The user manual 'Getting started with STM32CubeL5 TF-M application' (UM2671) describes an example of TF-M implementation with the STM32L5 Series MCU.   
The user manual 'Getting started with STM32CubeU5 TF-M application' (UM2851) describes an example of TF-M implementation with the STM32U5 Series MCU.

# 5.1

# Secure firmware install (SFI)

In ams uc ae   are pr o o to an untrusted environment.

In the  aro, he biar ae cpte usig ruste ackage reator otware ool and HSM within the production facility, to install the code in the microcontrollers.

# Note:

See AN5391, AN5054, and AN4992 for more information

SFI is supported on STM32L4, STM32L5, STM32U3, STM32U5, STM32H5, STM32N6, and STM32H7 series.

# 5.2 Root and chain of trust

a  ll, inherently efficient and also flexible.

iu depends.

T mo I uaqu alieex e volatile memory protection, so that a secure storage service can use it.

# 5.3

# STMicroelectronics proprietary SBSFU solution

Secure boot and secure firmware update are complementary security concepts. The associated model implementation can be found in the X-CUBE-SBSFU package.

# 5.3.1

# Secure boot (SB)

responsible for ensuring the global chain of trust of the system.

SB main functionalities:

Check the STM32 security configuration and set up runtime protections.   
Asr hetegriy entc eaplanags hatec e hegu).

![](images/05ab4de377d1ddffdb0c7f6e07f65e27eddca5f493fcc71f7c8dacd15654f8c0.jpg)  
Figure 6. Secure boot FSM

# Device security check

This parheliatinchecksstaciguatins ae corra enamnS secre configurations are defined by option bytes (RDP, PCROP, WRP, and HDP). Dynamic protections must be programmed (firewall, MPU, tamper detection, and IWDG).

# Integrity and authenticity check

The firmware integrity is performed by hashing the application image (with MD5, SHA1, or SHA256 hash aloriths, and coparing the diges with the expeced This way, theapplicationfware  con error-free.

An auhenticheck sdthepe cyp wiky harewenhw and the device. This key is stored in a protected area of the device.

# Protection attributes

The SB firmware must have the following attributes to fulfill its role:

It must be the device-unique entry point (no bypass).   
Its code must be immutable.   
It must have access to sensitive data (such as certificates or application signatures).

Ti ar   l P hide protection. the implementation depends on the STM32 available features.

# 5.3.2

# Secure firmware update (SFU)

T rovicuplentatonlwadatablngownlaef images to a device.

The firmware update is a sensitive operation that must protect two parties:

thedeviwerhe goal stoavo loadig acorruptefwa intentnally r ot) that an dae the device.   
the application owner (OEM): needs to protect his firmware from being cloned or loaded into   
an unauthorized device.

# Architecture

U rnvol othe M nd eevi ea e e eiatiaesicujve lhet device).

![](images/0d691fa8cf4f9828710bd11a23b33dce571c522d60d2b97ddd8347cfcdb8489b.jpg)  
Figure 7. Secure server/device SFU architecture

# Application

Fro OM  erveitaieha sible din he ptntl required) and signed firmware to an authenticated device.

The SFU application running on device is in charge of the following:

authentication and integrity checking of the loaded image before installing decrypting the new firmware if confidentiality is required checking the new firmware version (anti-rollback mechanism)

# 5.3.3 Configurations

The proprietary is ery configurable The most portant confguration optionis the choice  usa sigeordual imagehandling application code. Eachhas a separate example.Sigle mage leaves more space for application code. Two or more images add some advanced features to the image handling.

T

ECDSA asymmetric cryptography for firmware verification with AES-CBC or AES-CTR symmetric   
cryptography for firmware encryption   
ECDSA asymmetric cryptography for firmware verification without firmware encryption   
X509 certificate-based ECDSA asymmetric cryptography for firmware verification without firmware   
encryption   
AES-GCM symmetric cryptography for both firmware verification and encryption

For more details, see the document [9] or the document Integration guide or the X-CUBE-BSFU STM32Cube Expansion Package (AN5056).

# .4 Arm TF-M solution

Artrustare existrhis base nCore when he ecurortex-33 core was trduch Armv8-M architecture. A more compact TF-M open source implementation of PSA standard was provided as a reference secure firmware framework.

For STMicroelectronics MCUs that take advantage of the Armv8 architecture (such as STM32H5, STM32L5, STM32U3 and STM32U5 devices), the SBSFU is replaced with the TF-M based solution.

For a documentation n TF- itse, refer to the UM2851, nd use Arm resources as well as the code comments

For guidance on TF-M integration on the STM32L5 and STM32U5 devices, refer to the user manuals Getting started with STM32CubeL5 TF-M application (UM2671) or Getting started with STM32CubeU5 TF-M application (UM2851).

Refer to document [7] for a detailed comparison when migrating from X-CUBE-SBSFU package SBSFU to TF-M.

Table 8. Basic feature differences of TrustZone-based secure software   

<table><tr><td rowspan=1 colspan=1>Feature</td><td rowspan=1 colspan=1>SBSFU for TrustZone®</td><td rowspan=1 colspan=1>TF-M</td></tr><tr><td rowspan=1 colspan=1>RoT services</td><td rowspan=1 colspan=1>Immutable RoT</td><td rowspan=1 colspan=1>Immutable RoT + updatable RoT</td></tr><tr><td rowspan=1 colspan=1>Cryptographic key management</td><td rowspan=1 colspan=1>Static keys only</td><td rowspan=1 colspan=1>Key storage hierarchy with HUK root key</td></tr><tr><td rowspan=1 colspan=1>Secure storage</td><td rowspan=1 colspan=1>Absent</td><td rowspan=1 colspan=1>Internal and external</td></tr><tr><td rowspan=1 colspan=1>NV counter</td><td rowspan=1 colspan=1>No</td><td rowspan=1 colspan=1>Yes</td></tr></table>

Boteativs  ae MCU boot t whiUte liat iatu  - CUBE-SBSFU while retaining most flash memory space for user code, TF-M offers more functionality. Some o that can be dropped to gain memory space. For the STM32H57x line, the Secure manager, a closed-source implementation of TF-M, offers a convenient and express way to adopt certified secure solutions.

# 5.5

# Secure manager

TglSeeaagergucses ct coaolu Sec implements the SA secure APs (similar o the TF-M) and by using them, the user nonsecure applicatin cn form a secure system with certified attack resistance.

TS STM32H5 MCUs.

Secure manager can expand its secure functionality by using modules.

# 5.6 Product certifications

if l manner. Independent or government agencies grant the certification status to either an MCU application or a combination of MCUs with secure firmware after testing it against the evaluation goals.

he certifications and evaluations related to STM32 microcontrollers include, but are not limited to:

certi (platfor security architecture), govened byAr, focusedon o security, C certifatin, three levels of assessment

STM32L4, STM32G0, and STM32G4 devices are certifiable up to Level 1.   
STM32L5 devices with TF-M are certifiable up to Level 2.   
STM32U5, STM32H7S, STM32U0, STM32U3, and STM32H5 devices with TF-M are certifiable up to Level 3.   
To achieve Arm PSA certifiable security level, refer to the user manual STM32U585 security guidance for PSA Certified™ Level 3 with SESIP Profile (UM2852).

SESIP (security evaluation standard or lo platforms), international methodology adopted by several maor security evaluation labs, five levels

Systems using SBSFU or TF-M are compliant to Level 3 with STM32L4, STM32L4+, STM32L5, STM32H5, STM32N6, and STM32U5 devices.

PCI (payment card information), important security standard focusing on point of sale (POS) applications Good record of successful evaluation of systems, using for example, STM32L4 devices

FIPS (Federal Information Processing Standards) is a  of standars published by NIST, some f which (FIPS 140, SP800) are related to security or cryptography.

Table 9. Certifications coverage   

<table><tr><td rowspan=1 colspan=1>MCU series</td><td rowspan=1 colspan=1>Crypto conformancecertification</td><td rowspan=1 colspan=1>Security systemcertification</td><td rowspan=1 colspan=1>Security systemcertification with physicalresistance (invasive)</td></tr><tr><td rowspan=1 colspan=1>STM32G0/STM32G4</td><td rowspan=2 colspan=1>FIPS CAVP, SP800-90A</td><td rowspan=4 colspan=1>PSA L1</td><td rowspan=5 colspan=1></td></tr><tr><td rowspan=1 colspan=1>STM32L4</td></tr><tr><td rowspan=1 colspan=1>STM32L4+</td><td rowspan=3 colspan=1></td></tr><tr><td rowspan=1 colspan=1>STM32H7</td></tr><tr><td rowspan=1 colspan=1>STM32L5</td><td rowspan=1 colspan=1>PSA L2, SESIP L3</td></tr><tr><td rowspan=1 colspan=1>STM32WBA</td><td rowspan=2 colspan=1>FIPS CAVP, SP800-90B</td><td rowspan=4 colspan=1>Yes</td><td rowspan=2 colspan=1>PSA L3, SESIP L3 (withTF-M)</td></tr><tr><td rowspan=1 colspan=1>STM32U5</td></tr><tr><td rowspan=1 colspan=1>STM32H5</td><td rowspan=1 colspan=1></td><td rowspan=1 colspan=1>PSA L3, SESIP L3 (withSecure manager)</td></tr><tr><td rowspan=1 colspan=1>STM32H7Sx</td><td rowspan=1 colspan=1></td><td rowspan=1 colspan=1>PSA L3, SESIP L3 (usingRoT)</td></tr></table>

# 6 STM32 security features

Thi ecin peents alhe atues hat n s mee he iffen urint e in previous sections, and to achieve a high level of security.

# 6.1

# Overview of security features

# Static and dynamic protections

A distinction can be made depending on whether protection features are static or dynamic:

Stat protections er  features that are et with option bys.The coniguration s retainedat pw off.   
Static protections are RDP (or product state), PCROP, WRP, BOR, OTP, and secure hide protection (when available).   
Dynamic (or run time) protections do not retain their status at reset. They have to be configured at each boot (for example during Secure boot (SB) ).   
Dynamic protections provided by STM32 include MPU, tamper detection, and firewall.   
Other dynamic protections are related to both security and safety. An abnormal environment behavior may bacidental afetytentional, irder  carryout an atckThe protecions include clo power monitoring systems, memory integrity bits, and independent watchdog (IWDG).

# 6.1.2

# Security features by STM32 devices

Following tables are ntendeoreference and he prospects ecure code porting between 2 prcts. the available security certifications for the particular product.

Table 10. Security features for STM32C0, STM32F0/1/2/3/4, STM32G0/4 devices   

<table><tr><td rowspan=1 colspan=1>Feature</td><td rowspan=1 colspan=1>STM32C0</td><td rowspan=1 colspan=1>STM32F0</td><td rowspan=1 colspan=1>STM32F1</td><td rowspan=1 colspan=1>STM32F2</td><td rowspan=1 colspan=1>STM32F3</td><td rowspan=1 colspan=1>STM32F4</td><td rowspan=1 colspan=1>STM32G0</td><td rowspan=1 colspan=1>STM32G4</td></tr><tr><td rowspan=1 colspan=1>Cortex core</td><td rowspan=1 colspan=1>Cortex-M0+</td><td rowspan=1 colspan=1>Cortex-MO</td><td rowspan=1 colspan=1>Cortex-M3</td><td rowspan=1 colspan=1>Cortex-M3</td><td rowspan=1 colspan=1>Cortex-M4</td><td rowspan=1 colspan=1>Cortex-M4</td><td rowspan=1 colspan=1>Cortex-MO+</td><td rowspan=1 colspan=1>Cortex-M4</td></tr><tr><td rowspan=1 colspan=1>RDP additionalprotection</td><td rowspan=1 colspan=1>Bad OBLrecovery</td><td rowspan=1 colspan=1>Backupregisters</td><td rowspan=1 colspan=1>2 level RDPonly</td><td rowspan=1 colspan=1>Backup SRAM</td><td rowspan=1 colspan=1>Backupregisters</td><td rowspan=1 colspan=1>Backup SRAM</td><td rowspan=1 colspan=1>Backupregisters</td><td rowspan=1 colspan=1>Backupreisters, CMSRAM</td></tr><tr><td rowspan=1 colspan=1>Flash WRP</td><td rowspan=1 colspan=1>By area with2-Kbytegranularity, twoareas available</td><td rowspan=1 colspan=1>By sectors Kbytes)</td><td rowspan=1 colspan=1>By pages (4 Kor 8Kbytes)</td><td rowspan=1 colspan=1>By sectors(16 K, 64 K, or128 Kbyte</td><td rowspan=1 colspan=1>By sectors Kbytes)</td><td rowspan=1 colspan=1>By sectors(16 K, 64 K, or128 Kytes)</td><td rowspan=1 colspan=1>By area with2--Kbytegranularity, twoareas available</td><td rowspan=1 colspan=1>By page (2 K or4 Kbytes)</td></tr><tr><td rowspan=1 colspan=1>SRAM WRP</td><td rowspan=1 colspan=1>No</td><td rowspan=1 colspan=1>No</td><td rowspan=1 colspan=1>No</td><td rowspan=1 colspan=1>No</td><td rowspan=1 colspan=1>No</td><td rowspan=1 colspan=1>No</td><td rowspan=1 colspan=1>No</td><td rowspan=1 colspan=1>CCM SRAM,with 1-Kbytegrannularity</td></tr><tr><td rowspan=1 colspan=1>PCROP</td><td rowspan=1 colspan=1>By area with56-bytegranularity, onegarea per bank</td><td rowspan=1 colspan=1>No</td><td rowspan=1 colspan=1>No</td><td rowspan=1 colspan=1>No</td><td rowspan=1 colspan=1>No</td><td rowspan=1 colspan=1>By sectors</td><td rowspan=1 colspan=1>By area with512-bytegranularity, twoareas available</td><td rowspan=1 colspan=1>By area with64- or 28-bitgranulaity, upto two areas</td></tr><tr><td rowspan=1 colspan=1>HDP</td><td rowspan=1 colspan=1>Yes (securablememory area</td><td rowspan=1 colspan=1>No</td><td rowspan=1 colspan=1>No</td><td rowspan=1 colspan=1>No</td><td rowspan=1 colspan=1>No</td><td rowspan=1 colspan=1>No</td><td rowspan=1 colspan=2>Yes (securable memory area)</td></tr><tr><td rowspan=1 colspan=1>Firewall</td><td rowspan=1 colspan=1>No</td><td rowspan=1 colspan=1>No</td><td rowspan=1 colspan=1>No</td><td rowspan=1 colspan=1>No</td><td rowspan=1 colspan=1>No</td><td rowspan=1 colspan=1>No</td><td rowspan=1 colspan=1>No</td><td rowspan=1 colspan=1>No</td></tr><tr><td rowspan=1 colspan=1>MPU</td><td rowspan=1 colspan=1>Yes</td><td rowspan=1 colspan=1>No</td><td rowspan=1 colspan=1>Yes(1)</td><td rowspan=1 colspan=1>Yes</td><td rowspan=1 colspan=1>Yes(2)</td><td rowspan=1 colspan=1>Yes</td><td rowspan=1 colspan=1>Yes</td><td rowspan=1 colspan=1>Yes</td></tr><tr><td rowspan=1 colspan=1>OTP</td><td rowspan=1 colspan=1>1 Kbyte</td><td rowspan=1 colspan=1>No</td><td rowspan=1 colspan=1>No</td><td rowspan=1 colspan=1>Yes</td><td rowspan=1 colspan=1>Yes</td><td rowspan=1 colspan=1>512 bytes</td><td rowspan=1 colspan=1>1 Kbyte</td><td rowspan=1 colspan=1>1 Kbyte</td></tr><tr><td rowspan=1 colspan=1>UBE(3)</td><td rowspan=1 colspan=1>Yes (boot lockfeature)</td><td rowspan=1 colspan=1>No</td><td rowspan=1 colspan=1>No</td><td rowspan=1 colspan=1>No</td><td rowspan=1 colspan=1>No</td><td rowspan=1 colspan=1>No</td><td rowspan=1 colspan=1>Yes (boot lockeature)</td><td rowspan=1 colspan=1>Yes</td></tr><tr><td rowspan=1 colspan=1>Internal tamperettection</td><td rowspan=1 colspan=1>No</td><td rowspan=1 colspan=1>No</td><td rowspan=1 colspan=1>No</td><td rowspan=1 colspan=1>No</td><td rowspan=1 colspan=1>No</td><td rowspan=1 colspan=1>No</td><td rowspan=1 colspan=1>Yes</td><td rowspan=1 colspan=1>Yes</td></tr><tr><td rowspan=1 colspan=1>Hardwarecrypto(4</td><td rowspan=1 colspan=1>No</td><td rowspan=1 colspan=1>No</td><td rowspan=1 colspan=1>No</td><td rowspan=1 colspan=1>AES, HASH</td><td rowspan=1 colspan=1>No</td><td rowspan=1 colspan=1>AES, HASH</td><td rowspan=1 colspan=2>AES</td></tr><tr><td rowspan=1 colspan=1>RNG</td><td rowspan=1 colspan=1>No</td><td rowspan=1 colspan=1>No</td><td rowspan=1 colspan=1>No</td><td rowspan=1 colspan=1>SP800-90-A</td><td rowspan=1 colspan=1>No</td><td rowspan=1 colspan=3>SP800-90-A</td></tr></table>

<table><tr><td rowspan=1 colspan=2>Feature</td><td rowspan=1 colspan=1>STM32C0</td><td rowspan=1 colspan=1>STM32F0</td><td rowspan=1 colspan=1>STM32F1</td><td rowspan=1 colspan=1>STM32F2</td><td rowspan=1 colspan=1>STM32F3</td><td rowspan=1 colspan=1>STM32F4</td><td rowspan=1 colspan=1>STM32G0</td><td rowspan=1 colspan=1>STM32G4</td></tr><tr><td rowspan=3 colspan=1>20</td><td rowspan=1 colspan=1>SBSFU</td><td rowspan=1 colspan=1>No</td><td rowspan=1 colspan=1>No</td><td rowspan=1 colspan=1>No</td><td rowspan=1 colspan=1>No</td><td rowspan=1 colspan=1>No</td><td rowspan=1 colspan=1>Yes</td><td rowspan=1 colspan=1>Yes</td><td rowspan=1 colspan=1>Yes</td></tr><tr><td rowspan=1 colspan=1>TF-M</td><td rowspan=1 colspan=1>No</td><td rowspan=1 colspan=1>No</td><td rowspan=1 colspan=1>No</td><td rowspan=1 colspan=1>No</td><td rowspan=1 colspan=1>No</td><td rowspan=1 colspan=1>No</td><td rowspan=1 colspan=1>No</td><td rowspan=1 colspan=1>No</td></tr><tr><td rowspan=1 colspan=1>KMS</td><td rowspan=1 colspan=1>No</td><td rowspan=1 colspan=1>No</td><td rowspan=1 colspan=1>No</td><td rowspan=1 colspan=1>No</td><td rowspan=1 colspan=1>No</td><td rowspan=1 colspan=1>No</td><td rowspan=1 colspan=1>No</td><td rowspan=1 colspan=1>No</td></tr></table>

1. Only XL density devices feature the MPU. 2. MPU is not universally supported in STM32F3 seris. Refer to the product datasheet to confir availability. 3. Unique boot entry. For most devices with hardware crypto capability, there is a direct equivalent without it.

Table 11. Security features for STM32L0/1/4/4+ devices   

<table><tr><td rowspan=1 colspan=2>Feature</td><td rowspan=1 colspan=1>STM32L0</td><td rowspan=1 colspan=1>STM32L1</td><td rowspan=1 colspan=1>STM32L4</td><td rowspan=1 colspan=1>STM32L4+</td></tr><tr><td rowspan=1 colspan=2>Cortex core</td><td rowspan=1 colspan=1>Cortex-MO</td><td rowspan=1 colspan=1>Cortex-M3</td><td rowspan=1 colspan=2>Cortex-M4</td></tr><tr><td rowspan=1 colspan=2>RDP additional protection</td><td rowspan=1 colspan=2>EEPROM</td><td rowspan=1 colspan=2>Backup registers, SRAM2</td></tr><tr><td rowspan=1 colspan=2>Flash WRP</td><td rowspan=1 colspan=2>By sectors (4 Kbytes)</td><td rowspan=1 colspan=2>By area with 2-Kbyte granularity, one area per bank</td></tr><tr><td rowspan=1 colspan=2>SRAM WRP</td><td rowspan=1 colspan=1>No</td><td rowspan=1 colspan=1>No</td><td rowspan=1 colspan=2>SRAM2, with 1-Kbyte granularity</td></tr><tr><td rowspan=1 colspan=2>PCROP</td><td rowspan=1 colspan=2>By sectors</td><td rowspan=1 colspan=2>By area with 8-byte granularity, one area per bank</td></tr><tr><td rowspan=1 colspan=2>HDP</td><td rowspan=1 colspan=1>No</td><td rowspan=1 colspan=1>No</td><td rowspan=1 colspan=1>No</td><td rowspan=1 colspan=1>No</td></tr><tr><td rowspan=1 colspan=2>Firewall</td><td rowspan=1 colspan=1>Yes</td><td rowspan=1 colspan=1>No</td><td rowspan=1 colspan=1>Yes</td><td rowspan=1 colspan=1>Yes</td></tr><tr><td rowspan=1 colspan=2>MPU</td><td rowspan=1 colspan=1>Yes</td><td rowspan=1 colspan=1>Yes</td><td rowspan=1 colspan=1>Yes</td><td rowspan=1 colspan=1>Yes</td></tr><tr><td rowspan=1 colspan=2>OTP</td><td rowspan=1 colspan=1>No</td><td rowspan=1 colspan=1>No</td><td rowspan=1 colspan=2>1 Kbyte</td></tr><tr><td rowspan=1 colspan=2>UBE(1)</td><td rowspan=1 colspan=1>No</td><td rowspan=1 colspan=1>No</td><td rowspan=1 colspan=1>No</td><td rowspan=1 colspan=1>No</td></tr><tr><td rowspan=1 colspan=2>Internal tamper detection</td><td rowspan=1 colspan=1>No</td><td rowspan=1 colspan=1>No</td><td rowspan=1 colspan=1>No</td><td rowspan=1 colspan=1>No</td></tr><tr><td rowspan=1 colspan=2>Hardware crypto(2)</td><td rowspan=1 colspan=2>AES</td><td rowspan=1 colspan=1>AES, HASH</td><td rowspan=1 colspan=1>AES, HASH,some PKA)</td></tr><tr><td rowspan=1 colspan=2>RNG</td><td rowspan=1 colspan=1>No</td><td rowspan=1 colspan=1>No</td><td rowspan=1 colspan=1>SP800-90-A</td><td rowspan=1 colspan=1>SP 800-90-B</td></tr><tr><td rowspan=3 colspan=1>see snmee</td><td rowspan=1 colspan=1>SBSFU</td><td rowspan=1 colspan=1>Yes</td><td rowspan=1 colspan=1>Yes</td><td rowspan=1 colspan=1>Yes</td><td rowspan=1 colspan=1>Yes</td></tr><tr><td rowspan=1 colspan=1>TF-M</td><td rowspan=1 colspan=1>No</td><td rowspan=1 colspan=1>No</td><td rowspan=1 colspan=1>No</td><td rowspan=1 colspan=1>No</td></tr><tr><td rowspan=1 colspan=1>KMS</td><td rowspan=1 colspan=1>No</td><td rowspan=1 colspan=1>No</td><td rowspan=1 colspan=1>Yes</td><td rowspan=1 colspan=1>Yes</td></tr></table>

Unique boot entry. For most devices with hardware crypto capability, there is a direct equivalent without it.

Table 12. Security features for STM32WB, STM32WBA, STM32WB0x, STM32WL, and STM32WL3 devices   

<table><tr><td colspan="2" rowspan="1">Feature</td><td colspan="1" rowspan="1">STM32WB</td><td colspan="1" rowspan="1">STM32WBA</td><td colspan="1" rowspan="1">STM32WB0x</td><td colspan="1" rowspan="1">STM32WL</td><td colspan="1" rowspan="1">STM32WL3</td></tr><tr><td colspan="2" rowspan="1">Cortex core</td><td colspan="1" rowspan="1">Cortex-M4/Cortex-M0+</td><td colspan="1" rowspan="1">Cortex-M33</td><td colspan="1" rowspan="1">Cortex-M0+</td><td colspan="1" rowspan="1">Cortex-M4/Cortex-M0+</td><td colspan="1" rowspan="1">Cortex-M0+</td></tr><tr><td colspan="2" rowspan="1">RDP additional protection</td><td colspan="1" rowspan="1">Backup registers,RAM2</td><td colspan="1" rowspan="1">RDP four levels,backupregisters, SRAM</td><td colspan="1" rowspan="1">No</td><td colspan="1" rowspan="1">Backup registers,RAM2</td><td colspan="1" rowspan="1">No</td></tr><tr><td colspan="1" rowspan="1">Flash WRP</td><td colspan="1" rowspan="1">By area with 4-Kbytegranularity, two areasavailable</td><td colspan="1" rowspan="1">Two areas, defined bypage range</td><td colspan="2" rowspan="1">By area with 2-Kbyte granularity, two areasavailable</td><td colspan="2" rowspan="1">Four areas</td></tr><tr><td colspan="1" rowspan="1">SRAM WRP</td><td colspan="2" rowspan="1">SRAM2, with 1-Kbyte granularity</td><td colspan="1" rowspan="1">No</td><td colspan="1" rowspan="1">SRAM2, with 1-Kbytegranularity</td><td colspan="2" rowspan="1">No</td></tr><tr><td colspan="1" rowspan="1">PCROP</td><td colspan="1" rowspan="1">By area with 2-Kbytegranularity, up to twoareas</td><td colspan="2" rowspan="1">No</td><td colspan="1" rowspan="1">By area with 1-Kbytegranularity, two areasavailable</td><td colspan="2" rowspan="1">No</td></tr><tr><td colspan="2" rowspan="1">HDP</td><td colspan="1" rowspan="1">Yes (dedicated toCortex-M0+ firmwareonly)</td><td colspan="1" rowspan="1">Yes</td><td colspan="1" rowspan="1">No</td><td colspan="1" rowspan="1">Yes</td><td colspan="1" rowspan="1">No</td></tr><tr><td colspan="2" rowspan="1">Feature</td><td colspan="1" rowspan="1">STM32WB</td><td colspan="1" rowspan="1">STM32WBA</td><td colspan="1" rowspan="1">STM32WB0x</td><td colspan="1" rowspan="1">STM32WL</td><td colspan="1" rowspan="1">STM32WL3</td></tr><tr><td colspan="2" rowspan="1">Firewall</td><td colspan="1" rowspan="1">No</td><td colspan="2" rowspan="1">No</td><td colspan="1" rowspan="1">Yes</td><td colspan="1" rowspan="1">No</td></tr><tr><td colspan="2" rowspan="1">MPU</td><td colspan="1" rowspan="1">Yes (Cortex-M4)</td><td colspan="1" rowspan="1">Yes</td><td colspan="1" rowspan="1">Yes</td><td colspan="1" rowspan="1">Yes</td><td colspan="1" rowspan="1">Yes</td></tr><tr><td colspan="2" rowspan="1">OTP</td><td colspan="3" rowspan="1">1 Kbyte</td><td colspan="1" rowspan="1"></td><td colspan="1" rowspan="1"></td></tr><tr><td colspan="2" rowspan="1">UBE(1)</td><td colspan="1" rowspan="1">No</td><td colspan="1" rowspan="1">Yes (lockable secureand NS address)</td><td colspan="1" rowspan="1">No</td><td colspan="1" rowspan="1">Yes (boot lock feature)</td><td colspan="1" rowspan="1">No</td></tr><tr><td colspan="2" rowspan="1">Internal tamper detection</td><td colspan="1" rowspan="1">No</td><td colspan="1" rowspan="1">Yes</td><td colspan="1" rowspan="1">No</td><td colspan="1" rowspan="1">Yes</td><td colspan="1" rowspan="1">No</td></tr><tr><td colspan="2" rowspan="1">Hardware crypto(2)</td><td colspan="1" rowspan="1">AES, PKA</td><td colspan="1" rowspan="1">AES, HASH, PKA</td><td colspan="2" rowspan="1">AES(3), PKA</td><td colspan="1" rowspan="1">AES</td></tr><tr><td colspan="2" rowspan="1">RNG</td><td colspan="1" rowspan="1">SP800-90-A</td><td colspan="1" rowspan="1">800-90-B</td><td colspan="2" rowspan="1">SP 800-90-B</td><td colspan="1" rowspan="1"></td></tr><tr><td colspan="1" rowspan="3">20</td><td colspan="1" rowspan="1">SBSFU</td><td colspan="1" rowspan="1">Yes</td><td colspan="1" rowspan="1">Yes</td><td colspan="1" rowspan="1">Yes(4)</td><td colspan="1" rowspan="1">Yes</td><td colspan="1" rowspan="1">Yes(4)</td></tr><tr><td colspan="1" rowspan="1">TF-M</td><td colspan="1" rowspan="1">No</td><td colspan="1" rowspan="1">Yes</td><td colspan="1" rowspan="1">No</td><td colspan="1" rowspan="1">No</td><td colspan="1" rowspan="1">No</td></tr><tr><td colspan="1" rowspan="1">KMS</td><td colspan="1" rowspan="1">No</td><td colspan="1" rowspan="1">No</td><td colspan="1" rowspan="1">No</td><td colspan="1" rowspan="1">No</td><td colspan="1" rowspan="1">No</td></tr></table>

Unique boot entry. 2. For most devices with hardware crypto capability, there is a direct equivalent without it. 3. For STM32WB0, the AES is only available on the radio peripheral. Secure boot solution separated from the usual X-CUBE-SBSFU package.

# Table 13. Security features for STM32L5, STM32U0, STM32U3, STM32U5, STM32H503/5, STM32H7R/S, STM32H72x/73/74x/75, STM32H7Ax/7Bx, STM32F7 devices

<table><tr><td rowspan=1 colspan=1>Feature</td><td rowspan=1 colspan=1>STM32L5</td><td rowspan=1 colspan=1>STM32U0</td><td rowspan=1 colspan=1>STM32U3SSTM32U5</td><td rowspan=1 colspan=1>STM32H503</td><td rowspan=1 colspan=1>STM32H5</td><td rowspan=1 colspan=1>STM32H7R/S</td><td rowspan=1 colspan=1>STM32H72x/73x</td><td rowspan=1 colspan=1>STM32H74x/75x</td><td rowspan=1 colspan=1>STM32H7Ax/7Bx</td><td rowspan=1 colspan=1>STM32F7</td></tr><tr><td rowspan=1 colspan=1>Cortex core</td><td rowspan=1 colspan=1>Cortex-M33</td><td rowspan=1 colspan=1>Cortex-Mo+</td><td rowspan=1 colspan=1></td><td rowspan=1 colspan=2>Cortex-M33</td><td rowspan=1 colspan=2></td><td rowspan=1 colspan=1>Cortex-M7</td><td rowspan=1 colspan=1></td><td rowspan=1 colspan=1></td></tr><tr><td rowspan=1 colspan=1>RDP additionalprotection</td><td rowspan=1 colspan=1>RDP fourevels, backupreegisters, RAM</td><td rowspan=1 colspan=1>Backupreisters, RAM</td><td rowspan=1 colspan=1>RDP fourevels, backupreisters, RAM3</td><td rowspan=1 colspan=2>Product state instead ofRDP</td><td rowspan=1 colspan=1>Productsstatei nstead ofRDP backupSRAM</td><td rowspan=1 colspan=1>Backup RAM,backupregisters, OFDEC</td><td rowspan=1 colspan=1>BackupSA RAM,backupregisters</td><td rowspan=1 colspan=1>Backup RAM,backupreisters, OFDEC</td><td rowspan=1 colspan=1>Backup SRAM</td></tr><tr><td rowspan=1 colspan=1>Flash WRP</td><td rowspan=1 colspan=1>Up to fourprotectedaras withaK or4-bytey granularity</td><td rowspan=1 colspan=4>Two areas per bank defined by page range</td><td rowspan=1 colspan=1>By sectors(8 Kbytes)</td><td rowspan=1 colspan=2>By sectors (128 Kbytes)</td><td rowspan=1 colspan=1>By groupof 48-Kbysectors</td><td rowspan=1 colspan=1>By sectors 16K,,64 4K,128 K, or256 Kbytes)</td></tr><tr><td rowspan=1 colspan=1>SRAM WRP</td><td rowspan=1 colspan=1>SRAM2,with1-Kbytegranularity</td><td rowspan=1 colspan=1>No</td><td rowspan=1 colspan=3>SRAM2, with 1-Kbyte granularity</td><td rowspan=1 colspan=1>No</td><td rowspan=1 colspan=1>No</td><td rowspan=1 colspan=1>No</td><td rowspan=1 colspan=1>No</td><td rowspan=1 colspan=1>No</td></tr><tr><td rowspan=1 colspan=1>PCROP</td><td rowspan=1 colspan=1>No(replacedbyTrustZone</td><td rowspan=1 colspan=1>No</td><td rowspan=1 colspan=1>No(replacedbyTrustZone</td><td rowspan=1 colspan=1>No</td><td rowspan=1 colspan=1>No(replacedbyTrustZone</td><td rowspan=1 colspan=1>No</td><td rowspan=1 colspan=1>By areawith25-bytegranularity</td><td rowspan=1 colspan=2>By area with 256-bytegranularity, one area perbbank</td><td rowspan=1 colspan=1>By sectors</td></tr><tr><td rowspan=1 colspan=1>HDP</td><td rowspan=1 colspan=1>Up to twoecureide areas(HDP)inside theTrustZonesecuredomain</td><td rowspan=1 colspan=1>Yes, withsecondstageextension</td><td rowspan=1 colspan=1>Up to twoecureide areasHDP)inside ttheTustZonesecuredomain</td><td rowspan=1 colspan=3>3-stage temporal isolation, one perbank</td><td rowspan=1 colspan=3>Yes (secure user memory, with256-byte granularity)</td><td rowspan=1 colspan=1>No</td></tr><tr><td rowspan=1 colspan=1>Firewall</td><td rowspan=1 colspan=1>No(replacedbyTrustZone</td><td rowspan=1 colspan=1>No</td><td rowspan=1 colspan=1>No(replacedbbyTrustZone</td><td rowspan=1 colspan=1>No</td><td rowspan=1 colspan=1>No(replacedbyTrustZone</td><td rowspan=1 colspan=1>No</td><td rowspan=1 colspan=1>No</td><td rowspan=1 colspan=1>No</td><td rowspan=1 colspan=1>No</td><td rowspan=1 colspan=1>No</td></tr><tr><td rowspan=1 colspan=1>MPU</td><td rowspan=1 colspan=1>Yes</td><td rowspan=1 colspan=1>Yes</td><td rowspan=1 colspan=1>Yes</td><td rowspan=1 colspan=1>Yes</td><td rowspan=1 colspan=1>Yes</td><td rowspan=1 colspan=1>Yes</td><td rowspan=1 colspan=1>Yes</td><td rowspan=1 colspan=1>Yes</td><td rowspan=1 colspan=1>Yes</td><td rowspan=1 colspan=1>Yes</td></tr><tr><td rowspan=1 colspan=1>OTP</td><td rowspan=1 colspan=1>512 bytes</td><td rowspan=1 colspan=1>1 Kbyte</td><td rowspan=1 colspan=1>512 bytes</td><td rowspan=1 colspan=2>2 Kbytes</td><td rowspan=1 colspan=1>1 Kbyte</td><td rowspan=1 colspan=1>No</td><td rowspan=1 colspan=1>No</td><td rowspan=1 colspan=1>No</td><td rowspan=1 colspan=1>No</td></tr></table>

<table><tr><td rowspan=1 colspan=2>Feature</td><td rowspan=1 colspan=1>STM32L5</td><td rowspan=1 colspan=1>STM32U0</td><td rowspan=1 colspan=1>STM32U3ST32U5</td><td rowspan=1 colspan=1>STM32H503</td><td rowspan=1 colspan=1>STM32H5</td><td rowspan=1 colspan=1>STM32H7R/S</td><td rowspan=1 colspan=1>STM32 72x/73x</td><td rowspan=1 colspan=1>STM32H74x75x</td><td rowspan=1 colspan=1>STM32H7Ax/7Bx</td><td rowspan=1 colspan=1>STM32F7</td></tr><tr><td rowspan=1 colspan=2>UBE(1)</td><td rowspan=1 colspan=3>Yes (boot lock feature)</td><td rowspan=1 colspan=1>Yes</td><td rowspan=1 colspan=1>Yes</td><td rowspan=1 colspan=1>Yes (bootlockfeature</td><td rowspan=1 colspan=3>Yes (unique entry point in secureaccess)</td><td rowspan=1 colspan=1>No</td></tr><tr><td rowspan=1 colspan=2>Internal tamperdetection</td><td rowspan=1 colspan=1>Yes</td><td rowspan=1 colspan=1>Yes</td><td rowspan=1 colspan=1>Yes</td><td rowspan=1 colspan=1>Yes</td><td rowspan=1 colspan=1>Yes</td><td rowspan=1 colspan=1>Yes</td><td rowspan=1 colspan=1>Yes</td><td rowspan=1 colspan=1>Yes</td><td rowspan=1 colspan=1>Yes</td><td rowspan=1 colspan=1>Yes</td></tr><tr><td rowspan=1 colspan=2>Hardware crypto(2)</td><td rowspan=1 colspan=1>AES,HASH,KA</td><td rowspan=1 colspan=1>AES</td><td rowspan=1 colspan=1>AES,HASH,PKA</td><td rowspan=1 colspan=1>HASH</td><td rowspan=1 colspan=1>AES, ASH,OTFDEC,PKA</td><td rowspan=1 colspan=1>AES,HASH,PKA</td><td rowspan=1 colspan=3>AES, DES, HASH, OTFDEC</td><td rowspan=1 colspan=1>AES,HASH</td></tr><tr><td rowspan=1 colspan=2>RNG</td><td rowspan=1 colspan=7>SP 800-90-B</td><td rowspan=1 colspan=1>SP800-90-A(3)</td><td rowspan=1 colspan=1>SP800-90-B</td><td rowspan=1 colspan=1>SP800-90-A(3)</td></tr><tr><td rowspan=3 colspan=1>Seoe snmae</td><td rowspan=1 colspan=1>SBSFU</td><td rowspan=1 colspan=1>No</td><td rowspan=1 colspan=1>Yes</td><td rowspan=1 colspan=1>No</td><td rowspan=1 colspan=1>No</td><td rowspan=1 colspan=1>No</td><td rowspan=1 colspan=1>Yes</td><td rowspan=1 colspan=1>Yes</td><td rowspan=1 colspan=1>Yes</td><td rowspan=1 colspan=1>Yes</td><td rowspan=1 colspan=1>Yes</td></tr><tr><td rowspan=1 colspan=1>TF-M</td><td rowspan=1 colspan=1>Yes</td><td rowspan=1 colspan=1>No</td><td rowspan=1 colspan=1>Yes</td><td rowspan=1 colspan=1>No</td><td rowspan=1 colspan=1>Yes</td><td rowspan=1 colspan=1>-</td><td rowspan=1 colspan=1>No</td><td rowspan=1 colspan=1>No</td><td rowspan=1 colspan=1>No</td><td rowspan=1 colspan=1>No</td></tr><tr><td rowspan=1 colspan=1>KMS</td><td rowspan=1 colspan=1>No</td><td rowspan=1 colspan=1>No</td><td rowspan=1 colspan=1>No</td><td rowspan=1 colspan=1>No</td><td rowspan=1 colspan=1>Yes</td><td rowspan=1 colspan=1>-</td><td rowspan=1 colspan=1>No</td><td rowspan=1 colspan=1>No</td><td rowspan=1 colspan=1>No</td><td rowspan=1 colspan=1>No</td></tr></table>

Unique boot entry. For most devices with hardware crypto capability, there is a direct equivalent without it. RNG v2.0, can be used as a seed source for DRBG.

# 6.2

# Readout protection (RDP)

Theredout roecingloal smemo roeinallowiebeae pr against copy, reverse engineering, dumping,using debug tools, or code injection in SRAM.The user must e this protection after the binary code is loaded to the embedded flash memory.

The RDP applies to all STM32 devices for:

the main flash memory the option bytes (level 2 only)

Depending on the STM32 device, additional protections are available, including:

backup registers for real-time clock (RTC)   
backup SRAM   
Nonvolatile memories

![](images/98bd6bb0956268b4f1615821a1bbbd29162dcf61ed4aec1a95966159203b0d0f.jpg)  
Figure 8. Example of RDP protections (STM32L4 series)

# The RDP levels are defined as follows:

Level 0(default RDP level) The flash memory is fully open, and al memory operations are possible in ll boot configurations (debug features, boot from RAM, boot from system memory bootloader, boot from flash memory). There is no protection in this configuration mode that is appropriate only for development and debug.

# • Level 1

Flash memory accesses (read, erase, program), or SRAM2 accesses via debug features (such as serialwire or JTAG are forbidden, even while booting from SRAM or system memory bootloader. In these cases, any read request to the protected region generates a bus error.   
However, when booting from flash memory, accesses to both flash memory and to SRAM2 (from user code) are allowed.

# Level 2

All protections provided in Level 1 are active, and the MCU is fully protected.The RDP option byte and all other option bytes are frozen, and can no longer be modified. The JTAG, SWV (single-wire viewer), ETM, and boundary scan are all disabled.

A fourth RDP level is available for devices built on Armv8 architecture:

Level 0.5(for nonsecure debug only) All rd and writoperations no writ protection  et) om/tohe nonsecureash memory re possble. The debug access to secure area is prohibited. Debug access to nonsecure area remains possible.

# RDP level regression

RDP can always be leveled up. A level regression is possible with the following consequences:

Regression from RDP level 1 to RDP level 0 leads to a flash memory mass erase, and the erase of SRAM2 and backup registers.   
Regression from RDP level 1 to RDP level 0.5 leads to a partial flash memory erase: only the nonsecure part is erased.   
Regression from RDP level 0.5 to RDP level 0 leads to a flash memory mass erase, and the erase of SRAM2 and backup registers.

In RDP level 2, with exception of preconfigured OEM keys in STM32Ux series, no regression is possible.

# Internal flash memory content updating on an RDP protected STM32 MCU

In RDP level 1or , the fash memoy content can o longer be modifid with an exteral access (bootle booting from SRAM). However, modifications by an internal application are always possible. Practical implementations of such firmware updates are SFU (secure firmware update) and IAP (in-application-programming). See examples in related documents AN4657, AN5056, AN5544, and AN5447 to learn more.

# Regression locked by OEM keys

Te320an 2 rtduce he posbl eeect e (pasors) allocotrolled sonaple  ult naly oTeke proilr way gul byanallow ressin,hey eeepresnthedebuteacdeicte which prevents concurrent connection for normal debug session.

There are separate keys for regression from RDP2 and from RDP1.   
Regression is supported in the STM32CubeProgrammer utility both in GUI and CLI.

# The table below summarizes the RDP protections.

Table 14. RDP protections   
1Backup registers/SRAM   

<table><tr><td rowspan=2 colspan=1>Area</td><td rowspan=2 colspan=1>RDPlevel</td><td rowspan=1 colspan=3>Boot from user flashmemory</td><td rowspan=1 colspan=3>Debug or boot from SRAM or from bootloader</td></tr><tr><td rowspan=1 colspan=1>Read</td><td rowspan=1 colspan=1>Write</td><td rowspan=1 colspan=1>Erase</td><td rowspan=1 colspan=1>Read</td><td rowspan=1 colspan=1>Write</td><td rowspan=1 colspan=1>Erase</td></tr><tr><td rowspan=3 colspan=1>Flash main memory</td><td rowspan=1 colspan=1>0</td><td rowspan=1 colspan=1>Yes</td><td rowspan=1 colspan=1>Yes</td><td rowspan=1 colspan=1>Yes</td><td rowspan=1 colspan=1>Yes</td><td rowspan=1 colspan=1>Yes</td><td rowspan=1 colspan=1>Yes</td></tr><tr><td rowspan=1 colspan=1>1</td><td rowspan=1 colspan=1>Yes</td><td rowspan=1 colspan=1>Yes</td><td rowspan=1 colspan=1>Yes</td><td rowspan=1 colspan=1>No</td><td rowspan=1 colspan=1>No</td><td rowspan=1 colspan=1>No</td></tr><tr><td rowspan=1 colspan=1>2</td><td rowspan=1 colspan=1>Yes</td><td rowspan=1 colspan=1>Yes</td><td rowspan=1 colspan=1>Yes</td><td rowspan=1 colspan=1>N/A</td><td rowspan=1 colspan=1>N/A</td><td rowspan=1 colspan=1>N/A</td></tr><tr><td rowspan=3 colspan=1>System memory</td><td rowspan=1 colspan=1>0</td><td rowspan=1 colspan=1>Yes</td><td rowspan=1 colspan=1>No</td><td rowspan=1 colspan=1>No</td><td rowspan=1 colspan=1>Yes</td><td rowspan=1 colspan=1>No</td><td rowspan=1 colspan=1>No</td></tr><tr><td rowspan=1 colspan=1>1</td><td rowspan=1 colspan=1>Yes</td><td rowspan=1 colspan=1>No</td><td rowspan=1 colspan=1>No</td><td rowspan=1 colspan=1>No</td><td rowspan=1 colspan=1>No</td><td rowspan=1 colspan=1>No</td></tr><tr><td rowspan=1 colspan=1>2</td><td rowspan=1 colspan=1>Yes</td><td rowspan=1 colspan=1>No</td><td rowspan=1 colspan=1>No</td><td rowspan=1 colspan=1>N/A</td><td rowspan=1 colspan=1>N/A</td><td rowspan=1 colspan=1>N/A</td></tr><tr><td rowspan=3 colspan=1>Option bytes</td><td rowspan=1 colspan=1>0</td><td rowspan=1 colspan=1>Yes</td><td rowspan=1 colspan=1>Yes</td><td rowspan=1 colspan=1>Yes</td><td rowspan=1 colspan=1>Yes</td><td rowspan=1 colspan=1>Yes</td><td rowspan=1 colspan=1>Yes</td></tr><tr><td rowspan=1 colspan=1>1</td><td rowspan=1 colspan=1>Yes</td><td rowspan=1 colspan=1>Yes</td><td rowspan=1 colspan=1>Yes</td><td rowspan=1 colspan=1>Yes</td><td rowspan=1 colspan=1>Yes</td><td rowspan=1 colspan=1>Yes</td></tr><tr><td rowspan=1 colspan=1>2</td><td rowspan=1 colspan=1>Yes</td><td rowspan=1 colspan=1>No</td><td rowspan=1 colspan=1>No</td><td rowspan=1 colspan=1>N/A</td><td rowspan=1 colspan=1>N/A</td><td rowspan=1 colspan=1>N/A</td></tr><tr><td rowspan=2 colspan=1>Other protected assets</td><td rowspan=1 colspan=1>0</td><td rowspan=1 colspan=1>Yes</td><td rowspan=1 colspan=1>Yes</td><td rowspan=1 colspan=1>Yes</td><td rowspan=1 colspan=1>Yes</td><td rowspan=1 colspan=1>Yes</td><td rowspan=1 colspan=1>Yes</td></tr><tr><td rowspan=1 colspan=1>1</td><td rowspan=1 colspan=1>Yes</td><td rowspan=1 colspan=1>Yes</td><td rowspan=1 colspan=1>N/A</td><td rowspan=1 colspan=1>No</td><td rowspan=1 colspan=1>No</td><td rowspan=1 colspan=1>No</td></tr><tr><td rowspan=1 colspan=1></td><td rowspan=1 colspan=1>2</td><td rowspan=1 colspan=1>Yes</td><td rowspan=1 colspan=1>Yes</td><td rowspan=1 colspan=1>N/A</td><td rowspan=1 colspan=1>N/A</td><td rowspan=1 colspan=1>N/A</td><td rowspan=1 colspan=1>N/A</td></tr></table>

# When to use the RDP

On a consumer product, the RDP must always be set at least at level 1. This prevents basic attacks through thee por eo. Hoe iR herviu flash memory mass erase, following a return to RDP level 0.

The RDP level  s andatory implement an application with highersecurity level (uch as mutable de).   
Thedrawbackis that heD level can prevent deviexamiation, stanc r customeurn.

The RDP level 0.5 is used to debug a nonsecure application, while protecting contents within secure area boundaries from debug access. Refer to section 'Development recommendations using TrustZone®' of the application note Arm® TrustZone® features on STM32L5 and STM32U5 series (AN5347) for more information about this protection.

Note:

The RDP is availableon all STM32 device, unless succeeded by the liecycle management product state (ee Section 6.3).

# 6.3

# Lifecycle management—product state

The addition of RDP 0.5 into the RDP mechanism used by the STM32 enabled the necessary isolation between e nd onseue eveloment.However, he RDP does ot aow goig rthern the serexperene w the adoption of new development and OEM manufacturing models. The RDP has been replaced by the product stat amore eficycaageentystem,  he2 devics a a pilot projet.Te rodu ae rheeetinga haively ew a itallows them  peorm ressionihecnrollvoment sr povison was o the STM32U5 series, but the product state enabled finer control over delegating the debugging rights in To open and closed, for example, the STM32H7Rx/7Sx which implements the product state this way.

The new lecycanagement defi  eit sat n he possle nsin betweeheu as in the case of the RDP, but there are more states defined for the following:

Provision with immutable root of trust code.   
Clear separation of nonsecure and secure environment.   
Use certificates for controlled regression.   
Use certificates for temporary debug sessions.

For apliatins hat do ot nee thee ewptions,hee r il roduct statcondng thel RDP values.

The main available product states are:

Open: roughly equivalent to RDP 0   
Provisioning: marks an ongoing installation of iRoT   
iRoT-provisioned: roughly comparable to RDP 0.5   
TZ-closed: state in which debugging of nonsecure code is permitted   
Closed: equivalent of RDP2, but the regression is possible (only with a valid authorization)   
Locked: final state with no possibility of further transition (like RDP2)

# i.4 Unique boot entry

boot sequence from the intended progression. This is the goal of the unique boot entry or BOoT_LOCK.

The RDP2 on some products prevent booting from other memory. The BOOT_LOCK goes further by also working in RDP1 and working with the product state lie-cycle management. In some devices the BOOT_LOCK alows the possibility to lock the boot to a specific address.

Even if RDP2 is set; the unique boot entry provides additonal security assurance against glitch attacks.

A unique boot entry is available on STM32Ux, STM32Gx, STM32Hx, STM32Cx series, and in STM32WBA weeeviIplmentation det valableac evieerenceanual eectu boot configuration and flash.

# One-time programmable (OTP)

T any modification. It is usually a smaller area compared to the size of the user flash memory.

sliatga e siy put on reading written data.

# Note:

The OTP is available on most STM32 devices (refer to Section 2: Overview for more details).

# 6.6

# Boot and security control (BSEC)

On the STM32N6 series flashless microcontroller, the boot security and product state management are implemented using a large (12k) array of OTP fuses and data.

It is connected via core logic with debug interface, crypto, system bus, ST boot ROM, and clock control.

Thi ysallow trn potetinbuccen rdcacld o the external program memory.

The OTP nature means increased security compared to regular flash memory, with acceptable drawbacko lab oin p wus ca o other popular devices.

Boot security is implemented so that the STM32N6 always boots in the ST boot ROM, which uses the OTP settings to execute the boot progression in configured manner.

# 6.7 TrustZone®

Thi ctin desbesma ature rutZone® rhiectuorurthe oation, application note Arm® TrustZone® features on STM32L5 and STM32U5 series (AN5347), and to the device reference manual.

The Armv8-M TrustZone® architecture defines two domains at system level: secure and nonsecure. The full memory-map space  plit into secure ndnonsecueareas.his icluds al memor typs lash y, SRAM, and external memories), as well as all peripherals that can be shared (with specic context foreach domain) or dedicated to one domain or the other.

At system level, the isolation between secure and nonsecure domains relies on the following hardware mechanisms (see Figure 9):

speciic core architecture (Armv8-M Cortex-M33) with a dual execution domain for secure and nonsecure   
domains, and an implementation defined attribution unit (IDAU) to assert address range security status   
secure attribution unit (SAU) is used to refine settings of the IDAU   
bus infrastructure that propagates the secure and privilege attributes of any transaction (AHB5)   
dedicated hardware blocks managing the split between the two domains (GTZC to define security tribute   
for internal SRAMs and external FSMC/OCTOSPI memories, and peripherals)

![](images/1f7fc44ec190e7959c651c8460295832d18173d95ebed532d908a8241a031bd0.jpg)  
Figure 9. TrustZone® implementation at system level

# 6.7.1 Core state

The or ta depend  heregion he currnt ung codWhenhe code s rom  ecuen, the core is in secure state. Otherwise, the core is in nonsecure state.

# 6.7.2 Secure attribution unit (SAU)

T AU  har cuple  he o s he MPU)Te AU obleor tt ey atrut anactoneecurityruttrnactinfi yhergetd a memory-mapped resource memory areas or peripherals). Depending onthe AU configuration, an address is a s ecure, onsecurecallable S, ronsecure.TheS is a subdma he secure doman, a allows a gateway to be defined or nonsecure code to access the secure domain at a specific entry point.

T U gurable ycu ar. It an eonigur t boot  conguratinn e dynamically modified by a secure firmware.

# Note:

Ary atuot e  ce y rreu  >e default attribute set by hardware through an IDAU (implementation defined secure attribute). Refer to implementation details of each device in the reference manual.

# Address aliasing

The crttribut  depndng neercress.However meo-apesur ethe  secure onsecuredepending n the aplicatinTo overome thapparent contradicion, twoadresses are assigned to each memory-mapped resourceone used when the resource must be accessed in secure mode, one used in nonsecure mode. This mechanism is called address aliasing.

Tadres liasillows l phelcerueiy ogissteul scattered regions. Finally, the IDAU splits the memory-mapped resources in the following regions:

peripherals secure/nonsecure regions flash memory secure/nonsecure regions SRAM secure/nonsecure regions

Refer to device reference manual for the detailed configuration.

# Memory and peripheral protections

TU tares.he arge memors n periheralae protect yharware echaniss hat filrheas depending on the secure and privileged attributes.

There are two types of peripherals in the TrustZone® system architecture:

TrustZone-aware peripherals: connected directly to the AHB or APB bus, with a specific TrustZone® aviorsus ubscurgiT fontr cuinhe pl Securable peripherals: protected by an AHB/APB firewall gate controlled by the GTZC to define security properties

T  A , and others peripherals with a fundamental role within the system (PWR, RTC, system configuration). The remaining system peripherals are securable.

The GTZC defines the access state of securable peripherals, embedded SRAM, and external memories:

Peripherals can be set as secure or nonsecure (exclusively), privileged or unprivileged using TZSC.   
Embedded SRAM is protected by blocks of 256 bytes through the MPCBB.   
External memories are protected by regions (watermark: start and length). The number of protected regions depends on the memory types (NAND, NOR, or OCTOSPI).   
Illegal access events lead to secure interrupts generated by TZIC.

Note:

The flash memory security aribute is definedthrough secure watermark option bytes, and/or fash memory interface block-based registers.

# 6.8

# Flash memory write protection (WRP)

T   e For flash memory technology, an update must be considered as filling with zeros.

Foan r    p  feo  evn during a firmware or data update. It can also be set by default on the unused memory area to prevent any malware injection. Its granularity is linked to the page or sector size.

# When to use the WRP

T protecon must i particular when wriatin re with heplicat the case if data storage or code update operations are expected. The WRP prevents wrong accesses due to unsafe functions causing unexpected overflows.

Note:

The WRP is available on all STM32 devices with internal flash memory.

# 6.9

# Execute-only firmware (PCROP)

e as yu witeunlueastore conigured area can only be fetched by the CPU instruction bus.Any atempt to reador write his area is foiden.The protection applies against both internal (firware) accesses as wel as external debug ort) accesses. In an STM32 device, this feature is named proprietary code readout protection (PCROP).

The PCROP is a static protection set by option bytes. The number of protected areas and their granularity depends on the STM32 device (see Section 6.1.: Security features by STM32 devices). When the PCRP isn uk. Refer to the document [3] for more details.

I vu pant pal the protection.

# When to use the PCROP

T   hi-r ee  e eos the user firmware.

Note:

The PCROP is available on all STM32 devices listed inTable except onTrustZone-nabled devices, h t is superseded by another protection mechanism.

# 6.10

# Secure hide protection (HDP)

Some STM32 devices support the HDP memory concept. The HDP, named secure hide protection on STM32LE devices, is also known as secure user memory on STM32H7 devices, or securable memory on STM32G0 devices.

An HD ar par fheusr fash emoyhat can eonyonce, st t devicre. e HDP targets sensitive applications that embed or manipulate confidential data, and that must be securely e t bo.ncernsi eu he  ari osacnot ea y any means (see the figure below).

The cod that faciltates he HDP transitonsually  TMicroelectronic cod locate in heRSS.d SRAM is an alternative.

![](images/4ec665989699d6f435419e14c668e2e6694e732c84778203cedc6f01a974d15b.jpg)  
Figure 10. HDP protected firmware access

THDP sa stat protecn conigur y ptn by.Onc t, ePU boots  hea r idependen heboot cuatin  y boot boo dres. cn  gle use a monotonic counter to gradually cover more memory as the secure boot progresses (STM32H5). Some devices implement a dynamic HDP expansion. This means that the HDP can be extended by the number of sectors using the register value, without programming the OB (STM32H5, STM32U0).

# When to use the HDP

T used in synergy with the boot lock feature.

Note:

The HDP is available in STM32H7, STM32G0, STM32G4, STM32L5, STM32N6, STM32U0, STM32U5, and STM32H5 devices, with slight diffrences in its implementation and name (refer to the reference manuals for details).

# 6.11 Firewall

T particular areas:a code are (lashmemory, avolatil data area (SRAM)and aovolatildata arelas memory). The protected code is accessible through a single entry point (the call-gate mechanism explaied through the entry point, generates a system reset.

all i  poI    ar ape pln.

# Call gate mechanism

T a toeee poewl.  he rote  wt passi tal gateeanihe  ystm reserateanyistrctintheutsie he pr area, the firewall is closed (see the figure below).

![](images/d977de45e4f5ae45836c34770d19516fa411cf424bc732f1b92c6571219c066d.jpg)  
Figure 11. Firewall FSM

Since the only way to respect the call gate sequence is to pass through the single call gate entry point, amans latialul unprotected code area (such as encrypt and decrypt functions). A parameter can be used to specify which fuon to execue (such a al1Ga1IDrCal1GatFID).Accordig o the parameer, theht function is internally called. This mechanism is represented in the figure below.

![](images/3c5bfb250da2cc31c29d0e47090a636579e0909a76aaf7d526279014e13df08f.jpg)  
Figure 12. Firewall application example

# When to use the firewall

The firewl protects both code and data. The protected code can always be called as long as a call gate mechanism is respected.

Note:

A firewall is available on STM32L0 and STM32L4 devices only. Refer to the application note AN4730 for more details. The firewall functionality is replaced by TrustZone.

# 6.12

# Memory protection unit (MPU)

The MPU is a memory protection mechanism that allows specific access rights to be defined for amemory-mappe resourcef thedevicefash memory, SAM, and peripheral registersThis protecion is dynamically managed at runtime.

# Note:

MPU attributes are only set for CPU access. Other bus master requests (such as DMA) are not filtered by the MPU, and must be deactivated if they are not needed.

# Region access attributes

The MPU spli theemory map into several regions,ach havig wn access attributeAccess right n e set as executable, not executable(XN), read-write (RW), read only (RO), or no access.

# Note:

There are other attributes set by the MPU for each region: shareable, cacheable, and bufferable. This aliatinos ot covrhewholplexiheThis ctn poviesnytruct high-level overview. Refer to applicable programming manual, or to the document [5].

# Privileged and unprivileged modes

On  thesattbue, eArmCorearitudefis two eeuonmodes alloig  p vvodorgne ttte for each mode.

The table below shows the different cases supported by mixing modes and access attributes.

Table 15. Attributes and access permission managed by MPU   

<table><tr><td rowspan=1 colspan=1>Privileged mode attribute</td><td rowspan=1 colspan=1>Unprivileged mode attribute</td><td rowspan=1 colspan=1>Description</td></tr><tr><td rowspan=1 colspan=2>Execute never (XN)(1)</td><td rowspan=1 colspan=1>Code execution attribute</td></tr><tr><td rowspan=1 colspan=1>No access</td><td rowspan=1 colspan=1>No access</td><td rowspan=1 colspan=1>All accesses generate a permission fault.</td></tr><tr><td rowspan=1 colspan=1>RW</td><td rowspan=1 colspan=1>No access</td><td rowspan=1 colspan=1>Access from a privileged software only</td></tr><tr><td rowspan=1 colspan=1>RW</td><td rowspan=1 colspan=1>RO</td><td rowspan=1 colspan=1>Written by an unprivileged software generate a permission fault.</td></tr><tr><td rowspan=1 colspan=1>RW</td><td rowspan=1 colspan=1>RW</td><td rowspan=1 colspan=1>Full access</td></tr><tr><td rowspan=1 colspan=1>RO</td><td rowspan=1 colspan=1>No access</td><td rowspan=1 colspan=1>Read by a privileged software only</td></tr><tr><td rowspan=1 colspan=1>RO</td><td rowspan=1 colspan=1>RO</td><td rowspan=1 colspan=1>Read only, by privileged or unprivileged software</td></tr></table>

l

The code executed in privileged mode can access aditional specific instructions (MRS), and can also access Ar® core peripheral registers (such as NVIC, DWT, or SBC). This is useful for OS kernes or pieces f ecure code requiring access to sensitive resources that are otherwise inaccessible to unprivileged firmware.

# Secure process isolation strategy

voheeu y l .Te e  oat ec pro uc   kee, eyane )se untrusted processes (user applications).

Table 16. Process isolation   

<table><tr><td rowspan=1 colspan=1>Firmware type</td><td rowspan=1 colspan=1>Mode</td><td rowspan=1 colspan=1>Resources access</td></tr><tr><td rowspan=1 colspan=1>Secure firmware (such as SB or OS kernel)</td><td rowspan=1 colspan=1>Privileged</td><td rowspan=1 colspan=1>Full access</td></tr><tr><td rowspan=1 colspan=1>All remaining firmware</td><td rowspan=1 colspan=1>Unprivileged</td><td rowspan=1 colspan=1>MPU controlled access: no access, RO, RW</td></tr></table>

An OS kernel can manipulate MPU attributes dynamically to grant access to specific resources depending on the currently unning task.Access right can beupdated each time the OS switches rom one task toanohe

# When to use the MPU

The MPU is used at runtime to isolate sensitive code, and/or to manage access to resources depending on systems that incorporate security in their design.

Note:

The MPU is available on all STM32 devices except the STM32F0 (see the various programming manuals for more details).

# 6.13

# Resource isolation framework (RIF)

T p atal a eviI icapaleiplentvarus le olatin betwe aplication coeata erce n  multi-tenant secure OS.The RIF is complementing herustZone® system  AU/DAU isolat rules, known from other devices.

The configuration is volatile and set during the secure boot, and then fixed in place until next boot.   
In STM32N6, the RIF consists of RIFSC, RISAF and IAC parts.

# 6.14 Customer key storage (CKS)

ST32WB series are dual-core devices with one core (CPU1) for user application, and another core (CPU2) icatheieles al-iepeeecuin the ButothLoerg ZiBere ool). The flash memory used by CPU is isolate from the CPU1orexternal access.Communication between he wo cores is ensured by a mailbox and an interprocess channel control hardware block (IPCC).

Ine h wi a dedicated Aardwae periheral e Figu.eEkey egiste s cessible nly  heU, preventing access to the key by an untrusted process running on the CPU1, or by the debug port.

After the keys have been provisioned inside the secure area, the user application can use them by calng a secure load service with an index referencing the key and no more the key itself.

![](images/106fd44799e68c5d920ed9d3a9f2ec9250c004205cb11a2325524c76ec4738c2.jpg)  
Figure 13. Dual-core architecture with CKS service

# When to use the CKS

The CKS must be used when a user application reles on AES encryption or decryption. Provisioned keys can be stored in a secure area, so that no other internal process or external access can read their value.

Note:

The CKS is available on STM32WB series only.

# 6.15 Option byte keys (OBK)

Option bye keys are secure, nonvolatile storage intended or the protection of keys,specifically trage encryption keys. First introduced on the STM32H5, option byte keys are linked to a multilevel HDP boot progression. Each HDPL value increment closes access to keys used by lower levels, aiding in the implementation of a true secure boot.

The OBK was revised or the STM32H7RS where it is used for the same purpose, but with improvd mechanisms of OBK storage management.

OB is lnked to usage of SAES and in some cases, neverallows the actual key to be revealed outside the hardware storage (hardware keys).

(The OBK is included in STM32H5 and STM32H7R/S)

# Antitamper (TAMP)/backup registers (BKP)

The antitamper is a system level protection, used to detect physical tampering attempts on the system. Aetealtmpvenetet vetrstionedicatvi Intealtamns volaatuccvnt answakeherak actions (such as memory erase or alarm).

TTA perheral incles backupiser witcntent preerve bBAalog wit e al-timc (RTC). These registers can be reset if a tamper attempt is detected.

On me TM32 devices, this peripheral is known s backup registers (BP).On recent devices, has eolvd with additional features, such as monotonic counter, or secure section for TrustZone® secure area.

# When to use the antitamper

It must be used for system intrusion detection (in consumer products sealed enclosures for example).   
The monotonic counter is a countermeasure against tampering with the RTC.

# Note:

The external tamper detection is available on ll STM32 devices. More information about tamper functionality usage is available, for example, in AN4759.

# 6.17

# Clock security system (CSS)

Tl u is intentional or ot. In any case, the device must takeappropriate actions to recover.The  triggers an interrupt to the core in such event.

If teexteral clock soure rives themain system clock, te swithes the system t aninternal coc source.

# When to use the CSS

The CSS must be used when an external clock is used.

Note:

The CSS is available on all STM32 devices.

# 6.18

# Power monitoring (PVD)

Ste pla lo  wespplytotept ezeeevi atrrs e memory content.

The STM32 devices embed a programmable voltage detector (PVD) that can detect a drop of power. The PVD allows the configuration of a minimum voltage threshold, below which an interrupt is generated, so that appropriate actions are implemented.

# When to use the PVD

Tu  oil working memory (SRAM). A memory cleaning can be launched in case of power down detection.

# Note:

The PVD is available on all STM32 devices.

# 6.19

# Memory integrity hardware check

The error code correction (ECC) and parity checks are safety bits associated to the memory content:

. The ECC is associated to thememory words, used to recover from a single-bit error, or to detect up to two erroneous bits on each flash memory or SRAM word (32- to 256-bit word depending on the memory type). Refer to the AN5342 for more details.

A simple parity check allows the detection of a single error bit on the SRAM words where ECC is not implemented.

# When to use ECC and parity check

ECC and parity checks are mostly used or safety reasons. The ECC can also be used to prevent some invasive hardware attacks.

Note:

This integrity protection is available on all devices except STM32F1 and STM32L1. STM32H7 devices are champion in ECC protection.

# 6.20

# Independent watchdog (IWDG)

Th IDothat ne ystm e wheo veutvalen provolutalisloc e Wcce eows clockShaaactivevenh of a main clock failure.

# When to use the IWDG

T IG an eus reakdeloks Ian lo e s cnol ecume cal coe decryption or flash memory programming).

Note:

The IDWG is available on all STM32 devices.

# 6.21 Device ID

Eaevnt oival cevi These bits can never be altered by the user.

Tvn from a master OEM key.

# 6.22 Cryptography

As described in Section 5, cryptography is essential to secure an embedded system.The cryptography enables elih series include products with hardware cryptography peripherals. These peripherals allow cryptographic computations (such as hashing or symmetric algorithms) to beaccelerated. For devices with no such secii acratchtLp of a large set of cryptographic algorithms.

T  l second number or letter after the series identifier. For example the STM32L486 and STM32H7B3 devices have crpthardware while heTM32L476and STM32H7A3 have  use software librarymplement cryptogrpy and it can be known by their naming.

# 3.22.1 Hardware accelerators

The following cryptographic peripherals are available in STM32 devices:

TRNG (true random generator)

hardware-based peripheral providing a physical noise source. Used to feed a DRNG with a seed, or directly for random numbers, depending on device. Note: For details about the RNG validation, refer to the application note 'STM32 microcontroller random number generation validation using the NIST statistical test suite' (AN4230).

AES accelerator

encryption/decryption   
128- or 256-bit keys   
several modes of operation (such as ECB, CBC, CTR, or GCM)   
DMA support

Note: When the AES is used for encryption or decryption, the access to its registers containing the ke must be protected and cleaned after use (the MPU can be configured to restrict access to memory wi keys).

PKA accelerator

acceleration of RSA, DH, and ECC over GF(p) operations, based on the Montgomery method for fast   
modular multiplications   
built-in Montgomery domain inward and outward transformation

HASH accelerator

MD5, SHA1, SHA224, SHA256 FIPS compliant (FIPS Pub 180-2) DMA support

Note:

Many low-power STM32 devices feature hardware cryptography accelerators. The amount of energy needed to completcryptographic computations with them is lower than themount energy requird to treat them vi software processing.

# 6.22.2 CryptoLib software library

Th STM32 X-CUBE-CRYPTOLIBsotwa librar runs o  TM32 devics. I is vailable o ewn wt.co/n/product/-cubecptoleersinsvailablewitufapleentatnci for Cortex-M0, Cortex-M0+, Cortex-M3, Cortex-M33, Cortex-M4, and Cortex-M7.

The X-CUBE-CRYPTOLIB supports the following algorithms:

DES, 3DES with ECB and CBC   
AES with ECB, CBC, OFB, CCM, GCM, CMAC, KEY wrap, XTS   
Hash functions: MD5, SHA-1, SHA-224, SHA-256, SHA-384, SHA-512   
Other: ARC4, ChaCha20, Poly1305, Chacha20-Poly1305   
RSA signature with PKCS#1v1.5   
ECC with key generation, scalar multiplication (basis of ECDH) and ECDSA + ED25519 and Curve 25519

# On-the-fly decryption engine (OTFDEC)

etea meo ontnt de aot  o wdal /wr to protect the content is to encrypt and decrypt it inside the device before using it.

On olutio  ownld he exteal memoycontent insie heSRAM,decrypteecut hede, y and it uses a large amount of SRAM, depending on the content.

ThODEC perphealfr he possibl decypt hcntentey wit ao-atenc penaya witou he need r RAMallocatin.heEdecrypts heon-the usrafbase o hereaduest address information. It is used with the Octo-SPI interface (see the figure below).

![](images/df7d97bf63d1f1bc4297fa8b924b273601604bd19406114214beeab068d54e46.jpg)  
Figure 14. Typical OTFDEC configuration

The OTFDEC uses the AES-28 CTR mode, with a 128-bit key to achieve a latency below 12 system bus cycles. Up to four independent and nonoverlapping encrypted regions can be defined (4-Kbyte granularity), each with its own key.

# When to use the OTFDEC

The OTFDEC is used when an external memory is used by the system. For TrustZone® capable MCUs, the decryption keys can only be made accessible through the secure mode. See the application note How to use OTFDEC for encryption/decryption in trusted environment on STM32H73/H7B MCUs (AN5281) for more details.

The OTFDEC is available on STM32H5, STM35H7, STM32L5, and STM32U5 devices only.

# 6.24

# Memory crypto engine (MCE)

The memory crypto engine feature replaces theOTFDECin selecte products, specifically those with it internal memory and designed to use mainly external memory.

The differences are summarized in the following table.

Table 17. Features of the OTFDEC compared with the MCE   

<table><tr><td rowspan=1 colspan=1>Feature</td><td rowspan=1 colspan=1>OTFDEC</td><td rowspan=1 colspan=1>MCE</td></tr><tr><td rowspan=1 colspan=1>Function</td><td rowspan=1 colspan=1>On-the-fly decryption</td><td rowspan=1 colspan=1>Encryption and decryption</td></tr><tr><td rowspan=1 colspan=1>Algorithm</td><td rowspan=1 colspan=1>AES-based stream + proprietary</td><td rowspan=1 colspan=1>AES stream, AES block, DPA resistant</td></tr><tr><td rowspan=1 colspan=1>Key management</td><td rowspan=1 colspan=1>128b key per region, TZ protection, writeonnly</td><td rowspan=1 colspan=1>Similar, usually tied to OBK by thesoftware logic</td></tr><tr><td rowspan=1 colspan=1>Latency</td><td rowspan=1 colspan=1>Maximum of 12 cycles</td><td rowspan=1 colspan=1>11 to 36 cycles (scalable security)</td></tr><tr><td rowspan=1 colspan=1>Security</td><td rowspan=1 colspan=1>Base level</td><td rowspan=1 colspan=1>Including tamper and secure bootintegration</td></tr><tr><td rowspan=1 colspan=1>Integration</td><td rowspan=1 colspan=1>Associated with XSPI</td><td rowspan=1 colspan=1>Associated with memory subsystem,usable with FMC</td></tr></table>

# (The MCE is included in STM32H7Rx/7Sx)

# 7 Guidelines

Secure systems can take advantagemany security supporting hardware feature.Some areuseful r any RDP   y selected depending on user application and the required security level.

Ti sectionheldefining he daptesecurityatursependin he ysteuscas.euc r gathered in four main groups: protection againstexternal () and internal () threats, urity maintenance (3), and other use-cases related to cryptography (4) (see the table below).

Table 18. Security use cases   

<table><tr><td rowspan=1 colspan=2>1 Device protection against external threats: RDP protection, tamper detection, device monitoring</td></tr><tr><td rowspan=10 colspan=1></td><td rowspan=1 colspan=1>1.1 Device configuration (option bytes, not supposed to be modified ever)</td></tr><tr><td rowspan=1 colspan=1>Use RDP level 2. This closes the device from any external access.</td></tr><tr><td rowspan=1 colspan=1>1.2 Remove debug capability for the device.</td></tr><tr><td rowspan=1 colspan=1>Use RDP level 2 for permanently disabling the debug.</td></tr><tr><td rowspan=1 colspan=1>1.3 Protect a device against a loss of external clock source (crystal).</td></tr><tr><td rowspan=1 colspan=1>Enable clock security system (CSS).</td></tr><tr><td rowspan=1 colspan=1>1.4 Detect a system-level intrusion.</td></tr><tr><td rowspan=1 colspan=1>Use tamper detection capability of the RTC.</td></tr><tr><td rowspan=1 colspan=1>1.5 Protect a device from code injection.</td></tr><tr><td rowspan=1 colspan=1>Use the RDP.Isolate communication port protocol with the MPU, firewall, or HDP.Limit communication port protocol access range.Use write protection on empty memory areas (flash memory and SRAM).</td></tr></table>

2. Code protection against internal threats: TrustZone, PCROP, MPU, firewall, and HDP

<table><tr><td>2.1 Protect the code against cloning.</td></tr><tr><td>Use RDP level 1 or 2 against external access.</td></tr><tr><td>Use PCROP on most sensitive parts of the code against internal read access.</td></tr><tr><td>Use OTFDEC to secure code stored in the external memory.</td></tr><tr><td>2.2 Protect secret data from other processes.</td></tr><tr><td>Use firewall to protect both code and data.</td></tr><tr><td>Use MPU to protect secret data area from being read.</td></tr><tr><td>Use HDP in case data must only be used at reset.</td></tr><tr><td>Use secure domain of TrustZone, if available.</td></tr><tr><td>2.3 Protect code and data when not fully verified or trusted libraries are used.</td></tr><tr><td></td></tr><tr><td>Use PCROP to protect user most sensitive code. Use firewall to protect user sensitive application (code, data and execution).</td></tr><tr><td>Use MPU and de-privilege the untrusted library.</td></tr><tr><td>Use IWDG to avoid any deadlock.</td></tr><tr><td>Use secure domain of TrustZone, if available.</td></tr><tr><td></td></tr></table>

# 3. Device security check and maintenance: integrity checks, SB, SFU

3.1 Check code integrity.

Hash firmware code at reset and compare to expected value. Enable ECC on the flash memory and parity check on the SRAM

3.2 Security checks or embedded firmware authentication

Implement SB application with cryptography.   
Protect SB application secret data (refer to previous sections).

<table><tr><td></td><td></td><td>Guarantee unique boot entry on SB application: Use HDP if available.</td></tr><tr><td></td><td colspan="2">Use RDP level 2 and disable boot pin selection.</td></tr><tr><td></td><td>3.3 Securely update the firmware in the field.</td><td>Implement a SFU application with cryptography.</td></tr><tr><td></td><td>Apply relevant secure memory protection around the SFU secret data (refer to previous sections).</td><td></td></tr><tr><td colspan="2">4. Communication and authentication: cryptography</td><td></td></tr><tr><td></td><td>4.1 Communicate securely.</td><td></td></tr><tr><td></td><td>(such as TLS for Ethernet)</td><td>Use or implement secure communication stacks relying on cryptography for confidentiality and authentication</td></tr><tr><td></td><td></td><td>4.2 Use the ST AES/DES/SHA cryptographic functions with STM32 devices.</td></tr><tr><td></td><td>•</td><td>Use only official software implementation by ST with STM32 X-CUBE-CRYPTOLIB.</td></tr><tr><td></td><td>4.3 Accelerate AES/DES/SHA cryptographic functions.</td><td></td></tr><tr><td></td><td>Use OTFDEC to access AES-ciphered code in the external memory without latency penalty.</td><td>Use device with cryptographic hardware peripheral together with official STM32 X-CUBE-CRYPTOLIB.</td></tr><tr><td>•</td><td>4.4 Generate random data.</td><td></td></tr><tr><td></td><td>Use RNG embedded in the STM32 devices.</td><td></td></tr><tr><td>•</td><td>4.5 Uniquely identify ST microcontrollers.</td><td></td></tr><tr><td></td><td>Use STM32 96-bit unique ID.</td><td></td></tr><tr><td></td><td>4.6 Authenticate a product device.</td><td></td></tr><tr><td></td><td></td><td>Embed a shared encryption key in the device, and exchange encrypted message.</td></tr><tr><td></td><td>4.7 Uniquely authenticate a device.</td><td></td></tr><tr><td></td><td></td><td>Embed a device private key and its certificate in the device, and exchange encrypted message.</td></tr><tr><td></td><td>4.8 Authenticate communication servers.</td><td></td></tr><tr><td></td><td></td><td></td></tr><tr><td></td><td>Embed a shared encryption key in the device, and exchange encrypted message. Embed server public key in the device, and exchange encrypted message.</td><td></td></tr></table>

# 8 Conclusion

N stenma ecre ysply ablig ecury atureararSecuriy mus in the architecture of the complete solution.

The treatsmust bedenti he conteeasures correctlydesign and implementin synergy wi security features.

As security demands considerable resources, it isimportant to correctly evaluate the risks, and spend the resources efficiently, keeping in mind the cost of attack and the value of the protected asset.

T aliz attempting to apply security ad hoc.

With the STM32 microcontrollers, the embedded and loT security is very cost-effective and robust.

# Appendix A Cryptography - Main concepts

# Integrity, authentication, and confidentiality

The objectives of cryptography are threefold:

Confidentiality: protection of sensitive data against unauthorized read accesses Authentication: guarantee of the message sender identity Integrity: detection of any message corruption during transmission

To meet these objectives, ll secure data flows rely on more or less complex combinations of the below algorithms:

Secret key/symmetric cryptography Public key/asymmetric cryptography Hashing

These algorithms are described in this appendix.

# A.1

# Secret key algorithms

Tfmsuentialiyhe at wi ha t used for ciphering and deciphering.

![](images/f63bd922f90fffeffbb402aea5336da1b0c0634e6f1a8d5f837f61e1ae0c7529.jpg)  
Figure 15. Symmetric cryptography

The iherent weakness  thesagoriths is hekey harig between bot par. It may ot e viet  aacur lant t whe o paristanhekeyane a challenge.

Among all secret key algorithms, block-based algorithms are very common since they can be efficiently accelerated by hardware or software parallel implementations. Typical AES (advanced encryption standard agorithms operate on clear blocks of 8 bis.They produce ciphered blocks f the same length using keys r bisThe different ways to chai consecutive blocks ae call "mode eatins" T include cipher block chaining (CBC), counter mode (CTR) and Galois counter mode (GCM).

Seo ieyayuvan only for one session as initialization vector.

# A.2

# Public key algorithms (PKA)

Tca pye iatvawi asymmetric (asymmetric cryptography):

A message encrypted by the private key can be read by any party with the public key. This mechanism ensures a strong authentication of the sender since the private key has never been shared. Digital signatures are based on this mechanism.

![](images/ef11761111d6787a46189eb7c2fc09145052b1f48be9bee561ecf7e0518cb327.jpg)  
Figure 16. Signature

A message encrypted by the public key can only be read by the private key owner.

![](images/4feb5b1287962a45da3565ab1183c7c606674bc183e9cf6331f4862d3ac22677.jpg)  
Figure 17. PKA encryption

Temai publicy  uiato olvehe ey harg symmetric cryptography. However, this comes at he cost fmore complex operations, increase computation time and bigger memory footprint.

RSA and elliptic curve cryptography (ECC) are the most common asymmetric algorithms.

# Hybrid cryptography

Comon secure transer protocols such as Bluetoth and TL) rely on both algorithm types.This schme is known as hybrid cryptography:

apyha is exchanged by the public key owner to the private key owner. Transfer confidentiality is then provided by a symmetric algorithm using the session key.

# A.3

# Hash algorithms

Hasagori uaranteeesagntegryheygneratniqu-ng treamromm callhegestiffenchee o totally iffent tTei reversed to retrieve the input message.

Hashing can be used independently from message encryption.

![](images/998198a853dc37df61da1ee2bf13ddb94a9b49581adf7315db6ea469567d6c1c.jpg)  
Figure 18. Message hashing

Thedifrence wi classR is therbustness e erations hat e moe coplex an amuche diget length: up to2 bits instead of 16or 32 bits.s a example,CRCare reserved r fast integrity ec during data transfers. Digest length makes them virtually unique and ensures that no collision occurs.

Typical algorithms are the MD5 (128-bit digest), SHA-1 (160-bit digest), SHA-2 (224-, 256-,384, or 512-bit digest), and SHA-3 (224-, 256-, 384-, or 512-bit digest).

# MAC or signature and certificate

# MAC and signature

The message authentication code (MAC) and the signature ad authentication to integrity by encrypting the message hash. The difference between MAC and signature is that the MAC generation uses a symmetric key algorithm (Figure 19), while the signature uses the message sender private key (Figure 20).

The signature adds non-repudiation dimension to authentication:

A private key is ot supposed tobe evoked ts lfetime goes beyond thetranser peration), whilea et key may have a limited lifetime (limited to this transfer). The private key used for signature is never shared, its security is higher than a secrete key.

![](images/906745cf12ccf05394718aabe7239c27c871dabf8902fd18b5b708b7d13beaa6.jpg)  
Figure 19. MAC generation with secrete key algorithm

![](images/e8fa9fbe6fff0e238496e2c7da49d84dce26ac1ff497aa11c4fff9515365feaa.jpg)  
Figure 20. Signature generation with public key algorithm

# Certificate

in e public ky ned by a certiateauthority CA) private key.This  i cnsidere s fully.

In addition to the public key, the certificate also contains version numbers,validity period and some IDs.

# Revision history

Table 19. Document revision history   

<table><tr><td colspan="3" rowspan="2">Date       Version                                                    Changes</td></tr><tr><td colspan="1" rowspan="1">Date</td><td colspan="1" rowspan="1">Version</td></tr><tr><td colspan="1" rowspan="1">17-Oct-2018</td><td colspan="1" rowspan="1">1</td><td colspan="1" rowspan="1">Initial release.</td></tr><tr><td colspan="1" rowspan="1">25-Feb-2019</td><td colspan="1" rowspan="1">2</td><td colspan="1" rowspan="1">Updated:Table 1. Applicable productsSection 1 General informationTable 11. Security features for STM32H7, STM32G0, STM32G4 and STM32WB SeriesFigure 9. Example of RDP protections (STM32L4 Series)Section 6.6 FirewallAdded:Section 6.8 Cryptographic key storage (CKS)</td></tr><tr><td colspan="1" rowspan="1">7-Oct-2019</td><td colspan="1" rowspan="1">3</td><td colspan="1" rowspan="1">Updated:Table 1. Applicable productsSection "Introduction" renamed "Overview"Table 2. GlossarySection "Hardware protections" renamed "Device protections"Figure 4. Memory typesTable 5. Memory types and associated protectionSection 4.2.4 External Flash memoriesTable 6. Scope of STM32 embedded memories protection featuresTable 7. Software isolation mechanismSection 4.5 Boot protectionSection 5 Secure applications: Table 9, Table 10 and Table 11Section 6.2 Readout protection (RDP)Section 6.7 Secure hide protection (HDP)Section 6.17 CryptographySection 7 GuidelinesSome colors removed on all figuresAdded:Section 4.1 TrustZone® for Armv8-M architectureSection 6.4 TrustZoneSection 6.18 On-the-fly decryption engine (OTFDEC)</td></tr><tr><td colspan="1" rowspan="1">21-Feb-2020</td><td colspan="1" rowspan="1">4</td><td colspan="1" rowspan="1">Updated Section IntroductionAdded acronyms in Table 2. GlossaryUpdated Section 2 Overview and Section 3 Attack typesRestructured Section 3.4 loT system attack examples (added Section 3.5 List of attack targets)Updated Section 4 Device protectionsUpdated and restructured Section 5 Secure applicationsAdded Section 5.3 Arm TF-M solutionUpdated Section 6 STM32 security features, Section 7 Guidelines and Section 8 Conclusion</td></tr><tr><td colspan="1" rowspan="1">06-Nov-2020</td><td colspan="1" rowspan="1">5</td><td colspan="1" rowspan="1">Updated:Document's scope to add STM32WL SeriesTable 1. Applicable productsSection 1 General informationSection 3.1 Introduction to attack typesSection 3.2 Software attacksSection 3.3.1 Non-invasive attacks</td></tr><tr><td colspan="1" rowspan="1">Date</td><td colspan="1" rowspan="1">Version</td><td colspan="1" rowspan="2">ChangesUpdated:Section 3.3.2 Silicon invasive attacksSection 4.1 TrustZone® for Armv8-M architectureTable 5. Memory types and associated protectionSection 5.3 Arm TF-M solutionTable 8. Basic feature differencesSection 6.1 Security features overview including updates in all the tablesSection 6.2 Readout protection (RDP)Section 6.4 TrustZoneAdded:Section 4.2 Dual-core securitySection 6.3 One-time programmable (OTP)</td></tr><tr><td colspan="1" rowspan="1">06-Nov-2020</td><td colspan="3" rowspan="1">5 (cont'd)</td></tr><tr><td colspan="1" rowspan="1">07-Jul-2021</td><td colspan="1" rowspan="1">6</td><td colspan="1" rowspan="1">Updated:Document's scope to add STM32U5 SeriesTable 1. Applicable productsSection 3.3.1 Non-invasive attacksSection 4.3.3 Embedded SRAMSection 4.3.4 External Flash memoriesSection 5 Secure applicationsTable 9. Security features for STM32Fx SeriesTable 10. Security features for STM32Lx and STM32U5 SeriesTable 11. Security features for STM32H7, STM32G0, STM32G4, STM32WB and STM32WL SeriesSection 6.3 One-time programmable (OTP)Section 6.6 Execute-only firmware (PCROP)Section 6.8 FirewallSection 6.9 Memory protection unit (MPU)Section 6.17 CryptographySection 6.17.1 Hardware acceleratorsSection 6.17.2 CryptoLib software libraryAdded:Section 5.4 Product certifications</td></tr><tr><td colspan="1" rowspan="1">13-Jan-2023</td><td colspan="1" rowspan="1">7</td><td colspan="1" rowspan="1">Updated:Document scope to add STM32C0 and STM32H5 SeriesSection 1 General informationDebug port access and SCA in Section 3.3.1 Non-invasive attacksRandom number generation and Communication eavesdrop in Section 3.5 List of attack targetsNew Section 4.1 Configuration protectionIntroduction of Section 5.2 ST proprietary SBSFU solutionNew Section 5.2.3 ConfigurationsSection 5.3 Arm TF-M solutionSection 6.1 Overview of security featuresLast note in Section 6.2 Readout protection (RDP)New Section 6.3 Lifecycle management - product stateSection 6.7 Execute-only firmware (PCROP)</td></tr></table>

<table><tr><td rowspan="2">Date</td><td rowspan="2">Version</td><td rowspan="2"></td><td rowspan="2">Changes</td></tr><tr><td></td></tr><tr><td rowspan="2">22-Mar-2023</td><td>8</td><td>Updated:</td><td>Section 1 General information Section 4.1 Configuration protection Section 4.2 TrustZone® for Armv8-M architecture Table 6. Scope of STM32 embedded memory protection features Table 7. Software isolation mechanism Section 5.4 Arm TF-M solution Section 5.5 Product certifications Table 9. Security features for STM32C0, STM32F0/1/2/3/4, STM32G0/4 devices Section 6.2 Readout protection (RDP) Section 6.5 TrustZone® Section 6.7 Execute-only firmware (PCROP) Section 6.12 Antitamper (TAMP)/backup registers (BKP) Section 6.18 Cryptography</td></tr><tr><td>13-Oct-2023</td><td>9</td><td>Section 7 Guidelines Section 8 Conclusion Added: Section 5.1 Secure firmware install (SFI) Updated: Table 4. Attacks types and costs Section 5.6: Product certifications Section 6.3: Lifecycle management—product state Section 6.9: Secure hide protection (HDP) STM32WBA added to Table 11. Security features for STM32L0/1/4/4+, STM32WB, STM32WBA,</td></tr><tr><td></td><td></td><td>STM32WL devices Added: Section 5.5: Secure manager Updated: STM32 MCUs. Applicable products..</td><td>STM32H7R/S added to Table 12. Security features for STM32L5, STM32U5, STM32H503/ Document title from Introduction to STM32 microcontrollers security to Introduction to security for Added STM32U0 Series and STM32WB0 Series to the document scope and updated Table 1. Added footnotes to Hardware crypto row on Table 10, Table 11 and Table 13.</td></tr></table>

<table><tr><td>Date</td><td>Version</td><td>Changes</td></tr><tr><td>10-Feb-2025</td><td>11</td><td>Updated: Section 1: General information Section 4.2: TrustZone® for Armv8-M architecture Section 4.4: Memory protections Section 4.4.1: System flash memory Section 4.4.4: External flash memories Section 4.4.5: STM32 memory protections Section 4.6: Debug port and other interface protection Section 4.7: Boot protection Section 5.1: Secure firmware install (SFI) Section 5.4: Arm TF-M solution</td></tr></table>

# Contents

# 1 General information

Overview 5

2.1 Security purpose . 5

# Attack types .

3.1 Introduction to attack types 7   
3.2 Software attacks .8   
3.3 Hardware attacks .9   
3.3.1 Non-invasive attacks. 10   
3.3.2 Silicon invasive attacks . 11   
3.4 loT system attack examples 12   
3.5 List of attack targets 12

# Device protections. 16

4.1 Configuration protection 16   
4.2 TrustZone® for Armv8-M architecture. 16   
4.3 Dual-core architecture 17

# 4.4 Memory protections 18

4.4.1 System flash memory 19   
4.4.2 User flash memory 19   
4.4.3 Embedded SRAM . 19   
4.4.4 External flash memories 20   
4.4.5 STM32 memory protections 21

# 4.5 Software isolation 21

4.6 Debug port and other interface protection 21   
4.7 Boot protection 22   
4.8 System monitoring 22

# Secure applications. .23

5.1 Secure firmware install (SFI) 23   
5.2 Root and chain of trust 23

# 5.3 STMicroelectronics proprietary SBSFU solution . 23

5.3.1 Secure boot (SB) 23   
5.3.2 Secure firmware update (SFU) 24   
5.3.3 Configurations 25

# 5.4 Arm TF-M solution. 25

5.5 Secure manager 26

# 5.6 Product certifications 26

# STM32 security features 28

6.1 Overview of security features 28

6.1.1 Static and dynamic protections . 28   
6.1.2 Security features by STM32 devices. 28   
6.2 Readout protection (RDP) .31   
6.3 Lifecycle management—product state .33   
6.4 Unique boot entry .34   
6.5 One-time programmable (OTP). .34   
6.6 Boot and security control (BSEC) .34   
6.7 TrustZone® .34   
6.7.1 Core state .35   
6.7.2 Secure attribution unit (SAU). .35   
6.7.3 Memory and peripheral protections . .36   
6.8 Flash memory write protection (WRP) 36   
6.9 Execute-only firmware (PCROP). .36   
6.10 Secure hide protection (HDP) . .37   
6.11 Firewall . .37   
6.12 Memory protection unit (MPU). 39   
6.13 Resource isolation framework (RIF) .40   
6.14 Customer key storage (CKS). .40   
6.15 Option byte keys (OBK) .41   
6.16 Antitamper (TAMP)/backup registers (BKP). .41   
6.17 Clock security system (CSS). .41   
6.18 Power monitoring (PVD). .42   
6.19 Memory integrity hardware check. .42   
6.20 Independent watchdog (IWDG). .42   
6.21 Device ID .42   
6.22 Cryptography . .42   
6.22.1 Hardware accelerators .43   
. rypb stae .43   
6.23 On-the-fly decryption engine (OTFDEC) .43   
6.24 Memory crypto engine (MCE) .44   
Guidelines. .45   
Conclusion. .47   
Appendix A Cryptography - Main concepts 18

A.1 Secret key algorithms . 48   
A.2 Public key algorithms (PKA) 49   
A.3 Hash algorithms 50   
A.4 MAC or signature and certificate. 50

Revision history 52

# List of tables

Table 1. Applicable products 1   
Table 2. Glossary . 2   
Table 3. Assets to be protected 6   
Table 4. Attacks types and costs 8   
Table 5. Memory types and associated protection 18   
Table 6. Scope of STM32 embedded memory protection features 21   
Table 7. Software isolation mechanism 21   
Table 8. Basic feature differences of TrustZone-based secure software. 26   
Table 9. Certifications coverage 27   
Table 10. Security features for STM32C0, STM32F0/1/2/3/4, STM32G0/4 devices . 28   
Table 11. Security features for STM32L0/1/4/4+ devices . 29   
Table 12. Security features for STM32WB, STM32WBA, STM32WB0x, STM32WL, and STM32WL3 devices 29   
Table 13. Security features for STM32L5, STM32U0, STM32U3, STM32U5, STM32H503/5, STM32H7R/S,   
STM32H72x/73/74x/75, STM32H7Ax/7Bx, STM32F7 devices 30   
Table 14. RDP protections 33   
Table 15. Attributes and access permission managed by MPU. 39   
Table 16. Process isolation 40   
Table 17. Features of the OTFDEC compared with the MCE. 44   
Table 18. Security use cases. 45   
Table 19. Document revision history . 52

# List of figures

Figure 1. Corrupted connected device threat 5   
Figure 2. loT system. 12   
Figure 3. Armv8-M TrustZone® execution modes 17   
Figure 4. Simplified diagram of dual-core system architecture 17   
Figure 5. Memory types. 18   
Figure 6. Secure boot FSM 24   
Figure 7. Secure server/device SFU architecture 25   
Figure 8. Example of RDP protections (STM32L4 series). 31   
Figure 9. TrustZone® implementation at system level 35   
Figure 10. HDP protected firmware access 37   
Figure 11. Firewall FSM 38   
Figure 12. Firewall application example. 38   
Figure 13. Dual-core architecture with CKS service 41   
Figure 14. Typical OTFDEC configuration 44   
Figure 15. Symmetric cryptography 48   
Figure 16. Signature. 49   
Figure 17. PKA encryption. 49   
Figure 18. Message hashing 50   
Figure 19. MAC generation with secrete key algorithm 50   
Figure 20. Signature generation with public key algorithm 51

# IMPORTANT NOTICE  READ CAREFULLY

pt old ursant  dits   leole.

purchasers' products.

No license, express or implied, to any intellectual property right is granted by ST herein.

are the property of their respective owners.

I

© 2025 STMicroelectronics - All rights reserved