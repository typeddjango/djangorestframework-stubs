import datetime
import uuid
from collections.abc import Callable, Generator, Iterable, Mapping, Sequence
from decimal import Decimal
from enum import Enum
from json import JSONDecoder, JSONEncoder
from re import Pattern
from typing import Any, ClassVar, Final, Generic, NoReturn, Protocol, TypeAlias, TypeVar

from django.core.exceptions import ValidationError as DjangoValidationError
from django.core.files.base import File
from django.db import models
from django.forms import ImageField as DjangoImageField  # noqa: F401
from django_stubs_ext import StrOrPromise
from rest_framework.exceptions import ErrorDetail
from rest_framework.serializers import BaseSerializer
from rest_framework.validators import Validator
from typing_extensions import Self, override

class _Empty(Enum):
    sentinel = 0

# DISREPANCY: `empty` hinted as enum, to work correctly in unions:
# https://github.com/typeddjango/djangorestframework-stubs/issues/42
empty: Final = _Empty.sentinel

class BuiltinSignatureError(Exception): ...

def is_simple_callable(obj: Callable[..., Any]) -> bool: ...
def get_attribute(instance: Any, attrs: list[str] | None) -> Any: ...
def to_choices_dict(choices: Iterable[Any]) -> dict: ...
def flatten_choices_dict(choices: dict[Any, Any]) -> dict: ...
def iter_options(
    grouped_choices: dict, cutoff: int | None = None, cutoff_text: StrOrPromise | None = None
) -> Generator[Option]: ...
def get_error_detail(
    exc_info: DjangoValidationError,
) -> list[ErrorDetail] | dict[str, list[ErrorDetail]]: ...

class CreateOnlyDefault:
    requires_context: bool
    default: Any
    def __init__(self, default: Any) -> None: ...
    def __call__(self, serializer_field: Field) -> Any: ...

class CurrentUserDefault:
    requires_context: bool
    def __call__(self, serializer_field: Field) -> Any: ...

class SkipField(Exception): ...

class Option(Protocol):
    start_option_group: bool
    end_option_group: bool
    label: StrOrPromise
    value: str
    display_text: StrOrPromise

REGEX_TYPE: type[Pattern[str]]
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
    default_empty_html: Any  # Any: empty sentinel or field default value
    default_error_messages: ClassVar[dict[str, StrOrPromise]]
    default_validators: Sequence[Validator[_VT]]
    error_messages: dict[str, StrOrPromise]
    field_name: str | None
    help_text: StrOrPromise | None
    initial: _VT | Callable[[], _VT] | None
    label: StrOrPromise | None
    parent: BaseSerializer
    read_only: bool
    required: bool
    source: str | None
    source_attrs: list[str]
    style: dict[str, Any]
    write_only: bool
    def __init__(
        self,
        *,
        read_only: bool = False,
        write_only: bool = False,
        required: bool | None = None,
        default: _DefaultInitial[_VT] = ...,
        initial: _DefaultInitial[_VT] = ...,
        source: str | None = None,
        label: StrOrPromise | None = None,
        help_text: StrOrPromise | None = None,
        style: dict[str, Any] | None = None,
        error_messages: dict[str, StrOrPromise] | None = None,
        validators: Sequence[Validator[_VT]] | None = None,
        allow_null: bool = False,
    ) -> None: ...
    @classmethod
    def __class_getitem__(cls, *args: Any, **kwargs: Any) -> type[Self]: ...
    def bind(self, field_name: str, parent: BaseSerializer) -> None: ...
    @property
    def validators(self) -> list[Validator[_VT]]: ...
    @validators.setter
    def validators(self, validators: list[Validator[_VT]]) -> None: ...
    def get_validators(self) -> list[Validator[_VT]]: ...
    def get_initial(self) -> _VT | None: ...
    def get_value(self, dictionary: Mapping[str, Any]) -> Any: ...
    def get_attribute(self, instance: _IN) -> _VT | None: ...
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
    def context(self) -> Mapping[str, Any]: ...
    def __new__(cls, *args: Any, **kwargs: Any) -> Self: ...
    def __deepcopy__(self, memo: dict[int, Any]) -> Self: ...

