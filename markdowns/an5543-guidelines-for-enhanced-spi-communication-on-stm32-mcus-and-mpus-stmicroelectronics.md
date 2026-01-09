# Guidelines for enhanced SPI communication on STM32 MCUs and MPUs

# Introduction

handling decreases the overall system load.

manage the most frequent difficulties encountered when handling SPI communication.

Tarionspent eeiration MPU.

The reader must be already familiar with the basic SPI principles and peripheral configuration options.

description.

# 1 General information

# Note:

This document applies to STM32 Arm®-based devices.   
Arm is a registered trademark of Arm Limited (or its subsidiaries) in the US and/or elsewhere.

# arm

# 2 Released versions

The SPI peripheral for STM32 devices has evolved over time. The following table summarizes the main differences between active versions.

Table 1. Main SPI features on STM32 devices   

<table><tr><td rowspan=1 colspan=1>Version(1)</td><td rowspan=1 colspan=1>1.2.x</td><td rowspan=1 colspan=1>1.3.x</td><td rowspan=1 colspan=1>2.x.x({2)</td><td rowspan=1 colspan=1>3.x.x(2)</td></tr><tr><td rowspan=1 colspan=1>Data size</td><td rowspan=1 colspan=1>8- or 16-bit</td><td rowspan=1 colspan=1>4- to 16-bit</td><td rowspan=1 colspan=2>4- to 16/32-bit</td></tr><tr><td rowspan=1 colspan=1>Tx &amp; Rx FIFOs</td><td rowspan=1 colspan=1>No</td><td rowspan=1 colspan=1>2x 4-byte</td><td rowspan=1 colspan=2>2x 4- to 32-byte</td></tr><tr><td rowspan=1 colspan=1>Data packing by data-register access</td><td rowspan=1 colspan=1>No</td><td rowspan=1 colspan=1></td><td rowspan=1 colspan=2>Yes</td></tr><tr><td rowspan=1 colspan=1>Data packing by packets</td><td rowspan=1 colspan=2>No</td><td rowspan=1 colspan=2>Yes</td></tr><tr><td rowspan=1 colspan=1>Dual clock domain (APB and kernel)</td><td rowspan=1 colspan=2>No</td><td rowspan=1 colspan=2>Yes</td></tr><tr><td rowspan=1 colspan=1>Programmable transfer counters</td><td rowspan=1 colspan=2>No</td><td rowspan=1 colspan=2>Yes</td></tr><tr><td rowspan=1 colspan=1>Underrun detection/configuration</td><td rowspan=1 colspan=2>No</td><td rowspan=1 colspan=2>Yes</td></tr><tr><td rowspan=1 colspan=1>Autonomous operation in low-power modes</td><td rowspan=1 colspan=2>No</td><td rowspan=1 colspan=1>Yes(3)</td><td rowspan=1 colspan=1>Yes(4)</td></tr><tr><td rowspan=1 colspan=1>Master transfer suspension</td><td rowspan=1 colspan=2>No</td><td rowspan=1 colspan=2>Yes</td></tr><tr><td rowspan=1 colspan=1>Master automatic suspension</td><td rowspan=1 colspan=2>No</td><td rowspan=1 colspan=2>Yes</td></tr><tr><td rowspan=1 colspan=1>Flushing content of FIFOs</td><td rowspan=1 colspan=2>No</td><td rowspan=1 colspan=2>Yes</td></tr><tr><td rowspan=1 colspan=1>Master data/SS interleaving</td><td rowspan=1 colspan=2>No</td><td rowspan=1 colspan=2>Yes</td></tr><tr><td rowspan=1 colspan=1>GPIOs alternate function control when SPI isdisabled</td><td rowspan=1 colspan=2>No</td><td rowspan=1 colspan=2>Yes</td></tr><tr><td rowspan=1 colspan=1>Configuration protection by locking</td><td rowspan=1 colspan=2>No</td><td rowspan=1 colspan=2>Yes</td></tr><tr><td rowspan=1 colspan=1>Swap of MOSI/MISO, reversed SS logic</td><td rowspan=1 colspan=2>No</td><td rowspan=1 colspan=2>Yes</td></tr><tr><td rowspan=1 colspan=1>RDY signal option with suspension</td><td rowspan=1 colspan=3>No</td><td rowspan=1 colspan=1>Yes</td></tr><tr><td rowspan=1 colspan=1>Master input data sampling delay</td><td rowspan=1 colspan=3>No</td><td rowspan=1 colspan=1>Yes(4)</td></tr></table>

denti heversn and the available featue er the prdceerenemanal n datahet. 2. i audio specific protocol support depend upon the instance implementation. 3. Limited capability, not fully supported. 4. Dependent upon implementation, not available on all products.

# 2.1

# Differences between versions

Teifent vris hav e   n ple  heat Md epab wakufom o-pmoSom eaus  e es  soran heveilaf domain, and programmable transfer counters, described in the following subsections.

# Data size

Data size can be fixed and multiplied by 8-bit, or can be adjustable by bit.

# Data buffering of Tx and Rx streams

T o set of registers collected at dedicated FIFOs.

# Dual-clock domain

Tl u  l.

More recent versions feature an autonomous run at low-power modeunder kerne oralso under external clock ys ph int loc bil be snsekeel cloc rameock gete phal u APB.

# Programmable transfer counters

The speciiccontrol related to "end of transaction" actions such as slave-select (S) management, RC clic anheaeholae b prootacnueall  hould  ermeuatially yharwausi pe counters.

Earvsnsot atue obln  Avrkehesk . The latest versions feature embedd counters, hence S takesover control f programmable counters ctn via the SPI configuration. In these cases, the DMA role is limited to manage data transfers.

# 2.2 Frequency constraints

Teus banihdepenuonhereqency)appl he ssca cocai( suos a there is enough margin to handle all the fast data flow in time (see Section 4.1).

In stes atrig a sglclocain, he heeial limi isup tohal heAPB clock apl e peripheral in both master and slave configurations.

Ondul cocomi stes, hee specconstrait onenigherat been coc eediAPB a the kerlomais. In casnintffencs, heuermus pect embecloc p needed to synchronize and propagate the signals shared between the domains (such as changes of flags or asal whea shor, r examplethenderrun protecion logit slavorhandling nptional Rstatu sigal betwen master and slave.

Tl conpueatintal paala Temperature and low-supply voltage have an impact too: significant dirences at the highest accessible communication speed can be observed between SP instances (or their mapping options), SPI modes, power m the datasheets.

# 3 Data flow handling principle

Ta  ll l  ha input and output serial bit streams on MOSI and MISO pins, synchronously clocked by the SCK signal.

T u h rku weecluec through the MISO and MOSI pinsv shift registers associated with the RAM storage area providing separated Tx afr  he buf e geti Mo athwoner n accessiblereador writaccesses to physicallydoubled  dataregistersallocatedunder sigle cmo lu to this domain.

D t buffer is ready to accept new data.

Duel moved from it into the associated Rx buffer.

When the peripheral is configured as slave, the SCK clock is always provided by an external source. When curs,e Cccial e  e pal APB bus clock or a specific separated kernel clock). This clock signal divided by embedded clock baud rate generator feeds the outer serial interfaceof the SCK signal mastering communication with the slavenodes.

![](images/cf68dde54b7ff35d61ea7334977356663f384990ec6ffc1a083baf32f464e74e.jpg)  
Figure 1. Simplified data flow scheme

In ful-uplcomunication, hedatahandshakeorranission ad reception donen paral. Ea nw t traite datfaemust evailble ex urbeoreranser begisWheno ew available, SPI master suspends the communication, but the slave forced to continue operation faces data nal can be written into the buffer once there is enough space to store them.

T alwas ependent  heactual bufrcontent, whilehe s  hedatrame alread providd from he aateshif register is fied.Asa consequence,dataoutput sgal cantoggl ndependently n SCK al configuration.

T Whuipacpteex Tui completed.

T ollowinggure provides a spliexample a contuus  comuicatin handle by MAhe ie of the data corresponds to a single DMA access of the SPI data register. The DMA write stream is completed a o are completed (if CRC is applied).

Eve fot ecary i is visooior heBSY  EOT/TXC fag t the enf theranser  peven ngaee oen ame otn vgc ve o SPI versions replace the BSY signal by the EOT and TXC flags. Single-data handlig events signalized by TXE ad RXNE flags are replaced b TXP and RXP or DXP flags, whic handle the data packets events.The ti the sigals isalmost the sameacross al versions.Bfgmonitring is ot sugested tohandle hat flow.

![](images/4ebe1ee31f7dd44ed79916159c4d992c9daa818e87d0762c2fde8027dceaebdb.jpg)  
Figure 2. Timing of SPI data events and DMA transfer complete flags during a transfer

# 4 Data flow potential problems

The most frequent problems are grouped in three categories:

System performance and data flow

Ratio between APB and kernel clock Ratio between master and slave performance Frequency of the SPI and of the DMA events

Specific modes handling

Data corruption by a premature termination Handling exact number of data SPI reconfiguration and handling of associated GPIOs Handling half-duplex operations via a single bidirectional data line

Specific signals handling

Internal interface signals Optional external interface signals

Specichandling autonomous SP peration in low powermodes s utf thi document scope.Versin 2.. icapable todrive seral bus cocking  stop mode whileraisig asynchronous iterrupts tohandata exchange.Version 3.x.x, additonall, can handle the data exchange between the peripheral and memory via smart DA f implemented in the product. This is done without need or syste wakep, due to temporal domain's clock requests handled by the peripheral while the data transfers can be synchronized with other peripherals by internal triggers. Refer to documents targeting LBAM control, such as AN5645 "STM32U5 Series power optimization using LPBAM"

# System performance and data flow issues

The SPI bus is potentially fast and the system must be high-performance to handle the data flow in time. Depending on the SPI mode, the system must prevent data overrun in reception, and data underrun in tsTely nelwhe aC cl sialntus eatramhora lockparableaserhan core clock.

A praal example is a stin when hebaud ates L /,and dat fram  hortened o  s.The aces toP evet withach interval 8CL per n ull Duple-ode. Ihi case  CL simlar r equal t)the ystem clock, thers ot enouh margin  system level tohandesuchcnious betal icative whe levailabl peoancent i timi gr poe sas margeuus f nh statu gisteanhandeheanserten he atgisterandememo corresponding flag is active.

