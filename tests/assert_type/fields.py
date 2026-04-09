from collections.abc import Mapping
from typing import Any

from rest_framework import serializers
from rest_framework.fields import FloatField
from typing_extensions import assert_type

# case: field_get_attribute_returns_value_type
field = serializers.CharField()
result = field.get_attribute(object())
assert_type(result, str | None)

# case: field_context_is_mapping
assert_type(field.context, Mapping[str, Any])

# case: float_field_args_fields
FloatField(min_value=1, max_value=1.0)
FloatField(min_value=1.2, max_value=1)
