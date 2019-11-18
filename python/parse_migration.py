import ipaddress
import yaml
import os
import sys
import re
import subprocess

# ******************** #
arg = sys.argv
tenant_name1 = arg[1].split('.')[0]
Yaml_file = "/root/Migration-as-a-Service/ansible/config_files/migration/" + str(arg[1])
YAML_CONTENT = None
INFRA_CONTENT = None
MIGRATION_KEY = "Migrate"

tenant_name = arg[1].split("_")[0]
C1_infra_file = "/root/Migration-as-a-Service/" + tenant_name + "/" + tenant_name + "c1.yml"
C2_infra_file = "/root/Migration-as-a-Service/" + tenant_name + "/" + tenant_name + "c2.yml"

class Create_YAML_FILE():
  def __init__(self, file_name):
    self.file_name = file_name

  def parse_Migration(self, content_req):
    self.subnets_C1 = []
    self.subnets_C2 = []

    with open(Yaml_file,'r') as stream:
      try:
        YAML_CONTENT = yaml.safe_load(stream)
      except OSError:
        print ("Creation of the directory %s failed" % path)
    
    self.contents = YAML_CONTENT[content_req]
    

    for migrate in self.contents:
      source_cloud = migrate["source_cloud"]
      source_subnet = migrate["source_subnet"]
      if source_cloud == "C1":
        with open(C1_infra_file,'r') as stream:
          try:
            INFRA_CONTENT = yaml.safe_load(stream)
          except OSError:
            print ("Creation of the directory %s failed" % path)
      
        self.infra_contents = INFRA_CONTENT["Subnet"]
      
        migrate_list = {}

        for infra in self.infra_contents:
          subnet_ip = infra["subnet_ip"]
          ns_name = infra["ns_name"]
          infra_vms = infra["vms"]
          bridge_name = infra["bridge_name"]

          if subnet_ip == source_subnet:
            migrate_list["ns_name"] = ns_name
            migrate_list["bridge_name"] = bridge_name
            VM = migrate["VM"]
            vm = []
            for vms in VM:
              vm_list = {}
              vm_list["name"] = tenant_name + "_" + vms["name"]
              for infra_vm in infra_vms:
                if vm_list["name"] == infra_vm["name"]:
                  vm_list["vmif"] = infra_vm["vmif"]
                  vm_list["vmif_m"] = infra_vm["vmif"] + "_m"
                  vm_list["brif_m"] = infra_vm["brif"] + "_m"
                  cmd = "virsh domiflist " + vm_list["name"] + " |  awk 'FNR==3{ print $5 }'"
                  stream = os.popen(cmd)
                  out = stream.read()
                  vm_list["vm_mac"] = out.rstrip()
              vm.append(vm_list)
            migrate_list["VM"] = vm
        self.subnets_C1.append(migrate_list)
        file_name = "/root/Migration-as-a-Service/" + tenant_name1 + "/" + tenant_name1 + "C1.yml"
      print(source_cloud) 
      if source_cloud == "C2":
        with open(C2_infra_file,'r') as stream:
          try:
            INFRA_CONTENT = yaml.safe_load(stream)
          except OSError:
            print ("Creation of the directory %s failed" % path)
    
        self.infra_contents = INFRA_CONTENT["Subnet"]
    
        migrate_list = {}

        for infra in self.infra_contents:
          subnet_ip = infra["subnet_ip"]
          ns_name = infra["ns_name"]
          infra_vms = infra["vms"]
          bridge_name = infra["bridge_name"]

          if subnet_ip == source_subnet:
            migrate_list["ns_name"] = ns_name
            migrate_list["bridge_name"] = bridge_name
            VM = migrate["VM"]
            vm = []
            for vms in VM:
              vm_list = {}
              vm_list["name"] = tenant_name + "_" + vms["name"]
              for infra_vm in infra_vms:
                if vm_list["name"] == infra_vm["name"]:
                  vm_list["vmif"] = infra_vm["vmif"]
                  vm_list["vmif_m"] = infra_vm["vmif"] + "_m"
                  vm_list["brif_m"] = infra_vm["brif"] + "_m"
                  cmd = "virsh domiflist " + vm_list["name"] + " |  awk 'FNR==3{ print $5 }'"
                  stream = os.popen(cmd)
                  out = stream.read()
                  vm_list["vm_mac"] = out.rstrip()
              vm.append(vm_list)
            migrate_list["VM"] = vm
        
        file_name = "/root/Migration-as-a-Service/" + tenant_name1 + "/" + tenant_name1 + "C2.yml"
        self.subnets_C2.append(migrate_list)
        print(self.subnets_C2)
    
      self.dump_content(file_name, source_cloud)
    
  def dump_content(self, file_name, source_cloud):
    self.tenant = {}
    if source_cloud == "C1":
      self.tenant[MIGRATION_KEY] = self.subnets_C1
    if source_cloud == "C2":
      self.tenant[MIGRATION_KEY] = self.subnets_C2
    with open(file_name, "w") as file:
      doc = yaml.dump(self.tenant, file, default_flow_style=False)


def main():
  obj = Create_YAML_FILE(arg[1])

  with open(Yaml_file,'r') as stream:
      try:
        YAML_CONTENT = yaml.safe_load(stream)
      except OSError:
        print ("Creation of the directory %s failed" % path)

  if "VM_Migration" in YAML_CONTENT:
    obj.parse_Migration("VM_Migration")
main()
