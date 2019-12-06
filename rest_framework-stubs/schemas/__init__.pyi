from typing import Any, Callable, Optional, Sequence, Type

from rest_framework.renderers import BaseRenderer

from .generators import SchemaGenerator as SchemaGenerator
from .inspectors import AutoSchema as AutoSchema, DefaultSchema as DefaultSchema, ManualSchema as ManualSchema

def get_schema_view(
    title: Optional[str] = ...,
    url: Optional[str] = ...,
    description: Optional[str] = ...,
    urlconf: Optional[str] = ...,
    renderer_classes: Optional[Sequence[Type[BaseRenderer]]] = ...,
    public: bool = ...,
    patterns: Optional[Sequence[Any]] = ...,
    generator_class: Type[SchemaGenerator] = ...,
    authentication_classes: Sequence[str] = ...,
    permission_classes: Sequence[str] = ...,
    version: Optional[str] = ...,
) -> Callable[..., Any]: ...
