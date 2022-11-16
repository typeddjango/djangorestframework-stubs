from collections.abc import Iterable, Sequence
from typing_extensions import TypeAlias

from django.urls.resolvers import URLPattern, URLResolver

_AnyURL: TypeAlias = URLPattern | URLResolver

def apply_suffix_patterns(
    urlpatterns: Iterable[_AnyURL],
    suffix_pattern: str,
    suffix_required: bool,
    suffix_route: str | None = ...,
) -> list[URLResolver | URLPattern]: ...
def format_suffix_patterns(
    urlpatterns: Iterable[_AnyURL],
    suffix_required: bool = ...,
    allowed: Sequence[str] | None = ...,
) -> list[URLResolver | URLPattern]: ...
