from typing import Iterable, List, Optional, Sequence, Union

from django.urls.resolvers import URLPattern, URLResolver

_AnyURL = Union[URLPattern, URLResolver]

def apply_suffix_patterns(
    urlpatterns: Iterable[_AnyURL],
    suffix_pattern: str,
    suffix_required: bool,
    suffix_route: Optional[str] = ...,
) -> List[Union[URLResolver, URLPattern]]: ...
def format_suffix_patterns(
    urlpatterns: Iterable[_AnyURL],
    suffix_required: bool = ...,
    allowed: Optional[Sequence[str]] = ...,
) -> List[Union[URLResolver, URLPattern]]: ...
