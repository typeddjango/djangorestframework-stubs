from collections.abc import Callable, Mapping
from http import HTTPMethod
from typing import Any, Generic, TypeVar, assert_type

from django.db.models import Model
from django.http import HttpRequest
from mypy_extensions import Arg
from rest_framework import viewsets
from rest_framework.decorators import MethodMapper, action, api_view, permission_classes
from rest_framework.permissions import BasePermission, IsAuthenticated
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import AsView
from typing_extensions import override


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
MY_VAR: HTTPMethod = HTTPMethod.POST


class MyView2(viewsets.ViewSet):
    @action(methods=[HTTPMethod.GET], detail=False)
    def view_func_1(self, request: Request) -> Response: ...
    @action(methods=[MY_VAR], detail=False)
    def view_func_2(self, request: Request) -> Response: ...


# case: action_called_on_instance_is_bound
class ActionViewSet(viewsets.ViewSet):
    @action(detail=False)
    def list_action(self, request: Request) -> Response: ...
    @action(detail=True, methods=["post"])
    def detail_action(self, request: Request, pk: int | None = None) -> Response: ...
    @action(detail=False, methods=["get"])
    def mapped(self, request: Request) -> Response: ...
    @mapped.mapping.post
    def mapped_post(self, request: Request) -> Response: ...
    def call_from_method(self, request: Request) -> None:
        assert_type(self.list_action(request), Response)
        assert_type(self.detail_action(request, pk=1), Response)
        assert_type(self.mapped_post(request), Response)


action_view = ActionViewSet()
action_request: Request
assert_type(action_view.list_action(action_request), Response)
assert_type(action_view.detail_action(action_request), Response)
assert_type(action_view.detail_action(action_request, pk=1), Response)
assert_type(action_view.mapped_post(action_request), Response)


# case: action_called_on_class_takes_self
assert_type(ActionViewSet.list_action(action_view, action_request), Response)
assert_type(ActionViewSet.detail_action(action_view, action_request, pk=1), Response)


# case: action_attributes
assert_type(ActionViewSet.list_action.detail, bool)
assert_type(ActionViewSet.list_action.url_path, str)
assert_type(ActionViewSet.list_action.url_name, str)
assert_type(ActionViewSet.list_action.kwargs, Mapping[str, Any])
assert_type(ActionViewSet.list_action.mapping, MethodMapper)
assert_type(ActionViewSet.list_action.__name__, str)
assert_type(action_view.detail_action.detail, bool)
assert_type(action_view.detail_action.url_path, str)
assert_type(action_view.detail_action.url_name, str)
assert_type(action_view.detail_action.kwargs, Mapping[str, Any])
assert_type(action_view.detail_action.mapping, MethodMapper)
assert_type(action_view.detail_action.__name__, str)
ActionViewSet.as_view(actions={"get": ActionViewSet.list_action})


# case: action_overridden_in_subclass
class ActionViewSetChild(ActionViewSet):
    @override
    @action(detail=False)
    def list_action(self, request: Request) -> Response:
        return super().list_action(request)


# case: action_overridden_in_subclass_of_generic_viewset
_ActionModel = TypeVar("_ActionModel", bound=Model)


class GenericActionViewSet(viewsets.GenericViewSet[_ActionModel], Generic[_ActionModel]):
    @action(detail=False)
    def some_action(self, request: Request) -> Response: ...


class ConcreteActionViewSet(GenericActionViewSet[Model]):
    @override
    @action(detail=False)
    def some_action(self, request: Request) -> Response:
        return super().some_action(request)


assert_type(ConcreteActionViewSet().some_action(action_request), Response)
