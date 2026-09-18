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


# case: test_validation_error_detail_is_index_or_field_keyed
def handle_validation_error(exc: exceptions.ValidationError) -> None:
    # DRF keys error mappings by list index in `ListField.run_child_validation` and, since
    # DRF 3.18, in `ListSerializer.to_internal_value`, so keys are not necessarily field names.
    if isinstance(exc.detail, dict):
        for key in exc.detail:
            assert_type(key, str | int)


# case: test_validation_error_accepts_index_keyed_mapping
index_errors: dict[int, list[str]] = {0: ["A valid integer is required."]}
exceptions.ValidationError(index_errors)

field_errors: dict[str, list[str]] = {"field": ["A valid integer is required."]}
exceptions.ValidationError(field_errors)
