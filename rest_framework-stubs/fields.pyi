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
    Mapping,
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

_FT = TypeVar("_FT")  # Field Type
_FPT = TypeVar("_FPT")  # Field Primitive Type

_Validator = Callable[[Any], None]

class Field(Generic[_FT, _FPT]):
    _pyi_field_actual_type: Any
    _pyi_field_primitive_type: Any

    default_error_messages: Dict[str, str] = ...
    default_validators: List[Callable] = ...
    default_empty_html: Any = ...
    initial: Optional[Any] = ...
    # TODO: add Generic/Plugin support for parent
    parent: Optional[Any]
    validators: Optional[List[_Validator]]
    def __init__(
        self,
        read_only: bool = ...,
        write_only: bool = ...,
        required: bool = ...,
        default: Any = ...,
        initial: Any = ...,
        source: Union[Callable, str] = ...,
        label: Optional[str] = ...,
        help_text: str = ...,
        allow_null: bool = ...,
        validators: Optional[Sequence[_Validator]] = ...,
        error_messages: Optional[Mapping[str, str]] = ...,
        style: Optional[Mapping[str, Any]] = ...,
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

class BooleanField(Field[_FT, _FPT]):
    _pyi_field_actual_type: bool
    _pyi_field_primitive_type: bool

    TRUE_VALUES: Set[Any] = ...
    FALSE_VALUES: Set[Any] = ...
    NULL_VALUES: Set[Optional[Any]] = ...

class NullBooleanField(Field[_FT, _FPT]):
    _pyi_field_actual_type: Optional[bool]
    _pyi_field_primitive_type: Optional[bool]

    TRUE_VALUES: Set[Any] = ...
    FALSE_VALUES: Set[Any] = ...
    NULL_VALUES: Set[Optional[Any]] = ...

class CharField(Field[_FT, _FPT]):
    _pyi_field_actual_type: str
    _pyi_field_primitive_type: str
    def __init__(
        self,
        read_only: bool = ...,
        write_only: bool = ...,
        required: bool = ...,
        default: Any = ...,
        initial: Any = ...,
        source: Union[Callable, str] = ...,
        label: Optional[str] = ...,
        help_text: str = ...,
        allow_null: bool = ...,
        allow_blank: bool = ...,
        trim_whitespace: bool = ...,
        min_length: int = ...,
        max_length: int = ...,
        validators: Optional[Sequence[_Validator]] = ...,
        error_messages: Optional[Mapping[str, str]] = ...,
        style: Optional[Mapping[str, Any]] = ...,
    ): ...

class EmailField(CharField[_FT, _FPT]): ...

class RegexField(CharField[_FT, _FPT]):
    def __init__(
        self,
        regex: Union[str, Pattern],
        read_only: bool = ...,
        write_only: bool = ...,
        required: bool = ...,
        default: Any = ...,
        initial: Any = ...,
        source: Union[Callable, str] = ...,
        label: Optional[str] = ...,
        help_text: str = ...,
        allow_null: bool = ...,
        allow_blank: bool = ...,
        trim_whitespace: bool = ...,
        min_length: int = ...,
        max_length: int = ...,
        validators: Optional[Sequence[_Validator]] = ...,
        error_messages: Optional[Mapping[str, str]] = ...,
        style: Optional[Mapping[str, Any]] = ...,
    ): ...

class SlugField(CharField[_FT, _FPT]):
    def __init__(
        self,
        allow_unicode: bool = ...,
        read_only: bool = ...,
        write_only: bool = ...,
        required: bool = ...,
        default: Any = ...,
        initial: Any = ...,
        source: Union[Callable, str] = ...,
        label: Optional[str] = ...,
        help_text: str = ...,
        allow_null: bool = ...,
        allow_blank: bool = ...,
        trim_whitespace: bool = ...,
        min_length: int = ...,
        max_length: int = ...,
        validators: Optional[Sequence[_Validator]] = ...,
        error_messages: Optional[Mapping[str, str]] = ...,
        style: Optional[Mapping[str, Any]] = ...,
    ): ...

class URLField(CharField[_FT, _FPT]): ...

class UUIDField(Field[_FT, _FPT]):
    _pyi_field_actual_type: uuid.UUID
    _pyi_field_primitive_type: str

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
        label: Optional[str] = ...,
        help_text: str = ...,
        allow_null: bool = ...,
        validators: Optional[Sequence[_Validator]] = ...,
        error_messages: Optional[Mapping[str, str]] = ...,
        style: Optional[Mapping[str, Any]] = ...,
    ): ...

