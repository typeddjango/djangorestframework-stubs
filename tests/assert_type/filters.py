from typing import Any, assert_type

from django.db.models import Model, QuerySet
from rest_framework.filters import BaseFilterBackend, OrderingFilter
from rest_framework.generics import GenericAPIView
from rest_framework.request import Request
from rest_framework.views import APIView


# case: basic_filters
class MyView1(GenericAPIView[Any]):
    filter_backends = [OrderingFilter]


# case: django_filters
class MyModel(Model):
    pass


class MyFilterBackend:
    def filter_queryset(self, request: Request, queryset: QuerySet[MyModel], view: APIView) -> QuerySet[MyModel]:
        return queryset

    def get_schema_fields(self, view: APIView) -> list[Any]:
        return []

    def get_schema_operation_parameters(self, view: APIView) -> Any:
        pass


class MyView(GenericAPIView[MyModel]):
    filter_backends = [MyFilterBackend]


# case: base_filter_backend_preserves_queryset_type
def check_filter_queryset(
    backend: BaseFilterBackend, request: Request, view: APIView, values_qs: QuerySet[MyModel, dict[str, Any]]
) -> None:
    result = backend.filter_queryset(request, values_qs, view)
    assert_type(result, QuerySet[MyModel, dict[str, Any]])
