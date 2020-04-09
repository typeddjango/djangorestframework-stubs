import datetime
import decimal
import uuid
from decimal import Decimal
from json import JSONEncoder
from typing import (
    Any,
    Callable,
    Dict,
    List,
    NoReturn,
    Optional,
    Pattern,
    Sequence,
    Set,
    Tuple,
    TypeVar,
    Union,
    Iterable,
    Protocol,
    Type,
    Mapping,
    MutableMapping,
)

from django.contrib.auth.models import AnonymousUser, User
from django.core.exceptions import ValidationError
from django.db import models
from django.db.models import Model
from django.forms import FilePathField as DjangoFilePathField, ImageField as DjangoImageField
from rest_framework.serializers import BaseSerializer
from rest_framework.relations import Option

class empty: ...

def is_simple_callable(obj: Callable) -> bool: ...

class CreateOnlyDefault(object):
    def __init__(self, default: Any) -> None: ...
    def set_context(self, serializer_field: Field) -> None: ...
    def __call__(self) -> Any: ...

class CurrentUserDefault(object):
    def set_context(self, serializer_field: Field) -> None: ...
    def __call__(self) -> Union[AnonymousUser, User]: ...

class SkipField(Exception): ...

def set_value(dictionary: MutableMapping[str, Any], keys: Sequence[str], value: Any) -> None: ...
def get_error_detail(exc_info: ValidationError) -> Any: ...

_FT = TypeVar("_FT")  # Field Type
_FPT = TypeVar("_FPT")  # Field Primitive Type

_Validator = Callable[[Any], None]

class Field:
    default_error_messages: Dict[str, str] = ...
    default_validators: List[Callable] = ...
    default_empty_html: Any = ...
    initial: Optional[Any] = ...
    # TODO: add Generic/Plugin support for parent
    parent: Optional[Any]
    # From constructor
    read_only: bool
    write_only: bool
    required: bool
    default: Any
    source: Optional[Union[Callable, str]]
    label: Optional[str]
    help_text: Optional[str]
    validators: Optional[List[_Validator]]
    error_messages: Optional[Mapping[str, str]]
    style: Optional[Mapping[str, Any]]
    allow_null: bool
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
        style: Optional[Mapping[str, Any]] = ...,
        error_messages: Optional[Mapping[str, str]] = ...,
        validators: Optional[Sequence[_Validator]] = ...,
        allow_null: bool = ...,
    ): ...
    def bind(self, field_name: str, parent: BaseSerializer) -> None: ...
    def get_validators(self) -> List[Callable]: ...
    def get_initial(self) -> Any: ...
    def get_value(self, dictionary: Any) -> Any: ...
    def get_attribute(self, instance: Model) -> Optional[Any]: ...
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

class BooleanField(Field):
    TRUE_VALUES: Set[Any] = ...
    FALSE_VALUES: Set[Any] = ...
    NULL_VALUES: Set[Optional[Any]] = ...

class NullBooleanField(Field):
    TRUE_VALUES: Set[Any] = ...
    FALSE_VALUES: Set[Any] = ...
    NULL_VALUES: Set[Optional[Any]] = ...

class CharField(Field):
    _pyi_field_actual_type: str
    _pyi_field_primitive_type: str
    # From constructor
    allow_blank: bool
    trim_whitespace: bool
    max_length: Optional[int]
    min_length: Optional[int]
    def __init__(
        self,
        *,
        # **kwargs passed to Field:
        read_only: bool = ...,
        write_only: bool = ...,
        required: bool = ...,
        default: Any = ...,
        initial: Any = ...,
        source: Union[Callable, str] = ...,
        label: Optional[str] = ...,
        help_text: Optional[str] = ...,
        style: Optional[Mapping[str, Any]] = ...,
        error_messages: Optional[Mapping[str, str]] = ...,
        validators: Optional[Sequence[_Validator]] = ...,
        allow_null: bool = ...,
        # kwargs.pop() in CharField
        allow_blank: bool = ...,
        trim_whitespace: bool = ...,
        max_length: Optional[int] = ...,
        min_length: Optional[int] = ...,
    ): ...

