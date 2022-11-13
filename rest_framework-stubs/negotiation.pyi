from collections.abc import Iterable

from rest_framework.parsers import BaseParser
from rest_framework.renderers import BaseRenderer
from rest_framework.request import Request
from rest_framework.settings import api_settings

class BaseContentNegotiation:
    def select_parser(self, request: Request, parsers: Iterable[BaseParser]) -> BaseParser | None: ...
    def select_renderer(self, request: Request, renderers: Iterable[BaseRenderer], format_suffix: str | None = ...): ...

class DefaultContentNegotiation(BaseContentNegotiation):
    settings = api_settings
    def filter_renderers(self, renderers: Iterable[BaseRenderer], format: str) -> list[BaseRenderer]: ...
    def get_accept_list(self, request: Request) -> list[str]: ...
