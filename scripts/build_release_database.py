#!/usr/bin/env python3
"""
Build script for creating ChromaDB release artifacts.

This script:
1. Runs the full ingestion pipeline to build ChromaDB from markdown files
2. Validates the resulting database has expected chunk count
3. Packages the database into a tar.gz archive
4. Generates the manifest JSON with checksums

Usage:
    python scripts/build_release_database.py [OPTIONS]

Examples:
    # Build with validation (recommended for releases)
    python scripts/build_release_database.py --version v1.2.0 --validate

    # Build to custom output directory
    python scripts/build_release_database.py --output-dir ./my-artifacts

    # Quick build without validation (for testing)
    python scripts/build_release_database.py --no-validate

    # Force rebuild, clearing existing database
    python scripts/build_release_database.py --clean --version v1.2.0
"""

import argparse
import hashlib
import json
import logging
import os
import shutil
import sys
import tarfile
import tempfile
from datetime import datetime, timezone
from pathlib import Path

# Add project root to path for imports
PROJECT_ROOT = Path(__file__).parent.parent.resolve()
sys.path.insert(0, str(PROJECT_ROOT))

from rich.console import Console
from rich.panel import Panel
from rich.progress import (
    BarColumn,
    Progress,
    SpinnerColumn,
    TaskProgressColumn,
    TextColumn,
    TimeElapsedColumn,
)
from rich.table import Table

# Import project modules
from mcp_server.config import settings
from mcp_server.ingestion import run_ingestion
from storage.chroma_store import STM32ChromaStore

console = Console()
logger = logging.getLogger(__name__)

# Constants
DEFAULT_OUTPUT_DIR = PROJECT_ROOT / "release-artifacts"
ARCHIVE_NAME = "chromadb-stm32-docs.tar.gz"
MANIFEST_NAME = "chromadb-manifest.json"
BUILD_INFO_NAME = "build-info.json"
EMBEDDING_MODEL = "all-MiniLM-L6-v2"

# Validation thresholds
MIN_EXPECTED_CHUNKS = 12000
MAX_EXPECTED_CHUNKS = 16000
MIN_EXPECTED_FILES = 50


