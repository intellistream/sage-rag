"""Auto-register implementations to the local RAG interface registry."""

from sage_libs.sage_rag.interface import (
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

# Register implementations in local registry.
register_loader("text", TextLoader)
register_loader("markdown", MarkdownLoader)

register_chunker("sentence", SentenceChunker)
register_chunker("token", TokenChunker)

register_retriever("dense", DenseRetriever)
register_reranker("cross_encoder", CrossEncoderReranker)
register_pipeline("simple", SimpleRAGPipeline)
