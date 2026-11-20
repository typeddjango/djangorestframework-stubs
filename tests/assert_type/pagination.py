from typing import Any, assert_type

from django.contrib.auth.models import User
from django.db.models import QuerySet
from rest_framework.pagination import PageNumberPagination
from rest_framework.request import Request


# case: test_page_number_pagination_paginate_queryset
def check_model_page(request: Request, queryset: QuerySet[User]) -> None:
    page = PageNumberPagination().paginate_queryset(queryset, request)
    assert_type(page, list[User] | None)


# case: test_page_number_pagination_paginate_flat_values_queryset
def check_values_page(request: Request, queryset: QuerySet[User, str]) -> None:
    page = PageNumberPagination().paginate_queryset(queryset, request)
    assert_type(page, list[str] | None)


# case: test_page_number_pagination_paginate_sequence
def check_sequence_page(request: Request, sequence_data: list[dict[str, Any]]) -> None:
    page = PageNumberPagination().paginate_queryset(sequence_data, request)
    assert_type(page, list[dict[str, Any]] | None)
