# Getting started with STM32H723/733, STM32H725/735 and STM32H730 Value Line hardware development

# Introduction

Tploner hevelti as STM32H730 microcontroller lines, and need an implementation overview of the following hardware features:

Power supply Package selection Clock management Reset control Boot mode settings Debug management.

Thcentescbesheiharwaurcesquievlolicatin bas32/3, STM32H725/35 and STM32H730 microcontrollers.

# Reference documents

STM32H72x and STM32H73x datasheets STM32H723/733, STM32H725/735 and STM32H730 advanced Arm®-based 32-bit MCUs (RM0468) STM32H723/733, STM32H725/735 and STM32H730 errata sheet (ES0491)

The following documents are available on www.st.com website.

Oscillator design guide for STM8S, STM8A and STM32 microcontrollers application note (AN2867) STM32 microcontroller system memory boot mode application note (AN2606).

# General information

# Note:

This document applies to STM32H723/33, STM32H725/35 and STM32H730Arm®-based microcontroller lines.   
Arm is a registered trademark of Arm Limited (or its subsidiaries) in the US and/or elsewhere.

# 2

# Power supplies

# 2.1 Introduction

The STM32H723/33, STM32H725/35 and STM32H730 are highly integrated microcontrollers that are based on the Arm® Cortex®-M7 32-bit core (refer to the datasheets/databriefs for details).   
The STM32H723/33, STM32H725/35 and STM32H730 microcontrollers require at least one single power supply to be fully operational.

Atinal power sppliesoltag eerences require or soeuscaseshe general desi guielns are explained in the following sections. The figure below illustrates the power supply layout.

In all the diagrams, the gray boxes represent power domains.

![](images/390e5b7dfe721df9f2fb2ad8043c6d467720a4d7a17d2d0785eeab68885e1360.jpg)  
Figure 1. Power supplies

# Note:

VDDSMPS, VLXSMPS, VFBSMPS and VSSSMPS are available only on STM32H725/735 and STM32H730 devices.

Note:

On STM32H723/733, VDDLDO is not available on a pin/ball. It is internally connected to VDD.

Table 1. PWR input/output signals connected to package pins/balls   
Refer to Figure 2. System supply configuration for the different possible configuration   

<table><tr><td rowspan=1 colspan=1>Pin name</td><td rowspan=1 colspan=1>Signal type</td><td rowspan=1 colspan=1>Description</td></tr><tr><td rowspan=1 colspan=1>VDD</td><td rowspan=1 colspan=1>Supply input</td><td rowspan=1 colspan=1>Main I/O and VDD domain supply input.</td></tr><tr><td rowspan=1 colspan=1>VSS</td><td rowspan=1 colspan=1>Supply input</td><td rowspan=1 colspan=1>Main ground.</td></tr><tr><td rowspan=1 colspan=1>VDDA</td><td rowspan=1 colspan=1>Supply input</td><td rowspan=1 colspan=1>External analog power supply for analog peripherals.</td></tr><tr><td rowspan=1 colspan=1>VSSA</td><td rowspan=1 colspan=1>Supply input</td><td rowspan=1 colspan=1>Separated isolated ground for analog peripherals.</td></tr><tr><td rowspan=1 colspan=1>VBAT</td><td rowspan=1 colspan=1>Supply input/output</td><td rowspan=1 colspan=1>Backup battery supply: optional external supply for backup domain when VDD is notpresent. Can also be used to charge the external battery.</td></tr><tr><td rowspan=1 colspan=1>VDDSMPS</td><td rowspan=1 colspan=1>Supply input</td><td rowspan=1 colspan=1>Supply for switch mode power supply (SMPS) step-down converter.</td></tr><tr><td rowspan=1 colspan=1>VLXSMPS</td><td rowspan=1 colspan=1>Supply output</td><td rowspan=1 colspan=1>SMPS step-down converter output.</td></tr><tr><td rowspan=1 colspan=1>VFBSMPS</td><td rowspan=1 colspan=1>Supply regulation input</td><td rowspan=1 colspan=1>SMPS feedback voltage sense.</td></tr><tr><td rowspan=1 colspan=1>VSSSMPS</td><td rowspan=1 colspan=1>Supply input</td><td rowspan=1 colspan=1>Ground for SMPS step-down converter.</td></tr><tr><td rowspan=1 colspan=1>VDDLDO</td><td rowspan=1 colspan=1>Supply input</td><td rowspan=1 colspan=1>Supply for the integrated low drop out regulator.</td></tr><tr><td rowspan=1 colspan=1>VCAP</td><td rowspan=1 colspan=1>Supply input/output</td><td rowspan=1 colspan=1>Figure. System supply configuration shows the different possible regulator supplyconfigurations: using one, both or none.Digital Core supply input / output pin. Is either provided by the embedded regulator orfrom an external source.()</td></tr><tr><td rowspan=1 colspan=1>VDD50USB</td><td rowspan=1 colspan=1>Supply input</td><td rowspan=1 colspan=1>Supply for USB regulator.</td></tr><tr><td rowspan=1 colspan=1>VDD33USB</td><td rowspan=1 colspan=1>Supply input/output</td><td rowspan=1 colspan=1>Embedded USB regulator output or external USB supply when the internal regulator isnot used.</td></tr><tr><td rowspan=1 colspan=1>VREF+</td><td rowspan=1 colspan=1>Supply input/output</td><td rowspan=1 colspan=1>Reference voltage for ADCs and DACs. Can be generated through the internalVREFBUF or provided by an external source.</td></tr><tr><td rowspan=1 colspan=1>VREF-</td><td rowspan=1 colspan=1>Supply input</td><td rowspan=1 colspan=1>Ground reference for ADCs and DACs.</td></tr><tr><td rowspan=1 colspan=1>PDR_ON</td><td rowspan=1 colspan=1>Digital input</td><td rowspan=1 colspan=1>Control signal to switch the integrated POR/PDR circuitry ON/OFF.</td></tr></table>

![](images/09a4163a770e97d56b586c6942f3180369ab6ae1dc3659b1cd434c2b9150e16e.jpg)  
Figure 2. System supply configuration

# 2.1.1

# External power supplies and components

Refer to the STM32H72x and STM32H73x datasheets for more details on the electrical characteristics.

Table 2. Power supply connection   