class EmailField(CharField): ...

class RegexField(CharField):
    def __init__(
        self,
        regex: Union[str, Pattern],
        *,
        # **kwargs passed to CharField
        allow_blank: bool = ...,
        trim_whitespace: bool = ...,
        max_length: Optional[int] = ...,
        min_length: Optional[int] = ...,
        # **kwargs passed to Field:
        read_only: bool = ...,
        write_only: bool = ...,
        required: bool = ...,
        default: Any = ...,
        initial: Any = ...,
        source: Union[Callable, str] = ...,
        label: Optional[str] = ...,
        help_text: Optional[str] = ...,
        style: Optional[Mapping[str, Any]] = ...,
        error_messages: Optional[Mapping[str, str]] = ...,
        validators: Optional[Sequence[_Validator]] = ...,
        allow_null: bool = ...,
    ): ...

class SlugField(CharField):
    # From constructor
    allow_unicode: bool
    def __init__(
        self,
        allow_unicode: bool = ...,
        *,
        # **kwargs passed to CharField
        allow_blank: bool = ...,
        trim_whitespace: bool = ...,
        max_length: Optional[int] = ...,
        min_length: Optional[int] = ...,
        # **kwargs passed to Field:
        read_only: bool = ...,
        write_only: bool = ...,
        required: bool = ...,
        default: Any = ...,
        initial: Any = ...,
        source: Union[Callable, str] = ...,
        label: Optional[str] = ...,
        help_text: Optional[str] = ...,
        style: Optional[Mapping[str, Any]] = ...,
        error_messages: Optional[Mapping[str, str]] = ...,
        validators: Optional[Sequence[_Validator]] = ...,
        allow_null: bool = ...,
    ): ...

class URLField(CharField): ...

class UUIDField(Field):
    _pyi_field_actual_type: uuid.UUID
    _pyi_field_primitive_type: str

    valid_formats: Sequence[str] = ...
    # From constructor
    uuid_format: str
    def __init__(
        self,
        *,
        # kwargs.pop() in UUIDField:
        format: str = ...,
        # **kwargs passed to Field:
        read_only: bool = ...,
        write_only: bool = ...,
        required: bool = ...,
        default: Any = ...,
        initial: Any = ...,
        source: Union[Callable, str] = ...,
        label: Optional[str] = ...,
        help_text: Optional[str] = ...,
        style: Optional[Mapping[str, Any]] = ...,
        error_messages: Optional[Mapping[str, str]] = ...,
        validators: Optional[Sequence[_Validator]] = ...,
        allow_null: bool = ...,
    ): ...

class IPAddressField(CharField):
    # From constructor
    protocol: str
    unpack_ipv4: bool
    def __init__(
        self,
        protocol: str = ...,
        *,
        # **kwargs passed to CharField
        allow_blank: bool = ...,
        trim_whitespace: bool = ...,
        max_length: Optional[int] = ...,
        min_length: Optional[int] = ...,
        # **kwargs passed to Field:
        read_only: bool = ...,
        write_only: bool = ...,
        required: bool = ...,
        default: Any = ...,
        initial: Any = ...,
        source: Union[Callable, str] = ...,
        label: Optional[str] = ...,
        help_text: Optional[str] = ...,
        style: Optional[Mapping[str, Any]] = ...,
        error_messages: Optional[Mapping[str, str]] = ...,
        validators: Optional[Sequence[_Validator]] = ...,
        allow_null: bool = ...,
    ): ...