Se below a simplified piecef C-code loop it assumes that R1 and R2 PU registers keep the x and Rx data pointers towards the memory, while R3 register keeps the base address of the SPI registers):

while (1) { if ((SPI->SR & SPI_SR_TXE) == 0) { SPI->DR = \*tx_data++; } if ((SPI->SR & SPI_SR_RXNE) != 0) \*rx_data++ = SPI->DR; }

# The assembled result of the compilation of the C-code is shown below:

??main_1: LDR RO, [R3, #+08] ;test TXE flag LSLS RO,RO,#+30 BMI.N ??main_2 LDRB RO, [R], #+1 ;read and send next data from a memory STRB RO, [R3, #+12]   
??main_2: LDR RO, [R3, #+08] ;test RXNE flag LSLS RO,RO,#+31 BPL.N ??main_1 LDRB RO, [R3, #+12] ;store next data received to a volatile memory STRB RO, [R2], #+1 B.N ??main_1

Ev  pli loode e hot  ecith  epicogure or de spee otiization nh ort® example.Teeeutinf ths lo critil v within 16 cycles available with a standard 8-bit data-frame configuration.

I  event ehanded bynterups, te ystem must peform he same umbe ccodete the pgv queonshee v ol spends aditional cycles or service entry and return, necessary to safe and restore the interrupted main execution context at stack. That is why a solution based on interrupts is not useful in this case.

A psiblesolutionsplement DMA, ut heser mus ot overstiat heanwidth  provil solution to the problem. DA stil needs a few system cycles to perform the requird data transer whil the execution of the related service can be postponed because another system operation is ongoing. Each DMA tranermustst gothrough the busmatri bitration process (wier takes the mati path tomakethe transfer), hence the transfer and the associated arbitration takes up to seven system-clock cycles.

No v simultaneous request from another DMA channel or by the execution of a non-interruptible data-transfer peorme by he .Exaple uc sencs e he tac cntehandn tet hka eelay ev peniA qus aexweyste-cock cycemut frames can be missed on the SPI bus.

# Software or DMA unable to handle data on time

The remadcatorsdicating hat atmanagementot donent y otwarer DMA), py pceve data underrun.

# Data corruption (data flow is not as expected)

Some data patterns are missing, wrongly repeated or in any way partially corrupted.   
Note that when correct orderof bits is shifd by neor more bits in the fames, this situation rets   
a synchronization issue between master and slave rather than a late handling data by system.   
Some actions that help to identify data-corruption problems are:   
o The implementation of a HW CRC checksum at the end of each transfer batch. Any data redundancy check such as repetition of the messages, plausibility check (comparison of the message with the expected content) or any other similar predefined protocol.

# Data overrun (RxFIFO space overflow)

A system performance issue during reception is put in evidence when an OVR error flag is raised.   
Data overrun is mainly a slave device problem.

Data overrun can also appear on a master device configured in Receive-only mode, because the SCK clock signal is provided continuously and independently on the data-buffering process, except for devices featuring master automatic suspension of the communication mode when the RxFIFO is full (see MASRX bit control in the reference manuals).

# Data underrun (TxFIFO space underflow)

The primary cause is low system performance during transmission.

Data underrun occurs only on slave devices because master always suspends the transmission when its Tx data buffer becomes empty and there are no more data to transmit. A master configured in I2S mode works differently in case of underrun.

The most recent devices feature configurable behaviour and specific indication (via UDR flag) in case of underrun. The device can repeat a constant pattern defined by the user or apply the latest received pattern, behaving as a simple shift register (applicable at a multi-slave daisy-chain circular topology). Repetition of the last transferred data frame is useful in I2S mode to achieve a smooth audio output.

For devices not featuring UDR flag, the underrun event is hidden. Some side effects can be visible, such as a flow corruption by repetition of a data pattern previously transferred (the value depends upon the design). For example, when FIFO is implemented, the oldest FIFO pattern is applied(1).

Data underrun depends upon the timing between the moments when data to transmit are written to the data register by slave and the startof is transfer by master. I slave manages to write thedata withi  fst bit transer period n spif heunderr condiion, he new data can beaccepte o tranmission, but there is a potential risk of corruption of the irst transferred bit.This depends n he LSIRST bit setting if themost or he least niiant bt of thedat fram  onsiderd. If here comes later, the underrun pattern is completely transferred while new data are buffered for the next transfer.

1. master without any other update of the slave's TxFIFO, the slave output is OxAA, OxBB, OxCC, OxDD, OxAA.

In avgu hesval at ndtgis v v factors lock-phasettin,tmig between aocasinal late-datawriversus thebeginig the next

o the bus with he leadg CK egef the next ansacon o ewdat eaplheHA  is ieto   eee ae arasoa i postgecey heald ariteintoeategisa popaga intoepty T ufrhe becomes ready for the data transfer in this configuration.

else there is no toggle and the switch between the underrun and the valid data source is not visible.

T thal a e  mplng eder dept valrgly plW sampling is perorme at conguration  HA = when the data wricomes too lateer the sampli i performed at the beginning of the period.

![](images/7dc52ba49e1d37baa536122af0e9b1e54e3349ee4d60bfbd17fbea85e21d055d.jpg)  
Figur. A late write nderun) data while rs-it transfer sg

