# SAGE RAG

[![PyPI version](https://badge.fury.io/py/isage-rag.svg)](https://badge.fury.io/py/isage-rag)
[![Python 3.10+](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org/downloads/)
[![License](https://img.shields.io/badge/License-MIT-blue.svg)](https://opensource.org/licenses/MIT)

RAG (Retrieval-Augmented Generation) 组件库，提供文档加载、文本分块、检索和重排序功能。

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
