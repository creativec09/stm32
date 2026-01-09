# USB DFU protocol used in the STM32 bootloader

# Introduction

This application note describes the USB DFU protocol used in STM32 microcontroller bootloader, detailing each supported command.

This document applies to the STM32 products embedding bootloader versions V3.x, V4.x, V7.x, V9.x, V10.x, V13.x, and V14x, as specified in AN2606 "STM32 microcontroller system memory boot mode" (available on www.st.com), which also contains more information about the USB hardware resources and requirements for the device bootloader. These products are listed in Table 1, and are referred to as STM32 throughout the document.

Table 1. Applicable products   

<table><tr><td>Type</td><td>Series</td></tr><tr><td>Microcontrollers</td><td>STM32C0 series STM32F0 series STM32F1 series STM32F2 series STM32F3 series STM32F4 series STM32F7 series STM32G0 series STM32G4 series STM32H5 series STM32H7 series STM32L0 series</td></tr></table>

# Contents

Bootloader code sequence USB DFU bootloader requests . . DFU bootloader commands . . . . .

# DFU_UPLOAD request commands .. .. 10

4.1 Read memory . 10   
4.2 Get command 10

# DFU_DNLOAD request commands 13

5.1 Write memory 15   
5.2 Set Address Pointer command 16   
5.3 Erase command 17   
5.4 Read Unprotect command 18   
5.5 Leave DFU mode 19

# Bootloader protocol version evolution . .. . . . 21

Revision history 22

# List of tables

Table 1. Applicable products 1   
Table 2. DFU class requests 8   
Table 3. Summary of DFU class-specific requests. 8   
Table 4. DFU bootloader commands .9   
Table 5. Bootloader protocol versions 21   
Table 6. Document revision history 22

# List of figures

Figure 1. Bootloader for STM32 connectivity line devices. 6   
Figure 2. Bootloader for other STM32 devices .7   
Figure 3. DFU_UPLOAD request: device side. 11   
Figure 4. DFU_UPLOAD request: host side 12   
Figure 5. Download request: device side. 13   
Figure 6. Download request: host side 14   
Figure 7. Write memory: device side . 16   
Figure 8. Set Address Pointer command: device side. 17   
Figure 9. Erase command: device side 18   
Figure 10. Read Unprotect command: device side 19   
Figure 11. Leave DFU operation: device side 20

# Bootloader code sequence

There are no differences in terms of protocol (requests and commands) between different bootloader DFU versions. For the detailed difference list, refer to Section 6.