class IntegerField(Field):
    _pyi_field_actual_type: int
    _pyi_field_primitive_type: int

    MAX_STRING_LENGTH: str = ...
    re_decimal: Pattern = ...
    # From constructor
    max_value: Optional[int]
    min_value: Optional[int]
    def __init__(
        self,
        *,
        # kwargs.pop() in IntegerField:
        max_value: Optional[int] = ...,
        min_value: Optional[int] = ...,
        # **kwargs passed to Field:
        read_only: bool = ...,
        write_only: bool = ...,
        required: bool = ...,
        default: Any = ...,
        initial: Any = ...,
        source: Union[Callable, str] = ...,
        label: Optional[str] = ...,
        help_text: Optional[str] = ...,
        style: Optional[Mapping[str, Any]] = ...,
        error_messages: Optional[Mapping[str, str]] = ...,
        validators: Optional[Sequence[_Validator]] = ...,
        allow_null: bool = ...,
    ): ...

class FloatField(Field):
    _pyi_field_actual_type: float
    _pyi_field_primitive_type: float
    MAX_STRING_LENGTH: int = ...
    # From constructor
    max_value: Optional[Union[float, int]] = ...
    min_value: Optional[Union[float, int]] = ...
    def __init__(
        self,
        *,
        # kwargs.pop() in FloatField:
        max_value: Optional[Union[float, int]] = ...,
        min_value: Optional[Union[float, int]] = ...,
        # **kwargs passed to Field:
        read_only: bool = ...,
        write_only: bool = ...,
        required: bool = ...,
        default: Any = ...,
        initial: Any = ...,
        source: Union[Callable, str] = ...,
        label: Optional[str] = ...,
        help_text: Optional[str] = ...,
        style: Optional[Mapping[str, Any]] = ...,
        error_messages: Optional[Mapping[str, str]] = ...,
        validators: Optional[Sequence[_Validator]] = ...,
        allow_null: bool = ...,
    ): ...

class DecimalField(Field):
    MAX_STRING_LENGTH: int = ...
    # From constructor
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
        coerce_to_string: Optional[bool] = ...,
        max_value: Optional[Union[Decimal, int, float]] = ...,
        min_value: Optional[Union[Decimal, int, float]] = ...,
        localize: bool = ...,
        rounding: Optional[str] = ...,
        *,
        # **kwargs passed to Field:
        read_only: bool = ...,
        write_only: bool = ...,
        required: bool = ...,
        default: Any = ...,
        initial: Any = ...,
        source: Union[Callable, str] = ...,
        label: Optional[str] = ...,
        help_text: Optional[str] = ...,
        style: Optional[Mapping[str, Any]] = ...,
        error_messages: Optional[Mapping[str, str]] = ...,
        validators: Optional[Sequence[_Validator]] = ...,
        allow_null: bool = ...,
    ): ...
    def validate_precision(self, value: decimal.Decimal) -> decimal.Decimal: ...
    def quantize(self, value: decimal.Decimal) -> decimal.Decimal: ...

class DateTimeField(Field):
    _pyi_field_actual_type: datetime.datetime
    _pyi_field_primitive_type: str
    # From constructor
    format: Optional[str]
    input_formats: Sequence[str]
    timezone: datetime.tzinfo
    @classmethod
    def datetime_parser(cls, date_string: str, format: str) -> datetime.datetime: ...
    def __init__(
        self,
        format: Optional[str] = ...,
        input_formats: Optional[Sequence[str]] = ...,
        default_timezone: Optional[datetime.tzinfo] = ...,
        # *args, **kwargs passed to Field:
        read_only: bool = ...,
        write_only: bool = ...,
        required: bool = ...,
        default: Any = ...,
        initial: Any = ...,
        source: Union[Callable, str] = ...,
        label: Optional[str] = ...,
        help_text: Optional[str] = ...,
        style: Optional[Mapping[str, Any]] = ...,
        error_messages: Optional[Mapping[str, str]] = ...,
        validators: Optional[Sequence[_Validator]] = ...,
        allow_null: bool = ...,
    ): ...
    def enforce_timezone(self, value: Any) -> Any: ...
    def default_timezone(self) -> Optional[str]: ...

