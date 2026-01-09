# STM32 microcontroller GPIO hardware settings and low-power consumption

# Introduction

The STM32 microcontroller general-purpose input/output pin (GPIO) provides many ways to interface with external circuits within an application framework. This application note provides basic information about GPlO configurations as well as guidelines for hardware and software developers to optimize the power performance of their STM32 32-bit Arm® Cortex® MCUs using the GPIO pin.

This application note must be used in conjunction with the related STM32 reference manual and datasheet available at www.st.com.

# Contents

General information 6

# Documentation conventions .. .6

2.1 Glossary. 6   
2.2 Register abbreviations . . .

GPIO main features

# GPIO functional description . . 8

4.1 GPIO abbreviations 8   
4.2 GPIO equivalent schematics 9

4.3 GPIO modes description 10

4.3.1 Input mode configuration 10   
4.3.2 Output mode configuration 11   
4.3.3 Alternate functions 12   
4.3.4 Analog configuration 12

# GPIO electrical characteristics and definitions .. . 13

5.1 GPIO general information 13

5.1.1 Pad leakage current (Ilkg) 13   
5.1.2 Injected current (IINJ) 13   
5.1.3 GPIO current consumption 14   
5.1.4 Voltage output and current drive 14   
5.1.5 Pull-up calculation 16

# 5.2 Three-volt tolerant and five-volt tolerant . 17

5.2.1 Three-volt tolerant GPIO (TT) 17  
5.2.2 Five-volt tolerant GPIO (FT) 17

# 3 Five-volt tolerant application examples 18

5.3.1 White LED drive 18   
5.3.2 Triac drive 19   
5.3.3 |²C application .19   
5.3.4 UART application . 20   
5.3.5 USB VBUS example .21   
5.3.6 I/O usage for the five-volt ADC conversion 21

# GPIO hardware guideline .. 23

6.1 Avoid floating unused pin 23   
6.2 Cross-voltage domains leakage 23   
6.3 Voltage protection when no VDD is supplied 24   
6.4 Open-drain output with no load 25   
6.5 Using the MCO clock output . 25   
6.6 Debug pins have PU or PD by default 26   
6.7 NRST pin cannot be used as enable 26   
6.8 VBAT GPIO has limited current strength 26   
6.9 BOOTO pin 26

# GPIO software guidelines for power optimization . . . 27

7.1 Configure unused GPIO input as analog input . 27   
7.2 Adapt GPIO speed 27   
7.3 Disable GPIO register clock when not in use 27   
7.4 Configure GPIO when entering low-power modes 27   
7.5 Shutdown exit mode . . 27

# GPIO selection guide and configuration . . . 28

Revision history . 30

# List of tables

Table 1. List of GPIO structures 8   
Table 2. Document revision history 30

# List of figures

Figure 1. Three-volt compliant GPIO structure (TC) .9   
Figure 2. Three-volt or five-volt tolerant GPIO structure (TT or FT). 10   
Figure 3. Output buffer and current flow 15   
Figure 4. Logical level compatibility. 15   
Figure 5. STM32 current flow according to output voltage level 16   
Figure 6. Example of white LED drive connections 18   
Figure 7. Example of triac drive connections. 19   
Figure 8. Example of I2C connections 19   
Figure 9. Example of 5 V to 3.3 V power supply 20   
Figure 10. Example of UART connections. . 20   
Figure 11. Example of USB VBUS connections 21   
Figure 12. Example of VBUS to VDD power supply 21   
Figure 13. Example of five-volt ADC conversion 22   
Figure 14. Workaround example for five-volt ADC conversion 22   
Figure 15. Multi voltage leakage example 23   
Figure 16. Voltage protection when VDD is not supplied. 24   
Figure 17. Open-drain output with no load. 25   
Figure 18. GPIO configuration flowchart (1 of 2). 28   
Figure 19. GPIO configuration flowchart (2 of 2). 29

# 1 General information

m

# arm

# Documentation conventions

# 2.1 Glossary

This section defines the main acronyms and abbreviations used in this document.

AMR: absolute maximum rating   
GPIO: general-purpose input output   
GP: general-purpose   
PP: push-pull   
PU: pull-up   
PD: pull-down   
OD: open-drain   
AF: alternate function   
VIH: the minimum voltage level that is interpreted as a logical 1 by a digital input   
VIL: the maximum voltage level that is interpreted as a logical 0 by a digital input   
VoH: the guaranteed minimum voltage level that is provided by a digital output set to the logical 1 value   
VOL: the guaranteed maximum voltage level that is provided by a digital output set to the logical 0 value   
VDD: external power supply for the I/Os   
VDDIO2 external power supply for the l/Os, independent from the VDD voltage   
VDDA external power supply for analog   
Vss: ground   
IH: input current when input is 1   
IL: input current when input is 0   
loH: output current when output is 1   
IOL: output current when output is 0   
lkg: leakage current   
INJ injected current

