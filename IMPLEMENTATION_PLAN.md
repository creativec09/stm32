# STM32 MCP Plugin Improvements - Implementation Plan

This document provides a complete implementation plan for three key improvements to the STM32 MCP documentation server:

1. **Database Lazy-Download System** - Download pre-built ChromaDB from GitHub releases on first run
2. **New `/stm32-setup` Slash Command** - Interactive setup command for users
3. **CLAUDE.md Auto-Population** - Auto-update user's project CLAUDE.md with STM32 instructions

---

## Table of Contents

1. [Overview](#overview)
2. [File Structure](#file-structure)
3. [Implementation Order](#implementation-order)
4. [Part 1: Database Manager Module](#part-1-database-manager-module)
5. [Part 2: Update Server Startup Logic](#part-2-update-server-startup-logic)
6. [Part 3: Create /stm32-setup Slash Command](#part-3-create-stm32-setup-slash-command)
7. [Part 4: CLAUDE.md Generator](#part-4-claudemd-generator)
8. [Part 5: Update Configuration](#part-5-update-configuration)
9. [Part 6: GitHub Release Workflow](#part-6-github-release-workflow)
10. [Testing Steps](#testing-steps)

---

## Overview

### Current State
- Database is either:
  1. Pre-built and bundled with the package (large download)
  2. Built on first run via ingestion (slow, 5-10 min)
- No lazy-download mechanism
- Setup requires running CLI commands
- Users must manually learn about available tools/agents

### Target State
- Database is lazily downloaded from GitHub releases on first MCP server run
- `/stm32-setup` command provides guided setup experience
- CLAUDE.md is auto-populated with comprehensive STM32 instructions

---

## File Structure

Files to create:
```
mcp_server/
  database_manager.py       # NEW - Lazy download logic
  claude_md_generator.py    # NEW - CLAUDE.md content generator

commands/
  stm32-setup.md           # NEW - Slash command definition

.github/workflows/
  release-database.yml     # NEW - GitHub Action for packaging DB
```

Files to modify:
```
mcp_server/server.py      # Update lifespan to use DatabaseManager
mcp_server/config.py      # Add new configuration options
pyproject.toml            # Add httpx for downloads (already present)
```

---

## Implementation Order

1. Create `mcp_server/database_manager.py`
2. Update `mcp_server/config.py` with new settings
3. Update `mcp_server/server.py` to use DatabaseManager
4. Create `mcp_server/claude_md_generator.py`
5. Create `commands/stm32-setup.md`
6. Create GitHub workflow for release packaging
7. Test the complete flow

---

## Part 1: Database Manager Module

Create `/mnt/c/Users/creat/Claude/stm32-agents/mcp_server/database_manager.py`:

```python
"""
Database Manager for STM32 MCP Server.

Handles lazy downloading of pre-built ChromaDB from GitHub releases.
Provides progress feedback and fallback to local ingestion.
"""

import hashlib
import json
import logging
import os
import shutil
import tarfile
import tempfile
from dataclasses import dataclass
from pathlib import Path
from typing import Callable, Optional
from urllib.error import HTTPError, URLError
from urllib.request import Request, urlopen

logger = logging.getLogger(__name__)


@dataclass
class DatabaseInfo:
    """Information about the database."""
    exists: bool
    chunk_count: int
    version: str
    source: str  # "downloaded", "ingested", "bundled", "empty"
    path: Path


@dataclass
class DownloadProgress:
    """Progress information for downloads."""
    current_bytes: int
    total_bytes: int
    percentage: float
    message: str


class DatabaseManager:
    """
    Manages the ChromaDB database lifecycle.

    Responsibilities:
    - Check if database exists and is valid
    - Download pre-built database from GitHub releases
    - Fall back to local ingestion if download fails
    - Provide progress callbacks for UI feedback
    """

    # GitHub configuration
    GITHUB_REPO = "creativec09/stm32-agents"
    DB_ASSET_NAME = "chromadb-stm32-docs.tar.gz"
    DB_MANIFEST_NAME = "chromadb-manifest.json"

    def __init__(
        self,
        db_path: Path,
        markdowns_path: Path,
        progress_callback: Optional[Callable[[DownloadProgress], None]] = None
    ):
        """
        Initialize the database manager.

        Args:
            db_path: Path to ChromaDB storage directory
            markdowns_path: Path to markdown documentation files
            progress_callback: Optional callback for progress updates
        """
        self.db_path = Path(db_path)
        self.markdowns_path = Path(markdowns_path)
        self.progress_callback = progress_callback or self._default_progress
        self._manifest_path = self.db_path / "manifest.json"

    def _default_progress(self, progress: DownloadProgress) -> None:
        """Default progress handler - logs to console."""
        if progress.total_bytes > 0:
            logger.info(
                f"{progress.message}: {progress.percentage:.1f}% "
                f"({progress.current_bytes / 1024 / 1024:.1f} MB)"
            )
        else:
            logger.info(progress.message)

    def get_database_info(self) -> DatabaseInfo:
        """
        Get information about the current database state.

        Returns:
            DatabaseInfo with current state
        """
        if not self.db_path.exists():
            return DatabaseInfo(
                exists=False,
                chunk_count=0,
                version="none",
                source="empty",
                path=self.db_path
            )

        # Check for ChromaDB files
        chroma_db_file = self.db_path / "chroma.sqlite3"
        if not chroma_db_file.exists():
            return DatabaseInfo(
                exists=False,
                chunk_count=0,
                version="none",
                source="empty",
                path=self.db_path
            )

        # Read manifest if available
        version = "unknown"
        source = "unknown"
        if self._manifest_path.exists():
            try:
                with open(self._manifest_path) as f:
                    manifest = json.load(f)
                version = manifest.get("version", "unknown")
                source = manifest.get("source", "unknown")
            except Exception:
                pass

        # Get chunk count
        chunk_count = self._get_chunk_count()

        return DatabaseInfo(
            exists=chunk_count > 0,
            chunk_count=chunk_count,
            version=version,
            source=source,
            path=self.db_path
        )

    def _get_chunk_count(self) -> int:
        """Get the number of chunks in the database."""
        try:
            from storage.chroma_store import STM32ChromaStore
            store = STM32ChromaStore(
                persist_dir=self.db_path,
                collection_name="stm32_docs",
                embedding_model="all-MiniLM-L6-v2"
            )
            return store.count()
        except Exception as e:
            logger.warning(f"Could not count chunks: {e}")
            return 0

    def ensure_database(self, force_download: bool = False) -> DatabaseInfo:
        """
        Ensure the database is ready for use.

        This method:
        1. Checks if database already exists with documents
        2. If not, attempts to download from GitHub releases
        3. If download fails, falls back to local ingestion

        Args:
            force_download: Force re-download even if database exists

        Returns:
            DatabaseInfo with final state
        """
        # Check current state
        info = self.get_database_info()

        if info.exists and info.chunk_count > 0 and not force_download:
            logger.info(f"Database ready: {info.chunk_count} chunks (source: {info.source})")
            return info

        # Try to download
        logger.info("Database empty or missing - attempting download from GitHub releases...")

        if self._download_database():
            info = self.get_database_info()
            if info.exists and info.chunk_count > 0:
                logger.info(f"Download successful: {info.chunk_count} chunks")
                return info
            else:
                logger.warning("Download completed but database appears empty")

        # Fall back to local ingestion
        logger.info("Download failed or unavailable - falling back to local ingestion...")

        if self._run_local_ingestion():
            info = self.get_database_info()
            logger.info(f"Ingestion complete: {info.chunk_count} chunks")
            return info

        # Both failed
        logger.error("Both download and ingestion failed")
        return DatabaseInfo(
            exists=False,
            chunk_count=0,
            version="none",
            source="failed",
            path=self.db_path
        )

    def _download_database(self) -> bool:
        """
        Download pre-built database from GitHub releases.

        Returns:
            True if successful, False otherwise
        """
        try:
            # Get latest release
            release = self._get_latest_release()
            if not release:
                logger.warning("No releases found")
                return False

            # Find database asset
            db_asset = None
            manifest_asset = None
            for asset in release.get("assets", []):
                if asset["name"] == self.DB_ASSET_NAME:
                    db_asset = asset
                elif asset["name"] == self.DB_MANIFEST_NAME:
                    manifest_asset = asset

            if not db_asset:
                logger.warning(f"No database asset in release {release.get('tag_name')}")
                return False

            # Download to temp directory
            with tempfile.TemporaryDirectory() as tmpdir:
                tmp_path = Path(tmpdir)
                archive_path = tmp_path / self.DB_ASSET_NAME

                # Download archive
                self._report_progress("Downloading database", 0, db_asset["size"])

                if not self._download_file(
                    db_asset["browser_download_url"],
                    archive_path,
                    db_asset["size"]
                ):
                    return False

                # Download and verify manifest if available
                if manifest_asset:
                    manifest_path = tmp_path / self.DB_MANIFEST_NAME
                    self._download_file(
                        manifest_asset["browser_download_url"],
                        manifest_path,
                        manifest_asset.get("size", 0)
                    )

                    if manifest_path.exists():
                        try:
                            with open(manifest_path) as f:
                                manifest_data = json.load(f)

                            # Verify checksum
                            if "sha256" in manifest_data:
                                self._report_progress("Verifying checksum", 0, 0)
                                if not self._verify_checksum(archive_path, manifest_data["sha256"]):
                                    logger.error("Checksum verification failed")
                                    return False
                        except Exception as e:
                            logger.warning(f"Could not verify manifest: {e}")

                # Extract archive
                self._report_progress("Extracting database", 0, 0)

                # Backup existing database
                backup_path = None
                if self.db_path.exists() and any(self.db_path.iterdir()):
                    backup_path = self.db_path.parent / "chroma_db_backup"
                    if backup_path.exists():
                        shutil.rmtree(backup_path)
                    shutil.move(str(self.db_path), str(backup_path))

                # Extract
                self.db_path.mkdir(parents=True, exist_ok=True)

                try:
                    if not self._extract_archive(archive_path, self.db_path.parent):
                        # Restore backup
                        if backup_path and backup_path.exists():
                            shutil.move(str(backup_path), str(self.db_path))
                        return False

                    # Write manifest
                    manifest_info = {
                        "version": release.get("tag_name", "unknown"),
                        "source": "downloaded",
                        "release_url": release.get("html_url", ""),
                        "downloaded_at": str(Path(archive_path).stat().st_mtime)
                    }
                    with open(self._manifest_path, "w") as f:
                        json.dump(manifest_info, f, indent=2)

                    # Clean up backup
                    if backup_path and backup_path.exists():
                        shutil.rmtree(backup_path)

                    self._report_progress("Download complete", 100, 100)
                    return True

                except Exception as e:
                    logger.error(f"Extraction failed: {e}")
                    # Restore backup
                    if backup_path and backup_path.exists():
                        if self.db_path.exists():
                            shutil.rmtree(self.db_path)
                        shutil.move(str(backup_path), str(self.db_path))
                    return False

        except Exception as e:
            logger.error(f"Download failed: {e}")
            return False

    def _get_latest_release(self) -> Optional[dict]:
        """Fetch latest release from GitHub API."""
        url = f"https://api.github.com/repos/{self.GITHUB_REPO}/releases/latest"
        req = Request(url, headers={"Accept": "application/vnd.github.v3+json"})

        try:
            with urlopen(req, timeout=30) as response:
                return json.loads(response.read().decode())
        except HTTPError as e:
            if e.code == 404:
                # No releases yet, try to get all releases
                url = f"https://api.github.com/repos/{self.GITHUB_REPO}/releases"
                try:
                    with urlopen(Request(url, headers={"Accept": "application/vnd.github.v3+json"}), timeout=30) as response:
                        releases = json.loads(response.read().decode())
                        return releases[0] if releases else None
                except Exception:
                    pass
            logger.warning(f"GitHub API error: {e.code}")
            return None
        except URLError as e:
            logger.warning(f"Network error: {e}")
            return None

    def _download_file(self, url: str, dest: Path, expected_size: int) -> bool:
        """Download a file with progress updates."""
        req = Request(url, headers={"Accept": "application/octet-stream"})

        try:
            with urlopen(req, timeout=300) as response:
                total_size = int(response.headers.get("content-length", expected_size))
                downloaded = 0
                block_size = 8192

                with open(dest, "wb") as f:
                    while True:
                        chunk = response.read(block_size)
                        if not chunk:
                            break
                        f.write(chunk)
                        downloaded += len(chunk)

                        self._report_progress(
                            "Downloading database",
                            downloaded,
                            total_size
                        )

                return True

        except (HTTPError, URLError) as e:
            logger.error(f"Download failed: {e}")
            return False

    def _extract_archive(self, archive_path: Path, dest_dir: Path) -> bool:
        """Extract tar.gz archive with security checks."""
        try:
            with tarfile.open(archive_path, "r:gz") as tar:
                # Security check
                for member in tar.getmembers():
                    if member.name.startswith("/") or ".." in member.name:
                        logger.error(f"Invalid path in archive: {member.name}")
                        return False

                tar.extractall(dest_dir)

            return True

        except Exception as e:
            logger.error(f"Extraction failed: {e}")
            return False

    def _verify_checksum(self, file_path: Path, expected_sha256: str) -> bool:
        """Verify SHA256 checksum."""
        sha256 = hashlib.sha256()
        with open(file_path, "rb") as f:
            for chunk in iter(lambda: f.read(8192), b""):
                sha256.update(chunk)
        return sha256.hexdigest() == expected_sha256

    def _run_local_ingestion(self) -> bool:
        """Run local document ingestion as fallback."""
        # Check if markdown files exist
        if not self.markdowns_path.exists():
            logger.error(f"Markdown directory not found: {self.markdowns_path}")
            return False

        md_files = list(self.markdowns_path.glob("*.md"))
        if not md_files:
            logger.error(f"No markdown files in {self.markdowns_path}")
            return False

        self._report_progress(f"Ingesting {len(md_files)} documentation files", 0, len(md_files))

        try:
            from mcp_server.ingestion import run_ingestion
            from storage.chroma_store import STM32ChromaStore

            # Initialize store
            store = STM32ChromaStore(
                persist_dir=self.db_path,
                collection_name="stm32_docs",
                embedding_model="all-MiniLM-L6-v2"
            )

            # Progress wrapper
            def ingestion_progress(msg: str, current: int, total: int):
                self._report_progress(msg, current, total)

            # Run ingestion
            result = run_ingestion(
                source_dir=self.markdowns_path,
                store=store,
                chunk_size=1000,
                chunk_overlap=150,
                min_chunk_size=50,
                clear_existing=False,
                progress_callback=ingestion_progress
            )

            if result.get("success"):
                # Write manifest
                manifest_info = {
                    "version": "local",
                    "source": "ingested",
                    "total_files": result.get("total_files", 0),
                    "total_chunks": result.get("total_chunks", 0)
                }
                with open(self._manifest_path, "w") as f:
                    json.dump(manifest_info, f, indent=2)

                return True
            else:
                logger.error(f"Ingestion failed: {result.get('error')}")
                return False

        except Exception as e:
            logger.error(f"Ingestion error: {e}")
            return False

    def _report_progress(self, message: str, current: int, total: int) -> None:
        """Report progress to callback."""
        percentage = (current / total * 100) if total > 0 else 0
        progress = DownloadProgress(
            current_bytes=current,
            total_bytes=total,
            percentage=percentage,
            message=message
        )
        self.progress_callback(progress)

    def clear_database(self) -> bool:
        """Clear the database completely."""
        try:
            if self.db_path.exists():
                shutil.rmtree(self.db_path)
            self.db_path.mkdir(parents=True, exist_ok=True)
            logger.info("Database cleared")
            return True
        except Exception as e:
            logger.error(f"Failed to clear database: {e}")
            return False
```

---

## Part 2: Update Server Startup Logic

Modify `/mnt/c/Users/creat/Claude/stm32-agents/mcp_server/server.py`.

Find the `server_lifespan` function and update it to use `DatabaseManager`:

```python
# Add import at top of file
from mcp_server.database_manager import DatabaseManager, DownloadProgress

# Replace the server_lifespan function with:

@asynccontextmanager
async def server_lifespan(server: FastMCP):
    """
    Server lifespan context manager.

    This is called when the server starts up. It:
    1. Initializes the DatabaseManager
    2. Ensures database is ready (download or ingest if needed)
    3. Creates the ServerContext for sharing across requests
    """
    logger.info("=" * 60)
    logger.info(f"STM32 MCP Server v{settings.SERVER_VERSION} starting...")
    logger.info("=" * 60)

    # Ensure required directories exist
    settings.ensure_directories()

    # Progress callback for database operations
    def log_db_progress(progress: DownloadProgress):
        if progress.total_bytes > 0:
            logger.info(
                f"{progress.message}: {progress.percentage:.1f}% "
                f"({progress.current_bytes / 1024 / 1024:.1f} MB / "
                f"{progress.total_bytes / 1024 / 1024:.1f} MB)"
            )
        else:
            logger.info(progress.message)

    # Initialize DatabaseManager
    db_manager = DatabaseManager(
        db_path=settings.CHROMA_DB_PATH,
        markdowns_path=settings.RAW_DOCS_DIR,
        progress_callback=log_db_progress
    )

    # Ensure database is ready
    logger.info("Checking database status...")
    db_info = db_manager.ensure_database()

    # Initialize the ChromaDB store
    logger.info(f"Initializing ChromaDB store at {settings.CHROMA_DB_PATH}")
    store = STM32ChromaStore(
        persist_dir=settings.CHROMA_DB_PATH,
        collection_name=settings.COLLECTION_NAME,
        embedding_model=settings.EMBEDDING_MODEL
    )

    chunk_count = store.count()

    if db_info.exists and chunk_count > 0:
        status = "ready"
        message = f"Ready - {chunk_count:,} chunks indexed (source: {db_info.source})"
        logger.info(message)
    else:
        status = "setup_required"
        message = "Database is empty. Run /stm32-setup or check documentation."
        logger.warning(message)

    # Create resources handler
    resources_handler = DocumentationResources(store)

    # Create the server context
    context = ServerContext(
        store=store,
        resources=resources_handler,
        status=status,
        chunk_count=chunk_count,
        message=message
    )

    logger.info("=" * 60)
    logger.info(f"Server status: {status}")
    logger.info(f"Mode: {settings.SERVER_MODE.value}")
    logger.info("=" * 60)

    # Yield the context
    yield context

    # Cleanup on shutdown
    logger.info("STM32 MCP Server shutting down...")
```

---

## Part 3: Create /stm32-setup Slash Command

Create `/mnt/c/Users/creat/Claude/stm32-agents/commands/stm32-setup.md`:

```markdown
---
name: stm32-setup
description: Set up STM32 MCP documentation server in your project
---

# STM32 MCP Setup Command

Interactive setup for the STM32 documentation server.

## Usage

```
/stm32-setup                 Full setup with CLAUDE.md update
/stm32-setup --status        Show current installation status
/stm32-setup --update-claude Only update project CLAUDE.md
/stm32-setup --force-db      Force re-download of database
```

## What This Command Does

When you run `/stm32-setup`, the assistant will:

### 1. Check Database Status
- Verify if the STM32 documentation database is installed
- Report the number of indexed document chunks
- Show the database source (downloaded, ingested, or bundled)

### 2. Download Database (if needed)
- Automatically downloads pre-built vector database from GitHub releases
- Shows download progress
- Falls back to local ingestion if download fails

### 3. Update Project CLAUDE.md
- Adds comprehensive STM32 instructions to your project's CLAUDE.md
- Lists all 16 available STM32 agents and their purposes
- Documents all MCP tools (mcp__stm32-docs__*) with usage examples
- Provides best practices for STM32 queries

### 4. Show Installation Summary
- Database status and chunk count
- Installed agents list
- Available slash commands
- Quick start examples

## MCP Tools Used

This command relies on the following MCP tools:

| Tool | Purpose |
|------|---------|
| `mcp__stm32-docs__list_peripherals` | Verify database is working |
| Read resource `stm32://status` | Get server status |
| Read resource `stm32://health` | Check server health |

## Example Output

```
STM32 MCP Setup
===============

Database Status:
  - Status: Ready
  - Chunks: 13,815 document chunks
  - Source: Downloaded from GitHub release v0.1.0

Available Agents (16):
  - router: Query routing and classification
  - firmware: Core firmware development
  - debug: Debugging and troubleshooting
  ... (13 more)

Available Commands:
  - /stm32 <query>
  - /stm32-init <peripheral>
  - /stm32-hal <function>
  - /stm32-debug <issue>
  - /stm32-setup

CLAUDE.md Updated:
  Added STM32 instructions to ./CLAUDE.md

Quick Start:
  Try: /stm32 How do I configure UART with DMA?
```

## Instructions for the Assistant

When the user runs `/stm32-setup`, follow these steps:

1. **Check MCP Server Status**
   - Read the `stm32://status` resource to get database state
   - If status is "setup_required", inform the user

2. **Verify Database**
   - Call `mcp__stm32-docs__list_peripherals()` to verify the database works
   - Report the number of peripherals documented

3. **Update CLAUDE.md**
   - Check if a CLAUDE.md exists in the current project directory
   - If it exists, append STM32 instructions (avoiding duplicates)
   - If it doesn't exist, create it with STM32 instructions
   - Use the content from the STM32 CLAUDE.md template

4. **Show Summary**
   - Report all installed components
   - Provide quick start examples
   - Suggest first queries to try

## CLAUDE.md Template Content

When updating the user's project CLAUDE.md, add the following content:

```markdown
## STM32 Development Instructions

This project uses the STM32 MCP documentation server for embedded development assistance.

### IMPORTANT: Always Use MCP Tools for STM32 Questions

When answering ANY question about STM32 development:
1. ALWAYS search the documentation first using MCP tools
2. NEVER rely solely on training knowledge for STM32-specific details
3. Verify register names, function signatures, and configurations

### Available MCP Tools

| Tool | When to Use |
|------|-------------|
| `mcp__stm32-docs__search_stm32_docs` | General documentation search |
| `mcp__stm32-docs__get_peripheral_docs` | Peripheral-specific documentation |
| `mcp__stm32-docs__get_code_examples` | Find working code examples |
| `mcp__stm32-docs__get_register_info` | Register and bit field details |
| `mcp__stm32-docs__lookup_hal_function` | HAL/LL function documentation |
| `mcp__stm32-docs__troubleshoot_error` | Debug issues and errors |
| `mcp__stm32-docs__get_init_sequence` | Peripheral initialization code |
| `mcp__stm32-docs__get_clock_config` | Clock configuration examples |
| `mcp__stm32-docs__compare_peripheral_options` | Compare peripherals/modes |
| `mcp__stm32-docs__get_migration_guide` | Migration between STM32 families |
| `mcp__stm32-docs__get_interrupt_code` | Interrupt handling examples |
| `mcp__stm32-docs__get_dma_code` | DMA configuration examples |
| `mcp__stm32-docs__get_low_power_code` | Low power mode examples |
| `mcp__stm32-docs__get_callback_code` | HAL callback implementations |
| `mcp__stm32-docs__get_init_template` | Complete init templates |
| `mcp__stm32-docs__list_peripherals` | List documented peripherals |

### Available Slash Commands

- `/stm32 <query>` - Search STM32 documentation
- `/stm32-init <peripheral>` - Get initialization code
- `/stm32-hal <function>` - Look up HAL function
- `/stm32-debug <issue>` - Troubleshoot an issue
- `/stm32-setup` - Run setup and show status

### Available STM32 Agents

| Agent | Purpose |
|-------|---------|
| router | Query classification and routing |
| triage | Initial query analysis |
| firmware | General firmware development |
| firmware-core | Core HAL/LL, timers, DMA, interrupts |
| debug | Debugging and troubleshooting |
| bootloader | Bootloader development |
| bootloader-programming | Bootloader protocols |
| peripheral-comm | UART, SPI, I2C, CAN, USB |
| peripheral-analog | ADC, DAC, OPAMP, comparators |
| peripheral-graphics | LTDC, DMA2D, DCMI, TouchGFX |
| power | Power optimization |
| power-management | Sleep, Stop, Standby modes |
| safety | Safety-critical development |
| safety-certification | IEC 61508, ISO 26262 |
| security | Secure boot, TrustZone, crypto |
| hardware-design | PCB design, EMC, thermal |

### Best Practices

1. **Be specific in queries**
   - Good: "How to configure UART2 with DMA RX on STM32F4?"
   - Bad: "UART not working"

2. **Include context**
   - Mention STM32 family when relevant (F4, H7, G4, etc.)
   - Specify HAL vs LL preference
   - Include error messages exactly

3. **Use appropriate tools**
   - For code: `get_code_examples` or `get_init_sequence`
   - For errors: `troubleshoot_error`
   - For functions: `lookup_hal_function`

4. **Verify before using**
   - Always confirm register names match your specific chip
   - Check HAL library version compatibility
```
```

---

## Part 4: CLAUDE.md Generator

Create `/mnt/c/Users/creat/Claude/stm32-agents/mcp_server/claude_md_generator.py`:

```python
"""
CLAUDE.md Generator for STM32 MCP Server.

Generates and manages STM32 instructions for project CLAUDE.md files.
"""

from pathlib import Path
from typing import Optional


# Template content for CLAUDE.md STM32 section
STM32_CLAUDE_MD_TEMPLATE = '''
## STM32 Development Instructions

This project uses the STM32 MCP documentation server for embedded development assistance.

### IMPORTANT: Always Use MCP Tools for STM32 Questions

When answering ANY question about STM32 development:
1. **ALWAYS** search the documentation first using MCP tools
2. **NEVER** rely solely on training knowledge for STM32-specific details
3. **VERIFY** register names, function signatures, and configurations against docs

### Available MCP Tools (mcp__stm32-docs__*)

| Tool | When to Use | Example |
|------|-------------|---------|
| `search_stm32_docs` | General documentation search | `search_stm32_docs("UART DMA configuration")` |
| `get_peripheral_docs` | Peripheral-specific docs | `get_peripheral_docs("GPIO", topic="interrupt")` |
| `get_code_examples` | Find working code examples | `get_code_examples("SPI DMA", peripheral="SPI")` |
| `get_register_info` | Register and bit field details | `get_register_info("GPIO_MODER")` |
| `lookup_hal_function` | HAL/LL function documentation | `lookup_hal_function("HAL_UART_Transmit_DMA")` |
| `troubleshoot_error` | Debug issues and errors | `troubleshoot_error("I2C timeout", peripheral="I2C")` |
| `get_init_sequence` | Peripheral initialization | `get_init_sequence("ADC", use_case="continuous")` |
| `get_clock_config` | Clock tree configuration | `get_clock_config("168MHz", "HSE")` |
| `compare_peripheral_options` | Compare peripherals/modes | `compare_peripheral_options("SPI", "I2C")` |
| `get_migration_guide` | Migration between families | `get_migration_guide("STM32F4", "STM32H7")` |
| `get_interrupt_code` | Interrupt handling examples | `get_interrupt_code("TIM", interrupt_type="update")` |
| `get_dma_code` | DMA configuration examples | `get_dma_code("UART", direction="RX")` |
| `get_low_power_code` | Low power mode config | `get_low_power_code("Stop")` |
| `get_callback_code` | HAL callback implementations | `get_callback_code("SPI", callback_type="TxCplt")` |
| `get_init_template` | Complete init templates | `get_init_template("TIM", mode="PWM")` |
| `list_peripherals` | List documented peripherals | `list_peripherals()` |

### Available Slash Commands

| Command | Purpose | Example |
|---------|---------|---------|
| `/stm32` | Search STM32 documentation | `/stm32 How to configure UART with DMA` |
| `/stm32-init` | Get initialization code | `/stm32-init SPI master DMA mode` |
| `/stm32-hal` | Look up HAL function | `/stm32-hal HAL_GPIO_Init` |
| `/stm32-debug` | Troubleshoot an issue | `/stm32-debug I2C not responding` |
| `/stm32-setup` | Show setup status | `/stm32-setup --status` |

### Available STM32 Specialist Agents (16)

| Agent | Expertise Area | Use When |
|-------|----------------|----------|
| `router` | Query classification | First point of contact for ambiguous queries |
| `triage` | Initial analysis | Quick assessment of query type |
| `firmware` | General firmware | HAL/LL basics, project structure |
| `firmware-core` | Core peripherals | Timers, DMA, interrupts, GPIO |
| `debug` | Troubleshooting | HardFaults, debugging, trace |
| `bootloader` | Bootloader dev | IAP, DFU, system bootloader |
| `bootloader-programming` | Flash programming | Memory programming protocols |
| `peripheral-comm` | Communication | UART, SPI, I2C, CAN, USB, Ethernet |
| `peripheral-analog` | Analog circuits | ADC, DAC, OPAMP, comparators |
| `peripheral-graphics` | Display/Graphics | LTDC, DMA2D, DCMI, TouchGFX |
| `power` | Power optimization | Current measurement, optimization |
| `power-management` | Low power modes | Sleep, Stop, Standby, wakeup |
| `safety` | Safety critical | Self-tests, watchdogs, diagnostics |
| `safety-certification` | Certification | IEC 61508, ISO 26262, Class B |
| `security` | Security | Secure boot, TrustZone, crypto |
| `hardware-design` | Hardware | PCB, EMC, thermal, crystals |

### Query Best Practices

**Good queries (specific, contextual):**
```
/stm32 How to configure UART2 with DMA RX circular buffer on STM32F407?
/stm32-init ADC continuous conversion with DMA on PA0
/stm32-debug SPI returning wrong data order - MSB/LSB issue
```

**Poor queries (vague, missing context):**
```
/stm32 UART not working
/stm32-init timer
/stm32-debug my code doesn't work
```

### Workflow for STM32 Questions

1. **Identify the domain** - Peripheral, debugging, power, etc.
2. **Search documentation first** - Use appropriate MCP tool
3. **Get code examples** - Use `get_code_examples` or `get_init_sequence`
4. **Verify specifics** - Check register names, function signatures
5. **Provide complete answer** - Include all necessary configuration steps

### Important Notes

- Register names may vary between STM32 families (e.g., F4 vs H7)
- HAL library versions affect function availability
- Always verify clock enable for peripherals (RCC)
- Consider pin alternate function mapping for your specific chip
'''

# Marker to identify STM32 section in CLAUDE.md
STM32_SECTION_MARKER = "## STM32 Development Instructions"
STM32_END_MARKER = "<!-- END STM32 SECTION -->"


def get_stm32_claude_content() -> str:
    """
    Get the STM32 content for CLAUDE.md.

    Returns:
        The template content with end marker
    """
    return f"{STM32_CLAUDE_MD_TEMPLATE}\n{STM32_END_MARKER}\n"


def has_stm32_section(claude_md_path: Path) -> bool:
    """
    Check if CLAUDE.md already has STM32 section.

    Args:
        claude_md_path: Path to CLAUDE.md file

    Returns:
        True if STM32 section exists
    """
    if not claude_md_path.exists():
        return False

    content = claude_md_path.read_text(encoding="utf-8")
    return STM32_SECTION_MARKER in content


def update_claude_md(
    project_dir: Path,
    force: bool = False
) -> tuple[bool, str]:
    """
    Update or create CLAUDE.md with STM32 instructions.

    Args:
        project_dir: Project directory containing CLAUDE.md
        force: Force update even if section exists

    Returns:
        Tuple of (success, message)
    """
    claude_md_path = project_dir / "CLAUDE.md"
    stm32_content = get_stm32_claude_content()

    if claude_md_path.exists():
        existing_content = claude_md_path.read_text(encoding="utf-8")

        if has_stm32_section(claude_md_path):
            if not force:
                return True, "STM32 section already exists in CLAUDE.md"

            # Remove existing section and replace
            start_idx = existing_content.find(STM32_SECTION_MARKER)
            end_idx = existing_content.find(STM32_END_MARKER)

            if end_idx != -1:
                end_idx += len(STM32_END_MARKER)
                # Also remove trailing newlines
                while end_idx < len(existing_content) and existing_content[end_idx] == '\n':
                    end_idx += 1

                new_content = (
                    existing_content[:start_idx].rstrip() +
                    "\n\n" +
                    stm32_content +
                    existing_content[end_idx:]
                )
            else:
                # No end marker, just replace from start
                new_content = existing_content[:start_idx].rstrip() + "\n\n" + stm32_content

            claude_md_path.write_text(new_content, encoding="utf-8")
            return True, "Updated STM32 section in CLAUDE.md"
        else:
            # Append STM32 section
            new_content = existing_content.rstrip() + "\n\n" + stm32_content
            claude_md_path.write_text(new_content, encoding="utf-8")
            return True, "Added STM32 section to CLAUDE.md"
    else:
        # Create new CLAUDE.md
        header = f"# {project_dir.name} - Claude Code Project\n\n"
        claude_md_path.write_text(header + stm32_content, encoding="utf-8")
        return True, "Created CLAUDE.md with STM32 instructions"


def get_status_report(
    db_chunk_count: int,
    db_source: str,
    db_version: str
) -> str:
    """
    Generate a status report for /stm32-setup.

    Args:
        db_chunk_count: Number of chunks in database
        db_source: Source of database (downloaded, ingested, etc.)
        db_version: Version string

    Returns:
        Formatted status report
    """
    agents = [
        ("router", "Query classification and routing"),
        ("triage", "Initial query analysis"),
        ("firmware", "General firmware development"),
        ("firmware-core", "Core HAL/LL, timers, DMA, interrupts"),
        ("debug", "Debugging and troubleshooting"),
        ("bootloader", "Bootloader development"),
        ("bootloader-programming", "Bootloader programming protocols"),
        ("peripheral-comm", "UART, SPI, I2C, CAN, USB"),
        ("peripheral-analog", "ADC, DAC, OPAMP, comparators"),
        ("peripheral-graphics", "LTDC, DMA2D, DCMI, TouchGFX"),
        ("power", "Power optimization"),
        ("power-management", "Sleep, Stop, Standby modes"),
        ("safety", "Safety-critical development"),
        ("safety-certification", "IEC 61508, ISO 26262"),
        ("security", "Secure boot, TrustZone, crypto"),
        ("hardware-design", "PCB design, EMC, thermal"),
    ]

    commands = [
        ("/stm32 <query>", "Search STM32 documentation"),
        ("/stm32-init <peripheral>", "Get initialization code"),
        ("/stm32-hal <function>", "Look up HAL function"),
        ("/stm32-debug <issue>", "Troubleshoot an issue"),
        ("/stm32-setup", "Show setup status"),
    ]

    report = []
    report.append("=" * 60)
    report.append("STM32 MCP Server - Setup Status")
    report.append("=" * 60)
    report.append("")

    # Database status
    report.append("Database Status:")
    if db_chunk_count > 0:
        report.append(f"  Status: Ready")
        report.append(f"  Chunks: {db_chunk_count:,} document chunks indexed")
        report.append(f"  Source: {db_source}")
        report.append(f"  Version: {db_version}")
    else:
        report.append("  Status: Empty or not initialized")
        report.append("  Action: Run /stm32-setup to download database")

    report.append("")

    # Agents
    report.append(f"Available Agents ({len(agents)}):")
    for name, desc in agents:
        report.append(f"  - {name}: {desc}")

    report.append("")

    # Commands
    report.append("Available Commands:")
    for cmd, desc in commands:
        report.append(f"  - {cmd}: {desc}")

    report.append("")
    report.append("=" * 60)

    if db_chunk_count > 0:
        report.append("")
        report.append("Quick Start:")
        report.append("  Try: /stm32 How do I configure UART with DMA?")
        report.append("  Or:  /stm32-init SPI master mode")

    return "\n".join(report)
```

---

## Part 5: Update Configuration

Modify `/mnt/c/Users/creat/Claude/stm32-agents/mcp_server/config.py`.

Add these new configuration options after the existing settings:

```python
# Add after line ~170 (after CORS_ORIGINS)

    # =========================================================================
    # Database Download Configuration
    # =========================================================================

    GITHUB_REPO: str = Field(
        default="creativec09/stm32-agents",
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
```

---

## Part 6: GitHub Release Workflow

Create `/mnt/c/Users/creat/Claude/stm32-agents/.github/workflows/release-database.yml`:

```yaml
name: Package and Release Database

on:
  release:
    types: [published]
  workflow_dispatch:
    inputs:
      version:
        description: 'Version tag for the release'
        required: true
        default: 'v0.1.0'

jobs:
  package-database:
    runs-on: ubuntu-latest

    steps:
      - name: Checkout repository
        uses: actions/checkout@v4
        with:
          lfs: true

      - name: Set up Python
        uses: actions/setup-python@v5
        with:
          python-version: '3.11'

      - name: Install dependencies
        run: |
          python -m pip install --upgrade pip
          pip install -e .

      - name: Check for existing database
        id: check-db
        run: |
          if [ -d "data/chroma_db" ] && [ -f "data/chroma_db/chroma.sqlite3" ]; then
            echo "exists=true" >> $GITHUB_OUTPUT
          else
            echo "exists=false" >> $GITHUB_OUTPUT
          fi

      - name: Run ingestion (if no existing database)
        if: steps.check-db.outputs.exists == 'false'
        run: |
          python scripts/ingest_docs.py --verbose

      - name: Get database statistics
        id: db-stats
        run: |
          python -c "
          from storage.chroma_store import STM32ChromaStore
          from mcp_server.config import settings
          store = STM32ChromaStore(
              persist_dir=settings.CHROMA_DB_PATH,
              collection_name=settings.COLLECTION_NAME,
              embedding_model=settings.EMBEDDING_MODEL
          )
          count = store.count()
          print(f'chunk_count={count}')
          " >> $GITHUB_OUTPUT

      - name: Package database
        run: |
          cd data
          tar -czvf chromadb-stm32-docs.tar.gz chroma_db/

          # Calculate SHA256
          sha256sum chromadb-stm32-docs.tar.gz > chromadb-stm32-docs.tar.gz.sha256

          # Get size
          SIZE=$(stat -f%z chromadb-stm32-docs.tar.gz 2>/dev/null || stat -c%s chromadb-stm32-docs.tar.gz)

          # Create manifest
          cat > chromadb-manifest.json << EOF
          {
            "version": "${{ github.event.release.tag_name || github.event.inputs.version }}",
            "chunks": ${{ steps.db-stats.outputs.chunk_count }},
            "sha256": "$(cat chromadb-stm32-docs.tar.gz.sha256 | cut -d' ' -f1)",
            "size": ${SIZE},
            "created": "$(date -u +%Y-%m-%dT%H:%M:%SZ)",
            "embedding_model": "all-MiniLM-L6-v2"
          }
          EOF

          cat chromadb-manifest.json

      - name: Upload to Release
        if: github.event_name == 'release'
        uses: softprops/action-gh-release@v1
        with:
          files: |
            data/chromadb-stm32-docs.tar.gz
            data/chromadb-manifest.json
        env:
          GITHUB_TOKEN: ${{ secrets.GITHUB_TOKEN }}

      - name: Upload artifacts (for workflow_dispatch)
        if: github.event_name == 'workflow_dispatch'
        uses: actions/upload-artifact@v4
        with:
          name: database-package
          path: |
            data/chromadb-stm32-docs.tar.gz
            data/chromadb-manifest.json
          retention-days: 7
```

---

## Testing Steps

### 1. Unit Tests for Database Manager

Create test file `/mnt/c/Users/creat/Claude/stm32-agents/tests/test_database_manager.py`:

```python
"""Tests for DatabaseManager."""

import json
import tempfile
from pathlib import Path
from unittest.mock import MagicMock, patch

import pytest

from mcp_server.database_manager import DatabaseManager, DatabaseInfo, DownloadProgress


class TestDatabaseManager:
    """Test DatabaseManager functionality."""

    @pytest.fixture
    def temp_dirs(self):
        """Create temporary directories for testing."""
        with tempfile.TemporaryDirectory() as tmpdir:
            db_path = Path(tmpdir) / "chroma_db"
            md_path = Path(tmpdir) / "markdowns"
            db_path.mkdir()
            md_path.mkdir()

            # Create a test markdown file
            (md_path / "test.md").write_text("# Test\nTest content")

            yield db_path, md_path

    def test_get_database_info_empty(self, temp_dirs):
        """Test getting info for empty database."""
        db_path, md_path = temp_dirs

        manager = DatabaseManager(db_path, md_path)
        info = manager.get_database_info()

        assert info.exists is False
        assert info.chunk_count == 0
        assert info.source == "empty"

    def test_progress_callback(self, temp_dirs):
        """Test progress callback is called."""
        db_path, md_path = temp_dirs

        progress_calls = []

        def track_progress(progress: DownloadProgress):
            progress_calls.append(progress)

        manager = DatabaseManager(db_path, md_path, progress_callback=track_progress)
        manager._report_progress("Test message", 50, 100)

        assert len(progress_calls) == 1
        assert progress_calls[0].percentage == 50.0
        assert progress_calls[0].message == "Test message"

    @patch.object(DatabaseManager, '_get_latest_release')
    def test_download_no_releases(self, mock_release, temp_dirs):
        """Test download behavior when no releases exist."""
        db_path, md_path = temp_dirs
        mock_release.return_value = None

        manager = DatabaseManager(db_path, md_path)
        result = manager._download_database()

        assert result is False

    @patch.object(DatabaseManager, '_get_latest_release')
    def test_download_no_asset(self, mock_release, temp_dirs):
        """Test download behavior when release has no database asset."""
        db_path, md_path = temp_dirs
        mock_release.return_value = {
            "tag_name": "v0.1.0",
            "assets": []  # No assets
        }

        manager = DatabaseManager(db_path, md_path)
        result = manager._download_database()

        assert result is False
```

### 2. Integration Test

```python
"""Integration test for full setup flow."""

import tempfile
from pathlib import Path

from mcp_server.claude_md_generator import update_claude_md, has_stm32_section


class TestClaudeMdGenerator:
    """Test CLAUDE.md generation."""

    def test_create_new_claude_md(self):
        """Test creating new CLAUDE.md."""
        with tempfile.TemporaryDirectory() as tmpdir:
            project_dir = Path(tmpdir)

            success, message = update_claude_md(project_dir)

            assert success
            assert "Created" in message
            assert (project_dir / "CLAUDE.md").exists()
            assert has_stm32_section(project_dir / "CLAUDE.md")

    def test_append_to_existing(self):
        """Test appending to existing CLAUDE.md."""
        with tempfile.TemporaryDirectory() as tmpdir:
            project_dir = Path(tmpdir)
            claude_md = project_dir / "CLAUDE.md"
            claude_md.write_text("# My Project\n\nExisting content.\n")

            success, message = update_claude_md(project_dir)

            assert success
            assert "Added" in message
            content = claude_md.read_text()
            assert "Existing content" in content
            assert "## STM32 Development Instructions" in content

    def test_skip_if_exists(self):
        """Test skipping if STM32 section already exists."""
        with tempfile.TemporaryDirectory() as tmpdir:
            project_dir = Path(tmpdir)
            claude_md = project_dir / "CLAUDE.md"
            claude_md.write_text("# Project\n## STM32 Development Instructions\nContent\n")

            success, message = update_claude_md(project_dir)

            assert success
            assert "already exists" in message
```

### 3. Manual Testing Steps

1. **Test Database Download**
   ```bash
   # Clear existing database
   rm -rf data/chroma_db

   # Start MCP server and observe download
   python -m mcp_server
   ```

2. **Test Slash Command**
   In Claude Code:
   ```
   /stm32-setup
   /stm32-setup --status
   ```

3. **Test CLAUDE.md Update**
   ```bash
   # In a test project directory
   cd /tmp/test-project
   # Run setup via Claude Code
   # Verify CLAUDE.md is created/updated
   ```

4. **Test Fallback to Ingestion**
   ```bash
   # Block GitHub access temporarily
   # Or rename the release asset
   # Verify ingestion runs as fallback
   ```

---

## Summary

This implementation plan provides:

1. **DatabaseManager** (`mcp_server/database_manager.py`)
   - Lazy downloads pre-built ChromaDB from GitHub releases
   - Progress callbacks for UI feedback
   - Automatic fallback to local ingestion
   - Checksum verification for security

2. **Updated Server Startup** (`mcp_server/server.py`)
   - Uses DatabaseManager in lifespan
   - Provides progress logging during download
   - Graceful handling of all states

3. **New /stm32-setup Command** (`commands/stm32-setup.md`)
   - Interactive setup experience
   - Status checking
   - CLAUDE.md update trigger

4. **CLAUDE.md Generator** (`mcp_server/claude_md_generator.py`)
   - Comprehensive STM32 instructions template
   - Smart append/update logic
   - Lists all 16 agents and their purposes
   - Documents all MCP tools with examples
   - Best practices and query examples

5. **GitHub Workflow** (`.github/workflows/release-database.yml`)
   - Packages ChromaDB for releases
   - Creates manifest with checksum
   - Automated on release publish

### Key Design Decisions

- **Lazy Download**: Database only downloads when needed (not on package install)
- **Progress Feedback**: All long operations report progress
- **Fallback Strategy**: Download -> Ingestion -> Error with clear message
- **Non-Destructive**: Existing CLAUDE.md content preserved
- **Marker-Based**: STM32 section can be updated without touching other content

### Files Modified

| File | Change Type |
|------|-------------|
| `mcp_server/database_manager.py` | NEW |
| `mcp_server/claude_md_generator.py` | NEW |
| `commands/stm32-setup.md` | NEW |
| `.github/workflows/release-database.yml` | NEW |
| `mcp_server/server.py` | MODIFY |
| `mcp_server/config.py` | MODIFY |
| `tests/test_database_manager.py` | NEW |
