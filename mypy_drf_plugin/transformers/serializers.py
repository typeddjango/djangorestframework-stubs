from mypy.plugin import ClassDefContext
from mypy_django_plugin.lib import helpers as mypy_django_helpers


def make_meta_nested_class_inherit_from_any(ctx: ClassDefContext) -> None:
    meta_node = mypy_django_helpers.get_nested_meta_node_for_current_class(ctx.cls.info)
    if meta_node is None:
        return None
    meta_node.fallback_to_any = True
