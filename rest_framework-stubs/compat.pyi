from django.conf.urls import url
from markdown.preprocessors import Preprocessor
from typing import Any

def get_original_route(urlpattern: Any): ...
def get_regex_pattern(urlpattern: Any): ...
def is_route_pattern(urlpattern: Any): ...
def make_url_resolver(regex: Any, urlpatterns: Any): ...
def unicode_http_header(value: Any): ...
def distinct(queryset: Any, base: Any): ...

HEADERID_EXT_PATH: str
LEVEL_PARAM: str

def apply_markdown(text: Any): ...

apply_markdown: Any

def pygments_highlight(text: Any, lang: Any, style: Any): ...
def pygments_css(style: Any): ...

class CodeBlockPreprocessor(Preprocessor):
    pattern: Any = ...
    formatter: Any = ...
    def run(self, lines: Any): ...

def md_filter_add_syntax_highlight(md: Any): ...
re_path = url
SHORT_SEPARATORS: Any
LONG_SEPARATORS: Any
INDENT_SEPARATORS: Any
PY36: Any