Acangeenvalumplisrv wheA=despheatwri wis bit transaction period, so the transfer between Tx buffer and Tx shift register is still accepted.

# 4.1.1

# Recommended methods to handle frequent SPI and DMA events

T if ole waanden  MA eventut pblty e the desin. Olderdevices do ot ecessarily eature dataFFOs r widely configurable data size and theyhave limited configuration capabilities compared to recent devices.

T voee requests is very frequent.

Oi peoan s hiv whe DMA takes carl heat flow anoher speceventas wi theran poll byotani ytert abl yeleiv sTeu alway heck he tatuseror ags detec problems with busropurwit ytem peorma In some cases, even optimized system performance is not enough for a fast SPI fow, and the user must apply additional methods to secure sufficient bandwidth.

Some effective actions to improve the management of frequent SPI and DMA events are:

Decrease the bus rate: the ratio between the system and the kernel clock increases.   
Increase the data size.   
Collect data into packets when the software fills in and reads out the data.   
Balance the data register access with the data size and the threshold level of the FIFOs or of the data configuration setting. More information is detailed in the following section.   
Slow down the data rate leading to discontinuous clock by using fixed or enhanced adaptable methods the temporal communication suspension between provided data frames or sessions.

These actions decrease the frequency and the number of data handling events. The system performance improves, thanks to a better management of their detection.

