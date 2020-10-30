from typing import List, Optional, Pattern, Union

from django.urls.resolvers import RoutePattern, URLPattern, URLResolver

def apply_suffix_patterns(
    urlpatterns: List[Union[URLResolver, RoutePattern, URLPattern, Pattern]],
    suffix_pattern: Union[str, Pattern],
    suffix_required: bool,
    suffix_route: Optional[str] = ...,
) -> List[URLPattern]: ...
def format_suffix_patterns(
    urlpatterns: List[Union[URLResolver, RoutePattern, URLPattern, Pattern]],
    suffix_required: bool = ...,
    allowed: Optional[List[Union[URLPattern, Pattern, str]]] = ...,
) -> List[URLPattern]: ...
