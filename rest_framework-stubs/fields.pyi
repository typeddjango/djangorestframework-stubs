import datetime
import decimal
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
    TypeVar,
    Union,
)

from django.db import models
from django.db.models import Model
from rest_framework.relations import Option
from rest_framework.serializers import BaseSerializer

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

def is_simple_callable(obj: Callable) -> bool: ...
def get_attribute(instance: Any, attrs: Optional[List[str]]) -> Any: ...
def set_value(dictionary: MutableMapping[str, Any], keys: Sequence[str], value: Any) -> None: ...
def to_choices_dict(choices: Sequence) -> OrderedDict: ...
def flatten_choices_dict(choices: Dict[Any, Any]) -> OrderedDict: ...
def iter_options(grouped_choices: Iterable, cutoff: Optional[int] = ..., cutoff_text: Optional[str] = ...) -> None: ...
def get_error_detail(exc_info: Any) -> Any: ...

REGEX_TYPE: Pattern
NOT_READ_ONLY_WRITE_ONLY: str
NOT_READ_ONLY_REQUIRED: str
NOT_REQUIRED_DEFAULT: str
USE_READONLYFIELD: str
MISSING_ERROR_MESSAGE: str

_FT = TypeVar("_FT")  # Field Type
_FPT = TypeVar("_FPT")  # Field Primitive Type

_Instance = Union[Model, Mapping[Any, Any], Dict[Any, Any], Callable]

class SupportsToPython(Protocol):
    def to_python(self, value: Any) -> Any: ...

class Field:
    allow_null: bool
    default: Any
    default_empty_html: Any = ...
    default_error_messages: Dict[str, str] = ...
    default_validators: List[Callable] = ...
    error_messages: Dict[str, str] = ...
    field_name: Optional[str] = ...
    help_text: Optional[str]
    initial: Any = ...
    label: Optional[str]
    parent: BaseSerializer
    read_only: bool
    required: bool
    source: Optional[Union[Callable, str]]
    source_attrs: List[str] = ...
    style: Optional[Dict[str, Any]]
    write_only: bool
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
        style: Optional[Dict[str, Any]] = ...,
        error_messages: Optional[Dict[str, str]] = ...,
        validators: Optional[Sequence[Callable]] = ...,
        allow_null: bool = ...,
    ): ...
    def bind(self, field_name: str, parent: BaseSerializer) -> None: ...
    @property
    def validators(self) -> List[Callable]: ...
    @validators.setter
    def validators(self, validators: List[Callable]) -> None: ...
    def get_validators(self) -> List[Callable]: ...
    def get_initial(self) -> Any: ...
    def get_value(self, dictionary: Mapping[Any, Any]) -> Any: ...
    def get_attribute(self, instance: _Instance) -> Optional[Any]: ...
    def get_default(self) -> Any: ...
    def validate_empty_values(self, data: Any) -> Tuple[bool, Any]: ...
    def run_validation(self, data: Any = ...) -> Any: ...
    def run_validators(self, value: Any) -> None: ...
    def to_internal_value(self, data: Any) -> Any: ...
    def to_representation(self, value: Any) -> Any: ...
    def fail(self, key: str, **kwargs: Any) -> NoReturn: ...
    @property
    def root(self) -> BaseSerializer: ...
    @property
    def context(self) -> Dict[str, Any]: ...
    def __new__(cls, *args: Any, **kwargs: Any) -> Field: ...
    def __deepcopy__(self, memo: Mapping[Any, Any]) -> Field: ...

class BooleanField(Field):
    initial: bool = ...
    TRUE_VALUES: Set[Any] = ...
    FALSE_VALUES: Set[Any] = ...
    NULL_VALUES: Set[Optional[Any]] = ...

class NullBooleanField(Field):
    initial: Optional[bool] = ...
    TRUE_VALUES: Set[Any] = ...
    FALSE_VALUES: Set[Any] = ...
    NULL_VALUES: Set[Optional[Any]] = ...