Once the system memory boot mode is entered and the STM32 microcontroller (based on A u configures the USB and its interrupts, and waits for the "enumeration done" interrupt.

The USB enumeration is performed as soon as the USB cable is plugged (or immediately if the cable is already plugged). If the user does not want the microcontroller to enter the USB DFU bootloader application, the USB cable must be unplugged before reset.

The bootloader version is returned in the device descriptor in the MSB of the bcd device field (example: 0x2000 = version 2.0).

For connectivity line USB DFU bootloader, the device first tries the 25 MHz configuration then if it fails, the 14.7456 MHz configuration, and finally, if it fails, the 8 MHz configuration. In case of fail, this operation is repeated with a higher timeout value (the three configurations are tested again). If the second trial fails, a system reset is generated.

![](images/bde158911143030f40659b6f50baebf6c5da76ec0455580feb71401f71cc5038.jpg)  
Figure 1. Bootloader for STM32 connectivity line devices

ai17755

After system reset, the device returns to the BL_DFU loop or executes code from flash memory/RAM, depending upon the connection states and the boot pin status.

Leave DFU is achieved by a 0 data download request followed by GetStatus request and device reset

After six trials (the three clock configurations are tested twice), a system reset is generated.

• If the product uses HSE for the USB operation (except connectivity line):

At startup, the HSE is measured (if present) and, if supported the USB, is configured. If the HSE is not detected the Bootloader performs a system reset. If the measured value of the HSE clock is an unsupported value, the USB protocol does not work correctly.

If the product uses the HSI for the USB operation: At startup the USB is configured using the HSI clock.

Refer to AN2606 for more details about product configuration.

![](images/3c5eb9781015cf339705104cf7603356db7f4f87a332782b520c596916064e70.jpg)  
Figure 2. Bootloader for other STM32 devices   
After system reset, the device returns to the BL_DFU loop or execute code from flash memory/RAM, depending upon the connection states and the boot pin status. 2. Leave DFU is achieved by a 0 data download request followed by GetStatus request and device reset. 3. For some products the external oscllator HSE is not used for USB bootloader operations, only the internal oscillator HSl is used. Check AN2606 to know which oscillator is required for each product.

# USB DFU bootloader requests

The USB DFU bootloader supports the DFU protocol and requests compliant with the "Universal Serial Bus Device Upgrade Specification for Device Firmware Upgrade" version 1.1, Aug 5, 2004. For more details concerning these requests, refer to the specification.

Table 2 and Table 3 detail the DFU class-specific requests and their parameters.

Table 2. DFU class requests   

<table><tr><td rowspan=1 colspan=1>Request</td><td rowspan=1 colspan=1>Code</td><td rowspan=1 colspan=1>Description</td></tr><tr><td rowspan=1 colspan=1>DFU_DETACH</td><td rowspan=1 colspan=1>0x00</td><td rowspan=1 colspan=1>Requests the device to leave DFU mode and enter the application.</td></tr><tr><td rowspan=1 colspan=1>DFU_DNLOAD</td><td rowspan=1 colspan=1>0x01</td><td rowspan=1 colspan=1>Requests data transfer from Host to the device in order to load theminto device internal flash memory. Includes also erase commands.</td></tr><tr><td rowspan=1 colspan=1>DFU_UPLOAD</td><td rowspan=1 colspan=1>0x02</td><td rowspan=1 colspan=1>Requests data transfer from device to Host in order to load contentof device internal flash memory into a Host file.</td></tr><tr><td rowspan=1 colspan=1>DFU_GETSTATUS</td><td rowspan=1 colspan=1>0x03</td><td rowspan=1 colspan=1>Requests device to send status report to the Host (including statusresulting from the last request execution and the state the deviceenters immediately after this request).</td></tr><tr><td rowspan=1 colspan=1>DFU_CLRSTATUS</td><td rowspan=1 colspan=1>0x04</td><td rowspan=1 colspan=1>Requests device to clear error status and move to next step.</td></tr><tr><td rowspan=1 colspan=1>DFU_GETSTATE</td><td rowspan=1 colspan=1>0x05</td><td rowspan=1 colspan=1>Requests the device to send only the state it enters immediatelyafter this request.</td></tr><tr><td rowspan=1 colspan=1>DFU_ABORT</td><td rowspan=1 colspan=1>0x06</td><td rowspan=1 colspan=1>Requests device to exit the current state/operation and enter idlestate immediately.</td></tr></table>

Note:

The Detach request is not meaningful in the case of the bootloader. The bootloader starts with a system reset depending on the boot mode configuration settings, which means that no other application is running at that time.

Table 3. Summary of DFU class-specific requests   

<table><tr><td rowspan=1 colspan=1>bmRequest</td><td rowspan=1 colspan=1>bRequest</td><td rowspan=1 colspan=1>wValue</td><td rowspan=1 colspan=1>wIndex</td><td rowspan=1 colspan=1>wLength</td><td rowspan=1 colspan=1>Data</td></tr><tr><td rowspan=1 colspan=1>00100001b</td><td rowspan=1 colspan=1>DFU_DETACH</td><td rowspan=1 colspan=1>wTimeout</td><td rowspan=1 colspan=1>Interface</td><td rowspan=1 colspan=1>0</td><td rowspan=1 colspan=1>None</td></tr><tr><td rowspan=1 colspan=1>00100001b</td><td rowspan=1 colspan=1>DFU_DNLOAD</td><td rowspan=1 colspan=1>wBlockNum</td><td rowspan=1 colspan=1>Interface</td><td rowspan=1 colspan=1>Length</td><td rowspan=1 colspan=1>Firmware</td></tr><tr><td rowspan=1 colspan=1>10100001b</td><td rowspan=1 colspan=1>DFU_UPLOAD</td><td rowspan=1 colspan=1>wBlockNum</td><td rowspan=1 colspan=1>Interface</td><td rowspan=1 colspan=1>Length</td><td rowspan=1 colspan=1>Firmware</td></tr><tr><td rowspan=1 colspan=1>10100001b</td><td rowspan=1 colspan=1>DFU_GETSTATUS</td><td rowspan=1 colspan=1>0</td><td rowspan=1 colspan=1>Interface</td><td rowspan=1 colspan=1>6</td><td rowspan=1 colspan=1>Status</td></tr><tr><td rowspan=1 colspan=1>00100001b</td><td rowspan=1 colspan=1>DFU_CLRSTATUS</td><td rowspan=1 colspan=1>0</td><td rowspan=1 colspan=1>Interface</td><td rowspan=1 colspan=1>0</td><td rowspan=1 colspan=1>None</td></tr><tr><td rowspan=1 colspan=1>0010001b</td><td rowspan=1 colspan=1>DFU_GETSTATE</td><td rowspan=1 colspan=1>0</td><td rowspan=1 colspan=1>Interface</td><td rowspan=1 colspan=1>1</td><td rowspan=1 colspan=1>State</td></tr><tr><td rowspan=1 colspan=1>00100001b</td><td rowspan=1 colspan=1>DFU_ABORT</td><td rowspan=1 colspan=1>0</td><td rowspan=1 colspan=1>Interface</td><td rowspan=1 colspan=1>0</td><td rowspan=1 colspan=1>None</td></tr></table>

# Communication safety

The communication between host and device is secured by the embedded USB protection mechanisms (such as CRC checking, acknowledgments). No further protection is performed for transferred data or for bootloader specific commands/data.

# DFU bootloader commands

The DFU_DNLOAD and DFU_UPLOAD requests are mainly used to perform simple write and read memory operations. They are also used to initiate the integrated bootloader commands (such as Write, Read Unprotect, Erase, Set Address). The DFU_GETSTATUS command then triggers the command execution.

In the DFU download request, the command is selected through the wValue parameter in the USB request structure. If wValue = 0, the data sent by the host after the request is a bootloader command code. The first byte is the command code and the other bytes (if any) are the data related to the command.

In the DFU upload request, the command is selected through the wValue parameter in the USB request structure. If wValue = 0, the Get command is selected and performed.

Table 4. DFU bootloader commands   

<table><tr><td rowspan=2 colspan=1>DFU request</td><td rowspan=2 colspan=1>Bootloadercommand</td><td rowspan=1 colspan=1>Write protectiondisabled</td><td rowspan=1 colspan=1>Write protectionenabled</td><td rowspan=2 colspan=1>Protectionenabled</td></tr><tr><td rowspan=1 colspan=2>Protection disabled</td></tr><tr><td rowspan=2 colspan=1>DFU_UPLOAD</td><td rowspan=1 colspan=1>Read Memory</td><td rowspan=1 colspan=1>Allowed</td><td rowspan=1 colspan=1>Allowed</td><td rowspan=1 colspan=1>Not allowed</td></tr><tr><td rowspan=1 colspan=1>Get</td><td rowspan=1 colspan=1>Allowed</td><td rowspan=1 colspan=1>Allowed</td><td rowspan=1 colspan=1>Allowed</td></tr><tr><td rowspan=5 colspan=1>DFU_DNLOAD</td><td rowspan=1 colspan=1>Write Memory</td><td rowspan=1 colspan=1>Allowed</td><td rowspan=1 colspan=1>Allowed(1)</td><td rowspan=1 colspan=1>Not allowed</td></tr><tr><td rowspan=1 colspan=1>Erase</td><td rowspan=1 colspan=1>Allowed</td><td rowspan=1 colspan=1>Allowed(1)</td><td rowspan=1 colspan=1>Not allowed</td></tr><tr><td rowspan=1 colspan=1>Read Unprotect</td><td rowspan=1 colspan=1>N/A(2)</td><td rowspan=1 colspan=1>N/A(2)</td><td rowspan=1 colspan=1>Allowed(3)</td></tr><tr><td rowspan=1 colspan=1>Set Address Pointer</td><td rowspan=1 colspan=1>Allowed</td><td rowspan=1 colspan=1>Allowed</td><td rowspan=1 colspan=1>Allowed</td></tr><tr><td rowspan=1 colspan=1>Leave DFU mode</td><td rowspan=1 colspan=1>Allowed</td><td rowspan=1 colspan=1>Allowed</td><td rowspan=1 colspan=1>Allowed</td></tr></table>

tl uoiv o t  u rpl n o I the RAM or to the option byte area. 2Not applicable (this operation is allowed, but has no meaning as the memory is not protected). In this case, both the flash memory (from 0x0800 000) and the RAM are erased. The option byte area is reset to the default values.

If the user performs a Read Unprotect operation while the memory is not protected, the whole RAM is cleared by the bootloader firmware, while the flash memory is not erased (since it was not read-protected).

There are no commands for the Write Protect, Write Unprotect, and Read Protect operations. These operations can be performed through the Write Memory and Read Memory commands used for the option byte area.

# DFU_UPLOAD request commands

The upload request enables the execution of different commands. Their selection is done through the value of wValue in the USB request structure. The supported operations are described in sections 4.1 to 5.5.

# 4.1 Read memory

The Read memory operation is selected when wValue > 1.

The host requests the device to send a specified number of data bytes (wLength) from valid memory address (see Section 4) of the internal flash memory, embedded RAM, system memory, or from the option bytes.

The allowed number of bytes to read depends upon the memory target:

for the internal flash memory, the embedded RAM, and the system memory, read size can be from 2 to 2048 bytes   
for the option bytes read size must be equal to the option byte block size   
for other memory locations, refer to AN2606.

The address from which the host requests to read data is computed using the value of wBlockNumber (wValue) and the address pointer according to the following formula:

Address = (wBlockNum - 2) × wTransferSize) + Address_Pointer, where: wTransferSize is the length of the requested data buffer.

