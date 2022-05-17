from spaceone.core.manager import BaseManager
from spaceone.inventory.model.metadata.metadata import ServerMetadata, CloudServiceTypeMetadata
from spaceone.inventory.model.metadata.metadata_dynamic_layout import ItemDynamicLayout, TableDynamicLayout, \
    ListDynamicLayout
from spaceone.inventory.model.metadata.metadata_dynamic_field import TextDyField, EnumDyField, ListDyField, \
    DateTimeDyField, SizeField


class MetadataManager(BaseManager):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    @staticmethod
    def get_cloud_service_type_metadata():
        metadata = CloudServiceTypeMetadata.set_meta(
            fields=[
                TextDyField.data_source('Server ID', 'server_id'),
                TextDyField.data_source('Name', 'name'),
                TextDyField.data_source('Resource ID', 'reference.resource_id'),
                EnumDyField.data_source('Management State', 'state', default_state={
                    'safe': ['ACTIVE'], 'disable': ['DELETED']
                }, options={'is_optional': True}),
                TextDyField.data_source('Instance Type', 'data.compute.instance_type'),
                TextDyField.data_source('Core', 'data.hardware.core'),
                TextDyField.data_source('Memory', 'data.hardware.memory'),
                TextDyField.data_source('Provider', 'provider', reference={
                    'resource_type': 'identity.Provider',
                    'reference_key': 'provider'
                }),
                TextDyField.data_source('Cloud Service Group', 'cloud_service_group', options={
                    'is_optional': True
                }),
                TextDyField.data_source('Cloud Service Type', 'cloud_service_type', options={
                    'is_optional': True
                }),
                TextDyField.data_source('Instance ID', 'data.compute.instance_id', options={
                    'is_optional': True
                }),
                TextDyField.data_source('Key Pair', 'data.compute.keypair', options={
                    'is_optional': True
                }),
                TextDyField.data_source('Image', 'data.compute.image', options={
                    'is_optional': True
                }),
                TextDyField.data_source('Image', 'data.compute.image', options={
                    'is_optional': True
                }),
                EnumDyField.data_source('Instance State', 'data.compute.instance_state', default_state={
                    'safe': ['RUNNING'],
                    'warning': ['PENDING', 'REBOOTING', 'SHUTTING-DOWN', 'STOPPING', 'STARTING',
                                'PROVISIONING', 'STAGING', 'DEALLOCATING', 'REPAIRING'],
                    'alert': ['STOPPED', 'DEALLOCATED', 'SUSPENDED'],
                    'disable': ['TERMINATED']
                }, options={'is_optional': True}),
                TextDyField.data_source('Availability Zone', 'data.compute.az'),
                TextDyField.data_source('OS Type', 'data.os.os_type', options={
                    'is_optional': True
                }),
                TextDyField.data_source('OS', 'data.os.os_distro'),
                TextDyField.data_source('OS Architecture', 'data.os.os_arch', options={
                    'is_optional': True
                }),
                TextDyField.data_source('Primary IP', 'data.primary_ip_address'),
                TextDyField.data_source('Public IP', 'data.nics.public_ip_address'),
                TextDyField.data_source('Public DNS', 'data.tags.public_dns', options={
                    'is_optional': True
                }),
                TextDyField.data_source('All IP', 'ip_addresses', options={
                    'is_optional': True
                }),
                TextDyField.data_source('MAC Address', 'nics.mac_address', options={
                    'is_optional': True
                }),
                TextDyField.data_source('CIDR', 'nics.cidr', options={
                    'is_optional': True
                }),
                TextDyField.data_source('VPC ID', 'data.vpc.vpc_id', options={
                    'is_optional': True
                }),
                TextDyField.data_source('Subnet ID', 'data.subnet.subnet_id', options={
                    'is_optional': True
                }),
                TextDyField.data_source('Subnet Name', 'data.subnet.subnet_name', options={
                    'is_optional': True
                }),
                TextDyField.data_source('ELB Name', 'data.load_balancers.name', options={
                    'is_optional': True
                }),
                TextDyField.data_source('ELB DNS', 'data.load_balancers.dns', options={
                    'is_optional': True
                }),
                TextDyField.data_source('IAM Role ARN', 'data.aws.iam_instance_profile.arn', options={
                    'is_optional': True
                }),
                TextDyField.data_source('EC2 Lifecycle', 'data.aws.lifecycle', options={
                    'is_optional': True
                }),
                TextDyField.data_source('Auto Scaling Group', 'data.auto_scaling_group.name', options={
                    'is_optional': True
                }),
                TextDyField.data_source('CPU Utilization', 'data.monitoring.cpu.utilization.avg', options={
                    'default': 0,
                    'is_optional': True,
                    'field_description': '(Daily Average)'
                }),
                TextDyField.data_source('Memory Usage', 'data.monitoring.memory.usage.avg', options={
                    'default': 0,
                    'is_optional': True,
                    'field_description': '(Daily Average)'
                }),
                TextDyField.data_source('Disk Read IOPS', 'data.monitoring.disk.read_iops.avg', options={
                    'default': 0,
                    'is_optional': True,
                    'field_description': '(Daily Average)'
                }),
                TextDyField.data_source('Disk Write IOPS', 'data.monitoring.disk.write_iops.avg', options={
                    'default': 0,
                    'is_optional': True,
                    'field_description': '(Daily Average)'
                }),
                SizeField.data_source('Disk Read Throughput', 'data.monitoring.disk.read_throughput.avg', options={
                    'default': 0,
                    'is_optional': True,
                    'field_description': '(Daily Average)'
                }),
                SizeField.data_source('Disk Write Throughput', 'data.monitoring.disk.write_throughput.avg', options={
                    'default': 0,
                    'is_optional': True,
                    'field_description': '(Daily Average)'
                }),
                TextDyField.data_source('Network Received PPS', 'data.monitoring.network.received_pps.avg', options={
                    'default': 0,
                    'is_optional': True,
                    'field_description': '(Daily Average)'
                }),
                TextDyField.data_source('Network Send PPS', 'data.monitoring.network.sent_pps.avg', options={
                    'default': 0,
                    'is_optional': True,
                    'field_description': '(Daily Average)'
                }),
                SizeField.data_source('Network Received Throughput', 'data.monitoring.network.received_throughput.avg',
                                      options={
                                          'default': 0,
                                          'is_optional': True,
                                          'field_description': '(Daily Average)'
                                      }),
                SizeField.data_source('Network Sent Throughput', 'data.monitoring.network.sent_throughput.avg',
                                      options={
                                          'default': 0,
                                          'is_optional': True,
                                          'field_description': '(Daily Average)'
                                      }),
                TextDyField.data_source('CPU Utilization', 'data.monitoring.cpu.utilization.max', options={
                    'default': 0,
                    'is_optional': True,
                    'field_description': '(Daily Max)'
                }),
                TextDyField.data_source('Memory Usage', 'data.monitoring.memory.usage.max', options={
                    'default': 0,
                    'is_optional': True,
                    'field_description': '(Daily Max)'
                }),
                TextDyField.data_source('Disk Read IOPS', 'data.monitoring.disk.read_iops.max', options={
                    'default': 0,
                    'is_optional': True,
                    'field_description': '(Daily Max)'
                }),
                TextDyField.data_source('Disk Write IOPS', 'data.monitoring.disk.write_iops.max', options={
                    'default': 0,
                    'is_optional': True,
                    'field_description': '(Daily Max)'
                }),
                SizeField.data_source('Disk Read Throughput', 'data.monitoring.disk.read_throughput.max', options={
                    'default': 0,
                    'is_optional': True,
                    'field_description': '(Daily Max)'
                }),
                SizeField.data_source('Disk Write Throughput', 'data.monitoring.disk.write_throughput.max', options={
                    'default': 0,
                    'is_optional': True,
                    'field_description': '(Daily Max)'
                }),
                TextDyField.data_source('Network Received PPS', 'data.monitoring.network.received_pps.max', options={
                    'default': 0,
                    'is_optional': True,
                    'field_description': '(Daily Max)'
                }),
                TextDyField.data_source('Network Send PPS', 'data.monitoring.network.sent_pps.max', options={
                    'default': 0,
                    'is_optional': True,
                    'field_description': '(Daily Max)'
                }),
                SizeField.data_source('Network Received Throughput', 'data.monitoring.network.received_throughput.max',
                                      options={
                                          'default': 0,
                                          'is_optional': True,
                                          'field_description': '(Daily Max)'
                                      }),
                SizeField.data_source('Network Sent Throughput', 'data.monitoring.network.sent_throughput.max',
                                      options={
                                          'default': 0,
                                          'is_optional': True,
                                          'field_description': '(Daily Max)'
                                      }),
                TextDyField.data_source('Account ID', 'account'),
                TextDyField.data_source('Region', 'region_code',
                                        options={'is_optional': True},
                                        reference={'resource_type': 'inventory.Region',
                                                   'reference_key': 'region_code'}),
                TextDyField.data_source('Project', 'project_id',
                                        options={'sortable': False},
                                        reference={'resource_type': 'inventory.Project',
                                                   'reference_key': 'project_id'}),
                TextDyField.data_source('Service Accounts', 'collection_info.service_accounts',
                                        options={'is_optional': True},
                                        reference={'resource_type': 'inventory.ServiceAccount',
                                                   'reference_key': 'service_account_id'}),
                TextDyField.data_source('Secrets', 'collection_info.secrets',
                                        options={'is_optional': True},
                                        reference={'resource_type': 'secret.Secret',
                                                   'reference_key': 'secret_id'}),
                TextDyField.data_source('Collectors', 'collection_info.collectors',
                                        options={'is_optional': True},
                                        reference={'resource_type': 'inventory.Collector',
                                                   'reference_key': 'collector_id'}),
                TextDyField.data_source('Launched', 'launched_at', options={'is_optional': True}),
                DateTimeDyField.data_source('Last Collected', 'updated_at', options={'source_type': "iso8601"}),
                DateTimeDyField.data_source('Created', 'created_at', options={
                    'source_type': "iso8601",
                    'is_optional': True
                }),
                DateTimeDyField.data_source('Deleted', 'deleted_at', options={
                    'source_type': "iso8601",
                    'is_optional': True
                })
            ]
        )

        return metadata

    @staticmethod
    def get_server_metadata():
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

        vm_os = ItemDynamicLayout.set_fields('Operating System', fields=[
            TextDyField.data_source('OS Type', 'data.os.os_type', options={
                'translation_id': 'PAGE_SCHEMA.OS_TYPE'
            }),
            TextDyField.data_source('OS Distribution', 'data.os.os_distro', options={
                'translation_id': 'PAGE_SCHEMA.OS_DISTRO',
            }),
            TextDyField.data_source('OS Architecture', 'data.os.os_arch', options={
                'translation_id': 'PAGE_SCHEMA.OS_ARCH',
            }),
            TextDyField.data_source('OS Version Details', 'data.os.details', options={
                'translation_id': 'PAGE_SCHEMA.OS_DETAILS',
            }),
            TextDyField.data_source('OS License', 'data.os.os_license', options={
                'translation_id': 'PAGE_SCHEMA.OS_LICENSE',
            }),
        ])

        vm_hw = ItemDynamicLayout.set_fields('Hardware', fields=[
            TextDyField.data_source('Core', 'data.hardware.core', options={
                'translation_id': 'PAGE_SCHEMA.CPU_CORE',
            }),
            TextDyField.data_source('Memory', 'data.hardware.memory', options={
                'translation_id': 'PAGE_SCHEMA.MEMORY',
            }),
        ])

        azure_vm = ListDynamicLayout.set_layouts('Azure VM', layouts=[virtual_machine, vm_os, vm_hw, vnet])

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
            EnumDyField.data_source('Enable Accelerated Networking', 'tags.enable_accelerated_networking',
                                    default_badge={
                                        'indigo.500': ['true'], 'coral.600': ['false']
                                    }),
            EnumDyField.data_source('Enable IP Forwarding', 'tags.enable_ip_forwarding', default_badge={
                'indigo.500': ['true'], 'coral.600': ['false']
            }),
        ])

        security_group = TableDynamicLayout.set_fields('Network Security Groups', root_path='data.security_group',
                                                       fields=[
                                                           EnumDyField.data_source('Direction', 'direction',
                                                                                   default_badge={
                                                                                       'indigo.500': ['inbound'],
                                                                                       'coral.600': ['outbound']
                                                                                   }),
                                                           TextDyField.data_source('Name', 'security_group_name'),
                                                           EnumDyField.data_source('Protocol', 'protocol',
                                                                                   default_outline_badge=['ALL', 'TCP',
                                                                                                          'UDP',
                                                                                                          'ICMP']),
                                                           TextDyField.data_source('Port Range', 'port'),
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

        return ServerMetadata.set_layouts([azure_vm, tags, disk, nic, security_group, lb])
