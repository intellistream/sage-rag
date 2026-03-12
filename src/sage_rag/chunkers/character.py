"""Character-based text chunker.

Moved from sage.libs.rag.chunk — concrete implementation belongs in sage-rag (L3 algo).
"""

from __future__ import annotations

from typing import Any

from sage_rag.interface import Chunk, Document, TextChunker


class CharacterChunker(TextChunker):
    """Split text into overlapping chunks by character count.

    Args:
        chunk_size: Number of characters per chunk (default: 512).
        overlap: Number of overlapping characters between consecutive chunks (default: 128).
        separator: Optional string separator; if provided, text is split on this separator
            instead of by character count.

    Example:
        >>> from sage_libs.sage_rag import CharacterChunker
        >>> chunker = CharacterChunker(chunk_size=200, overlap=40)
        >>> chunks = chunker.chunk("Long text here...")
    """

    def __init__(
        self,
        chunk_size: int = 512,
        overlap: int = 128,
        separator: str | None = None,
    ) -> None:
        self.chunk_size = chunk_size
        self.overlap = overlap
        self.separator = separator

    def chunk(self, text: str, **kwargs: Any) -> list[Chunk]:
        """Split text into chunks.

        Args:
            text: The text to split.
            **kwargs: chunk_size / overlap / separator overrides.

        Returns:
            List of :class:`~sage.libs.rag.interface.Chunk` objects.
        """
        chunk_size = kwargs.get("chunk_size", self.chunk_size)
        overlap = kwargs.get("overlap", self.overlap)
        separator = kwargs.get("separator", self.separator)

        if separator:
            raw_chunks = [part for part in text.split(separator) if part.strip()]
            return [
                Chunk(
                    content=part,
                    metadata={"chunk_index": i, "chunker": "character", "separator": separator},
                )
                for i, part in enumerate(raw_chunks)
            ]

        # Character-level sliding window
        chars = list(text)
        if not chars:
            return [Chunk(content="", metadata={"chunk_index": 0, "chunker": "character"})]

        chunks: list[Chunk] = []
        start = 0
        while start < len(chars):
            end = start + chunk_size
            chunk_text = "".join(chars[start:end])
            chunks.append(
                Chunk(
                    content=chunk_text,
                    metadata={
                        "chunk_index": len(chunks),
                        "start_char": start,
                        "end_char": min(end, len(chars)),
                        "chunker": "character",
                    },
                )
            )
            next_start = start + chunk_size - overlap
            start = next_start if next_start > start else start + 1
        return chunks

    def chunk_document(self, document: Document, **kwargs: Any) -> list[Chunk]:
        """Chunk a full Document, propagating its metadata."""
        chunks = self.chunk(document.content, **kwargs)
        for ch in chunks:
            ch.metadata.update({"source": document.metadata.get("source", "")})
        return chunks

    def supported_formats(self) -> list[str]:
        return ["text/plain", "text/*"]
