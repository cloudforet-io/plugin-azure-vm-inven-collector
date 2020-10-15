__all__ = ['CollectorManager']

import time
import logging
from spaceone.core.manager import BaseManager
from spaceone.inventory.connector import AzureVMConnector
from spaceone.inventory.manager.azure import AzureDiskManager, AzureLoadBalancerManager, \
    AzureNetworkSecurityGroupManager, AzureNICManager, AzureResourceGroupManager, AzureVmManager, \
    AzureVMScaleSetManager, AzureVNetManager
from spaceone.inventory.manager.metadata.metadata_manager import MetadataManager
from spaceone.inventory.model.server import Server, ReferenceModel
from spaceone.inventory.model.region import Region


_LOGGER = logging.getLogger(__name__)


class CollectorManager(BaseManager):

    def __init__(self, transaction):
        super().__init__(transaction)
        # self.azure_vm_connector: AzureVMConnector = self.locator.get_connector('AzureVMConnector')

    def verify(self, options, secret_data):
        """ Check connection
        """
        azure_vm_connector = self.locator.get_connector('AzureVMConnector')
        r = azure_vm_connector.verify(options, secret_data)
        # ACTIVE/UNKNOWN
        return r

    def list_all_resource_groups(self, params):
        azure_vm_connector: AzureVMConnector = self.locator.get_connector('AzureVMConnector')
        azure_vm_connector.set_connect(params['secret_data'])

        rg_manager: AzureResourceGroupManager = AzureResourceGroupManager(params, azure_vm_connector=azure_vm_connector)
        return rg_manager.list_all_resource_groups()

    def list_vms(self, params, resource_group_name):
        azure_vm_connector: AzureVMConnector = self.locator.get_connector('AzureVMConnector')
        azure_vm_connector.set_connect(params['secret_data'])

        vm_manager: AzureVmManager = AzureVmManager(params, azure_vm_connector=azure_vm_connector)
        return vm_manager.list_vms(resource_group_name)

    def list_all_resources(self, params):
        server_vos = []
        azure_vm_connector: AzureVMConnector = self.locator.get_connector('AzureVMConnector')
        azure_vm_connector.set_connect(params['secret_data'])

        resource_group_name = params['resource_group'].name
        print(resource_group_name)

        # call all managers
        vm_manager: AzureVmManager = AzureVmManager(params, azure_vm_connector=azure_vm_connector)
        disk_manager: AzureDiskManager = AzureDiskManager(params, azure_vm_connector=azure_vm_connector)
        load_balancer_manager: AzureLoadBalancerManager = AzureLoadBalancerManager(params, azure_vm_connector=azure_vm_connector)
        network_security_group_manager: AzureNetworkSecurityGroupManager = AzureNetworkSecurityGroupManager(params, azure_vm_connector=azure_vm_connector)
        nic_manager: AzureNICManager = AzureNICManager(params, azure_vm_connector=azure_vm_connector)
        resource_group_manager: AzureResourceGroupManager(params, azure_vm_connector=azure_vm_connector)
        vmss_manager: AzureVMScaleSetManager = AzureVMScaleSetManager(params, azure_vm_connector=azure_vm_connector)
        vnet_manager: AzureVNetManager = AzureVNetManager(params, azure_vm_connector=azure_vm_connector)

        # VM list in resource group
        # vms = azure_vm_connector.list_vms_in_rg(resource_group_name)
        # vms = azure_vm_connector.list_vms(resource_group_name)
        vms = params['vms']

        disk_vos = disk_manager.get_disk_info(vms, resource_group_name)

        for vm in vms:
            print(vm)
            server_data = vm_manager.get_vm_info(vm, resource_group_name)

        # server_vos.append(Server(server_data), strict=False)

        return server_vos

    def list_resources(self, params):
        """ Get list of resources
        Args:
            params:
                - resource_group
                - vms

        Returns: list of resources
        """
        start_time = time.time()

        try:
            resources = self.list_all_resources(params)
            print(f'   [{params["resource_group"]}] Finished {time.time() - start_time} Seconds')
            return resources

        except Exception as e:
            print(f'[ERROR: {params["resource_group"]}] : {e}')
            raise e

    @staticmethod
    def get_region_from_result(result):
        REGION_INFO = {
            'us-east-1': {'name': 'US East (N. Virginia)', 'tags': {'latitude': '39.028760', 'longitude': '-77.458263'}},
            'us-east-2': {'name': 'US East (Ohio)', 'tags': {'latitude': '40.103564', 'longitude': '-83.200092'}},
            'us-west-1': {'name': 'US West (N. California)', 'tags': {'latitude': '37.242183', 'longitude': '-121.783380'}},
            'us-west-2': {'name': 'US West (Oregon)', 'tags': {'latitude': '45.841046', 'longitude': '-119.658093'}},
            'af-south-1': {'name': 'Africa (Cape Town)', 'tags': {'latitude': '-33.932268', 'longitude': '18.424434'}},
            'ap-east-1': {'name': 'Asia Pacific (Hong Kong)', 'tags': {'latitude': '22.365560', 'longitude': '114.119420'}},
            'ap-south-1': {'name': 'Asia Pacific (Mumbai)', 'tags': {'latitude': '19.147428', 'longitude': '73.013805'}},
            'ap-northeast-3': {'name': 'Asia Pacific (Osaka-Local)', 'tags': {'latitude': '34.675638', 'longitude': '135.495706'}},
            'ap-northeast-2': {'name': 'Asia Pacific (Seoul)', 'tags': {'latitude': '37.528547', 'longitude': '126.871867'}},
            'ap-southeast-1': {'name': 'Asia Pacific (Singapore)', 'tags': {'latitude': '1.321259', 'longitude': '103.695942'}},
            'ap-southeast-2	': {'name': 'Asia Pacific (Sydney)', 'tags': {'latitude': '-33.921423', 'longitude': '151.188076'}},
            'ap-northeast-1': {'name': 'Asia Pacific (Tokyo)', 'tags': {'latitude': '35.648411', 'longitude': '139.792566'}},
            'ca-central-1': {'name': 'Canada (Central)', 'tags': {'latitude': '43.650803', 'longitude': '-79.361824'}},
            'cn-north-1': {'name': 'China (Beijing)', 'tags': {'latitude': '39.919635', 'longitude': '116.307237'}},
            'cn-northwest-1': {'name': 'China (Ningxia)', 'tags': {'latitude': '37.354511', 'longitude': '106.106147'}},
            'eu-central-1': {'name': 'Europe (Frankfurt)', 'tags': {'latitude': '50.098645', 'longitude': '8.632262'}},
            'eu-west-1': {'name': 'Europe (Ireland)', 'tags': {'latitude': '53.330893', 'longitude': '-6.362217'}},
            'eu-west-2': {'name': 'Europe (London)', 'tags': {'latitude': '51.519749', 'longitude': '-0.087804'}},
            'eu-south-1': {'name': 'Europe (Milan)', 'tags': {'latitude': '45.448648', 'longitude': '9.147316'}},
            'eu-west-3': {'name': 'Europe (Paris)', 'tags': {'latitude': '48.905302', 'longitude': '2.369778'}},
            'eu-north-1': {'name': 'Europe (Stockholm)', 'tags': {'latitude': '59.263542', 'longitude': '18.104861'}},
            'me-south-1': {'name': 'Middle East (Bahrain)', 'tags': {'latitude': '26.240945', 'longitude': '50.586321'}},
            'sa-east-1': {'name': 'South America (São Paulo)', 'tags': {'latitude': '-23.493549', 'longitude': '-46.809319'}},
            'us-gov-east-1': {'name': 'AWS GovCloud (US-East)'},
            'us-gov-west-1': {'name': 'AWS GovCloud (US)'},
        }

        match_region_info = REGION_INFO.get(getattr(result.data.compute, 'region_name', None))

        if match_region_info is not None:
            region_info = match_region_info.copy()
            region_info.update({
                'region_code': result.data.compute.region_name
            })

            return Region(region_info, strict=False)

        return None
