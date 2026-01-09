# How to use the CORDIC to perform mathematical functions on STM32 MCUs

# Introduction

products.

particular trigonometric and hyperbolic functions, compared to a software implementation.

conversions between rectangular (x, y) and angular (amplitude, phase) coordinates.

ppltioncihoRIcerat worktoln compared with an equivalent software implementation.

C examples run on the NUCLEO-G474RE board.

Table 1. Applicable products   

<table><tr><td>Type</td><td>Products</td></tr><tr><td rowspan="5">Microcontrollers</td><td>STM32G4 series</td></tr><tr><td>STM32U5 series</td></tr><tr><td>STM32H7R3/7S3 product line</td></tr><tr><td>STM32H7R7/7S7 product line</td></tr><tr><td>STM32H563/573 product line</td></tr><tr><td rowspan="4"></td><td>STM32H723/733 product line</td></tr><tr><td>STM32H725/735 product line</td></tr><tr><td>STM32H730 value line</td></tr><tr><td></td></tr></table>

# 1 General information

The STM32CubeG4 MCU package runs on STM32G4 series microcontrollers, based on Arm® Cortex®-M4 processors.

# Note:

Arm is a registered trademark of Arm Limited (or its subsidiaries) in the US and/or elsewhere.

# arm

# 2 CORDIC introduction

The CORDIC (coordinate rotation digital computer) is a low-cost successive approximation algorithm for evaluating trigonometric and hyperbolic functions.

Originally presented by Jack Volder in 1959, it was widely used in early calculators.

I throh decreasing angles tan() (n =0,, until thecumulative sumfthe otation angles equale iu angleThe  andcartesin coponent  he rotatd vecor then correspon pectively the ad sine f .This is illustrated in Figur or an angle of 0.Thevector undergos a scaling by1. (\~1.65) over the course of the calculation.

![](images/481ca60e79e3f1e950c0a4a39b128ff4e242e8ecf1ad78e6faeac9d37457ddb6.jpg)  
Figure 1. CORDIC circular mode operation

I g corresponding to the arctangent (y/x).

TRIalo an l s lclatiypebolicisca) y plac circular rotations by hyperbolic angles tanh-1(2-i) (j = 1, 2, 3..), see Figure 2.

T atural arel senvepolgetafomy

![](images/5f832096ec7248bc80ccdd5cb6fca4883aec5376478230b75dcc169007004625.jpg)

Tl Wcula CORDIC also calculates (cosh² t - sinh² t) as a by-product. So, the square root is obtained from:

![](images/a84b40f89f8815f2dd57b77ee810ed249e242efbec371dbade1255c1f79db9b4.jpg)

Additional functions are calculated from the above using the following appropriate identities:

![](images/37dd39df4cc776b2717660b41c54a1e03357c9cae32ca0bcbf132787d369b475.jpg)

![](images/87ffc8ce17984182135e5da309b7cf80ab8f162acb1d29dfb684bcbddf3591fb.jpg)

The CORDIC algorithm lend tsef tohardwareimplementation since thereare omultiplications involv e fi scaling factor .s prelode. Only add and shit operations are perored.This lsomeans tat it is ideally suited to integer arithmetic.

![](images/77483112e1b0c99019b58adfeea530aaeac05a691344d774b1120c38a23cc629.jpg)  
Figure 2. CORDIC hyperbolic mode operation

# 2.1

# Limitations

In circular mode, the CORDIC converges fora angles in the range  toradians. The use of fixed point ulsg multiplied by 1/πt and output angles must be multiplied by  to convert back to radians.

Themodulus must  e ange whetherconvertin fo polar rectangularrectangular . Tens hat phas .1. gvs aleesus inceemodulus sange nsaturate CORDIC engine, even if only the phase is needed.

I= fi point umeicrange. Hence, theCORDIC withou aditinal scaling spports values x = cosh(t) in e ra to  ha , . oerdiviin ywhic ceons o theyeolangleaniee range 0 to 1.317 (cosh-1 2).

It ssiblecealaow ORaovg as j tends to infinity, the sum of |δtjl tends to 1.118:

