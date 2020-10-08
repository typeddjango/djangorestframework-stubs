import datetime
from django.core.files.base import File
import uuid
from collections import OrderedDict
from decimal import Decimal
from json import JSONDecoder, JSONEncoder
from typing import (
    Any,
    Callable,
    Dict,
    Iterable,
    List,
    Mapping,
    MutableMapping,
    NoReturn,
    Optional,
    Pattern,
    Protocol,
    Sequence,
    Set,
    Tuple,
    Type,
    Union,
    Generic,
    TypeVar,
    Generator,
)
from typing_extensions import Literal
from django.db import models
from django.db.models import Model
from rest_framework.serializers import BaseSerializer
from django.forms import ImageField as DjangoImageField  # noqa: F401

class empty: ...
class BuiltinSignatureError(Exception): ...

class CreateOnlyDefault:
    requires_context: bool = ...
    default: Any = ...
    def __init__(self, default: Any) -> None: ...
    def __call__(self, serializer_field: Field): ...

class CurrentUserDefault:
    requires_context: bool = ...
    def __call__(self, serializer_field: Field): ...

class SkipField(Exception): ...

class Option(Protocol):
    start_option_group: bool = ...
    end_option_group: bool = ...
    label: str
    value: str
    display_text: str

def is_simple_callable(obj: Callable) -> bool: ...
def get_attribute(instance: Any, attrs: Optional[List[str]]) -> Any: ...
def set_value(dictionary: MutableMapping[str, Any], keys: Sequence[str], value: Any) -> None: ...
def to_choices_dict(choices: Sequence) -> OrderedDict: ...
def flatten_choices_dict(choices: Dict[Any, Any]) -> OrderedDict: ...
def iter_options(
    grouped_choices: OrderedDict, cutoff: Optional[int] = ..., cutoff_text: Optional[str] = ...
) -> Generator[Option, None, None]: ...
def get_error_detail(exc_info: Any) -> Any: ...

REGEX_TYPE: Pattern
NOT_READ_ONLY_WRITE_ONLY: str
NOT_READ_ONLY_REQUIRED: str
NOT_REQUIRED_DEFAULT: str
USE_READONLYFIELD: str
MISSING_ERROR_MESSAGE: str

_IN = TypeVar("_IN", Model, Mapping[Any, Any], Sequence[Mapping[Any, Any]], covariant=True)  # Instance Type
_VT = TypeVar("_VT", covariant=True)  # Value Type
_DT = TypeVar("_DT", covariant=True)  # Data Type
_RP = TypeVar("_RP", covariant=True)  # Representation Type

class SupportsToPython(Protocol):
    def to_python(self, value: Any) -> Any: ...

class Field(Generic[_VT, _DT, _RP, _IN]):
    allow_null: bool
    default: Optional[_VT]
    default_empty_html: Any = ...
    default_error_messages: Dict[str, str] = ...
    default_validators: List[Callable] = ...
    error_messages: Dict[str, str] = ...
    field_name: Optional[str] = ...
    help_text: Optional[str] = ...
    initial: Optional[Union[_VT, Callable[[Any], _VT]]] = ...
    label: Optional[str]
    parent: BaseSerializer
    read_only: bool
    required: bool
    source: Optional[Union[Callable, str]]
    source_attrs: List[str] = ...
    style: Dict[str, Any]
    write_only: bool
    def __init__(
        self,
        read_only: bool = ...,
        write_only: bool = ...,
        required: bool = ...,
        default: Union[_VT, Callable[[Any], _VT]] = ...,
        initial: Union[_VT, Callable[[Any], _VT]] = ...,
        source: str = ...,
        label: str = ...,
        help_text: str = ...,
        style: Dict[str, Any] = ...,
        error_messages: Dict[str, str] = ...,
        validators: Sequence[Callable] = ...,
        allow_null: bool = ...,
    ): ...
    def bind(self, field_name: str, parent: BaseSerializer) -> None: ...
    @property
    def validators(self) -> List[Callable]: ...
    @validators.setter
    def validators(self, validators: List[Callable]) -> None: ...
    def get_validators(self) -> List[Callable]: ...
    def get_initial(self) -> Union[_VT, empty]: ...
    def get_value(self, dictionary: Mapping[Any, Any]) -> Any: ...
    def get_attribute(self, instance: _IN) -> Optional[_RP]: ...
    def get_default(self) -> Optional[_VT]: ...
    def validate_empty_values(self, data: Any) -> Tuple[bool, Any]: ...
    def run_validation(self, data: Any = ...) -> Any: ...
    def run_validators(self, value: Any) -> None: ...
    def to_internal_value(self, data: _DT) -> _VT: ...
    def to_representation(self, value: _VT) -> _RP: ...
    def fail(self, key: str, **kwargs: Any) -> NoReturn: ...
    @property
    def root(self) -> BaseSerializer: ...
    @property
    def context(self) -> Dict[str, Any]: ...
    def __new__(cls, *args: Any, **kwargs: Any) -> Field: ...
    def __deepcopy__(self, memo: Mapping[Any, Any]) -> Field: ...

