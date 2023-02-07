from collections.abc import Iterator, Sequence
from contextlib import AbstractContextManager, contextmanager
from types import TracebackType
from typing import Any

from django.contrib.auth.base_user import AbstractBaseUser
from django.contrib.auth.models import AnonymousUser
from django.http import HttpRequest
from django.http.request import _ImmutableQueryDict
from rest_framework.authentication import BaseAuthentication
from rest_framework.authtoken.models import Token
from rest_framework.negotiation import BaseContentNegotiation
from rest_framework.parsers import BaseParser
from rest_framework.versioning import BaseVersioning
from rest_framework.views import APIView

def is_form_media_type(media_type: str) -> bool: ...

class override_method(AbstractContextManager[Request]):
    def __init__(self, view: APIView, request: Request, method: str): ...
    def __enter__(self) -> Request: ...
    def __exit__(
        self,
        exc_type: type[BaseException] | None,
        exc_value: BaseException | None,
        traceback: TracebackType | None,
    ) -> bool | None: ...

class WrappedAttributeError(Exception): ...

@contextmanager
def wrap_attributeerrors() -> Iterator[None]: ...

class Empty: ...

def clone_request(request: Request, method: str) -> Request: ...

class ForcedAuthentication:
    force_user: AnonymousUser | AbstractBaseUser | None
    force_token: str | None
    def __init__(self, force_user: AnonymousUser | AbstractBaseUser | None, force_token: str | None) -> None: ...
    def authenticate(self, request: Request) -> tuple[AnonymousUser | AbstractBaseUser | None, Any | None]: ...

class Request(HttpRequest):
    parsers: Sequence[BaseParser] | None
    authenticators: Sequence[BaseAuthentication | ForcedAuthentication] | None
    negotiator: BaseContentNegotiation | None
    parser_context: dict[str, Any] | None
    version: str | None
    versioning_scheme: BaseVersioning | None
    _request: HttpRequest
    def __init__(
        self,
        request: HttpRequest,
        parsers: Sequence[BaseParser] | None = ...,
        authenticators: Sequence[BaseAuthentication] | None = ...,
        negotiator: BaseContentNegotiation | None = ...,
        parser_context: dict[str, Any] | None = ...,
    ) -> None: ...
    @property
    def content_type(self) -> str: ...  # type: ignore[override]
    @property
    def stream(self) -> Any: ...
    @property
    def query_params(self) -> _ImmutableQueryDict: ...
    @property
    def data(self) -> dict[str, Any]: ...
    @property  # type: ignore[override]
    def user(self) -> AbstractBaseUser | AnonymousUser: ...  # type: ignore[override]
    @user.setter
    def user(self, value: AbstractBaseUser | AnonymousUser) -> None: ...
    @property
    def auth(self) -> Token | Any: ...
    @auth.setter
    def auth(self, value: Token | Any) -> None: ...
    @property
    def successful_authenticator(self) -> BaseAuthentication | ForcedAuthentication | None: ...
    def __getattr__(self, attr: str) -> Any: ...
    @property
    def DATA(self) -> None: ...
    @property
    def POST(self) -> _ImmutableQueryDict: ...  # type: ignore[override]
    @property
    def FILES(self): ...
    @property
    def QUERY_PARAMS(self) -> None: ...
    def force_plaintext_errors(self, value: Any) -> None: ...
