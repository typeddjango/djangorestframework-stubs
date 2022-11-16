from collections.abc import Callable, Sequence
from typing import Any

from rest_framework.renderers import BaseRenderer
from rest_framework.schemas import SchemaGenerator
from rest_framework.urlpatterns import _AnyURL

def get_docs_view(
    title: str | None = ...,
    url: str | None = ...,
    description: str | None = ...,
    urlconf: str | None = ...,
    renderer_classes: Sequence[type[BaseRenderer]] | None = ...,
    public: bool = ...,
    patterns: Sequence[_AnyURL] | None = ...,
    generator_class: type[SchemaGenerator] = ...,
    authentication_classes: Sequence[str] = ...,
    permission_classes: Sequence[str] = ...,
) -> Callable[..., Any]: ...
def get_schemajs_view(
    title: str | None = ...,
    url: str | None = ...,
    description: str | None = ...,
    urlconf: str | None = ...,
    renderer_classes: Sequence[type[BaseRenderer]] | None = ...,
    public: bool = ...,
    patterns: Sequence[_AnyURL] | None = ...,
    generator_class: type[SchemaGenerator] = ...,
    authentication_classes: Sequence[str] = ...,
    permission_classes: Sequence[str] = ...,
) -> Callable[..., Any]: ...
def include_docs_urls(
    title: str | None = ...,
    url: str | None = ...,
    description: str | None = ...,
    urlconf: str | None = ...,
    renderer_classes: Sequence[type[BaseRenderer]] | None = ...,
    public: bool = ...,
    patterns: Sequence[_AnyURL] | None = ...,
    generator_class: type[SchemaGenerator] = ...,
    authentication_classes: Sequence[str] = ...,
    permission_classes: Sequence[str] = ...,
) -> Any: ...