# 2.2 Register abbreviations

The following abbreviations are used in register descriptions (x = A to H):

GPIOx_MODER: GPIOx_OTYPER: GPIOx_OSPEEDR: GPIOx_PUPDR: GPIOx_IDR: GPIOx_ODR: GPIOx_BSRR: GPIOx_LCKR: GPIOx_AFRL: GPIOx_AFRH: GPIOx_ASCR:

GPIO port mode register GPIO output type register GPIO output speed register GPIO port pull-up / pull-down register GPIO port input data register GPIO port output data register GPIO port bit set / reset register GPIO port configuration lock register GPIO alternate function low register GPIO alternate function high register GPIO port analog switch control register

# 3 GPIO main features

STM32 GPIO exhibits the following features:

Output states: push-pull, or open drain + pull-up / pull-down according to GPIOx_MODER, GPIOx_OTYPER, and GPIOx_PUPDR registers settings Output data from output data register GPIOx_ODR or peripheral (alternate function output)   
• Speed selection for each I/O (GPIOx_OSPEEDR) Input states: floating, pull-up / pull-down, analog according to GPIOx_MODER, GPIOx_PUPDR and GPIOx_ASCR registers settings   
• Input data to input data register (GPIOx_IDR) or peripheral (alternate function input)   
• Bit set and reset register (GPIOx_ BSRR) for bitwise write access to GPIOx_ODR   
• Locking mechanism (GPIOx_LCKR) provided to freeze the I/O port configurations   
• Analog function selection registers (GPIOx_MODER and GPIOx_ASCR)   
• Alternate function selection registers (GPIOx_MODER, GPIOx_AFRL, and GPIOx_AFRH)   
C Fast toggle capable of changing every two clock cycles Highly flexible pin multiplexing allowing the use of l/O pins as GPIO or as one of several peripheral functions

# 4 GPIO functional description

STM32 GPIO can be used in a variety of configurations. Each GPIO pin can be individually configured by software in any of the following modes:

• Input floating   
• Input pull-up   
• Input-pull-down   
• Analog   
• Output open-drain with pull-up or pull-down capability   
• Output push-pull with pull-up or pull-down capability   
• Alternate function push-pull with pull-up or pull-down capability Alternate function open-drain with pull-up or pull-down capability

# 4.1 GPIO abbreviations

Several GPIO structures are available across the range of STM32 devices. Each structure is associated with a list of options.

Table 1 summarizes the GPIO definitions and abbreviations applicable to STM32 products

Table 1. List of GPIO structures   

<table><tr><td rowspan=1 colspan=2>Name</td><td rowspan=1 colspan=1>Abbreviation</td><td rowspan=1 colspan=1>Definition</td></tr><tr><td rowspan=3 colspan=2>Pin Type</td><td rowspan=1 colspan=1>S</td><td rowspan=1 colspan=1>Supply pin</td></tr><tr><td rowspan=1 colspan=1>I</td><td rowspan=1 colspan=1>Input only pin</td></tr><tr><td rowspan=1 colspan=1>I/O</td><td rowspan=1 colspan=1>Input / output pin</td></tr><tr><td rowspan=5 colspan=2>I/O structure</td><td rowspan=1 colspan=1>FT(1)</td><td rowspan=1 colspan=1>Five-volt tolerant I/O pin</td></tr><tr><td rowspan=1 colspan=1>TT(1)</td><td rowspan=1 colspan=1>Three-volt tolerant I/O pin</td></tr><tr><td rowspan=1 colspan=1>TC</td><td rowspan=1 colspan=1>Three-volt capable I/O pin (Standard 3.3 V I/O)</td></tr><tr><td rowspan=1 colspan=1>B</td><td rowspan=1 colspan=1>Dedicated boot pin</td></tr><tr><td rowspan=1 colspan=1>RST</td><td rowspan=1 colspan=1>Bidirectional reset pin with embedded weak pull-up resistor</td></tr><tr><td rowspan=2 colspan=1>Pin functions</td><td rowspan=1 colspan=1>Alternate functions</td><td rowspan=1 colspan=2>Functions selected through GPIOx_AFR registers</td></tr><tr><td rowspan=1 colspan=1>Additional functions</td><td rowspan=1 colspan=2>Functions directly selected and enabled through peripheral registers</td></tr></table>

avt ep emus aa  .

As an example, the following description refers to a GPIO in a STM32 datasheet:

PB1 I/O FT means: pin PB1 I/O: port B bit 1 input / output FT: five-volt tolerant

Before starting a board design, it is important to refer to the datasheet of the STM32 product or to the STM32CubeMX tool to check for GPIO availability in coherence with the target application.

Refer to the section about software development tools at www.st.com/stm32.

# 4.2 GPIO equivalent schematics

STM32 products integrate three main GPIO basic structures:

