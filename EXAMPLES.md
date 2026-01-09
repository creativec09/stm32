# STM32 Multi-Agent Architecture - Concrete Examples

This document provides detailed examples of how the multi-agent system handles real-world STM32 development queries.

## Example 1: Single-Domain Query

### User Query
> "How do I configure UART1 for 115200 baud with DMA receive on STM32F4?"

### Triage Analysis
```
Query Classification:
├── Keywords: UART, baud, DMA, receive
├── STM32 Family: F4 (explicitly stated)
├── Primary Domain: peripheral-comm
├── Secondary Domains: none
├── Complexity: simple
└── Strategy: direct dispatch
```

### Agent Response (peripheral-comm)
```c
/**
 * @brief UART1 configuration with DMA receive
 * @device STM32F4
 */

/* Buffer for DMA receive */
#define UART_RX_BUFFER_SIZE 256
uint8_t uart_rx_buffer[UART_RX_BUFFER_SIZE];

UART_HandleTypeDef huart1;
DMA_HandleTypeDef hdma_usart1_rx;

void UART1_Init(void)
{
    /* Enable clocks */
    __HAL_RCC_USART1_CLK_ENABLE();
    __HAL_RCC_DMA2_CLK_ENABLE();
    __HAL_RCC_GPIOA_CLK_ENABLE();

    /* GPIO Configuration: PA9=TX, PA10=RX */
    GPIO_InitTypeDef GPIO_InitStruct = {0};
    GPIO_InitStruct.Pin = GPIO_PIN_9 | GPIO_PIN_10;
    GPIO_InitStruct.Mode = GPIO_MODE_AF_PP;
    GPIO_InitStruct.Pull = GPIO_PULLUP;
    GPIO_InitStruct.Speed = GPIO_SPEED_FREQ_HIGH;
    GPIO_InitStruct.Alternate = GPIO_AF7_USART1;
    HAL_GPIO_Init(GPIOA, &GPIO_InitStruct);

    /* UART Configuration */
    huart1.Instance = USART1;
    huart1.Init.BaudRate = 115200;
    huart1.Init.WordLength = UART_WORDLENGTH_8B;
    huart1.Init.StopBits = UART_STOPBITS_1;
    huart1.Init.Parity = UART_PARITY_NONE;
    huart1.Init.Mode = UART_MODE_TX_RX;
    huart1.Init.HwFlowCtl = UART_HWCONTROL_NONE;
    huart1.Init.OverSampling = UART_OVERSAMPLING_16;
    HAL_UART_Init(&huart1);

    /* DMA Configuration */
    hdma_usart1_rx.Instance = DMA2_Stream2;
    hdma_usart1_rx.Init.Channel = DMA_CHANNEL_4;
    hdma_usart1_rx.Init.Direction = DMA_PERIPH_TO_MEMORY;
    hdma_usart1_rx.Init.PeriphInc = DMA_PINC_DISABLE;
    hdma_usart1_rx.Init.MemInc = DMA_MINC_ENABLE;
    hdma_usart1_rx.Init.PeriphDataAlignment = DMA_PDATAALIGN_BYTE;
    hdma_usart1_rx.Init.MemDataAlignment = DMA_MDATAALIGN_BYTE;
    hdma_usart1_rx.Init.Mode = DMA_CIRCULAR;
    hdma_usart1_rx.Init.Priority = DMA_PRIORITY_HIGH;
    hdma_usart1_rx.Init.FIFOMode = DMA_FIFOMODE_DISABLE;
    HAL_DMA_Init(&hdma_usart1_rx);

    __HAL_LINKDMA(&huart1, hdmarx, hdma_usart1_rx);

    /* Start DMA receive */
    HAL_UART_Receive_DMA(&huart1, uart_rx_buffer, UART_RX_BUFFER_SIZE);

    /* Enable IDLE interrupt for packet detection */
    __HAL_UART_ENABLE_IT(&huart1, UART_IT_IDLE);
    HAL_NVIC_SetPriority(USART1_IRQn, 5, 0);
    HAL_NVIC_EnableIRQ(USART1_IRQn);
}
```

---

## Example 2: Multi-Domain Query (Parallel)

### User Query
> "My battery-powered device needs to wake from Stop mode on UART receive. What's the power consumption and how do I set it up?"

### Triage Analysis
```
Query Classification:
├── Keywords: battery, Stop mode, wake, UART, power consumption
├── STM32 Family: unknown (needs clarification or default)
├── Primary Domain: power-management
├── Secondary Domains: peripheral-comm
├── Complexity: medium
└── Strategy: parallel dispatch, then merge
```

