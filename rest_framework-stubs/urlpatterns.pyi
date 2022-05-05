from typing import List, Optional, Sequence, Union

from django.urls.resolvers import URLPattern, URLResolver

def apply_suffix_patterns(
    urlpatterns: Sequence[Union[URLResolver, URLPattern]],
    suffix_pattern: str,
    suffix_required: bool,
    suffix_route: Optional[str] = ...,
) -> List[Union[URLResolver, URLPattern]]: ...
def format_suffix_patterns(
    urlpatterns: Sequence[Union[URLResolver, URLPattern]],
    suffix_required: bool = ...,
    allowed: Optional[Sequence[str]] = ...,
) -> List[Union[URLResolver, URLPattern]]: ...
