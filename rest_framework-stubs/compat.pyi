from typing import Any

import coreapi  # noqa: F401
import requests  # noqa: F401
from django.conf.urls import url

try:
    import pygments
except ImportError:
    pygments = None

try:
    import markdown
    def apply_markdown(text: str): ...

except ImportError:
    apply_markdown = None  # type: ignore
    markdown = None

def get_original_route(urlpattern: Any): ...
def get_regex_pattern(urlpattern: Any): ...
def is_route_pattern(urlpattern: Any): ...
def make_url_resolver(regex: Any, urlpatterns: Any): ...
def unicode_http_header(value: Any): ...
def distinct(queryset: Any, base: Any): ...

HEADERID_EXT_PATH: str
LEVEL_PARAM: str

def pygments_highlight(text: str, lang: str, style: Any): ...
def pygments_css(style: Any): ...

if markdown is not None and pygments is not None:
    from markdown.preprocessors import Preprocessor
    class CodeBlockPreprocessor(Preprocessor):
        pattern: Any = ...
        formatter: Any = ...
        def run(self, lines: Any): ...

def md_filter_add_syntax_highlight(md: Any): ...

re_path = url
SHORT_SEPARATORS: tuple
LONG_SEPARATORS: tuple
INDENT_SEPARATORS: tuple
PY36: Any
