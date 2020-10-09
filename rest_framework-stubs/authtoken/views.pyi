from typing import Any

from rest_framework.authtoken.serializers import AuthTokenSerializer
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView, AsView

class ObtainAuthToken(APIView):
    serializer_class = AuthTokenSerializer
    def post(self, request: Request, *args: Any, **kwargs: Any) -> Response: ...

obtain_auth_token: AsView = ...
