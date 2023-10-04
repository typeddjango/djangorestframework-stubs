from collections.abc import MutableMapping, Sequence
from typing import Any, Generic, TypeVar

from _typeshed import Incomplete
from django.db import models

NUMERIC_FIELD_TYPES: Sequence[type[models.Field]]

_K = TypeVar("_K", bound=type)
_V = TypeVar("_V")

class ClassLookupDict(Generic[_K, _V]):
    mapping: MutableMapping[type[_K], _V]
    def __init__(self, mapping: MutableMapping[type[_K], _V]) -> None: ...
    def __getitem__(self, key: _K) -> _V: ...
    def __setitem__(self, key: _K, value: _V) -> None: ...

def needs_label(model_field: models.Field, field_name: str) -> bool: ...
def get_detail_view_name(model: models.Model) -> str: ...
def get_field_kwargs(field_name: str, model_field: models.Field) -> dict[str, Any]: ...
def get_relation_kwargs(field_name: str, relation_info: Incomplete) -> dict[str, Any]: ...
def get_nested_relation_kwargs(relation_info: Incomplete) -> dict[str, Any]: ...
def get_url_kwargs(model_field: models.Model) -> dict[str, Any]: ...
