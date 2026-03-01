"""Test SAGE interface registration for sage-rag."""



def test_loader_registration():
    """Test that loaders are registered to SAGE interface."""

    from sage.libs.rag.interface import registered_loaders

    loaders = registered_loaders()
    assert "text" in loaders, f"'text' not in registered loaders: {loaders}"
    assert "markdown" in loaders, f"'markdown' not in registered loaders: {loaders}"


def test_create_text_loader():
    """Test creating a TextLoader via factory."""

    from sage.libs.rag.interface import create_loader

    loader = create_loader("text")
    assert loader is not None
    assert hasattr(loader, "load")


def test_chunker_registration():
    """Test that chunkers are registered to SAGE interface."""

    from sage.libs.rag.interface import registered_chunkers

    chunkers = registered_chunkers()
    assert "sentence" in chunkers
    assert "token" in chunkers


def test_create_chunker():
    """Test creating a chunker via factory."""

    from sage.libs.rag.interface import create_chunker

    chunker = create_chunker("sentence")
    assert chunker is not None
    assert hasattr(chunker, "chunk")


def test_retriever_registration():
    """Test that retrievers are registered to SAGE interface."""

    from sage.libs.rag.interface import registered_retrievers

    retrievers = registered_retrievers()
    assert "dense" in retrievers


def test_create_retriever():
    """Test creating a retriever via factory."""

    from sage.libs.rag.interface import create_retriever

    class _MockEmbedding:
        def encode(self, _text: str):
            class _Vector:
                def tolist(self) -> list[float]:
                    return [1.0]

            return _Vector()

    class _MockVectorStore:
        def add(self, *_args, **_kwargs):
            return None

        def build_index(self):
            return None

        def search(self, *_args, **_kwargs):
            return []

        def delete(self, *_args, **_kwargs):
            return None

    retriever = create_retriever(
        "dense",
        embedding_model=_MockEmbedding(),
        vector_store=_MockVectorStore(),
    )
    assert retriever is not None
    assert hasattr(retriever, "retrieve")


def test_create_retriever_fail_fast_without_dependencies():
    """Test that retriever creation fails when required dependencies are missing."""

    import pytest
    from sage.libs.rag.interface import create_retriever

    with pytest.raises(TypeError):
        create_retriever("dense")


def test_reranker_registration():
    """Test that rerankers are registered to SAGE interface."""

    from sage.libs.rag.interface import registered_rerankers

    rerankers = registered_rerankers()
    assert "cross_encoder" in rerankers


def test_pipeline_registration():
    """Test that pipelines are registered to SAGE interface."""

    from sage.libs.rag.interface import registered_pipelines

    pipelines = registered_pipelines()
    assert "simple" in pipelines


def test_create_pipeline():
    """Test creating a pipeline via factory."""

    from sage.libs.rag.interface import create_loader, create_pipeline, create_retriever

    class _MockEmbedding:
        def encode(self, _text: str):
            class _Vector:
                def tolist(self) -> list[float]:
                    return [1.0]

            return _Vector()

    class _MockVectorStore:
        def add(self, *_args, **_kwargs):
            return None

        def build_index(self):
            return None

        def search(self, *_args, **_kwargs):
            return []

        def delete(self, *_args, **_kwargs):
            return None

    class _MockGenerator:
        def generate(self, _prompt: str) -> str:
            return "ok"

    pipeline = create_pipeline(
        "simple",
        loader=create_loader("text"),
        retriever=create_retriever(
            "dense",
            embedding_model=_MockEmbedding(),
            vector_store=_MockVectorStore(),
        ),
        generator=_MockGenerator(),
    )
    assert pipeline is not None
    assert hasattr(pipeline, "query")
