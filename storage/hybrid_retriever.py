"""
Hybrid Retriever combining BM25 and Vector Search with Reciprocal Rank Fusion.

This module provides a hybrid search approach that combines the strengths of:
- BM25 (keyword matching): Excellent for exact terms, function names, register names
- Vector search (semantic matching): Great for conceptual queries, synonyms

Results are combined using Reciprocal Rank Fusion (RRF) which is robust to
score scale differences between ranking methods.
"""

import logging
from dataclasses import dataclass, field
from typing import Optional

from .bm25_index import BM25Index, create_bm25_index
from .chroma_store import STM32ChromaStore
from .metadata import DocType, Peripheral


logger = logging.getLogger(__name__)


def reciprocal_rank_fusion(
    rankings: list[list[tuple[str, float]]],
    k: int = 60
) -> list[tuple[str, float]]:
    """
    Combine multiple rankings using Reciprocal Rank Fusion (RRF).

    RRF score = sum(1 / (k + rank_i)) for each ranking where document appears.

    This method is robust to:
    - Different score scales between rankers
    - Outliers in individual rankings
    - Missing documents in some rankings

    The k parameter (typically 60) prevents documents ranked first from
    dominating too heavily.

    Args:
        rankings: List of rankings, each is a list of (doc_id, score) tuples
                  sorted by score descending
        k: Ranking constant (industry standard is 60)

    Returns:
        Combined ranking as list of (doc_id, rrf_score) tuples, sorted descending

    Example:
        >>> rankings = [
        ...     [("doc1", 0.9), ("doc2", 0.8), ("doc3", 0.7)],  # Vector search
        ...     [("doc2", 5.0), ("doc1", 4.0), ("doc4", 3.0)],  # BM25
        ... ]
        >>> combined = reciprocal_rank_fusion(rankings)
        >>> # doc2 ranked high in both, will be at top
    """
    if not rankings:
        return []

    # Accumulate RRF scores for each document
    rrf_scores: dict[str, float] = {}

    for ranking in rankings:
        for rank, (doc_id, _score) in enumerate(ranking, start=1):
            if doc_id not in rrf_scores:
                rrf_scores[doc_id] = 0.0
            rrf_scores[doc_id] += 1.0 / (k + rank)

    # Sort by RRF score descending
    sorted_results = sorted(
        rrf_scores.items(),
        key=lambda x: x[1],
        reverse=True
    )

    return sorted_results


@dataclass
class HybridSearchConfig:
    """
    Configuration for hybrid search behavior.

    Attributes:
        rrf_k: RRF constant (default 60, industry standard)
        enable_hybrid: Whether to use hybrid search (False = vector only)
        min_bm25_score: Minimum BM25 score to include in fusion
        candidate_multiplier: Fetch this many more candidates for fusion
                              (e.g., 2.0 means fetch 2x n_results from each method)
    """

    rrf_k: int = 60
    enable_hybrid: bool = True
    min_bm25_score: float = 0.1
    candidate_multiplier: float = 2.0


