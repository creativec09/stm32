# Introduction

A partnership with Segger Microcontroller GmbH & Co. KG enables STMicroelectronics to provide STemWin Library, a product based on Segger's emWin graphic library.

The STemWin Library is a professional graphical stack library enabling the building up of graphical user interfaces (GUIs) with any STM32, LCD/TFT display and LCD/TFT controller, taking advantage of STM32 hardware acceleration whenever possible.

The STemWin Library is a comprehensive solution with rich features, such as JPG, GIF and PNG decoding, many widgets (checkboxes, buttons...), and a VNC server. It allows a local display to be displayed remotely, and also professional tools (such as GulBuilder) to create dialog boxes by a drag and drop font converter.

This graphic library is fully integrated inside the STM32Cube firmware packages (such as STM32CubeF2, STM32CubeF3 and STM32CubeF4). It can be downloaded free from the STMicroelectronics web site (http://www.st.com/stm32cube)

Table 1. Applicable software   

<table><tr><td>Type</td><td>Part numbers</td></tr><tr><td>MCUs Embedded Software</td><td>STemWin, STM32CubeF0, STM32CubeF1, STM32CubeF2, STM32CubeF3, STM32CubeF4, STM32CubeF7, STM32CubeL1, STM32CubeL4 and STM32CubeH7</td></tr></table>

# Contents

General information 6

# Library and package presentation . .6

2.1 Licensing information 6   
2.2 Library description 6   
2.3 Package organization 9   
2.4 Delivered binaries . . 9

# Supported boards and examples . . 12

# How to use STemWin Library step by step . . . . .. 14

4.1 Configuration 14

4.1.1 GUIConf.c .15   
4.1.2 LCDConf.c 15   
4.1.3 Hardware acceleration 15   
4.1.4 GUI_X.c or GUI_X_OS.c 17

4.2 GUI initialization 17

# 4.3 Core functions 17

4.3.1 Image file display. 17   
4.3.2 Bidirectional text 18   
4.3.3 Alpha blending 18   
4.3.4 Sprites and cursors .18

4.4 Memory devices 19

4.5 Antialiasing . . . 20   
4.6 Window Manager 20   
4.7 Widget library 20

4.8 VNC server 21

4.8.1 Requirements .22   
4.8.2 Process description. 23

4.9 Fonts 24

4.9.1 Fonts included in STemWin library 24   
4.9.2 How to add a new font 27   
4.9.3 Language support .33

# 4.10 GUIBuilder 37

4.10.1 Basic usage of the GUIBuilder. 38   
4.10.2 Creation routine 38   
4.10.3 User-defined code 38   
4.10.4 Callback routine 38   
4.11 Porting GUI on a different resolution 39   
4.12 How to add a new effect . 39   
4.13 How to add a new widget 40

# Performance and footprint . . .. 41

5.1 LCD driver performance . . 41   
5.2 STemWin footprint 42

FAQs (frequently asked questions) . .. . 44

Revision history 45

# List of tables

Table 1. Applicable Software 1   
Table 2. Supported LCD controllers .8   
Table 3. Supported boards and examples 12   
Table 4. Hardware acceleration API list 16   
Table 5. Font API 26   
Table 6. Speed test list . 41   
Table 7. Speed test for the FlexColor and Lin drivers 41   
Table 8. Module footprint 42   
Table 9. Widget footprint. 43   
Table 10. FAQs.. 44   
Table 11. Document revision history 45

# List of figures

Figure 1. STemWin layers 7   
Figure 2. Project tree 9   
Figure 3. Structure of the STemWin application 13   
Figure 4. STemWin initialization 14   
Figure 5. Alpha blending effect 18   
Figure 6. Animated sprites. 18   
Figure 7. Cursors . 19   
Figure 8. Scaling and rotation effect using memdev 19   
Figure 9. Shape antialiasing 20   
Figure 10. Widget examples 21   
Figure 11. VNC server usage 22   
Figure 12. VNC client.. 23   
Figure 13. Font converter. 28   
Figure 14. Type font and encoding option 29   
Figure 15. font, style and size choice. 29   
Figure 16. Creation of the font C file 30   
Figure 17. Disable/Enable font characters. 31   
Figure 18. Characters range choice. 31   
Figure 19. Creation of different texts of the application 33   
Figure 20. Read pattern file menu . 34   
Figure 21. Missing characters codes of the used font 34   
Figure 22. Pattern characters enabled. 35   
Figure 23. Creation of UTF-8 pattern. 36   
Figure 24. Conversion of the UTF-8 pattern to "C" code . .36   
Figure 25. The GUIBuilder application. . 38

# 1 General information

The STemWin supports Arm®(a)baseddeis.

# arm

# Library and package presentation

The STemWin Library package includes a set of firmware libraries and software tools used to build advanced and professional GUl-based applications.

# 2.1 Licensing information

C STemWin Library GUl files are provided in object format and licensed under MCD-ST Image Software License Agreement V2 (the "License"); you may not use this package except in compliance with the License. You may obtain a copy of the License at: www.st.com.

• STemWin Library configuration and header files are provided in source format and licensed under MCD-ST Liberty Software License Agreement V2 (the "License"); you may not use this package except in compliance with the License. You may obtain a copy of the License at: www.st.com.

Unless required by applicable law or agreed to in writing, software distributed under the License is distributed on an "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the License for the specific language governing permissions and limitations under the License.

# 2.2 Library description

Figure 1 shows how STemWin is structured internally and how it can be implemented in a complete project.

![](images/de2de163c4caade3cac780dbfb34f0d1038b813780e85f07beb785be4784f8b3.jpg)  
Figure 1. STemWin layers

The CRC module n RCC peripheral clock enable register) should be enabled before using the library.

STemWin Library includes two optimized drivers:

Direct linear access (LIN) driver. This kind of driver is used for example on STM32F429, STM32F769, STM32H743 and any STM32 based on the LCD TFT Display Controller (LTDC) or LTDC/DSI (Display Serial Interface) hardware. FlexColor (indirect access) driver for serial and parallel bus external LCD controllers.

Refer to Table 2 for a list of all supported display controllers.

Note:

It is stil possble o supor any other LCD type ust byplentng t wn "ust"i

In addition to the main application, the user has to set and customize two essential interface files:

LCD configuration file (LCDConf.c)   
− LCD Display initialization and configuration LCD Display driver link and customizing Additional hardware capability management

GUI configuration file (GUIConf.c) GUI management

Table 2. Supported LCD controllers   

<table><tr><td>Driver</td><td>Supported LCD controllers</td><td>Supported bits/pixels</td></tr><tr><td>GUIDRV_Lin</td><td>This driver supports every display controller with linear addressable video memory with a direct (full bus) interface. This means that the video RAM is directly addressable by the address lines of the CPU. The driver contains no controller-specific code. So it can also be used for solutions without display controller which require a driver which only manages the video RAM.</td><td>1, 2, 4, 8, 16, 24, 32</td></tr><tr><td>GUIDRV_FlexColor</td><td>Epson S1D19122 FocalTech FT1509 Himax HX8353, HX8325A, HX8357, HX8340, HX8347, HX8352A, HX8352B, HX8301 Hitachi HD66772 Ilitek ILI9320, ILI9325, ILI9328, ILI9335, ILI9338, ILI9340, ILI9341, ILI9342, ILI9163, ILI9481, ILI9486, ILI9488, ILI9220, ILI9221 LG Electronics LGDP4531, LGDP4551, GDP4525 Novatek NT39122 OriseTech SPFD5408, SPFD54124C, SPFD5414D Raio RA8870, RA8875 Renesas R61505, R61516, R61526, R61580 Samsung S6E63D6, S6D0117 Sitronix ST7628, ST7637, ST7687, ST7735, ST7712 Solomon SSD1284, SSD1289, SSD1298, SSD1355, SSD2119, SSD1963, SSD1961, SSD1351 Syncoam SEPS525</td><td>16, 18</td></tr></table>

# 2.3 Package organization

Figure 2 shows the project tree.

![](images/85399248a4102abf5896990dedbb9884d93eafd020284befdf3fc96b8dc0af73.jpg)  
Figure 2. Project tree

# 2.4 Delivered binaries

STemWin Library is distributed by ST as an object code library locked to STM32 products.

The library is compiled for CM0 and CM3 cores:

With and without OS support. • With Size optimization Using ABGR and ARGB format

The library is compiled for CM4 and CM7 cores:

• With and without OS support. • With size and time optimization • Using ABGR and ARGB format The FPU is enabled.

The library is compiler-dependent (IAR, Arm, GCC).

The library is also compiled for WiN32 simulation

Using ABGR and ARGB format

# Note:

In the STM32CubeFW relative to a given core, only binary files generated for this core and simulation one are included in the package.

To summarize, 74 binary files are generated and split as follow:

For a CMx (CM0 and CM3) core there are 12 binaries:

STemWinXY_CMx_GCC.a   
• STemWinXY_CMx_GCC_ARGB.a STemWinXY_CMx_IAR.a   
• STemWinXY_CMx_IAR_ARGB.a   
• STemWinXY_CMx_Keil.lib STemWinXY_CMx_Keil_ARGB.lib   
• STemWinXY_CMx_OS_GCC.a   
• STemWinXY_CMx_OS_GCC_ARGB.a STemWinXY_CMx_OS_IAR.a   
• STemWinXY_CMx_OS_IAR_ARGB.a   
• STemWinXY_CMx_OS_Keil.lib STemWinXY_CMx_OS_Keil_ARGB.lib

For a CMx (CM4 and CM7) core there are 24 binaries:

