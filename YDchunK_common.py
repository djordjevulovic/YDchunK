from ydk.services.crud_service import CRUDService
from ydk.providers.netconf_provider import NetconfServiceProvider

class YDchunK_NETCONF_Device:

    def __init__(self, host, port, username, password):

        self.host = host
        self.port = port
        self.username = username
        self.password = password

        self.ydk_provider = NetconfServiceProvider(address=self.host, port=self.port, username=self.username, password=self.password, protocol='ssh')

        self.ydk_crud = CRUDService()

class YDchunK_IOSXR_Device(YDchunK_NETCONF_Device):

    def __init__(self, host, port, username, password):

        YDchunK_NETCONF_Device.__init__(self, host, port, username, password)

class YDchunK_IOSXR_Generic:

    def __init__(self, xr_device):
            self.xr = xr_device

class YDchunK_IOSXR_Native(YDchunK_IOSXR_Generic):

    def __init__(self, xr_device):
        YDchunK_IOSXR_Generic.__init__(self, xr_device)

class YDchunK_IOSXR_OpenConfig(YDchunK_IOSXR_Generic):

    def __init__(self, xr_device):
        YDchunK_IOSXR_Generic.__init__(self, xr_device)
