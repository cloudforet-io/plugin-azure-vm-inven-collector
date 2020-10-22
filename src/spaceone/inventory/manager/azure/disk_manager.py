from spaceone.core.manager import BaseManager
from spaceone.inventory.model.disk import Disk, DiskTags
from spaceone.inventory.connector.azure_vm_connector import AzureVMConnector

import pprint


class AzureDiskManager(BaseManager):

    def __init__(self, params, azure_vm_connector=None, **kwargs):
        super().__init__(**kwargs)
        self.params = params
        self.azure_vm_connector: AzureVMConnector = azure_vm_connector

    def get_disk_info(self, vm, resource_group_name):
        '''
        disk_data = {
            "device_index": 0,
            "device": "",
            "disk_type": "disk",
            "size": 100,
            "tags": {
                "disk_name": "",
                "caching": "None" | "ReadOnly" | "ReadWrite"
                "storage_account_type": "Standard_LRS" | "Premium_LRS" | "StandardSSD_LRS" | "UltraSSD_LRS"
                "disk_encryption_set": "PMK" | "CMK"
                "iops": 60,
                "throughput_mbps": 200
            }
        }
        '''

        disk_data = []
        index = 0

        os_disk = vm.storage_profile.os_disk

        volume_data = {
            'device_index': index,
            'disk_type': 'os_disk',
            'size': os_disk.disk_size_gb,
            'tags': {
                'disk_name': os_disk.name,
                'caching': os_disk.caching,
                'storage_account_type': os_disk.managed_disk.storage_account_type,
                'disk_encryption_set': self.get_disk_encryption(os_disk),
             }
        }

        disk = self.get_iops_bps(os_disk, resource_group_name)

        volume_data['tags'].update({
            'iops': disk.disk_iops_read_write,
            'throughput_mbps': disk.disk_m_bps_read_write
        })

        disk_data.append(Disk(volume_data, strict=False))
        index += 1

        data_disks = vm.storage_profile.data_disks

        if data_disks:
            for data_disk in data_disks:
                volume_data_sub = {
                    'device_index': index,
                    'disk_type': 'data_disk',
                    'size': data_disk.disk_size_gb,
                    'tags': {
                        'disk_name': data_disk.name,
                        'caching': data_disk.caching,
                        'storage_account_type': data_disk.managed_disk.storage_account_type,
                        'disk_encryption_set': self.get_disk_encryption(data_disk),
                    }
                }

                disk_sub = self.get_iops_bps(data_disk, resource_group_name)
                volume_data_sub['tags'].update({'iops': disk_sub.disk_iops_read_write})
                volume_data_sub['tags'].update({'throughput_mbps': disk_sub.disk_m_bps_read_write})

                disk_data.append(Disk(volume_data_sub, strict=False))
                index += 1

        return disk_data

    def get_iops_bps(self, disk, resource_group_name):
        disk_name = disk.managed_disk.id.split('/')[-1]
        disk = self.azure_vm_connector.list_disk(resource_group_name, disk_name)
        return disk

    @staticmethod
    def get_disk_encryption(disk):
        if disk.managed_disk.disk_encryption_set:
            return 'CMK'
        else:
            return 'PMK'
