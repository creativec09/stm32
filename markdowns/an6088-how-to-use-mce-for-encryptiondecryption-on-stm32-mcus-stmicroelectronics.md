# How to use MCE for encryption/decryption on STM32 MCUs

# Introduction

t three use cases where the MCE can provide protection.

from an external flash memory. LRAMx i  Ae M . Ln AM RnC aa

T r-asaepe ubea e as immutable and OEM updatable root of trust boot solutions, referred to as STiRoT and OEMuRoT respectively.

RRvnRo OEMiRoT + OEMuRoT boot paths.

T

Table 1. Applicable products   

<table><tr><td>Type</td><td>Root part number</td></tr><tr><td rowspan="2">Microcontrollers</td><td>STM32H7S3A8, STM32H7S3I8, STM32H7S3L8, STM32H7S3L8U, STM32H7S3N8, STM32H7S3R8, STM32H7S3V8, STM32H7S3Z8</td></tr><tr><td>STM32H7S78-DK, STM32H7S7A8, STM32H7S7I8, STM32H7S7L8, STM32H7S7N8, STM32H7S7Z8</td></tr></table>

# MCE (memory cipher engine) overview

The memory cipher engine (MCE) defines multiple regions with a speciic securiy setup in a given adress erypted region ismanaged on-thely bythe MCE,automatically decrypting reads and encrypting writ authorized.

Upu g  f c C w lary C t e feature that can be applied in different regions (privileged, write). Refer to the figure below.

T MC  te ablelow Whe  h el activate the write protection as soon as the whole region has been encrypted (read-only region).

![](images/023359bc1e9b673e9a0504bc63529f4fddcb3b67ee57f15b5173866e5f0c63d6.jpg)  
Figure 1. MCE block diagram

The STM32H7Sx implementation defines three MCE instances connected to the external memory interfaces as icuWhe eC c wi  aty e ciey p m qu e  eo wri e  me 16-bytes bursts. Table 2 details the main implementation differences between the three MCE instances.

Table 2. MCE Main features   

<table><tr><td rowspan=1 colspan=1>MCE features</td><td rowspan=1 colspan=1>MCE1</td><td rowspan=1 colspan=1>MCE2 and MCE3</td></tr><tr><td rowspan=1 colspan=1>Number of regions</td><td rowspan=1 colspan=1></td><td rowspan=1 colspan=1>4</td></tr><tr><td rowspan=1 colspan=1>Cipher engines</td><td rowspan=1 colspan=1>AES</td><td rowspan=1 colspan=1>Noekeon</td></tr><tr><td rowspan=1 colspan=1>Derive key function</td><td rowspan=1 colspan=2>Normal, fast</td></tr><tr><td rowspan=1 colspan=1>Master key</td><td rowspan=1 colspan=2>2</td></tr><tr><td rowspan=1 colspan=1>Encryption mode</td><td rowspan=1 colspan=1>Block, stream</td><td rowspan=1 colspan=1>Block</td></tr></table>

# 2 MCE implementation in STM32H7Sx

The STM32H7Sx implementation define three MCE instances connected to the external memory interfaces as depicted in Figure . When MCE is used in conjunction with XSP, it ismandatory to set the flash meory coiey p mod aqu  e peo wrie ah mes 16-bytes bursts.

![](images/8822f66d59d42c8618ccf373cd0697157c79df69dc41713d9ab022638949b65b.jpg)  
Figure 2. STM32H7S MCE instances

In the 32x pleentatin Fgure) theE protects he conientiality code  ata storn the external memory (four regions/memory). The MCE peripheral instances are connected to the xSPI peripheral instances as follows:

MCE1 is connected to the xSPI1 memory interface, which can be connected to a NOR flash or a PSRAM. MCE2 is connected to the xSPI2 memory interface, which can be connected to a NOR flash or a PSRAM. MCE3 is connected to the FMC memory interface, which can be connected to a PSRAM, an SDRAM, or a FRAM.

In Figure 2, the xSPI1 and xSPI2 are connected to an XSPIM (xSPI IO manager) which allows a multiplexed connection of external memories (NOR flash or PSRAM). Several use cases can be considered as follows (refer to the XSPIM section of RM0477 for more details):

