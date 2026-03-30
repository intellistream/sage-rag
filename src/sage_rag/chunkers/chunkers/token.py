"""Token-based text chunker."""

from typing import Any

from sage.libs.rag.interface import Chunk, Document, TextChunker


class TokenChunker(TextChunker):
    """Chunk text by token count.

    Uses simple whitespace tokenization by default.
    Can be enhanced with actual tokenizer (tiktoken, etc.).

    Args:
        max_tokens: Maximum tokens per chunk.
        overlap_tokens: Number of overlapping tokens.

    Example:
        >>> from sage_libs.sage_rag import TokenChunker
        >>> chunker = TokenChunker(max_tokens=100, overlap_tokens=20)
        >>> chunks = chunker.chunk("Long text here...")
    """

    def __init__(self, max_tokens: int = 512, overlap_tokens: int = 50):
        self.max_tokens = max_tokens
        self.overlap_tokens = overlap_tokens
        self._tokenizer = None

    def chunk(self, text: str, **kwargs: Any) -> list[Chunk]:
        """Chunk text by token count.

        Args:
            text: Text to chunk.
            **kwargs: Additional options.

        Returns:
            List of text chunks.
        """
        max_tok = kwargs.get("max_tokens", self.max_tokens)
        overlap = kwargs.get("overlap_tokens", self.overlap_tokens)

        # Simple whitespace tokenization
        tokens = text.split()

        if not tokens:
            return []

        chunks = []
        i = 0

        while i < len(tokens):
            # Get chunk tokens
            chunk_tokens = tokens[i : i + max_tok]
            chunk_text = " ".join(chunk_tokens)

            # Find positions in original text
            start_pos = self._find_position(text, chunk_tokens[0], i)
            end_pos = start_pos + len(chunk_text)

            chunks.append(
                Chunk(
                    text=chunk_text,
                    start_pos=start_pos,
                    end_pos=end_pos,
                    metadata={
                        "chunker": "token",
                        "num_tokens": len(chunk_tokens),
                        "chunk_index": len(chunks),
                    },
                )
            )

            # Move window
            step = max_tok - overlap
            if step <= 0:
                step = max_tok
            i += step

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
            Chunk size (in tokens for this implementation)
        """
        return self.max_tokens

    def chunk_batch(self, texts: list[str], **kwargs: Any) -> list[list[Chunk]]:
        """Chunk multiple texts."""
        return [self.chunk(text, **kwargs) for text in texts]

    @property
    def chunk_size(self) -> int:
        """Return maximum tokens per chunk."""
        return self.max_tokens

    @property
    def chunk_overlap(self) -> int:
        """Return overlap tokens."""
        return self.overlap_tokens

    def _find_position(self, text: str, token: str, hint: int) -> int:
        """Find token position in text.

        Args:
            text: Original text.
            token: Token to find.
            hint: Hint for starting search position.

        Returns:
            Position of token in text.
        """
        # Simple search from beginning
        pos = text.find(token)
        return pos if pos >= 0 else 0