− STemWinXY_CMx_GCC.a   
• STemWinXY_CMx_GCC_ARGB.a   
• STemWinXY_CMx_GCC_ot.a STemWinXY_CMx_GCC_ot_ARGB.a   
• STemWinXY_CMx_IAR.a   
• STemWinXY_CMx_IAR_ARGB.a   
• STemWinXY_CMx_IAR_ot.a   
• STemWinXY_CMx_IAR_ot_ARGB.a   
• STemWinXY_CMx_Keil.lib   
• STemWinXY_CMx_Keil_ARGB.lib STemWinXY_CMx_Keil_ot.lib   
• STemWinXY_CMx_Keil_ot_ARGB.lib   
• STemWinXY_CMx_OS_GCC.a   
• STemWinXY_CMx_OS_GCC_ARGB.a   
• STemWinXY_CMx_OS_GCC_ot.a   
• STemWinXY_CMx_OS_GCC_ot_ARGB.a   
• STemWinXY_CMx_OS_IAR.a   
• STemWinXY_CMx_OS_IAR_ARGB.a   
• STemWinXY_CMx_OS_IAR_ot.a   
• STemWinXY_CMx_OS_IAR_ot_ARGB.a   
• STemWinXY_CMx_OS_Keil.lib   
• STemWinXY_CMx_OS_Keil_ARGB.lib   
• STemWinXY_CMx_OS_Keil_ot.lib   
• STemWinXY_CMx_OS_Keil_ot_ARGB.lib

Then user add the simulation binaries:

• STemWinXY_WIN32.libSTemWinXY_WIN32_ARGB.lib

# Supported boards and examples

Table 3 lists the supported boards and examples.

Table 3. Supported boards and examples   
Figure 3 shows the architecture of a given STemWin application.   

<table><tr><td rowspan=1 colspan=2>STM32 Series/board</td><td rowspan=1 colspan=1>LCD interface</td><td rowspan=1 colspan=1>LCD driver</td></tr><tr><td rowspan=1 colspan=1>STM32F0</td><td rowspan=1 colspan=1>STM32091C-EVAL</td><td rowspan=1 colspan=1>SPI</td><td rowspan=1 colspan=1>FlexColor</td></tr><tr><td rowspan=2 colspan=1>STM32F1</td><td rowspan=1 colspan=1>STM3210C-EVAL</td><td rowspan=1 colspan=1>SPI</td><td rowspan=2 colspan=1>FlexColor</td></tr><tr><td rowspan=1 colspan=1>STM3210E-EVAL</td><td rowspan=1 colspan=1>FSMC</td></tr><tr><td rowspan=1 colspan=1>STM32F2</td><td rowspan=1 colspan=1>STM322xG-EVAL</td><td rowspan=1 colspan=1>FSMC</td><td rowspan=1 colspan=1>FlexColor</td></tr><tr><td rowspan=3 colspan=1>STM32F3</td><td rowspan=1 colspan=1>STM32303C-EVAL</td><td rowspan=1 colspan=1>SPI</td><td rowspan=3 colspan=1>FlexColor</td></tr><tr><td rowspan=1 colspan=1>STM32303E-EVAL</td><td rowspan=1 colspan=1>SPI</td></tr><tr><td rowspan=1 colspan=1>STM32373C-EVAL</td><td rowspan=1 colspan=1>SPI</td></tr><tr><td rowspan=8 colspan=1>STM32F4</td><td rowspan=1 colspan=1>STM32F412G-DISCO</td><td rowspan=1 colspan=1>FMC</td><td rowspan=1 colspan=1>FlexColor</td></tr><tr><td rowspan=1 colspan=1>STM32F413G-DISCO</td><td rowspan=1 colspan=1>FMC</td><td rowspan=1 colspan=1>FlexColor</td></tr><tr><td rowspan=1 colspan=1>STM32F429I-DISCO</td><td rowspan=1 colspan=1>LTDC</td><td rowspan=1 colspan=1>Lin</td></tr><tr><td rowspan=1 colspan=1>STM32F4x9I-EVAL</td><td rowspan=1 colspan=1>LTDC</td><td rowspan=1 colspan=1>Lin</td></tr><tr><td rowspan=1 colspan=1>STM32F4xG-EVAL</td><td rowspan=1 colspan=1>FSMC</td><td rowspan=1 colspan=1>FlexColor</td></tr><tr><td rowspan=1 colspan=1>STM32F446E-EVAL</td><td rowspan=1 colspan=1>FMC</td><td rowspan=1 colspan=1>FlexColor</td></tr><tr><td rowspan=1 colspan=1>STM32F469I-EVAL</td><td rowspan=1 colspan=1>LTDC/DSI</td><td rowspan=1 colspan=1>Lin</td></tr><tr><td rowspan=1 colspan=1>STM32F469I-DISCO</td><td rowspan=1 colspan=1>LTDC/DSI</td><td rowspan=1 colspan=1>Lin</td></tr><tr><td rowspan=5 colspan=1>STM32F7</td><td rowspan=1 colspan=1>STM32F723E-DISCO</td><td rowspan=1 colspan=1>FMC</td><td rowspan=1 colspan=1>FlexColor</td></tr><tr><td rowspan=1 colspan=1>STM32F769I-EVAL</td><td rowspan=1 colspan=1>LTDC/DSI</td><td rowspan=1 colspan=1>Lin</td></tr><tr><td rowspan=1 colspan=1>STM32F769I-DISCO</td><td rowspan=1 colspan=1>LTDC/DSI</td><td rowspan=1 colspan=1>Lin</td></tr><tr><td rowspan=1 colspan=1>STM32F746G-DISCO</td><td rowspan=1 colspan=1>LTDC</td><td rowspan=1 colspan=1>Lin</td></tr><tr><td rowspan=1 colspan=1>STM32F756G-EVAL</td><td rowspan=1 colspan=1>LTDC</td><td rowspan=1 colspan=1>Lin</td></tr><tr><td rowspan=1 colspan=1>STM32H7</td><td rowspan=1 colspan=1>STM32H743I-EVAL</td><td rowspan=1 colspan=1>LTDC</td><td rowspan=1 colspan=1>Lin</td></tr><tr><td rowspan=1 colspan=1>STM32L1</td><td rowspan=1 colspan=1>STM32L152D-EVAL</td><td rowspan=1 colspan=1>FSMC</td><td rowspan=1 colspan=1>FlexColor</td></tr><tr><td rowspan=5 colspan=1>STM32L4</td><td rowspan=1 colspan=1>STM32L49I-EVAL-MB1314</td><td rowspan=1 colspan=1>GFXMMU/LTDC/DSI</td><td rowspan=1 colspan=1>Lin</td></tr><tr><td rowspan=1 colspan=1>STM32L49I-EVAL-MB1315</td><td rowspan=1 colspan=1>LTDC</td><td rowspan=1 colspan=1>Lin</td></tr><tr><td rowspan=1 colspan=1>STM32L49I-DISCO</td><td rowspan=1 colspan=1>GFXMMU/LTDC/DSI</td><td rowspan=1 colspan=1>Lin</td></tr><tr><td rowspan=1 colspan=1>STM32L476G-EVAL</td><td rowspan=1 colspan=1>FMC</td><td rowspan=1 colspan=1>FlexColor</td></tr><tr><td rowspan=1 colspan=1>STM32L496G-DISCO</td><td rowspan=1 colspan=1>FMC</td><td rowspan=1 colspan=1>FlexColor</td></tr></table>

![](images/1e5f65eb1a239a9fd6fc733251e662fd417703fbcd58f6ff70578f853c768e7f.jpg)  
Figure 3. Structure of the STemWin application

The "Target" folder contains the two interface files described in Section 2.2:

• GUIConf.c/.h • LCDConf.c/.h

A STemWin application can be built using or not an OS. On the application architecture presented above it's a non OS case.

# How to use STemWin Library step by step

This section provides an overview of the main features of STemWin Library, as well as the main settings and configuration steps. For further details, refer to the Segger's emWin User Manual.

# 4.1 Configuration

The configuration is basically divided into two parts: GUl configuration and LCD configuration.

The GUl configuration covers the configuration of default colors and fonts and of available memory. The LCD configuration is more hardware-dependent and enables the user to define the different graphical parameters, the display driver, the color conversion routines to be used and the drawing accelerated function if the STM32 support Chrom-ART.

When a new LCD controller needs to be supported, two essential files must be created/modified: GUIConf.c and LCDConf.c.

The stack initialization done by calling "GUl_Init()" function is based on these 2 files as shown in Figure 4.

![](images/688bcb4d2c9a7097ad98524ed7cc8665d6be0bab3a047514df6f3312e7533a10.jpg)  
Figure 4. STemWin initialization

# 4.1.1 GUIConf.c

In this file, the user should implement the Gul_x_Config() function which is the very first routine called during the initialization process. Its main task is to set up the available memory for the GUl and to then assign it to the dynamic memory management system.

This operation is done via the GUl_ALLOC_AssignMemory() function: it passes a pointer to a memory block and its size (in bytes) to the memory manager.

# Note:

The memory must be accessible and must be 8-, 16- and 32-bit wide. Memory access is checked during initialization.

# 4.1.2 LCDConf.c

The main function here is LCD_X_Config(), called immediately after GUl_X_Config() has been executed. LCD_x_Config() allows creating and configuring a display driver for each layer by calling:

GUI_DEVICE_CreateAndLink(), which creates the driver device and links it to the device chain; • LCD_SetSizeEx() and LCD_SetVSizeEx(), to set the display size configuration; Other driver-specific configuration routines such as: GUIDRV_FlexColor_Config(), in association with the usage of the FlexColor driver; LCD_SetVRAMAddrEx(), required in case of linear addressable memory.

As mentioned in Section 2.2, STemWin Library comes with two optimized drivers, GUIDRV_Lin and GUIDRV_FlexColor, which cover all the LCDs embedded in ST EVALboards.

For more details about usage of these drivers, please visit Segger's website:

http://www.segger.com

In general, when a new LCD type needs to be supported, the user should check if the same LCD controller is already supported, then he just has to update the already existing LCDConf.c.

Another function, LCD_X_DisplayDriver(), is called by the display driver for several purposes, for example when using advanced features like multiple buffers, smooth scrolling or virtual pages. To support the corresponding task, the routine needs to be adapted to the display controller.

If the used display controller is not supported, user can easily create his own driver just by adapting the GUIDRV_Template.c file located under the CubeFW on this path "MiddlewaresISTISTemWiniConfig"

Actually this template file contains the complete functionality needed for a display driver. The main routines that need to be adapted are _SetPixellndex() and _GetPixellndex(). If the display is not readable, a display data cache should be implemented instead of using the _GetPixellndex() function.

# 4.1.3 Hardware acceleration

In order to decrease the CPU load and speed up many drawing operations, ST had included a Hardware acceleration IP known as the Chrom-ART in many STM32 products.

EmWin on the other side provide a list of API functions that can be accelerated.

