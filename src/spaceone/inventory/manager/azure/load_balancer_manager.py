from spaceone.core.manager import BaseManager
from spaceone.inventory.model.load_balancer import LoadBalancer
from spaceone.inventory.connector.azure_vm_connector import AzureVMConnector

import pprint


class AzureLoadBalancerManager(BaseManager):

    def __init__(self, params, azure_vm_connector=None, **kwargs):
        super().__init__(**kwargs)
        self.params = params
        self.azure_vm_connector: AzureVMConnector = azure_vm_connector

    def get_load_balancer_info(self, vm, load_balancers, resource_group_name):
        """
        lb_data = {
            "type" = "application" | "network",
            "endpoint" = "",
            "port" = []
            "name" = ""
            "protocol" = []
            "scheme" = "internet-facing" | "internal"
            "tags" = {
                "lb_id" = ""
            }
        }
        """

        lb_data = []

        match_load_balancers = self.get_load_balancers_from_nic(vm, resource_group_name, load_balancers)

        for match_load_balancer in match_load_balancers:
            load_balancer_data = {
                'type': 'network',
                'scheme': self.get_lb_scheme(match_load_balancer),
                'endpoint': self.get_lb_endpoint(match_load_balancer, resource_group_name),
                'port': self.get_lb_port(match_load_balancer),
                'name': match_load_balancer.name,
                'protocol': self.get_lb_protocol(match_load_balancer),
                'tags': {
                    'lb_id': match_load_balancer.id
                }

            }
            # pprint.pprint(load_balancer_data)
            lb_data.append(LoadBalancer(load_balancer_data, strict=False))

        return lb_data

    def get_load_balancers_from_nic(self, vm, resource_group_name, load_balancers):
        match_load_balancers = []

        for lb in load_balancers:
            lb_name = lb.name
            # TODO: 탐색 구조 수정 (중복 call 제거)
            lb_nics = self.azure_vm_connector.list_load_balancer_network_interfaces(resource_group_name, lb_name)
            for lb_nic in lb_nics:
                if lb_nic.virtual_machine.id.split('/')[-1] == vm.name:
                    match_load_balancers.append(lb)

        return match_load_balancers

    def get_lb_endpoint(self, match_load_balancer, resource_group_name):
        frontend_ip_configurations = match_load_balancer.frontend_ip_configurations
        if self.get_lb_scheme(match_load_balancer) == 'internet-facing':
            for ip in frontend_ip_configurations:
                public_ip_address_name = ip.public_ip_address.id.split('/')[-1]
                public_ip_address = self.azure_vm_connector.get_public_ip_address(resource_group_name, public_ip_address_name)
                return public_ip_address.ip_address

        elif self.get_lb_scheme(match_load_balancer) == 'internal':
            for ip in frontend_ip_configurations:
                return ip.private_ip_address

    @staticmethod
    def get_lb_scheme(match_load_balancer):
        frontend_ip_configurations = match_load_balancer.frontend_ip_configurations
        for fe_ip_conf in frontend_ip_configurations:
            if fe_ip_conf.public_ip_address:
                return 'internet-facing'
            else:
                return 'internal'

    @staticmethod
    def get_lb_port(match_load_balancer):
        ports = []
        lb_rules = match_load_balancer.load_balancing_rules
        if lb_rules:
            for lbr in lb_rules:
                ports.append(lbr.frontend_port)

        return ports

    @staticmethod
    def get_lb_protocol(match_load_balancer):
        protocols = []
        lb_rules = match_load_balancer.load_balancing_rules
        if lb_rules:
            for lbr in lb_rules:
                protocols.append(lbr.protocol)

        return protocols
