"""SAGE RAG - Retrieval-Augmented Generation implementations.

This package provides concrete implementations for:
- Document Loaders (TextLoader, PDFLoader, MarkdownLoader)
- Text Chunkers (SentenceChunker, TokenChunker)
- Retrievers (DenseRetriever, SparseRetriever)
- Rerankers (CrossEncoderReranker)
- RAG Pipelines (SimpleRAGPipeline)

Usage:
    # Direct import
    from sage_libs.sage_rag import TextLoader, SimpleRAGPipeline

    # Or via SAGE factory (after import triggers registration)
    import sage_rag  # triggers auto-registration
    from sage.libs.rag.interface import create_loader, create_retriever, create_pipeline
    loader = create_loader("text")
    retriever = create_retriever(
        "dense",
        embedding_model=embedding_model,
        vector_store=vector_store,
    )
    pipeline = create_pipeline("simple", loader=loader, retriever=retriever, generator=generator)

Installation:
    pip install isage-rag
"""

# Auto-register implementations to SAGE interface
from . import _register  # noqa: F401
from ._version import __author__, __email__, __version__
from .chunkers import SentenceChunker, TokenChunker

# Public component exports
from .loaders import MarkdownLoader, TextLoader
from .pipelines import SimpleRAGPipeline
from .rerankers import CrossEncoderReranker
from .retrievers import DenseRetriever

__all__ = [
    # Version info
    "__version__",
    "__author__",
    "__email__",
    # Loaders
    "TextLoader",
    "MarkdownLoader",
    # Chunkers
    "SentenceChunker",
    "TokenChunker",
    # Retrievers
    "DenseRetriever",
    # Rerankers
    "CrossEncoderReranker",
    # Pipelines
    "SimpleRAGPipeline",
]
