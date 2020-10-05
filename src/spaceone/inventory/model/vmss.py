from schematics import Model
from schematics.types import StringType, IntType


class VMSS(Model):
    scale_set_name = StringType()
    capacity = IntType()
    admin_username = StringType()
    unique_id = StringType()

