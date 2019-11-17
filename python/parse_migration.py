import ipaddress
import yaml
import os
import sys


# ******************** #
arg = sys.argv
tenant_name = arg[1].split('.')[0]
Yaml_file = "/root/Migration-as-a-Service/ansible/config_files/migration/" + str(arg[1])
YAML_CONTENT = None
INFRA_CONTENT = None
MIGRATION_KEY = "Migrate"

tenant_name = arg[1].split("_")[0]
C1_infra_file = "/root/Migration-as-a-Service/" + tenant_name + "/" + tenant_name + "c1.yml"
C2_infra_file = "/root/Migration-as-a-Service/" + tenant_name + "/" + tenant_name + "c2.yml"

print(C1_infra_file)

class Create_YAML_FILE():
  def __init__(self, file_name):
    self.file_name = file_name

  def parse_Migration(self, content_req):
    self.subnets = []

    with open(Yaml_file,'r') as stream:
      try:
        YAML_CONTENT = yaml.safe_load(stream)
      except OSError:
        print ("Creation of the directory %s failed" % path)
    
    self.contents = YAML_CONTENT[content_req]
    
    migration = []

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
        if subnet_ip == source_subnet:
          migrate_list["ns_name"] = ns_name
          migration.append([migrate_list])

      self.subnets.append(migrate_list)
    
  def dump_content(self, file_name):
    self.tenant = {}
    self.tenant[MIGRATION_KEY] = self.subnets
    print(self.subnets)
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
    file_name = "/root/Migration-as-a-Service/" + tenant_name + "/" + tenant_name + ".yml"
    obj.parse_Migration("VM_Migration")
    obj.dump_content(file_name)
main()
