# SAGE RAG Copilot Instructions

## Scope
- Package: `isage-rag`, import path `sage_rag`.
- Purpose: reusable RAG components (loaders, chunkers, retrievers, rerankers, pipelines).

## Critical rules
- Keep package lightweight and modular; avoid unnecessary heavy dependencies.
- Preserve two usage modes: standalone usage and optional SAGE integration.
- Maintain typed public APIs and clear docstrings.
- Keep component registration logic coherent with `_register.py` and public exports in `__init__.py`.
- No silent error masking in core logic.

## Workflow
1. Implement minimal changes under `src/sage_libs/sage_rag/`.
2. Update tests under `tests/` for new behavior.
3. Keep README/docs examples aligned with API changes.

## Key paths
- `loaders/`, `chunkers/`, `retrievers/`, `rerankers/`, `pipelines/`, `_register.py`.
