"""Text file loader implementation."""

from pathlib import Path
from typing import Any

from sage.libs.rag.interface import Document, DocumentLoader


class TextLoader(DocumentLoader):
    """Load plain text files.

    Args:
        encoding: Text encoding (default: utf-8).

    Example:
        >>> from sage_libs.sage_rag import TextLoader
        >>> loader = TextLoader()
        >>> doc = loader.load("document.txt")
        >>> print(doc.content)
    """

    def __init__(self, encoding: str = "utf-8"):
        self.encoding = encoding

    def load(self, source: str, **kwargs: Any) -> Document:
        """Load a text file.

        Args:
            source: Path to the text file.
            **kwargs: Additional options (encoding override).

        Returns:
            Document with file content.

        Raises:
            FileNotFoundError: If file doesn't exist.
        """
        path = Path(source)
        if not path.exists():
            raise FileNotFoundError(f"File not found: {source}")

        encoding = kwargs.get("encoding", self.encoding)
        content = path.read_text(encoding=encoding)

        return Document(
            content=content,
            metadata={
                "source": str(path.absolute()),
                "filename": path.name,
                "extension": path.suffix,
                "size_bytes": path.stat().st_size,
                "loader": "text",
            },
        )

    def load_batch(self, sources: list[str], **kwargs: Any) -> list[Document]:
        """Load multiple text files.

        Args:
            sources: List of file paths.
            **kwargs: Additional options.

        Returns:
            List of documents.
        """
        return [self.load(source, **kwargs) for source in sources]

    def supported_formats(self) -> list[str]:
        """Get list of supported file formats.

        Returns:
            List of file extensions
        """
        return [".txt", ".text", ".log"]
