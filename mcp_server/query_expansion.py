"""
STM32 Query Expansion Module

This module provides synonym expansion and query normalization for STM32 documentation
searches. It handles domain-specific terminology, abbreviations, and alternative
naming conventions used in embedded systems development.

Features:
- Bidirectional synonym mappings for STM32 peripherals and concepts
- Query normalization to canonical forms
- Related peripheral detection
- Query classification (HAL function, register, peripheral, general)
- Pre-compiled regex patterns for efficient matching
"""

import re
from typing import Optional


# =============================================================================
# STM32 SYNONYM DICTIONARY
# =============================================================================
# Bidirectional mappings between equivalent terms in STM32 development.
# Each key maps to a set of synonyms that can be used interchangeably.

STM32_SYNONYMS: dict[str, set[str]] = {
    # -------------------------------------------------------------------------
    # Communication Peripherals
    # -------------------------------------------------------------------------
    "uart": {"usart", "serial", "rs232", "rs-232", "async serial"},
    "usart": {"uart", "serial", "rs232", "rs-232", "sync serial"},
    "serial": {"uart", "usart", "rs232", "rs-232"},
    "i2c": {"iic", "twi", "two wire", "two-wire", "smbus"},
    "iic": {"i2c", "twi", "two wire", "two-wire", "smbus"},
    "twi": {"i2c", "iic", "two wire", "two-wire"},
    "spi": {"serial peripheral interface", "synchronous serial"},
    "can": {"canbus", "can bus", "can-bus", "controller area network"},
    "canbus": {"can", "can bus", "can-bus"},
    "usb": {"universal serial bus"},
    "ethernet": {"eth", "lan", "network"},
    "eth": {"ethernet", "lan", "network"},
    "sdio": {"sdmmc", "sd card", "mmc"},
    "sdmmc": {"sdio", "sd card", "mmc"},
    "qspi": {"quadspi", "quad spi", "quad-spi"},
    "quadspi": {"qspi", "quad spi", "quad-spi"},
    "sai": {"serial audio interface", "i2s audio"},
    "i2s": {"inter-ic sound", "audio serial"},

    # -------------------------------------------------------------------------
    # Interrupts and Exceptions
    # -------------------------------------------------------------------------
    "interrupt": {"irq", "isr", "exception", "int"},
    "irq": {"interrupt", "isr", "interrupt request"},
    "isr": {"interrupt", "irq", "interrupt service routine", "handler"},
    "exti": {"external interrupt", "gpio interrupt", "ext interrupt", "external line"},
    "external interrupt": {"exti", "gpio interrupt", "ext interrupt"},
    "gpio interrupt": {"exti", "external interrupt", "pin interrupt"},
    "nvic": {"nested vectored interrupt controller", "interrupt controller"},
    "handler": {"callback", "isr", "interrupt handler"},
    "callback": {"handler", "completion callback", "event handler"},
    "pendsv": {"pendable service", "context switch"},
    "systick": {"system tick", "sys tick", "system timer"},

    # -------------------------------------------------------------------------
    # Clock and Reset
    # -------------------------------------------------------------------------
    "clock": {"rcc", "clk", "oscillator", "frequency"},
    "rcc": {"clock", "reset and clock control", "clock control"},
    "hse": {"external oscillator", "high speed external", "external crystal", "xtal"},
    "external oscillator": {"hse", "crystal", "xtal"},
    "hsi": {"internal oscillator", "high speed internal", "internal rc"},
    "internal oscillator": {"hsi", "internal rc", "rc oscillator"},
    "lse": {"low speed external", "32khz crystal", "rtc crystal"},
    "lsi": {"low speed internal", "internal 32khz", "rtc internal"},
    "pll": {"phase locked loop", "clock multiplier", "frequency multiplier"},
    "sysclk": {"system clock", "core clock", "cpu clock"},
    "hclk": {"ahb clock", "bus clock"},
    "pclk": {"apb clock", "peripheral clock"},
    "mco": {"master clock output", "clock output"},

    # -------------------------------------------------------------------------
    # Timers
    # -------------------------------------------------------------------------
    "timer": {"tim", "tmr", "counter"},
    "tim": {"timer", "tmr", "counter"},
    "pwm": {"pulse width modulation", "pulse width", "duty cycle"},
    "pulse width modulation": {"pwm", "duty cycle"},
    "capture": {"input capture", "ic", "timer capture"},
    "input capture": {"capture", "ic", "timer capture"},
    "compare": {"output compare", "oc", "timer compare"},
    "output compare": {"compare", "oc", "timer compare"},
    "watchdog": {"wdg", "iwdg", "wwdg", "watchdog timer"},
    "iwdg": {"independent watchdog", "watchdog"},
    "wwdg": {"window watchdog", "windowed watchdog"},
    "rtc": {"real time clock", "real-time clock", "calendar"},
    "encoder": {"quadrature encoder", "rotary encoder", "encoder mode"},
    "one pulse": {"single pulse", "monostable", "one shot"},

    # -------------------------------------------------------------------------
    # DMA
    # -------------------------------------------------------------------------
    "dma": {"direct memory access", "memory transfer"},
    "direct memory access": {"dma"},
    "circular": {"ring buffer", "circular buffer", "continuous"},
    "ring buffer": {"circular", "circular buffer"},
    "stream": {"dma stream", "dma channel"},
    "channel": {"dma channel", "stream"},
    "fifo": {"first in first out", "buffer"},
    "burst": {"burst mode", "burst transfer"},
    "memory to memory": {"mem2mem", "m2m"},
    "peripheral to memory": {"p2m", "rx dma"},
    "memory to peripheral": {"m2p", "tx dma"},

    # -------------------------------------------------------------------------
    # ADC and DAC
    # -------------------------------------------------------------------------
    "adc": {"analog to digital", "analog-to-digital", "a/d", "ad converter"},
    "analog to digital": {"adc", "a/d", "ad converter"},
    "dac": {"digital to analog", "digital-to-analog", "d/a", "da converter"},
    "digital to analog": {"dac", "d/a", "da converter"},
    "conversion": {"adc conversion", "sample", "sampling"},
    "continuous": {"continuous mode", "continuous conversion", "free running"},
    "single": {"single conversion", "one shot", "single mode"},
    "scan": {"scan mode", "multi channel", "sequence"},
    "injected": {"injected channel", "injected conversion", "triggered"},
    "regular": {"regular channel", "regular conversion", "regular group"},
    "opamp": {"operational amplifier", "op-amp", "op amp"},
    "comparator": {"comp", "analog comparator", "voltage comparator"},

    # -------------------------------------------------------------------------
    # Power Management
    # -------------------------------------------------------------------------
    "sleep": {"sleep mode", "wfi", "wait for interrupt"},
    "stop": {"stop mode", "deep sleep", "low power stop"},
    "standby": {"standby mode", "shutdown", "lowest power"},
    "low power": {"power saving", "low-power", "energy saving"},
    "wakeup": {"wake up", "wake-up", "exit sleep"},
    "vbat": {"backup battery", "battery backup", "rtc backup"},
    "voltage regulator": {"ldo", "power regulator", "vreg"},
    "brown out": {"bor", "brownout", "voltage drop"},
    "pvd": {"power voltage detector", "voltage monitor"},

    # -------------------------------------------------------------------------
    # GPIO
    # -------------------------------------------------------------------------
    "gpio": {"pin", "port", "io", "i/o", "general purpose io"},
    "pin": {"gpio", "io pin", "port pin"},
    "port": {"gpio port", "io port"},
    "output": {"output mode", "push-pull", "open drain"},
    "push pull": {"push-pull", "pp", "totem pole"},
    "open drain": {"open-drain", "od", "open collector"},
    "input": {"input mode", "digital input"},
    "pull up": {"pull-up", "pullup", "pu"},
    "pull down": {"pull-down", "pulldown", "pd"},
    "alternate function": {"af", "alternate", "peripheral function"},
    "af": {"alternate function", "alternate", "peripheral function"},
    "analog": {"analog mode", "analog input"},
    "remap": {"pin remap", "alternate mapping", "pin mapping"},

    # -------------------------------------------------------------------------
    # Configuration and Initialization
    # -------------------------------------------------------------------------
    "init": {"initialize", "setup", "configure", "initialization"},
    "initialize": {"init", "setup", "configure", "initialization"},
    "setup": {"init", "initialize", "configure", "configuration"},
    "configure": {"init", "initialize", "setup", "config"},
    "config": {"configuration", "configure", "settings"},
    "enable": {"activate", "turn on", "start"},
    "disable": {"deactivate", "turn off", "stop"},
    "reset": {"restart", "reinitialize", "clear"},
    "deinit": {"deinitialize", "uninitialize", "cleanup"},

    # -------------------------------------------------------------------------
    # HAL and Drivers
    # -------------------------------------------------------------------------
    "hal": {"hardware abstraction layer", "stm32 hal", "cube hal"},
    "ll": {"low level", "low-level", "ll driver"},
    "bsp": {"board support package", "board driver"},
    "middleware": {"mw", "software stack"},
    "driver": {"peripheral driver", "device driver"},
    "cubemx": {"stm32cubemx", "cube mx", "code generator"},
    "cubeide": {"stm32cubeide", "cube ide"},

    # -------------------------------------------------------------------------
    # Errors and Debugging
    # -------------------------------------------------------------------------
    "timeout": {"time out", "timed out", "hal_timeout"},
    "error": {"fault", "failure", "err"},
    "fault": {"error", "failure", "exception"},
    "hardfault": {"hard fault", "hard-fault", "crash"},
    "hard fault": {"hardfault", "hard-fault", "crash"},
    "busfault": {"bus fault", "bus-fault", "bus error"},
    "memfault": {"memory fault", "mem fault", "memory error"},
    "usagefault": {"usage fault", "usage-fault", "usage error"},
    "debug": {"debugging", "debugger", "trace"},
    "breakpoint": {"break point", "bp", "bkpt"},
    "swd": {"serial wire debug", "swdio", "swclk"},
    "jtag": {"joint test action group", "debug port"},
    "itm": {"instrumentation trace", "trace output"},
    "etm": {"embedded trace", "trace macrocell"},

    # -------------------------------------------------------------------------
    # Communication Parameters
    # -------------------------------------------------------------------------
    "baud rate": {"baudrate", "bit rate", "bitrate", "bps"},
    "baudrate": {"baud rate", "bit rate", "bitrate", "bps"},
    "bit rate": {"baud rate", "baudrate", "bitrate"},
    "parity": {"parity bit", "error detection"},
    "stop bit": {"stop bits", "stopbit"},
    "data bits": {"word length", "data length", "character size"},
    "flow control": {"handshake", "hardware flow control", "rts cts"},
    "full duplex": {"full-duplex", "bidirectional"},
    "half duplex": {"half-duplex", "single wire"},

    # -------------------------------------------------------------------------
    # Memory
    # -------------------------------------------------------------------------
    "flash": {"flash memory", "program memory", "rom"},
    "sram": {"ram", "data memory", "static ram"},
    "eeprom": {"emulated eeprom", "data eeprom"},
    "ccm": {"core coupled memory", "ccmram", "ccm ram"},
    "backup": {"backup ram", "backup sram", "bkp"},
    "fmc": {"flexible memory controller", "fsmc", "external memory"},
    "fsmc": {"fmc", "flexible static memory controller"},
    "mpu": {"memory protection unit", "memory protection"},
    "cache": {"icache", "dcache", "instruction cache", "data cache"},

    # -------------------------------------------------------------------------
    # Security
    # -------------------------------------------------------------------------
    "crc": {"cyclic redundancy check", "checksum"},
    "rng": {"random number generator", "trng", "random"},
    "aes": {"advanced encryption standard", "encryption", "crypto"},
    "hash": {"sha", "hash algorithm", "digest"},
    "trustzone": {"trust zone", "tz", "secure zone"},
    "firewall": {"memory firewall", "code isolation"},
    "secure boot": {"trusted boot", "verified boot"},
    "option bytes": {"ob", "flash option", "configuration bytes"},
    "rdp": {"read protection", "readout protection"},
    "pcrop": {"proprietary code readout protection"},

    # -------------------------------------------------------------------------
    # Display and Graphics
    # -------------------------------------------------------------------------
    "ltdc": {"lcd tft display controller", "lcd controller", "display"},
    "dma2d": {"chrom-art", "chromart", "graphics accelerator"},
    "dcmi": {"digital camera interface", "camera"},
    "dsi": {"display serial interface", "mipi dsi"},
    "touchgfx": {"touch gfx", "graphics library"},
    "lcd": {"liquid crystal display", "display", "screen"},
    "framebuffer": {"frame buffer", "video buffer", "display buffer"},

    # -------------------------------------------------------------------------
    # Motor Control
    # -------------------------------------------------------------------------
    "bldc": {"brushless dc", "brushless motor"},
    "pmsm": {"permanent magnet synchronous motor"},
    "foc": {"field oriented control", "vector control"},
    "svpwm": {"space vector pwm", "space vector modulation"},
    "hall": {"hall sensor", "hall effect"},
    "encoder interface": {"encoder mode", "quadrature interface"},
}


