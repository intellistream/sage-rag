# SAGE RAG - Copilot Instructions

## 📦 包信息

| 属性 | 值 |
|-----|-----|
| **PyPI 包名** | `isage-rag` |
| **导入名称** | `sage_rag` |
| **源代码路径** | `src/sage_libs/sage_rag/` |
| **版本** | `0.1.0.0` |
| **许可证** | MIT |

## 🎯 项目定位

这是一个 **RAG 组件库**，提供文档加载、文本分块、检索和重排序的具体实现。

### 核心功能
- 文档加载器（Loaders）
- 文本分块器（Chunkers）
- 检索器（Retrievers）
- 重排序器（Rerankers）
- RAG 流水线（Pipelines）

### 设计原则
1. **独立可用**：可以不依赖 SAGE 框架独立使用
2. **自动注册**：导入时自动注册到 SAGE 工厂（如果 SAGE 已安装）
3. **轻量级**：最小化依赖，核心功能仅需要 pydantic
4. **可扩展**：通过工厂模式支持自定义实现

## 📁 目录结构

```
src/sage_libs/sage_rag/
├── __init__.py          # 主入口，导出所有公开 API
├── _version.py          # 版本信息
├── _register.py         # 自动注册到 SAGE（如果可用）
├── py.typed             # 类型标注支持
├── loaders/             # 文档加载器
│   ├── __init__.py
│   ├── text.py          # TextLoader
│   └── markdown.py      # MarkdownLoader
├── chunkers/            # 文本分块器
│   ├── __init__.py
│   ├── sentence.py      # SentenceChunker
│   └── token.py         # TokenChunker
├── retrievers/          # 检索器
│   ├── __init__.py
│   └── dense.py         # DenseRetriever
├── rerankers/           # 重排序器
│   ├── __init__.py
│   └── cross_encoder.py # CrossEncoderReranker
└── pipelines/           # RAG 流水线
    ├── __init__.py
    └── simple.py        # SimpleRAGPipeline
```

## 🔌 与 SAGE 集成

### 独立使用模式
```python
# 直接导入使用
from sage_rag import TextLoader, SentenceChunker

loader = TextLoader()
chunker = SentenceChunker()
```

### SAGE 集成模式
```python
# 导入时自动注册到 SAGE 工厂
import sage_rag
from sage.libs.rag import create_loader

# 通过工厂创建
loader = create_loader("text")
```

### 注册机制 (_register.py)
```python
# _register.py 负责自动注册
try:
    from sage.libs.rag import register_loader, register_chunker
    from .loaders import TextLoader, MarkdownLoader
    from .chunkers import SentenceChunker
    
    # 注册所有组件
    register_loader("text", TextLoader)
    register_loader("markdown", MarkdownLoader)
    register_chunker("sentence", SentenceChunker)
except ImportError:
    # SAGE 未安装，作为独立库使用
    pass
```

## 🛠️ 开发指南

### 添加新组件
1. 在对应子目录创建模块文件（如 `loaders/pdf.py`）
2. 实现组件类
3. 在 `__init__.py` 中导出
4. 在 `_register.py` 中注册到 SAGE（如果适用）

### 代码规范
- 使用 `ruff` 进行代码格式化和检查
- 类型标注：所有公开 API 必须有类型标注
- 文档字符串：使用 Google 风格
- 测试：每个组件都应有对应的测试文件

### 测试
```bash
# 运行所有测试
pytest tests/ -v

# 测试特定模块
pytest tests/test_loaders.py -v
```

## 📦 依赖管理

### 核心依赖（必需）
```toml
dependencies = [
    "pydantic>=2.0.0",
    "typing-extensions>=4.0.0",
]
```

### 可选依赖（按需安装）
- 文档加载：`pypdf`, `python-docx`, `markdown`
- 文本分块：`sentence-transformers`, `tiktoken`
- 检索：`numpy`, `torch`
- 重排序：`transformers`

## ⚠️ 常见问题

### 问题 1：导入错误 "No module named 'sage_rag'"
**原因**：包未正确安装或路径配置错误

**解决**：
```bash
# 开发模式安装
pip install -e .

# 检查安装
python -c "import sage_rag; print(sage_rag.__version__)"
```

### 问题 2：SAGE 工厂注册失败
**原因**：`_register.py` 未被导入

**解决**：确保 `__init__.py` 中有：
```python
from . import _register  # noqa: F401
```

### 问题 3：类型检查错误
**原因**：缺少类型标注或 py.typed 文件

**解决**：
- 确保 `py.typed` 文件存在
- 使用 `mypy` 检查类型：`mypy src/sage_libs/sage_rag/`

## 🚀 发布流程

1. 更新版本号：编辑 `pyproject.toml` 和 `_version.py`
2. 构建：`python -m build`
3. 测试：`twine check dist/*`
4. 发布：`twine upload dist/*`

## 📝 编码提示

当开发此项目时，请遵循：

1. **保持轻量级**：避免引入重型依赖
2. **独立可测**：所有组件应该可以独立测试
3. **向后兼容**：API 变更要谨慎，遵循语义化版本
4. **文档完整**：每个公开 API 都要有清晰的文档
5. **类型安全**：充分利用 Python 类型系统
