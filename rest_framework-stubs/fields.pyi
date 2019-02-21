import datetime
import decimal
import uuid
from typing import (
    Any,
    Callable,
    Dict,
    Generic,
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
)

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

class SkipField(Exception): ...

_FT = TypeVar("_FT")

class Field(Generic[_FT]):
    _pyi_private_field_get_type: Any

    default_error_messages: Dict[str, str] = ...
    default_validators: List[Callable] = ...
    default_empty_html: Any = ...
    initial: Optional[Any] = ...

    read_only: bool
    write_only: bool
    required: bool
    default: Any
    label: str
    help_text: Optional[str]
    style: Dict[str, Any]
    allow_null: bool
    field_name: Optional[str]
    parent: Optional[Field]
    def __init__(
        self,
        read_only: bool = ...,
        write_only: bool = ...,
        required: bool = ...,
        default: Any = ...,
        initial: Any = ...,
        source: Union[Callable, str] = ...,
        help_text: str = ...,
        allow_null: bool = ...,
        **kwargs
    ): ...
    def bind(self, field_name: str, parent: BaseSerializer) -> None: ...
    @property
    def validators(self) -> List[Callable]: ...
    @validators.setter
    def validators(self, validators: List[Callable]) -> None: ...
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
    def __get__(self, instance, owner) -> _FT: ...

class BooleanField(Field):
    _pyi_private_field_type: bool

    TRUE_VALUES: Set[Any] = ...
    FALSE_VALUES: Set[Any] = ...
    NULL_VALUES: Set[Optional[Any]] = ...

class NullBooleanField(Field):
    _pyi_private_field_type: Optional[bool]

    TRUE_VALUES: Set[Any] = ...
    FALSE_VALUES: Set[Any] = ...
    NULL_VALUES: Set[Optional[Any]] = ...

class CharField(Field):
    _pyi_private_field_type: str
    def __init__(
        self,
        read_only: bool = ...,
        write_only: bool = ...,
        required: bool = ...,
        default: Any = ...,
        initial: Any = ...,
        source: Union[Callable, str] = ...,
        help_text: str = ...,
        allow_null: bool = ...,
        allow_blank: bool = ...,
        trim_whitespace: bool = ...,
        min_length: int = ...,
        max_length: int = ...,
        **kwargs
    ): ...

class EmailField(CharField): ...

class RegexField(CharField):
    def __init__(
        self,
        regex: Union[str, Pattern],
        read_only: bool = ...,
        write_only: bool = ...,
        required: bool = ...,
        default: Any = ...,
        initial: Any = ...,
        source: Union[Callable, str] = ...,
        help_text: str = ...,
        allow_null: bool = ...,
        **kwargs
    ): ...

class SlugField(CharField):
    def __init__(
        self,
        allow_unicode: bool = ...,
        read_only: bool = ...,
        write_only: bool = ...,
        required: bool = ...,
        default: Any = ...,
        initial: Any = ...,
        source: Union[Callable, str] = ...,
        help_text: str = ...,
        allow_null: bool = ...,
        allow_blank: bool = ...,
        trim_whitespace: bool = ...,
        min_length: int = ...,
        max_length: int = ...,
        **kwargs
    ): ...

class URLField(CharField): ...

class UUIDField(Field):
    _pyi_private_field_get_type: uuid.UUID
    valid_formats: Sequence[str] = ...
    def __init__(
        self,
        format: str = ...,
        read_only: bool = ...,
        write_only: bool = ...,
        required: bool = ...,
        default: Any = ...,
        initial: Any = ...,
        source: Union[Callable, str] = ...,
        help_text: str = ...,
        allow_null: bool = ...,
        **kwargs
    ): ...

class IPAddressField(CharField):
    def __init__(
        self,
        protocol: str = ...,
        read_only: bool = ...,
        write_only: bool = ...,
        required: bool = ...,
        default: Any = ...,
        initial: Any = ...,
        source: Union[Callable, str] = ...,
        help_text: str = ...,
        allow_null: bool = ...,
        allow_blank: bool = ...,
        trim_whitespace: bool = ...,
        min_length: int = ...,
        max_length: int = ...,
        **kwargs
    ): ...

class IntegerField(Field):
    _pyi_private_field_get_type: int

    MAX_STRING_LENGTH: str = ...
    re_decimal: Pattern = ...
    def __init__(
        self,
        min_value: int = ...,
        max_value: int = ...,
        read_only: bool = ...,
        write_only: bool = ...,
        required: bool = ...,
        default: Any = ...,
        initial: Any = ...,
        source: Union[Callable, str] = ...,
        help_text: str = ...,
        allow_null: bool = ...,
        **kwargs
    ): ...

