__all__ = ['CollectorManager']

import time
import logging
import pprint
from spaceone.core.manager import BaseManager
from spaceone.inventory.connector import AzureVMConnector
from spaceone.inventory.manager.azure import AzureDiskManager, AzureLoadBalancerManager, \
    AzureNetworkSecurityGroupManager, AzureNICManager, AzureResourceGroupManager, AzureVmManager, \
    AzureVMScaleSetManager, AzureVNetManager
from spaceone.inventory.manager.metadata.metadata_manager import MetadataManager
from spaceone.inventory.model.server import Server, ReferenceModel
from spaceone.inventory.model.region import Region
from spaceone.inventory.model.subscription import Subscription
from spaceone.inventory.model.cloud_service_type import CloudServiceType
from spaceone.inventory.model.monitor import Monitor


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
        vms = vm_manager.list_vms(resource_group_name)
        region_name = params['secret_data'].get('region_name')

        if region_name:
            return [vm for vm in vms if vm.location == region_name]

        return vms

    def list_all_resources(self, params):
        server_vos = []
        azure_vm_connector: AzureVMConnector = self.locator.get_connector('AzureVMConnector')
        azure_vm_connector.set_connect(params['secret_data'])

        resource_group = params['resource_group']
        resource_group_name = params['resource_group'].name
        subscription = params['secret_data'].get('subscription_id')

        # call all managers
        vm_manager: AzureVmManager = AzureVmManager(params, azure_vm_connector=azure_vm_connector)
        disk_manager: AzureDiskManager = AzureDiskManager(params, azure_vm_connector=azure_vm_connector)

        load_balancer_manager: AzureLoadBalancerManager = \
            AzureLoadBalancerManager(params, azure_vm_connector=azure_vm_connector)

        network_security_group_manager: AzureNetworkSecurityGroupManager = \
            AzureNetworkSecurityGroupManager(params, azure_vm_connector=azure_vm_connector)

        nic_manager: AzureNICManager = AzureNICManager(params, azure_vm_connector=azure_vm_connector)
        resource_group_manager: AzureResourceGroupManager(params, azure_vm_connector=azure_vm_connector)
        # vmss_manager: AzureVMScaleSetManager = AzureVMScaleSetManager(params, azure_vm_connector=azure_vm_connector)
        vnet_manager: AzureVNetManager = AzureVNetManager(params, azure_vm_connector=azure_vm_connector)

        meta_manager: MetadataManager = MetadataManager()

        vms = params['vms']

        load_balancers = list(azure_vm_connector.list_load_balancers(resource_group_name))
        network_security_groups = list(azure_vm_connector.list_network_security_groups(resource_group_name))
        network_interfaces = list(azure_vm_connector.list_network_interfaces(resource_group_name))
        list_disks = list(azure_vm_connector.list_disk())
        public_ip_addresses = list(azure_vm_connector.list_public_ip_address(resource_group_name))
        virtual_networks = list(azure_vm_connector.list_virtual_network(resource_group_name))
        # vmss = list(azure_vm_connector.list_virtual_machine_scale_sets(resource_group_name))

        # if vmss:
        #     for scale_set in vmss:
        #         print(scale_set.name)
        #         scale_set_vms = list(azure_vm_connector.list_scale_set_vms(resource_group_name, scale_set.name))
        #         pprint.pprint(scale_set_vms)
        #         for ss in scale_set_vms:
        #             vms.append(ss)
        #         vms.append(scale_set_vms)

        subscription_info = azure_vm_connector.get_subscription_info(subscription)

        # tenants_info = azure_vm_connector.list_tenants()

        subscription_data = {
            'subscription_id': subscription_info.subscription_id,
            'subscription_name': subscription_info.display_name,
            'tenant_id': subscription_info.tenant_id
        }

        vm_sizes = []

        for vm in vms:
            disk_vos = disk_manager.get_disk_info(vm, list_disks)

            nic_vos, primary_ip = nic_manager.get_nic_info(vm, network_interfaces, public_ip_addresses,
                                                           virtual_networks)

            server_data = vm_manager.get_vm_info(vm, resource_group, subscription, network_security_groups,
                                                 vm_sizes, primary_ip)

            if load_balancers is not None:
                lb_vos = load_balancer_manager.get_load_balancer_info(vm, load_balancers, public_ip_addresses)

            nsg_vos = network_security_group_manager.get_network_security_group_info(vm, network_security_groups,
                                                                                     network_interfaces)

            nic_name = vm.network_profile.network_interfaces[0].id.split('/')[-1]

            if nic_name is not None:
                # vnet_data, subnet_data = vnet_manager.get_vnet_info(nic_name, network_interfaces, virtual_networks)
                vnet_subnet_dict = vnet_manager.get_vnet_subnet_info(nic_name, network_interfaces, virtual_networks)

                if vnet_subnet_dict.get('vnet_info'):
                    vnet_data = vnet_subnet_dict['vnet_info']
                else:
                    vnet_data = None

                if vnet_subnet_dict.get('subnet_info'):
                    subnet_data = vnet_subnet_dict['subnet_info']
                else:
                    subnet_data = None

            server_data.update({
                'disks': disk_vos,
                'nics': nic_vos,
                'tags': self.get_tags(vm.tags)
            })

            server_data['data'].update({
                'load_balancer': lb_vos,
                'security_group': nsg_vos,
                'vnet': vnet_data,
                'subnet': subnet_data,
                'subscription': Subscription(subscription_data, strict=False),
                'azure_monitor': Monitor({
                    'resource_id': f'subscriptions/{subscription}/resourceGroups/{resource_group_name}/providers/Microsoft.Compute/virtualMachines/{server_data["name"]}'
                }, strict=False)
            })

            server_data['data']['compute']['account'] = subscription_data['subscription_name']

            server_data.update({
                '_metadata': meta_manager.get_metadata(),
                'reference': ReferenceModel({
                    'resource_id': server_data['data']['compute']['instance_id'],
                    'external_link': f"https://portal.azure.com/#@.onmicrosoft.com/resource/subscriptions/{subscription}/resourceGroups/{resource_group_name}/providers/Microsoft.Compute/virtualMachines/{server_data['data']['compute']['instance_name']}/overview"
                })
            })

            server_vos.append(Server(server_data, strict=False))

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
            print(f'   [{params["resource_group"].name}] Finished {time.time() - start_time} Seconds')
            return resources

        except Exception as e:
            print(f'[ERROR: {params["resource_group"].name}] : {e}')
            raise e

    @staticmethod
    def list_cloud_service_types():
        cloud_service_type = {
            'tags': {
                'spaceone:icon': 'https://spaceone-custom-assets.s3.ap-northeast-2.amazonaws.com/console-assets/icons/azure-vm.svg',
            },
            'is_major': True,
            'is_primary': True,
            'service_code': 'Microsoft.Compute/virtualMachines'

        }
        return [CloudServiceType(cloud_service_type, strict=False)]

    @staticmethod
    def get_region_from_result(result):
        REGION_INFO = {
            'eastus': {'name': 'US East (Virginia)', 'tags': {'latitude': '37.3719', 'longitude': '-79.8164'}},
            'eastus2': {'name': 'US East 2 (Virginia)', 'tags': {'latitude': '36.6681', 'longitude': '-78.3889'}},
            'westus': {'name': 'US West (California)', 'tags': {'latitude': '37.783', 'longitude': '-122.417'}},
            'westus2': {'name': 'US West 2 (Washington)', 'tags': {'latitude': '47.233', 'longitude': '-119.852'}},
            'centralus': {'name': 'US Central (Iowa)', 'tags': {'latitude': '41.5908', 'longitude': '-93.6208'}},
            'southcentralus': {'name': 'US South Central (Texas)',
                               'tags': {'latitude': '29.4167', 'longitude': '-98.5'}},
            'northcentralus': {'name': 'US North Central (Illinois)',
                               'tags': {'latitude': '41.8819', 'longitude': '-87.6278'}},
            'westcentralus': {'name': 'US West Central (Wyoming)',
                              'tags': {'latitude': '40.890', 'longitude': '-110.234'}},
            'canadacentral': {'name': 'Canada Central (Toronto)',
                              'tags': {'latitude': '43.653', 'longitude': '-79.383'}},
            'canadaeast': {'name': 'Canada East (Quebec)',
                           'tags': {'latitude': '46.817', 'longitude': '-71.217'}},
            'southafricanorth': {'name': 'South Africa North (Johannesburg)',
                                 'tags': {'latitude': '-25.731340', 'longitude': '28.218370'}},
            'southafricawest': {'name': 'South Africa West (Cape Town)',
                                'tags': {'latitude': '-34.075691', 'longitude': '18.843266'}},
            'eastasia': {'name': 'Asia Pacific East (Hong Kong)',
                         'tags': {'latitude': '22.267', 'longitude': '114.188'}},
            'centralindia': {'name': 'Asia Pacific Central India (Pune)',
                             'tags': {'latitude': '18.5822', 'longitude': '73.9197'}},
            'southindia': {'name': 'Asia Pacific South India (Chennai)',
                           'tags': {'latitude': '12.9822', 'longitude': '80.1636'}},
            'westindia': {'name': 'Asia Pacific West India (Mumbai)',
                          'tags': {'latitude': '19.088', 'longitude': '72.868'}},
            'southeastasia': {'name': 'Asia Pacific South East (Singapore)',
                              'tags': {'latitude': '1.283', 'longitude': '103.833'}},
            'japaneast': {'name': 'Asia Pacific Japan East (Tokyo, Saitama)',
                          'tags': {'latitude': '35.68', 'longitude': '139.77'}},
            'japanwest': {'name': 'Asia Pacific Japan West (Osaka)',
                          'tags': {'latitude': '34.6939', 'longitude': '135.5022'}},
            'koreacentral': {'name': 'Asia Pacific Korea Central (Seoul)',
                             'tags': {'latitude': '37.5665', 'longitude': '126.9780'}},
            'koreasouth': {'name': 'Asia Pacific Korea South (Busan)',
                           'tags': {'latitude': '35.1796', 'longitude': '129.0756'}},
            'australiaeast': {'name': 'Asia Pacific Australia East (New South Wales)',
                              'tags': {'latitude': '-33.86', 'longitude': '151.2094'}},
            'australiacentral': {'name': 'Asia Pacific Australia Central (Canberra)',
                                 'tags': {'latitude': '-35.3075', 'longitude': '149.1244'}},
            'australiacentral2': {'name': 'Asia Pacific Australia Central 2 (Canberra)',
                                  'tags': {'latitude': '-35.3075', 'longitude': '149.1244'}},
            'australiasoutheast': {'name': 'Asia Pacific Australia South East (Victoria)',
                                   'tags': {'latitude': '-37.8136', 'longitude': '144.9631'}},
            'northeurope': {'name': 'North Europe (Ireland)', 'tags': {'latitude': '53.3478', 'longitude': '-6.2597'}},
            'norwayeast': {'name': 'North Europe (Norway East)',
                           'tags': {'latitude': '59.913868', 'longitude': '10.752245'}},
            'norwaywest': {'name': 'North Europe (Norway West)',
                           'tags': {'latitude': '58.969975', 'longitude': '5.733107'}},
            'germanywestcentral': {'name': 'Europe Germany West Central (Frankfurt)',
                                   'tags': {'latitude': '50.110924', 'longitude': '8.682127'}},
            'germanynorth': {'name': 'Europe Germany North (Berlin)',
                             'tags': {'latitude': '53.073635', 'longitude': '8.806422'}},
            'switzerlandnorth': {'name': 'Europe Switzerland North (Zurich)',
                                 'tags': {'latitude': '47.451542', 'longitude': '8.564572'}},
            'switzerlandwest': {'name': 'Europe Switzerland West (Geneva)',
                                'tags': {'latitude': '46.204391', 'longitude': '6.143158'}},
            'francecentral': {'name': 'Europe France Central (Paris)',
                              'tags': {'latitude': '46.3772', 'longitude': '2.3730'}},
            'francesouth': {'name': 'Europe France South (Marseille)',
                            'tags': {'latitude': '43.8345', 'longitude': '2.1972'}},
            'westeurope': {'name': 'West Europe (Netherlands)', 'tags': {'latitude': '52.3667', 'longitude': '4.9'}},
            'uksouth': {'name': 'UK South (London)', 'tags': {'latitude': '50.941', 'longitude': '-0.799'}},
            'ukwest': {'name': 'UK West (Cardiff)', 'tags': {'latitude': '53.427', 'longitude': '-3.084'}},
            'uaenorth': {'name': 'Middle East UAE North (Dubai)',
                         'tags': {'latitude': '25.266666', 'longitude': '55.316666'}},
            'uaecentral': {'name': 'Middle East UAE Central (Abu Dhabi)',
                           'tags': {'latitude': '24.466667', 'longitude': '54.366669'}},
            'brazilsouth': {'name': 'South America Brazil South (Sao Paulo State)',
                            'tags': {'latitude': '-23.55', 'longitude': '-46.633'}},
            'brazilsoutheast': {'name': 'South America Brazil South East (Rio)',
                                'tags': {'latitude': '-22.90278', 'longitude': '-43.2075'}},
        }

        match_region_info = REGION_INFO.get(getattr(result, 'region_code', None))

        if match_region_info:
            region_info = match_region_info.copy()
            region_info.update({
                'region_code': result.region_code
            })

            return Region(region_info, strict=False)

        return None

    @staticmethod
    def get_tags(tags):
        tags_result = []
        if tags:
            for k, v in tags.items():
                tags_result.append({
                    'key': k,
                    'value': v
                })

        return tags_result