class BooleanField(
    Field[
        bool,
        Union[
            bool,
            None,
            Literal["t"],
            Literal["T"],
            Literal["y"],
            Literal["Y"],
            Literal["yes"],
            Literal["YES"],
            Literal["true"],
            Literal["True"],
            Literal["TRUE"],
            Literal["on"],
            Literal["On"],
            Literal["ON"],
            Literal["1"],
            Literal[1],
            Literal["f"],
            Literal["F"],
            Literal["n"],
            Literal["N"],
            Literal["no"],
            Literal["NO"],
            Literal["false"],
            Literal["False"],
            Literal["FALSE"],
            Literal["off"],
            Literal["Off"],
            Literal["OFF"],
            Literal["0"],
            Literal[0],
            Literal[0.0],
        ],
        bool,
    ]
):
    TRUE_VALUES: Set[str, bool, int] = ...
    FALSE_VALUES: Set[str, bool, int, float] = ...
    NULL_VALUES: Set[str, None] = ...

class NullBooleanField(
    Field[
        Union[bool, None],
        Union[
            bool,
            None,
            Literal["t"],
            Literal["T"],
            Literal["y"],
            Literal["Y"],
            Literal["yes"],
            Literal["YES"],
            Literal["true"],
            Literal["True"],
            Literal["TRUE"],
            Literal["on"],
            Literal["On"],
            Literal["ON"],
            Literal["1"],
            Literal[1],
            Literal["f"],
            Literal["F"],
            Literal["n"],
            Literal["N"],
            Literal["no"],
            Literal["NO"],
            Literal["false"],
            Literal["False"],
            Literal["FALSE"],
            Literal["off"],
            Literal["Off"],
            Literal["OFF"],
            Literal["0"],
            Literal[0],
            Literal[0.0],
            Literal["null"],
            Literal["Null"],
            Literal["NULL"],
            Literal[""],
        ],
        bool,
    ]
):
    TRUE_VALUES: Set[str, bool, int] = ...
    FALSE_VALUES: Set[str, bool, int, float] = ...
    NULL_VALUES: Set[str, None] = ...

class CharField(Field[str, str, str]):
    allow_blank: bool = ...
    trim_whitespace: bool = ...
    max_length: Optional[int] = ...
    min_length: Optional[int] = ...
    def __init__(
        self,
        read_only: bool = ...,
        write_only: bool = ...,
        required: bool = ...,
        default: Union[str, Callable[[Any], str]] = ...,
        initial: Union[str, Callable[[Any], str]] = ...,
        source: str = ...,
        label: str = ...,
        help_text: str = ...,
        style: Dict[str, Any] = ...,
        error_messages: Dict[str, str] = ...,
        validators: Sequence[Callable] = ...,
        allow_null: bool = ...,
        allow_blank: bool = ...,
        trim_whitespace: bool = ...,
        max_length: int = ...,
        min_length: Optional[int] = ...,
    ): ...

class EmailField(CharField): ...

class RegexField(CharField):
    def __init__(
        self,
        regex: Union[str, Pattern],
        read_only: bool = ...,
        write_only: bool = ...,
        required: bool = ...,
        default: Union[str, Callable[[Any], str]] = ...,
        initial: Union[str, Callable[[Any], str]] = ...,
        source: str = ...,
        label: str = ...,
        help_text: str = ...,
        style: Dict[str, Any] = ...,
        error_messages: Dict[str, str] = ...,
        validators: Sequence[Callable] = ...,
        allow_null: bool = ...,
        allow_blank: bool = ...,
        trim_whitespace: bool = ...,
        max_length: int = ...,
        min_length: Optional[int] = ...,
    ): ...

