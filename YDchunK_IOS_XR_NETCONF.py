from ncclient import manager
from lxml import etree
import datetime
from io import StringIO, BytesIO
from ydk.models.cisco_ios_xr import Cisco_IOS_XR_ip_static_cfg
from ydk.models.cisco_ios_xr import Cisco_IOS_XR_ifmgr_cfg, Cisco_IOS_XR_ipv4_bgp_cfg, Cisco_IOS_XR_ipv4_bgp_datatypes
from ydk.models.openconfig.openconfig_interfaces import Interfaces as OpenConfig_Interfaces
from ydk.models.openconfig.openconfig_bgp import Bgp as OpenConfig_Bgp
from ydk.models.openconfig.openconfig_bgp_types import Ipv4UnicastIdentity as OpenConfig_Ipv4UnicastIdentity
from ydk.models.ietf.iana_if_type import SoftwareloopbackIdentity

from ydk.models.cisco_ios_xr import Cisco_IOS_XR_ipv4_bgp_datatypes as xr_ipv4_bgp_datatypes
from ydk.services.crud_service import CRUDService
from ydk.providers import NetconfServiceProvider
import ydk.types
from  ydk.models.ietf.ietf_interfaces import InterfaceTypeIdentity

# HOST = '10.62.38.90'
# PORT = 830
# USER = 'cisco'
# PASS = 'cisco'

class dvulovic_NETCONF_Device:

    def __init__(self, host, port, username, password):

        self.host = host
        self.port = port
        self.username = username
        self.password = password

        self.m = manager.connect(host=self.host, port=self.port, username=self.username, password=self.password, hostkey_verify=False)

        self.ydk_provider = NetconfServiceProvider(address=self.host, port=self.port, username=self.username, password=self.password, protocol='ssh')

        self.ydk_crud = CRUDService()

class dvulovic_IOSXR(dvulovic_NETCONF_Device):

    def __init__(self, host, port, username, password):

        dvulovic_NETCONF_Device.__init__(self, host, port, username, password)

    def add_config(self, config_e):
        with self.m.locked(target="candidate"):
            self.m.edit_config(config=config_e, default_operation="merge", target="candidate")
            self.m.commit()

    def delete_config(self, config_e):
        with self.m.locked(target="candidate"):
            self.m.edit_config(config=config_e, default_operation="none", target="candidate")
            self.m.commit()

    def put_test_config_edit(self):

        current_time = datetime.datetime.strftime(datetime.datetime.now(), '%Y-%m-%d %H:%M:%S')
        config_e = etree.Element("config")
        configuration = etree.SubElement(config_e, "interface-configurations",
                                         nsmap={None: 'http://cisco.com/ns/yang/Cisco-IOS-XR-ifmgr-cfg'})
        interface_cfg = etree.SubElement(configuration, "interface-configuration")
        active = etree.SubElement(interface_cfg, "active").text = 'act'
        interface_name = etree.SubElement(interface_cfg, "interface-name").text = 'GigabitEthernet0/0/0/0'
        description = etree.SubElement(interface_cfg, "description").text = 'NETCONF configured - ' + current_time

        # print(etree.tostring(config_e, pretty_print=True))

        self.add_config(config_e)

    def get_running_config(self, filter_string=None):
        if (filter_string is None):
            return self.m.get_config(source='running').data_xml
        else:
            return self.m.get_config(source='running',filter=filter_string).data_xml


class dvulovic_Generic_IOSXR_Model:

    def __init__(self, xr_device):
            self.xr = xr_device