<table><tr><td colspan="1" rowspan="1">Package pin/ball</td><td colspan="1" rowspan="1">Voltage range</td><td colspan="1" rowspan="1">External components</td><td colspan="1" rowspan="1">Comments</td></tr><tr><td colspan="1" rowspan="1">VDD</td><td colspan="1" rowspan="1">1.62 to 3.6 V</td><td colspan="1" rowspan="1">100 nF ceramic, for each VDD asclose as possible of the pins. A 4.7 μF ceramicconnected to one of the VDD pin.</td><td colspan="1" rowspan="1">For VDD &lt; 1.71 V the PDR must be disabled (see Section2.2.1 Power-on reset (POR)/power-down reset (PDR))</td></tr><tr><td colspan="1" rowspan="4">VDDA</td><td colspan="1" rowspan="1">1.62 to 3.6 V</td><td colspan="1" rowspan="1"></td><td colspan="1" rowspan="1">VDDA can be connected to VDD through a ferrite bead.</td></tr><tr><td colspan="1" rowspan="1">1.8 to 3.6 V</td><td colspan="1" rowspan="1">1 µF ceramic and 100 nF as close as possible</td><td colspan="1" rowspan="1">Restriction if a DAC or VREFBUF is used.</td></tr><tr><td colspan="1" rowspan="1">2.0 to 3.6 V</td><td colspan="1" rowspan="2">of the pin</td><td colspan="1" rowspan="1">Restriction if an OPAMP used.</td></tr><tr><td colspan="1" rowspan="1">0 to 3.6 V</td><td colspan="1" rowspan="1">DAC, ADC, OPAMP, COMP, VREFBUF are not used.</td></tr><tr><td colspan="1" rowspan="1">VBAT</td><td colspan="1" rowspan="1">1.2 to 3.6 V</td><td colspan="1" rowspan="1">1 µF ceramic and 100 nF close to the VBAT pin</td><td colspan="1" rowspan="1">Can be connected directly to an external battery orsupply.The external battery can be charged through the internal5 kΩ or 1.5 kΩ resistor (see the reference manualSTM32H723/733, STM32H725/735 and STM32H730advanced Arm®-based 32-bit MCUs (RM0468).To be connected to VDD when not used.When the PDR_ON pin is set to Vss the VBAT pin mustbe connected to VDD since this functionality is no longeravailable.</td></tr><tr><td colspan="1" rowspan="4">VDDSMPS</td><td colspan="1" rowspan="1">O V</td><td colspan="1" rowspan="1">No capacitor required.</td><td colspan="1" rowspan="1">VDDSMPS connected to Vss when the converter is notused.</td></tr><tr><td colspan="1" rowspan="1">1.62 to 3.6 V =VDD</td><td colspan="1" rowspan="1">Four different solutions are recommended:</td><td colspan="1" rowspan="1">For SMPS supplying VcORE-</td></tr><tr><td colspan="1" rowspan="1">2.3 to 3.6 V =VD</td><td colspan="1" rowspan="1">10 μF (best cost trade-off), ESR 10mΩ2x 10 µF (best area/performance trade-off)10 µF + 100 nF close from pin (best cost/</td><td colspan="1" rowspan="1">For SMPS output regulated to 1.8 V.The SMPS supplies the LDO regulator or an externalregulator.</td></tr><tr><td colspan="1" rowspan="1">3 to 3.6 V = VDD</td><td colspan="1" rowspan="1">performance trade-off)10 μF + 4.7 µF (best performance)</td><td colspan="1" rowspan="1">For SMPS output regulated to 2.5 V.The SMPS supplies the LDO regulator or an externalregulator.</td></tr><tr><td colspan="1" rowspan="1">VLXSMPS</td><td colspan="1" rowspan="1">VCORE Or 1.8 V or 2.5 V</td><td colspan="1" rowspan="1">When the SMPS is used:2.2 μH (DCR 110mΩ, Isat 1.7 A, Itemp1. A) as close as possible to VLxSMPS.LQFP/BGA packages: 220 pF ceramiccapacitor on VLXSMPS.2x 10 µF (ESR 5 mΩ) close to theinductor on VFBSMPS connection side.</td><td colspan="1" rowspan="1">Depending on the use case, the SMPS provides thedigital core supply or a supply provided to anotherregulator (external or internal LDO).See Figure 2. System supply configuration for connection</td></tr><tr><td colspan="1" rowspan="1">VFBSMPS</td><td colspan="1" rowspan="1">VCoRE or 1.8 Vo 2.5 V</td><td colspan="1" rowspan="1"></td><td colspan="1" rowspan="1">Refer to Figure 2. System supply configuration for theuse case dependent of this pin.</td></tr><tr><td colspan="1" rowspan="1">VDDLDO</td><td colspan="1" rowspan="1">1.62 to 3.6 V</td><td colspan="1" rowspan="1">When the LDO is used: 1x 4.7 μF capacitorclose to one VDDLDOx pin, all VDDLDOx pinscorrectly connected together.Otherwise: no capacitor is required. ConnectVDDLDOx to VDD.</td><td colspan="1" rowspan="1">VDDLDO ≤ VDD.Up to three VDDLDO pins available depending on thepackage specification.</td></tr><tr><td colspan="1" rowspan="1">VCAP</td><td colspan="1" rowspan="1">VOS0/VOS1/VOS2/VOS3/SVOS3/SVOS4ISVOS5</td><td colspan="1" rowspan="1">LDO enabled and SMPS enabled or disabled:2.2 μF ESR &lt; 100 mΩ for VCAP12.2 µF ESR &lt; 100 mΩ for VCAP2LDO disabled:100 nF close to each VCAPx pinVCAPx connected together</td><td colspan="1" rowspan="1">If the VCAP3 pin is available (depending on thepagt   VCAP but no additional capacitance is required.In bypass mode the Vcore supply is externally providedthrough the VCAPx pins.</td></tr><tr><td colspan="1" rowspan="1">VDD50USB</td><td colspan="1" rowspan="1">4.0 to 5.5 V</td><td colspan="1" rowspan="1">4.7 μF ceramic</td><td colspan="1" rowspan="1">Connected to an external supply or USB VBUS for aninternal USB regulator use case.Connected to VDD33USB when the internal USBregulator is not used (for packages having this pinavailable).</td></tr><tr><td colspan="1" rowspan="2">VDD33USB</td><td colspan="1" rowspan="1">3.0 V to 3.6 V</td><td colspan="1" rowspan="1">1 µF ceramic and 100 nF ceramic (USB reg notused)1 µF max ESR 600 mΩ (USB reg used)</td><td colspan="1" rowspan="1">The VD33us supply can be provided externally orthrough the internal USB regulator.When the regulator is enabled its output will be provideddirectly to the VDD33USB through the internalconnection.This pin is internally tied to VDD when it is not present insome specific packages. In consequence, the VDDsupply level must be compliant with VDD33 if the USB isused for these packages.</td></tr><tr><td colspan="1" rowspan="1">0V to 3.6 V</td><td colspan="1" rowspan="1">-</td><td colspan="1" rowspan="1">When USB is not used.</td></tr><tr><td colspan="1" rowspan="3">VREF+</td><td colspan="1" rowspan="1">1.62 V to≤ VDDA</td><td colspan="1" rowspan="1">1 µF ceramic and100 nF ceramic close to the pin</td><td colspan="1" rowspan="1">VREF+ is provided externally.In some packages, the VREF+ pin is not available(internally connected to VDDA).</td></tr><tr><td colspan="1" rowspan="1">2 V to≤ VDDA</td><td colspan="1" rowspan="1">or connected to VDDA through a resistor(typically 47 )</td><td colspan="1" rowspan="1">External VREF+ with VDDA&gt;2 V and ADC used.</td></tr><tr><td colspan="1" rowspan="1">VREFBUFreferenceoltage</td><td colspan="1" rowspan="1">1 μF</td><td colspan="1" rowspan="1">VREF+ is provided by the embedded VREFBUF regulator.Do not activate the internal VREFBUF when VREF+ isprovided externally</td></tr><tr><td colspan="1" rowspan="1">VREF-</td><td colspan="1" rowspan="1">VssA</td><td colspan="1" rowspan="1">Tied to VSSA</td><td colspan="1" rowspan="1">Only available in some packagesInternally tied to VssA when this pin is not present</td></tr><tr><td colspan="1" rowspan="2">PDR_ON</td><td colspan="1" rowspan="2">VDD or Vss</td><td colspan="1" rowspan="1">Tied to VDD</td><td colspan="1" rowspan="1">Power-on reset (POR) and power-down reset (PDR)circuit switched ONInternally tied to VDD when this pin is not present in aspecific package.VDD: 1.71 to 3.6 V</td></tr><tr><td colspan="1" rowspan="1">Tied to VSS</td><td colspan="1" rowspan="1">POR and PDR circuit switched offVDD: 1.62 to 3.6 V</td></tr></table>

![](images/f22e5ea19935e50c7d940703c93b20907371a89fcba08a50aa66058af02b2c06.jpg)  
Figure 3. Power supply component layout

# 2.1.2

# Digital circuit core supply (Vcore)

vgua eee-ee y xtealuplyvolta bypass). The SMPS step-down converter can also be cascaded with the linear voltage regulator.

In R o VOSO to VOS3).

In  ooegvolauve pweonn olt SVOS3 to SVOS5).

For a detailed definition on the available power modes please read the power control (PWR) chapter f the reference manual STM32H723/733, STM32H725/735 and STM32H730 advanced Arm®-based 32-bit MCUs (RM0468).

# Independent analog supply and reference voltage

Trove nalog peripherl peormanc he analog peripheral feature independent power supply which can be separately filtered and shielded from noise on the PCB:

The analog supply voltage input is available on a separate VDDA pin.   
An isolated ground connection is provided on the VSSA pin.

T ensure betterADC and DAC accuracy, the reference voltage can be providd externally through the VREF+ pin, this however is not available in all packages.

he VREF- pin is available on some packages to improve the ground noise immunity.

The VDDA minmum value (VDDA_MiN) depends on the analog peripheral and on whether a referencevoltage is provided or not, refer to Table 2. Power supply connection for more details.

# 2.1.4

# Independent USB transceiver power supply

Thereare diffeent ways osupply heUSB transeivers,depending on VD33us and Vavaiabily

When the VDD5ouB pin is available, it can be used to supply an internal regulator dedicated to the USB transceivers.   
In this case,either he USB VBUS or an external power supply can beused to provide the requid volage. The internal regulator output supply is connected to the USB FS PHY and is also available on the VDD33USB pin (see Figure 1. Power supplies).

In this configuration, the VDDous voltage can rie either before or after the VDD power supply (see Figure 6. VDD50USB power supply).

An external capacitor must be connected to VDD33uSB (see Table 2. Power supply connection).

When the VDD33uB pin is available, it can be used to supply the internal transceiver. In this cas, the VDD33USB pin should receive a voltage ranging between 3.0 to 3.6 V. If the VDD50USB pin is available and the internal USB regulator is not used, VDD5ousB must be connected with the VDD33USB pin. As an example, when the device is powered at 1.8 V, an independent 3.3 V power supply can be applied to VDD33USB.

Whr uppoVA respected (see Figure 5. VDD33uSB connected to external power supply):

During the power-on and power-down phases (VDD < VDD minimum value), VDD33usB should always be lower than VDD.

VDD3usb rising and falling time specifications must be adhered to (refer to table power-up/power-down operating conditions for regulatoron and table power-up/power-downoperating conditions for regulator of provided in the STM32H72x and STM32H73x datasheets).

In operating mode, VDD33usB can be either lower or higher than VDD:

If a USB interface is used (USB OTG_HS / OTG_FS), the associated GPIOs powered by VDD33uSB operate between VDD33uSB_MIN and VDD33UsB_MAX(see Figure 5. VDD33USB connected to external power supply).

On some packages neither the VDD33USB pin, nor the VDD50USB pin are available, it is the VDD pin which supplies the VDD33usB through an internal connection.

• In this case, VDD is constrained by VDD33usB and must range between 3.0V and 3.6V

![](images/be52cd598a9ff6d5e1698604b7c38b268ba98b395a7cc24ec51aab112dd064e1.jpg)  
Figure 4. VDD33USB connected to VDD power supply

![](images/062d591b6441ba4701d0218859bf4e7ceb869781d73e6e263f9a4c860f109224.jpg)  
Figure 5. VDD33USB connected to external power supply

![](images/932eb851f4feeb0fa421cebc0aef85b4a010955881f964f2aec2fd702c8ff648.jpg)  
Figure 6. VDD50USB power supply

# 2.1.5

# Battery Backup domai

# Backup domain description

Tretain he content f eRTC Backup regisers, Bacu SRAM, and supply heRTC when DD  urff, the VBAT pin can be conected to an optional 1.2-3.6 V standby voltage supplied by a battery. Otherwis, VBAT must be conneced to another sour, uch a VDD.

When he Backup domain is supplied by VBAT (analog swih connected to VBAT sinceVD i ot present), te following functions are available:

PC14 and PC15 can be used for the LSE pins only.   
PC13 can be used as tamper pin (TAMP1).   
PC1 can be used as tamper pin (TAMP3).

DuringtrsTTEMPo delay at VD start-up orafter a Power-Down Reset (PDR) is detect, the powerswitch between VBAT and VDD remains connected to VBAT.

. njece inthVBA roug nnternal diodecoe betweenandhe poweswitch BT the powe supply/batty connecd to the VBAT pin canot support this curent injection, it is strgly recommended to connect an external low-drop diode between this power supply and the VBAT pin.

eer  theTM32H72x/73 datasheets or the actual valuef tsTTEMPO

# Battery charging

WhV el batBAhar al operation can be performed either through an internal 5 kΩ or 1.5 kΩ resistor. The resistor value can be configured by software.

Battery charging is automatically disabled in VBAT mode.

# 2.1.6 LDO voltage regulator

T oo ol  i disabledeven after any reset source except or a Power-on reset. For system supply configuration whee thi at o e ill ietayst ar  pa, pwe pply vaable exteal  Whei vilable  xteal is connected internally to VDD.

Fo hu h  plee u ve  .   
to Figure 2. System supply configuration for more details.

Te L n oe  urifent os.Oede coeson  tegulaorite O the three other modes to the regulator switched ON, in which case the mode depends on the application operating modes:

