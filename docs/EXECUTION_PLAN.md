# Universal DocSearch Platform - Agent Execution Plan

## Overview

This document contains agent-executable tasks for building the universal documentation search platform. Each task is designed to be run by an Opus-level agent with comprehensive context.

**Execution Model**: Tasks are organized into phases. Within each phase, tasks marked `[PARALLEL]` can run simultaneously. Tasks marked `[SEQUENTIAL]` must wait for dependencies.

---

## Claude Code Plugin Architecture Requirements

**CRITICAL**: Based on official Claude Code documentation validation, our plugins MUST follow these patterns:

### Plugin Structure (REQUIRED)
```
docsearch-stm32/
├── .claude-plugin/
│   └── plugin.json          # Plugin manifest (REQUIRED)
├── agents/
│   ├── stm32-firmware.md    # Auto-discovered by Claude Code
│   ├── stm32-debug.md       # NO copying to ~/.claude/agents/
│   └── ...
├── commands/
│   ├── search.md            # Becomes /stm32:search
│   └── init.md              # Becomes /stm32:init
├── server/
│   └── .mcp.json            # Bundled MCP server config
└── src/
    └── docsearch_stm32/
        └── ...
```

### Agent Frontmatter (REQUIRED)
```yaml
---
name: stm32-firmware                    # REQUIRED: lowercase, hyphens, matches filename
description: Expert STM32 firmware...   # REQUIRED: detailed for Claude's delegation decision
tools: Read, Grep, Glob, Bash          # OPTIONAL: restrict available tools
model: sonnet                           # OPTIONAL: sonnet, opus, haiku, or inherit
---
```

### Plugin Manifest (REQUIRED)
```json
// .claude-plugin/plugin.json
{
  "name": "stm32",
  "description": "STM32 microcontroller documentation search",
  "version": "1.0.0",
  "author": {"name": "Your Name"},
  "repository": "https://github.com/creativec09/stm32"
}
```

### Key Architecture Rules
1. **Agents are auto-discovered** from plugin's `agents/` directory - DO NOT copy to `~/.claude/agents/`
2. **Commands are namespaced** - `/stm32:search` not `/stm32-search`
3. **MCP servers are bundled** - defined in `server/.mcp.json` or inline in `plugin.json`
4. **First-run init** should only build database, NOT copy agents/commands

---

## Patterns to Steal from Existing Projects

### From Knowledge-Base-MCP (puran-water)
- [ ] Quality gates with canary QA framework
- [ ] Deterministic ingestion (smart update detection)
- [ ] Multi-collection support with independent tools
- [ ] Structured tool organization (31 tools pattern)

### From RAG-CLI (ItMeDiaTech)
- [ ] Native Claude Code slash command integration
- [ ] `/rag-project` auto-indexing pattern
- [ ] Fast vector search (<100ms target)
- [ ] Local-first processing architecture

### From Docs-MCP-Server (arabold)
- [ ] Web UI for document management
- [ ] Multi-source ingestion (GitHub, npm, PyPI, local)
- [ ] Version-aware documentation
- [ ] Intelligent semantic chunking

### From Context7 (upstash)
- [ ] Library version resolution pattern
- [ ] Real-time documentation updates
- [ ] Community contribution model

---

## Phase 0: Project Audit [SEQUENTIAL - Run First]

### Task 0.1: Audit Knowledge-Base-MCP
```
AGENT_TYPE: Opus
EXECUTION: SEQUENTIAL (must complete before Phase 1)
ESTIMATED_TIME: 30 minutes
```

**Prompt for Agent:**
```
You are auditing the Knowledge-Base-MCP project to extract reusable patterns for our universal documentation search platform.

Clone and analyze: https://github.com/puran-water/knowledge-base-mcp

Your mission:
1. Clone the repository to a temporary directory
2. Read and analyze the following files (in order):
   - README.md (understand overall architecture)
   - pyproject.toml (dependencies we might need)
   - src/ directory structure
   - Any files related to:
     - Quality gates / canary QA
     - Ingestion pipeline
     - Search implementation (hybrid, BM25, rerank)
     - Multi-collection support

3. Create a detailed report covering:

   A. ARCHITECTURE PATTERNS
   - How they structure their codebase
   - How they separate concerns
   - Configuration management approach

   B. QUALITY GATES (Priority - we want this)
   - How canary QA works
   - What metrics they track (recall, nDCG, latency)
   - How thresholds are configured
   - Implementation code snippets we can adapt

   C. INGESTION PIPELINE
   - Deterministic update detection mechanism
   - How they handle PDFs (Docling integration)
   - Chunking strategy
   - Metadata extraction

   D. SEARCH IMPLEMENTATION
   - Their hybrid search approach
   - Cross-encoder reranking
   - How they combine BM25 + vector

   E. TOOL ORGANIZATION
   - How they expose 31 tools
   - Tool naming conventions
   - Parameter schemas

4. Output a file: docs/audits/knowledge-base-mcp-audit.md

Do NOT modify any code in our repository yet. This is research only.
```

---

### Task 0.2: Audit RAG-CLI
```
AGENT_TYPE: Opus
EXECUTION: PARALLEL with Task 0.1
ESTIMATED_TIME: 30 minutes
```

**Prompt for Agent:**
```
You are auditing the RAG-CLI project to extract reusable patterns for our universal documentation search platform.

Clone and analyze: https://github.com/ItMeDiaTech/rag-cli

Your mission:
1. Clone the repository to a temporary directory
2. Read and analyze the codebase focusing on:
   - How they integrate with Claude Code
   - Their slash command implementation
   - Vector search performance optimizations
   - Local-first architecture

3. Create a detailed report covering:

   A. CLAUDE CODE INTEGRATION (Priority - we want this)
   - How /rag-project command works
   - How they register slash commands
   - Command argument handling
   - How they communicate results back to Claude

   B. PERFORMANCE OPTIMIZATIONS
   - How they achieve <100ms vector search
   - Caching strategies
   - Batch processing approaches
   - Index optimization techniques

   C. LOCAL-FIRST ARCHITECTURE
   - How they handle document processing locally
   - ChromaDB configuration
   - Embedding generation approach
   - Memory management for large doc sets

   D. MULTI-FORMAT SUPPORT
   - How they handle Markdown, PDF, DOCX, HTML
   - Format detection
   - Content extraction per format

   E. INDEXING PATTERNS
   - Auto-indexing on project open
   - Incremental indexing
   - Index invalidation

4. Output a file: docs/audits/rag-cli-audit.md

Do NOT modify any code in our repository yet. This is research only.
```

---

### Task 0.3: Audit Docs-MCP-Server
```
AGENT_TYPE: Opus
EXECUTION: PARALLEL with Tasks 0.1, 0.2
ESTIMATED_TIME: 30 minutes
```

