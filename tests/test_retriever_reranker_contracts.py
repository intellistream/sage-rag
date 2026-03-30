"""Contract tests for retriever/reranker behavior (issue #5)."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any

import pytest
from sage_rag.interface import Document, RetrievalResult
from sage_libs.sage_rag import CrossEncoderReranker, DenseRetriever


class _MockCrossEncoder:
    def __init__(self, scores: list[float]) -> None:
        self._scores = scores

    def predict(self, pairs: list[tuple[str, str]]) -> list[float]:
        assert len(pairs) == len(self._scores)
        return self._scores


class _MockEmbedding:
    def encode(self, text: str) -> _MockVector:
        tokens = text.lower().split()
        return _MockVector(
            [float("weather" in tokens), float("forecast" in tokens), float(len(tokens))]
        )


class _MockVector:
    def __init__(self, values: list[float]) -> None:
        self._values = values

    def tolist(self) -> list[float]:
        return self._values


@dataclass
class _StoreItem:
    metadata: dict[str, Any]
    score: float


class _MockVectorStore:
    def __init__(self) -> None:
        self._items: list[tuple[list[float], dict[str, Any]]] = []

    def add(self, embedding: list[float], metadata: dict[str, Any]) -> None:
        self._items.append((embedding, metadata))

    def build_index(self) -> None:
        return

    def search(self, query_embedding: list[float], k: int) -> list[_StoreItem]:
        scored: list[_StoreItem] = []
        for embedding, metadata in self._items:
            score = sum(a * b for a, b in zip(query_embedding, embedding, strict=True))
            scored.append(_StoreItem(metadata=metadata, score=float(score)))
        scored.sort(key=lambda item: item.score, reverse=True)
        return scored[:k]

    def delete(self, doc_id: str) -> None:
        self._items = [item for item in self._items if item[1].get("id") != doc_id]


def _docs() -> list[Document]:
    return [
        Document(content="weather forecast in beijing", metadata={"id": "d1"}),
        Document(content="stock market update", metadata={"id": "d2"}),
        Document(content="weather warning and humidity", metadata={"id": "d3"}),
    ]


def _is_descending(scores: list[float]) -> bool:
    return all(left >= right for left, right in zip(scores, scores[1:], strict=False))


def _make_retriever() -> DenseRetriever:
    return DenseRetriever(
        embedding_model=_MockEmbedding(),
        vector_store=_MockVectorStore(),
        top_k=3,
    )


def test_dense_retriever_contract_fail_fast_without_dependencies() -> None:
    with pytest.raises(ValueError, match="configured vector_store"):
        DenseRetriever(embedding_model=_MockEmbedding(), vector_store=None, top_k=3)

    with pytest.raises(ValueError, match="configured embedding_model"):
        DenseRetriever(embedding_model=None, vector_store=_MockVectorStore(), top_k=3)


def test_dense_retriever_contract_sorted_and_ranked_results() -> None:
    retriever = _make_retriever()
    retriever.index(_docs())

    results = retriever.retrieve("weather forecast", top_k=2)

    assert len(results) == 2
    assert all(isinstance(item, RetrievalResult) for item in results)
    assert [item.rank for item in results] == [1, 2]
    assert _is_descending([item.score for item in results])


def test_dense_retriever_contract_empty_index_returns_empty() -> None:
    retriever = _make_retriever()

    results = retriever.retrieve("anything", top_k=2)

    assert results == []


def test_dense_retriever_contract_delete_removes_target_documents() -> None:
    retriever = _make_retriever()
    retriever.index(_docs())

    retriever.delete_documents(["d1", "d3"])
    results = retriever.retrieve("weather", top_k=5)

    remaining_ids = [item.document.metadata.get("id") for item in results]
    assert "d1" not in remaining_ids
    assert "d3" not in remaining_ids


def test_cross_encoder_reranker_contract_fail_fast_without_model() -> None:
    with pytest.raises(ValueError, match="configured model"):
        CrossEncoderReranker(model=None, top_k=2)


def test_cross_encoder_reranker_contract_model_mode() -> None:
    model = _MockCrossEncoder([0.1, 0.8, 0.4])
    reranker = CrossEncoderReranker(model=model, top_k=2)
    results = [
        RetrievalResult(Document("doc a", {"id": "a"}), score=0.9, rank=1),
        RetrievalResult(Document("doc b", {"id": "b"}), score=0.1, rank=2),
        RetrievalResult(Document("doc c", {"id": "c"}), score=0.2, rank=3),
    ]

    reranked = reranker.rerank("query", results)

    assert [item.document.metadata.get("id") for item in reranked] == ["b", "c"]
    assert [item.rank for item in reranked] == [1, 2]
    assert all(isinstance(item.score, float) for item in reranked)


def test_cross_encoder_reranker_contract_empty_input() -> None:
    reranker = CrossEncoderReranker(model=_MockCrossEncoder([]), top_k=3)

    assert reranker.rerank("query", [], top_k=2) == []