D Switched OFF:

The Vcore is supplied externally through the VCAP pin (bypass mode);   
Or the Vcore is supplied through the SMPS step-down converter (see Section 2.1.7 SMPS step-down converter).

In Run mode:

The LDO regulator supplies the core and the backup domains; The LDO regulator output voltage can be dynamically scaled by programming the voltage scaling (VOS0 to VOS3) depending on the required performance (see the reference manual STM32H723/733, STM32H725/735 and STM32H730 advanced Arm®-based 32-bit MCUs (RM0468)).

• In Stop mode

The LDO regulator output level is reduced to the state programmed before entering stop mode (SVOS3 to SVOS5). The register and the SRAMs content is kept. For Svos3, further power reduction can be achieved by setting the regulator in low power deep sleep mode (for SvOS4 and SvOS5 the low power deep sleep mode is set automatically).

In Standby mode:

The regulator is powered down. The registers and SRAM content are lost except for those related to the standby circuitry and the backup domain.

# 2.1.7

# SMPS step-down converter

The embedded switch mode power supply (SMPS) step-down converter has a higher efficiency than the embedded LDO regulator.

Byuing the MP, the overall system powerconsumption improvedor ll powermodes at he extra cst an additional external inductor.

efer to the STM32H72x and STM32H73x datasheets to compare power efficiencies.

See Figure 2. System supply configuration for the possible configurations

The SMPS ste-oncnverters always nableater Powern reset when s powersuply is provie e VDDSMPS pin. If it is disabled, it remains disabled even after any reset except for Power-on reset.

The regulated output at start-up is 1.36 V.

The three main SMPS configurations are:

The SMPS is used but the Vcore supply is provided by the internal LDO regulator.   
After start-up the SMPS can be set by software to provide a regulated output of 1.8V or 2.5 V.   
The SMPS is used but the Vcore supply is provided by an external regulator.   
Atr art-up the MP can be et b otare rovie a regulat utput  1.8 Vor .5 V.The eteal regulator must ensure the correct voltage scaling for the run and stop modes (VOSx and SVOSx).

The SMPS is directly connected to the VCAP pin and provides the regulated supply to the Vcore.

Run mode:

o The converter can be dynamically scaled by programming the voltage scaling (VOS0 to VOS3) to the required performance (see the reference manual STM32H723/733, STM32H725/735 and STM32H730 advanced Arm®-based 32-bit MCUs (RM0468)).

In Stop mode:

o The converter output level is reduced to the state programmed before entering stop mode (SVOS3 to SVOS5). The register and SRAM content is kept   
o For SvOs3, a further power reduction can be achieved by setting the converter in low power mode (for SvOS4 and SvOS5 the low-power mode is always set automatically).

In Standby mode:

The converter is powered down. Both the register and SRAM content is lost except for the content related to the standby circuitry and the backup domain.

# 2.2

# Reset and power supply supervisor

# 2.2.1

# Power-on reset (POR)/power-down reset (PDR)

The devices have an integrated POR/PDR circuitry which ensures correct operational start-up from 1.71 V. Thedevice remains in reset mode whileV is below a specifid thresholdVoR/R,without he need or an exteal ree crc  ilustrate gurowern reset/powdown eset wavoror moreeail concerning the POR/PDR threshold, refer to the electrical characteristics of the STM32H72x and STM32H73x datasheets.

![](images/81b3e2bc2025e9ec9fd256eb26bc1d021f26daecee6eb92e6b32f199d258c277.jpg)  
Figure 7. Power on reset/power down reset waveform

RT is aitey 77 s.V/ ising ge 1.7 V (typial and VRll egeis.2 V (typical). Refer to the STM32H72x and STM32H73x datasheets for the actual values.

For packages embedding the PDRON pin, the power supply supervisor is enabled by holding PDR_ON high. On other packages, the power supply supervisor is always enabled.

T po upply upeviso iheyeig e R qu un ev VDD higher than 1.71 V.

In this case, an external power supply supervisor has to monitor VDD and control the NRST pin.

The device must be maintained in reset mode as long as VDD is below 1.62 V. The implemented circuit is illustrated in Figure 8. Power supply supervisor interconnection with internal reset OFF.

![](images/3998cee643022e0bc32781e65df058b5c4032df1ddae31eca16d9c7e515d2f98.jpg)  
Figure 8. Power supply supervisor interconnection with internal reset OFF

Tesply rne whi nevrobelow .Veanage morfetivey singhentealcc additional components are needed, thanks to the fully embedded reset controller).

When heepwsuply pevisoreoin negratatue e lnge:

The brown out reset (BOR) circuitry must be disabled The embedded programmable voltage detector (PVD) is disabled VBAT functionality is no longer available and VBAT pin must be connecte

# 1.2.2 Brownout reset (BOR)

Itn eBOR eese ystn ntVuppolt the selected VBOR threshold (also selected through option bytes, see the reference manual STM32H723/733, STM32H725/735 and STM32H730 advanced Arm®-based 32-bit MCUs (RM0468))

Three BOR levels are possible (2.1 V, 2.4 V, 2.7 V) (see the STM32H72x and STM32H73x datasheets for the electrical characteristics)

# Programmable voltage detector (PVD)