class IPAddressField(CharField[_FT, _FPT]):
    def __init__(
        self,
        protocol: str = ...,
        read_only: bool = ...,
        write_only: bool = ...,
        required: bool = ...,
        default: Any = ...,
        initial: Any = ...,
        source: Union[Callable, str] = ...,
        label: Optional[str] = ...,
        help_text: str = ...,
        allow_null: bool = ...,
        allow_blank: bool = ...,
        trim_whitespace: bool = ...,
        min_length: int = ...,
        max_length: int = ...,
        validators: Optional[Sequence[_Validator]] = ...,
        error_messages: Optional[Mapping[str, str]] = ...,
        style: Optional[Mapping[str, Any]] = ...,
    ): ...

class IntegerField(Field[_FT, _FPT]):
    _pyi_field_actual_type: int
    _pyi_field_primitive_type: int

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
        label: Optional[str] = ...,
        help_text: str = ...,
        allow_null: bool = ...,
        validators: Optional[Sequence[_Validator]] = ...,
        error_messages: Optional[Mapping[str, str]] = ...,
        style: Optional[Mapping[str, Any]] = ...,
    ): ...

class FloatField(Field[_FT, _FPT]):
    _pyi_field_actual_type: float
    _pyi_field_primitive_type: float

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
        label: Optional[str] = ...,
        help_text: str = ...,
        allow_null: bool = ...,
        validators: Optional[Sequence[_Validator]] = ...,
        error_messages: Optional[Mapping[str, str]] = ...,
        style: Optional[Mapping[str, Any]] = ...,
    ): ...

class DecimalField(Field[_FT, _FPT]):
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
        label: Optional[str] = ...,
        help_text: str = ...,
        allow_null: bool = ...,
        validators: Optional[Sequence[_Validator]] = ...,
        error_messages: Optional[Mapping[str, str]] = ...,
        style: Optional[Mapping[str, Any]] = ...,
    ): ...
    def validate_precision(self, value: decimal.Decimal) -> decimal.Decimal: ...
    def quantize(self, value: decimal.Decimal) -> decimal.Decimal: ...

class DateTimeField(Field[_FT, _FPT]):
    _pyi_field_actual_type: datetime.datetime
    _pyi_field_primitive_type: str

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
        label: Optional[str] = ...,
        help_text: str = ...,
        allow_null: bool = ...,
        validators: Optional[Sequence[_Validator]] = ...,
        error_messages: Optional[Mapping[str, str]] = ...,
        style: Optional[Mapping[str, Any]] = ...,
    ): ...
    def enforce_timezone(self, value: Any) -> Any: ...
    def default_timezone(self) -> Optional[str]: ...

class DateField(Field[_FT, _FPT]):
    _pyi_field_actual_type: datetime.date
    _pyi_field_primitive_type: str

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
        label: Optional[str] = ...,
        help_text: str = ...,
        allow_null: bool = ...,
        validators: Optional[Sequence[_Validator]] = ...,
        error_messages: Optional[Mapping[str, str]] = ...,
        style: Optional[Mapping[str, Any]] = ...,
    ): ...

class TimeField(Field[_FT, _FPT]):
    _pyi_field_actual_type: datetime.time
    _pyi_field_primitive_type: str

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
        label: Optional[str] = ...,
        help_text: str = ...,
        allow_null: bool = ...,
        validators: Optional[Sequence[_Validator]] = ...,
        error_messages: Optional[Mapping[str, str]] = ...,
        style: Optional[Mapping[str, Any]] = ...,
    ): ...

class DurationField(Field[_FT, _FPT]):
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
        label: Optional[str] = ...,
        help_text: str = ...,
        allow_null: bool = ...,
        validators: Optional[Sequence[_Validator]] = ...,
        error_messages: Optional[Mapping[str, str]] = ...,
        style: Optional[Mapping[str, Any]] = ...,
    ): ...

# Choice types...

