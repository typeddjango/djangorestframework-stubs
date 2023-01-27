import datetime
import uuid
from collections import OrderedDict
from collections.abc import Callable, Generator, Iterable, Mapping, MutableMapping, Sequence
from decimal import Decimal
from enum import Enum
from json import JSONDecoder, JSONEncoder
from re import Pattern
from typing import Any, Generic, NoReturn, Protocol, TypeVar

from _typeshed import Self
from django.core.files.base import File
from django.db import models
from django.forms import ImageField as DjangoImageField  # noqa: F401
from django_stubs_ext import StrOrPromise
from rest_framework.serializers import BaseSerializer
from rest_framework.validators import Validator
from typing_extensions import Final, TypeAlias

class _Empty(Enum):
    sentinel = 0  # noqa: Y015

empty: Final = _Empty.sentinel

class BuiltinSignatureError(Exception): ...

class CreateOnlyDefault:
    requires_context: bool
    default: Any
    def __init__(self, default: Any) -> None: ...
    def __call__(self, serializer_field: Field): ...

class CurrentUserDefault:
    requires_context: bool
    def __call__(self, serializer_field: Field): ...

class SkipField(Exception): ...

class Option(Protocol):
    start_option_group: bool
    end_option_group: bool
    label: StrOrPromise
    value: str
    display_text: StrOrPromise

def is_simple_callable(obj: Callable) -> bool: ...
def get_attribute(instance: Any, attrs: list[str] | None) -> Any: ...
def set_value(dictionary: MutableMapping[str, Any], keys: Sequence[str], value: Any) -> None: ...
def to_choices_dict(choices: Iterable[Any]) -> OrderedDict: ...
def flatten_choices_dict(choices: dict[Any, Any]) -> OrderedDict: ...
def iter_options(
    grouped_choices: OrderedDict, cutoff: int | None = ..., cutoff_text: StrOrPromise | None = ...
) -> Generator[Option, None, None]: ...
def get_error_detail(exc_info: Any) -> Any: ...

REGEX_TYPE: Pattern
NOT_READ_ONLY_WRITE_ONLY: str
NOT_READ_ONLY_REQUIRED: str
NOT_REQUIRED_DEFAULT: str
USE_READONLYFIELD: str
MISSING_ERROR_MESSAGE: str

_IN = TypeVar("_IN")  # Instance Type
_VT = TypeVar("_VT")  # Value Type
_DT = TypeVar("_DT")  # Data Type
_RP = TypeVar("_RP")  # Representation Type

class SupportsToPython(Protocol):
    def to_python(self, value: Any) -> Any: ...

_DefaultInitial: TypeAlias = _VT | Callable[[], _VT] | None | _Empty

class Field(Generic[_VT, _DT, _RP, _IN]):
    allow_null: bool
    default: _VT | None
    default_empty_html: Any
    default_error_messages: dict[str, StrOrPromise]
    default_validators: list[Validator[_VT]]
    error_messages: dict[str, StrOrPromise]
    field_name: str | None
    help_text: StrOrPromise | None
    initial: _VT | Callable[[], _VT] | None
    label: StrOrPromise | None
    parent: BaseSerializer
    read_only: bool
    required: bool
    source: Callable | str | None
    source_attrs: list[str]
    style: dict[str, Any]
    write_only: bool
    def __init__(
        self,
        read_only: bool = ...,
        write_only: bool = ...,
        required: bool = ...,
        default: _DefaultInitial[_VT] = ...,
        initial: _DefaultInitial[_VT] = ...,
        source: str = ...,
        label: StrOrPromise = ...,
        help_text: StrOrPromise = ...,
        style: dict[str, Any] = ...,
        error_messages: dict[str, StrOrPromise] = ...,
        validators: Sequence[Validator[_VT]] | None = ...,
        allow_null: bool = ...,
    ): ...
    def bind(self, field_name: str, parent: BaseSerializer) -> None: ...
    @property
    def validators(self) -> list[Validator[_VT]]: ...
    @validators.setter
    def validators(self, validators: list[Validator[_VT]]) -> None: ...
    def get_validators(self) -> list[Validator[_VT]]: ...
    def get_initial(self) -> _VT | None: ...
    def get_value(self, dictionary: Mapping[Any, Any]) -> Any: ...
    def get_attribute(self, instance: _IN) -> _RP | None: ...
    def get_default(self) -> _VT | None: ...
    def validate_empty_values(self, data: Any) -> tuple[bool, Any]: ...
    def run_validation(self, data: Any = ...) -> Any: ...
    def run_validators(self, value: Any) -> None: ...
    def to_internal_value(self, data: _DT) -> _VT: ...
    def to_representation(self, value: _VT) -> _RP: ...
    def fail(self, key: str, **kwargs: Any) -> NoReturn: ...
    @property
    def root(self) -> BaseSerializer: ...
    @property
    def context(self) -> dict[str, Any]: ...
    def __new__(cls: type[Self], *args: Any, **kwargs: Any) -> Self: ...
    def __deepcopy__(self, memo: Mapping[Any, Any]) -> Field: ...

