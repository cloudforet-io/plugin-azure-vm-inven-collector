import unittest
import time
import os
from datetime import datetime, timedelta
from unittest.mock import patch
from spaceone.core.unittest.result import print_data
from spaceone.core.unittest.runner import RichTestRunner
from spaceone.core import config
from spaceone.core.transaction import Transaction
from spaceone.core import utils
from spaceone.inventory.error import *
from spaceone.inventory.connector.azure_vm_connector import AzureVMConnector
from spaceone.inventory.manager.collector_manager import CollectorManager
from spaceone.inventory.service.collector_service import CollectorService


class TestMetricManager(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        config.init_conf(package='spaceone.inventory')

        config_path = os.environ.get('TEST_CONFIG')
        test_config = utils.load_yaml_from_file(config_path)

        cls.schema = 'azure_client_secret'
        cls.azure_credentials = test_config.get('AZURE_CREDENTIALS', {})

        cls.azure_vm_connector = AzureVMConnector(Transaction(), {})
        cls.collector_manager = CollectorManager(Transaction())
        cls.collector_service = CollectorService({})

        super().setUpClass()

    @classmethod
    def tearDownClass(cls) -> None:
        super().tearDownClass()

    @patch.object(CollectorService, '__init__', return_value=None)
    def test_collector_manager(self, *args):
        self.collector_service.init({'options': {}})
        secret_data = self.azure_credentials
        # self.collector_service.verify({'options': {}, 'secret_data': secret_data})

        params = {'options': {}, 'secret_data': secret_data, 'filter': {}}

        resource_groups = self.collector_manager.list_all_resource_groups(params)
        print(f'resource_groups: {resource_groups}')
        mt_params = []
        for rg in resource_groups:
            vms = self.collector_manager.list_vms(params, rg.name)

            if list(vms):
                mt_params.append({
                    'secret_data': params['secret_data'],
                    'resource_group': rg,
                    'vms': vms
                })

        for mt_param in mt_params:
            # print(mt_param)  # specific resource_group
            self.collector_manager.list_all_resources(mt_param)

        # self.collector_manager.list_resources(params)
        # self.collector_service.list_resources(params)


if __name__ == "__main__":
    unittest.main(testRunner=RichTestRunner)