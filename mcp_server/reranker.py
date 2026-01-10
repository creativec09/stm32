"""
Claude Headless Re-ranker Module for STM32 Documentation Search

This module provides intelligent re-ranking of search results using Claude Haiku
via the Claude Code CLI in headless mode. It leverages a Max 20x subscription
for aggressive re-ranking of ALL queries (not just a subset).

The re-ranker improves search quality by using an LLM to understand the semantic
relevance of documentation chunks to the user's query, beyond what embedding
similarity alone can capture.

Features:
- Aggressive re-ranking on all queries (Max 20x subscription)
- STM32-specific ranking prompt optimized for embedded documentation
- Graceful fallback to original order on failure
- Support for both claude-agent-sdk and subprocess CLI

Usage:
    from mcp_server.reranker import ClaudeReranker, RerankerConfig

    config = RerankerConfig()
    reranker = ClaudeReranker(config)

    # Re-rank search results
    reranked = await reranker.rerank_async(query, chunks)
    # Or synchronously
    reranked = reranker.rerank_sync(query, chunks)
"""

from __future__ import annotations

import asyncio
import json
import logging
import os
import re
import subprocess
import shutil
from dataclasses import dataclass, field
from typing import Any, Optional

logger = logging.getLogger(__name__)


# =============================================================================
# Configuration
# =============================================================================

@dataclass
class RerankerConfig:
    """
    Configuration for the Claude re-ranker.

    Attributes:
        model: Claude model to use for re-ranking (alias or full name)
        max_chunks: Maximum number of chunks to send to the re-ranker
        top_k: Number of top results to return after re-ranking
        timeout: Timeout in seconds for re-ranking requests
        use_subscription: Use Claude subscription instead of API key
        always_rerank: Always re-rank (True for Max 20x subscription)
        content_truncate_length: Maximum characters per chunk content
        enabled: Enable/disable re-ranking globally
    """
    model: str = "haiku"  # Alias for claude-3-haiku-20240307 (latest)
    max_chunks: int = 20
    top_k: int = 5
    timeout: int = 30
    use_subscription: bool = True
    always_rerank: bool = True  # Max 20x subscription - aggressive usage
    content_truncate_length: int = 500
    enabled: bool = True


# =============================================================================
# Claude Re-ranker Implementation
# =============================================================================

