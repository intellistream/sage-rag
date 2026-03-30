"""RAG Index Building Service (sage-rag operators)

This module provides index building functionality for RAG systems.
It orchestrates document processing, embedding, and vector storage.

Layer: sage-rag/operators
Dependencies:
  - sage.libs.rag (L2) - chunk, document_loaders
  - sage.common (L1) - utilities
  - Pluggable VectorStore backend (injected via factory)

Components:
- VectorStore: Protocol defining vector storage interface
- IndexManifest: Metadata describing a built index
- IndexBuilder: Service for building vector indices

Architecture Pattern:
- IndexBuilder uses dependency injection for backend
- sage-middleware provides SageDB backend implementation
- sage-rag/backends provides ChromaDB/Milvus implementations
- sage-cli uses IndexBuilder

Example Usage:
    >>> from sage_rag.operators.index_builder import IndexBuilder
    >>> from sage.middleware.components.sage_db import SageVDBBackend
    >>>
    >>> # Create backend factory
    >>> def factory(path, dim):
    ...     return SageVDBBackend(path, dim)
    >>>
    >>> # Build index
    >>> builder = IndexBuilder(backend_factory=factory)
    >>> manifest = builder.build_from_docs(
    ...     source_dir=Path("docs"),
    ...     persist_path=Path(".sage/index"),
    ...     embedding_model=embedder,
    ... )
"""

from sage_rag.operators.index_builder.builder import IndexBuilder
from sage_rag.operators.index_builder.manifest import IndexManifest
from sage_rag.operators.index_builder.storage import VectorStore

__all__ = [
    "IndexBuilder",
    "IndexManifest",
    "VectorStore",
]