The table below shows currently implemented HW acceleration API functions on the LCDConf.c".

Table 4. Hardware acceleration API list   

<table><tr><td rowspan=1 colspan=1>Function</td><td rowspan=1 colspan=1>Description</td></tr><tr><td rowspan=1 colspan=1>GUICC_M1555I_SetCustColorConv()</td><td rowspan=5 colspan=1>Function to set color conversion routines for theaccording fixed palette modes</td></tr><tr><td rowspan=1 colspan=1>GUICC_M565_SetCustColorConv()</td></tr><tr><td rowspan=1 colspan=1>GUICC_M4444I_SetCustColorConv()</td></tr><tr><td rowspan=1 colspan=1>GUICC_M888_SetCustColorConv()</td></tr><tr><td rowspan=1 colspan=1>GUICC_M8888I_SetCustColorConv()</td></tr><tr><td rowspan=1 colspan=1>LCD_DEVFUNC_COPYBUFFER</td><td rowspan=1 colspan=1>Id function to set a custom defined routine forcopying buffers</td></tr><tr><td rowspan=1 colspan=1>LCD_DEVFUNC_FILLRECT</td><td rowspan=1 colspan=1>Id function to set a custom defined routine forfilling rectangles</td></tr><tr><td rowspan=1 colspan=1>LCD_DEVFUNC_COPYRECT</td><td rowspan=1 colspan=1>Id function to set a custom defined routine forcopying rectangular areas</td></tr><tr><td rowspan=1 colspan=1>LCD_DEVFUNC_DRAWBMP_8BPP</td><td rowspan=1 colspan=1>Id function to set a custom routine for drawing8bpp bitmaps</td></tr><tr><td rowspan=1 colspan=1>LCD_DEVFUNC_DRAWBMP_16BPP</td><td rowspan=1 colspan=1>Id function to set a custom routine for drawing16bpp bitmaps</td></tr><tr><td rowspan=1 colspan=1>LCD_DEVFUNC_DRAWBMP_32BPP</td><td rowspan=1 colspan=1>Id function to set a custom routine for drawing32bpp bitmaps</td></tr><tr><td rowspan=1 colspan=1>GUI_SetFuncAlphaBlending()</td><td rowspan=1 colspan=1>Function to set up a custom defined function fordoing alpha blending operations</td></tr><tr><td rowspan=1 colspan=1>GUI_SetFuncGetpPalConvTable()</td><td rowspan=1 colspan=1>Function to set up palette conversion of a bitmapinto index values</td></tr><tr><td rowspan=1 colspan=1>GUI_SetFuncMixColorsBulk()</td><td rowspan=1 colspan=1>Function to set up bulk blending operations</td></tr><tr><td rowspan=1 colspan=1>GUI_AA_SetpfDrawCharAA4()</td><td rowspan=1 colspan=1>Function to set up drawing 4bpp alpha characters</td></tr><tr><td rowspan=1 colspan=1>GUI_MEMDEV_SetDrawMemdev16bppFunc()</td><td rowspan=1 colspan=1>Function to set up drawing 16bpp bitmaps into16bpp memory devices.</td></tr><tr><td rowspan=1 colspan=1>GUI_SetFuncDrawAlpha()</td><td rowspan=1 colspan=1>Function to set up 2 accelerations, first fordrawing memory devices with alpha value intoanother memory device and the second fordrawing bitmaps with alpha value.</td></tr></table>

# Remarks:

Note that not all STM32 products supports HW acceleration. On the currently delivered "LCDConf.c" some acceleration API are not yet implemented.

# 4.1.4 GUI_X.c or GUI_X_OS.c

GUI_X.c for single task execution:

"Single task" means that the project uses STemWin only from within one single task. The main purpose is to supply STemWin with a timing base. OS_TimeMS needs to be incremented each ms.

GUI_X_OS.c for multitask execution:

If STemWin is used in a multitasking system, this file contains additional routines required for synchronizing tasks.

All the functions of this file are using the CMSIS-RTOS API which is a generic RTOS interface for Arm® Cortex®-M processor-based devices, which provides a standardized API for software components that require RTOS functionality.

# 4.2 GUI initialization

To initialize the STemWin internal data structures and variables, GUl_Init() should be used.

Note that before initializing the GUI, the CRC module (in RCC peripheral clock enable register) should be enabled

A simple "Hello world" program illustrates this initialization, as shown below.

# "Hello world" example:

void Main(void) {int xPos, yPos;

_HAL_RCC_CRC_CLK_ENABLE(); GUI_Init();

xPos = LCD_GetXSize() / 2; yPos = LCD_GetYSize() / 3; GUI_SetFont(GUI_FONT_COMIC24B_ASCII); GUI_DispStringHCenterAt("Hello world!", xPos, yPos); while(1); }

# 4.3 Core functions

# 4.3.1 Image file display

STemWin currently supports the BMP, JPEG, GIF and PNG file formats. The library includes rich APls for each one of these image formats (fully documented in the STemWin User Manual). An approximation of the memory resources needed for each image type is given in Section 5: Performance and footprint.

# 4.3.2 Bidirectional text

Drawing Arabic or Hebrew text with STemWin is quite easy and is supported automatically in each text-based function. It only needs to be enabled once by using the following command:

GUI_UC_EnableBIDI()

# 4.3.3 Alpha blending

Alpha blending is a method combining the alpha channel with other layers in an image in order to create the appearance of semi-transparency (see Figure 5).

![](images/8d712549ae58ac81f23cc1e0c46cb03e21a5e2b80bd1cc054b1834009e5e0a1b.jpg)  
Figure 5. Alpha blending effect

The user can enable automatic alpha blending using the following command:

GUI_EnableAlpha()

He can also give an alpha value to determine how much of a pixel should be visible and how much of the background should show through:

GUI_SetUserAlpha()

# 4.3.4 Sprites and cursors

A sprite is an image which can be shown above all other graphics on the screen.

A sprite preserves the screen area it covers. It can be moved or removed at any time, fully restoring the screen content. Animation by use of multiple images is also possible.

![](images/004e94accc58753b845274ae19c835b142ecc60721b817a64a3fb16fda124f9f.jpg)  
Figure 6. Animated sprites

Sprites can be animated (Figure 6) by calling GUI_SPRITE_CreateAnim ( ).

Note that sprites manage the background automatically.

STemWin also includes a system-wide cursor (Figure 7), which can also be animated by using GUI_CURSOR_SetAnim ( ) . Cursors are actually based on sprites.

![](images/7a5156b727af23ed2a502794e4d2ce1e19b5eb732fd5e8916d47271e7e05ff9b.jpg)  
Figure 7. Cursors

Although the cursor always exists, it is hidden by default. It is not visible until a call is made to show it (GUI_cuRSoR_Show ( ) ), and may be hidden again at any point (GUI_CURSOR_Hide()).

# 4.4 Memory devices

A memory device is a hardware-independent destination device for drawing operations.

If a memory device is created (by calling GUI_MEMDEV_Create () then validated (by calling GUI_MEMDEV_Select ( ) ), all drawing operations are executed in memory. The final result is displayed on the screen only when all operations have been finished. This action is done by calling GUI_MEMDEV_CopyToLCD ( ).

Memory devices can be used:

• to prevent flickering effect (due to direct drawing on the display),   
• as containers for decompressed images, for rotating (GuI_MEMDEV_Rotate ( ) ) and scaling operations (Figure 8),   
• for fading operations, for window animations,   
• for transparency effects.

![](images/aab9adbbb38c6275feb5777cf8330a2dd996e748141a8491afaef7df227f3536.jpg)  
Figure 8. Scaling and rotation effect using memdev

Since memory devices need a considerable amount of memory (see component "Memory Device" in Table 8), it is advised to use an external memory if available.

# 4.5 Antialiasing

Antialiasing smoothes curves and diagonal lines by "blending" the background color with the foreground one. This is done by adding intermediate colors between object and background.

# Shape antialiasing

STemWin supports antialiased drawing of:

• Text (Font Converter is required to create AA fonts)   
• Arcs (GUI_AA_DrawArc())   
• Circles(GUI_AA_FillCircle())   
• Lines (GUI_AA_DrawLine())   
• Polygons (GUI_AA_DrawPolyOutline() and GUI_AA_FillPolygon())

![](images/9a71274e098565405c5bd4b53ab0baef44f00441fcdcf4a4fd93a8ba69e39856.jpg)  
Figure 9. Shape antialiasing

# 4.6 Window Manager

Window Manager can be described as:

A management system for a hierarchic window structure: Each layer has its own desktop window. Each desktop window can have its own hierarchic tree of child windows.   
A callback mechanism-based system: Communication is based on an event-driven callback mechanism. All drawing operations should be done within the WM_PAINT event.   
The foundation of the widget lbrary: All widgets are based on the functions of the Window Manager.

# 4.7 Widget library

Widgets (Window + Gadget) are windows with object-type properties. They require the Window Manager.

A list of all widgets available in STemWin Library can be found at: http://www.segger.com

Once a widget is created, it is treated just like any other window. The Window Manager ensures that it is properly displayed (and redrawn) whenever necessary.

![](images/49711e6a399b71384194e056e664c4a8163e5f12ca579e29d449c8664dda66ef.jpg)  
Figure 10. Widget examples

# Widget creation

Creating a widget can be done with one line of code.

Th aslyway  :

Direct creation:

Creation functions exist for each widget:

<WIDGET>_CreateEx ( ) : creation without user data. − <WIDGET>_CreateUser ( ): creation with user data.

Indirect creation:

"Indirect" means here using a dialog box creation function and a   
GUI_WIDGET_CREATE_INFO structure which contains a pointer to the indirect creation   
routine:

<WIDGET>_CreateIndirect ( ) : creation by dialog box creation function.

# 4.8 VNC server

VNC stands for "Virtual Network Computing". The VNC server is used to connect the embedded target to a network PC via TCP/IP, which allows to:

view the LCD content on the distant PC monitor, and to control the embedded environment using the mouse.

In other words, the display contents of the embedded device are visible on the screen of the machine running the client (for example, a network PC); the mouse and keyboard can then be used to control the target.

![](images/cb20d78042831ab5a3988bf9e49c2326c9ced5ae189816456a1857d282adba01.jpg)  
Figure 11. VNC server usage

# 4.8.1 Requirements

An STM32 device with embedded Ethernet IP, such as STM32F107xx, STM32F2x7xx or STM32F4x7xx. • A TCP/IP stack should be present in the target. In the delivered demo, LwlP is used. The VNC server should run as a separate thread. Therefore, a multitasking system is required to use the emWin VNC server. In our case, the demo package runs with FreeRTOS. A VNC viewer (such as RealVNC, TightVNC, UltraVNC..) should be present in the supervising PC.

# 4.8.2 Process description

Connect the target hardware to the network (or to the PC, if a local connection is needed) via an Ethernet cable.

Run the demo.

The VNC_Server_task is a sub-task of the Background_Task. After hardware (LEDs, Touch Screen, SRAM...) and GUI initialization, the TCP/IP (LwIP) stack is also initialized. Then GUI_VNC_X_StartServer() is called to:   
a) initialize the VNC context and attach it to a layer,   
b) create a task for the VNC server, which listens on port 5900 until an incoming connection is detected and then runs the actual server (by calling GUI_VNC_Process()).