class BooleanField(
    Field[
        bool,
        str | bool | int,
        bool,
        Any,
    ]
):
    initial: bool
    TRUE_VALUES: set[str | bool | int]
    FALSE_VALUES: set[str | bool | int | float]
    NULL_VALUES: set[str | None]

class CharField(Field[str, str, str, Any]):
    initial: str
    allow_blank: bool
    trim_whitespace: bool
    max_length: int | None
    min_length: int | None
    def __init__(
        self,
        *,
        read_only: bool = False,
        write_only: bool = False,
        required: bool | None = None,
        default: _DefaultInitial[StrOrPromise] = ...,
        initial: _DefaultInitial[str] = ...,
        source: str | None = None,
        label: StrOrPromise | None = None,
        help_text: StrOrPromise | None = None,
        style: dict[str, Any] | None = None,
        error_messages: dict[str, StrOrPromise] | None = None,
        validators: Sequence[Validator[str]] | None = None,
        allow_null: bool = False,
        allow_blank: bool = False,
        trim_whitespace: bool = True,
        max_length: int | None = None,
        min_length: int | None = None,
    ) -> None: ...

class EmailField(CharField): ...

class RegexField(CharField):
    def __init__(
        self,
        regex: str | Pattern[str],
        *,
        read_only: bool = False,
        write_only: bool = False,
        required: bool | None = None,
        default: _DefaultInitial[StrOrPromise] = ...,
        initial: _DefaultInitial[str] = ...,
        source: str | None = None,
        label: StrOrPromise | None = None,
        help_text: StrOrPromise | None = None,
        style: dict[str, Any] | None = None,
        error_messages: dict[str, StrOrPromise] | None = None,
        validators: Sequence[Validator[str]] | None = None,
        allow_null: bool = False,
        allow_blank: bool = False,
        trim_whitespace: bool = True,
        max_length: int | None = None,
        min_length: int | None = None,
    ) -> None: ...

class SlugField(CharField):
    allow_unicode: bool
    def __init__(
        self,
        allow_unicode: bool = False,
        *,
        read_only: bool = False,
        write_only: bool = False,
        required: bool | None = None,
        default: _DefaultInitial[StrOrPromise] = ...,
        initial: _DefaultInitial[str] = ...,
        source: str | None = None,
        label: StrOrPromise | None = None,
        help_text: StrOrPromise | None = None,
        style: dict[str, Any] | None = None,
        error_messages: dict[str, StrOrPromise] | None = None,
        validators: Sequence[Validator[str]] | None = None,
        allow_null: bool = False,
        allow_blank: bool = False,
        trim_whitespace: bool = True,
        max_length: int | None = None,
        min_length: int | None = None,
    ) -> None: ...

class URLField(CharField): ...

class UUIDField(Field[uuid.UUID, uuid.UUID | str | int, str, Any]):
    valid_formats: Sequence[str]
    uuid_format: str
    def __init__(
        self,
        *,
        format: str | None = None,
        read_only: bool = False,
        write_only: bool = False,
        required: bool | None = None,
        default: _DefaultInitial[uuid.UUID] = ...,
        initial: _DefaultInitial[uuid.UUID] = ...,
        source: str | None = None,
        label: StrOrPromise | None = None,
        help_text: StrOrPromise | None = None,
        style: dict[str, Any] | None = None,
        error_messages: dict[str, StrOrPromise] | None = None,
        validators: Sequence[Validator[uuid.UUID]] | None = None,
        allow_null: bool = False,
    ) -> None: ...

class IPAddressField(CharField):
    protocol: str
    unpack_ipv4: bool
    def __init__(
        self,
        protocol: str = "both",
        *,
        read_only: bool = False,
        write_only: bool = False,
        required: bool | None = None,
        default: _DefaultInitial[str] = ...,
        initial: _DefaultInitial[str] = ...,
        source: str | None = None,
        label: StrOrPromise | None = None,
        help_text: StrOrPromise | None = None,
        style: dict[str, Any] | None = None,
        error_messages: dict[str, StrOrPromise] | None = None,
        validators: Sequence[Validator[str]] | None = None,
        allow_null: bool = False,
        allow_blank: bool = False,
        trim_whitespace: bool = True,
        max_length: int | None = None,
        min_length: int | None = None,
    ) -> None: ...

