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
    Sequence,
    Tuple,
    Type,
    Union,
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
from rest_framework.fields import CharField as CharField
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
from rest_framework.utils.serializer_helpers import BoundField, ReturnDict, ReturnList

LIST_SERIALIZER_KWARGS: Sequence[str] = ...
ALL_FIELDS: str = ...

class BaseSerializer(Field):
    _declared_fields: Dict[str, Field]
    instance: Optional[Any]
    initial_data: Any
    partial: bool
    def __init__(self, instance: Optional[Any] = ..., data: Any = ..., **kwargs: Any): ...
    @classmethod
    def many_init(cls, *args: Any, **kwargs: Any) -> BaseSerializer: ...
    def to_internal_value(self, data: Any) -> Any: ...
    def to_representation(self, instance: Any) -> Any: ...
    def update(self, instance: Model, validated_data: Any) -> Any: ...
    def create(self, validated_data: Any) -> Any: ...
    def save(self, **kwargs: Any) -> Any: ...
    def is_valid(self, raise_exception: bool = ...) -> bool: ...
    @property
    def data(self) -> Any: ...
    @property
    def errors(self) -> Iterable[Any]: ...
    @property
    def validated_data(self) -> Any: ...

class SerializerMetaclass(type):
    @classmethod
    def _get_declared_fields(cls, bases: Sequence[type], attrs: Dict[str, Any]) -> Dict[str, Field]: ...

def as_serializer_error(exc: Exception) -> Dict[str, List[ErrorDetail]]: ...

class Serializer(BaseSerializer):
    @property
    def fields(self) -> Dict[str, Field]: ...
    @property
    def _writable_fields(self) -> List[Field]: ...
    @property
    def _readable_fields(self) -> List[Field]: ...
    def get_fields(self) -> Dict[str, Field]: ...
    def _read_only_defaults(self) -> Dict[str, Any]: ...
    def validate(self, attrs):
        return attrs
    @property
    def data(self) -> ReturnDict: ...
    @property
    def errors(self) -> ReturnDict: ...
    def __iter__(self) -> Iterator[str]: ...
    def __getitem__(self, key: str) -> BoundField: ...
    def __len__(self) -> int: ...

class ListSerializer(BaseSerializer):
    child: BaseSerializer = ...
    many: bool = ...
    def validate(self, attrs):
        return attrs
    @property
    def data(self) -> ReturnList: ...
    @property
    def errors(self) -> ReturnList: ...

def raise_errors_on_nested_writes(method_name: str, serializer: BaseSerializer, validated_data: Any) -> None: ...

class ModelSerializer(Serializer):
    serializer_field_mapping: Dict[Type[models.Field], Type[Field]] = ...
    serializer_related_field: Type[RelatedField] = ...
    serializer_related_to_field: Type[RelatedField] = ...
    serializer_url_field: Type[RelatedField] = ...
    serializer_choice_field: Type[Field] = ...
    url_field_name: Optional[str] = ...
    class Meta:
        model: Type[Model]
        fields: Optional[Union[Sequence[str], str]]
        read_only_fields: Optional[Sequence[str]]
        exclude: Optional[Sequence[str]]
        depth: Optional[int]
        extra_kwargs: Dict[str, Dict[str, Any]]
    def get_field_names(self, declared_fields: Mapping[str, Field], info: FieldInfo) -> List[str]: ...
    def get_default_field_names(self, declared_fields: Mapping[str, Field], model_info: FieldInfo) -> List[str]: ...
    def build_field(
        self, field_name: str, info: FieldInfo, model_class: Type[Model], nested_depth: int
    ) -> Tuple[Type[Field], Dict[str, Any]]: ...
    def build_standard_field(
        self, field_name: str, model_field: Type[models.Field]
    ) -> Tuple[Type[Field], Dict[str, Any]]: ...
    def build_relational_field(
        self, field_name: str, relation_info: RelationInfo
    ) -> Tuple[Type[Field], Dict[str, Any]]: ...
    def build_nested_field(
        self, field_name: str, relation_info: RelationInfo, nested_depth: int
    ) -> Tuple[Type[Field], Dict[str, Any]]: ...
    def build_property_field(self, field_name: str, model_class: Type[Model]) -> Tuple[Type[Field], Dict[str, Any]]: ...
    def build_url_field(self, field_name: str, model_class: Type[Model]) -> Tuple[Type[Field], Dict[str, Any]]: ...
    def build_unknown_field(self, field_name: str, model_class: Type[Model]) -> NoReturn: ...
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
