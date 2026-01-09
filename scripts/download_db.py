#!/usr/bin/env python3
"""
Download pre-built ChromaDB vector database from GitHub releases.

This script downloads a pre-built vector database to avoid the need for users
to run the time-consuming ingestion process. The database is hosted as a
release asset on GitHub.

Usage:
    python scripts/download_db.py              # Download latest release
    python scripts/download_db.py --version v0.1.0  # Download specific version
    python scripts/download_db.py --check      # Check if update available
    python scripts/download_db.py --info       # Show database info

The database is a compressed archive containing the ChromaDB files.
"""

import sys
import os
import json
import shutil
import hashlib
import tempfile
import argparse
from pathlib import Path
from urllib.request import urlopen, Request
from urllib.error import HTTPError, URLError
from typing import Optional, Dict, Any, Tuple

# Project root
SCRIPT_DIR = Path(__file__).parent
PROJECT_ROOT = SCRIPT_DIR.parent

# Add project to path
sys.path.insert(0, str(PROJECT_ROOT))

# Constants
GITHUB_REPO = "YOUR_USERNAME/stm32-agents"  # Update this!
DB_ASSET_NAME = "chromadb-stm32-docs.tar.gz"
DB_MANIFEST_NAME = "chromadb-manifest.json"
DEFAULT_DB_PATH = PROJECT_ROOT / "data" / "chroma_db"


