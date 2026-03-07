"""Transformer-tokenizer-based text chunker.

Moved from sage.libs.rag.chunk — concrete implementation belongs in sage-rag (L3 algo).
Requires: pip install isage-rag[llm]  (transformers package)
"""

from __future__ import annotations

from typing import Any

from sage.libs.rag.interface import Chunk, Document, TextChunker


class TransformerTokenChunker(TextChunker):
    """Split text into token-based chunks using a HuggingFace tokenizer.

    Unlike :class:`TokenChunker` (which uses simple whitespace tokenisation),
    this class uses a real sub-word tokenizer so that ``chunk_size`` is measured
    in *model tokens* rather than whitespace tokens.

    Args:
        model_name: HuggingFace tokenizer model name (default: ``"BAAI/bge-m3"``).
        chunk_size: Maximum number of tokens per chunk (default: 512).
        chunk_overlap: Number of overlapping tokens between consecutive chunks (default: 50).

    Note:
        Requires the ``transformers`` package::

            pip install transformers

    Example:
        >>> chunker = TransformerTokenChunker(chunk_size=256, chunk_overlap=32)
        >>> chunks = chunker.chunk("Long document text ...")
    """

    def __init__(
        self,
        model_name: str = "BAAI/bge-m3",
        chunk_size: int = 512,
        chunk_overlap: int = 50,
    ) -> None:
        self.model_name = model_name
        self.chunk_size = chunk_size
        self.chunk_overlap = chunk_overlap

        try:
            from transformers import AutoTokenizer  # type: ignore[import-untyped]

            self._tokenizer = AutoTokenizer.from_pretrained(model_name)
        except ImportError as exc:
            raise ImportError(
                "TransformerTokenChunker requires the 'transformers' package. "
                "Install it with: pip install transformers"
            ) from exc

    def chunk(self, text: str, **kwargs: Any) -> list[Chunk]:
        """Split text into token-bounded chunks.

        Args:
            text: The text to split.
            **kwargs: chunk_size / chunk_overlap overrides.

        Returns:
            List of :class:`~sage.libs.rag.interface.Chunk` objects.
        """
        chunk_size = kwargs.get("chunk_size", self.chunk_size)
        chunk_overlap = kwargs.get("chunk_overlap", self.chunk_overlap)

        token_ids: list[int] = self._tokenizer.encode(text, add_special_tokens=False)

        if not token_ids:
            return [Chunk(content="", metadata={"chunk_index": 0, "chunker": "transformer_token"})]

        chunks: list[Chunk] = []
        start = 0
        while start < len(token_ids):
            end = start + chunk_size
            chunk_ids = token_ids[start:end]
            chunk_text: str = self._tokenizer.decode(chunk_ids, skip_special_tokens=True)
            chunks.append(
                Chunk(
                    content=chunk_text,
                    metadata={
                        "chunk_index": len(chunks),
                        "token_start": start,
                        "token_end": min(end, len(token_ids)),
                        "chunker": "transformer_token",
                        "model": self.model_name,
                    },
                )
            )
            next_start = start + chunk_size - chunk_overlap
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
