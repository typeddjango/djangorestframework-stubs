from typing import Any, ClassVar

from django.db import models
from django.db.models.manager import Manager
from typing_extensions import Self

class Token(models.Model):
    key: models.CharField
    user: models.OneToOneField
    created: models.DateTimeField
    objects: ClassVar[Manager[Self]]
    @classmethod
    def generate_key(cls) -> str: ...

class TokenProxy(Token):
    @property
    def pk(self: Self) -> Any: ...
