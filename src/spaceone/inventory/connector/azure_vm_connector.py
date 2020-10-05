__all__ = ["AzureVMConnector"]

import logging
from spaceone.core.error import *
from spaceone.core import utils
from spaceone.core.connector import BaseConnector

import os

from azure.identity import DefaultAzureCredential
from azure.mgmt.compute import ComputeManagementClient
from azure.mgmt.network import NetworkManagementClient
from azure.mgmt.resource import ResourceManagementClient
from azure.mgmt.resource import SubscriptionClient
from azure.mgmt.monitor import MonitorClient

_LOGGER = logging.getLogger(__name__)
DEFAULT_REGION = ''


class AzureVMConnector(BaseConnector):

    def __init__(self, transaction=None, config=None):
        self.compute_client = None
        self.network_client = None
        self.resource_client = None
        self.subscription_client = None
        self.monitor_client = None
        pass

    def verify(self, options, secret_data):
        pass

    def set_connect(self, secret_data):
        params = {
            'azure_client_secret': secret_data['AZURE_CLIENT_SECRET'],
            'azure_client_id': secret_data['AZURE_CLIENT_ID'],
            'azure_tenant_id': secret_data['AZURE_TENANT_ID'],
            'subscription_id': secret_data['SUBSCRIPTION_ID']
        }

    def list_instances(self, **query):
        status_filter = {'key': 'status', 'values': ['STARTING', 'RUNNING', 'STOPPING', 'STOPPED', 'DEALLOCATING', 'DEALLOCATED']}

        if 'filter' in query:
            query.get('filter').append(status_filter)
        else:
            query.update({'filter': [status_filter]})

        query = self.generate_key_query('filter', self._get_filter_to_params(**query), '', is_default=True, **query)

        result = self.subscription_client.subscriptions.list(**query).execute()

    def _get_filter_to_params(self, **query):
        filtering_list = []
        filters = query.get('filter', None)
        if filters and isinstance(filters, list):
            for single_filter in filters:
                filter_key = single_filter.get('key', '')
                filter_values = single_filter.get('values', [])
                filter_str = self._get_full_filter_string(filter_key, filter_values)
                if filter_str != '':
                    filtering_list.append(filter_str)

            return ' AND '.join(filtering_list)

    def generate_query(self, **query):
        query.update({
            'project': self.project_id,
        })
        return query

    def generate_key_query(self, key, value, delete, is_default=False, **query):
        if is_default:
            if delete != '':
                query.pop(delete, None)

            query.update({
                key: value,
                'project': self.project_id
            })

        return query

    @staticmethod
    def _generate_query():
        credential = DefaultAzureCredential(),
        subscription_id = subscription_id