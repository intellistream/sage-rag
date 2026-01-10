# sage-rag Migration Guide

**Date**: 2026-01-10  
**Status**: ✅ Initial setup complete, ready for implementation migration

## Overview

`sage-rag` (PyPI: `isage-rag`) is extracted from the SAGE main repository following **REORGANIZATION_PROPOSAL.md Option A (Complete Extraction)**.

## What's Included

### Interface Layer (from sage-libs)
- `src/sage/libs/rag/interface/base.py` - Core abstractions (806 lines)
  - `DocumentLoader` - Document loading interface
  - `TextChunker` - Text chunking interface
  - `Retriever` - Retrieval interface
  - `Reranker` - Reranking interface
  - `RAGPipeline` - End-to-end RAG pipeline interface
  - Data types: `Document`, `Chunk`, `RetrievalResult`

- `src/sage/libs/rag/interface/factory.py` - Factory and registry
  - `create_document_loader()`, `register_document_loader()`
  - `create_text_chunker()`, `register_text_chunker()`
  - `create_retriever()`, `register_retriever()`
  - `create_reranker()`, `register_reranker()`
  - `create_rag_pipeline()`, `register_rag_pipeline()`

### Existing Implementations
- `src/sage/libs/rag/document_loaders.py` - Document loading utilities
- `src/sage/libs/rag/chunk.py` - Text chunking implementations
- `src/sage/libs/rag/types.py` - Data type definitions

## What's Missing (To Be Implemented)

### 1. Document Loaders
```
src/sage/libs/rag/document_loaders/
├── text_loader.py        # Plain text
├── pdf_loader.py         # PDF documents
├── docx_loader.py        # Word documents
├── markdown_loader.py    # Markdown files
├── html_loader.py        # HTML pages
└── json_loader.py        # JSON data
```

**Dependencies**: `pypdf`, `python-docx`, `markdown`, `beautifulsoup4`

### 2. Text Chunkers
```
src/sage/libs/rag/chunk/
├── character_splitter.py  # Character-based chunking
├── sentence_splitter.py   # Sentence-based chunking
├── token_splitter.py      # Token-based chunking
├── semantic_chunker.py    # Semantic chunking
└── hybrid_chunker.py      # Hybrid strategies
```

**Dependencies**: `sentence-transformers`, `tiktoken`, `nltk`

### 3. Retrievers
```
src/sage/libs/rag/retrieval/
├── sagedb_retriever.py    # SageVDB backend
├── chroma_retriever.py    # ChromaDB backend
├── milvus_retriever.py    # Milvus backend
├── faiss_retriever.py     # FAISS backend
└── hybrid_retriever.py    # Hybrid retrieval
```

**Dependencies**: `isage-vdb`, `chromadb`, `pymilvus`, `faiss-cpu`

### 4. Rerankers
```
src/sage/libs/rag/reranking/
├── cross_encoder.py       # Cross-encoder reranking
├── llm_reranker.py        # LLM-based reranking
└── hybrid_reranker.py     # Hybrid reranking
```

**Dependencies**: `sentence-transformers`, `torch`

### 5. RAG Pipeline
```
src/sage/libs/rag/pipeline/
├── default_pipeline.py    # Default RAG pipeline
├── custom_pipeline.py     # Customizable pipeline
└── streaming_pipeline.py  # Streaming RAG
```

**Dependencies**: `openai`, `anthropic`

### 6. Evaluation
```
src/sage/libs/rag/evaluation/
├── metrics.py             # RAG metrics (F1, ROUGE, BERTScore)
├── benchmarks.py          # Standard benchmarks
└── visualization.py       # Result visualization
```

**Dependencies**: `rouge-score`, `bert-score`

## Migration Steps

### Phase 1: Document Loaders (Priority: High)
1. Implement `PDFLoader`, `DocxLoader`, `MarkdownLoader`
2. Register loaders in factory
3. Add tests for each loader

### Phase 2: Text Chunkers
1. Implement character, sentence, token splitters
2. Implement semantic chunker
3. Add overlap and metadata handling

### Phase 3: Retrievers
1. Implement SageVDB retriever (priority)
2. Implement ChromaDB and Milvus retrievers
3. Add hybrid retrieval support

### Phase 4: RAG Pipeline
1. Build default pipeline orchestrator
2. Add component composition
3. Add streaming support

### Phase 5: Testing & Documentation
1. Add unit tests for all components
2. Add integration tests
3. Add end-to-end RAG examples
4. Add API documentation

## Installation (After Publishing)

```bash
# Basic installation
pip install isage-rag

# With optional dependencies
pip install isage-rag[loaders]      # Document loading
pip install isage-rag[chunking]     # Text chunking
pip install isage-rag[retrieval]    # Vector databases
pip install isage-rag[reranking]    # Reranking
pip install isage-rag[generation]   # LLM generation
pip install isage-rag[evaluation]   # Evaluation metrics
pip install isage-rag[all]          # Full installation
```

## Usage Example

```python
from sage.libs.rag.interface import (
    create_document_loader,
    create_text_chunker,
    create_rag_pipeline
)

# Load documents
loader = create_document_loader("pdf")
documents = loader.load("path/to/document.pdf")

# Chunk text
chunker = create_text_chunker("sentence_transformers")
chunks = chunker.chunk(documents, chunk_size=512, overlap=50)

# Build RAG pipeline
pipeline = create_rag_pipeline("default")
pipeline.configure(
    loader="pdf",
    chunker="sentence_transformers",
    retriever="sagedb",
    reranker="cross_encoder",
    generator="openai"
)

# Execute query
response = pipeline.query(
    "What are the main findings?",
    documents=["doc1.pdf", "doc2.pdf"]
)
print(response.answer)
```

## Integration with SAGE

In SAGE's `packages/sage-libs/pyproject.toml`:

```toml
[project.optional-dependencies]
rag = ["isage-rag>=0.1.0"]
```

Users can install:
```bash
pip install sage-libs[rag]
# or
pip install sage-libs[all]
```

## Repository Structure

```
sage-rag/
├── .gitignore
├── LICENSE
├── README.md
├── MIGRATION_GUIDE.md  (this file)
├── pyproject.toml
├── src/
│   └── sage/
│       └── libs/
│           └── rag/
│               ├── __init__.py
│               ├── interface/
│               │   ├── __init__.py
│               │   ├── base.py
│               │   └── factory.py
│               ├── document_loaders.py
│               ├── chunk.py
│               └── types.py
├── tests/
│   └── (to be added)
└── docs/
    └── (to be added)
```

## Git Commits

1. `50caffa` - Initial repository setup (pyproject.toml, README, LICENSE)
2. `5e2697f` - Add rag interface layer and implementations

## Next Steps

1. **Immediate**: Implement PDF, Docx, Markdown loaders
2. **Short-term**: Implement text chunkers (character, sentence, token)
3. **Medium-term**: Implement retrievers (SageVDB, ChromaDB)
4. **Long-term**: Build RAG pipeline orchestrator and evaluation framework

## References

- SAGE main repository: https://github.com/intellistream/SAGE
- REORGANIZATION_PROPOSAL.md: `/packages/sage-libs/docs/REORGANIZATION_PROPOSAL.md`
- Original code: `/packages/sage-libs/src/sage/libs/rag/`
- SageVDB: https://github.com/intellistream/sageVDB
