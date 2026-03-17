"""
Embedding providers for STM32 MCP Documentation Server.

Uses the Voyage 4 model family via the Voyage AI API:
- voyage-4-large: Document indexing (highest quality, one-time cost)
- voyage-4-lite: Query embeddings (fast, cheap, same embedding space)

All Voyage 4 models share an embedding space, enabling asymmetric retrieval:
index with large, query with lite. No local model hosting needed.
"""

import logging
from typing import Protocol, runtime_checkable

logger = logging.getLogger(__name__)


@runtime_checkable
class EmbeddingProvider(Protocol):
    """Protocol for embedding providers."""

    def embed_documents(self, texts: list[str]) -> list[list[float]]:
        """Embed a list of documents for indexing."""
        ...

    def embed_query(self, text: str) -> list[float]:
        """Embed a single query for search."""
        ...

    @property
    def dimensions(self) -> int:
        """Return the embedding dimensionality."""
        ...


class VoyageAPIProvider:
    """
    Voyage AI API provider for embeddings.

    Supports asymmetric retrieval: use model="voyage-4-large" for indexing
    and model="voyage-4-lite" for queries, or the same model for both.
    """

    def __init__(
        self,
        api_key: str,
        model: str = "voyage-4-large",
        query_model: str | None = None,
        output_dimensions: int = 1024,
        batch_size: int = 64,
    ):
        import voyageai

        self._client = voyageai.Client(api_key=api_key)
        self._model = model
        self._query_model = query_model or model
        self._dimensions = output_dimensions
        self._batch_size = batch_size
        logger.info(
            f"VoyageAPIProvider initialized: index={model}, "
            f"query={self._query_model}, dims={output_dimensions}"
        )

    def embed_documents(self, texts: list[str]) -> list[list[float]]:
        """Embed documents using Voyage AI API with batching."""
        all_embeddings: list[list[float]] = []

        for i in range(0, len(texts), self._batch_size):
            batch = texts[i : i + self._batch_size]
            result = self._client.embed(
                batch,
                model=self._model,
                input_type="document",
                output_dimension=self._dimensions,
            )
            all_embeddings.extend(result.embeddings)

            if len(texts) > self._batch_size:
                logger.info(
                    f"Embedded batch {i // self._batch_size + 1}/"
                    f"{(len(texts) - 1) // self._batch_size + 1}"
                )

        return all_embeddings

    def embed_query(self, text: str) -> list[float]:
        """Embed a single query using the query model (voyage-4-lite by default)."""
        result = self._client.embed(
            [text],
            model=self._query_model,
            input_type="query",
            output_dimension=self._dimensions,
        )
        return result.embeddings[0]

    @property
    def dimensions(self) -> int:
        return self._dimensions


def create_provider(
    api_key: str | None = None,
    index_model: str = "voyage-4-large",
    query_model: str = "voyage-4-lite",
    dimensions: int = 1024,
    **_kwargs,
) -> VoyageAPIProvider:
    """
    Create a Voyage AI embedding provider.

    Uses asymmetric retrieval by default: voyage-4-large for indexing,
    voyage-4-lite for queries. Both share the same embedding space.

    Args:
        api_key: Voyage AI API key (required)
        index_model: Model for document indexing (default: voyage-4-large)
        query_model: Model for query embedding (default: voyage-4-lite)
        dimensions: Output embedding dimensions (default: 1024)

    Returns:
        Configured VoyageAPIProvider instance
    """
    if not api_key:
        raise ValueError(
            "VOYAGE_API_KEY is required. Set it in .env or as environment variable."
        )
    return VoyageAPIProvider(
        api_key=api_key,
        model=index_model,
        query_model=query_model,
        output_dimensions=dimensions,
    )
