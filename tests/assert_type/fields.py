from collections.abc import Mapping
from typing import Any, assert_type

from rest_framework import serializers
from rest_framework.fields import FloatField

# case: field_get_attribute_returns_value_type
field = serializers.CharField()
result = field.get_attribute(object())
assert_type(result, str | None)

# case: field_context_is_mapping
assert_type(field.context, Mapping[str, Any])

# case: float_field_args_fields
FloatField(min_value=1, max_value=1.0)
FloatField(min_value=1.2, max_value=1)

# case: json_field_default_and_initial
assert_type(serializers.JSONField(default=1), serializers.JSONField)
assert_type(serializers.JSONField(default="abc"), serializers.JSONField)
assert_type(serializers.JSONField(default=[1, 2, 3]), serializers.JSONField)
assert_type(serializers.JSONField(default={"a": 1}), serializers.JSONField)
assert_type(serializers.JSONField(default=list), serializers.JSONField)
assert_type(serializers.JSONField(default=lambda: []), serializers.JSONField)
assert_type(serializers.JSONField(initial=1), serializers.JSONField)
assert_type(serializers.JSONField(initial="abc"), serializers.JSONField)
assert_type(serializers.JSONField(initial=[1, 2, 3]), serializers.JSONField)
assert_type(serializers.JSONField(initial={"a": 1}), serializers.JSONField)
assert_type(serializers.JSONField(initial=list), serializers.JSONField)
assert_type(serializers.JSONField(initial=lambda: []), serializers.JSONField)
