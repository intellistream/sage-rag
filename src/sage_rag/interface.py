"""Standalone RAG interfaces and registry helpers for ``sage-rag``."""

from __future__ import annotations

from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from typing import Any


@dataclass(slots=True)
class Document:
    """A loaded document with arbitrary metadata."""

    content: str
    metadata: dict[str, Any] = field(default_factory=dict)


@dataclass(slots=True)
class Chunk:
    """A text chunk emitted by a chunker."""

    content: str
    metadata: dict[str, Any] = field(default_factory=dict)
    start_pos: int | None = None
    end_pos: int | None = None

    @property
    def text(self) -> str:
        return self.content


@dataclass(slots=True)
class RetrievalResult:
    """A ranked retrieval result."""

    document: Document
    score: float
    rank: int


class DocumentLoader(ABC):
    """Base interface for document loaders."""

    @abstractmethod
    def load(self, source: str, **kwargs: Any) -> Document:
        """Load a single source into a document."""

    def load_batch(self, sources: list[str], **kwargs: Any) -> list[Document]:
        return [self.load(source, **kwargs) for source in sources]

    def supported_formats(self) -> list[str]:
        return []


class TextChunker(ABC):
    """Base interface for chunkers."""

    @abstractmethod
    def chunk(self, text: str, **kwargs: Any) -> list[Chunk]:
        """Split text into chunks."""

    def chunk_document(self, document: Document, **kwargs: Any) -> list[Chunk]:
        return self.chunk(document.content, **kwargs)

    def supported_formats(self) -> list[str]:
        return []


class Retriever(ABC):
    """Base interface for retrievers."""

    @abstractmethod
    def retrieve(
        self, query: str, top_k: int | None = None, **kwargs: Any
    ) -> list[RetrievalResult]:
        """Retrieve ranked documents for a query."""

    @abstractmethod
    def index(self, documents: list[Document], **kwargs: Any) -> None:
        """Index documents for retrieval."""


class Reranker(ABC):
    """Base interface for rerankers."""

    @abstractmethod
    def rerank(
        self,
        query: str,
        results: list[RetrievalResult],
        top_k: int | None = None,
        **kwargs: Any,
    ) -> list[RetrievalResult]:
        """Rerank retrieval results."""


class RAGPipeline(ABC):
    """Base interface for end-to-end RAG pipelines."""

    @abstractmethod
    def index_documents(self, sources: list[str], **kwargs: Any) -> dict[str, Any]:
        """Index sources into the pipeline."""

    @abstractmethod
    def query(self, query: str, top_k: int = 5, **kwargs: Any) -> dict[str, Any]:
        """Answer a user query."""


_LOADERS: dict[str, type[DocumentLoader]] = {}
_CHUNKERS: dict[str, type[TextChunker]] = {}
_RETRIEVERS: dict[str, type[Retriever]] = {}
_RERANKERS: dict[str, type[Reranker]] = {}
_PIPELINES: dict[str, type[RAGPipeline]] = {}


def register_loader(name: str, loader_cls: type[DocumentLoader]) -> None:
    _LOADERS[name] = loader_cls


def register_chunker(name: str, chunker_cls: type[TextChunker]) -> None:
    _CHUNKERS[name] = chunker_cls


def register_retriever(name: str, retriever_cls: type[Retriever]) -> None:
    _RETRIEVERS[name] = retriever_cls


def register_reranker(name: str, reranker_cls: type[Reranker]) -> None:
    _RERANKERS[name] = reranker_cls


def register_pipeline(name: str, pipeline_cls: type[RAGPipeline]) -> None:
    _PIPELINES[name] = pipeline_cls


def registered_loaders() -> list[str]:
    return sorted(_LOADERS)


def registered_chunkers() -> list[str]:
    return sorted(_CHUNKERS)


def registered_retrievers() -> list[str]:
    return sorted(_RETRIEVERS)


def registered_rerankers() -> list[str]:
    return sorted(_RERANKERS)


def registered_pipelines() -> list[str]:
    return sorted(_PIPELINES)


def _create(name: str, registry: dict[str, type[Any]], *args: Any, **kwargs: Any) -> Any:
    try:
        cls = registry[name]
    except KeyError as exc:
        raise ValueError(f"Unknown RAG component: {name}") from exc
    return cls(*args, **kwargs)


def create_loader(name: str, *args: Any, **kwargs: Any) -> DocumentLoader:
    return _create(name, _LOADERS, *args, **kwargs)


def create_chunker(name: str, *args: Any, **kwargs: Any) -> TextChunker:
    return _create(name, _CHUNKERS, *args, **kwargs)


def create_retriever(name: str, *args: Any, **kwargs: Any) -> Retriever:
    return _create(name, _RETRIEVERS, *args, **kwargs)


def create_reranker(name: str, *args: Any, **kwargs: Any) -> Reranker:
    return _create(name, _RERANKERS, *args, **kwargs)


def create_pipeline(name: str, *args: Any, **kwargs: Any) -> RAGPipeline:
    return _create(name, _PIPELINES, *args, **kwargs)


__all__ = [
    "Chunk",
    "Document",
    "DocumentLoader",
    "RAGPipeline",
    "Reranker",
    "RetrievalResult",
    "Retriever",
    "TextChunker",
    "create_chunker",
    "create_loader",
    "create_pipeline",
    "create_reranker",
    "create_retriever",
    "register_chunker",
    "register_loader",
    "register_pipeline",
    "register_reranker",
    "register_retriever",
    "registered_chunkers",
    "registered_loaders",
    "registered_pipelines",
    "registered_rerankers",
    "registered_retrievers",
]
