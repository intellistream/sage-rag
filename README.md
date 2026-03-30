# SAGE RAG

[![PyPI version](https://badge.fury.io/py/isage-rag.svg)](https://badge.fury.io/py/isage-rag)
[![Python 3.10+](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org/downloads/)
[![License](https://img.shields.io/badge/License-MIT-blue.svg)](https://opensource.org/licenses/MIT)

RAG (Retrieval-Augmented Generation) 组件库，提供文档加载、文本分块、检索和重排序功能。

## 🧭 边界说明（L3）

`sage-rag` 作为 L3 算法组件仓库，职责边界如下：

- **In-scope（本仓库负责）**
  - 文档加载（loaders）
  - 文本切分（chunkers）
  - 检索与重排实现（retrievers / rerankers）
  - RAG pipeline 组合逻辑（pipelines）
- **Out-of-scope（不在本仓库实现）**
  - 中间件/服务绑定能力（例如数据库服务编排、集群调度）
  - L4/L5 运行时和平台层实现
- **Forbidden imports（禁止越层依赖）**
  - `sage.middleware`
  - `sage.kernel`
  - `sage.platform`

边界与依赖审计 ADR：

- `docs/adr/0001-l3-boundary-convergence.md`
- `docs/adr/0002-pipeline-boundary-cleanup.md`
- `docs/adr/0003-retriever-reranker-contracts.md`
- `docs/adr/0004-phase1-dependency-audit.md`

## 📦 安装

```bash
pip install isage-rag
```

## 🚀 快速开始

```python
# 直接导入使用
from sage_rag import TextLoader, SentenceChunker

loader = TextLoader()
documents = loader.load("document.txt")

chunker = SentenceChunker()
chunks = chunker.chunk(documents)
```

## 📚 组件

- **Loaders**: TextLoader, MarkdownLoader
- **Chunkers**: SentenceChunker, TokenChunker
- **Retrievers**: DenseRetriever
- **Rerankers**: CrossEncoderReranker
- **Pipelines**: SimpleRAGPipeline

> `DenseRetriever` 需要显式提供 `vector_store` 与 `embedding_model` 后才能执行 `index/retrieve/delete_documents`。

详细文档请查看 [docs/](docs/) 目录。

## 🔌 与 SAGE 集成

本包会在导入时自动注册到本地 `sage_rag` 注册表：

```python
import sage_rag  # 自动注册
from sage_rag.interface import create_loader

loader = create_loader("text")
```

## 📄 许可证

MIT License - 详见 [LICENSE](LICENSE)

## 📧 联系

- GitHub: <https://github.com/intellistream/sage-rag>
- Email: <mailto:shuhao_zhang@hust.edu.cn>
