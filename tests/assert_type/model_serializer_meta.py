# pyright: reportIncompatibleVariableOverride=true

from typing import assert_type

from django.contrib.auth.models import User
from rest_framework.serializers import ModelSerializer


# case: concrete_serializer_meta_retains_its_inferred_types
class UserSerializer(ModelSerializer[User]):
    # This must not produce a pyright incompatible-variable-override error.
    class Meta:
        model = User
        fields = ("id", "username")

    def model_class(self) -> type[User]:
        return self.Meta.model


assert_type(UserSerializer.Meta.model, type[User])
