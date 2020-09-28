from schematics import Model
from schematics.types import serializable, ModelType, ListType, StringType
from spaceone.inventory.model import OS, Azure, Hardware, SecurityGroup, Compute, LoadBalancer, VNet, Subnet, \
    NIC, Disk, ServerMetadata, Monitor, VMSS, Subscription, ResourceGroup


class ReferenceModel(Model):
    class Option:
        serialize_when_none = False

    resource_id = StringType(required=False, serialize_when_none=False)
    external_link = StringType(required=False, serialize_when_none=False)


class ServerData(Model):
    os = ModelType(OS)
    azure = ModelType(Azure)
    hardware = ModelType(Hardware)
    security_group = ListType(ModelType(SecurityGroup))
    compute = ModelType(Compute)
    load_balancer = ListType(ModelType(LoadBalancer))
    vnet = ModelType(VNet)
    subnet = ModelType(Subnet)
    vmss = ModelType(VMSS)
    # auto_scaling_group = ModelType(AutoScalingGroup, serialize_when_none=False) # TODO
    monitor = ModelType(Monitor)
    subscription = ModelType(Subscription)
    resource_group = ModelType(ResourceGroup)


class Server(Model):
    name = StringType()
    region_code = StringType()
    region_type = StringType(default='AZURE')
    data = ModelType(ServerData)
    nics = ListType(ModelType(NIC))
    disks = ListType(ModelType(Disk))
    primary_ip_address = StringType(default='')
    ip_addresses = ListType(StringType())
    server_type = StringType(default='VM')
    os_type = StringType(choices=('LINUX', 'WINDOWS'))
    provider = StringType(default='azure')
    _metadata = ModelType(ServerMetadata, serialized_name='metadata')
    reference = ModelType(ReferenceModel)