# =============================================================================
# PERIPHERAL CATEGORIES
# =============================================================================
# Groupings of related peripherals for context-aware searching

PERIPHERAL_CATEGORIES: dict[str, set[str]] = {
    "communication": {"uart", "usart", "spi", "i2c", "can", "usb", "ethernet", "sdio", "qspi", "sai", "i2s"},
    "timers": {"tim", "timer", "rtc", "iwdg", "wwdg", "systick"},
    "analog": {"adc", "dac", "opamp", "comparator"},
    "dma": {"dma", "bdma", "mdma", "dmamux"},
    "gpio": {"gpio", "exti"},
    "clock": {"rcc", "pll", "hse", "hsi", "lse", "lsi"},
    "power": {"pwr", "sleep", "stop", "standby"},
    "memory": {"flash", "sram", "fmc", "fsmc", "mpu"},
    "debug": {"swd", "jtag", "itm", "etm", "dbg"},
    "security": {"crc", "rng", "aes", "hash", "firewall"},
    "display": {"ltdc", "dma2d", "dcmi", "dsi"},
    "interrupt": {"nvic", "exti", "systick"},
}


# =============================================================================
# PRE-COMPILED REGEX PATTERNS
# =============================================================================

# Pattern for HAL function names: HAL_<PERIPHERAL>_<Function> or __HAL_<PERIPHERAL>_<MACRO>
HAL_FUNCTION_PATTERN = re.compile(
    r'^(?:__)?HAL_([A-Z0-9]+)_\w+$',
    re.IGNORECASE
)

