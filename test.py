from YDchunK_IOSXR_Native_dvulovic import YDchunK_IOSXR_Native_static_dvulovic
from YDchunK_IOSXR_Native_dvulovic import YDchunK_IOSXR_Native_interface_dvulovic
from YDchunK_common import YDchunK_IOSXR_Device
import logging
import argparse

def test_interfaces(device):
    ydck = YDchunK_IOSXR_Native_interface_dvulovic(device)
    ydck.print_interfaces()

def test_static_routes(device):

    ydck1 = YDchunK_IOSXR_Native_static_dvulovic(device)
    ydck1.print_static_route()
    ydck1.add_static_route("13.11.11.0",24,"100.100.100.100")
    print ("added new route 13.11.11.0/24")
    ydck1.print_static_route()
    if (ydck1.check_if_static_route_exists("13.11.11.0",24,"100.100.100.100")):
        print ("13.11.11.0/24 exists")
    else:
        print ("13.11.11.0/24 does not exist")
    ydck1.delete_static_route("13.11.11.0",24,"100.100.100.100")
    print ("deleted route 13.11.11.0/24")
    ydck1.print_static_route()
    if (ydck1.check_if_static_route_exists("13.11.11.0",24,"100.100.100.100")):
        print ("13.11.11.0/24 exists")
    else:
        print ("13.11.11.0/24 does not exist")

parser = argparse.ArgumentParser()
parser.add_argument('--debug', action='store_true', help="Debug Mode")
parser.add_argument('--host', help="Host")
parser.add_argument('--port', default = 830, help="NETCONF port (default 830)")
parser.add_argument('--username', default = "cisco", help="Username (default = cisco)")
parser.add_argument('--password', default = "cisco", help="Password (default = cisco)")
parser.add_argument('action', help="Action (test_interfaces, test_static_routes)")
args = parser.parse_args()

if args.debug:
    log_level = logging.DEBUG
    print ("Debug mode")
else:
    log_level = logging.ERROR
    print("Standard mode")

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',level=log_level)
logging.getLogger('ncclient.transport.ssh').setLevel(log_level)
logging.getLogger('ncclient.transport.session').setLevel(log_level)
logging.getLogger('ncclient.operations.rpc').setLevel(log_level)

#device = YDchunK_IOSXR_Device("127.0.0.1", 2223,"admin","admin")
#device = YDchunK_IOSXR_Device("198.18.134.29", 830,"cisco","cisco")

device = YDchunK_IOSXR_Device(args.host,args.port,args.username,args.password)

if args.action == 'test_interfaces':
    test_interfaces(device)
else:
    if args.action == 'test_static_routes':
        test_static_routes(device)
    else:
        print ("Uknown action: %s".format(args.action))

