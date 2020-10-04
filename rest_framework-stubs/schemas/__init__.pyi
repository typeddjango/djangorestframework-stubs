from typing import Any, Callable, Optional, Sequence, Type

from rest_framework.renderers import BaseRenderer
from rest_framework.settings import api_settings as api_settings

from . import coreapi as coreapi
from . import openapi as openapi
from .coreapi import AutoSchema as AutoSchema
from .coreapi import ManualSchema as ManualSchema
from .coreapi import SchemaGenerator as SchemaGenerator
from .inspectors import DefaultSchema as DefaultSchema

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
