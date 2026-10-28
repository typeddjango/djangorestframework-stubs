from typing import Any, assert_type

from django.contrib.auth.models import User
from django.db.models import QuerySet
from rest_framework import serializers
from rest_framework.validators import (
    SerializerValidator,
    UniqueForDateValidator,
    UniqueTogetherValidator,
    UniqueValidator,
    qs_filter,
)

# case: qs_filter_preserves_queryset_type
values_qs: QuerySet[User, dict[str, Any]]
result = qs_filter(values_qs, pk=1)
assert_type(result, QuerySet[User, dict[str, Any]])


# case: unique_validator_filter_queryset_preserves_queryset_type
validator: UniqueValidator
result2 = validator.filter_queryset("value", values_qs, "name")
assert_type(result2, QuerySet[User, dict[str, Any]])


# case: unique_validator_exclude_current_instance_preserves_queryset_type
instance: User
result3 = validator.exclude_current_instance(values_qs, instance)
assert_type(result3, QuerySet[User, dict[str, Any]])


# case: serializer_level_validators_are_accepted_by_serializers
together = UniqueTogetherValidator(queryset=User.objects.all(), fields=["username", "email"])
for_date = UniqueForDateValidator(queryset=User.objects.all(), field="username", date_field="date_joined")


class UserSerializer(serializers.ModelSerializer[User]):
    class Meta:
        model = User
        fields = ["username", "email"]


user_serializer = UserSerializer(validators=[together, for_date])
user_serializer.validators = [*user_serializer.get_unique_together_validators(), for_date]
serializer_validators: list[SerializerValidator[Any]] = [together, for_date]


# case: serializer_validators_narrow_to_unique_together_validator
narrowed = [v for v in user_serializer.validators if isinstance(v, UniqueTogetherValidator)]
assert_type(narrowed, list[UniqueTogetherValidator])


# case: list_serializer_validators_receive_the_list
def at_most_two(value: list[Any]) -> None: ...


user_list = serializers.ListSerializer[User](child=UserSerializer(), validators=[at_most_two])
assert_type(user_list.validators, list[SerializerValidator[list[Any]]])
assert_type(user_list.get_validators(), list[SerializerValidator[list[Any]]])
user_list.validators = [at_most_two]