class Colors:
    """ANSI colors for terminal output."""
    RESET = '\033[0m'
    BOLD = '\033[1m'
    RED = '\033[91m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    BLUE = '\033[94m'
    CYAN = '\033[96m'

    @classmethod
    def disable(cls):
        cls.RESET = cls.BOLD = cls.RED = cls.GREEN = ''
        cls.YELLOW = cls.BLUE = cls.CYAN = ''


def print_info(msg: str):
    print(f"  {Colors.CYAN}[INFO]{Colors.RESET} {msg}")


def print_success(msg: str):
    print(f"  {Colors.GREEN}[OK]{Colors.RESET} {msg}")


def print_warning(msg: str):
    print(f"  {Colors.YELLOW}[WARN]{Colors.RESET} {msg}")


def print_error(msg: str):
    print(f"  {Colors.RED}[ERROR]{Colors.RESET} {msg}")


def get_github_releases(repo: str) -> list:
    """Fetch releases from GitHub API."""
    url = f"https://api.github.com/repos/{repo}/releases"
    req = Request(url, headers={'Accept': 'application/vnd.github.v3+json'})

    try:
        with urlopen(req, timeout=30) as response:
            return json.loads(response.read().decode())
    except HTTPError as e:
        if e.code == 404:
            print_error(f"Repository not found: {repo}")
        else:
            print_error(f"GitHub API error: {e.code}")
        return []
    except URLError as e:
        print_error(f"Network error: {e}")
        return []


def find_db_asset(release: Dict[str, Any]) -> Optional[Dict[str, Any]]:
    """Find the database asset in a release."""
    for asset in release.get('assets', []):
        if asset['name'] == DB_ASSET_NAME:
            return asset
    return None


def find_manifest_asset(release: Dict[str, Any]) -> Optional[Dict[str, Any]]:
    """Find the manifest asset in a release."""
    for asset in release.get('assets', []):
        if asset['name'] == DB_MANIFEST_NAME:
            return asset
    return None


def download_file(url: str, dest: Path, expected_size: Optional[int] = None) -> bool:
    """Download a file with progress indication."""
    req = Request(url, headers={'Accept': 'application/octet-stream'})

    try:
        with urlopen(req, timeout=300) as response:
            total_size = int(response.headers.get('content-length', 0))
            if expected_size and total_size != expected_size:
                print_warning(f"Size mismatch: expected {expected_size}, got {total_size}")

            downloaded = 0
            block_size = 8192

            with open(dest, 'wb') as f:
                while True:
                    chunk = response.read(block_size)
                    if not chunk:
                        break
                    f.write(chunk)
                    downloaded += len(chunk)

                    if total_size > 0:
                        pct = downloaded * 100 // total_size
                        mb_down = downloaded / (1024 * 1024)
                        mb_total = total_size / (1024 * 1024)
                        print(f"\r  Downloading: {pct:3d}% ({mb_down:.1f}/{mb_total:.1f} MB)", end='')

            print()  # New line after progress
            return True

    except (HTTPError, URLError) as e:
        print_error(f"Download failed: {e}")
        return False


def extract_archive(archive_path: Path, dest_dir: Path) -> bool:
    """Extract tar.gz archive."""
    import tarfile

    try:
        dest_dir.mkdir(parents=True, exist_ok=True)

        with tarfile.open(archive_path, 'r:gz') as tar:
            # Security check: ensure no path traversal
            for member in tar.getmembers():
                if member.name.startswith('/') or '..' in member.name:
                    print_error(f"Security: Invalid path in archive: {member.name}")
                    return False

            tar.extractall(dest_dir)

        return True

    except Exception as e:
        print_error(f"Extraction failed: {e}")
        return False


def verify_checksum(file_path: Path, expected_sha256: str) -> bool:
    """Verify file SHA256 checksum."""
    sha256 = hashlib.sha256()
    with open(file_path, 'rb') as f:
        for chunk in iter(lambda: f.read(8192), b''):
            sha256.update(chunk)
    return sha256.hexdigest() == expected_sha256


def get_local_db_info() -> Optional[Dict[str, Any]]:
    """Get information about local database."""
    manifest_path = DEFAULT_DB_PATH / "manifest.json"
    if manifest_path.exists():
        try:
            with open(manifest_path) as f:
                return json.load(f)
        except Exception:
            pass

    # Check if DB exists but no manifest
    if DEFAULT_DB_PATH.exists() and (DEFAULT_DB_PATH / "chroma.sqlite3").exists():
        return {"version": "unknown", "chunks": "unknown", "created": "unknown"}

    return None


def download_database(version: Optional[str] = None, force: bool = False) -> bool:
    """Download and install the pre-built database."""
    print(f"\n{Colors.BOLD}{Colors.BLUE}STM32 MCP - Download Pre-built Database{Colors.RESET}\n")

    # Check for existing database
    local_info = get_local_db_info()
    if local_info and not force:
        print_info(f"Existing database found (version: {local_info.get('version', 'unknown')})")
        print_info("Use --force to replace it")
        return True

    # Get releases
    print_info("Fetching releases from GitHub...")
    releases = get_github_releases(GITHUB_REPO)

    if not releases:
        print_error("No releases found or repository not accessible")
        print_info("You may need to run ingestion manually: stm32-ingest --clear")
        return False

    # Find target release
    target_release = None
    if version:
        for rel in releases:
            if rel['tag_name'] == version:
                target_release = rel
                break
        if not target_release:
            print_error(f"Version {version} not found")
            return False
    else:
        # Use latest release
        target_release = releases[0]

    print_info(f"Selected release: {target_release['tag_name']}")

    # Find database asset
    db_asset = find_db_asset(target_release)
    if not db_asset:
        print_warning(f"No database asset found in release {target_release['tag_name']}")
        print_info("This release may not include a pre-built database")
        print_info("Run ingestion manually: stm32-ingest --clear")
        return False

    # Download to temp file
    with tempfile.TemporaryDirectory() as tmpdir:
        tmp_path = Path(tmpdir)
        archive_path = tmp_path / DB_ASSET_NAME

        print_info(f"Downloading {db_asset['name']} ({db_asset['size'] / 1024 / 1024:.1f} MB)...")

        if not download_file(db_asset['browser_download_url'], archive_path, db_asset['size']):
            return False

        print_success("Download complete")

        # Download manifest if available
        manifest_asset = find_manifest_asset(target_release)
        manifest_data = None
        if manifest_asset:
            manifest_path = tmp_path / DB_MANIFEST_NAME
            if download_file(manifest_asset['browser_download_url'], manifest_path):
                try:
                    with open(manifest_path) as f:
                        manifest_data = json.load(f)

                    # Verify checksum
                    if 'sha256' in manifest_data:
                        print_info("Verifying checksum...")
                        if verify_checksum(archive_path, manifest_data['sha256']):
                            print_success("Checksum verified")
                        else:
                            print_error("Checksum mismatch - download may be corrupted")
                            return False
                except Exception as e:
                    print_warning(f"Could not parse manifest: {e}")

        # Backup existing database
        if DEFAULT_DB_PATH.exists() and any(DEFAULT_DB_PATH.iterdir()):
            backup_path = DEFAULT_DB_PATH.parent / "chroma_db_backup"
            print_info(f"Backing up existing database to {backup_path}")
            if backup_path.exists():
                shutil.rmtree(backup_path)
            shutil.move(str(DEFAULT_DB_PATH), str(backup_path))

        # Extract
        print_info("Extracting database...")
        DEFAULT_DB_PATH.mkdir(parents=True, exist_ok=True)

        if not extract_archive(archive_path, DEFAULT_DB_PATH.parent):
            # Restore backup
            backup_path = DEFAULT_DB_PATH.parent / "chroma_db_backup"
            if backup_path.exists():
                shutil.move(str(backup_path), str(DEFAULT_DB_PATH))
            return False

        print_success("Database extracted")

        # Write manifest
        if manifest_data:
            manifest_data['installed_from'] = target_release['tag_name']
            with open(DEFAULT_DB_PATH / "manifest.json", 'w') as f:
                json.dump(manifest_data, f, indent=2)

        # Clean up backup
        backup_path = DEFAULT_DB_PATH.parent / "chroma_db_backup"
        if backup_path.exists():
            shutil.rmtree(backup_path)

    # Verify installation
    print_info("Verifying installation...")
    try:
        from storage.chroma_store import STM32ChromaStore
        from mcp_server.config import settings

        store = STM32ChromaStore(
            persist_dir=settings.CHROMA_DB_PATH,
            collection_name=settings.COLLECTION_NAME,
            embedding_model=settings.EMBEDDING_MODEL
        )
        count = store.count()
        print_success(f"Database contains {count} document chunks")

    except Exception as e:
        print_warning(f"Could not verify database: {e}")

    print(f"\n{Colors.GREEN}Database installation complete!{Colors.RESET}")
    return True


def check_for_updates() -> bool:
    """Check if a newer database version is available."""
    print(f"\n{Colors.BOLD}{Colors.BLUE}Checking for Updates{Colors.RESET}\n")

    local_info = get_local_db_info()
    if not local_info:
        print_info("No local database found")
        print_info("Run: stm32-setup --ingest  OR  python scripts/download_db.py")
        return False

    releases = get_github_releases(GITHUB_REPO)
    if not releases:
        print_error("Could not fetch releases")
        return False

    latest = releases[0]
    db_asset = find_db_asset(latest)

    if not db_asset:
        print_info("Latest release has no database asset")
        return False

    local_version = local_info.get('version', 'unknown')
    remote_version = latest['tag_name']

    print_info(f"Local version:  {local_version}")
    print_info(f"Latest version: {remote_version}")

    if local_version == remote_version:
        print_success("Database is up to date")
        return True
    elif local_version == 'unknown':
        print_warning("Local database version unknown - consider updating")
    else:
        print_warning(f"Update available: {local_version} -> {remote_version}")
        print_info("Run: python scripts/download_db.py --force")

    return True


def show_info() -> None:
    """Show information about local and remote databases."""
    print(f"\n{Colors.BOLD}{Colors.BLUE}Database Information{Colors.RESET}\n")

    # Local info
    print(f"{Colors.CYAN}Local Database:{Colors.RESET}")
    local_info = get_local_db_info()

    if local_info:
        print(f"  Path: {DEFAULT_DB_PATH}")
        print(f"  Version: {local_info.get('version', 'unknown')}")
        print(f"  Chunks: {local_info.get('chunks', 'unknown')}")
        print(f"  Created: {local_info.get('created', 'unknown')}")

        # Get actual size
        if DEFAULT_DB_PATH.exists():
            total_size = sum(f.stat().st_size for f in DEFAULT_DB_PATH.rglob('*') if f.is_file())
            print(f"  Size: {total_size / 1024 / 1024:.1f} MB")
    else:
        print("  Not installed")

    # Remote info
    print(f"\n{Colors.CYAN}Remote Database:{Colors.RESET}")
    releases = get_github_releases(GITHUB_REPO)

    if releases:
        latest = releases[0]
        db_asset = find_db_asset(latest)

        print(f"  Repository: {GITHUB_REPO}")
        print(f"  Latest release: {latest['tag_name']}")
        print(f"  Published: {latest['published_at']}")

        if db_asset:
            print(f"  Database asset: {db_asset['name']}")
            print(f"  Size: {db_asset['size'] / 1024 / 1024:.1f} MB")
            print(f"  Downloads: {db_asset.get('download_count', 'N/A')}")
        else:
            print("  Database asset: Not available")
    else:
        print("  Could not fetch release information")


def main():
    """Main entry point."""
    parser = argparse.ArgumentParser(
        description="Download pre-built STM32 documentation database",
        formatter_class=argparse.RawDescriptionHelpFormatter
    )

    parser.add_argument(
        '--version', '-v',
        help='Specific version to download (e.g., v0.1.0)'
    )
    parser.add_argument(
        '--force', '-f',
        action='store_true',
        help='Force download even if database exists'
    )
    parser.add_argument(
        '--check', '-c',
        action='store_true',
        help='Check for updates without downloading'
    )
    parser.add_argument(
        '--info', '-i',
        action='store_true',
        help='Show database information'
    )
    parser.add_argument(
        '--no-color',
        action='store_true',
        help='Disable colored output'
    )

    args = parser.parse_args()

    if args.no_color or not sys.stdout.isatty():
        Colors.disable()

    if args.info:
        show_info()
        return 0

    if args.check:
        check_for_updates()
        return 0

    success = download_database(args.version, args.force)
    return 0 if success else 1


if __name__ == "__main__":
    sys.exit(main())
