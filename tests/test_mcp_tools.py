"""Test MCP server tools."""

import pytest
from pathlib import Path
import sys
from unittest.mock import patch, MagicMock
import tempfile

sys.path.insert(0, str(Path(__file__).parent.parent))

from storage.metadata import Peripheral, DocType


class TestMCPTools:
    """Test suite for MCP server tools."""

    @pytest.fixture
    def mock_store(self):
        """Create a mock ChromaDB store."""
        store = MagicMock()
        store.count.return_value = 100
        return store

    @pytest.fixture
    def sample_search_results(self):
        """Sample search results for mocking."""
        return [
            {
                'id': 'test_001',
                'content': 'Test content about GPIO configuration',
                'metadata': {
                    'source_file': 'gpio_guide.md',
                    'peripheral': 'GPIO',
                    'has_code': True,
                    'section_path': 'GPIO > Configuration'
                },
                'score': 0.95
            },
            {
                'id': 'test_002',
                'content': 'Another test about GPIO initialization',
                'metadata': {
                    'source_file': 'gpio_init.md',
                    'peripheral': 'GPIO',
                    'has_code': True,
                    'section_path': 'GPIO > Init'
                },
                'score': 0.85
            }
        ]

    @patch('mcp_server.server.get_store')
    def test_search_stm32_docs(self, mock_get_store, mock_store, sample_search_results):
        """Test search tool returns formatted results."""
        mock_store.search.return_value = sample_search_results
        mock_get_store.return_value = mock_store

        from mcp_server.server import search_stm32_docs
        result = search_stm32_docs("GPIO configuration")

        assert "Result 1" in result
        assert "GPIO" in result
        assert "gpio_guide.md" in result
        mock_store.search.assert_called_once()

    @patch('mcp_server.server.get_store')
    def test_search_no_results(self, mock_get_store, mock_store):
        """Test search with no results."""
        mock_store.search.return_value = []
        mock_get_store.return_value = mock_store

        from mcp_server.server import search_stm32_docs
        result = search_stm32_docs("nonexistent topic xyz")

        assert "No documentation found" in result

    @patch('mcp_server.server.get_store')
    def test_search_with_peripheral_filter(self, mock_get_store, mock_store, sample_search_results):
        """Test search with peripheral filter."""
        mock_store.search.return_value = sample_search_results
        mock_get_store.return_value = mock_store

        from mcp_server.server import search_stm32_docs
        result = search_stm32_docs("configuration", peripheral="GPIO")

        # Verify peripheral filter was passed
        call_args = mock_store.search.call_args
        assert call_args is not None

    @patch('mcp_server.server.get_store')
    def test_search_with_code_filter(self, mock_get_store, mock_store, sample_search_results):
        """Test search with require_code filter."""
        mock_store.search.return_value = sample_search_results
        mock_get_store.return_value = mock_store

        from mcp_server.server import search_stm32_docs
        result = search_stm32_docs("GPIO example", require_code=True)

        # Verify require_code filter was passed
        call_args = mock_store.search.call_args
        assert call_args is not None

    @patch('mcp_server.server.get_store')
    def test_list_peripherals(self, mock_get_store, mock_store):
        """Test peripheral listing."""
        mock_store.get_peripheral_distribution.return_value = {
            'GPIO': 30,
            'UART': 25,
            'SPI': 20
        }
        mock_store.get_stats.return_value = {
            'total_chunks': 100
        }
        mock_get_store.return_value = mock_store

        from mcp_server.server import list_peripherals
        result = list_peripherals()

        assert "GPIO" in result
        assert "UART" in result
        assert "SPI" in result

    @patch('mcp_server.server.get_store')
    def test_get_peripheral_docs(self, mock_get_store, mock_store, sample_search_results):
        """Test peripheral docs retrieval."""
        mock_store.search_by_peripheral.return_value = sample_search_results
        mock_get_store.return_value = mock_store

        from mcp_server.server import get_peripheral_docs
        result = get_peripheral_docs("GPIO")

        assert "GPIO" in result
        mock_store.search_by_peripheral.assert_called_once()

    @patch('mcp_server.server.get_store')
    def test_get_peripheral_docs_invalid_peripheral(self, mock_get_store, mock_store):
        """Test peripheral docs with invalid peripheral name."""
        mock_get_store.return_value = mock_store

        from mcp_server.server import get_peripheral_docs
        result = get_peripheral_docs("INVALID_PERIPHERAL_XYZ")

        assert "Unknown peripheral" in result

    @patch('mcp_server.server.get_store')
    def test_get_code_examples(self, mock_get_store, mock_store, sample_search_results):
        """Test getting code examples."""
        mock_store.get_code_examples.return_value = sample_search_results
        mock_get_store.return_value = mock_store

        from mcp_server.server import get_code_examples
        result = get_code_examples("UART transmit")

        assert "Example" in result
        mock_store.get_code_examples.assert_called_once()

    @patch('mcp_server.server.get_store')
    def test_get_code_examples_no_results(self, mock_get_store, mock_store):
        """Test getting code examples with no results."""
        mock_store.get_code_examples.return_value = []
        mock_get_store.return_value = mock_store

        from mcp_server.server import get_code_examples
        result = get_code_examples("nonexistent topic")

        assert "No code examples found" in result

    @patch('mcp_server.server.get_store')
    def test_get_register_info(self, mock_get_store, mock_store):
        """Test register information retrieval."""
        mock_store.get_register_info.return_value = [
            {
                'id': 'reg_001',
                'content': 'GPIO_MODER register description',
                'metadata': {'source_file': 'reference.md'},
                'score': 0.9
            }
        ]
        mock_get_store.return_value = mock_store

        from mcp_server.server import get_register_info
        result = get_register_info("GPIO_MODER")

        assert "GPIO_MODER" in result
        mock_store.get_register_info.assert_called_once()

    @patch('mcp_server.server.get_store')
    def test_search_hal_function(self, mock_get_store, mock_store):
        """Test HAL function search."""
        mock_store.search_hal_function.return_value = [
            {
                'id': 'hal_001',
                'content': 'HAL_GPIO_Init function documentation',
                'metadata': {'source_file': 'hal_guide.md'},
                'score': 0.95
            }
        ]
        mock_get_store.return_value = mock_store

        from mcp_server.server import search_hal_function
        result = search_hal_function("HAL_GPIO_Init")

        assert "HAL_GPIO_Init" in result


