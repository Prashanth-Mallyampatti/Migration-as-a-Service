import ipaddress
import yaml
import sys

#def valid_ip_mask(ip):
#    try:
#        ip_addr = ipaddress.ip_network(ip)
#        return True
#    except ValueError:
#        return False

arg = sys.argv
print(arg)
#print(arg[2])
#print(arg[1])
try:
    ip_addr = ipaddress.ip_network(arg[1])
except ValueError:
    print("ERR: Not a valid subnet mask")

#with open("test.yaml",'r') as stream:
#    try:
#        yaml_content = yaml.safe_load(stream)
#        subnet = yaml_content['C1'][0]['subnet_addr']
#        print(subnet)
#    except yaml.YAMLError as exc:
#        print(exc)        