# Pattern for LL function names: LL_<PERIPHERAL>_<Function>
LL_FUNCTION_PATTERN = re.compile(
    r'^LL_([A-Z0-9]+)_\w+$',
    re.IGNORECASE
)

# Pattern for register names: <PERIPHERAL>_<REGISTER> or <PERIPHERAL>x_<REGISTER>
REGISTER_PATTERN = re.compile(
    r'^([A-Z]+)x?_([A-Z0-9]+)$',
    re.IGNORECASE
)

# Pattern for peripheral names (standalone)
PERIPHERAL_PATTERN = re.compile(
    r'\b(GPIO|UART|USART|SPI|I2C|CAN|USB|TIM|ADC|DAC|DMA|RCC|NVIC|EXTI|'
    r'PWR|FLASH|RTC|IWDG|WWDG|ETH|SDIO|SDMMC|QSPI|SAI|I2S|LTDC|DMA2D|'
    r'DCMI|FMC|FSMC|CRC|RNG|AES|HASH|OPAMP|COMP|BDMA|MDMA|DMAMUX)\b',
    re.IGNORECASE
)

# Pattern for error-related queries
ERROR_PATTERN = re.compile(
    r'\b(error|fault|timeout|fail|crash|hardfault|busfault|memfault|'
    r'usagefault|stuck|hang|freeze|not working|problem|issue|debug)\b',
    re.IGNORECASE
)

