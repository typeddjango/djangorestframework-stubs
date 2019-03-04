from typing import cast

from mypy.nodes import StrExpr, TypeInfo, TupleExpr, ListExpr, SetExpr
from mypy.plugin import ClassDefContext
from mypy.semanal import SemanticAnalyzerPass2

from mypy_drf_plugin import helpers


def make_meta_nested_class_inherit_from_any(ctx: ClassDefContext) -> None:
    meta_node = helpers.get_nested_meta_node_for_current_class(ctx.cls.info)
    if meta_node is None:
        return None
    meta_node.fallback_to_any = True


def save_model_class_to_serializer_metadata(ctx: ClassDefContext) -> None:
    base_model = helpers.get_meta_attribute_value(ctx, 'model')
    if not base_model:
        return None

    api = cast(SemanticAnalyzerPass2, ctx.api)
    if isinstance(base_model, StrExpr):
        base_model_fullname = helpers.get_model_fullname_from_string(base_model.value,
                                                                     all_modules=api.modules)
    else:
        base_model_fullname = base_model.fullname

    helpers.get_drf_metadata(ctx.cls.info)['base_model'] = base_model_fullname


def save_fields_sequence_to_serializer_metadata(ctx: ClassDefContext) -> None:
    fields = helpers.get_meta_attribute_value(ctx, 'fields')
    if not fields:
        return None

    field_names = []
    if isinstance(fields, (TupleExpr, ListExpr, SetExpr)):
        for field_expr in fields.items:
            if isinstance(field_expr, StrExpr):
                field_names.append(field_expr.value)

    helpers.get_drf_metadata(ctx.cls.info)['fields'] = field_names


def transform_serializer_class(ctx: ClassDefContext) -> None:
    if ctx.cls.info.has_base(helpers.LIST_SERIALIZER_FULLNAME):
        sym = ctx.api.lookup_fully_qualified_or_none(helpers.LIST_SERIALIZER_FULLNAME)
        if sym is not None and isinstance(sym.node, TypeInfo):
            helpers.get_drf_metadata(sym.node)['list_serializer_bases'][ctx.cls.fullname] = 1
    else:
        sym = ctx.api.lookup_fully_qualified_or_none(helpers.BASE_SERIALIZER_FULLNAME)
        if sym is not None and isinstance(sym.node, TypeInfo):
            helpers.get_drf_metadata(sym.node)['serializer_bases'][ctx.cls.fullname] = 1

        save_model_class_to_serializer_metadata(ctx)
        save_fields_sequence_to_serializer_metadata(ctx)

    make_meta_nested_class_inherit_from_any(ctx)