class IntegerField(Field[int, float | int | str, int, Any]):
    MAX_STRING_LENGTH: int
    re_decimal: Pattern[str]
    max_value: int | None
    min_value: int | None
    def __init__(
        self,
        *,
        max_value: int | None = None,
        min_value: int | None = None,
        read_only: bool = False,
        write_only: bool = False,
        required: bool | None = None,
        default: _DefaultInitial[int] = ...,
        initial: _DefaultInitial[int] = ...,
        source: str | None = None,
        label: StrOrPromise | None = None,
        help_text: StrOrPromise | None = None,
        style: dict[str, Any] | None = None,
        error_messages: dict[str, StrOrPromise] | None = None,
        validators: Sequence[Validator[int]] | None = None,
        allow_null: bool = False,
    ) -> None: ...

class BigIntegerField(IntegerField):
    coerce_to_string: bool
    def __init__(
        self,
        coerce_to_string: bool | None = None,
        *,
        max_value: int | None = None,
        min_value: int | None = None,
        read_only: bool = False,
        write_only: bool = False,
        required: bool | None = None,
        default: _DefaultInitial[int] = ...,
        initial: _DefaultInitial[int] = ...,
        source: str | None = None,
        label: StrOrPromise | None = None,
        help_text: StrOrPromise | None = None,
        style: dict[str, Any] | None = None,
        error_messages: dict[str, StrOrPromise] | None = None,
        validators: Sequence[Validator[int]] | None = None,
        allow_null: bool = False,
    ) -> None: ...

class FloatField(Field[float, float | int | str, str, Any]):
    MAX_STRING_LENGTH: int
    max_value: float | None
    min_value: float | None
    def __init__(
        self,
        *,
        max_value: float | None = None,
        min_value: float | None = None,
        read_only: bool = False,
        write_only: bool = False,
        required: bool | None = None,
        default: _DefaultInitial[float] = ...,
        initial: _DefaultInitial[float] = ...,
        source: str | None = None,
        label: StrOrPromise | None = None,
        help_text: StrOrPromise | None = None,
        style: dict[str, Any] | None = None,
        error_messages: dict[str, StrOrPromise] | None = None,
        validators: Sequence[Validator[float]] | None = None,
        allow_null: bool = False,
    ) -> None: ...

class DecimalField(Field[Decimal, int | float | str | Decimal, str, Any]):
    MAX_STRING_LENGTH: int
    max_digits: int | None
    decimal_places: int | None
    coerce_to_string: bool | None
    max_value: Decimal | int | float | None
    min_value: Decimal | int | float | None
    localize: bool
    rounding: str | None
    normalize_output: bool
    max_whole_digits: int | None
    def __init__(
        self,
        max_digits: int | None,
        decimal_places: int | None,
        coerce_to_string: bool | None = None,
        max_value: Decimal | int | float | None = None,
        min_value: Decimal | int | float | None = None,
        localize: bool = False,
        rounding: str | None = None,
        normalize_output: bool = False,
        *,
        read_only: bool = False,
        write_only: bool = False,
        required: bool | None = None,
        default: _DefaultInitial[Decimal] = ...,
        initial: _DefaultInitial[Decimal] = ...,
        source: str | None = None,
        label: StrOrPromise | None = None,
        help_text: StrOrPromise | None = None,
        style: dict[str, Any] | None = None,
        error_messages: dict[str, StrOrPromise] | None = None,
        validators: Sequence[Validator[Decimal]] | None = None,
        allow_null: bool = False,
    ) -> None: ...
    def validate_precision(self, value: Decimal) -> Decimal: ...
    def quantize(self, value: Decimal) -> Decimal: ...