The VD can e use  monior theV owe supply y cmparing it  a trehold selected by the L [ bits in the PWR power control register (PWR_CR1).

The PVD is enabled by setting the PVDE bit.

The selectable threshold is between 1.95 V and 2.85 V (see the reference manual STM32H723/733, STM32H725/735 and STM32H730 advanced Arm®-based 32-bit MCUs (RM0468)).

APVDO flag s available n the PWR powe control/status register (PWRCSR1,  ndicate  VDD shie hanlen all t if enabled through the EXTI registers.

The PVD output interrupt can be generated when VDD drops below the VD threshold and/or when VDD rises abvhe VD rehold depending n EXTI in igfaling ege coniguratin.As a example, the vie routine could perform emergency shutdown tasks.

# 2.2.4

# Analog voltage detector (AVD)

Te AVD can e us monir VDDA powe supply  cmparig t  a threhold selechrough theALS[1:0] bit of the PWR power control register (PWRCR1). The threshold value can be configured to 1.7, 2.1, 2.5 2.8 V (refer to the STM32H72x and STM32H73x datasheets for the actual values).

The AVD is enabled by setting the AVDEN bit in PWRCR1 register. An interrupt can be raised when VDDAgoes above or below the configured threshold.

# 2.2.5 System reset

A   u al  S register and the registers in the backup domain (see Figure 9. Reset circuit).

system reset is generated when one of the following events occurs:

1. A low level on the NRST pin (external reset)   
2. Window watchdog end of count condition (WWDG reset)   
3. Independent watchdog end of count condition (IWDG reset)   
4. A software reset (Software reset)   
5. A low-power management reset.

![](images/1e61e93d77f4ace110f03e13138f88dec7956d1e82f5dd7a9ed9bf2537994385.jpg)  
Figure 9. Reset circuit

# 2.2.6

# Bypass mode

The power management uni is configurable by software with the option to bypass.When bypasse the ce power supply should be provided through VCAPx pins connected together.

In Bypass moe,henteal voltagscalngisotmanagternalyandheextealvolageval. 1.35 V) must be consistent with the targeted maximum frequency (see the STM32H72x and STM32H73x datasheets for the actual VOS level).

n Stop mode, it can be lowered to between 0.74 and 1.0 V (see datasheet for the actual SvOS level).

In Stay mode,he external sure will ewih f and hais pwe own The al source will be switched on when exiting Standby mode.

I B mo eeteal ole mus  et be the LDO, the external voltage must be kept above 1.15 V until the LDO is disabled by software.

# 3

# Clocks

# 3.1 Introduction

The STM32H723/33, STM32H725/35 and STM32H730 microcontrollers support several possible clock sources:

Two external oscillators (this will require external components):

High-speed external oscillator (HSE) Low-speed external oscillator (LSE).

Four internal oscillators:

High speed internal oscillator (HSI) High speed internal 48MHz oscillator (HSI48) Low-power internal oscillator (CSI) Low speed internal oscillator (LSI)

Three embedded PLLs can be used to generate the high frequency clocks for the system and peripherals.

For both the HSE and LSE, the clock can also be provided from an external source using the OCS_IN and OSC32_IN pins (HSE bypass and LSE bypass modes)

FigureClock generation an clock tree shematic shows theclock generation an clock tree architecure. For detail explanation refer to reference manual STM32H723/733, STM32H725/735 and STM32H730 advanced Arm®-based 32-bit MCUs (RM0468).   
The choice of clocks depends strongly on the application use case.   
Refer to the STM32H72x/ and STM32H73x datasheet for the electrical characteristics (range and accuracy)

![](images/71f9c8f198efa2bba1e00cd4587d4868b51642f64fcee422b72776078eeffd85.jpg)  
Figure 10. Clock generation and clock tree

Table 3. Clock connections   

<table><tr><td colspan="1" rowspan="1">Pin</td><td colspan="1" rowspan="1">External component</td><td colspan="1" rowspan="1">Comment</td></tr><tr><td colspan="1" rowspan="1">OSC32_IN</td><td colspan="1" rowspan="1">External clock input</td><td colspan="1" rowspan="1">LSE oscillatorLSE bypass input f≤ 1 MHz.</td></tr><tr><td>OSC32_IN</td><td>Typical example(1):</td><td>LSE oscillator input (see Figure 11. HSE/LSE clock source).</td></tr><tr><td rowspan="3">OSC32_OUT</td><td>Crystal: 32.768 kHz (6 pF, 50 KΩ)</td><td>LSE oscillator output</td></tr><tr><td>Capacitor: 2x 1.5 pF All components to be placed as close</td><td colspan="1">The external cap must be tuned because it isstrongly</td></tr><tr><td>as possible from the pins Unconnected in bypass</td><td colspan="1">dependent on the PCB design. Not used in bypass mode.</td></tr><tr><td rowspan="3">OSC_IN</td><td>External clock input</td><td>HSE oscillator</td></tr><tr><td></td><td colspan="1">HSE bypass input 4 MHz ≤ f ≤ 50 MHz.</td></tr><tr><td>Typical example(1): Crystal: 24 MHz (6 pF, 80 Ω)</td><td colspan="1">HSE oscillator input (see Figure 11. HSE/LSE clock source).</td></tr><tr><td rowspan="3">OSC_OUT</td><td>Capacitor: 2x 33 pF</td><td>HSE oscillator output</td></tr><tr><td>All components to be placed as close as possible from the pins</td><td colspan="1">The external cap must be tuned because it is strongly dependent on the PCB design.</td></tr><tr><td>Unconnected in bypass</td><td colspan="1">Not used in bypass mode.</td></tr><tr><td rowspan="2">I2S_CKIN</td><td rowspan="2">External clock input</td><td>External kernel clock input for audio interface SAI, DFSDM, I2S</td></tr><tr><td colspan="1">When an external clock reference is needed.</td></tr><tr><td rowspan="2">USB_PHY</td><td rowspan="2">External clock input</td><td>USB clock provided by the external PHY</td></tr><tr><td colspan="1">The embedded PHY supports FS</td></tr><tr><td>ETH_MII_TX_CLK/ ETH_MI_RX_CLK/ ETH RMII_REF_CLK</td><td>External clock input</td><td>For HS an external PHY needs to be used. Ethernet transmit and receive clock provided from an</td></tr><tr><td>MCO1</td><td>Internal clock output</td><td>external Ethernet PHY Some internal clocks can be provided to MCO1 pin.</td></tr><tr><td>MCO2</td><td>Internal clock output</td><td>An embedded divider allows frequency reduction See Figure 10. Clock generation and clock tree. Some internal clocks can be provided to MCO2 pin.</td></tr><tr><td></td><td></td><td>An embedded divider allows frequency reduction See Figure 10. Clock generation and clock tree. Synchronization source for the HSI48MHz embedded oscillator Clock Recovery System (CRS)</td></tr><tr><td>SYNC</td><td>External sync signal</td><td>One of the three possible sync signal, see the reference manual STM32H723/733, STM32H725/735 and STM32H730 advanced Arm®-based 32-bit MCUs (RM0468).</td></tr></table>

Oscilator design guide for STM8S, STM8A and STM32 microcontrollers application note (AN2867)

![](images/fbbe1e0af185c78b1b39b1200cfa4e1161b8b0a2a7758ba6d2a31269a4d713b0.jpg)  
Figure 11. HSE/LSE clock source

Table 4. Clock source generation   

<table><tr><td rowspan=1 colspan=1>Source</td><td rowspan=1 colspan=1>Frequency range</td><td rowspan=1 colspan=1>Externalcomponent</td><td rowspan=1 colspan=1>Comments</td></tr><tr><td rowspan=1 colspan=1>HSE</td><td rowspan=1 colspan=1>4 to 50 MHz</td><td rowspan=1 colspan=1>Yes</td><td rowspan=1 colspan=1>High Speed External clockUsed when a very accurate high speed clock is needed.</td></tr><tr><td rowspan=1 colspan=1>LSE</td><td rowspan=1 colspan=1>32.768 kHz(max 1 MHz)</td><td rowspan=1 colspan=1>Yes</td><td rowspan=1 colspan=1>Low Speed External clockUsed when a very accurate low speed clock is needed.For instance for the real time clock (RTC).</td></tr><tr><td rowspan=1 colspan=1>HSI</td><td rowspan=1 colspan=1>64 MHz</td><td rowspan=1 colspan=1>No</td><td rowspan=1 colspan=1>High Speed Internal ClockDefault system clock after a reset.</td></tr><tr><td rowspan=1 colspan=1>HSI48</td><td rowspan=1 colspan=1>48 MHz</td><td rowspan=1 colspan=1>No</td><td rowspan=1 colspan=1>High Speed Internal 48 MHz clockKernel clock for some peripherals.High precision clock for USB with Clock Recovery System which can usethe USB SOF signal.</td></tr><tr><td rowspan=1 colspan=1>CSI</td><td rowspan=1 colspan=1>4 MHz</td><td rowspan=1 colspan=1>No</td><td rowspan=1 colspan=1>Low Power Internal oscillatorFaster start-up time than HSICan be used for wake-up from Stop mode</td></tr><tr><td rowspan=1 colspan=1>LSI</td><td rowspan=1 colspan=1>32 KHz</td><td rowspan=1 colspan=1>No</td><td rowspan=1 colspan=1>Low Speed Internal clock, for independent watchdog (IWDG), RTC andauto-wakeup unit (AWU).This clock can run in Stop or Standby modes.</td></tr><tr><td rowspan=3 colspan=1>PLL</td><td rowspan=1 colspan=1>2 to 16 MHz input</td><td rowspan=2 colspan=1>No</td><td rowspan=1 colspan=1>Wide-range mode</td></tr><tr><td rowspan=1 colspan=1>1 to 2 MHz input</td><td rowspan=1 colspan=1>Low-range modeSome specific frequencies obtained with integer ratio which may beneeded for some application (e.g. Audio).</td></tr><tr><td rowspan=1 colspan=1>192 to 836 MHz VCOoutput</td><td rowspan=1 colspan=1></td><td rowspan=1 colspan=1>Integer or fractional ratios supported for all PLLs.</td></tr></table>

m weconptin closour nieeendenly whe.

Refer to the reference manual STM32H723/733, STM32H725/735 and STM32H730 advanced Arm®-based 32-bit MCU (RM0468) or  detaileddescription  the clock tree.This document provides a complete viewclock usage by peripheral is provided in the Kernel clock distribution overview.

# 3.1.1

# HSE and LSE bypass (external user clock)

In this mode, an external clock source must be provided to OSC_IN/OSC32_IN pins. For LSE bypass, the eal sure as  e "o ing".he ial ua us gle wi \~0% duty cce ri e OSC_IN/OSC32_IN pin.

# 3.1.2

# External crystal/ceramic resonator (HSE crystal)

The external oscillator has the advantage of producing a very accurate main clock.

Using a 25 MHz oscilator is a good choice for accurate USB OTG high-speed peripheral, I2S and SAI.

T la mzeu strtnn ar tablzatinTe apacanvalsuse according to the selected oscillator.

For CL1 and CL2, use high-quality ceramic capacitors in the 5 pF to 25 pF range (typical), designed forhihfrequency applications and selected to meet the requirements of the crystal or resonator. CL1 and CL2 are usually the same value.The crystal manufacturer typically specifis a load capacitance that ishe ries combination of CL1 and CL2. The PCB and MCU pin capacitances must be included when sizing CL1 and CL2 (10 pF can be used as a rough estimate for the combined pin and board capacitance).

The HSERDY flag in the RCC clock control register (RCCCR) indicates  the high-speed external oscior is enabled in the RCC clock interrupt register (RCC_CIR).

I it i ot use s cloc ur, he HSE cilatr can bei f uig he HSEON bi in the RCCco control register (RCC_CR).

# 3.2

# LSE oscillator clock

Tntauetealaoi oluoure real-time clock (RTC), clock/calendar and other timing functions.

l ren suitaheacil rovi datasheet (refer to Osillator design guide for STM8S, STM8A and STM32 microcontrollers application note (AN2867).

The driving capability is set through the LSEDRV [1:0] in RCC_BDCR register:

00: Low drive   
10: Medium low drive   
01: Medium high drive   
11: High drive.

The LSERDY flag in the RCC backup domain control register (RCC_BDCR) indicates whether the LSE crystal is interrupt can be generated if enabled in the RCC clock interrupt register (RCC_CIER).

The LSEcillator wihe any prrin he RCC backp macontrol e (RCC_BDCR).

# 3.3

# Clock security system (CSS)

The device provides two clock security systems (CSS), one or HSE oscillator and one for LSE ocillator. They can be independently enabled by software.

Wh co y HocHla up delay, and disabled when this oscillator is stopped:

I  latou ecty dectaseste cloc. Indy meani hat isu PLLiput clock, and the LL cock  he system clock When failure is detece the system clock swies to the HSI oscillator and the HSE oscillator is disabled. to the break inputs of the advanced-control timers TIM1, TIM8, TIM15, TIM16, and TIM17 and a non-maskable interrupt is generated to inform the software of the failure (clock security system interrupt rcc_hsecssit), allowing the MCU to perform the rescue operations needed. The rcc_hsecssit is linked to the Arm® Cortex®-M7 NMI (non-maskable interrupt) exception vector. • If the HSE oscillator clock was used as PLL clock source, the PLL is also disabled when the HSE fails.

The clock security system on LSE must be enabled only when the LSE is enabled and ready, and ater he clock has been selected through the RTCSRC[1:0] bits of RCC_BDCR register.

When an LSE failure is detected, the CSS on the LSE wakes the device up from all low-power modes except l LSE which is not automatic).

# Clock recovery system (CRS)

The clock recovery system (CRS) is dedicated to the internal HSI48 RC oscillator.

Toealaulty 48 MHz clock.

The CRS is ideally suited to provide a precise clock for the USB peripheral.

The CRS requires a synchronization signal.

Three possible sources are selectable with programmable pre-scaler and polarity:

SYNC external signal provided through pin;   
LSE oscillator output;   
USB SOF packet reception.

For more details refer to the reference manual STM32H723/733, STM32H725/735 and STM32H730 advanced Arm®-based 32-bit MCUs (RM0468).

# Alternate function mapping to pins

Tetivlyeploeheteat perhel ncion aping erhe32CubeX tol availbl www.st.com website.

# 4.1

# Analog inputs for ADC1, ADC2 and ADC3

The STM32H723/33, STM32H725/35 and STM32H730 microcontrollers embed four pads with a direct connection to the ADC (PAO_C; PA1_C; PC2_C; PC3_C).

It avoids the parasitic mpedancesa conventional pad and thereb ehancing the performance f he ADC. Figure . Analog inputs forADC1 and ADC2 shows the pad schematic (also available in the reference manual STM32H723/733, STM32H725/735 and STM32H730 advanced Arm®-based 32-bit MCUs (RM0468)).

![](images/bb698b1a14ee27d1faafc7d159981e4cb4f064f8732be2451d551a025301485d.jpg)  
Figure 12. Analog inputs for ADC1 and ADC2

Each ADC has 6 inputs optimized for high performance INPO to INP5 and INNO to INN5 (fast chanels).Rer to the ADC connectivity figure in the reference manual STM32H723/733, STM32H725/735 and STM32H730 advanced Arm®-based 32-bit MCUs (RM0468).

The other 14 channels have lower performance (slow channels)   
STM32CubeMX and the table "pin/ball definition" in the STM32H72x and STM32H73x datasheet show the availability of the Pxy_C and Pxy depending on the package.

# Packages having Pxy_C and Pxy pads available

The Pxy_C pads are routed with a direct connection to the ADC fast input channels.

For these packages, use the Pxy_C inputs for the ADC to get the best performance (see the STM32H72x and TM32H73x datasheets ADC characteristic table "Sampling rate for Direct channels")

The perforance of the Pxy standar pads connected to the ADC ast chanels are described in the TM32H7x and STM32H73x datasheets ADC characteristic table "Sampling rate for Fast channels

The performance of the Pxy standard pads connected to the ADC slow channels are described in the STM32H72x and STM32H73x datasheets ADC characteristic table "Sampling rate for Fast channels

# 4.1.2

# Packages having Pxy_C but not the peer Pxy

n some packages, the peer Pxy_C and Pxy is not available, only the Pxy_C ar

As described above these pads give the best performance for the ADC.

Telacntial eteali eeo p needs to be closed (PxySO bit).

In this way all the functionalities of the Pxy pad are available on the Pxy_C pad.

But there is an additional serial impedance due to this switch (300 Ω to 550 Ω) and additional parasitic capacitance (2.5 pF) which may impact timing sensitive signals.

STM32CubeMX and the table "Port A and Port C alternate function" of the STM32H72x and STM32H73x datasheets indicate the functions available on the PxyC pads by closing the switch between the two pad

# 4.1.3

# Package having Pxy available but nor the peer Pxy_C

Closing the switch in the pad (GPIOx_MODER bit) connects an ADC slow input to the Pxy pad (See Figure ADC connectivity in the reference manual STM32H723/733, STM32H725/735 and STM32H730 advanced Arm®-based 32-bit MCUs (RM0468). Also refer to the ADC STM32H72x and STM32H73x datasheets characteristic table "Sampling rate for Slow channels".

ie ppi pad. In this way, an ADC fast input is connected to the Pxy pad. The performance is improved but wil not however be as high as for a package having a direct input from a Pxy_C pad. (see the STM32H72x and STM32H73x datasheets ADC characteristic table "Sampling rate for Medium speed channels")

# 5 Boot configuration

# 5.1 Boot mode selection

In STM32H723/33, STM32H725/35 and STM32H730 microcontrollers, two different boot spaces can be selected through the BOOT pin and the boot base address programmed in the BOOT_ADD0 or BOOT_ADD1 option bytes as shown in the Table 5. Boot modes.

Table 5. Boot modes   

<table><tr><td rowspan=1 colspan=2>Boot mode selection</td><td rowspan=2 colspan=1>Boot space</td></tr><tr><td rowspan=1 colspan=1>BOOT pin</td><td rowspan=1 colspan=1>BOOT pin Boot address option bytes</td></tr><tr><td rowspan=1 colspan=1>0</td><td rowspan=1 colspan=1>BOOT_ADD0 [15:0]</td><td rowspan=1 colspan=1>Boot address defined by BOOT_ADD0[15:0] user option byte.Default factory programmed value: User Flash memory starting at Ox0800 0000.</td></tr><tr><td rowspan=1 colspan=1>1</td><td rowspan=1 colspan=1>BOOT_ADD1 [15:0]</td><td rowspan=1 colspan=1>Boot address defined by BOOT_ADD1[15:0] user option byte.Default factory programmed value: System Flash memory starting at Ox1FF0 0000.</td></tr></table>

The BOOT_ADD0 and BOOT_ADD1 address option bytes allow the boot to be programmed to any boot memory address from 0x0000 0000 to 0x3FFF 0000 which includes:

All the Flash memory address space mapped on the AXIM interface.   
All the RAM address space: ITCM, DTCM RAMs and SRAMs mapped on the AXIM interface.   
The system memory bootloader.

The BOOT_ADD0/BOOT_ADD1option bytes can be modified after the reset in order to boot from any other boot address after the next reset.

If te programmed boot memory address is ou f thememory mapped arer a reserved area,he default boot fetch address is programmed as follows:

Boot address O: Flash memory at Ox0800 0000   
Boot address 1: ITCM-RAM at 0x0000 0000

When theFlash level protectionis nabled nly boot fom Flash memory is avalable  the boot adress programmed in the BOOT_ADD0 / BOOT_ADD1 option bytes is out of the memory range or belongs to the RAM address range, the default fetch will be forced to the Flash memory at address Ox0800 0000.

When the secure access mode is enabled through option bytes, the boot behavior differs from the above description (refer to section Root secure services of the product reference manual).

# 5.2

# Boot pin connection

Figure . Boot mode selection implementation example shows the external connection required to select the boot memory of STM32H723/33, STM32H725/35 and STM32H730 microcontrollers.

![](images/f89dc0017cbb0f0e0b1dd9675ae96effa5d890ca0b972ad426f37c1e6f4386bd.jpg)  
Figure 13. Boot mode selection implementation example

Resistor values are given only as a typical example.

# 5.3

# System bootloader mode

The beebootadrcodeis locate ihe ystememory. I is programmed   durg producti. It is used to reprogram the Flash memory using one of the following serial interfaces.

Table 6. STM32H723/733, STM32H725/735 and STM32H730 microcontroller bootloader communication peripherals shows the supported communication peripherals by the system bootloader.

Table 6. STM32H723/733, STM32H725/735 and STM32H730 microcontroller bootloader communication peripherals   

<table><tr><td rowspan=1 colspan=1>Bootloader peripherals</td><td rowspan=1 colspan=1>Bootloader pins</td></tr><tr><td rowspan=1 colspan=1>DFU</td><td rowspan=1 colspan=1>USB OTG FS (PA11/PA12) in device mode</td></tr><tr><td rowspan=1 colspan=1>USART1</td><td rowspan=1 colspan=1>PA9/PA10</td></tr><tr><td rowspan=1 colspan=1>USART2</td><td rowspan=1 colspan=1>PA2/PA3</td></tr><tr><td rowspan=1 colspan=1>USART3</td><td rowspan=1 colspan=1>PB10/PB11 or PD8/PD9</td></tr><tr><td rowspan=1 colspan=1>FDCAN1</td><td rowspan=1 colspan=1>PH13/PH14 or PD0/PD1</td></tr><tr><td rowspan=1 colspan=1>I2C1</td><td rowspan=1 colspan=1>PB6/PB9</td></tr><tr><td rowspan=1 colspan=1>I2C2</td><td rowspan=1 colspan=1>PFO/PF1</td></tr><tr><td rowspan=1 colspan=1>I2C3</td><td rowspan=1 colspan=1>PA8/PC9</td></tr><tr><td rowspan=1 colspan=1>SPI1</td><td rowspan=1 colspan=1>PA4/PA5/PA6/PA7</td></tr><tr><td rowspan=1 colspan=1>SPI3</td><td rowspan=1 colspan=1>PA15/PC10/PC11/PC12</td></tr><tr><td rowspan=1 colspan=1>SPI4</td><td rowspan=1 colspan=1>PE11 / PE12 / PE13 / PE14</td></tr></table>

# 6

# Debug management

# 6.1 Introduction

The host / target interface is the hardware equipment that connects the host to the application boar.This ina ma  entaraebgol  JTAG W conor  able o thehost edebg touHos bor coen illustrat ecoion  eos evaluation board.

![](images/ffedad70d2c1f04944cad7d299a9b17a764ae6efe9765fb3de0eefcb070420ba.jpg)  
Figure 14. Host to board connection

# 6.2

# SWJ debug port (serial wire and JTAG)

The core of the STM32H723/33, STM32H725/35 and STM32H730 microcontrollers integrates the serial wire / JTAG debug port (SWJ-DP). It is an Arm® standard CoreSight™ debug port that combines a 5-pin JTAG-DP interface and a 2-pin SW-DP interface.

The JTAG debug port (JTAG-DP) provides a 5-pin standard JTAG interface to the AHP-AP port.   
The serial wire debug port (SW-DP) provides a 2-pin (clock + data) interface to the AHP-AP port.

In the SWJ-DP, the two SW-DP JTAG pins the are multiplexed with some of the JTAG-DP five JTAG pins. For more details on the SWJ debug port refer to the reference manual STM32H723/733, STM32H725/735 and STM32H730 advanced Arm®-based 32-bit MCUs (RM0468) SWJ debug port section (serial wire and JTAG).

# 6.2.1 TPIU trace port

Te trace port coprs urdata oututs pus e clock outut.e numbr data utputs an e cure otareau als n  uses G.  e trace port otequirel signals can be used as GPIOs. By default, the trace port is disabled.

T aat  clocra   eul ust k wi enough space to attach the trace port analyzer probe.

Refer to Table 7. TPIU trace pins for a summary of trace pins and GPIO assignment.

Table 7. TPIU trace pins   

<table><tr><td rowspan=1 colspan=1>Trace pin name</td><td rowspan=1 colspan=1>Type</td><td rowspan=1 colspan=1>Description</td><td rowspan=1 colspan=1>Pin assignment</td></tr><tr><td rowspan=1 colspan=1>TRACEDO</td><td rowspan=1 colspan=1>Output</td><td rowspan=1 colspan=1>Trace synchronous data out 0</td><td rowspan=1 colspan=1>PC1 or PE3 or PG13</td></tr><tr><td rowspan=1 colspan=1>TRACED1</td><td rowspan=1 colspan=1>Output</td><td rowspan=1 colspan=1>Trace synchronous data out 1</td><td rowspan=1 colspan=1>PC8 or PE4 or PG14</td></tr><tr><td rowspan=1 colspan=1>TRACED2</td><td rowspan=1 colspan=1>Output</td><td rowspan=1 colspan=1>Trace synchronous data out 2</td><td rowspan=1 colspan=1>PD2 or PE5</td></tr><tr><td rowspan=1 colspan=1>TRACED3</td><td rowspan=1 colspan=1>Output</td><td rowspan=1 colspan=1>Trace synchronous data out 3</td><td rowspan=1 colspan=1>PC12 or PE6</td></tr><tr><td rowspan=1 colspan=1>TRACECLK</td><td rowspan=1 colspan=1>Output</td><td rowspan=1 colspan=1>Trace clock</td><td rowspan=1 colspan=1>PE2</td></tr></table>

# 6.2.2

# External debug trigge

The bidirectional TRGIO signal can be configured as TRGIN or TRGOUT by software. Refer tTable . External debug trigger pins for a summary of trigger pins and GPlO assignment.

Table 8. External debug trigger pins   

<table><tr><td rowspan=1 colspan=1>Trigger pin name</td><td rowspan=1 colspan=1>Type</td><td rowspan=1 colspan=1>Description</td><td rowspan=1 colspan=1>Pin assignment</td></tr><tr><td rowspan=1 colspan=1>TRGIO</td><td rowspan=1 colspan=1>Input/output</td><td rowspan=1 colspan=1>Bidirectional external trigger</td><td rowspan=1 colspan=1>PC7</td></tr></table>

# 6.3 Pinout and debug port pins

STM32H723/33, STM32H725/35 and STM32H730 microcontrollers are available in various packages with diebe pisulscality elathe vbily  paral interface) and will differ between the packages.

# 6.3.1

# SWJ debug port pins

Five pins are used as outputs from the STM32H723/33, STM32H725/35 and STM32H730 microcontrollers for the SWJ-DP as alternate general-purpose Ounctionshese pins areavailable on l packages and detail Table 9. SWJ debug port pins.

Table 9. SWJ debug port pins   

<table><tr><td rowspan=2 colspan=1>SWJ-DP pin name</td><td rowspan=1 colspan=2>JTAG debug port</td><td rowspan=1 colspan=2>SW debug port</td><td rowspan=2 colspan=1>Pin assignment</td></tr><tr><td rowspan=1 colspan=1>Type</td><td rowspan=1 colspan=1>Description</td><td rowspan=1 colspan=1>Type</td><td rowspan=1 colspan=1>Debug assignment</td></tr><tr><td rowspan=1 colspan=1>JTMS/SWDIO</td><td rowspan=1 colspan=1>I</td><td rowspan=1 colspan=1>JTAG test modeselection</td><td rowspan=1 colspan=1>IO</td><td rowspan=1 colspan=1>Serial wire datainput/output</td><td rowspan=1 colspan=1>PA13</td></tr><tr><td rowspan=1 colspan=1>JTCK/SWCLK</td><td rowspan=1 colspan=1></td><td rowspan=1 colspan=1>JTAG test clock</td><td rowspan=1 colspan=1></td><td rowspan=1 colspan=1>Serial wire clock</td><td rowspan=1 colspan=1>PA14</td></tr><tr><td rowspan=1 colspan=1>JTDI</td><td rowspan=1 colspan=1></td><td rowspan=1 colspan=1>JTAG test data input</td><td rowspan=1 colspan=1>-</td><td rowspan=1 colspan=1></td><td rowspan=1 colspan=1>PA15</td></tr><tr><td rowspan=1 colspan=1>JTDO/TRACESWO</td><td rowspan=1 colspan=1>0</td><td rowspan=1 colspan=1>JTAG test data output</td><td rowspan=1 colspan=1></td><td rowspan=1 colspan=1>TRACESWO if asynchronous trace is enabled</td><td rowspan=1 colspan=1>PB3</td></tr><tr><td rowspan=1 colspan=1>NJTRST</td><td rowspan=1 colspan=1></td><td rowspan=1 colspan=1>JTAG test nReset</td><td rowspan=1 colspan=1>-</td><td rowspan=1 colspan=1></td><td rowspan=1 colspan=1>PB4</td></tr></table>

# 6.3.2

# Flexible SWJ-DP pin assignment

After RESET (SYSRESETn or PORESETn), allfive pins used for the SWJ-DP are assigned as dedicated pins imdiatelyvailable heeer ost notehat heractutae ot ssiexcept ly programmed by the debugger host).

