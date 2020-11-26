from schematics import Model
from schematics.types import StringType, ModelType, ListType


class Monitor(Model):
    class Option:
        serialize_when_none = False

    resource_id = StringType()
