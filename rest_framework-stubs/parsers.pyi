from typing import IO, Any, Dict, Generic, Mapping, Optional, Type, TypeVar, Union

from django.core.files.uploadedfile import UploadedFile
from django.http import QueryDict
from django.utils.datastructures import MultiValueDict
from rest_framework.renderers import JSONRenderer

_Data = TypeVar("_Data")
_Files = TypeVar("_Files")

class DataAndFiles(Generic[_Data, _Files]):
    data: _Data
    files: _Files
    def __init__(self, data: _Data, files: _Files) -> None: ...

class BaseParser:
    media_type: str = ...
    def parse(
        self, stream: IO[Any], media_type: Optional[str] = ..., parser_context: Optional[Mapping[str, Any]] = ...
    ) -> Union[Mapping[Any, Any], DataAndFiles]: ...

class JSONParser(BaseParser):
    renderer_class: Type[JSONRenderer] = ...
    strict: bool = ...
    def parse(
        self, stream: IO[Any], media_type: Optional[str] = ..., parser_context: Optional[Mapping[str, Any]] = ...
    ) -> Dict[str, Any]: ...

class FormParser(BaseParser):
    def parse(
        self, stream: IO[Any], media_type: Optional[str] = ..., parser_context: Optional[Mapping[str, Any]] = ...
    ) -> QueryDict: ...

class MultiPartParser(BaseParser):
    def parse(
        self, stream: IO[Any], media_type: Optional[str] = ..., parser_context: Optional[Mapping[str, Any]] = ...
    ) -> DataAndFiles[QueryDict, MultiValueDict]: ...

class FileUploadParser(BaseParser):
    errors: Dict[str, str] = ...
    def parse(
        self, stream: IO[Any], media_type: Optional[str] = ..., parser_context: Optional[Mapping[str, Any]] = ...
    ) -> DataAndFiles[None, Mapping[str, UploadedFile]]: ...
    def get_filename(self, stream: IO[Any], media_type: Optional[str], parser_context: Mapping[str, Any]) -> str: ...
    def get_encoded_filename(self, filename_parm: Mapping[str, Any]) -> str: ...
