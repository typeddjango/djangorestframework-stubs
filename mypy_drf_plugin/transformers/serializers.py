from mypy.nodes import ARG_NAMED_OPT, NameExpr
from mypy.plugin import ClassDefContext, FunctionSigContext
from mypy.types import CallableType, NoneType, UnionType
from mypy_django_plugin.lib import helpers as mypy_django_helpers


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


def add_list_serializer_kwargs_when_many(ctx: FunctionSigContext) -> CallableType:
    # When a Serializer is instantiated with ``many=True`` it becomes a
    # ListSerializer at runtime, which accepts ``min_length`` / ``max_length``.
    sig = ctx.default_signature
    if not _many_is_truthy(ctx):
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

    return sig.copy_modified(
        arg_kinds=new_arg_kinds,
        arg_names=new_arg_names,
        arg_types=new_arg_types,
    )
