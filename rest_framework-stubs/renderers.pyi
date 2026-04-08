from collections.abc import Iterable, Mapping, Sequence
from json import JSONEncoder
from typing import Any, ClassVar, Literal

from django import forms
from rest_framework.fields import Field
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.serializers import BaseSerializer
from rest_framework.utils.field_mapping import ClassLookupDict
from rest_framework.utils.serializer_helpers import BoundField
from rest_framework.views import APIView
from typing_extensions import override

def zero_as_none(value: Any) -> Any: ...

class BaseRenderer:
    # DISCREPANCY: `media_type`, `format` cannot be None.
    # None is a placeholder, but all subclasses must override this to `str`.
    media_type: str
    format: str
    charset: str | None
    render_style: str
    def render(
        self, data: Any, accepted_media_type: str | None = ..., renderer_context: Mapping[str, Any] | None = ...
    ) -> str | bytes: ...

class JSONRenderer(BaseRenderer):
    encoder_class: ClassVar[type[JSONEncoder]]
    ensure_ascii: ClassVar[bool]
    compact: ClassVar[bool]
    strict: ClassVar[bool]
    def get_indent(self, accepted_media_type: str, renderer_context: Mapping[str, Any]) -> int | None: ...
    @override
    def render(
        self, data: Any, accepted_media_type: str | None = ..., renderer_context: Mapping[str, Any] | None = ...
    ) -> bytes: ...

class TemplateHTMLRenderer(BaseRenderer):
    template_name: str | None
    exception_template_names: Sequence[str]
    def resolve_template(self, template_names: Iterable[str]) -> Any: ...  # Any: Django template backend object
    def get_template_context(self, data: Any, renderer_context: Mapping[str, Any]) -> dict[str, Any]: ...
    def get_template_names(self, response: Response, view: APIView) -> list[str]: ...
    def get_exception_template(self, response: Response) -> Any: ...  # Any: Django template backend object
    @override
    def render(
        self, data: Any, accepted_media_type: str | None = ..., renderer_context: Mapping[str, Any] | None = ...
    ) -> str: ...

class StaticHTMLRenderer(TemplateHTMLRenderer):
    @override
    def render(
        self, data: Any, accepted_media_type: str | None = ..., renderer_context: Mapping[str, Any] | None = ...
    ) -> str: ...

class HTMLFormRenderer(BaseRenderer):
    template_pack: str
    base_template: str

    default_style: ClassLookupDict[type[Field], dict[str, Any]]
    def render_field(self, field: BoundField, parent_style: Mapping[str, Any]) -> str: ...
    @override
    def render(
        self, data: Any, accepted_media_type: str | None = ..., renderer_context: Mapping[str, Any] | None = ...
    ) -> str: ...

class BrowsableAPIRenderer(BaseRenderer):
    """
    HTML renderer used to self-document the API.
    """

    template: str
    filter_template: str
    code_style: str
    form_renderer_class: type[BaseRenderer]
    def get_default_renderer(self, view: APIView) -> BaseRenderer | None: ...
    def get_content(
        self, renderer: BaseRenderer, data: Any, accepted_media_type: str | None, renderer_context: Mapping[str, Any]
    ) -> str: ...
    def show_form_for_method(self, view: APIView, method: str, request: Request, obj: Any) -> bool | None: ...
    def _get_serializer(
        self,
        serializer_class: type[BaseSerializer],
        view_instance: APIView,
        request: Request,
        *args: Any,  # Any: forwarded to serializer_class constructor
        **kwargs: Any,  # Any: forwarded to serializer_class constructor
    ) -> BaseSerializer: ...
    def get_rendered_html_form(
        self, data: Any, view: APIView, method: str, request: Request
    ) -> str | Literal[True] | None: ...
    def render_form_for_serializer(self, serializer: BaseSerializer) -> str | bytes | None: ...
    def get_raw_data_form(self, data: Any, view: APIView, method: str, request: Request) -> forms.Form | None: ...
    def get_name(self, view: APIView) -> str: ...
    def get_description(self, view: APIView, status_code: int) -> str: ...
    def get_breadcrumbs(self, request: Request) -> list[tuple[str, str]]: ...
    def get_extra_actions(self, view: APIView, status_code: int) -> dict[str, str] | None: ...
    def get_filter_form(self, data: Any, view: APIView, request: Request) -> str | None: ...
    def get_context(
        self, data: Any, accepted_media_type: str | None, renderer_context: Mapping[str, Any]
    ) -> dict[str, Any]: ...
    @override
    def render(
        self, data: Any, accepted_media_type: str | None = ..., renderer_context: Mapping[str, Any] | None = ...
    ) -> str: ...

class AdminRenderer(BrowsableAPIRenderer):
    def get_result_url(self, result: Mapping[str, Any], view: APIView) -> str | None: ...
    @override
    def render(
        self, data: Any, accepted_media_type: str | None = ..., renderer_context: Mapping[str, Any] | None = ...
    ) -> str: ...

class MultiPartRenderer(BaseRenderer):
    BOUNDARY: str
    @override
    def render(
        self, data: Any, accepted_media_type: str | None = ..., renderer_context: Mapping[str, Any] | None = ...
    ) -> bytes: ...

class OpenAPIRenderer(BaseRenderer):
    def __init__(self) -> None: ...
    @override
    def render(
        self, data: Any, media_type: str | None = ..., renderer_context: Mapping[str, Any] | None = ...
    ) -> bytes: ...

class JSONOpenAPIRenderer(BaseRenderer):
    encoder_class: ClassVar[type[JSONEncoder]]
    ensure_ascii: ClassVar[bool]
    @override
    def render(
        self, data: Any, media_type: str | None = ..., renderer_context: Mapping[str, Any] | None = ...
    ) -> bytes: ...
