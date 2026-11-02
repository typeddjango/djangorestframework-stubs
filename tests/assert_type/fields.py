from collections.abc import Mapping
from typing import Any, assert_type

from rest_framework import serializers
from rest_framework.fields import FloatField, JSONField

# case: field_get_attribute_returns_value_type
field = serializers.CharField()
result = field.get_attribute(object())
assert_type(result, str | None)

# case: field_context_is_mapping
assert_type(field.context, Mapping[str, Any])

# case: float_field_args_fields
FloatField(min_value=1, max_value=1.0)
FloatField(min_value=1.2, max_value=1)

# case: field_error_messages_accepts_mapping
error_messages: Mapping[str, str] = {"required": "Required."}
serializers.CharField(error_messages=error_messages)
serializers.IntegerField(error_messages=error_messages)

# case: json_field_default_and_initial
JSONField(allow_null=True, default=None, initial=None)
JSONField(default=1, initial=1)
JSONField(default=1.5, initial=1.5)
JSONField(default=True, initial=True)
JSONField(default="str", initial="str")
JSONField(default={}, initial={})
JSONField(default={"a": 1, "b": 2}, initial={"a": 1, "b": 2})
JSONField(default=[], initial=[])
JSONField(default=[1, 2, "three"], initial=[1, 2, "three"])
JSONField(default=(1, 2, 3), initial=(1, 2, 3))
JSONField(default=list, initial=list)
JSONField(default=dict, initial=dict)
JSONField(default=lambda: [], initial=lambda: [])
JSONField(default=lambda: {"a": [], "b": "str"}, initial=lambda: {"a": [], "b": "str"})
JSONField(default=lambda: 123, initial=lambda: 123)

# case: json_field_invalid_default_and_initial
JSONField(default=object())  # type: ignore[arg-type]
JSONField(initial=object())  # type: ignore[arg-type]
non_string_keys: Mapping[int, str] = {1: "value"}
JSONField(default=non_string_keys)  # type: ignore[arg-type]
JSONField(initial=non_string_keys)  # type: ignore[arg-type]
