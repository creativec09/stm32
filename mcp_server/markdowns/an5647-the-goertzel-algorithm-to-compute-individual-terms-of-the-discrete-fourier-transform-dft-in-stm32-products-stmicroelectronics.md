# The Goertzel algorithm to compute individual terms of the discrete Fourier transform (DFT) in STM32 products

# Introduction

T STM32 products.

o on the FFT is also included for verification.

The Goertzel algorithm is generalized to the non-integer frequency index case.

lAB test signal and perform floating point decoding. A fixed-point C implementation is also provided.

# General information

# Note:

This document applies to the Arm®-based devices.   
Arm is a registered trademark of Arm Limited (or its subsidiaries) in the US and/or elsewhere.

# arm

# 1.1 Reference documents

DT0085 Coordinate rotation digital computer algorithm (CORDIC) test and performance verification   
DT087 Coordinate rotation digital computer algorithm (CORDIC) to compute trigonometric and hyperbolic   
functions   
DT0088 FIR filter design by sampling, windowing and modulating the sinc() function   
DB2956 SensorTile development kit   
DB2854 Wearable sensor unit reference design for fast time to market

# 2 The Goertzel algorithm

A   pi int tuie t FT)y( =   W(nk) x(n he angom -anheic W( ise as exp (-j 2 π/N t).

T  W= ee W (k (n-N)) x(n). The sum can be unfolded and manipulated to make it recursive:

y(k) = W(-k) x(N-1) + W(-2k) x(N-2) + W(-3k) x(N-3) + . + W(-k(N-1)) x(1) + W(-k N) x(0)

y(k) = W(-k) [x(N-1) + W(-k) x(N-2) + W(-2k) x(N-3) + . + W(-k(N-2)) x(1) + W(-k(N-1)) x(0) ] y(k) = W(-k) [x(N-1) + W( -k) [x(N-2) + W( -k) x(N-3) + .. + W(-k(N-3)) x(1) + W(-k(N-2)) x(0) ]] y(k) = W(-k) [x(N-1) + W( -k) [x(N-2) + W( -k) [x(N-3) + .. + W(-k(N-4)) x(1) + W(-k(N-3)) x(0) ]]]

I yn(k) = W(-k) [ x(n) + yn-1(k) ], where n goes from 0 to N-1, yo(k) = 0.

T ru n. I i pssblealathecefficnt e at euatil numbers, except for the last step where the final complex output yn-1(k) is computed.

The recursive formula in z-domain is:

![](images/954697b4e701a2bcde7c06796bcdc52afdc0bd852504a25c855de28e6e3cada3.jpg)

Therefore the filter transfer function is:

![](images/a9a75b50df92b90660cdfd22c563ce581c28a39455c75e04c534e900003a4b07.jpg)

There is o change the umerator and the denominatoraemultiplied by he same quantity 1  W() ).

![](images/351750a3f810d9ff90000f96a6842aef1c681325db7b3c6550c53567d64b7421.jpg)

I fp multplatntc puitin to compute the real and the imaginary part of the output y(k).

Figure 1. Direct Il form for H(z) = (W - z − 1) / (1 - cz - 1 + z - 2), W = exp (j 2π/N k), c = 2cos(2π/N k)

![](images/a5a70a13607465a27c2a7d97f1d1d360ef50835b53c379547ff80d650fccda7b.jpg)

# 2.1

# Goertzel algorithm implementation

Theollakv a peuhent -.Thereal part is returne n I (in-phase) and the aginary part is eturned in Qquadrature-pase).

function [I,Q] = goertzel(x,k,N) W = 2\*pi\*k/N; CW = cos(w); c = 2\*cw; SW = sin(w); z1=0; z2=0; % init for n = 1 : N z0 = x(n) + c\*z1 − z2; z2 = z1; z1 = z0; end; It = cw\*z1 - z2; Qt = sw\*z1; I = real(It) - imag(Qt); % I = It for real x because imag(Qt)=0 Q = imag(It) + real(Qt); % Q = Qt for real x because imag(It)=0

# 2.2

# Goertzel as an lIR filter

Twcn u upan hon boHe Gze is implemented as an IIR filter.

function [I,Q] = goertzelIIR(x,k,N) W = exp(1i\*2\*pi\*k/N); c = 2\*cos(2\*pi\*k/N); b = [W -1 0]; % FIR coefficients a = [1 -c 1]; % IIR coefficients   
y = filter(b, a, x); I = real(y(end)); Q = imag(y(end));

# 2.3

# Goertzel as the k-th coefficient of an N-point FFT

Tollnc tu mu epihonbov He z is implemented as an FFT whose k-th coefficient is extracted.

function [I,Q] = goertzelFFT(x,k,N) y = fft(x); I = real(y(k+1)); Q = imag(y(k+1));

# 2.4

# Generalized Goertzel for k index not-integer

The Goertzel algorithm can be generalized to handle the case where the k index is not an integer. The cuatihe on eon eus hahe output.

Note:

The magnitude of the output is changed.

function [I,Q] = goertzelgen(x,k,N) w = 2\*pi\*k/N; CW = cos(w); c = 2\*cw; SW = sin(w); z1=0; z2=0; % init for n = 1 : N z0 = x(n) + c\*z1 − z2; z2 = z1; z1 = z0; end; It = cw\*z1 − z2; Qt = sw\*z1; w2 = 2\*pi\*k; cW2 = cos(w2); sw2 = sin(w2); I = It\*cw2 + Qt \*sw2; Q = -It\*sw2 + Qt\*cw2;

# 2.5

# Generalized Goertzel equivalence to IQ demodulation

The generalized Goertzel algorithm is equivalent to IQdemodulation. For an N-point FFT, the frequency bn c n =k/, s eaae mixer. The time vector is n\*1/Fs, n = 0 to N-1.

function [I,Q] = IQmixer(x,k,N) a = 2\*pi\*k/N\*[0:N-1]; c = cos(a); % in-phase carrier s = -sin(a); % quadrature carrier I = sum(x.\*c); Q = sum(x.\*s);   
end

# 2.6

# Test for Goertzel algorithm implementations

Te following script an beused  tet he Goertzel algorithm mplementations presente abovThe coputd numbers must be equal as indicated in the comments.

N = 64; % FFT length   
x = randn(1,N) + 1i\*randn(1,N); % random data kf = rand(1)\*(N-1); % k with fractional part k = round(kf); % integer index to FFT coeff [I1,Q1] = goertzelC(x,k,N);   
[I2,Q2] = goertzelIIR(x,k,N);   
[I3,Q3] = goertzelFFT(x,k,N);   
disp([I1 I2 I3]); % all equal   
disp([Q1 Q2 Q3]); % all equal   
[I4,Q4] = goertzelgen(x,kf,N);   
[I5,Q5] = IQmixer(x,kf,N);   
disp([I4 I5]); % all equal   
disp([Q4 Q5]); % all equal

# 2.7

# Goertzel error bounds

TG al near 0 or near N-. There is also a dependency on the input signal (.. a damped sinusoid may cause larer as ε x 104.

# 3 Application example: DTMF dual-tone multi-frequency signaling

Theual-neultequec naling Fhas been develope by heBel ytem  heUnit Stat Is rzo t  he in the keypad of telephones.

Table 1. Dual-tone multi-frequency (DTMF)   

<table><tr><td rowspan=1 colspan=1>Frequencies</td><td rowspan=1 colspan=1>1209 Hz</td><td rowspan=1 colspan=1>1336 Hz</td><td rowspan=1 colspan=1>1477 Hz</td><td rowspan=1 colspan=1>1633 Hz</td></tr><tr><td rowspan=1 colspan=1>697 Hz</td><td rowspan=1 colspan=1>1</td><td rowspan=1 colspan=1>2</td><td rowspan=1 colspan=1>3</td><td rowspan=1 colspan=1>A</td></tr><tr><td rowspan=1 colspan=1>770 Hz</td><td rowspan=1 colspan=1>4</td><td rowspan=1 colspan=1>5</td><td rowspan=1 colspan=1>6</td><td rowspan=1 colspan=1>B</td></tr><tr><td rowspan=1 colspan=1>852 Hz</td><td rowspan=1 colspan=1>7</td><td rowspan=1 colspan=1>8</td><td rowspan=1 colspan=1>9</td><td rowspan=1 colspan=1>C</td></tr><tr><td rowspan=1 colspan=1>941 Hz</td><td rowspan=1 colspan=1>*</td><td rowspan=1 colspan=1>0</td><td rowspan=1 colspan=1>#</td><td rowspan=1 colspan=1>D</td></tr></table>

Wheneve button  prese,  tones regnerated wit he equencyindicaten thecoepondingw n tG present in the signal.

# DTMF encoding and decoding, MATLAB script

In ol rtepl     s   0 vy 0 set of frequency coefficients is available. The minimum symbol duration is then N/Fs = 50 ms.

All psibl yols nceuratiasmbolnly lechereom 1.   
As the duration is variable, on the output some symbols may appear twice.

T  ha an Because of the quantization noise, on the output some symbols may be missing.

In tede heblock smple swioweusigHaig windw hanc hesnaonois t blttb tolu not decoded and a blank space is printed instead.

% DTMF test, dual-tone multi-frequency   
frow = [ 697, 770, 852, 941]; % frequencies for 1st tone   
fcol = [1209, 1336, 1477, 1633]; % frequencies for 2nd tone   
sym = ['1', '4', '7', '\*', '2', '5', '8', '0', ……. % SYMbOls '3', '6' 'g', '#' 'A', 'B' 'C′, 'D′];   
symrow = [1 2 3 4 1 2 3 4 1 2 3 4 1 2 3 4]; % 1st tone for given symbol   
symcol = [1 1 1 1 2 2 2 2 3 3 3 3 4 4 4 4]; % 2nd tone for given symbol   
symmtx = [1 59 13; 2, 6, 10, 14; 3, 7, 11, 15; 4, 8, 12, 16]; % decoding matrix   
Fs = 4000; % Hz, sampling frequency   
N = 200; % minimum number of samples per symbol   
x = []; % create test signal   
symoutref = []; % reference for decoded output   
for i=1:length(sym), % test each symbol Nsym = N + round(N/2\*rand(1)); % samples for current symbol t = [0:Nsym-1]/Fs; % time vector x1 = sin(2\*pi\*frow(symrow(i))\*t); % first tone x2 = sin(2\*pi\*fcol(symcol(i))\*t); % second tone x = [x, x1+x2]; symoutref = [symoutref, sym(i)];   
end; bits = 8;   
Q = (max(x)-min(x))/(2^bits); % quantization step for 8 bit signal x = round(x/Q); % some noise may also be added

fbin=Fs/N; % Goertzel frequency resolution, N must be high enough k=round([frow fcol]/fbin); % N high enough so that k is different for each tone if any(diff(k)==0), fprintf('same k index for different tones!\n'); return; end;

%% Goertzel-based DTMF decoding   
xblocks = floor(length(x)/N);   
myspec = []; % zeros(xblocks,length(k));   
for i = 1 : xblocks, i1 = (i-1)\*N+1; i2 = i1+N-1; xt = x(i1:i2); xt = xt.\*hamming(N)'; for j = 1 : length(k), [I,Q] = goertzel(xt,k(j),N); myspec(i,j) = sqrt(I\*I+Q\*Q); end;   
end;   
th = max(myspec(:))/2; % threshold   
myspecbin = myspec>th; % tone on/off detection   
symout = [];   
for i = 1 : xblocks, i1 = find(myspecbin(i,1:4)>0); if length(i1)\~=1, i1=0; end; % 1st tone i2 = find(myspecbin(i,5:8)>0); if length(i2)\~=1, i2=0; end; % 2nd tone if (i1==0) il (i2==0), symdec=' '; % no symbol decoded else symdec=sym(symmtx(il,i2)); % symbol decoded end; symout = [symout, symdec]; % append decoded symbol   
end;

% printout and plot fprintf('reference string: %s\n',symoutref); fprintf('decoded string: %s\n',symout);

figure; imagesc(fbin\*k/1000,[0:xblocks]\*N/Fs\*1000,myspec);   
axis xy; axis([0 Fs/2/1000 0 length(x)/Fs\*1000]); colorbar;   
xlabel('Frequency (kHz)'); ylabel('Time (ms)');   
title(sprintf('DTMF test, %d-bit Fs=%.1f kHz, %d-point Goertzel',bits,Fs/1000,N)); figure; imagesc(fbin\*k/1000,[0:xblocks]\*N/Fs\*1000,myspecbin);   
axis xy; axis([0 Fs/2/1000 0 length(x)/Fs\*1000]); colorbar;   
xlabel('Frequency (kHz)'); ylabel('Time (ms)');   
title(sprintf('DTMF test, %d-bit Fs=%.1f kHz, %d-point Goertzel, th=%1.f',bits,Fs/ 1000,N,th)); NFFT=128; NOVL=round(0.9\*NFFT); WIN=hamming(NFFT);   
figure; spectrogram(x,WIN,NOVL,NFFT,Fs);   
title(sprintf('DTMF test, %d-bit Fs=%.1f kHz, %d-points FFT',bits,Fs/1000,NFFT));

%% save quantized test signal to file to test C implementation h=fopen('in.txt','wt'); fprintf(h,'%d\n',x); fclose(h);

The script plots the spectrogram of the generated signal (Figure ), as well as the frequency coefficients Gzeu gfntbovol iv

![](images/67a1c7a64cb301885f301c184b487c0329a408028cca21c899a10ea16e0d5970.jpg)  
Figure 2. Spectrogram of the generated test signal

![](images/98a8a4b7c9fcc0cf43c0a2af68e597adb9dbcd5b74fcb7315cb11aaee34e7160.jpg)  
Figure 3. Frequency coefficients computed by the Goertzel algorithm

![](images/62664e53d2c538a9250d1190d62c228803330dc99199ef9528c120744ab4bb72.jpg)  
Figure 4. Frequency coefficients above threshold   
The MATLAB output for a typical run is the following:

reference string: 147\*2580369#ABCD decoded string: 147\*\*25800369 #ABBCD

#

# DTMF encoding and decoding, fixed-point C

The following C program performs the DTMF decoding using the Goertzel algorithm. The first argument on the A nt pevi ctTehgen he an ih plieqenc  Hzhe Gl during the decoding process.

The coputation  the Goertzel constant is base nsiand cos(These functions can e mplementi fixed-point using the CORDIC algorithm.

# Note:

For more informations about CORDIC algorithm refer to DT0087.

In the program the squared magnitude is computed, therefore a squared threshold must be used or decoding. Tmagnitud an lo becputeandusehe rtfnction must plementefiepoint use CORDIC algorithm.

#include <stdio.h> #include <stdlib.h> #include <math.h> #define MAXN 1000

// DTMF frequencies int frow[4] = { 697, 770, 852, 941 }; // 1st tone int fcol[4] = { 1209, 1336, 1477, 1633 }; // 2nd tone

DTMF decoding matrix int symmtx[4][4] = { { 0, 4, 8, 12 }, { 1, 5, 9, 13 }, { 2, 6, 10, 14 }, { 3, 7, 11, 15 } };

int win[MAXN]; // Window

Goertzel   
int c[8], CW[8], SW[8]; 7 Goertzel constants   
int z1[8], Z2[8]; Goertzel status registers   
int I[8], Q[8], M2[8];// Goertzel output: real, imag, squared magnitude

int main(int argc, char \*argv[]) FILE \*f; int i, Fs, N, b, x, n, z0, i1, i2, th; float w, S;

if(argc<6) { printf("usage: %s outfile Fs N bits threshold\n",argv[0]); return 0; if(NULL==(f=fopen(argv[1],"rt"))) { printf("cannot read %s\n",argv[1]); return 0; Fs=atoi(argv[2]); printf("Fs = %d Hz sampling frequency\n",Fs); N =atoi(argv[3]); printf("N = %d points for Goertzel\n",N); if(N>MAXN) { printf("max N = %d\n",MAXN); fclose(f); return O; } b =atoi(argv[4]); printf("b = %d scaling is 2^b\n",b); S = (float)(1<<b); // scaling factor th=atoi(argv[5]); printf("th = %d threshold\n",th);

printf("\nreference string: "); for(i2=0;i2<4;i2++) for(i1=0;i1<4;i1++) printf("%c",sym[symmtx[i1][i2]]); printf("\ndecoded string: ");

for(i=0;i<N;i++) { // init window (Hamming) win[i] = (int)round(S\*(0.54 -0.46\*cosf(2.0\*M_PI\*(float)i/(float)(N-1))));

for(i=0;i<4;i++) { // init Goertzel constants // coRDIC may be used here to compute sin() and cos() w = 2.O\*M_PI\*round((float)N\*(float)frow[i]/(float)Fs)/(float)N; cw[i] = (int)round(S\*cosf(w)); c[i] = cw[i]<<1; sw[i] = (int)round(S\*sinf(w)); w = 2.O\*M_PI\*round((float)N\*(float)fcol[i]/(float)Fs)/(float)N; cw[i+4] = (int)round(S\*cosf(w)); c[i+4] = cw[i+4]<<1; sw[i+4] = (int)round(S\*sinf(w)); }

for(n=0;!feof(f);){ i = fscanf(f,"%d",&x); if(i<1) continue; x = ((x\*win[n])>>b); // windowing if((n%N)==0) for(i=0;i<8;i++) { z1[i]=0; z2[i]=0; } // Goertzelreset // \*\*\*\* GOERTZEL ITERATION \*\*\*\* for(i=0;i<8;i++){ z0 = x + (c[i]\*z1[i])>>b) − z2[i]; // Goertzel iteration z2[i] = z1[i]; z1[i] = z0; } // Goertzel status update // \*\*\*\* GOERTZEL ITERATION \*\*\*\* n++; if((n%N)==0) { n=0; // finalize and decode for(i1=i2=-1,i=0;i<8;i++){ // coRDIC may be used here to compute atan2() and sqrt() I[i] = ((cw[i]\*z1[i])>>b) − z2[i]; // Goertzel final I Q[i] = ((sw[i]\*z1[i])>>b); // Goertzel final Q M2[i] = I[i]\*I[i] + Q[i]Q[i]; // magnitude squared if(M2[i]>th) { DTMF decoding if(i<4) { if(i1==-1) i1=i else i1=4; } // find 1st tone, one peak allowed else { if(i2==-1 i2=i-4;else i2=4; } // find 2nd tone, one peak allowed } if((i1>-1)&&(i1<4)&&(i2>-1)&&(i2<4)) printf("%c",sym[symmtx[i1][i2]]); else printf(“ "); } } printf("\n\n"); fclose(f); return O;

# The C output for a typical run on the same signal as the MATLAB is the following:

C:\>GoertzelDTMFdec in.txt 4000 200 12 2000000

Fs 4000 Hz sampling frequency N = 200 points for Goertzel b = 12 scaling is 2^b th = 2000000 threshold

reference string: 147\*2580369#ABCD decoded string: 147\* 25800369 #ABBCD

# Revision history

Table 2. Document revision history   

<table><tr><td>Date</td><td>Version</td><td>Changes</td></tr><tr><td>03-May-2021</td><td>1</td><td>Initial release.</td></tr></table>

# Contents

General information   
1.1 Reference documents.   
The Goertzel algorithm   
2.1 Goertzel algorithm implementation. 4   
2.2 Goertzel as an lIR filter.   
2.3 Goertzel as the k-th coefficient of an N-point FFT. 5   
2.4 Generalized Goertzel for k index not-integer. 5   
2.5 Generalized Goertzel equivalence to IQ demodulation 5   
2.6 Test for Goertzel algorithm implementations 6   
2.7 Goertzel error bounds. 6

# Application example: DTMF dual-tone multi-frequency signaling

3.1 DTMF encoding and decoding, MATLAB script.   
3.2 DTMF encoding and decoding, fixed-point C. 9   
Revision history. 13   
Contents .14   
List of tables .15   
List of figures. .16

# List of tables

Table 1. Dual-tone multi-frequency (DTMF) Table 2. Document revision history . 13

# List of figures

Figure 1. Direct I form for H(z) = (W − z − 1) / (1 − cz − 1 + z − 2), W = exp (j 2π/N k), c = 2cos(2π/N k) 4   
Figure 2. Spectrogram of the generated test signal. 9   
Figure 3. Frequency coefficients computed by the Goertzel algorithm 9   
Figure 4. Frequency coefficients above threshold. 9

# IMPORTANT NOTICE  PLEASE READ CAREFULLY

ol uant  l.

Purchasers' products.

No license, express or implied, to any intellectual property right is granted by ST herein.

names are the property of their respective owners.

I

© 2021 STMicroelectronics - All rights reserved