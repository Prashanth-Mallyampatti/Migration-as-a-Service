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

# Reading the subnet that needs to be migrated from source cloud to destination cloud and updating the tenant.yml file 

with open(mig_file,'r') as stream:
    try:
        yaml_mig_content = yaml.safe_load(stream)
        #print(yaml_content)

        Cloud_Number = []
        for each in yaml_mig_content:
            i = 0
            #print(each)
            for item in yaml_mig_content[each]:
                if len(item) > 0:
                    i = i + 1
            #print(i)
            Cloud_Number.append(i)

        Source_Cloud = []
        for x in range(0,Cloud_Number[0],1):
            #print x
            sc = str(yaml_mig_content['VM_Migration'][x]['source_cloud'])
            subnet = str(yaml_mig_content['VM_Migration'][x]['source_subnet'])
            if sc == 'C1':
                print("Checking whether subnet is present in C2")
                if subnet in C2S:
                    print("The subnet: " + str(subnet) + " is present in C2")
                else:
                    print("The subnet: " + str(subnet) + " is not present in C2")
                    #print(yaml_content)
                    print("")
                    new_dict = {'subnet_addr': subnet, 'VM': [{'name': [], 'disk': [], 'mem': [], 'vcpu': []}]}
                    #print(new_dict)
                    print("")
                    #print(yaml_content)
                    #print(type(new_dict))

                    if 'C2' not in yaml_content:
                        yaml_content['C2'] = new_dict
                    yaml_content['C2'].append(new_dict)
                    #print(yaml_content)
                    
                    with open(yaml_file,'w') as yamlfile:
                        yaml.dump(yaml_content, yamlfile,default_flow_style=False)
                    cmd = "sed -i '1 i\---' " + yaml_file
                    os.system(cmd)

            if sc == 'C2':
                print("Checking whether subnet is present in C1")
                if subnet in C1S:
                    print("The subnet: " + str(subnet) + " is present in C1")
                else:
                    print("The subnet: " + str(subnet) + " is not present in C1")
                    print("")
                    new_dict = {'subnet_addr': subnet, 'VM': [{'name': [], 'disk': [], 'mem': [], 'vcpu': []}]}
                    #print(new_dict)
                    print("")
                    #print(yaml_content)
                    #print(type(new_dict))

                    if 'C1' not in yaml_content:
                        yaml_content['C1'] = new_dict
                    yaml_content['C1'].append(new_dict)
                    #print(yaml_content)

                    with open(yaml_file,'w') as yamlfile:
                        yaml.dump(yaml_content, yamlfile,default_flow_style=False)
                    cmd = "sed -i '1 i\---' " + yaml_file
                    os.system(cmd)

            Source_Cloud.append(sc)


    except yaml.YAMLError as exception:
        print("Unable to load the migration.yml file")
        exit(1)

