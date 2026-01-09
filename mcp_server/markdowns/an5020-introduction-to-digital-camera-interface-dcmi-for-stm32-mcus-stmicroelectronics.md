# Introduction to digital camera interface (DCMI) for STM32 MCUs

# Introduction

technologies (such as 3D, computational, motion, and infrared).

eiveneseet hee emets,he32 CUbe  gil ame interfaCM, whicalo connection to efficient parallel camera modules.

C   P Asophisticated applications and connectivity solutions (loT).

architecture, and configuration of the DCMl. It is supported by an extensive set of detailed examples.

Refer to the device reference manual and datasheet for more details.

Table 1. Applicable products   

<table><tr><td rowspan=1 colspan=1>Type</td><td rowspan=1 colspan=1>STM32 lines and series</td></tr><tr><td rowspan=9 colspan=1>Microcontrollers</td><td rowspan=1 colspan=1>STM32F2x7</td></tr><tr><td rowspan=1 colspan=1>STM32F407/417, STM32F427/437, STM32F429/439, STM32F446, STM32F469/479</td></tr><tr><td rowspan=1 colspan=1>STM32F7x0 value line(1), STM32F7x5, STM32F7x6, STM32F7x7, STM32F7x8, STM32F7x9</td></tr><tr><td rowspan=1 colspan=1>STM32H723/733, STM32H725/735, STM32H730 value line, STM32H742, STM32H743/753, STM32H745/755,STM32H747/757, STM32H750 value line, STM32H7A3/B3</td></tr><tr><td rowspan=1 colspan=1>STM32L4x6</td></tr><tr><td rowspan=1 colspan=1>STM32L4P5/Q5, STM32L4R5/S5, STM32L4R7/S7, STM32L4R9/S9</td></tr><tr><td rowspan=1 colspan=1>STM32U5 series</td></tr><tr><td rowspan=1 colspan=1>STM32H563/573, STM32H562, STM32H523/533</td></tr><tr><td rowspan=1 colspan=1>STM32N6 series</td></tr></table>

# 1 General information

# Note:

This application note applies to the ST32 Series microcontrollers that are Arm® Cortex® core-based devics.   
Arm is a registered trademark of Arm Limited (or its subsidiaries) in the US and/or elsewhere.

# 2 Camera modules and basic concepts

Thi section provides a summarize description camera modules and thermain components. It also highlights the external interface focusing on parallel camera modules.

# 2.1 Basic imaging concepts

This section introduces the imaging field, and gives an overview of the basic concepts and fundamentals, such as pixel, resolution, color depth, and blanking.

Pixel: each point of an image represents a color for color images, or a gray scale for black-and-white photos

Adigitalapproximation sreconstructed tobe the fial imageThis digital mage satwo-imensionaly comose of physical points. Each point is called a pixel (invented from picture elements). In other words, a pil is the allest conrollable eement  a pictu.Eac pixel is essable.Figurilues the difference between the original image and the digital approximation.

![](images/5540434494e65e9cc173f93fb7ac36a55263af0867acc6c58cb3d9100166ec3c.jpg)  
Figure 1. Original versus digital image

Resolution: number of pixels in the image.

The more the pixe size increass, the more the mage ize increaes. For the same mage e theihr the number of pixels is, the more details the image contains.

Coldepth bt depth): henumbe  btused  indicate the color a pixel salso given i bt pe pixel, bpp)

For a bitonal image, each pixel comprises one bit. Each pixel is either black or white (0 or 1). For a gray scale, the image is most of the time composed of 2 bpp (each pixel can have one of four gray levels) to 8 bpp (each pixel can have one of 256 gray levels).   
For color images, the number of bits per pixel varies from 8 to 24 (each pixel can   
have up to 16777216 possible colors).

Frame rate (for video): number of frames (or images) transferred each second, expressed in frame per second (FPS).

Horizontal blanking: ignored rows between the end of one line and the beginning of the next one.

Figure 2. Horizontal blanking illustration   

<table><tr><td rowspan="2">Horizontal blanking</td><td>Line n (valid data)</td><td rowspan="2">Horizontal blanking</td></tr><tr><td>Line n + 1 (valid data)</td></tr></table>

Vl esn in the next frame.

Figure 3. Vertical blanking illustration   

<table><tr><td>Frame 1</td></tr><tr><td>Line n</td></tr><tr><td>Vertical blanking</td></tr><tr><td>Line 1 Frame2</td></tr></table>

The lines can be drawn one after the other in a sequence without separating the odd lines from the even ones, as for interlaced scan. To construct the image:

In progressive scan, the first line is drawn, then the second, and, finally, the third In interlaced scan, each frame is divided into two fields (odd and even lines), which are displayed alternately

# 2.2

# Camera module

Acera module consists of four parts: image sensor, lens, printed circuit board (PCB), and interace.   
Figure 4 shows some common camera modules examples.

![](images/5d2bece4b09398b741cd2cfeaa47b7deac141b0b192d3ccc38e990e6e7740458.jpg)  
Figure 4. Camera module examples

# 2.2.1

# Camera module components

The four components of a camera module are described below.

# Image sensor

It is an analog deviceused to convert the received light into electronic signals. These signals convy the information that constitutes the digital image.

There are two types of sensors that can be used in digital cameras:

CCD (charge-coupled device) sensors CMOS (complementary metal-oxide semiconductor) sensors

continually evolves and ther cost decreases,  imagers now dominate the digital photography landscape.

# Lens

I the proper lens is part of the user creativity, and affects considerably the image quality.

# Printed circuit board (PCB)

It  at sensor. The PCB also supports all the other parts of the camera module.

# Camera module interconnect

Thecameiteackiriehataowsheageensorect be ysta to send/receive signals. The following signals are transferred between a camera and an embedded system:

Control signals Image data signals Power supply signals Camera configuration signals

Tmenteaces edivieintotwotyeparallean serl inteacesependign hemetho t transfer data signals.

# 2.2.2

# Camera module interconnect (parallel interface)

As mentioned above, a cameramodule requires four main types f signals to transmit image data properly: l typical block diagram of a CMOS sensor, and the interconnection with an MCU.

![](images/b091e5d814bb7bd03683258293a241cb4da1c348afe2a5b47075909813fac53a.jpg)  
Figure 5. Interfacing a camera module with an STM32 MCU

;ontrol signals: used for clock generation and data transfer synchronizatiol

The camera clock must be provided according to the camera specification. The camera also provides two data synchronization signals: HSYNC (for horizontal/line synchronization) and VSYNC (for verticalframe synchronization).

Image data signals: each of them transmits a bit of the image data. Their width represents the number of bits to be transferred at each pixel clock. This number depends on the parallel interface of the camera module, and on the embedded system interface.

Power supply signals:

As any embedded electronic system, the camera module needs to have a power supply. The operating voltage of the camera module is specified in its datasheet.

Configuration signals: used for the following:

To configure the appropriate image features such as resolution, format, and frame rate To configure the contrast and the brightness To select the type of interface. (A camera module can support more than one interface: a parallel and a serial interface. The user must then choose the most convenient one for the application.)

Most camera modules are parametrized through an I2C communication bus.

# 3 STM32 DCMI overview

This section gives a general preview of the DCMI availability across the various STM32 devices, and gives an easy-to-understand explanation on the DCMI integration in the STM32 MCUs architecture.

The DCMl is a synchronous parallel data bus, which is used for an easy integration and easy adaptation to sic application requirements. The DCMI connects with 8,1  anbit CMOS camera modules, an supports a multitude of data formats.

# DCMI availability and features across STM32 MCUs

Table . Availability of DCMI and related resources summarizes the STM32 devices embedding the DCMI, and the DCMI in the same application.

ThM plitis ee  mebu sore he aptu mage. Isheary y destination that varies depending on the image size and the transfer speed.

I S a usn h asFotai heplto QuntcSTM: microcontrollers and microprocessors (AN4760).

The DMA2D (Chrom-ART Accelerator controller) is useful for color space transformation (such as RGB565 to ARGB8888), or for data transfer from one memory to another.

The JPEG codec allows data compression (JPEG encoding) or decompression (JPEG decoding).

Table 2. Availability of DCMI and related resources   

<table><tr><td rowspan=1 colspan=1>STM32 line</td><td rowspan=1 colspan=1>Max flashmemory size</td><td rowspan=1 colspan=1>On-chipSRAM(Kbytes)</td><td rowspan=1 colspan=1>QUADSPI</td><td rowspan=1 colspan=1>OCTOSPI</td><td rowspan=1 colspan=1>HSPI</td><td rowspan=1 colspan=1>XSPI</td><td rowspan=1 colspan=1>Max FMC(1)SRAM andSDRAMfrequencyMHz)</td><td rowspan=1 colspan=1>MaxDCMIpixelclockinput(MH)2</td><td rowspan=1 colspan=1>JPEGcodec</td><td rowspan=1 colspan=1>DMA2D</td><td rowspan=1 colspan=1>LCD_TFTcontroller(3)</td><td rowspan=1 colspan=1>LCDparallelinterface</td><td rowspan=1 colspan=1>MIPIDSIhosst(5)</td><td rowspan=1 colspan=1>Max AHBffrequency(MHz)</td></tr><tr><td rowspan=1 colspan=1>STM32F2x7</td><td rowspan=1 colspan=1>1 Mbyte</td><td rowspan=1 colspan=1>128</td><td rowspan=1 colspan=1>No</td><td rowspan=1 colspan=1>No</td><td rowspan=1 colspan=1>No</td><td rowspan=1 colspan=1>No</td><td rowspan=1 colspan=1>60</td><td rowspan=1 colspan=1>48</td><td rowspan=1 colspan=1>No</td><td rowspan=1 colspan=1>No</td><td rowspan=1 colspan=1>No</td><td rowspan=1 colspan=1>No</td><td rowspan=1 colspan=1>No</td><td rowspan=1 colspan=1>120</td></tr><tr><td rowspan=1 colspan=1>STM32F407ST1328417</td><td rowspan=1 colspan=1>1 Mbyte</td><td rowspan=1 colspan=1>192</td><td rowspan=1 colspan=1>No</td><td rowspan=1 colspan=1>No</td><td rowspan=1 colspan=1>No</td><td rowspan=1 colspan=1>No</td><td rowspan=1 colspan=1>60</td><td rowspan=1 colspan=1>54</td><td rowspan=1 colspan=1>No</td><td rowspan=1 colspan=1>No</td><td rowspan=1 colspan=1>No</td><td rowspan=1 colspan=1>No</td><td rowspan=1 colspan=1>No</td><td rowspan=1 colspan=1>168</td></tr><tr><td rowspan=1 colspan=1>STM32F427STM32F437</td><td rowspan=1 colspan=1>2 Mbytes</td><td rowspan=1 colspan=1>256</td><td rowspan=1 colspan=1>No</td><td rowspan=1 colspan=1>No</td><td rowspan=1 colspan=1>No</td><td rowspan=1 colspan=1>No</td><td rowspan=1 colspan=1>90</td><td rowspan=1 colspan=1>54</td><td rowspan=1 colspan=1>No</td><td rowspan=1 colspan=1>Yes</td><td rowspan=1 colspan=1>No</td><td rowspan=1 colspan=1>No</td><td rowspan=1 colspan=1>No</td><td rowspan=1 colspan=1>180</td></tr><tr><td rowspan=1 colspan=1>STM32F429STM32F439</td><td rowspan=1 colspan=1>2 Mbytes</td><td rowspan=1 colspan=1>256</td><td rowspan=1 colspan=1>No</td><td rowspan=1 colspan=1>No</td><td rowspan=1 colspan=1>No</td><td rowspan=1 colspan=1>No</td><td rowspan=1 colspan=1>90</td><td rowspan=1 colspan=1>54</td><td rowspan=1 colspan=1>No</td><td rowspan=1 colspan=1>Yes</td><td rowspan=1 colspan=1>Yes</td><td rowspan=1 colspan=1>No</td><td rowspan=1 colspan=1>No</td><td rowspan=1 colspan=1>180</td></tr><tr><td rowspan=1 colspan=1>STM32F446</td><td rowspan=1 colspan=1>512 Kbytes</td><td rowspan=1 colspan=1>128</td><td rowspan=1 colspan=1>Yes</td><td rowspan=1 colspan=1>No</td><td rowspan=1 colspan=1>No</td><td rowspan=1 colspan=1>No</td><td rowspan=1 colspan=1>90</td><td rowspan=1 colspan=1>54</td><td rowspan=1 colspan=1>No</td><td rowspan=1 colspan=1>No</td><td rowspan=1 colspan=1>No</td><td rowspan=1 colspan=1>No</td><td rowspan=1 colspan=1>No</td><td rowspan=1 colspan=1>180</td></tr><tr><td rowspan=1 colspan=1>STM32F469STM32F479</td><td rowspan=1 colspan=1>2 Mbytes</td><td rowspan=1 colspan=1>384</td><td rowspan=1 colspan=1>Yes</td><td rowspan=1 colspan=1>No</td><td rowspan=1 colspan=1>No</td><td rowspan=1 colspan=1>No</td><td rowspan=1 colspan=1>90</td><td rowspan=1 colspan=1>54</td><td rowspan=1 colspan=1>No</td><td rowspan=1 colspan=1>Yes</td><td rowspan=1 colspan=1>Yes</td><td rowspan=1 colspan=1>No</td><td rowspan=1 colspan=1>Yes</td><td rowspan=1 colspan=1>180</td></tr><tr><td rowspan=1 colspan=1>STM32F7x0</td><td rowspan=1 colspan=1>64 Kbytes</td><td rowspan=1 colspan=1>320</td><td rowspan=1 colspan=1>Yes</td><td rowspan=1 colspan=1>No</td><td rowspan=1 colspan=1>No</td><td rowspan=1 colspan=1>No</td><td rowspan=1 colspan=1>100</td><td rowspan=1 colspan=1>54</td><td rowspan=1 colspan=1>No</td><td rowspan=1 colspan=1>Yes</td><td rowspan=1 colspan=1>Yes</td><td rowspan=1 colspan=1>No</td><td rowspan=1 colspan=1>No</td><td rowspan=1 colspan=1>216</td></tr><tr><td rowspan=1 colspan=1>STM32F7x5</td><td rowspan=1 colspan=1>2 Mbytes</td><td rowspan=1 colspan=1>512</td><td rowspan=1 colspan=1>Yes</td><td rowspan=1 colspan=1>No</td><td rowspan=1 colspan=1>No</td><td rowspan=1 colspan=1>No</td><td rowspan=1 colspan=1>100</td><td rowspan=1 colspan=1>54</td><td rowspan=1 colspan=1>No</td><td rowspan=1 colspan=1>Yes</td><td rowspan=1 colspan=1>No</td><td rowspan=1 colspan=1>No</td><td rowspan=1 colspan=1>No</td><td rowspan=1 colspan=1>216</td></tr><tr><td rowspan=1 colspan=1>STM32F7x6</td><td rowspan=1 colspan=1>1 Mbyte</td><td rowspan=1 colspan=1>320</td><td rowspan=1 colspan=1>Yes</td><td rowspan=1 colspan=1>No</td><td rowspan=1 colspan=1>No</td><td rowspan=1 colspan=1>No</td><td rowspan=1 colspan=1>100</td><td rowspan=1 colspan=1>54</td><td rowspan=1 colspan=1>No</td><td rowspan=1 colspan=1>Yes</td><td rowspan=1 colspan=1>Yes</td><td rowspan=1 colspan=1>No</td><td rowspan=1 colspan=1>No</td><td rowspan=1 colspan=1>216</td></tr><tr><td rowspan=1 colspan=1>STM32F7x7</td><td rowspan=1 colspan=1>2 Mbytes</td><td rowspan=1 colspan=1>512</td><td rowspan=1 colspan=1>Yes</td><td rowspan=1 colspan=1>No</td><td rowspan=1 colspan=1>No</td><td rowspan=1 colspan=1>No</td><td rowspan=1 colspan=1>100</td><td rowspan=1 colspan=1>54</td><td rowspan=1 colspan=1>Yes</td><td rowspan=1 colspan=1>Yes</td><td rowspan=1 colspan=1>Yes</td><td rowspan=1 colspan=1>No</td><td rowspan=1 colspan=1>No</td><td rowspan=1 colspan=1>216</td></tr><tr><td rowspan=1 colspan=1>STM32F7x8SST132F7x9</td><td rowspan=1 colspan=1>2 Mbytes</td><td rowspan=1 colspan=1>512</td><td rowspan=1 colspan=1>Yes</td><td rowspan=1 colspan=1>No</td><td rowspan=1 colspan=1>No</td><td rowspan=1 colspan=1>No</td><td rowspan=1 colspan=1>100</td><td rowspan=1 colspan=1>54</td><td rowspan=1 colspan=1>Yes</td><td rowspan=1 colspan=1>Yes</td><td rowspan=1 colspan=1>Yes</td><td rowspan=1 colspan=1>No</td><td rowspan=1 colspan=1>Yes</td><td rowspan=1 colspan=1>216</td></tr><tr><td rowspan=1 colspan=1>STM32H723/733</td><td rowspan=1 colspan=1>1 Mbytes</td><td rowspan=1 colspan=1>564</td><td rowspan=1 colspan=1>No</td><td rowspan=1 colspan=1>Yes</td><td rowspan=1 colspan=1>No</td><td rowspan=1 colspan=1>No</td><td rowspan=1 colspan=1>137</td><td rowspan=1 colspan=1>110</td><td rowspan=1 colspan=1>No</td><td rowspan=1 colspan=1>Yes</td><td rowspan=1 colspan=1>Yes</td><td rowspan=1 colspan=1>No</td><td rowspan=1 colspan=1>No</td><td rowspan=1 colspan=1>240</td></tr><tr><td rowspan=1 colspan=1>STM32H725ST32H735</td><td rowspan=1 colspan=1>1 Mbyte</td><td rowspan=1 colspan=1>564</td><td rowspan=1 colspan=1>No</td><td rowspan=1 colspan=1>Yes</td><td rowspan=1 colspan=1>No</td><td rowspan=1 colspan=1>No</td><td rowspan=1 colspan=1>137</td><td rowspan=1 colspan=1>110</td><td rowspan=1 colspan=1>No</td><td rowspan=1 colspan=1>Yes</td><td rowspan=1 colspan=1>Yes</td><td rowspan=1 colspan=1>No</td><td rowspan=1 colspan=1>No</td><td rowspan=1 colspan=1>275</td></tr><tr><td rowspan=1 colspan=1>STM32H742ST32743ST32753</td><td rowspan=1 colspan=1>2 Mbytes</td><td rowspan=1 colspan=1>864</td><td rowspan=1 colspan=1>Yes</td><td rowspan=1 colspan=1>No</td><td rowspan=1 colspan=1>No</td><td rowspan=1 colspan=1>No</td><td rowspan=1 colspan=1>125</td><td rowspan=1 colspan=1>80</td><td rowspan=1 colspan=1>Yes</td><td rowspan=1 colspan=1>Yes</td><td rowspan=1 colspan=1>Yes</td><td rowspan=1 colspan=1>No</td><td rowspan=1 colspan=1>No</td><td rowspan=1 colspan=1>240</td></tr><tr><td rowspan=1 colspan=1>STM32H745ST132755</td><td rowspan=1 colspan=1>2 Mbytes</td><td rowspan=1 colspan=1>864</td><td rowspan=1 colspan=1>Yes</td><td rowspan=1 colspan=1>No</td><td rowspan=1 colspan=1>No</td><td rowspan=1 colspan=1>No</td><td rowspan=1 colspan=1>125</td><td rowspan=1 colspan=1>80</td><td rowspan=1 colspan=1>Yes</td><td rowspan=1 colspan=1>Yes</td><td rowspan=1 colspan=1>Yes</td><td rowspan=1 colspan=1>No</td><td rowspan=1 colspan=1>Yes</td><td rowspan=1 colspan=1>240</td></tr><tr><td rowspan=1 colspan=1>STM32H747ST132757</td><td rowspan=1 colspan=1>2 Mbytes</td><td rowspan=1 colspan=1>864</td><td rowspan=1 colspan=1>Yes</td><td rowspan=1 colspan=1>No</td><td rowspan=1 colspan=1>No</td><td rowspan=1 colspan=1>No</td><td rowspan=1 colspan=1>110</td><td rowspan=1 colspan=1>80</td><td rowspan=1 colspan=1>Yes</td><td rowspan=1 colspan=1>Yes</td><td rowspan=1 colspan=1>Yes</td><td rowspan=1 colspan=1>No</td><td rowspan=1 colspan=1>Yes</td><td rowspan=1 colspan=1>240</td></tr><tr><td rowspan=1 colspan=1>STM32H730</td><td rowspan=1 colspan=1>128 Kbytes</td><td rowspan=1 colspan=1>564</td><td rowspan=1 colspan=1>No</td><td rowspan=1 colspan=1>Yes</td><td rowspan=1 colspan=1>No</td><td rowspan=1 colspan=1>No</td><td rowspan=1 colspan=1>137</td><td rowspan=1 colspan=1>110</td><td rowspan=1 colspan=1>No</td><td rowspan=1 colspan=1>Yes</td><td rowspan=1 colspan=1>Yes</td><td rowspan=1 colspan=1>No</td><td rowspan=1 colspan=1>No</td><td rowspan=1 colspan=1>275</td></tr><tr><td rowspan=1 colspan=1>STM32H750</td><td rowspan=1 colspan=1>128 Kbytes</td><td rowspan=1 colspan=1>864</td><td rowspan=1 colspan=1>Yes</td><td rowspan=1 colspan=1>No</td><td rowspan=1 colspan=1>No</td><td rowspan=1 colspan=1>No</td><td rowspan=1 colspan=1>100</td><td rowspan=1 colspan=1>80</td><td rowspan=1 colspan=1>Yes</td><td rowspan=1 colspan=1>Yes</td><td rowspan=1 colspan=1>Yes</td><td rowspan=1 colspan=1>No</td><td rowspan=1 colspan=1>No</td><td rowspan=1 colspan=1>240</td></tr><tr><td rowspan=1 colspan=1>STM32H7A3STM32H7B3</td><td rowspan=1 colspan=1>2 Mbytes</td><td rowspan=1 colspan=1>1180</td><td rowspan=1 colspan=1>No</td><td rowspan=1 colspan=1>Yes</td><td rowspan=1 colspan=1>No</td><td rowspan=1 colspan=1>No</td><td rowspan=1 colspan=1>100</td><td rowspan=1 colspan=1>80</td><td rowspan=1 colspan=1>Yes</td><td rowspan=1 colspan=1>Yes</td><td rowspan=1 colspan=1>Yes</td><td rowspan=1 colspan=1>No</td><td rowspan=1 colspan=1>No</td><td rowspan=1 colspan=1>280</td></tr></table>

0 20