If DHCP is enabled ("#define USE_DHCP" in main.h):

Wait for the IP address to be assigned by the DHCP server; it will be displayed in the "VNC Server" page (just after the "Intro" page).   
If it is impossible to retrieve any IP address (DHCP timeout), a predefined static IP address is assigned and displayed.

If DHCP is disabled (or in case of DHCP timeout):

Wait for a static IP address to be displayed.   
Configure the IP address and the subnet mask of the PC with the same class address as used in the target hardware.

Start the VNC viewer.

Connect to the IP address of the target hardware (see Figure 12).   
The demo is then displayed on the PC.

Using the VNC viewer, the user can:

Watch the running demo on the PC monitor (live streaming); Control the target hardware from the PC (using the mouse); Take screenshots of the demo (if needed for a manual, for exampl

Note:

Breaking the viewer's connection to the server and then reconnecting does not result in any loss of data.

![](images/10bdda00cfd6f5aec66e88dda7001daeb709c8d4dc7a45fe7babd1e8080b2202.jpg)  
Figure 12. VNC client

# 4.9 Fonts

The most common fonts are included in STemWin Library as a standard font package. All of them contain the ASCll character set and most of them also the ISO 8859-1 characters.

A complete list of the embedded fonts is shown below (taken from GUl.h).

Note:

The STemWin Library default font is GUl_Font6x8.

# 4.9.1 Fonts included in STemWin library

//   
// Proportional fonts   
//   
#define GUI_FONT_8_ASCII &GUI_Font8_ASCII   
#define GUI_FONT_8_1 &GUI_Font8_1   
#define GUI_FONT_10S_ASCII &GUI_Font10S_ASCII   
#define GUI_FONT_10S_1 &GUI_Font10S_1   
#define GUI_FONT_10_ASCII &GUI_Font10_ASCII   
#define GUI_FONT_10_1 &GUI_Font10_1   
#define GUI_FONT_13_ASCII &GUI_Font13_ASCII   
#define GUI_FONT_13_1 &GUI_Font13_1   
#define GUI_FONT_13B_ASCII &GUI_Font13B_ASCII   
#define GUI_FONT_13B_1 &GUI_Font13B_1   
#define GUI_FONT_13H_ASCII &GUI_Font13H_ASCII   
#define GUI_FONT_13H_1 &GUI_Font13H_1   
#define GUI_FONT_13HB_ASCII &GUI_Font13HB_ASCII   
#define GUI_FONT_13HB_1 &GUI_Font13HB_1   
#define GUI_FONT_16_ASCII &GUI_Font16_ASCII   
#define GUI_FONT_16_1 &GUI_Font16_1   
#define GUI_FONT_16_HK &GUI_Font16_HK   
#define GUI_FONT_16_1HK &GUI_Font16_1HK   
#define GUI_FONT_16B_ASCII &GUI_Font16B_ASCII   
#define GUI_FONT_16B_1 &GUI_Font16B_1   
#define GUI_FONT_20_ASCII &GUI_Font20_ASCII   
#define GUI_FONT_20_1 &GUI_Font20_1   
#define GUI_FONT_20B_ASCII &GUI_Font20B_ASCII   
#define GUI_FONT_20B_1 &GUI_Font20B_1   
#define GUI_FONT_24_ASCII &GUI_Font24_ASCII   
#define GUI_FONT_24_1 &GUI_Font24_1   
#define GUI_FONT_24B_ASCII &GUI_Font24B_ASCII   
#define GUI_FONT_24B_1 &GUI_Font24B_1   
#define GUI_FONT_32_ASCII &GUI_Font32_ASCII   
#define GUI_FONT_32_1 &GUI_Font32_1   
#define GUI_FONT_32B_ASCII &GUI_Font32B_ASCII   
#define GUI_FONT_32B_1 &GUI_Font32B_1   
//   
// Proportional fonts, framed   
//   
#define GUI_FONT_20F_ASCII &GUI_Font20F_ASCII   
//   
// Monospaced   
//   
#define GUI_FONT_4X6 &GUI_Font4x6   
#define GUI_FONT_6X8 &GUI_Font6x8   
#define GUI_FONT_6X8_ASCII &GUI_Font6x8_ASCII   
#define GUI_FONT_6X8_1 &GUI_Font6x8_1   
#define GUI_FONT_6X9 &GUI_Font6x9   
#define GUI_FONT_8X8 &GUI_Font8x8   
#define GUI_FONT_8X8_ASCII &GUI_Font8x8_ASCII   
#define GUI_FONT_8X8_1 &GUI_Font8x8_1   
#define GUI_FONT_8X9 &GUI_Font8x9   
#define GUI_FONT_8X10_ASCII &GUI_Font8x10_ASCII   
#define GUI_FONT_8X12_ASCII &GUI_Font8x12_ASCII   
#define GUI_FONT_8X13_ASCII &GUI_Font8x13_ASCII   
#define GUI_FONT_8X13_1 &GUI_Font8x13_1   
#define GUI_FONT_8X15B_ASCII &GUI_Font8x15B_ASCII   
#define GUI_FONT_8X15B_1 &GUI_Font8x15B_1   
#define GUI_FONT_8X16 &GUI_Font8x16   
#define GUI_FONT_8X17 &GUI_Font8x17   
#define GUI_FONT_8X18 &GUI_Font8x18   
#define GUI_FONT_8X16X1X2 &GUI_Font8x16x1x2   
#define GUI_FONT_8X16X2X2 &GUI_Font8x16x2x2   
#define GUI_FONT_8X16X3X3 &GUI_Font8x16x3x3   
#define GUI_FONT_8X16_ASCII &GUI_Font8x16_ASCII   
#define GUI_FONT_8X16_1 &GUI_Font8x16_1

# //

// Digits   
//   
#define GUI_FONT_D24X32 &GUI_FontD24x32   
#define GUI_FONT_D32 &GUI_FontD32   
#define GUI_FONT_D36X48 &GUI_FontD36x48   
#define GUI_FONT_D48 &GUI_FontD48   
#define GUI_FONT_D48X64 &GUI_FontD48x64   
#define GUI_FONT_D64 &GUI_FontD64   
#define GUI_FONT_D60X80 &GUI_FontD60x80   
#define GUI_FONT_D80 &GUI_FontD80

// Comic fonts   
//   
#define GUI_FONT_COMIC18B_ASCII &GUI_FontComic18B_ASCII   
#define GUI_FONT_COMIC18B_1 &GUI_FontComic18B_1   
#define GUI_FONT_COMIC24B_ASCII &GUI_FontComic24B_ASCII   
#define GUI_FONT_COMIC24B_1 &GUI_FontComic24B_1

In most cases, those fonts are found sufficient. However, if needed, STemWin also supports several external font formats:

• System Independent Font (SIF) format • External Bitmap Font (XBF) format √ TrueType Font (TTF) format

For those, STemWin Library includes a rich font APl. See Table 5.

Table 5. Font API   

<table><tr><td colspan="1" rowspan="1">Routine</td><td colspan="1" rowspan="1">Description</td></tr><tr><td colspan="2" rowspan="1">C file related font functions</td></tr><tr><td colspan="1" rowspan="1">GUI_SetDefaultFont()</td><td colspan="1" rowspan="1">Sets the default font.</td></tr><tr><td colspan="1" rowspan="1">GUI_SetFont()</td><td colspan="1" rowspan="1">Sets the current font.</td></tr><tr><td colspan="2" rowspan="1">'SIF' file related font functions</td></tr><tr><td colspan="1" rowspan="1">GUI_SIF_CreateFont()</td><td colspan="1" rowspan="1">Creates and selects a font by passing a pointer to system-independent font data.</td></tr><tr><td colspan="1" rowspan="1">GUI_SIF_DeleteFont()</td><td colspan="1" rowspan="1">Deletes a font previously created by GUI_SIF_CreateFont().</td></tr><tr><td colspan="2" rowspan="1">'TTF' file related font functions</td></tr><tr><td colspan="1" rowspan="1">GUI_TTF_CreateFont()</td><td colspan="1" rowspan="1">Creates a GUI font from a TTF font file.</td></tr><tr><td colspan="1" rowspan="1">GUI_TTF_DestroyCache()</td><td colspan="1" rowspan="1">Destroys the cache of the TTF engine.</td></tr><tr><td colspan="1" rowspan="1">GUI_TTF_Done()</td><td colspan="1" rowspan="1">Frees all dynamically allocated memory of the TTF engine.</td></tr><tr><td colspan="1" rowspan="1">GUI_TTF_GetFamilyName()</td><td colspan="1" rowspan="1">Returns the family name of the font.</td></tr><tr><td colspan="1" rowspan="1">GUI_TTF_GetStyleName()</td><td colspan="1" rowspan="1">Returns the style name of the font.</td></tr><tr><td colspan="1" rowspan="1">GUI_TTF_SetCacheSize()</td><td colspan="1" rowspan="1">Can be used to set the default size of the TTF cache.</td></tr><tr><td colspan="2" rowspan="1">'XBF' file related font functions</td></tr><tr><td colspan="1" rowspan="1">GUI_XBF_CreateFont()</td><td colspan="1" rowspan="1">Creates and selects a font by passing a pointer to a callbackfunction, which then extracts data from the XBF font file.</td></tr><tr><td colspan="1" rowspan="1">GUI_XBF_DeleteFont()</td><td colspan="1" rowspan="1">Deletes a font previously created by GUI_XBF_CreateFont().</td></tr><tr><td colspan="2" rowspan="1">Common font-related functions</td></tr><tr><td colspan="1" rowspan="1">GUI_GetCharDistX()</td><td colspan="1" rowspan="1">Returns the width in pixels (X-size) of a specified character inthe current font.</td></tr><tr><td colspan="1" rowspan="1">GUI_GetFont()</td><td colspan="1" rowspan="1">Returns a pointer to the currently selected font.</td></tr><tr><td colspan="1" rowspan="1">GUI_GetFontDistY()</td><td colspan="1" rowspan="1">Returns the Y-spacing of the current font.</td></tr><tr><td colspan="1" rowspan="1">GUI_GetFontInfo()</td><td colspan="1" rowspan="1">Returns a structure containing font information.</td></tr><tr><td colspan="1" rowspan="1">GUI_GetFontSizeY()</td><td colspan="1" rowspan="1">Returns he height in pie  ecurrent nt.</td></tr><tr><td colspan="1" rowspan="1">GUI_GetLeadingBlankCols()</td><td colspan="1" rowspan="1">Returns the number of leading blank pixel columns of the givencharacter.</td></tr><tr><td colspan="1" rowspan="1">GUI_GetStringDistX()</td><td colspan="1" rowspan="1">Returns the X-size of a text using the current font.</td></tr><tr><td colspan="1" rowspan="1">GUI_GetTextExtend()</td><td colspan="1" rowspan="1">Evaluates the size of a text using the current font</td></tr><tr><td colspan="1" rowspan="1">GUI_GetTrailingBlankCols()</td><td colspan="1" rowspan="1">Returns the number of trailing blank pixel columns of the givencharacter.</td></tr><tr><td colspan="1" rowspan="1">GUI_GetYDistOfFont()</td><td colspan="1" rowspan="1">Returns the Y-spacing of a particular font.</td></tr><tr><td colspan="1" rowspan="1">GUI_GetYSizeOfFont()</td><td colspan="1" rowspan="1">Returns the Y-size of a particular font.</td></tr><tr><td colspan="1" rowspan="1">GUI_IslnFont()</td><td colspan="1" rowspan="1">Evaluates whether a specified character belongs to a particularfont.</td></tr></table>

# 4.9.2 How to add a new font

In order to be able to use any desired font when building our application, STemWin provides a tool called "Font Converter".

As a Windows program, it allows a convenient converting of any PC installed font into a STemWin (bitmap) font which can be easily integrated into our application.

The generated fonts will be defined either in C files or as binary files containing System Independent Fonts (SIF) or External Bitmap Font (XBF).

Only the generation of a C file from an installed font on the PC wilbe detailed on this part.

On the STM32CubeFW, go to the following path "MiddlewaresISTISTemWinlSoftware" and execute "FontCvtST.exe"

![](images/5b77525eedfb358588b4580137c73ed420eb2880ff56aef62aaa04a9cc26877a.jpg)  
Figure 13. Font converter   
Once opened you need to choose the type of the font to generate and the encoding option.

![](images/186fe692a29f3a5f9d379a73e80732c9358d72577f04521d7fe4f123b27507dd.jpg)  
Figure 14. Type font and encoding option

You need then to choose the desired font, its style and size.

![](images/975f308b2bf300b73fd51aca75c1d7f417f0e9b47d531e118601a9626a7f62fc.jpg)  
Figure 15. font, style and size choice

You need finally to save this font to a C file with the meaningful name that gives information about the font.

![](images/781645e0240074e7309bbb467e80145eab893462353061af67a91bbcfafe60f3.jpg)  
Figure 16. Creation of the font C file

# Optimization

The issue here is that the "C" file generated will contain all the characters and symbols of the font. As the "C" file will be compiled with the application so the user need enough addressable memory available for the font data.

As a solution to this issue, if some symbols and characters are not needed can disable them using the Font Converter and generate only the needed blocks from the desired font.

First for the opened font, the user need to disable all characters (Red selection on the following picture).

![](images/8cf458a3377f7bb07ef56d8f5212f510d3cce7f3568fdee347468f15ef46722d.jpg)  
Figure 17. Disable/Enable font characters

Then enable only the blocks of characters you want to keep (Blue selection on the above picture), you need just to enter the range of you selection.

![](images/f5b7b1f825923c9e079f8a3e06d23e74ae4cc38be0c1ea9f77f765179ac81c27.jpg)  
Figure 18. Characters range choice

Then you save as a "C" file.

If for example only the character 'A' is needed from this font, the generated font file will be the following:

#include "GUI.h"

#ifndef GUI_CONST_STORAGE #define GUI_CONST_STORAGE const #endif

/\* The following line needs to be included in any file selecting the font.   
\*/   
extern GUI_CONST_STORAGE GUI_FONT GUI_FontLucida_Console20;   
/\* Start of unicode area <Basic Latin> \*/   
GUI_CONST_STORAGE unsigned char acGUI_FontLucida_Console20_0041[ 26] = { /\*   
COde 0041, LATIN CAPITAL LETTER A \*/ XX_, XXXX, XXXX, X_XX, XX_X, X XX_X, X XXX, XX XX _,XX → XXXXXX, XX   
_XXXXXXX, XXX   
_XX , _XX →   
_XX ,_XX   
XX ,_XX _};   
GUI_CONST_STORAGE GUI_CHARINFO_EXT GUI_FontLucida_Console20_CharInfo[1] = { {12, 13, 0, 3, 12, acGuI_FontLucida_Console20_0041 } /\* code   
0041, LATIN CAPITAL LETTER A \*/   
};   
GUI_CONST_STORAGE GUI_FONT_PROP_EXT GUI_FontLucida_Console20_Prop1 = { Ox0041 /\* first character \*/ ,Ox0041 /\* last character \*/ ,&GUI_FontLucida_Console20_CharInfo[ 0] /\* address of first character \*/ , (GUI_CONST_STORAGE GUI_FONT_PROP_EXT \*)0 /\* pointer to next   
GUI_FONT_PROP_EXT \*/   
};

GUI_CONST_STORAGE GUI_FONT GUI_FontLucida_Console20 = { GUI_FONTTYPE_PROP_EXT /\* type of font \*/ ,20 /\* height of font \*/ ,20 /\* space of font y \*/ ,1 /\* magnification x \*/ ,1 /\* magnification y \*/ ,{&GUI_FontLucida_Console20_Prop1} ,16 /\* Baseline \*/ ,11 /\* Height of lowercase characters \*/ ,13 /\* Height of capital characters \*/

};

# .9.3 Language support

Text written in a language like Arabic, Hebrew, Thai or Chinese contains characters, which are normally not part of the fonts shipped with STemWin.

For such language with different read/write direction and for every meaningful character or text element of all known cultures, Unicode standard contains a unique digital code point.

To be able to decode text with Unicode characters, STemWin uses UTF-8 encoding method.   
(For more detail see User Manual).

The following sections explain how to support the usage of the fonts using above languages.

For a four given language there are two task to reach:

Generate the font "C" file that will be used   
Add the needed SW on STemWin application to be able to display the needed   
characters

Let's suppose that the user is trying to display "welcome" string translated on Thai, Arabic, Hebrew and traditional Chinese languages.

Firstly the user write the needed text using these languages, and save the text file using "Unicode" format. The user can use "Notepad.exe" for this, as showed in Figure 19.

![](images/19d10e697da476b56fda67cafcd18533879842f6d48cc7f89c3f7901cb760775.jpg)  
Figure 19. Creation of different texts of the application

# "C" file generation

Then using the "FontConverter" the user choose the font that support all these languages On the shown case, the user generate two fonts files, the first one for the Arabic, Hebrew and Thai languages; the second for the Chinese one.

Once the font is already opened on the "FontConverter" the user need to disable all the characters as shown in Optimization.

Then he e pattgeifn .

![](images/2e2a9e541684fdab3a4c510a5ea5edaef76fae087a6cc282b71c58ee2429a9ec.jpg)  
Figure 20. Read pattern file menu

Browse and load the file created. In the example, it will be "TestFont.txt".

If any language inside the "TestFont.txt" is not supported by the font used a warning message is shown.

![](images/505d2e6a706f6a9a8d447e2a11768cc5e9a16142f74a967296909aa36a637567.jpg)  
Figure 21. Missing characters codes of the used font

No problem with that, just push "OK" button.

Then the characters written on the "FontTest.txt" will be enabled.

<table><tr><td colspan="14">n Fon C -0 ×</td></tr><tr><td colspan="14"></td></tr><tr><td>File Edit View Options Help</td><td></td><td></td><td></td><td></td><td>-IH1TH</td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td></tr><tr><td>0 +1+</td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td>Hebrew (Basic and Extended)</td></tr><tr><td>0580 05C0</td><td></td><td></td><td></td><td></td><td></td><td>[</td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td>A Hebrew (Basic and Extended) Hebrew (Basic and Extended) Hebrew (Basic and Extended] Hebrew (Basic and Extended) Arabic (Basic and Extended</td></tr><tr><td>05D0</td><td>x 1</td><td>1</td><td></td><td>T</td><td>i7 1</td><td>T</td><td>n</td><td>U</td><td>1</td><td></td><td>D</td><td>7</td><td>0</td><td>n</td><td></td></tr><tr><td>05E0</td><td>]</td><td>0</td><td>U</td><td>7</td><td>9 P</td><td>y</td><td>7</td><td>7</td><td>W</td><td>n</td><td></td><td></td><td></td><td></td><td></td></tr><tr><td>05F0</td><td>11</td><td>1</td><td>11</td><td></td><td>#</td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td></tr><tr><td>0600</td><td>4</td><td>Whe</td><td>A</td><td>4</td><td></td><td></td><td></td><td></td><td></td><td></td><td>$\frac{{ 9 }$</td><td></td><td>′</td><td>P</td><td>6</td></tr><tr><td>0610</td><td>,.</td><td></td><td>v</td><td>)</td><td>H</td><td></td><td></td><td></td><td></td><td></td><td>!</td><td></td><td></td><td>A</td><td>ξ</td></tr><tr><td>0620</td><td></td><td>:</td><td></td><td></td><td>$\frac{{ }$</td><td>is</td><td>|</td><td>7</td><td>6</td><td>e</td><td>2</td><td>2</td><td>2</td><td>2</td><td>J</td></tr><tr><td>0630</td><td>5</td><td>2</td><td>j</td><td>U</td><td>v 4</td><td>$v</td><td>6</td><td>1</td><td>E</td><td>E</td><td></td><td></td><td></td><td></td><td></td></tr><tr><td>0640</td><td>-</td><td>3</td><td>3</td><td>J</td><td>J P</td><td></td><td>0</td><td>9</td><td>s</td><td>$</td><td></td><td>4</td><td></td><td></td><td></td></tr><tr><td>0650</td><td></td><td></td><td></td><td></td><td></td><td></td><td>6</td><td>•</td><td>-</td><td></td><td></td><td></td><td></td><td></td><td></td></tr><tr><td>0660</td><td>*</td><td>1</td><td>Y</td><td>7</td><td>≤ 0</td><td>7</td><td>V</td><td>A</td><td>9</td><td>%</td><td></td><td></td><td>*</td><td>c</td><td>9</td></tr><tr><td>0670</td><td></td><td></td><td>\}$</td><td>↓</td><td>$\frac}$ F</td><td>$\frac{{ }$</td><td>$\frac{ { 3 }$</td><td>s$</td><td>e</td><td>2</td><td>Y</td><td>U</td><td>2</td><td>4</td><td>U</td></tr><tr><td>0680</td><td>U</td><td>\$</td><td>t</td><td>2</td><td>2 $\fac}$</td><td>2</td><td>2</td><td>$\frac{{ 3 }$</td><td>$</td><td>2</td><td>$\frac { {  }$</td><td>$\f$</td><td>$\}$</td><td>$\frac { { 3}$</td><td>$\fra}$</td></tr><tr><td>0690</td><td>$\frac{ { 3 }$</td><td>3</td><td>j</td><td>Lo</td><td>dac}$ 2</td><td></td><td>j</td><td>$\frac3 }$</td><td>3</td><td>U</td><td>U</td><td>4</td><td>ve</td><td>$4\}$</td><td>$fra}$</td></tr><tr><td>06A0</td><td>$frac}$</td><td>c</td><td></td><td>4</td><td>fa}$ 4</td><td></td><td>$</td><td>$\frac{{ }$</td><td>≤</td><td>s</td><td>S</td><td>d</td><td>\</td><td>4</td><td>3 Arabic [Basic and Extended]</td></tr><tr><td>06B0</td><td>3</td><td>3</td><td>$</td><td>$</td><td>3 J</td><td></td><td>J</td><td>J</td><td>U</td><td>U</td><td>0</td><td>i</td><td>3</td><td>Δ</td><td>e Arabic (Basic and Extended]</td></tr><tr><td>06C0</td><td>$\frac  }$</td><td>^</td><td>$\$</td><td>^</td><td>3 3</td><td>$\frac3}$</td><td>$\fr{3 }$</td><td>$\frac{ { 39 }$</td><td>$\}$</td><td>\$</td><td>$\frac { { }$</td><td>s</td><td>s</td><td>is</td><td>Arabic (Basic and Extended j</td></tr><tr><td>06D0</td><td>$</td><td>$ a 7</td><td>L</td><td>\ •</td><td>0</td><td>r</td><td>$\frac{ { 2 }$</td><td></td><td>\</td><td>e</td><td></td><td>v</td><td>O</td><td></td><td>Arabic (Basic and Extended]</td></tr><tr><td>06E0</td><td></td><td></td><td>α 7</td><td></td><td></td><td>L</td><td>L</td><td>i</td><td>I</td><td></td><td></td><td></td><td></td><td>3</td><td>Arabic (Basic and Extended 3 Arabic (Basic and Extended)]</td></tr><tr><td>06F0</td><td>*</td><td>T |</td><td></td><td>F</td><td>0</td><td>9</td><td>v</td><td>A</td><td>9</td><td>vA</td><td>v</td><td>E</td><td>8</td><td>P</td><td>\</td></tr><tr><td>0700</td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td>Unassigned</td></tr><tr><td>0710</td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td>Unassigned</td></tr><tr><td>0720</td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td>Unassigned</td></tr><tr><td>0730 n740</td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td>Unassigned</td></tr><tr><td colspan="12">RReady •</td></tr></table>

Note:

Both Thai and Arabic language have some constraints of usage to display the exactly needed strings:

• For Arabic fonts the following range needs to be activated Ox600 to Ox6FF   
√ For Thai fonts The font file must be created as "Extended" The following range needs to be activated OxE00-0xE7F

Once done just save to your "C" file.

# Needed SW to add

As a result of the description above, we are having the two font files that user to add to application compilation.

Now to be able to display these strings on application the user adapt the application software to decode the Unicode.

STemWin is able to decode UTF-8 encoded strings, so to display the Unicode characters added on the file "FontTest.txt", user need firstly to save it on UTF-8 format.

![](images/3b53a0296933cb1969db55dcf802cfd8d3a0b5e45cb3fddb991e82a442cb5e6f.jpg)  
Figure 23. Creation of UTF-8 pattern

To convert the UTF-8 text to a "C" code, go to the STM32CubeFW on the following path "MiddlewaresISTISTemWinlSoftware" and execute "U2C.exe" with the file "FontTest.txt" as input.

![](images/a3b8ee4c6386fe50d0eaf8e7b5ace2b1302f45a026a0540540f20d860fc550f6.jpg)  
Figure 24. Conversion of the UTF-8 pattern to "C" code

# The output of the "U2C" converter will be:

"\xe0\xb8\xaa\xe0\xb8\xa7\xe0\xb8\xb1\xe0\xb8\xaa\xe0\xb8\x94\xe0\xb8\xb5\ xe0\xb8\x81\xe0\xb8\xb1\xe0\xb8\x9a\xe0\xb8\x84\xe0\xb8\xb8\xe0\xb8\x93” "\xd9\x85\xd8\xb1\xd8\xad\xd8\xa8\xd8\xa7\xd8\xa8\xd9\x83\xd9\x85" "\xd7\xa9\xd7\x9c\xd7\x95\xd7\x9d \xd7\x9c\xd7\x9b\xd7\x9d" "\xe5\x90\x91\xe4\xbd\xa0\xe5\x95\x8f\xe5\xa5\xbd"

Each line (text between " ") correspond to the string on the dame line on the "txt" file.

Now the user can create application using this output:

#include "GUI.h" /\* Font for Thai, Arabic and Hebrew languages \*/ #include "MicrosoftSansSerif20.c" /\* Font for Chinese language \*/ #include "Microsoft_YaHeiUI20.c"

static const char \* _apStrings[] =   
{   
"\xe0\xb8\xaa\xe0\xb8\xa7\xe0\xb8\xb1\xe0\xb8\xaa\xe0\xb8\x94\xe0\xb8\xb5|   
xe0\xb8\x81\xe0\xb8\xb1\xe0\xb8\x9a\xe0\xb8\x84\xe0\xb8\xb8\xe0\xb8\x93",   
"\xd9\x85\xd8\xb1\xd8\xad\xd8\xa8\xd8\xa7\xd8\xa8\xd9\x83\xd9\x85",   
"\xd7\xa9\xd7\x9c\xd7\x95\xd7\x9d \xd7\x9c\xd7\x9b\xd7\x9d",   
"\xe5\x90\x91\xe4\xbd\xa0\xe5\x95\x8f\xe5\xa5\xbd",   
};   
void MainTask(void)   
{ int i; GUI_Init(); GUI_SetFont(&GUI_FontMicrosoftSansSerif20); GUI_UC_SetEncodeUTF8(); /\* Thai string \*/ GUI_DispString(_apStrings[0]); GUI_DispNextLine(); /\* Arabic and Hebrew strings: In this case we need to enable bidirectional (right to left) text support \*/ GUI_UC_EnableBIDI(1); GUI_DispString(_apStrings[1]); GUI_DispNextLine(); GUI_DispString(_apStrings[2]); GUI_DispNextLine(); /\* Chinese string, bidirectional no more needed \*/ GUI_UC_EnableBIDI(0); GUI_DispString(_apStrings[3]); while(1) { GUI_Delay(500); }   
}

# 4.10 GUIBuilder

The GUlBuilder is a tool for easily creating dialogs: instead of writing source code, the user can place and size widgets by drag and drop. Additional properties can be added via a popup menu. Fine tuning can be done by editing the properties of the widgets.

The GulBuilder then generates some dialog C code that can be either customized or integrated as is in the project.

![](images/e94ade2057feaf48606e92ea426f70e57a9405e99c2eeffd9d5ec1f2e02f958b.jpg)  
Figure 25. The GUIBuilder application

# 4.10.1 Basic usage of the GUlBuilder

Start with the FRAMEWIN or WINDOW widget: only those widgets are able to serve as parent windows for a dialog.   
• Place the widgets within the parent window: the widgets can be placed and sized by moving them with the mouse and/or by editing the properties in the property window.   
• Configure the widgets: the pop-up menu shows the available options. Save the dialog: each dialog is saved in a separate file. The filenames are generated automatically, based on the name of the parent window.

# 4.10.2 Creation routine

The file generated using GulBuilder contains a creation routine for the dialog. The routine name includes the name of the parent window: WM_HWIN Create<WindowName> (void);

Simply call the following routine to create the dialog:

hWin = CreateFramewin();

# 4.10.3 User-defined code

The generated code contains a couple of comments to add user code between them. To be able to read back the file with the GUlBuilder, the code must be between these comments.

Adding code outside the user code comments makes the file unreadable for the GUlBuilder.

# 4.10.4 Callback routine

T u Il o message handlers:

WM_INIT_DIALOG

The widget initialization is done here immediately after creating all widgets of the dialog. The user code area can be used to add further initialization.

WM_NOTIFY_PARENT

It contains (empty) message handlers to be filled with user code. For each notification of the widget, there is one message handler. Further reactions on notification messages can be added.

# 4.11 Porting GUl on a different resolution

The setting of the GUI resolution is completely done on the "LCDConf.c" and it's very simple to go from one resolution to another.

The setting depend on the screen resolution attached the board that will be used. In this case a physical size of the screen is already known.

The variables "XSIZE_PHYS" and "YSIZE_PHYS" will be set on the "LCDConf.c" to mention the physical screen size.

Suppose that our screen has the resolution of (800x480), the "LCDConf.c" have the following content:

/\* Define physical screen sizes \*/ #define XSIZE_PHYS 800 #define YSIZE_PHYS 480

These variables will be used to initialize the hardware linked to the screen (ex: the LTDC/DSI).

The GUI resolution is then set using two other variables called "XSIZE_0" and "YSIZE_0".

" correspond to layer "0", so there are also "XSIZE_1" and "YSIZE_1" if the layer "1" is used.

Of course the GUl resolution must fit on the physical one.

#define XSIZE_0 XSIZE_PHYS #define YSIZE_0 YSIZE_PHYS

If now the screen (or the GUl resolution) have to be modified, the variables have to be modified as mentioned above.

# 4.12 How to add a new effect

SeW ese blity veef e lurbedng d using the memory devices API.

The user can also create some other effects using memory devices or any rectangular part of the used frame buffers.

Note that all effects added and data treatments will be done on ARGB8888 format.

Color conversions will be done when displaying on the LCD if needed.

The idea is to manipulate directly the data to modify. So it's mandatory to know the base address, the width and the height of the data to be treated.

Two method are available to reach this purpose:

• Use a free memory base address • Use the memory device, this wil allocate dynamically a given memory

It willbe easier and safer to use the memory devices knowing the multitude of APls provided by STemWin.

The new effect to be added, in the software, will be defined by a filter that get as input the data pointer, its width and height and give as output the modified data to a new address.

This will consist on the following steps:

• Create a 32 Bits Per Pixel (Bpp) source memory device   
• Create a 32 Bpp destination memory device with the same sizes   
• Select the source memory device using "GUl_MEMDEV_Select(hSrc)", draw on it the data that will modify by applying the new effect Get the pointers of the source and destination memory devices for direct manipulation The API "void \* GUI_MEMDEV_GetDataPtr(GUI_MEMDEV_Handle hSrc)", will be used. Note that if the bitmap is 32 Bpp, its data pointer can be used directly as the source pointer

Using these pointers, the width and the height, apply the effect filter to the source data and write it to the destination memory device.

O Once modified the destination memory device can be displayed on the LCD screen GUI_MEMDEV_Select(0); GUI_MEMDEV_CopyToLCD(hDest);

# 4.13 How to add a new widget

On STemWin, widgets are seen as windows with enhanced functionalities.

So creating a new widget will be based on the creation of a window but with the capability to store additional data.

Which consists essentially on adding the following functions:

C Create" function which returns a handle to the created widget and allows setting callback function. o "Set" and "Get" functions to request and set widget specific properties. • Callback" function to process messages which were sent to the custom widget

For a step by step description of this please refer to this path https://www.segger.com/downloads/emwin/AN03002

# 5

# Performance and footprint

# 5.1

# LCD driver performance

Table 6 lists a set of tests used to measure the speed of the display driver.

Table 6. Speed test list   

<table><tr><td rowspan=1 colspan=1>Test name</td><td rowspan=1 colspan=1>Description</td></tr><tr><td rowspan=1 colspan=1>Test 1: Filling</td><td rowspan=1 colspan=1>Measures the speed of filing. An area of 64 * 64 pixels is filled withdifferent colors.</td></tr><tr><td rowspan=1 colspan=1>Test 2: Small fonts</td><td rowspan=1 colspan=1>Measures the speed of small character output. An area of 60 * 64 pixels isfilled with small-character text.</td></tr><tr><td rowspan=1 colspan=1>Test 3: Big fonts</td><td rowspan=1 colspan=1>Measures the speed of big character output. An area of 65 * 48 pixels isfilled with big-character text.</td></tr><tr><td rowspan=1 colspan=1>Test 4: Bitmap 1 bpp</td><td rowspan=1 colspan=1>Measures the speed of 1 bpp bitmaps. An area of 58 * 8 pixels is filledwith a 1 bpp bitmap.</td></tr><tr><td rowspan=1 colspan=1>Test 5: Bitmap 2 bpp</td><td rowspan=1 colspan=1>Measures the speed of 2 bpp bitmaps. An area of 32 * 11 pixels is filledwith a 2 bpp bitmap.</td></tr><tr><td rowspan=1 colspan=1>Test 6: Bitmap 4 bpp</td><td rowspan=1 colspan=1>Measures the speed of 4 bpp bitmaps. An area of 32 * 11 pixels is filledwith a 4 bpp bitmap.</td></tr><tr><td rowspan=1 colspan=1>Test 7: Bitmap 8 bpp</td><td rowspan=1 colspan=1>Measures the speed of 8 bpp bitmaps. An area of 32 * 11 pixels is filledwith an 8 bpp bitmap.</td></tr><tr><td rowspan=1 colspan=1>Test 8: Bitmap 16 bpp</td><td rowspan=1 colspan=1>Measures the speed of 16 bpp bitmaps. An area of 64 * 8 pixels is filledwith an 8 bpp bitmap.</td></tr></table>

The tests were done on the STM324xG-EVAL and STM324x9l-EVAL boards using respectively FlexColor and Lin drivers.

The results are shown in Table 7.

Table 7. Speed test for the FlexColor and Lin drivers   

<table><tr><td rowspan=1 colspan=1>Test name</td><td rowspan=1 colspan=1>FlexColor</td><td rowspan=1 colspan=1>Lin</td></tr><tr><td rowspan=1 colspan=1>Test 1: Filling</td><td rowspan=1 colspan=1>7.48 M</td><td rowspan=1 colspan=1>73.47 M</td></tr><tr><td rowspan=1 colspan=1>Test 2: Small fonts</td><td rowspan=1 colspan=1>1.57 M</td><td rowspan=1 colspan=1>4.16 M</td></tr><tr><td rowspan=1 colspan=1>Test 3: Big fonts</td><td rowspan=1 colspan=1>2.35 M</td><td rowspan=1 colspan=1>5.96 M</td></tr><tr><td rowspan=1 colspan=1>Test 4: Bitmap 1bpp</td><td rowspan=1 colspan=1>3.23 M</td><td rowspan=1 colspan=1>8.81 M</td></tr><tr><td rowspan=1 colspan=1>Test 5: Bitmap 2bpp</td><td rowspan=1 colspan=1>2.28 M</td><td rowspan=1 colspan=1>6.29 M</td></tr><tr><td rowspan=1 colspan=1>Test 6: Bitmap 4bpp</td><td rowspan=1 colspan=1>2.22 M</td><td rowspan=1 colspan=1>6.13 M</td></tr><tr><td rowspan=1 colspan=1>Test 7: Bitmap 8bpp</td><td rowspan=1 colspan=1>1.17 M</td><td rowspan=1 colspan=1>9.71 M</td></tr><tr><td rowspan=1 colspan=1>Test 8: Bitmap 16bpp</td><td rowspan=1 colspan=1>5.57 M</td><td rowspan=1 colspan=1>4.55 M</td></tr></table>

# 5.2 STemWin footprint

The operation area of STemWin varies widely, depending primarily on the application and features used. In the following sections, memory requirements of various modules are listed, as well as the memory requirements of example applications.

The following table shows the memory requirements of the main components of STemWin.   
These values depend a lot on the compiler options, the compiler version and the used CPU.   
Note that the listed values are the requirements of the basic functions of each module.

Table 8. Module footprint   

<table><tr><td rowspan=1 colspan=1>Component</td><td rowspan=1 colspan=1>ROM</td><td rowspan=1 colspan=1>RAM</td><td rowspan=1 colspan=1>Description</td></tr><tr><td rowspan=1 colspan=1>Windows Manager</td><td rowspan=1 colspan=1>6.2 Kbytes</td><td rowspan=1 colspan=1>2.5 Kbytes</td><td rowspan=1 colspan=1>Additional memory requirements ofbasic application when using theWindow Manager.</td></tr><tr><td rowspan=1 colspan=1>Memory Devices</td><td rowspan=1 colspan=1>4.7 Kbytes</td><td rowspan=1 colspan=1>7 Kbytes</td><td rowspan=1 colspan=1>Additional memory requirements of abasic application when using memorydevices.</td></tr><tr><td rowspan=1 colspan=1>Antialiasing</td><td rowspan=1 colspan=1>4.5 Kbytes</td><td rowspan=1 colspan=1>2 * LCD_XSIZE</td><td rowspan=1 colspan=1>Additional memory requirements forthe antialiasing software item.</td></tr><tr><td rowspan=1 colspan=1>Driver</td><td rowspan=1 colspan=1>2 - 8 Kbytes</td><td rowspan=1 colspan=1>20 bytes</td><td rowspan=1 colspan=1>The memory requirements of the driverdepend on the configured driver andwhether a data cache is used or not.With a data cache, the driver requiresmore RAM.</td></tr><tr><td rowspan=1 colspan=1>Multilayer</td><td rowspan=1 colspan=1>2 - 8 Kbytes</td><td rowspan=1 colspan=1></td><td rowspan=1 colspan=1>If working with a multi layer or a multidisplay configuration, additionalmemory is required for each additionallayer, because each requires its owndriver.</td></tr><tr><td rowspan=1 colspan=1>Core</td><td rowspan=1 colspan=1>5.2 Kbytes</td><td rowspan=1 colspan=1>80 bytes</td><td rowspan=1 colspan=1>Memory requirements of a typicalapplication without using additionalsoftware items.</td></tr><tr><td rowspan=1 colspan=1>JPEG</td><td rowspan=1 colspan=1>12 Kbytes</td><td rowspan=1 colspan=1>38 Kbytes</td><td rowspan=1 colspan=1>Basic routines for drawing JPEG files.</td></tr><tr><td rowspan=1 colspan=1>GIF</td><td rowspan=1 colspan=1>3.3 Kbytes</td><td rowspan=1 colspan=1>17 Kbytes</td><td rowspan=1 colspan=1>Basic routines for drawing GIF files.</td></tr><tr><td rowspan=1 colspan=1>Sprites</td><td rowspan=1 colspan=1>4.7 Kbytes</td><td rowspan=1 colspan=1>16 bytes</td><td rowspan=1 colspan=1>Routines for drawing sprites andcursors.</td></tr><tr><td rowspan=1 colspan=1>Font</td><td rowspan=1 colspan=1>1 - 4 Kbytes</td><td rowspan=1 colspan=1></td><td rowspan=1 colspan=1>Depends on the font size to be used.</td></tr></table>

Table 9. Widget footprint   

<table><tr><td rowspan=1 colspan=1>Component</td><td rowspan=1 colspan=1>ROM</td><td rowspan=1 colspan=1>RAM</td><td rowspan=1 colspan=1>Description</td></tr><tr><td rowspan=1 colspan=1>BUTTON</td><td rowspan=1 colspan=1>1 Kbyte</td><td rowspan=1 colspan=1>40 bytes</td><td rowspan=1 colspan=1>*1</td></tr><tr><td rowspan=1 colspan=1>CHECKBOX</td><td rowspan=1 colspan=1>1 Kbyte</td><td rowspan=1 colspan=1>52 bytes</td><td rowspan=1 colspan=1>*1</td></tr><tr><td rowspan=1 colspan=1>DROPDOWN</td><td rowspan=1 colspan=1>1.8 Kbytes</td><td rowspan=1 colspan=1>52 bytes</td><td rowspan=1 colspan=1>*1</td></tr><tr><td rowspan=1 colspan=1>EDIT</td><td rowspan=1 colspan=1>2.2 Kbytes</td><td rowspan=1 colspan=1>28 bytes</td><td rowspan=1 colspan=1>*1</td></tr><tr><td rowspan=1 colspan=1>FRAMEWIN</td><td rowspan=1 colspan=1>2.2 Kbytes</td><td rowspan=1 colspan=1>12 bytes</td><td rowspan=1 colspan=1>*1</td></tr><tr><td rowspan=1 colspan=1>GRAPH</td><td rowspan=1 colspan=1>2.9 Kbytes</td><td rowspan=1 colspan=1>48 bytes</td><td rowspan=1 colspan=1>*1</td></tr><tr><td rowspan=1 colspan=1>GRAPH_DATA_XY</td><td rowspan=1 colspan=1>0.7 Kbytes</td><td rowspan=1 colspan=1></td><td rowspan=1 colspan=1>*1</td></tr><tr><td rowspan=1 colspan=1>GRAPH_DATA_YT</td><td rowspan=1 colspan=1>0.6 Kbytes</td><td rowspan=1 colspan=1>-</td><td rowspan=1 colspan=1>*1</td></tr><tr><td rowspan=1 colspan=1>HEADER</td><td rowspan=1 colspan=1>2.8 Kbytes</td><td rowspan=1 colspan=1>32 bytes</td><td rowspan=1 colspan=1>*1</td></tr><tr><td rowspan=1 colspan=1>LISTBOX</td><td rowspan=1 colspan=1>3.7 Kbytes</td><td rowspan=1 colspan=1>56 bytes</td><td rowspan=1 colspan=1>*1</td></tr><tr><td rowspan=1 colspan=1>LISTVIEW</td><td rowspan=1 colspan=1>3.6 Kbytes</td><td rowspan=1 colspan=1>44 bytes</td><td rowspan=1 colspan=1>*1</td></tr><tr><td rowspan=1 colspan=1>MENU</td><td rowspan=1 colspan=1>5.7 Kbytes</td><td rowspan=1 colspan=1>52 bytes</td><td rowspan=1 colspan=1>*1</td></tr><tr><td rowspan=1 colspan=1>MULTIEDIT</td><td rowspan=1 colspan=1>7.1 Kbytes</td><td rowspan=1 colspan=1>16 bytes</td><td rowspan=1 colspan=1>*1</td></tr><tr><td rowspan=1 colspan=1>MULTIPAGE</td><td rowspan=1 colspan=1>3.9 Kbytes</td><td rowspan=1 colspan=1>32 bytes</td><td rowspan=1 colspan=1>*1</td></tr><tr><td rowspan=1 colspan=1>PROGBAR</td><td rowspan=1 colspan=1>1.3 Kbytes</td><td rowspan=1 colspan=1>20 bytes</td><td rowspan=1 colspan=1>*1</td></tr><tr><td rowspan=1 colspan=1>RADIOBUTTON</td><td rowspan=1 colspan=1>1.4 Kbytes</td><td rowspan=1 colspan=1>32 bytes</td><td rowspan=1 colspan=1>*1</td></tr><tr><td rowspan=1 colspan=1>SCROLLBAR</td><td rowspan=1 colspan=1>2 Kbytes</td><td rowspan=1 colspan=1>14 bytes</td><td rowspan=1 colspan=1>*1</td></tr><tr><td rowspan=1 colspan=1>SLIDER</td><td rowspan=1 colspan=1>1.3 Kbytes</td><td rowspan=1 colspan=1>16 bytes</td><td rowspan=1 colspan=1>*1</td></tr><tr><td rowspan=1 colspan=1>TEXT</td><td rowspan=1 colspan=1>1 Kbyte</td><td rowspan=1 colspan=1>16 bytes</td><td rowspan=1 colspan=1>*1</td></tr><tr><td rowspan=1 colspan=1>CALENDAR</td><td rowspan=1 colspan=1>0.6 Kbyte</td><td rowspan=1 colspan=1>32 bytes</td><td rowspan=1 colspan=1>*1</td></tr></table>

# FAQs (frequently asked questions)

This section gathers some of the most frequent questions STemWin Library package users may ask, and provides some solutions and tips.

Table 10. FAQs   

<table><tr><td rowspan=1 colspan=1>No.</td><td rowspan=1 colspan=1>Question</td><td rowspan=1 colspan=1>Answer/solution</td></tr><tr><td rowspan=1 colspan=1>1</td><td rowspan=1 colspan=1>Are all the STemWin featuresincluded in the package?</td><td rowspan=1 colspan=1>Yes. The delivered locked binaries where compiled withall the features enabled.</td></tr><tr><td rowspan=1 colspan=1>2</td><td rowspan=1 colspan=1>What is the STemWin Libraryconfiguration (during the binarygeneration)?</td><td rowspan=1 colspan=1>The content of the &quot;GUlConf.h&quot; file used to generate theSTemWin binaries is as follows:#define GUI_DEFAULT_FONT      &amp;GUI_Font6x8#define GUI_NUM_LAYERS                          2#define GUI_SUPPORT_TOUCH                    (1)#define GUI_SUPPORT_MOUSE                    (1)#define GUI_WINSUPPORT                         (1)#define GUI_SUPPORT_MEMDEV                  (1)#define GUI_SUPPORT_DEVICES                  (1)#define BUTTON_REACT_ON_LEVEL             (1)#define GUI_MEMDEV_SUPPORT_CUSTOMDRAW (1)#define GUI_USE_ARGB                             (1)</td></tr><tr><td rowspan=1 colspan=1>3</td><td rowspan=1 colspan=1>Isn&#x27;t the delivered binary toolarge?</td><td rowspan=1 colspan=1>No. It depends on the application. The compilerconsiders only called parts from the external functions;thus, non-used resources are not included in the finalapplication size.</td></tr><tr><td rowspan=1 colspan=1>4</td><td rowspan=1 colspan=1>How can a new LCD controller besupported?</td><td rowspan=1 colspan=1>To support any kind of LCD controller, the user shouldimplement two configuration files:LCDConf.c/.hGUIConf.c/.hSection 4.1 describes in detail the content of those files.</td></tr><tr><td rowspan=1 colspan=1>5</td><td rowspan=1 colspan=1>Is it mandatory to use theFreeRTOS operating system?</td><td rowspan=1 colspan=1>No. Any other operating system can be used. But then acorresponding GUI_X_OS.c file is needed (seeSection 4.1.4).</td></tr><tr><td rowspan=1 colspan=1>6</td><td rowspan=1 colspan=1>The project is compiled withouterrors but, when running theapplication, the display does notwork.</td><td rowspan=1 colspan=1>This issue may be caused by one of the following:Stack size is too low.Wrong initialization of the display controller.Wrong configuration of the display interface.</td></tr></table>

# 7 Revision history

Table 11. Document revision history   

<table><tr><td rowspan=1 colspan=1>Date</td><td rowspan=1 colspan=1>Revision</td><td rowspan=1 colspan=1>Changes</td></tr><tr><td rowspan=1 colspan=1>19-Jul-2013</td><td rowspan=1 colspan=1>1</td><td rowspan=1 colspan=1>Initial release.</td></tr><tr><td rowspan=1 colspan=1>07-Feb-2014</td><td rowspan=1 colspan=1>2</td><td rowspan=1 colspan=1>- The use of STemWin generic version (XYZ).- The support of STM324x9I-EVAL board.</td></tr><tr><td rowspan=1 colspan=1>20-Mar-2014</td><td rowspan=1 colspan=1>3</td><td rowspan=1 colspan=1>- Added reference to STM32CubeF2 andSTM32CubeF4</td></tr><tr><td rowspan=1 colspan=1>25-Jun-2014</td><td rowspan=1 colspan=1>4</td><td rowspan=1 colspan=1>Added STM32CubeF3 in the list of applicable software.</td></tr><tr><td rowspan=1 colspan=1>04-Apr-2018</td><td rowspan=1 colspan=1>5</td><td rowspan=1 colspan=1>Updated Table 1: Applicable Software, Figure 1:STemWin layers, Section 2.2: Library description,Table 2: Supported LCD controllers, Figure 2: Projecttree, Section 2.4: Delivered binaries, Table 3: Supportedboards and examples, Figure 3: Structure of theSTemWin application, Section 3: Supported boards andexamples, Section 4.1: Configuration, Section 4.1.1:GUIConf.c, Section 4.1.2: LCDConf.c, Section 4.1.4:GUI_X.c or GUI_X_OS.c, Section 4.2: GUI initialization,Figure 25, Table 10: FAQsAdded Figure 4: STemWin initialization, Section 4.1.3:Hardware acceleration, Section 4.9.2: How to add a newfont, Section 4.9.3: Language support, Section 4.11:Porting GUI on a different resolution, Section 4.12: Howto add a new effect, Section 4.13: How to add a newwidget</td></tr></table>

# IMPORTANT NOTICE  PLEASE READ CAREFULLY

acknowledgement.

the design of Purchasers' products.

No license, express or implied, to any intellectual property right is granted by ST herein.

I