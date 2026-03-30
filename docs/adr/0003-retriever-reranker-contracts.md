# ADR 0003: Retriever/Reranker Contract Tests

## Status

Accepted

## Context

Issue `intellistream/sage-rag#5` requires executable contract coverage for retriever/reranker behavior stability and cross-implementation consistency.

Existing tests covered package imports and interface registration, but did not verify core runtime contracts such as:

- result ordering and rank monotonicity,
- `top_k` truncation behavior,
- empty-input behavior,
- deletion effect for indexed retriever state,
- explicit dependency requirements (`DenseRetriever` storage/embedding, `CrossEncoderReranker` model).

## Decision

Add dedicated contract tests in `tests/test_retriever_reranker_contracts.py` to lock the required behavior for:

- `DenseRetriever`
- `CrossEncoderReranker`

The tests enforce behavior-level contracts with direct fail-fast checks and canonical API usage.

## Consequences

- Boundary behavior is now regression-testable and reviewable.
- Future implementation changes must preserve the same API contracts.
- Callers must satisfy required dependencies explicitly.