<table><tr><td rowspan=1 colspan=1>STM32 line</td><td rowspan=1 colspan=1>Max flashmemory size</td><td rowspan=1 colspan=1>On-chipSRAM(Kbytes)</td><td rowspan=1 colspan=1>QUADSPI</td><td rowspan=1 colspan=1>OCTOSPI</td><td rowspan=1 colspan=1>HSPI</td><td rowspan=1 colspan=1>XSPI</td><td rowspan=1 colspan=1>Max FMC(1)SRAM andSDRAMfrequencyMHz)</td><td rowspan=1 colspan=1>MaxDCMIpixelclockiinput(MHz)(2)</td><td rowspan=1 colspan=1>JPEGcodec</td><td rowspan=1 colspan=1>DMA2D</td><td rowspan=1 colspan=1>LCD_TFTcontroller(3)</td><td rowspan=1 colspan=1>LCDparallelinterface</td><td rowspan=1 colspan=1>MIPIDSIhost(5)</td><td rowspan=1 colspan=1>Max AHBfrequencyMHz)</td></tr><tr><td rowspan=1 colspan=1>STM32L4x6</td><td rowspan=1 colspan=1>1 Mbyte</td><td rowspan=1 colspan=1>320</td><td rowspan=1 colspan=1>Yes</td><td rowspan=1 colspan=1>No</td><td rowspan=1 colspan=1>No</td><td rowspan=1 colspan=1>No</td><td rowspan=1 colspan=1>40</td><td rowspan=1 colspan=1>32</td><td rowspan=1 colspan=1>No</td><td rowspan=1 colspan=1>Yes</td><td rowspan=1 colspan=1>No</td><td rowspan=1 colspan=1>No</td><td rowspan=1 colspan=1>No</td><td rowspan=1 colspan=1>80</td></tr><tr><td rowspan=1 colspan=1>STM32L4R9S32L459STM32L4R7STM32457ST32L4R5S132L455</td><td rowspan=1 colspan=1>2 Mbytes</td><td rowspan=1 colspan=1>640</td><td rowspan=1 colspan=1>No</td><td rowspan=1 colspan=1>Yes</td><td rowspan=1 colspan=1>No</td><td rowspan=1 colspan=1>No</td><td rowspan=1 colspan=1>60</td><td rowspan=1 colspan=1>48</td><td rowspan=1 colspan=1>No</td><td rowspan=1 colspan=1>Yes</td><td rowspan=1 colspan=1>Yes</td><td rowspan=1 colspan=1>No</td><td rowspan=1 colspan=1>Yes</td><td rowspan=1 colspan=1>120</td></tr><tr><td rowspan=1 colspan=1>STM32L4P5STM3L45</td><td rowspan=1 colspan=1>1 Mbyte</td><td rowspan=1 colspan=1>320</td><td rowspan=1 colspan=1>No</td><td rowspan=1 colspan=1>Yes</td><td rowspan=1 colspan=1>No</td><td rowspan=1 colspan=1>No</td><td rowspan=1 colspan=1>60</td><td rowspan=1 colspan=1>48</td><td rowspan=1 colspan=1>No</td><td rowspan=1 colspan=1>Yes</td><td rowspan=1 colspan=1>Yes</td><td rowspan=1 colspan=1>No</td><td rowspan=1 colspan=1>No</td><td rowspan=1 colspan=1>120</td></tr><tr><td rowspan=1 colspan=1>STM32U575/585</td><td rowspan=1 colspan=1>2 Mbytes</td><td rowspan=1 colspan=1>786</td><td rowspan=1 colspan=1>No</td><td rowspan=1 colspan=1>Yes</td><td rowspan=1 colspan=1>No</td><td rowspan=1 colspan=1>No</td><td rowspan=1 colspan=1>80</td><td rowspan=1 colspan=1>64</td><td rowspan=1 colspan=1>No</td><td rowspan=1 colspan=1>Yes</td><td rowspan=1 colspan=1>No</td><td rowspan=1 colspan=1>Yes</td><td rowspan=1 colspan=1>No</td><td rowspan=1 colspan=1>160</td></tr><tr><td rowspan=1 colspan=1>STM32U535/545</td><td rowspan=1 colspan=1>512 Kbytes</td><td rowspan=1 colspan=1>274</td><td rowspan=1 colspan=1>No</td><td rowspan=1 colspan=1>Yes</td><td rowspan=1 colspan=1>No</td><td rowspan=1 colspan=1>No</td><td rowspan=1 colspan=1>No</td><td rowspan=1 colspan=1>64</td><td rowspan=1 colspan=1>No</td><td rowspan=1 colspan=1>Yes</td><td rowspan=1 colspan=1>No</td><td rowspan=1 colspan=1>No</td><td rowspan=1 colspan=1>No</td><td rowspan=1 colspan=1>160</td></tr><tr><td rowspan=1 colspan=1>STM32U595/5A5STM32U5995A9</td><td rowspan=1 colspan=1>4 Mbytes</td><td rowspan=1 colspan=1>2514</td><td rowspan=1 colspan=1>No</td><td rowspan=1 colspan=1>Yes</td><td rowspan=1 colspan=1>Yes</td><td rowspan=1 colspan=1>No</td><td rowspan=1 colspan=1>80</td><td rowspan=1 colspan=1>64</td><td rowspan=1 colspan=1>No</td><td rowspan=1 colspan=1>Yes</td><td rowspan=1 colspan=1>Yes</td><td rowspan=1 colspan=1>Yes</td><td rowspan=1 colspan=1>Yes</td><td rowspan=1 colspan=1>160</td></tr><tr><td rowspan=1 colspan=1>STM32U5F7/5G7STM32U5F9/5G9</td><td rowspan=1 colspan=1>4 Mbytes</td><td rowspan=1 colspan=1>3026</td><td rowspan=1 colspan=1>No</td><td rowspan=1 colspan=1>Yes</td><td rowspan=1 colspan=1>Yes</td><td rowspan=1 colspan=1>No</td><td rowspan=1 colspan=1>80</td><td rowspan=1 colspan=1>64</td><td rowspan=1 colspan=1>Yes</td><td rowspan=1 colspan=1>Yes</td><td rowspan=1 colspan=1>Yes</td><td rowspan=1 colspan=1>Yes</td><td rowspan=1 colspan=1>Yes</td><td rowspan=1 colspan=1>160</td></tr><tr><td rowspan=1 colspan=1>STM32H533/523</td><td rowspan=1 colspan=1>512 Kbytes</td><td rowspan=1 colspan=1>272</td><td rowspan=1 colspan=1>No</td><td rowspan=1 colspan=1>Yes</td><td rowspan=1 colspan=1>No</td><td rowspan=1 colspan=1>No</td><td rowspan=1 colspan=1>100</td><td rowspan=1 colspan=1>100</td><td rowspan=1 colspan=1>No</td><td rowspan=1 colspan=1>No</td><td rowspan=1 colspan=1>No</td><td rowspan=1 colspan=1>Yes</td><td rowspan=1 colspan=1>No</td><td rowspan=1 colspan=1>250</td></tr><tr><td rowspan=1 colspan=1>STM32H563/573ST132562</td><td rowspan=1 colspan=1>2 Mbytes</td><td rowspan=1 colspan=1>640</td><td rowspan=1 colspan=1>No</td><td rowspan=1 colspan=1>Yes</td><td rowspan=1 colspan=1>No</td><td rowspan=1 colspan=1>No</td><td rowspan=1 colspan=1>100</td><td rowspan=1 colspan=1>100</td><td rowspan=1 colspan=1>No</td><td rowspan=1 colspan=1>No</td><td rowspan=1 colspan=1>No</td><td rowspan=1 colspan=1>Yes</td><td rowspan=1 colspan=1>No</td><td rowspan=1 colspan=1>250</td></tr><tr><td rowspan=1 colspan=1>STM32N6 series</td><td rowspan=1 colspan=1>0 Kbytes</td><td rowspan=1 colspan=1>4200</td><td rowspan=1 colspan=1>No</td><td rowspan=1 colspan=1>No</td><td rowspan=1 colspan=1>No</td><td rowspan=1 colspan=1>Yes</td><td rowspan=1 colspan=1>166</td><td rowspan=1 colspan=1>100</td><td rowspan=1 colspan=1>Yes</td><td rowspan=1 colspan=1>Yes</td><td rowspan=1 colspan=1>Yes</td><td rowspan=1 colspan=1>No</td><td rowspan=1 colspan=1>Yes</td><td rowspan=1 colspan=1>200</td></tr></table>

1. FSMC for STM32F2x7, STM32F407/417, STM32L4+, and STM32U5 devices. 2. Refer to the datasheet for the pixel clock frequency (DCMI_PIXCLK). 3. See the application note AN4861 for more details on the STM32 LTDC peripheral. 4. LCD parallel interface via the FMC parallel interface. 5Refer to the application note AN4860 for more details on the STM32 MIPI-DSI host.

# 3.2

# DCMI in a smart architecture

The DCMI isconnected othe AHB bus matri. Iis accesed by the DMA to transer the receiveimageta.   
The destination of the received data depends on the application.

The smart architecture of STM32 MCUs allows the following

The DMA, as an AHB master, transfers the received data (image number n+1) to the memory, while the CPU processes the previously captured image (image number n).   
The DMA2D, as an AHB master, is used to transfer or modify the received data (CPU resources are kept for other tasks).   
The memories throughput and the performance are improved thanks to the multi-layer bus matrix.

# 3.2.1

# STM32F2 system architecture

The STM32F2x7 devices are based on a 32-bit multi-layer bus matri, used to interconnect eight masters and seven slaves.The DCMI is a slave AHB2 peripheral. The DMA2 performs the data transfer from the DCMI to internal SRAMs or external memories through the FSMC.

Figure 6 shows the DCMI interconnection and the data path in the STM32F2x7 devices.

![](images/22668324e3dc869e30456c026687df8640bf4f6f2725740bc81c008a827043c6.jpg)  
Figure 6. DCMI slave AHB2 peripheral in the STM32F2x7

# 3.2.2

# STM32F4 system architecture

The STM32F407/417, STM32F427/437, STM32F429/439, STM32F446, and STM32F469/479 line devices are based on a 32-bit multilayer bus matrix, allowing the interconnection between:

Ten masters and eight slaves for the STM32F429/439 devices Ten masters and nine slaves for the STM32F469/479 devices Seven masters and seven slaves for the STM32F446 devices Eight masters and seven slaves for the STM32F407/417 devices Eight masters and eight slaves for the STM32F427/437 devices

The DCMI is a slave AHB2 peripheral. The DMA2 performs the data transfer from the DCMI to internal SRAMs or external memories through the FMC (FSMC for the STM32F407/417 line) or the QUADSPI.

Figure 7 shows the DCMI interconnection and the data path in these devices.

![](images/94746fda108767b9a568cd9b1b73632f70f458c184dec816115bf88d17356ea2.jpg)  
Figure 7. DCMI slave AHB2 peripheral in the STM32F4

# Note:

See the table below for details on the SRAMs.

The dual- or quad-SPI interface is available only in the STM32F469/479 and STM32F446 devices.

3.The 64-Kbyte CCM data RAM is not available in the STM32F446xx devices.

4The Ethernet MAC interface is not available in the STM32F446xx devices.

5The LTDC and DMA2D are only available in the STM32F429/439 and STM32F469/479 devices.

In the STM32F407/417 devices, there is no interconnection between:

The Ethernet master and the DCode bus of the flash memory The USB master and the DCode bus of the flash memory

In the STM32F446 devices, there is no interconnection between the USB master and the DCode bus of the flash memory.

7It is FMSC for the STM32F407/417 devices.

Table 3. SRAM availability in the STM32F4 series   

<table><tr><td rowspan=1 colspan=1>STM32 line</td><td rowspan=1 colspan=1>SRAM1 (Kbytes)</td><td rowspan=1 colspan=1>SRAM2 (Kbytes)</td><td rowspan=1 colspan=1>SRAM3 (Kbytes)</td></tr><tr><td rowspan=1 colspan=1>STM32F407/417</td><td rowspan=3 colspan=1>112</td><td rowspan=3 colspan=1>16</td><td rowspan=1 colspan=1>N/A</td></tr><tr><td rowspan=1 colspan=1>STM32F427/437, STM32F429/439</td><td rowspan=1 colspan=1>64</td></tr><tr><td rowspan=1 colspan=1>STM32F446</td><td rowspan=1 colspan=1>N/A</td></tr><tr><td rowspan=1 colspan=1>STM32F469/479</td><td rowspan=1 colspan=1>160</td><td rowspan=1 colspan=1>32</td><td rowspan=1 colspan=1>128</td></tr></table>

# 3.2.3

# STM32F7 system architecture

The STM32F7x5, STM32F7x6, STM32F7x7, STM32F7x8, and STM32F7x9 line devices, and the STM32F750 evihe7xvlu  as iultlayruatillw et between:

Twelve masters and eight slaves for the STM32F7x6, STM32F7x7, STM32F7x8, STM32F7x9, and   
STM32F750 devices   
Eleven masters and eight slaves for the STM32F7x5 devices

The DCMI is a slave AHB2 peripheral. The DMA2 performs the data transfer from the DCMI to internal SRAMor external memories through the FMC or the QUADSPI.

![](images/dd903ee78cdd9a0e74c071e98fa41293d1c169fb66588b30bbeedb921eb8aaf6.jpg)  
Figure 8 shows the DCMl interconnection and the data path in these devices.   
Figure 8. DCMI slave AHB2 peripheral in the STM32F7

# Note:

The I/D cache size is:

4 Kbytes for the STM32F7x5/F7x6 and STM32F750 devices   
16 Kbytes for the STM32F7x7/F7x8/F7x9 devices

2The LTDC is only available in the STM32F7x6/F7x7/F7x8/F7x9 and STM32F750 devices.

The DTCM RAM size is: 64 Kbytes for the STM32F7x5/F7x6 and STM32F750 devices 128 Kbytes for the STM32F7x7/F7x8/F7x9 devices

4The ITCM RAM size is 16 Kbytes for the STM32F7x6/F7x7/F7x8/F7x9 and STM32F750 devices.

5 The SRAM1 size is: 240 Kbytes for the STM32F7x5/F7x6 and STM32F750 devices 368 Kbytes for the STM32F7x7/F7x8/F7x9 devices

6The SRAM2 size is 16 Kbytes for the STM32F7x6/F7x7/F7x8/F7x9 and STM32F750 devices.

# 3.2.4

# STM32H7 system architecture

The STM32H723/733, STM32H743/753, STM32H7A3/B3, STM32H747/757, STM32H745/755, STM32H742, STM32H725/735, STM32H750, and STM32H730 line devices are based on an AXI bus matrix, two AHB bus matrices, and bus bridges allowing the interconnection between:

23 masters and 18 slaves for the STM32H745/755 and STM32H747/757 devices   
18 masters and 18 slaves for the STM32H723/733, STM32H725/735, STM32H753, and STM32H730   
devices   
19 masters and 18 slaves for the STM32H742 and STM32H743 devices   
19 masters and 20 slaves for the STM32H7A3/B3 devices   
19 masters and 17 slaves for the STM32H750 Value line devices

# 3.2.4.1

# STM32H7x3, STM32H742, STM32H725/735, STM32H730, and STM32H750 deviCeS

The DCMI is a slave AHB2 peripheral.The DMA1 and DMA2 perform the data transfer from the DCMI to iteral SRAMs or external memories through the FMC, the QUADSPI, or the OCTOSPI.

The DMA1 and DMA2 are located in the D2 domain. They are able to access the slaves in the D1 and D3 domains. As a result, the DMA1 and DMA2 can transfer the data received by the DCMI (located in D2) to memories located in the D1 or D3 domains.

![](images/91438a5fb7a777fb5a4842d201d027df6ae71f12e0d6fe20dd757074393a66d9.jpg)  
Figure 9 shows the DCMI interconnection and the data path in these devices.   
Figure 9. DCMI slave AHB2 peripheral in the STM32H723/733, STM32H743/753, STM32H742, STM32H725/735, STM32H730, and STM32H750 devices

# Note:

1. Flash B is not available in the STM32H723/733, STM32H725/735, STM32H730, and STM32H750 devices.   
2. OCTOSPI1 and 2 are not available in the STM32H743/753, STM32H742, and STM32H750 devices.   
3. OTFDEC1 and 2 are only available in the STM32H723/733, STM32H725/735, and STM32H730 devices.   
4. The QUADSPI is only available in the STM32H743/753, STM32H742, and STM32H750 devices.   
5. The 192-Kbyte AXI SRAM and the 92-Kbyte ITCM are only available in the STM32H723/733,   
STM32H725/735, and STM32H730 devices.   
6. The USBHS2 is only available in the STM32H743/753, STM32H742, and STM32H750 devices.   
7. The SRAM3 is only available in the STM32H743/753, STM32H74,2 and STM32H750 devices.   
8 There is no connection between the APB3 and the D2 domain in the STM32H723/733, STM32H725/735,   
STM32H730, and STM32H750 devices.   
9. See Table 4 for more details on the SRAM1, SRAM2, SRAM3 and the AXI SRAM.

Table 4. SRAM availability in the STM32H723/733, STM32H743/753, STM32H742, STM32H725/735, STM32H730, and STM32H750 devices   

<table><tr><td rowspan=1 colspan=1>STM32 line</td><td rowspan=1 colspan=1>SRAM1 (Kbytes)</td><td rowspan=1 colspan=1>SRAM2 (Kbytes)</td><td rowspan=1 colspan=1>SRAM3 (Kbytes)</td><td rowspan=1 colspan=1>AXI SRAM (Kbytes)</td></tr><tr><td rowspan=1 colspan=1>STM32H723/733</td><td rowspan=1 colspan=1>16</td><td rowspan=1 colspan=1>16</td><td rowspan=1 colspan=1>X</td><td rowspan=1 colspan=1>128</td></tr><tr><td rowspan=1 colspan=1>STM32H725/735</td><td rowspan=1 colspan=1>16</td><td rowspan=1 colspan=1>16</td><td rowspan=1 colspan=1>X</td><td rowspan=1 colspan=1>128</td></tr><tr><td rowspan=1 colspan=1>STM32H730</td><td rowspan=1 colspan=1>16</td><td rowspan=1 colspan=1>16</td><td rowspan=1 colspan=1>X</td><td rowspan=1 colspan=1>128</td></tr><tr><td rowspan=1 colspan=1>STM32H743/753</td><td rowspan=1 colspan=1>128</td><td rowspan=1 colspan=1>128</td><td rowspan=1 colspan=1>32</td><td rowspan=1 colspan=1>512</td></tr><tr><td rowspan=1 colspan=1>STM32H742</td><td rowspan=1 colspan=1>128</td><td rowspan=1 colspan=1>128</td><td rowspan=1 colspan=1>32</td><td rowspan=1 colspan=1>512</td></tr><tr><td rowspan=1 colspan=1>STM32H750</td><td rowspan=1 colspan=1>128</td><td rowspan=1 colspan=1>128</td><td rowspan=1 colspan=1>32</td><td rowspan=1 colspan=1>512</td></tr></table>

# 3.2.4.2

# STM32H745/755 and STM32H747/757 devices

The DMA1 and DMA2 are in the D2 domain. They are able to access slaves in the D1 and D3 domains. As a reu, the DMA1 and DMA2 can transfer the data received by the DCMI (located in D2) tomemoris locate in the D1 or D3 domains. Figure 10 shows the DCMI interconnection and the data path in these devices.

![](images/cfccf97923043cd4463e8c95853083961ab2a2d914ab2be0be2915178ffa4523.jpg)  
Figure 10. DCMI slave AHB2 peripheral in the STM32H745/755 and STM32H747/757 devices

# 3.2.4.3

# STM32H7A3/7B3 device

The DMA1 and DMA2 are in the CD domain. They are able to access slaves in the CD and SRD domains. As a reut, the DMA1 and DMA2 can transfer he data received by he DCMI (locate in theCD domain) tmemories located in theCD or SRD domain. Figure1 shows the DCMI interconnection and the data path in these devices.

![](images/4cded8a9d374e21a90a6f8f704ebf2661c4320c847323944a891176c6a41dc2c.jpg)  
Figure 11. DCMI slave AHB2 peripheral in the STM32H7A3/B3

# Note:

OTFDEC1/2 are only available in the STM32H7B3 devices.

# 3.2.5

# STM32L4 system architecture

The STM32L496xx and STM32L4A6xx devices are based on a 32-bit multilayer bus matrix, allowing the interconnection between six masters and eight slaves.

The DCMI is a slaveAHB2 peripheral. The DMA2 performs the dat transferfrom the DCMI to internal SRAMs external memories through the FMC or QUADSPI.

The DMA has only one port (not like STM32F2/F4/F7 and STM32H7 devices where the peripheral port is separated from the memory port), but it supports circular-buffer management, peripheral-to-memory, memory-to-peripheral, and peripheral-to-peripheral transfers.

![](images/eeb6c3ec6573498521eaefd54887dce024c2abf204580e5d570cf5adbfc97f12.jpg)  
Figure 12 shows the DCMl interconnection and the data path in these devices.   
Figure 12. DCMI slave AHB2 peripheral in STM32L496/4A6

# 3.2.6

# STM32L4+ system architecture

The STM32L4R9/S9, STM32L4R7/S7, STM32L4R5/S5, and STM32L4P5/Q5 line devices are based on a 32-bit multilayer bus matrix, allowing the interconnection between:

9 masters and 10 slaves for the STM32L4P5/Q5 devices

9 masters and 11 slaves for the STM32L4R5/S5, STM32L4R7/S7, and STM32L4R9/S9 devices

TheDCM is a slave AHB2 peripheral.he DMA1 and DMA2 perform the data transfer from the DCMI to interal SRAMs or external memories through the FSMC or OCTOSPI.

The DMA has only one port. I is different from the STM32F2/F4/F7 and STM32H7 devices where the peripheral p sparat ohememory rt.Howeve ort circularbuangementmemory-y peripheral-to-memory, memory-to-peripheral, and peripheral-to-peripheral transfers.

Figure 13 shows the DCMl interconnection and the data path in these devices.

![](images/cba1fedd39e1e32b21cb2733d0121c92ee7d95634abbb808197d40e32c16f6eb.jpg)  
Figure 13. DCMI slave AHB2 peripheral in the STM32L4+

# Note:

1The GFXMMU is only available in the STM32L4R5/4R7/4R9/4S5/4S7/4S9 devices.

The SDMMC1 is only available in the STM32L4P5/4Q5 devices

3The SRAM1 size is: 128 Kbytes for the STM32L4P5/4Q5 devices 192 Kbytes for the STM32L4R5/4R7/4R9/4S5/4S7/4S9 devices.

4.The SRAM2 size is 64 Kbytes for the STM32L4P5/4Q5/R5/4R7/4R9/4S5/4S7/4S9 devices.

128 Kbytes for the STM32L4P5/4Q5 devices   
384 Kbytes for the STM32L4R5/4R7/4R9/4S5/4S7/4S9 devices

# STM32U5 system architecture

The STM32U5 devices are based on a 32-bit multilayer AHB bus matrix, nabling the interconnection between:

16 masters and 13 slaves in the STM32U595/5A5, STM32U599/5A9, STM32U5F7/5G7, and   
STM32U5F9/5G9 devices   
11 masters and 10 slaves in the STM32U575/585 devices   
9 masters and 7 slaves in the STM32U535/545 devices

The DCMI is a slave AHB2 peripheral.

The GPDMA1 performs the data transfer from the DCMI to internal SRAMs or external memories through the FSMC, OCTOSPI, or HSPI.

Figure 14 shows the DCMl interconnection and the data path in these devices.

![](images/50a1ddb177bbc5cc145e15c829a652cc27c30e9b1ceb712a6a1966749bff9aca.jpg)  
Figure 14. DCMI slave AHB2 peripheral in the STM32U5 devices

Pixel path through the DCMI and GPDMA1 Pixel path to the memory destination   
o Bus multiplexer Fast bus multiplexer   
• Fast bus multiplexer on STM32U59x/5Ax/5Fx/5Gx Fast bus multiplexer on STM32U575/585

MPCBBx: Block-based memory protection controller MPCWMx: Watermark-based memory protection controller

__ Master Interface

Slave Interface

# Note:

1This peripheral is not present in the STM32U535/545.   
2. This peripheral is not present in the STM32U535/545/575/585.   
3. This peripheral is present only in the STM32U5F7/5G7, STM32U5F9/5G9.   
4See Table 5 for more details on the SRAM1/2/3/4/5/6 and the BKPSRAM

Table 5. SRAM availability in the STM32U5 devices   

