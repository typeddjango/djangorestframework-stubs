import datetime
from typing import Any, Union, Callable, Dict, NoReturn, Optional, List, TypeVar, Tuple

from django.db.models import Model
from rest_framework.serializers import BaseSerializer

_T = TypeVar("_T")

class Field(object):
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
    # .validators is a lazily loaded property, that gets its default
    # value from `get_validators`.
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

class CharField(Field):
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
    def __get__(self, instance, owner) -> str: ...

class RegexField(Field):
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
    def __get__(self, instance, owner) -> str: ...

class EmailField(Field):
    def __get__(self, instance, owner) -> str: ...

class URLField(Field):
    def __get__(self, instance, owner) -> str: ...

class IntegerField(Field):
    def __get__(self, instance, owner) -> int: ...

class FloatField(Field):
    def __get__(self, instance, owner) -> float: ...

class BooleanField(Field):
    def __get__(self, instance, owner) -> bool: ...

class NullBooleanField(Field):
    def __get__(self, instance, owner) -> Optional[bool]: ...

class ListField(Field):
    def __get__(self, instance, owner) -> List[Any]: ...

class DictField(Field):
    def __get__(self, instance, owner) -> Dict[str, Any]: ...
    def run_child_validation(self, data: Dict[str, Any]) -> Dict[str, Any]: ...

class ChoiceField(Field):
    def __init__(
        self,
        choices: List[_T],
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
    def __get__(self, instance, owner) -> _T: ...

class JSONField(Field):
    def __get__(self, instance, owner) -> Any: ...

class DateTimeField(Field):
    def __get__(self, instance, owner) -> datetime.datetime: ...

class FileField(Field):
    def __get__(self, instance, owner) -> Any: ...

class HiddenField(Field): ...

class SerializerMethodField(Field):
    def __get__(self, instance, owner) -> Any: ...
