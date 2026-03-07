"""isage-rag — Retrieval-Augmented Generation components.

Canonical import path::

    from sage_rag import TextLoader, SentenceChunker, SimpleRAGPipeline

Install::

    pip install isage-rag
"""

# Trigger optional registration with sage-libs factory if installed
from . import _register  # noqa: F401
from ._version import __author__, __email__, __version__
from .chunkers import CharacterChunker, SentenceChunker, TokenChunker, TransformerTokenChunker
from .loaders import DocLoader, DocxLoader, LoaderFactory, MarkdownLoader, PDFLoader, TextLoader
from .pipelines import SimpleRAGPipeline
from .rerankers import CrossEncoderReranker
from .retrievers import DenseRetriever

__all__ = [
    "__version__",
    "__author__",
    "__email__",
    "TextLoader",
    "MarkdownLoader",
    "PDFLoader",
    "DocxLoader",
    "DocLoader",
    "LoaderFactory",
    "CharacterChunker",
    "SentenceChunker",
    "TokenChunker",
    "TransformerTokenChunker",
    "DenseRetriever",
    "CrossEncoderReranker",
    "SimpleRAGPipeline",
]