class DateField(Field):
    _pyi_field_actual_type: datetime.date
    _pyi_field_primitive_type: str
    # From constructor
    format: Optional[str]
    input_formats: Sequence[str]
    @classmethod
    def datetime_parser(cls, date_string: str, format: str) -> datetime.datetime: ...
    def __init__(
        self,
        format: Optional[str] = ...,
        input_formats: Optional[Sequence[str]] = ...,
        # *args, **kwargs passed to Field:
        read_only: bool = ...,
        write_only: bool = ...,
        required: bool = ...,
        default: Any = ...,
        initial: Any = ...,
        source: Union[Callable, str] = ...,
        label: Optional[str] = ...,
        help_text: Optional[str] = ...,
        style: Optional[Mapping[str, Any]] = ...,
        error_messages: Optional[Mapping[str, str]] = ...,
        validators: Optional[Sequence[_Validator]] = ...,
        allow_null: bool = ...,
    ): ...

class TimeField(Field):
    _pyi_field_actual_type: datetime.time
    _pyi_field_primitive_type: str
    # From constructor
    format: Optional[str]
    input_formats: Sequence[str]
    @classmethod
    def datetime_parser(cls, date_string: str, format: str) -> datetime.datetime: ...
    def __init__(
        self,
        format: Optional[str] = ...,
        input_formats: Optional[Sequence[str]] = ...,
        # *args, **kwargs passed to Field:
        read_only: bool = ...,
        write_only: bool = ...,
        required: bool = ...,
        default: Any = ...,
        initial: Any = ...,
        source: Union[Callable, str] = ...,
        label: Optional[str] = ...,
        help_text: Optional[str] = ...,
        style: Optional[Mapping[str, Any]] = ...,
        error_messages: Optional[Mapping[str, str]] = ...,
        validators: Optional[Sequence[_Validator]] = ...,
        allow_null: bool = ...,
    ): ...

class DurationField(Field):
    # From constructor
    max_value: Optional[Any]
    min_value: Optional[Any]
    def __init__(
        self,
        *,
        # kwargs.pop() in DurationField:
        max_value: Optional[Any] = ...,
        min_value: Optional[Any] = ...,
        # **kwargs passed to Field:
        read_only: bool = ...,
        write_only: bool = ...,
        required: bool = ...,
        default: Any = ...,
        initial: Any = ...,
        source: Union[Callable, str] = ...,
        label: Optional[str] = ...,
        help_text: Optional[str] = ...,
        style: Optional[Mapping[str, Any]] = ...,
        error_messages: Optional[Mapping[str, str]] = ...,
        validators: Optional[Sequence[_Validator]] = ...,
        allow_null: bool = ...,
    ): ...

# Choice types...
class ChoiceField(Field):
    # From constructor
    _choices: Dict[Any, Any]
    html_cutoff: Optional[int] = ...
    html_cutoff_text: Optional[str] = ...
    allow_blank: bool
    grouped_choices: Dict[Any, Any]
    def __init__(
        self,
        choices: Sequence[Any],
        *,
        # kwargs.pop() in ChoiceField:
        html_cutoff: Optional[int] = ...,
        html_cutoff_text: Optional[str] = ...,
        allow_blank: bool = ...,
        # **kwargs passed to Field:
        read_only: bool = ...,
        write_only: bool = ...,
        required: bool = ...,
        default: Any = ...,
        initial: Any = ...,
        source: Union[Callable, str] = ...,
        label: Optional[str] = ...,
        help_text: Optional[str] = ...,
        style: Optional[Mapping[str, Any]] = ...,
        error_messages: Optional[Mapping[str, str]] = ...,
        validators: Optional[Sequence[_Validator]] = ...,
        allow_null: bool = ...,
    ): ...
    def iter_options(self) -> Iterable[Option]: ...
    def _get_choices(self) -> Dict[Any, Any]: ...
    def _set_choices(self, choices: Sequence[Any]) -> None: ...
    choices = property(_get_choices, _set_choices)

