# Changelog

All notable changes to `isage-rag` will be documented in this file.

## [0.3.0] - 2026-03-07

### Added
- `src/sage_rag/operators/` — full RAG runtime operator suite migrated from
  `isage-middleware` (`sage.middleware.operators.rag`):
  - `retriever.py`: `ChromaRetriever`, `MilvusDenseRetriever`,
    `MilvusSparseRetriever`, `Wiki18FAISSRetriever`
  - `reranker.py`: `BGEReranker`, `LLMbased_Reranker`
  - `generator.py`: `OpenAIGenerator`, `HFGenerator`, `SageLLMRAGGenerator`
  - `evaluate.py`: `F1Evaluate`, `EMEvaluate`, `RecallEvaluate`,
    `BertRecallEvaluate`, `RougeLEvaluate`, `BRSEvaluate`, `AccuracyEvaluate`,
    `TokenCountEvaluate`, `LatencyEvaluate`, `ContextRecallEvaluate`,
    `CompressionRateEvaluate`, `MetricsAggregator`
  - `promptor.py`: `QAPromptor`, `SummarizationPromptor`, `QueryProfilerPromptor`
  - `refiner.py`: `RefinerOperator`
  - `arxiv.py`: `ArxivPDFDownloader`, `ArxivPDFParser`
  - `searcher.py`: `BochaWebSearch`
  - `writer.py`: `MemoryWriter`
  - `pipeline.py`: `RAGPipeline`
  - `profiler.py`: `Query_Profiler`, `QueryProfilerResult`
  - `types.py`, `chunk.py`, `document_loaders.py` — re-exports from `sage.libs.rag`
  - `index_builder/`: `IndexBuilder`, `IndexManifest`, `VectorStore`
  - `operators/__init__.py` — lazy import registry for all operators

### Changed
- `pyproject.toml`: added runtime deps (`isage-common>=0.2.4.30`,
  `isage-kernel>=0.2.4.28`, `isage-libs>=0.2.4.22`, `numpy>=1.21.0`,
  `requests>=2.28.0`, `jinja2>=3.1.0`) and optional extras (`operators`,
  `middleware`)
- `src/sage_rag/__init__.py`: exports `operators` sub-package

## [0.2.0] - 2026-02-27

### Added
- Initial standalone release: chunkers, loaders, pipelines, rerankers, retrievers
- Backends: ChromaDB (`sage_rag.backends.chroma`), Milvus (`sage_rag.backends.milvus`)
