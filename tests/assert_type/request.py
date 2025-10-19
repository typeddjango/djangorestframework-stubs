from rest_framework.request import Request
from typing_extensions import assert_type


# case: request_querydict
def some_view(request: Request) -> None:
    assert_type(request.query_params["field"], str)
    assert_type(request.POST["field"], str)
