"""
Metadata schema definitions for STM32 documentation chunks.

This module defines the data models for storing and retrieving STM32 documentation
metadata in ChromaDB. The schemas support rich classification of documentation
content including peripheral types, document types, and content characteristics.
"""

from enum import Enum
from pydantic import BaseModel, Field
from typing import Optional


class DocType(str, Enum):
    """Document type classification for STM32 documentation."""

    REFERENCE_MANUAL = "reference_manual"
    APPLICATION_NOTE = "application_note"
    USER_MANUAL = "user_manual"
    PROGRAMMING_MANUAL = "programming_manual"
    DATASHEET = "datasheet"
    HAL_GUIDE = "hal_guide"
    ERRATA = "errata"
    MIGRATION_GUIDE = "migration_guide"
    SAFETY_MANUAL = "safety_manual"
    GENERAL = "general"


class Peripheral(str, Enum):
    """STM32 peripheral classifications."""

    # Communication Peripherals
    GPIO = "GPIO"
    UART = "UART"
    USART = "USART"
    SPI = "SPI"
    I2C = "I2C"
    I3C = "I3C"
    CAN = "CAN"
    FDCAN = "FDCAN"
    USB = "USB"
    ETH = "ETH"
    SPDIF = "SPDIF"

    # Analog Peripherals
    ADC = "ADC"
    DAC = "DAC"

    # Timers
    TIM = "TIM"
    LPTIM = "LPTIM"
    RTC = "RTC"
    WWDG = "WWDG"
    IWDG = "IWDG"

    # DMA
    DMA = "DMA"
    BDMA = "BDMA"
    MDMA = "MDMA"

    # System Peripherals
    RCC = "RCC"
    PWR = "PWR"
    NVIC = "NVIC"
    EXTI = "EXTI"
    FLASH = "FLASH"
    CRC = "CRC"
    TAMP = "TAMP"

    # Memory & Storage
    FMC = "FMC"
    SDMMC = "SDMMC"
    OCTOSPI = "OCTOSPI"
    QUADSPI = "QUADSPI"

    # Graphics & Display
    LTDC = "LTDC"
    DCMI = "DCMI"
    DMA2D = "DMA2D"
    JPEG = "JPEG"

    # Audio
    SAI = "SAI"

    # Security & Crypto
    RNG = "RNG"
    CRYP = "CRYP"
    HASH = "HASH"

    # Math
    CORDIC = "CORDIC"

    # System
    MPU = "MPU"
    GENERAL = "GENERAL"


class ContentType(str, Enum):
    """Content classification for documentation chunks."""

    CONCEPTUAL = "conceptual"
    REGISTER_MAP = "register_map"
    CODE_EXAMPLE = "code_example"
    CONFIGURATION = "configuration"
    TROUBLESHOOTING = "troubleshooting"
    ELECTRICAL_SPEC = "electrical_spec"
    TIMING_DIAGRAM = "timing_diagram"
    PIN_DESCRIPTION = "pin_description"


