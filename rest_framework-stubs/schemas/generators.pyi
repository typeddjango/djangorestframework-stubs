from typing import Any, Iterable, List, Optional, Pattern, Sequence, Type, Union

from django.db.models.base import Model
from django.http.request import HttpRequest
from rest_framework.compat import coreapi

def common_path(paths: Iterable[str]) -> str: ...
def get_pk_name(model: Type[Model]) -> str: ...
def is_api_view(callback: Any) -> bool: ...

class EndpointEnumerator:
    patterns: List[Any]
    def __init__(self, patterns: Optional[List[Any]] = ..., urlconf: Optional[str] = ...) -> None: ...
    def get_api_endpoints(self, patterns: Optional[List[Any]] = ..., prefix: str = ...) -> List[_APIEndpoint]: ...
    def get_path_from_regex(self, path_regex: Union[Pattern, str]) -> str: ...
    def should_include_endpoint(self, path: str, callback: Any) -> bool: ...
    def get_allowed_methods(self, callback: Any) -> List[str]: ...

class BaseSchemaGenerator:
    endpoint_inspector_cls: Type[EndpointEnumerator] = ...
    coerce_path_pk: Optional[bool] = ...
    patterns: List[Any] = ...
    urlconf: Optional[str] = ...
    title: Optional[str] = ...
    description: Optional[str] = ...
    version: Optional[str] = ...
    url: Optional[str] = ...
    endpoints: Optional[Sequence[_APIEndpoint]] = ...
    def __init__(
        self,
        title: Optional[str] = ...,
        url: Optional[str] = ...,
        description: Optional[str] = ...,
        patterns: Optional[List[Any]] = ...,
        urlconf: Optional[str] = ...,
        version: Optional[str] = ...,
    ) -> None: ...
    def create_view(self, callback: Any, method: str, request: Optional[HttpRequest] = ...) -> Any: ...
    def coerce_path(self, path: str, method: str, view) -> str: ...
    def get_schema(self, request: Optional[HttpRequest] = ..., public: bool = ...) -> Optional[coreapi.Document]: ...
    def has_view_permissions(self, path: str, method: str, view) -> bool: ...
