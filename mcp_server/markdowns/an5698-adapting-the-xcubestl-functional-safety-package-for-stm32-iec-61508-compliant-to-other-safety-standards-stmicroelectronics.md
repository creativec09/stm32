# Adapting the X-CUBE-STL functional safety package for STM32 (IEC 61508 compliant) to other safety standards

# Introduction

Ta T standard addressed, the following items are considered:

IEC 61508.   
i safety performances of the devices according to the new standard.

The safety standards examined within this change impact analysis are:

ISO 13849-1:2015, ISO13849-2:2012: Safety of machinery and Safety, related parts of control systems

80:01abel rivstela arfy a.

# 1 About this document

# 1.1

# Purpose and scope

The safety analysis reported in STM32 MCU/MPU safety manuals is executed according to the IEC 61508 safety norm.

Thidocument includes theutcomea changepact analysi with respect direntsafetystanards, applied to the IEC61508 compliant safety analysis of STM32 MCU/MPU and included in related safety manuals. This document applies to STM32 MCUs and MPUs Arm®-based devices.

# Note:

Arm is a registered trademark of Arm Limited (or its subsidiaries) in the US and/or elsewhere.

# 1.2

# Terms and abbreviations

Table 1. Terms and abbreviations   

<table><tr><td rowspan=1 colspan=1>Acronym</td><td rowspan=1 colspan=1>Definition</td></tr><tr><td rowspan=1 colspan=1>CoU</td><td rowspan=1 colspan=1>Conditions of use</td></tr><tr><td rowspan=1 colspan=1>CPU</td><td rowspan=1 colspan=1>Central processing unit</td></tr><tr><td rowspan=1 colspan=1>DC</td><td rowspan=1 colspan=1>Diagnostic coverage</td></tr><tr><td rowspan=1 colspan=1>End user</td><td rowspan=1 colspan=1>Individual person or company who integrates device in their application, such as anelectronic control board</td></tr><tr><td rowspan=1 colspan=1>FIT</td><td rowspan=1 colspan=1>Failure in time</td></tr><tr><td rowspan=1 colspan=1>FMEA</td><td rowspan=1 colspan=1>Failure mode effect analysis</td></tr><tr><td rowspan=1 colspan=1>FMEDA</td><td rowspan=1 colspan=1>Failure mode effect diagnostic analysis</td></tr><tr><td rowspan=1 colspan=1>ITRS</td><td rowspan=1 colspan=1>International technology roadmap for semiconductors</td></tr><tr><td rowspan=1 colspan=1>MCU</td><td rowspan=1 colspan=1>Microcontroller unit</td></tr><tr><td rowspan=1 colspan=1>MPU</td><td rowspan=1 colspan=1>Microprocessor unit</td></tr><tr><td rowspan=1 colspan=1>SFF</td><td rowspan=1 colspan=1>Safe failure fraction</td></tr><tr><td rowspan=1 colspan=1>SIL</td><td rowspan=1 colspan=1>Safety integrity level</td></tr></table>

# 1.3

# Reference safety standards

[1] ISO 13849-1:2015, ISO13849-2:2012  Safety of machinery and Safety-related parts of control systems, [2] IEC 61800-5-2:2016 -Adjustable speed electrical power drive systems - Part 5-2: Safety requirements - Functional

[3] IEC61508:1-7© IEC:2010 - Functional safety of electrical/electronic/programmable electronic safety-related systems

# 2 ISO 13849-1:2015, ISO 13849-2:2012

ISO3849-1 is a type B1 standard. It provides a guideline for the development of Safety-related partso machinery control systems (SRP/CS) including programmable electronics, hardware and software.

# ISO 13849 architectural categories

The diagrammaticrepresentation f thetypical safetyunction  reported in SO3849-:2015, [.4]Und e assmption that Compliant item as defined in relate section of M Safety Manual is used toimplement the blocb ogic), theequivalencef the  389 repreentation with he e i safty manual  evident. The mapping of IO 3849 architectures with the one indicated in MCU Safety Manual for the definitionof the Compliant item is therefore possible.

