# STM32 SMBus/PMBus ™M expansion package for STM32Cube ™M

# Introduction

This document describes the X-CUBE-SMBUS, STM32 SMBus/PMBus™ (system management bus/power management bus) firmware stack.

This stack is based on the specific STM32Cube ™M HAL drivers available for all STM32 series, with the exception of older devices, in particular STM32F1, STM32F2, STM32F4 and STM32L1 series. These older devices are limited to SMBus 2.0 and are not compatible with the stack described in this AN. All other STM32 series (introduced after STM32F3) contain an I2C peripheral supporting the SMBus/PMBus ™m stack introduced in this document. Some series are presented with examples. Others can have the stack configured using the STM32CubeMX embedded software package, X-CUBE-SMBUS.

The SMBus was founded to standardize the power management related to internal communications, both in devices and in electronic systems. The SMBus builds on the widely adopted I2C bus and defines the links and network layers of the OSI (open systems interconnection) model.

The PMBus™ uses the SMBus as its physical layer and adds command definitions along with other new features. Most of the new features fall into medium-to-high layers of the OSl model. The PMBus ™ specifications are presented in this application note detailing the different aspects of their implementation.

The X-CUBE-SMBUS firmware provides the means to get information from the attached devices such as their manufacturer, their version and their capabilities. Once these informations are retrieved, the devices can be configured and managed using the SMBus transmitted commands.

By using this firmware, the devices also have the capability to asynchronously inform the bus host about events and errors. In its basic configuration the bus can be used to suspend and wake up simple devices. Figure 1 presents a snapshot of the system architecture.

![](images/a205cc5b32e1a7df77d70615b4e6d88006b05a710edbf42408ffe3ed8a32b395.jpg)  
Figure 1. X-CUBE-SMBUS system architecture

# Contents

General information 9

Resources 10

# Features supported by the stack . . 11

3.1 SMBus features 11   
3.2 PMBus features 11

# SMBus stack handle . 12

4.1 The handle structure 12

4.1.1 StateMachine 12   
4.1.2 Device 12   
4.1.3 ARP_UDID . 13   
4.1.4 CurrentCommand 13   
4.1.5 CMD_table . 13   
4.1.6 CMD_tableSize 13   
4.1.7 TheZone 13   
4.1.8 Byte_count . . 13   
4.1.9 SlaveAddress 13   
4.1.10 OwnAddress 14   
4.1.11 OpMode 14   
4.1.12 SRByte . 14   
4.1.13 Buffer 14

4.2 State machine explained 14

# 4.3 Command descriptor 18

4.3.1 cmnd_code .18   
4.3.2 cmnd_query .18   
4.3.3 cmnd_master_Tx_size 18   
4.3.4 cmnd_master_Rx_size .18

# SMBus stack API interfaces . .. 19

5.1 Callbacks 19  
5.1.1 STACK_SMBUS_AlertClbk 19  
5.1.2 STACK_SMBUS_AddrAccpt .19

5.1.3 STACK_SMBUS_LocateCommand 19

5.1.4 STACK_SMBUS_ExecuteCommand. 20

5.2 Host specific commands 20

5.2.1 STACK_SMBUS_HostCommand 20   
5.2.2 STACK_SMBUS_HostRead 21

3 Device specific commands 21

5.3.1 STACK_SMBUS_NotifyHost 21   
5.3.2 STACK_SMBUS_SendAlert 2   
5.3.3 STACK_SMBUS_ExtendCommand. 21

# 5.4 ARP specific commands 22

5.4.1 STACK_SMBUS_LocateCommandARP 22   
5.4.2 STACK_SMBUS_ExecuteCommandARP 22

# Common functions . . 23

5.5.1 STACK_SMBUS_Init .23   
5.5.2 STACK_SMBUS_GetBuffer . . 23

5.6 Useful macros defined by the stack 23

5.6.1 STACK_SMBUS_IsReady 23   
5.6.2 STACK_SMBUS_IsError 23   
5.6.3 STACK_SMBUS_IsBusy 23   
5.6.4 STACK_SMBUS_IsAlert 23

5.7 Private functions 24

5.7.1 STACK_SMBUS_ResolveContext . .24   
5.7.2 STACK_SMBUS_ReadyIfNoAlert .24

# SMBus operation overview .. 25

6.1 Host side 25

6.1.1 Quick command 26   
6.1.2 Send byte 28   
6.1.3 Receive byte 29   
6.1.4 Receive byte with PEC 30   
6.1.5 Write byte . 32   
6.1.6 Write word, Write 32 and Write 64 33   
6.1.7 Read byte 34   
6.1.8 Read word, Read 32 and Read 64 35   
6.1.9 Process call 36   
6.1.10 Block write 37   
6.1.11 Block read .38   
6.1.12 Block write - Block read process call 40   
6.1.13 Alert response . 42

# 6.2 Device side 43

6.2.1 Receive byte/Quick command read confusion 43   
6.2.2 Quick command write 45   
6.2.3 Send byte 46   
6.2.4 Write byte. 47   
6.2.5 Write word, Write 32 and Write 64 49   
6.2.6 Read byte 51   
6.2.7 Read word, Read 32 and Read 64 53   
6.2.8 Process call 55   
6.2.9 Block write 57   
6.2.10 Block read 59   
6.2.11 Block write - Block read process call 61   
6.2.12 SMBus alert 63

# 6.3 Address resolution protocol (ARP) 64

6.3.1 Host side 64   
6.3.2 Device side 64   
6.4 Known limitation 65

# PMBus support 66

7.1 Command support 66

7.2 PMBus stack API extensions 66

7.2.1 STACK_PMBUS_HostCommandGroup 66   
7.2.2 Extended command 66   
7.2.3 Zone commands .67

# Configuration . . . 70

8.1 The software package 70

8.1.1 Configuring the interface in the HAL 70   
8.1.2 Configuring the stack 71   
8.1.3 Generating the project 71

8.2 Manual configuration 71

8.2.1 HW initialization 71   
8.2.2 Registering the IRQs 72   
8.2.3 Initializing the driver.. 72   
8.2.4 Initializing the stack 72   
8.2.5 Optimization 73   
8.2.6 Conclusion 73

# Project example . . . 74

9.1 Hardware setup 74   
9.2 Configuration 74   
9.3 Functioning of the example 75

# 10 Revision history 76

# List of tables

Table 1. Definitions. .9   
Table 2. StateMachine attribute bits 15   
Table 3. Command query modes 18   
Table 4. Document revision history 76

# List of figures

Figure 1. X-CUBE-SMBUS system architecture .2   
Figure 2. Simplified state transition diagram 17   
Figure 3. Quick command write - sequence diagram 26   
Figure 4. Quick command read - sequence diagram. 27   
Figure 5. Send byte - sequence diagram. 28   
Figure 6. Receive byte - sequence diagram 29   
Figure 7. Receive byte with PEC OK - sequence diagram 30   
Figure 8. Receive byte with PEC error - sequence diagram 31   
Figure 9. Write byte - sequence diagram. 32   
Figure 10. Write word - sequence diagram 33   
Figure 11. Read byte - sequence diagram. 34   
Figure 12. Read word - sequence diagram 35   
Figure 13. Process call - sequence diagram 36   
Figure 14. Block write - sequence diagram 37   
Figure 15. Block read - sequence diagram - Part_1 38   
Figure 16. Block read - sequence diagram - Part_2 39   
Figure 17. Block write - Block read process call - sequence diagram - Part_1 40   
Figure 18. Block write - Block read process call - sequence diagram - Part_2 41   
Figure 19. SMBus alert treatment, master side - sequence diagram.. 42   
Figure 20. Receive byte processing - sequence diagram . 44   
Figure 21. Quick command write (slave side) - sequence diagram 45   
Figure 22. Send byte (slave side) - sequence diagram.. 46   
Figure 23. Write byte (slave side) - sequence diagram - Part_1 47   
Figure 24. Write byte (slave side) - sequence diagram - Part_2 48   
Figure 25. Write word (slave side) - sequence diagram - Part_1. 49   
Figure 26. Write word (slave side) - sequence diagram - Part_2. 50   
Figure 27. Read byte (slave side) - sequence diagram Part_1 51   
Fiigure 28. Read byte (slave side) - sequence diagram Part_2 52   
Figure 29. Read word (slave side) - sequence diagram - Part_1. 53   
Figure 30. Read word (slave side) - sequence diagram - Part_2. 54   
Figure 31. Process call (slave side) - sequence diagram - Part_1. 55   
Figure 32. Process call (slave side) - sequence diagram - Part_2. 56   
Figure 33. Block write (slave side) - sequence diagram - Part_1. 57   
Figure 34. Block write (slave side) - sequence diagram - Part_2. 58   
Figure 35. Block read (slave side) - sequence diagram - Part_1. 59   
Figure 36. Block read (slave side) - sequence diagram - Part_2. 60   
Figure 37. Block write - Block read process (slave side) - sequence diagram - Part_1. 61   
Figure 38. Block write - Block read process (slave side) - sequence diagram - Part_2. 62   
Figure 39. Alert signal processing (slave side) - sequence diagram 63   
Figure 40. Pinout & Configuration 70   
Figure 41. SMBus physical layer . 72