XSPI1 mapped to port 1, with XSPI2 mapped to port 2 (direct mode). XSPI1 mapped to port 2, with XSPI2 mapped to port 1 (swapped mode). Two XSPIs drive one external memory. XSPI1 and XSPI2 both mapped to port 1, with arbitration (multiplexed mode to port 1). XSPI1 and XSPI2 both mapped to port 2, with arbitration (multiplexed mode to port 2). • One XSPI drives two external memories.

MCE encryption/decryption must take the corresponding IO manager use case/mode into account before any ecrpte images installation.TheTM32CubeHR iware provides templates according he twst u cases of XSPIM.

# 2.1

# MCE1 implementation

The confidentialiy of MCE1 is based on legacy AES 128-bit cipher block (ECB) or stream (counter CTR) mode.

# 2.1.1 Block mode

The MCE1 block mode is based on the AES cipher that is compatible with the ECB mode specified in the NIST FIPS publication 197 advanced encryption standard (AES). The new AES 128-bit block cipher is used, the AES-ECB with the key derivation function based on the well-known Keccak-400 algorithm where each 56-bit word has its own AES key.

Tebloc-chemode wydevatoralrsorth par ecptingiudate w

The block-cipher mode key derivation can be either normal or fast (refer to RM0477 for more details).

Sinc the normal key derivationfunction s leakageresilient, themaster key informationinnormal modeis protected against side channel attacks (SCA). When a tamper event is confirmed in TAMP, ll MCE keys are erased.

In fast mode the SCA protection is not supported, hence the master key used in normal mode is never used in fast mode.

# 2.1.2 Stream mode

The MCE1 stream mode is based on the AES cipher that is compliant with the CTR mode specified in the NIST SP00-38A Recommendation for block cipher modes of operation. The legacy AES 128-bit counter cipher mode i . Ihe t    oe protection, or protection against bit-flip attacks is provided.

Instream ciher mode he partl update encrypt egonisotrecomende. Each time he conten encrypted region is changed the whole region must be reencrypted using a new key, a new 16-bit version, or a 64-bit nonce.

# MCE2 and MCE3 implementation

