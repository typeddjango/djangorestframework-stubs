from typing import Any, Dict

from mypy.nodes import TypeInfo


def get_drf_metadata(info: TypeInfo) -> Dict[str, Any]:
    return info.metadata.setdefault('drf', {})