class BooleanField(
    Field[
        bool,
        str | bool | int,
        bool,
        Any,
    ]
):
    TRUE_VALUES: set[str | bool | int]
    FALSE_VALUES: set[str | bool | int | float]
    NULL_VALUES: set[str | None]

class NullBooleanField(
    Field[
        bool | None,
        str | bool | int | None,
        bool,
        Any,
    ]
):
    TRUE_VALUES: set[str | bool | int]
    FALSE_VALUES: set[str | bool | int | float]
    NULL_VALUES: set[str | None]

class CharField(Field[str, str, str, Any]):
    allow_blank: bool
    trim_whitespace: bool
    max_length: int | None
    min_length: int | None
    def __init__(
        self,
        *,
        read_only: bool = ...,
        write_only: bool = ...,
        required: bool = ...,
        default: _DefaultInitial[StrOrPromise] = ...,
        initial: _DefaultInitial[str] = ...,
        source: str = ...,
        label: StrOrPromise = ...,
        help_text: StrOrPromise = ...,
        style: dict[str, Any] = ...,
        error_messages: dict[str, StrOrPromise] = ...,
        validators: Sequence[Validator[str]] | None = ...,
        allow_null: bool = ...,
        allow_blank: bool = ...,
        trim_whitespace: bool = ...,
        max_length: int = ...,
        min_length: int | None = ...,
    ): ...

class EmailField(CharField): ...

class RegexField(CharField):
    def __init__(
        self,
        regex: str | Pattern,
        *,
        read_only: bool = ...,
        write_only: bool = ...,
        required: bool = ...,
        default: _DefaultInitial[StrOrPromise] = ...,
        initial: _DefaultInitial[str] = ...,
        source: str = ...,
        label: StrOrPromise = ...,
        help_text: StrOrPromise = ...,
        style: dict[str, Any] = ...,
        error_messages: dict[str, StrOrPromise] = ...,
        validators: Sequence[Validator[str]] | None = ...,
        allow_null: bool = ...,
        allow_blank: bool = ...,
        trim_whitespace: bool = ...,
        max_length: int = ...,
        min_length: int | None = ...,
    ): ...

class SlugField(CharField):
    allow_unicode: bool
    def __init__(
        self,
        allow_unicode: bool = ...,
        *,
        read_only: bool = ...,
        write_only: bool = ...,
        required: bool = ...,
        default: _DefaultInitial[StrOrPromise] = ...,
        initial: _DefaultInitial[str] = ...,
        source: str = ...,
        label: StrOrPromise = ...,
        help_text: StrOrPromise = ...,
        style: dict[str, Any] = ...,
        error_messages: dict[str, StrOrPromise] = ...,
        validators: Sequence[Validator[str]] | None = ...,
        allow_null: bool = ...,
        allow_blank: bool = ...,
        trim_whitespace: bool = ...,
        max_length: int = ...,
        min_length: int | None = ...,
    ): ...

class URLField(CharField): ...

