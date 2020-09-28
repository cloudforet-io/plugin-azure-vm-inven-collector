from schematics import Model
from schematics.types import ModelType, StringType, BooleanType, ListType


class Tags(Model):
    Key = StringType()
    Value = StringType()


class Azure(Model):
    # TODO
    ultra_ssd_enabled = BooleanType(default=False)
    write_accelerator_enabled = BooleanType(default=False)
    boot_diagnostics = BooleanType(default=True)
    priority = StringType(choices=('Regular', 'Low', 'Spot'))
    tags = ListType(ModelType(Tags))
    pass

