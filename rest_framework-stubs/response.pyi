from typing import Any, Dict, List, Mapping, Optional, Tuple

from django.template.base import Template
from django.test.utils import ContextList
from django.template.response import SimpleTemplateResponse
from django.urls import ResolverMatch

from rest_framework.request import Request
from rest_framework.test import APIClient

class Response(SimpleTemplateResponse):
    data: Any
    exception: bool
    content_type: Optional[str]
    _request: Request
    def __init__(
        self,
        data: Any = ...,
        status: Optional[int] = ...,
        template_name: Optional[str] = ...,
        headers: Optional[Mapping[str, str]] = ...,
        exception: bool = ...,
        content_type: Optional[str] = ...,
    ): ...
    @property
    def rendered_content(self) -> Any: ...
    def render(self) -> Any: ...
    @property
    def status_text(self) -> str: ...

class _MonkeyPatchedResponse(Response):
    client: APIClient
    context: ContextList | Dict[str, Any]
    redirect_chain: List[Tuple[str, int]]
    request: Dict[str, Any]
    resolver_match: ResolverMatch
    templates: List[Template]
    def json(self) -> Any: ...
