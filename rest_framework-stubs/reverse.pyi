from typing import Any, Callable, Mapping, Optional, Sequence

from rest_framework.request import Request

def preserve_builtin_query_params(url: str, request: Optional[Request] = ...) -> str: ...
def reverse(
    viewname: str,
    args: Optional[Sequence[Any]] = ...,
    kwargs: Optional[Mapping[str, Any]] = ...,
    request: Optional[Request] = ...,
    format: Optional[str] = ...,
    **extra: Any
) -> str: ...
def _reverse(
    viewname: str,
    args: Optional[Sequence[Any]] = ...,
    kwargs: Optional[Mapping[str, Any]] = ...,
    request: Optional[Request] = ...,
    format: Optional[str] = ...,
    **extra: Any
) -> str: ...

reverse_lazy: Callable[..., str] = ...