To decrease the latency when serving the aised events, tmporarily disable interrupts or DMA channels from other peripherals, and set up and order priorities of the DMA channels.

Susitertizhecutheobiuatun he. usermust avoid automaticregister reresh ormemory dump windows during debug to avoiddecreasing the BUS matrix throughput. When DMA interrupts are enabled, the half DMA transfer-completion interrupt must be suppressed if not used. Servicing this event becomes critical when a small number of continuous data is transferred by the DMA session or when frequent DMA data-handling services face a bad system performance (refer to the DMA HT and TC events on Figure 2).

Aaheat owntto e. The atest vrsions eaturtinal progrmable iintrleaviggaps betwe es, etw e Sial that bece actvand datranse sessinbegin n they an lsoiplementanu suspension  themaster.This emporary suspension f the master's transfers prevents data underflow and ovefow,and can be achieve by monitorig heRxFFOocupancy (MASRX featureor bymonitrig adital l l v p aI up data output when communication timing control is done by filling dummy transmission data.

Other features present in latest SPI designs, which simplify the data-handling processes are:

Capability to use an optional coupled dual-flag event to control both transmission and reception of a common event with a single software service

l   nnWuvn ha ha dat riantondianrerhe eviiseenc becomes idle.

Thedualgandg must avoie savmod whenemast ntiuy oviin coc al a service of the pending TXP event (which always precedes a RXP event).

Themain sense  the DXP appears when targeting low-power applications, especially when the data-handig seriae mulateandheumbe decease minmum, which prevent ysefromfequen wake ups. The counterpart for that is slowing down the data rate.

# Balanced handling of communication events

Ataiveawigu pakingTes cngures herehold leveedat bufwhic etermie hquencya handling events.

Tti rgult ackgiqualiehanele size.

Awieraccessf the SPI data register can be provided by software or by DMA;he access correspons to a F e register. The type of access is defined by casting the address of the data register at code level.

In recent devices, he user can additinally defie longer data packets and cumulate eris  dataegister accesses on a single event. The number of accesses must correspond to defined threshold of the FO. The events hen sigal that just the pack servic s available and a next sequence repeated datacceis g  hn ack m dahandngevent ndeaseshe yte' siiant wayadtbatalwayrvic hillna by one data access sequences.

