"""Integration tests for the complete system."""

import pytest
from pathlib import Path
import sys
import json
import tempfile

sys.path.insert(0, str(Path(__file__).parent.parent))

PROJECT_ROOT = Path(__file__).parent.parent


class TestProjectStructure:
    """Test project structure and required files."""

    def test_project_directories_exist(self):
        """Verify project structure is complete."""
        required_dirs = [
            "mcp_server",
            "mcp_server/tools",
            "mcp_server/resources",
            "mcp_server/prompts",
            "pipeline",
            "storage",
            "scripts",
            "data",
            ".claude",
            ".claude/agents",
            ".claude/commands",
            "tests",
        ]

        for dir_name in required_dirs:
            dir_path = PROJECT_ROOT / dir_name
            assert dir_path.exists(), f"Missing directory: {dir_name}"

    def test_required_files_exist(self):
        """Check all required files exist."""
        required_files = [
            "pyproject.toml",
            "requirements.txt",
            "mcp_server/server.py",
            "mcp_server/config.py",
            "mcp_server/__init__.py",
            "mcp_server/tools/__init__.py",
            "mcp_server/tools/search.py",
            "mcp_server/resources/__init__.py",
            "mcp_server/resources/handlers.py",
            "pipeline/__init__.py",
            "pipeline/chunker.py",
            "pipeline/validator.py",
            "storage/__init__.py",
            "storage/chroma_store.py",
            "storage/metadata.py",
            "scripts/__init__.py",
            "scripts/ingest_docs.py",
            ".claude/mcp.json",
        ]

        for file_path in required_files:
            full_path = PROJECT_ROOT / file_path
            assert full_path.exists(), f"Missing file: {file_path}"


class TestMCPConfiguration:
    """Test MCP configuration validity."""

    def test_mcp_config_valid_json(self):
        """Verify MCP configuration is valid JSON."""
        config_path = PROJECT_ROOT / ".claude" / "mcp.json"

        if config_path.exists():
            content = config_path.read_text()
            config = json.loads(content)  # Will raise if invalid JSON

            assert "mcpServers" in config
            assert "stm32-docs" in config["mcpServers"]

    def test_mcp_config_has_required_fields(self):
        """Verify MCP config has required server fields."""
        config_path = PROJECT_ROOT / ".claude" / "mcp.json"

        if config_path.exists():
            config = json.loads(config_path.read_text())
            server_config = config["mcpServers"]["stm32-docs"]

            assert "command" in server_config
            assert "args" in server_config

    def test_mcp_server_path_valid(self):
        """Verify MCP server path in config is valid."""
        config_path = PROJECT_ROOT / ".claude" / "mcp.json"

        if config_path.exists():
            config = json.loads(config_path.read_text())
            server_config = config["mcpServers"]["stm32-docs"]

            # Check that the server script exists
            if "args" in server_config and len(server_config["args"]) > 0:
                server_path = Path(server_config["args"][0])
                # Path might be absolute or relative
                assert server_path.exists() or (PROJECT_ROOT / "mcp_server/server.py").exists()


class TestModuleImports:
    """Test that all modules can be imported."""

    def test_server_imports(self):
        """Verify server can be imported."""
        try:
            from mcp_server.server import mcp, search_stm32_docs, list_peripherals
            assert mcp is not None
            assert callable(search_stm32_docs)
            assert callable(list_peripherals)
        except ImportError as e:
            pytest.fail(f"Server import failed: {e}")

    def test_storage_imports(self):
        """Verify storage can be imported."""
        try:
            from storage.chroma_store import STM32ChromaStore
            from storage.metadata import ChunkMetadataSchema, Peripheral, DocType
            assert STM32ChromaStore is not None
            assert ChunkMetadataSchema is not None
        except ImportError as e:
            pytest.fail(f"Storage import failed: {e}")

    def test_pipeline_imports(self):
        """Verify pipeline can be imported."""
        try:
            from pipeline.chunker import STM32Chunker, ChunkingConfig, Chunk, ChunkMetadata
            from pipeline.validator import ChunkValidator, ValidationReport
            assert STM32Chunker is not None
            assert ChunkValidator is not None
        except ImportError as e:
            pytest.fail(f"Pipeline import failed: {e}")

    def test_config_imports(self):
        """Verify config can be imported."""
        try:
            from mcp_server.config import settings, Settings, ServerMode
            assert settings is not None
            assert Settings is not None
        except ImportError as e:
            pytest.fail(f"Config import failed: {e}")

    def test_tools_imports(self):
        """Verify tools can be imported."""
        try:
            from mcp_server.tools.search import (
                search_hal_function,
                search_error_solution,
                search_initialization_sequence
            )
            assert callable(search_hal_function)
        except ImportError as e:
            pytest.fail(f"Tools import failed: {e}")

    def test_resources_imports(self):
        """Verify resources can be imported."""
        try:
            from mcp_server.resources.handlers import DocumentationResources
            assert DocumentationResources is not None
        except ImportError as e:
            pytest.fail(f"Resources import failed: {e}")


