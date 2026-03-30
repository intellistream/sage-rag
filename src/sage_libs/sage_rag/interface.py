"""Local RAG interfaces and in-package registry.

This keeps the package self-contained after extraction from the SAGE monorepo.
"""

from __future__ import annotations

from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from typing import Any


@dataclass
class Document:
    content: str
    metadata: dict[str, Any] = field(default_factory=dict)


@dataclass
class Chunk:
    text: str
    start_pos: int
    end_pos: int
    metadata: dict[str, Any] = field(default_factory=dict)


@dataclass
class RetrievalResult:
    document: Document
    score: float
    rank: int


class DocumentLoader(ABC):
    @abstractmethod
    def load(self, source: str, **kwargs: Any) -> Document:
        raise NotImplementedError


class TextChunker(ABC):
    @abstractmethod
    def chunk(self, text: str, **kwargs: Any) -> list[Chunk]:
        raise NotImplementedError


class Retriever(ABC):
    @abstractmethod
    def retrieve(self, query: str, top_k: int | None = None, **kwargs: Any) -> list[RetrievalResult]:
        raise NotImplementedError


class Reranker(ABC):
    @abstractmethod
    def rerank(
        self,
        query: str,
        results: list[RetrievalResult],
        top_k: int | None = None,
        **kwargs: Any,
    ) -> list[RetrievalResult]:
        raise NotImplementedError


class RAGPipeline(ABC):
    @abstractmethod
    def query(self, question: str, top_k: int | None = None, **kwargs: Any) -> str:
        raise NotImplementedError


_LOADERS: dict[str, type[Any]] = {}
_CHUNKERS: dict[str, type[Any]] = {}
_RETRIEVERS: dict[str, type[Any]] = {}
_RERANKERS: dict[str, type[Any]] = {}
_PIPELINES: dict[str, type[Any]] = {}


def register_loader(name: str, impl: type[Any]) -> None:
    _LOADERS[name] = impl


def register_chunker(name: str, impl: type[Any]) -> None:
    _CHUNKERS[name] = impl


def register_retriever(name: str, impl: type[Any]) -> None:
    _RETRIEVERS[name] = impl


def register_reranker(name: str, impl: type[Any]) -> None:
    _RERANKERS[name] = impl


def register_pipeline(name: str, impl: type[Any]) -> None:
    _PIPELINES[name] = impl


def registered_loaders() -> list[str]:
    return sorted(_LOADERS.keys())


def registered_chunkers() -> list[str]:
    return sorted(_CHUNKERS.keys())


def registered_retrievers() -> list[str]:
    return sorted(_RETRIEVERS.keys())


def registered_rerankers() -> list[str]:
    return sorted(_RERANKERS.keys())


def registered_pipelines() -> list[str]:
    return sorted(_PIPELINES.keys())


def create_loader(name: str, **kwargs: Any) -> Any:
    return _LOADERS[name](**kwargs)


def create_chunker(name: str, **kwargs: Any) -> Any:
    return _CHUNKERS[name](**kwargs)


def create_retriever(name: str, **kwargs: Any) -> Any:
    return _RETRIEVERS[name](**kwargs)


def create_reranker(name: str, **kwargs: Any) -> Any:
    return _RERANKERS[name](**kwargs)


def create_pipeline(name: str, **kwargs: Any) -> Any:
    return _PIPELINES[name](**kwargs)
