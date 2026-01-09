# Introduction to USB Type-C® Power Delivery for STM32 MCUs and MPUs

# Introduction

Se C TP 8 -2a basic concepts of the two new USB Type-C® and USB Power Delivery standards are also introduced.

US facilitate the use of universal chargers.

with the optional USB Power Delivery feature.

# 1 General information

# Note:

This document applies to STM32 MCUs and MPUs, based on Arm® Cortex®-M processor. Arm is a registered trademark of Arm Limited (or its subsidiaries) in the US and/or elsewhere

# arm

# 1.1

# Acronyms and abbreviations

<table><tr><td rowspan=2 colspan=2>Acronym       Meaning</td></tr><tr><td rowspan=1 colspan=1>Acronym</td></tr><tr><td rowspan=1 colspan=1>AMS</td><td rowspan=1 colspan=1>Atomic message sequence</td></tr><tr><td rowspan=1 colspan=1>APDO</td><td rowspan=1 colspan=1>Augmented power delivery object</td></tr><tr><td rowspan=1 colspan=1>BMC</td><td rowspan=1 colspan=1>Bi-phase mark coding</td></tr><tr><td rowspan=1 colspan=1>BSP</td><td rowspan=1 colspan=1>Board support package</td></tr><tr><td rowspan=1 colspan=1>CAD</td><td rowspan=1 colspan=1>Cable detection module</td></tr><tr><td rowspan=1 colspan=1>DFP</td><td rowspan=1 colspan=1>Downstream facing port</td></tr><tr><td rowspan=1 colspan=1>DPM</td><td rowspan=1 colspan=1>Device policy manager</td></tr><tr><td rowspan=1 colspan=1>DRP</td><td rowspan=1 colspan=1>Dual-role power</td></tr><tr><td rowspan=1 colspan=1>DRS</td><td rowspan=1 colspan=1>Data role swap</td></tr><tr><td rowspan=1 colspan=1>GP</td><td rowspan=1 colspan=1>General purpose</td></tr><tr><td rowspan=1 colspan=1>GUI</td><td rowspan=1 colspan=1>Graphical user interface</td></tr><tr><td rowspan=1 colspan=1>HAL</td><td rowspan=1 colspan=1>Hardware abstraction layer</td></tr><tr><td rowspan=1 colspan=1>HW</td><td rowspan=1 colspan=1>Hardware</td></tr><tr><td rowspan=1 colspan=1>LL</td><td rowspan=1 colspan=1>Low layer</td></tr><tr><td rowspan=1 colspan=1>MSC</td><td rowspan=1 colspan=1>Message sequence chart</td></tr><tr><td rowspan=1 colspan=1>OVP</td><td rowspan=1 colspan=1>Over-voltage protection</td></tr><tr><td rowspan=1 colspan=1>PDO</td><td rowspan=1 colspan=1>Power delivery object</td></tr><tr><td rowspan=1 colspan=1>PE</td><td rowspan=1 colspan=1>Policy engine</td></tr><tr><td rowspan=1 colspan=1>PRL</td><td rowspan=1 colspan=1>Physical protocol layer</td></tr><tr><td rowspan=1 colspan=1>PRS</td><td rowspan=1 colspan=1>Power role swap</td></tr><tr><td rowspan=1 colspan=1>SNK</td><td rowspan=1 colspan=1>Power sink</td></tr><tr><td rowspan=1 colspan=1>SRC</td><td rowspan=1 colspan=1>Power source</td></tr><tr><td rowspan=1 colspan=1>UCPD</td><td rowspan=1 colspan=1>USB Type-C Power Delivery</td></tr><tr><td rowspan=1 colspan=1>UCSI</td><td rowspan=1 colspan=1>USB Type-C® Connector System Software Interface</td></tr><tr><td rowspan=1 colspan=1>UFP</td><td rowspan=1 colspan=1>Upstream facing port</td></tr><tr><td rowspan=1 colspan=1>VDM</td><td rowspan=1 colspan=1>Vendor defined messages</td></tr><tr><td rowspan=1 colspan=1>FWUP</td><td rowspan=1 colspan=1>Firmware update</td></tr><tr><td rowspan=1 colspan=1>PPS</td><td rowspan=1 colspan=1>Programmable power supply</td></tr><tr><td rowspan=1 colspan=1>TCPM</td><td rowspan=1 colspan=1>Type-C port manager</td></tr><tr><td rowspan=1 colspan=1>TCPC</td><td rowspan=1 colspan=1>Type-C port controller</td></tr><tr><td rowspan=1 colspan=1>TVS</td><td rowspan=1 colspan=1>Transient voltage suppression</td></tr></table>

# 1.2 Reference documents

Table 1. STMicroelectronics ecosystem documents   

<table><tr><td rowspan=1 colspan=1>Reference</td><td rowspan=1 colspan=1>Document title</td></tr><tr><td rowspan=1 colspan=1>STMicroelectronics ecosystem documents</td><td rowspan=1 colspan=1>STMicroelectronics ecosystem documents</td></tr><tr><td rowspan=1 colspan=1>[1]</td><td rowspan=1 colspan=1>Managing USB Power Delivery systems with STM32 microcontrollers, UM2552</td></tr><tr><td rowspan=1 colspan=1>[2]</td><td rowspan=1 colspan=1>STM32CubeMonitor-UCPD software tool for USB Type-C® Power Delivery port management, UM2468</td></tr><tr><td rowspan=1 colspan=1>[3]</td><td rowspan=1 colspan=1>TCPP01-M12 USB Type-C® port protection, DS12900</td></tr><tr><td rowspan=1 colspan=1>[4]</td><td rowspan=1 colspan=1>TCPP02-M18 USB Type-C® port protection, DS13787</td></tr><tr><td rowspan=1 colspan=1>[5]</td><td rowspan=1 colspan=1>TCPP03-M20 USB Type-C® port protection, DS13618</td></tr><tr><td rowspan=1 colspan=1>[6]</td><td rowspan=1 colspan=1>USB Type-C® protection and filtering, AN4871</td></tr><tr><td rowspan=1 colspan=1>[7]</td><td rowspan=1 colspan=1>STM32CubeMonitor-UCPD software tool for USB Type-C® Power Delivery port management, DB3747</td></tr><tr><td rowspan=1 colspan=1>[8]</td><td rowspan=1 colspan=1>USB Type-C® and Power Delivery DisplayPort Alternate Mode, TA0356</td></tr><tr><td rowspan=1 colspan=1>[9]</td><td rowspan=1 colspan=1>Overview of USB Type-C® and Power Delivery technologies, TA0357</td></tr><tr><td rowspan=1 colspan=1>[10]</td><td rowspan=1 colspan=1>STM32MP151/153/157 MPU lines and STPMIC1B integration on a battery powered application, AN5260</td></tr><tr><td rowspan=1 colspan=1>[11]</td><td rowspan=1 colspan=1>USB hardware and PCB guidelines using STM32 MCUs, AN4879</td></tr><tr><td rowspan=1 colspan=1>[12]</td><td rowspan=1 colspan=1>Getting started with the X-NUCLEO-DRP1M1 USB Type-C® Power Delivery dual role port expansionboard based on TCPP03-M20 for STM32 Nucleo, UM2891</td></tr><tr><td rowspan=1 colspan=1>[13]</td><td rowspan=1 colspan=1>Getting started with the X-NUCLEO-SRC1M1 USB Type-C® Power Delivery source expansion boardbased on TCPP02-M18 for STM32 Nucleo, UM2973</td></tr><tr><td rowspan=1 colspan=1>[14]</td><td rowspan=1 colspan=1>STM32 USB Power Delivery landing page htps://www.st.com/content/st_com/en/ecosystems/stm32-usb-c.html</td></tr><tr><td rowspan=1 colspan=1>[15]</td><td rowspan=1 colspan=1>STM32 USB Power Delivery wiki page https:/wiki.st.com/stm32mcu/wiki/Introduction_to_USB_Power_Delivery_with_STM32</td></tr><tr><td rowspan=1 colspan=2>USB specification documents</td></tr><tr><td rowspan=1 colspan=1>[16]</td><td rowspan=1 colspan=1>USB2.0 Universal Serial Bus Revision 2.0 Specification</td></tr><tr><td rowspan=1 colspan=1>[17]</td><td rowspan=1 colspan=1>USB3.1 Universal Serial Bus Revision 3.2 Specification</td></tr><tr><td rowspan=1 colspan=1>[18]</td><td rowspan=1 colspan=1>USB BC Battery Charging Specification Revision 1.2</td></tr><tr><td rowspan=1 colspan=1>[19]</td><td rowspan=1 colspan=1>USB BB USB Device Class Definition for Billboard Devices</td></tr><tr><td rowspan=1 colspan=1>[20]</td><td rowspan=1 colspan=1>Universal Serial Bus Power Delivery Specification, Revision 2.0, Version 1.3, January 12, 2017</td></tr><tr><td rowspan=1 colspan=1>[21]</td><td rowspan=1 colspan=1>Universal Serial Bus Power Delivery Specification, Revision 3.1, Version 1.7, January 2023</td></tr><tr><td rowspan=1 colspan=1>[22]</td><td rowspan=1 colspan=1>Universal Serial Bus Type-C Cable and Connector Specification 2.0, August 2019</td></tr><tr><td rowspan=1 colspan=1>[23]</td><td rowspan=1 colspan=1>USB Billboard Device Class Specification, Revision 1.0, August 1, 2014, htp:/www.usb.org/developers/docs</td></tr><tr><td rowspan=1 colspan=1>[24]</td><td rowspan=1 colspan=1>USB Type-C® Connector System Software Interface Specification, requirements specification (UCSI),January 2020, revision 1.2</td></tr></table>

# 2 USB Type-C in a nutshell

The USB Implementers Forum (USB-IF) introduces two complementary specifications:

The USB Type-C® cable and connector specification release 1.3 details a reversible, slim connector system based on high-speed USB2.0 signals and two super-speed lanes at up to 10 Gbits, which can also be used to support alternate modes. The USB Power Delivery (PD) specification revisions 2.0 and 3.0 detail how a link can be transformed from a 4.5 W power source (900 mA at 5 V on VBUS), to a 100 W power or consumer source (up to 5 A at 20 V).

Te new pin USB Type® plu isdesined  be on-polarizedand fuly everible, atte whi way inserted.

It supports all the advanced features proposed by Power Delivery:

negotiating power roles   
negotiating power sourcing and consumption levels   
performing active cable identification   
exchanging vendor-specific sideband messaging   
perorming alternate mode negotiation, allowing third-party communication protocols to berouted onto the   
reconfigurable pins of the USB Type-C® cable

![](images/64c492fd90ae1efd8edb34ade08b037b7eb1e231b99ae7ee567d570d73f484e1.jpg)  
Figure 1. USB connectors   
Multiple connectors to support all kind of USB data

The following points should also be noted:

USB Type-C® cables use the same plug on both ends.   
USB Ty   SB.   
capability.   
The new connector is quite small (it is 8.4 mm wide and 2.6 mm high).

As shown in Figure 1. USB connectors, the new USB Type-® plug covers al features provided by previous plugs, which ensure flexibility and simplifies the application.

A UB Type-® port can act as host only device only, orhave dual functin. Both data and power roles can independently and dynamically be swapped using USB Power Delivery commands.

# USB Type-C® vocabulary

The terminology commonly used for USB Type-C® system is:

Sor:A port power role. ort exposing Rp (pullp resistor e Figure.Pull up/down C detection) CC pins (command control pins, see Section 4 CC pins), and providing power over VBUS (5 V to 20 V and up to 5 A), most commonly a Host or Hub downstream-facing port (such as legacy Type-A port).

S A port power role.ort exposing Rd (Pull down resistor. ee Figure . ull up/down C detection)n CC pins and consuming power from VBUS (5 V to 20 V and up to 5 A), most commonly a device (such as a legacy Type-B port)

Dual-role power (DRP) port: A port that can play source or sink power roles, reversible dynamically.

Downstream-facing port (DFP): A port data role. A USB port at higher level of USB tree, such as a USB host or a hub expansion.

Upstream-acig port (UFP): A port data role.AUSB port at lower level  USB tree, such as a USB evice or a hub master port.

# 2.2

# Minimum mandatory feature set

It isnot mandatory plment n sppor  he dvanc atures that defi withTn Power Delivery specifications.

The mandatory functions to support are:

cable attach and detach detection plug orientation/cable twist detection USB2.0 connection

# 3 Connector pin mapping

The 24-pin USB Type-C® connector includes:

symmetric connections:

USB2.0 differential pairs (D+/D-) power pins: VBUS/GND

asymmetric connections

two sets of TX/RX signal paths which support USB3.1 data speed   
configuration channels (CC lines) which handle discovery, configuration and management of   
USB Type-C® Power Delivery features   
two side-band use signals (SBU lines) for analog audio modes or alternate mode

Figure 2. Receptacle pinout   

<table><tr><td>A12</td><td>A11</td><td>A10</td><td>A9</td><td>A8</td><td>A7</td><td>A6</td><td>A5</td><td>A4</td><td>A3</td><td>A2</td><td>A1</td></tr><tr><td>GND</td><td>RX2+</td><td>RX2-</td><td>VBUS</td><td>SBU1</td><td>D-</td><td>D+</td><td>CC1</td><td>VBUS</td><td>TX1-</td><td>TX1+</td><td>GND</td></tr><tr><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td></tr><tr><td>GND</td><td>TX2+</td><td>TX2-</td><td>VBUS</td><td>CC2</td><td>D+</td><td>D-</td><td>SBU2</td><td>VBUS</td><td>RX1-</td><td>RX1+</td><td>GND</td></tr><tr><td>B1</td><td>B2</td><td>B3</td><td>B4</td><td>B5</td><td>B6</td><td>B7</td><td>B8</td><td>B9</td><td>B10</td><td>B11</td><td>B12</td></tr></table>

Table 2. USB Type-C receptacle pin descriptions   

