from schematics import Model
from schematics.types import StringType


class ResourceGroup(Model):
    resource_group_name = StringType()
    resource_group_id = StringType()

