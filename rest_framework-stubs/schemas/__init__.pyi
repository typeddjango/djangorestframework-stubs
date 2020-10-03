from typing import Any, Callable, Optional, Sequence, Type

from rest_framework.renderers import BaseRenderer
from .generators import BaseSchemaGenerator as BaseSchemaGenerator
from . import coreapi as coreapi, openapi as openapi
from .coreapi import AutoSchema as AutoSchema, ManualSchema as ManualSchema, SchemaGenerator as SchemaGenerator
from .inspectors import DefaultSchema as DefaultSchema
from rest_framework.settings import api_settings as api_settings

def get_schema_view(
    title: Optional[str] = ...,
    url: Optional[str] = ...,
    description: Optional[str] = ...,
    urlconf: Optional[str] = ...,
    renderer_classes: Optional[Sequence[Type[BaseRenderer]]] = ...,
    public: bool = ...,
    patterns: Optional[Sequence[Any]] = ...,
    generator_class: Type[BaseSchemaGenerator] = ...,
    authentication_classes: Sequence[str] = ...,
    permission_classes: Sequence[str] = ...,
    version: Optional[str] = ...,
) -> Callable[..., Any]: ...