ISO 13849-1:2015in Section : ISO13849-1:2015, ISO13849-2:2012 defines in details five different categories. The following table lists for each category the possible implementation by one of the IEC 61508 compliant thaivable  eided yeecialue nosioverage C eantime ns failure (MTTFd) (refer to ISO 13849 safety metrics computation for details on computations).

Table 2. IS0 13849 architectural categories   

<table><tr><td rowspan=1 colspan=2>ISO13849-1:2015</td><td rowspan=2 colspan=1>Link to IEC61508-compliant safetyarchitectures</td><td rowspan=2 colspan=1>Notes/constraints</td></tr><tr><td rowspan=1 colspan=1>Category</td><td rowspan=1 colspan=1>Clause</td></tr><tr><td rowspan=1 colspan=1>B</td><td rowspan=1 colspan=1>6.2.3</td><td rowspan=1 colspan=1>Possible with 1001 architecture</td><td rowspan=1 colspan=1>No requirements for MTTFd and (DC)avg aregiven for category B, anyway it isrecommended to follow MCU safety manualrecommendation.</td></tr><tr><td rowspan=1 colspan=1>1</td><td rowspan=1 colspan=1>6.2.4</td><td rowspan=1 colspan=1>Not recommended</td><td rowspan=1 colspan=1>Category not recommended (seeIEC138491).</td></tr><tr><td rowspan=1 colspan=1>2</td><td rowspan=1 colspan=1>6.2.5</td><td rowspan=1 colspan=1>Possible with 1001 architecture (externalWDT is mandatory)</td><td rowspan=1 colspan=1>The adoption of external WDT (CPU_SM_5)acting as TE is mandatory.Constraints on (DC)avg and MTTFd can besatisfied but computations are needed.()Constraints on CCF are satisfied.</td></tr><tr><td rowspan=1 colspan=1>3</td><td rowspan=1 colspan=1>6.2.6</td><td rowspan=1 colspan=1>Possible with 1002 architecture +DUAL_SM_0</td><td rowspan=1 colspan=1>Constraints on DCavg and MTTFd can besatisfied but computations are needed.(1)Constraints on CCF are satisfied.(2)</td></tr><tr><td rowspan=1 colspan=1>4</td><td rowspan=1 colspan=1>6.2.7</td><td rowspan=1 colspan=1>Possible with 1o02 architecture +DUDUALSM_0</td><td rowspan=1 colspan=1>Implementation of DUAL_ SM_0 scheme ismandatory to mitigate fault accumulation.Constraints on DCavg and MTTFd can besatisfied but computations are needed.Constraints on CCF are satisfied.(2)</td></tr></table>

1. implementation (sensors, actuators, etc). The figures need therefore to be evaluated at system level.

2. CC compliance activity (MCU safety manual) helps to claim the score for item #4 in Table F.1.

# 2.2 ISO13849 safety metrics computation

Adi  I8 petstableaardizmeantengerous failureTr ev electric or electronics components. However, table C.3 in ISO 13849 points to ICs manufacturer's data while attempting to classify MTTFd for programmable ICs. As a consequence, safety analysis results of MCU safety manual can be re-mapped in ISO13849 domain, because even computed or IEC 61508 they are definitely more accurate in the definition of dangerous failures identification.

General guidance included in IEC61508-6 states that when for a certain component PFH << 1 then it can be asued that MTTF= 1 / PFH. In principle, this relationship could be used to derive MFFT values from FMEDA data. However, considering that in ISO13849:

unlike IEC61508, there is no formal definition for "safe state"   
MTTFd definition is associated to dangerous failures   
PFH and λ relationship can be assumed to be the same for continuous mode of operation in IEC61508

then it is more correct to adopt this formula:

MTTFd = 1 / ( λDU(perm)+ λDD(perm)+ λDU(trans)+ λDD(trans) )

Becuse  defiitionfocus ndngerous ilures,eduseran excludefrom coputation he  contru coming from ST32 peripherals not used or the implementation of safety related functions (refer to elated section of MCU safety manual for details)

