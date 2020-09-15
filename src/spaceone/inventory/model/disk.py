from schematics import Model
from schematics.types import StringType, IntType, BooleanType, ModelType, FloatType


class DiskTags(Model):
    # TODO
    pass


class Disk(Model):
    device_index = IntType()
    device = StringType()
    disk_type = StringType(default="Disk")
    size = FloatType()
    tags = ModelType(DiskTags, default={})