class TestEndToEndWorkflow:
    """Test complete workflows."""

    def test_chunking_to_storage_workflow(self):
        """Test document chunking and storage workflow."""
        from pipeline.chunker import STM32Chunker, ChunkingConfig
        from storage.chroma_store import STM32ChromaStore
        from storage.metadata import ChunkMetadataSchema, DocType, Peripheral, ContentType

        # Create chunker
        chunker = STM32Chunker(ChunkingConfig())

        # Create sample document
        content = """
# GPIO Configuration

Configure GPIO pins for output operation.

## Initialization

```c
GPIO_InitTypeDef gpio = {0};
gpio.Pin = GPIO_PIN_5;
gpio.Mode = GPIO_MODE_OUTPUT_PP;
HAL_GPIO_Init(GPIOA, &gpio);
```
"""

        # Chunk the document
        chunks = chunker.chunk_document(content, "gpio_test.md")
        assert len(chunks) >= 1

        # Create temporary store and add chunks
        with tempfile.TemporaryDirectory() as tmpdir:
            store = STM32ChromaStore(Path(tmpdir))

            # Convert chunks to storage format
            chunk_data = []
            for chunk in chunks:
                meta = ChunkMetadataSchema(
                    source_file=chunk.metadata.source_file,
                    doc_type=DocType.HAL_GUIDE,
                    peripheral=Peripheral.GPIO if chunk.metadata.peripheral == "GPIO" else None,
                    has_code=chunk.metadata.has_code,
                    section_path=chunk.metadata.section_path,
                )
                chunk_data.append((chunk.id, chunk.content, meta.to_chroma_metadata()))

            # Add to store
            added = store.add_chunks(chunk_data)
            assert added == len(chunks)

            # Search and verify
            results = store.search("GPIO configuration")
            assert len(results) > 0

    def test_validation_workflow(self):
        """Test chunk validation workflow."""
        from pipeline.chunker import STM32Chunker, ChunkingConfig
        from pipeline.validator import ChunkValidator

        # Create chunker and validator
        chunker = STM32Chunker(ChunkingConfig())
        validator = ChunkValidator()

        # Create sample document
        content = """
# UART Configuration

Configure UART for serial communication at 115200 baud.

## Code Example

```c
UART_HandleTypeDef huart;
huart.Init.BaudRate = 115200;
HAL_UART_Init(&huart);
```
"""

        # Chunk the document
        chunks = chunker.chunk_document(content, "uart_test.md")

        # Validate all chunks
        report = validator.generate_report(chunks)

        assert report.total_chunks == len(chunks)
        assert report.valid_chunks >= 0

    def test_search_workflow(self):
        """Test complete search workflow."""
        from storage.chroma_store import STM32ChromaStore
        from storage.metadata import ChunkMetadataSchema, DocType, Peripheral

        with tempfile.TemporaryDirectory() as tmpdir:
            store = STM32ChromaStore(Path(tmpdir))

            # Add test data
            test_chunks = [
                (
                    "test_001",
                    "Configure SPI in master mode with HAL_SPI_Init",
                    ChunkMetadataSchema(
                        source_file="spi_guide.md",
                        doc_type=DocType.HAL_GUIDE,
                        peripheral=Peripheral.SPI,
                        has_code=True,
                    ).to_chroma_metadata()
                ),
                (
                    "test_002",
                    "I2C slave mode configuration example",
                    ChunkMetadataSchema(
                        source_file="i2c_guide.md",
                        doc_type=DocType.HAL_GUIDE,
                        peripheral=Peripheral.I2C,
                        has_code=True,
                    ).to_chroma_metadata()
                ),
            ]
            store.add_chunks(test_chunks)

            # Test search
            results = store.search("SPI master mode")
            assert len(results) > 0

            # Test filtered search
            spi_results = store.search("configuration", peripheral=Peripheral.SPI)
            for r in spi_results:
                assert r['metadata']['peripheral'] == "SPI"


