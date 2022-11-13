from typing import Any

from django.db import models

class Token(models.Model):
    key: models.CharField
    user: models.OneToOneField
    created: models.DateTimeField
    @classmethod
    def generate_key(cls) -> str: ...

class TokenProxy(Token):
    @property
    def pk(self) -> Any: ...
