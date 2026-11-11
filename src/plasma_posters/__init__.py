"""Scientific posters from Python: a layout of text, figures and equations written to a print-ready PDF."""

from importlib.metadata import PackageNotFoundError, version

import scope_profiler as sp

from plasma_posters._profiling import PROFILE_TAGS

try:
    __version__ = version("plasma-posters")
except PackageNotFoundError:  # not installed, e.g. run from a source tree
    __version__ = "0.0.0+unknown"

from plasma_posters.poster import (  # noqa: E402
    Block,
    Poster,
    compile_latex,
    preview,
    preview_pages,
)

__all__ = [
    "Block",
    "Poster",
    "__version__",
    "compile_latex",
    "preview",
    "preview_pages",
]

# The decorated functions pick the tag up, so registering after the imports is in time.
sp.register_opt_in_tag(*PROFILE_TAGS)