Three-volt compliant (abbreviated as TC). The equivalent GPIO diagram structure is given in Figure 1. C Three-volt tolerant (abbreviated as TT). Five-volt tolerant (abbreviated as FT) The equivalent GPIO diagram structure for TT or FT is given in Figure 2.

# Note:

In Figure 1 and Figure 2, the analog switch in the dotted square is optional. Its presence depends on the STM32 product considered. The analog switch is controlled by enabling analog peripheral on the given pin (not by setting the GPlO in the analog mode). Refer to the product datasheet for details.

In Figure 1 and Figure 2, the VDD supply may refer to VDD or VDDIo2 according to the STM32 product considered. Refer to the product datasheet for details.

![](images/f68024383fdeb6443fe3fa191ff352057b32219986dcd7266b8bad6117e35a78.jpg)  
Figure 1. Three-volt compliant GPIO structure (TC)

MSv46872V1

Note:

The parasitic diode in the analog domain is connected to VDDA and cannot be used as a protection diode.

The voltage level called VDD_FT in some datasheets and reference manuals is inside the ESD protection block.

![](images/bc3a590e70c159123c57c99061dce3221144d6e6b297be0387d9466c3818d515.jpg)  
Figure 2. Three-volt or five-volt tolerant GPIO structure (TT or FT)

MSv46873V1

Note:

The parasitic diode in the analog domain is connected to VDDA and cannot be used as a protection diode.

The voltage level called VDD_FT in some datasheets and reference manuals is inside the ESD protection block.

When the analog option is selected (by enabling analog peripheral on the given pin), the

# Caution:

A TT or FT GPIO pin has no internal protection diode connected to supply (VDD). There is no physical limitation against over-voltage. Therefore, for applications requiring a limited voltage threshold, it is recommended to connect an external diode to VDD.

# 4.3

# GPIO modes description

This section describes the possible GPIO pin configurations available in STM32 devices.

# 4.3.1 Input mode configuration

When a STM32 device I/O pin is configured as input, one of three options must be selected:

Input with internal pull-up. Pull-up resistors are used in STM32 devices to ensure a well-defined logical level in case of floating input signal. Depending on application requirements, an external pull-up can be used instead.

Input with internal pull-down. Pull-down resistors are used in STM32 devices to ensure a well-defined logical level in case of floating input signal. Depending on application requirements, an external pull-down can be used instead.

Floating input. Signal level follows the external signal. When no external signal is present, the Schmitt trigger randomly toggles between the logical levels induced by the external noise. This increases the overall consumption.

Programmed as input, an l/O port exhibits the following characteristics:

• The output buffer is disabled   
• The Schmitt trigger input is activated The pull-up or pull-down resistors are activated depending on the value in the GPIOx_PUPDR register The data present on the l/O pin is sampled into the input data register at each AHB clock cycle The I/O state is obtained by reading the GPIOx_IDR input data register

# 4.3.2 Output mode configuration

When a STM32 device I/O pin is configured as output, one of two options must be selected:

Push-pull output mode:

The push-pull output actually uses two transistors: one PMOS and one NMOS. Each transistor is ON to drive the output to the appropriate level:

The top transistor (PMOS) is ON when the output has to drive HIGH state The bottom transistor (NMOS) is ON when the output has to drive a LOW state The control of the two transistors is done through the GPIO port output type register (GPIOx_OTYPER).   
Writing the related bit of the output register (GPIOx_ODR) to 0 activates the NMOS transistor to force the I/O pin to ground.   
Writing the related bit of the output register (GPIOx_ODR) to 1 activates the S nsistor  force he I/O pin VDD.

Open-drain output mode:

Open-drain output mode does not use the PMoS transistor and a pull-up resistor is required.

When the output has to go high, the NMOS transistor must be turned off, pulling the line high only by the pull-up resistor. This pull-up resistor could be internal with a typical value of 40 kOhm and activated through GPIO port pull-up / pull-down register (GPIOXx_PUPDR).

Note:

It is important to note that it is not possible to activate pull-up and pull-down at the same time on the same I/O pin.

It is also possible to use an external pull-up or pull-down resistor instead of the internal resistor. In this case, the value must be adapted to be compliant with the GPlO output voltage and current characteristics.

Programmed as output, an l/O port exhibits the following characteristics:

• The output buffer can be configured in open-drain or push-pull mode   
• The Schmitt trigger input is activated   
• Theinternalpull-upand pull-down resistors are activated dependingonthe valueinthe GPIOx_PUPDR register.   
• The written value into the output data register GPIOx_ODR sets the I/O pin state The written data on GPIOx_ODR can be read from GPIOx_IDR register that is updated every AHB clock cycle

Open-drain output is often used to control devices which operate at a different voltage supply than the STM32. Open-drain mode is also used to drive one or several I2C devices when specific pull-up resistors are required.

# 4.3.3 Alternate functions

