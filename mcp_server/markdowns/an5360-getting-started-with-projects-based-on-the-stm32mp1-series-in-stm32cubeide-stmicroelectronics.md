# Getting started with projects based on the STM32MP1 Series in STM32CubeIDE

# Introduction

Th apliion oecies how  ar wi pro bas2Sile STM32CubeIDE integrated development environment.

# General information

# Note:

STM32CubeIDE supports STM32 32-bit products based on the Arm® Cortex® processor.   
Arm is a registered trademark of Arm Limited (or its subsidiaries) in the US and/or elsewhere.

# 1.1

# Prerequisites

The following tools are prerequisites for understanding the tutorial in this document and developping an application based on the STM32MP1 Series:

STM32CubeIDE 1.1.0 or newer STM32Cube_FW_MP 1.1.0 or newer STM32CubeMX 5.4.0 or newer

Users aeadvie  keeupdated with heocentatin evoluionf the32PSer t .om/ microcontrollers-microprocessors/stm32mp1-series.

# The use cases in this document

In the STM32CubelDE context, users have different ways to explore and get started with the development of basnSrohe beloweleche est hat bes h considered and refer to the corresponding section in this application note:

• I already have an SW4STM32 project with an ioc file: Refer to Section 2.2 Import an SW4STM32 project with an ioc file   
• I already have an SW4STM32 project without an ioc file: Refer to Section 2.3 Import an SW4STM32 project without an ioc file   
• I want to learn with and explore example projects: Refer to Section 2.5 Import a project from the STM32CubeMP1 MCU Package

I want to start a first STM32MP1 project:

Empty project - No STM32CubeMX support for maximum flexibility.   
Refer to Section 2.4 Create an empty project based on the template in the STM32CubeMP1 MCU Package   
STM32CubeMP1 project - STM32CubeMX-managed project.   
Refer to Section 2.1 Create a new STM32 project

# Specific features of the STM32MP1 Series

The wayhe targebot poran. Boot pins r et byheusern Mieon boar byens ofswitches. For the STM32MP157C-V1 Evaluation board, related information is provided in the Boot options secion f the user manual (UM2535). Mor enerally, information isals available from TMicroelectroni MPU wiki at wiki.st.com/stm32mpu in the Boot related switches section of the board being used.

Two boot modes are considered:

Production boot mode: Linux® usually boots on an SD card, but is also capable to boot through an onboard NAND or NOR. The Cortex®-M4 e1f is downloaded through the network and loaded by the OpenAMP framework. It is possible to debug the application via JTAG/SWD by attaching to a runing target. Engineering boot mode: The Cortex®-A7 is effectively disabled and the application is downloaded directly to the Cortex®M4 through JTAG/SWD. Using this mode, the application is debugged like for any standard Cortex®-M4 device.

Aditional consequences of the choice between production and engineering modes are dealt with further in Section 3.1 Debug modes and Section 3.2 Target status.

# 1.3.1

# STM32MP1 project structure

Wh pr cuaally aie o theusercreates  ports n 32 project, t consistse root project together with su-projects referred to as MCU projects, for each core. A hierarchical structure example is shown in Figure 1.

![](images/5dcda49c30ace41647578ea1eea53247adcc313820829644baf342c226bbcf30.jpg)  
Figure 1. Hierarchical project structure

To o ealloa eo o cnai eiterbuild ordeb cnuratis.However, heMC projec l  proe hat both build and debug configurations.

If the project is not shown in a hierarchical structure, this can be changed as shown in Figure 2.

![](images/743d423d86b86b881fe6383b57d51c9709eb13fbf364e1701109277519a4ac30.jpg)  
Figure 2. Setting the project hierarchical view

# 2 Create and import projects

# 2.1

This chapter describes how to create or import projects for the STM32MP1 Series.

# Create a new STM32 project

To start a new project, go to [File]>[New]>[STM32 Project] as shown in Figure 3.

Figure 3. New STM32 project   

