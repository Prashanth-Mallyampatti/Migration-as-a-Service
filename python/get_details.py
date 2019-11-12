import ipaddress
import yaml
import os
import sys

def range_of_ips(ip, ns, br):
  try:
    ip_range = []
    network_mask = ipaddress.IPv4Network(ip)
    mask = (str(network_mask.with_netmask)).split("/")
    for addr in ipaddress.IPv4Network(ip):
      ip_range.append(str(addr))
    length = len(ip_range)
    ip_range_hosts = ""
    for i in range(2,length-1,1):
      ip_range_hosts = str(ip_range_hosts) + str(ip_range[i]) + ","

    return {'dhcp_start':ip_range[2], 'dhcp_end':ip_range[length-2],'bridge_ip': ip_range[1],'net_mask': mask[1], 'ns_name': ns, 'bridge_name': br}
  except ValueError:
    print("Not a valid IP range: " + str(ip_range))
    return None

arg = sys.argv
tenant_name = arg[1].split('.')[0]
Yaml_file = "/root/Migration-as-a-Service/ansible/config_files/" + str(arg[1])
ns_counter = 0
br_counter = 0
SUBNET_KEY = "Subnet"
YAML_CONTENT = None

class Create_YAML_FILE():
  def __init__(self, file_name):
    self.file_name = file_name

  def create_tenant(self, content_req):
    self.subnets = []
    with open(Yaml_file,'r') as stream:
      try:
        YAML_CONTENT = yaml.safe_load(stream)
      except OSError:
        print ("Creation of the directory %s failed" % path)

    self.contents = YAML_CONTENT[content_req]

    ns_counter = 0
    br_counter = 0
    subnet_list = []
    for subnet_addr_and_vm in self.contents:
      subnet_addr = subnet_addr_and_vm["subnet_addr"]
      ns_counter += 1
      br_counter += 1
      ns_name = str(tenant_name) + "ns" + str(ns_counter)
      br_name = str(tenant_name) + "br" + str(br_counter)
      subnet_val = range_of_ips(subnet_addr, ns_name, br_name)
      if subnet_val is None:
        exit()
      self.subnets.append(subnet_val)

  def add_veth_pairs(self):
    all_veth_pairs = [] 
    for br_count, subnet_addr_and_vm in enumerate(self.contents, 1):
      vms = subnet_addr_and_vm["VM"]
      veth_pairs = []
      for vm_count, vm in enumerate(vms, 1):
        vm_name = vm["name"]
        veth_pair = {}
        veth_pair["vmif"] = vm_name + "if1"
        veth_pair["brif"] = "br" + str(br_count) +"if" +  str(vm_count)
        veth_pairs.append(veth_pair)
      all_veth_pairs.append(veth_pairs)

    for subnet_no, subnet in enumerate(self.subnets):
        subnet["veth_pairs"] = all_veth_pairs[subnet_no]

  def dump_content(self, file_name):
    self.tenant = {}
    self.tenant[SUBNET_KEY] = self.subnets
    file_path = "/root/Migration-as-a-Service/" + tenant_name + "/"
    with open(file_path + file_name + ".yml", "w") as file:
      doc = yaml.dump(self.tenant, file, default_flow_style=False)

def main():
  obj = Create_YAML_FILE(arg[1])
  obj.create_tenant("C1")
  obj.add_veth_pairs()
  obj.dump_content("t1c1")
  obj.create_tenant("C2")
  obj.add_veth_pairs()
  obj.dump_content("t1c2")
main()
