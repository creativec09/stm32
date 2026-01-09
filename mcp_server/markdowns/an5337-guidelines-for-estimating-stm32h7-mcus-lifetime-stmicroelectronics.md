# Guidelines for estimating STM32H7 MCUs lifetime

# Introduction

o junction temperature (Tj).

product.

Table 1. Applicable products   

<table><tr><td>Type</td><td>Product lines</td></tr><tr><td>Microcontrollers</td><td>STM32H742, STM32H743/753, STM32H745/755, STM32H747/757, STM32H750 Value line STM32H723/733, STM32H725/735, STM32H730 Value line</td></tr></table>

# 1 General information

# Note:

Th document presents theT32seris lifetime usage estimation. These estimates are qualified dependin on frequencies, voltage, and junction temperature.   
The frequencies and applied voltages are provided in the device datasheets.   
The STM32H7 series microcontrollers are Arm®-based devices.   
Arm is a registered trademark of Arm Limited (or its subsidiaries) in the US and/or elsewhere.

# arm

# 2 STM32H7 series lifetime usage estimation

Thi section presents data nd ables representing he lfetime usageestmation or32 ser devi typical use conditions.

Table 2. STM32H7 series lifetime usage estimation for typical use conditions   

<table><tr><td rowspan=1 colspan=1>•</td><td rowspan=1 colspan=1>Lifetimeyears)</td><td rowspan=1 colspan=1>Operating ratio(%)</td><td rowspan=1 colspan=1>VDD nominal(V)</td><td rowspan=1 colspan=1>VCORE nominal¯(V)</td><td rowspan=1 colspan=1>Junctiontemperature (TJ)(</td></tr><tr><td rowspan=1 colspan=1>VOSO(1)</td><td rowspan=1 colspan=1>10</td><td rowspan=1 colspan=1>20</td><td rowspan=1 colspan=1>3.3</td><td rowspan=1 colspan=1>1.35</td><td rowspan=1 colspan=1>105</td></tr><tr><td rowspan=1 colspan=1>VOS1(2)</td><td rowspan=1 colspan=1>10</td><td rowspan=1 colspan=1>20</td><td rowspan=1 colspan=1>3.3</td><td rowspan=1 colspan=1>1.2</td><td rowspan=1 colspan=1>140(3)</td></tr><tr><td rowspan=1 colspan=1>VOS2 - VOS3</td><td rowspan=1 colspan=1>10</td><td rowspan=1 colspan=1>100</td><td rowspan=1 colspan=1>3.3</td><td rowspan=1 colspan=1>&lt;1.10</td><td rowspan=1 colspan=1>140(3)</td></tr></table>

Not applicable for STM32H757xxxxA.   
Max CPU1 frequency of 480 MHz and max CPU2 frequency of 240 MHz is achievable with VOS1 only for STM32H757xxxxA.   
3. T atuot     arers lusiv prrR product datasheet for more details.

![](images/38d6f5e4f0a454b7ee272481f1c43b6c05f988a2df8cc72a64ba6ed138b044ee.jpg)  
Figure 1. Lifetime estimation VOS0

According to Figure 1, when VOS0, VDD = 3.3 V, VcORE = 1.35 V and operation ratio 100%. Some examples are illustrated such as:

Tj = 105°C the lifetime estimation is 2 years Tj = 95°C the lifetime estimation is 3.5 years

In the same conditions and for an operation ratio of 20%, the lifetime estimation is as following:

Tj = 105°C the lifetime estimation is 10 years

Tj = 95°C the lifetime estimation is 17.5 years

![](images/9583b3980db29347c9fbcbecd9a4f92f0d88d1dabcc882887bffc262d87dd0f1.jpg)  
Figure 2. Lifetime estimation VOS1

According to Figure 2, when VOS1, VDD = 3.3 V, VcORE = 1.2 V and operation ratio of 100%. Some examples are illustrated such as:

Tj = 105°C the lifetime estimation is > 10 years Tj = 125°C the lifetime estimation is 4 years Tj = 140°C the lifetime estimation is 2 years

In ts n  aion a % e itaton  :

Tj = 125°C the lifetime estimation is 20 years Tj = 140°C the lifetime estimation is 10 years

![](images/8da24923c35a0fdcb9b4de95b6c933e46630b509c1d38902e7f561ce0404ea3d.jpg)  
Figure 3. Lifetime estimation VOS2 and VOS3

According to Figure 3, when VOS2 or VOS3, VDD = 3.3 V, VcORE < 1.10 V and operation ratio 100%. Some examples are illustrated such as:

Tj = 125°C the lifetime estimation is > 20 years Tj = 130°C the lifetime estimation is 16 years Tj = 140°C the lifetime estimation is 10 years

Not:For more inormation about the suff 3 or , reer  the product datasheet available n wwwt.com.

# Revision history

Table 3. Document revision history   

<table><tr><td>Date</td><td>Version</td><td>Changes</td></tr><tr><td>19-Jun-2019</td><td>1</td><td>Initial release.</td></tr><tr><td rowspan="2">03-Jul-2020</td><td rowspan="2">2</td><td>Added STM32H723, STM32H733, STM32H725, STM32H735, and STM32H730 part numbers.</td></tr><tr><td>Removed all the tables providing frequencies versus voltage scaling and temperature ranges for all product series.</td></tr><tr><td rowspan="2">18-Apr-2024</td><td rowspan="2">3</td><td>Updated: •</td></tr><tr><td>Document title Section 2: STM32H7 series lifetime usage estimation</td></tr></table>

# Contents

1 General information   
2 STM32H7 series lifetime usage estimation   
Revision history   
List of tables 8 List of figures.

# List of tables

Table 1. Applicable products Table 2. STM32H7 series lifetime usage estimation for typical use conditions 3 Table 3. Document revision history . 6

# List of figures

Figure 1. Lifetime estimation VOSO. 3   
Figure 2. Lifetime estimation VOS1. 4   
Figure 3. Lifetime estimation VOS2 and VOS3 5

# IMPORTANT NOTICE  READ CAREFULLY

pt old ursant  dits   leole.

purchasers' products.

No license, express or implied, to any intellectual property right is granted by ST herein.

are the property of their respective owners.

I

© 2024 STMicroelectronics - All rights reserved