# How to use Chrom-ART Accelerator to refresh an LCD-TFT display on STM32 MCUs

# Introduction

Chrom-ART Accelerator on STM32 microcontrollers listed in the table below.

This Chrom-ART Accelerator (DMA2D) is a specialized DMA dedicated to image manipulation.

The DMA2D can perform the following operations:

Fill a part or the whole of a destination image with a specific color.   
Be whole of a destination image with a different color format.

On STM32 microcontrolers, the FMC is used to access the LCD-TFT display through a parallel interface.

This application note explains how to:

Connect the LCD-TFT display to the FMC interface   
Configure the DMA2D for the LCD-TFT display refresh   
Use the DMA2D byte reordering features to directly drive Intel 8080 displays

Chrom-ART Accelerator (DMA2D).

Table 1. Applicable products   

<table><tr><td rowspan=1 colspan=1>Type</td><td rowspan=1 colspan=1>Applicable products</td></tr><tr><td rowspan=4 colspan=1>Microcontrollers</td><td rowspan=1 colspan=1>STM32L4x6 line</td></tr><tr><td rowspan=1 colspan=1>STM32L4R5/S5 line, STM32L4R7/S7 line, STM32L4R9/S9 line</td></tr><tr><td rowspan=1 colspan=1>STM32U5 series</td></tr><tr><td rowspan=1 colspan=1>STM32H7 series</td></tr></table>

# 1 General information

# Note:

This application note applies to STM32 microcontrollers Arm®-based devices.   
Arm is a registered trademark of Arm Limited (or its subsidiaries) in the US and/or elsewhere.

# arm

# Reference documents

Reference manual STM32L4x6 advanced Arm®-based 32-bit MCUs (RM0351)   
Reference manual STM32L4Rxx/L4Sxxx advanced Arm®-based 32-bit MCUs (RM0432)   
Reference manual STM32U5 series Arm ®-based 32-bit MCUs (RM0456)   
Reference manual STM32H7Rx/Sx Arm ®-based 32-bit MCUs (RM0477)   
User manual Discovery kit with STM32L496AG MCU (UM2160)   
User manual Getting started with STM32CubeL4 MCU Package for STM32L4 Series and STM32L4+   
Series (UM1860)

All documents are available on www.st. com.

# 2 Chrom-ART Accelerator (DMA2D) application use case overview

A typical application displaying an image into an LCD-TFT display is divided in two steps.

Step 1: creation of the frame buffer content:

The frame buffer is built by composing graphical primitives like icons, pictures and fonts.   
This operation is done by the CPU running a graphical library software.   
It can be accelerated by a dedicated hardware used with the CPU through the graphical library (Chrom-ART Accelerator (DMA2D)).   
The more often the frame buffer is updated, the more fluid are the animations.

Step 2: display of the frame buffer onto the LCD-TFT display:

The frame buffer is transferred to the display through a dedicated hardware interface. The transfer can be done using the CPU, the system DMA or using the Chrom-ART Accelerator (DMA2D).

In a typical display application example using he STM32 micocontrollers, the F(S)C is used as the harwae Quad-SPI flash memory and the frame buffer is stored in the internal SRAM. The Chrom-ART Accelerator AD)naloana ens eme bufhe LCD-Fiuusig PU  DMA resources.

The figure below shows this use case.

![](images/05e70ac0f431139b7b60a3ab7f92d162aba5ab2079332a176ad2822d41280c2e.jpg)  
Figure 1. Display application typical use case

For STM32H7R7/7S7 devices, which are boot flash MCUs with limited internal memory, to achieve steps 1 and 2 as shown in the figure below, the user must add external memories (flash and RAM).

![](images/f2213589dc72cd94b5a96356984808e2ba52d44b1c4a76a5bb578f08cb39e780.jpg)  
Figure 2. STM32H7R7/7S7 display application use case

TRa Aholu (partial refresh).

TheChrom-ART Accelerator (DMA2D) is configured (fullor partial refresh) by programming specific registers through the high-level HAL library function, as shown in Section 4: Chrom-ART Accelerator (DMA2D) configuration in STM32CubeL4.

# 3

# LCD-TFT display on F(S)MC

# 3.1

# Hardware interface description

Signals in the table below are used to connect the F(S)MC to the LCD-TFT display

Table 2. F(S)MC signals   

