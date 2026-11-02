from _typeshed import SupportsWrite
from collections.abc import Callable
from json import JSONEncoder

# Reuse stdlib signatures for following functions (different across Python versions)
from json import load as load
from json import loads as loads
from typing import Any, NoReturn

def strict_constant(o: Any) -> NoReturn: ...
def dump(
    obj: Any,
    fp: SupportsWrite[str],
    *,
    skipkeys: bool = False,
    ensure_ascii: bool = True,
    check_circular: bool = True,
    allow_nan: bool = False,  # DRF overrides the stdlib default to False.
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
    allow_nan: bool = False,  # DRF overrides the stdlib default to False.
    cls: type[JSONEncoder] | None = None,
    indent: int | str | None = None,
    separators: tuple[str, str] | None = None,
    default: Callable[[Any], Any] | None = None,
    sort_keys: bool = False,
    **kw: Any,
) -> str: ...
