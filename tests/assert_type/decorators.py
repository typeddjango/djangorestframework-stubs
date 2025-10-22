# case: api_view
import sys
from collections.abc import Callable
from typing import Any

from django.http import HttpRequest
from mypy_extensions import Arg
from rest_framework import viewsets
from rest_framework.decorators import action, api_view, permission_classes
from rest_framework.permissions import BasePermission, IsAuthenticated
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import AsView
from typing_extensions import assert_type


# case: api_view
@api_view()
def view_func1(request: Any) -> Any: ...


view_func1(HttpRequest())
assert_type(view_func1, AsView[Callable[[HttpRequest], Any]])
assert_type(view_func1(HttpRequest()), Any)


# case: api_view_fancy
@api_view(["GET", "POST"])
def view_func2(request: Request, arg: str) -> Response: ...


view_func2(HttpRequest(), "test")
view_func2(HttpRequest(), arg="test")
assert_type(view_func2, AsView[Callable[[HttpRequest, Arg(str, "arg")], Response]])
assert_type(view_func2(HttpRequest(), "test"), Response)


# case: permission_classes_with_operators
class Permission(BasePermission):
    pass


permission_classes([IsAuthenticated & Permission])
permission_classes([IsAuthenticated | Permission])
permission_classes([~Permission])


# case: method_decorator
class MyView(viewsets.ViewSet):
    @action(methods=("get",), detail=False)
    def view_func_1(self, request: Request) -> Response: ...
    @action(methods=["post"], detail=False)
    def view_func_2(self, request: Request) -> Response: ...
    @action(methods=("GET",), detail=False)
    def view_func_3(self, request: Request) -> Response: ...


# case: method_decorator_http_libary
if sys.version_info >= (3, 11):
    from http import HTTPMethod

    from rest_framework import viewsets
    from rest_framework.decorators import action
    from rest_framework.request import Request
    from rest_framework.response import Response

    MY_VAR: HTTPMethod = HTTPMethod.POST

    class MyView2(viewsets.ViewSet):
        @action(methods=[HTTPMethod.GET], detail=False)
        def view_func_1(self, request: Request) -> Response: ...
        @action(methods=[MY_VAR], detail=False)
        def view_func_2(self, request: Request) -> Response: ...
