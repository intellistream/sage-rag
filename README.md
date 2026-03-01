# SAGE RAG

[![PyPI version](https://badge.fury.io/py/isage-rag.svg)](https://badge.fury.io/py/isage-rag)
[![Python 3.10+](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org/downloads/)
[![License](https://img.shields.io/badge/License-MIT-blue.svg)](https://opensource.org/licenses/MIT)

RAG (Retrieval-Augmented Generation) 组件库，提供文档加载、文本分块、检索和重排序功能。

## 🧭 边界说明（L3）

- 本仓库仅提供算法与接口实现（L3），不承载 middleware/service 绑定逻辑。
- 禁止引入 `sage.middleware`、`sage.kernel`、`sage.platform` 依赖。
- 采用 fail-fast：缺失依赖直接报错，不保留额外路径。

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

本包可以自动注册到 SAGE 框架：

```python
import sage_rag  # 自动注册
from sage.libs.rag import create_loader

loader = create_loader("text")
```

## 📄 许可证

MIT License - 详见 [LICENSE](LICENSE)

## 📧 联系

- GitHub: https://github.com/intellistream/sage-rag
- Email: shuhao_zhang@hust.edu.cn
