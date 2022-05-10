from schematics import Model
from schematics.types import ListType, StringType, PolyModelType, DictType, BooleanType


class CloudServiceType(Model):
    name = StringType(default='VirtualMachine')
    provider = StringType(default='azure')
    group = StringType(default='Compute')
    labels = ListType(StringType(), serialize_when_none=False, default=['Compute', 'Server'])
    tags = DictType(StringType, serialize_when_none=False)
    is_primary = BooleanType(default=True)
    is_major = BooleanType(default=True)
    resource_type = StringType(default='inventory.CloudService')
    service_code = StringType(default='Microsoft.Compute/virtualMachines')
