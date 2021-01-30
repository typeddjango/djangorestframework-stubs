from typing import Any, Optional, Tuple, Union

import coreapi  # noqa: F401
import requests  # noqa: F401
from django.db.models import QuerySet

try:
    from django.contrib.postgres import fields as postgres_fields
except ImportError:
    postgres_fields = None  # type: ignore
try:
    import uritemplate
except ImportError:
    uritemplate = None  # type: ignore
try:
    import coreschema
except ImportError:
    coreschema = None  # type: ignore
try:
    import yaml
except ImportError:
    yaml = None  # type: ignore
try:
    import requests
except ImportError:
    requests = None  # type: ignore
try:
    import pygments
except ImportError:
    pygments = None  # type: ignore
try:
    import markdown
    def apply_markdown(text: str): ...

except ImportError:
    apply_markdown = None  # type: ignore
    markdown = None  # type: ignore

if markdown is not None and pygments is not None:
    from markdown.preprocessors import Preprocessor
    class CodeBlockPreprocessor(Preprocessor):
        pattern: Any = ...
        formatter: Any = ...
        def run(self, lines: Any): ...

def pygments_css(style: Any) -> Optional[str]: ...
def pygments_highlight(text: str, lang: str, style: Any) -> Any: ...
def md_filter_add_syntax_highlight(md: Any) -> bool: ...
def unicode_http_header(value: Union[str, bytes]) -> str: ...
def distinct(queryset: QuerySet, base: Optional[QuerySet]) -> QuerySet: ...

SHORT_SEPARATORS: Tuple[str, str]
LONG_SEPARATORS: Tuple[str, str]
INDENT_SEPARATORS: Tuple[str, str]

__all__ = [
    "coreapi",
    "coreschema",
    "requests",
    "postgres_fields",
    "QuerySet",
    "uritemplate",
    "yaml",
    "pygments",
    "markdown",
    "apply_markdown",
    "Preprocessor",
    "CodeBlockPreprocessor",
    "pygments_css",
    "pygments_highlight",
    "md_filter_add_syntax_highlight",
    "unicode_http_header",
    "distinct",
    "SHORT_SEPARATORS",
    "LONG_SEPARATORS",
    "INDENT_SEPARATORS",
]
