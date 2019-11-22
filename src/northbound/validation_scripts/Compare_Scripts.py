####################################################################
# Script to validate the config file for the tenant
# If the script fails, the infrastructure will not be created
###################################################################

import sys
import os
import yaml
import ipaddress
import logging
import datetime


# Logging File
logging.basicConfig(filename="/root/Migration-as-a-Service/var/logs/infrastructure.log", level = logging.INFO)

# yaml config file as parameter
arg = sys.argv
Yaml_file = os.path.join('/root/Migration-as-a-Service/src/northbound/config_files/infrastructure', arg[1])

# Read the config file
with open(Yaml_file,'r') as stream:
    try:
        yaml_content = yaml.safe_load(stream)
        print(yaml_content)
        
        Cloud_Number = []
        for each in yaml_content:
            i = 0
            print(each)
            for item in yaml_content[each]:
                if len(item) > 0:
                    i = i + 1
            print(i)
            Cloud_Number.append(i)

        # Listing all number of subnets in the C1 and C2
        print("List of subnets in the C1:")
        print("--------------------------")

        C1S = []
        for x in range(0,Cloud_Number[0],1):
            subnet = str(yaml_content['C1'][x]['subnet_addr'])
            try:
                ip_addr = ipaddress.ip_network(subnet)
                logging.info(' ' + str(datetime.datetime.now().time()) + ' ' + 'Provided subnet in C1: ' + subnet + ' is valid')
                C1S.append(subnet)
            except ValueError:
                logging.error(' ' + str(datetime.datetime.now().time()) + ' ' + 'Provided subnet in C1: ' + subnet + ' is not valid')
            if subnet in C1S:
                print("ERR: Duplicate subnet found in C1")
                logging.error(' ' + str(datetime.datetime.now().time()) + ' ' + 'Duplicate subnet in C1: ' + subnet)
                exit()

            #print(subnet)
#        print (C1S)
        
        print("List of subnets in the C2:")
        print("--------------------------")

        C2S = []
        for x in range(0,Cloud_Number[1],1):
            subnet = str(yaml_content['C2'][x]['subnet_addr'])
            try:
                ip_addr = ipaddress.ip_network(subnet)
                logging.info(' ' + str(datetime.datetime.now().time()) + ' ' + 'Provided subnet in C2: ' + subnet + ' is valid')
                C2S.append(subnet)
            except ValueError:
                logging.error(' ' + str(datetime.datetime.now().time()) + ' ' + 'Provided subnet in C2: ' + subnet + ' is not valid')
            if subnet in C2S:
                print("ERR: Duplicate subnet found in C2")
                logging.error(' ' + str(datetime.datetime.now().time()) + ' ' + 'Duplicate subnet in C2: ' + subnet)
                exit()
            #print(subnet)
#        print (C2S)

        #print(C1S)
        #print(C2S)

    except yaml.YAMLError as exc:
        print(exc)