<table><tr><td colspan="1" rowspan="1">Pin</td><td colspan="1" rowspan="1">Name</td><td colspan="1" rowspan="1">Description</td><td colspan="1" rowspan="1">Comment</td></tr><tr><td colspan="1" rowspan="1">A1</td><td colspan="1" rowspan="1">GND</td><td colspan="1" rowspan="1">Ground return</td><td colspan="1" rowspan="1">up to 5 A split into 4 pins</td></tr><tr><td colspan="1" rowspan="1">A2</td><td colspan="1" rowspan="1">TX1+</td><td colspan="1" rowspan="2">USB3.0 datalines or alternate</td><td colspan="1" rowspan="2">10 Gbit/s TX differential pair in USB3.1</td></tr><tr><td colspan="1" rowspan="1">A3</td><td colspan="1" rowspan="1">TX1-</td></tr><tr><td colspan="1" rowspan="1">A4</td><td colspan="1" rowspan="1">VBUS</td><td colspan="1" rowspan="1">Bus power</td><td colspan="1" rowspan="1">100 W max power split into 4 pins</td></tr><tr><td colspan="1" rowspan="1">A5</td><td colspan="1" rowspan="1">CC1 or VCONN</td><td colspan="1" rowspan="1">Configuration channel or power foractive or electronically marked cable</td><td colspan="1" rowspan="1">In VCONN configuration, min power is1 W</td></tr><tr><td colspan="1" rowspan="1">A6</td><td colspan="1" rowspan="1">D+</td><td colspan="1" rowspan="2">USB2.0 data lines</td><td colspan="1" rowspan="2"></td></tr><tr><td colspan="1" rowspan="1">A7</td><td colspan="1" rowspan="1">D-</td></tr><tr><td colspan="1" rowspan="1">A8</td><td colspan="1" rowspan="1">SBU1</td><td colspan="1" rowspan="1">Side band use</td><td colspan="1" rowspan="1">Alternate mode only</td></tr><tr><td colspan="1" rowspan="1">A9</td><td colspan="1" rowspan="1">VBUS</td><td colspan="1" rowspan="1">Bus power</td><td colspan="1" rowspan="1">100 W max power split into 4 pins</td></tr><tr><td colspan="1" rowspan="1">A10</td><td colspan="1" rowspan="1">RX2-</td><td colspan="1" rowspan="2">USB3.0 datalines or alternate</td><td colspan="1" rowspan="2">10 Gbit/s RX differential pair USB3.1</td></tr><tr><td colspan="1" rowspan="1">A11</td><td colspan="1" rowspan="1">RX2+</td></tr><tr><td colspan="1" rowspan="1">A12</td><td colspan="1" rowspan="1">GND</td><td colspan="1" rowspan="1">Ground return</td><td colspan="1" rowspan="1">up to 5 A split into 4 pins</td></tr><tr><td colspan="1" rowspan="1">B1</td><td colspan="1" rowspan="1">GND</td><td colspan="1" rowspan="1">Ground return</td><td colspan="1" rowspan="1">up to 5 A split into 4 pins</td></tr><tr><td colspan="1" rowspan="1">B2</td><td colspan="1" rowspan="1">TX2+</td><td colspan="1" rowspan="2">USB3.0 datalines or alternate</td><td colspan="1" rowspan="2">10 Gbit/s TX differential pair in USB3.1</td></tr><tr><td colspan="1" rowspan="1">B3</td><td colspan="1" rowspan="1">TX2-</td></tr><tr><td colspan="1" rowspan="1">B4</td><td colspan="1" rowspan="1">VBUS</td><td colspan="1" rowspan="1">Bus power</td><td colspan="1" rowspan="1">100 W max power split into 4 pins</td></tr><tr><td colspan="1" rowspan="1">B5</td><td colspan="1" rowspan="1">CC2 or VCONN</td><td colspan="1" rowspan="1">Configuration channel or power foractive or electronically marked cable</td><td colspan="1" rowspan="1">In VCONN configuration, min power is1W</td></tr><tr><td colspan="1" rowspan="1">B6</td><td colspan="1" rowspan="1">D+</td><td colspan="1" rowspan="2">USB2.0 datalines</td><td colspan="1" rowspan="1"></td></tr><tr><td colspan="1" rowspan="1">B7</td><td colspan="1" rowspan="1">D-</td><td colspan="1" rowspan="1"></td></tr><tr><td colspan="1" rowspan="1">B8</td><td colspan="1" rowspan="1">SBU2</td><td colspan="1" rowspan="1">Side band use</td><td colspan="1" rowspan="1">Alternate mode only</td></tr><tr><td colspan="1" rowspan="1">B9</td><td colspan="1" rowspan="1">VBUS</td><td colspan="1" rowspan="1">Bus power</td><td colspan="1" rowspan="1">100 W ma power split into 4 pins</td></tr><tr><td colspan="1" rowspan="1">B10</td><td colspan="1" rowspan="1">RX1-</td><td colspan="1" rowspan="2">USB3.0 datalines or alternate</td><td colspan="1" rowspan="2">10 Gbit/s RX differential pair in USB3.1</td></tr><tr><td colspan="1" rowspan="1">B11</td><td colspan="1" rowspan="1">RX1+</td></tr><tr><td colspan="1" rowspan="1">B12</td><td colspan="1" rowspan="1">GND</td><td colspan="1" rowspan="1">Ground return</td><td colspan="1" rowspan="1">Up to 5 A split into 4 pins</td></tr></table>

# 3.1 VBUS power options

VBUS provides a path to deliver power between a host and a device, and between a charger and a host or device.

Power options available from the perspective of a device with a USB Type-® connecor are listed below.

Table 3. Power supply options   

<table><tr><td rowspan=1 colspan=1>Mode of operation</td><td rowspan=1 colspan=1>Nominal voltage</td><td rowspan=1 colspan=1>Maximum current</td><td rowspan=1 colspan=1>Note</td></tr><tr><td rowspan=1 colspan=1>USB2.0</td><td rowspan=1 colspan=1>5V</td><td rowspan=1 colspan=1>500 mA</td><td rowspan=2 colspan=1>Default current based on specification</td></tr><tr><td rowspan=1 colspan=1>USB3.1</td><td rowspan=1 colspan=1>5V</td><td rowspan=1 colspan=1>900 mA</td></tr><tr><td rowspan=1 colspan=1>USB BC1.2</td><td rowspan=1 colspan=1>5V</td><td rowspan=1 colspan=1>1.5 A</td><td rowspan=1 colspan=1>Legacy charging</td></tr><tr><td rowspan=1 colspan=1>Current @1.5 A</td><td rowspan=1 colspan=1>5V</td><td rowspan=1 colspan=1>1.5 A</td><td rowspan=2 colspan=1>Support high-power devices</td></tr><tr><td rowspan=1 colspan=1>Current @3 A</td><td rowspan=1 colspan=1>5V</td><td rowspan=1 colspan=1>3A</td></tr><tr><td rowspan=1 colspan=1>USB PD</td><td rowspan=1 colspan=1>5 V to 20 V</td><td rowspan=1 colspan=1>5A</td><td rowspan=1 colspan=1>Directional control and power level management</td></tr></table>

Note:

USB Type-C® to Type-C™ cable assembly needs VBUS to be protected against 20 V DC at the rated cable current (3 A or 5 A).

# 4 CC pins

T w C i C nCT- uny C e n  ab at each end of the cable (they are connected in common through the cable). On both CC1 and CC2, a source u eo ul shers  ikmuseospull  isorlec ables provide a rsistor Ra,  ground onV.

From a source point of view, the state of attached devices can be determined by referring to Table 4.

Table 4. Attached device states - source perspective   

<table><tr><td rowspan=1 colspan=1>CC1</td><td rowspan=1 colspan=1>CC2</td><td rowspan=1 colspan=1>State</td></tr><tr><td rowspan=1 colspan=1>Open</td><td rowspan=1 colspan=1>Open</td><td rowspan=1 colspan=1>Nothing attached</td></tr><tr><td rowspan=1 colspan=1>Rd</td><td rowspan=1 colspan=1>Open</td><td rowspan=2 colspan=1>Sink attached</td></tr><tr><td rowspan=1 colspan=1>Open</td><td rowspan=1 colspan=1>Rd</td></tr><tr><td rowspan=1 colspan=1>Open</td><td rowspan=1 colspan=1>Ra</td><td rowspan=2 colspan=1>Powered cable without sink attached</td></tr><tr><td rowspan=1 colspan=1>Ra</td><td rowspan=1 colspan=1>Open</td></tr><tr><td rowspan=1 colspan=1>Rd</td><td rowspan=1 colspan=1>Ra</td><td rowspan=2 colspan=1>Powered cable with sink, VCONN-powered accessory (VPA), or VCONN-powered USB device (VPD) attached.</td></tr><tr><td rowspan=1 colspan=1>Ra</td><td rowspan=1 colspan=1>Rd</td></tr><tr><td rowspan=1 colspan=1>Rd</td><td rowspan=1 colspan=1>Rd</td><td rowspan=1 colspan=1>Debug accessory mode attached</td></tr><tr><td rowspan=1 colspan=1>Ra</td><td rowspan=1 colspan=1>Ra</td><td rowspan=1 colspan=1>Audio adapter accessory mode attached</td></tr></table>

# 4.1

# Plug orientation/cable twist detection

U the orientation. The detection is done through the CC lines using the Rp/Rd resistors. Initially a DFP presents Rp terminations on its CC pins and a UFP presents Rd terminations on its CC pins. To detect the connection, the DFP monitors both CC pins (see figure 4-30 in [22].

DFP monitors for connection

![](images/df79abb8c201eb69996f782cfd52f061df1a8ac8879d2bf17544e2e5407e1c6c.jpg)  
Figure 3. Pull up/down CC detection

UFP monitors for orientation

# 4.2

# Power capability detection and usage

Type-C offers increased current capabilities of 1.5 A and 3 A in addition to the default USB standard.   
Tppabe pr e  p va.   
High current (5 A) capability is negotiated using the USB Power Delivery protocol.   
Table 5 shows the possible values, as per [22].

Table 5. DFP CC termination (Rp) requirements   

<table><tr><td rowspan=1 colspan=1>VBUs power</td><td rowspan=1 colspan=1>Current source to1.7 V - 5.5 V</td><td rowspan=1 colspan=1>Rp pull up to4.75 V - 5.5 V</td><td rowspan=1 colspan=1>Rp pull up to3.3 V +/-5%</td></tr><tr><td rowspan=1 colspan=1>Default USB power</td><td rowspan=1 colspan=1>80 mA ± 20%</td><td rowspan=1 colspan=1>56 kΩ ± 20% (1)</td><td rowspan=1 colspan=1>36 kΩ ± 20%</td></tr><tr><td rowspan=1 colspan=1>1.5 A @5 V</td><td rowspan=1 colspan=1>180 mA ± 8%</td><td rowspan=1 colspan=1>22 kΩ ± 5%</td><td rowspan=1 colspan=1>12 kΩ ± 5%</td></tr><tr><td rowspan=1 colspan=1>3.0 A @5 V</td><td rowspan=1 colspan=1>330 mA ± 8%</td><td rowspan=1 colspan=1>10 kΩ ± 5%</td><td rowspan=1 colspan=1>4.7 kΩ ± 5%</td></tr></table>

1. ForR hepn he USB Type-plug n USBType- USB .1Sanar- Cablbly USB-CtoUSB.0Standard-A CableAssembly, aUSBType-CtoUSB.0Micro-BReceptaceAdapterssembly r  USB on VBus and GND in the cable assembly.

The UFP must expose Rd-pul down resistors on both CC1 and CC2 to bias the detection system and to be identified as the power sink, as per [22].

Table 6. UFP CC termination (Rd) requirements   

<table><tr><td rowspan=1 colspan=1>Rd implementation</td><td rowspan=1 colspan=1>Nominal value</td><td rowspan=1 colspan=1>Can detect powercapability?</td><td rowspan=1 colspan=1>max voltage on CC pin</td></tr><tr><td rowspan=1 colspan=1>± 20% voltage clamp</td><td rowspan=1 colspan=1>1.1 V</td><td rowspan=1 colspan=1>No</td><td rowspan=1 colspan=1>1.32 V</td></tr><tr><td rowspan=1 colspan=1>± 20% resistor to GND</td><td rowspan=1 colspan=1>5.1 kΩ</td><td rowspan=1 colspan=1>No</td><td rowspan=1 colspan=1>2.18 V</td></tr><tr><td rowspan=1 colspan=1>± 10% resistor to GND</td><td rowspan=1 colspan=1>5.1 kΩ</td><td rowspan=1 colspan=1>Yes</td><td rowspan=1 colspan=1>2.04 V</td></tr></table>

FP lC

Table 7. Voltage on sink CC pins (multiple source current advertisements)   

<table><tr><td rowspan=1 colspan=1>Detection</td><td rowspan=1 colspan=1>Min voltage (V)</td><td rowspan=1 colspan=1>Max voltage (V)</td><td rowspan=1 colspan=1>Threshold (V)</td></tr><tr><td rowspan=1 colspan=1>vRa</td><td rowspan=1 colspan=1>-0.25</td><td rowspan=1 colspan=1>0.15</td><td rowspan=1 colspan=1>0.2</td></tr><tr><td rowspan=1 colspan=1>vRd-Connect</td><td rowspan=1 colspan=1>0.25</td><td rowspan=1 colspan=1>2.04</td><td rowspan=1 colspan=1>-</td></tr><tr><td rowspan=1 colspan=1>vRd-USB</td><td rowspan=1 colspan=1>0.25</td><td rowspan=1 colspan=1>0.61</td><td rowspan=1 colspan=1>0.66</td></tr><tr><td rowspan=1 colspan=1>vRd-1.5</td><td rowspan=1 colspan=1>0.70</td><td rowspan=1 colspan=1>1.16</td><td rowspan=1 colspan=1>1.23</td></tr><tr><td rowspan=1 colspan=1>vRd-3.0</td><td rowspan=1 colspan=1>1.31</td><td rowspan=1 colspan=1>2.04</td><td rowspan=1 colspan=1>-</td></tr></table>

# 5 Power profiles

The USB Power Delivery protocol enables advanced voltage and current negotiation, to deliver up to100 Wo power, as defined in [21] and reported in the following figure:

![](images/fa89a951eca207949940f26b376072429d85c5228db7a14c7203cefd2863abf1.jpg)  
Figure 4. Power profile   
Tabl 8 shows he permittd voltage source and programable power supply ) selections, as  fncn the cable current rating.

Table 8. Fixed and programmable power supply current and cabling requirements   

<table><tr><td rowspan=2 colspan=1>Power range</td><td rowspan=1 colspan=4>Fixed voltage source</td><td rowspan=1 colspan=4>Programmable power supply (PPS)</td></tr><tr><td rowspan=1 colspan=1>5 V</td><td rowspan=1 colspan=1>9 V</td><td rowspan=1 colspan=1>15 V</td><td rowspan=1 colspan=1>20 V</td><td rowspan=1 colspan=1>5 V (3.3 to5.9 V)</td><td rowspan=1 colspan=1>9 V (3.3 to11 V)</td><td rowspan=1 colspan=1>15 V (3.3t 16 V)</td><td rowspan=1 colspan=1>20 V (3.3to21 V)</td></tr><tr><td rowspan=1 colspan=4>With 3 A cable</td><td rowspan=1 colspan=3></td><td rowspan=1 colspan=1></td><td rowspan=1 colspan=1></td></tr><tr><td rowspan=1 colspan=1>0 W &lt; PDP &lt;= 15 W</td><td rowspan=1 colspan=1>PDP /5</td><td rowspan=1 colspan=1>-</td><td rowspan=1 colspan=1>-</td><td rowspan=1 colspan=1>-</td><td rowspan=1 colspan=1>PDP /5</td><td rowspan=1 colspan=1>&#x27;</td><td rowspan=1 colspan=1>-</td><td rowspan=1 colspan=1>-</td></tr><tr><td rowspan=1 colspan=1>15 W &lt; PDP &lt;= 27 W</td><td rowspan=1 colspan=1>3.0 A</td><td rowspan=1 colspan=1>PDP /9</td><td rowspan=1 colspan=1>-</td><td rowspan=1 colspan=1>-</td><td rowspan=1 colspan=1>3.0 A</td><td rowspan=1 colspan=1>PDP /9</td><td rowspan=1 colspan=1>-</td><td rowspan=1 colspan=1>-</td></tr><tr><td rowspan=1 colspan=1>27 W &lt; PDP &lt;= 45 W</td><td rowspan=1 colspan=1>3.0 A</td><td rowspan=1 colspan=1>3.0 A</td><td rowspan=1 colspan=1>PDP /15</td><td rowspan=1 colspan=1>-</td><td rowspan=1 colspan=1>3.0 A</td><td rowspan=1 colspan=1>3.0 A</td><td rowspan=1 colspan=1>PDP /15</td><td rowspan=1 colspan=1>-</td></tr><tr><td rowspan=1 colspan=1>45 W &lt; PDP &lt;= 60 W</td><td rowspan=1 colspan=1>3.0 A</td><td rowspan=1 colspan=1>3.0 A</td><td rowspan=1 colspan=1>3.0 A</td><td rowspan=1 colspan=1>PDP / 20</td><td rowspan=1 colspan=1>3.0 A</td><td rowspan=1 colspan=1>3.0 A</td><td rowspan=1 colspan=1>3.0 A</td><td rowspan=1 colspan=1>PDP / 20</td></tr><tr><td rowspan=1 colspan=9>With 5 A cable</td></tr><tr><td rowspan=1 colspan=1>60 W &lt; PDP &lt;= 100 W</td><td rowspan=1 colspan=1>3.0 A</td><td rowspan=1 colspan=1>3.0 A</td><td rowspan=1 colspan=1>3.0 A</td><td rowspan=1 colspan=1>PDP / 20</td><td rowspan=1 colspan=1>3.0 A</td><td rowspan=1 colspan=1>3.0 A</td><td rowspan=1 colspan=1>3.0 A</td><td rowspan=1 colspan=1>PDP / 20</td></tr></table>

