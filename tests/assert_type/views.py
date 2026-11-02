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
    # These one-argument forms allowed model widening before the serializer parameter.
    # Making only _S covariant would not help: its defaults are BaseSerializer[ChildModel]
    # and BaseSerializer[MyModel], and BaseSerializer itself is invariant.
    # Covariant _S would help when one explicitly selected serializer subclasses another,
    # but that is not automatically safe because serializer_class is writable.
    accept_parent_view(view)
    accept_parent_list(list_view)
    accept_parent_viewset(viewset)

    # Model covariance still works when both views use exactly the same serializer type.
    accept_parent_with_fixed_serializer(fixed_serializer_view)


# case: test_custom_generic_view_preserves_model_covariance
_ModelT_co = TypeVar("_ModelT_co", bound=Model, covariant=True)


class ForwardingView(generics.GenericAPIView[_ModelT_co]):
    pass


def accept_parent_forwarding_view(view: ForwardingView[MyModel]) -> None: ...


def check_forwarded_model_covariance(view: ForwardingView[ChildModel]) -> None:
    # This remains a passing boundary case even though the built-in views above regress.
    accept_parent_forwarding_view(view)


# case: test_generic_api_view_many_returns_list_serializer
# These exercise the new two-argument API, not compatibility with the pre-PR signatures.
class ItemSerializer(Serializer[Any]):
    name = CharField()

    def to_dto(self) -> dict[str, str]:
        return {"name": self.data["name"]}


class ItemView(generics.GenericAPIView[Any, ItemSerializer]):
    serializer_class = ItemSerializer


single = ItemView().get_serializer()
assert_type(single, ItemSerializer)
assert_type(single.to_dto(), dict[str, str])

single_explicit = ItemView().get_serializer(many=False)
assert_type(single_explicit, ItemSerializer)

# Covariance cannot fix a return type that depends on the many argument.
many = ItemView().get_serializer(many=True)
assert_type(many, ListSerializer[Any])


# case: test_generic_api_view_dynamic_many_returns_either_serializer
def check_dynamic_many(flag: bool) -> None:
    serializer = ItemView().get_serializer(many=flag)
    assert_type(serializer, ItemSerializer | ListSerializer[Any])
