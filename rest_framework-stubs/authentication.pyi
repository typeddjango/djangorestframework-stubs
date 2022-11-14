from typing import Any

from django.contrib.auth import authenticate as authenticate
from django.db.models import Model
from django.middleware.csrf import CsrfViewMiddleware
from rest_framework.request import Request

def get_authorization_header(request: Request) -> bytes: ...

class CSRFCheck(CsrfViewMiddleware): ...

class BaseAuthentication:
    def authenticate(self, request: Request) -> tuple[Any, Any] | None: ...  # noqa: F811
    def authenticate_header(self, request: Request) -> str | None: ...

class BasicAuthentication(BaseAuthentication):
    www_authenticate_realm: str
    def authenticate_credentials(
        self, userid: str, password: str, request: Request | None = ...
    ) -> tuple[Any, None]: ...

class SessionAuthentication(BaseAuthentication):
    def enforce_csrf(self, request: Request) -> None: ...

class TokenAuthentication(BaseAuthentication):
    keyword: str
    model: type[Model] | None
    def get_model(self) -> type[Model]: ...
    def authenticate_credentials(self, key: str) -> tuple[Any, Any]: ...

class RemoteUserAuthentication(BaseAuthentication):
    header: str
