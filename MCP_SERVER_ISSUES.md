# STM32 MCP Server — Known Issues & Migration Notes

## Current Status: Partially Broken (March 2026)

The MCP docs server starts and connects but **all query tools fail** due to embedding dimension mismatch. The server needs migration to Voyage AI embeddings.

---

## Issues Found & Fixed

### 1. `trust_remote_code=True` (FIXED)
**File:** `storage/chroma_store.py` line 89
**Problem:** `SentenceTransformer()` call needed `trust_remote_code=True` for the nomic-bert model.
**Fix:** Added `trust_remote_code=True` parameter. Committed and pushed.

### 2. Missing `einops` dependency (FIXED)
**File:** `pyproject.toml`
**Problem:** The nomic-embed-text-v1.5 model requires `einops` at runtime, not listed in dependencies.
**Fix:** Added `"einops>=0.7.0"` to dependencies. Committed and pushed.

### 3. Embedding Dimension Mismatch (STILL BROKEN)
**Problem:** Two conflicting defaults for the embedding model:
- `mcp_server/config.py` line 252: `EMBEDDING_MODEL` defaults to `EmbeddingModel.NOMIC_V15` (768 dimensions)
- `storage/chroma_store.py` line 41: `__init__` parameter defaults to `"all-MiniLM-L6-v2"` (384 dimensions)

The ChromaDB collection was built with MiniLM (384-dim) during initial indexing. When the config later passes nomic (768-dim) for queries, ChromaDB rejects the query: `Embedding dimension 768 does not match collection dimensionality 384`.

**To fix temporarily:** Either:
- Set env var `STM32_EMBEDDING_MODEL=all-MiniLM-L6-v2` to force 384-dim everywhere
- OR delete ALL ChromaDB caches and ensure both config and constructor agree on the same model:
  ```bash
  find /home/jordan/.cache/uv/archive-v0 -name "chroma_db" -type d -exec rm -rf {} +
  rm -rf /mnt/c/Users/creat/Claude/stm32-agents/data/chroma_db
  ```

### 4. uv Cache Sprawl
**Problem:** The `uvx` tool creates multiple isolated virtual environments in `/home/jordan/.cache/uv/archive-v0/*/`. Each has its own copy of the package, ChromaDB data, and dependencies. Patches to source code don't propagate to all cached copies.

**Locations with copies:**
- `/home/jordan/.cache/uv/archive-v0/V0T1CAMI_DIToIpWfLNRR/` (most recent)
- 8+ other archive directories
- `/home/jordan/.claude/plugins/cache/stm32-marketplace/stm32/1.2.3/`
- `/mnt/c/Users/creat/Claude/stm32-agents/` (git repo source)

**To fix:** After any source code change:
1. Push to GitHub
2. `uv cache clean` to clear all archives
3. Kill the server process
4. `/reload-plugins` + `/mcp` reconnect
5. The server re-downloads from GitHub and rebuilds

---

## Planned Migration: Voyage AI Embeddings

### Why migrate
- nomic-embed-text-v1.5 requires `trust_remote_code` and `einops` — fragile dependency chain
- Local embedding model uses ~800MB RAM and takes 15+ seconds to load
- Voyage AI provides better quality embeddings via API (no local model needed)
- `voyage-3-large` for indexing, `voyage-3-lite` (or nano) for queries — fast and accurate

### Migration plan
1. Replace `SentenceTransformer` with Voyage AI Python SDK (`voyageai`)
2. Add `STM32_VOYAGE_API_KEY` to config (env var, `.env` file, or MCP config `env` field)
3. Update `ChromaStore._generate_embeddings()` to call Voyage API
4. Update `pyproject.toml` dependencies: remove `sentence-transformers`, `einops`; add `voyageai`
5. Delete all ChromaDB data (dimension will change)
6. Re-index all STM32 documentation with Voyage embeddings
7. Update config to remove `EmbeddingModel` enum (no longer needed)

### Key files to modify
- `storage/chroma_store.py` — replace embedding generation
- `mcp_server/config.py` — update embedding config
- `pyproject.toml` — swap dependencies
- `mcp_server/server.py` — ensure Voyage API key is loaded

---

## Architecture Notes

### Server startup flow
1. `uvx` downloads package from `git+https://github.com/creativec09/stm32.git`
2. Installs into isolated venv at `/home/jordan/.cache/uv/archive-v0/<hash>/`
3. Runs `stm32-mcp-docs` entry point
4. Starts SSE server on `http://127.0.0.1:8765`
5. `mcp-proxy` bridges SSE ↔ stdio for Claude Code
6. On first query, lazy-loads embedding model and builds/queries ChromaDB

### Plugin configuration
- Plugin config: `/home/jordan/.claude/plugins/cache/stm32-marketplace/stm32/1.2.3/`
- MCP connection: SSE via `mcp-proxy` to `http://127.0.0.1:8765/sse`
- Daemon startup script: `.claude/skills/stm32-setup.md` (references `STM32_SERVER_MODE=network`)

### Data directory
- ChromaDB: `data/chroma_db/` (relative to package install, NOT the git repo)
- STM32 docs source: `data/docs/` (markdown files indexed into ChromaDB)
- The DB is **inside the uv archive**, not in the git repo's `data/` directory
