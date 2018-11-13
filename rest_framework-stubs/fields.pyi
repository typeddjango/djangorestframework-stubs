from typing import Any, Union, Callable, Mapping, Dict


class Field(object):
    def __init__(self,
                 read_only: bool = ...,
                 write_only: bool = ...,
                 required: bool = ...,
                 default: Any = ...,
                 initial: Any = ...,
                 source: Union[Callable, str] = ...,
                 help_text: bool = ...,
                 allow_null: bool = ...,
                 **kwargs): ...

    def run_validation(self, data: Mapping[str, Any] = ...) -> Dict[str, Any]: ...

    def __get__(self, instance, owner) -> Any: ...


class CharField(Field):
    def __init__(self,
                 read_only: bool = ...,
                 write_only: bool = ...,
                 required: bool = ...,
                 default: Any = ...,
                 initial: Any = ...,
                 source: Union[Callable, str] = ...,
                 help_text: bool = ...,
                 allow_null: bool = ...,
                 allow_blank: bool = ...,
                 trim_whitespace: bool = ...,
                 min_length: int = ...,
                 max_length: int = ...,
                 **kwargs): ...

    def __get__(self, instance, owner) -> str: ...