The address pointer must be previously specified through a Set Address Pointer command (using a DFU_DNLOAD request), otherwise (if no address was previously specified) the device assumes that it is the internal flash memory start address (0x08000000).

If the flash memory protection is enabled, the read operation is not performed, and the returned device status is (Status = dfuERROR, State = errVENDOR) whatever the target (internal flash memory, embedded RAM, system memory, or option bytes).

# 4.2 Get command

This command is selected when wValue = 0.

The host requests to read the commands supported by the bootloader. After receiving this command, the device returns N bytes representing the command codes.

The STM32 sends bytes as follows (N = 4):

Byte 1: 0x00 Get command Byte 2: 0x21 Set Address Pointer Byte 3: 0x41 Erase Byte 4: 0x92 Read Unprotect

Beginning from the USB BL version V3.0, the number of commands is no more fixed. Some commands depend upon the HW features, hence they can be omitted.

As an example, for the STM32H5 series there is no RDP HW feature. The Get command is:

Byte 1: 0x00 Get command   
Byte 2: 0x21 Set Address Pointer   
Byte 3: 0x41 Erase   
The processing of the DFU_UPLOAD command is shown in Figure 3 and Figure 4.

![](images/3914c399edcf468d0f53ce226c560c995daa870e753018ad45756e8815aa301e.jpg)  
Figure 3. DFU_UPLOAD request: device side

