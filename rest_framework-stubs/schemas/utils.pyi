from typing import Type

from django.db.models import Model
from rest_framework.fields import Field
from rest_framework.views import APIView

def is_list_view(path: str, method: str, view: APIView) -> bool: ...
def get_pk_description(model: Type[Model], model_field: Field) -> str: ...