<table><tr><td rowspan=1 colspan=1>Signal name</td><td rowspan=1 colspan=1>F(S)MC I/O</td><td rowspan=1 colspan=1>Function</td></tr><tr><td rowspan=1 colspan=1>A[25:0]</td><td rowspan=1 colspan=1>O</td><td rowspan=1 colspan=1>Address bus</td></tr><tr><td rowspan=1 colspan=1>D[15:0]</td><td rowspan=1 colspan=1>I/O</td><td rowspan=1 colspan=1>Bidirectional data bus</td></tr><tr><td rowspan=1 colspan=1>NE[X]</td><td rowspan=1 colspan=1>O</td><td rowspan=1 colspan=1>Chip select, x=1.4</td></tr><tr><td rowspan=1 colspan=1>NOE</td><td rowspan=1 colspan=1>O</td><td rowspan=1 colspan=1>Output enable</td></tr><tr><td rowspan=1 colspan=1>NWE</td><td rowspan=1 colspan=1>O</td><td rowspan=1 colspan=1>Write enable</td></tr></table>

Ibeo  y B the MIP® Alliance standard for display bus interface.

Table 3. LCD-TFT signals   

<table><tr><td rowspan=1 colspan=1>Signal name</td><td rowspan=1 colspan=1>LCD-TFT I/O</td><td rowspan=1 colspan=1>Function</td></tr><tr><td rowspan=1 colspan=1>DICX</td><td rowspan=1 colspan=1>I</td><td rowspan=1 colspan=1>Data/command control signal</td></tr><tr><td rowspan=1 colspan=1>D[15:0]</td><td rowspan=1 colspan=1>I/O</td><td rowspan=1 colspan=1>Bidirectional information signals bus</td></tr><tr><td rowspan=1 colspan=1>CSx</td><td rowspan=1 colspan=1>I</td><td rowspan=1 colspan=1>Chip select control signal</td></tr><tr><td rowspan=1 colspan=1>RDX</td><td rowspan=1 colspan=1>I</td><td rowspan=1 colspan=1>Read control signal</td></tr><tr><td rowspan=1 colspan=1>WRX</td><td rowspan=1 colspan=1>I</td><td rowspan=1 colspan=1>Write control signal</td></tr><tr><td rowspan=1 colspan=1>TE</td><td rowspan=1 colspan=1>O</td><td rowspan=1 colspan=1>Tearing effect</td></tr><tr><td rowspan=1 colspan=1>RESX</td><td rowspan=1 colspan=1></td><td rowspan=1 colspan=1>Reset</td></tr></table>

The figure below shows a typical connection.

![](images/c92246bc1dbe27fa3f8f7ac32af2e0198aec457ff5ed82232706c7b2bae32c02.jpg)  
Figure 3. Display bus interface specification

# 3.2

# Display command set (DcS) software interface

The LCD-TFT displays can becntrolled through he physical interace (here he F(S)MC bus) using sotwae commands according to the display command set (DS), as defined in the MIP Alliance specification orDCS.

T n gule ana ufe

# Controlling the D/CX signal with STM32 microcontrollers

The data/command control (D/CX) signal of the DBI protocol is used t distinguish the commands (when D/CX = 0) from the data (when D/CX = 1) transfers.

There are two ways to control the D/CX signal:

Set the D/CX signal in "command mode" (setting the GPIO connected to the D/CX signal to 0 by software).   
2. Send the command.   
Set the D/CX signal in "data mode" (setting the GPIO connected to the D/CX signal to 1 by software). Send the data (frame buffer).   
By using an address bit of the F(S)MC address bus:   
Reserve a "low-level" address in the memory map for the command transfer.   
Reserve the higher memory map range for the data transfer.

Whenusing the DMA2D to access the LCD-TFT display on F(S)MC interface, remember that even if the LCD-TFT ispayargeit fidresseMAenthedress uhenitdat accs (like memory-to-memory acces).Thus, the F(S)C address bus is incremented t cover the full data range address in the memory map.

![](images/5a2465deeae63ec1e0f7404554a09d4de6f0fe69d06d39cbc4c929a10125722a.jpg)  
Figure 4. Memory map for LCD-TFT display access