class SlugField(CharField):
    allow_unicode: bool = ...
    def __init__(
        self,
        read_only: bool = ...,
        write_only: bool = ...,
        required: bool = ...,
        default: Union[str, Callable[[Any], str]] = ...,
        initial: Union[str, Callable[[Any], str]] = ...,
        source: str = ...,
        label: str = ...,
        help_text: str = ...,
        style: Dict[str, Any] = ...,
        error_messages: Dict[str, str] = ...,
        validators: Sequence[Callable] = ...,
        allow_null: bool = ...,
        allow_blank: bool = ...,
        trim_whitespace: bool = ...,
        max_length: int = ...,
        min_length: Optional[int] = ...,
        allow_unicode: bool = ...,
    ): ...

class URLField(CharField): ...

class UUIDField(Field[uuid.UUID, Union[uuid.UUID, str, int], str]):
    valid_formats: Sequence[str] = ...
    uuid_format: str
    def __init__(
        self,
        read_only: bool = ...,
        write_only: bool = ...,
        required: bool = ...,
        default: Union[uuid.UUID, Callable[[Any], uuid.UUID]] = ...,
        initial: Union[uuid.UUID, Callable[[Any], uuid.UUID]] = ...,
        source: str = ...,
        label: str = ...,
        help_text: str = ...,
        style: Dict[str, Any] = ...,
        error_messages: Dict[str, str] = ...,
        validators: Sequence[Callable] = ...,
        allow_null: bool = ...,
        format: str = ...,
    ): ...

class IPAddressField(CharField):
    protocol: str
    unpack_ipv4: bool
    def __init__(
        self,
        read_only: bool = ...,
        write_only: bool = ...,
        required: bool = ...,
        default: Union[str, Callable[[Any], str]] = ...,
        initial: Union[str, Callable[[Any], str]] = ...,
        source: str = ...,
        label: str = ...,
        help_text: str = ...,
        style: Dict[str, Any] = ...,
        error_messages: Dict[str, str] = ...,
        validators: Sequence[Callable] = ...,
        allow_null: bool = ...,
        allow_blank: bool = ...,
        trim_whitespace: bool = ...,
        max_length: int = ...,
        min_length: Optional[int] = ...,
        protocol: str = ...,
    ): ...

class IntegerField(Field[int, Union[float, int, str], int]):
    MAX_STRING_LENGTH: int = ...
    re_decimal: Pattern = ...
    max_value: Optional[int] = ...
    min_value: Optional[int] = ...
    def __init__(
        self,
        read_only: bool = ...,
        write_only: bool = ...,
        required: bool = ...,
        default: Union[int, Callable[[Any], int]] = ...,
        initial: Union[int, Callable[[Any], int]] = ...,
        source: str = ...,
        label: str = ...,
        help_text: str = ...,
        style: Dict[str, Any] = ...,
        error_messages: Dict[str, str] = ...,
        validators: Sequence[Callable] = ...,
        allow_null: bool = ...,
        max_value: int = ...,
        min_value: int = ...,
    ): ...

class FloatField(Field[float, Union[float, int, str], str]):
    MAX_STRING_LENGTH: int = ...
    re_decimal: Pattern = ...
    max_value: Optional[int] = ...
    min_value: Optional[int] = ...
    def __init__(
        self,
        read_only: bool = ...,
        write_only: bool = ...,
        required: bool = ...,
        default: Union[float, Callable[[Any], float]] = ...,
        initial: Union[float, Callable[[Any], float]] = ...,
        source: str = ...,
        label: str = ...,
        help_text: str = ...,
        style: Dict[str, Any] = ...,
        error_messages: Dict[str, str] = ...,
        validators: Sequence[Callable] = ...,
        allow_null: bool = ...,
        max_value: int = ...,
        min_value: int = ...,
    ): ...

