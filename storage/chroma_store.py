"""
ChromaDB wrapper for STM32 documentation storage and retrieval.

This module provides a high-level interface for storing and searching STM32
documentation chunks using ChromaDB as the vector database backend.
"""

import logging
from pathlib import Path
from typing import Optional, Union

import chromadb
from chromadb.config import Settings as ChromaSettings
from sentence_transformers import SentenceTransformer

from .metadata import ChunkMetadataSchema, DocType, Peripheral, ContentType


logger = logging.getLogger(__name__)


class STM32ChromaStore:
    """
    ChromaDB wrapper for STM32 documentation.

    Provides methods for adding, searching, and managing STM32 documentation chunks
    with rich metadata filtering and semantic search capabilities.

    Example:
        >>> store = STM32ChromaStore(Path("./data/chroma"))
        >>> store.add_chunks([
        ...     ("chunk_001", "GPIO configuration text", metadata.to_chroma_metadata())
        ... ])
        >>> results = store.search("How to configure GPIO?", peripheral=Peripheral.GPIO)
    """

    def __init__(
        self,
        persist_dir: Path,
        collection_name: str = "stm32_docs",
        embedding_model: str = "all-MiniLM-L6-v2",
        distance_metric: str = "cosine"
    ):
        """
        Initialize the ChromaDB store.

        Args:
            persist_dir: Directory for persistent storage
            collection_name: Name of the ChromaDB collection
            embedding_model: Sentence transformer model name
            distance_metric: Distance metric for similarity search (cosine, l2, ip)
        """
        self.persist_dir = persist_dir
        self.collection_name = collection_name
        self.embedding_model_name = embedding_model
        self.distance_metric = distance_metric

        # Ensure persist directory exists
        self.persist_dir.mkdir(parents=True, exist_ok=True)

        # Initialize ChromaDB client with persistent storage
        self._client = chromadb.PersistentClient(
            path=str(self.persist_dir),
            settings=ChromaSettings(
                anonymized_telemetry=False,
                allow_reset=True,
            )
        )

        # Lazy load embedding model (loaded on first use)
        self._embedding_model: Optional[SentenceTransformer] = None

        # Get or create collection
        self._collection = self._client.get_or_create_collection(
            name=self.collection_name,
            metadata={"hnsw:space": self.distance_metric}
        )

        logger.info(
            f"Initialized STM32ChromaStore at {self.persist_dir} "
            f"with collection '{self.collection_name}'"
        )

    @property
    def embedding_model(self) -> SentenceTransformer:
        """Lazy load the embedding model."""
        if self._embedding_model is None:
            logger.info(f"Loading embedding model: {self.embedding_model_name}")
            self._embedding_model = SentenceTransformer(self.embedding_model_name)
        return self._embedding_model

    def _generate_embeddings(self, texts: list[str]) -> list[list[float]]:
        """Generate embeddings for a list of texts."""
        embeddings = self.embedding_model.encode(
            texts,
            show_progress_bar=len(texts) > 10,
            convert_to_numpy=True
        )
        return embeddings.tolist()

    # Maximum batch size for ChromaDB operations
    MAX_BATCH_SIZE = 5000  # ChromaDB limit is 5461, use 5000 for safety margin

    def add_chunks(
        self,
        chunks: list[tuple[str, str, dict]]  # (id, content, metadata)
    ) -> int:
        """
        Add chunks to the store.

        Automatically handles batching for large chunk lists to avoid
        exceeding ChromaDB's batch size limits.

        Args:
            chunks: List of (id, content, metadata) tuples

        Returns:
            Number of chunks added

        Example:
            >>> store.add_chunks([
            ...     ("chunk_001", "GPIO text", meta.to_chroma_metadata()),
            ...     ("chunk_002", "UART text", meta2.to_chroma_metadata())
            ... ])
            2
        """
        if not chunks:
            return 0

        total_added = 0

        # Process in batches to avoid ChromaDB size limits
        for i in range(0, len(chunks), self.MAX_BATCH_SIZE):
            batch = chunks[i:i + self.MAX_BATCH_SIZE]

            ids, documents, metadatas = zip(*batch)

            # Generate embeddings for this batch
            embeddings = self._generate_embeddings(list(documents))

            # Add batch to collection
            try:
                self._collection.add(
                    ids=list(ids),
                    documents=list(documents),
                    metadatas=list(metadatas),
                    embeddings=embeddings
                )
                total_added += len(batch)
                if len(chunks) > self.MAX_BATCH_SIZE:
                    logger.info(f"Added batch {i // self.MAX_BATCH_SIZE + 1}: {len(batch)} chunks")
            except Exception as e:
                logger.error(f"Failed to add chunks: {e}")
                raise

        logger.info(f"Added {total_added} chunks to collection")
        return total_added

    def search(
        self,
        query: str,
        n_results: int = 5,
        peripheral: Optional[Peripheral] = None,
        doc_type: Optional[DocType] = None,
        require_code: bool = False,
        require_register: bool = False,
        min_score: float = 0.0
    ) -> list[dict]:
        """
        Search for relevant chunks.

        Args:
            query: Search query text
            n_results: Maximum number of results to return
            peripheral: Filter by peripheral type
            doc_type: Filter by document type
            require_code: Only return chunks with code examples
            require_register: Only return chunks with register maps
            min_score: Minimum similarity score (0.0-1.0)

        Returns:
            List of result dictionaries with keys: id, content, metadata, score

        Example:
            >>> results = store.search(
            ...     "GPIO configuration",
            ...     peripheral=Peripheral.GPIO,
            ...     require_code=True
            ... )
        """
        # Build filter query using $and for multiple conditions
        filter_conditions = []
        if peripheral:
            filter_conditions.append({"peripheral": peripheral.value})
        if doc_type:
            filter_conditions.append({"doc_type": doc_type.value})
        if require_code:
            filter_conditions.append({"has_code": True})
        if require_register:
            filter_conditions.append({"has_register_map": True})

        # ChromaDB requires $and when there are multiple conditions
        if len(filter_conditions) == 0:
            where_filter = None
        elif len(filter_conditions) == 1:
            where_filter = filter_conditions[0]
        else:
            where_filter = {"$and": filter_conditions}

        # Generate query embedding
        query_embedding = self._generate_embeddings([query])[0]

        # Execute search
        try:
            results = self._collection.query(
                query_embeddings=[query_embedding],
                n_results=n_results,
                where=where_filter
            )

            # Format results
            formatted_results = []
            if results["ids"] and results["ids"][0]:
                for i in range(len(results["ids"][0])):
                    # ChromaDB returns distances, convert to similarity scores
                    # For cosine distance: similarity = 1 - distance
                    distance = results["distances"][0][i]
                    score = 1.0 - distance

                    if score >= min_score:
                        formatted_results.append({
                            "id": results["ids"][0][i],
                            "content": results["documents"][0][i],
                            "metadata": results["metadatas"][0][i],
                            "score": score
                        })

            logger.debug(f"Search returned {len(formatted_results)} results")
            return formatted_results

        except Exception as e:
            logger.error(f"Search failed: {e}")
            raise

    def search_by_peripheral(
        self,
        peripheral: Peripheral,
        query: str = "",
        n_results: int = 10
    ) -> list[dict]:
        """
        Get all documentation for a specific peripheral.

        Args:
            peripheral: Peripheral to search for
            query: Optional query to refine results
            n_results: Maximum number of results

        Returns:
            List of result dictionaries

        Example:
            >>> results = store.search_by_peripheral(Peripheral.GPIO)
        """
        if query:
            return self.search(
                query=query,
                n_results=n_results,
                peripheral=peripheral
            )
        else:
            # Get all chunks for this peripheral
            try:
                results = self._collection.get(
                    where={"peripheral": peripheral.value},
                    limit=n_results
                )

                formatted_results = []
                if results["ids"]:
                    for i in range(len(results["ids"])):
                        formatted_results.append({
                            "id": results["ids"][i],
                            "content": results["documents"][i],
                            "metadata": results["metadatas"][i],
                            "score": 1.0  # No relevance score for direct fetch
                        })

                return formatted_results
            except Exception as e:
                logger.error(f"Failed to get peripheral docs: {e}")
                raise

    def get_code_examples(
        self,
        topic: str,
        peripheral: Optional[Peripheral] = None,
        n_results: int = 5
    ) -> list[dict]:
        """
        Get code examples for a topic.

        Args:
            topic: Topic to search for
            peripheral: Optional peripheral filter
            n_results: Maximum number of results

        Returns:
            List of code example chunks

        Example:
            >>> examples = store.get_code_examples(
            ...     "initialization",
            ...     peripheral=Peripheral.GPIO
            ... )
        """
        return self.search(
            query=topic,
            n_results=n_results,
            peripheral=peripheral,
            require_code=True
        )

    def get_register_info(
        self,
        register_name: str,
        n_results: int = 3
    ) -> list[dict]:
        """
        Get register documentation.

        Args:
            register_name: Name of the register (e.g., "GPIO_MODER")
            n_results: Maximum number of results

        Returns:
            List of register documentation chunks

        Example:
            >>> results = store.get_register_info("GPIO_MODER")
        """
        return self.search(
            query=register_name,
            n_results=n_results,
            require_register=True
        )

    def search_hal_function(
        self,
        function_name: str,
        n_results: int = 5
    ) -> list[dict]:
        """
        Search for HAL function documentation.

        Args:
            function_name: HAL function name (e.g., "HAL_GPIO_Init")
            n_results: Maximum number of results

        Returns:
            List of documentation chunks mentioning the function

        Example:
            >>> results = store.search_hal_function("HAL_GPIO_Init")
        """
        # Search for the function name in content
        return self.search(
            query=function_name,
            n_results=n_results,
            doc_type=DocType.HAL_GUIDE
        )

    def get_by_id(self, chunk_id: str) -> Optional[dict]:
        """
        Get a specific chunk by ID.

        Args:
            chunk_id: Chunk identifier

        Returns:
            Chunk dictionary or None if not found

        Example:
            >>> chunk = store.get_by_id("chunk_001")
        """
        try:
            results = self._collection.get(ids=[chunk_id])
            if results["ids"]:
                return {
                    "id": results["ids"][0],
                    "content": results["documents"][0],
                    "metadata": results["metadatas"][0],
                    "score": 1.0
                }
            return None
        except Exception as e:
            logger.error(f"Failed to get chunk by ID: {e}")
            return None

    def get_by_ids(self, chunk_ids: list[str]) -> list[dict]:
        """
        Get multiple chunks by IDs.

        Args:
            chunk_ids: List of chunk identifiers

        Returns:
            List of chunk dictionaries

        Example:
            >>> chunks = store.get_by_ids(["chunk_001", "chunk_002"])
        """
        if not chunk_ids:
            return []

        try:
            results = self._collection.get(ids=chunk_ids)
            formatted_results = []
            if results["ids"]:
                for i in range(len(results["ids"])):
                    formatted_results.append({
                        "id": results["ids"][i],
                        "content": results["documents"][i],
                        "metadata": results["metadatas"][i],
                        "score": 1.0
                    })
            return formatted_results
        except Exception as e:
            logger.error(f"Failed to get chunks by IDs: {e}")
            return []

    def delete_by_source(self, source_file: str) -> int:
        """
        Delete all chunks from a source file.

        Args:
            source_file: Source filename to delete

        Returns:
            Number of chunks deleted

        Example:
            >>> deleted = store.delete_by_source("stm32f4_reference.md")
        """
        try:
            # Get all chunks from this source
            results = self._collection.get(
                where={"source_file": source_file}
            )

            if results["ids"]:
                self._collection.delete(ids=results["ids"])
                count = len(results["ids"])
                logger.info(f"Deleted {count} chunks from {source_file}")
                return count
            return 0
        except Exception as e:
            logger.error(f"Failed to delete chunks: {e}")
            raise

    def get_stats(self) -> dict:
        """
        Get collection statistics.

        Returns:
            Dictionary with statistics about the collection

        Example:
            >>> stats = store.get_stats()
            >>> print(f"Total chunks: {stats['total_chunks']}")
        """
        try:
            count = self._collection.count()
            return {
                "total_chunks": count,
                "collection_name": self.collection_name,
                "persist_dir": str(self.persist_dir),
                "embedding_model": self.embedding_model_name,
                "distance_metric": self.distance_metric
            }
        except Exception as e:
            logger.error(f"Failed to get stats: {e}")
            return {"error": str(e)}

    def get_peripheral_distribution(self) -> dict[str, int]:
        """
        Get count of chunks per peripheral.

        Returns:
            Dictionary mapping peripheral names to chunk counts

        Example:
            >>> dist = store.get_peripheral_distribution()
            >>> print(f"GPIO chunks: {dist.get('GPIO', 0)}")
        """
        distribution = {}
        try:
            # Get all chunks
            results = self._collection.get()
            if results["metadatas"]:
                for meta in results["metadatas"]:
                    peripheral = meta.get("peripheral", "GENERAL")
                    if peripheral:
                        distribution[peripheral] = distribution.get(peripheral, 0) + 1
        except Exception as e:
            logger.error(f"Failed to get peripheral distribution: {e}")

        return distribution

    def get_doc_type_distribution(self) -> dict[str, int]:
        """
        Get count of chunks per document type.

        Returns:
            Dictionary mapping document types to chunk counts

        Example:
            >>> dist = store.get_doc_type_distribution()
            >>> print(f"Reference manuals: {dist.get('reference_manual', 0)}")
        """
        distribution = {}
        try:
            # Get all chunks
            results = self._collection.get()
            if results["metadatas"]:
                for meta in results["metadatas"]:
                    doc_type = meta.get("doc_type", "general")
                    distribution[doc_type] = distribution.get(doc_type, 0) + 1
        except Exception as e:
            logger.error(f"Failed to get doc type distribution: {e}")

        return distribution

    def list_sources(self) -> list[str]:
        """
        List all source files in the collection.

        Returns:
            List of unique source filenames

        Example:
            >>> sources = store.list_sources()
        """
        sources = set()
        try:
            results = self._collection.get()
            if results["metadatas"]:
                for meta in results["metadatas"]:
                    source = meta.get("source_file")
                    if source:
                        sources.add(source)
        except Exception as e:
            logger.error(f"Failed to list sources: {e}")

        return sorted(sources)

    def clear(self) -> None:
        """
        Clear all data (use with caution).

        This deletes the entire collection and recreates it empty.

        Example:
            >>> store.clear()  # Deletes all data!
        """
        logger.warning(f"Clearing collection '{self.collection_name}'")
        try:
            self._client.delete_collection(name=self.collection_name)
            self._collection = self._client.create_collection(
                name=self.collection_name,
                metadata={"hnsw:space": self.distance_metric}
            )
            logger.info("Collection cleared successfully")
        except Exception as e:
            logger.error(f"Failed to clear collection: {e}")
            raise

    def count(self) -> int:
        """
        Get total number of chunks.

        Returns:
            Total chunk count

        Example:
            >>> total = store.count()
        """
        try:
            return self._collection.count()
        except Exception as e:
            logger.error(f"Failed to count chunks: {e}")
            return 0