ItiworogmolyEacila ul considered as dangerous.Because of this assumption, the term λDU(trans)+ λDD(trans) can assume highvalues in some specific STM32 MCUs with large SRAM banks. Table C.3 f ISO 13849-1 allows to apply a 50% derating whn usimanctuerdt ut hat coul stilerom eeali  se spec. Therefore, the usef FMEDA data can lead to very conservative values see note) or computed MTT the end user must carefully consider this aspect, because MTTd values are used to compute system DCavg by mixing the contribution of each individual component.

In ISO 13849-1 the DC for each single component has the same meaning of the IEC 61508 metric; results of MCU safety manual and related FMEA/FMEDA can therefore be reused. However, this standard defines the ct avpliable eholRPe orm fheuat eiA  ul, where the contribution each par the control system s weighted with respect o M  thevarus subsystems of the channel. End user is therefore responsible or the computations of the overall DCavg.

The sandar denis any possibility aul exclusin whilcalculating DCavg (ISO13849-Tab.D.1oexcusn allowed), which is also the assumption of Device analysis documented in MCU safety manual.

Note that DC values included in FMEDA documents are computed as ratios between homogenous values ailure ratan o they depend just n arhitecural specs, nd they reot fcted y cnsieratinabout bas failure rate.

# Note:

It can happen that when computing system DCavg according ISO 13849-1, MTTF values coming from reliability are used for generic components different from STM32 MCUs.As the procedure used to derive reliability data oristanetoslcnrhefntiuoror permanent damages due to component overstress, related MTTF values might seems uncorrelated to what is computed for STM32 MCU according above procedure based on FMEDA data.

# 3 IEC 61800-5-2:2016

The scope of this standard is the functional safety of adjustable speed electric drive systems.

# 3.1

# IEC 61800 architectural categories

Because IEC 61800 definitions for HFT and for architectures are equivalent to the ones of IEC61508, the remapping is straightforward.

The STM32xx MCU is considered as Type B for the consideration reported in the MCU Safety Manual (refer to the section related to Assumptions).

# IEC 61800 safety metrics computation

The FH  a safety funcion perormed by PDS(R)is evaluated b the applicationf IEC 150-.The ro lik with e norm EC6150 s flecals by heoption  E 800-  he ameelevan metri H, an FF. So results f the MCU safety anual and relate FMEAand FMEDA can  e-appe in IEC61800 domain.

# Revision history

Table 3. Document revision history   

<table><tr><td rowspan=1 colspan=1>Date</td><td rowspan=1 colspan=1>Version</td><td rowspan=1 colspan=1>Changes</td></tr><tr><td rowspan=1 colspan=1>12-Oct-2021</td><td rowspan=1 colspan=1>1</td><td rowspan=1 colspan=1>Initial release.</td></tr><tr><td rowspan=1 colspan=1>12-Mar-2024</td><td rowspan=1 colspan=1>2</td><td rowspan=1 colspan=1>Updated Section 2.2: IS0 13849 safety metrics computation.</td></tr></table>

# Contents

# 1 About this document

1.1 Purpose and scope.   
1.2 Terms and abbreviations   
1.3 Reference safety standards.

# ISO 13849-1:2015, ISO 13849-2:2012

2.1 ISO 13849 architectural categories. . 3   
2.2 ISO13849 safety metrics computation 3

IEC 61800-5-2:2016 5

3.1 IEC 61800 architectural categories . . 5   
3.2 IEC 61800 safety metrics computation. 5

# Revision history 6

_ist of tables 8

# List of tables

Table 1. Terms and abbreviations. 2   
Table 2. ISO 13849 architectural categories. 3   
Table 3. Document revision history . 6

# IMPORTANT NOTICE  READ CAREFULLY

pt old ursant  dits   leole.

purchasers' products.

No license, express or implied, to any intellectual property right is granted by ST herein.

are the property of their respective owners.

I

© 2024 STMicroelectronics - All rights reserved