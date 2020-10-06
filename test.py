import os

from azure.identity import DefaultAzureCredential
from azure.mgmt.compute import ComputeManagementClient
from azure.mgmt.network import NetworkManagementClient
from azure.mgmt.resource import ResourceManagementClient
from azure.mgmt.resource import SubscriptionClient
from azure.mgmt.monitor import MonitorClient
# from azure.common.client_factory import import get_client_from_auth_file


def main():

    credential = DefaultAzureCredential()

    subscription_client = SubscriptionClient(credential)
    subscription = subscription_client.subscriptions.list()

    for subsc in subscription:
        subscription_id = subsc.subscription_id

        compute_client = ComputeManagementClient(
            credential=DefaultAzureCredential(),
            subscription_id=subscription_id
        )
        network_client = NetworkManagementClient(
            credential=DefaultAzureCredential(),
            subscription_id=subscription_id
        )

        monitor_client = MonitorClient(
            credential=DefaultAzureCredential(),
            subscription_id=subscription_id
        )

        # monitor = monitor_client.operations
        # val = monitor.list().value
        # for v in val:
        #     print(v.display.resource)

        resource_client = ResourceManagementClient(credential, subscription_id)
        resource_group = resource_client.resource_groups.list()

        for rsc_g in resource_group:
            resource_group_name = rsc_g.name
            compute = compute_client.virtual_machines.list(resource_group_name)
            for comp in compute:
                print(comp)
                # name = comp.name
                # extensions = compute_client.virtual_machine_extensions.list(resource_group_name, name)
                # print(extensions.value[0])

        # for rsc_g in resource_group:
        #     resource_group_name = rsc_g.name
        #     compute = compute_client.virtual_machines.list(resource_group_name)
        #     for comp in compute:
        #         data_disk = comp.diagnostics_profile
        #         if data_disk is not None:
        #             print(data_disk.boot_diagnostics.enabled)




            # rg_list = resource_client.resources.list_by_resource_group(resource_group_name)
        #
        #     for rg in rg_list:
        #         if rg.type == "Microsoft.Compute/virtualMachines":
        #             azure = compute_client.virtual_machines.get(resource_group_name, rg.name)
        #             print(azure.storage_profile.image_reference)




            # load_balancer = network_client.application_gateways.list(resource_group_name)
            # for lb in load_balancer:
            #     fe_ip_config = lb.frontend_ip_configurations
            #     for fe in fe_ip_config:
            #         if fe.public_ip_address is not None:
            #             ip_arr = fe.public_ip_address.id.split('/')
            #             ip_name = ip_arr[-1]
            #
            #             ip_info = network_client.public_ip_addresses.get(resource_group_name, ip_name)
            #             print(ip_info.ip_address)


if __name__ == "__main__":
    main()