On some STM32 GPIO pins, the user has the possibility to select alternate functions inputs / outputs. Each pin is multiplexed with up to sixteen peripheral functions such as communication interfaces (SPI, UART, I2C, USB, CAN, LCD and others), timers, debug interface, and others.

Thealternatefunction ofhe selected pin is configuredthrough two registers:

GPIOx_AFRL (for pin 0 to 7) GPIOx_AFRH (for pin 8 to 15)

To know which functions are multiplexed on each GPlO pin, refer to the device datasheet.

When the I/O port is programmed as alternate function mode:

• The output buffer can be configured in open-drain or push-pull mode The output buffer is driven by the signals coming from the peripheral (transmitter enable and data)   
• The Schmitt trigger input is activated The pull-up and pull-down resistors activations depend on the value in the registel GPIOx_PUPDR

The data present on the l/O pin are sampled into the input data register at each AHB clock cycle.

A read access to the input data register provides the l/O state.

Alternate functions details are provided in the datasheet and the reference manual of the product.

# 4.3.4 Analog configuration

Few STM32 GPIO pins can be configured in analog mode which allows the use of ADC, DAC, OPAMP, and COMP internal peripherals. To use a GPIO pin in analog mode, the following register are considered:

- GPIOx_MODER to select the mode (Input, Output, Alternate, Analog) - GPIOx_ASCR to select the required function ADC, DAC, OPAMP, or COMF

When the l/O port is programmed in an analog configuration:

The output buffer is disabled   
The Schmitt trigger input is deactivated, providing zero consumption for every analog value of the I/O pin.The output of the Schmitt trigger is forced to a constant value (0). The pull-up and pull-down resistors are disabled by hardware

Read access to the input data register gets the value 0.

For details concerning ADC, DAC, OPAMP and COMP function and programming, refer to the datasheet and reference manual of the product.

The analog switch itself is not closed. The analog switch is closed only when analog peripheral is selected (or enabled) on the given pin.

# GPIO electrical characteristics and definitions

This chapter defines and explains some of the electrical parameters in STM32 datasheets.

# 5.1 GPIO general information

The following sections detail some of the electrical parameters in the datasheets as a function of their use from an application point of view.

# AMR (absolute maximum ratings)

The absolute maximum ratings represent the values of voltages, current, temperatures, power dissipations, and others which must never be exceeded. Exceeding these values can lead to the deterioration or the destruction of the IC.

# Operating conditions

The operating conditions represent the range of guaranteed values within which the IC operates in proper conditions.

# 5.1.1 Pad leakage current (lkg)

The pad leakage current is the current which is sourced from the input signal by the l/O pin when it is configured in input mode. The value of the leakage current depends on the l/O structure and on the voltage range of the Vin signal applied to the I/O pin.

Leakage currents are product dependent. Refer to the datasheets for their values.

# 5.1.2 Injected current (INJ)

Injeincurrent is the urrent hat is beig fored into a pin by anput volage V)highrhan e positive supply (VDD + ΔV) or lower than ground (Vss).

Injection current above the given specifications causes a current flow inside the device and affects its reliability. Even a very small current exceeding the specified limit is not allowed.

STM32 datasheets specify injecte current and VIN

Negative-injection current is the current induced when Vin < Vss. The maximum negative injected current is -5 mA and the minimum Vin voltage level acceptable on the GPIO is -0.3 V for TT and FT GPIO.

Positive-injection current is the current induced when VIN > VDD. For STM32 devices, the maximum positive-injection current on TT and FT GPIO is defined as N/A or 0 mA.

N/A means that, as long as the input voltage is within the AMR range, and due to the internal design of the GPlO, no current injection occurs. As a result, no corruption of the GPIO and STM32 device operation is observed in such a case. 0 mA means that current injection can damage the GPIO and induce STM32 malfunction.

Warning: positive current injection is prohibited for a TT or FT GPIO defined as 0 mA

The maximum VIN voltage is equal to VDD + 0.3 V for TT GPIO. For FT GPIO, the VIN maximum voltage is the minimum value among VDD, VDDA, VDDIO2, VDDUSB, and VLCD) augmented of 3.6 V with a maximum Vin value limited to 5.5 V.

Note:

s   
The total injected current is limited, typically to 25 mA per device. Refer to the device datasheet for the value of the exact limitation. This restricts the number of pins on which current can be injected.

# 5.1.3 GPIO current consumption

There are two types of l/O pin current consumption in STM32 devices:

1The static current consumption which is mainly due to pull-up resistors when l/O pin is used as input and held low or when l/O pin is used as output with external pull-down or external load.   
2. The dynamic current consumption which is the current from the l/O supply voltage used by the l/O pin circuitry and capacitive load when the l/O pin switches.

The dynamic current consumption is given by Equation 1

# Equation 1 Isw = C x VDD X Fsw