![](images/36283cefa91ca69c0769a66ef709dda0e39babb7f19566a2117792e097999867.jpg)  
Figure 4. DFU_UPLOAD request: host side

# Note:

Before issuing an Upload request, the host must check that the device is in a correct state (dfuIDLE or dfuUPLOAD-IDLE state) and that there is no error reported in the status. If the device is not in the required state, the host must clear any error (DFU_CLRSTATUS request) and get the new status until the device returns to dfulDLE state.

# DFU_DNLOAD request commands

The download request is used to perform different commands. The command selection is done through the value of parameter wValue in the USB request structure. The following operations are supported:

• Write Memory (wValue > 1) • Set Address Pointer (wValue = 0 and first byte = 0x21) • Erase (wValue = 0 and first byte = 0x41) • Read Unprotect (wValue = 0 and first byte = 0x92)(a) • Leave DFU (leave DFU mode and jump to application)

![](images/c1d4e9873400d0dc6afbfa141c0afba5a5150cc575b43ce849c32553c8a39cd2.jpg)  
Figure 5. Download request: device side

This routine can be used to reset the device or to jump to the application.

![](images/ee1120cf260597fa74ec0af1cdf1d7037a50fd8732d605e11ab4e0ff913147b8.jpg)  
Figure 6. Download request: host side