Further information is available in [21] and [22].

# 6 USB Power Delivery 2.0

In U Deliy t pvol no and data flow over the USB cable. The CC wire is used as a BMC-coded communication channel. The mechanisms used operate independently of other USB power negotiation methods.

# Power Delivery signaling

All communications are done through a CC line in half-duplex mode at 300 Kbit/s.   
Communication uses BMC encoded 32-bit 4b/5b words over CC lines.

# 6.1.1

# Packet structure

The packet format is:

Preamble: 64-bit sequence of alternating 0s and 1s to synchronize with the transmitter.

SOP\*: start of packet. Can be SOP, SOP' start of packet sequence prime) or SOP" (start of packet sequence double prime), see Figure 5. SOP\* signaling.

SOP packets are limited to PD capable DFP and UFP only SOP' packets are used for communication with a cable plug attached to the DFP SOP" packets are used for communication with a cable plug attached to the UFP.

A cable plug capable of SOP' or SOP" communication must only detect and communicate with packets starting with SOP' or SOP".

Message data including message header which identifies type of packet and amount of data

• CRC: error checking

D EOP: end of packet, unique identifier.

![](images/8074714c584d9cfb596f8094931a0954da0b1708e8cb4f10e2e4d7c0f4b9f63c.jpg)  
Figure 5. SOP\* signaling

# 6.1.2

# K-codes

K-cdes are special symbols provided by the b5 coding. They signal hard reset, cable reset, and deleate packet boundaries.

# 6.2

# Negotiating power

The DFP is initially considered as a bus master.

The protocol layer allows the power configuration to be dynamically modified.

The power ole data role and VConN swapae possible independentl both ports support dual powerl unctionality.

The default voltage on VBUS is always 5 V and can be reconfigured as up to 20 V.

Tupbilaly    u electronically marked USB PD Type-C cable.

The protocol uses start-of-packet (SOP) communications, each of which begins with an encoded symbol (Kcode).

SOP communication contains a control or data message.

The control message has a 16-bit fixed size manages data flow.

The data message size varies depending on its contents. It provides information on data objects.

# 7 USB Power Delivery 3.0

From the power point of view, there are no differences between USB PD 2.0 and USB PD 3.0. AllUSB PD 3.0 devices are able to negotiate power contracts with USB PD 2.0 devices, and vice-versa. USB PD 3.0 adds the following key features:

Fast role swap   
Authentication   
Firmware update   
Programmable power supply (PPS) to support sink directed charging

The following is a summary of the major changes between the USB PD 3.0 and USB PD 2.0 specifications:

Support for both Revision 2.0 and Revision 3.0operation is mandated to ensure backward compatibility wit existing products.   
Profiles are deprecated and replaced with PD power rules.   
BFSK support deprecated including legacy cables, legacy connectors, legacy dead battery operation and related test modes.   
Extended messages with a data payload of up to 260 bytes are defined.   
Only the VCONN source is allowed to communicate with the cable plugs.   
Source coordinated collision avoidance scheme to enable either the source or sink to initiate an atomic message sequence (AMS).   
Fast role swap defined to enable externally powered docks and hubs to rapidly switch to bus power when their external power supply is removed.

Additional status and discovery of:

Power supply extended capabilities and status Battery capabilities and status Manufacturer defined information

Changeso fields in the passive cable,active cable and AMA VDOs indicated by achange i thestructurd VDM version to 2.0.   
Support for USB security-related requests and responses.   
Support for USB PD firmware update requests and responses.

System policy now references USBTypeCBridge 1.0.

# Alternate modes

All the hosts and devices (except chargers) using a USB Type-C® receptacle shall expose a USB interface. If the host or device optionally supports alternate modes:

The host and device shalluse USB Power Delivery structured vendor defined messages (structured VDMs) to discover, configure and enter/exit modes to enable alternate modes.   
It istrongly ncoragedthat the device provide equivalent Ufnctinality where such exists for he best user experience.   
Where no equivalent USB functionality is implemented, the device must provide a USB interface exposing a USB billboard deviceclass to providenormatinneeded to identify he deviceA device isnot requie to provide a USB interface exposing a USB billboard device class for non-user facing modes (for exmple diagnostic modes).

Aaltenatmod ottravereheUSBhubtologyheymustnly eused between a d o host and device.

# 8.1

# Alternate pin reassignments

In Figure 6, pins highlighted in yellow are the only pins that may bereconfigured in a fullfeature cable.

Figure 6. Pins available for reconfiguration over the full featured Cable   

<table><tr><td>A12</td><td>A11</td><td>A10</td><td>A9</td><td>A8</td><td>A7</td><td>A6</td><td>A5</td><td>A4</td><td>A3</td><td>A2</td><td>A1</td></tr><tr><td>GND</td><td>RX2+</td><td>RX2-</td><td>VBUS</td><td>SBU1</td><td>D-</td><td>D+</td><td>CC</td><td>VBUS</td><td>TX1-</td><td>TX1+</td><td>GND</td></tr><tr><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td></tr><tr><td>GND</td><td>TX2+</td><td>TX2-</td><td>VBUS</td><td>VCONN</td><td></td><td></td><td>SBU2</td><td>VBUS</td><td>RX1-</td><td>RX1+</td><td>GND</td></tr><tr><td>B1</td><td>B2</td><td>B3</td><td>B4</td><td>B5</td><td>B6</td><td>B7</td><td>B8</td><td>B9</td><td>B10</td><td>B11</td><td>B12</td></tr></table>

Reconfigurable pin

v Figure 6 because this configuration is not limited by the cable wiring.

Figure 7. Pins available for reconfiguration for direct connect applications   

<table><tr><td>A12</td><td>A11</td><td>A10</td><td>A9</td><td>A8</td><td>A7</td><td>A6</td><td>A5</td><td>A4</td><td>A3</td><td>A2</td><td>A1</td></tr><tr><td>GND</td><td>RX2+</td><td>RX2-</td><td>VBUS</td><td>SBU1</td><td>D-</td><td>D+</td><td>CC</td><td>VBUS</td><td>TX1-</td><td>TX1+</td><td>GND</td></tr><tr><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td></tr><tr><td>GND</td><td>TX2+</td><td>TX2-</td><td>VBUS</td><td>VCONN</td><td></td><td></td><td>SBU2</td><td>VBUS</td><td>RX1-</td><td>RX1+</td><td>GND</td></tr><tr><td>B1</td><td>B2</td><td>B3</td><td>B4</td><td>B5</td><td>B6</td><td>B7</td><td>B8</td><td>B9</td><td>B10</td><td>B11</td><td>B12</td></tr></table>

Reconfigurable pin

# Note:

SBU may be left open  no alternate mode is supporte When alternatemode is suppored, ad a resisor superior to 4 MΩ to ensure USB safe state.

# 8.2

# Billboard

The USB Billboard Device Class definition describes the methods used to communicate the alternate modes supported by a device container to a host system.   
This includes string descriptors to provide support details in a human-readable format.   
For more details, reer o [].

# 9 Product offer

STM32 MCUs and STM32 MPUs handle USB Type-C / USB Power Delivery interfacing by using the STM32 intratedUCPD USB Type- Power Delivery) peripheral, or  set f general-purpose GP) peripherals. See USB Type-C and Power Delivery application page.

![](images/dafbb4a0c3c52cd4944aadda8341e92ec297e6da08659a75394359c4e69f9cc1.jpg)  
Figure 8. USB Type-C Power Delivery block diagram

![](images/82b86fdaaed51c87d960b972967aadfca9891cf3c3a9e3e55101c50e43c84ac4.jpg)  
Figure 9. STM32G0 Discovery kit USB Type-C analyser

# STM32 MPU product specificities

For the STM32 MPU products, take into the consideration the following:

USB is only supported on Cortex-A7 core. No support on Cortex-M4 core.   
For compatibility with Linux framework, USB Type-C is managed by external devices. Refer to MB1272- DK2-C01 board schematics on , CN7 implementation with STUSB1600 chipset (as opposed to CN6 implementation with ADC).

FonenUSB ousUB c

# 10 Type-C with no Power Delivery

Ti chapermay not fu apply  pu e rucr he .

# STM32 USB2.0-only device conversion for USB Type-C platforms

A USB2.0 legacy device needs to present itse as a UFP b eans f an Rd pull-down resistor between he CC line and ground. It is assumed here that the maximum legacy USB 2.0 device current is needed, and it is therefore not necessary to monitor the CC lines.

She pli veibl e  D pai eed eo eac othe los  posble receptacle, before being routed to the STM32 device.

![](images/b55bd4c34c18ed52b52296453563cefb6a74f96df1f6deef209eacc24645cd5e.jpg)  
Figure 10. Legacy device using USB Type-C receptacle

# 10.2

# STM32 USB2.0 host conversion for USB Type-C platforms

his use case describes how to exchange a USB2.0 standard A receptacle for a USB Type-C® receptacle.

the plaor  esie  USB., theaxiucu apaciy 00A. I ahighe suply currt is available in the application, the Rp resistors can be adjusted to give 1.5 A or 3 A capability.

AUB2. legacy host needs o be conigured as a DFP bymeans  a Rp pull up resisor between the C ie and the 5 V supply.

As the plug is reversible, the two DP/DN couples need to be connected in pairs as close as possible to the receptacle, before being routed to the STM32 device.

Monitoring CC lines through the ADCIN inputs allow device-attachment detection and enabling of VBUSon the connector.

![](images/095a4bfaedf8129fd7fb2db82b9faedf350d23398a8674c8f4ad5684769226fa.jpg)  
Figure 11. Legacy host using USB Type-C receptacle

# 10.3

# STM32 legacy USB2.0 OTG conversion for USB Type-C platforms

This use case explains how to exchange USB2.0 micro-AB receptacle for a USB Type-C® receptacle.

In thiuse case the platform is desined or USB.,  the maximu current capacity s 00 mA. I ahie u blpln  u

A legacy OTG platform starts to work as host or device depending on the USB_ID pin impedance to ground provided by the cable.

USBT vbl y by sensing the CC lines (for example by using the ADC through its ADC_IN1 and ADC_IN2 inputs to detect the CC line level).

![](images/dee934cf53941aec299058a11fade3496099faa187268494b44bc9e6138cee59.jpg)  
Figure 12. Legacy OTG using USB Type-C receptacle

The suggested sequence is:

1. Connect GPIO1 to OTG_FS_DFP_UFP driving a high level, and GPIO2 to Switch_enable driving a low level, to identify the platform as UFP.   
2. If VBUS is detected, the platform starts with the USB2.0 controller acting as a device.   
3. If no VBUS is detected after 200 ms minimum, OTG_FS_DFP_UFP is pulled down to be identified as a DFP through the Rp resistors, and to check whether a UFP is connected by comparing the ADC_IN1 and ADC_IN2 voltages to the expected threshold on the CC lines. Power switch X1 is kept disabled.   
4. If UFP connection is detected, Switch_enable is pulled up to provide VBUS on the connector, and the platform starts with the USB2.0 controller acting as host.

Bee pl eibily e   pai ee  s pai cos ossbl receptacle, before routing to the STM32 device.

# Type-C with Power Delivery using integrated UCPD peripheral

chamay notu ply P p.ecf he .

# STM32 MCU software overview

STicroelectronics delivers a proprietary USB Power Delivery stack based on the USB.org specification. The stack architecture overview is shown below.

![](images/fc77e3a2596ce04018b849601f078004d9db408de9bf528bd2c2cfe5f2ca0bc8.jpg)  
Figure 13. USB Power Delivery stack architecture

Tw parts are flly managed by STMicroelectronics (USB PD core stack and USB PD devices), s the user only needs to focus development effort on two other parts:

User application part: called the 'device policy manager' inside the USB organization specification. STMicroelectronics delivers an application template to be completed according to the application need. Hardware part: the effort is mainly focused on energy management, which depends on the resource materials chosen by the user to manage Type-C power aspects.

This document provides hardware implementation guidelines for the use of the STM32 resources (ADC, GPIO, an so n, ut he eerence or power constraints r the developers s hapterin Power suppl e Universal Serial Bus Power Delivery Specification. Also refer to [1] for further information.

# Note:

The STMicelectrnis core stack isdelivered as a certifd library to ollow heUSB Power Delivy requirements (USB Power Delivery protocol, State machine specification). API description is defined in this document [1].

# 11.2

# STM32 MPU software overview

The power delivery controller can be monitored using USB Type-® Connector System Software Interface [24].   
The kernel driverof the UCSI layer is available in Linux Community on top of DevicePolicyManager (DPM).   
All schematics available for the STM32 MCU integrated UCPD peripheral can be applied.   
The hardware link used for the UCSl communication can be an I2C bus.

![](images/922aff934b98e05a361b136e3b925a965e7b440b275f1c98007c13b74e8bcdad.jpg)  
Figure 14. STM32 MPU software overview

# Resources

X-UBE-UCSI   TMl . I is sUSB Ty®   eli expansion for STM32Cube.

X-CUBE-UCSI package consists of libraries, drivers, sources, APIs, and application examples runnig on STM32G0 32-bit microcontroller. This microcontroller acts as an UCSI Plaform Policy Manager (PPM) on the STM32MP135F-DK board. The PPM is a combination of hardware and firmware that manages the USB Type-C® conecors on the platform. The TM32MP13has a roleof UCSI OS Policy Manager (OPM) to interface with the PPM, via I2C with the UCSI interface.

# 11.3 Hardware overview

Using the STM32 UCPD peripheral, flexible and scalable architectures can be achieved. TM32 GP peripherals such as PWM, ADC, DAC, I2C, SPI, UART, COMP, OPAMP, RNG, and RTC can be used. See the STM32CubeMx pinout tools for detailed information.

![](images/2af628efe4f5d3bc1a0cbaa72acb96a9ebbf10c6eec57dafcb81fd5a6c8f586f.jpg)  
Figure 15. Device pinout example

Te following scins howhow plement each power mode om hehardware point vwl inoratin concerning the software implementation is available in the reference specification.

# 11.3.1

# DBCC1 and DBCC2 lines

# Recap of Dead battery functionality in Type-C systems

AUSB Type-C sink supporting the Dead battey fnction keeps pulling the attached CC line(s) down as per Table9 even whenupowered.According the USB Type-standard, this can be implemented as a resistor a a etc hat e spwe whi coesponddea batteyrbatty-oweaplcatinTeUSB Type-C source (for example a battery charger) can then supply power through the VBUS line.

Table 9. USB Type-C sink behavior on CC lines   

<table><tr><td rowspan=2 colspan=1>State</td><td rowspan=1 colspan=2>Pull-down function on CC lines</td></tr><tr><td rowspan=1 colspan=1>Sink without Dead battery support</td><td rowspan=1 colspan=1>Sink with Dead battery support</td></tr><tr><td rowspan=1 colspan=1>Unpowered</td><td rowspan=1 colspan=1>None</td><td rowspan=1 colspan=1>5.1 kΩ resistor or a voltage clamp(DB)</td></tr><tr><td rowspan=1 colspan=1>Powered</td><td rowspan=1 colspan=1>5.1 kΩ</td><td rowspan=1 colspan=1>5.1 kΩ resistor</td></tr></table>

Whenhe USB Type-Csink is back t powered it changes the value  ts Rd pull-own resistance o n values specified for normal operation.

UpansitmDead bateyatBUS-po sae,eTypseat quihathe oeRvalue rom toperating"does not transihrough a statewithout any puldown reisanc It i tva parameters section of the USB Type-C specification for full requirements.

# Implementation on STM32 devices with integrated UCPD peripheral

The devices incorporate the Rp and Rd function of the CCx (x = 1 or 2) pins to fulfil the USB Type-C et. or e e batty upor,heCx  =  pi mus extally   wi respective CCx pins.

Control paths (1) to (3) shown in Figure 16 through Figure 19 manage the switching between Rp and Rd functionality on the CCx pins, according to the application topology and state.

When the STM32 device is unpowered, a voltage exceeding 1 V on the DBCCx pins acting as inputs activates, trh he ontrol path) heDead bay puowncnali B the epectivx p. It i mntbln pe action activates Rd or Rp value fornormal operation that the software application should set beforehand.

