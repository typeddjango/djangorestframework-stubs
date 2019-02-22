from typing import Callable, Dict, Optional

from mypy.nodes import TypeInfo
from mypy.plugin import ClassDefContext, Plugin

from mypy_drf_plugin import helpers


def make_meta_nested_class_inherit_from_any(ctx: ClassDefContext) -> None:
    meta_node = helpers.get_nested_meta_node_from_current_class(ctx.cls.info)
    if meta_node is None:
        return None
    meta_node.fallback_to_any = True


def transform_serializer_class(ctx: ClassDefContext) -> None:
    sym = ctx.api.lookup_fully_qualified_or_none(helpers.BASE_SERIALIZER_FULLNAME)
    if sym is not None and isinstance(sym.node, TypeInfo):
        sym.node.metadata['django']['modelform_bases'][ctx.cls.fullname] = 1

    make_meta_nested_class_inherit_from_any(ctx)


class DRFPlugin(Plugin):
    def _get_current_serializer_bases(self) -> Dict[str, int]:
        base_serializer_sym = self.lookup_fully_qualified(helpers.BASE_SERIALIZER_FULLNAME)
        if base_serializer_sym is not None and isinstance(base_serializer_sym.node, TypeInfo):
            return (base_serializer_sym.node.metadata
                    .setdefault('django', {})
                    .setdefault('modelform_bases', {helpers.BASE_SERIALIZER_FULLNAME: 1,
                                                    helpers.MODEL_SERIALIZER_FULLNAME: 1,
                                                    helpers.SERIALIZER_FULLNAME: 1}))
        else:
            return {}

    def get_base_class_hook(self, fullname: str
                            ) -> Optional[Callable[[ClassDefContext], None]]:
        if fullname in self._get_current_serializer_bases():
            return transform_serializer_class
        return None


def plugin(version):
    return DRFPlugin
