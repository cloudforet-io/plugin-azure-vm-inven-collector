from schematics import Model
from schematics.types import  StringType, DateTimeType, ListType, BooleanType, ModelType, DictType


class ComputeTags(Model):
    id = StringType()


class Compute(Model):
    keypair = StringType()
    az = StringType()
    instance_state = StringType(choices=('STARTING', 'RUNNING', 'STOPPING', 'STOPPED', 'DEALLOCATING', 'DEALLOCATED'))
    instance_type = StringType()
    launched_at = DateTimeType()
    instance_id = StringType(default='')
    instance_name = StringType(default='')
    security_groups = ListType(StringType())
    image = StringType()
    account = StringType()
    tags = ModelType(ComputeTags, default={})
