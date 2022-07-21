from schematics import Model
from schematics.types import StringType


class Monitor(Model):
    resource_id = StringType()