# General information

Th ae tack apple3Arm®bas .

# arm

Table 1. Definitions   

<table><tr><td rowspan=1 colspan=1>Term</td><td rowspan=1 colspan=1>Description</td></tr><tr><td rowspan=1 colspan=1>Alert</td><td rowspan=1 colspan=1>Wired signal, active low, notifying SMBus host about urgency onSMBus device by an interrupt.</td></tr><tr><td rowspan=1 colspan=1>ARA</td><td rowspan=1 colspan=1>Alert response address</td></tr><tr><td rowspan=1 colspan=1>ARP</td><td rowspan=1 colspan=1>Address resolution protocol</td></tr><tr><td rowspan=1 colspan=1>HAL</td><td rowspan=1 colspan=1>Hardware abstraction layer (drivers)</td></tr><tr><td rowspan=1 colspan=1>LSb</td><td rowspan=1 colspan=1>Least significant bit</td></tr><tr><td rowspan=1 colspan=1>LSB</td><td rowspan=1 colspan=1>Least significant byte</td></tr><tr><td rowspan=1 colspan=1>Master</td><td rowspan=1 colspan=1>Master is any device that initiates SMBus transactions anddrives the clock.</td></tr><tr><td rowspan=1 colspan=1>MSb</td><td rowspan=1 colspan=1>Most significant bit</td></tr><tr><td rowspan=1 colspan=1>MSB</td><td rowspan=1 colspan=1>Most significant byte</td></tr><tr><td rowspan=1 colspan=1>MSP</td><td rowspan=1 colspan=1>MCU specific package</td></tr><tr><td rowspan=1 colspan=1>PEC</td><td rowspan=1 colspan=1>Packet error check</td></tr><tr><td rowspan=1 colspan=1>PMBus</td><td rowspan=1 colspan=1>Power management bus</td></tr><tr><td rowspan=1 colspan=1>PSA</td><td rowspan=1 colspan=1>Persistent address</td></tr><tr><td rowspan=1 colspan=1>Slave</td><td rowspan=1 colspan=1>Slave is a target of an SMBus transaction which is driven bysome master.</td></tr><tr><td rowspan=1 colspan=1>SMBus</td><td rowspan=1 colspan=1>System management bus</td></tr><tr><td rowspan=1 colspan=1>SMBus host</td><td rowspan=1 colspan=1>A host is a specialized master that provides the main interfaceto the system CPU. A host is a master-slave and supports theSMBus host notify protocol. There may be at most one host in asystem.</td></tr><tr><td rowspan=1 colspan=1>SMBus device</td><td rowspan=1 colspan=1>A device may be designed so that it is never a master andalways a slave. A device may act as a slave most of the time,but in special cases it may become a master. A device can alsobe designed to be a master only. A system host is an exampleof a device that acts as a host most of the time but that includessome slave behavior.</td></tr><tr><td rowspan=1 colspan=1>UDID</td><td rowspan=1 colspan=1>Unique device identifier - ARP specific value</td></tr></table>

# 2 Resources

1System Management Bus (SMBus) Specification Version 3.0 from www.smbus.org

2. PMBus Power Management Bus Specification Part I - Revision 1.3.1 from www.pmbus.org

3. PMBus Power Management Bus Specification Part II - Revision 1.3.1 from www.pmbus.org

4. PMBus Power System Management Protocol Application Note AN001 from www.pmbus.org

# Features supported by the stack

# 3.1 SMBus features

The stack supports the following types of SMBus transactions (bus protocols) based on reference [1]:

• Quick command   
• Send byte   
• Receive byte   
• Read byte/word   
• Write byte/word   
• Block write/read   
• Process call   
• Block process call   
• SMBus host notify protocol   
• ARP   
• Zone commands   
• PEC integrity protection   
• Alert signal supported with an automated alert protocol treatment

Note:

The Quick command, Receive byte and Zone read handling are implemented with limitations (see Section 6.4 for more details).

The implementation has been tested with 100 kHz, 400 kHz, and 1 MHz bus speeds with the STMicroelectronics Nucleo or Discovery boards.

Features not supported:

• Control signal   
• Write protect   
• Pin-driven address configuration   
• Host side ARP management   
• Any persistent attributes (the stack uses non-volatile data storage of its own)

These features are left for the customer to finish, as their implementation cannot be generalized.

# 3.2 PMBus features

The PMBus extends the above mentioned SMBus functionalities adding:

• Group command protocol   
• Command table filled with command descriptors to ease application implementation   
• Limited extended command support

The PMBus specification supported by X-CUBE-SMBUS firmware, is limited to part I and part Il of the specification. The AVSBus™ (adaptive voltage scaling bus) interface described in part Ill of the specification is not supported at the moment of writing this application note (See Section 2 for complete reference of the specifications).

# 4 SMBus stack handle

Each SMBus related action is called and executed with respect of the values and the settings stored at the SMBus stack handle structure. This structure keeps the basic peripheral configuration, the internal state machine status of the stack and the communicated data in the l/O buffer.

Some MCUs may support multiple SMBus connections using separate physical interfaces.   
Each physical interface must have its own stack handle.

# 4.1 The handle structure

The structure type is defines as follows:

typedef struct   
{ uint32_t StateMachine; SMBUS_HandleTypeDef\* Device; uint8_t\* ARP_UDID; st_command\* CurrentCommand; st_command\* CMD_table; uint32_t CMD_tableSize; SMBUS_ZoneStateTypeDef TheZone; uint16_t Byte_count; uint16_t SlaveAddress; uint8_t OwnAddress; uint8_t OpMode; uint8_t SRByte; uint8_t Buffer[];   
}   
SMBUS_StackHandle;

The structure attributes are explained in details in the following sections.

TheZone structure is part of the handle only if conditional flag PMBUS13 is defined. The structure is described in detail in Zone configuration and associated data structure.

# 4.1.1 StateMachine

The StateMachine holds the current processing state and any error encountered. Neat macros are defined to ease extraction of useful information from the StateMachine. For more information, refer to Chapter 4.2.

# 4.1.2 Device

Pointer to the HAL SMBUS handle that is linked to this stack. It keeps information about the HW peripheral instance and its SMBUS related configuration.

# 4.1.3 ARP_UDID

Pointer to the unique device ID used for address resolution protocol. This pointer may refer to a read only memory location. SMBus stack never attempts to modify this information.

# 4.1.4 CurrentCommand

Pointer to the command descriptor definition of a command currently processed. It usually points inside the command table. The command descriptor structure is documented in Section 4.3.

# 4.1.5 CMD_table

Pointer to the start of the list of supported command descriptors. It must be set before the stack initialization call. The command descriptors must follow the structure described in Section 4.3. The PMBus source file contains a predefined table with the PMBus commands defined in reference [3].

# Note:

The stack by default searches for command definitions in CMD_table. For an alternate solution, the pointer can be redirected to another command descriptor list. Command table search method is implemented and may be modified in the STACK_ SMBUS_LocateCommand function (refer to Section 5.1.3). In some special cases as the ARP, the stack bypasses this table and look elsewhere (refer to Section 6.3).

# 4.1.6 CMD_tableSize

Number of commands listed in CMD_table. It must be set before the stack initialization call.

# 4.1.7 TheZone

This structure maintains information about the read and the write zones assigned to the device when the zone support feature is enabled. Then also contains information about read and write zones currently used. The content of the structure is checked by slave devices to handle the zone command flow. For further information, refer to Chapter 7.2.3

# 4.1.8 Byte_count

The actual position in l/O buffer. The application function may use this value to check size of the input after calling the STACK_ SMBUS_GetBuffer command(Section 5.5.2).

# 4.1.9 SlaveAddress

It is used by the host to store the address of the device that the stack is currently communicating with.

It is used by the slave to remember the address under which the command that is currently being processed was accepted. It is useful both for devices that support more than one address as well as for general call and zone access.

# 4.1.10 OwnAddress

It must be initialized with the value of the device address, or left as zero in case of the device relying on the ARP. For host, this attribute stores the received address after the alert signal treatment, as the host is only addressed in the host's notify command.

# Note:

For ARP enabled systems, it is important to initialize this attribute with the correct value if the device has either the ARP_AV or ARP_AR flag set by default (refer to Section 4.2) having fixed or persistent address. The same principle applies for Alert signal usage.

# 4.1.11 OpMode

Internal value, here the stack among else stored the value of direction option for the current command. It uses values defined in cmnd_query (refer to Section 4.3.2).

# 4.1.12 SRByte

