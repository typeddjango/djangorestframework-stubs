from collections.abc import Mapping
from typing import IO, Any, Generic, TypeVar

from django.core.files.uploadedfile import UploadedFile
from django.http.request import _ImmutableQueryDict
from django.utils.datastructures import MultiValueDict
from rest_framework.renderers import JSONRenderer

_Data = TypeVar("_Data")
_Files = TypeVar("_Files")

class DataAndFiles(Generic[_Data, _Files]):
    data: _Data
    files: _Files
    def __init__(self, data: _Data, files: _Files) -> None: ...

class BaseParser:
    media_type: str
    def parse(
        self, stream: IO[Any], media_type: str | None = ..., parser_context: Mapping[str, Any] | None = ...
    ) -> Mapping[Any, Any] | DataAndFiles: ...

class JSONParser(BaseParser):
    renderer_class: type[JSONRenderer]
    strict: bool
    def parse(
        self, stream: IO[Any], media_type: str | None = ..., parser_context: Mapping[str, Any] | None = ...
    ) -> dict[str, Any]: ...

class FormParser(BaseParser):
    def parse(
        self, stream: IO[Any], media_type: str | None = ..., parser_context: Mapping[str, Any] | None = ...
    ) -> _ImmutableQueryDict: ...

class MultiPartParser(BaseParser):
    def parse(
        self, stream: IO[Any], media_type: str | None = ..., parser_context: Mapping[str, Any] | None = ...
    ) -> DataAndFiles[_ImmutableQueryDict, MultiValueDict]: ...

class FileUploadParser(BaseParser):
    errors: dict[str, str]
    def parse(
        self, stream: IO[Any], media_type: str | None = ..., parser_context: Mapping[str, Any] | None = ...
    ) -> DataAndFiles[None, Mapping[str, UploadedFile]]: ...
    def get_filename(self, stream: IO[Any], media_type: str | None, parser_context: Mapping[str, Any]) -> str: ...
    def get_encoded_filename(self, filename_parm: Mapping[str, Any]) -> str: ...
