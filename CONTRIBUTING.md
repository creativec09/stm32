# Contributing to STM32 MCP Documentation Server

Thank you for your interest in contributing to the STM32 MCP Documentation Server! This document provides guidelines and instructions for contributing to the project.

## Table of Contents

- [Code of Conduct](#code-of-conduct)
- [Getting Started](#getting-started)
- [How to Contribute](#how-to-contribute)
- [Development Setup](#development-setup)
- [Coding Standards](#coding-standards)
- [Testing](#testing)
- [Submitting Changes](#submitting-changes)
- [Documentation](#documentation)
- [Reporting Issues](#reporting-issues)

---

## Code of Conduct

By participating in this project, you agree to abide by our code of conduct:

- Be respectful and inclusive
- Focus on constructive feedback
- Help others learn and grow
- Accept responsibility for mistakes and learn from them

---

## Getting Started

### Understanding the Project

Before contributing, familiarize yourself with:

1. **[README.md](README.md)** - Project overview and quick start
2. **[ARCHITECTURE.md](ARCHITECTURE.md)** - System architecture
3. **[docs/](docs/)** - Detailed documentation
4. **[INSTALL.md](INSTALL.md)** - Installation guide

### Key Components

| Component | Purpose | Location |
|-----------|---------|----------|
| MCP Server | Model Context Protocol server | `mcp_server/` |
| Pipeline | Document processing and chunking | `pipeline/` |
| Storage | ChromaDB vector storage | `storage/` |
| Scripts | CLI utilities | `scripts/` |
| Agents | Specialized AI agents | `.claude/agents/` |

---

## How to Contribute

### Types of Contributions

We welcome:

- **Bug Fixes**: Fix issues and improve stability
- **Features**: Add new functionality
- **Documentation**: Improve docs, add examples
- **Tests**: Add test coverage
- **Performance**: Optimize code and queries
- **Agents**: Create or improve specialized agents

### Good First Issues

Look for issues labeled `good first issue` for beginner-friendly tasks:

- Documentation improvements
- Adding test cases
- Small bug fixes
- Code cleanup

---

## Development Setup

### Prerequisites

- Python 3.11 or higher
- Git
- ~2GB disk space

### Setup Steps

```bash
# 1. Fork the repository on GitHub

# 2. Clone your fork
git clone https://github.com/creativec09/stm32-agents.git
cd stm32-agents

# 3. Add upstream remote
git remote add upstream https://github.com/ORIGINAL_OWNER/stm32-agents.git

# 4. Create virtual environment
python -m venv .venv
source .venv/bin/activate  # Linux/macOS
# .venv\Scripts\activate   # Windows

# 5. Install with development dependencies
pip install -e ".[dev]"

# 6. Install pre-commit hooks
pre-commit install

# 7. Ingest documentation
python scripts/ingest_docs.py --clear

# 8. Verify setup
python scripts/validate_system.py
```

### Keeping Your Fork Updated

```bash
# Fetch upstream changes
git fetch upstream

# Merge into your main branch
git checkout main
git merge upstream/main

# Push to your fork
git push origin main
```

---

## Coding Standards

### Python Style

We follow PEP 8 with these tools:

- **Black**: Code formatting
- **isort**: Import sorting
- **Ruff**: Linting
- **mypy**: Type checking

### Before Committing

```bash
# Format code
black .
isort .

# Check linting
ruff check .

# Type checking
mypy mcp_server pipeline storage

# Run all checks (via pre-commit)
pre-commit run --all-files
```

### Code Guidelines

1. **Type Hints**: Use type hints for all functions

   ```python
   def search(query: str, n_results: int = 5) -> list[dict[str, Any]]:
       ...
   ```

2. **Docstrings**: Use Google-style docstrings

   ```python
   def search(query: str, n_results: int = 5) -> list[dict[str, Any]]:
       """Search documentation for relevant chunks.

       Args:
           query: The search query string.
           n_results: Maximum number of results to return.

       Returns:
           List of matching documents with scores and metadata.

       Raises:
           ValueError: If query is empty.
       """
   ```

3. **Error Handling**: Use specific exceptions

   ```python
   if not query:
       raise ValueError("Query cannot be empty")
   ```

4. **Logging**: Use structured logging

   ```python
   import logging

   logger = logging.getLogger(__name__)
   logger.info("Search completed", extra={"query": query, "results": len(results)})
   ```

### File Organization

```
module/
├── __init__.py      # Public API exports
├── core.py          # Main functionality
├── utils.py         # Utility functions
├── exceptions.py    # Custom exceptions
└── types.py         # Type definitions
```

---

## Testing

### Running Tests

```bash
# Run all tests
pytest tests/

# Run with coverage
pytest tests/ --cov=mcp_server --cov=pipeline --cov=storage

# Run specific test file
pytest tests/test_chunker.py -v

# Run specific test
pytest tests/test_chunker.py::test_chunk_markdown -v

# Run marked tests
pytest tests/ -m "not slow"  # Skip slow tests
```

### Writing Tests

1. **Location**: Place tests in `tests/` directory
2. **Naming**: Use `test_<module>.py` format
3. **Structure**: Use pytest fixtures and classes

```python
import pytest
from pipeline.chunker import chunk_markdown

class TestChunker:
    """Tests for the chunker module."""

    @pytest.fixture
    def sample_markdown(self):
        return """# Header

        Some content here.
        """

    def test_chunk_markdown_basic(self, sample_markdown):
        """Test basic markdown chunking."""
        chunks = chunk_markdown(sample_markdown)
        assert len(chunks) > 0
        assert all(isinstance(c, str) for c in chunks)

    def test_chunk_markdown_empty(self):
        """Test chunking empty content."""
        with pytest.raises(ValueError):
            chunk_markdown("")
```

### Test Categories

Use markers for test categorization:

```python
@pytest.mark.slow
def test_full_ingestion():
    """This test takes a long time."""
    ...

@pytest.mark.integration
def test_mcp_connection():
    """This test requires MCP server running."""
    ...

@pytest.mark.network
def test_tailscale_connection():
    """This test requires network access."""
    ...
```

### Coverage Requirements

- Maintain minimum 70% code coverage
- New features should include tests
- Bug fixes should include regression tests

---

## Submitting Changes

### Branch Naming

Use descriptive branch names:

- `feature/add-uart-examples`
- `fix/search-returns-empty`
- `docs/update-installation`
- `refactor/cleanup-chunker`

### Commit Messages

Follow conventional commits:

```
type(scope): description

[optional body]

[optional footer]
```

Types:
- `feat`: New feature
- `fix`: Bug fix
- `docs`: Documentation
- `test`: Tests
- `refactor`: Code refactoring
- `perf`: Performance improvement
- `chore`: Maintenance

Examples:

```
feat(search): add peripheral filter to search tool

Adds ability to filter search results by STM32 peripheral type.
Supports GPIO, UART, SPI, I2C, TIM, and ADC filters.

Closes #42
```

```
fix(chunker): preserve code blocks during chunking

Code blocks were being split incorrectly when they exceeded
the chunk size limit. This fix ensures code blocks are kept
intact up to the maximum chunk size.

Fixes #38
```

### Pull Request Process

1. **Create Branch**
   ```bash
   git checkout -b feature/your-feature
   ```

2. **Make Changes**
   - Write code
   - Add tests
   - Update documentation

3. **Run Checks**
   ```bash
   pre-commit run --all-files
   pytest tests/
   ```

4. **Commit Changes**
   ```bash
   git add .
   git commit -m "feat(scope): description"
   ```

5. **Push Branch**
   ```bash
   git push origin feature/your-feature
   ```

6. **Open Pull Request**
   - Use the PR template
   - Link related issues
   - Request review

### Pull Request Template

```markdown
## Description
Brief description of the changes.

## Type of Change
- [ ] Bug fix
- [ ] New feature
- [ ] Documentation update
- [ ] Refactoring
- [ ] Performance improvement

## Related Issues
Fixes #123
Related to #456

## Testing
- [ ] Tests pass locally
- [ ] New tests added for changes
- [ ] Coverage maintained/improved

## Checklist
- [ ] Code follows style guidelines
- [ ] Documentation updated
- [ ] No breaking changes (or documented if necessary)
```

---

## Documentation

### Documentation Standards

- Use clear, concise language
- Include code examples
- Keep documentation up-to-date with code

### Types of Documentation

1. **Code Docstrings**: In-code documentation
2. **README Files**: Module-level documentation
3. **Docs Directory**: Detailed guides and references
4. **Inline Comments**: Complex logic explanation

### Adding Documentation

```bash
# Documentation is in docs/ directory
docs/
├── GETTING_STARTED.md
├── ARCHITECTURE.md
├── MCP_SERVER.md
└── ...

# Update INDEX.md when adding new files
```

---

## Reporting Issues

### Before Reporting

1. Check existing issues
2. Verify with latest version
3. Run validation scripts:
   ```bash
   python scripts/validate_system.py
   ```

### Issue Template

```markdown
## Description
Clear description of the issue.

## Steps to Reproduce
1. Step one
2. Step two
3. Error occurs

## Expected Behavior
What should happen.

## Actual Behavior
What actually happens.

## Environment
- OS:
- Python version:
- Package version:

## Logs/Error Output
```
Paste error here
```

## Additional Context
Any other relevant information.
```

### Issue Labels

- `bug`: Something isn't working
- `enhancement`: New feature request
- `documentation`: Documentation improvements
- `good first issue`: Good for newcomers
- `help wanted`: Extra attention needed
- `question`: Further information requested

---

## Recognition

Contributors are recognized in:

- GitHub contributors page
- Release notes
- CONTRIBUTORS.md (for significant contributions)

Thank you for contributing to the STM32 MCP Documentation Server!

---

## Questions?

- Open a GitHub issue with the `question` label
- Check existing documentation in [docs/](docs/)
- Review closed issues for similar questions
