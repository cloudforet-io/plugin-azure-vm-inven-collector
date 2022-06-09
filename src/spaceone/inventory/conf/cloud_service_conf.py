SUPPORTED_FEATURES = ['garbage_collection']
SUPPORTED_RESOURCE_TYPE = ['inventory.Server', 'inventory.Region']
NUMBER_OF_CONCURRENT = 20
SUPPORTED_SCHEDULES = ['hours']
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

REGION_INFO = {
    'eastus': {'name': 'US East (Virginia)',
               'tags': {'latitude': '37.3719', 'longitude': '-79.8164', 'continent': 'north_america'}},
    'eastus2': {'name': 'US East 2 (Virginia)',
                'tags': {'latitude': '36.6681', 'longitude': '-78.3889', 'continent': 'north_america'}},
    'westus': {'name': 'US West (California)',
               'tags': {'latitude': '37.783', 'longitude': '-122.417', 'continent': 'north_america'}},
    'westus2': {'name': 'US West 2 (Washington)',
                'tags': {'latitude': '47.233', 'longitude': '-119.852', 'continent': 'north_america'}},
    'centralus': {'name': 'US Central (Iowa)',
                  'tags': {'latitude': '41.5908', 'longitude': '-93.6208', 'continent': 'north_america'}},
    'southcentralus': {'name': 'US South Central (Texas)',
                       'tags': {'latitude': '29.4167', 'longitude': '-98.5', 'continent': 'north_america'}},
    'northcentralus': {'name': 'US North Central (Illinois)',
                       'tags': {'latitude': '41.8819', 'longitude': '-87.6278', 'continent': 'north_america'}},
    'westcentralus': {'name': 'US West Central (Wyoming)',
                      'tags': {'latitude': '40.890', 'longitude': '-110.234', 'continent': 'north_america'}},
    'canadacentral': {'name': 'Canada Central (Toronto)',
                      'tags': {'latitude': '43.653', 'longitude': '-79.383', 'continent': 'north_america'}},
    'canadaeast': {'name': 'Canada East (Quebec)',
                   'tags': {'latitude': '46.817', 'longitude': '-71.217', 'continent': 'north_america'}},
    'southafricanorth': {'name': 'South Africa North (Johannesburg)',
                         'tags': {'latitude': '-25.731340', 'longitude': '28.218370', 'continent': 'africa'}},
    'southafricawest': {'name': 'South Africa West (Cape Town)',
                        'tags': {'latitude': '-34.075691', 'longitude': '18.843266', 'continent': 'africa'}},
    'eastasia': {'name': 'Asia Pacific East (Hong Kong)',
                 'tags': {'latitude': '22.267', 'longitude': '114.188', 'continent': 'asia_pacific'}},
    'centralindia': {'name': 'Asia Pacific Central India (Pune)',
                     'tags': {'latitude': '18.5822', 'longitude': '73.9197', 'continent': 'asia_pacific'}},
    'southindia': {'name': 'Asia Pacific South India (Chennai)',
                   'tags': {'latitude': '12.9822', 'longitude': '80.1636', 'continent': 'asia_pacific'}},
    'westindia': {'name': 'Asia Pacific West India (Mumbai)',
                  'tags': {'latitude': '19.088', 'longitude': '72.868', 'continent': 'asia_pacific'}},
    'southeastasia': {'name': 'Asia Pacific South East (Singapore)',
                      'tags': {'latitude': '1.283', 'longitude': '103.833', 'continent': 'asia_pacific'}},
    'japaneast': {'name': 'Asia Pacific Japan East (Tokyo, Saitama)',
                  'tags': {'latitude': '35.68', 'longitude': '139.77', 'continent': 'asia_pacific'}},
    'japanwest': {'name': 'Asia Pacific Japan West (Osaka)',
                  'tags': {'latitude': '34.6939', 'longitude': '135.5022', 'continent': 'asia_pacific'}},
    'koreacentral': {'name': 'Asia Pacific Korea Central (Seoul)',
                     'tags': {'latitude': '37.5665', 'longitude': '126.9780', 'continent': 'asia_pacific'}},
    'koreasouth': {'name': 'Asia Pacific Korea South (Busan)',
                   'tags': {'latitude': '35.1796', 'longitude': '129.0756', 'continent': 'asia_pacific'}},
    'australiaeast': {'name': 'Asia Pacific Australia East (New South Wales)',
                      'tags': {'latitude': '-33.86', 'longitude': '151.2094', 'continent': 'asia_pacific'}},
    'australiacentral': {'name': 'Asia Pacific Australia Central (Canberra)',
                         'tags': {'latitude': '-35.3075', 'longitude': '149.1244',
                                  'continent': 'asia_pacific'}},
    'australiacentral2': {'name': 'Asia Pacific Australia Central 2 (Canberra)',
                          'tags': {'latitude': '-35.3075', 'longitude': '149.1244',
                                   'continent': 'asia_pacific'}},
    'australiasoutheast': {'name': 'Asia Pacific Australia South East (Victoria)',
                           'tags': {'latitude': '-37.8136', 'longitude': '144.9631',
                                    'continent': 'asia_pacific'}},
    'northeurope': {'name': 'North Europe (Ireland)',
                    'tags': {'latitude': '53.3478', 'longitude': '-6.2597', 'continent': 'europe'}},
    'norwayeast': {'name': 'North Europe (Norway East)',
                   'tags': {'latitude': '59.913868', 'longitude': '10.752245', 'continent': 'europe'}},
    'norwaywest': {'name': 'North Europe (Norway West)',
                   'tags': {'latitude': '58.969975', 'longitude': '5.733107', 'continent': 'europe'}},
    'germanywestcentral': {'name': 'Europe Germany West Central (Frankfurt)',
                           'tags': {'latitude': '50.110924', 'longitude': '8.682127', 'continent': 'europe'}},
    'germanynorth': {'name': 'Europe Germany North (Berlin)',
                     'tags': {'latitude': '53.073635', 'longitude': '8.806422', 'continent': 'europe'}},
    'switzerlandnorth': {'name': 'Europe Switzerland North (Zurich)',
                         'tags': {'latitude': '47.451542', 'longitude': '8.564572', 'continent': 'europe'}},
    'switzerlandwest': {'name': 'Europe Switzerland West (Geneva)',
                        'tags': {'latitude': '46.204391', 'longitude': '6.143158', 'continent': 'europe'}},
    'swedencentral': {'name': 'Sweden Central', 'tags': {'latitude': '60.67488', 'longitude': '17.14127'}},
    'francecentral': {'name': 'Europe France Central (Paris)',
                      'tags': {'latitude': '46.3772', 'longitude': '2.3730', 'continent': 'europe'}},
    'francesouth': {'name': 'Europe France South (Marseille)',
                    'tags': {'latitude': '43.8345', 'longitude': '2.1972', 'continent': 'europe'}},
    'westeurope': {'name': 'West Europe (Netherlands)',
                   'tags': {'latitude': '52.3667', 'longitude': '4.9', 'continent': 'europe'}},
    'uksouth': {'name': 'UK South (London)',
                'tags': {'latitude': '50.941', 'longitude': '-0.799', 'continent': 'europe'}},
    'ukwest': {'name': 'UK West (Cardiff)',
               'tags': {'latitude': '53.427', 'longitude': '-3.084', 'continent': 'europe'}},
    'uaenorth': {'name': 'Middle East UAE North (Dubai)',
                 'tags': {'latitude': '25.266666', 'longitude': '55.316666', 'continent': 'middle_east'}},
    'uaecentral': {'name': 'Middle East UAE Central (Abu Dhabi)',
                   'tags': {'latitude': '24.466667', 'longitude': '54.366669', 'continent': 'middle_east'}},
    'brazilsouth': {'name': 'South America Brazil South (Sao Paulo State)',
                    'tags': {'latitude': '-23.55', 'longitude': '-46.633', 'continent': 'south_america'}},
    'brazilsoutheast': {'name': 'South America Brazil South East (Rio)',
                        'tags': {'latitude': '-22.90278', 'longitude': '-43.2075',
                                 'continent': 'south_america'}}
}