# Introduction to using the hardware real-time clock (RTC) and the tamper management unit (TAMP) with STM32 MCUs

# Introduction

agendas, and many other devices.

alarm, wakeup, timestamp, tamper detection, or calibration.

A application note.

detection and internal tamper.

T - .

In this document, the ST32 microcontroller terminology applies to the products listed in the table below.

Table 1. Applicable products   

<table><tr><td>Type</td><td>Products</td></tr><tr><td>Expansion Package</td><td>X-CUBE-RTC</td></tr><tr><td>Microcontrollers</td><td>STM32C0 series, STM32F0 series, STM32F2 series, STM32F3 series, STM32F4 series, STM32F7 series, STM32G0 series, STM32G4 series, STM32H5 series, STM32H7 series, STM32L0 series, STM32L1 series, STM32L4 series, STM32L4+ series, STM32L5 series, STM32N6 series, STM32U0 series, STM32U3 series, STM32U5 series, STM32WB series, STM32WB0 series, STM32WBA series, STM32WL series</td></tr></table>

# Overview of the STM32 MCUs advanced RTC

# Note:

The RTC is embedded in STM32 Arm® Cortex®-based MCUs.   
Arm is a registered trademark of Arm Limited (or its subsidiaries) in the US and/or elsewhere.

arm

Tpviefuleature calendarala, pedic wakeupigalcalationnroin, timestamp, and advanced tamper detection.

