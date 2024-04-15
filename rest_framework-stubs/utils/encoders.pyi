import datetime
import json

from yaml import Dumper, ScalarNode

class JSONEncoder(json.JSONEncoder): ...

class CustomScalar:
    @classmethod
    def represent_timedelta(cls, dumper: Dumper, data: datetime.timedelta) -> ScalarNode: ...
