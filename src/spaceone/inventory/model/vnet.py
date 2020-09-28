from schematics import Model
from schematics.types import StringType


class VNet(Model):
    vnet_id = StringType()
    vnet_name = StringType()
    cidr = StringType()
    # TODO
    pass