A TXE corresponding to a TXP event is raised once the buffer for transmission can accept the next data p pc releasing the necessary space is transferred out.

The Tx bur may become empty and the SCK clock signal can stop and become non continuousf the master fn  iiW sameiuatinhappens whihemasterontinues hetranser, te saveacedatnderrconn.

Refer to Figure 3 for a related example. This case can also be observed at MisO toggle.

Ial e packe ould oe alsTia llws at servicing next packet close to a whole single-packet transfer duration.

I eFurnhaangp pack at receive data side at RxFIFO.

Underheabove coniguration, ven al ervilatencymaygenerateranserproblem anddat packi beoes useles.hat typ  configuration makes sens ointerleave  batches wit anumber a cpletely accomodateat  spac. I hat case, the aplicationas enouh room handedate a batch is completed before the next batch starts.

Whe ulupleoplheeheveall atrei i balandThe transferreddat goes n parallel with he common clock signal and the handling bot at icisg nandei d ot sar ontinue y nsactin,dh vefcsndeun whenever heo availabl ready at the Tx buffer while a transfer is ongoing.

Ivieuaplaviis reception flows together. This functionality is especially useful in low-power modes.

Some actions to cope with different timing of the both data flows are:

Store some data for transmission in advance   
Handle the middle of the transfer by common DXP events   
Finish the session by handling the remaining received data at the end of the session (for example by an EOT event).

# Note:

1 DXP event interrupt is suppressed by hardware once all the data for transmission is submitted.

The followigfigure is an example o a TXE/TXP event service atenc limit available at slave or DMA. The eaowtnnuecvlbl X XE durng Dtransenc paceareoug cmoatu  packe is eleasanavailable buffer to accept new data.

![](images/47f9faca5c9440b66ab06f254859629a1aad137ed0b829e3b44eaada1a727e4d.jpg)  
Figure 4. DMA late service of TXE/TXP event

# 4.2 Handling specific SPI modes

SPI transfers are based on a predefined exact number of data. Some enhanced SPI modes are sensitive to deteriisacntngpeontandleat loshea transfer.

# 4.2.1 End of the bus activity detection

by premature fatal terminating accesses are:

SS signal control   
Necessity to disable the peripheral after the session is completed due to system entry into low-power m pehel coovalae perhe oigurat eaplha direction at Half-duplex modeor setup another configuration of the SCK signal or baud rate or simply reset the internal state machine before next session start).

The end ofhe bu ctivy an beeteeasiy b RXNE RXP fasaling en last daten. E o e  exclusivly sn od. In scase  al onirhe  eu aivi  BSY, EOT rTXC fas.Ayi  DMA cpleventi otpliable,a SPI canil transmitting (refer to Figure 2).

Fo moitorg dial spemeasurment ua meou monioriaee ecus is not fully reliable on old devices. BSY should be cleared by hardware between data frames when cicatituheullpleewihlihtronzation between master and slave.

# Specific aspects when SPI is disabled

eectiviecbu e when doing so.

The FIFO content handling while SPI is disabled depends upon the design.

On versions 1.3.x, the content of the Rx FIFO is preserved and accessible. Disabling SPI is a standard procedure to terminate the simplex-receive modes. On versions 2.x.x and higher, software suspension is used to terminate whatever ongoing flow. Tx and Rx FIFO contents are flushed, lost and impossible to access when SPI is disabled.

Another problem related to peripheral disable is the control of the associated GPIOs:

Versions 1.x.x: the peripheral takes no control of the associated GPIOs when it is disabled. If the SPI signals are kept in alternate function configuration, they float if not supported by external resistors. Versions 2.x.x and higher: the peripheral can keep the GPIO control even when it is disabled (depending on IOs alternate function configuration managed by the AFCNTR bit) to prevent unexpected changes of the aociated masteroutputs especially. In the contrary, when user apply SP configurations affecting the IOs configured in the control keeping mode (such as change of the SCK signal polarity), new default levels are propagated out immediately despite is stil disabled. Be careful with desynchronization between master and slave, and perform the configuration change exclusively when no slave is selected.

SPI must be disabled before the system entries into Halt mode and between the transactions when SPI must be reigured or torestart he internal statemachine properlyEven  S disable between sessions is not manatouratienalil reigurationple nalit calculationcnting at cofigurettandardae conting ata whoseume isot aligned wia configur dat packe,ecovery otransactionsusns done by software) are applied.

T msto b eculcplehoul  or  sl at slave, especially between sessions, to prevent missing the next communication start.

Tmosen  ee ensitivarwal teon;heaste ovie ad thefollowig session.Thiss ot he case on older design where he S etectin  evel sesitive.

