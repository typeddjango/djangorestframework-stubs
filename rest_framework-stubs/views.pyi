from typing import Any, Callable, Dict, List, Mapping, NoReturn, Optional, Sequence, Tuple, Type, Union, Protocol, TypeVar

from django.http import HttpRequest
from django.http.response import HttpResponseBase
from django.views.generic import View
from rest_framework.authentication import BaseAuthentication
from rest_framework.metadata import BaseMetadata
from rest_framework.negotiation import BaseContentNegotiation
from rest_framework.parsers import BaseParser
from rest_framework.permissions import _PermissionClass, _SupportsHasPermission
from rest_framework.renderers import BaseRenderer
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.schemas.inspectors import ViewInspector
from rest_framework.settings import APISettings
from rest_framework.throttling import BaseThrottle
from rest_framework.versioning import BaseVersioning

def get_view_name(view: APIView) -> str: ...
def get_view_description(view: APIView, html: bool = ...) -> str: ...
def set_rollback() -> None: ...
def exception_handler(exc: Exception, context) -> Optional[Response]: ...

_View = TypeVar("_View", bound=Callable[..., HttpResponseBase])

class AsView(Protocol[_View]):
    self: APIView
    view_class: Type[APIView]
    view_initkwargs: Mapping[str, Any]
    __call__: _View

# Call signature for view function that's returned by as_view()
class GenericView(Protocol):
    def __call__(self, request: HttpRequest, *args: Any, **kwargs: Any) -> Response: ...

class APIView(View):
    args: Any = ...
    authentication_classes: Sequence[Type[BaseAuthentication]] = ...
    content_negotiation_class: Optional[str] = ...
    format_kwarg: Any = ...
    headers: Dict[str, str] = ...
    kwargs: Any = ...
    metadata_class: Optional[Union[str, BaseMetadata]] = ...
    parser_classes: Sequence[Type[BaseParser]] = ...
    permission_classes: Sequence[_PermissionClass] = ...
    renderer_classes: Sequence[Type[BaseRenderer]] = ...
    request: Request
    response: Response = ...
    schema: Optional[ViewInspector] = ...
    settings: APISettings
    throttle_classes: Sequence[Type[BaseThrottle]] = ...
    versioning_class: Optional[str] = ...
    @property
    def allowed_methods(self) -> List[str]: ...
    @property
    def default_response_headers(self) -> Dict[str, str]: ...
    @classmethod
    def as_view(cls, **initkwargs: Any) -> AsView[GenericView]: ...
    def http_method_not_allowed(self, request: Request, *args: Any, **kwargs: Any) -> Response: ...  # type: ignore[override]
    def permission_denied(self, request: Request, message: Optional[str] = ...) -> NoReturn: ...
    def throttled(self, request: Request, wait: float) -> NoReturn: ...
    def get_authenticate_header(self, request: Request) -> str: ...
    def get_parser_context(self, http_request: HttpRequest) -> Dict[str, Any]: ...
    def get_renderer_context(self) -> Dict[str, Any]: ...
    def get_exception_handler_context(self) -> Dict[str, Any]: ...
    def get_view_name(self) -> str: ...
    def get_view_description(self, html: bool = ...) -> str: ...
    def get_format_suffix(self, **kwargs: Any) -> Optional[str]: ...
    def get_renderers(self) -> List[BaseRenderer]: ...
    def get_parsers(self) -> List[BaseParser]: ...
    def get_authenticators(self) -> List[BaseAuthentication]: ...
    def get_permissions(self) -> List[_SupportsHasPermission]: ...
    def get_throttles(self) -> List[BaseThrottle]: ...
    def get_content_negotiator(self) -> BaseContentNegotiation: ...
    def get_exception_handler(self) -> Callable: ...
    def perform_content_negotiation(self, request: Request, force: bool = ...) -> Tuple[BaseRenderer, str]: ...
    def perform_authentication(self, request: Request) -> None: ...
    def check_permissions(self, request: Request) -> None: ...
    def check_object_permissions(self, request: Request, obj: Any) -> None: ...
    def check_throttles(self, request: Request) -> None: ...
    def determine_version(
        self, request: Request, *args: Any, **kwargs: Any
    ) -> Tuple[Optional[str], Optional[BaseVersioning]]: ...
    def initialize_request(self, request: HttpRequest, *args: Any, **kwargs: Any) -> Request: ...
    def initial(self, request: Request, *args: Any, **kwargs: Any) -> None: ...
    def finalize_response(self, request: Request, response: Response, *args: Any, **kwargs: Any) -> Response: ...
    def handle_exception(self, exc: Exception) -> Response: ...
    def raise_uncaught_exception(self, exc: Exception) -> NoReturn: ...
    def dispatch(self, request: HttpRequest, *args: Any, **kwargs: Any) -> HttpResponseBase:
    def options(self, request: Request, *args: Any, **kwargs: Any): ...  # type: ignore[override]