class DateTimeField(Field[datetime.datetime, datetime.datetime | str, str, Any]):
    datetime_parser: Callable[[str, str], datetime.datetime]
    format: str | None
    input_formats: Sequence[str]
    timezone: datetime.tzinfo
    def __init__(
        self,
        format: str | None | _Empty = ...,
        input_formats: Sequence[str] | None = None,
        default_timezone: datetime.tzinfo | None = None,
        *,
        read_only: bool = False,
        write_only: bool = False,
        required: bool | None = None,
        default: _DefaultInitial[datetime.datetime] = ...,
        initial: _DefaultInitial[datetime.datetime] = ...,
        source: str | None = None,
        label: StrOrPromise | None = None,
        help_text: StrOrPromise | None = None,
        style: dict[str, Any] | None = None,
        error_messages: dict[str, StrOrPromise] | None = None,
        validators: Sequence[Validator[datetime.datetime]] | None = None,
        allow_null: bool = False,
    ) -> None: ...
    def enforce_timezone(self, value: datetime.datetime) -> datetime.datetime: ...
    def default_timezone(self) -> datetime.tzinfo | None: ...
    @override
    def to_internal_value(self, value: datetime.datetime | str) -> datetime.datetime: ...

class DateField(Field[datetime.date, datetime.date | str, str, Any]):
    datetime_parser: Callable[[str, str], datetime.datetime]
    format: str | None
    input_formats: Sequence[str]
    def __init__(
        self,
        format: str | None | _Empty = ...,
        input_formats: Sequence[str] | None = None,
        *,
        read_only: bool = False,
        write_only: bool = False,
        required: bool | None = None,
        default: _DefaultInitial[datetime.date] = ...,
        initial: _DefaultInitial[datetime.date] = ...,
        source: str | None = None,
        label: StrOrPromise | None = None,
        help_text: StrOrPromise | None = None,
        style: dict[str, Any] | None = None,
        error_messages: dict[str, StrOrPromise] | None = None,
        validators: Sequence[Validator[datetime.date]] | None = None,
        allow_null: bool = False,
    ) -> None: ...
    @override
    def to_internal_value(self, value: datetime.date | str) -> datetime.date: ...

class TimeField(Field[datetime.time, datetime.time | str, str, Any]):
    datetime_parser: Callable[[str, str], datetime.datetime]
    format: str | None
    input_formats: Sequence[str]
    def __init__(
        self,
        format: str | None | _Empty = ...,
        input_formats: Sequence[str] | None = None,
        *,
        read_only: bool = False,
        write_only: bool = False,
        required: bool | None = None,
        default: _DefaultInitial[datetime.time] = ...,
        initial: _DefaultInitial[datetime.time] = ...,
        source: str | None = None,
        label: StrOrPromise | None = None,
        help_text: StrOrPromise | None = None,
        style: dict[str, Any] | None = None,
        error_messages: dict[str, StrOrPromise] | None = None,
        validators: Sequence[Validator[datetime.time]] | None = None,
        allow_null: bool = False,
    ) -> None: ...
    @override
    def to_internal_value(self, value: datetime.time | str) -> datetime.time: ...

class DurationField(Field[datetime.timedelta, datetime.timedelta | str, str, Any]):
    format: str | None
    max_value: datetime.timedelta | None
    min_value: datetime.timedelta | None
    def __init__(
        self,
        *,
        format: str | None | _Empty = ...,
        max_value: datetime.timedelta | int | float | None = None,
        min_value: datetime.timedelta | int | float | None = None,
        read_only: bool = False,
        write_only: bool = False,
        required: bool | None = None,
        default: _DefaultInitial[datetime.timedelta] = ...,
        initial: _DefaultInitial[datetime.timedelta] = ...,
        source: str | None = None,
        label: StrOrPromise | None = None,
        help_text: StrOrPromise | None = None,
        style: dict[str, Any] | None = None,
        error_messages: dict[str, StrOrPromise] | None = None,
        validators: Sequence[Validator[datetime.timedelta]] | None = None,
        allow_null: bool = False,
    ) -> None: ...
    @override
    def to_internal_value(self, value: datetime.timedelta | str) -> datetime.timedelta: ...

