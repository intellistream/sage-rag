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
        ...     retriever=DenseRetriever(),
        ... )
        >>> pipeline.index(["doc1.txt", "doc2.txt"])
        >>> response = pipeline.query("What is RAG?")
    """

    def __init__(
        self,
        loader: DocumentLoader | None = None,
        chunker: TextChunker | None = None,
        retriever: Retriever | None = None,
        reranker: Reranker | None = None,
        generator: Any = None,
        top_k: int = 5,
    ):
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
            self.loader = config["loader"]
        if "chunker" in config:
            self.chunker = config["chunker"]
        if "retriever" in config:
            self.retriever = config["retriever"]
        if "reranker" in config:
            self.reranker = config["reranker"]
        if "generator" in config:
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
        if self.loader is None or self.retriever is None:
            raise ValueError("Loader and retriever required for indexing")

        all_chunks = []
        num_docs = 0

        for source in sources:
            # Load document
            doc = self.loader.load(source, **kwargs)
            num_docs += 1

            # Chunk if chunker available
            if self.chunker is not None:
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
                    all_chunks.append(chunk_doc)
            else:
                all_chunks.append(doc)

        # Index all chunks
        self.retriever.index(all_chunks, **kwargs)
        self._indexed = True

        return {
            "num_docs": num_docs,
            "num_chunks": len(all_chunks),
            "indexed": True,
        }

    def index(self, sources: list[str], **kwargs: Any) -> None:
        """Index documents from sources.

        Args:
            sources: List of document sources (file paths, URLs, etc.).
            **kwargs: Additional indexing parameters.
        """
        if self.loader is None or self.retriever is None:
            raise ValueError("Loader and retriever required for indexing")

        all_chunks = []

        for source in sources:
            # Load document
            doc = self.loader.load(source, **kwargs)

            # Chunk if chunker available
            if self.chunker is not None:
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
                    all_chunks.append(chunk_doc)
            else:
                all_chunks.append(doc)

        # Index all chunks
        self.retriever.index(all_chunks, **kwargs)
        self._indexed = True

    def query(self, question: str, top_k: int | None = None, **kwargs: Any) -> str:
        """Query the RAG pipeline.

        Args:
            question: User question.
            top_k: Number of contexts to retrieve.
            **kwargs: Additional parameters.

        Returns:
            Generated response.
        """
        k = top_k or self.top_k

        # Retrieve relevant documents
        results = self.retrieve(question, k, **kwargs)

        # Build context from results
        context = self._build_context(results)

        # Generate response
        if self.generator is not None:
            return self._generate_response(question, context)

        # Without generator, return context summary
        return f"Retrieved {len(results)} relevant documents:\n\n{context}"

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
        if self.retriever is None:
            return []

        k = top_k or self.top_k
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

        # Call generator (assumed to have a generate or __call__ method)
        if hasattr(self.generator, "generate"):
            return self.generator.generate(prompt)
        elif callable(self.generator):
            return self.generator(prompt)
        else:
            return f"Generator not configured. Context:\n{context}"
