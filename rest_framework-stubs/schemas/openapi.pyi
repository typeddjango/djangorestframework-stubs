from typing import Any, Optional, Dict, Type, TypedDict, List, Sequence

from rest_framework import RemovedInDRF314Warning as RemovedInDRF314Warning
from rest_framework import exceptions as exceptions
from rest_framework import renderers as renderers
from rest_framework import serializers as serializers
from rest_framework.compat import uritemplate as uritemplate
from rest_framework.fields import empty as empty
from rest_framework.settings import api_settings as api_settings

from .generators import BaseSchemaGenerator as BaseSchemaGenerator
from .inspectors import ViewInspector as ViewInspector
from .utils import get_pk_description as get_pk_description
from .utils import is_list_view as is_list_view

from rest_framework.pagination import BasePagination
from rest_framework.fields import Field
from rest_framework.serializers import BaseSerializer
from rest_framework.request import Request

# OpenAPI requires its own typings. Below are minimal typing.
# TODO: evaluate using a 3rd party typing package for this, e.g.: https://github.com/meeshkan/openapi-typed

class DRFOpenAPIInfo(TypedDict, total=False):
    title: str
    version: str
    description: str

class DRFOpenAPISchema(TypedDict, total=False):
    openapi: str
    info: DRFOpenAPIInfo
    paths: Dict[str, Dict[str, Any]]
    components: Dict[str, Dict[str, Any]]

class SchemaGenerator(BaseSchemaGenerator):
    def get_info(self) -> DRFOpenAPIInfo: ...
    def check_duplicate_operation_id(self, paths: Dict[str, Dict[str, Any]]) -> None: ...
    def get_schema(self, request: Request = ..., public: bool = ...) -> DRFOpenAPISchema: ...  # type: ignore[override]

class AutoSchema(ViewInspector):
    operation_id_base: Optional[str] = ...
    component_name: Optional[str] = ...
    request_media_types: List[str] = ...
    response_media_types: List[str] = ...
    method_mapping: Dict[str, str] = ...
    def __init__(
        self, tags: Sequence[str] = ..., operation_id_base: Optional[str] = ..., component_name: Optional[str] = ...
    ) -> None: ...
    def get_operation(self, path: str, method: str) -> Dict[str, Any]: ...
    def get_component_name(self, serializer: BaseSerializer) -> str: ...
    def get_components(self, path: str, method: str) -> Dict[str, Any]: ...
    def get_operation_id_base(self, path: str, method: str, action: Any) -> str: ...
    def get_operation_id(self, path: str, method: str) -> str: ...
    def get_path_parameters(self, path: str, method: str) -> List[Dict[str, Any]]: ...
    def get_filter_parameters(self, path: str, method: str) -> List[Dict[str, Any]]: ...
    def allows_filters(self, path: str, method: str) -> bool: ...
    def get_pagination_parameters(self, path: str, method: str) -> List[Dict[str, Any]]: ...
    def map_choicefield(self, field: Field) -> Dict[str, Any]: ...
    def map_field(self, field: Field) -> Dict[str, Any]: ...
    def map_serializer(self, serializer: BaseSerializer) -> Dict[str, Any]: ...
    def map_field_validators(self, field: Any, schema: Any) -> None: ...
    def get_paginator(self) -> Optional[Type[BasePagination]]: ...
    def map_parsers(self, path: str, method: str) -> List[str]: ...
    def map_renderers(self, path: str, method: str) -> List[str]: ...
    def get_serializer(self, path: str, method: str) -> Optional[BaseSerializer]: ...
    def get_request_body(self, path: str, method: str) -> Dict[str, Any]: ...
    def get_responses(self, path: str, method: str) -> Dict[str, Any]: ...
    def get_tags(self, path: str, method: str) -> List[str]: ...