# Pattern for initialization queries
INIT_PATTERN = re.compile(
    r'\b(init|initialize|setup|configure|configuration|enable|start|begin)\b',
    re.IGNORECASE
)

# Pattern for code example queries
CODE_PATTERN = re.compile(
    r'\b(example|sample|code|how to|implementation|tutorial|snippet)\b',
    re.IGNORECASE
)

# Pattern to identify numeric values (baud rate, frequency, etc.)
NUMERIC_PATTERN = re.compile(
    r'\b(\d+(?:\.\d+)?)\s*(hz|khz|mhz|ghz|bps|kbps|mbps|ms|us|ns|v|mv)?\b',
    re.IGNORECASE
)


# =============================================================================
# QUERY EXPANSION FUNCTIONS
# =============================================================================

def expand_query(query: str, max_expansions: int = 3) -> list[str]:
    """
    Expand a query with synonyms to improve search coverage.

    This function identifies terms in the query that have known synonyms
    and generates alternative query forms using those synonyms.

    Args:
        query: The original search query
        max_expansions: Maximum number of expanded queries to return (default: 3)

    Returns:
        List of expanded queries, including the original (normalized) query first

    Example:
        >>> expand_query("uart configuration")
        ['uart configuration', 'usart configuration', 'serial configuration']
    """
    normalized = normalize_query(query)
    expansions = [normalized]

    # Find terms that have synonyms
    query_lower = normalized.lower()
    words = query_lower.split()

    # Build list of possible expansions
    expansion_candidates = []

    for word in words:
        if word in STM32_SYNONYMS:
            synonyms = STM32_SYNONYMS[word]
            for synonym in synonyms:
                # Create expanded query by replacing the word with its synonym
                expanded = query_lower.replace(word, synonym)
                if expanded not in expansions and expanded not in expansion_candidates:
                    expansion_candidates.append(expanded)

    # Also check for multi-word phrases
    for phrase, synonyms in STM32_SYNONYMS.items():
        if ' ' in phrase and phrase in query_lower:
            for synonym in synonyms:
                expanded = query_lower.replace(phrase, synonym)
                if expanded not in expansions and expanded not in expansion_candidates:
                    expansion_candidates.append(expanded)

    # Add candidates up to max_expansions (excluding the original)
    expansions.extend(expansion_candidates[:max_expansions - 1])

    return expansions


