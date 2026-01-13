"""Sentence-based text chunker."""

import re
from typing import Any

from sage.libs.rag.interface import Chunk, Document, TextChunker


class SentenceChunker(TextChunker):
    """Chunk text by sentences.

    Args:
        max_sentences: Maximum sentences per chunk.
        overlap_sentences: Number of overlapping sentences between chunks.

    Example:
        >>> from sage_libs.sage_rag import SentenceChunker
        >>> chunker = SentenceChunker(max_sentences=5)
        >>> chunks = chunker.chunk("Hello world. How are you?")
    """

    # Sentence boundary pattern
    SENTENCE_PATTERN = re.compile(r"(?<=[.!?])\s+")

    def __init__(self, max_sentences: int = 5, overlap_sentences: int = 1):
        self.max_sentences = max_sentences
        self.overlap_sentences = overlap_sentences

    def chunk(self, text: str, **kwargs: Any) -> list[Chunk]:
        """Chunk text into sentence-based chunks.

        Args:
            text: Text to chunk.
            **kwargs: Additional options (max_sentences, overlap_sentences).

        Returns:
            List of text chunks.
        """
        max_sent = kwargs.get("max_sentences", self.max_sentences)
        overlap = kwargs.get("overlap_sentences", self.overlap_sentences)

        # Split into sentences
        sentences = self.SENTENCE_PATTERN.split(text.strip())
        sentences = [s.strip() for s in sentences if s.strip()]

        if not sentences:
            return []

        chunks = []
        i = 0
        pos = 0

        while i < len(sentences):
            # Get chunk sentences
            chunk_sentences = sentences[i : i + max_sent]
            chunk_text = " ".join(chunk_sentences)

            # Find positions
            start_pos = text.find(chunk_sentences[0], pos)
            if start_pos == -1:
                start_pos = pos
            end_pos = start_pos + len(chunk_text)

            chunks.append(
                Chunk(
                    text=chunk_text,
                    start_pos=start_pos,
                    end_pos=end_pos,
                    metadata={
                        "chunker": "sentence",
                        "num_sentences": len(chunk_sentences),
                        "chunk_index": len(chunks),
                    },
                )
            )

            # Move window
            i += max_sent - overlap
            pos = start_pos + 1

        return chunks

    def chunk_document(self, document: Document, **kwargs: Any) -> list[Chunk]:
        """Chunk a document while preserving metadata.

        Args:
            document: Document to chunk
            **kwargs: Chunker-specific options

        Returns:
            List of chunks, each inheriting document metadata
        """
        chunks = self.chunk(document.content, **kwargs)
        # Add document metadata to each chunk
        for chunk in chunks:
            chunk.metadata.update(
                {
                    "source": document.metadata.get("source", ""),
                    "document_metadata": document.metadata,
                }
            )
        return chunks

    def get_chunk_size(self) -> int:
        """Get the configured chunk size.

        Returns:
            Chunk size (in sentences for this implementation)
        """
        return self.max_sentences

    def chunk_batch(self, texts: list[str], **kwargs: Any) -> list[list[Chunk]]:
        """Chunk multiple texts."""
        return [self.chunk(text, **kwargs) for text in texts]

    @property
    def chunk_size(self) -> int:
        """Return maximum sentences per chunk."""
        return self.max_sentences

    @property
    def chunk_overlap(self) -> int:
        """Return overlap sentences."""
        return self.overlap_sentences