class DatabaseBuilder:
    """Handles building and packaging the ChromaDB database for release."""

    def __init__(
        self,
        output_dir: Path,
        version: str,
        source_dir: Path | None = None,
        validate: bool = True,
        clean: bool = False,
        verbose: bool = False,
    ):
        """
        Initialize the database builder.

        Args:
            output_dir: Directory for output artifacts
            version: Version string for the release
            source_dir: Directory containing markdown files (default: from settings)
            validate: Whether to validate chunk count
            clean: Whether to clean existing database before building
            verbose: Enable verbose logging
        """
        self.output_dir = Path(output_dir)
        self.version = version
        self.source_dir = Path(source_dir) if source_dir else settings.RAW_DOCS_DIR
        self.validate = validate
        self.clean = clean
        self.verbose = verbose

        # Build directory (temporary for clean builds, or use existing)
        self.build_dir = tempfile.mkdtemp(prefix="stm32-db-build-") if clean else None
        self.db_path = Path(self.build_dir) / "chroma_db" if self.build_dir else settings.CHROMA_DB_PATH

        # Statistics
        self.stats = {
            "version": version,
            "chunks": 0,
            "source_files": 0,
            "embedding_model": EMBEDDING_MODEL,
            "build_timestamp": "",
            "sha256": "",
        }

    def run(self) -> bool:
        """
        Run the complete build process.

        Returns:
            True if build succeeded, False otherwise
        """
        console.print(Panel.fit(
            f"[bold blue]STM32 ChromaDB Release Build[/bold blue]\n"
            f"Version: {self.version}",
            subtitle=f"Source: {self.source_dir}"
        ))

        try:
            # Step 1: Verify source files
            if not self._verify_source_files():
                return False

            # Step 2: Build database
            if not self._build_database():
                return False

            # Step 3: Validate (if enabled)
            if self.validate and not self._validate_database():
                return False

            # Step 4: Create output directory
            self.output_dir.mkdir(parents=True, exist_ok=True)

            # Step 5: Create archive
            if not self._create_archive():
                return False

            # Step 6: Generate manifest
            if not self._generate_manifest():
                return False

            # Step 7: Generate build info
            self._generate_build_info()

            # Step 8: Print summary
            self._print_summary()

            return True

        except Exception as e:
            console.print(f"[red]Build failed with error: {e}[/red]")
            logger.exception("Build failed")
            return False

        finally:
            # Cleanup temporary build directory
            if self.build_dir and os.path.exists(self.build_dir):
                shutil.rmtree(self.build_dir)

    def _verify_source_files(self) -> bool:
        """Verify source markdown files exist."""
        console.print("\n[bold]Step 1: Verifying source files...[/bold]")

        if not self.source_dir.exists():
            console.print(f"[red]Source directory not found: {self.source_dir}[/red]")
            return False

        md_files = list(self.source_dir.glob("*.md"))
        self.stats["source_files"] = len(md_files)

        console.print(f"Found [green]{len(md_files)}[/green] markdown files")

        if len(md_files) < MIN_EXPECTED_FILES:
            console.print(
                f"[red]Expected at least {MIN_EXPECTED_FILES} files, "
                f"found {len(md_files)}[/red]"
            )
            return False

        if self.verbose:
            for md_file in md_files[:5]:
                console.print(f"  [dim]{md_file.name}[/dim]")
            if len(md_files) > 5:
                console.print(f"  [dim]... and {len(md_files) - 5} more[/dim]")

        return True

    def _build_database(self) -> bool:
        """Build the ChromaDB database from markdown files."""
        console.print("\n[bold]Step 2: Building ChromaDB database...[/bold]")

        # Ensure database directory exists
        self.db_path.mkdir(parents=True, exist_ok=True)

        # Initialize store
        store = STM32ChromaStore(
            persist_dir=self.db_path,
            collection_name=settings.COLLECTION_NAME,
            embedding_model=EMBEDDING_MODEL,
        )

        # Clear if clean build
        if self.clean:
            console.print("[yellow]Clearing existing data for clean build...[/yellow]")
            store.clear()

        # Progress tracking
        md_files = list(self.source_dir.glob("*.md"))

        with Progress(
            SpinnerColumn(),
            TextColumn("[progress.description]{task.description}"),
            BarColumn(),
            TaskProgressColumn(),
            TimeElapsedColumn(),
            console=console,
        ) as progress:
            task = progress.add_task("Processing files...", total=len(md_files))

            def progress_callback(msg: str, current: int, total: int) -> None:
                progress.update(task, completed=current, description=msg[:50])

            # Run ingestion
            result = run_ingestion(
                source_dir=self.source_dir,
                store=store,
                chunk_size=settings.CHUNK_SIZE,
                chunk_overlap=settings.CHUNK_OVERLAP,
                min_chunk_size=settings.MIN_CHUNK_SIZE,
                clear_existing=False,  # Already cleared if clean
                progress_callback=progress_callback,
            )

        if not result.get("success"):
            console.print(f"[red]Ingestion failed: {result.get('error')}[/red]")
            return False

        self.stats["chunks"] = result.get("total_chunks", 0)
        console.print(
            f"[green]Built database with {self.stats['chunks']} chunks "
            f"from {result.get('total_files', 0)} files[/green]"
        )

        # Store reference to the store for later
        self._store = store

        return True

    def _validate_database(self) -> bool:
        """Validate the database meets expectations."""
        console.print("\n[bold]Step 3: Validating database...[/bold]")

        chunk_count = self.stats["chunks"]

        # Check minimum
        if chunk_count < MIN_EXPECTED_CHUNKS:
            console.print(
                f"[red]Chunk count ({chunk_count}) is below minimum "
                f"expected ({MIN_EXPECTED_CHUNKS})[/red]"
            )
            console.print("[red]This may indicate a problem with the ingestion process.[/red]")
            return False

        # Check maximum (warning only)
        if chunk_count > MAX_EXPECTED_CHUNKS:
            console.print(
                f"[yellow]Warning: Chunk count ({chunk_count}) is above maximum "
                f"expected ({MAX_EXPECTED_CHUNKS})[/yellow]"
            )
            console.print("[yellow]This may be fine if new documentation was added.[/yellow]")

        # Verify we can query the database
        try:
            results = self._store.search("GPIO configuration", n_results=3)
            if not results:
                console.print("[red]Database query returned no results[/red]")
                return False
            console.print(f"[green]Database query test passed ({len(results)} results)[/green]")
        except Exception as e:
            console.print(f"[red]Database query failed: {e}[/red]")
            return False

        console.print(f"[green]Validation passed: {chunk_count} chunks[/green]")
        return True

    def _create_archive(self) -> bool:
        """Create the tar.gz archive of the database."""
        console.print("\n[bold]Step 4: Creating archive...[/bold]")

        archive_path = self.output_dir / ARCHIVE_NAME

        try:
            with tarfile.open(archive_path, "w:gz") as tar:
                # Add the chroma_db directory
                tar.add(
                    self.db_path,
                    arcname="chroma_db",
                    filter=self._tar_filter,
                )

            # Calculate SHA256
            self.stats["sha256"] = self._calculate_sha256(archive_path)

            archive_size = archive_path.stat().st_size
            console.print(
                f"[green]Created archive: {archive_path.name} "
                f"({archive_size / 1024 / 1024:.1f} MB)[/green]"
            )

            return True

        except Exception as e:
            console.print(f"[red]Failed to create archive: {e}[/red]")
            return False

    def _tar_filter(self, tarinfo: tarfile.TarInfo) -> tarfile.TarInfo | None:
        """Filter for tar archive to exclude unwanted files."""
        # Exclude common unwanted patterns
        exclude_patterns = [
            "__pycache__",
            ".pyc",
            ".pyo",
            ".DS_Store",
            ".git",
            "*.log",
        ]

        name = tarinfo.name
        for pattern in exclude_patterns:
            if pattern.startswith("*"):
                if name.endswith(pattern[1:]):
                    return None
            elif pattern in name:
                return None

        return tarinfo

    def _calculate_sha256(self, file_path: Path) -> str:
        """Calculate SHA256 checksum of a file."""
        sha256 = hashlib.sha256()
        with open(file_path, "rb") as f:
            for chunk in iter(lambda: f.read(8192), b""):
                sha256.update(chunk)
        return sha256.hexdigest()

    def _generate_manifest(self) -> bool:
        """Generate the manifest JSON file."""
        console.print("\n[bold]Step 5: Generating manifest...[/bold]")

        manifest_path = self.output_dir / MANIFEST_NAME

        self.stats["build_timestamp"] = datetime.now(timezone.utc).isoformat()

        manifest = {
            "version": self.stats["version"],
            "chunks": self.stats["chunks"],
            "sha256": self.stats["sha256"],
            "embedding_model": self.stats["embedding_model"],
            "build_timestamp": self.stats["build_timestamp"],
            "source_files": self.stats["source_files"],
        }

        try:
            with open(manifest_path, "w") as f:
                json.dump(manifest, f, indent=2)

            console.print(f"[green]Generated manifest: {manifest_path.name}[/green]")
            return True

        except Exception as e:
            console.print(f"[red]Failed to generate manifest: {e}[/red]")
            return False

    def _generate_build_info(self) -> None:
        """Generate detailed build info JSON for CI/CD."""
        build_info_path = self.output_dir / BUILD_INFO_NAME

        build_info = {
            **self.stats,
            "archive_name": ARCHIVE_NAME,
            "manifest_name": MANIFEST_NAME,
            "source_dir": str(self.source_dir),
            "python_version": sys.version,
            "clean_build": self.clean,
            "validated": self.validate,
        }

        with open(build_info_path, "w") as f:
            json.dump(build_info, f, indent=2)

        if self.verbose:
            console.print(f"[dim]Generated build info: {build_info_path.name}[/dim]")

    def _print_summary(self) -> None:
        """Print build summary."""
        console.print("\n")

        table = Table(title="Build Summary")
        table.add_column("Metric", style="cyan")
        table.add_column("Value", style="green")

        table.add_row("Version", self.stats["version"])
        table.add_row("Chunks", str(self.stats["chunks"]))
        table.add_row("Source Files", str(self.stats["source_files"]))
        table.add_row("Embedding Model", self.stats["embedding_model"])
        table.add_row("SHA256", self.stats["sha256"][:16] + "...")
        table.add_row("Build Time", self.stats["build_timestamp"])

        console.print(table)

        console.print("\n[bold green]Build completed successfully![/bold green]")
        console.print(f"\nArtifacts in: {self.output_dir}")
        console.print(f"  - {ARCHIVE_NAME}")
        console.print(f"  - {MANIFEST_NAME}")
        console.print(f"  - {BUILD_INFO_NAME}")