# Time-critical control at the end of transfer

just during last data handling:

Change of the FIFO threshold configuration to handle data not aligned correctly with data or packet size At the end the CRC pattern control of data validation Proper termination of continuous data-flow like master configured in Receive-only mode to prevent any unexpected additional dummy-data transfer and ensure that the required data are transferred. In earlier versions, terminate this mode requires nonstandard disable access during ongoing tra This is the case when SPI disable must be applied when communication is still ongoing on the bus.

tevTorilbeo a latency outside this interval.

T eu at h i da packe is proces afal incopletdata mus  nt.Te saewindow appl when conto cl fowreceiveony mode must eermiat propery master receive heexpec umbert while preventing next dummy data reception.

![](images/94199b7ac677b07404a51bce58d810e7fce9944029418c45af49403112647765.jpg)  
Figure 5. Examples of window available to perform specific control at the end of a transfer

If thdevicatur programabledatcounter speccontol sdoneutnomously thend ec ra. Inhs casheern perate wit e st ot-cople packewi nar ce pyent atl n revatn wrio g ca e owo pac nt pac ivsrmust check heOanc st he ernseo l number of data is received.

Asoleevidesot fatubeatconersvioeDMA ndatconter. DMA peormshe equi contro actin autnoouslytardware velhencehesk miss hevalble control window is lower compared to an actin performed by software.User must correctly et up the dat DMA counters to ensure handling f proper number of data on Tx and Rx side (especially when a CRC patten has to be added). The size of the CRC pattern must be excluded from the data counting number and theCRC p CRC is finished.

Teollg tble priverviwhei Rttgs pbl Moet be found on the corresponding product's reference manual.

Table 2. Differences of CRC control between active SPI versions   

<table><tr><td rowspan=1 colspan=1>Feature/Version</td><td rowspan=1 colspan=1>1.2.x</td><td rowspan=1 colspan=1>1.3.x</td><td rowspan=1 colspan=1>2.x.x</td><td rowspan=1 colspan=1>3.x.x</td></tr><tr><td rowspan=1 colspan=1>Setting of DMA data counters</td><td rowspan=1 colspan=1>Number of dataexcluding the CRC</td><td rowspan=1 colspan=1>Number of dataexcluding the CRC(1)</td><td rowspan=1 colspan=2>N/A</td></tr><tr><td rowspan=1 colspan=1>Setting of TSIZE counter</td><td rowspan=1 colspan=2>N/A</td><td rowspan=1 colspan=2>Number of data</td></tr><tr><td rowspan=1 colspan=1>Handling the end of a notaligned packed transfer</td><td rowspan=1 colspan=1>N/A</td><td rowspan=1 colspan=1>By software (viaLDMA_RX bit)</td><td rowspan=1 colspan=2>Automatically by hardware</td></tr><tr><td rowspan=1 colspan=1>CRC size</td><td rowspan=1 colspan=1>Fixed CRC8 for 8-bitdata and CRC16 for 16-bit data</td><td rowspan=1 colspan=1>CRC8 or CRC16 can beapplied for either 8- or16-bit data</td><td rowspan=1 colspan=2>4-16/32 bit(2)</td></tr><tr><td rowspan=1 colspan=1>Flushing of the CRC patternfrom RxFIFO</td><td rowspan=1 colspan=1>Exclusively by softwareread access of RxFIFO</td><td rowspan=1 colspan=1>By software read accessof RxFIFO(1)</td><td rowspan=1 colspan=2>Automatically by hardware</td></tr><tr><td rowspan=1 colspan=1>Initialization CRC pattern</td><td rowspan=1 colspan=2>Fixed to all 0s</td><td rowspan=1 colspan=2>Selectable all 0s or all 1s</td></tr><tr><td rowspan=1 colspan=1>Reset CRC calculation</td><td rowspan=1 colspan=2>Both SPI and CRC disable</td><td rowspan=1 colspan=2>By SPI disable</td></tr></table>

Fu lRCt be used in Rx-only mode, where the CRC pattern flushing is handled exclusively by software.

2. tR Tl configured for 32- or 16-bit instances. TSIZE can never be set to its maximum value when CRC is enabled.

# 4.2.4

# Handling the Half-duplex mode

Te most problematic  ask ishandling he Haluplexmode,whic requirscmon singleataine hare easaaa previously:

# Handling exact number of data at particular simplex sessions

Terminating of master-receiver working at Receive-only mode is critical when the ongoing continuous flow must be stopped correctly. When handling CRC pattern upend or when the session is not aligned with the configured data threshold both data-flow directions require a specific control of the correct numberof transferred data at the end of the flow.

# Checking the end of the bus activity of a particular session

The bus has tobereconfigurd between sessions norder tohange drection f the data le ile CRC or configure the next session parameters. To do the configuration, SPI has to be temporary disabled. Thi disable miht corrpt he  tegoig sessn, t is whyhe   e us actiiyhas properly detected before disabling the SPI.

