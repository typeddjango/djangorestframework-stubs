from typing import Any, Dict, Mapping, Optional

from django.template.response import SimpleTemplateResponse

class Response(SimpleTemplateResponse):
    """
    An HttpResponse that allows its data to be rendered into
    arbitrary media types.
    """

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
    def rendered_content(self) -> Any: ...
    @property
    def status_text(self) -> str: ...
    def __getstate__(self) -> Dict[str, Any]: ...
