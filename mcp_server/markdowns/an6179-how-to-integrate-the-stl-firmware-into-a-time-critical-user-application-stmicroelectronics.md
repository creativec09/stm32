# How to integrate the STL firmware into a time critical user application

# Introduction

# 1 General information

Table 1. Referenced document   

<table><tr><td>N°</td><td>Description</td></tr><tr><td>[1]</td><td>STM32G4 series UL/CSA/IEC 60730-1/60335-1 self-test library user manual (UM3167)</td></tr></table>

# 2 Overview

The latest versions o STMicroelectronics afetyware packages use software self-est modulesfocud rotroleodus petalplatiec pi heatole ealvolaysk teplt masurements implemente inthe application hardwaredesign. Examplesinclue reference levels, comparion of redundant I/Os, and verification loopbacks. The STM32 family safety manuals and STL-associated documentation provide numerous methods and knowledge to manage this user-specific development.

W ttorTeeeien vall y diagnostic system capable ofdiscovering faults and errors that could potentially lead to dangerous system bavir beoy proagat srus ystem failue portn the eror cover diagnostic determines the system safety integrity level.

Users must understand that the coverage of these STL tests executed by software is limited due to the palhiereatveo tTiighe eyteriy vuseleoic pucmus aply sea stucturepliatindedeonent as dancy iciple ECC on memories, dual channels with comparators, and voters.

# 3 Interference of STL running at application

The software-based testing cycle flow is compiled from a sequence of tests programmed and configured via STL sheduler services. This L flow must coexist with other software handlig the application flow, ad any unexpecinteerenc between Lan aplicatinsotwaremust e ue Mos thee constraint areasily manageable f the user respects the instructins provided inthe TLuser guides. This docment focuses on demanding cases, where the interrupt masking window applied during execution of specific test modules such as RAM and TM7 ones at X-CUBE-CLASSB STL providing destructive operations upon the memory content (see more details at chapter Interrupt management at L user guides). This masking would inblio ra icant constraints nstacle ystes wi lmit peacepecally whenandngecritical processes.

Comonly, the STL fow can beexecuted as the lowest priority level task,llwing it to beinterrupteo s the upper part o Figure, which explains the effect o interrupt masking perormed by the L when the application executes gularinterrupt ervices without applyng ay ensationmethod Some servi ik t ell  e eal l e newors Tabate oan onai iuo p peoed byhe when theapliatin execues regular interrupt ervics without applying y ltnycompensating method.

Ce u y l executing the STL without additional control can result in some critical services not being executed at the so pall h   pli shown by the red services in the case B timing scheme in Figure 1.

A typical example is a motor control application where the motor control regulation (PWM) cycle must be uvy precisey withi given equidistant intervalsTe parameterac cycl eed te preou and programmed in advance based on measurements and calculations done in the preceding cycle. The most cal asccurs whesu plicatn operats ear este peoane mndoreu STL interrupt masking time consumes a significant part of the required control cycle duration.

The remaining sections of this document provide options for coping with these timing constraints in STL ital applying an efficient solution.

![](images/bc3a9b066f600661d3a9259b450228320443809094dd943c4349305750fc4341.jpg)  
Figure 1. Effect of interrupt masking performed by the STL

# Legend

Regular interrupt service executed correctly with no latency   
2. STL partial execution at main level   
3 Interrupt disable interval applied by STL   
4. Interrupt service executed with latency due to accidental collision with interval (3)

# How to compensate effects of the STL interrupt masking

Few possible methods how to deal with the STL interrupt masking are provided in this section.

# Assuming responsibility for all possible interferences and conflicts

This is the most challenging option when STL is compiled with the defined compilation parameter STLENABLE_IT, which suppresses allinterrupt maskng during STLexecution. In such case, user nees o e vey car whe eecutig modul hat wounorally aply henterrpt maskigA possleu can be to implement, for example, a RAM test on a part of the RAM that is currently not in use, while the apliationaril eceonother parheAM that deso vera wit es

# 4.2

# No concerns about interrupt latency

ScnUse ut eort analy whiguwae po th laencicli onarype ihaingrvisamur whe p requst arises during the previous serviceexecution, as shown in the case Btiming scheme in Section 3. An abllu anhettira tee at taskiisottUstn aneteplati wiant vead whe he atenc troduced byLacmonly margial compard e eecution pern time frames dedicated to the implemented tasks, and no immediate reaction of the system is required.

# 4.3

# Adaptable dummy Loop at start of critical interrupt

Thotitaleheee lutonnati nstivtc cost is performance loss at each entry to the service protected this way.The system waits in an adaptable sronizaty los egingterrpt  wh pvntingal y ranri ves lo interval than hemaxuinterrupt maskngte produed byL.Thetiming cheme s provin Figure 2. Snapshot of the associated code modification is visible at bottom of the figure.

