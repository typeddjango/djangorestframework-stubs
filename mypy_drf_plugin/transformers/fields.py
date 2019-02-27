from mypy.nodes import TypeInfo, Var
from mypy.plugin import FunctionContext
from mypy.types import AnyType, Instance, Type, TypeOfAny

from mypy_drf_plugin import helpers


def retrieve_field_get_type(type_info: TypeInfo, private_field_name: str, is_nullable: bool) -> Type:
    if not type_info.has_readable_member(private_field_name):
        return AnyType(TypeOfAny.unannotated)

    node = type_info.get(private_field_name).node
    if isinstance(node, Var):
        descriptor_type = node.type
        if is_nullable:
            descriptor_type = helpers.make_optional(descriptor_type)
        return descriptor_type
    return AnyType(TypeOfAny.unannotated)


def set_generic_parameters_for_field(ctx: FunctionContext) -> Type:
    default_return_type = ctx.default_return_type
    if not isinstance(default_return_type, Instance):
        return default_return_type

    is_nullable = bool(helpers.parse_bool(helpers.get_argument_by_name(ctx, 'allow_null')))

    actual_field_datatype = retrieve_field_get_type(default_return_type.type,
                                                    private_field_name='_pyi_field_actual_type', is_nullable=is_nullable)
    primitive_field_datatype = retrieve_field_get_type(default_return_type.type,
                                                       private_field_name='_pyi_field_primitive_type', is_nullable=is_nullable)

    return helpers.reparametrize_instance(default_return_type, [actual_field_datatype,
                                                                primitive_field_datatype])