class DecimalField(Field[Decimal, Union[int, float, str, Decimal], str]):
    MAX_STRING_LENGTH: int = ...
    max_digits: Optional[int]
    decimal_places: Optional[int]
    coerce_to_string: Optional[bool]
    max_value: Optional[Union[Decimal, int, float]]
    min_value: Optional[Union[Decimal, int, float]]
    localize: bool
    rounding: Optional[str]
    max_whole_digits = Optional[int]
    def __init__(
        self,
        max_digits: Optional[int],
        decimal_places: Optional[int],
        read_only: bool = ...,
        write_only: bool = ...,
        required: bool = ...,
        default: Union[Decimal, Callable[[Any], Decimal]] = ...,
        initial: Union[Decimal, Callable[[Any], Decimal]] = ...,
        source: str = ...,
        label: str = ...,
        help_text: str = ...,
        style: Dict[str, Any] = ...,
        error_messages: Dict[str, str] = ...,
        validators: Sequence[Callable] = ...,
        allow_null: bool = ...,
        coerce_to_string: bool = ...,
        max_value: Union[Decimal, int, float] = ...,
        min_value: Union[Decimal, int, float] = ...,
        localize: bool = ...,
        rounding: str = ...,
    ): ...
    def validate_precision(self, value: Decimal) -> Decimal: ...
    def quantize(self, value: Decimal) -> Decimal: ...

class DateTimeField(Field[datetime.datetime, Union[datetime.datetime, str], str]):
    datetime_parser: Callable[[str, str], datetime.datetime] = ...
    format: Optional[str] = ...
    input_formats: Sequence[str] = ...
    timezone: datetime.tzinfo = ...
    def __init__(
        self,
        read_only: bool = ...,
        write_only: bool = ...,
        required: bool = ...,
        default: Union[datetime.datetime, Callable[[Any], datetime.datetime]] = ...,
        initial: Union[datetime.datetime, Callable[[Any], datetime.datetime]] = ...,
        source: str = ...,
        label: str = ...,
        help_text: str = ...,
        style: Dict[str, Any] = ...,
        error_messages: Dict[str, str] = ...,
        validators: Sequence[Callable] = ...,
        allow_null: bool = ...,
        format: str = ...,
        input_formats: Sequence[str] = ...,
        default_timezone: datetime.tzinfo = ...,
    ): ...
    def enforce_timezone(self, value: datetime.datetime) -> datetime.datetime: ...
    def default_timezone(self) -> Optional[str]: ...

class DateField(Field[datetime.date, Union[datetime.date, str], str]):
    datetime_parser: Callable[[str, str], datetime.datetime] = ...
    format: Optional[str]
    input_formats: Sequence[str]
    def __init__(
        self,
        read_only: bool = ...,
        write_only: bool = ...,
        required: bool = ...,
        default: Union[datetime.date, Callable[[Any], datetime.date]] = ...,
        initial: Union[datetime.date, Callable[[Any], datetime.date]] = ...,
        source: str = ...,
        label: str = ...,
        help_text: str = ...,
        style: Dict[str, Any] = ...,
        error_messages: Dict[str, str] = ...,
        validators: Sequence[Callable] = ...,
        allow_null: bool = ...,
        format: str = ...,
        input_formats: Sequence[str] = ...,
    ): ...

class TimeField(Field[datetime.time, Union[datetime.time, str], str]):
    datetime_parser: Callable[[str, str], datetime.datetime] = ...
    format: Optional[str]
    input_formats: Sequence[str]
    def __init__(
        self,
        read_only: bool = ...,
        write_only: bool = ...,
        required: bool = ...,
        default: Union[datetime.time, Callable[[Any], datetime.time]] = ...,
        initial: Union[datetime.time, Callable[[Any], datetime.time]] = ...,
        source: str = ...,
        label: str = ...,
        help_text: str = ...,
        style: Dict[str, Any] = ...,
        error_messages: Dict[str, str] = ...,
        validators: Sequence[Callable] = ...,
        allow_null: bool = ...,
        format: str = ...,
        input_formats: Sequence[str] = ...,
    ): ...

class DurationField(Field[datetime.timedelta, Union[datetime.timedelta, str], str]):
    max_value: Optional[datetime.timedelta]
    min_value: Optional[datetime.timedelta]
    def __init__(
        self,
        read_only: bool = ...,
        write_only: bool = ...,
        required: bool = ...,
        default: Union[datetime.timedelta, Callable[[Any], datetime.timedelta]] = ...,
        initial: Union[datetime.timedelta, Callable[[Any], datetime.timedelta]] = ...,
        source: str = ...,
        label: str = ...,
        help_text: str = ...,
        style: Dict[str, Any] = ...,
        error_messages: Dict[str, str] = ...,
        validators: Sequence[Callable] = ...,
        allow_null: bool = ...,
        max_value: datetime.timedelta = ...,
        min_value: datetime.timedelta = ...,
    ): ...