def normalize_query(query: str) -> str:
    """
    Normalize a query to canonical forms for consistent matching.

    This function standardizes terminology, fixes common variations,
    and prepares the query for optimal search matching.

    Args:
        query: The raw search query

    Returns:
        Normalized query string

    Example:
        >>> normalize_query("I2C setup")
        'i2c init'
    """
    # Start with lowercase
    normalized = query.lower().strip()

    # Standardize common variations
    replacements = [
        # Hyphenated to space or canonical form
        (r'i-2-c', 'i2c'),
        (r'i 2 c', 'i2c'),
        (r'rs-232', 'uart'),
        (r'rs232', 'uart'),
        (r'can-bus', 'can'),
        (r'can bus', 'can'),

        # Standardize initialization terms
        (r'\bsetup\b', 'init'),
        (r'\bconfigure\b', 'init'),
        (r'\bconfiguration\b', 'init'),
        (r'\binitialize\b', 'init'),
        (r'\binitialization\b', 'init'),

        # Standardize interrupt terms
        (r'\birq\b', 'interrupt'),
        (r'\bisr\b', 'interrupt'),

        # Standardize timer terms
        (r'\btmr\b', 'tim'),
        (r'\btimer\b', 'tim'),

        # Standardize baud rate terms
        (r'\bbit rate\b', 'baud rate'),
        (r'\bbitrate\b', 'baud rate'),

        # Remove extra whitespace
        (r'\s+', ' '),
    ]

    for pattern, replacement in replacements:
        normalized = re.sub(pattern, replacement, normalized)

    return normalized.strip()