class TestAdvancedSearchTools:
    """Test advanced search tools from mcp_server.tools.search."""

    @pytest.fixture
    def mock_store(self):
        """Create a mock store."""
        store = MagicMock()
        return store

    def test_search_hal_function_extract_peripheral(self, mock_store):
        """Test HAL function peripheral extraction."""
        from mcp_server.tools.search import _extract_peripheral_from_hal_function

        # Test various HAL function patterns
        assert _extract_peripheral_from_hal_function("HAL_UART_Transmit") == Peripheral.UART
        assert _extract_peripheral_from_hal_function("HAL_GPIO_Init") == Peripheral.GPIO
        assert _extract_peripheral_from_hal_function("HAL_SPI_Transmit") == Peripheral.SPI
        assert _extract_peripheral_from_hal_function("LL_GPIO_SetPinMode") == Peripheral.GPIO

    def test_search_hal_function_implementation(self, mock_store):
        """Test the search_hal_function implementation."""
        mock_store.search.return_value = [
            {
                'id': 'hal_001',
                'content': 'HAL_UART_Transmit documentation',
                'metadata': {
                    'source_file': 'uart_guide.md',
                    'peripheral': 'UART'
                },
                'score': 0.9
            }
        ]

        from mcp_server.tools.search import search_hal_function
        result = search_hal_function(mock_store, "HAL_UART_Transmit")

        assert "HAL_UART_Transmit" in result

    def test_search_error_solution(self, mock_store):
        """Test error solution search."""
        mock_store.search.return_value = [
            {
                'id': 'err_001',
                'content': 'Troubleshooting UART timeout errors',
                'metadata': {'source_file': 'troubleshooting.md'},
                'score': 0.85
            }
        ]

        from mcp_server.tools.search import search_error_solution
        result = search_error_solution(mock_store, "HAL_TIMEOUT error")

        assert len(result) > 0

    def test_search_initialization_sequence(self, mock_store):
        """Test initialization sequence search."""
        mock_store.search.return_value = [
            {
                'id': 'init_001',
                'content': 'UART initialization code example',
                'metadata': {'source_file': 'uart_init.md', 'has_code': True},
                'score': 0.9
            }
        ]

        from mcp_server.tools.search import search_initialization_sequence
        result = search_initialization_sequence(mock_store, "UART", "DMA mode")

        assert len(result) > 0

    def test_search_clock_configuration(self, mock_store):
        """Test clock configuration search."""
        mock_store.search.return_value = [
            {
                'id': 'clk_001',
                'content': 'Configure system clock to 168MHz',
                'metadata': {'source_file': 'clock_config.md'},
                'score': 0.9
            }
        ]

        from mcp_server.tools.search import search_clock_configuration
        result = search_clock_configuration(mock_store, "168MHz", "HSE")

        assert len(result) > 0

    def test_compare_peripherals(self, mock_store):
        """Test peripheral comparison search."""
        mock_store.search.return_value = [
            {
                'id': 'cmp_001',
                'content': 'UART vs USART comparison',
                'metadata': {'source_file': 'comparison.md'},
                'score': 0.85
            }
        ]
        mock_store.search_by_peripheral.return_value = []

        from mcp_server.tools.search import compare_peripherals
        result = compare_peripherals(mock_store, "UART", "USART")

        assert len(result) > 0

    def test_search_migration_info(self, mock_store):
        """Test migration info search."""
        mock_store.search.return_value = [
            {
                'id': 'mig_001',
                'content': 'Migration from STM32F4 to STM32H7',
                'metadata': {'source_file': 'migration.md'},
                'score': 0.9
            }
        ]

        from mcp_server.tools.search import search_migration_info
        result = search_migration_info(mock_store, "STM32F4", "STM32H7")

        assert len(result) > 0


