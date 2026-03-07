"""Deprecated namespace shim — use :mod:`sage_rag` directly.

This ``sage_libs.sage_rag`` path will be removed in a future release.
Please update your imports::

    # Old (deprecated)
    from sage_libs.sage_rag import TextLoader

    # New
    from sage_rag import TextLoader
    # or: pip install isage-rag
"""

import warnings

warnings.warn(
    "sage_libs.sage_rag is deprecated. Import from sage_rag instead: pip install isage-rag",
    DeprecationWarning,
    stacklevel=2,
)

from sage_rag import *  # noqa: F401, F403, E402
from sage_rag import __all__  # noqa: F401, E402