class MultipleChoiceField(ChoiceField):
    # From constructor
    allow_empty: bool
    def __init__(
        self,
        # *args, **kwargs passed to ChoiceField:
        choices: Sequence[Any],
        *,
        # kwargs.pop() in MultipleChoiceField:
        allow_empty: bool = ...,
        # kwargs.pop() in ChoiceField:
        html_cutoff: Optional[int] = ...,
        html_cutoff_text: Optional[str] = ...,
        allow_blank: bool = ...,
        # **kwargs passed to Field:
        read_only: bool = ...,
        write_only: bool = ...,
        required: bool = ...,
        default: Any = ...,
        initial: Any = ...,
        source: Union[Callable, str] = ...,
        label: Optional[str] = ...,
        help_text: Optional[str] = ...,
        style: Optional[Mapping[str, Any]] = ...,
        error_messages: Optional[Mapping[str, str]] = ...,
        validators: Optional[Sequence[_Validator]] = ...,
        allow_null: bool = ...,
    ): ...

class FilePathField(ChoiceField):
    def __init__(
        self,
        path: str = ...,
        match: Optional[str] = ...,
        recursive: bool = ...,
        allow_files: bool = ...,
        allow_folders: bool = ...,
        required: Optional[bool] = ...,
        *,
        # **kwargs passed to ChoiceField:
        # 'choices' is ignored (overwritten)
        html_cutoff: Optional[int] = ...,
        html_cutoff_text: Optional[str] = ...,
        allow_blank: bool = ...,
        # **kwargs passed to Field:
        read_only: bool = ...,
        write_only: bool = ...,
        # 'required' is not passed via **kwargs
        default: Any = ...,
        initial: Any = ...,
        source: Union[Callable, str] = ...,
        label: Optional[str] = ...,
        help_text: Optional[str] = ...,
        style: Optional[Mapping[str, Any]] = ...,
        error_messages: Optional[Mapping[str, str]] = ...,
        validators: Optional[Sequence[_Validator]] = ...,
        allow_null: bool = ...,
    ): ...

class FileField(Field):
    # From constructor
    max_length: Optional[int]
    allow_empty_file: bool
    use_url: bool
    def __init__(
        self,
        # *args, **kwargs passed to Field:
        read_only: bool = ...,
        write_only: bool = ...,
        required: bool = ...,
        default: Any = ...,
        initial: Any = ...,
        source: Union[Callable, str] = ...,
        label: Optional[str] = ...,
        help_text: Optional[str] = ...,
        style: Optional[Mapping[str, Any]] = ...,
        error_messages: Optional[Mapping[str, str]] = ...,
        validators: Optional[Sequence[_Validator]] = ...,
        allow_null: bool = ...,
        *,
        # kwargs.pop() in FileField
        max_length: Optional[int] = ...,
        allow_empty_file: bool = ...,
        use_url: bool = ...,
    ): ...

class SupportsToPython(Protocol):
    def to_python(self, value: Any) -> Any: ...

class ImageField(FileField):
    # From constructor
    _DjangoImageField: SupportsToPython
    def __init__(
        self,
        # *args, **kwargs passed to Field:
        read_only: bool = ...,
        write_only: bool = ...,
        required: bool = ...,
        default: Any = ...,
        initial: Any = ...,
        source: Union[Callable, str] = ...,
        label: Optional[str] = ...,
        help_text: Optional[str] = ...,
        style: Optional[Mapping[str, Any]] = ...,
        error_messages: Optional[Mapping[str, str]] = ...,
        validators: Optional[Sequence[_Validator]] = ...,
        allow_null: bool = ...,
        *,
        # kwargs.pop() in FileField:
        max_length: Optional[int] = ...,
        allow_empty_file: bool = ...,
        use_url: bool = ...,
        # kwargs.pop() in ImageField:
        _DjangoImageField: Type[SupportsToPython] = ...,
    ): ...

class _UnvalidatedField(Field): ...

