from typing import Any, Callable, List, Mapping, Optional, Sequence, Type, Union, Protocol, TypeVar

from django.http.response import HttpResponseBase
from rest_framework.authentication import BaseAuthentication
from rest_framework.parsers import BaseParser
from rest_framework.permissions import BasePermission
from rest_framework.renderers import BaseRenderer
from rest_framework.schemas.inspectors import ViewInspector
from rest_framework.throttling import BaseThrottle
from rest_framework.views import APIView, AsView  # noqa: F401
from typing_extensions import Literal

_View = TypeVar("_View", bound=Callable[..., HttpResponseBase])

class MethodMapper(dict):
    def __init__(self, action: _View, methods: Sequence[str]) -> None: ...
    def _map(self, method: str, func: _View) -> _View: ...
    def get(self, func: _View) -> _View: ...  # type: ignore
    def post(self, func: _View) -> _View: ...
    def put(self, func: _View) -> _View: ...
    def patch(self, func: _View) -> _View: ...
    def delete(self, func: _View) -> _View: ...
    def head(self, func: _View) -> _View: ...
    def options(self, func: _View) -> _View: ...
    def trace(self, func: _View) -> _View: ...

_LOWER_CASE_HTTP_VERBS = List[
    Literal[
        "get",
        "post",
        "delete",
        "put",
        "patch",
        "trace",
        "options",
    ]
]

_MIXED_CASE_HTTP_VERBS = List[
    Literal[
        "GET",
        "POST",
        "DELETE",
        "PUT",
        "PATCH",
        "TRACE",
        "OPTIONS",
        "get",
        "post",
        "delete",
        "put",
        "patch",
        "trace",
        "options",
    ]
]

class ViewSetAction(Protocol[_View]):
    detail: bool
    methods: _LOWER_CASE_HTTP_VERBS
    url_path: str
    url_name: str
    kwargs: Mapping[str, Any]
    mapping: MethodMapper
    __call__: _View

def api_view(http_method_names: Optional[Sequence[str]] = ...) -> Callable[[_View], AsView[_View]]: ...
def renderer_classes(
    renderer_classes: Sequence[Union[BaseRenderer, Type[BaseRenderer]]]
) -> Callable[[_View], _View]: ...
def parser_classes(parser_classes: Sequence[Union[BaseParser, Type[BaseParser]]]) -> Callable[[_View], _View]: ...
def authentication_classes(
    authentication_classes: Sequence[Union[BaseAuthentication, Type[BaseAuthentication]]]
) -> Callable[[_View], _View]: ...
def throttle_classes(
    throttle_classes: Sequence[Union[BaseThrottle, Type[BaseThrottle]]]
) -> Callable[[_View], _View]: ...
def permission_classes(
    permission_classes: Sequence[Union[BasePermission, Type[BasePermission]]]
) -> Callable[[_View], _View]: ...
def schema(view_inspector: Optional[Union[ViewInspector, Type[ViewInspector]]]) -> Callable[[_View], _View]: ...
def action(
    methods: Optional[_MIXED_CASE_HTTP_VERBS] = ...,
    detail: bool = ...,
    url_path: Optional[str] = ...,
    url_name: Optional[str] = ...,
    suffix: Optional[str] = ...,
    name: Optional[str] = ...,
    **kwargs: Any,
) -> Callable[[_View], ViewSetAction[_View]]: ...
