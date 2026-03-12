from _typeshed import Incomplete
from typing import Any

from django.core.management.base import BaseCommand
from typing_extensions import override

OPENAPI_MODE: str
COREAPI_MODE: str

class Command(BaseCommand):
    help: str
    def get_mode(self) -> Incomplete: ...
    @override
    def add_arguments(self, parser: Any) -> None: ...
    @override
    def handle(self, *args: Any, **options: Any) -> None: ...
    def get_renderer(self, format: str) -> Incomplete: ...
    def get_generator_class(self) -> Incomplete: ...