Tptin   he F(Cs makeoape han e -voa

The user cannot use, for example, the F(S)MC address LSB bit (F(S)MCA0) to control the "data or command the entire image frame buffer transfer.

![](images/bc6a95cb13b6b889862c4913aa4911cc17904ee1601779bc96e5e325e63f8bb9.jpg)  
Figure 5. Automatic control of LCD-TFT display data/command by F(S)MC interface

# 1x' as high as possible according to Table 4.

Foaple eae bufis   pi andhes isi R (one pixel transferred per access to LCD), the number of accesses are 240 x 240 = 57600 accesses and the F(S)MC address increments from Ox0000 0000 to 0x0000 EOFF.

Thu the  adres bit that does ot changeurig he ransethe  In thi pecicase F(S)MC_A16 or a higher address bit can be used.

# The table below shows the minimum F(S)MC adress bit that can be used depending on some image size.

Table 4. Minimum F(S)MC address bit to use depending on image size (16-bit RGB565 access)   

<table><tr><td rowspan=1 colspan=1>Image size</td><td rowspan=1 colspan=1>Number of pixels</td><td rowspan=1 colspan=1>Number of accesses</td><td rowspan=1 colspan=1>Max address</td><td rowspan=1 colspan=1>Min usable FSMCaddress bit</td></tr><tr><td rowspan=1 colspan=1>VGA</td><td rowspan=1 colspan=1>640 x 480</td><td rowspan=1 colspan=1>307200</td><td rowspan=1 colspan=1>0x4AFFF</td><td rowspan=1 colspan=1>F(S)MC_A19</td></tr><tr><td rowspan=1 colspan=1>HVGA</td><td rowspan=1 colspan=1>480 x 320</td><td rowspan=1 colspan=1>153600</td><td rowspan=1 colspan=1>0x257FF</td><td rowspan=1 colspan=1>F(S)MC_A18</td></tr><tr><td rowspan=1 colspan=1>QVGA</td><td rowspan=1 colspan=1>320 x 240</td><td rowspan=1 colspan=1>76800</td><td rowspan=1 colspan=1>0x12BFF</td><td rowspan=1 colspan=1>F(S)MC_A17</td></tr><tr><td rowspan=1 colspan=1>-</td><td rowspan=1 colspan=1>240 x 240</td><td rowspan=1 colspan=1>57600</td><td rowspan=1 colspan=1>0x0EOFF</td><td rowspan=1 colspan=1>F(S)MC_A16</td></tr></table>

# 4 Chrom-ART Accelerator (DMA2D) configuration in STM32CubeL4

# 4.1

# LCD partial refresh

An example configuring the DMA2D for an LCD partial refresh is provided in the following folder: STM32Cube_FW_L4\Firmware\Projects\STM32L496G-Discovery\Examples\DMA2D\ DMA2D_MemToMemWithLCD.

# The code used to configure and start the DMA2D is shown below.

/\* Configure LcD before image display: set first pixel position and image size \*/   
/\* the position of the partial refreshed window is defined here. A rectangle in the middle of the screen \*/   
LCD_ImagePreparation((ST7789H2_LCD_PIXEL_WIDTH - LAYER_SIZE_X)/2,   
(ST7789H2_LCD_PIXEL_HEIGHT - LAYER_SIZE_Y)/2, LAYER_SIZE_x,¯LAYER_SIZE_Y); /\*##-2- DMA2D configuration   
###################\*############################\*/   
DMA2D_Config();   
/\*##-3- Start DMA2D transfer   
###############################################\*/   
hal_status = HAL_DMA2D_Start_IT(&Dma2dHandle,   
(uint32_t)&RGB565_240x160, /\* Source buffer in format RGB565 and size 240x160\~\*/   
(uint32_t)&(LCD_ADDR->REG), /\* LCD data address \*/   
1, LAYER_SIZE_Y¯\* LAYER_SIZE_X); /\* number of pixel to transfer \*/   
OnError_Handler(hal_status != HAL_OK);   
/\*\*   
\* @brief DMA2D configuration.   
@note This function configure the DMA2D peripheral   
1) Configure the transfer mode : memory to memory   
2) Configure the output color mode as RGB565   
3) Configure the transfer from FLASH to SRAM   
4) Configure the data size : 240x160 (pixels)   
@retval   
\* None   
static void DMA2D_Config(void)   
HAL_StatusTypeDef hal_status = HAL_OK;   
/\* Configure the DMA2D Mode, color Mode and output offset \*/   
Dma2dHandle.Init.Mode = DMA2D_M2M; /\* DMA2D Mode memory to memory \*/   
Chrom-ART AcceleratorM (DMA2D) configuration in STM32CubeL4 AN4943   
12/22 DocID029937 Rev 2   
Dma2dHandle.Init.ColorMode = DMA2D_OUTPUT_RGB565; /\* Output color mode is RGB565: 16 bpp \*/   
Dma2dHandle.Init.OutputOffset = Ox0; /\* No offset in output \*/   
Dma2dHandle.Init.RedBlueSwap = DMA2D_RB_REGULAR; /\* No R&B Swap for   
the output image \*/   
Dma2dHandle.Init.AlphaInverted = DMA2D_REGULAR_ALPHA; /\* No alpha   
inversion for the output image \*/ /\* DMA2D Callbacks configuration \*/   
Dma2dHandle.XferCpltCallback = TransferComplete;   
Dma2dHandle.XferErrorCallback = TransferError;   
/\* Foreground configuration: Layer 1 \*/   
Dma2dHandle.LayerCfg[1].AlphaMode = DMA2D_NO_MODIF_ALPHA;   
Dma2dHandle.LayerCfg[1].InputAlpha = OxFF; /\* Fully opaque \*/   
Dma2dHandle.LayerCfg[1].InputColorMode = DMA2D_INPUT_RGB565; /\* Foreground layer format is RGB565 : 16 bpp \*/   
Dma2dHandle.LayerCfg[1].InputOffset = Ox0; /\* No offset in input \*/ Dma2dHandle.LayerCfg[1].RedBlueSwap = DMA2D_RB_REGULAR; /\* No R&B   
swap for the input foreground image \*/   
Dma2dHandle.LayerCfg[1].AlphaInverted = DMA2D_REGULAR_ALPHA; /\* No alpha inversion for the input foreground image \*/ Dma2dHandle.Instance = DMA2D;   
/\* DMA2D initialization \*/   
hal_status = HAL_DMA2D_Init(&Dma2dHandle);   
OnError_Handler(hal_status != HAL_OK);   
hal_status = HAL_DMA2D_ConfigLayer(&Dma2dHandle, 1); OnError_Handler(hal_status != HAL_OK);   
}

