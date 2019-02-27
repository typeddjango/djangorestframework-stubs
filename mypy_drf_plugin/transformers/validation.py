from collections import OrderedDict

from mypy.plugin import CheckerPluginInterface, MethodContext
from mypy.types import Instance, Type, TypedDictType

from mypy_drf_plugin import helpers


def get_corresponding_typeddict(serializer_type: Instance,
                                api: CheckerPluginInterface,
                                use_primitive_types: bool = False) -> TypedDictType:
    typeddict_items = OrderedDict()
    for base in reversed(serializer_type.type.mro):
        for name, sym in base.names.items():
            if name in typeddict_items:
                continue
            typ = sym.type
            if isinstance(typ, Instance) and typ.type.has_base(helpers.FIELD_FULLNAME):
                if use_primitive_types:
                    typeddict_items[name] = typ.args[1]
                else:
                    typeddict_items[name] = typ.args[0]

    return TypedDictType(items=typeddict_items,
                         required_keys=set(typeddict_items.keys()),
                         fallback=api.named_generic_type('builtins.object', []))


def return_typeddict_from_to_representation(ctx: MethodContext) -> Type:
    serializer_type = ctx.type
    if not isinstance(serializer_type, Instance):
        return ctx.default_return_type

    typeddict_type = get_corresponding_typeddict(serializer_type, ctx.api,
                                                 use_primitive_types=True)
    return typeddict_type


def return_list_of_typeddict_for_list_serializer_from_to_representation(ctx: MethodContext) -> Type:
    serializer_type = ctx.type
    if not isinstance(serializer_type, Instance):
        return ctx.default_return_type

    child_sym = serializer_type.type.get('child')
    if child_sym is None or not isinstance(child_sym.type, Instance):
        return ctx.default_return_type

    child_typeddict_type = get_corresponding_typeddict(child_sym.type, ctx.api,
                                                       use_primitive_types=True)
    return ctx.api.named_generic_type('builtins.list', [child_typeddict_type])


def return_typeddict_from_to_internal_value(ctx: MethodContext) -> Type:
    serializer_type = ctx.type
    if not isinstance(serializer_type, Instance):
        return ctx.default_return_type

    typeddict_type = get_corresponding_typeddict(serializer_type, ctx.api,
                                                 use_primitive_types=False)
    return typeddict_type


def return_list_of_typeddict_for_list_serializer_from_to_internal_value(ctx: MethodContext) -> Type:
    serializer_type = ctx.type
    if not isinstance(serializer_type, Instance):
        return ctx.default_return_type

    child_sym = serializer_type.type.get('child')
    if child_sym is None or not isinstance(child_sym.type, Instance):
        return ctx.default_return_type

    child_typeddict_type = get_corresponding_typeddict(child_sym.type, ctx.api,
                                                       use_primitive_types=False)
    return ctx.api.named_generic_type('builtins.list', [child_typeddict_type])
