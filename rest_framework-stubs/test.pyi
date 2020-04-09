from typing import Any, Optional, Sequence, Tuple, Union, Dict

from django.db.models import Model
from django.http import HttpRequest, HttpResponse
from django.test import testcases
from django.test.client import Client as DjangoClient, ClientHandler, RequestFactory as DjangoRequestFactory
from rest_framework.compat import requests
from rest_framework.response import Response

def force_authenticate(request: HttpRequest, user: Optional[Model] = ..., token: Optional[Any] = ...) -> None: ...

class RequestsClient(requests.Session): ...

class APIRequestFactory(DjangoRequestFactory):
    renderer_classes_list: Sequence[str] = ...
    default_format: str = ...
    def __init__(self, enforce_csrf_checks: bool = ..., **defaults: Any) -> None: ...
    def _encode_data(
        self, data: Optional[Any], format: Optional[str] = ..., content_type: Optional[str] = ...
    ) -> Tuple[bytes, str]: ...

class ForceAuthClientHandler(ClientHandler):
    def __init__(self, *args: Any, **kwargs: Any): ...
    def get_response(self, request: HttpRequest) -> HttpResponse: ...

class APIClient(DjangoClient):
    def credentials(self, **kwargs: Any): ...
    def force_authenticate(self, user: Optional[Model] = ..., token: Optional[Any] = ...) -> None: ...
    def request(self, **request: Any) -> Response: ...  # type: ignore[override]
    def get(  # type: ignore[override]
        self, path: str, data: Any = ..., secure: bool = ..., **extra: Any
    ) -> Response: ...
    def post(  # type: ignore[override]
        self, path: str, data: Any = ..., content_type: str = ..., secure: bool = ..., **extra: Any
    ) -> Response: ...
    def head(  # type: ignore[override]
        self, path: str, data: Any = ..., secure: bool = ..., **extra: Any
    ) -> Response: ...
    def trace(  # type: ignore[override]
        self, path: str, secure: bool = ..., **extra: Any
    ) -> Response: ...
    def options(  # type: ignore[override]
        self,
        path: str,
        data: Union[Dict[str, str], str] = ...,
        content_type: str = ...,
        secure: bool = ...,
        **extra: Any
    ) -> Response: ...
    def put(  # type: ignore[override]
        self, path: str, data: Any = ..., content_type: str = ..., secure: bool = ..., **extra: Any
    ) -> Response: ...
    def patch(  # type: ignore[override]
        self, path: str, data: Any = ..., content_type: str = ..., secure: bool = ..., **extra: Any
    ) -> Response: ...
    def delete(  # type: ignore[override]
        self, path: str, data: Any = ..., content_type: str = ..., secure: bool = ..., **extra: Any
    ) -> Response: ...
    def generic(  # type: ignore[override]
        self,
        method: str,
        path: str,
        data: Any = ...,
        content_type: Optional[str] = ...,
        secure: bool = ...,
        **extra: Any
    ) -> Response: ...

class APITransactionTestCase(testcases.TransactionTestCase):
    client: APIClient

class APITestCase(testcases.TestCase):
    client: APIClient

class APISimpleTestCase(testcases.SimpleTestCase):
    client: APIClient

class APILiveServerTestCase(testcases.LiveServerTestCase):
    client: APIClient

class URLPatternsTestCase(testcases.SimpleTestCase): ...