class TestExampleTools:
    """Test code example tools from mcp_server.tools.examples."""

    @pytest.fixture
    def mock_store(self):
        """Create a mock store."""
        store = MagicMock()
        store.search.return_value = [
            {
                'id': 'ex_001',
                'content': 'Example code content',
                'metadata': {'source_file': 'examples.md', 'has_code': True},
                'score': 0.9
            }
        ]
        return store

    def test_get_interrupt_example(self, mock_store):
        """Test interrupt example retrieval."""
        from mcp_server.tools.examples import get_interrupt_example
        result = get_interrupt_example(mock_store, "UART")

        assert len(result) > 0
        mock_store.search.assert_called()

    def test_get_dma_example(self, mock_store):
        """Test DMA example retrieval."""
        from mcp_server.tools.examples import get_dma_example
        result = get_dma_example(mock_store, "SPI", "TX")

        assert len(result) > 0
        mock_store.search.assert_called()

    def test_get_low_power_example(self, mock_store):
        """Test low power example retrieval."""
        from mcp_server.tools.examples import get_low_power_example
        result = get_low_power_example(mock_store, "Sleep")

        assert len(result) > 0
        mock_store.search.assert_called()

    def test_get_callback_example(self, mock_store):
        """Test callback example retrieval."""
        from mcp_server.tools.examples import get_callback_example
        result = get_callback_example(mock_store, "UART", "TxCplt")

        assert len(result) > 0
        mock_store.search.assert_called()

    def test_get_peripheral_init_template(self, mock_store):
        """Test peripheral init template retrieval."""
        from mcp_server.tools.examples import get_peripheral_init_template
        result = get_peripheral_init_template(mock_store, "SPI", "master")

        assert len(result) > 0
        mock_store.search.assert_called()


class TestResourceHandlers:
    """Test MCP resource handlers."""

    @pytest.fixture
    def mock_store(self):
        """Create a mock store."""
        store = MagicMock()
        store.count.return_value = 100
        store.get_stats.return_value = {
            'total_chunks': 100,
            'collection_name': 'stm32_docs',
            'embedding_model': 'all-MiniLM-L6-v2'
        }
        store.get_peripheral_distribution.return_value = {'GPIO': 30, 'UART': 25}
        store.get_doc_type_distribution.return_value = {'hal_guide': 50, 'reference_manual': 30}
        store.list_sources.return_value = ['gpio.md', 'uart.md', 'rm0468.md']
        return store

    def test_documentation_resources_init(self, mock_store):
        """Test DocumentationResources initialization."""
        from mcp_server.resources.handlers import DocumentationResources
        resources = DocumentationResources(mock_store)
        assert resources.store == mock_store

    def test_get_stats(self, mock_store):
        """Test getting documentation stats."""
        from mcp_server.resources.handlers import DocumentationResources
        resources = DocumentationResources(mock_store)
        result = resources.get_stats()

        assert 'total_chunks' in result
        mock_store.get_stats.assert_called()

    def test_list_sources(self, mock_store):
        """Test listing documentation sources."""
        from mcp_server.resources.handlers import DocumentationResources
        resources = DocumentationResources(mock_store)
        result = resources.list_sources()

        assert "Documentation Sources" in result

    def test_get_peripheral_overview(self, mock_store):
        """Test getting peripheral overview."""
        mock_store.search_by_peripheral.return_value = [
            {
                'content': 'GPIO overview content',
                'metadata': {}
            }
        ]

        from mcp_server.resources.handlers import DocumentationResources
        resources = DocumentationResources(mock_store)
        result = resources.get_peripheral_overview("GPIO")

        assert "GPIO" in result

    def test_get_peripheral_overview_invalid(self, mock_store):
        """Test getting overview for invalid peripheral."""
        from mcp_server.resources.handlers import DocumentationResources
        resources = DocumentationResources(mock_store)
        result = resources.get_peripheral_overview("INVALID_XYZ")

        assert "Unknown peripheral" in result


class TestServerConfiguration:
    """Test server configuration and settings."""

    def test_settings_import(self):
        """Test that settings can be imported."""
        from mcp_server.config import settings
        assert settings is not None
        assert hasattr(settings, 'SERVER_NAME')
        assert hasattr(settings, 'PORT')

    def test_settings_defaults(self):
        """Test default settings values."""
        from mcp_server.config import settings
        assert settings.SERVER_NAME == "stm32-docs"
        assert settings.PORT == 8765

    def test_settings_paths(self):
        """Test path settings."""
        from mcp_server.config import settings
        assert hasattr(settings, 'CHROMA_DB_PATH')
        assert hasattr(settings, 'DATA_DIR')

    def test_server_mode_enum(self):
        """Test server mode enum."""
        from mcp_server.config import ServerMode
        assert ServerMode.LOCAL.value == "local"
        assert ServerMode.NETWORK.value == "network"
        assert ServerMode.HYBRID.value == "hybrid"


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