class CharField(Field):
    _pyi_field_actual_type: str
    _pyi_field_primitive_type: str
    allow_blank: bool = ...
    trim_whitespace: bool = ...
    max_length: Optional[int] = ...
    min_length: Optional[int] = ...
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
        style: Optional[Dict[str, Any]] = ...,
        error_messages: Optional[Dict[str, str]] = ...,
        validators: Optional[Sequence[Callable]] = ...,
        allow_null: bool = ...,
        allow_blank: bool = ...,
        trim_whitespace: bool = ...,
        max_length: Optional[int] = ...,
        min_length: Optional[int] = ...,
    ): ...

class EmailField(CharField): ...

class RegexField(CharField):
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
        style: Optional[Dict[str, Any]] = ...,
        error_messages: Optional[Dict[str, str]] = ...,
        validators: Optional[Sequence[Callable]] = ...,
        allow_null: bool = ...,
        allow_blank: bool = ...,
        trim_whitespace: bool = ...,
        max_length: Optional[int] = ...,
        min_length: Optional[int] = ...,
        regex: Union[str, Pattern] = ...,
    ): ...

class SlugField(CharField):
    allow_unicode: bool = ...
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
        style: Optional[Dict[str, Any]] = ...,
        error_messages: Optional[Dict[str, str]] = ...,
        validators: Optional[Sequence[Callable]] = ...,
        allow_null: bool = ...,
        allow_blank: bool = ...,
        trim_whitespace: bool = ...,
        max_length: Optional[int] = ...,
        min_length: Optional[int] = ...,
        allow_unicode: bool = ...,
    ): ...

class URLField(CharField): ...

class UUIDField(Field):
    _pyi_field_actual_type: uuid.UUID
    _pyi_field_primitive_type: str
    valid_formats: Sequence[str] = ...
    uuid_format: str
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
        style: Optional[Dict[str, Any]] = ...,
        error_messages: Optional[Dict[str, str]] = ...,
        validators: Optional[Sequence[Callable]] = ...,
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
        default: Any = ...,
        initial: Any = ...,
        source: Union[Callable, str] = ...,
        label: Optional[str] = ...,
        help_text: Optional[str] = ...,
        style: Optional[Dict[str, Any]] = ...,
        error_messages: Optional[Dict[str, str]] = ...,
        validators: Optional[Sequence[Callable]] = ...,
        allow_null: bool = ...,
        allow_blank: bool = ...,
        trim_whitespace: bool = ...,
        max_length: Optional[int] = ...,
        min_length: Optional[int] = ...,
        protocol: str = ...,
    ): ...

class IntegerField(Field):
    _pyi_field_actual_type: int
    _pyi_field_primitive_type: int
    MAX_STRING_LENGTH: int = ...
    re_decimal: Pattern = ...
    max_value: Optional[int]
    min_value: Optional[int]
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
        style: Optional[Dict[str, Any]] = ...,
        error_messages: Optional[Dict[str, str]] = ...,
        validators: Optional[Sequence[Callable]] = ...,
        allow_null: bool = ...,
        max_value: Optional[int] = ...,
        min_value: Optional[int] = ...,
    ): ...

class FloatField(Field):
    _pyi_field_actual_type: float
    _pyi_field_primitive_type: float
    MAX_STRING_LENGTH: int = ...
    re_decimal: Pattern = ...
    max_value: Optional[int]
    min_value: Optional[int]
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
        style: Optional[Dict[str, Any]] = ...,
        error_messages: Optional[Dict[str, str]] = ...,
        validators: Optional[Sequence[Callable]] = ...,
        allow_null: bool = ...,
        max_value: Optional[int] = ...,
        min_value: Optional[int] = ...,
    ): ...

class DecimalField(Field):
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
        read_only: bool = ...,
        write_only: bool = ...,
        required: bool = ...,
        default: Any = ...,
        initial: Any = ...,
        source: Union[Callable, str] = ...,
        label: Optional[str] = ...,
        help_text: Optional[str] = ...,
        style: Optional[Dict[str, Any]] = ...,
        error_messages: Optional[Dict[str, str]] = ...,
        validators: Optional[Sequence[Callable]] = ...,
        allow_null: bool = ...,
        max_digits: Optional[int] = ...,
        decimal_places: Optional[int] = ...,
        coerce_to_string: Optional[bool] = ...,
        max_value: Optional[Union[Decimal, int, float]] = ...,
        min_value: Optional[Union[Decimal, int, float]] = ...,
        localize: bool = ...,
        rounding: Optional[str] = ...,
    ): ...
    def validate_precision(self, value: decimal.Decimal) -> decimal.Decimal: ...
    def quantize(self, value: decimal.Decimal) -> decimal.Decimal: ...

