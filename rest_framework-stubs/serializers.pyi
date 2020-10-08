from collections import OrderedDict
from typing import (
    Any,
    Callable,
    Dict,
    Iterable,
    Iterator,
    List,
    Mapping,
    MutableMapping,
    NoReturn,
    Optional,
    Protocol,
    Sequence,
    Tuple,
    Type,
    TypeVar,
    Union,
    Generic,
)

from django.core.exceptions import ValidationError as DjangoValidationError
from django.db import models
from django.db.models import DurationField as ModelDurationField
from django.db.models import Model
from django.db.models.fields import Field as DjangoModelField
from django.utils.translation import ugettext_lazy as _
from rest_framework.exceptions import APIException as APIException
from rest_framework.exceptions import AuthenticationFailed as AuthenticationFailed
from rest_framework.exceptions import ErrorDetail as ErrorDetail
from rest_framework.exceptions import MethodNotAllowed as MethodNotAllowed
from rest_framework.exceptions import NotAcceptable as NotAcceptable
from rest_framework.exceptions import NotAuthenticated as NotAuthenticated
from rest_framework.exceptions import NotFound as NotFound
from rest_framework.exceptions import ParseError as ParseError
from rest_framework.exceptions import PermissionDenied as PermissionDenied
from rest_framework.exceptions import Throttled as Throttled
from rest_framework.exceptions import UnsupportedMediaType as UnsupportedMediaType
from rest_framework.exceptions import ValidationError as ValidationError
from rest_framework.fields import BooleanField as BooleanField
from rest_framework.fields import CharField as CharField  # noqa: F401
from rest_framework.fields import ChoiceField as ChoiceField
from rest_framework.fields import CreateOnlyDefault as CreateOnlyDefault
from rest_framework.fields import CurrentUserDefault as CurrentUserDefault
from rest_framework.fields import DateField as DateField
from rest_framework.fields import DateTimeField as DateTimeField
from rest_framework.fields import DecimalField as DecimalField
from rest_framework.fields import DictField as DictField
from rest_framework.fields import DurationField as DurationField
from rest_framework.fields import EmailField as EmailField
from rest_framework.fields import Field as Field
from rest_framework.fields import FileField as FileField
from rest_framework.fields import FilePathField as FilePathField
from rest_framework.fields import FloatField as FloatField
from rest_framework.fields import HiddenField as HiddenField
from rest_framework.fields import HStoreField as HStoreField
from rest_framework.fields import ImageField as ImageField
from rest_framework.fields import IntegerField as IntegerField
from rest_framework.fields import IPAddressField as IPAddressField
from rest_framework.fields import JSONField as JSONField
from rest_framework.fields import ListField as ListField
from rest_framework.fields import ModelField as ModelField
from rest_framework.fields import MultipleChoiceField as MultipleChoiceField
from rest_framework.fields import NullBooleanField as NullBooleanField
from rest_framework.fields import ReadOnlyField as ReadOnlyField
from rest_framework.fields import RegexField as RegexField
from rest_framework.fields import SerializerMethodField as SerializerMethodField
from rest_framework.fields import SkipField as SkipField
from rest_framework.fields import SlugField as SlugField
from rest_framework.fields import TimeField as TimeField
from rest_framework.fields import URLField as URLField
from rest_framework.fields import UUIDField as UUIDField
from rest_framework.relations import Hyperlink as Hyperlink
from rest_framework.relations import HyperlinkedIdentityField as HyperlinkedIdentityField
from rest_framework.relations import HyperlinkedRelatedField as HyperlinkedRelatedField
from rest_framework.relations import ManyRelatedField as ManyRelatedField
from rest_framework.relations import PrimaryKeyRelatedField as PrimaryKeyRelatedField
from rest_framework.relations import RelatedField as RelatedField
from rest_framework.relations import SlugRelatedField as SlugRelatedField
from rest_framework.relations import StringRelatedField as StringRelatedField
from rest_framework.utils.model_meta import FieldInfo, RelationInfo
from rest_framework.utils.serializer_helpers import BindingDict, BoundField, ReturnDict, ReturnList
from typing_extensions import Literal

LIST_SERIALIZER_KWARGS: Sequence[str] = ...
ALL_FIELDS: str = ...