![](images/cc963b50bcac190a726c8536784f05c8dd54f672ab4c0f858eb3afc767cc67b0.jpg)

This is illustrated in Figure 3.

![](images/6e931a6f41196145dd791d1f4d8de83fe057a7e421708c0033249b963f1fdc15.jpg)  
Figure 3. Hyperbolic convergence limit

aiallhaRi functions coshf() and sinhf().

T tanh 1.118 = 0.806.

As previously stated, the natural log uses the identity:

![](images/638b6b0f41f282098ad1f2ee62bd6a16e721767688976acc741a7c92eaa96862.jpg)

Since the limit for the atanh input magnitude is 0.806, then:

![](images/0046bbb93d41b71169b541c56ef23147970b4e9039d18337e2388a0c40ba5f57.jpg)

of 2, such that 2-n.(x+1) < 1, to avoid overflowing the fixed point numerical format.

given by:

![](images/e37e82f84c094f5796c046feb3b7a0f2100a78d3d6c43849f0f621acb5ee6d18.jpg)

the expression:

![](images/5cfee131870c9770bcf0beee4d313e5a7d1a414311d54dc4877b9a4f5c19cff7.jpg)

Hence, x ≤ 2.34. Again, scaling must be applied such that 2-n.(x+0.25) < 1 to avoid saturation.

# 2.2 Convergence rate and precision

Incircular mode, he CORDICalgorithm converges at arate o 1binary digit per iteration. This means that 16 nsuihi eseauachievabl psiihe ne hei wehebsi R ol 16-bit and 32-bit input and output data, and has an internal precision of 24 bits.

Fgur hos he at convegence or eCRDn crcularmode.Te curv abel . aTca   ee Wh theaxiu eidual eraache he mit bi reision  = 1. 1, he qantz es cangult   ean ecr attsho CORDICegicnti nvegor -t tsheuantizatin erorheCORDICegie, wicseant  anstns sat e zeo n mocvec poss.Tea ial er hsx0 corresponds to 19-bit precision.

Iol rular u v n ateta ngpltwicte gencot a  eeue oemoaall  eegi the same between iteration 4 and 5. Therefore, the CORDIC takes two more iterations to achieve the same precision in hyperbolic mode than in circular mode.

q onoe  ol functios.

![](images/9975fb089d0b808431b4af5a14dbbfd04281db1904c12ca2a1536db7cd2b5ba5.jpg)  
Figure 4. CORDIC convergence (circular mode)

![](images/56f9c79580ec478e5825b034af97559538a8b4ee547bed1d6a6568afc03b7214.jpg)  
Figure 5. CORDIC convergence (hyperbolic mode)

# 3 Code examples and performance

# 3.1

# Acceleration example: one-off calculation in software

ThCORDICuni isdesigne primarily acceleratethe evaluationmathematical expressions compare to equivalent function from a software library such as math.h.

An example program is in the STM32CubeG4 MCU Package, under \Projects\NUCLEO-G474RE|Examples_LLICORDICICORDIC_CosSin. This example performs a polar to rectangular conversion escep cduses ow vehicas vehehanHA driver. Executing the function comprises three steps:

# Configure the CORDIC:

LL_CORDIC_Config(CORDIC,   
LL_CORDIC_FUNCTION_COSINE, /\* cosine function \*/   
LL_CORDIC_PRECISION_6CYCLES, /\* max precision for q1.31 cosine \*/   
LL_CORDIC_SCALE_0, /\* no scale \*/   
LL_CORDIC_NBWRITE_1, /\* One input data: angle. Second input data (modulus) is 1 af   
ter cordic reset \*/   
LL_CORDIC_NBREAD_2, /\* Two output data: cosine, then sine \*/   
LL_CORDIC_INSIZE_32BITS, /\* q1.31 format for input data \*/   
LL_CORDIC_OUTSIZE_32BITS); /\* q1.31 format for output data \*/

z time one of the above parameters changes.

Write the input argument(s):

/\* Write angle \* LL_CORDIC_WriteData(CORDIC, ANGLE_CORDIC);

