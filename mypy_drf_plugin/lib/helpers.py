from typing import Any

from mypy.nodes import TypeInfo


def get_drf_metadata(info: TypeInfo) -> dict[str, Any]:
    return info.metadata.setdefault("drf", {})