class UUIDField(Field[uuid.UUID, uuid.UUID | str | int, str, Any]):
    valid_formats: Sequence[str]
    uuid_format: str
    def __init__(
        self,
        *,
        format: str | None = ...,
        read_only: bool = ...,
        write_only: bool = ...,
        required: bool = ...,
        default: _DefaultInitial[uuid.UUID] = ...,
        initial: _DefaultInitial[uuid.UUID] = ...,
        source: str = ...,
        label: StrOrPromise = ...,
        help_text: StrOrPromise = ...,
        style: dict[str, Any] = ...,
        error_messages: dict[str, StrOrPromise] = ...,
        validators: Sequence[Validator[uuid.UUID]] | None = ...,
        allow_null: bool = ...,
    ): ...

class IPAddressField(CharField):
    protocol: str
    unpack_ipv4: bool
    def __init__(
        self,
        protocol: str = ...,
        *,
        read_only: bool = ...,
        write_only: bool = ...,
        required: bool = ...,
        default: _DefaultInitial[str] = ...,
        initial: _DefaultInitial[str] = ...,
        source: str = ...,
        label: StrOrPromise = ...,
        help_text: StrOrPromise = ...,
        style: dict[str, Any] = ...,
        error_messages: dict[str, StrOrPromise] = ...,
        validators: Sequence[Validator[str]] | None = ...,
        allow_null: bool = ...,
        allow_blank: bool = ...,
        trim_whitespace: bool = ...,
        max_length: int = ...,
        min_length: int | None = ...,
    ): ...

class IntegerField(Field[int, float | int | str, int, Any]):
    MAX_STRING_LENGTH: int
    re_decimal: Pattern
    max_value: int | None
    min_value: int | None
    def __init__(
        self,
        *,
        max_value: int = ...,
        min_value: int = ...,
        read_only: bool = ...,
        write_only: bool = ...,
        required: bool = ...,
        default: _DefaultInitial[int] = ...,
        initial: _DefaultInitial[int] = ...,
        source: str = ...,
        label: StrOrPromise = ...,
        help_text: StrOrPromise = ...,
        style: dict[str, Any] = ...,
        error_messages: dict[str, StrOrPromise] = ...,
        validators: Sequence[Validator[int]] | None = ...,
        allow_null: bool = ...,
    ): ...

class FloatField(Field[float, float | int | str, str, Any]):
    MAX_STRING_LENGTH: int
    re_decimal: Pattern
    max_value: float | None
    min_value: float | None
    def __init__(
        self,
        *,
        max_value: float = ...,
        min_value: float = ...,
        read_only: bool = ...,
        write_only: bool = ...,
        required: bool = ...,
        default: _DefaultInitial[float] = ...,
        initial: _DefaultInitial[float] = ...,
        source: str = ...,
        label: StrOrPromise = ...,
        help_text: StrOrPromise = ...,
        style: dict[str, Any] = ...,
        error_messages: dict[str, StrOrPromise] = ...,
        validators: Sequence[Validator[float]] | None = ...,
        allow_null: bool = ...,
    ): ...

class DecimalField(Field[Decimal, int | float | str | Decimal, str, Any]):
    MAX_STRING_LENGTH: int
    max_digits: int | None
    decimal_places: int | None
    coerce_to_string: bool | None
    max_value: Decimal | int | float | None
    min_value: Decimal | int | float | None
    localize: bool
    rounding: str | None
    max_whole_digits = int | None  # noqa: Y026
    def __init__(
        self,
        max_digits: int | None,
        decimal_places: int | None,
        coerce_to_string: bool = ...,
        max_value: Decimal | int | float = ...,
        min_value: Decimal | int | float = ...,
        localize: bool = ...,
        rounding: str | None = ...,
        normalize_output: bool = ...,
        *,
        read_only: bool = ...,
        write_only: bool = ...,
        required: bool = ...,
        default: _DefaultInitial[Decimal] = ...,
        initial: _DefaultInitial[Decimal] = ...,
        source: str = ...,
        label: StrOrPromise = ...,
        help_text: StrOrPromise = ...,
        style: dict[str, Any] = ...,
        error_messages: dict[str, StrOrPromise] = ...,
        validators: Sequence[Validator[Decimal]] | None = ...,
        allow_null: bool = ...,
    ): ...
    def validate_precision(self, value: Decimal) -> Decimal: ...
    def quantize(self, value: Decimal) -> Decimal: ...

