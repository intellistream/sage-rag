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

    retriever = create_retriever("dense")
    assert retriever is not None
    assert hasattr(retriever, "retrieve")


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

    from sage.libs.rag.interface import create_pipeline

    pipeline = create_pipeline("simple")
    assert pipeline is not None
    assert hasattr(pipeline, "query")
