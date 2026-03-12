"""
RAG (Retrieval-Augmented Generation) Operators

This module contains domain-specific operators for RAG applications:
- Pipeline (RAG orchestration and workflow)
- Profiler (Query profiling and analysis)
- Document Loaders (Document loading utilities)
- Generator operators (LLM response generation)
- Retriever operators (document/passage retrieval)
- Reranker operators (result reranking)
- Promptor operators (prompt construction)
- Evaluation operators (quality metrics)
- Document processing operators (chunking, refining, writing)
- External data source operators (ArXiv)

These operators inherit from the current SAGE base operator classes when needed
and implement RAG-specific business logic.
"""

# Export types for easier access
from sage_rag.types import (
    RAGDocument,
    RAGInput,
    RAGOutput,
    RAGQuery,
    RAGResponse,
    create_rag_response,
    ensure_rag_response,
    extract_query,
    extract_results,
)

# Lazy imports to avoid optional dependency issues
_IMPORTS = {
    # Pipeline and Profiler
    "RAGPipeline": ("sage_rag.operators.pipeline", "RAGPipeline"),
    "Query_Profiler": ("sage_rag.operators.profiler", "Query_Profiler"),
    "QueryProfilerResult": ("sage_rag.operators.profiler", "QueryProfilerResult"),
    # Document Loaders
    "TextLoader": ("sage_rag.operators.document_loaders", "TextLoader"),
    "PDFLoader": ("sage_rag.operators.document_loaders", "PDFLoader"),
    "DocxLoader": ("sage_rag.operators.document_loaders", "DocxLoader"),
    "DocLoader": ("sage_rag.operators.document_loaders", "DocLoader"),
    "MarkdownLoader": ("sage_rag.operators.document_loaders", "MarkdownLoader"),
    "LoaderFactory": ("sage_rag.operators.document_loaders", "LoaderFactory"),
    # Generators
    "OpenAIGenerator": ("sage_rag.operators.generator", "OpenAIGenerator"),
    "HFGenerator": ("sage_rag.operators.generator", "HFGenerator"),
    "SageLLMRAGGenerator": ("sage_rag.operators.generator", "SageLLMRAGGenerator"),
    # Retrievers
    "ChromaRetriever": ("sage_rag.operators.retriever", "ChromaRetriever"),
    "MilvusDenseRetriever": ("sage_rag.operators.retriever", "MilvusDenseRetriever"),
    "MilvusSparseRetriever": ("sage_rag.operators.retriever", "MilvusSparseRetriever"),
    "Wiki18FAISSRetriever": ("sage_rag.operators.retriever", "Wiki18FAISSRetriever"),
    # Rerankers
    "BGEReranker": ("sage_rag.operators.reranker", "BGEReranker"),
    "LLMbased_Reranker": ("sage_rag.operators.reranker", "LLMbased_Reranker"),
    # Promptors
    "QAPromptor": ("sage_rag.operators.promptor", "QAPromptor"),
    "SummarizationPromptor": ("sage_rag.operators.promptor", "SummarizationPromptor"),
    "QueryProfilerPromptor": ("sage_rag.operators.promptor", "QueryProfilerPromptor"),
    # Evaluation
    "F1Evaluate": ("sage_rag.operators.evaluate", "F1Evaluate"),
    "EMEvaluate": ("sage_rag.operators.evaluate", "EMEvaluate"),
    "RecallEvaluate": ("sage_rag.operators.evaluate", "RecallEvaluate"),
    "BertRecallEvaluate": ("sage_rag.operators.evaluate", "BertRecallEvaluate"),
    "RougeLEvaluate": ("sage_rag.operators.evaluate", "RougeLEvaluate"),
    "BRSEvaluate": ("sage_rag.operators.evaluate", "BRSEvaluate"),
    "AccuracyEvaluate": ("sage_rag.operators.evaluate", "AccuracyEvaluate"),
    "TokenCountEvaluate": ("sage_rag.operators.evaluate", "TokenCountEvaluate"),
    "LatencyEvaluate": ("sage_rag.operators.evaluate", "LatencyEvaluate"),
    "ContextRecallEvaluate": ("sage_rag.operators.evaluate", "ContextRecallEvaluate"),
    "CompressionRateEvaluate": ("sage_rag.operators.evaluate", "CompressionRateEvaluate"),
    # Document Processing
    "CharacterSplitter": ("sage_rag.operators.chunk", "CharacterSplitter"),
    "RefinerOperator": ("sage_rag.operators.refiner", "RefinerOperator"),
    "MemoryWriter": ("sage_rag.operators.writer", "MemoryWriter"),
    # External Data Sources (may require optional dependencies)
    "ArxivPDFDownloader": ("sage_rag.operators.arxiv", "ArxivPDFDownloader"),
    "ArxivPDFParser": ("sage_rag.operators.arxiv", "ArxivPDFParser"),
    # Web Search
    "BochaWebSearch": ("sage_rag.operators.searcher", "BochaWebSearch"),
    # Index Builder
    "IndexBuilder": ("sage_rag.operators.index_builder", "IndexBuilder"),
    "IndexManifest": ("sage_rag.operators.index_builder", "IndexManifest"),
    "VectorStore": ("sage_rag.operators.index_builder", "VectorStore"),
}

# Export all operator names and type utilities
__all__ = [  # type: ignore[misc]
    # Types
    "RAGDocument",
    "RAGQuery",
    "RAGResponse",
    "RAGInput",
    "RAGOutput",
    "ensure_rag_response",
    "extract_query",
    "extract_results",
    "create_rag_response",
    # Operators (lazy loaded)
    *list(_IMPORTS.keys()),
]


def __getattr__(name: str):
    """Lazy import to avoid optional dependency issues at import time."""
    if name in _IMPORTS:
        module_name, attr_name = _IMPORTS[name]
        import importlib

        module = importlib.import_module(module_name)
        return getattr(module, attr_name)
    raise AttributeError(f"module '{__name__}' has no attribute '{name}'")