# Reconfiguration of the bus between sessions

A change of the data-line direction must be synchronized on master and on slave sides, but these reconfigurations are independent, hence not fully synchronized. The reconfiguration timing is affected by how the involved nodes recognize the end of the bus activity and by the latencies of their SPl reconfiguration services. One node can initialize its GPlO output at common data-line while the opposite node is not yet able to manage the reconfiguration. Then it can happen that both GlOs outputs propagate diffutut evels nce  eeameme  u prepenn at transferre and on he lieclock phase setting). It ishighlyrecommended toimplement a serial resisorat this common data-line between the nodes. This action prevents a temporal short connection between the outputs and limits current blowing between them when just opposite levels are matching on the line.

# Control of associated GPlOs to keep nodes synchronized

The necessity of the peripheral reconfiguration within the session requires an SPI disable. It brings aditional effects like flushing the FIFO content or loosing control of theassociated GPIOs.Continuity o SPI signals during reconfiguration of the bus must be ensured to prevent any synchronization issue between the involved nodes. Master has to avoid any glitches on SCK and SS signal. These signals might have to be managed by software as a general purpose outputs during the interface reconfiguration phase. An interactive sessin often starts by a command (wrie) sequence sent by master olowed by an adequate response (writer or read) sequence when slave receives or sends data matched with the command content (except for cases when the protocol between master and slave is fixed). The master must always give sufficient time to the slave to reconfigure the bus, torecognize the command and to prepare the adequate answer. It mostly requires to avoid a continuous SCK clock signal and insert an adequate pause between such a command and data phases.

THalpeonypaluseeeavg line and the scate G pin utputare worth thert, s Full-uple couicatin mode s e t uluptuat can focus onhandling the data content at the required direction while the data at opposite direction (not monitored) is either ignored or placed dummy.

# Handling specific SPI signals

T tmecallaall of the SPI interface

# 4.3.1

# Handling specific internal signals and interfaces

Invsns,eAveak parcnol  alite acn, therefore her   wid interace between DMA and .Themos recent versions fully vertake heol ivol be correctly set and well balanced on both the SPI and DMA side, especialy when enhanced SPI modes are u. Note that allthe DMA aess is basd on the TXP and RXP or EOT datathreshold events. Ian vent is missing (for example when incomplete data packet is done), no DMA transfer is performed.

On recent I versions, the Simplex S modes are strictly separated. There is o longer need tomanage the unused RxFIFO flushing, nor to handle ts OVR errors. DMA channel enable must be prevented in the nused direction.

Wheariableescat guraltaoutod u a faciv  e a l  vrs p leaves them undefined and floating.

Ohebl attel al leve  ptn ufu). Thi proaatinayor patuArem ques eat l inteup ri eable in the configuration). Even a system without any FIFO could raise two consequent data requests when data write request immediately after the transfer starts (refer to Figure 2).

Table qce caal mus ol ront processing and to avoid missing any event service or a dysfunctional initialization of DMA streams.

Sal analatve wint ten ua-coca.Foa uvvalatde rhl clcoma iuenomeu isnecessary evaluate he status ewadtinal  clocksignal cycles areneededThisadtinalaf makevenrablyaablecny once the underrrun flag is detected or cleared.

T zccc between them, some system responses may be processed wit significant delay, causing unavailability some features (refer to Section 2.2: Frequency constraints).

Mot  wakes loo al-cloc can autonomously communicate at low-power mode while all the necessary internal clock requests are automatically provided at dependency on applied SPI configuration and actual FIFO status.

Rv uli seablea syncronization witohe peripheal evet without ystem wake-pTecnaliyd wakeu capal are product-dependent, refer to the reference manual for more details.

# 4.3.2 Handling optional signals

Slav elec (/S)is tial S inteac igalhis igal isseul t mult slavrmultase toogi pecaly when t ssins just sigle lave node oiation at his sial ul even at singlemaster/slave systems s it permits o separate and synchronizetransfers between both nodes. Specific modes lake Slave Select pulse or TI one synchronize even each data frame.

Harwaor he SSmasutpu tanar  Moola modeis ot eal overss. T al logiccopis he E taus an causs probles ande  Oaltenatnctin. Whenhe P i l el ge antat i nc set to zero.

O n  snoloverealt n  tevebl. e las Ml ny orig T le ucnhas e ela  anar) when handling a mult slave systemor when a specifi communication requires a reconfiguration f SP within a sgle essin (such at Halduplex mode whenhe  has  e isable temporarily while  eeds stay active).

Recent SPI versions are edge selective in SS input hardware management mode (SSM = 0). A session can be misd when  isenabled afer themasterhas provided the active egefhe  sigal. Olderdesis an SS software management mode (SSM = 1) are always level sensitive.

