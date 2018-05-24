from YDchunK_common import YDchunK_IOSXR_Native
import ydk.types
from ydk.models.cisco_ios_xr import Cisco_IOS_XR_ifmgr_cfg, Cisco_IOS_XR_ipv4_bgp_cfg, Cisco_IOS_XR_ipv4_bgp_datatypes
from ydk.models.cisco_ios_xr import Cisco_IOS_XR_ipv4_bgp_datatypes as xr_ipv4_bgp_datatypes
from ydk.models.cisco_ios_xr import Cisco_IOS_XR_ip_static_cfg
from ydk.models.cisco_ios_xr import Cisco_IOS_XR_ifmgr_cfg

class YDchunK_IOSXR_Native_interface_dvulovic(YDchunK_IOSXR_Native):

    def __init__(self, xr_device):
        YDchunK_IOSXR_Native.__init__(self, xr_device)

    def print_interfaces(self):

            filter = Cisco_IOS_XR_ifmgr_cfg.InterfaceConfigurations()

            interfaces = self.xr.ydk_crud.read(self.xr.ydk_provider, filter)

            for intf in interfaces.interface_configuration:
                print(intf.interface_name)

class YDchunK_IOSXR_Native_static_dvulovic(YDchunK_IOSXR_Native):

    def __init__(self, xr_device):
        YDchunK_IOSXR_Native.__init__(self, xr_device)

    def print_static_route(self):

        filter = Cisco_IOS_XR_ip_static_cfg.RouterStatic()

        router_static = self.xr.ydk_crud.read(self.xr.ydk_provider, filter)

        if not router_static.default_vrf:
            return

        for vrf_prefix in router_static.default_vrf.address_family.vrfipv4.vrf_unicast.vrf_prefixes.vrf_prefix:
            print(vrf_prefix.prefix + "/" + str(vrf_prefix.prefix_length))

    def __create_RouterStatic_obj(self, arg_prefix,arg_prefixlen,arg_nexthop):

        router_static = Cisco_IOS_XR_ip_static_cfg.RouterStatic()

        vrf_unicast = router_static.default_vrf.address_family.vrfipv4.vrf_unicast
        vrf_prefix = vrf_unicast.vrf_prefixes.VrfPrefix()
        vrf_prefix.prefix = arg_prefix
        vrf_prefix.prefix_length = arg_prefixlen
        vrf_next_hop_next_hop_address = vrf_prefix.vrf_route.vrf_next_hop_table.VrfNextHopNextHopAddress()
        vrf_next_hop_next_hop_address.next_hop_address = arg_nexthop
        vrf_prefix.vrf_route.vrf_next_hop_table.vrf_next_hop_next_hop_address.append(vrf_next_hop_next_hop_address)
        vrf_unicast.vrf_prefixes.vrf_prefix.append(vrf_prefix)

        return router_static

    def add_static_route(self, arg_prefix,arg_prefixlen,arg_nexthop):

        router_static = self.__create_RouterStatic_obj(arg_prefix,arg_prefixlen,arg_nexthop)

        self.xr.ydk_crud.create(self.xr.ydk_provider, router_static)

        self.xr.ydk_crud.read(self.xr.ydk_provider, router_static)

    def delete_static_route(self, arg_prefix,arg_prefixlen,arg_nexthop):

        router_static = self.__create_RouterStatic_obj(arg_prefix,arg_prefixlen,arg_nexthop)

        self.xr.ydk_crud.delete(self.xr.ydk_provider, router_static.default_vrf.address_family.vrfipv4.vrf_unicast.vrf_prefixes.vrf_prefix[0])

    def check_if_static_route_exists(self, arg_prefix,arg_prefixlen,arg_nexthop):

        filter = self.__create_RouterStatic_obj(arg_prefix,arg_prefixlen,arg_nexthop)

        router_static = self.xr.ydk_crud.read(self.xr.ydk_provider, filter)

        if (router_static.default_vrf.address_family.vrfipv4.vrf_unicast.vrf_prefixes.vrf_prefix):
            return True
        else:
            return False

