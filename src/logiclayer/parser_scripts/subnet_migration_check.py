import sys
import os
import yaml
import logging
import datetime

arg = sys.argv
#print(arg)
yaml_file = '/root/Migration-as-a-Service/src/northbound/config_files/infrastructure/' + arg[1]
mig_file = '/root/Migration-as-a-Service/src/northbound/config_files/migration/' + arg[2]
#print("The details of subnets in the Tenant t1.yml")


# Reading the Cloud - subnet details from the tenant.yaml file

with open(yaml_file,'r') as stream:
    try:
        yaml_content = yaml.safe_load(stream)
        #print(yaml_content)
        test = yaml_content

        Cloud_Number = []
        for each in yaml_content:
            i = 0
            #print(each)
            for item in yaml_content[each]:
                if len(item) > 0:
                    i = i + 1
            #print(i)
            Cloud_Number.append(i)

        C1S = []
        for x in range(0,Cloud_Number[0],1):
            #print x
            subnet = str(yaml_content['C1'][x]['subnet_addr'])
            C1S.append(subnet)
        print("Subnets in Cloud1 as per tenant's input")
        print(C1S)

        C2S = []
        for x in range(0,Cloud_Number[1],1):
            #print x
            subnet = str(yaml_content['C2'][x]['subnet_addr'])
            C2S.append(subnet)
        print("Subnets in Cloud2 as per tenant's input")
        print(C2S)

    except yaml.YAMLError as exception:
        print('Unable to load the tenant.yml file')
        exit(1)

   
with open(mig_file,'r') as stream:
    try:
        yaml_mig_content = yaml.safe_load(stream)
        Source_Cloud = []
        if yaml_mig_content['Subnet_Migration'] is None:
            print("No request for subnet migration found")
            exit(1)
        for x in yaml_mig_content['Subnet_Migration']:
            print(x)
            sc = str(x['source_cloud'])
            print(sc)
            subnet = str(x['subnet_addr'])
            print(subnet)
            print(yaml_mig_content['VM_Migration'])
            print("===========================")
            VM = []
            for y in yaml_content[sc]:
                if y["subnet_addr"] == subnet:
                    for z in y["VM"]:
                        if sc == 'C2':
                            new_dict = {'VM': [{'name': z["name"]}], 'source_cloud': 'C2', 'source_subnet': subnet, 'destination_cloud': 'C1'}
                            if yaml_mig_content['VM_Migration'] is None:
                              yaml_mig_content['VM_Migration'] = []
                            yaml_mig_content["VM_Migration"].append(new_dict)
                        else:
                            new_dict = {'VM': [{'name': z["name"]}], 'source_cloud': 'C1', 'source_subnet': subnet, 'destination_cloud': 'C2'}
                            if yaml_mig_content['VM_Migration'] is None:
                               yaml_mig_content['VM_Migration'] = []
                            yaml_mig_content["VM_Migration"].append(new_dict)
            print(yaml_mig_content)

    except yaml.YAMLError as exception:
        print('Unable to load the tenant_mig.yml file')
        exit(1)

with open(mig_file,'w') as yamlfile:
    yaml.dump(yaml_mig_content, yamlfile,default_flow_style=False)

with open(mig_file,'r') as stream:
    try:
        yaml_mig_content = yaml.safe_load(stream)
        print(yaml_mig_content)

        Cloud_Number = []
        for each in yaml_mig_content:
            i = 0
            print(each)
            for item in yaml_mig_content[each]:
                if len(item) > 0:
                   i = i + 1
            print(i)
            Cloud_Number.append(i)

            if sc == 'C1':
                if subnet in C1S:
                    if subnet in C2S:
                        print("Subnet is already present in the destination cloud C2. Subnet cannot be migrated")
                        exit(1)
                    else:
                        print("Subnet is not present in destination Cloud C2. Subnet can be migrated")
                else:
                    print("Subnet not present in cloud C1. Error in tenant migration file")
                    exit(1)
        
            elif sc == 'C2':
                if subnet in C2S:
                    if subnet in C1S:
                        print("Subnet is already present in the destination cloud C1. Subnet cannot be migrated")
                        exit(1)
                    else:
                        print("Subnet is not present in destination Cloud C1. Subnet can be migrated")
                else:
                    print("Subnet not present in cloud C2. Error in tenant migration file")
                    exit(1)
            else:
                print("ERR: The provided cloud details is incorrect")
                exit(1)


    except yaml.YAMLError as exception:
        print('Unable to load the tenant_mig.yml file')
        exit(1)
 
