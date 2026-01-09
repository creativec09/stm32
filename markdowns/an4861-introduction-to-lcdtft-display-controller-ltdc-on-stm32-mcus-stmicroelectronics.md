# Introduction to LCD-TFT display controller (LTDC) on STM32 MCUs

# Introduction

soareesours kememory r raphical riitivsrmebufer), adhigherprocessng peormas.

portfolio.

CoC memories to fetch pixel data.

the best graphical performances.

Table 1. Applicable products   

<table><tr><td>Type</td><td>Products</td></tr><tr><td></td><td>STM32F429/439 and STM32F469/479 lines STM32F7x6, STM32F7x7, STM32F7x8, and STM32F7x9 lines</td></tr><tr><td></td><td>STM32H7A3/B3, STM32H723/733, STM32H725/735, STM32H742, STM32H743/753, STM32H745/755,</td></tr><tr><td></td><td>STM32H747/757 lines</td></tr><tr><td>STM32 MCUs</td><td>STM32H7B0, STM32H730, STM32H750 value lines</td></tr><tr><td></td><td>STM32H7R3/7S3 and STM32H7R7/7S7 lines</td></tr><tr><td></td><td>STM32L4+ series</td></tr><tr><td></td><td>STM32U595/5A5, STM32U599/5A9, STM32U5F7/5G7, STM32U5F9/5G9 lines STM32N6 series</td></tr></table>

# 1 General information

# Note:

This document applies to STM32 Arm®-based microcontrollers Arm is a registered trademark of Arm Limited (or its subsidiaries) in the US and/or elsewhere.

# arm

# Reference documents

[1] Application note TFT LCD interfacing with the high-density STM32F10xxx FSMC (AN2790)   
[2] Application note QVGA TFT-LCD direct drive using the STM32F10xx FSMC peripheral (AN3241)   
[3] Application note DSI Host on STM32F469/479, STM32F7x8/x9, and STM32L4R9/S9 MCUs (AN4860)   
[4] Application note Quad-SPI interface on STM32 microcontrollers and microprocessors (AN4760)   
[5] Application note Octo-SPI interface on STM32 microcontrollers (AN5050)   
[6] Application note Managing memory protection unit in STM32 MCUs (AN4838)   
[7] Application note Level 1 cache on STM32F7 series and STM32H7 series (AN4839)   
[8] Programming manual STM32F7 series and STM32H7 series Cortex-M7 processor programming manual (PM0253)   
[9] Application note Quad-SPI (QSPI) interface on STM32 microcontrollers (AN4760)   
[10] Application note Getting started with STM32F7 series MCU hardware development (AN4661)   
[11] Application note Getting started with STM32F4xxxx MCU hardware development (AN4488)   
[12] User manual Discovery kit for STM32F7 series with STM32F746NG MCU (UM1907)

# 2 Display and graphics overview

Tneeaspay hontx  rovie general display and graphics nvinmentThis ection alo marizes hedisplayiterfacs ur by the STM32 Arm-based MCUs.

# Basic graphics concepts

This section describes a basic embedded graphic system, the display module categories and the display technologies.

# Basic embedded graphic system

A basic embedded graphic system schematic is described in Figure 1.

![](images/b0d94ee76a204574fa88e56d21e5e0a06f2342b787288564015aeb044c9433c8.jpg)  
Figure 1. Basic embedded graphic system

Abasibede graphi syste iscmpose amioconroller aramebuffer display controllerand a display glass.

The MCU computes the image to be displayed in the framebur, assembling graphical primitives such as icons or images. The CPU performs this operation by running a graphical library software. This process can be accelerated by a dedicated hardware like the DMA2D Chrom-Art Accelerator, used by the graphical library. The more often the framebuffer is updated, the more fluent the animations are (animation fs).

The ramebur is  volatilmemory used o store piel dataf themage o edisplayeThis memory is usually called the graphic RAM (GRAM). The required size of the framebuffer depends on the resolution and color depth of the display. See Section 5.2.: Framebuffer memory size requirements and location for more information on the required size of the framebuffer.

Double buffering isa tecnique that uses double amebuffers oavoiddisplaying what is beigwriten to the framebuffer.

Tiyntoltheipyeeufontn display glass 60 times per second (60 Hz). The display controller can be embedded either in the display module or in the MCU.

The display glass is driven by the display controller and is responsible to display the image that is composed of a matrix of pixels.

A display is characterized by:

Diplay size resolution): is defined by the numberof pixels of the display that is represented by horizontal (pixels number) x vertical (lines number).   
Cdefeclo  whi  i nrawIn pixel (bpp). For a color depth of 24 bpp (that can also be represented by RGB888) a pixel can be represented in 16777216 colors.   
Refresh rate in Hz): is the umber oftmes per second that the display panel s refreshed.A display must be refreshed 60 times per seconds (60 Hz) since lower refresh rate creates bad visual effects.

# Display module categories

The displaymodules are classified in twomain categorie, epending on whether they embedor ot antal controller and a GRAM:

The first category corresponds to the displays with an on-glass display controller and a GRAM (see Figure 2).   
The second category corresponds to the displays with anon-glass display with no main controller and that have only a low-level timing controller.   
Tointerface with displays without controller nor GRAM, the used framebuffer can be located in the MCU internal SRAM (see Figure 3) or located in an external memory (see Figure 4).

![](images/4c93904b51eb41d9e5799b3509f7dfdad918c6619f95a598282c0108cc12948f.jpg)  
Figure 2. Display module with embedded controller and GRAM

![](images/e94dca6e6fd7505bd67899fa0fcba1ccfe6c60263331b9aac56dc9656244c2c5.jpg)  
Figure 3. Display module without controller nor GRAM

![](images/b3b43ef0d90668fffa9d77c05da08a1225db28d5949fa68608f8ee53a02937a5.jpg)  
Figure 4. Display module without controller nor GRAM and with external framebuffer

# Display technologies

There are many display echnologies available on the market. The two main technologis used are desced below.

LCD-TFT isplays iqui cystal ispay  thin flmransisor):vran  LCD that uses heFT te to improve the control of each pixel. Thanks to the TFT technology, each pixel can be controlled by a transistor, allowing a fast response time and an accurate color control.   
OLED displays (organic LED): pixels made of organic LEDs emitting directly the light, offering a better contrast and an optimized consumption. The OLED technology enables the possibility to use flexible displays, as no glass nor backlight are required. The response time is very fast and the viewing angle is free as it does not depend on any light polarization.

TL backlight requirement, as the OLED does not require any.

# Display interface standards

T® mousy ro teacAlli gloalcollaboativrganizatincit define and proote nterace speciiations oobiledevis.The Alince develops new standars ut also standardizes the existing display interfaces:

# MIPI display bus interface (MIPI-DBI)

T I. The three types of interfaces defined inside the MiPI-DBI are:

Type A: based on Motorola 6800 bus Type B: based on Intel® 8080 bus Type C: based on SPI protocol

The MIPI-DBI is used to interface with a display with an integrated graphic RAM (GRAM). The pixel data is u AP

![](images/8a9e44cd987cd480baf4543e17793169ff21ab614403cae1734ab3060a4b3efb.jpg)  
Figure 5. MIPI-DBI type A or B interface

![](images/6caa55b16b699e051621273b7307387068cdb5cb3376d4d1477623b48e9eee8c.jpg)  
Figure 6 illustrates an MPI-DBI type C display interfacing example.   
Figure 6. MIPI-DBI type C interface

# MIPI display parallel interface (MIPI-DPI)

The DPI standardizes the interface through a TFT controller.An example is when using a 16-bit to -bt RGB signaling with synchronization signals (HSYNC, VSYNC, EN and LCD_CLK).

T is display.

The real-time peformance  excellent but requires a high bandwidth in the MCU to feed the display.

![](images/455ff088a1609d62c3804dd9c33776f19f20209cd8d3670e9fd9201b2be63701.jpg)  
Figure 7. MIPI-DPI interface

# MIPI display serial interface (MIPI-DSI)

In  yeP DSI is a high bandwidth multilane differential link; it uses standard MIPI D-PHY for the physical link. The DSI encapsulates either DBI or DPI signals and transmits them to the D-PHY through the PPI protocol.

![](images/422e6a78e1a3a84548d6a1d17cf5019041302bc683b975f4e5f40db0957bc1bc.jpg)  
Figure 8. MIPI-DSI interface

# 2.3

# Display interfaces supported by STM32 MCUs

Here below a summary on the MIPI Alliance display interfaces supported by STM32 MCUs:

All STM32 MCUs support the MIPI-DBI type C (SPI) interface.   
All STM32 MCUs with F(S)MC support the MIPI-DBI type A and B interfaces.   
STM32 MCUs with LTDC support the MIPI-DPI interface.   
STM32 MCUs embedding a DSI Host support the MIPI-DSI interface.

Table 2 ilustrates and summarizes the display interfaces supported by the STM32 microcontrollers.

Table 2. . Display interfaces supported by STM32 MCUs   

<table><tr><td colspan="2">Display interface</td><td colspan="2">Connecting display panels to STM32 MCU(1)</td></tr><tr><td rowspan="2">DBI(2)</td><td>Motorola 6800 DBI Type A</td><td>Cortex-M DMA</td><td rowspan="2">Display module Display ST</td></tr><tr><td>Intel 8080 DBI Type B</td><td>controller AHB 1 DBI GRAM RAM Flash FMC</td></tr></table>

![](images/fb9bf1eb645c4a5fbf4103b8b494d2f9d30b83ad1da36d9326875dccd0d9bd3b.jpg)

Purple arrows show the pixel data path to the display.   
o mo ratin n how uppor Motooa 6800 and Intel 8080 wi TM32 F()C, ee  the ocen [].   
heTM3 MCUs with  LTDC perhal cane driveLCD-FT pan usig FSMC and DMARe document [2].   
4. CUT Hos  e [] for more information.

# 3 Overview of LTDC controller and STM32 MCUs graphical portfolio

This section illustrates the LTDC controller benefits and summarizes the graphical portfolio of the STM32 microcontrollers.

# 3.1

# LCD-TFT display controller on STM32 MCUs

The LTDC o the TM32 miotrollers  an n-chip LCD ispa controller that provies up to -bit parlle iitalRG al ce witvru spa pans.enlsodrvhepay w paralle GiteaceikeheMOLEisplase LCallow teaci wit ow-osisplay l that do not embed neither a controller nor a graphic RAM.

# LTDC and graphic portfolio across STM32 MCUs

Tablesumarize he TM32 MCUs ebeding anLTDC and details he corponding availablegraphic poro.

Table 3. STM32 MCUs embedding an LTDC and their available graphic portfolio   

<table><tr><td rowspan=1 colspan=1>Device</td><td rowspan=1 colspan=1>FLASH(bytes)</td><td rowspan=1 colspan=1>On shipSRAM(bytes)</td><td rowspan=1 colspan=1>(b)|dS-pn0</td><td rowspan=1 colspan=1>20</td><td rowspan=1 colspan=1>20</td><td rowspan=1 colspan=1>MaxAHB/AXIffrequency(MHz)(2)</td><td rowspan=1 colspan=1>Max FMCSDRAMfrequencyMHz)</td><td rowspan=1 colspan=1>MaxOcto-SPIfrequencyMHz)</td><td rowspan=1 colspan=1>MaxHex-SPIfrequcyMHZz)</td><td rowspan=1 colspan=1>Maxpixelclock(MHz)(3)</td><td rowspan=1 colspan=1>20</td><td rowspan=1 colspan=1>(t)∀2(</td><td rowspan=1 colspan=1>()]Soy ISO-IdIW</td><td rowspan=1 colspan=1>weoo-oom0</td><td rowspan=20 colspan=2>GraphiclibrariesTouchGFXmbeddedwizardSEGGERSTemWin</td></tr><tr><td rowspan=1 colspan=1>STM32F429/439</td><td rowspan=1 colspan=1>Up to 2 M</td><td rowspan=1 colspan=1>256 K</td><td rowspan=1 colspan=1>No</td><td rowspan=1 colspan=1>No</td><td rowspan=1 colspan=1>No</td><td rowspan=1 colspan=1>180</td><td rowspan=1 colspan=1>90</td><td rowspan=1 colspan=1>-</td><td rowspan=1 colspan=1>-</td><td rowspan=1 colspan=1>83</td><td rowspan=1 colspan=1>No</td><td rowspan=1 colspan=1>Yes</td><td rowspan=1 colspan=1>No</td><td rowspan=1 colspan=1>No</td></tr><tr><td rowspan=1 colspan=1>STM32F469/479</td><td rowspan=1 colspan=1>Up to 2 M</td><td rowspan=1 colspan=1>384 K</td><td rowspan=1 colspan=1>Yes</td><td rowspan=1 colspan=1>No</td><td rowspan=1 colspan=1>No</td><td rowspan=1 colspan=1>180</td><td rowspan=1 colspan=1>90</td><td rowspan=1 colspan=1>-</td><td rowspan=1 colspan=1></td><td rowspan=1 colspan=1>83</td><td rowspan=1 colspan=1>No</td><td rowspan=1 colspan=1>Yes</td><td rowspan=1 colspan=1>Yes</td><td rowspan=1 colspan=1>No</td></tr><tr><td rowspan=1 colspan=1>STM32F7x6</td><td rowspan=1 colspan=1>Up to 1 M</td><td rowspan=1 colspan=1>320 K</td><td rowspan=1 colspan=1>Yes</td><td rowspan=1 colspan=1>No</td><td rowspan=1 colspan=1>No</td><td rowspan=1 colspan=1>216</td><td rowspan=1 colspan=1>100</td><td rowspan=1 colspan=1>-</td><td rowspan=1 colspan=1></td><td rowspan=1 colspan=1>83</td><td rowspan=1 colspan=1>No</td><td rowspan=1 colspan=1>Yes</td><td rowspan=1 colspan=1>No</td><td rowspan=1 colspan=1>No</td></tr><tr><td rowspan=1 colspan=1>STM32F7x7</td><td rowspan=1 colspan=1>Up to 2 M</td><td rowspan=1 colspan=1>512 K</td><td rowspan=1 colspan=1>Yes</td><td rowspan=1 colspan=1>No</td><td rowspan=1 colspan=1>No</td><td rowspan=1 colspan=1>216</td><td rowspan=1 colspan=1>100</td><td rowspan=1 colspan=1>-</td><td rowspan=1 colspan=1></td><td rowspan=1 colspan=1>83</td><td rowspan=1 colspan=1>Yes</td><td rowspan=1 colspan=1>Yes</td><td rowspan=1 colspan=1>No</td><td rowspan=1 colspan=1>No</td></tr><tr><td rowspan=1 colspan=1>STM32F7x8/9</td><td rowspan=1 colspan=1>Up to 2 M</td><td rowspan=1 colspan=1>512 K</td><td rowspan=1 colspan=1>Yes</td><td rowspan=1 colspan=1>No</td><td rowspan=1 colspan=1>No</td><td rowspan=1 colspan=1>216</td><td rowspan=1 colspan=1>100</td><td rowspan=1 colspan=1>-</td><td rowspan=1 colspan=1></td><td rowspan=1 colspan=1>83</td><td rowspan=1 colspan=1>Yes</td><td rowspan=1 colspan=1>Yes</td><td rowspan=1 colspan=1>Yes</td><td rowspan=1 colspan=1>No</td></tr><tr><td rowspan=1 colspan=1>STM32H7A3/B3</td><td rowspan=1 colspan=1>Up to 2 M</td><td rowspan=1 colspan=1>1.4 M</td><td rowspan=1 colspan=1>No</td><td rowspan=1 colspan=1>Yes</td><td rowspan=1 colspan=1>No</td><td rowspan=1 colspan=1>280</td><td rowspan=1 colspan=1>110</td><td rowspan=1 colspan=1>140</td><td rowspan=1 colspan=1>-</td><td rowspan=1 colspan=1>140</td><td rowspan=1 colspan=1>Yes</td><td rowspan=1 colspan=1>Yes</td><td rowspan=1 colspan=1>No</td><td rowspan=1 colspan=1>No</td></tr><tr><td rowspan=1 colspan=1>STM32H7B0</td><td rowspan=1 colspan=1>128 K</td><td rowspan=1 colspan=1>1.4 M</td><td rowspan=1 colspan=1>No</td><td rowspan=1 colspan=1>Yes</td><td rowspan=1 colspan=1>No</td><td rowspan=1 colspan=1>280</td><td rowspan=1 colspan=1>110</td><td rowspan=1 colspan=1>140</td><td rowspan=1 colspan=1>-</td><td rowspan=1 colspan=1>140</td><td rowspan=1 colspan=1>Yes</td><td rowspan=1 colspan=1>Yes</td><td rowspan=1 colspan=1>No</td><td rowspan=1 colspan=1>No</td></tr><tr><td rowspan=1 colspan=1>STM32H742/43/45/53/55</td><td rowspan=1 colspan=1>Up to 2 M</td><td rowspan=1 colspan=1>1M</td><td rowspan=1 colspan=1>Yes</td><td rowspan=1 colspan=1>No</td><td rowspan=1 colspan=1>No</td><td rowspan=1 colspan=1>240</td><td rowspan=1 colspan=1>110</td><td rowspan=1 colspan=1>-</td><td rowspan=1 colspan=1>-</td><td rowspan=1 colspan=1>150</td><td rowspan=1 colspan=1>Yes</td><td rowspan=1 colspan=1>Yes</td><td rowspan=1 colspan=1>No</td><td rowspan=1 colspan=1>No</td></tr><tr><td rowspan=1 colspan=1>STM32H747/57</td><td rowspan=1 colspan=1>Up to 2 M</td><td rowspan=1 colspan=1>1M</td><td rowspan=1 colspan=1>Yes</td><td rowspan=1 colspan=1>No</td><td rowspan=1 colspan=1>No</td><td rowspan=1 colspan=1>240</td><td rowspan=1 colspan=1>110</td><td rowspan=1 colspan=1>-</td><td rowspan=1 colspan=1>-</td><td rowspan=1 colspan=1>150</td><td rowspan=1 colspan=1>Yes</td><td rowspan=1 colspan=1>Yes</td><td rowspan=1 colspan=1>Yes</td><td rowspan=1 colspan=1>No</td></tr><tr><td rowspan=1 colspan=1>STM32H750</td><td rowspan=1 colspan=1>128 K</td><td rowspan=1 colspan=1>1M</td><td rowspan=1 colspan=1>Yes</td><td rowspan=1 colspan=1>No</td><td rowspan=1 colspan=1>No</td><td rowspan=1 colspan=1>240</td><td rowspan=1 colspan=1>110</td><td rowspan=1 colspan=1>-</td><td rowspan=1 colspan=1>-</td><td rowspan=1 colspan=1>150</td><td rowspan=1 colspan=1>Yes</td><td rowspan=1 colspan=1>Yes</td><td rowspan=1 colspan=1>No</td><td rowspan=1 colspan=1>No</td></tr><tr><td rowspan=1 colspan=1>STM32H7R7/7S7</td><td rowspan=1 colspan=1>Up to 64 K</td><td rowspan=1 colspan=1>Up to 488 K</td><td rowspan=1 colspan=1>Yes</td><td rowspan=1 colspan=1>Yes</td><td rowspan=1 colspan=1>Yes</td><td rowspan=1 colspan=1>300</td><td rowspan=1 colspan=1>100</td><td rowspan=1 colspan=1>200</td><td rowspan=1 colspan=1>200</td><td rowspan=1 colspan=1>90</td><td rowspan=1 colspan=1>Yes</td><td rowspan=1 colspan=1>Yes</td><td rowspan=1 colspan=1>No</td><td rowspan=1 colspan=1>Yes</td></tr><tr><td rowspan=1 colspan=1>STM32L4P/Q</td><td rowspan=1 colspan=1>Up to 1 M</td><td rowspan=1 colspan=1>320 K</td><td rowspan=1 colspan=1>No</td><td rowspan=1 colspan=1>Yes</td><td rowspan=1 colspan=1>No</td><td rowspan=1 colspan=1>120</td><td rowspan=1 colspan=1>60(6)</td><td rowspan=1 colspan=1>92</td><td rowspan=1 colspan=1>-</td><td rowspan=1 colspan=1>83</td><td rowspan=1 colspan=1>No</td><td rowspan=1 colspan=1>Yes</td><td rowspan=1 colspan=1>No</td><td rowspan=1 colspan=1>No</td></tr><tr><td rowspan=1 colspan=1>STM32L4R/S</td><td rowspan=1 colspan=1>Up to 2 M</td><td rowspan=1 colspan=1>640 K</td><td rowspan=1 colspan=1>No</td><td rowspan=1 colspan=1>Yes</td><td rowspan=1 colspan=1>No</td><td rowspan=1 colspan=1>120</td><td rowspan=1 colspan=1>60(6)</td><td rowspan=1 colspan=1>86</td><td rowspan=1 colspan=1>-</td><td rowspan=1 colspan=1>83</td><td rowspan=1 colspan=1>No</td><td rowspan=1 colspan=1>Yes</td><td rowspan=1 colspan=1>Yes</td><td rowspan=1 colspan=1>No</td></tr><tr><td rowspan=1 colspan=1>STM32H723/33/25/35</td><td rowspan=1 colspan=1>Up to 1 M</td><td rowspan=1 colspan=1>564 K</td><td rowspan=1 colspan=1>No</td><td rowspan=1 colspan=1>Yes</td><td rowspan=1 colspan=1>275</td><td rowspan=1 colspan=1>-</td><td rowspan=1 colspan=1>95</td><td rowspan=1 colspan=1>150</td><td rowspan=1 colspan=1>-</td><td rowspan=1 colspan=1>No</td><td rowspan=1 colspan=1>Yes</td><td rowspan=1 colspan=1>No</td><td rowspan=1 colspan=1>No</td><td rowspan=1 colspan=1>No</td></tr><tr><td rowspan=1 colspan=1>STM32H730</td><td rowspan=1 colspan=1>128 K</td><td rowspan=1 colspan=1>564 K</td><td rowspan=1 colspan=1>No</td><td rowspan=1 colspan=1>Yes</td><td rowspan=1 colspan=1>275</td><td rowspan=1 colspan=1>-</td><td rowspan=1 colspan=1>95</td><td rowspan=1 colspan=1>150</td><td rowspan=1 colspan=1>-</td><td rowspan=1 colspan=1>No</td><td rowspan=1 colspan=1>Yes</td><td rowspan=1 colspan=1>No</td><td rowspan=1 colspan=1>No</td><td rowspan=1 colspan=1>No</td></tr><tr><td rowspan=1 colspan=1>STM32U5Fx/5Gx</td><td rowspan=1 colspan=1>Up to 4 M</td><td rowspan=1 colspan=1>Up to 3 M</td><td rowspan=1 colspan=1>No</td><td rowspan=1 colspan=1>Yes</td><td rowspan=1 colspan=1>Yes</td><td rowspan=1 colspan=1>160</td><td rowspan=1 colspan=1>80(6)</td><td rowspan=1 colspan=1>100</td><td rowspan=1 colspan=1>160</td><td rowspan=1 colspan=1>116</td><td rowspan=1 colspan=1>Yes</td><td rowspan=1 colspan=1>Yes</td><td rowspan=1 colspan=1>No</td><td rowspan=1 colspan=1>Yes</td></tr><tr><td rowspan=1 colspan=1>STM32U59x/5Ax</td><td rowspan=1 colspan=1>Up to 4 M</td><td rowspan=1 colspan=1>Up to 2.5 M</td><td rowspan=1 colspan=1>No</td><td rowspan=1 colspan=1>Yes</td><td rowspan=1 colspan=1>Yes</td><td rowspan=1 colspan=1>160</td><td rowspan=1 colspan=1>80(6)</td><td rowspan=1 colspan=1>100</td><td rowspan=1 colspan=1>160</td><td rowspan=1 colspan=1>116</td><td rowspan=1 colspan=1>No</td><td rowspan=1 colspan=1>Yes</td><td rowspan=1 colspan=1>Yes</td><td rowspan=1 colspan=1>Yes</td></tr><tr><td rowspan=1 colspan=1>STM32H7R7/7S7</td><td rowspan=1 colspan=1>Up to 64 K</td><td rowspan=1 colspan=1>Up to 488 K</td><td rowspan=1 colspan=1>Yes</td><td rowspan=1 colspan=1>Yes</td><td rowspan=1 colspan=1>Yes</td><td rowspan=1 colspan=1>300</td><td rowspan=1 colspan=1>100</td><td rowspan=1 colspan=1>200</td><td rowspan=1 colspan=1>200</td><td rowspan=1 colspan=1>90</td><td rowspan=1 colspan=1>Yes</td><td rowspan=1 colspan=1>Yes</td><td rowspan=1 colspan=1>No</td><td rowspan=1 colspan=1>Yes</td></tr><tr><td rowspan=1 colspan=1>STM32N6x7/6x5</td><td rowspan=1 colspan=1>-</td><td rowspan=1 colspan=1>Up to 4.5 M</td><td rowspan=1 colspan=1>Yes</td><td rowspan=1 colspan=1>Yes</td><td rowspan=1 colspan=1>Yes</td><td rowspan=1 colspan=1>400</td><td rowspan=1 colspan=1>100</td><td rowspan=1 colspan=1>200</td><td rowspan=1 colspan=1>200</td><td rowspan=1 colspan=1>86</td><td rowspan=1 colspan=1>Yes</td><td rowspan=1 colspan=1>Yes</td><td rowspan=1 colspan=1>No</td><td rowspan=1 colspan=1>Yes</td></tr></table>

