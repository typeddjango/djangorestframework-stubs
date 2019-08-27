from typing import Any, Callable, Dict, Iterable, List, Mapping, Optional, Protocol, Sequence, Union

from django.db.models import Model
from django.db.models.query import QuerySet
from rest_framework.fields import Field, _Validator
from rest_framework.request import Request

def method_overridden(method_name: str, klass: type, instance: Any) -> bool: ...

class ObjectValueError(ValueError): ...
class ObjectTypeError(TypeError): ...

class Hyperlink(str):
    is_hyperlink: bool = ...
    obj: Any
    def __new__(cls, url: str, obj: Any) -> Hyperlink: ...
    @property
    def name(self) -> str: ...

class PKOnlyObject(object):
    def __init__(self, pk: Any) -> None: ...

MANY_RELATION_KWARGS: Sequence[str] = ...

_Choices = Dict[Any, Any]

class Option(Protocol):
    start_option_group: bool = ...
    end_option_group: bool = ...
    label: str
    value: Any
    display_text: str

class RelatedField(Field):
    def __init__(
        self,
        many: bool = ...,
        allow_empty: bool = ...,
        queryset: Optional[QuerySet] = ...,
        html_cutoff: Optional[int] = ...,
        html_cutoff_text: str = ...,
        read_only: bool = ...,
        write_only: bool = ...,
        required: bool = ...,
        default: Any = ...,
        initial: Any = ...,
        source: Union[Callable, str] = ...,
        label: Optional[str] = ...,
        help_text: str = ...,
        allow_null: bool = ...,
        validators: Optional[Sequence[_Validator]] = ...,
        error_messages: Optional[Mapping[str, str]] = ...,
        style: Optional[Mapping[str, Any]] = ...,
    ): ...
    queryset: Optional[QuerySet] = ...
    html_cutoff: Optional[int] = ...
    html_cutoff_text: Optional[str] = ...
    @classmethod
    def many_init(cls, *args: Any, **kwargs: Any) -> ManyRelatedField: ...
    def get_queryset(self) -> QuerySet: ...
    def use_pk_only_optimization(self) -> bool: ...
    def get_attribute(self, instance: Any) -> Any: ...
    def get_choices(self, cutoff: Optional[int] = ...) -> _Choices: ...
    @property
    def choices(self) -> _Choices: ...
    @property
    def grouped_choices(self) -> _Choices: ...
    def iter_options(self) -> Iterable[Option]: ...
    def display_value(self, instance: Any) -> str: ...

class StringRelatedField(RelatedField): ...
class PrimaryKeyRelatedField(RelatedField): ...

class HyperlinkedRelatedField(RelatedField):
    lookup_field: str = ...
    lookup_url_kwarg: str = ...
    format: Optional[str] = ...
    view_name: Optional[str] = ...
    def __init__(self, view_name: Optional[str] = ..., **kwargs: Any): ...
    def get_object(self, view_name: str, view_args: Any, view_kwargs: Any) -> Model: ...
    def get_url(self, obj: Model, view_name: str, request: Request, format: str) -> str: ...

class HyperlinkedIdentityField(HyperlinkedRelatedField): ...

class SlugRelatedField(RelatedField):
    slug_field: Optional[str] = ...
    def __init__(self, slug_field: Optional[str] = None, **kwargs: Any): ...

class ManyRelatedField(Field):
    initial: List[object] = ...
    default_empty_html: List[object] = ...
    html_cutoff: Optional[int] = ...
    html_cutoff_text: Optional[str] = ...
    child_relation: RelatedField = ...
    allow_empty: bool = ...
    def __init__(self, child_relation: Optional[RelatedField] = ..., *args: Any, **kwargs: Any) -> None: ...
    def get_choices(self, cutoff: Optional[int] = ...) -> _Choices: ...
    @property
    def choices(self) -> _Choices: ...
    @property
    def grouped_choices(self) -> _Choices: ...
    def iter_options(self) -> Iterable[Option]: ...
