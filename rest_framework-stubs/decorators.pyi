from collections.abc import Callable, Mapping, Sequence
from typing import Any, Protocol, TypeVar

from django.http import HttpRequest
from django.http.response import HttpResponseBase
from rest_framework.authentication import BaseAuthentication
from rest_framework.parsers import BaseParser
from rest_framework.permissions import _PermissionClass
from rest_framework.renderers import BaseRenderer
from rest_framework.request import Request
from rest_framework.schemas.inspectors import ViewInspector
from rest_framework.throttling import BaseThrottle
from rest_framework.views import APIView, AsView  # noqa: F401
from typing_extensions import Concatenate, Literal, ParamSpec, TypeAlias

_View = TypeVar("_View", bound=Callable[..., HttpResponseBase])
_P = ParamSpec("_P")
_RESP = TypeVar("_RESP", bound=HttpResponseBase)

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

_LOWER_CASE_HTTP_VERBS: TypeAlias = list[
    Literal[
        "get",
        "post",
        "delete",
        "put",
        "patch",
        "trace",
        "head",
        "options",
    ]
]

_MIXED_CASE_HTTP_VERBS: TypeAlias = list[
    Literal[
        "GET",
        "POST",
        "DELETE",
        "PUT",
        "PATCH",
        "TRACE",
        "HEAD",
        "OPTIONS",
        "get",
        "post",
        "delete",
        "put",
        "patch",
        "trace",
        "head",
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

def api_view(
    http_method_names: Sequence[str] | None = ...,
) -> Callable[[Callable[Concatenate[Request, _P], _RESP]], AsView[Callable[Concatenate[HttpRequest, _P], _RESP]]]: ...
def renderer_classes(renderer_classes: Sequence[BaseRenderer | type[BaseRenderer]]) -> Callable[[_View], _View]: ...
def parser_classes(parser_classes: Sequence[BaseParser | type[BaseParser]]) -> Callable[[_View], _View]: ...
def authentication_classes(
    authentication_classes: Sequence[BaseAuthentication | type[BaseAuthentication]],
) -> Callable[[_View], _View]: ...
def throttle_classes(throttle_classes: Sequence[BaseThrottle | type[BaseThrottle]]) -> Callable[[_View], _View]: ...
def permission_classes(permission_classes: Sequence[_PermissionClass]) -> Callable[[_View], _View]: ...
def schema(view_inspector: ViewInspector | type[ViewInspector] | None) -> Callable[[_View], _View]: ...
def action(
    methods: _MIXED_CASE_HTTP_VERBS | None = ...,
    detail: bool = ...,
    url_path: str | None = ...,
    url_name: str | None = ...,
    suffix: str | None = ...,
    name: str | None = ...,
    **kwargs: Any,
) -> Callable[[_View], ViewSetAction[_View]]: ...
