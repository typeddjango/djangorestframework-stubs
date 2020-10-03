from typing import Any, Dict, Iterable, List, Mapping, Optional, Sequence, Tuple, TypeVar

from django.db.models.query import QuerySet
from rest_framework.request import Request
from rest_framework.views import APIView

_Q = TypeVar("_Q", bound=QuerySet)

class BaseFilterBackend:
    def filter_queryset(self, request: Request, queryset: _Q, view) -> _Q: ...
    def get_schema_fields(self, view) -> List[Any]: ...
    def get_schema_operation_parameters(self, view: APIView): ...

class SearchFilter(BaseFilterBackend):
    search_param: str = ...
    template: str = ...
    lookup_prefixes: Dict[str, str] = ...
    search_title: str = ...
    search_description: str = ...
    def get_search_fields(self, view: APIView, request: Request): ...
    def get_search_terms(self, request: Request) -> List[str]: ...
    def construct_search(self, field_name: str) -> str: ...
    def must_call_distinct(self, queryset: QuerySet, search_fields) -> bool: ...
    def to_html(self, request: Request, queryset: QuerySet, view) -> str: ...

class OrderingFilter(BaseFilterBackend):
    ordering_param: str = ...
    ordering_fields: Optional[Sequence[str]] = ...
    ordering_title: str = ...
    ordering_description: str = ...
    template: str = ...
    def get_ordering(self, request: Request, queryset: QuerySet, view) -> Sequence[str]: ...
    def get_default_ordering(self, view) -> Sequence[str]: ...
    def get_default_valid_fields(
        self, queryset: QuerySet, view, context: Mapping[str, Any] = ...
    ) -> List[Tuple[str, str]]: ...
    def get_valid_fields(self, queryset: QuerySet, view, context: Mapping[str, Any] = ...) -> List[Tuple[str, str]]: ...
    def remove_invalid_fields(self, queryset: QuerySet, fields: Iterable[str], view, request: Request) -> List[str]: ...
    def get_template_context(self, request: Request, queryset: QuerySet, view) -> Dict[str, Any]: ...
    def to_html(self, request: Request, queryset: QuerySet, view) -> str: ...
