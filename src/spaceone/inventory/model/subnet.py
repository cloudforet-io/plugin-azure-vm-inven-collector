from schematics import Model
from schematics.types import StringType


class Subnet(Model):
    subnet_name = StringType()
    subnet_id = StringType()
    cidr = StringType()
