from typing import Iterable, List, Optional, Pattern, Sequence, Union

from django.urls.resolvers import RoutePattern, URLPattern, URLResolver

def apply_suffix_patterns(
    urlpatterns: Iterable[Union[URLResolver, RoutePattern, URLPattern, Pattern]],
    suffix_pattern: Union[str, Pattern],
    suffix_required: bool,
    suffix_route: Optional[str] = ...,
) -> List[URLPattern]: ...
def format_suffix_patterns(
    urlpatterns: Iterable[Union[URLResolver, RoutePattern, URLPattern, Pattern]],
    suffix_required: bool = ...,
    allowed: Optional[Sequence[Union[URLPattern, Pattern, str]]] = ...,
) -> List[URLPattern]: ...