def get_related_peripherals(query: str) -> list[str]:
    """
    Identify peripherals related to the query for context-aware searching.

    This function extracts explicitly mentioned peripherals and infers
    related peripherals based on the query context.

    Args:
        query: The search query

    Returns:
        List of related peripheral names (uppercase)

    Example:
        >>> get_related_peripherals("uart dma receive")
        ['UART', 'DMA', 'USART']
    """
    related = set()
    query_lower = query.lower()

    # Find explicitly mentioned peripherals
    matches = PERIPHERAL_PATTERN.findall(query)
    for match in matches:
        related.add(match.upper())

    # Check for peripheral keywords in synonyms
    for term, synonyms in STM32_SYNONYMS.items():
        if term in query_lower:
            # Check if this term maps to a peripheral
            term_upper = term.upper()
            if PERIPHERAL_PATTERN.match(term_upper):
                related.add(term_upper)
            # Also add any synonyms that are peripherals
            for syn in synonyms:
                syn_upper = syn.upper()
                if PERIPHERAL_PATTERN.match(syn_upper):
                    related.add(syn_upper)

    # Add related peripherals from categories
    for peripheral in list(related):
        peripheral_lower = peripheral.lower()
        for category, members in PERIPHERAL_CATEGORIES.items():
            if peripheral_lower in members:
                # Add commonly associated peripherals
                if category == "communication":
                    related.add("DMA")  # Communication often uses DMA
                elif category == "analog":
                    related.add("DMA")  # ADC/DAC often use DMA
                elif category == "timers":
                    if "pwm" in query_lower:
                        related.add("GPIO")  # PWM needs GPIO for output

    # Check for DMA-related terms
    if any(term in query_lower for term in ["dma", "circular", "stream", "channel", "transfer"]):
        related.add("DMA")

    # Check for interrupt-related terms
    if any(term in query_lower for term in ["interrupt", "irq", "callback", "handler", "nvic"]):
        related.add("NVIC")
        if "external" in query_lower or "gpio" in query_lower:
            related.add("EXTI")

    # Check for clock-related terms
    if any(term in query_lower for term in ["clock", "pll", "hse", "hsi", "frequency", "prescaler"]):
        related.add("RCC")

    return sorted(list(related))


def build_enhanced_query(query: str) -> str:
    """
    Build an enhanced query by adding context terms for better search results.

    This function analyzes the query and adds relevant context terms
    that might help find more comprehensive documentation.

    Args:
        query: The original search query

    Returns:
        Enhanced query with added context terms

    Example:
        >>> build_enhanced_query("uart init")
        'uart init stm32 hal configuration'
    """
    enhanced_parts = [normalize_query(query)]
    query_lower = query.lower()

    # Add STM32 context if not present
    if "stm32" not in query_lower:
        enhanced_parts.append("stm32")

    # Add HAL context for function queries
    if HAL_FUNCTION_PATTERN.search(query) or "hal_" in query_lower:
        if "hal" not in query_lower:
            enhanced_parts.append("hal")

    # Add LL context for low-level queries
    if LL_FUNCTION_PATTERN.search(query) or "ll_" in query_lower:
        if "ll" not in query_lower:
            enhanced_parts.append("ll driver")

    # Add init context for configuration queries
    if INIT_PATTERN.search(query):
        if "example" not in query_lower and "code" not in query_lower:
            enhanced_parts.append("configuration")

    # Add error/troubleshooting context
    if ERROR_PATTERN.search(query):
        enhanced_parts.append("troubleshooting")

    # Add related peripherals as context
    peripherals = get_related_peripherals(query)
    if peripherals and len(peripherals) <= 2:
        for p in peripherals:
            if p.lower() not in query_lower:
                enhanced_parts.append(p.lower())

    return " ".join(enhanced_parts)


def classify_query(query: str) -> str:
    """
    Classify a query to determine the best search strategy.

    Categories:
    - hal_function: Query is about a specific HAL/LL function
    - register: Query is about a hardware register
    - peripheral: Query is about a peripheral in general
    - error: Query is about an error or debugging issue
    - init: Query is about initialization/configuration
    - code: Query is looking for code examples
    - general: General STM32 query

    Args:
        query: The search query to classify

    Returns:
        Query classification string

    Example:
        >>> classify_query("HAL_UART_Transmit parameters")
        'hal_function'
        >>> classify_query("GPIOx_MODER register")
        'register'
    """
    query_stripped = query.strip()

    # Check for HAL function pattern
    if HAL_FUNCTION_PATTERN.search(query_stripped):
        return "hal_function"

    # Check for LL function pattern
    if LL_FUNCTION_PATTERN.search(query_stripped):
        return "hal_function"

    # Check for register pattern
    if REGISTER_PATTERN.search(query_stripped):
        return "register"

    # Check for explicit register keywords
    if re.search(r'\b(register|bit field|bit mask|bitfield)\b', query, re.IGNORECASE):
        return "register"

    # Check for error/debug queries
    if ERROR_PATTERN.search(query):
        return "error"

    # Check for code example queries
    if CODE_PATTERN.search(query):
        return "code"

    # Check for initialization queries
    if INIT_PATTERN.search(query):
        return "init"

    # Check if query is primarily about a peripheral
    peripherals = PERIPHERAL_PATTERN.findall(query)
    if peripherals:
        # If the query is mostly just a peripheral name, classify as peripheral
        words = query.split()
        peripheral_words = sum(1 for w in words if PERIPHERAL_PATTERN.match(w))
        if peripheral_words >= len(words) / 2:
            return "peripheral"

    return "general"


