from typing import Optional, Union, Pattern, List, Callable
from django.urls.resolvers import RoutePattern, URLPattern

def apply_suffix_patterns(
    urlpatterns: List[Union[URLResolve, RoutePattern, URLPattern, Pattern]],
    suffix_pattern: Union[str, Pattern],
    suffix_required: bool,
    suffix_route: Optional[str] = ...,
) -> List[URLPattern]: ...
def format_suffix_patterns(
    urlpatterns: List[URLPattern],
    suffix_required: bool = ...,
    allowed: Optional[List[Union[URLPattern, Pattern, str]]] = ...,
) -> List[URLPattern]: ...
