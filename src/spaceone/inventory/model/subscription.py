from schematics import Model
from schematics.types import StringType


class Subscription(Model):
    subscription_id = StringType()
    subscription_name = StringType()
    tenant_id = StringType()
    tenant_name = StringType(serialize_when_none=False)
    domain = StringType(serialize_when_none=False)