class DateTimeField(Field[datetime.datetime, datetime.datetime | str, str, Any]):
    datetime_parser: Callable[[str, str], datetime.datetime]
    format: str | None
    input_formats: Sequence[str]
    timezone: datetime.tzinfo
    def __init__(
        self,
        format: str | None = ...,
        input_formats: Sequence[str] = ...,
        default_timezone: datetime.tzinfo | None = ...,
        read_only: bool = ...,
        write_only: bool = ...,
        required: bool = ...,
        default: _DefaultInitial[datetime.datetime] = ...,
        initial: _DefaultInitial[datetime.datetime] = ...,
        source: str = ...,
        label: StrOrPromise = ...,
        help_text: StrOrPromise = ...,
        style: dict[str, Any] = ...,
        error_messages: dict[str, StrOrPromise] = ...,
        validators: Sequence[Validator[datetime.datetime]] | None = ...,
        allow_null: bool = ...,
    ): ...
    def enforce_timezone(self, value: datetime.datetime) -> datetime.datetime: ...
    def default_timezone(self) -> str | None: ...

class DateField(Field[datetime.date, datetime.date | str, str, Any]):
    datetime_parser: Callable[[str, str], datetime.datetime]
    format: str | None
    input_formats: Sequence[str]
    def __init__(
        self,
        format: str | None = ...,
        input_formats: Sequence[str] = ...,
        read_only: bool = ...,
        write_only: bool = ...,
        required: bool = ...,
        default: _DefaultInitial[datetime.date] = ...,
        initial: _DefaultInitial[datetime.date] = ...,
        source: str = ...,
        label: StrOrPromise = ...,
        help_text: StrOrPromise = ...,
        style: dict[str, Any] = ...,
        error_messages: dict[str, StrOrPromise] = ...,
        validators: Sequence[Validator[datetime.date]] | None = ...,
        allow_null: bool = ...,
    ): ...

class TimeField(Field[datetime.time, datetime.time | str, str, Any]):
    datetime_parser: Callable[[str, str], datetime.datetime]
    format: str | None
    input_formats: Sequence[str]
    def __init__(
        self,
        format: str | None = ...,
        input_formats: Sequence[str] = ...,
        read_only: bool = ...,
        write_only: bool = ...,
        required: bool = ...,
        default: _DefaultInitial[datetime.time] = ...,
        initial: _DefaultInitial[datetime.time] = ...,
        source: str = ...,
        label: StrOrPromise = ...,
        help_text: StrOrPromise = ...,
        style: dict[str, Any] = ...,
        error_messages: dict[str, StrOrPromise] = ...,
        validators: Sequence[Validator[datetime.time]] | None = ...,
        allow_null: bool = ...,
    ): ...

class DurationField(Field[datetime.timedelta, datetime.timedelta | str, str, Any]):
    max_value: datetime.timedelta | None
    min_value: datetime.timedelta | None
    def __init__(
        self,
        *,
        max_value: datetime.timedelta | int | float = ...,
        min_value: datetime.timedelta | int | float = ...,
        read_only: bool = ...,
        write_only: bool = ...,
        required: bool = ...,
        default: _DefaultInitial[datetime.timedelta] = ...,
        initial: _DefaultInitial[datetime.timedelta] = ...,
        source: str = ...,
        label: StrOrPromise = ...,
        help_text: StrOrPromise = ...,
        style: dict[str, Any] = ...,
        error_messages: dict[str, StrOrPromise] = ...,
        validators: Sequence[Validator[datetime.timedelta]] | None = ...,
        allow_null: bool = ...,
    ): ...