Read Unprotect command and Write operations to the option bytes need system reset.

After returning to the dfuDNBuY state, the device executes the requested operation and performs a system reset.The host can wait r the next enumeration or perform Get status agan, but he devic is unable to respond, unless it fails to execute the requested operation.

# Note:

Before issuing a Download request, the host must check that the device is in a correct state (dfuIDLE or dfuDNLOD-IDLE), and that no error is reported in the status. If the device is not in the required state, the host must clear any error (DFU_CLRSTATUS request) and get the status again until the device returns to the dfulDLE state.

# 5.1 Write memory

This operation is selected when wValue > 1.

The host requests the device to receive a specified number of data bytes (wLength) to load them into valid memory addresses (see Section 4) in the internal flash memory, RAM, or option bytes.

The allowed number of bytes to write depends upon the target memory:

for the internal flash memory and embedded RAM the write size ranges from 2 to 2048 bytes   
for the option bytes the write size must be equal to the option byte block size   
for other memory locations refer to AN2606.

Note:

A different write size is possible for the option bytes, but it is recommended to write the entire block with a single operation, to ensure data integrity. When the target is the option byte area, the address pointer must always be the start address of the option bytes, otherwise the request is not performed.

The Write memory operation is effectively executed only when a DFU_GETSTATUS request is issued by the host. If the status returned by the device is not dfuDNBUSY, an error occurred.

A second DFU_GETSTATUS request is needed to check if the command has been correctly executed, except when the destination is the option byte area (in this case the device is immediately reset after the write operation completion). If the received address is wrong or unsupported, the device status is (Status = dfuERROR, State = errTARGET).

The address where the host requests to write data is computed using the value of wBlockNumber (wValue) and the address pointer, according to the same formula as for an upload request:

Address = (wBlockNum - 2) × wTransferSize) + Addres_Pointer, where: wTransferSize: length of the data buffer sent by the host wBlockNumber: value of the wValue parameter

If the flash memory protection is enabled, the Write memory operation is not performed anc the returned device status is (Status = dfuERROR, State = errVENDOR), whatever the target (internal flash memory, embedded RAM, or option bytes).

If the Write memory command is issued to the option byte area, all options are erased before writing the new values, and, at the end of the command, the bootloader generates a system reset to take into account the new configuration of the option bytes.

Note: 1 When writing to the RAM, take care not to overlap the first RAM used by the bootloadr firmware.

2 No error is returned when performing write operations on write-protected sectors.

![](images/cda6cbfc81ad54b613a22c9f108d772894fdf81c24bc3d5fd5d996e05a9800b9.jpg)  
Figure 7. Write memory: device side   
1System reset is called only for some STM32 BL (STM32F0/F2/F4/F7) and some STM32L4 (STM32L412xx/422xx, STM32L43xxx/44xxx, STM32L45xxx/46xxx) products.

# 5.2 Set Address Pointer command

This command is selected when wValue = 0 and the first byte of the buffer sent by the host is 0x21. The buffer length is five bytes (the four remaining bytes are the address bytes, LSB first (32-bit address format)).

The host sends a DFU_DNLOAD request with the above-mentioned parameters to set the address pointer value used for computing the start address for Read and Write memory operations.

The STM32 receives bytes as follows:

Byte 1: 0x21 Set Address Pointer command Byte 2: A[7:0] LSB of the address pointer Byte 3: A[15:8] Second byte of the address pointer Byte 4: A[22:16] Third byte of the address pointer Byte 4: A[31:23] MSB of the address pointer

After sending the Set Address Pointer command, the host must send the DFU_GETSTATUS request.

The Set Address Pointer command is executed only when a DFU_GETSTATUS request is issued by the host. If the status returned by the device is not dfuDNBUsY, an error occurred.

A second DFU_GETSTATUS request is needed to check if the command has been correctly executed. If the received address is wrong or unsupported, the device status is (Status = dfuERROR, State = errTARGET).

