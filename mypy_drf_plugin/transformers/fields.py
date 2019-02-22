from mypy.nodes import TypeInfo, Var
from mypy.plugin import FunctionContext
from mypy.types import AnyType, Instance, Type, TypeOfAny
from mypy_django_plugin import helpers


def get_private_descriptor_type(type_info: TypeInfo, private_field_name: str, is_nullable: bool) -> Type:
    if not type_info.has_readable_member(private_field_name):
        return AnyType(TypeOfAny.unannotated)

    node = type_info.get(private_field_name).node
    if isinstance(node, Var):
        descriptor_type = node.type
        if is_nullable:
            descriptor_type = helpers.make_optional(descriptor_type)
        return descriptor_type
    return AnyType(TypeOfAny.unannotated)


def fill_parameters_of_descriptor_methods_from_private_attributes(ctx: FunctionContext) -> Type:
    default_return_type = ctx.default_return_type
    if not isinstance(default_return_type, Instance):
        return default_return_type

    is_nullable = bool(helpers.parse_bool(helpers.get_argument_by_name(ctx, 'allow_null')))
    get_type = get_private_descriptor_type(default_return_type.type, '_pyi_private_get_type',
                                           is_nullable=is_nullable)
    return helpers.reparametrize_instance(default_return_type, [get_type])
