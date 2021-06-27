from typing import Any, Dict, List, Optional, Protocol, Sequence, Type, TypeVar, Union

from django.db.models import Manager, Model
from django.db.models.query import QuerySet

from rest_framework import mixins, views
from rest_framework.filters import BaseFilterBackend
from rest_framework.pagination import BasePagination
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.serializers import BaseSerializer

_MT_co = TypeVar("_MT_co", bound=Model, covariant=True)

def get_object_or_404(
    queryset: Union[Type[_MT_co], Manager[_MT_co], QuerySet[_MT_co]], *filter_args: Any, **filter_kwargs: Any
) -> _MT_co: ...

class UsesQuerySet(Protocol[_MT_co]):
    def get_queryset(self) -> QuerySet[_MT_co]: ...

# Can't just use BaseFilterBackend because there's also things like django_filters.rest_framework.DjangoFilterBackend that are
# valid options but don't extend it
class BaseFilterProtocol(Protocol):
    def filter_queryset(self, request: Request, queryset: QuerySet[_MT_co], view: views.APIView) -> QuerySet[_MT_co]: ...
    def get_schema_fields(self, view: views.APIView) -> List[Any]: ...
    def get_schema_operation_parameters(self, view: views.APIView): ...

class GenericAPIView(views.APIView, UsesQuerySet[_MT_co]):
    queryset: Optional[Union[QuerySet[_MT_co], Manager[_MT_co]]] = ...
    serializer_class: Optional[Type[BaseSerializer]] = ...
    lookup_field: str = ...
    lookup_url_kwarg: Optional[str] = ...
    filter_backends: Sequence[Type[Union[BaseFilterBackend, BaseFilterProtocol]]] = ...
    pagination_class: Optional[Type[BasePagination]] = ...
    def get_object(self) -> _MT_co: ...
    def get_serializer(self, *args: Any, **kwargs: Any) -> BaseSerializer[_MT_co]: ...
    def get_serializer_class(self) -> Type[BaseSerializer[_MT_co]]: ...
    def get_serializer_context(self) -> Dict[str, Any]: ...
    def filter_queryset(self, queryset: QuerySet[_MT_co]) -> QuerySet[_MT_co]: ...
    @property
    def paginator(self) -> Optional[BasePagination]: ...
    def paginate_queryset(self, queryset: Union[QuerySet[_MT_co], Sequence[Any]]) -> Optional[Sequence[Any]]: ...
    def get_paginated_response(self, data: Any) -> Response: ...

class CreateAPIView(mixins.CreateModelMixin, GenericAPIView):
    def post(self, request: Request, *args: Any, **kwargs: Any) -> Response: ...

class ListAPIView(mixins.ListModelMixin, GenericAPIView):
    def get(self, request: Request, *args: Any, **kwargs: Any) -> Response: ...

class RetrieveAPIView(mixins.RetrieveModelMixin, GenericAPIView):
    def get(self, request: Request, *args: Any, **kwargs: Any) -> Response: ...

class DestroyAPIView(mixins.DestroyModelMixin, GenericAPIView):
    def delete(self, request: Request, *args: Any, **kwargs: Any) -> Response: ...

class UpdateAPIView(mixins.UpdateModelMixin, GenericAPIView):
    def put(self, request: Request, *args: Any, **kwargs: Any) -> Response: ...
    def patch(self, request: Request, *args: Any, **kwargs: Any) -> Response: ...

class ListCreateAPIView(mixins.ListModelMixin, mixins.CreateModelMixin, GenericAPIView):
    def get(self, request: Request, *args: Any, **kwargs: Any) -> Response: ...
    def post(self, request: Request, *args: Any, **kwargs: Any) -> Response: ...

class RetrieveUpdateAPIView(mixins.RetrieveModelMixin, mixins.UpdateModelMixin, GenericAPIView):
    def get(self, request: Request, *args: Any, **kwargs: Any) -> Response: ...
    def put(self, request: Request, *args: Any, **kwargs: Any) -> Response: ...
    def patch(self, request: Request, *args: Any, **kwargs: Any) -> Response: ...

class RetrieveDestroyAPIView(mixins.RetrieveModelMixin, mixins.DestroyModelMixin, GenericAPIView):
    def get(self, request: Request, *args: Any, **kwargs: Any) -> Response: ...
    def delete(self, request: Request, *args: Any, **kwargs: Any) -> Response: ...

class RetrieveUpdateDestroyAPIView(
    mixins.RetrieveModelMixin, mixins.UpdateModelMixin, mixins.DestroyModelMixin, GenericAPIView
):
    def get(self, request: Request, *args: Any, **kwargs: Any) -> Response: ...
    def put(self, request: Request, *args: Any, **kwargs: Any) -> Response: ...
    def patch(self, request: Request, *args: Any, **kwargs: Any) -> Response: ...
    def delete(self, request: Request, *args: Any, **kwargs: Any) -> Response: ...
