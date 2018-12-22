from typing import Dict

from rest_framework.fields import (
    Field as Field,
    CharField as CharField,
    RegexField as RegexField,
    EmailField as EmailField,
    URLField as URLField,
    FileField as FileField,
    IntegerField as IntegerField,
    FloatField as FloatField,
    BooleanField as BooleanField,
    NullBooleanField as NullBooleanField,
    ListField as ListField,
    DictField as DictField,
    ChoiceField as ChoiceField,
    JSONField as JSONField,
    DateTimeField as DateTimeField,
    SerializerMethodField as SerializerMethodField,
)
from rest_framework.exceptions import (
    APIException as APIException,
    ValidationError as ValidationError,
    ParseError as ParseError,
    NotAuthenticated as NotAuthenticated,
    PermissionDenied as PermissionDenied,
)

class BaseSerializer(Field):
    pass

class Serializer(BaseSerializer):
    @property
    def fields(self) -> Dict[str, Field]: ...
    def get_fields(self) -> Dict[str, Field]: ...