### Parallel Agent Dispatch

#### Power-Management Agent Response
```markdown
## Stop Mode Power Consumption

For STM32L4 series (ultra-low-power):
- Stop 0: ~1.0 µA (with LPUART active)
- Stop 1: ~0.8 µA
- Stop 2: ~0.3 µA (LPUART cannot wake)

For UART wake-up capability:
- Use Stop 0 or Stop 1 mode
- LPUART must be used (not regular UART)
- LPUART clocked from LSE (32.768 kHz)
```

```c
void Enter_StopMode_UART_Wakeup(void)
{
    /* LPUART must be configured first */

    /* Suspend SysTick */
    HAL_SuspendTick();

    /* Enter Stop 1 mode */
    HAL_PWREx_EnterSTOP1Mode(PWR_STOPENTRY_WFI);

    /* Restore clock after wake */
    SystemClock_Config();
    HAL_ResumeTick();
}
```

#### Peripheral-Comm Agent Response
```c
/* LPUART Configuration for Stop Mode Wake-up */
void LPUART_WakeUp_Init(void)
{
    /* Clock LPUART from LSE for low-power operation */
    RCC_PeriphCLKInitTypeDef PeriphClkInit = {0};
    PeriphClkInit.PeriphClockSelection = RCC_PERIPHCLK_LPUART1;
    PeriphClkInit.Lpuart1ClockSelection = RCC_LPUART1CLKSOURCE_LSE;
    HAL_RCCEx_PeriphCLKConfig(&PeriphClkInit);

    hlpuart1.Instance = LPUART1;
    hlpuart1.Init.BaudRate = 9600;  /* Max with LSE clock */
    hlpuart1.Init.WordLength = UART_WORDLENGTH_8B;
    hlpuart1.Init.StopBits = UART_STOPBITS_1;
    hlpuart1.Init.Parity = UART_PARITY_NONE;
    hlpuart1.Init.Mode = UART_MODE_TX_RX;
    HAL_UART_Init(&hlpuart1);

    /* Enable wake-up from Stop mode */
    UART_WakeUpTypeDef wakeup = {0};
    wakeup.WakeUpEvent = UART_WAKEUP_ON_STARTBIT;
    HAL_UARTEx_StopModeWakeUpSourceConfig(&hlpuart1, wakeup);
    HAL_UARTEx_EnableStopMode(&hlpuart1);
}
```

### Synthesized Response
```markdown
## Battery-Powered UART Wake-up Solution

### Power Budget
| Mode | Current | Duration | Energy/Day |
|------|---------|----------|------------|
| Stop 1 + LPUART | 1.0 µA | 23.9 hours | 86 µAh |
| Active (processing) | 5 mA | 0.1 hours | 500 µAh |
| **Total** | | | **586 µAh** |

With a 500mAh battery: ~850 days standby

### Implementation
1. Use LPUART (not regular UART) clocked from LSE
2. Maximum baud rate: 9600 with LSE
3. Use Stop 1 mode (Stop 2 cannot wake on UART)
4. Enable start bit wake-up detection

### Code Integration
[Combined code from both agents]
```

---

## Example 3: Multi-Domain Query (Sequential Chain)

### User Query
> "Help me implement secure firmware updates over USB for STM32H7"

### Triage Analysis
```
Query Classification:
├── Keywords: secure, firmware updates, USB
├── STM32 Family: H7
├── Primary Domains: security, bootloader-programming, peripheral-comm
├── Complexity: complex
└── Strategy: sequential chain

Execution Order:
1. security → Define security architecture
2. bootloader-programming → Implement update mechanism
3. peripheral-comm → USB protocol details
```

### Sequential Execution

#### Step 1: Security Agent
```markdown
## Secure Firmware Update Architecture

### Security Requirements
1. **Authentication**: Verify firmware comes from authorized source
2. **Integrity**: Ensure firmware not modified in transit
3. **Confidentiality**: (Optional) Encrypt firmware
4. **Anti-rollback**: Prevent downgrade attacks

### Recommended Approach
- ECDSA signature verification (P-256)
- SHA-256 hash for integrity
- Optional AES-GCM encryption
- Version counter in OTP or protected flash
```