The allowed locations for address pointer values are valid memory addresses in the internal flash memory, embedded RAM, system memory, and option bytes.

Jote: 1 Refer to Section 4 for more details about the valid memory addresses for the used device.

2 The Set Address Pointer command is allowed and executed when the flash memory read protection is enabled or disabled.

![](images/82f4da739bd9b02fa1bfbc17cf81ebb54467db662faa8f055dd6b26bf9a8cbd0.jpg)  
Figure 8. Set Address Pointer command: device side

# 5.3 Erase command

This command is selected when wValue = 0 and the first byte of the buffer sent by the host is Ox41. The buffer length can be five bytes (the four remaining bytes are the address bytes, LSB first) for the page erase operation, or only one byte (only the command byte) for the mass erase operation.

The host sends a DFU_DNLOAD request with the above parameters to erase one page of the internal flash memory, or to mass erase it.

The device receives the bytes as follows (page erase):

Byte 1: 0x41 Erase command Byte 2: A[7:0] LSB of the page address Byte 3: A[15:8] Second byte of the page address Byte 4: A[22:16] Third byte of the page address Byte 5: A[31:23] MSB of the page address

Or, if a 1-byte command is received:

The STM32 receives the bytes as follows (mass erase):

Byte 1: 0x41 Erase command

After sending an Erase command, the host must send a DFU_GETSTATUS request.

The Erase command is executed only when a DFU_GETSTATUS request is issued by the host. If the status returned by the device is not dfuDNBUSY, an error occurred.

A second DFU_GETSTATUS request is needed to check if the command has been correctly executed. If the received page address is wrong or unsupported, the device status is (Status = dfuERROR, State = errTARGET). If protection is active, the device returns the status (Status = dfuERROR, State = errVENDOR), and the erase operation is ignored.

The allowed Erase page addresses are internal flash memory addresses.

Note:

No error is returned when performing Erase operations on write-protected sectors.

![](images/e8cf04d3924611af2da252788957acdead24f794a1ce52c28670f1c323d688a9.jpg)  
Figure 9. Erase command: device side

# 5.4 Read Unprotect command

This command is selected when wValue = 0 and the first byte of the buffer sent by the host is Ox92. The buffer length is only one (the command) byte.

The host sends a DFU_DNLOAD request with the above parameters to remove the read protection of the internal flash memory.

The device receives the byte as follows:

Byte 1: 0x92 Read Unprotect command

After sending a Read Unprotect command, the host must send a DFU_GETSTATUS request.

The command is executed only when a DFU_GETSTATUS request is issued by the host. If the status returned by the device is not dfuDNBUSY, an error occurred. After this operation,

the device removes the read protection and, consequently, both the internal flash memory and the embedded RAM are fully erased.

Immediately after executing this command, the device disconnects itself and executes a system reset. In this case, the device is unable to respond to a second Get Status request, and the host must wait until the device is enumerated again.

A second DFU_GETSTATUS request may also be issued (if the device is still connected) to check if the command has been correctly executed. If the device fails to execute the command, it returns an error status (depending on the error type).

![](images/2e57835aaf6d16fded07a9421516343cb424281e80f9fb4f49e70b7838f93bcb.jpg)  
Figure 10. Read Unprotect command: device side

1System reset is called only in some STM32F0/F2/F4/F7, STM32L412xx/422xx, STM32L43xx/44xxx, and STM32L45xxx/46xxx products.

# 5.5 Leave DFU mode

It is possible to exit DFU mode (and bootloader) and jump to a loaded application (in the internal flash memory or in the embedded RAM) using the DFU download request.

The host sends a DFU_DNLOAD request with 0 data length (no data stage after the request) to inform the device that it must exit DFU mode. The device acknowledges this request if the current state is dfuDNLOAD-IDLE or dfulDLE.

The operation is effectively executed only when a DFU_GETSTATUS request is issued by the host. If the status returned by the device is not dfuMANIFEST, an error has occurred. After this operation, the device performs the following actions:

• Disconnects itself   
• Initializes the registers of the peripherals used by the bootloader to their default reset values   
• Initializes the user application main stack pointer   
o Jumps to the memory location programmed in the received address pointer + 4, which corresponds to the address of the application reset handler (as an example, if the

received address is Ox0800 0000, the bootloader jumps to the memory location programmed at address Ox0800 0004). In general, the host must send the base address where the application to jump to is programmed.

