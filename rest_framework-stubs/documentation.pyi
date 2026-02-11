from collections.abc import Callable, Sequence
from typing import Any

from rest_framework.authentication import BaseAuthentication
from rest_framework.permissions import _PermissionClass
from rest_framework.renderers import BaseRenderer
from rest_framework.schemas import SchemaGenerator
from rest_framework.urlpatterns import _AnyURL

def get_docs_view(
    title: str | None = ...,
    description: str | None = ...,
    schema_url: str | None = ...,
    urlconf: str | None = ...,
    public: bool = ...,
    patterns: Sequence[_AnyURL] | None = ...,
    generator_class: type[SchemaGenerator] = ...,
    authentication_classes: Sequence[type[BaseAuthentication]] = ...,
    permission_classes: Sequence[_PermissionClass] = ...,
    renderer_classes: Sequence[type[BaseRenderer]] | None = ...,
) -> Callable[..., Any]: ...
def get_schemajs_view(
    title: str | None = ...,
    description: str | None = ...,
    schema_url: str | None = ...,
    urlconf: str | None = ...,
    public: bool = ...,
    patterns: Sequence[_AnyURL] | None = ...,
    generator_class: type[SchemaGenerator] = ...,
    authentication_classes: Sequence[type[BaseAuthentication]] = ...,
    permission_classes: Sequence[_PermissionClass] = ...,
) -> Callable[..., Any]: ...
def include_docs_urls(
    title: str | None = ...,
    description: str | None = ...,
    schema_url: str | None = ...,
    urlconf: str | None = ...,
    public: bool = ...,
    patterns: Sequence[_AnyURL] | None = ...,
    generator_class: type[SchemaGenerator] = ...,
    authentication_classes: Sequence[type[BaseAuthentication]] = ...,
    permission_classes: Sequence[_PermissionClass] = ...,
    renderer_classes: Sequence[type[BaseRenderer]] | None = ...,
) -> Any: ...