class ChoiceField(Field[str, str, str]):
    html_cutoff: Optional[int] = ...
    html_cutoff_text: Optional[str] = ...
    allow_blank: bool
    grouped_choices: OrderedDict
    choice_strings_to_values: Dict[str, Any]
    _choices: OrderedDict
    def __init__(
        self,
        choices: Sequence[Any],
        read_only: bool = ...,
        write_only: bool = ...,
        required: bool = ...,
        default: Union[str, Callable[[Any], str]] = ...,
        initial: Union[str, Callable[[Any], str]] = ...,
        source: str = ...,
        label: str = ...,
        help_text: str = ...,
        style: Dict[str, Any] = ...,
        error_messages: Dict[str, str] = ...,
        validators: Sequence[Callable] = ...,
        allow_null: bool = ...,
        html_cutoff: int = ...,
        html_cutoff_text: str = ...,
        allow_blank: bool = ...,
    ): ...
    def iter_options(self) -> Iterable[Option]: ...
    def _get_choices(self) -> Dict[Any, Any]: ...
    def _set_choices(self, choices: Sequence[Any]) -> None: ...
    choices = property(_get_choices, _set_choices)

class MultipleChoiceField(ChoiceField, Field[str, Sequence[str], Sequence[str]]):
    allow_empty: bool
    def __init__(
        self,
        choices: Sequence[Any],
        read_only: bool = ...,
        write_only: bool = ...,
        required: bool = ...,
        default: Union[Sequence[str], Callable[[Any], Sequence[str]]] = ...,
        initial: Union[Sequence[str], Callable[[Any], Sequence[str]]] = ...,
        source: str = ...,
        label: str = ...,
        help_text: str = ...,
        style: Dict[str, Any] = ...,
        error_messages: Dict[str, str] = ...,
        validators: Sequence[Callable] = ...,
        allow_null: bool = ...,
        html_cutoff: int = ...,
        html_cutoff_text: str = ...,
        allow_blank: bool = ...,
        allow_empty: bool = ...,
    ): ...

class FilePathField(ChoiceField):
    def __init__(
        self,
        path: str,
        read_only: bool = ...,
        write_only: bool = ...,
        required: bool = ...,
        default: Union[str, Callable[[Any], str]] = ...,
        initial: Union[str, Callable[[Any], str]] = ...,
        source: str = ...,
        label: str = ...,
        help_text: str = ...,
        style: Dict[str, Any] = ...,
        error_messages: Dict[str, str] = ...,
        validators: Sequence[Callable] = ...,
        allow_null: bool = ...,
        html_cutoff: int = ...,
        html_cutoff_text: str = ...,
        allow_blank: bool = ...,
        match: str = ...,
        recursive: bool = ...,
        allow_files: bool = ...,
        allow_folders: bool = ...,
    ): ...

class FileField(Field[File, File, Union[str, None]]):  # this field can return None without raising!
    max_length: int
    allow_empty_file: bool
    use_url: bool
    def __init__(
        self,
        read_only: bool = ...,
        write_only: bool = ...,
        required: bool = ...,
        default: Union[File, Callable[[Any], File]] = ...,
        initial: Union[File, Callable[[Any], File]] = ...,
        source: str = ...,
        label: str = ...,
        help_text: str = ...,
        style: Dict[str, Any] = ...,
        error_messages: Dict[str, str] = ...,
        validators: Sequence[Callable] = ...,
        allow_null: bool = ...,
        max_length: int = ...,
        allow_empty_file: bool = ...,
        use_url: bool = ...,
    ): ...

class ImageField(FileField):
    _DjangoImageField: SupportsToPython
    def __init__(
        self,
        read_only: bool = ...,
        write_only: bool = ...,
        required: bool = ...,
        default: Union[File, Callable[[Any], File]] = ...,
        initial: Union[File, Callable[[Any], File]] = ...,
        source: str = ...,
        label: str = ...,
        help_text: str = ...,
        style: Dict[str, Any] = ...,
        error_messages: Dict[str, str] = ...,
        validators: Sequence[Callable] = ...,
        allow_null: bool = ...,
        max_length: int = ...,
        allow_empty_file: bool = ...,
        use_url: bool = ...,
        _DjangoImageField: Type[SupportsToPython] = ...,
    ): ...

