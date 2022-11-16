from collections.abc import Callable, Sequence
from typing import Any

from rest_framework.renderers import BaseRenderer
from rest_framework.urlpatterns import _AnyURL

from . import coreapi as coreapi
from . import openapi as openapi
from .coreapi import AutoSchema as AutoSchema
from .coreapi import ManualSchema as ManualSchema
from .coreapi import SchemaGenerator as SchemaGenerator
from .generators import BaseSchemaGenerator
from .inspectors import DefaultSchema as DefaultSchema

def get_schema_view(
    title: str | None = ...,
    url: str | None = ...,
    description: str | None = ...,
    urlconf: str | None = ...,
    renderer_classes: Sequence[type[BaseRenderer]] | None = ...,
    public: bool = ...,
    patterns: Sequence[_AnyURL] | None = ...,
    generator_class: type[BaseSchemaGenerator] = ...,
    authentication_classes: Sequence[str] = ...,
    permission_classes: Sequence[str] = ...,
    version: str | None = ...,
) -> Callable[..., Any]: ...
