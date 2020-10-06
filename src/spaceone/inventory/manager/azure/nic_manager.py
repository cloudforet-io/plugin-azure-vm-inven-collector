from spaceone.core.manager import BaseManager
from spaceone.inventory.model.nic import NIC, NICTags
from spaceone.inventory.connector.azure_vm_connector import AzureVMConnector


class AzureNICManager(BaseManager):

    def __init__(self, params, azure_vm_connector=None, **kwargs):
        super().__init__(**kwargs)
        self.params = params
        self.azure_vm_connector: AzureVMConnector = azure_vm_connector

    def get_nic_info(self, nic):
        '''
        nic_data = {
            "device_index": 0,
            "device": "",
            "nic_type": "",
            "ip_addresses": [],
            "cidr": "",
            "mac_address": "",
            "public_ip_address": "",
            "tags": {
                "nic_id": ""
            }
        }
        '''

        nic_data = {}
        return NIC(nic_data, strict=False)
