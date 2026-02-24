from django.contrib.auth.models import User
from django.db.models import QuerySet
from rest_framework.pagination import PageNumberPagination
from rest_framework.request import Request
from typing_extensions import assert_type

# case: test_page_number_pagination_paginate_queryset
paginator = PageNumberPagination()
request: Request
queryset: QuerySet[User]
page = paginator.paginate_queryset(queryset, request)
assert_type(page, list[User] | None)


# case: test_page_number_pagination_paginate_flat_values_queryset
flat_values_queryset: QuerySet[User, str]
flat_values_page = paginator.paginate_queryset(flat_values_queryset, request)
assert_type(flat_values_page, list[str] | None)
