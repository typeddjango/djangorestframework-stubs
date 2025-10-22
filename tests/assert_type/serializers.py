from collections.abc import Mapping, Sequence
from typing import Any, cast

from django.contrib.auth.models import User
from django.utils.functional import cached_property
from rest_framework import serializers
from rest_framework.relations import PKOnlyObject
from rest_framework.utils.serializer_helpers import BindingDict, ReturnDict, ReturnList
from typing_extensions import assert_type


# case: multiple_inheritance_from_two_serializers_with_meta_nested_class_defined
class SerializerA(serializers.Serializer):
    class Meta:
        pass


class SerializerB(serializers.Serializer):
    class Meta:
        pass


class SerializerC(SerializerA, SerializerB):
    pass


# case: model_serializer_meta_attributes
assert_type(serializers.ModelSerializer.Meta.model, type[serializers._MT])  # type: ignore[valid-type]
assert_type(serializers.ModelSerializer.Meta.fields, Sequence[str])
assert_type(serializers.ModelSerializer.Meta.read_only_fields, Sequence[str] | None)
assert_type(serializers.ModelSerializer.Meta.exclude, Sequence[str] | None)
assert_type(serializers.ModelSerializer.Meta.depth, int | None)
assert_type(serializers.ModelSerializer.Meta.extra_kwargs, dict[str, dict[str, Any]])


# case: test_model_serializer_passes_check
class TestSerializer(serializers.ModelSerializer):
    class Meta:
        model = User


def is_meta_model(serializer: type[serializers.ModelSerializer]) -> bool:
    return bool(serializer.Meta.model)


assert_type(is_meta_model(TestSerializer), bool)


# case: test_return_dict_reduce
class TestSerializer2(serializers.Serializer):
    def test(self) -> None:
        ret = ReturnDict({"a": "1"}, serializer=self)
        callable, args = ret.__reduce__()
        assert_type(callable(*args), dict[str, str])


# case: test_model_serializer_with_customized_serializer_field_mapping
class TestSerializer3(serializers.ModelSerializer):
    serializer_related_field = serializers.PrimaryKeyRelatedField
    serializer_related_to_field = serializers.SlugRelatedField
    serializer_url_field = serializers.HyperlinkedIdentityField
    serializer_choice_field = serializers.ChoiceField

    class Meta:
        model = User


# case: related_field_get_attribute_model_or_pk
field = serializers.PrimaryKeyRelatedField(queryset=User.objects.all())
user = cast("User", object())
value = field.get_attribute(user)
assert_type(value, User | PKOnlyObject | None)

# case: slug_related_field_accepts_pk_object
field = serializers.SlugRelatedField(slug_field="username", queryset=User.objects.all())
obj = PKOnlyObject(pk=1)
assert_type(field.to_representation(obj), str)


# case: test_hyperlinked_model_serializer_with_customized_serializer_field_mapping
class TestSerializer4(serializers.HyperlinkedModelSerializer):
    serializer_related_field = serializers.HyperlinkedRelatedField

    class Meta:
        model = User


# case: test_model_serializer_with_overriden_fields_property
class TestSerializer5(serializers.ModelSerializer):
    class Meta:
        model = User

    @cached_property
    def fields(self) -> BindingDict:
        return super().fields


# case: test_return_list
class TestSerializer6(serializers.Serializer):
    def test(self) -> None:
        ReturnList([], serializer=self)
        ReturnList((), serializer=self)
        ReturnList([{}], serializer=self)
        ReturnList(serializer=self)
        ret = ReturnList(["1"], serializer=self)
        assert_type(ret, ReturnList[str])


# case: test_return_list_reduce
class TestSerializer7(serializers.Serializer):
    def test(self) -> None:
        ret = ReturnList(["1"], serializer=self)
        callable, args = ret.__reduce__()
        assert_type(callable(*args), list[str])


# case: test_return_dict
class TestSerializer8(serializers.Serializer):
    def test(self) -> None:
        input: Mapping[str, str] = {}
        ReturnDict({}, serializer=self)
        ReturnDict([("a", "a")], serializer=self)
        ReturnDict(input, serializer=self)
        iterable = ""
        sep = " "
        ReturnDict((string.split(sep) for string in iterable), serializer=self)
        ReturnDict(serializer=self)
        ret = ReturnDict({"a": "a"}, serializer=self)
        assert_type(ret, ReturnDict[str, str])
        copy = ret.copy()
        assert_type(copy, ReturnDict[str, str])
