from spaceone.core.manager import BaseManager
from spaceone.inventory.model.nic import NIC, NICTags
from spaceone.inventory.connector.azure_vm_connector import AzureVMConnector

import pprint


class AzureNICManager(BaseManager):

    def __init__(self, params, azure_vm_connector=None, **kwargs):
        super().__init__(**kwargs)
        self.params = params
        self.azure_vm_connector: AzureVMConnector = azure_vm_connector

    def get_nic_info(self, vm, resource_group_name):
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

        nic_data = []
        index = 0

        network_interfaces = vm.network_profile.network_interfaces
        nic_list = list(self.azure_vm_connector.list_network_interfaces(resource_group_name))

        for network_interface in network_interfaces:
            network_data = {
                'device_index': index,
                'cidr': self.get_nic_cidr(nic_list, network_interface, resource_group_name),
                'ip_addresses': self.get_nic_ip_addresses(nic_list, network_interface),
                'mac_address': self.get_nic_mac_address(nic_list, network_interface),
                'public_ip_address': self.get_nic_public_ip_addresses(nic_list, network_interface, resource_group_name),
                'tags': self.get_tags(nic_list, network_interface)
            }

            # pprint.pprint(network_data)
            index += 1
            nic_data.append(NIC(network_data, strict=False))

        return nic_data

    def get_nic_public_ip_addresses(self, nic_list, network_interface, resource_group_name):
        conf = self.get_ip_configurations(nic_list, network_interface)
        public_ip_name = conf[0].public_ip_address.id.split('/')[-1]
        public_ip_address = self.azure_vm_connector.get_public_ip_address(resource_group_name, public_ip_name)
        return public_ip_address.ip_address

    def get_nic_cidr(self, nic_list, network_interface, resource_group_name):
        conf = self.get_ip_configurations(nic_list, network_interface)
        subnet_name = conf[0].subnet.id.split('/')[-3]
        subnet = self.azure_vm_connector.get_virtual_network(resource_group_name, subnet_name)
        if subnet.subnets:
            return subnet.subnets[0].address_prefix

    def get_nic_mac_address(self, nic_list, network_interface):
        nic = self.match_nic(nic_list, network_interface)
        return nic.mac_address

    def get_nic_ip_addresses(self, nic_list, network_interface):
        ip_addresses = []
        confs = self.get_ip_configurations(nic_list, network_interface)
        for conf in confs:
            ip_addresses.append(conf.private_ip_address)

        return ip_addresses

    def get_ip_configurations(self, nic_list, network_interface):
        nic = self.match_nic(nic_list, network_interface)
        if nic.ip_configurations is not None:
            return nic.ip_configurations

    def get_tags(self, nic_list, network_interface):
        tag_info = {}
        nic = self.match_nic(nic_list, network_interface)
        # print(nic.name)
        # print(nic.etag)
        # print(nic.enable_accelerated_networking)
        # print(nic.enable_ip_forwarding)
        tag_info.update({'name': self.get_nic_id(network_interface)})
        tag_info.update({'etag': nic.etag})
        tag_info.update({'enable_accelerated_networking': nic.enable_accelerated_networking})
        tag_info.update({'enable_ip_forwarding': nic.enable_ip_forwarding})

        return tag_info


    def match_nic(self, nic_list, network_interface):
        for nic in nic_list:
            if nic.name == self.get_nic_id(network_interface):
                return nic

    @staticmethod
    def get_nic_id(network_interface):
        return network_interface.id.split('/')[-1]