2. LTDC fetches graphical data at AHB/AXI speed. Chrom-Art Accelerator . MIPI-DSI host, refr t the document [].

# 3.3

# LTDC in a smart architecture

The LTDC  a master n heHB arhtecture hat pefors read acss on interal anexternal memors. Te LTDC has two independent layers, each one with its own FIFO enabling more flexibility of the display.

The LTDCntrolleusy c ahicl ate spee AHB us ombu.T graphical data is then stored in one of the FiFO internal layers then driven to the display.

Th tearhitecurllws aphi e uil n plott hecrewihout y  tevent. T LTChA a.

The LTDC interface is integrated in a smart architecture allowing:

LTDC autonomously fetches the graphical data from the framebuffer (can be internal memories such as internal flash, internal SRAM or external memories, such as FMC_SDRAM or Quad-SPI) and drives it to the display. DMA2D, as an AHB master, can be used to offload the CPU from graphics intensive tasks. LTDC is able to continue displaying graphics even in Sleep mode when the CPU does not run. The multilayer AHB bus architecture improves memories throughput and leads to higher performance.

# ystem architecture on STM32F429/439 and STM32F469/479 microcontrollers

The system architecture of the STM32F429/439 line and the STM32F469/479 line consists mainly of 32-bit multilayerAHB bus matrix that interconnects te masters and nine slaves (eight slaves for the STM32F429/F39). The LTDC is one of the ten AHB masters on the AHB bus matrix.

The LTDC can autonomously access all the memory slaves on the AHB bus matrix, such as FLASH, SRAM1, SRAM2, SRAM3 FMCor Quad-SPI enabling an efficient data transfer that is ideal for graphical applications.

Figure 9 shows the LTDC interconnection in the STM32F429/439 and STM32F469/479 lines systems.

(1) SRAM1 size = 112 Kbytes for STM32F429/439 and 160 Kbytes for STM32F469/479.   
(2) SRAM2 size = 16 Kbytes for STM32F429/439 and 32 Kbytes for STM32F469/479.   
(3) SRAM3 size = 64 Kbytes for STM32F429/439 and 128 Kbytes for STM32F469/479.   
(4) Dual Quad-SPI interface is only available for STM32F469/479.

![](images/434bc79d684dce754e27d1ba0a7f0d570c9020dc0e7b2d8fde56a37403ac2449.jpg)  
Figure 9. LTDC AHB master in STM32F429/439 and STM32F469/479 smart architecture

# System architecture on STM32F7x6, STM32F7x7, STM32F7x8, and STM32F7x9

The system architecture of the STM32F7x6, STM32F7x7, STM32F7x8, and STM32F7x9 consists mainly of 32-bit ultilHuaia e twevase  h saveLThewelH masters on the AHB bus matrix.

The LTDC can autonomously access ll the memory slaves on the AHB bus matrix, such as FLASH, SRAM1, SRAM MCQuaSPabling efcnt datranserha eal ohial platis shows the LTDC interconnection in the STM32F7x6, STM32F7x7, STM32F7x8, and STM32F7x9 systems.

Figure 10. LTDC AHB master in STM32F7x6, STM32F7x7, STM32F7x8, and STM32F7x9 smart architecture

(1) I/D Cache size = 4 Kbytes for STM32F7x6.   
I/D Cache size = 16 Kbytes for STM32F7x7, STM32F7x8, and STM32F7x9.   
(2) DTCM RAM size = 64 Kbytes for STM32F7x6.   
DTCM RAM size = 128 Kbytes for STM32F7x7, STM32F7x8, and STM32F7x9.   
(3) ITCM RAM size = 16 Kbytes for STM32F7x6, STM32F7x7, STM32F7x8, and STM32F7x9.   
(4) SRAM1 size = 240 Kbytes for STM32F7x6.   
SRAM1 size = 368 Kbytes for STM32F7x7, STM32F7x8, and STM32F7x9.   
(5) SRAM2 size = 16 Kbytes for STM32F7x6, STM32F7x7, STM32F7x8, and STM32F7x9.

![](images/81d7532ebb9243fba6d81a560e1627ef56762e6211041e6cc88f66b9474986c0.jpg)

# System architecture on STM32H7Rx/7Sx

The system architecture of the STM32H7Rx/7Sx primarily consists f a 64-bit AXI, a 32-bit multilayer AHB bus a  v ua 11 masters and 10 slaves. The LTDC is one of the 11 AXI masters on the AXI bus matrix. The LTDC can autonomously access al the memory slaves on the AHB bus matrix, such as FLASH, SRAM1, SRAM2, FMC, or XSPl, enabling efficient data transfer ideal for graphical applications.

I/D Cache size = 32 Kbytes DTCM RAM size = 64 Kbytes ITCM RAM size= 64 Kbytes SRAM1 size = 16 Kbytes SRAM2 size = 16 Kbytes

![](images/9746a6ae9e9b85013b2106bd115bbeba16b5250612f670c451e7330ea7eb70ce.jpg)  
Figure 11. LTDC AXI master in STM32H7Rx/7Sx

# 3.4

# Advantages of using an STM32 LTDC controller

Table 4 summarizes the major advantages of using the STM32 embedded LTDC interface.

Table 4. Advantages of using STM32 MCUs LTDC controller   

<table><tr><td rowspan=1 colspan=1>Advantage</td><td rowspan=1 colspan=1>Comments</td></tr><tr><td rowspan=1 colspan=1>Cost savings</td><td rowspan=1 colspan=1>Compared to other DBI interfaces (SPI, Motorola 6800 or Intel 8080), the LTDCallows a connection to any low-cost display module with no display controller norGRAM.</td></tr><tr><td rowspan=1 colspan=1>CPU offloaded</td><td rowspan=1 colspan=1>The LTDC is an AHB master with its own DMA, that fetches data autonomouslyfrom any AHB memory without any CPU intervention.</td></tr><tr><td rowspan=1 colspan=1>No need for extra applicative layer</td><td rowspan=1 colspan=1>The LTDC hardware fully manages the data fetching, the RGB outputting and thesignals control, so no need for extra applicative layer.</td></tr><tr><td rowspan=1 colspan=1>Fully programmable resolutionsupporting custom and standarddisplays</td><td rowspan=1 colspan=1>Fully programmable resolution with total width of up to 4096 pixels and total heightof up to 2048 lines and with pixel clock of up to 83 MHz.Support of custom and standard resolutions (QVGA, VGA, SVGA, WVGA, XGA,HD, and others).</td></tr><tr><td rowspan=1 colspan=1>Flexible color format</td><td rowspan=1 colspan=1>Each LTDC layer can be configured to fetch the framebuffer in the desired pixelformat (see Section 4.3.2: Programmable layer: color framebuffer).</td></tr><tr><td rowspan=1 colspan=1>Flexible parallel RGB interface</td><td rowspan=1 colspan=1>The flexible parallel RGB interace allows  driv-t bit nd -it disays.</td></tr><tr><td rowspan=1 colspan=1>Ideal for low-power and mobileapplications such as smart watches.</td><td rowspan=1 colspan=1>The LTDC is able to continue graphic data fetching and display driving while theCPU is in Sleep mode.</td></tr></table>

# 1 LCD-TFT (LTDC) display controller description

The LC is acnroller hat reads he data mage  a le per e ashion. Itmemoyacc m 2-yteorHB/AX) length,u when he en l ahe and less han6 byte orBXI are left, the LTDC fetches the remaining data.

# Functional description

O  liv oeG i   blen ieac with ye pi cult ida, unit and is driven into the RGB interface. The pixel is then displayed on the screen.

![](images/5cf9d8a0a7c955e3c04fb2f08727b98e4204b1425b361fc064b1ec8901b6fc93.jpg)  
Figure 12. LTDC block diagram

# 4.1.1

# LTDC clock domains

The LCD-TFT controller peripheral uses three clock domains:

AHcoc aCL)nstome  IFO ye nd he h around.   
APB clock domain (PCLK): used to access the configuration and status registers.   
Pixel clock domain (LCD_CLK): used to generate the LCD-TFT interface signals.   
The LCD_CLK output need to be configured following the panel requirements through the PLL.

# 4.1.2 LTDC reset

The LTDC is reset by setting the LTDCRST bit in the RCC_APB2RSTR register.

# 4.2

# Flexible timings and hardware interface

T with different resolutions and signal polarities.

# 4.2.1

# LCD-TFT pins and signal interface

Tdrive LCD-TFT displays, the LTDC provides up o 8 signals using imple 3.V snaling inclig:

Pixel clock LCD_CLK   
Data enable LCD_DE   
Synchronization signals (LCD_HSYNC and LCD_VSYNC)   
Pixel data RGB888

# Note:

The LTDC controller may support other display technologies if their interface is compatible.

The LTDC interface output signals are illustrated in Table 5

Table 5. LTDC interface output signals   

<table><tr><td rowspan=1 colspan=1>LCD-TFT signal</td><td rowspan=1 colspan=1>Description</td></tr><tr><td rowspan=1 colspan=1>LCD_CLK</td><td rowspan=1 colspan=1>The LCD_CLK acts as the data valid signal for the LCD-TFT. The data is considered by the display onlyon the LCD_CLK rising or falling edge.</td></tr><tr><td rowspan=1 colspan=1>LCD_HSYNC</td><td rowspan=1 colspan=1>The line synchronization signal (LCD_HSYNC) manages horizontal line scanning and acts as line displaystrobe.</td></tr><tr><td rowspan=1 colspan=1>LCD_VSYNC</td><td rowspan=1 colspan=1>The frame synchronization signal (LCD_vSYNC) manages vertical scanning and acts as a frame updatestrobe.</td></tr><tr><td rowspan=1 colspan=1>LCD_DE</td><td rowspan=1 colspan=1>The DE signal, indicates to the LCD-TFT that the data in the RGB bus is valid and must be latched to bedrawn.</td></tr><tr><td rowspan=1 colspan=1>Pixel RGB data</td><td rowspan=1 colspan=1>The LDC interface can be configured tooutut more than one color depth. It can use up o 4 data lines(RGB888) as display interface bus.</td></tr></table>

# Other signals

Iti co T luual able to drive only signals described in Table 5.

The signals that are not part of the LTDC, may be managed using GPIOs and other peripherals and may need specific circuits.

T

S ispla paes ee ese snal an also alteace such  CSP.Tent in general for the display initialization commands or for the touch panel control.

Figure shows a display panel connected to an STM32 MCU, using he LTDC interface signals illustratein Table 5.

![](images/7c0e152713b12fab4d9cebf87a1e3b7af086183be8addc41ce8feec7443e6d14.jpg)  
Figure 13. LTDC signal interface

The LTDC can output data according to the following parallel formats: RGB565, RGB666, and RGB888.   
So, 16-bit RGB565, 18-bit RGB666 or 24-bit RGB888 display can be connected.

# LTDC signals programmable polarity

The LTDC contro signals polariy programmable allowing he TM32 micocontroller driveany RGB paralle isay. The control sgnals (HSYNC, VSYNC, and data eable DE) as well as the piel clock (LCDCLK) can e defined to be active high or active low through the LTDC_GCR register.

# Fully programmable timings for different display sizes

Ta i  palr spha pgramable ming parameeregistrandheaxial sport piel cock describeabl Table 11 to Table 16.

The user must consider the timings registers described in Table 6 when programming as the LTDC timings and synchronization signals must be programmed to match the display specification.

Table 6 summarizes the timings registers supported by the LTDC.

Table 6. LTDC timing registers   

<table><tr><td rowspan=1 colspan=2>Register</td><td rowspan=1 colspan=1>Timing parameter</td><td rowspan=1 colspan=1>Value to beprogrammed</td></tr><tr><td rowspan=2 colspan=1>LTDC_SSCR(1)</td><td rowspan=1 colspan=1>HSW[11:0]</td><td rowspan=1 colspan=1>HSYNC width - 1</td><td rowspan=1 colspan=1>From 1 to 4096 pixels</td></tr><tr><td rowspan=1 colspan=1>VSH[11:0]</td><td rowspan=1 colspan=1>VSYNC height - 1</td><td rowspan=1 colspan=1>From 1 to 2048 lines</td></tr><tr><td rowspan=2 colspan=1>LTDC_BPCR</td><td rowspan=1 colspan=1>AHBP[11:0]</td><td rowspan=1 colspan=1>HSYNC width + HBP - 1</td><td rowspan=1 colspan=1>From 1 to 4096 pixels</td></tr><tr><td rowspan=1 colspan=1>AVBP[10:0]</td><td rowspan=1 colspan=1>VSYNC height + VBP - 1</td><td rowspan=1 colspan=1>From 1 to 2048 lines</td></tr><tr><td rowspan=2 colspan=1>LTDC_AWCR</td><td rowspan=1 colspan=1>AAW[11:0]</td><td rowspan=1 colspan=1>HSYNC width + HBP + active width - 1</td><td rowspan=1 colspan=1>From 1 to 4096 pixels</td></tr><tr><td rowspan=1 colspan=1>AAH[10:0]</td><td rowspan=1 colspan=1>VSYNC height + BVBP + active height - 1</td><td rowspan=1 colspan=1>From 1 to 2048 lines</td></tr><tr><td rowspan=2 colspan=1>LTDC_TWCR</td><td rowspan=1 colspan=1>TOTALW[11:0]</td><td rowspan=1 colspan=1>HSYNC width + HBP + active width + HFP - 1</td><td rowspan=1 colspan=1>From 1 to 4096 pixels</td></tr><tr><td rowspan=1 colspan=1>TOTALH[10:0]</td><td rowspan=1 colspan=1>VSYNC height + BVBP + active height + VFP - 1</td><td rowspan=1 colspan=1>From 1 to 2048 lines</td></tr></table>

1. Se C[: i uCDLSC[1:0] line period.

# Example of a typical LTDC display frame

Fgurhows example  typical Lspayrameshowing he tming parameerdescribe nTab

![](images/a5fd28aae1d74b17e8df2b9c6957b3c6cc961bf6fcad195251cfe2698bc554b2.jpg)  
Figure 14. Typical LTDC display frame (active width = 480 pixels)

# LTDC flexible timings

T LC pllloeu wi   a w u p total height of up to 2048 lines (refer to Table 6).   
Figure 15 illustrates fully programmable timings and resolutions.

![](images/caee9c31c05f32070d91ce9d5d0e78170a010861b6d1ecf723b4532285c925cd.jpg)  
Figure 15. Fully programmable timings and resolutions

# Caution:

Any display eolution belonging to themaxial totalarein 96 08 as dscibed i Figureis by the LTDC only if the following conditions are met:

The display panel pixel clock must not exceed the maximal LTDC pixel clock in Table 2.

The display panel pixel clock must not exceed the maximal STM32 pixel clock respecting the framebuffe bandwidth (see Section 5.: Checking the display size and color depth compatibility with the hardware configuration).

Figure 6 shows some custom and standard resolutions belonging to the maximal 4096 x 2048 supported by the LTDC.

# Figure 16. LTDC fully programmable display resolution with total width up to 4096 pixels and total height up to 2048 lines

Only the active display area is shown in this figure.

![](images/16a2a08fce0e1866c8baeb72e78fe42fe91881bd99244d0fdb27da512d9bc0f3.jpg)

# 4.3

# Two programmable LTDC layers

T L eaus wo layr each ayercanablebl  cgu ratelyTe window.

T  atucgurableblendg cBendng lays activusialphavale color, and then the Layer2 is blended with the result of the blended color of Layer1 and the background.

The background color is programmable through the LTDCBCCR register. A constant background color can be prorammed in the RGB888 ormat where the BCRED[7:0] feld is used for the red value, the BCGREEN[7:0] is used for the green value and the BCBLUE[7:0] is used for the blue value.

Figure 17 illustrates the blending of two layers with a background.

![](images/d92d848d89b4cebb643a6a0f12b8831bb776bdaea810212cef2f1f43f19cea14.jpg)  
Figure 17. Blending two layers with a background

# 4.3.1

# Flexible window position and size configuration

Every layer can be positioned and resized at runtime and it must be inside the active display area. The frame.

Furhows al  whey pornheag playwhilheaig r displayed.

LTDC_xWHPCRndLDCWVPCR  eivelyLTDC ayero an rtl registers where "x" can refer to Layer1 or Layer2.

![](images/41686563fa95d8a79b426575b3842df85082a3bcb62dbd3a90c4cbccd6f2b110.jpg)  
Figure 18. Layer window programmable size and position

# 4.3.2

# Programmable layer: color framebuffer

Evyyeasicatgurablbe n  g eolou pitch.

# Color framebuffer address

Every layer has a start address for the color framebuffer configured through the LTDC_LxCFBAR register.

# Color framebuffer length (size)

T the end of the framebuffer.

The line length (in bytes) is configurable in the LTDC_LxCFBLR register. The number of lines (in bytes) is configurable in the LTDC_LxCFBLNR register

# Color framebuffer pitch

in the LTDC_LxCFBLR register.

# Pixel input format

The programmable pixel format is used in allthe data stored in the framebuffer of each LTDC layer.

F  e i iua gu ate u wi eight programmable input color formats per layer.

Figure 19 illustrates the pixel data mapping versus the selected input color format.

![](images/362524120aec3521f3ae4e6d227d2191b24bcb6573a38160861904b0d9edbdc4.jpg)  
Figure 19. Pixel data mapping versus color format

Figure 20 summarizes all layer color framebuffer configurable parameters.

![](images/0cf7a37173407de5c4e24df8cebe6760033049501462f73127f09106c4c042da.jpg)  
Figure 20. Programmable color layer in framebuffer

# Pixel format conversion (PFC)

A internal ARGB8888 format.

T hathavwia an    y chosen.

igure 21 shows a conversion from RGB565 input pixel format to the internal ARGB8888 format.

![](images/ac22cf31f6a470be2a526c057a2e248379296e86b64afcfbc4893aba3ada85c9.jpg)  
Figure 21. Pixel format conversion from RGB565 input pixel format to the internal ARGB8888 format

Note:

Usin tayer ceatesandiconstraintonhestem. preerablesenlyeyen thecomposition with theChrom-Ar Accelerator duringheframebuffer calculatin e Section5..Cheki display compatibility considering the memory bandwidth requirements).

# 4.4

# Interrupts

The LTDC peripheral supports two global interrupts:

LTDC global interrupt LTDC global error interrupt

Eac gloal intrup icwo LTCterupt gicallysjonthat aneaskeey t interrupt is generated.

Table 7. LTDC interrupts summary   

<table><tr><td rowspan=1 colspan=1>Related NVICinterrupt</td><td rowspan=1 colspan=1>Interrupt event</td><td rowspan=1 colspan=1>Event flag bit(LTDCCISR)register</td><td rowspan=1 colspan=1>Enable bit(LTDC_IERregister</td><td rowspan=1 colspan=1>Clear bit(LTDC_ICRregister)</td><td rowspan=1 colspan=1>Description</td></tr><tr><td rowspan=2 colspan=1>LTDC GLOBALINTERRUPT</td><td rowspan=1 colspan=1>Line</td><td rowspan=1 colspan=1>LIF</td><td rowspan=1 colspan=1>LIE</td><td rowspan=1 colspan=1>CLIF</td><td rowspan=1 colspan=1>Generated when adefined line on thescreen is reached</td></tr><tr><td rowspan=1 colspan=1>Register reload</td><td rowspan=1 colspan=1>RRIF</td><td rowspan=1 colspan=1>RRIE</td><td rowspan=1 colspan=1>CRRIF</td><td rowspan=1 colspan=1>Generated whenthe shadow reloadoccurs</td></tr><tr><td rowspan=2 colspan=1>LTDC GLOBALERRORINTERRUPT</td><td rowspan=1 colspan=1>FIFO underrun(1)</td><td rowspan=1 colspan=1>FUIF</td><td rowspan=1 colspan=1>FUIE</td><td rowspan=1 colspan=1>CFUIF</td><td rowspan=1 colspan=1>Generated when apixel is requestedwhile the FIFO isempty</td></tr><tr><td rowspan=1 colspan=1>Transfer error</td><td rowspan=1 colspan=1>TERRIF</td><td rowspan=1 colspan=1>TERRIE</td><td rowspan=1 colspan=1>CTERRIF</td><td rowspan=1 colspan=1>Generated whenbus error occurs</td></tr></table>

compatibility considering the memory bandwidth requirements).

