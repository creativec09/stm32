"""
BM25 Index for STM32 Documentation.

Provides keyword-based retrieval to complement vector search.
Uses custom tokenization optimized for STM32 technical terminology.
"""

import re
import logging
from typing import Optional
from dataclasses import dataclass, field

try:
    from rank_bm25 import BM25Okapi
    HAS_BM25 = True
except ImportError:
    HAS_BM25 = False
    BM25Okapi = None

logger = logging.getLogger(__name__)


class STM32Tokenizer:
    """
    Custom tokenizer for STM32 technical documentation.

    Handles:
    - Preserving technical terms (HAL_GPIO_Init, STM32F4, GPIOx_MODER)
    - Case normalization with exceptions for important acronyms
    - Register names and peripheral identifiers
    - Underscore-separated identifiers
    """

    # Patterns to preserve as single tokens (case-sensitive)
    PRESERVE_PATTERNS = [
        r'HAL_[A-Z][A-Za-z0-9_]+',       # HAL functions: HAL_GPIO_Init
        r'LL_[A-Z][A-Za-z0-9_]+',         # LL functions: LL_GPIO_SetPinMode
        r'__HAL_[A-Z_]+',                 # HAL macros: __HAL_RCC_GPIOA_CLK_ENABLE
        r'STM32[A-Z][0-9]+[A-Za-z0-9]*',  # STM32 families: STM32F407, STM32H743
        r'GPIO[A-Z]',                     # GPIO ports: GPIOA, GPIOB
        r'[A-Z]+[0-9]*_[A-Z]+[0-9]*',     # Registers: GPIOx_MODER, USART_CR1, TIM1_CCR1
        r'0x[0-9A-Fa-f]+',                # Hex values: 0x40020000
    ]

    # Common stopwords for technical documentation
    STOPWORDS = frozenset({
        'the', 'a', 'an', 'is', 'are', 'was', 'were', 'be', 'been',
        'being', 'have', 'has', 'had', 'do', 'does', 'did', 'will',
        'would', 'could', 'should', 'may', 'might', 'must', 'shall',
        'can', 'to', 'of', 'in', 'for', 'on', 'with', 'at', 'by',
        'from', 'as', 'into', 'through', 'during', 'before', 'after',
        'above', 'below', 'between', 'under', 'again', 'further',
        'then', 'once', 'here', 'there', 'when', 'where', 'why',
        'how', 'all', 'each', 'few', 'more', 'most', 'other', 'some',
        'such', 'no', 'nor', 'not', 'only', 'own', 'same', 'so',
        'than', 'too', 'very', 'just', 'and', 'but', 'if', 'or',
        'because', 'until', 'while', 'this', 'that', 'these', 'those',
        'it', 'its', 'you', 'your', 'we', 'our', 'they', 'their',
    })

    # Technical terms to always keep (lowercased for matching)
    KEEP_TERMS = frozenset({
        'gpio', 'uart', 'usart', 'spi', 'i2c', 'adc', 'dac', 'dma',
        'tim', 'timer', 'pwm', 'nvic', 'exti', 'rcc', 'can', 'usb',
        'hal', 'll', 'init', 'config', 'enable', 'disable', 'clock',
        'interrupt', 'callback', 'transmit', 'receive', 'read', 'write',
        'pin', 'port', 'mode', 'speed', 'pull', 'alternate', 'output',
        'input', 'register', 'bit', 'flag', 'status', 'error', 'timeout',
        'baud', 'baudrate', 'frequency', 'prescaler', 'channel', 'stream',
    })

    def __init__(self):
        # Compile patterns for efficiency
        self._preserve_pattern = re.compile(
            '|'.join(f'({p})' for p in self.PRESERVE_PATTERNS)
        )

    def tokenize(self, text: str) -> list[str]:
        """
        Tokenize text for BM25 indexing.

        Preserves technical terms while normalizing general text.

        Args:
            text: Input text to tokenize

        Returns:
            List of tokens
        """
        if not text:
            return []

        tokens = []

        # Extract and preserve technical terms first
        preserved_terms = []
        for match in self._preserve_pattern.finditer(text):
            term = match.group()
            preserved_terms.append(term)
            tokens.append(term.lower())  # Add lowercased version

        # Also add the original case version for exact matching
        tokens.extend(preserved_terms)

        # Tokenize the rest normally
        # Split on whitespace and punctuation (but keep underscores in words)
        words = re.findall(r'\b[a-zA-Z_][a-zA-Z0-9_]*\b', text.lower())

        for word in words:
            # Skip stopwords unless they're technical terms
            if word in self.STOPWORDS and word not in self.KEEP_TERMS:
                continue
            # Skip very short words
            if len(word) < 2:
                continue
            tokens.append(word)

        # Deduplicate while preserving order
        seen = set()
        unique_tokens = []
        for token in tokens:
            if token not in seen:
                seen.add(token)
                unique_tokens.append(token)

        return unique_tokens


