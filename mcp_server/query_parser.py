"""
Query parser module for extracting metadata filters from natural language queries.

This module provides intelligent parsing of user queries to extract structured
metadata that can be used to filter and enhance vector search results. It detects
HAL/LL function names, register references, STM32 families, peripherals, and
user intent signals.
"""

import re
from dataclasses import dataclass, field
from typing import Optional

from storage.metadata import Peripheral, DocType, ContentType


@dataclass
class ParsedQuery:
    """
    Structured representation of a parsed user query.

    Contains the semantic query text for vector search along with
    extracted metadata filters and intent signals.

    Attributes:
        semantic_query: Cleaned text for vector search
        peripheral: Detected peripheral (e.g., "UART", "GPIO")
        hal_function: Extracted HAL/LL function name
        register: Extracted register name
        doc_type: Detected document type hint
        content_type: Detected content type hint
        stm32_family: Extracted STM32 family (e.g., "STM32H7")
        require_code: User wants code examples
        require_register: User wants register information
    """

    semantic_query: str
    peripheral: Optional[str] = None
    hal_function: Optional[str] = None
    register: Optional[str] = None
    doc_type: Optional[str] = None
    content_type: Optional[str] = None
    stm32_family: Optional[str] = None
    require_code: bool = False
    require_register: bool = False

    def has_filters(self) -> bool:
        """Check if any metadata filters are present."""
        return any([
            self.peripheral,
            self.hal_function,
            self.register,
            self.doc_type,
            self.content_type,
            self.stm32_family,
        ])

    def to_dict(self) -> dict:
        """Convert to dictionary for debugging or logging."""
        return {
            "semantic_query": self.semantic_query,
            "peripheral": self.peripheral,
            "hal_function": self.hal_function,
            "register": self.register,
            "doc_type": self.doc_type,
            "content_type": self.content_type,
            "stm32_family": self.stm32_family,
            "require_code": self.require_code,
            "require_register": self.require_register,
        }


