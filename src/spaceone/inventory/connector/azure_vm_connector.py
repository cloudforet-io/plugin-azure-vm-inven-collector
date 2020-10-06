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
        # TODO
        pass

    def set_connect(self, secret_data):
        subscription_id = secret_data['subscription_id']

        os.environ["AZURE_SUBSCRIPTION_ID"] = subscription_id
        os.environ["AZURE_TENANT_ID"] = secret_data['azure_tenant_id']
        os.environ["AZURE_CLIENT_ID"] = secret_data['azure_client_id']
        os.environ["AZURE_CLIENT_SECRET"] = secret_data['azure_client_secret']

        credential = DefaultAzureCredential()

        self.compute_client = ComputeManagementClient(credential=credential, subscription_id=subscription_id)
        self.network_client = NetworkManagementClient(credential=credential, subscription_id=subscription_id)
        self.resource_client = ResourceManagementClient(credential=credential, subscription_id=subscription_id)
        self.subscription_client: SubscriptionClient = SubscriptionClient(credential=credential)

    def list_resource_groups(self, **query):
        return self.resource_client.resource_groups.list(**query)

    def list_all_vms(self, **query):
        return self.compute_client.virtual_machines.list_all(**query)

    def list_vms(self, resource_group_name, **query):
        return self.compute_client.virtual_machines.list(resource_group_name=resource_group_name, **query)