**Prompt for Agent:**
```
You are auditing the Docs-MCP-Server project to extract reusable patterns for our universal documentation search platform.

Clone and analyze: https://github.com/arabold/docs-mcp-server

Your mission:
1. Clone the repository to a temporary directory
2. Read and analyze the codebase focusing on:
   - Web UI implementation
   - Multi-source ingestion
   - Version-aware search
   - Semantic chunking

3. Create a detailed report covering:

   A. WEB UI FOR DOCUMENT MANAGEMENT
   - Tech stack (React? Vue? Plain HTML?)
   - API endpoints for CRUD operations
   - How they handle file uploads
   - UI/UX patterns worth copying

   B. MULTI-SOURCE INGESTION (Priority)
   - GitHub repository scraping
   - npm/PyPI package doc fetching
   - Local file handling (file:// URLs)
   - URL normalization and validation

   C. VERSION-AWARE DOCUMENTATION
   - How they track library versions
   - Version resolution logic
   - Storing multiple versions
   - Querying specific versions

   D. SEMANTIC CHUNKING
   - How they split documents intelligently
   - Code block preservation
   - Section boundary detection
   - Chunk size strategies

   E. CONFIGURATION
   - How users configure the server
   - Environment variables
   - Runtime configuration

4. Output a file: docs/audits/docs-mcp-server-audit.md

Do NOT modify any code in our repository yet. This is research only.
```

---

### Task 0.4: Synthesize Audit Findings
```
AGENT_TYPE: Opus
EXECUTION: SEQUENTIAL (after Tasks 0.1, 0.2, 0.3 complete)
ESTIMATED_TIME: 20 minutes
DEPENDENCIES: Task 0.1, Task 0.2, Task 0.3
```

**Prompt for Agent:**
```
You have access to three audit reports in docs/audits/:
- knowledge-base-mcp-audit.md
- rag-cli-audit.md
- docs-mcp-server-audit.md

Your mission is to synthesize these into actionable recommendations.

Read all three audit files, then create: docs/audits/SYNTHESIS.md

The synthesis document must contain:

1. ARCHITECTURE DECISION
   - Which project's architecture is closest to our needs?
   - What modifications are needed?
   - Recommended package structure

2. COMPONENTS TO STEAL (with code references)
   For each component, specify:
   - Source project and file path
   - What to copy vs. adapt
   - Integration points with our existing code

   Components:
   - [ ] Quality gates framework
   - [ ] Slash command integration
   - [ ] Multi-source ingestion
   - [ ] Performance optimizations
   - [ ] Web UI (optional)

3. COMPONENTS TO KEEP FROM OUR CODEBASE
   - storage/bm25_index.py (STM32 tokenizer)
   - storage/hybrid_retriever.py (RRF fusion)
   - mcp_server/query_expansion.py (172 synonyms)
   - mcp_server/reranker.py (Claude headless)
   - mcp_server/query_parser.py (HAL/register detection)

4. INTEGRATION PLAN
   - Order of integration
   - Potential conflicts
   - Testing strategy

5. UPDATED PACKAGE STRUCTURE
   Based on learnings, propose final structure for:
   - docsearch-core/
   - docsearch-stm32/

Output the synthesis document only. Do not modify code yet.
```

---

## Phase 1: Extract Core Library [SEQUENTIAL within phase]

### Task 1.1: Create Core Package Structure
```
AGENT_TYPE: Opus
EXECUTION: SEQUENTIAL (first in Phase 1)
ESTIMATED_TIME: 15 minutes
DEPENDENCIES: Phase 0 complete
```

**Prompt for Agent:**
```
You are creating the package structure for docsearch-core, the domain-agnostic core library.

Based on the synthesis in docs/audits/SYNTHESIS.md, create the following structure:

packages/
└── docsearch-core/
    ├── pyproject.toml
    ├── README.md
    └── src/
        └── docsearch_core/
            ├── __init__.py
            ├── retrieval/
            │   ├── __init__.py
            │   ├── hybrid.py      (placeholder)
            │   └── bm25.py        (placeholder)
            ├── storage/
            │   ├── __init__.py
            │   └── chroma_store.py (placeholder)
            ├── ranking/
            │   ├── __init__.py
            │   └── reranker.py    (placeholder)
            ├── tokenization/
            │   ├── __init__.py
            │   ├── base.py        (placeholder)
            │   └── default.py     (placeholder)
            ├── expansion/
            │   ├── __init__.py
            │   └── base.py        (placeholder)
            ├── plugins/
            │   ├── __init__.py
            │   ├── base.py        (placeholder)
            │   └── registry.py    (placeholder)
            ├── quality/           (NEW - from Knowledge-Base-MCP)
            │   ├── __init__.py
            │   ├── gates.py       (placeholder)
            │   └── metrics.py     (placeholder)
            └── config/
                ├── __init__.py
                └── settings.py    (placeholder)

For pyproject.toml, include:
- Name: docsearch-core
- Version: 0.1.0
- Dependencies from our current pyproject.toml (chromadb, sentence-transformers, etc.)
- Add any new dependencies identified in the synthesis

Each placeholder file should contain:
- Module docstring explaining purpose
- TODO comments for what will be implemented
- Any base classes/protocols that define the interface

Create all files. This is the foundation for everything else.
```

---

### Task 1.2: Extract Base Tokenizer Interface
```
AGENT_TYPE: Opus
EXECUTION: SEQUENTIAL (after 1.1)
ESTIMATED_TIME: 20 minutes
DEPENDENCIES: Task 1.1
```

**Prompt for Agent:**
```
You are extracting the tokenization interface for docsearch-core.

Read our current implementation:
- storage/bm25_index.py (contains STM32Tokenizer class)

Your task:
1. Create a domain-agnostic base tokenizer in:
   packages/docsearch-core/src/docsearch_core/tokenization/base.py

   The base tokenizer must:
   - Define TokenizerProtocol (typing.Protocol)
   - Define BaseTokenizer abstract class
   - Include methods:
     - tokenize(text: str) -> List[str]
     - filter_tokens(tokens: List[str]) -> List[str]
   - Support configurable:
     - lowercase: bool
     - min_token_length: int
     - stopwords: Set[str]
     - preserve_patterns: List[re.Pattern] (for domain-specific terms)

2. Create a default tokenizer in:
   packages/docsearch-core/src/docsearch_core/tokenization/default.py

   This should be a basic English tokenizer that:
   - Splits on whitespace and punctuation
   - Removes stopwords
   - Applies lowercase
   - Preserves code-like tokens (camelCase, snake_case)

3. Update the __init__.py to export:
   - TokenizerProtocol
   - BaseTokenizer
   - DefaultTokenizer

4. Write tests in:
   packages/docsearch-core/tests/test_tokenization.py

   Test cases:
   - Basic tokenization
   - Stopword removal
   - Pattern preservation
   - Edge cases (empty string, unicode, etc.)

The interface must be general enough that our STM32Tokenizer can extend it later.
```

---

### Task 1.3: Extract BM25 Index
```
AGENT_TYPE: Opus
EXECUTION: PARALLEL with Task 1.4
ESTIMATED_TIME: 25 minutes
DEPENDENCIES: Task 1.2
```

