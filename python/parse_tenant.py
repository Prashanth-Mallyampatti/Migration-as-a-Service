import ipaddress
import yaml
import os
import sys

def range_of_ips(ip):
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

    return {}, ip_range, mask[1]
  except ValueError:
    print("Not a valid IP range: " + str(ip_range))
    return None

def parse_DNS(C1_contents, C2):
  with open(Yaml_file,'r') as stream:
    try:
      YAML_CONTENT = yaml.safe_load(stream)
    except OSError:
      print ("Creation of the directory %s failed" % path)

  C2_contents = YAML_CONTENT[C2]
  for i in C2_contents:
    if C1_contents["subnet_addr"] == i["subnet_addr"]:
       return False
 
# ******************** #
arg = sys.argv
tenant_name = arg[1].split('.')[0]
Yaml_file = "/root/Migration-as-a-Service/ansible/config_files/" + str(arg[1])
SUBNET_KEY = "Subnet"
TENANT_KEY = "Namespace"
YAML_CONTENT = None
full_range = False

class Create_YAML_FILE():
  def __init__(self, file_name):
    self.file_name = file_name

  def parseSubnets(self, content_req):
    IP_COUNTER = 0
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
    dns = []
    tenant_ns = []
    vxlan = []
    route = []
    for subnet_addr_and_vm in self.contents:
      subnet_addr = subnet_addr_and_vm["subnet_addr"]
      dns_list = {}
      tenant_ns_list = {}
      vxlan_list = {}
      route_list = {}

      ns_counter += 1
      br_counter += 1
      ns_name = str(tenant_name) + "ns" + str(ns_counter)
      br_name = str(tenant_name) + "br" + str(br_counter)
      subnet_val, ip_range, mask = range_of_ips(subnet_addr)
      subnet_val["ns_name"] = ns_name
      subnet_val["bridge_name"] = br_name
      subnet_val["bridge_ip"] = ip_range[1]
      if subnet_val is None:
        exit()
      self.subnets.append(subnet_val)

      mask_num = subnet_addr.split("/")
      dns_list["brif"] = "dnsbrif"
      dns_list["dnsif"] = "dnsif"
      
      if content_req == "C1":
        full_range = parse_DNS(subnet_addr_and_vm, "C2")
        if full_range is False:
          dns_list["dnsif_ip"] = ip_range[1] + "/" + mask_num[1]
          dns_list["dhcp_start"] = ip_range[5]
          dns_list["dhcp_end"] = ip_range[len(ip_range)//2 - 2]
        else:
          dns_list["dnsif_ip"] = ip_range[1] + "/" + mask_num[1]
          dns_list["dhcp_start"] = ip_range[5]
          dns_list["dhcp_end"] = ip_range[len(ip_range) - 2]

      elif content_req == "C2":
        full_range = parse_DNS(subnet_addr_and_vm, "C1")
        if full_range is False:
          dns_list["dnsif_ip"] = ip_range[len(ip_range)//2] + "/" + mask_num[1]
          dns_list["dhcp_start"] = ip_range[len(ip_range)//2 + 5]
          dns_list["dhcp_end"] = ip_range[len(ip_range) - 2]
        else:
          dns_list["dnsif_ip"] = ip_range[1] + "/" + mask_num[1]
          dns_list["dhcp_start"] = ip_range[5]
          dns_list["dhcp_end"] = ip_range[len(ip_range) - 2]

      dns_list["net_mask"] = mask
      dns.append([dns_list])

      IP_COUNTER += 1
      ip = ((int(tenant_name[-1:]) - 1) * 10) + IP_COUNTER
      
      if content_req == "C1":
        tenant_ns_ip = "10.1." + str(ip) + ".1"
        tenant_sub_ip = "10.1." + str(ip) + ".2"
      
      if content_req == "C2":
        tenant_ns_ip = "10.2." + str(ip) + ".1"
        tenant_sub_ip = "10.2." + str(ip) + ".2"

      tenant_ns_list["tenant_ns_name"] = tenant_name
      tenant_ns_list["tenant_ns_if"] = tenant_name + "s" + str(br_counter) + "if"
      tenant_ns_list["tenant_sub_if"] = "s" + str(br_counter) + "if"
      tenant_ns_list["tenant_ns_ip"] = tenant_ns_ip + "/" + mask_num[1]
      tenant_ns_list["tenant_sub_ip"] = tenant_sub_ip + "/" + mask_num[1]

      tenant_ns.append([tenant_ns_list])
      
      subnet_val["default_route_ip"] = tenant_ns_ip
      if content_req == "C1":
        C2_contents = YAML_CONTENT["C2"]
        for subnet_C2 in C2_contents:
          subnet_addr_C2 = subnet_C2["subnet_addr"]
          if subnet_addr_C2 == subnet_addr:
            vxlan_list["v_name"] = "vxlan_" + tenant_name + "s" + str(br_counter)
            vxlan_list["local_ip"] = tenant_ns_list["tenant_sub_ip"].split("/")[0]
            vxlan_list["remote_ip"] = "10.2." + str(ip) + ".2"
            vxlan_list["id"] = 42
            vxlan_list["dsport"] = 4789
            vxlan_list["dev"] = tenant_ns_list["tenant_sub_if"]
            vxlan.append([vxlan_list])
            break
          else: 
            vxlan_list["v_name"] = []
            vxlan_list["local_ip"] = []
            vxlan_list["remote_ip"] = []
            vxlan_list["id"] = []
            vxlan_list["dsport"] = []
            vxlan_list["dev"] = []
            vxlan.append([vxlan_list])

      if content_req == "C2":
        C1_contents = YAML_CONTENT["C1"]
        for subnet_C1 in C1_contents:
          subnet_addr_C1 = subnet_C1["subnet_addr"]
          if subnet_addr_C1 == subnet_addr:
            vxlan_list["v_name"] = "vxlan_" + tenant_name + "s" + str(br_counter)
            vxlan_list["local_ip"] = tenant_ns_list["tenant_sub_ip"].split("/")[0]
            vxlan_list["remote_ip"] = "10.1." + str(ip) + ".2"
            vxlan_list["id"] = 42
            vxlan_list["dsport"] = 4789
            vxlan_list["dev"] = tenant_ns_list["tenant_sub_if"]
            vxlan.append([vxlan_list])
            break
          else:
            vxlan_list["v_name"] = []
            vxlan_list["local_ip"] = []
            vxlan_list["remote_ip"] = []
            vxlan_list["id"] = []
            vxlan_list["dsport"] = []
            vxlan_list["dev"] = []
            vxlan.append([vxlan_list])
      
      route_list["ip"] = tenant_ns_ip + "/" + mask_num[1]
      route_list["if"] = "p1"
      route_list["ns_name"] = tenant_name
      route_list["ns_if"] = tenant_name + "if"
      route.append([route_list])


    for subnet_no, subnet in enumerate(self.subnets):
      subnet["dns"] = dns[subnet_no]
      subnet["tenant_ns"] = tenant_ns[subnet_no]
      subnet["vxlan"] = vxlan[subnet_no]
      subnet["route"] = route[subnet_no]

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
  
  def parseTENANT(self, content_req):
    self.tenant_ns = []
    tenant_list = {}

    if content_req == "C1": 
      pns_ip = "192.168." + tenant_name[-1:] + ".1"
      tenant_ip = "192.168." + tenant_name[-1:] + ".2"
    if content_req == "C2":
      temp = 128 + int(tenant_name[-1:])
      pns_ip = "192.168." + str(temp) + ".1"
      tenant_ip = "192.168." + str(temp) + ".2"

    tenant_list["name"] = tenant_name
    tenant_list["tenant_if"] = tenant_name + "if"
    tenant_list["pns_if"] = tenant_name + "pns_if"
    tenant_list["pns_ip"] = pns_ip + "/24"
    tenant_list["tenant_ip"] = tenant_ip + "/24"
    tenant_list["default_route_ip"] = pns_ip
    self.tenant_ns = [tenant_list]

  def dump_content(self, file_name):
    self.tenant = {}
    self.tenant[SUBNET_KEY] = self.subnets
    self.tenant[TENANT_KEY] = self.tenant_ns
    file_path = "/root/Migration-as-a-Service/" + tenant_name + "/"
    with open(file_path + file_name + ".yml", "w") as file:
      doc = yaml.dump(self.tenant, file, default_flow_style=False)

def main():
  obj = Create_YAML_FILE(arg[1])

  with open(Yaml_file,'r') as stream:
      try:
        YAML_CONTENT = yaml.safe_load(stream)
      except OSError:
        print ("Creation of the directory %s failed" % path)

  if "C1" in YAML_CONTENT:
    obj.parseTENANT("C1")
    obj.parseSubnets("C1")
    obj.parseVMs()
    file_name = tenant_name + "c1"
    obj.dump_content(file_name)
  if "C2" in YAML_CONTENT:
    obj.parseTENANT("C2")
    obj.parseSubnets("C2")
    obj.parseVMs()
    file_name = tenant_name + "c2"
    obj.dump_content(file_name)
main()
