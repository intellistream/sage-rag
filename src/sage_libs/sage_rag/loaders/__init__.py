"""Document Loader implementations for SAGE RAG."""

from pathlib import Path
from typing import Any

from sage.libs.rag.interface import Document

from .markdown import MarkdownLoader
from .pdf import PDFLoader
from .text import TextLoader
from .word import DocLoader, DocxLoader


class LoaderFactory:
    """Select and invoke the appropriate loader based on file extension.

    Example::

        from sage_libs.sage_rag.loaders import LoaderFactory

        doc = LoaderFactory.load("report.pdf")
        print(doc.content)
    """

    _loader_map: dict[str, type] = {
        ".txt": TextLoader,
        ".pdf": PDFLoader,
        ".docx": DocxLoader,
        ".doc": DocLoader,
        ".md": MarkdownLoader,
        ".markdown": MarkdownLoader,
        ".mdown": MarkdownLoader,
    }

    @classmethod
    def load(cls, filepath: str, **kwargs: Any) -> Document:
        """Load a file using the appropriate loader.

        Args:
            filepath: Path to the file.
            **kwargs: Forwarded to the loader's ``load()`` method.

        Returns:
            Loaded :class:`~sage.libs.rag.interface.Document`.

        Raises:
            ValueError: If the file extension is not supported.
        """
        ext = Path(filepath).suffix.lower()
        loader_cls = cls._loader_map.get(ext)
        if loader_cls is None:
            raise ValueError(
                f"Unsupported file extension: {ext!r}. "
                f"Supported: {sorted(cls._loader_map)}"
            )
        return loader_cls().load(filepath, **kwargs)

    @classmethod
    def supported_extensions(cls) -> list[str]:
        """Return all registered file extensions."""
        return sorted(cls._loader_map)


__all__ = [
    "TextLoader",
    "MarkdownLoader",
    "PDFLoader",
    "DocxLoader",
    "DocLoader",
    "LoaderFactory",
]
