from typing import Iterable, List, Sequence

from django.urls.resolvers import URLPattern, URLResolver

_AnyURL = URLPattern | URLResolver

def apply_suffix_patterns(
    urlpatterns: Iterable[_AnyURL],
    suffix_pattern: str,
    suffix_required: bool,
    suffix_route: str | None = ...,
) -> List[URLResolver | URLPattern]: ...
def format_suffix_patterns(
    urlpatterns: Iterable[_AnyURL],
    suffix_required: bool = ...,
    allowed: Sequence[str] | None = ...,
) -> List[URLResolver | URLPattern]: ...
