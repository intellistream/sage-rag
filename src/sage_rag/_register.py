"""Auto-register implementations to SAGE interface.

This module is imported in __init__.py to register all implementations
with the SAGE RAG interface factory.
"""

from sage.libs.rag.interface import (
    register_chunker,
    register_loader,
    register_pipeline,
    register_reranker,
    register_retriever,
)

from .chunkers import SentenceChunker, TokenChunker
from .loaders import MarkdownLoader, TextLoader
from .pipelines import SimpleRAGPipeline
from .rerankers import CrossEncoderReranker
from .retrievers import DenseRetriever

# ==================== Register Loaders ====================
register_loader("text", TextLoader)
register_loader("markdown", MarkdownLoader)

# ==================== Register Chunkers ====================
register_chunker("sentence", SentenceChunker)
register_chunker("token", TokenChunker)

# ==================== Register Retrievers ====================
register_retriever("dense", DenseRetriever)

# ==================== Register Rerankers ====================
register_reranker("cross_encoder", CrossEncoderReranker)

# ==================== Register Pipelines ====================
register_pipeline("simple", SimpleRAGPipeline)
