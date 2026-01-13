"""Dense vector retriever implementation."""

from typing import Any

from sage.libs.rag.interface import Document, RetrievalResult, Retriever


class DenseRetriever(Retriever):
    """Dense vector retriever using embeddings.

    Args:
        embedding_model: Model for generating embeddings.
        vector_store: Vector store backend (e.g., SageVDB, FAISS).
        top_k: Default number of results to return.

    Example:
        >>> from sage_libs.sage_rag import DenseRetriever
        >>> retriever = DenseRetriever(embedding_model=model, vector_store=store)
        >>> results = retriever.retrieve("What is RAG?")
    """

    def __init__(
        self,
        embedding_model: Any = None,
        vector_store: Any = None,
        top_k: int = 5,
    ):
        self.embedding_model = embedding_model
        self.vector_store = vector_store
        self.top_k = top_k
        self._documents: list[Document] = []
        self._embeddings: list[list[float]] = []

    def retrieve(
        self, query: str, top_k: int | None = None, **kwargs: Any
    ) -> list[RetrievalResult]:
        """Retrieve relevant documents.

        Args:
            query: Search query.
            top_k: Number of results (default: self.top_k).
            **kwargs: Additional search parameters.

        Returns:
            List of retrieval results with scores.
        """
        k = top_k or self.top_k

        if self.vector_store is not None:
            # Use vector store for retrieval
            return self._retrieve_from_store(query, k, **kwargs)

        # Fallback to in-memory search
        return self._retrieve_in_memory(query, k)

    def index(self, documents: list[Document], **kwargs: Any) -> None:
        """Index documents for retrieval.

        Args:
            documents: Documents to index.
            **kwargs: Indexing parameters.
        """
        if self.vector_store is not None:
            # Index to vector store
            for doc in documents:
                embedding = self._get_embedding(doc.content)
                self.vector_store.add(embedding, metadata={"content": doc.content, **doc.metadata})
            self.vector_store.build_index()
        else:
            # In-memory indexing
            for doc in documents:
                embedding = self._get_embedding(doc.content)
                self._documents.append(doc)
                self._embeddings.append(embedding)

    def add_documents(self, documents: list[Document]) -> None:
        """Add documents to the retrieval index.

        Args:
            documents: Documents to index
        """
        self.index(documents)

    def delete_documents(self, doc_ids: list[str]) -> None:
        """Delete documents from the index.

        Args:
            doc_ids: List of document IDs to delete
        """
        if self.vector_store is not None:
            # Delete from vector store
            for doc_id in doc_ids:
                self.vector_store.delete(doc_id)
        else:
            # In-memory deletion
            indices_to_remove = []
            for i, doc in enumerate(self._documents):
                if doc.metadata.get("id") in doc_ids or doc.metadata.get("source") in doc_ids:
                    indices_to_remove.append(i)

            # Remove in reverse order to maintain indices
            for i in reversed(indices_to_remove):
                del self._documents[i]
                del self._embeddings[i]

    def _retrieve_from_store(self, query: str, top_k: int, **kwargs: Any) -> list[RetrievalResult]:
        """Retrieve from vector store.

        Args:
            query: Search query.
            top_k: Number of results.
            **kwargs: Additional parameters.

        Returns:
            Retrieval results.
        """
        query_embedding = self._get_embedding(query)
        results = self.vector_store.search(query_embedding, k=top_k)

        retrieval_results = []
        for i, result in enumerate(results):
            doc = Document(
                content=result.metadata.get("content", ""),
                metadata=result.metadata,
            )
            retrieval_results.append(RetrievalResult(document=doc, score=result.score, rank=i + 1))

        return retrieval_results

    def _retrieve_in_memory(self, query: str, top_k: int) -> list[RetrievalResult]:
        """Retrieve from in-memory index.

        Args:
            query: Search query.
            top_k: Number of results.

        Returns:
            Retrieval results.
        """
        if not self._documents:
            return []

        query_embedding = self._get_embedding(query)

        # Compute similarities
        scores = []
        for i, doc_embedding in enumerate(self._embeddings):
            score = self._cosine_similarity(query_embedding, doc_embedding)
            scores.append((i, score))

        # Sort by score
        scores.sort(key=lambda x: x[1], reverse=True)

        # Return top-k
        results = []
        for rank, (idx, score) in enumerate(scores[:top_k], 1):
            results.append(
                RetrievalResult(
                    document=self._documents[idx],
                    score=score,
                    rank=rank,
                )
            )

        return results

    def _get_embedding(self, text: str) -> list[float]:
        """Get embedding for text.

        Args:
            text: Text to embed.

        Returns:
            Embedding vector.
        """
        if self.embedding_model is None:
            # Simple hash-based pseudo-embedding
            return [
                hash(text[i : i + 10]) % 1000 / 1000.0 for i in range(0, min(100, len(text)), 10)
            ]

        # Use embedding model
        return self.embedding_model.encode(text).tolist()

    def _cosine_similarity(self, vec1: list[float], vec2: list[float]) -> float:
        """Compute cosine similarity.

        Args:
            vec1: First vector.
            vec2: Second vector.

        Returns:
            Cosine similarity score.
        """
        if len(vec1) != len(vec2):
            return 0.0

        dot_product = sum(a * b for a, b in zip(vec1, vec2, strict=True))
        norm1 = sum(a * a for a in vec1) ** 0.5
        norm2 = sum(b * b for b in vec2) ** 0.5

        if norm1 == 0 or norm2 == 0:
            return 0.0

        return dot_product / (norm1 * norm2)
