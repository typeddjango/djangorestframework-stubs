from django.db.models import Model
from rest_framework.generics import GenericAPIView
from rest_framework.mixins import CreateModelMixin, DestroyModelMixin, UpdateModelMixin
from rest_framework.serializers import BaseSerializer
from typing_extensions import override


class MyModel(Model):
    pass


# Pyright does not use the UsesQuerySet self annotation to specialize these hook overrides.
# Keep the model-specific signatures; mypy resolves them from GenericAPIView[MyModel].
# case: test_create
class CreateView(GenericAPIView[MyModel], CreateModelMixin):
    @override
    def perform_create(self, serializer: BaseSerializer[MyModel]) -> None: ...  # pyright: ignore[reportIncompatibleMethodOverride]


# case: test_perform_update
class UpdateView(GenericAPIView[MyModel], UpdateModelMixin):
    @override
    def perform_update(self, serializer: BaseSerializer[MyModel]) -> None: ...  # pyright: ignore[reportIncompatibleMethodOverride]


# case: test_perform_destroy
class DestroyView(GenericAPIView[MyModel], DestroyModelMixin):
    @override
    def perform_destroy(self, instance: MyModel) -> None: ...  # pyright: ignore[reportIncompatibleMethodOverride]
