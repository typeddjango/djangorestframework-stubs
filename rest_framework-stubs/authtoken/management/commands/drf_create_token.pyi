from typing import Any

from _typeshed import Incomplete
from django.contrib.auth.base_user import AbstractBaseUser
from django.core.management.base import BaseCommand

UserModel: AbstractBaseUser

class Command(BaseCommand):
    help: str
    def create_user_token(self, username: str, reset_token: bool) -> Incomplete: ...
    def add_arguments(self, parser: Any) -> None: ...
    def handle(self, *args: Any, **options: Any) -> None: ...
