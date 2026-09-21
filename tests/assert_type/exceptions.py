from collections.abc import Mapping, Sequence
from typing import assert_type

from django.utils.translation import gettext_lazy as _
from rest_framework import exceptions


# case: test_exception_declaration
class MyException1(exceptions.APIException):
    status_code = 200
    default_detail = "Everything is a okay"
    default_code = "ok"


# case: test_exception_declaration_dict_detail
class MyException2(exceptions.APIException):
    status_code = 200
    default_detail = {"ok": "everything"}
    default_code = "ok"


# case: test_exception_declaration_lazystr
class MyException3(exceptions.APIException):
    status_code = 200
    default_detail = _("Está tudo bem")
    default_code = "ok"


# case: test_exception_input_accepts_every_member_of_the_union
# `_Detail`
exceptions.APIException(exceptions.ErrorDetail("with code", code="brown"))
exceptions.APIException([exceptions.ErrorDetail("in a list")])
exceptions.APIException({"field": exceptions.ErrorDetail("field keyed")})
exceptions.APIException({0: exceptions.ErrorDetail("index keyed")})
# `StrOrPromise`
exceptions.APIException("I am just a message", code="msg")
exceptions.APIException(_("translated"))
# `Sequence[_APIExceptionInput]`
exceptions.APIException(["value", _("translated"), {"nested": "test"}])
exceptions.APIException(("also", "tuple", exceptions.ErrorDetail("value")))
# `Mapping[str, _APIExceptionInput]` / `Mapping[int, _APIExceptionInput]`
field_errors: Mapping[str, Sequence[str]] = {"field": ["A valid integer is required."]}
exceptions.APIException(field_errors)
index_errors: Mapping[int, Sequence[str]] = {0: ["A valid integer is required."]}
exceptions.APIException(index_errors)
# `None`
exceptions.APIException(None, None)
exceptions.APIException()


# case: test_exception_detail_round_trips_as_input
def round_trip(exc: exceptions.APIException) -> None:
    exceptions.APIException(detail=exc.detail, code="123")
    exceptions.APIException(detail=[exc.detail], code="123")
    exceptions.APIException(detail={"nested": exc.detail}, code="123")
    exceptions.APIException(detail={0: exc.detail}, code="123")


# case: test_validation_error_detail_keys_may_be_field_names_or_list_indexes
def handle_validation_error(exc: exceptions.ValidationError) -> None:
    # `ListField.run_child_validation` and, since DRF 3.18, `ListSerializer.to_internal_value`
    # key their error mappings by list index rather than by field name.
    if isinstance(exc.detail, dict):
        for key in exc.detail:
            assert_type(key, str | int)