The RTC features and their implementation can be significantly different (regarding the registers map for epledepending on e productTwoRTC types C andRT3 aistinguished and characterize table below. These types affect the information presented in the rest of this application note.

Table 2. RTC/TAMP types   

<table><tr><td colspan="3" rowspan="2">FeaturesRTC clock source (LSE, LSI, HSE with prescaler)</td><td colspan="1" rowspan="1">RTC2</td><td colspan="4" rowspan="1">RTC3</td></tr><tr><td colspan="1" rowspan="1">X</td><td colspan="4" rowspan="1">X</td></tr><tr><td colspan="3" rowspan="1">Binary mode</td><td colspan="1" rowspan="1">-</td><td colspan="4" rowspan="1">X</td></tr><tr><td colspan="3" rowspan="1">Mixed mode (BCD and binary)</td><td colspan="1" rowspan="1">-</td><td colspan="4" rowspan="1">X</td></tr><tr><td colspan="1" rowspan="2">Prescalers</td><td colspan="2" rowspan="1">Asynchronous</td><td colspan="1" rowspan="1">X</td><td colspan="4" rowspan="1">X</td></tr><tr><td colspan="3" rowspan="1">Synchronous</td><td colspan="1" rowspan="1">X</td><td colspan="1" rowspan="1">X</td></tr><tr><td colspan="1" rowspan="7">Calendar</td><td colspan="1" rowspan="3">Time</td><td colspan="1" rowspan="1">12 h/24 h format</td><td colspan="1" rowspan="1">X</td><td colspan="4" rowspan="1">X</td></tr><tr><td colspan="1" rowspan="1">Hour, minute, second</td><td colspan="1" rowspan="1">X</td><td colspan="4" rowspan="1">X</td></tr><tr><td colspan="1" rowspan="1">Subsecond</td><td colspan="1" rowspan="1">X</td><td colspan="4" rowspan="1">X</td></tr><tr><td colspan="3" rowspan="1">Date</td><td colspan="1" rowspan="1">X</td><td colspan="1" rowspan="1">X</td></tr><tr><td colspan="3" rowspan="1">Daylight operation</td><td colspan="1" rowspan="1">X</td><td colspan="1" rowspan="1">X</td></tr><tr><td colspan="3" rowspan="1">Bypass the shadow registers</td><td colspan="1" rowspan="1">X</td><td colspan="1" rowspan="1">X</td></tr><tr><td colspan="3" rowspan="1">Power optimization mode</td><td colspan="1" rowspan="1">-</td><td colspan="1" rowspan="1">X</td></tr><tr><td colspan="1" rowspan="7">Alarm</td><td colspan="1" rowspan="2">Alarmsavailable</td><td colspan="1" rowspan="1">Alarm A</td><td colspan="1" rowspan="1">X</td><td colspan="4" rowspan="1">X</td></tr><tr><td colspan="1" rowspan="1">Alarm B</td><td colspan="1" rowspan="1">X</td><td colspan="4" rowspan="1">X</td></tr><tr><td colspan="1" rowspan="3">Time</td><td colspan="1" rowspan="1">12 h/24 h format</td><td colspan="1" rowspan="1">X</td><td colspan="4" rowspan="1">X</td></tr><tr><td colspan="1" rowspan="1">Hour, minutes, seconds</td><td colspan="1" rowspan="1">X</td><td colspan="4" rowspan="1">X</td></tr><tr><td colspan="1" rowspan="1">Subseconds</td><td colspan="1" rowspan="1">X</td><td colspan="4" rowspan="1">X</td></tr><tr><td colspan="3" rowspan="1">Date or week day</td><td colspan="1" rowspan="1">X</td><td colspan="1" rowspan="1">X</td></tr><tr><td colspan="3" rowspan="1">Binary mode alarm</td><td colspan="1" rowspan="1">-</td><td colspan="1" rowspan="1">×</td></tr><tr><td colspan="1" rowspan="9">Tamper detection</td><td colspan="1" rowspan="3">Tampere fffects</td><td colspan="1" rowspan="1">Backup registers erase()</td><td colspan="1" rowspan="1">X</td><td colspan="4" rowspan="1">X</td></tr><tr><td colspan="1" rowspan="1">Interruption</td><td colspan="1" rowspan="1">X</td><td colspan="4" rowspan="1">X</td></tr><tr><td colspan="1" rowspan="1">Trigger for low-power timer</td><td colspan="1" rowspan="1">X</td><td colspan="4" rowspan="1">X</td></tr><tr><td colspan="3" rowspan="1">Configurable edge detection</td><td colspan="1" rowspan="1">X</td><td colspan="1" rowspan="1">X</td></tr><tr><td colspan="3" rowspan="1">Configurable level detection (filtering, sampling and prechargeconfiguration, internal pull-up</td><td colspan="1" rowspan="1">X</td><td colspan="1" rowspan="1">X</td></tr><tr><td colspan="3" rowspan="1">Internal tamper events</td><td colspan="1" rowspan="1">-</td><td colspan="1" rowspan="1">X</td></tr><tr><td colspan="3" rowspan="1">External tamper inputs</td><td colspan="1" rowspan="1">X</td><td colspan="1" rowspan="1">X</td></tr><tr><td colspan="3" rowspan="1">VBAT mode pins</td><td colspan="1" rowspan="1">X</td><td colspan="1" rowspan="1">X</td></tr><tr><td colspan="3" rowspan="1">NOERASE mode</td><td colspan="1" rowspan="1">X</td><td colspan="1" rowspan="1">X</td></tr><tr><td colspan="3" rowspan="8">FeaturesIndependent watchdog linked to an internal tamper forpotential detection timeoutActive tamperTamper detection            Monotonic counterSAES key storageSecure protection modesPrivileged protection mode</td><td></td><td></td></tr><tr><td colspan="1" rowspan="1">RTC2</td><td colspan="1" rowspan="1">RTC3</td></tr><tr><td colspan="1" rowspan="6">Tamper detection</td><td colspan="2" rowspan="1">Independent watchdog linked to an internal tamper forpotential detection timeout</td><td colspan="1" rowspan="1"></td><td colspan="1" rowspan="1">X</td></tr><tr><td colspan="2" rowspan="1">Active tamper</td><td colspan="1" rowspan="1"></td><td colspan="1" rowspan="1">X</td></tr><tr><td colspan="2" rowspan="1">Monotonic counter</td><td colspan="1" rowspan="1"></td><td colspan="1" rowspan="1">X</td></tr><tr><td colspan="2" rowspan="1">SAES key storage</td><td colspan="1" rowspan="1"></td><td colspan="1" rowspan="1">X</td></tr><tr><td colspan="2" rowspan="1">Secure protection modes</td><td colspan="1" rowspan="1"></td><td colspan="1" rowspan="1">X</td></tr><tr><td colspan="2" rowspan="1">Privileged protection mode</td><td colspan="1" rowspan="1"></td><td colspan="1" rowspan="1">X</td></tr><tr><td colspan="1" rowspan="6">Timestamp</td><td colspan="2" rowspan="1">Configurable input mapping</td><td colspan="1" rowspan="1">X</td><td colspan="1" rowspan="1">X</td></tr><tr><td colspan="1" rowspan="2">Time</td><td colspan="1" rowspan="1">Hour, minute, second</td><td colspan="1" rowspan="1">X</td><td colspan="1" rowspan="1">X</td></tr><tr><td colspan="1" rowspan="1">Subsecond</td><td colspan="1" rowspan="1">X</td><td colspan="1" rowspan="1">X</td></tr><tr><td colspan="2" rowspan="1">Date (day, month)</td><td colspan="1" rowspan="1">X</td><td colspan="1" rowspan="1">X</td></tr><tr><td colspan="2" rowspan="1">Timestamp on tamper detection event</td><td colspan="1" rowspan="1">X</td><td colspan="1" rowspan="1">X</td></tr><tr><td colspan="2" rowspan="1">Timestamp on switch to VBAT mode</td><td colspan="1" rowspan="1">X</td><td colspan="1" rowspan="1">X</td></tr><tr><td colspan="1" rowspan="2">Wakeup unit</td><td colspan="2" rowspan="1">Clock source available</td><td colspan="1" rowspan="1">X</td><td colspan="1" rowspan="1">X</td></tr><tr><td colspan="2" rowspan="1">Hardware automatic flag clearance</td><td colspan="1" rowspan="1">X</td><td colspan="1" rowspan="1">X</td></tr><tr><td colspan="1" rowspan="5">RTC outputs</td><td colspan="1" rowspan="3">TAMPALRM</td><td colspan="1" rowspan="1">Alarm event</td><td colspan="1" rowspan="1">X</td><td colspan="1" rowspan="1">X</td></tr><tr><td colspan="1" rowspan="1">Wakeup event</td><td colspan="1" rowspan="1">X</td><td colspan="1" rowspan="1">X</td></tr><tr><td colspan="1" rowspan="1">Tamper event</td><td colspan="1" rowspan="1">-</td><td colspan="1" rowspan="1">X</td></tr><tr><td colspan="1" rowspan="2">CALIB</td><td colspan="1" rowspan="1">512 Hz</td><td colspan="1" rowspan="1">X</td><td colspan="1" rowspan="1">X</td></tr><tr><td colspan="1" rowspan="1">1 Hz</td><td colspan="1" rowspan="1">X</td><td colspan="1" rowspan="1">X</td></tr><tr><td colspan="1" rowspan="2">Smooth digital calibration</td><td colspan="2" rowspan="1">Smooth calibration</td><td colspan="1" rowspan="1">X</td><td colspan="1" rowspan="1">X</td></tr><tr><td colspan="2" rowspan="1">Power optimization mode</td><td colspan="1" rowspan="1">-</td><td colspan="1" rowspan="1">X</td></tr><tr><td colspan="3" rowspan="1">RTC synchronization</td><td colspan="1" rowspan="1">X</td><td colspan="1" rowspan="1">X</td></tr><tr><td colspan="3" rowspan="1">Reference clock detection</td><td colspan="1" rowspan="1">X</td><td colspan="1" rowspan="1">X</td></tr><tr><td colspan="1" rowspan="2">Backup registers</td><td colspan="2" rowspan="1">Reset on a tamper detection</td><td colspan="1" rowspan="1">X</td><td colspan="1" rowspan="1">X</td></tr><tr><td colspan="2" rowspan="1">Reset when Flash memory readout protection is disabled</td><td colspan="1" rowspan="1">X</td><td colspan="1" rowspan="1">X</td></tr><tr><td colspan="3" rowspan="1">RTC secure protection mode</td><td colspan="1" rowspan="1">-</td><td colspan="1" rowspan="1">X</td></tr><tr><td colspan="3" rowspan="1">RTC privileged protection mode</td><td colspan="1" rowspan="1">-</td><td colspan="1" rowspan="1">X</td></tr></table>

Depending on devices, other resources can also be erased.

The RTC acts as an independent binary-coded decimal (BCD) timer/counter. For he RTC3 type, a binary and a mixed (both binary and BCD) modes are available.

Aavble y uotp  Tb Ta more details).

The table below specifies which RTC type is implemented on which product.

Table 3. RTC type on STM32 MCUs   

<table><tr><td>RTC type</td><td>STM32 MCUs</td></tr><tr><td>RTC2</td><td>STM32F0 series, STM32F2 series, STM32F3 series, STM32F4 series, STM32F7 series, STM32H72/H73/H74/H75xxx, STM32L0 series, STM32L1 series, STM32L43/L44/L45/46/47/48xxx, STM32L4R5/Q5 line, STM32L4R7/S7 line, STM32L4R9/S9 line, STM32WB series, STM32WB0 series</td></tr><tr><td>RTC3</td><td>STM32C0 series, STM32G0 series, STM32G4 series, STM32H5 series, STM32H7A3/7B3 line, STM32H7Rx/7Sx line, STM32L41/L42xxx, STM32L4P5/Q5 line, STM32L5 series, STM32N6 series, STM32U0 series, STM32U3 series, STM32U5 series, STM32WL series, STM32WBA series</td></tr></table>

# 2 Advanced RTC features

The following tables summarize the RTC features available on each STM32 MCU.

Table 4. Advanced features for RTC2 type   

<table><tr><td colspan="3" rowspan="2">Features</td><td colspan="1" rowspan="2">2</td><td colspan="1" rowspan="2">2</td><td colspan="1" rowspan="2">M</td><td colspan="1" rowspan="2">20</td><td colspan="1" rowspan="2">2</td><td colspan="1" rowspan="2">0</td><td colspan="2" rowspan="1">STM32L1</td><td colspan="1" rowspan="2">((z)+32)</td><td colspan="1" rowspan="2">202</td><td colspan="1" rowspan="2">20</td><td colspan="1" rowspan="2">20</td></tr><tr><td colspan="1" rowspan="1">20</td><td colspan="1" rowspan="1">u</td></tr><tr><td colspan="3" rowspan="1">RTC clock source (LSE, LSI, HSE withprescaler</td><td colspan="1" rowspan="1">X</td><td colspan="1" rowspan="1">X</td><td colspan="1" rowspan="1">X</td><td colspan="1" rowspan="1">X</td><td colspan="1" rowspan="1">X</td><td colspan="1" rowspan="1">X</td><td colspan="1" rowspan="1">X</td><td colspan="1" rowspan="1">X</td><td colspan="1" rowspan="1">X</td><td colspan="1" rowspan="1">X</td><td colspan="1" rowspan="1">X</td><td colspan="1" rowspan="1">X</td></tr><tr><td colspan="1" rowspan="2">Pejeer</td><td colspan="2" rowspan="1">Asynchronous (number of bits)</td><td colspan="1" rowspan="1">X(7)</td><td colspan="1" rowspan="1">×(7)</td><td colspan="1" rowspan="1">X(7)</td><td colspan="1" rowspan="1">X(7)</td><td colspan="1" rowspan="1">X(7)</td><td colspan="1" rowspan="1">X(7)</td><td colspan="1" rowspan="1">×(7)</td><td colspan="1" rowspan="1">X(7)</td><td colspan="1" rowspan="1">×(7)</td><td colspan="1" rowspan="1">X(7)</td><td colspan="1" rowspan="1">X(7)</td><td colspan="1" rowspan="1">X(7)</td></tr><tr><td colspan="2" rowspan="1">Synchronous (number of bts)</td><td colspan="1" rowspan="1">X(15)</td><td colspan="1" rowspan="1">X(13)</td><td colspan="1" rowspan="1">X(15)</td><td colspan="1" rowspan="1">X(15)</td><td colspan="1" rowspan="1">X(15)</td><td colspan="1" rowspan="1">X(15)</td><td colspan="1" rowspan="1">×(15)</td><td colspan="1" rowspan="1">X(13)</td><td colspan="1" rowspan="1">X(15)</td><td colspan="1" rowspan="1">x(15)</td><td colspan="1" rowspan="1">X(15)</td><td colspan="1" rowspan="1">X (15)</td></tr><tr><td colspan="1" rowspan="7">20</td><td colspan="1" rowspan="3">Time</td><td colspan="1" rowspan="1">12 h/24 h format</td><td colspan="1" rowspan="1">×</td><td colspan="1" rowspan="1">×</td><td colspan="1" rowspan="1">×</td><td colspan="1" rowspan="1">X</td><td colspan="1" rowspan="1">X</td><td colspan="1" rowspan="1">×</td><td colspan="1" rowspan="1">×</td><td colspan="1" rowspan="1">×</td><td colspan="1" rowspan="1">×</td><td colspan="1" rowspan="1">×</td><td colspan="1" rowspan="1">X</td><td colspan="1" rowspan="1">×</td></tr><tr><td colspan="1" rowspan="1">Hour, minute,second</td><td colspan="1" rowspan="1">X</td><td colspan="1" rowspan="1">X</td><td colspan="1" rowspan="1">X</td><td colspan="1" rowspan="1">X</td><td colspan="1" rowspan="1">X</td><td colspan="1" rowspan="1">X</td><td colspan="1" rowspan="1">X</td><td colspan="1" rowspan="1">X</td><td colspan="1" rowspan="1">X</td><td colspan="1" rowspan="1">X</td><td colspan="1" rowspan="1">X</td><td colspan="1" rowspan="1">X</td></tr><tr><td colspan="1" rowspan="1">Subsecond</td><td colspan="1" rowspan="1">X</td><td colspan="1" rowspan="1">N/A</td><td colspan="1" rowspan="1">×</td><td colspan="1" rowspan="1">×</td><td colspan="1" rowspan="1">X</td><td colspan="1" rowspan="1">×</td><td colspan="1" rowspan="1">×</td><td colspan="1" rowspan="1">N/A</td><td colspan="1" rowspan="1">×</td><td colspan="1" rowspan="1">×</td><td colspan="1" rowspan="1">X</td><td colspan="1" rowspan="1">×</td></tr><tr><td colspan="2" rowspan="1">Date</td><td colspan="1" rowspan="1">X</td><td colspan="1" rowspan="1">×</td><td colspan="1" rowspan="1">×</td><td colspan="1" rowspan="1">X</td><td colspan="1" rowspan="1">X</td><td colspan="1" rowspan="1">×</td><td colspan="1" rowspan="1">×</td><td colspan="1" rowspan="1">X</td><td colspan="1" rowspan="1">X</td><td colspan="1" rowspan="1">X</td><td colspan="1" rowspan="1">X</td><td colspan="1" rowspan="1">×</td></tr><tr><td colspan="2" rowspan="1">Daylight operation</td><td colspan="1" rowspan="1">×</td><td colspan="1" rowspan="1">×</td><td colspan="1" rowspan="1">×</td><td colspan="1" rowspan="1">X</td><td colspan="1" rowspan="1">X</td><td colspan="1" rowspan="1">X</td><td colspan="1" rowspan="1">×</td><td colspan="1" rowspan="1">X</td><td colspan="1" rowspan="1">X</td><td colspan="1" rowspan="1">×</td><td colspan="1" rowspan="1">X</td><td colspan="1" rowspan="1">×</td></tr><tr><td colspan="2" rowspan="1">Bypass shadow registers</td><td colspan="1" rowspan="1">X</td><td colspan="1" rowspan="1">N/A</td><td colspan="1" rowspan="1">X</td><td colspan="1" rowspan="1">X</td><td colspan="1" rowspan="1">X</td><td colspan="1" rowspan="1">X</td><td colspan="1" rowspan="1">×</td><td colspan="1" rowspan="1">N/A</td><td colspan="1" rowspan="1">X</td><td colspan="1" rowspan="1">X</td><td colspan="1" rowspan="1">X</td><td colspan="1" rowspan="1">X</td></tr><tr><td colspan="2" rowspan="1">VBAT mode</td><td colspan="1" rowspan="1">X</td><td colspan="1" rowspan="1">x</td><td colspan="1" rowspan="1">X</td><td colspan="1" rowspan="1">X</td><td colspan="1" rowspan="1">X</td><td colspan="1" rowspan="1">N/A</td><td colspan="1" rowspan="1">N/A</td><td colspan="1" rowspan="1">N/A</td><td colspan="1" rowspan="1">X</td><td colspan="1" rowspan="1">X</td><td colspan="1" rowspan="1">X</td><td colspan="1" rowspan="1">X</td></tr><tr><td colspan="1" rowspan="6">r</td><td colspan="1" rowspan="2">Alarms available</td><td colspan="1" rowspan="1">Alarm A</td><td colspan="1" rowspan="1">X</td><td colspan="1" rowspan="1">X</td><td colspan="1" rowspan="1">X</td><td colspan="1" rowspan="1">X</td><td colspan="1" rowspan="1">X</td><td colspan="1" rowspan="1">×</td><td colspan="1" rowspan="1">×</td><td colspan="1" rowspan="1">×</td><td colspan="1" rowspan="1">X</td><td colspan="1" rowspan="1">X</td><td colspan="1" rowspan="1">X</td><td colspan="1" rowspan="1">X</td></tr><tr><td colspan="1" rowspan="1">Alarm B</td><td colspan="1" rowspan="1">N/A</td><td colspan="1" rowspan="1">×</td><td colspan="1" rowspan="1">×</td><td colspan="1" rowspan="1">X</td><td colspan="1" rowspan="1">X</td><td colspan="1" rowspan="1">×</td><td colspan="1" rowspan="1">×</td><td colspan="1" rowspan="1">×</td><td colspan="1" rowspan="1">X</td><td colspan="1" rowspan="1">×</td><td colspan="1" rowspan="1">X</td><td colspan="1" rowspan="1">N/A</td></tr><tr><td colspan="1" rowspan="3">Time</td><td colspan="1" rowspan="1">12 h/24 h format</td><td colspan="1" rowspan="1">×</td><td colspan="1" rowspan="1">X</td><td colspan="1" rowspan="1">X</td><td colspan="1" rowspan="1">X</td><td colspan="1" rowspan="1">X</td><td colspan="1" rowspan="1">X</td><td colspan="1" rowspan="1">X</td><td colspan="1" rowspan="1">X</td><td colspan="1" rowspan="1">X</td><td colspan="1" rowspan="1">X</td><td colspan="1" rowspan="1">X</td><td colspan="1" rowspan="1">×</td></tr><tr><td colspan="1" rowspan="1">Hour, minute,second</td><td colspan="1" rowspan="1">X</td><td colspan="1" rowspan="1">X</td><td colspan="1" rowspan="1">X</td><td colspan="1" rowspan="1">X</td><td colspan="1" rowspan="1">X</td><td colspan="1" rowspan="1">X</td><td colspan="1" rowspan="1">X</td><td colspan="1" rowspan="1">X</td><td colspan="1" rowspan="1">X</td><td colspan="1" rowspan="1">X</td><td colspan="1" rowspan="1">X</td><td colspan="1" rowspan="1">X</td></tr><tr><td colspan="1" rowspan="1">Subsecond</td><td colspan="1" rowspan="1">×</td><td colspan="1" rowspan="1">N/A</td><td colspan="1" rowspan="1">X</td><td colspan="1" rowspan="1">X</td><td colspan="1" rowspan="1">X</td><td colspan="1" rowspan="1">×</td><td colspan="1" rowspan="1">×</td><td colspan="1" rowspan="1">N/A</td><td colspan="1" rowspan="1">X</td><td colspan="1" rowspan="1">X</td><td colspan="1" rowspan="1">×</td><td colspan="1" rowspan="1">×</td></tr><tr><td colspan="2" rowspan="1">Date or week day</td><td colspan="1" rowspan="1">×</td><td colspan="1" rowspan="1">×</td><td colspan="1" rowspan="1">×</td><td colspan="1" rowspan="1">X</td><td colspan="1" rowspan="1">X</td><td colspan="1" rowspan="1">×</td><td colspan="1" rowspan="1">X</td><td colspan="1" rowspan="1">X</td><td colspan="1" rowspan="1">X</td><td colspan="1" rowspan="1">×</td><td colspan="1" rowspan="1">×</td><td colspan="1" rowspan="1">×</td></tr><tr><td colspan="1" rowspan="6">Tamej edcon</td><td colspan="2" rowspan="1">Configurable input mapping</td><td colspan="1" rowspan="1">X</td><td colspan="1" rowspan="1">X</td><td colspan="1" rowspan="1">X</td><td colspan="1" rowspan="1">X</td><td colspan="1" rowspan="1">X</td><td colspan="1" rowspan="1">×</td><td colspan="1" rowspan="1">N/A</td><td colspan="1" rowspan="1">N/A</td><td colspan="1" rowspan="1">X</td><td colspan="1" rowspan="1">X</td><td colspan="1" rowspan="1">X</td><td colspan="1" rowspan="1">×</td></tr><tr><td colspan="2" rowspan="1">Configurable edge detection</td><td colspan="1" rowspan="1">×</td><td colspan="1" rowspan="1">×</td><td colspan="1" rowspan="1">×</td><td colspan="1" rowspan="1">×</td><td colspan="1" rowspan="1">X</td><td colspan="1" rowspan="1">×</td><td colspan="1" rowspan="1">×</td><td colspan="1" rowspan="1">×</td><td colspan="1" rowspan="1">X</td><td colspan="1" rowspan="1">×</td><td colspan="1" rowspan="1">×</td><td colspan="1" rowspan="1">N/A</td></tr><tr><td colspan="2" rowspan="1">Configurable evel detectionfigsampling, and precharge configurationon tamper input</td><td colspan="1" rowspan="1">X</td><td colspan="1" rowspan="1">N/A</td><td colspan="1" rowspan="1">X</td><td colspan="1" rowspan="1">X</td><td colspan="1" rowspan="1">X</td><td colspan="1" rowspan="1">X</td><td colspan="1" rowspan="1">X</td><td colspan="1" rowspan="1">N/A</td><td colspan="1" rowspan="1">X</td><td colspan="1" rowspan="1">X</td><td colspan="1" rowspan="1">X</td><td colspan="1" rowspan="1">N/A</td></tr><tr><td colspan="2" rowspan="1">Number of tamper inputs</td><td colspan="1" rowspan="1">2(3)</td><td colspan="1" rowspan="1">2</td><td colspan="1" rowspan="1">2</td><td colspan="1" rowspan="1">2</td><td colspan="1" rowspan="1">3</td><td colspan="1" rowspan="1">3</td><td colspan="1" rowspan="1">3</td><td colspan="1" rowspan="1">1</td><td colspan="1" rowspan="1">3</td><td colspan="1" rowspan="1">3</td><td colspan="1" rowspan="1">3</td><td colspan="1" rowspan="1">N/A</td></tr><tr><td colspan="2" rowspan="1">Number of tamper events</td><td colspan="1" rowspan="1">0</td><td colspan="1" rowspan="1">1</td><td colspan="1" rowspan="1">2</td><td colspan="1" rowspan="1">2</td><td colspan="1" rowspan="1">3</td><td colspan="1" rowspan="1">3</td><td colspan="1" rowspan="1">3</td><td colspan="1" rowspan="1">1</td><td colspan="1" rowspan="1">3</td><td colspan="1" rowspan="1">3</td><td colspan="1" rowspan="1">3</td><td colspan="1" rowspan="1">N/A</td></tr><tr><td colspan="2" rowspan="1">VBAT mode pins (inputs)</td><td colspan="1" rowspan="1">1</td><td colspan="1" rowspan="1">1</td><td colspan="1" rowspan="1">1</td><td colspan="1" rowspan="1">2</td><td colspan="1" rowspan="1">2</td><td colspan="1" rowspan="1">N/A</td><td colspan="1" rowspan="1">N/A</td><td colspan="1" rowspan="1">N/A</td><td colspan="1" rowspan="1">3</td><td colspan="1" rowspan="1">3</td><td colspan="1" rowspan="1">3</td><td colspan="1" rowspan="1">N/A</td></tr><tr><td colspan="1" rowspan="5">iwmsem</td><td colspan="2" rowspan="1">Configurable input mapping</td><td colspan="1" rowspan="1">X</td><td colspan="1" rowspan="1">X</td><td colspan="1" rowspan="1">X</td><td colspan="1" rowspan="1">X</td><td colspan="1" rowspan="1">X</td><td colspan="1" rowspan="1">X(4)</td><td colspan="1" rowspan="1">N/A</td><td colspan="1" rowspan="1">N/A</td><td colspan="1" rowspan="1">X(4)</td><td colspan="1" rowspan="1">X</td><td colspan="1" rowspan="1">X(4)</td><td colspan="1" rowspan="1">N/A</td></tr><tr><td colspan="1" rowspan="2">Time</td><td colspan="1" rowspan="1">Hour, minute,second</td><td colspan="1" rowspan="1">X</td><td colspan="1" rowspan="1">X</td><td colspan="1" rowspan="1">X</td><td colspan="1" rowspan="1">X</td><td colspan="1" rowspan="1">X</td><td colspan="1" rowspan="1">X</td><td colspan="1" rowspan="1">X</td><td colspan="1" rowspan="1">X</td><td colspan="1" rowspan="1">X</td><td colspan="1" rowspan="1">X</td><td colspan="1" rowspan="1">X</td><td colspan="1" rowspan="1">N/A</td></tr><tr><td colspan="1" rowspan="1">Subseconds</td><td colspan="1" rowspan="1">X</td><td colspan="1" rowspan="1">N/A</td><td colspan="1" rowspan="1">×</td><td colspan="1" rowspan="1">X</td><td colspan="1" rowspan="1">X</td><td colspan="1" rowspan="1">×</td><td colspan="1" rowspan="1">X</td><td colspan="1" rowspan="1">N/A</td><td colspan="1" rowspan="1">X</td><td colspan="1" rowspan="1">×</td><td colspan="1" rowspan="1">×</td><td colspan="1" rowspan="1">N/A</td></tr><tr><td colspan="2" rowspan="1">Date (day, month)</td><td colspan="1" rowspan="1">X</td><td colspan="1" rowspan="1">×</td><td colspan="1" rowspan="1">X</td><td colspan="1" rowspan="1">X</td><td colspan="1" rowspan="1">X</td><td colspan="1" rowspan="1">X</td><td colspan="1" rowspan="1">×</td><td colspan="1" rowspan="1">×</td><td colspan="1" rowspan="1">X</td><td colspan="1" rowspan="1">X</td><td colspan="1" rowspan="1">X</td><td colspan="1" rowspan="1">N/A</td></tr><tr><td colspan="2" rowspan="1">Timestamp on tamper detection event</td><td colspan="1" rowspan="1">X</td><td colspan="1" rowspan="1">×</td><td colspan="1" rowspan="1">×</td><td colspan="1" rowspan="1">×</td><td colspan="1" rowspan="1">×</td><td colspan="1" rowspan="1">×</td><td colspan="1" rowspan="1">×</td><td colspan="1" rowspan="1">×</td><td colspan="1" rowspan="1">×</td><td colspan="1" rowspan="1">×</td><td colspan="1" rowspan="1">×</td><td colspan="1" rowspan="1">N/A</td></tr><tr><td colspan="3" rowspan="2">Features</td><td colspan="1" rowspan="2">STMRS</td><td colspan="1" rowspan="2">2</td><td colspan="1" rowspan="2">1</td><td colspan="1" rowspan="2">2</td><td colspan="1" rowspan="2">STM32</td><td colspan="1" rowspan="2">N</td><td colspan="2" rowspan="1">STM32L1</td><td colspan="1" rowspan="2">()1⊥|(z)+M32⊥</td><td colspan="1" rowspan="2">20</td><td colspan="1" rowspan="2">2</td><td colspan="1" rowspan="2">2</td></tr><tr><td colspan="1" rowspan="1">20</td><td colspan="1" rowspan="1">C∃</td></tr><tr><td colspan="1" rowspan="1">iwmemm</td><td colspan="2" rowspan="1">Timestamp on switch to VBAT mode</td><td colspan="1" rowspan="1">N/A</td><td colspan="1" rowspan="1">N/A</td><td colspan="1" rowspan="1">N/A</td><td colspan="1" rowspan="1">N/A</td><td colspan="1" rowspan="1">X</td><td colspan="1" rowspan="1">N/A</td><td colspan="1" rowspan="1">N/A</td><td colspan="1" rowspan="1">N/A</td><td colspan="1" rowspan="1">X</td><td colspan="1" rowspan="1">X</td><td colspan="1" rowspan="1">X</td><td colspan="1" rowspan="1">N/A</td></tr><tr><td colspan="1" rowspan="4">Pn S</td><td colspan="1" rowspan="2">RTC_ ALARM</td><td colspan="1" rowspan="1">Alarm event</td><td colspan="1" rowspan="1">X</td><td colspan="1" rowspan="1">X</td><td colspan="1" rowspan="1">X</td><td colspan="1" rowspan="1">×</td><td colspan="1" rowspan="1">×</td><td colspan="1" rowspan="1">X</td><td colspan="1" rowspan="1">X</td><td colspan="1" rowspan="1">X</td><td colspan="1" rowspan="1">X</td><td colspan="1" rowspan="1">X</td><td colspan="1" rowspan="1">X</td><td colspan="1" rowspan="1">X</td></tr><tr><td colspan="1" rowspan="1">Wakeup event</td><td colspan="1" rowspan="1">X</td><td colspan="1" rowspan="1">X</td><td colspan="1" rowspan="1">X</td><td colspan="1" rowspan="1">X</td><td colspan="1" rowspan="1">X</td><td colspan="1" rowspan="1">X</td><td colspan="1" rowspan="1">X</td><td colspan="1" rowspan="1">X</td><td colspan="1" rowspan="1">X</td><td colspan="1" rowspan="1">X</td><td colspan="1" rowspan="1">X</td><td colspan="1" rowspan="1">X</td></tr><tr><td colspan="1" rowspan="2">RTC_ CALIB</td><td colspan="1" rowspan="1">512 Hz</td><td colspan="1" rowspan="1">X</td><td colspan="1" rowspan="1">X</td><td colspan="1" rowspan="1">×</td><td colspan="1" rowspan="1">×</td><td colspan="1" rowspan="1">×</td><td colspan="1" rowspan="1">X</td><td colspan="1" rowspan="1">X</td><td colspan="1" rowspan="1">X</td><td colspan="1" rowspan="1">X</td><td colspan="1" rowspan="1">×</td><td colspan="1" rowspan="1">×</td><td colspan="1" rowspan="1">X</td></tr><tr><td colspan="1" rowspan="1">1 Hz</td><td colspan="1" rowspan="1">X</td><td colspan="1" rowspan="1">N/A</td><td colspan="1" rowspan="1">X</td><td colspan="1" rowspan="1">X</td><td colspan="1" rowspan="1">X</td><td colspan="1" rowspan="1">X</td><td colspan="1" rowspan="1">X</td><td colspan="1" rowspan="1">N/A</td><td colspan="1" rowspan="1">X</td><td colspan="1" rowspan="1">X</td><td colspan="1" rowspan="1">X</td><td colspan="1" rowspan="1">X</td></tr></table>

<table><tr><td rowspan=2 colspan=2>Features</td><td rowspan=2 colspan=1>2</td><td rowspan=2 colspan=1>2</td><td rowspan=2 colspan=1>M</td><td rowspan=2 colspan=1>2</td><td rowspan=2 colspan=1>2</td><td rowspan=2 colspan=1>N</td><td rowspan=1 colspan=2>STM32L1</td><td rowspan=2 colspan=1>(∃1⊥|(z)+M2⊥</td><td rowspan=2 colspan=1>202</td><td rowspan=2 colspan=1>2</td><td rowspan=2 colspan=1>2</td></tr><tr><td rowspan=1 colspan=1>20</td><td rowspan=1 colspan=1></td></tr><tr><td rowspan=2 colspan=1>20DaE</td><td rowspan=1 colspan=1>Coarse calibration</td><td rowspan=1 colspan=1>N/A(5)</td><td rowspan=1 colspan=1>X</td><td rowspan=1 colspan=1>N/A(5)</td><td rowspan=1 colspan=1>X</td><td rowspan=1 colspan=1>N/A(5)</td><td rowspan=1 colspan=1>N/A(5)</td><td rowspan=1 colspan=1>X</td><td rowspan=1 colspan=1>X</td><td rowspan=1 colspan=1>N/A(5)</td><td rowspan=1 colspan=1>N/A(5)</td><td rowspan=1 colspan=1>N/A(5)</td><td rowspan=1 colspan=1>N/A(5)</td></tr><tr><td rowspan=1 colspan=1>Smooth calibration</td><td rowspan=1 colspan=1>X</td><td rowspan=1 colspan=1>N/A</td><td rowspan=1 colspan=1>X</td><td rowspan=1 colspan=1>X</td><td rowspan=1 colspan=1>X</td><td rowspan=1 colspan=1>X</td><td rowspan=1 colspan=1>X</td><td rowspan=1 colspan=1>N/A</td><td rowspan=1 colspan=1>X</td><td rowspan=1 colspan=1>X</td><td rowspan=1 colspan=1>X</td><td rowspan=1 colspan=1>X</td></tr><tr><td rowspan=1 colspan=2>Synchronizing the RTC</td><td rowspan=1 colspan=1>X</td><td rowspan=1 colspan=1>N/A</td><td rowspan=1 colspan=1>X</td><td rowspan=1 colspan=1>X</td><td rowspan=1 colspan=1>X</td><td rowspan=1 colspan=1>X</td><td rowspan=1 colspan=1>X</td><td rowspan=1 colspan=1>N/A</td><td rowspan=1 colspan=1>X</td><td rowspan=1 colspan=1>×</td><td rowspan=1 colspan=1>X</td><td rowspan=1 colspan=1>X</td></tr><tr><td rowspan=1 colspan=2>Reference clock detection</td><td rowspan=1 colspan=1>X</td><td rowspan=1 colspan=1>×</td><td rowspan=1 colspan=1>X</td><td rowspan=1 colspan=1>X</td><td rowspan=1 colspan=1>X</td><td rowspan=1 colspan=1>X</td><td rowspan=1 colspan=1>X</td><td rowspan=1 colspan=1>×</td><td rowspan=1 colspan=1>X</td><td rowspan=1 colspan=1>X</td><td rowspan=1 colspan=1>X</td><td rowspan=1 colspan=1>X</td></tr><tr><td rowspan=4 colspan=1>sesbe rsg</td><td rowspan=1 colspan=1>Powered-on VBAT</td><td rowspan=1 colspan=1>X</td><td rowspan=1 colspan=1>X</td><td rowspan=1 colspan=1>X</td><td rowspan=1 colspan=1>X</td><td rowspan=1 colspan=1>X</td><td rowspan=1 colspan=1>N/A</td><td rowspan=1 colspan=1>N/A</td><td rowspan=1 colspan=1>N/A</td><td rowspan=1 colspan=1>X</td><td rowspan=1 colspan=1>X</td><td rowspan=1 colspan=1>X</td><td rowspan=1 colspan=1>VDD12</td></tr><tr><td rowspan=1 colspan=1>Reset on a tamper detection</td><td rowspan=1 colspan=1>X</td><td rowspan=1 colspan=1>X</td><td rowspan=1 colspan=1>X</td><td rowspan=1 colspan=1>X</td><td rowspan=1 colspan=1>X</td><td rowspan=1 colspan=1>X</td><td rowspan=1 colspan=1>X</td><td rowspan=1 colspan=1>X</td><td rowspan=1 colspan=1>X</td><td rowspan=1 colspan=1>X</td><td rowspan=1 colspan=1>X</td><td rowspan=1 colspan=1>N/A</td></tr><tr><td rowspan=1 colspan=1>Reset when flash memory readoutprotection is disabled</td><td rowspan=1 colspan=1>X</td><td rowspan=1 colspan=1>N/A</td><td rowspan=1 colspan=1>X</td><td rowspan=1 colspan=1>N/A</td><td rowspan=1 colspan=1>X</td><td rowspan=1 colspan=1>X</td><td rowspan=1 colspan=1>X</td><td rowspan=1 colspan=1>X</td><td rowspan=1 colspan=1>X</td><td rowspan=1 colspan=1>X</td><td rowspan=1 colspan=1>X</td><td rowspan=1 colspan=1>N/A</td></tr><tr><td rowspan=1 colspan=1>Number of backup registers</td><td rowspan=1 colspan=1>5</td><td rowspan=1 colspan=1>20</td><td rowspan=1 colspan=1>16</td><td rowspan=1 colspan=1>20</td><td rowspan=1 colspan=1>32</td><td rowspan=1 colspan=1>5</td><td rowspan=1 colspan=1>32(6)</td><td rowspan=1 colspan=1>20</td><td rowspan=1 colspan=1>20(7)</td><td rowspan=1 colspan=1>32</td><td rowspan=1 colspan=1>20</td><td rowspan=1 colspan=1>5</td></tr></table>

1. Except STM32L41/42xxx. 2. Except STM32L4P5/Q5 line. 3. 3 inputs for STM32F07/F09x. 4. Thanks to timestamp on tamper event. 5. Obsolete, replaced by smooth calibration. 6. Only 20 for Cat 2. 7. 32 for STM32L4R/4S line.

Table 5. Advanced features of RTC3 type   

<table><tr><td colspan="3" rowspan="1">Features</td><td colspan="1" rowspan="1">20</td><td colspan="1" rowspan="1">20</td><td colspan="1" rowspan="1">20</td><td colspan="1" rowspan="1">2</td><td colspan="1" rowspan="1">20</td><td colspan="1" rowspan="1"></td><td colspan="1" rowspan="1">N</td><td colspan="1" rowspan="1">N</td><td colspan="1" rowspan="1">2</td><td colspan="1" rowspan="1">2</td><td colspan="1" rowspan="1">20</td><td colspan="1" rowspan="1">N</td><td colspan="1" rowspan="1">20</td><td colspan="1" rowspan="1">20</td></tr><tr><td colspan="3" rowspan="1">RTC clock source (LSE, LSI,HSE with prescaler)</td><td colspan="1" rowspan="1">X</td><td colspan="1" rowspan="1">X</td><td colspan="1" rowspan="1">X</td><td colspan="1" rowspan="1">X</td><td colspan="1" rowspan="1">X</td><td colspan="1" rowspan="1">X</td><td colspan="1" rowspan="1">X</td><td colspan="1" rowspan="1">X</td><td colspan="1" rowspan="1">X</td><td colspan="1" rowspan="1">X</td><td colspan="1" rowspan="1">X</td><td colspan="1" rowspan="1">X</td><td colspan="1" rowspan="1">X</td><td colspan="1" rowspan="1">X</td></tr><tr><td colspan="3" rowspan="1">Binary mode</td><td colspan="1" rowspan="1">N/A</td><td colspan="1" rowspan="1">N/A</td><td colspan="1" rowspan="1">N/A</td><td colspan="1" rowspan="1">X</td><td colspan="1" rowspan="1">N/A</td><td colspan="1" rowspan="1">N/A</td><td colspan="1" rowspan="1">N/A</td><td colspan="1" rowspan="1">X</td><td colspan="1" rowspan="1">X</td><td colspan="1" rowspan="1">X</td><td colspan="1" rowspan="1">X</td><td colspan="1" rowspan="1">X</td><td colspan="1" rowspan="1">N/A</td><td colspan="1" rowspan="1">X</td></tr><tr><td colspan="3" rowspan="1">Mixed mode (BCD andbinary)</td><td colspan="1" rowspan="1">N/A</td><td colspan="1" rowspan="1">N/A</td><td colspan="1" rowspan="1">N/A</td><td colspan="1" rowspan="1">X</td><td colspan="1" rowspan="1">N/A</td><td colspan="1" rowspan="1">N/A</td><td colspan="1" rowspan="1">N/A</td><td colspan="1" rowspan="1">X</td><td colspan="1" rowspan="1">X</td><td colspan="1" rowspan="1">X</td><td colspan="1" rowspan="1">X</td><td colspan="1" rowspan="1">X</td><td colspan="1" rowspan="1">N/A</td><td colspan="1" rowspan="1">X</td></tr><tr><td colspan="1" rowspan="2">20</td><td colspan="2" rowspan="1">Asynchronous(number of bits)</td><td colspan="1" rowspan="1">X (7)</td><td colspan="1" rowspan="1">X (7)</td><td colspan="1" rowspan="1">X (7)</td><td colspan="1" rowspan="1">X (7)</td><td colspan="1" rowspan="1">X (7)</td><td colspan="1" rowspan="1">X (7)</td><td colspan="1" rowspan="1">X (7)</td><td colspan="1" rowspan="1">X (7)</td><td colspan="1" rowspan="1">X (7)</td><td colspan="1" rowspan="1">X (7)</td><td colspan="1" rowspan="1">X (7)</td><td colspan="1" rowspan="1">X (7)</td><td colspan="1" rowspan="1">X(7)</td><td colspan="1" rowspan="1">X(7)</td></tr><tr><td colspan="2" rowspan="1">Synchronous (numberof bits)</td><td colspan="1" rowspan="1">X (15)</td><td colspan="1" rowspan="1">X(15)</td><td colspan="1" rowspan="1">X(15)</td><td colspan="1" rowspan="1">X(15)</td><td colspan="1" rowspan="1">X(15)</td><td colspan="1" rowspan="1">X(15)</td><td colspan="1" rowspan="1">X(15)</td><td colspan="1" rowspan="1">X(15)</td><td colspan="1" rowspan="1">X(15)</td><td colspan="1" rowspan="1">X (15)</td><td colspan="1" rowspan="1">X (15)</td><td colspan="1" rowspan="1">X(15)</td><td colspan="1" rowspan="1">X(15)</td><td colspan="1" rowspan="1">X(15)</td></tr><tr><td colspan="1" rowspan="7">20</td><td colspan="1" rowspan="2">Time</td><td colspan="1" rowspan="1">12 h/24 hformat</td><td colspan="1" rowspan="1">X</td><td colspan="1" rowspan="1">X</td><td colspan="1" rowspan="1">X</td><td colspan="1" rowspan="1">X</td><td colspan="1" rowspan="1">X</td><td colspan="1" rowspan="1">X</td><td colspan="1" rowspan="1">X</td><td colspan="1" rowspan="1">X</td><td colspan="1" rowspan="1">X</td><td colspan="1" rowspan="1">X</td><td colspan="1" rowspan="1">X</td><td colspan="1" rowspan="1">X</td><td colspan="1" rowspan="1">X</td><td colspan="1" rowspan="1">X</td></tr><tr><td colspan="1" rowspan="1">Hour,minute,second</td><td colspan="1" rowspan="1">X</td><td colspan="1" rowspan="1">X</td><td colspan="1" rowspan="1">X</td><td colspan="1" rowspan="1">X</td><td colspan="1" rowspan="1">X</td><td colspan="1" rowspan="1">X</td><td colspan="1" rowspan="1">X</td><td colspan="1" rowspan="1">X</td><td colspan="1" rowspan="1">X</td><td colspan="1" rowspan="1">X</td><td colspan="1" rowspan="1">X</td><td colspan="1" rowspan="1">X</td><td colspan="1" rowspan="1">X</td><td colspan="1" rowspan="1">X</td></tr><tr><td colspan="1" rowspan="1"></td><td colspan="1" rowspan="1">Subsecond</td><td colspan="1" rowspan="1">X</td><td colspan="1" rowspan="1">X</td><td colspan="1" rowspan="1">X</td><td colspan="1" rowspan="1">X</td><td colspan="1" rowspan="1">X</td><td colspan="1" rowspan="1">X</td><td colspan="1" rowspan="1">X</td><td colspan="1" rowspan="1">X</td><td colspan="1" rowspan="1">X</td><td colspan="1" rowspan="1">X</td><td colspan="1" rowspan="1">X</td><td colspan="1" rowspan="1">X</td><td colspan="1" rowspan="1">X</td><td colspan="1" rowspan="1">X</td></tr><tr><td colspan="2" rowspan="1">Date</td><td colspan="1" rowspan="1">X</td><td colspan="1" rowspan="1">X</td><td colspan="1" rowspan="1">X</td><td colspan="1" rowspan="1">X</td><td colspan="1" rowspan="1">X</td><td colspan="1" rowspan="1">X</td><td colspan="1" rowspan="1">X</td><td colspan="1" rowspan="1">X</td><td colspan="1" rowspan="1">X</td><td colspan="1" rowspan="1">X</td><td colspan="1" rowspan="1">X</td><td colspan="1" rowspan="1">X</td><td colspan="1" rowspan="1">X</td><td colspan="1" rowspan="1">X</td></tr><tr><td colspan="2" rowspan="1">Daylight operation</td><td colspan="1" rowspan="1">X</td><td colspan="1" rowspan="1">X</td><td colspan="1" rowspan="1">X</td><td colspan="1" rowspan="1">X</td><td colspan="1" rowspan="1">X</td><td colspan="1" rowspan="1">X</td><td colspan="1" rowspan="1">X</td><td colspan="1" rowspan="1">X</td><td colspan="1" rowspan="1">X</td><td colspan="1" rowspan="1">X</td><td colspan="1" rowspan="1">X</td><td colspan="1" rowspan="1">X</td><td colspan="1" rowspan="1">X</td><td colspan="1" rowspan="1">X</td></tr><tr><td colspan="2" rowspan="1">Bypass the shadowregisters</td><td colspan="1" rowspan="1">X</td><td colspan="1" rowspan="1">X</td><td colspan="1" rowspan="1">X</td><td colspan="1" rowspan="1">X</td><td colspan="1" rowspan="1">X</td><td colspan="1" rowspan="1">X</td><td colspan="1" rowspan="1">X</td><td colspan="1" rowspan="1">X</td><td colspan="1" rowspan="1">X</td><td colspan="1" rowspan="1">X</td><td colspan="1" rowspan="1">X</td><td colspan="1" rowspan="1">X</td><td colspan="1" rowspan="1">X</td><td colspan="1" rowspan="1">X</td></tr><tr><td colspan="2" rowspan="1">Power optimizationmode</td><td colspan="1" rowspan="1">N/A</td><td colspan="1" rowspan="1">N/A</td><td colspan="1" rowspan="1">N/A</td><td colspan="1" rowspan="1">X</td><td colspan="1" rowspan="1">N/A</td><td colspan="1" rowspan="1">X</td><td colspan="1" rowspan="1">X</td><td colspan="1" rowspan="1">X</td><td colspan="1" rowspan="1">X</td><td colspan="1" rowspan="1">X</td><td colspan="1" rowspan="1">X</td><td colspan="1" rowspan="1">X</td><td colspan="1" rowspan="1">X</td><td colspan="1" rowspan="1">X</td></tr><tr><td colspan="1" rowspan="7">r</td><td colspan="1" rowspan="1">Alarms</td><td colspan="1" rowspan="1">Alarm A</td><td colspan="1" rowspan="1">X</td><td colspan="1" rowspan="1">X</td><td colspan="1" rowspan="1">X</td><td colspan="1" rowspan="1">X</td><td colspan="1" rowspan="1">X</td><td colspan="1" rowspan="1">X</td><td colspan="1" rowspan="1">X</td><td colspan="1" rowspan="1">X</td><td colspan="1" rowspan="1">X</td><td colspan="1" rowspan="1">X</td><td colspan="1" rowspan="1">X</td><td colspan="1" rowspan="1">X</td><td colspan="1" rowspan="1">X</td><td colspan="1" rowspan="1">X</td></tr><tr><td colspan="1" rowspan="1">avilable</td><td colspan="1" rowspan="1">Alarm B</td><td colspan="1" rowspan="1">N/A</td><td colspan="1" rowspan="1">X</td><td colspan="1" rowspan="1">X</td><td colspan="1" rowspan="1">X</td><td colspan="1" rowspan="1">X</td><td colspan="1" rowspan="1">X</td><td colspan="1" rowspan="1">X</td><td colspan="1" rowspan="1">X</td><td colspan="1" rowspan="1">X</td><td colspan="1" rowspan="1">X</td><td colspan="1" rowspan="1">X</td><td colspan="1" rowspan="1">X</td><td colspan="1" rowspan="1">X</td><td colspan="1" rowspan="1">X</td></tr><tr><td colspan="1" rowspan="3">Time</td><td colspan="1" rowspan="1">12 h/24 hformat</td><td colspan="1" rowspan="1">X</td><td colspan="1" rowspan="1">X</td><td colspan="1" rowspan="1">X</td><td colspan="1" rowspan="1">X</td><td colspan="1" rowspan="1">X</td><td colspan="1" rowspan="1">X</td><td colspan="1" rowspan="1">X</td><td colspan="1" rowspan="1">X</td><td colspan="1" rowspan="1">X</td><td colspan="1" rowspan="1">X</td><td colspan="1" rowspan="1">X</td><td colspan="1" rowspan="1">X</td><td colspan="1" rowspan="1">X</td><td colspan="1" rowspan="1">X</td></tr><tr><td colspan="1" rowspan="1">Hour,minute,second</td><td colspan="1" rowspan="1">X</td><td colspan="1" rowspan="1">X</td><td colspan="1" rowspan="1">X</td><td colspan="1" rowspan="1">X</td><td colspan="1" rowspan="1">X</td><td colspan="1" rowspan="1">X</td><td colspan="1" rowspan="1">X</td><td colspan="1" rowspan="1">X</td><td colspan="1" rowspan="1">X</td><td colspan="1" rowspan="1">X</td><td colspan="1" rowspan="1">X</td><td colspan="1" rowspan="1">X</td><td colspan="1" rowspan="1">X</td><td colspan="1" rowspan="1">X</td></tr><tr><td colspan="1" rowspan="1">Subsecond</td><td colspan="1" rowspan="1">X</td><td colspan="1" rowspan="1">X</td><td colspan="1" rowspan="1">X</td><td colspan="1" rowspan="1">X</td><td colspan="1" rowspan="1">X</td><td colspan="1" rowspan="1">X</td><td colspan="1" rowspan="1">X</td><td colspan="1" rowspan="1">X</td><td colspan="1" rowspan="1">X</td><td colspan="1" rowspan="1">X</td><td colspan="1" rowspan="1">X</td><td colspan="1" rowspan="1">X</td><td colspan="1" rowspan="1">X</td><td colspan="1" rowspan="1">X</td></tr><tr><td colspan="2" rowspan="1">Date or week day</td><td colspan="1" rowspan="1">X</td><td colspan="1" rowspan="1">X</td><td colspan="1" rowspan="1">X</td><td colspan="1" rowspan="1">X</td><td colspan="1" rowspan="1">X</td><td colspan="1" rowspan="1">X</td><td colspan="1" rowspan="1">X</td><td colspan="1" rowspan="1">X</td><td colspan="1" rowspan="1">×</td><td colspan="1" rowspan="1">X</td><td colspan="1" rowspan="1">X</td><td colspan="1" rowspan="1">X</td><td colspan="1" rowspan="1">×</td><td colspan="1" rowspan="1">×</td></tr><tr><td colspan="2" rowspan="1">Binary mode alarm</td><td colspan="1" rowspan="1">N/A</td><td colspan="1" rowspan="1">N/A</td><td colspan="1" rowspan="1">N/A</td><td colspan="1" rowspan="1">X</td><td colspan="1" rowspan="1">N/A</td><td colspan="1" rowspan="1">N/A</td><td colspan="1" rowspan="1">N/A</td><td colspan="1" rowspan="1">X</td><td colspan="1" rowspan="1">X</td><td colspan="1" rowspan="1">X</td><td colspan="1" rowspan="1">X</td><td colspan="1" rowspan="1">X</td><td colspan="1" rowspan="1">X</td><td colspan="1" rowspan="1">X</td></tr><tr><td colspan="1" rowspan="9">20</td><td colspan="1" rowspan="3">Tamperreactions</td><td colspan="1" rowspan="1">Backuegisters rasing</td><td colspan="1" rowspan="1">N/A</td><td colspan="1" rowspan="1">X</td><td colspan="1" rowspan="1">X</td><td colspan="1" rowspan="1">X(2)</td><td colspan="1" rowspan="1">X(1)</td><td colspan="1" rowspan="1">X</td><td colspan="1" rowspan="1">X(1)</td><td colspan="1" rowspan="1">X(2)</td><td colspan="1" rowspan="1">X(2)</td><td colspan="1" rowspan="1">X(2)</td><td colspan="1" rowspan="1">X(1)</td><td colspan="1" rowspan="1">X(1)</td><td colspan="1" rowspan="1">X(1)</td><td colspan="1" rowspan="1">X(2)</td></tr><tr><td colspan="1" rowspan="1">Interruption</td><td colspan="1" rowspan="1">N/A</td><td colspan="1" rowspan="1">X</td><td colspan="1" rowspan="1">X</td><td colspan="1" rowspan="1">X</td><td colspan="1" rowspan="1">X</td><td colspan="1" rowspan="1">X</td><td colspan="1" rowspan="1">X</td><td colspan="1" rowspan="1">X</td><td colspan="1" rowspan="1">X</td><td colspan="1" rowspan="1">X</td><td colspan="1" rowspan="1">X</td><td colspan="1" rowspan="1">X</td><td colspan="1" rowspan="1">X</td><td colspan="1" rowspan="1">X</td></tr><tr><td colspan="1" rowspan="1">Triger ime e</td><td colspan="1" rowspan="1">N/A</td><td colspan="1" rowspan="1">X</td><td colspan="1" rowspan="1">X</td><td colspan="1" rowspan="1">X</td><td colspan="1" rowspan="1">X</td><td colspan="1" rowspan="1">X</td><td colspan="1" rowspan="1">X</td><td colspan="1" rowspan="1">X</td><td colspan="1" rowspan="1">X</td><td colspan="1" rowspan="1">X</td><td colspan="1" rowspan="1">X</td><td colspan="1" rowspan="1">X</td><td colspan="1" rowspan="1">X</td><td colspan="1" rowspan="1">X</td></tr><tr><td colspan="2" rowspan="1">Configurable edgedtection</td><td colspan="1" rowspan="1">N/A</td><td colspan="1" rowspan="1">X</td><td colspan="1" rowspan="1">X</td><td colspan="1" rowspan="1">X</td><td colspan="1" rowspan="1">X</td><td colspan="1" rowspan="1">X</td><td colspan="1" rowspan="1">X</td><td colspan="1" rowspan="1">X</td><td colspan="1" rowspan="1">X</td><td colspan="1" rowspan="1">X</td><td colspan="1" rowspan="1">X</td><td colspan="1" rowspan="1">X</td><td colspan="1" rowspan="1">X</td><td colspan="1" rowspan="1">X</td></tr><tr><td colspan="2" rowspan="1">Configurable leveldetection)</td><td colspan="1" rowspan="1">N/A</td><td colspan="1" rowspan="1">X</td><td colspan="1" rowspan="1">X</td><td colspan="1" rowspan="1">X</td><td colspan="1" rowspan="1">X</td><td colspan="1" rowspan="1">X</td><td colspan="1" rowspan="1">X</td><td colspan="1" rowspan="1">X</td><td colspan="1" rowspan="1">X</td><td colspan="1" rowspan="1">X</td><td colspan="1" rowspan="1">X</td><td colspan="1" rowspan="1">X</td><td colspan="1" rowspan="1">X</td><td colspan="1" rowspan="1">X</td></tr><tr><td colspan="2" rowspan="1">Number of internaltamper events</td><td colspan="1" rowspan="1">N/A</td><td colspan="1" rowspan="1">4</td><td colspan="1" rowspan="1">4</td><td colspan="1" rowspan="1">13</td><td colspan="1" rowspan="1">7</td><td colspan="1" rowspan="1">N/A</td><td colspan="1" rowspan="1">5</td><td colspan="1" rowspan="1">10</td><td colspan="1" rowspan="1">11</td><td colspan="1" rowspan="1">9</td><td colspan="1" rowspan="1">4</td><td colspan="1" rowspan="1">4</td><td colspan="1" rowspan="1">11</td><td colspan="1" rowspan="1">9</td></tr><tr><td colspan="2" rowspan="1">Number of externaltamper inputs</td><td colspan="1" rowspan="1">N/A</td><td colspan="1" rowspan="1">2</td><td colspan="1" rowspan="1">3</td><td colspan="1" rowspan="1">8 (11ppins)</td><td colspan="1" rowspan="1">3</td><td colspan="1" rowspan="1">3 (4)</td><td colspan="1" rowspan="1">8</td><td colspan="1" rowspan="1">7</td><td colspan="1" rowspan="1">8</td><td colspan="1" rowspan="1">5</td><td colspan="1" rowspan="1">3</td><td colspan="1" rowspan="1">5</td><td colspan="1" rowspan="1">8</td><td colspan="1" rowspan="1">6 (6 pins)</td></tr><tr><td colspan="2" rowspan="1">VBAT mode pins</td><td colspan="1" rowspan="1">N/A</td><td colspan="1" rowspan="1">N/A</td><td colspan="1" rowspan="1">N/A</td><td colspan="1" rowspan="1">TAMP_IN[8:1]N TAMP0UT 8:1.R TS,RT OUT1/2</td><td colspan="1" rowspan="1">RTC_TS.RTC_OUT1/2</td><td colspan="1" rowspan="1">RTC_TAMP1/2/3,RTC_TS,RTC_OUTforSTM32L441142..RTC_TS,R COUT1forSTM32L4P5/Q5</td><td colspan="1" rowspan="1">TAMP_IN1/213, TAMPOUT2</td><td colspan="1" rowspan="1">TAMP N14:1],TAMP_OUT 12:1],RTC OUT1RC</td><td colspan="1" rowspan="1">TAMP_IN[8:1],TAMP_OUT[8:1],RCTS,R TC_QUT1/-2</td><td colspan="1" rowspan="1">RTC_OUT1,TRTCTST AMP_IT5:1]</td><td colspan="1" rowspan="1">RTC_TS,RTCOU11</td><td colspan="1" rowspan="1">TAMP_IN[5:0], RTCTS,R C_OUT1</td><td colspan="1" rowspan="1">TAMP_IN[3:1],TAMP_OUT2, RTC_TS,R RTCOUT1/2</td><td colspan="1" rowspan="1">N/A</td></tr><tr><td colspan="2" rowspan="1">NOERASE mode</td><td colspan="1" rowspan="1">N/A</td><td colspan="1" rowspan="1">N/A</td><td colspan="1" rowspan="1">N/A</td><td colspan="1" rowspan="1">X</td><td colspan="1" rowspan="1">N/A</td><td colspan="1" rowspan="1">×</td><td colspan="1" rowspan="1">N/A</td><td colspan="1" rowspan="1">X</td><td colspan="1" rowspan="1">X</td><td colspan="1" rowspan="1">X</td><td colspan="1" rowspan="1">N/A</td><td colspan="1" rowspan="1">N/A</td><td colspan="1" rowspan="1">N/A</td><td colspan="1" rowspan="1">X</td></tr><tr><td colspan="1" rowspan="9">20</td><td colspan="2" rowspan="1">Active tamper</td><td colspan="1" rowspan="1">N/A</td><td colspan="1" rowspan="1">N/A</td><td colspan="1" rowspan="1">N/A</td><td colspan="1" rowspan="1">X</td><td colspan="1" rowspan="1">X</td><td colspan="1" rowspan="1">N/A</td><td colspan="1" rowspan="1">X</td><td colspan="1" rowspan="1">X</td><td colspan="1" rowspan="1">X</td><td colspan="1" rowspan="1">X</td><td colspan="1" rowspan="1">N/A</td><td colspan="1" rowspan="1">N/A</td><td colspan="1" rowspan="1">X</td><td colspan="1" rowspan="1">X</td></tr><tr><td colspan="2" rowspan="1">Monotonic counter</td><td colspan="1" rowspan="1">N/A</td><td colspan="1" rowspan="1">N/A</td><td colspan="1" rowspan="1">N/A</td><td colspan="1" rowspan="1">X</td><td colspan="1" rowspan="1">X</td><td colspan="1" rowspan="1">N/A</td><td colspan="1" rowspan="1">X</td><td colspan="1" rowspan="1">X</td><td colspan="1" rowspan="1">X</td><td colspan="1" rowspan="1">X</td><td colspan="1" rowspan="1">X</td><td colspan="1" rowspan="1">N/A</td><td colspan="1" rowspan="1">X</td><td colspan="1" rowspan="1">X</td></tr><tr><td colspan="1" rowspan="4">LP modeeffect onTAMP</td><td colspan="1" rowspan="1">Sleep</td><td colspan="1" rowspan="1">N/A</td><td colspan="13" rowspan="1">No effect</td></tr><tr><td colspan="1" rowspan="1">Stop</td><td colspan="1" rowspan="1">N/A</td><td colspan="13" rowspan="2">No effect except for filtered level detection and active tamper if clock source is not LSE or LSI</td></tr><tr><td colspan="1" rowspan="1">Standby</td><td colspan="1" rowspan="1">N/A</td></tr><tr><td colspan="1" rowspan="1">Shutdown</td><td colspan="1" rowspan="1">N/A</td><td colspan="2" rowspan="1">No effectexcpt forfiltered leveldetection andactive tamper ifclock source isot LSE</td><td colspan="1" rowspan="1">N/A</td><td colspan="3" rowspan="1">No effect except for filteredlevel detection and activetamper if clock source is notLSE</td><td colspan="1" rowspan="1">N/A</td><td colspan="5" rowspan="1">No effect except or filtered level detection an activetampe clocsource is not LSE</td><td colspan="1" rowspan="1">No effectexcpt forfiltered leveldetecionand actvetamper ifclock sourcei not LSEo  LS</td></tr><tr><td colspan="2" rowspan="1">SAES key storageprotection</td><td colspan="1" rowspan="1">N/A</td><td colspan="1" rowspan="1">N/A</td><td colspan="1" rowspan="1">N/A</td><td colspan="1" rowspan="1">X</td><td colspan="1" rowspan="1">N/A</td><td colspan="1" rowspan="1">N/A</td><td colspan="1" rowspan="1">N/A</td><td colspan="1" rowspan="1">X</td><td colspan="1" rowspan="1">X</td><td colspan="1" rowspan="1">X</td><td colspan="1" rowspan="1">N/A</td><td colspan="1" rowspan="1">N/A</td><td colspan="1" rowspan="1">N/A</td><td colspan="1" rowspan="1">X</td></tr><tr><td colspan="2" rowspan="1">Secure protectionmodes</td><td colspan="1" rowspan="1">N/A</td><td colspan="1" rowspan="1">N/A</td><td colspan="1" rowspan="1">N/A</td><td colspan="1" rowspan="1">X(6)</td><td colspan="1" rowspan="1">N/A</td><td colspan="1" rowspan="1">N/A</td><td colspan="1" rowspan="1">X</td><td colspan="1" rowspan="1">X</td><td colspan="1" rowspan="1">X</td><td colspan="1" rowspan="1">X</td><td colspan="1" rowspan="1">N/A</td><td colspan="1" rowspan="1">N/A</td><td colspan="1" rowspan="1">N/A</td><td colspan="1" rowspan="1">X</td></tr><tr><td colspan="2" rowspan="1">Privileged protectionmode</td><td colspan="1" rowspan="1">N/A</td><td colspan="1" rowspan="1">N/A</td><td colspan="1" rowspan="1">N/A</td><td colspan="1" rowspan="1">X(6)</td><td colspan="1" rowspan="1">N/A</td><td colspan="1" rowspan="1">N/A</td><td colspan="1" rowspan="1">X</td><td colspan="1" rowspan="1">X</td><td colspan="1" rowspan="1">X</td><td colspan="1" rowspan="1">X</td><td colspan="1" rowspan="1">N/A</td><td colspan="1" rowspan="1">N/A</td><td colspan="1" rowspan="1">N/A</td><td colspan="1" rowspan="1">X</td></tr><tr><td colspan="1" rowspan="6">2</td><td colspan="2" rowspan="1">Configurable inputmapping</td><td colspan="1" rowspan="1">X</td><td colspan="1" rowspan="1">X</td><td colspan="1" rowspan="1">X</td><td colspan="1" rowspan="1">X</td><td colspan="1" rowspan="1">X</td><td colspan="1" rowspan="1">X</td><td colspan="1" rowspan="1">X</td><td colspan="1" rowspan="1">X</td><td colspan="1" rowspan="1">X</td><td colspan="1" rowspan="1">X</td><td colspan="1" rowspan="1">X</td><td colspan="1" rowspan="1">X</td><td colspan="1" rowspan="1">X</td><td colspan="1" rowspan="1">X</td></tr><tr><td colspan="1" rowspan="1">Time</td><td colspan="1" rowspan="1">Hour,minute,second</td><td colspan="1" rowspan="1">X</td><td colspan="1" rowspan="1">X</td><td colspan="1" rowspan="1">X</td><td colspan="1" rowspan="1">X</td><td colspan="1" rowspan="1">X</td><td colspan="1" rowspan="1">X</td><td colspan="1" rowspan="1">X</td><td colspan="1" rowspan="1">X</td><td colspan="1" rowspan="1">X</td><td colspan="1" rowspan="1">X</td><td colspan="1" rowspan="1">X</td><td colspan="1" rowspan="1">X</td><td colspan="1" rowspan="1">X</td><td colspan="1" rowspan="1">X</td></tr><tr><td colspan="1" rowspan="1"></td><td colspan="1" rowspan="1">Subsecond</td><td colspan="1" rowspan="1">X</td><td colspan="1" rowspan="1">X</td><td colspan="1" rowspan="1">X</td><td colspan="1" rowspan="1">X</td><td colspan="1" rowspan="1">X</td><td colspan="1" rowspan="1">X</td><td colspan="1" rowspan="1">X</td><td colspan="1" rowspan="1">X</td><td colspan="1" rowspan="1">X</td><td colspan="1" rowspan="1">X</td><td colspan="1" rowspan="1">X</td><td colspan="1" rowspan="1">X</td><td colspan="1" rowspan="1">X</td><td colspan="1" rowspan="1">X</td></tr><tr><td colspan="2" rowspan="1">Date (day, month)</td><td colspan="1" rowspan="1">X</td><td colspan="1" rowspan="1">X</td><td colspan="1" rowspan="1">X</td><td colspan="1" rowspan="1">X</td><td colspan="1" rowspan="1">X</td><td colspan="1" rowspan="1">X</td><td colspan="1" rowspan="1">X</td><td colspan="1" rowspan="1">X</td><td colspan="1" rowspan="1">X</td><td colspan="1" rowspan="1">X</td><td colspan="1" rowspan="1">X</td><td colspan="1" rowspan="1">X</td><td colspan="1" rowspan="1">X</td><td colspan="1" rowspan="1">X</td></tr><tr><td colspan="2" rowspan="1">Timestamp on tamperdetection event</td><td colspan="1" rowspan="1">N/A</td><td colspan="1" rowspan="1">X</td><td colspan="1" rowspan="1">X</td><td colspan="1" rowspan="1">X</td><td colspan="1" rowspan="1">X</td><td colspan="1" rowspan="1">X</td><td colspan="1" rowspan="1">X</td><td colspan="1" rowspan="1">X</td><td colspan="1" rowspan="1">X</td><td colspan="1" rowspan="1">X</td><td colspan="1" rowspan="1">X</td><td colspan="1" rowspan="1">X</td><td colspan="1" rowspan="1">X</td><td colspan="1" rowspan="1">X</td></tr><tr><td colspan="1" rowspan="1">Timestamp on switchto VBAT mode</td><td colspan="1" rowspan="1">Timestamp on switchto VBAT mode</td><td colspan="1" rowspan="1">N/A</td><td colspan="1" rowspan="1">X</td><td colspan="1" rowspan="1">X</td><td colspan="1" rowspan="1">X</td><td colspan="1" rowspan="1">X</td><td colspan="1" rowspan="1">X</td><td colspan="1" rowspan="1">X</td><td colspan="1" rowspan="1">X</td><td colspan="1" rowspan="1">X</td><td colspan="1" rowspan="1">X</td><td colspan="1" rowspan="1">X</td><td colspan="1" rowspan="1">X</td><td colspan="1" rowspan="1">X</td><td colspan="1" rowspan="1">N/A</td></tr><tr><td colspan="1" rowspan="2">Wun dnexen</td><td colspan="1" rowspan="1">Clock source available</td><td colspan="1" rowspan="1">Clock source available</td><td colspan="1" rowspan="1">N/A</td><td colspan="1" rowspan="1"></td><td colspan="1" rowspan="1"></td><td colspan="1" rowspan="1"></td><td colspan="1" rowspan="1"></td><td colspan="1" rowspan="1">RTC clo</td><td colspan="1" rowspan="1">k divided</td><td colspan="1" rowspan="1">by 2, 4,</td><td colspan="3" rowspan="1">RTC clock divided by 2, 4, 8, 16 or RTC synchronous prescaler output</td><td colspan="2" rowspan="1"></td><td colspan="1" rowspan="1"></td></tr><tr><td colspan="2" rowspan="1">Hardware automaticflag clearing</td><td colspan="1" rowspan="1">N/A</td><td colspan="1" rowspan="1">N/A</td><td colspan="1" rowspan="1">N/A</td><td colspan="1" rowspan="1">X</td><td colspan="1" rowspan="1">N/A</td><td colspan="1" rowspan="1">X</td><td colspan="1" rowspan="1">X</td><td colspan="1" rowspan="1">X</td><td colspan="1" rowspan="1">X</td><td colspan="1" rowspan="1">X</td><td colspan="1" rowspan="1">X</td><td colspan="1" rowspan="1">X</td><td colspan="1" rowspan="1">X</td><td colspan="1" rowspan="1">X</td></tr><tr><td colspan="1" rowspan="6">20</td><td colspan="2" rowspan="1">Number of outputs</td><td colspan="1" rowspan="1">2</td><td colspan="1" rowspan="1">2</td><td colspan="1" rowspan="1">2</td><td colspan="1" rowspan="1">2</td><td colspan="1" rowspan="1">2</td><td colspan="1" rowspan="1">2</td><td colspan="1" rowspan="1">2</td><td colspan="1" rowspan="1">2</td><td colspan="1" rowspan="1">2</td><td colspan="1" rowspan="1">X</td><td colspan="1" rowspan="1">2</td><td colspan="1" rowspan="1">2</td><td colspan="1" rowspan="1">2</td><td colspan="1" rowspan="1">2</td></tr><tr><td colspan="1" rowspan="3">AARM </td><td colspan="1" rowspan="1">Alarmevent</td><td colspan="1" rowspan="1">X</td><td colspan="1" rowspan="1">X</td><td colspan="1" rowspan="1">X</td><td colspan="1" rowspan="1">X</td><td colspan="1" rowspan="1">X</td><td colspan="1" rowspan="1">X</td><td colspan="1" rowspan="1">X</td><td colspan="1" rowspan="1">X</td><td colspan="1" rowspan="1">X</td><td colspan="1" rowspan="1">X</td><td colspan="1" rowspan="1">X</td><td colspan="1" rowspan="1">X</td><td colspan="1" rowspan="1">X</td><td colspan="1" rowspan="1">X</td></tr><tr><td colspan="1" rowspan="1">Wakeupevent</td><td colspan="1" rowspan="1">N/A</td><td colspan="1" rowspan="1">X</td><td colspan="1" rowspan="1">X</td><td colspan="1" rowspan="1">X</td><td colspan="1" rowspan="1">X</td><td colspan="1" rowspan="1">X</td><td colspan="1" rowspan="1">X</td><td colspan="1" rowspan="1">X</td><td colspan="1" rowspan="1">X</td><td colspan="1" rowspan="1">X</td><td colspan="1" rowspan="1">X</td><td colspan="1" rowspan="1">X</td><td colspan="1" rowspan="1">X</td><td colspan="1" rowspan="1">X</td></tr><tr><td colspan="1" rowspan="1">Tampervent</td><td colspan="1" rowspan="1">N/A</td><td colspan="1" rowspan="1">X</td><td colspan="1" rowspan="1">X</td><td colspan="1" rowspan="1">X</td><td colspan="1" rowspan="1">X</td><td colspan="1" rowspan="1">X</td><td colspan="1" rowspan="1">X</td><td colspan="1" rowspan="1">X</td><td colspan="1" rowspan="1">X</td><td colspan="1" rowspan="1">X</td><td colspan="1" rowspan="1">X</td><td colspan="1" rowspan="1">X</td><td colspan="1" rowspan="1">X</td><td colspan="1" rowspan="1">X</td></tr><tr><td colspan="1" rowspan="2">CALIB</td><td colspan="1" rowspan="1">512 Hz</td><td colspan="1" rowspan="1">X</td><td colspan="1" rowspan="1">X</td><td colspan="1" rowspan="1">X</td><td colspan="1" rowspan="1">X</td><td colspan="1" rowspan="1">X</td><td colspan="1" rowspan="1">X</td><td colspan="1" rowspan="1">X</td><td colspan="1" rowspan="1">X</td><td colspan="1" rowspan="1">X</td><td colspan="1" rowspan="1">X</td><td colspan="1" rowspan="1">X</td><td colspan="1" rowspan="1">X</td><td colspan="1" rowspan="1">X</td><td colspan="1" rowspan="1">X</td></tr><tr><td colspan="1" rowspan="1">1 Hz</td><td colspan="1" rowspan="1">X</td><td colspan="1" rowspan="1">X</td><td colspan="1" rowspan="1">X</td><td colspan="1" rowspan="1">X</td><td colspan="1" rowspan="1">X</td><td colspan="1" rowspan="1">X</td><td colspan="1" rowspan="1">X</td><td colspan="1" rowspan="1">X</td><td colspan="1" rowspan="1">X</td><td colspan="1" rowspan="1">X</td><td colspan="1" rowspan="1">X</td><td colspan="1" rowspan="1">X</td><td colspan="1" rowspan="1">X</td><td colspan="1" rowspan="1">X</td></tr><tr><td colspan="1" rowspan="2">20</td><td colspan="2" rowspan="1">Smooth calibration</td><td colspan="1" rowspan="1">X</td><td colspan="1" rowspan="1">X</td><td colspan="1" rowspan="1">X</td><td colspan="1" rowspan="1">X</td><td colspan="1" rowspan="1">X</td><td colspan="1" rowspan="1">X</td><td colspan="1" rowspan="1">X</td><td colspan="1" rowspan="1">X</td><td colspan="1" rowspan="1">X</td><td colspan="1" rowspan="1">X</td><td colspan="1" rowspan="1">X</td><td colspan="1" rowspan="1">X</td><td colspan="1" rowspan="1">X</td><td colspan="1" rowspan="1">X</td></tr><tr><td colspan="2" rowspan="1">Ultra-low-power mode</td><td colspan="1" rowspan="1">N/A</td><td colspan="1" rowspan="1">N/A</td><td colspan="1" rowspan="1">N/A</td><td colspan="1" rowspan="1">X</td><td colspan="1" rowspan="1">N/A</td><td colspan="1" rowspan="1">X</td><td colspan="1" rowspan="1">X</td><td colspan="1" rowspan="1">X</td><td colspan="1" rowspan="1">X</td><td colspan="1" rowspan="1">X</td><td colspan="1" rowspan="1">X</td><td colspan="1" rowspan="1">X</td><td colspan="1" rowspan="1">N/A</td><td colspan="1" rowspan="1">X</td></tr><tr><td colspan="1" rowspan="1"></td><td colspan="2" rowspan="1">RTC synchronization</td><td colspan="1" rowspan="1">X</td><td colspan="1" rowspan="1">X</td><td colspan="1" rowspan="1">X</td><td colspan="1" rowspan="1">X</td><td colspan="1" rowspan="1">X</td><td colspan="1" rowspan="1">X</td><td colspan="1" rowspan="1">X</td><td colspan="1" rowspan="1">X</td><td colspan="1" rowspan="1">X</td><td colspan="1" rowspan="1">X</td><td colspan="1" rowspan="1">X</td><td colspan="1" rowspan="1">X</td><td colspan="1" rowspan="1">X</td><td colspan="1" rowspan="1">X</td></tr><tr><td colspan="1" rowspan="1">Re</td><td colspan="2" rowspan="1">Reference clock detection</td><td colspan="1" rowspan="1">×</td><td colspan="1" rowspan="1">X</td><td colspan="1" rowspan="1">X</td><td colspan="1" rowspan="1">X</td><td colspan="1" rowspan="1">X</td><td colspan="1" rowspan="1">X</td><td colspan="1" rowspan="1">X</td><td colspan="1" rowspan="1">X</td><td colspan="1" rowspan="1">X</td><td colspan="1" rowspan="1">X</td><td colspan="1" rowspan="1">X</td><td colspan="1" rowspan="1">X</td><td colspan="1" rowspan="1">X</td><td colspan="1" rowspan="1">X</td></tr><tr><td colspan="1" rowspan="3">20</td><td colspan="2" rowspan="1">Powered on VBAT</td><td colspan="1" rowspan="1">N/A</td><td colspan="1" rowspan="1">X</td><td colspan="1" rowspan="1">X</td><td colspan="1" rowspan="1">X</td><td colspan="1" rowspan="1">X</td><td colspan="1" rowspan="1">X</td><td colspan="1" rowspan="1">X</td><td colspan="1" rowspan="1">X</td><td colspan="1" rowspan="1">X</td><td colspan="1" rowspan="1">X</td><td colspan="1" rowspan="1">X</td><td colspan="1" rowspan="1">X</td><td colspan="1" rowspan="1">X</td><td colspan="1" rowspan="1">N/A</td></tr><tr><td colspan="2" rowspan="1">Reset on a tamperdetection</td><td colspan="1" rowspan="1">N/A</td><td colspan="1" rowspan="1">X</td><td colspan="1" rowspan="1">X</td><td colspan="1" rowspan="1">X</td><td colspan="1" rowspan="1">X</td><td colspan="1" rowspan="1">X</td><td colspan="1" rowspan="1">X</td><td colspan="1" rowspan="1">X</td><td colspan="1" rowspan="1">X</td><td colspan="1" rowspan="1">X</td><td colspan="1" rowspan="1">X</td><td colspan="1" rowspan="1">X</td><td colspan="1" rowspan="1">X</td><td colspan="1" rowspan="1">X</td></tr><tr><td colspan="2" rowspan="1">Reset when flashmemory readoutprotection is disabled</td><td colspan="1" rowspan="1">N/A</td><td colspan="1" rowspan="1">X</td><td colspan="1" rowspan="1">X</td><td colspan="1" rowspan="1">X</td><td colspan="1" rowspan="1">X</td><td colspan="1" rowspan="1">X</td><td colspan="1" rowspan="1">X</td><td colspan="1" rowspan="1">X</td><td colspan="1" rowspan="1">X</td><td colspan="1" rowspan="1">X</td><td colspan="1" rowspan="1">X</td><td colspan="1" rowspan="1">X</td><td colspan="1" rowspan="1">X</td><td colspan="1" rowspan="1">X</td></tr><tr><td colspan="2" rowspan="1">Features</td><td colspan="1" rowspan="1">2</td><td colspan="1" rowspan="1">2</td><td colspan="1" rowspan="1">2</td><td colspan="1" rowspan="1">STMS</td><td colspan="1" rowspan="1">2</td><td colspan="1" rowspan="1">2010</td><td colspan="1" rowspan="1"></td><td colspan="1" rowspan="1">20</td><td colspan="1" rowspan="1">2</td><td colspan="1" rowspan="1">20</td><td colspan="1" rowspan="1">STMWM</td><td colspan="1" rowspan="1">2</td><td colspan="1" rowspan="1">20</td><td colspan="1" rowspan="1">N</td></tr><tr><td colspan="1" rowspan="1">seete yg</td><td colspan="1" rowspan="1">Number of backupregisters (size in bits)</td><td colspan="1" rowspan="1">4 (32)P())</td><td colspan="1" rowspan="1">5 (32)</td><td colspan="1" rowspan="1">320(32)(5)</td><td colspan="1" rowspan="1">32 (32)</td><td colspan="1" rowspan="1">$32 2</td><td colspan="1" rowspan="1">32 (32)</td><td colspan="1" rowspan="1">$32</td><td colspan="1" rowspan="1">32 2</td><td colspan="1" rowspan="1">32 (32)</td><td colspan="1" rowspan="1">32 (32)</td><td colspan="1" rowspan="1">20 (32)</td><td colspan="1" rowspan="1">9 (32)</td><td colspan="1" rowspan="1">32 (32)</td><td colspan="2" rowspan="1">32 (32)</td></tr><tr><td colspan="1" rowspan="4">20</td><td colspan="1" rowspan="1">Sleep</td><td colspan="1" rowspan="1">RTC in- terruptsmy exitmay de</td><td colspan="10" rowspan="1">No effect</td><td colspan="4" rowspan="1">No effect; RTC interrupts may exit Sleepmode</td></tr><tr><td colspan="1" rowspan="1">Stop</td><td colspan="1" rowspan="1">Active ifR ic cllockedBO LSE </td><td colspan="14" rowspan="2">Active if RTC is clocked by LSE or LSI</td></tr><tr><td colspan="1" rowspan="1">Standby</td><td colspan="2" rowspan="1">RTCpowereddownai and musted</td></tr><tr><td colspan="1" rowspan="1">Shutdown</td><td colspan="1" rowspan="1">N/A</td><td colspan="2" rowspan="1">Active if RTC isclook by LSE</td><td colspan="1" rowspan="1">N/A</td><td colspan="3" rowspan="1">Active if RTC is clocked byLSE</td><td colspan="1" rowspan="1">N/A</td><td colspan="3" rowspan="1">Active if RTC is clocked by LSE</td><td colspan="1" rowspan="1">N/A</td><td colspan="1" rowspan="1">Active ifRTCiclocked byLSE</td><td colspan="2" rowspan="1">N/A</td></tr><tr><td colspan="2" rowspan="1">RTC secure protection mode</td><td colspan="1" rowspan="1">N/A</td><td colspan="1" rowspan="1">N/A</td><td colspan="1" rowspan="1">N/A</td><td colspan="1" rowspan="1">$x()</td><td colspan="1" rowspan="1">N/A</td><td colspan="1" rowspan="1">N/A</td><td colspan="1" rowspan="1">X</td><td colspan="1" rowspan="1">X</td><td colspan="1" rowspan="1">X</td><td colspan="1" rowspan="1">X</td><td colspan="1" rowspan="1">N/A</td><td colspan="1" rowspan="1">N/A</td><td colspan="1" rowspan="1">N/A</td><td colspan="1" rowspan="1">X</td></tr><tr><td colspan="2" rowspan="1">RTC privilege protectionmode</td><td colspan="1" rowspan="1">N/A</td><td colspan="1" rowspan="1">N/A</td><td colspan="1" rowspan="1">N/A</td><td colspan="1" rowspan="1">X(6)</td><td colspan="1" rowspan="1">N/A</td><td colspan="1" rowspan="1">N/A</td><td colspan="1" rowspan="1">X</td><td colspan="1" rowspan="1">X</td><td colspan="1" rowspan="1">X</td><td colspan="1" rowspan="1">X</td><td colspan="1" rowspan="1">N/A</td><td colspan="1" rowspan="1">N/A</td><td colspan="1" rowspan="1">X</td><td colspan="1" rowspan="1">X</td></tr></table>