<table><tr><td>IDE workspace - STM32CubeIDE</td><td colspan="4"></td></tr><tr><td>File</td><td colspan="3">Edit Source Refactor Navigate Search Project Run Window Help</td><td colspan="2"></td></tr><tr><td rowspan="7">0</td><td>New</td><td>Alt+Shift+N &gt;</td><td></td><td>Makefile Project with Existing Code</td></tr><tr><td>Open File...</td><td></td><td>C/C++ Project</td><td></td></tr><tr><td>Open Projects from File System..</td><td></td><td>ESTM32 Project Project...</td><td></td></tr><tr><td>Recent Files Close</td><td>&gt;</td><td>C++</td><td></td></tr><tr><td>Close All</td><td>Ctrl+W</td><td>Source Folder</td><td>Convert to a C/C++ Project (Adds C/C++ Nature)</td></tr><tr><td></td><td>Ctrl+Shift+W</td><td>Folder</td><td></td></tr><tr><td></td><td>Ctrl+S</td><td>Source File</td><td></td></tr><tr><td rowspan="4">Save 8 B Save As... Revert</td><td></td><td></td><td></td><td></td></tr><tr><td>Save All</td><td>Ctrl+Shift+S</td><td></td><td>Header File</td></tr><tr><td></td><td></td><td>Class</td><td>File from Template</td></tr><tr><td></td><td>C</td><td>Other...</td><td>Ctrl+N</td></tr></table>

Select the desired MCU or board. In the example illustrated in Figure 4, the selected board is the STM32MP157C-EV1. Click on [Next >].

STM32 Project

# Target Selection

![](images/2b69fc1e6e54ca9bbce4d02451f5724b59e175505a0d9b04431e113e0a9a6711.jpg)  
Figure 4. Target selection

Select STM32 target

Ate the target selection comes he project setu teshown nFigure TheTargeted rojec Typett determines whether the project gets generated by STM32CubeMX or not. An Empty project is a skeleton of a project that needs building upon while STM32Cube indicates an STM32CubeMX-managed project.

![](images/0afb174387f0c9fc4e81f6916a23affd3f941601938ab9ead20f1a41c8972e50.jpg)  
Figure 5. Projet setup

# 2.2

# Import an SW4STM32 project with an ioc file

I  proj rea cntaisn easst way ort he project int workg2C evioment is to copy it and open the copy trough32Cube stan alone, then, inhe Projec Mae, change the Toolchain / IDE to STM32CubeIDE and regenerate the project.

Aft the projec is geeate go o [File>[ort.]an choo tmport  as  Existi proje workspace as shown in Figure 6.

![](images/2055a8d1281b9386643186e5a8cf8922e64dbbc89367451c59252202cdea98b4.jpg)  
Figure 6. Import an existing projet with an ioc file   
Figure 7. New STM32 project

Th he n he f //lo ha i in he TM32CubeIDE environment.

# 2.3

# Import an SW4STM32 project without an ioc file

make ure he projec get a hiarchil ucture, he eoende way s o go o [ile]ew][2 Project] as shown in Figure 7.

<table><tr><td colspan="5">IDE workspace - STM32CubeIDE</td></tr><tr><td>File</td><td>Edit Source Refactor Navigate Search Project Run Window Help</td><td></td><td></td><td></td></tr><tr><td></td><td>New</td><td>Alt+Shift+N &gt;</td><td></td><td>Makefile Project with Existing Code</td></tr><tr><td>0</td><td>Open File...</td><td></td><td>C/C++ Project IDE</td><td></td></tr><tr><td></td><td>Open Projects from File System...</td><td></td><td>STM32 Project </td><td></td></tr><tr><td></td><td>Recent Files</td><td>&gt;</td><td>Project....</td><td></td></tr><tr><td></td><td>Close</td><td>Ctrl+W</td><td>Ca Source Folder</td><td>Convert to a C/C++ Project (Adds C/C++ Nature)</td></tr><tr><td></td><td>Close All</td><td>Ctrl+Shift+W</td><td>Folder</td><td></td></tr><tr><td>8 Save</td><td></td><td>Ctrl+S</td><td></td><td></td></tr><tr><td></td><td>Save As...</td><td></td><td>Source File</td><td></td></tr><tr><td>G</td><td></td><td>Ctrl+Shift+S</td><td>Header File </td><td></td></tr><tr><td>Revert</td><td>Save All</td><td></td><td>C Class</td><td>File from Template</td></tr><tr><td></td><td></td><td></td><td>¤</td><td></td></tr><tr><td></td><td>Move...</td><td></td><td>Other..</td><td>Ctrl+N</td></tr></table>

