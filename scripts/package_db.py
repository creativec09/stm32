#!/usr/bin/env python3
"""
Package ChromaDB for GitHub release distribution.

This script creates a compressed archive of the ChromaDB vector database
suitable for distribution via GitHub releases. It also generates a manifest
file with checksums and metadata.

Usage:
    python scripts/package_db.py              # Package with auto-detected version
    python scripts/package_db.py --version v0.1.0  # Package with specific version
    python scripts/package_db.py --output ./release  # Custom output directory

Output:
    - chromadb-stm32-docs.tar.gz  - Compressed database archive
    - chromadb-manifest.json      - Metadata and checksum
"""

import sys
import os
import json
import hashlib
import tarfile
import argparse
from pathlib import Path
from datetime import datetime, timezone

# Project root
SCRIPT_DIR = Path(__file__).parent
PROJECT_ROOT = SCRIPT_DIR.parent

# Add project to path
sys.path.insert(0, str(PROJECT_ROOT))

# Constants
DEFAULT_DB_PATH = PROJECT_ROOT / "data" / "chroma_db"
DEFAULT_OUTPUT_DIR = PROJECT_ROOT / "dist"


def get_db_stats(db_path: Path) -> dict:
    """Get statistics about the ChromaDB."""
    try:
        from storage.chroma_store import STM32ChromaStore
        from mcp_server.config import settings

        store = STM32ChromaStore(
            persist_dir=db_path,
            collection_name=settings.COLLECTION_NAME,
            embedding_model=settings.EMBEDDING_MODEL
        )

        return {
            "chunks": store.count(),
            "sources": len(store.list_sources()),
            "peripherals": store.get_peripheral_distribution(),
            "doc_types": store.get_doc_type_distribution()
        }
    except Exception as e:
        print(f"Warning: Could not get DB stats: {e}")
        return {}


def calculate_sha256(file_path: Path) -> str:
    """Calculate SHA256 hash of a file."""
    sha256 = hashlib.sha256()
    with open(file_path, 'rb') as f:
        for chunk in iter(lambda: f.read(8192), b''):
            sha256.update(chunk)
    return sha256.hexdigest()


def get_version() -> str:
    """Get version from pyproject.toml or git tag."""
    # Try pyproject.toml
    pyproject_path = PROJECT_ROOT / "pyproject.toml"
    if pyproject_path.exists():
        import re
        content = pyproject_path.read_text()
        match = re.search(r'version\s*=\s*"([^"]+)"', content)
        if match:
            return f"v{match.group(1)}"

    # Try git tag
    try:
        import subprocess
        result = subprocess.run(
            ['git', 'describe', '--tags', '--abbrev=0'],
            capture_output=True,
            text=True,
            cwd=PROJECT_ROOT
        )
        if result.returncode == 0:
            return result.stdout.strip()
    except Exception:
        pass

    return "v0.0.0"


def package_database(
    db_path: Path,
    output_dir: Path,
    version: str = None
) -> tuple:
    """
    Package the ChromaDB into a distributable archive.

    Returns:
        Tuple of (archive_path, manifest_path)
    """
    if not db_path.exists():
        raise FileNotFoundError(f"Database not found: {db_path}")

    version = version or get_version()
    output_dir.mkdir(parents=True, exist_ok=True)

    # Archive name
    archive_name = "chromadb-stm32-docs.tar.gz"
    archive_path = output_dir / archive_name
    manifest_path = output_dir / "chromadb-manifest.json"

    print(f"Packaging ChromaDB v{version}")
    print(f"  Source: {db_path}")
    print(f"  Output: {archive_path}")

    # Get database stats before packaging
    print("  Getting database statistics...")
    stats = get_db_stats(db_path)

    # Create tarball
    print("  Creating archive...")
    with tarfile.open(archive_path, 'w:gz') as tar:
        # Add the chroma_db directory
        for item in db_path.iterdir():
            arcname = f"chroma_db/{item.name}"
            tar.add(item, arcname=arcname)

    archive_size = archive_path.stat().st_size
    print(f"  Archive size: {archive_size / 1024 / 1024:.1f} MB")

    # Calculate checksum
    print("  Calculating checksum...")
    sha256 = calculate_sha256(archive_path)

    # Create manifest
    manifest = {
        "version": version,
        "created": datetime.now(timezone.utc).isoformat(),
        "archive": archive_name,
        "size": archive_size,
        "sha256": sha256,
        "chunks": stats.get("chunks", 0),
        "sources": stats.get("sources", 0),
        "embedding_model": "all-MiniLM-L6-v2",
        "peripherals": stats.get("peripherals", {}),
        "doc_types": stats.get("doc_types", {})
    }

    with open(manifest_path, 'w') as f:
        json.dump(manifest, f, indent=2)

    print(f"  Manifest: {manifest_path}")
    print("\nPackaging complete!")
    print(f"\nManifest contents:")
    print(json.dumps(manifest, indent=2))

    return archive_path, manifest_path


def main():
    parser = argparse.ArgumentParser(
        description="Package ChromaDB for GitHub release"
    )

    parser.add_argument(
        '--db-path',
        type=Path,
        default=DEFAULT_DB_PATH,
        help=f'Path to ChromaDB directory (default: {DEFAULT_DB_PATH})'
    )
    parser.add_argument(
        '--output', '-o',
        type=Path,
        default=DEFAULT_OUTPUT_DIR,
        help=f'Output directory (default: {DEFAULT_OUTPUT_DIR})'
    )
    parser.add_argument(
        '--version', '-v',
        help='Version string (default: auto-detect)'
    )

    args = parser.parse_args()

    try:
        archive_path, manifest_path = package_database(
            args.db_path,
            args.output,
            args.version
        )

        print(f"\n--- Upload these to GitHub release: ---")
        print(f"  {archive_path}")
        print(f"  {manifest_path}")

    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        return 1

    return 0


if __name__ == "__main__":
    sys.exit(main())