However, the STM32H723/33, STM32H725/35 and STM32H730 microcontrollers offer the possibility of disabling some or allof the SWJ-DP ports and so freeing the associated pins for general-purpose IO (GPIO)usage.

Table 10. Flexible SWJ-DP assignment shows the different possibilies to release some pins.

Table 10. Flexible SWJ-DP assignment   

<table><tr><td rowspan=2 colspan=1>Available debug ports</td><td rowspan=1 colspan=5>SWJ IO pin assigned</td></tr><tr><td rowspan=1 colspan=1>PA13/JTMS/SWDIO</td><td rowspan=1 colspan=1>PA14/JTCK/SWCLK</td><td rowspan=1 colspan=1>PA15/JTDI</td><td rowspan=1 colspan=1>PB3/JTDO</td><td rowspan=1 colspan=1>PB4/NJTRST</td></tr><tr><td rowspan=1 colspan=1>Full SWJ (JTAG-DP + SW-DP) - reset state</td><td rowspan=1 colspan=1>X</td><td rowspan=1 colspan=1>X</td><td rowspan=1 colspan=1>X</td><td rowspan=1 colspan=1>X</td><td rowspan=1 colspan=1>X</td></tr><tr><td rowspan=1 colspan=1>Full SWJ (JTAG-DP + SW-DP) but without NJTRST</td><td rowspan=1 colspan=1>X</td><td rowspan=1 colspan=1>X</td><td rowspan=1 colspan=1>X</td><td rowspan=1 colspan=1>X</td><td rowspan=2 colspan=1></td></tr><tr><td rowspan=1 colspan=1>JTAG-DP disabled and SW-DP enabled</td><td rowspan=1 colspan=1>X</td><td rowspan=1 colspan=1>X</td><td rowspan=1 colspan=2></td></tr><tr><td rowspan=1 colspan=1>JTAG-DP disabled and SW-DP disabled</td><td rowspan=1 colspan=5>Released</td></tr></table>

