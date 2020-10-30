from schematics import Model
from schematics.types import StringType, IntType, BooleanType, ModelType, FloatType


class DiskTags(Model):
    disk_name = StringType()
    caching = StringType(choices=('None', 'ReadOnly', 'ReadWrite'))
    storage_account_type = StringType(choices=('Standard_LRS', 'Premium_LRS', 'StandardSSD_LRS', 'UltraSSD_LRS'))
    disk_encryption_set = StringType(choices=('PMK', 'CMK'), default='PMK')
    iops = IntType()
    throughput_mbps = IntType()


class Disk(Model):
    device_index = IntType()
    device = StringType()
    disk_type = StringType(choices=('os_disk', 'data_disk'))
    size = FloatType()
    tags = ModelType(DiskTags, default={})
