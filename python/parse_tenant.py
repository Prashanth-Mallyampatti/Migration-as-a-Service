import ipaddress
import yaml
import os
import sys

def range_of_ips(ip, br, ip_range):
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

    return {'bridge_ip': ip_range[1],'net_mask': mask[1], 'bridge_name': br}, ip_range
  except ValueError:
    print("Not a valid IP range: " + str(ip_range))
    return None

arg = sys.argv
tenant_name = arg[1].split('.')[0]
Yaml_file = "/root/Migration-as-a-Service/ansible/config_files/" + str(arg[1])
SUBNET_KEY = "Subnet"
YAML_CONTENT = None

class Create_YAML_FILE():
  def __init__(self, file_name):
    self.file_name = file_name

  def parseSubnets(self, content_req):
    self.subnets = []
    with open(Yaml_file,'r') as stream:
      try:
        YAML_CONTENT = yaml.safe_load(stream)
      except OSError:
        print ("Creation of the directory %s failed" % path)

    self.contents = YAML_CONTENT[content_req]

    ns_counter = 0
    br_counter = 0
    ip_range = []
    subnet_list = []
    dns = []
    namespace = []
    for subnet_addr_and_vm in self.contents:
      subnet_addr = subnet_addr_and_vm["subnet_addr"]
      dns_list = {}
      ns_list = {}
      ns_counter += 1
      br_counter += 1
      ns_name = str(tenant_name) + "ns" + str(ns_counter)
      br_name = str(tenant_name) + "br" + str(br_counter)
      subnet_val, ip_range = range_of_ips(subnet_addr, br_name, ip_range)
      if subnet_val is None:
        exit()
      self.subnets.append(subnet_val)

      dns_list["brif"] = "dnsbrif"
      dns_list["dnsif"] = "dnsif"
      dns_list["dhcp_start"] = ip_range[2]
      dns_list["dhcp_end"] = ip_range[len(ip_range) - 2]
      dns.append([dns_list])

      ns_list["name"] = ns_name
      namespace.append([ns_list])
    
    for subnet_no, subnet in enumerate(self.subnets):
      subnet["dns"] = dns[subnet_no]
      subnet["namespace"] = namespace[subnet_no]

  def parseVMs(self):
    all_vm_lists = []
    for br_count, subnet_addr_and_vm in enumerate(self.contents, 1):
      vms = subnet_addr_and_vm["VM"]
      vm_lists = []
      for vm_count, vm in enumerate(vms, 1):
        vm_name = vm["name"]
        disk_size = vm["disk"]
        mem_size = vm["mem"]
        vcpus = vm["vcpu"]
        vm_list = {}
        vm_list["name"] = tenant_name + "_" + vm_name
        vm_list["disk"] = disk_size
        vm_list["mem"] = mem_size
        vm_list["vcpu"] = vcpus
        vm_list["vmif"] = vm_name + "if1"
        vm_list["brif"] = "br" + str(br_count) + "if" + str(vm_count)
        vm_lists.append(vm_list)
      all_vm_lists.append(vm_lists)

    for subnet_no, subnet in enumerate(self.subnets):
        subnet["vms"] = all_vm_lists[subnet_no]

  def dump_content(self, file_name):
    self.tenant = {}
    self.tenant[SUBNET_KEY] = self.subnets
    file_path = "/root/Migration-as-a-Service/" + tenant_name + "/"
    with open(file_path + file_name + ".yml", "w") as file:
      doc = yaml.dump(self.tenant, file, default_flow_style=False)

def main():
  obj = Create_YAML_FILE(arg[1])
  obj.parseSubnets("C1")
  obj.parseVMs()
  obj.dump_content("t1c1")
  obj.parseSubnets("C2")
  obj.parseVMs()
  obj.dump_content("t1c2")
main()
