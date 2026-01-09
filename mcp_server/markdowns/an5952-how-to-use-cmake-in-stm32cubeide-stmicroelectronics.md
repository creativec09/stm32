# How to use CMake in STM32CubeIDE

# Introduction

the STMicroelectronics STM32CubeIDE integrated development environment.

# 1 General information

# Note:

STM32CubelDE supports STM32 32-bit products based on the Arm® Cortex® processor.   
Arm is a registered trademark of Arm Limited (or its subsidiaries) in the US and/or elsewhere.

arm

# 1.1

# Purpose

ST32CubeDE offers the user-requested CMake feature, which developers can leverage or ther developments in the STM32 MPU and MCU ecosystems.

# The use cases in this document

In the STM32CubelDE context, a user can compile C/C++ projects using either the makefile or the CMake solutions. This document details the use of CMake for two use cases:

The user wants to work with an existing CMake project structure The user wants to start a CMake development from scratch

# 1.3

# Compatible toolchair

The STM32CubelDE CMake support presented in this application note works with the following minimum version of the toolchain:

STMicroelectronics STM32CubeIDE v1.13.0

# 1.4

# Prerequisites

CMake must be installed on the user's computer. The compatibility with STM32CubelDE is from CMakev3.13 onwards.

# 2 Create projects

# 2.1

# Creation with an existing CMake project structure

Cratig a new project wit an existig CMake structureoffers an easy way to use an already developedor lownloaded project or library for use in STM32CubelDE. To do so, start by following the steps below:

Select [File]>[New]>[STM32 CMake Project]

![](images/a9b8f498d54ccda0c971004dda8e3e2d2b6a7232d8f6f963967d33d55b6d90b9.jpg)  
Figure 1. CMake project creation

# Select [Project with existing CMake sources]

![](images/09b3d84b74dda9627c3fbceaff5f90f6fee6301375689043afccd265f6cb880a.jpg)  
Figure 2. CMake project types

# Select [Next >]

The next wizard page allows the setup of a CMake project in two different ways:

