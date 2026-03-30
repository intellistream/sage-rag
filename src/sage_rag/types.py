"""Shared lightweight RAG payload types for ``sage-rag`` operators."""

from __future__ import annotations

from typing import Any, TypeAlias

from .interface import Document

RAGDocument = Document
RAGQuery: TypeAlias = str
RAGResponse: TypeAlias = dict[str, Any]
RAGInput: TypeAlias = dict[str, Any] | str
RAGOutput: TypeAlias = dict[str, Any]


def extract_query(data: RAGInput) -> str:
    if isinstance(data, str):
        return data
    return str(data.get("query", data.get("question", "")))


def extract_results(data: RAGInput) -> list[Any]:
    if isinstance(data, str):
        return []
    for key in ("results", "retrieval_results", "sources", "context"):
        value = data.get(key)
        if isinstance(value, list):
            return value
    return []


def create_rag_response(query: str, results: list[Any], **extra: Any) -> RAGResponse:
    return {"query": query, "results": list(results), **extra}


def ensure_rag_response(payload: Any) -> RAGResponse:
    if isinstance(payload, dict) and "query" in payload and "results" in payload:
        return payload
    if isinstance(payload, str):
        return create_rag_response(payload, [])
    return create_rag_response("", [])


__all__ = [
    "RAGDocument",
    "RAGInput",
    "RAGOutput",
    "RAGQuery",
    "RAGResponse",
    "create_rag_response",
    "ensure_rag_response",
    "extract_query",
    "extract_results",
]