class ListField(Field):
    # From constructor
    child: Field = ...
    allow_empty: bool = ...
    max_length: Optional[int] = ...
    min_length: Optional[int] = ...
    def __init__(
        self,
        # *args, **kwargs passed to Field:
        read_only: bool = ...,
        write_only: bool = ...,
        required: bool = ...,
        default: Any = ...,
        initial: Any = ...,
        source: Union[Callable, str] = ...,
        label: Optional[str] = ...,
        help_text: Optional[str] = ...,
        style: Optional[Mapping[str, Any]] = ...,
        error_messages: Optional[Mapping[str, str]] = ...,
        validators: Optional[Sequence[_Validator]] = ...,
        allow_null: bool = ...,
        *,
        # kwargs.pop() in ListField:
        child: Field = ...,
        allow_empty: bool = ...,
        max_length: Optional[int] = ...,
        min_length: Optional[int] = ...,
    ): ...
    def run_child_validation(self, data: Any) -> Any: ...

class DictField(Field):
    # From constructor
    child: Field = ...
    allow_empty: bool
    def __init__(
        self,
        # *args, **kwargs passed to Field:
        read_only: bool = ...,
        write_only: bool = ...,
        required: bool = ...,
        default: Any = ...,
        initial: Any = ...,
        source: Union[Callable, str] = ...,
        label: Optional[str] = ...,
        help_text: Optional[str] = ...,
        style: Optional[Mapping[str, Any]] = ...,
        error_messages: Optional[Mapping[str, str]] = ...,
        validators: Optional[Sequence[_Validator]] = ...,
        allow_null: bool = ...,
        *,
        # kwargs.pop() in DictField:
        child: Field = ...,
        allow_empty: bool = ...,
    ): ...
    def run_child_validation(self, data: Any) -> Any: ...

class HStoreField(DictField):
    child: CharField = ...

class JSONField(Field):
    # From constructor
    binary: bool
    encoder: Optional[JSONEncoder]
    def __init__(
        self,
        # *args, **kwargs passed to Field:
        read_only: bool = ...,
        write_only: bool = ...,
        required: bool = ...,
        default: Any = ...,
        initial: Any = ...,
        source: Union[Callable, str] = ...,
        label: Optional[str] = ...,
        help_text: Optional[str] = ...,
        style: Optional[Mapping[str, Any]] = ...,
        error_messages: Optional[Mapping[str, str]] = ...,
        validators: Optional[Sequence[_Validator]] = ...,
        allow_null: bool = ...,
        *,
        # kwargs.pop() in JSONField:
        binary: bool = ...,
        encoder: Optional[JSONEncoder] = ...,
    ): ...

class ReadOnlyField(Field): ...
class HiddenField(Field): ...

class SerializerMethodField(Field):
    # From constructor
    method_name: str
    def __init__(
        self,
        method_name: Optional[str] = ...,
        *,
        # **kwargs passed to Field:
        # 'read_only' is ignored (overwritten)
        write_only: bool = ...,
        required: bool = ...,
        default: Any = ...,
        initial: Any = ...,
        # 'source' is ignored (overwritten)
        label: Optional[str] = ...,
        help_text: Optional[str] = ...,
        style: Optional[Mapping[str, Any]] = ...,
        error_messages: Optional[Mapping[str, str]] = ...,
        validators: Optional[Sequence[_Validator]] = ...,
        allow_null: bool = ...,
    ): ...

class ModelField(Field):
    # From constructor
    model_field: models.Field
    max_length: Optional[int]
    def __init__(
        self,
        model_field: models.Field,
        *,
        # **kwargs passed to Field:
        read_only: bool = ...,
        write_only: bool = ...,
        required: bool = ...,
        default: Any = ...,
        initial: Any = ...,
        source: Union[Callable, str] = ...,
        label: Optional[str] = ...,
        help_text: Optional[str] = ...,
        style: Optional[Mapping[str, Any]] = ...,
        error_messages: Optional[Mapping[str, str]] = ...,
        validators: Optional[Sequence[_Validator]] = ...,
        allow_null: bool = ...,
    ): ...