```c
/* Firmware header with security fields */
typedef struct {
    uint32_t magic;           /* 0x53544D55 = "STMU" */
    uint32_t version;
    uint32_t size;
    uint8_t  sha256[32];      /* Hash of firmware */
    uint8_t  signature[64];   /* ECDSA signature */
    uint8_t  iv[16];          /* AES IV (if encrypted) */
} SecureFirmwareHeader_t;

/* Signature verification */
bool Verify_Firmware_Signature(SecureFirmwareHeader_t *hdr, uint8_t *fw_data)
{
    uint8_t computed_hash[32];

    /* Compute SHA-256 of firmware */
    HAL_HASH_SHA256_Start(&hhash, fw_data, hdr->size, computed_hash, 1000);

    /* Verify hash matches header */
    if (memcmp(computed_hash, hdr->sha256, 32) != 0) {
        return false;
    }

    /* Verify ECDSA signature */
    return PKA_ECDSA_Verify(hdr->sha256, hdr->signature, public_key);
}
```

#### Step 2: Bootloader-Programming Agent (uses security output)
```c
/* Secure bootloader main flow */
void SecureBootloader_Main(void)
{
    /* Check for update request */
    if (USB_UpdatePending()) {
        /* Receive firmware via USB */
        SecureFirmwareHeader_t header;
        uint8_t *fw_buffer = (uint8_t *)DOWNLOAD_BUFFER;

        USB_ReceiveFirmware(&header, fw_buffer);

        /* Verify signature (from security agent) */
        if (!Verify_Firmware_Signature(&header, fw_buffer)) {
            USB_SendStatus(UPDATE_SIGNATURE_INVALID);
            return;
        }

        /* Check anti-rollback */
        if (header.version <= Get_Minimum_Version()) {
            USB_SendStatus(UPDATE_ROLLBACK_DETECTED);
            return;
        }

        /* Decrypt if needed */
        if (Is_Encrypted(&header)) {
            AES_GCM_Decrypt(fw_buffer, header.size, header.iv);
        }

        /* Write to flash */
        Flash_Write(APP_START, fw_buffer, header.size);

        /* Update anti-rollback counter */
        Set_Minimum_Version(header.version);

        USB_SendStatus(UPDATE_SUCCESS);
    }

    /* Boot application */
    if (Verify_Application(APP_START)) {
        Jump_To_Application(APP_START);
    }
}
```

#### Step 3: Peripheral-Comm Agent (USB details)
```c
/* USB DFU class for firmware updates */
#define USB_DFU_TRANSFER_SIZE  4096

/* DFU state machine */
typedef enum {
    DFU_IDLE,
    DFU_DOWNLOAD_SYNC,
    DFU_DOWNLOAD_BUSY,
    DFU_DOWNLOAD_IDLE,
    DFU_MANIFEST_SYNC,
    DFU_MANIFEST,
    DFU_ERROR
} DFU_State_t;

/* Handle DFU download request */
void DFU_Download_Handler(uint16_t block_num, uint8_t *data, uint16_t length)
{
    static uint32_t download_offset = 0;

    if (block_num == 0 && length == sizeof(SecureFirmwareHeader_t)) {
        /* First block is header */
        memcpy(&firmware_header, data, sizeof(SecureFirmwareHeader_t));
        download_offset = 0;
    } else {
        /* Data blocks */
        memcpy(download_buffer + download_offset, data, length);
        download_offset += length;
    }

    /* Check if download complete */
    if (download_offset >= firmware_header.size) {
        DFU_State = DFU_MANIFEST_SYNC;
    }
}
```

### Final Synthesized Response
```markdown
## Complete Secure USB Firmware Update Solution

### Architecture Overview
```
┌─────────────┐      ┌─────────────┐      ┌─────────────┐
│   Host PC   │─USB─►│  DFU Boot   │─────►│  Verify &   │
│  (dfu-util) │      │  Protocol   │      │  Decrypt    │
└─────────────┘      └─────────────┘      └──────┬──────┘
                                                  │
                                                  ▼
                     ┌─────────────┐      ┌─────────────┐
                     │    Flash    │◄─────│  Write to   │
                     │  Application│      │    Flash    │
                     └─────────────┘      └─────────────┘
```

### Security Features
- ECDSA P-256 signature verification
- SHA-256 integrity check
- Optional AES-256-GCM encryption
- Anti-rollback protection

### Implementation Files
1. `secure_boot.h/c` - Security verification
2. `bootloader.h/c` - Main boot logic
3. `usbd_dfu.h/c` - USB DFU protocol

### Usage
```bash
# Sign firmware on host
python sign_firmware.py --key private.pem firmware.bin

# Upload via DFU
dfu-util -a 0 -D firmware_signed.bin
```
```

---

## Example 4: Debugging Session with Handoffs

### User Query
> "My STM32F4 crashes randomly. I see HardFaults but don't know what's causing them."