When the device is used as USB Type-C source or as a USB Type-C sink without Dead battery support, the DBCCx pis can e use as IOs cntoll rgh he control path (. In sucapplatns, a weak extal puls 0Ω  ha ullal on the corresponding CCx pin when the device is powered down.

# DBCCx usage in non-protected application

When the device is unpowered, the DBCCx pins act as inputs Ahigh level on a DBCCx has the consequenceo epsing Rd = DBon the coresponding CCx pin to signal dead battery state.For the device acting as ik to suport he Dead battey uncn when iretconeed with a USB Tpe-source, he DBCCx pi must e shorted with their corresponding CCx pins. As soon as the device is powered, the Rd exposed on its CCx pins u this configuration must be of Rd (pull-down) type.

![](images/b33b5bdf9015feb91e8286584bb8b342ca23d43c6535f9913d7c0a02a6d7cac6.jpg)  
Figure 16. Non-protected sink application supporting Dead battery feature

Table 10. Non-protected sink - sequence of exiting Dead battery mode   

<table><tr><td rowspan=1 colspan=1>Sequence</td><td rowspan=1 colspan=1>VBUS</td><td rowspan=1 colspan=1>VDD</td><td rowspan=1 colspan=1>Rd value</td><td rowspan=1 colspan=1>Comment</td></tr><tr><td rowspan=1 colspan=1>Step 0</td><td rowspan=1 colspan=1>OV</td><td rowspan=1 colspan=1>O V</td><td rowspan=1 colspan=1>DB</td><td rowspan=1 colspan=1></td></tr><tr><td rowspan=1 colspan=1>Step 1</td><td rowspan=1 colspan=1>5V</td><td rowspan=1 colspan=1>OV</td><td rowspan=1 colspan=1>DB</td><td rowspan=1 colspan=1>VBUS arrives</td></tr><tr><td rowspan=1 colspan=1>Step 2</td><td rowspan=1 colspan=1>5V</td><td rowspan=1 colspan=1>3.3 V</td><td rowspan=1 colspan=1>default Rd</td><td rowspan=1 colspan=1>device supply arrives</td></tr><tr><td rowspan=1 colspan=1>Step 3</td><td rowspan=1 colspan=1>5V</td><td rowspan=1 colspan=1>3.3 V</td><td rowspan=1 colspan=1>as selected by SW</td><td rowspan=1 colspan=1>upon write to ANAMODE</td></tr></table>

When the device acts as a USB Type-C source, the Rd on CCx pins must never be set to DB value. This is ensured by keeping the DBCCx pins separate from their corresponding CCx pins and by pulling them down tr haluc 0 eteal pulown iso whic hee a he o The solution also fits a non-protected non-Dead-battery sink application.

In both cases, when the device is powered, the DBCCx pins can be used as l/Os, as shown in Figure 17.

![](images/9e544b186ee3fac3cc3560f4efb1dacd8cc698d33bb3096040a2ee916b6beec2.jpg)  
Figure 17. Non-protected sink not supporting Dead battery feature

# DBCCx usage in protected application

A protecion circuit such as TCPP01-M12) can be placed between the STM32 device and the Type-C connecor lWhen ctiaaheeviC pi o  rotc evic el esuc ycor eptin atmayestcvwhen non-terminated cable  connected When deactivated it connects the device C pins t theType-conn.

TI the Type-C connector when unpowered (protection active), and it couples the CCx pin of the devices with the Type-C connector when powered (protection inactive or bypass).

For aplications spporting Dead batery feature, the active protection circuiton a CCx lie must esa Rd =DB hep Cx  Iv/evausas aVBUS v oBT oiargivoltenVBUShe o deactivated (its Rd deconnected and the CCx line connected with the device CCx pin). However, as the STM32 evimay ot t epl  ha istanmut ke vere Dead battey al exRd = DB h oe prote circ y he must  hor wih eco pin and it cannot be used for other purposes.

The following figure shows a typical application with protection, supporting Dead battery feature.

![](images/7611b15f7f04d30fda9469a3bb6b9fd1cf5c280fd6dacb5a519e3931d5c93ba9.jpg)  
Figure 18. Protected sink application supporting Dead battery feature

Te ollog tablehows Dead battey mode exi uenc or  USBType-sik aplcatn wih a pro circuit. The term connected/isolated means CCx pins connected / non-connected with Type-C source CCx lines. T  ae tvaR= De on sur.he protecion circit tate ypassmeans protection circuideactivated otecting thee n connecting the device CCx pins with the Type-C source CCx lines.

Table 11. Protected sink application - sequence of exiting Dead battery mode   

<table><tr><td rowspan=1 colspan=1>Sequence</td><td rowspan=1 colspan=1>VBUS</td><td rowspan=1 colspan=1>VDD</td><td rowspan=1 colspan=1>Protection circuitstate</td><td rowspan=1 colspan=1>Device CC pins/Rdvalue</td><td rowspan=1 colspan=1>Comment</td></tr><tr><td rowspan=1 colspan=1>Step 0</td><td rowspan=1 colspan=1>OV</td><td rowspan=1 colspan=1>OV</td><td rowspan=1 colspan=1>active</td><td rowspan=1 colspan=1>isolated/DB</td><td rowspan=1 colspan=1>-</td></tr><tr><td rowspan=1 colspan=1>Step 1</td><td rowspan=1 colspan=1>5V</td><td rowspan=1 colspan=1>0 V</td><td rowspan=1 colspan=1>bypass</td><td rowspan=1 colspan=1>connected/DB</td><td rowspan=1 colspan=1>VBUS arrives</td></tr><tr><td rowspan=1 colspan=1>Step 2</td><td rowspan=1 colspan=1>5V</td><td rowspan=1 colspan=1>3.3 V</td><td rowspan=1 colspan=1>bypass</td><td rowspan=1 colspan=1>connected/ default Rd</td><td rowspan=1 colspan=1>device supply arrives</td></tr><tr><td rowspan=1 colspan=1>Step 3</td><td rowspan=1 colspan=1>5 V</td><td rowspan=1 colspan=1>3.3 V</td><td rowspan=1 colspan=1>bypass</td><td rowspan=1 colspan=1>connected / as selectedby SW</td><td rowspan=1 colspan=1>upon write toANAMODE</td></tr><tr><td rowspan=1 colspan=1>Step 4</td><td rowspan=1 colspan=1>5 V</td><td rowspan=1 colspan=1>3.3 V</td><td rowspan=1 colspan=1>bypass, low power</td><td rowspan=1 colspan=1>connected / as selectedbby SW</td><td rowspan=1 colspan=1>upon I2C write toprotection circuit</td></tr></table>

T o  ebataoau device.

Itvvapola u paTeatllev e a     / figures show examples of the application topology for either case.

![](images/ac6a07e1e5105ebdaa4719efc61a420c0cb4cb0ae04691d1dbb28df1bc6ac79e.jpg)  
Figure 19. Protected sink application not supporting Dead battery feature - activation through supply

![](images/f45aab62e81e4db48a18f22651c07e3f4ff9eac998b0f97b3bfd79c9f1bfadb2.jpg)  
Figure 0. Protected sink application not supporting Dead battery feature - activation through dedicated input

# Summary of application topologies

The following table lists the principal topologies of USB Type-C application with compatible STM32 microcontrollers.

Table 12. Summary of principal Type-C application topologies   
Pertains to CCx line   

<table><tr><td rowspan=1 colspan=3>Application</td><td rowspan=1 colspan=2>DBCCx</td><td rowspan=2 colspan=1>Note</td></tr><tr><td rowspan=1 colspan=1>Protected(1)</td><td rowspan=1 colspan=1>Dead batterycompliant</td><td rowspan=1 colspan=1>Sink/source</td><td rowspan=1 colspan=1>Shorted withCCx</td><td rowspan=1 colspan=1>Reusable</td></tr><tr><td rowspan=1 colspan=1>No</td><td rowspan=1 colspan=1>Yes</td><td rowspan=1 colspan=1>Sink</td><td rowspan=1 colspan=1>Yes</td><td rowspan=1 colspan=1>No</td><td rowspan=1 colspan=1>-</td></tr><tr><td rowspan=1 colspan=1>No</td><td rowspan=1 colspan=1>No</td><td rowspan=1 colspan=1>Sink</td><td rowspan=1 colspan=1>No</td><td rowspan=1 colspan=1>Yes</td><td rowspan=1 colspan=1>Application must ensure low level on DBCCxwhen the device is unpowered.</td></tr><tr><td rowspan=1 colspan=1>Yes</td><td rowspan=1 colspan=1>Yes</td><td rowspan=1 colspan=1>Sink</td><td rowspan=1 colspan=1>Yes</td><td rowspan=1 colspan=1>No</td><td rowspan=1 colspan=1>Protection circuit deactivated when supplied</td></tr><tr><td rowspan=2 colspan=1>Yes</td><td rowspan=2 colspan=1>No</td><td rowspan=2 colspan=1>Sink</td><td rowspan=2 colspan=1>No</td><td rowspan=2 colspan=1>Yes</td><td rowspan=1 colspan=1>Protection circuit deactivated when supplied:the application must ensure low level onDBCCx when the device is unpowered.</td></tr><tr><td rowspan=1 colspan=1>Protection circuit deactivated by software: thedefault Rd is never exposed to Type-Csource.</td></tr><tr><td rowspan=1 colspan=1>No</td><td rowspan=1 colspan=1>Notapplicable</td><td rowspan=1 colspan=1>Source</td><td rowspan=1 colspan=1>No</td><td rowspan=1 colspan=1>Yes</td><td rowspan=1 colspan=1>Rp exposed on CCx when the device ispowered.The application must ensure low level onDBCCx when the device is unpowered.</td></tr></table>

# 11.3.2 Sink port

The USB Type-C Power Delivery sink (SNK) port exposes pull-down resistors (Rd) to the CC lines, and it consumes power from the VBUS line (5 V to 20 V and up to 5 A).

From a sink point of view:

# Mandatory

Type-C port asserts Rd (pull-down resistor) on CC lines VBUS sensing Source detach detection, when VBUS moves outside the vSafe5V range

# Optional

• Sink power from VBUS

# Optional protection

OVP as defined by usb.org: In the attach state, a sink should measure the VBUS voltage level. An STM32 general-purpose ADC can perform this measurement.

Protection and EMI fltering on CC1, CC2, and VBUS lines. See Section 14 Recommendations

The features are summarized in the following table:

Table 13. Sink features   

<table><tr><td rowspan=1 colspan=1>Feature</td><td rowspan=1 colspan=1>STM32peripheralsnvolved</td><td rowspan=1 colspan=1>numberof STM32pins</td><td rowspan=1 colspan=1>External components or devices</td><td rowspan=1 colspan=1>Comments</td><td rowspan=1 colspan=1>Signal name</td></tr><tr><td rowspan=1 colspan=1>Protocol</td><td rowspan=1 colspan=1></td><td rowspan=1 colspan=1></td><td rowspan=1 colspan=1></td><td rowspan=1 colspan=1></td><td rowspan=1 colspan=1></td></tr><tr><td rowspan=1 colspan=1>Communicationchannels CC1 andC2</td><td rowspan=1 colspan=1>UCPD: CC1,CC2</td><td rowspan=1 colspan=1>2</td><td rowspan=1 colspan=1>-</td><td rowspan=1 colspan=1>Mandatory. Able tohandle Rd and Rp</td><td rowspan=1 colspan=1>CC1, CC2</td></tr><tr><td rowspan=1 colspan=1>Dead battery</td><td rowspan=1 colspan=1>UCPD:DBC1,DBC2</td><td rowspan=1 colspan=1>2</td><td rowspan=1 colspan=1></td><td rowspan=1 colspan=1>Handles Rd</td><td rowspan=1 colspan=1>DBCC1,DBC2</td></tr><tr><td rowspan=1 colspan=1>VBUS level,VSafe5X,measurement</td><td rowspan=1 colspan=1>ADC</td><td rowspan=1 colspan=1>1</td><td rowspan=1 colspan=1>Resistor divider bridge with orwithout op-amp for safety purpose</td><td rowspan=1 colspan=1>Mandatory only forOVP protectionpurpose</td><td rowspan=1 colspan=1>V_SENSE</td></tr><tr><td rowspan=1 colspan=1>Power</td><td rowspan=1 colspan=1></td><td rowspan=1 colspan=1></td><td rowspan=1 colspan=1></td><td rowspan=1 colspan=1></td><td rowspan=1 colspan=1></td></tr><tr><td rowspan=1 colspan=1>Sink power from VBUS</td><td rowspan=1 colspan=1>-</td><td rowspan=1 colspan=1></td><td rowspan=1 colspan=1>DC/DC from VBUS to 3.3 V (VDD)</td><td rowspan=1 colspan=1>Optional, LDO,DC/DC, SMPS</td><td rowspan=1 colspan=1>-</td></tr><tr><td rowspan=1 colspan=1>Extra Power switch</td><td rowspan=1 colspan=1>GPIO</td><td rowspan=1 colspan=1>1</td><td rowspan=1 colspan=1>Power switch</td><td rowspan=1 colspan=1>Optional,MOSFET or powerswitch can be use</td><td rowspan=1 colspan=1>SNK_EN</td></tr><tr><td rowspan=1 colspan=4>Protection</td><td rowspan=1 colspan=1></td><td rowspan=1 colspan=1></td></tr><tr><td rowspan=1 colspan=1>CC1 and CC2</td><td rowspan=1 colspan=1></td><td rowspan=1 colspan=1></td><td rowspan=1 colspan=1>See Section 14 Recommendations</td><td rowspan=1 colspan=1>Optional</td><td rowspan=1 colspan=1>CC1 and CC2on Type-C side</td></tr><tr><td rowspan=1 colspan=1>VBus</td><td rowspan=1 colspan=1></td><td rowspan=1 colspan=1></td><td rowspan=1 colspan=1>See Section 14 Recommendations</td><td rowspan=1 colspan=1>Optional</td><td rowspan=1 colspan=1>VBUS onType-C side</td></tr><tr><td rowspan=1 colspan=1>Software</td><td rowspan=1 colspan=1></td><td rowspan=1 colspan=1></td><td rowspan=1 colspan=2></td><td rowspan=1 colspan=1></td></tr><tr><td rowspan=1 colspan=1>Message repetition</td><td rowspan=1 colspan=1>TIM</td><td rowspan=1 colspan=1></td><td rowspan=1 colspan=1></td><td rowspan=1 colspan=1>Used to drivetiming repetition1200 us et 900 μs</td><td rowspan=1 colspan=1>See UM2552for details</td></tr><tr><td rowspan=1 colspan=1>Messagetransmissions</td><td rowspan=1 colspan=1>DMA</td><td rowspan=1 colspan=1></td><td rowspan=1 colspan=1></td><td rowspan=1 colspan=1>For TX et RXtransfer</td><td rowspan=1 colspan=1>See UM2552for details</td></tr></table>