class dvulovic_Native_IOSXR_Model(dvulovic_Generic_IOSXR_Model):

    def __init__(self, xr_device):
        dvulovic_Generic_IOSXR_Model.__init__(self, xr_device)

    def create_static_route_XML(self, arg_prefix,arg_prefixlen,arg_nexthop, delete=False):

        config_e = etree.Element("config", nsmap={'xc': 'urn:ietf:params:xml:ns:netconf:base:1.0'})
        router_static = etree.SubElement(config_e, "router-static", nsmap = {None: 'http://cisco.com/ns/yang/Cisco-IOS-XR-ip-static-cfg'})
        default_vrf = etree.SubElement(router_static, "default-vrf")
        address_family = etree.SubElement(default_vrf, "address-family")
        vrfipv4 = etree.SubElement(address_family, "vrfipv4")
        vrf_unicast = etree.SubElement(vrfipv4, "vrf-unicast")
        vrf_prefixes = etree.SubElement(vrf_unicast, "vrf-prefixes")
        vrf_prefix = etree.SubElement(vrf_prefixes, "vrf-prefix")

        prefix = etree.SubElement(vrf_prefix, "prefix")
        prefix.text = arg_prefix

        prefix_length = etree.SubElement(vrf_prefix, "prefix-length")
        prefix_length.text = arg_prefixlen

        vrf_route = etree.SubElement(vrf_prefix, "vrf-route")
        vrf_next_hop_table = etree.SubElement(vrf_route, "vrf-next-hop-table")
        vrf_next_hop_next_hop_address = etree.SubElement(vrf_next_hop_table, "vrf-next-hop-next-hop-address")

        if (delete is True):
            vrf_next_hop_next_hop_address.attrib[etree.QName("urn:ietf:params:xml:ns:netconf:base:1.0","operation")] = "delete"

        next_hop_address = etree.SubElement(vrf_next_hop_next_hop_address , "next-hop-address").text = arg_nexthop

        #print(etree.tostring(config_e, pretty_print=True).decode('utf-8'))

        return config_e

    def add_static_route(self, arg_prefix,arg_prefixlen,arg_nexthop):

        self.xr.add_config(self.create_static_route_XML(arg_prefix,arg_prefixlen,arg_nexthop))

    def delete_static_route(self, arg_prefix,arg_prefixlen,arg_nexthop):

        self.xr.delete_config(self.create_static_route_XML(arg_prefix,arg_prefixlen,arg_nexthop,delete=True))

    def get_running_config_interface(self):
        filter_subtree = '''
                                <filter type="subtree">
                                    <interface-configurations xmlns="http://cisco.com/ns/yang/Cisco-IOS-XR-ifmgr-cfg">
                                 </interface-configurations>
                                </filter>
                               '''

    #    return m.get_config(source='running',filter=filter_subtree).data_xml
        return self.xr.get_running_config(filter_subtree)


    def get_running_config_static_routes(self):
        filter_subtree = '''
                                <filter type="subtree">
                                    <router-static xmlns="http://cisco.com/ns/yang/Cisco-IOS-XR-ip-static-cfg">
                                    </router-static>
                                </filter>
                               '''

        return self.xr.get_running_config(filter_subtree)

    def IOSXR_prettyprint_static_routes_config(self):

        xml = self.get_running_config_static_routes()

        events = ("start", "end")

        for action, elem in etree.iterparse(BytesIO(bytes(xml,'utf-8')), events=events):
                #print("%s: %s" % (action, elem.tag))
                if (elem.tag == "{http://cisco.com/ns/yang/Cisco-IOS-XR-ip-static-cfg}prefix"):
                    prefix = elem.text
                else:
                    if (elem.tag == "{http://cisco.com/ns/yang/Cisco-IOS-XR-ip-static-cfg}prefix-length"):
                        prefix_length = elem.text
                    else:
                        if (action == "end" and elem.tag == "{http://cisco.com/ns/yang/Cisco-IOS-XR-ip-static-cfg}vrf-prefix"):
                            print ("%s/%s" % (prefix,prefix_length))

                        def check_if_static_route_exists(self, target_prefix, target_prefix_length, target_next_hop):

                            xml = self.xr_native_model.get_running_config_static_routes()

                            events = ("start", "end")

                            found_prefix = False
                            found_prefix_length = False
                            found_next_hop = False

                            for action, elem in etree.iterparse(BytesIO(bytes(xml, 'utf-8')), events=events):

                                if (elem.tag == "{http://cisco.com/ns/yang/Cisco-IOS-XR-ip-static-cfg}prefix"):
                                    if (elem.text == target_prefix):
                                        found_prefix = True

                                if (elem.tag == "{http://cisco.com/ns/yang/Cisco-IOS-XR-ip-static-cfg}prefix-length"):
                                    if (elem.text == target_prefix_length):
                                        found_prefix_length = True

                                if (
                                    elem.tag == "{http://cisco.com/ns/yang/Cisco-IOS-XR-ip-static-cfg}next-hop-address"):
                                    if (elem.text == target_next_hop):
                                        found_next_hop = True

                                if (
                                        action == "end" and elem.tag == "{http://cisco.com/ns/yang/Cisco-IOS-XR-ip-static-cfg}vrf-prefix"):
                                    if (
                                                found_prefix == True and found_prefix_length == True and found_next_hop == True):
                                        return True

                                    found_prefix = False
                                    found_prefix_length = False
                                    found_next_hop = False

                            return False

    def check_if_static_route_exists(self, target_prefix, target_prefix_length, target_next_hop):
        xml = self.get_running_config_static_routes()

        events = ("start", "end")

        found_prefix = False
        found_prefix_length = False
        found_next_hop = False

        for action, elem in etree.iterparse(BytesIO(bytes(xml, 'utf-8')), events=events):

            if (elem.tag == "{http://cisco.com/ns/yang/Cisco-IOS-XR-ip-static-cfg}prefix"):
                if (elem.text == target_prefix):
                    found_prefix = True

            if (elem.tag == "{http://cisco.com/ns/yang/Cisco-IOS-XR-ip-static-cfg}prefix-length"):
                if (elem.text == target_prefix_length):
                    found_prefix_length = True

            if (elem.tag == "{http://cisco.com/ns/yang/Cisco-IOS-XR-ip-static-cfg}next-hop-address"):
                if (elem.text == target_next_hop):
                    found_next_hop = True

            if (action == "end" and elem.tag == "{http://cisco.com/ns/yang/Cisco-IOS-XR-ip-static-cfg}vrf-prefix"):
                if (found_prefix == True and found_prefix_length == True and found_next_hop == True):
                    return True

                found_prefix = False
                found_prefix_length = False
                found_next_hop = False

        return False

