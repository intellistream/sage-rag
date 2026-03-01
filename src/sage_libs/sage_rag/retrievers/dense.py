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
        if self.vector_store is None:
            raise ValueError("DenseRetriever requires a configured vector_store")

        k = top_k or self.top_k
        return self._retrieve_from_store(query, k, **kwargs)

    def index(self, documents: list[Document], **kwargs: Any) -> None:
        """Index documents for retrieval.

        Args:
            documents: Documents to index.
            **kwargs: Indexing parameters.
        """
        if self.vector_store is None:
            raise ValueError("DenseRetriever requires a configured vector_store")

        for doc in documents:
            embedding = self._get_embedding(doc.content)
            self.vector_store.add(embedding, metadata={"content": doc.content, **doc.metadata})
        self.vector_store.build_index()

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
        if self.vector_store is None:
            raise ValueError("DenseRetriever requires a configured vector_store")

        for doc_id in doc_ids:
            self.vector_store.delete(doc_id)

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

    def _get_embedding(self, text: str) -> list[float]:
        """Get embedding for text.

        Args:
            text: Text to embed.

        Returns:
            Embedding vector.
        """
        if self.embedding_model is None:
            raise ValueError("DenseRetriever requires a configured embedding_model")

        # Use embedding model
        return self.embedding_model.encode(text).tolist()