<table><tr><td rowspan=1 colspan=1>STM32 lines</td><td rowspan=1 colspan=1>SRAM1Kbytes)</td><td rowspan=1 colspan=1>SRAM2Kbytes)</td><td rowspan=1 colspan=1>SRAM3Kbytes)</td><td rowspan=1 colspan=1>SRAM4Kbytes)</td><td rowspan=1 colspan=1>SRAM5Kbytes)</td><td rowspan=1 colspan=1>SRAM6 Kbytes)</td><td rowspan=1 colspan=1>BKSRAMKKytes)</td></tr><tr><td rowspan=1 colspan=1>STM32U535/545</td><td rowspan=1 colspan=1>192</td><td rowspan=1 colspan=1>64</td><td rowspan=1 colspan=1>X</td><td rowspan=1 colspan=1>16</td><td rowspan=1 colspan=1>X</td><td rowspan=1 colspan=1>X</td><td rowspan=1 colspan=1>2</td></tr><tr><td rowspan=1 colspan=1>STM32U575/585</td><td rowspan=1 colspan=1>192</td><td rowspan=1 colspan=1>64</td><td rowspan=1 colspan=1>512</td><td rowspan=1 colspan=1>16</td><td rowspan=1 colspan=1>X</td><td rowspan=1 colspan=1>X</td><td rowspan=1 colspan=1>2</td></tr><tr><td rowspan=1 colspan=1>STM32U595/5A5STM32U599/5A9</td><td rowspan=1 colspan=1>768</td><td rowspan=1 colspan=1>64</td><td rowspan=1 colspan=1>832</td><td rowspan=1 colspan=1>16</td><td rowspan=1 colspan=1>832</td><td rowspan=1 colspan=1>X</td><td rowspan=1 colspan=1>2</td></tr><tr><td rowspan=1 colspan=1>STM32U5F7/5G7STM32U5F9/5G9</td><td rowspan=1 colspan=1>768</td><td rowspan=1 colspan=1>64</td><td rowspan=1 colspan=1>832</td><td rowspan=1 colspan=1>16</td><td rowspan=1 colspan=1>832</td><td rowspan=1 colspan=1>512</td><td rowspan=1 colspan=1>2</td></tr></table>

# 3.2.8

# STM32H5 system architecture

The STM32H562 and STM32H563/573 devices are based on a 32-bit multilayer AHB bus matrix, enabling the interconnection between 13 masters and 10 slaves.

The DCMI is a slave AHB2 peripheral.

The GPDMA1 performs the data transfer from the DCMI to internal SRAMs or external memories through the FMC or OCTOSPI.

Figure 15 shows the DCMl interconnection and the data path in these devices.

![](images/5ac1e6868f5f190e09d06f3a7930fc702e6dff59c082d97254ad77e5aa134b12.jpg)  
Figure 15. DCMI slave AHB2 peripheral for the STM32H562 and STM32H563/573

# __ Master Interface

Slave Interface

Bus multiplexer

D Fast bus multiplexer

MPCBBx: Block-based memory protection controller MPCWMx: Watermark-based memory protection controller

Pixel path through the DCMI and GPDMA1 , Pixel path through the DCMI and GPDMA2 Pixel path to the memory destination

# 3.2.9

# STM32N6 system architecture

The STM32N6 devices are based on a 32-bit multilayer AHB busmatrix, enabling theinterconnection between 8 masters and 29 slaves.

The DCMI is a slave AHB5 peripheral. The PDMA performs the data transfer from the DCMI to internal SRAM or external memories through the FMC or the XSPI.

# 4 Reference boards with DCMI and/or camera modules

Many STM32 reference boards are available. Most of them embed the DCMI, and someof them have an obord camera module.The board selection depends o the application and the hardwareresourcesThe table below summarizes the DCMI, the camera modules, and the memories availability across various STM32 boards.

Table 6. DCMI and camera modules on STM32 boards   

<table><tr><td rowspan=1 colspan=1>STM32 line</td><td rowspan=1 colspan=1>Board</td><td rowspan=1 colspan=1>Cameramodule</td><td rowspan=1 colspan=1>CMOSsensor</td><td rowspan=1 colspan=1>Internal SRAMKbytes)</td><td rowspan=1 colspan=1>External SDRAMbus width (bits)</td><td rowspan=1 colspan=1>External SRAMbus width (bits)</td></tr><tr><td rowspan=2 colspan=1>STM32F2x7</td><td rowspan=1 colspan=1>STM3220G-EVAL</td><td rowspan=2 colspan=1>Yes(1)</td><td rowspan=2 colspan=1>OV2640 orO9655</td><td rowspan=2 colspan=1>132</td><td rowspan=5 colspan=2>N/A</td></tr><tr><td rowspan=1 colspan=1>STM3221G-EVAL</td></tr><tr><td rowspan=3 colspan=1>STM32F407/417</td><td rowspan=1 colspan=1>STM32F4DISCOVERY</td><td rowspan=1 colspan=1>N/A()(3)</td><td rowspan=3 colspan=1>OV9655</td><td rowspan=3 colspan=1>196</td></tr><tr><td rowspan=1 colspan=1>STM3240G-EVAL</td><td rowspan=2 colspan=1>Yes(1)</td></tr><tr><td rowspan=1 colspan=1>STM3241G-EVAL</td></tr><tr><td rowspan=3 colspan=1>STM32F429/439</td><td rowspan=1 colspan=1>32F429IDISCOVERY</td><td rowspan=1 colspan=1>N/A(3)</td><td rowspan=1 colspan=1>N/A</td><td rowspan=1 colspan=1></td><td rowspan=1 colspan=1>16</td><td rowspan=1 colspan=1>N/A</td></tr><tr><td rowspan=1 colspan=1>STM32429I-EVAL</td><td rowspan=2 colspan=1>Yes(4)</td><td rowspan=2 colspan=1>OV2640 orO9655</td><td rowspan=2 colspan=1>256</td><td rowspan=2 colspan=1>32</td><td rowspan=2 colspan=1>16</td></tr><tr><td rowspan=1 colspan=1>STM32439I-EVAL</td></tr><tr><td rowspan=1 colspan=1>STM32F446</td><td rowspan=1 colspan=1>STM32446E-EVAL</td><td rowspan=1 colspan=1>Yes(5)</td><td rowspan=1 colspan=1>S5k5CAGA</td><td rowspan=1 colspan=1>128</td><td rowspan=1 colspan=1>16</td><td rowspan=1 colspan=1>N/A</td></tr><tr><td rowspan=3 colspan=1>STM32F469/479</td><td rowspan=1 colspan=1>32F469IDISCOVERY</td><td rowspan=1 colspan=1>N/A(3)</td><td rowspan=1 colspan=1>N/A</td><td rowspan=3 colspan=1>388</td><td rowspan=3 colspan=1>32</td><td rowspan=1 colspan=1>N/A</td></tr><tr><td rowspan=1 colspan=1>STM32469I-EVAL</td><td rowspan=2 colspan=1>Yes(5)</td><td rowspan=2 colspan=1>S5k5CAGA</td><td rowspan=2 colspan=1>16</td></tr><tr><td rowspan=1 colspan=1>STM32479I-EVAL</td></tr><tr><td rowspan=1 colspan=1>STM32F7x0</td><td rowspan=1 colspan=1>STM32F7508DISCOVERY</td><td rowspan=1 colspan=1>N/A(3)</td><td rowspan=1 colspan=1>OV9655</td><td rowspan=1 colspan=1>340</td><td rowspan=1 colspan=1>32</td><td rowspan=1 colspan=1>N/A</td></tr><tr><td rowspan=3 colspan=1>STM32F7x6</td><td rowspan=1 colspan=1>32F746GDISCOVERY</td><td rowspan=1 colspan=1>Yes(6)</td><td rowspan=1 colspan=1>OV9655</td><td rowspan=1 colspan=1></td><td rowspan=1 colspan=1>16</td><td rowspan=1 colspan=1>N/A</td></tr><tr><td rowspan=1 colspan=1>STM32746G-EVAL</td><td rowspan=2 colspan=1>Yes(5)</td><td rowspan=2 colspan=1>S5k5CAGA</td><td rowspan=2 colspan=1>320</td><td rowspan=2 colspan=1>32</td><td rowspan=2 colspan=1>16</td></tr><tr><td rowspan=1 colspan=1>STM32756G-EVAL</td></tr><tr><td rowspan=3 colspan=1>STM32F7x9</td><td rowspan=1 colspan=1>32F769IDISCOVERY</td><td rowspan=1 colspan=1>N/A(3)</td><td rowspan=1 colspan=1>N/A</td><td rowspan=3 colspan=1>512</td><td rowspan=3 colspan=1>32</td><td rowspan=1 colspan=1>N/A</td></tr><tr><td rowspan=1 colspan=1>STM32F769I-EVAL</td><td rowspan=2 colspan=1>Yes(5)</td><td rowspan=2 colspan=1>S5k5CAGA</td><td rowspan=2 colspan=1>16</td></tr><tr><td rowspan=1 colspan=1>STM32F779I-EVAL</td></tr><tr><td rowspan=1 colspan=1>STM32H7x3</td><td rowspan=1 colspan=1>STM32H743I-EVALSTM32H753I-EVAL</td><td rowspan=1 colspan=1>N/A(3)</td><td rowspan=1 colspan=1>N/A</td><td rowspan=1 colspan=1>864</td><td rowspan=1 colspan=1>32</td><td rowspan=1 colspan=1>16</td></tr><tr><td rowspan=1 colspan=1>STM32H747/757</td><td rowspan=1 colspan=1>STM32H747DISCOVERY</td><td rowspan=1 colspan=1>Yes(7)</td><td rowspan=1 colspan=1>OV5640 or 965</td><td rowspan=1 colspan=1>868</td><td rowspan=1 colspan=1>32</td><td rowspan=1 colspan=1>N/A</td></tr><tr><td rowspan=1 colspan=1>STM32H7A3/B3</td><td rowspan=1 colspan=1>STM32H7B3I-EVAL</td><td rowspan=1 colspan=1>Yes(8)</td><td rowspan=1 colspan=1>OV5640</td><td rowspan=1 colspan=1>1600</td><td rowspan=1 colspan=1>32</td><td rowspan=1 colspan=1>N/A</td></tr><tr><td rowspan=1 colspan=1>STM32L4x6</td><td rowspan=1 colspan=1>32L496GDISCOVERY</td><td rowspan=1 colspan=1>Yes(6)</td><td rowspan=1 colspan=1>OV9655</td><td rowspan=1 colspan=1>320</td><td rowspan=2 colspan=2>N/A</td></tr><tr><td rowspan=1 colspan=1>STM32L4+</td><td rowspan=1 colspan=1>32L4R9IDISCOVERY</td><td rowspan=1 colspan=1>Yes(8)</td><td rowspan=1 colspan=1>OV9655</td><td rowspan=1 colspan=1>640</td></tr><tr><td rowspan=4 colspan=1>STM32U5</td><td rowspan=1 colspan=1>STM32U575I-EVAL</td><td rowspan=1 colspan=1>Yes(8)</td><td rowspan=1 colspan=1>OV5640</td><td rowspan=1 colspan=1>786</td><td rowspan=1 colspan=1>N/A</td><td rowspan=1 colspan=1>N/A</td></tr><tr><td rowspan=1 colspan=1>STM32U5F9J-DK1</td><td rowspan=1 colspan=1>N/A(3)</td><td rowspan=1 colspan=1>N/A</td><td rowspan=1 colspan=1>3026</td><td rowspan=1 colspan=1>N/A</td><td rowspan=1 colspan=1>N/A</td></tr><tr><td rowspan=1 colspan=1>STM32U5F9J-DK2</td><td rowspan=1 colspan=1>N/A(3)</td><td rowspan=1 colspan=1>N/A</td><td rowspan=1 colspan=1>3026</td><td rowspan=1 colspan=1>N/A</td><td rowspan=1 colspan=1>N/A</td></tr><tr><td rowspan=1 colspan=1>STM32U599J-DK</td><td rowspan=1 colspan=1>N/A(3)</td><td rowspan=1 colspan=1>N/A</td><td rowspan=1 colspan=1>2514</td><td rowspan=1 colspan=1>N/A</td><td rowspan=1 colspan=1>N/A</td></tr><tr><td rowspan=1 colspan=1>STM32H573</td><td rowspan=1 colspan=1>STM32H573I-DK</td><td rowspan=1 colspan=1>N/A(3)</td><td rowspan=1 colspan=1>N/A</td><td rowspan=1 colspan=1>644</td><td rowspan=1 colspan=1>16</td><td rowspan=1 colspan=1>16</td></tr></table>

00H (CMOS sensor OV2640, 2 megapixels) means o vailblTe apliatonus s ede amoulecpatible wi  M i The camera module can be connected to the DCMI through the GPIO pins.

4. The camera module daughterboard MB1066 is connected.   
5. The camera module daughterboard MB1183 is connected.   
6.   
7. The camera module can be connected with caution before powering the Discovery board.   
8. The camera module daughter board MB1379 is connected.

# 5 DCMI description

# Note:

This section details the DCM and itmaner dealig with theimage data and the ynchronization sinals.   
The DCMI supports only the slave input mode.

# 5.1

# Hardware interface

The DCMI consists of:

Up to 14 data lines (D13-D0) The pixel clock line DCMI_PIXCLK The DCMI_HSYNC line (horizontal synchronization) The DCMI_VSYNC line (vertical synchronization).

The DCMI comprises up to 17 inputs. Depending on the number of data lines enabled by the user (8, 10, , or 14), the number of the DCMI inputs varies (11, 13, 15, or 17 signals).

If lehait ata wi is heu pimust ot esee al functions. The unused input pins can be assigned to other peripherals.

In the case of embedded synchronization, the DCMI needs only nine inputs (eight data lines and DCMI_PIXCLK) to operate properly. The eight unused pins can be used for GPiO or other functions.

Figure 16 shows the DCMI signals.

![](images/c6f9686ae9191d783bc42fb0f11be08d7011728fcf228f94582975a18f32050a.jpg)  
Figure 16. DCMI signals

= transferred each DCMI_PIXCLK cycle, and packed into a 32-bit register.

Figure 17 shows the four main DCMI components.

![](images/53218641e5a29b1fc370743994fddb8369a4315fcf3aea329a8f05c558ab9b31.jpg)  
Figure 17. DCMl block diagram: example of 12-bit data width

Note: \* D12 and D13 are not used for the 12-bit data width example.

The DCMI synchronizer ensures the control of the ordered sequencing of the data flow through the DCMI. It controls the data extractor, the FIFO, and the 32-bit register.   
The data extractor ensures the extraction of the data received by the DCMI.   
The 4-word FIFO is implemented to adapt the data rate transfers to the AHB. There is no overrun pretion prevent datfrom beingverrtenheHBdesot sustainhedattransert In erunrerors in the synchronization signals, the FFO is rse, and the DCMI waits or a new star frame.

A2-bit data register where the data bits are packed or transerthrough a general-purpose DMA channel. The placement of the captured data in the 32-bit register depends on the data width:

For an 8-bit data width, the DCMI captures the eight LSBs (the six other inputs D[13:8] are ignored). The first captured data byte is placed in the LSB position in the 32-bit word, and the fourth captured data byte is placed in the MSB position. In this case, a 32-bit data word is made up every four pixel clock cycles. For more details, see Section 5.6.

DCMI_DR Dn + 3 [7:0] Dn + 2 [7:0] Dn+1 [7:0] Dn [7:0] Bit number [31 24|23 16|15 817 0

For a 10-bit data width, the DCMI captures the 10 LSBs (the four other inputs D[13:10] are ignored). The first 10 bits captured are placed as the 10 LSBs of a 16-bit word. The remaining MSBs in the 16- bit word of the DCMlDR register (bits 10 to 15) are cleared. In this case, a 32-bit data word is made up every two pixel clock cycles.

DCMI_DR 000000 Dn + 1 [9:0] 000000 Dn [9:0] Bit number |31 26 25 16|15 10|9 0

For a 12-bit data width, the DCMI captures the 12-bit LSBs (the two other inputs D[13:12] are ignored). The first 12 bits captured are placed as the 12 LSBs of a 16-bit word. The remaining MSBs in the 16-bit word of the DCMIDR register (bits 2 to 15) are cleared. In this case, a 32-bit data word is made up every two pixel clock cycles.

DCMI_DR 0000 Dn + 1 [11:0] 0000 Dn [11:0] Bit number | 31 28|27 16 |15 12/11 0

For a 14-bit data width, the DCMI captures allthe received bits. The first 14 bits captured are placed as the 14 LSBs of a 16-bit word. The remaining MSBs in the 16-bit word of the DCMI_DR register (bits 4 and 15) are cleared. In this case, a 32-bit data word is made up every two pixel clock cycles.

DCMI_DR 00 Dn + 1 [13:0] 00 Dn [13:0] Bit number |31 30| 29 16 |15 14|13 0|

# 5.2

# Camera module and DCMI interconnection

As mentionedinSecton.., the camera modul sconeced othe DCMI through the ollowing sigal tpes:

DCMI clock and data signals I2C configuration signals

![](images/f083b124ce59ec12106eecc1f393a3d223130da54cef38c3c936ccde0274a81c.jpg)  
Figure 22. STM32 MCU and camera module interconnection

# 5.3

# DCMI functional description

T w es a heteal DM ceatin  ivn eampleat fo the system bus matrix:

After receiving the different signals, the synchronizercontrols the data flow through the different DCM components (data extractor, FIFO, and 32-bit data register).

Bei extracted b the extractordata e packe inhe -worFF theodere in he bit rr

3Once the 32-bit data block is packed in the register, a DMA request is generated.

The DMA transfers the data to the corresponding memory destination.

Depending on the application, data stored in the memory can be processed differently.

Note:

It is assumed that all image preprocessing is performed in the camera module.

# 5.4

# Data synchronization

The camera interface has a configurable parallel data interface from 8 to 14 data lines, together with:

A pixel clock line, DCMI_PIXCLK (rising/falling edge configuration) A horizontal synchronization line, DCMI_HSYNC A vertical synchronization line, DCMI_VSYNC, with a programmable polarity

The DCMI_PIXCLK and AHB clocks must respect the minimum ratio AHB/DCMI_PIXCLK of 2.5. Smmoulor heatn whihor ehra embedded synchronization.

# Hardware (or external) synchronization

In this mode, the DCMI_VSYNC and DCMI_HSYNC signals are used for the synchronization:

The line synchronization is always referred to as DCMI_HSYNC (also known as LINE VALID).

The frame synchronization is always referred to as DCMI_VSYNC (also known as FRAME VALID).

The polarities of the DCMI_PIXCLK and the synchronization signals (DCMI_HSYNC and DCMI_VSYNC) are programmable.

Da  wi DXael e pil coc on the configured polarity.

If the DCMI_VSYNC and DCMI_HSYNC signals are programmed active level (active high or active low), the data is not valid in the parallel interface when VSYNC or HSYNC is at that level (high or low).

For example, if VSYNC is programmed active high:

When VSYNC is low, the data is valid.   
When VSYNC is high, the data is not valid (vertical blanking).

The DCMI_HSYNC and DCMI_VSYNC signals act like blanking signals, since all data received during DCMI_HSYNC/DCMI_VSYNC active periods are ignored.

Figure 23 shows an example of data transfer when DCM_VSYNC and DCMI_HSYNC are active high, and when the capture edge for DCMi_PIXCLK is the rising edge.

![](images/897663ffacf7c46bd7126fd39d7fc138eb44e7fefbb3a34682548a5e58c681ca.jpg)  
Figure 23. Frame structure in hardware synchronization mode

# Compressed data synchronization

For compressed data (JPEG), the DCMI supports only the hardware synchronization. Each JPEG stream is divided into packets, which have programmable ize The packets dispatching depends n the image content, and results in a variable blanking duration between two packets.

DCMI_HSYNC is used to signal the start/end of a packet. DCMI_VSYNC is used to signal the start/end of the stream.

If the full data stream finishes and the detection of an end-of-stream does not occur (DCMl_VSYNC does not change), the DCMI pads out the end-of-frame by inserting zeros.

# 5.4.2

# Embedded (or internal) synchronization

Inthis case, delimiter codes are used or synchronization.These codes are embedded within the data flow to indicate the start/end of line or the start/end of frame.

# Note:

Thee codes are suppored only for 8-bit parallel data interface width. For other data widths, this mode generates unpredictable results, and must not be used.

The codes eliminate the need for DCMI_HSYNC and DCMI_VSYNC to signal the end/start of the line or the Whencratnmohevalushat must ot es nval contro the data values.Image data can then have only 254 possible values (x00 <image data value < xFF.

Each synchronization code consists of 4-byte sequence 0xFF 00 00 XY (as shown in Figure 24), where all delimiter codes have the same first 3-byte sequence OxFF 00 00. Only the final one OxXY is programmed to indicate the corresponding event.

Figure 24. Embedded code bytes   

<table><tr><td rowspan=1 colspan=1>Embededcode</td><td rowspan=1 colspan=1>0xFF</td><td rowspan=1 colspan=1>0x00</td><td rowspan=1 colspan=1>0x00</td><td rowspan=1 colspan=1>0xXY</td></tr></table>

DCMI_DR← Common bytes for all codes ←Variable byte →

# 5.4.2.1

# Mode 1

This mode is ITU656 compatible (ITU656 is the digital video protocol ITU-R BT.656). The following reference codes indicate a set of four events:

SAV (active line): line-start   
EAV (active line): line-end   
SAV (blanking): line-start during inter-frame blanking period EAV (blanking): line-end during inter-frame blanking period

Figure 25 illustrates the frame structure using this mode.

(banking) Vertical (or frame) blanking (anking) DataLine_0   
(active line) (@ctiveie ina Iin) Hozonta DataLine_N   
(banking) Vertical (or frame) blanking (banking)   
Synchronization code Data Blanking

# 5.4.2.2

# Mode 2

The embedded synchronization codes signal another set of events:

Frame-start (FS) Frame-end (FE) Line-start (LS) Line-end (LE)

A Oxval prorameas  rme-nd FE)mens hat ll heus codshe ossible alues es other than FS, LS, LE) are interpreted as valid FE codes.

I an FE code followed by an FS code.

Figure 26 illustrates the frame structure when using this mode.

Vertical (or frame) blanking FS DataLine_0 LE Horizontal (or line) LS blanking DataLine_N FE Vertical (or frame) blanking Synchronization code Data Blanking

# Note:

The camera modules can have up to eight synchronization codes in interleaved mode. This mode is then not surted by the camer interac oherisvery otherhal ame  arded When usinghe eed synchronization mode, the DCMI does not support the compressed data (JPEG) and the crop feature.

# 5.4.2.3

# Embedded unmask code

Tdeo a tnmankhecot all the receive code with the programmed one to set the corresponding event, he user can select only some unmasked bits to compare with the bits of the programmed code having the same position.

The user applies a mask to the corresponding code by configuring the DCMI embeded synchronization unmask register (DCMI_ESUR). Each byte in this register is an unmask code, corresponding to an embedded synchronization code:

Tmos int yherelis U):ec  t pl hat h the frame-end-code, must be compared with the received data to know if it is a frame-end event or not. Ths by s he en eliask LEU):each t et pls that his i in theiend-code, must be compared with the received data to know if it is a line-end event or not. Tcode, must be compared with the received data to know if it is a line-start event or not. T nt y earl )  plat h the framestart-code must beomparedwith he eceivedat to know s aframestarevent not.

different codes corresponding t e event) have theunmasked bts inhe same position (sameunmask de).

Example: FSC = 0xA5 and unmask code FSU = 0x10 (as shown in Figure 27). In this case the frame-start ane neere u pae nlye received code with the bit number 4 of the programmed code, to know if it is a frame-start event or not.

![](images/3052ee410486117fbc3049d5dad26649e24fb80e6166be66374d2398a9ac2cd8.jpg)  
Figure 27. Embedded code unmasking

# Note:

Make sure that each synchronization code has different unmask code to avoid synchronization errors.

# 5.5

# Capture modes

Tts optaot g a  ). Theuser can control thecapture rate b selecting the bytes, les and frames capture n the DCCR ..

# 5.1 Snapshot mode

Ind gleamptuerheapt  bl ett APTURb DCMR, theinteace wait r eetectiosarfameheext DCM e extbeeamat code, depending on the synchronization mode) before sampling the data.

Once the first complete frame is received, the DCMI is automatically disabled (CAPTURE bit automatically disabled.

![](images/352b0a55cd7db88a624960458bc5bd3d91f538138111783d1ab25ab39dfe7609.jpg)  
Figure 28. Frame reception in snapshot mode

# 5.5.2 Continuous grab mode

Ool n hepu bl APRE= )e wahe star of frame the next DCMIVYCor thenext embeded frame-start code,depending on the synchronizatn mode) before sampling the data.