### Triage Analysis
```
Query Classification:
├── Keywords: crashes, HardFault
├── STM32 Family: F4
├── Primary Domain: debug
├── Complexity: iterative (debugging)
└── Strategy: debug-led investigation with potential handoffs
```

### Debug Agent Initial Response
```c
/* Enhanced HardFault handler for diagnosis */
void HardFault_Handler(void)
{
    __asm volatile(
        "TST LR, #4     \n"
        "ITE EQ         \n"
        "MRSEQ R0, MSP  \n"
        "MRSNE R0, PSP  \n"
        "B HardFault_Handler_C \n"
    );
}

void HardFault_Handler_C(uint32_t *stack)
{
    volatile uint32_t cfsr = SCB->CFSR;
    volatile uint32_t hfsr = SCB->HFSR;
    volatile uint32_t pc = stack[6];
    volatile uint32_t lr = stack[5];

    /* Decode fault */
    if (cfsr & 0x8000) {  /* BFARVALID */
        volatile uint32_t bfar = SCB->BFAR;
        /* Bus fault at address 'bfar' */
    }

    if (cfsr & 0x80) {  /* MMARVALID */
        volatile uint32_t mmar = SCB->MMFAR;
        /* Memory fault at address 'mmar' */
    }

    __BKPT(0);  /* Break for debugger */
    while(1);
}
```

### User Follow-up
> "I added your handler. CFSR = 0x00010000, PC = 0x08004A32. The crash happens during DMA transfer."

### Debug Agent Analysis → Handoff to firmware-core
```
Fault Decoded:
├── CFSR bit 16 = UNDEFINSTR (Undefined instruction)
├── PC = 0x08004A32 (in valid flash range)
├── Context: During DMA transfer
└── Hypothesis: Possible memory corruption or unaligned access

Handoff to firmware-core:
├── Reason: DMA configuration review needed
└── Context: Suspected DMA overwriting code/stack
```

### Firmware-Core Agent Response
```markdown
## Analysis: DMA Configuration Issue

The undefined instruction fault during DMA suggests:
1. DMA is overwriting memory it shouldn't
2. Possible buffer overflow in DMA destination

### Check These Items:
```c
/* Verify DMA destination buffer */
#define DMA_BUFFER_SIZE 1024
uint8_t dma_buffer[DMA_BUFFER_SIZE];  /* Is this big enough? */

/* Check DMA configuration */
hdma.Init.PeriphInc = DMA_PINC_DISABLE;  /* Correct? */
hdma.Init.MemInc = DMA_MINC_ENABLE;
hdma.Init.Mode = DMA_CIRCULAR;  /* Does buffer handle wrap? */

/* Verify buffer placement */
/* If buffer is near stack, DMA might overwrite stack */
```

### Likely Root Cause
DMA in circular mode with buffer too small, causing it to wrap and overwrite adjacent memory (possibly the stack or code in RAM).

### Fix
```c
/* Place DMA buffer in specific memory section */
__attribute__((section(".dma_buffer")))
__attribute__((aligned(4)))
uint8_t dma_buffer[DMA_BUFFER_SIZE];

/* In linker script, place .dma_buffer away from stack */
```
```

### Final Resolution
```markdown
## Root Cause Identified

The DMA buffer was placed on the stack (local variable in a function) and the DMA was configured for circular mode. When the function returned, the stack was reused but DMA continued writing to that memory location.

### Solution Applied
1. Move DMA buffer to global scope or dedicated RAM section
2. Ensure buffer size matches expected data
3. Add buffer alignment for DMA requirements

### Prevention
- Never use stack-allocated buffers for DMA
- Use memory sections for DMA buffers
- Enable MPU to protect critical memory regions
```

---

## Example 5: Hardware + Software Combined Query

### User Query
> "My custom STM32H7 board's USB won't enumerate. I've checked my code and it looks correct."

### Triage Analysis
```
Query Classification:
├── Keywords: custom board, USB, enumerate
├── STM32 Family: H7
├── Primary Domains: peripheral-comm, hardware-design
├── Complexity: medium (debugging)
└── Strategy: parallel investigation
```

### Peripheral-Comm Agent
```markdown
## USB Enumeration Checklist (Software)

### 1. Clock Configuration
```c
/* USB requires 48MHz clock */
RCC_PeriphCLKInitTypeDef PeriphClkInit = {0};
PeriphClkInit.PeriphClockSelection = RCC_PERIPHCLK_USB;
PeriphClkInit.UsbClockSelection = RCC_USBCLKSOURCE_HSI48;
HAL_RCCEx_PeriphCLKConfig(&PeriphClkInit);

