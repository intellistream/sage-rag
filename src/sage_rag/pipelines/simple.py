"""Simple RAG pipeline implementation."""

from typing import Any

from sage.libs.rag.interface import (
    Document,
    DocumentLoader,
    RAGPipeline,
    Reranker,
    RetrievalResult,
    Retriever,
    TextChunker,
)


class SimpleRAGPipeline(RAGPipeline):
    """Simple RAG pipeline for basic retrieval-augmented generation.

    Orchestrates the full RAG workflow:
    1. Load documents
    2. Chunk documents
    3. Index chunks
    4. Retrieve relevant chunks
    5. (Optional) Rerank results
    6. Generate response

    Args:
        loader: Document loader.
        chunker: Text chunker.
        retriever: Document retriever.
        reranker: Optional reranker.
        generator: LLM for response generation.

    Example:
        >>> from sage_libs.sage_rag import SimpleRAGPipeline, TextLoader, SentenceChunker, DenseRetriever
        >>> pipeline = SimpleRAGPipeline(
        ...     loader=TextLoader(),
        ...     chunker=SentenceChunker(),
        ...     retriever=DenseRetriever(embedding_model=embedding_model, vector_store=vector_store),
        ...     generator=generator,
        ... )
        >>> _ = pipeline.index_documents(["doc1.txt", "doc2.txt"])
        >>> response = pipeline.query("What is RAG?")
        >>> print(response["answer"])
    """

    def __init__(
        self,
        loader: DocumentLoader,
        retriever: Retriever,
        generator: Any,
        chunker: TextChunker | None = None,
        reranker: Reranker | None = None,
        top_k: int = 5,
    ):
        if loader is None:
            raise ValueError("Loader required for pipeline initialization")
        if retriever is None:
            raise ValueError("Retriever required for pipeline initialization")
        if generator is None:
            raise ValueError("Generator required for pipeline initialization")
        self.loader = loader
        self.chunker = chunker
        self.retriever = retriever
        self.reranker = reranker
        self.generator = generator
        self.top_k = top_k
        self._indexed = False

    def configure(self, **config: Any) -> None:
        """Configure pipeline components.

        Args:
            **config: Configuration options (loader, chunker, retriever, etc.)
        """
        if "loader" in config:
            if config["loader"] is None:
                raise ValueError("Loader cannot be None")
            self.loader = config["loader"]
        if "chunker" in config:
            self.chunker = config["chunker"]
        if "retriever" in config:
            if config["retriever"] is None:
                raise ValueError("Retriever cannot be None")
            self.retriever = config["retriever"]
        if "reranker" in config:
            self.reranker = config["reranker"]
        if "generator" in config:
            if config["generator"] is None:
                raise ValueError("Generator cannot be None")
            self.generator = config["generator"]
        if "top_k" in config:
            self.top_k = config["top_k"]

    def index_documents(self, sources: list[str], **kwargs: Any) -> dict[str, Any]:
        """Index documents into the RAG system.

        Args:
            sources: Document sources (file paths, URLs, etc.)
            **kwargs: Pipeline-specific options

        Returns:
            Indexing statistics (num_docs, num_chunks, etc.)
        """
        documents, num_docs = self._collect_documents(sources, **kwargs)
        self.retriever.index(documents, **kwargs)
        self._indexed = True

        return {
            "num_docs": num_docs,
            "num_chunks": len(documents),
            "indexed": True,
        }

    def query(self, query: str, top_k: int = 5, **kwargs: Any) -> dict[str, Any]:
        """Query the RAG pipeline.

        Args:
            query: User query.
            top_k: Number of contexts to retrieve.
            **kwargs: Additional parameters.

        Returns:
            RAG response payload containing answer, sources, and metadata.
        """
        k = top_k
        results = self.retrieve(query, k, **kwargs)
        context = self._build_context(results)
        answer = self._generate_response(query, context)

        return {
            "answer": answer,
            "sources": [result.document for result in results],
            "metadata": {
                "top_k": k,
                "num_results": len(results),
                "indexed": self._indexed,
            },
        }

    def retrieve(
        self, query: str, top_k: int | None = None, **kwargs: Any
    ) -> list[RetrievalResult]:
        """Retrieve relevant documents.

        Args:
            query: Search query.
            top_k: Number of results.
            **kwargs: Additional parameters.

        Returns:
            List of retrieval results.
        """
        k = top_k if top_k is not None else self.top_k
        results = self.retriever.retrieve(query, top_k=k, **kwargs)

        # Rerank if reranker available
        if self.reranker is not None:
            results = self.reranker.rerank(query, results, top_k=k, **kwargs)

        return results

    def _build_context(self, results: list[RetrievalResult]) -> str:
        """Build context string from retrieval results.

        Args:
            results: Retrieval results.

        Returns:
            Formatted context string.
        """
        if not results:
            return "No relevant documents found."

        context_parts = []
        for i, result in enumerate(results, 1):
            source = result.document.metadata.get("source", "unknown")
            context_parts.append(
                f"[{i}] (score: {result.score:.3f}, source: {source})\n{result.document.content}"
            )

        return "\n\n".join(context_parts)

    def _generate_response(self, question: str, context: str) -> str:
        """Generate response using LLM.

        Args:
            question: User question.
            context: Retrieved context.

        Returns:
            Generated response.
        """
        prompt = f"""Answer the following question based on the provided context.

Context:
{context}

Question: {question}

Answer:"""

        generate_fn = getattr(self.generator, "generate", None)
        if not callable(generate_fn):
            raise TypeError("Generator must provide callable generate(prompt) method")

        return generate_fn(prompt)

    def _collect_documents(self, sources: list[str], **kwargs: Any) -> tuple[list[Document], int]:
        """Load and chunk documents from sources."""
        documents: list[Document] = []

        for source in sources:
            doc = self.loader.load(source, **kwargs)

            if self.chunker is None:
                documents.append(doc)
                continue

            chunks = self.chunker.chunk(doc.content, **kwargs)
            for chunk in chunks:
                chunk_doc = Document(
                    content=chunk.text,
                    metadata={
                        **doc.metadata,
                        "chunk_index": chunk.metadata.get("chunk_index", 0),
                        "start_pos": chunk.start_pos,
                        "end_pos": chunk.end_pos,
                    },
                )
                documents.append(chunk_doc)

        return documents, len(sources)
