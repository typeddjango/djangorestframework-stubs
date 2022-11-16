from collections.abc import Callable, Iterable, Mapping
from typing import Any, NamedTuple

from django.utils.deprecation import RenameMethodsBase
from rest_framework import views
from rest_framework.renderers import BaseRenderer
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.schemas import SchemaGenerator
from rest_framework.schemas.views import SchemaView
from rest_framework.urlpatterns import _AnyURL
from rest_framework.viewsets import ViewSetMixin

class Route(NamedTuple):
    url: str
    mapping: dict[str, str]
    name: str
    detail: bool
    initkwargs: dict[str, Any]

class DynamicRoute(NamedTuple):
    url: str
    name: str
    detail: bool
    initkwargs: dict[str, Any]

def escape_curly_brackets(url_path: str) -> str: ...
def flatten(list_of_lists: Iterable[Iterable[Any]]) -> Iterable[Any]: ...

class RenameRouterMethods(RenameMethodsBase):
    renamed_methods: Iterable[str | Callable]

class BaseRouter(metaclass=RenameRouterMethods):
    registry: list[tuple[str, type[ViewSetMixin], str]]
    def register(
        self, prefix: str, viewset: type[ViewSetMixin], basename: str | None = ..., base_name: str | None = ...
    ) -> None: ...
    def get_default_basename(self, viewset: type[ViewSetMixin]) -> str: ...
    def get_urls(self) -> list[_AnyURL]: ...
    @property
    def urls(self) -> list[_AnyURL]: ...

class SimpleRouter(BaseRouter):
    routes: list[Route | DynamicRoute]
    trailing_slash: str
    def __init__(self, trailing_slash: bool = ...) -> None: ...
    def get_routes(self, viewset: type[ViewSetMixin]) -> list[Route]: ...
    def _get_dynamic_route(self, route: DynamicRoute, action: Any) -> Route: ...
    def get_method_map(self, viewset: type[ViewSetMixin], method_map: Mapping[str, str]) -> dict[str, str]: ...
    def get_lookup_regex(self, viewset: type[ViewSetMixin], lookup_prefix: str = ...) -> str: ...

class APIRootView(views.APIView):
    _ignore_model_permissions: bool
    api_root_dict: dict[str, str] | None
    def get(self, request: Request, *args: Any, **kwargs: Any) -> Response: ...

class DefaultRouter(SimpleRouter):
    include_root_view: bool
    include_format_suffixes: bool
    root_view_name: str
    default_schema_renderers: Any
    APIRootView = APIRootView
    APISchemaView = SchemaView
    SchemaGenerator = SchemaGenerator

    root_renderers: list[type[BaseRenderer]]
    def __init__(self, *args: Any, **kwargs: Any) -> None: ...
    def get_api_root_view(self, api_urls: Any | None = ...) -> Callable: ...
