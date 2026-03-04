from typing import Any

from django.contrib.auth.models import User
from django.db.models import QuerySet
from rest_framework.validators import UniqueValidator, qs_filter
from typing_extensions import assert_type

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
