from spaceone.core.manager import BaseManager
from spaceone.inventory.model.metadata.metadata import ServerMetadata
from spaceone.inventory.model.metadata.metadata_dynamic_layout import ItemDynamicLayout, TableDynamicLayout, \
    ListDynamicLayout
from spaceone.inventory.model.metadata.metadata_dynamic_field import TextDyField, EnumDyField, ListDyField, \
    DateTimeDyField, SizeField

virtual_machine = ItemDynamicLayout.set_fields('Virtual Machine', fields=[
    TextDyField.data_source('Resource ID', 'data.compute.instance_id'),
    TextDyField.data_source('VM ID', 'data.compute.tags.vm_id'),
    EnumDyField.data_source('VM State', 'data.compute.instance_state', default_state={
        'safe': ['RUNNING'],
        'warning': ['STARTING', 'DEALLOCATING', 'STOPPING', 'DEALLOCATING'],
        'disable': ['DEALLOCATED'],
        'alert': ['STOPPED']
    }),
    TextDyField.data_source('Instance Type', 'data.compute.instance_type'),
    TextDyField.data_source('Image', 'data.compute.image'),
    EnumDyField.data_source('Azure Priority', 'data.azure.priority', default_badge={
        'indigo.500': ['Regular'], 'coral.600': ['Low'], 'peacock.600': ['Spot']
    }),
    TextDyField.data_source('Region', 'region_code'),
    TextDyField.data_source('Availability Zone', 'data.compute.az'),
    TextDyField.data_source('Key Pair', 'data.compute.keypair'),
    EnumDyField.data_source('Ultra SSD Enabled', 'data.azure.ultra_ssd_enabled', default_badge={
        'indigo.500': ['true'], 'coral.600': ['false'],
    }),
    EnumDyField.data_source('Write Accelerator Enabled', 'data.azure.write_accelerator_enabled', default_badge={
        'indigo.500': ['true'], 'coral.600': ['false']
    }),
    EnumDyField.data_source('Boot Diagnostics', 'data.azure.boot_diagnostics', default_badge={
        'indigo.500': ['true'], 'coral.600': ['false']
    }),
    ListDyField.data_source('Public IP', 'nics',
                            default_badge={'type': 'outline', 'sub_key': 'public_ip_address'}),
    ListDyField.data_source('Security Groups', 'data.compute.security_groups',
                            default_badge={'type': 'outline', 'delimiter': '<br>', 'sub_key': 'display'}),
    DateTimeDyField.data_source('Launched At', 'data.compute.launched_at'),
])

vnet = ItemDynamicLayout.set_fields('Virtual Network', fields=[
    TextDyField.data_source('VNet ID', 'data.vnet.vnet_id'),
    TextDyField.data_source('VNet Name', 'data.vnet.vnet_name'),
    TextDyField.data_source('Subnet ID', 'data.subnet.subnet_id'),
    TextDyField.data_source('Subnet Name', 'data.subnet.subnet_name'),
])

azure_vm = ListDynamicLayout.set_layouts('Azure VM', layouts=[virtual_machine, vnet])

disk = TableDynamicLayout.set_fields('Disk', root_path='disks', fields=[
    TextDyField.data_source('Index', 'device_index'),
    TextDyField.data_source('Name', 'tags.disk_name'),
    SizeField.data_source('Size', 'size'),
    TextDyField.data_source('Disk ID', 'tags.disk_id'),
    TextDyField.data_source('Storage Account Type', 'tags.storage_Account_type'),
    TextDyField.data_source('IOPS', 'tags.iops'),
    TextDyField.data_source('Throughput (mbps)', 'tags.throughput_mbps'),
    TextDyField.data_source('Encryption Set', 'tags.disk_encryption_set'),
    TextDyField.data_source('Caching', 'tags.caching'),
])

nic = TableDynamicLayout.set_fields('NIC', root_path='nics', fields=[
    TextDyField.data_source('Index', 'device_index'),
    TextDyField.data_source('Name', 'tags.name'),
    ListDyField.data_source('IP Addresses', 'ip_addresses', options={'delimiter': '<br>'}),
    TextDyField.data_source('Public IP', 'public_ip_address'),
    TextDyField.data_source('MAC Address', 'mac_address'),
    TextDyField.data_source('CIDR', 'cidr'),
    TextDyField.data_source('etag', 'tags.etag'),
    EnumDyField.data_source('Enable Accelerated Networking', 'tags.enable_accelerated_networking', default_badge={
        'indigo.500': ['true'], 'coral.600': ['false']
    }),
    EnumDyField.data_source('Enable IP Forwarding', 'tags.enable_ip_forwarding', default_badge={
        'indigo.500': ['true'], 'coral.600': ['false']
    }),
])

security_group = TableDynamicLayout.set_fields('Network Security Groups', root_path='data.security_group', fields=[
    EnumDyField.data_source('Direction', 'direction', default_badge={
        'indigo.500': ['inbound'], 'coral.600': ['outbound']
    }),
    TextDyField.data_source('Name', 'security_group_name'),
    EnumDyField.data_source('Protocol', 'protocol', default_outline_badge=['ALL', 'TCP', 'UDP', 'ICMP']),
    TextDyField.data_source('Port Rage', 'port'),
    TextDyField.data_source('Remote', 'remote'),
    TextDyField.data_source('Priority', 'priority'),
    EnumDyField.data_source('Action', 'action', default_badge={
        'indigo.500': ['allow'], 'coral.600': ['deny']
    }),
    TextDyField.data_source('Description', 'description'),
])

lb = TableDynamicLayout.set_fields('Load Balancer', root_path='data.load_balancer', fields=[
    TextDyField.data_source('Name', 'name'),
    TextDyField.data_source('Endpoint', 'endpoint'),
    EnumDyField.data_source('Type', 'type', default_badge={
        'indigo.500': ['network'], 'coral.600': ['application']
    }),
    ListDyField.data_source('Protocol', 'protocol', options={'delimiter': '<br>'}),
    ListDyField.data_source('Port', 'port', options={'delimiter': '<br>'}),
    EnumDyField.data_source('Scheme', 'scheme', default_badge={
        'indigo.500': ['internet-facing'], 'coral.600': ['internal']
    }),
])

tags = TableDynamicLayout.set_fields('Azure Tags', root_path='data.azure.tags', fields=[
    TextDyField.data_source('Key', 'key'),
    TextDyField.data_source('Value', 'value'),
])

metadata = ServerMetadata.set_layouts([azure_vm, tags, disk, nic, security_group, lb])


class MetadataManager(BaseManager):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.metadata = metadata

    def get_metadata(self):
        return self.metadata
