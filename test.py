from YDchunK_IOSXR_Native_dvulovic import YDchunK_IOSXR_Native_static_dvulovic
from YDchunK_IOSXR_Native_dvulovic import YDchunK_IOSXR_Native_interface_dvulovic
from YDchunK_common import YDchunK_IOSXR_Device
import logging

#logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',level=logging.DEBUG)
#logger = logging.getLogger('test')

#device = YDchunK_IOSXR_Device("127.0.0.1", 2223,"admin","admin")
device = YDchunK_IOSXR_Device("198.18.134.29", 830,"cisco","cisco")

ydck1 = YDchunK_IOSXR_Native_static_dvulovic(device)
ydck1.print_static_route()
ydck1.add_static_route("13.11.11.0",24," 100.100.100.100")
print ("added new route 13.11.11.0/24")
ydck1.print_static_route()
if (ydck1.check_if_static_route_exists("13.11.11.0",24," 100.100.100.100")):
    print ("13.11.11.0/24 exists")
else:
    print ("13.11.11.0/24 does not exist")
ydck1.delete_static_route("13.11.11.0",24," 100.100.100.100")
print ("deleted route 13.11.11.0/24")
ydck1.print_static_route()
if (ydck1.check_if_static_route_exists("13.11.11.0",24," 100.100.100.100")):
    print ("13.11.11.0/24 exists")
else:
    print ("13.11.11.0/24 does not exist")
#ydck2 = YDchunK_IOSXR_Native_interface_dvulovic(device)
#ydck2.print_interfaces()