The address pointer must be set (using the Set Address Pointer command) before launching the Leave DFU routine, otherwise the bootloader jumps to the default address (internal flash memory start address: 0x08000000).

The address pointer can also be set through the last Write memory operation: if a download operation is performed, the address pointer used for this download is stored and used later for the jump.

# Note:

If the address pointer points to an address that does not contain executable code, the device is reset and, depending on the state of the boot pins, may re-enter the bootloader mode.

Since the bootloader DFU application is not manifestation-tolerant, the device is unable to respond to host requests after a manifestation phase is completed.

A second DFU_GETSTATUS request may also be issued (if the device is still connected) to check if the command has been correctly executed. If the device fails to execute the command, it returns an error status (depending on the error type).

No The Jup to appltin works ny  the us appltin st he vr tble cor point to the application address.

2 When performing a jump from the bootloader to a loaded application code using the USB IP, the application must disable all pending USB interrupts and reset the core before enabling interrupts. Otherwise, a pending interrupt (issued from the bootloader code) can interfere with the user code, and cause a functional failure. This procedure is not needed after exiting the system memory boot mode.

Figure 11. Leave DFU operation: device side

![](images/bbd54306d2e8f3f139b417ce4c7a5b31a6025e6b78784ae24cdc51dcde6c2741.jpg)

# Bootloader protocol version evolution

Table 5 lists the bootloader versions.

Table 5. Bootloader protocol versions   

<table><tr><td rowspan=1 colspan=1>Version</td><td rowspan=1 colspan=1>Description</td></tr><tr><td rowspan=1 colspan=1>V2.0</td><td rowspan=1 colspan=1>Initial bootloader version.</td></tr><tr><td rowspan=1 colspan=1>V2.1</td><td rowspan=1 colspan=1>DFU Bootloader version V2.1.Unlike version V2.0, this version features an extended interface descriptor includingOTP memory interface and device feature interface.V2.0 and V2.1 are implemented on different devices. Refer to AN2606 to know theversion implemented on the used device.Fixed bug found when writing in data memory timing by using an adequate timeout.</td></tr><tr><td rowspan=1 colspan=1>V2.2</td><td rowspan=1 colspan=1>Updated option bytes, OTP and device feature descriptors to support only Read/Writeoperation instead of Read/Write/Erase.</td></tr><tr><td rowspan=1 colspan=1>V3.0</td><td rowspan=1 colspan=1>The number of command can vary on devices with the same protocol version v3.0. Toknow supported commands, use Get command.</td></tr></table>

# 7 Revision history

Table 6. Document revision history   

