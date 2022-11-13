from typing import Any

from rest_framework import serializers
from rest_framework.request import Request
from rest_framework.serializers import BaseSerializer
from rest_framework.utils.field_mapping import ClassLookupDict
from rest_framework.views import APIView

class BaseMetadata:
    def determine_metadata(self, request: Request, view: APIView) -> dict[str, Any]: ...

class SimpleMetadata(BaseMetadata):
    label_lookup: ClassLookupDict[type[serializers.Field], str]
    def determine_actions(self, request: Request, view: APIView) -> dict[str, Any]: ...
    def get_serializer_info(self, serializer: BaseSerializer) -> dict[str, dict[str, Any]]: ...
    def get_field_info(self, field: serializers.Field) -> dict[str, Any]: ...