class ChoiceField(Field[str, str | int | tuple[str | int, str | int | tuple], str, Any]):
    html_cutoff: int | None
    html_cutoff_text: StrOrPromise | None
    allow_blank: bool
    grouped_choices: dict
    choice_strings_to_values: dict[str, Any]  # Any: heterogeneous choice values
    _choices: dict
    def __init__(
        self,
        choices: Sequence[Any],
        *,
        read_only: bool = False,
        write_only: bool = False,
        required: bool | None = None,
        default: _DefaultInitial[StrOrPromise | int] = ...,
        initial: _DefaultInitial[str | int] = ...,
        source: str | None = None,
        label: StrOrPromise | None = None,
        help_text: StrOrPromise | None = None,
        style: dict[str, Any] | None = None,
        error_messages: dict[str, StrOrPromise] | None = None,
        validators: Sequence[Validator[Any]] | None = None,
        allow_null: bool = False,
        html_cutoff: int = ...,
        html_cutoff_text: StrOrPromise = ...,
        allow_blank: bool = False,
    ) -> None: ...
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
        *,
        choices: Sequence[Any],
        read_only: bool = False,
        write_only: bool = False,
        required: bool | None = None,
        default: _DefaultInitial[set[str | int] | set[str] | set[int]] = ...,
        initial: _DefaultInitial[set[StrOrPromise | int] | set[StrOrPromise] | set[int]] = ...,
        source: str | None = None,
        label: StrOrPromise | None = None,
        help_text: StrOrPromise | None = None,
        style: dict[str, Any] | None = None,
        error_messages: dict[str, StrOrPromise] | None = None,
        validators: Sequence[Validator[Any]] | None = None,
        allow_null: bool = False,
        html_cutoff: int = ...,
        html_cutoff_text: StrOrPromise = ...,
        allow_blank: bool = False,
        allow_empty: bool = True,
    ) -> None: ...

class FilePathField(ChoiceField):
    def __init__(
        self,
        path: str,
        match: str | None = None,
        recursive: bool = False,
        allow_files: bool = True,
        allow_folders: bool = False,
        required: bool | None = None,
        *,
        read_only: bool = False,
        write_only: bool = False,
        default: _DefaultInitial[str] = ...,
        initial: _DefaultInitial[str] = ...,
        source: str | None = None,
        label: StrOrPromise | None = None,
        help_text: StrOrPromise | None = None,
        style: dict[str, Any] | None = None,
        error_messages: dict[str, StrOrPromise] | None = None,
        validators: Sequence[Validator[Any]] | None = None,
        allow_null: bool = False,
        html_cutoff: int = ...,
        html_cutoff_text: StrOrPromise = ...,
        allow_blank: bool = False,
    ) -> None: ...

class FileField(Field[File, File, str | None, Any]):  # this field can return None without raising!
    max_length: int | None
    allow_empty_file: bool
    use_url: bool
    def __init__(
        self,
        *,
        read_only: bool = False,
        write_only: bool = False,
        required: bool | None = None,
        default: _DefaultInitial[File] = ...,
        initial: _DefaultInitial[File] = ...,
        source: str | None = None,
        label: StrOrPromise | None = None,
        help_text: StrOrPromise | None = None,
        style: dict[str, Any] | None = None,
        error_messages: dict[str, StrOrPromise] | None = None,
        validators: Sequence[Validator[File]] | None = None,
        allow_null: bool = False,
        max_length: int | None = None,
        allow_empty_file: bool = False,
        use_url: bool = ...,
    ) -> None: ...

class ImageField(FileField):
    _DjangoImageField: SupportsToPython
    def __init__(
        self,
        *,
        read_only: bool = False,
        write_only: bool = False,
        required: bool | None = None,
        default: _DefaultInitial[File] = ...,
        initial: _DefaultInitial[File] = ...,
        source: str | None = None,
        label: StrOrPromise | None = None,
        help_text: StrOrPromise | None = None,
        style: dict[str, Any] | None = None,
        error_messages: dict[str, StrOrPromise] | None = None,
        validators: Sequence[Validator[File]] | None = None,
        allow_null: bool = False,
        max_length: int | None = None,
        allow_empty_file: bool = False,
        use_url: bool = ...,
        _DjangoImageField: type[SupportsToPython] = ...,
    ) -> None: ...

class _UnvalidatedField(Field):
    allow_blank: bool

