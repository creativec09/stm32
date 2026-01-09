# Introduction to DMAMUX for STM32 MCUs

# Introduction

P trigger.

e channel. The application cannot freely map any peripheral request to any channel.

TA tl qute UX cguabutsi helMAtoledtroleA.

and provides guidance on the use of the new synchronization and request generation capabilities.

F

Table 1. Applicable products   

<table><tr><td rowspan=9 colspan=1>TypeMicrocontrollers</td><td rowspan=1 colspan=1>Product series</td></tr><tr><td rowspan=1 colspan=1>STM32C0 series</td></tr><tr><td rowspan=1 colspan=1>STM32G0 series</td></tr><tr><td rowspan=1 colspan=1>STM32G4 series</td></tr><tr><td rowspan=1 colspan=1>STM32H7 series</td></tr><tr><td rowspan=1 colspan=1>STM32L4+ series</td></tr><tr><td rowspan=1 colspan=1>STM32L5 series</td></tr><tr><td rowspan=1 colspan=1>STM32U0 series</td></tr><tr><td rowspan=1 colspan=1>STM32WB series</td></tr><tr><td rowspan=1 colspan=1>Microprocessors</td><td rowspan=1 colspan=1>STM32MP1 series</td></tr></table>

# 1 DMAMUX description

A perheral dicates  equest or DMA transr ysetting MA request igalTeDMArequest is di until it is served by the DMA controer hat generates a DMA acknowlege inal, and the correspondig DMA request signal is de-asserted.

In tocent, e cntrol sals equird or e DMA requestacknowle protool is ot eplicty described and it is referred to as peripheral DMA request line.

Th DMA equest routeran be considere as anextension  he DMA controller. It routeshe DMA pereal requests to the DMA controller itself.