_MT = TypeVar("_MT", bound=Model)  # Model Type
_IN = TypeVar("_IN", Model, Mapping[str, Any], Sequence[Any], covariant=True)  # Instance Type
_DT = TypeVar("_DT", List[Any], Mapping[str, Any], Sequence[Mapping[str, Any]], covariant=True)  # Data Type
_VT = TypeVar("_VT", Model, Mapping[str, Any], Sequence[Mapping[str, Any]], covariant=True)  # Value Type
_RP = TypeVar("_RP", Dict[str, Any], List[Dict[str, Any]], covariant=True)  # Representation Type

class SerializerProtocol(Protocol[_IN, _DT, _VT, _RP]):
    def __init__(
        self,
        instance: _IN = ...,
        data: _DT = ...,
        partial: bool = ...,
        read_only: bool = ...,
        write_only: bool = ...,
        required: bool = ...,
        default: Union[_VT, Callable[[], _VT]] = ...,
        initial: Union[_VT, Callable[[], _VT]] = ...,
        source: str = ...,
        label: str = ...,
        help_text: str = ...,
        style: Dict[str, Any] = ...,
        error_messages: Dict[str, str] = ...,
        validators: Sequence[Callable] = ...,
        allow_null: bool = ...,
    ): ...
    def update(self, instance: _IN, validated_data: OrderedDict) -> _IN: ...
    def create(self, validated_data: OrderedDict) -> _IN: ...
    def save(self, **kwargs: Any) -> _IN: ...
    def to_internal_value(self, data: _DT) -> _VT: ...
    def to_representation(self, instance: _IN) -> _RP: ...

class BaseSerializer(Generic[_VT, _DT, _RP, _IN], Field[_VT, _DT, _RP, _IN], SerializerProtocol[_VT, _DT, _RP, _IN]):
    partial: bool
    instance: Optional[_IN]
    initial_data: Optional[_DT]
    def __new__(cls, *args: Any, **kwargs: Any) -> BaseSerializer: ...
    def __class_getitem__(cls, *args, **kwargs): ...
    @classmethod
    def many_init(cls, *args: Any, **kwargs: Any) -> BaseSerializer: ...
    def is_valid(self, raise_exception: bool = ...) -> bool: ...
    @property
    def data(self) -> Any: ...
    @property
    def errors(self) -> Iterable[Any]: ...
    @property
    def validated_data(self) -> OrderedDict: ...

class SerializerMetaclass(type):
    def __new__(cls, name: Any, bases: Any, attrs: Any): ...
    @classmethod
    def _get_declared_fields(cls, bases: Sequence[type], attrs: Dict[str, Any]) -> Dict[str, Field]: ...

def as_serializer_error(exc: Exception) -> Dict[str, List[ErrorDetail]]: ...

class Serializer(
    BaseSerializer[
        Union[_MT, Mapping[str, Any]], Mapping[str, Any], Dict[str, Any], Dict[str, Any], Union[_MT, Mapping[str, Any]]
    ],
    metaclass=SerializerMetaclass,
):
    _declared_fields: Dict[str, Field]
    default_error_messages: Dict[str, Any] = ...
    def get_initial(self) -> OrderedDict: ...
    @property
    def fields(self) -> BindingDict: ...
    def get_fields(self) -> Dict[str, Field]: ...
    def validate(self, attrs: OrderedDict) -> OrderedDict: ...
    def __iter__(self) -> Iterator[str]: ...
    def __getitem__(self, key: str) -> BoundField: ...
    def _read_only_defaults(self) -> Dict[str, Any]: ...
    @property
    def _writable_fields(self) -> List[Field]: ...
    @property
    def _readable_fields(self) -> List[Field]: ...
    @property
    def data(self) -> ReturnDict: ...
    @property
    def errors(self) -> ReturnDict: ...

