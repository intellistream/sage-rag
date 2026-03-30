"""Cross-encoder reranker implementation."""

from typing import Any

from sage_rag.interface import Reranker, RetrievalResult


class CrossEncoderReranker(Reranker):
    """Rerank results using cross-encoder model.

    Cross-encoders process query-document pairs together for more
    accurate relevance scoring than bi-encoders.

    Args:
        model: Cross-encoder model (e.g., sentence-transformers).
        top_k: Number of results to return after reranking.

    Example:
        >>> from sage_libs.sage_rag import CrossEncoderReranker
        >>> reranker = CrossEncoderReranker(model=cross_encoder)
        >>> reranked = reranker.rerank("query", results)
    """

    def __init__(self, model: Any, top_k: int | None = None):
        if model is None:
            raise ValueError("CrossEncoderReranker requires a configured model")
        self.model = model
        self.top_k = top_k

    def rerank(
        self,
        query: str,
        results: list[RetrievalResult],
        top_k: int | None = None,
        **kwargs: Any,
    ) -> list[RetrievalResult]:
        """Rerank retrieval results.

        Args:
            query: Original query.
            results: Initial retrieval results.
            top_k: Number of results to return.
            **kwargs: Additional parameters.

        Returns:
            Reranked results with updated scores.
        """
        if not results:
            return []

        k = top_k or self.top_k or len(results)
        return self._model_rerank(query, results, k)

    def _model_rerank(
        self, query: str, results: list[RetrievalResult], top_k: int
    ) -> list[RetrievalResult]:
        """Rerank using cross-encoder model.

        Args:
            query: Query string.
            results: Results to rerank.
            top_k: Number to return.

        Returns:
            Reranked results.
        """
        # Prepare query-document pairs
        pairs = [(query, r.document.content) for r in results]

        # Get cross-encoder scores
        scores = self.model.predict(pairs)

        # Create scored results
        scored = list(zip(results, scores, strict=True))
        scored.sort(key=lambda x: x[1], reverse=True)

        # Return top-k with updated scores and ranks
        reranked = []
        for rank, (result, score) in enumerate(scored[:top_k], 1):
            reranked.append(
                RetrievalResult(
                    document=result.document,
                    score=float(score),
                    rank=rank,
                )
            )

        return reranked
