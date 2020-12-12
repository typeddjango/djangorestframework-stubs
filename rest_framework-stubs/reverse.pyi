from typing import Any, Callable, Mapping, Optional, Sequence

from django.http import HttpRequest

def preserve_builtin_query_params(url: str, request: Optional[HttpRequest] = ...) -> str: ...
def reverse(
    viewname: str,
    args: Optional[Sequence[Any]] = ...,
    kwargs: Optional[Mapping[str, Any]] = ...,
    request: Optional[HttpRequest] = ...,
    format: Optional[str] = ...,
    **extra: Any
) -> str: ...
def _reverse(
    viewname: str,
    args: Optional[Sequence[Any]] = ...,
    kwargs: Optional[Mapping[str, Any]] = ...,
    request: Optional[HttpRequest] = ...,
    format: Optional[str] = ...,
    **extra: Any
) -> str: ...

reverse_lazy: Callable[..., str] = ...
