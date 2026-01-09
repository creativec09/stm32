# Releasing the STM32 MCP Documentation Server

This document describes how to create releases for the STM32 MCP Documentation Server, including building and publishing the pre-built ChromaDB database.

## Overview

Each release includes:
1. **Source code** - The MCP server implementation
2. **Pre-built ChromaDB database** - Vector embeddings for ~80 markdown documentation files (~13,815 chunks)
3. **Database manifest** - Metadata including version, checksum, and build info

## Prerequisites

- Python 3.11+
- Git with push access to the repository
- GitHub CLI (`gh`) for manual release management

## Release Methods

### Method 1: Tag-based Release (Recommended)

Create and push a version tag to trigger automatic release:

```bash
# Ensure you're on main branch with latest changes
git checkout main
git pull origin main

# Create annotated tag
git tag -a v1.2.0 -m "Release v1.2.0: Description of changes"

# Push tag to trigger workflow
git push origin v1.2.0
```

The GitHub Actions workflow will:
1. Build the ChromaDB database from source markdowns
2. Validate chunk count (12,000 - 16,000 expected)
3. Create release archive and manifest
4. Create GitHub release with assets attached

### Method 2: Manual Workflow Dispatch

Trigger the workflow manually from GitHub Actions:

1. Go to **Actions** > **Build and Release Database**
2. Click **Run workflow**
3. Fill in options:
   - `version`: Version string (e.g., `v1.2.0`) - leave empty for auto-generate
   - `attach_to_release`: Check to attach to existing release
   - `force_rebuild`: Check to replace existing assets
4. Click **Run workflow**

### Method 3: Create Release First

Create a release in GitHub UI, then the workflow attaches database assets:

1. Go to **Releases** > **Draft a new release**
2. Create tag (e.g., `v1.2.0`)
3. Add release notes
4. Publish release
5. The workflow automatically runs and attaches database assets

## Local Testing

Before creating a release, test the build locally:

```bash
# Quick build (uses existing database if available)
python scripts/build_release_database.py --version v1.2.0-test

# Clean build (rebuilds from scratch)
python scripts/build_release_database.py --version v1.2.0-test --clean

# Build with verbose output
python scripts/build_release_database.py --version v1.2.0-test --clean --verbose

# Build without validation (faster, for quick testing)
python scripts/build_release_database.py --version test --no-validate
```

### Verify Build Output

After building, check the artifacts in `release-artifacts/`:

```bash
# List artifacts
ls -la release-artifacts/

# View manifest
cat release-artifacts/chromadb-manifest.json

# Verify archive structure
tar -tzf release-artifacts/chromadb-stm32-docs.tar.gz | head -20

# Verify checksum matches manifest
sha256sum release-artifacts/chromadb-stm32-docs.tar.gz
```

Expected manifest format:
```json
{
  "version": "v1.2.0",
  "chunks": 13815,
  "sha256": "abc123...",
  "embedding_model": "all-MiniLM-L6-v2",
  "build_timestamp": "2025-01-09T12:00:00+00:00",
  "source_files": 80
}
```

Expected archive structure:
```
chromadb-stm32-docs.tar.gz
└── chroma_db/
    ├── chroma.sqlite3
    └── [embedding index files]
```

## Release Checklist

Before releasing:

- [ ] All tests pass (`pytest tests/`)
- [ ] Markdown documentation is up to date
- [ ] Version number follows semantic versioning
- [ ] CHANGELOG is updated (if applicable)
- [ ] Local build test passes with expected chunk count

During release:

- [ ] GitHub Actions workflow completes successfully
- [ ] Chunk count is in expected range (12,000 - 16,000)
- [ ] Archive and manifest are attached to release
- [ ] SHA256 checksum in manifest matches archive

After release:

- [ ] Test installation: `uvx --from git+https://github.com/creativec09/stm32-agents.git stm32-mcp-docs`
- [ ] Verify database downloads correctly
- [ ] Test basic search functionality

## Troubleshooting

### Build Fails with "Chunk count below minimum"

**Cause**: The ingestion pipeline produced fewer chunks than expected.

**Solutions**:
1. Check that all markdown files are present in `mcp_server/markdowns/`
2. Verify markdown files are not empty or corrupted
3. Check ingestion logs for errors
4. Run local build with `--verbose` for detailed output

### Build Fails with "No markdown files found"

**Cause**: Source directory is missing or empty.

**Solutions**:
1. Ensure `mcp_server/markdowns/` directory exists
2. Check that markdown files have `.md` extension
3. Verify files are not in a subdirectory

### Archive Checksum Mismatch

**Cause**: Archive was modified after checksum calculation.

**Solutions**:
1. Rebuild from scratch with `--clean`
2. Check for filesystem issues
3. Verify no concurrent processes are modifying files

### Database Download Fails for Users

**Cause**: Release assets not properly attached or GitHub API issues.

**Solutions**:
1. Verify assets are visible in GitHub release
2. Check asset names match expected (`chromadb-stm32-docs.tar.gz`, `chromadb-manifest.json`)
3. Try manual download and verification
4. Check GitHub status for API issues

### Workflow Times Out

**Cause**: Database build is taking too long (30 minute timeout).

**Solutions**:
1. Check for large or problematic markdown files
2. Reduce chunk size or overlap settings
3. Investigate embedding model performance
4. Consider splitting the workflow

## Database Versioning

The database version follows the release tag (e.g., `v1.2.0`). The `DatabaseManager` uses the latest release by default, but users can specify a version.

When to bump versions:
- **Patch** (v1.2.x): Documentation updates, bug fixes
- **Minor** (v1.x.0): New peripherals/features documented
- **Major** (vx.0.0): Breaking changes to database schema or API

## Assets and Naming

| Asset | Name | Description |
|-------|------|-------------|
| Database Archive | `chromadb-stm32-docs.tar.gz` | Compressed ChromaDB directory |
| Manifest | `chromadb-manifest.json` | Version, checksum, metadata |

These names are expected by `DatabaseManager` and should not be changed without updating the client code.

## Embedding Model

The default embedding model is `all-MiniLM-L6-v2`:
- 384-dimensional embeddings
- Fast inference
- Good semantic similarity for technical documentation

Changing the model requires:
1. Updating `EMBEDDING_MODEL` in `mcp_server/config.py`
2. Updating `EMBEDDING_MODEL` in `scripts/build_release_database.py`
3. Rebuilding all databases (breaking change for users)

## Security Considerations

- Release assets are publicly accessible
- SHA256 checksum provides integrity verification
- Archive is verified for path traversal attacks
- GitHub token is only used for release operations (not in archive)

## Monitoring

After a release, monitor:
1. Download counts in GitHub Insights
2. User issues related to database download
3. CI/CD workflow success rate
4. Error reports from `DatabaseManager`

## Emergency Procedures

### Rolling Back a Release

```bash
# Delete the release and tag
gh release delete v1.2.0 --yes
git push origin --delete v1.2.0
git tag -d v1.2.0

# The previous release becomes "latest" again
```

### Force Rebuild Existing Release

```bash
# Use workflow dispatch with force_rebuild=true
# Or manually:
gh release delete-asset v1.2.0 chromadb-stm32-docs.tar.gz --yes
gh release delete-asset v1.2.0 chromadb-manifest.json --yes

# Then re-run workflow with attach_to_release=true
```

### Hotfix for Database Issues

1. Create hotfix branch from release tag
2. Fix issues in markdown or pipeline
3. Create new patch release (e.g., v1.2.1)
4. Verify with local build before pushing tag