class DateTimeField(Field):
    _pyi_field_actual_type: datetime.datetime
    _pyi_field_primitive_type: str
    datetime_parser: Callable[str, str, datetime.datetime] = ...
    format: Optional[str] = ...
    input_formats: Sequence[str] = ...
    timezone: datetime.tzinfo = ...
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
        style: Optional[Dict[str, Any]] = ...,
        error_messages: Optional[Dict[str, str]] = ...,
        validators: Optional[Sequence[Callable]] = ...,
        allow_null: bool = ...,
        format: Optional[str] = ...,
        input_formats: Optional[Sequence[str]] = ...,
        default_timezone: Optional[datetime.tzinfo] = ...,
    ): ...
    def enforce_timezone(self, value: datetime.datetime) -> datetime.datetime: ...
    def default_timezone(self) -> Optional[str]: ...

class DateField(Field):
    _pyi_field_actual_type: datetime.date
    _pyi_field_primitive_type: str
    datetime_parser: Callable[str, str, datetime.datetime] = ...
    format: Optional[str]
    input_formats: Sequence[str]
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
        style: Optional[Dict[str, Any]] = ...,
        error_messages: Optional[Dict[str, str]] = ...,
        validators: Optional[Sequence[Callable]] = ...,
        allow_null: bool = ...,
        format: Optional[str] = ...,
        input_formats: Optional[Sequence[str]] = ...,
    ): ...

class TimeField(Field):
    _pyi_field_actual_type: datetime.time
    _pyi_field_primitive_type: str
    datetime_parser: Callable[str, str, datetime.datetime] = ...
    format: Optional[str]
    input_formats: Sequence[str]
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
        style: Optional[Dict[str, Any]] = ...,
        error_messages: Optional[Dict[str, str]] = ...,
        validators: Optional[Sequence[Callable]] = ...,
        allow_null: bool = ...,
        format: Optional[str] = ...,
        input_formats: Optional[Sequence[str]] = ...,
    ): ...

class DurationField(Field):
    max_value: Optional[datetime.timedelta]
    min_value: Optional[datetime.timedelta]
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
        style: Optional[Dict[str, Any]] = ...,
        error_messages: Optional[Dict[str, str]] = ...,
        validators: Optional[Sequence[Callable]] = ...,
        allow_null: bool = ...,
        max_value: Optional[datetime.timedelta] = ...,
        min_value: Optional[datetime.timedelta] = ...,
    ): ...

# Choice types...
class ChoiceField(Field):
    html_cutoff: Optional[int] = ...
    html_cutoff_text: Optional[str] = ...
    allow_blank: bool
    grouped_choices: OrderedDict
    choice_strings_to_values: Dict[str, Any]
    _choices: OrderedDict
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
        style: Optional[Dict[str, Any]] = ...,
        error_messages: Optional[Dict[str, str]] = ...,
        validators: Optional[Sequence[Callable]] = ...,
        allow_null: bool = ...,
        choices: Sequence[Any] = ...,
        html_cutoff: Optional[int] = ...,
        html_cutoff_text: Optional[str] = ...,
        allow_blank: bool = ...,
    ): ...
    def iter_options(self) -> Iterable[Option]: ...
    def _get_choices(self) -> Dict[Any, Any]: ...
    def _set_choices(self, choices: Sequence[Any]) -> None: ...
    choices = property(_get_choices, _set_choices)

