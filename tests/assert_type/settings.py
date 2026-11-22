from collections.abc import Sequence
from typing import assert_type

from rest_framework.settings import APISettings, api_settings


# case: test_allowed_versions_setting_is_a_sequence_of_versions
def check_allowed_versions_setting() -> None:
    assert_type(api_settings.ALLOWED_VERSIONS, Sequence[str] | None)


# case: test_user_settings_accept_a_sequence_of_allowed_versions
def check_user_settings_allowed_versions() -> APISettings:
    return APISettings({"ALLOWED_VERSIONS": ("v1", "v2")})
