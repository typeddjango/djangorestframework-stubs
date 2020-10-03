from typing import IO, Any, Dict, Mapping, Optional, Type

from rest_framework.renderers import BaseRenderer

class DataAndFiles:
    data: Any
    files: Mapping[str, IO[Any]]
    def __init__(self, data: Any, files: Mapping[str, IO[Any]]) -> None: ...

class BaseParser:
    media_type: str = ...
    def parse(
        self, stream: IO[Any], media_type: Optional[str] = ..., parser_context: Optional[Mapping[str, Any]] = ...
    ) -> Dict[str, Any]: ...

class JSONParser(BaseParser):
    renderer_class: Type[BaseRenderer] = ...
    strict: bool = ...

class FormParser(BaseParser): ...
class MultiPartParser(BaseParser): ...

class FileUploadParser(BaseParser):
    errors: Dict[str, str] = ...
    def get_filename(self, stream: IO[Any], media_type: Optional[str], parser_context: Mapping[str, Any]) -> str: ...
    def get_encoded_filename(self, filename_parm: Mapping[str, Any]) -> str: ...
