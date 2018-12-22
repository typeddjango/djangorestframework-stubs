from typing import Any, Union, Dict, Optional

class APIException(Exception):
    status_code: int

class ValidationError(APIException):
    detail: Union[str, Dict[str, Any]]
    def __init__(self, detail: Optional[Union[str, Dict[str, Any]]] = ...): ...

class NotAuthenticated(APIException):
    pass

class ParseError(APIException):
    pass

class PermissionDenied(APIException):
    pass
