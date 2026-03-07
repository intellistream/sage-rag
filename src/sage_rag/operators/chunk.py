"""RAG chunking operators.

Re-exports ``CharacterSplitter`` from ``sage.libs.rag.chunk``.
"""

from sage.libs.rag.chunk import (  # noqa: F401
    CharacterSplitter,
)

__all__ = ["CharacterSplitter"]
