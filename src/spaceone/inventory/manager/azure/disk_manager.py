from spaceone.core.manager import BaseManager
from spaceone.inventory.model.disk import Disk, DiskTags
from spaceone.inventory.connector.azure_vm_connector import AzureVMConnector


class AzureDiskManager(BaseManager):

    def __init__(self, params, azure_vm_connector=None, **kwargs):
        super().__init__(**kwargs)
        self.params = params
        self.azure_vm_connector: AzureVMConnector = azure_vm_connector

    def get_disk_info(self, disk):
        '''
        disk_data = {
            "device_index": 0,
            "device": "",
            "disk_type": "EBS",
            "size": 100,
            "tags": {
                "disk_name": "",
                "caching": "None" | "ReadOnly" | "ReadWrite"
                "storage_account_type": "Standard_LRS" | "Premium_LRS" | "StandardSSD_LRS" | "UltraSSD_LRS"
                "disk_encryption_set": "PMK" | "CMK"
            }
        }
        '''

        disk_data = {}
        return Disk(disk_data, strict=False)
