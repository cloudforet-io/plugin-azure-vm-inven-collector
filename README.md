# Azure VM Collector Plugin

## ABOUT
**Azure VM Collector** collects Microsoft Azure VMs in user's subscription. You can check all VMs belonging to the resource group and subscription. In addition, associated services such as Load Balancer, Security Groups, NIC, Scale Sets are also displayed through Azure VM Collector.

## SETTING
You should insert information about account in SpaceONE's **Service Account** initially.
* Base Information
	* `name`
	* `Tenant ID`
	* `Subscription ID`
	* `Tag`

* Credentials
	* `Tenant ID`
	* `Subscription ID`
	* `Client Secret`
	* `Client ID`

## CONTENTS
The information collected for each VM is as follows.

* VM - name, region, ip addresses, os, disk, nic, hardware
* Security Groups
* Load Balancers
* Subscription, Resource Group, Subnet, Vnet
* VM Scale Sets