# 4.5 Low-power modes

The STM32 power state has a direct effect on the LTDC peripheral. While in Sleep mode, the LTDC is not a ndkeepsiviaphial dathecreeWhiStany nSodes, eLl anoutput drivenhrough t parallel interfacxitgStandy modemust  ollwe with the LTDC reconfiguration.

A display panel can be driven in Sleep mode while the CPU is stopped, thanks to the smart architecture ebeed in theTM32 MCUs that allows all peripherals to be enabledeven in Sleep mode.This feature it wearable applications where the low-power consumption is a must.

The LTDC, as an AHB master, can continue fetching data from FMC_SDRAM, Quad-SPI or Octo-SPI (when the Memory-mapped mode is used), even after entering the MCU in Sleep mode. A line event or register eload interrupt can be generated to wake up the ST32 when a defined lne on the screen is reached or when the shadow reload occurs.

More information on reducing power consumption is available on Section 6.   
Table 8 summarizes the LTDC state versus the STM32 low-power modes.

Table 8. LTDC peripheral state versus STM32 low-power modes   

<table><tr><td rowspan=1 colspan=1>Mode</td><td rowspan=1 colspan=1>Description</td></tr><tr><td rowspan=1 colspan=1>Run</td><td rowspan=1 colspan=1>Active</td></tr><tr><td rowspan=1 colspan=1>Sleep</td><td rowspan=1 colspan=1>ActivePerheral interrupts cause the devic  exi Slee mode.</td></tr><tr><td rowspan=1 colspan=1>Stop</td><td rowspan=1 colspan=1>FrozenPeripheral registers content is kept.</td></tr><tr><td rowspan=1 colspan=1>Standby</td><td rowspan=1 colspan=1>Powered-downThe peripheral must be reinitialized after exiting Standby mode.</td></tr></table>

# 5 Creating a graphical application with LTDC

Thi ecustratesheifn e qu endurahialplatindeveo LC.Tesmus etehil plat qu  hece heharwa conguratnDurnggraphial plicatn cpatibilityhec phas ee STeferene boar esibeable can euse evaluateisharware  soa coguion.

# Determining graphical application requirements

Determining the graphical application needs is a crucial step to start from. Some of the most important pearnhtot depth, as well as the nature of the data to display (static images, text, or animation).

Once the basic parameters mentioned above are defined, the user must determine the graphical hardware arhitecture f he application, s wel as the requi hardware resourcs.The best-fitng 2 packge (see Table 20) must be selected, according to the following parameters:

If an external memory is needed for the framebuffer.   
The external framebuffer memory bus width   
The LTDC interface: RGB565, RGB666, or RGB888 depending on the display module If an external memory is needed to store graphic primitives (QSPI or FMC_NOR).

# Checking the display size and color depth compatibility with the hardware configuration

Whe starting a graphicapplication development using an ST32 microcontrolle, the user has often a defined desired display size and color depth. A key question that the user must answer before continuing the development is if such display size and color depth match a specific hardware configuration.

The following steps are needed in order to answer this question:   
Determine the required framebuffer size and its location.   
Check the compatibility of the display versus the framebuffer memory bandwidth requirements. Check the compatibility of the display panel interface with the LTDC.

# Framebuffer memory size requirements and location

Deutibl Themeory sa quiineAM  pport hemebufr ust  cntuous and wi e equal to:

Framebuffer size = number of pixels x bits per pixel

Aboquupl depth.

a an RGB888 display can be driven using an RGB565 framebuffer.

# Note:

Tequeufbleoubleufngratin. Ion le uhh to prepare the next image.

Table 9 shows the framebuffer size needed for standard screen resolutions with different pixel formats.

Table 9. Framebuffer size for different screen resolutions   

<table><tr><td colspan="1" rowspan="2">Screen resolution</td><td colspan="1" rowspan="2">Number of pixels</td><td colspan="4" rowspan="1">Framebuffer size (Kbyte)(1)</td></tr><tr><td colspan="1" rowspan="1">8 bpp</td><td colspan="1" rowspan="1">16 bpp</td><td colspan="1" rowspan="1">24 bpp</td><td colspan="1" rowspan="1">32 bpp</td></tr><tr><td colspan="1" rowspan="1">QVGA (320 x 240)</td><td colspan="1" rowspan="1">76800</td><td colspan="1" rowspan="1">75</td><td colspan="1" rowspan="1">150</td><td colspan="1" rowspan="1">225</td><td colspan="1" rowspan="1">300</td></tr><tr><td colspan="1" rowspan="1">Custom (480 x 272)(2)</td><td colspan="1" rowspan="1">130560</td><td colspan="1" rowspan="1">128</td><td colspan="1" rowspan="1">255</td><td colspan="1" rowspan="1">383</td><td colspan="1" rowspan="1">510</td></tr><tr><td colspan="1" rowspan="1">HVGA(480 x 320)</td><td colspan="1" rowspan="1">153600</td><td colspan="1" rowspan="1">150</td><td colspan="1" rowspan="1">300</td><td colspan="1" rowspan="1">450</td><td colspan="1" rowspan="1">600</td></tr><tr><td colspan="1" rowspan="1">VGA (640 x 480)</td><td colspan="1" rowspan="1">307200</td><td colspan="1" rowspan="1">300</td><td colspan="1" rowspan="1">600</td><td colspan="1" rowspan="1">900</td><td colspan="1" rowspan="1">1200</td></tr><tr><td colspan="1" rowspan="1">WVGA(800 x 480)</td><td colspan="1" rowspan="1">384000</td><td colspan="1" rowspan="1">375</td><td colspan="1" rowspan="1">750</td><td colspan="1" rowspan="1">1125</td><td colspan="1" rowspan="1">1500</td></tr><tr><td colspan="1" rowspan="1">SVGA (800 x 600)</td><td colspan="1" rowspan="1">480000</td><td colspan="1" rowspan="1">469</td><td colspan="1" rowspan="1">938</td><td colspan="1" rowspan="1">1407</td><td colspan="1" rowspan="1">1875</td></tr><tr><td colspan="1" rowspan="1">XGA (1024 x 768)</td><td colspan="1" rowspan="1">786432</td><td colspan="1" rowspan="1">768</td><td colspan="1" rowspan="1">1536</td><td colspan="1" rowspan="1">2304</td><td colspan="1" rowspan="1">3072</td></tr><tr><td colspan="1" rowspan="1">HD (1280 x 720)</td><td colspan="1" rowspan="1">921600</td><td colspan="1" rowspan="1">900</td><td colspan="1" rowspan="1">1800</td><td colspan="1" rowspan="1">2700</td><td colspan="1" rowspan="1">3600</td></tr></table>

1The required framebuffer size is doubled for double-framebuffer configuration. 2. An example of a custom 480 x 272 display is the ROCKTECH embedded on the STM32F746 discovery kit (32F746GDISCOVERY).

# Framebuffer location

uuaA external SRAM/SDRAM.

If the internal RAM is not enough for the framebuffer, the user must use an external SDRAM/SRAM connece to the FMC.

Coquently heequimebuf deteie eun exteralmemory ieeet.   
required framebuffer size depends on the display size and color depth.

# Locating the framebuffer in the Internal SRAM

Dei eufheufn plahtealAMhe SRAM or SDRAM.

Using an internal SRAM as a framebufalows hemaxmum peformances and avoids any bandwith imtatin issues for the LTDC.

Jsing the internal SRAM instead of an external SRAM or SDRAM has many advantages:

higher throughput (0 wait state access) reduced number of required pins and PCB design complexity reduced BOM, hence cost, since no external memory is needed

The nly itaon whenusinghe tenal AM  mi i udre  y Whenheuf size exceeds the available memory, the external SDRAM or SRAM (driven by the FMC interface) must be used. Howe hen dealng wit exteal meor, heer ust e careul tavod bandwih itatn. detailed information, refer to Section 5.5: Graphic performance optimization.

# Note:

Tlr ok abl an esece quufFo oetai the STM32 MCU reference manual).

# 5.2.2

# Checking display compatibility considering the memory bandwidth requirements

This section eplainshow heck adispaycpatibility considerinhe fmebufmemory andwidh.Se ntieeeplaoweieeun tpiel clockanhe.all spleethoonce whetheds ispa zle with a specific hardware configuration; is detailed.

# Framebuffer memory bandwidth aspects

can sustain the hardware configuration.

T eck hememory bandwith can sustan he LTDC requi bandwih,he user must consr yhe concurrent accesses to the memory.

In general, a small izeramebuffer located in the internal RAM does ot requie a high bandwidh.Thisis because a small size framebuffer means low pixel clock, hence low LTDC required bandwidth.

A more complex use case to analyze is when the framebuffer is located in an external memory (SDRAM or SRAM).

# Framebuffer memory bus concurrency

• LTDC, DMA2D, and CPU masters. In a typical graphic application where an external SDRAM or SRAM memory is used as framebuffer, two or three main AHB masters concurrently use the same memory. The DMA2D (or the CPU) updates the next image to be displayed while the LTDC fetches and displays the actual image. The memory bus load depends mainly on the LTDC required bandwidth.

• Other AHB masters.

It is common that an external SDRAM or SRAM memory is shared by other masters and not only by those used for graphics. This concurrency leads to heavy bus load and may impact the graphic performances.

Figure 22 shows all the AHB masters with concurrent access to the SDRAM.

![](images/bdb703b932e4bb58bd838f47deaf4dc66fe0a97c0829c435222bb6fab6272e8f.jpg)  
Figure 22. AHB masters concurrent access to SDRAM

# External SDRAM/SRAM memory bus width

When locating the framebuffer in an external SDRAM/SRAM, the user must consider that the external memory sa y must be considered as the bottleneck of the whole graphic system.

Onfhe needed parameters or checking thedisplaycompatibli is the memory bus width. For SDRAM, an 8 bit, 16-bit, or 32-bit configuration can be used.

aepalehe memory:

Temaseoncue s hesmexteal meoy lmo ateiparut

# Determining pixel clock and LTDC required bandwidth

# Pixel clock computation

T  e. To get h typical pixe clock  thedisplay reer the isplaydatashet.Thecompued piel clock ne t respect the display specifications.

The pixel clock for a specific refresh rate is calculated with the following formula: LCD_CLK (MHz) = total screen size x refresh rate   
Where total screen size = total width x total height.

# LTDC required bandwidth

The LTDC required bandwidth depends mainly on three factors:

Number of used LTDC layers.   
LTDC layer color depth.   
Pixel clock (depends on the resolution of the display panel and on the refresh rate).

The maximum required bandwidth can be calculated as described below:

• If only one LTDC layer is used: LTDC required bandwidth = LCD_CLK x BppL1   
. If two LTDC layers are used: LTDC required bandwidth = LCD_CLK x (BppL1 + BppL2)

Where BppL1 and BppL2 are respectively the color depth for LTDC Layer1 and Layer2. The LTDC required bandwidth must not exceed thememory available bandwidth, herwis display problems mayoccurand the b thefrmebue slouseorhepliatin purposs i may pact egraphical peorans system.

# Check if the used display resolution fits the hardware configuration

Thegneral method orheckn wheherdspay iewit  particular color deptopatible wit meoy bandwidth includes the following steps:

Compute the pixel clock according to the display size or extract it from the display datasheet.

Check if the display pixel clock does not exceed the maximum system-supported pixel clock described in Table 10 to Table 16. The following parameters must be used to extract from Table 10 or Table 16 the maximum-supported pixel clock corresponding to the used hardware configuration:

Number of used LTDC layers.   
Used system clock speed HCLK and framebuffer memory speed.   
External framebuffer memory bus width.   
Number of AHB masters accessing concurrently to external framebuffer memory.

The user must perform some tests to confirm the hardware compatibility with the desired display size and color depth. To do it, the user must monitor the LTDC FIFOunderrun interrupt fag in the LTDCISR reier I  Odernterupt lwa re,heneuconis hat eesi ispy z compatible with the hardware configuration.

If the FIFO underrun flag is set, the user must check the following points:

e p lc TT hardware (mistake example: 16-bit SDRAM but extracted pixel clock corresponding to a 32-bit SDRAM).

The color framebuffer lie width is not 64/128 bytes (for AHB/AXl) aligned (see Section 5.5.: Optimizing the LTDC framebuffer fetching from external memories (SDRAM or SRAM)).

cFor the STM32F7 and STM32H7 devices, the MPU is not correctly configured to avoid Cortex®-M7 speculative read accesses to the external memory (see Section 5.6: Special recommendations for Cortex-M7 (STM32F7/H7)).

I he IFO underrun is silet becaue thereae more than two AHB mastes concuent access  he external memory, the user must relax the memory bandwidth using the below recommendations:

o Use only one LTDC layer. Use the largest possible memory bus width (32-bit instead of 16- or 8-bit SDRAM/SRAM). Update the framebuffer content during the blanking period when the LTDC is not fetching.   
o Use the highest possible system clock HCLK and the highest memory speed.   
o Decrease the images color depth (bpp). For more details on memory bandwidth optimization, see Section 5.5: Graphic performance optimization.

# Note:

T evaluate the STM32graphical capability in a specifi hardware configuration, the user can use the STM32 boards described in Table 24. STM32 reference boards embedding LTDC and featuring an on-board LCD-TFT panel.

Figure 3 shows a typical graphic hardware configuration where an external SDRAM is connected to the FMC that is used or ramebufr.The SDRAM memory bandwidth depends n he bus width and in the opeati clock.

The SDRAM bus width can be 3-bit, -bit, o 8-bit, while the operating clock depends on the system clock HCLK and the configured prescaler (HCLK/2 or HCLK/3).

![](images/ec7152adbe7bf65e5e1ddd85352a41774fe41753df74a4446119990c91672a17.jpg)  
Figure 23. Typical graphic hardware configuration with external SDRAM

TTTTTTb clock at system level for various STM32 MCUs.

Table 10. STM32F4x9 maximal supported pixel clock   

<table><tr><td rowspan=4 colspan=1>Used LTDC layers</td><td rowspan=4 colspan=1>Color depth (bpp)</td><td rowspan=1 colspan=4>Maximum pixel clock (MHz)(1)</td></tr><tr><td rowspan=1 colspan=2>LTDC(2)</td><td rowspan=1 colspan=2>LTDC + DMA2D(3)</td></tr><tr><td rowspan=1 colspan=4>FMC</td></tr><tr><td rowspan=1 colspan=1>SDRAM 16-bit</td><td rowspan=1 colspan=1>SDRAM 32-bit</td><td rowspan=1 colspan=1>SDRAM 16-bit</td><td rowspan=1 colspan=1>SDRAM 32-bit</td></tr><tr><td rowspan=4 colspan=1>1 layer</td><td rowspan=1 colspan=1>32</td><td rowspan=1 colspan=1>38</td><td rowspan=1 colspan=1>67</td><td rowspan=1 colspan=1>22</td><td rowspan=1 colspan=1>35</td></tr><tr><td rowspan=1 colspan=1>24</td><td rowspan=1 colspan=1>51</td><td rowspan=1 colspan=1>83</td><td rowspan=1 colspan=1>30</td><td rowspan=1 colspan=1>47</td></tr><tr><td rowspan=1 colspan=1>16</td><td rowspan=1 colspan=1>76</td><td rowspan=1 colspan=1>83</td><td rowspan=1 colspan=1>45</td><td rowspan=1 colspan=1>70</td></tr><tr><td rowspan=1 colspan=1>8</td><td rowspan=1 colspan=1>83</td><td rowspan=1 colspan=1>83</td><td rowspan=1 colspan=1>83</td><td rowspan=1 colspan=1>83</td></tr><tr><td rowspan=10 colspan=1>2 layers</td><td rowspan=1 colspan=1>32/32</td><td rowspan=1 colspan=1>19</td><td rowspan=1 colspan=1>33</td><td rowspan=1 colspan=1>NA</td><td rowspan=1 colspan=1>18</td></tr><tr><td rowspan=1 colspan=1>32/24</td><td rowspan=1 colspan=1>22</td><td rowspan=1 colspan=1>38</td><td rowspan=1 colspan=1>13</td><td rowspan=1 colspan=1>21</td></tr><tr><td rowspan=1 colspan=1>32/16</td><td rowspan=1 colspan=1>25</td><td rowspan=1 colspan=1>44</td><td rowspan=1 colspan=1>15</td><td rowspan=1 colspan=1>25</td></tr><tr><td rowspan=1 colspan=1>32/8</td><td rowspan=1 colspan=1>30</td><td rowspan=1 colspan=1>53</td><td rowspan=1 colspan=1>19</td><td rowspan=1 colspan=1>30</td></tr><tr><td rowspan=1 colspan=1>24/24</td><td rowspan=1 colspan=1>26</td><td rowspan=1 colspan=1>44</td><td rowspan=1 colspan=1>15</td><td rowspan=1 colspan=1>24</td></tr><tr><td rowspan=1 colspan=1>24/16</td><td rowspan=1 colspan=1>31</td><td rowspan=1 colspan=1>53</td><td rowspan=1 colspan=1>18</td><td rowspan=1 colspan=1>30</td></tr><tr><td rowspan=1 colspan=1>24/8</td><td rowspan=1 colspan=1>38</td><td rowspan=1 colspan=1>67</td><td rowspan=1 colspan=1>23</td><td rowspan=1 colspan=1>38</td></tr><tr><td rowspan=1 colspan=1>16/16</td><td rowspan=1 colspan=1>39</td><td rowspan=1 colspan=1>67</td><td rowspan=1 colspan=1>22</td><td rowspan=1 colspan=1>37</td></tr><tr><td rowspan=1 colspan=1>16/8</td><td rowspan=1 colspan=1>51</td><td rowspan=1 colspan=1>83</td><td rowspan=1 colspan=1>31</td><td rowspan=1 colspan=1>50</td></tr><tr><td rowspan=1 colspan=1>8/8</td><td rowspan=1 colspan=1>78</td><td rowspan=1 colspan=1>83</td><td rowspan=1 colspan=1>46</td><td rowspan=1 colspan=1>74</td></tr></table>

System clock HCLK = 180 MHz, SDRAM runs at 90 MHz. 2. color depth is 8, 16, 24, or 32 bpp.

Table 11. STM32F7x6/7/8/9 maximal supported pixel clock   

<table><tr><td rowspan=4 colspan=1>Used LTDC layers</td><td rowspan=4 colspan=1>Color depth (bpp)</td><td rowspan=1 colspan=4>Maximum pixel clock (MHz)(1)</td></tr><tr><td rowspan=1 colspan=2>LTDC(2)</td><td rowspan=1 colspan=2>LTDC + DMA2D(3)</td></tr><tr><td rowspan=1 colspan=4>fmc</td></tr><tr><td rowspan=1 colspan=1>SDRAM 16-bit</td><td rowspan=1 colspan=1>SDRAM 32-bit</td><td rowspan=1 colspan=1>SDRAM 16-bit</td><td rowspan=1 colspan=1>SDRAM 32-bit</td></tr><tr><td rowspan=4 colspan=1>1 layer</td><td rowspan=1 colspan=1>32</td><td rowspan=1 colspan=1>42</td><td rowspan=1 colspan=1>74</td><td rowspan=1 colspan=1>25</td><td rowspan=1 colspan=1>39</td></tr><tr><td rowspan=1 colspan=1>24</td><td rowspan=1 colspan=1>56</td><td rowspan=1 colspan=1>83</td><td rowspan=1 colspan=1>34</td><td rowspan=1 colspan=1>52</td></tr><tr><td rowspan=1 colspan=1>16</td><td rowspan=1 colspan=1>83</td><td rowspan=1 colspan=1>83</td><td rowspan=1 colspan=1>51</td><td rowspan=1 colspan=1>78</td></tr><tr><td rowspan=1 colspan=1>8</td><td rowspan=1 colspan=1>83</td><td rowspan=1 colspan=1>83</td><td rowspan=1 colspan=1>83</td><td rowspan=1 colspan=1>83</td></tr><tr><td rowspan=10 colspan=1>2 layers</td><td rowspan=1 colspan=1>32/32</td><td rowspan=1 colspan=1>21</td><td rowspan=1 colspan=1>37</td><td rowspan=1 colspan=1>12</td><td rowspan=1 colspan=1>20</td></tr><tr><td rowspan=1 colspan=1>32/24</td><td rowspan=1 colspan=1>24</td><td rowspan=1 colspan=1>42</td><td rowspan=1 colspan=1>14</td><td rowspan=1 colspan=1>23</td></tr><tr><td rowspan=1 colspan=1>32/16</td><td rowspan=1 colspan=1>28</td><td rowspan=1 colspan=1>49</td><td rowspan=1 colspan=1>17</td><td rowspan=1 colspan=1>28</td></tr><tr><td rowspan=1 colspan=1>32/8</td><td rowspan=1 colspan=1>34</td><td rowspan=1 colspan=1>59</td><td rowspan=1 colspan=1>21</td><td rowspan=1 colspan=1>34</td></tr><tr><td rowspan=1 colspan=1>24/24</td><td rowspan=1 colspan=1>29</td><td rowspan=1 colspan=1>49</td><td rowspan=1 colspan=1>17</td><td rowspan=1 colspan=1>27</td></tr><tr><td rowspan=1 colspan=1>24/16</td><td rowspan=1 colspan=1>34</td><td rowspan=1 colspan=1>59</td><td rowspan=1 colspan=1>20</td><td rowspan=1 colspan=1>33</td></tr><tr><td rowspan=1 colspan=1>24/8</td><td rowspan=1 colspan=1>42</td><td rowspan=1 colspan=1>74</td><td rowspan=1 colspan=1>26</td><td rowspan=1 colspan=1>42</td></tr><tr><td rowspan=1 colspan=1>16/16</td><td rowspan=1 colspan=1>43</td><td rowspan=1 colspan=1>74</td><td rowspan=1 colspan=1>25</td><td rowspan=1 colspan=1>41</td></tr><tr><td rowspan=1 colspan=1>16/8</td><td rowspan=1 colspan=1>57</td><td rowspan=1 colspan=1>83</td><td rowspan=1 colspan=1>34</td><td rowspan=1 colspan=1>56</td></tr><tr><td rowspan=1 colspan=1>8/8</td><td rowspan=1 colspan=1>83</td><td rowspan=1 colspan=1>83</td><td rowspan=1 colspan=1>51</td><td rowspan=1 colspan=1>82</td></tr></table>

System clock HCLK = 200 MHz, SDRAM runs at 100 MHz. color depth is 8, 16, 24, or 32 bpp.