1. Erasing part of SRAM is also possible. 2. Erasing of part of SRAM, caches and cryptographic registers is also possible. 3. Filtering, sampling and precharge configuration, internal pull-up. 4. Only two for STM32L4 devices. 5. Depends on device category. 6. This feature is not available for STM32H503.

# 2.1

# RTC calendar

A calendar keeps track o the time (hours, minutes and seconds) and date (day, week, month, year. The RTC calendar offers the following features to easily configure and display the calendar data fields:

Calendar with subseconds (not programmable), seconds, minutes, hours (12 h/24 h format), day of the   
week (day), day of the month (date), month, year   
Calendar in BCD format   
Automatic management of 28-, 29- (leap year), 30-, and 31-day months   
Daylight saving time adjustment programmable by software

![](images/4e77b6cb5a7dd4a4c335f4fac2056eac77f82458f6e8d340e1eb06bd9cd970d4.jpg)  
Figure 1. RTC calendar fields   
I

# 2.1.1

# Software calendar

Asotware calenda is software counter (sually 32-it long) that represents henumberseconds. The This data can be converted to BCD format and displayed on a standard LCD. Conversion routines use a significant program memory space and are CPU-time consuming, that may be critical in certain real-time applications.

# 2.1.2 RTC hardware calendar

Whsale in ut  oe ehc performed by hardware.

The STM32 RTC calendar is provided in BCD format. This avoids binary to BCD software conversion routines, that save system resources.

![](images/921e4c90cbd0e18ec4320d6c1d976a6062f1fd007601b4f07e249e137021e006.jpg)  
Figure 2. Example of calendar displayed on an LCD

# 2.1.3 Initialize the calendar

the table below describes the steps required to correctly configure the calendar time and date.

Table 6. Steps to initialize the calendar   

<table><tr><td rowspan=1 colspan=1>Step</td><td rowspan=1 colspan=1>What</td><td rowspan=1 colspan=1>How</td><td rowspan=1 colspan=1>Comments</td></tr><tr><td rowspan=1 colspan=1>1</td><td rowspan=1 colspan=1>Disable the RTC registers writeprotection.</td><td rowspan=1 colspan=1>Write 0xCA and then 0x53 intoRTC_WPR.</td><td rowspan=1 colspan=1>RTC registers can be modified.</td></tr><tr><td rowspan=1 colspan=1>2</td><td rowspan=1 colspan=1>Enter initialization mode.</td><td rowspan=1 colspan=1>Set INIT = 1 in RTC_ISR (RTC2)RTC_ICSR (RTC3) register</td><td rowspan=1 colspan=1>The calendar counter is stopped to allow its update.</td></tr><tr><td rowspan=1 colspan=1>3</td><td rowspan=1 colspan=1>Wait for the confirmation ofinitialization mode (clocksynchronization).</td><td rowspan=1 colspan=1>Poll INITF bit of in RTC_ISR (RTC2)/RTC_ICSR (RTC3) until it is set.</td><td rowspan=1 colspan=1>For RTC2: It takes around two RTCCLK clockcycles due to clock synchronization.For RTC3: If LPCAL = 0, INITF is set aroundtwo RTCLK cycles after INIT is set. IfLPCAL = 1, INITF is set up to two ck_aprecycles after INIT is set.</td></tr><tr><td rowspan=1 colspan=1>4</td><td rowspan=1 colspan=1>Program the prescaler values(if needed).</td><td rowspan=1 colspan=1>In RTC_PRER, write first the synchronousvalue, and then write the asynchronousvalue.For RTC3, program also BIN and BCDU inRTC_ICSR, if in binary or mixed mode.</td><td rowspan=1 colspan=1>By default (in BCD mode for RTC3), RTC_PRER isinitialized to provide 1 Hz to the calendar unit (whenRTCCLK = 32768 Hz).</td></tr><tr><td rowspan=1 colspan=1>5</td><td rowspan=1 colspan=1>Load time and date values inthe shadow registers.</td><td rowspan=1 colspan=1>Set RTC_TR and RTC_DR.</td><td rowspan=1 colspan=1></td></tr><tr><td rowspan=1 colspan=1>6</td><td rowspan=1 colspan=1>Configure the time format(12 h or 24 h)</td><td rowspan=1 colspan=1>Set FMT bit in RTC_CR.</td><td rowspan=1 colspan=1>If FMT = 0, the format is 24 hour/day.If FMT = 1, the format is 12 h am/pm.</td></tr><tr><td rowspan=1 colspan=1>7</td><td rowspan=1 colspan=1>Exit initialization mode.</td><td rowspan=1 colspan=1>Clear INIT in RTC_ISR (RTC2))RTC_ICSR (RTC3).</td><td rowspan=1 colspan=1>For RTC2: The current calendar counter isautomatically loaded and the counting restarts afterfour RTCCLK clock cycles.For RTC3: If LPCAL = 0, the counting restarts afterfour RTCCLK clock cycles. If LPCAL = 1, thecounting restarts after up to two RTCCLK +1 ck_apre cycles.</td></tr><tr><td rowspan=1 colspan=1>8</td><td rowspan=1 colspan=1>Enable write protection of theRTC registers.</td><td rowspan=1 colspan=1>Write OxFF into RTC_WPR.</td><td rowspan=1 colspan=1>The RTC registers can no longer be modified.</td></tr></table>