class ListField(Field[list[Any], list[Any], list[Any], Any]):
    child: Field
    initial: list[Any]
    allow_empty: bool
    max_length: int | None
    min_length: int | None
    def __init__(
        self,
        *,
        read_only: bool = False,
        write_only: bool = False,
        required: bool | None = None,
        default: _DefaultInitial[list[Any]] = ...,
        initial: _DefaultInitial[list[Any]] = ...,
        source: str | None = None,
        label: StrOrPromise | None = None,
        help_text: StrOrPromise | None = None,
        style: dict[str, Any] | None = None,
        error_messages: dict[str, StrOrPromise] | None = None,
        validators: Sequence[Validator[list[Any]]] | None = None,
        allow_null: bool = False,
        child: Field = ...,
        allow_empty: bool = True,
        max_length: int | None = None,
        min_length: int | None = None,
    ) -> None: ...
    @override
    def to_representation(self, data: list[Any]) -> list[Any]: ...
    def run_child_validation(self, data: list[Mapping[Any, Any]]) -> list[Any]: ...

class DictField(Field[dict[Any, Any], dict[Any, Any], dict[Any, Any], Any]):
    child: Field
    initial: dict[Any, Any]
    allow_empty: bool
    def __init__(
        self,
        *,
        read_only: bool = False,
        write_only: bool = False,
        required: bool | None = None,
        default: _DefaultInitial[dict[Any, Any]] = ...,
        initial: _DefaultInitial[dict[Any, Any]] = ...,
        source: str | None = None,
        label: StrOrPromise | None = None,
        help_text: StrOrPromise | None = None,
        style: dict[str, Any] | None = None,
        error_messages: dict[str, StrOrPromise] | None = None,
        validators: Sequence[Validator[dict[Any, Any]]] | None = None,
        allow_null: bool = False,
        child: Field = ...,
        allow_empty: bool = True,
    ) -> None: ...
    def run_child_validation(self, data: Mapping[str, Any]) -> dict[str, Any]: ...

class HStoreField(DictField):
    child: CharField

class JSONField(Field[dict[str, Any] | list[dict[str, Any]], dict[str, Any] | list[dict[str, Any]], str, Any]):
    binary: bool
    encoder: type[JSONEncoder] | None
    decoder: type[JSONDecoder] | None
    def __init__(
        self,
        *,
        read_only: bool = False,
        write_only: bool = False,
        required: bool | None = None,
        default: _DefaultInitial[Mapping[Any, Any]] = ...,
        initial: _DefaultInitial[Mapping[Any, Any]] = ...,
        source: str | None = None,
        label: StrOrPromise | None = None,
        help_text: StrOrPromise | None = None,
        style: dict[str, Any] | None = None,
        error_messages: dict[str, StrOrPromise] | None = None,
        validators: Sequence[Validator[Any]] | None = None,
        allow_null: bool = False,
        binary: bool = False,
        encoder: type[JSONEncoder] | None = None,
        decoder: type[JSONDecoder] | None = None,
    ) -> None: ...

class ReadOnlyField(Field): ...
class HiddenField(Field): ...

class SerializerMethodField(Field):
    method_name: str
    def __init__(
        self,
        method_name: str | None = None,
        *,
        read_only: bool = False,
        write_only: bool = False,
        required: bool | None = None,
        default: Any = ...,
        initial: Any = ...,
        source: str | None = None,
        label: StrOrPromise | None = None,
        help_text: StrOrPromise | None = None,
        style: dict[str, Any] | None = None,
        error_messages: dict[str, StrOrPromise] | None = None,
        validators: Sequence[Validator[Any]] | None = None,
        allow_null: bool = False,
    ) -> None: ...

class ModelField(Field):
    model_field: models.Field
    max_length: int | None
    def __init__(
        self,
        model_field: models.Field,
        *,
        read_only: bool = False,
        write_only: bool = False,
        required: bool | None = None,
        default: Any = ...,
        initial: Any = ...,
        source: str | None = None,
        label: StrOrPromise | None = None,
        help_text: StrOrPromise | None = None,
        style: dict[str, Any] | None = None,
        error_messages: dict[str, StrOrPromise] | None = None,
        validators: Sequence[Validator[Any]] | None = None,
        allow_null: bool = False,
        max_length: int | None = None,
    ) -> None: ...
    @override
    def get_attribute(self, obj: Any) -> Any: ...  # Any: returns obj unchanged
    @override
    def to_representation(self, obj: Any) -> Any: ...  # Any: delegates to model_field