For more details on how to disable SWJ-DP port pins, refer to the STM32H723/733, STM32H725/735 and STM32H730 advanced Arm®-based 32-bit MCUs (RM0468) I/O pin alternate function multiplexer and mapping section.

# 6.3.3

# Internal pull-up and pull-down on JTAG pins

The devices embed internal pul-ps and pull-downs to guarantee a correct JTAG behavior. Consequently, the them:

NJTRST: internal pull-up.   
JTDI: internal pull-up.   
JTMS/SWDIO: internal pull-up.   
JTCK/SWCLK: internal pull-down.   
JTDO: floating state (tristate)

I they are reconfigured by software. Special care must be taken with the TCK/SWCLK pin, which is directly co om teclock flos sc houl ottglo JTAG /Oslea byhe software.

# 6.3.4

# SWJ debug port connection with standard JTAG connector

Figure 15. JTAG connector implementation shows the connection between STM32H723/33, STM32H725/35 and STM32H730 microcontrollers and a standard JTAG connector.

![](images/66de838086aed6365d1c00bae7b4966726dbecddb7a2053d73764e7b1bb2b2c2.jpg)  
Figure 15. JTAG connector implementation

# 7 Recommendations

# 7.1 Printed circuit board

F the ground (Vss) and another dedicated to the VDD supply. This provides both good decoupling and good requirement is to ensure a good structure for the ground and the power supply.

# 2 Component position

erooleao-c ru oltal components.

# 7.3 Ground and power supply (Vss,VDD)

e   sigle poit. Lops must eavoidd rhaveaminum arThe powrsupply should  pleen antenna, and therefore will become the EMI main transmitter and receiver. All component-ree PCB areas must befilled with additional grounding to create adequate shielding (especially when using single-layer PCBs).

# 7.4 Decoupling

All the power supply and ground pins must be properly connected to the power supplies. These connections, v widths and, preferably, the use of dedicated power supply planes in multilayer PCBs.

In p pl ou le e pa o eoe pi ee  Tp val 00,u al depends n heaplication needsFiuTypical layout r ai hows he typical layu such a VDD/Vss pair.

![](images/9b95d12e28654718afdfd0ddab7893a3831e937cfce311b92c5c1fae8e096c26.jpg)  
Figure 16. Typical layout for VDD/Vss pair

# 7.5

# Other signals

When designing an application, the EMC performance can be improved by closely studying:

Sials o whic  temporary distubanc ffect thenig process peranentlyhe cas interupts and handshaking strobe signals, and not the case for LED commands). For these signals, a surrounding ground trace, shorter lengths and the absence of noisy and sensitive traces nearby (crosstalk effect) iove the MC performanc. For digital signals, the best possible electrical margin must bereace for the two logical states and slow Schmitt triggers are recommended to eliminate parasitic states.   
Noisy signals (such as clock).   
Sensitive signals (such as high impedance).

# 7.6 Unused l/Os and features