# 2.1.4 RTC clock configuration

# RTC clock source

The RTC calendar can be driven by one of three possible clock sources LSE, LSI or HSE.

I   us  n its possible values and configurations.

Morover, tehoicf theRTC cloc ourc  ne hanks  heCL:0] i  RCC egiser.Thi e depends on the product and this information can also be found in the product reference manual.

# How to adjust the RTC calendar clock

TheRTC eatures seveal precalers hatllw elivering   Hz clock o the alendar  egardless  e clock source.

For heTC type he BCDi mod  ser. In bia modevalable nly RTC3), e c is not functional.

Calendar unit   
RTC Asynchronous Synchronous   
clock prescaler prescaler PREDIV_A PREDIV_S ck_spre Shadow Asynchronous Synchronous registers 7-bit prescaler 13-bit presecaler (RTC_TR and (default: 128) (default: 256) RTCDR)

# Important:

Thecalendar unit is liked tockspre but belongs to theckapre asynchronos prescale) clock domai. The choice of ck_apre can help to optimize power consumption.

The formula to calculate ck_spre is:

![](images/ff1dd73a4c27549eaf8621333a6d77d5867317c102ba18e9385f47107f87ab1e.jpg)

# where:

RTCCLK is any clock source (HSE_RTC, LSE or LSI).   
PREDIV_A is any number from 1 to 127.   
PREDIV_S is any number from 0 to 32767.

The table below shows several ways to obtain the calendar clock ck_spre = 1 Hz.

Other PREDIV_A[6:0]/PREDIV_S[14:0] values are possible. The user must always prefer the combination where PREDIV_A[6:0] is the highest for the needed accuracy and for lower consumption.

Figure 3. Prescalers from RTC clock source to calendar unit   
Table 7. Calendar clock ck_spre= 1 Hz with various clock source   

<table><tr><td rowspan=2 colspan=1>RTCCLK clock source</td><td rowspan=1 colspan=2>Prescalers</td></tr><tr><td rowspan=1 colspan=1>PREDIV_A[6:0]</td><td rowspan=1 colspan=1>PREDIV_S[14:0]</td></tr><tr><td rowspan=1 colspan=1>HSE_RTC = 1 MHz</td><td rowspan=1 colspan=1>124 (div 125)</td><td rowspan=1 colspan=1>799 (div 8000)</td></tr><tr><td rowspan=1 colspan=1>LSE = 32.768 kHz</td><td rowspan=1 colspan=1>127 (div 128)</td><td rowspan=1 colspan=1>255 (div 256)</td></tr><tr><td rowspan=1 colspan=1>LSI = 32 kHz</td><td rowspan=1 colspan=1>127 (div 128)</td><td rowspan=1 colspan=1>249 (div 250)</td></tr><tr><td rowspan=1 colspan=1>LSI = 37 kHz</td><td rowspan=1 colspan=1>124 (div 125)</td><td rowspan=1 colspan=1>295 (div 296)</td></tr><tr><td rowspan=1 colspan=1>LSI = 40 kHz</td><td rowspan=1 colspan=1>127 (div 128)</td><td rowspan=1 colspan=1>311 (div 312)</td></tr></table>

# 2.1.5

# Calendar firmware examples

The ces wit a  eaple projet  hat heuser an quickly bece fmar with h perel Refer to the X-CUBE-RTC Expansion Package for a complete projects list.

or example, the user can find the following projects concerning calendar:

For the NUCLEO-L412RB-P equipped with an RTC3: STM32Cube_FW_L4_Vx.y.z\Projects\NUCLEO-L412RB-P|Examples|\RTCIRTC_Calendar STM32Cube_FW_L4_Vx.y.Zz\Projects|NUCLEO-L412RB-P|Examples_LLIRTC\RTC_Calendar • For the P-NUCLEO-WB55 equipped with an RTC2: STM32Cube_FW_WB_Vx.y.z\Projects|P-NUCLEO-WB55.Nucleol Examples_LLIRTC\RTC_Calendar_Init

If one example is not available in the X-CUBE-RTC for a given STM32 MCU, the user can adapt it.

# 2.2

# Binary and mixed modes (RTC3 only)

F RTC sub-second register (SSR) is extended to 32 bits (16 bits in normal mode) and is used as a binary downcounter.

T fo heheT aurn BCD--avionoee (whe ui b pl).

The binary mode implementation is simple:

Initialization: Set INIT = 1 in RTC_ICSR and wait for INITF to be set.   
2. Define the asynchronous prescaler value in RTC_PRER to clock the binary counter.   
3. Set BIN[1:0] = 01 in RTC_ICSR: the RTC_SSR register is initialized to OxFFFF FFFF.   
zT  .   
The counte is clocked by theRTC asynchronos prescaleroutput When it reaches , it is reloade with 0xFFFF FFFF.

In binary mode, the RTC_ALRABINR register is used to program the subsecond field of the alarm.

The mie mode alsooffered by RTC typeallows both the32-bi biary down-counterand the BCD calenr. In this mode, the user can choose when the calendar is incremented by  second with BCDU[2:0] in RTC_ICSR. T  oa s nt o   e e be incremented by 1 second.

A shadow register exists for RTC_SSR. It can be bypassed when BYPSHAD = 1 in RTCCR. See Section 2.13.3 for more details on BYPSHAD use and associated cautions to take.

# 2.3 RTC alarms

# 2.3.1

# RTC alarm configuration

Tembes two equivalent alarms:alar A and alar B.An alar can e generated at a given timen dat programmed bythe user. The RT provides a rihcombination alarm settings, and offs many fatres to make them easy to configure and display.

Each alarm unit provides the following features:

Fully programmable alarm: subsecond, second, minute, hour and date fields can be independently selected or masked to provide a rich combination of alarms.   
The device can be wake up from low-power modes when the alarm occurs.   
The alarm event can be routed to a specific output pin with configurable polarity.   
Dedicated alarm flags and interrupt are available.

![](images/16080223dcd895ebbe86297dcb8d85deca52ef1f3158b8a9d2c8aaeef5558828.jpg)  
Figure 4. Alarm A fields   
otes: . Sames fields are available in RTC_ALRMAR and RTC_ALRMBR registers. . Sames fields are available in RTC_ALRMASSR and RTC_ARRMBSSR registers. s  CRMARs.CRBR    e/ CRMAR CRMB. . Mask ss bits are available in RTC_ALRMASSR and RTC_ALRMBSSR.

T on the RTCTR time register, or easier software anipulation. When the RTC time counter reaches the value programmed in the alarm register, a flag is set to indicate that an alarm event occurred (ALRAF-or-ALRBF-in-RTC_SR).

The RTC alarm can be configured by hardware to generate different types of alarms. For more details, refer to Table 9.

# 2.3.1.1 Program the alarm

The table below describes the steps required to configure alarm A.

Table 8. Steps to confirm alarm A   

<table><tr><td rowspan=1 colspan=1>Step</td><td rowspan=1 colspan=1>What</td><td rowspan=1 colspan=1>How</td><td rowspan=1 colspan=1>Comment</td></tr><tr><td rowspan=1 colspan=1>1</td><td rowspan=1 colspan=1>Disable write protection on RTC registers.</td><td rowspan=1 colspan=1>Write 0xCA and then 0x53 intoRTC_WPR.</td><td rowspan=1 colspan=1>The RTC registers can be modified.</td></tr><tr><td rowspan=1 colspan=1>2</td><td rowspan=1 colspan=1>Disable alarm A.</td><td rowspan=1 colspan=1>Clear ALRAE(1) in RTC_CR(2).</td><td rowspan=1 colspan=1></td></tr><tr><td rowspan=1 colspan=1>3(3)</td><td rowspan=1 colspan=1>Check that RTC_ALRMAR can beaccessed.</td><td rowspan=1 colspan=1>Poll ALRAWF(4) until it is set in RTC_ISR.</td><td rowspan=1 colspan=1>It takes around two RTCCLK clock cyclesdue to clock synchronization.</td></tr><tr><td rowspan=1 colspan=1>4</td><td rowspan=1 colspan=1>Configure the alarm.</td><td rowspan=1 colspan=1>Configure RTC_ALRMAR(5).</td><td rowspan=1 colspan=1>The alarm hour format must be thesame®) as the RTC calendar inRTC_ALRMAR(5).</td></tr><tr><td rowspan=1 colspan=1>5</td><td rowspan=1 colspan=1>Re-enable alarm A.</td><td rowspan=1 colspan=1>Set ALRAE(7) in RTC_CR.</td><td rowspan=1 colspan=1></td></tr><tr><td rowspan=1 colspan=1>6</td><td rowspan=1 colspan=1>Enable write protection on the RTCregisters.</td><td rowspan=1 colspan=1>Write OxFF into RTC_WPR.</td><td rowspan=1 colspan=1>The RTC registers can no longer bemodified.</td></tr></table>

1Respectively ALRBE for alarm B.

2. RTeTiz   
3. Only required for RTC2 type.   
4. Resp. ALRBWF for alarm B. ALRAWF and ALRBWF does not exist on RTC3 type.   
5. Respectively RTC_ALRMBR for alarm B.   
6.   
the RTC calendar is 24-hour format and the alarm is 12-hour format.   
7Respectively ALRBE for alarm B.

# Configure the alarm behavior using the MSKx bits

The alarm behavior can be configured using the MSKx bits (x = 1, 2, 3, 4) of RTC_ALRMAR for alarm A (RTC_ALRMBR for alarm B). The table below shows all possible alarm settings.

Table 9. Alarm combinations   

<table><tr><td colspan="1" rowspan="1">MSK4</td><td colspan="1" rowspan="1">MSK3</td><td colspan="1" rowspan="1">MSK2</td><td colspan="1" rowspan="1">MSK1</td><td colspan="1" rowspan="1">Alarm behavior</td></tr><tr><td colspan="1" rowspan="1">0</td><td colspan="1" rowspan="1">0</td><td colspan="1" rowspan="1">0</td><td colspan="1" rowspan="1">0</td><td colspan="1" rowspan="1">All fields are used in the alarm comparison.Example: the alarm occurs at 23:15:07, each Monday.</td></tr><tr><td colspan="1" rowspan="1">0</td><td colspan="1" rowspan="1">0</td><td colspan="1" rowspan="1">0</td><td colspan="1" rowspan="1">1</td><td colspan="1" rowspan="1">Seconds do not matter in the alarm comparison.Example: the alarm occurs every second of 23:15, each Monday.</td></tr><tr><td colspan="1" rowspan="1">0</td><td colspan="1" rowspan="1">0</td><td colspan="1" rowspan="1">1</td><td colspan="1" rowspan="1">0</td><td colspan="1" rowspan="1">Minutes do not matter in the alarm comparison.Example: the alarm occurs at the 7th second of every minute of 23:XX, each Monday.</td></tr><tr><td colspan="1" rowspan="1">0</td><td colspan="1" rowspan="1">0</td><td colspan="1" rowspan="1">1</td><td colspan="1" rowspan="1">1</td><td colspan="1" rowspan="1">Minutes and seconds do not matter in the alarm comparison.</td></tr><tr><td colspan="1" rowspan="1">0</td><td colspan="1" rowspan="1">1</td><td colspan="1" rowspan="1">0</td><td colspan="1" rowspan="1">0</td><td colspan="1" rowspan="1">Hours do not matter in the alarm comparison.</td></tr><tr><td colspan="1" rowspan="1">0</td><td colspan="1" rowspan="1">1</td><td colspan="1" rowspan="1">0</td><td colspan="1" rowspan="1">1</td><td colspan="1" rowspan="1">Hours and seconds do not matter in the alarm comparison.</td></tr><tr><td colspan="1" rowspan="1">0</td><td colspan="1" rowspan="1">1</td><td colspan="1" rowspan="1">1</td><td colspan="1" rowspan="1">0</td><td colspan="1" rowspan="1">Hours and minutes do not matter in the alarm comparison.</td></tr><tr><td colspan="1" rowspan="1">0</td><td colspan="1" rowspan="1">1</td><td colspan="1" rowspan="1">1</td><td colspan="1" rowspan="1">1</td><td colspan="1" rowspan="1">Hours, minutes and seconds do not matter in the alarm comparison.Example: the alarm is set every second, each Monday, during the whole day.</td></tr><tr><td colspan="1" rowspan="1"></td><td colspan="1" rowspan="1">0</td><td colspan="1" rowspan="1">0</td><td colspan="1" rowspan="1">0</td><td colspan="1" rowspan="1">Week day (or date, if selected) do not matter in the alarm comparison.Example: the alarm occurs althe days at 23:15:07.</td></tr><tr><td colspan="1" rowspan="1">1</td><td colspan="1" rowspan="1">0</td><td colspan="1" rowspan="1">0</td><td colspan="1" rowspan="1">1</td><td colspan="1" rowspan="1">Week day and seconds do not matter in the alarm comparison.</td></tr><tr><td colspan="1" rowspan="1">1</td><td colspan="1" rowspan="1">0</td><td colspan="1" rowspan="1">1</td><td colspan="1" rowspan="1">0</td><td colspan="1" rowspan="1">Week day and minutes do not matter in the alarm comparison.</td></tr><tr><td colspan="1" rowspan="1">1</td><td colspan="1" rowspan="1">0</td><td colspan="1" rowspan="1">1</td><td colspan="1" rowspan="1">1</td><td colspan="1" rowspan="1">Week day, minutes and seconds do not matter in the alarm comparison.</td></tr><tr><td colspan="1" rowspan="1">1</td><td colspan="1" rowspan="1">1</td><td colspan="1" rowspan="1">0</td><td colspan="1" rowspan="1">0</td><td colspan="1" rowspan="1">Week day and hours do not matter in the alarm comparison.</td></tr><tr><td colspan="1" rowspan="1">1</td><td colspan="1" rowspan="1">1</td><td colspan="1" rowspan="1">0</td><td colspan="1" rowspan="1">1</td><td colspan="1" rowspan="1">Week day, hours and seconds do not matter in the alarm comparison.</td></tr><tr><td colspan="1" rowspan="1"></td><td colspan="1" rowspan="1">1</td><td colspan="1" rowspan="1">1</td><td colspan="1" rowspan="1">0</td><td colspan="1" rowspan="1">Week day, hours and minutes do not matter in the alarm comparison.</td></tr><tr><td colspan="1" rowspan="1">1</td><td colspan="1" rowspan="1">1</td><td colspan="1" rowspan="1">1</td><td colspan="1" rowspan="1">1</td><td colspan="1" rowspan="1">The alarm occurs every second.</td></tr></table>

