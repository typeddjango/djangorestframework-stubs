import datetime
from typing import Any, Union, Callable, Dict, NoReturn, Optional, List, TypeVar

_T = TypeVar('_T')

class Field(object):
    def __init__(self,
                 read_only: bool = ...,
                 write_only: bool = ...,
                 required: bool = ...,
                 default: Any = ...,
                 initial: Any = ...,
                 source: Union[Callable, str] = ...,
                 help_text: str = ...,
                 allow_null: bool = ...,
                 **kwargs): ...

    def bind(self, field_name: str, parent): ...

    def to_representation(self, value: Any) -> Any: ...

    def run_validation(self, data: Any = ...) -> Any: ...

    def to_internal_value(self, data: Any): ...

    def __get__(self, instance, owner) -> Any: ...

    def fail(self, key: str, **kwargs) -> NoReturn: ...




class CharField(Field):
    def __init__(self,
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
                 **kwargs): ...

    def __get__(self, instance, owner) -> str: ...

class RegexField(Field):
    def __init__(self,
                 regex: str,
                 read_only: bool = ...,
                 write_only: bool = ...,
                 required: bool = ...,
                 default: Any = ...,
                 initial: Any = ...,
                 source: Union[Callable, str] = ...,
                 help_text: str = ...,
                 allow_null: bool = ...,
                 **kwargs): ...

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
    def __init__(self,
                 choices: List[_T],
                 read_only: bool = ...,
                 write_only: bool = ...,
                 required: bool = ...,
                 default: Any = ...,
                 initial: Any = ...,
                 source: Union[Callable, str] = ...,
                 help_text: str = ...,
                 allow_null: bool = ...,
                 **kwargs): ...

    def __get__(self, instance, owner) -> _T: ...

class JSONField(Field):
    def __get__(self, instance, owner) -> Any: ...

class DateTimeField(Field):
    def __get__(self, instance, owner) -> datetime.datetime: ...

class FileField(Field):
    def __get__(self, instance, owner) -> Any: ...

class SerializerMethodField(Field):
    def __get__(self, instance, owner) -> Any: ...