class ChoiceField(Field[_FT, _FPT]):
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
        label: Optional[str] = ...,
        help_text: str = ...,
        allow_null: bool = ...,
        validators: Optional[Sequence[_Validator]] = ...,
        error_messages: Optional[Mapping[str, str]] = ...,
        style: Optional[Mapping[str, Any]] = ...,
    ): ...
    def iter_options(self) -> Iterable[Option]: ...
    def _get_choices(self) -> Sequence[Any]: ...
    def _set_choices(self, choices: Sequence[Any]) -> None: ...

class MultipleChoiceField(ChoiceField[_FT, _FPT]):
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
        label: Optional[str] = ...,
        help_text: str = ...,
        allow_null: bool = ...,
        validators: Optional[Sequence[_Validator]] = ...,
        error_messages: Optional[Mapping[str, str]] = ...,
        style: Optional[Mapping[str, Any]] = ...,
    ): ...

class FilePathField(ChoiceField[_FT, _FPT]):
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
        label: Optional[str] = ...,
        help_text: str = ...,
        allow_null: bool = ...,
        validators: Optional[Sequence[_Validator]] = ...,
        error_messages: Optional[Mapping[str, str]] = ...,
        style: Optional[Mapping[str, Any]] = ...,
    ): ...

class FileField(Field[_FT, _FPT]):
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
        label: Optional[str] = ...,
        help_text: str = ...,
        allow_null: bool = ...,
        validators: Optional[Sequence[_Validator]] = ...,
        error_messages: Optional[Mapping[str, str]] = ...,
        style: Optional[Mapping[str, Any]] = ...,
    ): ...

class SupportsToPython(Protocol):
    def to_python(self, value: Any) -> Any: ...

class ImageField(FileField[_FT, _FPT]):
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
        label: Optional[str] = ...,
        help_text: str = ...,
        allow_null: bool = ...,
        validators: Optional[Sequence[_Validator]] = ...,
        error_messages: Optional[Mapping[str, str]] = ...,
        style: Optional[Mapping[str, Any]] = ...,
    ): ...

class _UnvalidatedField(Field[_FT, _FPT]): ...

class ListField(Field[_FT, _FPT]):
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
        label: Optional[str] = ...,
        help_text: str = ...,
        allow_null: bool = ...,
        validators: Optional[Sequence[_Validator]] = ...,
        error_messages: Optional[Mapping[str, str]] = ...,
        style: Optional[Mapping[str, Any]] = ...,
    ): ...
    def run_child_validation(self, data: Any) -> Any: ...

class DictField(Field[_FT, _FPT]):
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
        label: Optional[str] = ...,
        help_text: str = ...,
        allow_null: bool = ...,
        validators: Optional[Sequence[_Validator]] = ...,
        error_messages: Optional[Mapping[str, str]] = ...,
        style: Optional[Mapping[str, Any]] = ...,
    ): ...
    def run_child_validation(self, data: Any) -> Any: ...

class HStoreField(DictField[_FT, _FPT]):
    child: CharField = ...

class JSONField(Field[_FT, _FPT]):
    def __init__(
        self,
        binary: bool = ...,
        read_only: bool = ...,
        write_only: bool = ...,
        required: bool = ...,
        default: Any = ...,
        initial: Any = ...,
        source: Union[Callable, str] = ...,
        label: Optional[str] = ...,
        help_text: str = ...,
        allow_null: bool = ...,
        validators: Optional[Sequence[_Validator]] = ...,
        error_messages: Optional[Mapping[str, str]] = ...,
        style: Optional[Mapping[str, Any]] = ...,
    ): ...

class ReadOnlyField(Field[_FT, _FPT]): ...
class HiddenField(Field[_FT, _FPT]): ...

class SerializerMethodField(Field[_FT, _FPT]):
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
        label: Optional[str] = ...,
        help_text: str = ...,
        allow_null: bool = ...,
        validators: Optional[Sequence[_Validator]] = ...,
        error_messages: Optional[Mapping[str, str]] = ...,
        style: Optional[Mapping[str, Any]] = ...,
    ): ...

class ModelField(Field[_FT, _FPT]):
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
        label: Optional[str] = ...,
        help_text: str = ...,
        allow_null: bool = ...,
        validators: Optional[Sequence[_Validator]] = ...,
        error_messages: Optional[Mapping[str, str]] = ...,
        style: Optional[Mapping[str, Any]] = ...,
    ): ...
