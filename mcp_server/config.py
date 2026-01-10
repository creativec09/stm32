"""
STM32 MCP Documentation Server - Configuration

This module provides comprehensive configuration for the MCP server,
supporting both local (stdio) and network (HTTP/SSE via Tailscale) modes.

Configuration can be set via:
1. Environment variables (prefixed with STM32_)
2. .env file in the project root
3. Default values defined here

Example .env file:
    STM32_SERVER_MODE=network
    STM32_HOST=0.0.0.0
    STM32_PORT=8765
    STM32_EMBEDDING_MODEL=all-MiniLM-L6-v2
"""

from __future__ import annotations

import os
from enum import Enum
from pathlib import Path
from typing import Optional

from pydantic import Field, field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict


class ServerMode(str, Enum):
    """Server transport mode."""

    LOCAL = "local"  # stdio transport for local Claude Code
    NETWORK = "network"  # HTTP/SSE transport for Tailscale network access
    HYBRID = "hybrid"  # Both local and network (default)


class LogLevel(str, Enum):
    """Logging level configuration."""

    DEBUG = "DEBUG"
    INFO = "INFO"
    WARNING = "WARNING"
    ERROR = "ERROR"
    CRITICAL = "CRITICAL"


class EmbeddingModel(str, Enum):
    """Supported embedding models."""

    MINILM_L6 = "all-MiniLM-L6-v2"  # Fast, 384 dimensions
    MINILM_L12 = "all-MiniLM-L12-v2"  # Better quality, 384 dimensions
    MPNET = "all-mpnet-base-v2"  # Best quality, 768 dimensions
    E5_SMALL = "intfloat/e5-small-v2"  # Efficient, 384 dimensions
    E5_BASE = "intfloat/e5-base-v2"  # Good balance, 768 dimensions
    NOMIC_V15 = "nomic-ai/nomic-embed-text-v1.5"  # High quality, 768 dimensions, Matryoshka


