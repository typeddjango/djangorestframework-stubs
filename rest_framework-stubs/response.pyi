from typing import Any, Mapping

from django.template.response import SimpleTemplateResponse

from rest_framework.request import Request

class Response(SimpleTemplateResponse):
    data: Any
    exception: bool
    content_type: str | None
    _request: Request
    def __init__(
        self,
        data: Any = ...,
        status: int | None = ...,
        template_name: str | None = ...,
        headers: Mapping[str, str] | None = ...,
        exception: bool = ...,
        content_type: str | None = ...,
    ): ...
    @property
    def rendered_content(self) -> Any: ...
    def render(self) -> Any: ...
    @property
    def status_text(self) -> str: ...
