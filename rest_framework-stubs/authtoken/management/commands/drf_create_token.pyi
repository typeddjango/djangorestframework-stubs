from typing import Any

from django.contrib.auth.base_user import AbstractBaseUser
from django.core.management.base import BaseCommand
from rest_framework.authtoken.models import Token
from typing_extensions import override

UserModel: AbstractBaseUser

class Command(BaseCommand):
    help: str
    def create_user_token(self, username: str, reset_token: bool) -> Token: ...
    @override
    def add_arguments(self, parser: Any) -> None: ...
    @override
    def handle(self, *args: Any, **options: Any) -> None: ...