@dataclass
class HybridRetriever:
    """
    Hybrid retriever combining BM25 and vector search.

    Lazily builds a BM25 index from ChromaDB documents on first use,
    then uses RRF to combine BM25 and vector search results.

    Example:
        >>> from storage import STM32ChromaStore
        >>> from storage.hybrid_retriever import HybridRetriever, HybridSearchConfig
        >>>
        >>> store = STM32ChromaStore(Path("./data/chroma_db"))
        >>> retriever = HybridRetriever(store)
        >>>
        >>> # Hybrid search (combines BM25 + vector)
        >>> results = retriever.search("HAL_GPIO_Init configuration", n_results=5)
        >>>
        >>> # Vector-only search
        >>> results = retriever.search_vector_only("GPIO setup", n_results=5)
        >>>
        >>> # BM25-only search
        >>> results = retriever.search_keyword_only("HAL_GPIO_Init", n_results=5)
    """

    store: STM32ChromaStore
    config: HybridSearchConfig = field(default_factory=HybridSearchConfig)
    _bm25_index: Optional[BM25Index] = field(default=None, repr=False)
    _index_built: bool = field(default=False, repr=False)
    _doc_metadata: dict[str, dict] = field(default_factory=dict, repr=False)

    def ensure_bm25_index(self) -> bool:
        """
        Lazily build BM25 index from ChromaDB documents.

        Fetches all documents from ChromaDB and builds the BM25 index.
        Only runs once; subsequent calls return immediately.

        Returns:
            True if index is available, False if build failed
        """
        if self._index_built:
            return self._bm25_index is not None and self._bm25_index.is_built

        logger.info("Building BM25 index from ChromaDB documents...")

        try:
            # Get all documents from ChromaDB
            # Using the internal collection to fetch all documents
            results = self.store._collection.get()

            if not results["ids"]:
                logger.warning("No documents in ChromaDB to build BM25 index from")
                self._index_built = True
                return False

            # Build document list for BM25
            documents: list[tuple[str, str]] = []
            for i in range(len(results["ids"])):
                doc_id = results["ids"][i]
                content = results["documents"][i]
                metadata = results["metadatas"][i] if results["metadatas"] else {}

                documents.append((doc_id, content))
                self._doc_metadata[doc_id] = metadata

            # Create and build BM25 index
            self._bm25_index = create_bm25_index()
            success = self._bm25_index.build_from_documents(documents)

            self._index_built = True

            if success:
                logger.info(
                    f"BM25 index built with {self._bm25_index.document_count} documents"
                )
            else:
                logger.warning("Failed to build BM25 index")

            return success

        except Exception as e:
            logger.error(f"Error building BM25 index: {e}")
            self._index_built = True
            return False

    def _apply_metadata_filter(
        self,
        doc_ids: list[str],
        peripheral: Optional[Peripheral] = None,
        doc_type: Optional[DocType] = None,
        require_code: bool = False
    ) -> list[str]:
        """
        Filter document IDs based on metadata criteria.

        Args:
            doc_ids: List of document IDs to filter
            peripheral: Filter by peripheral type
            doc_type: Filter by document type
            require_code: Only include documents with code examples

        Returns:
            Filtered list of document IDs
        """
        if not peripheral and not doc_type and not require_code:
            return doc_ids

        filtered = []
        for doc_id in doc_ids:
            metadata = self._doc_metadata.get(doc_id, {})

            # Check peripheral filter
            if peripheral:
                doc_peripheral = metadata.get("peripheral", "")
                if doc_peripheral != peripheral.value:
                    continue

            # Check doc_type filter
            if doc_type:
                doc_doc_type = metadata.get("doc_type", "")
                if doc_doc_type != doc_type.value:
                    continue

            # Check require_code filter
            if require_code:
                has_code = metadata.get("has_code", False)
                if not has_code:
                    continue

            filtered.append(doc_id)

        return filtered

    def search(
        self,
        query: str,
        n_results: int = 5,
        peripheral: Optional[Peripheral] = None,
        doc_type: Optional[DocType] = None,
        require_code: bool = False
    ) -> list[dict]:
        """
        Perform hybrid search combining BM25 and vector search.

        Uses Reciprocal Rank Fusion to combine results from both methods.
        Falls back to vector-only search if BM25 is unavailable.

        Args:
            query: Search query text
            n_results: Number of results to return
            peripheral: Filter by peripheral type
            doc_type: Filter by document type
            require_code: Only return chunks with code examples

        Returns:
            List of result dictionaries with keys: id, content, metadata, score
            Score is the RRF score (higher is better, max depends on fusion)
        """
        if not self.config.enable_hybrid:
            return self.search_vector_only(
                query, n_results, peripheral, doc_type, require_code
            )

        # Ensure BM25 index is built
        bm25_available = self.ensure_bm25_index()

        if not bm25_available:
            logger.debug("BM25 not available, falling back to vector-only search")
            return self.search_vector_only(
                query, n_results, peripheral, doc_type, require_code
            )

        # Calculate number of candidates to fetch from each method
        n_candidates = int(n_results * self.config.candidate_multiplier)

        # Get BM25 results
        bm25_results = self._bm25_index.search(
            query,
            n_results=n_candidates * 2,  # Fetch more since we'll filter
            min_score=self.config.min_bm25_score
        )

        # Apply metadata filters to BM25 results
        if peripheral or doc_type or require_code:
            bm25_doc_ids = [doc_id for doc_id, _ in bm25_results]
            filtered_ids = set(self._apply_metadata_filter(
                bm25_doc_ids, peripheral, doc_type, require_code
            ))
            bm25_results = [
                (doc_id, score)
                for doc_id, score in bm25_results
                if doc_id in filtered_ids
            ][:n_candidates]

        # Get vector search results
        vector_results = self.store.search(
            query,
            n_results=n_candidates,
            peripheral=peripheral,
            doc_type=doc_type,
            require_code=require_code
        )

        # Convert vector results to ranking format
        vector_ranking = [
            (result["id"], result["score"])
            for result in vector_results
        ]

        # Combine rankings with RRF
        rankings = [bm25_results, vector_ranking]
        combined = reciprocal_rank_fusion(rankings, k=self.config.rrf_k)

        # Get top n_results
        top_results = combined[:n_results]

        # Fetch full documents for results
        results = []
        for doc_id, rrf_score in top_results:
            # Try to get from store
            doc = self.store.get_by_id(doc_id)
            if doc:
                doc["score"] = rrf_score
                results.append(doc)
            else:
                # Fallback: get content from BM25 index
                content = self._bm25_index.get_document(doc_id)
                metadata = self._doc_metadata.get(doc_id, {})
                if content:
                    results.append({
                        "id": doc_id,
                        "content": content,
                        "metadata": metadata,
                        "score": rrf_score
                    })

        logger.debug(
            f"Hybrid search: {len(bm25_results)} BM25 + {len(vector_results)} vector "
            f"-> {len(results)} combined results"
        )

        return results

    def search_keyword_only(
        self,
        query: str,
        n_results: int = 5,
        peripheral: Optional[Peripheral] = None,
        doc_type: Optional[DocType] = None,
        require_code: bool = False
    ) -> list[dict]:
        """
        Perform BM25 keyword-only search.

        Useful for debugging or when you specifically want keyword matching
        (e.g., exact function names, register names).

        Args:
            query: Search query text
            n_results: Number of results to return
            peripheral: Filter by peripheral type
            doc_type: Filter by document type
            require_code: Only return chunks with code examples

        Returns:
            List of result dictionaries with keys: id, content, metadata, score
            Score is the BM25 score
        """
        # Ensure BM25 index is built
        if not self.ensure_bm25_index():
            logger.warning("BM25 index not available")
            return []

        # Fetch more results to account for filtering
        fetch_multiplier = 3 if (peripheral or doc_type or require_code) else 1
        bm25_results = self._bm25_index.search(
            query,
            n_results=n_results * fetch_multiplier,
            min_score=self.config.min_bm25_score
        )

        # Apply metadata filters
        if peripheral or doc_type or require_code:
            bm25_doc_ids = [doc_id for doc_id, _ in bm25_results]
            filtered_ids = set(self._apply_metadata_filter(
                bm25_doc_ids, peripheral, doc_type, require_code
            ))
            bm25_results = [
                (doc_id, score)
                for doc_id, score in bm25_results
                if doc_id in filtered_ids
            ]

        # Limit to n_results
        bm25_results = bm25_results[:n_results]

        # Fetch full documents
        results = []
        for doc_id, bm25_score in bm25_results:
            doc = self.store.get_by_id(doc_id)
            if doc:
                doc["score"] = bm25_score
                results.append(doc)
            else:
                content = self._bm25_index.get_document(doc_id)
                metadata = self._doc_metadata.get(doc_id, {})
                if content:
                    results.append({
                        "id": doc_id,
                        "content": content,
                        "metadata": metadata,
                        "score": bm25_score
                    })

        return results

    def search_vector_only(
        self,
        query: str,
        n_results: int = 5,
        peripheral: Optional[Peripheral] = None,
        doc_type: Optional[DocType] = None,
        require_code: bool = False
    ) -> list[dict]:
        """
        Perform vector-only semantic search.

        Useful for debugging or when you specifically want semantic matching
        (e.g., conceptual queries, finding similar content).

        Args:
            query: Search query text
            n_results: Number of results to return
            peripheral: Filter by peripheral type
            doc_type: Filter by document type
            require_code: Only return chunks with code examples

        Returns:
            List of result dictionaries with keys: id, content, metadata, score
            Score is the cosine similarity (0-1)
        """
        return self.store.search(
            query,
            n_results=n_results,
            peripheral=peripheral,
            doc_type=doc_type,
            require_code=require_code
        )

    def get_stats(self) -> dict:
        """
        Get statistics about the hybrid retriever.

        Returns:
            Dictionary with retriever statistics
        """
        stats = {
            "hybrid_enabled": self.config.enable_hybrid,
            "rrf_k": self.config.rrf_k,
            "min_bm25_score": self.config.min_bm25_score,
            "candidate_multiplier": self.config.candidate_multiplier,
            "bm25_index_built": self._index_built,
        }

        if self._bm25_index and self._bm25_index.is_built:
            stats["bm25_document_count"] = self._bm25_index.document_count

        store_stats = self.store.get_stats()
        stats["vector_store"] = store_stats

        return stats

    def rebuild_bm25_index(self) -> bool:
        """
        Force rebuild of the BM25 index.

        Use this after adding new documents to ChromaDB.

        Returns:
            True if rebuild was successful
        """
        self._index_built = False
        self._bm25_index = None
        self._doc_metadata = {}
        return self.ensure_bm25_index()


