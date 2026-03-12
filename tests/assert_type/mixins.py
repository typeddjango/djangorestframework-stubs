from django.db.models import Model
from rest_framework.generics import GenericAPIView
from rest_framework.mixins import CreateModelMixin, DestroyModelMixin, UpdateModelMixin
from rest_framework.serializers import BaseSerializer
from typing_extensions import override


class MyModel(Model):
    pass


# case: test_create
class CreateView(GenericAPIView, CreateModelMixin):
    @override
    def perform_create(self, serializer: BaseSerializer[MyModel]) -> None: ...


# case: test_perform_update
class UpdateView(GenericAPIView, UpdateModelMixin):
    @override
    def perform_update(self, serializer: BaseSerializer[MyModel]) -> None: ...


# case: test_perform_destroy
class DestroyView(GenericAPIView, DestroyModelMixin):
    @override
    def perform_destroy(self, instance: MyModel) -> None: ...