class FloatField(Field):
    _pyi_private_field_get_type: float

    MAX_STRING_LENGTH: int = ...
    def __init__(
        self,
        min_value: float = ...,
        max_value: float = ...,
        read_only: bool = ...,
        write_only: bool = ...,
        required: bool = ...,
        default: Any = ...,
        initial: Any = ...,
        source: Union[Callable, str] = ...,
        help_text: str = ...,
        allow_null: bool = ...,
        **kwargs
    ): ...

class DecimalField(Field):
    MAX_STRING_LENGTH: int = ...
    def __init__(
        self,
        max_digits: Optional[int],
        decimal_places: Optional[int],
        coerce_to_string: Optional[bool] = ...,
        max_value: Optional[Any] = ...,
        min_value: Optional[Any] = ...,
        localize: bool = ...,
        rounding: Optional[str] = ...,
        read_only: bool = ...,
        write_only: bool = ...,
        required: bool = ...,
        default: Any = ...,
        initial: Any = ...,
        source: Union[Callable, str] = ...,
        help_text: str = ...,
        allow_null: bool = ...,
        **kwargs
    ): ...
    def validate_precision(self, value: decimal.Decimal) -> decimal.Decimal: ...
    def quantize(self, value: decimal.Decimal) -> decimal.Decimal: ...

class DateTimeField(Field):
    _pyi_private_field_get_type: datetime.datetime

    datetime_parser: Callable = ...
    def __init__(
        self,
        format: Optional[str] = ...,
        input_formats: Optional[Sequence[str]] = ...,
        default_timezone: Optional[Union[str, datetime.tzinfo]] = ...,
        *args,
        read_only: bool = ...,
        write_only: bool = ...,
        required: bool = ...,
        default: Any = ...,
        initial: Any = ...,
        source: Union[Callable, str] = ...,
        help_text: str = ...,
        allow_null: bool = ...,
        **kwargs
    ): ...
    def enforce_timezone(self, value: Any) -> Any: ...
    def default_timezone(self) -> Optional[str]: ...

class DateField(Field):
    _pyi_private_field_get_type: datetime.date

    datetime_parser: Callable = ...
    def __init__(
        self,
        format: Optional[str] = ...,
        input_formats: Optional[Sequence[str]] = ...,
        read_only: bool = ...,
        write_only: bool = ...,
        required: bool = ...,
        default: Any = ...,
        initial: Any = ...,
        source: Union[Callable, str] = ...,
        help_text: str = ...,
        allow_null: bool = ...,
        **kwargs
    ): ...

class TimeField(Field):
    _pyi_private_field_get_type: datetime.time

    datetime_parser: Callable = ...
    def __init__(
        self,
        format: Optional[str] = ...,
        input_formats: Optional[Sequence[str]] = ...,
        read_only: bool = ...,
        write_only: bool = ...,
        required: bool = ...,
        default: Any = ...,
        initial: Any = ...,
        source: Union[Callable, str] = ...,
        help_text: str = ...,
        allow_null: bool = ...,
        **kwargs
    ): ...

class DurationField(Field):
    max_value: Any
    min_value: Any
    def __init__(
        self,
        max_value: object = ...,
        min_value: object = ...,
        read_only: bool = ...,
        write_only: bool = ...,
        required: bool = ...,
        default: Any = ...,
        initial: Any = ...,
        source: Union[Callable, str] = ...,
        help_text: str = ...,
        allow_null: bool = ...,
        **kwargs
    ): ...

# Choice types...

class ChoiceField(Field):
    choices: Sequence[Any]
    html_cutoff: Optional[int] = ...
    html_cutoff_text: Optional[str] = ...
    def __init__(
        self,
        choices: Sequence[Any],
        html_cutoff: Optional[int] = ...,
        html_cutoff_text: Optional[str] = ...,
        allow_blank: bool = ...,
        read_only: bool = ...,
        write_only: bool = ...,
        required: bool = ...,
        default: Any = ...,
        initial: Any = ...,
        source: Union[Callable, str] = ...,
        help_text: str = ...,
        allow_null: bool = ...,
        **kwargs
    ): ...
    def iter_options(self) -> Iterable[Option]: ...
    def _get_choices(self) -> Sequence[Any]: ...
    def _set_choices(self, choices: Sequence[Any]) -> None: ...

