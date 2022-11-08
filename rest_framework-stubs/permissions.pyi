from typing import Any, Dict, List, Protocol, Sequence, Type, Union

from django.db.models import Model, QuerySet
from rest_framework.request import Request
from rest_framework.views import APIView

SAFE_METHODS: Sequence[str] = ("GET", "HEAD", "OPTIONS")

class _SupportsHasPermission(Protocol):
    def has_permission(self, request: Request, view: APIView) -> bool: ...
    def has_object_permission(self, request: Request, view: APIView, obj: Any) -> bool: ...

_PermissionClass = Union[Type[BasePermission], OperandHolder, SingleOperandHolder]

class OperationHolderMixin:
    def __and__(self, other: _PermissionClass) -> OperandHolder: ...
    def __or__(self, other: _PermissionClass) -> OperandHolder: ...
    def __rand__(self, other: _PermissionClass) -> OperandHolder: ...
    def __ror__(self, other: _PermissionClass) -> OperandHolder: ...
    def __invert__(self) -> SingleOperandHolder: ...

class SingleOperandHolder(OperationHolderMixin):
    operator_class: _SupportsHasPermission
    op1_class: _PermissionClass
    def __init__(self, operator_class: _SupportsHasPermission, op1_class: _PermissionClass): ...
    def __call__(self, *args, **kwargs) -> _SupportsHasPermission: ...

class OperandHolder(OperationHolderMixin):
    operator_class: _SupportsHasPermission
    op1_class: _PermissionClass
    op2_class: _PermissionClass
    def __init__(
        self, operator_class: _SupportsHasPermission, op1_class: _PermissionClass, op2_class: _PermissionClass
    ): ...
    def __call__(self, *args, **kwargs) -> _SupportsHasPermission: ...

class AND(_SupportsHasPermission):
    def __init__(self, op1: _SupportsHasPermission, op2: _SupportsHasPermission) -> None: ...

class OR(_SupportsHasPermission):
    def __init__(self, op1: _SupportsHasPermission, op2: _SupportsHasPermission) -> None: ...

class NOT(_SupportsHasPermission):
    def __init__(self, op1: _SupportsHasPermission) -> None: ...

class BasePermissionMetaclass(OperationHolderMixin, type): ...  # type: ignore[misc]

class BasePermission(metaclass=BasePermissionMetaclass):  # type: ignore[misc]
    def has_permission(self, request: Request, view: APIView) -> bool: ...
    def has_object_permission(self, request: Request, view: APIView, obj: Any) -> bool: ...

class AllowAny(BasePermission): ...
class IsAuthenticated(BasePermission): ...
class IsAdminUser(BasePermission): ...
class IsAuthenticatedOrReadOnly(BasePermission): ...

class DjangoModelPermissions(BasePermission):
    perms_map: Dict[str, List[str]] = ...
    authenticated_users_only: bool = ...
    def get_required_permissions(self, method: str, model_cls: Type[Model]) -> List[str]: ...
    def _queryset(self, view: APIView) -> QuerySet: ...

class DjangoModelPermissionsOrAnonReadOnly(DjangoModelPermissions): ...

class DjangoObjectPermissions(DjangoModelPermissions):
    def get_required_object_permissions(self, method: str, model_cls: Type[Model]) -> List[str]: ...
