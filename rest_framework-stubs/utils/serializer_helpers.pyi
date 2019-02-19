from typing import Any, Dict, List, Mapping, MutableMapping

from rest_framework.exceptions import ErrorDetail
from rest_framework.fields import Field
from rest_framework.serializers import BaseSerializer

class ReturnDict(dict):
    serializer: BaseSerializer

class ReturnList(list):
    serializer: BaseSerializer

class BoundField(object):
    """
    A field object that also includes `.value` and `.error` properties.
    Returned when iterating over a serializer instance,
    providing an API similar to Django forms and form fields.
    """

    value: Any
    fields: Dict[str, Field]
    errors: List[ErrorDetail]
    def __init__(self, field: Field, value: Any, errors: List[ErrorDetail], prefix: str = ...): ...
    def as_form_field(self) -> BoundField: ...

class JSONBoundField(BoundField): ...

class NestedBoundField(BoundField, Mapping[str, Field]):
    def __iter__(self): ...
    def __getitem__(self, key): ...

class BindingDict(MutableMapping[str, Field]): ...