![](images/eb7ff3fd35d1ff04b4eac92ff68f4e2a54c76b842d26d2caddcbaabfc7c99b02.jpg)  
Figure 2. Compensating interrupt latency with adaptable dummy Loop

Void HAL_TIM_PeriodElapsedCallback (TIM_HandleTypeDef \*htim) {   
If (htim->Instance == TIM1) { while (htim->Instance->CNT < GUARDING_LOOP_LENGTH) {} // wait Here, do anything after jtter has been taken out   
}   
Legend Due to that compensation, the service is always executed at regular equidistant intervals.   
2. STL partial execution at main level   
Interrupt disable interval applied by STL

# 4.4

# Guarding loop service protecting higher priority latency-critical interrupt entry

Thotmohiticat ieeeply al eowy o en etbcurl sTe suend theTLeecuion  advance prote cital servic entyeve the TLaplishe ongest askrar u owest ma evel collecn fow  eetsT guardig o servian execueapt operations that do ot applyany interrupt masking and involvedetection of the guarding service end Once ue nratailia

![](images/4c6f93cd19c15212b88e3ba93c5c5f88c3e91b59e9906a9bde66e6646b072cc9.jpg)  
Figure 3. Interrupt latency compensated by low-priority guarding loop

# Legend

Ruailinterup ve oy wit y   
2. STL partial execution at main level   
3. Interrupt disable interval applied by STL compensates occasional interval (3) occurrence   
5. End of the critical service releases the guarding loop interrupt and STL can continue at execution

# 5 Implementing latency-compensating guarding loop in motor control applications

Thi ectieostrateshetgration cncemotocontrol aplicationwi  guari compensating the latency of critical motor control interrupts. The exampleuses the P-NUCLEO-IHM03 pack, consisting of a NUCLEO-G431RB microcontroller board, an X-NUCLEO-IHM16M1 motor control expansion board, and a GBM2804H-100T motor. It showcases sensorless control of a PMDC motor using a three-shunt togydriver.igure  nd Figureilltrate he basoolgyheapl sies ad crent measurement on the motor winding shunts, while Figure 6 and Figure7 provide time schemes of the motor control process.

An efficient Lguarding looplementation e guremust ebased n detailting analysi e critial ervices within hemotor control cree nchroniz Ws control hemotor phase curretv atupautygurellmoS items 3 and 4 in Figure 6. The most time-critical service within the PWM period is the PWM computation prdure (6n igure), which calculates, plans, and preprograms all parameters and measurements  e M cycl om parameers re propagat inte capture compare egisters from thr preprograme gise heavear  ven for newly starting cycle.

The PWM computation process uses the latest available ADC measurement results (5 in Figure 6) and must be plebeore csusha e c p  cura done in time, benefiting from the applied hardware control associated with the timer update event. ADC cersi por lehutolmesensnieacrounauualltart midle of the PWM cycle.The specic shunts measured and the exact moment of ther measurement are redeterminedevery ped. I specic cases, the W coputation procedure nFigure)can plan diffent ADC conversion timingsrspeci hunt cobnationsor heext ccl to esue hemeasuremen ettl current values. The goal is to avoid measurements near expected switch changes, which can cause unstable a must be zero (See Figure 4 and Figure 5).

![](images/e4443313ba24ebce68a360ef6a66659d8f9de058d189fa6cdb90a623896dde46.jpg)  
Figure 4. Current flows through the shunt when the corresponding low-side switch is closed

![](images/3f386b63141842f85c5ff4176a97f3a374676caa53c662ba165148047f0455b0.jpg)  
Figure 5. Phase current measurement using shunt resistors and PwM duty cycles

Note:

Depending on the PWM duty cycles, the voltages on the shunt resistors are proportional to the phase currents after sure certain stabilization time (to avoid inverter switching that introduces a noise on shunts). Sum of all the currents then should be zero (la + Ib + Ic = 0), therefore two phase currents are measured at a time and remaining one is calculated.

Themost critial moment of the WM cycle s defined by he end of theADC conversion (5nFigure),which (CHighFrequencyTask). Figureextends some details f the Figure6 with focus on second hal f the WM Wl PWM cycle is defined by the sum of the ADC conversion and t interrupt service durations, which must e mae withi he secon half the WM cycl  the WM cycle  relatively sow andhe Lmaxum in Figure 7). However, f he STL maximum maskig tme could delay the end of the PWM computation service he  ccike ase  gu garg lo mus pnt honu iT ues hat eetio ar a nt im PWM computation procedure (6 in Figure 6) within the ongoing cycle. The STL can resume once the HighFrequencyTask is completed and so computation procedure of the next PWM cycle is done. Physically the guarding loop ends when interrupt service handling the HighFrequencyTask terminates (6 in Figure 6).

