from mypy.nodes import TypeInfo
from mypy.plugin import ClassDefContext, FunctionContext
from mypy.types import AnyType, Instance, Type, TypeOfAny

from mypy_drf_plugin import helpers


def retrieve_field_get_type(type_info: TypeInfo, private_field_name: str) -> Type:
    if not type_info.has_readable_member(private_field_name):
        return AnyType(TypeOfAny.explicit)

    sym = type_info.get(private_field_name)
    if sym and isinstance(sym.type, Instance):
        return sym.type

    return AnyType(TypeOfAny.explicit)


def set_types_metadata(ctx: ClassDefContext) -> None:
    actual_field_datatype = retrieve_field_get_type(ctx.cls.info,
                                                    private_field_name='_pyi_field_actual_type')
    primitive_field_datatype = retrieve_field_get_type(ctx.cls.info,
                                                       private_field_name='_pyi_field_primitive_type')

    # add types to metadata for use in ModelSerializer.Meta.fields
    metadata = helpers.get_drf_metadata(ctx.cls.info)
    if 'types' not in metadata:
        metadata['types'] = {'actual': actual_field_datatype.serialize(),
                             'primitive': primitive_field_datatype.serialize()}

    sym = ctx.api.lookup_fully_qualified_or_none(helpers.FIELD_FULLNAME)
    if sym and isinstance(sym.node, TypeInfo):
        helpers.get_drf_metadata(sym.node)['field_bases'][ctx.cls.fullname] = 1


def set_generic_parameters_for_field(ctx: FunctionContext) -> Type:
    default_return_type = ctx.default_return_type
    if not isinstance(default_return_type, Instance):
        return default_return_type

    types = helpers.get_drf_metadata_key(default_return_type.type, 'types', traverse_mro=True)
    if types is None:
        return default_return_type

    actual_field_datatype = helpers.deserialize_type(ctx.api, types['actual'])
    primitive_field_datatype = helpers.deserialize_type(ctx.api, types['primitive'])

    is_nullable = bool(helpers.parse_bool(helpers.get_argument_by_name(ctx, 'allow_null')))
    if is_nullable:
        actual_field_datatype = helpers.make_optional(actual_field_datatype)
        primitive_field_datatype = helpers.make_optional(primitive_field_datatype)

    return helpers.reparametrize_instance(default_return_type, [actual_field_datatype,
                                                                primitive_field_datatype])
