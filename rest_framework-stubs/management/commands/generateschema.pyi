from typing import Any

from django.core.management.base import BaseCommand
from rest_framework.renderers import BaseRenderer
from typing_extensions import override

class Command(BaseCommand):
    help: str
    @override
    def add_arguments(self, parser: Any) -> None: ...
    @override
    def handle(self, *args: Any, **options: Any) -> None: ...
    def get_renderer(self, format: str) -> BaseRenderer: ...