**Prompt for Agent:**
```
You are extracting the BM25 index implementation for docsearch-core.

Read our current implementation:
- storage/bm25_index.py

Your task:
1. Create a domain-agnostic BM25 index in:
   packages/docsearch-core/src/docsearch_core/retrieval/bm25.py

   Requirements:
   - Remove all STM32-specific code (move to domain plugin later)
   - Accept any TokenizerProtocol for tokenization
   - Support BM25, BM25+, and BM25L algorithms via config
   - Include BM25Config dataclass with:
     - k1: float = 1.5
     - b: float = 0.75
     - delta: float = 0.5
     - algorithm: Literal["bm25", "bm25plus", "bm25l"] = "bm25plus"

   - Methods:
     - add_documents(docs: List[Tuple[str, str, Dict]]) -> None
     - search(query_tokens: List[str], k: int, filters: Dict) -> List[SearchResult]
     - remove_document(doc_id: str) -> bool
     - get_stats() -> Dict

   - Support metadata filtering in search

2. Create SearchResult dataclass in:
   packages/docsearch-core/src/docsearch_core/retrieval/__init__.py

   Fields:
   - chunk_id: str
   - content: str
   - score: float
   - metadata: Dict[str, Any]
   - source: str  # "bm25", "semantic", "hybrid"
   - rank: int

3. Write tests in:
   packages/docsearch-core/tests/test_bm25.py

   Test cases:
   - Document indexing
   - Basic search
   - Search with filters
   - BM25 vs BM25+ scoring differences
   - Empty index handling
   - Document removal

Steal the deterministic indexing pattern from Knowledge-Base-MCP if identified in the audit.
```

---

### Task 1.4: Extract Hybrid Retriever
```
AGENT_TYPE: Opus
EXECUTION: PARALLEL with Task 1.3
ESTIMATED_TIME: 25 minutes
DEPENDENCIES: Task 1.2
```

**Prompt for Agent:**
```
You are extracting the hybrid retriever for docsearch-core.

Read our current implementations:
- storage/hybrid_retriever.py
- storage/chroma_store.py

Your task:
1. Create ChromaStore wrapper in:
   packages/docsearch-core/src/docsearch_core/storage/chroma_store.py

   Requirements:
   - Domain-agnostic (no STM32 references)
   - ChromaConfig dataclass:
     - persist_directory: Path
     - collection_name: str
     - embedding_model: str = "nomic-ai/nomic-embed-text-v1.5"
     - distance_metric: str = "cosine"
   - Methods:
     - add_documents(docs: List[Tuple[str, str, Dict]])
     - search(query: str, k: int, filters: Dict) -> List[SearchResult]
     - delete_collection()
     - get_stats() -> Dict

2. Create HybridRetriever in:
   packages/docsearch-core/src/docsearch_core/retrieval/hybrid.py

   Requirements:
   - Accept pluggable BM25Index and ChromaStore
   - Accept pluggable TokenizerProtocol
   - Accept optional query_expander: Callable[[str], str]
   - HybridRetrieverConfig:
     - bm25_weight: float = 0.4
     - semantic_weight: float = 0.6
     - bm25_k: int = 50
     - semantic_k: int = 50
     - final_k: int = 20
     - rrf_k: int = 60
     - fusion_method: Literal["rrf", "linear", "max"] = "rrf"

   - Methods:
     - search(query: str, k: int, filters: Dict) -> List[SearchResult]

   - Implement RRF (Reciprocal Rank Fusion) as primary fusion method

3. Write tests in:
   packages/docsearch-core/tests/test_hybrid.py

   Test cases:
   - RRF fusion correctness
   - Weight balancing
   - Filter propagation
   - Empty results handling

Steal performance optimizations from RAG-CLI audit if applicable.
```

---

### Task 1.5: Extract Reranker
```
AGENT_TYPE: Opus
EXECUTION: PARALLEL with Tasks 1.3, 1.4
ESTIMATED_TIME: 20 minutes
DEPENDENCIES: Task 1.2
```

**Prompt for Agent:**
```
You are extracting the Claude reranker for docsearch-core.

Read our current implementation:
- mcp_server/reranker.py

Your task:
1. Create base reranker in:
   packages/docsearch-core/src/docsearch_core/ranking/reranker.py

   Requirements:
   - RerankerConfig dataclass:
     - model: str = "haiku"
     - max_tokens: int = 1024
     - temperature: float = 0.0
     - timeout_seconds: int = 30
     - max_results_to_rerank: int = 20
     - use_subscription: bool = True  # Claude Code headless, not API
     - always_rerank: bool = True

   - ClaudeReranker class:
     - Accept custom prompt_template (for domain customization)
     - Accept relevance_criteria: Dict[str, str] (domain-specific)
     - is_available() -> bool (check Claude CLI)
     - rerank(query: str, results: List[SearchResult], top_k: int) -> List[SearchResult]

   - Default prompt template should be domain-agnostic
   - Support for domain plugins to override the template

2. Create abstract RerankerProtocol in same file:
   - Allows alternative rerankers (e.g., cross-encoder from Knowledge-Base-MCP)

3. Write tests in:
   packages/docsearch-core/tests/test_reranker.py

   Test cases:
   - Reranker initialization
   - CLI availability check (mock)
   - Reranking logic (mock Claude response)
   - Fallback when CLI unavailable
   - Custom prompt template

Keep the Claude Code headless mode approach (subscription-based, not API credits).
```

---

### Task 1.6: Create Plugin System
```
AGENT_TYPE: Opus
EXECUTION: SEQUENTIAL (after 1.3, 1.4, 1.5)
ESTIMATED_TIME: 30 minutes
DEPENDENCIES: Tasks 1.3, 1.4, 1.5
```

**Prompt for Agent:**
```
You are creating the plugin system for docsearch-core.

This is the most critical component - it defines how domain plugins integrate.

Your task:
1. Create DomainConfig dataclass in:
   packages/docsearch-core/src/docsearch_core/plugins/base.py

   Fields:
   - name: str  # e.g., "stm32"
   - display_name: str  # e.g., "STM32"
   - description: str
   - version: str
   - core_version_requirement: str  # e.g., ">=0.1.0,<1.0.0"
   - package_name: str  # e.g., "docsearch_stm32"
   - markdowns_path: str = "markdowns"
   - agents_path: str = "agents"
   - commands_path: str = "commands"
   - synonyms_file: str = "config/synonyms.yaml"
   - relevance_criteria: Dict[str, str]  # For reranker
   - mcp_tools: List[str]  # Tools this domain exposes

2. Create DomainPlugin abstract base class:

   Abstract methods (domains MUST implement):
   - domain_config() -> DomainConfig
   - get_tokenizer() -> TokenizerProtocol
   - get_synonyms() -> Dict[str, List[str]]
   - get_query_patterns() -> Dict[str, str]  # Regex patterns
   - get_metadata_class() -> Type[ChunkMetadata]

   Concrete methods (domains CAN override):
   - get_rerank_prompt() -> str
   - get_agents_path() -> Path
   - get_commands_path() -> Path
   - get_markdowns_path() -> Path
   - validate() -> List[str]  # Validation errors

3. Create PluginRegistry in:
   packages/docsearch-core/src/docsearch_core/plugins/registry.py

   - Use entry_points for plugin discovery ("docsearch_domains" group)
   - discover_plugins() -> List[str]
   - get_plugin(name: str) -> Optional[DomainPlugin]
   - register_plugin(name: str, plugin: DomainPlugin)
   - list_plugins() -> List[str]

4. Create base ChunkMetadata in:
   packages/docsearch-core/src/docsearch_core/metadata/base.py

   Base fields that all domains share:
   - chunk_id: str
   - source_file: str
   - doc_type: Optional[str]
   - content_type: Optional[str]
   - section: Optional[str]
   - keywords: List[str]
   - has_code: bool
   - custom: Dict[str, Any]  # Domain-specific extensions

5. Write comprehensive tests in:
   packages/docsearch-core/tests/test_plugins.py

   Test cases:
   - Plugin registration
   - Plugin discovery via entry_points (mock)
   - DomainConfig validation
   - Abstract method enforcement
   - Metadata extension

This plugin system should be inspired by the tool organization pattern from Knowledge-Base-MCP.
```