class dvulovic_Native_IOSXR_Model_YDK(dvulovic_Native_IOSXR_Model):

    def __init__(self, xr_device):
        dvulovic_Native_IOSXR_Model.__init__(self, xr_device)

    def create_loopback(self, arg_loopbacknum, arg_ip, arg_mask):
        interface_configurations = Cisco_IOS_XR_ifmgr_cfg.InterfaceConfigurations()

        interface_configuration = interface_configurations.InterfaceConfiguration()

        interface_configuration.active = "act"
        interface_configuration.interface_name = "Loopback" + arg_loopbacknum
        interface_configuration.interface_virtual = ydk.types.Empty()

        #interface_configuration.description = "CONNECTS TO LSR1 (g0/0/0/1)"
        #mtu = interface_configuration.mtus.Mtu()
        #mtu.owner = "GigabitEthernet"
        #mtu.mtu = 9192
        #interface_configuration.mtus.mtu.append(mtu)

        #interface_configuration.statistics.load_interval = 30

        # regular_address = addresses.regular_addresses.RegularAddress()
        primary_address = interface_configuration.ipv4_network.addresses.Primary()
        primary_address.address = arg_ip
        primary_address.netmask = arg_mask

        interface_configuration.ipv4_network.addresses.primary = primary_address

        interface_configurations.interface_configuration.append(interface_configuration)

        self.xr.ydk_crud.create(self.xr.ydk_provider, interface_configurations)

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

    def add_bgp_neighbor(self, arg_asnumber, arg_neighbor_ip, arg_remote_as, arg_update_source = None):
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
        if(arg_update_source):
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
############################################################################################################
# with manager.connect(host=HOST, port=PORT, username=USER, password=PASS, hostkey_verify=False) as m:
#    c = m.get_config(source='running').data_xml
#    print (c)

#with manager.connect(host=HOST, port=PORT, username=USER, password=PASS, hostkey_verify=False) as m:
#    IOSXR_test_config_edit(m)
#    IOSXR_add_static_route(m,'3.3.3.3','32','30.30.30.30')
#    IOSXR_delete_static_route(m,'3.3.3.3','32','30.30.30.30')
#    print (IOSXR_get_running_config(m))
#    print (IOSXR_get_running_config_interface(m))
#    print (IOSXR_get_running_config_static_routes(m))
#    IOSXR_prettyprint_static_routes_config(m)

