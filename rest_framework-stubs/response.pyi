from collections.abc import Mapping
from typing import Any

from django.core.handlers.wsgi import WSGIRequest
from django.template.base import Template
from django.template.response import SimpleTemplateResponse
from django.test.utils import ContextList
from django.urls import ResolverMatch
from rest_framework.renderers import BaseRenderer
from rest_framework.request import Request
from rest_framework.test import APIClient
from typing_extensions import Self

class Response(SimpleTemplateResponse):
    data: Any
    exception: bool
    content_type: str | None
    accepted_renderer: BaseRenderer
    accepted_media_type: str
    _request: Request
    def __init__(
        self,
        data: Any = ...,
        status: int | None = ...,
        template_name: str | None = ...,
        headers: Mapping[str, str] | None = ...,
        exception: bool = ...,
        content_type: str | None = ...,
    ) -> None: ...
    def __class_getitem__(cls, *args: Any, **kwargs: Any) -> type[Self]: ...
    @property
    def rendered_content(self) -> Any: ...
    def render(self) -> Any: ...
    @property
    def status_text(self) -> str: ...

class _MonkeyPatchedResponse(Response):
    client: APIClient
    context: ContextList | dict[str, Any]
    redirect_chain: list[tuple[str, int]]
    request: dict[str, Any]
    wsgi_request: WSGIRequest
    resolver_match: ResolverMatch
    templates: list[Template]
    def json(self) -> Any: ...