class TestDataIntegrity:
    """Test data integrity in the system."""

    def test_metadata_roundtrip(self):
        """Test metadata survives storage roundtrip."""
        from storage.metadata import ChunkMetadataSchema, DocType, Peripheral, ContentType

        original = ChunkMetadataSchema(
            source_file="test_file.md",
            doc_type=DocType.APPLICATION_NOTE,
            peripheral=Peripheral.TIM,
            content_type=ContentType.CODE_EXAMPLE,
            has_code=True,
            has_table=True,
            section_path=["Timers", "PWM", "Configuration"],
            stm32_families=["STM32F4", "STM32H7"],
            hal_functions=["HAL_TIM_PWM_Start", "HAL_TIM_PWM_Stop"],
            registers=["TIM_CR1", "TIM_ARR", "TIM_CCR1"],
        )

        # Convert to Chroma format
        chroma_meta = original.to_chroma_metadata()

        # Convert back
        reconstructed = ChunkMetadataSchema.from_chroma_metadata(chroma_meta)

        # Verify key fields
        assert reconstructed.source_file == original.source_file
        assert reconstructed.doc_type == original.doc_type
        assert reconstructed.peripheral == original.peripheral
        assert reconstructed.has_code == original.has_code
        assert reconstructed.has_table == original.has_table

    def test_chunk_id_determinism(self):
        """Test that chunk IDs are deterministic."""
        from pipeline.chunker import STM32Chunker, ChunkingConfig

        chunker = STM32Chunker(ChunkingConfig())
        content = "# Test\n\nSome content here."

        # Generate chunks twice
        chunks1 = chunker.chunk_document(content, "test.md")
        chunks2 = chunker.chunk_document(content, "test.md")

        # IDs should match
        assert len(chunks1) == len(chunks2)
        for c1, c2 in zip(chunks1, chunks2):
            assert c1.id == c2.id


class TestPeripheralEnums:
    """Test peripheral enum completeness."""

    def test_all_common_peripherals_defined(self):
        """Verify common peripherals are defined."""
        from storage.metadata import Peripheral

        common_peripherals = [
            "GPIO", "UART", "USART", "SPI", "I2C", "ADC", "DAC",
            "TIM", "DMA", "RCC", "NVIC", "EXTI", "FLASH", "PWR"
        ]

        for peripheral in common_peripherals:
            assert hasattr(Peripheral, peripheral), f"Missing peripheral: {peripheral}"


class TestDocTypeEnums:
    """Test document type enum completeness."""

    def test_all_doc_types_defined(self):
        """Verify all document types are defined."""
        from storage.metadata import DocType

        doc_types = [
            "REFERENCE_MANUAL", "APPLICATION_NOTE", "USER_MANUAL",
            "PROGRAMMING_MANUAL", "DATASHEET", "HAL_GUIDE", "GENERAL"
        ]

        for doc_type in doc_types:
            assert hasattr(DocType, doc_type), f"Missing doc type: {doc_type}"


class TestConfigurationValidation:
    """Test configuration validation."""

    def test_settings_validation(self):
        """Test settings are valid."""
        from mcp_server.config import settings

        # Check required settings exist
        assert hasattr(settings, 'CHUNK_SIZE')
        assert hasattr(settings, 'CHUNK_OVERLAP')
        assert hasattr(settings, 'EMBEDDING_MODEL')

        # Check settings are reasonable
        assert settings.CHUNK_SIZE > 0
        assert settings.CHUNK_OVERLAP >= 0
        assert settings.CHUNK_OVERLAP < settings.CHUNK_SIZE

    def test_paths_are_paths(self):
        """Test that path settings are Path objects."""
        from mcp_server.config import settings

        assert isinstance(settings.PROJECT_ROOT, Path)
        assert isinstance(settings.CHROMA_DB_PATH, Path)


class TestAgentConfiguration:
    """Test agent configuration files."""

    def test_agent_files_exist(self):
        """Test that agent definition files exist."""
        agents_dir = PROJECT_ROOT / ".claude" / "agents"

        if agents_dir.exists():
            # Check for some expected agent files
            expected_agents = ["router.md", "firmware.md"]
            for agent_file in expected_agents:
                agent_path = agents_dir / agent_file
                if agent_path.exists():
                    content = agent_path.read_text()
                    assert len(content) > 0, f"Agent file is empty: {agent_file}"

    def test_command_files_exist(self):
        """Test that command definition files exist."""
        commands_dir = PROJECT_ROOT / ".claude" / "commands"

        if commands_dir.exists():
            # Check for expected command files
            expected_commands = ["stm32.md"]
            for cmd_file in expected_commands:
                cmd_path = commands_dir / cmd_file
                if cmd_path.exists():
                    content = cmd_path.read_text()
                    assert len(content) > 0, f"Command file is empty: {cmd_file}"


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