---

### Task 1.7: Create Quality Gates (Stolen from Knowledge-Base-MCP)
```
AGENT_TYPE: Opus
EXECUTION: PARALLEL with Task 1.6
ESTIMATED_TIME: 25 minutes
DEPENDENCIES: Tasks 1.3, 1.4
```

**Prompt for Agent:**
```
You are implementing quality gates for docsearch-core, inspired by Knowledge-Base-MCP's canary QA framework.

Read the audit: docs/audits/knowledge-base-mcp-audit.md

Your task:
1. Create quality metrics in:
   packages/docsearch-core/src/docsearch_core/quality/metrics.py

   Implement:
   - RetrievalMetrics dataclass:
     - recall_at_k: float
     - precision_at_k: float
     - ndcg_at_k: float
     - mrr: float  # Mean Reciprocal Rank
     - latency_ms: float

   - calculate_recall(retrieved: List[str], relevant: List[str], k: int) -> float
   - calculate_precision(retrieved: List[str], relevant: List[str], k: int) -> float
   - calculate_ndcg(retrieved: List[str], relevant: List[str], k: int) -> float
   - calculate_mrr(retrieved: List[str], relevant: List[str]) -> float

2. Create quality gates in:
   packages/docsearch-core/src/docsearch_core/quality/gates.py

   Implement:
   - QualityGateConfig dataclass:
     - min_recall: float = 0.7
     - min_precision: float = 0.5
     - min_ndcg: float = 0.6
     - max_latency_ms: float = 500.0
     - test_queries_file: Optional[Path] = None

   - QualityGate class:
     - __init__(config: QualityGateConfig, retriever: HybridRetriever)
     - run_evaluation(test_cases: List[TestCase]) -> EvaluationResult
     - check_gates() -> Tuple[bool, List[str]]  # (passed, failures)

   - TestCase dataclass:
     - query: str
     - expected_docs: List[str]  # Expected chunk_ids
     - filters: Optional[Dict]

   - EvaluationResult dataclass:
     - metrics: RetrievalMetrics
     - passed: bool
     - failures: List[str]
     - test_cases_run: int

3. Create canary evaluation in:
   packages/docsearch-core/src/docsearch_core/quality/canary.py

   - CanaryEvaluator class:
     - load_test_cases(path: Path) -> List[TestCase]
     - run_canary() -> EvaluationResult
     - generate_report() -> str

4. Write tests in:
   packages/docsearch-core/tests/test_quality.py

This is a key differentiator - most MCP servers don't have quality assurance.
```

---

### Task 1.8: Wire Everything Together
```
AGENT_TYPE: Opus
EXECUTION: SEQUENTIAL (after all Phase 1 tasks)
ESTIMATED_TIME: 20 minutes
DEPENDENCIES: Tasks 1.1-1.7
```

**Prompt for Agent:**
```
You are wiring together all docsearch-core components and ensuring they work together.

Your task:
1. Update packages/docsearch-core/src/docsearch_core/__init__.py

   Export all public APIs:
   - From retrieval: SearchResult, BM25Index, BM25Config, HybridRetriever, HybridRetrieverConfig
   - From storage: ChromaStore, ChromaConfig
   - From ranking: ClaudeReranker, RerankerConfig, RerankerProtocol
   - From tokenization: TokenizerProtocol, BaseTokenizer, DefaultTokenizer
   - From plugins: DomainPlugin, DomainConfig, PluginRegistry, get_plugin
   - From quality: QualityGate, QualityGateConfig, RetrievalMetrics, CanaryEvaluator
   - From metadata: ChunkMetadata

   Set __version__ = "0.1.0"

2. Create a convenience factory in:
   packages/docsearch-core/src/docsearch_core/factory.py

   - create_retriever(plugin: DomainPlugin, config: Dict) -> HybridRetriever
     This should:
     - Initialize ChromaStore with plugin's collection
     - Initialize BM25Index with plugin's tokenizer
     - Initialize HybridRetriever with both
     - Optionally wrap with ClaudeReranker

   - create_quality_gate(plugin: DomainPlugin, retriever: HybridRetriever) -> QualityGate

3. Run all tests:
   cd packages/docsearch-core && pytest tests/ -v

4. Fix any import errors or circular dependencies

5. Create integration test in:
   packages/docsearch-core/tests/test_integration.py

   Test the full pipeline:
   - Create mock plugin
   - Use factory to create retriever
   - Add test documents
   - Run search
   - Verify results

Document any issues encountered for the next phase.
```

---

## Phase 2: Create STM32 Domain Plugin [SEQUENTIAL within phase]

### Task 2.1: Create STM32 Package Structure (Claude Code Plugin Format)
```
AGENT_TYPE: Opus
EXECUTION: SEQUENTIAL (first in Phase 2)
ESTIMATED_TIME: 20 minutes
DEPENDENCIES: Phase 1 complete
```

**Prompt for Agent:**
```
You are creating the STM32 domain plugin package structure following Claude Code plugin architecture.

CRITICAL: This must follow Claude Code's plugin discovery patterns:
- .claude-plugin/plugin.json is REQUIRED for plugin discovery
- agents/ directory is auto-discovered (no copying needed)
- commands/ directory is auto-discovered (no copying needed)
- server/.mcp.json defines the bundled MCP server

Create:
packages/
└── docsearch-stm32/
    ├── .claude-plugin/
    │   └── plugin.json            # REQUIRED: Plugin manifest
    ├── agents/                    # Auto-discovered by Claude Code
    │   ├── stm32-firmware.md
    │   ├── stm32-debug.md
    │   └── ... (all 16 agents)
    ├── commands/                  # Auto-discovered, namespaced as /stm32:*
    │   ├── search.md              # -> /stm32:search
    │   ├── init.md                # -> /stm32:init
    │   ├── hal.md                 # -> /stm32:hal
    │   └── debug.md               # -> /stm32:debug
    ├── server/
    │   └── .mcp.json              # Bundled MCP server config
    ├── pyproject.toml
    ├── README.md
    └── src/
        └── docsearch_stm32/
            ├── __init__.py
            ├── __main__.py
            ├── plugin.py
            ├── tokenization/
            │   ├── __init__.py
            │   └── stm32_tokenizer.py
            ├── expansion/
            │   ├── __init__.py
            │   └── synonyms.py
            ├── parsing/
            │   ├── __init__.py
            │   └── query_parser.py
            ├── metadata/
            │   ├── __init__.py
            │   └── stm32_metadata.py
            ├── config/
            │   ├── __init__.py
            │   ├── stm32_config.yaml
            │   └── synonyms.yaml
            ├── server/
            │   ├── __init__.py
            │   └── mcp_server.py
            └── markdowns/        (bundled documentation)

1. Create .claude-plugin/plugin.json:
   ```json
   {
     "name": "stm32",
     "description": "STM32 microcontroller documentation search with semantic search, code examples, and 16 expert agents",
     "version": "1.0.0",
     "author": {
       "name": "Your Name"
     },
     "repository": "https://github.com/creativec09/stm32",
     "license": "MIT",
     "keywords": ["stm32", "microcontroller", "embedded", "arm", "cortex"]
   }
   ```

2. Create server/.mcp.json:
   ```json
   {
     "mcpServers": {
       "stm32-docs": {
         "command": "python",
         "args": ["-m", "docsearch_stm32"],
         "env": {}
       }
     }
   }
   ```

3. For pyproject.toml:
   - Name: docsearch-stm32
   - Version: 0.1.0
   - Dependency: docsearch-core>=0.1.0
   - Entry point: stm32-mcp-docs = docsearch_stm32.__main__:main
   - Plugin entry point: [project.entry-points."docsearch_domains"]
                         stm32 = "docsearch_stm32.plugin:STM32Plugin"

4. Copy from current repository:
   - mcp_server/agents/ -> packages/docsearch-stm32/agents/
   - .claude/commands/ -> packages/docsearch-stm32/commands/
   - mcp_server/markdowns/ -> packages/docsearch-stm32/src/docsearch_stm32/markdowns/

NOTE: Agents and commands go at PLUGIN ROOT (not in src/), so Claude Code can discover them.
Markdowns go in src/ because they're bundled with the Python package.
```

