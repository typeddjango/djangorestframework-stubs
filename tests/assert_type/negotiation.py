from typing import assert_type

from rest_framework.negotiation import DefaultContentNegotiation
from rest_framework.parsers import get_encoding
from rest_framework.utils.mediatypes import _MediaType, order_parsed_by_precedence

# case: negotiation_limits
assert_type(DefaultContentNegotiation.max_accept_header_length, int)
assert_type(DefaultContentNegotiation.max_accept_tokens, int)
assert_type(DefaultContentNegotiation.max_media_type_length, int)


# case: subclass_overrides_limits
class StrictNegotiation(DefaultContentNegotiation):
    max_accept_header_length = 1024
    max_accept_tokens = 8
    max_media_type_length = 64


# case: media_type_precedence
assert_type(order_parsed_by_precedence([_MediaType("text/html")]), list[set[_MediaType]])
assert_type(_MediaType(None), _MediaType)
assert_type({_MediaType("text/html")}, set[_MediaType])

# case: parser_get_encoding
assert_type(get_encoding({"encoding": "utf-8"}), str)