Simple response byte preset. This value is used as reply in case the Receive byte transaction comes. This value gets its MSb forced to one before reply transmission if flag RCV_BYTE_LMT is set (refer to Section 4.2).

# 4.1.13 Buffer

The common l/O buffer used for the SMBus communication. It is not recommended to access the buffer directly but rather to use the STACK_ SMBUS_GetBuffer (Section 5.5.2) function call. The buffer size is based on the STACK_NBYTE_SIZE HAL compilation parameter, indicating the maximum amount of user data transferred in the command. The user can modify this constant to balance the capability and the footprint.

# 4.2 State machine explained

The state machine states are coded by a combination of flags in the StateMachine attribute of the SMBUS_StackHandle. The StateMachine is a 32 bit unsigned integer used as register bitmap of flags.

Reset value is Ox00000000 and is defined as SMBus_sMS_NONE.

In the code, all state machine defines start with SMBUS_SMS_ prefix, unlike here in this section where only the variable part of the identifier is used.

Table 2. StateMachine attribute bits   

<table><tr><td rowspan=1 colspan=9>31          30         29         28          27         26         25          24</td></tr><tr><td></td><td rowspan=1 colspan=1>Res</td><td rowspan=1 colspan=1>ARP_AM</td><td rowspan=1 colspan=1>ARP_AR</td><td rowspan=1 colspan=1>ARP_AV</td><td rowspan=1 colspan=1>Res</td><td rowspan=1 colspan=1>PEC_ACTIVE</td><td rowspan=1 colspan=1>RCV_BYTE_LMT</td><td rowspan=1 colspan=1>RCV_BYTE_OFF</td></tr><tr><td></td><td rowspan=1 colspan=1>-</td><td rowspan=1 colspan=1>r</td><td rowspan=1 colspan=1>rw</td><td rowspan=1 colspan=1>r</td><td rowspan=1 colspan=1>-</td><td rowspan=1 colspan=1>W</td><td rowspan=1 colspan=1>W</td><td rowspan=1 colspan=1>W</td></tr><tr><td rowspan=1 colspan=9>23          22         21          20          19          18          17          16</td></tr><tr><td></td><td rowspan=1 colspan=1>ERRPECERR</td><td rowspan=1 colspan=1>Res</td><td rowspan=1 colspan=1>ERR_BTO</td><td rowspan=1 colspan=1>ERR_HTO</td><td rowspan=1 colspan=1>ERR_OVR</td><td rowspan=1 colspan=1>ERRACKF</td><td rowspan=1 colspan=1>ERR_ARLO</td><td rowspan=1 colspan=1>ERRBERR</td></tr><tr><td></td><td rowspan=1 colspan=1>r/reset</td><td rowspan=1 colspan=1></td><td rowspan=1 colspan=1>r/reset</td><td rowspan=1 colspan=1>r/reset</td><td rowspan=1 colspan=1>r/reset</td><td rowspan=1 colspan=1>r/reset</td><td rowspan=1 colspan=1>r/reset</td><td rowspan=1 colspan=1>r/reset</td></tr></table>

<table><tr><td>15</td><td>14</td><td>13</td><td>12</td><td>11</td><td>10</td><td>9</td><td>8</td></tr></table>

<table><tr><td rowspan=1 colspan=1>Res</td><td rowspan=1 colspan=1>Res</td><td rowspan=1 colspan=1>QUICKCMD_W</td><td rowspan=1 colspan=1>QUICKCMD_R</td><td rowspan=1 colspan=1>Res</td><td rowspan=1 colspan=1>Res</td><td rowspan=1 colspan=1>ERROR</td><td rowspan=1 colspan=1>ZONE_READ</td></tr><tr><td rowspan=1 colspan=1>-</td><td rowspan=1 colspan=1>-</td><td rowspan=1 colspan=1>r/reset</td><td rowspan=1 colspan=1>r/reset</td><td rowspan=1 colspan=1>-</td><td rowspan=1 colspan=1>-</td><td rowspan=1 colspan=1>r/reset</td><td rowspan=1 colspan=1>-</td></tr></table>

<table><tr><td rowspan=1 colspan=1>ALERTADDRESS</td><td rowspan=1 colspan=1>ALERT_PENDING</td><td rowspan=1 colspan=1>IGNORED</td><td rowspan=1 colspan=1>RESPONSE_READY</td><td rowspan=1 colspan=1>PROCESSING</td><td rowspan=1 colspan=1>RECEIVE</td><td rowspan=1 colspan=1>TRANSMIT</td><td rowspan=1 colspan=1>READY</td></tr><tr><td rowspan=1 colspan=1>r/reset</td><td rowspan=1 colspan=1>r</td><td rowspan=1 colspan=1>r</td><td rowspan=1 colspan=1>r</td><td rowspan=1 colspan=1>r</td><td rowspan=1 colspan=1>r</td><td rowspan=1 colspan=1>r</td><td rowspan=1 colspan=1>r</td></tr></table>

Bit 31 Reserved

Bit 30 ARP_AM: Address resolution protocol address match (ARP command)

Bit 29 ARP_AR: Address resolution protocol address resolved flag processing

Bt 28 ARP_AV: Address resolution protocol address valid flag

Bit 27 Reserved

Bit 26 PEC_ACTIVE: PEC feature activation flag It must remain the same during all operations.

RCV_BYTE_LMT: All Receive byte slave responses are ORed with Ox80, to prevent stalling the bus.

RCV_BYTE_OFF: Any direct read is treated as Quick command read to prevent stalling the bus with attempted data transmission.

Bit 23 ERR_PECERR: PEC error - data integrity lost

Bit 22 Reserved

3it 21 ERR_BTO: Bus timeout

Bit 20 ERR_HTO. Timeout error

Bit 19 ERR_OVR: Overrun/underrun error It enables SCL stretching to prevent this error.

Bit 18 ERR_ACKF: ACK failure error - probably wrong slave address.

Bit 17 ERRARLO: Arbitration lost error The device lost the bus. Usually the slave wants to transmit but master stops, frequent with Quick command read.

Bit 16 ERR_BERR: BuS error Misplaced start or stop, try lower-speed.

Bits 15:14 Reserved

Bit 13 QUICK_cMD_W: A Quick command write was received (device-specific). This is a notification flag. The application must reset it after taking appropriate action.

Bit 12 QUICK_cMD_R: A Quick command read was received (device-specific). This is a notification flag. Up to the application to reset it once the command is treate

Bits 11:10 Reserved

Bit 9 ERROR: Any other error.

8 zONE_READ: Flag set on a slave device to indicate that the status read is not completed.

7 ALERT_ADDRESS: Alert signal treated, address read (host-specific) This is a notification flag the application must reset each time the stack sets it.

Bit 6 ALERT_PENDING: Alert signal detected, address not known yet Most likely the host retrieves the address automatically soon.

Bit 5 IGNORED: Arbitration lost or command is refused by software The stack ignores the rest of the current command frame. Particularly important for process call and read commands, where there are two address matches.

Bt 4 RESPONSE_READY: Slave has a command reply ready for transmission in the I/O buffer.

Bt  EssIG: Processing block flag (variable length transmission)

Bt 2 REEIVE: State of receiving data on the bus

B  ST: Sae f wrting data o he us

Bt 0 READ: The stack is listening and ready to process a request.

Note:

The HAL driver has its own state machine, working with lower-level and more detailed states during the communication processing. The state machines are loosely related by function calls, interrupt requests and callbacks.

![](images/163250c97f0366217928a1c2d29eca9fb90983df001e33d3613b18c8a64cc895.jpg)  
Figure 2. Simplified state transition diagram   
Figure 2 illustrates basic state transitions based on flags in StateMachine (listed in Table 2). In this diagram both states error and notification represent flags marked as r/reset (read and reset) in Table 2. These flags are set by the stack and the application should reset them after taking appropriate action.

In Figure 2, the blue color lines indicate HAL calls, while the black lines represent the application and the stack.

For more detailed flows specific to different transaction types, please see Section 6.

# 4.3 Command descriptor

This section describes the format of items included at the command table (Section 4.1.5). These records represent supported commands that are provided as parameter to function STACK_SMBUS_HostCommand (Section 5.2.1).

Each record has to follow this exact structure:

typedef struct { uint8_t cmnd_code; uint8_t cmnd_query; uint8_t cmnd_master_Tx_size; uint8_t cmnd_master_Rx_size;   
} st_command;   
where the attributes roles are described in the next sections.

# 4.3.1 cmnd_code

This is a command code. It is the first byte written in most transaction types, identifying the command and subsequent data meaning.

# 4.3.2 cmnd_query

This attribute determines the supported command types. The command code may be used in write/read transactions, in process call, in block transfer and in combinations thereof. It indicates which values the OpMode (Section 4.1.11) may assume while processing this particular command.

The allowed values are shown in Table 3.

Table 3. Command query modes   

