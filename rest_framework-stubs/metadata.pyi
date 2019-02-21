from typing import Any, Dict, Type

from rest_framework.request import Request
from rest_framework.serializers import BaseSerializer
from rest_framework.utils.field_mapping import ClassLookupDict
from rest_framework.views import APIView

from rest_framework import serializers

class BaseMetadata(object):
    def determine_metadata(self, request: Request, view: APIView) -> Dict[str, Any]: ...

class SimpleMetadata(BaseMetadata):
    label_lookup: ClassLookupDict[Type[serializers.Field], str]
    def determine_actions(self, request: Request, view: APIView) -> Dict[str, Any]: ...
    def get_serializer_info(self, serializer: BaseSerializer) -> Dict[str, Dict[str, Any]]: ...
    def get_field_info(self, field: serializers.Field) -> Dict[str, Any]: ...
