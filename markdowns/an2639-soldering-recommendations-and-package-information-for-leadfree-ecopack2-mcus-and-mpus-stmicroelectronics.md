# Soldering recommendations and package information for lead-free ECOPACK2 MCUs and MPUs

# Introduction

S CUMPUrOPAC cks. TB varu packageyesuseiroduceseifrnmontignologiangivsolderinecoenatis.

# 1 Lead-free packages at STMicroelectronics

STMicroelectronicsisfully committed toenvironment protection and sustainabledevelopment and started in1997 avoluntary program or removing polluting andhazardous ubstancesfrom ll devices. In 000, a strategic program, named ECOPACK2 has been officially launched to develop and implement solutions leading to envromentindly packaging nd ban progressively lead andotherheavymetals rom urmanufacturiines. ECOPACK2 is a registered trademark of STMicroelectronics.

STMicroelectronics ECOPACK2 products are RoHS compliant according to EU 2011/65/EU directive.

For more detailed information, go to https://www.st.com.

# Note:

RoH stands or "Restriction o theuse of certain hazardous substances". It is specified by theditive 201/65/EU of the European Parliment and of the Council of 8h June 2011 on the restriction of the use caiazardou substance nelecrical  electrnquentThis dectivs therecas heRoH Drective2002/95/ECof the Eropean Parliment and of theCouncl of 7th January 2003 on theRestricn the use of certain Hazardous Substances in Electrical and Electronic Equipment.

# 2 Packages overview

The different packages available at STMicroelectronics are described in Table 1.

Table 1. Package types   
Larger package portfolios can be proposed upon request.   

<table><tr><td rowspan=1 colspan=1>Surface mount technology</td><td rowspan=1 colspan=1>Through hole technology</td></tr><tr><td rowspan=1 colspan=1>Package</td><td rowspan=1 colspan=1>Package</td></tr><tr><td rowspan=1 colspan=1>SON</td><td rowspan=1 colspan=1>PDIP.3</td></tr><tr><td rowspan=1 colspan=1>SOW</td><td rowspan=1 colspan=1>PDIP.4</td></tr><tr><td rowspan=1 colspan=1>PQFP, LQFP, TQFP</td><td rowspan=1 colspan=1></td></tr><tr><td rowspan=1 colspan=1>PBGA, LFBGA, TFBGA, VFBGA, UFBGA</td><td rowspan=1 colspan=1></td></tr><tr><td rowspan=1 colspan=1>LGA</td><td rowspan=1 colspan=1></td></tr><tr><td rowspan=1 colspan=1>TSSOP</td><td rowspan=1 colspan=1></td></tr><tr><td rowspan=1 colspan=1>VFQFPN, UFQFPN, WFQFPN</td><td rowspan=1 colspan=1></td></tr><tr><td rowspan=1 colspan=1>WLCSP</td><td rowspan=1 colspan=1></td></tr></table>

Through hole technology (THT) and surface mount technology (SMT) imply dfferent soldering technologies leading to different constraints.

In TT, the package body s eoed to elatively low teperatures (<0) because the leadexremi odippenheoldg lhers  ewho pckae bod p  yhih t (from 245 C to 260 C) during reflow soldering process.

In addition, molding compounds used for integrated circuit encapsulation absorb moisture from the ambient mi.Durgrapheatngn hesolde eo pros e Secon Sldengmehosrmodtails, thiasemoisuvapozrati eset  pailion lasteac package, with a risk of package cracking and potential degradation of device reliability.

# 3 SMD presentation

