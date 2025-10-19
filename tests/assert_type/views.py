from typing import Any

from django.db.models import Model, QuerySet
from django.http.request import HttpRequest
from rest_framework import generics, viewsets
from rest_framework.permissions import BasePermission
from rest_framework.request import Request
from rest_framework.views import APIView
from rest_framework.viewsets import GenericViewSet
from typing_extensions import assert_type


class MyModel(Model):
    pass


# case: test_view_request_type
class MyListView(generics.ListAPIView):
    def filter_queryset(self, queryset: QuerySet[Any]) -> QuerySet[Any]:
        assert_type(self.request, Request)
        return queryset


# case: test_build_api_request
request: HttpRequest
view: APIView
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
class MyView(GenericViewSet):
    def get_permissions(self) -> list[BasePermission]: ...