class ChoiceField(Field[str, str | int | tuple[str | int, str | int | tuple], str, Any]):
    html_cutoff: int | None
    html_cutoff_text: StrOrPromise | None
    allow_blank: bool
    grouped_choices: OrderedDict
    choice_strings_to_values: dict[str, Any]
    _choices: OrderedDict
    def __init__(
        self,
        choices: Iterable[Any],
        *,
        read_only: bool = ...,
        write_only: bool = ...,
        required: bool = ...,
        default: _DefaultInitial[StrOrPromise | int] = ...,
        initial: _DefaultInitial[str | int] = ...,
        source: str = ...,
        label: StrOrPromise = ...,
        help_text: StrOrPromise = ...,
        style: dict[str, Any] = ...,
        error_messages: dict[str, StrOrPromise] = ...,
        validators: Sequence[Validator[Any]] | None = ...,
        allow_null: bool = ...,
        html_cutoff: int = ...,
        html_cutoff_text: StrOrPromise = ...,
        allow_blank: bool = ...,
    ): ...
    def iter_options(self) -> Iterable[Option]: ...
    def _get_choices(self) -> dict[Any, Any]: ...
    def _set_choices(self, choices: Iterable[Any]) -> None: ...
    choices = property(_get_choices, _set_choices)

class MultipleChoiceField(
    ChoiceField,
    Field[
        str,
        Sequence[str | int | tuple[str | int, str | int]],
        Sequence[str | tuple[str | int, str | int]],
        Any,
    ],
):
    allow_empty: bool
    def __init__(
        self,
        choices: Iterable[Any],
        read_only: bool = ...,
        write_only: bool = ...,
        required: bool = ...,
        default: _DefaultInitial[set[str | int] | set[str] | set[int]] = ...,
        initial: _DefaultInitial[set[StrOrPromise | int] | set[StrOrPromise] | set[int]] = ...,
        source: str = ...,
        label: StrOrPromise = ...,
        help_text: StrOrPromise = ...,
        style: dict[str, Any] = ...,
        error_messages: dict[str, StrOrPromise] = ...,
        validators: Sequence[Validator[Any]] | None = ...,
        allow_null: bool = ...,
        html_cutoff: int = ...,
        html_cutoff_text: StrOrPromise = ...,
        allow_blank: bool = ...,
        allow_empty: bool = ...,
    ): ...

class FilePathField(ChoiceField):
    def __init__(
        self,
        path: str,
        match: str = ...,
        recursive: bool = ...,
        allow_files: bool = ...,
        allow_folders: bool = ...,
        required: bool = ...,
        read_only: bool = ...,
        write_only: bool = ...,
        default: _DefaultInitial[str] = ...,
        initial: _DefaultInitial[str] = ...,
        source: str = ...,
        label: StrOrPromise = ...,
        help_text: StrOrPromise = ...,
        style: dict[str, Any] = ...,
        error_messages: dict[str, StrOrPromise] = ...,
        validators: Sequence[Validator[Any]] | None = ...,
        allow_null: bool = ...,
        html_cutoff: int = ...,
        html_cutoff_text: StrOrPromise = ...,
        allow_blank: bool = ...,
    ): ...

class FileField(Field[File, File, str | None, Any]):  # this field can return None without raising!
    max_length: int
    allow_empty_file: bool
    use_url: bool
    def __init__(
        self,
        *,
        read_only: bool = ...,
        write_only: bool = ...,
        required: bool = ...,
        default: _DefaultInitial[File] = ...,
        initial: _DefaultInitial[File] = ...,
        source: str = ...,
        label: StrOrPromise = ...,
        help_text: StrOrPromise = ...,
        style: dict[str, Any] = ...,
        error_messages: dict[str, StrOrPromise] = ...,
        validators: Sequence[Validator[File]] | None = ...,
        allow_null: bool = ...,
        max_length: int = ...,
        allow_empty_file: bool = ...,
        use_url: bool = ...,
    ): ...

class ImageField(FileField):
    _DjangoImageField: SupportsToPython
    def __init__(
        self,
        *,
        read_only: bool = ...,
        write_only: bool = ...,
        required: bool = ...,
        default: _DefaultInitial[File] = ...,
        initial: _DefaultInitial[File] = ...,
        source: str = ...,
        label: StrOrPromise = ...,
        help_text: StrOrPromise = ...,
        style: dict[str, Any] = ...,
        error_messages: dict[str, StrOrPromise] = ...,
        validators: Sequence[Validator[File]] | None = ...,
        allow_null: bool = ...,
        max_length: int = ...,
        allow_empty_file: bool = ...,
        use_url: bool = ...,
        _DjangoImageField: type[SupportsToPython] = ...,
    ): ...

