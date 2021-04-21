from schematics import Model
from schematics.types import serializable, ModelType, ListType, StringType
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
    subscription = ModelType(Subscription)
    resource_group = ModelType(ResourceGroup)


class Server(Model):
    name = StringType()
    region_code = StringType()
    data = ModelType(ServerData)
    tags = ListType(ModelType(Tags))
    nics = ListType(ModelType(NIC))
    disks = ListType(ModelType(Disk))
    primary_ip_address = StringType(default='')
    ip_addresses = ListType(StringType())
    server_type = StringType(default='VM')
    os_type = StringType(choices=('LINUX', 'WINDOWS'))
    provider = StringType(default='azure')
    cloud_service_type = StringType(default='VirtualMachine')
    cloud_service_group = StringType(default='Compute')
    _metadata = ModelType(ServerMetadata, serialized_name='metadata')
    reference = ModelType(ReferenceModel)