class ListSerializer(
    BaseSerializer[
        List[Mapping[Any, Any]],
        List[Mapping[Any, Any]],
        List[Dict[str, Any]],
        List[Dict[str, Any]],
        List[Mapping[Any, Any]],
    ]
):
    child: Optional[
        Union[
            Field,
            BaseSerializer,
        ]
    ] = ...
    many: bool = ...
    default_error_messages: Dict[str, Any] = ...
    allow_empty: Optional[bool] = ...
    def __init__(
        self,
        instance: _IN = ...,
        data: _DT = ...,
        partial: bool = ...,
        child: Optional[
            Union[
                Field,
                BaseSerializer,
            ]
        ] = ...,
        read_only: bool = ...,
        write_only: bool = ...,
        required: bool = ...,
        default: Union[List[Mapping[Any, Any]], Callable[[], List[Mapping[Any, Any]]]] = ...,
        initial: Union[List[Mapping[Any, Any]], Callable[[], List[Mapping[Any, Any]]]] = ...,
        source: str = ...,
        label: str = ...,
        help_text: str = ...,
        style: Dict[str, Any] = ...,
        error_messages: Dict[str, str] = ...,
        validators: Sequence[Callable] = ...,
        allow_null: bool = ...,
    ): ...
    def get_initial(self) -> List[Any]: ...
    def validate(self, attrs: OrderedDict) -> OrderedDict: ...
    @property
    def data(self) -> ReturnList: ...
    @property
    def errors(self) -> ReturnList: ...

def raise_errors_on_nested_writes(method_name: str, serializer: BaseSerializer, validated_data: Any) -> NoReturn: ...

class ModelSerializer(Serializer, SerializerProtocol[_MT, Mapping[str, Any], Dict[str, Any], Dict[str, Any]]):
    serializer_field_mapping: Dict[Type[models.Field], Field] = ...
    serializer_related_field: RelatedField = ...
    serializer_related_to_field: RelatedField = ...
    serializer_url_field: RelatedField = ...
    serializer_choice_field: Field = ...
    url_field_name: Optional[str] = ...
    instance: Optional[_MT] = ...
    class Meta:
        model: _MT  # type: ignore
        fields: Union[Sequence[str], Literal["__all__"]]
        read_only_fields: Optional[Sequence[str]]
        exclude: Optional[Sequence[str]]
        depth: Optional[int]
        extra_kwargs: Dict[str, Dict[str, Any]]  # type: ignore[override]
    def get_field_names(self, declared_fields: Mapping[str, Field], info: FieldInfo) -> List[str]: ...
    def get_default_field_names(self, declared_fields: Mapping[str, Field], model_info: FieldInfo) -> List[str]: ...
    def build_field(
        self, field_name: str, info: FieldInfo, model_class: _MT, nested_depth: int
    ) -> Tuple[Field, Dict[str, Any]]: ...
    def build_standard_field(
        self, field_name: str, model_field: Type[models.Field]
    ) -> Tuple[Field, Dict[str, Any]]: ...
    def build_relational_field(self, field_name: str, relation_info: RelationInfo) -> Tuple[Field, Dict[str, Any]]: ...
    def build_nested_field(
        self, field_name: str, relation_info: RelationInfo, nested_depth: int
    ) -> Tuple[Field, Dict[str, Any]]: ...
    def build_property_field(self, field_name: str, model_class: _MT) -> Tuple[Field, Dict[str, Any]]: ...
    def build_url_field(self, field_name: str, model_class: _MT) -> Tuple[Field, Dict[str, Any]]: ...
    def build_unknown_field(self, field_name: str, model_class: _MT) -> NoReturn: ...
    def include_extra_kwargs(
        self, kwargs: MutableMapping[str, Any], extra_kwargs: MutableMapping[str, Any]
    ) -> MutableMapping[str, Any]: ...
    def get_extra_kwargs(self) -> Dict[str, Any]: ...
    def get_uniqueness_extra_kwargs(
        self, field_names: Iterable[str], declared_fields: Mapping[str, Field], extra_kwargs: Dict[str, Any]
    ) -> Tuple[Dict[str, Any], Dict[str, HiddenField]]: ...
    def _get_model_fields(
        self, field_names: Iterable[str], declared_fields: Mapping[str, Field], extra_kwargs: MutableMapping[str, Any]
    ) -> Dict[str, models.Field]: ...
    def get_unique_together_validators(self) -> List[Callable]: ...
    def get_unique_for_date_validators(self) -> List[Callable]: ...

class HyperlinkedModelSerializer(ModelSerializer): ...
