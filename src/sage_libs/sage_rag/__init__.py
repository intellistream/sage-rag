"""SAGE RAG - Retrieval-Augmented Generation implementations.

This package provides concrete implementations for:
- Document Loaders (TextLoader, PDFLoader, DocxLoader, DocLoader, MarkdownLoader)
- Text Chunkers (CharacterChunker, SentenceChunker, TokenChunker, TransformerTokenChunker)
- Retrievers (DenseRetriever, SparseRetriever)
- Rerankers (CrossEncoderReranker)
- RAG Pipelines (SimpleRAGPipeline)

Usage:
    # Direct import
    from sage_libs.sage_rag import TextLoader, SimpleRAGPipeline

    # Or via SAGE factory (after import triggers registration)
    import sage_rag  # triggers auto-registration
    from sage.libs.rag.interface import create_loader, create_pipeline
    loader = create_loader("text")
    pipeline = create_pipeline("simple")

Installation:
    pip install isage-rag
"""

# Auto-register implementations to SAGE interface
from . import _register  # noqa: F401
from ._version import __author__, __email__, __version__
from .chunkers import CharacterChunker, SentenceChunker, TokenChunker, TransformerTokenChunker

# Public component exports
from .loaders import DocLoader, DocxLoader, LoaderFactory, MarkdownLoader, PDFLoader, TextLoader
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
    "PDFLoader",
    "DocxLoader",
    "DocLoader",
    "LoaderFactory",
    # Chunkers
    "CharacterChunker",
    "SentenceChunker",
    "TokenChunker",
    "TransformerTokenChunker",
    # Retrievers
    "DenseRetriever",
    # Rerankers
    "CrossEncoderReranker",
    # Pipelines
    "SimpleRAGPipeline",
]
