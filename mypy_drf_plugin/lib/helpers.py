from typing import Any, Dict

from mypy.nodes import TypeInfo
from mypy_django_plugin.lib import helpers as mypy_django_helpers


def get_drf_metadata(info: TypeInfo) -> Dict[str, Any]:
    return info.metadata.setdefault('drf', {})