class _UnvalidatedField(Field): ...

class ListField(Field[List[Mapping[Any, Any]], List[Dict[Any, Any]], List[Mapping[Any, Any]]]):
    child: Field = ...
    allow_empty: bool = ...
    max_length: Optional[int] = ...
    min_length: Optional[int] = ...
    def __init__(
        self,
        read_only: bool = ...,
        write_only: bool = ...,
        required: bool = ...,
        default: Union[List[Mapping[Any, Any]], Callable[[Any], List[Mapping[Any, Any]]]] = ...,
        initial: Union[List[Mapping[Any, Any]], Callable[[Any], List[Mapping[Any, Any]]]] = ...,
        source: str = ...,
        label: str = ...,
        help_text: str = ...,
        style: Dict[str, Any] = ...,
        error_messages: Dict[str, str] = ...,
        validators: Sequence[Callable] = ...,
        allow_null: bool = ...,
        child: Field = ...,
        allow_empty: bool = ...,
        max_length: int = ...,
        min_length: int = ...,
    ): ...
    def run_child_validation(self, data: List[Mapping[Any, Any]]) -> Any: ...

class DictField(Field[Dict[Any, Any], Dict[Any, Any], Dict[Any, Any]]):
    child: Field = ...
    allow_empty: bool = ...
    def __init__(
        self,
        read_only: bool = ...,
        write_only: bool = ...,
        required: bool = ...,
        default: Union[Dict[Any, Any], Callable[[Any], Dict[Any, Any]]] = ...,
        initial: Union[Dict[Any, Any], Callable[[Any], Dict[Any, Any]]] = ...,
        source: str = ...,
        label: str = ...,
        help_text: str = ...,
        style: Dict[str, Any] = ...,
        error_messages: Dict[str, str] = ...,
        validators: Sequence[Callable] = ...,
        allow_null: bool = ...,
        child: Field = ...,
        allow_empty: bool = ...,
    ): ...
    def run_child_validation(self, data: Any) -> Any: ...

class HStoreField(DictField):
    child: CharField = ...

class JSONField(Field[Union[Dict[str, Any], List[Dict[str, Any]]], Union[Dict[str, Any], List[Dict[str, Any]]], str]):
    binary: bool = ...
    encoder: Optional[JSONEncoder] = ...
    decoder: Optional[JSONDecoder] = ...
    def __init__(
        self,
        read_only: bool = ...,
        write_only: bool = ...,
        required: bool = ...,
        default: Union[Mapping[Any, Any], Callable[[Any], Mapping[Any, Any]]] = ...,
        initial: Union[Mapping[Any, Any], Callable[[Any], Mapping[Any, Any]]] = ...,
        source: str = ...,
        label: str = ...,
        help_text: str = ...,
        style: Dict[str, Any] = ...,
        error_messages: Dict[str, str] = ...,
        validators: Sequence[Callable] = ...,
        allow_null: bool = ...,
        binary: bool = ...,
        encoder: JSONEncoder = ...,
        decoder: JSONDecoder = ...,
    ): ...

class ReadOnlyField(Field): ...
class HiddenField(Field): ...

class SerializerMethodField(Field):
    method_name: str = ...
    def __init__(
        self,
        read_only: bool = ...,
        write_only: bool = ...,
        required: bool = ...,
        default: Any = ...,
        initial: Any = ...,
        source: str = ...,
        label: str = ...,
        help_text: str = ...,
        style: Dict[str, Any] = ...,
        error_messages: Dict[str, str] = ...,
        validators: Sequence[Callable] = ...,
        allow_null: bool = ...,
        method_name: str = ...,
    ): ...

class ModelField(Field):
    model_field: models.Field = ...
    max_length: int = ...
    def __init__(
        self,
        model_field: models.Field,
        read_only: bool = ...,
        write_only: bool = ...,
        required: bool = ...,
        default: Any = ...,
        initial: Any = ...,
        source: str = ...,
        label: str = ...,
        help_text: str = ...,
        style: Dict[str, Any] = ...,
        error_messages: Dict[str, str] = ...,
        validators: Sequence[Callable] = ...,
        allow_null: bool = ...,
        max_length: int = ...,
    ): ...
