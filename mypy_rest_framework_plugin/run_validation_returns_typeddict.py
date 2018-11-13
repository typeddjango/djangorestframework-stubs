from collections import OrderedDict
from typing import Optional, Callable, cast

from mypy.checker import TypeChecker
from mypy.plugin import Plugin, MethodContext
from mypy.types import Type, TypedDictType, Instance


def is_field_subtype(typ: Instance) -> bool:
    for base in typ.type.bases:
        if base.type.fullname() == 'rest_framework.fields.Field':
            return True
    return False


def extract_descriptor_return_type(typ: Instance) -> Type:
    descriptor_get_node = typ.type.names.get('__get__', None)
    if descriptor_get_node is None:
        return typ

    return descriptor_get_node.type.ret_type


def return_typeddict_from_run_validation(ctx: MethodContext) -> Type:
    api = cast(TypeChecker, ctx.api)

    typeddict_items = OrderedDict()
    for name, node in ctx.type.type.names.items():
        if not is_field_subtype(node.type):
            continue

        node_real_type = extract_descriptor_return_type(node.type)
        typeddict_items[name] = node_real_type

    return TypedDictType(items=typeddict_items,
                         required_keys=set(typeddict_items.keys()),
                         fallback=api.named_type('builtins.object'))


class RunValidationPlugin(Plugin):
    def get_method_hook(self, fullname: str
                        ) -> Optional[Callable[[MethodContext], Type]]:
        if fullname.endswith('run_validation'):
            return return_typeddict_from_run_validation
        return None


def plugin(version):
    return RunValidationPlugin