The following architecture schematics explain how to implement various sink modes.

# 11.3.2.1 VBUS-powered sink

From the STM32 point of view, VDD is generated from VBUS. An external LDO, DC/DC converter, or SMPS is used, and an optional power-switch wire on VBUS can power extra load. The SNK_EN GPIO pin controls this optional power-switch.

Regarding the protocol, two dedicated STM32 UCPD pins, DBCC1 and DBCC2, set Rd on the CC1 and CC2 l.The DBCC ies must be wired oCC nes.No softae actin s eed as R is present on the Clines through the DBCC lines, with or without the STM32 power supply (VDD). After STM32 power-up, the USB-PD software stack switches the resistor connection from the DBCC to the CC lines.

![](images/6e576ca54a987d8800684f020df3d4a91dabc6b3a28205001dbc9afac80b9992.jpg)  
Figure 21. Unprotected VBUS-powered (Dead battery) sink connections

# Signal description

CC1 and CC2 communication channel signals wired to dedicated Type-C connector pins   
The DBCC1 dead-battery signal is wired to CC1. This handles Rd when the STM32 is not powered via the CC1 line.   
The DBCC2 dead-battery signal is wired to CC2. This handles Rd when the STM32 is not powered via the CC2 line.

# Optional:

V_SENSE wired to an ADC through a resistor divider. VBUS voltage measurement for OVP and safety purposes. The software stack, using the HAL_ADC driver, measures the VBUS voltage level. SNK_EN signal GPIO connects and disconnects an optional VBUS load.

# Time line

![](images/4a59ccad22c4335ef26990e50717ebf4f9faf0e2272842275a0bab2a8bf70276.jpg)  
Figure 22. VBUS-powered sink timeline

The states are described below. Actions in italics are GPIO-based (ADC, IO, and so on):

State 0: No connection between equipment

Detach state Rp = 1.5A Rd = 5.1K (DBCC pin)

State 1: Connect cable; VBUS is in Attach state

State 2: STM32 boot, start application and initialize USB-PD software

State 3: Port partner starts AMS power negotiation

State 4: USB-PD: use Rd from CC instead of DBCC

State 5: SNK detects the attachment

State 6: USB-PD: Enable load using SNK_EN GPIO and a contract is establishea

State 7: USB-PD SW: OVP and safety are looking for V/I VBUS senses

State 8: Disconnect cable, VBUS is OFF on the sink side

State 9: Source discharges VBUS to vSafe0V

# 11.3.2.2

# Separately powered sink

The STM32 device is powered from a separate AC/DC or DC/DC converter, SMPS, LDO, or battery, and not from VBUS. An additional load can optionally be powered from VBUS through a power switch controlled by the SNK_EN GPIO.

Regarding the protocol, the CC1 and CC2 lines set Rd. The DBCC1 and DBCC2 lines must be connect to GND.

![](images/f66360ccfb05dedf4b0238d1290be998902dc57ff2d4f1ec8cd4051b741ab7f4.jpg)  
Figure 23. SNK external power connections

# Signal description

CC1 and CC2 communication channel signals wired to dedicated Type-C connector pins   
DBCC1 signal wired to GND (as dead-battery mode is not used)   
DBCC2 signal wired to GND (as dead-battery mode is not used)

# Optional:

V_SENSE signal wired to an ADC through a resistor divider VBUS voltage is measured for OVP and safety purposes The software stack, using the HAL_ADC, measures the VBUS voltage leve

SNK_EN signal GPIO pin connects and disconnects an optional VBUS load.

# Time line

![](images/a4a39d30eeaf1fdb5f92ca27879b510f5f565f70d4875c8930f4829b7a96cd98.jpg)  
Figure 24. Sink external power time line

The states are described below. Actions in italics are GPIO-based (ADC, IO and so on)

State 0: No connection between equipment

Detach state Rp = 1.5 A Rd = 5.1 K (CC pin) State 1: Connect cable. VBUS is in Attach state. State 2: AMS between SRC and SNK. State 3: USB-PD: Enable load using SNK_EN GPIO pin. State 4 SNK requests 9 V. State 5: USB-PD SW: OVP and safety are looking for V/I VBUS senses. State 6: SNK requests 15 V. State 7: SNK requests 5 V. State 8: Disconnect cable, VBUS is off on the sink side. State 9: Source discharge VBUS to vSafe0V.

# 11.3.3 Source port

T USB y-w Deivur RC) r  pu  Rp e Cean power over VBUS (5 V to 20 V and up to 5 A).

From a source point of view:

# Mandatory

Type-C port asserts Rp on CC lines   
Feed power to VBUS   
During detach or communication failure, the source reduces VBUS to vSafe0V. An STM32 GP GPIO discharges VBUS using an external MOSFET.

# Optional

• An STM32 GP ADC can do these measurements using a shunt or resistor bridge.

# Optional protection

Protection and EMI filtering on CC1, CC2 and VBus lines. See Section 14 Recommendations.

# Source features

The features are summarized in Table 14.

Table 14. Source features   

<table><tr><td rowspan=1 colspan=1>Feature</td><td rowspan=1 colspan=1>STM32Peripheralsinvolved</td><td rowspan=1 colspan=1>Numbero f STM32pins</td><td rowspan=1 colspan=1>External components or devices</td><td rowspan=1 colspan=1>Comments</td><td rowspan=1 colspan=1>Signal name</td></tr><tr><td rowspan=1 colspan=1>Protocol</td><td rowspan=1 colspan=1></td><td rowspan=1 colspan=1></td><td rowspan=1 colspan=1></td><td rowspan=1 colspan=1></td><td rowspan=1 colspan=1></td></tr><tr><td rowspan=1 colspan=1>CC1 and CC2communicationchannels</td><td rowspan=1 colspan=1>UCPD:CC1, CC2</td><td rowspan=1 colspan=1>2</td><td rowspan=1 colspan=1></td><td rowspan=1 colspan=1>Mandatory</td><td rowspan=1 colspan=1>CC1CC2</td></tr><tr><td rowspan=1 colspan=1>Dead Batterysupport</td><td rowspan=1 colspan=1>UCPD:DBCC1,DBCC2</td><td rowspan=1 colspan=1>2</td><td rowspan=1 colspan=1></td><td rowspan=1 colspan=1>Mandatory</td><td rowspan=1 colspan=1>DBCC1DBCC1</td></tr><tr><td rowspan=1 colspan=1>VBUS level,Safeov,measurement</td><td rowspan=1 colspan=1>ADC</td><td rowspan=1 colspan=1>1</td><td rowspan=1 colspan=1>Resistor bridge with or without op-amp for safety purpose</td><td rowspan=1 colspan=1>Mandatory(1)</td><td rowspan=1 colspan=1>V_SENSE</td></tr><tr><td rowspan=1 colspan=1>Power</td><td rowspan=1 colspan=1></td><td rowspan=1 colspan=1></td><td rowspan=1 colspan=1></td><td rowspan=1 colspan=1></td><td rowspan=1 colspan=1></td></tr><tr><td rowspan=1 colspan=1>Provide power fromVBUS</td><td rowspan=1 colspan=1>GPIO</td><td rowspan=1 colspan=1>1</td><td rowspan=1 colspan=1>Power switch</td><td rowspan=1 colspan=1>Mandatory,Dual-MOSFETcan be used</td><td rowspan=1 colspan=1>SRC_EN</td></tr><tr><td rowspan=1 colspan=1>Discharge VBUS toSafeov</td><td rowspan=1 colspan=1>GPIO</td><td rowspan=1 colspan=1>1</td><td rowspan=1 colspan=1>MOSFET + charge resistors</td><td rowspan=1 colspan=1>Mandatory</td><td rowspan=1 colspan=1>SRC_DISCH</td></tr><tr><td rowspan=1 colspan=1>ISensemeasurement</td><td rowspan=1 colspan=1>ADC</td><td rowspan=1 colspan=1>1</td><td rowspan=1 colspan=1>Op-amp + shunt resistors</td><td rowspan=1 colspan=1>Optional</td><td rowspan=1 colspan=1>I_SENSE</td></tr><tr><td rowspan=1 colspan=1>CC1 and CC2</td><td rowspan=1 colspan=1></td><td rowspan=1 colspan=1></td><td rowspan=1 colspan=1>See Section 14 Recommendations</td><td rowspan=1 colspan=1></td><td rowspan=1 colspan=1>CC1 and CC2 onType-C side</td></tr><tr><td rowspan=1 colspan=1>Protection</td><td rowspan=1 colspan=1></td><td rowspan=1 colspan=1></td><td rowspan=1 colspan=1></td><td rowspan=1 colspan=1></td><td rowspan=1 colspan=1></td></tr><tr><td rowspan=1 colspan=1>VBUS</td><td rowspan=1 colspan=1></td><td rowspan=1 colspan=1>-</td><td rowspan=1 colspan=1>See Section 14 Recommendations</td><td rowspan=1 colspan=1>-</td><td rowspan=1 colspan=1>VBUS on Type-Cside</td></tr><tr><td rowspan=1 colspan=1>Software</td><td rowspan=1 colspan=1></td><td rowspan=1 colspan=1></td><td rowspan=1 colspan=1></td><td rowspan=1 colspan=1></td><td rowspan=1 colspan=1></td></tr><tr><td rowspan=1 colspan=1>Message repetition</td><td rowspan=1 colspan=1>TIM</td><td rowspan=1 colspan=1></td><td rowspan=1 colspan=1>-</td><td rowspan=1 colspan=1>Used to drivetiming repetition1200 us et 900μs</td><td rowspan=1 colspan=1>See [1] for details</td></tr><tr><td rowspan=1 colspan=1>Messagetransmissions</td><td rowspan=1 colspan=1>DMA</td><td rowspan=1 colspan=1></td><td rowspan=1 colspan=1></td><td rowspan=1 colspan=1>For TX et RXtransfer</td><td rowspan=1 colspan=1>See [1] for details</td></tr></table>

1For certification purposes, vsafe0V must be checked.

Figure 25 explains how to handle Source (SRC) mode. From the STM32 point of view, power is provided by an external source such as an AC/DC, DC/DC, SMPS, LDO, or battery.

Rp management is handled by the UCPD software stack. In this case, the DBCC lines must not be wired t the CC1 and CC2 lines. The DBCC1 and DBCC2 pins are wired to GND.

![](images/eb0bcc7f64e443afa6f1fe1222ef6d208cd5c7177b349cb5f712c2a57820a9df.jpg)  
Figure 25. Source architecture

The VCoNN circuit is not shown in this figure. See Section 13.1 Sourcing power to VBUS

# Signal description

CC1 and CC2 communication channel signals wired to dedicated Type-C connector pins   
the DBCC1 signal is wired to GND   
the DBCC2 signal is wired to GND

# Optional:

V_SENSE signal wired to an ADC through a resistor divider. VBUS voltage measurement for OVP and safety purposes. Software stack, using the HAL_ADC driver to measure the VBUS voltage level. In the case of negative VBUS transitions, for example 15 V to 5 V or 9 V to 5 V, a discharge path can be u before the oad switch (controlled by SRCE) to reduce he time needed o thi transition and to sty in specification.

# Time line

![](images/9962e893590ffb0d4904ed51172856c5737dbb48fff45814a9aa58a256d9127f.jpg)  
Figure 26. SRC (source) mode power timings

The states are described below. Actions in italics are GPIO-based (ADC, IO, and so on):

State 0: No connection between equipment

Detach state Rp = 1.5 A, Rd = 5.1 kΩ (CC pin)

State 1: Connect cable. VBUS is on

Attach state   
USB-PD switches on VBUS using the SRC_EN GPIO pin   
Capability exchange

State 2: AMS between SRC and SNK

State 3: USB-PD SW: OVP and safety are looking for V/I VBUS senses

State 4: Disconnect cable, VBUS is OFF on the sink side USB-PD initiates VBUS discharge using the DISCH GPIO pin, until VBUS reaches vSafeOV

State 5: Source VBUS discharged to vSafe0V

# 11.3.4

# Dual-role power port

g   e por oake e   wh  e prt keP role. The port role may be changed dynamically to reverse either power or data roles.

From a dual-role power port point of view:

# Mandatory

Type-C port asserts Rp on CC lines when in source mode   
Type-C port assert Rd on CC lines when in sink mode   
Feed power to VBUS   
During detach or communication failure, the source takes VBUS down to vSafe0v An STM32 GP GPIO discharges VBUS using an external MOS

# Optional

Measure VBUS voltage and current values A STM32 GP ADC can do this measurement using a shunt, or a resistor bridge   
Get power from VBUS   
Source 'detach' detection, when VBUS moves outside vSafe5V range   
Manage fast role swap (FRS) protocol. (USB-PD 3.0 only)

Optional protection

Protection and EMI filtering on CC1, CC2 and VBUS lines. See Section 14 Recommendations.

# Features

The features are summarized in Table 15:

Table 15. Dual-role power port features   

