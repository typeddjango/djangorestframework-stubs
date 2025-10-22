from django.db.models import Model
from rest_framework.generics import GenericAPIView
from rest_framework.mixins import CreateModelMixin, DestroyModelMixin, UpdateModelMixin
from rest_framework.serializers import BaseSerializer


class MyModel(Model):
    pass


# case: test_create
class CreateView(GenericAPIView, CreateModelMixin):
    def perform_create(self, serializer: BaseSerializer[MyModel]) -> None: ...


# case: test_perform_update
class UpdateView(GenericAPIView, UpdateModelMixin):
    def perform_update(self, serializer: BaseSerializer[MyModel]) -> None: ...


# case: test_perform_destroy
class DestroyView(GenericAPIView, DestroyModelMixin):
    def perform_destroy(self, instance: MyModel) -> None: ...
