from mypy.types import Instance, Type

from mypy_drf_plugin import helpers


def make_field_repr_not_return_any_generics():
    from mypy import messages

    # format_bare
    old_format_bare = messages.MessageBuilder.format_bare

    def patched_format_bare(self, typ: Type, verbosity: int = 0) -> str:
        if isinstance(typ, Instance) and typ.type.has_base(helpers.FIELD_FULLNAME):
            typ = helpers.reparametrize_instance(typ, [])

        return old_format_bare(self, typ, verbosity)

    messages.MessageBuilder.format_bare = patched_format_bare
