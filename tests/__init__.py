"""
Test Suite for STM32 MCP Documentation Server

Comprehensive tests covering all components of the MCP server.

Test Modules:
- test_chunking.py: Document chunking tests
- test_storage.py: ChromaDB storage tests
- test_mcp_tools.py: MCP tool tests
- test_integration.py: End-to-end integration tests
- conftest.py: Shared fixtures

Running Tests:
    # Run all tests
    pytest

    # Run with coverage
    pytest --cov=mcp_server --cov=pipeline --cov=storage

    # Run specific test file
    pytest tests/test_chunking.py

    # Run with verbose output
    pytest -v

    # Run only fast tests (skip integration)
    pytest -m "not integration"

Fixtures (defined in conftest.py):
- temp_dir: Temporary directory for test files
- temp_store: Temporary ChromaDB store
- sample_chunks: Pre-populated test chunks
- chunker: STM32Chunker instance
- sample_markdown: Sample markdown content

Environment:
    Tests use temporary directories and do not modify the main database.
    ChromaDB is initialized in a temp directory for each test session.
"""

__version__ = "1.0.0"

__all__: list[str] = []
