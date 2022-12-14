__all__ = ["AzureVMConnector"]

import logging
from spaceone.core.error import *
from spaceone.core import utils
from spaceone.core.connector import BaseConnector

import sys
import os

from azure.identity import DefaultAzureCredential
from azure.mgmt.compute import ComputeManagementClient
from azure.mgmt.network import NetworkManagementClient
from azure.mgmt.resource import ResourceManagementClient
from azure.mgmt.resource import SubscriptionClient

from azure.common.client_factory import get_client_from_json_dict

_LOGGER = logging.getLogger(__name__)
DEFAULT_REGION = ''


class AzureVMConnector(BaseConnector):

    def __init__(self, transaction=None, config=None):
        self.compute_client = None
        self.network_client = None
        self.resource_client = None
        self.subscription_client = None

    def verify(self, options, secret_data):
        self.set_connect(secret_data)
        return "ACTIVE"

    def set_connect(self, secret_data):
        subscription_id = secret_data['subscription_id']

        os.environ["AZURE_SUBSCRIPTION_ID"] = subscription_id
        os.environ["AZURE_TENANT_ID"] = secret_data['tenant_id']
        os.environ["AZURE_CLIENT_ID"] = secret_data['client_id']
        os.environ["AZURE_CLIENT_SECRET"] = secret_data['client_secret']

        credential = DefaultAzureCredential()

        self.compute_client = ComputeManagementClient(credential=credential, subscription_id=subscription_id)
        self.network_client = NetworkManagementClient(credential=credential, subscription_id=subscription_id)
        self.resource_client = ResourceManagementClient(credential=credential, subscription_id=subscription_id)
        self.subscription_client: SubscriptionClient = SubscriptionClient(credential=credential)

    def list_resource_groups(self):
        return self.resource_client.resource_groups.list()

    def list_tenants(self):
        return self.subscription_client.tenants.list()

    def list_vms(self, resource_group_name, **query):
        return list(self.compute_client.virtual_machines.list(resource_group_name=resource_group_name, **query))

    def list_all_vms(self, **query):
        return list(self.compute_client.virtual_machines.list_all(**query))

    def get_vm(self, resource_group_name, vm_name):
        return self.compute_client.virtual_machines.get(resource_group_name, vm_name, expand='instanceView')

    # def list_instance_types(self, **query):
    #     pass

    def list_vms_in_rg(self, resource_group_name):
        return self.compute_client.virtual_machines.list(resource_group_name=resource_group_name)

    def list_virtual_machine_sizes(self, location):
        return self.compute_client.virtual_machine_sizes.list(location=location)

    def list_resources(self, resource_group_name):
        return self.resource_client.resources.list_by_resource_group(resource_group_name=resource_group_name)

    def list_network_interfaces(self, resource_group_name):
        return self.network_client.network_interfaces.list(resource_group_name)

    def list_disk(self):
        return self.compute_client.disks.list()

    def list_virtual_network(self, resource_group_name):
        return self.network_client.virtual_networks.list(resource_group_name)

    def list_public_ip_address(self, resource_group_name):
        return self.network_client.public_ip_addresses.list(resource_group_name)

    def list_load_balancers(self, resource_group_name):
        return self.network_client.load_balancers.list(resource_group_name)

    def list_load_balancer_network_interfaces(self, resource_group_name, lb_name):
        return self.network_client.load_balancer_network_interfaces.list(resource_group_name, lb_name)

    def list_network_security_groups(self, resource_group_name):
        return self.network_client.network_security_groups.list(resource_group_name)

    def get_subscription_info(self, subscription_id):
        return self.subscription_client.subscriptions.get(subscription_id)

    def list_virtual_machine_scale_sets(self, resource_group_name):
        return self.compute_client.virtual_machine_scale_sets.list(resource_group_name)

    def list_scale_set_vms(self, resource_group_name, scale_set_name):
        return self.compute_client.virtual_machine_scale_set_vms.list(resource_group_name, scale_set_name)