<table><tr><td rowspan=1 colspan=1>Identifier</td><td rowspan=1 colspan=1>Value</td><td rowspan=1 colspan=1>Description</td></tr><tr><td rowspan=1 colspan=1>READ</td><td rowspan=1 colspan=1>0x20</td><td rowspan=1 colspan=1>Read operation / fixed size read only command</td></tr><tr><td rowspan=1 colspan=1>WRITE</td><td rowspan=1 colspan=1>0x40</td><td rowspan=1 colspan=1>Write operation / fixed size write only command</td></tr><tr><td rowspan=1 colspan=1>READ_OR_WRITE</td><td rowspan=1 colspan=1>0x60</td><td rowspan=1 colspan=1>Command executed either as read or as write of fixed size</td></tr><tr><td rowspan=1 colspan=1>BLOCK_READ</td><td rowspan=1 colspan=1>0x30</td><td rowspan=1 colspan=1>Read block operation / read only command</td></tr><tr><td rowspan=1 colspan=1>BLOCK_WRITE</td><td rowspan=1 colspan=1>0x50</td><td rowspan=1 colspan=1>Write block operation / write only command</td></tr><tr><td rowspan=1 colspan=1>BLK_PRC_CALL</td><td rowspan=1 colspan=1>0x90</td><td rowspan=1 colspan=1>Block process call - write, then read, variable sizes</td></tr><tr><td rowspan=1 colspan=1>PROCESS_CALL</td><td rowspan=1 colspan=1>0x80−</td><td rowspan=1 colspan=1>Simple process call - write, then read, fixed sizes</td></tr><tr><td rowspan=1 colspan=1>BLK_RD_OR_WR</td><td rowspan=1 colspan=1>0x70</td><td rowspan=1 colspan=1>Command can be executed either as read or as write of variable size</td></tr></table>

# 4.3.3 cmnd_master_Tx_size

Number of bytes transmitted from the host, including the command code byte.

# 4.3.4 cmnd_master_Rx_size

Number of bytes transmitted in the slave response.

# 5 SMBus stack API interfaces

This section describes the functions and macros provided for the application layer.

# 5.1 Callbacks

Callback functions are meant to be implemented in the user application. The stack only implements these functions as weak to support that substitution. The number of callbacks was reduced to keep the application role simple and the execution efficient:

# 5.1.1 STACK_SMBUS_AlertCIbk

Parameter:

pStackContext - Pointer to a SMBUS_StackHandle structure that contains the configuration information for the specified SMBus (Section 4).

No return value.

This callback is specific to the host side. It informs the application that the address has been retrieved from the slave that just recently sent an alert address.

# 5.1.2 STACK_SMBUS_AddrAccpt

Parameters:

pStackContext - Pointer to a SMBUS_StackHandle structure (Section 4)

AddrMatchCode - Address match code, 16-bit unsigned intege

Returns the ErrorStatus response code.

The stack asks the application whether to accept call with a particular address, intended for more complex devices that serve a range of addresses.

# 5.1.3 STACK_SMBUS_LocateCommand

Parameter:

pStackContext - Pointer to a SMBUS_StackHandle structure (Section 4).

No return value.

This function is defined as weak, to provide easy means for the application to redefine the way the structured command information is located within the command table. Implementation is also modifiable by compile time switches ARP and DENSE_CMD_TABLE. Slave specific.

# 5.1.4 STACK_SMBUS_ExecuteCommand

Parameter:

pStackContext - Pointer to a SMBUS_StackHandle structure (Section 4).

Returns the HAL_StatusTypeDef response code.

This call represents the command processing implementation.

This function performs the following actions:

1. Get the command code or flag from the stack handle. If the current command pointer is NULL, this function checks the state machine (Section 4.2) for flags indicating the codeless commands (Quick command read and Quick command write).

# Note:

The Receive byte bus transaction is an exception, the slave command callback is not called for it.

2. Get the input/output buffer pointer (function STACK_ SMBUS_GetBuffer (Section 5.5.2) if necessary.   
3. Perform the command action.   
4. If applicable, provide the response to the command to the input/output buffer.

# 5.2 Host specific commands

# 5.2.1 STACK_SMBUS_HostCommand

Parameters:

pStackContext - Pointer to a SMBUS_StackHandle structure (Section 4).

pCommand - pointer to command descriptor of the command to be transmitted, NULL for Quick command.

address - slave address to be used in the transmission, 16-bit unsigned integer.

direction - either READ or WRITE, some commands have the choice with the same ordinal.

Do not use BLOCK_READ and BLOCK_WRITE. It is tied to command definition and implicit. Leave zero for process call, 32 bit unsigned integer type.

Returns the HAL_StatusTypeDef response code.

Call this function with selected parameters to send a command to the bus. This function serves to perform Quick command write, Send byte, Write byte/word, Read byte/word, Process call and all block transfers.

For most commands, it is necessary to first call function STACK_ SMBUS_GetBuffer (Section 5.5.2), and prepare the command output data.

# 5.2.2 STACK_SMBUS_HostRead

Parameters:

pStackContext - Pointer to a SMBUS_StackHandle structure (Section 4).

data - pointer to the 8-bit integer variable where response should be stored.

address - slave address to be used in the transmission, 16-bit unsigned integer.

Returns the HAL_StatusTypeDef response code.

Simplified call with no command code and read-only transmission. This function can be used by the bus master to issue Quick command read or Receive byte.

# 5.3 Device specific commands

# 5.3.1 STACK_SMBUS_NotifyHost

Parameter:

pStackContext - Pointer to a SMBUS_StackHandle structure (Section 4).

Returns the HAL_StatusTypeDef response code.

Initiates the host notify protocol by assuming master role and transmitting the command.

# 5.3.2 STACK_SMBUS_SendAlert

Parameter:

pStackContext - Pointer to a SMBUS_StackHandle structure (Section 4).

No return value.

Initiates the alert response protocol by issuing the alert signal.

Note:

The signal itself is only the first step of the whole protocol. For the process to conclude correctly the OwnAddress must be initialized in the stack handle.

# 5.3.3 STACK_SMBUS_ExtendCommand

Parameter:

pStackContext - Pointer to a SMBUS_StackHandle structure (Section 4).

No return value.

A callback added for users wanting to customize the Extended command processing (see Section 7.2.2 or protocol specification for more details). Called when received input command code equals the Extend command reserved value.

# 5.4 ARP specific commands

The address resolution protocol introduces several irregularities to the SMBus functionality, namely command processing. For the ARP to work correctly, the device must be configured as discoverable (DEV_DIS build option defined. For further information, refer to Section 9.2). To process the ARP commands correctly, following functions are introduced:

# 5.4.1 STACK_SMBUS_LocateCommandARP

Parameter:

pStackContext - Pointer to a SMBUS_StackHandle structure (Section 4).

No return value.

This is a subroutine of the STACK_SMBUS_LocateCommand (Section 5.1.3) called in case of ARP (device addressed on ARP default address). It bypasses the search for command in the main command table and identifies the ARP applicable command.

# 5.4.2 STACK_SMBUS_ExecuteCommandARP

Parameter:

pStackContext - Pointer to a SMBUS_StackHandle structure (Section 4).

Returns the HAL_StatusTypeDef response code, zero means success.

This function is called instead of the regular STACK_SMBUS_ExecuteCommand (Section 5.1.4) in case of ARP (device addressed on ARP default address). It directly implements the actions needed to finish these commands.

# 5.5 Common functions

# 5.5.1 STACK_SMBUS_Init

Parameter:

pStackContext - Pointer to a SMBUS_StackHandle structure (Section 4).

Returns the HAL_StatusTypeDef response code, zero means success.

Initializing the SMBus stack. It can only be done successfully after the HAL initialization finished.

# 5.5.2 STACK_SMBUS_GetBuffer

Parameter:

pStackContext - Pointer to a SMBUS_StackHandle structure (Section 4).

Returns pointer to the stack l/O buffer, array of bytes.

Function called to retrieve the input/output buffer pointer.

Note:

Though the pointer remains the same value, it is still recommended to keep calling this function each time to make sure the buffer is available for use.

# 5.6

# Useful macros defined by the stack

# 5.6.1

# STACK_SMBUS_IsReady

Return value is 1 in case the stack is ready to process a new command (not busy), 0 otherwise.

# 5.6.2 STACK_SMBUS_IsError

Return value is 1 if serious error occurred on the SMBus, or else 0.

# 5.6.3

# STACK_SMBUS_IsBusy

Return value is 1 if a communication is ongoing, or 0 in case it is not.

# 5.6.4 STACK_SMBUS_IsAlert

Return value is 1 if the host stack has the address of the slave that asserted alert signal obtained, otherwise it is 0.

# 5.7 Private functions

# 5.7.1 STACK_SMBUS_ResolveContext

Parameter:

hsmbus - Pointer to a SMBUS_HandleTypeDef structure (from HAL) that contains the configuration information for the specified SMBus.

Returns pointer to the stack SMBUs_StackHandle structure.

Used by the stack to link the stack handle with physical device, useful for applications with multiple SMBus interfaces.

# 5.7.2 STACK_SMBUS_ReadylfNoAlert

Parameter:

pStackContext - Pointer to a SMBUS_StackHandle structure (Section 4).

No return value.

The function used to automate conclusion of a transaction on the host side.

# SMBus operation overview

This section describes the typical flow of calls and events at application, stack, and HAL levels when executing commands for both host side and device side of the SMBus stack.

The key differences between commands are highlighted using bold type in the following figures.

# 6.1 Host side

A properly initialized SMBus stack is only conveying commands, not taking any action by itself. The exception to this rule is the alert signal and the host notify protocol functionality. Each time the stack detects an alert signal assert, it automatically retrieves the slave address of the device that issued the alert. When the previous action is successful, the master stack notifies the application using a callback function. In a similar manner, there is a callback for the host notify.

On the master device, the application calls a stack API function to initiate the command sent to the slave. Sending a command consists of the following five simple steps:

1. Retrieve the I/O buffer pointer from the stack by calling STACK_SMBUS_GetBuffer (Section 5.5.2). The stack checks its readiness before returning the pointer.   
2. Prepare the command output data, if any. This is excluding the command code. Only write to the appointed buffer one byte for a Send byte command, or two bytes for a Send word. There is no check done by the stack on completeness or integrity of the message in buffer. Only exception is a forced hardcap on amount of data in block transfer to STACK_NBYTE_SIZE (defined at compile time).   
3. Call the STACK_SMBUS_HostCommand (Section 5.2.1) or STACK_SMBUS_HostRead (Section 5.2.2) to initiate the SMBus communication.   
4. Poll the stack status for command completion using STACK_ SMBUS_IsBusy (Section 5.6.3) or STACK_ SMBUS_IsReady (Section 5.6.1) macros. Make sure no errors were reported by the stack (STACK_SMBUS_IsError (Section 5.6.2)).   
5. Optionally read the slave response data from the l/O buffer.

For more details about a particular transaction type processing, refer to the sequence diagrams in the next sections.

# 6.1.1

# Quick command

The Quick command is used generally for small devices that have limited support of SMBus.

# Quick command write

![](images/da76a7a3f68708bec4b7da4f966fdc45ed54d5e6939d29483b2cc22af6d83d2f.jpg)  
Figure 3. Quick command write - sequence diagram   
ACBC L \*command descriptor parameter.

![](images/b7c4f65d03fd5f979c987ee1b175a328fce74ed096d3b3156d5456142d41e838.jpg)  
Figure 4. Quick command read - sequence diagram

ubACBUL parameter.

# 6.1.2 Send byte

Avav .   
All or part of the data byte contribute to a "command code".

![](images/e6c40a42e887c70d781c09b5b8c6f72f41323a9f7355f9a7299e56418212fcc3.jpg)  
Figure 5. Send byte - sequence diagram

The Send byte command descriptor has WRITE for cmnd_query and 1 for cmnd_master_Tx_size.

# 6.1.3 Receive byte

The Receive byte is similar to a Send byte. The only difference is the direction of transfer.

A "NACK" (1 in the Ack bit) means the end of transfer.

![](images/1dac1d3f97dbe982f6c301ff3f41ccc78717a896697fabae16fd3e91990a4a22.jpg)  
Figure 6. Receive byte - sequence diagram

STACK_ SMBUS_HostRead with valid pointer as \*data parameter.

# 6.1.4 Receive byte with PEC

Au

StateMachine during an ongoing communication.

![](images/b130d2ab915db5a9618255ea8e5cc25100f15dedf5ee63554f6254b5e109364f.jpg)  
Figure 7. Receive byte with PEC OK - sequence diagram

![](images/3b0af982d68c10ca2a21cd801ef60adc66d4777d1f79df1c4743065ce9d42260.jpg)  
Figure 8. Receive byte with PEC error - sequence diagram

STACK_ SMBUS_HostRead with valid pointer as \*data parameter.

# 6.1.5 Write byte

The first byte of a Write byte is the command code.

The next byte is the data to be written.

![](images/3e1f4b445251f183de19f16a7f6e85316aa812029070cef32af6640e50c50a94.jpg)  
Figure 9. Write byte - sequence diagram   
The Write byte command descriptor has WRITE for cmnd_query and 2 for cmnd_master_Tx_size.

# 6.1.6 Write word, Write 32 and Write 64

T protocols) are the data to be written

