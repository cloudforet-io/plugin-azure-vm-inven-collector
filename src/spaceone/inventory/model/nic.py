from schematics import Model
from schematics.types import StringType, IntType, ListType, DictType, ModelType, BooleanType


class NICTags(Model):
    name = StringType()
    etag = StringType()
    enable_accelerated_networking = BooleanType(default=False)
    enable_ip_forwarding = BooleanType(default=False)


class NIC(Model):
    device_index = IntType()
    device = StringType(default="")
    nic_type = StringType()
    ip_addresses = ListType(StringType())
    cidr = StringType()
    mac_address = StringType()
    public_ip_address = StringType()
    tags = ModelType(NICTags, default={})