---

### Task 2.1b: Audit and Fix Agent Frontmatter
```
AGENT_TYPE: Opus
EXECUTION: SEQUENTIAL (after 2.1)
ESTIMATED_TIME: 25 minutes
DEPENDENCIES: Task 2.1
```

**Prompt for Agent:**
```
You are auditing and fixing all 16 STM32 agent files to ensure they comply with Claude Code's required frontmatter format.

REQUIRED FRONTMATTER FIELDS:
- name: REQUIRED - lowercase, hyphens, must match filename (minus .md)
- description: REQUIRED - detailed description for Claude's delegation decision
- tools: OPTIONAL - restrict which tools the agent can use
- model: OPTIONAL - sonnet (default), opus, haiku, or inherit

Read all agent files in:
- packages/docsearch-stm32/agents/ (or mcp_server/agents/ if not yet copied)

For EACH agent file:

1. Check frontmatter exists and has required fields
2. Ensure 'name' matches filename (e.g., stm32-firmware.md -> name: stm32-firmware)
3. Ensure 'description' is detailed enough for Claude to know when to delegate
   BAD:  "Firmware development"
   GOOD: "Expert STM32 firmware developer. Use for implementing peripheral drivers, interrupt handlers, DMA transfers, and HAL/LL library usage. Proactively delegate firmware implementation tasks."
4. Add 'tools' if the agent should be restricted
5. Add 'model' if non-default (most should use sonnet)

Example CORRECT format:
```yaml
---
name: stm32-firmware
description: Expert STM32 firmware developer specializing in HAL/LL libraries. Use for implementing peripheral drivers, interrupt handlers, DMA configurations, and initialization sequences. Proactively use for any firmware code generation or modification tasks.
tools: Read, Grep, Glob, Bash, Edit, Write
model: sonnet
---

You are an expert STM32 firmware developer...
```

Create a report listing:
1. Each agent file
2. Current frontmatter (before)
3. Fixed frontmatter (after)
4. Changes made

Then update all agent files with the corrected frontmatter.

Output: packages/docsearch-stm32/agents/*.md (all 16 files updated)
```

---

### Task 2.1c: Rename Commands for Plugin Namespacing
```
AGENT_TYPE: Opus
EXECUTION: PARALLEL with Task 2.1b
ESTIMATED_TIME: 15 minutes
DEPENDENCIES: Task 2.1
```

**Prompt for Agent:**
```
You are renaming slash command files for Claude Code plugin namespacing.

When commands are in a plugin named "stm32", they become:
- commands/search.md -> /stm32:search
- commands/init.md -> /stm32:init

Current command structure (in .claude/commands/ or mcp_server/commands/):
- stm32.md
- stm32-init.md
- stm32-hal.md
- stm32-debug.md

These need to be renamed to avoid double-nesting:
- stm32.md -> search.md (becomes /stm32:search)
- stm32-init.md -> init.md (becomes /stm32:init)
- stm32-hal.md -> hal.md (becomes /stm32:hal)
- stm32-debug.md -> debug.md (becomes /stm32:debug)

Your task:
1. Copy command files to packages/docsearch-stm32/commands/
2. Rename them to short names (without stm32- prefix)
3. Update any internal references to the command names
4. Ensure $ARGUMENTS handling still works

Output: packages/docsearch-stm32/commands/*.md (renamed files)
```

---

### Task 2.2: Migrate STM32 Tokenizer
```
AGENT_TYPE: Opus
EXECUTION: PARALLEL with Tasks 2.3, 2.4, 2.5 (after 2.1b, 2.1c complete)
ESTIMATED_TIME: 20 minutes
DEPENDENCIES: Task 2.1
```

**Prompt for Agent:**
```
You are migrating the STM32-specific tokenizer to the new plugin structure.

Read our current implementation:
- storage/bm25_index.py (STM32Tokenizer class and PRESERVE_PATTERNS)

Your task:
1. Create STM32Tokenizer in:
   packages/docsearch-stm32/src/docsearch_stm32/tokenization/stm32_tokenizer.py

   Requirements:
   - Extend BaseTokenizer from docsearch_core
   - Keep all STM32-specific patterns:
     - HAL_[A-Z][A-Za-z0-9_]+
     - LL_[A-Z][A-Za-z0-9_]+
     - STM32[A-Z][0-9]+[A-Za-z0-9]*
     - [A-Z]+[0-9]*_[A-Z]+[0-9]* (registers)
     - __HAL_RCC patterns
   - Keep STM32_STOPWORDS
   - Implement tokenize() using parent's filter_tokens()

2. Write tests in:
   packages/docsearch-stm32/tests/test_tokenizer.py

   Test cases:
   - HAL function preservation: "HAL_GPIO_Init" stays intact
   - LL function preservation: "LL_USART_Enable" stays intact
   - Register preservation: "GPIOx_MODER" stays intact
   - STM32 family preservation: "STM32H7" stays intact
   - Normal word tokenization still works

Ensure backward compatibility - the tokenizer should produce identical output to the current one.
```

---

### Task 2.3: Migrate Query Expansion
```
AGENT_TYPE: Opus
EXECUTION: PARALLEL with Task 2.2
ESTIMATED_TIME: 15 minutes
DEPENDENCIES: Task 2.1
```

**Prompt for Agent:**
```
You are migrating STM32 query expansion to the new plugin structure.

Read our current implementation:
- mcp_server/query_expansion.py (172 synonym mappings)

Your task:
1. Create synonyms.yaml in:
   packages/docsearch-stm32/src/docsearch_stm32/config/synonyms.yaml

   Convert STM32_SYNONYMS dict to YAML format:
   ```yaml
   uart:
     - usart
     - serial
     - rs232
   i2c:
     - iic
     - twi
     - two-wire
   # ... all 172 mappings
   ```

2. Create synonym loader in:
   packages/docsearch-stm32/src/docsearch_stm32/expansion/synonyms.py

   - load_synonyms(path: Path) -> Dict[str, Set[str]]
   - expand_query(query: str, synonyms: Dict) -> str

   Keep the same expansion logic from current query_expansion.py

3. Write tests in:
   packages/docsearch-stm32/tests/test_expansion.py

   Test cases:
   - "uart configuration" expands to include "usart", "serial"
   - "i2c setup" expands to include "iic", "twi"
   - Case insensitivity
   - No double-expansion

Verify all 172 synonyms are preserved in the YAML file.
```

