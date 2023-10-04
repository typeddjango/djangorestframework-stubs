from typing import Any

from django.db import models
from typing_extensions import Self

class Token(models.Model):
    key: models.CharField
    user: models.OneToOneField
    created: models.DateTimeField
    @classmethod
    def generate_key(cls) -> str: ...

class TokenProxy(Token):
    @property
    def pk(self: Self) -> Any: ...
