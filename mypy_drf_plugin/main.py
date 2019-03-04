from typing import Callable, Dict, Optional, Sequence

from mypy.nodes import TypeInfo
from mypy.options import Options
from mypy.plugin import AttributeContext, ClassDefContext, FunctionContext, MethodContext, Plugin
from mypy.types import Instance, Type

from mypy_drf_plugin import helpers, monkeypatch
from mypy_drf_plugin.transformers import fields, serializers, validation


def extract_base_model_fullname(serializer_type: Type) -> Optional[str]:
    if not isinstance(serializer_type, Instance):
        return None

    base_model_fullname = helpers.get_drf_metadata(serializer_type.type).get('base_model')
    if not base_model_fullname:
        return None

    return base_model_fullname


def get_instance_of_model_bound_to_serializer(ctx: MethodContext) -> Type:
    base_model_fullname = extract_base_model_fullname(ctx.type)
    if not base_model_fullname:
        return ctx.default_return_type

    try:
        return ctx.api.named_generic_type(base_model_fullname, [])
    except AssertionError:  # cannot find a model with name
        return ctx.default_return_type


class BaseClassTransformers:
    def __init__(self, hooks: Sequence[Callable]):
        self.hooks = hooks

    def __call__(self, ctx: ClassDefContext) -> None:
        for hook in self.hooks:
            hook(ctx)


class DRFPlugin(Plugin):
    def __init__(self, options: Options) -> None:
        super().__init__(options)
        monkeypatch.make_field_repr_not_return_any_generics()

    def _get_currently_defined_serializers(self) -> Dict[str, int]:
        base_serializer_sym = self.lookup_fully_qualified(helpers.BASE_SERIALIZER_FULLNAME)
        if base_serializer_sym is not None and isinstance(base_serializer_sym.node, TypeInfo):
            return (base_serializer_sym.node.metadata
                    .setdefault('drf', {})
                    .setdefault('serializer_bases', {helpers.BASE_SERIALIZER_FULLNAME: 1,
                                                     helpers.MODEL_SERIALIZER_FULLNAME: 1,
                                                     helpers.SERIALIZER_FULLNAME: 1}))
        else:
            return {}

    def _get_currently_defined_list_serializers(self) -> Dict[str, int]:
        list_serializer_sym = self.lookup_fully_qualified(helpers.LIST_SERIALIZER_FULLNAME)
        if list_serializer_sym is not None and isinstance(list_serializer_sym.node, TypeInfo):
            return (helpers.get_drf_metadata(list_serializer_sym.node)
                    .setdefault('list_serializer_bases', {helpers.LIST_SERIALIZER_FULLNAME: 1}))
        else:
            return {}

    def _get_defined_serializer_base_classes(self) -> Dict[str, int]:
        return {**self._get_currently_defined_serializers(), **self._get_currently_defined_list_serializers()}

    def _get_defined_field_base_classes(self) -> Dict[str, int]:
        base_field_sym = self.lookup_fully_qualified(helpers.FIELD_FULLNAME)
        if base_field_sym is not None and isinstance(base_field_sym.node, TypeInfo):
            return (helpers.get_drf_metadata(base_field_sym.node)
                    .setdefault('field_bases', {helpers.FIELD_FULLNAME: 1}))
        else:
            return {}

    def get_function_hook(self, fullname: str
                          ) -> Optional[Callable[[FunctionContext], Type]]:
        sym = self.lookup_fully_qualified(fullname)
        if sym is not None and isinstance(sym.node, TypeInfo):
            if sym.node.has_base(helpers.FIELD_FULLNAME):
                return fields.set_generic_parameters_for_field

    def get_method_hook(self, fullname: str
                        ) -> Optional[Callable[[MethodContext], Type]]:
        class_name, _, method_name = fullname.rpartition('.')
        if method_name == 'to_representation':
            if class_name in self._get_currently_defined_serializers():
                return validation.return_typeddict_from_to_representation

            if class_name in self._get_currently_defined_list_serializers():
                return validation.return_list_of_typeddict_for_list_serializer_from_to_representation

        if method_name in {'to_internal_value', 'run_validation'}:
            if class_name in self._get_currently_defined_serializers():
                return validation.return_typeddict_from_to_internal_value

            if class_name in self._get_currently_defined_list_serializers():
                return validation.return_list_of_typeddict_for_list_serializer_from_to_internal_value

        if method_name in {'create', 'save'}:
            if class_name in self._get_currently_defined_serializers():
                return get_instance_of_model_bound_to_serializer

    def get_base_class_hook(self, fullname: str
                            ) -> Optional[Callable[[ClassDefContext], None]]:
        if fullname in self._get_defined_serializer_base_classes():
            return BaseClassTransformers([serializers.transform_serializer_class,
                                          fields.set_types_metadata])

        if fullname in self._get_defined_field_base_classes():
            return fields.set_types_metadata


def plugin(version):
    return DRFPlugin
