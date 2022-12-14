from schematics import Model
from schematics.types import StringType


class OS(Model):
    os_distro = StringType()
    os_arch = StringType(default='x86_64')
    details = StringType()
    os_type = StringType(choices=('LINUX', 'WINDOWS'))