Project creation inside an existing CMake project structure (refer to Section 2.1.2 Project creation external to an existing CMake project structure (refer to Section 2.1.3)

# 2.1.1

# CMake project as a subproject

Aaivea pe o context menu option.

![](images/d16ef47bc23883ba45588a129d862459c616a0cd737a5a7509b7065bffd59d66.jpg)  
Figure 3. CMake project as a subproject

# 2.1.2

# Creation inside an existing CMake project structure

Tocreate a new project inside an existing package hat was already downladed or created, do the following:

Specify a name for the project.   
Uncheck [Use default location].   
Use the [Browse..] button and select the root directory of a CMake-based project. This disables the [Source directory] field since the project location and the CMake source directory are the same.   
is config_default relative to the CMake source directory.

![](images/3c504a9ce0bf31d2e83c1c7f9a9ce56358a19f1628cda9663de093c3a7086982.jpg)  
Figure 4. Project creation inside an existing CMake project structure

# 2.1.3

# Creation external to an existing CMake project structure

project structure to link the existing package from the source directory to the project.

Specify a name for the project.   
Specify an empty directory for the project. Keep [Use default location] checked so that the project is created inside the current workspace directory.   
Use the [Browse.] button and select the root directory of a CMake-based project. The selected diectory is linked into the project.   
p auauleui igdefaurelative to the CMake source direcory.

![](images/2b365be963ea501bdbc85a555f719c108ecc222c3b6ccf03a8af06022cfdaea0.jpg)  
Figure 5. Project creation external to an existing CMake project structure

# Click on [Next >].

Text wiz peallows ecguration dealt tolchaanlevantinsre To eantil Mak po cu ut m u information for certain of its features to function properly.

# Fill in:

The information about the MCU and core for the debugger   
The proper indexing, for instance for code completion   
The selected toolchain, which is added to the PATH variable when building the project

![](images/3e3e8004e62d790ae901066c4e258aac68a31623cdeb6f78f7860158ec3658c1.jpg)  
Figure 6. CMake default toolchain

# Select [Finish]

t this stage, the project is created and visible in the Project Explorer view

# Starting CMake project development from scratch

SCubeElo he possblcat n u pousak pr the steps below:

Select [File]> [New]>[STM32 CMake Project]

![](images/a1a18168d1c6d1273c1b8b4a021dd4dacf315309123911e64458b510d000afa1.jpg)  
Figure 7. CMake project creation (alt.)

# Select [Project from CMake template]

![](images/5c0a9925589eeb92dc78eed73246835262a31649b5c4ceaa8830ee321c784f63.jpg)  
Figure 8. CMake project types (alt.)

Provide the information requested for the project creation:

Specify a name for the project.   
Speiy an empty directory or the project. Keep [Use default location] checked so that the project is created inside the current workspace directory.   
Select the template to use for the project. Currently, the templates for "Executable" and "Static Library" targeting the "MCU ARM GCC toolchain" are available.

![](images/a5db389b30b55b7ca05e1d021058dd173646a9d003d214e924cf21bdb5c403cb.jpg)  
Figure 9. CMake project from template

# Click on [Next >]

Thenet wizr peallows he cguraion  deault tolchai nelevant tinsr oroject.

Select the options for the STM32 device to be used for the new project

![](images/506864929599f5c74fd11236fffbc51b9bf2931c9555ff0633a3eb0d18dbd384.jpg)  
Figure 10. CMake default toolchain (alt.)

# Click on [Finish]

# 3 Configure and build

# 3.1 CMake build settings

The CMake-related build settings can be specified in the project properties

Select C/C++ Build available in the project properties.   
Select the CMake Settings tab.   
Select the build system in [Generator]: "Unix Makefiles" "Ninja"

Speiy the initial values or the CMake configuration step in [Other Options]. The example presente in Figure 11 is for configuring the amazon-freertos CMake package for the B-L475E-IOT01A STM32 Discovery kit.

![](images/0d0cdb1b762631997010e7985a23b57aed839e3085c7306284fbef7085aa4ea3.jpg)  
Figure 11. CMake build options (Generator)

# Select the [CMake build type]:

Empty (default value)   
"Debug"   
"Release"   
"RelWithDebugInfo" (release with debug information)   
"MinSizeRel" (minimum size release)

![](images/dfb67c48b563d40ffec714862cfa5398829b8c967b2e2f01422fb03fce26a577.jpg)  
Figure 12. CMake build options (CMake build type)

Configure the parameters as shown in Figure 3, when working with CMake projects in STM32CubelDE, to mitigate indexer issues resulting from CDT™ limitations.

![](images/6bea2dc252004d31ec58c884d10def0b2983e6454848ceb95d0a4f698ea31ad3.jpg)  
Figure 13. Compilation database parser

# 3.2

# Building a CMake-based project

For ake-as proje, e IDE build configurationmanagementanuserinterfaces a milartho non-CMake-based projects, including:

Menus Toolbars Buttons

ult o uts  tt "Debug" and "Release".

![](images/3bf7a39fe9eea8736bf48bb3bb4adb253cbf792b15a4537ced3e45d38c74c5b2.jpg)  
Figure 14. CMake project manual build

During the first project build, the IDE automatically performs:

The CMake configure step   
The setup of the CMake cache   
The build files generation into the specified build directory

Any subsequent build is performed in the build directory using the existing CMake cache.

# 3.3

# CMake manual configure step

The CMake configure step and build files generation can also be performed manually from:

Either the project context menu

![](images/700bfec1f449bb055880581b549e88679dde39e4d9d3057f5abfe4db2f110500.jpg)  
Figure 15. CMake project context menu

# Or the Project menu

![](images/9b7fe70ae20a4bd533081355c3f4c3072ae5f35edb86bc5009799abf79231f06.jpg)  
Figure 16. CMake project menu

# Revision history

Table 1. Document revision history   

<table><tr><td rowspan=1 colspan=1>Date</td><td rowspan=1 colspan=1>Revision</td><td rowspan=1 colspan=1>Changes</td></tr><tr><td rowspan=1 colspan=1>07-Jul-2023</td><td rowspan=1 colspan=1>1</td><td rowspan=1 colspan=1>Initial release.</td></tr><tr><td rowspan=1 colspan=1>19-Feb-2025</td><td rowspan=1 colspan=1>2</td><td rowspan=1 colspan=1>Updated Section 3.1: CMake build settings:Updated Figure 11. CMake build options (Generator)Added Figure 12. CMake build options (CMake build type) andFigure 13. Compilation database parser</td></tr></table>

# Contents

# 1 General information

1.1 Purpose 2   
1.2 The use cases in this document   
1.3 Compatible toolchain   
1.4 Prerequisites

# Create projects

# 2.1 Creation with an existing CMake project structure 3

2.1.1 CMake project as a subproject 4 2.1.2 Creation inside an existing CMake project structure . 5 2.1.3 Creation external to an existing CMake project structure 6 2.2 Starting CMake project development from scratch.

# Configure and build. 11

3.1 CMake build settings 11   
3.2 Building a CMake-based project. 14   
3.3 CMake manual configure step. 15

# Revision history 17

List of figures. . 19

# List of figures

Figure 1. CMake project creation 3   
Figure 2. CMake project types 3   
Figure 3. CMake project as a subproject. 4   
Figure 4. Project creation inside an existing CMake project structure. 5   
Figure 5. Project creation external to an existing CMake project structure 6   
Figure 6. CMake default toolchain 7   
Figure 7. CMake project creation (alt.). 7   
Figure 8. CMake project types (alt.. 8   
Figure 9. CMake project from template .9   
Figure 10. CMake default toolchain (alt.). 10   
Figure 11. CMake build options (Generator) 11   
Figure 12. CMake build options (CMake build type) 12   
Figure 13. Compilation database parser 13   
Figure 14. CMake project manual build . 14   
Figure 15. CMake project context menu 15   
Figure 16. CMake project menu. 16

# IMPORTANT NOTICE  READ CAREFULLY

pt old ursant  dits   leole.

purchasers' products.

No license, express or implied, to any intellectual property right is granted by ST herein.

are the property of their respective owners.

I

© 2025 STMicroelectronics - All rights reserved