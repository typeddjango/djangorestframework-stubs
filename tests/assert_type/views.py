from typing import Any, TypeVar, assert_type

from django.db.models import Model, QuerySet
from django.http.request import HttpRequest
from rest_framework import generics, viewsets
from rest_framework.fields import CharField
from rest_framework.permissions import BasePermission
from rest_framework.request import Request
from rest_framework.serializers import BaseSerializer, ListSerializer, Serializer
from rest_framework.views import APIView
from rest_framework.viewsets import GenericViewSet
from typing_extensions import override


class MyModel(Model):
    pass


# case: test_view_request_type
class MyListView(generics.ListAPIView):
    @override
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
    @override
    def get_permissions(self) -> list[BasePermission]: ...


# case: test_filter_queryset_preserves_row_type
my_view: generics.GenericAPIView[MyModel]
values_qs: QuerySet[MyModel, dict[str, Any]]
filtered = my_view.filter_queryset(values_qs)
assert_type(filtered, QuerySet[MyModel, dict[str, Any]])

# case: test_paginate_queryset_extracts_row_type
page = my_view.paginate_queryset(values_qs)
assert_type(page, list[dict[str, Any]] | None)

# case: test_paginate_queryset_accepts_sequence
sequence_data: list[dict[str, Any]] = [{"key": "value"}]
sequence_page = my_view.paginate_queryset(sequence_data)
assert_type(sequence_page, list[dict[str, Any]] | None)


# case: test_generic_api_view_default_preserves_model_covariance
class ChildModel(MyModel):
    pass


def accept_parent_view(view: generics.GenericAPIView[MyModel]) -> None: ...
def accept_parent_list(view: generics.ListAPIView[MyModel]) -> None: ...
def accept_parent_viewset(view: viewsets.ModelViewSet[MyModel]) -> None: ...


def accept_parent_with_fixed_serializer(
    view: generics.GenericAPIView[MyModel, BaseSerializer[Model]],
) -> None: ...


def check_model_covariance(
    view: generics.GenericAPIView[ChildModel],
    list_view: generics.ListAPIView[ChildModel],
    viewset: viewsets.ModelViewSet[ChildModel],
    fixed_serializer_view: generics.GenericAPIView[ChildModel, BaseSerializer[Model]],
) -> None:
    # Making only _S covariant would not fix these failures: BaseSerializer[ChildModel]
    # is not a subtype of BaseSerializer[MyModel] (BaseSerializer is invariant).
    # Covariant _S would help when one chosen serializer subclasses another, but allowing
    # callers to replace serializer_class makes that unsafe.
    # Regression: a child-model view used to work where a parent-model view was expected.
    accept_parent_view(view)
    # Regression: the same valid model widening now fails for built-in list views.
    accept_parent_list(list_view)
    # Regression: the same valid model widening now fails for model viewsets.
    accept_parent_viewset(viewset)

    # OK on the PR: model widening works when both views name the exact same serializer type.
    accept_parent_with_fixed_serializer(fixed_serializer_view)


# case: test_custom_generic_view_preserves_model_covariance
_ModelT_co = TypeVar("_ModelT_co", bound=Model, covariant=True)


class ForwardingView(generics.GenericAPIView[_ModelT_co]):
    pass


def accept_parent_forwarding_view(view: ForwardingView[MyModel]) -> None: ...


def check_forwarded_model_covariance(view: ForwardingView[ChildModel]) -> None:
    # OK on the PR: a custom generic view still accepts a child model in place of its parent.
    accept_parent_forwarding_view(view)


# case: test_generic_api_view_many_returns_list_serializer
# New-API checks below: master does not support the second type argument used here.
class ItemSerializer(Serializer[Any]):
    name = CharField()

    def to_dto(self) -> dict[str, str]:
        return {"name": self.data["name"]}


class ItemView(generics.GenericAPIView[Any, ItemSerializer]):
    serializer_class = ItemSerializer


# OK on the PR: without many=True, get_serializer() returns the chosen serializer.
single = ItemView().get_serializer()
assert_type(single, ItemSerializer)
assert_type(single.to_dto(), dict[str, str])

# OK on the PR: explicitly passing many=False also returns the chosen serializer.
single_explicit = ItemView().get_serializer(many=False)
assert_type(single_explicit, ItemSerializer)

# New-API problem, not a master regression: many=True returns a list serializer at runtime,
# but the PR claims it returns ItemSerializer. Making _S covariant would not fix this.
many = ItemView().get_serializer(many=True)
assert_type(many, ListSerializer[Any])


# case: test_generic_api_view_dynamic_many_returns_either_serializer
def check_dynamic_many(flag: bool) -> None:
    # New-API problem, not a master regression: an unknown flag can return either type,
    # but the PR claims it always returns ItemSerializer.
    serializer = ItemView().get_serializer(many=flag)
    assert_type(serializer, ItemSerializer | ListSerializer[Any])
