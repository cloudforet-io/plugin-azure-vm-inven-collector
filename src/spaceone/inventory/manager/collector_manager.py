__all__ = ['CollectorManager']

import time
import logging
from spaceone.core.manager import BaseManager
# from spaceone.inventory.connector import EC2Connector
# from spaceone.inventory.manager.ec2 import EC2InstanceManager, AutoScalingGroupManager, LoadBalancerManager, \
#     DiskManager, NICManager, VPCManager, SecurityGroupManager, CloudWatchManager
# from spaceone.inventory.manager.metadata.metadata_manager import MetadataManager
# from spaceone.inventory.model.server import Server, ReferenceModel
# from spaceone.inventory.model.region import Region


class CollectorManager(BaseManager):

    def __init__(self, transaction):
        super().__init__(transaction)
