from typing import NamedTuple

from django.db.models import Model
from django.db.models.fields import Field
from django.db.models.fields.related import RelatedField

class RelationInfo(NamedTuple):
    model_field: RelatedField | None
    related_model: type[Model]
    to_many: bool
    to_field: str
    has_through_model: bool
    reverse: bool

class FieldInfo(NamedTuple):
    pk: Field
    fields: dict[str, Field]
    forward_relations: dict[str, RelationInfo]
    reverse_relations: dict[str, RelationInfo]
    fields_and_pk: dict[str, Field]
    relations: dict[str, RelationInfo]

def get_field_info(model: type[Model]) -> FieldInfo: ...
def is_abstract_model(model: type[Model]) -> bool: ...
