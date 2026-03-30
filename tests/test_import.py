"""Import smoke tests for sage-rag."""



def test_import_package():
    """Test that package can be imported."""
    import sage_rag
    from sage_rag._version import __version__ as pkg_version

    assert hasattr(sage_rag, "__version__")
    assert sage_rag.__version__ == pkg_version


def test_import_version():
    """Test version format is four-segment."""
    from sage_libs.sage_rag import __version__

    parts = __version__.split(".")
    assert len(parts) == 4, f"Expected 4 segments, got {len(parts)}: {__version__}"


def test_import_loaders():
    """Test that loader classes can be imported."""
    from sage_libs.sage_rag import MarkdownLoader, TextLoader

    assert TextLoader is not None
    assert MarkdownLoader is not None


def test_import_chunkers():
    """Test that chunker classes can be imported."""
    from sage_libs.sage_rag import SentenceChunker, TokenChunker

    assert SentenceChunker is not None
    assert TokenChunker is not None


def test_import_retrievers():
    """Test that retriever classes can be imported."""
    from sage_libs.sage_rag import DenseRetriever

    assert DenseRetriever is not None


def test_import_rerankers():
    """Test that reranker classes can be imported."""
    from sage_libs.sage_rag import CrossEncoderReranker

    assert CrossEncoderReranker is not None


def test_import_pipelines():
    """Test that pipeline classes can be imported."""
    from sage_libs.sage_rag import SimpleRAGPipeline

    assert SimpleRAGPipeline is not None
