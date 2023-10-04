from collections.abc import Iterable, Mapping, Sequence
from typing import Any, TypeVar

from _typeshed import Incomplete
from django.db.models import Model, QuerySet
from rest_framework.request import Request
from rest_framework.views import APIView

_MT = TypeVar("_MT", bound=Model)

class BaseFilterBackend:
    def filter_queryset(self, request: Request, queryset: QuerySet[_MT], view: APIView) -> QuerySet[_MT]: ...
    def get_schema_fields(self, view: APIView) -> list[Any]: ...
    def get_schema_operation_parameters(self, view: APIView) -> Incomplete: ...

class SearchFilter(BaseFilterBackend):
    search_param: str
    template: str
    lookup_prefixes: dict[str, str]
    search_title: str
    search_description: str
    def get_search_fields(self, view: APIView, request: Request) -> Incomplete: ...
    def get_search_terms(self, request: Request) -> list[str]: ...
    def construct_search(self, field_name: str) -> str: ...
    def must_call_distinct(self, queryset: QuerySet, search_fields: Incomplete) -> bool: ...
    def to_html(self, request: Request, queryset: QuerySet, view: APIView) -> str: ...

class OrderingFilter(BaseFilterBackend):
    ordering_param: str
    ordering_fields: Sequence[str] | None
    ordering_title: str
    ordering_description: str
    template: str
    def get_ordering(self, request: Request, queryset: QuerySet, view: APIView) -> Sequence[str] | None: ...
    def get_default_ordering(self, view: APIView) -> Sequence[str] | None: ...
    def get_default_valid_fields(
        self, queryset: QuerySet, view: APIView, context: Mapping[str, Any] = ...
    ) -> list[tuple[str, str]]: ...
    def get_valid_fields(
        self, queryset: QuerySet, view: APIView, context: Mapping[str, Any] = ...
    ) -> list[tuple[str, str]]: ...
    def remove_invalid_fields(
        self, queryset: QuerySet, fields: Iterable[str], view: APIView, request: Request
    ) -> list[str]: ...
    def get_template_context(self, request: Request, queryset: QuerySet, view: APIView) -> dict[str, Any]: ...
    def to_html(self, request: Request, queryset: QuerySet, view: APIView) -> str: ...
