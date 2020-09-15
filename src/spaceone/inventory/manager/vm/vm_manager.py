from spaceone.core.manager import BaseManager
from spaceone.inventory.model.compute import Compute
from spaceone.inventory.model.aws import AWS
from spaceone.inventory.model.os import OS
from spaceone.inventory.model.hardware import Hardware
from spaceone.inventory.connector.ec2_connector import EC2Connector


class EC2InstanceManager(BaseManager):

    def __init__(self, params, ec2_connector=None, **kwargs):
        super().__init__(**kwargs)
        self.params = params
        self.ec2_connector: EC2Connector = ec2_connector
