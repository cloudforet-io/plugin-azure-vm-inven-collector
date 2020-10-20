from spaceone.core.manager import BaseManager
from spaceone.inventory.model.security_group import SecurityGroup
from spaceone.inventory.connector.azure_vm_connector import AzureVMConnector

import pprint


class AzureNetworkSecurityGroupManager(BaseManager):

    def __init__(self, params, azure_vm_connector=None, **kwargs):
        super().__init__(**kwargs)
        self.params = params
        self.azure_vm_connector: AzureVMConnector = azure_vm_connector

    def get_network_security_group_info(self, vm, network_security_groups, resource_group_name):
        '''
        nsg_data = {
            "protocol" = "",
            "remote" = "",
            "remote_cidr" = "",
            "remote_id" = "",
            "security_group_name" = "",
            "security_group_id" = "",
            "description" = "",
            "direction" = "inbound" | "outbound",
            "port_range_min" = 0,
            "port_range_max" = 0,
            "port" = "",
            "priority" = 0
        }
        '''

        nsg_data = []

        network_security_groups_data = []
        network_interfaces = vm.network_profile.network_interfaces
        match_network_security_groups = self.get_network_security_group_from_nic(network_interfaces, resource_group_name, network_security_groups)

        for network_security_group in match_network_security_groups:

            security_rules = network_security_group.security_rules
            sg_id = network_security_group.id
            security_data = self.get_nsg_security_rules(security_rules, sg_id)
            network_security_groups_data.extend(security_data)

            default_security_rules = network_security_group.default_security_rules
            default_security_data = self.get_nsg_default_security_rules(default_security_rules, sg_id)
            network_security_groups_data.extend(default_security_data)

        for nsg in network_security_groups_data:
            nsg_data.append(SecurityGroup(nsg, strict=False))

        # pprint.pprint(nsg_data)

        return nsg_data

    def get_network_security_group_from_nic(self, network_interfaces, resource_group_name, network_security_groups):
        nsgs = []
        for nic in network_interfaces:
            nic_name = nic.id.split('/')[-1]
            nics = self.azure_vm_connector.list_network_interfaces(resource_group_name)
            for nic in nics:
                if nic_name == nic.name:
                    nsg_name = nic.network_security_group.id.split('/')[-1]
                    for nsg in network_security_groups:
                        if nsg.name == nsg_name:
                            nsgs.append(nsg)

        return nsgs

    def get_nsg_security_rules(self, security_rules, sg_id):
        result = []
        for s_rule in security_rules:
            # print(s_rule)
            security_rule_data = {
                'protocol': s_rule.protocol,
                'remote_id': s_rule.id,
                'security_group_name': s_rule.name,
                'description': s_rule.description,
                'direction': s_rule.direction.lower(),
                'priority': s_rule.priority,
                'security_group_id': sg_id
            }

            remote_data = self.get_nsg_remote(s_rule)
            security_rule_data.update(remote_data)

            port_data = self.get_nsg_port(s_rule)
            security_rule_data.update(port_data)

            result.append(security_rule_data)

        return result

    def get_nsg_default_security_rules(self, default_security_rules, sg_id):
        result = []
        for s_rule in default_security_rules:
            # print(s_rule)
            default_security_rule_data = {
                'protocol': s_rule.protocol,
                'remote_id': s_rule.id,
                'security_group_name': s_rule.name,
                'description': s_rule.description,
                'direction': s_rule.direction.lower(),
                'priority': s_rule.priority,
                'security_group_id': sg_id
            }

            remote_data = self.get_nsg_remote(s_rule)
            default_security_rule_data.update(remote_data)

            port_data = self.get_nsg_port(s_rule)
            default_security_rule_data.update(port_data)

            result.append(default_security_rule_data)

        return result

    @staticmethod
    def get_nsg_remote(s_rule):
        remote_result = {}
        if s_rule.source_address_prefix is not None:
            if '/' in s_rule.source_address_prefix:
                remote_result.update({
                    'remote': s_rule.source_address_prefix,
                    'remote_cidr': s_rule.source_address_prefix
                })
            elif s_rule.source_address_prefix == '*':
                remote_result.update({
                    'remote': '*',
                    'remote_cidr': '*'
                })
            else:
                remote_result.update({
                    'remote': s_rule.source_address_prefix
                })

        else:
            address_prefixes = s_rule.source_address_prefixes
            remote = ''
            for prfx in address_prefixes:
                remote += prfx
                remote += ', '

            remote = remote[:-2]

            remote_result.update({
                'remote': remote,
                'remote_cidr': remote
            })

        return remote_result

    @staticmethod
    def get_nsg_port(s_rule):
        port_result = {}
        if s_rule.destination_port_range is not None:
            # print(s_rule.destination_port_range)
            if '-' in s_rule.destination_port_range:
                port_min = s_rule.destination_port_range.split('-')[0]
                port_max = s_rule.destination_port_range.split('-')[1]
                port_result.update({
                    'port_range_min': port_min,
                    'port_range_max': port_max,
                    'port': s_rule.destination_port_range
                })
            elif s_rule.destination_port_range == '*':
                port_result.update({
                    'port_range_min': 0,
                    'port_range_max': 0,
                    'port': '*'
                })
            else:
                port_result.update({
                    'port_range_min': s_rule.destination_port_range,
                    'port_range_max': s_rule.destination_port_range,
                    'port': s_rule.destination_port_range
                })
        else:
            port_ranges = s_rule.destination_port_ranges
            port_min = int(port_ranges[0])
            port_max = int(port_ranges[0])
            all_port = ''
            for port in port_ranges:
                if int(port.split('-')[0]) < port_min:
                    port_min = int(port.split('-')[0])
                if int(port.split('-')[-1]) > port_max:
                    port_max = int(port.split('-')[1])

                all_port += port
                all_port += ', '

            all_port = all_port[:-2]

            port_result.update({
                'port_range_min': port_min,
                'port_range_max': port_max,
                'port': all_port
            })

        return port_result
