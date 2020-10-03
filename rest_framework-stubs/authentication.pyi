from typing import Any, Optional, Tuple, Type

from django.contrib.auth import authenticate as authenticate
from django.db.models import Model
from django.middleware.csrf import CsrfViewMiddleware
from rest_framework.request import Request

def get_authorization_header(request: Request) -> bytes: ...

class CSRFCheck(CsrfViewMiddleware): ...

class BaseAuthentication:
    def authenticate(self, request: Request) -> Optional[Tuple[Any, Any]]: ...
    def authenticate_header(self, request: Request) -> Optional[str]: ...

class BasicAuthentication(BaseAuthentication):
    www_authenticate_realm: str = ...
    def authenticate_credentials(
        self, userid: str, password: str, request: Optional[Request] = ...
    ) -> Tuple[Any, None]: ...

class SessionAuthentication(BaseAuthentication):
    def enforce_csrf(self, request: Request) -> None: ...

class TokenAuthentication(BaseAuthentication):
    keyword: str = ...
    model: Optional[Type[Model]] = ...
    def get_model(self) -> Type[Model]: ...
    def authenticate_credentials(self, key: str) -> Tuple[Any, Any]: ...

class RemoteUserAuthentication(BaseAuthentication):
    header: str = ...