class YDchunK_IOSXR_Native_bgp_dvulovic(YDchunK_IOSXR_Native):

    def __init__(self, xr_device):
        YDchunK_IOSXR_Native.__init__(self, xr_device)

    def create_bgp_process(self, arg_asnum):
        bgp = Cisco_IOS_XR_ipv4_bgp_cfg.Bgp()

        instance = bgp.Instance()
        instance.instance_name = "default"

        instance_as = instance.InstanceAs()
        instance_as.as_ = 0

        instance_as_four_byte_as = instance_as.FourByteAs()
        instance_as_four_byte_as.bgp_running = ydk.types.Empty()
        instance_as_four_byte_as.as_ = arg_asnum
        instance_as.four_byte_as.append(instance_as_four_byte_as)

        instance.instance_as.append(instance_as)

        bgp.instance.append(instance)

        self.xr.ydk_crud.create(self.xr.ydk_provider, bgp)


    def add_bgp_neighbor(self, arg_asnumber, arg_neighbor_ip, arg_remote_as, arg_update_source=None):
        bgp = Cisco_IOS_XR_ipv4_bgp_cfg.Bgp()

        instance = bgp.Instance()
        instance.instance_name = "default"

        instance_as = instance.InstanceAs()
        instance_as.as_ = 0

        instance_as_four_byte_as = instance_as.FourByteAs()
        instance_as_four_byte_as.bgp_running = ydk.types.Empty()
        instance_as_four_byte_as.as_ = arg_asnumber

        neighbor = instance_as_four_byte_as.default_vrf.bgp_entity.neighbors.Neighbor()
        neighbor.neighbor_address = arg_neighbor_ip
        neighbor.remote_as.as_xx = 0
        neighbor.remote_as.as_yy = arg_remote_as
        if (arg_update_source):
            neighbor.update_source_interface = arg_update_source

        instance_as_four_byte_as.default_vrf.bgp_entity.neighbors.neighbor.append(neighbor)

        instance_as.four_byte_as.append(instance_as_four_byte_as)

        instance.instance_as.append(instance_as)

        bgp.instance.append(instance)

        self.xr.ydk_crud.create(self.xr.ydk_provider, bgp)


    def add_ipv4_unicast_SAFI_to_bgp_neighbor(self, arg_asnumber, arg_neighbor_ip):
        bgp = Cisco_IOS_XR_ipv4_bgp_cfg.Bgp()

        instance = bgp.Instance()
        instance.instance_name = "default"

        instance_as = instance.InstanceAs()
        instance_as.as_ = 0

        instance_as_four_byte_as = instance_as.FourByteAs()
        instance_as_four_byte_as.bgp_running = ydk.types.Empty()
        instance_as_four_byte_as.as_ = arg_asnumber

        neighbor = instance_as_four_byte_as.default_vrf.bgp_entity.neighbors.Neighbor()
        neighbor.neighbor_address = arg_neighbor_ip

        neighbor_af = neighbor.neighbor_afs.NeighborAf()
        neighbor_af.af_name = Cisco_IOS_XR_ipv4_bgp_datatypes.BgpAddressFamilyEnum.ipv4_unicast
        neighbor_af.activate = ydk.types.Empty()
        neighbor.neighbor_afs.neighbor_af.append(neighbor_af)

        instance_as_four_byte_as.default_vrf.bgp_entity.neighbors.neighbor.append(neighbor)

        instance_as.four_byte_as.append(instance_as_four_byte_as)

        instance.instance_as.append(instance_as)

        bgp.instance.append(instance)

        self.xr.ydk_crud.create(self.xr.ydk_provider, bgp)

    def add_bgp_ipv4_unicast_network(self, arg_asnum, arg_ip, arg_prefixlen):
        bgp = Cisco_IOS_XR_ipv4_bgp_cfg.Bgp()

        instance = bgp.Instance()
        instance.instance_name = "default"

        instance_as = instance.InstanceAs()
        instance_as.as_ = 0

        instance_as_four_byte_as = instance_as.FourByteAs()
        instance_as_four_byte_as.bgp_running = ydk.types.Empty()
        instance_as_four_byte_as.as_ = arg_asnum

        global_af = instance_as_four_byte_as.default_vrf.global_.global_afs.GlobalAf()
        global_af.af_name = xr_ipv4_bgp_datatypes.BgpAddressFamilyEnum.ipv4_unicast
        global_af.enable = ydk.types.Empty()

        sourced_network = global_af.sourced_networks.SourcedNetwork()
        sourced_network.network_addr = arg_ip
        sourced_network.network_prefix = arg_prefixlen

        global_af.sourced_networks.sourced_network.append(sourced_network)

        instance_as_four_byte_as.default_vrf.global_.global_afs.global_af.append(global_af)

        instance_as.four_byte_as.append(instance_as_four_byte_as)

        instance.instance_as.append(instance_as)

        bgp.instance.append(instance)

        self.xr.ydk_crud.create(self.xr.ydk_provider, bgp)
