from YDchunK_common import YDchunK_IOSXR_OpenConfig
from ydk.models.openconfig.openconfig_interfaces import Interfaces as OpenConfig_Interfaces
from ydk.models.openconfig.openconfig_bgp import Bgp as OpenConfig_Bgp
from ydk.models.openconfig.openconfig_bgp_types import Ipv4UnicastIdentity as OpenConfig_Ipv4UnicastIdentity
from ydk.models.ietf.iana_if_type import SoftwareloopbackIdentity

class YDchunK_IOSXR_OpenConfig_interface_dvulovic(YDchunK_IOSXR_OpenConfig):

    def __init__(self, xr_device):
        YDchunK_IOSXR_OpenConfig.__init__(self, xr_device)


    def create_loopack(self, arg_loopbacknum, arg_ip, arg_prefixlen):
        """
          <interfaces xmlns="http://openconfig.net/yang/interfaces">
           <interface>
            <name>Loopback0</name>
            <config>
             <name>Loopback0</name>
             <type xmlns:idx="urn:ietf:params:xml:ns:yang:iana-if-type">idx:softwareLoopback</type>
             <enabled>true</enabled>
            </config>
            <subinterfaces>
             <subinterface>
              <index>0</index>
              <ipv4 xmlns="http://openconfig.net/yang/interfaces/ip">
               <address>
                <ip>172.16.255.1</ip>
                <config>
                 <ip>172.16.255.1</ip>
                 <prefix-length>32</prefix-length>
                </config>
               </address>
              </ipv4>
             </subinterface>
            </subinterfaces>
           </interface>
        """
        oc_interface = OpenConfig_Interfaces.Interface()

        oc_interface.name = "Loopback" + arg_loopbacknum
        oc_interface.config.name = "Loopback" + arg_loopbacknum
        oc_interface.config.type = SoftwareloopbackIdentity()
        oc_interface.config.enabled = True

        oc_subinterface = oc_interface.subinterfaces.Subinterface()
        oc_subinterface.index = 0

        oc_subinterface_ipv4 = oc_subinterface.Ipv4()

        oc_subinterface_ipv4_address = oc_subinterface_ipv4.Address()
        oc_subinterface_ipv4_address.ip = arg_ip
        oc_subinterface_ipv4_address.config.ip = arg_ip
        oc_subinterface_ipv4_address.config.prefix_length = arg_prefixlen
        oc_subinterface_ipv4.address.append(oc_subinterface_ipv4_address)

        oc_subinterface.ipv4 = oc_subinterface_ipv4

        oc_interface.subinterfaces.subinterface.append(oc_subinterface)

        self.xr.ydk_crud.create(self.xr.ydk_provider, oc_interface)

class YDchunK_IOSXR_OpenConfig_bgp_dvulovic(YDchunK_IOSXR_OpenConfig):

    def __init__(self, xr_device):
        YDchunK_IOSXR_OpenConfig.__init__(self, xr_device)

    def create_bgp_procces(self, arg_asnumber):
        oc_bgp = OpenConfig_Bgp()
        oc_bgp.global_.config.as_ = arg_asnumber

        self.xr.ydk_crud.create(self.xr.ydk_provider, oc_bgp)


    def add_bgp_neighbor(self, arg_asnumber, arg_neighbor_ip, arg_remote_as, arg_update_source=None):
        oc_bgp = OpenConfig_Bgp()

        oc_neighor = oc_bgp.neighbors.Neighbor()
        oc_neighor.neighbor_address = arg_neighbor_ip
        oc_neighor.config.neighbor_address = arg_neighbor_ip
        oc_neighor.config.peer_as = arg_remote_as

        if (arg_update_source):
            oc_neighor.transport.config.local_address = arg_update_source

        oc_bgp.neighbors.neighbor.append(oc_neighor)

        self.xr.ydk_crud.create(self.xr.ydk_provider, oc_bgp)


    def add_ipv4_unicast_SAFI_to_bgp_neighbor(self, arg_asnumber, arg_neighbor_ip):
        oc_bgp = OpenConfig_Bgp()

        oc_neighor = oc_bgp.neighbors.Neighbor()
        oc_neighor.neighbor_address = arg_neighbor_ip

        oc_safi = oc_neighor.afi_safis
        oc_safi = oc_neighor.afi_safis.AfiSafi()
        oc_safi.afi_safi_name = OpenConfig_Ipv4UnicastIdentity()
        oc_safi.config.enabled = True
        oc_safi.config.afi_safi_name = OpenConfig_Ipv4UnicastIdentity()

        oc_neighor.afi_safis.afi_safi.append(oc_safi)

        oc_bgp.neighbors.neighbor.append(oc_neighor)

        self.xr.ydk_crud.create(self.xr.ydk_provider, oc_bgp)
