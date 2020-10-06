from spaceone.core.manager import BaseManager
from spaceone.inventory.model.load_balancer import LoadBalancer
from spaceone.inventory.connector.azure_vm_connector import AzureVMConnector


class AzureLoadBalancerManager(BaseManager):

    def __init__(self, params, azure_vm_connector=None, **kwargs):
        super().__init__(**kwargs)
        self.params = params
        self.azure_vm_connector: AzureVMConnector = azure_vm_connector

    def get_load_balancer_info(self, lb):
        '''
        lb_data = {

        }
        '''

        lb_data = {}
        return LoadBalancer(lb_data, strict=False)