In case, there  nly earguent,he ngle defie   constant value/8). Theotherrguent is the default modulus of 1, so does not need to be written.   
As soon as the expected number of arguments is written, the calculation starts.

# Read the result(s):

/\* Read cosine \* /   
cosOutput = (int32_t)LL_CORDIC_ReadData(CORDIC); /\* Read sine \*/   
sinOutput = (int32_t)LL_CORDIC_ReadData(CORDIC);

There are two results expected. Since the output format is 32-bit, two reads are necessary. Not that o poll teutpu ready girequihes read nycoplees when heult is available.

# 3.1.1

# Measuring the execution time

The usercan measure the number procesor cycles required to execute steps2 and 3 above by comparing the STick"counter value before and afer.The SysTick counter decrements each procesor clock cycle. In he ST2Cubehe valueheime is eadusing he pointrSTick-VALSmeashetime heSTc conter read medately before writin theargument  the CORDIC nd agamediately terreadi he results:

/\* Read systick counter \*/   
start_ticks = SysTick->VAL;   
/\* Write angle \*/   
LL_CORDIC_WriteData(CORDIC, ANGLE_CORDIC);   
/\*¯Read cosine \*/   
cosOutput = (int32_t)LL_CORDIC_ReadData(CORDIC); /\* Read sine \*/   
sinOutput = (int32_t)LL_CORDIC_ReadData(CORDIC); /\* Read systick counter\~\*/   
stop_ticks = SysTick->VAL;   
/\* Calculate number of cycles elapsed \*/   
elapsed_ticks = start_ticks-stop_ticks;

number of cycles taken to calculate the sine and cosine is the difference between the two count val

# Note:

TSTcly h   kvl For short measurement periods however this is not likely to occur.   
Il ignored.

# 3.1.2 Performance comparison

The following performance figures (Table ) are obtained using the NUCLEO-G474RE, with the Cortex®-M4F running at 170 MHz from flash (with the ART cache enabled). The CORDIC executes at the same clock freuency. The code is compiled using the IAR Embedded Workbench IDE for Arm, v8.30.1. The optimization is set to high for speed and for size.

Table 2. Execution time versus software for polar to rectangular conversion   