class ClaudeReranker:
    """
    Re-ranks search results using Claude Haiku via Claude Code CLI.

    This class provides both async and sync methods for re-ranking search
    results. It uses the Claude Code CLI in headless/print mode to leverage
    the user's Max 20x subscription rather than requiring an API key.

    Example:
        >>> config = RerankerConfig()
        >>> reranker = ClaudeReranker(config)
        >>>
        >>> # Chunks from vector search
        >>> chunks = [
        ...     {"id": "chunk_001", "content": "...", "metadata": {...}, "score": 0.85},
        ...     {"id": "chunk_002", "content": "...", "metadata": {...}, "score": 0.82},
        ... ]
        >>>
        >>> # Re-rank based on query
        >>> reranked = reranker.rerank_sync("How to configure UART DMA?", chunks)
    """

    def __init__(self, config: Optional[RerankerConfig] = None):
        """
        Initialize the Claude re-ranker.

        Args:
            config: Re-ranker configuration. Uses defaults if not provided.
        """
        self.config = config or RerankerConfig()
        self._sdk_available: Optional[bool] = None
        self._cli_available: Optional[bool] = None

        # Ensure we use subscription, not API key
        if self.config.use_subscription:
            self._unset_api_key()

    def _unset_api_key(self) -> None:
        """
        Unset ANTHROPIC_API_KEY to ensure subscription usage.

        When using the Claude Code CLI with a subscription, we don't want
        the API key to be used. This ensures the CLI uses the logged-in
        user's subscription credits.
        """
        if "ANTHROPIC_API_KEY" in os.environ:
            logger.debug("Unsetting ANTHROPIC_API_KEY to use subscription")
            del os.environ["ANTHROPIC_API_KEY"]

    def _check_sdk_available(self) -> bool:
        """Check if claude-agent-sdk is available."""
        if self._sdk_available is None:
            try:
                import claude_agent_sdk  # noqa: F401
                self._sdk_available = True
                logger.debug("claude-agent-sdk is available")
            except ImportError:
                self._sdk_available = False
                logger.debug("claude-agent-sdk not available, will use CLI")
        return self._sdk_available

    def _check_cli_available(self) -> bool:
        """Check if claude CLI is available."""
        if self._cli_available is None:
            self._cli_available = shutil.which("claude") is not None
            if self._cli_available:
                logger.debug("Claude CLI found in PATH")
            else:
                logger.warning("Claude CLI not found in PATH")
        return self._cli_available

    def _build_prompt(
        self,
        query: str,
        chunks: list[dict[str, Any]]
    ) -> str:
        """
        Build the STM32-specific re-ranking prompt.

        Args:
            query: User's search query
            chunks: List of chunks to rank

        Returns:
            Formatted prompt for the re-ranker
        """
        # Format chunks for the prompt
        chunk_texts = []
        for i, chunk in enumerate(chunks):
            chunk_id = chunk.get("id", f"chunk_{i}")
            content = chunk.get("content", "")
            metadata = chunk.get("metadata", {})

            # Truncate content to avoid excessive token usage
            if len(content) > self.config.content_truncate_length:
                content = content[:self.config.content_truncate_length] + "..."

            # Extract useful metadata
            peripheral = metadata.get("peripheral", "")
            source = metadata.get("source_file", "")
            has_code = metadata.get("has_code", False)
            section = metadata.get("section_title", "")

            # Format metadata line
            meta_parts = []
            if peripheral:
                meta_parts.append(f"Peripheral: {peripheral}")
            if source:
                meta_parts.append(f"Source: {source}")
            if has_code:
                meta_parts.append("Contains code")
            if section:
                meta_parts.append(f"Section: {section}")

            meta_line = " | ".join(meta_parts) if meta_parts else "No metadata"

            chunk_texts.append(
                f"[ID: {chunk_id}]\n"
                f"Metadata: {meta_line}\n"
                f"Content:\n{content}\n"
            )

        chunks_formatted = "\n---\n".join(chunk_texts)

        prompt = f"""You are an STM32 documentation ranking expert. Your task is to rank the following documentation chunks by their relevance to the user's query.

USER QUERY: {query}

DOCUMENTATION CHUNKS:
{chunks_formatted}

INSTRUCTIONS:
1. Analyze each chunk's relevance to the query
2. Consider both direct matches and conceptually related content
3. Prioritize chunks that:
   - Directly answer the query
   - Contain relevant code examples
   - Cover the specific peripheral or topic mentioned
   - Provide complete, actionable information
4. Deprioritize chunks that:
   - Are only tangentially related
   - Contain general information not specific to the query
   - Are incomplete or fragmentary

RESPONSE FORMAT:
Return ONLY a JSON array of chunk IDs ordered from most to least relevant.
Example: ["chunk_003", "chunk_001", "chunk_005", "chunk_002", "chunk_004"]

If no chunks are relevant, return an empty array: []
If all chunks are equally relevant, maintain the original order.

Respond with ONLY the JSON array, no explanation or additional text."""

        return prompt

    def _parse_ranking(
        self,
        response: str,
        original_chunks: list[dict[str, Any]]
    ) -> list[str]:
        """
        Parse the ranking response from Claude.

        Args:
            response: Raw response from Claude
            original_chunks: Original chunks for ID validation

        Returns:
            List of chunk IDs in ranked order
        """
        # Extract JSON array from response
        try:
            # Try direct JSON parse first
            ranking = json.loads(response.strip())
            if isinstance(ranking, list):
                return ranking
        except json.JSONDecodeError:
            pass

        # Try to extract JSON array from response text
        json_match = re.search(r'\[[\s\S]*?\]', response)
        if json_match:
            try:
                ranking = json.loads(json_match.group())
                if isinstance(ranking, list):
                    return ranking
            except json.JSONDecodeError:
                pass

        # Fallback: try to extract IDs line by line
        ids = []
        for line in response.split('\n'):
            # Look for chunk IDs in various formats
            id_match = re.search(r'["\'](chunk[_\-]?\w+)["\']', line)
            if id_match:
                ids.append(id_match.group(1))
            else:
                # Try without quotes
                id_match = re.search(r'(chunk[_\-]?\w+)', line)
                if id_match:
                    ids.append(id_match.group(1))

        if ids:
            return ids

        # If all parsing fails, return original order
        logger.warning("Failed to parse ranking response, returning original order")
        return [chunk.get("id", f"chunk_{i}") for i, chunk in enumerate(original_chunks)]

    def _reorder_chunks(
        self,
        chunks: list[dict[str, Any]],
        ranked_ids: list[str]
    ) -> list[dict[str, Any]]:
        """
        Reorder chunks based on ranked IDs.

        Args:
            chunks: Original chunks
            ranked_ids: Chunk IDs in ranked order

        Returns:
            Reordered chunks
        """
        # Build ID to chunk mapping
        chunk_map = {chunk.get("id", f"chunk_{i}"): chunk for i, chunk in enumerate(chunks)}

        # Reorder based on ranking
        reordered = []
        seen_ids = set()

        for chunk_id in ranked_ids:
            if chunk_id in chunk_map and chunk_id not in seen_ids:
                reordered.append(chunk_map[chunk_id])
                seen_ids.add(chunk_id)

        # Add any chunks that weren't in the ranking (shouldn't happen, but safe)
        for chunk in chunks:
            chunk_id = chunk.get("id")
            if chunk_id and chunk_id not in seen_ids:
                reordered.append(chunk)
                seen_ids.add(chunk_id)

        return reordered

    async def rerank_async(
        self,
        query: str,
        chunks: list[dict[str, Any]]
    ) -> list[dict[str, Any]]:
        """
        Re-rank chunks asynchronously using Claude.

        Args:
            query: User's search query
            chunks: List of chunks from vector search

        Returns:
            Re-ranked chunks (limited to top_k)
        """
        if not self.config.enabled:
            logger.debug("Re-ranking disabled, returning original order")
            return chunks[:self.config.top_k]

        if not chunks:
            return []

        # Limit chunks to max_chunks
        chunks_to_rank = chunks[:self.config.max_chunks]

        # Try SDK first if available
        if self._check_sdk_available():
            try:
                return await self._rerank_with_sdk(query, chunks_to_rank)
            except Exception as e:
                logger.warning(f"SDK re-ranking failed: {e}, falling back to CLI")

        # Fall back to CLI
        if self._check_cli_available():
            # Run CLI in executor to avoid blocking
            loop = asyncio.get_event_loop()
            return await loop.run_in_executor(
                None,
                self._rerank_with_cli,
                query,
                chunks_to_rank
            )

        # No method available, return original order
        logger.warning("No re-ranking method available, returning original order")
        return chunks[:self.config.top_k]

    async def _rerank_with_sdk(
        self,
        query: str,
        chunks: list[dict[str, Any]]
    ) -> list[dict[str, Any]]:
        """
        Re-rank using claude-agent-sdk (if available).

        This is a placeholder for future SDK integration.
        """
        # SDK implementation would go here
        # For now, fall through to CLI
        raise NotImplementedError("SDK not yet implemented")

    def rerank_sync(
        self,
        query: str,
        chunks: list[dict[str, Any]]
    ) -> list[dict[str, Any]]:
        """
        Re-rank chunks synchronously using Claude CLI.

        Args:
            query: User's search query
            chunks: List of chunks from vector search

        Returns:
            Re-ranked chunks (limited to top_k)
        """
        if not self.config.enabled:
            logger.debug("Re-ranking disabled, returning original order")
            return chunks[:self.config.top_k]

        if not chunks:
            return []

        # Limit chunks to max_chunks
        chunks_to_rank = chunks[:self.config.max_chunks]

        if self._check_cli_available():
            return self._rerank_with_cli(query, chunks_to_rank)

        # No method available, return original order
        logger.warning("Claude CLI not available, returning original order")
        return chunks[:self.config.top_k]

    def _rerank_with_cli(
        self,
        query: str,
        chunks: list[dict[str, Any]]
    ) -> list[dict[str, Any]]:
        """
        Re-rank using Claude Code CLI subprocess.

        Uses the CLI in print mode (-p) for single-turn interaction.

        Args:
            query: User's search query
            chunks: Chunks to rank

        Returns:
            Re-ranked chunks
        """
        prompt = self._build_prompt(query, chunks)

        try:
            # Build CLI command
            # Using --print (-p) for single-turn, non-interactive mode
            # Using --model to specify Haiku
            cmd = [
                "claude",
                "--print",  # Non-interactive, single response
                "--model", self.config.model,
                prompt
            ]

            logger.debug(f"Running Claude CLI for re-ranking with model {self.config.model}")

            # Execute CLI
            result = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                timeout=self.config.timeout,
                env={k: v for k, v in os.environ.items() if k != "ANTHROPIC_API_KEY"}
            )

            if result.returncode != 0:
                logger.warning(f"Claude CLI returned non-zero: {result.returncode}")
                logger.debug(f"stderr: {result.stderr}")
                return chunks[:self.config.top_k]

            response = result.stdout.strip()
            logger.debug(f"Claude CLI response: {response[:200]}...")

            # Parse ranking
            ranked_ids = self._parse_ranking(response, chunks)

            # Reorder chunks
            reordered = self._reorder_chunks(chunks, ranked_ids)

            logger.info(f"Re-ranked {len(chunks)} chunks, returning top {self.config.top_k}")
            return reordered[:self.config.top_k]

        except subprocess.TimeoutExpired:
            logger.warning(f"Claude CLI timed out after {self.config.timeout}s")
            return chunks[:self.config.top_k]
        except FileNotFoundError:
            logger.error("Claude CLI not found")
            return chunks[:self.config.top_k]
        except Exception as e:
            logger.error(f"Claude CLI error: {e}")
            return chunks[:self.config.top_k]


