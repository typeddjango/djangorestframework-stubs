from mypy.plugin import MethodContext
from mypy.types import Instance, Type

from mypy_drf_plugin import helpers


def return_typeddict_from_to_representation(ctx: MethodContext) -> Type:
    serializer_type = ctx.type
    if not isinstance(serializer_type, Instance):
        return ctx.default_return_type

    typeddict_type = helpers.get_corresponding_typeddict(serializer_type, ctx.api,
                                                         use_primitive_types=True)
    return typeddict_type


def return_list_of_typeddict_for_list_serializer_from_to_representation(ctx: MethodContext) -> Type:
    serializer_type = ctx.type
    if not isinstance(serializer_type, Instance):
        return ctx.default_return_type

    child_sym = serializer_type.type.get('child')
    if child_sym is None or not isinstance(child_sym.type, Instance):
        return ctx.default_return_type

    child_typeddict_type = helpers.get_corresponding_typeddict(child_sym.type, ctx.api,
                                                               use_primitive_types=True)
    return ctx.api.named_generic_type('builtins.list', [child_typeddict_type])


def return_typeddict_from_to_internal_value(ctx: MethodContext) -> Type:
    serializer_type = ctx.type
    if not isinstance(serializer_type, Instance):
        return ctx.default_return_type

    typeddict_type = helpers.get_corresponding_typeddict(serializer_type, ctx.api,
                                                         use_primitive_types=False)
    return typeddict_type


def return_list_of_typeddict_for_list_serializer_from_to_internal_value(ctx: MethodContext) -> Type:
    serializer_type = ctx.type
    if not isinstance(serializer_type, Instance):
        return ctx.default_return_type

    child_sym = serializer_type.type.get('child')
    if child_sym is None or not isinstance(child_sym.type, Instance):
        return ctx.default_return_type

    child_typeddict_type = helpers.get_corresponding_typeddict(child_sym.type, ctx.api,
                                                               use_primitive_types=False)
    return ctx.api.named_generic_type('builtins.list', [child_typeddict_type])
