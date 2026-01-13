"""Markdown file loader implementation."""

from pathlib import Path
from typing import Any

from sage.libs.rag.interface import Document, DocumentLoader


class MarkdownLoader(DocumentLoader):
    """Load Markdown files.

    Args:
        encoding: Text encoding (default: utf-8).
        include_metadata: Whether to extract YAML frontmatter.

    Example:
        >>> from sage_libs.sage_rag import MarkdownLoader
        >>> loader = MarkdownLoader()
        >>> doc = loader.load("README.md")
    """

    def __init__(self, encoding: str = "utf-8", include_metadata: bool = True):
        self.encoding = encoding
        self.include_metadata = include_metadata

    def load(self, source: str, **kwargs: Any) -> Document:
        """Load a Markdown file.

        Args:
            source: Path to the Markdown file.
            **kwargs: Additional options.

        Returns:
            Document with file content.
        """
        path = Path(source)
        if not path.exists():
            raise FileNotFoundError(f"File not found: {source}")

        encoding = kwargs.get("encoding", self.encoding)
        content = path.read_text(encoding=encoding)

        metadata = {
            "source": str(path.absolute()),
            "filename": path.name,
            "extension": path.suffix,
            "size_bytes": path.stat().st_size,
            "loader": "markdown",
        }

        # Extract YAML frontmatter if present
        if self.include_metadata and content.startswith("---"):
            parts = content.split("---", 2)
            if len(parts) >= 3:
                frontmatter = parts[1].strip()
                content = parts[2].strip()
                metadata["frontmatter"] = frontmatter

        return Document(content=content, metadata=metadata)

    def load_batch(self, sources: list[str], **kwargs: Any) -> list[Document]:
        """Load multiple Markdown files."""
        return [self.load(source, **kwargs) for source in sources]

    def supported_formats(self) -> list[str]:
        """Get list of supported file formats.

        Returns:
            List of file extensions
        """
        return [".md", ".markdown", ".mdown"]
