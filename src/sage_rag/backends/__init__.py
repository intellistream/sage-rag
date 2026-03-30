"""Vector store backends for sage-rag.

This module provides adapters for various vector databases used by RAG pipelines:
- ChromaDB (local-persistent and HTTP client modes)
- Milvus / Milvus Lite (local .db and remote server modes)

Usage::

    from sage_rag.backends import ChromaBackend, ChromaUtils
    from sage_rag.backends import MilvusBackend, MilvusUtils
    from sage_rag.backends import ChromaVectorStoreAdapter

Optional dependencies:
    - chromadb      (for Chroma backends):  pip install isage-rag[chroma]
    - pymilvus      (for Milvus backends):  pip install isage-rag[milvus]
"""

from sage_rag.backends.chroma import ChromaBackend, ChromaUtils
from sage_rag.backends.chroma_adapter import ChromaVectorStoreAdapter
from sage_rag.backends.milvus import MilvusBackend, MilvusUtils

__all__ = [
    "ChromaBackend",
    "ChromaUtils",
    "ChromaVectorStoreAdapter",
    "MilvusBackend",
    "MilvusUtils",
]
