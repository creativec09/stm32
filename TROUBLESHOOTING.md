# Troubleshooting Guide

This guide helps you diagnose and resolve common issues with the STM32 MCP Documentation Server.

## Table of Contents

- [Quick Diagnostics](#quick-diagnostics)
- [Server Issues](#server-issues)
  - [Server Won't Start](#server-wont-start)
  - [MCP Connection Issues](#mcp-connection-issues)
  - [Network Mode Problems](#network-mode-problems)
- [Search Issues](#search-issues)
  - [No Results Found](#no-results-found)
  - [Irrelevant Results](#irrelevant-results)
  - [Slow Searches](#slow-searches)
- [Database Issues](#database-issues)
  - [ChromaDB Errors](#chromadb-errors)
  - [Embedding Model Errors](#embedding-model-errors)
  - [Corrupted Database](#corrupted-database)
- [Installation Issues](#installation-issues)
  - [Import Errors](#import-errors)
  - [Permission Errors](#permission-errors)
  - [Dependency Conflicts](#dependency-conflicts)
- [Performance Issues](#performance-issues)
  - [Slow First Request](#slow-first-request)
  - [High Memory Usage](#high-memory-usage)
- [Logging and Diagnostics](#logging-and-diagnostics)
- [Validation Scripts](#validation-scripts)
- [Reporting Issues](#reporting-issues)

---

## Quick Diagnostics

Run these commands to quickly identify issues:

```bash
# Activate virtual environment
source .venv/bin/activate

# 1. Check Python version
python --version  # Should be 3.11+

# 2. Verify package installation
python -c "import mcp_server; print('MCP server module OK')"

# 3. Check configuration
python -c "from mcp_server.config import settings; print(settings)"

# 4. Verify database
python -c "from storage.chroma_store import STM32ChromaStore; s = STM32ChromaStore('data/chroma_db/'); print(f'Chunks: {s.count()}')"

# 5. Run full validation
python scripts/validate_system.py
```

---

## Server Issues

### Server Won't Start

#### Symptom
Server fails to start or crashes immediately.

#### Diagnosis

```bash
# Check for syntax errors
python -m py_compile mcp_server/server.py

# Try running directly with verbose output
python mcp_server/server.py 2>&1

# Check configuration
python -c "from mcp_server.config import settings; print(settings.model_dump_json(indent=2))"
```

#### Common Causes and Solutions

**1. Missing Dependencies**
```bash
# Reinstall all dependencies
pip install -e . --force-reinstall
```

**2. Invalid Configuration**
```bash
# Check .env file syntax
cat .env | grep -v "^#" | grep -v "^$"

# Try with default configuration
mv .env .env.backup
python scripts/start_server.py
```

**3. Port Already in Use (Network Mode)**
```bash
# Check if port is in use
lsof -i :8765  # Linux/macOS
netstat -ano | findstr :8765  # Windows

# Use a different port
STM32_PORT=8766 python scripts/start_server.py
```

**4. Database Not Initialized**
```bash
# Check if database exists
ls -la data/chroma_db/

# Reinitialize
python scripts/ingest_docs.py --clear
```

### MCP Connection Issues

#### Symptom
Claude Code can't connect to the MCP server or tools don't appear.

#### Diagnosis

```bash
# Verify MCP configuration
# For user scope (recommended): ~/.claude.json
cat ~/.claude.json

# For project scope: .mcp.json in project root
cat .mcp.json

# Test server manually
python mcp_server/server.py
```

#### Solutions

**1. Check Configuration Paths**

For user-scoped MCP servers (`-s user`), configs are in `~/.claude.json`.
For project-scoped servers (`-s project`), configs are in `.mcp.json` at project root.

Ensure all paths in your config are absolute:

```json
{
  "mcpServers": {
    "stm32-docs": {
      "command": "/absolute/path/to/.venv/bin/python",
      "args": ["/absolute/path/to/mcp_server/server.py"],
      "env": {
        "PYTHONPATH": "/absolute/path/to/stm32-agents"
      }
    }
  }
}
```

**2. Verify Python Executable**

```bash
# Check the Python path exists
ls -la /path/to/.venv/bin/python

# Or on Windows
dir C:\path\to\.venv\Scripts\python.exe
```

**3. Check PYTHONPATH**

The `PYTHONPATH` must include the project root:

```bash
# Test import with PYTHONPATH set
PYTHONPATH=/path/to/stm32-agents python -c "from mcp_server.server import mcp"
```

**4. Restart Claude Code**

After changing your MCP configuration, fully restart Claude Code (not just the window).

### Network Mode Problems

#### Symptom
Remote clients can't connect to the server.

#### Diagnosis

```bash
# Check server is listening
netstat -tlnp | grep 8765  # Linux
lsof -i :8765              # macOS

# Test local connection
curl http://localhost:8765/health

# Test from remote (on client)
curl http://SERVER_IP:8765/health
```

#### Solutions

**1. Firewall Blocking**

```bash
# Linux (ufw)
sudo ufw allow 8765

# Linux (firewalld)
sudo firewall-cmd --add-port=8765/tcp --permanent
sudo firewall-cmd --reload
```

**2. Tailscale Not Connected**

```bash
# Check Tailscale status
tailscale status

# Reconnect if needed
tailscale up
```

**3. Wrong IP Address**

Use the Tailscale IP, not the local IP:

```bash
# Get Tailscale IP
tailscale ip -4
```

**4. Server Not Bound to All Interfaces**

Ensure `STM32_HOST=0.0.0.0` in `.env` or environment.

---

## Search Issues

### No Results Found

#### Symptom
Searches return empty results or "No documentation found".

#### Diagnosis

```bash
# Check document count
python -c "
from storage.chroma_store import STM32ChromaStore
store = STM32ChromaStore('data/chroma_db/')
print(f'Total chunks: {store.count()}')
"

# Test a simple search
python -c "
from storage.chroma_store import STM32ChromaStore
store = STM32ChromaStore('data/chroma_db/')
results = store.search('GPIO', n_results=5)
print(f'Found: {len(results)} results')
"
```

#### Solutions

**1. Database Empty**

```bash
# Re-ingest documentation
python scripts/ingest_docs.py --clear
```

**2. Wrong Database Path**

```bash
# Check database path in config
python -c "from mcp_server.config import settings; print(settings.chroma_db_path)"

# Verify it matches where you ingested
ls -la data/chroma_db/
```

**3. Embedding Model Mismatch**

If you changed the embedding model after ingestion:

```bash
# Re-ingest with new model
STM32_EMBEDDING_MODEL=all-MiniLM-L6-v2 python scripts/ingest_docs.py --clear
```

### Irrelevant Results

#### Symptom
Search returns results that don't match the query.

#### Solutions

**1. Be More Specific**

Instead of "timer", try "TIM PWM output configuration".

**2. Use Peripheral Filters**

```python
from storage.chroma_store import STM32ChromaStore
from storage.metadata import Peripheral

store = STM32ChromaStore('data/chroma_db/')
results = store.search(
    "DMA configuration",
    peripheral=Peripheral.UART,  # Filter to UART-related DMA
    n_results=5
)
```

**3. Adjust Minimum Score**

Set `STM32_MIN_RELEVANCE_SCORE` in `.env`:

```bash
# Only return highly relevant results
STM32_MIN_RELEVANCE_SCORE=0.5
```

**4. Check Source Documents**

Ensure your markdown files contain the content you're searching for:

```bash
grep -r "your search term" markdowns/
```

### Slow Searches

#### Symptom
Search queries take more than a few seconds.

#### Solutions

**1. First Query Initialization**

The first query loads the embedding model (~90 seconds). This is normal.

**2. Pre-warm the Server**

```bash
# Load model before first real query
python -c "from storage.chroma_store import STM32ChromaStore; STM32ChromaStore('data/chroma_db/')"
```

**3. Reduce Result Count**

```bash
# In .env
STM32_DEFAULT_SEARCH_RESULTS=5
STM32_MAX_SEARCH_RESULTS=10
```

---

## Database Issues

### ChromaDB Errors

#### Symptom
Errors mentioning ChromaDB, sqlite, or collection not found.

#### Common Errors and Solutions

**"Collection not found"**

```bash
# Reinitialize database
python scripts/ingest_docs.py --clear
```

**"Database is locked"**

Another process is using the database:

```bash
# Find and kill ChromaDB processes
lsof +D data/chroma_db/

# Or force close
rm -f data/chroma_db/*.lock
```

**"Corrupt database"**

```bash
# Backup and rebuild
mv data/chroma_db/ data/chroma_db.backup/
python scripts/ingest_docs.py --clear
```

### Embedding Model Errors

#### Symptom
Errors about sentence-transformers, torch, or model loading.

#### Solutions

**1. Model Download Failed**

```bash
# Clear model cache and retry
rm -rf ~/.cache/huggingface/
rm -rf ~/.cache/torch/

# Reinstall sentence-transformers
pip install --force-reinstall sentence-transformers

# Pre-download model
python -c "from sentence_transformers import SentenceTransformer; SentenceTransformer('all-MiniLM-L6-v2')"
```

**2. CUDA/GPU Errors**

If using GPU and encountering errors:

```bash
# Force CPU mode
STM32_EMBEDDING_DEVICE=cpu python scripts/ingest_docs.py --clear
```

**3. Memory Errors During Loading**

```bash
# Reduce batch size
STM32_EMBEDDING_BATCH_SIZE=16 python scripts/ingest_docs.py --clear
```

### Corrupted Database

#### Symptom
Various database errors that don't resolve with normal fixes.

#### Solution

Complete rebuild:

```bash
# Remove old database
rm -rf data/chroma_db/

# Clear any cached data
rm -rf .pytest_cache/
find . -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null

# Reingest
python scripts/ingest_docs.py --clear

# Verify
python scripts/verify_mcp.py
```

---

## Installation Issues

### Import Errors

#### Symptom
`ModuleNotFoundError` or `ImportError` when running scripts.

#### Solutions

**1. Virtual Environment Not Activated**

```bash
source .venv/bin/activate
# Verify
which python  # Should show .venv path
```

**2. Package Not Installed**

```bash
pip install -e .
```

**3. PYTHONPATH Not Set**

```bash
export PYTHONPATH=/path/to/stm32-agents:$PYTHONPATH
python -c "import mcp_server"
```

**4. Wrong Python Version**

```bash
# Check version
python --version

# If wrong, use explicit path
/usr/bin/python3.11 -m venv .venv
```

### Permission Errors

#### Symptom
"Permission denied" errors during installation or runtime.

#### Solutions

**1. Can't Install Packages**

```bash
# Use user installation
pip install --user -e .

# Or fix venv permissions
chmod -R u+rwX .venv/
```

**2. Can't Write to Data Directory**

```bash
# Fix data directory permissions
chmod -R 755 data/
chmod -R 755 logs/
```

**3. Can't Create Virtual Environment**

```bash
# Ensure you own the directory
sudo chown -R $USER:$USER /path/to/stm32-agents
```

### Dependency Conflicts

#### Symptom
Package version conflicts or incompatibility errors.

#### Solutions

**1. Clean Reinstall**

```bash
# Remove and recreate venv
rm -rf .venv/
python -m venv .venv
source .venv/bin/activate
pip install -e .
```

**2. Specific Version Conflicts**

```bash
# Check what's installed
pip list

# Install specific versions
pip install chromadb==0.4.22
pip install sentence-transformers==2.2.2
```

---

## Performance Issues

### Slow First Request

#### Explanation
The first request after starting takes ~90 seconds because it loads:
1. The sentence-transformers embedding model
2. PyTorch runtime
3. ChromaDB indexes

This is expected behavior.

#### Mitigation

**Pre-warm on Startup**

Add to your startup script:

```bash
# Pre-load model
python -c "
from storage.chroma_store import STM32ChromaStore
store = STM32ChromaStore('data/chroma_db/')
store.search('test', n_results=1)
print('Model loaded and ready')
"
```

**Use Lazy Loading**

Set in `.env`:

```bash
STM32_LAZY_LOAD_EMBEDDINGS=false  # Load on startup instead of first request
```

### High Memory Usage

#### Symptom
Server uses excessive RAM (>4GB).

#### Solutions

**1. Use Smaller Model**

```bash
# all-MiniLM-L6-v2 is smallest (default)
STM32_EMBEDDING_MODEL=all-MiniLM-L6-v2
```

**2. Reduce Batch Size**

```bash
STM32_EMBEDDING_BATCH_SIZE=16
```

**3. Enable Garbage Collection**

Add to your scripts if needed:

```python
import gc
gc.collect()
```

---

## Logging and Diagnostics

### Enable Debug Logging

```bash
# Set in .env or environment
STM32_LOG_LEVEL=DEBUG
```

### View Logs

```bash
# Logs are in logs/ directory
tail -f logs/stm32_mcp.log

# Or check console output
python scripts/start_server.py 2>&1 | tee server.log
```

### Log File Locations

| Log | Location |
|-----|----------|
| Server logs | `logs/stm32_mcp.log` |
| Ingestion logs | Console output |
| Test logs | `.pytest_cache/` |

### Common Log Messages

| Message | Meaning |
|---------|---------|
| "Loading embedding model..." | Model initialization (expected to be slow) |
| "Collection not found, creating..." | First run, database being initialized |
| "Connection refused" | Network mode client can't reach server |
| "Search returned 0 results" | Query didn't match any documents |

---

## Validation Scripts

### Full System Validation

```bash
python scripts/validate_system.py
```

Checks:
- Python version
- Required packages
- Database connectivity
- Document count
- Search functionality
- MCP tool registration

### Quick MCP Verification

```bash
python scripts/verify_mcp.py
```

Checks:
- Server imports
- Configuration loading
- Basic functionality

### Search Quality Test

```bash
python scripts/test_retrieval.py
```

Runs test queries and reports:
- Result count
- Relevance scores
- Response times

### Custom Diagnostic Script

Create a diagnostic script:

```python
#!/usr/bin/env python
"""Diagnostic script for STM32 MCP server."""

import sys
from pathlib import Path

def check_python():
    print(f"Python: {sys.version}")
    return sys.version_info >= (3, 11)

def check_imports():
    try:
        import mcp_server
        import storage
        import pipeline
        print("Core imports: OK")
        return True
    except ImportError as e:
        print(f"Import error: {e}")
        return False

def check_config():
    try:
        from mcp_server.config import settings
        print(f"Config: {settings.server_mode}")
        return True
    except Exception as e:
        print(f"Config error: {e}")
        return False

def check_database():
    try:
        from storage.chroma_store import STM32ChromaStore
        store = STM32ChromaStore("data/chroma_db/")
        count = store.count()
        print(f"Database: {count} chunks")
        return count > 0
    except Exception as e:
        print(f"Database error: {e}")
        return False

def check_search():
    try:
        from storage.chroma_store import STM32ChromaStore
        store = STM32ChromaStore("data/chroma_db/")
        results = store.search("UART", n_results=1)
        print(f"Search: {'OK' if results else 'No results'}")
        return len(results) > 0
    except Exception as e:
        print(f"Search error: {e}")
        return False

if __name__ == "__main__":
    checks = [
        ("Python version", check_python),
        ("Imports", check_imports),
        ("Configuration", check_config),
        ("Database", check_database),
        ("Search", check_search),
    ]

    all_passed = True
    for name, check in checks:
        print(f"\n{name}:")
        if not check():
            all_passed = False

    print(f"\n{'All checks passed!' if all_passed else 'Some checks failed.'}")
    sys.exit(0 if all_passed else 1)
```

---

## Reporting Issues

If you can't resolve an issue, please open a GitHub issue with:

### Required Information

1. **Environment**
   - OS and version
   - Python version (`python --version`)
   - Package versions (`pip list`)

2. **Error Details**
   - Full error message and traceback
   - Steps to reproduce
   - What you've already tried

3. **Configuration**
   - `.env` contents (redact any secrets)
   - MCP configuration (`~/.claude.json` for user scope or `.mcp.json` for project scope)
   - Any custom settings

4. **Logs**
   - Relevant log output
   - Debug logs if possible (`STM32_LOG_LEVEL=DEBUG`)

### Template

```markdown
## Environment
- OS: Ubuntu 22.04
- Python: 3.11.5
- Installation method: pip install -e .

## Description
Brief description of the issue.

## Steps to Reproduce
1. Step one
2. Step two
3. Error occurs

## Expected Behavior
What should happen.

## Actual Behavior
What actually happens.

## Error Output
```
Paste error here
```

## Configuration
```
Relevant config (redacted)
```

## What I've Tried
- Tried solution A
- Tried solution B
```

### Getting Help

- GitHub Issues: For bugs and feature requests
- Documentation: Check [docs/](docs/) for detailed guides
- Validation: Run `python scripts/validate_system.py` before reporting