class Settings(BaseSettings):
    """
    Main configuration settings for the STM32 MCP Documentation Server.

    All settings can be overridden via environment variables with STM32_ prefix.
    """

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        env_prefix="STM32_",
        case_sensitive=False,
        extra="ignore",
    )

    # =========================================================================
    # Path Configuration
    # =========================================================================

    PROJECT_ROOT: Path = Field(
        default_factory=lambda: Path(__file__).parent.parent.resolve(),
        description="Root directory of the project",
    )

    @property
    def DATA_DIR(self) -> Path:
        """Directory for all data storage."""
        return self.PROJECT_ROOT / "data"

    @property
    def RAW_DOCS_DIR(self) -> Path:
        """Directory containing raw markdown documentation files.

        The markdowns are bundled inside the mcp_server package to ensure
        they are available when installed via pip/uvx.
        """
        # Markdowns are inside the mcp_server package
        package_dir = Path(__file__).parent
        return package_dir / "markdowns"

    @property
    def CHUNKS_DIR(self) -> Path:
        """Directory for processed chunk JSON files."""
        return self.DATA_DIR / "chunks"

    @property
    def CHROMA_DB_PATH(self) -> Path:
        """Directory for ChromaDB persistent storage."""
        return self.DATA_DIR / "chroma_db"

    @property
    def LOGS_DIR(self) -> Path:
        """Directory for log files."""
        return self.PROJECT_ROOT / "logs"

    # =========================================================================
    # Server Configuration
    # =========================================================================

    SERVER_MODE: ServerMode = Field(
        default=ServerMode.HYBRID,
        description="Server transport mode: local, network, or hybrid",
    )

    HOST: str = Field(
        default="0.0.0.0",
        description="Host to bind for network mode (0.0.0.0 for all interfaces)",
    )

    PORT: int = Field(
        default=8765,
        description="Port for network mode HTTP/SSE server",
        ge=1024,
        le=65535,
    )

    SERVER_NAME: str = Field(
        default="stm32-docs",
        description="MCP server name for identification",
    )

    SERVER_VERSION: str = Field(
        default="1.0.0",
        description="Server version string",
    )

    SERVER_DESCRIPTION: str = Field(
        default="STM32 documentation search and retrieval via MCP",
        description="Server description for MCP protocol",
    )

    # =========================================================================
    # Tailscale / Network Configuration
    # =========================================================================

    TAILSCALE_HOSTNAME: Optional[str] = Field(
        default=None,
        description="Tailscale hostname for the server (e.g., 'stm32-docs-server')",
    )

    ALLOWED_TAILSCALE_IPS: list[str] = Field(
        default_factory=list,
        description="List of allowed Tailscale IPs (empty = allow all Tailscale IPs)",
    )

    CORS_ORIGINS: list[str] = Field(
        default_factory=lambda: ["*"],
        description="Allowed CORS origins for network mode",
    )

    API_KEY: Optional[str] = Field(
        default=None,
        description="Optional API key for network authentication",
    )

    # =========================================================================
    # Database Download Configuration
    # =========================================================================

    GITHUB_REPO: str = Field(
        default="creativec09/stm32",
        description="GitHub repository for downloading pre-built database",
    )

    DB_ASSET_NAME: str = Field(
        default="chromadb-stm32-docs.tar.gz",
        description="Name of the database asset in GitHub releases",
    )

    DB_MANIFEST_NAME: str = Field(
        default="chromadb-manifest.json",
        description="Name of the manifest file in GitHub releases",
    )

    ENABLE_AUTO_DOWNLOAD: bool = Field(
        default=True,
        description="Automatically download database on first run",
    )

    DOWNLOAD_TIMEOUT: int = Field(
        default=300,
        description="Timeout for database download in seconds",
        ge=30,
        le=600,
    )

    # =========================================================================
    # Chunking Configuration
    # =========================================================================

    CHUNK_SIZE: int = Field(
        default=1000,
        description="Target chunk size in tokens",
        ge=100,
        le=4000,
    )

    CHUNK_OVERLAP: int = Field(
        default=150,
        description="Overlap between chunks in tokens",
        ge=0,
        le=500,
    )

    MIN_CHUNK_SIZE: int = Field(
        default=50,
        description="Minimum chunk size in tokens",
        ge=10,
        le=500,
    )

    MAX_CHUNK_SIZE: int = Field(
        default=2000,
        description="Maximum chunk size in tokens (for oversized content)",
        ge=500,
        le=8000,
    )

    PRESERVE_CODE_BLOCKS: bool = Field(
        default=True,
        description="Never split code blocks across chunks",
    )

    PRESERVE_TABLES: bool = Field(
        default=True,
        description="Never split tables across chunks",
    )

    # =========================================================================
    # Embedding Configuration
    # =========================================================================

    EMBEDDING_MODEL: str = Field(
        default=EmbeddingModel.NOMIC_V15.value,
        description="Sentence transformer model for embeddings",
    )

    EMBEDDING_BATCH_SIZE: int = Field(
        default=32,
        description="Batch size for embedding generation",
        ge=1,
        le=256,
    )

    EMBEDDING_DEVICE: str = Field(
        default="cpu",
        description="Device for embeddings: cpu, cuda, mps",
    )

    NORMALIZE_EMBEDDINGS: bool = Field(
        default=True,
        description="Normalize embedding vectors",
    )

    # Task prefixes for nomic-embed-text models
    EMBEDDING_TASK_PREFIX_DOC: str = Field(
        default="search_document: ",
        description="Task prefix for document indexing (nomic models)",
    )

    EMBEDDING_TASK_PREFIX_QUERY: str = Field(
        default="search_query: ",
        description="Task prefix for search queries (nomic models)",
    )

    USE_TASK_PREFIXES: bool = Field(
        default=True,
        description="Use task prefixes for embedding (required for nomic models)",
    )

    # =========================================================================
    # Hybrid Search Configuration
    # =========================================================================

    ENABLE_HYBRID_SEARCH: bool = Field(
        default=True,
        description="Enable hybrid search combining vector and BM25",
    )

    RRF_K: int = Field(
        default=60,
        description="Reciprocal Rank Fusion constant k",
        ge=1,
        le=100,
    )

    MIN_BM25_SCORE: float = Field(
        default=0.1,
        description="Minimum BM25 score to include in hybrid results",
        ge=0.0,
        le=1.0,
    )

    HYBRID_CANDIDATE_MULTIPLIER: float = Field(
        default=2.0,
        description="Multiplier for candidate retrieval in hybrid search",
        ge=1.0,
        le=5.0,
    )

    # =========================================================================
    # Re-ranker Configuration
    # =========================================================================

    ENABLE_RERANKING: bool = Field(
        default=True,
        description="Enable LLM-based re-ranking of search results",
    )

    RERANK_MODEL: str = Field(
        default="haiku",
        description="Model for re-ranking: haiku, sonnet, or opus",
    )

    RERANK_TOP_K: int = Field(
        default=5,
        description="Number of top results to return after re-ranking",
        ge=1,
        le=20,
    )

    RERANK_ALWAYS: bool = Field(
        default=True,
        description="Always re-rank results (recommended for Max 20x subscription)",
    )

    # =========================================================================
    # ChromaDB Configuration
    # =========================================================================

    COLLECTION_NAME: str = Field(
        default="stm32_docs",
        description="ChromaDB collection name",
    )

    CHROMA_DISTANCE_METRIC: str = Field(
        default="cosine",
        description="Distance metric for ChromaDB: cosine, l2, ip",
    )

    CHROMA_ANONYMIZED_TELEMETRY: bool = Field(
        default=False,
        description="Enable ChromaDB anonymous telemetry",
    )

    # =========================================================================
    # Search Configuration
    # =========================================================================

    DEFAULT_SEARCH_RESULTS: int = Field(
        default=5,
        description="Default number of search results",
        ge=1,
        le=50,
    )

    MAX_SEARCH_RESULTS: int = Field(
        default=20,
        description="Maximum number of search results",
        ge=1,
        le=100,
    )

    MIN_RELEVANCE_SCORE: float = Field(
        default=0.1,
        description="Minimum relevance score to include in results (lowered to improve recall)",
        ge=0.0,
        le=1.0,
    )

    RERANK_RESULTS: bool = Field(
        default=False,
        description="Apply reranking to search results",
    )

    # =========================================================================
    # Logging Configuration
    # =========================================================================

    LOG_LEVEL: LogLevel = Field(
        default=LogLevel.INFO,
        description="Logging level",
    )

    LOG_FORMAT: str = Field(
        default="%(asctime)s | %(levelname)-8s | %(name)s | %(message)s",
        description="Log message format",
    )

    LOG_TO_FILE: bool = Field(
        default=True,
        description="Write logs to file in addition to console",
    )

    LOG_FILE_MAX_SIZE: int = Field(
        default=10 * 1024 * 1024,  # 10 MB
        description="Maximum log file size in bytes before rotation",
    )

    LOG_FILE_BACKUP_COUNT: int = Field(
        default=5,
        description="Number of backup log files to keep",
    )

    # =========================================================================
    # Performance Configuration
    # =========================================================================

    CACHE_EMBEDDINGS: bool = Field(
        default=True,
        description="Cache embedding model in memory",
    )

    LAZY_LOAD_EMBEDDINGS: bool = Field(
        default=True,
        description="Load embedding model on first use",
    )

    CONNECTION_POOL_SIZE: int = Field(
        default=10,
        description="Maximum concurrent connections for network mode",
        ge=1,
        le=100,
    )

    REQUEST_TIMEOUT: int = Field(
        default=30,
        description="Request timeout in seconds",
        ge=5,
        le=300,
    )

    # =========================================================================
    # Validation
    # =========================================================================

    @field_validator("CHUNK_OVERLAP")
    @classmethod
    def validate_chunk_overlap(cls, v: int, info) -> int:
        """Ensure overlap is less than chunk size."""
        chunk_size = info.data.get("CHUNK_SIZE", 1000)
        if v >= chunk_size:
            raise ValueError(f"CHUNK_OVERLAP ({v}) must be less than CHUNK_SIZE ({chunk_size})")
        return v

    @field_validator("EMBEDDING_DEVICE")
    @classmethod
    def validate_embedding_device(cls, v: str) -> str:
        """Validate embedding device."""
        valid_devices = {"cpu", "cuda", "mps", "auto"}
        if v.lower() not in valid_devices:
            raise ValueError(f"EMBEDDING_DEVICE must be one of: {valid_devices}")
        return v.lower()

    # =========================================================================
    # Helper Methods
    # =========================================================================

    def ensure_directories(self) -> None:
        """Create all required directories if they don't exist."""
        directories = [
            self.DATA_DIR,
            self.RAW_DOCS_DIR,
            self.CHUNKS_DIR,
            self.CHROMA_DB_PATH,
            self.LOGS_DIR,
        ]
        for directory in directories:
            directory.mkdir(parents=True, exist_ok=True)

    def get_network_url(self) -> str:
        """Get the full network URL for the server."""
        host = self.TAILSCALE_HOSTNAME or self.HOST
        return f"http://{host}:{self.PORT}"

    def is_network_enabled(self) -> bool:
        """Check if network mode is enabled."""
        return self.SERVER_MODE in (ServerMode.NETWORK, ServerMode.HYBRID)

    def is_local_enabled(self) -> bool:
        """Check if local mode is enabled."""
        return self.SERVER_MODE in (ServerMode.LOCAL, ServerMode.HYBRID)

    def to_dict(self) -> dict:
        """Convert settings to dictionary for logging/debugging."""
        return {
            "server_mode": self.SERVER_MODE.value,
            "host": self.HOST,
            "port": self.PORT,
            "embedding_model": self.EMBEDDING_MODEL,
            "collection_name": self.COLLECTION_NAME,
            "chunk_size": self.CHUNK_SIZE,
            "chunk_overlap": self.CHUNK_OVERLAP,
            "log_level": self.LOG_LEVEL.value,
            "project_root": str(self.PROJECT_ROOT),
            "chroma_db_path": str(self.CHROMA_DB_PATH),
        }


