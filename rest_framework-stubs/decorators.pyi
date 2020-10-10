from typing import Any, Callable, List, Mapping, Optional, Sequence, Type, Union

from rest_framework.authentication import BaseAuthentication
from rest_framework.parsers import BaseParser
from rest_framework.permissions import BasePermission
from rest_framework.renderers import BaseRenderer
from rest_framework.schemas.inspectors import ViewInspector
from rest_framework.throttling import BaseThrottle
from rest_framework.views import APIView, AsView  # noqa: F401
from typing_extensions import Literal

class MethodMapper(dict):
    def __init__(self, action: Callable, methods: Sequence[str]) -> None: ...
    def _map(self, method: str, func: Callable) -> Callable: ...
    def get(self, func: Callable) -> Callable: ...  # type: ignore
    def post(self, func: Callable) -> Callable: ...
    def put(self, func: Callable) -> Callable: ...
    def patch(self, func: Callable) -> Callable: ...
    def delete(self, func: Callable) -> Callable: ...
    def head(self, func: Callable) -> Callable: ...
    def options(self, func: Callable) -> Callable: ...
    def trace(self, func: Callable) -> Callable: ...

_LOWER_CASE_HTTP_VERBS = List[
    Union[
        Literal["get"],
        Literal["post"],
        Literal["delete"],
        Literal["put"],
        Literal["patch"],
        Literal["trace"],
        Literal["options"],
    ]
]

_MIXED_CASE_HTTP_VERBS = List[
    Union[
        Literal["GET"],
        Literal["POST"],
        Literal["DELETE"],
        Literal["PUT"],
        Literal["PATCH"],
        Literal["TRACE"],
        Literal["OPTIONS"],
        Literal["get"],
        Literal["post"],
        Literal["delete"],
        Literal["put"],
        Literal["patch"],
        Literal["trace"],
        Literal["options"],
    ]
]

class ViewSetAction:
    detail: bool
    methods: _LOWER_CASE_HTTP_VERBS
    url_path: str
    url_name: str
    kwargs: Mapping[str, Any]
    mapping: MethodMapper
    def __call__(self, *args, **kwargs): ...

def api_view(http_method_names: Optional[Sequence[str]] = ...) -> Callable[[Callable], AsView]: ...
def renderer_classes(
    renderer_classes: Sequence[Union[BaseRenderer, Type[BaseRenderer]]]
) -> Callable[[Callable], Callable]: ...
def parser_classes(parser_classes: Sequence[Union[BaseParser, Type[BaseParser]]]) -> Callable[[Callable], Callable]: ...
def authentication_classes(
    authentication_classes: Sequence[Union[BaseAuthentication, Type[BaseAuthentication]]]
) -> Callable[[Callable], Callable]: ...
def throttle_classes(
    throttle_classes: Sequence[Union[BaseThrottle, Type[BaseThrottle]]]
) -> Callable[[Callable], Callable]: ...
def permission_classes(
    permission_classes: Sequence[Union[BasePermission, Type[BasePermission]]]
) -> Callable[[Callable], Callable]: ...
def schema(view_inspector: Optional[Union[ViewInspector, Type[ViewInspector]]]) -> Callable[[Callable], Callable]: ...
def action(
    methods: Optional[_MIXED_CASE_HTTP_VERBS] = ...,
    detail: bool = ...,
    url_path: Optional[str] = ...,
    url_name: Optional[str] = ...,
    suffix: Optional[str] = ...,
    name: Optional[str] = ...,
    **kwargs: Any,
) -> Callable[[Callable], ViewSetAction]: ...
