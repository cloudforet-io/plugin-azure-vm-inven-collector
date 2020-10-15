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

    def list_vms(self, resource_group_name):
        return self.azure_vm_connector.list_vms(resource_group_name)

    def get_vm_info(self, vm, resource_group_name):
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

        print("IN!!")

        vm_dic = self.get_vm_dic(vm)
        os_data = self.get_os_data(vm.storage_profile)
        hardware_data = self.get_hardware_data(vm)
        azure_data = self.get_azure_data(vm)
        compute_data = self.get_compute_data(vm, resource_group_name)

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
        location = vm.location
        size = vm.hardware_profile.vm_size

        hardware_data = self.get_vm_hardware_info(location, size)

        return Hardware(hardware_data, strict=False)

    def get_compute_data(self, vm, resource_group_name):
        compute_data = {
            'az': vm.location,
            'instance_state': vm.instance_view.statuses.display_status,
            'instance_type': vm.hardware_profile.vm_size,
            'launched_at': self.get_launched_time(vm.storage_profile.os_disk.managed_disk, resource_group_name),
            'instance_id': vm.vm_id,
            'instance_name': vm.name,
            'security_groups': self.get_security_groups(vm.network_profile.network_interfaces, resource_group_name),
            'image': self.get_os_details(vm.storage_profile.image_reference),
            'tags': {
                'id': vm.id
            }
        }
        return Compute(compute_data, strict=False)

    def get_azure_data(self, vm):
        azure_data = {
            'boot_diagnostics': vm.diagnostics_profile.boot_diagnostics,
            'ultra_ssd_enabled': vm.additional_capabilities.ultra_ssd_enabled,
            'write_accelerator_enabled': vm.storage_profile.os_disk.write_accelerator_enabled,
            'priority': vm.priority,
            'tags': self.get_tags(vm.tags)

        }
        return Azure(azure_data, strict=False)

    def get_vm_hardware_info(self, location, size):
        result = {}
        vm_sizes = self.azure_vm_connector.list_virtual_machine_sizes(location)
        for vm_size in vm_sizes:
            if vm_size.name == size:
                result.update({'core': vm_size.number_of_cores})
                result.update({'memory': round(float(vm_size.memory_in_mb/1074), 2)})

        return result

    def get_launched_time(self, managed_disk, resource_group_name):
        disk_name_arr = managed_disk.id.split('/')
        disk_name = disk_name_arr[-1]
        disk_info = self.azure_vm_connector.list_nic_disks(resource_group_name, disk_name)
        return disk_info.time_created

    def get_security_groups(self, network_interfaces, resource_group_name):
        for nic in network_interfaces:
            id_arr = nic.id.split('/')
            nic_name = id_arr[-1]
            list_nic = self.azure_vm_connector.list_network_interfaces(resource_group_name, nic_name)
            return list_nic.network_security_group.id

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

    @staticmethod
    def get_tags(tags):
        tags_result = []
        if tags is not None:
            for k, v in tags.items():
                tag_info = {}
                tag_info.update({'key': k})
                tag_info.update({'value': v})
                tags_result.append(tag_info)

        return tags_result
