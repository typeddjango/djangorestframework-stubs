from typing import assert_type

from rest_framework.request import MAX_MEDIA_TYPE_LENGTH, Request, is_form_media_type


# case: request_querydict
def some_view(request: Request) -> None:
    assert_type(request.query_params["field"], str)
    assert_type(request.POST["field"], str)


# case: is_form_media_type
assert_type(is_form_media_type("application/json"), bool)
assert_type(MAX_MEDIA_TYPE_LENGTH, int)