In this mode, the DCMI can be configured to capture all the frames, every alternate frame (50% bandwidth recton), reframeut f four 5% bandwidt reduction).The camera interfac  ot automaically disabled but the user must disable it by setting CAPTURE = 0. After being disabled by the user, the DCM continues to grab data until the end of the current frame.

![](images/d0eaaa1c57dafe58eb5a81c457146d38654e39180c6d90ded0785078f31f6271.jpg)  
Figure 29. Frame reception in continuous grab mode

# 5.6

# Data formats and storage

The DCMI supports the following data formats:

8-bit progressive video: either monochrome or raw Bayer   
YCbCr 4:2:2 progressive video   
RGB565 progressive video   
Compressed data (JPEG)

For monochrome, RGB and YCbCr, the frame buffer is stored in raster mode as shown in Figure 30.

![](images/e0d0d0d8c2d475e6619d7dc60f0ff1e1372c161f63f68204c4ea9e2498255734.jpg)  
Figure 30. Pixel raster scan order

# Note:

eeen the smallest address).

Data received from the camera can be organized in lines, frames (raw YUv/RGB/Bayer modes), or can be a sequence of JPEG images.

T case since a DMA request is generated each time a complete 32-bit word has been constructed from the cature atWhenfamete nd wor nesot bee c received, the remaining data are padded with zeros, and a DMA request is generated.

# 5.6.1 Monochrome

The DCMI supports themonorome format 8 bpp. In he case a 8-bit data width is selected when con the DCMl, the data register has the structure shown in Figure 31.

DCMI_DR Dn + 3 Dn + 2 Dn+1 Dn Bit number 31 24|23 16 15 87 0

# 5.6.2 RGB565

RGB refers to Red Green, and Blue, which represent the three hues of light.Any color is obtained by ixing these three colors.

565 is used to indicate that each pixel consists of 16 bits divided as follows:

5 bits for encoding the red value (the most significant 5 bits)   
6 bits for encoding the green value   
5 bits for encoding the blue value (the less significant 5 bits)

Ea coenthas he same spatial rsolutin :4:4 ormat) each sample as  r (R), a green (G a blu  component. Figure shows the DCMI data registercontaining RGB data, when an 8-bit data with is selected.

![](images/47acd5b54973881caa83aea23872630a5f2528cb096944de3b14be4e88c0e3ca.jpg)  
Figure 32. DCMI data register filled with RGB data

# 5.6.3 YCbCr

Y fmilcolorspacesha eparate heiancum ihtfom heria chroma (color differences).

YCbCr consists of three components:

Y refers to the luminance or luma (black and white).   
Cb refers to the blue difference chroma.   
Cr refers to the red difference chroma.

Yr 4::2 s a subsampling heme, which requires a hal esolution in horizontal drection:r evy w horizontal Y samples, there is one Cb or Cr sample.

Eac component (, b, and Cr) is encoded in 8 bits. Figure 33 shows the DCMI data register containing YCbC data when an 8-bit data width is selected.

Figure 31. DCMI data register filled with monochrome data   
Figure 33. DCMI data register filled with YCbCr data   

<table><tr><td rowspan=1 colspan=1>DCMI_DR</td><td rowspan=1 colspan=1>Yn + 1</td><td rowspan=1 colspan=1>Crn</td><td rowspan=1 colspan=1>Yn</td><td rowspan=1 colspan=1>Cbn</td></tr></table>

<table><tr><td>Bit number 31</td><td></td><td>24|23</td><td>16 | 15</td><td></td><td>8 |7</td><td>0</td></tr></table>

# 5.6.4

# YCbCr, Y only

Note:

This data format is only available for the STM32F446, STM32F469/479, STM32F7, STM32H7, STM32L496, STM32L4A6, STM32L4+, STM32U5, STM32H5, and STM32N6 devices listed in Table 1.

The buf contains nly heYinforation monohrome mage.The hroma inormation sdroppe.Oy he u cpen ach pielcode  8 bits,  storeTheesul s mooroemagehavigalhoizontal esolution of the original image Cbr data).Figure shows the DCMI register when a -i data width is selected.

DCMI_DR Yn +3 Yn+2 Yn+1 Yn Bit number [31 24/23 16 15 817 0

# 5.6.5

# JPEG

For cpres data (JPEG, he DCMI supports only he hardware synchronzation, and he input z s ot limited. Each JPEG stream is divided into packets, which have programmable size. The packet dispatching depends on the image content, and results in a variable blanking duration between two packets.

Toallow JPEGa tin, e JPEG  ust be t  one n he DCMIRegis Te JPEGa not stored as lines and frames.The DCMIVSYNC signal is used to start the capture while DCMHSYNC serves as a data enable signal.

If the full data stream finishes and the detection of an end of stream does not occur (DCMI_VSYNC does not the end of the stream, the DCMI pads the remaining data with zeros.

# Note:

The crop feature and embedded synchronization mode cannot be used in the JPEG format.

![](images/0402e31ffef52ff3a1cefd3072fe16eb24e467adf9cae9ea386ba8a950de0d9f.jpg)  
Figure 35. JPEG data reception

# 5.7

# Crop feature

With rop feature ecamer interface elect rectangular windowfrom he receiv magTe ar coordinates (upper-left corner) are specified in the 32-bit DCMI_CWSTRT register.

The windw i secif iumber  pielclocks horizontal dmensin, d inmber l l dimension) in the DCMI_CWSIZE register.

# 5.8

# Image resizing (resolution modification)

Note:

This feature is only available for STM32F446, STM32F469/479, STM32F7x5/6/7/8/9, STM32F750, STM32H7, STM32L496xx, STM32L4A6, STM32L4+, STM32U5, STM32H5, and STM32N6 devices listed in Table 1.

As described in Section 5.5, the DCMI capture features are set through the DCMI_CR register.

T M captus l v e eu to heuser  hoos pture he vn lines).

T auerl olnht n eie   fm divided by two (only the odd or the even lines are received).

This interface also allows the capture of:

All received data   
v oher bye fe id dat e byeu tolyhe   e ven byts   
One byte out of four   
Two bytes out of four

This featureaffects the horizontal resolutin allowing the user to select neof the follwig resolutons:

The full horizontal resolution   
The half of the horizontal resolution   
The quarter of the horizontal resolution (available only for 8 bpp data formats)

# Caution:

Foret  sa, theoatonheoznt oluin allowsan format. For example, when the data format is YCbCr, the data is received interleaved (CbYCrYCbYCr). When the user chooses to receive every other byte, the DCMI receives only the Y component o each sample, means convetingbrdata intoY-only dataThis conversionafects both thehorizontal esolution ony hal e image is received), and the data format.

Figure 36 shows one frame when receiving only one byte out of four and one line out of two.

![](images/c1eabfc17b4bb2f7d1a5b89bcd6cf856cf3d64ef36af118d02eca0bfab09e8ce.jpg)  
Figure 36. Frame resolution modification

# 5.9

# DCMI interrupts

The following interrupts can be generated:

IT_LINE indicates the end of line.   
IT_FRAME indicates the end of frame capture.   
IT_OVR indicates the overrun of data reception.   
IT_VSYNC indicates the synchronization frame.   
IT_ERR indicates the detection of an error in the embedded synchronization code order (only in embedded synchronization mode).

Allinteruts an easke yaTe gloalnterupt dmi is he gOR all hedal interrupts.

The DCMI interrupts are handled through the following registers:

DCMI_IER: read/write register allowing the interrupts to be generated when the corresponding event occurs DCMIRIS:read-nly register giving the current statusf the correspondig interrupt, befoemasking this interrupt with DCMIIER (each bit gives the status of the interrupt that can be enabled or disabled in DCIIER). . DCMI_MIS:read-only register providing the current masked status of the corresponding interrupt, depending on DCMI_IER and DCMI_RIS.

If an event occurs and the corresponding interrupt is enabled, the DCMI global interrupt is generated.

![](images/d46c090917db2f3e68f33c761e270f66fbdf4869eb79073b917c782a39a9093b.jpg)  
Figure 37. DCMI interrupts and registers

# 5.10

# Low-power modes

The STM32 power mode has a direct effect on the DCMI, which operates as follows over the different power modes:

In Run mode, the DCMI and all peripherals operate normally.   
In Sleep mode, the DCMI and all peripherals work normally, and generate interrupts to wake up the CPU.   
In Stop and Standby modes, the DCMI does not work.

For some STM32 devices, there are other low-power modes where the state of the DCMI varies from one to the other:

Low-power Run mode Low-power Sleep mode: interrupts from peripherals cause the device to exit this mode. Stop 0, Stop 1, Stop 2, Stop 3 modes: the content of peripheral registers is kept. Shutdown mode: the peripheral must be reinitialized when exiting Shutdown mode.

# The table below summarizes the DCMI operation in the different modes.

Table 7. DCMI operation in low-power modes   

<table><tr><td rowspan=1 colspan=1>Mode</td><td rowspan=1 colspan=1>DCMI operation</td></tr><tr><td rowspan=1 colspan=1>Run</td><td rowspan=4 colspan=1>Active</td></tr><tr><td rowspan=1 colspan=1>Low-power Run(1)</td></tr><tr><td rowspan=1 colspan=1>Sleep</td></tr><tr><td rowspan=1 colspan=1>Low-power Sleep(1)</td></tr><tr><td rowspan=1 colspan=1>Stop2)</td><td rowspan=7 colspan=1>Frozen</td></tr><tr><td rowspan=1 colspan=1>Stop O(3)</td></tr><tr><td rowspan=1 colspan=1>Stop 1(3)</td></tr><tr><td rowspan=1 colspan=1>Stop 2(3)</td></tr><tr><td rowspan=1 colspan=1>Stop 3(4)</td><td rowspan=1 colspan=1></td></tr><tr><td rowspan=1 colspan=1>Stop mode SVOS high(5)</td></tr><tr><td rowspan=1 colspan=1>Stop mode SVOS low(5)</td></tr><tr><td rowspan=1 colspan=1>Standby</td><td rowspan=2 colspan=1>Powered down</td></tr><tr><td rowspan=1 colspan=1>Shutdown(3)</td></tr></table>

1. Only for the STM32L496xx, STM32L4A6xx, and STM32L4+ devices. 2. Not available on the STM32N6 devices. 3. Only for the STM32L496xx, STM32L4A6xx, STM32L4+, and STM32U5 devices. 4. Only on the STM32U5 devices. 5. Only for the STM32N6 devices.

# 6 DCMI configuration

When selecting a camera module tointerface with STM32 MCUs, theuser must consier some parameters such as the pixel clock, the supported data format, and the resolutions.

o correctly implement the application, the user needs to perform the following configurations:

Configure the GPIOs.   
Configure the timings and the clocks.   
Configure the DCMI peripheral.   
Configure the DMA.   
Configure the camera module: Configure the I2C to allow the camera module configuration and control. Set parameters such as contrast, brightness, color effect, polarities, and data format.

Note:

It is recommended to reset the DCMI and the camera module before starting the configuration. The DCMI can be reset by setting the corresponding bit in the RCC_AHB2RSTR register, which resets the clock domains.

# 6.1

# GPIO configuration

Ti cngure he DCMI GIs (suchas ata ps, cnrol sigals s, cmcoguratn pins  t avoid any pin conflicts, it is recommended to use the STM32CubeMX configuration and initialization code generator.

Thanks to the STM32CubeMX, the user generates a project with ll the needed peripherals preconfigured.

Depending on the extended data mode chosen by configuring EDM bits in DCMI_CR register, the DCMI receives a 8-, 10-, 12-, or 14-bpp clock (DCMI_PIXCLK).

The user needs to configure:

11, 13, 15, or 17 GPIOs for the DCMI for the hardware synchronization only nine GPIOs (eight pins for data and one pin for DCMI_PIXCLK) for the embedded synchronization

The user nees  conigure alsohe , and in some cases he camea power supply n  the amea p supply source is the STM32 MCU).

# Enable interrupts

T bleu  CM iteruts,heru ablee CM global intrupt nhe NVIC c interrupt is then enabled separately by enabling its corresponding enable bit in the DCMIIER register:

Only four interrupts (IT_LINE, IT_FRAME, IT_OVR, and IT_DCMI_VSYNC) can be used in hardware synchronization mode.   
The five interrupts can be used in embedded synchronization mode.

Teus e whe ec itepth oe state of the flags.

# 6.2

# Clock and timing configuration

# System clock configuration (HCLK)

It is recommended to use the highest system clock to get the best performance. This recommendation applies be set at the highest allowed speed to get the best memory bandwidth.

# Examples:

. STM32F4x9xx devices: the maximum system speed is 180 MHz. If an external SDRAM is connected to the FMC, the maximum SDRAM clock is 90 MHz (HCLK/2). STM32F7 devices: the maximum system speed is 216 MHz. With this speed and HCLK/2 prescaler, the SDRAM speed exceeds the maximum allowed speed (see datasheets for more details). To get the maximum SDRAM, it is recommended to configure HCLK @ 200 MHz, then the SDRAM speed is set at 100 MHz.

The clock configurations providing the highest performance are the following:

For STM32F2x7 devices, HCLK @ 120 MHz and SRAM @ 60 MHz For STM32F407/417 devices, HCLK @ 168 MHz and SRAM @ 60 MHz For STM32L4x6 devices, HCLK @ 80 MHz and SRAM @ 40 MHz

# DCMI clock and timing configuration (DCMI_PIXCLK)

The DCMI piel clock configuration depends on the configuration  the pil clockf the camera modul. The uermust make urehat e pil coc as he sam configurationnhe M an he cameamodules.

DCMI_IXCL s an iput sinal or h DCMIused o iput data sampliTe user ele either he the falling edge for capturing data by configuring the PCKPOL bit in the DCMI_CR register.

As explained in Section 5., there are two types of synchronization: embedded and hardware. To select the desired synchronization mode for the application, the user needs to configure the ESS bit in DCMI_CR.

# 6.2.2.1

# DCMI clock configuration in hardware synchronization

The DCMI_HSYNC and DCMI_VSYNC signals are used. The configuration of these two signals is defined by selecting each signal active level (high or low) for the VSPOL and HSPOL bits in DCMI_CR.

# Note:

The user must make sure that DCMI_HSYNC and DCMI_VSYNC polarities are programmed according to the camera module configuration. In the hardware synchronization mode (ESS = 0 in DCMI_CR), the IT_VSYNC interrupt is generated (if enabled), even when CAPTURE = 0 in DCMI_CR. To reduce the frame capture rate even further, the IT_vSYNCinterrupt can be used o count the numberof frames between two captures, in conjunction with the snapshot mode. This is not allowed by the embedded synchronization mode.

# 6.2.2.2

# DCMI clock configuration in embedded synchronization

The line-startline-end andframe-startframe-end are determined bycodes ormarkers embedded within thedat fow The embedded synchronization codes are supportedonly or an 8-bit parallel data interface width. The synchronization codes must be programmed in the DCMI_ESCR register as defined in Figure 38.

Figure 38. DCMI_ESCR register bytes   

<table><tr><td rowspan=1 colspan=1>DCMI_ESCR</td><td rowspan=1 colspan=1>FEC</td><td rowspan=1 colspan=1>LEC</td><td rowspan=1 colspan=1>LSC</td><td rowspan=1 colspan=1>FSC</td></tr></table>

<table><tr><td>Bit number 31</td><td></td><td>24 23</td><td>16 |15</td><td></td><td>8 7</td><td>0</td></tr></table>

# FEC (frame-end code)

Themost snificant byte pecis heramen delmier.Tecameamodule sen a bit word cont OxF 0 00 XY wit Y = FEC cde,  nal theend   fram.e code s eiv s diat nFi

![](images/45b8468edbadf941d1be6b68496b63e976cd5497beedd897eeafa5e57d08812b.jpg)  
Figure 39. FEC structure

Be etif ECeCust  toCMRdicat valame reeptionfhe ECVYNCmust leared  zer ndicate ha  yncronization betwenm. VSYNC must remain at zero until the reception of the next frame-start code.

If FEC = 0xFF (the camera module sends 0xFF 00 00 FF), allthe unused codes are interpreted as frame-end codes. There are 253 values corresponding to the end-of-frame delimiter (0xFF000oFF and the 252 unused codes).

# LEC (line-end code)

T y  aroa 00 XY with XY = LEC code.

![](images/17aa2184ab139c02f898db03d88a9d37a8d1ab40b3e1085c3cefcecabf602ffa.jpg)  
Figure 40. LEC structure

# FSC (frame-start code)

yrar is 0xFF 00 00 XY with XY = FSC code.

![](images/b093e214408cbced312e29782705ba4ad72ba6e59efeec61194351b91a484fdb.jpg)  
Figure 41. FSC structure

# LSC (line-start code)

T arara 0xFF 00 00 XY with XY = LSC code.

I L=F  o r eM of an LSC code after an FEC code as an FSC code occurrence.

![](images/4d37ae42dc3525ee5b7fab62b3b09fdd6efce4b953a41e4148119e0d81062b15.jpg)  
Figure 42. LSC structure

In this embedded synchronization mode, HSPOL and VSPOL bits are ignored. While the DCMI receives data (CAPTURE = 1 in DCMI_CR), the user can monitor the data flow to know if it is an active line/frame or a synchronization between lines/frames, by reading VSYNC and HSYNC in DCMI_SR. If ERR_IE = 1 in DCMI_IER, an interrupt is generated each time an error occurs (such as embedded synchronization characters not received in the correct order).

![](images/4baae87ab830dec27399b064590a9fa5233508f0263db62c77124f889119ad0a.jpg)  
Figure 43 shows a frame received in embedded synchronization mode.   
Figure 43. Frame structure in embedded synchronization mode

# 6.3

# DCMI configuration

T M cguran alls he  electe aptueo eat at,heg resolution.

# 6.3.1

# Capture mode selectior

The user can capture an image or a video by selecting one of the following modes:

The continuous grab mode to capture frames (images) continuously The snapshot mode to capture a single frame

The eivtapshontiabodanerheemoymebuyheDMA.   
The buffer location and mode (linear or circular buffer) are controlled through the system DMA.

# 6.3.2 Data format selection

The DCMI allows the reception of compressed data (JPEG) or many uncompressed data formats (such as monochrome, RGB, or YCbCr). For more details, refer to Section 5.6.

# 6.3.3 Image resolution and size

The DCMl allows the reception  a wide rangef resolutions (low, medium, high) and image izes, since the depeneageeolun  atratTeAensureeransn he plac of the received images in the memory frame buffer.

e a  .e  abl select a rectangular window from the received image (see Section 5.7).

# Note:

The DCMI configuration registers must be programmed correctly before enabling the ENABLE bit in DCMI_CR. The DMA controller and all DCMI configuration registers must be programmed correctly before enabling the CAPTURE bit in DCMI_CR.

# 6.4

# DMA configuration

The DMA configuration is a crucial step to ensure the success of the application.

As mentioned in Section 3.2, the DMA2 ensures the transfer from the DCMI to the memory (internal SRAM or external SRAM/SDRAM) for all STM32 devices embedding the DCMI.

For the STM32H7 and SMT32L4+ devices, the DMA1 can also access the AHB2 peripherals and ensures the ransfer of the received data from the DcMl to the memory frame buffer.

For the STM32U5 and STM32N6 devices, the GPDMA1 ensures the transfer from the DCMI to the memory.   
For the STM32H5 devices, the GPDMA1 and the GPDMA2 ensure the transfer from the DCMI to the memory.

# DMA configuration for DCMI-to-memory transfers

The transfer direction must be peripheral-to-memory by configuring:

DIR bits in DMA_SxCR for the STM32F2, STM32F4, STM32F7, and STM32H7 devices DIR bits in DMA_CCRx for the STM32L4x6 and STM32L4+ devices SWREQ = 0 and REQSEL[6:0] in GPDMA_CxTR2 for the STM32U5 and STM32H5

he source address (DCMI data register address) must be written:

In DMA_SxPAR for the STM32F2, STM32F4, STM32F7, and STM32H7 devices In DMA_CPARx for the STM32L4x6 and STM32L4+ devices In GPDMA_CxSAR for the STM32U5, STM32H5, and STM32N6 devices

The destination address (frame buffer address in internal SRAM or external SRAM/SDRAM) must be written:

In DMA_SxMAR for the STM32F2, STM32F4, STM32F7, and STM32H7 device: In DMA_CMARx for the STM32L4x6 and STM32L4+ devices In GPDMA_CxDAR for the STM32U5, STM32H5, and STM32N6 devices

n aA wai DCMI. The relevant stream and channel must be configured. For more details, refer to Section 6.4.3.

S DMAqus eateach tme he DCMI at egise i hedataneomDCM must have a 32-bit width. Data is transferred:

To the DMA2 (or the DMA1 for the STM32H7 and STM32L4+ devices) for ll STM32 except for the   
STM32U5, STM32H5, and STM32N6   
To the GPDMA1 for the STM32U5, STM32H5, and STM32N6 devices   
To the GPDMA2 for the STM32H5 devices

The peripheral data width must be 32-bit words. It is programmed:

By PSIZE bits in DMA_SxCR for the STM32F2, STM32F4, STM32F7, and STM32H7 devices By PSIZE bits in DMA_CCRx register for the STM32L4x6 and STM32L4+ devices By DDW_LOG2 and DBL_1 in GPDMA_CxTR1 for the STM32U5, STM32H5, and STM32N6 devices

To 1 to 65535 (see Section 6.4.4 for more details):

In DMA_SxNDTR for the STM32F2, STM32F4, STM32F7, and STM32H7 devices In DMA_CNDTRx for the STM32L4x6 and STM32L4+ devices In GPDMA_CxBr1 for the STM32U5, STM32H5, and STM32N6 devices

The DMA operates in one of the following modes:

Direct mode: each word received from the DCMl is transferred to the memory frame buffer. FIFO mode: the DMA uses its internal FIFO to ensure burst transfers (more than one word from the DM FIFO to the memory destination).

For more details on the DMA internal FIFO, refer to Section 6.4.5.

Figure 44 shows the DMA2 (or the DMA1 for STM32H7 and STM32L4+ devices, the GPDMA1 for the STM32U5, and STM32N6 devices, the GPDMA1 or the GPDMA2 for the STM32H5 devices) operation in peripheral-tomemory mode, except for the STM32L496xx and STM32L4A6xx devices. The DMA2 in these devices has only one port.

![](images/9e7aa0d05f71a1a89662c776d7dfd45562a17f90ba3ef31f91ca2bb97f02b1c3.jpg)  
Figure 44. Data transfer through the DMA

# 6.4.2

# DMA configuration versus image size and capture mode

T DMA mus guai  loretoln)ept:

In snapshot mode, the DMA must ensure the transfer of one frame (image) from the DCMI to the desired memory:

If the image size in words does not exceed 65535, the stream can be configured in normal mode (see Section 6.4.6).   
If the image size in words is between 65535 and 131070, the stream can be configured in doublebuffer mode (see Section 6.4.8).   
If the image size in words exceeds 131070, the stream cannot be configured in double-buffer mode (see Section 6.4.9).

In continuous mode: the DMA must ensure the transfer of successive frames (images) from the DCMI to tdeimmoyc ti e A nihes eranse ram  arteansext frame:

If one image size in words does not exceed 65535, the stream can be configured in circular mode (see Section 6.4.7).   
If one image size in words is between 65535 and 131070, the stream can be configured in doublebuffer mode (see Section 6.4.8).   
If one image size in words exceeds 131070, the stream cannot be configured in double-buffer mode (see Section 6.4.9).

# 6.4.3

# DCMI channel and stream configuration

The user must also configure the corresponding DMA2 (or the DMA1 for the STM32H7 and STM32L4+ devices, the GPDMA1 for the STM32U5 and STM32N6 devices, the GPDMA1 and GPDMA2 for the STM32H5 devices) stream and channel to ensure the DMA acknowledgment each time the DCMI data register is fulfilled.

