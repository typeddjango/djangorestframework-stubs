import datetime
from typing import Any, Union, Callable, Dict, NoReturn, Optional, List, TypeVar, Tuple, Generic

from django.db.models import Model
from rest_framework.serializers import BaseSerializer

_FT = TypeVar("_FT")

class Field(Generic[_FT]):
    _pyi_private_field_type: Any

    default_error_messages: Dict[str, str] = ...
    default_validators: List[Callable] = ...
    default_empty_html: Any = ...
    initial: Optional[Any] = ...
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

class RegexField(Field):
    _pyi_private_field_type: str
    def __init__(
        self,
        regex: str,
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

class EmailField(Field):
    _pyi_private_field_type: str

class URLField(Field):
    _pyi_private_field_type: str

class IntegerField(Field):
    _pyi_private_field_type: int

class FloatField(Field):
    _pyi_private_field_type: float

class BooleanField(Field):
    _pyi_private_field_type: bool

class NullBooleanField(Field):
    _pyi_private_field_type: Optional[bool]

class ListField(Field):
    _pyi_private_field_type: List[Any]

class DictField(Field):
    _pyi_private_field_type: Dict[str, Any]
    def run_child_validation(self, data: Dict[str, Any]) -> Dict[str, Any]: ...

class ChoiceField(Field):
    def __init__(
        self,
        choices: List[Any],
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

class JSONField(Field): ...

class DateTimeField(Field):
    _pyi_private_field_type: datetime.datetime

class FileField(Field): ...
class HiddenField(Field): ...
class SerializerMethodField(Field): ...
