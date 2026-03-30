"""PDF document loader implementation.

Moved from sage.libs.rag.document_loaders — concrete implementation belongs in sage-rag.
Requires: pip install isage-rag[pdf]  (PyPDF2 package)
"""

from __future__ import annotations

from pathlib import Path
from typing import Any

from sage.libs.rag.interface import Document, DocumentLoader


class PDFLoader(DocumentLoader):
    """Load PDF documents.

    Args:
        extract_images: Whether to attempt image text extraction (default: False).

    Note:
        Requires ``PyPDF2``::

            pip install PyPDF2

    Example:
        >>> from sage_libs.sage_rag import PDFLoader
        >>> loader = PDFLoader()
        >>> doc = loader.load("paper.pdf")
        >>> print(doc.content)
    """

    def __init__(self, extract_images: bool = False) -> None:
        self.extract_images = extract_images

    def load(self, source: str, **kwargs: Any) -> Document:
        """Load a PDF file.

        Args:
            source: Path to the PDF file.
            **kwargs: Additional options.

        Returns:
            Document with extracted text content.

        Raises:
            FileNotFoundError: If file does not exist.
            ImportError: If PyPDF2 is not installed.
        """
        try:
            from PyPDF2 import PdfReader  # type: ignore[import-untyped]
        except ImportError as exc:
            raise ImportError(
                "PDFLoader requires 'PyPDF2'. Install with: pip install PyPDF2"
            ) from exc

        path = Path(source)
        if not path.exists():
            raise FileNotFoundError(f"File not found: {source}")

        reader = PdfReader(str(path))
        text_parts: list[str] = []
        for page in reader.pages:
            page_text = page.extract_text()
            if page_text:
                text_parts.append(page_text)
        content = "\n".join(text_parts)

        return Document(
            content=content,
            metadata={
                "source": str(path.absolute()),
                "filename": path.name,
                "extension": path.suffix,
                "size_bytes": path.stat().st_size,
                "pages": len(reader.pages),
                "loader": "pdf",
            },
        )

    def load_batch(self, sources: list[str], **kwargs: Any) -> list[Document]:
        """Load multiple PDF files."""
        return [self.load(source, **kwargs) for source in sources]

    def supported_formats(self) -> list[str]:
        return [".pdf"]
