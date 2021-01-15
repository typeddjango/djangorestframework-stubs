from collections import OrderedDict
from typing import Any, Callable, Dict, Generic, Iterable, List, Mapping, Optional, Sequence, TypeVar, Union

from django.db.models import Manager, Model, QuerySet
from rest_framework.fields import Field, Option
from rest_framework.request import Request
from rest_framework.validators import Validator

def method_overridden(method_name: str, klass: type, instance: Model) -> bool: ...

class ObjectValueError(ValueError): ...
class ObjectTypeError(TypeError): ...

class Hyperlink(str):
    def __new__(cls, url: str, obj: Any) -> Hyperlink: ...
    def __getnewargs__(self): ...
    @property
    def name(self) -> str: ...
    is_hyperlink: bool = ...
    obj: Any

class PKOnlyObject:
    pk: Any = ...
    def __init__(self, pk: Any) -> None: ...

MANY_RELATION_KWARGS: Sequence[str]

_MT = TypeVar("_MT", bound=Model)
_DT = TypeVar("_DT")  # Data Type
_PT = TypeVar("_PT")  # Primitive Type

class RelatedField(Generic[_MT, _DT, _PT], Field[_MT, _DT, _PT, Any]):
    queryset: Optional[Union[QuerySet[_MT], Manager[_MT]]] = ...
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
        validators: Optional[Sequence[Validator[_MT]]] = ...,
        error_messages: Optional[Dict[str, str]] = ...,
        style: Optional[Dict[str, str]] = ...,
    ): ...
    # mypy doesn't accept the typing below, although its accurate to what this class is doing, hence the ignore
    def __new__(cls, *args: Any, **kwargs: Any) -> Union[RelatedField[_MT, _DT, _PT], ManyRelatedField]: ...  # type: ignore
    @classmethod
    def many_init(cls, *args: Any, **kwargs: Any) -> ManyRelatedField: ...
    def get_queryset(self) -> QuerySet[_MT]: ...
    def use_pk_only_optimization(self) -> bool: ...
    def get_choices(self, cutoff: Optional[int] = ...) -> OrderedDict: ...
    @property
    def choices(self) -> OrderedDict: ...
    @property
    def grouped_choices(self) -> OrderedDict: ...
    def iter_options(self) -> Iterable[Option]: ...
    def get_attribute(self, instance: _MT) -> Optional[_PT]: ...  # type: ignore[override]
    def display_value(self, instance: _MT) -> str: ...

class StringRelatedField(RelatedField[_MT, _MT, str]): ...

class PrimaryKeyRelatedField(RelatedField[_MT, _MT, Any]):
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
        validators: Optional[Sequence[Validator[_MT]]] = ...,
        error_messages: Optional[Dict[str, str]] = ...,
        style: Optional[Dict[str, str]] = ...,
        pk_field: Optional[Union[str, Field]] = ...,
    ): ...

class HyperlinkedRelatedField(RelatedField[_MT, str, Hyperlink]):
    reverse: Callable = ...
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
        validators: Optional[Sequence[Validator[_MT]]] = ...,
        error_messages: Optional[Dict[str, str]] = ...,
        style: Optional[Dict[str, str]] = ...,
        view_name: Optional[str] = ...,
        lookup_field: Optional[str] = ...,
        lookup_url_kwarg: Optional[str] = ...,
        format: Optional[str] = ...,
    ): ...
    def get_object(self, view_name: str, *view_args: Any, **view_kwargs: Any) -> _MT: ...
    def get_url(self, obj: Model, view_name: str, request: Request, format: str) -> Optional[str]: ...

class HyperlinkedIdentityField(HyperlinkedRelatedField): ...

class SlugRelatedField(RelatedField[_MT, str, str]):
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
        default: _DT = ...,
        initial: Union[_MT, Callable[[Any], _MT]] = ...,
        source: Union[Callable, str] = ...,
        label: Optional[str] = ...,
        help_text: str = ...,
        allow_null: bool = ...,
        validators: Optional[Sequence[Validator[_MT]]] = ...,
        error_messages: Optional[Dict[str, str]] = ...,
        style: Optional[Dict[str, str]] = ...,
        slug_field: Optional[str] = ...,
    ): ...
    def to_internal_value(self, data: Any) -> _MT: ...
    def to_representation(self, value: _MT) -> str: ...

class ManyRelatedField(Field[Sequence[Any], Sequence[Any], List[Any], Any]):
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
        default: Sequence[Any] = ...,
        initial: Union[Sequence[Any], Callable[[Any], Sequence[Any]]] = ...,
        source: Union[Callable, str] = ...,
        label: Optional[str] = ...,
        help_text: Optional[str] = ...,
        style: Optional[Dict[str, str]] = ...,
        error_messages: Optional[Dict[str, str]] = ...,
        validators: Optional[Sequence[Validator[Sequence[Any]]]] = ...,
        allow_null: bool = ...,
        child_relation: RelatedField = ...,
    ): ...
    def get_value(self, dictionary: Mapping[Any, Any]) -> List[Any]: ...  # type: ignore[override]
    def get_choices(self, cutoff: Optional[int] = ...) -> OrderedDict: ...
    @property
    def choices(self) -> OrderedDict: ...
    @property
    def grouped_choices(self) -> OrderedDict: ...
    def iter_options(self) -> Iterable[Option]: ...
