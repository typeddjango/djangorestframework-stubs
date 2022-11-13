from rest_framework.schemas import SchemaGenerator
from rest_framework.views import APIView

class SchemaView(APIView):
    _ignore_model_permissions: bool
    public: bool
    schema_generator: SchemaGenerator | None
