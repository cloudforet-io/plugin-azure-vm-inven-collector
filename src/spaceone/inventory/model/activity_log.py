from schematics import Model
from schematics.types import StringType


class ActivityLog(Model):
    resource_uri = StringType()