The DMAMUX request multiplexer enables routing a DMA request line from the peripherals to the DMA croe  e prouct.Terutinction ssur by a proramablemulhanel DA reust multiplexer. ach channel (A channel  ihe example hown Figur)select aunique MA ruest lin  forward (unconditnally or synchronously to theassociated DMA controllerhannel (DMA channel ). Thi allows he DMA requss anaged wi hih fexibilityaxiizinghember DMA requ tha run concurrently.

![](images/22259f1d67319f96a5de80a9b7b8087917fd0c38ee97a30b5b388128f54eb482.jpg)  
Figure 1. DMAMUX request multiplexer   
Px Peripheral X request (example LPUART1_TX or LPUART1_RX)

# DMAMUX features

A siplif DA block diagram s hown inFigureThe Request multiplexerstructure sduplicat times, depending upon the number of DMA channels managed by the DMAMUX.

![](images/87f20f675bdee886c74715da015def72eb50b26cb2a06f8ede264abf0735b612.jpg)  
Figure 2. DMAMUX simplified block diagram

Note: Simplified block diagram with only one request multiplexer.

The DMAMUX is mainly composed of two components, the request multiplexer (or router block), and the request generator.

The request multiplexer includes a synchronization unit per channel, with inputs/outputs as follows:

Inputs:

dmamux_reqx: DMA request from a peripheral (dmamux_req_inx) or from the request generator (dmamux_req_genx)   
dmamux_req_gen[0..n] are affected, respectively, to dmamux_req[1..n+1], and dmamux_req_inx are affected starting from dmamux_req[n+2].   
dmamux_syncx: optional synchronization event

# Outputs:

dmamux_req_outx: DMA request dmamux_reqx forwarded from the input to the output dmamux_evtx: optional generated event, can be used to trigger/synchronize other DMAMUX channels

T qu ratol MAeuatitalve uutu :

Input: dmamux_trgx, trigger event inputs to the request generator sub-block   
Output: dmamux_req_genx, DMA request from the request generator sub-block to the DMAMUX request   
multiplexer channels

The number of request multiplexer blocks depends on the number of DMA channels managed by the DMAMUX.

For an 8-channel DMA, 8 request multiplexer channels must be available.   
For a product with two DMA controllers with 8 channels each, 16 request multiplexer channels must be available.

The request generator is instantiated once by DMAMuX. It contains N channels (depending on the prouct) calegenerating DMA requests.Reer he 'DMAMX implmentation' section n he produc reence manual for more details.

Thanks to the request generator block, the user software can trigger DMA transfers based on signals from peripherals that do not implement the DMA requests.

# 2.1

# Request routing and synchronization

# 2.1.1

# Unconditional request forwarding

T peform peripheral-to-memorymemory-to-peripheral transfers, the DMA controlchannel requir each time a peripheral DMA request line. When a request occurs, the DMA channel transfers data from/to the peripheral. The DMAMuX request multiplexer channel x allows the selection/routing of the peripheral DMA request line to the DMA channel x.

Whe eutex s t MAREQIDotqual  zros eaca uti MA st .Te coection peripheral MAequest hemultiplexerhannel utpulectehrough the prorame DMAREQ_ID bits of the channel control register (DMAMUX_CxCR).

For each peripheral DMA request line in the product, a unique ID is affected. The value zero (DMAREQ_ID = Ox00) corresponds to no DMA request line selected.

Aft he configuration a DMAMX hannel, e corresponding DMA controllehael an  configur Tw different DMAMUX channels cannot be configured to select the same peripheral DMA request line as source.

# 2.1.2 Conditional request forwarding

The synchronization unit allows the software to implement conditional request forwarding. The routing is eivelydone nly whedeficnditdetecthe MAtranse an e nronz wi or external signals.

F DMA request can be forwarded in one of the following ways:

each time an edge is detected on a GPIO pin (EXTI) in response to a periodic event from a timer in response to an asynchronous event from a peripheral in response to an event from another request router (request chaining)

Oizainaoatv other DMAMUX sub-blocks (such as the request generator or another DMAMUX request multiplexer channel).

![](images/d0927049001f5f668a4689d4f826624387db235adb55e77a04769986298df395.jpg)  
Figure 3. DMA request line multiplexer channel - Event generation

When a DMAMuX channel is configured in synchronous mode its behavior is as follows:

qut ultple t A est fome rhen bee tuiot ar the DMAMUX request multiplexer output until the synchronization signal is received.   
2. When the synchronization event s received the request multiplexer connects s input and output, and the pending peripheral request, if any, is forwarded.   
3. Each forwarded DMA request decrements the request multiplexer counter (user programmed value). When the counter reaches zero and the last forwarded request is acknowledged by the DMA controller, the connection between the DMA controller and the peripheral is disabled (not forwarded), waiting for a new synchronization event.

Fulpel asond DAX lThe same event can be used in somelow-power scenaris,  switch the system bac t Stop mode, without any CPU intervention.

Sroizatnodan uatially nroniatransoreaple wi trigger the transfers on a peripheral event.

T synchronization sigal (CID), the synchronization signal polarity (SOL) and theumber request to forward (NBREQ + 1) are configured in the request line multiplexer channel configuration register (DMAMUX_CxCR).

# 2.2

# Request generation

The request generator can be considered as an intermediary between a peripheral and the DMA controllers. It allows peripherals without DMA capability (such as RTC alarm or comparators) to generate a programmable A    ehe al SGDhe e ola he requests minus 1 to generate (GNBREQ) are configured in the request generator configuration register (DMAMUX_RGxCR).

Uponthe trigger event reception, the corresponding generator channel starts generating DMA requestsn it ouut. Each time the DMAMX generated request is served by the connected DMA controller, a built-n DMA request counter (one counter per request generator channel) is decremented.

At it underrun, the request generator channel sops generating DMA requests and the DMA request counter is automatically reloaded to its programmed value upon the next trigger event.

![](images/d6c8d1d1e0754c61dee1743181868cb89d35366be5ac6ec9b4a937fb0ccef609.jpg)  
Figure 4. DMA request generation

If a neigerven is eceiv whil hegenerato isaaginghe reviugee DArqus qe, then therequstger ven vern agb  isasserted y thearware he tatu MARGSR register.

# Request generation and synchronization

Ipecno a,A bl request generation and request synchronization feature within the same configuration.

# 3 DMAMUX examples

# Note:

These examples use the STM32CubeMX tool version 4.26.1, running on STM32 microcontrollers and microprocessors (based on Arm® cores).

Arm is a registered trademark of Arm Limited (or its subsidiaries) in the US and/or elsewhere.

# 3.1

# Example using the synchronization

After the configuration of the DMA channel to serve the peripheral DMA request line (example SPI6TX), the satblock canable howFigu Inh cas  ut al used to control the transfer periods.

![](images/41bfbab64e3776783861772701fa557719702a570351d897ebdf756e8e2a9f25.jpg)  
Figure 5. Example using the synchronization (based on STM32CubeH7)

# 3.2

# Example using the DMAMUX request generator sub-block

In order to have some automation, new DMA transfers can be generated following the DMA transfer to SPI6. Thanks to the DMAux Channel  event generation, the request generator can betriggered The scenari car be configured as shown in the figure below.

![](images/5f7e7bcb461c1a78c321b371707e322f7bd8767c131a7fa8353bfceac18d363a.jpg)  
Figure 6. Example using the request generator (based on STM32CubeH7)

# 3.3

# STM32CubeH7 examples

The following examples are available on the STM32CubeH7 under root "ProjectsISTM32H743l-EVAL\Examples\DMAI":

# DMAMUX_RequestGen

This example uses the EXTI0 line to trigger the DMAMUX request generator and to perform DMA data transers from the SRAM buffer to the GIOoutput data register, changing output pin state on everyEXTI rising edge occurrence.

![](images/0aca930c553ebf5792be8b0849d6483728e017e6619085dbe4ff9ce742a39421.jpg)  
Figure 7. DMAMUX_RequestGen

# DMAMUX_SYNC

This example uses the USART1 in DMA synchronized mode to send a countdown from 10 to 00 with 2 seconds period. The DMAMUX synchronization block is configured to synchronize the DMA transfer with the LPTIM1 output signal. Each rising edge of the synchronization signal (LPTIM1 output signal) authorizes four USART1 requests to be transmied to the USART1 peripheral using the DMA. These four requests represent the two characters 'Inr' plus the two characters count down itself from 10 to 00. L1 is configured to generate a PWM with 2 seconds period.

![](images/98e23b47e44464089c469eba46449d605f48dc64416ce1b1c7a9784f445d7a14.jpg)  
Figure 8. DMAMUX_SYNC

# 4 Conclusion

TheDAuX controller designe tosimpliy heallocationbeeapplication resources. Iff the flibiliallyealaAbilth sychronization mechanism that allowsee he from some tasks.he cmbination  synchronizatinan requst generation can be used toimplement poweroptimizd data transer n autonomous mode without CPU involvement).