The tables below summarize the DMA stream and channels that enable the DMA request from the DCMI.

Table 8. DMA stream selection across STM32 devices   

<table><tr><td rowspan=1 colspan=1>STM32</td><td rowspan=1 colspan=1>DMA stream</td><td rowspan=1 colspan=1>Channel</td></tr><tr><td rowspan=1 colspan=1>STM32F2</td><td rowspan=3 colspan=1>Stream 1 and stream 7</td><td rowspan=3 colspan=1>Channel 1</td></tr><tr><td rowspan=1 colspan=1>STM32F4</td></tr><tr><td rowspan=1 colspan=1>STM32F7</td></tr><tr><td rowspan=1 colspan=1>STM32H7</td><td rowspan=1 colspan=1>Stream 0 to stream 7</td><td rowspan=1 colspan=1>Multiplexer 1 request 75</td></tr><tr><td rowspan=2 colspan=1>STM32L4</td><td rowspan=1 colspan=1>Stream 0</td><td rowspan=1 colspan=1>Channel 6</td></tr><tr><td rowspan=1 colspan=1>Stream 4</td><td rowspan=1 colspan=1>Channel 5</td></tr></table>

Table 9. DMA stream selection across STM32 devices   

<table><tr><td rowspan=1 colspan=2>STM32</td><td rowspan=1 colspan=1>DMA channel</td><td rowspan=1 colspan=1>Request</td></tr><tr><td rowspan=2 colspan=1>STM32L4+</td><td rowspan=1 colspan=1>STM32L4Rxxx and STM32L4Sxxx</td><td rowspan=1 colspan=1>Channel 1 to</td><td rowspan=1 colspan=1>DMA request multiplexer 90</td></tr><tr><td rowspan=1 colspan=1>STM32L4P5xx and STM32L4Q5xx</td><td rowspan=1 colspan=1>channel 7</td><td rowspan=1 colspan=1>DMA request multiplexer 91</td></tr><tr><td rowspan=1 colspan=2>STM32U5</td><td rowspan=1 colspan=1>Channel 0 tochannel 5</td><td rowspan=1 colspan=1>GPDMA1 request 86</td></tr><tr><td rowspan=1 colspan=2>STM32H5</td><td rowspan=1 colspan=1>Channel 0 tohannel 7</td><td rowspan=1 colspan=1>GPDMA1/2 request 108</td></tr><tr><td rowspan=1 colspan=2>STM32N6</td><td rowspan=1 colspan=1>Channel 0 tochanneel 15</td><td rowspan=1 colspan=1>GPDMA1 request 140</td></tr></table>

# Note:

See the referencemanual for a step-by-step descriptionof the stream andchannel configuration procedure.

# 6.4.4

# DMA_SxNDTR/DMA_CNDTRx/GPDMA_CxBR1 register

The total number of words to transfer from the DCMI to the memory is programmed in this register (see Section 6.4.1).

When the DMA start he transr fom he DCMI  theemory tenumber items decreass fromh programmedvalueuntil the end of the transfer reaching zeroordisabling the stream by software before the number of data remaining reaches zero).

T bl elogivheumbe ycreondige prorae alueandh iheral a (PSIZE bitfield).

Table 10. Maximum number of bytes transferred during one DMA transfer   

<table><tr><td rowspan=1 colspan=1>Programmed value in the register</td><td rowspan=1 colspan=1>Peripheral size</td><td rowspan=1 colspan=1>Number of bytes</td></tr><tr><td rowspan=1 colspan=1>65535</td><td rowspan=2 colspan=1>Words</td><td rowspan=1 colspan=1>262140</td></tr><tr><td rowspan=1 colspan=1>0 &lt; N &lt; 35535</td><td rowspan=1 colspan=1>4*N</td></tr></table>

Note:

To avoid data corruption, this programmed value must be a multiple of MSIZE or PSIZE.

# 6.4.5

# FIFO and burst transfer configuration

TMA p e aner wi  iou ablig he orFFOWhenhe IFOsablehe data width (programmed in SIZE) can differ from the destination data width (programmed inMSZ. In this case, the user must pay attention to adapt the address to write:

In DMA_SxPAR and DMA_SxM0AR (and DMA_SxM1AR in case of double-buffer mode configuration) to the data width programmed in PSIZE and MSIZE of DMA_SxCR for all STM32 except the STM32L4/L4+, STM32U5, STM32H5, and STM32N6 devices   
In DMA_CPARx and DMA_CMARx to the data width programmed in PSIZE and MSIZE of DMA_CCRx for the STM32L4 and STM32L4+ devices   
In GPDMA_CxSAR and GPDMA_CxDAR to the data width programmed with a burst length by SBL_1[5:0] (respectively DBL_1[5:0]), and with a data width defined by SDW_LOG2[1:0] (respectively   
DDW_LOG2[1:0]) in GPDMA_CxTR1 for the STM32U5, STM32H5, and STM32N6 devices

For a better performance, it is recommended to use the FIFO. When the FIFO mode is enabled, the user can ueBR ak heMA p burs anr up or)omeal O the destination memory, which guarantees better performance.

# Normal mode for low resolution in snapshot capture

Loeoluage h s havi iit word) ls tha 6. Inapsot mode,hel mode can be used to ensure the transfer of low-resolution frames (see Table 10).

The maximum number f pixels depends on the bit depth of the image (number f bytes per pixel The DCMI supports two possible bit depths:

1 byte per pixel in monochrome or Y only format   
2 bytes per pixel in case of RGB565 or YCbCr format

The table below summarizes the maximum image resolution that can be transferred using the normal mode.

Table 11. Maximum image resolution in normal mode   

<table><tr><td rowspan=1 colspan=1>Item</td><td rowspan=1 colspan=1>Max number of bytes</td><td rowspan=1 colspan=1>Bit depth (byte/pixel)</td><td rowspan=1 colspan=1>Max number of pixels</td><td rowspan=1 colspan=1>Max resolution</td></tr><tr><td rowspan=2 colspan=1>Word</td><td rowspan=2 colspan=1>262140</td><td rowspan=1 colspan=1>1</td><td rowspan=1 colspan=1>262140</td><td rowspan=1 colspan=1>720x364</td></tr><tr><td rowspan=1 colspan=1>2</td><td rowspan=1 colspan=1>131070</td><td rowspan=1 colspan=1>480x272</td></tr></table>

# 6.4.7

# Circular mode for low resolution in continuous capture

T is less than 65535. The initial size value is programmed:

In DMA_SxNDTR for the STM32F2, STM32F4, STM32F7, and STM32H7 devices In DMA_CNDTRx for the STM32L4x6 and STM32L4+ devices In GPDMA_CxBr1 for the STM32U5, STM32H5, and STM32N6 devices

Eatnbeadeenti acheezet woruaticll ensures the transfer of the next frame.

The resolutions listed in Table 11 are also valid for the low resolution in continuous mode.

Figure 5 shows the DMASxNDTR value and the frame buffer pointermodifiations during a DMA transerand between two successive DMA transfers.

![](images/b04647a56cd4aa11f045c8734f01c1fbd15095103d5177dcfeb4dfeb02cb6428.jpg)  
Figure 45. Frame buffer and DMA_SxNDTR register in circular mode

# 6.4.8

# Double-buffer mode for medium resolutions (snapshot or continuous capture)

# Note:

This mode is not available for STM32L4A6xx and STM32L496xx devices.

Medium resolution images are the ones with a size (in 32-bit words) between 65536 and 131070. When the louble-buffer mode is enabled, the circular mode is automatically enabled.

I ag  or) heau zet apsottio thedouble-bufrmode must e n apshot contios moe In thicase, he umbe  pi p faallowe is doubl ereeivdataestorin toburach buffermaxu  n t words) is 6535 (the maximum frame ize s 31070 words or 524280 bytes). The images sizes and resolutions allowed to be received by the DCMI and transferred by the DMA are then doubled.

Table 12. Maximum image resolution in double-buffer mode   

<table><tr><td rowspan=1 colspan=1>Item</td><td rowspan=1 colspan=1>Max number ofbytes</td><td rowspan=1 colspan=1>Bit depth (byte/pixel)</td><td rowspan=1 colspan=1>programmedvalue in theregister</td><td rowspan=1 colspan=1>Number of pixels</td><td rowspan=1 colspan=1>Max resolution</td></tr><tr><td rowspan=4 colspan=1>Word</td><td rowspan=4 colspan=1>524280</td><td rowspan=2 colspan=1>1</td><td rowspan=1 colspan=1>65535</td><td rowspan=1 colspan=1>524280</td><td rowspan=2 colspan=1>960x544</td></tr><tr><td rowspan=1 colspan=1>0 &lt; N &lt; 65535</td><td rowspan=1 colspan=1>8*N</td></tr><tr><td rowspan=2 colspan=1>2</td><td rowspan=1 colspan=1>65535</td><td rowspan=1 colspan=1>262140</td><td rowspan=2 colspan=1>720x364</td></tr><tr><td rowspan=1 colspan=1>0 &lt; N&lt; 65535</td><td rowspan=1 colspan=1>4*N</td></tr></table>

I transaction:

• Ineau filled (at this level, the register is reinitialized to the programmed value, and the DMA pointer swites to the econ rame buffr),heat is transerd he eod buff.hetotal rame ie  wori divided by two and programmed into the register. The image is stored to two buffers with the same size. Incntinuous mode,each time e frame (image) is receivedand stored o the two buffers.As the rcular m  nable he gister  renitialize othe proramed valuetotal ame izedivided by two, a the DMA pointer switches to the first frame buffer to receive the next frame.

Figure 46 shows the two pointers and the DMA_SxNDTR value modifications during the DMA transfers.

![](images/170aa6ed9eed348c5b3db67a9b30b4b13d35c3313700f963a21d203838c4b989.jpg)  
Figure 46. Frame buffer and DMA_SxNDTR register in double-buffer mode

# 6.4.9

# DMA configuration for higher resolutions

When thenumber  word in e frame mage in sapshot or continuous modeexces 070,and when he ubluns of the received data.

# Note:

This section highlights only the DMA operation in case of high resolution. An example is developed and described using this DMA configuration in Section 8.3.6: Resolution capture (YCbCr data format).

The STM32F2, STM32F4, STM32F7, STM32H7, and STM32L4+ devices embed a very important feature in double-buer ode: he possibility toupdate he programme adress or theAHBmemory port on-thely in DMA_SxMOAR or DMA_SxM1AR) when the stream is enabled. The folowing conditions must be respected:

• When CT is cleared to zero in DMA_SxCR (current target memory is memory 0), the DMA_SxM1AR rn rAtti wh gise whi=gatea r the stream is automatically disabled. When CT is set to one in DMA_SxCR (current target memory is memory 1), the DMA_SxM0AR register can be written. Atempting to write to this register while CT = 0 generates an error flag (TEIF), and the stream is automatically disabled.

To avoid any error condition, i is advised to change the programmed address as soon as the TCF flag is asserted. At this point, the targeted memory must have changed from memory 0 to memory 1 (or from 1 to 0), depending on the CT bit value in DMA_SxCR.

# Note:

For alltheothermodes than thedouble-bufferne thememory address gisters arewrie-protected as son as the stream is enabled.

The DMA allows then the management of more than two buffers:

In the first cycle, while the DMA uses the buffer 0 addressed by pointer 0 (memory 0 address in   
DMA_SxM0AR), the buffer 1 is addressed by pointer 1 (memory 1 address in DMA_SxM1AR).   
In the second cycle, while DMA uses the buffer 1 addressed by pointer 1, the buffer 0 address can be changed, and the frame buffer 2 can be addressed by pointer 0.   
In the second cycle while the DA isusing he buffr adresd by pointer , heframe bufadress can be changed, and the buffer 3 can be addressed by pointer 1.

DMA_SxM0AR and DMA_SxM1AR can then be used to address many buffers, ensuring the transfer of high resolution images.

# Note:

Tplheh eatsivehequal fWh capturing high resolution images, the user must secure that the memory destination has a sufficient size.

Ele I hax10hea  wor biz ual buf w must then be divided into 16 frame buffers, with each frame buffersize equal to0960 (lower than 655).

Figure 47 illustrates the DMA_SxM0AR and DMA_SxM1AR update during the DMA transfer:

![](images/594d1ed15dbb6b12c6aa0edf1fb09a016ed5ad3fe7bd76d413ce315bea77f56d.jpg)  
Figure 47. DMA operation in high resolution case

<table><tr><td rowspan=1 colspan=1>CT=0</td><td rowspan=1 colspan=1>Buffer 0=Memory </td><td rowspan=1 colspan=1>Buffer 1=Memory</td><td rowspan=1 colspan=1>Buffer 2</td><td rowspan=1 colspan=1>Buffer 3</td><td rowspan=1 colspan=1></td><td rowspan=1 colspan=1>Buffer 14</td><td rowspan=1 colspan=1>Buffer 15</td></tr></table>

# Cycle 1

DMA_ SxMOAR DMA_SxM1AR

Address 14 Address 15

<table><tr><td rowspan=1 colspan=1>CT=1</td><td rowspan=1 colspan=1>Buffer 0</td><td rowspan=1 colspan=1>Buffer 1=Memory 1</td><td rowspan=1 colspan=1>Buffer 2=Memory 0</td><td rowspan=1 colspan=1>Buffer 3</td><td rowspan=1 colspan=1></td><td rowspan=1 colspan=1>Buffer 14</td><td rowspan=1 colspan=1>Buffer 15</td></tr></table>

Cycle 2

DMA_ SxMOAR DMA_SxM1AR

Address 0 Address 1 Address 2 Address

Address 14 Address 15

<table><tr><td>CT=0</td><td>Buffer 0</td><td>Buffer 1</td><td>Buffer 2 = Memory 0</td><td>Buffer 3 = Memory 1</td><td></td><td>Buffer 14</td><td>Buffer 15</td></tr></table>

# Cycle 14

# DMA_SxM0AR

# DMA_SxM1AR

<table><tr><td rowspan="2"></td><td>Address 0</td><td>Address 1</td><td>Address 2 Address 3</td><td></td><td></td><td></td><td>Address 14 Address 15</td></tr><tr><td></td><td>Buffer 1</td><td>Buffer 2</td><td>Buffer 3</td><td></td><td>Buffer 14</td><td>Buffer 15</td></tr><tr><td>CT=0</td><td>Buffer 0</td><td></td><td></td><td></td><td></td><td>= Memory 0 Memory 1</td><td>=</td></tr></table>

Current buffer DMA destination

# 6.5

# Camera module configuration

The following steps allow a correct configuration f the camera module reer also to the camera module datasheet):

uual communication, mostly |2C).

Apply hardware reset on the camera module.

3Initialize the camera module:

Configure the image resolution.   
Configure the contrast and the brightness.   
Configure the white balance of the camera (such as black and white, white negative, white normal).   
Select the camera interface (some camera modules have serial and parallel interface).   
Select the synchronization mode if the camera module supports more than one.   
Configure the clock signals frequencies.   
Select the output data format.

# Power consumption and performance

# 7.1 Power consumption

Inrr avemorenergy when hepliation low-power moderecmende  put he module in low-power mode before the STM32 entry in low-power mode.

Putting camera module in low-power mode ensures a considerable gain in power consumption.

Example for OV9655 CMOS sensor:

