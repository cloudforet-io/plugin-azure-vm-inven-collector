__all__ = ["AzureVMConnector"]

import logging
from spaceone.core.error import *
from spaceone.core import utils
from spaceone.core.connector import BaseConnector

_LOGGER = logging.getLogger(__name__)
DEFAULT_REGION = ''


class AzureVMConnector(BaseConnector):

    def __init__(self, transaction=None, config=None):
        pass