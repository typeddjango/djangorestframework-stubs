from typing import Any

from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.schemas import SchemaGenerator
from rest_framework.views import APIView

class SchemaView(APIView):
    _ignore_model_permissions: bool
    public: bool
    schema_generator: SchemaGenerator | None

    def get(self, request: Request, *args: Any, **kwargs: Any) -> Response: ...
