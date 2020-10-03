from .generators import BaseSchemaGenerator as BaseSchemaGenerator
from .inspectors import ViewInspector as ViewInspector
from collections import OrderedDict
from typing import Any, Optional

def common_path(paths: Any): ...
def is_custom_action(action: Any): ...
def distribute_links(obj: Any) -> None: ...

INSERT_INTO_COLLISION_FMT: str

class LinkNode(OrderedDict):
    links: Any = ...
    methods_counter: Any = ...
    def __init__(self) -> None: ...
    def get_available_key(self, preferred_key: Any): ...

def insert_into(target: Any, keys: Any, value: Any) -> None: ...

class SchemaGenerator(BaseSchemaGenerator):
    default_mapping: Any = ...
    coerce_method_names: Any = ...
    def __init__(self, title: Optional[Any] = ..., url: Optional[Any] = ..., description: Optional[Any] = ..., patterns: Optional[Any] = ..., urlconf: Optional[Any] = ..., version: Optional[Any] = ...) -> None: ...
    def get_links(self, request: Optional[Any] = ...): ...
    def get_schema(self, request: Optional[Any] = ..., public: bool = ...): ...
    def get_keys(self, subpath: Any, method: Any, view: Any): ...
    def determine_path_prefix(self, paths: Any): ...

def field_to_schema(field: Any): ...

class AutoSchema(ViewInspector):
    def __init__(self, manual_fields: Optional[Any] = ...) -> None: ...
    def get_link(self, path: Any, method: Any, base_url: Any): ...
    def get_path_fields(self, path: Any, method: Any): ...
    def get_serializer_fields(self, path: Any, method: Any): ...
    def get_pagination_fields(self, path: Any, method: Any): ...
    def get_filter_fields(self, path: Any, method: Any): ...
    def get_manual_fields(self, path: Any, method: Any): ...
    @staticmethod
    def update_fields(fields: Any, update_with: Any): ...
    def get_encoding(self, path: Any, method: Any): ...

class ManualSchema(ViewInspector):
    def __init__(self, fields: Any, description: str = ..., encoding: Optional[Any] = ...) -> None: ...
    def get_link(self, path: Any, method: Any, base_url: Any): ...

def is_enabled(): ...