<table><tr><td rowspan=1 colspan=1>Feature</td><td rowspan=1 colspan=1>STM32Peripheralsnvolved</td><td rowspan=1 colspan=1>Number ofST32 pins</td><td rowspan=1 colspan=1>External componentsor devices</td><td rowspan=1 colspan=1>Comments</td><td rowspan=1 colspan=1>Signal name</td></tr><tr><td rowspan=1 colspan=1>Protocol</td><td rowspan=1 colspan=1></td><td rowspan=1 colspan=1></td><td rowspan=1 colspan=1></td><td rowspan=1 colspan=2></td></tr><tr><td rowspan=1 colspan=1>CC1 and CC2communicationchhannels</td><td rowspan=1 colspan=1>UCPD:CC1, CC2</td><td rowspan=1 colspan=1>2</td><td rowspan=1 colspan=1></td><td rowspan=1 colspan=1>MandatoryAble to handle Rd&amp; Rp</td><td rowspan=1 colspan=1>CC1CC2</td></tr><tr><td rowspan=1 colspan=1>Dead Battery</td><td rowspan=1 colspan=1>UCPD:DBCC1, DBCC2</td><td rowspan=1 colspan=1>2</td><td rowspan=1 colspan=1></td><td rowspan=1 colspan=1>MandatoryWire to GND</td><td rowspan=1 colspan=1>DBCC1DBCC1</td></tr><tr><td rowspan=1 colspan=1>VBUS Level, vSafe0V,vSafe5V,measurements</td><td rowspan=1 colspan=1>ADC</td><td rowspan=1 colspan=1>1</td><td rowspan=1 colspan=1>Resistor divider bridgewith or without op-Ampfor safety purpose</td><td rowspan=1 colspan=1>Mandatory for OVPprotection purpose</td><td rowspan=1 colspan=1>V_SENSE</td></tr><tr><td rowspan=1 colspan=1>Fast Role Swap</td><td rowspan=1 colspan=1>UCPD:FRSTX1,FRSTX2</td><td rowspan=1 colspan=1>2</td><td rowspan=1 colspan=1>MOS to drive CC linesto GND</td><td rowspan=1 colspan=1>Mandatory</td><td rowspan=1 colspan=1>FRSTX1FRSTX2</td></tr><tr><td rowspan=1 colspan=1>On Power level</td><td rowspan=1 colspan=1>-</td><td rowspan=1 colspan=1>-</td><td rowspan=1 colspan=1></td><td rowspan=1 colspan=1>-</td><td rowspan=1 colspan=1></td></tr><tr><td rowspan=1 colspan=1>Provide power fromVBUS</td><td rowspan=1 colspan=1>GPIO</td><td rowspan=1 colspan=1>1</td><td rowspan=1 colspan=1>Power switch</td><td rowspan=1 colspan=1>Mandatory, MOScan be use</td><td rowspan=1 colspan=1>SRC_EN</td></tr><tr><td rowspan=1 colspan=1>Extra Power switch</td><td rowspan=1 colspan=1>GPIO</td><td rowspan=1 colspan=1></td><td rowspan=1 colspan=1>Power switch</td><td rowspan=1 colspan=1>Optional, MOS canbe use</td><td rowspan=1 colspan=1>SNK_EN</td></tr><tr><td rowspan=1 colspan=1>Discharge VBUS toSafeov</td><td rowspan=1 colspan=1>GPIO</td><td rowspan=1 colspan=1>1</td><td rowspan=1 colspan=1>MOS + chargeResistors</td><td rowspan=1 colspan=1>Mandatory</td><td rowspan=1 colspan=1>SRC_DISCH</td></tr><tr><td rowspan=1 colspan=1>ISense measurement</td><td rowspan=1 colspan=1>ADC</td><td rowspan=1 colspan=1>1</td><td rowspan=1 colspan=1>OpAmp + shuntResistors</td><td rowspan=1 colspan=1>Optional</td><td rowspan=1 colspan=1>I_SENSE</td></tr><tr><td rowspan=1 colspan=1>Protection</td><td rowspan=1 colspan=1></td><td rowspan=1 colspan=1></td><td rowspan=1 colspan=1></td><td rowspan=1 colspan=1></td><td rowspan=1 colspan=1></td></tr><tr><td rowspan=1 colspan=1>CC1 and CC2</td><td rowspan=1 colspan=1></td><td rowspan=1 colspan=1>-</td><td rowspan=1 colspan=1>See chapter xxx</td><td rowspan=1 colspan=1>Optional</td><td rowspan=1 colspan=1>CC1 and CC2 onType-C side</td></tr><tr><td rowspan=1 colspan=1>VBUS</td><td rowspan=1 colspan=1></td><td rowspan=1 colspan=1>-</td><td rowspan=1 colspan=1>See chapter xxx</td><td rowspan=1 colspan=1>Optional</td><td rowspan=1 colspan=1>VBUS on Type-Cside</td></tr><tr><td rowspan=1 colspan=1>Software</td><td rowspan=1 colspan=1></td><td rowspan=1 colspan=1></td><td rowspan=1 colspan=1></td><td rowspan=1 colspan=1></td><td rowspan=1 colspan=1></td></tr><tr><td rowspan=1 colspan=1>same as previous</td><td rowspan=1 colspan=1>-</td><td rowspan=1 colspan=1>-</td><td rowspan=1 colspan=1></td><td rowspan=1 colspan=1></td><td rowspan=1 colspan=1></td></tr></table>

![](images/bb4951e2951866f764f51c9a51780ec0c0052d8bd73e4500b96399d4ee6ee0f1.jpg)  
Figure 27 shows the connections used in DRP mode.   
Figure 27. DRP connections

# Note:

the VCoNN circuit is not shown in this figure. See Section 13.1 Sourcing power to VBUS.   
The signal descriptions are given in Section 11.3.2 Sink port and Section 11.3.3 Source port.

# Time line

![](images/919d90cf310c470fe126b50a55eebb2fc6fe0f7b789b675ab6b1423117d34242.jpg)  
Figure 28. DRP with FRS mode time line example

The steps in italics are based on GPIOs (ADC, IO, and so n).

State 0: No connection between equipment

Detach state DRP = SRC role Rp = 1.5 A (CC pin)

State 1: USB-PD stack decide to move from SRC to SNK role DRP = SNK role Rd = 5.1K (CC pin)

State 2: USB-PD stack decide to move from SNK to SRC role DRP = SRC role Rp = 1.5A (CC pin)

State 3: USB-PD stack decide to move from SRC to SNK role DRP = SNK role Rd = 5.1K (CC pin)

# 11.3.5 Dual-role power port with FRS

In this configuration, the STM32 device is supplied from a separate source such as an AC/DC or DC/DC converter, SMPS, LDO, or battery. The UCPD peripheral handles Rp and Rd through software. The powerrole, source or sink, can be changed on-the-fly without any cable disconnect when both devices are DRP ports.

F allos   s pea pwe)l contion to a sink with fast role swap capability r more rapidy than without RS.s RS sinaling/detecton worksdurig esaging andregardless o the collision control, it takes o lngerthan 0 s.Once tesi Rl  atc VBU evel roTeiolRCk the VBUS drive within a delay (for example 150 µs) specified by the FRS procedure.

![](images/88ce4f347104fec2f9c3e317f18a86fbe1b1a883e7bdc2bdc4dee0fe6e4fb055.jpg)  
Figure 29. DRP with FRS VBUS = 5 V / 9 V / 15 V connections   
Note that the VCoNN circuit is not shown in this figure. See Section 1.1Sourcing power to VBUS.

# Signal description

The CC1 and CC2 communication channel signals wired to dedicated Type-C connector pins   
The DBCC1 signal is wired to GND.   
The DBCC2 signal is wired to GND.   
The SRC_EN signal GPIO pin is used to switch-on VBUS using an external MOSFET or power switch. The SRC_DISCH signal GPIO pin initiates the discharge of VBUS on detach. An external MOSFET can be used.   
The FRSTX1 and FRSTX2 fast role swap signals are wired to external MOSFETs to drive the CC lines. The V_ SENSE signal is wired to an ADC through a resistor divider. The VBUS voltage measurement for OVP and safety purpose. The software stack, using the HAL_ADC driver, measures the VBUS voltage level. The I_SENSE signal is wired to an ADC through a resistor shunt. VBUS current measurement for safety purposes. The software stack, using the HAL_ADC driver, measures the VBUS current level.   
The SNK_EN signal GPIO pin is used to connect and disconnect an optional VBUS load.

# Time line

![](images/1bce3a47be96bdf123427106408818c72cb4a633871b70949f1f1be710bac521.jpg)  
Figure 30. DRP with FRS - time line example

The steps in italics are based on GPIOs (ADC, IO, and so on)

• State 0: No connection between equipment Detach state Rp = 1.5A Rd = 5.1K (CC pin)

State 1: Connect cable VBUS is on DRP1 set SRC_EN GPIO pin

State 2: Capabilitiy exchanges DRP2 switches the on load on VBUs using the SNK_EN GPIO pin

State 3: FRSTX (fast role swap) start

State 4: DRP1 moves VBUs to vSafe0V

State 5: The DISXH GPIO pin initiates the DRP1 discharge

State 6: End of VBus discharge

State 7: Role swap between DRP1 and DRP2

State 8: DRP2 enables VBUS using the SRC_EN GPIO pin

State 9: DRP1 uses the SNK_EN GPIO pin on the VBUs load ON

• State 10: Disconnect cable

State 11: End of discharge

# 12 Type-C with Power Delivery using a general-purpose peripheral

Ti chapermaynot fu apply   pu er cruc orhe e.

# 12.1

# Software overview

The software architecture is the same as that described in Section1.ST32 MCU software overviw.

# 12.2 Hardware overview

![](images/3d3d28385d7e9e73133e46524d7d080e8a9cf96feaf0d7564d2435e043ae844a.jpg)  
Figure 31. Hardware view for Type-C Power Delivery with a general-purpose peripheral

Using a general-purpose peripheral, the TCPM/TCPC interfaces are a convenient way of handling USB Power Delivery. STM32 MCUs and STM32 MPUs using a communication bus can handle alI TCPM/TCPC companion chips.

Usually the I2C, SPI or GPIOs are used to handle communication messages and exceptions.

# 12.2.1

# Sink port using TCPM/TCPC interface

In sink (SNK) mode, the Type-C port must expose Rd (pull-down resistor) on CC lines and takes power from VBUS. The sink detects source attachment when VBUS reaches vSafe5V. Detection requires an ADC for example.

The STM32 communicates with the TCPM/TCPC interface, typically using the I2C bus. In some cases an SPI, ADC, DAC, or GPIO completes the communication between the STM32 general-purpose MCU and the TCPM/ TCPC external component.

![](images/db7ecc54d062744405857d513dea45f6aada503b151139b01f733dee59c935ff.jpg)  
Figure 32. Sink port using TCPM/TCPC interface

# 12.2.2

# Source port using TCPM/TCPC interface

In rc RC) mode, e Type- port must eposeRp (pllp reisor) o the C lies and provie powr throgh B.Durig detachcommunications failures, e source musteduceB SafeV.Thisme that a device must discharge VBUS.

The STM32 (acting as TCPM) usually communicates with TCPM/TCPC interfaces using the I2C bus. In some cases an SPI, ADC, DAC, or a GPIO complete the communication between the STM32 general-purpose MCU and TCPM/TCPC external components.

![](images/35ae52261a7232917c12b767722807378af56ea288cb4ca38304e19a3ccab4e5.jpg)  
Figure 33. Source mode using TCPM/TCPC interface

# 12.2.3

# Dual-role power port using TCPM/TCPC interface

Aa-o pr RP) por an ete hes RC)   STheoe  he port n e pr oake le c r wheet  he orak sre faci prt Te porea hannamilevr ee poweatos.

The STM32 usually communicates with the TCPM/TCPC interface using the I2C bus. In some cases, an SPI, ADC, DAC, or GPIO completes communications between the STM32 general-purpose MCU and the TCPM/ TCPC external component.

![](images/463f7af661c073338333541a504e3866a32f298bb5ded2761e1cb7e84a67a6cb.jpg)  
Figure 34. Dual-role power port using TCPM/TCPC interface

# 13 Dedicated architecture proposals and solutions

Thichaermay not ly ply  ps ecuc f orhe se.

# 13.1 Sourcing power to VBUS

SRC port and DRP acting as Power Delivery source provide power to the VBUS line. Commonly used power stages include DC/DC converter, AC/DC converter, and switched-mode power supply (SMPS), with or without a bateryA powe switchconets theiroutput (VOUT t theVBUS i.The general-purposeTM32 ADC, DAC, GPIOand I2C periherals alow flexible and scalable powerstage control,as shown he ollwi gure.

![](images/5542372b728b488aecf9b223b32ad11ca741256d6ad31a16bfe8bdcf92627bb4.jpg)  
Figure 35. Sourcing power to VBUS

# Signal description

ADC: VBUS voltage and current measurement GPIO: power switch control, power stage enable, error sensing PWM or DAC: voltage reference to the power stage I2C: digital control of a power stage with I2C-bus.

In a STM32G implementation, the DC/DC converter i driven by a PWM generated with a timer (available n he STM32,). The aim is to determine the PWM corresponding to the requested voltage. An iteration algorithm estimates the target PWM, and a voltage measurement confirms whether the expected value is reached.

# 13.2

# DC/DC output control with GPIOs

# Control through a resistor bridge switched with GPIOs

the desired value with open-drain GPlOs, as shown in the following figure.

![](images/426b7cec0b4d55a1679cff049c0794c3e71e743b555f65288182f9d95a46c494.jpg)  
Figure 36. Setting VRef with a switched resistor bridge

# Control with a GPIO acting as a PWM output

The VREF evoltages t wi rieR/Rivi eVOT eoltaeandwit e PWMrur line voltage.

![](images/51752dbd9e5bcedfd9355a502659cb0f1b3875d1793dd838dbf5a993f1c0c349.jpg)  
Figure 37. Setting VRef with a PWM GPIO

# Control with a GPIO acting as a DAC output

The VREF line voltage can be driven by an STM32 DAC output.

# 13.3

# Applying Vconn on CC lines

An SRC port or a DRP playing the role of source must support VCONN function in the following cases:

to supply or draw more than 3 A to support USB3

Agleovoltage generator is present in he syste.Two powries apply eo 5t the CC1 or CC2 pin, and simultaneously, two MOSFETs isolate the STM32 UCPD CC1 and CC2 pins from the CC lines. Two FRS commutation MOSFETs discharge the CC lines when the power switches stop applying Vconn to the CC lines.

This implies the use of at least two GPIOs to control VCONN_EN1 and VCONNEN2, as shown in the following figure.

![](images/28b9d95f4a4886043528a6707b9e7377f29bbc4cddef84fb8e3c7b6c56d0312d.jpg)  
Figure 38. Applying Vconn on CC lines

# Signal description

Two GPIOs (shown as VCONNEN1 and VCONN_EN2 in the figure) control the switch to apply VcoNn to the CC lines and the simultaneous isolation of the STM32 CC pins from the CC lines.   
For software details, see [1].

# 13.3.1 Time line

![](images/1e2fb33576971153be1c501b4d0fa00a8652386d90e560beb823df019ee73f01.jpg)  
Figure 39. Applying Vconn - time line example

The squenc s s ollows, whee acns  alic a base n GPIOs (ADC, IO, and ):

State 0: No connection between equipment

Detach state Rp = 1.5A Rd = 5.1K (CC pin)

State 1: Connect cable. VBUS is turned on using the SRC_EN GPIO. Attach state. USB-PD switch on VBUS using SRC_EN GPIO pin capabilities exchanged

State 2: Request VCONN ON

State 3: Enable VCONN using VCONN_EN1/2 GPIOs

State 4: USB-PD SW: OVP and safety are looking for V/I VBUS senses

State 5: Request VCONN ON

State 6: Disable VCONN using VCONN_EN1/2 GPIOs Start discharging CC1/2 line using FRSTX pin or a GPIO

State 7: Disconnect cable, VBUS is OFF on the sink side USB Power Delivery uses the DISCH GPIO pin to initiate the VBUS discharge until the VBUS voltage reaches vSafe0v

State 8: The VBUS voltage reaches vSafe0V

# 13.4 FRS signalling

FRS snaling is nly requr or Tp-DRP role apigOnly  DRP erang   powouroally sends FRS signals on power-outage detection.

FRS signaling (TX): UCPD peripheral requires external hardware to pull the CC line strongly to GND

This implies two external NMOS transistors, controlled by the STM32 UCPD peripheral One per CC line, controlled with GPIO set to the corresponding FRSTX1 or FRSTX2 AF

FRS detection (RX): The detection of FRS signaling is internal. It can be enabled by software.

• Software uses a UCPD interruption.

T UCPD hl oiol  RSTX)ilblulpei I oy written to  to start the RS signaligcondition.Thecondition is auto-cleared in order to respect he required timing. See the relevant TM32 MCU or MPU product datasheet for further details.This behavior is eliyalpoI power roles for a source that loses its ability to supply power.

ADRinsur SRC) moesas FRS ale on  ore  ap pweole hat, he VBUS source) as quickly as possible. Typically, this is useful in the absence of a local battery.

When the VCONN feature is used, FRSTX1 and FRSTX2 discharge the CC1 and CC2 lines through MOSFETs.

