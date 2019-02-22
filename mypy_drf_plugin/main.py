from typing import Callable, Dict, Optional

from mypy.nodes import TypeInfo
from mypy.plugin import ClassDefContext, FunctionContext, MethodContext, Plugin
from mypy.types import Type

from mypy_drf_plugin import helpers
from mypy_drf_plugin.transformers import fields, validation


def make_meta_nested_class_inherit_from_any(ctx: ClassDefContext) -> None:
    meta_node = helpers.get_nested_meta_node_for_current_class(ctx.cls.info)
    if meta_node is None:
        return None
    meta_node.fallback_to_any = True


def transform_serializer_class(ctx: ClassDefContext) -> None:
    sym = ctx.api.lookup_fully_qualified_or_none(helpers.BASE_SERIALIZER_FULLNAME)
    if sym is not None and isinstance(sym.node, TypeInfo):
        sym.node.metadata['django']['modelform_bases'][ctx.cls.fullname] = 1

    make_meta_nested_class_inherit_from_any(ctx)


class DRFPlugin(Plugin):
    def _get_currently_defined_serializers(self) -> Dict[str, int]:
        base_serializer_sym = self.lookup_fully_qualified(helpers.BASE_SERIALIZER_FULLNAME)
        if base_serializer_sym is not None and isinstance(base_serializer_sym.node, TypeInfo):
            return (base_serializer_sym.node.metadata
                    .setdefault('django', {})
                    .setdefault('modelform_bases', {helpers.BASE_SERIALIZER_FULLNAME: 1,
                                                    helpers.MODEL_SERIALIZER_FULLNAME: 1,
                                                    helpers.SERIALIZER_FULLNAME: 1}))
        else:
            return {}

    def get_function_hook(self, fullname: str
                          ) -> Optional[Callable[[FunctionContext], Type]]:
        sym = self.lookup_fully_qualified(fullname)
        if sym is not None and isinstance(sym.node, TypeInfo):
            if sym.node.has_base(helpers.FIELD_FULLNAME):
                return fields.fill_parameters_of_descriptor_methods_from_private_attributes

    def get_method_hook(self, fullname: str
                        ) -> Optional[Callable[[MethodContext], Type]]:
        class_name, _, method_name = fullname.rpartition('.')
        if method_name == 'run_validation' and class_name in self._get_currently_defined_serializers():
            return validation.return_typeddict_from_run_validation

    def get_base_class_hook(self, fullname: str
                            ) -> Optional[Callable[[ClassDefContext], None]]:
        if fullname in self._get_currently_defined_serializers():
            return transform_serializer_class


def plugin(version):
    return DRFPlugin
