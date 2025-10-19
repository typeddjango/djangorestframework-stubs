import types

from django.contrib.postgres import fields as django_postgres_fields
from rest_framework.compat import postgres_fields
from typing_extensions import assert_type

# case: test_compat_postgres_fields
assert_type(postgres_fields, types.ModuleType)
assert_type(postgres_fields.hstore.HStoreField(), django_postgres_fields.HStoreField)
