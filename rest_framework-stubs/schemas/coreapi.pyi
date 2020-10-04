from collections import Counter, OrderedDict
from typing import Any, Dict, List, Optional, Sequence

from rest_frame.fields import Field
from rest_framework.compat import coreapi
from rest_framework.request import Request
from rest_framework.views import APIView

from .generators import BaseSchemaGenerator as BaseSchemaGenerator
from .inspectors import ViewInspector as ViewInspector

def common_path(paths: Any): ...
def is_custom_action(action: Any): ...
def distribute_links(obj: Any) -> None: ...

INSERT_INTO_COLLISION_FMT: str

class LinkNode(OrderedDict):
    links: List[Any] = ...
    methods_counter: Counter = ...
    def __init__(self) -> None: ...
    def get_available_key(self, preferred_key: str) -> str: ...

def insert_into(target: LinkNode, keys: Sequence[str], value: Any) -> None: ...

class SchemaGenerator(BaseSchemaGenerator):
    default_mapping: Dict[str, str] = ...
    coerce_method_names: Optional[Dict[str, str]] = ...
    def __init__(
        self,
        title: Optional[Any] = ...,
        url: Optional[Any] = ...,
        description: Optional[Any] = ...,
        patterns: Optional[Any] = ...,
        urlconf: Optional[Any] = ...,
        version: Optional[Any] = ...,
    ) -> None: ...
    def get_links(self, request: Optional[Request] = ...) -> Optional[LinkNode]: ...
    def get_schema(self, request: Optional[Request] = ..., public: bool = ...) -> Optional[coreapi.Document]: ...
    def get_keys(self, subpath: Any, method: Any, view: APIView) -> List[str]: ...
    def determine_path_prefix(self, paths: List[str]) -> str: ...

def field_to_schema(field: Field): ...

class AutoSchema(ViewInspector):
    def __init__(self, manual_fields: Optional[Sequence[Any]] = ...) -> None: ...
    def get_description(self, path: str, method: str) -> str: ...
    def get_path_fields(self, path: str, method: str) -> List[Any]: ...
    def get_serializer_fields(self, path: str, method: str) -> List[Any]: ...
    def get_pagination_fields(self, path: str, method: str) -> List[Any]: ...
    def get_filter_fields(self, path: str, method: str) -> List[Any]: ...
    def get_manual_fields(self, path: str, method: str) -> List[Any]: ...
    @staticmethod
    def update_fields(fields: List[Any], update_with: List[Any]) -> List[Any]: ...
    def get_encoding(self, path: str, method: str) -> Optional[str]: ...

class ManualSchema(ViewInspector):
    def __init__(self, fields: Sequence[Any], description: str = ..., encoding: Optional[str] = ...) -> None: ...
    def get_link(self, path: str, method: str, base_url: str): ...

def is_enabled(): ...