![](images/995a1a7519c91f19837af80f5d9e925437842e2ca605912e92adcb6e98255211.jpg)  
Figure 10. Write word - sequence diagram

The Write word command descriptor has WRITE for cnd_query and 3 for cnd_masterTx_size. Write 32 has cmnd_master_Tx_size of 5. In the case of Write 64, it is equal to 9.

# 6.1.7 Read byte

The first byte of a Read byte is the command code.

The next one is the read data. Between these two parts, a repeated start condition is necessary.

![](images/898598e01e0e6b855fe128cec7b9b5cc1dfc2cf7fa3da08c614f88353cb2a378.jpg)  
Figure 11. Read byte - sequence diagram   
The Read byte command descriptor has READ for cmnd_query and value 1 for both cmnd_master_Tx_size and cmnd_master_Rx_size.

# 6.1.8 Read word, Read 32 and Read 64

T protocols) are the read data. Between these two parts, a repeated start condition is necessary.

![](images/a028cfe29589bcb91e25962a9c50af1283debacdb18c339db3713d84c9214bcd.jpg)  
Figure 12. Read word - sequence diagram

ThR o aecpoas EAD  nd_quey  nase_in   nd_mastRx_ie Wr32has ndmastrRx_sze. In thecase Writ,  is qual  The es ais he.

# 6.1.9 Process call

T W

![](images/0e6243998a683896ab5bcef6b2abaad4b92ba6fd7dab1f20e721b4fdc711bac4.jpg)  
Figure 13. Process call - sequence diagram

L8l and 2 for cmnd_master_Rx_size. The sizes may be different.

# 6.1.10 Block write

message.

![](images/8190ff57b446fec16e55596906d22d5adf4355262ec936f3a5fae4982ba961a8.jpg)  
Figure 14. Block write - sequence diagram

T w LCRT   qunei   s cmnd_master_Tx_size. The cmnd_master_Rx_size remains 0.

# 6.1.11 Block read

describes how many bytes follow the message from the slave.

![](images/f8577adf40abc089911842b04a500ae1db72af30b019a1fa9ed6726ffe2a718d.jpg)  
Figure 15. Block read - sequence diagram - Part_1

![](images/d9580fb1b4f079ac4793deaf2b59edc0dcd8bd2ca368ae7ec5f986cd9780dbe4.jpg)  
Figure 16. Block read - sequence diagram - Part_2

ThBlock rea can erorhas BLOCKREADor e dque ndvaluhe c code z cmnd_master_Tx_size. The cmnd_master_Rx_size must be at least 2.

# 6.1.12 Block write - Block read process call

command code.

![](images/9da122cff350d36652bb0f580760cd25dfd7bcb2f67c8ae42b70bdd41fe4d84d.jpg)  
Figure 17. Block write - Block read process call - sequence diagram - Part_1

![](images/adce150770d84ffbd09bce98830459681d65bdd3c7aeb7dd21d750cfcedde39d.jpg)  
Figure 18. Block write - Block read process call - sequence diagram - Part_2

TBlc BasBLKRCALequ alst cmnd_master_Tx_size. The cmnd_master_Rx_size must be at least 2.

# 6.1.13 Alert response

The SMBALERT is a third wire and a signal besides the SMBCLK and the SMBDAT.

SMBALERT devices through the alert response address (ARA = Ox18).

![](images/3dd85a9678b8b215954fddef12ea05c79a45d6dd5fc637c6d434aaa2cc850ff2.jpg)  
Figure 19. SMBus alert treatment, master side - sequence diagram

A

# 6.2 Device side

After initialization, the slave stack sets the driver to listen mode, awaiting for an incoming command. Almost alinteractions with the application layer consist of callbacks, where an appropriate action is expected from the application.

These callbacks are put in place when the stack needs the application to make a decision or to provide data. With a typical command processing, the stack calls the three following most important callbacks:

1. STACK_ SMBUS_AddrAccpt (Section 5.1.2). If the slave device uses only one fixed address, it is not necessary to implement this callback in the user application.   
2. STACK_SMBUS_LocateCommand (Section 5.1.3). Already implemented in the stack, but the user may replace the default implementation with one simpler or more complex, depending on the application needs.   
3. STACK_ SMBUS_ExecuteCommand (Section 5.1.4). This is the actual command processing. The stack holds the information about the command code and inputs data in its handle. Typically the application grabs that available information and uses a switch-case branching to call a particular command function.

For more details about particular transaction type processing, please refer to the sequence diagrams.