class MultipleChoiceField(ChoiceField):
    allow_empty: bool
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
        style: Optional[Dict[str, Any]] = ...,
        error_messages: Optional[Dict[str, str]] = ...,
        validators: Optional[Sequence[Callable]] = ...,
        allow_null: bool = ...,
        choices: Sequence[Any] = ...,
        html_cutoff: Optional[int] = ...,
        html_cutoff_text: Optional[str] = ...,
        allow_blank: bool = ...,
        allow_empty: bool = ...,
    ): ...

class FilePathField(ChoiceField):
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
        style: Optional[Dict[str, Any]] = ...,
        error_messages: Optional[Dict[str, str]] = ...,
        validators: Optional[Sequence[Callable]] = ...,
        allow_null: bool = ...,
        html_cutoff: Optional[int] = ...,
        html_cutoff_text: Optional[str] = ...,
        allow_blank: bool = ...,
        path: str = ...,
        match: Optional[str] = ...,
        recursive: bool = ...,
        allow_files: bool = ...,
        allow_folders: bool = ...,
    ): ...

class FileField(Field):
    max_length: Optional[int]
    allow_empty_file: bool
    use_url: bool
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
        style: Optional[Dict[str, Any]] = ...,
        error_messages: Optional[Dict[str, str]] = ...,
        validators: Optional[Sequence[Callable]] = ...,
        allow_null: bool = ...,
        max_length: Optional[int] = ...,
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
        default: Any = ...,
        initial: Any = ...,
        source: Union[Callable, str] = ...,
        label: Optional[str] = ...,
        help_text: Optional[str] = ...,
        style: Optional[Dict[str, Any]] = ...,
        error_messages: Optional[Dict[str, str]] = ...,
        validators: Optional[Sequence[Callable]] = ...,
        allow_null: bool = ...,
        max_length: Optional[int] = ...,
        allow_empty_file: bool = ...,
        use_url: bool = ...,
        _DjangoImageField: Type[SupportsToPython] = ...,
    ): ...

class _UnvalidatedField(Field): ...

class ListField(Field):
    child: Field = ...
    allow_empty: bool = ...
    max_length: Optional[int] = ...
    min_length: Optional[int] = ...
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
        style: Optional[Dict[str, Any]] = ...,
        error_messages: Optional[Dict[str, str]] = ...,
        validators: Optional[Sequence[Callable]] = ...,
        allow_null: bool = ...,
        child: Field = ...,
        allow_empty: bool = ...,
        max_length: Optional[int] = ...,
        min_length: Optional[int] = ...,
    ): ...
    def run_child_validation(self, data: Any) -> Any: ...

class DictField(Field):
    child: Field = ...
    allow_empty: bool = ...
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
        style: Optional[Dict[str, Any]] = ...,
        error_messages: Optional[Dict[str, str]] = ...,
        validators: Optional[Sequence[Callable]] = ...,
        allow_null: bool = ...,
        child: Field = ...,
        allow_empty: bool = ...,
    ): ...
    def run_child_validation(self, data: Any) -> Any: ...

class HStoreField(DictField):
    child: CharField = ...

class JSONField(Field):
    binary: bool = ...
    encoder: Optional[JSONEncoder] = ...
    decoder: Optional[JSONDecoder] = ...
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
        style: Optional[Dict[str, Any]] = ...,
        error_messages: Optional[Dict[str, str]] = ...,
        validators: Optional[Sequence[Callable]] = ...,
        allow_null: bool = ...,
        binary: bool = ...,
        encoder: Optional[JSONEncoder] = ...,
        decoder: Optional[JSONDecoder] = ...,
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
        source: Union[Callable, str] = ...,
        label: Optional[str] = ...,
        help_text: Optional[str] = ...,
        style: Optional[Dict[str, Any]] = ...,
        error_messages: Optional[Dict[str, str]] = ...,
        validators: Optional[Sequence[Callable]] = ...,
        allow_null: bool = ...,
        method_name: Optional[str] = ...,
    ): ...

class ModelField(Field):
    model_field: models.Field = ...
    max_length: Optional[int] = ...
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
        style: Optional[Dict[str, Any]] = ...,
        error_messages: Optional[Dict[str, str]] = ...,
        validators: Optional[Sequence[Callable]] = ...,
        allow_null: bool = ...,
        model_field: models.Field = ...,
    ): ...