MCE1 and MC ae bas n he Noekon algorit(rerhtts://grooekeon.org)that suports heblock ciphering mode with normal or fast key derivation.

Tebloc-chemde w ydeatn orals spore alecptngpdat

The MCE1 and MCE2 normal key derivation mode is leakage resilient. The master key information in normal mde is protected against ide hannel attacks (SCA). When a tamper event is confire in TAMP, all MCE keys are erased. In fast mode the SCA protection is not supported, hence the master key used in normal mode is never used in fast mode, in MCE2 and MCE3.

# 2.3

# Selecting an MCE configuration

The MCE configuration to be used depends on many considerations as follows:

The implementation path: each MCE is connected to a fixed external memory interface (xSPI1, XSPI2, or FMC). Each MCE supports a set of memory technologies (volatile or nonvolatile). The MCE1 is connected to xSPI1. The MCE2 is connected to xSPI2. The MCE3 is connected to FMC.

The memory type: volatile or nonvolatile. In addition, memories connected to xSPI1 or xSPI2 can be multiplexed via the XSPI IO manager (XSPIM) as depicted in Figure 2.

• Priority between security and performance:

The Noekeon cipher has a security level of \~96 bits, lower than the 128 bits of the AES-128 cipher. Block or stream cipher modes: security and performance compromises must consider that the MCE stream cipher mode is faster than the block cipher mode, but the latter is more secure than the former. Indeed, block cipher provides protection against bit-flip attacks. And write protection must be used after encrypting an image with stream cipher (to prevent encrypting multiple times with same key and IV).

Normal or fast key derivation in block-cipher mode: key derivation can be normal giving higher protection with SCA resistance or fast, giving better performance without any SCA resistance. Hence the master key used in normal mode is never used in fast mode.

Partal updates: in block cipher mode any part of the encrypted region can be updated anytime whatever the key derivation: normal of fast. This feature is not supported in stream cipher mode.

When the MCE is used in conjunction with xSPI1 or xSPI2, it is mandatory to read or write the flash memory using the memory map mode of the flash memory controller.

# Table 3 summarizes the latency in cycle for 16-bytes data.

Table 3. MCEs performances comparison   

<table><tr><td rowspan=1 colspan=1>Mode (1)</td><td rowspan=1 colspan=1>MCE1 AES-block</td><td rowspan=1 colspan=1>MCE2/3 Noekeon-block</td><td rowspan=1 colspan=1>MCE1 AES-stream</td></tr><tr><td rowspan=1 colspan=1>Normal</td><td rowspan=1 colspan=1>25 (2)</td><td rowspan=1 colspan=1>21</td><td rowspan=1 colspan=1>11 (masked)</td></tr><tr><td rowspan=1 colspan=1>Fast</td><td rowspan=1 colspan=1>15 (2)</td><td rowspan=1 colspan=1>11</td><td rowspan=1 colspan=1>N/A</td></tr></table>

Latency in cycle for 16-bytes data. Add 10 for writes.

Table 4 summarizes the recommended MCE1 configurations to use regarding security protection and performance scales.

Table 4. MCE1 configuration selection   

<table><tr><td rowspan=1 colspan=1>Selection criteria</td><td rowspan=1 colspan=1>Recommended MCE configuration</td><td rowspan=1 colspan=1>Selected configuration features</td></tr><tr><td rowspan=1 colspan=1>Security</td><td rowspan=1 colspan=1>MCE1 block cipher mode,Normal key derivation</td><td rowspan=1 colspan=1>AES-128 bit ECBKeccak-400 key derivationSCA resistantPartial encryption updatesSuitable for code+data encryption</td></tr><tr><td rowspan=1 colspan=1>PerformanceNon-SCA protection</td><td rowspan=1 colspan=1>MCE1 block cipher mode•    Fast key derivation</td><td rowspan=1 colspan=1>•    AES-128 bit ECBFast key derivation•    No SCA resistancePartial encryption updatesSuitable for code + data protection</td></tr><tr><td rowspan=1 colspan=1>Performance</td><td rowspan=1 colspan=1>MCE1 streamNo key derivation (n/a)</td><td rowspan=1 colspan=1>AES-128 CTRNo SCA resistanceNo partial encryption updatesSuitable for code protection</td></tr></table>

MCE2 and MCE3 are based on Noekeon with a security level of \~96 bits versus 128 bits for AES-128 bits in the case of MCE1. When a security level is key, the user can move to MCE1 configurations in Table 4. Table 5 summarizes the possible configurations when MCE2 or MCE3 are used.

Table 5. MCE2 and MCE3 configuration selection   

<table><tr><td rowspan=1 colspan=1>selection criteria</td><td rowspan=1 colspan=1>Recommended MCE configuration</td><td rowspan=1 colspan=1>Selected configuration features</td></tr><tr><td rowspan=1 colspan=1>Security</td><td rowspan=1 colspan=1>MCE2 or MCE3 block cipher modeNormal key derivation</td><td rowspan=1 colspan=1>Noekeon block modeNormal key derivationSCA resistantPartial encryption updatesSuitable for code + data encryption</td></tr><tr><td rowspan=1 colspan=1>Performance</td><td rowspan=1 colspan=1>MCE2 or MCE3 block cipher modeFast key derivation</td><td rowspan=1 colspan=1>Noekeon block modeFast key derivationNo SCA resistancePartial encryption updatesSuitable for code + data protection</td></tr></table>

# 3 MCE configuration and external flash regions

The STM32H7Sx devices provide a small-sized internal user flash of 64 Kbytes. When the TiRoT is used, the intealuseash must hold heextealmemoy manageLad uable oe provieby . Thi midlewareallows access to all ypes  external memoris, and launches aapplication that istore in exeal emoryThis s y he exteal memoymanagerLoade  coyo ad heplt firmware (refer to Figure 3).

The STM32H7Sx devices also feature 128 Kbytes of internal flash as system flash memory. It is intended to iis curatneu viupoc e o nlat t Figure 3.

ST immutable RoT (STiRoT): manages the secure boot and the secure update of the first stage of the application. It is present in the STM32H7Sx only as it is based on the hardware crypto accelerators. Debug control (ST-DA): debug reopening and regression controls.   
Se ervics (RSS): secure rware installation FI ST immutable code allowing instal seuely an extension (RSS-e).   
RSS-Lib: an RSS extension library that provides a set of APls to manage the temporal isolation (HDPL ) ntrol he prouc c s GetroducState(nSeruStatecns), o provision the option byte keys (OBKey).

The figure below provides a genericmapping f an external flash managed by the MCE encryption regions. This n o ola needs.

In region 1: no MCE encryption. The download slots are used to host images that are already encrypted (with transport keys, not with MCE keys). When confidentiality is not required, there is no need to encrypt the user application. Data storage can be cleared or encrypted with DHUK keys using the SAES. In region 2: MCE encryption/decryption of the user application in the instalation slot can bemanaged with the same key for all STM32H7Sx devices, or with a different key per device.   
In region3: MCE manages encrypted data storage in external memory. Region 3 can be protected with different MCE keys per STM32H7Sx device.   
In region : the MCE can manage the encryption in the installation slot with different keys perdevice e first boot level.

![](images/1e874351a3aec7c7fb350f01d253403d8d0548ef609f7ea8ab2f301d463f8d7d.jpg)  
Figure 3. Typical internal and external flash mapping versus MCE regions

The selection of the MCE configuration depends on the degree of performance and security required by the customers as described in Section 2: MCE implementation in STM32H7Sx. Hereafter, some recommendations of MCE configuration regarding the MCE encrypted regions 2, 3 and 4.

# Regions 2 and 4

Regns 2 an4 peor the encyption code nthe external flash slot #5and slot #7, the userappliati installation slot and the OEMuRoT installation slot respectively.

Encryption of user application slot #5 can be performed using either the same key for all STM32H7Sx devices or a different/unique MCE key per device.

Encryption of updatable root of trust slot #7 with the same or different key depends on the OEMuRoT firmware implementation as detailed in Section 5: MCE protection in case of XiP. A different key is recommended in the case of the first boot level of this uRoT installation slot #7.

[MCE1 AES-block mode + normal] for security: as detailed in Section 2: MCE implementation in STM32H7Sx, it is recommended to configure MCE1 in AES block ciphering with normal key derivation. Thi configuration s thebest choice or securityreasons,as it brings theSCA reistance  ke deatin combined with AES-128.

Selecting the [MCE1 AES-block mode + fast] configuration loses the SCA resistance of key derivation.

[MCE1 AES-stream] for performance: when performance is a matter, the MCE1 configuration with stream gives the best performance. In that case, write protection has to be used, but it is not recommended to partally update the encyption these regions.s a consequenc, tistream mode isnly aplicable t code.

[MCE2 or MCE3 Noekeon-block]: if MCE2 or MCE3 are used to protect an image, only Noekeon-block is available. Then normal or fast key derivation can be selected depending on security/performance targets. In normal mode the key derivation is SCA resistant, however the fast mode is not.

# Region 3

Region 3 is dedicated to encryption of data storage in the external flash slot #6

Encrypted data storage in external memory can be protected with MCE/different keys. [MCE1 AES-block mode + normal], [MCE1 AES-block mode + fast] and [MCE2 or MCE3 Noekeonblock] configurations are the same as described in region 2 and 4 above. Encrypted regions can be partially updated. [MCE1 AES-stream] partial updates of an encrypted region can be an issue, and is not recommended.

# Recommended keys for external memory protection

Exteal memory protecon can be encrypte by ME, by transport,  by DUKkes. This secton describe he recommended encryption approach.

In volatile external SRAM memories, it is recommended to use dynamic values for keys as they usuallystore iz a different key for each STM32H7Sx, which can be based on the application hardware key mechanism (AHK).

In te nonvolati (NV)external fashmemoris, encryption s doneonly when neede Different encryptin ky approaches can be considered as stated below:

Images that are not encrypted by MCE keys but are encrypted at application level, using SAES for example. Images encrypted with MCE using the same key for all the STM32H7Sx devices. Images encrypted with MCE using a different key for each STM32H7Sx device. External memories are not erased by DA-regressions. When confidentiality protection is needed, the MCE encryption is recommended for all data storage and code that need to be erased from a full regression.

A different key per device is preferable for many reasons, for example the ones listed below:

If all devices have the same key, the security of ll devices is compromised in case of key leakage. With a diferent key per device, an external memory device is assigned to one product only. It is not possible to reuse an external memory device in a second product as the second STM32H7Sx is not provisioned with the same key.   
In the case of reverse engineering, i s not possible to reuse the external flash inother environments, making the reverse process very complicate.

In Vxeeo it  en onl and on first boot timing constraints:

# MCE usage with a different key per device

Cerlht y o meorys he nt odevinoteaacturgea de could impact the first boot time when the image size is too large.

Durmanuacturgdrhel prograheag e prosinin wi GANG programming or with an external flash loader.

Wh  eviea an inteo i executed, the installation of the image is performed via the OEMuRoT.

# MCE usage with the same key for all devices

al

Ourigmanufacturing,orduring the inital programming o the mages, provisioning can bedone with GANG orogramming or with an external flash loader.

Who The binary is preencrypted with tools in a trusted environment or in an untrusted environment using SFI.

When using the same MCE key oral devices fr a user application, the fmware can be installed tly preecryptedininstallation slot #The advantages areelated to bot securityand initial boot ime:

(+) Security: the firmware is shared encrypted.   
the first boot then executed at a second boot.

On the other hand, when using the same MCE key for all devices for user application, allthe devices are provisioned with the same key. This implies two major security drawbacks:

compromised.

(Serity:  al the devies useonly the same key(s), it means that there is o proteon or exteral memory exchanges. Besides, the encrypted image loaded into one external memory is the same for all other external memories.

# 5 MCE protection in case of XiP

When STiRoT is used as the execution entry point, the MCE usage in a XiP use-case can be described as e  uai gnol e creexteal

Tl defiwhich rgins have ypton, ad whic ones ot havThe r each regin an - MCE based key is defined, summarized in are summarized in Table 6.

Region without MCE encryption: region 1.

Download slot: used to host already encrypted images with transport keys, no need to encrypt with MCE.   
Data download slot, it is also encrypted with transport keys if needed, or kept in clear.   
Encrypted data storage: can be protected by the DHUK key and encrypted using the SAES. In a clear user application installation slot: no encryption of user application when no confidentiality is required.

Regions with MCE encryption protection:

Region 2: user application installation slot. It can be encrypted with the same MCE key or with a different key per device.   
Region 3: encrypted data storage in external memory can be protected with MCE, with the same key, or with a different key per device.   
Region 4: instalation slot of the first boot level where the OEMuRoT (that acts as the second boot stage) is installed. This slot is always encrypted using MCE keys that are different per STM32H7Sx device, as mentioned above.

All the configurations f STiRoT and OEMuRoT are set in HDPL1 and HDPL2 respectively. In this way, when the the application and protected.

With this typical external flash scheme, there are two sets of MCE keys that are used:

The MCE encryption keys that are managed at HDPL1 for STiRoT:

STiRoT is responsible for the secure boot secure firmware update of the next level (OEMuRoT or application). It uses an "install slot" key to access the next level and "transport keys" to manage decryption of updates.

o When OEMuRoT is acting as a second boot stage, the STiRoT configures the MCE in decryption mode with an "install slot" key. This action allows the external memory manager/ iLoader to load the OEMuRoT image into the external SRAM, before launching it.   
o In case of an update of the OEMuRoT version, the STiRoT decrypts the new image using the MCU boot STiRoT keys (transport keys of the image). Then STiRoT checks the image authenticity and integrity. If validated, the STiRoT configures the MCE in encryption mode using the MCE "install slot" keys. Finally, the external memory manager/iLoader installs the encrypted image using HDPL1 MCE keys into the external flash at the OEMuRoT installation slot.

The MCE encryption keys are provisioned at HDPL2 for OEMuRoT:

OEMuRoT is responsible for the secure boot secure firmware update of the next level (application). It uses an "install slot" key to access the next level and "transport keys" to manage decryption of updates.

The same flow as STiRoT is used to launch the application image or to install a new application version into the application installation slot.

In installing the new application version, OEMuRoT checks if a new user application is stored in the download slot. If there is any, OEMuRoT decrypts it with a "transport key" and controls its integrity, its authenticity, and its antirollback version. If successful, OEMuRoT configures the MCE with "install slot" encryption keys. The image is reencrypted by the MCE and copied in the user application installation slot.

o When launching the user application, OEMuRoT controls the integrity and the authenticity of the user application from the installation slot. If successful, OEMuRoT executes it from external flash memory based on the MCE decryption using the MCE "install slot" keys configured by the OEMuRoT.

To eal

Table 6. External flash slot protection with MCE and non-MCE keys   

<table><tr><td rowspan=1 colspan=1>Slotindex</td><td rowspan=1 colspan=1>External flashmemory slot</td><td rowspan=1 colspan=1>MCE key protection</td><td rowspan=1 colspan=1>Non-MCE key protection</td></tr><tr><td rowspan=1 colspan=1>1</td><td rowspan=1 colspan=1>User or OEM downloadslot(no execution)</td><td rowspan=1 colspan=1>N/A (no need to encrypt with MCE for protection)</td><td rowspan=1 colspan=1>AES encryption with MCUBootSTiRoT keys (update transportkeys) when a new OEMuRoTimage is available.AES encryption with MCUBootOEMuRoT keys (updatetransport keys) when a newuser-application is available.</td></tr><tr><td rowspan=1 colspan=1>2</td><td rowspan=1 colspan=1>Data download slot(no execution)</td><td rowspan=1 colspan=1>N/A (no need to encrypt with MCE for protection)</td><td rowspan=1 colspan=1>AES encryption using one of SAES orAES source. Managed by the firmwareaccessing them.</td></tr><tr><td rowspan=1 colspan=1>3</td><td rowspan=1 colspan=1>Encrypted data storage(no execution)</td><td rowspan=1 colspan=1>N/A (no need to encrypt with MCE for protection)</td><td rowspan=1 colspan=1>Encrypted data storage in externalmemory can be protect with DHUKskeys using SAES.</td></tr><tr><td rowspan=1 colspan=1>4</td><td rowspan=1 colspan=1>In clearUser applicationInstallation slot</td><td rowspan=1 colspan=1>N/A (no need to encrypt with MCE for protection)</td><td rowspan=1 colspan=1>No encryption of user application whenno confidentiality is required.</td></tr><tr><td rowspan=1 colspan=1>5</td><td rowspan=1 colspan=1>User applicationInstallation slot</td><td rowspan=1 colspan=1>•    Encryption with &quot;installation slot&quot; key with adifferent key (per product key) or with thesame key.Different keys: derived from HUK (AHK,application hardware key, secret tosoftware).Same key: stored in OBKeys.AES &quot;installation slot&quot; key managed byOEMuRoT (HDPL2).</td><td rowspan=1 colspan=1></td></tr><tr><td rowspan=1 colspan=1>6</td><td rowspan=1 colspan=1>Encrypted data storage(no execution)</td><td rowspan=1 colspan=1>Encrypted data storage in external memory canbe protected with different MCE keys (HDPL2).</td><td rowspan=1 colspan=1></td></tr><tr><td rowspan=1 colspan=1>7</td><td rowspan=1 colspan=1>OEMuRoT installationslot(no execution)</td><td rowspan=1 colspan=1>Encryption with &quot;installation slot&quot; key, always&quot;different&quot; with STiRoT. The key is controlled bySTiRoT.</td><td rowspan=1 colspan=1></td></tr></table>

The provided use cases in the STM32CubeH7RS firmware are based on the STiRoT + OEMuRoT. The latter should be installed first in the OEMuRoT installation slot. In this use case, the STiRoT can only manage OEMuRoT images encrypted with different MCE keys.

When running from the internal SRAM the OEMuRoT manages to install a new user application or to launch the application available n theapplication download slot.By default, theOMuRouses mages encrypte w different MCE keys ", but the user can customize the code to use the same key.

The choice to user different keys or the same key can be performed by firmware configuration in the STM32CubeH7RS firmware.

# MCE protection in case of "Ioad and run"

n a "oad and run" scheme (L&R), there are two use cases for MCE usage in the STM32CubeH7RS: L&R from external RAM, and L&R from internal RAM (refer to Figure 4 and Figure 5).

For the use case of L&R from external RAM, the following rules apply:

The execution from external RAM recommends the usage of keys that are different for each initialization Dynamic external SRAM content always requires dynamic keys for protection. For this reason, different AHK keys per device are used in either:

Encrypted data storage slot (MCE-AHK1) or Encrypted user application slot (MCE-AHK2) or The same MCE-AHK for both data storage and user applicatic

If tecontent is ored encrypted into the external flash slots, the userapplication i the L&R contet must lvry and un t fom he exteal RAM.Theuserapplicatin must have n exta code hat g he slot inoratn, lads t into heexteral RAM andmanagestoveryand lunchThis isalsoapple for encrypted content to be loaded into internal RAM in the context of L&R form internal RAM.

![](images/327bf0f1abf511c710087158ab6e820803ed21f8e8bcb93d7503fb991e97ebb9.jpg)  
Figure 4. MCE usage in the context of L&R from external RAM

![](images/9c8375fe22492fd4332b827ad24dbe682af8353492a842e44770670b85efb543.jpg)  
Figure 5. MCE usage in the context of L&R from internal RAM

Inhe cntxt  L fr exteal RAM Fguthe sot heexteal fash memory e lade ow into the internal or the external RAM:

The OEMuRoT, used in case f boot orupdate,  always decryptd and loade into thenternal RAM. It is done using MCE STiRoT different keys per device. The same approach is followed in the contexts of L&R from internal RAM and of XiP.

It is recommended to load the "encrypted data storage" slot 6, based on MCE key encryption, into the inteal RAM. It is up to theapplication tomanage the decryption while it is loading this slot from the external flash to the internal RAM. This rule is valid for both L&R from internal RAM, and L&R from external RAM.

The "encrypted data storage" slot 3 with data security based on SAES with DHUK and no MCE encryption, is loaded into the external RAM. The access is managed by the user application through MCE.

It is up to the application to load, verify, and run into the external RAM:

The "encrypted user application" slot 5 loaded into the MCE region encrypted using and "AHK different keys per device" or a derived key. The "in clear user application" slot 4 loaded into the MCE region without encryption.

In tecontext fLR frointernal RAM (Figur), ll istallation slotsftheexternal fash,includige R o ntal AM.csan external RAM. However, the user must consider that there is a maximum of 456 Kbytes of contiguous SRAM available per product, minus \~70 Kbytes already reserved for the OEMuRoT execution slot.

# 7 MCE key provisioning with different keys

The figure below shows how the MCE keys are provisioned for STiRoT in HDPL1, and for OEMuRoT in HDPL2. The keysae generated by calling theRSSLiataProviigAPl.ThisAPonthe first call genrates and stores keys: AHK for OBKeys, AHK for MCE1, and AHK for MCE2.

The MCE keys are then stored into OBKey HDPL1 for STiRoT usage and in HDPL2 for OEMuRoT usage. STiRoT ll u intt  vin he generated keys, which explains why STiRoT MCE keys are always different per product or device.

OEMuRoT uses the randomly generated AHK-MCE1 in HDPL2, which explains why these OEMuRoT keys are by e in oani o same MCE key for all products.

The HDPL temporal isolation enables the advantage of having keys provisioned for HDPL lower-level autmaticaly protecte inhigher DPL lvel. In the MCE usage, the configurationf the MCE to prot he OEMuRoT image is set in HDPL1 by STiRoT. When the OEMuRoT is running in HDPL2, it has all MCE keys automatically protected by the HDPL1.

Inadition, he conguratin MCE protect heuse alication mage  inHDPL b eOMuRT.All the aplatins nig  HDPL3 fom extal fash memory have alltherMCE keys utaially prote y HDPL2.

![](images/38847022f8f0adaad42ebcf71e6e53f92e1eb670a89dfe298f95caba633b7bd8.jpg)  
Figure 6. AHK-MCE provisioning

# 8 Debugging application in the MCE use cases

Degig a application, when MCE must eusdepends n he cestate he product. When the (locked), or can be opened using the debug authentication (DA) with certificates.

Debug on HDPL3 can be performed without compromising the MCE keys on a closed product thanks to the debug authentication.

Debugging a product during development, in open state, when MCE encryption is required, can rely on MCE usvelot Tet  a n mplat ey regions, and context as done by the MCE example provided in the STM32CubeH7RS V1.0.0 or higher. A cutoiz etup metho also possible rexample by calnga servie adean execu omheRAM.

Degig  produc nheflwhenhe tat cosed and the MCEecpton s quiran ye MCE setup in HDPL1 (STiRoT AHK-MCE keys) or HDPL2 (OEM-uRoT AHK-MCE or OEMuRoT same key). The uermustu he debug authentcation open debugrLan   breakpoint n heu apl (HDPL3). After reset, the execution goes through the RSS, then through the STiRoT (HDPL1) to launch the uRoT (HDPL which then launcheshe serappliation n HDPL3.Accordingly is possble dee uplatin c  son  he eut arHLWithhtin eC   ot they are managed by the HDPL2.

# 9 MCE use cases in manufacturing

The STM32H7Sx provisioning and programming steps covered during manufacturing depend on whether the manacturiviomentrusteotTheeuwanstllatin Feendent manufacturing environment and not required when the environment is trusted.

The AN6103, "Third party programmers guide for the STM32H7R/S MCUs", can help the third party companies specialized in programmers tounderstand the programming and loading steps covereduring hemanufacuring of STM32H7R/S products. (An NDA is required to have access to AN6103).

# Revision history

Table 7. Document revision history   

<table><tr><td>Date</td><td>Version</td><td>Changes</td></tr><tr><td>09-Apr-2024</td><td>1</td><td>Initial release.</td></tr></table>

# Contents

1 MCE (memory cipher engine) overview.

2 MCE implementation in STM32H7Sx

2.1 MCE1 implementation 3

2.1.1 Block mode .  
2.1.2 Stream mode

2.2 MCE2 and MCE3 implementation 4

2.3 Selecting an MCE configuration 4

MCE configuration and external flash regions . 6

# Recommended keys for external memory protection 9

4.1 MCE usage with a different key per device 9

4.2 MCE usage with the same key for all devices . 9

MCE protection in case of XiP. 11

MCE protection in case of "Ioad and run" 13

MCE key provisioning with different keys 15

Debugging application in the MCE use cases 16

MCE use cases in manufacturing 17

Revision history 18

List of tables 20

List of figures. 21

# List of tables

Table 1. Applicable products   
Table 2. MCE Main features 2   
Table 3. MCEs performances comparison . 5   
Table 4. MCE1 configuration selection 5   
Table 5. MCE2 and MCE3 configuration selection 5   
Table 6. External flash slot protection with MCE and non-MCE keys. 12   
Table 7. Document revision history . 18

# List of figures

Figure 1. MCE block diagram. 2   
Figure 2. STM32H7S MCE instances 3   
Figure 3. Typical internal and external flash mapping versus MCE regions. 7   
Figure 4. MCE usage in the context of L&R from external RAM 13   
Figure 5. MCE usage in the context of L&R from internal RAM. 14   
Figure 6. AHK-MCE provisioning 15

# IMPORTANT NOTICE  READ CAREFULLY

pt old ursant  dits   leole.

purchasers' products.

No license, express or implied, to any intellectual property right is granted by ST herein.

are the property of their respective owners.

I

© 2024 STMicroelectronics - All rights reserved