Table 12. STM32H742/43/45/47/53/55/57 and STM32H750 maximal supported pixel clock   

<table><tr><td rowspan=4 colspan=1>Used LTDC layers</td><td rowspan=4 colspan=1>Color depth (bpp)</td><td rowspan=1 colspan=4>Maximum pixel clock(1)</td></tr><tr><td rowspan=1 colspan=2>LTDC(2)</td><td rowspan=1 colspan=2>LTDC + DMA2D(3)</td></tr><tr><td rowspan=1 colspan=4>FMC</td></tr><tr><td rowspan=1 colspan=1>SDRAM 16-bit</td><td rowspan=1 colspan=1>SDRAM 32-bit</td><td rowspan=1 colspan=1>SDRAM 16-bit</td><td rowspan=1 colspan=1>SDRAM 32-bit</td></tr><tr><td rowspan=4 colspan=1>1 layer</td><td rowspan=1 colspan=1>32</td><td rowspan=1 colspan=1>49</td><td rowspan=1 colspan=1>93</td><td rowspan=1 colspan=1>29</td><td rowspan=1 colspan=1>48</td></tr><tr><td rowspan=1 colspan=1>24</td><td rowspan=1 colspan=1>66</td><td rowspan=1 colspan=1>124</td><td rowspan=1 colspan=1>38</td><td rowspan=1 colspan=1>64</td></tr><tr><td rowspan=1 colspan=1>16</td><td rowspan=1 colspan=1>99</td><td rowspan=1 colspan=1>150</td><td rowspan=1 colspan=1>58</td><td rowspan=1 colspan=1>96</td></tr><tr><td rowspan=1 colspan=1>8</td><td rowspan=1 colspan=1>150</td><td rowspan=1 colspan=1>150</td><td rowspan=1 colspan=1>116</td><td rowspan=1 colspan=1>150</td></tr></table>

1. System clock HCLK = 240 MHz, SDRAM runs at 110 MHz. LTDC fetches the front buffer from the external memory. The LTDC layer color depth is 8 16, , or 32 bpp.

Table 13. STM32H7R7/7S7 maximal supported pixel clock   

<table><tr><td rowspan=4 colspan=1>UsedLTDClayers</td><td rowspan=4 colspan=1>Colordepthbpp)</td><td rowspan=1 colspan=8>Maximum pixel clock(1)</td></tr><tr><td rowspan=1 colspan=4>LTDC(2)</td><td rowspan=1 colspan=4>LTDC + DMA2D(3)</td></tr><tr><td rowspan=1 colspan=2>XSPI</td><td rowspan=1 colspan=2>FMC</td><td rowspan=1 colspan=2>XSPI</td><td rowspan=1 colspan=2>FMC</td></tr><tr><td rowspan=1 colspan=1>8-bitPSRAMDDR</td><td rowspan=1 colspan=1>16-bitPSRAMDR</td><td rowspan=1 colspan=1>SDRAM16-bit</td><td rowspan=1 colspan=1>SDRAM32-bit</td><td rowspan=1 colspan=1>8-bitPSRAMDDR</td><td rowspan=1 colspan=1>16-bitPSRAMDDR</td><td rowspan=1 colspan=1>SDRAM16-bit</td><td rowspan=1 colspan=1>SDRAM32-bit</td></tr><tr><td rowspan=4 colspan=1>1 layer</td><td rowspan=1 colspan=1>32</td><td rowspan=1 colspan=1>89</td><td rowspan=1 colspan=1>90</td><td rowspan=1 colspan=1>48</td><td rowspan=1 colspan=1>90</td><td rowspan=1 colspan=1>35</td><td rowspan=1 colspan=1>61</td><td rowspan=1 colspan=1>28</td><td rowspan=1 colspan=1>48</td></tr><tr><td rowspan=1 colspan=1>24</td><td rowspan=1 colspan=1>90</td><td rowspan=1 colspan=1>90</td><td rowspan=1 colspan=1>64</td><td rowspan=1 colspan=1>90</td><td rowspan=1 colspan=1>46</td><td rowspan=1 colspan=1>83</td><td rowspan=1 colspan=1>36</td><td rowspan=1 colspan=1>60</td></tr><tr><td rowspan=1 colspan=1>16</td><td rowspan=1 colspan=1>90</td><td rowspan=1 colspan=1>90</td><td rowspan=1 colspan=1>90</td><td rowspan=1 colspan=1>90</td><td rowspan=1 colspan=1>69</td><td rowspan=1 colspan=1>90</td><td rowspan=1 colspan=1>56</td><td rowspan=1 colspan=1>90</td></tr><tr><td rowspan=1 colspan=1>8</td><td rowspan=1 colspan=1>90</td><td rowspan=1 colspan=1>90</td><td rowspan=1 colspan=1>90</td><td rowspan=1 colspan=1>90</td><td rowspan=1 colspan=1>90</td><td rowspan=1 colspan=1>90</td><td rowspan=1 colspan=1>90</td><td rowspan=1 colspan=1>90</td></tr></table>

1 System clock HCLK = 300 MHz, PSRAM runs at 200MHz, SDRAM runs at 100 MHz LTDC fetches the front buffer from the external memory. The LTDC layer color depth is 8 16, ,or 32 bpp.

Table 14. STM32H7A3/B3 and STM32H7B0 maximal supported pixel clock   

<table><tr><td rowspan=4 colspan=1>Used LTDClayers</td><td rowspan=4 colspan=1>Color depth(bpp)</td><td rowspan=1 colspan=6>Maximum pixel clock(1)</td></tr><tr><td rowspan=1 colspan=3>LTDC(2)</td><td rowspan=1 colspan=3>LTDC + DMA2D(3)</td></tr><tr><td rowspan=1 colspan=1>OCTOSPI</td><td rowspan=1 colspan=2>FMC</td><td rowspan=1 colspan=1>OCTOSPI</td><td rowspan=1 colspan=2>FMC</td></tr><tr><td rowspan=1 colspan=1>HyperRAM™8-bit DDR</td><td rowspan=1 colspan=1>SDRAM16-bit</td><td rowspan=1 colspan=1>SDRAM32-bit</td><td rowspan=1 colspan=1>HyperRAM™8-bbit DR</td><td rowspan=1 colspan=1>SDRAM16-bit</td><td rowspan=1 colspan=1>SDRAM32-bit</td></tr><tr><td rowspan=4 colspan=1>1 layer</td><td rowspan=1 colspan=1>32</td><td rowspan=1 colspan=1>52</td><td rowspan=1 colspan=1>52</td><td rowspan=1 colspan=1>97</td><td rowspan=1 colspan=1>22</td><td rowspan=1 colspan=1>30</td><td rowspan=1 colspan=1>50</td></tr><tr><td rowspan=1 colspan=1>24</td><td rowspan=1 colspan=1>70</td><td rowspan=1 colspan=1>70</td><td rowspan=1 colspan=1>130</td><td rowspan=1 colspan=1>29</td><td rowspan=1 colspan=1>40</td><td rowspan=1 colspan=1>66</td></tr><tr><td rowspan=1 colspan=1>16</td><td rowspan=1 colspan=1>105</td><td rowspan=1 colspan=1>105</td><td rowspan=1 colspan=1>140</td><td rowspan=1 colspan=1>44</td><td rowspan=1 colspan=1>60</td><td rowspan=1 colspan=1>100</td></tr><tr><td rowspan=1 colspan=1>8</td><td rowspan=1 colspan=1>140</td><td rowspan=1 colspan=1>140</td><td rowspan=1 colspan=1>140</td><td rowspan=1 colspan=1>89</td><td rowspan=1 colspan=1>121</td><td rowspan=1 colspan=1>140</td></tr></table>

1. System clock HCLK = 280 MHz, SDRAM/HyperRAM run at 110 MHz. LTDC fetches the front buffer from the external memory. The LTDC layer color depth is 8, 16, , or 32 bpp.

Table 15. STM32L4+ maximal supported pixel clock   

<table><tr><td rowspan=4 colspan=1>Used LTDC layers</td><td rowspan=4 colspan=1>Color depth (bpp)</td><td rowspan=1 colspan=2>Maximum pixel clock(1)</td></tr><tr><td rowspan=1 colspan=1>LTDCX(2)</td><td rowspan=1 colspan=1>LTDC + DMA2D(3)</td></tr><tr><td rowspan=1 colspan=2>FSMC</td></tr><tr><td rowspan=1 colspan=2>SRAM 16-bit</td></tr><tr><td rowspan=4 colspan=1>1 layer</td><td rowspan=1 colspan=1>32</td><td rowspan=1 colspan=1>11</td><td rowspan=1 colspan=1>-</td></tr><tr><td rowspan=1 colspan=1>24</td><td rowspan=1 colspan=1>15</td><td rowspan=1 colspan=1>10</td></tr><tr><td rowspan=1 colspan=1>16</td><td rowspan=1 colspan=1>23</td><td rowspan=1 colspan=1>15</td></tr><tr><td rowspan=1 colspan=1>8</td><td rowspan=1 colspan=1>47</td><td rowspan=1 colspan=1>31</td></tr></table>

1 System clock HCLK = 120 MHz, SRAM is asynchronous. LTDC fetches the front buffer from the external memory. The LTDC layer color depth is 8, 16, 4,or 32 bpp.

Table 16. STM32L4P/Q maximal supported pixel clock   

<table><tr><td rowspan=4 colspan=1>Used LTDC layers</td><td rowspan=4 colspan=1>Color depth (bpp)</td><td rowspan=1 colspan=2>Maximum pixel clock(1)</td></tr><tr><td rowspan=1 colspan=1>LTDC(2)</td><td rowspan=1 colspan=1>LTDC + DMA2D(3)</td></tr><tr><td rowspan=1 colspan=2>OCTOSPI</td></tr><tr><td rowspan=1 colspan=2>8-bit PSRAM DDR</td></tr><tr><td rowspan=4 colspan=1>1 layer</td><td rowspan=1 colspan=1>32</td><td rowspan=1 colspan=1>27</td><td rowspan=1 colspan=1>11</td></tr><tr><td rowspan=1 colspan=1>24</td><td rowspan=1 colspan=1>37</td><td rowspan=1 colspan=1>15</td></tr><tr><td rowspan=1 colspan=1>16</td><td rowspan=1 colspan=1>55</td><td rowspan=1 colspan=1>23</td></tr><tr><td rowspan=1 colspan=1>8</td><td rowspan=1 colspan=1>60</td><td rowspan=1 colspan=1>46</td></tr></table>

1. System clock HCLK = 120 MHz, PSRAM runs at 60 MHz. LTDC fetches the front buffer from the external memory. The LTDC layer color depth is 8 16, ,or 32 bpp.

Note:

Decreasing the system clock (HCLK then LTDC) leads to a degradation of graphic performances

Table 17. STM32U59/A/F/G maximal supported pixel clock   

<table><tr><td rowspan=4 colspan=1>Used LTDC layers</td><td rowspan=4 colspan=1>Color depth (bpp)</td><td rowspan=1 colspan=2>Maximum pixel clock(1)(2)</td></tr><tr><td rowspan=1 colspan=1>LTDC(3)</td><td rowspan=1 colspan=1>LTDC + DMA2D(4)</td></tr><tr><td rowspan=1 colspan=2>OCTOSPI</td></tr><tr><td rowspan=1 colspan=2>16-bit PSRAM DDR</td></tr><tr><td rowspan=4 colspan=1>1 layer</td><td rowspan=1 colspan=1>32</td><td rowspan=1 colspan=1>116</td><td rowspan=1 colspan=1>42</td></tr><tr><td rowspan=1 colspan=1>24</td><td rowspan=1 colspan=1>116</td><td rowspan=1 colspan=1>48</td></tr><tr><td rowspan=1 colspan=1>16</td><td rowspan=1 colspan=1>116</td><td rowspan=1 colspan=1>71</td></tr><tr><td rowspan=1 colspan=1>8</td><td rowspan=1 colspan=1>116</td><td rowspan=1 colspan=1>116</td></tr></table>

System clock HCLK = 160 MHz, PSRAM memory runs at 160 MHz. Limited by LTDC maximum output clock frequency, refer to the relevant product datasheet. LTDC fetches the front buffer from the external memory. The LTDC layer color depth is 8, 16, 4,or 32 bpp. h

Table 18. STM32N6x5/6x7 maximal supported pixel clock   

<table><tr><td rowspan=4 colspan=1>Used LTDC layers</td><td rowspan=4 colspan=1>Color depth (bpp)</td><td rowspan=1 colspan=2>Maximum pixel clock(1)</td></tr><tr><td rowspan=1 colspan=2>LTDC(2)</td></tr><tr><td rowspan=1 colspan=2>XSPI</td></tr><tr><td rowspan=1 colspan=1>8-bit PSRAM DDR</td><td rowspan=1 colspan=1>16-bit PSRAM DDR</td></tr><tr><td rowspan=4 colspan=1>1 layer</td><td rowspan=1 colspan=1>32</td><td rowspan=1 colspan=1>88</td><td rowspan=1 colspan=1>88</td></tr><tr><td rowspan=1 colspan=1>24</td><td rowspan=1 colspan=1>88</td><td rowspan=1 colspan=1>88</td></tr><tr><td rowspan=1 colspan=1>16</td><td rowspan=1 colspan=1>88</td><td rowspan=1 colspan=1>88</td></tr><tr><td rowspan=1 colspan=1>8</td><td rowspan=1 colspan=1>88</td><td rowspan=1 colspan=1>88</td></tr></table>

System clock HCLK = 400 MHz, PSRAM runs at 200 MHz LTDC fetches the front buffer from the external memory. The LTDC layer color depth is 8 16, , or 32 bpp.

# Note:

For STM32N6x5/6x7 devices, the AXI QOS is set to maximum for LTDC. As a consequence, the maximal suported pixel clock is the same for both LTDC and LTDC+DMA2D tests. The values are limited by the LTDC Kernel clock at 88 MHz.

# Example of supported display resolutions for STM32F4x9 and STM32F7x6/7/8/9

Table 19 lists an example of some standard and custom display sizes supported by the STM32F4x9 and STM32F7x6/7/8/9, in the following conditions:

For STM32F4x9, the system clock HCLK runs @ 180 MHz and the SDRAM @ 90 MHz.   
For STM32F7x6/7/8/9, the system clock HCLK runs @ 200 MHz and the SDRAM @ 100 MHz.   
Only one LTDC layer is used.   
Two AHB masters concurrent access to the SDRAM (LTDC + DMA2D).

Table 19. Example of supported display resolutions in specific STM32 hardware configurations   

<table><tr><td rowspan=1 colspan=9>Display characteristics</td><td rowspan=1 colspan=2>STM32 LTDC configuration</td></tr><tr><td rowspan=2 colspan=1>Resolution</td><td rowspan=2 colspan=6>Refresh rate (Hz)</td><td rowspan=2 colspan=1>Pixel clock (MHz)</td><td rowspan=2 colspan=1>Display standard</td><td rowspan=1 colspan=2>Color depth</td></tr><tr><td rowspan=1 colspan=1>SDRAM 16-bit</td><td rowspan=1 colspan=1>SDRAM 32-bit</td></tr><tr><td rowspan=1 colspan=1>320 x 240 (QVGA)</td><td rowspan=1 colspan=6></td><td rowspan=1 colspan=1>5.6</td><td rowspan=2 colspan=1>Custom</td><td rowspan=2 colspan=2>Up to 32 bpp</td></tr><tr><td rowspan=1 colspan=1>480 x 272</td><td rowspan=1 colspan=6></td><td rowspan=1 colspan=1></td><td rowspan=1 colspan=1>9.5</td></tr><tr><td rowspan=2 colspan=1>640 x 480 (VGA)</td><td rowspan=2 colspan=2></td><td rowspan=1 colspan=1></td><td rowspan=2 colspan=2></td><td rowspan=1 colspan=1></td><td rowspan=2 colspan=1></td><td rowspan=2 colspan=1>25.175</td><td rowspan=2 colspan=1>Industry standard</td><td rowspan=2 colspan=1>Up to 24 bpp</td></tr><tr><td rowspan=1 colspan=2></td><td rowspan=1 colspan=2></td></tr><tr><td rowspan=1 colspan=1>800 x 600 (SVGA)</td><td rowspan=1 colspan=6>60</td><td rowspan=1 colspan=1>40.000</td><td rowspan=2 colspan=1>VESA guidelines(1)</td><td rowspan=1 colspan=1>Up to 16 bpp</td><td rowspan=1 colspan=1>Up to 24 bpp</td></tr><tr><td rowspan=1 colspan=1>1024 x 768 (XGA)</td><td rowspan=1 colspan=6></td><td rowspan=1 colspan=1>65</td><td rowspan=4 colspan=1>8 bpp</td><td rowspan=2 colspan=1>Up to 16 bpp</td></tr><tr><td rowspan=1 colspan=1>1280 x 768</td><td rowspan=1 colspan=6></td><td rowspan=1 colspan=1>68.250</td><td rowspan=1 colspan=1>CVT R.B(2)</td></tr><tr><td rowspan=1 colspan=1>1280 x 720 (HD)</td><td rowspan=1 colspan=6></td><td rowspan=2 colspan=1>74.25</td><td rowspan=2 colspan=1>CEA(3)</td><td rowspan=2 colspan=1>Up to 16 bpp(4)</td></tr><tr><td rowspan=1 colspan=1>1920 x1080</td><td rowspan=1 colspan=6>30</td></tr></table>

1. VEvieniartionarzate providing display monitor timing (DMT) standards. 2. CVT R.B: coordinated video timings reduced blanking standard by VESA. 3. CEA = consumer electronics association. 4. Up to 8 bpp for the STM32F4x9 microcontrollers.

5.2.3

# Check the compatibility of the display panel interface with the LTDC

The usermust choose he LCD panel depending on he applicatin needsThe two main factors to considr when chg eLC pane e heeolut andhe olordept.Thes t actors havedirpac following parameters:

required GPIO number framebuffer size and location pixel clock of the display

When selecting a display panel, the user must:

Ensure that the display interface is compatible with the LTDC (parallel RGB with control signals). Check if the control signals can be controlled by the LTDC (additional GPIOs are sometimes needed). Ensure that the display signal levels are matching the LTDC interface signal levels (VDD from 1.8 V to 3.6 V).   
Ensure that the display pixel clock is supported by the LTDC maximum pixel clock defined in the relevant STM32 product datasheet.   
Verify that the display timings parameters are supported by the LTDC timings (see Table 6).   
Check that the display size and color depth are supported by the LTDC (refer to Section 5.2.2: Checking display compatibility considering the memory bandwidth requirements).

# STM32 package selection guide

A hin i in terms of GPIOs:

whether an external memory is needed and which is the bus width

which LTDC configuration to use: RGB565, RGB666, or RGB888

When selecting the STM32 package,he user has toconsider the RGBinterfaces availabilityand the appliatin ement terumbr. sermust er he produc dtasheet   vlle packages with GPIOs.

A syac pckahic en ee of GPIO number, is to use STM32CubeMX (the pinout tab).

Table 20 summarizes the available packages and RGB interface of some STM32 MCUs embedding an LTDC.

# Table 20. STM32 packages with LTDC peripheral versus RGB interface availability

