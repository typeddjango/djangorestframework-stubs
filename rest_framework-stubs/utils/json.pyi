from json import JSONDecoder, JSONEncoder
from typing import IO, Any, Callable, NoReturn

def strict_constant(o: Any) -> NoReturn: ...
def dump(
    obj: Any,
    fp: IO[str],
    *,
    skipkeys: bool = False,
    ensure_ascii: bool = True,
    check_circular: bool = True,
    allow_nan: bool = True,
    cls: type[JSONEncoder] | None = None,
    indent: int | str | None = None,
    separators: tuple[str, str] | None = None,
    default: Callable[[Any], Any] | None = None,
    sort_keys: bool = False,
    **kw: Any,
) -> None: ...
def dumps(
    obj: Any,
    *,
    skipkeys: bool = False,
    ensure_ascii: bool = True,
    check_circular: bool = True,
    allow_nan: bool = True,
    cls: type[JSONEncoder] | None = None,
    indent: int | str | None = None,
    separators: tuple[str, str] | None = None,
    default: Callable[[Any], Any] | None = None,
    sort_keys: bool = False,
    **kw: Any,
) -> str: ...
def load(
    fp: IO[str],
    *,
    cls: type[JSONDecoder] | None = None,
    object_hook: Callable[[dict[str, Any]], Any] | None = None,
    parse_float: Callable[[str], Any] | None = None,
    parse_int: Callable[[str], Any] | None = None,
    parse_constant: Callable[[str], Any] | None = None,
    object_pairs_hook: Callable[[list[tuple[str, Any]]], Any] | None = None,
    **kw: Any,
) -> Any: ...
def loads(
    s: str,
    *,
    cls: type[JSONDecoder] | None = None,
    object_hook: Callable[[dict[str, Any]], Any] | None = None,
    parse_float: Callable[[str], Any] | None = None,
    parse_int: Callable[[str], Any] | None = None,
    parse_constant: Callable[[str], Any] | None = None,
    object_pairs_hook: Callable[[list[tuple[str, Any]]], Any] | None = None,
    **kw: Any,
) -> Any: ...
