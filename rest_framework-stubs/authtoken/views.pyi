from typing import Any

from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.serializers import Serializer, _ContextType
from rest_framework.views import APIView, AsView, GenericView
from typing_extensions import Self

class ObtainAuthToken(APIView):
    serializer_class: type[Serializer]
    def post(self, request: Request, *args: Any, **kwargs: Any) -> Response: ...
    def get_serializer_context(self) -> _ContextType[Self]: ...
    def get_serializer(self, *args: Any, **kwargs: Any) -> Serializer: ...

obtain_auth_token: AsView[GenericView]
