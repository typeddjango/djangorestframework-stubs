from collections import OrderedDict
from collections.abc import Callable, Iterable, Mapping, Sequence
from typing import Any, Generic, TypeVar

from _typeshed import Self
from django.db.models import Manager, Model, QuerySet
from rest_framework.fields import Field, Option
from rest_framework.request import Request
from rest_framework.validators import Validator

def method_overridden(method_name: str, klass: type, instance: Model) -> bool: ...

class ObjectValueError(ValueError): ...
class ObjectTypeError(TypeError): ...

class Hyperlink(str):
    def __new__(cls: type[Self], url: str, obj: Any) -> Self: ...
    def __getnewargs__(self): ...
    @property
    def name(self) -> str: ...
    is_hyperlink: bool
    obj: Any

class PKOnlyObject:
    pk: Any
    def __init__(self, pk: Any) -> None: ...

MANY_RELATION_KWARGS: Sequence[str]

_MT = TypeVar("_MT", bound=Model)
_DT = TypeVar("_DT")  # Data Type
_PT = TypeVar("_PT")  # Primitive Type

class RelatedField(Generic[_MT, _DT, _PT], Field[_MT, _DT, _PT, Any]):
    queryset: QuerySet[_MT] | Manager[_MT] | None
    html_cutoff: int | None
    html_cutoff_text: str | None
    def __init__(
        self,
        many: bool = ...,
        allow_empty: bool = ...,
        queryset: QuerySet[_MT] | Manager[_MT] | None = ...,
        html_cutoff: int | None = ...,
        html_cutoff_text: str = ...,
        read_only: bool = ...,
        write_only: bool = ...,
        required: bool = ...,
        default: Any = ...,
        initial: Any = ...,
        source: Callable | str = ...,
        label: str | None = ...,
        help_text: str = ...,
        allow_null: bool = ...,
        validators: Sequence[Validator[_MT]] | None = ...,
        error_messages: dict[str, str] | None = ...,
        style: dict[str, str] | None = ...,
    ): ...
    # mypy doesn't accept the typing below, although its accurate to what this class is doing, hence the ignore
    def __new__(cls, *args: Any, **kwargs: Any) -> RelatedField[_MT, _DT, _PT] | ManyRelatedField: ...  # type: ignore
    @classmethod
    def many_init(cls, *args: Any, **kwargs: Any) -> ManyRelatedField: ...
    def get_queryset(self) -> QuerySet[_MT]: ...
    def use_pk_only_optimization(self) -> bool: ...
    def get_choices(self, cutoff: int | None = ...) -> OrderedDict: ...
    @property
    def choices(self) -> OrderedDict: ...
    @property
    def grouped_choices(self) -> OrderedDict: ...
    def iter_options(self) -> Iterable[Option]: ...
    def get_attribute(self, instance: _MT) -> _PT | None: ...  # type: ignore[override]
    def display_value(self, instance: _MT) -> str: ...

class StringRelatedField(RelatedField[_MT, _MT, str]): ...

class PrimaryKeyRelatedField(RelatedField[_MT, _MT, Any]):
    pk_field: str | None
    def __init__(
        self,
        many: bool = ...,
        allow_empty: bool = ...,
        queryset: QuerySet[_MT] | Manager[_MT] | None = ...,
        html_cutoff: int | None = ...,
        html_cutoff_text: str = ...,
        read_only: bool = ...,
        write_only: bool = ...,
        required: bool = ...,
        default: Any = ...,
        initial: Any = ...,
        source: Callable | str = ...,
        label: str | None = ...,
        help_text: str = ...,
        allow_null: bool = ...,
        validators: Sequence[Validator[_MT]] | None = ...,
        error_messages: dict[str, str] | None = ...,
        style: dict[str, str] | None = ...,
        pk_field: str | Field | None = ...,
    ): ...

class HyperlinkedRelatedField(RelatedField[_MT, str, Hyperlink]):
    reverse: Callable
    lookup_field: str
    lookup_url_kwarg: str
    format: str | None
    view_name: str | None
    def __init__(
        self,
        many: bool = ...,
        allow_empty: bool = ...,
        queryset: QuerySet[_MT] | Manager[_MT] | None = ...,
        html_cutoff: int | None = ...,
        html_cutoff_text: str = ...,
        read_only: bool = ...,
        write_only: bool = ...,
        required: bool = ...,
        default: Any = ...,
        initial: Any = ...,
        source: Callable | str = ...,
        label: str | None = ...,
        help_text: str = ...,
        allow_null: bool = ...,
        validators: Sequence[Validator[_MT]] | None = ...,
        error_messages: dict[str, str] | None = ...,
        style: dict[str, str] | None = ...,
        view_name: str | None = ...,
        lookup_field: str | None = ...,
        lookup_url_kwarg: str | None = ...,
        format: str | None = ...,
    ): ...
    def get_object(self, view_name: str, *view_args: Any, **view_kwargs: Any) -> _MT: ...
    def get_url(self, obj: Model, view_name: str, request: Request, format: str) -> str | None: ...

class HyperlinkedIdentityField(HyperlinkedRelatedField): ...

class SlugRelatedField(RelatedField[_MT, str, str]):
    slug_field: str | None
    def __init__(
        self,
        many: bool = ...,
        allow_empty: bool = ...,
        queryset: QuerySet[_MT] | Manager[_MT] | None = ...,
        html_cutoff: int | None = ...,
        html_cutoff_text: str = ...,
        read_only: bool = ...,
        write_only: bool = ...,
        required: bool = ...,
        default: _DT = ...,
        initial: _MT | Callable[[Any], _MT] = ...,
        source: Callable | str = ...,
        label: str | None = ...,
        help_text: str = ...,
        allow_null: bool = ...,
        validators: Sequence[Validator[_MT]] | None = ...,
        error_messages: dict[str, str] | None = ...,
        style: dict[str, str] | None = ...,
        slug_field: str | None = ...,
    ): ...
    def to_internal_value(self, data: Any) -> _MT: ...
    def to_representation(self, value: _MT) -> str: ...

class ManyRelatedField(Field[Sequence[Any], Sequence[Any], list[Any], Any]):
    default_empty_html: list[object]
    html_cutoff: int | None
    html_cutoff_text: str | None
    child_relation: RelatedField
    allow_empty: bool
    def __init__(
        self,
        read_only: bool = ...,
        write_only: bool = ...,
        required: bool = ...,
        default: Sequence[Any] = ...,
        initial: Sequence[Any] | Callable[[Any], Sequence[Any]] = ...,
        source: Callable | str = ...,
        label: str | None = ...,
        help_text: str | None = ...,
        style: dict[str, str] | None = ...,
        error_messages: dict[str, str] | None = ...,
        validators: Sequence[Validator[Sequence[Any]]] | None = ...,
        allow_null: bool = ...,
        allow_empty: bool = ...,
        child_relation: RelatedField = ...,
    ): ...
    def get_value(self, dictionary: Mapping[Any, Any]) -> list[Any]: ...  # type: ignore[override]
    def get_choices(self, cutoff: int | None = ...) -> OrderedDict: ...
    @property
    def choices(self) -> OrderedDict: ...
    @property
    def grouped_choices(self) -> OrderedDict: ...
    def iter_options(self) -> Iterable[Option]: ...
