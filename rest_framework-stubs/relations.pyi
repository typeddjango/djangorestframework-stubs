from typing import Any, Callable, Dict, Iterable, List, Optional, Protocol, Sequence, Union

from django.db.models import Model
from django.db.models.query import QuerySet
from rest_framework.fields import Field
from rest_framework.request import Request

def method_overridden(method_name: str, klass: type, instance: Model) -> bool: ...

_Choices = Dict[Any, Any]

class Option(Protocol):
    start_option_group: bool = ...
    end_option_group: bool = ...
    label: str
    value: Any
    display_text: str

class ObjectValueError(ValueError): ...
class ObjectTypeError(TypeError): ...

class Hyperlink(str):
    def __new__(cls, url: str, obj: Any) -> Hyperlink: ...
    def __getnewargs__(self): ...
    @property
    def name(self) -> str: ...
    is_hyperlink: bool = ...

class PKOnlyObject:
    pk: Any = ...
    def __init__(self, pk: Any) -> None: ...

MANY_RELATION_KWARGS: Sequence[str]

class RelatedField(Field):
    queryset: Optional[QuerySet] = ...
    html_cutoff: Optional[int] = ...
    html_cutoff_text: Optional[str] = ...
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
        validators: Optional[Sequence[Callable]] = ...,
        error_messages: Optional[Dict[str, str]] = ...,
        style: Optional[Dict[str, str]] = ...,
    ): ...
    @classmethod
    def many_init(cls, *args: Any, **kwargs: Any) -> ManyRelatedField: ...
    def get_queryset(self) -> QuerySet: ...
    def use_pk_only_optimization(self) -> bool: ...
    def get_attribute(self, instance: Model) -> Any: ...
    def get_choices(self, cutoff: Optional[int] = ...) -> _Choices: ...
    @property
    def choices(self) -> _Choices: ...
    @property
    def grouped_choices(self) -> _Choices: ...
    def iter_options(self) -> Iterable[Option]: ...
    def display_value(self, instance: Model) -> str: ...
    def run_validation(self, data: Any = ...): ...

class StringRelatedField(RelatedField): ...

class PrimaryKeyRelatedField(RelatedField):
    pk_field: Optional[str] = ...
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
        validators: Optional[Sequence[Callable]] = ...,
        error_messages: Optional[Dict[str, str]] = ...,
        style: Optional[Dict[str, str]] = ...,
        pk_field: Optional[Union[str, Field]] = ...,
    ): ...

class HyperlinkedRelatedField(RelatedField):
    reverse: Any = ...
    lookup_field: str = ...
    lookup_url_kwarg: str = ...
    format: Optional[str] = ...
    view_name: Optional[str] = ...
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
        validators: Optional[Sequence[Callable]] = ...,
        error_messages: Optional[Dict[str, str]] = ...,
        style: Optional[Dict[str, str]] = ...,
        view_name: Optional[str] = ...,
        lookup_field: Optional[str] = ...,
        lookup_url_kwarg: Optional[str] = ...,
        format: Optional[str] = ...,
    ): ...
    def get_object(self, view_name: str, *view_args: Any, **view_kwargs: Any) -> Model: ...
    def get_url(self, obj: Model, view_name: str, request: Request, format: str) -> Optional[str]: ...

class HyperlinkedIdentityField(HyperlinkedRelatedField): ...

class SlugRelatedField(RelatedField):
    slug_field: Optional[str] = ...
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
        validators: Optional[Sequence[Callable]] = ...,
        error_messages: Optional[Dict[str, str]] = ...,
        style: Optional[Dict[str, str]] = ...,
        slug_field: Optional[str] = ...,
    ): ...

class ManyRelatedField(Field):
    initial: List[object] = ...
    default_empty_html: List[object] = ...
    html_cutoff: Optional[int] = ...
    html_cutoff_text: Optional[str] = ...
    child_relation: Any = ...
    allow_empty: Any = ...
    def __init__(
        self,
        read_only: bool = ...,
        write_only: bool = ...,
        required: bool = ...,
        default: Any = ...,
        initial: Any = ...,
        source: Union[Callable, str] = ...,
        label: Optional[str] = ...,
        help_text: Optional[str] = ...,
        style: Optional[Dict[str, str]] = ...,
        error_messages: Optional[Dict[str, str]] = ...,
        validators: Optional[Sequence[Callable]] = ...,
        allow_null: bool = ...,
        child_relation: Optional[RelatedField] = ...,
    ): ...
    def get_choices(self, cutoff: Optional[int] = ...) -> _Choices: ...
    def get_value(self, dictionary: dict): ...
    def get_attribute(self, instance: Model) -> Any: ...
    @property
    def choices(self) -> _Choices: ...
    @property
    def grouped_choices(self) -> _Choices: ...
    def iter_options(self) -> Iterable[Option]: ...
