from spaceone.core.manager import BaseManager
from spaceone.inventory.model.security_group import SecurityGroup
from spaceone.inventory.connector.azure_vm_connector import AzureVMConnector


class AzureNetworkSecurityGroupManager(BaseManager):

    def __init__(self, params, azure_vm_connector=None, **kwargs):
        super().__init__(**kwargs)
        self.params = params
        self.azure_vm_connector: AzureVMConnector = azure_vm_connector

    def get_network_security_group_info(self, nsg):
        '''
        nsg_data = {

        }
        '''

        nsg_data = {}
        return SecurityGroup(nsg_data, strict=False)