yz the LCD size.

LCD_ImagePreparation(O, 0, ST7789H2_LCD_PIXEL_WIDTH, ST7789H2_LCD_PIXEL_HEIGHT);

# Changing the number of pixels to be transferred in the DMA2D start command:

hal_status = HAL_DMA2D_Start_IT(&Dma2dHandle,   
(uint32_t)&RGB565_240x240, /\* Source buffer in format RGB565 and size 240x240\~\*/   
(uint32_t)&(LCD_ADDR->REG), /\* LCD data address \*/   
1, ST7789H2_LCD_PIXEL_HEIGHT \* ST7789H2_LCD_PIXEL_WIDTH); /\* number of pixel to transfer \*/   
OnError_Handler(hal_status != HAL_OK);

# 5 New DMA2D features to support Intel 8080 displays

Ool e pil atohbueo tendr n highest address.

For example: in case of the RGB888 pixel format, the blue component is stored at address 0 while the red component is stored at address 2.

W which is the blue component in this example.

Ths creates a mismatch with some Intel 8080 LCD displaycolorcoding which requires themost significant byte to be transmitted first (red component in case of the RGB888 pixel format).

Ta et  i through the F(S)MC.

A oAO tdrectly drive the LCD displays from a frame buffer with aclassic RGB order without any extra sowae manipulation.

# 5.1

# Intel 8080 interface color coding

e u 16 and 18-bit bus.

This section shows the Intel 808 display color coding that creates a mimatch with a classcRGBordee STM32 memory. Various cases are detailed below:

24 bpp (16.7M colors) and 18 bpp (262k colors) over 16-bit interface   
The figure below shows the color coding for transmittng 4 p data over a 1-bit bus interface n Intel 8080 displays.

![](images/0d4d72c37ae3c0fad96b07cf5914b50fc93be975bec7e56c60554aa6590b598b.jpg)  
Figure 6. 24 bpp over 16-bit interface color coding

# Note:

The 18 bpp displays have the same color coding except that in case of 18 bpp, R/G/B[6:0] are placed in the most significant bits of the bus and the data lines D9, D8, D1 and D0 are ignored.

16 bpp (64k colors) over 8-bit interface The figure below shows the pixel color coding for 16 bpp displays over an 8-bit bus interface.

![](images/89ae4f74196b9e26088f581a8d89f3d75c01ec9d3c6333204773a907b72723b6.jpg)  
Figure 7. 16 bpp over 8-bit interface color coding

24 bpp (16.7M colors) and 18 bpp (262k colors) over 8-bit interface The figure below shows the pixel color coding for 24 bpp over an 8-bit bus interface.

![](images/8a6dc0b4b7707da58ed55ec0515d3b63394bbebe4f211fefd27cf0344f177167.jpg)  
Figure 8. 24 bpp over 8-bit interface color coding