Isw is the current sunk by a switching l/O to charge / discharge the capacitive load   
CL is the total load capacitance seen by the l/O pin   
C is the sum of internal, external, PCB, and package capacitances   
VDD is the I/O supply voltage   
Fsw is the I/O switching frequency

Note:

The GPIO speed has no impact on the dynamic current consumption.

# 5.1.4 Voltage output and current drive

All STM32 GPIOs are CMOS and TTL compliant and are able to source or sink current from external pin. Figure 3 shows the current flow according to the output level selected. IoH is sourced current when GPIO output is in High state. IoL is sunk current when GPIO output is in Low state. The maximum output current which can be sunk or sourced by one GPlO or from the power supplies is limited to preserve the GPlO from as well as that the sum of the current sourced or sunk by all GPIO and cannot exceed the AMR values fixed inside the product datasheet. Following the current drive limitations, the number of GPlO which can drive current has to be limited consequently.

For more details, see the values of lvDD, IvSs, Io and ∑ IvDD, ∑ Ivss, and ∑ Iio parameters allowed into the AMR current characteristics table available in the datasheet.

![](images/bcb9b1048838fc976bae9ecd1256d122112df3b15164cd83a360fc3365e0257b.jpg)  
Figure 3. Output buffer and current flow

In case of communication exchange, STM32 output signals must be compatible with the VIL / VIH of the receptor device and STM32 inputs must be compliant with the VoL / VoH of the transmitter device as shown in Figure 4.

![](images/3bb05ef3793b2e6de5cddcf9bf7a7207fc9c0763b0d064e26c04e12669057495.jpg)  
Figure 4. Logical level compatibility

For the CMOS technology, the input threshold voltages are relative to VDD as follows:

VIHmin \~ 2 / 3 VDD and VILmax \~ 1 / 3 VDD.

For the TTL technology, the levels are fixed and equal to VIHmin = 2V and VILmax = 0.8 V.

The VoH , VoL, VIH, VIL levels and the values of output-driving currents are part of the general input/output characteristics given in the STM32 datasheet.

# 5.1.5 Pull-up calculation

Each STM32 GPIO offers the possibility to select internal pull-up and pull-down (typical value = 40 kOhm). Some STM32 applications may require to use an external pull-up resistor. This section presents output and input levels compatibility and the way to calculate the appropriate pull-up resistor when the STM32 GPIO open-drain output is connected to an external device.

![](images/57228e8745afe6191dc80b54a9c066f8938ee49435e868b09219bb602f49e20a.jpg)  
Figure 5. STM32 current flow according to output voltage level

The schematics in Figure 5 shows the current flows (gray arrows) and the associated voltages needed to calculate the Rpu pull-up resistor.

The value of Rpu is maximum when GPIO output equals 1. This means that the NMOS transistor is OFF; the VoHmin voltage is used for the calculation.

The value of Rpu is minimum when GPIO output equals 0. This means that the NMOS transistor is ON; the VoLmax voltage is used or the calculation.

# Pull-up calculation for the 12C bus:

Pull-up calculation in case of I2C bus is different because the I2C mode must be taken into account. This calculation depends on the I2C mode (Standard Mode, Fast Mode, Fast mode Plus), on the VDD of the device, and on the bus capacitance.

A low pull-up resistor value prevents the dedicated STM32 GPIO 12C pins to generate a low al according to Equation 2.

# Equation 2 RpUmin = (VDD -VOLmax) / IOL

The maximum pull-up resistance RpUmax is limited by the total capacitance of the bus including the capacitance of the wire, connections and pins (Cb), and the maximum rise time (trmax) of the SDA and SCL signals. Refer to the datasheet and to the I2C bus specification for more details.

pul ot al  e pulled low. The maximum value RpUmax is calculated according to Equation 3.

Equation 3 RpUmax = trmax / (0.8473 x Cb)

The rationale for Equation 3 is described in the following steps:

1. Voltage amplitude over time is RC time-constant dependent according to V(t) = VDD X (1 - e(-t / RC))   
2. With VIH = 0.3 x VDD, the time  at which ViH is reached satisfies to V(t) = 0.3 x VDD = VDD X (1 − e(-t1 / RpUCb)) leading to t1 = 0.3566749 x Rpu x Cb   
3. With VoH = 0.7 x VDD, the time t at which VoH is reached satisfies to V(t2) = 0.7 x VDD= VDD X (1 − e(-t2 / RpUCb)) leading to t = 1.2039729 x Rpu  C   
4. With t, = t2 - t1, it comes t, = 0.8473 x Rpu x Cb

# 5.2 Three-volt tolerant and five-volt tolerant

Electrical characteristics defines GPlO as three-volt tolerant, five-volt tolerant, and also three-volt capable. Tolerance represents the voltage value which can be accepted by the GPIO. Capability represents the voltage value which can be output by the GPIO.

# 5.2.1 Three-volt tolerant GPIO (TT)

