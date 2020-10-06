from spaceone.core.manager import BaseManager
from spaceone.inventory.model.resource_group import ResourceGroup
from spaceone.inventory.connector.azure_vm_connector import AzureVMConnector


class AzureResourceGroupManager(BaseManager):

    def __init__(self, params, azure_vm_connector=None, **kwargs):
        super().__init__(**kwargs)
        self.params = params
        self.azure_vm_connector: AzureVMConnector = azure_vm_connector

    def list_all_resource_groups(self):
        return self.azure_vm_connector.list_resource_groups()

    @staticmethod
    def get_resource_group_info(resource_group):
        """
        resource_group_data = {
            "resource_group_name": "name",
            "resource_group_id": "id"
        }
        """

        rg_info = {
            'resource_group_name': resource_group.name,
            'resource_group_id': resource_group.id
        }

        return ResourceGroup(rg_info, strict=False)
