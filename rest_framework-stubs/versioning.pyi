from collections.abc import Mapping, Sequence
from re import Pattern
from typing import Any

from rest_framework.request import Request

class BaseVersioning:
    default_version: str | None
    allowed_versions: Sequence[str] | None
    version_param: str
    def determine_version(self, request: Request, *args: Any, **kwargs: Any) -> str: ...
    def reverse(
        self,
        viewname: str,
        args: Sequence[Any] | None = ...,
        kwargs: Mapping[str, Any] | None = ...,
        request: Request | None = ...,
        format: str | None = ...,
        **extra: Any
    ) -> str: ...
    def is_allowed_version(self, version: str | None) -> bool: ...

class AcceptHeaderVersioning(BaseVersioning):
    invalid_version_message: str

class URLPathVersioning(BaseVersioning):
    invalid_version_message: str

class NamespaceVersioning(BaseVersioning):
    invalid_version_message: str
    def get_versioned_viewname(self, viewname: str, request: Request) -> str: ...

class HostNameVersioning(BaseVersioning):
    hostname_regex: Pattern
    invalid_version_message: str

class QueryParameterVersioning(BaseVersioning):
    invalid_version_message: str