The actions where the slave acts actively is the alert protocol and host notify protocol. To alert the SMBus master, simply call STACK_ SMBUS_ SendAlert (Section 5.3.2). The stack asserts the signal and treats automatically the alert response call from master, returning the OwnAddress configured in the stack handle.

The host notify protocol is initiated by calling STACK_SMBUS_NotifyHost (Section 5.3.1) function. The PMBus specifies ([2] and [3]) the contents of the two data bytes of the host notiy. It is the responsibility of the application to prepare this data to the output buffer, before calling the function. The stack automatically uses either the OwnAddress attribute (if valid) or sends the ARP version (own device address not assigned yet).

# 6.2.1 Receive byte/Quick command read confusion

While most transaction types starts with a host writing command code, determining the subsequent action taken, the Quick command read and the Receive byte transactions start with a read frame. It is impossible for the slave to predict whether to expect a STOP condition right after an address (Quick command), or to transmit the prepared byte (Receive byte case). In some cases, this may lead to a situation where the slave device stalls the SDA line by forcing it low, preventing the master to assert a correct STOP condition. This type of situations lead to errors on both sides and to a stack reset after timeout.

There are two flags introduced to the stack specifically to prevent this problem:

SMBUS_SMS_RCV_BYTE_OFF, causing any direct read being treated as Quick command read. No attempt to transmit the data is done. This flag basicaly drops the Receive byte from the list of supported SMBus transactions.   
SMBUS_SMS_RCV_BYTE_LMT. This compromised solution forces the MSb of the Receive byte data byte to a logical one. The master may assert a STOP condition to the bus and complete the Quick command.

If none of these solutions are applied in the final product, the Receive byte works without any limitation. Though any received Quick command read causes an error state.

![](images/5de63d59892fe2eb16de5953fe175278f021e0a9fe5e8602c69551e0bec54a3d.jpg)  
Figure 20. Receive byte processing - sequence diagram

translated to SMBUS_SMS_QUICK_CMD_R flag in the statemachine and STACK_SMBUS_ExecuteComman callback is

# 5.2.2 Quick command write

command write.

![](images/2c658332778d349ed89115ee6198805017c7d9e542d79f4e363d498f1815e90e.jpg)  
Figure 21. Quick command write (slave side) - sequence diagram

The STACK_SMBUS_ExecuteCommand callback finds the CurrentCommand attribute set to NULL, but SMBUS_SMS_QUICK_CMD_Wis set as HAL_SMBUS_ListenCpltCallback finds the stack expecting more data

# 6.2.3 Send byte

For a command with no datainvolved, isees pointless to separate the STACK_SMBUS_LocateCommand and the STACB IMB delay between command code transmission and the actual STOP condition may be substantial.

![](images/cbf966b7df7dbeafb2ee154cb0cab460d0a10f9ab250423d7821692d0d4c3988.jpg)  
Figure 22. Send byte (slave side) - sequence diagram

# 6.2.4 Write byte

TWr Wrworyarav .

![](images/ddd1d6b3061804db4455b66fc9bebbee83d5c6d9dcbbbcc9d691c7ccebabff12.jpg)  
Figure 23. Write byte (slave side) - sequence diagram - Part_1

![](images/3b8bafd098921036a4ee194130e5494402e16d63427810ef1461647d7db0c5fc.jpg)  
Figure 24. Write byte (slave side) - sequence diagram - Part_2

![](images/6b3b07bf163aa64278bdd76d9e0234a456126d77b631d1cd4e251a02c9e19dd3.jpg)  
Figure 25. Write word (slave side) - sequence diagram - Part_1

![](images/621c61b13f88e0430bb68fd540ed81d9b3f74f06758b22aa15d4e5b9b2fc5bac.jpg)  
Figure 26. Write word (slave side) - sequence diagram - Part_2

identified.

![](images/1404d5ee7e8b287c3cc7a9cc0685a832783e4a5480dd9e63dcbaaee9025f7007.jpg)  
Figure 27. Read byte (slave side) - sequence diagram Part_1

![](images/88a58e6521ae6d5e920b13662423804c21143e7f1d4d4bb5e6fd649d05e5901a.jpg)  
Figure 28. Read byte (slave side) - sequence diagram Part_2   
timeout.

![](images/a03ce01c19d7ab3c2f962c49df3162c7f75076d62bb4695e22310530ec76e24c.jpg)  
Figure 29. Read word (slave side) - sequence diagram - Part_1

![](images/f549724663d995479d4e5d046d972f98aaedaed026d98abac24205f45a588d41.jpg)  
Figure 30. Read word (slave side) - sequence diagram - Part_2

T    HALBSai ive R Re identified.

![](images/7393c3a6ef69e4ae9d36420fe150a9a151f83974156524e0a8b11601cab030b8.jpg)  
Figure 31. Process call (slave side) - sequence diagram - Part_1   
20

![](images/b8eeeb6a6556d29574875191c40ada3c865338ba7e949ec9c9898b2ce5e30a59.jpg)  
Figure 32. Process call (slave side) - sequence diagram - Part_2   
20   
The process call execution bears the same execution timing restriction as the other read commands do.

![](images/fdc964fee3f06e2da6cb8f82b58b9b8e0f6d557bcafd88a6b82b70dea31b717e.jpg)  
Figure 33. Block write (slave side) - sequence diagram - Part_1

![](images/e55829e50a72f4dfbba4c2688360c257a06ac7a59379302b8accbb734fff80cd.jpg)  
Figure 34. Block write (slave side) - sequence diagram - Part_2

![](images/cab667ba2676c8947421b45bbcff157b2c57372ceac44947c64400531c3d188b.jpg)  
Figure 35. Block read (slave side) - sequence diagram - Part_1

![](images/c9797159326599249435d2280d6cd1befbe21ac0379156ccaa78d396bce4ef44.jpg)  
Figure 36. Block read (slave side) - sequence diagram - Part_2   
20

returned by GetBuffer.

![](images/97ccfe1b0075c7cb948f1904822e482cbaff866fb0b9ba81f22e35d3fbe40964.jpg)  
Figure 37. Block write -Block read process (slave side) - sequence diagram - Part_1   
20

![](images/3aa5557c93750351568c907b1e3faa8bd5889360d53a4fee67f27e1ae7b79936.jpg)  
Figure 38. Block write - Block read process (slave side) - sequence diagram - Part_2

# 6.2.12 SMBus alert

correctly configured in the stack handle.

![](images/ace59e532949b26433f9b4e29006898b4101d32d99e7816759e0b34789e16678.jpg)  
Figure 39. Alert signal processing (slave side) - sequence diagram

the alert signal. It is then recommended for the application not to de-assert this signal.

# 6.3 Address resolution protocol (ARP)

The ARP enumerates the bus, assigns addresses to all devices needing one, or confirms addresses of devices with address preset. This stack implements a part of the ARP, though some choices and actions, particularly on the host side, are left to be done by the application.

# 6.3.1 Host side

The crucial ARP host structure, the device list, is left on application discretion to be implemented. It may be partially flled with fixed addresses for specific purposes, partially persistent.

The host initiates the ARP automatically on reset, or waits for the ARP host notify command (option implemented in the example). An implementation of an ARP host notify into STACK_SMBUS_ExecuteCommand (Section 5.1.4) is application choice.

Upon reception, the application should initiate the ARP by calling the sequence of ARP commands using the STACK_ SMBUS_HostCommand (Section 5.2.1), and using the templates from the PMBUS_COMMANDS_ARP table collecting specific ARP commands (Chapter 5.4).

# 6.3.2 Device side

The device must have the unique device identifier ARP-UDID initialized in the stack handle and one of the device type - operating modes selected. The device type and behavior is selected compile-time in the present stack version, using DEV_PSA and DEV_DIS define configuration options.

The PeripheralMode item of the SMBUS HAL driver initialization structure has to be initialized to setup proper reaction upon the SMBus default device address (OxC2), preferably by setting the init.PeripheralMode to value   
SMBUS_PERIPHERAL_MODE_SMBUS_SLAVE_ARP.

It is also important for the application to correctly initialize the ARP_AR and ARP_AV flags in the stack state machine (Section 4.2).

If the application needs the bus host to assign an address to the device it runs, the application must call STACK_ SMBUS_NotifyHost (Section 5.3.1). If the OwnAddress field in the stack handle structure is not assigned yet (meaning it equals zero), the stack sends the ARP notify host frame.

# Note:

As the SMBus has no mechanism to prevent bus collision, the application should check the stack handle state machine to see whether the notify host was processed correctly.

The responses to ARP command are then implemented in the stack functions   
STACK_SMBUS_LocateCommand (Section 5.1.3) and   
STACK_SMBUS_ExecuteCommand (Section 5.1.4), which, in the default state, replace the regular ones each time the address is the default device address.

If the application needs to redefine the STACK_SMBUS_LocateCommand, it must then keep the ARP part in the beginning in order for the ARP to work.

