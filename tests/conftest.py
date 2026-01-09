"""
Pytest configuration and fixtures for STM32 MCP tests.

This module provides:
- Path configuration for imports
- Shared fixtures for tests
- Test data factories
"""

import sys
import tempfile
from pathlib import Path
from typing import Generator

import pytest

# Add project root to path for imports
PROJECT_ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

# Also add mcp_server as mcp_server module path
# This handles the hyphen/underscore naming issue
MCP_SERVER_PATH = PROJECT_ROOT / "mcp_server"
if MCP_SERVER_PATH.exists():
    sys.path.insert(0, str(MCP_SERVER_PATH.parent))
    # Create module alias
    if "mcp_server" not in sys.modules:
        import importlib.util
        spec = importlib.util.spec_from_file_location(
            "mcp_server",
            MCP_SERVER_PATH / "__init__.py"
        )
        if spec and spec.loader:
            mcp_server_module = importlib.util.module_from_spec(spec)
            sys.modules["mcp_server"] = mcp_server_module
            # Don't execute the module, just register it


# ============================================================================
# FIXTURES - Shared test fixtures
# ============================================================================

@pytest.fixture
def project_root() -> Path:
    """Return the project root path."""
    return PROJECT_ROOT


@pytest.fixture
def sample_markdown() -> str:
    """Return sample markdown content for testing."""
    return '''
# GPIO Configuration

## Overview

The GPIO peripheral provides general purpose input/output functionality.

## Register Map

| Register | Offset | Description |
|----------|--------|-------------|
| MODER    | 0x00   | Mode register |
| OTYPER   | 0x04   | Output type |

## Code Example

```c
GPIO_InitTypeDef gpio = {0};
gpio.Pin = GPIO_PIN_5;
gpio.Mode = GPIO_MODE_OUTPUT_PP;
HAL_GPIO_Init(GPIOA, &gpio);
```

## HAL Functions

- HAL_GPIO_Init()
- HAL_GPIO_WritePin()
'''


@pytest.fixture
def sample_uart_content() -> str:
    """Return sample UART documentation content."""
    return '''
# UART Configuration

## Overview

The UART peripheral provides asynchronous serial communication.

## Initialization

Configure UART for 115200 baud rate with 8N1 settings:

```c
UART_HandleTypeDef huart;
huart.Instance = USART1;
huart.Init.BaudRate = 115200;
huart.Init.WordLength = UART_WORDLENGTH_8B;
huart.Init.StopBits = UART_STOPBITS_1;
huart.Init.Parity = UART_PARITY_NONE;
huart.Init.Mode = UART_MODE_TX_RX;
HAL_UART_Init(&huart);
```

## HAL Functions

- HAL_UART_Init()
- HAL_UART_Transmit()
- HAL_UART_Receive()
'''


@pytest.fixture
def temp_dir() -> Generator[Path, None, None]:
    """Create a temporary directory for test files."""
    with tempfile.TemporaryDirectory() as tmpdir:
        yield Path(tmpdir)


@pytest.fixture
def chunker():
    """Create a chunker instance for testing."""
    try:
        from pipeline.chunker import STM32Chunker, ChunkingConfig
        return STM32Chunker(ChunkingConfig())
    except ImportError:
        pytest.skip("pipeline.chunker not available")


@pytest.fixture
def validator():
    """Create a validator instance for testing."""
    try:
        from pipeline.validator import ChunkValidator
        return ChunkValidator()
    except ImportError:
        pytest.skip("pipeline.validator not available")


# ============================================================================
# MARKERS - Custom pytest markers
# ============================================================================

def pytest_configure(config):
    """Configure custom markers."""
    config.addinivalue_line(
        "markers", "slow: marks tests as slow (deselect with '-m \"not slow\"')"
    )
    config.addinivalue_line(
        "markers", "integration: marks tests as integration tests"
    )
    config.addinivalue_line(
        "markers", "requires_chromadb: marks tests requiring ChromaDB"
    )
    config.addinivalue_line(
        "markers", "requires_network: marks tests requiring network access"
    )


# ============================================================================
# SKIP HELPERS - Skip tests based on availability
# ============================================================================

def pytest_collection_modifyitems(config, items):
    """Modify test collection based on available modules."""
    skip_chromadb = pytest.mark.skip(reason="chromadb not available")
    skip_mcp = pytest.mark.skip(reason="mcp module not available")

    for item in items:
        if "requires_chromadb" in item.keywords:
            try:
                import chromadb
            except ImportError:
                item.add_marker(skip_chromadb)

        if "test_mcp" in item.nodeid or "mcp_tools" in item.nodeid:
            try:
                import mcp
            except ImportError:
                item.add_marker(skip_mcp)
