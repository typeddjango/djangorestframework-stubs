from typing import Any

from _typeshed import Incomplete
from django.core.management.base import BaseCommand

OPENAPI_MODE: str
COREAPI_MODE: str

class Command(BaseCommand):
    help: str
    def get_mode(self) -> Incomplete: ...
    def add_arguments(self, parser: Any) -> None: ...
    def handle(self, *args: Any, **options: Any) -> None: ...
    def get_renderer(self, format: str) -> Incomplete: ...
    def get_generator_class(self) -> Incomplete: ...
