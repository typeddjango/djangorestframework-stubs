from collections.abc import Mapping, Sequence
from typing import Any

from django.http import HttpRequest, JsonResponse
from django_stubs_ext import StrOrPromise
from rest_framework.renderers import BaseRenderer
from rest_framework.request import Request
from typing_extensions import TypeAlias, TypedDict

class ErrorDetail(str):
    code: str | None
    def __new__(cls, string: str, code: str | None = ...): ...

_Detail: TypeAlias = ErrorDetail | list[ErrorDetail] | dict[str, ErrorDetail]
# NB! _APIExceptionInput doesn't technically handle Sequence/Mapping, but only list/tuple/dict.
# But since list/tuple are non-covariant types, we run into issues with union type compatibility for input params.
# So use the more relaxed Sequence/Mapping for now.
_APIExceptionInput: TypeAlias = (
    _Detail | StrOrPromise | Sequence[_APIExceptionInput] | Mapping[str, _APIExceptionInput] | None
)
_ErrorCodes: TypeAlias = str | None | list[_ErrorCodes] | dict[str, _ErrorCodes]

class _FullDetailDict(TypedDict):
    message: ErrorDetail
    code: str | None

_ErrorFullDetails: TypeAlias = _FullDetailDict | list[_FullDetailDict] | dict[str, _FullDetailDict]

def _get_error_details(data: _APIExceptionInput, default_code: str | None = ...) -> _Detail: ...
def _get_codes(detail: _Detail) -> _ErrorCodes: ...
def _get_full_details(detail: _Detail) -> _ErrorFullDetails: ...

class APIException(Exception):
    status_code: int
    default_detail: _APIExceptionInput
    default_code: str

    detail: _Detail
    def __init__(self, detail: _APIExceptionInput = ..., code: str | None = ...) -> None: ...
    def get_codes(self) -> _ErrorCodes: ...
    def get_full_details(self) -> _ErrorFullDetails: ...

class ValidationError(APIException):
    # ValidationError always wraps `detail` in a list.
    detail: list[ErrorDetail] | dict[str, ErrorDetail]

class ParseError(APIException): ...
class AuthenticationFailed(APIException): ...
class NotAuthenticated(APIException): ...
class PermissionDenied(APIException): ...
class NotFound(APIException): ...

class MethodNotAllowed(APIException):
    def __init__(self, method: str, detail: _APIExceptionInput = ..., code: str | None = ...) -> None: ...

class NotAcceptable(APIException):
    available_renderers: Sequence[BaseRenderer] | None
    def __init__(
        self,
        detail: _APIExceptionInput = ...,
        code: str | None = ...,
        available_renderers: Sequence[BaseRenderer] | None = ...,
    ) -> None: ...

class UnsupportedMediaType(APIException):
    def __init__(self, media_type: str, detail: _APIExceptionInput = ..., code: str | None = ...) -> None: ...

class Throttled(APIException):
    extra_detail_singular: str
    extra_detail_plural: str
    def __init__(self, wait: float | None = ..., detail: _APIExceptionInput = ..., code: str | None = ...): ...

def server_error(request: HttpRequest | Request, *args: Any, **kwargs: Any) -> JsonResponse: ...
def bad_request(request: HttpRequest | Request, exception: Exception, *args: Any, **kwargs: Any) -> JsonResponse: ...
