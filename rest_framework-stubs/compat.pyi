from typing import Any, TypeAlias

from django.db.models import Q, QuerySet

try:
    from django.contrib.postgres import fields as postgres_fields
except ImportError:
    postgres_fields: TypeAlias = None  # type: ignore[no-redef]
try:
    import coreapi  # type: ignore[import-untyped]
except ImportError:
    coreapi: TypeAlias = None  # type: ignore[no-redef]
try:
    import uritemplate
except ImportError:
    uritemplate: TypeAlias = None  # type: ignore[no-redef]
try:
    import coreschema  # type: ignore[import-untyped]
except ImportError:
    coreschema: TypeAlias = None  # type: ignore[no-redef]
try:
    import yaml
except ImportError:
    yaml: TypeAlias = None  # type: ignore[no-redef]
try:
    import inflection  # type: ignore[import-not-found,unused-ignore]
except ImportError:
    inflection: TypeAlias = None  # type: ignore[no-redef]
try:
    import requests
except ImportError:
    requests: TypeAlias = None  # type: ignore[no-redef]
try:
    import pygments
except ImportError:
    pygments: TypeAlias = None  # type: ignore[no-redef]

try:
    import markdown
    from markdown.preprocessors import Preprocessor
    def apply_markdown(text: str) -> str: ...

    class CodeBlockPreprocessor(Preprocessor):
        pattern: Any
        formatter: Any
        def run(self, lines: list[str]) -> list[str]: ...

except ImportError:
    apply_markdown: TypeAlias = None  # type: ignore[no-redef]
    markdown: TypeAlias = None  # type: ignore[no-redef]

def pygments_css(style: Any) -> str | None: ...
def pygments_highlight(text: str, lang: str, style: Any) -> Any: ...
def md_filter_add_syntax_highlight(md: Any) -> bool: ...
def unicode_http_header(value: str | bytes) -> str: ...
def get_referenced_base_fields_from_q(q: Q) -> set[str]: ...

SHORT_SEPARATORS: tuple[str, str]
LONG_SEPARATORS: tuple[str, str]
INDENT_SEPARATORS: tuple[str, str]

__all__ = [
    "INDENT_SEPARATORS",
    "LONG_SEPARATORS",
    "SHORT_SEPARATORS",
    "CodeBlockPreprocessor",
    "Preprocessor",
    "QuerySet",
    "apply_markdown",
    "coreapi",
    "coreschema",
    "inflection",
    "markdown",
    "md_filter_add_syntax_highlight",
    "postgres_fields",
    "pygments",
    "pygments_css",
    "pygments_highlight",
    "requests",
    "unicode_http_header",
    "uritemplate",
    "yaml",
]
