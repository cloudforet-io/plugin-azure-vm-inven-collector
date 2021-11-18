import time
import logging
import concurrent.futures
import json

from spaceone.core.service import *
from spaceone.inventory.manager.collector_manager import CollectorManager
from spaceone.inventory.model.resource import CloudServiceTypeResourceResponse, ServerResourceResponse, RegionResourceResponse, ErrorResourceResponse

_LOGGER = logging.getLogger(__name__)

FILTER_FORMAT = [
    {
        'key': 'project_id',
        'name': 'Project ID',
        'type': 'str',
        'resource_type': 'SERVER',
        'search_key': 'identity.Project.project_id',
        'change_rules': [{
            'resource_key': 'data.compute.instance_id',
            'change_key': 'instance_id'
        }, {
            'resource_key': 'data.compute.region',
            'change_key': 'region_name'
        }]
    }, {
        'key': 'collection_info.service_accounts',
        'name': 'Service Account ID',
        'type': 'str',
        'resource_type': 'SERVER',
        'search_key': 'identity.ServiceAccount.service_account_id',
        'change_rules': [{
            'resource_key': 'data.compute.instance_id',
            'change_key': 'instance_id'
        }, {
            'resource_key': 'data.compute.region',
            'change_key': 'region_name'
        }]
    }, {
        'key': 'server_id',
        'name': 'Server ID',
        'type': 'list',
        'resource_type': 'SERVER',
        'search_key': 'inventory.Server.server_id',
        'change_rules': [{
            'resource_key': 'data.compute.instance_id',
            'change_key': 'instance_id'
        }, {
            'resource_key': 'data.compute.region',
            'change_key': 'region_name'
        }]
    }, {
        'key': 'instance_id',
        'name': 'Instance ID',
        'type': 'list',
        'resource_type': 'CUSTOM'
    },
    {
        'key': 'region_name',
        'name': 'Region',
        'type': 'list',
        'resource_type': 'CUSTOM'
    }
]
SUPPORTED_FEATURES = ['garbage_collection']
SUPPORTED_RESOURCE_TYPE = ['inventory.Server', 'inventory.Region']
NUMBER_OF_CONCURRENT = 20
SUPPORTED_SCHEDULES = ['hours']


@authentication_handler
class CollectorService(BaseService):
    def __init__(self, metadata):
        super().__init__(metadata)
        self.collector_manager: CollectorManager = self.locator.get_manager('CollectorManager')

    @transaction
    @check_required(['options'])
    def init(self, params):
        """ init plugin by options
        """
        capability = {
            'filter_format': FILTER_FORMAT,
            'supported_resource_type': SUPPORTED_RESOURCE_TYPE,
            'supported_features': SUPPORTED_FEATURES,
            'supported_schedules': SUPPORTED_SCHEDULES
        }
        return {'metadata': capability}

    @transaction
    @check_required(['options', 'secret_data'])
    def verify(self, params):
        """ verify options capability
        Args:
            params
              - options
              - secret_data: may be empty dictionary

        Returns:

        Raises:
             ERROR_VERIFY_FAILED:
        """
        manager = self.locator.get_manager('CollectorManager')
        secret_data = params['secret_data']
        options = params.get('options', {})
        active = manager.verify(options, secret_data)

        return {}

    @transaction
    @check_required(['options', 'secret_data', 'filter'])
    def collect(self, params):
        """ Get quick list of resources
        Args:
            params:
                - options
                - secret_data
                - filter

        Returns: list of resources
        """
        start_time = time.time()
        resource_regions = []
        collected_region_code = []

        for cloud_service_type in self.collector_manager.list_cloud_service_types():
            yield CloudServiceTypeResourceResponse({'resource': cloud_service_type})

        resource_groups = self.collector_manager.list_all_resource_groups(params)

        mt_params = []
        for rg in resource_groups:
            vms = self.collector_manager.list_vms(params, rg.name)

            if list(vms):
                mt_params.append({
                    'secret_data': params['secret_data'],
                    'resource_group': rg,
                    'vms': vms
                })
        '''
        if mt_params:
            for mt_param in mt_params:
                results = self.collector_manager.list_resources(mt_param)

                for result in results:
                    collected_region = self.collector_manager.get_region_from_result(result)

                    if collected_region is not None and collected_region.region_code not in collected_region_code:
                        resource_regions.append(collected_region)
                        collected_region_code.append(collected_region.region_code)

                    yield result, server_resource_format

                for resource_region in resource_regions:
                    yield resource_region, region_resource_format
        '''
        if mt_params:
            with concurrent.futures.ThreadPoolExecutor(max_workers=NUMBER_OF_CONCURRENT) as executor:
                future_executors = []
                for mt_param in mt_params:
                    future_executors.append(executor.submit(self.collector_manager.list_resources, mt_param))

                try:
                    for future in concurrent.futures.as_completed(future_executors):
                        for result in future.result():
                            if result.resource_type == 'inventory.Server':
                                try:
                                    collected_region = self.collector_manager.get_region_from_result(result.resource)

                                    if collected_region is not None and collected_region.region_code not in collected_region_code:
                                        resource_regions.append(collected_region)
                                        collected_region_code.append(collected_region.region_code)

                                except Exception as e:
                                    _LOGGER.error(f'[collect] {e}')

                                    if type(e) is dict:
                                        error_resource_response = ErrorResourceResponse({
                                            'message': json.dumps(e),
                                            'resource': {'resource_type': 'inventory.Region'}
                                        })
                                    else:
                                        error_resource_response = ErrorResourceResponse({
                                            'message': str(e),
                                            'resource': {'resource_type': 'inventory.Region'}
                                        })

                                    yield error_resource_response

                            yield result

                except Exception as e:
                    _LOGGER.error(f'failed to result {e}')

            for resource_region in resource_regions:
                yield RegionResourceResponse({'resource': resource_region})

        _LOGGER.debug(f'[collect] TOTAL FINISHED {time.time() - start_time} Sec')