Once the ARP is complete and an address is assigned, the stack handle attribute OwnAddress and the ARP_AR and ARP_AV flags are set.

# 6.4 Known limitation

Particularly in the case of the ARP, there may be a situation when a device firmware realizes that it must not respond to a read request. Even though the address decoding finds the acceptable address on the input, sometimes the firmware wants to quit the communication, avoiding to stretch the clock or transmitting any data.

This is not the case in the current implementation, even when there is still room for improvement. It is particularly problem of Address Match Callback function, when IGNORED flag is set in the stack handle state machine.

# PMBus support

# 7.1 Command support

The PMBus stack implementation includes a command table based on reference [3]. The command implementations are not supplied by the stack.

Different versions of the specification used for the command table can be selected in compile-time using defines. More details about defines are found in Section 9.2.

# 7.2 PMBus stack API extensions

# 7.2.1 STACK_PMBUS_HostCommandGroup

Parameters:

pStackContext (Section 4).

pCommand - pointer to the command descriptor of the command to be transmitted, NULL for quick command.

address - slave address to be used in the transmission, 16-bit unsigned integer.

last - parameter set to 1 indicates that STOP condition should conclude this transmission 8-bit unsigned type

Returns the HAL_StatusTypeDef response code.

Group commands are transmitted using the STACK_PMBUS_HostCommandGroup function. For each command in the group, this function has to be called. In between the commands, a call to the STACK_ SMBUS_GetBuffer (Section 5.5.2) can be done to modify the contents of the output buffer.

It is mandatory to make this GetBuffer call (and test it returns valid address) even when the output must remain the same. It ensures synchronicity of the output.

The last call of STACK_PMBUS_HostCommandGroup must have its last parameter set to indicate that the host has to send a STOP condition to the bus.

# 7.2.2 Extended command

This feature of the PMBus enables a support of more commands than what can be selected by the 8-bit command code. This implementation enables transmission and reception of extended commands. However, many actions have to be carried out by the application.

# Host side

A set of predefined st_command structures (extended_read_byte, extended_read_word, extended_write_byte and extended_write_word) should be used with the regular STACK_SMBUS_HostCommand (Section 5.2.1) function. STACK_SMBUS_GetBuffer (Section 5.5.2) sets the command code directly to the output buffer.

# Device side

The device receiving the extended command must have

the regular STACK_ SMBUS_LocateCommand (Section 5.1.3) function redefined in the PMBUS stack source file   
a function that chooses the extended_read_byte template regardless of the selected command table the stack uses. The reason is that all the extended commands share the same base command code.

Extended reads are handled as a process call by the stack

After reception of the real command code, the command implementation SMBUS_STACK_ExecuteCommand callback (Section 5.1.4) is called. At this point, the application assists the stack in determining the actual structure of the transmission through the following steps:

No stack handle modification is required for extended read byte.   
For extended read word, modify the value of CurrentCommand pointer in the actual   
stack to the predefined extended_read_word structure. The stack transmits two data   
bytes in response.   
For Extended write byte, modifying the CurrentCommand pointer is still necessary but   
not sufficient. The application has to: secure it receives the callback again once the reception is complete, by clearing SMBUS_ SMS_RESPONSE_READY flag in the stack state machine (Section 4.2). order reception of an extra byte (call directly the HAL driver function HAL_SMBUS_Slave_Receive_IT). take note that it has already been called for this command once in order not to request another byte from the master again and to perform the actual command action when callback is called the second time for the same command.

Extended write word differs from extended write byte only in number of bytes requested from the driver.

# 7.2.3 Zone commands

This feature was added in the PMBus specification version 1.3 to address the need of a master to issue a command to several slaves at once. For a write command, this feature allows synchronization of the slaves actions. For a read command, it eases the gathering of the information from the system.

To get a complete description of the Zone system, please refer to references [2] and [3]. To enable a Zone support, select PMBus version 1.3 when configuring the stack in the STM32CubeMX or define the conditional flag PMBUS13, described in Section 9.2.

This stack contains provisions to help in the implementation of the Zone commands and to allow basic testing with the SMBus example. This specification also recognizes the separate notions of Read Zones and Write Zones, as there are often different slaves in the data acquisition and control jobs.

ZONE_WRITE and READ_ZONE new addresses are introduced, allow the addressing of all the slaves supporting Zone control at once.

The following sections describe simple wrappers of the STACK_SMBUS_HostCommand defined to ease the use of the Zone feature.

# Zone configuration and associated data structure

The Zone configuration is a regular command addressed to a single device and implemented in STACK_PMBUS_MasterZoneConfig wrapper. Its goal is to configure the device to a specific Read Zone or to a specific Write Zone.

# STACK_PMBUS_MasterZoneConfig

Parameters:

pStackContext - stack context (Section 4).

address - used in the command call zone, pointer to the SMBUS_ZoneStateTypeDef structure with configuration.

Returns HAL_StatusTypeDef as a regular host command.

A structure is defined to help on the use, convey and store of the Zone state.

typedef struct   
{ uint8_t readZone; uint8_t writeZone; uint8_t activeReadZone; uint8_t activeWriteZone;   
} SMBUs_ZoneStateTypeDef;

This structure is part of the SMBus handle structure for each slave on the bus, and is used to identify the commands intended for itself.

# Zone active command

The Zone active command is sent to a ZONE_WRITE address with a ZONE_ACTIVE command code. It is implemented in the stack wrapper function STACK_PMBUS_MasterZoneActive.

# STACK_PMBUS_MasterZoneActive

Parameters:

pStackContext - stack context (Section 4).

zone - pointer to the SMBUs_ZoneStateTypeDef structure with configuration.

Returns HAL_StatusTypeDef as a regular host command.

Each slave on the bus has to check if the new active Zone is identical to the Zone currently configured. After confirmation, the slave is prepared to receive further Zone commands.

# Zone write command

Any command can be sent to the Zone write recipient address, as long as it does not involve any reading (not even as a Block read or a process call). The only difference is in the address value. All the slaves within the active Zone receive and execute the command.

Due to the physical properties of the bus, the ACK nature is OR. The master cannot have then an immediate acknowledge from all the slaves. One acknowledge is enough. The wrapper STACK_PMBUS_MasterZoneWrite is used to transmit the command.

# STACK_PMBUS_MasterZoneWrite

Parameters:

pStackContext - stack context (Section 4).

pCommand - pointer to the command sent to the Zone. NULL for quick command.

Returns HAL_StatusTypeDef as a regular host command.

# Zone read command

The Zone read capability is not mandatory as it requires a special arbitration and a repeated start capability. It is however supported in both Master and Slave modes in its basic form by executing the STACK_PMBUS_MasterReadZoneStatus function wrapper.

# STACK_PMBUS_MasterReadZoneStatus

# Parameters:

pStackContext - stack context (Section 4).   
ccode - control code.   
mask - sent with the read request.

Returns HAL_StatusTypeDef as a regular host command.

# 8 Configuration

The STM32CubeMX GUI tool and the software package generate the correct configuration.   
The steps are detailed in the Section 8.1: The software package.

The manual configuration of the stack is also possible. The steps are described in the Section 8.2: Manual configuration.

# 8.1 The software package

The CubeMX supports the usage of plug-ins, allowing the GUl to:

• configure the software, which is delivered with the software package.   
• project that configuration into the generated project.

After installing the X-CUBE-SMBUS software package, it can be added to the "Pinout & Configuration" tab. This tab is accessible from the "Software packs" dropdown menu.

![](images/d1f065f5510b117373dcf17cfaa0346f82227132c17b599c4d7add065b6e90b1.jpg)

# 8.1.1 Configuring the interface in the HAL

A

Select the suitable I2C instance and all the known parameters, such as the own address, the bus speed and the role (master/slave).   
Select the available GPIOs. Also for Alert if needed.   
Enable all the interrupts in the "NviC settings" tab. The stack operates exclusively in the interrupt mode, and it expects both event and error interrupts that were enabled in the "NVIC Settings" tab from the I2C HAL configuration.   
For ARP and general call support, the "General Call Address Detection" HAL slave setting must be enabled.   
For PMBus 1.3 support of the Zone commands, the "Dual Address Acknowledged" HAL slave setting must be enabled. The recommended settings are Ox40 for the secondary slave address, and Ox05 for the secondary address mask.

# 8.1.2 Configuring the stack

Tick both checkboxes in the software pack upper "Mode" window.

Make sure that the stack configuration matches the HAL configuration. To obtain functional results, the settings for Master/slave, PEC, and alert must be aligned between the stack and the HAL before proceeding to project generation. If the assert option is enabled in the project generation, the generated code checks the settings alignment for basic parameters.

# 8.1.3 Generating the project

After following these steps, it is now possible to generate the project.

The Slave configured device calls by default the STACK_SMBUS_ExecuteCommand() function for each command received. This is the most likely place to start the actual command implementation.