# =============================================================================
# Factory and Utility Functions
# =============================================================================

def create_reranker(
    enabled: bool = True,
    model: str = "haiku",
    max_chunks: int = 20,
    top_k: int = 5,
    timeout: int = 30
) -> ClaudeReranker:
    """
    Factory function to create a configured re-ranker.

    Args:
        enabled: Enable re-ranking
        model: Claude model to use
        max_chunks: Maximum chunks to rank
        top_k: Number of results to return
        timeout: Request timeout

    Returns:
        Configured ClaudeReranker instance
    """
    config = RerankerConfig(
        enabled=enabled,
        model=model,
        max_chunks=max_chunks,
        top_k=top_k,
        timeout=timeout
    )
    return ClaudeReranker(config)


def is_reranking_available() -> bool:
    """
    Check if re-ranking is available (CLI installed).

    Returns:
        True if Claude CLI is available
    """
    return shutil.which("claude") is not None


# =============================================================================
# Integration Helper for Server
# =============================================================================

class RerankerMixin:
    """
    Mixin class to add re-ranking capability to search functions.

    Add this mixin to classes that perform searches and want to
    optionally re-rank results.

    Example:
        class SearchHandler(RerankerMixin):
            def __init__(self):
                self.init_reranker()

            def search(self, query: str) -> list[dict]:
                results = self._vector_search(query)
                return self.rerank_if_enabled(query, results)
    """

    _reranker: Optional[ClaudeReranker] = None
    _reranker_config: Optional[RerankerConfig] = None

    def init_reranker(
        self,
        config: Optional[RerankerConfig] = None,
        enabled: bool = True
    ) -> None:
        """
        Initialize the re-ranker.

        Args:
            config: Optional custom configuration
            enabled: Enable/disable re-ranking
        """
        if config:
            self._reranker_config = config
        else:
            self._reranker_config = RerankerConfig(enabled=enabled)

        if self._reranker_config.enabled and is_reranking_available():
            self._reranker = ClaudeReranker(self._reranker_config)
            logger.info("Re-ranker initialized")
        else:
            self._reranker = None
            logger.info("Re-ranker not available or disabled")

    def rerank_if_enabled(
        self,
        query: str,
        chunks: list[dict[str, Any]],
        top_k: Optional[int] = None
    ) -> list[dict[str, Any]]:
        """
        Re-rank chunks if re-ranking is enabled.

        Args:
            query: Search query
            chunks: Search results
            top_k: Override default top_k

        Returns:
            Re-ranked or original chunks
        """
        if self._reranker is None:
            return chunks

        # Override top_k if specified
        if top_k is not None:
            original_top_k = self._reranker.config.top_k
            self._reranker.config.top_k = top_k
            try:
                return self._reranker.rerank_sync(query, chunks)
            finally:
                self._reranker.config.top_k = original_top_k

        return self._reranker.rerank_sync(query, chunks)

    async def rerank_if_enabled_async(
        self,
        query: str,
        chunks: list[dict[str, Any]],
        top_k: Optional[int] = None
    ) -> list[dict[str, Any]]:
        """
        Async version of rerank_if_enabled.
        """
        if self._reranker is None:
            return chunks

        if top_k is not None:
            original_top_k = self._reranker.config.top_k
            self._reranker.config.top_k = top_k
            try:
                return await self._reranker.rerank_async(query, chunks)
            finally:
                self._reranker.config.top_k = original_top_k

        return await self._reranker.rerank_async(query, chunks)