class ChunkMetadataSchema(BaseModel):
    """
    Schema for chunk metadata stored in ChromaDB.

    This schema represents all metadata associated with a documentation chunk,
    including source information, content classification, hierarchy, and
    STM32-specific information like HAL functions and register references.
    """

    # Source identification
    source_file: str = Field(..., description="Original filename")
    doc_type: DocType = Field(default=DocType.GENERAL, description="Document type")

    # Content classification
    peripheral: Optional[Peripheral] = Field(None, description="Primary peripheral")
    secondary_peripherals: list[str] = Field(
        default_factory=list,
        description="Additional peripherals mentioned in chunk"
    )
    content_type: ContentType = Field(
        default=ContentType.CONCEPTUAL,
        description="Type of content in chunk"
    )

    # Hierarchy
    section_path: list[str] = Field(
        default_factory=list,
        description="Header hierarchy path (e.g., ['GPIO', 'Configuration', 'Initialization'])"
    )
    section_title: str = Field(
        default="",
        description="Current section title"
    )

    # Content flags
    has_code: bool = Field(default=False, description="Contains code examples")
    has_table: bool = Field(default=False, description="Contains tables")
    has_register_map: bool = Field(default=False, description="Contains register maps")
    has_diagram_ref: bool = Field(default=False, description="References diagrams")

    # Position
    chunk_index: int = Field(default=0, description="Index of chunk in document")
    start_line: int = Field(default=0, description="Starting line number in source")

    # STM32 specific
    stm32_families: list[str] = Field(
        default_factory=list,
        description="STM32 families mentioned (e.g., ['STM32F4', 'STM32H7'])"
    )
    hal_functions: list[str] = Field(
        default_factory=list,
        description="HAL/LL function names mentioned"
    )
    registers: list[str] = Field(
        default_factory=list,
        description="Register names mentioned"
    )

    def to_chroma_metadata(self) -> dict:
        """
        Convert to flat dict for ChromaDB storage.

        ChromaDB only supports str, int, float, and bool types for metadata.
        Lists are converted to comma-separated strings.

        Returns:
            Flat dictionary suitable for ChromaDB metadata storage
        """
        return {
            "source_file": self.source_file,
            "doc_type": self.doc_type.value,
            "peripheral": self.peripheral.value if self.peripheral else "",
            "secondary_peripherals": ",".join(self.secondary_peripherals),
            "content_type": self.content_type.value,
            "section_path": " > ".join(self.section_path),
            "section_title": self.section_title,
            "has_code": self.has_code,
            "has_table": self.has_table,
            "has_register_map": self.has_register_map,
            "has_diagram_ref": self.has_diagram_ref,
            "chunk_index": self.chunk_index,
            "start_line": self.start_line,
            "stm32_families": ",".join(self.stm32_families),
            "hal_functions": ",".join(self.hal_functions[:10]),  # Limit for storage
            "registers": ",".join(self.registers[:15]),
        }

    @classmethod
    def from_chroma_metadata(cls, data: dict) -> "ChunkMetadataSchema":
        """
        Reconstruct from ChromaDB metadata.

        Converts the flattened ChromaDB metadata back into the full schema,
        parsing comma-separated strings back into lists and enum values.

        Args:
            data: Flat dictionary from ChromaDB

        Returns:
            ChunkMetadataSchema instance
        """
        # Parse peripheral enum
        peripheral = None
        if data.get("peripheral"):
            try:
                peripheral = Peripheral(data["peripheral"])
            except ValueError:
                peripheral = None

        # Parse lists from comma-separated strings
        secondary_peripherals = [
            p.strip() for p in data.get("secondary_peripherals", "").split(",")
            if p.strip()
        ]

        section_path = [
            s.strip() for s in data.get("section_path", "").split(">")
            if s.strip()
        ]

        stm32_families = [
            f.strip() for f in data.get("stm32_families", "").split(",")
            if f.strip()
        ]

        hal_functions = [
            f.strip() for f in data.get("hal_functions", "").split(",")
            if f.strip()
        ]

        registers = [
            r.strip() for r in data.get("registers", "").split(",")
            if r.strip()
        ]

        return cls(
            source_file=data.get("source_file", ""),
            doc_type=DocType(data.get("doc_type", "general")),
            peripheral=peripheral,
            secondary_peripherals=secondary_peripherals,
            content_type=ContentType(data.get("content_type", "conceptual")),
            section_path=section_path,
            section_title=data.get("section_title", ""),
            has_code=data.get("has_code", False),
            has_table=data.get("has_table", False),
            has_register_map=data.get("has_register_map", False),
            has_diagram_ref=data.get("has_diagram_ref", False),
            chunk_index=data.get("chunk_index", 0),
            start_line=data.get("start_line", 0),
            stm32_families=stm32_families,
            hal_functions=hal_functions,
            registers=registers,
        )


# Export all public classes
__all__ = [
    "DocType",
    "Peripheral",
    "ContentType",
    "ChunkMetadataSchema",
]