The Master is expected to call STACK_SMBUS_HostCommand() to initiate a communication.

# 8.2 Manual configuration

# 8.2.1 HW initialization

The stack follows the usual STM32Cube software structure. It is necessary to add the I2C l/O configuration to the MSP_init function with the following steps:

1. Enable the clock domain for the I2C.   
2. Properly configure the ports and GPlO alternate function registers, including the alert pin, in case it is used in the application. It is recommended to use an external pull-up as too many internal pull-ups in devices may stall the bus.   
3. Configure and enable the interrupt.

![](images/802b3ea02f2bd67000353b38c44c74f7a84ee6e89c8f4eeba8c2d277b1928165.jpg)  
Figure 41. SMBus physical layer

# 8.2.2 Registering the IRQs

Interrupts are not treated on the stack level. The HAL driver is configured directly. For example, STM32F3 and STM32L4 series have separate interrupt vectors for error and event interrupts, while STM32F0 series and STM32L0 series treat both events and errors in single interrupt vector. The recommended solution is to call first an event handling, following by an error handling in the interrupt service routine.

It is important to correctly assign the vectors to particular instances of HAL driver handles. The stack makes no attempt to automate the resource assignment in this case for performance reasons.

# 8.2.3 Initializing the driver

For details, please refer to the SMBUS HAL driver documentation in the source files.

# 8.2.4 Initializing the stack

The objective of the stack initialization is to register the stack handle instance and to link it with a driver instance and thus a physical interface. Allocate a variable of SMBUs_StackHandle type and set the following attributes:

• CMD_Table - initialize with pointer to a set of supported commands structured   
• CMD_TableSize - set number of records in the supported command stable   
• Device - initialize with pointer to the driver handle APR-UDID - initialize the UDID if ARP code is included.

Additional attributes may need to be initialized:

SRByte - if the device configured supports Receive byte transaction • OwnAddress - ifdevice with PSA - persistent address. This must be initialized. StateMachine - SMBUS_SMS_RCV_BYTE_OFF, SMBUS_SMS_RCV_BYTE_LMT and SMBUS_SMS_PEC_ACTIVE flags must be initialized if used. Same for the ARP_AR and ARP_AV flags, if ARP is used (See Section 4.2 for details).

The initialization is concluded by calling the function STACK_ SMBUS_Init (Section 5.5.1) with pointer to the prepared SMBUS_ StackHandle structure as parameter.

# 8.2.5 Optimization

The example code is not optimized. The primary goal is to provide a solution that is easy to understand, integrate, and maintain. Portability to wide range of STM32 products was also a high priority.

For products with limited amount of available program memory, we suggest to undefine conditional define flags such as ARP or PMBUS13 to drop support of unused features from the built code. It is also possible to define other such flags to limit the functionality to host only or device only, if the complete, full featured, implementation is not necessary.

Furtherotimizations woud probably requie comple rewriting o the stack, probablyusing the low level HAL library.

# 8.2.6 Conclusion

After enabling the interrupts, the SMBus device and the stack are operational.

# 9 Project example

An example code is supplied with this application note, demonstrating the usage of all the SMBus and PMBus features.

The example is developed and tested with Discovery boards of STM32F0, STM32F3, STM32L0, and STM32L4 series. Other devices such as STM32H7 and STM32WB series are tested with Nucleo boards. This section describes the STM32F3 series version as all others are similar but with only one SMBus interface, configured in the example, on different pin numbers. The readme file in each particular project describes the differences.

# 9.1 Hardware setup

Two boards are needed to get a properly working example: one as host and the other as device.

The SCL and SDA pins of the two boards are connected with wires (for example PB6 and PB7 pins for the STM32F3 series Discovery boards). Refer to the readme file provided with the examples to see the pins used on other boards. If the host side does not have internal pull-up configured, external pull-up resistors are needed. It is not recommended to have internal pull-up configured on more devices. To test the alert capability, interconnect the alert pins.

# 9.2 Configuration

Various features and working modes of the example firmware can be configured using the following preprocessor defines:

• SMB1 - define to configure I2C1 to SMBus (Port B)   
• SMB2 - define to configure I2C2 to SMBus (Port A, available in selected examples only)   
• ARP - define to enable the automatic address resolution protocol execution in the code startup   
• DEV_DIS - device is discoverable - reacts to general ARP calls on default address   
• DEV_PSA - device has a persistent address. HOST1  define to configure I2C1 as the bus host. If ARP is defined as well, the host waits for "ARP notify host" command from a device. Otherwise, the host immediately attempts to send loop of test commands to the device on address that goes first in the device list (address Ox1A by default).   
• TEST2 - replaces the first test command with a PMBus group command test.   
• TEST3 - replaces the initial 4 test cases with PMBus extended command tests.   
• TEST4 - replaces the default test group with a set of actual PMBus commands.   
• TEST5 - switch to test the Zone commands.   
• PMBuS12 - includes commands newly added to the PMBus specification in V1.2.   
• PMBuS13 - includes new features such as Zone operations from PMBUS 1.3 and SMBUS 3.0.   
• ALERT - enables an alert signal. It must be defined both in master and slave.   
• USE_PEC - switch to enable packet error checking. Implicitly enabled with ARP.

# 9.3 Functioning of the example

The host-configured Discovery board flashes a LED light while transmitting commands. The device receiving the commands flashes a LED in the frame frequency.

The host mounted user buttons (usually with blue cap) is available to cycle between commands (test cases).

The device mounted user button may be used to send an alert or a notify.

# 10 Revision history

Table 4. Document revision history   

<table><tr><td>Date 17-Oct-2014</td><td>Revision</td><td>Changes</td></tr><tr><td></td><td>1</td><td>Initial release. Updated: — Introduction Section 1: Definitions</td></tr><tr><td>6-Jun-2017</td><td>2</td><td>Section 2: Resources - Section 3: Features Section 3.1: SMBus features -Section 3.2: PMBus features Section 4: SMBus stack context Section 4.1: The context structure Section 4.1.9: SlaveAddress Section 5.1.2: STACK_SMBUS_AddrAccpt Section 5.1.3: STACK_SMBUS_LocateCommand Section 5.1.4: STACK_SMBUS_ExecuteCommand Section 5.2.1: STACK_SMBUS_HostCommand Section 5.2.2: STACK_SMBUS_HostRead - Section 5.3.1: STACK_SMBUS_NotifyHost Section 5.3.2: STACK_SMBUS_SendAlert Section 5.4: ARP specific commands Section 5.4.1: STACK_SMBUS_LocateCommandARP Section 5.4.2: STACK_SMBUS_ExecuteCommandARP Section 5.5.1: STACK_SMBUS_Init Section 5.5.2: STACK_SMBUS_GetBuffer Section 5.7.2: STACK_SMBUS_ReadyIfNoAlert Section 6.1.6: Write word, Write 32 and Write 64 Section 6.1.8: Read word, Read 32 and Read 64 Section 6.2.5: Write word, Write 32 and Write 64 - Section 6.2.7: Read word, Read 32 and Read 64 Section 6.3.2: Device side Section 6.4: Known limitation Section 7.1: Command support Section 8.2: Register the IRQs Section 9.1: HW setup Section 9.2: Configuration — Figure 1: X-CUBE-SMBUS system architecture Figure 2: Simplified state transition diagram Table 2: StateMachine attribute bits Added: Section 4.1.7: TheZone - Section 7.2.3: Zone commands</td></tr><tr><td colspan="1" rowspan="1">Date</td><td colspan="1" rowspan="1">Revision</td><td colspan="1" rowspan="1">Changes</td></tr><tr><td colspan="1" rowspan="1">5-Mar-2019</td><td colspan="1" rowspan="1">3</td><td colspan="1" rowspan="1">Updated:- Title of the document- Introduction- Section 1: General information— Context replaced by handle in most part of the document- Section 3.1: SMBus features Table 2: StateMachine attribute bits— Section 8: Configuration- Section 9: Project exampleAdded:- Section 5.3.3: STACK_SMBUS_ExtendCommand- Section 8.2.5: Optimization</td></tr><tr><td colspan="1" rowspan="1">07-Mar-2023</td><td colspan="1" rowspan="1">4</td><td colspan="1" rowspan="1">Updated:Section : IntroductionSection 3: Features supported by the stackSection 4.1.1: StateMachineSection 4.1.2: DeviceSection 4.1.7: TheZoneSection 4.1.13: BufferTable 2: StateMachine attribute bitsFigure 2: Simplified state transition diagramTable 3: Quick command write - sequence diagramSection 7.2.3: Zone commandsSection 8: ConfigurationSection 8.2: Manual configurationAdded software package and configuration information:Section 8.1: The software package</td></tr></table>

# IMPORTANT NOTICE  PLEASE READ CAREFULLY

acknowledgement.

the design of Purchasers' products.

No license, express or implied, to any intellectual property right is granted by ST herein.

product or service names are the property of their respective owners.

I