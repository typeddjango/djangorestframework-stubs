from _typeshed import SupportsKeysAndGetItem
from collections.abc import Iterable, Iterator, MutableMapping
from typing import Any, Generic, TypeVar, overload

from rest_framework.exceptions import ErrorDetail
from rest_framework.fields import Field
from rest_framework.serializers import BaseSerializer

_T = TypeVar("_T")
_VT = TypeVar("_VT")
_KT = TypeVar("_KT")

class ReturnDict(dict[_KT, _VT], Generic[_KT, _VT]):
    serializer: BaseSerializer
    # Copied from https://github.com/python/typeshed/blob/main/stdlib/builtins.pyi `class dict`
    @overload
    def __init__(self, *, serializer: BaseSerializer) -> None: ...
    @overload
    def __init__(self: ReturnDict[str, _VT], *, serializer: BaseSerializer, **kwargs: _VT) -> None: ...
    @overload
    def __init__(self, __map: SupportsKeysAndGetItem[_KT, _VT], *, serializer: BaseSerializer) -> None: ...
    @overload
    def __init__(
        self: ReturnDict[str, _VT],
        __map: SupportsKeysAndGetItem[str, _VT],
        *,
        serializer: BaseSerializer,
        **kwargs: _VT
    ) -> None: ...
    @overload
    def __init__(self, __iterable: Iterable[tuple[_KT, _VT]], *, serializer: BaseSerializer) -> None: ...
    @overload
    def __init__(
        self: ReturnDict[str, _VT], __iterable: Iterable[tuple[str, _VT]], *, serializer: BaseSerializer, **kwargs: _VT
    ) -> None: ...
    # Next two overloads are for dict(string.split(sep) for string in iterable)
    # Cannot be Iterable[Sequence[_T]] or otherwise dict(["foo", "bar", "baz"]) is not an error
    @overload
    def __init__(
        self: ReturnDict[str, str], __iterable: Iterable[list[str]], *, serializer: BaseSerializer
    ) -> None: ...
    @overload
    def __init__(
        self: ReturnDict[bytes, bytes], __iterable: Iterable[list[bytes]], *, serializer: BaseSerializer
    ) -> None: ...
    def copy(self) -> ReturnDict[_KT, _VT]: ...
    def __reduce__(self) -> tuple[type[dict[_KT, _VT]], tuple[dict[_KT, _VT]]]: ...

class ReturnList(list[_T], Generic[_T]):
    serializer: BaseSerializer
    # Copied from https://github.com/python/typeshed/blob/main/stdlib/builtins.pyi `class list`
    @overload
    def __init__(self, *, serializer: BaseSerializer) -> None: ...
    @overload
    def __init__(self, __iterable: Iterable[_T], *, serializer: BaseSerializer) -> None: ...
    def __reduce__(self) -> tuple[type[list[_T]], tuple[list[_T]]]: ...

class BoundField:
    """
    A field object that also includes `.value` and `.error` properties.
    Returned when iterating over a serializer instance,
    providing an API similar to Django forms and form fields.
    """

    value: Any
    fields: dict[str, Field]
    errors: list[ErrorDetail]
    def __init__(self, field: Field, value: Any, errors: list[ErrorDetail], prefix: str = ...) -> None: ...
    def __getattr__(self, attr_name: str) -> Any: ...
    def as_form_field(self) -> BoundField: ...

class JSONBoundField(BoundField): ...

class NestedBoundField(BoundField):
    def __iter__(self) -> Iterator[str]: ...
    def __getitem__(self, key: str) -> BoundField | NestedBoundField: ...

class BindingDict(MutableMapping[str, Field]):
    serializer: BaseSerializer
    fields: dict[str, Field]
    def __init__(self, serializer: BaseSerializer) -> None: ...
    def __setitem__(self, key: str, field: Field) -> None: ...
    def __getitem__(self, key: str) -> Field: ...
    def __delitem__(self, key: str) -> None: ...
    def __iter__(self) -> Iterator[Field]: ...  # type: ignore[override]
    def __len__(self) -> int: ...
