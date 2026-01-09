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
