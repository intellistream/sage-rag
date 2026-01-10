# SAGE RAG

**Document Loading, Chunking, Retrieval, and RAG Pipeline Orchestration**

[![PyPI version](https://badge.fury.io/py/isage-rag.svg)](https://badge.fury.io/py/isage-rag)
[![Python 3.10+](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org/downloads/)
[![License](https://img.shields.io/badge/License-Apache%202.0-blue.svg)](https://opensource.org/licenses/Apache-2.0)

**SAGE RAG** 是从 [SAGE](https://github.com/intellistream/SAGE) 框架中提取的独立 RAG 组件，提供完整的文档加载、文本分块、检索、重排序和 RAG 管道编排能力。

## ✨ 核心特性

### 📄 Document Loading
- **DocumentLoader** 抽象接口 - 统一的文档加载接口
- 支持多种格式：
  - 纯文本 (TextLoader)
  - PDF (PDFLoader)
  - Word 文档 (DocxLoader)
  - Markdown (MarkdownLoader)
  - HTML (HTMLLoader)
- **Document** 数据类型 - 标准化文档表示

### ✂️ Text Chunking
- **TextChunker** 抽象接口 - 文本分块策略
- 多种分块算法：
  - 字符级分块 (CharacterSplitter)
  - 句子级分块 (SentenceSplitter)
  - Token 级分块 (TokenTextSplitter, SentenceTransformersTokenTextSplitter)
  - 语义分块 (SemanticChunker)
- **Chunk** 数据类型 - 包含元数据的文本块

### 🔍 Retrieval
- **Retriever** 抽象接口 - 检索策略
- 支持多种后端：
  - SageVDB (isage-vdb)
  - ChromaDB
  - Milvus
  - FAISS
- **RetrievalResult** 数据类型 - 检索结果表示

### 🎯 Reranking
- **Reranker** 抽象接口 - 重排序策略
- 算法支持：
  - Cross-encoder reranking
  - LLM-based reranking
  - Hybrid reranking

### 🔄 RAG Pipeline
- **RAGPipeline** - 端到端 RAG 流程编排
- 支持自定义组件组合
- 内置评估指标

## �� 安装

### 基础安装
```bash
pip install isage-rag
```

### 完整安装（包含所有可选功能）
```bash
pip install isage-rag[all]
```

### 按需安装
```bash
# 文档加载
pip install isage-rag[loaders]

# 文本分块
pip install isage-rag[chunking]

# 向量检索
pip install isage-rag[retrieval]

# 重排序
pip install isage-rag[reranking]

# LLM 生成
pip install isage-rag[generation]

# 评估指标
pip install isage-rag[evaluation]
```

## 🚀 快速开始

### 1. 文档加载

```python
from sage.libs.rag.interface import create_document_loader

# 加载 PDF 文档
loader = create_document_loader("pdf")
documents = loader.load("path/to/document.pdf")

for doc in documents:
    print(f"Page {doc.metadata['page']}: {doc.content[:100]}...")
```

### 2. 文本分块

```python
from sage.libs.rag.interface import create_text_chunker

# 创建分块器
chunker = create_text_chunker("sentence_transformers")

# 分块文档
chunks = chunker.chunk(documents, chunk_size=512, overlap=50)
print(f"Total chunks: {len(chunks)}")
```

### 3. 构建 RAG 管道

```python
from sage.libs.rag.interface import create_rag_pipeline

# 创建完整 RAG 管道
pipeline = create_rag_pipeline("default")

# 配置组件
pipeline.configure(
    loader="pdf",
    chunker="sentence_transformers",
    retriever="sagedb",
    reranker="cross_encoder",
    generator="openai"
)

# 执行 RAG 查询
response = pipeline.query(
    "What are the main findings?",
    documents=["path/to/doc1.pdf", "path/to/doc2.pdf"]
)
print(response.answer)
```

### 4. 使用接口抽象

```python
from sage.libs.rag.interface import DocumentLoader, TextChunker, Retriever

# 实现自定义文档加载器
class CustomLoader(DocumentLoader):
    def load(self, source: str) -> list[Document]:
        # 自定义加载逻辑
        pass

# 注册到工厂
from sage.libs.rag.interface import register_document_loader
register_document_loader("custom", CustomLoader)

# 使用工厂创建
loader = create_document_loader("custom")
```

## 🏗️ 架构

```
sage.libs.rag/
├── interface/              # 公共接口（从 sage-libs 导入）
│   ├── base.py            # DocumentLoader, TextChunker, Retriever, Reranker, RAGPipeline
│   ├── factory.py         # 工厂函数和注册表
│   └── __init__.py        # 公共 API
├── document_loaders/      # 文档加载器实现
│   ├── text_loader.py
│   ├── pdf_loader.py
│   ├── docx_loader.py
│   └── markdown_loader.py
├── chunk/                 # 文本分块实现
│   ├── character_splitter.py
│   ├── sentence_splitter.py
│   └── token_splitter.py
├── retrieval/            # 检索实现
│   ├── sagedb_retriever.py
│   ├── chroma_retriever.py
│   └── milvus_retriever.py
├── reranking/            # 重排序实现
│   ├── cross_encoder.py
│   └── llm_reranker.py
├── pipeline/             # RAG 管道编排
│   ├── default_pipeline.py
│   └── custom_pipeline.py
└── types/                # 数据类型定义
    ├── document.py
    ├── chunk.py
    └── retrieval_result.py
```

## 🔌 与 SAGE 集成

虽然 `isage-rag` 可以独立使用，但它与 SAGE 框架深度集成：

```python
# 在 SAGE 项目中使用（通过 sage-libs）
from sage.libs.rag.interface import create_rag_pipeline

# 接口层在 sage-libs，实现在 isage-rag
pipeline = create_rag_pipeline("default")
```

在 SAGE 项目的 `pyproject.toml` 中：
```toml
[project.optional-dependencies]
rag = ["isage-rag>=0.1.0"]
```

安装 SAGE 时自动包含 RAG：
```bash
pip install sage-libs[rag]
# 或
pip install sage-libs[all]
```

## 📚 文档

- [完整文档](https://sage-docs.org/rag)
- [API 参考](https://sage-docs.org/rag/api)
- [示例集合](https://github.com/intellistream/sage-examples)

## 🤝 贡献

欢迎贡献！请查看 [CONTRIBUTING.md](CONTRIBUTING.md) 了解详情。

## 📄 许可证

Apache License 2.0 - 详见 [LICENSE](LICENSE)

## 🔗 相关项目

- [SAGE](https://github.com/intellistream/SAGE) - 主框架
- [sage-libs](https://github.com/intellistream/SAGE/tree/main/packages/sage-libs) - 接口层
- [isage-agentic](https://github.com/intellistream/sage-agentic) - Agent 框架
- [isage-vdb](https://github.com/intellistream/sageVDB) - 向量数据库
- [isage-anns](https://github.com/intellistream/sage-anns) - ANN 算法库

## 📧 联系

- **团队**: IntelliStream Team
- **邮箱**: shuhao_zhang@hust.edu.cn
- **GitHub**: https://github.com/intellistream/sage-rag
