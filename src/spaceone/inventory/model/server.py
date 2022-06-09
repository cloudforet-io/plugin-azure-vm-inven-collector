from schematics import Model
from schematics.types import serializable, ModelType, ListType, StringType, FloatType, DateTimeType
from spaceone.inventory.model import OS, Azure, Hardware, SecurityGroup, Compute, LoadBalancer, VNet, Subnet, \
    NIC, Disk, ServerMetadata, Monitor, VMSS, Subscription, ResourceGroup


class ReferenceModel(Model):
    class Option:
        serialize_when_none = False

    resource_id = StringType(required=False, serialize_when_none=False)
    external_link = StringType(required=False, serialize_when_none=False)


class Tags(Model):
    key = StringType(serialize_when_none=False)
    value = StringType(serialize_when_none=False)


class ServerData(Model):
    os = ModelType(OS)
    azure = ModelType(Azure)
    hardware = ModelType(Hardware)
    security_group = ListType(ModelType(SecurityGroup))
    compute = ModelType(Compute)
    load_balancer = ListType(ModelType(LoadBalancer))
    vnet = ModelType(VNet)
    subnet = ModelType(Subnet)
    vmss = ModelType(VMSS, serialize_when_none=False)
    azure_monitor = ModelType(Monitor, serialize_when_none=False)
    primary_ip_address = StringType(default='')
    disks = ListType(ModelType(Disk))
    nics = ListType(ModelType(NIC))
    subscription = ModelType(Subscription)
    resource_group = ModelType(ResourceGroup)


class Server(Model):
    name = StringType()
    region_code = StringType()
    data = ModelType(ServerData)
    tags = ListType(ModelType(Tags))
    ip_addresses = ListType(StringType())
    server_type = StringType(default='VM')
    provider = StringType(default='azure')
    cloud_service_type = StringType(default='VirtualMachine')
    cloud_service_group = StringType(default='Compute')
    _metadata = ModelType(ServerMetadata, serialized_name='metadata')
    reference = ModelType(ReferenceModel)
    account = StringType(serialize_when_none=False)
    instance_type = StringType(serialize_when_none=False)
    instance_size = FloatType(serialize_when_none=False)
    launched_at = DateTimeType(serialize_when_none=False)