For some STM32, electrical specifications define GPIO as three-volt tolerant or three-volt compliant. From the user point of view, there is no difference between these two kinds of GPIO.

Input voltage on three-volt tolerant cannot exceed VDD + 0.3 V.

If some analog input function is enabled on the GPIO (I/O structure TT_a with ADC input active, COMP input, OPAMP input), then the maximum operating voltage on pin cannot exceed min(VDDA, VREF+) + 0.3 V.

# 5.2.2 Five-volt tolerant GPIO (FT)

STM32 devices embed five-volt tolerant GPIOs. These GPIOs are actually tolerant to VDD + 3.6 V. It means that the l/O pins can accept such voltages without causing leakage current and damages on the GPIOs.

Regardless of the supply voltage, Vin cannot exceed 5.5 V.

When VDD = 0 V, the input voltage on the GPIO cannot exceed 3.6 V.

In ce f a multi-supplied and multiplexed GPIO (VDD VDDSB, VLCD VDDA), the GPIO is tolerant to 3.6 V augmented of the minimum supply voltage among VDD. VDDUB VLCD, and VDDA.

However, a GPlO is five-volt tolerant only in input mode. When the output mode is enabled, the I is more ie-volt tolerant.For moe details about I/O ipu voltage, er Vi parameters in the general operating conditions table of the datasheet.

A GPlO is five-volt tolerant only if there is no analog function enabled on pin (for I/O structure FT_a, FT_fa, TT_a). If some analog input function is enabled on the GPIO (ADC input active, COMP input, OPAMP input), then the maximum operating voltage on pin cannot exceed min(VDDA, VREF+) + 0.3 V.

# 5.3 Five-volt tolerant application examples

The following figures give examples of applications only using five-volt tolerant GPIO.

# 5.3.1 White LED drive

A white LED needs a typical \~20 mA current under typical 3.5 V supply (4 V max.).

As STM32 devices maximum sink current is 25 mA, there is not enough margin to directly drive a LED. Two options, using an external MOSFET (or BJT) or driving by means of two GPIOs, are presented in Figure 6.

![](images/4ec47a51ce17d64f5d203970ecf549fa80b1fea0d686c64437e413695e3896e3.jpg)  
Figure 6. Example of white LED drive connections

MSv46877V1

For the GPlO parallel drive option, open-drain mode must be used and internal pull-up must be disabled. Since the ground current is huge compared to the MCU consumption, the ground layout needs to be designed with care.

# 5.3.2 Triac drive

A triac drive example is shown in Figure 7 for the -5 V supply system.

![](images/178e618a2681253f940a01be42918c2fe6400bcc422a0df36c0c8296643bf268.jpg)  
Figure 7. Example of triac drive connections

In this set up, the STM32 current flow depends on the output voltage level. The STM32 GPIO must be set up in open-drain mode. If the I/O drive current is not sufficient, coupled GPIOs can be used in parallel.

# 5.3.3 2C application

The STM32 device supplied by 1.8 V or 3.3 V can directly communicate with a 5 V I2C bus as illustrated in Figure 8.

![](images/5bb223296a9b83035199daae5c98858191f54c312b7f767bfdedd342dc73e190.jpg)  
Figure 8. Example of I²C connections

MSv46879V1

If it occurs that VDD = 0 V while VDDX = 5 V (even transient), it is recommended to place a Zenner diode (for instance 3.3 V) between VDD and VDDX.

![](images/ddccd1c545d4f6db4d667ab597f8c47705f92a5f00ad7a06bec1750d28b7490c.jpg)  
Fgur .  y

# 5.3.4 UART application

If the UART transceiver to communicate with is supplied with TTL-compatible 5 V, the STM32 device can directly communicate as shown in Figure 10.

![](images/b7a2a162499d50a253a9852ba2e5533780d63c329e77f7b2323c6d588956c772.jpg)  
Figure 10. Example of UART connections

If the 5 V UART interface input is TTL compatible, VoL < 0.8 V and VoH > 2.0 V. This implies that a 3.3 V CMOS output can drive without any problem. An STM32 FT pad can accept 0 V to 5 V CMOS level input when VDD = 3.3 V.

# 5.3.5 USB VBUS example

The VBUS pad of STM32 devices is five-volt tolerant, However, it needs to comply with the VDD maximum rating. If STM32 is supplied from an independent supply, it is not allowed to connect VBUS as long as STM32 is not supplied. Another solution is to place a Zenner diode (ex. 3.3 V) between VBUS and VDD as illustrated in Figure 11.

![](images/08939bef1850200c915048b7dcebf192b1b0c0561f5aa491a434fed1c9d60b73.jpg)  
Figure 11. Example of USB VBUS connections

If the STM32 supply is provided by an LDO supplied by VBUS, it is recommended to use a Zenner diode (ex. 3.3 V) as illustrated in Figure 12.