<table><tr><td rowspan=1 colspan=21>Cells with &quot;NA&quot; = the package is not available for that specific product.Cells with &quot;-&quot; = the package is available without RGBxxX outputs options.Cells with &quot;18&quot; value = only RGB565 and RGB666 parallel outputs are supported.Cells with &quot;24&quot; value = all of RGB565, RGB666, and RGB888 outputs are supported.</td></tr><tr><td rowspan=1 colspan=1>Product</td><td rowspan=1 colspan=1>0</td><td rowspan=1 colspan=1>0</td><td rowspan=1 colspan=1>2</td><td rowspan=1 colspan=1>20</td><td rowspan=1 colspan=1>1</td><td rowspan=1 colspan=1>0</td><td rowspan=1 colspan=1>2</td><td rowspan=1 colspan=1>0</td><td rowspan=1 colspan=1>W!1SL</td><td rowspan=1 colspan=1>2</td><td rowspan=1 colspan=1>20</td><td rowspan=1 colspan=1>2</td><td rowspan=1 colspan=1>0</td><td rowspan=1 colspan=1>2</td><td rowspan=1 colspan=1>20</td><td rowspan=1 colspan=1>0</td><td rowspan=1 colspan=1>0</td><td rowspan=1 colspan=1>0</td><td rowspan=1 colspan=1>2</td><td rowspan=1 colspan=1>20</td></tr><tr><td rowspan=1 colspan=1>VFBGA264STM32F429/439</td><td rowspan=1 colspan=1>18</td><td rowspan=1 colspan=1>NA</td><td rowspan=1 colspan=1>18</td><td rowspan=1 colspan=1>24</td><td rowspan=1 colspan=1>24</td><td rowspan=1 colspan=1>24</td><td rowspan=1 colspan=1>24</td><td rowspan=1 colspan=1>24</td><td rowspan=1 colspan=1>18</td><td rowspan=1 colspan=1>NA</td><td rowspan=1 colspan=1>NA</td><td rowspan=1 colspan=1>NA</td><td rowspan=1 colspan=1>NA</td><td rowspan=1 colspan=1>NA</td><td rowspan=1 colspan=1>NA</td><td rowspan=1 colspan=1>NA</td><td rowspan=1 colspan=1>NA</td><td rowspan=1 colspan=1>NA</td><td rowspan=1 colspan=1>NA</td><td rowspan=1 colspan=1>NA</td></tr><tr><td rowspan=1 colspan=1>STM32F469/479(1)</td><td rowspan=1 colspan=1>18</td><td rowspan=1 colspan=1>NA</td><td rowspan=1 colspan=1>18</td><td rowspan=1 colspan=1>24</td><td rowspan=1 colspan=1>24</td><td rowspan=1 colspan=1>24</td><td rowspan=1 colspan=1>24</td><td rowspan=1 colspan=1>24</td><td rowspan=1 colspan=1>NA</td><td rowspan=1 colspan=1>24</td><td rowspan=1 colspan=1>NA</td><td rowspan=1 colspan=1>NA</td><td rowspan=1 colspan=1>NA</td><td rowspan=1 colspan=1>NA</td><td rowspan=1 colspan=1>NA</td><td rowspan=1 colspan=1>NA</td><td rowspan=1 colspan=1>NA</td><td rowspan=1 colspan=1>NA</td><td rowspan=1 colspan=1>NA</td><td rowspan=1 colspan=1>NA</td></tr><tr><td rowspan=1 colspan=1>STM32F7x6</td><td rowspan=1 colspan=1>18</td><td rowspan=1 colspan=1>18</td><td rowspan=1 colspan=1>24</td><td rowspan=1 colspan=1>NA</td><td rowspan=1 colspan=1>24</td><td rowspan=1 colspan=1>24</td><td rowspan=1 colspan=1>24</td><td rowspan=1 colspan=1>24</td><td rowspan=1 colspan=1>24</td><td rowspan=1 colspan=1>NA</td><td rowspan=1 colspan=1>NA</td><td rowspan=1 colspan=1>NA</td><td rowspan=1 colspan=1>NA</td><td rowspan=1 colspan=1>NA</td><td rowspan=1 colspan=1>NA</td><td rowspan=1 colspan=1>NA</td><td rowspan=1 colspan=1>NA</td><td rowspan=1 colspan=1>NA</td><td rowspan=1 colspan=1>NA</td><td rowspan=1 colspan=1>NA</td></tr><tr><td rowspan=1 colspan=1>STM32F7x7</td><td rowspan=1 colspan=1>18</td><td rowspan=1 colspan=1>NA</td><td rowspan=1 colspan=1>24</td><td rowspan=1 colspan=1>NA</td><td rowspan=1 colspan=1>24</td><td rowspan=1 colspan=1>24</td><td rowspan=1 colspan=1>24</td><td rowspan=1 colspan=1>24</td><td rowspan=1 colspan=1>NA</td><td rowspan=1 colspan=1>NA</td><td rowspan=1 colspan=1>NA</td><td rowspan=1 colspan=1>NA</td><td rowspan=1 colspan=1>NA</td><td rowspan=1 colspan=1>NA</td><td rowspan=1 colspan=1>NA</td><td rowspan=1 colspan=1>NA</td><td rowspan=1 colspan=1>NA</td><td rowspan=1 colspan=1>NA</td><td rowspan=1 colspan=1>NA</td><td rowspan=1 colspan=1>NA</td></tr><tr><td rowspan=1 colspan=1>STM32F7x8(1)</td><td rowspan=1 colspan=1>NA</td><td rowspan=1 colspan=1>NA</td><td rowspan=1 colspan=1>NA</td><td rowspan=1 colspan=1>NA</td><td rowspan=1 colspan=1>NA</td><td rowspan=1 colspan=1>NA</td><td rowspan=1 colspan=1>NA</td><td rowspan=1 colspan=1>NA</td><td rowspan=1 colspan=1>NA</td><td rowspan=1 colspan=1>NA</td><td rowspan=1 colspan=1>24</td><td rowspan=1 colspan=1>NA</td><td rowspan=1 colspan=1>NA</td><td rowspan=1 colspan=1>NA</td><td rowspan=1 colspan=1>NA</td><td rowspan=1 colspan=1>NA</td><td rowspan=1 colspan=1>NA</td><td rowspan=1 colspan=1>NA</td><td rowspan=1 colspan=1>NA</td><td rowspan=1 colspan=1>NA</td></tr><tr><td rowspan=1 colspan=1>STM32F7x9(1)</td><td rowspan=1 colspan=1>NA</td><td rowspan=1 colspan=1>NA</td><td rowspan=1 colspan=1>NA</td><td rowspan=1 colspan=1>NA</td><td rowspan=1 colspan=1>NA</td><td rowspan=1 colspan=1>24</td><td rowspan=1 colspan=1>24</td><td rowspan=1 colspan=1>24</td><td rowspan=1 colspan=1>NA</td><td rowspan=1 colspan=1>NA</td><td rowspan=1 colspan=1>24</td><td rowspan=1 colspan=1>NA</td><td rowspan=1 colspan=1>NA</td><td rowspan=1 colspan=1>NA</td><td rowspan=1 colspan=1>NA</td><td rowspan=1 colspan=1>NA</td><td rowspan=1 colspan=1>NA</td><td rowspan=1 colspan=1>NA</td><td rowspan=1 colspan=1>NA</td><td rowspan=1 colspan=1>NA</td></tr><tr><td rowspan=1 colspan=1>STM32H7R7/7S7</td><td rowspan=1 colspan=1></td><td rowspan=1 colspan=1></td><td rowspan=1 colspan=1></td><td rowspan=1 colspan=1></td><td rowspan=1 colspan=1>24</td><td rowspan=1 colspan=1>24(UFBGA176 + 25)</td><td rowspan=1 colspan=1>24</td><td rowspan=1 colspan=1>NA</td><td rowspan=1 colspan=1>NA</td><td rowspan=1 colspan=1>NA</td><td rowspan=1 colspan=1>NA</td><td rowspan=1 colspan=1>-</td><td rowspan=1 colspan=1>-</td><td rowspan=1 colspan=1>18</td><td rowspan=1 colspan=1>24</td><td rowspan=1 colspan=1>NA</td><td rowspan=1 colspan=1>NA</td><td rowspan=1 colspan=1>NA</td><td rowspan=1 colspan=1>NA</td><td rowspan=1 colspan=1>NA</td></tr><tr><td rowspan=1 colspan=1>STM32N647xx</td><td rowspan=1 colspan=1>NA</td><td rowspan=1 colspan=1>NA</td><td rowspan=1 colspan=1>NA</td><td rowspan=1 colspan=1>NA</td><td rowspan=1 colspan=1>NA</td><td rowspan=1 colspan=1>NA</td><td rowspan=1 colspan=1>NA</td><td rowspan=1 colspan=1>NA</td><td rowspan=1 colspan=1>NA</td><td rowspan=1 colspan=1>NA</td><td rowspan=1 colspan=1>NA</td><td rowspan=1 colspan=1>NA</td><td rowspan=1 colspan=1>NA</td><td rowspan=1 colspan=1>NA</td><td rowspan=1 colspan=1>24</td><td rowspan=1 colspan=1>24</td><td rowspan=1 colspan=1>24</td><td rowspan=1 colspan=1>24</td><td rowspan=1 colspan=1>24</td><td rowspan=1 colspan=1>24</td></tr></table>

IP STM32 MIPI-DSI host.

# 5.4

# LTDC synchronization with DMA2D and CPU

# 5.4.1 DMA2D usage

The DMA2D is a master on the AHB bus matrix performing graphical data transfers inter-memories. It is recommended to use the DMA2D in order to offload the CPU.

The DMA2D implements four basic tasks:

Fill a rectangular shape with a unique color.   
Copy a frame or a rectangular part of a frame from a memory to another.   
C aguar wh another memory.   
Blend two images with different sizes and pixel format and store the resulting image in one resulting memory.

# 5.4.2

# LTDC and DMA2D/CPU synchronization

Wua Multiple buffering techniques, such as the double buffering, are commonly used to avoid displaying the framebuffer calculation on the screen.

Ev whleuprza te L UA  olv e the VSYNC signal to synchronize the workflow of these two masters (LTDC and either CPU or DMA2D).

T L hehal atmu l hileA aeex iu two buffers needs to be flipped.

![](images/d8ff2f344017e8aefaf049901283eee53cbb98b0d32d54dc01736905c134f5ec.jpg)  
Figure 24. Double buffering: synchronizing LTDC with DMA2D or CPU

The LTDC provides different options to synchronize this workflow:

Prgram he neinteruption with thevalue the ast creen Theinterupt hander must e framebuffers and start the next framebuffer calculation.

Program the shadow reload register (LTDC_SRCR) to vertical blanking reload to change the LTDC framebuffer address on the VSYNC period, and poll on VSYNC bit of the LTDC_CDSR register to unblock the DMA2D.

# 5.5

# Graphic performance optimization

Aspreiusahoceneeuemoryndwihemosportn arme grahicapplication.Thi section providessome recomendations optimizehe graphicperformances ba bandwidth optimizations of the framebuffer memory.

# 5.5.1

# Memory allocatio

The smart architecture of the STM32 MCUs enables a significant system performance gain when using the internal SRAM memory, split into two or more slaves.

Splitting up the slaves memories between masters helps to decrease the competition between them when they access simultaneously the same SRAM. This action also creates an additional system bus bandwidth.

As shown in the example described in Figure 25, SRAM2 and SRAM3 are dedicated to graphics for the framebuffer while the SRAM1 is used by the CPU.

![](images/0eac8fb61be3e9ddd7f65bc55a25c44daf3ce27f47499ead2ec818ae4cf791ae.jpg)  
Figure 25. Example of taking advantage from memory slaves split on STM32F4x9

# 5.5.2

# Optimizing the LTDC framebuffer fetching from external memories (SDRAM or SRAM)

Anotherconsieration elate heSDRAM/SRAMishe placement  theframbufferandhe e lengt iSnce he HB usmai prohii aeoy burs asshat coses ebye boary an s e LTDC peors burs rea  6/8 ytorHB/AXI placing h content emeufferres the edge of 1 Kbyte splits the burst read into single accesses, which can heavily affect the graphical performances.

The same problem can ccr when hedata ie le  piels otamultiple  6/128 bytes  AHB AXUndehen eLTCd bur c by that splits the burst read into single accesses.

As a consequence, when the LTDC des not generate a burst, eac access is interrupted by a CPU oranother master access (such as Chrom-Art Accelerator or Ethernet).

The interruptions highly reduce the LTDC bandwidth on a high-latencymemory like the exteral SDRAM that leads to an underrun.

To or use one of the two following methods:

Reduce the layer window and the framebuffer line widths.   
Add a number of dummy bytes at the end of every line of pixels to match the closest frame line width multiple of 64/128 bytes (for AHB/AXI).

# Example: 480 x 272 display with 24 bpp

F ay   piewi ohe equal to 1440 bytes that is not a multiple of 64/128 bytes (for AHB/AXI).

# Note:

Fthat reolution, thave multiplee width se 4/2 bytes or AHB/AX, the ser can usno color depth such as RGB565.

Sinc the frame lne s composed o 2 bursts f 64/128 bytes (or AHB/AXl) and one 32 bytes burst, the10th into single accesses.

Figure 26 illustrates the 1-Kbyte boundary cross problem for the given example.

![](images/44ce01cf10edc3c265c96b47691702844f75f2504b3e2e3f81eea1df34a4cb00.jpg)  
Figure 26. Burst access crossing the 1-Kbyte boundary

For this example, the two methods to solve the crossing 1-Kbyte boundary issue are detailed below:

# First method

Reduce the layer window and the framebuffer line widths: use the LTDC layer windowing feature by reducing the window size to match the closest frame line width multiple of 64/128 bytes (for AHB/AXIl). Since the window width is reduced, the framebuffer size must also be reduced since the extra 22 and 23 bursts for all frame lines are not fetched nor displayed by LTDC.

This method solves the 1-Kbyte boundary crossing issue with a slight window width decrease (see Figure 27).

The code below is based on the HAL drivers and shows an example of setting the pitch as described in Figure 27:

