import datetime
from typing import Any, Union, Callable, Mapping, Dict, NoReturn, Optional, List


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

    def run_validation(self, data: Mapping[str, Any] = ...) -> Dict[str, Any]: ...

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
    def __get__(self, instance, owner) -> str: ...

class EmailField(Field):
    def __get__(self, instance, owner) -> str: ...

class IntegerField(Field):
    def __get__(self, instance, owner) -> int: ...

class BooleanField(Field):
    def __get__(self, instance, owner) -> bool: ...

class NullBooleanField(Field):
    def __get__(self, instance, owner) -> Optional[bool]: ...

class ListField(Field):
    def __get__(self, instance, owner) -> List[Any]: ...

class DictField(Field):
    def __get__(self, instance, owner) -> Dict[str, Any]: ...

class ChoiceField(Field):
    def __get__(self, instance, owner) -> Any: ...

class JSONField(Field):
    def __get__(self, instance, owner) -> Any: ...

class DateTimeField(Field):
    def __get__(self, instance, owner) -> datetime.datetime: ...
