# plugin-azure-vm-inven-collector

![Microsoft Azure Cloud Services](https://spaceone-custom-assets.s3.ap-northeast-2.amazonaws.com/console-assets/icons/azure-cloud-services.svg)
**Plugin to collect Microsoft Azure VM (Virtual Machine)**

**Azure VM Collector** collects Microsoft Azure VMs in user's subscription. You can check all VMs belonging to the resource group and subscription. In addition, associated services such as Load Balancer, Security Groups, NIC, Scale Sets are also displayed through Azure VM Collector.

> SpaceONE's [plugin-azure-vm-inven-collector](https://github.com/spaceone-dev/plugin-azure-vm-inven-collector) is a convenient tool to 
get cloud service data from Microsoft Azure VM. 

Find us also at [Dockerhub](https://hub.docker.com/r/spaceone/azure-vm)
> Latest stable version : 1.2.14

Please contact us if you need any further information. 
<support@spaceone.dev>


## Setting
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


## Contents
The information collected for each VM is as follows.

 * Virtual Machines
    * Azure VM (Instance)
    * Disk
    * NIC
    * Network Security Groups
    * Load Balancer


## Authentication Overview
Registered service account on SpaceONE must have certain permissions to collect cloud service data 
Please, set authentication privilege for followings:
 

#### [Virtual Machines](https://docs.microsoft.com/ko-kr/rest/api/compute/virtualmachines/list)

- Azure VM (Instance)
    - Scope
        - https://docs.microsoft.com/ko-kr/rest/api/compute/virtualmachines/listall
        - https://docs.microsoft.com/ko-kr/rest/api/compute/virtualmachines/get
        - https://docs.microsoft.com/ko-kr/rest/api/virtualnetwork/virtualnetworks/list
        - https://docs.microsoft.com/ko-kr/rest/api/virtualnetwork/publicipaddresses/list
        - https://docs.microsoft.com/ko-kr/rest/api/virtualnetwork/virtualnetworks
        - https://docs.microsoft.com/ko-kr/rest/api/virtualnetwork/networkinterfaces
        - https://docs.microsoft.com/ko-kr/rest/api/virtualnetwork/networksecuritygroups
		
    - Permissions
        - Microsoft.Compute/*/read
        - Microsoft.Resources/*/read
        - Microsoft.Network/networkInterfaces/read	
        - Microsoft.Network/publicIPAddresses/read
        - Microsoft.Network/networkSecurityGroups/read
        - Microsoft.Network/loadBalancers/read
	

## Release Notes
### Ver 1.2.14
* [Add fields to cloud services model(account, instance_type, instance_size, launched_at)](https://github.com/spaceone-dev/plugin-azure-vm-inven-collector/issues/89) 
* [Add ErrorResources to collect error messages as resources](https://github.com/spaceone-dev/plugin-azure-vm-inven-collector/issues/84)

### Ver 1.2.13
* [Add RegionResource to collect error messages as resources](https://github.com/spaceone-dev/plugin-azure-vm-inven-collector/issues/84)
* [Update CI workflows](https://github.com/spaceone-dev/plugin-azure-vm-inven-collector/commit/6e00cda34b953d1bc84e6cf75cb0fb338595058e)