---

### Task 2.4: Migrate Query Parser
```
AGENT_TYPE: Opus
EXECUTION: PARALLEL with Tasks 2.2, 2.3
ESTIMATED_TIME: 20 minutes
DEPENDENCIES: Task 2.1
```

**Prompt for Agent:**
```
You are migrating the STM32 query parser to the new plugin structure.

Read our current implementation:
- mcp_server/query_parser.py

Your task:
1. Create query parser in:
   packages/docsearch-stm32/src/docsearch_stm32/parsing/query_parser.py

   Keep:
   - ParsedQuery dataclass with all fields
   - HAL function detection patterns
   - LL function detection patterns
   - Register detection (GPIOx_MODER, etc.)
   - STM32 family detection (STM32F4, STM32H7, etc.)
   - Peripheral extraction
   - Intent detection (code request, troubleshooting, etc.)

   The QueryParser class should:
   - parse(query: str) -> ParsedQuery
   - Be usable by the plugin's get_query_patterns() method

2. Write tests in:
   packages/docsearch-stm32/tests/test_parser.py

   Test cases:
   - "How to use HAL_UART_Transmit" -> detects HAL function
   - "Configure GPIOx_MODER register" -> detects register
   - "STM32H7 DMA setup" -> detects family and peripheral
   - "Why is my UART not working" -> detects troubleshooting intent
   - Edge cases with mixed queries

Ensure all regex patterns from current implementation are preserved.
```

---

### Task 2.5: Migrate STM32 Metadata
```
AGENT_TYPE: Opus
EXECUTION: PARALLEL with Tasks 2.2, 2.3, 2.4
ESTIMATED_TIME: 15 minutes
DEPENDENCIES: Task 2.1
```

**Prompt for Agent:**
```
You are migrating STM32-specific metadata schemas to the new plugin structure.

Read our current implementation:
- storage/metadata.py

Your task:
1. Create STM32 metadata in:
   packages/docsearch-stm32/src/docsearch_stm32/metadata/stm32_metadata.py

   Create:
   - STM32Peripheral enum (GPIO, UART, SPI, I2C, ADC, TIM, DMA, etc.)
   - STM32DocType enum (reference_manual, datasheet, application_note, etc.)
   - STM32ContentType enum (conceptual, code_example, register_description, etc.)
   - STM32ChunkMetadata class extending ChunkMetadata from core
     Additional fields:
     - peripheral: Optional[STM32Peripheral]
     - stm32_family: Optional[str]
     - hal_functions: List[str]
     - registers: List[str]
     - library_type: Optional[str]  # HAL, LL, CMSIS

2. Write tests in:
   packages/docsearch-stm32/tests/test_metadata.py

   Test cases:
   - Enum value validation
   - Metadata serialization to dict
   - Metadata deserialization from dict
   - Extension of base ChunkMetadata

All enums should match current implementation exactly for backward compatibility.
```

---

### Task 2.6: Implement STM32Plugin Class
```
AGENT_TYPE: Opus
EXECUTION: SEQUENTIAL (after 2.2, 2.3, 2.4, 2.5)
ESTIMATED_TIME: 25 minutes
DEPENDENCIES: Tasks 2.2, 2.3, 2.4, 2.5
```

**Prompt for Agent:**
```
You are implementing the main STM32Plugin class that ties everything together.

Your task:
1. Implement STM32Plugin in:
   packages/docsearch-stm32/src/docsearch_stm32/plugin.py

   ```python
   from docsearch_core.plugins.base import DomainPlugin, DomainConfig

   class STM32Plugin(DomainPlugin):
       VERSION = "0.1.0"
       CORE_VERSION = ">=0.1.0,<1.0.0"

       @property
       def domain_config(self) -> DomainConfig:
           return DomainConfig(
               name="stm32",
               display_name="STM32",
               description="STM32 microcontroller documentation search",
               version=self.VERSION,
               core_version_requirement=self.CORE_VERSION,
               package_name="docsearch_stm32",
               relevance_criteria={
                   "Peripheral match": "Result covers the specific peripheral mentioned",
                   "Code completeness": "Code examples are complete and runnable",
                   "HAL/LL accuracy": "Uses correct HAL or LL library as context requires",
                   "Family compatibility": "Compatible with mentioned STM32 family",
                   "Register accuracy": "Register descriptions match query context",
               },
               mcp_tools=[
                   "search_stm32_docs",
                   "get_peripheral_docs",
                   "get_code_examples",
                   "get_register_info",
                   "lookup_hal_function",
                   "troubleshoot_error",
                   "get_init_sequence",
                   "get_clock_config",
                   # ... all 15+ tools
               ],
           )

       def get_tokenizer(self) -> TokenizerProtocol:
           # Return STM32Tokenizer

       def get_synonyms(self) -> Dict[str, List[str]]:
           # Load from config/synonyms.yaml

       def get_query_patterns(self) -> Dict[str, str]:
           # Return patterns from query_parser

       def get_metadata_class(self) -> Type[ChunkMetadata]:
           return STM32ChunkMetadata
   ```

2. Write tests in:
   packages/docsearch-stm32/tests/test_plugin.py

   Test cases:
   - Plugin instantiation
   - domain_config validation
   - get_tokenizer returns STM32Tokenizer
   - get_synonyms loads all 172 synonyms
   - validate() returns no errors
   - Plugin discovery via entry_points

3. Verify plugin works with core:
   ```python
   from docsearch_core.plugins.registry import get_plugin
   plugin = get_plugin("stm32")
   assert plugin is not None
   ```
```

---

### Task 2.7: Migrate MCP Server
```
AGENT_TYPE: Opus
EXECUTION: SEQUENTIAL (after 2.6)
ESTIMATED_TIME: 30 minutes
DEPENDENCIES: Task 2.6
```

**Prompt for Agent:**
```
You are migrating the MCP server to use the new plugin architecture.

Read our current implementation:
- mcp_server/server.py

Your task:
1. Create new MCP server in:
   packages/docsearch-stm32/src/docsearch_stm32/server/mcp_server.py

   Requirements:
   - Use STM32Plugin for all domain-specific behavior
   - Use docsearch_core factory for retriever setup
   - Keep all 15+ tools with same signatures
   - Keep all 4 resources (stm32://status, etc.)
   - Use plugin's rerank prompt template

   Structure:
   ```python
   from mcp.server import Server
   from docsearch_core import create_retriever, ClaudeReranker
   from docsearch_stm32.plugin import STM32Plugin

   server = Server("stm32-docs")
   plugin = STM32Plugin()
   retriever = None  # Lazy init

   @server.list_tools()
   async def list_tools():
       # Generate from plugin.domain_config.mcp_tools

   @server.call_tool()
   async def call_tool(name: str, arguments: dict):
       # Route to appropriate handler
   ```

2. Create entry point in:
   packages/docsearch-stm32/src/docsearch_stm32/__main__.py

   ```python
   from .server.mcp_server import main

   if __name__ == "__main__":
       main()
   ```

3. Keep backward compatibility:
   - Same tool names
   - Same parameter schemas
   - Same response formats

4. Write integration test in:
   packages/docsearch-stm32/tests/test_mcp_server.py

   Test (with mocked retriever):
   - Tool listing
   - search_stm32_docs call
   - get_peripheral_docs call
   - Resource access

The server should work identically to the current one from a user perspective.
```