# Example

To configure the alarm time to 23:15:07 on Monday assuming WDSEL = 1, configure all MSKx to zero with DU[3:0] = 0001 (Monday), HT[1:0] = 10, HU[3:0] = 0011, MNT[2:0] = 001, MNU[3:0] = 0101, ST[2:0] = 000, SU[3:0] = 0111 (23:15:07), PM = 0 (24h format) in RTC_ALRMAR (resp. RTC_ALRMBR) .

When WDSEL = 0,an alaroccurs on the day number specifed in DT and DU bitfelds in RTCALRMxR, iste ay  the week.T get this alar ne a mon at ::0,  heay, RTCALRMxR bielt be st as followS: all MSKx = 0, WDSEL = 0, DT[1:0] = 01, DU[3:0] = 0100, HT[1:0] = 10, HU[3:0] = 0011, MNT[2:0] = 001, MNU[3:0] = 0101, ST[2:0] = 000, SU[3:0] = 0111, PM = 0.

# Caution:

If the second field is selected (MSK1 reset in RTC_ALRMAR or RTC_ALRMBR), the synchronous prescaler division factor PREDIV_S[14:0] (set in RTC_PRER) must be at least 3 to ensure a correct behavior.

# 2.3.2

# Alarm subsecond configuration

nly RTC3 type with BCD or mixed mode is considered in this section.

The RTC provides similar programmable alarms, subsecond A and B. They generate alarms with a high relution or he secondivision).Thevalue programmein thealar subsecon giste is compare the content of the subsecond field in the calendar unit.

T usecond  countcount ownfomealuconigurnenronou ecaler ea then reloads a value from RTC_SPRE.

![](images/d7d5912e74c147c3e54768fcefff506808f45ab42cec5b2c6f062df3e87dd290.jpg)  
Figure 5. Alarm subsecond field

# Note:

Massheos fint  nhesolarThs paheon rer. Mask  s-bit lngth (om 0 too T typeand can ep to-it length rom 0 to) RTC3 type (RTC_SSR always 16-bit length for RTC2 type, and can be expanded to 32 bits on some RTC3 type).

The subsecond alarm is configured using MASKSS[5:0] in RTC_ALRMASSR (resp. RTC_ALRMBSSR). The tab blohows e uratn psbilite ask g poide ampl wit settings:

LSE selected as RTC clock source (for example LSE = 32768 Hz) Asynchronous prescaler = 127 Synchronous prescaler = 255 (calendar clock = 1 Hz) Alarm A subsecond = 255 (SS[14:0] = 255)

Table 10. Alarm subsecond mask combinations (RTC2 type)   

<table><tr><td rowspan=1 colspan=1>MASKSS[5:0]</td><td rowspan=1 colspan=1>Alarm A subsecond behavior</td><td rowspan=1 colspan=1>Example result</td></tr><tr><td rowspan=1 colspan=1>0</td><td rowspan=1 colspan=1>No comparison on subsecond for alarmThe alarm is activated when the second unit is incremented.</td><td rowspan=1 colspan=1>Alarm activated every 1 s</td></tr><tr><td rowspan=1 colspan=1>1</td><td rowspan=1 colspan=1>Only the AlarmA_SS[0] bit is compared to RTC_SSR.</td><td rowspan=1 colspan=1>Alarm activated every 1/128 s</td></tr><tr><td rowspan=1 colspan=1>2</td><td rowspan=1 colspan=1>Only the AlarmA_SS[1:0] bits are compared to RTC_SSR.</td><td rowspan=1 colspan=1>Alarm activated every 1/64 s</td></tr><tr><td rowspan=1 colspan=1>3</td><td rowspan=1 colspan=1>Only the AlarmA_SS[2:0] bits are compared to RTC_SSR.</td><td rowspan=1 colspan=1>Alarm activated every 1/32 s</td></tr><tr><td rowspan=1 colspan=1>4</td><td rowspan=1 colspan=1>Only the AlarmA_SS[3:0] bits are compared to RTC_SSR.</td><td rowspan=1 colspan=1>Alarm activated every 1/16 s</td></tr><tr><td rowspan=1 colspan=1>5</td><td rowspan=1 colspan=1>Only the AlarmA_SS[4:0] bits are compared to RTC_SSR.</td><td rowspan=1 colspan=1>Alarm activated every 125 ms</td></tr><tr><td rowspan=1 colspan=1>6</td><td rowspan=1 colspan=1>Only the AlarmA_SS[5:0] bits are compared to RTC_SSR.</td><td rowspan=1 colspan=1>Alarm activated every 250 ms</td></tr><tr><td rowspan=1 colspan=1>7</td><td rowspan=1 colspan=1>Only the AlarmA_SS[6:0] bits are compared to RTC_SSR.</td><td rowspan=1 colspan=1>Alarm activated every 500 ms</td></tr><tr><td rowspan=1 colspan=1>8</td><td rowspan=1 colspan=1>Only the AlarmA_SS[7:0] bits are compared to RTC_SSR.</td><td rowspan=1 colspan=1>Alarm activated every 1 s</td></tr><tr><td rowspan=1 colspan=1>9</td><td rowspan=1 colspan=1>Only the AlarmA_SS[8:0] bits are compared to RTC_SSR.</td><td rowspan=1 colspan=1>Alarm activated every 1 s</td></tr><tr><td rowspan=1 colspan=1>10</td><td rowspan=1 colspan=1>Only the AlarmA_SS[9:0] bits are compared to RTC_SSR.</td><td rowspan=1 colspan=1>Alarm activated every 1 s</td></tr><tr><td rowspan=1 colspan=1>11</td><td rowspan=1 colspan=1>Only the AlarmA_SS[10:0] bits are compared to RTC_SSR.</td><td rowspan=1 colspan=1>Alarm activated every 1 s</td></tr><tr><td rowspan=1 colspan=1>12</td><td rowspan=1 colspan=1>Only the AlarmA_SS[11:0] bits are compared to RTC_SSR.</td><td rowspan=1 colspan=1>Alarm activated every 1 s</td></tr><tr><td rowspan=1 colspan=1>13</td><td rowspan=1 colspan=1>Only the AlarmA_SS[12:0] bits are compared to RTC_SSR.</td><td rowspan=1 colspan=1>Alarm activated every 1 s</td></tr><tr><td rowspan=1 colspan=1>14</td><td rowspan=1 colspan=1>Only the AlarmA_SS[13:0] bits are compared to RTC_SSR.</td><td rowspan=1 colspan=1>Alarm activated every 1 s</td></tr><tr><td rowspan=1 colspan=1>15</td><td rowspan=1 colspan=1>Only the AlarmA_SS[14:0] bits are compared to RTC_SSR.</td><td rowspan=1 colspan=1>Alarm activated every 1 s</td></tr></table>

# Note:

For RTC3 type, this table can be completed up to MASKSS equal to 31 and the SS[31:16] value is given by RTC_ALRÁBINR (resp. RTC_ALRBBINR).

The overflow bit in the subsecond register (bit 15 for RTC2 and 31 for RTC3) is never comparec

# 2.3.3 Alarm firmware examples

The ces wit   eaple projet  that heuse an quickl bece fmar with th pereal Refer to the X-CUBE-RTC Expansion Package for a complete projects list.

or example, the user can find the following projects concerning alarms:

For the NUCLEO-L412RB-P equipped with an RTC3:

STM32Cube_FW_L4_Vx.y.Z\Projects|NUCLEO-L412RB-P|Examples| RTCIRTC_Alarm STM32Cube_FW_L4_Vx.y.z\Projects\NUCLEO-L412RB-P|Examples_LLIRTC\RTC_Alarm STM32Cube_FW_L4_Vx.y.z\Projects|NUCLEO-L412RB-P|Examples_LLIRTCIRTC_Alarm_Init

f one example is not available in the X-CUBE-RTC for a given STM32 MCU, the user can adapt it.

# 2.4

# RTC periodic wakeup unit

The STM32 MCUs provide several low-power modes to reduce the power consumption. The RTC features a peas  wakup nithal  wakestfom owpowo programmable down-counting auto-reload timer. When this counter reaches zero, a flag and an interrupt (if enabled) are generated.

The wakeup unit has the following features:

Programmable down-counting auto-reload timer   
Specific flag and interrupt capable of waking up the device from low-power modes   
Wakeup alternate function output that can be routed to the RTC_ALARM output for RTC2 and the   
TAMPALRM output or RT3 nique pad or alarm A, alarm B or wakeup events) with configurable polarity   
Full set of prescalers to select the desired waiting period

# 2.4.1 Program the auto-wakeup unit

The table below describes the steps required to configure the auto-wakeup unit.

Table 11. Steps to configure the auto-wakeup unit   

<table><tr><td rowspan=1 colspan=1>Step</td><td rowspan=1 colspan=1>What</td><td rowspan=1 colspan=1>How</td><td rowspan=1 colspan=1>Comment</td></tr><tr><td rowspan=1 colspan=1>1</td><td rowspan=1 colspan=1>Disable write protection on RTCregisters.</td><td rowspan=1 colspan=1>Write 0xCA and then 0x53 intoRTC_WPR.</td><td rowspan=1 colspan=1>The RTC registers can be modified.</td></tr><tr><td rowspan=1 colspan=1>2</td><td rowspan=1 colspan=1>Disable the wakeup timer.</td><td rowspan=1 colspan=1>Clear WUTE bit in RTC_CR.</td><td rowspan=1 colspan=1></td></tr><tr><td rowspan=1 colspan=1>3</td><td rowspan=1 colspan=1>Ensure access to wakeup auto-reload counter and WUCKSEL[2:0]are allowed.</td><td rowspan=1 colspan=1>Poll WUTWF until it is set inRTC_ISR (RTC2))RTC_ICSR (RTC3)</td><td rowspan=1 colspan=1>For RTC2: It takes around two RTCCLK clockcycles due to clock synchronization.For RTC3(1):If WUCKSEL[2] = 0, WUTWF is set. It takesaround 1 ck_wut + 1 RTCCLK cycles afterWUTE is cleared.If WUCKSEL[2] = 1, WUTWF is set. It takesup to 1 ck_apre + 1 RTCCLK cycles afterWUTE is cleared.</td></tr><tr><td rowspan=1 colspan=1>4</td><td rowspan=1 colspan=1>Program the value into the wakeuptimer.</td><td rowspan=1 colspan=1>Set WUT[15:0] in RTC_WUTR.For RTC3, the user must alsoprogram WUTOCLR[15:0]2)inRT_WUCR</td><td rowspan=2 colspan=1>See Section 2.4.2: Maximum and minimum RTCwakeup period.</td></tr><tr><td rowspan=1 colspan=1>5</td><td rowspan=1 colspan=1>Select the desired clock source.</td><td rowspan=1 colspan=1>Program WUCKSEL[2:0] inTCR.</td></tr><tr><td rowspan=1 colspan=1>6</td><td rowspan=1 colspan=1>Re-enable the wakeup timer.</td><td rowspan=1 colspan=1>Set WUTE in RTC_CR.</td><td rowspan=1 colspan=1>The wakeup timer restarts counting down.</td></tr><tr><td rowspan=1 colspan=1>7</td><td rowspan=1 colspan=1>Enable write protection on RTCregisters.</td><td rowspan=1 colspan=1>Write OxFF into the RTC_WPR.</td><td rowspan=1 colspan=1>The RTC registers cannot be modified.</td></tr></table>

.

type, WUTF must always be cleared by software.

# 2.4.2

# Maximum and minimum RTC wakeup period

The wakeup unit clock is configured through WUCKSEL[2:0] in RTCCR. Three different configurations are possible:

Configuration 1: WUCKSEL[2:0] = 0xx for short wakeup periods (see Section 2.4.2.1) Configuration 2: WUCKSEL[2:0] = 10x for medium wakeup periods (see Section 2.4.2.2) Configuration 3: WUCkSEL[2:0] = 11x for long wakeup periods (see Section 2.4.2.3)

# 2.4.2.1

# Periodic timebase/wakeup configuration for clock configuration 1

The figure below shows the prescaler connection to the timebase/wakeup unit and the table below gives the timebase/wakeup clock resolutions corresponding to configuration 1.

The prescaler depends on the wakeup clock selection as follows:

WUCKSEL[2:0] =000: RTCCLK/16 clock selected WUCKSEL[2:0] =001: RTCCLK/8 clock selected WUCKSEL[2:0] =010: RTCCLK/4 clock selected WUCKSEL[2:0] =011: RTCCLK/2 clock selected

![](images/01d4ca6970f4377aee81c25ef9cb5bed57128b121bc730dd3fa6d11db20c82f3.jpg)  
Figure 6. Prescalers connected to the timebase/wakeup unit for configuration 1

Table 12. Timebase/wakeup unit period resolution with clock configuration 1   

<table><tr><td rowspan=2 colspan=1>Clock source</td><td rowspan=1 colspan=2>Wakeup period resolution</td></tr><tr><td rowspan=1 colspan=1>WUCKSEL[2:0] = 000 (div16)</td><td rowspan=1 colspan=1>WUCKSEL[2:0] = 011 (div2)</td></tr><tr><td rowspan=1 colspan=1>LSE = 32 768 Hz</td><td rowspan=1 colspan=1>488.28 μs</td><td rowspan=1 colspan=1>61.035 μs</td></tr></table>

When RTCCLK= 32768 Hz, the minimum timebase/wakeup resolution is 61.035 µs, and the maximum resolution is 488.28 µs. As a result:

The minimum timebase/wakeup period is (0x0001 + 1) x 61.035 µs = 122.07 µs. The timebase/wakeup timer counter WUT[15:0] cannot be set to 0x0000 with WUCKSEL[2:0] = 011 (cL/2) because this configuration is prohibited. Refer to the product reference manuals for more details. • The maximum timebase/wakeup period is (0xFFFF+ 1) x 488.28 µs = 32 s.

# 2.4.2.2

# Periodic timebase/wakeup configuration for clock configuration 2

The figure below shows the prescaler connection to the timebase/wakeup unit corresponding to configuration 2 and 3.

![](images/c7fe79406677776a9a366d1edc046bb96bdf98c9e2270ce51fa94f3e02da51fa.jpg)  
Figure 7. Prescalers connected to the wakeup unit for configurations 2 and 3

If ck_spre (synchronous prescaler output clock) is adjusted to 1 Hz, then: The minimum timebase/wakeup period is (0x0000 + 1) x 1 s = 1 s. The maximum timebase/wakeup period is (0xFFFF+ 1) x 1 s = 65536 s (18 hours).

# 2.4.2.3

# Periodic timebase/wakeup configuration for clock configuration 3

Fogrationouti guratiea/wak down counts starting from Ox1FFFF to 0x00000 (instead of OxFFFF to 0x0000 for configuration 2).

If ck_spre is adjusted to 1 Hz, then:

The minimum timebase/wakeup period is (0x10000 + 1) x 1 s = 65537 s (18 hours + 1 s).   
The maximum timebase/wakeup period is (0x1FFFF+ 1) x 1 s = 131072 s (36 hours).

# Note:

Inbinary ormied modes, ck_spre is replacd by the clock used to update the calendar (as defined by BCDU bits in RTC_ICSR). See Section 2.2 for more details on BCDU).

# 2.4.2.4

# Summary of timebase/wakeup period extrema

When RTCCLK= 32768 Hz and ck_spre (synchronous prescaler output clock) is adjusted to 1 Hz, theminimum and maximum period values are listed in the table below.

Table 13. Min. and max. timebase/wakeup period when RTCCLK= 32768   

<table><tr><td rowspan=1 colspan=1>Configuration</td><td rowspan=1 colspan=1>Minimum period</td><td rowspan=1 colspan=1>Maximum period</td></tr><tr><td rowspan=1 colspan=1>1</td><td rowspan=1 colspan=1>122.07 us</td><td rowspan=1 colspan=1>32 s</td></tr><tr><td rowspan=1 colspan=1>2</td><td rowspan=1 colspan=1>1s</td><td rowspan=1 colspan=1>18 hours</td></tr><tr><td rowspan=1 colspan=1>3</td><td rowspan=1 colspan=1>18 hours +1 s</td><td rowspan=1 colspan=1>36 hours</td></tr></table>

# 2.4.3

# Wakeup firmware example

The RC cmes with a et  example projects o that the usercan quickly become fmiiar with this peripheal.   
Refer to the X-CUBE-RTC Expansion Package for a complete projects list.

For example, the user can find the following projects concerning wakeup:

. For the NUCLEO-L412RB-P equipped with an RTC3: STM32Cube_FW_L4_Vx.y.z\Projects\NUCLEO-L412RB-P\Examples_LLIRTCIRTC_ExitStandbyWithWakeUpTimer   
. For the NUCLEO-G071RB equipped with an RTC3: STM32Cube_FW_G0_Vx.y.z\Projects\NUCLEO-G071RB|Examples_LLIRTCIRTC_ExitStandbyWithWakeUpTimer_Init For the NUCLEO-G431RB equipped with an RTC3: STM32Cube_FW_G4_Vx.y.z\Projects\NUCLEO-G431RB|Examples_LLIRTC\RTC_ProgrammingTheWakeUpTime

If one example is not available in the X-CUBE-RTC for a given STM32 MCU, the user can adapt it.

# 2.5

# Smooth digital calibration

# 2.5.1

# RTC calibration basics

TequeTe af supeaccrayversus therconvential cillatresis,but theyae ot per, s the qurtz crystals are sensitive to temperature variations. igure 8 shows the relationship between accuracy , temperature (T) and curvature (K) for a typical 32.768 kHz crystal, following the general formula:

![](images/72024226adfec1823c8a90250cbc3a496cb0b31e2e42d252cd9a660c494a530d.jpg)

where To = 25 ° ± 5 °C and K = -0.032 ppm/2.

# Note:

The Kvariable  crystal-dependent.Thevaluindicated here is or thecrystal mounted on theST32L47RG-Nucleo board. Refer to the crystal manufacturer for more details on this parameter.

Tcocumsplt qaevl cv achieving this accuracy.

Twmaoachexispesatilatinequencevationillator when signal is used to clock a time-keeping logic:

# Analog approach

Theollator built wih bedecapacitor bankon both input and utput fhescillato Tust the oscilation frequency, the software needs to configure the oscillator to switch on or o some o the embedded load capacitors to adjust the overall load capacitance seen by the crystal resonator. Note that the two external load capacitors are always needed even with this kind of osillators.The two external load capacitors make the dominant part of the load capacitance of the crystal resonator. The ocillator embedded capacitor banks are only intended to compensate for the capacitancevalue dispersion oe two external load capacitors; or to compensate or the temperature variation.This approach suffers from most of drawbacks that generally analog circuits suffer from, such as relatively important value dispersion from one chip to another.

# Digital approach

The osillation frequency deviation is not compensated at oscillator level. The compensation is made at time-keeping logic/function level. The time-keeping logic either adds or removes few clock cycles to/from the deviating clock signal that feeds itcounter. Themain advantage of thisapproach is thedetermistic compensation effect from one device to another. This approach is adopted to compensate the LSE oscillation frequency deviation when LSE is used to clock the RTC. The RTC is built with a dedicated register to configure the number of clock cycles to add or remove from the feeding clock signal.

![](images/5e94f9cc349c7a3f40f75617e772844c3be35eebd35a71f67a3179fa656f6c5d.jpg)  
Figure 8. Typical crystal accuracy plotted against temperature

# 2.5.2 RTC calibration methodology

Tclocec us alsent dictal ck_cal (smooth calibration clock) pulses.

For RTC2 type, ck_cal is always RTCCLK.

Fo RTC3 type, if LPCAL = 0 in RTC_CALR, ck_cal = RTCCLK. If LPCAL = 1, ck_al = ck_apre (clocoutt y the RTC asynchronous prescaler). Moreover, when setting LPCAL to 1 and choosing ck_apre, the calibration consumption decreases, ts accuracy remains the same and the calibration window changes to about 20 x PREDIV_A x RTCCLK pulses (instead of 220 RTCCLK pulses when LPCAL = 0).

The RTC clock can be calibrated with a resolution of about 0.954 ppm with a range from -487.1 ppm to +488.5 ppm.

Tlilat or crystal aging).

![](images/15d9f7feb408280b0469c481d6731eab0f0a6eb12eb4a0bf61d863a227ee8db9.jpg)  
Figure 9. Smooth calibration block for RTC2 type

![](images/a3421eefd0a9226332427c4b68dd3b63b55c4345a3e0957711b8c5bc4ba933a7.jpg)  
Figure 10. Smooth calibration block for RTC3 type (LPCAL = 1)

Thuerancpu heclock vinsighRTCALI ialhedathe alian bloc I alo possibleputan extenal  Hzreernceand make he dequa proesg inside he MCU tc the RTC clock. The user finds such example in Section 4 and in Section 6.

The calibratin result can be checked by using the caliration output 512 Hz or  Hz or the RTCALB al Refer to Table 4 and Table 5.

A smooth calibration consists of masking and adding N (configurable) 32 kHz-requency pulses that are well distributed in a configurable window (8 s, 16 s or 32 s).

The number of masked or added pulses is defined using CALP and CALM[8:0] in RTC_CALR register.

By default, when the input frequency is 32768 Hz, the caliration window duration is 32 seconds (consirig LPCAL = 0 for RTC3). It can be reduced to 8 or 16 seconds by setting CALW8 or CALW16 in RTC_CALR.

# Note:

The 0.954 ppm accuracy of the mooth calibration is only achievable by 32 s calibratin window, for 16 s, the best accuracy is (0.954 x 2), and for 8 s is (0.954 x 4).

# Example 1

Setting CALM[0] = 1, CALP = 0 and using 32 s calibration window, results in exactly one pulse being masked fr 32 s.

# Example 2

Settng CALM[2] = 1, CALP = 0 and using 32  calibration window, results in exactl four pulses being masked fr 32 s.

# Note:

Both CALM[8:0] and CALP can be used. In this case, an offset ranging from-511 to +512 pulses can beaded for 32 s (calibration window).

hen the asynchronous prescaler is less than 3, CALP cannot be set to 1.

T orula  alculate hefectv aliratefequencyLgivenhe put equency

FCAL = FRTCCLK X [1 + (CALP x 512 - CALM) / (20 + CALM - CALP x 512)]

h detected.

# Check the smooth calibration

Tocalan fecaler co cloc n eecke  latusig following:

RTC_CALIB output (1 Hz) Subsecond alarms Wake-up timer

# 2.6

# Synchronize the RTC

arnm  coc cochia reding he subseond l calculatin eprecfft between he ebeigmaintaine  e e cloc and hedhe an eut bymovi  fft widuste the shift register control.

![](images/cc4cdff904d4bca6c38fc2d112acbc4c8eeb3aa248c55b4b4a9a3048af8f13cc.jpg)  
Figure 11. RTC shift register

The ynhronization hi ncti canot heckusigheRTCCALIutu sinc he hieatn no impact on the RTC clock (except adding or subtracting a few fractions from the calendar counter).

# Correct the RTC calendar time

I coc anc cpar heeo cock yacineons, eetvalue ut e writte in SUBFS[14:0] in RTCSHIFTR, that is aded to the synchronou prescaler counter. As this counter counts down, this operation effectively subtracts from (delays) the clock by:

Delay (seconds) = SUBFS / (PREDIV_S + 1)

I ecceva added to the clock (advancing the clock) when ADD1 in RTC_SHIFTR is used in conjunction with SUBFS, effectively advancing the clock by:

