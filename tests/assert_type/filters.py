from typing import Any

from django.db.models import Model, QuerySet
from rest_framework.filters import BaseFilterBackend, OrderingFilter
from rest_framework.generics import GenericAPIView
from rest_framework.request import Request
from rest_framework.views import APIView
from typing_extensions import assert_type


# case: basic_filters
class MyView1(GenericAPIView):
    filter_backends = [OrderingFilter]


# case: django_filters
class MyModel(Model):
    pass


class MyFilterBackend:
    def filter_queryset(self, request: Request, queryset: QuerySet[MyModel], view: APIView) -> QuerySet[MyModel]:
        pass

    def get_schema_fields(self, view: APIView) -> list[Any]:
        pass

    def get_schema_operation_parameters(self, view: APIView) -> Any:
        pass


class MyView(GenericAPIView):
    filter_backends = [MyFilterBackend]


# case: base_filter_backend_preserves_queryset_type
backend = BaseFilterBackend()
request: Request
view: APIView
values_qs: QuerySet[MyModel, dict[str, Any]]
result = backend.filter_queryset(request, values_qs, view)
assert_type(result, QuerySet[MyModel, dict[str, Any]])