def create_hybrid_retriever(
    store: STM32ChromaStore,
    config: Optional[HybridSearchConfig] = None
) -> HybridRetriever:
    """
    Factory function to create a HybridRetriever.

    Args:
        store: STM32ChromaStore instance
        config: Optional search configuration

    Returns:
        Configured HybridRetriever instance
    """
    if config is None:
        config = HybridSearchConfig()
    return HybridRetriever(store=store, config=config)


# Test code
if __name__ == "__main__":
    import tempfile
    from pathlib import Path

    from .metadata import ChunkMetadataSchema

    # Configure logging
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )

    print("Testing HybridRetriever...")
    print("=" * 60)

    with tempfile.TemporaryDirectory() as tmpdir:
        # Initialize store
        print("\n1. Initializing ChromaDB store...")
        store = STM32ChromaStore(Path(tmpdir))

        # Create test documents
        print("\n2. Adding test documents...")
        test_docs = [
            (
                "gpio_001",
                "HAL_GPIO_Init configures GPIO pins. Set GPIO_MODE_OUTPUT_PP for push-pull output. "
                "The GPIO_MODER register controls pin mode. Enable clock with __HAL_RCC_GPIOA_CLK_ENABLE.",
                ChunkMetadataSchema(
                    source_file="gpio_guide.md",
                    doc_type=DocType.HAL_GUIDE,
                    peripheral=Peripheral.GPIO,
                    has_code=True,
                    hal_functions=["HAL_GPIO_Init"],
                    registers=["GPIO_MODER"]
                ).to_chroma_metadata()
            ),
            (
                "uart_001",
                "UART configuration for serial communication. Use HAL_UART_Transmit to send data. "
                "Configure baud rate in USART_BRR register. Enable UART clock first.",
                ChunkMetadataSchema(
                    source_file="uart_guide.md",
                    doc_type=DocType.HAL_GUIDE,
                    peripheral=Peripheral.UART,
                    has_code=True,
                    hal_functions=["HAL_UART_Transmit"],
                    registers=["USART_BRR"]
                ).to_chroma_metadata()
            ),
            (
                "dma_001",
                "DMA transfers data without CPU intervention. Configure stream and channel. "
                "Use HAL_DMA_Start for blocking or HAL_DMA_Start_IT for interrupt mode.",
                ChunkMetadataSchema(
                    source_file="dma_guide.md",
                    doc_type=DocType.HAL_GUIDE,
                    peripheral=Peripheral.DMA,
                    has_code=False,
                    hal_functions=["HAL_DMA_Start", "HAL_DMA_Start_IT"]
                ).to_chroma_metadata()
            ),
        ]

        store.add_chunks(test_docs)

        # Create hybrid retriever
        print("\n3. Creating hybrid retriever...")
        retriever = HybridRetriever(store=store)

        # Test hybrid search
        print("\n4. Testing hybrid search for 'GPIO configuration'...")
        results = retriever.search("GPIO configuration", n_results=3)
        print(f"Found {len(results)} results:")
        for i, result in enumerate(results, 1):
            print(f"  {i}. [{result['id']}] score={result['score']:.4f}")
            print(f"     {result['content'][:80]}...")

        # Test keyword-only search
        print("\n5. Testing BM25-only search for 'HAL_GPIO_Init'...")
        results = retriever.search_keyword_only("HAL_GPIO_Init", n_results=3)
        print(f"Found {len(results)} results:")
        for i, result in enumerate(results, 1):
            print(f"  {i}. [{result['id']}] score={result['score']:.4f}")

        # Test vector-only search
        print("\n6. Testing vector-only search for 'serial communication'...")
        results = retriever.search_vector_only("serial communication", n_results=3)
        print(f"Found {len(results)} results:")
        for i, result in enumerate(results, 1):
            print(f"  {i}. [{result['id']}] score={result['score']:.4f}")

        # Test with peripheral filter
        print("\n7. Testing hybrid search with peripheral filter (UART)...")
        results = retriever.search(
            "data transfer",
            n_results=3,
            peripheral=Peripheral.UART
        )
        print(f"Found {len(results)} results:")
        for i, result in enumerate(results, 1):
            peripheral = result['metadata'].get('peripheral', 'N/A')
            print(f"  {i}. [{result['id']}] peripheral={peripheral}")

        # Test with require_code filter
        print("\n8. Testing hybrid search with require_code=True...")
        results = retriever.search("configuration", n_results=3, require_code=True)
        print(f"Found {len(results)} results (all should have code):")
        for i, result in enumerate(results, 1):
            has_code = result['metadata'].get('has_code', False)
            print(f"  {i}. [{result['id']}] has_code={has_code}")

        # Get stats
        print("\n9. Getting retriever stats...")
        stats = retriever.get_stats()
        print(f"  Hybrid enabled: {stats['hybrid_enabled']}")
        print(f"  RRF k: {stats['rrf_k']}")
        print(f"  BM25 index built: {stats['bm25_index_built']}")
        print(f"  BM25 documents: {stats.get('bm25_document_count', 'N/A')}")

        print("\n" + "=" * 60)
        print("All tests completed successfully!")
