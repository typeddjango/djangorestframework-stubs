from collections.abc import Callable, Container, Iterable, MutableMapping
from typing import Any, Protocol, TypeAlias, TypeVar

from django.db.models import Model, Q, QuerySet
from django_stubs_ext import StrOrPromise
from rest_framework.fields import Field
from rest_framework.serializers import BaseSerializer

_T = TypeVar("_T", bound=Model)
_V = TypeVar("_V", contravariant=True)

class ContextValidator(Protocol[_V]):
    requires_context: bool
    def __call__(self, value: _V, context: Field, /) -> None: ...

Validator: TypeAlias = Callable[[_V], None] | ContextValidator[_V]

def qs_exists(queryset: QuerySet) -> bool: ...
def qs_filter(queryset: QuerySet[_T], **kwargs: Any) -> QuerySet[_T]: ...

class UniqueValidator:
    message: StrOrPromise
    requires_context: bool
    queryset: QuerySet
    lookup: str
    def __init__(self, queryset: QuerySet, message: StrOrPromise | None = ..., lookup: str = ...) -> None: ...
    def filter_queryset(self, value: Any, queryset: QuerySet[_T], field_name: str) -> QuerySet[_T]: ...
    def exclude_current_instance(self, queryset: QuerySet[_T], instance: _T) -> QuerySet[_T]: ...
    def __call__(self, value: Any, serializer_field: Field) -> None: ...

class UniqueTogetherValidator:
    message: StrOrPromise
    missing_message: StrOrPromise
    requires_context: bool
    queryset: QuerySet
    fields: Iterable[str]
    def __init__(
        self,
        queryset: QuerySet,
        fields: Iterable[str],
        message: StrOrPromise | None = ...,
        condition_fields: Iterable[str] | None = None,
        condition: Q | None = None,
    ) -> None: ...
    def enforce_required_fields(self, attrs: Container[str], serializer: BaseSerializer) -> None: ...
    def filter_queryset(
        self, attrs: MutableMapping[str, Any], queryset: QuerySet[_T], serializer: BaseSerializer
    ) -> QuerySet[_T]: ...
    def exclude_current_instance(
        self, attrs: MutableMapping[str, Any], queryset: QuerySet[_T], instance: _T
    ) -> QuerySet[_T]: ...
    def __call__(self, attrs: MutableMapping[str, Any], serializer: BaseSerializer) -> None: ...

def qs_exists_with_condition(queryset: QuerySet[Any], condition: Q | None, against: dict[str, Any]) -> bool: ...

class ProhibitSurrogateCharactersValidator:
    message: StrOrPromise
    code: str
    def __call__(self, value: Any) -> None: ...

class BaseUniqueForValidator:
    message: StrOrPromise
    missing_message: StrOrPromise
    requires_context: bool
    queryset: QuerySet
    field: str
    date_field: str
    def __init__(self, queryset: QuerySet, field: str, date_field: str, message: StrOrPromise | None = ...) -> None: ...
    def enforce_required_fields(self, attrs: Container[str]) -> None: ...
    def filter_queryset(
        self, attrs: MutableMapping[str, Any], queryset: QuerySet[_T], field_name: str, date_field_name: str
    ) -> QuerySet[_T]: ...
    def exclude_current_instance(
        self, attrs: MutableMapping[str, Any], queryset: QuerySet[_T], instance: Model
    ) -> QuerySet[_T]: ...
    def __call__(self, attrs: MutableMapping[str, Any], serializer: BaseSerializer) -> None: ...

class UniqueForDateValidator(BaseUniqueForValidator): ...
class UniqueForMonthValidator(BaseUniqueForValidator): ...
class UniqueForYearValidator(BaseUniqueForValidator): ...