<table><tr><td colspan="1" rowspan="1">Date</td><td colspan="1" rowspan="1">Revision</td><td colspan="1" rowspan="1">Changes</td></tr><tr><td colspan="1" rowspan="1">09-Mar-2010</td><td colspan="1" rowspan="1">1</td><td colspan="1" rowspan="1">Initial release.</td></tr><tr><td colspan="1" rowspan="1">15-Apr-2011</td><td colspan="1" rowspan="1">2</td><td colspan="1" rowspan="1">Introduced bootloader version V2.0 and V2.1 and update description ofbootloader sequence in Section 1. Added Figure 2: Bootloader for otherSTM32 devices.Updated allowed number of bytes when reading from option byte area,and added other memory locations in Section 4.1: Read memory.Updated allowed number of bytes when writing to option byte area, andadded other memory locations in Section 5.1: Write memory.Added bootloader V2.1 in Section 6.</td></tr><tr><td colspan="1" rowspan="1">12-Feb-2013</td><td colspan="1" rowspan="1">3</td><td colspan="1" rowspan="1">Changed title for Figure 1: Bootloader for STM32 connectivity linedevices.Updated Figure 2: Bootloader for other STM32 devices including title.Added Note: below Figure 2.Added Table 1: Applicable products.</td></tr><tr><td colspan="1" rowspan="1">30-Apr-2014</td><td colspan="1" rowspan="1">4</td><td colspan="1" rowspan="1">Updated Table 1: Applicable products and Table 5: Bootloader protocolversions.Updated Section 1: Bootloader code sequence.Removed section dedicated to Device-dependent bootloaderparameters.Updated Figure 2: Bootloader for other STM32 devices and addedfootnote 3.</td></tr><tr><td colspan="1" rowspan="1">21-Oct-2016</td><td colspan="1" rowspan="1">5</td><td colspan="1" rowspan="1">Updated Introduction and Table 1: Applicable products.</td></tr><tr><td colspan="1" rowspan="1">16-Mar-2017</td><td colspan="1" rowspan="1">6</td><td colspan="1" rowspan="1">Updated Table 1: Applicable products.</td></tr><tr><td colspan="1" rowspan="1">14-Feb-2019</td><td colspan="1" rowspan="1">7</td><td colspan="1" rowspan="1">Added STM32H7 series, hence updated Table 1: Applicable products.Updated Section 1: Bootloader code sequence.Minor text edits across the whole document.</td></tr><tr><td colspan="1" rowspan="1">21-Feb-2019</td><td colspan="1" rowspan="1">8</td><td colspan="1" rowspan="1">Added STM32WB series, hence updated Table 1: Applicable products.</td></tr><tr><td colspan="1" rowspan="1">09-Apr-2019</td><td colspan="1" rowspan="1">9</td><td colspan="1" rowspan="1">Added STM32G0 and STM32G4 series, hence updated Table 1:Applicable products.</td></tr><tr><td colspan="1" rowspan="1">23-Sep-2019</td><td colspan="1" rowspan="1">10</td><td colspan="1" rowspan="1">Added STM32L5 series, hence updated Table 1: Applicable products.Updated Introduction and Section 5.3: Erase command.</td></tr><tr><td colspan="1" rowspan="1">26-Nov-2019</td><td colspan="1" rowspan="1">11</td><td colspan="1" rowspan="1">Updated Table 1: Applicable products.Updated Figure 4: DFU_UPLOAD request: host side and Figure 5:Download request: device side.</td></tr><tr><td colspan="1" rowspan="1">02-Jun-2021</td><td colspan="1" rowspan="1">12</td><td colspan="1" rowspan="1">Updated Figure 7: Write memory: device side and Figure 10: ReadUnprotect command: device side and added footnotes to them.Minor text edits across the whole document.</td></tr><tr><td colspan="1" rowspan="1">08-Feb-2022</td><td colspan="1" rowspan="1">13</td><td colspan="1" rowspan="1">Added STM32U5 series, hence updated Table 1: Applicable products.</td></tr><tr><td colspan="1" rowspan="1">07-Feb-2023</td><td colspan="1" rowspan="1">14</td><td colspan="1" rowspan="1">Updated Introduction and Section 4.1: Read memory.Updated Table 1: Applicable products, Table 4: DFU bootloadercommands, and Table 5: Bootloader protocol versions.Added footnote in Section 5: DFU_DNLOAD request commands.Updated Figure 3: DFU_UPLOAD request: device side, Figure 4:DFU_UPLOAD request: host side, Figure 6: Download request: hostside, Figure 7: Write memory: device side, and Figure 9: Erasecommand: device side.Minor text edits across the whole document.</td></tr><tr><td colspan="1" rowspan="1">23-Feb-2024</td><td colspan="1" rowspan="1">15</td><td colspan="1" rowspan="1">Added STM32U0 series, hence updated Table 1: Applicable products.Updated Table 3: Summary of DFU class-specific requests.Minor text edits across the whole document.</td></tr><tr><td colspan="1" rowspan="1">18-Sep-2024</td><td colspan="1" rowspan="1">16</td><td colspan="1" rowspan="1">Added STM32C0 series, hence updated Table 1: Applicable products.</td></tr><tr><td colspan="1" rowspan="1">07-Feb-2025</td><td colspan="1" rowspan="1">17</td><td colspan="1" rowspan="1">Added STM32U3 and STM32WBA series, hence updated Table 1:Applicable products.</td></tr></table>

# IMPORTANT NOTICE  READ CAREFULLY

acknowledgment.

the design of purchasers' products.

No license, express or implied, to any intellectual property right is granted by ST herein.

or service names are the property of their respective owners.

I