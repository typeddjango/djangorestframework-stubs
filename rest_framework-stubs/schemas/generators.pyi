from collections.abc import Iterable, Sequence
from types import ModuleType
from typing import Any

from django.db.models.base import Model
from rest_framework.compat import coreapi
from rest_framework.request import Request
from rest_framework.urlpatterns import _AnyURL
from rest_framework.views import APIView
from typing_extensions import TypeAlias

def common_path(paths: Iterable[str]) -> str: ...
def get_pk_name(model: type[Model]) -> str: ...
def is_api_view(callback: Any) -> bool: ...

_APIEndpoint: TypeAlias = tuple[str, str, Any]

class EndpointEnumerator:
    patterns: Sequence[_AnyURL] | None
    def __init__(
        self,
        patterns: Sequence[_AnyURL] | None = ...,
        urlconf: str | ModuleType | None = ...,
    ) -> None: ...
    def get_api_endpoints(self, patterns: Iterable[_AnyURL] | None = ..., prefix: str = ...) -> list[_APIEndpoint]: ...
    def get_path_from_regex(self, path_regex: str) -> str: ...
    def should_include_endpoint(self, path: str, callback: Any) -> bool: ...
    def get_allowed_methods(self, callback: Any) -> list[str]: ...

class BaseSchemaGenerator:
    endpoint_inspector_cls: type[EndpointEnumerator]
    coerce_path_pk: bool | None
    patterns: Sequence[_AnyURL] | None
    urlconf: str | None
    title: str | None
    description: str | None
    version: str | None
    url: str | None
    endpoints: Sequence[_APIEndpoint] | None
    def __init__(
        self,
        title: str | None = ...,
        url: str | None = ...,
        description: str | None = ...,
        patterns: Sequence[_AnyURL] | None = ...,
        urlconf: str | None = ...,
        version: str | None = ...,
    ) -> None: ...
    def create_view(self, callback: Any, method: str, request: Request | None = ...) -> Any: ...
    def coerce_path(self, path: str, method: str, view: APIView) -> str: ...
    def get_schema(self, request: Request | None = ..., public: bool = ...) -> coreapi.Document | None: ...
    def has_view_permissions(self, path: str, method: str, view: APIView) -> bool: ...
