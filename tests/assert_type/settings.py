from collections.abc import Callable, Sequence
from typing import Any, assert_type

from django.contrib.auth.models import User
from rest_framework import generics
from rest_framework.filters import BaseFilterBackend
from rest_framework.generics import BaseFilterProtocol
from rest_framework.negotiation import BaseContentNegotiation
from rest_framework.pagination import BasePagination
from rest_framework.renderers import BaseRenderer
from rest_framework.response import Response
from rest_framework.settings import api_settings
from rest_framework.views import APIView

# case: api_settings_import_strings_are_resolved
assert_type(api_settings.DEFAULT_RENDERER_CLASSES, Sequence[type[BaseRenderer]])
assert_type(api_settings.DEFAULT_FILTER_BACKENDS, Sequence[type[BaseFilterBackend | BaseFilterProtocol[Any]]])
assert_type(api_settings.DEFAULT_PAGINATION_CLASS, type[BasePagination] | None)
assert_type(api_settings.DEFAULT_CONTENT_NEGOTIATION_CLASS, type[BaseContentNegotiation])
assert_type(api_settings.EXCEPTION_HANDLER, Callable[[Exception, dict[str, Any]], Response | None])
assert_type(api_settings.VIEW_DESCRIPTION_FUNCTION, Callable[[APIView, bool], str])


# case: api_settings_defaults_as_view_attributes
class UserList(generics.ListAPIView[User]):
    filter_backends = api_settings.DEFAULT_FILTER_BACKENDS
    pagination_class = api_settings.DEFAULT_PAGINATION_CLASS
    renderer_classes = api_settings.DEFAULT_RENDERER_CLASSES
    parser_classes = api_settings.DEFAULT_PARSER_CLASSES
    authentication_classes = api_settings.DEFAULT_AUTHENTICATION_CLASSES
    permission_classes = api_settings.DEFAULT_PERMISSION_CLASSES
    throttle_classes = api_settings.DEFAULT_THROTTLE_CLASSES
    content_negotiation_class = api_settings.DEFAULT_CONTENT_NEGOTIATION_CLASS
    metadata_class = api_settings.DEFAULT_METADATA_CLASS
    versioning_class = api_settings.DEFAULT_VERSIONING_CLASS