/\* Setting the Layer1 window to 448x272 at positions X = 16 and Y = 0 \*/ pLayerCfg.WindowX0 = 16; pLayerCfg.WindowX1 = 464; pLayerCfg.WindowY0 = 0; pLayerCfg.WindowY1 = 272; pLayerCfg.PixelFormat = LTDC_PIXEL_FORMAT_RGB888; pLayerCfg.Alpha = 255; pLayerCfg.Alpha0 = 0; pLayerCfg.BlendingFactorl = LTDC_BLENDING_FACTOR1_PAxCA; pLayerCfg.BlendingFactor2 = LTDC_BLENDING_FACTOR1_PAxCA; Framebuffer start address: LTDC fetches the image directly from internal flash that the re   
al image width is 448 pixels. Only the 448 pixels width is displayed\*/ pLayerCfg.FBStartAdress = (uint32_t)&image_data_Image_RGB888_448x272; pLayerCfg.ImageWidth = 448; pLayerCfg.ImageHeight = 272; pLayerCfg.Backcolor.Blue = 0; pLayerCfg.Backcolor.Green = 0; pLayerCfg.Backcolor.Red = 0; if (HAL_LTDC_ConfigLayer(&hltdc, &pLayerCfg, O) != HAL_OK) { Error_Handler();

![](images/d1c5f79392cff530ce412f79ff4dbd215b93bd6be8e9aa96058c56e959ed4165.jpg)  
Figure 27. Reducing layer window and framebuffer line widths

# Second method

Add a number of dummy bytes at the end of every line of pixels to match the closest frame line width multiple of 64/128 bytes (for AHB/AXI). This can be done using the LTDC layer pitch (see Section 4.: Two programmable LTDC layers). To do this, the user must consider the two points below:

The framebuffer must contain the dummy bytes (as described in Figure 28):when writing data into the framebuffer, it can be done by programming an output offset of the DMA2D equal to the difference between the closest burst multiple and the actual line length data size. The LTDC line length must always be equal to the active data size, but, the LTDC pitch must be programmed with the value of the closest bytes number multiple of 64/128 bytes (for AHB/AXI).

The HAL_LTDC_SetPitch function provided under the hal_Itdc driver can be used to program the desired p val umber piels. or the previus example,h value he pitch  pas  this must be equal to512 (512is the number of pixels per lie corresponding toa line length sizeof1536 bytes that is multiple of 64/128 bytes (for AHB/AXi).

The code below is based on the HAL drivers and shows an example of setting the pitch as described in Figure 28:

/\* Setting the Layer1 window to 480x272 at positions X = 0 and Y = 0 \*/ pLayerCfg.WindowX0 = 0; pLayerCfg.WindowX1 = 480; pLayerCfg.WindowYO = 0; pLayerCfg.WindowY1 = 272; pLayerCfg.PixelFormat = LTDC_PIXEL_FORMAT_RGB888; pLayerCfg.Alpha = 255; pLayerCfg.Alpha0 = 0; pLayerCfg.BlendingFactor1 = LTDC_BLENDING_FACTOR1_PAxCA; pLayerCfg.BlendingFactor2 = LTDC_BLENDING_FACTOR1_PAxCA;   
/\* Framebuffer start address: LTDC fetches the image directly from internal flash that the re   
al image width is 480 pixels but additional 32 pixels are added to each line to get a 512 pix   
els pitch.   
Only the 480 pixels width is displayed\*/ pLayerCfg.FBStartAdress = (uint32_t)&image_data_Image_RGB888_512x272; pLayerCfg.ImageWidth = 480; pLayerCfg.ImageHeight = 272; pLayerCfg.Backcolor.Blue = 0; pLayerCfg.Backcolor.Green = 0; pLayerCfg.Backcolor.Red = 0; if (HAL_LTDC_ConfigLayer(&hltdc, &pLayerCfg, O) != HAL_OK) Error_Handler(); \* Sets the Layerl (index 0 refers to Layerl) Pitch to 512 pixels \*/ HAL_LTDC_SetPitch(&hltdc, 512, 0);

![](images/5c73c35c1ff79251433de9eed7cc986a8a95d20a192cf79110be74d194b3af3c.jpg)  
Figure 28. Adding dummy bytes to make the line width multiple of 64 bytes

Active display area 480 x 272 X 32 dummy bytes X 64 dummy bytes X 64 bytes burst x 32 bytes burst

# Optimizing the LTDC framebuffer fetching from SDRAM

Making random access into a bank generates some precharge cycles that increase the SDRAM latency seen by the LTDC. As he LTDC peror equenti access ortant hat oothe ast access e me SDRAM bank.

The external SDRAM is composed of multiple banks. Given that, making random accesses on a bank generates some precharge and activates some cycles.The framebuffr must be placed in an independent bank accessed only by the LTDC. This action reduces the external memory latency and leads to a higher throughput. As a coquence whenedoublermeburhniqus iioendehavheuffrn separate banks.

T eyorgeuheRAM geacu adding an offset with the size of one bank.

![](images/5636da822f1292b5810578e2e858706edfc5d4ca1ee46453685a4b9ea4ec314d.jpg)  
Figure 29. Placing the two buffers in independent SDRAM banks

For instance, when the SDRAM bank size is equal to 4 Mbytes, the following line code can be used:

/\* Framebuffer addresses within external SDRAM \*/ /\* Frontbuffer in bank 1 of SDRAM memory \*/ uint32_t FrontBuffer = LCD_FB_START_ADRESS; /\* Backbuffer in the bank 2 of sDRAM memory \*/ uint32_t BackBuffer = LCD_FB_START_ADRESS + 1024 \* 1024 \* 4;

# SDRAMRBURST

Another interesting feature allowing optimization of reading performances from the SDRAM is the use of RBURST.

The DRAM controller adds a cacheable read FFO with a depth ix 3-it lnes.The read FFOis used when the read burst is enabled and allows the next read accesses to be anticipated during CAS latencies.

# 5.5.4

# Framebuffer content update during blanking period

Awa tzh eaceally whee peancottlec seeuey performed.

# 5.6

# Special recommendations for Cortex-M7 (STM32F7/H7)

This section illustrates some recommendations for the STM32F7/H7 devices embedding the Cortex-M7 CPU.

Theeendations a eci he ortex-M ic ashe ollwg particularit pare  e Cortex-M4:

. The Cortex-M7 does some speculative read accesses to normal memory regions. These speculative read accesses may cause high latency or system errors when performed on external memories over FMC, Quad-SPI or Octo-SPI. This impacts AHB/AXI masters (such as LTDC) accessing the FMC, Quad-SPI or Octo-SPI, and particularly decreases graphical performances and may lead to system errors (if the LTDC framebuffer is located in external memory and/or if the Quad-SPI memory is used for graphics). The Cortex-M7 CPU embeds an L1-Cache (see Figure 10). Som graphi issues may beencountere due ositable cace settings.Bad graphic visal efes may our if cache maintenance is not properly performed. If the suitable cache maintenance method is not used, graphical performances may be impacted.

# 5.6.1

# Disable FMC Bank1 if not used

Afer reset, the FMC Bank1 is always enabled to allow boot into external memories. Snce the CortexM7 does some speculations, it can generate a speculative read access to the first FMC bank.

The default MC configuration being very slow, this speculative access blocks theaccess to the MC bhe AHB masters for a very long time, leading to underrun on the LTDC side.

To prevent CPU speculative read accesses on FMC Bank1, it is recommended to disable it when  is not usd.   
This can be done by resetting the MBKEN Bit in FMC_BCR1 register that is, by default, enabled after reset.

To disable the FMC Bank1, the following code can be used in STM32F7 series:

/\* Disabling FMC Bank1: After reset FMC_BCR1 = Ox000030DB where MBKEN = 1b meaning that FMC_B ankl is enabled   
and MTYP[1:0]= 10 meaning that memory type is set to NOR Flash/OneNAND Flash\*/   
FMC_Bank1->BTCR[0] = 0x000030D2;

For more details on FMC configuration, refer to the STM32 product reference manual.

# 5.6.2

# Configure the memory protection unit (MPU)

This section defines the STM32F7/H7 system memory attributes and the basic MPU concepts. It also describes guePr evnahial oassuelateorex-e read accesses and cache maintenance.

# Note:

This section only describes some necessary basic MPU concepts needed for configuration.

For frther details on MPU and cache, refer to the documents [6], [7], [8], and the Ar Cortex-M7 tecnial reference manual.

# MPU attributes configuration

Inordr  prevent graphic peormance issues elated o the Cortex-M7 seculative read acces, heue mu reviw al hememory map  theaplication and conigure he MP aording  thearwar.S te user has to set the following configurations:

Define the framebuffer MPU region and the other application MPU regions.   
MPU must be configured according to the size of the memory used by the application.   
The MPU attributes of the unused regions must be configured to strongly ordered execute never (XN). For example, for the Quad-SPl, if an 8-Mbyte memory is connected, the remaining 248-Mbyte unused space (from a total 256-Mbyte addressable space) must be set to strongly ordered XN. See example in Section 7.2.7.   
Prevent the Cortex-M7 speculative read accesses to the external SDRAM/SRAM (if the FMC swap is enabled, see Figure 30). To do it, the SDRAM/SRAM MPU region must be set to execute never (XN). If the Cortex-M7 CPU is used for framebuffer processing (writing to SDRAM/SRAM), the framebuffer region MPU attribute must be set to normal cacheable with read and write access permission.

# Note:

The frmebuffer MPU region atributemust bet to execute never ince it is nly dedicated or grahical content creation.

Figure 30 describes the STM32F7 FMC banks and Quad-SPI MPU memory attributes at default system memory map

![](images/75f7b0fbe506446ea5cb3bd8a08f4a4ad61b84aa1df5219323ee50cd3322f967.jpg)  
Figure 30. FMC SDRAM and NOR/PSRAM memory swap at default system memory map (MPU disabled)

# MPU and cache policy configuration

The use o Cortex-M7 cache alows system and graphic performances to be boosted. This performance gain is especially seen when the CPU accesses external memories such as SDRAM or Quad-SPI.

In h platnhe u llthembuffatin  etealeoy DRAM RAM.In at as h consider the following points when using the cache:

MPU memory region cacheability   
As previously illustrated in Figure30, in the default system memory region MPU attrbutes, some system memory regions are normal cacheable while others are device noncacheable.   
When the CPU is used for framebuffer processing, the user must change the framebuffer region MPU attribute to normal cacheable (or do an FMC swap, see Figure 30).

ache maintenance and data coherency: visual impact of WBWA without cache maintenance operat

The data coherency issue is often encountered when performing framebuffer processing using a Cortex-M7 CPU with L1-cache enabled and a WBWA cache policy. This issue occurs when multiple masters such as Cortex-M7 and LTDC share the same region (framebuffer) and the cache maintenance is not performed. WheeU pos e meuff rimeuffer  heeuffrginasback cache policy, the processed result (image to be displayed) is not seen on the framebuffer (may be SRAM or SDRAM), and then it is not displayed.

To avoid this issue, the following methods can be used:

Configure the framebuffer region cache attribute to write-through (WT). In that case, each write operation is performed on the cache and on the framebuffer.

# Note:

For some products, there is a limitation with the write-through policy. Use the write-back policy as stated in the second method. For more details about this limitation, refer to the product related errata sheet.

Configure the framebufer region cache attribute to write back write allocate (WBwA) and perform the cache maintenance by software.

Write-through is safer for data coherency but may impact graphic performances.

The suitable cache policy matching the application must be used. Each method has its cons and pros, so the user must consider the following particularities for each method:

Write-through is very simple to manage (no need to perform cache maintenance by software) and safer for data coherency but it generates a lot of single-write operations to the framebuffer, which may impact LTDC accesses.

# Note:

The user must also consider that cache maintenance may impact graphic performances even when the CPU is not used for framebuffer processing. Thus, in some applications, the CPU accesses the external SDRAM or SRAM for other purposes than graphics with cache enabled. In that case, cache maintenance may impact the LTDC accesses.

Writeback-write allocate: it is more suitable to use WBWA and software routine and to synchronize the cache maintenance operation with the LTDC during blanking. This allows an additional bandwidth creation on the framebuffer memory (SRAM or SDRAM). The cache maintenance operation need to be performed by software after writing data to the framebuffer memory region. This is done by forcing a D-cache clean operation using the CMSIS function SCBC1eanDCache (). So, all the dirty lines in the cache are written back to the framebuffer.

# MPU configuration example

Aeaple MPU cogrationebeect..oghow  eeufPU whe he s sd (wit cachenable orgraphical operationshe escribeexampl create  e STM32F746G-DISCO board hardware configuration, where the external SDRAM is used or ramebufr and the external Quad-SPI flash memory contains the graphic primitives.

# 5.7

# LTDC peripheral configuration

This section describes the steps needed to configure the LTDC peripheral.

# Note:

It is recommended to reset the LTDC peripheral before starting the configuration and it is alsorecommended to guarante that the peripheral is inreset satTheLTDC can e reset by settig he corresponding bi he RCC_APB2RSTR register, which resets the three clock domains.

# 5.7.1

# Display panel connection

T LCharntea prov ht b er olor us,an peec rRG8 color pel. The LTDC hardware interface provides also timing signals: LCD_HSYNC, LCD_VSYNC, LCD_DE, and LCD_CLK.

Th LTDC GPIOsmust becnigure he correpondent alternate nctin.For more detal n LTDC al fns avalbilityvrs Geltenancnmap b e produc datt.

# Note:

All GPlOs have to be configured in very-high-speed mode.

# Connecting lower palette display panels

For display panels with a lower color palette (such as RGB666 and RGB565), the bus connecion must be done with the most significant bits of the dat signals. igureshows an example f conecing anRGB iplay panel.

![](images/b763d1437bfc8902488dd9424f8aa1c2b094617e4700a47e2e64b23b7930aa53.jpg)  
Figure 31. Connecting an RGB666 display panel

# GPIOs configuration using STM32CubeMX tool

Toconnect a display panel to an STM32 MCU, the user must configure the GPIOs to be used for interfacing. Using the STM32CubeMX too is a very simple, easy, and rapid way to configure the LTDC peripheral and its GIO, since  allows a project o be generatd with a preconigured LTDC ee Section 7.. LTDC GPIOs configuration).

# Configuration of specific pins of a display module

Sispayodules may neeothe sals   fullcnal.s an some peherals n be t control these signals.

An example of using GPIOs to control the displayenable pin (LCD_DISP) on a display panel is described in Section 7.2.3: LTDC GPIOs configuration.

# Enabling LTDC interrupts

Tble u  DC esuable LCgoaeu NVIC available in the LTDC_IER register described in Table 7. LTDC interrupts summary.

Th FIFOanransrontrut able nheal_IriveHALTC

An example of enabling LTDC interrupts using STM32CubeMX is described in Section 7.2.3: LTDC GPIOs configuration

# 5.7.2

# LTDC clocks and timings configuration

This section describes the steps needed to configure the LTDC clock and timings respecting the display specifications. It also provides a configuration example for the ROCKTECH (RK043FN48H) display embedded on the STM32F746G-DISCO board.

# System clock configuration

It is recommended to use the highest system clock to get the best graphic performances. This recommendation aarhextealmemoyebu. exteralmemoy rhmeuf highest allowed clock speed must be used to get the best memory bandwidth.

For instance, for the STM32F4x9, the maximum system speed is 180 MHz. So, if an external SDRAM is connected to the FMC, the maximum SDRAM clock is 90 MHz (HCLK/2).

For the STM32F7, the maximum system speed is 216 MHz but with this speed and HCLK/2 prescaler the SDRAM spee exceeds the maximum allowed speed (see product datasheet or more details). So, to get the maximum SDRAM, it is recommended to configure HCLK to 200 MHz, then the SDRAM speed is set to 100 MHz.

The clock configuration providing the highest performances is:

STM32F4x9:HCLK @ 180 MHz and SDRAM @ 90 MHz STM32F7:HCLK @ 200 MHz and SDRAM @ 100 MHz

An example of LTDC configuration using STM32CubeMX is described in Section 7.2.4: LTDC peripheral configuration.

# Pixel clock and timings configuration

A t agehegaphial pliatindevelomen hesermust haveareadyhecean confirha to be configured must be already known, either extracted from the display datasheet or calculated (see Section 5.2.2: Checking display compatibility considering the memory bandwidth requirements).

Example: LTDC timings configuration for ROCKTECH RK043FN48H display embedded on the STM32F746G-recommended to use typical display timings.

The cells in bold highlight the values used in the example presented below.

Table 21. LCD-TFT timings extracted from ROCKTECH RK043FN48H datasheet   

<table><tr><td rowspan=1 colspan=3>Item</td><td rowspan=1 colspan=1>Symbol</td><td rowspan=1 colspan=1>Min.</td><td rowspan=1 colspan=1>Typ.</td><td rowspan=1 colspan=1>Max.</td><td rowspan=1 colspan=1>Unit</td></tr><tr><td rowspan=1 colspan=3>DCLK frequency</td><td rowspan=1 colspan=1>Fclk</td><td rowspan=1 colspan=1>5</td><td rowspan=1 colspan=1>9</td><td rowspan=1 colspan=1>12</td><td rowspan=1 colspan=1>MHz</td></tr><tr><td rowspan=1 colspan=3>DCLK period</td><td rowspan=1 colspan=1>Tclk</td><td rowspan=1 colspan=1>83</td><td rowspan=1 colspan=1>110</td><td rowspan=1 colspan=1>200</td><td rowspan=1 colspan=1>ns</td></tr><tr><td rowspan=5 colspan=2>Hsync</td><td rowspan=1 colspan=1>Period time</td><td rowspan=1 colspan=1>Th</td><td rowspan=1 colspan=1>490</td><td rowspan=1 colspan=1>531</td><td rowspan=1 colspan=1>605</td><td rowspan=1 colspan=1>DCLK</td></tr><tr><td rowspan=1 colspan=1>Display period</td><td rowspan=1 colspan=1>Thdisp</td><td rowspan=1 colspan=1>-</td><td rowspan=1 colspan=1>480</td><td rowspan=1 colspan=1>-</td><td rowspan=1 colspan=1>DCLK</td></tr><tr><td rowspan=1 colspan=1>Back porch</td><td rowspan=1 colspan=1>Thbp</td><td rowspan=1 colspan=1>8</td><td rowspan=1 colspan=1>43</td><td rowspan=1 colspan=1>-</td><td rowspan=1 colspan=1>DCLK</td></tr><tr><td rowspan=1 colspan=1>Front porch</td><td rowspan=1 colspan=1>Thfp</td><td rowspan=1 colspan=1>2</td><td rowspan=1 colspan=1>8</td><td rowspan=1 colspan=1></td><td rowspan=1 colspan=1>DCLK</td></tr><tr><td rowspan=1 colspan=1>Pulse width</td><td rowspan=1 colspan=1>Thw</td><td rowspan=1 colspan=1>1</td><td rowspan=1 colspan=1>-</td><td rowspan=1 colspan=1>-</td><td rowspan=1 colspan=1>DCLK</td></tr><tr><td rowspan=5 colspan=2>Vsync</td><td rowspan=1 colspan=1>Period time</td><td rowspan=1 colspan=1>Tv</td><td rowspan=1 colspan=1>275</td><td rowspan=1 colspan=1>288</td><td rowspan=1 colspan=1>335</td><td rowspan=1 colspan=1>H</td></tr><tr><td rowspan=1 colspan=1></td><td rowspan=1 colspan=1>Display period</td><td rowspan=1 colspan=1>Tvdisp</td><td rowspan=1 colspan=1>-</td><td rowspan=1 colspan=1>272</td><td rowspan=1 colspan=1>-</td><td rowspan=1 colspan=1>H</td></tr><tr><td rowspan=1 colspan=1></td><td rowspan=1 colspan=1>Back porch</td><td rowspan=1 colspan=1>Tvbp</td><td rowspan=1 colspan=1>2</td><td rowspan=1 colspan=1>12</td><td rowspan=1 colspan=1></td><td rowspan=1 colspan=1>H</td></tr><tr><td rowspan=1 colspan=1>Front porch</td><td rowspan=1 colspan=1>Tvfp</td><td rowspan=1 colspan=1>1</td><td rowspan=1 colspan=1>4</td><td rowspan=1 colspan=1></td><td rowspan=1 colspan=1>H</td></tr><tr><td rowspan=1 colspan=1>Pulse width</td><td rowspan=1 colspan=1>Tvw</td><td rowspan=1 colspan=1>1</td><td rowspan=1 colspan=1>10</td><td rowspan=1 colspan=1>-</td><td rowspan=1 colspan=1>H</td></tr></table>

Based on the above table, the extracted timing parameters are:

Display period (active width) = 480 pixels

Back porch HBP = 43 pixels   
Front porch HFP = 8 pixels   
Pulse width HSYNC = 1 pixel (minimum value)   
Display period (active height) = 272 lines   
Vertical back porch VBP = 12 lines   
Front porch VFP = 4 lines   
Pulse width VSYNC = 10 lines

Program timing parameters: once timing parameters are extracted, they are used to program the LTDC timing registers, Table 22 summarizes all the parameters to be programmed.

Timing parameters configuration with ST32CubeMX: it is very easy to program the tming parameters using STM32CubeMX. The user must simply fil the extracted parameters in the LTDC configuration window (see section Section 7.2.4: LTDC peripheral configuration).

Table 22. Programming LTDC timing registers   

<table><tr><td rowspan=1 colspan=2>Register</td><td rowspan=1 colspan=1>•</td><td rowspan=1 colspan=1>Value to beprogrammed</td></tr><tr><td rowspan=2 colspan=1>LTDC_SSCR</td><td rowspan=1 colspan=1>HSW[11:0]</td><td rowspan=1 colspan=1>HSYNC Width - 1</td><td rowspan=1 colspan=1>0</td></tr><tr><td rowspan=1 colspan=1>VSH[11:0]</td><td rowspan=1 colspan=1>VSYNC Height - 1</td><td rowspan=1 colspan=1>9</td></tr><tr><td rowspan=2 colspan=1>LTDC_BPCR</td><td rowspan=1 colspan=1>AHBP[11:0]</td><td rowspan=1 colspan=1>HSYNC Width + HBP - 1</td><td rowspan=1 colspan=1>43</td></tr><tr><td rowspan=1 colspan=1>AVBP[10:0]</td><td rowspan=1 colspan=1>VSYNC Height + VBP - 1</td><td rowspan=1 colspan=1>21</td></tr><tr><td rowspan=2 colspan=1>LTDC_AWCR</td><td rowspan=1 colspan=1>AAW[11:0]</td><td rowspan=1 colspan=1>HSYNC Width + HBP + Active Width - 1</td><td rowspan=1 colspan=1>523</td></tr><tr><td rowspan=1 colspan=1>AAH[10:0]</td><td rowspan=1 colspan=1>VSYNC Height + BVBP + Active Height - 1</td><td rowspan=1 colspan=1>293</td></tr><tr><td rowspan=2 colspan=1>LTDC_TWCR</td><td rowspan=1 colspan=1>TOTALW[11:0]</td><td rowspan=1 colspan=1>HSYNC Width + HBP + Active Width + HFP - 1</td><td rowspan=1 colspan=1>531</td></tr><tr><td rowspan=1 colspan=1>TOTALH[10:0]</td><td rowspan=1 colspan=1>VSYNC Height+ BVBP + Active Height + VFP - 1</td><td rowspan=1 colspan=1>297</td></tr></table>

Pi clock configuration with STM32CubeMX: the pixel clock is calculatd wih a 60Hz reresh rate ashown below:

LCD_CLK = TOTALW x TOTALH x refresh rate   
Based on Table 22, TOTALW= 531 and TOTALH = 297.   
And for this example:   
LCD_CLK = 531 x 297 x 60 = 9.5 MHz   
Refer to the LTDC pixel clock configuration STM32CubeMX example in Section 7.2.4.

# LTDC control signals polarity configuration

The LTDC control signals (HSYNC, VSYNC, DE, and LCD_CLK) polarities must be configured respecting the display specifications.

# Note:

On theDEontro sgal must verteversu heDE polaridicate ntheisplyatashet.h control signals must be configured exactly like the display datasheet.

# 5.7.3 LTDC layers configuration

Thisectondescribes heneeded eps  conigure the LTC ayers repecing he display izeand th ol depth.

As previously statedin Section .., he LTDC features two independently configurable layers the userc is displayed (the default color is black).

he user can display Layer1 + background or display Layer1 + Layer2 + backgroun

# Display only the background

Iu background black color is displayed (LTDC_BCCR = 0x00000000).

To set a blue background color, the LTDC_BCCR register must be set to Ox000000FF.

# Layer parameters configuration

Once LTDC GPIOs, clocks and timings are properly set, the user must configure the following LTDC layer parameters. Each LTDC layer has its own parameters that must be configured separately:

window size and position   
pixel input format   
framebuffer start address   
framebuffer size (image width and image height) and pitch   
layer default color in ARGB8888 format   
layer constant alpha for blending   
layer blending factor1 and factor2

An example of LTDC layer parameters configuration using STM32CubeMX is described in LTDC Layer parameters configuration.

# Note:

All layer parameters can bemodified on the fly, except for the CLUT. The new configuration has to be ether reloaded immediately or during vertical blanking period by configuring the LTDC_SRCR register.

# 5.7.4 Display panel configuration

Some displays require to be configured using serial communication interfaces such as I2C or SPI. For instance, the STM32F429I-DISCO embeds the ILI9341 display module that is initialized through the SPI interface.

Adeicativeohpymodull.icludglizationconguratioca available in the STM32Cube firmware package

under:STM32Cube_FW_F4_Vx.Xx.x\Drivers\BSP\Components\ili9341

Aeapleilizatiahnccl examples for the STM32F429I-Discovery board

under:STM32Cube_FW_F4_Vx.Xx.x\Projects\STM32F429I-Discovery\Examples\LTDC\LTDc_Display_2Layers

# Storing graphic primitives

Grappivat ataiil content that is displayed.

Stadata must e placeinanonvolatilmemory When hemount  dat o tore s elatively ow the internal flash memory can be used. Otherwise, graphical contents must be placed in external memories.

The STM32 MCUs offer parallel (FMC) or serial (Quad-SPI) interface for external NOR Flash memories (see Table 3).

TilA lle O a Quad-SPI Flash.

Refer to the document [9] for more details on storing graphic content on QSPI memory.

# 5.8.1

# Converting images to C files

Tah iv ohe use tools can be used to generate C or \*.h files.

Warning: The user must convert images to C files respecting the configured pixel input format described in Pixel input format. Some tools may generate C or \*.h files with Red and Blue colors swapped. To avoid this issue, the LCD image converter tool can be used.

T LCDmaoner eyszableeeol useveagend era esoa plSec.spayoenteal .

# 5.9

# Hardware considerations

Twportant hardware interfaces must be carefully designed: he LTDC interface and the external memory interface (used for framebuffer) such as FMC_SDRAM or FMC_SRAM.

# LTDC parallel interface

When the pixel clock is below 40 MHz (SVGA), a simple 3.3 V signaling can be used.

t isposible  reach 83 MHz with a parallelRGB f the lad and the wie ength are educe orexape nterface on the same PCB with on-board an LVDS or HDMI transceiver).

It is recommended to configure the LTDC GPIOs at the maximum operating speed OSPEEDRy[1:0] = 11. Refer to the product reference manual for a description of the GPIOx_SPEEDR register.

# FMC SDRAM/SRAM interface

When using an external SRAM or SDRAM memory for a framebuffer, the FMC-SDRAM and the FMC-SRAM interfaces speed depend on many factors including the board layout and the pad speed. A good PCB design enables to reach the maximum pixel clock described in Table 10 to Table 16.

The layout must be as good as possible in ordero get the best performances. For more information n PCB routing guidelines, refer to the documents [10] and [11] available on the STMicroelectronics website

# 6 Saving power consumption

Wv Slee mode to reduce the power consmption. In Sleep mode, al peripherals can be enabled (FMC-SDRAM and LTDC for instance) while the CPU is stopped.

External memories, such as SDRAM or Quad-SPI Flash, can be driven in low-power modes whenever it is needed in order to avoid the waste of power.

Ippltn oowtat u euiispaphis eanee cti SAM saves even more power.

Thep aloisable pu low-powmod  isot nee whenng epltn.

# LTDC application examples

This section provides:

some graphic implementation examples considering the resources requirements an example on how to create a basic graphical application a summary of STM32 reference boards that embeds LTDC and features an on-board LCD-TFT panel

# 7.1

# Implementation examples and resources requirements

# 7.1.1

# Single-chip MCU

Thanks to ther integrated SRAM, the STM32 MCUs can beused or graphic applications, without the nee exteal SDRAM/SRAMmemory r framebuffeAlso,thanks totherhigh-izeinternal flash (up toMbyes), all pins, easy PCB design and cost savings.

D internal flash up to 2 Mbytes, storing user application code and graphic primitives

Depending on the internal SRAM size for each STM32 MCU, the user can interface with a corresponding display size and color depth as illustrated below:

STM32F7x7: use SRAM1 (368 Kbytes) to support resolutions 400 x 400 16 bpp (313 Kbytes) or 480 x 272 16 bpp (255 Kbytes)   
STM32F7x6: use SRAM1 (240 Kbytes) to support 320 x 320 resolution with 16 bpp (200 Kbytes) STM32F469/F479: use SRAM1 (160 Kbytes) to support 320 x 240 resolution with 16 bpp (154 Kbytes   
STM32F429/F439: use SRAM1 (112 Kbytes) to support 320 x 240 resolution with 8 pp (75 Kytes). STM32 MCU packages: LQFP 100 or TFBGA100

Figure 32 ilustrates a graphic implementation example, with a single chip and no external memories used.

![](images/e4e34b1ed3435a2617886a319b27e0df3cc99bbf361093572c7a6601e0f32e58.jpg)  
Figure 32. Low-end graphic implementation example

# 7.1.2 MCU with external memory

In order to interface with higher resolution displays, an external memory connected to the FMC isneede for framebuffer. An external Quad-SPI flash memory can be used to store graphic primitives.

For mid-end or high-end graphical applications, the following hardware configuration example can beused:

external Quad-SPI flash memory with up to 256 Mbytes addressable memory-mapped, used to store graphic primitives   
external SDRAM 32-bit memory used for framebuffer   
STM32 MCU packages: UFBGA169, UFBGA176, LQFP 176, LQFP 208, TFBGA216, WLCSP168, and WLCSP180.

Figure ilustrates a graphicmplementation example where two external memories ae connected t n STM32 MCU, one for the framebuffer and the other for graphic primitives.

![](images/c6e568161d55fb2b2ef8424f382581af35f5c5e9cfad42373388b93f1fa9fac0.jpg)  
Figure 33. High-end graphic implementation example   
Table 23 summarizes an example of graphic implementations in different STM32 hardware configurations.

Table 23. Example of graphic implantations with STM32 in different hardware configurations   

<table><tr><td rowspan=1 colspan=1>Variant</td><td rowspan=1 colspan=1>Display size</td><td rowspan=1 colspan=1>Color depth</td><td rowspan=1 colspan=1>External memory-SDRAM</td><td rowspan=1 colspan=1>Display interface</td><td rowspan=1 colspan=1>STM32 package(1)</td></tr><tr><td rowspan=4 colspan=1>High-end</td><td rowspan=1 colspan=1>1280 x 720</td><td rowspan=2 colspan=1>16bpp</td><td rowspan=2 colspan=1></td><td rowspan=2 colspan=1></td><td rowspan=2 colspan=1>UFBGA176TFBGA216/UFBGA169/</td></tr><tr><td rowspan=1 colspan=1>1024 x 768</td></tr><tr><td rowspan=1 colspan=1>1600 x 272</td><td rowspan=2 colspan=1>24bpp</td><td rowspan=2 colspan=1>32-bit</td><td rowspan=2 colspan=1>RGB888</td><td rowspan=2 colspan=1>LQFFP176/LQFP208WLCSP180/WLCSP168/UFBGA176 + 25/TFBGA225</td></tr><tr><td rowspan=1 colspan=1>800 x 600</td></tr><tr><td rowspan=4 colspan=1>Mid-end</td><td rowspan=1 colspan=1>800 x 600</td><td rowspan=1 colspan=1>16bpp</td><td rowspan=4 colspan=1>16-bit</td><td rowspan=4 colspan=1>RGB666</td><td rowspan=4 colspan=1>LQFP144/WLCSP143</td></tr><tr><td rowspan=1 colspan=1>800 x 480</td><td rowspan=3 colspan=1>24bpp</td></tr><tr><td rowspan=1 colspan=1>640 x 480</td></tr><tr><td rowspan=1 colspan=1>400 x 400(2)</td></tr><tr><td rowspan=4 colspan=1>Low-end</td><td rowspan=1 colspan=1>400 x 400</td><td rowspan=4 colspan=1>16bpp</td><td rowspan=4 colspan=1>No</td><td rowspan=4 colspan=1>RGB666</td><td rowspan=4 colspan=1>LQFP100/TFBG100/UFBGA144</td></tr><tr><td rowspan=1 colspan=1>480 x 272</td></tr><tr><td rowspan=1 colspan=1>320 x 320</td></tr><tr><td rowspan=1 colspan=1>320 x 240</td></tr></table>

Package availability of STM32 MCUs embedding LTDC is summarized in Table 20. 2400 x 400 and 320 x 320 are specific display resolutions commonly used for smart watches.

# Example: creating a basic graphical application

This section provides an example based on the STM32F746G-DISCO board, describing the steps required to create a basic graphic application.

# 7.2.1

# Hardware description

The hardware resources embedded on the STM32F746G-DISCO board are used in this example. Figure 34 describes the graphic hardware resources to be used:

The pink arrow shows the pixel data path to the display.

![](images/363ffed009c302d7874663fb79a5edfbc9857ebd2796c8bf3cd0d789fb33fa0c.jpg)  
Figure 34. Graphic hardware configuration in the STM32F746G-DISCO

The STM32F746G-DISCO board embeds a parallel true color RGB888 LCD-TFT panel with a 480 x 272 resolution.

For more details on the STM32F746G-DISCO board, refer to the document [12].   
Figure 35 shows the ROCKTECH RK043FN48H true color panel (RGB888) connected to the STM32F746 MCU.

![](images/2e9a82190649e9f20bc9995ae1f6046aa5eae673ca7ddaa53d98b673c7aa848a.jpg)  
Figure 35. LCD-TFT connection in the STM32F746G-DISCO board

Ashownhe ast gureheispaymodulcneethe C throu tofferent cates:

LTDC interface pins:

24-bit RGB interface Timing signals: LCD_HSYNC, LCD_VSYNC, LCD_DE and LCD_CLK

Other specific pins:

LCD_DISP to enable/disable display Standby mode   
INT interrupt line: allows the touch sensor to generate interrupts   
interface to control the touch sensor   
LCDRST reset pin: allows the LCD-TFT reset. This pin is connected to the global MCU rest pn (NRST).   
LCD_BL_A and LCD_BL_K pins for LED backlight control: the backlight is controlled b the STLD40DPUR circuit.

Bacliht cnrolle:hLDPRc eribur  eerhaerat 3.0 o   Vvuh the STLD40D datasheet for more information on the backlight controller.

Thehigh level on the LCDBL_CTRL (PK3) signal lights the backlight on, while the low level switches it off.

# Note:

It isposible hang heispay ghtnes dim hebacklight tensity) yplyin lowrequency kHz) PWM signal to the EN pin 7of the STLD40D circuit. This action needs a rework since there is no timer PWMoutput alternatefnction available on the PK3 pin.The user must remove the R81 resistance and co another GPIO pin with the PWM output alternate function.

