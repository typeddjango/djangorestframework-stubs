from mypy.maptype import map_instance_to_supertype
from mypy.nodes import ARG_NAMED_OPT, NameExpr
from mypy.plugin import ClassDefContext, FunctionSigContext
from mypy.types import AnyType, CallableType, Instance, NoneType, TypeOfAny, UnionType
from mypy.types import Type as MypyType
from mypy_django_plugin.lib import helpers as mypy_django_helpers

from mypy_drf_plugin.lib import fullnames


def make_meta_nested_class_inherit_from_any(ctx: ClassDefContext) -> None:
    meta_node = mypy_django_helpers.get_nested_meta_node_for_current_class(ctx.cls.info)
    if meta_node is None:
        return None
    meta_node.fallback_to_any = True


def _many_is_truthy(ctx: FunctionSigContext) -> bool:
    sig = ctx.default_signature
    try:
        many_idx = sig.arg_names.index("many")
    except ValueError:
        return False
    return any(isinstance(expr, NameExpr) and expr.fullname == "builtins.True" for expr in ctx.args[many_idx])


def _child_instance_type(sig: CallableType) -> MypyType:
    # Walk the child serializer's MRO up to BaseSerializer[_IN] and return the
    # bound _IN. Falls back to Any if the return type isn't a normal Instance
    # or BaseSerializer isn't in its MRO.
    ret = sig.ret_type
    if not isinstance(ret, Instance):
        return AnyType(TypeOfAny.special_form)
    base = next((b for b in ret.type.mro if b.fullname == fullnames.BASE_SERIALIZER_FULLNAME), None)
    if base is None or not base.type_vars:
        return AnyType(TypeOfAny.special_form)
    mapped = map_instance_to_supertype(ret, base)
    if not mapped.args:
        return AnyType(TypeOfAny.special_form)
    return mapped.args[0]


def transform_serializer_constructor_when_many(ctx: FunctionSigContext) -> CallableType:
    # A Serializer called with ``many=True`` is turned into a ListSerializer by
    # ``many_init`` at runtime. Reflect that by accepting ListSerializer-only
    # kwargs (``min_length`` / ``max_length``) and returning
    # ``ListSerializer[Iterable[_IN]]`` so that ``.instance`` keeps the
    # element type of the child serializer.
    sig = ctx.default_signature
    if not _many_is_truthy(ctx):
        return sig

    list_serializer_info = mypy_django_helpers.lookup_fully_qualified_typeinfo(
        ctx.api, fullnames.LIST_SERIALIZER_FULLNAME
    )
    if list_serializer_info is None:
        return sig

    int_or_none = UnionType([ctx.api.named_generic_type("builtins.int", []), NoneType()])

    new_arg_kinds = list(sig.arg_kinds)
    new_arg_names: list[str | None] = list(sig.arg_names)
    new_arg_types = list(sig.arg_types)
    for name in ("min_length", "max_length"):
        if name in sig.arg_names:
            continue
        new_arg_kinds.append(ARG_NAMED_OPT)
        new_arg_names.append(name)
        new_arg_types.append(int_or_none)

    iterable_of_child = ctx.api.named_generic_type("typing.Iterable", [_child_instance_type(sig)])

    return sig.copy_modified(
        arg_kinds=new_arg_kinds,
        arg_names=new_arg_names,
        arg_types=new_arg_types,
        ret_type=Instance(list_serializer_info, [iterable_of_child]),
    )