Advance (seconds) = (1 - (SUBFS / (PREDIV_S + 1)).

# Caution:

For RTC3 type, ADD1S has no effect in binary mode. In mixed mode, the SUBFS[14:BCDU+8] must be written with 0. Before niating a shift peration in BCD mode, the user must check that S[5] = 0inorder t se that no overflow occurs. In mixed mode, the user must check that the bit SS[BCDU+8] = 0.

An example for this feature is provided in the X-CUBE-RTC (see Section 7 for more details).

# RTC reference clock detection

For RTC3 type, this feature is available only in BCD mode (BIN = 00).

The reference clock (50 Hz or 60 Hz) must have a hiher precision than the 32.768 kHz LSE clock This s why the RTC provides a reference clock input (RTC_REFIN pin) that can be used to compensate the imprecision of the calendar frequency (1 Hz). The RTC_REFIN pin must be configured in input floating mode.

This mechanism enables the calendar to be as precise as the reference clock.

The reference clock detection is enabled by setting REFCKON inRTCCR. When the reference clock detection is enabled, PREDIV_A and PREDIV_S must be set to their default values (PREDIV_A = Ox007F and PREDIV_S = 0x00FF).

# Note:

This feature is only valid with the RTC clock from LSE oscillator oscillating at 32.768 kHz due to this requirement.

Whe heeen cloc deteion s ableHz cloc  parheearst efeenl c W t 1 Hzcloc bceiligee  thesn  the E clock, he TC hihe Hz clock that future 1 Hz clock edges are aligned. The update window is three ck_apre periods.

I chaaa thenlocusdetwinnt  peautt cock The detection window is seven ck_apre periods.

Tc must be much more precise than 32 kHz quartz.

The detection system is used only when the reference clock needs to be detected back after a loss. As the 00Hcc have wTetihenh is ialhancoc

Asig that ckre isnot lost more than once a day, the totaluncertaint permonth is 20 ms 1x 30 = 0. , which is much less than the uncertainty of a typical quartz (53 s/month for ±20 ppm quartz).

![](images/5cc8ef598dc01f393911b5dfbb0bd21de93984ccf58b12c7918d395ff787dd32.jpg)  
Figure 12. RTC reference clock detection

# Note:

The reference clock calibration and the RTC synchronization (shift feature) cannot be used together. The H  s s, eac    esThe e loco inVBT mode.Thereerence clockcalration can nly eused if the userprovides a precise50r 0H ut.

An example for this feature is provided in the X-CUBE-RTC (see Section 8 for more details).

# RTC prescaler adjustment with LSI measurements

Whe L is elece  TCclocsour teran eseeasur  equency najus synchronous prescaler depending on the result got. The goal is to improve the observed LS accuracy.

The LS clocksgal  e heput captue e32timers ehe time coe al  p p elapsd betwen twoS rig egeassociated.The software exploits he number  perids cunt ycpar t with hemoexpecanadjuseRsncronu precalvalurder the RTC accuracy.

A firmware example is available in the STM32CubeL4 MCU Package for NUCLEO-L412RB-P (RTC3 type): STM32Cube_FW_L4_Vx.y.z\Projects|NUCLEO-L412RB-P|Examples|RTC\RTC_LSI

If one example is not available in the STM32Cube for a given STM32 MCU, the user can adapt it.

# 2.9

# Timestamp function

The timestamp feature is used toautomatically save the current calendar when some specific eventscur.

![](images/17927346271d787216c8b6556e63ade76c7014564662addd625bf6d12a362da2.jpg)  
Figure 13. Timestamp event procedure

When this function is enabled, the calendar is saved in the timestamp registers (RTC_TSTR, RTC_TSDR, RTCTSSSR) when an internal or external timestamp event is detected. When a timestamp event occurs, the timestamp flag bit (TSF) is set in RTC_ISR (RTC2)/RTC_SR (RTC3).

The following events can generate a timestamp:

Edge detection on the RTC_TS I/O   
Tamper event detection (from all RTC_TAMP I/Os)   
Switch to VBAT when the main supply if powered off (available for example on STM32L4 series, see the   
product reference manual and datasheet to verify availability for other products)

Table 14. Timestamp features   

<table><tr><td rowspan=1 colspan=1>What</td><td rowspan=1 colspan=1>How</td><td rowspan=1 colspan=1>Comments</td></tr><tr><td rowspan=1 colspan=1>Enable timestamp.</td><td rowspan=1 colspan=1>Set to 1 TSE, ITSE or TAMPTS in RTC_CR.</td><td rowspan=1 colspan=1>TAMPTS is only available on RTC3 to allow tamper events to triggertimestamp.</td></tr><tr><td rowspan=1 colspan=1>Detect a timestampevent by interrupt.</td><td rowspan=1 colspan=1>Set TSIE in RTC_CR.</td><td rowspan=1 colspan=1>An interrupt is generated when a timestamp event occurs.</td></tr><tr><td rowspan=1 colspan=1>Detect a timestampevent by polling.</td><td rowspan=1 colspan=1>Poll on the timestamp flags (TSF or ITSF(1) inRTC_ISR (RC2)/RTC_SR (RTC3).</td><td rowspan=1 colspan=1>To clear the flag, write zero on TSF or ITSF(2).</td></tr><tr><td rowspan=1 colspan=1>Detect a timestampoverflow event.(3)</td><td rowspan=1 colspan=1>Check on TSOVF(4) in RTC_ISR (RC2)RTC_SR (RTC3).</td><td rowspan=1 colspan=1>To clear the flag, write zero in TSOVF.RTC_TSTR, RTC_TSDR, and RTC_TSSSR maintain theresults of the previous event.If a timestamp event occurs immediately after TSF is supposedto be cleared, then both TSF and TSOVF are set.</td></tr></table>

TSF is set two ck_apre cycles after the timestamp event occurs, due to the synchronization process. 2. read this bit at 1. 3. The timestamp overflow event is not connected to an interrupt. 4. T recommended to poll TSOVF only after TSF has been set.

# 2.9.1

# Timestamp firmware examples

The R cmes wit a  eample projects o that the user cn quickly becme fmiiar with thi perheal.   
Refer to the STM32Cube MCU Package of the product for a complete projects list.

For example, the user can find the following projects concerning timestamp:

For the NUCLEO-L412RB-P equipped with an RTC3: STM32Cube_FW_L4_Vx.y.z|Projects|NUCLEO-L412RB-PlExamples|RTCIRTC_TimeStamp . For the NUCLEO-G071RB equipped with an RTC3: STM32Cube_FW_G0_Vx.y.z\Projects|NUCLEO-G071RB|Examples_LLIRTCIRTC_TimeStamp_Init

If an example is not available in the STM32Cube for a given STM32 MCU, the user can adapt it.

# RTC tamper detection function

Tclueeval tamperetectn ipuetame input n cigureetec ifrent of tamper events. Each tamper input has an individual flag (TAMPxF in RTC_ISR (RTC2)/TAMP_SR (RTC3)).

A tamper detection event generates an interrupt when TAMPIE or TAMPxIE is set in RTC_TAMPCR (RTC2) TAMP_IER (RTC3).

The configuration of the tamper fltr, TAMPFLT[1:0] i TAMPFLTCR, defies whether the tamper detetion is activated on edge (set TAMPFLT[1:0] = 00), or on level (TAMPFLT[1:0] ≠ 00).

The number of tamper inputs depends on product packages. Each input has a TAMPxF individual flag in RTC_ISR (RTC2)/TAMP_SR (RTC3).

The DB bt (he regiserassociat depens nhe product), must e aow wriacs toany TAMP registers after a system reset.

# 2.10.1 Edge detection on tamper input

Whe TAMPFLT[:0] = 00, hetamperput detein rig when  ii ege r  faling ee depeni TAMPxTRG) is observed on the input pin RTC_TAMPx (RTC2)/TAMP_INx (RTC3).

![](images/e7fcd2a0c47eb985d018d265ebbf74bece01c81b553011c9fbc8ebdeb7d0dde9.jpg)  
Figure 14. Tamper with edge detection   
u allows the bypass of the internal pull-up resistor.

With the edge detection, the sampling and precharge features are deactivated.

Table 15. Tamper features (edge detection)   

<table><tr><td rowspan=1 colspan=1>What</td><td rowspan=1 colspan=1>How</td><td rowspan=1 colspan=1>Comment</td></tr><tr><td rowspan=1 colspan=1>Enable tamper.</td><td rowspan=1 colspan=1>Set TAMPxE = 1 in RTC_TAMPCR (RTC2)TAMP_CR1 (RTC3).</td><td rowspan=1 colspan=1></td></tr><tr><td rowspan=1 colspan=1>Select tamper active edgedetection.</td><td rowspan=1 colspan=1>Select with TAMPxTRG in RTC_TAMPCR (RTC2)/TAMP_ CR2 (RTC3).</td><td rowspan=1 colspan=1>The default edge is rising edge.</td></tr><tr><td rowspan=1 colspan=1>Detect a tamper event byinterrupt.</td><td rowspan=1 colspan=1>Set TAMPIE or TAMPxIE in RTC_TAMPCR (RTC2)TAMP_IER (RTC3) register</td><td rowspan=1 colspan=1>An interrupt is generated when a tamperdetection event occurs.</td></tr><tr><td rowspan=1 colspan=1>Detect a tamper event bypolling.</td><td rowspan=1 colspan=1>Poll TAMPxF in the RTC_ISR (RTC2)/TAMP_SR (RTC3).</td><td rowspan=1 colspan=1>RTC2: To clear the flag, write zero in TAMPxF.RTC3: Write 1 in CTAMPxF in TAMP_SCRclears TAMPxF in TAMP_SR.</td></tr></table>

# 2.10.2

# Level detection on tamper input

Setting TAMPFLT[1:0] to a value other than zer means that the tamper input triggers when a selected level (high or low) is observed on the corresponding input pin RTC_TAMPx (RTC2)/TAMP_INx (RTC3).

A tamper detection event is generated when either two, four or eight (depending on the TAMPFLT value) consecutive samples are observed at the selected level.

![](images/17e66e60bc03fa27c60e468518155fdd4fb5f2c3b466c84ffc756e1fa7b1d4ab.jpg)  
Figure 15. Tamper with level detection

Using the level detection (TAMPFLT[1:0] ≠ 0), the tamper input pin can be precharged by resettin TAMPPUDIS TAMPPRCH[1:0]).

![](images/bd8fee873d11dc6fe058862978a3740a5fe367c8a955b1722860a7a6f1897d21.jpg)  
Figure 16. Tamper sampling with precharge pulse

# Note:

When the internal pull-up is not applied the I/O Schmit triggers are disabled inorder to avoid an extra consumption if the tamper switch is open.

The tradeo between the tamperdetection latency and the power consumption through the weak pullo external pull-down can be reduced by using a tamper sampling frequency feature. The tamper sampling frequency is determined by configuring TAMPFREQ[2:0] in RTC_TAMPCR (RTC2)/TAMP_FLTCR (RTC3) reier Whenusing the L at 32768 Hz as theRC cloc source, te samplig fequenc can be , , 4, 8 32, 64, or 128 Hz.

Table 16. Tamper features (level detection)   

<table><tr><td rowspan=1 colspan=1>What</td><td rowspan=1 colspan=1>How</td><td rowspan=1 colspan=1>Comment</td></tr><tr><td rowspan=1 colspan=1>Enable tamper.</td><td rowspan=1 colspan=1>Set to 1 TAMPxE in RTC_TAMPCR (RTC2)/TAMP_CR1 (RTC3).</td><td rowspan=1 colspan=1></td></tr><tr><td rowspan=1 colspan=1>Configure tamper filter count.</td><td rowspan=1 colspan=1>Configure TAMPFLT bits in RTC_TAMPCR (RTC2)TAMP_FLTCR (RTC3).</td><td rowspan=1 colspan=1></td></tr><tr><td rowspan=1 colspan=1>Configure tamper samplingfrequency.</td><td rowspan=1 colspan=1>Configure TAMPFREQ bits in RTC_TAMPCR (RTC2)TAMP_FLTCR (RTC3).</td><td rowspan=1 colspan=1>Default value is 1Hz.</td></tr><tr><td rowspan=1 colspan=1>Configure tamper internal pull-upand precharge duration.</td><td rowspan=1 colspan=1>Configure TAMPPUDIS and TAMPPPRCH in RTC_TAMPCR (RTC2)TAMP_FLTCR (RTC3).</td><td rowspan=1 colspan=1></td></tr><tr><td rowspan=1 colspan=1>Select tamper active edge/leveldetection.</td><td rowspan=1 colspan=1>Select with RTC_TAMPCR (RTC2)/TAMP_CR2 (RTC3).</td><td rowspan=1 colspan=1>Edge or level depends on tamperfilter configuration.</td></tr><tr><td rowspan=1 colspan=1>Detect a tamper event byinterrupt.</td><td rowspan=1 colspan=1>Set TAMPIE or TAMPxIE in RTC_TAMPCR (RTC2)TAMP_IER (RTC3).</td><td rowspan=1 colspan=1>An interrupt is generated whentamper detection event occurs.</td></tr><tr><td rowspan=1 colspan=1>Detect a tamper event by polling.</td><td rowspan=1 colspan=1>Poll TAMPxF in RTC_ISR (RTC2)/TAMP_SR (RTC3).</td><td rowspan=1 colspan=1>To clear the flag, write zero inTAMPxF.</td></tr></table>

# 2.10.3

# Action on tamper detection event

By setting TAMPTS = 1, any tamper event (with edge or level detection) causes a timestamp to occur. The timestapadestamp ovefow gs ehen t whene mper   nd work nhe samea as when a normal timestamp event occurs.

# Note:

It is not necessary to enable or disable the timestamp function when using this feature.

Oactins hantestamnrgere tamperdeetion ependng e produc usRe the product documentation for a complete list of actions.

For example, a tamper detection can:

Erase the backup registers, SRAMs content or specific peripheral registers   
Generate an interrupt that can wake up the device from low-power modes   
Generate an hardware trigger for a low-power timer or a RTC timestamp event (see TAMPTS bit mentioned   
efore)

On sme product,he protection specifidevicassets an e enabledisabled thanks to the RCFGy TAMP_ERCFGR. If this bit s et, in case f a tamperdetection or when BKBLOCK = 1 in TAMP_CR2, theread/ write accesses to the concerned device assets are blocked.

# 2.10.4

# Active tamper detection (RTC3 only)

The tamper detection can  made robust agaist tamper  beig externallyopene  hortThat isdone thanks to the active tamper.

The pinciple s to set TAMP_OUTy utput pins todelive a rand mesage, and TAMP_INx input pins to ive heen sot i vTAM TAMP_SR for the TAMP_INx pin detecting the error. Depending on the tamper pins available, several nzatins an e oguror eampl  ht tamer p, e ser n havefouroutpus u inputs with four different messages, or seven inputs with one output and one message exchanged.

![](images/5a1ccd0084e6363f5f0284d7a524e5917c52eaf1666b275431276f1eb8e42d99.jpg)  
Figure 17. Tamper detection

# 2.10.4.1

# Active pin IN/OuT association

The user configures TAMP_INx as active input pins by setting TAMPxAM = 1 in TAMP_ATCR1.

By default, when TAMP_INx is activated as active tamper pins, the TAMP_OUTx pin is associated to it to implement the active tamper detection mechanism.

I otherTAMP_Ny pins need to be associated to TAMPOUTx pin (the e mentned above) for the applion, ATOSHAR ivu har) t n   akeal  TAMPOUT pis,c TAMP_OUTx, sharable.

When ATOSHARE = 1, ATOSELi (active tamper output selection) alows the choice of the new TAMP_OUT pin associated to TAMP_INi.

Exaple: consiering there re t least two active tamper pins on he product, TAMP_OUT1 can beus for comparison with TAMP_IN1 and TAMP_IN2 by configuring and enabling both TAMP_IN1 and TAMP_2 in active mode, with ATOSHARE = 1, ATOSEL1 = 0 and ATOSEL2 = 0.

# Note:

ATOSHARE and ATOSELi bits are respectively in TAMP_ATCR1 and TAMP_ATCR2.

# 2.10.4.2 Filtering

a tamper event is triggered when two comparisons among four are false (receivedmessage different fom the sent one).

# 2.10.4.3 Message randomization

Coningendmzationhemessagnt yheivuu   peanubr (RNG valuein TAMPATOR) isused and need to be d periiclly wit a new seed.To ensue that, euse nees to maintain four 32-bit random values in the code. These last one are not necessarily generated by a random generator, the user can choose random values and update it with a mathematical formula.

By writing consecutively these four values in TAMP_ATSEEDR register, the user feeds the PRNG and allows active output pins to renew the randomization of their message.

The PRNG takes several APB clock cycles (refer to the product documentation) to take into account the seed given, during this time the SEEDF bit in the TAMP_ATOR register is set and the TAMP_APB clock must not be icectveoutut ns elyactvat er he RGhastake eitoacco the user must wait SEEDF to be cleared before, for example, entering low-power modes.

I erdsot wan n lo-powemod,hepdthe e an eoeur tmve activity.The update ate or he seds depends on the number ftamper active outputs used,he prouc reference manual gives advisable time references for this action.

# 2.10.4.4 Initialization

If INITS is not set in TAMP_ATOR register, the active tamper initialization must be done:

Configure the active tamper clock prescaler with ATCKSEL in TAMP_ATCR1. Set the filter and associate TAMP in and out pins as needed (explained above). Enable tamper pins used in TAMP_CR1 register (all in the same write access). Feed the PRNG and wait for SEEDF to be cleared. Then backup registers are protected by active tamper.

I c more robust randomization.

# 2.10.5

# Internal tamper detection (RTC3 only)

The internal tamper detection feature allows the detectionf transient and environmental perturbations. An inteal tamper event i nabled with ITAMPx nTAMPCR1.Thenterrupt isenabled by ettng ITAMPIE TAMP_IER. Then, i the evetccur, ITAMPxF is set iTAMPSR, and ITAMPxMF is set in TAMP_MISR f e interrupt has been enabled.

To clear both flags (polling and interrupt mode), the corresponding bit in TAMP_SCR must be set. The STM32 MCUs implement some of the internal tampers listed below (refer to product reference manua

ITAMP1: supply voltage monitoring (or backup domain voltage monitor)   
ITAMP2: temperature monitoring   
ITAMP3: LSE monitoring (CSS)   
ITAMP4: HSE monitoring (CSS)   
ITAMP5: RTC calendar overflow   
ITAMP6: JTAG/SWD access when RDP > 0 (or NVSTATE != open in STM32H5)   
ITAMP7: ADC analog watchdog monitoring 1   
ITAMP8: monotonic counter 1 overflow   
ITAMP9: cryptographic peripheral fault (SAES, AES, PKA or RNG)   
ITAMP10: reserved   
ITAMP11: IDWG reset when tamper flag is set (potential tamper timeout)   
ITAMP12: ADC analog watchdog monitoring 2   
ITAMP13: ADC analog watchdog monitoring 3   
ITAMP14: reserved   
ITAMP15: system fault   
ITAMP16: reserved

values and conditions on event triggering (example: voltage value threshold for voltage monitoring).

A en atusetal vent llattackthe. F cet  ysicog back akeoT st existence of the ITAMP5 signal.

A firmware example exploiting the ITAMP5 event is provided in the X-CUBE-RTC and detailed in Section 9.

The RTC3 tamper detection unit embeds also a monotonic counter implemented in TAMP_COUNTR register (called TAMP_COUNT1R on some products) and associated to ITAMP8. See Table 4 and Table 5 for the r written value.TAMPCouNTR cannot roll-over and is frozen when reachin its maximum. This register an be neltn  owobusys cnte trigger a tamper event.

ITAMP7, ITAMP12 and ITAMP13 are associated to analog watchdogs and are used to consider that an ADC channel going out of a configured voltage range is a tamperevent (see the documentation of the products featuring this internal tamper for more details).

# 2.10.6 Potential detection management (RTC3 only)

If TAMPxNOER = 0 in TAMP_CR2 or ITAMPxNOER = 0 in TAMP_CR3, the backup registers and other device secrets are automatically erased by hardware on an external (passive or active orinternal tamper event.

I aviou tper ags t TAMP n ITAMPF).Tee t events e conser s potentialtpe, the user can investigate f thetamper event corresponds to a trueor to a false tamper, and then take the necessary actions.

BKERASE = 1 in TAMP_CR2. If the tamper is not confirmed and is considered a false detection, the user must c hc is possible again.

By associating the NOERASE feature with the IWDG (independent watchdog), a timeout can be implemented to automatically launch hardware erasing after a potential tamper detection. On some products, the ITAMP11 is asiated o the IWDG reset.In this case  a tamperevent in NOERASE configuration sdetecte and IWD e c lll occurs at the same time than a tamper detection is very low so the hardware considers it is a real attack.

# 2.10.7

# Tamper detection firmware examples

The R cmes wit a  eample projects o that the user cn quickly becme fmiiar with thi perheal.   
Refer to the STM32Cube MCU Package of the product for a complete projects list.

For example, the user can find the following projects concerning tamper detection:

For most microcontrollers equipped with either an RTC2 or an RTC3:   
STM32Cube_FW_product_Vx.y.z\Projects\board|Examples|RTCIRTC_Tamper   
For many products equipped with either an RTC2 or an RTC3:   
STM32Cube_FW_product_Vx.y.z\Projects\board|Examples_LLIRTCIRTC_Tamper_Init   
For the STM32L552E evaluation board, the STM32H7B3I evaluation board and the STM32U575ZI Nucleo   
board equipped with an RTC3:   
STM32Cube_FW_product_Vx.y.z|Projects\board\Examples|RTCIRTC_ActiveTamper

I example is ot available  heT32Cube or give TM32 MCU,he user can adapt t froma example.

# 2.11 Backup registers

The 32-bit backup registers (RTCBKPR)are reset when a tamper detection event occurs.These registers re per-n AT hn ihee product  otplment hiatur, Iike 32L and STM32L series. Refer toTable 4 and Table 5.They are not reset by a system reset, and their contents remain valid when the device operates in low-power mode.

For RTC2 type on STM32L0, STM32L4, and STM32F7 series, the 32-bit backup registers (RTC_BKPxR) are not reset if TAMPxNOERASE = 1 or if TAMPxMF = 1 in RTC_TAMPCR.

For RTC3 type, the 32-bit backup registers (TAMP_BKPxR) are not reset if TAMPxNOER = 1 or if TAMPxMSK = 1 in TAMP_CR3.

For RTC andRTC3abling he backup rgisr reet eatue allows n LTIM event  berige fm e filtering, either to generate triggers or to generate interrupts.

# Note:

TVA blh Llty  eac is  heprR Table 4 and Table 5.

The RTC3 backup registers can be protected against nonsecure or unprivileged accesses (see Section 2.14: Reduce power consumption).

BKPRWDPROT[7:0] and BKPWDPROT[7:0] in TAMP_SMCR (except for the STM32U3 and STM32U5 series: BKPRWSEC[7:0] and BKPWSEC[7:0] in TAMP_SECCFGR) are used to program the backup registers offset, delimiting three protection zones for the backup registers:

Zone 1: read and write secure

Zone 2: read nonsecure and write secure

Zone 3: read and write nonsecure

Secure AES boot hardware key (RTC3 only)

# Note:

This section is valid only for products embedding a SAES.

T c  e H yA srts Arm® TrustZone® secrity, the eight first backu registers (TAMPBKPR to TAMPBKP7R) must e configured as belonging to the zone 1 (r/w secure) by setting BKPRWSEC ≥ 8 in TAMP_SECCFGR.

Once the registers are written with the key, BHKLOCK must be set to 1in TAMPSECCFGR to definitively block the readwricceses  theseregisters ny reading returns ad an writing is ored). KLCK cy cleared by harware ter tamper even  when eadout protectondisable In thesetwo cas backup registers are also erased. After BHKLOCK is set, the SAES coprocessor can use the BHK thanks to a pharaus ehe AE cn he ouc eeanal anmo peciy ESE the SAES control register).

# 2.12 Alternate function RTC outputs

The RTC has two outputs:

RTC_CALIB (RTC2)/CALIB (RTC3), used to generate an external clock RTC_ALARM (RTC2)/TAMPALARM (RTC3), unique output resulting from the multiplexing of the RTC alarm and wakeup events (and also tamper detection events for RTC3 type)

For RTC3 type, theseoutputs can be associated to two pins against ne pin or RTC2 type. Refer to OUT2ENn RTC_CR of RTC3 type to choose which function is output on which pin.

# 2.12.1

# RTC_CALIB output

The RTC_CALIB output can be used to generate a 1 Hz or 512 Hz signal, and to measure the RTC clock deviation when compared to a more precise clock.

# Setting 512 Hz as output signal

Select LSE at 32768 Hz as RTC clock source.   
2Set the asynchronous prescaler to the default value 128.   
3Enable the output calibration by setting COE = 1.   
4Select 512 Hz as the calibration output by setting COSEL = 0.

# Setting 1 Hz as the output signal

Select LSE at 32768 Hz as the RTC clock source.   
2Set the asynchronous prescaler to the default value 128.   
3. Set the synchronous prescaler to the default value 256.   
4.Enable the output calibration by setting COE = 1.   
Select 1 Hz as the calibration output by setting COSEL = 1.

Note:

Refer to figures in Section 2.5.2: RTC calibration methodology.

# Maximum and minimum RTC_CALIB 512 Hz output frequency

The RTC_CALIB output can also be used to generate a variable-frequency signal. Depending on the user to generate sound.

The signal frequency is configured using the 6 LSB bits (PREDIVA [5:0]) of the asynchronous prescaler PREDIV_A[6:0].

Table 17. RTC_CALIB output frequency versus clock source   

<table><tr><td rowspan=2 colspan=1>RTC clock source</td><td rowspan=1 colspan=2>RTC_CALIB output frequency</td></tr><tr><td rowspan=1 colspan=1>MinimumPREDIV_A[5:0] = 111111 (div64)</td><td rowspan=1 colspan=1>MaximumPREDIV_A[5:0] = 100000(1) (div32)</td></tr><tr><td rowspan=1 colspan=1>HSE_RTC = 1 MHz</td><td rowspan=1 colspan=1>15.625 kHz</td><td rowspan=1 colspan=1>30.303 kHz</td></tr><tr><td rowspan=1 colspan=1>LSE = 32768 Hz</td><td rowspan=1 colspan=1>512 Hz(default output frequency)</td><td rowspan=1 colspan=1>993 Hz</td></tr><tr><td rowspan=1 colspan=1>LSI = 32 kHz</td><td rowspan=1 colspan=1>500 Hz</td><td rowspan=1 colspan=1>969 Hz</td></tr><tr><td rowspan=1 colspan=1>LSI = 37 kHz</td><td rowspan=1 colspan=1>578 Hz</td><td rowspan=1 colspan=1>1.121 kHz</td></tr><tr><td rowspan=1 colspan=1>LSI = 40 kHz</td><td rowspan=1 colspan=1>625 Hz</td><td rowspan=1 colspan=1>1.212 kHz</td></tr></table>

