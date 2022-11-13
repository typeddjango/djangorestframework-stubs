from typing import Any, Callable, Mapping, Sequence

from django.http import HttpRequest

def preserve_builtin_query_params(url: str, request: HttpRequest | None = ...) -> str: ...
def reverse(
    viewname: str,
    args: Sequence[Any] | None = ...,
    kwargs: Mapping[str, Any] | None = ...,
    request: HttpRequest | None = ...,
    format: str | None = ...,
    **extra: Any
) -> str: ...
def _reverse(
    viewname: str,
    args: Sequence[Any] | None = ...,
    kwargs: Mapping[str, Any] | None = ...,
    request: HttpRequest | None = ...,
    format: str | None = ...,
    **extra: Any
) -> str: ...

reverse_lazy: Callable[..., str]