![](images/a7a5d6aa5b4d8867efd71adce6f662dfac222198d83ce389ea35fbfd5556592f.jpg)  
Figure 12. Example of VBus to VDD power supply

# 5.3.6 I/O usage for the five-volt ADC conversion

STM32 devices have FT pads which are connected to ADC input. When ADC is not connected (analog switch in l/O is not closed), the I/O can accept VDD + 3.6 V. In this situation, 5 V applied to FT pad can be granted.

However, once the l/O input is connected to the ADC, and during the sampling phase, the parasitic diode to VDDA and/or VREF+ is forward biased as shown in Figure 13.

![](images/9499f64ac5f4041f5a2a2d9ae226f7ebf0a70c25a0d3187d431f52250d73ad3b.jpg)  
Figure 13. Example of five-volt ADC conversion

MSv46884V1

It is recommended to clamp the input voltage with an external clamp (for instance a series of resistors and the Schottky diode to VREF+).

The parasitic diodes are not characterized for reliability. STMicroelectronics does not guarantee the level of current which those diodes can accept.

# Work around proposal

If there is an unused FT pad available on the STM32 device, connect it to the ADC input pad with parallel configuration as illustrated in Figure 14.

![](images/3b47293bf97f301db01edb970b6873684c75950919806b79a1154140f7902eef.jpg)  
Figure 14. Workaround example for five-volt ADC conversion

1. The ADC makes the conversion with the other FT_PAD pull-down enabled. 2. If first ADC conversion result is less than 2 V (which indicates that the DC source is inside the ADC input range), the ADC re-does the conversion with pull-down disabled.

The above method avoids the parasitic diode forward bias.

# 6 GPIO hardware guideline

This chapter sums up some of the most important rules to check when developing applications with STM32 GPIO.

# 6.1 Avoid floating unused pin

Do not leave unused pin floating. Connect it either to ground or to supply on the PCB, or use PU / PD. Noise on non-connected input pin is a source of extra consumption by making the input buffer switch randomly.

If the application is sensitive to ESD, prefer a connection to ground or define the pin as PP output and drive it to low.

# 6.2 Cross-voltage domains leakage

In applications with multiple different voltages (for instance 3.3 V and 1.8 V, or 5 V and 3.3 V), check that all the GPIOs with PU are not exposed to an input voltage that exceeds VDD. This is particularly valid when optional external circuitry is connected (debugger probe and systems or others).

![](images/75c4318d0711273e3c62f75711a652beab95d887913dee381ae13a56a4b3e025.jpg)  
Figure 15. Multi voltage leakage example

The example provided in Figure 15 shows the leakage current induced by the internal pullup resistor when the STM32 and the driving buffer are not supplied with the same VDD source. The pink arrow marks the leakage current path.

# 6.3 Voltage protection when no VDD is supplied

Voltage protection (for example five-volt tolerance for inputs) is guaranteed only if the STM32 is supplied.

o

If VDD is not present, for example grounded, the maximum voltage must not exceed 3.6 V (the exact limit value is provided in the STM32 datasheet).

# Warning: If the external voltage exceeds the maximum voltage value, the STM32 device can be damaged.

![](images/c461c7b69da10f410c4be30c1cc9fcc463866f02d24ce8a6ae76e8b2a7a6bc02.jpg)  
Figure 16. Voltage protection when VDD is not supplied

The example provided in Figure 16 shows the leakage current induced when no VDD is supplied. The pink arrow marks the leakage current path.

# 6.4 Open-drain output with no load

When the GPlO is configured as an open drain output with no external pull-up load or internal pull-up, it must be forced to low drive so that the input signal on the pin is defined. This avoids a floating input. This configuration is shown in Figure 17.

![](images/f6dab6754c351ff671f1fa343bf1a36b5195093203aa318ccc48ff336acd29e6.jpg)  
Figure 17. Open-drain output with no load

# 6.5 Using the MCO clock output

