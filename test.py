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
        print(next(resource_group))

        for rsc_g in resource_group:
            resource_group_name = rsc_g.name
            # rg_list = resource_client.resources.list_by_resource_group(resource_group_name)
            compute = compute_client.virtual_machines.list(resource_group_name)
            # for comp in compute:
            #     print(comp)


if __name__ == "__main__":
    main()