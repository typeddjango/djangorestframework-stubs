from mypy.nodes import TypeInfo
from mypy.plugin import ClassDefContext

from mypy_drf_plugin import helpers


def make_meta_nested_class_inherit_from_any(ctx: ClassDefContext) -> None:
    meta_node = helpers.get_nested_meta_node_for_current_class(ctx.cls.info)
    if meta_node is None:
        return None
    meta_node.fallback_to_any = True


def save_model_class_to_serializer_metadata(ctx: ClassDefContext) -> None:
    meta_info = helpers.get_nested_meta_node_for_current_class(ctx.cls.info)
    if meta_info is None:
        return None

    base_model = helpers.get_assigned_value_for_class(meta_info, 'model')
    if base_model is None:
        return None

    ctx.cls.info.metadata.setdefault('drf', {})['base_model'] = base_model.fullname


def transform_serializer_class(ctx: ClassDefContext) -> None:
    sym = ctx.api.lookup_fully_qualified_or_none(helpers.BASE_SERIALIZER_FULLNAME)
    if sym is not None and isinstance(sym.node, TypeInfo):
        sym.node.metadata['django']['serializer_bases'][ctx.cls.fullname] = 1

    make_meta_nested_class_inherit_from_any(ctx)
    save_model_class_to_serializer_metadata(ctx)