Unlike through hole technology where leads areinserted into the printe circuit board, SD (surface mount evipacka tt paesta etiysel applications because it has the following advantages:

Packages are smaller and support higher pin counts Packages are light and compact, thus reducing system sizes Mounting can be done on either side of the PCB No cost for drilling holes into the PCB

Surface mount technology also comes along with a few disadvantages:

Increased sensitivity to soldering heat because of their thinner dimension Soldering conditions harder to determine (use of finer structures and higher pin count)

# 3.1

# Handling SMDs

Though the intrinsic reliabilityof SMD packages is now excellent, the use of inappropriate techniques o

When handling an SMD packageisstrongly recomended t use adapted tools such as vacuu pipes avo touching the pins as much as possible. Manual handling could affect lead coplanarity and cause lead catioulabils between two consecutive pins.

# 4 Soldering

# 4.1

# Soldering methods

There are three main soldering methods (which are detailed in Figure 1. Soldering method descriptions):

Single-sided reflow soldering Double-sided reflow soldering Wave soldering (for THT devices)

# 4.1.1 Bending leads

I ueeahe compromised, affecting device reliability.

# 4.1.2 Insertion

the specified pin spacing of the device:do not try to bend the leads to fit nonstandard hole spacing.

![](images/64ab7e25b1a9e1a3531f95362d0256a34d67b7123f10cc0eb6547106645197a7.jpg)  
Figure 1. Soldering method descriptions

# 4.2

# Soldering recommendations

The following recommendations must be followed for soldering each package type (see Table 2).

# Table 2. Package/soldering process compatibility

Re wi DIP  wavl wh BGA, VFQFPN, UFQFPN, WFQFPN, nd WLCSP due to the lead/ball configuration.

<table><tr><td rowspan=2 colspan=1>Package</td><td rowspan=1 colspan=2>Reflow processing process</td><td rowspan=1 colspan=2>Wave soldering process</td></tr><tr><td rowspan=1 colspan=1>Process</td><td rowspan=1 colspan=1>Reliability</td><td rowspan=1 colspan=1>Process</td><td rowspan=1 colspan=1>Reliability</td></tr><tr><td rowspan=1 colspan=1>SOP</td><td rowspan=1 colspan=1>OK</td><td rowspan=1 colspan=1>OK</td><td rowspan=1 colspan=1>feasible</td><td rowspan=1 colspan=1>(1)</td></tr><tr><td rowspan=1 colspan=1>QFP</td><td rowspan=1 colspan=1>OK</td><td rowspan=1 colspan=1>OK</td><td rowspan=1 colspan=1>Under customer responsibility</td><td rowspan=1 colspan=1>(1)</td></tr><tr><td rowspan=1 colspan=1>BGA</td><td rowspan=1 colspan=1>OK</td><td rowspan=1 colspan=1>OK</td><td rowspan=1 colspan=1>impossible</td><td rowspan=1 colspan=1>N/A</td></tr><tr><td rowspan=1 colspan=1>VFQFPN, UFQFPN</td><td rowspan=1 colspan=1>OK</td><td rowspan=1 colspan=1>OK</td><td rowspan=1 colspan=1>impossible</td><td rowspan=1 colspan=1>N/A</td></tr><tr><td rowspan=1 colspan=1>WLCSP</td><td rowspan=1 colspan=1>OK</td><td rowspan=1 colspan=1>OK</td><td rowspan=1 colspan=1>impossible</td><td rowspan=1 colspan=1>N/A</td></tr></table>

1. Wav olderig iMT package ot qualif  MilectroniMT packa ualatin peo s standard by STMicroelectronics only includes infrared reflow soldering. JEDEC JESD22A111 recomends that wave soldering f SMT packages is evaluated by theuser because the ress . 2. Wavoldeg wiVFQFPN, UFQFPNand WFQFPN isot e asiult avooler when leads pass through the double wave.

# 4.3

# Compatibility with leaded soldering process

.ead-free packages can be assembled using a leaded soldering process.

# 4.4

# Reflow soldering conditions

o for an excessive period of time, it may be damaged and its reliability reduced.

It na reResidual fux between the leads rin contact with herein must beremoved toguarantee on-ter relbily.The solvent used to remove exces flux should be chosen with care. It is particular tue or trichloroethylene (CHCl: CCl2). Base solvents should be avoided because the residue could corrode the encapsulating resin.

Hiuality owefolderiquientyinhetpatu rooewge utzi ea colu itol and components.

A typical profile consists of a preheat, dry out, and reflow sections.

Tl minimize thermal shock on the semiconductor components.

Thedryut section is used primarily toensure that the solder paste s fullydrid before hitng fow temperatures.

Sooi zhe pasat the melting solder point.Melting temperature must be exceded byapproximately to ensure quality

![](images/32dd598ec61cfd8a76dfe825cb76bd1952dc29a21593d149a6b6a5748717080a.jpg)  
Figure 2. Typical reflow soldering profile

The recommended reflow profile and typical reflow profile parameters for BGA packages are shown in Figure 3 and Table 3, respectively.

![](images/66e6e7c62935b7b98204d76f3b9a9647ed05b4aa221e42edd79f480a7478e187.jpg)  
Figure 3. Recommended lead-free reflow soldering profile for BGA packages

Table 3. Typical lead-free reflow profile parameters for BGA packages   

<table><tr><td rowspan=1 colspan=1>Profile</td><td rowspan=1 colspan=1>Ramp to spike</td><td rowspan=1 colspan=1>Ramp-soak-spike</td></tr><tr><td rowspan=1 colspan=1>Temperature gradient during preheat</td><td rowspan=1 colspan=1>Temp = 70 to 150 C: 0.9+/-0.1 C/s</td><td rowspan=1 colspan=1>Temp = 70 to 150 °C: 2+/-1 C/s</td></tr><tr><td rowspan=1 colspan=1>Soak/Dwell(1)</td><td rowspan=1 colspan=1>N/A orTemp = 150 to 200 °C: 60+/-20 °C/s</td><td rowspan=1 colspan=1>SoakTemp = 150 to 200 C: 70+/-30 °C/s</td></tr><tr><td rowspan=1 colspan=1>Temperature gradient during preheat</td><td rowspan=1 colspan=2>Temp = 200 to 225 °: 2+/-1 C/s</td></tr><tr><td rowspan=1 colspan=1>Peak temperature</td><td rowspan=1 colspan=2>235 to 245 </td></tr><tr><td rowspan=1 colspan=1>Duration above 220</td><td rowspan=1 colspan=2>40 to 60 s</td></tr><tr><td rowspan=1 colspan=1>Temperature gradient during cooling</td><td rowspan=1 colspan=2>-1 to -5 °</td></tr></table>

1. Refer to solder paste supplier recommendation.

# Note:

STMicroelectronic cannot guarantee the statef the product after relow soldering while t is powereon, because the product is not qualified or characterized at such temperatures (above the absolute maximum ratings). The product can go into an unknown state, and long-term reliability may be impacted.

It is strongly recommended to change the PCB architecture to avoid product bias during reflow.

f it i not possible  reoende to peror  powen reset  rivigheVBAT pin lowormoe than 100 ms while VDD is below the PDR threshold (1.60 V), in order to put the product in a determinate state.

A h is to short the VBAT pin to ground for a certain period of time.

# 5 SMD gluability

It isy ologpi ti gp polymerization for optimal glue efficiency.

![](images/4144a4d2abae0f98ec9af0534341de92667fbf2e7aeb659b998f741f2ec91e57.jpg)  
Figure 4. Recommended profiles for glue polymerization using regular oven and linear flow oven

![](images/26508c002a4b0cfae8c426df142113452300816f0a0e40430963b16890507ee3.jpg)  
Figure 5. Gluability evaluation with a shear test

Various tests have shown that the glue shear test specification limit conforms to the IPC SM817 standard (0.75 kg/mm² minimum). Customer complaints usully happen when values are below 0.5 kg/mm². It has been verid that below 0.kg/mm comonentsll from PCB durig handling.General capabiliyin plastic SMDis greater than 1 kg/mm2.

# 6 Dry packing

The quality and reliabiliy of SMDs afersoldering depend heavily on moisture absorption during storage. A si packg ll y pckwasiplemened r deficonditins at he delivryTmeanenve modify the amount of humidity absorbed. Moisture sensitive SMDs (SOP, PQFP, BGA, VFQFPN, UFQFPN, and WLCP)are dry packed to protect them frommoisture asorptiondurigshiment / storage and then oruce failure risks mainly due to popcorn effect.

# i.1 Pop-corn effect

thetrends towards largerize iintegrate circuits.This phenomenon ismainly caused by themosue absorbed by the epoxy molding. When the package is exposed to high temperatures, as in most ST soldering pewaeae pasn i enlratng pressure.Cracks may occur in the molding compound depending on the absorbed moisture level, soldering temperature and time, die size, package structure and molding compound characteristics.

MD products are contained in tubes, trays, or tapes, and are then vacuum-sealed in a hermetic bag.

Opning he package stops theeal condtins n sarts the nfluencef heoral envioment. Fu shows the recommended handling flow.

![](images/b332992360542df56b426e3f4d897f7f53de81df1d02c71aefc8c3c1e39738ac.jpg)  
Figure 6. Recommended flow to control package moisture absorption

1X depends on the MSL level (see JEDEC standard J-STD-020D).

It is recomende  store parts ndry packndry boxes hat icabints undernitrogenatmosher. Se Table 4 for the recommended environmental conditions for storage when no dry boxes are available.

Table 4. Environmental conditions   

<table><tr><td rowspan=1 colspan=1>Condition</td><td rowspan=1 colspan=1>Recommended value</td></tr><tr><td rowspan=1 colspan=1>Temperature</td><td rowspan=1 colspan=1>5→ 30 </td></tr><tr><td rowspan=1 colspan=1>Humidity</td><td rowspan=1 colspan=1>60% RH max</td></tr></table>

uoulToul vrahicul sor pa To avoid excess weight packing, containers should not be stacked on top of each other.

# 5.2 Dry pack opening

After opening a dry pack, soldering should be done within  hours. SMD products stored over the specied storge period need to be baked at 15 for4 hours (under nitrogen atmosphere). Devices packed in tue in tapes must be transferred to metal tubes before baking whereas trays are bake able.

![](images/f97903ec5122bc3feae61ee53ccdf927f83b27c136764356068d709694ad55cd.jpg)  
Figure 7. Moisture absorption/drying curve

# Revision history

Table 5. Document revision history   

<table><tr><td rowspan=1 colspan=1>Date</td><td rowspan=1 colspan=1>Revision</td><td rowspan=2 colspan=1>ChangesInitial release.</td></tr><tr><td rowspan=1 colspan=1>16-Oct-2007</td><td rowspan=1 colspan=1>1</td></tr><tr><td rowspan=1 colspan=1>26-May-2009</td><td rowspan=1 colspan=1>2</td><td rowspan=1 colspan=1>Modified t and tpin in Table 3. JEDEC standard lead-free reflow profile (accordingto J-STD-020D).Updated Figure 6. Recommended flow to control package moisture absorption.</td></tr><tr><td rowspan=1 colspan=1>22-May-2013</td><td rowspan=1 colspan=1>3</td><td rowspan=1 colspan=1>Updated Table 1. Package types and Table 2. Package/soldering processcompatibility.Added UFQFPN and WLCSP packages in Section 6: Dry packing.Document converted to new template and disclaimer updated.</td></tr><tr><td rowspan=1 colspan=1>07-Jul-2014</td><td rowspan=1 colspan=1>4</td><td rowspan=1 colspan=1>Updated RoHS directive and related note in Section 1: Lead-free packages atSTMicroelectronics.</td></tr><tr><td rowspan=1 colspan=1>17-May-2016</td><td rowspan=1 colspan=1>5</td><td rowspan=1 colspan=1>Updated maximum temperature during soldering in Section 2: Packages overview.Removed reference to application note AN2034 in Section 4.3: Compatibility withleaded soldering process.Updated humidity recommended value unit in Table 4. Environmental conditions.</td></tr><tr><td rowspan=1 colspan=1>27-Mar-2018</td><td rowspan=1 colspan=1>6</td><td rowspan=1 colspan=1>Table 2. Package/soldering process compatibility:updated note 1.changed process for QFP packages</td></tr><tr><td rowspan=1 colspan=1>10-Oct-2019</td><td rowspan=1 colspan=1>7</td><td rowspan=1 colspan=1>Updated Section Introduction, title of Section 2: Packages overview, Table 1.Package types, Table 3. JEDEC standard lead-free reflow profile (according to J-STD-020D).</td></tr><tr><td rowspan=1 colspan=1>05-Nov-2024</td><td rowspan=1 colspan=1>8</td><td rowspan=1 colspan=1>Replaced ECOPACK by ECOPACK2.Removed PLCC package from the whole document.Updated Table 1. Package types and Table 2. Package/soldering processcompatibility.Updated Section 4.4: Reflow soldering conditions.</td></tr><tr><td rowspan=1 colspan=1>03-Apr-2025</td><td rowspan=1 colspan=1>9</td><td rowspan=1 colspan=1>Added note on product state after reflow after Table 3. Typical lead-free reflowprofile parameters for BGA packages.</td></tr></table>

# Contents

#

# 1 Lead-free packages at STMicroelectronics

2 Packages overview 3

SMD presentation. 4

3.1 Handling SMDs 4

# Soldering. 5

# 4.1 Soldering methods 5

4.1.1 Bending leads . 5   
4.1.2 Insertion 5

4.2 Soldering recommendations 6

4.3 Compatibility with leaded soldering process 6

4.4 Reflow soldering conditions. 6

# 5 SMD gluability. 9

# Dry packing 10

6.1 Pop-corn effect 10   
6.2 Dry pack opening 11

# levision history 12

_ist of tables 14

List of figures. .15

# List of tables

Table 1. Package types. 3   
Table 2. Package/soldering process compatibility . 6   
Table 3. Typical lead-free reflow profile parameters for BGA packages 8   
Table 4. Environmental conditions 10   
Table 5. Document revision history. 12

# List of figures

Figure 1. Soldering method descriptions 5 Figure 2. Typical reflow soldering profile   
Figure 3. Recommended lead-free reflow soldering profile for BGA packages   
Figure 4. Recommended profiles for glue polymerization using regular oven and linear flow oven. 9 Figure 5. Gluability evaluation with a shear test 9 Figure 6. Recommended flow to control package moisture absorption. 10 Figure 7. Moisture absorption/drying curve

# IMPORTANT NOTICE  READ CAREFULLY

pt old ursant  dits   leole.

purchasers' products.

No license, express or implied, to any intellectual property right is granted by ST herein.

are the property of their respective owners.

I

© 2025 STMicroelectronics - All rights reserved