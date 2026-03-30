# ADR 0004: Phase 1 dependency audit for issue #2

## Status

Accepted

## Context

Issue `intellistream/sage-rag#2` requires that dependency declarations in `pyproject.toml`
match runtime imports and that retained dependencies have explicit justification.

## Audit scope

- Runtime package: `src/sage_libs/sage_rag/**`
- Public package entrypoint: `src/sage_rag/**`
- Tests and docs are out of runtime dependency scope.

## Runtime dependency mapping

### Kept in `project.dependencies`

- `isage-libs>=0.2.4.22`
  - Required for `sage.libs.rag.interface` contracts (`Document`, `Chunk`, `Retriever`, etc.).
  - Used by all loaders/chunkers/retrievers/rerankers/pipelines.
- `pydantic>=2.0.0`
  - Retained for interface/model compatibility with SAGE ecosystem package constraints.
- `typing-extensions>=4.0.0`
  - Retained for typing compatibility in Python 3.10+ multi-repo environments.

### Optional runtime extras (import-on-demand)

- `PyPDF2` for `PDFLoader`
- `python-docx` for `DocxLoader`
- `pywin32` for `DocLoader` (Windows only)
- `transformers` for `TransformerTokenChunker`

These are intentionally not hard-required in base install to keep the core package lightweight,
while each component remains fail-fast with explicit `ImportError` when the optional dependency is missing.

## Boundary verdict

- No runtime imports from forbidden upper-layer modules (`sage.middleware`, `sage.kernel`, `sage.platform`).
- No newly introduced fallback/shim behavior in runtime logic.
- Dependency declarations are consistent with current runtime import strategy.