![](images/e90fafa07aa90afbc888c1c1baa089b7cf2524aaa35d5068f4065b94c146cab7.jpg)  
Figure 40. Fast role-swap DRP mode circuit

# 13.5

# Monitoring VBUS voltage and current

# Protection and safety

ADC/DCconverter circuit, such as theL7987, isuse o generate VBUS and VCONN, and inclues builtOTP O eror   espln ve  y . To do this, the DC/DC fault output signal can be routed to EXTI on the STM32 side.

# PD protocol

A SNK port or a DRP in the role of power sink measures the VBUS level to handle REQUEST_ACCEPT / PS_RDY / DETACH protocol messages on the software side. For this purpose, one ADC is required on the STM32 side.

A SRC port or a DRP in therole of power source provides power to the VBUS and keeps ts voltage within the specified target (through monitoring it and controlling the DC/DC converter), for PDO or APOD uses cases.

# Method

measetial BUcnt,ua lo eisanshunt.Tmeas Bvolt  bas bridge. Optionally add an operational amplifier for OvP and safety purposes.

Note:

TSC1641, TSC2011 and TSC2012 precision bidirectional current sense amplifier can be used. See datasheets on www.st.com.

![](images/da48750e5e901eb60a21cb4a11db9f41cf13368329589e1ee9a5a07cc4703ba8.jpg)  
Figure 41. VBUS voltage and current monitoring circuit

Note: Extra protection (P1 in Figure 41) in can be added on Isense and Vsense. See Section4 Recommendations

# 13.6

# Dual-role power por

Dual-role power port application examples based on STM32G0 and TCPP03 STMicroelectronics part numbers are given be in Figure 42 and Table 16. The NUCLEO-G071RB and X-NUCLEO-DRP1M1 can be used for fast prototyping.

![](images/2feba7342bdb93a094e3b19f30623101d6590f0a80add5d63508b9146756c3ae.jpg)  
Figure 42. STM32G0 pin/resource assignments

Table 16. STM32G0 resources   

<table><tr><td rowspan=1 colspan=1>Item</td><td rowspan=1 colspan=1>X-NUCLEO G0-1Address: Ox68</td><td rowspan=1 colspan=1>X-NUCLEO G0-2Address: Ox6A</td><td rowspan=1 colspan=2>STM32G0 IOsUCPD1 left - UCPD2 right</td><td rowspan=1 colspan=1>Comment</td></tr><tr><td rowspan=1 colspan=1>I2C1 SCL</td><td rowspan=1 colspan=2>CN10-3(1)</td><td rowspan=1 colspan=2>PB8</td><td rowspan=1 colspan=1>-</td></tr><tr><td rowspan=1 colspan=1>I2C1 SDA</td><td rowspan=1 colspan=2>CN10-5(1)</td><td rowspan=1 colspan=2>PB9</td><td rowspan=1 colspan=1></td></tr><tr><td rowspan=1 colspan=1>CC1</td><td rowspan=1 colspan=1>C10-23/C10-17(1)</td><td rowspan=1 colspan=1>CN7-9(1)</td><td rowspan=1 colspan=1>PA8</td><td rowspan=1 colspan=1>PDO</td><td rowspan=1 colspan=1>-</td></tr><tr><td rowspan=1 colspan=1>CC2</td><td rowspan=1 colspan=1>C10-26/C10-27(1)</td><td rowspan=1 colspan=1>CN7-4(1)</td><td rowspan=1 colspan=1>PB15</td><td rowspan=1 colspan=1>PD2</td><td rowspan=1 colspan=1></td></tr><tr><td rowspan=1 colspan=1>GPIO FIgn</td><td rowspan=1 colspan=1>CN10-37(1)</td><td rowspan=1 colspan=1>CN10-29(1)</td><td rowspan=1 colspan=1>PC5</td><td rowspan=1 colspan=1>PB5</td><td rowspan=1 colspan=1>Wake-up GPIO</td></tr><tr><td rowspan=1 colspan=1>ADC Vbusc</td><td rowspan=1 colspan=1>CN7-28(1)</td><td rowspan=1 colspan=1>CN10-13(1)</td><td rowspan=1 colspan=1>PAO/INO</td><td rowspan=1 colspan=1>PA6/IN6</td><td rowspan=1 colspan=1></td></tr><tr><td rowspan=1 colspan=1>ADC Prov</td><td rowspan=1 colspan=1>CN7-30(2)</td><td rowspan=1 colspan=1>CN10-15(2)</td><td rowspan=1 colspan=1>PA1/IN1</td><td rowspan=1 colspan=1>PA7/IN7</td><td rowspan=1 colspan=1></td></tr><tr><td rowspan=1 colspan=1>ADC Cons</td><td rowspan=1 colspan=1>CN7-32(2)</td><td rowspan=1 colspan=1>CN10-17(2)</td><td rowspan=1 colspan=1>PA4/IN4</td><td rowspan=1 colspan=1>PBO/IN8</td><td rowspan=1 colspan=1></td></tr><tr><td rowspan=1 colspan=1>ADC Isense</td><td rowspan=1 colspan=1>CN7-36(2)</td><td rowspan=1 colspan=1>CN10-38(2)</td><td rowspan=1 colspan=1>PB11/IN15</td><td rowspan=1 colspan=1>PB12/IN16</td><td rowspan=1 colspan=1></td></tr><tr><td rowspan=1 colspan=1>ENABLE</td><td rowspan=1 colspan=1>CN10-2</td><td rowspan=1 colspan=1>CN10-1</td><td rowspan=1 colspan=1>PC8</td><td rowspan=1 colspan=1>PC9</td><td rowspan=1 colspan=1>Vddl via GPIO</td></tr><tr><td rowspan=1 colspan=1>D+</td><td rowspan=1 colspan=1>CN10-12</td><td rowspan=1 colspan=1>-</td><td rowspan=1 colspan=1>PA12</td><td rowspan=1 colspan=1>N/A</td><td rowspan=2 colspan=1>Only 1 port onS32G0</td></tr><tr><td rowspan=1 colspan=1>D-</td><td rowspan=1 colspan=1>CN10-14</td><td rowspan=1 colspan=1>-</td><td rowspan=1 colspan=1>PA11</td><td rowspan=1 colspan=1>N/A</td></tr><tr><td rowspan=1 colspan=1>CC1 DB</td><td rowspan=1 colspan=1>CN10-21(2)</td><td rowspan=1 colspan=1>CN7-10(2)</td><td rowspan=1 colspan=1>PA9</td><td rowspan=1 colspan=1>PD1</td><td rowspan=1 colspan=1></td></tr><tr><td rowspan=1 colspan=1>CC2 DB</td><td rowspan=1 colspan=1>CN10-33(2)</td><td rowspan=1 colspan=1>CN7-11(2)</td><td rowspan=1 colspan=1>PA10</td><td rowspan=1 colspan=1>PD3</td><td rowspan=1 colspan=1></td></tr><tr><td rowspan=1 colspan=1>USART2</td><td rowspan=1 colspan=2>ST-link part(3)</td><td rowspan=1 colspan=2>PA2-PA3</td><td rowspan=1 colspan=1>For traces</td></tr><tr><td rowspan=1 colspan=1>LED</td><td rowspan=1 colspan=2>CN10-11(3)</td><td rowspan=1 colspan=2>PA5</td><td rowspan=1 colspan=1>For debug</td></tr></table>

1 Mandatory Optional For debug purposes

# 14 Recommendations

# 14.1

# ESD/EOS protection devices for USB Type-C®

Dedicated ESD and EOS protection can be used on:

VBus power delivery signals   
D+/D-  
USBLC6-2P6 if RF is close to connector, then ECMF2-40A100N6.   
Tx/Rx SuperSpeed   
HSP051-4xx if RF is close to connector, then ECMF4-40A100N10.   
Common Criteria lines   
ESDA25L if 20 V compliant   
ESDA6V1 if 5 V compliant, otherwise short-to-VBus with voltage higher than 5 V that destroys the line. TCPP series embeds ESD and OVP protection for STM32 (FT I/O).   
SBU lines   
ESDA25L if 20 V compliant   
ESDA6V1if 5 V compliant, then short-to-VBus with voltage higher than 5 V that destroys the line.

For further information, refer to Section 1.2 and to www.st.com (search Type-C protection). For rg evisTVSmust belecaordin heoltage n heB hat can ier hanV):

ESDA7P120-1U1M for 5 V VBUS ESDA13P70-1U1M for 9 V VBUS ESDA15P60-1U1M for 12 V VBUS ESDA17P50-1U1M for 15 V VBUS ESDA25P35-1U1M for 20 V VBUS

For sinking devices, TVS (ESDA25P35-1U1M) and an overvoltage protection (TCPP01-M12 or TCPP03-M20) are recommended to avoid destruction in case of defective adapter sourcing at maximum voltage.

# 14.2 Capacitors on CC lines

The USB PD specification allows CC receiver (cReceiver) capacitance in the range of 200 pF to 600 pF. For noie filterin purposes, an extra 390 F +/ 0% apactance must be ade on each CC lne close he Type-C connector. When a TCPPOx is used, these capacitors must be added between the TCPPOx and the Type-C connector, as close to the Type-C connector as possible.

# 14.3 Capacitors on VBUS line

# 14.3.1

# Sink mode

![](images/fabbb8808a47dbb2c2289e1ec676c8338f6ca2184f9166ac8e8d814ae8cb5aad.jpg)  
Figure 43. Sink mode scheme

# Note:

1. According to the Csnk capacitance value, consider the MOS rise time to comply with the USB inrush current (see Section 14.3.4 How to limit the inrush current in Sink mode). 2. Use Cvbus = 2.2 uF to comply with the cSnkBulk range.

# 14.3.2 SRC mode

![](images/93b725fc0337f76cdad34fa1c296d7ae7046c73f8b9e65bce829887ee54371e8.jpg)  
Figure 44. SRC mode scheme

Note: 1. Use Cvbus = 2.2 μF.

# 14.3.3 DRP mode

![](images/a7eabcb50c40005b5f245491f3869a4c7356f00e677b459d91c0d114b8472fab.jpg)  
Figure 45. DRP mode scheme

# Note:

According to the Csnk capacitance value, the MOS rise time must comply with the USB inrush current (see Section.3.4 How to limit the inrush current in Sink mode). 2. Use Cvbus = 2.2μF.

# 14.3.4

# How to limit the inrush current in Sink mode

Regarding thefunction Enable or he Mos comand, a capacitor g can be added between Gate and Drain to limit the inrush current and OCP. 100pF for each 10µF is recommended (Csnk). See Figure 43. Sink mode scheme and Figure 45. DRP mode scheme, and consult the user manual [12] for more details.

# TCPP01, TCPP02 and TCPP03 Type-C port protection devices

Two Type-C Power Delivery failure modes are identified:

VBUS high voltage short circuit to the CC lines when a unplug is done with a poor mechanical quality connector. Over voltage protection is needed on the CC line. This use case appears only when Power Delivery is used. VBUS line compromised if a defective charger s stuck at a high voltage.Over-voltage protection is needed on the VBuS line. This use case can occur even when Power Delivery is not used.

A dedicated single TCPP01, TCPP02 or TCPP03 chip, can be used for system protection. They provide a costeffective solution to protect ow-voltage MCUs or other controllers performing USB Type-C Power Delivery management:

TCPP01-M12 for power sink protection TCPP02-M18 for power source protection TCPP03-M20 for protection of dual-role power scenarios.

The TCPP01-M12, TCPP02-M18, and TCPP03-M20 provide 20 V short-to-VBUS over-voltage and IEC ESD potecion nC es, as well  programable overvoltage protection wih n  at rive orhe VBUS lin They also integrate dead battery management, and can be completely turned off for battery-powered devices. A fault report is also generated.

The TCPP02-M18 and TCPP03-M20 also integrate a dual VBUS gate driver, and an I2C communication interface for dual-port applications.

TVS is still required on VBUS (ESDA25P35-1U1M), and then only the maximum voltage is considered.   
More details are given in the TCPP01, TCPP02 and TCPP03 data sheets [3], [4],and [5].

# 14.4.1

# SNK or sink power applications

The ollg fguhows  kpatiawigl  powerom heUSB Type-coor VBUS .

![](images/a63a1668cd753147c108a8a352c38ec949f701072f068ac5ed98a81f3bdcb3d2.jpg)  
Figure 46. Entirely VBUS-powered sink

FLT (FAULT) is an open-drain output pin.   
DB/ is a pull-down TCPP input. Connect it to 3.3 V if not managed by the MCU software. FLT (FAULT) is an open-drain output pin.   
DB/ is a pull-down TCPP input. Connect it to 3.3 V if not managed by the MCU software. FLT (FAULT) is an open-drain output pin, to leave open if not connected.   
When GPIO1 is low, TCPP01-M12 is OFF with zero current consumption.   
When GPIO1 is low, TCPP01-M12 is ON with ADC1 or ADC2 checking the source capability. In dead battery condition, the following sequence applies:   
1. TCPP01-M12 presents a DB clamp (1.1 V) on CC1 and CC2 lines.   
2. The source detects the clamp presence and applies 5 V on VBUS.   
3. N-MOSFET T1 is normally ON and the power management block is supplied with 5 V.   
4. The MCU wakes-up, and applies 3.3 V on GPIO1 to wake up TCPP01-M12.   
5. TCPP01-M12 releases the clamp on the CC1 and CC2 lines so that ADC1 or ADC2 can sense the SOURCE pin capability with the voltage across R5 or R6.

![](images/43c3434534e32e8c24d43ab1e30f16a024456cededa910da6d3c5fd4d8440568.jpg)  
Figure 47. Sink application with battery (PD3.0)

![](images/5011859ec2e9d952fba4d2239f2e2e4358704b857314477862ed9986c94674ef.jpg)  
Figure 48. 15 W sink application with battery

# 14.4.2

# DRP or dual-role power applications

Figure 49 shows a DRP application using dedicated power management.

![](images/d3ec7a6fa86ac0515121dbe73ed351c07bc66682168ee6c170fc5734549fd5fc.jpg)  
Figure 49. Battery DRP application example

1. I2C_ADD can be connected to GND or VddIO 3. VDDIO ring: (1.8 V +/- 5%, 3.3 V +/ 10%)   
2. VCC IO ring: (3.3 V +/- 10%, 5 V +/- 10%) 4. \* = Not mandatory

# Note:

If the ENABLE pin of TCPP(02/03) is used for power on reset, then the rise time must be shorter than 50 microS. See the document [12] for more details.

# 14.4.3

# SRC or source power applications

Figure 50 shows a SRC application using dedicated power management.

![](images/9d608b354a23b5b3517c1e7562150cad34ed7d6fb03d2ddd3946e70cface6c4e.jpg)  
Figure 50. SRC application using dedicated power management

1. I2C_ADD (I2C address): can be connected to GND or VddIO 3. VDDIO ring: (1.8 V +/- 5%, 3.3 V +/- 10%)   
2. VCC IO ring: (3.3 V +/- 10%, 5 V +/- 10%) 4. \* = Not mandatory

# Note:

If the ENABLE pin of TCPP(02/03) is used for power on reset, then the rise time must be shorter than 50 microS. See the document [13] for more details.

# 14.4.4

# Handling dead battery condition

# TCPP01

For the TCPP01 device, the DB/ (dead battery resistor management) pin is a pulled-down active-low TCPP01 input. The DB/ pin can either be connected to VCC or driven by an MCU GPIO.