def main() -> None:
    """Main entry point."""
    parser = argparse.ArgumentParser(
        description="Build ChromaDB release artifacts for STM32 documentation",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=__doc__,
    )

    parser.add_argument(
        "--version",
        "-V",
        default="dev",
        help="Version string for the release (default: dev)",
    )

    parser.add_argument(
        "--output-dir",
        "-o",
        type=Path,
        default=DEFAULT_OUTPUT_DIR,
        help=f"Output directory for artifacts (default: {DEFAULT_OUTPUT_DIR})",
    )

    parser.add_argument(
        "--source-dir",
        "-s",
        type=Path,
        default=None,
        help="Source directory with markdown files (default: from config)",
    )

    parser.add_argument(
        "--validate/--no-validate",
        default=True,
        dest="validate",
        action=argparse.BooleanOptionalAction,
        help="Validate chunk count (default: enabled)",
    )

    parser.add_argument(
        "--clean",
        "-c",
        action="store_true",
        help="Clean build (don't use existing database)",
    )

    parser.add_argument(
        "--verbose",
        "-v",
        action="store_true",
        help="Verbose output",
    )

    args = parser.parse_args()

    # Configure logging
    log_level = logging.DEBUG if args.verbose else logging.INFO
    logging.basicConfig(
        level=log_level,
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    )

    # Run builder
    builder = DatabaseBuilder(
        output_dir=args.output_dir,
        version=args.version,
        source_dir=args.source_dir,
        validate=args.validate,
        clean=args.clean,
        verbose=args.verbose,
    )

    success = builder.run()
    sys.exit(0 if success else 1)


if __name__ == "__main__":
    main()
