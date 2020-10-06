from typing import Any, Callable, Dict, List, NamedTuple, Optional, Sequence, Tuple, Type, Union, TypeVar
from typing_extensions import TypedDict
from django.core.paginator import Page, Paginator
from django.db.models import QuerySet, Model
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView
from coreapi import Field as CoreAPIField

def _positive_int(integer_string: str, strict: bool = ..., cutoff: Optional[int] = ...) -> int: ...
def _divide_with_ceil(a: int, b: int) -> int: ...
def _get_displayed_page_numbers(current: int, final: int) -> List[Optional[int]]: ...
def _get_page_links(
    page_numbers: Sequence[Optional[int]], current: int, url_func: Callable[[int], str]
) -> List[PageLink]: ...
def _reverse_ordering(ordering_tuple: Sequence[str]) -> Tuple[str, ...]: ...

class Cursor(NamedTuple):
    offset: int
    reverse: bool
    position: Optional[int]

class PageLink(NamedTuple):
    url: Optional[str]
    number: Optional[int]
    is_active: bool
    is_break: bool

class HtmlContext(TypedDict):
    previous_url: str
    next_url: str

class HtmlContextWithPageLinks(HtmlContext):
    page_links: List[PageLink]

PAGE_BREAK: PageLink = ...

_MT = TypeVar("_MT", bound=Model)

class BasePagination:
    display_page_controls: bool = ...
    def get_paginated_response_schema(self, schema: Any): ...
    def get_paginated_response(self, data: Any) -> Response: ...
    def get_results(self, data: Dict[str, Any]) -> Any: ...
    def get_schema_fields(self, view: APIView) -> list: ...
    def get_schema_operation_parameters(self, view: APIView) -> list: ...
    def paginate_queryset(self, queryset: QuerySet, request: Request, view: Optional[APIView] = ...): ...
    def to_html(self) -> str: ...

class PageNumberPagination(BasePagination):
    display_page_controls: bool = ...
    django_paginator_class: Type[Paginator] = ...
    invalid_page_message: str = ...
    last_page_strings: Sequence[str] = ...
    max_page_size: Optional[int] = ...
    page_query_description: str = ...
    page_query_param: str = ...
    page_size_query_description: str = ...
    page_size_query_param: Optional[str] = ...
    page_size: Optional[int] = ...
    page: Optional[Page] = ...
    request: Optional[Request] = ...
    template: str = ...
    def paginate_queryset(
        self, queryset: QuerySet, request: Request, view: Optional[APIView] = ...
    ) -> Optional[List[Page]]: ...
    def get_paginated_response_schema(self, schema: Dict[str, Any]) -> Dict[str, Any]: ...
    def get_schema_fields(self, view: APIView) -> List[CoreAPIField]: ...
    def get_schema_operation_parameters(self, view: APIView) -> List[Dict[str, Any]]: ...
    def get_page_size(self, request: Request) -> Optional[int]: ...
    def get_next_link(self) -> Optional[str]: ...
    def get_previous_link(self) -> Optional[str]: ...
    def get_html_context(self) -> HtmlContextWithPageLinks: ...

class LimitOffsetPagination(BasePagination):
    count: Optional[int] = ...
    default_limit: Optional[int] = ...
    limit_query_description: str = ...
    limit_query_param: str = ...
    limit: Optional[int] = ...
    max_limit: Optional[int] = ...
    offset_query_description: str = ...
    offset_query_param: str = ...
    offset: Optional[int] = ...
    request: Optional[Request] = ...
    template: str = ...
    def paginate_queryset(
        self, queryset: QuerySet[_MT], request: Request, view: Optional[APIView] = ...
    ) -> Optional[List[_MT]]: ...
    def get_limit(self, request: Request) -> Optional[int]: ...
    def get_offset(self, request: Request) -> int: ...
    def get_next_link(self) -> Optional[str]: ...
    def get_previous_link(self) -> Optional[str]: ...
    def get_html_context(self) -> HtmlContextWithPageLinks: ...
    def get_count(self, queryset: Union[QuerySet, Sequence]) -> int: ...

class CursorPagination(BasePagination):
    base_url: Optional[str] = ...
    cursor_query_description: str = ...
    cursor_query_param: str = ...
    cursor: Optional[Cursor] = ...
    has_next: Optional[bool] = ...
    has_previous: Optional[bool] = ...
    invalid_cursor_message: str = ...
    max_page_size: Optional[int] = ...
    next_position: Optional[str] = ...
    offset_cutoff: int = ...
    ordering: Union[str, List[str], Tuple[str, ...]] = ...
    page_size_query_description: str = ...
    page_size_query_param: Optional[str] = ...
    page_size: Optional[int] = ...
    page: Optional[List[Any]] = ...
    previous_position: Optional[str] = ...
    template: str = ...
    def paginate_queryset(
        self, queryset: QuerySet[_MT], request: Request, view: Optional[APIView] = ...
    ) -> Optional[List[_MT]]: ...
    def get_page_size(self, request: Request) -> Optional[int]: ...
    def get_next_link(self) -> Optional[str]: ...
    def get_previous_link(self) -> Optional[str]: ...
    def get_html_context(self) -> HtmlContext: ...
    def get_ordering(self, request: Request, queryset: QuerySet, view: APIView) -> Tuple[str, ...]: ...
    def decode_cursor(self, request: Request) -> Optional[Cursor]: ...
    def encode_cursor(self, cursor: Cursor) -> str: ...
    def _get_position_from_instance(self, instance: Any, ordering: Sequence[str]) -> str: ...