Allo %  he MCU urcs.T ceas h MC pocnu clockcnt r I/O hould l o    (ul  ul  e  p should be frozen or disabled.

# 8

# Reference design

# 8.1 Description

The STM32H725G-DK Discovery board and the NUCLEO-H723ZG and NUCLEO-H725ZG Nucleo boards are good references that can be used as a basis for a specific application development. Details of these boards are available on www.st.com website.

# Recommended PCB routing guidelines for STM32H723/733, STM32H725/735 and STM32H730 microcontrollers

# 9.1 PCB stack-up

In order to reduce the reflections on high speed signals, the impedance between the source, sink and tis avaecln with respect to any reference plane.

Trwi ageeiet peacentedene c acks miatiseum tace wih nspacg whic dep of PCB technology and cost requirements, a PCB stack-up needs to be chosen which addresses all the impedance requirements .

Tmiucguran hat an eus  4 r 6aye tack-p.An 8 layes boar may  qu very dense PCBs that have multiple SDRAM/SRAM/NOR/LCD components.

The foowing stack-ups (Figure 7. Four layer PCB stack-up example and Figure 18. Six layer PCB stack-p eaplaentendeas eamples which can esed  guide ies or stackup evaluation an eleon. Thesackcgurations placheND planaent he power pancs eapacitan reuce the physical gap between G and the power plane So high speed sigals n he top layer wil avea l GD eec panewhihels uc e MCsshere og heayes nda a GND reference for each PCB signal layer will further improve the radiated EMC performance.

![](images/291be27396ae569f1810566fd8b8b15d49808bde3a2c4b9aa2944d72ec7f2ccc.jpg)  
Figure 17. Four layer PCB stack-up example

![](images/c61dd7e8ff385ceba59be86dfd7866a91bb7a5f1de21e724871c6130a208a5d5.jpg)  
Figure 18. Six layer PCB stack-up example

# 9.2

# Crystal oscillator

Use the application note: Oscillator design guide for STM8S, STM8A and STM32 microcontrollers (AN2867), for further guidance on how to layout and route crystal oscillator circuits.

# 9.3

# Power supply decoupling

An adequate power decoupling for STM32H723/33, STM32H725/35 and STM32H730 microcontrollers is necessary to prevent excessive power and ground bounce noise. Refer to Section 2 Power supplies.

The following recommendations shall be followed:

Place the decoupling capacitors as close as possible to the power and ground pins of the MCU. For BGA packages, it is recommended to place the decoupling capacitors on the opposing side of the PCB (see Figure 19. Decoupling capacitor placement depending on package type).   
Add the recommended decoupling capacitors to as many VDD/Vss pairs as possible.   
Connect the decoupling capacitor pad to the power and ground plane with a wide and short trace/via. This reduces the serisinductance,maximizes the current fow and minimizes the transient voltage drops from the power plane and in turn reduces the ground bounce occurrence.

Figure 0. Example of decoupling capacitor placed underneath shows an example of decoupling capacitor placement underneath STM32H723/33, STM32H725/35 and STM32H730 microcontrollr, closer to the pins and with less vias.

![](images/4ae0d531cb5e6a59c07cac5d033c137957d96716fc99e31cea1fbed07a08aca0.jpg)  
Figure 19. Decoupling capacitor placement depending on package type

![](images/434283c01ae0597dbe8e6f14efb2a863fa3d04d02b593149dd38269fec66e5b3.jpg)  
Figure 20. Example of decoupling capacitor placed underneath

# High speed signal layout

# 9.4.1

# SDMMC bus interface

# Interface connectivity

The SD/SDIO MMC card host interface (SDMMC) provides an interface between the AHB peripheral bus and Multi Media Cards (MMCs), SD memory cards and SDIO cards. The SDMMC interface is a serial data bus interface, that consists of a clock (CK), command signal (CMD) and 8 data lines (D[0:7]).

# Interface signal layout guidelines

Reference the plane using GND or PWR (if PWR, add 1Onf switching cap between PWR and GND).   
Trace impedance: 50 Ω ± 10%.   
All clock and data lines should have equal lengths to minimize any skew.   
The maximum skew between data and clock should be less than 250 ps @ 10mm.   
The maximum trace length should be less than 20 mm. f the signal trace exceds this trace-length/speed criteria, then a termination should be used.   
The trace capacitance should not exceed 20 pF at 3.3 V and 15 pF at 1.8 V.   
The maximum signal trace inductance should be less than 16 nH.   
Use the recommended pullup resistance for CMD and data signals to prevent the bus from floating.   
The mismatch within data bus, data and CK or CK and CMD should be below 10mm.   
All data signals must have the same number of vias.

# Note:

The total capacitancef the memory card bu is he sumf theus master capacitanco, he bus capacitance CBus itself and the capacitance CcaRD of each card connected to this line. The total bus capacitance is CL= CHost + CBus + N\*CCard Where the host is an STM32H723/33, STM32H725/35 and STM32H730 microcontroller, the bus is all the signals and Card is SD card.

FguremicroS card interconnection example and Figure  card interconnection example show different typical use cases

![](images/1a20005238939ea9d775748800b395eb7c9eafc3e980b22a8e46519c39732de8.jpg)  
Figure 21. microSD card interconnection example

![](images/e1267905bcc3df1e2504dcd7c087fb670536173385a54a629cf718dad4ba1e4f.jpg)  
Figure 22. SD card interconnection example   
Only default 3.3 V Card signaling supported without level Translator

# 9.4.2

# Flexible memory controller (FMC) interface

# Interface connectivity

The FMC controller and in particular SDRAM memory controller are composed of many signals, most of them alolul

An address group which consists of row/column address and bank address.   
A command group which includes the row address strobe (NRAS), the column address strobe (NCAS), and the write enable (SDWE).   
A control group which includes a chip select bank1 and bank2 (SDNE0/1), a clock enable bank1 and bank2 (SDCKE0/1), and an output byte mask for the write access (DQM).

A data group/lane which contains 8 signals.

# Note:

It depends of the memory specification: SDRAM with x8 bus widths have only one data group, while x16 buswidth SDRAM have two lanes.

# Interface signal layout guidelines

For reference the plane using GND or PWR (if PWR), add 10 nf stitching cap between PWR and GND. Trace impedance: 50 Ω ± 10%.   
The maximum trace length should not exceed 120mm. If the signal trace exceeds this trace-length / speed criteria, then a termination should be used.   
To reduce the crosstalk, it is strongly recommended to place data tracks on the diferent layers to the address and control lanes. However, when the data and address / control tracks coexist on the same layer they must be separated from each other by at least 5 mm.   
Match the trace lengths for the data group within ± 10 mm of each other to reduce any excessive skew. Serpentine traces (this is an "S" pattern to increase trace length) can be used to match the lengths. Placng the clock (DCL) signal on an internal layer, minimizes the noise EM). Route the clock sial at les tree tmes he withetraceaway fomother sials.avoineesary peanc and reflection, avoid the use of vias as much as possible. Serpentine routing is to be avoided also. Match the clock traces to the data/address group traces length to within ±10 mm.   
Match the clock traces length to each signal trace in the address and command groups to within ±10 mm (with maximum of ≤ 20 mm).

Trace capacitances:

At 3.3 V keep the trace capacitance within 20 pF with overall capacitive loading (including Data, Address, SDCLK and Control) no more than 30 pF.   
At 1.8 V keep the trace capacitance within 15 pF with overall capacitive loading (including Data, Address, SDCLK and Control) no more than 20 pF.

# 9.4.3 Octo-SPI interface

# Interface connectivity

The OctoSPl is a specializedcommunication interface targeting single,dual, quad and octal communication. (Refer to the reference manual STM32H723/733, STM32H725/735 and STM32H730 advanced Arm®-based 32- bit MCUs (RM0468)) for details)

Refer to the STM32H72x and STM32H73x datasheets for the full electrical characteristic.

# Interface signal layout guidelines

Reference the plane using GND or PWR (if PWR, add 1Onf stitching cap between PWR and GND Trace impedance: 50 Ω for single-ended and 100 Ω for differential pairs (CLK/NCLK)   
The maximum trace length should be less than120 mm. If the signal trace exceeds this trace-length/sped criterion, then a termination should be used   
Avoid using multiple signal layers for the data signal routing.   
Route the clock signal at least three times the width of the trace away from other signals. To avoid unnecessary impedance changes and reflection, avoid the use of vias as much as possible. Serpentine routing is to be avoided also.   
Match the trace lengths for the data group within ± 10 mm of each other to reduce any excessive skew. Serpentie tracs his is an "S" shape pattern t incease trace lengh) can be used to match the lghs. Avs etteocsalan  pslehol via alters the impedance and adds a reflection to the signal.   
Avoid discontinuities on high speed traces (vias, SMD components).

Figure 23. Octo-SPI interconnection example and Figure 4. Octo-SPI multiplexed interconnection example illustrate possible interconnection examples.

If SMD components are needed, place these components symmetrically to ensure good signal quality.

![](images/823966f8cda5d1bf4f9ca3f4c643454a5633eff1b6a59539189ebbde54bdd1d7.jpg)  
Figure 23. Octo-SPI interconnection example

![](images/1fa96359978be09e6032ff54a18d3db37f4c9e0cabbce7d2f1ce246ab183560c.jpg)  
Figure 24. Octo-SPI multiplexed interconnection example

In multiplexed mode, the same bus can be shared between two external Octo-SPI memories.   
The multiplexed mode must be configured to avoid unwanted transactions when the OcTOSPls are disabled.   
The multiplexed mode can be very useful for some packages where the port2 is not mapped.

# 9.4.4 DFSDM interface

Thedigital filter or the sigma deltamodulator (DFSDM) is dedicated tothe external sigma-deltamodulator's interface (refer to the reference manual STM32H723/733, STM32H725/735 and STM32H730 advanced Arm® b C daiIa ess r u density modulation (PDM) microphones.

The DFSDM embedded in STM32H723/33, STM32H725/35 and STM32H730 devices is composed of eight flters (see reference manual STM32H723/733, STM32H725/735 advanced and STM32H730 Arm®-based 32-bit MCUs (RM0468))

Figure 25. Stereo microphone interconnection shows an example of a stereo microphone interconnection.

![](images/9434e633f0d5370e4000e33f95a762c26e20dfc640185d699e4dfe95184a3184.jpg)  
Figure 25. Stereo microphone interconnection

This example can be transposed to other kinds of external sensors.

# 9.4.5

# Embedded trace macrocell (ETM)

# Interface connectivity

Tableeectructine rogram eecutnheatacsgheat watpo tra (DWT) component or he instruction trace acrocell (TM) whereas instructions ae trace usig the aceace M. he Minteac s r wit he ur at us e D[0:3]  e clock signal CLK.

# Interface signals layout guidelines

Reference the plane using GND or PWR (if PWR, add 10 nf stitching capacitor between PWR and GND Trace impedance: 50 Ω ± 10%   
All the data trace should be as short as possible (≤25 mm),   
Trace the lines which should run on the same layer with a solid ground plane underneath it without vias. Trace the clock which should have only point-to-point connection. Any stubs should be avoided.   
It isrongly cene also rother at) nes  be poit--pointonly. y stubs e eede e should be as short as possible. If long stubs are required, there should be a possibility to optinally disconnect them (e.g. by jumpers).

# 10 Use case examples

STM32CubeMX must be used to determine the most appropriate package for a given use case.

Table .Use case examples gives some typical use case examples. It defines the package which supports a e larger packages.

Table 11. Use case examples   

