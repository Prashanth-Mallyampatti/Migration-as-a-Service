############################################################################
# This script is used to compare the subnets in the multicloud environment.
# The script reads the tenant config file and compares subnets in one cloud
# with subnets in another cloud to determine the spread of tenant subnets 
# across the multicloud environment. 
#
# If the same subnet is spread across multiple clouds, we need to ensure
# L2 connectivity between the subnets in different clouds.
############################################################################

import sys
import os
import yaml
import logging
import datetime

# Log file
logging.basicConfig(filename="/root/Migration-as-a-Service/var/logs/infrastructure.log", level=logging.INFO)

# Receive the yaml file of the tenant
arg = sys.argv
logging.info(' ' + str(datetime.datetime.now().time()) + ' ' + 'Invoking compare_script for ' + arg[1])
Yaml_file = os.path.join('/root/Migration-as-a-Service/src/northbound/config_files/infrastructure', arg[1])
print(Yaml_file)
# Read the yaml config file
with open(Yaml_file,'r') as stream:
    try:
        yaml_content = yaml.safe_load(stream)
        print(yaml_content)
        logging.info(' ' + str(datetime.datetime.now().time()) + ' ' + str(yaml_content))
        
        Cloud_Number = []
        for each in yaml_content:
            i = 0
            print(each)
            for item in yaml_content[each]:
                if len(item) > 0:
                    i = i + 1
            print(i)
            Cloud_Number.append(i)

        print(Cloud_Number)
        # Listing all subnets in the Cloud 1 and Cloud 2
        logging.info(' ' + str(datetime.datetime.now().time()) + ' ' + 'Listing all subnets in cloud 1')
        logging.info(' ' + str(datetime.datetime.now().time()) + ' ' + '--------------------------')

        C1S = []
        for x in range(0,Cloud_Number[0],1):
            #print x
            subnet = str(yaml_content['C1'][x]['subnet_addr'])
            C1S.append(subnet)
            logging.info(' ' + str(datetime.datetime.now().time()) + ' ' + str(subnet))

        #print("\n")
        logging.info(' ' + str(datetime.datetime.now().time()) + ' ' + 'Listing all subnets in cloud 2')
        logging.info(' ' + str(datetime.datetime.now().time()) + ' ' + '--------------------------')

        C2S = []
        for x in range(0,Cloud_Number[1],1):
            #print x
            subnet = str(yaml_content['C2'][x]['subnet_addr'])
            C2S.append(subnet)
            #print(subnet)
            logging.info(' ' + str(datetime.datetime.now().time()) + ' ' + str(subnet))

        #print(C1S)
        #print(C2S)

        # Identify if subnets are spread across clouds and create L2 tunnel
        # If tenant chooses to have routed gateway as a requirement,
        # ensure that all the subnets are reachable from each other
        compare_subnet_list_vxlan = []
        compare_subnet_list_gre = []
         
        for i in range(0,Cloud_Number[0],1):
            for j in range(0,Cloud_Number[1],1):
                if (C1S[i] == C2S[j]):
                    #print("Entered in to the if loop")
                    logging.info(' ' + str(datetime.datetime.now().time()) + ' ' + 'Identified same subnet across multiple clouds, create L2 tunnel')
                    test = str(C1S[i]) + ' - ' + str(C2S[j]) + ' - ' + 'VxLan'
                    #print(test)
                    compare_subnet_list_vxlan.append(test)
                else:
                    #TODO: Check if the tenant needs a routed gateway.
                    #      If yes, create L3 tunnel
                    #      If no, don not create anything
                    logging.info(' ' + str(datetime.datetime.now().time()) + ' ' + 'Identified multiple subnets across multiple clouds, create L3 tunnel')
                    test = str(C1S[i]) + ' - ' + str(C2S[j]) + ' - ' + 'GRE'
                    compare_subnet_list_gre.append(test)
    

        length = Cloud_Number[0] * Cloud_Number[1]
        
        len1 = len(compare_subnet_list_vxlan)
        len2 = len(compare_subnet_list_gre)
        
        if len1 > 0:
            for i in range(0,len1,1):
                logging.info(' ' + str(datetime.datetime.now().time()) + ' ' + compare_subnet_list_vxlan[i])
        if len2 > 0:
            for i in range(0,len2,1):
                #print(compare_subnet_list_gre[i])
                logging.info(' ' + str(datetime.datetime.now().time()) + ' ' + compare_subnet_list_gre[i])
    
        # Writing the list in to the file
        #path = '/home/ece792/LN_PROJECT/'
        path = '/root/Migration-as-a-Service/etc'
        #file_path = '/home/ece792/LN_PROJECT/Compare_Subnets_Across_Clouds.yaml'
        file_path = '/root/Migration-as-a-Service/etc/Compare_Subnets_Across_Clouds.yaml'
        try:
            if not os.path.exists(path):
                os.makedirs(path)
                logging.info(' ' + str(datetime.datetime.now().time()) + ' ' + 'Creating Compare_Subnets_Across_Clouds.yaml')
            else:
                #print("The file path already exists: "+ str(path))
                logging.info(' ' + str(datetime.datetime.now().time()) + ' ' + 'Compare_Subnets_Across_Clouds.yaml file exists')

        except OSError:
            #print ("Creation of the directory %s failed" % path)
            logging.error(' ' + str(datetime.datetime.now().time()) + ' ' + 'Failed to create Compare_Subnets_Across_Clouds.yaml')
        
        with open(file_path, 'w') as file:
            documents = yaml.dump(compare_subnet_list_vxlan, file, default_flow_style=False)
            documents = yaml.dump(compare_subnet_list_gre, file, default_flow_style=False)

    except yaml.YAMLError as exception:
        #print(exc)
        logging.error(' ' + str(datetime.datetime.now().time()) + ' ' + exception)