In active mode, the operating current is 20 mA.   
In standby mode, the current requirements drop to1mA in case of 2C-nitiated Standby mode (the interal circit activiy isspende buthe clockisot halte, nd n case pi-nate Stanye evlcaloe datasheet.

# 7.2 Performance

For all STM32 MCUs, the number of bytes to be transferred at each pixel clock depends on the extended data mode:

When the DCMl is configured to receive 8-bit data, the camera interface takes four pixel clock cycles to capture a 32-bit data word.   
When theDCMl isconigured to receivebit data, the camera interace takes two pixel co cycles to capture a 32-bit data word.

The table below summarizes the maximum data flow depending on the data width configuration.

alucaCbile.

Table 13. Maximum data flow at maximum DCMI_PIXCLK   

<table><tr><td rowspan=2 colspan=1>STM32</td><td rowspan=1 colspan=4>Data flow (max Mbyte/s) in extended data mode</td></tr><tr><td rowspan=1 colspan=1>8-bit1 byte per PICXCLK</td><td rowspan=1 colspan=1>10-bit1.25 bytesper PICXCLK</td><td rowspan=1 colspan=1>12-bit1.5 btesper PICXCLK</td><td rowspan=1 colspan=1>14-bit1.75 bytesper PICXCLK</td></tr><tr><td rowspan=1 colspan=1>STM32F2</td><td rowspan=1 colspan=1>46.875</td><td rowspan=1 colspan=1>58.594</td><td rowspan=1 colspan=1>70.312</td><td rowspan=1 colspan=1>82.031</td></tr><tr><td rowspan=1 colspan=1>STM32F4</td><td rowspan=2 colspan=1>52.734</td><td rowspan=2 colspan=1>65.918</td><td rowspan=2 colspan=1>79.101</td><td rowspan=2 colspan=1>92.285</td></tr><tr><td rowspan=1 colspan=1>STM32F7</td></tr><tr><td rowspan=1 colspan=1>STM32H723/733, STM32H743/753,STM32H747/757, STM32H745/755,STM32H742, STM32H750, STM32H7A3/7B3</td><td rowspan=1 colspan=1>78.125</td><td rowspan=1 colspan=1>97.656</td><td rowspan=1 colspan=1>117.187</td><td rowspan=1 colspan=1>136.718</td></tr><tr><td rowspan=1 colspan=1>STM32H725/735, STM32H730</td><td rowspan=1 colspan=1>107.422</td><td rowspan=1 colspan=1>134.277</td><td rowspan=1 colspan=1>161.133</td><td rowspan=1 colspan=1>187.988</td></tr><tr><td rowspan=1 colspan=1>STM32L4</td><td rowspan=1 colspan=1>31.25</td><td rowspan=1 colspan=1>39.062</td><td rowspan=1 colspan=1>46.875</td><td rowspan=1 colspan=1>54.687</td></tr><tr><td rowspan=1 colspan=1>STM32L4+</td><td rowspan=1 colspan=1>46.875</td><td rowspan=1 colspan=1>58.594</td><td rowspan=1 colspan=1>70.312</td><td rowspan=1 colspan=1>82.031</td></tr><tr><td rowspan=1 colspan=1>STM32U5</td><td rowspan=1 colspan=1>62.5</td><td rowspan=1 colspan=1>78.125</td><td rowspan=1 colspan=1>93.75</td><td rowspan=1 colspan=1>109.375</td></tr><tr><td rowspan=1 colspan=1>STM32H5</td><td rowspan=2 colspan=1>93.75</td><td rowspan=2 colspan=1>117.187</td><td rowspan=2 colspan=1>140.625</td><td rowspan=2 colspan=1>164.062</td></tr><tr><td rowspan=1 colspan=1>STM32N6</td></tr></table>

In some applications, the DMA2 (or the DMA1 for the STM32H7 and STM32L4+; the GPDMA1 for the STM32U5 and STM32N6; and the GPDMA1 and GPDMA2 for the STM32H5) is configured to serve other requests in ius consider the performance impact when the DMA serves other streams in parallel with the DCMI.

For better performance, when using the DCMl in parall with other peripherals having requests that can be coneced toeither DMA1or DMA2, or to GPDMA1 and GPDMA2, it is better t configure these streams t be served by the DMA/GPDMA that is not serving the DCMI.

Theuser must mak ure that he CM supports e piel clock configur  hecameamodule se v the overrun.

It is recommended to use the highest system speed HCLK for better performance. However, the user must cer sl  epl  setalv and to ensure the successful operation of the application.

The DCM is ot theonly AHB peripheral but there emany other peripherals.The DMA is ot he nly maser that can access the AHB peripherals. Using many AHB peripherals or other masters accessing the AHB peripherals leads to a concurrency on the AHB: the user must consider its impact on performance.

# 8 DCMI application examples

This section details how to use the DCMl, and provides step-by-step implementation examples .

# I DCMI use cases

There are several imaging aplications that can be implemented using the DCMI and other STM32 peripherals Here below some application examples:

• Machine vision Toys Biometry Security and video surveillance Door phone and home automation Industrial monitoring systems and automated inspection System control Access control systems Bar-code scanning Video conferencing Drones Real-time video streaming and battery-powered video camer

Figure 48 provides examples of applications based on an STM32 MCU. These applications allow the user to:

Capture data   
Store it to internal or external memories   
Display it   
Share it via the internet   
Communicate with human beings

![](images/57f42d1e357d16b09b6687f025be2adf110f52b1e719ca5b73265872b7de8092.jpg)  
Figure 48. STM32 DCMI application example

# 8.2

# STM32Cube examples

The STM32CubeF2, STM32CubeF4, STM32CubeF7, STM32CubeH7, STM32CubeL4, and STM32CubeU5 MCU Packages offer a large set of examples implemented and tested on the corresponding boards.

The table below gives an overview f the DCMI examples and applications across various STM32Cube. Allthee p resolutions: QQVGA 160x120, QVGA 320x240, 480x272, VGA 640x480.

Table 14. STM32Cube DCMI examples   

<table><tr><td rowspan=1 colspan=1>MCU Package</td><td rowspan=1 colspan=1>Project name</td><td rowspan=1 colspan=1>Board</td></tr><tr><td rowspan=3 colspan=1>STM32CubeF2</td><td rowspan=1 colspan=1>DCMI_CaptureMode</td><td rowspan=3 colspan=1>STM3220G-EVAL, STM3221G-EVAL</td></tr><tr><td rowspan=1 colspan=1>SnapshotMode</td></tr><tr><td rowspan=1 colspan=1>Camera_To_USBDisk</td></tr><tr><td rowspan=3 colspan=1>STM32CubeF4</td><td rowspan=1 colspan=1>DCMI_CaptureMode</td><td rowspan=3 colspan=1>STM32446E-EVAL, STM32429I-EVAL1,STM32469I-EVAL, STM3240G-EVAL</td></tr><tr><td rowspan=1 colspan=1>SnapshotMode</td></tr><tr><td rowspan=1 colspan=1>Camera_To_USBDisk</td></tr><tr><td rowspan=4 colspan=1>STM32CubeF7</td><td rowspan=1 colspan=1>DCMI_CaptureMode</td><td rowspan=3 colspan=1>STM32756G-EVAL, STM32F769I-EVAL</td></tr><tr><td rowspan=1 colspan=1>SnapshotMode</td></tr><tr><td rowspan=1 colspan=1>Camera_To_USBDisk</td></tr><tr><td rowspan=1 colspan=1>Camera</td><td rowspan=1 colspan=1>STM32F7508-DISCOVERY</td></tr><tr><td rowspan=2 colspan=1>STM32CubeH7</td><td rowspan=1 colspan=1>DCMI_CaptureMode</td><td rowspan=2 colspan=1>STM32H747I-DISCOVERY</td></tr><tr><td rowspan=1 colspan=1>SnapshotMode</td></tr><tr><td rowspan=3 colspan=1>STM32CubeL4</td><td rowspan=1 colspan=1>DCMI_CaptureMode</td><td rowspan=1 colspan=1>32L496GDISCOVERY, 32L4R9IDISCOVERY</td></tr><tr><td rowspan=1 colspan=1>SnapshotMode</td><td rowspan=2 colspan=1>32L496GDISCOVERY</td></tr><tr><td rowspan=1 colspan=1>DCMI_Preview</td></tr><tr><td rowspan=1 colspan=1>STM32CubeU5</td><td rowspan=1 colspan=1>DCMI_ContinousCap_EmbeddedSynchMode</td><td rowspan=1 colspan=1>STM32U575I-EVAL</td></tr></table>

# 8.3

# DCMI examples based on STM32CubeMX

This section details the following typical examples of DCMl use:

. Capture and display of RGB data Data captured in RGB565 format with QVGA (320 × 240) resolution, stored in the SDRAM, and displayed on the LCD-TFT Capture of YCbCr data Data captured in YCbCr format with QVGA (320 × 240) resolution and stored in the SDRAM Capture of Y-only data DCMI configured to receive Y-only data to be stored in the SDRAM Resolution capture (YCbCr data format) Data captured in YCbCr format with a 1280 x 1024 resolution and stored in the SDRAM Capture of JPEG data Data captured in JPEG format, and stored in the SDRAM

All these examples have been implemented on 32F746GDISCOVERY using STM32F4DIS-CAM (OV9655 CMOS sensor), except the capture of JPEG data that was implemented on STM324x9I-EVAL (OV2640 CMOS sensor).

As illustrated in Figure 49, the application consists of three main steps:

Import the received data from the DCMI to the DMA (to be stored in FIFO temporarily) through its peripheral port.   
2Transfer the data from the FIFO to the SDRAM.   
Iport dat from he DRAM to be isplaye on he LCD-FTonly for heGB dat formatFor eYCb JPEG data format, the user must convert the received data to RGB to be displayed.

![](images/93179d54aba68b9c0e3982017588ce4104df12c36aa7cfdd3a9c32e8b07968eb.jpg)  
Figure 49. Data path in capture and display application

For these examples, the user nees t configure he DCMI, he DMA2, he LTDC (or the RGB data captue and display example), and the SDRAM.

The five examples described in the next sections have some common configurations based on STM32CubeMX:

GPIO configuration DMA configuration Clock configuration

The following specific configurations are needed for Y-only and JPEG capture examples:

DCMI configuration Camera module configuration

The next sections provide the hardware description, the common configuration using STM32CubeMX, and the common modifications that have to be added to the STM32CubeMX generated project.

# 8.3.1 Hardware description

All examples except the JPEG capture, were implemented on 32F746GDISCOVERY using the camera board STM32F4DIS-CAM, as shown in Figure 50.

![](images/69d6fcb9b69711172851fbe9f9fbf588bab2817f2e2471dc3fc8b21681bba13a.jpg)  
Figure 50. 32F746GDISCOVERY and STM32F4DIS-CAM interconnection

The STM32F4DIS-CAM board includes an Omnivision CMOS sensor (ov9655), 1.3 megapixels. The resolution can reach 1280x1024. This camera module is connected to the DCMI via a 30-pin FFC.

The 32F746GDISCOVERY board features a 4.3-inch color LCD-TFT with capacitive touch screen that is used in the first example to display the captured images.

As shown in Figure 51, the camera module is connected to the STM32F7 through:

Control signals DCMI_PIXCLK, DCMI_VSYNC, DCMI_HSYNC Image data signals DCMI_D[0..7]

Additional signals are provided to the camera module through the 30-pin FFC:

Power supply signals (DCMI_PWR_EN)   
Clock for the camera module (Camera_CLK)   
Configuration signals (I2C)   
Reset signal (DCMI_NRST)

Fo more details on these signals, efer t Section .. Camera module interconnect (paral inteace).

The camera clock is provided to the camera module through the CameraCLK pin, by the NZ2520SB crystal clock oscilator (X1) embeded on the 32F746GDiSCOVERY board Thefrequency f the camera clock  equal to 24 MHz.

The DCMI reset pin (DCMI_NRST) used to reset the camera module is connected to the global MCU reset pin (NRST).

![](images/735b27ae0a7cefd6c80378cdf0425d6cda4cc98e518ab7cd93a8402b66426716.jpg)  
Figure 51. Camera connector on 32F746GDISCOVERY

For more details on the 32F746GDISCOVERY board, refer to the user manual Discovery kit for STM32F7 series with STM32F746NG MCU (UM1907) available on the STMicroelectronics website.

![](images/02c89aa4b6814d0fd0abe710fa3bfe44c927c7609402e0f8fc4ce0de6d461b0e.jpg)  
Figure 52 details the camera module connector implemented on STM32F4DIS-CAM.   
Figure 52. Camera connector on STM32F4DIS-CAM

# 8.3.2

# Configuration of common examples

When starting with STM32CubeMX, the first step is to configure the project location and the correspoding toolchain or IDE (menu Project/Settings).

# 8.3.2.1

# STM32CubeMX - Configuration of DCMI GPIOs

Select the DCMI and choose Slave 8 bits External Synchro"in the Pinout &configuration multimedia tbto configure the DCMl in slave 8-bit external (hardware) synchronization.

![](images/56676b27dd92c0378643f49870927cbbf551c1bee3b398fb37cdcab98380e361.jpg)  
Figure 53. STM32CubeMX - DCMI synchronization mode selection

Ir selecting e hardware configuration (Slave 8 bits External ynchroorexample), the used GOsdo nt match with thehardware, the user can change the desired Gs, an configure thealternate ction directly on the pin.

Another method consists of configuring manually the GPlO pins by selecting the right alternate function for each of them. For more details on the GPlOs that must be configured, refer to Figure 55. After this step, 11 pins must be highlighted in green (D[0.7], DCMI_VSYNC, DCMI_HSYNC, and DCMI_PIXCLK).

When the DCMI configuration window appears, select the GPIO Settings tab.

![](images/61fe30c15c57ad128724082c1aa630dff1d7b9d69cee5369df40f80662971db3.jpg)  
Figure 54. STM32CubeMX - GPIO settings selection

# Select all the DCMI pins.

Figure 55. STM32CubeMX - DCMI pin selection   

<table><tr><td rowspan=1 colspan=1>Pin Name</td><td rowspan=1 colspan=1>Signal on Pin</td><td rowspan=1 colspan=1>GPIO output I...</td><td rowspan=1 colspan=1>GPIO mode</td><td rowspan=1 colspan=1>GPIO Pull-up...</td><td rowspan=1 colspan=1>Maximum out...</td><td rowspan=1 colspan=1>User Label</td><td rowspan=1 colspan=1>Modified</td></tr><tr><td rowspan=1 colspan=1>PA4</td><td rowspan=1 colspan=1>DCMI_HSYNC</td><td rowspan=1 colspan=1>n/a</td><td rowspan=1 colspan=1>Alternate Fun...</td><td rowspan=1 colspan=1>No pull-up an..</td><td rowspan=1 colspan=1>Low</td><td rowspan=1 colspan=1>DCMI_HSYNC</td><td rowspan=1 colspan=1>V</td></tr><tr><td rowspan=1 colspan=1>PA6</td><td rowspan=1 colspan=1>DCMI_PIxCLK</td><td rowspan=1 colspan=1>n/a</td><td rowspan=1 colspan=1>Alternate Fun..</td><td rowspan=1 colspan=1>No pull-up an...</td><td rowspan=1 colspan=1>Low</td><td rowspan=1 colspan=1></td><td rowspan=1 colspan=1>□</td></tr><tr><td rowspan=1 colspan=1>PD3</td><td rowspan=1 colspan=1>DCMI_D5</td><td rowspan=1 colspan=1>n/a</td><td rowspan=1 colspan=1>Alternate Fun...</td><td rowspan=1 colspan=1>No pull-up an..</td><td rowspan=1 colspan=1>Low</td><td rowspan=1 colspan=1>DCMI_D5</td><td rowspan=1 colspan=1>V</td></tr><tr><td rowspan=1 colspan=1>PE5</td><td rowspan=1 colspan=1>DCMI_D6</td><td rowspan=1 colspan=1>n/a</td><td rowspan=1 colspan=1>Alternate Fun..</td><td rowspan=1 colspan=1>No pull-up an...</td><td rowspan=1 colspan=1>Low</td><td rowspan=1 colspan=1>DCMI_D6</td><td rowspan=1 colspan=1>V</td></tr><tr><td rowspan=1 colspan=1>PE6</td><td rowspan=1 colspan=1>DCMI_D7</td><td rowspan=1 colspan=1>n/a</td><td rowspan=1 colspan=1>Alternate Fun..</td><td rowspan=1 colspan=1>No pull-up an.….</td><td rowspan=1 colspan=1>Low</td><td rowspan=1 colspan=1>DCMI_D7</td><td rowspan=1 colspan=1>V</td></tr><tr><td rowspan=1 colspan=1>PG9</td><td rowspan=1 colspan=1>DCMI_VSYNC</td><td rowspan=1 colspan=1>n/a</td><td rowspan=1 colspan=1>Alternate Fun..</td><td rowspan=1 colspan=1>No pull-up an..</td><td rowspan=1 colspan=1>Low</td><td rowspan=1 colspan=1>DCMI_VSYNC</td><td rowspan=1 colspan=1>V</td></tr><tr><td rowspan=1 colspan=1>PH9</td><td rowspan=1 colspan=1>DCMI_Do</td><td rowspan=1 colspan=1>n/a</td><td rowspan=1 colspan=1>Alternate Fun...</td><td rowspan=1 colspan=1>No pull-up an...</td><td rowspan=1 colspan=1>Low</td><td rowspan=1 colspan=1>DCMI_Do</td><td rowspan=1 colspan=1>V</td></tr><tr><td rowspan=1 colspan=1>PH10</td><td rowspan=1 colspan=1>DCMI_D1</td><td rowspan=1 colspan=1>n/a</td><td rowspan=1 colspan=1>Alternate Fun...</td><td rowspan=1 colspan=1>No pull-up an...</td><td rowspan=1 colspan=1>Low</td><td rowspan=1 colspan=1>DCMI_D1</td><td rowspan=1 colspan=1>V</td></tr><tr><td rowspan=1 colspan=1>PH11</td><td rowspan=1 colspan=1>DCMI_D2</td><td rowspan=1 colspan=1>n/a</td><td rowspan=1 colspan=1>Alternate Fun...</td><td rowspan=1 colspan=1>No pull-up an..</td><td rowspan=1 colspan=1>Low</td><td rowspan=1 colspan=1>DCMI_D2</td><td rowspan=1 colspan=1>V</td></tr><tr><td rowspan=1 colspan=1>PH12</td><td rowspan=1 colspan=1>DCMI_D3</td><td rowspan=1 colspan=1>n/a</td><td rowspan=1 colspan=1>Alternate Fun..</td><td rowspan=1 colspan=1>No pull-up an.</td><td rowspan=1 colspan=1>Low</td><td rowspan=1 colspan=1>DCMI_D3</td><td rowspan=1 colspan=1>V</td></tr><tr><td rowspan=1 colspan=1>PH14</td><td rowspan=1 colspan=1>DCMI_D4</td><td rowspan=1 colspan=1>n/a</td><td rowspan=1 colspan=1>Alternate Fun..[</td><td rowspan=1 colspan=1>No pull-up an..</td><td rowspan=1 colspan=1>Low</td><td rowspan=1 colspan=1>DCMI_D4</td><td rowspan=1 colspan=1></td></tr></table>

# Set the GPIO pull-up/pull-down.

GPIO Pull-up/Pull-down

![](images/6069530af46ed8bdba1795a87e60c50c38b85ac5989bb92ff2640de09450c410.jpg)  
Figure 56. STM32CubeMX - GPIO no pull-up and no pull-down selection

# STM32CubeMX - Configuration of DCMI control signals and capture mode

1Click on Parameter Settings tab in DCMI Configuration window.

![](images/a824ca68a71641fffff3de0a74c9f036e5a8d7cf7d0a12a8501c37c58902dff0.jpg)  
Figure 57. STM32CubeMX - Parameter Settings tab

Set hedifferent parmeer vertial synchronization,horizntal ynchronization,an piel clock pol that must be programmed according to the camera module configuration.

![](images/2d681b623feccb955bde78297716431e42f65129a08e8b27b38f9255e4b61e6e.jpg)  
Figure 58. STM32CubeMX - DCMI control signals and capture mode

# Note:

Thevertical synchronization polarity must be activehigh, and thehorizontal synchronization polarity must e active low. They must not be inverted for this configuration of the camera module.

# 8.3.2.3

# STM32CubeMX - Enable DCMI interrupts

Select NVIC Settings tab in DCMI Configuration window, and check the DCMI global interrupt.

![](images/368a8bf1a7121dc194f485dc8352820354601ff737a39ab09f469512e463c080.jpg)  
Figure 59. STM32CubeMX - Configuration of DCMI interrupts

# 8.3.2.4

# STM32CubeMX - DMA configuration

This configuration aims to receive RGB565 data (2 byte/pixel). The image resolution is QVGA (320x240). The image size is then 320 × 240 x 2 = 153600 bytes.

She a wi fom heMy wor ent fomeMI atgis e dataitems i heMASDTRregister heumber  word ranser.Thember word  hen 38400 (153600 / 4) which is less than 65535.

In apshot mode, the user can confgure heDA i oral mode. I contis mode, the usercan coure the DMA in circular mode.

Select DMA Settings tab in DCMI Configuration window.

![](images/ca46c4557857230eb5ed3cabd987e906fac14e724fa52851a736ca770b8401cb.jpg)  
Figure 60. STM32CubeMX - DMA Settings tab

# Click on the Add button.

![](images/4b61675b354db00bbc08b138b7241468db030553f91017979eb1f5476c5f428a.jpg)  
Figure 61. STM32CubeMX - Add button

Click on Select under DMA Request, and choose DCMI. The DMA2 Stream 1 channel 1 is configured to transfer the DCMl request each time its time register is fulfilled.

![](images/a57a9c6a89ed5f116cb558324b69f1a84aff14cee883763e31c4e0910dde2c91.jpg)  
Figure 62. STM32CubeMX - DMA stream configuration

# Modify the DMA Request Settings.

![](images/346cc476f81f297a6dc83293e0d11c630e21aa89a37ae1018eab04013f34fcfe.jpg)  
Figure 63. STM32CubeMX - DMA configuration

# 8.3.2.5

# STM32CubeMX - Camera module power-up pins

To power up the camera module, the PH13 pin must be configured for 32F746GDISCOVERY.   
Click on the PH13 pin and select GPIO_Output in the Pinout tab.

![](images/eb9a0f95207ec11797c55d17d6e8512da3e00d5ec041fbe40122d45a84785743.jpg)  
Figure 64. STM32CubeMX - PH13 pin configuration   
Figure 65. STM32CubeMX - GPIO button

In Pinout & Configuration tab system core, click on the GPIO button.

# 3Set the parameters.

![](images/0029ab81a6d18a92dc20a08092375063d30b56343b96a2923059f566be906a41.jpg)  
Figure 66. STM32CubeMX - DCMI power pin configuration

# 8.3.2.6

# STM32CubeMX - System clock configuration

In this example, the system clock is configured as follows:

Use of an external HSE clock, where the main PLL is used as a system source clock HCLK @ 200 MHz, so the Cortex®-M7 and LTDC are both running at 200 MHz

# Note:

HCLK is set to 200 MHz but not 216 MHz, to set the SDRAM_FMC at its maximum speed of 100 MHz with an HCLK/2 prescaler.

Select the Clock Configuration tab.

![](images/b90f0f4c05217187b4a97439c379af5780e38a3823db76b9105ae3058f053721.jpg)  
Figure 67. STM32CubeMX - HSE configuration

Set the PLLs and the prescalers in the Clock Configuration tab, t get the system clock HCLK @ 200 MHz.

![](images/d2635cf2c1b8b31d74c1a8c68a021f9eea4588f3291242ddcc10edcf33d5306d.jpg)  
Figure 68. STM32CubeMX - Clock configuration

# 8.3.2.7

# Adding files to the proje

Generate the code and open the generated project using the preferred toolchain. Then follow these steps:

1. Right click on Drivers/STM32F7xx_HAL_Driver.

2Choose "Add Existing Files to group 'Drivers/STM32F7xx_HAL_Driver...'

3. Select the following files in Drivers/STM32F7xx_HAL_Driver/Src:

stm32f7xx_hal_dma2d.c stm32f7xx_hal_ltdc.c stm32f7xx_hal_ltdc_ex.c stm32f7xx_hal_sdram.c stm32f7xx_hal_uart.c stm32f7xx_ll_fmc.c

4Create a new group called, for example, Imported_Drivers.

yeo 32G ldeoy helde he o:

stm32746g_discovery.c stm32746g_discovery_sdram.c

yheoll  from he T37GDyolderory he Inoldehe o: stm32746g_discovery.h stm32746g_discovery_sdram.h

7Copy ov9655 . c from the Components folder to the Src folder.

i.Copy ov9655 . h from the Components folder to the Inc folder.

9. Copy camera . h from the Component/Common folder to the Inc folder.

10. Add the following files in the new group (called Imported_Drivers in this example):

stm32746g_discovery.h stm32746g_discovery_sdram.h ov9655.c

11. Allow modifications on ov9655.h and camera.h (read-only by default):

aClick right on the file.   
bUncheck read-only.   
cClick on Apply and OK.

12.Modify ov9655.h by replacing #include "../Common/camera.h" by #include "camera.h".

13. Copy the following files to the Inc folder:

rk043fn48h.h from Components folder fonts. h from Utilities/Fonts folder

14. Copy fonts24. c from Utilities/Fonts folder to the Src folder.

Check that no problem happened by rebuilding allfiles. There must be no error and no warning.

# 8.3.2.8 Modifications in main.c file

Upyertng ometcn clueeedequaadi bold below). This task provides the project modification and regeneration without losing the user code.

# USER CODE BEGIN Includes \*/

#include "stm32746g_discovery.h"   
#include "stm32746g_discovery_sdram.h"   
#include "ov9655.h"   
#include "rk043fn48h.h"   
#include "fonts.h"

'\* USER CODE END Includes \*/

Some variable declarations must then be inserted in the adequate space indicated in bold below.

/\* USER CODE BEGIN PV \*/   
/\* Private variables   
typedef enum   
{   
CAMERA_OK = Ox00,   
CAMERA_ERROR = Ox01,   
CAMERA_TIMEOUT = Ox02,   
CAMERA_NOT_DETECTED = Ox03,   
CAMERA_NOT_SUPPORTED = Ox04   
Camera_StatusTypeDef;   
typedef struct   
{   
uint32_t TextColor;   
uint32_t BackColor;   
SFONT \*pFont;   
}LCD_DrawPropTypeDef;   
typedef struct   
{   
int16_t X;   
int16_t Y;   
}Point, \* pPoint;   
static LCD_DrawPropTypeDef DrawProp[2];   
LTDC_HandleTypeDef hltdc;   
LTDC_LayerCfgTypeDef layer_cfg;   
static RCC_PeriphCLKInitTypeDef periph_clk_init_struct; CAMERA_DrvTypeDef \*camera_driv;   
/\* Camera module I2C HW address \*/   
static uint32_t CameraHwAddress;   
/\* Image size\*/   
uint32_t Im_size = 0;   
/\* USER CODE END PV \*/

The function prototypes must also be inserted in the adequate space indicated in bold below.

# /\* USER CODE BEGIN PFP \* / \* Private function prototypes

uint8_t CAMERA_Init(uint32_t );   
static void LTDC_Init(uint32_t , uint16_t , uint16_t , uint16_t, uint16_t );   
void LCD_GPIO_Init(LTDC_HandleTypeDef \*, void \*);

/\* USER CODE END PFP \*/

Updatemaifunction by inserting some functions i theadequate spaceindicatein bold below).

LTDC_Init allows the configuration and initialization of the LCD.   
BSP_SDRAM_Init allows the configuration and initialization of the SDRAM.   
CAMERA_ Init allows the configuration of the camera module, DCMI registers, and DCMI parameters.   
One of the two functions HAL_DCMI_Start_DMA allowing the DCMI configuration in snapshot or in continuous mode, must be uncommented.

# /\* USER CODE BEGIN 2 \*/

LTDC_Init(FRAME_BUFFER, 0, 0, 320, 240);   
BSP_SDRAM_Init();   
CAMERA_Init(CAMERA_R320x240);   
HAL_Delay(1000); //Delay for the camera to output correct data   
Im_size = 0x9600; //size=320\*240\*2/4   
/\*¯uncomment the following line in case of snapshot mode \*/   
//HAL_DCMI_Start_DMA(&hdcmi, DCMI_MODE_SNAPSHOT, (uint32_t)FRAME_BUFFER, Im_size); /\* uncomment the following line in case of continuous mode \*/   
HAL_DCMI_Start_DMA(&hdcmi, DCMI_MODE_CONTINUOUS , (uint32_t)FRAME_BUFFER, Im_size); /\* USER CODE END 2 \*/

adequate space, indicated in bold below.

/\* USER CODE BEGIN 4 \*/   
void LCD_GPIO_Init(LTDC_HandleTypeDef \*hltdc, void \*Params)   
{   
GPIO_InitTypeDef gpio_init_structure;   
/\* Enable the LTDC and DMA2D clocks \*/   
HAL_RCC_LTDC_CLK_ENABLE();   
HAL_RCC_DMA2D_CLK_ENABLE();   
/\* Enable GPIos clock \*/   
HAL_RCC_GPIOE_CLK_ENABLE();   
HAL_RCC_GPIOG_CLK_ENABLE();   
_HAL_RCC_GPIOI_CLK_ENABLE();   
_HAL_RCC_GPIOJ_CLK_ENABLE();   
_HAL_RCC_GPIOK_CLK_ENABLE();   
/\*\*\* LTDC Pins configuration \*\*\*/   
/\* GPIOE configuration \*/   
gpio_init_structure.Pin = GPIO_PIN_4;   
gpio_init_structure.Mode = GPI_MODE_AF_PP;   
gpio_init_structure.Pull = GPIo_NOPULL;   
gpio_init_structure.Speed = GPIo_SPEED_FAST;   
gpio_init_structure.Alternate = GPIO_AF14_LTDC;   
HAL_GPIO_Init(GPIOE, &gpio_init_structure);   
/\* GPIOG configuration \*/   
gpio_init_structure.Pin = GPIO_PIN_12;   
gpio_init_structure.Mode = GPI_MODE_AF_PP;   
gpio_init_structure.Alternate =¯GPIO_AF9_LTDC;   
HAL_GPIO_Init(GPIOG, &gpio_init_structure);   
/\* GPIOI¯LTDC alternate configuration \*/   
gpio_init_structure.Pin = GPIO_PIN_9 | GPIO_PIN_10 | GPIO_PIN_13   
GPIO_PIN_14 | GPIO_PIN_15;   
gpio_init_structure.Mode = GPIO_MODE_AF_PP;   
gpio_init_structure.Alternate =¯GPIO_AF14_LTDC;   
HAL_GPIO_Init(GPIOI, &gpio_init_structure);   
/\* GPIOJ¯configuration \*/   
gpio_init_structure.Pin = GPIO_PIN_0 | GPIO_PIN_1 | GPIO_PIN_2   
GPIO_PIN_3 | GPIO_PIN_4 | GPIO_PIN_5 | GPIO_PIN_6 | GPIO_PIN_7 GPIO_PIN_5 | GPIO_PIN_6 | GPIO_PIN_7 |GPI_PIN_8 | GPI_PIN_9 | GPI_PIN_10   
GPIO_PIN_11 | GPIO_PIN_13 | GPIO_PIN_14 | GPIO_PIN_15;   
gpio_init_structure.Mode = GPIO_MODE_AF_PP;   
gpio_init_structure.Alternate =¯GPIo_AF14_LTDC;   
HAL_GPIO_Init(GPIOJ, &gpio_init_structure);   
/\* GPIOK configuration \*/   
gpio_init_structure.Pin = GPIo_PIN_0 | GPIO_PIN_1 | GPIO_PIN_2   
GPIO_PIN_4 | GPIO_PIN_5 | GPIO_PIN_6 | GPIO_PIN_7;   
gpio_init_structure.Mode = GPI_MODE_AF_PP;   
gpio_init_structure.Alternate =¯GPIO_AF14_LTDC;   
HAL_GPIO_Init(GPIOK, &gpio_init_structure);   
/\* LCD_DISP GPIO configuration \*/   
gpio_init_structure.Pin = GPIO_PIN_12; /\* LCD_DISP pin has to be   
manually controlled \*/   
gpio_init_structure.Mode = GPIO_MODE_OUTPUT_PP;   
HAL_GPIO_Init(GPIOI, &gpio_init_structure);   
/\* LCD_BL_cTRL GPIO configuratin \*/   
gpio_init_structure.Pin = GPIO_PIN_3; /\* LCD_BL_CTRL pin has to be   
manually controlled \*/   
gpio_init_structure.Mode = GPIO_MODE_OUTPUT_PP;   
HAL_GPIO_Init(GPIOK, &gpio_init_structure);   
}   
static void LTDC_Init(uint32_t FB_Address, uint16_t Xpos, uint16_t Ypos, uint16_t Width, uint16_t Height)   
{   
/\* Timing Configuration \*/   
hltdc.Init.HorizontalSync = (RK043FN48H_HSYNC - 1);   
hltdc.Init.VerticalSync = (RK043FN48H_vSYNC - 1);   
hltdc.Init.AccumulatedHBP = (RK043FN48H_HSYNC + RK043FN48H_HBP - 1); hltdc.Init.AccumulatedVBP = (RK043FN48H_vSYNC + RK043FN48H_vBP - 1); hltdc.Init.AccumulatedActiveH = (RK043FN48H_HEIGHT + RK043FN48H_VSYNC + RK043FN48H_VBP - 1); hltdc.Init.AccumulatedActiveW = (RK043FN48H_WIDTH + RK043FN48H_HSYNC + RK043FN48H_HBP - 1);   
hltdc.Init.TotalHeigh = (RK043FN48H_HEIGHT + RKO43FN48H_VSYNC + RK043FN48H_VBP + RK043FN48H_VFP - 1);   
hltdc.Init.TotalWidth = (RK043FN48H_WIDTH + RK043FN48H_HSYNC +   
RK043FN48H_HBP + RK043FN48H_HFP - 1);   
/\* LCD clock configuration \*/   
periph_clk_init_struct.PeriphClockSelection = RCC_PERIPHCLK_LTDC; periph_clk_init_struct.PLLSAI.PLLSAIN = 192;   
periph_clk_init_struct.PLLSAI.PLLSAIR = RKO43FN48H_FREQUENCY_DIVIDER; periph_clk_init_struct.PLLSAIDivR = RCC_PLLSAIDIVR_4;   
HAL_RCCEx_PeriphCLKConfig(&periph_clk_init_struct);   
/\* Initialize the LCD pixel width\~and pixel height \*/   
hltdc.LayerCfg->ImageWidth = RK043FN48H_WIDTH;   
hltdc.LayerCfg->ImageHeight = RK043FN48H_HEIGHT;   
hltdc.Init.Backcolor.Blue = 0;/\* Background value \*/   
hltdc.Init.Backcolor.Green = 0;   
hltdc.Init.Backcolor.Red = 0;   
/\* Polarity \*/   
hltdc.Init.HSPolarity = LTDC_HSPOLARITY_AL;   
hltdc.Init.VSPolarity = LTDc_vSPOLARITY_AL;   
hltdc.Init.DEPolarity = LTDC_DEPOLARITY_AL;   
hltdc.Init.PCPolarity = LTDC_PCPOLARITY_IPC;   
hltdc.Instance = LTDC;   
if(HAL_LTDC_GetState(&hltdc) == HAL_LTDC_STATE_RESET)   
{   
LCD_GPIO_Init(&hltdc, NULL);   
HAL_LTDC_Init(&hltdc);   
/\* Assert display enable LCD_DISP pin \*/   
HAL_GPIO_WritePin(GPIOI, GPI_PIN_12, GPIO_PIN_SET);   
/\* Assert backlight LCD_BL_CTRL pin \*/   
HAL_GPIO_WritePin(GPIOK, GPIO_PIN_3, GPIO_PIN_SET);   
DrawProp[0].pFont = &Font24;   
/\* Layer Init \*/   
layer_cfg.WindowX0 = Xpos;   
layer_cfg.WindowX1 = Width;   
layer_cfg.WindowY0 = Ypos;   
layer_cfg.WindowY1 = Height;   
layer_cfg.PixelFormat = LTDC_PIXEL_FORMAT_RGB565;   
layer_cfg.FBStartAdress = FB_Address;   
layer_cfg.Alpha = 255;   
layer_cfg.Alpha0 = 0;   
layer_cfg.Backcolor.Blue = 0;   
layer_cfg.Backcolor.Green = 0;   
layer_cfg.Backcolor.Red = 0;   
layer_cfg.BlendingFactor1 = LTDC_BLENDING_FACTORl_PAxCA;   
layer_cfg.BlendingFactor2 = LTDC_BLENDING_FACTOR2_PAxCA;   
layer_cfg.ImageWidth = Width;   
layer_cfg.ImageHeight = Height;   
HAL_LTDC_ConfigLayer(&hltdc, &layer_cfg, 1);   
DrawProp[1].BackColor = ((uint32_t)OxFFFFFFFF);   
DrawProp[1].pFont = &Font24;   
DrawProp[1].TextColor = ((uint32_t)OxFF000000);   
}   
uint8_t CAMERA_Init(uint32_t Resolution) /\*Camera initialization\*/ {   
uint8_t status = CAMERA_ERROR;   
/\* Read ID of Camera module via I2C \*/   
if(Ov9655_ReadID(CAMERA_I2C_ADDRESS) == OV9655_ID)   
{   
camera_driv = &ov9655_drv;/\* Initialize the camera driver structure \*/ CameraHwAddress = CAMERA_I2C_ADDRESS;   
if (Resolution == CAMERA_R320x240)   
camera_driv->Init(CameraHwAddress, Resolution);   
HAL_DCMI_DisableCROP(&hdcmi);   
}   
status = CAMERA_OK; /\* Return CAMERA_OK status \*/   
} else   
{   
status = CAMERA_NOT_SUPPORTED; /\* Return CAMERA_NOT_SUPPORTED status }   
return status;   
}   
/\* USER CODE END 4

# 8.3.2.9 Modifications in main.h file

Upa

/\* USER CODE BEGIN Private defines \* #define FRAME_BUFFER OxC0000000 /\* USER CODE END Private defines \*

At this stage, the user can build, debug, and run the project.

# 8.3.3

# RGB data capture and display

To simplify this example, data are captured and displayed inRGB565 format (2 pp. The mage resolution is 320x240 (QVGA). The frame buffer is placed in the SDRAM. Camera and LCD data are located in the same frame buffer. The LCD displays then directly the data captured through the DCMI without any processing. The camera module is configured to output RGB565 data, QVGA (320x240).

The configuration of this example can be done by following the steps described in Section 8.3.2.

# 8.3.4 YCbCr data capture

This implementation example aims to receive YCbCrdata from the camera module, and to transfer them t the SDRAM.

Displaying the YCbCr received data on the LCD (configured to display RGB565 data in the previous configuration) is not correct, but can be used for verification.

To display images correctly, YCbCr data must be converted into RGB565 data (or RGB888 or ARGB8888, depending on the application needs).

All the configuration steps signaled in Section 8.3.2 must be followed.

Someinstructions must be added tobtain YCbCr data.Only he camera configuration has to beupdated by adding:

A table of constants allowing the configuration of camera module registers

• A new function used to configure the camera module by sending the register configuration through the I2C.

# Add the table containing the configuration of camera module registers in main C,

below /\* Private variables

const unsigned char OV9655_YUV_QVGA [ ][2]=  
{ { 0x12, 0x80 },{ Ox00, Ox00 },{ Ox01, Ox80 },{ Ox02, Ox80 },{ 0x03, 0x02},{ 0x04, 0x03 },{ Ox0e, Ox61 } { Ox0f, Ox42 },{ Ox11, Ox01 },{ Ox12, 0x62},{ x13, Oxe7 },{ Ox14, Ox3a },{ Ox16, 0x24 },{ Ox17, 0x18 }, { 0x18, 0x04},{Ox19, Ox01 },{ Ox1a, Ox81 } ,{ Ox1e, Ox04 },{ Ox24, Ox3c },{ Ox25, 0x36},{0x26, 0x72 }, { Ox27, 0x08 },{ 0x28, Ox08 },{ Ox29, Ox15 },{Ox2a, 0x00},{ 0x2b, 0x00 },{ Ox2c, Ox08 },{ Ox32, Ox24 }, 0x33, Ox00 },{ Ox34, 0x3f}, { 0x35, 0x00 },{ Ox36, 0x3a },{ 0x38, Ox72 },{ Ox39, Ox57 } , { 0x3a, 0x0c}, { 0x3b, 0x04 },{ Ox3d, Ox99 },{ Ox3e, Ox0e },{ Ox3f, Oxc1 },{Ox40,Oxc0},{ Ox41, Ox01 },{ Ox42, Oxc0 },{ Ox43, Ox0a },{ Ox44, Oxf0 },{ Ox45, Ox46},{ 0x46, 0x62} , { 0x47, 0x2a }, { 0x48, Ox3c },{ Ox4a, Oxfc}, { 0x4b, 0xfc},{Ox4c, 0x7f },{ Ox4d, 0x7f}, Ox4e, Ox7f },{ Ox52, Ox28 },{ Ox53, 0x88},{0x54, Oxb0 }, { Ox4f, 0x98 },{Ox50,Ox98} , { Ox51, Ox00 },{ Ox58, Ox1a} { 0x59, Ox85 },{ Ox5a, Oxa9 },{ Ox5b, Ox64 } ,{ Ox5c, Ox84 },{ 0x5d, 0x53},{Ox5e, Ox0e },{ Ox5f, Oxf0 },{ Ox60, Oxf0 },{ Ox61, 0xf0 } , { 0x62, 0x00}, 0x63, 0x00 },{ Ox64, Ox02 },{ Ox65, Ox20 },{ Ox66, 0x00 },{ Ox69, 0x0a}, { Ox6b, 0x5a },{ Ox6c, 0x04 }, { 0x6d, Ox55 },{ Ox6e, Ox00 },{ Ox6f, 0x9d}, { 0x70, 0x21 },{Ox71, 0x78 },{ Ox72, Ox11 },{ Ox73, Ox01 { 0x74 0x10}, { 0x75 0x10 } { 0x76, 0x01 },{ Ox77, Ox02 },{ Ox7a, Ox12 },{ Ox7b, 0x08}, { 0x7c, 0x15 }, { 0x7d, Ox24 },{ Ox7e, Ox45 },{ Ox7f, Ox55 },{ Ox80, Ox6a} { 0x81, Ox78 },{ Ox82, Ox87 },{ Ox83, Ox96 }, { Ox84, Oxa3 },{ Ox85, 0xb4},{ 0x86, 0xc3 },{0x87, Oxd6 },{ Ox88, Oxe6 } ,{ Ox89, Oxf2 },{ Ox8a, Ox24}, { 0x8c, 0x80 }{ 0x90, Ox7d },{ Ox91, Ox7b },{ Ox9d, 0x02 } , { 0x9e, 0x02}, { 0x9f, Ox7a },{ Oxa0, Ox79 }, { Oxal, 0x40 },{ Oxa4, Ox50 },{ Oxa5, 0x68}, { Oxa6, Ox4a },{ Oxa8, Oxc1 },{ Oxa9, Oxef },{ Oxaa, Ox92 }, { Oxab, 0x04} , { Oxac, 0x80 },{ Oxad, Ox80 },{ Oxae, Ox80 },{ Oxaf, Ox80 },{ Oxb2, 0xf2}, { Oxb3, Ox20 } ,{ Oxb4, Ox20 },{ Oxb5, Ox00 },{ Oxb6, Oxaf },{ Oxbb, Oxae}, { Oxbc, Ox7f },{ Oxbd, Ox7f } ,{ Oxbe, Ox7f },{ Oxbf, Ox7f },{ Oxc0, Oxaa},{Oxc1, Oxc0 },{ Oxc2, Ox01 },{ Oxc3, Ox4e } ,{ Oxc6, Ox05 },{ Oxc7, Ox81}{ Oxc9, Oxe0 },{ Oxca, Oxe8 },{ Oxcb, Oxf0 },{ Oxcc, Oxd8 } ,{ Oxcd, 0x93}, { Oxcd, 0x93 },{ OxFF, OxFF }};

