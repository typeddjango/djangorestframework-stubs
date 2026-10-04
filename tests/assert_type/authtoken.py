from typing import assert_type

from rest_framework.authtoken.models import Token, TokenProxy, TokenProxyQuerySet

# case: test_token_objects
assert_type(Token.objects.get(pk="key"), Token)
assert_type(Token.generate_key(), str)

# case: test_token_proxy_delete
assert_type(TokenProxy().delete(), tuple[int, dict[str, int]])


# case: test_token_proxy_queryset_delete
def delete_tokens(queryset: TokenProxyQuerySet) -> tuple[int, dict[str, int]]:
    return queryset.delete()
