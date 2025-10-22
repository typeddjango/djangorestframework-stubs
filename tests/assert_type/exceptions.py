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