/* Or use PLL */
// RCC->PLLCFGR configured for 48MHz on PLLQ
```

### 2. GPIO Configuration
```c
/* PA11 = USB_DM, PA12 = USB_DP */
GPIO_InitTypeDef GPIO_InitStruct = {0};
GPIO_InitStruct.Pin = GPIO_PIN_11 | GPIO_PIN_12;
GPIO_InitStruct.Mode = GPIO_MODE_AF_PP;
GPIO_InitStruct.Pull = GPIO_NOPULL;  /* External pullup on DP */
GPIO_InitStruct.Speed = GPIO_SPEED_FREQ_VERY_HIGH;
GPIO_InitStruct.Alternate = GPIO_AF10_OTG1_FS;
HAL_GPIO_Init(GPIOA, &GPIO_InitStruct);
```

### 3. USB Initialization Order
- Enable clocks
- Configure GPIO
- Initialize USB peripheral
- Start USB device

### Common Software Issues
- [ ] Wrong USB clock (must be exactly 48MHz)
- [ ] GPIO not configured as alternate function
- [ ] Missing NVIC interrupt enable
- [ ] USB descriptor errors
```

### Hardware-Design Agent
```markdown
## USB Hardware Checklist

### 1. Schematic Review
```
           1.5kΩ (for FS)
VBUS ─────────┬──────────────── to MCU PA9 (OTG_FS_VBUS)
              │
           100nF
              │
             GND

D- (PA11) ────┬───────────────── USB Connector D-
              22Ω (optional)

D+ (PA12) ────┬───────────────── USB Connector D+
              │
           1.5kΩ to 3.3V (for device mode detection)
```

### 2. Critical Components
- [ ] 1.5kΩ pull-up on D+ (built-in on some STM32, check datasheet)
- [ ] ESD protection on D+/D- lines
- [ ] 22Ω series resistors (impedance matching)
- [ ] Decoupling on VBUS sensing pin

### 3. PCB Layout
- [ ] D+/D- traces: 90Ω differential impedance
- [ ] D+/D- length matched (±2mm)
- [ ] No signals crossing under USB traces
- [ ] Ground plane under USB section

### 4. Common Hardware Issues
- [ ] Missing DP pull-up resistor
- [ ] Wrong crystal (USB timing sensitive)
- [ ] Poor ground connection
- [ ] ESD damage from handling
```

### Synthesized Diagnostic Steps
```markdown
## USB Not Enumerating - Diagnostic Steps

### Step 1: Verify Clock
```c
/* Add this to check USB clock */
uint32_t usb_clock = HAL_RCCEx_GetPeriphCLKFreq(RCC_PERIPHCLK_USB);
/* Must be 48000000 (48MHz) */
```

### Step 2: Check Hardware
1. Measure voltage on D+ line with USB unplugged
   - Should see 3.3V through 1.5kΩ pull-up
   - If 0V: Pull-up missing or GPIO misconfigured

2. Connect USB and measure D+
   - Should drop to ~3.0V when host connects
   - If still 3.3V: Host not seeing device

### Step 3: Protocol Analyzer
If available, capture USB traffic:
- No traffic = electrical issue
- Reset only = clock or pull-up issue
- Enumeration starts = descriptor issue

### Step 4: Minimal Test Code
```c
/* Bare minimum USB device test */
int main(void)
{
    HAL_Init();
    SystemClock_Config();

    /* Just USB, nothing else */
    MX_USB_DEVICE_Init();

    while(1) {
        /* LED toggle to show running */
        HAL_GPIO_TogglePin(LED_GPIO_Port, LED_Pin);
        HAL_Delay(500);
    }
}
```

### Most Likely Causes (Custom Board)
1. **Missing 1.5kΩ pull-up on D+** (most common)
2. **Wrong USB clock frequency**
3. **Crystal frequency mismatch**
4. **VBUS not connected to MCU** (if using VBUS sensing)
```

---

## Summary: Query Routing Quick Reference

| Query Pattern | Agents Involved | Strategy |
|--------------|-----------------|----------|
| "Configure X peripheral" | Specific peripheral agent | Direct |
| "X not working" | debug + relevant peripheral | Sequential |
| "Optimize power" | power-management | Direct |
| "Secure X" | security + relevant domain | Sequential |
| "Design schematic for X" | hardware-design | Direct |
| "X crashes/faults" | debug | Iterative |
| "Meet Y standard" | safety-certification | Direct |
| "Update firmware" | bootloader + (security) | Sequential |
| "Battery-powered X" | power + peripheral | Parallel |
| "Custom board issue" | hardware + peripheral | Parallel |