# Note:

The 18 bpp displays have the same color coding except that in case of 18 bpp, R/G/B[6:0] are placed in the most significant bits of the bus and the data lines D9, D8, D1 and D0 are ignored.

# 5.2

# DMA2D reordering features

TAutut yt an eorerport espame bufpda le interace (F(S)C) directl rom the DMA2.The user can do combination  reorderig operations to get the right byte endianness aligned with the display color coding.

# 5.2.1 Red and blue swap

The red and blue components can be swapped by setting the RBS bit in DMA2DOPFCCR.This feature exists in all products stated in Table 1.

# 5.2.2

# Byte swap

The MSB and the LSB bytes of a half-word can be swapped in the output FIFO by setting the SB bit in DMA2D_OPFCCR.

This feature exists in all products stated in Table 1 except STM32L4 series.

The table below shows the swap operations required to match the LCD display color coding depending on the display color depth and the bus interface width.

Table 5. Swap operations   

<table><tr><td rowspan=2 colspan=1>Color depth</td><td rowspan=2 colspan=1>Interface bus width</td><td rowspan=1 colspan=2>Required operation</td></tr><tr><td rowspan=1 colspan=1>Red blue swap</td><td rowspan=1 colspan=1>Byte swap</td></tr><tr><td rowspan=2 colspan=1>8 bpp (256 colors)</td><td rowspan=1 colspan=1>8-bit</td><td rowspan=1 colspan=1>No</td><td rowspan=1 colspan=1>No</td></tr><tr><td rowspan=1 colspan=1>16-bit</td><td rowspan=1 colspan=1>No</td><td rowspan=1 colspan=1>Yes</td></tr><tr><td rowspan=2 colspan=1>16 bpp (64k colors)</td><td rowspan=1 colspan=1>8-bit</td><td rowspan=1 colspan=1>No</td><td rowspan=1 colspan=1>Yes</td></tr><tr><td rowspan=1 colspan=1>16-bit</td><td rowspan=1 colspan=1>No</td><td rowspan=1 colspan=1>No</td></tr><tr><td rowspan=2 colspan=1>18 bpp (262k colors)</td><td rowspan=1 colspan=1>8-bit</td><td rowspan=1 colspan=1>Yes</td><td rowspan=1 colspan=1>No</td></tr><tr><td rowspan=1 colspan=1>16-bit</td><td rowspan=1 colspan=1>Yes</td><td rowspan=1 colspan=1>Yes</td></tr><tr><td rowspan=2 colspan=1>24 bpp (16.7M colors)</td><td rowspan=1 colspan=1>8-bit</td><td rowspan=1 colspan=1>Yes</td><td rowspan=1 colspan=1>No</td></tr><tr><td rowspan=1 colspan=1>16-bit</td><td rowspan=1 colspan=1>Yes</td><td rowspan=1 colspan=1>Yes</td></tr></table>

# 5.3

# DMA2D reordering use case examples

# 5.3.1

# 24 bpp/18 bpp over 16-bit F(S)MC data bus interface

Inoer sort isplas usig e 0 sandar toperatins erequie n he rame uf data:

Red and blue swap MSB and LSB bytes of a half-word swap

The figure below shows he operations performed by the DMA2D tohave the good byte ordercorrespondng t the Intel 8080 protocol for 24-bpp color depth over a 16-bit interface.

![](images/94c66257e6172c2f5f86ea7877551e73d39b4725e7a43ff37cdcde0c1939a2bb.jpg)  
Figure 9. DMA2D operations to support 24 bpp over 16-bit interface

# Note:

On MCUs ot supporting the bye swap, ahardware i can e mplemented by swapping the data lines the LCD itec n the boar.he ispay D[1:8] nes e o  he F)C D[:0] ies and thepy D[7:0] lines are connected to the F(S)MC D[15:8] lines.

# 5.3.2

# 24 bpp/18 bpp over 8-bit F(S)MC data bus interface

T  p  . Te igure below shows heeand blue swap peratn done byhe DA2allowing havehe good byes order.

![](images/3a7449c69d3fe9ea5b07d753b4760475f915f67e0d8c5c7c109984d6fc4f80e2.jpg)  
Figure 10. DMA2D operations to support 24 bpp over 8-bit interface

# 5.3.3

# 16 bpp over 8-bit F(S)MC data bus interface

I  ve ey be swapped.

The figure below shows how the swap operation allows having the good bytes order.