class QueryParser:
    """
    Parser for extracting structured metadata from natural language queries.

    This parser uses regex patterns and keyword matching to identify:
    - HAL/LL function references (e.g., HAL_UART_Transmit)
    - Register names (e.g., GPIOx_MODER, USART_CR1)
    - STM32 family identifiers (e.g., STM32F4, STM32H7)
    - Peripheral keywords
    - User intent signals (code examples, register info)
    - Document type hints (troubleshooting, migration, etc.)

    Example:
        >>> parser = QueryParser()
        >>> result = parser.parse("How do I use HAL_UART_Transmit_DMA on STM32H7?")
        >>> result.hal_function
        'HAL_UART_Transmit_DMA'
        >>> result.peripheral
        'UART'
        >>> result.stm32_family
        'STM32H7'
    """

    # Regex pattern for HAL/LL function names
    # Matches: HAL_UART_Transmit, LL_GPIO_SetPinMode, HAL_SPI_TransmitReceive_DMA
    HAL_PATTERN = re.compile(
        r'\b(HAL|LL)_([A-Z0-9]+)_([A-Za-z0-9_]+)\b'
    )

    # Regex pattern for register names
    # Matches: GPIOx_MODER, USART_CR1, TIMx_CCR1, RCC_AHB1ENR
    REGISTER_PATTERN = re.compile(
        r'\b([A-Z]{2,}[0-9]*)x?_([A-Z][A-Z0-9_]+)\b'
    )

    # Regex pattern for STM32 family identifiers
    # Matches: STM32F4, STM32H7, STM32L4, STM32G0
    FAMILY_PATTERN = re.compile(
        r'\b(STM32[A-Z][0-9]+)\b',
        re.IGNORECASE
    )

    # Mapping from peripheral enum values to keyword variations
    # Used for detecting peripherals from natural language
    PERIPHERAL_KEYWORDS: dict[str, list[str]] = {
        # Communication peripherals
        Peripheral.GPIO.value: ["gpio", "pin", "pins", "port", "ports", "digital i/o"],
        Peripheral.UART.value: ["uart", "serial", "rs232", "rs-232"],
        Peripheral.USART.value: ["usart", "synchronous serial"],
        Peripheral.SPI.value: ["spi", "serial peripheral interface"],
        Peripheral.I2C.value: ["i2c", "iic", "twi", "two-wire", "two wire"],
        Peripheral.I3C.value: ["i3c"],
        Peripheral.CAN.value: ["can", "canbus", "can bus", "bxcan"],
        Peripheral.FDCAN.value: ["fdcan", "can-fd", "can fd"],
        Peripheral.USB.value: ["usb", "usb otg", "usb device", "usb host"],
        Peripheral.ETH.value: ["ethernet", "eth", "mac", "rmii", "mii"],
        Peripheral.SPDIF.value: ["spdif", "s/pdif"],

        # Analog peripherals
        Peripheral.ADC.value: ["adc", "analog-to-digital", "analog to digital", "a/d"],
        Peripheral.DAC.value: ["dac", "digital-to-analog", "digital to analog", "d/a"],

        # Timers
        Peripheral.TIM.value: ["timer", "timers", "pwm", "pulse width", "input capture", "output compare"],
        Peripheral.LPTIM.value: ["lptim", "low-power timer", "low power timer"],
        Peripheral.RTC.value: ["rtc", "real-time clock", "real time clock", "calendar"],
        Peripheral.WWDG.value: ["wwdg", "window watchdog"],
        Peripheral.IWDG.value: ["iwdg", "independent watchdog", "watchdog"],

        # DMA
        Peripheral.DMA.value: ["dma", "direct memory access"],
        Peripheral.BDMA.value: ["bdma", "basic dma"],
        Peripheral.MDMA.value: ["mdma", "master dma"],

        # System peripherals
        Peripheral.RCC.value: ["rcc", "clock", "clocks", "pll", "hse", "hsi", "sysclk"],
        Peripheral.PWR.value: ["pwr", "power", "sleep", "stop", "standby", "low power"],
        Peripheral.NVIC.value: ["nvic", "interrupt", "interrupts", "irq", "priority"],
        Peripheral.EXTI.value: ["exti", "external interrupt", "external interrupts"],
        Peripheral.FLASH.value: ["flash", "programming", "erase", "option bytes"],
        Peripheral.CRC.value: ["crc", "checksum", "cyclic redundancy"],
        Peripheral.TAMP.value: ["tamp", "tamper", "backup"],

        # Memory and storage
        Peripheral.FMC.value: ["fmc", "fsmc", "external memory", "sdram", "sram"],
        Peripheral.SDMMC.value: ["sdmmc", "sd card", "sdcard", "mmc", "emmc"],
        Peripheral.OCTOSPI.value: ["octospi", "ospi", "octo-spi"],
        Peripheral.QUADSPI.value: ["quadspi", "qspi", "quad-spi"],

        # Graphics and display
        Peripheral.LTDC.value: ["ltdc", "lcd-tft", "lcd tft", "display controller"],
        Peripheral.DCMI.value: ["dcmi", "camera", "digital camera"],
        Peripheral.DMA2D.value: ["dma2d", "chrom-art", "chromart", "2d graphics"],
        Peripheral.JPEG.value: ["jpeg", "jpg", "image codec"],

        # Audio
        Peripheral.SAI.value: ["sai", "serial audio", "i2s", "audio"],

        # Security and crypto
        Peripheral.RNG.value: ["rng", "random number", "random generator"],
        Peripheral.CRYP.value: ["cryp", "crypto", "cryptographic", "aes", "des", "encryption"],
        Peripheral.HASH.value: ["hash", "sha", "md5", "digest"],

        # Math
        Peripheral.CORDIC.value: ["cordic", "trigonometric", "sine", "cosine"],

        # System
        Peripheral.MPU.value: ["mpu", "memory protection", "memory region"],
    }

    # Keywords that indicate the user wants code examples
    CODE_INTENT_KEYWORDS: list[str] = [
        "example", "examples", "code", "sample", "snippet",
        "how to", "howto", "implementation", "implement",
        "show me", "write", "create", "configure", "init",
        "initialize", "initialization", "setup", "set up"
    ]

    # Keywords that indicate the user wants register information
    REGISTER_INTENT_KEYWORDS: list[str] = [
        "register", "registers", "bit", "bits", "bitfield",
        "bit field", "offset", "reset value", "read-only",
        "write-only", "read/write"
    ]

    # Document type keyword mapping
    DOC_TYPE_KEYWORDS: dict[str, list[str]] = {
        DocType.HAL_GUIDE.value: ["hal", "hardware abstraction", "ll", "low-level driver"],
        DocType.MIGRATION_GUIDE.value: ["migrate", "migration", "port", "porting", "upgrade", "from", "to"],
        DocType.APPLICATION_NOTE.value: ["application note", "app note", "an"],
        DocType.ERRATA.value: ["errata", "bug", "silicon", "workaround"],
        DocType.REFERENCE_MANUAL.value: ["reference manual", "rm", "detailed"],
        DocType.DATASHEET.value: ["datasheet", "specifications", "specs", "electrical"],
        DocType.SAFETY_MANUAL.value: ["safety", "functional safety", "iec 61508", "iso 26262"],
        # Note: Troubleshooting is a ContentType, not DocType - handled in CONTENT_TYPE_KEYWORDS
    }

    # Content type keyword mapping
    CONTENT_TYPE_KEYWORDS: dict[str, list[str]] = {
        ContentType.CODE_EXAMPLE.value: ["example", "code", "sample", "snippet"],
        ContentType.REGISTER_MAP.value: ["register", "bit field", "offset", "map"],
        ContentType.CONFIGURATION.value: ["configure", "configuration", "setup", "settings"],
        ContentType.TROUBLESHOOTING.value: [
            "troubleshoot", "troubleshooting", "debug", "debugging",
            "error", "fix", "solve", "problem", "issue",
            "not working", "doesn't work", "failed", "failure"
        ],
        ContentType.ELECTRICAL_SPEC.value: ["electrical", "voltage", "current", "power consumption"],
        ContentType.TIMING_DIAGRAM.value: ["timing", "waveform", "diagram", "signal"],
        ContentType.PIN_DESCRIPTION.value: ["pin", "pinout", "alternate function", "af"],
    }

    def __init__(self):
        """Initialize the query parser."""
        # Build reverse lookup for faster peripheral detection
        self._peripheral_lookup: dict[str, str] = {}
        for peripheral, keywords in self.PERIPHERAL_KEYWORDS.items():
            for keyword in keywords:
                self._peripheral_lookup[keyword.lower()] = peripheral

    def parse(self, query: str) -> ParsedQuery:
        """
        Parse a natural language query to extract metadata filters.

        Analyzes the query to detect:
        - HAL/LL function names
        - Register references
        - STM32 family identifiers
        - Peripheral keywords
        - User intent (code examples, register info)
        - Document type hints

        Args:
            query: Natural language query string

        Returns:
            ParsedQuery with extracted metadata and cleaned semantic query
        """
        if not query or not query.strip():
            return ParsedQuery(semantic_query="")

        query_lower = query.lower()

        # Extract HAL/LL function
        hal_function = self._extract_hal_function(query)

        # Extract register name
        register = self._extract_register(query)

        # Extract STM32 family
        stm32_family = self._extract_family(query)

        # Detect peripheral
        peripheral = self._detect_peripheral(query_lower, hal_function)

        # Detect intent
        require_code = self._detect_code_intent(query_lower)
        require_register = self._detect_register_intent(query_lower)

        # Detect document type
        doc_type = self._detect_doc_type(query_lower)

        # Detect content type
        content_type = self._detect_content_type(query_lower)

        # Clean semantic query (keep original text for vector search)
        semantic_query = self._clean_semantic_query(query)

        return ParsedQuery(
            semantic_query=semantic_query,
            peripheral=peripheral,
            hal_function=hal_function,
            register=register,
            doc_type=doc_type,
            content_type=content_type,
            stm32_family=stm32_family,
            require_code=require_code,
            require_register=require_register,
        )

    def _extract_hal_function(self, query: str) -> Optional[str]:
        """
        Extract HAL/LL function name from query.

        Args:
            query: Original query string

        Returns:
            Extracted function name or None
        """
        match = self.HAL_PATTERN.search(query)
        if match:
            # Reconstruct full function name
            return f"{match.group(1)}_{match.group(2)}_{match.group(3)}"
        return None

    def _extract_register(self, query: str) -> Optional[str]:
        """
        Extract register name from query.

        Filters out common false positives like HAL function components.

        Args:
            query: Original query string

        Returns:
            Extracted register name or None
        """
        # First, remove any HAL/LL function matches to avoid confusion
        query_cleaned = self.HAL_PATTERN.sub("", query)

        match = self.REGISTER_PATTERN.search(query_cleaned)
        if match:
            prefix = match.group(1)
            suffix = match.group(2)

            # Filter out common false positives
            false_positives = {"DMA", "IRQ", "CLK", "EN", "IT"}
            if prefix in false_positives and len(suffix) <= 2:
                return None

            # Must look like a register (common patterns)
            valid_prefixes = {
                "GPIO", "USART", "UART", "SPI", "I2C", "TIM", "ADC", "DAC",
                "RCC", "PWR", "FLASH", "DMA", "EXTI", "NVIC", "CAN", "FDCAN",
                "USB", "ETH", "SAI", "LTDC", "DCMI", "RTC", "IWDG", "WWDG",
                "CRC", "RNG", "CRYP", "HASH", "FMC", "SDMMC", "QUADSPI", "OCTOSPI"
            }

            # Check if prefix matches known peripheral register prefix
            base_prefix = prefix.rstrip("0123456789")
            if base_prefix in valid_prefixes:
                return f"{prefix}x_{suffix}" if prefix.endswith(tuple("0123456789")) else f"{prefix}_{suffix}"

        return None

    def _extract_family(self, query: str) -> Optional[str]:
        """
        Extract STM32 family identifier from query.

        Args:
            query: Original query string

        Returns:
            Extracted family (e.g., "STM32H7") or None
        """
        match = self.FAMILY_PATTERN.search(query)
        if match:
            return match.group(1).upper()
        return None

    def _detect_peripheral(
        self, query_lower: str, hal_function: Optional[str]
    ) -> Optional[str]:
        """
        Detect peripheral from query keywords or HAL function.

        First checks if a peripheral can be inferred from the HAL function,
        then falls back to keyword matching.

        Args:
            query_lower: Lowercase query string
            hal_function: Extracted HAL function name (if any)

        Returns:
            Detected peripheral name or None
        """
        # Try to extract from HAL function first
        if hal_function:
            match = self.HAL_PATTERN.match(hal_function)
            if match:
                peripheral_part = match.group(2)
                # Normalize peripheral name
                if peripheral_part in [p.value for p in Peripheral]:
                    return peripheral_part
                # Handle variations
                if peripheral_part == "TIMER":
                    return Peripheral.TIM.value

        # Check for peripheral keywords in query
        # Sort by keyword length (longest first) to match most specific
        for keyword in sorted(self._peripheral_lookup.keys(), key=len, reverse=True):
            # Use word boundary matching for short keywords to avoid false matches
            if len(keyword) <= 3:
                pattern = rf'\b{re.escape(keyword)}\b'
                if re.search(pattern, query_lower):
                    return self._peripheral_lookup[keyword]
            elif keyword in query_lower:
                return self._peripheral_lookup[keyword]

        return None

    def _detect_code_intent(self, query_lower: str) -> bool:
        """
        Detect if the user wants code examples.

        Args:
            query_lower: Lowercase query string

        Returns:
            True if code examples are likely wanted
        """
        return any(keyword in query_lower for keyword in self.CODE_INTENT_KEYWORDS)

    def _detect_register_intent(self, query_lower: str) -> bool:
        """
        Detect if the user wants register information.

        Args:
            query_lower: Lowercase query string

        Returns:
            True if register info is likely wanted
        """
        return any(keyword in query_lower for keyword in self.REGISTER_INTENT_KEYWORDS)

    def _detect_doc_type(self, query_lower: str) -> Optional[str]:
        """
        Detect document type hint from query.

        Args:
            query_lower: Lowercase query string

        Returns:
            Document type value or None
        """
        for doc_type, keywords in self.DOC_TYPE_KEYWORDS.items():
            if any(keyword in query_lower for keyword in keywords):
                return doc_type
        return None

    def _detect_content_type(self, query_lower: str) -> Optional[str]:
        """
        Detect content type hint from query.

        Args:
            query_lower: Lowercase query string

        Returns:
            Content type value or None
        """
        for content_type, keywords in self.CONTENT_TYPE_KEYWORDS.items():
            if any(keyword in query_lower for keyword in keywords):
                return content_type
        return None

    def _clean_semantic_query(self, query: str) -> str:
        """
        Clean query for semantic search.

        Removes excessive whitespace while preserving the original meaning.
        The query is kept largely intact as the vector model should handle
        natural language well.

        Args:
            query: Original query string

        Returns:
            Cleaned query suitable for vector search
        """
        # Normalize whitespace
        cleaned = " ".join(query.split())
        return cleaned.strip()


# Module-level parser instance for convenience
_default_parser: Optional[QueryParser] = None


def get_parser() -> QueryParser:
    """Get or create the default parser instance."""
    global _default_parser
    if _default_parser is None:
        _default_parser = QueryParser()
    return _default_parser


def parse_query(query: str) -> ParsedQuery:
    """
    Convenience function to parse a query using the default parser.

    Args:
        query: Natural language query string

    Returns:
        ParsedQuery with extracted metadata
    """
    return get_parser().parse(query)


# Export public interface
__all__ = [
    "ParsedQuery",
    "QueryParser",
    "parse_query",
    "get_parser",
]
