from typing import Any, Dict, Mapping, Optional

from django.template.response import SimpleTemplateResponse

class Response(SimpleTemplateResponse):
    data: Optional[Any] = ...
    exception: bool = ...
    content_type: Optional[str] = ...
    def __init__(
        self,
        data: Optional[Any] = ...,
        status: Optional[int] = ...,
        template_name: Optional[str] = ...,
        headers: Optional[Mapping[str, Any]] = ...,
        exception: bool = ...,
        content_type: Optional[str] = ...,
    ): ...
    @property
    def status_text(self) -> str: ...
