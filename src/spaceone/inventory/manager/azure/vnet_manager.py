from spaceone.core.manager import BaseManager
from spaceone.inventory.model.vnet import VNet
from spaceone.inventory.model.subnet import Subnet
from spaceone.inventory.connector.azure_vm_connector import AzureVMConnector


class AzureVNetManager(BaseManager):

    def __init__(self, params, azure_vm_connector=None, **kwargs):
        super().__init__(**kwargs)
        self.params = params
        self.azure_vm_connector: AzureVMConnector = azure_vm_connector

    def get_vnet_info(self, vnet):
        '''
        vnet_data = {

        }
        '''

        vnet_data = {}
        return VNet(vnet_data, strict=False)

    def get_subnet_info(self, subnet):
        '''
        subnet_data = {
            "subnet_name": "",
            "subnet_id": "",
            "cidr": ""
        }
        '''

        subnet_data = {}
        return Subnet(subnet_data, strict=False)
