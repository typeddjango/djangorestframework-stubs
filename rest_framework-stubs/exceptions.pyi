from typing import Any, Dict, List, Optional, Sequence, Union

from django.http import HttpRequest, JsonResponse
from rest_framework.renderers import BaseRenderer
from rest_framework.request import Request

def _get_error_details(data: Any, default_code: Optional[str] = ...) -> Any: ...
def _get_codes(detail: Any) -> Any: ...
def _get_full_details(detail: Any) -> Any: ...

class ErrorDetail(str):
    code: Optional[str] = None
    def __new__(cls, string: str, code: Optional[str] = ...): ...

_Detail = Union[str, List[Any], Dict[str, Any]]

class APIException(Exception):
    status_code: int = ...
    default_detail: _Detail = ...
    default_code: str = ...

    detail: _Detail
    def __init__(self, detail: Optional[_Detail] = ..., code: Optional[str] = ...) -> None: ...
    def get_codes(self) -> Any: ...
    def get_full_details(self) -> Any: ...

class ValidationError(APIException): ...
class ParseError(APIException): ...
class AuthenticationFailed(APIException): ...
class NotAuthenticated(APIException): ...
class PermissionDenied(APIException): ...
class NotFound(APIException): ...

class MethodNotAllowed(APIException):
    def __init__(self, method: str, detail: Optional[_Detail] = ..., code: Optional[str] = ...) -> None: ...

class NotAcceptable(APIException):
    available_renderers: Optional[Sequence[BaseRenderer]]
    def __init__(
        self,
        detail: Optional[_Detail] = ...,
        code: Optional[str] = ...,
        available_renderers: Optional[Sequence[BaseRenderer]] = ...,
    ) -> None: ...

class UnsupportedMediaType(APIException):
    def __init__(self, media_type: str, detail: Optional[_Detail] = ..., code: Optional[str] = ...) -> None: ...

class Throttled(APIException):
    extra_detail_singular: str = ...
    extra_detail_plural: str = ...
    def __init__(self, wait: Optional[float] = ..., detail: Optional[_Detail] = ..., code: Optional[str] = ...): ...

def server_error(request: Union[HttpRequest, Request], *args: Any, **kwargs: Any) -> JsonResponse: ...
def bad_request(
    request: Union[HttpRequest, Request], exception: Exception, *args: Any, **kwargs: Any
) -> JsonResponse: ...
