"""Regression tests for issue #4 pipeline boundary cleanup."""

from __future__ import annotations

from typing import Any

import pytest
from sage_rag.interface import Document, RetrievalResult
from sage_libs.sage_rag.pipelines.simple import SimpleRAGPipeline


class _MockLoader:
    def load(self, source: str, **_kwargs: Any) -> Document:
        return Document(content=f"content for {source}", metadata={"source": source})


class _MockRetriever:
    def __init__(self) -> None:
        self._documents: list[Document] = []

    def index(self, documents: list[Document], **_kwargs: Any) -> None:
        self._documents = list(documents)

    def retrieve(self, _query: str, top_k: int, **_kwargs: Any) -> list[RetrievalResult]:
        return [
            RetrievalResult(document=doc, score=1.0 - (idx * 0.1), rank=idx + 1)
            for idx, doc in enumerate(self._documents[:top_k])
        ]


class _MockGenerator:
    def generate(self, prompt: str) -> str:
        return f"generated::{len(prompt)}"


class _InvalidGenerator:
    pass


def test_pipeline_has_single_index_entrypoint() -> None:
    assert hasattr(SimpleRAGPipeline, "index_documents")
    assert not hasattr(SimpleRAGPipeline, "index")


def test_pipeline_requires_loader_at_init() -> None:
    with pytest.raises(ValueError, match="Loader required"):
        SimpleRAGPipeline(loader=None, retriever=_MockRetriever(), generator=_MockGenerator())


def test_pipeline_requires_retriever_at_init() -> None:
    with pytest.raises(ValueError, match="Retriever required"):
        SimpleRAGPipeline(loader=_MockLoader(), retriever=None, generator=_MockGenerator())


def test_pipeline_requires_generator_at_init() -> None:
    with pytest.raises(ValueError, match="Generator required"):
        SimpleRAGPipeline(loader=_MockLoader(), retriever=_MockRetriever(), generator=None)


def test_index_documents_returns_stats_and_marks_indexed() -> None:
    pipeline = SimpleRAGPipeline(
        loader=_MockLoader(),
        retriever=_MockRetriever(),
        generator=_MockGenerator(),
    )

    stats = pipeline.index_documents(["a.txt", "b.txt"])

    assert stats == {"num_docs": 2, "num_chunks": 2, "indexed": True}


def test_query_fail_fast_for_invalid_generator_contract() -> None:
    pipeline = SimpleRAGPipeline(
        loader=_MockLoader(),
        retriever=_MockRetriever(),
        generator=_InvalidGenerator(),
    )
    pipeline.index_documents(["a.txt"])

    with pytest.raises(TypeError, match=r"generate\(prompt\)"):
        pipeline.query("what is rag")


def test_query_returns_contract_payload() -> None:
    pipeline = SimpleRAGPipeline(
        loader=_MockLoader(),
        retriever=_MockRetriever(),
        generator=_MockGenerator(),
    )
    pipeline.index_documents(["a.txt", "b.txt"])

    response = pipeline.query("what is rag", top_k=1)

    assert set(response.keys()) == {"answer", "sources", "metadata"}
    assert isinstance(response["answer"], str)
    assert len(response["sources"]) == 1
    assert response["metadata"]["top_k"] == 1
    assert response["metadata"]["num_results"] == 1
    assert response["metadata"]["indexed"] is True