---

### Task 2.8: Create First-Run Initialization (Database Only)
```
AGENT_TYPE: Opus
EXECUTION: PARALLEL with Task 2.7
ESTIMATED_TIME: 20 minutes
DEPENDENCIES: Task 2.6
```

**Prompt for Agent:**
```
You are creating the first-run initialization system for docsearch-stm32.

CRITICAL: Per Claude Code plugin architecture:
- Agents are AUTO-DISCOVERED from plugin's agents/ directory
- Commands are AUTO-DISCOVERED from plugin's commands/ directory
- DO NOT copy agents or commands to ~/.claude/agents/ or ~/.claude/commands/
- First-run init ONLY needs to build the vector database

This handles ONLY:
- Building the vector database from bundled markdowns
- Creating the BM25 index
- Database versioning for updates

Read our current implementation:
- mcp_server/ingestion.py

Your task:
1. Create initialization module in:
   packages/docsearch-stm32/src/docsearch_stm32/init.py

   ```python
   class STM32Initializer:
       def __init__(self, plugin: STM32Plugin):
           self.plugin = plugin
           self.data_dir = Path.home() / ".docsearch" / "stm32"
           self.db_version_file = self.data_dir / ".db_version"
           self.current_version = "1.0.0"  # Increment when docs change

       def needs_initialization(self) -> bool:
           """Check if database needs to be built or updated."""
           if not self.db_version_file.exists():
               return True
           stored_version = self.db_version_file.read_text().strip()
           return stored_version != self.current_version

       def initialize(self, force: bool = False) -> None:
           if not force and not self.needs_initialization():
               return

           self._build_database()
           self._save_version()

       # NOTE: No _install_agents() or _install_commands()
       # Claude Code auto-discovers these from plugin directory

       def _build_database(self) -> None:
           # Use create_retriever to build ChromaDB + BM25
           # Process all markdowns from plugin.get_markdowns_path()
           pass

       def _save_version(self) -> None:
           self.data_dir.mkdir(parents=True, exist_ok=True)
           self.db_version_file.write_text(self.current_version)
   ```

2. Integrate with MCP server startup in __main__.py:
   ```python
   def main():
       initializer = STM32Initializer(plugin)
       if initializer.needs_initialization():
           print("[stm32-docs] Building documentation database...")
           initializer.initialize()

       # Start MCP server
   ```

3. Steal the deterministic ingestion pattern from Knowledge-Base-MCP:
   - Track file hashes to detect changes
   - Only re-index changed files
   - Store ingestion metadata

4. Write tests for initialization logic (with mocked filesystem)

IMPORTANT: Remove any logic that copies agents or commands. Claude Code
discovers these automatically from the plugin's agents/ and commands/
directories when the plugin is installed.
```

---

## Phase 3: Validation & Quality [PARALLEL tasks]

### Task 3.1: End-to-End Testing
```
AGENT_TYPE: Opus
EXECUTION: PARALLEL (start of Phase 3)
ESTIMATED_TIME: 30 minutes
DEPENDENCIES: Phase 2 complete
```

**Prompt for Agent:**
```
You are creating comprehensive end-to-end tests for the new architecture.

Your task:
1. Create test suite in:
   packages/docsearch-stm32/tests/e2e/

   Tests:
   a) test_full_pipeline.py
      - Initialize plugin
      - Build database from test markdowns
      - Run searches
      - Verify results quality

   b) test_mcp_integration.py
      - Start MCP server (subprocess)
      - Send tool requests
      - Verify responses

   c) test_backward_compatibility.py
      - Compare new search results to baseline
      - Ensure no regressions in search quality

2. Create test fixtures:
   - Sample markdown documents
   - Expected search results (ground truth)
   - Test queries with known answers

3. Create quality baseline:
   - Run current implementation on test queries
   - Save results as baseline
   - New implementation must match or exceed

4. Run all tests and document results

Any failures should be documented with clear reproduction steps.
```

---

### Task 3.2: Performance Benchmarking
```
AGENT_TYPE: Opus
EXECUTION: PARALLEL with Task 3.1
ESTIMATED_TIME: 25 minutes
DEPENDENCIES: Phase 2 complete
```

**Prompt for Agent:**
```
You are creating performance benchmarks for the new architecture.

Target metrics (inspired by RAG-CLI):
- Vector search: <100ms
- BM25 search: <50ms
- Hybrid search: <200ms
- Full pipeline with rerank: <5 seconds

Your task:
1. Create benchmark suite in:
   packages/docsearch-stm32/tests/benchmarks/

   a) bench_bm25.py
      - Index 1000 documents
      - Run 100 searches
      - Measure p50, p95, p99 latency

   b) bench_vector.py
      - Same with vector search

   c) bench_hybrid.py
      - Same with hybrid search

   d) bench_full_pipeline.py
      - Include reranking
      - Measure end-to-end latency

2. Create performance regression test:
   - Store baseline metrics
   - CI should fail if metrics regress >20%

3. Profile memory usage:
   - Peak memory during indexing
   - Steady-state memory
   - Memory per 1000 documents

4. Document optimization opportunities

Use pytest-benchmark for measurements.
```

---

### Task 3.3: Quality Gates Validation
```
AGENT_TYPE: Opus
EXECUTION: PARALLEL with Tasks 3.1, 3.2
ESTIMATED_TIME: 25 minutes
DEPENDENCIES: Phase 2 complete
```

**Prompt for Agent:**
```
You are validating the quality gates system with real STM32 test cases.

Your task:
1. Create STM32 test cases in:
   packages/docsearch-stm32/tests/quality/stm32_test_cases.yaml

   Format:
   ```yaml
   test_cases:
     - query: "How to configure UART with DMA"
       expected_docs:
         - "uart_dma_guide_chunk_3"
         - "dma_configuration_chunk_1"
       filters:
         peripheral: UART

     - query: "HAL_GPIO_Init parameters"
       expected_docs:
         - "gpio_hal_reference_chunk_7"
       filters:
         has_code: true

     # Add 20+ test cases covering:
     # - Different peripherals
     # - HAL vs LL queries
     # - Register lookups
     # - Troubleshooting queries
     # - Code example requests
   ```

2. Run quality gates:
   ```python
   from docsearch_core.quality import QualityGate, CanaryEvaluator
   from docsearch_stm32 import STM32Plugin

   plugin = STM32Plugin()
   retriever = create_retriever(plugin)
   gate = QualityGate(config, retriever)

   results = gate.run_evaluation(test_cases)
   print(results.metrics)
   assert results.passed
   ```

3. Document baseline metrics:
   - Current recall@5
   - Current precision@5
   - Current nDCG@5
   - Current MRR

4. Set thresholds in config:
   - min_recall: based on baseline - 5%
   - min_precision: based on baseline - 5%

These become our regression tests.
```