@dataclass
class BM25Index:
    """
    BM25 index for STM32 documentation chunks.

    Maintains an in-memory BM25 index that can be built from ChromaDB
    documents and searched alongside vector search.

    Example:
        >>> index = BM25Index()
        >>> index.build_from_documents([("id1", "GPIO configuration..."), ...])
        >>> results = index.search("HAL_GPIO_Init", n_results=5)
    """

    tokenizer: STM32Tokenizer = field(default_factory=STM32Tokenizer)
    _index: Optional[BM25Okapi] = field(default=None, repr=False)
    _doc_ids: list[str] = field(default_factory=list)
    _documents: dict[str, str] = field(default_factory=dict, repr=False)
    _tokenized_corpus: list[list[str]] = field(default_factory=list, repr=False)
    _is_built: bool = False

    def __post_init__(self):
        if not HAS_BM25:
            logger.warning(
                "rank_bm25 not installed. BM25 search will be disabled. "
                "Install with: pip install rank-bm25"
            )

    def build_from_documents(
        self,
        documents: list[tuple[str, str]]
    ) -> bool:
        """
        Build BM25 index from documents.

        Args:
            documents: List of (doc_id, content) tuples

        Returns:
            True if index was built successfully
        """
        if not HAS_BM25:
            logger.error("Cannot build BM25 index: rank_bm25 not installed")
            return False

        if not documents:
            logger.warning("No documents provided for BM25 index")
            return False

        logger.info(f"Building BM25 index from {len(documents)} documents...")

        self._doc_ids = []
        self._documents = {}
        self._tokenized_corpus = []

        for doc_id, content in documents:
            self._doc_ids.append(doc_id)
            self._documents[doc_id] = content
            tokens = self.tokenizer.tokenize(content)
            self._tokenized_corpus.append(tokens)

        # Build BM25 index
        self._index = BM25Okapi(self._tokenized_corpus)
        self._is_built = True

        logger.info(f"BM25 index built with {len(self._doc_ids)} documents")
        return True

    def add_documents(self, documents: list[tuple[str, str]]) -> bool:
        """
        Add documents to existing index (requires rebuild).

        For efficiency with large additions, consider batching.

        Args:
            documents: List of (doc_id, content) tuples

        Returns:
            True if successful
        """
        if not HAS_BM25:
            return False

        for doc_id, content in documents:
            if doc_id not in self._documents:
                self._doc_ids.append(doc_id)
            self._documents[doc_id] = content

        # Rebuild index with all documents
        all_docs = [(doc_id, self._documents[doc_id]) for doc_id in self._doc_ids]
        return self.build_from_documents(all_docs)

    def search(
        self,
        query: str,
        n_results: int = 10,
        min_score: float = 0.0
    ) -> list[tuple[str, float]]:
        """
        Search the BM25 index.

        Args:
            query: Search query
            n_results: Number of results to return
            min_score: Minimum BM25 score threshold

        Returns:
            List of (doc_id, bm25_score) tuples, sorted by score descending
        """
        if not self._is_built or not HAS_BM25:
            logger.warning("BM25 index not available, returning empty results")
            return []

        query_tokens = self.tokenizer.tokenize(query)

        if not query_tokens:
            logger.debug(f"No tokens extracted from query: {query}")
            return []

        # Get BM25 scores for all documents
        scores = self._index.get_scores(query_tokens)

        # Create (doc_id, score) pairs and sort
        scored_docs = [
            (self._doc_ids[i], float(scores[i]))
            for i in range(len(scores))
            if scores[i] > min_score
        ]
        scored_docs.sort(key=lambda x: x[1], reverse=True)

        return scored_docs[:n_results]

    def get_document(self, doc_id: str) -> Optional[str]:
        """Get document content by ID."""
        return self._documents.get(doc_id)

    @property
    def is_built(self) -> bool:
        """Check if index has been built."""
        return self._is_built and HAS_BM25

    @property
    def document_count(self) -> int:
        """Get number of indexed documents."""
        return len(self._doc_ids)

    def clear(self) -> None:
        """Clear the index."""
        self._index = None
        self._doc_ids = []
        self._documents = {}
        self._tokenized_corpus = []
        self._is_built = False


def create_bm25_index(tokenizer: Optional[STM32Tokenizer] = None) -> BM25Index:
    """
    Factory function to create a BM25 index.

    Args:
        tokenizer: Optional custom tokenizer

    Returns:
        BM25Index instance
    """
    if tokenizer:
        return BM25Index(tokenizer=tokenizer)
    return BM25Index()
