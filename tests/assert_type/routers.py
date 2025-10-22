from django.urls import URLPattern, URLResolver, include, path
from rest_framework.routers import DefaultRouter, SimpleRouter
from rest_framework.urlpatterns import _AnyURL
from typing_extensions import assert_type

# case: test_router_urls
simple = SimpleRouter()
assert_type(simple.urls, list[URLPattern | URLResolver])

default = DefaultRouter()
assert_type(default.urls, list[URLPattern | URLResolver])

urlpatterns: list[_AnyURL] = [
    path("api/", include(simple.urls)),
    path("api/", include((simple.urls, "app_name"), namespace="instance_name")),
    path("default/", include(default.urls)),
]
