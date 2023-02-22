from collections import OrderedDict
from collections.abc import Callable
from typing import Any

from django.http.request import HttpRequest
from django.http.response import HttpResponseBase
from rest_framework import generics, mixins, views
from rest_framework.decorators import ViewSetAction
from rest_framework.generics import _MT_co
from rest_framework.request import Request
from rest_framework.views import AsView, GenericView
from typing_extensions import TypeAlias

def _is_extra_action(attr: Any) -> bool: ...

_ViewFunc: TypeAlias = Callable[..., HttpResponseBase]

class ViewSetMixin:
    # Classvars assigned in as_view()
    name: str | None
    description: str | None
    suffix: str | None
    detail: bool
    basename: str
    # Instance attributes assigned in view wrapper
    action_map: dict[str, str]
    args: tuple[Any, ...]
    kwargs: dict[str, Any]
    # Assigned in initialize_request()
    action: str
    @classmethod
    def as_view(
        cls, actions: dict[str, str | ViewSetAction] | None = ..., **initkwargs: Any
    ) -> AsView[GenericView]: ...
    def initialize_request(self, request: HttpRequest, *args: Any, **kwargs: Any) -> Request: ...
    def reverse_action(self, url_name: str, *args: Any, **kwargs: Any) -> str: ...
    @classmethod
    def get_extra_actions(cls) -> list[_ViewFunc]: ...
    def get_extra_action_url_map(self) -> OrderedDict[str, str]: ...

class ViewSet(ViewSetMixin, views.APIView): ...
class GenericViewSet(ViewSetMixin, generics.GenericAPIView[_MT_co]): ...
class ReadOnlyModelViewSet(mixins.RetrieveModelMixin, mixins.ListModelMixin, GenericViewSet[_MT_co]): ...
class ModelViewSet(
    mixins.CreateModelMixin,
    mixins.RetrieveModelMixin,
    mixins.UpdateModelMixin,
    mixins.DestroyModelMixin,
    mixins.ListModelMixin,
    GenericViewSet[_MT_co],
): ...