<table><tr><td rowspan=1 colspan=1>Function used to calculate sine and cosine</td><td rowspan=1 colspan=1>CPU cycles(optimized forspeed</td><td rowspan=1 colspan=1>CPU cycles(optimized for size)</td></tr><tr><td rowspan=1 colspan=1>CORDIC in zero overhead mode (32-bit integer)</td><td rowspan=1 colspan=1>29</td><td rowspan=1 colspan=1>29</td></tr><tr><td rowspan=1 colspan=1>CORDIC in zero overhead mode with conversion from single precision floating-point to 32-bitinteger and back</td><td rowspan=1 colspan=1>79</td><td rowspan=1 colspan=1>82</td></tr><tr><td rowspan=1 colspan=1>math.h single precision floating-point functions:float sinf(float), float cosf(float)</td><td rowspan=1 colspan=1>416</td><td rowspan=1 colspan=1>416</td></tr><tr><td rowspan=1 colspan=1>arm_math.h DSP library 32-bit fixed point function: arm_sin_cos_q31(q31_t, q31_t*, q31_t*)</td><td rowspan=1 colspan=1>742</td><td rowspan=1 colspan=1>733</td></tr><tr><td rowspan=1 colspan=1>arm_math.h DSP library 32-bit floating-point function: arm_sin_cos_f32(float32_t, float32_,f float32*)</td><td rowspan=1 colspan=1>405</td><td rowspan=1 colspan=1>413</td></tr><tr><td rowspan=1 colspan=1>math.h double precision floating-point functions:double sin(double), double cos(double)</td><td rowspan=1 colspan=1>4036</td><td rowspan=1 colspan=1>4053</td></tr></table>

The gures clearlydemonstrateheadvantagehe CORDIC or polar rectangularconversions.Copar to the Arm DSP library function in q31 fixed point, the CORDIC uses less than 4% of the CPU cycles. Even ter with heconvrsionfom fati-point nteerand back, eCORDCus leshan 20% f CPU cycles used by the single-precision Arm DSP library function or math.h functions. The double precision measurements are o reference. None o the otheroptions, including th CORDIC, achieves double precision accuracy but the cost in cycles on a processor such as the Cortex®-M4 is much lower.

Table 3 shows the comparison for some of the other functions supported by the CORDIC.

Table 3. Execution time versus software for other functions   

<table><tr><td colspan="1" rowspan="1">Function</td><td colspan="1" rowspan="1">CPU cycles(optimized for speed)</td><td colspan="1" rowspan="1">CPU cycles(optimized for size)</td></tr><tr><td colspan="2" rowspan="1">Rectangular to polar conversion, atan2(y,x)</td><td colspan="1" rowspan="1"></td></tr><tr><td colspan="1" rowspan="1">CORDIC in zero overhead mode</td><td colspan="1" rowspan="1">33</td><td colspan="1" rowspan="1">25</td></tr><tr><td colspan="1" rowspan="1">CORDIC in zero overhead mode with conversion from single precision floating-point to 32-bit integer and back</td><td colspan="1" rowspan="1">107</td><td colspan="1" rowspan="1">111</td></tr><tr><td colspan="1" rowspan="1">math.h single precision floating-point function:float atan2f(float, float)</td><td colspan="1" rowspan="1">332</td><td colspan="1" rowspan="1">325</td></tr><tr><td colspan="1" rowspan="1">math.h double precision floating-point function:double atan2(double, double)</td><td colspan="1" rowspan="1">4194</td><td colspan="1" rowspan="1">4209</td></tr><tr><td colspan="1" rowspan="1">Exponent, exp(x)</td><td colspan="1" rowspan="1"></td><td colspan="1" rowspan="1"></td></tr><tr><td colspan="1" rowspan="1">CORDIC in zero overhead mode (sinh + cosh)</td><td colspan="1" rowspan="1">39</td><td colspan="1" rowspan="1">39</td></tr><tr><td colspan="1" rowspan="1">CORDIC in zero overhead mode with conversion from single precision floating-point to 32-bit integer and back</td><td colspan="1" rowspan="1">81</td><td colspan="1" rowspan="1">81</td></tr><tr><td colspan="1" rowspan="1">math sige precision floating-point function:float expf(float)</td><td colspan="1" rowspan="1">319</td><td colspan="1" rowspan="1">322</td></tr><tr><td colspan="1" rowspan="1">math.h double precision floating-point function:double exp(double)</td><td colspan="1" rowspan="1">3604</td><td colspan="1" rowspan="1">3608</td></tr><tr><td colspan="1" rowspan="1">Natural logarithm, In(x)</td><td colspan="1" rowspan="1"></td><td colspan="1" rowspan="1"></td></tr><tr><td colspan="1" rowspan="1">CORDIC in zero overhead mode</td><td colspan="1" rowspan="1">27</td><td colspan="1" rowspan="1">26</td></tr><tr><td colspan="1" rowspan="1">CRDze  t bit integer and back</td><td colspan="1" rowspan="1">61</td><td colspan="1" rowspan="1">61</td></tr><tr><td colspan="1" rowspan="1">math.h single precision floating-point function:float Inf(float)</td><td colspan="1" rowspan="1">260</td><td colspan="1" rowspan="1">256</td></tr><tr><td colspan="1" rowspan="1">math.h double precision floating-point function:double log(double)</td><td colspan="1" rowspan="1">2744</td><td colspan="1" rowspan="1">2740</td></tr><tr><td colspan="1" rowspan="1">Square root, sqrt(x)</td><td colspan="1" rowspan="1"></td><td colspan="1" rowspan="1"></td></tr><tr><td colspan="1" rowspan="1">CORDIC in zero overhead mode</td><td colspan="1" rowspan="1">23</td><td colspan="1" rowspan="1">21</td></tr><tr><td colspan="1" rowspan="1">CORDIC in zero overhead mode with conversion from single precision floating-point to 32-bit integer and back</td><td colspan="1" rowspan="1">53</td><td colspan="1" rowspan="1">52</td></tr><tr><td colspan="1" rowspan="1">math. sigle precision foating-point uncion:float sqrtf(float)</td><td colspan="1" rowspan="1">58</td><td colspan="1" rowspan="1">74</td></tr><tr><td colspan="1" rowspan="1">arm_math.h DSP library 32-bit fixed point function: arm_sqrt_q31(q31_t, q31_t)</td><td colspan="1" rowspan="1">313</td><td colspan="1" rowspan="1">313</td></tr><tr><td colspan="1" rowspan="1">arm_math.h DSP library 32-bit floating-point function: arm_sqrt_f32(float32_t, float32_t*)</td><td colspan="1" rowspan="1">57</td><td colspan="1" rowspan="1">57</td></tr><tr><td colspan="1" rowspan="1">math.h double precision floating-point function:double sqrt(double)</td><td colspan="1" rowspan="1">814</td><td colspan="1" rowspan="1">814</td></tr></table>

![](images/e3b07185b083a33c400a23bb83338e74821aa7456f78f6d25c73f9edb1211f01.jpg)  
Figure 6. Summary of CORDIC performance versus software

The above measurements (without the double precision result) are summarize in FigureThe CORDI gves a significant speedup or all supportenctions when fied point orinteger ritheticis used. For sgle -pot-o® en between floating-point and integer more or less cancels the advantage of the CORDIC.

Nohat eR peors he alculatns   clock ccr e square otTeainig are used up accessing the memory and the CORDIC registers. This can vary depending on the compiler vpu rectangular conversion using the CORDIC in integer mode drops from 29 to 17 cycles.

# Acceleration example: multiple data using DMA

Another usef the CORDIC unit i to perform repetitive calculations on multiple data.An example is in the STM32CubeG4 MCU package, under \Projects|NUCLEO-G474RE|ExamplesICORDICICORDIC_Sin_DMA. This epcnvert vecornges towave putanuput at estoreinmeory DMA controller can handle ll the transfers between memory and the CORDIC.The processor thus plays o part in the operation, apart from initializing the CORDIC unit.

Ti eapleses he HALivr liz he CORDICand he DMA.his as o effec n he po since the software does not intervene in the actual calculation and data transfer to and from memory.

ARDee gurm  ecgent anu (both 32-bit integers) are required. The precision is again set to six cycles:

/\*## Configure the CoRDIC peripheral ####################################\*/   
sCordicConfig.Function = CORDIC_FUNCTION_SINE; /\* sine function \*/sCordicConfig.Precision = C ORDIC_PRECISION_6CYCLES; /\* max¯precision for q1.31 sine \*/   
sCordicConfig.Scale = CORDIC_SCALE_O; /\* no scale \*/   
sCordicConfig.NbWrite = CORDIC_NBWRITE_1; /\* One input data: angle.   
Second input data (modulus) is¯1 after¯cordic reset \*/   
sCordicConfig.NbRead = CORDIC_NBREAD_1; /\* One output data: sine\*/   
sCordicConfig.InSize = CORDIC_INSIZE_32BITS; /\* q1.31 format for input data \*/   
sCordicConfig.OutSize = CORDIC_OUTSIZE_32BITS; /\* q1.31 format for output data \*/if (HAL_CORD IC_Configure(&hcordic, &sCordicConfig)¯!= HAL_OK)   
/\* Configuration Error \*/   
Error_Handler();

# A DMA channel is configured to transfer data from memory to the CORDIC:

/\* CORDIC_WRITE Init \*/ hdma_cordic_write.Instance = DMAl_Channel1;   
hdma_cordic_write.Init.Request = DMA_REQUEST_CORDIC_WRITE;   
hdma_cordic_write.Init.Direction = DMA_MEMORY_TO_PERIPH;   
hdma_cordic_write.Init.PeriphInc = DMA_PINC_DISABLE;   
hdma_cordic_write.Init.MemInc = DMA_MINC_ENABLE;   
hdma_cordic_write.Init.PeriphDataAlignment = DMA_PDATAALIGN_WORD;   
hdma_cordic_write.Init.MemDataAlignment = DMA_MDATAALIGN_WORD;   
hdma_cordic_write.Init.Mode = DMA_NORMAL;   
hdma_cordic_write.Init.Priority = DMA_PRIORITY_LOW;   
if (HAL_DMA_Init(&hdma_cordic_write) = HAL_OK) Error_Handler();

# A second channel is configured to transfer data from the CORDIC to memory:

/\* CORDIC_READ Init \*/ hdma_cordic_read.Instance = DMAl_Channel2;   
hdma_cordic_read.Init.Request = DMA_REQUEST_CORDIC_READ;   
hdma_cordic_read.Init.Direction = DMA_PERIPH_TO_MEMORY;   
hdma_cordic_read.Init.PeriphInc = DMA_PINC_DISABLE;   
hdma_cordic_read.Init.MemInc = DMA_MINC_ENABLE;   
hdma_cordic_read.Init.PeriphDataAlignment = DMA_PDATAALIGN_WORD;   
hdma_cordic_read.Init.MemDataAlignment = DMA_MDATAALIGN_WORD;   
hdma_cordic_read.Init.Mode = DMA_NORMAL;   
hdma_cordic_read.Init.Priority =¯DMA_PRIORITY_LOW;   
if (HAL_DMA_Init(&hdma_cordic_read) = HAL_OK) Error_Handler();

# The CORDIC is started with the HAL_CORDIC_Start_DMA() function:

/\*## Start calculation of sines in DMA mode #################### if (HAL_CORDIC_Calculate_DMA(&hcordic, aAngles, aCalculatedSin, ARRAY_SIZE, CORDIC_DMA_DIR_IN_OUT) != HAL_OK)   
Error_Handler();

The CORDIC generates a DMA request on its write channel (DMA channel 1), upon which the DMA controller fe  valu from hetablenglememoy nt32Angles[ARRAYSIZE]andwri into heCORDIC WTva transfer of the second angle value.

Wh ORDIc u RATAi generates a DMA request n he read chanel (DMAchannel The DMA controller reads he result and wriet theesult table, it32CalculateSin[ARRAYSIZE]Theacedi heRDATAegiseiger ahih continues until all 64 entries in the table have been processed.

PMAei aORD hMA the read request. Thus, the CORDiC operates at close to maximum speed.

ore DMAtranscomplenterrupt, eleaseORD procs.heumbeycles take  s angn tThde e the begining and enf the lop. To be more accurate, the second SyTick read must e performed oeny into the DMA transfer complete interrupt handler.

In tiexample  total  cycles equir  proes valeThicoreons  verage. pervalSce ORDIC ca pr valu i cloc cycle clear hat DMA elu previous example one calculation at a time.

# 3.3

# Optimal performance

To ahive the maximum theoretical perormance from the CORDIC, he softwar must perform the transer o data from thememory  the CORDC and back, instead of the DMAThe followig code replaces thecall to HAL_CORDIC_Calculate_DMA() in the previous example:

\* Write first angle to cordic \*   
CORDIC->WDATA = aAngles[0];   
'\* Write remaining angles and read sine results \*   
for(uint32_t i = 0; i < ARRAY_SIZE; i++) { CORDIC->WDATA = aAngles[i]; \*pCalculatedSin++ = CORDIC->RDATA;   
/\* Read last result \*/   
\*pCalculatedSin = CORDIC->RDATA;

# where \*pCalculatedSin is a pointer to the start of aCalculatedSin[]:

/\* Array of calculated sines in Q1.31 format \* static int32_t aCalculatedSin[ARRAY_SIZE]; /\* Pointer to start of array \*/ int32_t \*pCalculatedSin = aCalculatedSin;

ohal  e CORDIC is never idle waiting for a new argument.

Wit theabove code, a bufferARRAYSIZE= 3024values  processe in 4261cycles,corresponding ve cc valotceegi ha R the result into the RDATA register. Hence, the CORDIC is operating at maximum throughput.

# 4 Conclusion

TCORDIC a nificant speed-ponmericandyperbolicunctions, a we  atural epnent compared to software implementations. The biggest gains areobtained when working in theative f point frat.Thisvoid hecostcversion from n fatig-point. everheles art fe Thiatonhl duceeop eygo suc  he parandheve par used in motor control applications.

T s ppeuti vl pari contiuouslyvariablefrequency oe generatior waveform synthes. a maximu speeis requi he the proceor, and ee uphe prceo time o hertasks, then he DMA conroller isusedo servie CORDIC, with little loss of performance.

Writ oftware or he CORDICs mplepecl usig hencns ndmaos provide by he HAL Lriversn 32CuHowever aremust  aken not exce hemeal limit hen whc may require additional software checks if not specified by design - not tested in production.

# Revision history

Table 4. Document revision history   

<table><tr><td rowspan=1 colspan=1>Date</td><td rowspan=1 colspan=1>Revision</td><td rowspan=2 colspan=1>ChangesInitial release.</td></tr><tr><td rowspan=1 colspan=1>23-May-2019</td><td rowspan=1 colspan=1>1</td></tr><tr><td rowspan=1 colspan=1>11-Mar-2021</td><td rowspan=1 colspan=1>2</td><td rowspan=1 colspan=1>Updated:•    Section 2: CORDIC introduction.Table 3. Execution time versus software for other functions.Section 3.2: Acceleration example: multiple data using DMA.</td></tr><tr><td rowspan=1 colspan=1>6-Jul-2022</td><td rowspan=1 colspan=1>3</td><td rowspan=1 colspan=1>Updated Section Introduction</td></tr><tr><td rowspan=1 colspan=1>28-Sep-2022</td><td rowspan=1 colspan=1>4</td><td rowspan=1 colspan=1>Updated /* Write first angle to cordic */ CORDIC-&gt;WDATA = aAngles[0]; /* Write remaining anglesand read sine results */ for(uint32_t i= 0; i &lt; ARRAY_SIZE; i++) { CORDIC-&gt;WDATA = aAngles[i]j;*pCalculatedSin++ = CORDIC-&gt;RDATA; }/* Read last result */ *pCalculatedSin = CORDIC-RDATA;Replaced &quot;BLOCKSIZE&quot; with &quot;ARRAY_SIZE&quot;</td></tr><tr><td rowspan=1 colspan=1>27-Feb-2023</td><td rowspan=1 colspan=1>5</td><td rowspan=1 colspan=1>Changed title of the documentAdded STM32H563/573 product line in Table 1. Applicable products</td></tr><tr><td rowspan=1 colspan=1>07-Mar-2024</td><td rowspan=1 colspan=1>6</td><td rowspan=1 colspan=1>Added STM32H7Rx/Sx products in Table 1. Applicable products</td></tr></table>

# Contents

# 1 General information

2 CORDIC introduction 3

2.1 Limitations 4   
2.2 Convergence rate and precision 6

# Code examples and performance 8

3.1 Acceleration example: one-off calculation in software 8

3.1.1 Measuring the execution time . 9   
3.1.2 Performance comparison 10

3.2 Acceleration example: multiple data using DMA. 12

3.3 Optimal performance 14

# 1 Conclusion. 15

Revision history 16

List of tables 18

List of figures. 19

# List of tables

Table 1. Applicable products 1   
Table 2. Execution time versus software for polar to rectangular conversion 10   
Table 3. Execution time versus software for other functions . 10   
Table 4. Document revision history . 16

# List of figures

Figure 1. CORDIC circular mode operation 3   
Figure 2. CORDIC hyperbolic mode operation 4   
Figure 3. Hyperbolic convergence limit 5   
Figure 4. CORDIC convergence (circular mode). 6   
Figure 5. CORDIC convergence (hyperbolic mode).   
Figure 6. Summary of CORDIC performance versus software 11

# IMPORTANT NOTICE  READ CAREFULLY

pt old ursant  dits   leole.

purchasers' products.

No license, express or implied, to any intellectual property right is granted by ST herein.

are the property of their respective owners.

I

© 2024 STMicroelectronics - All rights reserved