# Test code
if __name__ == "__main__":
    from pathlib import Path
    import tempfile

    # Configure logging
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )

    print("Testing STM32ChromaStore...")
    print("=" * 60)

    with tempfile.TemporaryDirectory() as tmpdir:
        # Initialize store
        print("\n1. Initializing store...")
        store = STM32ChromaStore(Path(tmpdir))

        # Create test metadata
        print("\n2. Creating test chunk...")
        meta = ChunkMetadataSchema(
            source_file="test.md",
            doc_type=DocType.HAL_GUIDE,
            peripheral=Peripheral.GPIO,
            has_code=True,
            section_path=["GPIO", "Configuration"],
            hal_functions=["HAL_GPIO_Init", "HAL_GPIO_WritePin"],
            registers=["GPIO_MODER", "GPIO_ODR"]
        )

        # Add test chunk
        print("\n3. Adding chunk to store...")
        store.add_chunks([
            (
                "test_001",
                "Configure GPIO pin as output using HAL_GPIO_Init with GPIO_MODE_OUTPUT_PP. "
                "The GPIO_MODER register controls the mode of each pin. "
                "Use HAL_GPIO_WritePin to set the output state.",
                meta.to_chroma_metadata()
            )
        ])

        # Search
        print("\n4. Searching for 'GPIO configuration'...")
        results = store.search("GPIO configuration")
        print(f"Found {len(results)} results")
        if results:
            print(f"Top result score: {results[0]['score']:.3f}")
            print(f"Content: {results[0]['content'][:100]}...")

        # Search with filters
        print("\n5. Searching for code examples...")
        code_results = store.get_code_examples("GPIO initialization")
        print(f"Found {len(code_results)} code examples")

        # Get stats
        print("\n6. Getting collection statistics...")
        stats = store.get_stats()
        print(f"Total chunks: {stats['total_chunks']}")
        print(f"Collection: {stats['collection_name']}")
        print(f"Embedding model: {stats['embedding_model']}")

        # Get distributions
        print("\n7. Getting peripheral distribution...")
        peripheral_dist = store.get_peripheral_distribution()
        for peripheral, count in peripheral_dist.items():
            print(f"  {peripheral}: {count}")

        print("\n8. Getting document type distribution...")
        doc_dist = store.get_doc_type_distribution()
        for doc_type, count in doc_dist.items():
            print(f"  {doc_type}: {count}")

        # List sources
        print("\n9. Listing sources...")
        sources = store.list_sources()
        for source in sources:
            print(f"  {source}")

        print("\n" + "=" * 60)
        print("All tests completed successfully!")