Clock signals can be a major factor of high current consumption. Specific attention must be paid to all input and output clocks related to the MCU or to other components on the board. Designers must consider that clocking other components on the board with the MCU clock through an output pin (such as the MCO(a) increases the current consumption due to the I/O switching frequency.

For this reason, it is up to the hardware designer to choose either routing a PCB wire from the MCO(a) pin to other clock input components or to use an external oscillator depending on the full set of clock requirements on the board (number of clock inputs and clock frequencies).

# 6.6 Debug pins have PU or PD by default

Some pins are by default programmed as inputs with PU or PD (see STM32 datasheet for the related GPlO). If these pins are used for other purposes, it must be avoided to force a 0 while PU or a 1 while PD, as this causes extra consumption.

# 6.7 NRST pin cannot be used as enable

The NRST pin cannot be used as an enable pin in order to achieve the lowest power consumption. Permanently grounding it maintains the device in the startup phase. It is preferred to release the NRST pin and enter one of the low-power mode (either Standby or Shutdown) if possible.

Note:

The NRST pin already integrates a weak PU (about 40 kOhm).

# 6.8 VBAT GPIO has limited current strength

The VBAT GPIO pin allows to supply the STM32 backup domain from an external voltage source (battery or capacitor). When an STM32 microcontroller is in VBAT mode, most of the GPIOs are shut down. Only the GPlOs which are part of the backup domain are powered through the VBAT voltage when VDD is not present. Backup GPIOs are supplied through an integrated switch that has limited drive strength (it cannot exceed 3 mA). These l/Os must not be used to drive high current and their speed is limited, even when VDD is valid.

Overdriving this capability could lead to unspecified level that could create extra power consumption in the system.

# 6.9 BOOTO pin

Applying VDD voltage permanently to BOOTO generates extra consumption.

# GPIO software guidelines for power optimization

# 7.1

# Configure unused GPIO input as analog input

GPIO always have aninput channel, which can be either digital oranalog.

If it is not necessary to read the GPlO data, prefer the configuration as analog input. This saves the consumption of the input Schmitt trigger.

# 7.2 Adapt GPIO speed

The rise time, fall time and maximum frequency are configurable using the GPIOx_OSPEEDR configuration register. Such adjustment has an impact on the EMI (electromagnetic interferences) and SsO ( simultaneous switching output) due to higher switching current peak. A compromise has to be done between GPlO performance versus noise. The rise time and fall time of each GPlO signal must be adapted to the minimal value compatible with the associated signal frequency and board capacitive load.

In order to help users to control the signal integrity in their applications, the IBIS model of the selected STM32 GPIO pin is available and can be downloaded from STMicroelectronics web site at www.st.com.

# 7.3 Disable GPIO register clock when not in use

If a GPlO bank does not need to be used for a long period, disable its clock by using the HAL_RCC_GPIOx_CLK_DISABLE() function.

# Configure GPlO when entering low-power modes

When enterig lo-power mode, all pin signals must be td either  VDD or toground.

If the GPIO is connected to an external receiver (external component input), the GPIO signal value must be forced using either a PP or a PU/PD.

When the GPlO is connected to a driver (external component output or bus), the driver must provide a valid level (either VDD or ground). If the driver level is undefined, the signal on the GPIO must be forced by using PU/PD.

For practical reasons, it may be easier to use input PU/PD in low-power mode when the GPIO is an input (analog or digital) in Run mode; and output PP when the GPIO is an output in Run mode. This avoids to manage the changes when entering or exiting Stop modes.

# 7.5 Shutdown exit mode

Note:

This section applies only to the microcontrollers in the STM32L4 Series, STM32L4+ Series, STM32L5 Series, and STM32U5 Series.

When exiting from Shutdown mode, the GPlOs are reconfigured to their default values at Power On Reset. This can create extra system consumption before they can be reprogrammed to their correct value. If this is an issue for the application, the Standby mode must be used instead of the Shutdown mode.

# GPIO selection guide and configuration

The flowchart presented in Figure 18 and Figure 19 provides users with a quick help to select the GPlO mode and configuration adapted to their application.

![](images/3452ad6606ee1329c3f6a76aa429a342f26510cf3d59c0f8ae33bb8f32238931.jpg)  
Figure 18. GPIO configuration flowchart (1 of 2)

![](images/63a2c5f043a0ff377b7c9d482431e9cc8f60ece114a1c0231e197696990b41da.jpg)  
Figure 1. GPIO configuration flowchart (2 f 2)

# 9 Revision history

Table 2. Document revision history   

<table><tr><td rowspan=1 colspan=1>Date</td><td rowspan=1 colspan=1>Revision</td><td rowspan=1 colspan=1>Changes</td></tr><tr><td rowspan=1 colspan=1>21-Sep-2017</td><td rowspan=1 colspan=1>1</td><td rowspan=1 colspan=1>Initial release.</td></tr><tr><td rowspan=1 colspan=1>12-Aug-2021</td><td rowspan=1 colspan=1>2</td><td rowspan=1 colspan=1>Updated the document title.Added a note to Section 5.2.1: Three-volt tolerant GPIO(TT) and Section 5.2.2: Five-volt tolerant GPIO (FT)about the maximum operating voltage when an analoginput function is enabled.Added remarks about the analog switch in Section 4.2:GPIO equivalent schematics and Section 4.3.4: Analogconfiguration.</td></tr><tr><td rowspan=1 colspan=1>29-Mar-2022</td><td rowspan=1 colspan=1>3</td><td rowspan=1 colspan=1>Updated the document title.Updated the applicability of Section 7.5: Shutdown exitmode.</td></tr></table>

# IMPORTANT NOTICE  READ CAREFULLY

acknowledgment.

the design of purchasers' products.

No license, express or implied, to any intellectual property right is granted by ST herein.

product or service names are the property of their respective owners.

I