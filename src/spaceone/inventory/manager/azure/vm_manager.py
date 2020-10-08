from spaceone.core.manager import BaseManager
from spaceone.inventory.model.compute import Compute
from spaceone.inventory.model.azure import Azure
from spaceone.inventory.model.os import OS
from spaceone.inventory.model.hardware import Hardware
from spaceone.inventory.connector.azure_vm_connector import AzureVMConnector


class AzureVmManager(BaseManager):

    def __init__(self, params, azure_vm_connector=None, **kwargs):
        super().__init__(**kwargs)
        self.params = params
        self.azure_vm_connector: AzureVMConnector = azure_vm_connector

    def list_vms(self, resource_group):
        return self.azure_vm_connector.list_vms(resource_group)

    def get_vm_info(self, vm):
        '''
        server_data = {
            "os_type": "LINUX" | "WINDOWS"
            "name": ""
            "ip_addresses": [],
            "primary_ip_address": "",
            "data":  {
                "os": {
                    "os_distro": "",
                    "os_arch": "",
                    "os_details": ""
                },
                "azure": {
                    "boot_diagnostics": "true" | "false",
                    "ultra_ssd_enabled": "true" | "false",
                    "write_accelerator_enabled": "true" | "false",
                    "priority": "Regular" | "Low" | "Spot",
                    "tags": {
                        "Key": "",
                        "Value": ""
                    },
                },
                "hardware": {
                    "core": 0,
                    "memory": 0
                },
                "compute": {
                    "keypair": "",
                    "availability_zone": "",
                    "instance_state": "",
                    "instance_type": "",
                    "launched_at": "datetime",
                    "instance_id": "",
                    "instance_name": "",
                    "security_groups": [
                        {
                            "id": "",
                            "name": "",
                            "display": ""
                        },
                        ...
                    ],
                    "image": "",
                    "account": "",
                    "tags": {
                        "id": ""
                    }
                },
            }
        }
        '''

        vm_dic = self.get_vm_dic(vm)
        os_data = self.get_os_data(vm.storage_profile)
        hardware_data = self.get_hardware_data(vm)
        azure_data = self.get_azure_data(vm)
        compute_data = self.get_compute_data(vm)

        vm_dic.update({
            'data': {
                'os': os_data,
                'hardware': hardware_data,
                'azure': azure_data,
                'compute': compute_data
            }
        })

        return vm_dic

    def get_vm_dic(self, vm):
        vm_data = {
            'name': vm.name,
            'os_type': self.get_os_type(vm.storage_profile.os_disk),
            'region_code': vm.location
        }
        return vm_data

    def get_os_data(self, vm_storage_profile):
        os_data = {
            'os_distro': self.get_os_distro(vm_storage_profile.image_reference.offer),
            'os_arch': '',
            'os_details': self.get_os_details(vm_storage_profile.image_reference)
        }
        return OS(os_data, strict=False)

    def get_hardware_data(self, vm):
        # vm_size = self.match_vm_type(vm.hardware_profile.vm_size)
        location = vm.location

        hardware_data = {
            'core': self.get_vm_size(location=location).get('number_of_cores'),
            'memory': round(float((self.get_vm_size(location=location).get('memory_in_mb'))/1024), 2)
        }
        return Hardware(hardware_data, strict=False)

    def get_compute_data(self, vm):
        compute_data = {
            'az': vm.location,
            'instance_state': vm.instance_view.statuses.display_status,
            'instance_id': vm.vm_id,
            'instance_name': vm.name,
            'tags': ''
        }
        return Compute(compute_data, strict=False)

    def get_azure_data(self, vm):
        azure_data = {
            'boot_diagnostics': vm.diagnostics_profile.boot_diagnostics.enabled,
            'ultra_ssd_enabled': vm.additional_capabilities.ultra_ssd_enabled,
            'write_accelerator_enabled': vm.storage_profile.os_disk.write_accelerator_enabled,
            'priority': vm.priority,
            'tags': ''
        }
        return Azure(azure_data, strict=False)

    @staticmethod
    def get_os_type(os_disk):
        return os_disk.os_type.upper()

    def get_vm_size(self, location):
        return self.azure_vm_connector.list_virtual_machine_sizes(location)

    @staticmethod
    def get_os_distro(offer):
        return offer.lower()

    @staticmethod
    def get_os_details(image_reference):
        publisher = image_reference.publisher
        offer = image_reference.offer
        sku = image_reference.sku
        os_details = publisher + ', ' + offer + ', ' + sku
        return os_details

    @staticmethod
    def match_vm_type(vm_size):
        # TODO: find vm_size_list checking method
        pass