As ongsheDBu is ow  r eennd l bui kΩ pu resistor), the dead-battery resistors are connected and CC switches are opened (OFF state).

When he DB/ pin is tid to VCC, the DB resistors on he CC pins ae disconeced and CCswitches are close (ON state).

DB/ usage (sink application):

After system power-up, the DB/ pin must be kept low, which activates DB Rd of TCPP01.   
Once the DB Rd is enabled on STM32 CC pins, the DB/ pin must be set high.

# TCPP03

Thedead batterymanagement is integrated in the hip. See he Power Mode chapter in theTP3 dat sheet [5].

# 14.5

# EMC considerations in USB HS cases

To decrease noise on VBUS due to D+/D- lines activities, a 100 pF capacitor can be added between VBUS and GND close to the Type-C connector.

# 14.6 VBUS inrush current considerations in Sink cases

To lmit the inrush current n VBU, a aditioal 00 F apacitor or evey aditional 0F decpli ccoreition  eenragae powwi to the TCPP01 gate pin.

# VBUS overshoot considerations in Sink cases

To limit overshoot on VBUS, a damping filter can be added between VBUS and GND close to the Type-C connector.

As an example: a 1 µF capacitor in parallel with a 4.7 μF capacitor in sers with 1 Ω reduces the overshoot amplitude.

# 14.8 VBUS discharge

O Sourcowrapliatn,ext iharge cuity may e gur Sourcarhiue. Th VBUS ischarge eature s integrated in heTCPP2 an TCPP. See theirrespectiv datasheets ], [5], for further information.

# 14.9 VBUS sensing detection

See chapter VBUS sensing detection in the Introduction to USB hardware and PCB guidelines using STM32 MCUs application note (AN4879).

# 15 Additional information

The USB Power Delivery protocol over CC lines is defined as an extension to both USB2.0 and USB3.1, and only applies to the use of the Type-C connector.

# Protocol purpose

The purpose of this protocol is tonegotiate the power capabilitis and power requirementsof the devices coe throgh a USB Type® cable, iorder  safely deliver powerrom he powersourc devic  e power sink device.

The protocol combined with the Type-C connectionllows the increasef the maximum power delivery o100 W (5 A at 20 V).

The Power Delivery role sourceor sink) isdissociated from the upstream/downstream-facing portroles. For ee,  USB device/ubupstream-acig port) can eliverpower he USB host downtream-facin ort). DFP) can be swapped over the Type-C connection.

# New Type-C cable additional pins

The new Type-C cable has two additional wires, CC1 and CC2, for configuration control. Oalle n ur   uppy  eteory. I the signalling function of the pin is not available.

# Power Delivery port - pull-up/down resistors

Adevice acting as a Type-C port supporting Power Delivery protocol must pull the CC line(s) up ordown:

r source: pull u wit  equal o f tree speci valus,dependig n he powe equents of the sink   
Power sink: pull down with Rd equal to a specified value   
Dual-role power port: as power source or power sink, depending on its actual role.

# System attach

Once a debounce period has elapsed, the system becomes attached:

• On CC, Power Delivery messaging can be used for communication over CC lines

power capabilities, for example beyond 5 V/3 A   
power-role swaps   
data role swaps (similar to HNP in OTG)   
VCONN swap

On VCONN: on seeing an Ra resistor a 5 V supply must be provided

# Single Type-C port pins

• Source/sink/DRP port cases: Two CC pins (CC1/CC2) allow for unknown orientation of the cable   
. Cable and accessory cases: Orientation is pre-determined A single CC pin is needed

# Dead battery support

Dead battery nalling capability a Type power k translates nto eposinga pull-own resistr a g  at with no battery.

Type-C power source (such as a wall charger) must not provide dead battery signalling.

# Revision history

<table><tr><td colspan="3">Table 17. Document revision history</td></tr><tr><td>Date</td><td>Version</td><td>Changes</td></tr><tr><td>24-Apr-2019</td><td>1</td><td>Initial release.</td></tr><tr><td rowspan="12">26-Sep-2019 01-Sep-2020</td><td rowspan="10"></td><td>Updated:</td></tr><tr><td>Section 1.2 Reference documents</td><td>Section Introduction</td></tr><tr><td></td><td></td></tr><tr><td>Table 8 Fixed and programmable power suply current and cabling requirements</td><td></td></tr><tr><td></td><td>Figure 25. Source architecture</td></tr><tr><td></td><td>Figure 29. DRP with FRS VBUS = 5 V / 9 V / 15 V connections</td></tr><tr><td>Figure 38. Applying Vconn on CC lines</td><td></td></tr><tr><td></td><td>Figure 46. Entirely VBUS-powered sink</td></tr><tr><td></td><td>Figure 47. Sink application with battery (PD3.0)</td></tr><tr><td>Figure 48. 15 W sink application with battery</td><td>Section 14.4.1 SNK or sink power applications</td></tr><tr><td rowspan="8"></td><td>Added:</td></tr><tr><td></td></tr><tr><td>Figure 8. USB Type-C Power Delivery block diagram and Figure 9. STM32G0 Discovery kit USB Type-C analyser</td></tr><tr><td>New Figure 27. DRP connections</td></tr><tr><td>New Figure 1</td></tr><tr><td>Removed Source and Source/Sink mode description subsections from Section 14.4 TCPP01, TCPP02 and TCPP03 Type-C port protection devices.</td></tr><tr><td>Updated:</td></tr><tr><td>Section Introduction</td></tr><tr><td rowspan="9">3 4</td><td rowspan="9">Section 9 Product offer</td><td></td></tr><tr><td>Section 1.2 Reference documents</td></tr><tr><td>Section 5 Power profiles</td></tr><tr><td></td></tr><tr><td>Section 11 Type-C with Power Delivery using integrated UCPD</td></tr><tr><td>peripheral, Section 11.3 Hardware overview Section 12 Type-C with Power Delivery using a general-purpose</td></tr><tr><td>peripheral, Section 12.2 Hardware overview</td></tr><tr><td></td></tr><tr><td></td></tr><tr><td rowspan="11">14-Sep-2021</td><td></td><td>Section 13 Dedicated architecture proposals and solutions</td></tr><tr><td>Updated:</td><td>Section 14 Recommendations</td></tr><tr><td></td><td></td></tr><tr><td></td><td>Section 1.2 Reference documents</td></tr><tr><td>Table 14. Source features</td><td></td></tr><tr><td></td><td>Section 13.5 Monitoring VBUS voltage and current and Figure 41</td></tr><tr><td>devices (and rearranged subsequent subsections).</td><td>Section 14.4 TCPP01, TCPP02 and TCPP03 Type-C port protection</td></tr><tr><td>Added:</td><td></td></tr><tr><td>Section 13.6 Dual-role power port</td><td></td></tr><tr><td></td><td>Section 14.4.2 DRP or dual-role power applications</td></tr><tr><td></td><td>Section 14.6 VBUS inrush current considerations in Sink cases</td></tr><tr><td></td><td></td><td>Section 14.7 VBUS overshoot considerations in Sink cases</td></tr><tr><td></td><td></td><td>Section 14.8 VBUS discharge</td></tr><tr><td></td><td>Updated:</td><td></td></tr><tr><td rowspan="2">12-Oct-2021</td><td>5</td><td colspan="2">Section Introduction</td></tr><tr><td></td><td colspan="2">Updated:</td></tr><tr><td rowspan="2">16-Mar-2022</td><td>6</td><td colspan="2"></td></tr><tr><td rowspan="2"></td><td rowspan="2"></td><td colspan="2"></td></tr><tr><td colspan="2">Figure 48. 15 W sink application with battery</td></tr></table>

<table><tr><td rowspan=1 colspan=1>Date</td><td rowspan=1 colspan=1>Version</td><td rowspan=1 colspan=1>Changes</td></tr><tr><td rowspan=1 colspan=1></td><td rowspan=1 colspan=1></td><td rowspan=1 colspan=1>Figure 49. Battery DRP application exampleFigure 50. SRC application using dedicated power management</td></tr><tr><td rowspan=1 colspan=1>23-Jun-2023</td><td rowspan=1 colspan=1>7</td><td rowspan=1 colspan=1>Added:•    Section 11.2 STM32 MPU software overviewSection 14.3 Capacitors on VBUS lineVBUS sensing detectionUpdated:Section IntroductionSection 1.2 Reference documentsSection 11.1 STM32 MCU software overview</td></tr></table>

# Contents

# General information

1.1 Acronyms and abbreviations 2   
1.2 Reference documents. 3

# USB Type-C in a nutshell 4

2.1 USB Type-C® vocabulary.. 5   
2.2 Minimum mandatory feature set 5

# Connector pin mapping. 6

3.1 VBUS power options.

# CC pins.. 8

4.1 Plug orientation/cable twist detection . 8   
4.2 Power capability detection and usage 10

# Power profiles 11

# USB Power Delivery 2.0. 12

6.1 Power Delivery signaling 12

6.1.1 Packet structure 12   
6.1.2 K-codes. 12

6.2 Negotiating power. 13

# USB Power Delivery 3.0. 14

# Alternate modes 15

8.1 Alternate pin reassignments 15   
8.2 Billboard. 16

# Product offer 17

# 10 Type-C with no Power Delivery . . 19

10.1 STM32 USB2.0-only device conversion for USB Type-C platforms . 19   
10.2 STM32 USB2.0 host conversion for USB Type-C platforms . 19   
10.3 STM32 legacy USB2.0 OTG conversion for USB Type-C platforms. 20

# Type-C with Power Delivery using integrated UCPD peripheral .22

11.1 STM32 MCU software overview 22   
11.2 STM32 MPU software overview 23

# 11.3 Hardware overview 24

11.3.1 DBCC1 and DBCC2 lines . 25   
11.3.2 Sink port . .30   
11.3.3 Source port . 35   
11.3.4 Dual-role power port . 39   
11.3.5 Dual-role power port with FRS 43

# 2 Type-C with Power Delivery using a general-purpose peripheral. .46

12.1 Software overview. 46

12.2 Hardware overview 46

12.2.1 Sink port using TCPM/TCPC interface 47   
12.2.2 Source port using TCPM/TCPC interface 48   
12.2.3 Dual-role power port using TCPM/TCPC interface 49

# 3 Dedicated architecture proposals and solutions. 50

13.1 Sourcing power to VBUS 50   
13.2 DC/DC output control with GPIOs. 51   
13.3 Applying VcoNN on CC lines . .52   
13.3.1 Time line . 53   
13.4 FRS signalling . 54   
13.5 Monitoring VBUS voltage and current 55   
13.6 Dual-role power port. 56

# 4 Recommendations. 58

14.1 ESD/EOS protection devices for USB Type-C® 58

14.2 Capacitors on CC lines. 58

14.3 Capacitors on VBUS line 59

14.3.1 Sink mode. 59   
14.3.2 SRC mode 60   
14.3.3 DRP mode 61   
14.3.4 How to limit the inrush current in Sink mode 61

14.4 TCPP01, TCPP02 and TCPP03 Type-C port protection devices 62

14.4.1 SNK or sink power applications. 62

14.4.2 DRP or dual-role power applications . 65

14.4.3 SRC or source power applications 66   
14.4.4 Handling dead battery condition 66   
14.5 EMC considerations in USB HS cases. .66   
14.6 Vbus Inrush current in Sink cases consideration. .67   
14.7 Vbus overshoot considerations in Sink cases . .67   
14.8 VBUS discharge .67   
14.9 VBUS sensing detection. .67

15 Additional information .68

Revision history 69

# List of tables

Table 1. STMicroelectronics ecosystem documents 3   
Table 2. USB Type-C receptacle pin descriptions 6   
Table 3. Power supply options 7   
Table 4. Attached device states - source perspective 8   
Table 5. DFP CC termination (Rp) requirements. 10   
Table 6. UFP CC termination (Rd) requirements 10   
Table 7. Voltage on sink CC pins (multiple source current advertisements) 10   
Table 8. Fixed and programmable power supply current and cabling requirements . 11   
Table 9. USB Type-C sink behavior on CC lines. 25   
Table 10. Non-protected sink - sequence of exiting Dead battery mode. 26   
Table 11. Protected sink application - sequence of exiting Dead battery mode. 28   
Table 12. Summary of principal Type-C application topologies 30   
Table 13. Sink features 31   
Table 14. Source features. 36   
Table 15. Dual-role power port features 40   
Table 16. STM32G0 resources 57   
Table 17. Document revision history . 69

# List of figures

Figure 1. USB connectors 4   
Figure 2. Receptacle pinout . 6   
Figure 3. Pull up/down CC detection. 9   
Figure 4. Power profile 11   
Figure 5. SOP\* signaling . 12   
Figure 6. Pins available for reconfiguration over the full featured Cable 15   
Figure 7. Pavailableoguration oc plito 16   
Figure 8. USB Type-C Power Delivery block diagram 17   
Figure 9. STM32G0 Discovery kit USB Type-C analyser 17   
Figure 10. Legacy device using USB Type-C receptacle 19   
Figure 11. Legacy host using USB Type-C receptacle. 20   
Figure 12. Legacy OTG using USB Type-C receptacle 21   
Figure 13. USB Power Delivery stack architecture 22   
Figure 14. STM32 MPU software overview 23   
Figure 15. Device pinout example 24   
Figure 16. Non-protected sink application supporting Dead battery feature 26   
Figure 17. Non-protected sink not supporting Dead battery feature . . 27   
Figure 18. Protected sink application supporting Dead battery feature. 28   
Figure 19. Protected sink application not supporting Dead battery feature - activation through supply 29   
Figure 20. Protected sinkapplication ot supporting Dead battery fature activation through dedicatedu. 29   
Figure 21. Unprotected VBUS-powered (Dead battery) sink connections. 32   
Figure 22. VBUS-powered sink timeline 33   
Figure 23. SNK external power connections 34   
Figure 24. Sink external power time line 35   
Figure 25. Source architecture. . 37   
Figure 26. SRC (source) mode power timings 38   
Figure 27. DRP connections 41   
Figure 28. DRP with FRS mode time line example 42   
Figure 29. DRP with FRS VBUS = 5 V / 9 V / 15 V connections 43   
Figure 30. DRP with FRS - time line example. 44   
Figure 31. Hardware view for Type-C Power Delivery with a general-purpose peripheral 46   
Figure 32. Sink port using TCPM/TCPC interface. 47   
Figure 33. Source mode using TCPM/TCPC interface. 48   
Figure 34. Dual-role power port using TCPM/TCPC interface. 49   
Figure 35. Sourcing power to VBUS 50   
Figure 36. Setting VRef with a switched resistor bridge 51   
Figure 37. Setting VRef with a PWM GPIO. 51   
Figure 38. Applying Vconn on CC lines. 52   
Figure 39. Applying Vconn - time line example 53   
Figure 40. Fast role-swap DRP mode circuit 54   
Figure 41. VBUS voltage and current monitoring circuit. 55   
Figure 42. STM32G0 pin/resource assignments . 56   
Figure 43. Sink mode scheme 59   
Figure 44. SRC mode scheme. 60   
Figure 45. DRP mode scheme. 61   
Figure 46. Entirely VBUS-powered sink. 62   
Figure 47. Sink application with battery (PD3.0) 63   
Figure 48. 15 W sink application with battery 63   
Figure 49. Battery DRP application example 65   
Figure 50. SRC application using dedicated power management 66

# IMPORTANT NOTICE  READ CAREFULLY

t old purant s dits  lo.

purchasers' products.

No license, express or implied, to any intellectual property right is granted by ST herein.

are the property of their respective owners.

I

© 2023 STMicroelectronics - All rights reserved