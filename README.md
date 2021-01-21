# Azure VM Collector Plugin

## ABOUT
**Azure VM Collector** collects Microsoft Azure VMs in user's subscription. You can check all VMs belonging to the resource group and subscription. In addition, associated services such as Load Balancer, Security Groups, NIC, Scale Sets are also displayed through Azure VM Collector.

![Microsoft Azure Cloud Services](https://spaceone-custom-assets.s3.ap-northeast-2.amazonaws.com/console-assets/icons/azure-cloud-services.svg)
**Plugin to collect Microsoft Azure Cloud Services**

> SpaceONE's [plugin-azure-cloud-services](https://github.com/spaceone-dev/plugin-azure-vm) is a convenient tool to 
get cloud service data from Microsoft Azure Cloud Services. 

Find us also at [Dockerhub](https://hub.docker.com/r/spaceone/azure-vm)
> Latest stable version : 1.2.1

Please contact us if you need any further information. 
<support@spaceone.dev>


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

* Table of Contents
    * [Virtual Machines](#Azure_VM_(Instance))
        * [Azure VM (Instance)](#azure_vm_instance)
        * [Disk](#disks)
        * [NIC](#NIC)
        * [Network Security Groups](#network_security_groups)
        * [Load Balancer](#load_balancer)

---

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

- Disks
    - Permissions
        - Microsoft.Compute/disks/read	
        
- NIC
    - Permissions
        - Microsoft.Network/networkInterfaces/read	
     
- Network Security Groups
    - Permissions
        - Microsoft.Network/networkSecurityGroups/read	
    
- Load Balancer
    - Permissions
        - Microsoft.Network/loadBalancers/read

