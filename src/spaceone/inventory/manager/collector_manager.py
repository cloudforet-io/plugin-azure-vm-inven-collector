__all__ = ['CollectorManager']

import logging
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
from spaceone.inventory.model.resource import ErrorResourceResponse, ServerResourceResponse
from spaceone.inventory.model.metadata.metadata import CloudServiceTypeMetadata
from spaceone.inventory.model.metadata.metadata_dynamic_field import TextDyField
from spaceone.inventory.conf.cloud_service_conf import *
from spaceone.core.utils import *

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

    def list_all_vms(self, params):
        azure_vm_connector: AzureVMConnector = self.locator.get_connector('AzureVMConnector')
        azure_vm_connector.set_connect(params['secret_data'])

        vm_manager: AzureVmManager = AzureVmManager(params, azure_vm_connector=azure_vm_connector)
        return vm_manager.list_all_vms()

    def list_all_resources(self, params):
        servers = []
        errors = []

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
        subscription_data = {
            'subscription_id': subscription_info.subscription_id,
            'subscription_name': subscription_info.display_name,
            'tenant_id': subscription_info.tenant_id
        }

        vm_sizes = []

        for vm in vms:
            try:
                vnet_data = None
                subnet_data = None
                lb_vos = []
                disk_vos = disk_manager.get_disk_info(vm, list_disks)
                nic_vos, primary_ip = nic_manager.get_nic_info(vm, network_interfaces, public_ip_addresses,
                                                               virtual_networks)

                server_data = vm_manager.get_vm_info(vm, disk_vos, nic_vos, resource_group, subscription,
                                                     network_security_groups, vm_sizes, primary_ip)

                if load_balancers is not None:
                    lb_vos = load_balancer_manager.get_load_balancer_info(vm, load_balancers, public_ip_addresses)

                nsg_vos = network_security_group_manager.get_network_security_group_info(vm, network_security_groups,
                                                                                         network_interfaces)

                nic_name = vm.network_profile.network_interfaces[0].id.split('/')[-1]

                if nic_name is not None:
                    vnet_subnet_dict = vnet_manager.get_vnet_subnet_info(nic_name, network_interfaces, virtual_networks)

                    if vnet_subnet_dict.get('vnet_info'):
                        vnet_data = vnet_subnet_dict['vnet_info']

                    if vnet_subnet_dict.get('subnet_info'):
                        subnet_data = vnet_subnet_dict['subnet_info']

                server_data.update({
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
                    '_metadata': meta_manager.get_server_metadata(),
                    'reference': ReferenceModel({
                        'resource_id': server_data['data']['compute']['instance_id'],
                        'external_link': f"https://portal.azure.com/#@.onmicrosoft.com/resource/subscriptions/{subscription}/resourceGroups/{resource_group_name}/providers/Microsoft.Compute/virtualMachines/{server_data['data']['compute']['instance_name']}/overview"
                    }),
                    'account': subscription_data['subscription_id'],
                    'instance_type': server_data['data']['compute']['instance_type'],
                    'launched_at': datetime_to_iso8601(server_data['data']['compute']['launched_at'])
                })
                server_resource = Server(server_data, strict=False)
                servers.append(ServerResourceResponse({'resource': server_resource}))
            except Exception as e:
                _LOGGER.error(f'[list_instances] [{vm.id}] {e}')

                if type(e) is dict:
                    error_resource_response = ErrorResourceResponse({'message': json.dumps(e)})
                else:
                    error_resource_response = ErrorResourceResponse({'message': str(e), 'resource': {'resource_id': vm.id}})

                errors.append(error_resource_response)

        return servers, errors

    def list_resources(self, params):
        """ Get list of resources
        Args:
            params:
                - resource_group
                - vms

        Returns: list of resources
        """
        start_time = time.time()
        total_resources = []

        try:
            resources, error_resources = self.list_all_resources(params)
            total_resources.extend(resources)
            total_resources.extend(error_resources)
            _LOGGER.debug(f'[{params["resource_group"].name}] Finished {time.time() - start_time} Seconds')

            return total_resources

        except Exception as e:
            _LOGGER.debug(f'[list_resources]: {params["resource_group"].name}] : {e}')

            if type(e) is dict:
                error_resource_response = ErrorResourceResponse({'message': json.dumps(e)})
            else:
                error_resource_response = ErrorResourceResponse({'message': str(e)})

            total_resources.append(error_resource_response)
            return total_resources

    @staticmethod
    def list_cloud_service_types():
        meta_manager: MetadataManager = MetadataManager()

        cloud_service_type = {
            '_metadata': meta_manager.get_cloud_service_type_metadata(),
            'tags': {
                'spaceone:icon': 'https://spaceone-custom-assets.s3.ap-northeast-2.amazonaws.com/console-assets/icons/azure-vm.svg',
            }
        }
        return [CloudServiceType(cloud_service_type, strict=False)]

    @staticmethod
    def get_region_from_result(result):
        match_region_info = REGION_INFO.get(getattr(result.data.compute, 'az', None))

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