class MultipleChoiceField(ChoiceField):
    def __init__(
        self,
        choices: Sequence[Any],
        html_cutoff: Optional[int] = ...,
        html_cutoff_text: Optional[str] = ...,
        allow_blank: bool = ...,
        allow_empty: bool = ...,
        read_only: bool = ...,
        write_only: bool = ...,
        required: bool = ...,
        default: Any = ...,
        initial: Any = ...,
        source: Union[Callable, str] = ...,
        help_text: str = ...,
        allow_null: bool = ...,
        **kwargs
    ): ...

class FilePathField(ChoiceField):
    def __init__(
        self,
        path: str = ...,
        match: Optional[str] = ...,
        choices: Sequence[Any] = ...,
        recursive: bool = ...,
        allow_files: bool = ...,
        allow_folders: bool = ...,
        read_only: bool = ...,
        write_only: bool = ...,
        required: Optional[bool] = ...,
        default: Any = ...,
        initial: Any = ...,
        source: Union[Callable, str] = ...,
        help_text: str = ...,
        allow_null: bool = ...,
        **kwargs
    ): ...

class FileField(Field):
    max_length: int
    allow_empty_file: bool
    def __init__(
        self,
        allow_empty_file: bool = ...,
        max_length: int = ...,
        use_url: bool = ...,
        read_only: bool = ...,
        write_only: bool = ...,
        required: bool = ...,
        default: Any = ...,
        initial: Any = ...,
        source: Union[Callable, str] = ...,
        help_text: str = ...,
        allow_null: bool = ...,
        **kwargs
    ): ...

class SupportsToPython(Protocol):
    def to_python(self, value: Any) -> Any: ...

class ImageField(FileField):
    _DjangoImageField: SupportsToPython
    def __init__(
        self,
        _DjangoImageField: Type[SupportsToPython] = ...,
        allow_empty: bool = ...,
        max_length: int = ...,
        min_length: int = ...,
        read_only: bool = ...,
        write_only: bool = ...,
        required: bool = ...,
        default: Any = ...,
        initial: Any = ...,
        source: Union[Callable, str] = ...,
        help_text: str = ...,
        allow_null: bool = ...,
        **kwargs
    ): ...

class _UnvalidatedField(Field): ...

class ListField(Field):
    child: Field = ...
    allow_empty: bool = ...
    max_length: int = ...
    min_length: int = ...
    def __init__(
        self,
        child: Field = ...,
        allow_empty: bool = ...,
        max_length: int = ...,
        min_length: int = ...,
        read_only: bool = ...,
        write_only: bool = ...,
        required: bool = ...,
        default: Any = ...,
        initial: Any = ...,
        source: Union[Callable, str] = ...,
        help_text: str = ...,
        allow_null: bool = ...,
        **kwargs
    ): ...
    def run_child_validation(self, data: Any) -> Any: ...

class DictField(Field):
    child: Field = ...
    def __init__(
        self,
        child: Field = ...,
        read_only: bool = ...,
        write_only: bool = ...,
        required: bool = ...,
        default: Any = ...,
        initial: Any = ...,
        source: Union[Callable, str] = ...,
        help_text: str = ...,
        allow_null: bool = ...,
        **kwargs
    ): ...
    def run_child_validation(self, data: Any) -> Any: ...

class HStoreField(DictField):
    child: CharField = ...

class JSONField(Field):
    def __init__(
        self,
        binary: bool = ...,
        read_only: bool = ...,
        write_only: bool = ...,
        required: bool = ...,
        default: Any = ...,
        initial: Any = ...,
        source: Union[Callable, str] = ...,
        help_text: str = ...,
        allow_null: bool = ...,
        **kwargs
    ): ...

class ReadOnlyField(Field): ...
class HiddenField(Field): ...

class SerializerMethodField(Field):
    method_name: str
    def __init__(
        self,
        method_name: Optional[str] = ...,
        read_only: bool = ...,
        write_only: bool = ...,
        required: bool = ...,
        default: Any = ...,
        initial: Any = ...,
        source: Union[Callable, str] = ...,
        help_text: str = ...,
        allow_null: bool = ...,
        **kwargs
    ): ...

class ModelField(Field):
    model_field: models.Field
    def __init__(
        self,
        model_field: models.Field,
        max_length: int = ...,
        read_only: bool = ...,
        write_only: bool = ...,
        required: bool = ...,
        default: Any = ...,
        initial: Any = ...,
        source: Union[Callable, str] = ...,
        help_text: str = ...,
        allow_null: bool = ...,
        **kwargs
    ): ...
