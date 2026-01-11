# SAGE RAG (isage-rag) - Copilot Instructions

## Package Identity

| 属性 | 值 |
|-----|-----|
| **PyPI 包名** | `isage-rag` |
| **导入名称** | `sage_rag` |
| **SAGE 架构层级** | **L3 (Algorithm Library)** |
| **版本格式** | 四段式 `0.0.0.x` |
| **仓库** | `intellistream/sage-rag` |

## 层级定位

这是一个 **L3 纯算法库**，提供 RAG (Retrieval-Augmented Generation) 的具体实现。

### ✅ 允许的依赖

- Python 标准库
- `sage-common` (L1) - 通过 SAGE 框架使用时
- `sage-libs` 接口层 (L3) - 注册到 SAGE 工厂
- 轻量级第三方库：`sentence-transformers`, `transformers`, `numpy` 等

### ❌ 禁止的依赖

- 任何 L4+ 层的包 (`sage-middleware`, `sage-kernel`)
- 向量数据库客户端 (FAISS, Milvus, SageVDB) - 这些属于 middleware
- 网络服务、数据库连接
- 重型运行时后端

## 与 SAGE 主仓库的关系

### SAGE 侧 (`sage.libs.rag`)

SAGE 主仓库中的 `sage.libs.rag` 包含：

1. **接口层** (`sage.libs.rag.interface`)：
   - 抽象基类：`DocumentLoader`, `TextChunker`, `Retriever`, `Reranker`, `RAGPipeline`
   - 工厂函数：`create_loader()`, `create_retriever()`, `register_loader()` 等

2. **类型定义** (`sage.libs.rag.types`)：
   - Pipeline 类型：`RAGDocument`, `RAGQuery`, `RAGResponse`, `RAGInput`, `RAGOutput`
   - 辅助函数：`create_rag_response()`, `ensure_rag_response()`, `extract_query()`

3. **内置工具** (`sage.libs.rag.document_loaders`, `sage.libs.rag.chunk`)：
   - 文档加载器：`TextLoader`, `PDFLoader`, `MarkdownLoader`, `LoaderFactory`
   - 分块器：`CharacterSplitter`, `SentenceTransformersTokenTextSplitter`

### 本包 (`sage_rag`) 提供

**具体实现**，通过 `_register.py` 自动注册到 SAGE 工厂：

- `TextLoader`, `MarkdownLoader` - 文档加载
- `SentenceChunker`, `TokenChunker` - 文本分块
- `DenseRetriever` - 稠密向量检索
- `CrossEncoderReranker` - 重排序
- `SimpleRAGPipeline` - 简单 RAG 流水线

## 导入方式

```python
# 方式 1：直接使用（独立模式）
from sage_rag import TextLoader, DenseRetriever, SimpleRAGPipeline

# 方式 2：通过 SAGE 工厂（集成模式）
import sage_rag  # 触发自动注册
from sage.libs.rag import create_loader, create_retriever
loader = create_loader("text")
retriever = create_retriever("dense")
```

## 目录结构

```
sage-rag/
├── src/sage_rag/
│   ├── __init__.py      # 主入口，导出所有公开 API
│   ├── _version.py      # 版本：__version__ = "0.0.0.x"
│   ├── _register.py     # 自动注册到 SAGE 工厂
│   ├── loaders/         # 文档加载器实现
│   ├── chunkers/        # 文本分块器实现
│   ├── retrievers/      # 检索器实现
│   ├── rerankers/       # 重排序器实现
│   └── pipelines/       # RAG 流水线实现
├── tests/
├── pyproject.toml
└── README.md
```

## 常见问题修复指南

### 问题 1：导入失败 - "No module named 'sage_rag.xxx'"

**检查**：
1. 确认 `src/sage_rag/__init__.py` 正确导出模块
2. 确认子模块有 `__init__.py`
3. 确认 `pyproject.toml` 配置正确

### 问题 2：SAGE 工厂未注册

**检查**：
1. `_register.py` 是否正确实现
2. `__init__.py` 是否导入了 `_register`

```python
# _register.py 示例
try:
    from sage.libs.rag import register_loader
    from .loaders import TextLoader
    register_loader("text", TextLoader)
except ImportError:
    pass  # SAGE 未安装，作为独立库使用
```

### 问题 3：类型不兼容

**原则**：
- 本包的实现应符合 `sage.libs.rag.interface` 的抽象基类
- 不要在本包中重新定义 `RAGDocument` 等类型，那些属于 SAGE 主仓库

## 测试

```bash
# 运行测试
pytest tests/ -v

# 独立模式测试（不依赖 SAGE）
pytest tests/ -v -k "not integration"

# 集成模式测试（需要 SAGE 安装）
pytest tests/integration/ -v
```

## 发布

```bash
# 版本递增
# 修改 src/sage_rag/_version.py: __version__ = "0.0.0.2"

# 构建和发布
pip install build twine
python -m build
twine upload dist/*
```
