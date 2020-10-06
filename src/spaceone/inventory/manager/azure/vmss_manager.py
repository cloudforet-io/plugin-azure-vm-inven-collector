from spaceone.core.manager import BaseManager
from spaceone.inventory.model.vmss import VMSS
from spaceone.inventory.connector.azure_vm_connector import AzureVMConnector


class AzureVMScaleSetManager(BaseManager):

    def __init__(self, params, azure_vm_connector=None, **kwargs):
        super().__init__(**kwargs)
        self.params = params
        self.azure_vm_connector: AzureVMConnector = azure_vm_connector

    def get_vmss_info(self, vmss):
        '''
        vmss_data = {
            "scale_set_name": ""
            "capacity": ""
            "admin_username": ""
            "unique_id": ""
        }
        '''

        vmss_data = {}
        return VMSS(vmss_data, strict=False)

