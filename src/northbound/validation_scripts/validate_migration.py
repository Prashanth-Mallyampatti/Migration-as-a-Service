############################################################################
# Script that validates the migration config yaml file provided
# by tenant in /root/Migration-as-a-Service/src/northbound/config_files/migration
############################################################################

import ipaddress
import yaml
import sys
import datetime
import logging
import os
import subprocess

subnet = ""

# Reading the subnets and the VMS
arg = sys.argv

# Logging file
logging.basicConfig(filename="/root/Migration-as-a-Service/var/logs/infrastructure.log", level=logging.INFO)

Yaml_File = "/root/Migration-as-a-Service/src/northbound/config_files/infrastructure/" + arg[1]
Migration_File = "/root/Migration-as-a-Service/src/northbound/config_files/migration/" + arg[2]
#print(Yaml_File)

with open(Yaml_File,'r') as stream:
    try:
        yaml_content = yaml.safe_load(stream)
        #print(yaml_content)

        Cloud_Number = []
        for each in yaml_content:
            i = 0
         #   print(each)
            for item in yaml_content[each]:
                if len(item) > 0:
                    i = i + 1
          #  print(i)
            Cloud_Number.append(i)
       # print("==========================")
       # print(Cloud_Number)
        
       # print("List of subnets in the C1:")
       # print("--------------------------")

        C1S = []
        for x in range(0,Cloud_Number[0],1):
            subnet = str(yaml_content['C1'][x]['subnet_addr'])
            C1S.append(subnet)
 #       print(C1S)

        C2S = []
        for x in range(0,Cloud_Number[1],1):
            subnet = str(yaml_content['C2'][x]['subnet_addr'])
            C2S.append(subnet)
  #      print(C2S)

        VMC1 = []
        for x in range(0,Cloud_Number[0],1):
            VM = yaml_content['C1'][x]['VM']
            #print(VM)
            for vm in VM:
                vm_name = vm["name"]
                #print (vm_name)
                VMC1.append(vm_name)
   #     print(VMC1)

        VMC2 = []        
        for x in range(0,Cloud_Number[1],1):
            VM = yaml_content['C2'][x]['VM']
            #print(VM)
            for vm in VM:
                vm_name = vm["name"]
                #print (vm_name)
                VMC2.append(vm_name)
    #    print(VMC2)

    except yaml.YAMLError as exc:
        logging.error(' ' + str(datetime.datetime.now().time()) + ' ' + "Unable to parse the content of yaml file:" + Yaml_File )


with open(Migration_File,'r') as stream:
    try:
        yaml_content = yaml.safe_load(stream)
        #print(yaml_content)
        #logging.info(' ' + str(datetime.datetime.now().time()) + ' ' + str(yaml_content)))
        source_cloud = []
        for each in yaml_content:
            i = 0
         #   print(each)
            for item in yaml_content[each]:
                if len(item) > 0:
                    i = i + 1
          #  print(i)
            source_cloud.append(i)

       # print("==========================")
       # print(source_cloud)

        SC = []
        source_subnet_C1 = []
        source_subnet_C2 = []
        for x in range(0,source_cloud[0],1):
            test = yaml_content['VM_Migration'][x]['source_cloud']
        #    print(test)
            if test == "C1":
                test1 = yaml_content['VM_Migration'][x]['source_subnet']
                source_subnet_C1.append(test1)
            else:
                test1 = yaml_content['VM_Migration'][x]['source_subnet']
                source_subnet_C2.append(test1)
        
#        print(source_subnet_C1)
#        print(source_subnet_C2)
       
        VM_Mig_FC1 = []
        VM_Mig_FC2 = []
        for x in range(0,source_cloud[0],1):
            VM = yaml_content['VM_Migration'][x]['VM']
            if yaml_content['VM_Migration'][x]['source_cloud'] == "C1":
                for vm in VM:
                    vm_name = vm["name"]
                    #print (vm_name)
                    VM_Mig_FC1.append(vm_name)
            else:
                for vm in VM:
                    vm_name = vm["name"]
                    #print (vm_name)
                    VM_Mig_FC2.append(vm_name)
#        print(VM_Mig_FC1)
#        print(VM_Mig_FC2)

        # Checking the Subnets is present or not
        for x in source_subnet_C1:
            if x in C1S:
                logging.info(' ' + str(datetime.datetime.now().time()) + ' ' + "The subnet " + x + " is present in Cloud 1")
            else:
                logging.error(' ' + str(datetime.datetime.now().time()) + ' ' + "The subnet " + x +" is not present in Cloud 1")
                exit(1)

        for y in source_subnet_C2:
            if y in C2S:
                logging.info(' ' + str(datetime.datetime.now().time()) + ' ' + "The subnet " + y + " is present in Cloud 2")
            else:
                logging.error(' ' + str(datetime.datetime.now().time()) + ' ' + "The subnet " + y +" is not present in Cloud 2")
                exit(1)


        # Checking the VMs is present or not
        for x in VM_Mig_FC1:
            if x in VMC1:
                logging.info(' ' + str(datetime.datetime.now().time()) + ' ' + "The VM " + x +" is present in Cloud 1")
            else:
                logging.error(' ' + str(datetime.datetime.now().time()) + ' ' + "The VM " + x +" is not present in Cloud 1")
                exit(1)

        for y in VM_Mig_FC2:
            if y in VMC2:
                 logging.info(' ' + str(datetime.datetime.now().time()) + ' ' + "The VM " + y +" is present in Cloud 2")
            else:
                logging.error(' ' + str(datetime.datetime.now().time()) + ' ' + "The VM " + y +" is not present in Cloud 2")
                exit(1)



        #check if the VM belong to respective subnets
        

        # Checking whether the subnet is present in the remote host where the instance needs to be migrated
        for x in range(0,source_cloud[0],1):
            test = yaml_content['VM_Migration'][x]['source_cloud']
            print(test)
            if test == "C1":
                x = yaml_content['VM_Migration'][x]['source_subnet']
                if x in source_subnet_C2:
                    logging.info(' ' + str(datetime.datetime.now().time()) + ' ' + "The subnet " + x + " is present in destination cloud")
                else:
                    logging.error(' ' + str(datetime.datetime.now().time()) + ' ' + "The subnet " + x + " is not present in the destination cloud")
            if test == "C2":
                #for x in source_subnet_C2:
                x = yaml_content['VM_Migration'][x]['source_subnet']
                if x in source_subnet_C1:
                    logging.info(' ' + str(datetime.datetime.now().time()) + ' ' + "The subnet " + x + " is present in destination cloud")
                else:
                    logging.error(' ' + str(datetime.datetime.now().time()) + ' ' + "The subnet " + x + " is not present in the destination cloud")


    except yaml.YAMLError as exc:
        logging.error(' ' + str(datetime.datetime.now().time()) + ' ' + "Unable to parse the content of migration yaml file: "+ Migration_File)