The guardng loo proceur prevent anycasinal iutin he ew WM cc planng byantu tu t he  he WM peraccountig r hemaxium Linterrupt isable nterval and e tme needed to complete the PWM computation service (6 in Figure 6) before the end of the ongoing cycle. This si poll speclease ag isered by heuserat hend  the nterupt serviandge HigFrequency task. Once detected, the guarding loopterinates, blocking heLexecutin process which can then resume at the main level.

T a never exceed half of the cycle duration.

Temeonol sk 8guans ctlm  u, a uuaru Iuuculav n process safety time.

To relax main level performance, users can consider executing light application tasks, such as some fast STL twigarg lopoih  poleardiat sifiantly.Users must avoid any interrupt masking at this level. All procedures and Tmodules reuirig masking must be executed exclusively at the lowest priority (main) level, guarded by the guarding loop implementation.

![](images/5de63bb29f201e112e5d1b0b9667793ddbd8475a1206f20333d65d511b55d92e.jpg)  
Figure 6. Guarding loop for critical interrupt latency in motor control

# Legend

1 Motor control background process   
2. STL partial execution at main level protected by guarding loop interrupt service routine   
3. Timer 1 channel 1-3 outputs (control of motor driver low-side switches)   
4. Timer 1 counter value (center-aligned PWM mode)   
5. ADC conversion of the selected shunt's voltage measurement (triggered by hardware)   
6. PWM planning, computation, and preprogramming procedure   
  
Medium-requenc motor control task (not synchronized with PWM ccle)   
9. STL partial execution cycle   
10.Maximum interrupt masking interval caused by STL   
11.Guarding loop interrupt service routine

![](images/b987ef9f3330b96dff4de96371e64a66a0cd4df299b73bd00082ec48b760451f.jpg)  
Figure 7. Time analysis of the single PWM cycle

Case I: Guarding loop must be applied as there is a potential danger that the PWM computation procedure should not be completed before the next PWM period starts at the most critical case

Case II: Guarding loop implementation is not necessary as the PWM computation procedure is always mangble iih ego  p ve pc  muntertski interval

# Timing analysis of motor control vs. available safety task time

An initial timing analysis must be done to consider the following criteria:

The necessity of any guarding loop implementation to prevent any timing conflicts as visible in Figure 7. The goal is to verify how the critical motor control processes fit into a single PWM period summarized at table 1 in Figure 8.   
The remaining performance budget available for STL overall execution management from a safety point of view. The estimation of time necessary to execute all the remaining motor control and application proceses gives some picture about the time remaining to handle the STLoveral flow cycle. See table in Figure 8.

The example is built on the STM32G4 MCU running at a frequency f 170 MHz while executing the motor control lc yal CMRAM er As detailed in the next chapter, users can measure and calculate that the three-shunt FOC motor can be exete reliably up toaproximately 38 kHzor such a coniguration.The limitig factor is the sum ADC conversion time (\~0.5 µs) and the execution of the ADC1_2_IRQHandler (\~12.7 µs), as both must be executed within the second half of the PWM cycle.

