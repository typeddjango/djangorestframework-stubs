from typing import Optional

from mypy.nodes import TypeInfo

BASE_SERIALIZER_FULLNAME = 'rest_framework.serializers.BaseSerializer'
SERIALIZER_FULLNAME = 'rest_framework.serializers.Serializer'
MODEL_SERIALIZER_FULLNAME = 'rest_framework.serializers.ModelSerializer'


def get_nested_meta_node_from_current_class(info: TypeInfo) -> Optional[TypeInfo]:
    metaclass_sym = info.names.get('Meta')
    if metaclass_sym is not None and isinstance(metaclass_sym.node, TypeInfo):
        return metaclass_sym.node
    return None

