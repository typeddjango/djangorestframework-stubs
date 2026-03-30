import datetime
import json
from typing import Any

from typing_extensions import override
from yaml import Dumper, ScalarNode

class JSONEncoder(json.JSONEncoder):
    @override
    def default(self, obj: Any) -> Any: ...

class CustomScalar:
    @classmethod
    def represent_timedelta(cls, dumper: Dumper, data: datetime.timedelta) -> ScalarNode: ...
