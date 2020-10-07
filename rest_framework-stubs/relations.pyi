from collections import OrderedDict
from typing import (
    Any,
    Callable,
    Dict,
    Generic,
    Iterable,
    List,
    Mapping,
    Optional,
    Protocol,
    Sequence,
    Type,
    TypeVar,
    Union,
)

from django.db.models import Manager, Model, QuerySet
from rest_framework.fields import Field, Option
from rest_framework.request import Request

def method_overridden(method_name: str, klass: type, instance: Model) -> bool: ...

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

_MT = TypeVar("_MT", bound=Model)

class UsesQuerySet(Protocol[_MT]):
    queryset: Optional[Union[QuerySet[_MT], Manager[_MT]]] = ...
    def get_queryset(self) -> QuerySet[_MT]: ...

class RelatedField(Field, UsesQuerySet):
    queryset: Optional[QuerySet] = ...
    html_cutoff: Optional[int] = ...
    html_cutoff_text: Optional[str] = ...
    def __init__(
        self,
        many: bool = ...,
        allow_empty: bool = ...,
        queryset: Optional[Union[QuerySet[_MT], Manager[_MT]]] = ...,
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
    def __new__(cls, *args: Any, **kwargs: Any) -> Union[Type[RelatedField], Type[ManyRelatedField[_MT]]]: ...
    @classmethod
    def many_init(cls, *args: Any, **kwargs: Any) -> ManyRelatedField[_MT]: ...
    def get_queryset(self) -> QuerySet: ...
    def use_pk_only_optimization(self) -> bool: ...
    def get_choices(self, cutoff: Optional[int] = ...) -> OrderedDict: ...
    @property
    def choices(self) -> OrderedDict: ...
    @property
    def grouped_choices(self) -> OrderedDict: ...
    def iter_options(self) -> Iterable[Option]: ...
    def run_validation(self, data: Any = ...): ...
    def get_attribute(self, instance: _MT) -> Any: ...  # type: ignore[override]
    def display_value(self, instance: _MT) -> str: ...

class StringRelatedField(RelatedField):
    def to_representation(self, value: Any) -> str: ...

class PrimaryKeyRelatedField(RelatedField):
    pk_field: Optional[str] = ...
    def __init__(
        self,
        many: bool = ...,
        allow_empty: bool = ...,
        queryset: Optional[Union[QuerySet[_MT], Manager[_MT]]] = ...,
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
    def to_internal_value(self, data: Any) -> _MT: ...
    def to_representation(self, value: _MT) -> Any: ...

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
        queryset: Optional[Union[QuerySet[_MT], Manager[_MT]]] = ...,
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
    def get_object(self, view_name: str, *view_args: Any, **view_kwargs: Any) -> _MT: ...
    def get_url(self, obj: Model, view_name: str, request: Request, format: str) -> Optional[str]: ...
    def to_internal_value(self, data: Any) -> _MT: ...
    def to_representation(self, value: _MT) -> Hyperlink: ...

class HyperlinkedIdentityField(HyperlinkedRelatedField): ...

class SlugRelatedField(RelatedField):
    slug_field: Optional[str] = ...
    def __init__(
        self,
        many: bool = ...,
        allow_empty: bool = ...,
        queryset: Optional[Union[QuerySet[_MT], Manager[_MT]]] = ...,
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
    def to_internal_value(self, data: Any) -> _MT: ...
    def to_representation(self, value: _MT) -> str: ...

class ManyRelatedField(Field, Generic[_MT]):
    initial: List[_MT] = ...
    default_empty_html: List[object] = ...
    html_cutoff: Optional[int] = ...
    html_cutoff_text: Optional[str] = ...
    child_relation: RelatedField = ...
    allow_empty: bool = ...
    def __init__(
        self,
        read_only: bool = ...,
        write_only: bool = ...,
        required: bool = ...,
        default: Any = ...,
        initial: List[_MT] = ...,
        source: Union[Callable, str] = ...,
        label: Optional[str] = ...,
        help_text: Optional[str] = ...,
        style: Optional[Dict[str, str]] = ...,
        error_messages: Optional[Dict[str, str]] = ...,
        validators: Optional[Sequence[Callable]] = ...,
        allow_null: bool = ...,
        child_relation: RelatedField = ...,
    ): ...
    def get_value(self, dictionary: Mapping[Any, Any]) -> List[_MT]: ...
    def to_internal_value(self, data: List[Any]) -> List[_MT]: ...
    def to_representation(self, value: Iterable[_MT]) -> List[Any]: ...
    def get_attribute(self, instance: _MT) -> Any: ...  # type: ignore[override]
    def get_choices(self, cutoff: Optional[int] = ...) -> OrderedDict: ...
    @property
    def choices(self) -> OrderedDict: ...
    @property
    def grouped_choices(self) -> OrderedDict: ...
    def iter_options(self) -> Iterable[Option]: ...
