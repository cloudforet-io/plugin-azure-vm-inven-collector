from spaceone.core.manager import BaseManager
from spaceone.inventory.model.disk import Disk, DiskTags
from spaceone.inventory.connector.azure_vm_connector import AzureVMConnector


class AzureDiskManager(BaseManager):

    def __init__(self, params, azure_vm_connector=None, **kwargs):
        super().__init__(**kwargs)
        self.params = params
        self.azure_vm_connector: AzureVMConnector = azure_vm_connector

    def get_disk_info(self, vms, resource_group_name):
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
        for vm in vms:
            os_disk = vm.storage_profile.os_disk

            volume_data = {
                'device_index': index,
                'device': '',
                'disk_type': 'disk',
                'size': os_disk.disk_size_gb,
                'tags': {
                    'disk_name': os_disk.name,
                    'caching': os_disk.caching,
                    'storage_account_type': os_disk.managed_disk.storage_account_type,
                    'disk_encryption_set': self.get_disk_encryption(os_disk),
                }
            }

            disk = self.get_iops_bps(os_disk, resource_group_name)
            volume_data['tags'].update({'iops': disk.disk_iops_read_write})
            volume_data['tags'].update({'throughput_mbps': disk.disk_m_bps_read_write})

            disk_data.append(Disk(volume_data, strict=False))
            index += 1

        return disk_data

    def get_iops_bps(self, os_disk, resource_group_name):
        disk_name = os_disk.managed_disk.id.split('/')[-1]
        disk = self.azure_vm_connector.list_disks(resource_group_name, disk_name)
        return disk

    @staticmethod
    def get_disk_encryption(os_disk):
        if os_disk.managed_disk.disk_encryption_set:
            return 'CMK'
        else:
            return 'PMK'