class dvulovic_OpenConfig_IOSXR_Model(dvulovic_Generic_IOSXR_Model):

    def __init__(self, xr_device):
        dvulovic_Generic_IOSXR_Model.__init__(self, xr_device)

    def create_bgp_procces(self, arg_asnumber):

        config_e = etree.Element("config", nsmap={'xc': 'urn:ietf:params:xml:ns:netconf:base:1.0'})
        bgp_e = etree.SubElement(config_e, "bgp", nsmap = {None: 'http://openconfig.net/yang/bgp'})
        global_e = etree.SubElement(bgp_e, "global")
        config2_e = etree.SubElement(global_e, "config")

        as_e = etree.SubElement(config2_e, "as")
        as_e.text = arg_asnumber

        # print(etree.tostring(config_e, pretty_print=True).decode('utf-8'))

        self.xr.add_config(config_e)
        return config_e

    def add_prefix_to_prefix_set(self, arg_name, arg_prefix, arg_prefixlen, delete=False):
        """
        <routing-policy xmlns="http://openconfig.net/yang/routing-policy">
           <defined-sets>
            <prefix-sets>
             <prefix-set>
              <prefix-set-name>PS-bgp-advertise</prefix-set-name>
              <prefix>
               <ip-prefix>172.16.101.0/24</ip-prefix>
               <masklength-range>exact</masklength-range>
              </prefix>
             </prefix-set>
            </prefix-sets>
           </defined-sets>
        """

        config_e = etree.Element("config", nsmap={'xc': 'urn:ietf:params:xml:ns:netconf:base:1.0'})

        rp_e = etree.SubElement(config_e, "routing-policy", nsmap = {None: 'http://openconfig.net/yang/routing-policy'})

        definedsets_e = etree.SubElement(rp_e, "defined-sets")

        psets_e = etree.SubElement(definedsets_e, "prefix-sets")

        pset_e = etree.SubElement(psets_e, "prefix-set")

        psetname_e = etree.SubElement(pset_e, "prefix-set-name")
        psetname_e.text = arg_name

        prefix_e = etree.SubElement(pset_e, "prefix")

        ipprefix_e = etree.SubElement(prefix_e, "ip-prefix")
        ipprefix_e.text = arg_prefix + "/" + arg_prefixlen

        masklen_e = etree.SubElement(prefix_e, "masklength-range")
        masklen_e.text = "exact"

        print(etree.tostring(config_e, pretty_print=True).decode('utf-8'))

        self.xr.add_config(config_e)
        return config_e

    def create_sample_RPL(self, arg_name, arg_psetname):
        """
        <routing-policy xmlns="http://openconfig.net/yang/routing-policy">
      <policy-definitions>
        <policy-definition>
          <name>RPL-oc-test</name>
          <statements>
            <statement>
              <name>test prefix</name>
              <conditions>
                <match-prefix-set>
                  <prefix-set>PS-bgp-advertise</prefix-set>
                  <match-set-options>ANY</match-set-options>
                </match-prefix-set>
              </conditions>
              <actions>
                <accept-route/>
              </actions>
            </statement>
            <statement>
              <name>reject</name>
              <actions>
                <reject-route/>
              </actions>
            </statement>
          </statements>
        </policy-definition>
      </policy-definitions>
        """

        config_e = etree.Element("config", nsmap={'xc': 'urn:ietf:params:xml:ns:netconf:base:1.0'})

        rp_e = etree.SubElement(config_e, "routing-policy", nsmap = {None: 'http://openconfig.net/yang/routing-policy'})

        poldefs_e = etree.SubElement(rp_e, "policy-definitions")

        poldef_e = etree.SubElement(poldefs_e, "policy-definition")

        polname_e = etree.SubElement(poldef_e, "name")
        polname_e.text = arg_name

        statements_e = etree.SubElement(poldef_e, "statements")

        statement1_e = etree.SubElement(statements_e, "statement")

        st1name_e = etree.SubElement(statement1_e, "name")
        st1name_e.text = "test prefix"

        st1cond_e = etree.SubElement(statement1_e, "conditions")

        st1matchps_e = etree.SubElement(st1cond_e, "match-prefix-set")

        st1pset_e = etree.SubElement(st1matchps_e, "prefix-set")
        st1pset_e.text = arg_psetname

        st1psetopts_e = etree.SubElement(st1cond_e, "match-set-options")
        st1psetopts_e.text = "ANY"

        st1actions_e = etree.SubElement(statement1_e, "actions")

        st1acceptroute_e = etree.SubElement(st1actions_e, "accept-route")

        statement2_e = etree.SubElement(statements_e, "statement")

        st2name_e = etree.SubElement(statement2_e, "name")
        st2name_e.text = "default reject"

        st2actions_e = etree.SubElement(statement2_e, "actions")

        st2rejectroute_e = etree.SubElement(st1actions_e, "reject-route")

        print(etree.tostring(config_e, pretty_print=True).decode('utf-8'))

        self.xr.add_config(config_e)
        return config_e

class dvulovic_OpenConfig_IOSXR_Model_YDK(dvulovic_OpenConfig_IOSXR_Model):

    def __init__(self, xr_device):
        dvulovic_OpenConfig_IOSXR_Model.__init__(self, xr_device)

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


    def create_bgp_procces(self, arg_asnumber):

        oc_bgp = OpenConfig_Bgp()
        oc_bgp.global_.config.as_ = arg_asnumber

        self.xr.ydk_crud.create(self.xr.ydk_provider, oc_bgp)

    def add_bgp_neighbor(self, arg_asnumber, arg_neighbor_ip, arg_remote_as, arg_update_source = None):
        oc_bgp = OpenConfig_Bgp()

        oc_neighor = oc_bgp.neighbors.Neighbor()
        oc_neighor.neighbor_address = arg_neighbor_ip
        oc_neighor.config.neighbor_address = arg_neighbor_ip
        oc_neighor.config.peer_as = arg_remote_as

        if(arg_update_source):
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