Select the device for the project being imported and click on [Next >].

W   o on [Finish].

![](images/0d398603a92ac8d52d14dd81cf4f98ddf864738122ad0a1cda2078560347b6e5.jpg)  
Figure 8. Projet setup

After the empty hierarchical project is generated:

1. Go to [File ]>[Import...]   
2. Import the SW4STM32 project as Import ac6 System Workbench for STM32 Project   
3. Copy and paste the project content into the sub-project of the empty project by means of SM32CubelDE project explorer as shown in Figure 9

![](images/3af02fbc1c9544c8b82fc3489721491f7b4375193cf95d2b77e0e51cf7eb0a8a.jpg)  
Figure 9. Copy project content to empty sub- project

# Note:

It is not recommended to import the . cproject, .project or .settings files.

It intuett wpy wh w e vent e rojntkr hoseee edat the correct resource in the file system.

This process is necessary because when importing a project from SW4STM32 without any special treatment and that does not have an oc-file then it will be mported intoSTM32CubelDE with a flat project strucure.

# 2.4

# Create an empty project based on the template in the STM32CubeMP1 MCU Package

Follow the same steps as in Section2.3 but use STM32CubeFW_MP firmware in the STM32CubeMP1 MCU Package as input.

# 2.5

# Import a project from the STM32CubeMP1 MCU Package