class _UnvalidatedField(Field): ...

class ListField(Field[list[Any], list[Any], list[Any], Any]):
    child: Field
    allow_empty: bool
    max_length: int | None
    min_length: int | None
    def __init__(
        self,
        read_only: bool = ...,
        write_only: bool = ...,
        required: bool = ...,
        default: _DefaultInitial[list[Any]] = ...,
        initial: _DefaultInitial[list[Any]] = ...,
        source: str = ...,
        label: StrOrPromise = ...,
        help_text: StrOrPromise = ...,
        style: dict[str, Any] = ...,
        error_messages: dict[str, StrOrPromise] = ...,
        validators: Sequence[Validator[list[Any]]] | None = ...,
        allow_null: bool = ...,
        *,
        child: Field = ...,
        allow_empty: bool = ...,
        max_length: int = ...,
        min_length: int = ...,
    ): ...
    def run_child_validation(self, data: list[Mapping[Any, Any]]) -> Any: ...

class DictField(Field[dict[Any, Any], dict[Any, Any], dict[Any, Any], Any]):
    child: Field
    allow_empty: bool
    def __init__(
        self,
        read_only: bool = ...,
        write_only: bool = ...,
        required: bool = ...,
        default: _DefaultInitial[dict[Any, Any]] = ...,
        initial: _DefaultInitial[dict[Any, Any]] = ...,
        source: str = ...,
        label: StrOrPromise = ...,
        help_text: StrOrPromise = ...,
        style: dict[str, Any] = ...,
        error_messages: dict[str, StrOrPromise] = ...,
        validators: Sequence[Validator[dict[Any, Any]]] | None = ...,
        allow_null: bool = ...,
        *,
        child: Field = ...,
        allow_empty: bool = ...,
    ): ...
    def run_child_validation(self, data: Any) -> Any: ...

class HStoreField(DictField):
    child: CharField

class JSONField(Field[dict[str, Any] | list[dict[str, Any]], dict[str, Any] | list[dict[str, Any]], str, Any]):
    binary: bool
    encoder: type[JSONEncoder] | None
    decoder: type[JSONDecoder] | None
    def __init__(
        self,
        read_only: bool = ...,
        write_only: bool = ...,
        required: bool = ...,
        default: _DefaultInitial[Mapping[Any, Any]] = ...,
        initial: _DefaultInitial[Mapping[Any, Any]] = ...,
        source: str = ...,
        label: StrOrPromise = ...,
        help_text: StrOrPromise = ...,
        style: dict[str, Any] = ...,
        error_messages: dict[str, StrOrPromise] = ...,
        validators: Sequence[Validator[Any]] | None = ...,
        allow_null: bool = ...,
        *,
        binary: bool = ...,
        encoder: type[JSONEncoder] | None = ...,
        decoder: type[JSONDecoder] | None = ...,
    ): ...

class ReadOnlyField(Field): ...
class HiddenField(Field): ...

class SerializerMethodField(Field):
    method_name: str
    def __init__(
        self,
        method_name: str | None = ...,
        *,
        read_only: bool = ...,
        write_only: bool = ...,
        required: bool = ...,
        default: Any = ...,
        initial: Any = ...,
        source: str = ...,
        label: StrOrPromise = ...,
        help_text: StrOrPromise = ...,
        style: dict[str, Any] = ...,
        error_messages: dict[str, StrOrPromise] = ...,
        validators: Sequence[Validator[Any]] | None = ...,
        allow_null: bool = ...,
    ): ...

class ModelField(Field):
    model_field: models.Field
    max_length: int
    def __init__(
        self,
        model_field: models.Field,
        *,
        read_only: bool = ...,
        write_only: bool = ...,
        required: bool = ...,
        default: Any = ...,
        initial: Any = ...,
        source: str = ...,
        label: StrOrPromise = ...,
        help_text: StrOrPromise = ...,
        style: dict[str, Any] = ...,
        error_messages: dict[str, StrOrPromise] = ...,
        validators: Sequence[Validator[Any]] | None = ...,
        allow_null: bool = ...,
        max_length: int = ...,
    ): ...
