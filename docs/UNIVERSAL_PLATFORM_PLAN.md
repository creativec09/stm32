# Universal Documentation Search Platform

## Comprehensive Implementation Plan

**Status**: Planning Phase
**Created**: 2026-01-09
**Target**: Transform STM32 MCP documentation server into a universal, multi-domain documentation search platform

---

## Table of Contents

1. [Architecture Overview](#1-architecture-overview)
2. [Package Structure](#2-package-structure)
3. [Core Components](#3-core-components)
4. [Domain Plugin System](#4-domain-plugin-system)
5. [Claude Code Integration](#5-claude-code-integration)
6. [Configuration System](#6-configuration-system)
7. [Syncing Strategy](#7-syncing-strategy)
8. [Development Workflow](#8-development-workflow)
9. [Migration Path](#9-migration-path)
10. [Example: Adding Arduino Domain](#10-example-adding-new-domain-arduino)
11. [Distribution & Deployment](#11-distribution--deployment)
12. [Documentation Requirements](#12-documentation-requirements)

---

## 1. Architecture Overview

### 1.1 High-Level System Diagram

```
┌─────────────────────────────────────────────────────────────────────────────────┐
│                           DOCSEARCH UNIVERSAL PLATFORM                          │
│                                                                                  │
│  ┌─────────────────────────────────────────────────────────────────────────┐    │
│  │                         Claude Code Integration                          │    │
│  │  ┌───────────────┐  ┌───────────────┐  ┌───────────────┐                │    │
│  │  │ MCP Server    │  │ MCP Server    │  │ MCP Server    │    ...         │    │
│  │  │ (STM32)       │  │ (Arduino)     │  │ (AWS)         │                │    │
│  │  └───────┬───────┘  └───────┬───────┘  └───────┬───────┘                │    │
│  │          │                  │                  │                         │    │
│  │  ┌───────┴───────┐  ┌───────┴───────┐  ┌───────┴───────┐                │    │
│  │  │ Agents (16)   │  │ Agents (12)   │  │ Agents (20)   │                │    │
│  │  │ Commands (4)  │  │ Commands (4)  │  │ Commands (6)  │                │    │
│  │  └───────────────┘  └───────────────┘  └───────────────┘                │    │
│  └─────────────────────────────────────────────────────────────────────────┘    │
│                                      │                                           │
│                                      ▼                                           │
│  ┌─────────────────────────────────────────────────────────────────────────┐    │
│  │                        Domain Plugin Layer                               │    │
│  │  ┌───────────────┐  ┌───────────────┐  ┌───────────────┐                │    │
│  │  │ docsearch-    │  │ docsearch-    │  │ docsearch-    │                │    │
│  │  │ stm32         │  │ arduino       │  │ aws           │    ...         │    │
│  │  │               │  │               │  │               │                │    │
│  │  │ - Tokenizer   │  │ - Tokenizer   │  │ - Tokenizer   │                │    │
│  │  │ - Synonyms    │  │ - Synonyms    │  │ - Synonyms    │                │    │
│  │  │ - Patterns    │  │ - Patterns    │  │ - Patterns    │                │    │
│  │  │ - Metadata    │  │ - Metadata    │  │ - Metadata    │                │    │
│  │  │ - Rerank Tmpl │  │ - Rerank Tmpl │  │ - Rerank Tmpl │                │    │
│  │  └───────┬───────┘  └───────┬───────┘  └───────┬───────┘                │    │
│  └──────────┼──────────────────┼──────────────────┼────────────────────────┘    │
│             │                  │                  │                              │
│             └──────────────────┴──────────────────┘                              │
│                                │                                                 │
│                                ▼                                                 │
│  ┌─────────────────────────────────────────────────────────────────────────┐    │
│  │                          Core Library                                    │    │
│  │                       (docsearch-core)                                   │    │
│  │                                                                          │    │
│  │  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐     │    │
│  │  │ Hybrid      │  │ BM25 Index  │  │ Chroma      │  │ Claude      │     │    │
│  │  │ Retriever   │  │             │  │ Store       │  │ Reranker    │     │    │
│  │  └─────────────┘  └─────────────┘  └─────────────┘  └─────────────┘     │    │
│  │                                                                          │    │
│  │  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐     │    │
│  │  │ Base        │  │ Config      │  │ Plugin      │  │ Query       │     │    │
│  │  │ Tokenizer   │  │ System      │  │ Registry    │  │ Expansion   │     │    │
│  │  └─────────────┘  └─────────────┘  └─────────────┘  └─────────────┘     │    │
│  │                                                                          │    │
│  └─────────────────────────────────────────────────────────────────────────┘    │
│                                                                                  │
│  ┌─────────────────────────────────────────────────────────────────────────┐    │
│  │                           Storage Layer                                  │    │
│  │  ┌───────────────────────────────┐  ┌───────────────────────────────┐   │    │
│  │  │ ChromaDB (Vector Store)       │  │ BM25 Index (Keyword Store)    │   │    │
│  │  │ ~/.docsearch/{domain}/chroma  │  │ ~/.docsearch/{domain}/bm25    │   │    │
│  │  └───────────────────────────────┘  └───────────────────────────────┘   │    │
│  └─────────────────────────────────────────────────────────────────────────┘    │
│                                                                                  │
└─────────────────────────────────────────────────────────────────────────────────┘
```

### 1.2 Core and Domain Plugin Interaction

```
┌─────────────────────────────────────────────────────────────────────────────────┐
│                        PLUGIN INTERACTION FLOW                                   │
│                                                                                  │
│  User Query: "How to configure UART with DMA on STM32H7"                        │
│                                                                                  │
│  ┌─────────────────────────────────────────────────────────────────────────┐    │
│  │ 1. MCP Server receives query                                             │    │
│  │    └── search_stm32_docs("How to configure UART with DMA on STM32H7")   │    │
│  └─────────────────────────────────────────────────────────────────────────┘    │
│                                      │                                           │
│                                      ▼                                           │
│  ┌─────────────────────────────────────────────────────────────────────────┐    │
│  │ 2. Domain Plugin (STM32) provides:                                       │    │
│  │    ├── Tokenizer: STM32Tokenizer.tokenize() → preserves "STM32H7"       │    │
│  │    ├── Synonyms: "UART" → ["USART", "serial", "rs232"]                  │    │
│  │    ├── Patterns: detects peripheral=UART, family=STM32H7                │    │
│  │    └── Metadata: filters by peripheral and family                       │    │
│  └─────────────────────────────────────────────────────────────────────────┘    │
│                                      │                                           │
│                                      ▼                                           │
│  ┌─────────────────────────────────────────────────────────────────────────┐    │
│  │ 3. Core Library executes search:                                         │    │
│  │    ├── HybridRetriever.search()                                         │    │
│  │    │   ├── BM25: keyword match with tokenizer                           │    │
│  │    │   ├── Semantic: vector similarity search                           │    │
│  │    │   └── RRF: fuse results                                            │    │
│  │    └── ClaudeReranker.rerank() using domain's prompt template           │    │
│  └─────────────────────────────────────────────────────────────────────────┘    │
│                                      │                                           │
│                                      ▼                                           │
│  ┌─────────────────────────────────────────────────────────────────────────┐    │
│  │ 4. Return ranked results with STM32-specific metadata                    │    │
│  └─────────────────────────────────────────────────────────────────────────┘    │
│                                                                                  │
└─────────────────────────────────────────────────────────────────────────────────┘
```

---

## 2. Package Structure

### 2.1 Monorepo Structure (Recommended)

```
docsearch/
├── README.md
├── pyproject.toml                    # Workspace configuration
├── .github/
│   └── workflows/
│       ├── ci.yaml                   # Continuous integration
│       ├── release-core.yaml         # Core package release
│       └── release-domain.yaml       # Domain package release
│
├── packages/
│   ├── docsearch-core/               # Core library
│   │   ├── pyproject.toml
│   │   ├── README.md
│   │   └── src/
│   │       └── docsearch_core/
│   │           ├── __init__.py
│   │           ├── retrieval/
│   │           │   ├── __init__.py
│   │           │   ├── hybrid.py     # HybridRetriever
│   │           │   └── bm25.py       # BM25Index
│   │           ├── storage/
│   │           │   ├── __init__.py
│   │           │   └── chroma_store.py
│   │           ├── ranking/
│   │           │   ├── __init__.py
│   │           │   └── reranker.py   # ClaudeReranker
│   │           ├── tokenization/
│   │           │   ├── __init__.py
│   │           │   ├── base.py       # BaseTokenizer
│   │           │   └── default.py    # DefaultTokenizer
│   │           ├── expansion/
│   │           │   ├── __init__.py
│   │           │   └── synonyms.py   # SynonymExpander
│   │           ├── plugins/
│   │           │   ├── __init__.py
│   │           │   ├── base.py       # DomainPlugin base class
│   │           │   └── registry.py   # Plugin discovery
│   │           ├── config/
│   │           │   ├── __init__.py
│   │           │   ├── settings.py   # Configuration management
│   │           │   └── schema.py     # Config validation
│   │           └── metadata/
│   │               ├── __init__.py
│   │               └── base.py       # Base metadata schemas
│   │
│   ├── docsearch-stm32/              # STM32 domain plugin
│   │   ├── pyproject.toml
│   │   ├── README.md
│   │   └── src/
│   │       └── docsearch_stm32/
│   │           ├── __init__.py
│   │           ├── __main__.py       # Entry point
│   │           ├── plugin.py         # STM32Plugin implementation
│   │           ├── tokenization/
│   │           │   └── stm32_tokenizer.py
│   │           ├── config/
│   │           │   ├── stm32_config.yaml
│   │           │   ├── synonyms.yaml
│   │           │   └── patterns.yaml
│   │           ├── metadata/
│   │           │   └── stm32_metadata.py
│   │           ├── server/
│   │           │   └── mcp_server.py
│   │           ├── agents/           # 16 STM32 agents
│   │           │   ├── stm32-router.md
│   │           │   ├── stm32-firmware.md
│   │           │   └── ...
│   │           ├── commands/         # Slash commands
│   │           │   ├── stm32.md
│   │           │   └── stm32-init.md
│   │           └── markdowns/        # 80 bundled docs
│   │               ├── gpio_guide.md
│   │               └── ...
│   │
│   ├── docsearch-arduino/            # Arduino domain plugin
│   │   └── ...
│   │
│   └── docsearch-aws/                # AWS domain plugin
│       └── ...
│
├── docs/                             # Documentation
│   ├── getting-started/
│   ├── domains/
│   ├── development/
│   └── api/
│
├── scripts/
│   ├── create-domain.py              # Domain scaffolding
│   ├── sync-core.py                  # Sync core to domains
│   └── release.py                    # Release automation
│
└── tests/
    └── integration/                  # Cross-package tests
```

### 2.2 Naming Conventions

| Component | Convention | Example |
|-----------|------------|---------|
| Core package | `docsearch-core` | `docsearch-core` |
| Domain package | `docsearch-{domain}` | `docsearch-stm32` |
| Python module | `docsearch_{domain}` | `docsearch_stm32` |
| MCP server command | `{domain}-mcp-docs` | `stm32-mcp-docs` |
| Agent files | `{domain}-{role}.md` | `stm32-firmware.md` |
| Command files | `{domain}[-action].md` | `stm32-init.md` |
| Config files | `{domain}_config.yaml` | `stm32_config.yaml` |

---

## 3. Core Components

### 3.1 HybridRetriever with Pluggable Tokenizer

```python
# packages/docsearch-core/src/docsearch_core/retrieval/hybrid.py

from typing import List, Optional, Protocol, Dict, Any
from dataclasses import dataclass, field


class TokenizerProtocol(Protocol):
    """Protocol for pluggable tokenizers."""

    def tokenize(self, text: str) -> List[str]:
        """Tokenize text into a list of tokens."""
        ...


@dataclass
class HybridRetrieverConfig:
    """Configuration for hybrid retrieval."""

    # Weights for combining results
    bm25_weight: float = 0.4
    semantic_weight: float = 0.6

    # Number of candidates to retrieve from each source
    bm25_k: int = 50
    semantic_k: int = 50

    # Final number of results to return
    final_k: int = 20

    # RRF fusion parameter
    rrf_k: int = 60

    # Fusion method: "rrf", "linear", "max"
    fusion_method: str = "rrf"

    # Query expansion
    enable_query_expansion: bool = True

    # Minimum score threshold
    min_score_threshold: float = 0.0


@dataclass
class SearchResult:
    """A single search result."""

    chunk_id: str
    content: str
    score: float
    metadata: Dict[str, Any] = field(default_factory=dict)
    source: str = "hybrid"  # "bm25", "semantic", or "hybrid"
    rank: int = 0


class HybridRetriever:
    """
    Hybrid retriever combining BM25 and semantic search.

    Uses Reciprocal Rank Fusion (RRF) to combine results from
    keyword-based BM25 search and vector-based semantic search.
    """

    def __init__(
        self,
        bm25_index: "BM25Index",
        semantic_searcher: "SemanticSearcher",
        tokenizer: TokenizerProtocol,
        config: Optional[HybridRetrieverConfig] = None,
        query_expander: Optional[callable] = None,
    ):
        self.bm25_index = bm25_index
        self.semantic_searcher = semantic_searcher
        self.tokenizer = tokenizer
        self.config = config or HybridRetrieverConfig()
        self.query_expander = query_expander

    def search(
        self,
        query: str,
        k: Optional[int] = None,
        filters: Optional[Dict[str, Any]] = None,
        include_scores: bool = True,
    ) -> List[SearchResult]:
        """
        Execute hybrid search.

        Args:
            query: The search query
            k: Number of results to return (default: config.final_k)
            filters: Optional metadata filters
            include_scores: Whether to include relevance scores

        Returns:
            List of SearchResult objects ranked by relevance
        """
        k = k or self.config.final_k

        # Expand query if enabled
        expanded_query = query
        if self.config.enable_query_expansion and self.query_expander:
            expanded_query = self.query_expander(query)

        # Tokenize for BM25
        tokens = self.tokenizer.tokenize(expanded_query)

        # Get BM25 results
        bm25_results = self.bm25_index.search(
            tokens,
            k=self.config.bm25_k,
            filters=filters,
        )

        # Get semantic results
        semantic_results = self.semantic_searcher.search(
            expanded_query,
            k=self.config.semantic_k,
            filters=filters,
        )

        # Fuse results
        if self.config.fusion_method == "rrf":
            fused = self._reciprocal_rank_fusion(bm25_results, semantic_results)
        elif self.config.fusion_method == "linear":
            fused = self._linear_fusion(bm25_results, semantic_results)
        else:
            fused = self._max_fusion(bm25_results, semantic_results)

        # Sort by score and limit
        fused.sort(key=lambda x: x.score, reverse=True)
        results = fused[:k]

        # Assign ranks
        for i, result in enumerate(results):
            result.rank = i + 1

        return results

    def _reciprocal_rank_fusion(
        self,
        bm25_results: List[SearchResult],
        semantic_results: List[SearchResult],
    ) -> List[SearchResult]:
        """Combine results using Reciprocal Rank Fusion."""
        scores: Dict[str, float] = {}
        results_map: Dict[str, SearchResult] = {}

        k = self.config.rrf_k

        # Score BM25 results
        for rank, result in enumerate(bm25_results, start=1):
            scores[result.chunk_id] = scores.get(result.chunk_id, 0) + 1.0 / (k + rank)
            results_map[result.chunk_id] = result

        # Score semantic results
        for rank, result in enumerate(semantic_results, start=1):
            scores[result.chunk_id] = scores.get(result.chunk_id, 0) + 1.0 / (k + rank)
            if result.chunk_id not in results_map:
                results_map[result.chunk_id] = result

        # Build fused results
        fused = []
        for chunk_id, score in scores.items():
            result = results_map[chunk_id]
            result.score = score
            result.source = "hybrid"
            fused.append(result)

        return fused
```

### 3.2 BM25Index with Configurable Patterns

```python
# packages/docsearch-core/src/docsearch_core/retrieval/bm25.py

from typing import List, Dict, Any, Optional, Tuple
from dataclasses import dataclass
import math
from collections import Counter


@dataclass
class BM25Config:
    """BM25 algorithm configuration."""

    k1: float = 1.5      # Term frequency saturation parameter
    b: float = 0.75      # Length normalization parameter
    delta: float = 0.5   # BM25+ delta parameter
    algorithm: str = "bm25plus"  # "bm25", "bm25plus", "bm25l"


class BM25Index:
    """
    BM25 keyword search index with pluggable tokenizer.

    Supports BM25, BM25+, and BM25L algorithms.
    """

    def __init__(
        self,
        tokenizer: "TokenizerProtocol",
        config: Optional[BM25Config] = None,
    ):
        self.tokenizer = tokenizer
        self.config = config or BM25Config()

        # Document storage
        self.documents: Dict[str, Tuple[List[str], Dict[str, Any]]] = {}
        self.doc_lengths: Dict[str, int] = {}
        self.avg_doc_length: float = 0.0

        # Inverted index
        self.inverted_index: Dict[str, Dict[str, int]] = {}
        self.doc_freqs: Dict[str, int] = {}

        # Statistics
        self.total_docs: int = 0

    def add_documents(
        self,
        documents: List[Tuple[str, str, Dict[str, Any]]],
    ) -> None:
        """
        Add documents to the index.

        Args:
            documents: List of (doc_id, text, metadata) tuples
        """
        for doc_id, text, metadata in documents:
            tokens = self.tokenizer.tokenize(text)
            self.documents[doc_id] = (tokens, metadata)
            self.doc_lengths[doc_id] = len(tokens)

            # Update inverted index
            token_counts = Counter(tokens)
            for token, count in token_counts.items():
                if token not in self.inverted_index:
                    self.inverted_index[token] = {}
                self.inverted_index[token][doc_id] = count

                # Update document frequency
                if doc_id not in self.inverted_index.get(token, {}):
                    self.doc_freqs[token] = self.doc_freqs.get(token, 0) + 1

        # Update statistics
        self.total_docs = len(self.documents)
        if self.total_docs > 0:
            self.avg_doc_length = sum(self.doc_lengths.values()) / self.total_docs

    def search(
        self,
        query_tokens: List[str],
        k: int = 10,
        filters: Optional[Dict[str, Any]] = None,
    ) -> List["SearchResult"]:
        """
        Search the index.

        Args:
            query_tokens: Tokenized query
            k: Number of results to return
            filters: Optional metadata filters

        Returns:
            List of SearchResult objects
        """
        from .hybrid import SearchResult

        scores: Dict[str, float] = {}

        for token in query_tokens:
            if token not in self.inverted_index:
                continue

            # IDF calculation
            df = self.doc_freqs.get(token, 0)
            idf = math.log((self.total_docs - df + 0.5) / (df + 0.5) + 1)

            for doc_id, tf in self.inverted_index[token].items():
                # Apply filters
                if filters:
                    _, metadata = self.documents[doc_id]
                    if not self._matches_filters(metadata, filters):
                        continue

                # BM25 score calculation
                doc_len = self.doc_lengths[doc_id]
                score = self._calculate_score(tf, idf, doc_len)
                scores[doc_id] = scores.get(doc_id, 0) + score

        # Sort and return top-k
        sorted_docs = sorted(scores.items(), key=lambda x: x[1], reverse=True)[:k]

        results = []
        for doc_id, score in sorted_docs:
            tokens, metadata = self.documents[doc_id]
            results.append(SearchResult(
                chunk_id=doc_id,
                content=" ".join(tokens),
                score=score,
                metadata=metadata,
                source="bm25",
            ))

        return results

    def _calculate_score(self, tf: int, idf: float, doc_len: int) -> float:
        """Calculate BM25/BM25+/BM25L score."""
        k1 = self.config.k1
        b = self.config.b

        # Length normalization
        norm = 1 - b + b * (doc_len / self.avg_doc_length)

        if self.config.algorithm == "bm25plus":
            # BM25+ adds delta to prevent zero scores
            return idf * ((tf * (k1 + 1)) / (tf + k1 * norm) + self.config.delta)
        elif self.config.algorithm == "bm25l":
            # BM25L with different normalization
            ctd = tf / (1 - b + b * (doc_len / self.avg_doc_length))
            return idf * ((k1 + 1) * ctd) / (k1 + ctd)
        else:
            # Standard BM25
            return idf * (tf * (k1 + 1)) / (tf + k1 * norm)

    def _matches_filters(
        self,
        metadata: Dict[str, Any],
        filters: Dict[str, Any],
    ) -> bool:
        """Check if metadata matches filters."""
        for key, value in filters.items():
            if key not in metadata:
                return False
            if isinstance(value, list):
                if metadata[key] not in value:
                    return False
            elif metadata[key] != value:
                return False
        return True
```

### 3.3 ClaudeReranker with Templated Prompts

```python
# packages/docsearch-core/src/docsearch_core/ranking/reranker.py

from typing import List, Optional, Dict, Any
from dataclasses import dataclass
import subprocess
import json
import os


@dataclass
class RerankerConfig:
    """Configuration for Claude-based reranking."""

    model: str = "haiku"  # "haiku", "sonnet", "opus"
    max_tokens: int = 1024
    temperature: float = 0.0
    timeout_seconds: int = 30
    max_results_to_rerank: int = 20
    min_relevance_threshold: float = 0.3
    use_subscription: bool = True  # Use Claude Code subscription, not API
    always_rerank: bool = True  # For Max subscription users


class ClaudeReranker:
    """
    Reranks search results using Claude via Claude Code headless mode.

    Uses the user's Claude subscription (not API credits) by calling
    `claude -p --model {model}` in print mode.
    """

    # Default rerank prompt template
    DEFAULT_PROMPT_TEMPLATE = '''You are a documentation search result ranker.

Given a user query and a list of search results, rank them by relevance.

Query: {query}

Results to rank:
{results}

Rank these results from most to least relevant. Consider:
{relevance_criteria}

Return a JSON array of result IDs in order of relevance:
["id1", "id2", "id3", ...]

Only return the JSON array, nothing else.'''

    def __init__(
        self,
        config: Optional[RerankerConfig] = None,
        prompt_template: Optional[str] = None,
        relevance_criteria: Optional[Dict[str, str]] = None,
    ):
        self.config = config or RerankerConfig()
        self.prompt_template = prompt_template or self.DEFAULT_PROMPT_TEMPLATE
        self.relevance_criteria = relevance_criteria or {}
        self._cli_available: Optional[bool] = None

    def is_available(self) -> bool:
        """Check if Claude CLI is available."""
        if self._cli_available is None:
            try:
                result = subprocess.run(
                    ["claude", "--version"],
                    capture_output=True,
                    timeout=5,
                )
                self._cli_available = result.returncode == 0
            except (subprocess.TimeoutExpired, FileNotFoundError):
                self._cli_available = False
        return self._cli_available

    def rerank(
        self,
        query: str,
        results: List["SearchResult"],
        top_k: Optional[int] = None,
    ) -> List["SearchResult"]:
        """
        Rerank search results using Claude.

        Args:
            query: The original search query
            results: List of SearchResult objects to rerank
            top_k: Number of top results to return (default: len(results))

        Returns:
            Reranked list of SearchResult objects
        """
        if not self.is_available():
            return results

        if not results:
            return results

        # Limit results to rerank
        results_to_rerank = results[:self.config.max_results_to_rerank]
        top_k = top_k or len(results_to_rerank)

        # Format results for prompt
        results_text = self._format_results(results_to_rerank)

        # Format relevance criteria
        criteria_text = "\n".join(
            f"- {name}: {desc}"
            for name, desc in self.relevance_criteria.items()
        ) or "- Relevance to the query\n- Completeness of information\n- Code examples if requested"

        # Build prompt
        prompt = self.prompt_template.format(
            query=query,
            results=results_text,
            relevance_criteria=criteria_text,
        )

        # Call Claude CLI
        try:
            ranked_ids = self._call_claude(prompt)
            return self._reorder_results(results_to_rerank, ranked_ids, top_k)
        except Exception:
            # Fallback to original order
            return results_to_rerank[:top_k]

    def _format_results(self, results: List["SearchResult"]) -> str:
        """Format results for the rerank prompt."""
        formatted = []
        for result in results:
            formatted.append(
                f"ID: {result.chunk_id}\n"
                f"Content: {result.content[:500]}...\n"
                f"---"
            )
        return "\n".join(formatted)

    def _call_claude(self, prompt: str) -> List[str]:
        """Call Claude CLI in print mode."""
        env = os.environ.copy()
        if self.config.use_subscription:
            env.pop("ANTHROPIC_API_KEY", None)

        result = subprocess.run(
            ["claude", "-p", "--model", self.config.model, prompt],
            capture_output=True,
            text=True,
            timeout=self.config.timeout_seconds,
            env=env,
        )

        if result.returncode != 0:
            raise RuntimeError(f"Claude CLI error: {result.stderr}")

        # Parse JSON response
        response = result.stdout.strip()
        return json.loads(response)

    def _reorder_results(
        self,
        results: List["SearchResult"],
        ranked_ids: List[str],
        top_k: int,
    ) -> List["SearchResult"]:
        """Reorder results based on ranked IDs."""
        id_to_result = {r.chunk_id: r for r in results}

        reranked = []
        for i, chunk_id in enumerate(ranked_ids[:top_k]):
            if chunk_id in id_to_result:
                result = id_to_result[chunk_id]
                result.rank = i + 1
                reranked.append(result)

        # Add any missing results at the end
        seen = set(ranked_ids)
        for result in results:
            if result.chunk_id not in seen:
                result.rank = len(reranked) + 1
                reranked.append(result)
                if len(reranked) >= top_k:
                    break

        return reranked
```

### 3.4 Base Metadata Schemas

```python
# packages/docsearch-core/src/docsearch_core/metadata/base.py

from typing import Optional, List, Dict, Any
from enum import Enum
from dataclasses import dataclass, field
from abc import ABC, abstractmethod


class BaseDocType(str, Enum):
    """Base document types (extensible by domains)."""

    REFERENCE = "reference"
    TUTORIAL = "tutorial"
    GUIDE = "guide"
    API = "api"
    EXAMPLE = "example"
    FAQ = "faq"
    TROUBLESHOOTING = "troubleshooting"


class BaseContentType(str, Enum):
    """Base content types."""

    CONCEPTUAL = "conceptual"
    CODE_EXAMPLE = "code_example"
    CONFIGURATION = "configuration"
    PROCEDURE = "procedure"
    REFERENCE = "reference"


@dataclass
class ChunkMetadata:
    """
    Base metadata for documentation chunks.

    Domain plugins should extend this class to add
    domain-specific metadata fields.
    """

    # Required fields
    chunk_id: str
    source_file: str

    # Content classification
    doc_type: Optional[str] = None
    content_type: Optional[str] = None

    # Hierarchy
    section: Optional[str] = None
    subsection: Optional[str] = None

    # Search hints
    keywords: List[str] = field(default_factory=list)

    # Quality indicators
    has_code: bool = False
    code_language: Optional[str] = None

    # Chunk position
    chunk_index: int = 0
    total_chunks: int = 1

    # Custom fields (for domain extensions)
    custom: Dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for storage."""
        result = {
            "chunk_id": self.chunk_id,
            "source_file": self.source_file,
            "doc_type": self.doc_type,
            "content_type": self.content_type,
            "section": self.section,
            "subsection": self.subsection,
            "keywords": self.keywords,
            "has_code": self.has_code,
            "code_language": self.code_language,
            "chunk_index": self.chunk_index,
            "total_chunks": self.total_chunks,
        }
        result.update(self.custom)
        return result

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "ChunkMetadata":
        """Create from dictionary."""
        known_fields = {
            "chunk_id", "source_file", "doc_type", "content_type",
            "section", "subsection", "keywords", "has_code",
            "code_language", "chunk_index", "total_chunks",
        }

        known = {k: v for k, v in data.items() if k in known_fields}
        custom = {k: v for k, v in data.items() if k not in known_fields}

        return cls(**known, custom=custom)
```

---

## 4. Domain Plugin System

### 4.1 DomainPlugin Base Class

```python
# packages/docsearch-core/src/docsearch_core/plugins/base.py

from typing import Dict, List, Optional, Type, Any
from dataclasses import dataclass, field
from abc import ABC, abstractmethod
from pathlib import Path
import importlib.resources


@dataclass
class DomainConfig:
    """Configuration specification for a domain plugin."""

    # Identity
    name: str                      # e.g., "stm32"
    display_name: str              # e.g., "STM32"
    description: str
    version: str
    core_version_requirement: str  # e.g., ">=1.0.0,<2.0.0"

    # Package info
    package_name: str              # e.g., "docsearch_stm32"

    # Resource paths (relative to package)
    markdowns_path: str = "markdowns"
    agents_path: str = "agents"
    commands_path: str = "commands"

    # Plugin components
    tokenizer_class: str = ""      # e.g., "docsearch_stm32.tokenization:STM32Tokenizer"
    synonyms_file: str = "config/synonyms.yaml"
    config_file: str = "config/domain_config.yaml"

    # Reranking
    relevance_criteria: Dict[str, str] = field(default_factory=dict)
    rerank_prompt_template: Optional[str] = None

    # MCP tools to expose
    mcp_tools: List[str] = field(default_factory=list)

    def get_package_path(self) -> Path:
        """Get the filesystem path to the package."""
        module = importlib.import_module(self.package_name)
        return Path(module.__file__).parent


class DomainPlugin(ABC):
    """
    Base class for domain plugins.

    Domain plugins must implement this interface to integrate
    with the docsearch core library.
    """

    def __init__(self):
        self._tokenizer = None
        self._synonyms = None
        self._config = None

    @property
    @abstractmethod
    def domain_config(self) -> DomainConfig:
        """Return the domain configuration."""
        pass

    @abstractmethod
    def get_tokenizer(self) -> "TokenizerProtocol":
        """Return the domain-specific tokenizer."""
        pass

    @abstractmethod
    def get_synonyms(self) -> Dict[str, List[str]]:
        """Return the synonym dictionary."""
        pass

    @abstractmethod
    def get_query_patterns(self) -> Dict[str, str]:
        """Return regex patterns for query parsing."""
        pass

    @abstractmethod
    def get_metadata_class(self) -> Type["ChunkMetadata"]:
        """Return the domain-specific metadata class."""
        pass

    def get_rerank_prompt(self) -> str:
        """Return the reranking prompt template."""
        config = self.domain_config
        if config.rerank_prompt_template:
            return config.rerank_prompt_template

        # Build from relevance criteria
        criteria = "\n".join(
            f"- {name}: {desc}"
            for name, desc in config.relevance_criteria.items()
        )

        return f'''You are a {config.display_name} documentation expert.

Rank these search results by relevance to the query.

Consider:
{criteria}

Query: {{query}}

Results:
{{results}}

Return a JSON array of result IDs in order of relevance.'''

    def get_agents_path(self) -> Path:
        """Get path to agents directory."""
        config = self.domain_config
        return config.get_package_path() / config.agents_path

    def get_commands_path(self) -> Path:
        """Get path to commands directory."""
        config = self.domain_config
        return config.get_package_path() / config.commands_path

    def get_markdowns_path(self) -> Path:
        """Get path to markdown documentation."""
        config = self.domain_config
        return config.get_package_path() / config.markdowns_path

    def validate(self) -> List[str]:
        """
        Validate the plugin configuration.

        Returns a list of validation error messages.
        """
        errors = []
        config = self.domain_config

        # Check required fields
        if not config.name:
            errors.append("Domain name is required")
        if not config.display_name:
            errors.append("Display name is required")

        # Check paths exist
        pkg_path = config.get_package_path()

        agents_path = pkg_path / config.agents_path
        if not agents_path.exists():
            errors.append(f"Agents path does not exist: {agents_path}")

        markdowns_path = pkg_path / config.markdowns_path
        if not markdowns_path.exists():
            errors.append(f"Markdowns path does not exist: {markdowns_path}")

        # Check tokenizer
        try:
            self.get_tokenizer()
        except Exception as e:
            errors.append(f"Failed to load tokenizer: {e}")

        return errors
```

### 4.2 Plugin Registry

```python
# packages/docsearch-core/src/docsearch_core/plugins/registry.py

from typing import Dict, Optional, List, Type
from importlib.metadata import entry_points
import logging

from .base import DomainPlugin


logger = logging.getLogger(__name__)


class PluginRegistry:
    """
    Registry for discovering and loading domain plugins.

    Plugins are discovered via the 'docsearch_domains' entry point group.
    """

    _instance: Optional["PluginRegistry"] = None

    def __init__(self):
        self._plugins: Dict[str, DomainPlugin] = {}
        self._plugin_classes: Dict[str, Type[DomainPlugin]] = {}

    @classmethod
    def get_instance(cls) -> "PluginRegistry":
        """Get the singleton registry instance."""
        if cls._instance is None:
            cls._instance = cls()
        return cls._instance

    def discover_plugins(self) -> List[str]:
        """
        Discover available domain plugins.

        Returns list of discovered plugin names.
        """
        discovered = []

        # Python 3.10+ entry_points API
        try:
            eps = entry_points(group="docsearch_domains")
        except TypeError:
            # Python 3.9 fallback
            eps = entry_points().get("docsearch_domains", [])

        for ep in eps:
            try:
                plugin_class = ep.load()
                self._plugin_classes[ep.name] = plugin_class
                discovered.append(ep.name)
                logger.info(f"Discovered domain plugin: {ep.name}")
            except Exception as e:
                logger.warning(f"Failed to load plugin {ep.name}: {e}")

        return discovered

    def get_plugin(self, name: str) -> Optional[DomainPlugin]:
        """Get a plugin instance by name."""
        if name not in self._plugins:
            if name in self._plugin_classes:
                self._plugins[name] = self._plugin_classes[name]()
            else:
                return None
        return self._plugins[name]

    def register_plugin(self, name: str, plugin: DomainPlugin) -> None:
        """Manually register a plugin."""
        self._plugins[name] = plugin

    def list_plugins(self) -> List[str]:
        """List all available plugin names."""
        return list(set(self._plugins.keys()) | set(self._plugin_classes.keys()))


def get_plugin(name: str) -> Optional[DomainPlugin]:
    """Convenience function to get a plugin by name."""
    registry = PluginRegistry.get_instance()
    registry.discover_plugins()
    return registry.get_plugin(name)
```

---

## 5. Claude Code Integration

### 5.1 MCP Server Per Domain (Recommended)

Each domain has its own MCP server that:
- Registers domain-specific tools
- Uses the shared core library
- Provides domain-specific resources

```python
# packages/docsearch-stm32/src/docsearch_stm32/server/mcp_server.py

from typing import Any
from mcp.server import Server
from mcp.types import Tool, TextContent

from docsearch_core.retrieval.hybrid import HybridRetriever
from docsearch_core.ranking.reranker import ClaudeReranker
from docsearch_core.plugins.registry import get_plugin

from ..plugin import STM32Plugin


# Initialize server
server = Server("stm32-docs")

# Get plugin
plugin = STM32Plugin()

# Initialize components
hybrid_retriever = None
reranker = None


@server.list_tools()
async def list_tools() -> list[Tool]:
    """List available tools."""
    return [
        Tool(
            name="search_stm32_docs",
            description="Search STM32 documentation using semantic search",
            inputSchema={
                "type": "object",
                "properties": {
                    "query": {"type": "string", "description": "Search query"},
                    "num_results": {"type": "integer", "default": 5},
                    "peripheral": {"type": "string", "description": "Filter by peripheral"},
                    "require_code": {"type": "boolean", "default": False},
                },
                "required": ["query"],
            },
        ),
        Tool(
            name="get_peripheral_docs",
            description="Get documentation for a specific STM32 peripheral",
            inputSchema={
                "type": "object",
                "properties": {
                    "peripheral": {"type": "string"},
                    "topic": {"type": "string", "default": ""},
                },
                "required": ["peripheral"],
            },
        ),
        # ... more tools
    ]


@server.call_tool()
async def call_tool(name: str, arguments: dict[str, Any]) -> list[TextContent]:
    """Handle tool calls."""
    global hybrid_retriever, reranker

    # Lazy initialization
    if hybrid_retriever is None:
        hybrid_retriever = _initialize_retriever()
        reranker = ClaudeReranker(
            prompt_template=plugin.get_rerank_prompt(),
            relevance_criteria=plugin.domain_config.relevance_criteria,
        )

    if name == "search_stm32_docs":
        results = hybrid_retriever.search(
            query=arguments["query"],
            k=arguments.get("num_results", 5),
            filters=_build_filters(arguments),
        )

        # Rerank if enabled
        if reranker.is_available():
            results = reranker.rerank(arguments["query"], results)

        return [TextContent(
            type="text",
            text=_format_results(results),
        )]

    # ... handle other tools


def main():
    """Entry point for MCP server."""
    import asyncio
    from mcp.server.stdio import stdio_server

    async def run():
        async with stdio_server() as (read_stream, write_stream):
            await server.run(read_stream, write_stream, server.create_initialization_options())

    asyncio.run(run())


if __name__ == "__main__":
    main()
```

### 5.2 Agent Generator

```python
# packages/docsearch-core/src/docsearch_core/generators/agents.py

from typing import List, Dict, Any
from pathlib import Path
import yaml


class AgentGenerator:
    """
    Generates agent definition files for a domain.

    Agents are Markdown files with YAML frontmatter that define
    specialized AI assistants for Claude Code.
    """

    AGENT_TEMPLATE = '''---
name: {name}
description: {description}
---

# {title}

You are an expert in {specialty}.

## Available Tools

{tools}

## Expertise Areas

{expertise}

## Guidelines

{guidelines}

## Example Interactions

{examples}
'''

    def __init__(self, domain_config: "DomainConfig"):
        self.config = domain_config

    def generate(
        self,
        role: str,
        role_title: str,
        description: str,
        specialty: str,
        tools: List[str],
        expertise: List[str] = None,
        guidelines: List[str] = None,
        examples: List[str] = None,
    ) -> str:
        """Generate agent markdown content."""
        name = f"{self.config.name}-{role}"

        tools_text = "\n".join(f"- `{tool}` - {self._get_tool_description(tool)}" for tool in tools)
        expertise_text = "\n".join(f"- {e}" for e in (expertise or []))
        guidelines_text = "\n".join(f"{i+1}. {g}" for i, g in enumerate(guidelines or []))
        examples_text = "\n".join(f"- {e}" for e in (examples or []))

        return self.AGENT_TEMPLATE.format(
            name=name,
            title=f"{self.config.display_name} {role_title} Agent",
            description=description,
            specialty=specialty,
            tools=tools_text,
            expertise=expertise_text or "General domain expertise",
            guidelines=guidelines_text or "Follow best practices",
            examples=examples_text or "Answer user questions accurately",
        )

    def _get_tool_description(self, tool: str) -> str:
        """Get description for a tool."""
        descriptions = {
            f"search_{self.config.name}_docs": f"Search {self.config.display_name} documentation",
            "get_peripheral_docs": "Get peripheral documentation",
            "get_code_examples": "Find code examples",
            "troubleshoot_error": "Troubleshoot errors",
        }
        return descriptions.get(tool, "Tool for domain operations")

    def generate_router(self) -> str:
        """Generate a router agent for the domain."""
        return self.generate(
            role="router",
            role_title="Router",
            description=f"Routes {self.config.display_name} queries to appropriate specialist agents",
            specialty="query classification and routing",
            tools=[f"search_{self.config.name}_docs"],
            guidelines=[
                "Analyze the user's query to determine the best specialist agent",
                "Consider the query topic, complexity, and required expertise",
                "Route to the most appropriate specialist for detailed help",
            ],
            examples=[
                f"'How do I configure X?' -> {self.config.name}-config agent",
                f"'Why is X not working?' -> {self.config.name}-debug agent",
                f"'Show me example code for X' -> {self.config.name}-examples agent",
            ],
        )
```

### 5.3 Installation Flow for End Users

```
┌─────────────────────────────────────────────────────────────────────────────────┐
│                         END USER INSTALLATION FLOW                               │
│                                                                                  │
│  Step 1: User runs installation command                                         │
│  ┌─────────────────────────────────────────────────────────────────────────┐    │
│  │  claude mcp add stm32-docs -- uvx --from docsearch-stm32 stm32-mcp-docs │    │
│  └─────────────────────────────────────────────────────────────────────────┘    │
│                                        │                                         │
│                                        ▼                                         │
│  Step 2: uvx downloads and installs docsearch-stm32 package                     │
│  ┌─────────────────────────────────────────────────────────────────────────┐    │
│  │  - docsearch-stm32 (domain package)                                     │    │
│  │  - docsearch-core (dependency, pulled automatically)                    │    │
│  │  - sentence-transformers, chromadb, etc.                                │    │
│  └─────────────────────────────────────────────────────────────────────────┘    │
│                                        │                                         │
│                                        ▼                                         │
│  Step 3: MCP server starts, first-run initialization triggers                   │
│  ┌─────────────────────────────────────────────────────────────────────────┐    │
│  │  if not ~/.docsearch/stm32/.installed:                                  │    │
│  │      - Copy 16 agents to ~/.claude/agents/                              │    │
│  │      - Copy 4 commands to ~/.claude/commands/                           │    │
│  │      - Generate embeddings for 80 markdown files                        │    │
│  │      - Build BM25 index                                                 │    │
│  │      - Create ChromaDB collection                                       │    │
│  │      - Touch .installed marker                                          │    │
│  └─────────────────────────────────────────────────────────────────────────┘    │
│                                        │                                         │
│                                        ▼                                         │
│  Step 4: MCP server ready, Claude Code can use tools                            │
│  ┌─────────────────────────────────────────────────────────────────────────┐    │
│  │  Available:                                                             │    │
│  │  - 15+ MCP tools (search_stm32_docs, get_peripheral_docs, etc.)        │    │
│  │  - 4 MCP resources (stm32://status, etc.)                              │    │
│  │  - 16 agents in ~/.claude/agents/stm32-*.md                            │    │
│  │  - 4 slash commands (/stm32, /stm32-init, etc.)                        │    │
│  └─────────────────────────────────────────────────────────────────────────┘    │
│                                                                                  │
└─────────────────────────────────────────────────────────────────────────────────┘
```

### 5.4 Claude Code Configuration Files

```json
// ~/.claude/mcp.json (after installing multiple domains)
{
  "mcpServers": {
    "stm32-docs": {
      "command": "uvx",
      "args": ["--from", "docsearch-stm32", "stm32-mcp-docs"]
    },
    "arduino-docs": {
      "command": "uvx",
      "args": ["--from", "docsearch-arduino", "arduino-mcp-docs"]
    },
    "aws-docs": {
      "command": "uvx",
      "args": ["--from", "docsearch-aws", "aws-mcp-docs"]
    }
  }
}
```

---

## 6. Configuration System

### 6.1 YAML Schema for Domain Configs

```yaml
# Domain configuration schema (config_schema.yaml)

# Required fields
domain:
  name: string          # lowercase identifier (e.g., "stm32")
  display_name: string  # human-readable name (e.g., "STM32")
  description: string   # one-line description
  version: string       # semver (e.g., "1.0.0")

# Core compatibility
compatibility:
  core_version: string  # semver range (e.g., ">=1.0.0,<2.0.0")

# Retrieval settings (override core defaults)
retrieval:
  bm25_weight: float       # 0.0-1.0, default 0.4
  semantic_weight: float   # 0.0-1.0, default 0.6
  bm25_k: int              # candidates from BM25, default 50
  semantic_k: int          # candidates from semantic, default 50
  final_k: int             # final results, default 20
  fusion_method: string    # "rrf", "linear", "max"
  rrf_k: int               # RRF constant, default 60
  enable_query_expansion: bool
  min_score_threshold: float

# BM25 settings
bm25:
  k1: float      # term frequency saturation, default 1.5
  b: float       # length normalization, default 0.75
  delta: float   # BM25+ delta, default 0.5
  algorithm: string  # "bm25", "bm25plus", "bm25l"

# Storage settings
storage:
  collection_name: string    # ChromaDB collection name
  embedding_model: string    # sentence-transformers model
  distance_metric: string    # "cosine", "l2", "ip"
  batch_size: int            # embedding batch size

# Ranking settings
ranking:
  rerank_model: string            # Claude model for reranking
  max_tokens: int                 # max tokens for rerank response
  temperature: float              # 0.0 for deterministic
  max_results_to_rerank: int      # limit for performance
  min_relevance_threshold: float  # filter low-relevance results
  batch_size: int                 # rerank batch size

# Server settings
server:
  mode: string      # "local", "network", "hybrid"
  host: string      # bind address
  port: int         # bind port
  log_level: string # "DEBUG", "INFO", "WARNING", "ERROR"

# Domain-specific settings (arbitrary key-value)
custom:
  key: value
```

### 6.2 Environment Variable Conventions

```bash
# Core environment variables (apply to all domains)
DOCSEARCH_LOG_LEVEL=INFO
DOCSEARCH_EMBEDDING_MODEL=all-MiniLM-L6-v2
DOCSEARCH_BM25_WEIGHT=0.4
DOCSEARCH_SEMANTIC_WEIGHT=0.6
DOCSEARCH_RERANK_MODEL=claude-3-5-haiku-20241022

# Domain-specific environment variables
# Pattern: DOCSEARCH_{DOMAIN}_{SETTING}

# STM32
DOCSEARCH_STM32_DB_PATH=~/.docsearch/stm32/chroma_db
DOCSEARCH_STM32_COLLECTION=stm32_docs
DOCSEARCH_STM32_DEFAULT_FAMILY=STM32F4

# Arduino
DOCSEARCH_ARDUINO_DB_PATH=~/.docsearch/arduino/chroma_db
DOCSEARCH_ARDUINO_COLLECTION=arduino_docs
DOCSEARCH_ARDUINO_INCLUDE_ESP32=true

# AWS
DOCSEARCH_AWS_DB_PATH=~/.docsearch/aws/chroma_db
DOCSEARCH_AWS_COLLECTION=aws_docs
DOCSEARCH_AWS_SERVICES_FILTER=ec2,s3,lambda
```

### 6.3 Per-Project Overrides

```yaml
# .docsearch.yaml (placed in project root)
# Overrides user and domain defaults for this project

# Override for all domains
retrieval:
  final_k: 10  # Fewer results for this project

# Domain-specific project overrides
domains:
  stm32:
    custom:
      default_family: STM32H7
      preferred_library: LL
    retrieval:
      min_score_threshold: 0.3

  aws:
    custom:
      services_filter:
        - lambda
        - dynamodb
        - api-gateway
```

---

## 7. Syncing Strategy

### 7.1 Version Management

```
┌─────────────────────────────────────────────────────────────────────────────────┐
│                           VERSION MANAGEMENT                                     │
│                                                                                  │
│  Semantic Versioning: MAJOR.MINOR.PATCH                                         │
│                                                                                  │
│  Core Package (docsearch-core):                                                  │
│  ├── MAJOR: Breaking API changes (tokenizer interface, plugin base class)       │
│  ├── MINOR: New features, non-breaking additions                                │
│  └── PATCH: Bug fixes, performance improvements                                  │
│                                                                                  │
│  Domain Packages (docsearch-{domain}):                                          │
│  ├── MAJOR: Breaking changes to domain-specific features                        │
│  ├── MINOR: New agents, tools, documentation updates                            │
│  └── PATCH: Bug fixes, typo corrections                                          │
│                                                                                  │
│  Compatibility Matrix:                                                           │
│  ┌─────────────────────────────────────────────────────────────────────────┐    │
│  │  docsearch-core  │  docsearch-stm32  │  docsearch-arduino  │  Status    │    │
│  │──────────────────│───────────────────│─────────────────────│────────────│    │
│  │  1.0.x           │  1.0.x - 1.2.x    │  1.0.x              │  Supported │    │
│  │  1.1.x           │  1.1.x - 1.3.x    │  1.0.x - 1.1.x      │  Supported │    │
│  │  2.0.x           │  2.0.x+           │  2.0.x+             │  Planned   │    │
│  └─────────────────────────────────────────────────────────────────────────┘    │
│                                                                                  │
└─────────────────────────────────────────────────────────────────────────────────┘
```

### 7.2 Core Update Propagation Script

```python
# scripts/sync-core.py

"""
Sync core changes to all domain packages.

This script:
1. Updates core dependency version in domain pyproject.toml files
2. Regenerates any templated files
3. Runs tests across all domains
4. Creates a PR for the updates
"""

import subprocess
import sys
from pathlib import Path
import toml


REPO_ROOT = Path(__file__).parent.parent
PACKAGES_DIR = REPO_ROOT / "packages"
CORE_PACKAGE = PACKAGES_DIR / "docsearch-core"
DOMAIN_PACKAGES = [
    p for p in PACKAGES_DIR.iterdir()
    if p.is_dir() and p.name.startswith("docsearch-") and p.name != "docsearch-core"
]


def get_core_version() -> str:
    """Get current core version."""
    pyproject = CORE_PACKAGE / "pyproject.toml"
    data = toml.load(pyproject)
    return data["project"]["version"]


def update_domain_dependency(domain_path: Path, core_version: str) -> bool:
    """Update domain's core dependency."""
    pyproject = domain_path / "pyproject.toml"
    data = toml.load(pyproject)

    # Update dependency
    deps = data["project"]["dependencies"]
    for i, dep in enumerate(deps):
        if dep.startswith("docsearch-core"):
            # Parse version requirement
            major, minor, _ = core_version.split(".")
            new_requirement = f"docsearch-core>={core_version},<{int(major)+1}.0.0"
            deps[i] = new_requirement
            break

    # Write back
    with open(pyproject, "w") as f:
        toml.dump(data, f)

    return True


def run_domain_tests(domain_path: Path) -> bool:
    """Run tests for a domain package."""
    result = subprocess.run(
        ["pytest", str(domain_path / "tests"), "-v"],
        capture_output=True,
        text=True,
    )
    return result.returncode == 0


def sync_all_domains():
    """Sync core to all domain packages."""
    core_version = get_core_version()
    print(f"Syncing core version {core_version} to domains...")

    results = {}
    for domain_path in DOMAIN_PACKAGES:
        print(f"\nProcessing {domain_path.name}...")

        # Update dependency
        update_domain_dependency(domain_path, core_version)

        # Run tests
        test_passed = run_domain_tests(domain_path)
        results[domain_path.name] = test_passed

        if test_passed:
            print(f"  ✓ Tests passed")
        else:
            print(f"  ✗ Tests failed")

    # Summary
    print("\n" + "="*50)
    print("SYNC SUMMARY")
    print("="*50)
    for domain, passed in results.items():
        status = "✓" if passed else "✗"
        print(f"  {status} {domain}")

    failed = [d for d, p in results.items() if not p]
    if failed:
        print(f"\n{len(failed)} domain(s) failed tests. Please fix before merging.")
        sys.exit(1)
    else:
        print("\nAll domains synced successfully!")


if __name__ == "__main__":
    sync_all_domains()
```

### 7.3 CI/CD Pipeline

```yaml
# .github/workflows/ci.yaml

name: CI

on:
  push:
    branches: [main, develop]
  pull_request:
    branches: [main]

jobs:
  test-core:
    runs-on: ubuntu-latest
    strategy:
      matrix:
        python-version: ["3.9", "3.10", "3.11", "3.12"]

    steps:
      - uses: actions/checkout@v4

      - name: Set up Python
        uses: actions/setup-python@v5
        with:
          python-version: ${{ matrix.python-version }}

      - name: Install core package
        run: |
          cd packages/docsearch-core
          pip install -e ".[dev]"

      - name: Run core tests
        run: |
          cd packages/docsearch-core
          pytest tests/ -v --cov=docsearch_core

      - name: Upload coverage
        uses: codecov/codecov-action@v4
        with:
          file: packages/docsearch-core/coverage.xml

  test-domains:
    needs: test-core
    runs-on: ubuntu-latest
    strategy:
      matrix:
        domain: [stm32, arduino, aws]

    steps:
      - uses: actions/checkout@v4

      - name: Set up Python
        uses: actions/setup-python@v5
        with:
          python-version: "3.11"

      - name: Install packages
        run: |
          cd packages/docsearch-core
          pip install -e .
          cd ../docsearch-${{ matrix.domain }}
          pip install -e ".[dev]"

      - name: Run domain tests
        run: |
          cd packages/docsearch-${{ matrix.domain }}
          pytest tests/ -v

  integration-tests:
    needs: [test-core, test-domains]
    runs-on: ubuntu-latest

    steps:
      - uses: actions/checkout@v4

      - name: Set up Python
        uses: actions/setup-python@v5
        with:
          python-version: "3.11"

      - name: Install all packages
        run: |
          pip install -e packages/docsearch-core
          pip install -e packages/docsearch-stm32
          pip install -e packages/docsearch-arduino

      - name: Run integration tests
        run: pytest tests/integration/ -v

  lint:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4

      - name: Set up Python
        uses: actions/setup-python@v5
        with:
          python-version: "3.11"

      - name: Install linters
        run: pip install ruff mypy

      - name: Run ruff
        run: ruff check packages/

      - name: Run mypy
        run: mypy packages/docsearch-core/src
```

---

## 8. Development Workflow

### 8.1 Core Development

```bash
# Clone the monorepo
git clone https://github.com/your-org/docsearch.git
cd docsearch

# Create virtual environment
python -m venv .venv
source .venv/bin/activate

# Install core in development mode
cd packages/docsearch-core
pip install -e ".[dev]"

# Run core tests
pytest tests/ -v

# Make changes to core
# ... edit files ...

# Run tests again
pytest tests/ -v

# Check types
mypy src/docsearch_core

# Format code
ruff format src/ tests/
ruff check src/ tests/ --fix

# Test with a domain
cd ../docsearch-stm32
pip install -e ".[dev]"
pytest tests/ -v

# Commit changes
git add .
git commit -m "feat(core): Add new tokenizer feature"
```

### 8.2 Domain Development

```bash
# From monorepo root
cd packages/docsearch-stm32

# Install with dev dependencies
pip install -e ".[dev]"

# Run domain tests
pytest tests/ -v

# Test the MCP server locally
python -m docsearch_stm32

# In another terminal, test with Claude Code
claude mcp add stm32-local --command python --args "-m" "docsearch_stm32"

# Make changes
# ... edit tokenizer, add agents, etc ...

# Test search quality
python scripts/test_search_quality.py

# Build documentation database
python scripts/rebuild_database.py

# Commit
git add .
git commit -m "feat(stm32): Add new peripheral documentation"
```

### 8.3 Testing Strategy

```python
# tests/conftest.py (shared fixtures)

import pytest
from pathlib import Path
from docsearch_core.tokenization.default import DefaultTokenizer
from docsearch_core.retrieval.bm25 import BM25Index, BM25Config
from docsearch_core.storage.chroma_store import ChromaStore, ChromaConfig


@pytest.fixture
def temp_data_dir(tmp_path):
    """Temporary data directory for tests."""
    return tmp_path / "docsearch_test"


@pytest.fixture
def default_tokenizer():
    """Default tokenizer for tests."""
    return DefaultTokenizer()


@pytest.fixture
def bm25_index(default_tokenizer, temp_data_dir):
    """BM25 index with test documents."""
    index = BM25Index(
        tokenizer=default_tokenizer,
        config=BM25Config(),
    )

    # Add test documents
    index.add_documents([
        ("doc1", "This is a test document about GPIO configuration", {"type": "tutorial"}),
        ("doc2", "UART serial communication setup guide", {"type": "guide"}),
        ("doc3", "SPI master mode configuration example", {"type": "example"}),
    ])

    return index


@pytest.fixture
def chroma_store(temp_data_dir):
    """ChromaDB store for tests."""
    return ChromaStore(
        ChromaConfig(
            persist_directory=temp_data_dir / "chroma",
            collection_name="test_docs",
        )
    )
```

---

## 9. Migration Path

### 9.1 Phased Approach

```
┌─────────────────────────────────────────────────────────────────────────────────┐
│                           MIGRATION PHASES                                       │
│                                                                                  │
│  Phase 1: Extract Core (2-3 weeks)                                              │
│  ┌─────────────────────────────────────────────────────────────────────────┐    │
│  │  - Create docsearch-core package structure                              │    │
│  │  - Move generic components from stm32-agents:                           │    │
│  │    - HybridRetriever → docsearch_core.retrieval.hybrid                  │    │
│  │    - BM25Index → docsearch_core.retrieval.bm25                          │    │
│  │    - ChromaStore → docsearch_core.storage.chroma_store                  │    │
│  │    - ClaudeReranker → docsearch_core.ranking.reranker                   │    │
│  │  - Create plugin base classes                                           │    │
│  │  - Write core tests                                                     │    │
│  │  - DO NOT change stm32-agents yet (keep working)                        │    │
│  └─────────────────────────────────────────────────────────────────────────┘    │
│                                                                                  │
│  Phase 2: Create STM32 Plugin (1-2 weeks)                                       │
│  ┌─────────────────────────────────────────────────────────────────────────┐    │
│  │  - Create docsearch-stm32 package                                       │    │
│  │  - Move STM32-specific code:                                            │    │
│  │    - STM32Tokenizer                                                     │    │
│  │    - Synonyms, patterns                                                 │    │
│  │    - Metadata extensions                                                │    │
│  │    - Agents, commands                                                   │    │
│  │  - Implement STM32Plugin class                                          │    │
│  │  - Create new MCP server using core                                     │    │
│  │  - Test thoroughly                                                      │    │
│  └─────────────────────────────────────────────────────────────────────────┘    │
│                                                                                  │
│  Phase 3: Parallel Operation (1 week)                                           │
│  ┌─────────────────────────────────────────────────────────────────────────┐    │
│  │  - Keep old stm32-agents working                                        │    │
│  │  - Deploy new docsearch-stm32 alongside                                 │    │
│  │  - Compare search quality                                               │    │
│  │  - Fix any regressions                                                  │    │
│  │  - Document migration for users                                         │    │
│  └─────────────────────────────────────────────────────────────────────────┘    │
│                                                                                  │
│  Phase 4: Cutover (1 week)                                                      │
│  ┌─────────────────────────────────────────────────────────────────────────┐    │
│  │  - Update installation documentation                                    │    │
│  │  - Publish docsearch-core to PyPI                                       │    │
│  │  - Publish docsearch-stm32 to PyPI                                      │    │
│  │  - Update GitHub repo (rename/redirect)                                 │    │
│  │  - Announce migration to users                                          │    │
│  │  - Deprecate old stm32-agents package                                   │    │
│  └─────────────────────────────────────────────────────────────────────────┘    │
│                                                                                  │
│  Phase 5: Add New Domains (ongoing)                                             │
│  ┌─────────────────────────────────────────────────────────────────────────┐    │
│  │  - Create docsearch-arduino                                             │    │
│  │  - Create docsearch-aws                                                 │    │
│  │  - Create docsearch-linux                                               │    │
│  │  - etc.                                                                 │    │
│  └─────────────────────────────────────────────────────────────────────────┘    │
│                                                                                  │
└─────────────────────────────────────────────────────────────────────────────────┘
```

### 9.2 Backward Compatibility Layer

```python
# stm32-agents/mcp_server/compat.py
# Compatibility layer during migration

"""
Compatibility module for stm32-agents -> docsearch-stm32 migration.

This module provides backward-compatible imports during the transition period.
Users can continue using old import paths while we migrate to the new structure.
"""

import warnings
from typing import TYPE_CHECKING

# Check if new packages are available
try:
    from docsearch_core.retrieval.hybrid import HybridRetriever
    from docsearch_core.retrieval.bm25 import BM25Index
    from docsearch_core.storage.chroma_store import ChromaStore
    NEW_PACKAGES_AVAILABLE = True
except ImportError:
    NEW_PACKAGES_AVAILABLE = False


def get_hybrid_retriever(*args, **kwargs):
    """Get HybridRetriever with deprecation warning."""
    if NEW_PACKAGES_AVAILABLE:
        warnings.warn(
            "Importing from stm32-agents is deprecated. "
            "Use 'from docsearch_core.retrieval.hybrid import HybridRetriever' instead.",
            DeprecationWarning,
            stacklevel=2,
        )
        return HybridRetriever(*args, **kwargs)
    else:
        # Fall back to old implementation
        from .retrieval import HybridRetriever as OldHybridRetriever
        return OldHybridRetriever(*args, **kwargs)
```

---

## 10. Example: Adding New Domain (Arduino)

### 10.1 Step-by-Step Walkthrough

```bash
# Step 1: Create domain package from template
cd docsearch/packages
python ../scripts/create-domain.py arduino \
    --display-name "Arduino" \
    --description "Arduino and ESP32 documentation search"

# This creates:
# packages/docsearch-arduino/
# ├── pyproject.toml
# ├── README.md
# └── src/
#     └── docsearch_arduino/
#         ├── __init__.py
#         ├── __main__.py
#         ├── plugin.py
#         ├── config/
#         │   ├── arduino_config.yaml
#         │   ├── synonyms.yaml
#         │   └── patterns.yaml
#         ├── tokenization/
#         │   └── arduino_tokenizer.py
#         ├── agents/
#         ├── commands/
#         ├── markdowns/
#         └── server/
#             └── mcp_server.py
```

### 10.2 Arduino Tokenizer Implementation

```python
# packages/docsearch-arduino/src/docsearch_arduino/tokenization/arduino_tokenizer.py

import re
from typing import List
from docsearch_core.tokenization.base import BaseTokenizer


class ArduinoTokenizer(BaseTokenizer):
    """
    Arduino-specific tokenizer.

    Handles:
    - Board names: Arduino Uno, ESP32-WROOM, etc.
    - Library names: Wire, SPI, WiFi
    - Function names: digitalWrite, analogRead
    - Pin names: D0, A0, GPIO2
    """

    # Arduino board patterns
    BOARD_PATTERNS = [
        re.compile(r"(Arduino)\s*(Uno|Nano|Mega|Due|Zero|MKR|Leonardo)", re.I),
        re.compile(r"(ESP32|ESP8266)[-\s]?(\w+)?", re.I),
        re.compile(r"(Teensy)\s*(\d+\.?\d*)?", re.I),
    ]

    # Pin patterns
    PIN_PATTERN = re.compile(r"\b(D\d+|A\d+|GPIO\d+|PIN_\w+)\b", re.I)

    # Arduino function pattern (camelCase)
    FUNCTION_PATTERN = re.compile(r"\b([a-z]+[A-Z][a-zA-Z]*)\b")

    ARDUINO_STOPWORDS = {
        "the", "a", "an", "is", "are", "was", "were", "be", "been",
        "have", "has", "had", "do", "does", "did", "will", "would",
        "could", "should", "can", "need", "to", "of", "in", "for",
        "on", "with", "at", "by", "from", "as", "and", "or", "but",
        "if", "this", "that", "these", "those", "it", "its",
    }

    def __init__(self):
        super().__init__(
            lowercase=False,
            min_token_length=2,
            stopwords=self.ARDUINO_STOPWORDS,
        )

    def tokenize(self, text: str) -> List[str]:
        tokens = []

        # Extract board names
        for pattern in self.BOARD_PATTERNS:
            for match in pattern.finditer(text):
                tokens.extend(g.lower() for g in match.groups() if g)

        # Extract pin names
        for match in self.PIN_PATTERN.finditer(text):
            tokens.append(match.group(1).upper())

        # Extract function names (split camelCase)
        for match in self.FUNCTION_PATTERN.finditer(text):
            func = match.group(1)
            # Split camelCase
            parts = re.split(r'(?<=[a-z])(?=[A-Z])', func)
            tokens.extend(p.lower() for p in parts)
            tokens.append(func.lower())  # Also keep original

        # Standard word tokenization
        words = re.split(r'[\s\-_.,;:!?()[\]{}\"\'`]+', text)
        for word in words:
            if word and len(word) >= self.min_token_length:
                tokens.append(word.lower())

        return self.filter_tokens(tokens)
```

### 10.3 Arduino Configuration

```yaml
# packages/docsearch-arduino/src/docsearch_arduino/config/arduino_config.yaml

domain:
  name: arduino
  display_name: Arduino
  description: "Semantic search over Arduino and ESP32 documentation"

retrieval:
  bm25_weight: 0.4
  semantic_weight: 0.6
  enable_query_expansion: true

storage:
  collection_name: arduino_docs

# Arduino-specific settings
arduino:
  include_esp32: true
  include_esp8266: true
  default_board: null
  library_index_url: "https://downloads.arduino.cc/libraries/library_index.json"
```

```yaml
# packages/docsearch-arduino/src/docsearch_arduino/config/synonyms.yaml

# Board synonyms
Arduino:
  - AVR
  - ATmega

ESP32:
  - Espressif
  - ESP-IDF
  - ESP32-WROOM

ESP8266:
  - NodeMCU
  - Wemos D1

# Function synonyms
digitalWrite:
  - digital write
  - set pin high
  - set pin low

analogRead:
  - analog read
  - read analog
  - ADC read

Serial:
  - UART
  - serial monitor
  - USB serial

Wire:
  - I2C
  - TWI
  - two wire

SPI:
  - serial peripheral interface

WiFi:
  - wireless
  - network
  - internet

# Concept synonyms
sketch:
  - program
  - code
  - firmware

library:
  - lib
  - module
  - package
```

### 10.4 Arduino Plugin Implementation

```python
# packages/docsearch-arduino/src/docsearch_arduino/plugin.py

from typing import Dict, List, Type
from pathlib import Path
import yaml

from docsearch_core.plugins.base import DomainPlugin, DomainConfig
from docsearch_core.tokenization.base import BaseTokenizer
from docsearch_core.metadata.base import ChunkMetadata

from .tokenization.arduino_tokenizer import ArduinoTokenizer
from .config.metadata import ArduinoMetadata


class ArduinoPlugin(DomainPlugin):
    """Arduino domain plugin."""

    VERSION = "1.0.0"
    CORE_VERSION_REQUIREMENT = ">=1.0.0,<2.0.0"

    @property
    def domain_config(self) -> DomainConfig:
        return DomainConfig(
            name="arduino",
            display_name="Arduino",
            description="Arduino and ESP32 documentation search",
            version=self.VERSION,
            core_version_requirement=self.CORE_VERSION_REQUIREMENT,

            package_name="docsearch_arduino",
            markdowns_path="markdowns",
            agents_path="agents",
            commands_path="commands",

            tokenizer_class="docsearch_arduino.tokenization.arduino_tokenizer:ArduinoTokenizer",
            synonyms_file="config/synonyms.yaml",
            config_file="config/arduino_config.yaml",

            relevance_criteria={
                "Board compatibility": "Code works on the user's target board",
                "Library availability": "Required libraries are available",
                "Code completeness": "Example is complete and runnable",
                "Beginner friendliness": "Explanations are accessible",
            },

            mcp_tools=[
                "search_arduino_docs",
                "get_function_docs",
                "get_library_docs",
                "get_board_docs",
                "get_code_examples",
                "troubleshoot_error",
            ],
        )

    def get_tokenizer(self) -> BaseTokenizer:
        if self._tokenizer is None:
            self._tokenizer = ArduinoTokenizer()
        return self._tokenizer

    def get_synonyms(self) -> Dict[str, List[str]]:
        if self._synonyms is None:
            config = self.domain_config
            package_path = config.get_package_path()
            synonyms_path = package_path / config.synonyms_file

            if synonyms_path.exists():
                with open(synonyms_path) as f:
                    self._synonyms = yaml.safe_load(f)
            else:
                self._synonyms = {}

        return self._synonyms

    def get_query_patterns(self) -> Dict[str, str]:
        return {
            "function_lookup": r"(how to use|what is|explain)\s+(\w+)\(\)",
            "library_lookup": r"(how to use|install|include)\s+(\w+)\s+library",
            "board_specific": r"(for|on|with)\s+(Arduino|ESP32|ESP8266|Teensy)",
        }

    def get_metadata_class(self) -> Type[ChunkMetadata]:
        return ArduinoMetadata
```

---

## 11. Distribution & Deployment

### 11.1 PyPI Package Configuration

```toml
# packages/docsearch-core/pyproject.toml

[build-system]
requires = ["hatchling"]
build-backend = "hatchling.build"

[project]
name = "docsearch-core"
version = "1.0.0"
description = "Core library for universal documentation search"
readme = "README.md"
license = "MIT"
requires-python = ">=3.9"
authors = [
    {name = "Your Name", email = "you@example.com"}
]
keywords = ["documentation", "search", "semantic", "mcp", "claude"]
classifiers = [
    "Development Status :: 4 - Beta",
    "Intended Audience :: Developers",
    "License :: OSI Approved :: MIT License",
    "Programming Language :: Python :: 3",
    "Programming Language :: Python :: 3.9",
    "Programming Language :: Python :: 3.10",
    "Programming Language :: Python :: 3.11",
    "Programming Language :: Python :: 3.12",
]

dependencies = [
    "chromadb>=0.4.0",
    "sentence-transformers>=2.2.0",
    "anthropic>=0.18.0",
    "mcp>=1.0.0",
    "pyyaml>=6.0",
    "numpy>=1.24.0",
]

[project.optional-dependencies]
dev = [
    "pytest>=7.0",
    "pytest-cov>=4.0",
    "pytest-asyncio>=0.21",
    "ruff>=0.1.0",
    "mypy>=1.0",
]

[project.urls]
Homepage = "https://github.com/your-org/docsearch"
Documentation = "https://docsearch.readthedocs.io"
Repository = "https://github.com/your-org/docsearch"
```

### 11.2 Claude Code Installation Commands

```bash
# Core installation commands for each domain

# STM32
claude mcp add stm32-docs -- uvx --from docsearch-stm32 stm32-mcp-docs

# Arduino
claude mcp add arduino-docs -- uvx --from docsearch-arduino arduino-mcp-docs

# AWS
claude mcp add aws-docs -- uvx --from docsearch-aws aws-mcp-docs

# Linux
claude mcp add linux-docs -- uvx --from docsearch-linux linux-mcp-docs

# With auto-install of uv (for fresh systems)
claude mcp add-json stm32-docs --scope user '{"command":"bash","args":["-c","export PATH=\"$HOME/.local/bin:$PATH\" && (command -v uvx >/dev/null 2>&1 || curl -LsSf https://astral.sh/uv/install.sh | sh -s -- -q) && uvx --from docsearch-stm32 stm32-mcp-docs"]}'
```

### 11.3 Auto-Update Mechanism

```python
# packages/docsearch-core/src/docsearch_core/updates.py

"""
Auto-update mechanism for docsearch packages.
"""

import subprocess
import sys
from typing import Optional, Tuple
from packaging import version
import httpx


PYPI_URL = "https://pypi.org/pypi/{package}/json"


def get_installed_version(package: str) -> Optional[str]:
    """Get installed version of a package."""
    try:
        from importlib.metadata import version as get_version
        return get_version(package.replace("-", "_"))
    except Exception:
        return None


def get_latest_version(package: str) -> Optional[str]:
    """Get latest version from PyPI."""
    try:
        response = httpx.get(PYPI_URL.format(package=package), timeout=5.0)
        if response.status_code == 200:
            return response.json()["info"]["version"]
    except Exception:
        pass
    return None


def check_for_updates(package: str) -> Tuple[bool, Optional[str], Optional[str]]:
    """
    Check if an update is available.

    Returns:
        (update_available, current_version, latest_version)
    """
    current = get_installed_version(package)
    latest = get_latest_version(package)

    if current is None or latest is None:
        return False, current, latest

    try:
        update_available = version.parse(latest) > version.parse(current)
        return update_available, current, latest
    except Exception:
        return False, current, latest


def update_package(package: str) -> bool:
    """Update a package to latest version."""
    try:
        subprocess.check_call([
            sys.executable, "-m", "pip", "install",
            "--upgrade", package,
        ])
        return True
    except subprocess.CalledProcessError:
        return False
```

---

## 12. Documentation Requirements

### 12.1 User Documentation Structure

```
docs/
├── index.md                    # Main landing page
├── getting-started/
│   ├── installation.md         # Installation guide
│   ├── quick-start.md          # Quick start tutorial
│   └── configuration.md        # Configuration options
│
├── domains/
│   ├── stm32/
│   │   ├── index.md           # STM32 domain overview
│   │   ├── tools.md           # Available MCP tools
│   │   ├── agents.md          # Available agents
│   │   ├── commands.md        # Slash commands
│   │   └── examples.md        # Usage examples
│   │
│   ├── arduino/
│   │   └── ...
│   │
│   └── aws/
│       └── ...
│
├── guides/
│   ├── search-tips.md          # How to write effective queries
│   ├── customization.md        # Customizing for your needs
│   └── troubleshooting.md      # Common issues and solutions
│
└── reference/
    ├── configuration.md        # Full configuration reference
    ├── environment-vars.md     # Environment variables
    └── api.md                  # Python API reference
```

### 12.2 Developer Documentation

```
docs/
├── development/
│   ├── architecture.md         # System architecture
│   ├── core-components.md      # Core library components
│   ├── plugin-system.md        # Plugin system details
│   └── contributing.md         # Contribution guide
│
├── creating-domains/
│   ├── overview.md             # Domain creation overview
│   ├── step-by-step.md         # Step-by-step tutorial
│   ├── tokenizer.md            # Creating custom tokenizers
│   ├── agents.md               # Writing domain agents
│   ├── mcp-server.md           # MCP server implementation
│   ├── testing.md              # Testing your domain
│   └── publishing.md           # Publishing to PyPI
│
├── api/
│   ├── docsearch_core/
│   │   ├── retrieval.md
│   │   ├── storage.md
│   │   ├── ranking.md
│   │   ├── plugins.md
│   │   └── config.md
│   │
│   └── domain-plugin.md        # DomainPlugin API
│
└── migrations/
    ├── v1-to-v2.md             # Major version migration guides
    └── stm32-agents.md         # Legacy stm32-agents migration
```

---

## Summary

This comprehensive plan provides a complete blueprint for transforming the STM32 MCP documentation server into a universal, multi-domain documentation search platform. Key aspects include:

1. **Modular Architecture**: Clear separation between core infrastructure (docsearch-core) and domain-specific plugins (docsearch-{domain})

2. **Plugin System**: Well-defined `DomainPlugin` base class and `DomainConfig` specification that domains must implement

3. **Extensibility**: Pluggable tokenizers, customizable synonyms, configurable ranking, and templated prompts

4. **Claude Code Integration**: Per-domain MCP servers with auto-installing agents and commands

5. **Configuration Flexibility**: Multi-level configuration (core defaults → domain defaults → user config → project config → environment variables)

6. **Version Management**: Semantic versioning with compatibility matrices and automated sync between core and domains

7. **Migration Path**: Phased approach that maintains backward compatibility during transition

8. **Distribution**: PyPI packages with uvx-based installation and auto-update mechanism

The implementation can proceed in phases, starting with extracting the core library, then migrating STM32, and finally adding new domains like Arduino and AWS. The monorepo structure enables coordinated development while allowing independent package releases.