Inore ort he M32Cue  projec nt 32CubeDE, o [ile[prt] and elec ac6 System Workbench for STM32 Project as shown in Figure 10 and click on [Next >].

![](images/8c2bb64c6b3df33b1e9ad3f86176dc003801e714641c393d7b3ad1d5a020802c.jpg)  
Figure 10. Import of firmware project info STM32CubelDE

Then select the correct project. A project example is by default located at \$\32CubReST M32Cube_FW_MPl_VX.X.X\Projects\STM32MP157C-EV1\Examples\ADC\ADC_SingleConversion_Tr iggerTimer_DMA\SW4STM32\ADC_SingleConversion_TriggerTimer_DMA.

![](images/caeee97ab35c685032d49489dc75115883d160a172b59ea60835289c667ac2b7.jpg)  
Figure 11. Firmware project selection

After selecting the project, click on [Finish] to import and build the project.

# 3 Debugging

# 3.1

This chapter highlights some of the points to bear in mind while debugging a device in the STM32MP Series.

# Debug modes

There are two modes or debugging a device in the TM32PSeri, the production mode and the engineerig mode.

# Production mode

T ak e P l lore® Iak l re® havr®l s following points into consideration:

To enable the production mode, the switcheson he board must be t correctl Consult Microelectronic MPU wiki at wiki.st.com/stm32mpu in the Boot related switches section of the board being used. For the STM32MP157C-EV1 Evaluation board, related information is provided in the Boot options section of the user manual (UM2535).

Firmware is downloaded to the embedded Linux® file system and then uploaded to the Cortex®M4 through the remoeprframework. Due to the fact that the Cortex®-M4 core is started by Linux®, there is o way the application startup phase s require,e possibility is tomodify the startup codeof he Corte®M4 aplaion hava busy-wait lop baseon a regisevalead thenmanuall eeleaseva the register through the debug session to release the Cortex®-M4.

• The target nees to be conneed to a network and Linux® must berunig Make sure that he status liht is green and an IP address is presented to know that the connection is up and running (refer to Section 3.2 ).

• In this mode, the Cortex®-A7 Linux® core gives commands to the Cortex®-M4.

# Engineering mode

To enable the engineering mode, the switches on the board must be set correctly. Consult STMicroelectronics MPU wiki at wiki.st.com/stm32mpu in the Boot related switches section of the board being used. For the STM32MP157C-EV1 Evaluation board, related information is provided in the Boot options section of the user manual (UM2535).

The Cortex®-A7 goes into a loop and the Cortex®-M4 is debugged as a regular STM32 device, where the application is loaded using the debugger connection.

# 3.2 Target status

In the production mode a status light in he bottm ight f he TM32CubelDE window provides inforatin regarding the current status of the connection between the computer and the embedded Linux® system.

# Note:

T t from the view.

The various values of the target status light are presented in Table 1.

Table 1. Target status light   

<table><tr><td rowspan=1 colspan=1>Status light</td><td rowspan=1 colspan=1>Icon</td><td rowspan=1 colspan=1>Description</td></tr><tr><td rowspan=1 colspan=1>Black</td><td rowspan=1 colspan=1>Stopped             •</td><td rowspan=1 colspan=1>The light completely off means that the widget is disabled.</td></tr><tr><td rowspan=1 colspan=1>Red</td><td rowspan=1 colspan=1>Status: offline        0</td><td rowspan=1 colspan=1>STM32CubelDE cannot establish contact and cannot detect any target.</td></tr><tr><td rowspan=1 colspan=1>Yellow</td><td rowspan=1 colspan=1>Serial console in use0</td><td rowspan=1 colspan=1>Indicates a dysfunction such as:1.   No network connection between the computer and the MPU.2.  The consoled is opened.</td></tr><tr><td rowspan=1 colspan=1>Green</td><td rowspan=1 colspan=1>Status: idle</td><td rowspan=1 colspan=1>The connection is up and running.</td></tr></table>

# 3.3

# Serial console

To open the serial console, click on this icon:

A vh activgUsm Explorer perspective, a second connection to the target can be made over SSH. When the serial console is with the Target Widget Status when it needs to refresh the IP address of the target.

# Revision history

Table 2. Document revision history   

<table><tr><td>Date</td><td>Version</td><td>Changes</td></tr><tr><td>29-Oct-2019</td><td>1</td><td>Initial release.</td></tr></table>

# Contents

# 1 General information

1.1 Prerequisites 1.2 The use cases in this document 1.3 Specific features of the STM32MP1 Series . 1.3.1 STM32MP1 project structure.

# Create and import projects. 5

2.1 Create a new STM32 project . 5   
2.2 Import an SW4STM32 project with an ioc file . .   
2.3 Import an SW4STM32 project without an ioc file 8   
2.4 Create an empty project based on the template in the STM32CubeMP1 MCU Package . . 10   
2.5 Import a project from the STM32CubeMP1 MCU Package . 10

# Debugging 13

3.1 Debug modes 13   
3.2 Target status 13   
3.3 Serial console 14

# Revision history 15

# Contents .16

# _ist of tables 17

# List of figures. .18

# List of tables

Table 1. Target status light. 14   
Table 2. Document revision history . 15

# List of figures

Figure 1. Hierarchical project structure 3   
Figure 2. Setting the project hierarchical view. 4   
Figure 3. New STM32 project. 5   
Figure 4. Target selection 6   
Figure 5. Projet setup 7   
Figure 6. Import an existing projet with an ioc file 8   
Figure 7. New STM32 project. 8   
Figure 8. Projet setup . 9   
Figure 9. Copy project content to empty sub- project.. 10   
Figure 10. Import of firmware project info STM32CubeIDE. 11   
Figure 11. Firmware project selection 12

# IMPORTANT NOTICE - PLEASE READ CAREFULLY

ol uant   .

Purchasers' products.

No license, express or implied, to any intellectual property right is granted by ST herein.

names are the property of their respective owners.

I