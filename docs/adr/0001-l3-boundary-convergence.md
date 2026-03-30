# ADR 0001: RAG pipeline boundary convergence to pure L3 components

## Status

Accepted

## Context

Issue `intellistream/sage-rag#3` requires that `sage-rag` stays as a pure L3 package and avoids middleware/service binding implementations.

Audit findings:

- No direct imports from `sage.middleware`, `sage.kernel`, or `sage.platform` in `src/sage_libs/sage_rag`.
- `DenseRetriever` previously contained a silent in-memory fallback path when `vector_store` was not configured.

This fallback hides missing dependency wiring and violates the fail-fast constraint from the parent boundary refactor issue.

## Decision

1. Keep `sage-rag` as pure L3 algorithm/interface implementation.
2. Enforce fail-fast behavior in `DenseRetriever`:
   - `retrieve/index/delete_documents` now require `vector_store`.
   - embedding generation now requires `embedding_model`.
3. Add regression tests to guard:
   - forbidden cross-layer imports are absent,
   - `DenseRetriever` no longer silently falls back.

## Consequences

- Missing retriever dependencies are surfaced immediately as explicit errors.
- Runtime/service-layer binding responsibility remains outside this repository.
- Boundary contracts become test-enforced and reviewable.
