from rest_framework.authtoken.models import TokenProxyQuerySet


# case: test_token_proxy_queryset_delete
def delete_tokens(queryset: TokenProxyQuerySet) -> tuple[int, dict[str, int]]:
    return queryset.delete()
