from typing import Any, assert_type

from django.db.models import Model, QuerySet
from django.http.request import HttpRequest
from rest_framework import generics, viewsets
from rest_framework.permissions import BasePermission
from rest_framework.request import Request
from rest_framework.views import APIView
from rest_framework.viewsets import GenericViewSet
from typing_extensions import override


class MyModel(Model):
    pass


# case: test_view_request_type
class MyListView(generics.ListAPIView[MyModel]):
    @override
    def filter_queryset(self, queryset: QuerySet[Any]) -> QuerySet[Any]:
        assert_type(self.request, Request)
        return queryset


# case: test_build_api_request
def check_api_request(view: APIView, request: HttpRequest) -> None:
    api_request = view.initialize_request(request)
    assert_type(api_request, Request)


# case: test_generics_of_extended_generic_view
class MyRetrieveView(generics.RetrieveAPIView[MyModel]):
    pass


assert_type(MyRetrieveView().get_object(), MyModel)


# case: test_generics_of_extended_generic_view_set
class MyRetrieveViewSet(viewsets.GenericViewSet[MyModel]):
    pass


assert_type(MyRetrieveViewSet().get_object(), MyModel)


# case: test_override_get_permissions
class MyView(GenericViewSet[MyModel]):
    @override
    def get_permissions(self) -> list[BasePermission]: ...


# case: test_filter_queryset_preserves_row_type
def check_queryset_rows(
    my_view: generics.GenericAPIView[MyModel],
    values_qs: QuerySet[MyModel, dict[str, Any]],
    sequence_data: list[dict[str, Any]],
) -> None:
    filtered = my_view.filter_queryset(values_qs)
    assert_type(filtered, QuerySet[MyModel, dict[str, Any]])

    # case: test_paginate_queryset_extracts_row_type
    page = my_view.paginate_queryset(values_qs)
    assert_type(page, list[dict[str, Any]] | None)

    # case: test_paginate_queryset_accepts_sequence
    sequence_page = my_view.paginate_queryset(sequence_data)
    assert_type(sequence_page, list[dict[str, Any]] | None)