# =============================================================================
# UTILITY FUNCTIONS
# =============================================================================

def get_all_synonyms(term: str) -> set[str]:
    """
    Get all synonyms for a term, including transitive synonyms.

    Args:
        term: The term to find synonyms for

    Returns:
        Set of all related terms
    """
    term_lower = term.lower()
    result = {term_lower}

    if term_lower in STM32_SYNONYMS:
        result.update(STM32_SYNONYMS[term_lower])

    # Check if term appears in any synonym sets
    for key, synonyms in STM32_SYNONYMS.items():
        if term_lower in synonyms:
            result.add(key)
            result.update(synonyms)

    return result


def extract_peripheral_from_function(function_name: str) -> Optional[str]:
    """
    Extract the peripheral name from a HAL/LL function name.

    Args:
        function_name: HAL or LL function name

    Returns:
        Peripheral name or None if not found

    Example:
        >>> extract_peripheral_from_function("HAL_UART_Transmit")
        'UART'
    """
    # Try HAL pattern
    match = HAL_FUNCTION_PATTERN.match(function_name)
    if match:
        return match.group(1).upper()

    # Try LL pattern
    match = LL_FUNCTION_PATTERN.match(function_name)
    if match:
        return match.group(1).upper()

    return None


def is_hal_macro(name: str) -> bool:
    """
    Check if a name appears to be a HAL macro (starts with __HAL_).

    Args:
        name: The name to check

    Returns:
        True if it appears to be a HAL macro
    """
    return name.strip().startswith("__HAL_")


def get_peripheral_category(peripheral: str) -> Optional[str]:
    """
    Get the category a peripheral belongs to.

    Args:
        peripheral: Peripheral name

    Returns:
        Category name or None if not categorized
    """
    peripheral_lower = peripheral.lower()
    for category, members in PERIPHERAL_CATEGORIES.items():
        if peripheral_lower in members:
            return category
    return None


def suggest_related_topics(query: str) -> list[str]:
    """
    Suggest related topics based on the query.

    Args:
        query: The search query

    Returns:
        List of suggested related topics
    """
    suggestions = []
    query_lower = query.lower()
    peripherals = get_related_peripherals(query)

    for peripheral in peripherals:
        p_lower = peripheral.lower()

        # Suggest DMA if applicable
        if p_lower in PERIPHERAL_CATEGORIES.get("communication", set()):
            if "dma" not in query_lower:
                suggestions.append(f"{peripheral} DMA")

        # Suggest interrupts
        if "interrupt" not in query_lower and "callback" not in query_lower:
            suggestions.append(f"{peripheral} interrupt")

        # Suggest initialization
        if not INIT_PATTERN.search(query):
            suggestions.append(f"{peripheral} init")

    return suggestions[:5]  # Limit to 5 suggestions


# =============================================================================
# MODULE EXPORTS
# =============================================================================

__all__ = [
    # Main dictionary
    "STM32_SYNONYMS",
    "PERIPHERAL_CATEGORIES",

    # Compiled patterns
    "HAL_FUNCTION_PATTERN",
    "LL_FUNCTION_PATTERN",
    "REGISTER_PATTERN",
    "PERIPHERAL_PATTERN",
    "ERROR_PATTERN",
    "INIT_PATTERN",
    "CODE_PATTERN",
    "NUMERIC_PATTERN",

    # Main functions
    "expand_query",
    "normalize_query",
    "get_related_peripherals",
    "build_enhanced_query",
    "classify_query",

    # Utility functions
    "get_all_synonyms",
    "extract_peripheral_from_function",
    "is_hal_macro",
    "get_peripheral_category",
    "suggest_related_topics",
]