![](images/8d40c61965455a2e4e23ce590109076dc511d96ea40d33697b71ac9634e1822d.jpg)  
Figure 36. Backlight controller module

# 7.2.2

# How to check if a specific display size matches the hardware configuration

Thi us   spay     t Hz  wi  olor dept ae the right hardware configuration.

# Desired display panel

The desired display is the ROCKTECH RK043FN48H-CT672B display:

display resolution: 480 x 272 pixels with LED backlight and capacitive touch panel display interface: 24-bit RGB888 (in total 28 signals)

# Determining framebuffer size and location

Depending n  izendon he nternal availableRAM ie,hefrmebuffer an be locat eithehe internal SRAM or in the external SDRAM. The total embedded SRAM size for the STM32F746NGH6 MCU is 320 Kbytes where SRAM1 (240 Kbytes) can be used (see Figure 10).

The framebuffer size is calculated in the following way:

for 24 bpp, framebuffer (Kbyte) = 480 x 272 x 3 / 1024 = 382.5   
for 16 bpp, framebuffer (Kbyte) = 480 x 272 x 2 / 1024 = 255   
for 8 bpp, framebuffer (Kbyte) = 480 x 272 / 1024 = 128

y s aitelyoaliashe 128 x 2 Kbytes exceeds the internal SRAM size.

For e16 p colordepth andina dubleeuffcniguratin he quimuffersiz x Kbytes)excees theinternal SRAM size, o using an external SRAM or SDRAM is a must for this configuration. For oloret nubleuratn uuffer internal SRAM size (2 x 382.5 Kbytes), so using an external SRAM, or SDRAM is a must for this configuration. The next step is to check he SDRAM16-bit us with can sustain hedesiesolution andcolorepth.

# Check if a 480 x 272 resolution with 24 bpp fits the SDRAM 16-bit configuration

At this stage the user decided t use n external SDRAM but stil has tocheck fhe SDRAM16-bit u width cl arwapleentation heiovey rmatches e8   0 zispay zan color depth.

Ian  cl the user must first compute the pixel clock.

The computed LCD_CLK is about 9.5 MHz (for computing pixel clock refer to Section 7.2.3: LTDC GPIOs configuration).

Th esmuseasoll ee i clco e maximum LCD_CLK indicated in Table 11:

number of used LTDC layers: in this example, only one layer used   
system clock speed HCLK and framebuffer memory speed: HCLK @ 200 MHz and SDRAM @ 100 MHz external framebuffer memory bus width 16-bit SDRAM   
number of AHB masters accessing concurrently to external SDRAM: two masters (DMA2D and LTDC)

Reeri he pie clocTabl L +Aol n  aeow, e i cock c 34 MHz for a 16-bit SDRAM.

So, the 16-bit SDRAM bus width is quite enough to sustain a 480 x 272 @ 60 Hz resolution (LCD_CLK = 9.5 MHz) with 24 bpp color depth.

# 2.3

# LTDC GPIOs configuration

As shown on Figure 35, the ROCKTECH RK043FN48H display is connected to the STM32F746xx using a parallel RGB888 of 24 bits.

# LTDCRGB interface pins configuration

Once that the STM32CubeMX project is created, in the Pinout tab, choose one from the listed hardware configurations. Figure 37 shows how to select the RGB888 hardware configuration with the STM32CubeMX. Theuser can also configure all he Gs by setting therigt altenate ncon oreach G e b .

![](images/58a61dfc48a88873f0161f0b30a4ec85355acfb1089aaf2d8e3985295b917f88.jpg)  
Figure 37. STM32CubeMX: LTDC GPIOs configuration

If afer selecting one hardware configuration (RGB888 as shown in the above fgure), the used GPIOs do not ma wi paboreaeu f ecthe uhoowuaally J LCaea

![](images/f54b1ce154c8b9fa4ce234c0879f1c8074188062ece65e3c35b774aac5ab027b.jpg)  
Figure 38. STM32CubeMX: PJ7 pin configuration to LTDC_G0 alternate function

The used pins are highlightein green once all LDC interface GIs are correctly conigure The user mst now set their speed to very high.

To set the GPIOs speed using STM32CubeMX, select the Configuration tab then click on the LTDC button as shown in Figure 39.

![](images/244196af629f492ce4fd482c7c6da10dd9c15506c210269496c6962a88f7f209.jpg)  
Figure 39. STM32CubeMX: LTDC configuration

In the LTDC Configuration window described inFigure 0, selec al the LTDC pis, then e heaxiuuu speed to Very High.

![](images/ebd319e528f6a963a6a2a99a798c17e6d36c0cd9df1c4fee125dd8da910dde39.jpg)  
Figure 40. STM32CubeMX: LTDC GPIOs output speed configuration

# Specific pins configuration of the display module

Ol LTDCinterac pins corry conigu penghe LCD-TFT panelcoon he smus configure the other specific pins connected to the display (LCD_DISP, INT pin and I2C interface).

T LCDDIP p P12 p) has  egur a tu push-pull wth high level inorder able display, otherwise the display stays in Standby mode.

Tgure he LCDDISP pi inutut mde wit STM32CubeMX, in the put tab click on the 12 p he select GPIO_Output (see Figure 41).

![](images/e9051e7f0729e1dfd28b628bddb69cf2c8aaaaaf6d66788e54b554c37dfd0e34.jpg)  
Figure 41. STM32CubeMX: display enable pin (LCD_DISP) configuration   
Then, the LDCDISP (PI12) pinmust be configured to high level: in the Configuration tab, click on the GPIO button. In the Pin Configuration window, set the GPlO output level to high as described in Figure 42.

![](images/7a8af43c1541ea080f1a866faf1797f589e6dd80f9438ce5381f7e5e3be216aa.jpg)  
Figure 42. STM32CubeMX: setting LCD_DISP pin output level to high

DeR8 ul ch  evel ulLCDBLRL kept floating. There is no need to configure this pin.

# Enabling LTDC interrupts

T IFOanrnrroerutblheal_iveHALT The user must just enable the LTDC global interrupt on the NVIC side.

Toeable he LDC global interrupts using STM32CubeMX, select heConfiguration tab then click on he LTDC button as shown in Figure 39.

In the LTDC Configuration window shown in Figure 43, select the NVIC settings tab. Check the LTDC global interrupts then click on the OK button.

![](images/678f099ac9e651de1b281db6300c2458e809982fb9326d922f30f8bc3f06a7aa.jpg)  
Figure 43. STM32CubeMX: enabling LTDC global and error interrupts

# 7.2.4

# LTDC peripheral configuration

This section demonstrates how to configure LTDC clocks, timings, and layer parameters using STM32CubeMX.

LTDC clock and timing configuration

# System clock configuration

In this example the system clock is configured with the following configuration:

use of internal HSI RC, where main PLL is used as system source clock HCLK @ 200 MHz (Cortex-M7 and LTDC both running @ 200 MHz)

# Note:

HCLK is set to 200 MHz but not 216 MHz. This is to set the SDRAM_FMC at its maximum speed of 100 MHz with HCLK/2 prescaler.

In order to configure the system clock using STM32CubeMX, select the Clock Configuration tab as shown in Figure 44.

![](images/a8aac9e8b3957701c7cdb51576ad61daeffb0fd1146e2d7fb18e35add41b4dab.jpg)  
Figure 44. STM32CubeMX: clock configuration tab

To get the system clock HCLK @ 200 MHz, set the PLLs and the prescalers in the Clock Configuration tab as shown in Figure 45.

![](images/18d0ad96c8e93c883b99baddcb8d6bd054e241e58403211765d27acb5c85ab67.jpg)  
Figure 45. STM32CubeMX: System clock configuration

# Pixel clock configuration

The LCDCLK must be calculated using the parameters found in the display datasheet. In order to do the ccateusealwi  talheTpi clcalculatwi refresh rate as shown below:

LCD_CLK = TOTALW x TOTALH x refresh rate (see extracted display timing parameters in Section 5.7.2) ==> LCD_CLK = 531 x 297 x 60 = 9.5 MHz

T cnigure the LTDC pixel clock to 9.5 MHzusin ST32CubeMX, select theClock Configuration tab, then se the PLLSAI and the prescalers as shown in Figure 46.

![](images/2c52d7a221fc56034ebc7874a52d6eca55de99305d8994819ce40a20ce5cb0de.jpg)  
Figure 46. STM32CubeMX: LTDC pixel clock configuration

# Timing parameter configuration

Inore confgure he isplaymigs usiT32CubeMX, the usermustextract hetmig paramer rom the device datasheet. For thi example, seean extract ROCEC datasheet n TableItisrecomeded to use the typical display timings.

Igupmeusrantu the clicnh u cgu io esermus elec  Sett and fill in the timing values (refer to Figure 47).

# LTDC control signals polarity configuration

Referring to the display datasheet, HSYNC and VSYNC must be active low and the DE signal must be active ivo be inverted.

Figure 47 shows the control signal polarity configuration and the LTDC configuration according to the ROCKTECH display datasheet.

![](images/c988cde01e71559fba91d6be0a6f9a64982f164c1e052e9a390c1a72fbf009dd.jpg)  
Figure 47. STM32CubeMX: LTDC timing configuration

# LTDC Layer parameters configuration

At this stage, all LTDC clocks and timings have been set in the STM32CubeMX project.   
The user must configure the LTDC Layer1 parameters according to the display size and the color depth.

If needed, the user can also enable the Layer2 by setting to 2layers the Numberof Layers feld in the LTDC configuration window shown in Figure 48.

T et the LTDC Layer1 parameters using STM32CubeMX, the user must select the Configuration tab then clic on the LTDC button as shown in Figure 38.

In the LTDCConfiguration window shown in Figure 8, the user must select the Layer Settings tab, set the LTDC layer1 parameters and then click on the OK button.

Aerat pr witeiohcroGa

![](images/b4840a5518a88966528b5f0ce620d87a0d1278c7253191abad0e97888837ac11.jpg)  
Figure 48. STM32CubeMX: LTDC Layer1 parameters setting

# 7.2.5

# Display an image from the internal flash

Ia to display an image from the internal flash.

do it, the user must first convert the image to a C or a header file and add it to the project.

# Converting the image to a header file using the LCD image converter tool

The user must generate the header file respecting the configured LTDC layer pixel input format RGB565 (see Pixel input format and Section 5.8).

In thisexample, the LCD-Image-Converter-20161012 tool is used (see Section 5.8 or more details on this tool). Tcver nmage,he usermust fstrun heLCD-mag-Converer tol.Then, inthe home pageshown Figure 49, click on File->Open and select the image file to be converted.