I w consier he maxiu interruptmaskig me appli by heTL library e [, he achievable WM freuenc would be reduce to approximately kHz to accommodate the possible increase interrupt rvice lr ol o latest possible entry t the AD_IRQHandler procedure, the safely achievable PWM frequency can return to the 38 kHz limit.

Theraehen cionhvlablelaiplati p i ow v ihe L he ma evel .%al MCU performance buget, whic i mostly available during the rst hal of the WM peri See table Figure 8.

Thevalues and fequencies are precalculated wit aconservativeapproach since heduration the PWM computation procedure (FOC_HighFrequencyTask called from the ADC1_2_IRQHandler) can slightly vary dependingnhemotor staus.The wors-casescenarimeasureat motrarup was considere Move, the critical part of the PWM computation procedure ends slightly before the ADC1_2_IRQHandler terminates. Thereore,ven better results (W fequency up  0 zan e ahive i moor control, while  all . Hove, h evalableMCU pans fian u \~%) e WM cyc 20 µs in this case.

Bp themodules eexecuteonceover he teste areas. For example  code are should b te flash via the hardware CRC unit and a 160 KB code area in RAM, allthe tests should be executed within an interval approximately 6s, base on dat adapted from table  n theuser manual User can the alcuahat  con eMCU   yL anare finished below \~140 ms (38 kHz) or \~320 ms (50 kHz) if considering the performance budget available for STL, iavnhat  puee a ivablpliatieibutionlplcation icludipliation m eptnru DMA transfers, which is the case with the STM32G4.

Morove ilaplatn casseoot testevehentange withi igle parts, in atomic steps during runtime, to split the MCU performance equally among other low-level tasks. Repeition  theatomic ses onsume bit more MCU perorane.Usua hese part SLmemoy s ml  eplengl heh ttulesl hecu i eal pleveheuow aratomic es apliand the periodicity theexecution Nevertheless, the calculated rmeas verifed time of the overall STL cycle execution should not exceed the process safety time defined by the application safety task.

a calculated with conservative approach (PWM peformed at 37,9 kHz by Cortex-M4running o170 MHz fromflash)   

<table><tr><td rowspan=1 colspan=1>Process</td><td rowspan=1 colspan=1>Trigger</td><td rowspan=1 colspan=1>Service/Event</td><td rowspan=1 colspan=1>Priority</td><td rowspan=1 colspan=1>Duration[us]</td><td rowspan=1 colspan=1>Contribution at themin PWM cycle [%]</td></tr><tr><td rowspan=1 colspan=1>ADC configuration</td><td rowspan=1 colspan=1>TIM1 update</td><td rowspan=1 colspan=1>TIM1_IRQHandler</td><td rowspan=1 colspan=1>Highest (0)</td><td rowspan=1 colspan=1>0,6</td><td rowspan=1 colspan=1>2.3</td></tr><tr><td rowspan=1 colspan=1>ADC conversion</td><td rowspan=1 colspan=1>TIM1 Ch4 CC</td><td rowspan=1 colspan=1>ADC1_2_IRQHandler</td><td rowspan=1 colspan=1>NA</td><td rowspan=1 colspan=1>0,5*</td><td rowspan=1 colspan=1>NA</td></tr><tr><td rowspan=1 colspan=1>ADC1_2_IRQHandler</td><td rowspan=1 colspan=1>End of ADC conversion</td><td rowspan=1 colspan=1>FOC_HighFrequencyTask*</td><td rowspan=1 colspan=1>High (2)</td><td rowspan=1 colspan=1>12,7*</td><td rowspan=1 colspan=1>48,1</td></tr><tr><td rowspan=1 colspan=1>Guarding loop</td><td rowspan=1 colspan=1>TIMx CC</td><td rowspan=1 colspan=1>TIMx_CC_IRQHandler</td><td rowspan=1 colspan=1>Low (7)</td><td rowspan=1 colspan=1>4</td><td rowspan=1 colspan=1>15,2</td></tr><tr><td rowspan=1 colspan=1>STL partial execution andother processes</td><td rowspan=1 colspan=1>NA</td><td rowspan=1 colspan=1>NA</td><td rowspan=1 colspan=1>Depends on processmain for STL)</td><td rowspan=1 colspan=1>9.1</td><td rowspan=1 colspan=1>34,5</td></tr></table>

\*) Must fit within half of the PWM period (\~50% of the PWM cycle) \*\*) PWM computation procedure taking significant part of the ADC1_2_IRQHandler

Tanalyamplpliati pocovelnrutiontiaur single STL complete cycle within the available performance budget   

<table><tr><td rowspan=1 colspan=1>Process</td><td rowspan=1 colspan=1>Trigger</td><td rowspan=1 colspan=1>Service/Event</td><td rowspan=1 colspan=1>Priority</td><td rowspan=1 colspan=1>Duration /period [us]</td><td rowspan=1 colspan=1>MCU performancecontribution [%]</td></tr><tr><td rowspan=1 colspan=1>PWM cycle control + guarding</td><td rowspan=1 colspan=1></td><td rowspan=1 colspan=1></td><td rowspan=1 colspan=1>Different</td><td rowspan=1 colspan=1>NA</td><td rowspan=1 colspan=1>65,5</td></tr><tr><td rowspan=1 colspan=1>Medium frequency MC task</td><td rowspan=1 colspan=1>Systick</td><td rowspan=1 colspan=1>Systick_IRQHandler</td><td rowspan=1 colspan=1>Middle (4)</td><td rowspan=1 colspan=1>7.6 / 500</td><td rowspan=1 colspan=1>1.5</td></tr><tr><td rowspan=1 colspan=1>Application interrupts</td><td rowspan=1 colspan=1>NA</td><td rowspan=1 colspan=1>NA</td><td rowspan=1 colspan=1>NA</td><td rowspan=1 colspan=1>NA</td><td rowspan=1 colspan=1>0</td></tr><tr><td rowspan=1 colspan=1>Application DMA</td><td rowspan=1 colspan=1>NA</td><td rowspan=1 colspan=1>NA</td><td rowspan=1 colspan=1>NA</td><td rowspan=1 colspan=1>NA</td><td rowspan=1 colspan=1>0</td></tr><tr><td rowspan=1 colspan=1>Application flow</td><td rowspan=1 colspan=1>NA</td><td rowspan=1 colspan=1>NA</td><td rowspan=1 colspan=1>Lowest (main)</td><td rowspan=1 colspan=1>NA</td><td rowspan=1 colspan=1>0</td></tr><tr><td rowspan=1 colspan=1>STL complete cycle</td><td rowspan=1 colspan=1>NA</td><td rowspan=1 colspan=1>NA</td><td rowspan=1 colspan=1>Lowest (main)</td><td rowspan=1 colspan=1>46000/NA</td><td rowspan=1 colspan=1>33,0</td></tr></table>

