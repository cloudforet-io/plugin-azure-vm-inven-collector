from schematics import Model
from schematics.types import  StringType, DateTimeType, ListType, BooleanType, ModelType, DictType


class SecurityGroups(Model):
    display = StringType()
    id = StringType()
    name = StringType()


class ComputeTags(Model):
    vm_id = StringType()


class Compute(Model):
    keypair = StringType()
    az = StringType()
    instance_state = StringType(choices=('STARTING', 'RUNNING', 'STOPPING', 'STOPPED', 'DEALLOCATING', 'DEALLOCATED'))
    instance_type = StringType()
    launched_at = DateTimeType()
    instance_id = StringType(default='')
    instance_name = StringType(default='')
    security_groups = ListType(ModelType(SecurityGroups))
    image = StringType()
    account = StringType(default='')
    tags = ModelType(ComputeTags, default={})