<table><tr><td rowspan=1 colspan=1>Package</td><td rowspan=1 colspan=3>Use Case</td><td rowspan=1 colspan=1>Peripheral</td><td rowspan=1 colspan=1>Comment</td></tr><tr><td rowspan=8 colspan=1>LQFP100 (no SMPS)</td><td rowspan=8 colspan=3>Display and μSD</td><td rowspan=1 colspan=1>LCD</td><td rowspan=1 colspan=1>RGB TFT Display 8/8/8</td></tr><tr><td rowspan=1 colspan=1>12C</td><td rowspan=1 colspan=1>Communication interface</td></tr><tr><td rowspan=1 colspan=1>SDMMC2</td><td rowspan=1 colspan=1>μSD</td></tr><tr><td rowspan=1 colspan=1>GPIO</td><td rowspan=1 colspan=1>SD card detection</td></tr><tr><td rowspan=1 colspan=1>USB-FS</td><td rowspan=1 colspan=1></td></tr><tr><td rowspan=1 colspan=1>USART3</td><td rowspan=1 colspan=1>Communication interface</td></tr><tr><td rowspan=1 colspan=1>SPI3</td><td rowspan=1 colspan=1>Communication interface</td></tr><tr><td rowspan=1 colspan=1>GPIO</td><td rowspan=1 colspan=1>remaining GPIO available</td></tr><tr><td rowspan=8 colspan=1>LQFP100 (no SMPS) Display and OCTOSPI</td><td rowspan=8 colspan=3>LQFP100 (no SMPS) Display and OCTOSPI</td><td rowspan=1 colspan=1>LCD</td><td rowspan=1 colspan=1>RGB TFT display 8/8/8</td></tr><tr><td rowspan=1 colspan=1>I2C1</td><td rowspan=1 colspan=1>Touch screen or communication interface</td></tr><tr><td rowspan=1 colspan=1>OCTOSPIM_P1</td><td rowspan=1 colspan=1>External memory</td></tr><tr><td rowspan=2 colspan=2></td><td rowspan=2 colspan=1></td><td></td><td></td></tr><tr><td rowspan=1 colspan=1>USART2</td><td rowspan=1 colspan=1>Communication interface</td></tr><tr><td rowspan=1 colspan=1>SPI1</td><td rowspan=1 colspan=1>Communication interface</td></tr><tr><td rowspan=1 colspan=1>USB-FS</td><td rowspan=1 colspan=1></td></tr><tr><td rowspan=1 colspan=1>GPIO</td><td rowspan=1 colspan=1>Remaining GPIO available</td></tr><tr><td rowspan=7 colspan=1>LQFP100 (no SMPS)</td><td rowspan=7 colspan=3>Audio beam forming and VADDisplayExternal memory or wifi module</td><td rowspan=1 colspan=1>FMC</td><td rowspan=1 colspan=1>Memory interface used to drive a display (up to 16 bit parallel</td></tr><tr><td rowspan=1 colspan=1>I2C4</td><td rowspan=1 colspan=1>Touch screen or communication interface</td></tr><tr><td rowspan=1 colspan=1>DFSDM2</td><td rowspan=1 colspan=1>Digital microphone interface for voice activity detection (VAD),shared with DFSDM1 (see section ...)</td></tr><tr><td rowspan=1 colspan=1>DFSDM1</td><td rowspan=1 colspan=1>Digital microphone interface (up to 8)Beam forming</td></tr><tr><td rowspan=1 colspan=1>SDMMC</td><td rowspan=1 colspan=1>To interface WIFI module or memory</td></tr><tr><td rowspan=1 colspan=1>SPI1</td><td rowspan=1 colspan=1>Communication interface</td></tr><tr><td rowspan=1 colspan=1>USB-FS</td><td rowspan=1 colspan=1></td></tr><tr><td rowspan=6 colspan=1>LQFP100</td><td rowspan=6 colspan=3>Camera, Display and μSD</td><td rowspan=1 colspan=1>FMC</td><td rowspan=1 colspan=1>Memory interface used to drive a display (up to 14 bit parallel)</td></tr><tr><td rowspan=1 colspan=1>I2C2</td><td rowspan=1 colspan=1>Touch screen or communication interface</td></tr><tr><td rowspan=1 colspan=1>DCMI</td><td rowspan=1 colspan=1>14 bit parallel camera interface</td></tr><tr><td rowspan=1 colspan=1>USB-FS</td><td rowspan=1 colspan=1></td></tr><tr><td rowspan=1 colspan=1>SDMMC2</td><td rowspan=1 colspan=1>μSD (four bit mode)</td></tr><tr><td rowspan=1 colspan=1>GPIO</td><td rowspan=1 colspan=1>μSD detection</td></tr></table>

# 11 Conclusion

This application note must be used as reference when starting a new design with an STM32H723/33, STM32H725/35 and STM32H730 microcontroller.

# Revision history

Table 12. Document revision history   

<table><tr><td>Date</td><td>Version</td><td>Changes</td></tr><tr><td>13-Nov-2019</td><td>1</td><td>Initial release.</td></tr><tr><td>20-May-2020</td><td>2</td><td>Changed document classification to public. Added STM32H730 Value Line. Updated external components for VLXSMPS and VDDLDO in Table 2. Power supply connection and updated values of external capacitors connected to VLXSMPS in Figure 3. Power supply component layout. Only one additional external inductor required to improve the overall system power consumption with SMPS in Section 2.1.7 SMPS step-down converter. Updated Section 2.2.1 Power-on reset (POR)/power-down reset (PDR).</td></tr></table>

# Contents

# General information 2

# Power supplies 3

# 2.1 Introduction 3

2.1.1 External power supplies and components.   
2.1.2 Digital circuit core supply (Vcore) 10   
2.1.3 Independent analog supply and reference voltage 10   
2.1.4 Independent USB transceiver power supply 10   
2.1.5 Battery backup domain. 12   
2.1.6 LDO voltage regulator . 12   
2.1.7 SMPS step-down converter. 14

1.2 Reset and power supply supervisor 15

2.2.1 Power-on reset (POR)/power-down reset (PDR). 15   
2.2.2 BrownOut reset (BOR) 16   
2.2.3 Programmable voltage detector (PVD) 16   
2.2.4 Analog voltage detector (AVD) 17   
2.2.5 System reset. 17   
2.2.6 Bypass mode 17

# Clocks. .18

# 3.1 Introduction 18

3.1.1 HSE and LSE bypass (external user clock). 22   
3.1.2 External crystal/ceramic resonator (HSE crystal) 22   
3.2 LSE oscillator clock. 23   
3.3 Clock security system (CSS). 23   
3.4 Clock recovery system (CRS) 23

# Alternate function mapping to pins 24

4.1 Analog inputs for ADC1, ADC2 and ADC3 24

4.1.1 Packages having Pxy_C and Pxy pads available 24   
4.1.2 Packages having Pxy_C but not the peer Pxy. 25   
4.1.3 Package having Pxy available but nor the peer Pxy_C. 25

# 5 Boot configuration. .26

5.1 Boot mode selection.. 26   
5.2 Boot pin connection 27   
5.3 System bootloader mode. 27

# Debug management .28

6.1 Introduction .28

# 6.2 SWJ debug port (serial wire and JTAG). 28

6.2.1 TPIU trace port . 28   
6.2.2 External debug trigger. 28

# 6.3 Pinout and debug port pins 29

6.3.1 SWJ debug port pins. 29   
6.3.2 Flexible SWJ-DP pin assignment 29   
6.3.3 Internal pull-up and pull-down on JTAG pins . 30   
6.3.4 SWJ debug port connection with standard JTAG connector 30

# Recommendations. .31

7.1 Printed circuit board 31   
7.2 Component position .31   
7.3 Ground and power supply (VSS,VDD). .31   
7.4 Decoupling. .31   
7.5 Other signals .32   
7.6 Unused I/Os and features 32

# Reference design .33

# 8.1 Description. 33

# Recommended PCB routing guidelines for STM32H723/733, STM32H725/735 and STM32H730 microcontrollers 34

9.1 PCB stack-up. 34   
9.2 Crystal oscillator 35   
9.3 Power supply decoupling .35

# 9.4 High speed signal layout 36

9.4.1 SDMMC bus interface. 36   
9.4.2 Flexible memory controller (FMC) interface. 37   
9.4.3 Octo-SPI interface. 38

9.4.4 DFSDM interface 40

9.4.5 Embedded trace macrocell (ETM). 41

10 Use case examples 42

11 Conclusion. .43

Revision history 44

Contents .45

List of tables 48

List of figures. .49

# List of tables

Table 1. PWR input/output signals connected to package pins/balls 5   
Table 2. Power supply connection 7   
Table 3. Clock connections 19   
Table 4. Clock source generation . 21   
Table 5. Boot modes. 26   
Table 6. STM32H723/733, STM32H725/735 and STM32H730 microcontroller bootloader communication peripherals 27   
Table 7. TPIU trace pins 28   
Table 8. External debug trigger pins 29   
Table 9. SWJ debug port pins 29   
Table 10. Flexible SWJ-DP assignment 29   
Table 11. Use case examples 42   
Table 12. Document revision history . 44

# List of figures

Figure 1. Power supplies. 4   
Figure 2. System supply configuration. 6   
Figure 3. Power supply component layout 9   
Figure 4. VDD33USB connected to VDD power supply 11   
Figure 5. VDD33USB connected to external power supply. 11   
Figure 6. VDD50USB power supply 12   
Figure 7. Power on reset/power down reset waveform. 15   
Figure 8. Power supply supervisor interconnection with internal reset OFF. 16   
Figure 9. Reset circuit . 17   
Figure 10. Clock generation and clock tree 19   
Figure 11. HSE/LSE clock source. 21   
Figure 12. Analog inputs for ADC1 and ADC2 24   
Figure 13. Boot mode selection implementation example 27   
Figure 14. Host to board connection 28   
Figure 15. JTAG connector implementation 30   
Figure 16. Typical layout for VDD/Vss pair . 31   
Figure 17. Four layer PCB stack-up example . 34   
Figure 18. Six layer PCB stack-up example . 34   
Figure 19. Decoupling capacitor placement depending on package type . 35   
Figure 20. Example of decoupling capacitor placed underneath 36   
Figure 21. microSD card interconnection example 37   
Figure 22. SD card interconnection example 37   
Figure 23. Octo-SPI interconnection example 39   
Figure 24. Octo-SPI multiplexed interconnection example 40   
Figure 25. Stereo microphone interconnection 41

# IMPORTANT NOTICE - PLEASE READ CAREFULLY

ol uant   .

Purchasers' products.

No license, express or implied, to any intellectual property right is granted by ST herein.

names are the property of their respective owners.

I