:.The new function prototype has to be inserted below /\* Private function prototypes \* .

void Ov9655_YUV_Init (uint16_t );

The second step of modifications in main. described in Section 8.3.2.8 has to be updated. Modify the tollowicseuaaidaol blow the two functions allowing the DCMI configuration in snapshot or in continuous mode must be uncommented.

# 1 \* USER CODE BEGIN 2 \*/

BSP_SDRAM_Init();   
CAMERA_Init(CameraHwAddress);   
OV9655_YUV_Init(CameraHwAddress);   
HAL_Delay(1000); //Delay for the camera to output correct data   
Im_size = 0x9600; //size=320\*240\*2/4   
/\*¯uncomment the following line in case of snapshot mode \*/   
//HAL_DCMI_Start_DMA(&hdcmi, DCMI_MODE_SNAPSHOT, (uint32_t)FRAME_BUFFER, Im_size); /\* uncomment the¯following line in case of continuous mode \*/   
HAL_DCMI_Start_DMA(&hdcmi, DCMI_MODE_CONTINUOUS , (uint32_t)FRAME_BUFFER, Im_size); /\* USER CODE END 2 \*/

The third step o modfications inmaidescribed inSection 8.3..8has to be updated by ading thenew function implementation.

void Ov9655_YUV_Init(uint16_t DeviceAddr)   
{ uint32_t index;   
for(index=0; index<(sizeof(OV9655_YUV_QVGA)/2); index++) [ CAMERA_IO_Write(DeviceAddr, OV9655_YUV_QVGA[index][0], OV9655_YUV_QVGA[index][1]);   
CAMERA_Delay(1);

# 1.3.5

# Y only data capture

Iple  uut ayge yel e,he r cop  n  only hecot ranser t the frame buffer in the SDRAM.

All the configuration steps signaled in Section 8.3.2 must be followed.

S instucins must eae btain eYy aOny hemea an heDM coguratins e ut To simpliy this taskmmust bemodifi sdescibe inSection 8.., ut the econs STM32CubeMX - DCMI control signals and capture mode configuration, or the static void MX_DCMI_Init (void) function (this function is implemented in main. c) must be modified..

hdcmi.Instance = DCMI;   
hdcmi.Init.SynchroMode = DCMI_SYNCHRO_HARDWARE;   
hdcmi.Init.PCKPolarity = DCMI_PCKPOLARITY_RISING;   
hdcmi.Init.VSPolarity = DCMI_vSPOLARITY_HIGH;   
hdcmi.Init.HSPolarity = DCMI_HSPOLARITY_LOW;   
hdcmi.Init.CaptureRate = DCMI_CR_ALL_FRAME;   
hdcmi.Init.ExtendedDataMode =¯DCMI_EXTEND_DATA_8B;   
hdcmi.Init.ByteSelectMode = DCMI_BSM_OTHER;   
hdcmi.Init.ByteSelectStart = DCMI_OEBS_EVEN;   
hdcmi.Init.LineSelectMode = DCMI_LSM_ALL;   
hdcmi.Init.LineSelectStart = DCMI_OELS_ODD;

# 8.3.6

# Resolution capture (YCbCr data format)

This implementation example aims to receive YCbCrdata from the camera module, and to transfer them t the SDRAM. The captured image resolution is 1280x1024.

To display images correctly, YCbCr data must be converted into RGB565 data (or RGB888 or ARGB8888, depending on the application needs).

the configuration steps details in Section 8.3.2 must be followed.

Som istructions must beaded tobtain heYCbCrdataOnlyhe DMA and the camera module configuratin have to be updated.

# DMA configuration

The DMA is configured as described in Section 6.4.9: DMA configuration for higher resolutions. The HALATARTcn ensure h cguratin becaus heag  ec heaxualw for double-buffer mode.

Calling HALDATART ensures thedivision of the received frames to equal parts, and the placement ach pnbuf u buffer size is equal to 40960 words.

For the uffdess, ALAARsures he placment e1 me buffr in heemory. I case, the address f the first frame buffers OxC00000.The second address is then xC0163840 (xC0000000 + (40960 \* 4)). The 16th frame buffer address is (0xC0000000 + 16 \* (40960 \* 4)).

iscalculate and oe pointe ismodifd as ilustrated n igure.DMAoperatio high resolutis.

# Camera module configuration

The new camera module configuration is done by adding:

A table of constants allowing the configuration of camera module registers A new function used to configure the camera module by sending the register configuration through the I2C

To ensure that the camera module sends images having a YCbCr format, the CMOS sensor registers must be configured with the following steps:

# . Add the table containing the configuration of camera module registers in main. C

# below /\* Private variables

const unsigned char ov9655_yuv_sxga[][2]= {{ Ox12, Ox80 },{ Ox00, 0x00 },{ Ox01, Ox80 },{ Ox02, Ox80 },{ Ox03, Ox1b },{Ox04, Ox03 }, { Ox0e, Ox61 },{ Ox0f, Ox42 },{ Ox11, Ox00 },{ Ox12, Ox02 },{Ox13, Oxe7 },{ Ox14, Ox3a },{ Ox16, Ox24 }, { Ox17, Ox1d },{ Ox18, Oxbd },{Ox19, Ox01 },{ Oxla, Ox81 }, { Ox1e, Ox04 }, { Ox24, Ox3c }, { Ox25, Ox36},{ O0x26, Ox72 }, { Ox27, 0x08 }, { 0x28, 0x08 },{ 0x29, Ox15 },{ Ox2a, 0x00},{ Ox2b, Ox00 },{ Ox2c, Ox08 },{ Ox32, Oxff },{ Ox33, Ox00 },{ Ox34, Ox3d},{ Ox35, Ox00 },{ Ox36, Oxf8 },{ Ox38, Ox72 },{ Ox39, Ox57 }, { Ox3a, Ox0c},{Ox3b, 0x04 },{ Ox3d, Ox99 }, { Ox3e, Ox0c },{ Ox3f, Oxc1 },{ Ox40, Oxd0},{Ox41 Ox00 },{ Ox42, Oxc0 },{ Ox43, Ox0a },{ Ox44, Oxf0 },{ Ox45, Ox46},{0x46, Ox62 }, { Ox47, Ox2a }, { Ox48, Ox3c },{ Ox4a, Oxfc },{ Ox4b, Oxfc},{Ox4c, Ox7f },{ Ox4d, Ox7f },{ Ox4e, Ox7f },{ Ox52, Ox28 },{ Ox53, 0x88},{0x54, Oxb0 },{ Ox4f, Ox98 },{ Ox50, Ox98 },{ Ox51, 0x00 },{ Ox58, Ox1a},{ Ox58, Ox1a },{ Ox59, Ox85 },{ Ox5a, Oxa9 },{ Ox5b, Ox64 },{ Ox5c, Ox84},{ Ox5d, Ox53 },{ Ox5e, Ox0e }, { Ox5f, Oxf0 }, { Ox60, Oxf0 }, { Ox61,Oxf0 },{ Ox62, Ox00 }, { 0x63, 0x00 }, { O0x64, 0x02 },{ 0x65, Ox16 },{ Ox66,Ox01 },{ Ox69, 0x02 },{ Ox6b, Ox5a }, { Ox6c, Ox04 }, { Ox6d, 0x55 }, {Ox6e, Ox00 },{ Ox6f, Ox9d },{ Ox70, Ox21 }, { Ox71, Ox78 },{ Ox72, Ox00 },{Ox73, Ox01 },{ Ox74, Ox3a },{ Ox75, Ox35_},{ Ox76, Ox01 },{ Ox77, Ox02 },{0x7a, Ox12 },{ Ox7b, Ox08 }, { Ox7c, Ox15 }, { Ox7d, Ox24 },{ Ox7e, Ox45 },{Ox7f, Ox55 },{ Ox80, Ox6a },{ Ox81, Ox78 },{ Ox82, Ox87 },{ Ox83, Ox96 },{Ox84, Oxa3 },{ Ox85, Oxb4 }, { Ox86, Oxc3 },{ Ox87, Oxd6 },{ Ox88, Oxe6 },{ Ox89, Oxf2 },{ Ox8a, Ox03 }, { Ox8c, 0x0d }, { Ox90, Ox7d }, { Ox91, Ox7b}, { Ox9d, 0x03 },{ Ox9e, Ox04 }, { Ox9f, Ox7a }, { Oxa0, Ox79 }, { Oxal,Ox40 }, { Oxa4, Ox50 },{ Oxa5, Ox68 }, { Oxa6, Ox4a }, { Oxa8, Oxcl },{Oxa9, Oxef }, { Oxaa, Ox92 },{ Oxab, Ox04 },{ Oxac, Ox80 },{ Oxad, Ox80 },{Oxae, Ox80 },{ Oxaf, Ox80 },{ Oxb2, Oxf2 },{ Oxb3, Ox20 },{ Oxb4, Ox20 },{Oxb5, Ox00 },{ Oxb6, Oxaf },{ Oxbb, Oxae },{ Oxbc, Ox7f },{ Oxbd, Ox7f },{Oxbe, Ox7f }, { Oxbf, Ox7f },{ Oxc0, Oxe2 },{ Oxc1, Oxc0 },{ Oxc2, Ox01 },{ Oxc3, Ox4e }, { Oxc6, Ox05 },{ Oxc7, Ox80 }, { Oxc9, Oxe0 },{ Oxca, Oxe8}, { Oxcb, Oxf0 },{ Oxcc, Oxd8 },{0xcd, Ox93},{ OxFF, OxFF } };

The new function prototype has to be inserted below /\* Private function prototypes

void Ov9655_YUV_Init (uint16_t );

sfiatn plat heion folloing fnctionsin the adequate space ndicated in bold below). One f the twounctions aowig he DCMI configuration in snapshot or in continuous mode must be uncommented.

# \* USER CODE BEGIN 2 \*/

BSP_SDRAM_Init();   
CAMERA_Init(CameraHwAddress);   
OV9655_YUV_Init(CameraHwAddress);   
HAL_Delay(Io00); //Delay for the camera to output correct data   
Im_size = 0xA0000; //size=1280\*1024\*2/4   
/\*¯uncomment the following line in case of snapshot mode \*/   
//HAL_DCMI_Start_DMA(&hdcmi, DCMI_MODE_SNAPSHOT, (uint32_t)FRAME_BUFFER, Im_size);   
/\*¯uncomment the following line in case of continuous mode \*/   
HAL_DCMI_Start_DMA(&hdcmi, DCMI_MODE_CONTINUOUS , (uint32_t)FRAME_BUFFER, Im_size);

/\* USER CODE END 2 \*/

The third step of modifications in maidescribed in Section 8.3.2.8 has to be updated by ading the new function implementation below /\* USER CODE BEGIN 4 \*/.

void OV9655_YUV_Init(uint16_t DeviceAddr)   
{   
uint32_t index;   
for(index=0; index<(sizeof(ov9655_yuv_sxga)/2);index++) CAMERA_IO_Write(DeviceAddr, ov9655_yuv_sxga[index][0], ov9655_yuv_sxga[index][1]);   
CAMERA_Delay(1);

Note:

In cawit RG tora hesran eucheolun ispay heivag LCD_TFT by using the resizing feature of the DCMI.

# 8.3.7

# JPEG data capture

The OV9655 CMOS sensor embedded in the STM32F4DIS-Cam board does not support the compressed output data. This example is then implemented using OV2640 CMOS sensor, supporting the 8-bit format compressed data.

This example is based on the STM324x9I-EVAL (REV B) board embedding the OV2640 CMOS sensor (MB1066). The compressed data (JPEG) must be uncompressed to have YCbCr data, and converted to RGB to be playuthiplentatn exampleas nly recev JPEGdatrough he DCM nd osthe in the SDRAM.

This example is developed based on the DCMI example (SnapshotMode) provided within the STM32CubeF4 firmware, located in Projects\STM324x9I_EVAL\Examples\DCMI\DCMI_SnapshotMode.The provided example, aims to capture one RGB frame (QVGA resolution), and to display it on the LCD-TFT, having the following configuration:

The DCMI and I2C GPIOs are configured as described in Section 8.3.2.   
The system clock runs at 180 MHz.   
SDRAM clock runs at 90 MHz.   
The DCMI is configured to capture 8-bit data width in hardware synchronization (uncompressed data).   
The camera module is configured to output RGB data images with QVGA resolution.

Bason this example, t be able to capture JPEGdat, the user needs tomodify the DCMI and thecamea module configuration.

# DCMI configuration

The DCMI needs to be configured to receive compressed data (JPEG) by setting the JPEG bit in DCMI_CR. To t thi heuser mussiplya he nstuion rie nbold belowh fleiuint8tBSP_CAMERA_Init(uint32tResolution) (thisnctcalleinmain() toconue the DCMI and the camera module). The DCMI previous configuration is kept.

phdcmi->Init.CaptureRate = DCMI_CR_ALL_FRAME;   
phdcmi->Init.HSPolarity = DCMI_HSPOLARITY_LOW;   
phdcmi->Init.SynchroMode = DCMI_SYNCHRO_HARDWARE;   
phdcmi->Init.VSPolarity = DCMI_VSPOLARITY_LOW;   
phdcmi->Init.ExtendedDataMode = DCMI_EXTEND_DATA_8B;   
phdcmi->Init.PCKPolarity = DCMI_PCKPOLARITY_RISING;   
phdcmi->Init.JPEGMode = DCMI_JPEG_ENABLE;

# Camera module configuration

# The configuration of CMOS sensor (ov2640) registers must be inserted in the ov2 64 0. c file.

const unsigned char OV2640_JPEG[][2]=   
{Oxff, Ox00},{0x2c, Oxff},{0x2e, Oxdf},{0xff, Ox01},{0x12, Ox80},{0x3c, Ox32},{0x11, Ox00},{0x09,0x02},{0x04,Ox28},{0x13, Oxe5},{0x14, Ox48},{0x2c, Ox0c},{0x33, Ox78},{0x3a, Ox33},{0x3b, Oxfb},{0x3e, Ox00},{0x43, Ox11},{0x16, Ox10},{0x39, 0x02},{0x35, Ox88},{0x22, Ox0a},{0x37, Ox40},{0x23, Ox00},{0x34,   
Oxa0},{0x36,0x1a},{0x06, Ox02},{0x07, Oxc0}, {0x0d, Oxb7},{0x0e, Ox01},{0x4c, Ox00},{0x4a, Ox81},{0x21, Ox99},{0x24, Ox40},{0x25, 0x38},{0x26, 0x82}, {0x5c, Ox00},{0x63, Ox00},{0x46, Ox3f},{0x61, Ox70},{0x62, Ox80},{0x7c, Ox05}, {0x20, Ox80},{0x28, Ox30},{0x6c, Ox00},{0x6d, 0x80},{0x6e, Ox00},{0x70, Ox02},{0x71,Ox94},{0x73, Oxc1},{0x3d, 0x34},{0x5a, 0x57},{0x4f, Oxbb},{0x50, Ox9c},{0xff, Ox00},{0xe5, 0x7f},{0xf9, Oxc0},{0x41, 0x24},{Oxe0, Ox14},{0x76, Oxff},{0x33, Oxa0},{0x42, 0x20},{0x43, Ox18},{0x4c, Ox00},{0x87, Oxd0},{0x88, Ox3f},{0xd7, 0x03},{0xd9, Ox10},{0xd3, Ox82},{0xc8, Ox08},{0xc9, Ox80},{0x7c, 0x00}, {0x7d, 0x00},{0x7c, 0x03},{0x7d, 0x48},{0x7d, 0x48},{0x7c,0x08},{0x7d, Ox20},{0x7d, Ox10},{0x7d, Ox0e},{0x90, Ox00},{0x91, Ox0e},{0x91, Ox1a},{0x91, Ox31},{0x91, Ox5a},{0x91, 0x69},{0x91, Ox75},{0x91, Ox7e},{0x91, Ox88},{0x91, Ox8f},{0x91, Ox96}, {0x91, Oxa3},{0x91, Oxaf},{0x91, Oxc4},{0x91, Oxd7},{0x91, Oxe8},{0x91, Ox20},{0x92, Ox00},{0x93, Ox06},{0x93, Oxe3},{0x93, 0x05},{0x93, 0x05},{0x93, 0x00},{0x93, 0x04},{0x93, Ox00},{0x93, 0x00},{0x93, 0x00},{0x93, Ox00},{0x93, 0x00},{0x93, Ox00},{0x93, 0x00},{0x96, Ox00},{0x97, 0x08},{0x97, Ox19},{0x97, Ox02},{0x97, Ox0c},{0x97, 0x24},{0x97, 0x30},{0x97, 0x28},{0x97, Ox26},{0x97, 0x02},{0x97, 0x98},{0x97, 0x80},{0x97, 0x00},{0x97, Ox00},{Oxc3, Oxed},{0xc5, Ox11},{Oxc6, 0x51},{Oxbf, Ox80},{0xc7, Ox00},{0xb6, 0x66},{0xb8, OxA5},{0xb7, Ox64},{0xb9, Ox7C},{Oxb3, Oxaf},{0xb4, 0x97},{0xb5, OxFF},{Oxb0, OxC5},{Oxb1, 0x94},{Oxb2, Ox0f},{Oxc4, 0x5c},{Oxc0, Oxc8},{0xc1, Ox96},{0x86, Ox1d},{0x50, Ox00},{0x51, 0x90},{0x52, Ox18}, {0x53, Ox00},{0x54, 0x00},{0x55, Ox88},{0x57, 0x00},{0x5a, Ox90},{0x5b, Ox18}, {0x5c, 0x05},{Oxc3, Oxed},{0x7f, Ox00},{Oxda, Ox00},{0xe5, Ox1f},{Oxe1, 0x77},{Oxe0, Ox00},{0xdd, Ox7f},{0x05, Ox00},{0xFF, Ox00},{0x05, Ox00},{OxDA, Ox10},{0xD7, Ox03},{0xDF, Ox00},{0x33, Ox80},{0x3C, Ox40}, {0xe1, {0x00,Ox00} };

s s. I 0.c,invoid ov2640_Init(uint16_t DeviceAddr, uint32_t resolution),replace:

case CAMERA_R320x240:   
{   
for(index=0; index<(sizeof(OV2640_QVGA)/2); index++) {   
CAMERA_IO_Write(DeviceAddr, OV2640_QVGA[index][0], OV2640_QVGA[index][1]);   
CAMERA_Delay(1);   
break;   
}

# by

case CAMERA_R320x240:   
for(index=0; index<(sizeof( OV2640_JPEG)/2); index++) CAMERA_IO_Write(DeviceAddr, OV2640_JPEG[index] [0], OV2640_JPEG[index][1]);   
CAMERA_Delay(1);   
1   
break;   
}

# 9 Supported devices

To know if a CMOS sensor (a camera module) is compatible with the DCMI or not, the user must check the following points in the CMOS sensor specifications:

Parallel interface (8-, 10-, 12-, or 14-bit) Control signals (VSYNC, HSYNC, and PIXCLK) Supported pixel clock frequency output Supported data output

There is a wide range of camera modules and CMOS sensors that are compatible with the STM32 DCMI.   
The table below lists some of them.

Table 15. Examples of supported camera modules   

<table><tr><td rowspan=1 colspan=1>CMOS sensor</td><td rowspan=1 colspan=1>Camera module</td><td rowspan=1 colspan=1>Formats</td><td rowspan=1 colspan=1>Parallel interface</td></tr><tr><td rowspan=1 colspan=1>MT9D111</td><td rowspan=1 colspan=1>ArduCAM 2 megapixels</td><td rowspan=1 colspan=1>RGB, YCbCr, JPEG</td><td rowspan=1 colspan=1>10-bit</td></tr><tr><td rowspan=1 colspan=1>MT9P111</td><td rowspan=1 colspan=1>5 megapixels</td><td rowspan=1 colspan=1>RGB, YCbCr, JPEG</td><td rowspan=1 colspan=1>8-bit</td></tr><tr><td rowspan=1 colspan=1>NT99141</td><td rowspan=1 colspan=1>ArduCAM 1 megapixel</td><td rowspan=1 colspan=1>RGB, YCbCr, JPEG</td><td rowspan=1 colspan=1>8-bit</td></tr><tr><td rowspan=1 colspan=1>OV2640</td><td rowspan=1 colspan=1>ArduCAM 2 megapixels</td><td rowspan=1 colspan=1>RGB, YCbCr, JPEG</td><td rowspan=1 colspan=1>8-bit, 10-bit</td></tr><tr><td rowspan=1 colspan=1>OV3660</td><td rowspan=1 colspan=1>3 megapixels</td><td rowspan=1 colspan=1>RGB, YCbCr</td><td rowspan=1 colspan=1>8-bit, 10-bit</td></tr><tr><td rowspan=1 colspan=1>OV5640</td><td rowspan=1 colspan=1>ArduCAM 5 megapixels</td><td rowspan=1 colspan=1>RGB, YCbCr, JPEG</td><td rowspan=1 colspan=1>8-bit, 10-bit</td></tr><tr><td rowspan=1 colspan=1>OV5642</td><td rowspan=1 colspan=1>ArduCAM 5 megapixels</td><td rowspan=1 colspan=1>RGB, YCbCr, JPEG</td><td rowspan=1 colspan=1>8-bit, 10-bit</td></tr><tr><td rowspan=1 colspan=1>OV9655</td><td rowspan=1 colspan=1>ArduCAM 1.3 megapixels</td><td rowspan=1 colspan=1>RGB, YCbCr</td><td rowspan=1 colspan=1>8-bit</td></tr><tr><td rowspan=1 colspan=1>S5k4ECGX</td><td rowspan=1 colspan=1>5 megapixels</td><td rowspan=1 colspan=1>RGB, JPEG</td><td rowspan=1 colspan=1>10-bit</td></tr><tr><td rowspan=1 colspan=1>S5k5CAGA</td><td rowspan=1 colspan=1>3 megapixels</td><td rowspan=1 colspan=1>RGB, JPEG</td><td rowspan=1 colspan=1>10-bit</td></tr></table>

# 10 Conclusion

The DCMI represents an efficient interface to connect the camera modules to the STM32 MCUs supporting high speed, high resolutions, and a variety of data formats/widths.

Together with hevariey  peripherals and interaces integrated inTM32 MCUs and benefiting from theSTM32 smart architecture, the DCMl can be used in large and sophisticated imaging applications.

This application note covers the DCMI across the STM32 MCUs, providing allthe necessary information to cohe    pleentigapliatins arthecpatibl camel selection to detailed examples implementation.

# Revision history

Table 16. Document revision history   

<table><tr><td colspan="1" rowspan="2">Date</td><td colspan="3" rowspan="2">Version</td><td></td></tr><tr><td colspan="1" rowspan="3">ChangesInitial release.Updated:Table 1. Applicable productsTable 2. DCMI and related resources availabilitySection 3.2: DCMI in a smart architecture with all new productsTable 6. DCMI and camera modules on STM32 boardsSection 5.6.4: YCbCr, Y onlySection 5.8: Image resizing (resolution modification)Table 7. DCMI operation in low-power modesSection 6.4.1: DMA configuration for DCMI-to-memory transfersTable 8. DMA stream selection across STM32 devicesSection 6.4.4: DMA_SxNDTR/DMA_CNDTRx/GPDMA_CxBR1 registerTable 13. Maximum data flow at maximum DCMI_PIXCLKTable 14. STM32Cube DCMI examplesSection 8.3.2: Configuration of common examplesTable 15. Examples of supported camera modules</td></tr><tr><td colspan="1" rowspan="1">3-Aug-2017</td><td colspan="3" rowspan="1">1</td></tr><tr><td colspan="1" rowspan="1">17-Oct-2022</td><td colspan="3" rowspan="1">2</td></tr><tr><td colspan="1" rowspan="1"></td><td colspan="3" rowspan="6"></td><td colspan="1" rowspan="10">Updated:Table 1. Applicable productsTable 2. DCMI and related resources availabilityFigure 7. DCMI slave AHB2 peripheral in the STM32F4Figure 8. DCMI slave AHB2 peripheral in the STM32F7Figure 9. DCMI slave AHB2 peripheral in the STM32H723/733, STM32H743/753,STM32H742, STM32H725/735, STM32H730, and STM32H750 devicesFigure 10. DCMI slave AHB2 peripheral in the STM32H745/755 and STM32H747/757devicesFigure 11. DCMI slave AHB2 peripheral in the STM32H7A3/B3Figure 12. DCMI slave AHB2 peripheral in STM32L496/4A6Figure 13. DCMI slave AHB2 peripheral in the STM32L4+Table 6. DCMI and camera modules on STM32 boardsFigure 17. DCMI block diagram: example of 12-bit data widthSection 6.4: DMA configurationTable 9. DMA stream selection across STM32 devicesTable 13. Maximum data flow at maximum DCMI_PIXCLKSection 3.2.4.3: STM32H7A3/7B3 devicesAdded:Section 3.2.8: STM32H5 system architectureSection 3.2.7: STM32U5 system architecture</td></tr><tr><td colspan="1" rowspan="1"></td></tr><tr><td colspan="1" rowspan="1"></td></tr><tr><td colspan="1" rowspan="2"></td></tr><tr><td colspan="2" rowspan="1"></td></tr><tr><td colspan="1" rowspan="1"></td><td colspan="2" rowspan="1"></td></tr><tr><td colspan="1" rowspan="1">24-Feb-2023</td><td colspan="2" rowspan="1"></td><td colspan="1" rowspan="4">3</td></tr><tr><td colspan="1" rowspan="1"></td><td></td><td></td></tr><tr><td colspan="1" rowspan="1"></td><td></td><td></td></tr><tr><td colspan="1" rowspan="1"></td><td></td><td></td></tr><tr><td colspan="1" rowspan="1">20-Nov-2024</td><td colspan="3" rowspan="1">4</td><td colspan="1" rowspan="1">Document updated to add STM32H523/533 line and STM32N6 series to the scope of thisdocument.</td></tr><tr><td>Date</td><td colspan="3">Version</td><td>Changes</td></tr><tr><td></td><td colspan="3"></td><td>Updated: Table 1. Applicable products: add new products in the scope of the document Section 2.1: Basic imaging concepts: title updated, and typos corrected inside the section Section 3.1: DCMI availability and features across STM32 MCUs: Table 2 Section 3.2: DCMI in a smart architecture Section 3.2.4.1: STM32H7x3, STM32H742, STM32H725/735, STM32H730, and STM32H750 devices Section 3.2.5: STM32L4 system architecture Section 3.2.6: STM32L4+ system architecture including Figure 13. DCMI slave AHB2 peripheral in the STM32L4+ Section 3.2.7: STM32U5 system architecture Section 3.2.8: STM32H5 system architecture CMOS senSors for STM32H7B3I-EVAL and STM32U575I-EVAL in Table 6. DCMI and camera modules on STM32 boards Figure 17. DCMI block diagram: example of 12-bit data width Section 5.6: Data formats and storage Section 5.6.4: YCbCr, Y only Section 5.8: Image resizing (resolution modification) Table 7. DCMI operation in low-power modes Section 6.4: DMA configuration Section 6.4.1: DMA configuration for DCMI-to-memory transfers</td></tr></table>

# Contents

#

# 1 General information

# 2 Camera modules and basic concepts 3

2.1 Basic imaging concepts 3

2.2 Camera module. 4

2.2.1 Camera module components 4   
2.2.2 Camera module interconnect (parallel interface). . 5

# STM32 DCMI overview 6

3.1 DCMI availability and features across STM32 MCUs. 6

3.1.1 Availability of DCMl and related resources_ topic for table rotation.

# .2 DCMI in a smart architecture. 9

3.2.1 STM32F2 system architecture 9   
3.2.2 STM32F4 system architecture .9   
3.2.3 STM32F7 system architecture 11   
3.2.4 STM32H7 system architecture 13   
3.2.5 STM32L4 system architecture. 16   
3.2.6 STM32L4+ system architecture. 17   
3.2.7 STM32U5 system architecture 18   
3.2.8 STM32H5 system architecture 20   
3.2.9 STM32N6 system architecture 21

# 1 Reference boards with DCMI and/or camera modules 22

# 5 DCMI description .24

5.1 Hardware interface 24   
5.2 Camera module and DCMI interconnection. 27   
5.3 DCMI functional description 27

5.4 Data synchronization 27

5.4.1 Hardware (or external) synchronization. 27   
5.4.2 Embedded (or internal) synchronization 28

# 5.5 Capture modes 31

5.5.1 Snapshot mode. 31   
5.5.2 Continuous grab mode 31

5.6 Data formats and storage. 32

5.6.1 Monochrome. 33

5.6.2 RGB565 33

5.6.3 YCbCr. 33

5.6.4 YCbCr, Y only 34

# 5.6.5 JPEG 34

5.7 Crop feature. 34   
5.8 Image resizing (resolution modification) . . 35   
5.9 DCMI interrupts . 35   
5.10 Low-power modes. 36

# DCMI configuration .38

6.1 GPIO configuration 38

# 6.2 Clock and timing configuration. 38

6.2.1 System clock configuration (HCLK). 38   
6.2.2 DCMI clock and timing configuration (DCMI_PIXCLK) 39

# 3 DCMI configuration 41

6.3.1 Capture mode selection 41   
6.3.2 Data format selection 41   
6.3.3 Image resolution and size . 41

# i.4 DMA configuration. 42

6.4.1 DMA configuration for DCMI-to-memory transfers. 42   
6.4.2 DMA configuration versus image size and capture mode 43   
6.4.3 DCMI channel and stream configuration . 43   
6.4.4 DMA_SxNDTR/DMA_CNDTRx/GPDMA_CxBR1 register. 44   
6.4.5 FIFO and burst transfer configuration 45   
6.4.6 Normal mode for low resolution in snapshot capture. 45   
6.4.7 Circular mode for low resolution in continuous capture. 45   
6.4.8 Double-buffer mode for medium resolutions (snapshot or continuous capture). 46   
6.4.9 DMA configuration for higher resolutions. 47

# 6.5 Camera module configuration 49

# Power consumption and performance. .50

7.1 Power consumption 50   
7.2 Performance .50

# DCMI application examples 52

8.1 DCMI use cases 52

8.2 STM32Cube examples 53

# 8.3 DCMI examples based on STM32CubeMX. 53

8.3.1 Hardware description 55   
8.3.2 Configuration of common examples 57   
8.3.3 RGB data capture and display 68   
8.3.4 YCbCr data capture 68   
8.3.5 Y only data capture. 69

8.3.6 Resolution capture (YCbCr data format) 70

8.3.7 JPEG data capture 72

3 Supported devices. 74

10 Conclusion 75

Revision history 76

List of tables .81

List of figures.. .82

# List of tables

Table 1. Applicable products   
Table 2. Availability of DCMI and related resources   
Table 3. SRAM availability in the STM32F4 series 11   
Table 4. SRAM availability in the STM32H723/733, STM32H743/753, STM32H742, STM32H725/735, STM32H730, and   
STM32H750 devices 15   
Table 5. SRAM availability in the STM32U5 devices . 20   
Table 6. DCMI and camera modules on STM32 boards. 22   
Table 7. DCMI operation in low-power modes 37   
Table 8. DMA stream selection across STM32 devices 44   
Table 9. DMA stream selection across STM32 devices 44   
Table 10. Maximum number of bytes transferred during one DMA transfer 44   
Table 11. Maximum image resolution in normal mode. 45   
Table 12. Maximum image resolution in double-buffer mode 46   
Table 13. Maximum data flow at maximum DCMI_PIXCLK 50   
Table 14. STM32Cube DCMI examples 53   
Table 15. Examples of supported camera modules. 74   
Table 16. Document revision history . 76

# List of figures

Figure 1. Original versus digital image. 3   
Figure 2. Horizontal blanking illustration 3   
Figure 3. Vertical blanking illustration 4   
Figure 4. Camera module examples 4   
Figure 5. Interfacing a camera module with an STM32 MCU 5   
Figure 6. DCMI slave AHB2 peripheral in the STM32F2x7. 9   
Figure 7. DCMI slave AHB2 peripheral in the STM32F4 10   
Figure 8. DCMI slave AHB2 peripheral in the STM32F7 12   
Figure 9. DCMI slave AHB2 peripheral in the STM32H723/733, STM32H743/753, STM32H742, STM32H725/735,   
STM32H730, and STM32H750 devices 14   
Figure 10. DCMI slave AHB2 peripheral in the STM32H745/755 and STM32H747/757 devices 15   
Figure 11. DCMI slave AHB2 peripheral in the STM32H7A3/B3 16   
Figure 12. DCMI slave AHB2 peripheral in STM32L496/4A6 17   
Figure 13. DCMI slave AHB2 peripheral in the STM32L4+. 18   
Figure 14. DCMI slave AHB2 peripheral in the STM32U5 devices 19   
Figure 15. DCMI slave AHB2 peripheral for the STM32H562 and STM32H563/573 20   
Figure 16. DCMI signals . 24   
Figure 17. DCMI block diagram: example of 12-bit data width 25   
Figure 18. Data register filed for 8-bit data width 26   
Figure 19. Data register filled for 10-bit data width 26   
Figure 20. Data register filled for 12-bit data width 26   
Figure 21. Data register filled for 14-bit data width 26   
Figure 22. STM32 MCU and camera module interconnection. 27   
Figure 23. Frame structure in hardware synchronization mode. 28   
Figure 24. Embedded code bytes. 28   
Figure 25. Frame structure in embedded synchronization mode 1 29   
Figure 26. Frame structure in embedded synchronization mode 2 30   
Figure 27. Embedded code unmasking. 30   
Figure 28. Frame reception in snapshot mode 31   
Figure 29. Frame reception in continuous grab mode 32   
Figure 30. Pixel raster scan order. 32   
Figure 31. DCMI data register filled with monochrome data 33   
Figure 32. DCMI data register filled with RGB data . 33   
Figure 33. DCMI data register filled with YCbCr data 33   
Figure 34. DCMI data register filled with Y only data 34   
Figure 35. JPEG data reception. 34   
Figure 36. Frame resolution modification. 35   
Figure 37. DCMI interrupts and registers . 36   
Figure 38. DCMI_ESCR register bytes 39   
Figure 39. FEC structure. 39   
Figure 40. LEC structure . 40   
Figure 41. FSC structure. 40   
Figure 42. LSC structure . 40   
Figure 43. Frame structure in embedded synchronization mode 41   
Figure 44. Data transfer through the DMA . 43   
Figure 45. Frame buffer and DMA_SxNDTR register in circular mode 46   
Figure 46. Frame buffer and DMA_SxNDTR register in double-buffer mode. 47   
Figure 47. DMA operation in high resolution case. 48   
Figure 48. STM32 DCMI application example 52   
Figure 49. Data path in capture and display application. 54   
Figure 50. 32F746GDISCOVERY and STM32F4DIS-CAM interconnection 55   
Figure 51. Camera connector on 32F746GDISCOVERY 56   
Figure 52. Camera connector on STM32F4DIS-CAM 57   
Figure 53. STM32CubeMX - DCMI synchronization mode selection 58   
Figure 54. STM32CubeMX - GPIO settings selection 58   
Figure 55. STM32CubeMX - DCMI pin selection 59   
Figure 56. STM32CubeMX - GPIO no pull-up and no pull-down selection 59   
Figure 57. STM32CubeMX - Parameter Settings tab. 59   
Figure 58. STM32CubeMX - DCMI control signals and capture mode 59   
Figure 59. STM32CubeMX - Configuration of DCMI interrupts 60   
Figure 60. STM32CubeMX - DMA Settings tab 60   
Figure 61. STM32CubeMX - Add button 60   
Figure 62. STM32CubeMX - DMA stream configuration 60   
Figure 63. STM32CubeMX - DMA configuration. 61   
Figure 64. STM32CubeMX - PH13 pin configuration . 61   
Figure 65. STM32CubeMX - GPIO button . 61   
Figure 66. STM32CubeMX - DCMI power pin configuration . 62   
Figure 67. STM32CubeMX - HSE configuration 62   
Figure 68. STM32CubeMX - Clock configuration 63

# IMPORTANT NOTICE  READ CAREFULLY

pt old ursant  dits   leole.

purchasers' products.

No license, express or implied, to any intellectual property right is granted by ST herein.

are the property of their respective owners.

I

© 2024 STMicroelectronics - All rights reserved