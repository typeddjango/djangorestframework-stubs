from typing import Optional

from rest_framework.views import APIView

from rest_framework.schemas import SchemaGenerator

class SchemaView(APIView):
    _ignore_model_permissions: bool = ...
    public: bool = ...
    schema_generator: Optional[SchemaGenerator] = ...
