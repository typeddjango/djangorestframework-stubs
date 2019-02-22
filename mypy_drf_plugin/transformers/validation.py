from collections import OrderedDict

from mypy.plugin import MethodContext
from mypy.types import Instance, Type, TypedDictType

from mypy_drf_plugin import helpers


def return_typeddict_from_run_validation(ctx: MethodContext) -> Type:
    serializer_type = ctx.type
    if not isinstance(serializer_type, Instance):
        return ctx.default_return_type

    typeddict_items = OrderedDict()
    for base in reversed(serializer_type.type.mro):
        for name, sym in base.names.items():
            if name in typeddict_items:
                continue
            typ = sym.type
            if isinstance(typ, Instance) and typ.type.has_base(helpers.FIELD_FULLNAME):
                typeddict_items[name] = typ.args[0]

    return TypedDictType(items=typeddict_items,
                         required_keys=set(typeddict_items.keys()),
                         fallback=ctx.api.named_generic_type('builtins.object', []))