The used iage izemust be aligned with the LTDC Layerconguration (480 x 27. I the used iage s not aligned with the LTDC Layer1 configuration, the user can resize the image by going to Image->Resizeor choose another image with the correct size.

For this example, the used image size is 480 x 272 and shows the STMicroelectronics logo (see Figure 50).

![](images/c0738b04c7e2410a1b64d9e73f9771ddc75340defb98a9ff456f1f7d3d80653c.jpg)  
Figure 49. LCD-Image-Converter: home page

The image is then displayed on the LCD-Image-Converter tool home page as described in Figure 50.

Tr ea egeRean BewaplaiS . Options->Conversion as shown in Figure 50.

![](images/8957ff9789c66a00eeea66fe6da1bd8ee8acac57a4e80b540c3e3611a77de8a9.jpg)  
Figure 50. LCD-Image-Converter: image project

In te Otis winohown n igureelec he ageb then select heGB5 color in he re f Set the Block size field to 32-bit and click on the OK button.

# Note:

Tern tablu as ap Bu in the Conversion window matrix tab.

![](images/8edc66ab67a66cd1e4938c70d3f5fb88e02606e54ff7d8cd11c75af9d70a4244.jpg)  
Figure 51. LCD-Image-Converter: setting conversion options

Save button.

![](images/d9bb5310f177e969cab8caf5e989eaa04f90a1ddb74040ef135684fc5f4360aa.jpg)  
Figure 52. LCD-Image-Converter: generating the header file

represents two pixels.

I table definition as shown below:

/\* Converted image: image_data_STLogo definition \* const uint32_t image_data_sTLogo[65280] = {Oxffffffff, Oxffffffff,

# Setting the LTDC framebuffer Layer1 start address to the internal flash (image address in the flash)

The generated project by STM32CubeMX must include in the main. file theXLTCIniunction that allows the LTDC peripheral configuration.

Ips yur image in the internal flash.

TheMXLTCInitfunction s presented below with the framebuffer start address settig

/\* LTDC configuration function generated by STM32CubeMX tool \*/   
static void MX_LTDC_Init(void) LTDC_LayerCfgTypeDef pLayerCfg; hltdc.Instance = LTDC; /\* LTDC control signals polarity setting \*/ hltdc.Init.HSPolarity = LTDC_HSPOLARITY_AL; hltdc.Init.VSPolarity = LTDC_vSPOLARITY_AL; hltdc.Init.DEPolarity = LTDC_DEPOLARITY_AL; hltdc.Init.PCPolarity = LTDC_PCPOLARITY_IPC; /\* Timings configuration \*/ hltdc.Init.HorizontalSync = 0; hltdc.Init.VerticalSync = 9; hltdc.Init.AccumulatedHBP = 43; hltdc.Init.AccumulatedVBP = 21; hltdc.Init.AccumulatedActiveW = 523; hltdc.Init.AccumulatedActiveH = 293; hltdc.Init.TotalWidth = 531; hltdc.Init.TotalHeigh = 297; /\* Background color \*/ hltdc.Init.Backcolor.Blue = O; hltdc.Init.Backcolor.Green = 0; hltdc.Init.Backcolor.Red = Ox0; if (HAL_LTDC_Init(&hltdc) != HAL_OK) Error_Handler(); /\* Layerl Window size and position setting \*/ pLayerCfg.WindowX0 = 0; pLayerCfg.WindowX1 = 480; pLayerCfg.WindowY0 = 0; pLayerCfg.WindowY1 = 272; /\* Layeri Pixel Input Format setting \*/ pLayerCfg.PixelFormat = LTDC_PIXEL_FORMAT_RGB565; /\* Layer1 constant Alpha setting 100% opaque \*/ pLayerCfg.Alpha = 255; /\* Layer1 Blending factors setting \*/ pLayerCfg.BlendingFactor1 = LTDC_BLENDING_FACTOR1_PAxCA; pLayerCfg.BlendingFactor2 = LTDC_BLENDING_FACTOR2_PAxCA; /\* User should set the framebuffer start address (can be Oxc0000000 if external SDRAM is   
used)\*/ pLayerCfg.FBStartAdress = (uint32_t)&image_data_STLogo; pLayerCfg.ImageWidth = 480; pLayerCfg.ImageHeight = 272; /\* Layeri Default color setting \*/ pLayerCfg.Alpha0 = O; pLayerCfg.Backcolor.Blue = 0; pLayerCfg.Backcolor.Green = 0; pLayerCfg.Backcolor.Red = 0; if (HAL_LTDC_ConfigLayer(&hltdc, &pLayerCfg, O) != HAL_OK) { Error_Handler(); }   
}

Onc the LTDC is correctly configured in the project, the user must build the project, and then run t.

# 7.2.6

# FMC SDRAM configuratiol

The external SDRAM must be configured as it contains the LTDC framebuffer. To configure the FMC_SDRAM and the SDRAM memory device mounted on the STM32746G-Discovery board, STM32CubeMX or the existing BSP driver can be used.

To configure the FMC_SDRAM using the BSP driver, follow the steps below:

Ad the following filestothe project:BSP stm32746g_discovery_sdram.anstm32746g_discovery_sdram.h. Include the stm32f7xx_hal_sdram.h in the main.c file. Add the stm32f7xx_hal_sdram.c and stm32f7xx_I_fmc.c HAL drivers to the project.

nable the SDRAM module in the stm32f7xx_hal_conf.h file by uncommenting the SDRAM module definition.   
3.Call the BSP_SDRAM_Init () function in the main () function.

# 7.2.7 MPU and cache configuration

illSetuuhl issues related to the Cortex-M7 speculative read accesses and cache maintenance.

This section describes an example of MPU attribute configuration with respect to the STM32F746G-DISCO board hardware configuration.

The MPU memory attributes can be easily configured with STM32CubeMX. A code example of MPU configuration generated using STM32CubeMX is described at the end of this section.

# MPU configuration example: FMC_SDRAM

Igaulu lRA Bank1 while the backbuffer is placed in the SDRAM Bank2 with respect to the SDRAM bandwidth optimization described in Section 5.5.3.

The following MPU regions are created (FMC without swap):

Region0: defines the SDRAM memory size 8 Mbytes Region1: defines the frontbuffer 256 Kbytes (16 bpp x 480 x 272). It overlaps Region0. Region2: defines the backbuffer 256 Kbytes (16 bpp x 480 x 272). It overlaps Region0.

Figure 53 illustrates the MPU configuration of the SDRAM region.

![](images/ad554cada8b3d815f5d98444baf14ad3be8649393984eee02334fc9b2574ecca.jpg)  
Figure 53. FMC SDRAM MPU configuration example

# MPU configuration example: Quad-SPI in Memory-mapped mode

This example shows how to configure the MPU for the Quad-SPI interface. The Quad-SPI memory contains grahi prtivs andcan becee by Cortex-M7,DMA2D, r LTDC. Forhat, he Qua-SP inteacut be set to Memory-mapped mode and the MPU regions must be configured as described below:

CPU speculative read access to that region.   
Region4: defines the real Quad-SPI memory space reflecting the size of the memory that can be accessed by any master.

Figure 54 illustrates the MPU configuration of the Quad-SPI region.

![](images/ec37c7dde5952bbfb5f48683760aece8279df4cbb01b9d53b8bc76e26dc5191a.jpg)  
Figure 54. MPU configuration for Quad-SPI region

# SDRAM and Quad-SPI MPU configuration example

The following code (generated by STM32CubeMX) shows how to set the MPU attributes for the FMC_SDRAM and Quad-SPI respecting the previously described configurations.

/\* MPU Configuration \*,   
void MPU_Config(void)   
{ MPU_Region_InitTypeDef MPU_InitStruct; /\* Disables the MPU \*/ HAL_MPU_Disable(); /\* Configure the MPU attributes for region 0 \*/ \* Configure the MPU attributes for SDRAM to normal memory\*/ MPU_InitStruct.Enable = MPU_REGION_ENABLE; MPU_InitStruct.Number = MPU_REGION_NUMBERO; MPU_InitStruct.BaseAddress = OxC000000; MPU_InitStruct.Size = MPU_REGION_SIZE_8MB; MPU_InitStruct.SubRegionDisable = Ox0; MPU_InitStruct.TypeExtField = MPU_TEX_LEVELO; MPU_InitStruct.AccessPermission = MPU_REGION_FULL_ACCESS; MPU_InitStruct.DisableExec = MPU_INSTRUCTION_ACCESS_ENABLE; MPU_InitStruct.IsShareable = MPU_ACCESS_NOT_SHAREABLE; MPU_InitStruct.IsCacheable = MPU_ACCESS_CACHEABLE; MPU_InitStruct.IsBufferable = MPU_ACCESS_NOT_BUFFERABLE; HAL_MPU_ConfigRegion(&MPU_InitStruct); /\* Configure the MPU attributes for region 1 \*/ \* Configure the MPU attributes for the frontbuffer to normal memory\*/ MPU_InitStruct.Enable = MPU_REGION_ENABLE; MPU_InitStruct.Number = MPU_REGION_NUMBER1; MPU_InitStruct.BaseAddress = OxC0000000; MPU_InitStruct.Size = MPU_REGION_SIZE_256KB; MPU_InitStruct.SubRegionDisable = Ox0; MPU_InitStruct.TypeExtField = MPU_TEX_LEVELO; MPU_InitStruct.AccessPermission = MPU_REGION_FULL_ACCESS; MPU_InitStruct.DisableExec = MPU_INSTRUCTION_ACCESS_DISABLE; MPU_InitStruct.IsShareable = MPU_ACCESS_NOT_SHAREABLE; MPU_InitStruct.IsCacheable = MPU_ACCESS_CACHEABLE; MPU_InitStruct.IsBufferable = MPU_ACCESS_NOT_BUFFERABLE; HAL_MPU_ConfigRegion(&MPU_InitStruct); /\* Configure the MPU attributes for region 2 \*/   
\* Configure the MPU attributes for the backbuffer to normal memory\*/ MPU_InitStruct.Enable = MPU_REGION_ENABLE; MPU_InitStruct.Number = MPU_REGION_NUMBER2; MPU_InitStruct.BaseAddress = OxC0200000; MPU_InitStruct.Size = MPU_REGION_SIZE_256KB; MPU InitStruct.SubRegionDisable = Ox0; MPU_InitStruct.TypeExtField = MPU_TEX_LEVELO; MPU_InitStruct.AccessPermission = MPU_REGION_FULL_ACCESS; MPU_InitStruct.DisableExec = MPU_INSTRUCTION_ACCESS_DISABLE; MPU_InitStruct.IsShareable = MPU_ACCESS_NOT_SHAREABLE; MPU_InitStruct.IsCacheable = MPU_ACCESS_cACHEABLE; MPU_InitStruct.IsBufferable = MPU_ACCESS_NOT_BUFFERABLE; HAL_MPU_ConfigRegion(&MPU_InitStruct);   
/\* Configure the MPU attributes for region 3 \*/   
/\* Configure the MPU attributes for Quad-sPI area to strongly ordered memory\*/ MPU_InitStruct.Enable = MPU_REGION_ENABLE; MPU_InitStruct.Number = MPU_REGION_NUMBER3; MPU_InitStruct.BaseAddress = Ox9000000; MPU_InitStruct.Size = MPU_REGION_SIZE_256MB; MPU_InitStruct.SubRegionDisable = Ox0; MPU_InitStruct.TypeExtField = MPU_TEX_LEVELO; MPU_InitStruct.AccessPermission =¯MPU_REGION_NO_ACCESS; MPU_InitStruct.DisableExec = MPU_INSTRUCTION_ACCESS_DISABLE; MPU_InitStruct.IsShareable = MPU_ACCESS_NOT_SHAREABLE; MPU_InitStruct.IsCacheable = MPU_ACCESS_NOT_CACHEABLE; MPU_InitStruct.IsBufferable = MPU_ACCESS_NOT_BUFFERABLE; HAL_MPU_ConfigRegion(&MPU_InitStruct);   
/\* Configure the MPU attributes for region 4 \*/   
/\* Configure the MPU attributes for QSPI memory to normal memory\*/ MPU_InitStruct.Enable = MPU_REGION_ENABLE; MPU InitStruct.Number = MPU REGION NUMBER4; MPU InitStruct.BaseAddress = Ox90000000; MPU_InitStruct.Size = MPU_REGION_SIZE_16MB; MPU_InitStruct.SubRegionDisable = Ox0; MPU_InitStruct.TypeExtField = MPU_TEX_LEVELO; MPU InitStruct.AccessPermission = MPU REGION PRIV RO; MPU_InitStruct.DisableExec = MPU_INSTRUCTION_ACCESS_DISABLE; MPU_InitStruct.IsShareable = MPU_ACCESS_NOT_SHAREABLE; MPU_InitStruct.IsCacheable = MPU_ACCESS_CACHEABLE; MPU_InitStruct.IsBufferable = MPU_ACCESS_NOT_BUFFERABLE; HAL_MPU_ConfigRegion(&MPU_InitStruct); /\* Enables the MPU \*/ HAL_MPU_Enable(MPU_PRIVILEGED_DEFAULT);

# Reference boards with LCD-TFT panel

Sofers  wide range  reference boards such as Nuclo, Discovery, anEvaluaton boards. Many  hem embed display panels.

For STM32 reference boards featuring an on-board display but not embedding an LTDC, the DBI (FMC or SPI) interface is used to connect the STM32 with the display.

For the other STM32 boards, the LTDC is used to interface with the display panel.

These reference boards can be used to evaluate the graphic capability in specific hardware/software configurations.

Table 24 summarizes the STM32 reference boards embedding LTDC and featuring an on-board TFT-LCD pane

Table 24. STM32 reference boards embedding LTDC and featuring an on-board LCD-TFT panel   

<table><tr><td rowspan=2 colspan=1>Product</td><td rowspan=2 colspan=1>Board</td><td rowspan=1 colspan=5>LCD-TFT panel</td><td rowspan=2 colspan=1>Int.SRAMKbyte)</td><td rowspan=2 colspan=1>Ext.SDRAM(bit)</td><td rowspan=2 colspan=1>Ext.SRAM(it)</td><td rowspan=2 colspan=1>Quad-SPI(Mbyte)</td></tr><tr><td rowspan=1 colspan=1>Interface</td><td rowspan=1 colspan=1>Size(Inch)</td><td rowspan=1 colspan=1>Resolution</td><td rowspan=1 colspan=1>Colordepth</td><td rowspan=1 colspan=1>Touchsensor</td></tr><tr><td rowspan=3 colspan=1>STM32F429/439</td><td rowspan=1 colspan=1>32F429IDISCOVERY</td><td rowspan=1 colspan=1>DPI</td><td rowspan=1 colspan=1>2.4</td><td rowspan=1 colspan=1>240 x 320</td><td rowspan=1 colspan=1>RGB666</td><td rowspan=1 colspan=1>Resistive</td><td rowspan=3 colspan=1>256</td><td rowspan=1 colspan=1>16</td><td rowspan=1 colspan=1>NA</td><td rowspan=1 colspan=1>NA</td></tr><tr><td rowspan=1 colspan=1>STM32439I-EVAL2</td><td rowspan=1 colspan=1>DPI</td><td rowspan=1 colspan=1>5.7</td><td rowspan=1 colspan=1>640 x 480</td><td rowspan=1 colspan=1>RGB666</td><td rowspan=1 colspan=1>Capacitive</td><td rowspan=2 colspan=1>32</td><td rowspan=2 colspan=1>16</td><td rowspan=2 colspan=1>NA</td></tr><tr><td rowspan=1 colspan=1>STM32429I-EVAL1</td><td rowspan=1 colspan=1>DPI</td><td rowspan=1 colspan=1>4.3</td><td rowspan=1 colspan=1>480 x 272</td><td rowspan=1 colspan=1>RGB888</td><td rowspan=1 colspan=1>Resistive</td></tr><tr><td rowspan=2 colspan=1>STM32F469/479</td><td rowspan=1 colspan=1>32F4691DISCORY</td><td rowspan=1 colspan=1>MIPI-DSI</td><td rowspan=1 colspan=1>4</td><td rowspan=1 colspan=1>800 x 480</td><td rowspan=1 colspan=1>RGB888</td><td rowspan=1 colspan=1>Capacitive</td><td rowspan=1 colspan=1>384</td><td rowspan=1 colspan=1>32</td><td rowspan=1 colspan=1>NA</td><td rowspan=1 colspan=1>16</td></tr><tr><td rowspan=1 colspan=1>STM32469I-EVAL()</td><td rowspan=1 colspan=1>MIPI-DSI</td><td rowspan=1 colspan=1>4</td><td rowspan=1 colspan=1>800 x 480</td><td rowspan=1 colspan=1>RGB888</td><td rowspan=1 colspan=1>Capacitive</td><td rowspan=1 colspan=1></td><td rowspan=1 colspan=1>32</td><td rowspan=1 colspan=1>16</td><td rowspan=1 colspan=1>64</td></tr><tr><td rowspan=3 colspan=1>STM32F7x6</td><td rowspan=1 colspan=1>32F746GDISCOVERY</td><td rowspan=1 colspan=1>DPI</td><td rowspan=1 colspan=1>4.3</td><td rowspan=1 colspan=1>480 x 272</td><td rowspan=1 colspan=1>RGB888</td><td rowspan=1 colspan=1>Capacitive</td><td rowspan=1 colspan=1></td><td rowspan=1 colspan=1>16</td><td rowspan=1 colspan=1>NA</td><td rowspan=1 colspan=1>16</td></tr><tr><td rowspan=2 colspan=1>STM32746G-EVAL</td><td rowspan=1 colspan=1>DPI</td><td rowspan=1 colspan=1>5.7</td><td rowspan=1 colspan=1>640 x 480</td><td rowspan=1 colspan=1>RGB666</td><td rowspan=1 colspan=1>Capacitive</td><td rowspan=2 colspan=1>320</td><td rowspan=2 colspan=1>32</td><td rowspan=2 colspan=1>16</td><td rowspan=2 colspan=1>64</td></tr><tr><td rowspan=1 colspan=1>DPI</td><td rowspan=1 colspan=1>4.3</td><td rowspan=1 colspan=1>480 x 272</td><td rowspan=1 colspan=1>RGB888</td><td rowspan=1 colspan=1>Resistive</td></tr><tr><td rowspan=2 colspan=1>STM32 F7x9(1)</td><td rowspan=1 colspan=1>STM32F769I-DISCO(2)</td><td rowspan=1 colspan=1>MIPI-DSI</td><td rowspan=1 colspan=1>4</td><td rowspan=1 colspan=1>800 x 480</td><td rowspan=1 colspan=1>RGB888</td><td rowspan=1 colspan=1>Capacitive</td><td rowspan=1 colspan=1></td><td rowspan=1 colspan=1>32</td><td rowspan=1 colspan=1>NA</td><td rowspan=1 colspan=1>64</td></tr><tr><td rowspan=1 colspan=1>STM32F779I-EVALSTM32F769I-EVAL</td><td rowspan=1 colspan=1>MIPI-DSI</td><td rowspan=1 colspan=1>4</td><td rowspan=1 colspan=1>800 x 480</td><td rowspan=1 colspan=1>RGB888</td><td rowspan=1 colspan=1>Capacitive</td><td rowspan=1 colspan=1>512</td><td rowspan=1 colspan=1>32</td><td rowspan=1 colspan=1>16</td><td rowspan=1 colspan=1>64</td></tr></table>

LCADM consumer displays. CAP motherboard to the standard display connector (TE 1-1734248). B-LCD40-DSI1 ordering code.

# 8 Supported display panels

Tpntoebe  eiblteacha poeheeau beloha allow TM32 MCU rultple-paraeisplay pan suc  LCD-TFT an OLED isplayvailable heake:

Different signal polarities Programmable timings and resolutions

The display panel piel clock (asindicated in themanufacturer datasheet) must not be higher than the STM32 c than the maximum pixel clock.

# Frequently asked questions

This section summarizes the most frequently asked questions regarding the LTDC usage and configurations.

Table 25. Frequently asked questions   

<table><tr><td rowspan=1 colspan=1>Question</td><td rowspan=2 colspan=1>AnswerThere is no absolute maximum resolution since it depends on severalparameters such as:color depthused SDRAM bus widthsystem operating speed (HCLK)number of AHB masters accessing concurrently to memory used forframebufferSee Section 5.2.2.</td></tr><tr><td rowspan=1 colspan=1>What is the LTDC maximum supportedresolution?</td></tr><tr><td rowspan=1 colspan=1>Does the STM32F4 or the STM32F7 supporta 1280 x 720p 60 Hz resolution?</td><td rowspan=1 colspan=1>Yes, see examples in Section 5.2.2.</td></tr><tr><td rowspan=1 colspan=1>Which SDRAM bus width must be used for aspecific resolution?</td><td rowspan=1 colspan=1>There is not an exact specific bus width, it depends on the resolution, thecolor depth and whether the SDRAM is shared with other AHB masters or not.The higher the SDRAM bus width, the better. An SDRAM 32-bit provides thebest possible performance.</td></tr><tr><td rowspan=1 colspan=1>How to get the maximal supported resolutionfor a specific hardware?</td><td rowspan=1 colspan=1>Refer to Section 5.2.2.</td></tr><tr><td rowspan=1 colspan=1>Does LTDC support OLED displays?</td><td rowspan=1 colspan=1>Yes, if the OLED display has a parallel RGB interface.</td></tr><tr><td rowspan=1 colspan=1>Does LTDC support STN displays?</td><td rowspan=1 colspan=1>No, STN displays are not supported by LTDC.</td></tr><tr><td rowspan=1 colspan=1>Why the image is displayed with Red andBlue colors swapped?</td><td rowspan=1 colspan=1>This is because the image is not stored into memory respecting the configuredpixel input format (see Section 5.8.1).</td></tr><tr><td rowspan=1 colspan=1>Does LTDC support gray scale?</td><td rowspan=1 colspan=1>Yes, it is possible by using the L8 mode and using a correct CLUT (R=G=B).</td></tr><tr><td rowspan=1 colspan=2>Many factors can lead to a bad visual effect. The user can perform thefollowing checks:Check if the used display is correctly initialized / configured (somedisplays need an initialization / configuration sequence).Why is the display bad (displaying bad visual        Check if the LTDC timings and layer parameters are correctly set (seeeffects)?                                            example in Section 7.2.4)..    Display an image directly from the internal flash (see example inSection 7.2.5).Check if there is a nonsynchronization between the LTDC and theframebuffer update (by DMA2D or CPU), see Section 5.2.2.</td></tr></table>

# 10 Conclusion

ThU pyeitrole wwep ower cost and offering high performances.

Thakstrationar hitcureLTCuulyhherphicalat framebuffer and drives them to the display without any CPU intervention.

T LChalaivipy hiU is ideal for low-power and mobile applications such as smart watches.

This application note described the STM32 graphical capabilities and presented some considerations and recommendations to take fully advantage of the smart system architecture.

# Revision history

Table 26. Document revision history   

<table><tr><td rowspan=1 colspan=1>Date</td><td rowspan=1 colspan=1>Revision</td><td rowspan=1 colspan=1>Changes</td></tr><tr><td rowspan=1 colspan=1>10-Feb-2017</td><td rowspan=1 colspan=1>1</td><td rowspan=1 colspan=1>Initial release.</td></tr><tr><td rowspan=1 colspan=1>10-Feb-2017</td><td rowspan=1 colspan=1>2</td><td rowspan=1 colspan=1>Updated code on SDRAM and Quad-SPI MPU configuration example</td></tr><tr><td rowspan=1 colspan=1>10-Jul-2020</td><td rowspan=1 colspan=1>3</td><td rowspan=1 colspan=1>Updated:IntroductionProduct list extended in Table 1 and in the whole docTable 3: STM32 MCUs embedding an LTDC and their available graphic portfolioTable 10 and Table 11New Table 13 to Table 15Section 6.2.6: FMC SDRAM configurationFigure 52: FMC SDRAM MPU configuration exampleCode in SDRAM and Quad-SPI MPU configuration example</td></tr><tr><td rowspan=1 colspan=1>13-Mar-2023</td><td rowspan=1 colspan=1>4</td><td rowspan=1 colspan=1>Updated Section: Introduction and Section Table 1.: Applicable products to addSTM32U5 information.Updated the information in Section Table 15.: STM32L4P/Q maximal supported pixelclock.Edited the whole document to apply minor changes.Added Section Table 16.: STM32U59/A/F/G maximal supported pixel clock</td></tr><tr><td rowspan=1 colspan=1>08-Mar-2024</td><td rowspan=1 colspan=1>5</td><td rowspan=1 colspan=1>Added STM32H7Rx/7Sx linesUpdated document title</td></tr><tr><td rowspan=1 colspan=1>07-Feb-2025</td><td rowspan=1 colspan=1>6</td><td rowspan=1 colspan=1>Updated:Section IntroductionSection 3.2: LTDC and graphic portfolio across STM32 MCUsSection 3.3: LTDC in a smart architectureSection 5.2.2: Checking display compatibility considering the memory bandwidthrequirementsSection 5.3: STM32 package selection guide</td></tr></table>

# Contents

# 1 General information

2 Display and graphics overview.

2.1 Basic graphics concepts. 3   
2.2 Display interface standards 5   
2.3 Display interfaces supported by STM32 MCUs. 6

# Overview of LTDC controller and STM32 MCUs graphical portfolio 8

3.1 LCD-TFT display controller on STM32 MCUs . 8   
3.2 LTDC and graphic portfolio across STM32 MCUs .9   
3.3 LTDC in a smart architecture 11   
3.4 Advantages of using an STM32 LTDC controller 14

# LCD-TFT (LTDC) display controller description. 15

# 4.1 Functional description. 15

4.1.1 LTDC clock domains . 15   
4.1.2 LTDC reset 15

2 Flexible timings and hardware interface. 15

4.2.1 LCD-TFT pins and signal interface 16   
4.2.2 Fully programmable timings for different display sizes 17

# Two programmable LTDC layers. 19

4.3.1 Flexible window position and size configuration 20

4.3.2 Programmable layer: color framebuffer. 20

# 4.4 Interrupts 22

# 4.5 Low-power modes. 22

# Creating a graphical application with LTDC .24

5.1 Determining graphical application requirements 24

5.2 Checking the display size and color depth compatibility with the hardware configuration . .24

5.2.1 Framebuffer memory size requirements and location 24   
5.2.2 Checking display compatibility considering the memory bandwidth requirements . . 25   
5.2.3 Check the compatibility of the display panel interface with the LTDC 32

5.3 STM32 package selection guide . 32

# 5.4 LTDC synchronization with DMA2D and CPU. 33

5.4.1 DMA2D usage. 33   
5.4.2 LTDC and DMA2D/CPU synchronization 33

# Graphic performance optimization 34

5.5.1 Memory allocation. 34   
5.5.2 Optimizing the LTDC framebuffer fetching from external memories (SDRAM or SRAM) . . 35

5.5.3 Optimizing the LTDC framebuffer fetching from SDRAM. 38

5.5.4 Framebuffer content update during blanking period 39

Special recommendations for Cortex-M7 (STM32F7/H7) 39

5.6.1 Disable FMC Bank1 if not used. 39   
5.6.2 Configure the memory protection unit (MPU) 39

# 7 LTDC peripheral configuration. 41

5.7.1 Display panel connection 42   
5.7.2 LTDC clocks and timings configuration 43   
5.7.3 LTDC layers configuration. 44   
5.7.4 Display panel configuration 45

Storing graphic primitives. 45

5.8.1 Converting images to C files 45

3 Hardware considerations 45

# Saving power consumption .47

# LTDC application examples 48

# 7.1 Implementation examples and resources requirements. 48

7.1.1 Single-chip MCU. 48   
7.1.2 MCU with external memory . 48

7.2 Example: creating a basic graphical application 49

7.2.1 Hardware description 50   
7.2.2 How to check if a specific display size matches the hardware configuration .51   
7.2.3 LTDC GPIOs configuration 52   
7.2.4 LTDC peripheral configuration. 56   
7.2.5 Display an image from the internal flash 59   
7.2.6 FMC SDRAM configuration. . 63   
7.2.7 MPU and cache configuration . 64

7.3 Reference boards with LCD-TFT panel .66

# Supported display panels. 68

) Frequently asked questions. 69

10 Conclusion 70

Revision history 71

# _ist of tables 74

List of figures. .75

# List of tables

Table 1. Applicable products 1   
Table 2. . Display interfaces supported by STM32 MCUs. 6   
Table 3. STM32 MCUs embedding an LTDC and their available graphic portfolio 9   
Table 4. Advantages of using STM32 MCUs LTDC controller. 14   
Table 5. LTDC interface output signals 16   
Table 6. LTDC timing registers 17   
Table 7. LTDC interrupts summary 22   
Table 8. LTDC peripheral state versus STM32 low-power modes 23   
Table 9. Framebuffer size for different screen resolutions 24   
Table 10. STM32F4x9 maximal supported pixel clock. 28   
Table 11. STM32F7x6/7/8/9 maximal supported pixel clock . 29   
Table 12. STM32H742/43/45/47/53/55/57 and STM32H750 maximal supported pixel clock . 29   
Table 13. STM32H7R7/7S7 maximal supported pixel clock 30   
Table 14. STM32H7A3/B3 and STM32H7B0 maximal supported pixel clock 30   
Table 15. STM32L4+ maximal supported pixel clock. 30   
Table 16. STM32L4P/Q maximal supported pixel clock . 31   
Table 17. STM32U59/A/F/G maximal supported pixel clock . 31   
Table 18. STM32N6x5/6x7 maximal supported pixel clock. 31   
Table 19. Example of supported display resolutions in specific STM32 hardware configurations. 32   
Table 20. STM32 packages with LTDC peripheral versus RGB interface availability 33   
Table 21. LCD-TFT timings extracted from ROCKTECH RK043FN48H datasheet 43   
Table 22. Programming LTDC timing registers . 44   
Table 23. Example of graphic implantations with STM32 in different hardware configurations. 49   
Table 24. STM32 reference boards embedding LTDC and featuring an on-board LCD-TFT panel. 67   
Table 25. Frequently asked questions. 69   
Table 26. Document revision history . 71

# List of figures

Figure 1. Basic embedded graphic system. . 3   
Figure 2. Display module with embedded controller and GRAM 4   
Figure 3. Display module without controller nor GRAM 4   
Figure 4. Display module without controller nor GRAM and with external framebuffer 4   
Figure 5. MIPI-DBI type A or B interface 5   
Figure 6. MIPI-DBI type C interface. 5   
Figure 7. MIPI-DPI interface. 6   
Figure 8. MIPI-DSI interface. 6   
Figure 9. LTDC AHB master in STM32F429/439 and STM32F469/479 smart architecture . . 11   
Figure 10. LTDC AHB master in STM32F7x6, STM32F7x7, STM32F7x8, and STM32F7x9 smart architecture . 12   
Figure 11. LTDC AXI master in STM32H7Rx/7Sx . 13   
Figure 12. LTDC block diagram 15   
Figure 13. LTDC signal interface 16   
Figure 14. Typical LTDC display frame (active width = 480 pixels) 17   
Figure 15. Fully programmable timings and resolutions . 18   
Figure 16. LTCu poableispay olutn wih toal widh u 9 pielnd tota height u  08   
Figure 17. Blending two layers with a background 19   
Figure 18. Layer window programmable size and position 20   
Figure 19. Pixel data mapping versus color format 21   
Figure 20. Programmable color layer in framebuffer 21   
Figure 21. Pixel format conversion from RGB565 input pixel format to the internal ARGB8888 format . 22   
Figure 22. AHB masters concurrent access to SDRAM . 26   
Figure 23. Typical graphic hardware configuration with external SDRAM. 28   
Figure 24. Double buffering: synchronizing LTDC with DMA2D or CPU 34   
Figure 25. Example of taking advantage from memory slaves split on STM32F4x9. 34   
Figure 26. Burst access crossing the 1-Kbyte boundary 35   
Figure 27. Reducing layer window and framebuffer line widths. 36   
Figure 28. Adding dummy bytes to make the line width multiple of 64 bytes. 38   
Figure 29. Placing the two buffers in independent SDRAM banks. 38   
Figure 30. FMC SDRAM and NOR/PSRAM memory swap at default system memory map (MPU disabled) 40   
Figure 31. Connecting an RGB666 display panel . . 42   
Figure 32. Low-end graphic implementation example 48   
Figure 33. High-end graphic implementation example. 49   
Figure 34. Graphic hardware configuration in the STM32F746G-DISCO 50   
Figure 35. LCD-TFT connection in the STM32F746G-DISCO board 50   
Figure 36. Backlight controller module 51   
Figure 37. STM32CubeMX: LTDC GPIOs configuration. 52   
Figure 38. STM32CubeMX: PJ7 pin configuration to LTDC_G0 alternate function. 53   
Figure 39. STM32CubeMX: LTDC configuration . 53   
Figure 40. STM32CubeMX: LTDC GPIOs output speed configuration . 54   
Figure 41. STM32CubeMX: display enable pin (LCD_DISP) configuration 54   
Figure 42. STM32CubeMX: setting LCD_DISP pin output level to high 55   
Figure 43. STM32CubeMX: enabling LTDC global and error interrupts 56   
Figure 44. STM32CubeMX: clock configuration tab. . 57   
Figure 45. STM32CubeMX: System clock configuration 57   
Figure 46. STM32CubeMX: LTDC pixel clock configuration 57   
Figure 47. STM32CubeMX: LTDC timing configuration 58   
Figure 48. STM32CubeMX: LTDC Layer1 parameters setting 59   
Figure 49. LCD-Image-Converter: home page 60   
Figure 50. LCD-Image-Converter: image project 61   
Figure 51. LCD-Image-Converter: setting conversion options. 62   
Figure 52. LCD-Image-Converter: generating the header file 62   
Figure 53. FMC SDRAM MPU configuration example 64

Figure 54. MPU configuration for Quad-SPI region . 65

# IMPORTANT NOTICE  READ CAREFULLY

pt old ursant  dits   leole.

purchasers' products.

No license, express or implied, to any intellectual property right is granted by ST herein.

are the property of their respective owners.

I

© 2025 STMicroelectronics - All rights reserved