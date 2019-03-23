from typing import Any, Callable, Optional, Sequence, Type

from rest_framework.renderers import BaseRenderer

from rest_framework.schemas import SchemaGenerator

def get_docs_view(
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
) -> Callable[..., Any]: ...
def get_schemajs_view(
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
) -> Callable[..., Any]: ...
def include_docs_urls(
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
) -> Any: ...
