from typing import Callable, Dict, Optional

from mypy.nodes import TypeInfo
from mypy.options import Options
from mypy.plugin import ClassDefContext, Plugin
from mypy_django_plugin import main as mypy_django_main
from mypy_django_plugin.django.context import DjangoContext

from mypy_drf_plugin.lib import fullnames, helpers
from mypy_drf_plugin.transformers import serializers


def transform_serializer_class(ctx: ClassDefContext) -> None:
    sym = ctx.api.lookup_fully_qualified_or_none(fullnames.BASE_SERIALIZER_FULLNAME)
    if sym is not None and isinstance(sym.node, TypeInfo):
        helpers.get_drf_metadata(sym.node)['serializer_bases'][ctx.cls.fullname] = 1

    serializers.make_meta_nested_class_inherit_from_any(ctx)


class NewSemanalDRFPlugin(Plugin):
    def __init__(self, options: Options) -> None:
        super().__init__(options)

        django_settings_module = mypy_django_main.extract_django_settings_module(options.config_file)
        self.django_context = DjangoContext(django_settings_module)

    def _get_currently_defined_serializers(self) -> Dict[str, int]:
        base_serializer_sym = self.lookup_fully_qualified(fullnames.BASE_SERIALIZER_FULLNAME)
        if base_serializer_sym is not None and isinstance(base_serializer_sym.node, TypeInfo):
            return (base_serializer_sym.node.metadata
                    .setdefault('drf', {})
                    .setdefault('serializer_bases', {fullnames.BASE_SERIALIZER_FULLNAME: 1}))
        else:
            return {}

    def get_base_class_hook(self, fullname: str
                            ) -> Optional[Callable[[ClassDefContext], None]]:
        if fullname in self._get_currently_defined_serializers():
            return transform_serializer_class
        return None


def plugin(version):
    return NewSemanalDRFPlugin