![](images/b8ac411c369aafb043ee08ce71b065662d1f79310e39bf5a902ef03545d55a94.jpg)  
Figure 11. DMA2D operations to support 16 bpp over 8-bit interface

# 6 Conclusion

This application note explains how to easilytransermages to an LCD-TFT display via the F(S)MCinteace uig theChrom-ART Accelerator (DMA2D), withot using the PU or the DMA resources. focu is given the correct control of the D/CX signal of the LCD-TFT display. Some code examples are provided to setup the DMA2D.

Thi document presents he new byte reordering features the DMA2D used  support aupdate  1.7M and 262k color Intel 8080 displays directly through the F(S)MC.

# Revision history

Table 6. Document revision history   

<table><tr><td>Date</td><td>Revision</td><td>Changes</td></tr><tr><td>27-Jan-2017</td><td>1</td><td>Initial release.</td></tr><tr><td>23-Oct-2017</td><td>2</td><td>Added STM32L4Rxxx/L4Sxxx devices in the whole document. Added Section 5: New DMA2D features to support Intel 8080 displays.</td></tr><tr><td rowspan="6">23-Sept-2021</td><td rowspan="6">3</td><td></td></tr><tr><td>Updated:</td></tr><tr><td>Document title</td></tr><tr><td>Table 1. Applicable products Section 5.2.1 Red and blue swap</td></tr><tr><td>Section 5.2.2 Byte swap</td></tr><tr><td>Name of devices in the whole document</td></tr><tr><td rowspan="6">22-Mar-2024</td><td rowspan="6">4</td><td>Updated:</td></tr><tr><td>Table 1. Applicable products</td></tr><tr><td>Section 5.2.1: Red and blue swap</td></tr><tr><td>Section 5.2.2: Byte swap</td></tr><tr><td>Terminology updated.</td></tr><tr><td>Applicable products updated.</td></tr><tr><td>10-Dec-2024</td><td>5</td><td>Updated Section 2: Chrom-ART Accelerator (DMA2D) application use case overview.</td></tr></table>

# Contents

# 1 General information

# 2 Chrom-ART Accelerator (DMA2D) application use case overview .

# 3 LCD-TFT display on F(S)MC. 5

3.1 Hardware interface description 5   
3.2 Display command set (DCS) software interface 6   
3.3 Controlling the D/CX signal with STM32 microcontrollers . 6

# Chrom-ART Accelerator (DMA2D) configuration in STM32CubeL4 9

4.1 LCD partial refresh 9

# New DMA2D features to support Intel 8080 displays . 11

5.1 Intel 8080 interface color coding 12

5.2 DMA2D reordering features. 14

5.2.1 Red and blue swap. 14   
5.2.2 Byte swap . 14

# 5.3 DMA2D reordering use case examples 15

5.3.1 24 bpp/18 bpp over 16-bit F(S)MC data bus interface . . 15   
5.3.2 24 bpp/18 bpp over 8-bit F(S)MC data bus interface. 16   
5.3.3 16 bpp over 8-bit F(S)MC data bus interface. 17

# 6 Conclusion 18

# Revision history 19

# List of tables .21

List of figures.. 22

# List of tables

Table 1. Applicable products 1   
Table 2. F(S)MC signals 5   
Table 3. LCD-TFT signals . 5   
Table 4. Minimum F(S)MC address bit to use depending on image size (16-bit RGB565 access) 8   
Table 5. Swap operations 14   
Table 6. Document revision history . 19

# List of figures

Figure 1. Display application typical use case. 3   
Figure 2. STM32H7R7/7S7 display application use case 4   
Figure 3. Display bus interface specification. 6   
Figure 4. Memory map for LCD-TFT display access 7   
Figure 5. Automatic control of LCD-TFT display data/command by F(S)MC interface   
Figure 6. 24 bpp over 16-bit interface color coding 12   
Figure 7. 16 bpp over 8-bit interface color coding 13   
Figure 8. 24 bpp over 8-bit interface color coding 13   
Figure 9. DMA2D operations to support 24 bpp over 16-bit interface. 15   
Figure 10. DMA2D operations to support 24 bpp over 8-bit interface. 16   
Figure 11. DMA2D operations to support 16 bpp over 8-bit interface. 17

# IMPORTANT NOTICE  READ CAREFULLY

pt old ursant  dits   leole.

purchasers' products.

No license, express or implied, to any intellectual property right is granted by ST herein.

are the property of their respective owners.

I

© 2024 STMicroelectronics - All rights reserved