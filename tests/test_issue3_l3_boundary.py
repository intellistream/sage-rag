"""Regression tests for issue #3 L3 boundary convergence."""

from __future__ import annotations

from pathlib import Path

import pytest

from sage_libs.sage_rag.retrievers.dense import DenseRetriever


REPO_ROOT = Path(__file__).resolve().parents[1]


@pytest.mark.parametrize(
    "forbidden",
    [
        "sage.middleware",
        "sage.kernel",
        "sage.platform",
    ],
)
def test_no_forbidden_cross_layer_imports(forbidden: str) -> None:
    source_root = REPO_ROOT / "src" / "sage_libs" / "sage_rag"
    for py_file in source_root.rglob("*.py"):
        content = py_file.read_text(encoding="utf-8")
        assert forbidden not in content, f"Forbidden import marker '{forbidden}' in {py_file}"


def test_dense_retriever_requires_vector_store() -> None:
    class MockEmbedding:
        def encode(self, _text: str):
            class _Vector:
                def tolist(self) -> list[float]:
                    return [1.0]

            return _Vector()

    with pytest.raises(ValueError, match="vector_store"):
        DenseRetriever(embedding_model=MockEmbedding(), vector_store=None)


def test_dense_retriever_requires_embedding_model() -> None:
    class MockStore:
        def add(self, *_args, **_kwargs):
            return None

        def build_index(self):
            return None

        def search(self, *_args, **_kwargs):
            return []

        def delete(self, *_args, **_kwargs):
            return None

    with pytest.raises(ValueError, match="embedding_model"):
        DenseRetriever(embedding_model=None, vector_store=MockStore())
