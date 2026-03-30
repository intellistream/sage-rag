# ADR 0002: Pipeline boundary cleanup (Issue #4)

## Status

Accepted

## Context

Issue `intellistream/sage-rag#4` requires removing duplicate public abstractions and enforcing strict boundary behavior.

Problems found in `SimpleRAGPipeline`:

- Public `index_documents()` and `index()` duplicated the same indexing flow.
- `retrieve()` silently returned empty results when retriever was missing.
- `query()` returned string responses instead of the `RAGPipeline` contract payload.
- `_generate_response()` accepted multiple generation entrypoints and non-explicit error paths.

These behaviors violated fail-fast and single-entrypoint principles in the boundary-refactor plan.

## Decision

1. Keep only one indexing entrypoint: `index_documents()`.
2. Make querying fail-fast:
   - missing retriever -> raise `ValueError`
   - missing generator -> raise `ValueError`
   - invalid generator contract -> raise `TypeError`
3. Align `query()` return shape with `RAGPipeline` interface contract:
   - `{"answer": ..., "sources": ..., "metadata": ...}`
4. Extract shared indexing flow into internal helper (`_collect_documents`) instead of duplicate public APIs.

## Consequences

- Pipeline behavior is stricter and deterministic.
- Silent non-explicit paths are removed.
- Callers should use the canonical pipeline contract (`index_documents()` and structured `query()` result).
- Regression tests were added to lock the new boundary behavior.
