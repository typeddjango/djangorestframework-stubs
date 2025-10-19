from typing import Any

from django.db.models import Model, QuerySet
from rest_framework.filters import OrderingFilter
from rest_framework.generics import GenericAPIView
from rest_framework.request import Request
from rest_framework.views import APIView


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
