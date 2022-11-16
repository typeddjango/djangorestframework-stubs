from collections.abc import Callable, Mapping, Sequence
from typing import Any

from typing_extensions import TypedDict

class DefaultsSettings(TypedDict, total=False):
    DEFAULT_RENDERER_CLASSES: Sequence[str]
    DEFAULT_PARSER_CLASSES: Sequence[str]
    DEFAULT_AUTHENTICATION_CLASSES: Sequence[str]
    DEFAULT_PERMISSION_CLASSES: Sequence[str]
    DEFAULT_THROTTLE_CLASSES: Sequence[str]
    DEFAULT_CONTENT_NEGOTIATION_CLASS: str
    DEFAULT_METADATA_CLASS: str
    DEFAULT_VERSIONING_CLASS: str | None
    DEFAULT_PAGINATION_CLASS: str | None
    DEFAULT_FILTER_BACKENDS: Sequence[str]
    DEFAULT_SCHEMA_CLASS: str
    DEFAULT_THROTTLE_RATES: dict[str, float | int | None]
    NUM_PROXIES: int | None
    PAGE_SIZE: int | None
    SEARCH_PARAM: str
    ORDERING_PARAM: str
    DEFAULT_VERSION: str | None
    ALLOWED_VERSIONS: str | None
    VERSION_PARAM: str
    UNAUTHENTICATED_USER: str
    UNAUTHENTICATED_TOKEN: str | None
    VIEW_NAME_FUNCTION: str
    VIEW_DESCRIPTION_FUNCTION: str
    EXCEPTION_HANDLER: str | Callable[[Any, Any], Any]
    NON_FIELD_ERRORS_KEY: str
    TEST_REQUEST_RENDERER_CLASSES: Sequence[str]
    TEST_REQUEST_DEFAULT_FORMAT: str
    URL_FORMAT_OVERRIDE: str
    FORMAT_SUFFIX_KWARG: str
    URL_FIELD_NAME: str
    DATE_FORMAT: str
    DATE_INPUT_FORMATS: Sequence[str]
    DATETIME_FORMAT: str
    DATETIME_INPUT_FORMATS: Sequence[str]
    TIME_FORMAT: str
    TIME_INPUT_FORMATS: Sequence[str]
    UNICODE_JSON: bool
    COMPACT_JSON: bool
    STRICT_JSON: bool
    COERCE_DECIMAL_TO_STRING: bool
    UPLOADED_FILES_USE_URL: bool
    HTML_SELECT_CUTOFF: int
    HTML_SELECT_CUTOFF_TEXT: str
    SCHEMA_COERCE_PATH_PK: bool
    SCHEMA_COERCE_METHOD_NAMES: dict[str, str]

DEFAULTS: DefaultsSettings
IMPORT_STRINGS: Sequence[str]
REMOVED_SETTINGS: Sequence[str]

def perform_import(val: Any | None, setting_name: str) -> Any | None: ...
def import_from_string(val: Any | None, setting_name: str) -> Any: ...

class APISettings:
    defaults: DefaultsSettings
    import_strings: Sequence[str]
    def __init__(
        self,
        user_settings: DefaultsSettings | None = ...,
        defaults: DefaultsSettings | None = ...,
        import_strings: Sequence[str] | None = ...,
    ): ...
    @property
    def user_settings(self) -> Mapping[str, Any]: ...
    def __getattr__(self, attr: str) -> Any: ...
    def __check_user_settings(self, user_settings: Mapping[str, Any]) -> Mapping[str, Any]: ...
    def reload(self) -> None: ...

class _Settings(APISettings):
    DEFAULT_RENDERER_CLASSES: Sequence[str]
    DEFAULT_PARSER_CLASSES: Sequence[str]
    DEFAULT_AUTHENTICATION_CLASSES: Sequence[str]
    DEFAULT_PERMISSION_CLASSES: Sequence[str]
    DEFAULT_THROTTLE_CLASSES: Sequence[str]
    DEFAULT_CONTENT_NEGOTIATION_CLASS: str
    DEFAULT_METADATA_CLASS: str
    DEFAULT_VERSIONING_CLASS: str | None
    DEFAULT_PAGINATION_CLASS: str | None
    DEFAULT_FILTER_BACKENDS: Sequence[str]
    DEFAULT_SCHEMA_CLASS: str
    DEFAULT_THROTTLE_RATES: dict[str, float | int | None]
    NUM_PROXIES: int | None
    PAGE_SIZE: int | None
    SEARCH_PARAM: str
    ORDERING_PARAM: str
    DEFAULT_VERSION: str | None
    ALLOWED_VERSIONS: str | None
    VERSION_PARAM: str
    UNAUTHENTICATED_USER: str
    UNAUTHENTICATED_TOKEN: str | None
    VIEW_NAME_FUNCTION: str
    VIEW_DESCRIPTION_FUNCTION: str
    EXCEPTION_HANDLER: str | Callable[[Any, Any], Any]
    NON_FIELD_ERRORS_KEY: str
    TEST_REQUEST_RENDERER_CLASSES: Sequence[str]
    TEST_REQUEST_DEFAULT_FORMAT: str
    URL_FORMAT_OVERRIDE: str
    FORMAT_SUFFIX_KWARG: str
    URL_FIELD_NAME: str
    DATE_FORMAT: str
    DATE_INPUT_FORMATS: Sequence[str]
    DATETIME_FORMAT: str
    DATETIME_INPUT_FORMATS: Sequence[str]
    TIME_FORMAT: str
    TIME_INPUT_FORMATS: Sequence[str]
    UNICODE_JSON: bool
    COMPACT_JSON: bool
    STRICT_JSON: bool
    COERCE_DECIMAL_TO_STRING: bool
    UPLOADED_FILES_USE_URL: bool
    HTML_SELECT_CUTOFF: int
    HTML_SELECT_CUTOFF_TEXT: str
    SCHEMA_COERCE_PATH_PK: bool
    SCHEMA_COERCE_METHOD_NAMES: dict[str, str]

api_settings: _Settings

def reload_api_settings(*args: Any, **kwargs: Any) -> None: ...
