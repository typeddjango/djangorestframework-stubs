from collections import OrderedDict
from typing import Any, Callable, Dict, List, Optional, Tuple

from django.http.response import HttpResponseBase

from rest_framework.request import Request

from rest_framework import generics, mixins, views

def _is_extra_action(attr: Any) -> bool: ...

_ViewFunc = Callable[..., HttpResponseBase]

class ViewSetMixin(object):
    # Classvars assigned in as_view()
    name: Optional[str]
    description: Optional[str]
    suffix: Optional[str]
    detail: bool
    basename: str
    # Instance attributes assigned in view wrapper
    action_map: Dict[str, str]
    args: Tuple[Any, ...]
    kwargs: Dict[str, Any]
    # Assigned in initialize_request()
    action: str
    @classmethod
    def as_view(cls, actions: Optional[Dict[str, str]] = ..., **initkwargs: Any) -> Callable: ...
    def initialize_request(self, request: Request, *args: Any, **kwargs: Any) -> Request: ...
    def reverse_action(self, url_name: str, *args: Any, **kwargs: Any) -> str: ...
    @classmethod
    def get_extra_actions(cls) -> List[_ViewFunc]: ...
    def get_extra_action_url_map(self) -> OrderedDict[str, str]: ...

class ViewSet(ViewSetMixin, views.APIView): ...
class GenericViewSet(ViewSetMixin, generics.GenericAPIView): ...
class ReadOnlyModelViewSet(mixins.RetrieveModelMixin, mixins.ListModelMixin, GenericViewSet): ...
class ModelViewSet(
    mixins.CreateModelMixin,
    mixins.RetrieveModelMixin,
    mixins.UpdateModelMixin,
    mixins.DestroyModelMixin,
    mixins.ListModelMixin,
    GenericViewSet,
): ...