# Global settings instance
settings = Settings()


def get_settings() -> Settings:
    """Get the global settings instance."""
    return settings


def reload_settings() -> Settings:
    """Reload settings from environment/files."""
    global settings
    settings = Settings()
    return settings


# =============================================================================
# Quick Access Constants
# =============================================================================

# Peripheral names for validation and filtering
VALID_PERIPHERALS = [
    "GPIO",
    "UART",
    "USART",
    "SPI",
    "I2C",
    "I3C",
    "ADC",
    "DAC",
    "TIM",
    "LPTIM",
    "DMA",
    "BDMA",
    "MDMA",
    "RCC",
    "PWR",
    "NVIC",
    "EXTI",
    "FLASH",
    "FMC",
    "FSMC",
    "SDMMC",
    "USB",
    "CAN",
    "FDCAN",
    "ETH",
    "LTDC",
    "DCMI",
    "RNG",
    "CRYP",
    "HASH",
    "RTC",
    "TAMP",
    "WWDG",
    "IWDG",
    "CRC",
    "CORDIC",
    "FMAC",
    "SAI",
    "SPDIF",
    "HDMI_CEC",
    "SWPMI",
    "DFSDM",
    "OCTOSPI",
    "QUADSPI",
    "XSPI",
    "MPU",
    "DMA2D",
    "JPEG",
]

# Document types for classification
VALID_DOC_TYPES = [
    "reference_manual",
    "application_note",
    "user_manual",
    "programming_manual",
    "datasheet",
    "hal_guide",
    "errata",
    "migration_guide",
    "safety_manual",
    "general",
]

# STM32 family identifiers
STM32_FAMILIES = [
    "STM32F0",
    "STM32F1",
    "STM32F2",
    "STM32F3",
    "STM32F4",
    "STM32F7",
    "STM32G0",
    "STM32G4",
    "STM32H5",
    "STM32H7",
    "STM32L0",
    "STM32L1",
    "STM32L4",
    "STM32L5",
    "STM32U5",
    "STM32WB",
    "STM32WL",
    "STM32MP1",
    "STM32N6",
]


if __name__ == "__main__":
    # Print current configuration for debugging
    import json

    print("STM32 MCP Server Configuration")
    print("=" * 60)
    print(json.dumps(settings.to_dict(), indent=2))
    print("=" * 60)
    print(f"Network URL: {settings.get_network_url()}")
    print(f"Network enabled: {settings.is_network_enabled()}")
    print(f"Local enabled: {settings.is_local_enabled()}")