# Revision history

Table 2. Document revision history   

<table><tr><td rowspan=1 colspan=1>Date</td><td rowspan=1 colspan=1>Version</td><td rowspan=1 colspan=1>Changes</td></tr><tr><td rowspan=1 colspan=1>16-Oct-2018</td><td rowspan=1 colspan=1>1</td><td rowspan=1 colspan=1>Initial release.</td></tr><tr><td rowspan=1 colspan=1>20-Nov-2018</td><td rowspan=1 colspan=1>2</td><td rowspan=1 colspan=1>Updated Table 1. Applicable products.</td></tr><tr><td rowspan=1 colspan=1>16-Jan-2019</td><td rowspan=1 colspan=1>3</td><td rowspan=1 colspan=1>Updated Section 3: DMAMUX examples.</td></tr><tr><td rowspan=1 colspan=1>8-Jun-2020</td><td rowspan=1 colspan=1>4</td><td rowspan=1 colspan=1>Updated Introduction with new products STM32G4, STM32L5, and STM32MP1 series.</td></tr><tr><td rowspan=1 colspan=1>09-Jan-2023</td><td rowspan=1 colspan=1>5</td><td rowspan=1 colspan=1>Updated Table 1. Applicable products.Minor text edits across the whole document.</td></tr><tr><td rowspan=1 colspan=1>15-Feb-2024</td><td rowspan=1 colspan=1>6</td><td rowspan=1 colspan=1>Updated document title.Document scope extended to STM32U0 series, hence updated Table 1. Applicable products.Updated Section 3.3: STM32CubeH7 examples.</td></tr></table>

# Contents

#

# 1 DMAMUX description

2 DMAMUX features 3

2.1 Request routing and synchronization. 2.1.1 Unconditional request forwarding 2.1.2 Conditional request forwarding   
2.2 Request generation. 6   
2.3 Request generation and synchronization. 6

# DMAMUX examples.

3.1 Example using the synchronization.   
3.2 Example using the DMAMUX request generator sub-block. 8   
3.3 STM32CubeH7 examples 9

# 4 Conclusion 10

Revision history 11

# List of figures

Figure 1. DMAMUX request multiplexer. 2   
Figure 2. DMAMUX simplified block diagram 3   
Figure 3. DMA request line multiplexer channel - Event generation. 4   
Figure 4. DMA request generation 6   
Figure 5. Example using the synchronization (based on STM32CubeH7). 7   
Figure 6. Example using the request generator (based on STM32CubeH7) 8   
Figure 7. DMAMUX_RequestGen. 9   
Figure 8. DMAMUX_SYNC 9

# IMPORTANT NOTICE  READ CAREFULLY

pt old ursant  dits   leole.

purchasers' products.

No license, express or implied, to any intellectual property right is granted by ST herein.

are the property of their respective owners.

I

© 2024 STMicroelectronics - All rights reserved