An optional RDY signal s featured in some SPI versions, which perorms he slave's FIFOs occupancy status, RDY ean  ave vein.vi communication is temporarily frozen when the slave provides a not-ready status.

# SPI instances with different features

On 32 devices the same peripherals can be mplemented with different configurations The main diffeences are:

Maximum supported data size and its configurability (by bit or by multiple of bytes)   
Maximum supported polynomial or frame CRC size   
CRC configurability (by bit or by multiple of bytes)   
FIFOs capacity   
I2S support availability   
Maximum number of data in single session

# Low-power mode operation capabilities

Thedifferencs between he mplemente instances ardetaile in he implementation tablereence manuals.

# SPI synchronization between nodes

S  o zas handling. The only synchronization signals featured by SPI are NSS/SS, hence the user must check all desynchronization symptoms.

Pusncratinglialsacroan SCK alternate output during SPI reconfiguration.

Deit fag can exceptionallyhag monitoring clearing can helpfu when communication beome idle. If it stays set, it might signal possible synchronization issues between master and slave.

Corr at hi ymoe  nRCeorssequencnronization probles. I a the root cause. If a desynchronization occurs, both the master and the slave nodes must be restarted.

Recnt products can support hal SCK clock perid delay the MIOmaster input samplig.This canhelp to cpesat galeon elayais exaple, wheu ignals otosolat ee availability in configuration registers).

Apply S disable between sessions.This resets the internal state machine, and corrects desynchronization problems, if present.

# Revision history

Table 3. Document revision history   

<table><tr><td rowspan=1 colspan=1>Date</td><td rowspan=1 colspan=1>Version</td><td rowspan=1 colspan=1>Changes</td></tr><tr><td rowspan=1 colspan=1>30-Nov-2020</td><td rowspan=1 colspan=1>1</td><td rowspan=1 colspan=1>Initial release.</td></tr><tr><td rowspan=1 colspan=1>29-Jun-2021</td><td rowspan=1 colspan=1>2</td><td rowspan=1 colspan=1>Updated Table 1. Main SPI features on STM32 devices</td></tr><tr><td rowspan=1 colspan=1>12-Apr-2024</td><td rowspan=1 colspan=1>3</td><td rowspan=1 colspan=1>Updated document title, Introduction, Section 4: Data flow potential problems, andSection 4.5: SPI synchronization between nodes.Updated Table 1. Main SPI features on STM32 devices, and Table 2. Differences ofCRC control between active SPI versions.Minor text edits across the whole document.</td></tr><tr><td rowspan=1 colspan=1>03-Oct-2024</td><td rowspan=1 colspan=1>4</td><td rowspan=1 colspan=1>Updated Table 1. Main SPI features on STM32 devices.Minor text edits across the whole document.</td></tr><tr><td rowspan=1 colspan=1>21-Nov-2025</td><td rowspan=1 colspan=1>5</td><td rowspan=1 colspan=1>Updated Table 1. Main SPI features on STM32 devices and its footnotes.</td></tr></table>

# Contents

# 1 General information

2 Released versions 3

2.1 Differences between versions 3   
2.2 Frequency constraints 4

Data flow handling principle 5

Data flow potential problems.

4.1 System performance and data flow issues

4.1.1 Recommended methods to handle frequent SPI and DMA events 10   
4.1.2 Balanced handling of communication events 11

4.2 Handling specific SPI modes. 13

4.2.1 End of the bus activity detection 13   
4.2.2 Specific aspects when SPI is disabled 13   
4.2.3 Time-critical control at the end of transfer 14   
4.2.4 Handling the Half-duplex mode. 17

Handling specific SPI signals. 17

4.3.1 Handling specific internal signals and interfaces . 17

4.3.2 Handling optional signals 18 .4 SPI instances with different features. 18

4.5 SPI synchronization between nodes. 19

# evision history 20

.ist of tables .22

.ist of figures. .23

# List of tables

Table 1. Main SPI features on STM32 devices . 3   
Table 2. Differences of CRC control between active SPI versions . 16   
Table 3. Document revision history . 20

# List of figures

Figure 1. Simplified data flow scheme . 5   
Figure 2. Timing of SPI data events and DMA transfer complete flags during a transfer. 6   
Figure 3. arawhin 10   
Figure 4. DMA late service of TXE/TXP event 13   
Figure 5. Examples of window available to perform specific control at the end of a transfer 15

# IMPORTANT NOTICE  READ CAREFULLY

products and/or to this document at any time without notice.

ST, the provisions of such contractual arrangement shall prevail.

T conditions of sale in place at the time of order acknowledgment.

T the purchasers' products.

No license, express or implied, to any intellectual property right is granted by ST herein.

segment, the purchasers shall contact ST for more information.

are the property of their respective owners.