from typing import Iterable, List, Optional

from rest_framework.parsers import BaseParser
from rest_framework.renderers import BaseRenderer
from rest_framework.request import Request
from rest_framework.settings import api_settings

class BaseContentNegotiation(object):
    def select_parser(self, request: Request, parsers: Iterable[BaseParser]) -> Optional[BaseParser]: ...
    def select_renderer(
        self, request: Request, renderers: Iterable[BaseRenderer], format_suffix: Optional[str] = ...
    ): ...

class DefaultContentNegotiation(BaseContentNegotiation):
    settings = api_settings
    def filter_renderers(self, renderers: Iterable[BaseRenderer], format: str) -> List[BaseRenderer]: ...
    def get_accept_list(self, request: Request) -> List[str]: ...