# =============================================================================
# Test/Demo Code
# =============================================================================

if __name__ == "__main__":
    # Configure logging for testing
    logging.basicConfig(
        level=logging.DEBUG,
        format='%(asctime)s | %(levelname)-8s | %(name)s | %(message)s'
    )

    print("=" * 60)
    print("Claude Headless Re-ranker Test")
    print("=" * 60)

    # Check availability
    print(f"\nClaude CLI available: {is_reranking_available()}")

    # Create test chunks
    test_chunks = [
        {
            "id": "chunk_001",
            "content": "UART initialization requires enabling the peripheral clock via RCC.",
            "metadata": {"peripheral": "UART", "source_file": "uart_guide.md", "has_code": False},
            "score": 0.85
        },
        {
            "id": "chunk_002",
            "content": "DMA configuration for UART receive mode. Configure DMA stream with peripheral-to-memory direction.",
            "metadata": {"peripheral": "DMA", "source_file": "dma_guide.md", "has_code": True},
            "score": 0.82
        },
        {
            "id": "chunk_003",
            "content": "HAL_UART_Receive_DMA() function starts DMA-based UART reception. Parameters: huart, pData, Size.",
            "metadata": {"peripheral": "UART", "source_file": "hal_uart.md", "has_code": True},
            "score": 0.80
        },
        {
            "id": "chunk_004",
            "content": "GPIO configuration basics. Each pin can be configured as input, output, alternate function, or analog.",
            "metadata": {"peripheral": "GPIO", "source_file": "gpio_guide.md", "has_code": False},
            "score": 0.75
        },
        {
            "id": "chunk_005",
            "content": "UART DMA circular mode example code for continuous reception without CPU intervention.",
            "metadata": {"peripheral": "UART", "source_file": "examples.md", "has_code": True},
            "score": 0.70
        },
    ]

    query = "How to configure UART DMA receive?"

    print(f"\nTest query: {query}")
    print(f"Number of chunks: {len(test_chunks)}")

    # Test re-ranker
    if is_reranking_available():
        print("\n--- Testing Re-ranker ---")
        config = RerankerConfig(top_k=3)
        reranker = ClaudeReranker(config)

        print("\nOriginal order:")
        for i, chunk in enumerate(test_chunks):
            print(f"  {i+1}. {chunk['id']} (score: {chunk['score']}) - {chunk['content'][:50]}...")

        print("\nRe-ranking...")
        reranked = reranker.rerank_sync(query, test_chunks)

        print(f"\nRe-ranked order (top {config.top_k}):")
        for i, chunk in enumerate(reranked):
            print(f"  {i+1}. {chunk['id']} (score: {chunk['score']}) - {chunk['content'][:50]}...")
    else:
        print("\nClaude CLI not available - skipping re-rank test")
        print("Install Claude Code CLI and log in to test re-ranking")

    print("\n" + "=" * 60)
    print("Test complete")