---

## Phase 4: Documentation & Release [SEQUENTIAL]

### Task 4.1: Update All Documentation
```
AGENT_TYPE: Opus
EXECUTION: SEQUENTIAL (first in Phase 4)
ESTIMATED_TIME: 30 minutes
DEPENDENCIES: Phase 3 complete
```

**Prompt for Agent:**
```
You are updating all documentation for the new architecture.

Your task:
1. Update CLAUDE.md in repository root:
   - New installation command using docsearch-stm32
   - Updated architecture description
   - New package structure
   - Plugin system documentation
   - Keep all existing tool/agent documentation

2. Update docs/UNIVERSAL_PLATFORM_PLAN.md:
   - Mark completed items
   - Update based on actual implementation
   - Add lessons learned

3. Create packages/docsearch-core/README.md:
   - What is docsearch-core
   - Installation
   - Creating a domain plugin
   - API overview

4. Create packages/docsearch-stm32/README.md:
   - What is docsearch-stm32
   - Installation (one-liner)
   - Available tools
   - Available agents
   - Configuration

5. Update root README.md:
   - Mention universal platform
   - Link to domain-specific READMEs

All documentation should be clear enough for a new user to get started.
```

---

### Task 4.2: Prepare Release
```
AGENT_TYPE: Opus
EXECUTION: SEQUENTIAL (after 4.1)
ESTIMATED_TIME: 20 minutes
DEPENDENCIES: Task 4.1
```

**Prompt for Agent:**
```
You are preparing the packages for release.

Your task:
1. Verify package metadata:
   - docsearch-core/pyproject.toml
   - docsearch-stm32/pyproject.toml
   - Correct versions
   - Correct dependencies
   - Correct entry points

2. Create CHANGELOG.md for each package:
   - docsearch-core/CHANGELOG.md
   - docsearch-stm32/CHANGELOG.md

   Format:
   ```markdown
   # Changelog

   ## [0.1.0] - 2026-01-XX

   ### Added
   - Initial release
   - Hybrid search (BM25 + vector)
   - Plugin system for domain support
   - Quality gates framework
   - Claude Haiku reranking
   ```

3. Test package builds:
   ```bash
   cd packages/docsearch-core && python -m build
   cd packages/docsearch-stm32 && python -m build
   ```

4. Test local installation:
   ```bash
   pip install packages/docsearch-core/dist/*.whl
   pip install packages/docsearch-stm32/dist/*.whl
   stm32-mcp-docs  # Should start
   ```

5. Verify Claude Code integration:
   ```bash
   claude mcp add stm32-test -- python -m docsearch_stm32
   # Test a search
   ```

6. Create GitHub release notes draft

Document any issues for final resolution.
```

---

## Execution Summary

### Phase Dependencies

```
Phase 0 (Audit)          ──────────────────────────────────────────┐
  Task 0.1 ─┬─ [PARALLEL]                                         │
  Task 0.2 ─┤                                                     │
  Task 0.3 ─┘                                                     │
       │                                                          │
       ▼                                                          │
  Task 0.4 ── [SEQUENTIAL - needs 0.1, 0.2, 0.3]                  │
       │                                                          │
       ▼                                                          │
Phase 1 (Core) ───────────────────────────────────────────────────┤
  Task 1.1 ── [SEQUENTIAL - first]                                │
       │                                                          │
       ▼                                                          │
  Task 1.2 ── [SEQUENTIAL - needs 1.1]                            │
       │                                                          │
       ▼                                                          │
  Task 1.3 ─┬─ [PARALLEL]                                         │
  Task 1.4 ─┤                                                     │
  Task 1.5 ─┘                                                     │
       │                                                          │
       ▼                                                          │
  Task 1.6 ─┬─ [PARALLEL - needs 1.3, 1.4, 1.5]                   │
  Task 1.7 ─┘                                                     │
       │                                                          │
       ▼                                                          │
  Task 1.8 ── [SEQUENTIAL - needs all Phase 1]                    │
       │                                                          │
       ▼                                                          │
Phase 2 (STM32 Plugin) ───────────────────────────────────────────┤
  Task 2.1  ── [SEQUENTIAL - first: package + plugin manifest]    │
       │                                                          │
       ▼                                                          │
  Task 2.1b ─┬─ [PARALLEL - agent frontmatter audit]              │
  Task 2.1c ─┘   [PARALLEL - command renaming]                    │
       │                                                          │
       ▼                                                          │
  Task 2.2 ─┬─ [PARALLEL - after 2.1b, 2.1c]                      │
  Task 2.3 ─┤                                                     │
  Task 2.4 ─┤                                                     │
  Task 2.5 ─┘                                                     │
       │                                                          │
       ▼                                                          │
  Task 2.6 ── [SEQUENTIAL - needs 2.2-2.5]                        │
       │                                                          │
       ▼                                                          │
  Task 2.7 ─┬─ [PARALLEL]                                         │
  Task 2.8 ─┘   (DB init only - no agent copying!)                │
       │                                                          │
       ▼                                                          │
Phase 3 (Validation) ─────────────────────────────────────────────┤
  Task 3.1 ─┬─ [PARALLEL]                                         │
  Task 3.2 ─┤                                                     │
  Task 3.3 ─┘                                                     │
       │                                                          │
       ▼                                                          │
Phase 4 (Release) ────────────────────────────────────────────────┘
  Task 4.1 ── [SEQUENTIAL]
       │
       ▼
  Task 4.2 ── [SEQUENTIAL]
```

### Task Count by Phase

| Phase | Total Tasks | Parallel Groups | Sequential |
|-------|-------------|-----------------|------------|
| 0: Audit | 4 | 1 (3 tasks) | 1 |
| 1: Core | 8 | 2 (5 tasks) | 3 |
| 2: STM32 | 10 | 3 (8 tasks) | 2 |
| 3: Validation | 3 | 1 (3 tasks) | 0 |
| 4: Release | 2 | 0 | 2 |
| **Total** | **27** | **7 groups** | **8 tasks** |

### Estimated Timeline

With parallel execution:
- Phase 0: ~1 hour (3 parallel audits + synthesis)
- Phase 1: ~2 hours (with parallel task groups)
- Phase 2: ~2.5 hours (with parallel task groups, +2 new tasks)
- Phase 3: ~45 minutes (all parallel)
- Phase 4: ~1 hour (sequential)

**Total: ~7.5 hours of agent time** (can be run over multiple sessions)

---

## How to Execute This Plan

### Option A: Manual Execution
Copy each task's prompt and run with:
```bash
claude -p "$(cat task_prompt.txt)"
```

### Option B: Orchestrated Execution
```python
# orchestrator.py
tasks = load_tasks("EXECUTION_PLAN.md")

for phase in tasks.phases:
    parallel_groups = phase.get_parallel_groups()

    for group in parallel_groups:
        # Run all tasks in group simultaneously
        results = await asyncio.gather(*[
            run_agent(task.prompt, model="opus")
            for task in group
        ])

        # Verify all succeeded before next group
        assert all(r.success for r in results)
```

### Option C: Claude Code with Task Tool
Run parallel tasks using multiple Task tool invocations in a single message.