# Steps to integrate STL into a simple MCSDK project

The MCSDK project used in the STL integration example associated with this document was made by the following steps:

Tow il reference and describe the stepsused tocreate the included example project. For usage istructions e MCSDK, refer to the MCSDK documentation.

# Create a simple MCSDK project

Motor control workbench (version 6.3.0 used here)

Create a new project:

Number of motors: 1 motor   
Driving algorithm: FOC (Field-Oriented control)   
Hardware mode: Pack   
Select hardware: P-NUCLEO-IHM03   
P frequency: Set to a conservative or higher value (for example, 50 kHz to test the system behavior   
near its limits) Navigate to "PWM generation" block -> Config -> PWM frequency (in Hz) -> OK

2Save the project: Save the project to a suitable location.

Generate the project:

Project generation settings:

o STM32CubeMX version: 6.12.0 used o Preferred target toolchain: Select your preferred toolchain o Firmware package version: FW V1.6.0 (as recommended) o Drive type: HAL (default)

Click on Generate.

Note: Generating the MC workbench project also runs CubeMX project generation. There is no need to open or change the CubeMX project at this point.

# IDE project

Open the generated project: Open the generated project in your IDE of choice.

Modify the main. c file:

Defe thevarable:Defiehefolloigvariablemaket global and volatileo that it canbemofd   
by the debugger):   
volatile float programmed_speed_f = 150.0;   
Add code in while (1) Loop: Add the following code into the main application while (1) loop in   
main() (within the /\* USER CODE BEGIN WHILE \*/ block):   
MCI_State_t MciState = MC_GetSTMStateMotor1();   
if (MciState == FAULT_OVER) { MC_AcknowledgeFaultMotorl();   
if (MciState == IDLE) MC_ProgramSpeedRampMotorl_F(programmed_speed_f, 5000); MC_StartMotorl();

Build and run he projec: Now, build and run he proje.he motor should start runnig at 0 RPMany speed set by the debugger before starting or restarting the motor.

Note:

When changing parameters in MCSDK up to version 6.3.0, the PWM frequency and regenerating the project, as this causes theriveparameters. file to be generated with incorrect parameters. This issue has been fixed in the version 6.3.1. A workaround for earlier versions of MCSDK is to generate the project from the eoy npacheyveiteeprmfwi from a freshly generated separate project.

In principle, ther iso need o regenerate themotor control workbench project. The userneeds to apply he following changes to the already generated STM32CubeMX project and associated IDE configuration only.

Perform the following steps to add the STL library to the MCSDK project:

Copy the Middlewares directory from the STL into the project directory structure on the file system   
Perform the following modifications at IDE configuration: STM32CubeIDE

Create a folder Middlewares/ST/STM32_Safety_STL in the project structure and link the stl_user_param_template.c and stl_util.c files into this folder.

In the Project → Properties → C/C++ General → Paths and Symbols window of the project:

In the Library Paths tab, add ../Middlewares/ST/STM32_Safety_STL/Lib.

In the Includes tab, add ../Middlewares/ST/STM32_Safety_STL/Inc.

In the linker file (STM32G431RBTX_FLASH.1d):

Add the folowing section between .finiarray and .data (necessary for RAM STL tests): backup_buffer_section (NOLOAD): { \*(backup_buffer_section) } >RAM

# EWARM

Create a folder Middlewares/ST/STM32_Safety_STL in the project structure and link the stl_user_param_template.c and stl_util.c files into this folder.

# In Project → Options:

o In C/C++ Compiler → Preprocessor → Additional include directories, add the new directory: \$PROJ_DIR\$/../Middlewares/ST/STM32_Safety_STL/Inc In Linker → Library → Additional libraries, add the new library: \$PROJ_DIR\$/../Middlewares/ST/STM32_Safety_STL/Lib/STL_Lib.a

In the linker file (stm32g431xx_flash.icf), replace the following line: place in RAM_region { readwrite, block CSTACK, block HEAP

with the following two lines:

define block FIXED_ORDER_RAM with fixed order { section backup_buffer_section, readwrite, block CsTACK, block   
HEAP };   
place in RAM_region { block FIXED_ORDER_RAM };

# Keil MDK

Create a folder Middlewares/ST/STM32_Safety_STL in the project structure and link the stl_user_param_template.c, stl_util.c, and sTL_Lib.a files into this folder.

Right-click on STI_Lib. a file, choose Options for File, and change File Type to Object file

Change the following project options:

0 In the Target tab, select Use default compiler version 6 in the Code Generation -> ARM Compiler subwindow.   
o In the C/C++ (AC6) tab, uncheck the Short enums/wchar tick box and add../Middlewares/ST/STM32_Safety_STL/Inc to the Include Path.   
o In the Linker tab, uncheck the Use Memory Layout from Target Dialog tick box.   
o In the Linker tab, open the Scatter File via the Edit button and insert the line \* (backup_buffer_section) at the start of the RAM section.   
o Change the .sct file location to the root of the Keil® project (recommended).

3Perform the following modifications in STM32CubeMX:

In Project Manager → Code Generator → Generated files tab:

o Uncheck Delete previously generated files when not regenerated.   
o Check Backup previously generated files when regenerating (recommended).

In the Pinout & Configuration tab:

In the Timers tab, set up the following parameters for TIM4:

Clock Source: internal clock   
Prescaler: ((TIM_CLOCK_DIVIDER) - 1) (change "Decimal" to "No Check")   
Counter Mode: Up   
Counter Period: (guarding_delay) (change "Decimal" to "No Check")

In System Core → NVIC tab:

In the NVIC subtab, enable TIM4 global interrupt and set Preemption Priority to 7. In the Code generation subtab, uncheck the Call HAL handler column for TIM4 global interrupt.

Generate the code

4. Perform the next modifications at application main.c file here.

# At the beginning of the file

#include "stl_user_api.h" // include header file with STL API definitions   
volatile int guarding_delay = 1000; // define debugger tunable variables, values to be tweaked later   
volatile int STL_activate = O;

# Before the main loop body entry

LL_TIM_SetOnePulseMode(TIM4, LL_TIM_ONEPULSEMODE_SINGLE);// enable TIM4 one-pulse   
mode HAL_TIM_CLEAR_IT(&htim4, TIM_IT_UPDATE); HAL_TIM_ENABLE_IT(&htim4, TIM_IT_UPDATE);   
STL_SCH_Init(); // call STL scheduler initialization

# Within the main loop body

if (STL_activate != O) { // conditional insertion of the STL flow (here TM7 is   
called exclusively) STL_TmStatus_t StlTmStatus = STL_NOT_TESTED; STL_Status_t¯StlStatus = STL_SCH_RunCpuTM7(&StlTmStatus); if (StlTmStatus != STL_PASSED ||¯StlStatus != STL_OK) { // fail, add error handler entry here }   
}

# 5. Perform next modifications at application stm32g4xx_mc_it.c here:

# At the beginning of the file

extern volatile int Mc_hi_f_task_done; // global variable declaration - to   
signalize guarding loop end, variable is defined in stm32g4xx_it.c   
volatile int wait_loop_hi_f_enabled = 1; // to control enable and disable the   
guarding loop while debugging   
extern volatile int guarding_delay; // to control the guarding loop timing while   
debugging   
extern TIM_HandleTypeDef htim4; // to control TIM4

# At the end of ADC1_2_IRQHandler ("USER CODE BEGIN HighFreq" block)

MC_hi_f_task_done = 1; /1 guarding loop can terminate (placed at the end of ADCl_2_IRQHandler "USER CODE BEGIN HighFreq" block)

# At the start of TIMx_UP_M1_IRQHandler ("USER CODE BEGIN TIMx_UP_M1_IRQn O" block)

if (wait_loop_hi_f_enabled) guarding loop control at the start of   
TIMx_UP_M1_IRQHandler ("USER CODE BEGIN TIMx_UP_M1_IRQn O" block) int¯x = guarding_delay - TIM1->CNT; // subtract TIM1 value from guarding delay   
to compensate ISR entry latency if (x > 0) { TIM4->ARR = x; else { TIM4->ARR = 0; } TIM4->CNT = 0; NVIC_ClearPendingIRQ(TIM4_IRQn); _HAL_TIM_CLEAR_IT(&htim4, TIM_IT_UPDATE); TIM4->CR1¯|= TIM_CR1_CEN;

6.Perform next modifications at application stm32g4xx_it.c file here:

# At the beginning of the file

volatile int Mc_hi_f_task_done = O; // global variable declaration extern volatile int wait_loop_hi_f_enabled;

# At the beginning of TIM4_IRQHandler()

if (TIM4->SR & TIM_SR_UIF) _HAL_TIM_CLEAR_IT(&htim4, TIM_IT_UPDATE);   
MC_hi_f_task_done = 0;   
while¯(wait_loop_hi_f_enabled && !MC_hi_f_task_done) { if (!(TIM1->DIER & TIM_DIER_UIE)) { // Motor control timer IR cycle stopped, break out: break; }   
}

# Build and debug the project

u thevariable usig he debugeraweweakng heguardng looptimig b hangighe guarigeay variable. Note that the TL fow is reduced in the shown code snippets.The TM7 moduleis c plua the eai dule or howe andng upt oheouls.Te flow must be adapted by the end user. Refer to the project examples delivered with the STL lirary.

# Setup to observe and measure the PWM cycle parameters

Users can implement a specific setup to measure the critical processes within the WM loop. This could be amut  prevent ay nepec jmotor cntrol  teerenTebes methoservi al the following GPIOs:

PC5: TIM1 CH4N signal (used for ADC measurement) to trigger a stable signal for the oscilloscope.   
Set and reset when the TIM1 update interrupt is entered and exited to measure the highest priority task duration (7 in Figure 6).   
P Set and reset when the high-frequency task or its critical part is entered and exited (6 in Figure .   
PC12: Signals that the guarding loop is active or interrupted.

# CubeMX setup:

At Pinout & Configuration → Timers → TIM1 → Mode, change Channel 4 Mode from PWM Generation no output to PWM Generation CH4N.

At Pinout & Configuration → Timers → TIM1 → Parameter Settings.

ChangeCounter Period from ((PWM_PERIOD_CYCLES) / 2) tO ((PWM_PERIOD_CYCLES) / 2 + 1) to ensure a nonzero width pulse.   
At PWM Generation Channel 4 → Mode, change the PWM back to mode 2 (note that   
reconfiguration of CH4 reverts it to mode 1).

At Pinout & Configuration → Timers → TIM1 → GPIO Settings, change PC5 GPIO speed to Medium.

At Pinout view, change PC12, PC11, and PC10 modes to GPIO Output.

• Regenerate the CubeMX project.

# Application code modification:

nert thefollowig ne  he befoe he main body loop enty (block SER ODE BEGI TIM1->CCER |= TIM_CCER_CC4NE; // enable TIM1 CH4N output signal

2Place the following lines in stm32g4xx_it.c at the beginning and end of TIM4_IRQHandler: GPIOC->BSRR = 1<<12; // at the beginning GPIOC->BRR = 1<<12; // at the end

3.Place the following lines in stm32g4xx_mc_it.c:

At the beginning and end of ADC1_2_IRQHand1er (blocks USER CODE BEGIN ADC1_2_IRQn 0 and   
1):   
GPIOC->BSRR = 1<<11; // at the beginning   
GPIOC->BRR = 1<<11; // at the end

At the beginning and end of TIMx_UP_M1_IRQHandler (blocks USER CODE BEGIN TIMx_UP_M1_iRQn 0 and 1):

GPIOC->BSRR = 1<<10; // at the beginning GPIOC->BRR = 1<<10; // at the end

# Oscilloscope setup for timing requirement measurement:

Use an oscilloscope with infinite persistence enabled.   
Trigger off PC10 (TIM1 update interrupt).   
Place cursor_1 exactly on the PC5 (TIM1 CH4N) pulse (when stable, that is, no deviation is happening).   
Clear the persistence memory.   
Leave running for a long enough time.   
Place cursor_2 on the latest recorded falling edge of PC11 (HighFrequencyTask).

measurement on a project with a low enough PWM frequency o that there is no dangerof ISRs interfering with the measurements (for example, 20 kHz) and with STL not running (clean project).

The highequency ask takeheongest tmeterval when emoto tartgMake urehat ure r RPM whi oo  r Atavel e ehih-euy task nly I h case, e tglemust e plain he the block USER CODE BEGIN HighFrequencyTask SINGLEDRIVE_2.

At the rest of this chapter user can find a few snapshots taken during measurement of the P-NUCLEO-IHM03 pack applied for control of the GBM2804H-100T motor.

Motor stable state at PWM frequency 20 kHz [1]

The motor already started up.   
STL activity is disabled. No guarding loop is applied.

![](images/b066ec6f29910d2e67758b52eb25c412af3047d0f3464112a8c6411980d3d68d.jpg)  
Figure 9. Timing of motor control tasks during normal operation

Motor startup with PWM frequency of 20 kHz [1]

High-frequency task takes the longest. Its start can be deviated in time too.   
The moment of its worst-case can be measured from the center of the PWM pulse.   
STL activity is disabled. No guarding loop is applied.

![](images/0ee324ab5390c9b84068bc84bd02000a729f77042952b01e6720ddadff86c2bb.jpg)  
Figure 10. Timing of motor control tasks during motor startup

Motor stable state with PWM frequency of 20 kHz [2]

STL is running, with interrupt masking enabled, and the guarding loop is disabled.   
Interrupt masking causes jitter on the high-frequency task.

![](images/4bfea493b69de6bb40f25df62f5aa4a87ee76b36325701d35a516fc2eec7da9a.jpg)  
Figure 11. Timing of motor control tasks during normal operation with STL enable

Motor stable state at PWM frequency 20 kHz [2]

Jitter on the high-frequency task disappears. Its execution slot is protected by a low-level guarding interrupt service preventing any interrupt masking there.

Jitter observed on the TIM1_update task execution signals that the task is not protected by the guarding The loop is released by the high-requency task. In this case, it protection is not necessary as it does not take up a significant portion of the half-cycle.

Jitter can be observed on guarding loop entry, as well as occasional longer pulses when the guarding loop gets interrupted by the SysTick handler.

![](images/647e2bfb3b464c84d361aad5b180efcfc2a455640fee71cd7344b7bbdcd2a71f.jpg)  
Figure 12. Timing of motor control tasks during normal operation with STL enabled but guarded

# Motor stable state at critical PWM frequency 50 kHz [2]

This figure shows a case where the critical partof the high-requency task still gets executed before the TIM update event. It stillfits into the second half PWM cycle. Even though its entire execution time stretches into the next PWM cycle begin, the motor control stil functions well if the guarding loop is used. As a result of this extreme case, ittle execution time is left for the main task. Signs of task starvation by the guarding loop or higher priority interrupts can be observed.

![](images/ee40fb209cec066e50baba56c358f68cc7fe3f3fd824b51d3cd029c22ea6d1e1.jpg)  
Figure 13. Timing of motor control tasks with STL active but guarded at nearly maximum possible PWM frequency

Triggered off PC10 (TIM1_update task) Triggered off PC5 (TIM1_ch4N)

# Revision history

Table 2. Document revision history   

<table><tr><td>Date</td><td>Revision</td><td>Changes</td></tr><tr><td>27-Nov-2024</td><td>1</td><td>Initial release.</td></tr></table>

# Contents

2 Overview 3

3 Interference of STL running at application. 4

# 4 How to compensate effects of the STL interrupt masking.

4.1 Assuming responsibility for all possible interferences and conflicts .5   
4.2 No concerns about interrupt latency. .5   
4.3 Adaptable dummy Loop at start of critical interrupt. 5   
4.4 Guarding loop service protecting higher priority latency-critical interrupt entry. 6

Implementing latency-compensating guarding loop in motor control applications ..7

Timing analysis of motor control vs. available safety task time 11

Steps to integrate STL into a simple MCSDK project. 13

3 Setup to observe and measure the PWM cycle parameters 17

# Revision history .21

# List of tables 23

List of figures. .24

# List of tables

Table 1. Referenced document 2   
Table 2. Document revision history . 21

# List of figures

Figure 1. Effect of interrupt masking performed by the STL 4   
Figure 2. Compensating interrupt latency with adaptable dummy Loop 5   
Figure 3. Interrupt latency compensated by low-priority guarding loop. 6   
Figure 4. Current flows through the shunt when the corresponding low-side switch is closed 7   
Figure 5. Phase current measurement using shunt resistors and PWM duty cycles . 8   
Figure 6. Guarding loop for critical interrupt latency in motor control 9   
Figure 7. Time analysis of the single PWM cycle 10   
Figure 8. Time analysis comparison 12   
Figure 9. Timing of motor control tasks during normal operation 18   
Figure 10. Timing of motor control tasks during motor startup. 18   
Figure 11. Timing of motor control tasks during normal operation with STL enabled 19   
Figure 12. Timing of motor control tasks during normal operation with STL enabled but guarded 19   
Figure 13. Tming  motor control tasks with Tactive but guarded at nearly maximum possible WM frequenc

# IMPORTANT NOTICE  READ CAREFULLY

pt old ursant  dits   leole.

purchasers' products.

No license, express or implied, to any intellectual property right is granted by ST herein.

are the property of their respective owners.

I

© 2024 STMicroelectronics - All rights reserved