from collections import OrderedDict
from typing import Any, Dict

from mypy.nodes import TypeInfo
from mypy.plugin import CheckerPluginInterface
from mypy.types import Instance, TypedDictType, TypeOfAny, AnyType
# noinspection PyUnresolvedReferences
from mypy_django_plugin.helpers import get_argument_by_name, get_argument_type_by_name, get_assigned_value_for_class, \
    get_nested_meta_node_for_current_class, has_any_of_bases, is_none_expr, is_optional, iter_over_assignments, make_optional, \
    make_required, parse_bool, reparametrize_instance, get_model_fullname_from_string


FIELD_FULLNAME = 'rest_framework.fields.Field'
BASE_SERIALIZER_FULLNAME = 'rest_framework.serializers.BaseSerializer'
SERIALIZER_FULLNAME = 'rest_framework.serializers.Serializer'
LIST_SERIALIZER_FULLNAME = 'rest_framework.serializers.ListSerializer'
MODEL_SERIALIZER_FULLNAME = 'rest_framework.serializers.ModelSerializer'


def get_corresponding_typeddict(serializer_type: Instance,
                                api: CheckerPluginInterface,
                                use_primitive_types: bool = False) -> TypedDictType:
    typeddict_items = OrderedDict()
    for base in reversed(serializer_type.type.mro):
        for name, sym in base.names.items():
            if name in typeddict_items:
                continue
            typ = sym.type
            if isinstance(typ, Instance) and typ.type.has_base(FIELD_FULLNAME):
                if use_primitive_types:
                    typeddict_items[name] = typ.args[1]
                else:
                    typeddict_items[name] = typ.args[0]

    return TypedDictType(items=typeddict_items,
                         required_keys=set(typeddict_items.keys()),
                         fallback=api.named_generic_type('builtins.dict', [api.named_generic_type('builtins.str', []),
                                                                           AnyType(TypeOfAny.explicit)]))


def get_drf_metadata(info: TypeInfo) -> Dict[str, Any]:
    return info.metadata.setdefault('drf', {})