1. DIV[   RTCCAL  REDIVA[5= on RTC_CALIB.

# 2.12.2

# RTC_ALARM (RTC2)/TAMPALRM (RTC3) output

The alarm, wakeup and tamper flags can be routed to the RTC outputs (one output for RTC2 type, three for RTC3 type) thanks to OSEL[1:0] in RTC_CR.

# For RTC2 type

OSEL[1:0] = 01 roots alarm A to the RTC_ALARM output.   
OSEL[1:0] = 10 roots alarm B to the RTC_ALARM output.   
OSEL[1:0] = 11 roots wakeup flag to the RTC_ALARM output.

Once OSEL[1:0] is fixed, the output reflects the selected flag stored in RTC_ISR.

# For RTC3 type

The OSEL[1:0] slection follows he same principle as or RTC2 but, when TAMPOE =  in RTCCR, tamper flags a Red wit he galredy ele alaralarBake beore heRresult  eote TAMPALRM output.

If TAMPOE = 1 and OSEL[1:0] = 00, TAMPALRM output reflects only the tamper flags.

For both RTC2 and RTC3 types, the output pin polarity is selected with POL in RTCCR. When POL = 1, the oie state of the flag concerne is output on RTCALARM (RTC2)/TAMPALRM (RTC3). The pin can also be configured as open drain or push-pu with the ALARMOUTTYPE (RTC2)/TAMPALRM_TYPE (RTC3) bit f the same register (0 for push-pull, 1 for open-drain).

For RTC3, an internal pull-up can be added to the output pin by setting TAMPALRM_PU = 1 in RTC_CR.

# 2.13 RTC safety aspects

# 2.13.1 RTC register write protection

To protect the RTC register against possible unintentional write acceses after reset, the RTC register a ly and date.

Tewrs  heCise abled b wrt  key RCWPRnly with heo eqe Write OxCA in RTC_WPR.

Write Ox53 in RTC_WPR.

Any other write access sequence to RTCWPR activates the write-protection mechanism for the RTC registers.

# 2.13.2 Enter/exit initialization mode

The RTC can operate in two modes:

Initialization mode (counters stopped) Free-running mode (counters running)

The calendarcanot  pdated whil he counters aernig.TeC must consequently be wihed  he InlatetWhe they start counting from the new value when the RTC enters Free-running mode.

The INIT bit in RTC_ISR (RTC2)/RTC_ICSR (RTC3) enables the user to switch from one mode to another. The INITF bit in the same register can be used to check the RTC current mode.

The RTC must be in Initialization mode to program the time and date registers (RTCTRand RTCDR) and the prescalers register (RTC_PRER). This is done by setting INIT = 1 and waiting until INITF flag is set.

T return  heFree-nig mode and restrt countig,he Cmust exit e Initialization mode o y resetting INIT = 0).

Only a power-n reset can reset he calendar on MCUs without the VBAT pin.A system reset does not ffect the calendar but resets the shadow registers (APB registers clocked by the APB bus clock) that are read by he application. These registers are updated again when RSF = 1 in RTC_ISR (RTC2)/RTC_ICSR (RTC3).

After a system reset, the application can use the INITS status flag in RTC_ISR (RTC2)/RTC_ICSR (RTC3) to alumenhat calenarusttlizTeler an soe yett  = in the RCC, even when VBAT is present.

The LSE clock initialization is not always needed after a system reset. It is recommended to check LSERDY in RCC_BDCR and to initialize LSE only if this flag is not already set.

# 2.13.3 RTC clock synchronization

Wheepliatin ea lena gishat conta hel time and date clocked by the RTC clock (RTCCLK). There is a shadow register associated to RTCTR, RTCDR and RTC_SSR. RSF is set in RTC_ISR (RTC2)/RTC_ICSR (RTC3) each time the calendar time and date shadow registers are updated with the real calendar value. The copy is performed every RL cycle, synchronized with the APB bus clock (APB bus by which the RTC is accessed). After a system reset or after exiting the Inlization mode, the aplication must wait or the bit o be et befoe reading the calendar aow registers.

When the system is woken up from low-power modes (SYSCLK was off, consequently, the APB clock was off to, theapplication must frs clear F,and then wait until R is et again before reading the calendar avtao before entering the low-power mode.

Bysetting BYPSHAD =  in RTCCR, the calendarvalues ar taken drectly from the calendar counters s eadw gis Inhaotmandatoywai eynhroatn e carisenmus emus len vl.he rad operaion must then e performe agaThe resul  he two red sequences ae copr. third read result is valid.

# Note:

Asettg BPHAD = 0, the hadw gistrs may co until the ext yncroizatin. In th s the softwae ust clearRSF = 0, wait for he ynchronizaton (RFmust be et), and finally read the haow registers.

# 2.14

# Reduce power consumption

The RTC is designed to minimize the power consumption and can be configured to optimize further its consumption.

# 2.14.1

# Use the right power reduction mode

The RC can e activ he ollowing low-powe mode rom he bigest current consuer themallest):

Sleep mode Stop mode if the RTC clock is provided by LSE or LSI Standby mode if the RTC clock is provided by LSE or LSI Shutdown mode if the RTC clock is provided by LSE

Te precie  modecpatile with the produc and theconsmption estein produceence manual and datasheet.

Thanks to the RTC wakeup unit, the user can wake up the STM32 MCU from this mode. Depending on the application needs in term  low-power phases and current consumption target, the adequate low-powermode and wakeup frequency must be selected.

# 2.14.2

# Jse internal pull-up resistor on tamper pin

T  u pl s u u/utl ulul down ensures a lowest power consumption.

Te adebetweehetmperetectnatenc de pownstion yheCteal pull beotimizd using TAMPFREQ[2:0], that determines the requency f the tamper sampling from128 Hz to 1 Hz when RTCCLK equals 32768 Hz.

# Note:

Refer tothe product datasheeteerencemanual ortheavailabily/electrialcharacteristif the pullresistors.

# 2.14.3

# Set RTC prescalers

T rescale usr ealendarvie intasynonous n  snrono prescales Inc the PREDIVA value of the asynchronous prescaler while reducing the synchronous prescaler accordingly to keep the 1 Hz output, reduces the RTC power consumption.

On RTC3 type, the RTC dynamic consumption is optimized for LPCAL = 1 and PREDIV_A + 1 being a power of two (considering the RTC as the only peripheral using LSE).

# 2.14.4

# External optimization factors

T pealer nke he  cock canaltmiz  nsn.e seee  elect heS clsourehiprecaleivides  y  e  rough 0Hz coc stea heer3 Hz. activated by LSIPRE in RCC_CSR.

a to a typical 250 nA (against 630 nA for a high drive capability). This is done by setting LSEDRV = 00 in RCC_BDCR.

# 2.14.5

# Low-power management firmware examples

The RC comes wit a eample projects o that the user can quickly bece fmar with thi perpheal.   
Refer to the STM32Cube MCU Package of the product for a complete projects list.

Fople e al  uc  hern  he o g management:

For NUCLEO-L412RB-P:   
STM32Cube_FW_L4_Vx.y.z\Projects|NUCLEO-L412RB-P|Examples|RTCIRTC_LowPower_STANDBY   
For NUCLEO-L412KB:   
STM32Cube_FW_L4_Vx.y.zZ\Projects\NUCLEO-L412KB\Examples|PWRIPWR_STANDBY_RTC   
STM32Cube_FW_L4_Vx.y.z\Projects|NUCLEO-L412KB\Examples|PWRIPWR_STOP1_RTC   
STM32Cube_FW_L4_Vx.y.zProjects\NUCLEO-L412KB|Examples|PWRIPWR_STOP2_RTC

Analogous examples are available for STM32F0, STM32F2, STM32F3, STM32F4, STM32F7, STM32G4, STM32H7, STM32L0, STM32L1, STM32U3, STM32U5, STM32WB and STM32WL. If one example is not available in the STM32Cube for a given STM32 MCU, the user can adapt it.

# RTC3 secure and privileged protection modes

Some STM32 MCUs can run in secure or nonsecure mode. Each mode having its own environment, allowing a truul zone, not accessible in nonsecure mode, o be maintained in secure mode TrustZone® feature).

Avli v v unprivileged mode.

O  pu Tabl abhe gi po allo hes ric e / rationnTAMPregister ecureprivilegmodesSom coiguration b stablish hee smegsTe gister/bi rogram  produc ependen heno etail to the product reference manual).

# Note:

The backup registers and the monotonic counter have their own protection mode settings.

# STM32L4 API and tamper detection application example

# STM32CubeL4 firmware libraries for tamper detection

The RTC comes with:

A firmware driver API abstracting the RTC features for the end user   
Refer to stm3214xx_hal_rtc.cand stm3214xx_hal_rtc_ex.c files in   
ISTM32Cube_FW_L4_Vx.y.z\Drivers|STM32L4xx_HAL_Driverl   
A set of example projects in |STM32Cube_FW_L4_Vx.y.Z|Projects|ISTM32L476RG-Eval|Examples|RTC

# X-CUBE-RTC for tamper detection

X-CUBE-RTC shows an example where a real-time clock must be maintained alive while using as low power as possible (STM32CubeExpansion_AN4759_RTC_STM32L_Vx.y.z\Projects\STM32L476G_EVAL\RTC_TamperVBATT).

The firmware implements:

Hints to ensure a low current consumption   
Adisplay in the debugger (date and time, timestamp date and time) and on LEDs (power-up events, reset   
events, tamper events, error)   
A display on the TFT screen, using STemWin library   
Tampering detection capability, both when the main power supply (VDD) is present and when the RTC is   
battery powered   
The ability to timestamp the tampering event   
The abiliy to erase the backup registers that may contain sensitive dataupon tamper detetion

The application flowchart is shown in the figure below.

![](images/48810429084a87e970353a26d37589eb538739887b1890714c5afed5f1092494.jpg)  
Figure 18. Application example flowchart

# 3.3

# Tamper detection application example (STM32L4)

# 3.3.1 Hardware setup

In order to use the application example project, the user needs a STM32L476G evaluation board (STM32L476G-EVAL).

![](images/7ffba48ac9b7abe0ea773ea3d093303992c520aef0a3e0ab1f2f85924f594519.jpg)  
Figure 19. STM32L476G-EVAL board

Supply the board using the USB cable and tie PA0 (tamper pin 2) to 0, with the following actions:

Remove the jumper JP7.   
Connect the CN7 pin 37 to GND.

# Note:

PC13 (tamper pin 1) connected to the blue push-button is not used in this demonstration firmware as it is coeanteal puldownisr eventingheheamperetecionn eve witnteapullup (the lowest consumption mode).

For more information, refer to the user manual Evaluation board with STM32L476ZGT6 MCU (UM1855).

# 3.3.2

# Software setup

Open the project under the user favorite IDE (integrated development environment). For IAR Embedded Workbench®, open the project.eww file. For Keil MDK--ARM, open the project.uvprojx file, compile and launch the debug session. For SW4STM32, open the SW4STM32 toolchain, browse to the SW4STM32 workspac rectoryelec andimport he project RTCTamperBATT. Launching he debug sessin los he program in the internal Flash memory and executes it.

In IAR Embedded Workbench debug session, the user can view the calendar and tamper event timestamp (time and date) by opening a Live watch window (ViewLive watch) and observe the following global variables:

aShowTime   
aShowDate   
aShowTimeStampTime aShowTimeStampDate

The same observation can be done using MDK-ARM development tools. To open the Watch1 window, do ViewlWatch Windows|Watch1.

# 3.3.3 LED meaning

LD1 (green): tamper event detected   
TFT displays: the tamper date and tamper time are different from their initialization state. LD2 (orange): power-on reset occurred   
TFT displays: the tamper date and tamper time are at their initialization state.   
LD3 (red): error (RTC or RCC configuration error, backup registers not erased)   
TFT displays: "error occurred" is displayed.   
LD4 (blue): reset occurred   
TFT displays: the tamper date and tamper time are at their initialization state.

# 3.3.4

# Tamper detection during normal operation

Disconnect the debugger. A power-on reset can be generated by removing the JP7 jumper and placing it gain on ST-LINK.

O A pu o fatg, he LD h how hat meevent detecnFT, he date and time are updated with the timestamp of the tamper event.

# Note:

A ey y  hevn he in the tamper detection frequency (TAMPFREQ) chosen to ensure the lowest power consumption.

At an eappl y ige blackeset buTeplatowblehe et ew event.

# 3.3.5

# Tamper detection when main power supply is off

I  usuppl he BAT p wit he exteal CR1220 batey (JP2n BAT posin, hea eve be detected even if the main power supply is off, with the following steps:

Remove the JP17 jumper.   
Open PAO.   
Te PA0 to GND (simulating that the end-user takes care to close the box containing the electronics before supplying it again).   
Set JP17 on STIk.   
The LD1 lights showing that a tamper event has been detected during the power-down. On TFT, the tamper date and tamper time are updated with the timestamp of the tamper event

# Note:

If the usersupplies the VBAT pin with 3 V (JP12 on VDD position), the RTC is no longer supplied when the main porsupply is switched ofTheapplication is o lngerable todetect the tampering event while h power supply is off.

# STM32L4 API and smooth digital calibration application example

# 4.1

# STM32CubeL4 firmware libraries for smooth calibration

The timer peripheral comes with:

• A firmware driver API abstracting the timer features for the end-user Refer to stm3214xx_hal_tim.c and stm3214xx_hal_tim_ex.c files in ISTM32Cube_FW_L4_Vx.y.z\Drivers|STM32L4xx_HAL_Driverl   
• A set of example projects in \STM32Cube_FW_L4_Vx.y.Z|Projects|STM32L476RG-Nucleo|ExamplesITIM

The RTC comes with:

A firmware driver API abstracting the RTC features for the end-user Refer to stm3214xx_hal_rtc.c and stm3214xx_hal_rtc_ex.c files in ISTM32Cube_FW_L4_Vx.y.z\Drivers|STM32L4xx_HAL_Driverl • A set of example projects in \STM32Cube_FW_L4_Vx.y.Z|Projects|STM32L476RG-Nucleo|Examples|RTC

# 4.2

# X-CUBE-RTC for smooth calibration

X-CUBE-RTC shows an implementation of the smooth digital calibration feature of the RTC using also the GPTIMER HAL API).

In this example, the RTC_CLK is smoothly calibrated based on an external 1 Hz reference (STM32CubeExpansion_AN4759_RTC_STM32L_Vx.y.zIProjectsISTM32L476RG_NucleolRTC_SmoothCalib).

The firmware implements:

A GPTIMER (general-purpose timer) in Master mode using channel 1 in output compare mode (and using an external trigger clock)   
A GPTIMER in Master mode using channel 1 in input capture mode and channel 2 in output compare mode   
This timer is also configured to use the LSE clock thanks to the TIM option register.   
The RTC with the CALR register programming   
GPIOs to connect the input 1 Hz reference clock and the "corrected" RTC_OUT_CALIB clock

# 4.3

# Smooth calibration application example (STM32L4)

# 4.3.1 Hardware setup

In order to use the application example project, the user needs a STM32L476RG Nucleo board (NUCLEO-L476RG).

![](images/fa86af4b3e4941f09da5e4389933c0fa62ada57932378b044146d3727a1e21cb.jpg)  
Figure 20. NUCLEO-L476RG board   
Note: this picture is not contractual.

Supply the board using the USB cable and perform the following actions:

• Connect PD2 to a signal generator driving 1 Hz clock with 3.3 V amplitude. It is advised to control the generated frequency at few ppm. C n of 1 pm).

# 4.3.2 Software setup

Opn the project under he user favorite IDE. For IAR Embeded Workbench, open theRCmthCal.l. For MDK-ARM, open the RTC_SmoothCalib. uvprojx file. For SW4STM32, open the SW4STM32 toolchain, browse to the SW4STM32 workspace directory, select and import the project RTC_SmoothCalib.

Compile and launch the debug session. It loads the program in the internal Flash memory and executes t.

After a maximum of 64 seconds, make a frequency measurement of the CALIB_OUT clock n PB2. The user gets a frequency accurate at 1 ppm compared to the 1 Hz reference clock sent on PD2.

The user can then modify the PD2 clock by few ppm, wait 64 seconds, and check that the PB2 clock has been changed accordingly.

Under debugger, the user can monitor the evolution of the CALR register fields (CALP and CALM).

# 4.3.3

# Smooth calibration application principle

The figure below provides a block diagram of the smooth digital calibration application.

![](images/150cc54b1f2eb75b4da60029ab446ee341e7a9f0431ce1e8293c05eccdde640e.jpg)  
Figure 21. Block diagram of a smooth digital calibration

This application is based on the following steps:

1. A 1 Hz reference clock is connected to TIM3 through the PD2 GPIO.   
is configured to generate a risig edge ater 2  Hz reference rising edges.his gives an event vy 32 s.   
3. TIM2 is configured to increment its counter on CLK_RTC, to get the counter value on the rising edge generated by TIM3, and to store it in TIM2_CCR1 register. Then TIM2 counter is reset.   
4. The Cortex-M4 core gets the TIM2_CCR1 value, compares it with the number of CLK_RTC cycles expected in 32 s and processes the comparison results to update the CALP and CALM[8:0] in RTC_CALR.

The calibration is continuous.

# 3.4 Run time observations

The following steps are needed to check the correct functionality:

IModify the 1 Hz reference clock (for instance by forcing 1.0001 Hz).

Wait 2 x 32 s.

Measure the output frequency. Depending on the accuracy of the generator and the measurement device used, the user can see around 1 ppm accuracy.

The user can also monitor in Debug mode:

CALP and CALM[8:0] in RTC_CALR TIM2_CCR1 register (contains the number of CLK_RTC cycles within a 32 s window)

# ..3.5 Porting suggestions

The software example expects that the TM2 is more than 20 bit, 32 bit in case of L76RB. With products featurngnmerende erackt tieovelowssgefta perform the calibration with 16-th overflow to compensate for the missing 4 bits.

# STM32L0 API and tampering detection application example

# STM32CubeL0 firmware libraries

The RTC comes with:

• A firmware driver API abstracting RTC features for the end-user Refer to stm3210xx_hal_rtc.cand stm3210xx_hal_rtc_ex.c files in ISTM32Cube_FW_Lo_Vx.y.z\Drivers|STM32LOxx_HAL_Driverl A set of example projects in \STM32Cube_FW_L0_Vx.y.Z|Projects|STM32L053R8-Nucleo|ExamplesIRTC

# X-CUBE-RTC for tamper detection

X-CUBE-RTC shows an example where a real-time clock must be maintained alive while using as less power as possible (STM32CubeExpansion_AN4759_RTC_STM32L_Vx.y.z|Projects|STM32L053R8-NucleolRTC_Tamper.

The firmware implements:

A few hints order to ensure a low current consumption   
Adisplay in the debugger (date and time, tmestamp date and time) andon a single LED (power-up events,   
reset events, tamper events, error)   
Tampering detection capability   
The ability to timestamp the tampering event   
The ability to erase the backup registers that may contain sensitive data upon tamper detection

The application flowchart is shown in Figure 18.

# 5.3

# Tamper detection application example (STM32L0)

# 5.3.1 Hardware setup

In order to use the application example project, the user needs a STM32L053R8 Nucleo board (NUCLEO-L053R8).

![](images/7946c81a54ecbb305dfb6cfbfd922722dbad3714e68c1e2fc154641fff53d30a.jpg)  
Figure 22. NUCLEO-L053R8 board   
Note: this picture is not contractual.

Suply he boardusing the USB cable. In this example, the B1 push button is used tosmulate theexteal tamper event. The user can observe the software "private variables" on LED LD2 and CN5 pin 6 (SCK/D13). Details regarding the LED LD2 behavior are available in main. c file.

![](images/9a3ae2ff4029509dabbf14e9d440d361845af9a8fa4b57c799b86ef8f55ac693.jpg)  
Figure 23. LED LD2 behavior

# 5.3.2

# Software setup

Open the project under the user favorite IDE (integrated development environment). For IAR Embedded Worbenc, en  .FoKel MD-ARM, enhe  ecle ndc the debug session. For SW4STM32, open the SW4STM32 toolchain, browse to the SW4STM32 workspace directory, select and import the project RTC_Tamper.

Compile and launch the debug session. This loads the program in the internal Flash memory and executes it. In IAR Embedded Workbench debug session, the user can view the calendar and tamper event timestamp (time and date) by opening a Live watch window (ViewLive watch) and observe the following global variables:

aShowTime   
aShowDate   
aShowTimeStampTime aShowTimeStampDate

The user can add and follow these private variables with:

LED1_Green_Tamper_event_detected LED2_Red_Power_On_Reset_occurred LED3_Red_Error LED4_Blue_Reset_occurred

The same observation can be done using MDK-ARM development tools. To open the Watch1 window, do ViewlWatch Windows|Watch1.

# 5.3.3 LED meaning

Only one LED (LD2) is available on the STM32L053R8 Nucleo board. To match with the STM32L4 examples, described in Section 3.3, LED1, LED2, LED3 and LED4 are replaced by the following integers:

uint32_t LED1_Green_Tamper_event_detected: set when tamper1 event is detected   
(LED1 equivalent)   
uint32_t LED2_Red_Power_On_Reset_occurred: set when power-on reset is detected   
(LED2 equivalent)   
uint32_t LED3_Red_Error: set in errors cases (LED3 equivalent)   
uint32_t LED4_Blue_Reset_occurred: set when reset is detected (B2 black push button,   
LED4 equivalent)

The v at LE L CN5 pin 6 (SCK/D13). Regarding the LED LD2 behavior, see details in main. c file.

# 5.3.4

# Tampering detection during normal operation

# Step 1

A power-on reset can be generated by disconnecting/connecting the USB cable on CN1.

Table 18. Tamper detection status when a power-on reset is detected   

<table><tr><td rowspan=1 colspan=1>Meaning</td><td rowspan=1 colspan=1>Status</td><td rowspan=1 colspan=1>LD2 blink</td></tr><tr><td rowspan=1 colspan=1>LED1_Green_Tamper_event_detected</td><td rowspan=1 colspan=1>0</td><td rowspan=1 colspan=1>OFF</td></tr><tr><td rowspan=1 colspan=1>LED2_Red_Power_On_Reset_occurred</td><td rowspan=1 colspan=1>1</td><td rowspan=1 colspan=1>ON</td></tr><tr><td rowspan=1 colspan=1>LED3_Red_Error</td><td rowspan=1 colspan=1>0</td><td rowspan=1 colspan=1>OFF</td></tr><tr><td rowspan=1 colspan=1>LED4_Blue_Reset_occurred</td><td rowspan=1 colspan=1>1</td><td rowspan=1 colspan=1>ON</td></tr></table>

# Step 2

Push B1 to simulate a tamper event.

Table 19. Tamper detection status when a tamper event is detected (after a power-on reset)   

<table><tr><td rowspan=1 colspan=1>Meaning</td><td rowspan=1 colspan=1>Status</td><td rowspan=1 colspan=1>LD2 blink</td></tr><tr><td rowspan=1 colspan=1>LED1_Green_Tamper_event_detected</td><td rowspan=1 colspan=1>1</td><td rowspan=1 colspan=1>ON</td></tr><tr><td rowspan=1 colspan=1>LED2_Red_Power_On_Reset_occurred</td><td rowspan=1 colspan=1>1</td><td rowspan=1 colspan=1>ON</td></tr><tr><td rowspan=1 colspan=1>LED3_Red_Error</td><td rowspan=1 colspan=1>0</td><td rowspan=1 colspan=1>OFF</td></tr><tr><td rowspan=1 colspan=1>LED4_Blue_Reset_occurred</td><td rowspan=1 colspan=1>1</td><td rowspan=1 colspan=1>ON</td></tr></table>

# Step 3

# Push B2 to simulate a reset.

Table 20. Tamper detection status when a reset is detected   

<table><tr><td rowspan=1 colspan=1>Meaning</td><td rowspan=1 colspan=1>Status</td><td rowspan=1 colspan=1>LD2 blink</td></tr><tr><td rowspan=1 colspan=1>LED1_Green_Tamper_event_detected</td><td rowspan=1 colspan=1>0</td><td rowspan=1 colspan=1>OFF</td></tr><tr><td rowspan=1 colspan=1>LED2_Red_Power_On_Reset_occurred</td><td rowspan=1 colspan=1>0</td><td rowspan=1 colspan=1>OFF</td></tr><tr><td rowspan=1 colspan=1>LED3_Red_Error</td><td rowspan=1 colspan=1>0</td><td rowspan=1 colspan=1>OFF</td></tr><tr><td rowspan=1 colspan=1>LED4_Blue_Reset_occurred</td><td rowspan=1 colspan=1>1</td><td rowspan=1 colspan=1>ON</td></tr></table>

# Step 4

Push B1 to simulate a tamper event.

Table 21. Tamper detection status when a tamper event is detected (after a reset)   

<table><tr><td rowspan=1 colspan=1>Meaning</td><td rowspan=1 colspan=1>Status</td><td rowspan=1 colspan=1>LD2 blink</td></tr><tr><td rowspan=1 colspan=1>LED1_Green_Tamper_event_detected</td><td rowspan=1 colspan=1>1</td><td rowspan=1 colspan=1>ON</td></tr><tr><td rowspan=1 colspan=1>LED2_Red_Power_On_Reset_occurred</td><td rowspan=1 colspan=1>0</td><td rowspan=1 colspan=1>OFF</td></tr><tr><td rowspan=1 colspan=1>LED3_Red_Error</td><td rowspan=1 colspan=1>0</td><td rowspan=1 colspan=1>OFF</td></tr><tr><td rowspan=1 colspan=1>LED4_Blue_Reset_occurred</td><td rowspan=1 colspan=1>1</td><td rowspan=1 colspan=1>ON</td></tr></table>

# STM32L5 API and smooth digital calibration application example

# 6.1

# STM32CubeL5 firmware libraries for smooth calibration application

The timer peripheral (TIM) comes with:

A firmware driver API abstracting TIM features for the end-user   
Refer to stm3215xx_hal_tim.cand stm3215xx_hal_tim_ex.c files in   
ISTM32Cube_FW_L5_Vx.y.z\Drivers|STM32L5xx_HAL_Driverl   
A set of example projects in ISTM32Cube_FW_L5_Vx.y.Z|Projectsl NUCLEO-L552ZE-Q|Examples|ITIM

The RTC comes with:

• A firmware driver API abstracting TIM features for the end-user Refer to stm3215xx_hal_rtc.cand stm3215xx_hal_rtc_ex.c filesin ISTM32Cube_FW_L5_Vx.y.z\Drivers|STM32L5xx_HAL_Driverl A set of example projects in \STM32Cube_FW_L5_Vx.y.z\Projects| NUCLEO-L552ZE-Q|Examples|IRTC

# 6.2

# X-CUBE-RTC for smooth calibration

X-CUBE-RTC shows an implementation of the smooth digital calibration feature of the RTC using also the GPTIMER HAL API).

