from typing import List, Union

from django.urls import URLPattern, URLResolver

app_name: str
urlpatterns: List[Union[URLPattern, URLResolver]]