In this example, the RTC_CLK is smoothly calibrated based on an external 1 Hz reference (STM32CubeExpansion_AN4759_RTC_STM32L_Vx.y.ZlProjectsINUCLEO-L552ZE-QIRTC_SmoothCalib).

The firmware implements:

A GPTIMER (general-purpose timer) in Master mode using channel 1 in output compare mode (and using an external trigger clock)   
A GPTIMER in Master mode using channel 1 in input capture mode and channel 2 in output compare mode   
This timer is also configured to use the LSE clock thanks to the TIM option register.   
The RTC with the CALR register programming   
GPIOs to connect the input 1 Hz reference clock and the "corrected" RTC_OUT_CALIB clock

# 6.3

# Smooth calibration application example (STM32L5)

# 6.3.1 Hardware setup

In order to use the application example project, the user needs a STM32L552ZE-Q Nucleo board (NUCLEO-L552ZE-Q)

![](images/dc8c51846220f1e9f7ef984e9ebdf42120eaaa31d93a56a49b69198d9e0f39fd.jpg)  
Figure 24. NUCLEO-L552ZE-Q board

Note: this picture is not contractual.

Supply the board using the USB cable and perform the following actions:

Connect PE2 to a signal generator driving 1 Hz clock with 3.3 V amplitude. It is advised to control the generated frequency at few ppm.   
C  o euacecmentel e of 1 pm).

# 6.3.2

# Software setup

Open the project under the user favorite IDE. For IAR Embedded Workbench, open the RTCmothCalib.   
file.For MDK-ARM, open the RTCSmoothCalib.uvprojx fle. For STM32CubelDE, open the.cproject file.

Compile and launch the debug session. It loads the program in the internal Flash memory and executes t.

After a maximum of 64 seconds, make a frequency measurement of the CALIB_OUT clock on PB2. The user get a frequency accurate at 1 ppm compared to the 1 Hz reference clock sent on PE2.

The user can then modify the PE2 clock by few ppm, wait 64 seconds, and check that the PB2 clock has been changed accordingly.

Under debugger, the user can monitor the evolution of the CALR register fields (CALP and CALM).

# 6.3.3

# Smooth calibration principle

Figure 21 provides a block diagram of the smooth digital calibration application.

This application is based on the following steps:

1A 1 Hz reference clock is connected to TIM3 through the PE2 GPIO. is configured to generate a rising edge after 2 x 1 Hz reference rising edges. This gives an event evey   
32 s.   
3. TM  un  L    al generated by TIM3, and to store it in TIM2_CCR1 register. Then, TIM2 counter is reset.   
4. The Cortex-M33 core gets the TIM2_CCR1 value, compares it with the number of CLK_RTC cycles expected in 32 s and processes the comparison results to update the CALP and CALM[8:0] in RTC_CALR.

The calibration is continuous.

# 3.4 Run time observations

The following steps are needed to check the correct functionality:   
Modify the 1 Hz reference clock (for instance by forcing 1.0001 Hz).   
Wait 2 x 32 s.   
Measure the output frequency. Depending on the accuracy of the generator and the measurement device used, the user can see around 1 ppm accuracy.

The user can also monitor in Debug mode:

CALP and CALM[8:0] in RTC_CALR TIM2_CCR1 register (contains the number of CLK_RTC cycles within a 32 s window)

# STM32L5 API and synchronization application example

STM32CubeL5 firmware libraries are the same as in Section 6.1.

# 7.1

# X-CUBE-RTC for synchronization application

X-CUBE-RTC shows an implementation of the RTC calendar synchronization with the HSE (provided by an external signal: HSE bypass feature used)

(STM32CubeExpansion_AN4759_RTC_STM32L_Vx.y.zlProjects|NUCLEO-L552ZE-QIRTC_Synchronization)

The firmware implements:

TIM1 in Master mode with update interrupt activated to generate an interruption each second. It is configured to exploit an external 16 MHz signal thanks to the bypass of HSE clock. A PLL is also used for the timer to be clocked by a 100 MHz signal.   
the RTC with the SHIFTR register programming   
GPIO: RTC_OUT CALIB to check if the RTC 1 Hz output frequenc is real 1 Hz (synchronzation does not affect the RTC_OUT CALIB output but this signal needs to be as close as possible to 1 Hz for the synchronization to work)   
The user LED2 (PB7) is used to visualize the 1-s period and the good working of the application.

# 7.2

# Synchronization application example (STM32L5)

# 7.2.1 Hardware setup

In order to use the application example project, the user needs a STM32L552ZE-Q Nucleo board (NUCLEO-L552ZE-Q). Supply the board using the USB cable.

The TIM1 clock source is HSE. However, the X3 crystal associated to HSE is not implemented by default on the Nuc boarThe,heplication eplot heH byass ctinality he 32 iput extel MHz signal to substitute the crystal (for this feature, the user must have SB142 ON, SB145 ON, SB143 OFF, SB OFF,SB7 OFF). This signal must be generated on PH0 (position 29 on CN11, right next to the connection A1f CN9).

Tal HS c o c  haEhccTC.   
the HSE external 16 MHz signal must be more precise than the LSE.

Teeha e eu ear  l on PB2 (RTC_OUT CALIB output).

# 7.2.2 Software setup

Open the project under the userfavorite IDE. For IAR Embeded Workbench, open the RTCSynchronization ww file.For MDK-ARM, open the RTcSyncronizatin.uvprj file.For STM32CubeDE, open thecprjet file.

Compile and launch the debug session. It loads the program in the internal Flash memory and executes t.

# Synchronization application principle

This application is based on the following steps:

TIM1 is configured and launched to generate an interruption each second (APB2 timer clock = 100 MHz).   
2.RTC is configured and launched including its calendar (RTC clock = LSE).   
The 1-second period counted by the TM1 interruptions allows a more precise time base than with RTC the external HSE bypass signal must be more precise than LSE).   
With this time base and thanks to the subsecond register, the advance/delay of the RTC clock can be analysed on the TIM1 1-second period.   
5With the SHIFTR register, this advance or delay is compensated.

The synchronization is continuous.

# 7.2.4 Run time observations

The following steps are needed to check the correct functionality:

Set the SYNCHRO_ACTIVATED to 0 and observe the time_elapsed variable deriving (getting away from 255/1 sec). The user can monitor it in Debug mode.   
Set the SYNCHRO_ACTIVATED to 1 and observe that the time_elapsed variable derivation is less important.

time _elapsed embodies the 1-second period measured for RTC.

# Note:

Atypial quartzhas anncertainty /monthThisncertainty must betenuated wit synchronizatita sefcient if the clockused (external 16 MHz in the prent case) has a betterncerainty. Using an HE X3 crystal is not so efficient if the LSE crystal has the same uncertainty.

Tha pl o ealizheL the RTC_OUT CALIB output on the PB2 pin (these two observations do not witness the efficiency of the synchronization but can help the user to understand what happens).

# 8 STM32L5 API and reference clock detection application example

STM32CubeL5 firmware libraries are the same as in Section 6.1.

# X-CUBE-RTC for reference clock detection application

X-CUBE-RTC shows an implementation of the reference clock detection (STM32CubeExpansion_AN4759_RTC_STM32L_Vx.y.ZIProjectsINUCLEO-L552ZE-QIRTC_RefClockDetection).

The firmware implements:

TIM1 in Master mode with update interrupt activated to generate an interruption each second. It is configured to use the HSI clock through a PLL to be clocked by a 100 MHz signal (HSI is less precise than the LSE clocking the RTC but allows the measure of the RTC period without the need to inject another signal than the 50/60 Hz one).   
the RTC with the activation of the reference clock detection feature   
GPIO: RTC_OUT CALIB (PB2) to check if the RTC 1 Hz output frequency is really 1 Hz. The user LED2 (PB7) to visualize the 1-second period and the good working of the application. The RTC_REFIN pin (PB15) to host the 50/60 Hz signal used as the reference clock detected.

# 8.2

# Reference clock detection application example

# 8.2.1 Hardware setup

In order to use the application example project, the user needs a STM32L552ZE-Q Nucleo board (NUCLEO-L552ZE-Q). Supply the board using the USB cable.

Asat heplatam eeencclocmust elie at th goal,heuer as  take  0/6 z ial moe prei than he  clck  the Nuco boarad inject it on the PB15 pin (position 26 on CN12 of the Nucleo board).

Teha  euear  l on PB2 (RTC_OUT CALIB output).

# .2.2

# Software setup

Open the project under the user favorite IDE. For IAR Embedded Workbench, open the RcSynchronizati fe.For MD-ARM, en theRTCSnizatinvx file.For STM32CubeDE, en file.

Compile and launch the debug session. It loads the program in the internal Flash memory and executes it.

# 8.2.3

# Reference clock detection principle

This application performs the following steps:

TIM1 is configured and launched to generate an interruption each second (APB2 timer clock = 100 MHz).   
RTC is configured and launched including its calendar and reference clock detection feature (RTC clock = LSE).   
When the 50/60 Hz signal is available on PB15, the RTC automatically aligns the rising edges of this reference clock with the ones of the output of the synchronous RTC prescaler (1 Hz clock). Thus, the RTC 1 Hz clock is synchronized with the signal provided by the user.   
4. The 1-second period counted by the TM1 interruptions allows the measure of the RTC perid. The HSI TIM clock source) is less precise than the LSE (RTC clock source). The LSE is synchronized with an even more precised reference clock by the way. Thus, this measure is made for testing the application.

by LSE.

# 8.2.4

# Run time observations

The following steps are needed to check the correct functionality:

Set the CLK_REF_ACTIVATED to 0 and observe the time_elapsed variable deriving (getting away from 255/1 s). The user can monitor it in Debug mode.   
Set the CLK_REF _ACTIVATED to 1 and observe that the time_elapsed variable derivation is less important.

time _elapsed embodies the 1-second period measured for RTC.

# Note:

Atypia quarthasanrtaintyont.Thrainty mus ttuat wit theeren detection and synchronization.

Movehcha el  po eus an oialzheL ik seond and the RTC_OUT CALIB output on PB2 pin (these two observations do ot witness the ffienc f he reference synchronization).

# STM32L5 API and internal tamper detection application example

# 9.1

# X-CUBE-RTC for internal tamper detection application

X-CUBE-RTC shows an implementation of the internal tamper detection in the folder: STM32CubeExpansion_AN4759_RTC_STM32L_Vx.y.z\Projects|NUCLEO-L552ZE-Q \RTC_InternalTamperCalOvf

This example uses the RTC firmware driver API mentioned in Section 6 and Section . It is develope r the NUCLEO-L552ZE-Q board and exploits the ITAMP5 signal associated to a RTC calendar overflow event.

Tmus plye uc boarU,he p  nit  pee  F IAR Embeded Workbench, open the RTCSynchronization.eww file. For MDK-ARM, open the RTCSyncroniz ation.uvprojx file. For STM32CubelDE, open the . cproject file.

The X-CUBE-RTC simply configures the RTC calendar at 23:59:30 on the 31st of December of the year xx99 and activates the internal tamper 5. The user can choose the polling mode or interrupt mode with the ITAMP_INTERRUPT constant in main. h: 1 is interrupt mode, 0 is polling mode.

Wh e pas ,hetal  v s n egreeu   poll the blue user LED2 PB7 if in interrupt mode, is turned on.

RTC_DR and RTC_TR allow the contents of the RTC calendar to be observed in debug mode.

The user can easily modify this example to exploit all the others internal tamper event sources.

# Revision history

Table 22. Document revision history   

<table><tr><td colspan="1" rowspan="1"></td><td colspan="1" rowspan="1"></td><td colspan="1" rowspan="3">ChangesInitial release.</td></tr><tr><td colspan="1" rowspan="1">Date</td><td colspan="1" rowspan="1">Version</td></tr><tr><td colspan="1" rowspan="1">26-May-2016</td><td colspan="1" rowspan="1">1</td></tr><tr><td colspan="1" rowspan="1">25-Oct-2016</td><td colspan="1" rowspan="1">2</td><td colspan="1" rowspan="1">Updated:Table 1: Applicable products adding product series and part number.Figure 3: STM32F2, STM32F4, STM32L0 and STM32L1 Series RTC clock sourCes.Figure 4: STM32F0, STM32F3, STM32F7, STM32L4 and STM32WB Series RTC clock sourCeSTable 3: Calendar clock equal to 1 Hz with different clock sourcesSection 1.4: Digital smooth calibration adding the RTC calibration basicsTable 14: Advanced RTC featuresSection 4.3.3: LED meaningnew Section 5: STM32L4 API and digital smooth calibration application exampleSection 6.3.1: Hardware setupSection 6.3.2: Software setupSection 7: Reference documentation</td></tr><tr><td colspan="1" rowspan="1">11-May-2017</td><td colspan="1" rowspan="1">3</td><td colspan="1" rowspan="1">Updated:Figure 4: STM32F0, STM32F3, STM32F7, STM32L4 and STM32WB Series RTC clock sourCesTable 3: Calendar clock equal to 1 Hz with different clock sources adding noteSection 1.4.1: RTC calibration basicsSection 1.11.1: RTC register write protectionTable 14: Advanced RTC features RTC calibration for STM32F2 Series</td></tr><tr><td colspan="1" rowspan="1">11-Feb-2019</td><td colspan="1" rowspan="1">4</td><td colspan="1" rowspan="1">Updated:Table 1 with the STM32WB SeriesSection 1: Overview of the STM32 MCUs advanced RTCFigure 4: STM32F0, STM32F3, STM32F7, STM32L4 and STM32WB Series RTC clock sourCesAdvanced RTC features tableRemoved Section 7. Reference documentation.</td></tr><tr><td colspan="1" rowspan="1">12-Feb-2020</td><td colspan="1" rowspan="1">5</td><td colspan="1" rowspan="1">Updated:IntroductionTable 1: Applicable productsSection 1: Overview of the STM32 MCUs advanced RTC: new Table 2: RTC/TAMP typesversus features and new Table 3: RTC type versus STM32 productsTable 4: Advanced RTC2 featuresnew Table 5: Advanced RTC3 featuresTable 6: Steps to initialize the calendarFootnote Table 7: Calendar clock equal to 1 Hz with different clock sourcesSection 2.1.4: RTC clock configurationTable 8: Steps to configure the alarmSection 2.3.2: Alarm sub-second configurationSection 2.4: RTC periodic wakeup unitTable 1: Steps to configure the auto-wakeup unitSection 2.5.2: Methodology paragraph and Figure 10: Smooth calibration block for RTC3 withLPCAL=1Section 2.9: Timestamp functionSection 2.10: RTC tamper detection functionSection 2.11: Backup registersSection 2.12: Alternate function RTC outputsSection 2.13: RTC safety aspectsSection 2.1 Reducing power consumption</td></tr><tr><td colspan="1" rowspan="1">12-Feb-2020(cont'd)</td><td colspan="1" rowspan="1">5</td><td colspan="1" rowspan="1">Added:Section 2.1.5: Calendar firmware examplesSection 2.4.3: Wakeup firmware examplesSection 2.8: RTC prescaler adjustment with LSI measurementsSection 2.10.4: Active tamper detection (RTC3 only)Figure 17: Tamper detection</td></tr><tr><td>Date</td><td>Version</td><td>Changes</td></tr><tr><td rowspan="7"></td><td rowspan="7"></td><td>Section 2.10.7: Tamper detection firmware examples</td></tr><tr><td colspan="1">Section 6: STM32L5 API and digital smooth calibration application example</td></tr><tr><td colspan="1">Section 7: STM32L5 API and synchronization application example</td></tr><tr><td colspan="1">Section 8: STM32L5 API and reference clock detection application example</td></tr><tr><td colspan="1"></td></tr><tr><td colspan="1">Section 9: STM32L5 API and internal tamper detection application example</td></tr><tr><td colspan="1">Updated with the STM32U5 Series:</td></tr><tr><td rowspan="7">4-Jun-2021</td><td rowspan="7">6</td><td>Introduction Table 2. RTC/TAMP types</td></tr><tr><td colspan="1">Table 3. RTC type on STM32 MCUs</td></tr><tr><td colspan="1">STM32H7 in Table 4. Advanced features for RTC2 type</td></tr><tr><td colspan="1">STM32U5 in Table 5. Advanced features of RTC3 type</td></tr><tr><td colspan="1">Notes in Figure 1. RTC calendar fields</td></tr><tr><td colspan="1">Example in Section 2.3.1.2 Configure the alarm behavior using the MSKx bits</td></tr><tr><td colspan="1"></td></tr><tr><td rowspan="7"></td><td rowspan="7"></td><td>Note in Section 2.4.2.3 Periodic timebase/wakeup configuration for clock configuration 3 Caution in Section 2.6 Synchronize the RTC</td></tr><tr><td colspan="1">Section 2.10.3 Action on tamper detection event</td></tr><tr><td colspan="1">Section 2.10.5 Internal tamper detection (RTC3 only)</td></tr><tr><td colspan="1">Section 2.11 Backup registers</td></tr><tr><td colspan="1">Section 2.13.2 Enter/exit initialization mode</td></tr><tr><td colspan="1">Titles and structure of to Section 3 to Section 9</td></tr><tr><td colspan="1">Added:</td></tr><tr><td rowspan="2">20-Sep-2021</td><td rowspan="2"></td><td>Section 2.2 Binary and mixed modes (RTC3 only) Section 2.10.6 Potential detection management (RTC3 only)</td></tr><tr><td colspan="1">Updated:</td></tr><tr><td rowspan="2">08-Nov-2022</td><td rowspan="2">7</td><td>Section 2.1.5: Calendar firmware examples Figure 9. Smooth calibration block for RTC2 type</td></tr><tr><td colspan="1">Updated: Section Introduction to add the STM32C0 and the STM32H5 Series.</td></tr><tr><td>12-Mar-2024</td><td>9</td><td>Table 5. Advanced features of RTC3 type. Section 2.10.5: Internal tamper detection (RTC3 only) to update the internal tamper list. Section 2.10.7: Tamper detection firmware examples Section 2.14.5: Low-power management firmware examples Updated: Document title Table 1. Applicable products</td></tr><tr><td></td><td>10</td><td>Table 3. RTC type on STM32 MCUs Table 4. Advanced features for RTC2 type Table 5. Advanced features of RTC3 type Section 2.13.3: RTC clock synchronization Updated: Table 1. Applicable products Table 3. RTC type on STM32 MCUs</td></tr><tr><td>30-Jan-2025</td><td></td><td>Table 4. Advanced features for RTC2 type and Table 5. Advanced features of RTC3 type Section 2.8: RTC prescaler adjustment with LSI measurements Section 2.11: Backup registers Section 2.14.5: Low-power management firmware examples</td></tr></table>

# Contents

# 1 Overview of the STM32 MCUs advanced RTC

# Advanced RTC features. 4

# 2.1 RTC calendar. 9

2.1.1 Software calendar. 10   
2.1.2 RTC hardware calendar 10   
2.1.3 Initialize the calendar 11   
2.1.4 RTC clock configuration 11   
2.1.5 Calendar firmware examples 12

2.2 Binary and mixed modes (RTC3 only) 13

# 2.3 RTC alarms 13

2.3.1 RTC alarm configuration . 13   
2.3.2 Alarm subsecond configuration . 15   
2.3.3 Alarm firmware examples 16

# 2.4 RTC periodic wakeup unit 17

2.4.1 Program the auto-wakeup unit 17   
2.4.2 Maximum and minimum RTC wakeup period 17   
2.4.3 Wakeup firmware examples 19

# 1.5 Smooth digital calibration. 19

2.5.1 RTC calibration basics 19   
2.5.2 RTC calibration methodology 20

# Synchronize the RTC 22

RTC reference clock detection 22

RTC prescaler adjustment with LSI measurements 23

# Timestamp function. 24

2.9.1 Timestamp firmware examples 25

# |0 RTC tamper detection function 25

2.10.1 Edge detection on tamper input 25   
2.10.2 Level detection on tamper input .26   
2.10.3 Action on tamper detection event 27   
2.10.4 Active tamper detection (RTC3 only). . 28   
2.10.5 Internal tamper detection (RTC3 only). 29   
2.10.6 Potential detection management (RTC3 only). 30   
2.10.7 Tamper detection firmware examples 30

# .11 Backup registers 30

2.12 Alternate function RTC outputs. 31

2.12.1 RTC_CALIB output. 31   
2.12.2 RTC_ALARM (RTC2)/TAMPALRM (RTC3) output 32

# 13 RTC safety aspects. 32

2.13.1 RTC register write protection. 32   
2.13.2 Enter/exit initialization mode 33   
2.13.3 RTC clock synchronization 33

2.14 Reduce power consumption 33

2.14.1 Use the right power reduction mode 34   
2.14.2 Use internal pull-up resistor on tamper pin 34   
2.14.3 Set RTC prescalers. 34   
2.14.4 External optimization factors . 34   
2.14.5 Low-power management firmware examples 34

2.15 RTC3 secure and privileged protection modes 35

# STM32L4 API and tamper detection application example .36

3.1 STM32CubeL4 firmware libraries for tamper detection 36

3.2 X-CUBE-RTC for tamper detection. 36

3.3 Tamper detection application example (STM32L4). 38

3.3.1 Hardware setup. 38   
3.3.2 Software setup 38   
3.3.3 LED meaning 39   
3.3.4 Tamper detection during normal operation 39   
3.3.5 Tamper detection when main power supply is off 39

# STM32L4 API and smooth digital calibration application example .40

4.1 STM32CubeL4 firmware libraries for smooth calibration 40

4.2 X-CUBE-RTC for smooth calibration 40

4.3 Smooth calibration application example (STM32L4) 41

4.3.1 Hardware setup. 41   
4.3.2 Software setup 41   
4.3.3 Smooth calibration application principle 42   
4.3.4 Run time observations 42   
4.3.5 Porting suggestions. 42

# 5 STM32L0 API and tampering detection application example .43

5.1 STM32CubeL0 firmware libraries 43   
5.2 X-CUBE-RTC for tamper detection. .43   
5.3 Tamper detection application example (STM32L0). . 43   
5.3.1 Hardware setup. 43   
5.3.2 Software setup 44   
5.3.3 LED meaning 44   
5.3.4 Tampering detection during normal operation. 45

# STM32L5 API and smooth digital calibration application example. .46

6.1 STM32CubeL5 firmware libraries for smooth calibration application 46

6.2 X-CUBE-RTC for smooth calibration 46

6.3 Smooth calibration application example (STM32L5) 47

6.3.1 Hardware setup. 47   
6.3.2 Software setup 47   
6.3.3 Smooth calibration principle 48   
6.3.4 Run time observations 48

# STM32L5 API and synchronization application example .49

7.1 X-CUBE-RTC for synchronization application 49

7.2 Synchronization application example (STM32L5). 49

7.2.1 Hardware setup. 49   
7.2.2 Software setup 49   
7.2.3 Synchronization application principle 49   
7.2.4 Run time observations 50

# STM32L5 API and reference clock detection application example .. .51

8.1 X-CUBE-RTC for reference clock detection application. 51

8.2 Reference clock detection application example 51

8.2.1 Hardware setup. 51   
8.2.2 Software setup 51   
8.2.3 Reference clock detection principle. 51   
8.2.4 Run time observations 52

# STM32L5 API and internal tamper detection application example . .53

9.1 X-CUBE-RTC for internal tamper detection application 53

Revision history .54

List of tables 59

List of figures. .60

# List of tables

Table 1. Applicable products   
Table 2. RTC/TAMP types . 2   
Table 3. RTC type on STM32 MCUs. 3   
Table 4. Advanced features for RTC2 type 4   
Table 5. Advanced features of RTC3 type . 7   
Table 6. Steps to initialize the calendar 11   
Table 7. Calendar clock ck_spre= 1 Hz with various clock source. 12   
Table 8. Steps to confirm alarm A. 14   
Table 9. Alarm combinations 14   
Table 10. Alarm subsecond mask combinations (RTC2 type). 16   
Table 11. Steps to configure the auto-wakeup unit 17   
Table 12. Timebase/wakeup unit period resolution with clock configuration 1 18   
Table 13. Min. and max. timebase/wakeup period when RTCCLK= 32768 19   
Table 14. Timestamp features 24   
Table 15. Tamper features (edge detection). 26   
Table 16. Tamper features (level detection). 27   
Table 17. RTC_CALIB output frequency versus clock source. 32   
Table 18. Tamper detection status when a power-on reset is detected 45   
Table 19. Tamper detection status when a tamper event is detected (after a power-on reset). 45   
Table 20. Tamper detection status when a reset is detected 45   
Table 21. Tamper detection status when a tamper event is detected (after a reset). 45   
Table 22. Document revision history . 54

# List of figures

Figure 1. RTC calendar fields. 10   
Figure 2. Example of calendar displayed on an LCD 10   
Figure 3. Prescalers from RTC clock source to calendar unit 12   
Figure 4. Alarm A fields . 13   
Figure 5. Alarm subsecond field 15   
Figure 6. Prescalers connected to the timebase/wakeup unit for configuration 1 18   
Figure 7. Prescalers connected to the wakeup unit for configurations 2 and 3. 18   
Figure 8. Typical crystal accuracy plotted against temperature 20   
Figure 9. Smooth calibration block for RTC2 type 21   
Figure 10. Smooth calibration block for RTC3 type (LPCAL = 1). 21   
Figure 11. RTC shift register 22   
Figure 12. RTC reference clock detection 23   
Figure 13. Timestamp event procedure . 24   
Figure 14. Tamper with edge detection 25   
Figure 15. Tamper with level detection 26   
Figure 16. Tamper sampling with precharge pulse 27   
Figure 17. Tamper detection 28   
Figure 18. Application example flowchart 37   
Figure 19. STM32L476G-EVAL board. 38   
Figure 20. NUCLEO-L476RG board 41   
Figure 21. Block diagram of a smooth digital calibration 42   
Figure 22. NUCLEO-L053R8 board 43   
Figure 23. LED LD2 behavior. 44   
Figure 24. NUCLEO-L552ZE-Q board. 47

# IMPORTANT NOTICE  READ CAREFULLY

pt old ursant  dits   leole.

purchasers' products.

No license, express or implied, to any intellectual property right is granted by ST herein.

are the property of their respective owners.

I

© 2025 STMicroelectronics - All rights reserved